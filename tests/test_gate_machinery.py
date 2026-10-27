"""Mutation proofs and coverage of the gate machinery (RB-G4, bead bo0).

A test that only asserts that it is green today checks the world and not the
gate. For every self-built gate this file holds the run that turns it red — and
for the remaining scripts the execution that the ratchets (OHNE_AUFRUFER /
OHNE_TEST in ci_gates.py) demand.
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
# gate-schema — the gate that reads the gate file itself
# --------------------------------------------------------------------------


def test_gate_schema_gate_goes_red_when_an_entry_has_no_command() -> None:
    import ci_gates

    schlecht = {
        "schema_version": 2,
        "gates": [
            {
                "id": "kaputt",
                "title": "weder Kommando noch Action",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "both",
                "reason": "a seed that demonstrates the schema error",
            }
        ],
    }
    befunde = ci_gates.validate_schema(schlecht)
    assert befunde, "a gate without command and without action must fail the schema"
    assert any("kaputt" in b for b in befunde)


def test_gate_schema_gate_accepts_the_real_gate_file() -> None:
    import ci_gates

    doc = yaml.safe_load((REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
    assert ci_gates.validate_schema(doc) == []


def test_gate_schema_gate_rejects_a_non_boolean_needs_tracker() -> None:
    """Bead 4t8: needs_tracker controls a CI step — a text there would be silence."""
    import ci_gates

    schlecht = {
        "schema_version": 2,
        "gates": [
            {
                "id": "kaputt",
                "title": "needs_tracker als Text",
                "command": "python3 -c 'print(1)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "both",
                "needs_tracker": "yes",
                "reason": "a seed that demonstrates the schema error",
            }
        ],
    }
    befunde = ci_gates.validate_schema(schlecht)
    assert befunde, "needs_tracker must be a boolean"
    assert any("needs_tracker" in b for b in befunde)


def test_gate_schema_gate_rejects_an_unknown_placement() -> None:
    """Bead 1jg.2: placement is closed — a fourth word is a schema error."""
    import ci_gates

    schlecht = {
        "schema_version": 2,
        "gates": [
            {
                "id": "kaputt",
                "title": "placement als Freitext",
                "command": "python3 -c 'print(1)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "manchmal",
                "reason": "a seed that demonstrates the schema error",
            }
        ],
    }
    befunde = ci_gates.validate_schema(schlecht)
    assert befunde, "placement must follow the closed vocabulary"
    assert any("placement" in b for b in befunde)


def test_gate_schema_gate_requires_a_placement() -> None:
    """Bead 1jg.2: without placement the place of measuring would be implicit knowledge again."""
    import ci_gates

    schlecht = {
        "schema_version": 2,
        "gates": [
            {
                "id": "kaputt",
                "title": "ohne placement",
                "command": "python3 -c 'print(1)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "reason": "a seed that demonstrates the schema error",
            }
        ],
    }
    befunde = ci_gates.validate_schema(schlecht)
    assert befunde, "placement is mandatory"
    assert any("placement" in b for b in befunde)


def test_the_generated_workflow_leaves_writer_only_gates_out(tmp_path: Path, monkeypatch) -> None:
    """Bead 1jg.2: writer-only gates are measured only by the writing machine —
    the derived ci.yml keeps them out by declaration, and a writer-only gate with
    needs_tracker triggers no hydration there either."""
    import ci_gates

    doc = {
        "schema_version": 2,
        "tools": {"python": ["3.11", "3.12"]},
        "gates": [
            {
                "id": "lauf-ueberall",
                "title": "misst ueberall",
                "command": "python3 -c 'print(1)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "both",
                "reason": "benchmark of the seed",
            },
            {
                "id": "nur-schreiber",
                "title": "misst nur an der Schreibmaschine",
                "command": "python3 -c 'print(2)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "writer",
                "needs_tracker": True,
                "reason": "seed for the declared omission",
            },
        ],
    }
    gate_datei = tmp_path / "gates.yaml"
    gate_datei.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(ci_gates, "GATE_FILE", gate_datei)

    ableitung = ci_gates.generate_ci()
    assert "nur-schreiber" not in ableitung, "writer-only gates do not belong in CI"
    assert "lauf-ueberall" in ableitung
    assert "Hydrate the tracker" not in ableitung, (
        "a writer-only gate with needs_tracker must not trigger the CI hydration"
    )


def test_the_local_command_list_skips_hosted_only_gates(tmp_path: Path, monkeypatch, capsys) -> None:
    """Bead 1jg.2: hosted-only gates cannot be measured by the local run — it
    leaves them out by declaration instead of letting them run impossibly red."""
    import ci_gates

    doc = {
        "schema_version": 2,
        "tools": {"python": ["3.11", "3.12"]},
        "gates": [
            {
                "id": "lauf-ueberall",
                "title": "misst ueberall",
                "command": "python3 -c 'print(1)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "both",
                "reason": "benchmark of the seed",
            },
            {
                "id": "nur-ci",
                "title": "misst nur in der gehosteten CI",
                "command": "python3 -c 'print(2)'",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "hosted",
                "reason": "seed for the declared omission",
            },
        ],
    }
    gate_datei = tmp_path / "gates.yaml"
    gate_datei.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(ci_gates, "GATE_FILE", gate_datei)
    monkeypatch.setattr(sys, "argv", ["ci_gates.py", "--commands", "--job", "verify", "--placement", "lokal", "--tsv"])

    assert ci_gates.main() == 0
    ausgegeben = capsys.readouterr().out
    assert "nur-ci" not in ausgegeben, "hosted-only gates do not belong in the local run"
    assert "lauf-ueberall" in ausgegeben


# --------------------------------------------------------------------------
# ci-drift — the derived ci.yml against the hand edit
# --------------------------------------------------------------------------


def test_ci_drift_gate_goes_red_when_the_workflow_is_hand_edited(tmp_path: Path, monkeypatch) -> None:
    import ci_gates

    soll = ci_gates.generate_ci()
    ziel = tmp_path / "ci.yml"

    monkeypatch.setattr(ci_gates, "CI_FILE", ziel)
    ziel.write_text(soll, encoding="utf-8")
    assert ci_gates.check_ci() == 0, "the exact derivation must pass as green"

    hand = soll.replace("cron:", "cron-handgriff:")
    ziel.write_text(hand, encoding="utf-8")
    assert ci_gates.check_ci() == 1, "a hand edit in the derived file must turn it red"


def test_the_pinned_ci_gates_cli_runs_green_against_the_real_gate_file() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/ci_gates.py", "--check-schema"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


# --------------------------------------------------------------------------
# docs-links — frontmatter, links, anchors
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
    assert erg.returncode in (0, 1), erg.stdout + erg.stderr  # green or findings, never a crash


# --------------------------------------------------------------------------
# bead-export — the rendered tracker
# --------------------------------------------------------------------------


def test_check_bead_export_gate_goes_red_when_a_line_is_broken(tmp_path: Path) -> None:
    import check_bead_export

    kaputt = tmp_path / "issues.jsonl"
    kaputt.write_text('{"id": "a", "status": "open"}\n{kaputt\n', encoding="utf-8")
    befunde = check_bead_export.run(kaputt)
    assert befunde, "a broken line must yield a finding"

    ok = tmp_path / "ok.jsonl"
    ok.write_text('{"id": "a", "status": "open"}\n', encoding="utf-8")
    assert check_bead_export.run(ok) == []


def test_check_bead_export_gate_refuses_an_empty_export(tmp_path: Path) -> None:
    """Bead 4t8: an export over zero lines measures nothing — that is a finding.

    Until 2026-09-22 the gate was green here: every line check ran over zero
    lines and reported completeness over an empty set. Exactly the gap that the
    interview calls "floor: true is not empty".
    """
    import check_bead_export

    leer = tmp_path / "leer.jsonl"
    leer.write_text("\n\n", encoding="utf-8")
    befunde = check_bead_export.run(leer)
    assert befunde, "an empty export must yield a finding"
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
# The remaining scripts — the execution that the ratchets demand
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


def test_the_ramp_valve_gate_goes_red_when_a_valve_is_due(monkeypatch: pytest.MonkeyPatch) -> None:
    """A valve whose condition holds and still sits open turns the gate red.

    Until 2026-10-25 the `ramp-valves` gate counted as covered because files
    named its script beside unrelated mutation tests; none seeded a fault into
    it (bead coding-harness-a05).
    """
    import ramp_valves
    from _verdict import Ramp

    waiting = Ramp(name="seeded-waiting", condition="a condition that does not hold", predicate=lambda: False)
    due = Ramp(name="seeded-due", condition="a condition that holds", predicate=lambda: True)
    monkeypatch.setattr(sys, "argv", ["ramp_valves.py"])

    monkeypatch.setattr(ramp_valves, "valves", lambda: [waiting])
    assert ramp_valves.main() == 0, "precondition: a valve that still waits keeps the gate green"
    monkeypatch.setattr(ramp_valves, "valves", lambda: [waiting, due])
    assert ramp_valves.main() == 1, "a due valve left open did not turn the gate red"


# --------------------------------------------------------------------------
# dangling-beads — cited ticket IDs resolve in the export
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
# decision-continuity — a decision disappears only visibly (question 5)
# --------------------------------------------------------------------------


def test_decision_continuity_gate_goes_red_when_an_id_is_missing(tmp_path: Path) -> None:
    import check_decision_continuity

    ziel = tmp_path / "target.md"
    ziel.write_text(
        "# Target\n\n## Decision continuity\n\n| Decision | Disposition |\n|---|---|\n| D-1 — vocabulary | Retain |\n",
        encoding="utf-8",
    )
    befunde = check_decision_continuity.run(ziel, tmp_path)
    assert any("D-17 missing" in b for b in befunde), befunde
    assert any("D-2 missing" in b for b in befunde), befunde
    assert any("ADR missing" in b for b in befunde), befunde


def test_the_real_decision_continuity_check_runs_green_here() -> None:
    erg = subprocess.run(
        [sys.executable, "scripts/check_decision_continuity.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert erg.returncode == 0, erg.stdout + erg.stderr


def test_decision_continuity_is_red_while_its_target_is_missing(tmp_path: Path) -> None:
    """Bead 4t8: floor: true — a missing target is exit 3, not a silent green.

    Until the #8 merge this situation reported "SKIP" (exit 0) and named as the
    reason a state that has since become the past. A gate whose target is
    missing cannot measure — and a floor gate that does not measure fails.
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


