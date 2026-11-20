"""The startup guard (bead coding-harness-s55e): scripts started with the caller's Python use the checkout's own
environment, and a kit instance keeps its existing fallback.

Every behavioural case starts a real subprocess in a tree of its own (a copy of the guard, a throwaway environment
with a stub `yaml`, controlled interpreters); nothing is downloaded and no provider is called. The "system"
interpreter is the base interpreter of the running one, so it never carries the stub.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import venv
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
GUARD = SCRIPTS / "venv_guard.py"
KIT = SCRIPTS / "kit"
MARKER = "VENV_GUARD_ENTERED"
THIRD_PARTY = frozenset({"yaml", "jinja2", "pydantic"})
# The caller's interpreter: a bare environment of the running Python, without the stubs and without any site
# package of the host. The base interpreter alone is not enough: a hosted CI installs PyYAML into it, and then the
# guard rightly finds nothing missing and never restarts (PR #415, CI run of 2026-11-19). Set per module below.
SYSTEM_PYTHON = str(getattr(sys, "_base_executable", None) or sys.executable)


@pytest.fixture(scope="module", autouse=True)
def _bare_system_python(tmp_path_factory: pytest.TempPathFactory) -> None:
    global SYSTEM_PYTHON
    base = tmp_path_factory.mktemp("system-python")
    venv.EnvBuilder(with_pip=False, symlinks=True, system_site_packages=False).create(base)
    SYSTEM_PYTHON = str(base / "bin" / "python3")
    probe_result = subprocess.run(
        [SYSTEM_PYTHON, "-c", "import importlib.util, sys; sys.exit(importlib.util.find_spec('yaml') is not None)"],
        capture_output=True,
        timeout=60,
    )
    assert probe_result.returncode == 0, "the bare caller interpreter must not import PyYAML"


sys.path.insert(0, str(KIT))
import probe  # noqa: E402

EXPORT_MANIFEST = SCRIPTS / "export" / "manifest.yaml"

TOOL = """\
import os
import sys

import venv_guard  # noqa: F401

print("entered", os.environ.get("VENV_GUARD_ENTERED"), flush=True)
import yaml

