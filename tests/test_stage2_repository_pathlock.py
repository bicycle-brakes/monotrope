"""The repository seats' path lock, tested without Pi and without network.

`scripts/stage2_repository_pathlock.mjs` is the ONLY extension a repository
seat's Pi context loads (decisions.md Q-16, finding F-24, spec criterion 52).
A node driver loads a copy of it and calls its `tool_call` gate the way Pi
does: a path outside the worktree - absolute, through `..`, through a symbolic
link, through `~` - is blocked for read, grep, find and ls; a path inside is
let through. The suite skips when `node` is not installed.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
EXTENSION = HERE.parent / "scripts" / "stage2_repository_pathlock.mjs"
DRIVER = HERE / "stage2_repository_pathlock_driver.mjs"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None, reason="node is not installed; the extension is JavaScript"
)


@dataclass
class World:
    root: Path  # the worktree the seat starts in
    outside: Path  # a directory beside it: the model's home, the state store
    copy: Path

    def gate(self, tool: str, **input_: object) -> dict | None:
        return self.run([{"tool": tool, "input": input_}])[0]["result"]

    def run(self, cases: list[dict]) -> list[dict]:
        done = subprocess.run(
            ["node", str(DRIVER)],
            input=json.dumps({"module": str(self.copy), "root": str(self.root), "cases": cases}),
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ},
            check=False,
        )
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)


@pytest.fixture
def world(tmp_path: Path) -> World:
    root = tmp_path / "worktree"
    (root / "src").mkdir(parents=True)
    (root / "src" / "a.txt").write_text("inside\n", encoding="utf-8")
    outside = tmp_path / "state"
    outside.mkdir()
    (outside / "canary.txt").write_text("CANARY-STATE\n", encoding="utf-8")
    (root / "link-to-outside").symlink_to(outside)
    (root / "link-to-file").symlink_to(outside / "canary.txt")
    (root / "link-inside").symlink_to(root / "src")
    copy = tmp_path / "scratch" / "repository-pathlock.mjs"  # a generic scratch path, as the runner copies it
    copy.parent.mkdir()
    shutil.copy(EXTENSION, copy)
    return World(root, outside, copy)


def blocked(result: dict | None) -> bool:
    return bool(result) and result.get("block") is True and bool(result.get("reason"))


@pytest.mark.parametrize("tool", ["read", "grep", "find", "ls"])
def test_an_absolute_path_outside_the_worktree_is_refused(world: World, tool: str) -> None:
    target = world.outside / "canary.txt" if tool == "read" else world.outside
    args = {"path": str(target)}
    if tool in ("grep", "find"):
        args["pattern"] = "x"
    result = world.gate(tool, **args)
    assert blocked(result), result
    assert "outside the worktree" in result["reason"]


@pytest.mark.parametrize("tool", ["read", "grep", "find", "ls"])
def test_a_dotdot_escape_is_refused(world: World, tool: str) -> None:
    args = {"path": "src/../../state/canary.txt" if tool == "read" else "../state"}
    if tool in ("grep", "find"):
        args["pattern"] = "x"
    assert blocked(world.gate(tool, **args))


@pytest.mark.parametrize("name", ["link-to-outside", "link-to-outside/canary.txt", "link-to-file"])
def test_a_symlink_escape_is_refused(world: World, name: str) -> None:
    assert blocked(world.gate("read", path=name))
    assert blocked(world.gate("ls", path=name))


def test_a_new_name_under_a_symlinked_directory_is_judged_by_where_it_would_be(world: World) -> None:
    assert blocked(world.gate("read", path="link-to-outside/not-yet-there.txt"))


def test_a_home_shortcut_and_the_at_prefix_do_not_get_around_the_lock(world: World) -> None:
    assert blocked(world.gate("read", path="~/.ssh/id_ed25519"))
    assert blocked(world.gate("read", path="@" + str(world.outside / "canary.txt")))


def test_a_path_inside_the_worktree_is_let_through(world: World) -> None:
    for path in (
        "src/a.txt",
        str(world.root / "src" / "a.txt"),
        "src/../src/a.txt",
        "link-inside/a.txt",
        ".",
        "no/such/file",
    ):
        assert world.gate("read", path=path) is None, path
    assert world.gate("ls", path=".") is None
    assert world.gate("ls") is None  # no path: the working directory
    assert world.gate("grep", pattern="inside", path="src", glob="*.txt") is None
    assert world.gate("find", pattern="**/*.txt") is None


def test_a_file_named_with_leading_dots_is_not_mistaken_for_an_escape(world: World) -> None:
    (world.root / "..hidden").write_text("x", encoding="utf-8")
    assert world.gate("read", path="..hidden") is None


def test_an_absolute_or_dotdot_glob_is_refused(world: World) -> None:
    assert blocked(world.gate("find", pattern="../state/*"))
    assert blocked(world.gate("find", pattern=str(world.outside / "*")))
    assert blocked(world.gate("grep", pattern="x", glob="../state/**"))
    assert world.gate("grep", pattern="../x(y)?", path="src") is None  # a grep pattern is a regex, not a path


def test_a_tool_outside_the_four_file_tools_is_blocked(world: World) -> None:
    for tool in ("bash", "write", "edit", "public_fetch"):
        assert blocked(world.gate(tool, command="env")), tool


def test_a_non_string_path_is_refused(world: World) -> None:
    assert blocked(world.gate("read", path=["/etc/passwd"]))
    assert blocked(world.gate("read"))


def test_the_extension_registers_only_a_gate_and_refuses_other_hosts(world: World) -> None:
    loaded, bare = world.run([{"load": True}, {"load": "no-host"}])
    assert loaded == {"events": ["tool_call"]}
    assert "threw" in bare and "Pi host" in bare["threw"]


def test_the_repository_seat_launch_loads_only_the_path_lock(tmp_path: Path) -> None:
    """Run.pi_command keeps --no-extensions and adds the one explicit -e of the lock, copied to a scratch path."""
    import sys
    from types import SimpleNamespace

    sys.path.insert(0, str(HERE.parent / "scripts"))
    import stage2
    from stage2_research_run import Run

    run = Run.__new__(Run)
    run.root, run.change, run.key = tmp_path, "some-change", "k"
    run.selection = {}
    run.runner = SimpleNamespace(
        PI_WRAPPER=Path("/pinned/pi"), PI_TOOLS=stage2.PI_TOOLS, foreign_env=stage2.foreign_env
    )
    scratch = tmp_path / "seat"
    scratch.mkdir()
    command, cwd, _env = run.pi_command({"model": "qwen3.8-flash", "tools": "repository"}, "prompt", scratch)
    assert cwd == tmp_path
    assert command.count("-e") == 1 and command.count("--no-extensions") == 1
    assert command.index("--no-extensions") < command.index("-e")
    loaded = Path(command[command.index("-e") + 1])
    assert loaded.parent == scratch and loaded.read_text(encoding="utf-8") == EXTENSION.read_text(encoding="utf-8")
    assert command[command.index("--tools") + 1] == "read,grep,find,ls"


@pytest.mark.parametrize("tool", ["read", "grep", "find", "ls"])
def test_a_file_url_is_judged_where_pi_reads_it(world: World, tool: str) -> None:
    """Pi turns a `file://` path into a real path with fileURLToPath; the lock must judge that path (RS-3-2)."""
    target = world.outside / "canary.txt" if tool == "read" else world.outside
    args = {"path": target.as_uri()}
    if tool in ("grep", "find"):
        args["pattern"] = "x"
    result = world.gate(tool, **args)
    assert blocked(result), result
    assert "outside the worktree" in result["reason"]
    inside = world.root / "src" / ("a.txt" if tool == "read" else "")
    args["path"] = inside.as_uri()
    assert world.gate(tool, **args) is None


def test_an_unreadable_file_url_is_refused(world: World) -> None:
    assert blocked(world.gate("read", path="file://remote-host/etc/hostname"))


def test_unicode_spaces_are_normalised_as_pi_normalises_them(world: World) -> None:
    # Pi maps U+00A0, U+2000-U+200A, U+202F, U+205F and U+3000 to a space before resolving.
    (world.root / "a b").mkdir()
    (world.root / "a b" / "c").symlink_to(world.outside)
    for space in ("\u00a0", "\u2007", "\u202f", "\u205f", "\u3000"):
        assert blocked(world.gate("ls", path=f"a{space}b/c")), repr(space)


@pytest.mark.parametrize(
    ("planted", "asked"),
    [
        ("notes\u2019", "notes'"),  # Pi's curly-quote fallback
        ("cafe\u0301", "caf\u00e9"),  # Pi's NFD fallback
        ("Shot 1\u202fPM.d", "Shot 1 PM.d"),  # Pi's macOS AM/PM fallback
    ],
)
def test_reads_through_pi_fallback_names_are_judged_too(world: World, planted: str, asked: str) -> None:
    """Pi's read falls back to curly-quote, NFD and AM/PM variants of a missing path (RS-3-6)."""
    (world.root / planted).symlink_to(world.outside)
    assert blocked(world.gate("read", path=f"{asked}/canary.txt"))
    assert blocked(world.gate("read", path=f"{planted}/canary.txt"))
    (world.root / f"{planted}-in").mkdir()
    (world.root / f"{planted}-in" / "x.txt").write_text("x", encoding="utf-8")
    assert world.gate("read", path=f"{asked}-in/x.txt") is None
