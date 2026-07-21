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
