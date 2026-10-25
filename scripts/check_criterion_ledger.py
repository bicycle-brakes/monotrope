#!/usr/bin/env python3
"""check_criterion_ledger.py — every test a plan names for an acceptance criterion still exists.

Every ``plan.md`` of a change carries exactly one section headed
``## Criterion ledger``, one line per criterion and the proof that holds it.
This gate holds that section: a named test that is no longer defined, a
criterion of the spec without an entry, an entry for a criterion the spec does
not have, and a line in none of the three entry forms are findings (ADR 0013;
``decisions.md`` Q-1 and Q-2 of the change ``criterion-test-ledger``, bead
coding-harness-909). Deleting or renaming a test then turns ``make verify``
red until its ledger line changes with it — while the change is live and,
from 2026-10-11 on, after it is archived too.

The three entry forms, one line each:

- a test entry:            ``- <n>: tests/<path>::<function>``
- a not-yet-written entry: ``- <n>: not yet written tests/<path>::<function>``
- a not-a-test entry:      ``- <n>: not a test — <what holds it>``

``<n>`` is a criterion number of the change's ``spec.md``, written without a
leading zero. A test entry and a not-yet-written entry may end in `` — `` and
the fault that turns the test red. An indented line continues the entry above
it; an indented line that begins with ``- `` is a finding, never an entry.
While a change is live, a not-yet-written entry whose function is not yet
defined is accepted; a not-yet-written entry whose function already exists is
a finding, and so is every not-yet-written entry of an archived plan.

A function is defined when the named file exists and holds a line beginning
``def <function>(`` — a top-level function, found by reading the file as text.
The gate never imports or runs a named test file (spec criterion 7).

Archived plans are held like live ones as soon as they carry a ledger section.
An archived plan without one is exempt only when its header holds exactly one
line ``date: YYYY-MM-DD`` with a real calendar date before the cut-off;
a quoted, commented, missing, impossible or doubled date measures instead of
exempting. A change folder without a ``plan.md`` — live or archived — is not
examined at all (spec criterion 1).

Usage:
    python3 scripts/check_criterion_ledger.py [--root DIR]

Exit:
    0 = nothing found
    1 = findings
    3 = could not measure
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

CHANGES_DIR = "plans/changes"
ARCHIVE = "archive"
HEADING = "## Criterion ledger"
# The day of the maintainer's answers (decisions.md Q-2); changing it is a
# governance act, stated in docs/WORKFLOW.md beside this gate.
CUTOFF = date(2026, 10, 11)

_N = r"(?P<n>[1-9][0-9]*)"
_REF = r"(?P<path>tests/(?:[^\s/:`]+/)*test_[^\s/:`]*\.py)::(?P<function>test_[A-Za-z0-9_]*)"
_FAULT = r"(?: — (?P<text>\S.*))?"
TEST = re.compile(rf"- {_N}: {_REF}{_FAULT}", re.ASCII)
NOT_YET = re.compile(rf"- {_N}: not yet written {_REF}{_FAULT}", re.ASCII)
NOT_A_TEST = re.compile(rf"- {_N}: not a test — (?P<text>\S.*)", re.ASCII)

_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_FENCE_CLOSE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
_LEVEL12 = re.compile(r"^#{1,2}(?:[ \t]|$)")
_LEVEL2 = re.compile(r"^##(?:[ \t]|$)")
_NUMBERED = re.compile(r"^([1-9][0-9]*)\. ")
_DATE = re.compile(r"date: ([0-9]{4}-[0-9]{2}-[0-9]{2})")
_INDENTED_LIST = re.compile(r"^[ \t]+- ")

_FORMS = (
    '"- <n>: tests/<file>::<function>"',
    '"- <n>: not yet written tests/<file>::<function>"',
    '"- <n>: not a test — <what holds it>"',
)

Reading = tuple[str | None, str | None]


class CannotMeasure(Exception):
    """The root cannot be measured at all."""


@dataclass(frozen=True)
class Entry:
    """One line of a ledger section that matched an entry form."""

    line: int
    kind: str  # "test", "not yet written" or "not a test"
    number: int
    path: str = ""
    function: str = ""


@dataclass
class Tally:
    """What a run counted."""

    live: int = 0
    archived: int = 0
    exempt: int = 0
    test: int = 0
    not_yet: int = 0
    not_a_test: int = 0

    @property
    def held(self) -> int:
        return self.live + self.archived

    @property
    def entries(self) -> int:
        return self.test + self.not_yet + self.not_a_test


def _lines(text: str) -> list[str]:
    """Split on newline only; drop a leading byte-order mark and trailing whitespace."""
    if text.startswith("\ufeff"):  # a leading byte-order mark; an empty text has none
        text = text[1:]
    return [line.rstrip() for line in text.split("\n")]


def _fenced(lines: list[str]) -> list[bool]:
    """Per line, whether it stands in a fenced code block (CommonMark fences)."""
    inside = [False] * len(lines)
    marker = ""
    length = 0
    for i, line in enumerate(lines):
        if marker:
            inside[i] = True
            closed = _FENCE_CLOSE.match(line)
            if closed and closed.group(1)[0] == marker and len(closed.group(1)) >= length:
                marker, length = "", 0
            continue
        opened = _FENCE.match(line)
        # CommonMark: the info string of a backtick fence holds no backtick
        # (tildes may); such a line opens nothing (review-loop row F-4).
        if opened and not (opened.group(1)[0] == "`" and "`" in line[opened.end() :]):
            inside[i] = True
            marker, length = opened.group(1)[0], len(opened.group(1))
    return inside


def parse_entry(text: str, line: int = 0) -> Entry | None:
    """Read one ledger line in one of the three entry forms; None when in none.

    A line that begins with whitespace is never an entry: an indented
    ``- <n>: …`` is a finding, and a continuation line is not read.
    """
    stripped = text.rstrip()
    if stripped != stripped.lstrip():
        return None
    forms = ((NOT_A_TEST, "not a test"), (NOT_YET, "not yet written"), (TEST, "test"))
    for pattern, kind in forms:
        matched = pattern.fullmatch(stripped)
        if not matched:
            continue
        groups = matched.groupdict()
        path = str(groups.get("path") or "")
        function = str(groups.get("function") or "")
        if path and any(segment in (".", "..") for segment in path.split("/")):
            return None  # the path would climb out of tests/
        return Entry(line=line, kind=kind, number=int(matched.group("n")), path=path, function=function)
    return None


def ledger_sections(lines: list[str]) -> list[list[tuple[int, str]]]:
    """Every ``## Criterion ledger`` heading outside a fence, with its lines to the next heading.

    A section runs to the next level-1 or level-2 heading outside a fence, or
    to the end of the file. Each section is a list of (line number, line)
    pairs; the heading itself is not part of the list.
    """
    inside = _fenced(lines)
    sections: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] | None = None
    for number, line in enumerate(lines, start=1):
        if not inside[number - 1]:
            if line == HEADING:
                current = []
                sections.append(current)
                continue
            if current is not None and _LEVEL12.match(line):
                current = None
        if current is not None:
            current.append((number, line))
    return sections


def clear_written(root: Path, plan: Path) -> list[int]:
    """Remove `not yet written` from every ledger entry whose named test exists; return their numbers.

    The marker is derivable from the tree, so the stage-2 runner clears it before its own `make
    verify`, as it renders the index and stamps the dates (bead coding-harness-7g6h). An entry whose
    file or function is missing keeps its marker, and lines in a fence are never touched. Every other
    byte of the plan stays as it was.
    """
    text, _ = read(plan)
    if text is None:
        return []
    raw = text.split("\n")
    lines = _lines(text)
    # A fence under the ledger heading still belongs to the section; its lines are examples (P239-1).
    fenced = _fenced(lines)
    cleared: list[int] = []
    for section in ledger_sections(lines):
        for number, line in section:
            if fenced[number - 1]:
                continue
            entry = parse_entry(line, number)
            if entry is None or entry.kind != "not yet written":
                continue
            found, _ = read(root / entry.path)
            if found is None or not _defined(found, entry.function):
                continue
            raw[number - 1] = raw[number - 1].replace(": not yet written ", ": ", 1)
            cleared.append(entry.number)
    if cleared:
        plan.write_text("\n".join(raw), encoding="utf-8")
    return cleared


def criterion_numbers(spec_text: str) -> set[int]:
    """Every criterion number of a ``## Acceptance criteria`` section, as ``<n>. `` at line start.

    Every such section of the spec counts, their numbers united; a level-3
    heading does not end a section, a fenced code block is never read.
    """
    lines = _lines(spec_text)
    inside = _fenced(lines)
    numbers: set[int] = set()
    in_section = False
    for i, line in enumerate(lines):
        if inside[i]:
            continue
        if line == "## Acceptance criteria":
            in_section = True
            continue
        if in_section and _LEVEL2.match(line):
            in_section = False
        if in_section:
            matched = _NUMBERED.match(line)
            if matched:
                numbers.add(int(matched.group(1)))
    return numbers


def exempt_by_date(plan_text: str) -> bool:
    """Whether an archived plan without a ledger is exempt by its header date alone.

    Exactly one header line ``date: YYYY-MM-DD`` with a real calendar date
    before the cut-off exempts (decisions.md Q-2); a quoted, commented,
    missing, impossible or doubled date measures instead of exempting.
    """
    lines = _lines(plan_text)
    if not lines or lines[0] != "---":
        return False
    header: list[str] = []
    for line in lines[1:]:
        if line == "---":
            break
        header.append(line)
    else:
        return False  # no closing ---: not a header
    dated = [matched for line in header if (matched := _DATE.fullmatch(line))]
    if len(dated) != 1:
        return False
    try:
        day = date.fromisoformat(dated[0].group(1))
    except ValueError:
        return False
    return day < CUTOFF


def read(path: Path) -> Reading:
    """The file's text, or (None, reason). Reads bytes; never raises."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return None, f"cannot be read ({exc.strerror or exc})"
    try:
        return raw.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "is not valid UTF-8"


