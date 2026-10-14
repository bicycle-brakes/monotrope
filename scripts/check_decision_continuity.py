#!/usr/bin/env python3
"""check_decision_continuity.py — a decision disappears only visibly.

On 2026-09-17 the first draft of the new target was lost: LikeC4 and parts of
the interview were missing, and nothing turned red (gap analysis, P1). This
gate turns that into a machine: the current target file must carry EVERY
decided ID of the interviews (D-1..D-17, O-1..O-4) in its decision-continuity
table, and every AMENDMENT claim needs its ADR file that names it.

A missing ID or ADR is a finding — not a state. If the target document itself
is missing, the gate is NOT MEASURED and fails (exit 3): it is set to
floor: true, and a floor gate that does not measure is red
(bead coding-harness-4t8).

Usage:
    python3 scripts/check_decision_continuity.py
Exit: 0 = chain complete, 1 = findings, 3 = target document missing (not measured).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "docs" / "architecture" / "2026-09-17-omnigent-first-target.md"
ADR_DIR = REPO_ROOT / "docs" / "adr"

# The 21 interview decisions of 2026-09-16 — a historical stock, not
# derivable. A new decision extends these tuples visibly.
EXPECTED_D = tuple(f"D-{i}" for i in range(1, 18))
EXPECTED_O = tuple(f"O-{i}" for i in range(1, 5))

# Every AMENDMENT claim of the target needs exactly these ADR files, and
# every ADR names the IDs it speaks for. This mapping is the map; whoever
# changes it changes a responsibility.
AMENDMENT_ADRS: dict[str, tuple[str, ...]] = {
    "D-3": ("0001-early-parallelism.md", "0006-parallel-work-without-a-pilot.md"),
    "D-7": (
        "0001-early-parallelism.md",
        "0006-parallel-work-without-a-pilot.md",
        "0010-hermes-first-unattended-writing-agent.md",
    ),
    "D-4": ("0004-tracker-render-is-the-contract.md",),
    "D-13": ("0007-stage-2-reviews-by-codex-and-glm.md",),
    "D-17": ("0003-public-scan-naming-boundary.md",),
    "D-15": ("0009-architecture-delta-in-design-md.md",),
    "O-3": ("0009-architecture-delta-in-design-md.md",),
    "coordinator-permission": (
        "0002-exclusive-coordinator-writer.md",
        "0005-workers-claim-their-own-bead.md",
        "0006-parallel-work-without-a-pilot.md",
    ),
}


def run(target: Path, adr_dir: Path = ADR_DIR) -> list[str]:
    """Checks continuity and ADR coverage. Returns findings; empty = green."""
    befunde: list[str] = []
    if not target.is_file():
        return [f"Target file missing: {target}"]
    text = target.read_text(encoding="utf-8")

    stueck = re.split(r"^## Decision continuity\s*$", text, maxsplit=1, flags=re.M)
    if len(stueck) < 2:
        return [f"{target.name}: no 'Decision continuity' section"]
    tabelle = stueck[1].split("\n## ", 1)[0]

    for sid in (*EXPECTED_D, *EXPECTED_O):
        if not re.search(rf"\b{re.escape(sid)}\b", tabelle):
            befunde.append(f"{target.name}: Decision {sid} missing from the continuity table")

    for schluessel, adrs in AMENDMENT_ADRS.items():
        for adr in adrs:
            pfad = adr_dir / adr
            if not pfad.is_file():
                befunde.append(f"ADR missing: docs/adr/{adr} (for {schluessel})")
                continue
            inhalt = pfad.read_text(encoding="utf-8")
            zitieren = [s for s in (schluessel,) if s.startswith(("D-", "O-"))] + (
                ["coordinator"] if schluessel == "coordinator-permission" else []
            )
            for z in zitieren:
                if not re.search(rf"\b{re.escape(z)}\b", inhalt):
                    befunde.append(f"docs/adr/{adr}: does not name '{z}' — the mapping is empty")
    return befunde


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=Path, default=TARGET, help="the current target file")
    args = ap.parse_args()
    if not args.target.is_file():
        # Bead coding-harness-4t8: floor: true means — not measuring is red.
        # The old text ("still lives in docs PR #8, becomes active after the
        # merge") has been outdated since the #8 merge (2026-09-22); a missing
        # target is a state that fails the run, not one that lets it pass.
        # "NICHT GEMESSEN" stays as the shared gate-status marker (also printed
        # by bead_render.py, asserted by tests).
        print(
            f"decision-continuity NICHT GEMESSEN (not measured): {args.target.name} is missing — the "
            "decision-continuity table is unreadable. floor: true: not "
            "measuring is red for this gate (bead 4t8)."
        )
        return 3
    befunde = run(args.target)
    if befunde:
        print(f"{len(befunde)} findings:")
        for b in befunde:
            print(f"  - {b}")
        return 1
    print(f"Decision continuity ok: all {len(EXPECTED_D) + len(EXPECTED_O)} IDs mapped, all amendment ADRs present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
