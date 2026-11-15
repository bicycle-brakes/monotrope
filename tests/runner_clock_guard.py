"""The runtime clock guard: the choke point that the runner's clock reads go through `clock_now`.

Spec runner-clock, criterion 2 and its Boundary; decisions.md Q-2 (maintainer,
2026-11-15). The static guard in `tests/test_stage2.py` reads the runner's
source and stays as a cheap advisory check; five review findings of that one
mechanism showed a static reading cannot close the set of spellings
(`time.monotonic.__call__()`, a default argument evaluated at import, ...).
This module closes it at run time instead.

`install()` runs once, when `tests/conftest.py` is imported and before any test
module imports the runner. It replaces every clock-reading `time` function
with a wrapper on the `time` module, and the clock-reading class methods of
`datetime.date` and `datetime.datetime` with wrappers in the types' own
dictionaries. Every alias, `from … import`, default argument, `__call__`,
`getattr` or `functools.partial` the runner builds therefore reaches a
wrapper, at import as at call time. A wrapper looks at the Python frame that
called it: a frame from a guarded runner file outside the one module-level
`clock_now` is recorded and raises `RunnerClockRead`. The standard library,
test code and every other module keep reading freely, so the frame - not a
list of spellings - decides. The record stands even when runner code swallows
the exception; the autouse fixture in `tests/conftest.py` fails the test on any
new record.

A clock callable the runner holds instead of reading by attribute is the one
shape a frame check misses: an original bound before `install()` escapes the
wrappers, and a held wrapper (a dataclass `default_factory`, a thread target)
can be called from a frame that is not the runner's. `bound_reference_violations`
finds both in a module's globals, its functions' defaults, keyword defaults and
closures, and its classes' attributes and dataclass fields; the autouse
fixture runs it once per imported runner module.
"""

from __future__ import annotations

import contextlib
import ctypes
import dataclasses
import datetime as dt
import functools
import gc
import os
import sys
import time
import types
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The files whose frames may not read a machine clock outside `clock_now`: the
# runner as the spec defines it. Every other `scripts/stage2*.py` keeps its own
# clock boundary (spec, Terms and Protected areas); a record-only census of the
# test session on 2026-11-15 found direct reads there (decisions.md, Q-2).
GUARDED_FILES = frozenset({os.path.realpath(REPO_ROOT / "scripts" / "stage2.py")})
# The one function whose body may acquire: a module-level definition, so a
# nested or class-level `clock_now` has a different qualified name.
BOUNDARY_QUALNAME = "clock_now"

# The complete declared set of `time` functions that read or wait on a machine
# clock (Python 3.12+: wall, monotonic, performance, CPU and raw POSIX clocks).
# The static and the runtime guard share these sets.
TIME_CLOCK_ATTRS = {
    "time",
    "time_ns",
    "monotonic",
    "monotonic_ns",
    "perf_counter",
    "perf_counter_ns",
    "process_time",
    "process_time_ns",
    "thread_time",
    "thread_time_ns",
    "clock_gettime",
    "clock_gettime_ns",
    "sleep",
}
# The `time` conversions that read the current time only when the instant is
# left out: the value is the number of positional arguments that makes the call
# a pure conversion. `strftime(format)` formats now; `strftime(format, tuple)` does not.
TIME_CONVERSION_ATTRS = {"ctime": 1, "localtime": 1, "gmtime": 1, "asctime": 1, "strftime": 2}
# The `datetime`/`date` class methods that answer the current wall time or date.
DATETIME_CLOCK_ATTRS = {"now", "utcnow", "today"}
CLOCK_MODULES = ("time", "datetime")
# The `time` callables that neither read nor wait on a clock: pure conversions,
# clock metadata and the setters (a write, never a reading). With the two sets
# above they classify every public callable the installed `time` module has;
# `test_runner_clock_guard_sets_classify_the_installed_modules` holds that.
TIME_NON_CLOCK_ATTRS = {
    "clock_getres",
    "clock_settime",
    "clock_settime_ns",
    "get_clock_info",
    "mktime",
    "pthread_getcpuclockid",
    "strptime",
    "struct_time",
    "tzset",
}
# The `datetime`/`date`/`time` class methods that build a value from their arguments alone.
DATETIME_NON_CLOCK_ATTRS = {
    "combine",
    "fromisocalendar",
    "fromisoformat",
    "fromordinal",
    "fromtimestamp",
    "strptime",
    "utcfromtimestamp",
}


class RunnerClockRead(AssertionError):
    """A guarded runner frame read a machine clock outside `clock_now`."""


@dataclass(frozen=True)
class Read:
    """One clock read a guarded frame made outside the boundary."""

    api: str
    filename: str
    lineno: int
    function: str
    during_test: bool

    def __str__(self) -> str:
        return f"{self.api} read in {self.function} at {self.filename}:{self.lineno}"


