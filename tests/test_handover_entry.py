"""The handover injection and its trust threshold (bead hit, part 2).

Until 2026-09-22 the content of the newest handover flowed into every session
as additionalContext merely because `journal/` or `docs/journal/handover/`
existed — in a cloned repository, whoever controls the cloning thereby decides
the session context. Now content flows only for trusted repositories
(`~/.claude/handover-trust`, one regex per line, matched against the origin
URL); otherwise metadata plus a hint to read the file oneself.

The subject (`tools/claude-code/`) is part of this repo and does not travel —
in the dry run this file therefore skips (skipif); it measures here.

The expected strings asserted below ("Übergabe:", "nicht automatisch
eingelesen", "Vertrauensliste", "Nächster Schritt", "keinen Übergabe-Ordner",
"[… gekürzt") are the maintainer's German display texts of
`tools/claude-code/hooks/handover.sh` and stay German by rule; so does the
German fixture handover.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HANDOVER = REPO_ROOT / "tools" / "claude-code" / "hooks" / "handover.sh"

pytestmark = pytest.mark.skipif(
    not HANDOVER.is_file(),
    reason="tools/claude-code is part of this repo and does not travel (kit probe)",
)

ÜBERGABE = """# Test-Übergabe

Kurzer Kontext des fake Repos.

## Nächster Schritt

Prüfe die Injection-Fläche.
"""


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _start(repo: Path, home: Path, sid: str = "s1") -> tuple[str, str]:
    """Runs handover.sh start and returns (systemMessage, additionalContext)."""
    erg = subprocess.run(
        ["bash", str(HANDOVER), "start"],
        cwd=str(repo),
        input=json.dumps({"session_id": sid, "cwd": str(repo), "source": "startup"}),
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(home)},
    )
    assert erg.returncode == 0, erg.stderr
    antwort = json.loads(erg.stdout)
    return antwort["systemMessage"], antwort["hookSpecificOutput"]["additionalContext"]


@pytest.fixture
def werkstatt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fake HOME — no handover-trust until a test creates it."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def uebergabe_repo(tmp_path: Path) -> Path:
    """A fake repository with the journal/ convention, a commit and an origin."""
    r = tmp_path / "klon"
    (r / "journal").mkdir(parents=True)
    (r / "journal" / "2026-09-22-test.md").write_text(ÜBERGABE, encoding="utf-8")
    _git(r, "init", "--initial-branch=main", "--quiet")
    _git(r, "config", "user.email", "test@example.invalid")
    _git(r, "config", "user.name", "Test")
    _git(r, "remote", "add", "origin", "https://github.com/fremd/klon.git")
    _git(r, "add", "-A")
    _git(r, "commit", "-m", "fixture", "--quiet")
    return r


def _vertraue(home: Path, muster: str) -> None:
    datei = home / ".claude" / "handover-trust"
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(muster + "\n", encoding="utf-8")


def test_without_a_trust_file_the_content_stays_out_of_the_context(werkstatt: Path, uebergabe_repo: Path) -> None:
    sichtbar, kontext = _start(uebergabe_repo, werkstatt)
    assert "Übergabe:" in sichtbar, "the person still sees title and age"
    assert "Prüfe die Injection-Fläche" not in kontext, "without trust the body must not enter the context"
    assert "nicht automatisch eingelesen" in kontext, "the context names the reason and the way to the file"
    assert "Vertrauensliste" in kontext


def test_a_trusted_repository_gets_the_content(werkstatt: Path, uebergabe_repo: Path) -> None:
    _vertraue(werkstatt, r"github\.com/fremd/")
    sichtbar, kontext = _start(uebergabe_repo, werkstatt)
    assert "nicht automatisch eingelesen" not in kontext, "the untrusted branch ran although the repository is trusted"
    assert "Prüfe die Injection-Fläche" in kontext, "trust: the content travels"
    assert "Nächster Schritt" in sichtbar, "the next step is shown to the person"


def test_a_trust_file_without_a_match_keeps_the_content_out(werkstatt: Path, uebergabe_repo: Path) -> None:
    _vertraue(werkstatt, r"github\.com/andere-org/")
    _, kontext = _start(uebergabe_repo, werkstatt)
    assert "Prüfe die Injection-Fläche" not in kontext
    assert "nicht automatisch eingelesen" in kontext


def test_a_broken_regex_fails_closed(werkstatt: Path, uebergabe_repo: Path) -> None:
    _vertraue(werkstatt, "([ungueltig")
    _, kontext = _start(uebergabe_repo, werkstatt)
    assert "Prüfe die Injection-Fläche" not in kontext, "a broken expression must not release everything"
    assert "nicht automatisch eingelesen" in kontext


def test_a_repo_without_a_handover_convention_says_so(werkstatt: Path, tmp_path: Path) -> None:
    r = tmp_path / "ohne"
    r.mkdir()
    _git(r, "init", "--initial-branch=main", "--quiet")
    _, kontext = _start(r, werkstatt)
    assert "keinen Übergabe-Ordner" in kontext


def test_a_trusted_long_handover_is_cut_at_the_known_mark(werkstatt: Path, uebergabe_repo: Path) -> None:
    """The 6000-character cap stays: over-long content carries the marker instead of itself."""
    _vertraue(werkstatt, r"github\.com/fremd/")
    datei = next((uebergabe_repo / "journal").glob("*.md"))
    fueller = ("Fülltext für die Kappung. " * 40 + "\n") * 7  # > 6000 characters
    datei.write_text(fueller + ÜBERGABE, encoding="utf-8")
    _git(uebergabe_repo, "add", "-A")
    _git(uebergabe_repo, "commit", "-m", "laenger", "--quiet")
    _, kontext = _start(uebergabe_repo, werkstatt)
    assert "[… gekürzt" in kontext
    assert "Prüfe die Injection-Fläche" not in kontext, "the addendum lies behind the cap and does not get through"
