#!/usr/bin/env python3
"""check_dangling_bead_ids.py — zitierte Vorgangs-IDs loesen im Export auf.

Die Provenanz-Kette lebt von Zaehlen, die man nachschlagen kann: Eine
Änderung nennt ihren Vorgang, ein Grund nennt seinen Besitzer. Zitiert ein
Artefakt eine ID, die der Export nicht kennt, ist die Kette gekappt — und
zwar still. Dieses Gate liest den Export und prueft jede Zitation im
Dokumentations- und Planungsbaum darauf.

Usage:
    python3 scripts/check_dangling_bead_ids.py
Exit: 0 = alle Zitationen loesen auf, 1 = haengende IDs.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"

# Der Praefix ist beim init fest vergeben und kann nicht korrigiert werden
# (AGENTS.md, Hausregel 3). Nur Zitationen dieses Praefixs werden geprueft —
# fremde Tracker-Praefixe sind nicht unsere Bilanz.
#
# Die IDs selbst sind kurze Suffixe OHNE Bindestrich (bo0, 2ee, 9qo). Der
# Negative-Lookahead verhindert, dass ein laengerer Bezeichner — etwa der
# Worktree-Name `coding-harness-omnigent-pr` — als Zitation gelesen wird.
PRAEFIX = "coding-harness-"
MUSTER = re.compile(r"\b" + re.escape(PRAEFIX) + r"([a-z0-9]{3,8})(?![a-z0-9.\-])")


def _bekannte_ids(export: Path) -> set[str]:
    if not export.is_file():
        return set()
    ids: set[str] = set()
    for zeile in export.read_text(encoding="utf-8").splitlines():
        if not zeile.strip():
            continue
        try:
            satz = json.loads(zeile)
        except json.JSONDecodeError:
            continue
        if isinstance(satz, dict) and isinstance(satz.get("id"), str):
            ids.add(satz["id"])
    return ids


def run(basis: Path, export: Path) -> list[str]:
    """Prueft alle Zitationen unter `basis` gegen den Export."""
    bekannt = _bekannte_ids(export)
    if not bekannt:
        return [f"der Export {export} nennt keine einzige ID — die Pruefung misst nichts"]
    befunde: list[str] = []
    dateien = sorted(basis.rglob("*.md"))
    for p in dateien:
        rel = p.relative_to(basis)
        text = p.read_text(encoding="utf-8")
        for treffer in MUSTER.finditer(text):
            voll = PRAEFIX + treffer.group(1)
            if voll not in bekannt:
                befunde.append(f"{rel}: haengende ID {voll} — im Export nicht bekannt")
    return befunde


def main() -> int:
    befunde = run(REPO_ROOT / "docs", EXPORT)
    if befunde:
        print(f"{len(befunde)} haengende Vorgangs-Zitationen:")
        for b in befunde:
            print(f"  - {b}")
        return 1
    print("Alle zitierten Vorgangs-IDs loesen im Export auf.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
