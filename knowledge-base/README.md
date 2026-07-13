# JudgeHarness Knowledge Base

Everything needed to build JudgeHarness: the vision, the decisions we've locked,
the trust metrics, and the interpretability research that underpins the "look
inside the judge" ambition.

## Index

| File | What's in it |
|---|---|
| [`00-vision.md`](./00-vision.md) | The thesis, the Dario quote, the problem, the "output vs. thought" framing |
| [`01-brainstorm-decisions.md`](./01-brainstorm-decisions.md) | Every decision locked so far + open questions |
| [`02-trust-metrics.md`](./02-trust-metrics.md) | The meta-metrics that make up a judge's "trust score" |
| [`03-interpretability-techniques.md`](./03-interpretability-techniques.md) | Transformer Circuits techniques (SAEs, attribution graphs, etc.), black-box vs white-box |
| [`04-global-workspace-jlens.md`](./04-global-workspace-jlens.md) | Deep notes on the 2026 Global Workspace / Jacobian lens paper |
| [`05-technique-to-judge-check.md`](./05-technique-to-judge-check.md) | The core mapping: each technique → a concrete judge-trust check |
| [`06-architecture.md`](./06-architecture.md) | Harness architecture, core objects, pipeline, CLI |
| [`07-references.md`](./07-references.md) | Papers, links, reading order |

## The one-paragraph pitch

LLM-as-judge is a black box you're forced to trust on vibes. JudgeHarness makes
it measurable: it scores how much a judge agrees with you (agreement), how stable
it is (consistency), and how biased it is (position bias, self-preference) — then
hands you a frozen, reproducible judge config. Two tiers: **behavioral** checks
that work on any API model (ships first), and **mechanistic** checks (J-lens,
attribution graphs) that read the judge's *unspoken* reasoning on open-weight
models (the moat).

## The spine (memorize this)

- **Repeatable** → self-consistency
- **Mechanical / impartial** → bias scores (position, self-preference)
- **Transparent** → per-criterion breakdown (v1) + workspace readout (v2)

> A trustworthy judge isn't one with a nice-sounding rationale — it's one whose
> *unspoken* workspace agrees with its verdict.
