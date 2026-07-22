# Design notes

JudgeHarness is a Git-native control plane for LLM migrations. Its core invariant
is simple: **a migration may pass only when a reproducible, human-calibrated
decision supports the repository's committed policy.**

## Product boundary

Existing tools execute evals. JudgeHarness consumes their evidence and owns:

1. normalization into a stable paired-result contract;
2. blind, stratified human-audit selection;
3. automated-evaluator calibration;
4. uncertainty-aware migration policy;
5. a content-addressed decision lockfile;
6. local and CI verification of that lockfile.

Promptfoo is the first adapter, not the runtime foundation. Generic paired JSONL
is supported from the start. A thin LiteLLM runner is optional and uses the same
canonical contract as imported results.

## Core objects

### Pair

One representative input with incumbent and challenger evidence:

```json
{
  "schema_version": 1,
  "id": "support-001",
  "input": {"question": "..."},
  "incumbent": {"output": "...", "latency_ms": 820, "cost_usd": 0.003},
  "challenger": {"output": "...", "latency_ms": 510, "cost_usd": 0.001},
  "scores": {},
  "tags": {"intent": "refund", "criticality": "high"},
  "provenance": {"adapter": "promptfoo", "source_id": "..."}
}
```

### Judgment

An automated material-regression verdict with rubric criteria, quoted evidence,
judge identity/configuration, response order, schema status, and source score.
Both A/B orders are required when JudgeHarness supplies the judgment.

### Audit label

An append-only blind human decision: material regression `yes`, `no`, or
`unsure`, plus failed criterion and optional note. The record includes reviewer
identity only when explicitly configured; local OSS defaults to an opaque ID.

### Decision lockfile

`decision.lock.json` commits:

- hashes of normalized pairs, policy, rubric, judgments, and audit labels;
- source adapter/version and upstream artifact hashes;
- sampling seed, strata, inclusion probabilities, priors, and software version;
- raw and calibrated regression estimates with intervals;
- adequacy diagnostics, threshold values, and final outcome;
- no raw prompts, responses, secrets, or provider payloads.

## Decision pipeline

```text
external results
      │
      ▼
validate + normalize ──────── preserve source + hashes
      │
      ▼
fill missing judgments ───── pairwise, both orders, forced schema
      │
      ▼
stratified audit sample ───── verdict × flip × criticality × tags
      │
      ▼
blind local labels ────────── yes / no / unsure
      │
      ▼
calibrate by stratum ──────── posterior true-regression prevalence
      │
      ▼
apply committed policy ───── safe / unsafe / insufficient
      │
      ▼
lockfile + report + CI status
```

The first calibrated endpoint is binary: whether the challenger introduces a
material quality regression on a case. Cost, latency, deterministic errors,
improvements, and tags are reported and may be hard policy gates, but they do not
get mixed into an unexplained composite trust score.

## Git workflow

Repository-owned files:

```text
evals/model-migration/
├── judgeharness.yaml
├── rubric.yaml
├── audit-labels.jsonl     # only when safe to commit
├── decision.lock.json
└── report.md              # optional
```

Local-only files:

```text
.judgeharness/
├── imports/
├── pairs.jsonl
├── judgments.jsonl
├── cache.sqlite
└── reports/
```

`judgeharness check` is non-interactive. It verifies hashes, recomputes the
decision, writes a GitHub Step Summary when available, and exits with a stable
status:

| Outcome | Meaning |
|---|---|
| `0 SAFE` | Evidence is current and policy permits migration |
| `10 UNSAFE` | Corrected risk or a hard gate blocks migration |
| `11 INSUFFICIENT` | More human evidence is required |
| `12 STALE` | Lockfile does not match current inputs/configuration |
| `13 INVALID` | Artifact, schema, or calibration validation failed |

The generated GitHub Action runs with least privilege. It never receives
provider secrets on untrusted fork PRs and does not upload raw reports unless the
repository policy explicitly permits it.

## OSS architecture

```text
src/judgeharness/
├── adapters/       # promptfoo + generic paired JSONL
├── models.py      # versioned canonical schemas
├── judging.py    # optional missing-verdict judge
├── sampling.py   # seeded audit strata and selection
├── audit.py      # blind, resumable terminal labeling
├── calibration.py
├── decision.py   # policy and adequacy rules
├── lockfile.py
├── reports.py
├── storage.py    # local artifact protocol
└── cli.py
```

Python 3.11+, Typer, Pydantic, NumPy, Jinja, JSONL/JSON artifacts, and optional
LiteLLM/SQLite for missing judgments or the convenience runner. Statistical
coverage and false-safe behavior are tested with offline simulations; paid API
calls are never required by the default test suite.

## Enterprise architecture

The enterprise product replaces local backends without changing decision
semantics:

```text
GitHub/GitLab             enterprise control plane
     │                    projects · policy · identity
     ▼                              │
required check ◄──── signed decision/artifact metadata
                                    │
                         customer VPC worker plane
                         replay · judge · audit queue
                                    │
                         object store + metadata DB
```

Paid capabilities are organizational: SSO/SCIM/RBAC, approvals, shared evidence,
model inventory and deprecation tracking, scheduled revalidation, immutable
audit logs, private workers, retention controls, and support. The evaluation
logic, artifact schema, calibration, and individual Git workflow remain OSS.

## Non-goals for the MVP

- a provider catalog, generic assertion library, experiment tracker, or dashboard;
- a proprietary tracing SDK—future production imports use OpenTelemetry;
- runtime routing, an always-on proxy, or automatic model selection;
- more than one incumbent/challenger pair per decision;
- a GitHub App or hosted human-review UI;
- mechanistic interpretability or a public benchmark.
