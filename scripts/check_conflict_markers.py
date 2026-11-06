#!/usr/bin/env python3
"""check_conflict_markers.py — tracked text carries no merge-conflict marker, and Git's own check passes.

A merge followed by a commit and push of unresolved markers left a clean Git
status over conflicted text (bead coding-harness-i76l). This gate measures the
committed and working text itself:

- every tracked regular file without a NUL byte is read as bytes; a line that
  begins in column one with ``<<<<<<<``, ``=======`` or ``>>>>>>>`` (any
  suffix, none, or more marker characters) is a finding with its path and
  one-based line number, wherever it stands — a fenced example is no
  exemption;
- ``git diff --check`` and ``git diff --cached --check`` run over the unstaged
  and the staged changes and their diagnostics are findings;
- a path in ``FIXTURE_EXCEPTIONS`` (an exact repository-relative path, never a
  directory or a wildcard) is skipped by both measurements. The list starts
  empty.

Inspection that cannot complete — a root that is not a Git work tree, a failed
Git command, a tracked regular file that cannot be read — is a finding too:
what was not measured is never reported as clean. Symlinks, submodule entries
and paths absent from the working tree are not scanned. The gate writes
nothing: no file, no index entry, no ref.

Usage:
    python3 scripts/check_conflict_markers.py [--root DIR]

Exit:
    0 = measured, nothing found
    2 = findings, or something could not be measured (BLOCK)
"""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _verdict import Verdict  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

# The marker prefixes, as bytes: a file that is not valid UTF-8 is still text.
MARKER_PREFIXES: tuple[bytes, ...] = (b"<" * 7, b"=" * 7, b">" * 7)

# Exact repository-relative paths (forward slashes) that may carry marker lines
# or whitespace faults on purpose. Reviewed one by one; empty on purpose.
FIXTURE_EXCEPTIONS: frozenset[str] = frozenset()

REGULAR_MODES = frozenset({"100644", "100755"})


@dataclass
class Result:
    """What one run measured and found."""

    scanned: int = 0
    markers: dict[str, list[tuple[int, str]]] = field(default_factory=dict)
    diff_findings: list[tuple[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not (self.markers or self.diff_findings or self.errors)


def _git(root: Path, *args: str) -> tuple[int, bytes, str]:
    """Run git at root with an argument array; (returncode, stdout, stderr). 127 when git is missing."""
    try:
        done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    except OSError as exc:
        return 127, b"", f"cannot run git ({exc.strerror or exc})"
    return done.returncode, done.stdout, done.stderr.decode("utf-8", "replace").strip()


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _tracked_regular_paths(root: Path, result: Result) -> list[str] | None:
    """Tracked paths of regular-file mode, deduplicated; None when the index cannot be listed."""
    code, out, err = _git(root, "rev-parse", "--show-toplevel")
    if code != 0:
        result.errors.append(f"{root} is not inside a Git work tree — nothing was measured ({err or 'git failed'})")
        return None
    try:
        top = Path(os.fsdecode(out).strip()).resolve()
    except OSError as exc:
        result.errors.append(f"the work tree of {root} cannot be resolved ({exc.strerror or exc})")
        return None
    if top != root.resolve():
        result.errors.append(f"{root} is not the top of a Git work tree ({top}) — nothing was measured")
        return None
    code, out, err = _git(root, "ls-files", "-z", "--stage")
    if code != 0:
        result.errors.append(f"git ls-files failed — the tracked files were not listed ({err or f'exit {code}'})")
        return None
    paths: dict[str, None] = {}
    for entry in out.split(b"\0"):
        if not entry:
            continue
        meta, _, raw = entry.partition(b"\t")
        mode = meta.split(b" ")[0].decode("ascii", "replace")
        if mode in REGULAR_MODES:
            paths[os.fsdecode(raw)] = None
    return list(paths)


def _scan_file(root: Path, rel: str, result: Result) -> None:
    path = root / rel
    try:
        info = path.lstat()
    except FileNotFoundError:
        return  # deleted in the working tree: no text to scan
    except OSError as exc:
        result.errors.append(f"{rel} cannot be examined ({exc.strerror or exc}) — its text was not measured")
        return
    if not stat.S_ISREG(info.st_mode):
        return  # a symlink or other entry in its place: never followed
    try:
        inside = path.parent.resolve().is_relative_to(root.resolve())
    except OSError as exc:
        result.errors.append(f"{rel} cannot be examined ({exc.strerror or exc}) — its text was not measured")
        return
    if not inside:
        return  # a parent symlink that leaves the root: never followed
    try:
        data = _read_bytes(path)
    except OSError as exc:
        result.errors.append(f"{rel} cannot be read ({exc.strerror or exc}) — its text was not measured")
        return
    if b"\0" in data:
        return  # binary
    result.scanned += 1
    for number, line in enumerate(data.split(b"\n"), start=1):
        for prefix in MARKER_PREFIXES:
            if line.startswith(prefix):
                result.markers.setdefault(rel, []).append((number, prefix.decode("ascii")))
                break


def _diff_check(root: Path, fixtures: frozenset[str], result: Result) -> None:
    excludes = [f":(exclude,literal){name}" for name in sorted(fixtures)]
    for label, extra in (("unstaged", []), ("staged", ["--cached"])):
        args = ["diff", "--check", "--no-ext-diff", "--no-textconv", *extra, "--", ".", *excludes]
        code, out, err = _git(root, *args)
        text = out.decode("utf-8", "replace").strip()
        if code == 0:
            continue
        if code < 100 and code & 2 and text:
            result.diff_findings.append((label, text))
        else:
            why = err or text or f"exit {code}"
            result.errors.append(f"git diff --check ({label}) failed — not measured ({why})")


def measure(root: Path, fixtures: frozenset[str] | None = None) -> Result:
    """Measure root; never writes. Findings and unmeasured parts both land in the result."""
    fixtures = FIXTURE_EXCEPTIONS if fixtures is None else fixtures
    result = Result()
    paths = _tracked_regular_paths(root, result)
    if paths is None:
        return result
    for rel in paths:
        if rel in fixtures:
            continue
        _scan_file(root, rel, result)
    _diff_check(root, fixtures, result)
    return result


def run(root: Path) -> int:
    result = measure(root)
    verdict = Verdict()
    for rel in sorted(result.markers):
        spots = ", ".join(f"line {number}" for number, _ in result.markers[rel])
        remedy = "remove the marker line, or resolve the conflict it marks"
        verdict.block(f"{rel}: conflict marker at {spots}", remedy)
    for label, text in result.diff_findings:
        verdict.block(f"git diff --check found a fault in {label} changes", text)
    for error in result.errors:
        verdict.block(f"not measured: {error}")
    code = verdict.exit_code()
    if code:
        print(verdict.render())
        for rel in sorted(result.markers):
            for number, prefix in result.markers[rel]:
                print(f"{rel}:{number}: marker line {prefix}")
        summary = f"conflict-markers: {len(result.markers)} files with markers, {len(result.errors)} not measured"
        print(summary, file=sys.stderr)
        return code
    print(f"conflict-markers: scanned {result.scanned} tracked text files; no marker line, git diff --check clean")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument(
        "--root", default=REPO_ROOT, type=Path, help="repository root to measure (default: this repository)"
    )
    args = parser.parse_args(argv)
    return run(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
