# 08 — Market & the pivot

Where the wedge points, and why. "Evaluate an LLM judge" is a real pain but a
hard *product* to sell. The asset that transfers is bigger than the framing.

## Two things transfer (the judge is just one instance)

1. **A reliability method for fuzzy AI decisions** — agreement, consistency,
   position bias, self-preference, calibration. A *reward model is a judge*. A
   *verifier is a judge*. A *guardian/referee is a judge*.
2. **A mechanistic-interpretability capability** — read the model's *unspoken*
   reasoning (J-lens tier). Rare, funded hard (Goodfire $1.25B, Dec 2025), but
   everyone aims it at model *builders*, nobody at *trust buyers*.

## The pivot (locked direction)

> Not "we evaluate your LLM judge" — **"we're the independent trust layer for AI
> verifiers and reward models: we red-team them for reward hacking and certify
> they can't be gamed."**

A reward model / verifier / LLM-judge is the *grader* that trains and gates AI.
If the grader is gameable, you ship a model that learned to cheat while your
metrics looked great (METR: o3 reward-hacks 30% of runs *knowing* it cheats;
Anthropic Nov 2025: reward hacking generalizes to sabotage). **Everyone tests the
agent; nobody independently certifies the grader that trains it.**

## Adjacent markets, ranked (research synthesis, 2025–2026)

| Market | Why it's the pivot | Buyer / urgency |
|---|---|---|
| **Reward models / RL verifiers** ★ | Field declared *verification the bottleneck* (Verifier's Law). Reward hacking now a safety-grade problem. A reward model *is* a judge → near-zero repositioning. | RL-env & data vendors (Surge, Mercor, Scale, Handshake, Prime Intellect) — must *prove* verifier quality to the labs they sell to. Buy, not build. |
| **Guardian agents** | Gartner named the category (Feb 2026); 10–15% of the ~$46–52B agentic market → **$5–8B by 2030**. >40% of agent projects canceled by 2027 on trust. *Independence* is the stated buying criterion. | Security/risk + AI-eng leaders. Runtime referee for agent decisions. |
| **AI governance / audit** (interp moat) | SR 11-7 model validation, NYC LL144 bias audits, EU AI Act. Interp-as-audit is unclaimed. | Financial Model Risk / CRO first. Slow, big budgets. The *second act*, not the wedge. |
| Content moderation / T&S | Literal "repeatable auditable fuzzy judgment"; DSA/OSA mandate consistency + appeals. | Platforms (often build in-house). |
| Hiring / credit decisioning | Hardest literal audit statutes; but crowded incumbents + softening US enforcement. | Proof points, not primary market. |

## Why YC-legible

- **White space in YC's own portfolio.** YC funds the *supply* side heavily (HUD,
  Osmosis, Refresh, Idler build verifiers/RL envs). **No YC company audits the
  verifier.** Their portfolio are our design partners.
- Garry Tan: *"Evals are emerging as the real moat for AI startups."* We go one
  level up — certify the eval itself.
- Cautionary comp: **Atla (S23)** built judge *models* → now inactive. We don't
  build a judge; we're the independent auditor of everyone's. A vendor can't
  grade its own grader.

## Landmines

- **Not "AI safety / alignment."** Frame as a money + shipping problem (you
  trained on a broken reward signal). YC is cold on safety-as-mission.
- **Not "an eval platform."** Crowded inside YC (Confident AI, ZeroEval, Soren,
  Kairos). Our category is a level up: certify the grader.