# --- reproducible export (coding-harness-1jg.1) -----------------------------

_ZEILE_OHNE_LEASE = '{"id":"x-1","status":"open","owner":"\\u003cjemand\\u003e","title":"a \\u0026 b"}'
_ZEILE_MIT_LEASE = (
    '{"id":"x-2","status":"in_progress","heartbeat_at":"2026-09-19T13:36:50Z",'
    '"lease_expires_at":"2026-09-19T13:41:50Z","title":"\\u003cin Arbeit\\u003e"}'
)


def test_the_render_omits_machine_local_lease_fields() -> None:
    """Two machines render the same bytes from the same state — without lease fields."""
    import json

    import render_beads_export as rbe

    aus = rbe._ohne_maschinenlokales(_ZEILE_OHNE_LEASE + "\n" + _ZEILE_MIT_LEASE + "\n")
    saetze = [json.loads(z) for z in aus.splitlines()]
    assert [s["id"] for s in saetze] == ["x-1", "x-2"], "order and number of the lines stay"
    for feld in rbe.MASCHINENLOKAL:
        assert all(feld not in s for s in saetze), f"{feld} is still in the render"
    assert aus.endswith("\n")


def test_the_render_leaves_every_other_byte_alone() -> None:
    """A line without a lease passes through untouched; one with a lease loses only the fields."""
    import render_beads_export as rbe

    aus = rbe._ohne_maschinenlokales(_ZEILE_OHNE_LEASE + "\n" + _ZEILE_MIT_LEASE + "\n").splitlines()
    assert aus[0] == _ZEILE_OHNE_LEASE, "a line without a machine-local field was rewritten"
    assert aus[1] == '{"id":"x-2","status":"in_progress","title":"\\u003cin Arbeit\\u003e"}', (
        "the rewritten line does not carry the tracker's spelling"
    )


