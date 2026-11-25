"""The runtime check on declared stand-in logs (change flaky-swarm-leak-test, decisions.md#Q-5).

During the test session a declared stand-in log or its counter
(`atomic_test_log.STAND_IN_FILES`, identified by its file name as the helper's
`_declared` does) may be read or appended only through the helper's locked
functions, `append_record`, `read_records`, `append_counted` and the counter
reader `_load_counter` (change standin-call-counter). Only the innermost caller
outside this module and the standard library counts, so a record builder that
`append_counted` calls back is checked like any other code. Every other `open`, `io.open`, `os.open` or `pathlib.Path`
`open`, `read_text`, `read_bytes`, `write_text` or `write_bytes` of such a file
raises `RawStandInLogAccess` and is recorded; `tests/conftest.py` fails the
test that made a recorded access even when the code under test swallowed the
error or it happened in another thread. This is the choke point; the static
guard in `tests/test_atomic_test_log.py` stays as a cheap advisory.

Scope: the pytest process (each xdist worker) from conftest import on. The
stand-in child processes run outside it and stay under the static guard and
the embedded helper. Removal (`unlink`) and `exists` stay untouched: removing
the file is the suites' clear. An integer file descriptor carries no name and
passes. A test that must plant the unlocked fault itself carries the marker
`raw_stand_in_log_access(reason=...)`, which suspends the check for that test.
"""

from __future__ import annotations

import builtins
import io
import os
import pathlib
import sys
import threading
from pathlib import Path, PurePath

import atomic_test_log

# The helper functions whose own file access is the locked one.
_HELPER_FUNCTIONS = frozenset({"_append_text", "read_records", "append_counted", "_load_counter"})
_HELPER_FILE = os.path.realpath(atomic_test_log.__file__)
_THIS_FILE = os.path.realpath(__file__)
_STDLIB = str(Path(os.__file__).resolve().parent) + os.sep
_PATH_METHODS = ("open", "read_text", "read_bytes", "write_text", "write_bytes")

# The phase buffer may be drained; the session audit is append-only.
VIOLATIONS: list[str] = []
_session_violations: list[str] = []
_test_id = "<outside a test>"
_lock = threading.Lock()
_state = {"installed": False, "suspended": False}
_real: dict[str, object] = {}
_realpaths: dict[str, str] = {}


class RawStandInLogAccess(AssertionError):
    """A declared stand-in log was read, written or opened outside the shared helper."""


def _name(target) -> str | None:
    """The file name a path argument carries, or None for a descriptor or an unreadable value."""
    if isinstance(target, int):
        return None
    try:
        raw = os.fspath(target)
    except TypeError:
        return None
    if isinstance(raw, bytes):
        raw = os.fsdecode(raw)
    return PurePath(raw).name


def _real_file(code_file: str) -> str:
    known = _realpaths.get(code_file)
    if known is None:
        known = _realpaths[code_file] = os.path.realpath(code_file)
    return known


def _from_helper(frame) -> bool:
    """Whether the innermost caller outside this module and the standard library is a locked helper function."""
    while frame is not None:
        code = frame.f_code
        where = _real_file(code.co_filename)
        if where == _THIS_FILE or where.startswith(_STDLIB):
            frame = frame.f_back
            continue
        return code.co_name in _HELPER_FUNCTIONS and where == _HELPER_FILE
    return False


def _caller(frame) -> str:
    """The first frame outside this module and the standard library."""
    while frame is not None:
        where = _real_file(frame.f_code.co_filename)
        if where != _THIS_FILE and not where.startswith(_STDLIB):
            return f"{frame.f_code.co_filename}:{frame.f_lineno}"
        frame = frame.f_back
    return "unknown location"


def check(target, operation: str) -> None:
    """Refuse and record this access when it reaches a declared log from outside the helper."""
    if _state["suspended"]:
        return
    name = _name(target)
    if name not in atomic_test_log.STAND_IN_FILES:
        return
    frame = sys._getframe(2)
    if _from_helper(frame):
        return
    message = (
        f"raw {operation} of the declared stand-in log {os.fspath(target)!s} at {_caller(frame)}: "
        "read and append it only through atomic_test_log.read_records / append_record"
    )
    with _lock:
        VIOLATIONS.append(message)
        _session_violations.append(f"{_test_id}: {message}")
    raise RawStandInLogAccess(message)


def _wrap_open(real):
    def open(file, *args, **kwargs):  # noqa: A001 - stands in for the builtin
        check(file, "open")
        return real(file, *args, **kwargs)

    open.__wrapped__ = real
    open.__doc__ = real.__doc__
    return open


def _wrap_os_open(real):
    def os_open(path, *args, **kwargs):
        check(path, "os.open")
        return real(path, *args, **kwargs)

    os_open.__wrapped__ = real
    return os_open


def _wrap_method(name: str, real):
    def method(self, *args, **kwargs):
        check(self, name)
        return real(self, *args, **kwargs)

    method.__name__ = name
    method.__qualname__ = f"Path.{name}"
    method.__wrapped__ = real
    method.__doc__ = real.__doc__
    return method


def install() -> None:
    """Wrap the file entry points once for the rest of this process."""
    if _state["installed"]:
        return
    _real["builtins.open"] = builtins.open
    _real["io.open"] = io.open
    _real["os.open"] = os.open
    builtins.open = _wrap_open(builtins.open)
    io.open = _wrap_open(io.open)
    os.open = _wrap_os_open(os.open)
    for name in _PATH_METHODS:
        real = getattr(pathlib.Path, name)
        _real[f"Path.{name}"] = real
        setattr(pathlib.Path, name, _wrap_method(name, real))
    _state["installed"] = True


def suspend(suspended: bool) -> None:
    """Suspend the check for a test that plants the unlocked fault itself (its marker), or resume it."""
    _state["suspended"] = suspended


def take_violations() -> list[str]:
    """The accesses recorded since the last call, which are cleared."""
    with _lock:
        taken = list(VIOLATIONS)
        VIOLATIONS.clear()
    return taken


def set_test_id(nodeid: str) -> None:
    """Attribute accesses, including those from threads and finalizers, to this test."""
    global _test_id
    with _lock:
        _test_id = nodeid


def session_violations() -> list[str]:
    """Snapshot every recorded access without clearing the session audit."""
    with _lock:
        return list(_session_violations)
