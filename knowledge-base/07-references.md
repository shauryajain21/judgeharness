# 07 — References

## Primary inspiration

- Dario Amodei, **Machines of Loving Grace** (2024).
  https://darioamodei.com/machines-of-loving-grace
  - Key line: AI is "the first technology capable of making broad, fuzzy
    judgements in a repeatable and mechanical way."
  - Follow-up page: interpretability to "see inside the final model and assess it
    for hidden biases."

## Transformer Circuits Thread (https://transformer-circuits.pub/)

Reading order for this project:

1. **Verbalizable Representations Form a Global Workspace in Language Models**
   (Lindsey et al., Jul 6, 2026) — *the* paper for us. J-lens, workspace,
   eval-awareness, hidden-intent detection, counterfactual reflection training.
   https://transformer-circuits.pub/2026/workspace/index.html
2. **On the Biology of a Large Language Model** (Mar 2025) — attribution graphs
   applied; CoT faithfulness (genuine vs. bullshit vs. motivated), hidden goals,
   hallucination circuits.
   https://transformer-circuits.pub/2025/attribution-graphs/biology.html
3. **Circuit Tracing: Revealing Computational Graphs in Language Models**
   (Mar 2025) — the methods companion (CLT replacement model, attribution graphs).
   https://transformer-circuits.pub/2025/attribution-graphs/methods.html
4. **Scaling Monosemanticity** (May 2024) — SAEs at production scale; safety
   features (deception, sycophancy, bias); steering.
   https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html
5. **Towards Monosemanticity** (2023) — SAEs foundation, one-layer model.
   https://transformer-circuits.pub/2023/monosemantic-features/index.html
6. **Toy Models of Superposition** (2022) — why neurons are polysemantic.
   https://transformer-circuits.pub/2022/toy_model/index.html
7. **A Mathematical Framework for Transformer Circuits** (2021) & **In-context
   Learning and Induction Heads** (2022) — foundations.
   https://transformer-circuits.pub/2021/framework/index.html

## Tooling for the mechanistic (v2) tier

- **Neuronpedia** — J-lens readouts + SAE features on open-weight models.
  https://neuronpedia.org
- **TransformerLens** — activation access / patching for open models.
- **nnsight** — remote/local activation access.
- **litellm** — multi-provider API adapter (v1 behavioral tier).

## Concepts to read up on (methodology we borrow, not the data)

- Cohen's κ / Krippendorff's α — chance-corrected agreement.
- Expected Calibration Error (ECE) — confidence calibration.
- LLM-as-judge position bias & self-preference literature (e.g. MT-Bench,
  "LLMs are not fair evaluators", G-Eval) — prior art to cite & differentiate.
- Public benchmarks for the *sanity floor* only: SimpleQA, TruthfulQA, MMLU.