def test_the_render_refuses_a_line_it_cannot_reproduce(tmp_path: Path, monkeypatch, capsys) -> None:
    """If the tracker changes its spelling, the render is discarded instead of silently rewritten."""
    import render_beads_export as rbe

    fremd = '{"id": "x-3", "status": "in_progress", "heartbeat_at": "2026-09-19T13:36:50Z"}'
    with pytest.raises(rbe.NichtReproduzierbar):
        rbe._ohne_maschinenlokales(fremd + "\n")

    committed = tmp_path / "issues.jsonl"
    committed.write_text(_ZEILE_OHNE_LEASE + "\n", encoding="utf-8")
    monkeypatch.setattr(rbe, "EXPORT", committed)

    def wirft(_p: Path) -> None:
        raise rbe.NichtReproduzierbar("Line 1 (x-3)")

    monkeypatch.setattr(rbe, "_render_nach", wirft)
    assert rbe.main([]) == 1
    assert committed.read_text(encoding="utf-8") == _ZEILE_OHNE_LEASE + "\n", "a discarded render has written"
    assert "discarded" in capsys.readouterr().out


def test_the_omitted_keys_are_named_once() -> None:
    """The list stands in the renderer and nowhere else — otherwise two lists drift.

    The bare field name is searched, in every spelling, in scripts and decision
    files. `tests/` is left out: there the fields stand as data in the stand-in
    lines, not as a second list.
    """
    import render_beads_export as rbe

    assert rbe.MASCHINENLOKAL, "an empty list measures nothing"
    kandidaten = sorted((REPO_ROOT / "scripts").rglob("*.py")) + sorted((REPO_ROOT / "decisions").rglob("*.y*ml"))
    assert any(p.name == "render_beads_export.py" for p in kandidaten), "the search does not see the renderer"
    treffer = sorted(
        {
            str(p.relative_to(REPO_ROOT))
            for p in kandidaten
            if any(feld in p.read_text(encoding="utf-8") for feld in rbe.MASCHINENLOKAL)
        }
    )
    assert treffer == ["scripts/render_beads_export.py"], f"the fields stand in more than one file: {treffer}"


