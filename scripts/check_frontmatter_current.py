#!/usr/bin/env python3
"""check_frontmatter_current.py — a document header must not be older than its document.

A header that says a document is older than its content misleads every reader,
and nothing noticed. This check holds every Markdown file whose prefix in
`provenance.yaml` declares `frontmatter: required` to one rule: its `updated:`
date is not earlier than the date of the file's last change.

  * the reference date of a clean file is the committer date (in the offset
    recorded in the commit) of the newest non-merge commit that changed it —
    what `git log -1 --no-merges -- <file>` answers with literal pathspecs and
    `log.follow` off, read for every clean file from one batched `git log`;
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
import heapq
import itertools
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import venv_guard  # noqa: F401
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

# A header may start with a UTF-8 byte-order mark and use CRLF line endings. With CRLF each
# line of the captured block keeps its trailing `\r`; the stamp relies on that.
_BLOCK = re.compile(r"^﻿?---\r?\n(.*?)\n---\r?\n", re.S)
_UPDATED_LINE = re.compile(r"^updated:")
# YAML reads `2026-09-10  # stamped` as the date, so a comment after whitespace is not part of the value.
_VALUE = re.compile(r"""^["']?(\d{4}-\d{2}-\d{2})["']?\s*(?:\s#.*)?$""")


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
    if shallow.returncode != 0:
        # A git without the flag (before 2.15) cannot say. That is not "full history".
        raise CannotMeasure(
            f"cannot tell whether {root} is a shallow clone "
            f"(git rev-parse --is-shallow-repository failed: {shallow.stderr.strip() or shallow.returncode})"
        )
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
    zeilen = [z for z in m.group(1).split("\n") if _UPDATED_LINE.match(z)]  # CRLF: each keeps its `\r`
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


# One `git log` over the whole history replaces one `git log -1 -- <file>` per clean file. It prints every
# commit reachable from HEAD with its diff against each parent (`--diff-merges=separate`), and the walk each
# per-file call would make is replayed here: newest committer timestamp first, ties in insertion order, a
# merge followed only to its first parent that leaves the file unchanged (git's default history
# simplification), merges never shown (`--no-merges`). The call has no pathspec, so nothing in a file name is
# read as a glob or as pathspec magic; `log.follow` is forced off, the root diff and plain output forced on.
HISTORY_FORMAT = "%x01%H %T %ct %cs %h %P"
HISTORY_ARGS = (
    "--literal-pathspecs",
    "-c",
    "log.follow=false",
    "-c",
    "log.showRoot=true",
    "-c",
    "log.showSignature=false",
    "log",
    "--no-color",
    f"--format={HISTORY_FORMAT}",
    "--raw",
    "-z",
    "--no-renames",
    "--diff-merges=separate",
    "--relative",
    "HEAD",
    "--",
)
ABSENT_MODE = "000000"
STDERR_LINES = 20
STDERR_CHARS = 2000
STDERR_CUT = "[stderr truncated: only its end is shown]"


def stderr_tail(text: str) -> str:
    """The end of a failed command's stderr: at most STDERR_LINES lines and STDERR_CHARS characters, unredacted."""
    zeilen = text.rstrip("\n").split("\n")
    cut = len(zeilen) > STDERR_LINES
    rest = "\n".join(zeilen[-STDERR_LINES:])
    if len(rest) > STDERR_CHARS:
        rest = rest[-STDERR_CHARS:]
        cut = True
    return f"{STDERR_CUT}\n{rest}" if cut else rest


@dataclass
class _Commit:
    tree: str
    when: int
    day: str
    short: str
    parents: list[str]
    # Each diff git printed for this commit, in parent order; a parent whose diff is empty prints none.
    # A diff maps a path to (old mode, old object, new mode, new object).
    printed: list[dict[str, tuple[str, str, str, str]]] = field(default_factory=list)


class _History:
    """The parsed batch, and the per-file walk replayed over it."""

    def __init__(self, command: str, output: str) -> None:
        self.command = command
        self.head: str | None = None
        self.commits: dict[str, _Commit] = {}
        self._diffs: dict[str, list[dict[str, tuple[str, str, str, str]]]] = {}
        self._parse(output)

    def _fail(self, what: str) -> CannotMeasure:
        return CannotMeasure(f"history batch `{self.command}` {what}")

    def _parse(self, output: str) -> None:
        tokens = output.split("\0")
        current: _Commit | None = None
        diff: dict[str, tuple[str, str, str, str]] = {}
        i = 0
        while i < len(tokens):
            token = tokens[i].lstrip("\n")
            i += 1
            if not token:
                continue
            if token.startswith("\x01"):
                teile = token[1:].split(" ")
                if len(teile) < 5 or not teile[2].isdigit():
                    raise self._fail(f"printed an unreadable commit line: {token[1:200]!r}")
                sha = teile[0]
                current = self.commits.get(sha)
                if current is None:
                    current = _Commit(teile[1], int(teile[2]), teile[3], teile[4], [p for p in teile[5:] if p])
                    self.commits[sha] = current
                    if self.head is None:
                        self.head = sha
                diff = {}
                current.printed.append(diff)
                continue
            meta = token[1:].split()
            if not token.startswith(":") or current is None or len(meta) < 5 or i >= len(tokens):
                raise self._fail(f"printed an unreadable diff line: {token[:200]!r}")
            diff[tokens[i]] = (meta[0], meta[2], meta[1], meta[3])
            i += 1
        for commit in self.commits.values():
            commit.printed = [d for d in commit.printed if d]

    def commit(self, sha: str) -> _Commit:
        found = self.commits.get(sha)
        if found is None:
            raise self._fail(f"did not print commit {sha}, a parent of a printed commit")
        return found

    def diffs(self, sha: str) -> list[dict[str, tuple[str, str, str, str]]]:
        """The diff against each parent in order (a root commit: against the empty tree)."""
        known = self._diffs.get(sha)
        if known is not None:
            return known
        c = self.commit(sha)
        n = max(1, len(c.parents))
        k = len(c.printed)
        if k == n:
            result = list(c.printed)
        elif k == 0:
            result = [{} for _ in range(n)]
        elif k > n:
            raise self._fail(f"printed {k} diffs for commit {sha} with {n} parents")
        else:
            result = self._place(sha, c)
        self._diffs[sha] = result
        return result

    def _place(self, sha: str, c: _Commit) -> list[dict[str, tuple[str, str, str, str]]]:
        """Which parents the printed diffs of a merge belong to, when some parents printed none."""
        result: list[dict[str, tuple[str, str, str, str]]] = [{} for _ in c.parents]
        # A parent with the merge's own tree has an empty diff; the others usually have one.
        candidates = [i for i, p in enumerate(c.parents) if self.commit(p).tree != c.tree]
        if len(candidates) == len(c.printed):
            for i, printed in zip(candidates, c.printed, strict=True):
                result[i] = printed
            return result
        # Below a subdirectory root a parent can differ outside it only. A printed diff belongs to the next
        # candidate whose version of one of its paths is the diff's old side; an empty one holds the new side.
        j = 0
        for i in candidates:
            if j == len(c.printed):
                break
            path, (old_mode, old_object, _, _) = next(iter(c.printed[j].items()))
            old = None if old_mode == ABSENT_MODE else (old_mode, old_object)
            if self.version(c.parents[i], path) == old:
                result[i] = c.printed[j]
                j += 1
        if j != len(c.printed):
            raise self._fail(f"printed diffs for merge {sha} that match none of its parents")
        return result

    def version(self, sha: str, path: str) -> tuple[str, str] | None:
        """(mode, object) of a path at a commit, or None where it does not exist."""
        while True:
            change = self.diffs(sha)[0].get(path)
            if change is not None:
                return None if change[2] == ABSENT_MODE else (change[2], change[3])
            parents = self.commit(sha).parents
            if not parents:
                return None
            sha = parents[0]

    def dates(self, targets: set[str]) -> dict[str, tuple[str, str]]:
        """Per target the `%cs %h` of the first commit its own `git log -1 --no-merges -- <path>` would show."""
        for sha in reversed(self.commits):  # oldest first, so a merge's ancestors are placed before it
            self.diffs(sha)
        touched: dict[tuple[str, int], set[str]] = {}

        def changed(sha: str, nth: int) -> set[str]:
            # A literal pathspec also matches everything below it, should a held name once have been a directory.
            key = (sha, nth)
            if key not in touched:
                hits: set[str] = set()
                for path in self.diffs(sha)[nth]:
                    if path in targets:
                        hits.add(path)
                    cut = path.find("/")
                    while cut != -1:
                        if path[:cut] in targets:
                            hits.add(path[:cut])
                        cut = path.find("/", cut + 1)
                touched[key] = hits
            return touched[key]

        found: dict[str, tuple[str, str]] = {}
        pending = set(targets)
        queue: list[tuple[int, int, str, set[str]]] = []
        order = itertools.count()
        seen: dict[str, set[str]] = {}

        def push(sha: str, paths: set[str]) -> None:
            # git adds a commit to one file's walk once; here each file keeps that rule for itself.
            already = seen.setdefault(sha, set())
            new = paths - already
            if new:
                already |= new
                heapq.heappush(queue, (-self.commit(sha).when, next(order), sha, new))

        if self.head is None or not pending:
            return found
        push(self.head, pending)
        while queue and pending:
            _, _, sha, paths = heapq.heappop(queue)
            live = paths & pending
            if not live:
                continue
            c = self.commits[sha]
            if len(c.parents) <= 1:
                hit = live & changed(sha, 0)
                for f in hit:
                    found[f] = (c.day, c.short)
                pending -= hit
                if c.parents and live - hit:
                    push(c.parents[0], live - hit)
                continue
            # A merge: each file follows the first parent it is unchanged against, or every parent if none.
            follow: list[set[str]] = []
            rest = live
            for nth in range(len(c.parents)):
                follow.append(rest - changed(sha, nth))
                rest = rest & changed(sha, nth)
            for parent, paths_here in zip(c.parents, follow, strict=True):
                if paths_here | rest:
                    push(parent, paths_here | rest)
        return found


def history_dates(root: Path, targets: set[str]) -> dict[str, tuple[str, str]]:
    """`%cs %h` for every target with history, from one batched `git log`."""
    command = shlex.join(["git", "-C", str(root), *HISTORY_ARGS])
    erg = _git(root, *HISTORY_ARGS)
    if erg.returncode != 0:
        raise CannotMeasure(
            f"history batch `{command}` failed with exit {erg.returncode}; stderr:\n{stderr_tail(erg.stderr)}"
        )
    return _History(command, erg.stdout).dates(targets)


def reference_dates(root: Path, files: list[str], today: date) -> dict[str, tuple[date, str]]:
    """Per file: the date its `updated:` must reach, and where that date comes from."""
    dirty = set(_git_z(root, "diff", "--name-only", "--no-renames", "--relative", "-z", "HEAD"))
    dirty |= set(_git_z(root, "ls-files", "-z", "--others", "--exclude-standard"))
    clean = {f for f in files if f not in dirty}
    dated = history_dates(root, clean) if clean else {}
    out: dict[str, tuple[date, str]] = {}
    for f in files:
        if f in dirty:
            out[f] = (today, "uncommitted")
            continue
        if f not in dated:
            raise CannotMeasure(f"git log cannot date {f}: no commit changed it")
        tag, kurz = dated[f]
        out[f] = (date.fromisoformat(tag), kurz)
    return out


def findings(root: Path, today: date, utc_today: date) -> list[tuple[str, str, str]]:
    """(path, kind, detail) for every held file that is reported. Empty = green."""
    files = held_files(root)
    if not files:
        # A gate over an empty set cannot bite, and green here would say it did.
        raise CannotMeasure(
            "provenance.yaml holds no document: no `frontmatter: required` prefix matches a Markdown file, "
            "so the check measures nothing"
        )
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


class CannotStamp(Exception):  # noqa: N818 — a verdict, not an error class
    """The file cannot be edited without guessing. Named by the caller, left unchanged."""


def stamped(text: str, today: date) -> str:
    """The text with its header's `updated:` set to today, by editing one line; unchanged without a header.

    The pure half of ``stamp``: a writer that must replace a file in one atomic step (the research append,
    deep review RS-2-6) stamps the bytes it is about to write instead of rewriting the file a second time.
    """
    m = _BLOCK.match(text)
    if not m:
        return text
    zeilen = m.group(1).split("\n")
    neu = f"updated: {today.isoformat()}"
    vorhanden = [i for i, z in enumerate(zeilen) if _UPDATED_LINE.match(z)]
    if len(vorhanden) > 1:
        return text
    if vorhanden:
        # A CRLF line keeps its `\r`; the value and anything after it are replaced.
        zeilen[vorhanden[0]] = neu + ("\r" if zeilen[vorhanden[0]].endswith("\r") else "")
    else:
        nach = [i for i, z in enumerate(zeilen) if z.startswith("last_reviewed:")]
        stelle = nach[0] if nach else len(zeilen) - 1
        zeilen.insert(stelle + 1, neu + ("\r" if zeilen[stelle].endswith("\r") else ""))
    return text[: m.start(1)] + "\n".join(zeilen) + text[m.end(1) :]


def stamp(path: Path, today: date) -> bool:
    """Set `updated:` to today by editing one line. True when the file changed.

    Raises CannotStamp for a file that is not valid UTF-8: reading it with replacement
    characters and writing it back would change bytes outside the line.
    """
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CannotStamp(f"not valid UTF-8 ({exc.reason} at byte {exc.start})") from exc
    ergebnis = stamped(text, today)
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
        refused = 0
        for f, art, detail in befunde:
            if art in STAMPABLE:
                try:
                    stamp(root / f, today)
                except CannotStamp as exc:
                    print(f"{f}: {art} — not stamped, {exc}; the file is left unchanged")
                    refused += 1
                    continue
                print(f"stamped {f} ({art}) -> updated: {today}")
            else:
                rest.append((f, art, detail))
        for f, art, _ in rest:
            print(f"{f}: {art} — a stamp cannot repair this; edit the header by hand")
        return 1 if rest or refused else 0

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