# Every read recorded this session, in order; `capture` removes what it hands out.
READS: list[Read] = []
# Whether a test is running: a read outside one happened at import or collection.
_state = {"in_test": False, "installed": False}
# The originals the wrappers replaced, keyed by their public dotted name.
ORIGINALS: dict[str, object] = {}
# The installed wrappers, keyed like ORIGINALS: the time functions themselves,
# the datetime entries as the classmethod objects in the type dictionaries.
WRAPPERS: dict[str, object] = {}
# The classes whose dictionaries hold a datetime wrapper, by attribute name.
_DATETIME_OWNERS = {"now": dt.datetime, "utcnow": dt.datetime, "today": dt.date}

_guarded_cache: dict[str, bool] = {}


def is_guarded(filename: str) -> bool:
    """Whether code compiled from `filename` belongs to a guarded runner file."""
    known = _guarded_cache.get(filename)
    if known is None:
        known = os.path.realpath(filename) in GUARDED_FILES
        _guarded_cache[filename] = known
    return known


def _judge(frame: types.FrameType, api: str) -> None:
    code = frame.f_code
    if not is_guarded(code.co_filename) or code.co_qualname == BOUNDARY_QUALNAME:
        return
    read = Read(api, code.co_filename, frame.f_lineno, code.co_qualname, _state["in_test"])
    READS.append(read)
    raise RunnerClockRead(f"runner clock read outside clock_now: {read}")


def _time_wrapper(name: str, original: Callable[..., object]) -> Callable[..., object]:
    def wrapper(*args: object, **kwargs: object) -> object:
        _judge(sys._getframe(1), f"time.{name}")
        return original(*args, **kwargs)

    wrapper.__name__ = wrapper.__qualname__ = name
    return wrapper


def _conversion_wrapper(name: str, positional: int, original: Callable[..., object]) -> Callable[..., object]:
    def wrapper(*args: object, **kwargs: object) -> object:
        if len(args) < positional or args[positional - 1] is None:
            _judge(sys._getframe(1), f"time.{name}")
        return original(*args, **kwargs)

    wrapper.__name__ = wrapper.__qualname__ = name
    return wrapper


def _datetime_wrapper(owner: type, name: str, original: object) -> classmethod:
    label = f"{owner.__name__}.{name}"

    def wrapper(cls: type, *args: object, **kwargs: object) -> object:
        _judge(sys._getframe(1), label)
        return original.__get__(None, cls)(*args, **kwargs)  # type: ignore[attr-defined]

    wrapper.__name__ = name
    wrapper.__qualname__ = label
    return classmethod(wrapper)


def _type_dict(owner: type) -> dict[str, object]:
    """The writable dictionary behind a built-in type's read-only mapping proxy."""
    (namespace,) = gc.get_referents(owner.__dict__)
    return namespace


