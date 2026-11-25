#!/usr/bin/env python3
"""job_containment.py - the one place that finds and ends the processes of a detached job (bead coding-harness-a6ns.1).

`scripts/jobs.py stop` calls only `end`; nothing else in the launcher finds or signals a job's processes.

The members of a job are:

1. the started command's process tree (by parent pid), from a verified command identity;
2. every process whose environment carries the job token (`HARNESS_JOB_TOKEN=<id>`), also after reparenting;
3. every process of a recorded process group, or of the session such a group leads, that started no earlier
   than the recorded leader - unless the leader's pid now belongs to another process (a reused pid);

Never a member: this process and its ancestors, the job's wrapper and its ancestors (the tmux server among
them), and every other job's wrapper and members by rules 1-3. Working directories and open files do not
establish membership.

`end` sends SIGTERM, waits the grace period, sends SIGKILL to every member still alive (scanning again, so a
member that appeared meanwhile is included), then scans once more and returns every survivor (pid, start
time, command); the caller writes them into the job record, never silently.

The backend is a seam: `PsBackend` reads `ps`. A Linux cgroup backend can follow
(follow-up bead); `scripts/stage2.py` `kill_live` and the verify supervisor adopt this module there.
"""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

STOP_GRACE = 5.0  # seconds between SIGTERM and SIGKILL
KILL_WAIT = 2.0  # seconds a stop waits for killed members to vanish before it names survivors
POLL = 0.1
TOKEN_ENV = "HARNESS_JOB_TOKEN"


@dataclass(frozen=True)
class Proc:
    """One visible process; `start` is its `ps` start time, with the pid its identity."""

    pid: int
    ppid: int
    pgid: int
    uid: int
    tty: str
    stat: str
    start: str
    command: str


def _norm(text: str) -> str:
    return " ".join(text.split())


def _run(args: list[str], *, any_status: bool = False, timeout: float = 10.0) -> str | None:
    """Standard output of a read-only helper, run from `/` so it never lies inside a job's directory."""
    env = {**os.environ, "LC_ALL": "C"}
    try:
        done = subprocess.run(
            args,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            env=env,
            cwd="/",
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if (any_status or done.returncode == 0) else None


def process_start(pid: int | None) -> str | None:
    """The start time `ps` reports for `pid` - with the pid, the identity of a process - or None when it is gone."""
    if pid is None or pid <= 0:
        return None
    text = _norm(_run(["ps", "-o", "lstart=", "-p", str(pid)]) or "")
    return text or None


def start_epoch(text: str | None) -> float | None:
    """A `ps` start time as epoch seconds (local time, one-second resolution), or None."""
    if not text:
        return None
    try:
        return time.mktime(time.strptime(text, "%a %b %d %H:%M:%S %Y"))
    except (ValueError, OverflowError):
        return None


class PsBackend:
    """Finds processes through `ps`; signals through `os.kill`."""

    def processes(self) -> list[Proc]:
        rows = []
        text = _run(["ps", "-axo", "pid=,ppid=,pgid=,uid=,tty=,stat=,lstart=,command="]) or ""
        for line in text.splitlines():
            parts = line.split(None, 11)
            if len(parts) < 11 or not all(part.isdigit() for part in parts[:4]):
                continue
            rows.append(
                Proc(
                    pid=int(parts[0]),
                    ppid=int(parts[1]),
                    pgid=int(parts[2]),
                    uid=int(parts[3]),
                    tty=parts[4],
                    stat=parts[5],
                    start=_norm(" ".join(parts[6:11])),
                    command=parts[11] if len(parts) > 11 else "",
                )
            )
        return rows

    def session(self, pid: int) -> int | None:
        try:
            return os.getsid(pid)
        except OSError:
            return None

    def token_holders(self, token: str) -> set[int]:
        found = set()
        for line in (_run(["ps", "eww", "-axo", "pid=,command="]) or "").splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) == 2 and parts[0].isdigit() and token in parts[1].split():
                found.add(int(parts[0]))
        return found

    def alive(self, pid: int, start: str) -> bool:
        """True when `pid` runs (not a zombie) and began at `start`; a reused pid counts as gone."""
        text = _run(["ps", "-o", "stat=,lstart=", "-p", str(pid)]) or ""
        parts = text.split(None, 1)
        return len(parts) == 2 and not parts[0].startswith("Z") and _norm(parts[1]) == start

    def send(self, pid: int, signum: int) -> None:
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.kill(pid, signum)


