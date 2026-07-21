# Planning Doc — Transparent LLM Judges for Vendor Selection

*Working draft — brain-dump + distillation. Last updated: July 19, 2026.*

---

## 1. The Ideology (why this company exists)

**Make LLM judges and evals transparent and observable, so people can understand how AI makes decisions — and eventually use AI to make stronger, better decisions they actually trust.**

The long arc: raise the confidence level people have when they use LLMs to do things. Today AI outputs are accepted or rejected on vibes; judgments are black boxes. If the *judging* layer becomes legible — you can see what the judge valued, how it weighed trade-offs, why it preferred A over B — then AI-assisted decisions become auditable, and trust compounds.

The starting point for that thesis is **building judges** — and the first productization is **helping AI companies choose the right vendors**.

## 2. The Problem (wedge)

Every AI agent / AI product is assembled from adjacent components:

- Web search APIs (Exa, Linkup, Tavily, Brave, Perplexity…)
- Model providers (Anthropic, OpenAI, Google, open weights…)
- MCP tools / connectors
- Infra providers
- Data providers / enrichment APIs
- Anything else that goes into an agent's loop

**How these get chosen today is basically arbitrary:**

- A provider was picked years ago and stuck because of legacy relationships. Switching costs feel high because *evaluating the alternative* is the hard part, not the migration.
- When starting something new or adding a feature, teams can't easily answer:
  - Which provider is actually best *for my use case*?
  - Which model is best?
  - How much should I be spending? How much *would* I spend on each option?
  - What's the latency? What's the quality?
- These metrics are blind spots. Teams fall back on **lab-published benchmarks** — which are accurate as far as they go, but are **not representative of what happens in production**. Benchmark distribution ≠ your traffic distribution.

## 3. The Product (v1 concept)

**An eval engine that takes an AI product's production traffic and replays it across alternative providers, then judges the results.**

Canonical example: Harvey (AI legal agent) uses Exa for web search. Harvey routes a slice of its production traffic through other web search APIs. Our engine runs the same queries everywhere, judges the outputs, and shows Harvey that provider X is better on quality, cheaper, or faster — with evidence. Harvey switches with confidence.

### The flow

1. **Ingest** — customer connects production traffic (logs/traces of calls to the incumbent provider), or generates synthetic traffic (see §5).
2. **Select candidates** — pick the vendors/models to test against (e.g., current search API vs. 4 alternatives; current model vs. 3 others).
3. **Configure the judge** — the customer tweaks the judge so it's judging the right things *in the way they want*. Subjective dimensions like quality are defined by them, not by us.
4. **Replay & eval** — run the traffic through every candidate, judge every result.
5. **Report** — results on (at least) three axes: **quality, latency, cost**. Output is a ranked recommendation: "the right vendor for you," with the judge's reasoning fully inspectable.

### The moat: the judge

