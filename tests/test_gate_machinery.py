"""Mutationsnachweise und Abdeckung der Gate-Maschinerie (RB-G4, bead bo0).

Ein Test, der nur assertiert, dass es heute gruen ist, prueft die Welt und
nicht das Gate. Diese Datei haelt fuer jeden selbstgebauten Gate den Lauf,
der ihn rot macht — und fuer die uebrigen Scripts die Ausfuehrung, die die
Sperrklinken (OHNE_AUFRUFER / OHNE_TEST in ci_gates.py) verlangen.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


# --------------------------------------------------------------------------
# gate-schema — das Gate, das die Gate-Datei selbst liest
# --------------------------------------------------------------------------


def test_gate_schema_gate_goes_red_when_an_entry_has_no_command() -> None:
    import ci_gates

    schlecht = {
        "schema_version": 1,
        "gates": [
            {
                "id": "kaputt",
                "title": "weder Kommando noch Action",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "reason": "ein Seed, der den Schemafehler demonstriert",
            }
        ],
    }
    befunde = ci_gates.validate_schema(schlecht)
    assert befunde, "ein Gate ohne command und ohne action muss ins Schema fallen"
    assert any("kaputt" in b for b in befunde)


def test_gate_schema_gate_accepts_the_real_gate_file() -> None:
    import ci_gates

    doc = yaml.safe_load((REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
    assert ci_gates.validate_schema(doc) == []


# --------------------------------------------------------------------------
# ci-drift — die abgeleitete ci.yml gegen den Handgriff
# --------------------------------------------------------------------------


def test_ci_drift_gate_goes_red_when_the_workflow_is_hand_edited(tmp_path: Path, monkeypatch) -> None:
    import ci_gates

    soll = ci_gates.generate_ci()
    ziel = tmp_path / "ci.yml"

    monkeypatch.setattr(ci_gates, "CI_FILE", ziel)
    ziel.write_text(soll, encoding="utf-8")
    assert ci_gates.check_ci() == 0, "die exakte Ableitung muss als gruen durchgehen"

    hand = soll.replace("cron:", "cron-handgriff:")
    ziel.write_text(hand, encoding="utf-8")
    assert ci_gates.check_ci() == 1, "ein Handgriff in der abgeleiteten Datei muss rot machen"


def test_the_pinned_ci_gates_cli_runs_green_against_the_real_gate_file() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/ci_gates.py", "--check-schema"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


# --------------------------------------------------------------------------
# docs-links — Frontmatter, Links, Anker
# --------------------------------------------------------------------------


def test_check_docs_gate_goes_red_when_a_link_is_broken(tmp_path: Path) -> None:
    import check_docs

    kopf = (
        "---\ntitle: Probe\ncategory: architecture\nstatus: proposed\n"
        "created: 2026-09-19\nlast_reviewed: 2026-09-19\nowner: framework-architect\n"
        "provenance: ai-drafted-reviewed\nproduced_by:\n  kind: llm-session\n"
        "  name: probe\n  version: '1'\nreview:\n  status: pending\n"
        "  approved_by: null\n  approved_at: null\ntags: [probe]\n---\n\n"
    )
    (tmp_path / "kaputt.md").write_text(kopf + "[toter Nachbar](fehlt.md)\n", encoding="utf-8")
    befunde = check_docs.run(tmp_path)
    assert any("toter Link" in b for b in befunde), befunde

    (tmp_path / "ok.md").write_text(kopf + "[echter Nachbar](kaputt.md)\n", encoding="utf-8")
    rest = [b for b in check_docs.run(tmp_path) if "ok.md" in b]
    assert not rest, rest


def test_the_check_docs_cli_runs_over_the_documentation() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/check_docs.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode in (0, 1), erg.stdout + erg.stderr  # gruen oder Befunde, nie Absturz


# --------------------------------------------------------------------------
# bead-export — der gerenderte Tracker
# --------------------------------------------------------------------------


def test_check_bead_export_gate_goes_red_when_a_line_is_broken(tmp_path: Path) -> None:
    import check_bead_export

    kaputt = tmp_path / "issues.jsonl"
    kaputt.write_text('{"id": "a", "status": "open"}\n{kaputt\n', encoding="utf-8")
    befunde = check_bead_export.run(kaputt)
    assert befunde, "eine kaputte Zeile muss einen Befund liefern"

    ok = tmp_path / "ok.jsonl"
    ok.write_text('{"id": "a", "status": "open"}\n', encoding="utf-8")
    assert check_bead_export.run(ok) == []


def test_the_real_bead_export_parses_line_by_line() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/check_bead_export.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


# --------------------------------------------------------------------------
# Die uebrigen Scripts — die Ausfuehrung, die die Sperrklinken verlangen
# --------------------------------------------------------------------------


def test_the_plans_registry_staleness_check_runs_green_here() -> None:
    import plans_registry

    assert plans_registry.main(["--check"]) == 0


def test_the_ramp_valve_check_runs_green_here() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/ramp_valves.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


# --------------------------------------------------------------------------
# dangling-beads — zitierte Vorgangs-IDs loesen im Export auf
# --------------------------------------------------------------------------


def test_dangling_beads_gate_goes_red_when_a_cited_id_is_unknown(tmp_path: Path) -> None:
    import check_dangling_bead_ids

    basis = tmp_path / "docs"
    basis.mkdir()
    (basis / "zitat.md").write_text("Siehe `coding-harness-nichtda` und `coding-harness-bo0`.\n", encoding="utf-8")
    export = tmp_path / "issues.jsonl"
    export.write_text('{"id": "coding-harness-bo0", "status": "open"}\n', encoding="utf-8")
    befunde = check_dangling_bead_ids.run(basis, export)
    assert any("coding-harness-nichtda" in b for b in befunde), befunde
    assert not any("coding-harness-bo0" in b for b in befunde), befunde


def test_the_real_dangling_bead_check_runs_green_here() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/check_dangling_bead_ids.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


# --------------------------------------------------------------------------
# decision-continuity — eine Entscheidung verschwindet nur sichtbar (Frage 5)
# --------------------------------------------------------------------------


def test_decision_continuity_gate_goes_red_when_an_id_is_missing(tmp_path: Path) -> None:
    import check_decision_continuity

    ziel = tmp_path / "target.md"
    ziel.write_text(
        "# Target\n\n## Decision continuity\n\n| Decision | Disposition |\n|---|---|\n| D-1 — vocabulary | Retain |\n",
        encoding="utf-8",
    )
    befunde = check_decision_continuity.run(ziel, tmp_path)
    assert any("D-17 fehlt" in b for b in befunde), befunde
    assert any("D-2 fehlt" in b for b in befunde), befunde
    assert any("ADR fehlt" in b for b in befunde), befunde


def test_the_real_decision_continuity_check_runs_green_here() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/check_decision_continuity.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


# --------------------------------------------------------------------------
# export-identity — der committed Export ist das frische Render (D-4)
# --------------------------------------------------------------------------


def test_export_identity_gate_goes_red_when_the_committed_export_drifts(tmp_path: Path, monkeypatch) -> None:
    # Der Gate: python3 scripts/render_beads_export.py --check
    import render_beads_export as rbe

    committed = tmp_path / "issues.jsonl"
    committed.write_text('{"id": "a", "status": "open"}\n', encoding="utf-8")
    frisch = tmp_path / "frisch.jsonl"
    frisch.write_text('{"id": "a", "status": "open"}\n{"id": "b", "status": "closed"}\n', encoding="utf-8")
    monkeypatch.setattr(rbe, "EXPORT", committed)
    monkeypatch.setattr(rbe, "_render_nach", lambda p: p.write_bytes(frisch.read_bytes()))
    assert rbe.main(["--check"]) == 1


def test_export_identity_gate_accepts_the_identical_render(tmp_path: Path, monkeypatch) -> None:
    import render_beads_export as rbe

    identisch = '{"id": "a", "status": "open"}\n'
    committed = tmp_path / "issues.jsonl"
    committed.write_text(identisch, encoding="utf-8")
    frisch = tmp_path / "frisch.jsonl"
    frisch.write_text(identisch, encoding="utf-8")
    monkeypatch.setattr(rbe, "EXPORT", committed)
    monkeypatch.setattr(rbe, "_render_nach", lambda p: p.write_bytes(frisch.read_bytes()))
    assert rbe.main(["--check"]) == 0


def test_export_identity_gate_skips_visibly_where_the_tracker_does_not_live(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import render_beads_export as rbe

    monkeypatch.setattr(rbe, "EXPORT", tmp_path / "issues.jsonl")

    def fehlt(_p: Path) -> None:
        raise rbe.RendererFehlt("tools/bd fehlt in dieser Umgebung")

    monkeypatch.setattr(rbe, "_render_nach", fehlt)
    assert rbe.main(["--check"]) == 0
    assert "SKIP" in capsys.readouterr().out


def test_export_identity_gate_skips_when_the_wrapper_finds_no_binary(tmp_path: Path, monkeypatch, capsys) -> None:
    """Der echte Weg der CI: tools/bd existiert, das gepinnte Binary nicht.

    Der Test darueber reicht die Ausnahme von Hand herein; hier laeuft der
    Wrapper wirklich, in einer Umgebung ohne bd. Ohne die Unterscheidung am
    Exit-Code endete genau diese Lage in Exit 2 statt im sichtbaren SKIP.
    """
    import render_beads_export as rbe

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setattr(rbe, "EXPORT", tmp_path / "issues.jsonl")
    assert rbe.main(["--check"]) == 0
    assert "SKIP" in capsys.readouterr().out
