#!/usr/bin/env python3
"""check_interview_minimums.py — the phase-1a interview is owed where minimums stand.

The rules are the maintainer's ten decisions of 2026-10-08
(`plans/changes/archive/2026-10-08-interview-minimums/decisions.md`):

- a `feature` owes at least three counted interview records;
- a change whose diff creates or changes a file under `docs/adr/` owes five,
  whatever its class; a feature that is also an ADR change owes five in
  total, never the sum (Q-1);
- a `spike` owes three counted records — learning goal, time budget,
  expected outcome — or a skip record with its reason (Q-3);
- a `bounded` change owes at least one counted record or a skip record with
  its reason (Q-6);
- an `architectural` change owes five only when its diff touches `docs/adr/`.

Counted means: `status: answered`, `answered_by: maintainer`, and the first
occurrence of its question id in the file (Q-5). Agent answers, open
questions and repeated confirmations do not count. A skip record is a
`## SKIP · interview` block with `status: skipped` and a non-empty `reason:`;
a skip without its reason is not a skip. This check counts documented human
answers; it cannot see who wrote them — the merge confirms them (ADR 0008),
exactly the limit `check_adr_answers.py` states for its own file.

Prospective only (Q-4, Q-8): a change is subject when its spec `date` is
later than `CUTOFF`; the stock, active and archived, stays exempt.

The diff is the `stage2.change_diff()` states — `git diff <base>` covers
committed, staged and unstaged paths, untracked files come from
`ls-files --others` — restricted to `docs/adr/**`, attributed to the owning
change: the `plans/changes/<name>/` paths the same diff touches (F-5). A diff
that touches an ADR and owns no change, or more than one, is a finding. A
change folder the diff touches through its `plan.md` alone is not an owner:
a plan edit is a ledger migration, not the home of an ADR's answers
(criterion-test-ledger, bead coding-harness-909, 2026-10-11 — one ADR draft
lands beside four migrated plans), and the five answers still answer for
exactly one folder.

Base rule (Q-7): a genuine checkout of `main` compares against the first
parent (`HEAD^`); every other state — feature branch, detached HEAD,
worktree — compares against `merge-base(HEAD, origin/main)`. When no base
can be built, the gate says so with exit 3 instead of guessing green
(bead coding-harness-4t8's rule: unmeasured is red on a block gate).

Usage:
    python3 scripts/check_interview_minimums.py                # this repository
    python3 scripts/check_interview_minimums.py --root DIR     # another tree (tests)
    python3 scripts/check_interview_minimums.py --change NAME  # one change (the spec gate)
Exit: 0 = nothing found, 1 = findings, 3 = could not measure.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The merge date of plans/changes/archive/2026-10-08-interview-minimums — the cut-off the
# maintainer set (decisions.md Q-4). A change is subject when its spec date
# is strictly later (Q-8). Changing this constant changes when the rule
# began; it is a governance act, stated in docs/WORKFLOW.md beside this gate.
CUTOFF = date(2026, 10, 8)

CHANGES_DIR = "plans/changes"
ARCHIVE = "archive"
ADR_DIR = "docs/adr"

CLASSES = ("spike", "bounded", "feature", "architectural")
MINIMUMS = {"feature": 3, "spike": 3, "bounded": 1, "architectural": 0}

# A first line `---`, the header, the next line that is `---` — the same
# block rule check_adr_answers.py parses spec headers with, byte for byte,
# so the two gates cannot disagree about what a header is.
_BLOCK = re.compile(r"\A﻿?---\r?\n(.*?)^---[ \t]*\r?$", re.S | re.M)
_CLASS_LINE = re.compile(
    r"""^class:[ \t]+(?:"([^"\n]*)"|'([^'\n]*)'|([^\s"'#]\S*))(?:[ \t]+\#.*)?[ \t]*\r?$""",
    re.M,
)
_DATE_LINE = re.compile(r"^date:[ \t]*(\S+)(?:[ \t]+\#.*)?[ \t]*\r?$", re.M)

# One interview record: `## Q-<id> · <title>` and its field lines. One skip
# record: `## SKIP · interview` with `status: skipped` and a `reason:`.
# The `## ` itself is split away before these match the heading.
_RECORD = re.compile(r"^(Q-[^\s·]+)[ \t]*·[ \t]*(.*)$")
_SKIP_HEADING = re.compile(r"^SKIP[ \t]*·[ \t]*interview[ \t]*$")
_FIELDS = ("asked", "answer", "answered_by", "status", "reason")
_FIELD_LINE = re.compile(r"^(?P<name>" + "|".join(_FIELDS) + r"):[ \t]*(?P<value>.*)$")


