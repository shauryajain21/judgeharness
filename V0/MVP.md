# MVP — Metanoia v1: AI Model Bake-off

*The smallest thing that proves the thesis: describe a use case → get a validated,
inspectable model recommendation across quality / latency / cost, in one CLI run.*

Last updated: July 22, 2026.

---

## 1. Scope decision

- **Category:** AI **model providers** (not web search).
  - Biggest, hottest pain: "which model for my use case, and what will it cost me?"
  - Sharpest neutrality story: the judge is itself a model, so **self-preference
    bias** is a real, documented failure — which makes our blinding + meta-eval
    machinery the whole point, not a nice-to-have.
  - Plumbing is nearly free: `litellm` gives every provider behind one adapter, so
    effort goes into the judge (the moat), not the harness.
- **Interface:** local **OSS CLI**. No hosted product, no UI, no dashboards yet.
- **Traffic:** **synthetic** front door (cold-start mode). No production-traffic
  ingestion in v1 — it sidesteps the two hardest early problems (wiring up
  sensitive traffic + third-party consent) and doubles as top-of-funnel.
- **Axes:** fixed — **quality, latency, cost**.

## 2. The flow (four commands)

```bash
metanoia init support-drafter     # scaffold a project
metanoia synth                    # generate synthetic inputs from a use-case description
metanoia sweep                    # fan inputs across candidate models, judge each (blinded)
metanoia report                   # ranked recommendation + judge's self-trust metrics
```

Project layout:

```
support-drafter/
  usecase.yaml        # what you're building + who the user is
  candidates.yaml     # models to bake off + shared knobs (temp, max_tokens)
  rubric.yaml         # the judge: criteria, weights, your definition of "good"
  gold.yaml           # ~15 human-labeled examples to validate the judge (meta-eval)
  runs/               # cached raw completions (by hash) + full verdict traces
  report.md           # committable output
```

## 3. Worked example — customer-support reply drafter

A team building a support-reply drafter doesn't know which model to ship. No traffic yet.

### 3.1 Describe the use case

```yaml
# usecase.yaml
task: draft a support reply from a ticket + knowledge-base snippet
user: SaaS support team, friendly-but-concise tone
inputs_to_synthesize:
  - a customer ticket (varying anger, clarity, topic)
  - 1-2 relevant KB snippets
volume: 50
```

`metanoia synth` uses a strong model to expand this into 50 diverse, realistic
inputs, **saved to disk as a visible, editable artifact** (so a human can prune or
adjust before spending money on the sweep).

### 3.2 Candidates + rubric (same input to every model, blinded to identity)

```yaml
# candidates.yaml
candidates: [gpt-5, gpt-5-mini, claude-sonnet-4.5, gemini-2.5-flash, llama-4-70b, deepseek-v3]
temperature: 0
max_tokens: 400
```

```yaml
# rubric.yaml
mode: score            # 1-5 per criterion
criteria:
  - {name: correctness, weight: 0.35, guide: "reply matches the KB; no invented policy"}
  - {name: tone,        weight: 0.25, guide: "friendly, concise, on-brand"}
  - {name: resolution,  weight: 0.25, guide: "actually resolves or advances the ticket"}
  - {name: safety,      weight: 0.15, guide: "no over-promising, no leaking internal notes"}
```

### 3.3 Sweep

50 inputs × 6 models = 300 completions, streamed (capture TTFT + total), token-costed,
cached by `(input, model, config)` hash, then judged **blinded** at `temperature=0`.

### 3.4 Report

```
METANOIA — support-drafter  ·  50 synthetic tickets  ·  2026-07-22

Model               Quality  TTFT   total   $/1k tasks  Verdict
claude-sonnet-4.5    4.44    340ms  2.1s     $9.20       * best quality
gpt-5                4.39    410ms  2.8s     $12.50
gpt-5-mini           4.12    280ms  1.4s     $1.90       > best value
gemini-2.5-flash     3.98    190ms  0.9s     $0.60       > fastest / cheapest
llama-4-70b          3.71    520ms  3.0s     $0.80
deepseek-v3          3.55    600ms  3.4s     $0.40

Recommendation: gpt-5-mini — 93% of top quality at ~1/5 the cost & half the latency.
Judge trust on your 15 gold labels: agreement 0.86 · flip-rate 0.03 · self-pref 0.01
Every score -> expand for criterion breakdown, reasoning, and quoted evidence.
```

The **"best value"** line — near-frontier quality at a fraction of cost/latency — is
the money shot for a model decision.

## 4. Model-specific things to nail

- **Self-preference must be measured and shown.** Pick a judge from a *different*
  family than most candidates (or rotate judges and report cross-judge agreement).
  Surface a `self-pref` number in the report — it's the credibility line that
  proves the ranking isn't rigged.
- **Quality is subjective**, so the ~15 gold labels matter even more than in a
  search bake-off. The judge-vs-human **agreement** line is what earns the right to
  make a recommendation at all.
- **Token cost, computed not guessed.** Versioned, dated pricing table per model;
  record input+output tokens and cost per call.
- **Latency measured honestly.** TTFT and total, excluding our own harness overhead;
  report p50 and p95, not just the mean.

## 5. Judge design (inherited from plan.md §11.2)

- Rubric is a typed YAML contract; malformed rubric fails loudly.
- Forced per-criterion structured output `{score, reasoning, evidence}`; refuse
  verdict on schema-validation failure.
- Evidence-grounded: judge must quote the span it's scoring.
- Aggregate weights **in code**, not in the model → verdict is provably a function
  of the criterion scores.
- Blinded to model identity (`A`/`B`/`C`).
- Bias defaults on: `temperature=0`, order-swap + `flip_rate` (pairwise mode),
  cross-generator scoring for self-preference.
- Meta-eval built in: judge-vs-human agreement / consistency / bias shown in report.
- Two-stage tuning then **freeze** the (versioned) judge config.
- Every verdict stored as a replayable trace.

## 6. Honest caveats (state these in the product)

- **Synthetic ≠ production.** Report labels itself "synthetic"; frames output as
  "where to *start*," graduating to real-traffic evals once the customer is live.
- **The synthesizer is a quiet risk:** a biased query generator biases the whole
  verdict. Generated inputs are a visible, editable artifact.
- **Unvalidated judge = no recommendation.** If judge-vs-human agreement on the gold
  set is low, tune the rubric before trusting the ranking.

## 7. Explicitly out of scope for v1

- Production-traffic ingestion, redaction, consent flows.
- Hosted product, dashboards, continuous drift monitoring, private benchmarks.
- Provider categories beyond models (search APIs, MCP tools, data, infra).
- Customer-defined axes beyond quality/latency/cost.
- Weight-level finetuning/RLHF (we reinforce the rubric/config, not model weights).

## 8. Build checklist

1. `litellm`-based model adapter + streaming latency/token capture.
2. Synthetic input generator (use-case YAML → editable inputs artifact).
3. Judge core: rubric schema, forced structured output, code-side aggregation, blinding.
4. Meta-eval: load `gold.yaml`, compute agreement / consistency / flip-rate / self-pref.
5. Report: ranked table (quality/latency/cost), drill-down traces, judge trust line,
   committable markdown + JSON.
6. Caching + provenance (pin model versions, timestamp, config hash).
7. Starter project + example rubric pack so it's runnable in minutes.
