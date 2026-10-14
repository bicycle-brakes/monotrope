"""The session scan and the status line — the arming behind the ⚠ (bead hit).

Until 2026-09-22 `IFS=$'\\t' read` let empty fields slide onto their
neighbours: a session without a name or status slid into the `kind` column,
counted as non-interactive and was never reported as a clash — the bead
verified this with three fake sessions (PR #10 review). This file keeps the
proof as a test: the producer (`hooks/session-scan.sh`, NUL-separated
fields), the consumer (`statusline.sh`, split by parameter expansion), and
the case end to end.

The subject itself (`tools/claude-code/`) is part of this repo and does not
travel with the kit — in the dry run this file therefore skips (skipif
below); it measures here.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN = REPO_ROOT / "tools" / "claude-code" / "hooks" / "session-scan.sh"
STATUSLINE = REPO_ROOT / "tools" / "claude-code" / "statusline.sh"

pytestmark = pytest.mark.skipif(
    not (SCAN.is_file() and STATUSLINE.is_file()),
    reason="tools/claude-code is part of this repo and does not travel (kit probe)",
)


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _session(
    home: Path,
    *,
    pid: int,
    sid: str,
    cwd: Path,
    name: str | None = None,
    status: str | None = None,
    kind: str = "interactive",
    start: str = "",
) -> None:
    """A fake session file, as Claude Code writes it to ~/.claude/sessions/.

    `procStart` is left empty on purpose: the scan compares it only when it
    is present, and a test that had to fake `ps` localisation would check the
    wrong thing.
    """
    satz = {
        "pid": pid,
        "sessionId": sid,
        "cwd": str(cwd),
        "name": name,
        "status": status,
        "kind": kind,
        "procStart": start,
    }
    (home / ".claude" / "sessions" / f"{pid}.json").write_text(json.dumps(satz), encoding="utf-8")


def _scan(home: Path, sid: str, cwd: Path) -> list[list[str]]:
    erg = subprocess.run(
        ["bash", str(home / ".claude" / "hooks" / "session-scan.sh"), sid, str(cwd)],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(home)},
    )
    assert erg.returncode == 0, erg.stderr
    # Python's split does not collapse empty fields — exactly the yardstick
    # the old `IFS=$'\t' read` broke on.
    return [zeile.split("\t") for zeile in erg.stdout.splitlines()]


@pytest.fixture
def werkstatt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fake HOME with the scan installed and an empty session registry."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    (home / ".claude" / "sessions").mkdir()
    shutil.copy2(SCAN, home / ".claude" / "hooks" / "session-scan.sh")
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A real mini repository with one commit — never this project's tree."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "--initial-branch=main", "--quiet")
    _git(r, "config", "user.email", "test@example.invalid")
    _git(r, "config", "user.name", "Test")
    (r / "datei.txt").write_text("x\n", encoding="utf-8")
    _git(r, "add", "-A")
    _git(r, "commit", "-m", "fixture", "--quiet")
    return r


def test_a_session_without_name_or_status_is_reported_and_never_shifts(werkstatt: Path, tmp_path: Path) -> None:
    """The bead case: empty fields do not shift columns.

    Before the fix, behind an empty name the status slid into the `kind`
    column — the session counted as non-interactive and was invisible, exactly
    when it was least allowed to be.
    """
    fremd = tmp_path / "fremd"
    fremd.mkdir()
    zweitprozess = subprocess.Popen(["sleep", "30"])
    try:
        _session(werkstatt, pid=os.getpid(), sid="f1", cwd=fremd)
        _session(
            werkstatt,
            pid=zweitprozess.pid,
            sid="f2",
            cwd=fremd,
            name="Andere",
            status="busy",
        )

        zeilen = _scan(werkstatt, "ich", fremd)
        assert len(zeilen) == 2, f"both sessions report: {zeilen}"

        leer = next(z for z in zeilen if z[3] == "f1")
        assert leer[0] == "other"
        assert leer[1] == "fremd", "label falls back to basename(cwd)"
        assert leer[2] == "", "a missing status stays an empty field, no shifting"
        assert leer[4] == str(fremd)

        voll = next(z for z in zeilen if z[3] == "f2")
        assert (voll[1], voll[2]) == ("Andere", "arbeitet")
    finally:
        zweitprozess.kill()
        zweitprozess.wait()


def test_a_clash_with_empty_fields_is_reported_as_a_clash(werkstatt: Path, repo: Path) -> None:
    """The consequence the bead means: a real clash must never be invisible."""
    _session(werkstatt, pid=os.getpid(), sid="klon", cwd=repo)  # name and status empty
    zeilen = _scan(werkstatt, "ich", repo)
    assert len(zeilen) == 1, zeilen
    assert zeilen[0][0] == "clash", f"same checkout not detected: {zeilen}"
    assert zeilen[0][3] == "klon"


def test_another_worktree_of_the_same_repo_is_a_sibling(werkstatt: Path, repo: Path, tmp_path: Path) -> None:
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "-b", "zweig")
    _session(werkstatt, pid=os.getpid(), sid="w1", cwd=wt)
    zeilen = _scan(werkstatt, "ich", repo)
    assert len(zeilen) == 1, zeilen
    assert zeilen[0][0] == "sibling"


def test_own_non_interactive_and_dead_sessions_are_not_reported(werkstatt: Path, tmp_path: Path) -> None:
    hier = tmp_path / "hier"
    hier.mkdir()
    _session(werkstatt, pid=os.getpid(), sid="ich", cwd=hier)  # own session: filtered
    _session(werkstatt, pid=os.getpid(), sid="hook", cwd=hier, kind="hook")
    tot = subprocess.Popen(["true"])
    tot.wait()
    _session(werkstatt, pid=tot.pid, sid="tot", cwd=hier)
    assert _scan(werkstatt, "ich", hier) == []


def test_a_tab_in_the_session_name_does_not_break_the_row_format(werkstatt: Path, tmp_path: Path) -> None:
    """The name travels on visibly as \\t — the cells stay five."""
    fremd = tmp_path / "fremd"
    fremd.mkdir()
    _session(werkstatt, pid=os.getpid(), sid="t1", cwd=fremd, name="zwei\tspalten")
    zeilen = _scan(werkstatt, "ich", fremd)
    assert len(zeilen) == 1, "a tab in the name must not open a sixth cell"
    assert zeilen[0][1] == "zwei\\tspalten"


def test_the_status_line_names_the_clash_even_with_empty_fields(werkstatt: Path, repo: Path) -> None:
    """End to end: the status line warns even when both fields are empty.

    Exactly the bead's chain: the scan drops the session, the status line
    shows no ⚠, two sessions write into one tree without either learning of
    it. The test runs the real statusline.sh with a fake registry.
    """
    _session(werkstatt, pid=os.getpid(), sid="klon", cwd=repo)
    erg = subprocess.run(
        ["bash", str(STATUSLINE)],
        cwd=str(repo),
        input=json.dumps({"workspace": {"current_dir": str(repo)}, "session_id": "ich"}),
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(werkstatt)},
    )
    assert erg.returncode == 0, erg.stderr
    assert "Gleicher Checkout" in erg.stdout, erg.stdout
    # The label falls back to basename(cwd), the empty status stays empty:
    # the cell reads "()" — the shift fix is visible here.
    # "Gleicher Checkout" and "arbeitet" above are German display texts of
    # tools/claude-code and stay German by rule.
    assert "repo ()" in erg.stdout, erg.stdout
