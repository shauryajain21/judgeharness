# 09 — Product: three layers, one engine

Same backend (the harness from `06-architecture.md`, pointed at graders instead of
outputs). Three surfaces on top, each a different stage of the funnel.

```
                 ┌─────────────────────────────────────────┐
                 │   ENGINE  (sweep + trust metrics + J-lens) │
                 │   behavioral battery + reward-hack attacks  │
                 └─────────────────────────────────────────┘
                    ▲              ▲                  ▲
        ┌───────────┘        ┌─────┘          ┌───────┘
   1. FREE GRADER        2. OSS CLI        3. B2B PLATFORM
   (top of funnel)       (dev wedge)       (revenue)
   web, no signup        npx, GitHub       continuous cert
   shareable score       Action            + interp moat
```

## Layer 1 — Free grader (the Product Hunt hero, top of funnel)

Paste an eval prompt / pick a model → **0–100 reliability score + a shareable
report card** in 30s. No signup. The card is the viral loop.
- Checks: position bias, length bias, self-preference, sycophancy, **gameability**.
- Pattern = HubSpot Website Grader / GPTZero: score free, the *fix* gated.

## Layer 2 — OSS CLI (the developer wedge, bottom-up land)

```
npx gradecheck <your-judge>     # red/green report in the terminal
```
Plus a GitHub Action. Buys the open-source badge, Hacker News + Dev Hunt reach,
and bottom-up adoption (the Snyk motion). Free tier generous; continuous runs paid.

## Layer 3 — B2B platform (the revenue)

Gated behind the free score:
- **Continuous certification** in the training/RL loop; reward-drift alerts.
- A signed, version-hashed **Verifier Trust Report** vendors attach to lab deliverables.
- A **"Judge Certified" badge** for model cards / READMEs.
- **Interpretability tier** (open-weight): read whether the grader *internally*
  represents "I'm being gamed" even when its score looks clean. The moat.

## The engine (what all three call)

- **Behavioral battery** — already specced in `02` + `05`: order-swap → flip-rate,
  criterion ablation, paraphrase, authority injection, cross-generator self-pref,
  consistency-N. Ships now, any API model.
- **Reward-hack attack library** — the new build: adversarial candidates that
  *farm reward without solving* (verbosity, format-matching, reference leakage,
  sycophancy triggers, spec-gaming). Measures reward↔solve correlation +
  hack-susceptibility. Bounded, well-scoped (reward-hack benchmark literature
  gives the taxonomy).
- **Interpretability tier** — logit lens first, then J-lens (`04`). v2, open-weight.

## Why one engine, three surfaces

The free grader generates the shareable **failure-signature dataset** (the data
flywheel / moat). It's simultaneously: PH virality, YC traction proof, design-partner
bait, and top-of-funnel for the certification contracts. One artifact, every channel.

> Free score → OSS scan lands in the org → team-wide continuous certification.
