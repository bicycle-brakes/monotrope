"""The guard before every agent session — and its five counter-checks.

**The incident it stands against.** A worktree sat on a detached HEAD at the
*old* review base. The agent worked from a commit that predated the last
round; the commits after it were invisible to it, and the diff it read was
not the diff that merged later. Nothing about this was red — git does exactly
what it is asked to do.

Hence the precondition is fail-closed: every suspicious state stops. The only
self-repair is a detached HEAD on an *ancestor* of the expected branch —
nothing can have been lost there.

Every rule has its counter-check here. A guard that was never red is not one:
its behaviour would never have been established (RB-G7).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKRIPT = REPO_ROOT / "scripts" / "check_worktree_state.sh"


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _lauf(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["bash", str(SKRIPT), *args], capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A real mini repo with three commits — never the project's tree."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "--initial-branch=main", "--quiet")
    _git(r, "config", "user.email", "test@example.invalid")
    _git(r, "config", "user.name", "Test")
    for i in range(3):
        (r / f"datei-{i}.txt").write_text(f"Inhalt {i}\n", encoding="utf-8")
        _git(r, "add", "-A")
        _git(r, "commit", "-m", f"commit {i}", "--quiet")
    return r


def test_the_guard_exists_and_is_executable() -> None:
    """Without the file, everything below checks nothing (RB-G7)."""
    assert SKRIPT.is_file(), f"{SKRIPT} is missing"
    assert SKRIPT.stat().st_mode & 0o111, "guard is not executable"


def test_a_healthy_worktree_passes(repo: Path) -> None:
    """The counter-check to the counter-check: green must really occur."""
    e = _lauf(str(repo), "main")
    assert e.returncode == 0, e.stderr
    assert "usable" in e.stdout


def test_any_branch_mode_passes_on_a_branch(repo: Path) -> None:
    """`-` allows any branch — but it must be a branch."""
    e = _lauf(str(repo), "-")
    assert e.returncode == 0, e.stderr


def test_a_missing_directory_is_refused(tmp_path: Path) -> None:
    e = _lauf(str(tmp_path / "gibt-es-nicht"), "main")
    assert e.returncode == 1
    assert "no such directory" in e.stderr


def test_a_directory_that_is_no_repository_is_refused(tmp_path: Path) -> None:
    """A directory without git is not a worktree, even if it exists."""
    d = tmp_path / "leer"
    d.mkdir()
    e = _lauf(str(d), "main")
    assert e.returncode == 1
    assert "not a git worktree" in e.stderr


def test_the_wrong_branch_is_refused(repo: Path) -> None:
    e = _lauf(str(repo), "ein-anderer-zweig")
    assert e.returncode == 1
    assert "expected 'ein-anderer-zweig'" in e.stderr


def test_a_detached_head_on_an_ancestor_is_reattached(repo: Path) -> None:
    """The ONLY self-repair — and only because nothing can be lost."""
    _git(repo, "checkout", "--quiet", "HEAD~1")
    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD") == "HEAD"
    e = _lauf(str(repo), "main")
    assert e.returncode == 0, e.stderr
    assert "reattaching" in e.stdout
    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD") == "main"


def test_a_detached_head_off_the_branch_is_a_hard_stop(repo: Path) -> None:
    """A commit beside the branch: work there would land on no branch."""
    _git(repo, "checkout", "--quiet", "HEAD~1")
    (repo / "seitenast.txt").write_text("neben dem Zweig\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seitenast", "--quiet")
    e = _lauf(str(repo), "main")
    assert e.returncode == 1
    assert "NOT on main" in e.stderr


def test_a_detached_head_is_refused_in_any_branch_mode(repo: Path) -> None:
    """`-` must not let a detached HEAD through.

    Without an expected branch there is no tip to compare against — reattaching
    would mean guessing which branch was meant. So: hard stop.
    """
    _git(repo, "checkout", "--quiet", "HEAD~1")
    e = _lauf(str(repo), "-")
    assert e.returncode == 1
    assert "detached HEAD" in e.stderr
    assert "no branch" in e.stderr, "the message must name the reason, not 'NOT on -'"
    assert "NOT on -" not in e.stderr


def test_a_rebase_in_progress_is_refused(repo: Path) -> None:
    """A half-finished rebase is not a state in which an agent starts."""
    marker = Path(_git(repo, "rev-parse", "--git-path", "rebase-merge"))
    if not marker.is_absolute():
        marker = repo / marker
    marker.mkdir(parents=True)
    e = _lauf(str(repo), "main")
    assert e.returncode == 1
    assert "rebase-merge in progress" in e.stderr


def test_head_moved_backward_is_refused(repo: Path) -> None:
    """The incident itself: HEAD is an ancestor of the recorded state."""
    aufgezeichnet = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", "HEAD~2", "--quiet")
    e = _lauf(str(repo), "main", aufgezeichnet)
    assert e.returncode == 1
    assert "moved BACKWARD" in e.stderr


def test_moving_forward_is_allowed(repo: Path) -> None:
    """The counter-check: forward is the normal case and must pass."""
    alt = _git(repo, "rev-parse", "HEAD~2")
    e = _lauf(str(repo), "main", alt)
    assert e.returncode == 0, e.stderr


def test_an_unknown_recorded_commit_is_refused(repo: Path) -> None:
    """Record and tree contradict each other — this is explained, not guessed."""
    e = _lauf(str(repo), "main", "0" * 40)
    assert e.returncode == 1
    assert "does not exist" in e.stderr
