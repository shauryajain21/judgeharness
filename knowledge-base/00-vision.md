# 00 — Vision

## The problem (from the user's own words)

> "I use a bunch of AI judges... I use an LLM as a judge to run an eval or figure
> out, between two outcomes, what's the better one. It always doesn't work out the
> way I want it to be, and it's a low trust score."

Original framing of the pain:
1. AI judges are a black box — ~80% trust in the prompt, ~20% trust in the response.
2. Don't know which model is ideal to solve for a given judging task.

Four concrete failure modes (all selected as real pains):
- **Flaky** — same input, different verdict.
- **Confidently wrong** — disagrees with the user's own judgment.
- **Opaque** — can't tell *why* it decided.
- **Model choice** — don't know which model to even use.

## The inspiration

From Dario Amodei's *Machines of Loving Grace* (highlighted on the user's Kindle):

> "AI might be smart enough for this: it is the first technology capable of making
> broad, fuzzy judgements in a **repeatable and mechanical way**."

And, on the next page:

> "Transparency would be important in any such system... advanced interpretability
> techniques could be used to see inside the final model and assess it for hidden
> biases, in a way that is simply not possible with humans."

**The gap:** Dario says AI *can* judge repeatably, mechanically, transparently.
Today it does none of those — same input → different verdict, hidden thumb on the
scale, opaque rationale. JudgeHarness is the infrastructure that makes that
sentence *true instead of aspirational.*

## The thesis

JudgeHarness is a **meta-eval**: it doesn't judge outputs, it evaluates the
evaluator. It turns "trust" from a feeling into a set of numbers, and hands the
user a **frozen, reproducible judge config** they can commit, cite, and ship.

## The reframed insight (important)

- "Which model?" is the **last** problem, not the first. A great rubric on a cheap
  model beats a vague rubric on the best model. Order of leverage:
  **rubric + gold set > schema/consistency > model choice.**
- Public benchmarks (SimpleQA, TruthfulQA, MMLU) test whether *a model* is good.
  They do **not** test whether *your judge* is good on *your* task. You borrow the
  *methodology* (fixed labeled reference + scoring protocol), not the data.

## The sharpest framing (post-interpretability research)

> A trustworthy judge isn't one with a nice-sounding rationale — it's one whose
> *unspoken* workspace agrees with its verdict.
> **Behavioral** checks (v1) test the output; **mechanistic** checks (v2, J-lens)
> test the thought.

This "output vs. thought" gap is the project's point of view, and it's grounded
in real 2024–2026 interpretability research (see files 03–05).
