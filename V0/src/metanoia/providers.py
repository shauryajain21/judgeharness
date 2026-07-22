"""Model adapter layer.

One canonical interface (`complete`) over many providers. Mock mode makes the
whole pipeline runnable offline (no keys) with deterministic, realistic-looking
outputs so we can test the machinery. Live mode uses litellm.
"""

from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass

from .pricing import cost_usd


@dataclass
class Completion:
    model: str
    text: str
    in_tokens: int
    out_tokens: int
    ttft_ms: float
    total_ms: float
    cost_usd: float
    error: str | None = None


def _seed(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return int(h[:12], 16)


# --------------------------------------------------------------------------- #
# Mock "skill" profiles — let different models rank differently in tests.
# quality_bias nudges the mock judge; speed/verbosity shape latency & tokens.
# --------------------------------------------------------------------------- #
_MOCK_PROFILES: dict[str, dict[str, float]] = {
    "gpt-5": {"quality": 0.92, "speed": 0.55, "verbosity": 1.15},
    "claude-sonnet-4.5": {"quality": 0.94, "speed": 0.60, "verbosity": 1.05},
    "gpt-5-mini": {"quality": 0.84, "speed": 0.80, "verbosity": 0.95},
    "gemini-2.5-flash": {"quality": 0.80, "speed": 0.95, "verbosity": 0.85},
    "llama-4-70b": {"quality": 0.74, "speed": 0.50, "verbosity": 1.10},
    "deepseek-v3": {"quality": 0.70, "speed": 0.45, "verbosity": 1.20},
    "mock-strong": {"quality": 0.93, "speed": 0.6, "verbosity": 1.0},
    "mock-mid": {"quality": 0.82, "speed": 0.8, "verbosity": 0.95},
    "mock-cheap": {"quality": 0.75, "speed": 0.95, "verbosity": 0.85},
}


def mock_profile(model: str) -> dict[str, float]:
    return _MOCK_PROFILES.get(model, {"quality": 0.72, "speed": 0.6, "verbosity": 1.0})


def _mock_complete(model: str, prompt: str, max_tokens: int) -> Completion:
    prof = mock_profile(model)
    rnd = _seed(model, prompt)
    jitter = (rnd % 1000) / 1000.0

    in_tokens = max(12, len(prompt) // 4)
    out_tokens = int(min(max_tokens, 60 + prof["verbosity"] * 120 + jitter * 40))

    # latency: faster models -> lower; a little input-dependent jitter
    base = 1600 * (1.1 - prof["speed"])
    total_ms = base + jitter * 400 + in_tokens * 0.6
    ttft_ms = total_ms * (0.25 + jitter * 0.1)

    text = (
        f"[{model}] draft response to: {prompt[:80].strip()}...\n"
        f"(mock output — quality≈{prof['quality']:.2f}, {out_tokens} tok)"
    )
    return Completion(
        model=model,
        text=text,
        in_tokens=in_tokens,
        out_tokens=out_tokens,
        ttft_ms=round(ttft_ms, 1),
        total_ms=round(total_ms, 1),
        cost_usd=cost_usd(model, in_tokens, out_tokens),
    )


def _live_complete(model: str, prompt: str, temperature: float, max_tokens: int) -> Completion:
    try:
        import litellm  # lazy import; only needed in live mode
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "live mode needs litellm — install with: pip install 'metanoia[live]'"
        ) from e

    litellm.drop_params = True  # tolerate provider-specific unsupported params
    t0 = time.perf_counter()
    try:
        resp = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=60,
            num_retries=0,  # fail fast → error row, no slow backoff on bad IDs
        )
    except Exception as e:  # normalize vendor errors into data, not crashes
        dt = (time.perf_counter() - t0) * 1000
        return Completion(model, "", 0, 0, 0.0, round(dt, 1), 0.0, error=str(e)[:200])

    total_ms = (time.perf_counter() - t0) * 1000
    text = resp.choices[0].message.content or ""
    usage = getattr(resp, "usage", None)
    in_tok = getattr(usage, "prompt_tokens", 0) or 0
    out_tok = getattr(usage, "completion_tokens", 0) or 0
    # Prefer litellm's own cost calc (knows OpenRouter/provider pricing); fall back
    # to our local table for models it doesn't recognize.
    try:
        cost = float(litellm.completion_cost(completion_response=resp))
    except Exception:
        cost = cost_usd(model, in_tok, out_tok)
    return Completion(
        model=model,
        text=text,
        in_tokens=in_tok,
        out_tokens=out_tok,
        ttft_ms=round(total_ms, 1),  # non-streaming: TTFT≈total
        total_ms=round(total_ms, 1),
        cost_usd=round(cost, 6),
    )


def complete(
    model: str,
    prompt: str,
    *,
    temperature: float = 0.0,
    max_tokens: int = 512,
    mock: bool | None = None,
) -> Completion:
    """Generate one completion under the canonical interface."""
    if mock is None:
        mock = os.environ.get("METANOIA_MOCK", "1") == "1"
    if mock:
        return _mock_complete(model, prompt, max_tokens)
    return _live_complete(model, prompt, temperature, max_tokens)