BACKEND = PsBackend()


def _ancestors(pid: int, by_pid: dict[int, Proc]) -> set[int]:
    """`pid` and every ancestor of it."""
    chain = {pid}
    current = by_pid.get(pid)
    while current is not None and current.ppid not in chain and current.ppid > 0:
        chain.add(current.ppid)
        current = by_pid.get(current.ppid)
    return chain


def _core(record: dict, table: list[Proc], by_pid: dict[int, Proc], backend) -> dict[int, Proc]:
    """Rules 1-3: the command tree, the token holders and the recorded groups and sessions."""
    found: dict[int, Proc] = {}
    root = by_pid.get(record.get("command_pid") or -1)
    if root is not None and root.start == record.get("command_start"):
        children: dict[int, list[Proc]] = {}
        for proc in table:
            children.setdefault(proc.ppid, []).append(proc)
        found[root.pid] = root
        pending = [root.pid]
        while pending:
            for child in children.get(pending.pop(), []):
                if child.pid not in found:
                    found[child.pid] = child
                    pending.append(child.pid)
    for pid in backend.token_holders(f"{TOKEN_ENV}={record['id']}"):
        if pid in by_pid:
            found[pid] = by_pid[pid]
    for group in record.get("groups", []):
        leader = by_pid.get(group["pid"])
        if group["start"] is None or (leader is not None and leader.start != group["start"]):
            continue  # unknown identity, or the leader's pid now belongs to another process
        floor = start_epoch(group["start"])
        if floor is None:
            continue
        for proc in table:
            if proc.pgid == group["pgid"] or backend.session(proc.pid) == group["pgid"]:
                began = start_epoch(proc.start)
                if began is not None and began >= floor:
                    found[proc.pid] = proc
    return found


def members(record: dict, others: Iterable[dict] = (), backend=None) -> dict[int, Proc]:
    """pid -> process of every member of the job `record`, never the caller, a wrapper or another job."""
    backend = backend or BACKEND
    table = backend.processes()
    by_pid = {proc.pid: proc for proc in table}
    excluded = _ancestors(os.getpid(), by_pid)
    wrapper = record.get("wrapper_pid")
    if wrapper:
        excluded |= _ancestors(wrapper, by_pid)
    for other in others:
        if other.get("wrapper_pid"):
            excluded.add(other["wrapper_pid"])
        excluded |= set(_core(other, table, by_pid, backend))
    found = _core(record, table, by_pid, backend)
    return {pid: proc for pid, proc in found.items() if pid not in excluded}


def end(
    record: dict,
    others: Iterable[dict] = (),
    *,
    send: Callable[[int, int], None] | None = None,
    backend=None,
) -> list[dict]:
    """End every member of the job: SIGTERM, the grace, SIGKILL, a last scan; return the survivors.

    Each survivor is `{"pid", "start", "command"}`; an empty list means every member is gone.
    """
    backend = backend or BACKEND
    kill = send or backend.send
    others = list(others)

    def scan() -> dict[int, Proc]:
        return members(record, others, backend)

    def living(found: dict[int, Proc]) -> dict[int, Proc]:
        return {pid: proc for pid, proc in found.items() if backend.alive(pid, proc.start)}

    first = scan()
    for pid in living(first):
        kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + STOP_GRACE
    while time.monotonic() < deadline and living(first):
        time.sleep(POLL)
    killed: dict[int, Proc] = {}
    deadline = time.monotonic() + KILL_WAIT
    while True:
        left = living({**first, **killed, **scan()})
        for pid, proc in left.items():
            if pid not in killed:
                kill(pid, signal.SIGKILL)
                killed[pid] = proc
        if not left or time.monotonic() >= deadline:
            break
        time.sleep(POLL)
    survivors = living({**killed, **scan()})
    return [
        {"pid": proc.pid, "start": proc.start, "command": proc.command[:300]}
        for proc in sorted(survivors.values(), key=lambda proc: proc.pid)
    ]
