#!/usr/bin/env python3
"""render_beads_export.py — der Eine-Schreiber-Renderer des Trackers (D-4).

Auto-Export ist seit dem 2026-09-17 ausgeschaltet. Der Export wird EINMAL,
am Sitzungsende, von dem einen Schreiber gerendert, der die Writer-Lock
haelt (ADR 0002). Dieses Script ist dieser eine Aufruf:

    python3 scripts/render_beads_export.py

Es rendert über das gepinnte `tools/bd` in eine Temp-Datei, prueft das
Ergebnis Zeile fuer Zeile (ueber check_bead_export.run) und uebertraegt es
erst dann an `.beads/issues.jsonl` — kaputte Renders erreichen den committed
Stand nie. Der SHA-256 des Ergebnisses geht auf stdout: er bindet den
Sitzungsbericht an genau diesen Export.

Usage:
    python3 scripts/render_beads_export.py [--check]
Exit: 0 = gerendert (oder --check: identisch, oder SKIP ohne Tracker),
      1 = Befund, 2 = Vorbedingung.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"
BD = REPO_ROOT / "tools" / "bd"
BD_FEHLT = 127  # tools/bd: "no bd binary found" — und nur das


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


def _sha(pfad: Path) -> str:
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="nicht schreiben: den committed Export gegen ein frisches Render vergleichen",
    )
    args = ap.parse_args(argv)

    if args.check:
        with tempfile.TemporaryDirectory() as td:
            frisch = Path(td) / "issues.jsonl"
            try:
                _render_nach(frisch)
            except RendererFehlt as exc:
                print(f"export-identity SKIP: {exc}")
                print("Der Gate gilt dort, wo der Tracker lebt (Writer-Lock, ADR 0002).")
                return 0
            soll = _sha(frisch)
        ist = _sha(EXPORT) if EXPORT.is_file() else None
        if ist == soll:
            print(f"Export-Identitaet ok (sha256 {soll[:12]}…).")
            return 0
        print("Export DRIFT: der committed Stand ist nicht das frische Render.")
        print("Rendern:  python3 scripts/render_beads_export.py")
        print(f"  committed sha256: {ist or '—'}")
        print(f"  frisch   sha256: {soll}")
        return 1

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

    print(f"Export gerendert: {EXPORT.relative_to(REPO_ROOT)} (sha256 {_sha(EXPORT)[:12]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
