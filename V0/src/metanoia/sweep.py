"""Sweep orchestration: fan every synthetic input across every candidate model,
capture output + latency + cost, then judge each output (blinded).

Results are cached by content hash and persisted as a full, replayable trace.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from .cache import Cache
from .config import Candidates, Rubric, SynthInputs, UseCase
from .judge import score
from .providers import Completion, complete


@dataclass
class Judged:
    input_id: str
    model: str
    output: str
    in_tokens: int
    out_tokens: int
    ttft_ms: float
    total_ms: float
    cost_usd: float
    quality: float
    criterion_scores: dict[str, float]
    reasoning: dict[str, str]
    evidence: dict[str, str]
    repeat_qualities: list[float] | None = None
    error: str | None = None


def _build_prompt(task: str, input_text: str) -> str:
    return f"{task}\n\n{input_text}"


def run_sweep(
    root: Path,
    uc: UseCase,
    cands: Candidates,
    rubric: Rubric,
    inputs: SynthInputs,
    *,
    repeats: int = 1,
    mock: bool | None = None,
) -> list[Judged]:
    if mock is None:
        mock = os.environ.get("METANOIA_MOCK", "1") == "1"
    cache = Cache(root)
    results: list[Judged] = []

    # Interleave: for each input, hit every candidate (round-robin), so
    # time-of-day / load effects hit all models evenly.
    for inp in inputs.inputs:
        prompt = _build_prompt(uc.task, inp.text)
        for model in cands.candidates:
            gkey = cache.key("gen", model, prompt, cands.temperature, cands.max_tokens)
            cached = cache.get(gkey)
            if cached:
                comp = Completion(**cached)
            else:
                comp = complete(
                    model,
                    prompt,
                    temperature=cands.temperature,
                    max_tokens=cands.max_tokens,
                    mock=mock,
                )
                cache.put(gkey, asdict(comp))

            # Judge (blinded). Repeat to measure self-consistency downstream.
            verdicts = []
            for r in range(repeats):
                v = score(
                    rubric,
                    hidden_model=model,
                    output_text=comp.text,
                    task=uc.task,
                    input_text=inp.text,
                    repeat=r,
                    mock=mock,
                )
                verdicts.append(v)
            primary = verdicts[0]

            results.append(
                Judged(
                    input_id=inp.id,
                    model=model,
                    output=comp.text,
                    in_tokens=comp.in_tokens,
                    out_tokens=comp.out_tokens,
                    ttft_ms=comp.ttft_ms,
                    total_ms=comp.total_ms,
                    cost_usd=comp.cost_usd,
                    quality=primary.quality,
                    criterion_scores=primary.by_name(),
                    reasoning={s.name: s.reasoning for s in primary.scores},
                    evidence={s.name: s.evidence for s in primary.scores},
                    repeat_qualities=[round(v.quality, 4) for v in verdicts],
                    error=comp.error,
                )
            )

    _persist(root, results, repeats)
    return results


def _persist(root: Path, results: list[Judged], repeats: int) -> None:
    trace = root / "runs" / "trace.json"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text(
        json.dumps(
            {"repeats": repeats, "results": [asdict(r) for r in results]}, indent=2
        )
    )


def load_trace(root: Path) -> tuple[int, list[Judged]]:
    data = json.loads((root / "runs" / "trace.json").read_text())
    return data.get("repeats", 1), [Judged(**r) for r in data["results"]]
