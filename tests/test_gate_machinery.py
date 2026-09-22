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

import pytest
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


def test_gate_schema_gate_rejects_a_non_boolean_needs_tracker() -> None:
    """Bead 4t8: needs_tracker steuert einen CI-Schritt — ein Text dort waere Stille."""
    import ci_gates

    schlecht = {
        "schema_version": 1,
        "gates": [
            {
                "id": "kaputt",
                "title": "needs_tracker als Text",
                "command": "python3 -c 'print(1)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "needs_tracker": "yes",
                "reason": "ein Seed, der den Schemafehler demonstriert",
            }
        ],
    }
    befunde = ci_gates.validate_schema(schlecht)
    assert befunde, "needs_tracker muss ein Boolean sein"
    assert any("needs_tracker" in b for b in befunde)


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


def test_check_bead_export_gate_refuses_an_empty_export(tmp_path: Path) -> None:
    """Bead 4t8: ein Export ueber null Zeilen misst nichts — das ist ein Befund.

    Bis 2026-09-22 war der Gate hier gruen: jede Zeilenpruefung lief ueber null
    Zeilen und meldete Vollstaendigkeit ueber einer leeren Menge. Genau die
    Luecke, die das Interview "floor: true ist nicht leer" nennt.
    """
    import check_bead_export

    leer = tmp_path / "leer.jsonl"
    leer.write_text("\n\n", encoding="utf-8")
    befunde = check_bead_export.run(leer)
    assert befunde, "ein leerer Export muss einen Befund liefern"
    assert "leer" in befunde[0]


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


