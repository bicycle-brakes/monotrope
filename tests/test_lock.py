"""The project file, its lock and the interpreter that runs the suite (bead coding-harness-ei0).

This module reads this repository's own lock (`requirements-ci.txt`) and project
file (`pyproject.toml`). Neither file travels with the kit — an instance
declares its own — so the module is `bestand` and does not run in the probe copy.

Three questions, one module, because they are one promise: *the suite runs on
exactly the packages the lock names, under an interpreter the CI also runs.*

1. Is every pin of the project file exact, and does the lock hold that version?
2. Does the environment that runs the suite hold what the lock holds?
3. Is the interpreter that runs the suite one of the declared interpreters?

The checks are functions of this module, fed by the tests — so a test can feed a
constructed input and see the check go red, which is the only way to know the
check can go red at all. No new script: the gate `pytest` runs this file in every
leg of the CI and in every local run.
"""

from __future__ import annotations

import functools
import importlib.metadata
import re
import sys
import tomllib
from pathlib import Path

import pytest
import yaml
from packaging.markers import Marker
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCK = REPO_ROOT / "requirements-ci.txt"
PROJECT_FILE = REPO_ROOT / "pyproject.toml"
EXPORT_MANIFEST = REPO_ROOT / "scripts" / "export" / "manifest.yaml"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "kit"))
import ci_gates  # noqa: E402
import probe  # noqa: E402

HINT = "build the locked environment: make venv (or set PYTHON to an interpreter built from requirements-ci.txt)"
LOCK_HINT = "regenerate the lock with make lock, then " + HINT

# An entry of the lock starts in column 0 as `name==version`, with an optional
# environment marker, then the line continues with `\` and the `--hash` lines.
_ENTRY = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)==(?P<version>[^\s;\\]+)\s*(?:;\s*(?P<marker>[^\\]+?))?\s*\\?\s*$"
)


def lock_pins(text: str) -> dict[str, tuple[str, str | None]]:
    """The pins of a lock: normalised name to (version, marker or None)."""
    pins: dict[str, tuple[str, str | None]] = {}
    for line in text.splitlines():
        found = _ENTRY.match(line)
        if found:
            pins[canonicalize_name(found["name"])] = (found["version"], found["marker"])
    return pins


def pin_problems(specs: list[str], locked: dict[str, tuple[str, str | None]]) -> list[str]:
    """What is wrong between the project file's specs and the lock; empty = fine.

    A spec is fine when it is one exact `==` pin (no range, no wildcard) and the
    lock holds that very version of that package.
    """
    problems: list[str] = []
    for spec in specs:
        requirement = Requirement(spec)
        name = canonicalize_name(requirement.name)
        operators = [(s.operator, s.version) for s in requirement.specifier]
        if len(operators) != 1 or operators[0][0] != "==" or operators[0][1].endswith(".*"):
            problems.append(f"{requirement.name}: {spec!r} is not an exact == pin; {LOCK_HINT}")
            continue
        wanted = operators[0][1]
        if name not in locked:
            problems.append(f"{requirement.name}: the lock has no entry for {wanted}; {LOCK_HINT}")
        elif locked[name][0] != wanted:
            problems.append(
                f"{requirement.name}: the project file pins {wanted}, the lock holds {locked[name][0]}; {LOCK_HINT}"
            )
    return problems


def environment_problems(
    locked: dict[str, tuple[str, str | None]],
    installed: dict[str, str],
    interpreter: str,
    declared: list[str],
) -> list[str]:
    """What differs between the lock and the running environment; empty = fine.

    A pin whose marker does not apply to this environment is skipped. A package
    that is installed beyond the lock is tolerated: the CI installs only the lock,
    so an import of anything else goes red there.
    """
    problems: list[str] = []
    if interpreter not in declared:
        problems.append(f"Python {interpreter} is not a declared interpreter ({', '.join(declared)}); {HINT}")
    for name, (version, marker) in sorted(locked.items()):
        if marker is not None and not Marker(marker).evaluate():
            continue
        if name not in installed:
            problems.append(f"{name} {version} is locked but not installed; {HINT}")
        elif installed[name] != version:
            problems.append(f"{name}: the lock holds {version}, the environment {installed[name]}; {HINT}")
    return problems