def _exists(path: Path) -> bool:
    """Whether path exists; one that cannot be examined counts as present, so the read finding stands."""
    try:
        return path.exists()
    except OSError:
        return True


def _defined(text: str, function: str) -> bool:
    return re.search(rf"^def {function}\(", text, re.M | re.ASCII) is not None


def measure(root: Path) -> tuple[list[tuple[str, int, str]], Tally]:
    """Measure every held plan under root; return the findings and the counts.

    Raises CannotMeasure when root is not a readable directory holding
    ``plans/changes/``.
    """
    if not root.is_dir():
        raise CannotMeasure(f"{root} is not a readable directory")
    changes = root / CHANGES_DIR
    if not changes.is_dir():
        raise CannotMeasure(f"{root} has no {CHANGES_DIR}/ directory")
    archive_dir = changes / ARCHIVE
    try:
        live = sorted(folder for folder in changes.iterdir() if folder.is_dir() and folder.name != ARCHIVE)
        archived = sorted(folder for folder in archive_dir.iterdir() if folder.is_dir()) if archive_dir.is_dir() else []
    except OSError as error:
        # exists but cannot be listed: not a readable directory (criterion 18)
        raise CannotMeasure(f"{changes} cannot be listed ({error.strerror or error})") from error
    findings: list[tuple[str, int, str]] = []
    tally = Tally()
    files: dict[Path, Reading] = {}
    for folder in live:
        _measure_plan(root, folder, False, findings, tally, files)
    for folder in archived:
        _measure_plan(root, folder, True, findings, tally, files)
    return findings, tally


