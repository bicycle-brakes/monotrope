"""Der Session-Scan und die Statuszeile — die Scharstellung hinter dem ⚠ (bead hit).

Bis zum 2026-09-22 las `IFS=$'\\t' read` leere Felder auf die Nachbarn
rutschen: eine Session ohne Namen oder Status rutschte in der Spalte `kind`,
galt als nicht-interaktiv und wurde nie als Clash gemeldet — der Bead hat das
mit drei fake Sessions verifiziert (PR #10-Review). Diese Datei haelt den
Nachweis als Test: den Produzenten (`hooks/session-scan.sh`, Feldtrennung per
NUL) und den Consumer (`statusline.sh`, Trennung per Parameter-Expansion),
sowie den Fall Ende-zu-Ende.

Das Objekt selbst (`tools/claude-code/`) ist Bestand dieses Repos und reist
nicht mit dem Kit — in der Leerprobe skippt diese Datei deshalb (skipif
unten), sie misst hier.
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
    reason="tools/claude-code ist Bestand dieses Repos und reist nicht (Kit-Probe)",
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
    """Eine fake Session-Datei, wie Claude Code sie nach ~/.claude/sessions/ schreibt.

    `procStart` bleibt absichtlich leer: der Scan vergleicht ihn nur, wenn er
    da ist, und ein Test, der `ps`-Lokalisierung faken muesste, pruefte die
    falsche Sache.
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
    # Python-Split kollabiert keine leeren Felder — genau der Maszstab, an dem
    # der alte `IFS=$'\t' read` zerbrach.
    return [zeile.split("\t") for zeile in erg.stdout.splitlines()]


@pytest.fixture
def werkstatt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fake-HOME mit installiertem Scan und leerem Session-Register."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    (home / ".claude" / "sessions").mkdir()
    shutil.copy2(SCAN, home / ".claude" / "hooks" / "session-scan.sh")
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Ein echtes Mini-Repository mit einem Commit — nie der Baum dieses Projekts."""
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
    """Der Bead-Fall: leere Felder verschieben keine Spalten.

    Vor dem Fix rutschte hinter einem leeren Namen der Status in die Spalte
    `kind` — die Session galt als nicht-interaktiv und war unsichtbar, genau
    wenn sie am wenigsten sichtbar sein durfte.
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
        assert len(zeilen) == 2, f"beide Sessions melden sich: {zeilen}"

        leer = next(z for z in zeilen if z[3] == "f1")
        assert leer[0] == "other"
        assert leer[1] == "fremd", "label faellt auf basename(cwd) zurueck"
        assert leer[2] == "", "fehlender Status bleibt leeres Feld, kein Verschieben"
        assert leer[4] == str(fremd)

        voll = next(z for z in zeilen if z[3] == "f2")
        assert (voll[1], voll[2]) == ("Andere", "arbeitet")
    finally:
        zweitprozess.kill()
        zweitprozess.wait()


def test_a_clash_with_empty_fields_is_reported_as_a_clash(werkstatt: Path, repo: Path) -> None:
    """Die Folge, die der Bead meint: ein echter Clash darf nie unsichtbar sein."""
    _session(werkstatt, pid=os.getpid(), sid="klon", cwd=repo)  # Name und Status leer
    zeilen = _scan(werkstatt, "ich", repo)
    assert len(zeilen) == 1, zeilen
    assert zeilen[0][0] == "clash", f"gleicher Checkout nicht erkannt: {zeilen}"
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
    _session(werkstatt, pid=os.getpid(), sid="ich", cwd=hier)  # eigene: gefiltert
    _session(werkstatt, pid=os.getpid(), sid="hook", cwd=hier, kind="hook")
    tot = subprocess.Popen(["true"])
    tot.wait()
    _session(werkstatt, pid=tot.pid, sid="tot", cwd=hier)
    assert _scan(werkstatt, "ich", hier) == []


def test_a_tab_in_the_session_name_does_not_break_the_row_format(werkstatt: Path, tmp_path: Path) -> None:
    """Der Name reist sichtbar als \\t weiter — die Zellen bleiben fuenf."""
    fremd = tmp_path / "fremd"
    fremd.mkdir()
    _session(werkstatt, pid=os.getpid(), sid="t1", cwd=fremd, name="zwei\tspalten")
    zeilen = _scan(werkstatt, "ich", fremd)
    assert len(zeilen) == 1, "ein Tab im Namen darf keine sechste Zelle aufmachen"
    assert zeilen[0][1] == "zwei\\tspalten"


def test_the_status_line_names_the_clash_even_with_empty_fields(werkstatt: Path, repo: Path) -> None:
    """Ende-zu-Ende: die Statuszeile warnt, auch wenn beide Felder leer sind.

    Genau die Kette des Beads: Scan wirft die Session weg, die Statuszeile
    zeigt keinen ⚠, zwei Sessions schreiben in einen Baum, ohne dass eine es
    erfahrt. Der Test faehrt die echte statusline.sh mit Fake-Register.
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
    # Label faellt auf basename(cwd) zurueck, der leere Status bleibt leer:
    # die Zelle sieht als "()" — der Verschiebe-Fix ist hier sichtbar.
    assert "repo ()" in erg.stdout, erg.stdout
