"""The judge core.

Design guarantees (from plan.md §11.2):
- Blinded to model identity (never sees the model name).
- Forced per-criterion structured output {score, reasoning, evidence}.
- Weighted roll-up to a quality score happens *in code*, so the verdict is
  provably a function of the criterion scores (not a vibe).
- Refuses to emit a verdict on schema-validation failure.
"""

from __future__ import annotations

import json
import math
import os

from pydantic import BaseModel, ValidationError

from .config import Rubric
from .providers import complete, mock_profile


class CriterionScore(BaseModel):
    name: str
    score: float
    reasoning: str = ""
    evidence: str = ""


class Verdict(BaseModel):
    scores: list[CriterionScore]
    quality: float  # weighted aggregate, computed in code

    def by_name(self) -> dict[str, float]:
        return {s.name: s.score for s in self.scores}


def _extract_json(text: str) -> dict:
    """Tolerate models that wrap JSON in ```json fences or surrounding prose."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    s = text.strip()
    if "```" in s:  # strip code fences
        parts = s.split("```")
        for p in parts:
            p = p.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            if p.startswith("{"):
                s = p
                break
    a, b = s.find("{"), s.rfind("}")
    if a != -1 and b != -1 and b > a:
        return json.loads(s[a : b + 1])
    raise json.JSONDecodeError("no JSON object found", text, 0)


def _aggregate(rubric: Rubric, scores: list[CriterionScore]) -> float:
    """Deterministic weighted roll-up — the faithfulness gate, in code."""
    w = {c.name: c.weight for c in rubric.criteria}
    return round(sum(s.score * w.get(s.name, 0.0) for s in scores), 4)


def _seed(*parts: str) -> int:
    import hashlib

    return int(hashlib.sha256("|".join(parts).encode()).hexdigest()[:12], 16)


def _mock_score(
    rubric: Rubric, hidden_model: str, input_text: str, repeat: int
) -> Verdict:
    """Simulate a competent, blinded judge.

    The mock judge 'perceives' the hidden model's true quality (its profile) plus
    per-criterion structure and a small amount of run-to-run noise (so
    self-consistency is realistically < 1.0).
    """
    q = mock_profile(hidden_model)["quality"]
    scores: list[CriterionScore] = []
    for c in rubric.criteria:
        base = _seed(c.name, hidden_model, input_text)
        crit_offset = ((base % 100) / 100.0 - 0.5) * 0.12
        noise_seed = _seed(c.name, hidden_model, input_text, str(repeat))
        noise = ((noise_seed % 100) / 100.0 - 0.5) * 0.10
        raw = (q + crit_offset + noise) * rubric.scale
        val = max(1.0, min(float(rubric.scale), round(raw)))
        scores.append(
            CriterionScore(
                name=c.name,
                score=val,
                reasoning=f"[mock] judged '{c.name}' from the output against: {c.guide or c.name}",
                evidence=input_text[:48].replace("\n", " ") + "…",
            )
        )
    return Verdict(scores=scores, quality=_aggregate(rubric, scores))


def _live_score(
    rubric: Rubric, output_text: str, task: str, input_text: str, judge_model: str
) -> Verdict:
    crit_desc = "\n".join(
        f"- {c.name} (1-{rubric.scale}): {c.guide}" for c in rubric.criteria
    )
    prompt = (
        "You are a rigorous, impartial evaluator. You are judging the output of an "
        "ANONYMOUS model (you do NOT know which model produced it — do not guess or "
        "let brand influence you).\n\n"
        f"TASK THE MODEL PERFORMED:\n{task}\n\n"
        f"INPUT GIVEN TO THE MODEL:\n{input_text}\n\n"
        f"MODEL OUTPUT TO JUDGE:\n{output_text}\n\n"
        f"Score EACH criterion from 1 to {rubric.scale}:\n{crit_desc}\n\n"
        "For each criterion, quote the specific span of the output that justifies "
        "the score. Return STRICT JSON:\n"
        '{"scores":[{"name":"...","score":N,"reasoning":"...","evidence":"..."}]}'
    )
    resp = complete(judge_model, prompt, temperature=0.0, max_tokens=1200, mock=False)
    try:
        data = _extract_json(resp.text)
        raw = [CriterionScore(**s) for s in data["scores"]]
    except (json.JSONDecodeError, KeyError, ValidationError, TypeError) as e:
        raise ValueError(f"judge returned invalid schema: {e}")

    got = {s.name for s in raw}
    want = {c.name for c in rubric.criteria}
    if got != want:
        raise ValueError(f"judge criteria {got} != rubric criteria {want}")
    for s in raw:
        s.score = max(1.0, min(float(rubric.scale), float(s.score)))
    return Verdict(scores=raw, quality=_aggregate(rubric, raw))


def score(
    rubric: Rubric,
    *,
    hidden_model: str,
    output_text: str,
    task: str,
    input_text: str,
    repeat: int = 0,
    judge_model: str | None = None,
    mock: bool | None = None,
) -> Verdict:
    """Score one output. `hidden_model` is used only by the mock judge to simulate
    perceived quality and to measure self-preference downstream — the live judge
    never receives it."""
    if mock is None:
        mock = os.environ.get("METANOIA_MOCK", "1") == "1"
    if mock:
        return _mock_score(rubric, hidden_model, input_text, repeat)
    jm = judge_model or os.environ.get("METANOIA_JUDGE_MODEL", "gpt-5")
    return _live_score(rubric, output_text, task, input_text, jm)


def pairwise_pick(
    rubric: Rubric,
    va: Verdict,
    vb: Verdict,
) -> str:
    """Higher aggregate quality wins; ties broken deterministically toward A."""
    return "A" if va.quality >= vb.quality else "B"
