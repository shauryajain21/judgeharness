# Metanoia V0 — AI Model Bake-off (runnable MVP)

Describe a use case → fan it across candidate models → judge every output with a
blinded, evidence-grounded rubric → get a validated, inspectable recommendation
across **quality / latency / cost**. Runs fully in **mock mode** (no API keys) so
you can test the whole pipeline offline, then drop in real models via `litellm`.

See [`MVP.md`](./MVP.md) for the full spec and design rationale.

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install -e .          # mock mode only
.venv/bin/pip install -e '.[live]'  # + litellm for real model calls
```

## Quickstart (mock — no keys needed)

```bash
metanoia init my-eval
cd my-eval && metanoia run
```

Produces a ranked `report.md` + `report.json` with a recommendation and the
judge's own trust metrics (agreement / consistency / self-preference).

## Go live (real models)

Bring an OpenRouter key (one key → every provider) or per-provider keys:

```bash
echo 'OPENROUTER_API_KEY=sk-or-...' > .env
set -a && . ./.env && set +a
export METANOIA_JUDGE_MODEL=openrouter/openai/gpt-4o-mini
metanoia run --live
```

Edit `candidates.yaml` with real model IDs (e.g. `openrouter/deepseek/deepseek-chat`,
`openrouter/anthropic/claude-haiku-4.5`, `openrouter/google/gemini-2.5-flash`).

## Commands

| Command | Purpose |
|---|---|
| `metanoia init <name>` | Scaffold a project (usecase / candidates / rubric / gold) |
| `metanoia synth`       | Generate synthetic inputs → `inputs.yaml` (editable artifact) |
| `metanoia sweep`       | Fan inputs across models, judge each (blinded) |
| `metanoia report`      | Ranked recommendation + judge-trust metrics |
| `metanoia run`         | synth → sweep → report in one shot |

Add `--live` to any command to use real models (needs `metanoia[live]` + keys).

## Layout

```
src/metanoia/
  config.py     typed schemas (fail loudly on bad config)
  providers.py  model adapter (mock + litellm), latency/token/cost capture
  synth.py      synthetic input generation
  judge.py      blinded, structured, code-side weighted aggregation
  metrics.py    meta-eval: agreement / consistency / self-pref
  report.py     Rich table + committable markdown + JSON
  sweep.py      orchestration + content-addressed cache
  cli.py        init / synth / sweep / report / run
```
