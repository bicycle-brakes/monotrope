#!/usr/bin/env python3
"""check_bead_export.py — der gerenderte Export, Zeile fuer Zeile (bead bo0).

`check_bead_export.py` prueft das gerenderte Bild des Trackers Zeile fuer
Zeile. Den Stand bezieht es ueber den EINEN Zugriffspunkt (`bead_render.py`,
bead 1jg.3): in der CI das vorgesetzte Render, beim Schreiber ein frisches
Render, uebergangsweise die committete Kopie. Kein Mensch schreibt den
Export, aber jeder liest ihn: Tests zitieren Vorgangs-Status daraus, und
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


def run(pfad: Path) -> list[str]:
    """Prueft eine Export-Datei Zeile fuer Zeile. Liefert Befunde, leer = gruen."""
    if not pfad.is_file():
        return [f"Export fehlt: {pfad} — dann zitiert kein Test einen echten Stand"]
    befunde: list[str] = []
    saetze = 0
    for nr, zeile in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
        if not zeile.strip():
            continue
        saetze += 1
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
    if saetze == 0:
        # Bead coding-harness-4t8: ein Export ueber null Zeilen ist kein gruenes
        # Ergebnis — jeder Leser (Tests, dangling-beads, Handovers) zitiert eine
        # leere Wahrheit und merkt es nicht. Nichts messen ist hier ein Befund.
        befunde.append("der Export ist leer — ein Gate ueber null Zeilen misst nichts")
    return befunde


def main() -> int:
    from bead_render import render_pfad  # noqa: E402 — der EINE Zugriffspunkt (bead 1jg.3)

    quelle = render_pfad()
    befunde = run(quelle)
    if befunde:
        print(f"{len(befunde)} Befunde in {quelle}:")
        for b in befunde:
            print(f"  - {b}")
        return 1
    zeilen = sum(1 for z in quelle.read_text(encoding="utf-8").splitlines() if z.strip())
    print(f"Bead-Render ok: {zeilen} Zeilen, jede mit id und status.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