def _measure_plan(
    root: Path,
    folder: Path,
    archived: bool,
    findings: list[tuple[str, int, str]],
    tally: Tally,
    files: dict[Path, Reading],
) -> None:
    """One plan: its section, the spec, the section lines, the entries, the coverage."""
    where = folder.relative_to(root).as_posix()
    plan_rel = f"{where}/plan.md"
    spec_rel = f"{where}/spec.md"
    plan_path = folder / "plan.md"
    try:
        present = plan_path.exists()
    except OSError as error:
        # A directory that cannot be searched: a finding for this plan, the run goes on (criterion 17).
        why = f"cannot be examined ({error.strerror or error})"
        findings.append((plan_rel, 0, f"{plan_rel} {why} — make {where}/ searchable"))
        return
    if not present:
        return  # a change without a plan.md is not examined (criterion 1)
    text, reason = read(plan_path)
    if text is None:
        unread = f"{plan_rel} {reason}"
        findings.append((plan_rel, 0, f"{unread} — a plan the gate cannot read is a plan it cannot hold"))
        return
    lines = _lines(text)
    sections = ledger_sections(lines)
    if not sections:
        if archived and exempt_by_date(text):
            tally.exempt += 1
        else:
            missing = f'{plan_rel} has no "{HEADING}" section'
            findings.append((plan_rel, 0, f"{missing} — add it, with one entry per criterion and proof"))
        return
    if len(sections) > 1:
        doubled = f'{plan_rel} has {len(sections)} "{HEADING}" sections'
        # The second heading's line: one above its first line, or the last line when it holds none.
        second = sections[1][0][0] - 1 if sections[1] else len(lines)
        findings.append((plan_rel, second, f"{doubled} — keep exactly one"))
        return
    if archived:
        tally.archived += 1
    else:
        tally.live += 1

    spec_text, spec_reason = read(folder / "spec.md")
    numbers: set[int] | None = None
    if spec_text is None:
        unread = f"{spec_rel} {spec_reason}"
        findings.append((spec_rel, 0, f"{unread} — the ledger's criterion numbers are read from spec.md"))
    else:
        numbers = criterion_numbers(spec_text)
        if not numbers:
            unnumbered = f'{spec_rel} has no criterion number under "## Acceptance criteria"'
            findings.append((spec_rel, 0, f'{unnumbered} — number them "1. ", "2. ", …'))
            # One finding says it all: with no numbers to compare against, every
            # entry would otherwise be reported as unknown (loop row L2-2).
            numbers = None

    entries: list[Entry] = []
    chain = False  # the line above is an entry or a continuation line
    for number, line in sections[0]:
        if not line:
            chain = False
            continue
        entry = parse_entry(line, number)
        if entry is not None:
            entries.append(entry)
            chain = True
            continue
        if line[0] in " \t" and not _INDENTED_LIST.match(line) and chain:
            continue  # a continuation line continues the entry above, and is not read
        malformed = "the line is in none of the three entry forms"
        findings.append((plan_rel, number, f"{malformed} — write one of {' or '.join(_FORMS)}"))
        chain = False

    for entry in entries:
        if numbers is not None and entry.number not in numbers:
            unknown = f"the entry names criterion {entry.number}, which {spec_rel} does not have"
            findings.append((plan_rel, entry.line, f"{unknown} — correct the number or the spec"))
        if entry.kind == "not a test":
            tally.not_a_test += 1
        elif entry.kind == "test":
            tally.test += 1
            found, why = _file(root, entry.path, files)
            if found is None:
                absent = f'criterion {entry.number}: "{entry.function}" is not held — {entry.path} {why}'
                findings.append((plan_rel, entry.line, f"{absent} — write the test or change the entry"))
            elif not _defined(found, entry.function):
                absent = f'criterion {entry.number}: "{entry.function}" is not defined in {entry.path}'
                findings.append((plan_rel, entry.line, f"{absent} — write the test or change the entry"))
        else:
            tally.not_yet += 1
            if archived:
                promised = f"criterion {entry.number}: an archived plan holds a not-yet-written entry"
                remedy = "write the test and remove `not yet written`, or make it a not-a-test entry"
                findings.append((plan_rel, entry.line, f"{promised} — {remedy}"))
            else:
                found, why = _file(root, entry.path, files)
                if found is None and _exists(root / entry.path):
                    # Only a missing file may stand as not yet written; one it cannot read is a finding.
                    unread = f'criterion {entry.number}: "{entry.function}" — {entry.path} {why}'
                    findings.append((plan_rel, entry.line, f"{unread} — make the file readable UTF-8"))
                elif found is not None and _defined(found, entry.function):
                    written = f'criterion {entry.number}: "{entry.function}" exists'
                    findings.append((plan_rel, entry.line, f"{written} — remove `not yet written` from the entry"))

    if numbers is not None:
        covered = {entry.number for entry in entries}
        for number in sorted(numbers - covered):
            uncovered = f"criterion {number} has no entry in the ledger"
            remedy = "hold it by a test, a not-yet-written or a not-a-test entry"
            findings.append((plan_rel, 0, f"{uncovered} — {remedy}"))