print("where", yaml.WHERE)
print("prefix", os.path.realpath(sys.prefix))
print("argv", sys.argv[1:])
print("cwd", os.path.realpath(os.getcwd()))
print("stdin", sys.stdin.read())
print("to-stderr", file=sys.stderr)
sys.exit(7)
"""


# ---------------------------------------------------------------------------
# Trees and runs
# ---------------------------------------------------------------------------


def _tree(base: Path, *, framework: bool, environment: bool, name: str = "tree") -> Path:
    """A checkout (the two framework files) or a kit instance (neither), with or without an environment."""
    root = base / name
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "venv_guard.py").write_text(GUARD.read_text(encoding="utf-8"), encoding="utf-8")
    if framework:
        (root / "pyproject.toml").write_text("[project]\nname = 'fixture'\n", encoding="utf-8")
        (root / "requirements-ci.txt").write_text("", encoding="utf-8")
    if environment:
        venv.EnvBuilder(with_pip=False, symlinks=True).create(root / ".venv")
        site = next((root / ".venv" / "lib").glob("python*/site-packages"))
        (site / "yaml.py").write_text('WHERE = "checkout environment"\n', encoding="utf-8")
        for name in ("jinja2", "pydantic"):
            (site / f"{name}.py").write_text("", encoding="utf-8")
    return root


def _write(root: Path, name: str, text: str) -> Path:
    path = root / "scripts" / name
    path.write_text(text, encoding="utf-8")
    return path


def _run(
    command: list[str], cwd: Path, *, stdin: str = "payload", extra_env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k not in (MARKER, "PYTHONPATH", "PYTHONHOME")}
    env.update(extra_env or {})
    return subprocess.run(command, cwd=cwd, input=stdin, capture_output=True, text=True, env=env, timeout=120)


def _lines(result: subprocess.CompletedProcess[str]) -> list[str]:
    return result.stdout.splitlines()


# ---------------------------------------------------------------------------
# 1 · the checkout's interpreter is used
# ---------------------------------------------------------------------------


def test_direct_invocation_uses_checkout_environment(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    script = _write(root, "tool.py", TOOL)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    environment = os.path.realpath(root / ".venv")

    result = _run([SYSTEM_PYTHON, str(script), "a b", "--c"], elsewhere)

    assert result.returncode == 7, result.stderr
    assert _lines(result) == [
        "entered None",
        "where checkout environment",
        f"prefix {environment}",
        "argv ['a b', '--c']",
        f"cwd {os.path.realpath(elsewhere)}",
        "stdin payload",
    ]
    assert result.stderr == "to-stderr\n"


# ---------------------------------------------------------------------------
# 2 · no repeated replacement
# ---------------------------------------------------------------------------


def test_active_environment_does_not_reexec(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    script = _write(root, "tool.py", TOOL)
    environment = os.path.realpath(root / ".venv")

    already_there = _run([str(root / ".venv" / "bin" / "python3"), str(script)], tmp_path)
    assert already_there.returncode == 7, already_there.stderr
    assert _lines(already_there)[0] == "entered None", "an invocation inside the environment replaced itself"
    assert _lines(already_there)[2] == f"prefix {environment}"

    # The marker names the environment a replacement already entered: a caller that carries it is left alone,
    # so a replacement that did not land in the environment cannot loop.
    probe_script = _write(root, "plain.py", "import sys\nimport venv_guard  # noqa: F401\nprint(sys.prefix)\n")
    marked = _run([SYSTEM_PYTHON, str(probe_script)], tmp_path, extra_env={MARKER: environment})
    assert marked.returncode == 0, marked.stderr
    assert os.path.realpath(marked.stdout.strip()) != environment, "a marked invocation was replaced again"


# ---------------------------------------------------------------------------
# 3 · a framework checkout without an environment says `make venv`
# ---------------------------------------------------------------------------


def test_framework_missing_environment_reports_make_venv(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=False)
    script = _write(root, "tool.py", TOOL)

    # `-S` leaves the interpreter without site-packages, so PyYAML is genuinely missing.
    missing = _run([sys.executable, "-S", str(script)], tmp_path)
    assert missing.returncode == 1
    assert "ModuleNotFoundError: No module named 'yaml'" in missing.stderr
    assert "make venv" in missing.stderr.splitlines()[-1]

    # A dangling interpreter is no environment either.
    (root / ".venv" / "bin").mkdir(parents=True)
    (root / ".venv" / "bin" / "python3").symlink_to(tmp_path / "gone")
    broken = _run([sys.executable, "-S", str(script)], tmp_path)
    assert broken.returncode == 1
    assert "make venv" in broken.stderr.splitlines()[-1]

    # An import error that is not a missing dependency stays as it is, without the hint.
    other = _write(root, "other.py", "import venv_guard  # noqa: F401\nimport not_a_dependency_anywhere\n")
    unrelated = _run([sys.executable, "-S", str(other)], tmp_path)
    assert unrelated.returncode == 1
    assert "No module named 'not_a_dependency_anywhere'" in unrelated.stderr
    assert "make venv" not in unrelated.stderr


# ---------------------------------------------------------------------------
# 4 · a kit instance without an environment is left as it was
# ---------------------------------------------------------------------------


def test_kit_without_environment_preserves_behavior(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=False, environment=False)
    script = _write(root, "tool.py", TOOL)

    result = _run([sys.executable, "-S", str(script)], tmp_path)

    assert result.returncode == 1
    assert _lines(result) == ["entered None"], "the guard replaced the process or changed its start"
    assert result.stderr.rstrip().splitlines()[-1] == "ModuleNotFoundError: No module named 'yaml'"
    assert "make venv" not in result.stderr


# ---------------------------------------------------------------------------
# 5 · every direct third-party import has its guard first
# ---------------------------------------------------------------------------


def _third_party(statement: ast.stmt) -> list[str]:
    return probe._third_party(statement)


def unguarded_imports(source: str) -> list[tuple[int, str]]:
    return probe.unguarded_imports(source)


def effects_before_guard(source: str) -> list[int]:
    return probe.effects_before_guard(source)


# Declared exemptions: a script that must not carry the guard, with its reason.
NOT_GUARDED = {
    "scripts/omnigent_policy.py": "runs under Omnigent's own Python, never re-executed into the checkout's .venv",
}


def test_all_third_party_imports_are_guarded() -> None:
    files = sorted(SCRIPTS.rglob("*.py"))
    assert SCRIPTS / "kit" / "probe.py" in files, "the scan must reach nested directories"
    importing: list[str] = []
    unguarded: list[str] = []
    acting_first: list[str] = []
    for path in files:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        if any(_third_party(node) for node in ast.walk(tree) if isinstance(node, ast.stmt)):
            importing.append(path.relative_to(REPO_ROOT).as_posix())
        name = path.relative_to(REPO_ROOT).as_posix()
        if name in NOT_GUARDED:
            continue
        unguarded += [f"{name}:{line} {dependency}" for line, dependency in unguarded_imports(source)]
        if path != GUARD:
            acting_first += [f"{name}:{line}" for line in effects_before_guard(source)]
    assert "scripts/harness.py" in importing and "scripts/omnigent_policy.py" in importing, importing
    assert not unguarded, "third-party import without an earlier `import venv_guard`: " + ", ".join(unguarded)
    assert not acting_first, "statement with an effect before the guard (a restart would repeat it): " + ", ".join(
        acting_first
    )


@pytest.mark.parametrize(
    "source",
    [
        'print("hi")\nimport venv_guard\n',
        "import os\nos.makedirs('x')\nimport venv_guard\n",
        "for i in range(2):\n    pass\nimport venv_guard\n",
        "if True:\n    pass\nimport venv_guard\n",
        "main()\nimport venv_guard\n",
    ],
)
def test_the_guard_check_rejects_effects_before_the_guard(source: str) -> None:
    assert effects_before_guard(source), source


@pytest.mark.parametrize(
    "source",
    [
        '"""doc"""\nfrom __future__ import annotations\nimport os\nimport venv_guard\nprint("x")\n',
        "import sys\nROOT = 1\nsys.path.insert(0, 'x')\nimport venv_guard\nprint('x')\n",
        "def f():\n    print('x')\n\n\nimport venv_guard\n",
        "print('no top-level guard')\n",
        "def load():\n    import venv_guard\n",
    ],
)
def test_the_guard_check_accepts_a_guard_ahead_of_every_effect(source: str) -> None:
    assert not effects_before_guard(source), source


def test_guard_check_visits_match_cases() -> None:
    source = "match value:\n    case 1:\n        import yaml\n"
    assert unguarded_imports(source) == [(3, "yaml")]
    assert not unguarded_imports("import venv_guard\n" + source)


@pytest.mark.parametrize(
    "source",
    [
        "import yaml\n",
        "import yaml\nimport venv_guard\n",
        "# import venv_guard\nimport yaml\n",
        '"import venv_guard"\nimport yaml\n',
        "if False:\n    import venv_guard\nimport yaml\n",
        "from yaml import safe_load\n",
        "import jinja2\n",
        "from pydantic import BaseModel\n",
        "def load():\n    import yaml\n",
        "try:\n    import yaml\nexcept ImportError:\n    pass\n",
        "def guarded():\n    import venv_guard\n\n\ndef other():\n    import yaml\n",
    ],
)
def test_the_guard_check_rejects_unguarded_and_reordered_imports(source: str) -> None:
    assert unguarded_imports(source), source


@pytest.mark.parametrize(
    "source",
    [
        "import venv_guard  # noqa: F401\nimport yaml\n",
        "import os\nimport venv_guard\n\ntry:\n    import yaml\nexcept ImportError:\n    pass\n",
        "def load():\n    import venv_guard\n    import yaml\n",
        "import venv_guard\n\n\ndef load():\n    from pydantic import BaseModel\n    import jinja2\n",
        "import os\nimport json\n",
    ],
)
def test_the_guard_check_accepts_guarded_imports(source: str) -> None:
    assert not unguarded_imports(source), source


# ---------------------------------------------------------------------------
# 6 · an imported guarded module keeps the original entry point
# ---------------------------------------------------------------------------


def test_imported_module_preserves_original_invocation(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    _write(root, "lib.py", 'import venv_guard  # noqa: F401\nimport yaml\n\nprint("lib", yaml.WHERE)\n')
    entry = (
        "import os\nimport sys\n\nimport lib  # noqa: F401\n\n"
        'print("entry", __name__, sys.argv[1:], os.path.realpath(os.getcwd()))\n'
    )
    _write(root, "entry.py", entry)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    by_path = _run([SYSTEM_PYTHON, str(root / "scripts" / "entry.py"), "x", "y"], elsewhere)
    assert by_path.returncode == 0, by_path.stderr
    assert _lines(by_path) == ["lib checkout environment", f"entry __main__ ['x', 'y'] {os.path.realpath(elsewhere)}"]

    by_module = _run([SYSTEM_PYTHON, "-m", "entry", "x"], root / "scripts")
    assert by_module.returncode == 0, by_module.stderr
    assert _lines(by_module) == [
        "lib checkout environment",
        f"entry __main__ ['x'] {os.path.realpath(root / 'scripts')}",
    ]


# ---------------------------------------------------------------------------
# 7 · the exported kit carries the guard
# ---------------------------------------------------------------------------


def _guarded_scripts() -> list[str]:
    guarded = []
    for path in sorted(SCRIPTS.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if any(probe._is_guard(node) for node in ast.walk(tree) if isinstance(node, ast.stmt)):
            guarded.append(path.relative_to(REPO_ROOT).as_posix())
    return guarded


def _export_verdict(path: str) -> str | None:
    rules = yaml.safe_load(EXPORT_MANIFEST.read_text(encoding="utf-8"))["rules"]
    hits = [rule for rule in rules if path.startswith(rule["prefix"])]
    return max(hits, key=lambda rule: len(rule["prefix"]))["verdict"] if hits else None


def test_exported_kit_contains_guard(tmp_path: Path) -> None:
    guard = "scripts/venv_guard.py"
    guarded = _guarded_scripts()
    assert guarded, "no script loads the guard"

    # Both manifests: whatever travels and loads the guard brings the guard.
    travelling = [path for path in guarded if (probe.rolle(path) or ("", ""))[0] == "mechanismus"]
    assert travelling, "no guarded script is part of the kit — the case would check nothing"
    assert (probe.rolle(guard) or ("", ""))[0] == "mechanismus", "the kit manifest does not carry the guard"
    for path in guarded:
        if _export_verdict(path) == "carry":
            assert _export_verdict(guard) == "carry", f"{path} is exported without the guard"

    # A clean instance: only the kit's files, and the guard loads there under a bare interpreter.
    instance = tmp_path / "instance"
    for path in {*travelling, guard}:
        target = instance / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((REPO_ROOT / path).read_text(encoding="utf-8"), encoding="utf-8")
    loaded = _run([sys.executable, "-S", "-c", "import venv_guard"], instance / "scripts")
    assert loaded.returncode == 0, loaded.stderr


def test_active_environment_missing_dependency_reports_hint(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    site = next((root / ".venv" / "lib").glob("python*/site-packages"))
    (site / "yaml.py").unlink()
    script = _write(root, "missing.py", "import venv_guard\nimport yaml\n")

    result = _run([str(root / ".venv" / "bin" / "python3"), str(script)], tmp_path)

    assert result.returncode == 1
    assert "No module named 'yaml'" in result.stderr
    assert "make venv" in result.stderr


def test_guards_from_two_checkouts_replace_process_at_most_once(tmp_path: Path) -> None:
    first = _tree(tmp_path, framework=True, environment=True, name="first")
    second = _tree(tmp_path, framework=True, environment=True, name="second")
    # Only the first environment lacks the dependencies, so the second guard really has to replace the process;
    # the second environment carries them, so the replacement ends the chain and the marker is exercised.
    site = next((first / ".venv" / "lib").glob("python*/site-packages"))
    for dependency in THIRD_PARTY:
        (site / f"{dependency}.py").unlink()
    counter = tmp_path / "starts"
    script = _write(
        first,
        "cross.py",
        "import importlib.util\n"
        "from pathlib import Path\n"
        f"counter = Path({str(counter)!r})\n"
        "count = int(counter.read_text()) + 1 if counter.exists() else 1\n"
        "counter.write_text(str(count))\n"
        "if count > 3: raise SystemExit('replacement loop')\n"
        "import venv_guard\n"
        f"spec = importlib.util.spec_from_file_location('other_guard', {str(second / 'scripts' / 'venv_guard.py')!r})\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n",
    )

    result = _run([str(first / ".venv" / "bin" / "python3"), str(script)], tmp_path)

    assert result.returncode == 0, result.stderr
    assert int(counter.read_text()) == 2, "the second guard must replace the process exactly once"


def test_foreign_marker_allows_checkout_entry(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    script = _write(root, "tool.py", "import venv_guard\nimport yaml\nprint(yaml.WHERE)\n")
    result = _run([SYSTEM_PYTHON, str(script)], tmp_path, extra_env={MARKER: "/foreign/.venv"})
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "checkout environment"


def test_available_dependencies_keep_selected_interpreter(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    packages = tmp_path / "packages"
    packages.mkdir()
    for name in THIRD_PARTY:
        (packages / f"{name}.py").write_text("", encoding="utf-8")
    script = _write(root, "tool.py", "import sys\nimport venv_guard\nprint(sys.prefix)\n")
    result = _run([sys.executable, str(script)], tmp_path, extra_env={"PYTHONPATH": str(packages)})
    assert result.returncode == 0, result.stderr
    assert os.path.realpath(result.stdout.strip()) == os.path.realpath(sys.prefix)


def test_unreplayable_or_broken_environment_reports_hint(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    script = _write(root, "tool.py", "import venv_guard\nimport yaml\n")
    site = next((root / ".venv" / "lib").glob("python*/site-packages"))
    (site / "yaml.py").unlink()
    result = _run([sys.executable, "-S", str(script)], tmp_path)
    assert result.returncode == 1
    assert "make venv" in result.stderr


def test_roster_missing_yaml_is_not_swallowed(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=False)
    (root / "provenance.yaml").write_text("roles: {}\n", encoding="utf-8")
    (root / "scripts" / "ramp_valves.py").write_text((SCRIPTS / "ramp_valves.py").read_text(), encoding="utf-8")
    (root / "scripts" / "_verdict.py").write_text((SCRIPTS / "_verdict.py").read_text(), encoding="utf-8")
    result = _run([sys.executable, "-S", "-c", "import ramp_valves; ramp_valves._roster_handles()"], root / "scripts")
    assert result.returncode != 0
    assert "make venv" in result.stderr


@pytest.mark.parametrize("error", ["ImportError", "ValueError"])
def test_broken_dependency_spec_is_treated_as_missing(tmp_path: Path, error: str) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    script = _write(
        root,
        "broken_spec.py",
        "import importlib.util\n"
        "def broken(name):\n"
        f"    raise {error}('broken spec')\n"
        "importlib.util.find_spec = broken\n"
        "import venv_guard\n"
        "print('guard loaded')\n",
    )
    result = _run([str(root / ".venv" / "bin" / "python3"), str(script)], tmp_path)
    assert result.returncode == 0, f"guard import must survive a broken spec: {result.stderr}"
    assert result.stdout.strip() == "guard loaded"


def test_reentered_process_does_not_pass_marker_to_child(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    child = _write(root, "child.py", "import venv_guard\nimport yaml\nprint(yaml.WHERE)\n")
    parent = _write(
        root,
        "parent.py",
        "import subprocess\nimport sys\nimport venv_guard\n"
        f"result = subprocess.run([{SYSTEM_PYTHON!r}, {str(child)!r}], capture_output=True, text=True)\n"
        "print(result.stdout, end='')\nprint(result.stderr, file=sys.stderr, end='')\n"
        "sys.exit(result.returncode)\n",
    )
    result = _run([SYSTEM_PYTHON, str(parent)], tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "checkout environment"


def test_site_disabled_invocation_enters_checkout_environment(tmp_path: Path) -> None:
    root = _tree(tmp_path, framework=True, environment=True)
    script = _write(root, "tool.py", "import venv_guard\nimport yaml\nprint(yaml.WHERE)\n")
    for flag in ("-S", "-sS"):
        result = _run([sys.executable, flag, str(script), "-S"], tmp_path)
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "checkout environment"


def test_guard_check_detects_calls_in_early_definitions() -> None:
    for source in (
        "result = print('started')\nimport venv_guard\n",
        "@decorate()\ndef f(): pass\nimport venv_guard\n",
        "class C:\n    value = print('started')\nimport venv_guard\n",
    ):
        try:
            result = effects_before_guard(source)
        except AttributeError:
            pytest.fail("the guard check must detect calls before the guard")
        assert result, source


def test_guard_check_rejects_combined_guard_import() -> None:
    try:
        first = unguarded_imports("import yaml, venv_guard\n")
        second = unguarded_imports("import venv_guard, yaml\n")
    except AttributeError:
        pytest.fail("the guard check must reject combined imports")
    assert first
    assert second