@functools.lru_cache(maxsize=1)
def _locked() -> dict[str, tuple[str, str | None]]:
    return lock_pins(LOCK.read_text(encoding="utf-8"))


def _specs() -> list[str]:
    project = tomllib.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    return [*project["project"]["dependencies"], *project["dependency-groups"]["dev"]]


def _installed() -> dict[str, str]:
    return {canonicalize_name(d.metadata["Name"]): d.version for d in importlib.metadata.distributions()}


def _interpreter() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


# --------------------------------------------------------------------------
# 1 · The project file and the lock agree
# --------------------------------------------------------------------------


def test_the_lock_is_not_empty() -> None:
    """An empty lock makes every later check green over zero packages."""
    assert len(_locked()) >= 6, f"the lock holds {len(_locked())} pins — the parser found nothing to compare"


def test_every_pin_of_the_project_file_is_exact_and_locked() -> None:
    specs = _specs()
    assert len(specs) >= 6, "the project file names fewer packages than the six it must pin"
    assert pin_problems(specs, _locked()) == []


def test_a_range_or_a_stale_pin_goes_red() -> None:
    """The check can fail: fed a range, an old pin, a pin the lock lacks."""
    locked = _locked()
    assert pin_problems(["pydantic==2.13.5"], locked) == [], "the control: the right pin passes"

    # A range is refused as a range — also when its bound is the very version the
    # lock holds, where a version comparison alone would find nothing to say.
    for spec in ("pydantic>=2.13", "pydantic>=2.13.5", "pydantic~=2.13.5", "pydantic==2.13.*", "pydantic"):
        range_problems = pin_problems([spec], locked)
        assert len(range_problems) == 1 and "pydantic" in range_problems[0] and "exact" in range_problems[0], (
            spec,
            range_problems,
        )

    stale_problems = pin_problems(["pydantic==2.13.4"], locked)
    assert len(stale_problems) == 1 and "pydantic" in stale_problems[0] and "2.13.4" in stale_problems[0], (
        stale_problems
    )

    missing_problems = pin_problems(["not-in-the-lock==1.0"], locked)
    assert len(missing_problems) == 1 and "not-in-the-lock" in missing_problems[0], missing_problems


def test_the_lock_names_a_package_by_its_normalised_name() -> None:
    """`PyYAML` in the project file is `pyyaml` in the lock; the comparison must not mind."""
    pins = lock_pins(
        "pyyaml==6.0.2 \\\n    --hash=sha256:00\ncolorama==0.4.6 ; sys_platform == 'win32' \\\n    --hash=sha256:11\n"
    )
    assert pins == {"pyyaml": ("6.0.2", None), "colorama": ("0.4.6", "sys_platform == 'win32'")}
    assert pin_problems(["PyYAML==6.0.2"], pins) == []


# --------------------------------------------------------------------------
# 2 · The environment that runs the suite is the locked one
# --------------------------------------------------------------------------


def test_the_environment_matches_the_lock() -> None:
    problems = environment_problems(_locked(), _installed(), _interpreter(), ci_gates.interpreters())
    assert problems == [], "\n".join(problems)


def test_a_drifted_package_goes_red() -> None:
    """The check can fail: fed pydantic 2.10.6 and no Jinja2."""
    locked = {"pydantic": ("2.13.5", None), "jinja2": ("3.1.6", None), "pyyaml": ("6.0.2", None)}
    installed = {"pydantic": "2.10.6", "pyyaml": "6.0.2"}
    problems = environment_problems(locked, installed, "3.12", ["3.11", "3.12"])
    assert len(problems) == 2, problems
    assert any("pydantic" in p and "2.13.5" in p and "2.10.6" in p for p in problems), problems
    assert any("jinja2" in p and "not installed" in p for p in problems), problems
    assert all(p.endswith(HINT) for p in problems), "every message tells how to build the environment"
    assert all("make venv" in p for p in problems)


