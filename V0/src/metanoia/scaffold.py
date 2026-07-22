"""Project scaffolding — writes a runnable starter project (support-drafter
example) so a new user can `metanoia run` in seconds."""

from __future__ import annotations

from pathlib import Path

USECASE = """\
task: Draft a support reply from a customer ticket and a knowledge-base snippet.
user: SaaS support team, friendly-but-concise tone
inputs_to_synthesize:
  - a customer ticket (varying anger, clarity, topic)
  - one or two relevant knowledge-base snippets
volume: 12
"""

CANDIDATES = """\
candidates:
  - gpt-5
  - gpt-5-mini
  - claude-sonnet-4.5
  - gemini-2.5-flash
  - llama-4-70b
  - deepseek-v3
temperature: 0.0
max_tokens: 400
"""

RUBRIC = """\
mode: score
scale: 5
criteria:
  - name: correctness
    weight: 0.35
    guide: Reply matches the knowledge base; no invented policy.
  - name: tone
    weight: 0.25
    guide: Friendly, concise, on-brand.
  - name: resolution
    weight: 0.25
    guide: Actually resolves or advances the ticket.
  - name: safety
    weight: 0.15
    guide: No over-promising, no leaking internal notes.
"""

# A tiny human-labeled set to validate the judge. The last pair is a genuine
# "trick": the human prefers the output from the weaker model, so a good judge
# should NOT hit 100% agreement — realistic meta-eval.
GOLD = """\
pairs:
  - input: "Ticket: I was double charged this month. KB: refunds issued within 5 business days."
    a: "You were double charged — I've flagged it and a refund will arrive within 5 business days. Sorry for the hassle!"
    b: "Charges are usually correct. Please check your bank."
    human: A
    a_model: claude-sonnet-4.5
    b_model: deepseek-v3
  - input: "Ticket: How do I export my data? KB: Settings > Export > CSV."
    a: "Go to Settings > Export and choose CSV. Let me know if you hit any snags!"
    b: "You can probably find it somewhere in settings."
    human: A
    a_model: gpt-5
    b_model: llama-4-70b
  - input: "Ticket: Your product is terrible and I want a refund now. KB: refunds within 5 business days."
    a: "I hear you, and I'm sorry. I've started your refund — it lands within 5 business days."
    b: "I completely understand your frustration, and you deserve better. I've initiated your full refund right away; it will arrive within 5 business days. If there's anything else I can make right, tell me."
    human: B
    a_model: gpt-5-mini
    b_model: claude-sonnet-4.5
  - input: "Ticket: Can I change my plan mid-cycle? KB: plan changes prorate automatically."
    a: "Yes! Change it any time under Billing — we prorate the difference automatically."
    b: "Plans can be changed. It prorates."
    human: A
    a_model: gemini-2.5-flash
    b_model: llama-4-70b
  - input: "Ticket: Is my data encrypted? KB: AES-256 at rest, TLS 1.3 in transit."
    a: "Short answer: yes. Data is encrypted with AES-256 at rest and TLS 1.3 in transit."
    b: "We take security seriously and your data is encrypted end to end with bank-level security across everything we do, so you never have to worry."
    human: A
    a_model: gpt-5-mini
    b_model: claude-sonnet-4.5
"""

README = """\
# Metanoia project

Run the whole pipeline (mock mode, no API keys needed):

    metanoia run

Or step by step:

    metanoia synth        # generate inputs.yaml (edit it before sweeping!)
    metanoia sweep        # fan across models, judge blinded
    metanoia report       # ranked recommendation + judge trust

Go live with real models (needs `pip install 'metanoia[live]'` + provider keys):

    metanoia run --live

Files:
- usecase.yaml   — what you're building (seed for synthetic inputs)
- candidates.yaml— models to bake off + shared knobs
- rubric.yaml    — how "quality" is defined (the judge's contract)
- gold.yaml      — human-labeled pairs to validate the judge (meta-eval)
- inputs.yaml    — generated inputs (editable artifact)
- report.md/json — the deliverable
"""


def scaffold(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "usecase.yaml").write_text(USECASE)
    (root / "candidates.yaml").write_text(CANDIDATES)
    (root / "rubric.yaml").write_text(RUBRIC)
    (root / "gold.yaml").write_text(GOLD)
    (root / "README.md").write_text(README)
