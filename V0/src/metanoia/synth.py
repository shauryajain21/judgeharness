"""Synthetic input generation (cold-start mode).

Turns a use-case description into realistic task instances. The output is a
visible, editable artifact (inputs.yaml) so a human can prune/adjust before
spending money on a sweep — the synthesizer is a quiet source of bias.
"""

from __future__ import annotations

import json
import os

from .config import SynthInput, SynthInputs, UseCase
from .providers import complete


def _mock_synth(uc: UseCase) -> list[SynthInput]:
    comps = uc.inputs_to_synthesize or ["a representative input"]
    out: list[SynthInput] = []
    for i in range(uc.volume):
        parts = [f"{c} (variant {i + 1})" for c in comps]
        text = f"TASK: {uc.task}\n" + "\n".join(f"- {p}" for p in parts)
        out.append(SynthInput(id=f"q{i + 1:03d}", text=text))
    return out


def _live_synth(uc: UseCase) -> list[SynthInput]:
    prompt = (
        "You generate realistic, diverse evaluation inputs for testing AI models.\n"
        f"Task the models will perform: {uc.task}\n"
        f"Target user/persona: {uc.user}\n"
        f"Each input should include: {', '.join(uc.inputs_to_synthesize)}\n"
        f"Generate exactly {uc.volume} varied inputs. Return a JSON array of strings, "
        "each a complete, self-contained input scenario. JSON only."
    )
    # Use a strong model as the generator (different from candidates ideally).
    gen_model = os.environ.get("METANOIA_SYNTH_MODEL", "gpt-5")
    resp = complete(gen_model, prompt, temperature=0.8, max_tokens=4000, mock=False)
    try:
        arr = json.loads(resp.text)
    except json.JSONDecodeError:
        # tolerate models that wrap JSON in prose/fences
        s, e = resp.text.find("["), resp.text.rfind("]")
        arr = json.loads(resp.text[s : e + 1]) if s != -1 and e != -1 else []
    return [
        SynthInput(id=f"q{i + 1:03d}", text=str(t))
        for i, t in enumerate(arr[: uc.volume])
    ]


def synthesize(uc: UseCase, *, mock: bool | None = None) -> SynthInputs:
    if mock is None:
        mock = os.environ.get("METANOIA_MOCK", "1") == "1"
    inputs = _mock_synth(uc) if mock else _live_synth(uc)
    return SynthInputs(usecase_task=uc.task, inputs=inputs)
