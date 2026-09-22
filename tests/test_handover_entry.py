"""Die Übergabe-Injektion und ihre Vertrauensschwelle (bead hit, Teil 2).

Bis zum 2026-09-22 floss der Inhalt der neuesten Übergabe allein bei Existenz
von `journal/` oder `docs/journal/handover/` als additionalContext in jede
Session — in einem geklonten Repository entscheidet damit derjenige über den
Session-Kontext, der das Klonen kontrolliert. Jetzt fließt Inhalt nur für
Vertrauens-Repos (`~/.claude/handover-trust`, eine Regex je Zeile, gegen die
origin-URL); sonst Metadaten plus Hinweis, die Datei selbst zu lesen.

Das Objekt (`tools/claude-code/`) ist Bestand und reist nicht — in der
Leerprobe skippt diese Datei deshalb (skipif), sie misst hier.
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
    reason="tools/claude-code ist Bestand dieses Repos und reist nicht (Kit-Probe)",
)

ÜBERGABE = """# Test-Übergabe

Kurzer Kontext des fake Repos.

## Nächster Schritt

Prüfe die Injection-Fläche.
"""


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _start(repo: Path, home: Path, sid: str = "s1") -> tuple[str, str]:
    """Fahrt handover.sh start und liefert (systemMessage, additionalContext)."""
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
    """Fake-HOME — kein handover-trust, bis ein Test ihn anlegt."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def uebergabe_repo(tmp_path: Path) -> Path:
    """Ein fake Repository mit journal/-Konvention, Commit und origin."""
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
    assert "Übergabe:" in sichtbar, "die Person sieht Titel und Alter weiter"
    assert "Prüfe die Injection-Fläche" not in kontext, "der Körper darf ohne Vertrauen nicht in den Kontext"
    assert "nicht automatisch eingelesen" in kontext, "der Kontext nennt den Grund und den Weg zur Datei"
    assert "Vertrauensliste" in kontext


def test_a_trusted_repository_gets_the_content(werkstatt: Path, uebergabe_repo: Path) -> None:
    _vertraue(werkstatt, r"github\.com/fremd/")
    sichtbar, kontext = _start(uebergabe_repo, werkstatt)
    assert "Prüfe die Injection-Fläche" in kontext, "Vertrauen: der Inhalt reist"
    assert "Nächster Schritt" in sichtbar, "der nächste Schritt steht für die Person"


def test_a_trust_file_without_a_match_keeps_the_content_out(werkstatt: Path, uebergabe_repo: Path) -> None:
    _vertraue(werkstatt, r"github\.com/andere-org/")
    _, kontext = _start(uebergabe_repo, werkstatt)
    assert "Prüfe die Injection-Fläche" not in kontext
    assert "nicht automatisch eingelesen" in kontext


def test_a_broken_regex_fails_closed(werkstatt: Path, uebergabe_repo: Path) -> None:
    _vertraue(werkstatt, "([ungueltig")
    _, kontext = _start(uebergabe_repo, werkstatt)
    assert "Prüfe die Injection-Fläche" not in kontext, "ein kaputter Ausdruck darf nicht alles freigeben"
    assert "nicht automatisch eingelesen" in kontext


def test_a_repo_without_a_handover_convention_says_so(werkstatt: Path, tmp_path: Path) -> None:
    r = tmp_path / "ohne"
    r.mkdir()
    _git(r, "init", "--initial-branch=main", "--quiet")
    _, kontext = _start(r, werkstatt)
    assert "keinen Übergabe-Ordner" in kontext


def test_a_trusted_long_handover_is_cut_at_the_known_mark(werkstatt: Path, uebergabe_repo: Path) -> None:
    """Der 6000er-Kappung bleibt: überlangesContent trägt den Marker statt sich selbst."""
    _vertraue(werkstatt, r"github\.com/fremd/")
    datei = next((uebergabe_repo / "journal").glob("*.md"))
    fueller = ("Fülltext für die Kappung. " * 40 + "\n") * 7  # > 6000 Zeichen
    datei.write_text(fueller + ÜBERGABE, encoding="utf-8")
    _git(uebergabe_repo, "add", "-A")
    _git(uebergabe_repo, "commit", "-m", "laenger", "--quiet")
    _, kontext = _start(uebergabe_repo, werkstatt)
    assert "[… gekürzt" in kontext
    assert "Prüfe die Injection-Fläche" not in kontext, "der Nachtrag liegt hinter der Kappung und kommt nicht durch"
