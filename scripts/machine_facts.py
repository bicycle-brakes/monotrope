#!/usr/bin/env python3
"""machine_facts.py - one dated, read-only machine-facts block for the night run (bead coding-harness-yql7).

    python3 scripts/machine_facts.py    # from the repository worktree the night run drives

One invocation collects one snapshot and prints it: free disk on the invoking
worktree's filesystem, host-wide swap, the repository's registered non-bare
worktrees, and the runner and verification invocations the existing run report
recognizes. The block is an observation to show in the main conversation
before lanes start and to record in the night plan's start state
(docs/orchestration.md) - not a gate: no threshold is compared and nothing is
refused, cleaned up, admitted, started or stopped (spec criteria 7 and 8).

What a source cannot provide, its field says `not read` with a short,
source-specific reason - never a zero, never raw command output - and the
independently readable fields remain; the invocation still exits zero (spec
criterion 6). The snapshot is fresh per invocation and writes nothing: no
file, no bytecode, no Git or tracker state, no network (spec criterion 7).

Running jobs are not a second definition of runner work: this script reuses
`run_report.run_command`, `run_report.parse_processes` and
`run_report.active_changes`, so machine facts and `make report` name the same
processes. Rows carry PID, elapsed time, verb and a known change or
`not read`; invocations are counted, never deduplicated into logical jobs.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the snapshot writes nothing - bytecode included (spec criterion 7)

import argparse  # noqa: E402
import contextlib  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from collections.abc import Callable  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from datetime import UTC, datetime  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_report  # noqa: E402

NOT_READ = run_report.NOT_READ
RunCommand = run_report.RunCommand
StatVfs = Callable[[str | os.PathLike[str]], os.statvfs_result]
KIB = 1024
MIB = 1024**2
GIB = 1024**3


@dataclass
class MachineSnapshot:
    """One invocation's readings: the UTC start stamp and the four fields, already rendered."""

    stamp: str
    disk: str
    swap: str
    worktrees: str
    jobs: list[str] = field(default_factory=list)


def _utc_now() -> datetime:
    return datetime.now(UTC)


def resolve_worktree(run: RunCommand, cwd: Path) -> Path | None:
    """The repository worktree that contains the invoking directory, or None.

    Read-only Git answers from the current working directory - never from this
    script's installation path, which may sit in a different checkout (spec
    criterion 1). Only a readable directory counts as the answer.
    """
    try:
        answer = run(["git", "-C", str(cwd), "rev-parse", "--show-toplevel"])
    except run_report.SourceError:
        return None
    candidate = Path(answer.removesuffix("\n"))
    if not candidate.is_dir():
        return None
    return candidate


# ---------------------------------------------------------------------------
# Free disk
# ---------------------------------------------------------------------------


def disk_field(statvfs: StatVfs, worktree: Path, *, worktree_identified: bool = True) -> str:
    """User-available GiB on the worktree filesystem, or an explicitly labelled cwd fallback."""
    try:
        status = statvfs(worktree)
    except OSError:
        return f"{NOT_READ} (statvfs: unavailable)"
    available = status.f_bavail * status.f_frsize
    scope = (
        "filesystem of the invoking worktree"
        if worktree_identified
        else "filesystem of the invoking directory; worktree not identified"
    )
    return f"{available / GIB:.1f} GiB available ({scope})"


# ---------------------------------------------------------------------------
# Swap
# ---------------------------------------------------------------------------


def _macos_mebibytes(text: str, key: str) -> float:
    """One `total`/`used` value of `sysctl -n vm.swapusage`, in MiB."""
    matched = re.search(rf"{key}\s*=\s*(\S+?)\s*M\b", text)
    if matched is None:
        raise run_report.SourceError(f"{NOT_READ} (vm.swapusage: no {key} value)")
    try:
        return float(matched.group(1))
    except ValueError:
        raise run_report.SourceError(f"{NOT_READ} (vm.swapusage: {key} is not a number)") from None


