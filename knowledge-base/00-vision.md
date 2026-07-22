# 00 — Vision

## The original problem

LLM judges are flaky, confidently wrong, opaque, and sensitive to model/prompt
choice. That remains the technical foundation of JudgeHarness: automated
evaluation cannot be treated as ground truth merely because it returns a score.

## The product problem

The sharp commercial instance is a forced model migration. A production model is
retired; a developer must replace it by a deadline; an existing eval framework
compares the outputs; someone still has to decide whether the evidence is
trustworthy enough to ship.

Today that final step is usually a dashboard glance, an average score, or a few
manually inspected examples. None produces a reproducible approval trail or
propagates evaluator mistakes into the migration decision.

## The thesis

> **An LLM migration should pass only when human-calibrated evidence satisfies a
> policy that can be reproduced from the repository.**

JudgeHarness is the migration audit and decision layer:

1. import paired incumbent/challenger evidence from Promptfoo, another eval tool,
   or generic JSONL;
2. select a blind, statistically useful human-audit sample;
3. estimate how automated judgments differ from the user's labels;
4. propagate that uncertainty to the material-regression rate;
5. emit safe, unsafe, or insufficient evidence;
6. bind the decision to a content-addressed lockfile and required PR check.

## The infrastructure vision

The OSS CLI is the edge of a model-migration control plane:

```text
production evidence → evaluation → human audit → calibrated decision → PR gate
```

For an individual, every step runs locally and the repository owns the policy
and lockfile. For an enterprise, the same artifacts feed shared model inventory,
deprecation tracking, datasets, VPC workers, approvals, identity, and immutable
audit logs.

## What survives from the original judge thesis

- Order swaps remain mandatory when JudgeHarness creates pairwise judgments.
- Invalid or inconsistent judgments never become silent ties.
- Human labels calibrate the evaluator instead of decorating the report.
- Every automated conclusion must be traceable to its rubric and evidence.
- A judge's confidence is never confused with confidence in the migration.

Mechanistic interpretability and general judge certification remain useful
research directions, documented in files 03–05, but they are not MVP scope or
the current product wedge.
