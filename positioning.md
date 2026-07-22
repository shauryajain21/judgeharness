# Positioning

## Category

**Model-migration control plane** or **Git-native infrastructure for LLM
migrations**.

JudgeHarness is not positioned as an eval framework. It is the evidence,
approval, and policy layer between an evaluation run and a production model
change.

## Primary message

> **Prove your replacement model is safe before the old one disappears.**

Supporting explanation:

> Import the evals you already run. JudgeHarness audits the evaluator against a
> small blind human sample, corrects the estimated regression rate, and attaches
> a reproducible migration decision to your pull request.

## One sentence

**JudgeHarness checks whether you can trust your eval enough to approve an LLM
migration.**

## Developer pitch

> Change the model in a PR, attach an audited migration lockfile, and let CI
> verify that the evidence still supports shipping.

## Enterprise pitch

> Know which production systems depend on retiring models, require calibrated
> evidence before replacements ship, and preserve an immutable approval trail
> across every team and provider.

## What makes it different

- Promptfoo and DeepEval execute and score evals; JudgeHarness audits whether
  those scores are trustworthy enough for the migration threshold.
- The automated result and human-corrected result are always shown together.
- “Insufficient evidence” is a product outcome, not an error to average away.
- The decision is a content-addressed lockfile verified in CI, not a dashboard
  screenshot or mutable hosted result.
- OSS users keep raw prompts, responses, labels, and provider keys local.

## Messaging hierarchy

1. **Deadline:** the incumbent model is being retired.
2. **Risk:** automated evals can be confidently wrong.
3. **Action:** audit a small targeted sample.
4. **Decision:** safe, unsafe, or insufficient evidence.
5. **Workflow:** commit the migration lockfile and verify it in the PR.

## Taglines

- **The required check for model migrations.**
- **Trust your eval before you trust the replacement.**
- **A lockfile for model-migration evidence.**
- **Ship the new model with proof.**
- **Model changes deserve release gates.**

## Avoid

- “Another LLM eval platform.”
- Generic “faster, better, cheaper” vendor-selection language.
- Claiming the LLM judge itself is the moat.
- Leading with statistical terminology rather than the migration decision.
- “AI safety certification” or compliance claims before external validation.
- Implying Promptfoo is required; it is the first adapter.

## OSS-to-enterprise motion

```text
local CLI + lockfile
        ↓
required PR check
        ↓
multiple migrations across a team
        ↓
shared policy, approvals, VPC workers, audit logs
```

The OSS call to action is `pipx install judgeharness`, never “book a demo.” The
enterprise conversation begins only after teams need shared evidence,
governance, identity, deployment controls, or support.
