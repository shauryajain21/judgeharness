# 05 — Technique → concrete judge check

The core mapping. Each interpretability idea → a concrete check JudgeHarness can
run, tagged by tier (behavioral = any API model; mechanistic = open-weight only).

## Tier 1 — Behavioral (black-box, ships first, works on any API judge)

These borrow the *spirit* of interpretability ("don't trust the story, test it
causally") without needing weights.

| Check | What it does | Detects | Inspired by |
|---|---|---|---|
| **Criterion ablation** | Drop one rubric criterion, re-judge. If verdict unchanged, that criterion was decorative. | Rubric theater / which criteria actually drive the verdict | Feature ablation |
| **Order swap** | Run each pair A/B and B/A; measure `flip_rate`. | Position bias | Intervention experiments |
| **Paraphrase invariance** | Re-judge semantically-identical paraphrases. | Style/surface sensitivity, brittleness | Counterfactual perturbation |
| **Authority injection** | Insert a fake cue ("an expert says A is correct"). Does verdict move? | Sycophancy / motivated reasoning | CoT "works backward from a hint" finding |
| **Cross-generator eval** | Judge outputs from multiple generators incl. the judge's own family. | Self-preference | "Self / sycophancy" feature |
| **Faithfulness gate** | Force per-criterion scores FIRST, then verdict; test if verdict is predictable from scores. | Post-hoc rationalization (unfaithful CoT) | CoT faithfulness (genuine vs. bullshit) |
| **Consistency-N** | Run N times; measure verdict agreement / score variance. | Flakiness | (baseline reliability) |
| **Known-entity probe** | Include items the judge shouldn't have an opinion on; does it fabricate one? | Hallucinated confidence | Entity-recognition / hallucination circuit |

## Tier 2 — Mechanistic (white-box, open-weight judges only, the moat)

Requires residual-stream access. Prototype with the **logit lens** (cheap), then
the **J-lens** (better in early layers), then SAE features / attribution graphs.

| Check | What it does | Detects | Technique |
|---|---|---|---|
| **Workspace verdict-agreement** | Read J-space at the verdict token; does the unspoken workspace agree with the written verdict? | Unfaithful verdict ("output vs. thought" gap) | J-lens read |
| **Eval-awareness probe** | Probe for `fake`/`fictional`/eval-awareness concepts while judging. Optionally ablate and re-judge. | Judge behaving differently because it knows it's tested (threatens your gold set!) | J-lens read + ablation |
| **Bias-feature monitor** | Probe for sycophancy / self-preference / bias features firing during the verdict. | Hidden bias not visible in text | SAE feature probe / J-lens |
| **Manipulation detection** | Probe for prompt-injection / "suspicious input" recognition when judging adversarial candidates. | Judge noticing (or missing) manipulation attempts | J-lens (paper showed injection flagging) |
| **Criterion-attribution** | Attribution graph from rubric-criterion features → verdict token. | Whether it actually weighed "correctness" vs. anchored on length/style | Attribution graphs |
| **Reasoning-step swap** | Identify an intermediate judgment feature; swap it; confirm verdict changes as predicted. | Whether stated reasoning is causal or decorative | Feature swap (Dallas→Texas→Austin style) |

## Tier 3 — Advanced / research (from counterfactual reflection training)

| Idea | Application to judges |
|---|---|
| **Reflective shaping** | Improve a judge's rubric-adherence by training/prompting its *reflective dispositions* ("if interrupted, what principle applies?"), not just its final verdict. Rigorous form of the user's original "influence the thinking" idea. |
| **Implant + verify** | Implant rubric principles into the workspace; verify by ablation that they causally drive better verdicts. |

## Product framing

> **Two tiers of judge trust.**
> **Behavioral** (black-box, any model, ships now) and **Mechanistic**
> (white-box, open-weight, the moat). Both answer Anthropic's question:
> *is the reasoning faithful, or is the model just telling me a nice story?*

Ship Tier 1 as the CLI MVP. Tier 2 is the differentiator that makes this "an
interpretability-grade judge harness," not "another eval tool." Start Tier 2 with
the **logit lens** (no special deps) before investing in full J-lens/SAE tooling.
