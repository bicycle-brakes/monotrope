"""This repository's own adoption day (ADR 0014).

The case asserts the day this repository adopted the gate, so it stays here:
no manifest rule lets it travel, and a repository that records its own day
keeps its own case.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import adoption  # noqa: E402


def test_this_repository_adopted_the_gate_on_2026_10_08() -> None:
    assert adoption.adopted_on(REPO_ROOT, "interview-minimums") == date(2026, 10, 8)
