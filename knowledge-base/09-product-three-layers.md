# 09 — Product layers: one decision contract

The product expands by coordination scope, not by withholding evaluation logic.

```text
              DECISION CONTRACT
   evidence → audit → calibration → policy → lockfile
          ▲                 ▲                 ▲
          │                 │                 │
   1. OSS LOCAL       2. GIT WORKFLOW    3. ENTERPRISE
   individual use     team adoption      organization control
```

## Layer 1 — OSS local workflow

For indie developers and small teams:

- import Promptfoo or generic paired results;
- audit a blind, stratified sample in the terminal;
- produce raw and corrected regression estimates;
- emit safe, unsafe, or insufficient evidence;
- write portable reports and a content-addressed lockfile.

No account, telemetry, hosted storage, or proprietary SDK. This entire layer is
MIT licensed and useful on its own.

## Layer 2 — Git workflow

The developer wedge becomes team infrastructure when the migration lockfile is
reviewed with the model change:

- repository-owned `judgeharness.yaml`, rubric, and decision lockfile;
- generated GitHub Action and stable CI exit codes;
- required check for model, prompt, tool-schema, or policy changes;
- stale-evidence detection and explicit insufficient-evidence remediation;
- Step Summary and policy-controlled build artifacts.

This is the adoption loop: one developer creates a migration decision; the team
makes the check required; every future model change inherits the evidence
discipline.

## Layer 3 — Enterprise control plane

Enterprises pay when local artifacts need organization-wide coordination:

- inventory of production systems, providers, models, owners, and deprecations;
- shared datasets, rubrics, label queues, and approval policies;
- VPC/on-prem workers, managed queues, caching, budgets, and secret integration;
- SSO, SCIM, RBAC, separation of duties, and immutable audit logs;
- scheduled revalidation and deployment gates across repositories;
- retention/residency controls, SLAs, procurement, and support.

The control plane stores signed artifact metadata and policy state. Sensitive
execution can remain in customer infrastructure. Enterprise features never
change the meaning of an OSS decision lockfile.

## Why this can compound

Each completed migration creates reusable, customer-owned assets:

- representative paired cases;
- human labels and known evaluator failure modes;
- a calibrated rubric and decision policy;
- provenance linking a model change to its approval evidence.

The next migration needs fewer setup decisions and exposes organization-wide
needs naturally. The expansion path is therefore:

> local audited migration → required repository check → shared organizational
> policy and evidence infrastructure

## Explicitly abandoned layers

The earlier free web grader, verifier certification, reward-hack scanner, and
mechanistic-interpretability tier are not the current roadmap. Their research
remains in this knowledge base, but none should block or dilute the model-
migration workflow.
