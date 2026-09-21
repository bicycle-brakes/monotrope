#!/usr/bin/env python3
"""check_docs.py — Frontmatter, Links und Anker der Dokumentation (bead bo0).

Der Ablauf lebt in Markdown. Ein gebrochener Anker trennt eine Anweisung
stumm von ihrem Leser — deshalb wird geprueft statt vertraut:

  * YAML-Frontmatter, wenn vorhanden: die Kernschluessel muessen stehen
  * lokale Links: das Ziel muss existieren
  * Anker: das Ziel-Dokument muss die Ueberschrift tragen
  * Sprungmarken im selben Dokument genauso

Usage:
    python3 scripts/check_docs.py                 # docs/ rekursiv
    python3 scripts/check_docs.py --base docs/architecture
Exit: 0 = gruen, 1 = Befunde.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Wenn eine Datei Frontmatter traegt, muessen diese Schluessel stehen.
PFlicht: tuple[str, ...] = (
    "title",
    "category",
    "status",
    "created",
    "last_reviewed",
    "owner",
    "provenance",
    "produced_by",
    "review",
    "tags",
)


def _anker(ueberschrift: str) -> str:
    """GitHub-Anker einer Ueberschrift — die Form, in der Links sie zitieren."""
    a = ueberschrift.strip().lower()
    a = re.sub(r"[^a-z0-9 -]", "", a)
    return a.replace(" ", "-")


def run(basis: Path) -> list[str]:
    """Prueft alle *.md unter `basis`. Liefert Befunde, leer = gruen."""
    befunde: list[str] = []
    dateien = sorted(basis.rglob("*.md"))
    if not dateien:
        return [f"keine Markdown-Dateien unter {basis} — die Pruefung misst nichts"]
    for p in dateien:
        text = p.read_text(encoding="utf-8")
        rel = p.relative_to(basis)
        kopf = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if kopf:
            fm = kopf.group(1)
            for schluessel in PFlicht:
                if not re.search(rf"^{re.escape(schluessel)}:", fm, re.M):
                    befunde.append(f"{rel}: Frontmatter ohne '{schluessel}'")
        ueberschriften = re.findall(r"^#{1,6}\s+(.*)$", text, re.M)
        anker = {_anker(u) for u in ueberschriften}
        for ziel, sprungmarke in re.findall(r"\]\(([^)#]+?)(#[^)]+)?\)", text):
            if ziel.startswith(("http://", "https://", "mailto:")):
                continue
            zp = (p.parent / ziel).resolve()
            if not zp.exists():
                befunde.append(f"{rel}: toter Link {ziel}")
            elif sprungmarke:
                fa = sprungmarke[1:]
                tt = zp.read_text(encoding="utf-8")
                ta = {_anker(u) for u in re.findall(r"^#{1,6}\s+(.*)$", tt, re.M)}
                if fa not in ta:
                    befunde.append(f"{rel}: toter Anker {ziel}{sprungmarke}")
        for sprungmarke in re.findall(r"\]\(#([^)]+)\)", text):
            if sprungmarke not in anker:
                befunde.append(f"{rel}: tote Sprungmarke #{sprungmarke}")
    return befunde


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", type=Path, default=REPO_ROOT / "docs", help="Wurzel der Pruefung")
    args = ap.parse_args()
    befunde = run(args.base)
    if befunde:
        print(f"{len(befunde)} Befunde unter {args.base}:")
        for b in befunde:
            print(f"  - {b}")
        return 1
    print(f"Docs ok: alle Links, Anker und Frontmatter-Schluessel unter {args.base} geloest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
