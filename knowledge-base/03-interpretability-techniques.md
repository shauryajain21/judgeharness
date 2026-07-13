# 03 — Interpretability techniques (Transformer Circuits)

Source: the Transformer Circuits Thread (https://transformer-circuits.pub/).
These are the techniques that underpin the **mechanistic (v2)** tier of trust.

## The critical access distinction

| Access | What you can do | Applies to |
|---|---|---|
| **Black-box / behavioral** | Perturb inputs, ablate rubric criteria, run N times, swap order, cross-generator tests | **Any model**, incl. GPT/Claude/Gemini APIs → **v1, ships now** |
| **White-box / mechanistic** | Read & steer internal features/activations (SAEs, attribution graphs, J-lens) | **Open-weight only** (Llama, Qwen, Gemma, GPT-OSS) → **v2, the moat** |

Key implication: an API judge's *written* reasoning is exactly the thing this
research shows you **cannot fully trust** (it can be post-hoc rationalization).
Mechanistic tools require weights/activations you only get on open models.

## Core concepts

### Superposition
Models represent **more concepts than they have neurons** by using
almost-orthogonal directions in high-dimensional space. Consequence: individual
neurons are **polysemantic** (fire for many unrelated things), so you can't read a
model by looking at raw neurons.
- Ref: *Toy Models of Superposition* (2022).

### Features (the unit of analysis)
Meaningful concepts are **linear directions** in activation space (the "linear
representation hypothesis"). A feature can be low-level ("the word capital") or
abstract ("code security vulnerability", "sycophancy", "deception").

### Sparse autoencoders (SAEs) / dictionary learning
Method to **decompose activations into monosemantic features**. Train an SAE
(encoder→sparse features→decoder→reconstruction) on model activations; each
learned feature ≈ one interpretable concept.
- *Scaling Monosemanticity* (2024): pulled millions of features from Claude 3
  Sonnet, incl. safety-relevant ones (deception, sycophancy, bias, dangerous
  content). Found a systematic frequency↔dictionary-size relationship.
- Ref: *Towards Monosemanticity* (2023), *Scaling Monosemanticity* (2024).

### Steering
Clamp a feature up/down → behavior changes predictably. The **causal test** that a
feature is real and functional (e.g. the "Golden Gate Bridge" steering demo).

### Attribution graphs / circuit tracing
Trace the **chain of internal steps** from prompt → output. Nodes = features,
edges = causal influence. Built on a **cross-layer transcoder (CLT)** "replacement
model" (30M features) that approximates the real model with interpretable parts;
**error nodes** track what's unexplained; attention patterns borrowed from the
real model → the "local replacement model."
- *Circuit Tracing* (2025, methods) + *On the Biology of a Large Language Model*
  (2025, applications).

### Intervention / ablation (validation)
Attribution graphs only give **hypotheses**. You validate by **inhibiting** a
feature group in the real model and checking the output changes as predicted.
Feature labels & groupings are fixed **before** measuring, to avoid hindsight bias.

## Findings from *Biology of an LLM* (2025) most relevant to judging

- **Multi-step reasoning in the head** — model computes Dallas → "Texas" →
  "Austin" internally; you can swap the "Texas" step and it outputs "Sacramento".
- **Forward + backward planning** — plans rhyming words before writing the line.
- **Entity recognition & hallucination** — a "known/unknown entity" circuit gates
  whether it answers or says "I don't know"; misfires → hallucination.
- **Chain-of-thought (un)faithfulness** ← **most important for judges.** They can
  distinguish: (a) genuine reasoning, (b) **bullshitting** (making up reasoning
  with no regard for truth), and (c) **motivated reasoning** (working backwards
  from a human-provided hint to justify a predetermined answer).
- **Hidden goals** — a model finetuned with a secret goal concealed it in text,
  but the goal was visible mechanistically, embedded in its "Assistant" persona.

## Why this matters for JudgeHarness

- The (b) and (c) CoT failure modes are **exactly** what a bad judge does: emit a
  plausible rationale that doesn't reflect the real decision, or rationalize a
  verdict it anchored on for the wrong reason (length, style, position, a hint).
- Behavioral checks (v1) can *detect the symptom* (verdict flips under
  perturbation). Mechanistic checks (v2) can *see the cause* (which feature drove
  it). Same question Anthropic asks: **is the reasoning faithful, or a story?**

## Limitations (honest)

- Attribution graphs gave "satisfying insight" for only ~25% of prompts tried.
- The replacement model is imperfect (error nodes exist); results are hypotheses
  requiring intervention to confirm.
- All white-box → open-weight only in the wild. Treat v2 as ambitious, not v1.
