# Design notes

The whole idea in one line: **evaluate the evaluator.** JudgeHarness is a meta-eval —
it doesn't judge outputs, it measures whether *your judge* can be trusted to.

## Core objects (keep it to ~4)

```yaml
# 1. Dataset — your calibration / gold set (the answer key)
dataset:
  - id: ex1
    input: "..."          # the thing being judged (or an A/B pair)
    gold: "A"             # human verdict — the ground truth
    meta: { domain: code }

# 2. Judge — a frozen, versioned config
judge:
  id: code-review-v3
  model: gpt-5-mini
  mode: pairwise          # or "score"
  temperature: 0
  rubric: ./rubrics/code_review.yaml
  output_schema: per_criterion   # forces structured verdict

# 3. Rubric — domain-specific criteria (the contributable pack)
rubric:
  criteria:
    - name: correctness
      weight: 0.5
      guide: "Does it compile & handle edge cases?"
    - name: clarity
      weight: 0.3
    - name: security
      weight: 0.2

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
2. **Expand** into runs: N repeats × A/B-swapped × candidate models.
3. **Execute** (async, cached by hash — never re-pay for a run you've done).
4. **Score** against gold + compute meta-metrics.
5. **Report** — markdown + JSON leaderboard.

## Meta-metrics (the "trust score")

- **Agreement** — does judge match human labels? (accuracy / Cohen's κ)
- **Consistency** — same input, N runs → same verdict?
- **Position bias** — swap A/B → does verdict flip? (should be ~0)
- **Self-preference** — does a GPT-judge favor GPT-outputs?
- **Calibration** — when judge says "9/10 confident," is it right 90% of the time?

## Commands

- `init` — scaffold a project + starter gold sets per domain.
- `label` — bootstrap-assisted answer key (a *stronger* model drafts, you confirm).
- `sweep` — the money command: {models} × {prompts} × {temp}, order-swapped, N repeats.
- `report` — committable markdown + JSON.

## Opinionated defaults (baked-in trust)

- `temperature=0` + forced JSON schema (kills most flakiness).
- Auto A/B order swap + report `flip_rate` (kills position bias).
- Require per-criterion justification (kills opacity).
- Refuse to emit a verdict if schema validation fails (no silent garbage).
- `label` must use a different/stronger model than the judge under test.

## Stack

Python · `pydantic` (schemas) · `litellm` (multi-provider adapter) · local SQLite/JSON cache.
No server, no DB. Runs in CI.

## Non-goals

- Not a public benchmark (SimpleQA etc. test *models*, not *your judge*).
- No mid-verdict "nudging" — iteration happens at rubric-design time, then you freeze.
