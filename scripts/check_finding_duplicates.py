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

Exit: 0 = nothing found, 1 = findings, 2 = bad usage, 3 = cannot measure.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import findings_reader as reader  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL = re.compile(
    r"rejected — duplicate of (?P<ids>[A-Za-z0-9]{1,8}(?:-[A-Za-z]?\d+)+"
    r"(?: and [A-Za-z0-9]{1,8}(?:-[A-Za-z]?\d+)+)*)(?:: .+)?"
)
# A row the gate reads: a table line that is no furniture, a finding id in its
# first cell, and a width whose Status cell the reader knows.
RowCells = tuple[str, ...]


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)


def merge_base(root: Path, head: str) -> str:
    """The merge base with origin/main (the same gate locally and in CI, decisions F-16)."""
    for ref in ("origin/main", "main"):
        done = git(root, "merge-base", ref, head)
        if done.returncode == 0:
            return done.stdout.decode().strip()
    raise SystemExit("check-duplicates: cannot measure — no origin/main or main to take the merge base from (3)")


def head_commit(root: Path, rev: str) -> str:
    done = git(root, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if done.returncode != 0:
        raise SystemExit(f"check-duplicates: cannot measure — git does not know the revision {rev!r} (3)")
    return done.stdout.decode().strip()


def changed_files(root: Path, base: str, head: str) -> list[tuple[str, str]]:
    """The findings.md files added, changed or renamed between base and head, as (old, new) paths."""
    done = git(root, "diff", "-M", "-z", "--name-status", base, head, "--", "plans/changes")
    if done.returncode != 0:
        raise SystemExit(f"check-duplicates: cannot measure — the diff failed: {done.stderr.decode().strip()} (3)")
    tokens = done.stdout.decode().split("\0")
    pairs: list[tuple[str, str]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        if not status:
            index += 1
            continue
        if status.startswith("R"):
            old, new = tokens[index + 1], tokens[index + 2]
            index += 3
        else:
            old = new = tokens[index + 1]
            index += 2
        if new.endswith("/findings.md"):
            pairs.append((old, new))
    return pairs


def rows_at(root: Path, rev: str, path: str) -> dict[str, list[RowCells]]:
    """Every readable row of one findings.md at one commit, by id, in file order."""
    done = git(root, "show", f"{rev}:{path}")
    if done.returncode != 0:
        raise SystemExit(f"check-duplicates: cannot measure — {path} is not in {rev[:12]} (3)")
    try:
        text = done.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise SystemExit(f"check-duplicates: cannot measure — {path} at {rev[:12]} is not valid UTF-8 (3)") from None
    rows: dict[str, list[RowCells]] = {}
    for line in text.splitlines():
        cells = reader.split_row(line)
        if cells is None or reader.furniture(cells) or not any(cell.strip() for cell in cells):
            continue
        if reader.ROW_ID.fullmatch(cells[0]) is None or reader.status_cell(cells) is None:
            continue
        rows.setdefault(cells[0], []).append(tuple(cells))
    return rows


def marks_duplicate(status: str) -> bool:
    """The row marks a duplicate: a marker in its status, or the bare canonical leading word."""
    return reader.DUPLICATE_MARKER.search(status) is not None or reader.normalized_status(status).startswith("duplicate")


def measure(root: Path, base: str, head: str) -> list[str]:
    """The findings of the gate: changed rows whose duplicate form is not the canonical one."""
    findings: list[str] = []
    for old, new in changed_files(root, base, head):
        before = rows_at(root, base, old)
        after = rows_at(root, head, new)
        for row_id, rows in sorted(after.items()):
            if before.get(row_id) == rows:
                continue  # an unchanged row is not new, whatever happened to its file (F-22)
            for cells in rows:
                status = (reader.status_cell(list(cells)) or "").strip()
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
    parser.add_argument("--head", default="HEAD", help="the head revision (default: HEAD)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    head = head_commit(root, args.head)
    base = head_commit(root, args.base) if args.base else merge_base(root, head)
    findings = measure(root, base, head)
    if findings:
        for finding in findings:
            print(finding)
        print(f"check-duplicates: {len(findings)} finding(s)", file=sys.stderr)
        return 1
    print("check-duplicates: every new or changed duplicate row uses the canonical form")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