def _file(root: Path, rel: str, files: dict[Path, Reading]) -> Reading:
    """A named test file's text, read once per run."""
    path = root / rel
    if path not in files:
        files[path] = read(path)
    return files[path]


def _s(count: int, word: str) -> str:
    """A count and its noun, pluralised only when the count is not one."""
    if count == 1:
        return f"{count} {word}"
    return f"{count} {word[:-1] + 'ies' if word.endswith('y') else word + 's'}"


def run(root: Path, out: Callable[[str], None] = print) -> int:
    """Run the gate over root; print and return the exit code."""
    try:
        findings, tally = measure(root)
    except CannotMeasure as exc:
        out(f"criterion-ledger: not measured — {exc}")
        return 3
    exempt = f"{_s(tally.exempt, 'archived plan')} dated before {CUTOFF.isoformat()} exempt"
    if findings:
        for path, line, finding in sorted(findings):
            out(f"{path}:{line}: {finding}" if line else f"{path}: {finding}")
        # A change with findings on both its plan.md and its spec.md is one plan.
        plans = len({str(Path(path).parent) for path, _, _ in findings})
        summary = f"criterion-ledger: {len(findings)} findings in {_s(plans, 'plan')}"
        print(summary, file=sys.stderr)
        return 1
    if tally.held == 0:
        out(f"criterion-ledger: examined nothing — no plan.md under {CHANGES_DIR}/ is held; {exempt}")
        return 0
    held = f"held {_s(tally.held, 'plan')} ({tally.live} live, {tally.archived} archived)"
    entries = (
        f"read {_s(tally.entries, 'entry')} "
        f"({tally.test} test, {tally.not_yet} not yet written, {tally.not_a_test} not a test)"
    )
    out(f"criterion-ledger: {held}; {entries}; {exempt}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument(
        "--root", default=".", type=Path, help="repository root to measure (default: the working directory)"
    )
    args = parser.parse_args(argv)
    return run(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
