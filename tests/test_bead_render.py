"""The ONE access point for the tracker render (bead 1jg.3): order,
fallback, and the D-54 reproducibility as a repeatable test."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_the_env_render_wins_over_everything(tmp_path: Path, monkeypatch) -> None:
    """The CI renders ONCE and sets BEAD_RENDER — all readers of this run
    take exactly this render, not one each."""
    import bead_render

    vorgesetzt = tmp_path / "vorgesetzt.jsonl"
    vorgesetzt.write_text('{"id":"coding-harness-1jg.3","status":"in_progress"}\n', encoding="utf-8")
    monkeypatch.setenv("BEAD_RENDER", str(vorgesetzt))

    assert bead_render.render_pfad() == vorgesetzt
    assert bead_render.quelle(vorgesetzt) == bead_render.QUELLE_VORGESETZT


def test_a_missing_env_render_is_an_error_not_a_silent_fallback(tmp_path: Path, monkeypatch) -> None:
    """A preset render that has vanished is a setup error — the silent
    fallback would hide exactly the drift the access point stands against."""
    import bead_render

    monkeypatch.setenv("BEAD_RENDER", str(tmp_path / "fehlt.jsonl"))

    with pytest.raises(FileNotFoundError):
        bead_render.render_pfad()


def test_without_renderer_or_preset_render_it_raises_and_names_both_ways_out(monkeypatch) -> None:
    """No copy left to fall back on silently (D-52 fulfilled): the access
    point raises — and the reason names bootstrap and BEAD_RENDER, so that a
    machine without a tracker knows what to do."""
    import bead_render

    def kaputt() -> None:
        raise bead_render.RendererNichtMoeglich("no renderer in this environment")

    monkeypatch.setattr(bead_render, "_frisches_render", kaputt)
    monkeypatch.delenv("BEAD_RENDER", raising=False)

    with pytest.raises(bead_render.RendererNichtMoeglich) as excinfo:
        bead_render.render_pfad()
    grund = str(excinfo.value)
    assert "bootstrap" in grund
    assert "BEAD_RENDER" in grund


def test_render_twice_is_byte_equal() -> None:
    """D-54: the verification lives as a repeatable test — render twice,
    byte-equal. Without an executable tracker (dry run) it honestly skips.
    """
    from render_beads_export import RendererFehlt, _render_nach

    with tempfile.TemporaryDirectory() as td:
        erstes, zweites = Path(td) / "a.jsonl", Path(td) / "b.jsonl"
        try:
            _render_nach(erstes)
        except (RendererFehlt, SystemExit) as exc:
            pytest.skip(f"no executable tracker in this environment: {exc}")
        _render_nach(zweites)
        assert erstes.read_bytes() == zweites.read_bytes(), (
            "the same tracker state must render byte-equal on the same machine"
        )


def test_the_access_point_cli_names_its_source_or_its_way_out(monkeypatch, capsys) -> None:
    """The CLI report has two honest outcomes: path plus origin (0), or —
    without a renderer and without a preset render — exit 2 with the way out
    on stderr. Both answers nameable, neither is silent."""
    import bead_render

    monkeypatch.delenv("BEAD_RENDER", raising=False)

    code = bead_render.main()
    gefangen = capsys.readouterr()
    if code == 0:
        pfad_text, quell_text = gefangen.out.strip().split("\t")
        assert Path(pfad_text).is_file()
        assert quell_text in (bead_render.QUELLE_VORGESETZT, bead_render.QUELLE_GERENDERT)
    else:
        assert code == 2
        assert "bootstrap" in gefangen.err
        assert "BEAD_RENDER" in gefangen.err


# --- Review of e02c915, 2026-09-23 ------------------------------------------


def test_without_a_bd_binary_the_access_point_names_both_ways(monkeypatch) -> None:
    """The most common case without a tracker — no bd on the machine — makes
    the renderer raise `RendererFehlt`. The access point turns that into its
    own error naming both ways out, instead of passing a traceback through."""
    import bead_render
    import render_beads_export

    def fehlt(_ziel: Path) -> None:
        raise render_beads_export.RendererFehlt("no bd binary found.")

    monkeypatch.setattr(render_beads_export, "_render_nach", fehlt)
    # Reset both: monkeypatch keeps the originals alive and restores them —
    # otherwise the finalizer of the old temp folder would delete the cached
    # render that later tests of the same process read.
    monkeypatch.setattr(bead_render, "_HALTER", None)
    monkeypatch.setattr(bead_render, "_GERENDERT", None)
    monkeypatch.delenv("BEAD_RENDER", raising=False)
    with pytest.raises(bead_render.RendererNichtMoeglich) as excinfo:
        bead_render.render_pfad()
    assert "bootstrap" in str(excinfo.value) and "BEAD_RENDER" in str(excinfo.value)


@pytest.mark.parametrize(
    ("modul", "gate"), [("check_bead_export", "bead-export"), ("check_dangling_bead_ids", "dangling-beads")]
)
def test_a_reader_without_tracker_exits_3_not_measured(modul: str, gate: str, monkeypatch, capsys) -> None:
    """Bead 4t8: a gate that does not measure ends in exit 3 with a reason —
    not in a traceback that looks like a finding in the code."""
    import importlib

    import bead_render

    def kaputt() -> Path:
        raise bead_render.RendererNichtMoeglich("no executable bd")

    monkeypatch.setattr(bead_render, "render_pfad", kaputt)
    leser = importlib.import_module(modul)
    assert leser.main() == 3
    assert f"{gate} NICHT GEMESSEN" in capsys.readouterr().out


def test_plans_registry_blocks_instead_of_crashing_without_tracker(monkeypatch) -> None:
    import bead_render
    import plans_registry

    def kaputt() -> Path:
        raise bead_render.RendererNichtMoeglich("no executable bd")

    monkeypatch.setattr(plans_registry, "_bead_export_path", kaputt)
    verdict = plans_registry.check()
    assert any("not measurable" in f.message for f in verdict.findings if f.level.name == "BLOCK")


def test_plans_registry_names_a_render_outside_the_repo(tmp_path: Path, monkeypatch) -> None:
    """A fresh render lives in /tmp: the message shows the path instead of
    crashing on `relative_to(REPO)` with a ValueError."""
    import plans_registry

    leer = tmp_path / "issues.jsonl"
    leer.write_text("", encoding="utf-8")
    monkeypatch.setattr(plans_registry, "_bead_export_path", lambda: leer)
    verdict = plans_registry.check()
    assert any(str(leer) in f.message for f in verdict.findings if f.level.name == "BLOCK")
