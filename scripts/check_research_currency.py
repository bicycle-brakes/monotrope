#!/usr/bin/env python3
"""check_research_currency.py — list the research notes whose last review is too old.

The research under `docs/research/` assesses outside tools that change without a
commit here. Every note carries `last_reviewed:` in its YAML header — the day its
content was last checked against its sources. This script reads that one date from
every note and lists the notes whose review is more than 90 days before the day of
the run. It is a report: it decides nothing and turns nothing red (spec criteria 1-11
of plans/changes/research-currency/spec.md).

  * a note is a `*.md` file under `docs/research/`, at any depth, whose name does not
    start with `_` (the index is a reading map, not a source review);
  * the review date is the top-level `last_reviewed:` and nothing else — `updated:`,
    `created:`, the provenance block and the git history are never consulted;
  * a note whose review date cannot be used (no header, no key, empty, not a date,
    later than tomorrow, not UTF-8) is due, first in the order, with the reason;
  * the order is: unusable dates first, then oldest first, ties by path — the same
    tree and the same day of the run give the same bytes;
  * the run only reads. It needs no git, no network and no tracker; its one write is
    the job summary, when `GITHUB_STEP_SUMMARY` names a file.

Usage:
    python3 scripts/check_research_currency.py                    # text
    python3 scripts/check_research_currency.py --format json      # for a re-check agent
    python3 scripts/check_research_currency.py --today 2026-12-20 # pin the day of the run
    python3 scripts/check_research_currency.py --root DIR         # another repository (tests)
Exit: 0 = the list was produced, however many notes are due; 2 = usage;
      3 = not measured (no `docs/research/` or no note in it) — a line beginning
      `research-currency: not measured` is printed on stdout, in either format.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

CORPUS = "docs/research"
# The same number as `plans_registry.py` uses for plans, deliberately not imported:
# a change to the plans rhythm must not move the research rhythm silently.
STALE_AFTER_DAYS = 90
# The shape of `--format json`. A change to a key or its meaning raises it.
SCHEMA_VERSION = 1

# A header may start with a UTF-8 byte-order mark and use CRLF line endings (the form
# of `check_frontmatter_current.py`).
_BLOCK = re.compile(r"^﻿?---\r?\n(.*?)\n---\r?\n", re.S)
# `date.fromisoformat` also takes `20260916`; the date of a header is `YYYY-MM-DD`.
_ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
_TIMESTAMP_TAG = "tag:yaml.org,2002:timestamp"
_REASON_WIDTH = 80


class CannotMeasure(Exception):  # noqa: N818 — a verdict, not an error class
    """Nothing was measured: an empty list here would claim a measurement of nothing."""


class _Loader(yaml.SafeLoader):
    """A SafeLoader that leaves a date-looking scalar a string.

    PyYAML builds a `date` or a `datetime` from `2026-09-16` and raises ValueError on
    `2026-02-30`, which would end the run on one bad note. Whether a value is a date is
    this script's judgement, so the value stays text until then.
    """


_Loader.yaml_implicit_resolvers = {
    first: [(tag, pattern) for tag, pattern in resolvers if tag != _TIMESTAMP_TAG]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


@dataclass(frozen=True)
class Note:
    path: str  # relative to the root, `/`-separated
    last_reviewed: date | None
    age_days: int | None
    due: bool
    problem: str | None


def _shown(value: object) -> str:
    """A header value as one short line for a reason."""
    text = " ".join(str(value).split())
    return text if len(text) <= _REASON_WIDTH else text[: _REASON_WIDTH - 1] + "…"


def review_date(text: str, today: date) -> tuple[date | None, str | None]:
    """`(the review date, None)` or `(None, why there is none)` for one note's text."""
    block = _BLOCK.match(text)
    if not block:
        return None, "no frontmatter"
    try:
        header = yaml.load(block.group(1), Loader=_Loader)  # noqa: S506 — a SafeLoader subclass
    except (yaml.YAMLError, ValueError):
        return None, "frontmatter is not a YAML mapping"
    if not isinstance(header, dict):
        return None, "frontmatter is not a YAML mapping"
    if "last_reviewed" not in header:
        return None, "no last_reviewed"
    value = header["last_reviewed"]
    if value is None or value == "":
        return None, "last_reviewed is empty"
    not_a_date = f"last_reviewed '{_shown(value)}' is not a YYYY-MM-DD date"
    if not isinstance(value, str) or not _ISO.fullmatch(value):
        return None, not_a_date
    try:
        reviewed = date.fromisoformat(value)
    except ValueError:
        return None, not_a_date
    # One day of slack: a review is dated in the maintainer's time zone, the nightly
    # run is in UTC (the same slack `check_frontmatter_current.py` allows).
    if reviewed > today + timedelta(days=1):
        return None, f"last_reviewed {reviewed} is in the future"
    return reviewed, None


