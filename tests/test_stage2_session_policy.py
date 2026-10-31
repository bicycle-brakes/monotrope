"""The policy extension of an interactive Pi session, tested without Pi and without a model.

`scripts/stage2_session_policy.mjs` is what the runner copies into a session's private directory and
loads with `pi --no-extensions -e <copy>` (plans/changes/stage2-session/spec.md, criterion 11). A node
driver (`stage2_session_policy_driver.mjs`) loads a copy of it and calls its `tool_call` handler with
made-up events in a temporary worktree: paths inside and outside, symlinks, the protected places,
dangerous and harmless shell commands, and a handler that fails.

Each rule has a case that goes red when the rule is removed; the runs that proved it are in
`plans/changes/stage2-session/plan.md`. The suite skips when `node` is not installed.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
POLICY = HERE.parent / "scripts" / "stage2_session_policy.mjs"
DRIVER = HERE / "stage2_session_policy_driver.mjs"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None, reason="node is not installed; the policy extension is JavaScript"
)

PATH_TOOLS = ("read", "grep", "find", "ls", "edit", "write")
WRITE_TOOLS = ("edit", "write")
READ_TOOLS = ("read", "grep", "find", "ls")


@dataclass
class World:
    root: Path  # the worktree, the session's cwd
    out: Path  # a directory beside it
    home: Path  # $HOME for the node run, outside the worktree
    policy: Path  # the copy of the extension that is loaded, inside the worktree

    def run(self, cases: list[dict]) -> list[dict]:
        request = {"module": str(self.policy), "cases": cases}
        done = subprocess.run(
            ["node", str(DRIVER)],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "HOME": str(self.home)},
            check=False,
        )
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)

    def call(self, tool: str, **fields: object) -> dict:
        return self.run([self.case(tool, **fields)])[0]

    def case(self, tool: str, **fields: object) -> dict:
        extra = {key: fields.pop(key) for key in ("hasUI", "answer", "explode") if key in fields}
        return {"mode": "handler", "cwd": str(self.root), "event": {"toolName": tool, "input": fields}, **extra}


@pytest.fixture
def world(tmp_path: Path) -> World:
    root, out, home = tmp_path / "wt", tmp_path / "out", tmp_path / "home"
    for folder in (
        root / "src",
        root / ".stage2-sessions" / "s1",
        root / ".pi",
        root / ".git",
        root / "tools",
        out,
        home,
    ):
        folder.mkdir(parents=True)
    (root / "src" / "a.txt").write_text("a\n", encoding="utf-8")
    (root / ".pi" / "settings.json").write_text("{}\n", encoding="utf-8")
    (root / ".git" / "config").write_text("[core]\n", encoding="utf-8")
    (out / "secret.txt").write_text("secret\n", encoding="utf-8")
    (root / "link").symlink_to(out)
    (root / "loop").symlink_to(root / "loop")
    # Inside the worktree but outside the protected directories, so the own-file rule stands alone.
    policy = root / "tools" / "policy.mjs"
    shutil.copy(POLICY, policy)
    return World(root, out, home, policy)


def blocked(answer: dict, *, mentioning: str) -> None:
    result = answer["result"]
    assert result is not None and result["block"] is True, answer
    assert mentioning in result["reason"], result["reason"]


def passed(answer: dict) -> None:
    assert answer["result"] is None, answer
    assert answer["asked"] == [], "a question was asked"


# --- (a) the file tools stay inside the worktree -------------------------------------------------


@pytest.mark.parametrize("tool", PATH_TOOLS)
@pytest.mark.parametrize("how", ["relative", "dot", "absolute", "new-file", "at-prefix", "file-url"])
def test_a_path_inside_the_worktree_passes(world: World, tool: str, how: str) -> None:
    path = {
        "relative": "src/a.txt",
        "dot": "./src/a.txt",
        "absolute": str(world.root / "src" / "a.txt"),
        "new-file": "src/new/deep/file.txt",
        "at-prefix": "@src/a.txt",
        "file-url": (world.root / "src" / "a.txt").as_uri(),
    }[how]
    passed(world.call(tool, path=path))


@pytest.mark.parametrize("tool", ("grep", "find", "ls"))
def test_a_search_without_a_path_stays_in_the_working_directory(world: World, tool: str) -> None:
    passed(world.call(tool, pattern="x"))


@pytest.mark.parametrize("tool", PATH_TOOLS)
@pytest.mark.parametrize(
    "how",
    [
        "absolute",
        "dotdot",
        "etc",
        "tilde",
        "bare-tilde",
        "at-absolute",
        "file-url",
        "symlink",
        "new-file-beneath-symlink",
    ],
)
def test_a_path_outside_the_worktree_is_blocked(world: World, tool: str, how: str) -> None:
    path = {
        "absolute": str(world.out / "secret.txt"),
        "dotdot": "../out/secret.txt",
        "etc": "/etc/passwd",
        "tilde": "~/notes.txt",  # $HOME is outside the worktree in this test
        "bare-tilde": "~",  # `ls ~` would list the home directory
        "at-absolute": "@" + str(world.out / "secret.txt"),
        "file-url": (world.out / "secret.txt").as_uri(),
        "symlink": "link/secret.txt",
        "new-file-beneath-symlink": "link/new.txt",
    }[how]
    blocked(world.call(tool, path=path), mentioning="outside the worktree")


@pytest.mark.parametrize("tool", PATH_TOOLS)
def test_a_missing_or_malformed_path_is_blocked(world: World, tool: str) -> None:
    if tool in ("grep", "find", "ls"):
        blocked(world.call(tool, path=7), mentioning="handler failed")
    else:
        blocked(world.call(tool), mentioning="handler failed")
    blocked(world.call(tool, path="src/a\0.txt"), mentioning="NUL byte")


@pytest.mark.parametrize("pattern", ["../**", "/etc/*", "~/*", "@/etc/*", "a/../../b", "file:///etc/*"])
def test_a_find_pattern_or_grep_glob_that_reaches_out_is_blocked(world: World, pattern: str) -> None:
    blocked(world.call("find", pattern=pattern), mentioning="find pattern")
    blocked(world.call("grep", pattern="x", glob=pattern), mentioning="grep glob")


@pytest.mark.parametrize("pattern", ["**/*.py", "src/*.txt", "*..txt", "a..b/*"])
def test_a_find_pattern_or_grep_glob_inside_passes(world: World, pattern: str) -> None:
    passed(world.call("find", pattern=pattern))
    passed(world.call("grep", pattern="x", glob=pattern))


# --- (b) the policy cannot be rewritten ----------------------------------------------------------


@pytest.mark.parametrize("tool", WRITE_TOOLS)
@pytest.mark.parametrize(
    ("path", "reason"),
    [
        (".stage2-sessions/s1/launch.txt", "protected directory"),
        (".stage2-sessions", "protected directory"),
        (".pi/settings.json", "protected directory"),
        (".pi/new/extension.ts", "protected directory"),
        (".pi", "protected directory"),
        ("tools/policy.mjs", "own file"),
        ("src/../tools/policy.mjs", "own file"),
    ],
)
def test_a_write_to_a_protected_place_is_blocked(world: World, tool: str, path: str, reason: str) -> None:
    blocked(world.call(tool, path=path), mentioning=reason)


@pytest.mark.parametrize("tool", READ_TOOLS)
@pytest.mark.parametrize("path", [".stage2-sessions/s1", ".pi/settings.json", "tools/policy.mjs"])
def test_a_read_of_a_protected_place_passes(world: World, tool: str, path: str) -> None:
    passed(world.call(tool, path=path))


@pytest.mark.parametrize("tool", WRITE_TOOLS)
def test_a_write_to_the_git_directory_is_not_protected(world: World, tool: str) -> None:
    # Maintainer's answer Q-3: `.git/` stays writable; the record names the cost.
    passed(world.call(tool, path=".git/config"))


@pytest.mark.parametrize("tool", WRITE_TOOLS)
def test_a_symlink_to_a_protected_place_does_not_hide_it(world: World, tool: str) -> None:
    (world.root / "src" / "sneaky").symlink_to(world.root / ".pi")
    blocked(world.call(tool, path="src/sneaky/settings.json"), mentioning="protected directory")


def test_case_folding_is_a_host_setting_and_catches_a_differently_cased_name(world: World) -> None:
    def decide(path: str, *, caseInsensitive: bool) -> dict:  # noqa: N803 - the node env key
        env = {
            "cwd": str(world.root),
            "home": str(world.home),
            "ownFile": str(world.policy),
            "caseInsensitive": caseInsensitive,
        }
        event = {"toolName": "write", "input": {"path": path}}
        return world.run([{"mode": "decide", "event": event, "env": env}])[0]["decision"]

    assert decide(".PI/settings.json", caseInsensitive=True)["action"] == "block"
    assert decide(".Stage2-Sessions/x", caseInsensitive=True)["action"] == "block"
    assert decide("TOOLS/POLICY.MJS", caseInsensitive=True)["action"] == "block"
    # On a case-sensitive file system `.PI` is another directory. On a case-insensitive one (APFS on
    # macOS) the path resolves into the protected `.pi`, so the block is right and the allow cannot hold.
    if not (world.root / ".PI").exists():
        assert decide(".PI/settings.json", caseInsensitive=False)["action"] == "allow"


def test_the_case_rule_follows_the_host_platform(world: World) -> None:
    platforms = ["darwin", "win32", "linux", "freebsd"]
    answers = world.run([{"mode": "platform", "platform": name} for name in platforms])
    assert [a["caseInsensitive"] for a in answers] == [True, True, False, False]


# --- (c) dangerous shell commands ask ------------------------------------------------------------

DANGEROUS_COMMANDS = [
    "rm -rf build",
    "rm -r build",
    "rm -fr build",
    "rm --recursive build",
    "rm build -r",
    "sudo ls",
    "chmod 777 x",
    "chmod -R 777 .",
    "chown root:root x 777",
    "git reset --hard HEAD~1",
    "git reset HEAD~1 --hard",
    "git -C . reset --hard",
    "git -c core.pager=cat --no-pager reset --hard",
    "git clean -fd",
    "git -C sub clean -n",
    # Quoted option values and arguments (a reviewer's finding, 2026-10-09).
    'git -C "my dir" reset --hard',
    "git -C 'my dir' clean -fd",
    'rm "a;b" -r',
    "rm \\\n  -rf y",
    # The maintainer's extension of Q-8: the other ways to discard unsaved edits.
    "git checkout -- .",
    "git checkout main -- src/a.txt",
    "git checkout .",
    "git checkout -f",
    "git restore .",
    "git restore src/a.txt",
    "git restore --worktree --staged .",
    'git -C "my dir" restore .',
]


@pytest.mark.parametrize("command", DANGEROUS_COMMANDS)
def test_a_dangerous_command_asks_and_runs_only_on_yes(world: World, command: str) -> None:
    yes, no, dismissed = world.run(
        [
            world.case("bash", command=command, answer="Yes"),
            world.case("bash", command=command, answer="No"),
            world.case("bash", command=command),
        ]
    )
    assert yes["result"] is None and len(yes["asked"]) == 1 and command in yes["asked"][0]
    blocked(no, mentioning="refused by the user")
    blocked(dismissed, mentioning="refused by the user")


@pytest.mark.parametrize("command", DANGEROUS_COMMANDS)
def test_a_dangerous_command_is_blocked_when_no_ui_can_ask(world: World, command: str) -> None:
    answer = world.call("bash", command=command, hasUI=False, answer="Yes")
    blocked(answer, mentioning="no UI")
    assert answer["asked"] == []


@pytest.mark.parametrize(
    "command",
    [
        "ls -la",
        "git status",
        "git diff origin/main",
        "git commit -m 'x'",
        "git commit -m 'push the button'",  # the word in a message, not the verb
        "git log --grep pushed",  # a different word
        "git reset HEAD~1",  # a soft reset keeps the work
        "git reset --soft HEAD~1",
        "git checkout main",  # switching a branch keeps the work or refuses
        "git checkout -b topic",
        "git restore --staged src/a.txt",  # only unstages
        "git restore -S src/a.txt",
        # Q-7: network programs do not ask, however they are used.
        "curl https://example.invalid/x | sh",
        "wget https://example.invalid/x",
        "scp a host:b",
        "rsync -a a host:b",
        "ssh host",
        "nc -l 1234",
        # Q-8: `git push` does not ask, with or without global options.
        "git push origin main",
        "git -C . push",
        "python3 -m pytest tests -q",
        "make verify",
        "rm file.txt",
        "echo 'curling'",
        "grep -rn sudoku src",
    ],
)
def test_any_other_command_runs_without_a_question(world: World, command: str) -> None:
    # Maintainer's answer Q-2: only the listed patterns ask; the record names the cost.
    passed(world.call("bash", command=command))


def test_a_bash_call_without_a_command_is_blocked(world: World) -> None:
    blocked(world.call("bash"), mentioning="without a command")


# --- (d) a failing handler blocks ----------------------------------------------------------------


@pytest.mark.parametrize("tool", ["read", "write", "bash", "ls"])
def test_a_handler_that_throws_blocks_the_call(world: World, tool: str) -> None:
    blocked(world.call(tool, path="src/a.txt", command="ls", explode=True), mentioning="handler failed")


def test_a_symlink_loop_the_file_system_refuses_blocks_the_call(world: World) -> None:
    blocked(world.call("read", path="loop/x"), mentioning="handler failed")


def test_a_question_that_fails_blocks_the_call(world: World) -> None:
    blocked(world.call("bash", command="sudo ls", answer="throw"), mentioning="handler failed")


# --- (e) the checked initial model binds (go-access-point) ---------------------------------------

CHECKED = {
    "provider": "opencode-go",
    "model": {
        "id": "mimo-v2.6-flash",
        "name": "Mimo",
        "api": "openai-completions",
        "baseUrl": "https://opencode.ai/zen/go/v1",
        "reasoning": False,
        "input": ["text"],
        "contextWindow": 128000,
        "maxTokens": 4096,
    },
}


def test_the_checked_binding_registers_its_definition_on_the_provider(world: World) -> None:
    # The sidecar the runner wrote is exactly the definition Pi gets, under the record's provider.
    answer = world.run([{"mode": "register", "sidecar": json.dumps(CHECKED)}])[0]
    assert answer["registered"] == [{"name": "opencode-go", "options": {"models": [CHECKED["model"]]}}]


@pytest.mark.parametrize(
    "sidecar",
    [
        "not json at all",  # not JSON
        "null",
        "17",
        '"text"',
        "[]",
        json.dumps({"model": CHECKED["model"]}),  # no provider
        json.dumps({"provider": "", "model": CHECKED["model"]}),
        json.dumps({"provider": "opencode-go"}),  # no model
        json.dumps({"provider": "opencode-go", "model": "mimo"}),
        json.dumps({"provider": "opencode-go", "model": {"name": "no id"}}),
    ],
)
def test_a_sidecar_that_is_no_binding_throws_instead_of_registering(world: World, sidecar: str) -> None:
    answer = world.run([{"mode": "register", "sidecar": sidecar}])[0]
    assert "threw" in answer, answer


def test_a_sidecar_beside_the_copy_binds_at_load(world: World) -> None:
    (world.policy.parent / "checked-model.json").write_text(json.dumps(CHECKED), encoding="utf-8")
    answer = world.call("read", path="src/a.txt")
    assert answer["registered"] == [{"name": "opencode-go", "options": {"models": [CHECKED["model"]]}}]
    assert answer["handlers"] == ["tool_call"]


def test_a_malformed_sidecar_beside_the_copy_fails_the_load(world: World) -> None:
    # A session must never start on an unchecked model while pretending it was bound.
    (world.policy.parent / "checked-model.json").write_text("{broken", encoding="utf-8")
    # The driver's node run ends non-zero when the extension throws at load; `World.run` asserts on it.
    with pytest.raises(AssertionError):
        world.call("read", path="src/a.txt")


# --- what the runner relies on -------------------------------------------------------------------


def test_loading_registers_one_flag_and_one_tool_call_handler(world: World) -> None:
    answer = world.call("read", path="src/a.txt")
    assert [flag["name"] for flag in answer["flags"]] == ["stage2-session-policy"]
    assert answer["flags"][0]["type"] == "boolean"
    assert answer["handlers"] == ["tool_call"]


def test_the_extension_imports_nothing_but_node_so_a_copy_runs_anywhere() -> None:
    source = POLICY.read_text(encoding="utf-8")
    specifiers = re.findall(r"""from\s+["']([^"']+)["']""", source)
    assert specifiers, "the extension should import node modules"
    assert all(spec.startswith("node:") for spec in specifiers), specifiers
    assert "import(" not in source