def macos_swap(run: RunCommand) -> str:
    """Host-wide used and total swap from `sysctl -n vm.swapusage`, normalized to GiB."""
    try:
        text = run(["sysctl", "-n", "vm.swapusage"])
        total = _macos_mebibytes(text, "total")
        used = _macos_mebibytes(text, "used")
    except run_report.SourceError as error:
        return str(error)
    if not (math.isfinite(total) and math.isfinite(used)) or total < 0 or used < 0 or used > total:
        return f"{NOT_READ} (vm.swapusage: inconsistent reading)"
    return f"{used * MIB / GIB:.1f} GiB used of {total * MIB / GIB:.1f} GiB total (host-wide)"


SWAP_INFO = re.compile(r"^(Swap(?:Total|Free)):\s+(\d+)\s+kB$", re.MULTILINE)


def linux_swap(proc_dir: Path) -> str:
    """Host-wide used and total swap from /proc/meminfo's SwapTotal/SwapFree, normalized to GiB.

    Used is the subtraction `SwapTotal - SwapFree`; a configured-but-empty
    swap (0 kB of 0 kB) is a readable zero, never a failure (spec criterion 3).
    """
    try:
        text = (proc_dir / "meminfo").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return f"{NOT_READ} (meminfo: SwapTotal/SwapFree unreadable)"
    fields = {name: int(value) for name, value in SWAP_INFO.findall(text)}
    total = fields.get("SwapTotal")
    free = fields.get("SwapFree")
    if total is None or free is None or free > total:
        return f"{NOT_READ} (meminfo: SwapTotal/SwapFree missing or inconsistent)"
    total_bytes = total * KIB
    used_bytes = (total - free) * KIB
    return f"{used_bytes / GIB:.1f} GiB used of {total_bytes / GIB:.1f} GiB total (host-wide)"


def swap_field(run: RunCommand, proc_dir: Path | None) -> str:
    """The platform's host-wide swap reading; a given proc directory selects the Linux source."""
    if proc_dir is None:
        return macos_swap(run)
    return linux_swap(proc_dir)


# ---------------------------------------------------------------------------
# Registered worktrees
# ---------------------------------------------------------------------------


def worktree_records(raw: str) -> list[list[str]]:
    """The records of one `git worktree list --porcelain -z` table.

    `-z` terminates every attribute with a NUL and separates records with
    an empty attribute. A path stays intact, including newlines and leading
    or trailing whitespace; `bare` is a separate attribute (spec criterion 4).
    """
    malformed = f"{NOT_READ} (git worktree list: malformed table)"
    if not raw.endswith("\0\0"):
        raise run_report.SourceError(malformed)
    records = [record.split("\0") for record in raw[:-2].split("\0\0")]
    for record in records:
        if (
            not record[0].startswith("worktree ")
            or not record[0][len("worktree ") :]
            or not any(attribute == "bare" or attribute.startswith("HEAD ") for attribute in record[1:])
            or any(not attribute or attribute.startswith("worktree ") for attribute in record[1:])
        ):
            raise run_report.SourceError(malformed)
    return records


def worktree_field(run: RunCommand, worktree: Path | None) -> str:
    """How many non-bare worktrees are registered with this repository - stale ones included, never pruned."""
    if worktree is None:
        return f"{NOT_READ} (worktree: not identified)"
    try:
        raw = run(["git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"])
        records = worktree_records(raw)
    except run_report.SourceError as error:
        return str(error)
    count = sum(1 for record in records if "bare" not in record)
    return f"{count} (git worktree list; non-bare entries, stale registrations included)"


# ---------------------------------------------------------------------------
# Running jobs
# ---------------------------------------------------------------------------