def _note(path: str, text: str, today: date) -> Note:
    reviewed, problem = review_date(text, today)
    if reviewed is None:
        return Note(path, None, None, True, problem)
    age = (today - reviewed).days
    return Note(path, reviewed, age, age > STALE_AFTER_DAYS, None)


def measure(root: Path, today: date) -> list[Note]:
    """Every note under `docs/research/` of `root`, in the order of criterion 5."""
    corpus = root / CORPUS
    if not corpus.is_dir():
        raise CannotMeasure(f"{CORPUS}/ is not a directory under {root}")
    files = {
        p.relative_to(root).as_posix(): p for p in corpus.rglob("*.md") if p.is_file() and not p.name.startswith("_")
    }
    if not files:
        raise CannotMeasure(f"{CORPUS}/ under {root} holds no note")
    notes: list[Note] = []
    for rel, path in files.items():
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            notes.append(Note(rel, None, None, True, "not valid UTF-8"))
            continue
        except OSError as exc:
            notes.append(Note(rel, None, None, True, f"cannot be read ({exc.strerror or type(exc).__name__})"))
            continue
        notes.append(_note(rel, text, today))
    return sorted(notes, key=lambda n: (n.problem is None, n.last_reviewed or date.min, n.path))


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------


def _count(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _ago(age: int) -> str:
    if age < 0:
        return "tomorrow"
    if age == 0:
        return "today"
    return f"{_count(age, 'day')} ago"


def _summary_line(notes: list[Note], today: date) -> str:
    due = sum(n.due for n in notes)
    return (
        f"{_count(len(notes), 'note')} under {CORPUS}/, {due} due "
        f"(review more than {STALE_AFTER_DAYS} days before {today})"
    )


def _oldest(notes: list[Note]) -> str:
    first = notes[0]
    if first.last_reviewed is None or first.age_days is None:
        return f"{first.path}, no usable review date ({first.problem})"
    return f"{first.path}, reviewed {first.last_reviewed}, {_ago(first.age_days)}"


def render_text(notes: list[Note], today: date) -> str:
    lines = [f"research-currency: {_summary_line(notes, today)}"]
    for n in notes:
        if not n.due:
            continue
        if n.last_reviewed is None:
            lines.append(f"  due  no date  {n.path} — {n.problem}")
        else:
            lines.append(f"  due  {n.last_reviewed}  {_count(n.age_days or 0, 'day')}  {n.path}")
    lines.append(f"oldest: {_oldest(notes)}")
    return "\n".join(lines) + "\n"


def render_json(notes: list[Note], today: date) -> str:
    doc = {
        "schema_version": SCHEMA_VERSION,
        "today": today.isoformat(),
        "threshold_days": STALE_AFTER_DAYS,
        "corpus": f"{CORPUS}/",
        "notes": [
            {
                "path": n.path,
                "last_reviewed": n.last_reviewed.isoformat() if n.last_reviewed else None,
                "age_days": n.age_days,
                "due": n.due,
                "problem": n.problem,
            }
            for n in notes
        ],
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def render_markdown(notes: list[Note], today: date) -> str:
    lines = ["### Research currency", "", f"{_summary_line(notes, today)}.", ""]
    due = [n for n in notes if n.due]
    if due:
        lines += ["| Reviewed | Days | Note |", "| --- | --- | --- |"]
        for n in due:
            if n.last_reviewed is None:
                lines.append(f"| no date | — | `{_cell(n.path)}` — {_cell(str(n.problem))} |")
            else:
                lines.append(f"| {n.last_reviewed} | {n.age_days} | `{_cell(n.path)}` |")
        lines.append("")
    lines.append(f"Oldest: {_oldest(notes)}.")
    return "\n".join(lines) + "\n"


def _append_summary(markdown: str) -> None:
    """Append to the job summary when the environment names a file; never fail over it."""
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    try:
        with Path(target).open("a", encoding="utf-8") as handle:
            handle.write(markdown + "\n")
    except OSError as exc:
        print(
            f"research-currency: cannot write the job summary ({exc.strerror or type(exc).__name__})", file=sys.stderr
        )


# ---------------------------------------------------------------------------
# the command line
# ---------------------------------------------------------------------------


def _day(value: str) -> date:
    if not _ISO.fullmatch(value):
        raise argparse.ArgumentTypeError(f"'{value}' is not a YYYY-MM-DD date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"'{value}' is not a date ({exc})") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository to measure (default: this one)")
    parser.add_argument("--today", type=_day, default=None, help="the day of the run, YYYY-MM-DD (default: local date)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    today = args.today or date.today()
    try:
        notes = measure(args.root.resolve(), today)
    except CannotMeasure as exc:
        line = f"research-currency: not measured — {exc}"
        print(line)
        _append_summary(f"### Research currency\n\n{line}\n")
        return 3
    print(render_json(notes, today) if args.format == "json" else render_text(notes, today), end="")
    _append_summary(render_markdown(notes, today))
    return 0


if __name__ == "__main__":
    sys.exit(main())
