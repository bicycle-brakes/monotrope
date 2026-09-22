"""Der Einstieg in den Arbeitsablauf — das Scaffold eines Change-Ordners.

`scripts/new_change.py` ist der dokumentierte Einstieg in Phase 1
(docs/WORKFLOW.md). Bis zum 2026-09-21 blockte er hier still: sein Waechter
`scripts/check_worktree_state.sh` war beim Umzug des Mechanismus aus
portfolio-agentic-engineering nicht mitgereist (Bead coding-harness-cke) —
jeder Change startete von Hand.

Die fuenf Wrapper- und Make-Target-Tests aus portfolio gehoeren zu einem
Startkommando, das es hier noch nicht gibt (Bead coding-harness-kkh); die
volle Verhaltensmenge steht in portfolio, `tests/test_workflow_entry.py`.

Jede Regel hier steht neben ihrer Gegenprobe. Eine Pruefung, die nie rot war,
misst nichts — der fehlende Guard hat das hier auf eigene Haut erfahren.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import new_change  # noqa: E402
import plans_registry as reg  # noqa: E402

# Platzhalter-IDs: das Drift-Gate (check_dangling_bead_ids.py) liest nur
# docs/**/*.md — diese Datei wird nie gescannt. Die Form folgt trotzdem dem
# Muster aus portfolio (Praefix + kurzes Suffix), damit eine spaetere
# Ausweitung des Gates nicht hier zuerst bunt wird.
OPEN_BEAD = "coding-harness-xyz"
CLOSED_BEAD = "coding-harness-abc"


def _write_bead_export(repo: Path, entries: dict[str, str]) -> None:
    beads_dir = repo / ".beads"
    beads_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({"id": bead_id, "status": status}) for bead_id, status in entries.items()]
    (beads_dir / "issues.jsonl").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _init_git(repo: Path) -> None:
    """Ein echter Arbeitsbaum, weil `new_change.py` seit dem 2026-09-10 einen verlangt.

    Der Aufruf prueft vor dem Schreiben, dass der Baum auf einem Zweig steht
    (`scripts/check_worktree_state.sh`). Ein `tmp_path` ohne git ist kein
    Arbeitsbaum — und die Pruefung deshalb stillzulegen waere die falsche
    Reparatur: dann liefe die Vorbedingung im Test nie, und ihr Ausfall waere
    genau hier unsichtbar.
    """
    run = lambda *a: subprocess.run(  # noqa: E731
        ["git", *a], cwd=repo, check=True, capture_output=True, text=True
    )
    run("init", "--initial-branch=main", "--quiet")
    run("config", "user.email", "test@example.invalid")
    run("config", "user.name", "Test")
    (repo / ".gitkeep").write_text("", encoding="utf-8")
    run("add", "-A")
    run("commit", "-m", "fixture", "--quiet")


@pytest.fixture
def workflow(tmp_path, monkeypatch):
    """Eigener plans/-Baum, eigener Bead-Export — nie der echte Baum dieses Repos."""
    _init_git(tmp_path)
    root = tmp_path / "plans"
    (root / "changes").mkdir(parents=True)
    (root / "specs").mkdir()
    monkeypatch.setattr(reg, "REPO", tmp_path)
    monkeypatch.setattr(reg, "PLANS", root)
    monkeypatch.setattr(reg, "INDEX", root / "INDEX.md")
    _write_bead_export(tmp_path, {OPEN_BEAD: "open", CLOSED_BEAD: "closed"})
    return root


def test_new_change_creates_the_folder_and_a_current_index(workflow) -> None:
    """Die Akzeptanz von cke, erste Haelfte: der Einstieg scaffoldet hier."""
    exit_code = new_change.main(["probe", "--bead", OPEN_BEAD])
    assert exit_code == 0
    assert (workflow / "changes" / "probe" / "research.md").is_file()
    assert reg.INDEX.is_file(), "der Index wurde nicht mitgerendert"


def test_new_change_refuses_a_closed_bead(workflow) -> None:
    """Ein neuer Ordner an einem geschlossenen Vorgang waere sofort DRIFT."""
    exit_code = new_change.main(["probe", "--bead", CLOSED_BEAD])
    assert exit_code == 2
    assert not (workflow / "changes" / "probe").exists(), "trotz geschlossenem Vorgang geschrieben"


def test_new_change_refuses_a_detached_head(workflow, tmp_path) -> None:
    """Die Gegenprobe zur Vorbedingung aus Schritt 2a.

    Ein Ordner, an einem losgeloesten HEAD angelegt, haengt an einem Commit, den
    kein Zweig haelt. Sichtbar wird das erst, wenn jemand ihn sucht — also haelt
    der Aufruf vorher an.
    """
    subprocess.run(
        ["git", "checkout", "--detach", "--quiet", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    exit_code = new_change.main(["probe", "--bead", OPEN_BEAD])
    assert exit_code == 2
    assert not (workflow / "changes" / "probe").exists(), "trotz BLOCK geschrieben"


@pytest.mark.usefixtures("workflow")
def test_the_precondition_is_actually_reached(capsys) -> None:
    """Gegenprobe zur Gegenprobe: der gesunde Fall meldet den Waechter NICHT.

    Sonst koennte der Test oben auch gruen sein, weil der Aufruf aus einem
    ganz anderen Grund blockt.
    """
    assert new_change.main(["probe", "--bead", OPEN_BEAD]) == 0
    assert "Arbeitsbaum ist nicht" not in capsys.readouterr().out


def test_a_missing_guard_blocks_the_entry(workflow, monkeypatch, capsys) -> None:
    """Der Akzeptanztest von cke: fehlt der Guard, blockt der Einstieg — nennend.

    Genau das geschah live: `new_change.py` verlangte den Waechter, der Waechter
    war beim Umzug nicht mitgereist, und der Einstieg blockte mit genau dieser
    Meldung — aber kein Test wusste davon. Der BLOCK muss nennen, was fehlt,
    nicht still scheitern; und er muss BLOCK sein, nicht Durchlassen.
    """
    fehlend = workflow / "gibt-es-nicht" / "check_worktree_state.sh"
    monkeypatch.setattr(new_change, "WAECHTER", fehlend)
    exit_code = new_change.main(["probe", "--bead", OPEN_BEAD])
    assert exit_code == 2
    ausgabe = capsys.readouterr().out
    assert "check_worktree_state.sh fehlt" in ausgabe, "der BLOCK muss die fehlende Datei beim Namen nennen"
    assert not (workflow / "changes" / "probe").exists(), "trotz fehlendem Guard geschrieben"