def jobs_field(run: RunCommand, worktree: Path | None) -> list[str]:
    """The runner and verification invocations of one `ps` snapshot, recognized by the run report.

    Rows carry PID, elapsed time, verb and a known change or `not read` -
    never raw command arguments - and invocations are counted, not
    deduplicated into logical jobs (spec criterion 5). When the shared runner
    definitions are unavailable, runner recognition says `not read` instead
    of claiming no runners; a failed process table says so without touching
    the other fields.
    """
    lines: list[str] = []
    if run_report.stage2 is None:
        lines.append(f"runner recognition: {NOT_READ} (runner verb definitions unavailable)")
    changes = frozenset()
    if worktree is not None:
        with contextlib.suppress(run_report.SourceError):
            # attribution stays `not read`; readable rows still render
            changes = frozenset(run_report.active_changes(worktree))
    try:
        raw = run(["ps", "-axo", "pid,etime,command"])
        table = raw.splitlines()
        # Validate source readability before the shared recognizer filters out
        # unrelated processes. A readable header-only table can mean no matches.
        if table and table[0].split() in (["PID", "ELAPSED", "COMMAND"], ["PID", "TIME", "COMMAND"]):
            table = table[1:]
        elif not table:
            raise run_report.SourceError(f"{NOT_READ} (ps: malformed table)")
        for line in table:
            parts = line.split(None, 2)
            if (
                len(parts) != 3
                or not parts[0].isdigit()
                or not run_report.ETIME.fullmatch(parts[1])
                or not parts[2].strip()
            ):
                raise run_report.SourceError(f"{NOT_READ} (ps: malformed table)")
        rows = run_report.parse_processes(raw, changes)
    except run_report.SourceError as error:
        lines.append(str(error))
        return lines
    if not rows:
        if run_report.stage2 is not None:
            lines.append("none matched")
        return lines
    lines.extend(f"pid {row.pid} · {row.label} · change {row.change} · elapsed {row.elapsed}" for row in rows)
    return lines


# ---------------------------------------------------------------------------
# The snapshot
# ---------------------------------------------------------------------------


def collect_snapshot(
    *,
    run: RunCommand = run_report.run_command,
    statvfs: StatVfs = os.statvfs,
    now: Callable[[], datetime] = _utc_now,
    proc_dir: Path | None = None,
    cwd: Path | None = None,
) -> MachineSnapshot:
    """One fresh snapshot: every field is collected independently, one failure never reaches the others."""
    if cwd is None:
        cwd = Path.cwd()
    stamp = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        worktree = resolve_worktree(run, cwd)
    except Exception:
        worktree = None  # Git-dependent facts are unavailable; the disk reader stays independent
    try:
        disk = disk_field(statvfs, worktree if worktree is not None else cwd, worktree_identified=worktree is not None)
    except Exception as error:
        disk = f"{NOT_READ} (statvfs: internal error: {type(error).__name__})"
    where = proc_dir if proc_dir is not None else (None if sys.platform == "darwin" else Path("/proc"))
    try:
        swap = swap_field(run, where)
    except Exception as error:
        swap = f"{NOT_READ} (swap: internal error: {type(error).__name__})"
    try:
        worktrees = worktree_field(run, worktree)
    except Exception as error:
        worktrees = f"{NOT_READ} (git: internal error: {type(error).__name__})"
    try:
        jobs = jobs_field(run, worktree)
    except Exception as error:
        jobs = [f"{NOT_READ} (ps: internal error: {type(error).__name__})"]
    return MachineSnapshot(stamp=stamp, disk=disk, swap=swap, worktrees=worktrees, jobs=jobs)


def render(snapshot: MachineSnapshot) -> str:
    """The block as text: one dated header, the four labelled fields, nothing else."""
    lines = [
        f"machine facts — {snapshot.stamp} (UTC snapshot · local, read-only · not a gate)",
        f"free disk: {snapshot.disk}",
        f"swap: {snapshot.swap}",
        f"registered worktrees: {snapshot.worktrees}",
        "running jobs:",
        *[f"  {line}" for line in snapshot.jobs],
    ]
    return "\n".join(lines)


def main(
    argv: list[str] | None = None,
    *,
    run: RunCommand = run_report.run_command,
    statvfs: StatVfs = os.statvfs,
    now: Callable[[], datetime] = _utc_now,
    proc_dir: Path | None = None,
    cwd: Path | None = None,
) -> int:
    """Print one machine-facts block and exit zero - a failed source is `not read`, never a failing run."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.parse_args(argv)  # no operational options: the block carries no policy (spec non-goals)
    try:
        snapshot = collect_snapshot(run=run, statvfs=statvfs, now=now, proc_dir=proc_dir, cwd=cwd)
    except Exception as error:  # the class name is the bounded diagnostic, as in run_report.main
        print(f"machine facts: not printed (internal error: {type(error).__name__})")
        return 0
    print(render(snapshot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
