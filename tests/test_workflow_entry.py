"""The entry into the workflow — the scaffold of a change folder.

`scripts/new_change.py` is the documented entry into phase 1
(docs/WORKFLOW.md). Until 2026-09-21 it blocked silently here: its guard
`scripts/check_worktree_state.sh` had not travelled along when the mechanism
moved out of portfolio-agentic-engineering (bead coding-harness-cke) — every
change started by hand.

The wrapper and make-target shortcuts measure here since bead
coding-harness-i0l. The Makefile and `.claude/commands/` are inventory of
this repository and do not travel with the kit, so those cases skip where
their object is absent — the travelling copy stays green without a new
`REIST_NICHT` entry, whose cap may only sink.

Every rule here stands next to its counter-check. A check that was never red
measures nothing — the missing guard learned that the hard way.
"""

from __future__ import annotations

import json
import shutil
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


# --------------------------------------------------------------------------
#  The promised shortcuts (bead coding-harness-i0l): `make change`,
#  `make index`, `make help` and `/workflow-start`. They delegate to the
#  entry script and the registry; nothing here restates their behavior.
# --------------------------------------------------------------------------

MAKEFILE = REPO_ROOT / "Makefile"
COMMAND = REPO_ROOT / ".claude" / "commands" / "workflow-start.md"

MAKE_SKIP = pytest.mark.skipif(
    not MAKEFILE.is_file() or shutil.which("make") is None,
    reason="the Makefile is inventory of this repository and does not travel (kit probe)",
)
COMMAND_SKIP = pytest.mark.skipif(
    not COMMAND.is_file(),
    reason=".claude/commands is inventory of this repository and does not travel (kit probe)",
)

# The entry script imports these from `scripts/`; a fixture tree that runs the
# real recipes carries its own copies.
ENTRY_SCRIPTS = ("new_change.py", "plans_registry.py", "_verdict.py", "bead_render.py", "check_worktree_state.sh")


def _fixture_tree(tmp_path: Path, name: str = "tree") -> Path:
    """A full isolated tree: entry scripts, Makefile, plans/, bead export, git.

    The recipes run against this tree, never against the shared checkout or
    its tracker; the bead export is preset through `BEAD_RENDER`, the way CI
    does it (D-52). A test that compares a recipe's work against the direct
    entry builds two trees under different names — one name would alias both
    handles to the same directory.
    """
    tree = tmp_path / name
    (tree / "scripts").mkdir(parents=True)
    for name in ENTRY_SCRIPTS:
        shutil.copy(REPO_ROOT / "scripts" / name, tree / "scripts" / name)
    shutil.copy(MAKEFILE, tree / "Makefile")
    (tree / "plans" / "changes").mkdir(parents=True)
    (tree / "plans" / "specs").mkdir()
    _write_bead_export(tree, {OPEN_BEAD: "open", CLOSED_BEAD: "closed"})
    _init_git(tree)
    return tree