The differentiation is not the replay harness (that's plumbing anyone can build). It's an **insanely good LLM judge** that is:

- **Transparent** — you can see *what* the judgment is and *how* it was reached.
- **Observable / traceable** — every verdict decomposes into inspectable steps, criteria, and evidence. A judge you can debug.
- **Tweakable** — the customer shapes the judge's preferences and criteria; the judge adapts to their definition of "good."

This is where the ideology and the product meet: the vendor-selection wedge is a forcing function to build the most trustworthy, legible judge in the market.

## 4. Interface (ideal shape)

- User brings production traffic (or synthesizes it).
- Chooses the model and/or vendor they want to test against or switch to.
- Tweaks the judge — criteria, weights, subjective quality definitions.
- Runs evals; gets back per-provider results across quality/latency/cost.
- Picks the right provider from the ranked list, with judge reasoning attached to every score.

## 5. Cold-start: synthetic traffic mode

For teams with no production traffic yet (pre-launch, new feature):

- Describe the use case → we synthesize realistic queries with models.
- Run the same eval pipeline over synthetic data.
- Output: "here's what you should choose to start with."

This doubles as top-of-funnel: anyone evaluating vendors for a *new* build can use us on day one, then graduate to production-traffic evals once live.

## 6. Go-to-market / packaging

- **Now:** open-source on GitHub (the eval engine + judge framework). OSS builds trust — fitting, since transparency *is* the thesis — and gets it into developers' hands.
- **Landing page** early, even in the OSS phase.
- **Later:** hosted product (managed replay, dashboards, continuous monitoring of provider drift, private benchmarks per customer).

## 7. Expansion path

Start narrow, then widen along two axes:

1. **Provider categories:** web search APIs first → models (the biggest one) → MCP tools, data providers, GPS/other APIs, infra — anything an agent depends on.
2. **From one-shot to continuous:** one-time vendor bake-offs → continuous evaluation (providers change under you; the judge keeps watch) → eventually the general-purpose transparent judging layer for any AI decision.

The end state isn't "vendor comparison tool" — it's *the trust layer for AI decisions*. Vendor selection is the first decision worth trusting.

---

## 8. Distillation (the pitch in four lines)

- **Thesis:** AI decisions become trustworthy when the judging is transparent.
- **Wedge:** AI companies choose vendors (search APIs, models, tools, data) arbitrarily, because lab benchmarks don't reflect their production reality.
- **Product:** replay your production traffic across candidate providers; a transparent, customer-tuned LLM judge scores quality/latency/cost and recommends the right one — with reasoning you can inspect.
- **Moat:** the judge — observable, traceable, tweakable — not the harness.

## 9. Open questions to resolve

**Product**
- What's the *minimum* v1? (e.g., web-search-API bake-off only, CLI + report, judge config as a YAML/prompt file?)
- How does the customer *validate the judge itself*? (Meta-eval: judge vs. human agreement rates shown in-product — this may be a core feature, not a nice-to-have, given the transparency thesis.)
- What does "tweaking the judge" concretely look like — natural-language rubric? example-based calibration (label 20 pairs, judge learns preferences)? both?
- Quality/latency/cost — fixed axes, or customer-defined dimensions?

**Data & trust**
- Production traffic is sensitive (Harvey's legal queries!). Self-hosted/OSS-first helps here — is "your traffic never leaves your infra" a core promise?
- Replaying traffic through candidate vendors costs real money and sends customer data to third parties — who pays, and how is that consented/sandboxed?

**Market**
- Who's the buyer — the eng lead adding a feature, or the CTO doing annual vendor review?
- Competitive positioning: eval/observability players (Braintrust, LangSmith, Langfuse, Patronus, Galileo) do evals; nobody owns *vendor selection on your own traffic* as the job-to-be-done. Sharpen that wedge in messaging.
- Do vendors themselves become customers ("prove we're better on real traffic")? That's a second revenue side, but creates neutrality/conflict-of-interest questions — the judge's credibility is the whole business.

**Business**
- OSS license and what stays open vs. what's the paid layer.
- Pricing: per eval run? per replayed request? seat-based? % of savings identified?

## 10. Near-term next steps

1. Name + one-line positioning.
2. Landing page (waitlist + the thesis).
3. v1 scope decision: pick **one** provider category (web search APIs is the obvious first — deep familiarity with the vendor landscape) and **one** interface (CLI/OSS repo).
4. Build the judge framework: traceable verdicts, customer-tunable rubric, meta-eval (judge-vs-human agreement).
5. Design partner: 2–3 AI startups willing to run a slice of production traffic through a bake-off.

---

## 11. How we'd implement this (5 points)

- **Ingest + replay harness** — adapters that take production traffic (or synthetic queries) and fan the same inputs across candidate vendors/models, capturing output + latency + cost per call. This is the plumbing; keep it thin.
- **The judge core** — a traceable LLM judge that scores each output per-criterion with reasoning + evidence attached; config is a YAML rubric (criteria, weights, customer-defined "quality"). Reuse the `knowledge-base/` trust primitives.
- **Meta-eval (the credibility layer)** — let the customer label ~20 pairs, then show judge-vs-human agreement/consistency/bias right in the report. Ship this as core, not a nice-to-have — it's the transparency thesis made real.
- **Report + recommendation** — ranked per-vendor results on quality/latency/cost, every score expandable to the judge's reasoning; output "the right vendor for you."
- **Package as OSS CLI first** — `ingest → sweep → report`, runs locally so sensitive traffic never leaves customer infra; landing page + 2–3 design partners (start with web-search-API bake-offs).

### 11.1 Ingest + replay harness for production or synthetic traffic

Keep it thin, but these are the non-negotiables:

- **One canonical schema + per-vendor adapters.** Normalize every vendor's API into a common request/response shape so you fan out *one* input and compare like-for-like. Adapters are the only vendor-specific code; everything downstream stays vendor-agnostic.
- **Faithful, apples-to-apples replay.** Hold everything constant except the vendor: same query, same result count / `top_k`, same effective params. Log every knob you set — most "vendor X is better" claims die on unequal configs.
- **Capture the full triple per call: output + latency + cost.** Store the raw response verbatim (so the judge can re-score later without re-querying), and measure latency honestly (total vs. time-to-first-byte, excluding *your* harness overhead).
- **Cost must be computed, not guessed.** Each vendor prices differently (per-request, per-1k-tokens, per-result); keep a pricing table that's versioned and dated, since it drifts. Record cost per call so the report is defensible.
- **Data sensitivity is a first-class constraint.** Production traffic can be legal/PII (Harvey!). Design for local/self-hosted runs, optional redaction, and explicit consent before any input leaves the customer's infra to a third-party vendor. "Your traffic never leaves your box" is a feature, not an afterthought.
- **Spend + rate-limit guardrails.** Replaying real traffic costs money and hits vendor rate caps. Build in concurrency limits, per-run budget caps, sampling (test a *slice*, not all traffic), and backoff — so a bake-off can't silently rack up a huge bill.
- **Cache by `(input, vendor, config)` hash.** Never re-pay for a call you've already made; makes reruns free and results reproducible. Same reproducibility principle as the judge side.
- **Robust failure handling as data, not noise.** Timeouts, retries, partial failures — normalize vendor errors and *record error/timeout rate as its own metric*. A vendor that's 5% faster but fails 3% of the time should show that in the report.
- **Interleave, don't batch by vendor.** Run candidates round-robin per query rather than "all of vendor A, then all of B," so time-of-day, network, and vendor-load effects hit everyone equally instead of biasing one.
- **Pin and timestamp everything.** Vendor API version, model version, region, and run time — stored with each result. Vendors change under you; without provenance you can't trust or reproduce a past bake-off.

### 11.2 The judge core

The design moves that make it "traceable" rather than just another LLM-as-judge wrapper:

- **Rubric as a typed YAML contract.** Criteria + weights + a customer-authored `guide` per criterion (their definition of "quality") + a scoring scale. This is the whole tuning surface — natural language where it's subjective, structured where it's mechanical. Validate with a schema so a malformed rubric fails loudly, not silently.
- **Force structured, per-criterion output.** The judge never returns a bare 1–10. It returns `{criterion → score, reasoning, evidence}` via a forced JSON schema (pydantic), and you *refuse the verdict if it doesn't validate*. This is the "no silent garbage" default and what makes verdicts inspectable.
- **Evidence-grounded reasoning.** Require the judge to *quote the specific span* of the output it's scoring against. Anchored evidence kills hand-wavy rationalization and gives the customer something concrete to audit.
- **Aggregate in code, not in the model.** The LLM scores each criterion; the weighted roll-up to a final verdict happens deterministically in code. This guarantees the verdict is *provably a function of the criterion scores* — the "faithfulness gate" made structural, killing the "nice rationale, unrelated verdict" failure.
- **Blind the judge to vendor identity.** For vendor selection this is critical: anonymize outputs to `A`/`B`/`C` so the judge can't brand-bias toward a name or the incumbent. Neutrality *is* the business — a judge caught favoring a name is worthless.
- **Bias defaults baked in.** `temperature=0`, auto order-swap with `flip_rate` reporting for pairwise, cross-generator scoring for self-preference (all from `knowledge-base/02-trust-metrics.md`). On by default, not opt-in.
- **Meta-eval is part of the judge, not a separate tool.** The judge validates itself against ~20 customer-labeled gold pairs and surfaces agreement / consistency / bias *in the report*. Given the transparency thesis, "here's how much this judge agrees with you" is a core feature — it's what lets a customer trust the recommendation.
- **Two-stage tuning, then freeze.** Customer iterates: edit rubric → run on gold set → check agreement → repeat. Once agreement is high, **freeze the judge config** (versioned). Frozen = reproducible = citable. No mid-verdict nudging.
- **Domain rubric packs, shared harness.** The judging machinery is generic; criteria differ per category (web-search relevance ≠ code quality ≠ RAG faithfulness). Ship starter packs, let customers fork them — "harness generalizes, rubrics don't," and it doubles as the OSS contribution surface.
- **Everything is a stored, replayable trace.** Persist each verdict's full trace (inputs, criterion scores, reasoning, evidence, model + rubric version). Re-audit or re-aggregate later without re-calling the model — mirrors the replay harness's caching.

Through-line: the judge is trustworthy because the verdict is a *deterministic function of inspectable, evidence-backed, criterion-level scores from a blinded, frozen, meta-eval-validated judge* — not because the model "seems smart."

### 11.3 Human reinforcement

Targeted human reinforcement — and precisely: it reinforces the **rubric + judge config**, not the model weights (we don't own the models).

- **Gold labels are the anchor.** The primary human input is the ~20–50 labeled examples (the calibration set). The human defines "good"; the judge learns to reproduce it.
- **Bootstrap keeps it cheap.** A stronger model drafts labels; the human confirms/corrects. Low effort, high leverage — if labeling is painful, people skip it and fall back to vibes.
- **Disagreement is the reinforcement signal.** Every judge-vs-human disagreement is the highest-value data point. Loop: disagree → human reviews → either fix the rubric/criteria or add that case as a new calibration example. The judge aligns more each iteration.
- **Active learning, not random labeling.** Surface the cases that matter — low-confidence verdicts, high-variance (flaky) items, and A/B pairs that flipped on order-swap — instead of asking the human to label everything.
- **Config-level RL, not weight-level.** We reinforce the rubric, weights, and calibration set — a frozen, versioned artifact — not model parameters. Reproducible and portable across providers. True RLHF/finetuning is a later, optional lever.
- **The customer is the human, not us.** Reinforces neutrality: subjective "quality" is owned by the customer's labels, so the recommendation reflects *their* standard.
- **Continuous reinforcement guards against drift.** Because production traffic changes over time, periodically sample fresh cases for human review to catch the judge silently drifting on new distributions.

Net: the human is in the **calibration and disagreement-review loop**, not in every verdict. The judge freezes once agreement is high enough; re-engage the human only when meta-eval agreement drops.

### 11.4 Report + recommendation

Ranked per-vendor results on quality/latency/cost, every score expandable to the judge's reasoning, output "the right vendor for you." What makes the report trustworthy and decision-grade:

- **Trade-offs, not a single winner.** Rarely does one vendor win all three axes. Show the Pareto frontier and "best for X" (best quality / cheapest / fastest / best balanced), so the buyer picks against *their* priority rather than a black-box overall score.
- **Every score drills down.** Expand any cell → criterion-level scores → judge reasoning → the quoted evidence span → the raw vendor output. Full path from headline number to source. This is the transparency thesis rendered in the UI.
- **Statistical honesty.** Don't claim "X is better" off 10 queries. Show sample size, confidence intervals, and whether a difference is significant. A close call should *look* close.
- **The judge grades itself in the report.** Surface the judge's own trust metrics (agreement vs. human labels, consistency, `flip_rate`) alongside the vendor results. The reader must know how much to trust the recommendation before acting on it.
- **Segment breakdowns.** Vendor A may win short queries, B long ones; one wins legal-domain traffic, another wins code. Report per-segment winners, not just the global average — that's where real switching decisions live.
- **Cost projected to real money.** Extrapolate per-call cost to "your monthly spend at current volume" per vendor. `-40% cost` in dollars is the line that moves a buyer, not fractions of a cent per call.
- **Actionable recommendation with honest caveats.** "Switch to X: +12% quality, −40% cost, +50ms latency." State the trade-off plainly; never hide the downside.
- **Committable, reproducible artifact.** Report is markdown + JSON with a footer of config hash, model/rubric/vendor versions, and timestamp. Auditable, diffable, citable.
- **Diff / regression mode.** Compare against a previous run to show drift ("Vendor A's quality dropped 8% since last month") — the on-ramp from one-shot bake-off to continuous monitoring.

### 11.5 Package as OSS CLI first

`ingest → sweep → report`, runs locally so sensitive traffic never leaves customer infra. Specifics:

- **Local-first / privacy is the core promise.** Runs entirely on customer infra, bring-your-own API keys, nothing phones home. Fits the transparency thesis and unblocks sensitive traffic (legal/PII). Any telemetry is strictly opt-in.
- **Config-as-files, git-native.** Dataset, rubric, and vendor/candidate lists are all YAML; the report is a committable artifact. Everything lives in the customer's repo and diffs cleanly.
- **Clear command surface.** `init` (scaffold) → `ingest` (load prod traffic or synthesize) → `label` (bootstrap gold set) → `sweep`/`replay` (fan across candidates) → `report` (ranked recommendation). Each stage cached and resumable.
- **CI-friendly by design.** Meaningful exit codes and thresholds so a bake-off can run in a pipeline and *fail the build* when a vendor regresses — the mechanism that turns one-shot into continuous eval.
- **Vendor adapters as plugins.** Adding a provider = writing one thin adapter to the canonical schema. Ship web-search adapters first (Exa, Linkup, Tavily, Brave, Perplexity); models next.
- **Disciplined secrets handling.** Keys via env/`.env`, never logged, never written to the cache. Cache stores results keyed by hash, not credentials.
- **Minimal deps, easy install.** `pip install`, works offline except for the actual vendor calls. Low activation energy = adoption.
- **Explicit open-core boundary.** Decide up front what's OSS (engine, judge framework, adapters, report) vs. paid/hosted later (managed replay, dashboards, continuous drift monitoring, private per-customer benchmarks). License: permissive (MIT/Apache-2.0) to maximize trust and distribution.
- **Day-one usable.** Ship starter rubric packs + example datasets + a quickstart so someone can run a real web-search bake-off in minutes. Pair with an early landing page (waitlist + thesis) and 2–3 design partners running a slice of production traffic.

---

# Part II — Research & the MVP

*Appended July 21, 2026, after a portfolio scan of all 6,063 YC companies (through
S26) and a literature review. Part I above is the thesis; Part II is what survived
contact with evidence, and the MVP we actually build.*

## 12. Research: what the market and the literature say

### 12.1 Method

- **YC scan.** Pulled the full YC company dataset (6,063 companies, Winter 2005 →
  Summer 2026) and pattern-matched across eight axes: evals/observability,
  judges/verifiers/reward models, routing/gateways, benchmarking, vendor selection
  and procurement, search APIs for agents, replay/simulation, and independent
  audit/assurance. Read the long descriptions of every near-neighbour by hand.
- **Literature.** ~20 papers across four clusters: statistical rigour in LLM evals,
  LLM-judge bias, retrieval/relevance judging, and routing.
- **Competitive.** The vendors themselves — including reading the benchmark code
  Exa and Tavily each publish.

### 12.2 Finding #1: the horizontal eval platform is a graveyard. Do not build one.

Of the YC cohort that shipped "LLM eval / observability platform":

| Company | Batch | Status |
|---|---|---|
| Humanloop | S20 | **Acquired** |
| Langfuse | W23 | **Acquired** |
| Helicone | W23 | **Acquired** |
| Chatter | S23 | **Acquired** |
| DAGWorks | W23 | **Acquired** |
| FlowiseAI | S23 | **Acquired** |
| Atla | S23 | **Inactive** |
| Magicflow | W23 | **Inactive** |
| Airtrain AI | S22 | **Inactive** |
| Vango AI | S23 | **Inactive** |
| BricksAI | S22 | **Inactive** |

Eleven companies, zero independent survivors at scale. The ones still standing
went enterprise (Confident AI, W25) or fused evals into a gateway (Respan, W24 —
"observability, evals, *and* gateway"). Outside YC the category consolidated
upward: **Braintrust raised an $80M Series B at ~$800M in Feb 2026.**

Atla is the sharpest cautionary tale, and it echoes `knowledge-base/08`: they built
judge *models* (Selene, 60k+ downloads) and are now inactive. **Being good at
judging is not a business. Being the reason someone changes a vendor is.**

→ **Implication: never say "eval platform."** The category is priced, crowded, and
consolidating. We sell a *decision*, and evals are how we produce it.

### 12.3 Finding #2: the closest neighbours all skip the proof step

| Company | Batch | What they do | What they don't do |
|---|---|---|---|
| **Understudy Labs** | S26 | OSS toolkit: capture traces → evaluate cheaper models → A/B every switch → fine-tune → ship "specialist routes you own" | Destination is predetermined (open weights + your own fine-tune). Not neutral, not multi-vendor, models only. |
| **Conifer** | S26 | Local-first least-cost routing, "~80% cheaper," one invoice | Routes at runtime on a cost heuristic. Never proves quality held. |
| **The Hog** | F25 | One API over Exa/Tavily/Apollo/Clay with "multi-provider waterfall logic" | Aggregates and routes. The customer never sees which source was better or why. |
| **LLM Stats** | S25 | Independent, contamination-proof public benchmarks | Public data, not your traffic. |
| **Respan** | W24 | Observability + evals + adaptive gateway, 1B+ logs/mo | Optimizes within your stack; doesn't run vendor bake-offs. |
| **Armature** | Sp26 | Measures your product's "agent experience" *against competitors* | Sells to the **vendor**, not the buyer — the mirror image of us. |
| **Confident AI** | W25 | DeepEval + enterprise eval/observe/red-team/govern | Grades outputs; assumes you already picked the vendor. |

Understudy Labs is the closest and the most instructive. YC funded, in the most
recent batch, the shape "capture prod traces → benchmark alternatives → only switch
when the held-out eval is beaten." **That validates the motion and tells us where
to differentiate:** they answer *"how do I get off the expensive model?"* We answer
*"which of these N vendors is actually right for me, and can you prove it?"* —
neutral, multi-category (search → rerankers → models → tools → data), and
statistically defensible rather than a pass/fail gate.

→ **Implication:** every neighbour either *routes without proving* or *migrates
toward a predetermined destination*. Nobody sells the **proof**. That's the wedge.

### 12.4 Finding #3: the sharpest pitch in the portfolio is not an AI company

**Floracene (S26)** — "shows independent surgery centers the best-priced equivalent
implant for every procedure." Their own words:

> "90%+ of expensive implants they use are clinically interchangeable, but the
> choice comes down to habit, brand comfort, or the device rep... Roughly ~20–30%
> of that spend is recoverable by switching to a clinically-equivalent device."

That is our thesis, in another market, funded by YC in the latest batch. The shape
— *substitution-with-proof against a habit-driven incumbent* — is repeatedly
fundable: Vendr (S19, acquired) for SaaS contracts, Dexter (F24) for supplier
consolidation, Alara (S25) / DGI (W24) / Reframe (W26) for cross-vendor comparison.

**Our version:** AI vendors are largely interchangeable at the interface, the choice
comes down to habit and whoever you integrated first, 20–40% of spend *and* a real
slice of quality is recoverable — **but unlike implants, nobody can even establish
equivalence, because there is no accepted way to measure it on your own traffic.**
That missing measurement is the product.

### 12.5 Finding #4 (the money slide): every vendor wins its own benchmark

Search vendors publish open-source benchmark harnesses. We read them.

| Source | Claim |
|---|---|
| **Tavily's own repo** (`tavily-ai/tavily-search-evals`; supports Tavily, Exa, Brave, Serper, Perplexity, GPTR) | Tavily wins SimpleQA at **93.3%**; **"Exa Search consistently ranks lowest on both metrics."** |
| **Exa's own repo** (`exa-labs/benchmarks`; ~840 WebCode + 1,400 people + ~800 company queries) | **"Exa dominates across nearly all measured categories"** — 82.8% vs Parallel 74.2%; 72.0% R@1 vs Brave 44.4%; 79% vs 65–66% RAG accuracy. |
| **Linkup** (blog) | Linkup best: **92% F-score on Verified SimpleQA**, "highest of any sub-second web search API." |
| **Parallel** | Parallel **47% on HLE** vs Exa 24%, Perplexity 30%, Tavily 21%. |
| **Exa vs Tavily page** | Exa 81% vs 71% on complex retrieval; p95 latency **1.4–1.7s vs 3.8–4.5s**. |

**Exa is simultaneously "consistently lowest" and "dominates nearly all
categories," depending on whose repo you run.** Both harnesses are open source.
Both are reproducible. Both are honest. They just encode different definitions of
"good" on different query distributions.

This is not a gotcha — **it's the whole argument.** There is no neutral answer
because "best" is distribution-dependent and rubric-dependent. The only defensible
answer is the one computed on *your* queries with *your* definition of good. That
sentence is the company.

> **The line:** *Every search vendor ships an open-source benchmark. Every one of
> them wins it. None of them ran on your traffic.*

### 12.6 Finding #5: the vendor layer is consolidating — a recurring "why now"

**Nebius acquired Tavily for $275M on Feb 10, 2026** (up to ~$400M with earnouts);
Tavily now sits inside an AI cloud. Every acquisition, price change, model
deprecation, and index refresh is a reason your 2023 vendor choice is stale — and a
trigger event for a bake-off. Adjacent: enterprise LLM API spend passed **$8.4B in
2025 and is on track to double**, while per-token prices fell ~280× since 2022 —
i.e. **usage, not price, drives the bill**, so *which* vendor you use compounds.

### 12.7 Findings from the literature (these changed the design)

**(a) The impossibility result — meta-eval is mathematically required, not a nice-to-have.**
*Best Arm Identification with LLM Judges and Limited Human Audits* (arXiv 2601.21471)
proves that **selecting the best arm by judge alone is impossible under differential
bias**: if the judge is biased differently across candidates, *collecting more judge
observations reinforces confidence in the wrong decision.* Empirically, judge-only
selection scored **0% accuracy** in their setup. Full human audit cost 10,500 units.
Their hybrid: **70–90% cheaper than human-only** with δ-correctness guarantees.

> This upgrades §11.3 from "credibility feature" to **load-bearing mathematics**.
> A vendor bake-off without human audits isn't conservative — it's *invalid*. It
> also reframes the meta-eval from a trust-marketing gesture into the thing that
> makes the recommendation mean anything, which is the most defensible technical
> position available to us.

Their algorithm is our spine:
- Estimate each arm as `θ̂ = judge_mean + IPW-corrected residual`, where the
  residual `(human − judge)` is only computed on audited items and reweighted by
  `1/π` to undo selective auditing.
- **Neyman audit allocation:** audit probability `π ∝ √Var(human − judge)` — audit
  where the judge is *unpredictable*, not uniformly. **48% cheaper than uniform
  10% auditing** at identical accuracy.
- **Anytime-valid confidence sequences** (sub-Gaussian for the judge mean, empirical
  Bernstein for the residual, δ/K per arm) so you can peek continuously and stop
  adaptively. Stop when the leader's lower bound clears every challenger's upper
  bound. Coverage measured at 98.8% against a 95% target.

**(b) Paired analysis is free statistical power — and our design is already paired.**
Miller, *Adding Error Bars to Evals* (arXiv 2411.00640, Anthropic): report SEM and
95% CI; use **clustered standard errors** when questions come in groups; and run
**question-level paired-difference tests** when comparing two systems, which
eliminates question-difficulty variance. Replay sends *the same query to every
vendor* — it is paired by construction. Most vendor "benchmarks" throw this away by
comparing population means.

**(c) Position bias is worst exactly where we operate.**
*Judging the Judges* (arXiv 2406.07791): position consistency ranges ~0.57–0.82
across judges; the dominant driver is the **answer-quality gap** — judges are
consistent when candidates differ a lot and **flip when candidates are similar**.
Question/response/prompt length barely matter. Broader surveys put position bias at
**10–15 points of win-rate swing** and verbosity bias at **15–30 points**.

> Competing vendors are *by definition* close in quality. So our use case sits in
> the worst region of the bias curve. Design consequence: **an order-swap flip is
> not noise to average away — it is the finding.** Flips get reported as
> "too close to call," never silently resolved.

**(d) Listwise ranking is the worst way to compare 5 vendors.**
Position bias is present in pointwise, pairwise, *and* listwise, but **listwise
suffers most and pairwise least.** Pairwise over all candidates is O(n²).
→ **Resolution: pairwise against the incumbent as the control arm.** O(n),
minimum-bias comparison mode, and it exactly matches the business question
("should I switch *from what I have*?").

**(e) Checklists beat scalar scores, and make small judges viable.**
*RocketEval* (ICLR 2025, arXiv 2503.05142): reframe judging as answering an
**instance-specific checklist**, grade items with a lightweight model, then
**reweight checklist items via supervised fitting to human annotations**.
Gemma-2-2B reached **0.965 correlation with human preferences — comparable to
GPT-4o — at >50× lower cost**, explicitly because checklists cut uncertainty and
positional bias. *Replacing Judges with Juries* (arXiv 2404.18796, Cohere): a panel
of three small models from **disjoint families** beats one large judge, with less
intra-model bias, at **>7× lower cost**.
→ Checklist grading + a small-model panel is both cheaper *and* less biased. And
item reweighting is exactly the "human reinforcement" loop of §11.3, done properly.

**(f) Criteria drift — the rubric cannot be configured up front.**
Shankar et al., *Who Validates the Validators?* (UIST 2024, arXiv 2404.12272):
**"users need criteria to grade outputs, but grading outputs helps users define
criteria."** Criteria are often dependent on the specific outputs observed.
→ Kills plan.md §3 step 3 ("configure the judge") as a *first* step. The rubric UI
must be **grade-then-refine**: show real outputs, let the user react, mine criteria
from their reactions. Configure-first is a research-documented failure mode.

**(g) There is a credible, citable default rubric for search.**
UMBRELA (arXiv 2406.06519) reproduces Bing's LLM relevance assessor on a 0–3 graded
scale, correlates highly with human labels and system rankings across TREC DL
2019–2023, and was **adopted by TREC 2024 RAG for automated evaluation.** Known
failure mode: LLM judges **over-rate relevance** relative to humans, with false
positives correlating with query-term presence.
→ Ship UMBRELA-style graded relevance as the v1 default rubric (nDCG@k / MRR /
recall@k computed on top), and note that its known over-rating bias is precisely
what the human audit correction in (a) removes.

**(h) PPI: 20 human labels can become an estimator, not a vibe check.**
Prediction-Powered Inference and StratPPI (arXiv 2406.04291, Fisch et al.) combine a
small human-labeled set with a large auto-labeled set to get **unbiased estimates
with tighter intervals than human-only**; stratification tightens further when
autorater accuracy varies across the distribution. *How to Correctly Report
LLM-as-a-Judge Evaluations* (arXiv 2511.21140) adds plug-in correction for imperfect
judge sensitivity/specificity, CIs accounting for both test *and* calibration
uncertainty, adaptive calibration allocation, and — importantly — **unbiasedness
under distribution shift between calibration and test sets**, which naive approaches
lack. (Relevant: your gold set will *always* drift from live traffic.)

**(i) What we're replacing costs weeks.** Current best practice for a provider swap
is **shadow-test for 1–4 weeks at ~2× inference cost, ~10,000 production cases,
then canary** — a 3–6 week window, hand-rolled per team.

**(j) Ingest is a solved standard — don't build SDKs.** OpenTelemetry **GenAI
semantic conventions** (CNCF GenAI SIG, v1.37+) standardize `gen_ai.*` spans:
`gen_ai.request.model`, `gen_ai.usage.input_tokens`/`output_tokens`,
`gen_ai.provider.name`, `gen_ai.input.messages`/`output.messages`, operation names
`chat` / `embeddings` / `execute_tool` / `invoke_agent`, span naming
`{operation} {name}` (e.g. `execute_tool web_search`). Adopted by Datadog, AWS,
Azure, GCP.
→ **v1 ingest = read OTel GenAI spans.** One adapter, industry-standard, and most
target customers already emit it. Building a proprietary SDK would be the single
biggest waste of MVP time.

---

## 13. The MVP

### 13.1 Scope decision: web-search APIs first — and the reason isn't familiarity

The deciding criterion is **reversibility**: pick the category where acting on the
recommendation is a one-line change, so value is realized in days, not quarters.

| | Web search APIs | Models |
|---|---|---|
| Candidate set | 5–7, well-defined | 50+, fuzzy |
| Cost to replay 1k queries × 5 | **~$30** | $50–500+ |
| Output length to judge | Short (10 results) | Long-form, expensive |
| Cost of acting on the answer | **One API call swap** | Prompt migration, regression risk |
| Vendor claims | **Provably contradictory (§12.5)** | Partially settled by public leaderboards |
| Competitive density in YC | ~zero | Understudy, Conifer, routers, every eval platform |
| Buyer urgency trigger | Tavily→Nebius, index churn, price changes | Model deprecations |

→ **v1 = web-search API bake-offs.** Expansion order, by rising switching cost:
**search → rerankers/embeddings → models → MCP tools & data providers → infra.**
(Rerankers second is deliberate: same shape as search, same rubric machinery, and
ZeroEntropy-class vendors make it a live decision.)

### 13.2 The product in one sentence

> **Point it at your traffic, pick your candidates, and it returns a switching
> decision with a confidence interval — or tells you the difference isn't real.**

The second half matters as much as the first. A tool willing to say *"these two
vendors are indistinguishable on your traffic; keep the cheaper one"* is a tool you
can trust when it says switch. **Our defensible negative is the credibility asset.**

### 13.3 The core protocol (this is the actual invention)

**Challenger-vs-incumbent, paired, order-swapped, audit-debiased.**

1. **Ingest.** Read OTel GenAI spans (`execute_tool web_search`), or a CSV/JSONL of
   queries, or synthesize from a use-case description. Sample a slice, don't take
   everything.
2. **Stratify.** Bucket queries by observable features (length, intent class,
   domain, has-entity). Stratification tightens intervals (StratPPI) *and* produces
   the per-segment winners that drive real decisions.
3. **Replay, interleaved.** Round-robin per query across incumbent + challengers —
   never "all of A, then all of B" — so time-of-day and vendor-load effects hit
   everyone equally. Cache by `(query, vendor, config)` hash. Record output verbatim,
   TTFB, total latency, computed cost, and error/timeout as a first-class metric.
4. **Judge, pairwise vs. the incumbent, both orders.** Instance-specific checklist
   (RocketEval), graded by a **panel of 3 small models from disjoint families**
   (PoLL), each item requiring a **quoted evidence span**. Roll up to a verdict
   **deterministically in code**, never in the model.
   - Order-swap flip → labeled **`TOO_CLOSE`**, surfaced, never averaged away.
   - `flip_rate` is a headline number, not a footnote.
5. **Audit, variance-guided.** Choose which items a human labels by Neyman
   allocation `π ∝ √Var(human − judge)`, targeting ~10% audit rate, floor `π_min`.
   Bootstrap each label with a stronger model drafting and the human confirming.
6. **Estimate.** `θ̂_vendor = judge_mean + IPW(human − judge)` per stratum, with
   anytime-valid confidence sequences and δ/K allocation across K candidates.
   Question-level **paired differences** vs. the incumbent (Miller).
7. **Stop.** When the leader's lower bound clears all challengers' upper bounds →
   declare a winner. When budget is exhausted first → **declare no significant
   difference and say so.** Both are valid, reportable outcomes.

**Why this is hard to copy:** any competitor can fan out API calls. The moat is
(1) the audit-debiasing estimator that makes the verdict *valid* rather than
*plausible*, (2) the frozen, versioned, reproducible rubric artifact, and (3) the
neutrality that comes from selling to the buyer, never the vendor.

### 13.4 What v1 deliberately does NOT include

Cut ruthlessly. Everything below is post-MVP:

- ❌ Runtime routing / gateway (that's Conifer, Respan, OpenRouter — and it makes us
  a dependency instead of an auditor)
- ❌ Hosted dashboard, accounts, multi-tenancy
- ❌ Fine-tuning or model training (that's Understudy/Cascade)
- ❌ Continuous monitoring — v1 ships `diff` against a previous run and stops there
- ❌ Mechanistic interpretability / J-lens tier (`knowledge-base/03–05`) — v2 moat,
  not v1 scope
- ❌ Categories beyond web search
- ❌ Anything that requires the customer's data to leave their machine

### 13.5 Shape, commands, stack

Local-first OSS CLI. Config in, committable report out. No server, no DB.

```bash
bakeoff init                      # scaffold: candidates.yaml, rubric.yaml, .env
bakeoff ingest --otel ./traces/   # or --csv queries.csv, or --synthesize "legal research agent"
bakeoff run --incumbent exa --challengers tavily,brave,linkup,parallel \
            --budget 50usd --audit-rate 0.10 --confidence 0.95
bakeoff label                     # only the items Neyman allocation asked for
bakeoff report                    # report.md + report.json + config hash
bakeoff diff ./runs/2026-06 ./runs/2026-07   # drift
```

- **Stack:** Python · `pydantic` (forced schemas, refuse-on-invalid) · `litellm`
  (LiteLLM is YC W23 — the adapter layer, don't rebuild it) · SQLite cache ·
  `presidio` optional redaction pass before anything leaves the box.
- **Reuse from `knowledge-base/`:** the trust-metric definitions (`02`), the
  freeze-and-version discipline (`01`), the pipeline shape (`06`). The engine is
  the same harness pointed at vendors instead of judges.
- **Privacy is the sales argument, not a checkbox.** Runs entirely local, BYO keys,
  nothing phones home, opt-in telemetry only, `--redact` before any third-party
  call. Harvey-class customers cannot use a hosted alternative at all.

### 13.6 Rubric UX: grade-then-refine (per §12.7f)

Wrong: "configure your judge, then run." Right:

1. Run a 20-query pilot with the UMBRELA-style default rubric.
2. Show the user **real side-by-side outputs** and ask for their verdict on ~20.
3. **Mine criteria from their disagreements with the default**, propose rubric edits
   in their language, show the agreement (Cohen's κ) move.
4. Iterate until κ clears threshold → **freeze and version the rubric.** Frozen =
   reproducible = citable. No mid-verdict nudging (`knowledge-base/01`).

### 13.7 The report

Every principle in §11.4 stands. The research adds four requirements:

- **Paired differences with CIs**, not two population means side by side.
- **`TOO_CLOSE` is a first-class verdict**, with `flip_rate` shown next to every
  headline number.
- **A judge-trust panel** at the top: agreement (Cohen's κ), audit count, audit
  rate, coverage, `flip_rate`, panel disagreement. *The reader must know how much
  to trust the recommendation before reading it.*
- **Per-stratum winners** — the global average is usually the least actionable number
  in the report.

Headline format:

```
Switch to Linkup for entity queries (61% of your traffic):
  quality  +7.2 pts  [95% CI: +3.1, +11.3]  (paired, n=612, 58 audited)
  cost     -34%      ($1,240/mo → $818/mo at your current volume)
  latency  +180ms p95
  flip_rate 0.04 · κ vs your labels 0.81 · 3-model panel, 2 dissents

Short factual queries (39%): no significant difference. Keep Exa.
```

### 13.8 Cost model — the number that sells the demo

Per bake-off, 1,000 queries × 5 vendors:

| Line | Cost |
|---|---|
| 5,000 searches @ ~$5–9/1k (Exa $7, Brave $5–9, Linkup €5, Tavily $5–8, Perplexity $5) | **~$30** |
| ~8,000 checklist judgments, small-model panel (RocketEval: >50× cheaper) | **~$5–15** |
| Human audit: ~10% of decisions, bootstrap-drafted | **~1 hour** |
| **Total** | **< $50 and under an hour** |

Against the status quo — **1–4 weeks of shadow traffic at ~2× inference cost across
~10,000 cases, then canary, a 3–6 week window.**

> **The demo claim: a defensible vendor switching decision for under $50 and one
> hour of human attention, instead of a month of shadow traffic.**

### 13.9 Build plan

| Week | Ship | Done when |
|---|---|---|
| **1** | Canonical schema, 5 search adapters (Exa, Tavily, Brave, Linkup, Parallel), interleaved replay, hash cache, versioned pricing table, latency/error capture | `bakeoff run` produces a clean result matrix on 100 queries |
| **2** | Checklist judge: forced pydantic schema, evidence spans, 3-model disjoint panel, code-side aggregation, mandatory order swap + `flip_rate`, `TOO_CLOSE` | Judge never emits an unvalidated verdict; flips are visible |
| **3** | **The statistics layer** — paired differences, stratification, Neyman audit allocation, IPW residual correction, anytime-valid confidence sequences, stopping rule | Simulation harness confirms coverage ≥ nominal; correct answer at ~10% audit rate |
| **4** | `label` (bootstrap-drafted), `report` (md+JSON, drill-down to evidence, monthly-$ projection), `diff`, UMBRELA-style starter rubric pack, quickstart | A stranger runs a real 5-vendor bake-off from a cold `pip install` |
| **5–6** | Design partners + the public leaderboard (§13.10) | 3 partners have run their own traffic; leaderboard live and reproducible |

Week 3 is the week that matters. Weeks 1–2 are plumbing anyone can write; week 3 is
the company. If schedule slips, cut week 4 features, never week 3.

### 13.10 Distribution: the neutral leaderboard

Same engine, second surface — mirrors the three-layer structure in
`knowledge-base/09`.

Publish a **continuously-updated, fully reproducible, neutral leaderboard for
search APIs**, generated by the OSS harness, with the rubric, query set, run
config, and raw outputs public. Explicitly positioned against §12.5:

> *Four vendors publish four benchmarks and each one wins. Here's one that nobody
> being measured paid for — and here's the command to reproduce it yourself.*

Why it compounds: it's the credibility proof (transparency thesis rendered as a
public artifact), the top-of-funnel ("this is great, but run it on *my* queries" →
`pip install`), the PR engine on every vendor launch and acquisition, and the
design-partner bait. **Neutrality is enforced structurally: we never take money
from a vendor being ranked.** That single rule is the asset — and it is why we
cannot become Armature, which sells the same measurement to the vendor.

### 13.11 Design partners

Target teams where search quality is visibly load-bearing and traffic is
sensitive enough that local-first is a requirement, not a preference: AI legal and
finance research (Harvey-class), deep-research agents, GTM/enrichment agents,
support agents with retrieval. YC's own portfolio is the warm list — every company
that names Exa/Tavily/Serper in its stack is a prospect, and the RL/eval cohort
(hud, Osmosis, Halluminate, Polymath, Ressl) are peers who understand the argument
immediately.

**The ask is small on purpose:** "give us 500 of your search queries, redacted,
and one hour of one engineer's labeling. You get a report you can act on today."

### 13.12 Traction target for the application

One sentence, and it should be a *finding*, not a feature list:

> **"We ran neutral bake-offs on 5 companies' real production traffic. In 4 of 5,
> the vendor they'd been paying for since 2023 was not the best one for their
> traffic — and in 2 of those, that vendor's own published benchmark had claimed
> it was."**

That last clause is the whole company in eleven words.

### 13.13 Risks and kill criteria

| Risk | Mitigation | Kill criterion |
|---|---|---|
| **Vendors are genuinely indistinguishable** on real traffic — nothing to sell | Cost/latency deltas are large and real even at quality parity; "keep the cheaper one, here's proof" is still a decision worth paying for | If <2 of 5 design partners have *any* significant difference on any stratum, the wedge is wrong — move to rerankers or models |
| **One-shot purchase** — you buy once, then never again | Trigger events are frequent (acquisitions, price changes, index refreshes, new entrants); `diff` mode + CI thresholds convert one-shot into continuous | If no partner re-runs within 60 days, the continuous story is fiction |
| **Judge disagrees with the buyer** and they don't trust the result | κ is reported before the recommendation; grade-then-refine raises it; audit correction makes the estimate valid even with a mediocre judge | If κ can't clear ~0.6 after rubric iteration on 3 of 5 partners |
| **Buyer won't send traffic to competitors** (legal/PII) | Local-first, BYO keys, Presidio redaction, explicit per-vendor consent gate | — |
| **Incumbent eval platforms bolt this on** (Braintrust at $800M has the traces) | They grade outputs and assume the grader is fine; the audit-debiasing estimator + structural neutrality is not a feature they can bolt on while selling to everyone | — |
| **A gateway commoditizes it** (Respan, Conifer, OpenRouter) | Their incentive is to route, not to tell you to leave. Structurally they cannot be neutral about vendors they resell | — |
| **We're too niche** (search APIs is a small market) | Search is the wedge, not the market: the harness is category-agnostic and rerankers/models/tools follow | If expansion to rerankers takes >1 month of new engine work, the harness isn't as generic as claimed |

### 13.14 Application drafts

| Field | Answer |
|---|---|
| **What we make** | We replay your production traffic across candidate AI vendors and give you a switching decision with a confidence interval — or tell you the difference isn't real. OSS CLI, runs on your infra. |
| **One-liner (≤50 chars)** | *Prove which AI vendor is best on your traffic.* |
| **The problem** | Every AI vendor publishes a benchmark it wins. Exa's repo says Exa dominates; Tavily's repo says Exa ranks last. Both are open source. Neither ran on your queries. |
| **Why now** | The vendor layer is consolidating (Nebius bought Tavily for $275M in Feb 2026), enterprise LLM API spend passed $8.4B and is doubling, and the standard alternative — 1–4 weeks of shadow traffic at 2× cost — is something almost nobody actually does. |
| **What's new / technically hard** | A judge alone provably *cannot* pick the best vendor: under differential bias, more judge samples increase confidence in the wrong answer (arXiv 2601.21471). We combine a cheap checklist judge with variance-guided human audits and an IPW-debiased, anytime-valid estimator — a statistically valid decision at ~10% audit cost, ~70–90% cheaper than human-only. |
| **Competitors** | Braintrust/Confident AI grade outputs *after* you picked the vendor. Conifer/Respan/OpenRouter route at runtime and can't be neutral about vendors they resell. Understudy Labs migrates you to a predetermined destination (open weights). Armature sells the same measurement to the *vendor*. Nobody sells the buyer a defensible switching decision. |
| **Business model** | OSS engine free. Paid: hosted continuous re-runs and drift alerts, private per-customer benchmarks, and a signed reproducible report. Deliberately *not* shared-savings — taking a cut of savings gives us an incentive to recommend switching, and neutrality is the entire asset. |
| **Why us** | Deep familiarity with the search-vendor landscape, and a prior body of work (`knowledge-base/`) on exactly what makes a judge trustworthy — agreement, consistency, position bias, self-preference, calibration. |

### 13.15 Open questions from §9, now resolved

| Question | Resolution |
|---|---|
| What's the minimum v1? | Web-search bake-off, OSS CLI, local-first. §13.1–13.5. |
| How does the customer validate the judge? | Not just reported agreement — the human labels *enter the estimator* via IPW correction. The judge doesn't have to be perfect; the estimate has to be valid. §13.3. |
| What does "tweaking the judge" look like? | Grade-then-refine, not configure-first — criteria drift makes upfront configuration a documented failure mode. §13.6. |
| Fixed or customer-defined axes? | Quality/latency/cost fixed as the reporting frame; *quality* is defined entirely by the customer's checklist and labels. |
| Who pays for replay cost? | Customer, BYO keys, with a hard `--budget` cap. A full bake-off is <$50. |
| Do vendors become customers? | **No.** Structural rule: we never take money from a vendor we rank. Armature (Sp26) already occupies the vendor side; being neutral is the only differentiated position left. |
| Pricing? | Not shared-savings — it corrupts the recommendation. Per-run / seat / enterprise continuous. |
| OSS boundary? | Open: engine, adapters, judge framework, rubric packs, report. Paid: hosted continuous runs, drift alerts, private benchmarks, signed reports. Apache-2.0. |

Still open: the name; whether the public leaderboard should launch before or with
the CLI; and whether rerankers or models is the correct second category.

### 13.16 References

**Statistical core**
- *Best Arm Identification with LLM Judges and Limited Human Audits* — arXiv 2601.21471 — **the spine of §13.3**
- Miller, *Adding Error Bars to Evals* — arXiv 2411.00640 (Anthropic)
- Fisch et al., *Stratified Prediction-Powered Inference* — arXiv 2406.04291
- *How to Correctly Report LLM-as-a-Judge Evaluations* — arXiv 2511.21140
- *Valid Best-Model Identification via Low-Rank Factorization* — arXiv 2605.10405
- Howard et al., time-uniform confidence sequences; Track-and-Stop (fixed-confidence BAI)

**Judge design**
- Wei et al., *RocketEval: Efficient Automated LLM Evaluation via Grading Checklist* — ICLR 2025, arXiv 2503.05142
- Verga et al., *Replacing Judges with Juries* — arXiv 2404.18796 (Cohere)
- *Judging the Judges: Position Bias in Pairwise Comparative Assessments* — arXiv 2406.07791
- *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge* — arXiv 2410.02736
- *Self-Preference Bias in LLM-as-a-Judge* — arXiv 2410.21819
- Shankar et al., *Who Validates the Validators?* — UIST 2024, arXiv 2404.12272

**Retrieval judging**
- Upadhyay et al., *UMBRELA* — arXiv 2406.06519 (adopted by TREC 2024 RAG)
- SimpleQA, FRAMES (824 multi-hop), BrowseComp (1,266 queries) — cold-start seed sets

**Routing (adjacent, not our product)**
- RouteLLM, RouterBench (AIQ metric), FrugalGPT

**Primary sources for §12.5**
- `github.com/tavily-ai/tavily-search-evals` · `github.com/exa-labs/benchmarks` · Linkup and Parallel published benchmarks
