"""Shared locked access to the stand-in test logs (change flaky-swarm-leak-test).

The stage-2 suites' stand-in processes append JSON records larger than one
atomic write to the same log file while other processes and the pytest
observers read it. Without a common lock a reader can see a torn last line and
its `json.loads` raises; under the swarm runner such an exception inside a
gate is converted fail-closed into a security refusal. This is an inferred
explanation for the main-CI fixture failures; their diagnostics were not read
and the natural failure was not reproduced locally (bead coding-harness-yb1l).
Every append and every
snapshot read takes an advisory `fcntl.flock` on the data file itself, so
writers and readers meet on the file's own identity across threads and
processes, however a caller spells its path.

This module is the one place a stand-in log is declared: `STAND_IN_LOGS`
names every log file, the JSON functions refuse any other name, and
`text_append` refuses these declared names so JSON logs must use
`append_record`. In the pytest process any read or append of a declared log
that does not go through these functions fails its test at run time
(`tests/stand_in_log_guard.py`, wired by `tests/conftest.py`); the static
guard in `tests/test_atomic_test_log.py` is a cheap advisory that also reads
the stand-in sources.

Standard library only: the stand-in templates embed this module's source
verbatim at their `@ATOMIC_LOG@` render marker, because the sandboxed children
get no import path. Host-side test code imports this module directly. A
missing data file - or a missing directory - reads as an empty snapshot
(only `FileNotFoundError`). Other I/O errors, including `NotADirectoryError`
when a parent component is a regular file, propagate. A malformed stored
line raises; a lock not obtained within `LOCK_TIMEOUT` seconds raises
`TimeoutError` instead of hanging. Nothing is retried or
suppressed, and no durability beyond a flushed buffered write is promised.

The per-key call counter (change standin-call-counter, bead
coding-harness-bxxt.14): `append_counted` appends a record and returns how
many earlier records of the log carry its key, without parsing the log when
the small counter beside it (`<log>.counts.json`) is current. The counter is
tagged with the log's device, inode, byte size and modification time after its
last update. `append_counted` reads and rebuilds it under the log's exclusive
lock; `read_counter` is an unlocked test observer. It is published whole by a
temporary file and `os.replace`, so a writer still holding a removed log's
inode can neither expose a partial counter nor make the new log's count stale:
its tag no longer matches, and the next call rebuilds from the current log. A
counter read error means rebuild; a counter write or replacement error
propagates. The counters are declared beside the logs (`STAND_IN_COUNTERS`).
"""

import fcntl
import json
import os
import tempfile
import threading
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

# The per-key counter beside a declared log, and every declared counter name.
COUNTER_SUFFIX = ".counts.json"
STAND_IN_COUNTERS = tuple(name + COUNTER_SUFFIX for name in STAND_IN_LOGS)

# Every file the runtime guard watches: the logs and their counters.
STAND_IN_FILES = STAND_IN_LOGS + STAND_IN_COUNTERS

# Seconds a reader or writer waits for the lock before it fails loudly.
LOCK_TIMEOUT = 60.0
_builder_state = threading.local()


def _lock(handle, operation: int, timeout: float | None) -> None:
    """Take the advisory lock on this open file, or raise `TimeoutError` at the deadline."""
    status = os.fstat(handle.fileno())
    if (status.st_dev, status.st_ino) in getattr(_builder_state, "locked", set()):
        raise RuntimeError("a counted record builder cannot re-enter the same log")
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
    if path.name in STAND_IN_COUNTERS:
        raise ValueError(f"{path.name} is a declared stand-in counter; use append_counted")
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


def counter_path(data_path: str | Path) -> Path:
    """The counter file beside a declared log."""
    path = _declared(data_path)
    return path.with_name(path.name + COUNTER_SUFFIX)


