# 02 — Trust metrics (the "trust score")

These five meta-metrics turn a black-box judge into a glass box. All are
**black-box / behavioral** — they work on any API model.

## The five

| Metric | Question it answers | How to compute | Good value |
|---|---|---|---|
| **Agreement** | Does the judge match human labels? | accuracy vs. gold; Cohen's κ for chance-correction | κ > 0.6 (substantial); higher is better |
| **Consistency** | Same input, N runs → same verdict? | run N times (even at temp=0, providers drift); % identical verdict, or variance of score | > 0.95 verdict agreement |
| **Position bias** | Does swapping A/B flip the verdict? | run each pair in both orders; `flip_rate` = fraction that disagree | ≈ 0 |
| **Self-preference** | Does a model-X judge favor model-X outputs? | judge outputs from multiple generators; test for own-generator lift | ≈ 0 lift |
| **Calibration** | When it says "9/10 confident," is it right 90%? | bin by stated confidence, plot reliability curve; ECE | low ECE |

## The headline triad (map to Dario)

- **Repeatable** → consistency
- **Mechanical / impartial** → position bias + self-preference
- **Transparent** → per-criterion breakdown (+ v2 workspace readout)

Lead the report and README with this triad.

## Notes / gotchas

- **Consistency at temp=0 is not guaranteed.** Provider nondeterminism (batching,
  MoE routing, float nonddeterminism) means you still must measure it empirically.
- **Position bias is the biggest silent killer** in pairwise judging. Always run
  both orders; report `flip_rate`. A judge with high agreement but high flip_rate
  is not trustworthy — it got lucky on order.
- **Self-preference is real and measurable** (documented in interpretability work
  too — a "self / sycophancy" concept can fire internally). Cross-generator eval
  is the behavioral proxy.
- **Majority vote over N** is a cheap reliability boost once you've measured
  consistency — but report both the single-shot and voted numbers.
- **Agreement needs chance-correction.** Raw accuracy inflates on imbalanced
  label sets; prefer Cohen's κ (or Krippendorff's α for >2 raters/labels).

## The composite score (leaderboard sort key)

No single number tells the whole story, but for ranking configs in a sweep:

```
rank_score = agreement × consistency × (1 − flip_rate)   # then break ties by cost
```

Report the components separately too — never collapse to one opaque number
(that would recreate the black box we're trying to kill).

## What a report looks like

```
Config                        Agreement  Consistency  FlipRate  SelfPref  $/judge
gpt-5-mini + rubric-v3          0.94        0.97        0.02      0.01     $0.0011  ★
claude-sonnet + rubric-v3       0.96        0.91        0.05      0.00     $0.0090
gemini-flash + rubric-v3        0.88        0.95        0.03      0.02     $0.0004
```