def test_decision_continuity_is_red_while_its_target_is_missing(tmp_path: Path) -> None:
    """Bead 4t8: floor: true — ein fehlendes Ziel ist Exit 3, kein stilles gruen.

    Bis zum #8-Merge meldete diese Lage "SKIP" (Exit 0) und nannte als Grund
    einen Zustand, der seitdem Vergangenheit ist. Ein Gate, dessen Ziel fehlt,
    kann nicht messen — und ein floor-Gate, das nicht misst, faellt.
    """
    erg = subprocess.run(
        [
            sys.executable,
            "scripts/check_decision_continuity.py",
            "--target",
            str(tmp_path / "fehlt.md"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 3, erg.stdout + erg.stderr
    assert "NICHT GEMESSEN" in erg.stdout


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


def test_export_identity_gate_is_red_where_the_tracker_does_not_live(tmp_path: Path, monkeypatch, capsys) -> None:
    """Bead 4t8: der Gate steht auf floor: true — nicht messen ist rot, nicht gruen.

    Bis 2026-09-22 meldete diese Lage "SKIP" und endete in Exit 0: die CI war
    dauerhaft gruen, ohne je gemessen zu haben. Jetzt ist es Exit 3 — der
    Runner macht daraus bei einem block-Gate rot.
    """
    import render_beads_export as rbe

    monkeypatch.setattr(rbe, "EXPORT", tmp_path / "issues.jsonl")

    def fehlt(_p: Path) -> None:
        raise rbe.RendererFehlt("tools/bd fehlt in dieser Umgebung")

    monkeypatch.setattr(rbe, "_render_nach", fehlt)
    assert rbe.main(["--check"]) == 3
    assert "NICHT GEMESSEN" in capsys.readouterr().out


def test_export_identity_gate_is_red_when_the_wrapper_finds_no_binary(tmp_path: Path, monkeypatch, capsys) -> None:
    """Der echte Weg der CI ohne Tracker-Hydratation: tools/bd da, Binary fehlt.

    Der Test darueber reicht die Ausnahme von Hand herein; hier laeuft der
    Wrapper wirklich, in einer Umgebung ohne bd. Ohne die Unterscheidung am
    Exit-Code endete genau diese Lage in Exit 2 statt im benennbaren Exit 3
    (bead 4t8).
    """
    import render_beads_export as rbe

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setattr(rbe, "EXPORT", tmp_path / "issues.jsonl")
    assert rbe.main(["--check"]) == 3
    assert "NICHT GEMESSEN" in capsys.readouterr().out


# --- reproduzierbarer Export (coding-harness-1jg.1) -------------------------

_ZEILE_OHNE_LEASE = '{"id":"x-1","status":"open","owner":"\\u003cjemand\\u003e","title":"a \\u0026 b"}'
_ZEILE_MIT_LEASE = (
    '{"id":"x-2","status":"in_progress","heartbeat_at":"2026-09-19T13:36:50Z",'
    '"lease_expires_at":"2026-09-19T13:41:50Z","title":"\\u003cin Arbeit\\u003e"}'
)


def test_the_render_omits_machine_local_lease_fields() -> None:
    """Zwei Maschinen rendern aus demselben Stand dieselben Bytes — ohne Lease-Felder."""
    import json

    import render_beads_export as rbe

    aus = rbe._ohne_maschinenlokales(_ZEILE_OHNE_LEASE + "\n" + _ZEILE_MIT_LEASE + "\n")
    saetze = [json.loads(z) for z in aus.splitlines()]
    assert [s["id"] for s in saetze] == ["x-1", "x-2"], "Reihenfolge und Menge der Zeilen bleiben"
    for feld in rbe.MASCHINENLOKAL:
        assert all(feld not in s for s in saetze), f"{feld} steht noch im Render"
    assert aus.endswith("\n")


def test_the_render_leaves_every_other_byte_alone() -> None:
    """Eine Zeile ohne Lease geht unberuehrt durch; eine mit Lease verliert nur die Felder."""
    import render_beads_export as rbe

    aus = rbe._ohne_maschinenlokales(_ZEILE_OHNE_LEASE + "\n" + _ZEILE_MIT_LEASE + "\n").splitlines()
    assert aus[0] == _ZEILE_OHNE_LEASE, "eine Zeile ohne maschinenlokales Feld wurde umgeschrieben"
    assert aus[1] == '{"id":"x-2","status":"in_progress","title":"\\u003cin Arbeit\\u003e"}', (
        "die umgeschriebene Zeile traegt nicht die Schreibweise des Trackers"
    )


def test_the_render_refuses_a_line_it_cannot_reproduce(tmp_path: Path, monkeypatch, capsys) -> None:
    """Aendert der Tracker seine Schreibweise, wird verworfen statt still umgeschrieben."""
    import render_beads_export as rbe

    fremd = '{"id": "x-3", "status": "in_progress", "heartbeat_at": "2026-09-19T13:36:50Z"}'
    with pytest.raises(rbe.NichtReproduzierbar):
        rbe._ohne_maschinenlokales(fremd + "\n")

    committed = tmp_path / "issues.jsonl"
    committed.write_text(_ZEILE_OHNE_LEASE + "\n", encoding="utf-8")
    monkeypatch.setattr(rbe, "EXPORT", committed)

    def wirft(_p: Path) -> None:
        raise rbe.NichtReproduzierbar("Zeile 1 (x-3)")

    monkeypatch.setattr(rbe, "_render_nach", wirft)
    assert rbe.main([]) == 1
    assert committed.read_text(encoding="utf-8") == _ZEILE_OHNE_LEASE + "\n", "ein verworfener Render hat geschrieben"
    assert "verworfen" in capsys.readouterr().out


def test_the_omitted_keys_are_named_once() -> None:
    """Die Liste steht im Renderer und nirgends sonst — sonst driften zwei Listen.

    Gesucht wird der blosse Feldname, in jeder Schreibweise, in Scripts und
    Entscheidungsdateien. `tests/` bleibt aussen vor: dort stehen die Felder
    als Daten in den Stellvertreter-Zeilen, nicht als zweite Liste.
    """
    import render_beads_export as rbe

    assert rbe.MASCHINENLOKAL, "eine leere Liste misst nichts"
    kandidaten = sorted((REPO_ROOT / "scripts").rglob("*.py")) + sorted((REPO_ROOT / "decisions").rglob("*.y*ml"))
    assert any(p.name == "render_beads_export.py" for p in kandidaten), "die Suche sieht den Renderer nicht"
    treffer = sorted(
        {
            str(p.relative_to(REPO_ROOT))
            for p in kandidaten
            if any(feld in p.read_text(encoding="utf-8") for feld in rbe.MASCHINENLOKAL)
        }
    )
    assert treffer == ["scripts/render_beads_export.py"], f"die Felder stehen in mehr als einer Datei: {treffer}"


def test_a_record_with_a_raw_line_separator_stays_one_line() -> None:
    """U+0085 und U+2028 stehen roh in Texten; nur `\\n` trennt Saetze (Review F-1)."""
    import render_beads_export as rbe

    roh = '{"id":"x-9","status":"open","title":"Zeile\u0085zwei\u2028drei"}\n' + _ZEILE_MIT_LEASE + "\n"
    aus = rbe._ohne_maschinenlokales(roh)
    assert aus.split("\n")[0] == roh.split("\n")[0], "ein Satz ohne Lease wurde zerschnitten oder umgeschrieben"
    assert aus.count("\n") == 2


def test_the_omission_is_wired_into_the_one_render_path(tmp_path: Path, monkeypatch) -> None:
    """Schreibweg und --check rendern beide ueber `_render_nach` — dort muss die Auslassung sitzen.

    Ein Stellvertreter fuer `tools/bd` schreibt eine Zeile mit Lease; liefe die
    Auslassung nur in der Hilfsfunktion und nicht im Renderweg, bliebe sie stehen.
    """
    import render_beads_export as rbe

    stellvertreter = tmp_path / "bd"
    stellvertreter.write_text(f"#!/bin/sh\nprintf '%s\\n' '{_ZEILE_MIT_LEASE}' > \"$3\"\n", encoding="utf-8")
    stellvertreter.chmod(0o755)
    monkeypatch.setattr(rbe, "BD", stellvertreter)
    ziel = tmp_path / "render.jsonl"
    rbe._render_nach(ziel)
    text = ziel.read_text(encoding="utf-8")
    assert all(feld not in text for feld in rbe.MASCHINENLOKAL), "der Renderweg laesst die Lease-Felder stehen"
    assert '"id":"x-2"' in text
