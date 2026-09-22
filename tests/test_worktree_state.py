"""Der Waechter vor jeder Agentensitzung — und seine fuenf Gegenproben.

**Der Vorfall, gegen den er steht.** Ein Arbeitsbaum stand auf einem losgeloesten
HEAD an der *alten* Review-Basis. Der Agent arbeitete von einem Commit aus, der
vor der letzten Runde lag; die Commits danach waren fuer ihn unsichtbar, und der
Diff, den er las, war nicht der Diff, der spaeter mergte. Nichts daran war rot —
git tut genau das, worum es gebeten wird.

Deshalb ist die Vorbedingung fail-closed: jeder verdaechtige Zustand haelt an.
Die einzige Selbstreparatur ist ein losgeloester HEAD auf einem *Vorfahren* des
erwarteten Zweiges — dort kann nichts verloren gegangen sein.

Jede Regel hat hier ihre Gegenprobe. Ein Waechter, der nie rot war, ist keiner:
sein Verhalten waere nie festgestellt worden (RB-G7).
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
    """Ein echtes Mini-Repo mit drei Commits — nie der Baum des Projekts."""
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
    """Ohne die Datei prueft alles darunter nichts (RB-G7)."""
    assert SKRIPT.is_file(), f"{SKRIPT} fehlt"
    assert SKRIPT.stat().st_mode & 0o111, "Waechter ist nicht ausfuehrbar"


def test_a_healthy_worktree_passes(repo: Path) -> None:
    """Die Gegenprobe zur Gegenprobe: gruen muss auch wirklich vorkommen."""
    e = _lauf(str(repo), "main")
    assert e.returncode == 0, e.stderr
    assert "usable" in e.stdout


def test_any_branch_mode_passes_on_a_branch(repo: Path) -> None:
    """`-` laesst jeden Zweig zu — aber es ist ein Zweig."""
    e = _lauf(str(repo), "-")
    assert e.returncode == 0, e.stderr


def test_a_missing_directory_is_refused(tmp_path: Path) -> None:
    e = _lauf(str(tmp_path / "gibt-es-nicht"), "main")
    assert e.returncode == 1
    assert "no such directory" in e.stderr


def test_a_directory_that_is_no_repository_is_refused(tmp_path: Path) -> None:
    """Ein Verzeichnis ohne git ist kein Arbeitsbaum, auch wenn es existiert."""
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
    """Die EINZIGE Selbstreparatur — und nur, weil nichts verloren sein kann."""
    _git(repo, "checkout", "--quiet", "HEAD~1")
    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD") == "HEAD"
    e = _lauf(str(repo), "main")
    assert e.returncode == 0, e.stderr
    assert "reattaching" in e.stdout
    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD") == "main"


def test_a_detached_head_off_the_branch_is_a_hard_stop(repo: Path) -> None:
    """Ein Commit neben dem Zweig: Arbeit dort landete auf keinem Zweig."""
    _git(repo, "checkout", "--quiet", "HEAD~1")
    (repo / "seitenast.txt").write_text("neben dem Zweig\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seitenast", "--quiet")
    e = _lauf(str(repo), "main")
    assert e.returncode == 1
    assert "NOT on main" in e.stderr


def test_a_detached_head_is_refused_in_any_branch_mode(repo: Path) -> None:
    """`-` darf die Loesloesung nicht durchlassen.

    Ohne erwarteten Zweig gibt es keine Spitze zum Vergleichen — anzuhaengen
    hiesse raten, welcher Zweig gemeint war. Also: harter Halt.
    """
    _git(repo, "checkout", "--quiet", "HEAD~1")
    e = _lauf(str(repo), "-")
    assert e.returncode == 1
    assert "detached HEAD" in e.stderr
    assert "no branch" in e.stderr, "die Meldung muss den Grund nennen, nicht 'NOT on -'"
    assert "NOT on -" not in e.stderr


def test_a_rebase_in_progress_is_refused(repo: Path) -> None:
    """Ein halb fertiger Rebase ist kein Zustand, in dem ein Agent anfaengt."""
    marker = Path(_git(repo, "rev-parse", "--git-path", "rebase-merge"))
    if not marker.is_absolute():
        marker = repo / marker
    marker.mkdir(parents=True)
    e = _lauf(str(repo), "main")
    assert e.returncode == 1
    assert "rebase-merge in progress" in e.stderr


def test_head_moved_backward_is_refused(repo: Path) -> None:
    """Der Vorfall selbst: HEAD ist Vorfahr des aufgezeichneten Standes."""
    aufgezeichnet = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", "HEAD~2", "--quiet")
    e = _lauf(str(repo), "main", aufgezeichnet)
    assert e.returncode == 1
    assert "moved BACKWARD" in e.stderr


def test_moving_forward_is_allowed(repo: Path) -> None:
    """Die Gegenprobe: vorwaerts ist der Normalfall und muss durchgehen."""
    alt = _git(repo, "rev-parse", "HEAD~2")
    e = _lauf(str(repo), "main", alt)
    assert e.returncode == 0, e.stderr


def test_an_unknown_recorded_commit_is_refused(repo: Path) -> None:
    """Aufzeichnung und Baum widersprechen sich — das wird erklaert, nicht geraten."""
    e = _lauf(str(repo), "main", "0" * 40)
    assert e.returncode == 1
    assert "does not exist" in e.stderr
