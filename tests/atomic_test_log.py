"""Shared locked access to the stand-in test logs (change flaky-swarm-leak-test).

The stage-2 suites' stand-in processes append JSON records larger than one
atomic write to the same log file while other processes and the pytest
observers read it. Without a common lock a reader can see a torn last line and
its `json.loads` raises; under the swarm runner such an exception inside a
gate is converted fail-closed into a security refusal, which turned a green
fixture red on main CI (bead coding-harness-yb1l). Every append and every
snapshot read takes an advisory `fcntl.flock` on the data file itself, so
writers and readers meet on the file's own identity across threads and
processes, however a caller spells its path.

This module is the one place a stand-in log is declared: `STAND_IN_LOGS`
names every log file, the JSON functions refuse any other name, and
`text_append` refuses these declared names so JSON logs must use
`append_record`. The guard in `tests/test_atomic_test_log.py` fails on any
read or append of a declared log that does not go through these functions.

Standard library only: the stand-in templates embed this module's source
verbatim at their `@ATOMIC_LOG@` render marker, because the sandboxed children
get no import path. Host-side test code imports this module directly. A
missing data file - or a missing directory - reads as an empty snapshot
(only `FileNotFoundError`). Other I/O errors, including `NotADirectoryError`
when a parent component is a regular file, propagate. A malformed stored
line raises; a lock not obtained within `LOCK_TIMEOUT` seconds raises
`TimeoutError` instead of hanging. Nothing is retried or
suppressed, and no durability beyond a flushed buffered write is promised.
"""

import fcntl
import json
import time
from pathlib import Path

MARKER = "@ATOMIC_LOG@"

# The declared stand-in logs: the file names every suite's stand-ins append
# JSON records to and its observers read.
STAND_IN_LOGS = (
    "calls.jsonl",
    "versions.jsonl",
    "infrastructure.jsonl",
    "local-pi.jsonl",
    "path-pi.jsonl",
    "npm-calls.jsonl",
)

# Seconds a reader or writer waits for the lock before it fails loudly.
LOCK_TIMEOUT = 60.0


def _lock(handle, operation: int, timeout: float | None) -> None:
    """Take the advisory lock on this open file, or raise `TimeoutError` at the deadline."""
    timeout = LOCK_TIMEOUT if timeout is None else timeout
    deadline = time.monotonic() + timeout
    while True:
        try:
            fcntl.flock(handle, operation | fcntl.LOCK_NB)
            return
        except BlockingIOError:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"no lock on {handle.name} within {timeout} s") from None
            time.sleep(0.005)


def _declared(data_path: str | Path) -> Path:
    path = Path(data_path)
    if path.name not in STAND_IN_LOGS:
        raise ValueError(f"{path.name} is not a declared stand-in log (atomic_test_log.STAND_IN_LOGS)")
    return path


def text_append(data_path: str | Path, text: str, timeout: float | None = None) -> None:
    """Append exactly this text under the exclusive lock; no newline is added.

    Serves scenario text appends to fixture documents and receipts, which
    are not declared logs. Declared stand-in logs require `append_record`.
    """
    path = Path(data_path)
    if path.name in STAND_IN_LOGS:
        raise ValueError(f"{path.name} is a declared stand-in log; use append_record")
    _append_text(path, text, timeout)


def _append_text(data_path: Path, text: str, timeout: float | None) -> None:
    """Shared locked write after the public API has checked the destination."""
    with data_path.open("a", encoding="utf-8") as handle:
        _lock(handle, fcntl.LOCK_EX, timeout)
        try:
            handle.write(text)
            handle.flush()
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def append_record(data_path: str | Path, record, timeout: float | None = None) -> None:
    """Append one JSON record as one line of a declared log under the exclusive lock."""
    _append_text(_declared(data_path), json.dumps(record) + "\n", timeout)


def read_records(data_path: str | Path, timeout: float | None = None) -> list:
    """A snapshot of complete records of a declared log: an in-progress append waits, a missing file is empty.

    The shared lock is held through the read, so no reader observes a
    fragment. Only `FileNotFoundError` (a missing file or directory) means
    empty; other I/O errors propagate, including `NotADirectoryError` for a
    regular-file parent. A malformed stored line raises; nothing is skipped
    or retried.
    """
    try:
        handle = _declared(data_path).open(encoding="utf-8")
    except FileNotFoundError:
        return []
    with handle:
        _lock(handle, fcntl.LOCK_SH, timeout)
        try:
            text = handle.read()
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)
    return [json.loads(line) for line in text.splitlines()]


def embedded_source() -> str:
    """This module's own source, for the stand-ins' `@ATOMIC_LOG@` render marker."""
    return Path(__file__).read_text(encoding="utf-8")
