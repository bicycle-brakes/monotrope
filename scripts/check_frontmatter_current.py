#!/usr/bin/env python3
"""check_frontmatter_current.py — a document header must not be older than its document.

A header that says a document is older than its content misleads every reader,
and nothing noticed. This check holds every Markdown file whose prefix in
`provenance.yaml` declares `frontmatter: required` to one rule: its `updated:`
date is not earlier than the date of the file's last change.

  * the reference date of a clean file is the committer date (in the offset
    recorded in the commit) of the newest non-merge commit that changed it;
  * the reference date of an untracked or modified file is today;
  * a shallow clone cannot answer the question and is refused, not guessed at.

`--stamp` sets `updated:` to today in every file reported for a missing,
unreadable, stale or future `updated:`. It edits that one line and nothing else.

Usage:
    python3 scripts/check_frontmatter_current.py             # measure
    python3 scripts/check_frontmatter_current.py --stamp     # repair what a stamp can repair
    python3 scripts/check_frontmatter_current.py --root DIR  # another repository (tests)
Exit: 0 = every held file is current, 1 = findings, 3 = could not measure.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

FIX_COMMAND = "python3 scripts/check_frontmatter_current.py --stamp"

# What `read_updated` can say instead of a date.
NO_FRONTMATTER = "no-frontmatter"
MISSING = "missing"
DUPLICATE = "duplicate"
UNREADABLE = "unreadable"
STALE = "stale"
FUTURE = "future"

# A stamp repairs these. The other two need a person: there is no header to
# write into, or two lines and no way to tell which one is meant.
STAMPABLE = (MISSING, UNREADABLE, STALE, FUTURE)

_BLOCK = re.compile(r"^---\n(.*?)\n---\n", re.S)
_UPDATED_LINE = re.compile(r"^updated:")
_VALUE = re.compile(r"""^["']?(\d{4}-\d{2}-\d{2})["']?\s*$""")


class CannotMeasure(Exception):  # noqa: N818 — a verdict, not an error class
    """The question cannot be answered here. Exit 3, nothing measured."""


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def _git_z(root: Path, *args: str) -> list[str]:
    erg = _git(root, *args)
    if erg.returncode != 0:
        raise CannotMeasure(f"git {' '.join(args)} failed: {erg.stderr.strip() or erg.returncode}")
    return [p for p in erg.stdout.split("\0") if p]


def preflight(root: Path) -> None:
    """Refuse to measure where the answer would be a guess."""
    try:
        inside = _git(root, "rev-parse", "--is-inside-work-tree")
    except FileNotFoundError as exc:
        raise CannotMeasure("git is not installed") from exc
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise CannotMeasure(f"{root} is not a git work tree")
    if _git(root, "rev-parse", "--verify", "HEAD").returncode != 0:
        raise CannotMeasure(f"{root} has no commit yet — there is no last change to compare with")
    shallow = _git(root, "rev-parse", "--is-shallow-repository")
    if shallow.stdout.strip() == "true":
        raise CannotMeasure(
            "this is a shallow clone: git log would return the checked-out commit for every file. "
            "Check out the full history (`fetch-depth: 0` in CI; the gate declares `needs_history`) "
            "or run `git fetch --unshallow`."
        )


# ---------------------------------------------------------------------------
# which files are held
# ---------------------------------------------------------------------------


def load_map(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """`paths:` and `excluded:` of the provenance map, or CannotMeasure."""
    karte = root / "provenance.yaml"
    try:
        doc = yaml.safe_load(karte.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CannotMeasure(f"cannot read {karte}: {exc}") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("paths"), list):
        raise CannotMeasure(f"{karte} has no `paths:` list")
    excluded = doc.get("excluded") or []
    if not isinstance(excluded, list):
        raise CannotMeasure(f"{karte}: `excluded:` is not a list")
    return doc["paths"], [str(e) for e in excluded]


def is_held(rel: str, paths: list[dict[str, Any]], excluded: list[str]) -> bool:
    """Criterion 1: a Markdown file, not excluded, whose longest prefix says `required`."""
    if not rel.endswith(".md"):
        return False
    if any(rel.startswith(e) for e in excluded):
        return False
    treffer = [p for p in paths if rel.startswith(str(p.get("prefix", "")))]
    if not treffer:
        return False
    laengster = max(treffer, key=lambda p: len(str(p["prefix"])))
    return laengster.get("frontmatter") == "required"


def held_files(root: Path) -> list[str]:
    """Tracked or untracked-but-not-ignored, present on disk, held by the map."""
    paths, excluded = load_map(root)
    dateien = _git_z(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    return sorted({f for f in dateien if is_held(f, paths, excluded) and (root / f).is_file()})


# ---------------------------------------------------------------------------
# what a header says
# ---------------------------------------------------------------------------


def read_updated(text: str) -> str | date:
    """The `updated:` date of a header, or the reason there is none."""
    m = _BLOCK.match(text)
    if not m:
        return NO_FRONTMATTER
    zeilen = [z for z in m.group(1).split("\n") if _UPDATED_LINE.match(z)]
    if not zeilen:
        return MISSING
    if len(zeilen) > 1:
        return DUPLICATE
    wert = _VALUE.match(zeilen[0][len("updated:") :].strip())
    if not wert:
        return UNREADABLE
    try:
        return date.fromisoformat(wert.group(1))
    except ValueError:
        return UNREADABLE


# ---------------------------------------------------------------------------
# what it must not be older than
# ---------------------------------------------------------------------------


def reference_dates(root: Path, files: list[str], today: date) -> dict[str, tuple[date, str]]:
    """Per file: the date its `updated:` must reach, and where that date comes from."""
    dirty = set(_git_z(root, "diff", "--name-only", "--no-renames", "--relative", "-z", "HEAD"))
    dirty |= set(_git_z(root, "ls-files", "-z", "--others", "--exclude-standard"))
    out: dict[str, tuple[date, str]] = {}
    for f in files:
        if f in dirty:
            out[f] = (today, "uncommitted")
            continue
        erg = _git(root, "log", "-1", "--no-merges", "--format=%cs %h", "--", f)
        zeile = erg.stdout.strip()
        if erg.returncode != 0 or not zeile:
            raise CannotMeasure(f"git log cannot date {f}: {erg.stderr.strip() or 'no commit changed it'}")
        tag, kurz = zeile.split(" ", 1)
        out[f] = (date.fromisoformat(tag), kurz)
    return out


def findings(root: Path, today: date, utc_today: date) -> list[tuple[str, str, str]]:
    """(path, kind, detail) for every held file that is reported. Empty = green."""
    files = held_files(root)
    refs = reference_dates(root, files, today)
    grenze = utc_today + timedelta(days=1)
    befunde: list[tuple[str, str, str]] = []
    for f in files:
        gelesen = read_updated((root / f).read_bytes().decode("utf-8", errors="replace"))
        if isinstance(gelesen, str):
            befunde.append((f, gelesen, ""))
            continue
        ref, woher = refs[f]
        if gelesen < ref:
            befunde.append((f, STALE, f"updated {gelesen} is older than its last change {ref} ({woher})"))
        elif gelesen > grenze:
            befunde.append((f, FUTURE, f"updated {gelesen} is later than tomorrow (UTC) {grenze}"))
    return befunde


# ---------------------------------------------------------------------------
# the stamp
# ---------------------------------------------------------------------------


def stamp(path: Path, today: date) -> bool:
    """Set `updated:` to today by editing one line. True when the file changed."""
    text = path.read_bytes().decode("utf-8")
    m = _BLOCK.match(text)
    if not m:
        return False
    zeilen = m.group(1).split("\n")
    neu = f"updated: {today.isoformat()}"
    vorhanden = [i for i, z in enumerate(zeilen) if _UPDATED_LINE.match(z)]
    if len(vorhanden) > 1:
        return False
    if vorhanden:
        zeilen[vorhanden[0]] = neu
    else:
        nach = [i for i, z in enumerate(zeilen) if z.startswith("last_reviewed:")]
        zeilen.insert(nach[0] + 1 if nach else len(zeilen), neu)
    ergebnis = text[: m.start(1)] + "\n".join(zeilen) + text[m.end(1) :]
    if ergebnis == text:
        return False
    path.write_bytes(ergebnis.encode("utf-8"))
    return True


# ---------------------------------------------------------------------------
# the command line
# ---------------------------------------------------------------------------


def run(root: Path, do_stamp: bool, today: date, utc_today: date) -> int:
    try:
        preflight(root)
        befunde = findings(root, today, utc_today)
        gezaehlt = len(held_files(root))
    except CannotMeasure as exc:
        print(f"NOT MEASURED: {exc}", file=sys.stderr)
        return 3

    if do_stamp:
        rest: list[tuple[str, str, str]] = []
        for f, art, detail in befunde:
            if art in STAMPABLE:
                stamp(root / f, today)
                print(f"stamped {f} ({art}) -> updated: {today}")
            else:
                rest.append((f, art, detail))
        for f, art, _ in rest:
            print(f"{f}: {art} — a stamp cannot repair this; edit the header by hand")
        return 1 if rest else 0

    if not befunde:
        print(f"frontmatter-current: {gezaehlt} held documents, every `updated:` is current.")
        return 0
    for f, art, detail in befunde:
        print(f"{f}: {art}" + (f" — {detail}" if detail else ""))
    print(f"fix: {FIX_COMMAND}")
    if any(a in (NO_FRONTMATTER, DUPLICATE) for _, a, _ in befunde):
        print(f"({NO_FRONTMATTER} and {DUPLICATE} need a hand edit; the stamp names them and leaves them alone.)")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stamp", action="store_true", help="set `updated:` to today where a stamp can repair it")
    ap.add_argument("--root", type=Path, default=REPO_ROOT, help="repository to measure (default: this one)")
    args = ap.parse_args()
    return run(args.root.resolve(), args.stamp, date.today(), datetime.now(UTC).date())


if __name__ == "__main__":
    sys.exit(main())
