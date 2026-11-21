#!/usr/bin/env python3
"""check_finding_duplicates.py — a new or changed duplicate row uses the canonical form.

The gate of spec criterion 9 (bead coding-harness-qut1, decisions F-16,
F-26): a finding row added or changed relative to the merge base with
``origin/main`` that marks a duplicate must read exactly

    rejected — duplicate of <ID>[: <reason>]

with several ids joined by `` and `` (``rejected — duplicate of L2-1 and
L2-2: same shell``). Historical rows are evidence and are never demanded a
rewrite: only rows that are new or changed against the merge base are
checked, and rows that move unchanged with their file — ``make archive``
renames the folder and stamps the header — are not new (decisions F-22,
rename-aware ``git diff -M``).

    python3 scripts/check_finding_duplicates.py [--root DIR] [--base REV] [--head REV]

Without ``--head``, the gate compares the merge base against the working tree
(committed, staged, unstaged and untracked ``findings.md`` files, rename-aware
for tracked files). With ``--head REV``, it compares against that commit.

Exit: 0 = nothing found, 1 = findings, 2 = bad usage, 3 = cannot measure.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import findings_reader as reader  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL = re.compile(
    rf"rejected — duplicate of (?P<ids>{reader.FINDING_ID.pattern}"
    rf"(?: and {reader.FINDING_ID.pattern})*)(?:: .+)?"
)
# A row the gate reads: a finding row of the reader's grammar (`table_rows`),
# with a width whose Status cell the reader knows.
RowCells = tuple[str, ...]


class CannotMeasure(Exception):
    """The gate could not read the requested evidence."""


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)


def merge_base(root: Path, head: str) -> str:
    """The merge base with origin/main (the same gate locally and in CI, decisions F-16)."""
    for ref in ("origin/main", "main"):
        done = git(root, "merge-base", ref, head)
        if done.returncode == 0:
            return done.stdout.decode().strip()
    raise CannotMeasure("check-duplicates: cannot measure — no origin/main or main to take the merge base from (3)")


def head_commit(root: Path, rev: str) -> str:
    done = git(root, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if done.returncode != 0:
        raise CannotMeasure(f"check-duplicates: cannot measure — git does not know the revision {rev!r} (3)")
    return done.stdout.decode().strip()


def changed_files(root: Path, base: str, head: str | None = None) -> list[tuple[str | None, str]]:
    """The findings.md files added, changed or renamed between base and head (or working tree), as (old, new) paths.

    An added or untracked file has no old path (None); a deleted file carries no new rows and is skipped.
    """
    diff_args = (
        ("diff", "-M", "-z", "--name-status", base, "--", "plans/changes")
        if head is None
        else ("diff", "-M", "-z", "--name-status", base, head, "--", "plans/changes")
    )
    done = git(root, *diff_args)
    if done.returncode != 0:
        raise CannotMeasure(f"check-duplicates: cannot measure — the diff failed: {done.stderr.decode().strip()} (3)")
    tokens = done.stdout.decode().split("\0")
    pairs: list[tuple[str | None, str]] = []
    deleted: list[str] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        if not status:
            index += 1
            continue
        old: str | None
        if status.startswith(("R", "C")):
            old, new = tokens[index + 1], tokens[index + 2]
            index += 3
        else:
            old = new = tokens[index + 1]
            index += 2
            if status.startswith("A"):
                old = None
            elif status.startswith("D"):
                if old.endswith("/findings.md"):
                    deleted.append(old)
                continue
        if new.endswith("/findings.md"):
            pairs.append((old, new))
    if head is None:
        untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", "plans/changes")
        if untracked.returncode != 0:
            raise CannotMeasure(
                f"check-duplicates: cannot measure — listing untracked files failed: "
                f"{untracked.stderr.decode().strip()} (3)"
            )
        seen = {new for _, new in pairs}
        paths = sorted(p for p in untracked.stdout.decode().split("\0") if p.endswith("/findings.md") and p not in seen)
        # Git cannot detect renames to untracked files. Pair sufficiently similar
        # deleted and untracked files one-to-one before comparing their rows.
        candidates: list[tuple[float, str, str]] = []
        for old in deleted:
            before = git(root, "show", f"{base}:{old}")
            if before.returncode != 0:
                raise CannotMeasure(f"check-duplicates: cannot measure — {old} is not in {base[:12]} (3)")
            for new in paths:
                try:
                    after = (root / new).read_bytes()
                except OSError as exc:
                    raise CannotMeasure(f"check-duplicates: cannot measure — cannot read {new}: {exc} (3)") from None
                score = SequenceMatcher(
                    None, before.stdout.splitlines(keepends=True), after.splitlines(keepends=True), autojunk=False
                ).ratio()
                if score >= 0.5:
                    candidates.append((score, old, new))
        used_old: set[str] = set()
        used_new: set[str] = set()
        for _, old, new in sorted(candidates, key=lambda item: (-item[0], item[1], item[2])):
            if old not in used_old and new not in used_new:
                pairs.append((old, new))
                used_old.add(old)
                used_new.add(new)
        pairs.extend((None, path) for path in paths if path not in used_new)
    return pairs


def _rows_from_text(text: str) -> dict[str, list[RowCells]]:
    rows: dict[str, list[RowCells]] = {}
    for _, cells in reader.table_rows(text):  # the reader's one input grammar
        rows.setdefault(cells[0], []).append(tuple(cells))
    return rows


def rows_at(root: Path, rev: str | None, path: str) -> dict[str, list[RowCells]]:
    """Every readable row of one findings.md at one commit or in the working tree, by id, in file order."""
    if rev is None:
        try:
            raw = (root / path).read_bytes()
        except OSError as exc:
            raise CannotMeasure(f"check-duplicates: cannot measure — cannot read {path}: {exc} (3)") from None
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise CannotMeasure(
                f"check-duplicates: cannot measure — {path} in working tree is not valid UTF-8 (3)"
            ) from None
        return _rows_from_text(text)
    done = git(root, "show", f"{rev}:{path}")
    if done.returncode != 0:
        raise CannotMeasure(f"check-duplicates: cannot measure — {path} is not in {rev[:12]} (3)")
    try:
        text = done.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise CannotMeasure(f"check-duplicates: cannot measure — {path} at {rev[:12]} is not valid UTF-8 (3)") from None
    return _rows_from_text(text)


def marks_duplicate(status: str) -> bool:
    """The row marks a duplicate: a marker naming a row id (a marker without an id is none, criterion 7)."""
    return reader.is_duplicate(status)


def measure(root: Path, base: str, head: str | None = None) -> list[str]:
    """The findings of the gate: changed rows whose duplicate form is not the canonical one."""
    findings: list[str] = []
    for old, new in changed_files(root, base, head):
        before = rows_at(root, base, old) if old is not None else {}
        after = rows_at(root, head, new)
        for row_id, rows in sorted(after.items()):
            remaining = Counter(before.get(row_id, []))
            for cells in rows:
                if remaining[cells]:
                    remaining[cells] -= 1
                    continue  # unchanged occurrence, including in a moved file
                status_cell = reader.status_cell(list(cells))
                if status_cell is None:
                    findings.append(f"{new}:{row_id}: unknown finding row width {len(cells)}")
                    continue
                status = status_cell.strip()
                if not marks_duplicate(status) or CANONICAL.fullmatch(status):
                    continue
                findings.append(
                    f"{new}:{row_id}: a new or changed duplicate row must read "
                    f"`rejected — duplicate of <ID>[: <reason>]` with ids joined by ` and `; found {status!r}"
                )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository to measure (default: this checkout)")
    parser.add_argument("--base", default=None, help="the base revision (default: the merge base with origin/main)")
    parser.add_argument("--head", default=None, help="the head revision (default: working tree)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        head = head_commit(root, args.head) if args.head is not None else None
        if args.base:
            base = head_commit(root, args.base)
        else:
            base = merge_base(root, head if head is not None else head_commit(root, "HEAD"))
        findings = measure(root, base, head)
    except CannotMeasure as exc:
        print(exc, file=sys.stderr)
        return 3
    if findings:
        for finding in findings:
            print(finding)
        print(f"check-duplicates: {len(findings)} finding(s)", file=sys.stderr)
        return 1
    print("check-duplicates: every new or changed duplicate row uses the canonical form")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
