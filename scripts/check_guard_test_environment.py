#!/usr/bin/env python3
"""check_guard_test_environment.py — the verification environment carries no planting switch.

A guard test plants its real fault only under `STAGE2_PLANT_FAULT=1`, and the
repair runner sets that switch itself, in the planted proof run alone (ADR 0023).
Verification must never run with the switch present, whatever its value: a
green suite under it counts planted faults as passing proof, and a planted
value would make the guard proofs' clean leg lie. This gate is part of both
verification paths — the local `make verify` and the hosted CI job — and is
registered in `decisions/gates.yaml` as `guard-test-environment`.

The gate names the variable and nothing else: it never prints the environment
or the value it found, so a value cannot smuggle content into a log.

Usage:
    python3 scripts/check_guard_test_environment.py
Exit: 0 = the switch is absent, 1 = the switch is present.
"""

from __future__ import annotations

import os
import sys
from typing import Any

SWITCH = "STAGE2_PLANT_FAULT"
GATE = "guard-test-environment"


def run(environ: dict[str, str] | None = None, out: Any = print) -> int:
    """Exit 1 while `SWITCH` is present under any name-binding, even empty or `0`."""
    names = os.environ if environ is None else environ
    if SWITCH in names:
        out(
            f"{GATE}: {SWITCH} is present in the verification environment; a guard test's planted fault must not run here"
        )
        return 1
    out(f"{GATE}: {SWITCH} is absent; verification runs without planted faults")
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    sys.exit(main())
