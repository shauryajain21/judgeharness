# 06 — Architecture

The maintained architecture specification is [`../DESIGN.md`](../DESIGN.md).
This page records the conceptual boundaries used by the rest of the knowledge
base.

## System boundary

JudgeHarness sits after an eval runner and before a production release:

```text
Promptfoo / DeepEval / internal system / paired JSONL
                         ↓
              canonical paired evidence
                         ↓
          blind audit + judge calibration
                         ↓
               migration policy gate
                         ↓
            decision lockfile + PR check
```

It may fill missing judgments through LiteLLM, but execution is not the core.
The stable interfaces are:

- `ResultAdapter` — converts external results while preserving provenance;
- `ArtifactStore` — stores canonical pairs, judgments, labels, and decisions;
- `JudgeProvider` — optionally creates missing structured judgments.

## Canonical artifacts

| Artifact | Purpose | Committed by default? |
|---|---|---|
| `pairs.jsonl` | Normalized incumbent/challenger evidence | No |
| `judgments.jsonl` | Automated verdicts, criteria, swaps, evidence | No |
| `audit-labels.jsonl` | Append-only blind human labels | Only when safe |
| `judgeharness.yaml` | Migration policy and adapter mapping | Yes |
| `rubric.yaml` | Definition of material regression | Yes |
| `decision.lock.json` | Hashes, method, calibrated result, outcome | Yes |
| `report.md` / `report.html` | Reviewable explanation | Policy-controlled |

## OSS execution model

- Local-first Python CLI and callable library.
- JSONL/JSON source of truth; optional SQLite cache only for model calls.
- Seeded audit sampling and posterior simulation.
- No telemetry or hosted account.
- GitHub Action uses `judgeharness check` and stable exit codes.
- Untrusted fork PRs receive no provider keys and make no paid calls.

## Enterprise substitution points

The enterprise control plane replaces local storage and coordination, not the
decision method:

- filesystem → object storage and metadata database;
- local process → customer-VPC workers and queue;
- opaque local reviewer → SSO identity and approval chain;
- one repository → organization model inventory and deprecation calendar;
- local history → immutable audit log and scheduled revalidation.

The decision lockfile remains portable across OSS, cloud, and private
deployments.
