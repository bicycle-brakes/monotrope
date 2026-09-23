#!/usr/bin/env python3
"""render_beads_export.py — der Eine-Schreiber-Renderer des Trackers (D-4).

Der Render ist der tragende Vertrag (ADR 0004); eine committete Kopie gibt
es seit bead coding-harness-1jg.3 nicht mehr. Wer das Render braucht, geht
ueber `scripts/bead_render.py` — dieses Script ist der Eine-Schreiber
HINTER dem Zugriffspunkt:

    python3 scripts/render_beads_export.py

Es rendert über das gepinnte `tools/bd` in eine Temp-Datei, prueft das
Ergebnis Zeile fuer Zeile (ueber check_bead_export.run) und schreibt es
erst dann an seinen Zielort — kaputte Renders erreichen keinen Leser. Die
 gehostete CI ruft es im Hydratationsschritt genau einmal auf und setzt
`BEAD_RENDER` auf das Ergebnis; alle Leser des Laufs nehmen dieses Render
(D-52, Bedingung 2).

Usage:
    python3 scripts/render_beads_export.py
Exit: 0 = gerendert, 1 = Befund, 2 = Vorbedingung.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"
BD = REPO_ROOT / "tools" / "bd"
BD_FEHLT = 127  # tools/bd: "no bd binary found" — und nur das


# Maschinenlokale Felder. Eine Lease gehoert der Maschine, die den Vorgang
# gerade haelt: bd 1.3.0 schreibt `heartbeat_at` und `lease_expires_at` in den
# Export des Schreibers, ein frischer Klon desselben Dolt-Stands rendert sie
# nicht (gemessen 2026-09-21: identischer Inhalt, zwei abweichende Felder an
# einem Vorgang in Arbeit). Mit ihnen ist der Export nur auf der Maschine
# byte-gleich, die zuletzt gerendert hat — und die Identitaetspruefung haelt
# nirgends sonst. Die Liste steht EINMAL, hier; Tests lesen sie von hier.
MASCHINENLOKAL: tuple[str, ...] = ("heartbeat_at", "lease_expires_at")

# So schreibt der Tracker JSON: kompakt, und `<`, `>`, `&` sowie U+2028/U+2029
# als \uXXXX. Wer eine Zeile neu schreibt, muss genau das treffen.
_TRACKER_ESCAPES = {"<": "\\u003c", ">": "\\u003e", "&": "\\u0026", "\u2028": "\\u2028", "\u2029": "\\u2029"}


class NichtReproduzierbar(RuntimeError):
    """Eine Exportzeile laesst sich nicht byte-gleich wiedergeben — also wird sie nicht umgeschrieben."""


def _wie_der_tracker(satz: dict) -> str:
    text = json.dumps(satz, ensure_ascii=False, separators=(",", ":"))
    for zeichen, ersatz in _TRACKER_ESCAPES.items():
        text = text.replace(zeichen, ersatz)
    return text


def _ohne_maschinenlokales(roh: str) -> str:
    """Nimmt die maschinenlokalen Felder heraus und laesst jedes andere Byte stehen.

    Eine Zeile ohne ein solches Feld geht unberuehrt durch. Eine Zeile mit
    einem wird neu geschrieben — aber erst, nachdem dieselbe Schreibweise die
    UNVERAENDERTE Zeile byte-gleich wiedergegeben hat. Gelingt das nicht, ist
    die Schreibweise des Trackers eine andere geworden, und ein stilles
    Umschreiben waere genau die Drift, gegen die diese Datei steht.
    """
    zeilen = []
    # Nur `\n` trennt Saetze. `str.splitlines()` schneidet auch an U+0085,
    # U+2028 und anderen Zeichen, die der Tracker roh in einen Text schreibt —
    # und zerlegte damit einen Satz in zwei kaputte Zeilen (Review F-1).
    ende = "\n" if roh.endswith("\n") else ""
    for nr, zeile in enumerate((roh[:-1] if ende else roh).split("\n"), 1):
        try:
            satz = json.loads(zeile) if zeile.strip() else None
        except json.JSONDecodeError:
            satz = None  # die Zeilenpruefung danach benennt den Befund
        if not isinstance(satz, dict) or not any(k in satz for k in MASCHINENLOKAL):
            zeilen.append(zeile)
            continue
        if _wie_der_tracker(satz) != zeile:
            raise NichtReproduzierbar(
                f"Zeile {nr} ({satz.get('id', '?')}): die Schreibweise des Trackers laesst sich nicht "
                "byte-gleich wiedergeben — maschinenlokale Felder bleiben stehen, der Render wird verworfen"
            )
        zeilen.append(_wie_der_tracker({k: v for k, v in satz.items() if k not in MASCHINENLOKAL}))
    return "\n".join(zeilen) + ende


class RendererFehlt(RuntimeError):
    """`tools/bd` ist in dieser Umgebung nicht ausfuehrbar (z. B. CI ohne Tracker)."""


def _render_nach(tmp: Path) -> None:
    """Rendert ueber tools/bd in die Temp-Datei. Kein bare bd, kein zweiter Pfad."""
    try:
        erg = subprocess.run(
            [str(BD), "export", "-o", str(tmp)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RendererFehlt(str(exc)) from exc
    if erg.returncode == BD_FEHLT:
        # Der Wrapper ist da, das gepinnte Binary nicht: dieselbe Lage wie ein
        # fehlender Wrapper. Jeder andere Fehler (Versionskonflikt, kaputter
        # Store) bleibt ein harter Fehler.
        raise RendererFehlt((erg.stderr or erg.stdout).strip().splitlines()[0])
    if erg.returncode != 0:
        sys.stderr.write(erg.stdout + erg.stderr)
        raise SystemExit(2)
    tmp.write_text(_ohne_maschinenlokales(tmp.read_text(encoding="utf-8")), encoding="utf-8")


def _sha(pfad: Path) -> str:
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    try:
        return _main(argv)
    except NichtReproduzierbar as exc:
        print(f"Render verworfen: {exc}")
        return 1


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args(argv)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "issues.jsonl"
        _render_nach(tmp)
        from check_bead_export import run  # noqa: E402 — gleiche Zeilenpruefung

        befunde = run(tmp)
        if befunde:
            print("Render verworfen — der Renderer schreibt keinen kaputten Export:")
            for b in befunde:
                print(f"  - {b}")
            return 1
        EXPORT.write_bytes(tmp.read_bytes())

    print(f"Render geschrieben: {EXPORT.relative_to(REPO_ROOT)} (sha256 {_sha(EXPORT)[:12]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
