# 06 — Architecture

See also the top-level [`DESIGN.md`](../DESIGN.md). This file is the fuller version.

## Mental model

JudgeHarness is a **meta-eval**: config in → report out, fully reproducible.
It doesn't judge outputs; it measures whether *your judge* can be trusted to.

## Core objects (~4)

```yaml
# 1. Dataset — your calibration / gold set (the answer key)
dataset:
  - id: ex1
    input: "..."          # thing being judged (or an A/B pair)
    gold: "A"             # human verdict — the ground truth
    meta: { domain: code }

# 2. Judge — a frozen, versioned config
judge:
  id: code-review-v3
  model: gpt-5-mini
  mode: pairwise          # or "score"
  temperature: 0
  rubric: ./rubrics/code_review.yaml
  output_schema: per_criterion

# 3. Rubric — domain-specific criteria (contributable pack)
rubric:
  criteria:
    - { name: correctness, weight: 0.5, guide: "compiles & handles edge cases?" }
    - { name: clarity,     weight: 0.3 }
    - { name: security,    weight: 0.2 }

# 4. Report — auto-generated, committable
report:
  judge: code-review-v3
  agreement: 0.94
  flip_rate: 0.02
  self_consistency: 0.97
  cost_per_judge: 0.0011
```

## Pipeline (5 stages)

1. **Load** dataset + judge config.
2. **Expand** into runs: N repeats × A/B-swapped × candidate models × prompt variants.
3. **Execute** (async; **cache by hash** — never re-pay for a run you've done).
4. **Score** vs. gold + compute meta-metrics (see `02-trust-metrics.md`).
5. **Report** — markdown + JSON leaderboard.

## CLI commands

| Command | Purpose |
|---|---|
| `init` | Scaffold a project + starter gold sets per domain |
| `label` | Bootstrap-assisted answer key (stronger model drafts, human confirms) |
| `sweep` | The money command: {models}×{prompts}×{temp}, order-swapped, N repeats |
| `report` | Committable markdown + JSON |
| `check` (v2) | Run mechanistic checks (logit/J-lens) on an open-weight judge |

### The money command

```bash
judgeharness sweep \
  --dataset gold.yaml \
  --models gpt-5-mini,claude-sonnet,gemini-flash \
  --rubric code_review.yaml \
  --repeats 5 --swap-order
```

## Stack

- Python · `pydantic` (schemas) · `litellm` (multi-provider adapter) ·
  local SQLite/JSON cache. No server, no DB. Runs in CI.
- **v2 mechanistic**: `transformer-lens` / `nnsight` for activation access;
  Neuronpedia for J-lens vectors on open-weight models. Start with a
  dependency-light **logit lens** before full J-lens/SAE tooling.

## Trust-by-default (baked in)

- `temperature=0` + forced JSON schema.
- Auto A/B order swap + report `flip_rate`.
- Require per-criterion justification; refuse verdict on schema-validation failure.
- `label` enforces/warns: drafting model must differ from judge under test.

## Non-goals

- Not a public benchmark (those test *models*, not *your judge*).
- No mid-verdict nudging — iterate the rubric, then **freeze** the judge.
- Speed is a later concern; correctness of the rubric/gold loop comes first.
