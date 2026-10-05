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


def test_without_renderer_or_preset_render_it_raises_and_names_both_ways_out(monkeypatch) -> None:
    """Keine Kopie mehr, auf die man still fallen koennte (D-52 erfuellt): der
    Zugriffspunkt wirft — und der Grund nennt bootstrap und BEAD_RENDER, damit
    eine Maschine ohne Tracker weiss, was zu tun ist."""
    import bead_render

    def kaputt() -> None:
        raise bead_render.RendererNichtMoeglich("kein Renderer in dieser Umgebung")

    monkeypatch.setattr(bead_render, "_frisches_render", kaputt)
    monkeypatch.delenv("BEAD_RENDER", raising=False)

    with pytest.raises(bead_render.RendererNichtMoeglich) as excinfo:
        bead_render.render_pfad()
    grund = str(excinfo.value)
    assert "bootstrap" in grund
    assert "BEAD_RENDER" in grund


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


def test_the_access_point_cli_names_its_source_or_its_way_out(monkeypatch, capsys) -> None:
    """Der CLI-Bericht hat zwei ehrliche Ausgaenge: Pfad plus Herkunft (0),
    oder — ohne Renderer und ohne vorgesetztes Render — Exit 2 mit dem Weg
    zum Ziel auf stderr. Beide Antworten benennbar, keine schweigt."""
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


# --- Review von e02c915, 2026-09-23 ------------------------------------------


def test_without_a_bd_binary_the_access_point_names_both_ways(monkeypatch) -> None:
    """Der haeufigste Fall ohne Tracker — kein bd auf der Maschine — wirft im
    Renderer `RendererFehlt`. Der Zugriffspunkt macht daraus seinen eigenen
    Fehler mit beiden Wegen, statt einen Traceback durchzureichen."""
    import bead_render
    import render_beads_export

    def fehlt(_ziel: Path) -> None:
        raise render_beads_export.RendererFehlt("no bd binary found.")

    monkeypatch.setattr(render_beads_export, "_render_nach", fehlt)
    # Beide zuruecksetzen: monkeypatch haelt die Originale am Leben und stellt
    # sie wieder her — sonst loeschte der Finalizer des alten Temp-Ordners das
    # zwischengespeicherte Render, das spaetere Tests desselben Prozesses lesen.
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
    """Bead 4t8: ein Gate, das nicht misst, endet in Exit 3 mit Grund — nicht
    in einem Traceback, der wie ein Befund im Code aussieht."""
    import importlib

    import bead_render

    def kaputt() -> Path:
        raise bead_render.RendererNichtMoeglich("kein bd ausfuehrbar")

    monkeypatch.setattr(bead_render, "render_pfad", kaputt)
    leser = importlib.import_module(modul)
    assert leser.main() == 3
    assert f"{gate} NICHT GEMESSEN" in capsys.readouterr().out


def test_plans_registry_blocks_instead_of_crashing_without_tracker(monkeypatch) -> None:
    import bead_render
    import plans_registry

    def kaputt() -> Path:
        raise bead_render.RendererNichtMoeglich("kein bd ausfuehrbar")

    monkeypatch.setattr(plans_registry, "_bead_export_path", kaputt)
    verdict = plans_registry.check()
    assert any("not measurable" in f.message for f in verdict.findings if f.level.name == "BLOCK")


def test_plans_registry_names_a_render_outside_the_repo(tmp_path: Path, monkeypatch) -> None:
    """Ein frisches Render liegt in /tmp: die Meldung zeigt den Pfad, statt an
    `relative_to(REPO)` mit ValueError abzustuerzen."""
    import plans_registry

    leer = tmp_path / "issues.jsonl"
    leer.write_text("", encoding="utf-8")
    monkeypatch.setattr(plans_registry, "_bead_export_path", lambda: leer)
    verdict = plans_registry.check()
    assert any(str(leer) in f.message for f in verdict.findings if f.level.name == "BLOCK")
