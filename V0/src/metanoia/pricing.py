"""Versioned, dated model pricing table (USD per 1M tokens).

Cost must be computed, not guessed. Prices drift — keep this dated and update it.
Unknown models fall back to a conservative default and are flagged.
"""

from __future__ import annotations

PRICING_AS_OF = "2026-07-22"

# name -> (input $/1M tokens, output $/1M tokens)
PRICING: dict[str, tuple[float, float]] = {
    "gpt-5": (5.00, 15.00),
    "gpt-5-mini": (0.60, 2.40),
    "claude-sonnet-4.5": (3.00, 15.00),
    "claude-haiku-4.5": (0.80, 4.00),
    "gemini-2.5-flash": (0.15, 0.60),
    "gemini-2.5-pro": (1.25, 10.00),
    "llama-4-70b": (0.30, 0.50),
    "deepseek-v3": (0.14, 0.28),
    # common OpenRouter / real model IDs (last path segment is matched too)
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "claude-3.5-haiku": (0.80, 4.00),
    "claude-3.5-sonnet": (3.00, 15.00),
    "gemini-flash-1.5": (0.075, 0.30),
    "llama-3.3-70b-instruct": (0.13, 0.40),
    "deepseek-chat": (0.14, 0.28),
    # mock/testing
    "mock-strong": (3.00, 15.00),
    "mock-mid": (0.60, 2.40),
    "mock-cheap": (0.15, 0.60),
}

_DEFAULT = (1.00, 3.00)


def _normalize(model: str) -> str:
    # "openrouter/openai/gpt-4o-mini" -> "gpt-4o-mini"
    return model.split("/")[-1]


def price_of(model: str) -> tuple[float, float]:
    if model in PRICING:
        return PRICING[model]
    return PRICING.get(_normalize(model), _DEFAULT)


def is_known(model: str) -> bool:
    return model in PRICING or _normalize(model) in PRICING


def cost_usd(model: str, in_tokens: int, out_tokens: int) -> float:
    pin, pout = price_of(model)
    return (in_tokens * pin + out_tokens * pout) / 1_000_000.0
