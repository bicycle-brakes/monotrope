"""Start a script under the checkout's own environment, before it imports a third-party dependency.

Importing this module IS the guard (bead coding-harness-s55e). Put

    import venv_guard  # noqa: F401

before the first import of PyYAML, Jinja2 or pydantic — in a function, before that function's own import, when
the dependency is imported lazily. The module uses the standard library only, so it loads under any `python3`.

What it does, in order:

1. The checkout is the parent of the directory this file lives in, never the current directory. When its
   `.venv/bin/python3` is usable, a dependency is missing and the process does not already run there, it is replaced
   by that interpreter with the original command line (`sys.orig_argv`): the same script or `-m` module, the same
   arguments, working directory, standard streams and exit status. An importing script is therefore never replaced
   by the module it imports — the replacement restarts whatever the caller originally ran. A marker in the
   environment names the environment already entered, so no invocation loops.
2. In a framework checkout (it carries `pyproject.toml` and
   `requirements-ci.txt`, which the kit does not) an uncaught missing PyYAML, Jinja2 or pydantic gets one extra
   line after its traceback telling the caller to run `make venv`; the exit status and every other error stay as
   they were.
3. A kit instance without a `.venv` is left exactly as it was: no replacement, no hint.
"""

from __future__ import annotations

import contextlib
import importlib.util
import os
import sys
from pathlib import Path

CHECKOUT = Path(__file__).resolve().parent.parent
VENV = CHECKOUT / ".venv"
MARKER = "VENV_GUARD_ENTERED"
DEPENDENCIES = frozenset({"yaml", "jinja2", "pydantic"})
HINT = "venv-guard: the dependency '{name}' is missing and this checkout has a missing or unusable environment - run `make venv`."


def _usable(python: Path) -> bool:
    """A file that can be started. A dangling link or a deleted base interpreter is not usable."""
    return python.is_file() and os.access(python, os.X_OK)


def _active() -> bool:
    return os.path.realpath(sys.prefix) == os.path.realpath(VENV)


def _original_command() -> list[str] | None:
    """The interpreter's own command line, or None where it cannot be replayed (stdin, interactive, Python < 3.10)."""
    original = getattr(sys, "orig_argv", None)
    if not original or len(original) < 2 or sys.argv[0] in ("", "-"):
        return None
    return list(original)


def _reexec(python: Path) -> None:
    """Replace this process; return only when that is impossible."""
    command = _original_command()
    if command is None:
        return
    os.environ[MARKER] = str(VENV)
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(OSError, ValueError):
            stream.flush()
    # Remove -S only from interpreter options, never from the script arguments.
    options = command[1:]
    index = 0
    while index < len(options):
        arg = options[index]
        if arg in ("-c", "-m", "--") or not arg.startswith("-") or arg == "-":
            break
        if arg.startswith("-") and not arg.startswith(("--", "-W", "-X")) and "S" in arg:
            options[index] = arg.replace("S", "")
            if options[index] == "-":
                options.pop(index)
                continue
        if arg in ("-W", "-X"):
            index += 1
        index += 1
    try:
        os.execv(str(python), [str(python), *options])
    except OSError:
        os.environ.pop(MARKER, None)


def _is_framework_checkout() -> bool:
    return (CHECKOUT / "pyproject.toml").is_file() and (CHECKOUT / "requirements-ci.txt").is_file()


def _install_hint() -> None:
    previous = sys.excepthook
    if getattr(previous, "_venv_guard", False):
        return

    def hook(kind, value, trace):
        previous(kind, value, trace)
        if issubclass(kind, ModuleNotFoundError):
            name = (getattr(value, "name", None) or "").split(".")[0]
            if name in DEPENDENCIES:
                print(HINT.format(name=name), file=sys.stderr)

    hook._venv_guard = True  # type: ignore[attr-defined]
    sys.excepthook = hook


def _missing(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is None
    except (ImportError, ValueError):
        return True


def ensure() -> None:
    """Enter the checkout's environment when there is one; otherwise explain, in a framework checkout only."""
    entered = os.environ.pop(MARKER, None)
    python = VENV / "bin" / "python3"
    if _is_framework_checkout():
        _install_hint()
    missing = any(_missing(name) for name in DEPENDENCIES)
    if missing and _usable(python) and not _active() and entered != str(VENV):
        _reexec(python)


ensure()