def _controlled_python(tree: Path, log: Path) -> None:
    """A `python3` that logs every invocation and then runs the real interpreter.

    The delegation tests read the log line: the recipe must start the entry
    script or the registry as the docs promise, not something of its own.
    """
    wrapper = tree / "bin" / "python3"
    wrapper.parent.mkdir()
    wrapper.write_text(f'#!/bin/sh\necho "$@" >> "{log}"\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    wrapper.chmod(0o755)


def _run_make(tree: Path, log: Path, *args: str) -> subprocess.CompletedProcess:
    """A real `make` run inside the tree, with the controlled python3 first on the path.

    The log starts empty: whatever it holds afterwards, the controlled
    python3 appended — an invocation. A recipe that never starts one leaves
    it at zero bytes, and that is what the no-side-effect cases read.
    """
    log.touch()
    make = shutil.which("make")
    assert make, "precondition: make is on the path"
    env = {
        "HOME": str(tree.parent / "home"),
        "PATH": f"{tree / 'bin'}:/usr/bin:/bin",
        "BEAD_RENDER": str(tree / ".beads" / "issues.jsonl"),
        # Bytecode caches in scripts/__pycache__/ are interpreter residue, not
        # tree state — the tree-preservation cases measure the latter.
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    return subprocess.run([make, *args], cwd=tree, env=env, capture_output=True, text=True)


def _run_entry(tree: Path, *args: str) -> subprocess.CompletedProcess:
    """The documented entry, started directly — the behavior the recipes must reproduce."""
    env = {
        "HOME": str(tree.parent / "home"),
        "PATH": "/usr/bin:/bin",
        "BEAD_RENDER": str(tree / ".beads" / "issues.jsonl"),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    return subprocess.run(
        [sys.executable, "scripts/new_change.py", *args], cwd=tree, env=env, capture_output=True, text=True
    )


def _snapshot(root: Path) -> dict[str, bytes]:
    """Every file of the tree except git's own, as bytes — rejections change nothing."""
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.relative_to(root).parts[0] != ".git"
    }


@MAKE_SKIP
def test_make_change_delegates_to_scaffold(tmp_path: Path) -> None:
    """Criterion 3: the recipe produces exactly what the direct entry produces.

    Two identical trees; one runs `make change`, the other starts
    `scripts/new_change.py` the documented way. The scaffold, the bead link,
    the index and the next-phase guidance must match byte for byte — and the
    log line must show the recipe started the entry script.
    """
    make_tree, direct_tree = _fixture_tree(tmp_path, "make"), _fixture_tree(tmp_path, "direct")
    log = tmp_path / "aufrufe.log"
    _controlled_python(make_tree, log)

    ergebnis = _run_make(make_tree, log, "change", "NAME=probe", f"BEAD={OPEN_BEAD}")
    assert ergebnis.returncode == 0, ergebnis.stderr + ergebnis.stdout

    direkt = _run_entry(direct_tree, "probe", "--bead", OPEN_BEAD)
    assert direkt.returncode == 0, direkt.stderr + direkt.stdout

    research = make_tree / "plans" / "changes" / "probe" / "research.md"
    assert research.is_file(), "the recipe created no scaffold"
    assert sorted(p.name for p in (make_tree / "plans" / "changes" / "probe").iterdir()) == ["research.md"]
    assert research.read_bytes() == (direct_tree / "plans" / "changes" / "probe" / "research.md").read_bytes()
    index_bytes = make_tree.joinpath("plans", "INDEX.md").read_bytes()
    assert index_bytes == direct_tree.joinpath("plans", "INDEX.md").read_bytes(), "the recipe left a stale index"

    scaffold = research.read_text(encoding="utf-8")
    assert OPEN_BEAD in scaffold, "the scaffold lost its bead link"
    assert "01-explore" in scaffold, "the scaffold lost the pointer to phase 1"

    aufrufe = log.read_text(encoding="utf-8")
    assert "scripts/new_change.py" in aufrufe, f"the recipe did not start the entry script: {aufrufe!r}"
    assert "--bead" in aufrufe and OPEN_BEAD in aufrufe


@MAKE_SKIP
@pytest.mark.parametrize(
    ("argv", "plant"),
    [
        (["change", f"BEAD={OPEN_BEAD}"], None),  # empty NAME
        (["change", "NAME=probe"], None),  # empty BEAD
        (["change", "NAME=probe", "BEAD=coding-harness-missing"], None),  # unknown bead
        (["change", "NAME=probe", f"BEAD={CLOSED_BEAD}"], None),  # closed bead
        (["change", "NAME=probe", f"BEAD={OPEN_BEAD}"], "duplicate"),  # name taken
        (["change", "NAME=probe", f"BEAD={OPEN_BEAD}"], "detached"),  # no branch
    ],
    ids=["empty-name", "empty-bead", "unknown-bead", "closed-bead", "duplicate-name", "detached-head"],
)
def test_make_change_rejections_preserve_tree(
    tmp_path: Path, argv: list[str], plant: str | None, request: pytest.FixtureRequest
) -> None:
    """Criterion 4: every rejection exits nonzero and leaves the tree byte for byte.

    A rejected request may not succeed, may not leave a new change folder and
    may not touch the index — not even where a folder already exists (the
    duplicate case) or the checkout stands on no branch.
    """
    tree = _fixture_tree(tmp_path)
    log = tmp_path / "aufrufe.log"
    _controlled_python(tree, log)
    if plant == "duplicate":
        ordner = tree / "plans" / "changes" / "probe"
        ordner.mkdir()
        (ordner / "research.md").write_text("taken\n", encoding="utf-8")
    elif plant == "detached":
        subprocess.run(
            ["git", "checkout", "--detach", "--quiet", "HEAD"],
            cwd=tree,
            check=True,
            capture_output=True,
            text=True,
        )
    davor = _snapshot(tree)

    ergebnis = _run_make(tree, log, *argv)
    assert ergebnis.returncode != 0, f"{request.node.callspec.id} succeeded: {ergebnis.stdout}"
    assert _snapshot(tree) == davor, f"{request.node.callspec.id} changed the tree"
    if "empty" in request.node.callspec.id:
        assert "usage" in ergebnis.stderr, "the empty-input refusal does not say what was missing"
        assert log.read_text(encoding="utf-8") == "", "the empty-input check still started the entry script"


@MAKE_SKIP
def test_make_index_delegates_to_registry(tmp_path: Path) -> None:
    """Criterion 5: `make index` regenerates the index from the registry — and forwards its failure."""
    tree = _fixture_tree(tmp_path)
    log = tmp_path / "aufrufe.log"
    _controlled_python(tree, log)

    direkt = _run_entry(tree, "probe", "--bead", OPEN_BEAD)
    assert direkt.returncode == 0, direkt.stderr + direkt.stdout

    index = tree / "plans" / "INDEX.md"
    aktuell = index.read_bytes()
    index.write_text("# stale\n", encoding="utf-8")

    ergebnis = _run_make(tree, log, "index")
    assert ergebnis.returncode == 0, ergebnis.stderr + ergebnis.stdout
    assert index.read_bytes() == aktuell, "the regenerated index differs from the registry's rendering"

    aufrufe = log.read_text(encoding="utf-8")
    assert "scripts/plans_registry.py" in aufrufe and "--index" in aufrufe, f"not delegated: {aufrufe!r}"

    # The recipe may not swallow a red delegate: without the registry, `make index` is red.
    (tree / "scripts" / "plans_registry.py").unlink()
    assert _run_make(tree, log, "index").returncode != 0, "a failing delegate was hidden"


@MAKE_SKIP
def test_make_help_lists_targets_without_side_effects(tmp_path: Path) -> None:
    """Criterion 6: help names every public target and its inputs — and runs nothing."""
    tree = _fixture_tree(tmp_path)
    log = tmp_path / "aufrufe.log"
    _controlled_python(tree, log)
    davor = _snapshot(tree)

    ergebnis = _run_make(tree, log, "help")
    assert ergebnis.returncode == 0, ergebnis.stderr
    assert _snapshot(tree) == davor, "help wrote something"
    assert log.read_text(encoding="utf-8") == "", "help invoked a command"

    zeilen = ergebnis.stdout.splitlines()
    for ziel in ("change", "index", "help", "verify", "test", "staleness", "gates", "leakcheck", "venv", "lock"):
        assert any(zeile.startswith(f"make {ziel}") for zeile in zeilen), f"help does not list {ziel}: {zeilen}"
    change = next(zeile for zeile in zeilen if zeile.startswith("make change"))
    assert "NAME=" in change and "BEAD=" in change, "help omits the required change inputs"


@COMMAND_SKIP
def test_workflow_start_delegates_to_scaffold(workflow) -> None:
    """Criterion 7: the command hands name and bead to the entry script — data, not instructions.

    The text contract is read here; running the command once inside Claude
    Code stays a phase-6 manual check and is not claimed by this test. What
    the test can run is the documented invocation against the scaffold
    fixture: the entry script the command names behaves as the command says.
    """
    text = COMMAND.read_text(encoding="utf-8")
    assert "scripts/new_change.py" in text, "the command does not name the entry script"
    assert "$ARGUMENTS" in text, "the command does not take its arguments from the invocation"
    assert "--bead" in text, "the command does not pass a bead"
    assert "usage" in text.lower(), "missing inputs are not answered with usage"
    assert "required" in text.lower(), "the command does not say which inputs are required"
    niedrig = text.lower()
    assert "mkdir" not in niedrig, "the command builds its own scaffold"
    assert "01-explore" not in text, "the command starts phase 1 itself"
    assert "plans_registry" not in text, "the command does the registry's work itself"

    # The documented invocation, run against the scaffold fixture.
    assert new_change.main(["probe", "--bead", OPEN_BEAD]) == 0
    assert (workflow / "changes" / "probe" / "research.md").is_file()

    # Missing input: usage, never an inferred identifier, no folder.
    with pytest.raises(SystemExit) as auf:
        new_change.main(["probe2"])
    assert auf.value.code != 0
    assert not (workflow / "changes" / "probe2").exists()
