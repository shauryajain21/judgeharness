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
