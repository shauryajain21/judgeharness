# JudgeHarness

> "AI might be smart enough for this: it is the first technology capable of
> making broad, fuzzy judgements in a repeatable and mechanical way."
> — Dario Amodei, *Machines of Loving Grace*

There's just one problem: today it doesn't.

Ask an LLM "which output is better?" twice and you'll often get two answers.
Swap the order of the options and the verdict flips. Ask *why* and you get a
number with no reasoning. **Fuzzy judgment, delivered in a fuzzy, irreproducible
way** — the opposite of what makes a judge trustworthy.

JudgeHarness is the missing repeatability layer for LLM-as-judge. It measures how
much your judge actually agrees with you, how stable it is, and how biased it is —
then hands you a **frozen, reproducible judge config** you can commit, cite, and ship.

## The three properties of a trustworthy judge

| Property (from the essay) | What it means | How we measure it |
|---|---|---|
| **Repeatable** | Same input → same verdict | Self-consistency across N runs |
| **Mechanical / impartial** | No hidden thumb on the scale | Position-bias & self-preference scores |
| **Transparent** | You can see *why* | Per-criterion scores + required justification |

If a judge can't clear all three, you shouldn't trust its verdicts. Most can't —
until you tune them against real examples.

## How it works

1. **Give it an answer key.** 20–30 examples where *you* know the right verdict.
2. **Sweep.** JudgeHarness tries your candidate models, prompts, and settings —
   running each multiple times with the options order-swapped.
3. **Get a leaderboard.** Ranked by agreement × consistency × cost.
4. **Freeze the winner.** Ship a judge config that's reproducible by design.

## The one command that matters

```bash
judgeharness sweep \
  --dataset gold.yaml \
  --models gpt-5-mini,claude-sonnet,gemini-flash \
  --rubric code_review.yaml \
  --repeats 5 --swap-order
```

```
Config                        Agreement  Consistency  FlipRate  $/judge
gpt-5-mini + rubric-v3          0.94        0.97        0.02     $0.0011  ★
claude-sonnet + rubric-v3       0.96        0.91        0.05     $0.0090
gemini-flash + rubric-v3        0.88        0.95        0.03     $0.0004
```

Stop trusting your judge on vibes. Measure it.

## Status

Early / brainstorm stage. Design notes live in [`DESIGN.md`](./DESIGN.md).

## License

MIT
