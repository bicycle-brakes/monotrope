"""Der EINE Zugriffspunkt fuers Tracker-Render (bead 1jg.3): Reihenfolge,
Rueckfallebene, und die D-54-Reproduzierbarkeit als wiederholbarer Test."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_the_env_render_wins_over_everything(tmp_path: Path, monkeypatch) -> None:
    """Die CI rendert EINMAL und setzt BEAD_RENDER — alle Leser dieses Laufs
    nehmen genau dieses Render, nicht je eines."""
    import bead_render

    vorgesetzt = tmp_path / "vorgesetzt.jsonl"
    vorgesetzt.write_text('{"id":"coding-harness-1jg.3","status":"in_progress"}\n', encoding="utf-8")
    monkeypatch.setenv("BEAD_RENDER", str(vorgesetzt))

    assert bead_render.render_pfad() == vorgesetzt
    assert bead_render.quelle(vorgesetzt) == bead_render.QUELLE_VORGESETZT


def test_a_missing_env_render_is_an_error_not_a_silent_fallback(tmp_path: Path, monkeypatch) -> None:
    """Ein angesetztes Render, das verschwunden ist, ist ein Setupfehler —
    die stille Rueckfallebene wuerde genau die Drift verbergen, gegen die der
    Zugriffspunkt steht."""
    import bead_render

    monkeypatch.setenv("BEAD_RENDER", str(tmp_path / "fehlt.jsonl"))

    with pytest.raises(FileNotFoundError):
        bead_render.render_pfad()


def test_without_a_renderer_the_committed_copy_answers(monkeypatch) -> None:
    """Uebergangsweise (D-52): die Leerprobe und frische Klone ohne bootstrap
    koennen nicht frisch messen — die Kopie antwortet, bis sie faellt."""
    import bead_render

    def kaputt() -> None:
        raise bead_render.RendererNichtMoeglich("kein Renderer in dieser Umgebung")

    monkeypatch.setattr(bead_render, "_frisches_render", kaputt)
    monkeypatch.delenv("BEAD_RENDER", raising=False)

    assert bead_render.render_pfad() == REPO_ROOT / ".beads" / "issues.jsonl"
    assert bead_render.quelle(bead_render.render_pfad()) == bead_render.QUELLE_COMMITTET


def test_render_twice_is_byte_equal() -> None:
    """D-54: die Verifikation lebt als wiederholbarer Test — zweimal rendern,
    byte-gleich. Ohne ausfuehrbaren Tracker (Leerprobe) springt er ehrlich ab.
    """
    from render_beads_export import RendererFehlt, _render_nach

    with tempfile.TemporaryDirectory() as td:
        erstes, zweites = Path(td) / "a.jsonl", Path(td) / "b.jsonl"
        try:
            _render_nach(erstes)
        except (RendererFehlt, SystemExit) as exc:
            pytest.skip(f"kein ausfuehrbarer Tracker in dieser Umgebung: {exc}")
        _render_nach(zweites)
        assert erstes.read_bytes() == zweites.read_bytes(), (
            "derselbe Tracker-Stand muss auf derselben Maschine byte-gleich rendern"
        )


def test_the_access_point_cli_names_its_source(monkeypatch, capsys) -> None:
    """Ein Leser, der wissen will, womit er gemessen hat, fragt die Quelle —
    der CLI-Bericht nennt Pfad und Herkunft, damit kein Befund aus dem
    falschen Bild zitiert."""
    import bead_render

    monkeypatch.delenv("BEAD_RENDER", raising=False)

    assert bead_render.main() == 0
    zeile = capsys.readouterr().out.strip()
    pfad_text, quell_text = zeile.split("\t")
    assert Path(pfad_text).is_file()
    assert quell_text in (bead_render.QUELLE_GERENDERT, bead_render.QUELLE_COMMITTET)