def test_a_record_with_a_raw_line_separator_stays_one_line() -> None:
    """U+0085 and U+2028 stand raw in texts; only `\\n` separates records (review F-1)."""
    import render_beads_export as rbe

    roh = '{"id":"x-9","status":"open","title":"Zeile\u0085zwei\u2028drei"}\n' + _ZEILE_MIT_LEASE + "\n"
    aus = rbe._ohne_maschinenlokales(roh)
    assert aus.split("\n")[0] == roh.split("\n")[0], "a record without a lease was cut up or rewritten"
    assert aus.count("\n") == 2


def test_the_omission_is_wired_into_the_one_render_path(tmp_path: Path, monkeypatch) -> None:
    """The write path and --check both render through `_render_nach` — the omission must sit there.

    A stand-in for `tools/bd` writes a line with a lease; if the omission ran
    only in the helper function and not in the render path, the lease would stay.
    """
    import render_beads_export as rbe

    stellvertreter = tmp_path / "bd"
    stellvertreter.write_text(f"#!/bin/sh\nprintf '%s\\n' '{_ZEILE_MIT_LEASE}' > \"$3\"\n", encoding="utf-8")
    stellvertreter.chmod(0o755)
    monkeypatch.setattr(rbe, "BD", stellvertreter)
    ziel = tmp_path / "render.jsonl"
    rbe._render_nach(ziel)
    text = ziel.read_text(encoding="utf-8")
    assert all(feld not in text for feld in rbe.MASCHINENLOKAL), "the render path leaves the lease fields in place"
    assert '"id":"x-2"' in text


def test_gate_schema_gate_holds_an_action_without_local_equivalent_to_hosted() -> None:
    """Bead 1jg.2: an action without a local equivalent measures only hosted — on
    both it would stand wrongly, and the local runner would silently leave it out."""
    import ci_gates

    def doc(placement: str) -> dict:
        return {
            "schema_version": 2,
            "tools": {"python": ["3.11", "3.12"]},
            "gates": [
                {
                    "id": "nur-action",
                    "title": "Marketplace-Action ohne lokale Entsprechung",
                    "action": "example/no-local-equivalent@v1",
                    "job": "verify",
                    "enforcement": "advisory",
                    "floor": False,
                    "placement": placement,
                    "reason": "a seed that demonstrates the schema error",
                }
            ],
        }

    assert any("hosted" in b for b in ci_gates.validate_schema(doc("both")))
    assert any("hosted" in b for b in ci_gates.validate_schema(doc("writer")))
    assert ci_gates.validate_schema(doc("hosted")) == []


def test_placement_rule_lives_in_one_predicate() -> None:
    """Bead 1jg.2: the derivation and the local runner ask the same function."""
    import ci_gates

    assert ci_gates.misst_in({"placement": "both"}, "lokal")
    assert ci_gates.misst_in({"placement": "both"}, "ci")
    assert not ci_gates.misst_in({"placement": "hosted"}, "lokal")
    assert ci_gates.misst_in({"placement": "hosted"}, "ci")
    assert ci_gates.misst_in({"placement": "writer"}, "lokal")
    assert not ci_gates.misst_in({"placement": "writer"}, "ci")
