#!/usr/bin/env python3
"""bead_render.py — the ONE access point for the tracker render (bead 1jg.3).

D-52 (lakeswitch-ai PR #37) set the contract, ADR 0004 (accepted 2026-09-23)
confirms the direction: the render is the load-bearing contract, the committed
copy is transitional. Whoever needs the tracker state asks HERE — not
`.beads/issues.jsonl` directly and not `bd` itself. That is the third condition
of the D-52 decision: every reader on one access point; only once it stands
does the copy go.

The order in which this access point resolves:

  1. `BEAD_RENDER` — the hosted CI hydrates the tracker and renders ONCE; all
     readers of the run take exactly this render.
  2. a fresh render through `tools/bd` — once per process, then cached.
     `render_beads_export.py` stays the one-writer renderer; this access point
     is not a second renderer, it imports it.

The committed copy has been removed since the second step of this bead (D-52
thereby fulfilled): whoever has neither way does not measure — and the run says
so with a reason instead of reading an old state. A machine without a tracker
builds one (`tools/beads/install.sh` + `tools/bd bootstrap --yes`); the empty
probe deliberately measures nothing and honestly skips these tests.

Usage:
    python3 scripts/bead_render.py     # path + source on stdout
Exit: 0 = path delivered, 2 = no state measurable (way to the goal on stderr).
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

_HALTER: tempfile.TemporaryDirectory | None = None
_GERENDERT: Path | None = None


class RendererNichtMoeglich(RuntimeError):
    """This environment cannot measure fresh — no renderer, no store."""


def _frisches_render() -> Path:
    """Renders once per process through the one-writer renderer."""
    global _HALTER, _GERENDERT
    if _GERENDERT is None:
        _HALTER = tempfile.TemporaryDirectory(prefix="bead-render-")
        ziel = Path(_HALTER.name) / "issues.jsonl"
        from render_beads_export import RendererFehlt, _render_nach  # noqa: E402 — no second renderer

        try:
            _render_nach(ziel)
        except RendererFehlt as exc:
            # No bd on this machine (fresh clone, an agent without bd) —
            # exactly the case for which D-52 demands the instructions as
            # successor to the copy, not a traceback (review 2026-09-23).
            _HALTER.cleanup()
            _HALTER, _GERENDERT = None, None
            raise RendererNichtMoeglich(f"no executable bd ({exc})") from None
        except SystemExit as exc:
            # _render_nach reports preconditions beyond the missing binary
            # as SystemExit(2) — the same finding, just another wrapper.
            if exc.code != 2:
                raise
            _HALTER.cleanup()
            _HALTER, _GERENDERT = None, None
            raise RendererNichtMoeglich("the renderer refuses in this environment") from None
        _GERENDERT = ziel
    return _GERENDERT


def render_pfad() -> Path:
    """The path ALL readers of this run take. Raises if nothing measures.

    Without a preset render and without a renderer this is a hard error that
    names both ways — a silent fall-back to an old state would be exactly the
    lie D-52 set the contract against.
    """
    vorgesetzt = os.environ.get(UMGEBUNGS_RENDER, "").strip()
    if vorgesetzt:
        pfad = Path(vorgesetzt)
        if not pfad.is_file():
            raise FileNotFoundError(
                f"{UMGEBUNGS_RENDER} points to {pfad}, the file is missing — a "
                "preset render that has vanished is a setup error, "
                "not a reason for a silent fall-back."
            )
        return pfad
    try:
        return _frisches_render()
    except RendererNichtMoeglich as exc:
        raise RendererNichtMoeglich(
            f"{exc} — no tracker state measurable. Two ways: "
            "`tools/beads/install.sh && tools/bd bootstrap --yes` (this "
            f"machine measures fresh) or set {UMGEBUNGS_RENDER} to a render "
            "(this is what CI does)."
        ) from None


def nicht_gemessen(gate: str, exc: Exception) -> int:
    """Exit 3 with a reason: a gate that cannot reach the tracker does not measure.

    The runner turns exit 3 on a block gate red (bead 4t8) — like
    decision-continuity without a target document. The reason names both ways to
    the goal.
    """
    print(f"{gate} NICHT GEMESSEN: {exc}")
    return 3


def quelle(pfad: Path) -> str:
    """For the report only: where the delivered path comes from."""
    if os.environ.get(UMGEBUNGS_RENDER, "").strip() == str(pfad):
        return QUELLE_VORGESETZT
    return QUELLE_GERENDERT


def main() -> int:
    try:
        pfad = render_pfad()
    except (FileNotFoundError, RendererNichtMoeglich) as exc:
        print(f"no tracker state measurable: {exc}", file=sys.stderr)
        return 2
    print(f"{pfad}\t{quelle(pfad)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
