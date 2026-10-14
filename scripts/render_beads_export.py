#!/usr/bin/env python3
"""render_beads_export.py — the one-writer renderer of the tracker (D-4).

The render is the load-bearing contract (ADR 0004); since bead
coding-harness-1jg.3 there is no committed copy any more. Whoever needs the
render goes through `scripts/bead_render.py` — this script is the one writer
BEHIND that access point:

    python3 scripts/render_beads_export.py

It renders through the pinned `tools/bd` into a temp file, checks the result
line by line (via check_bead_export.run) and only then writes it to its
destination — a broken render never reaches a reader. The hosted CI calls it
exactly once in the hydration step and sets `BEAD_RENDER` to the result; all
readers of the run take that render (D-52, condition 2).

Usage:
    python3 scripts/render_beads_export.py
Exit: 0 = rendered, 1 = finding, 2 = precondition.
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
BD_FEHLT = 127  # tools/bd: "no bd binary found" — and only that


# Machine-local fields. A lease belongs to the machine that currently holds
# the item: bd 1.3.0 writes `heartbeat_at` and `lease_expires_at` into the
# writer's export, while a fresh clone of the same Dolt state does not render
# them (measured 2026-09-21: identical content, two differing fields on one
# item in progress). With them the export is byte-equal only on the machine
# that rendered last — and the identity check holds nowhere else. The list
# stands ONCE, here; tests read it from here.
MASCHINENLOKAL: tuple[str, ...] = ("heartbeat_at", "lease_expires_at")

# This is how the tracker writes JSON: compact, with `<`, `>`, `&` and
# U+2028/U+2029 as \uXXXX. Whoever rewrites a line must hit exactly that.
_TRACKER_ESCAPES = {"<": "\\u003c", ">": "\\u003e", "&": "\\u0026", "\u2028": "\\u2028", "\u2029": "\\u2029"}


class NichtReproduzierbar(RuntimeError):
    """An export line cannot be reproduced byte-for-byte — so it is not rewritten."""


def _wie_der_tracker(satz: dict) -> str:
    text = json.dumps(satz, ensure_ascii=False, separators=(",", ":"))
    for zeichen, ersatz in _TRACKER_ESCAPES.items():
        text = text.replace(zeichen, ersatz)
    return text


def _ohne_maschinenlokales(roh: str) -> str:
    """Removes the machine-local fields and leaves every other byte alone.

    A line without such a field passes through untouched. A line with one is
    rewritten — but only after the same notation has reproduced the UNCHANGED
    line byte-for-byte. If that fails, the tracker's notation has changed, and
    a silent rewrite would be exactly the drift this file stands against.
    """
    zeilen = []
    # Only `\n` separates records. `str.splitlines()` also cuts at U+0085,
    # U+2028 and other characters the tracker writes raw into a text — and
    # would thereby split one record into two broken lines (review F-1).
    ende = "\n" if roh.endswith("\n") else ""
    for nr, zeile in enumerate((roh[:-1] if ende else roh).split("\n"), 1):
        try:
            satz = json.loads(zeile) if zeile.strip() else None
        except json.JSONDecodeError:
            satz = None  # the line check afterwards names the finding
        if not isinstance(satz, dict) or not any(k in satz for k in MASCHINENLOKAL):
            zeilen.append(zeile)
            continue
        if _wie_der_tracker(satz) != zeile:
            raise NichtReproduzierbar(
                f"Line {nr} ({satz.get('id', '?')}): the tracker's notation cannot be reproduced "
                "byte-for-byte — machine-local fields stay in place, the render is discarded"
            )
        zeilen.append(_wie_der_tracker({k: v for k, v in satz.items() if k not in MASCHINENLOKAL}))
    return "\n".join(zeilen) + ende


class RendererFehlt(RuntimeError):
    """`tools/bd` is not executable in this environment (e.g. CI without a tracker)."""


def _render_nach(tmp: Path) -> None:
    """Renders through tools/bd into the temp file. No bare bd, no second path."""
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
        # The wrapper is there, the pinned binary is not: the same situation
        # as a missing wrapper. Every other error (version conflict, broken
        # store) remains a hard error.
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
        print(f"Render discarded: {exc}")
        return 1


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args(argv)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "issues.jsonl"
        _render_nach(tmp)
        from check_bead_export import run  # noqa: E402 — same line check

        befunde = run(tmp)
        if befunde:
            print("Render discarded — the renderer does not write a broken export:")
            for b in befunde:
                print(f"  - {b}")
            return 1
        EXPORT.write_bytes(tmp.read_bytes())

    print(f"Render written: {EXPORT.relative_to(REPO_ROOT)} (sha256 {_sha(EXPORT)[:12]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
