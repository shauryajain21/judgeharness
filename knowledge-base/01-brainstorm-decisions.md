# 01 — Locked product decisions

The canonical implementation plan is Part III of [`../plan.md`](../plan.md).
This file is the compact decision register.

## Product

| Decision | Choice | Reason |
|---|---|---|
| Initial job | Validate one forced LLM migration | Deadline, incumbent, and challenger are explicit |
| Initial user | Indie developer or small product team | Self-serve OSS can reach them without enterprise sales |
| Category | Git-native model-migration control plane | Broader and more durable than a Promptfoo wrapper |
| Decision endpoint | Material regression: yes/no with uncertainty | Human-labelable and directly tied to shipping risk |
| Outcomes | Safe, unsafe, insufficient evidence | Never force ambiguity into pass/fail |

## Workflow

| Decision | Choice | Reason |
|---|---|---|
| Primary surface | Local CLI + committed lockfile + required PR check | Fits existing developer release workflow |
| First integration | Promptfoo result import | Mature OSS runner; do not rebuild it |
| Neutral contract | Versioned paired JSONL | Prevents dependency on any one eval tool |
| Human review | Blind, seeded, stratified, resumable | Reduces bias and makes selection reproducible |
| CI behavior | Non-interactive lockfile verification | CI must not invent human labels |
| Production ingest | OpenTelemetry export after MVP | Standard over proprietary instrumentation |

## Technical

| Decision | Choice | Reason |
|---|---|---|
| Calibration | Stratum-weighted beta-binomial baseline | Transparent, simulatable, and easy to audit |
| Pairwise judge | Both response orders, forced schema, quoted evidence | Makes position bias and invalid output visible |
| Artifact store | Local JSONL/JSON; raw evidence gitignored | Portable and privacy-preserving |
| Lockfile | Hash all evidence, labels, policy, rubric, seed, and method | Reproducible approval without committing raw content |
| Optional runner | Thin LiteLLM path, cut first | Convenience only; not differentiation |
| Test bar | Offline adapter/golden/simulation tests | No paid API calls required for correctness |

## OSS and revenue

| Decision | Choice |
|---|---|
| License | MIT |
| OSS boundary | Import, audit, calibration, policy, lockfile, report, CI check |
| Enterprise value | Shared evidence, model inventory, VPC workers, governance, approvals, SSO/RBAC, audit logs, support |
| Hosted trigger | Multiple developers at one company demand coordination or controls |

## Anti-patterns

- Do not build a general-purpose eval framework, provider catalog, metric zoo,
  experiment tracker, observability dashboard, or model router.
- Do not expose provider secrets to untrusted fork pull requests.
- Do not upload prompts, responses, labels, or reports without explicit policy.
- Do not call a raw automated score a migration confidence value.
- Do not build the enterprise control plane before OSS usage pulls the product
  into teams.
- Do not ship if calibration merely reformats the same conclusion produced by
  existing tools.

## Validation required before expansion

Run three real migrations through existing tooling and JudgeHarness. At least
one must show a material raw-vs-calibrated conclusion change, and two of three
must demonstrate a clearer audit trail, fewer labels, or a caught evaluator
mistake. Otherwise contribute the calibration feature upstream rather than
creating a separate product.
