"""Shared locked access to the stand-in test logs (change flaky-swarm-leak-test).

The stage-2 suites' stand-in processes append JSON records larger than one
atomic write to the same log file while other processes and the pytest
observers read it. Without a common lock a reader can see a torn last line and
its `json.loads` raises; under the swarm runner such an exception inside a
gate is converted fail-closed into a security refusal, which turned a green
fixture red on main CI (bead coding-harness-yb1l). Every append and every
snapshot read of these logs takes an advisory `fcntl.flock` on one stable
sidecar beside the destination, so writers and readers meet on one lock
identity across threads and processes.

Standard library only: the stand-in templates embed this module's source
verbatim at their `@ATOMIC_LOG@` render marker, because the sandboxed children
get no import path. Host-side test code imports this module directly. A
missing data file reads as an empty snapshot; a malformed stored line raises;
nothing is retried or suppressed, and no durability beyond a flushed buffered
write is promised.
"""

import fcntl
import hashlib
import json
from pathlib import Path

MARKER = "@ATOMIC_LOG@"


def lock_path(data_path: str | Path, lock_dir: str | Path | None = None) -> Path:
    """The stable sidecar whose advisory lock serialises access to this destination.

    By default it sits beside the destination. A caller that appends to a
    repository document passes `lock_dir`, so no sidecar appears in the tree;
    the sidecar is then named after the destination's resolved path. The suffix
    is not `.lock`, which other suites count as a runner lock.
    """
    path = Path(data_path)
    if lock_dir is None:
        return path.with_name(path.name + ".guard")
    digest = hashlib.sha1(str(path.resolve()).encode("utf-8")).hexdigest()[:16]
    return Path(lock_dir) / (digest + ".guard")


class HoldLock:
    """The sidecar's advisory lock, held for the whole `with` block.

    `flock` excludes by open file description, so independent opens - in
    threads as in processes - wait for each other; the data file's inode is
    never locked, because a test may replace the file between appends.
    """

    def __init__(self, data_path: str | Path, shared: bool = False, lock_dir: str | Path | None = None) -> None:
        self._handle = lock_path(data_path, lock_dir).open("a")
        self._shared = shared

    def __enter__(self):
        fcntl.flock(self._handle, fcntl.LOCK_SH if self._shared else fcntl.LOCK_EX)
        return self._handle

    def __exit__(self, *_exc_info: object) -> bool:
        fcntl.flock(self._handle, fcntl.LOCK_UN)
        self._handle.close()
        return False


def text_append(data_path: str | Path, text: str, lock_dir: str | Path | None = None) -> None:
    """Append exactly this text under the exclusive lock; no newline is added."""
    with HoldLock(data_path, lock_dir=lock_dir), Path(data_path).open("a", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()


def append_record(data_path: str | Path, record) -> None:
    """Append one JSON record as one line under the exclusive lock."""
    text_append(data_path, json.dumps(record) + "\n")


def read_records(data_path: str | Path) -> list:
    """A snapshot of complete records: an in-progress append waits, a missing file is empty.

    The shared lock is held through read and parse, so no reader observes a
    fragment. A malformed stored line raises; nothing is skipped or retried.
    """
    with HoldLock(data_path, shared=True):
        data = Path(data_path)
        if not data.exists():
            return []
        return [json.loads(line) for line in data.read_text(encoding="utf-8").splitlines()]


def embedded_source() -> str:
    """This module's own source, for the stand-ins' `@ATOMIC_LOG@` render marker."""
    return Path(__file__).read_text(encoding="utf-8")