def _guarded_modules() -> list[types.ModuleType]:
    found = []
    for module in list(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if isinstance(filename, str) and is_guarded(filename):
            found.append(module)
    return found


def install() -> None:
    """Wrap every clock read in place; idempotent. Refuses when the runner is already imported.

    A runner imported before the wrappers holds whatever it bound at import,
    and an import-time read has already happened unseen, so the guard would
    claim more than it checks.
    """
    if _state["installed"]:
        return
    early = _guarded_modules()
    if early:
        raise RuntimeError(f"the runner was imported before the clock guard: {[m.__name__ for m in early]}")
    for name in sorted(TIME_CLOCK_ATTRS):
        original = getattr(time, name)
        ORIGINALS[f"time.{name}"] = original
        WRAPPERS[f"time.{name}"] = _time_wrapper(name, original)
    for name, positional in sorted(TIME_CONVERSION_ATTRS.items()):
        original = getattr(time, name)
        ORIGINALS[f"time.{name}"] = original
        WRAPPERS[f"time.{name}"] = _conversion_wrapper(name, positional, original)
    for key, wrapper in WRAPPERS.items():
        setattr(time, key.removeprefix("time."), wrapper)
    for name, owner in _DATETIME_OWNERS.items():
        key = f"{owner.__name__}.{name}"
        original = owner.__dict__[name]
        ORIGINALS[key] = original
        WRAPPERS[key] = _datetime_wrapper(owner, name, original)
        _type_dict(owner)[name] = WRAPPERS[key]
    for owner in (dt.date, dt.datetime):
        ctypes.pythonapi.PyType_Modified(ctypes.py_object(owner))
    _state["installed"] = True
    problems = installation_problems()
    if problems:
        raise RuntimeError(f"the clock guard did not take effect: {problems}")


def installation_problems() -> list[str]:
    """Each wrapper that is not where a clock read resolves; empty when the guard is live."""
    problems = []
    if not _state["installed"]:
        return ["the clock guard is not installed"]
    for key, wrapper in WRAPPERS.items():
        if key.startswith("time."):
            if getattr(time, key.removeprefix("time.")) is not wrapper:
                problems.append(f"{key} is displaced")
            continue
        name = key.rsplit(".", 1)[1]
        func = wrapper.__func__  # type: ignore[attr-defined]
        subclass = type("Probe", (_DATETIME_OWNERS[name],), {})
        for owner in (_DATETIME_OWNERS[name], subclass):
            if getattr(getattr(owner, name), "__func__", None) is not func:
                problems.append(f"{owner.__name__}.{name} does not resolve to the guard")
        if name == "today" and getattr(dt.datetime.today, "__func__", None) is not func:
            problems.append("datetime.today does not resolve to the guard")
    return problems


def _clock_named(value: object) -> str | None:
    """The public name of the clock callable `value` is, wraps or binds; None for anything else.

    Both an original and a wrapper count: an original escapes the guard, and a
    wrapper the runner holds can be called later from a frame that is not the
    runner's - a dataclass `default_factory` runs in generated `__init__` code,
    a thread target in the standard library - so the read would pass unseen.
    """
    for key, original in ORIGINALS.items():
        if value is original:
            return f"the original {key}"
    for key, wrapper in WRAPPERS.items():
        func = getattr(wrapper, "__func__", wrapper)
        if value is wrapper or getattr(value, "__func__", None) is func:
            return f"the clock callable {key}"
    if isinstance(value, types.BuiltinMethodType):
        owner = getattr(value, "__self__", None)
        if isinstance(owner, type) and issubclass(owner, dt.date) and value.__name__ in DATETIME_CLOCK_ATTRS:
            return f"the original {owner.__name__}.{value.__name__}"
    if isinstance(value, functools.partial):
        return _clock_named(value.func)
    wrapped = getattr(value, "__self__", None)
    if isinstance(value, types.MethodWrapperType) and wrapped is not None:
        return _clock_named(wrapped)
    if isinstance(value, dataclasses.Field):
        return _clock_named(value.default_factory) or _clock_named(value.default)
    return None


def _values(value: object, depth: int = 3) -> Iterator[object]:
    yield value
    if depth <= 0:
        return
    if isinstance(value, dict):
        items: list[object] = [*value.keys(), *value.values()]
    elif isinstance(value, tuple | list | set | frozenset):
        items = list(value)
    else:
        return
    for item in items:
        yield from _values(item, depth - 1)


def _function_slots(where: str, function: types.FunctionType) -> Iterator[tuple[str, object]]:
    for index, default in enumerate(function.__defaults__ or ()):
        yield f"{where} default {index}", default
    for name, default in (function.__kwdefaults__ or {}).items():
        yield f"{where} keyword default {name}", default
    for name, cell in zip(function.__code__.co_freevars, function.__closure__ or (), strict=False):
        with contextlib.suppress(ValueError):
            yield f"{where} closure {name}", cell.cell_contents


def bound_reference_violations(module: types.ModuleType) -> list[str]:
    """Every clock callable `module` holds bound rather than reading it by attribute at call time.

    It looks where a reference bound at import lives: the module's globals,
    its functions' defaults, keyword defaults and closure cells, and its
    classes' attributes (with their methods' defaults and closures and their
    dataclass fields). An original escapes the wrappers; a held wrapper can be
    called from a frame that is not the runner's. `clock_now` reads by
    attribute, so the runner holds neither.
    """
    slots: list[tuple[str, object]] = []
    for name, value in vars(module).items():
        slots.append((f"global {name}", value))
        if isinstance(value, types.FunctionType) and value.__module__ == module.__name__:
            slots.extend(_function_slots(f"function {name}", value))
        elif isinstance(value, type) and value.__module__ == module.__name__:
            for attr, member in vars(value).items():
                slots.append((f"class {name}.{attr}", member))
                inner = member.__func__ if isinstance(member, staticmethod | classmethod) else member
                if isinstance(inner, types.FunctionType):
                    slots.extend(_function_slots(f"method {name}.{attr}", inner))
    found = []
    for where, value in slots:
        for item in _values(value):
            named = _clock_named(item)
            if named:
                found.append(f"{module.__name__}: {where} holds {named}")
    return found


_scanned: set[int] = set()


def unscanned_bound_reference_violations() -> list[str]:
    """`bound_reference_violations` of each guarded module not yet scanned this session."""
    found = []
    for module in _guarded_modules():
        if id(module) in _scanned:
            continue
        _scanned.add(id(module))
        found.extend(bound_reference_violations(module))
    return found


def import_time_reads() -> list[Read]:
    """The recorded reads no test was running for: an import or collection read."""
    return [read for read in READS if not read.during_test]


_reported: set[int] = set()


def unreported_import_time_reads() -> list[Read]:
    """The import-time reads no test has failed for yet; each is handed out once per session."""
    found = [read for read in import_time_reads() if id(read) not in _reported]
    _reported.update(id(read) for read in found)
    return found


@contextlib.contextmanager
def in_test() -> Iterator[None]:
    """Mark the reads inside as made during a test (the autouse fixture's bracket)."""
    _state["in_test"] = True
    try:
        yield
    finally:
        _state["in_test"] = False


@contextlib.contextmanager
def capture() -> Iterator[list[Read]]:
    """Hand a planted-bypass test the reads made inside, and take them out of the session record."""
    start = len(READS)
    caught: list[Read] = []
    try:
        yield caught
    finally:
        caught.extend(READS[start:])
        del READS[start:]
