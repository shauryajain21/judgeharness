# JudgeHarness knowledge base

Research and decision history for JudgeHarness. The current product is a
Git-native model-migration control plane; Part III of [`../plan.md`](../plan.md)
and [`../DESIGN.md`](../DESIGN.md) are authoritative where older research
conflicts.

## Current product spine

| File | Purpose |
|---|---|
| [`00-vision.md`](./00-vision.md) | Current migration problem, thesis, and infrastructure vision |
| [`01-brainstorm-decisions.md`](./01-brainstorm-decisions.md) | Locked product, workflow, technical, and OSS decisions |
| [`06-architecture.md`](./06-architecture.md) | Canonical artifacts and OSS/enterprise system boundaries |
| [`09-product-three-layers.md`](./09-product-three-layers.md) | OSS local → Git workflow → enterprise control plane |

## Technical research retained

| File | Purpose |
|---|---|
| [`02-trust-metrics.md`](./02-trust-metrics.md) | Agreement, consistency, position bias, self-preference, calibration |
| [`03-interpretability-techniques.md`](./03-interpretability-techniques.md) | Black-box and mechanistic evaluator research; post-MVP |
| [`04-global-workspace-jlens.md`](./04-global-workspace-jlens.md) | 2026 Global Workspace / Jacobian-lens notes; post-MVP |
| [`05-technique-to-judge-check.md`](./05-technique-to-judge-check.md) | Technique-to-check mapping; historical/future research |
| [`07-references.md`](./07-references.md) | Papers, links, and reading order |

## Historical market explorations

| File | Status |
|---|---|
| [`08-market-and-pivot.md`](./08-market-and-pivot.md) | Superseded verifier/reward-model positioning research |
| [`10-gtm-yc-and-product-hunt.md`](./10-gtm-yc-and-product-hunt.md) | Superseded certification/launch plan |

These files are kept to preserve the reasoning trail, not as current
implementation instructions.

## Current pitch

JudgeHarness imports the evals developers already run, audits the automated
evaluator against a small blind human sample, corrects the estimated regression
rate, and binds the resulting migration decision to a reproducible lockfile and
required pull-request check.

> **Change the model in a PR, attach audited evidence, and let CI verify that it
> is still safe to ship.**