class CannotMeasure(Exception):  # noqa: N818 — a verdict, not an error class
    """The question cannot be answered here. Exit 3, nothing measured."""


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise CannotMeasure(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout.strip()


def _mainline_ci() -> bool:
    """True in the hosted run that pushes the main line: the derived workflow
    checks out a detached HEAD, so the branch name cannot speak there."""
    return os.environ.get("GITHUB_REF") == "refs/heads/main"


def _base(root: Path) -> str:
    """The comparison base (decisions.md Q-7 and its addendum, loop row L1-2,
    phase-6 rows F-13/F-14/F-15): the first parent on the main line — a
    genuine `main` checkout or the hosted main-line run — else the merge base
    with `origin/main`. A detached HEAD sitting at `origin/main` cannot
    delimit the committed landfall and is NOT MEASURED (exit 3), never
    silently green: on a named branch HEAD equal to the merge base proves
    nothing was committed beyond main, detached it proves nothing."""
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if branch == "main" or _mainline_ci():
        return _git(root, "rev-parse", "HEAD^")
    merge_base = _git(root, "merge-base", "HEAD", "origin/main")
    if branch != "HEAD":
        # a named branch: HEAD == merge base proves nothing was committed
        # beyond main, so the merge base (even when equal to HEAD) is exact
        return merge_base
    if merge_base != _git(root, "rev-parse", "HEAD"):
        return merge_base
    raise CannotMeasure(
        "detached HEAD at origin/main — the committed delta since the base "
        "cannot be delimited; check out main or a named branch"
    )


def _changed_paths(root: Path) -> set[str]:
    """Everything the measured diff holds: committed and unstaged paths
    against the base, the staged index state against the base (phase-6 row
    F-16 — a staged edit whose working file matches the base hides from the
    working-tree diff), and untracked files — the change_diff states."""
    base = _base(root)
    flags = ["--name-only", "--no-renames", "-z"]
    worktree = _git(root, "diff", *flags, base).split("\0")
    index = _git(root, "diff", "--cached", *flags, base).split("\0")
    untracked = _git(root, "ls-files", "-z", "--others", "--exclude-standard").split("\0")
    return {name for name in [*worktree, *index, *untracked] if name}


def _active_changes(root: Path) -> list[Path]:
    """Every change folder that carries a spec — active and archived. The
    cut-off decides who is subject, not the folder's place (phase-6 row
    F-11): a change dated after the cut-off owes its interview also once
    archived, while the stock stays exempt wherever it lies."""
    changes = root / CHANGES_DIR
    if not changes.is_dir():
        return []
    folders = [p for p in changes.iterdir() if p.is_dir() and p.name != ARCHIVE and (p / "spec.md").is_file()]
    archive = changes / ARCHIVE
    if archive.is_dir():
        folders.extend(p for p in archive.iterdir() if p.is_dir() and (p / "spec.md").is_file())
    return sorted(folders)


def _spec_class_and_date(spec: Path) -> tuple[str, date | None]:
    """The `class:` and `date:` of a spec header; class "" when absent."""
    text = spec.read_text(encoding="utf-8")
    block = _BLOCK.match(text)
    if not block:
        return "", None
    header = block.group(1)
    class_match = _CLASS_LINE.search(header)
    klass = class_match.group(1) or class_match.group(2) or class_match.group(3) if class_match else ""
    date_match = _DATE_LINE.search(header)
    spec_date = None
    if date_match:
        # quoted dates and trailing comments are valid YAML metadata — strip
        # them before reading (phase-6 row F-10); a date that still does not
        # parse leaves spec_date None, and the change is then measured rather
        # than silently exempted
        raw = date_match.group(1).split("#", 1)[0].strip().strip("\"'")
        try:
            spec_date = date.fromisoformat(raw)
        except ValueError:
            spec_date = None
    return klass, spec_date


def _parse_records(text: str) -> tuple[list[tuple[str, dict[str, str]]], list[dict[str, str]]]:
    """Interview records as (id, fields) in document order, and skip records."""
    records: list[tuple[str, dict[str, str]]] = []
    skips: list[dict[str, str]] = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        heading = block.split("\n", 1)[0]
        body = block[len(heading) :]
        fields: dict[str, str] = {}
        for line in body.splitlines():
            match = _FIELD_LINE.match(line)
            if match:
                fields[match.group("name")] = match.group("value").strip()
        record = _RECORD.match(heading)
        if record:
            records.append((record.group(1), fields))
        elif _SKIP_HEADING.match(heading):
            skips.append(fields)
    return records, skips


def _counted(records: list[tuple[str, dict[str, str]]]) -> int:
    """Distinct maintainer answers: first counted occurrence of an id wins
    (Q-5; loop row L1-1). A block without a stated question and answer is not
    an interview record, whatever its other fields claim (phase-6 row F-12)."""
    seen: set[str] = set()
    for record_id, fields in records:
        if fields.get("status") != "answered":
            continue
        if fields.get("answered_by") != "maintainer":
            continue
        if not fields.get("asked", "").strip() or not fields.get("answer", "").strip():
            continue
        if record_id in seen:
            continue
        seen.add(record_id)
    return len(seen)


def _has_reasoned_skip(skips: list[dict[str, str]]) -> bool:
    return any(s.get("status") == "skipped" and s.get("reason", "").strip() for s in skips)


# ---------------------------------------------------------------------------
# the measurement
# ---------------------------------------------------------------------------


def measure(root: Path, only: str | None = None) -> tuple[list[str], int]:
    """Findings and the number of changes measured; raises CannotMeasure."""
    changed = _changed_paths(root)
    adr_paths = {p for p in changed if p.startswith(ADR_DIR + "/")}
    owning: set[str] = set()
    for path in changed:
        if not path.startswith(CHANGES_DIR + "/"):
            continue
        parts = path.split("/")
        # plans/changes/<name>/<file>: the owning folder sits at parts[2]. A
        # folder whose diff touches plan.md alone is a ledger migration, not
        # the home of the ADR's answers (criterion-test-ledger, 2026-10-11).
        if len(parts) > 3 and parts[2] != ARCHIVE and parts[3] != "plan.md":
            owning.add(parts[2])

    if adr_paths and len(owning) != 1:
        whom = ", ".join(sorted(owning)) or "none"
        return (
            [
                f"{len(adr_paths)} ADR path(s) changed under {ADR_DIR}/ but the diff "
                f"owns {len(owning)} change folder(s): {whom} — an ADR change runs "
                "inside exactly one change folder under plans/changes/, whose "
                "decisions.md carries the five answers"
            ],
            0,
        )

    adr_touched = bool(adr_paths)
    owner = next(iter(owning)) if adr_touched else None

    findings: list[str] = []
    measured = 0
    named_found = False
    named_measured = False

    # The ADR duty attaches to the work, not to the folder's age or class
    # (G-2, G-5; loop row L1-3): the owner owes five counted records whatever
    # its class and whatever its spec date — the cut-off exempts a folder's
    # own class minimums, never a new ADR edit.
    if adr_touched:
        measured += 1
        if only and owner == only:
            named_found = True
            named_measured = True
        decisions = root / CHANGES_DIR / owner / "decisions.md"
        text = decisions.read_text(encoding="utf-8") if decisions.is_file() else ""
        counted = _counted(_parse_records(text)[0])
        if counted < 5:
            findings.append(
                f"{owner} (ADR change): {counted} of 5 counted interview "
                "record(s) in decisions.md — five are owed whatever the class"
            )

    for folder in _active_changes(root):
        name = folder.name
        if folder.parent.name == ARCHIVE:
            name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)
        if only and name != only:
            continue
        named_found = True
        if adr_touched and name == owner:
            continue  # already measured above
        klass, spec_date = _spec_class_and_date(folder / "spec.md")
        if klass not in CLASSES:
            continue
        if spec_date is not None and spec_date <= CUTOFF:
            continue  # Q-4/Q-8: the stock stays exempt — a change whose date
            # cannot be read is measured, never silently exempted (F-10)
        measured += 1
        if only:
            named_measured = True
        decisions = folder / "decisions.md"
        text = decisions.read_text(encoding="utf-8") if decisions.is_file() else ""
        records, skips = _parse_records(text)
        counted = _counted(records)
        skip_ok = _has_reasoned_skip(skips)

        required = MINIMUMS[klass]
        if klass == "bounded":
            if counted < 1 and not skip_ok:  # Q-6
                findings.append(
                    f"{name} (bounded): neither an interview record answered by the "
                    "maintainer nor a reasoned skip stands in decisions.md"
                )
            continue
        if klass == "spike":
            if counted < required and not skip_ok:  # Q-3
                findings.append(
                    f"{name} (spike): {counted} of {required} counted interview "
                    "record(s) and no reasoned skip in decisions.md"
                )
            continue
        if required and counted < required:
            findings.append(f"{name} ({klass}): {counted} of {required} counted interview record(s) in decisions.md")

    if only:
        # Loop row L1-6 and phase-6 row F-17: the spec gate's verdict belongs
        # to the named change alone — a passing unrelated measurement does
        # not answer for it, and a folder that exists but is exempt by the
        # cut-off is named, not silent.
        if not named_found:
            findings.append(f"--change {only}: no change folder under {CHANGES_DIR}/ — nothing was measured")
        elif not named_measured:
            print(
                f"interview-minimums: {only} is exempt by the cut-off "
                f"({CUTOFF.isoformat()}) — the class minimums do not hold for it."
            )
    return findings, measured


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="another tree (tests)")
    parser.add_argument("--change", type=str, default=None, help="measure one change only (the spec gate)")
    args = parser.parse_args()
    try:
        findings, measured = measure(args.root, args.change)
    except CannotMeasure as cannot:
        print(f"interview-minimums NOT MEASURED: {cannot} — exit 3, nothing measured.")
        return 3
    if findings:
        print(f"{len(findings)} finding(s):")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(
        f"interview-minimums ok: {measured} change(s) measured"
        + (f", {args.change} green" if args.change else "")
        + f"; cut-off {CUTOFF.isoformat()}, stock exempt."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
