#!/usr/bin/env python3
"""check_bead_export.py — der gerenderte Export, Zeile fuer Zeile (bead bo0).

`.beads/issues.jsonl` ist das gerenderte Bild des Trackers — kein Mensch
schreibt es, aber jeder liest es: Tests zitieren Vorgangs-Status daraus, und
ein kaputtes Bild liest sich als Wahrheit. Deshalb Zeilenpruefung statt
Vertrauen: jede Zeile JSON, jedes Objekt mit id und status.

Usage:
    python3 scripts/check_bead_export.py
Exit: 0 = gruen, 1 = Befunde.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"


def run(pfad: Path) -> list[str]:
    """Prueft eine Export-Datei Zeile fuer Zeile. Liefert Befunde, leer = gruen."""
    if not pfad.is_file():
        return [f"Export fehlt: {pfad} — dann zitiert kein Test einen echten Stand"]
    befunde: list[str] = []
    for nr, zeile in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
        if not zeile.strip():
            continue
        try:
            satz = json.loads(zeile)
        except json.JSONDecodeError as exc:
            befunde.append(f"Zeile {nr}: kein JSON ({exc})")
            continue
        if not isinstance(satz, dict):
            befunde.append(f"Zeile {nr}: kein Objekt")
            continue
        if not isinstance(satz.get("id"), str) or not satz["id"]:
            befunde.append(f"Zeile {nr}: ohne id")
        if not isinstance(satz.get("status"), str) or not satz["status"]:
            befunde.append(f"Zeile {nr}: ohne status")
    return befunde


def main() -> int:
    befunde = run(EXPORT)
    if befunde:
        print(f"{len(befunde)} Befunde in {EXPORT.relative_to(REPO_ROOT)}:")
        for b in befunde:
            print(f"  - {b}")
        return 1
    zeilen = sum(1 for z in EXPORT.read_text(encoding="utf-8").splitlines() if z.strip())
    print(f"Bead-Export ok: {zeilen} Zeilen, jede mit id und status.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
