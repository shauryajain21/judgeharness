"""Content-addressed cache: never re-pay for a call already made.

Keyed by a hash of (kind, model, prompt, config), so reruns are free and
reproducible. Stored as JSON under runs/cache/.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class Cache:
    def __init__(self, root: Path):
        self.dir = root / "runs" / "cache"
        self.dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def key(*parts: Any) -> str:
        blob = json.dumps(parts, sort_keys=True, default=str)
        return hashlib.sha256(blob.encode()).hexdigest()[:24]

    def get(self, key: str) -> dict | None:
        p = self.dir / f"{key}.json"
        if p.exists():
            return json.loads(p.read_text())
        return None

    def put(self, key: str, value: dict) -> None:
        (self.dir / f"{key}.json").write_text(json.dumps(value, indent=2))
