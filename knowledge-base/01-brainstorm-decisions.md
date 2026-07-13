# 01 — Brainstorm decisions

Locked decisions from the brainstorm, plus open questions.

## Locked

| Decision | Choice | Rationale |
|---|---|---|
| Judging modes | **Both** pairwise (A/B) and absolute scoring | User does both roughly equally |
| Ground truth | **Domain calibration set** (20–50 examples), not public benchmarks | Public sets test the *model*, not *your judge on your task* |
| Artifact | **Brainstorm/spec first**, then OSS CLI | User wanted to think it through before building |
| Distribution | **Public / OSS** | "Maximize distribution someway" |
| Primary surface | **CLI + config files** | Most OSS-native, CI-friendly |
| Gold set creation | **Semi-auto bootstrap** — strong model drafts labels, human confirms | Kills the "labeling is boring → skip it → back to vibes" trap |
| Domains | **General-purpose harness, many rubric packs** | User judges code, text, agent, RAG — all of them |

## Key principle: harness generalizes, rubrics don't

- A single universal judge prompt across code+text+agent+RAG will be mediocre at all.
- What generalizes = the **harness** (calibration + meta-metrics loop).
- What stays domain-specific = the **rubric packs** (contributable via PR → distribution engine).

## Bootstrap labeling rule (trust-critical)

The model that **drafts** gold labels must be **different / stronger** than the
judge being tested. Otherwise you're grading a student with its own answer key.
The harness should enforce or at least warn on this.

## Anti-patterns to avoid (decided against)

- **No mid-verdict "nudging."** Letting a user steer the judge mid-reasoning just
  injects their bias. Iteration happens at **rubric-design** time; then you
  **freeze** the judge. A frozen judge is a trustworthy judge.
- **No silent garbage.** If schema validation fails, refuse to emit a verdict.
- **Speed is not the first priority.** Correctness of the rubric/gold loop first;
  optimize the harness for speed once the rubric is stable.

## Design principles (OSS-friendly)

- **Config in, report out.** No hidden state. A judge run = a file you can commit and diff.
- **Rubrics are data, not code.** YAML/JSON so people contribute packs via PR.
- **Bring-your-own-model.** Thin adapter layer; don't lock to one provider.
- **Everything reproducible.** Same config + seed → same report. This *is* the trust.

## Opinionated defaults (bake in)

- `temperature=0` + forced JSON schema (kills most flakiness).
- Auto A/B order swap + report `flip_rate` (kills position bias).
- Require per-criterion justification (kills opacity).
- Ship starter gold sets per domain (~20 each) to lower activation energy.
- Make the report a committable markdown file (people paste `agreement: 0.94` in
  READMEs → free marketing, normalizes citing a judge's trust score).

## Open questions

- Name: "JudgeHarness" is a working title — gut-check later.
- v2 mechanistic tier: which open-weight models to support first (Llama / Qwen /
  Gemma / GPT-OSS)? Neuronpedia integration for J-lens?
- Bootstrap: fully-auto with confidence threshold vs. always human-in-the-loop?
- Report format: markdown + JSON is decided; add an HTML/dashboard view later?
