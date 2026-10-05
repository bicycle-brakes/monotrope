#!/usr/bin/env python3
"""check_decision_continuity.py — eine Entscheidung verschwindet nur sichtbar.

Am 2026-09-17 ging der erste Entwurf des neuen Ziels verloren: LikeC4 und
Teile des Interviews fehlten, und nichts wurde rot (Gap-Analyse, P1). Dieses
Gate macht daraus eine Maschine: Die aktuelle Ziel-Datei muss JEDE entschiedene
ID der Interviews (D-1..D-17, O-1..O-4) in ihrer Decision-Continuity-Tabelle
fuehren, und jede AMENDMENT-Behauptung braucht ihre ADR-Datei, die sie nennt.

Fehlt eine ID oder eine ADR, ist das ein Befund — kein Zustand. Fehlt das
Zieldokument selbst, ist der Gate NICHT GEMESSEN und faellt (Exit 3): er
steht auf floor: true, und ein floor-Gate, das nicht misst, ist rot
(bead coding-harness-4t8).

Usage:
    python3 scripts/check_decision_continuity.py
Exit: 0 = Kette ganz, 1 = Befunde, 3 = Zieldokument fehlt (nicht gemessen).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "docs" / "architecture" / "2026-09-17-omnigent-first-target.md"
ADR_DIR = REPO_ROOT / "docs" / "adr"

# Die 21 Interview-Entscheidungen des 2026-09-16 — ein historischer Bestand,
# nicht ableitbar. Eine neue Entscheidung erweitert diese Tupel sichtbar.
EXPECTED_D = tuple(f"D-{i}" for i in range(1, 18))
EXPECTED_O = tuple(f"O-{i}" for i in range(1, 5))

# Jede AMENDMENT-Behauptung des Ziels braucht genau diese ADR-Dateien, und
# jede ADR nennt die IDs, fuer die sie spricht. Diese Zuordnung ist die Karte;
# wer sie aendert, aendert eine Verantwortung.
AMENDMENT_ADRS: dict[str, tuple[str, ...]] = {
    "D-3": ("0001-early-parallelism.md", "0006-parallel-work-without-a-pilot.md"),
    "D-7": (
        "0001-early-parallelism.md",
        "0006-parallel-work-without-a-pilot.md",
        "0010-hermes-first-unattended-writing-agent.md",
    ),
    "D-4": ("0004-tracker-render-is-the-contract.md",),
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
    """Prueft Kontinuitaet und ADR-Abdeckung. Liefert Befunde, leer = gruen."""
    befunde: list[str] = []
    if not target.is_file():
        return [f"Ziel-Datei fehlt: {target}"]
    text = target.read_text(encoding="utf-8")

    stueck = re.split(r"^## Decision continuity\s*$", text, maxsplit=1, flags=re.M)
    if len(stueck) < 2:
        return [f"{target.name}: keine Sektion 'Decision continuity'"]
    tabelle = stueck[1].split("\n## ", 1)[0]

    for sid in (*EXPECTED_D, *EXPECTED_O):
        if not re.search(rf"\b{re.escape(sid)}\b", tabelle):
            befunde.append(f"{target.name}: Decision {sid} fehlt in der Continuity-Tabelle")

    for schluessel, adrs in AMENDMENT_ADRS.items():
        for adr in adrs:
            pfad = adr_dir / adr
            if not pfad.is_file():
                befunde.append(f"ADR fehlt: docs/adr/{adr} (fuer {schluessel})")
                continue
            inhalt = pfad.read_text(encoding="utf-8")
            zitieren = [s for s in (schluessel,) if s.startswith(("D-", "O-"))] + (
                ["coordinator"] if schluessel == "coordinator-permission" else []
            )
            for z in zitieren:
                if not re.search(rf"\b{re.escape(z)}\b", inhalt):
                    befunde.append(f"docs/adr/{adr}: nennt '{z}' nicht — die Zuordnung ist leer")
    return befunde


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=Path, default=TARGET, help="die aktuelle Ziel-Datei")
    args = ap.parse_args()
    if not args.target.is_file():
        # Bead coding-harness-4t8: floor: true heisst — nicht messen ist rot.
        # Der alte Text ("lebt noch im Docs-PR #8, wird nach dem Merge scharf")
        # ist seit dem #8-Merge (2026-09-22) ueberholt; ein fehlendes Ziel ist
        # ein Zustand, der den Lauf faellt, keiner, der ihn gruen laesst.
        print(
            f"decision-continuity NICHT GEMESSEN: {args.target.name} fehlt — die "
            "Decision-Continuity-Tabelle ist nicht lesbar. floor: true: nicht "
            "messen ist fuer diesen Gate rot (bead 4t8)."
        )
        return 3
    befunde = run(args.target)
    if befunde:
        print(f"{len(befunde)} Befunde:")
        for b in befunde:
            print(f"  - {b}")
        return 1
    print(
        f"Decision-Continuity ok: alle {len(EXPECTED_D) + len(EXPECTED_O)} IDs gemappt, alle Amendment-ADRs vorhanden."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
