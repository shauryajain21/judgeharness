"""Metanoia CLI: init → synth → sweep → report.

Runs in mock mode by default (no API keys) so the full pipeline is testable
offline. Pass --live (or METANOIA_MOCK=0) to hit real models via litellm.
"""

from __future__ import annotations

import os
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .config import (
    load_candidates,
    load_gold,
    load_rubric,
    load_synth_inputs,
    load_usecase,
    write_yaml,
)
from .metrics import judge_trust, model_stats
from .report import write_report
from .scaffold import scaffold
from .sweep import load_trace, run_sweep
from .synth import synthesize

console = Console()


def _set_mock(live: bool) -> bool:
    mock = not live
    os.environ["METANOIA_MOCK"] = "0" if live else "1"
    return mock


@click.group(help="Transparent LLM judges for model selection.")
@click.version_option(__version__)
def cli() -> None:
    pass


@cli.command(help="Scaffold a new project directory.")
@click.argument("name")
def init(name: str) -> None:
    root = Path(name)
    if root.exists() and any(root.iterdir()):
        raise click.ClickException(f"{root} already exists and is not empty")
    scaffold(root)
    console.print(f"[green]✓[/green] scaffolded [bold]{root}[/bold]")
    console.print("Next: [bold]cd {0} && metanoia run[/bold]".format(name))


@cli.command(help="Generate synthetic inputs from usecase.yaml.")
@click.option("--root", default=".", help="Project directory")
@click.option("--live", is_flag=True, help="Use a real model to synthesize")
def synth(root: str, live: bool) -> None:
    r = Path(root)
    mock = _set_mock(live)
    uc = load_usecase(r)
    inputs = synthesize(uc, mock=mock)
    write_yaml(r / "inputs.yaml", inputs)
    console.print(f"[green]✓[/green] generated {len(inputs.inputs)} inputs → inputs.yaml")


@cli.command(help="Fan inputs across candidate models and judge each (blinded).")
@click.option("--root", default=".", help="Project directory")
@click.option("--repeats", default=3, help="Judge repeats (for consistency metric)")
@click.option("--live", is_flag=True, help="Call real models + judge via litellm")
def sweep(root: str, repeats: int, live: bool) -> None:
    r = Path(root)
    mock = _set_mock(live)
    uc, cands, rubric = load_usecase(r), load_candidates(r), load_rubric(r)
    inputs = load_synth_inputs(r)
    n_calls = len(inputs.inputs) * len(cands.candidates)
    console.print(
        f"Sweeping {len(inputs.inputs)} inputs × {len(cands.candidates)} models "
        f"= {n_calls} calls ({'MOCK' if mock else 'LIVE'})…"
    )
    results = run_sweep(r, uc, cands, rubric, inputs, repeats=repeats, mock=mock)
    console.print(f"[green]✓[/green] judged {len(results)} outputs → runs/trace.json")


@cli.command(help="Build the ranked report + recommendation from the last sweep.")
@click.option("--root", default=".", help="Project directory")
@click.option("--live", is_flag=True, help="Score gold pairs with a real judge")
def report(root: str, live: bool) -> None:
    r = Path(root)
    mock = _set_mock(live)
    rubric, gold = load_rubric(r), load_gold(r)
    _, results = load_trace(r)
    inputs = load_synth_inputs(r)
    stats = model_stats(results)
    trust = judge_trust(r, rubric, gold, results, mock=mock)
    path = write_report(r, r.resolve().name, len(inputs.inputs), stats, trust)
    console.print(f"[green]✓[/green] wrote {path} and report.json")


@cli.command(help="Run the whole pipeline: synth → sweep → report.")
@click.option("--root", default=".", help="Project directory")
@click.option("--repeats", default=3)
@click.option("--live", is_flag=True)
@click.pass_context
def run(ctx: click.Context, root: str, repeats: int, live: bool) -> None:
    r = Path(root)
    mock = _set_mock(live)
    uc, cands, rubric, gold = (
        load_usecase(r), load_candidates(r), load_rubric(r), load_gold(r),
    )
    inputs = synthesize(uc, mock=mock)
    write_yaml(r / "inputs.yaml", inputs)
    console.print(f"[green]✓[/green] {len(inputs.inputs)} inputs")
    results = run_sweep(r, uc, cands, rubric, inputs, repeats=repeats, mock=mock)
    console.print(f"[green]✓[/green] {len(results)} outputs judged")
    stats = model_stats(results)
    trust = judge_trust(r, rubric, gold, results, mock=mock)
    write_report(r, r.resolve().name, len(inputs.inputs), stats, trust)
    console.print(f"[dim]report.md + report.json written to {r.resolve()}[/dim]")


if __name__ == "__main__":
    cli()
