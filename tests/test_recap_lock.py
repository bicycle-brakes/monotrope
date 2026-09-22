"""Der Recap-Lock — Besitz statt Diebstahl, und das Kind faehrt privat (bead hit, Teil 3).

Bis zum 2026-09-22: der Lock-Loop fiel nach 90 Sekunden durch und schrieb
**ohne Besitz** weiter — und sein EXIT-Trap raeumte den Lock weg, den
zwischenzeitlich ein anderer Lauf hielt. Ausserdem lief `claude -p` aus /tmp:
ein weltbeschreibbares Verzeichnis, aus dem `--setting-sources project` jede
dort abgelegte Einstellung laed. Jetzt: Besitz oder Ausstieg, und das Kind
faehrt aus einem privaten mktemp-Verzeichnis (0700, hinterher entfernt).

Das Objekt (`tools/claude-code/`) ist Bestand und reist nicht — in der
Leerprobe skippt diese Datei deshalb (skipif), sie misst hier.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
RECAP = REPO_ROOT / "tools" / "claude-code" / "hooks" / "recap.sh"
HANDOVER = REPO_ROOT / "tools" / "claude-code" / "hooks" / "handover.sh"

pytestmark = pytest.mark.skipif(
    not (RECAP.is_file() and HANDOVER.is_file()),
    reason="tools/claude-code ist Bestand dieses Repos und reist nicht (Kit-Probe)",
)

LETZTE_ANTWORT = "Die letzte Antwort der Session."


FAKE_CLAUDE = """#!/bin/bash
pwd > "$RECAP_FAKE_VERZEICHNIS/cwd"
{ stat -c %a "$PWD" || stat -f %Lp "$PWD"; } > "$RECAP_FAKE_VERZEICHNIS/mode" 2>/dev/null
cat > /dev/null
printf 'RECAP: Erledigt: Probe · Nächstes: Der Schritt.\\n## Wo wir stehen\\nFake.\\n## Nächster Schritt\\nDer Schritt.\\n## Was ich von dir brauche\\nnichts genannt\\n## Offen\\n- nichts genannt\\n'
"""


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _stop(home: Path, cwd: Path, sid: str = "s1") -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(RECAP), "stop"],
        input=json.dumps({"session_id": sid, "cwd": str(cwd), "last_assistant_message": LETZTE_ANTWORT}),
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(home), "RECAP_LOCK_SEKUNDEN": "2"},
    )


@pytest.fixture
def werkstatt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fake-HOME: installierte Hooks, gefakter claude-Aufruf, leeres Register."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    (home / ".claude" / "recaps").mkdir()
    (home / ".claude" / "session-notes").mkdir()
    shutil.copy2(RECAP, home / ".claude" / "hooks" / "recap.sh")
    shutil.copy2(HANDOVER, home / ".claude" / "hooks" / "handover.sh")
    fake_bin = tmp_path / "fake-bin"
    fake_bin.mkdir()
    fakes = fake_bin / "claude"
    fakes.write_text(FAKE_CLAUDE, encoding="utf-8")
    fakes.chmod(0o755)
    verzeichnis = tmp_path / "fake-verzeichnis"
    verzeichnis.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("RECAP_FAKE_VERZEICHNIS", str(verzeichnis))
    monkeypatch.setenv("RECAP_LOCK_SEKUNDEN", "2")
    return home


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "--initial-branch=main", "--quiet")
    _git(r, "config", "user.email", "test@example.invalid")
    _git(r, "config", "user.name", "Test")
    (r / "datei.txt").write_text("x\n", encoding="utf-8")
    _git(r, "add", "-A")
    _git(r, "commit", "-m", "fixture", "--quiet")
    return r


def test_a_fresh_foreign_lock_is_never_stolen(werkstatt: Path, repo: Path) -> None:
    """Der Bead-Fall: der Lauf faellt aus, statt ohne Besitz zu schreiben.

    Der alte Code entfernte nach 90 Sekunden sogar den Lock, den inzwischen
    ein anderer Lauf hielt — dreifach falsch: ohne Besitz geschrieben, den
    fremden Lock geraeumt, und sein eigenes Verstummen als Erfolg verkauft.
    """
    lock = werkstatt / ".claude" / "recaps" / "s1.lock"
    lock.mkdir()
    (werkstatt / ".claude" / "recaps" / "s1.now").write_text("eine Anfrage\n", encoding="utf-8")

    erg = _stop(werkstatt, repo)
    assert erg.returncode == 0, erg.stderr
    assert lock.is_dir(), "der frische Lock eines anderen wurde weggeraeumt"
    assert (werkstatt / ".claude" / "recaps" / "s1.now").is_file(), "es wurde doch geschrieben — ohne Besitz"
    assert not (werkstatt / ".claude" / "recaps" / "s1.txt").exists()


def test_a_stale_lock_is_removed_and_the_run_proceeds(werkstatt: Path, repo: Path) -> None:
    lock = werkstatt / ".claude" / "recaps" / "s1.lock"
    lock.mkdir()
    alt = lock.stat().st_mtime - 400
    os.utime(lock, (alt, alt))

    erg = _stop(werkstatt, repo)
    assert erg.returncode == 0, erg.stderr
    assert not lock.exists(), "der toote Lock blieb liegen"
    assert (werkstatt / ".claude" / "recaps" / "s1.txt").is_file(), "nach dem toten Lock wurde gearbeitet"


def test_the_child_runs_from_a_private_directory(werkstatt: Path, repo: Path) -> None:
    """claude -p lief aus /tmp — ein weltbeschreibbares Verzeichnis, aus dem
    --setting-sources project jede dort gepflanzte Einstellung laed."""
    verzeichnis = Path(os.environ["RECAP_FAKE_VERZEICHNIS"])
    erg = _stop(werkstatt, repo)
    assert erg.returncode == 0, erg.stderr

    kind_cwd = (verzeichnis / "cwd").read_text(encoding="utf-8").strip()
    kind_modus = (verzeichnis / "mode").read_text(encoding="utf-8").strip()
    assert kind_cwd != "/tmp", "das Kind lief aus /tmp"
    assert int(kind_modus, 8) & 0o077 == 0, f"das Arbeitsverzeichnis des Kindes ist nicht privat: {kind_modus}"
    assert (werkstatt / ".claude" / "recaps" / "s1.txt").is_file(), (
        "der Recap aus der Fake-Antwort wurde nicht uebernommen"
    )
    assert (werkstatt / ".claude" / "session-notes" / "s1.md").is_file(), (
        "die Notiz wurde nicht an handover.sh note uebergeben"
    )
