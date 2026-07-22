"""Report + recommendation.

Ranked per-model results on quality / latency / cost, the judge's own trust
metrics, and a plain recommendation ("the right model for you") with the
trade-off stated honestly. Emits a Rich terminal table + committable
markdown + JSON.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .metrics import JudgeTrust, ModelStats
from .pricing import PRICING_AS_OF


def _recommend(stats: list[ModelStats]) -> dict[str, str]:
    # Only rank models that actually produced results — a fully-errored model
    # must not win "cheapest"/"fastest" on its $0 / 0ms placeholder.
    stats = [s for s in stats if s.error_rate < 1.0 and s.quality > 0]
    if not stats:
        return {}
    best_q = max(stats, key=lambda s: s.quality)
    cheapest = min(stats, key=lambda s: s.cost_per_1k)
    fastest = min(stats, key=lambda s: s.total_p50)
    # best value: cheapest model that keeps >=85% of the top quality
    thresh = 0.85 * best_q.quality
    value_pool = [s for s in stats if s.quality >= thresh]
    best_value = min(value_pool, key=lambda s: s.cost_per_1k) if value_pool else best_q
    return {
        "best_quality": best_q.model,
        "cheapest": cheapest.model,
        "fastest": fastest.model,
        "best_value": best_value.model,
    }


def _verdict_tags(stats: list[ModelStats], rec: dict[str, str]) -> dict[str, str]:
    tags: dict[str, list[str]] = {s.model: [] for s in stats}
    if rec.get("best_quality"):
        tags[rec["best_quality"]].append("★ best quality")
    if rec.get("best_value") and rec["best_value"] != rec.get("best_quality"):
        tags[rec["best_value"]].append("best value")
    if rec.get("cheapest") and "best value" not in tags[rec["cheapest"]]:
        tags[rec["cheapest"]].append("cheapest")
    if rec.get("fastest"):
        tags[rec["fastest"]].append("fastest")
    return {m: " · ".join(t) for m, t in tags.items()}


def _recommendation_line(stats: list[ModelStats], rec: dict[str, str]) -> str:
    by = {s.model: s for s in stats}
    bv, bq = rec.get("best_value"), rec.get("best_quality")
    if not bv or not bq:
        return "No recommendation (no results)."
    v, q = by[bv], by[bq]
    if bv == bq:
        return f"{bv} — top quality ({q.quality}) and a sensible default."
    q_pct = round(100 * v.quality / q.quality) if q.quality else 0
    cost_ratio = f"{q.cost_per_1k / v.cost_per_1k:.1f}×" if v.cost_per_1k else "much"
    return (
        f"{bv} — {q_pct}% of top quality (vs {bq}) at ~{cost_ratio} lower cost "
        f"(${v.cost_per_1k}/1k vs ${q.cost_per_1k}/1k), p50 {v.total_p50}ms."
    )


def render(
    project: str,
    n_inputs: int,
    stats: list[ModelStats],
    trust: JudgeTrust,
    synthetic: bool = True,
) -> str:
    rec = _recommend(stats)
    tags = _verdict_tags(stats, rec)
    console = Console()

    table = Table(title=f"METANOIA — {project}", title_style="bold")
    table.add_column("Model", style="bold")
    table.add_column("Quality", justify="right")
    table.add_column("TTFT", justify="right")
    table.add_column("p50", justify="right")
    table.add_column("p95", justify="right")
    table.add_column("$/1k", justify="right")
    table.add_column("Err", justify="right")
    table.add_column("Verdict")
    for s in stats:
        table.add_row(
            s.model, f"{s.quality:.2f}", f"{s.ttft_p50:.0f}ms", f"{s.total_p50:.0f}ms",
            f"{s.total_p95:.0f}ms", f"${s.cost_per_1k}", f"{s.error_rate:.0%}",
            tags.get(s.model, ""),
        )
    console.print()
    console.print(table)
    tail = "synthetic" if synthetic else "production"
    console.print(f"[dim]{n_inputs} {tail} inputs · pricing as of {PRICING_AS_OF}[/dim]")
    console.print()
    console.print(f"[bold green]Recommendation:[/bold green] {_recommendation_line(stats, rec)}")
    fr = "n/a" if trust.flip_rate is None else trust.flip_rate
    ag = "n/a (no gold)" if trust.agreement is None else trust.agreement
    tline = f"[bold]Judge trust:[/bold] agreement {ag} · consistency {trust.consistency} · flip-rate {fr} · self-pref {trust.self_pref} (n={trust.n_gold})"
    console.print(tline)
    for note in trust.notes:
        console.print(f"[yellow]⚠ {note}[/yellow]")
    console.print()
    return _markdown(project, n_inputs, stats, trust, rec, tags, synthetic)


def _markdown(project, n_inputs, stats, trust, rec, tags, synthetic) -> str:
    tail = "synthetic" if synthetic else "production"
    lines = [
        f"# Metanoia report — {project}",
        "",
        f"*{n_inputs} {tail} inputs · {date.today().isoformat()} · pricing as of {PRICING_AS_OF}*",
        "",
        "| Model | Quality | TTFT | p50 | p95 | $/1k | Err | Verdict |",
        "|---|--:|--:|--:|--:|--:|--:|---|",
    ]
    for s in stats:
        lines.append(
            f"| {s.model} | {s.quality:.2f} | {s.ttft_p50:.0f}ms | {s.total_p50:.0f}ms "
            f"| {s.total_p95:.0f}ms | ${s.cost_per_1k} | {s.error_rate:.0%} | {tags.get(s.model,'')} |"
        )
    lines += [
        "",
        f"**Recommendation:** {_recommendation_line(stats, rec)}",
        "",
        f"**Judge trust:** agreement `{trust.agreement if trust.agreement is not None else 'n/a'}` "
        f"· consistency `{trust.consistency}` "
        f"· flip-rate `{trust.flip_rate if trust.flip_rate is not None else 'n/a'}` "
        f"· self-pref `{trust.self_pref}` (n={trust.n_gold})",
    ]
    for note in trust.notes:
        lines.append(f"> ⚠ {note}")
    if synthetic:
        lines += ["", "> Synthetic run — treat as *where to start*, not a production verdict."]
    return "\n".join(lines) + "\n"


def write_report(
    root: Path, project: str, n_inputs: int, stats, trust, synthetic=True
) -> Path:
    md = render(project, n_inputs, stats, trust, synthetic)
    (root / "report.md").write_text(md)
    (root / "report.json").write_text(
        json.dumps(
            {
                "project": project,
                "n_inputs": n_inputs,
                "synthetic": synthetic,
                "models": [asdict(s) for s in stats],
                "judge_trust": asdict(trust),
                "recommendation": _recommend(stats),
            },
            indent=2,
        )
    )
    return root / "report.md"
