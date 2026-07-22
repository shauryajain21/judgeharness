"""Typed configuration + artifact schemas.

Everything the CLI reads/writes is a validated pydantic model, so malformed
configs fail loudly instead of silently producing garbage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator


# --------------------------------------------------------------------------- #
# Input configs (authored by the user)
# --------------------------------------------------------------------------- #
class UseCase(BaseModel):
    """What the user is building — the seed for synthetic input generation."""

    task: str
    user: str = ""
    inputs_to_synthesize: list[str] = Field(default_factory=list)
    volume: int = 20

    @field_validator("volume")
    @classmethod
    def _volume_sane(cls, v: int) -> int:
        if not 1 <= v <= 1000:
            raise ValueError("volume must be between 1 and 1000")
        return v


class Candidates(BaseModel):
    """The models to bake off + shared generation knobs (held constant)."""

    candidates: list[str]
    temperature: float = 0.0
    max_tokens: int = 512

    @field_validator("candidates")
    @classmethod
    def _non_empty(cls, v: list[str]) -> list[str]:
        if len(v) < 2:
            raise ValueError("need at least 2 candidate models to compare")
        return v


class Criterion(BaseModel):
    name: str
    weight: float
    guide: str = ""


class Rubric(BaseModel):
    """The judge's contract: how 'quality' is defined for this use case."""

    mode: Literal["score", "pairwise"] = "score"
    scale: int = 5
    criteria: list[Criterion]

    @field_validator("criteria")
    @classmethod
    def _weights(cls, v: list[Criterion]) -> list[Criterion]:
        if not v:
            raise ValueError("rubric needs at least one criterion")
        total = sum(c.weight for c in v)
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"criterion weights must sum to 1.0 (got {total:.3f})")
        return v


class GoldPair(BaseModel):
    """A human-labeled comparison used to validate the judge (meta-eval)."""

    input: str
    a: str
    b: str
    human: Literal["A", "B"]
    # optional provenance so we can measure self-preference
    a_model: str | None = None
    b_model: str | None = None


class Gold(BaseModel):
    pairs: list[GoldPair] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Generated artifacts
# --------------------------------------------------------------------------- #
class SynthInput(BaseModel):
    id: str
    text: str


class SynthInputs(BaseModel):
    usecase_task: str
    inputs: list[SynthInput]


# --------------------------------------------------------------------------- #
# YAML helpers
# --------------------------------------------------------------------------- #
def _read_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"missing config: {path}")
    with path.open() as f:
        return yaml.safe_load(f) or {}


def load_usecase(root: Path) -> UseCase:
    return UseCase(**_read_yaml(root / "usecase.yaml"))


def load_candidates(root: Path) -> Candidates:
    return Candidates(**_read_yaml(root / "candidates.yaml"))


def load_rubric(root: Path) -> Rubric:
    return Rubric(**_read_yaml(root / "rubric.yaml"))


def load_gold(root: Path) -> Gold:
    path = root / "gold.yaml"
    if not path.exists():
        return Gold()
    data = _read_yaml(path)
    # accept either {pairs: [...]} or a bare list
    if isinstance(data, list):
        data = {"pairs": data}
    return Gold(**data)


def load_synth_inputs(root: Path) -> SynthInputs:
    return SynthInputs(**_read_yaml(root / "inputs.yaml"))


def write_yaml(path: Path, model: BaseModel) -> None:
    with path.open("w") as f:
        yaml.safe_dump(model.model_dump(), f, sort_keys=False, allow_unicode=True)
