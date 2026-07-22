# JudgeHarness

> Infrastructure for approving LLM model migrations with evidence you can trust.

Model providers retire and replace models continuously. The hard part is not
calling the old and new APIs; Promptfoo, DeepEval, and internal eval systems
already do that. The hard part is deciding whether the automated evaluator is
reliable enough to authorize the production change.

JudgeHarness is an MIT-licensed, local-first **migration audit and decision
layer**. It imports paired incumbent/challenger results, selects a small blind
human-audit sample, measures evaluator error, propagates that error into the
estimated regression rate, and produces one of three outcomes:

- **safe to migrate**;
- **do not migrate**;
- **insufficient evidence**, with the next cases to label.

## Planned developer workflow

JudgeHarness integrates with Git rather than asking developers to adopt another
hosted eval dashboard.

```bash
# Run the eval tool you already use
promptfoo eval --output results.json

# Import, audit, and lock the migration decision
judgeharness import promptfoo results.json --run ./migration-audit
judgeharness audit ./migration-audit
judgeharness decide ./migration-audit \
  --lock evals/model-migration/decision.lock.json

# Verify the committed evidence in CI
judgeharness check
```

The migration PR contains the model/config change plus a reviewable lockfile.
The GitHub Action verifies hashes, recalculates the decision, rejects stale or
insufficient evidence, and posts a compact Step Summary. Raw prompts, responses,
provider payloads, and caches remain local and gitignored by default.

## What JudgeHarness owns

```text
Promptfoo / DeepEval / internal eval / paired JSONL
                         │
                         ▼
              canonical evidence ledger
                         │
             blind stratified human audit
                         │
                         ▼
             evaluator-error calibration
                         │
                         ▼
             migration policy + lockfile
                         │
                         ▼
                 required PR check
```

The first adapter is Promptfoo. A stable paired JSONL contract prevents it from
becoming a Promptfoo wrapper, and later adapters can consume DeepEval, Driftcut,
OpenTelemetry exports, or internal evaluation results.

## Why calibration matters

A conventional eval report treats automated scores as observations. But the
judge can be biased, order-sensitive, or confidently wrong. JudgeHarness audits
a seeded sample blindly, estimates the true material-regression prevalence
within relevant strata, and carries human-label uncertainty into the final
decision.

The report always shows the raw automated result beside the human-corrected
estimate. If the evidence cannot support the configured migration threshold,
JudgeHarness refuses to manufacture a pass.

## OSS and enterprise boundary

The complete individual workflow stays open source: importers, canonical
artifacts, audit sampling and labeling, calibration, policy gates, reports,
lockfiles, and CI verification.

An enterprise control plane can later add shared datasets and rubrics, managed or
VPC workers, SSO/RBAC, approval chains, immutable audit logs, fleet-wide model
inventory, scheduled revalidation, private deployment, and support. The OSS
lockfile and decision semantics remain the source of truth.

## Scope

JudgeHarness is not another general-purpose eval framework, provider catalog,
observability platform, model router, or metric library. It integrates with
those systems and owns the path from evaluation evidence to an approved or
blocked migration.

## Status

Planning and implementation design. The current canonical build plan is
[`plan.md`](./plan.md#part-iii--mvp-implementation-plan).

- Product and artifact design: [`DESIGN.md`](./DESIGN.md)
- Research and prior decisions: [`knowledge-base/`](./knowledge-base/)
- Positioning: [`positioning.md`](./positioning.md)

## License

MIT