def append_counted(data_path: str | Path, key: str, build, timeout: float | None = None) -> int:
    """Append the record `build(index)` returns and return `index`, the earlier records carrying `key`.

    The builder runs under the exclusive lock and must not re-enter the same
    log through a locked helper; doing so raises RuntimeError immediately.
    Everything happens under the log inode's exclusive lock: the count comes
    from the counter when its tag equals this inode's device, inode, size and mtime,
    else it is rebuilt from this log's records; the record, whose `key` must
    equal `key`, is appended; the counter is published with the new size.
    """
    if not isinstance(key, str):
        raise TypeError("the counted key must be a string")
    path = _declared(data_path)
    counter = path.with_name(path.name + COUNTER_SUFFIX)
    with path.open("a+b") as handle:
        _lock(handle, fcntl.LOCK_EX, timeout)
        try:
            status = os.fstat(handle.fileno())
            tag = [status.st_dev, status.st_ino, status.st_size, status.st_mtime_ns]
            try:
                stored = _load_counter(counter)
            except (OSError, ValueError, RecursionError):
                stored = None  # missing, unreadable or truncated: rebuilt below
            counts = _current_counts(stored, tag)
            if counts is None:
                counts = _rebuild_counts(handle)
            index = counts.get(key, 0)
            identity = (status.st_dev, status.st_ino)
            locked = getattr(_builder_state, "locked", set())
            _builder_state.locked = locked
            locked.add(identity)
            try:
                record = build(index)
            finally:
                locked.remove(identity)
            if not isinstance(record, dict) or record.get("key") != key:
                raise ValueError(f"the counted record must carry the key {key!r}")
            handle.seek(0, os.SEEK_END)
            handle.write((json.dumps(record) + "\n").encode("utf-8"))
            handle.flush()
            counts[key] = index + 1
            status = os.fstat(handle.fileno())
            _publish_counter(
                counter,
                {
                    "device": status.st_dev,
                    "inode": status.st_ino,
                    "size": status.st_size,
                    "mtime_ns": status.st_mtime_ns,
                    "counts": counts,
                },
            )
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)
    return index


def read_counter(data_path: str | Path):
    """Observe the published counter unlocked; missing means None, other read errors propagate."""
    try:
        return _load_counter(counter_path(data_path))
    except FileNotFoundError:
        return None


def _load_counter(counter: Path):
    with counter.open(encoding="utf-8") as handle:
        return json.loads(handle.read())


def _current_counts(stored, tag: list) -> dict | None:
    """The stored per-key counts when the counter has the known shape and this tag, else None."""
    if not isinstance(stored, dict) or set(stored) != {"device", "inode", "size", "mtime_ns", "counts"}:
        return None
    numbers = [stored["device"], stored["inode"], stored["size"], stored["mtime_ns"]]
    if any(type(number) is not int for number in numbers) or numbers != tag:
        return None
    counts = stored["counts"]
    if not isinstance(counts, dict) or any(type(value) is not int or value < 0 for value in counts.values()):
        return None
    return dict(counts)


def _rebuild_counts(handle) -> dict:
    """Per-key counts of the records of the locked log handle; a malformed line raises."""
    handle.seek(0)
    counts: dict = {}
    for line in handle.read().decode("utf-8").splitlines():
        key = json.loads(line).get("key")
        if isinstance(key, str):
            counts[key] = counts.get(key, 0) + 1
    return counts


def _publish_counter(counter: Path, data: dict) -> None:
    """Write the counter whole to a temporary file and replace it; any failure propagates."""
    descriptor, temporary = tempfile.mkstemp(prefix=counter.name + ".", suffix=".tmp", dir=counter.parent)
    staged = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as out:
            out.write(json.dumps(data))
        staged.replace(counter)
    except BaseException:
        staged.unlink(missing_ok=True)
        raise


def embedded_source() -> str:
    """This module's own source, for the stand-ins' `@ATOMIC_LOG@` render marker."""
    return Path(__file__).read_text(encoding="utf-8")
