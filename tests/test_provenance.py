"""RB-P5: der Verlauf wird nie ohne sein Datum zitiert.

Das Ventil `journal-date-citation` im Regelwerk (§ P) benennt diesen Test.
Ein Verweis auf eine Verlaufs-Aufzeichnung, der ihr Datum unterschlaegt,
macht die Aussage unpruefbar — die Handover-Dateien sind nach ihrem Datum
benannt, ein Zitat traegt es also mit dem Pfad.

Ausgenommen sind Nennungen, die kein Record-Zitat sind: das Verzeichnis
selbst (`docs/journal/handover/`), die undatierte Route `_INDEX.md` und die
Platzhalter der Konvention (`<datum>-<name>.md`) — sie fordern das Datum
ein, sie behaupten es nicht.

Dazu der Change journal-citation-gate (2026-11-19, Entscheid Q-1): ein Ziel
ist ein Muster und kein Zitat, wenn nach der Normalisierung ein `*` uebrig
bleibt; eine Auslassung (`…`, `...`) gilt wie ein Platzhalter. Vom
Forschungslauf geschriebene `research-swarm/v2`-Umhuellungen — Aufzeichnungen
und ihr Begleittext — sind nur in der `research.md` eines Changes (aktiv oder
Archiv) ausgenommen, und nur wenn der eine Leser
(`scripts/check_research_handoff.py`) die ganze Datei ohne Befund liest; eine
Datei, die er nicht liest, wird ohne Ausnahme voll gescannt.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_research_handoff as handoff_gate  # noqa: E402
from test_research_handoff import RUN1, RUN2, run_text  # noqa: E402

_ZITAT = re.compile(r"docs/journal/handover/([^\s`)\],;]*)")
_ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
_PATH_CHAR = re.compile(r"[A-Za-z0-9._/*-]")
_EMPHASIS_TAIL = re.compile(r"[*_]+\Z")
_MD_TAIL = re.compile(r"\.md\Z")
_ELISIONS = ("…", "...")
_RESEARCH_ACTIVE = re.compile(r"(?:\A|/)plans/changes/[^/]+/research\.md\Z")
_RESEARCH_ARCHIVE = re.compile(r"(?:\A|/)plans/changes/archive/[0-9]{4}-[0-9]{2}-[0-9]{2}-.+/research\.md\Z")


def _normalised_target(target: str) -> str:
    """Spec details S-1, S-11 and S-12: elision, possessive, path alphabet and `.md` emphasis boundary."""
    # An exact elision - including surrounding trailing formatting - is a placeholder (S-1).
    candidate = target
    while candidate and candidate[-1] != "…" and not _PATH_CHAR.match(candidate[-1]):
        candidate = candidate[:-1]
    if candidate in _ELISIONS:
        return candidate
    # Every other target: trailing possessives, sentence-final periods and characters outside the path
    # alphabet, repeating until none remain (S-11).
    while True:
        if target.endswith("'s") or target.endswith("’s"):
            target = target[:-2]
        elif target.endswith(".") or target and not _PATH_CHAR.match(target[-1]):
            target = target[:-1]
        else:
            break
    # A trailing run of `*` or `_` is emphasis only after a file name with an extension; otherwise it
    # stays, and any remaining `*` makes the target a pattern (S-12).
    emphasis = _EMPHASIS_TAIL.search(target)
    if emphasis and _MD_TAIL.search(target[: emphasis.start()]):
        target = target[: emphasis.start()]
    return target


def _undatierte_zitate(text: str) -> list[str]:
    """Konkrete Record-Zitate ohne ISO-Datum; Platzhalter, Auslassungen und Muster gelten nicht."""
    befunde = []
    for fund in _ZITAT.finditer(text):
        ziel = _normalised_target(fund.group(1))
        if not ziel or ziel.startswith("<") or ziel in _ELISIONS or "*" in ziel or _ISO.search(ziel):
            continue
        befunde.append(fund.group(0))
    return befunde


def _is_change_research(path: Path) -> bool:
    """The research.md of an active or archived change; no other file is exempt (spec S-3).

    The shape is matched on the path string, not on `parts`: the enforcer hands in absolute paths
    under its repository root, while the tests hand in absolute paths under a temporary tree.
    """
    posix = path.as_posix()
    if _RESEARCH_ARCHIVE.search(posix):
        return True
    return _RESEARCH_ACTIVE.search(posix) is not None


def _file_findings(path: Path, text: str) -> list[str]:
    """The undated citations of one file; trusted runner envelopes of change research files are exempt.

    Acceptance is per file and at parse level (spec S-8): when the one handoff reader
    (`check_research_handoff.parse_text`) reads the whole research file, its run envelopes - opening
    marker through closing marker, audit prose included - are exempt; when it refuses the file,
    nothing is exempt and the whole text is scanned.
    """
    if not _is_change_research(path):
        return _undatierte_zitate(text)
    try:
        runs = handoff_gate.parse_text(text, path.name)
    except handoff_gate.CannotMeasure:
        return _undatierte_zitate(text)
    befunde: list[str] = []
    scanned = 0
    for start, end in sorted(run.span for run in runs if run.span is not None):
        befunde += _undatierte_zitate(text[scanned:start])
        scanned = max(scanned, end)
    return befunde + _undatierte_zitate(text[scanned:])


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
        for zitat in _file_findings(pfad, text):
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


def test_patterns_are_not_journal_citations() -> None:
    """Criterion 1: a `*` left after normalisation is a pattern, not a citation (Q-1, S-12)."""
    for muster in (
        "siehe `docs/journal/handover/*.md`",
        "siehe `docs/journal/handover/2026-11-*`",
        "siehe `docs/journal/handover/coding-harness-*`",
        "fett **docs/journal/handover/*.md** in einer Zeile",
        "der Ordner **docs/journal/handover/** selbst",
    ):
        assert _undatierte_zitate(muster) == [], muster
    # The planted fault: the same sentence with a concrete undated target must stay red.
    assert _undatierte_zitate("siehe `docs/journal/handover/coding-harness-bootstrap.md`")


def test_runner_envelopes_are_not_journal_citations(tmp_path: Path) -> None:
    """Criterion 2: records and audit prose of a parseable envelope are exempt, at parse level (Q-1, S-8)."""
    pfad = tmp_path / "plans" / "changes" / "demo" / "research.md"
    zitat = "Siehe `docs/journal/handover/bootstrap.md`."
    run = run_text(RUN1)
    text = "---\ntitle: Research\n---\n\n# Research\n\n" + run
    assert _file_findings(pfad, text) == []
    archiv = tmp_path / "plans" / "changes" / "archive" / "2026-11-01-old" / "research.md"
    assert _file_findings(archiv, text) == [], "an archived change's research.md is exempt as well"
    inside = text.replace(f"run {RUN1} status: complete.", f"run {RUN1} status: complete. {zitat}")
    assert inside != text
    assert _file_findings(pfad, inside) == [], "the audit prose inside the envelope is exempt"
    # The exemption is parse-level: whole-change validation fails, the envelope stays trusted (S-9).
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(inside, encoding="utf-8")
    spec = pfad.parent / "spec.md"
    spec.write_text(
        "---\ntitle: Spec\nneighbours: []\n---\n\n## Acceptance criteria\n\n1. When x, y.\n   *Refuted by:* z.\n",
        encoding="utf-8",
    )
    outcome = handoff_gate.check_change(pfad.parent, "demo")
    assert outcome.findings, "without an answered record the handoff gate reports the change"
    assert _file_findings(pfad, inside) == [], "a failing whole-change validation does not unexempt the envelope"
    # Before the envelope the check still scans.
    before = text.replace("# Research\n", f"# Research\n\n{zitat}\n", 1)
    befunde = _file_findings(pfad, before)
    assert befunde and "bootstrap.md" in befunde[0]


def test_undated_citations_outside_runner_envelopes_are_reported(tmp_path: Path) -> None:
    """Criterion 3: a hand-written undated citation stays red, also beside a trusted envelope (Q-1, S-2)."""
    pfad = tmp_path / "plans" / "changes" / "demo" / "research.md"
    zitat = "Siehe `docs/journal/handover/bootstrap.md`."
    run = run_text(RUN1)
    header = "---\ntitle: Research\n---\n\n# Research\n\n"
    befunde = _file_findings(pfad, f"{header}{zitat}\n\n" + run)
    assert befunde and "bootstrap.md" in befunde[0], "a citation before the envelope is scanned"
    befunde = _file_findings(pfad, f"{header}{run}\n\n{zitat}\n")
    assert befunde and "bootstrap.md" in befunde[0], "a citation after the envelope is scanned"
    fremd = tmp_path / "docs" / "notes.md"
    assert _file_findings(fremd, zitat), "a file that is no change research is scanned wholly"
    # Emphasis, a closing quote and a typographic possessive do not rescue a citation (S-2, S-12).
    for zeile in (
        "„**docs/journal/handover/bootstrap.md**“",
        "siehe `docs/journal/handover/bootstrap.md’s`",
        "siehe **docs/journal/handover/bootstrap.md**.",
        "siehe `docs/journal/handover/bootstrap.md`.",
    ):
        assert _undatierte_zitate(zeile), zeile


def test_existing_exemptions_and_elisions() -> None:
    """Criterion 4: dated, empty, placeholder, elision and marker-only targets are not reported (S-1, S-6)."""
    for ausnahme in (
        "siehe `docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`",
        "gilt ab `docs/journal/handover/`",
        "abgelegt als `docs/journal/handover/<datum>-<name>.md`",
        "ausgelassen `docs/journal/handover/…`",
        "ausgelassen `docs/journal/handover/...`",
        "zitiert als Auslassung `docs/journal/handover/...“`",
        "abgeschnitten `docs/journal/handover/…“.`",
        "nur Marker `docs/journal/handover/**`",
        "geroutet ueber `docs/journal/_INDEX.md`",
    ):
        assert _undatierte_zitate(ausnahme) == [], ausnahme
    # The planted fault: the same sentence with the date removed must turn red.
    assert _undatierte_zitate("siehe `docs/journal/handover/coding-harness-bootstrap.md`")


def test_malformed_or_forged_envelopes_remain_scannable(tmp_path: Path) -> None:
    """Criterion 5: only a reader-accepted envelope in a change research file is exempt (S-3, S-4, S-8)."""
    pfad = tmp_path / "plans" / "changes" / "demo" / "research.md"
    zitat = "Siehe `docs/journal/handover/bootstrap.md`."
    header = "---\ntitle: Research\n---\n\n# Research\n\n"
    unclosed = f"{header}<!-- research-swarm/v2 run {RUN1} -->\n\n{zitat}\n"
    nested = (
        f"{header}<!-- research-swarm/v2 run {RUN1} -->\n\n"
        f"<!-- research-swarm/v2 run {RUN2} -->\n\n{zitat}\n\n<!-- /research-swarm/v2 -->\n"
    )
    manifest = json.dumps(
        {
            "schema": "research-swarm/v2",
            "run_id": RUN2,
            "class": "feature",
            "status": "complete",
            "given_neighbours": [],
        },
        sort_keys=True,
        indent=2,
    )
    mismatched = (
        f"{header}<!-- research-swarm/v2 run {RUN1} -->\n\n"
        f"```research-swarm/v2 manifest\n{manifest}\n```\n\n{zitat}\n\n<!-- /research-swarm/v2 -->\n"
    )
    # An envelope the reader refuses hides nothing: the whole file is scanned (S-4, S-8).
    for kaputt in (unclosed, nested, mismatched):
        with pytest.raises(handoff_gate.CannotMeasure):
            handoff_gate.parse_text(kaputt, pfad.name)
        befunde = _file_findings(pfad, kaputt)
        assert befunde and "bootstrap.md" in befunde[0], "an unparseable research file is scanned without exemptions"
    # A valid run stays exempt only while the whole file parses: a malformed second run unexempts it (S-8).
    good = run_text(RUN1)
    inside = good.replace(f"run {RUN1} status: complete.", f"run {RUN1} status: complete. {zitat}")
    assert inside != good
    malformed = (
        f"<!-- research-swarm/v2 run {RUN2} -->\n\n"
        "```research-swarm/v2 manifest\n{not json\n```\n\n<!-- /research-swarm/v2 -->\n"
    )
    beides = header + inside + "\n" + malformed
    with pytest.raises(handoff_gate.CannotMeasure):
        handoff_gate.parse_text(beides, pfad.name)
    befunde = _file_findings(pfad, beides)
    assert befunde and "bootstrap.md" in befunde[0], "a malformed second run unexempts the whole file"
    # A forged envelope in any other file is scanned like ordinary text (S-3).
    forge = f"<!-- research-swarm/v2 run {RUN1} -->\n\n{zitat}\n\n<!-- /research-swarm/v2 -->\n"
    for fremd in (
        tmp_path / "plans" / "changes" / "demo" / "findings.md",
        tmp_path / "docs" / "journal" / "notes.md",
        tmp_path / "plans" / "specs" / "living" / "research.md",
        tmp_path / "plans" / "other" / "research.md",
    ):
        befunde = _file_findings(fremd, forge)
        assert befunde and "bootstrap.md" in befunde[0], str(fremd)