def test_a_version_is_compared_whole_not_by_prefix() -> None:
    locked = {"pydantic": ("2.13.5", None)}
    for installed_version in ("2.13", "2.13.50", "2.13.5.post1", "2.13.5+local"):
        problems = environment_problems(locked, {"pydantic": installed_version}, "3.12", ["3.12"])
        assert len(problems) == 1, (installed_version, problems)
    assert environment_problems(locked, {"pydantic": "2.13.5"}, "3.12", ["3.12"]) == []


def test_a_marker_that_does_not_apply_is_skipped_and_one_that_does_is_not() -> None:
    elsewhere = {"colorama": ("0.4.6", "sys_platform == 'no-such-platform'")}
    assert environment_problems(elsewhere, {}, "3.12", ["3.12"]) == [], "a pin for another platform is not owed"
    here = {"colorama": ("0.4.6", f"python_version >= '{_interpreter()}'")}
    problems = environment_problems(here, {}, "3.12", ["3.12"])
    assert len(problems) == 1 and "colorama" in problems[0], problems


def test_an_undeclared_interpreter_goes_red() -> None:
    """The check can fail: fed Python 3.13 against the declared 3.11 and 3.12."""
    assert environment_problems({}, {}, "3.12", ["3.11", "3.12"]) == [], "the control: a declared one passes"
    problems = environment_problems({}, {}, "3.13", ["3.11", "3.12"])
    assert len(problems) == 1 and "3.13" in problems[0] and "make venv" in problems[0], problems


# --------------------------------------------------------------------------
# 3 · What the project file says about pytest, and where the files stay
# --------------------------------------------------------------------------


def test_the_repository_root_is_on_pytests_path(pytestconfig: pytest.Config) -> None:
    """`harness/` at the root is importable by the suite without a `sys.path` line per test."""
    roots = [Path(p).resolve() for p in pytestconfig.getini("pythonpath")]
    assert REPO_ROOT in roots, f"pytest's pythonpath is {roots}; the project file must carry pythonpath = ['.']"


def test_make_venv_installs_the_lock_in_hash_checking_mode() -> None:
    """`make venv` builds `.venv` in the checkout and installs only the lock, with `--require-hashes`.

    The environment check above cannot see the flag: pip also checks hashes when a
    file carries them, so the same venv comes out without it. The flag is what
    makes a lock without hashes an error, so the recipe is read here.
    """
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    found = re.search(r"^venv:\n((?:\t.*\n)+)", makefile, re.M)
    assert found, "the Makefile has no target `venv`"
    recipe = [line.strip() for line in found.group(1).splitlines()]
    assert recipe == [
        "python3 -m venv .venv",
        ".venv/bin/python3 -m pip install --require-hashes -r requirements-ci.txt",
    ], recipe


def _export_verdicts(path: str) -> list[tuple[str, str]]:
    rules = yaml.safe_load(EXPORT_MANIFEST.read_text(encoding="utf-8"))["rules"]
    return [(r["prefix"], r["verdict"]) for r in rules if path.startswith(r["prefix"])]


@pytest.mark.parametrize("path", ["pyproject.toml", "requirements-ci.txt"])
def test_the_lock_and_the_project_file_stay_home(path: str) -> None:
    """Neither file travels: kit role `bestand`, export verdict `drop` by the catch-all alone."""
    role = probe.rolle(path)
    assert role is not None and role[0] == "bestand", f"{path}: kit role {role}"
    assert path in probe.getrackte_dateien(), f"{path} is not tracked — the check would read a file that is not there"
    assert _export_verdicts(path) == [("", "drop")], (
        f"{path}: only the catch-all may match, got {_export_verdicts(path)}"
    )
