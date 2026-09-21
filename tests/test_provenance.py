"""RB-P5: der Verlauf wird nie ohne sein Datum zitiert.

Das Ventil `journal-date-citation` im Regelwerk (§ P) benennt diesen Test.
Ein Verweis auf eine Verlaufs-Aufzeichnung, der ihr Datum unterschlaegt,
macht die Aussage unpruefbar — die Handover-Dateien sind nach ihrem Datum
benannt, ein Zitat traegt es also mit dem Pfad.

Ausgenommen sind Nennungen, die kein Record-Zitat sind: das Verzeichnis
selbst (`docs/journal/handover/`), die undatierte Route `_INDEX.md` und die
Platzhalter der Konvention (`<datum>-<name>.md`) — sie fordern das Datum
ein, sie behaupten es nicht.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_ZITAT = re.compile(r"docs/journal/handover/([^\s`)\],;]*)")
_ISO = re.compile(r"\d{4}-\d{2}-\d{2}")


def _undatierte_zitate(text: str) -> list[str]:
    """Konkrete Record-Zitate ohne ISO-Datum; Platzhalter und Verzeichnis gelten nicht."""
    befunde = []
    for fund in _ZITAT.finditer(text):
        ziel = fund.group(1)
        if not ziel or ziel.startswith("<") or _ISO.search(ziel):
            continue
        befunde.append(fund.group(0))
    return befunde


def _verfolgte_markdown() -> list[Path]:
    roh = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(REPO_ROOT / zeile for zeile in roh.stdout.splitlines() if zeile)


def test_journal_is_never_cited_without_a_date() -> None:
    """RB-P5, zweiter Halbsatz: das Zitat traegt das Datum mit dem Pfad."""
    befunde = []
    for pfad in _verfolgte_markdown():
        text = pfad.read_text(encoding="utf-8")
        for zitat in _undatierte_zitate(text):
            befunde.append(f"{pfad.relative_to(REPO_ROOT)}: {zitat}")
    assert not befunde, (
        "Diese Stellen zitieren eine Verlaufs-Aufzeichnung ohne ihr Datum — "
        "den dated Dateinamen ergaenzen oder die Nennung als Konvention "
        f"kenntlich machen (Platzhalter): {befunde}"
    )


def test_the_date_check_goes_red_when_a_citation_loses_its_date() -> None:
    """Mutation auf einer Kopie: ohne Datum wird das Zitat ein Befund (F-A-28)."""
    datiert = "siehe `docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`"
    assert _undatierte_zitate(datiert) == [], "datiertes Zitat zu Unrecht beanstandet"

    entdatumt = "siehe `docs/journal/handover/bootstrap.md`"
    assert _undatierte_zitate(entdatumt), "entdatumtes Zitat nicht gefangen"

    for ausnahme in (
        "gilt ab `docs/journal/handover/`",
        "abgelegt als `docs/journal/handover/<datum>-<name>.md`",
        "geroutet ueber `docs/journal/_INDEX.md`",
    ):
        assert _undatierte_zitate(ausnahme) == [], f"zu Unrecht beanstandet: {ausnahme!r}"
