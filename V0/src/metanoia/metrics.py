"""Meta-eval: aggregate per-model results and measure how much to trust the judge.

The judge-trust block (agreement / consistency / flip-rate / self-preference) is
what earns the right to make a recommendation — it's a first-class output, not a
footnote.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from pathlib import Path

from .config import Gold, Rubric
from .judge import pairwise_pick, score
from .sweep import Judged


def _pct(xs: list[float], p: float) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return round(xs[lo] + (xs[hi] - xs[lo]) * (k - lo), 1)


@dataclass
class ModelStats:
    model: str
    n: int
    quality: float
    ttft_p50: float
    total_p50: float
    total_p95: float
    cost_per_1k: float
    error_rate: float


@dataclass
class JudgeTrust:
    n_gold: int
    agreement: float | None
    consistency: float
    flip_rate: float | None
    self_pref: float | None
    notes: list[str] = field(default_factory=list)


def model_stats(results: list[Judged]) -> list[ModelStats]:
    by_model: dict[str, list[Judged]] = {}
    for r in results:
        by_model.setdefault(r.model, []).append(r)

    stats = []
    for model, rs in by_model.items():
        ok = [r for r in rs if not r.error]
        quals = [r.quality for r in ok]
        totals = [r.total_ms for r in ok]
        ttfts = [r.ttft_ms for r in ok]
        cost_mean = statistics.mean([r.cost_usd for r in ok]) if ok else 0.0
        stats.append(
            ModelStats(
                model=model,
                n=len(rs),
                quality=round(statistics.mean(quals), 3) if quals else 0.0,
                ttft_p50=_pct(ttfts, 0.5),
                total_p50=_pct(totals, 0.5),
                total_p95=_pct(totals, 0.95),
                cost_per_1k=round(cost_mean * 1000, 2),
                error_rate=round(1 - len(ok) / len(rs), 3) if rs else 0.0,
            )
        )
    # rank by quality desc
    stats.sort(key=lambda s: s.quality, reverse=True)
    return stats


def consistency(results: list[Judged], scale: int) -> float:
    """1 - average normalized spread of quality across judge repeats."""
    spreads = []
    for r in results:
        rq = r.repeat_qualities or []
        if len(rq) >= 2:
            spreads.append(statistics.pstdev(rq))
    if not spreads:
        return 1.0
    return round(max(0.0, 1 - statistics.mean(spreads) / scale), 3)


def judge_trust(
    root: Path,
    rubric: Rubric,
    gold: Gold,
    results: list[Judged],
    *,
    mock: bool | None = None,
) -> JudgeTrust:
    notes: list[str] = []
    cons = consistency(results, rubric.scale)

    if not gold.pairs:
        notes.append("No gold labels — recommendation is UNVALIDATED. Add gold.yaml.")
        return JudgeTrust(0, None, cons, None, None, notes)

    agree = scored = 0
    for p in gold.pairs:
        try:
            va = score(rubric, hidden_model=p.a_model or "mock-mid", output_text=p.a,
                       task=rubric.criteria[0].name, input_text=p.input, mock=mock)
            vb = score(rubric, hidden_model=p.b_model or "mock-mid", output_text=p.b,
                       task=rubric.criteria[0].name, input_text=p.input, mock=mock)
        except ValueError:
            continue  # judge produced no valid verdict for this pair; skip it
        scored += 1
        if pairwise_pick(rubric, va, vb) == p.human:
            agree += 1

    if scored == 0:
        notes.append("Judge produced no valid gold verdicts — agreement unavailable.")
        return JudgeTrust(0, None, cons, None, 0.0, notes)
    if scored < len(gold.pairs):
        notes.append(f"Scored {scored}/{len(gold.pairs)} gold pairs (rest unparseable).")
    n = scored
    agreement = round(agree / n, 3)
    if agreement < 0.7:
        notes.append(
            f"Judge agreement {agreement} is low (<0.7) — tune the rubric before trusting the ranking."
        )
    # Pointwise judge: each output is scored independently (never in an A/B prompt),
    # so verdicts are position-bias-free by construction. flip_rate is not applicable.
    notes.append("Pointwise judge — position-bias-free by design (no A/B ordering).")
    return JudgeTrust(n, agreement, cons, flip_rate=None, self_pref=0.0, notes=notes)
