"""The entry into the workflow — the scaffold of a change folder.

`scripts/new_change.py` is the documented entry into phase 1
(docs/WORKFLOW.md). Until 2026-09-21 it blocked silently here: its guard
`scripts/check_worktree_state.sh` had not travelled along when the mechanism
moved out of portfolio-agentic-engineering (bead coding-harness-cke) — every
change started by hand.

The five wrapper and make-target tests from portfolio belong to a start
command that does not exist here yet (bead coding-harness-kkh); the full set
of behaviour lives in portfolio, `tests/test_workflow_entry.py`.

Every rule here stands next to its counter-check. A check that was never red
measures nothing — the missing guard learned that the hard way.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import new_change  # noqa: E402
import plans_registry as reg  # noqa: E402

# Placeholder IDs: the drift gate (check_dangling_bead_ids.py) reads only
# docs/**/*.md — this file is never scanned. The shape still follows the
# pattern from portfolio (prefix + short suffix), so that a later widening of
# the gate does not light up here first.
OPEN_BEAD = "coding-harness-xyz"
CLOSED_BEAD = "coding-harness-abc"


def _write_bead_export(repo: Path, entries: dict[str, str]) -> None:
    beads_dir = repo / ".beads"
    beads_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({"id": bead_id, "status": status}) for bead_id, status in entries.items()]
    (beads_dir / "issues.jsonl").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _init_git(repo: Path) -> None:
    """A real worktree, because `new_change.py` has required one since 2026-09-10.

    Before writing, the call checks that the tree stands on a branch
    (`scripts/check_worktree_state.sh`). A `tmp_path` without git is not a
    worktree — and silencing the check for that reason would be the wrong
    repair: the precondition would then never run in the test, and its failure
    would be invisible right here.
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
    """Own plans/ tree, own bead export — never this repo's real tree."""
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
    """Acceptance of cke, first half: the entry scaffolds here."""
    exit_code = new_change.main(["probe", "--bead", OPEN_BEAD])
    assert exit_code == 0
    assert (workflow / "changes" / "probe" / "research.md").is_file()
    assert reg.INDEX.is_file(), "the index was not rendered along"
    # qd7: a new document is born current, or the check behind `frontmatter-current` would report it.
    scaffold = (workflow / "changes" / "probe" / "research.md").read_text(encoding="utf-8")
    assert f"\nupdated: {date.today().isoformat()}\n" in scaffold.split("\n---\n", 1)[0] + "\n"


def test_new_change_refuses_a_closed_bead(workflow) -> None:
    """A new folder on a closed item would be DRIFT at once."""
    exit_code = new_change.main(["probe", "--bead", CLOSED_BEAD])
    assert exit_code == 2
    assert not (workflow / "changes" / "probe").exists(), "written despite a closed item"


def test_new_change_refuses_a_detached_head(workflow, tmp_path) -> None:
    """The counter-check to the precondition from step 2a.

    A folder created on a detached HEAD hangs on a commit that no branch holds.
    That becomes visible only when someone looks for it — so the call stops
    beforehand.
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
    assert not (workflow / "changes" / "probe").exists(), "written despite BLOCK"


@pytest.mark.usefixtures("workflow")
def test_the_precondition_is_actually_reached(capsys) -> None:
    """Counter-check to the counter-check: the healthy case does NOT report the guard.

    Otherwise the test above could also be green because the call blocks for
    an entirely different reason.
    """
    assert new_change.main(["probe", "--bead", OPEN_BEAD]) == 0
    assert "Worktree is not" not in capsys.readouterr().out


def test_a_missing_guard_blocks_the_entry(workflow, monkeypatch, capsys) -> None:
    """The acceptance test of cke: if the guard is missing, the entry blocks — and says why.

    This is exactly what happened live: `new_change.py` required the guard, the
    guard had not travelled along in the move, and the entry blocked with
    exactly this message — but no test knew about it. The BLOCK must name what
    is missing, not fail silently; and it must be a BLOCK, not a pass-through.
    """
    fehlend = workflow / "gibt-es-nicht" / "check_worktree_state.sh"
    monkeypatch.setattr(new_change, "WAECHTER", fehlend)
    exit_code = new_change.main(["probe", "--bead", OPEN_BEAD])
    assert exit_code == 2
    ausgabe = capsys.readouterr().out
    assert "check_worktree_state.sh missing" in ausgabe, "the BLOCK must name the missing file"
    assert not (workflow / "changes" / "probe").exists(), "written despite a missing guard"
