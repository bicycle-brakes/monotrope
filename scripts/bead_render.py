#!/usr/bin/env python3
"""bead_render.py — der EINE Zugriffspunkt fuers Tracker-Render (bead 1jg.3).

D-52 (lakeswitch-ai PR #37) hat den Vertrag gesetzt, ADR 0004 (proposed)
bestaetigt die Richtung: Der Render ist der tragende Vertrag, die committete
Kopie ist uebergangsweise. Wer den Tracker-Stand braucht, fragt HIER — nicht
`.beads/issues.jsonl` direkt und nicht `bd` selbst. Das ist die dritte
Bedingung des D-52-Beschlusses: jeder Leser auf einem Zugriffspunkt; erst
wenn sie steht, faellt die Kopie.

Die Reihenfolge, in der dieser Zugriffspunkt aufloest:

  1. `BEAD_RENDER` — die gehostete CI rendert EINMAL (nach der Hydratation)
     und setzt diesen Pfad; alle Leser des Laufs nehmen genau dieses Render.
  2. ein frisches Render ueber `tools/bd` — einmal pro Prozess, dann
     gecached. `render_beads_export.py` bleibt der Eine-Schreiber-Renderer;
     dieser Zugriffspunkt ist kein zweiter Renderer, er importiert ihn.
  3. die committete Kopie — UEBERGANGSWEISE (D-52), solange sie existiert:
     die Leerprobe und Umgebungen ohne ausfuehrbaren Renderer koennen nicht
     frisch messen; sie lesen den Stand, den der letzte Sitzungsschluss
     hinterlassen hat. Ihr Wegfallen ist der zweite Schritt dieses Beads —
     dann setzt die CI `BEAD_RENDER`, und nur Klone mit bootstrap bleiben
     lesefaehig.

Usage:
    python3 scripts/bead_render.py     # Pfad + Quelle auf stdout
Exit: 0 = Pfad geliefert, 2 = keiner (weder Render noch Kopie).
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

UMGEBUNGS_RENDER = "BEAD_RENDER"
QUELLE_VORGESETZT = "vorgesetzt"
QUELLE_GERENDERT = "gerendert"
QUELLE_COMMITTET = "committet"

_HALTER: tempfile.TemporaryDirectory | None = None
_GERENDERT: Path | None = None


class RendererNichtMoeglich(RuntimeError):
    """Diese Umgebung kann nicht frisch messen — kein Renderer, kein Store."""


def _frisches_render() -> Path:
    """Rendert einmal pro Prozess ueber den Eine-Schreiber-Renderer."""
    global _HALTER, _GERENDERT
    if _GERENDERT is None:
        _HALTER = tempfile.TemporaryDirectory(prefix="bead-render-")
        ziel = Path(_HALTER.name) / "issues.jsonl"
        from render_beads_export import _render_nach  # noqa: E402 — kein zweiter Renderer

        try:
            _render_nach(ziel)
        except SystemExit as exc:
            # _render_nach meldet Vorbedingungen jenseits des fehlenden Binary
            # als SystemExit(2) — derselbe Befund, nur eine andere Schelle.
            if exc.code != 2:
                raise
            _HALTER.cleanup()
            _HALTER, _GERENDERT = None, None
            raise RendererNichtMoeglich("der Renderer verweigert in dieser Umgebung") from None
        _GERENDERT = ziel
    return _GERENDERT


def render_pfad() -> Path:
    """Der Pfad, den ALLE Leser dieses Laufs nehmen. Wirft, wenn nichts misst."""
    vorgesetzt = os.environ.get(UMGEBUNGS_RENDER, "").strip()
    if vorgesetzt:
        pfad = Path(vorgesetzt)
        if not pfad.is_file():
            raise FileNotFoundError(
                f"{UMGEBUNGS_RENDER} zeigt auf {pfad}, die Datei fehlt — ein "
                "angesetztes Render, das verschwunden ist, ist ein Setupfehler, "
                "kein Grund zur stillen Rueckfallebene."
            )
        return pfad
    try:
        return _frisches_render()
    except RendererNichtMoeglich:
        kopie = REPO_ROOT / ".beads" / "issues.jsonl"
        if kopie.is_file():
            return kopie
        raise


def quelle(pfad: Path) -> str:
    """Nur fuer den Bericht: woher der gelieferte Pfad stammt."""
    if os.environ.get(UMGEBUNGS_RENDER, "").strip() == str(pfad):
        return QUELLE_VORGESETZT
    if _GERENDERT is not None and pfad == _GERENDERT:
        return QUELLE_GERENDERT
    return QUELLE_COMMITTET


def main() -> int:
    try:
        pfad = render_pfad()
    except (FileNotFoundError, RendererNichtMoeglich) as exc:
        print(f"kein Tracker-Stand messbar: {exc}", file=sys.stderr)
        return 2
    print(f"{pfad}\t{quelle(pfad)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
