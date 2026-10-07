"""The checked interactive session behind `stage2.py session` - and every boundary it refuses.

Every case runs the verb in-process against a temporary repository with a real
git worktree at `.claude/worktrees/demo`, and against three stand-ins: `codex`,
`opencode` and `osascript` record their call, print canned output and contact
nothing. The `osascript` stand-in can execute the command it was handed through
/bin/sh, so a test sees exactly what a Terminal would have run. No test opens a
window, starts a real CLI or reaches a model endpoint; the platform check is
stubbed, so the suite runs on a machine that has no Terminal at all.

Each test comes with its fault: the fault that must turn it red is planted one
variant at a time and named in the test.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402
import stage2_session  # noqa: E402

LEAK = "LEAKMARK-123456"
DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"
GO_BARE = "mimo-v2.6-flash"
GO_MODEL = f"opencode-go/{GO_BARE}"
TRUNCATION = "/var/folders/T/oc-truncation"
HANDOVER = "Hand over: continue the session work where the last one stopped.\n"

# A stand-in for all three programs: it records its call, may plant or delete
# files, may sleep, and - as osascript only, when told - runs the command it
# was handed through /bin/sh, the way a Terminal would.
LAUNCH_STAND_IN = """#!@PYTHON@
# stage2-session stand-in: records its call, prints canned output, contacts nothing.
import json
import os
import subprocess
import sys
import time
from pathlib import Path

here = Path(__file__).resolve().parent
name = Path(sys.argv[0]).name
scenario = json.loads((here / "scenario.json").read_text())
log = here / "calls.jsonl"
previous = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
steps = scenario.get(name, [])
index = sum(1 for call in previous if call["name"] == name)
step = steps[index] if index < len(steps) else {}
argv = sys.argv[1:]

for relative, text in step.get("plant", {}).items():
    path = Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
for relative in step.get("delete", []):
    Path(relative).unlink(missing_ok=True)
if step.get("sleep"):
    time.sleep(step["sleep"])

record = {"name": name, "argv": argv, "env": dict(os.environ), "cwd": os.getcwd()}
with log.open("a") as handle:
    handle.write(json.dumps(record) + "\\n")

if step.get("exec_command") and len(argv) >= 2:
    done = subprocess.run(["/bin/sh", "-c", argv[1]], capture_output=True, text=True)
    with log.open("a") as handle:
        handle.write(json.dumps({"name": "sh", "stdout": done.stdout, "returncode": done.returncode}) + "\\n")

sys.stdout.write(step.get("stdout", ""))
sys.stderr.write(step.get("stderr", ""))
raise SystemExit(step.get("exit", 0))
"""


def git(cwd: Path, *args: str) -> str:
    run = subprocess.run(
        [
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return run.stdout.strip()


@dataclass
class World:
    root: Path
    tree: Path
    bin: Path
    monkey: pytest.MonkeyPatch

    def script(self, **steps: object) -> None:
        (self.bin / "scenario.json").write_text(json.dumps(steps), encoding="utf-8")

    def calls(self, name: str | None = None) -> list[dict]:
        log = self.bin / "calls.jsonl"
        found = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        return [call for call in found if name is None or call["name"] == name]

    def run(
        self,
        *options: str,
        change: str = "demo",
        model: str | None = "gpt-6.1-sol",
        root: Path | None = None,
        cwd: Path | None = None,
    ) -> int:
        argv = ["session", change]
        if model is not None:
            argv += ["--model", model]
        argv += [*options, "--root", str(root or self.tree)]
        self.monkey.chdir(cwd or self.tree)
        return stage2.main(argv)

    @property
    def findings(self) -> Path:
        return self.tree / "plans" / "changes" / "demo" / "findings.md"

    @property
    def handover(self) -> Path:
        return self.tree / "plans" / "changes" / "demo" / "handover.md"

    def text(self) -> str:
        return self.findings.read_text(encoding="utf-8")

    def policies(self) -> list[Path]:
        base = self.tree / stage2_session.SESSION_ROOT
        return sorted(base.iterdir()) if base.is_dir() else []

    def config(self) -> dict:
        (policy,) = [p for p in self.policies() if p.is_dir()]
        file = policy / "opencode.policy.json"
        return json.loads(file.read_text(encoding="utf-8")) if file.exists() else {}

    def script_file(self) -> Path:
        (policy,) = [p for p in self.policies() if p.is_dir()]
        return policy / stage2_session.SCRIPT_NAME

    def command(self) -> str:
        (call,) = self.calls("osascript")
        assert len(call["argv"]) == 2, call["argv"]
        return call["argv"][1]

    def declare_go(self, **changes: object) -> None:
        """Declare an `opencode-go` endpoint in the worktree's copy - a fixture, not a production allow-list."""
        entry = {
            "name": "opencode-go",
            "betreiber": "OpenCode (Operator Anomaly Innovations, Inc.)",
            "residenz": "anbieter-erklaert",
            "abrechnung": "abonnement",
            "darf_sehen": ["framework"],
            "modelle": [GO_BARE],
        }
        entry.update(changes)
        path = self.tree / "model-endpoints.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["endpunkte"] = [e for e in data["endpunkte"] if e.get("name") != "opencode-go"]
        data["endpunkte"].append(entry)
        path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")

    def cli_argv(self, name: str = "codex") -> list[str]:
        """What a Terminal actually ran, as the stand-in recorded it."""
        (call,) = self.calls(name)
        return call["argv"]


def expected_prompt(world: World, handover_text: str) -> str:
    """The prompt the helper must assemble: handover text first, then the rules, the limits, the read request."""
    rules = (world.tree / "AGENTS.md").read_text(encoding="utf-8").rstrip()
    return "\n\n".join(
        [
            handover_text.rstrip(),
            "## Repository agent rules\n\n" + rules,
            stage2_session.LAUNCH_LIMITS,
            stage2.READ_REQUEST,
        ]
    )


def from_config(permission: dict) -> list[dict]:
    """OpenCode's `Permission.fromConfig`: a config map as ordered `{permission, pattern, action}` rules."""
    found = []
    for key, value in permission.items():
        if isinstance(value, str):
            found.append({"permission": key, "pattern": "*", "action": value})
        else:
            found += [{"permission": key, "pattern": pattern, "action": action} for pattern, action in value.items()]
    return found


def effective(
    model: str,
    *,
    appended: bool = False,
    after: tuple[dict, ...] = (),
    pinned: str | None = None,
    mode: str = "primary",
) -> str:
    """A canned `opencode --pure debug agent` answer in OpenCode 1.18.35's `Agent.Info` shape.

    The rules come in OpenCode's order: its defaults (a catch-all allow, and an outside-directory ask with
    the truncation directory allowed), the runner's policy at the global level, the same policy at the
    agent level, `after` (what another configuration added for the agent), and - when `appended` - the
    truncation allowance OpenCode appends unless that exact pattern is denied explicitly.
    """
    policy = stage2_session.policy_config(model)["permission"]
    if not appended:
        policy["external_directory"][TRUNCATION] = "deny"
    defaults = {
        "*": "allow",
        "doom_loop": "ask",
        "external_directory": {"*": "ask", TRUNCATION: "allow"},
        "question": "deny",
        "read": {"*": "allow", "*.env": "ask"},
    }
    rules = from_config(defaults) + from_config(policy) + from_config(policy) + list(after)
    if appended:
        rules.append({"permission": "external_directory", "pattern": TRUNCATION, "action": "allow"})
    provider, _, model_id = (pinned or model).partition("/")
    return json.dumps(
        {
            "name": stage2_session.AGENT,
            "mode": mode,
            "native": False,
            "permission": rules,
            "model": {"providerID": provider, "modelID": model_id},
            "options": {},
            "tools": {"bash": True, "read": True, "task": False},
        }
    )


def rule(permission: str, pattern: str, action: str) -> dict:
    return {"permission": permission, "pattern": pattern, "action": action}


@pytest.fixture
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    """A repository, its dedicated worktree, three stand-ins and an environment that belong to the test."""
    root = tmp_path / "repo"
    tree = root / ".claude" / "worktrees" / "demo"
    (root / "plans" / "changes" / "demo").mkdir(parents=True)
    (root / "plans" / "changes" / "demo" / "spec.md").write_text(
        "---\ntitle: Spec\nbead: demo-1\n---\n\n# Spec\n", encoding="utf-8"
    )
    (root / "AGENTS.md").write_text("# Agent rules\n\nStay inside the repository.\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("value = 1\n", encoding="utf-8")
    shutil.copy(REPO_ROOT / "model-endpoints.yaml", root / "model-endpoints.yaml")
    shutil.copytree(REPO_ROOT / "prompts", root / "prompts")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("codex", "opencode", "osascript"):
        program = bin_dir / name
        program.write_text(LAUNCH_STAND_IN.replace("@PYTHON@", sys.executable), encoding="utf-8")
        program.chmod(0o755)
    git_dir = tmp_path / "gitbin"
    git_dir.mkdir()
    (git_dir / "git").symlink_to(shutil.which("git"))
    (tmp_path / "denylist.txt").write_text(DENYLIST, encoding="utf-8")
    (tmp_path / "secrets.env").write_text("OTHER=1\n", encoding="utf-8")

    for name, value in {
        "PATH": f"{bin_dir}:{git_dir}",
        "HOME": str(tmp_path / "home"),
        "LEAKCHECK_DENYLIST": str(tmp_path / "denylist.txt"),
        "CC_SECRETS": str(tmp_path / "secrets.env"),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CEILING_DIRECTORIES": str(tmp_path),
        "GH_TOKEN": "caller-gh-token",
        "OPENAI_API_KEY": "caller-openai-key",
        "X_SECRET": "caller-secret",
        "ANTHROPIC_MODEL": "caller-model",
        "ANTHROPIC_BASE_URL": "http://caller.invalid",
    }.items():
        monkeypatch.setenv(name, value)

    git(root, "init", "--quiet", "--initial-branch=main")
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "base")
    git(root, "worktree", "add", "-b", "wt-demo", "--quiet", str(tree))
    (tree / "plans" / "changes" / "demo" / "handover.md").write_text(HANDOVER, encoding="utf-8")
    monkeypatch.setattr(stage2_session, "on_macos", lambda: True)
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"session read a secret: {name}"))
    w = World(root, tree, bin_dir, monkeypatch)
    w.script()
    return w


# ---------------------------------------------------------------------------
# Where a session runs (spec 1)
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("world")
def test_only_stand_ins_answer_the_session() -> None:
    found = []
    for entry in os.environ["PATH"].split(os.pathsep):
        for name in ("codex", "opencode", "osascript"):
            program = Path(entry) / name
            if program.is_file():
                found.append(name)
                assert "stage2-session stand-in" in program.read_text(encoding="utf-8"), f"{program} is no stand-in"
    assert sorted(found) == ["codex", "opencode", "osascript"]


def test_a_session_dispatches_from_the_dedicated_worktree(world: World) -> None:
    assert world.run() == 0
    assert world.calls("codex") == [], "the runner locates the CLI; Terminal, not the runner, starts it"
    assert world.command().startswith(f"cd {shlex.quote(str(world.tree))} ")


@pytest.mark.parametrize(
    ("where", "needle"),
    [
        ("main", "dedicated worktree"),
        ("wrong-cwd", "working directory"),
        ("subdir", "working directory"),
        ("detached", "attached branch"),
        ("other-platform", "macOS"),
    ],
)
def test_a_session_outside_its_boundaries_refuses_before_anything_starts(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], where: str, needle: str
) -> None:
    if where == "main":
        assert world.run(root=world.root, cwd=world.root) == 2
    elif where == "wrong-cwd":
        assert world.run(cwd=world.root) == 2
    elif where == "subdir":
        (world.tree / "src").mkdir(exist_ok=True)
        assert world.run(cwd=world.tree / "src") == 2
    elif where == "detached":
        git(world.tree, "checkout", "--quiet", "--detach")
        assert world.run() == 2
    else:
        monkeypatch.setattr(stage2_session, "on_macos", lambda: False)
        assert world.run() == 2
    assert needle in capsys.readouterr().err
    assert world.calls() == []
    assert not world.findings.exists() or "Stage-2 session" not in world.text()


def test_the_refusal_reason_reaches_the_caller(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    assert world.run(root=world.root, cwd=world.root) == 2
    assert "dedicated worktree" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# The declaration decides the transport (spec 2)
# ---------------------------------------------------------------------------


def test_a_plain_codex_model_selects_the_codex_transport(world: World) -> None:
    assert world.run() == 0
    assert "endpoint openai-codex" in world.text()
    assert "--sandbox workspace-write" in world.command()


def test_a_declared_go_model_selects_the_opencode_transport(world: World) -> None:
    world.declare_go()
    world.script(opencode=[{"stdout": effective(GO_MODEL)}])
    assert world.run(model=GO_MODEL) == 0
    assert "endpoint opencode-go" in world.text()
    assert f"--model {GO_MODEL}" in world.command()


@pytest.mark.parametrize(
    ("model", "prepare"),
    [
        ("never-declared-1", None),
        ("mimo-v2.6-flash", "go-declared"),
        (GO_MODEL, None),  # the production declaration names no opencode-go at all
        ("glm-5.3", None),  # declared - but for a transport no session drives
        ("gpt-6.1-sol extra", None),
    ],
    ids=["unknown", "plain-go-name", "go-undeclared", "other-transport", "whitespace"],
)
def test_a_model_no_declaration_clears_for_a_session_refuses(world: World, model: str, prepare: str | None) -> None:
    if prepare == "go-declared":
        world.declare_go()
    assert world.run(model=model) == 2
    assert world.calls() == [] and not world.findings.exists()


def test_the_id_form_decides_and_a_disallowing_declaration_refuses(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    world.declare_go(modelle=[GO_BARE, "gpt-6.1-sol"])
    assert world.run() == 0, "a plain id is Codex's even when opencode-go lists the same id"
    assert "endpoint openai-codex" in world.text()
    world.findings.unlink()
    world.script()
    (world.bin / "calls.jsonl").unlink(missing_ok=True)

    for model in ("opencode-go/", "opencode-go/a/b", GO_MODEL + "-other"):
        assert world.run(model=model) == 2, model
        assert world.calls() == []

    world.declare_go(modelle=[GO_MODEL])
    assert world.run(model=GO_MODEL) == 2, "the declaration lists bare ids; a listed full id selects nothing"
    assert "lists mimo-v2.6-flash" in capsys.readouterr().err
    assert world.calls() == []

    world.declare_go(darf_sehen=[])
    assert world.run(model=GO_MODEL) == 2, "an endpoint that may not see framework content is refused"
    assert world.calls() == []

    world.declare_go(residenz="nicht-erklaert")
    assert world.run(model=GO_MODEL) == 2, "an endpoint without a residency statement is refused"
    assert world.calls() == []


@pytest.mark.parametrize(
    "yaml_text",
    [
        ":::: not yaml\n",
        "schema_version: 1\n",
        "endpunkte: [{}]\n",
        "endpunkte: [{name: somewhere, modelle: not-a-list}]\n",
        "endpunkte: [{name: openai-codex, modelle: [gpt-6.1-sol]}, {name: openai-codex, modelle: []}]\n",
    ],
    ids=["unparsable", "no-endpoints", "unnamed-entry", "modelle-not-a-list", "duplicate-name"],
)
def test_a_malformed_declaration_refuses(world: World, yaml_text: str) -> None:
    (world.tree / "model-endpoints.yaml").write_text(yaml_text, encoding="utf-8")
    assert world.run() == 2
    assert world.calls() == [] and not world.findings.exists()


# ---------------------------------------------------------------------------
# The handover is the first prompt (spec 3, 4)
# ---------------------------------------------------------------------------


def test_the_handover_text_itself_becomes_the_first_prompt(world: World) -> None:
    world.script(osascript=[{"exec_command": True}])
    assert world.run() == 0
    prompt = world.cli_argv()[-1]
    assert prompt.startswith("Hand over: continue the session work"), "the text is sent, not the pathname"
    assert "Stay inside the repository." in prompt and stage2.READ_REQUEST in prompt
    assert "limits of this launch" in prompt and "other model again through the runner" in prompt


def test_an_explicit_handover_is_taken_over_the_default(world: World) -> None:
    other = world.tree / "docs" / "journal" / "handover"
    other.mkdir(parents=True)
    (other / "note.md").write_text("Explicit: resume from the takeover note.\n", encoding="utf-8")
    world.script(osascript=[{"exec_command": True}])
    assert world.run("--handover", "docs/journal/handover/note.md") == 0
    assert world.cli_argv()[-1].startswith("Explicit: resume from the takeover note.")
    assert "handover docs/journal/handover/note.md" in world.text()


def test_a_symlink_that_stays_inside_is_read(world: World) -> None:
    (world.tree / "link.md").symlink_to(world.handover)
    world.script(osascript=[{"exec_command": True}])
    assert world.run("--handover", "link.md") == 0
    assert world.cli_argv()[-1].startswith("Hand over:")


@pytest.mark.parametrize(
    ("fault", "needle"),
    [
        ("missing", "does not exist"),
        ("empty", "empty"),
        ("blank", "empty"),
        ("bad-utf8", "UTF-8"),
        ("nul", "NUL"),
        ("oversized", "at most"),
        ("directory", "not a regular file"),
        ("fifo", "not a regular file"),
    ],
)
def test_a_handover_that_cannot_be_sent_refuses(
    world: World, fault: str, needle: str, capsys: pytest.CaptureFixture[str]
) -> None:
    if fault == "missing":
        world.handover.unlink()
    elif fault == "empty":
        world.handover.write_text("", encoding="utf-8")
    elif fault == "blank":
        world.handover.write_text("  \n", encoding="utf-8")
    elif fault == "bad-utf8":
        world.handover.write_bytes(b"\xff\xfe broken")
    elif fault == "nul":
        world.handover.write_bytes(b"before\x00after")
    elif fault == "oversized":
        world.handover.write_text("a" * (32 * 1024 + 1), encoding="utf-8")
    elif fault == "directory":
        world.handover.unlink()
        world.handover.mkdir()
    else:
        world.handover.unlink()
        os.mkfifo(world.handover)
    assert world.run() == 2
    assert needle in capsys.readouterr().err
    assert world.calls() == [] and not world.findings.exists()


def test_a_handover_that_resolves_outside_the_worktree_refuses(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    (world.root / "outside-secret.txt").write_text("SECRET-OUTSIDE-1\n", encoding="utf-8")
    (world.tree / "escape.md").symlink_to(world.root / "outside-secret.txt")
    for handover in ("../AGENTS.md", "../../../etc/passwd", "escape.md", str(world.root / "outside-secret.txt")):
        assert world.run("--handover", handover) == 2, handover
        assert "outside the worktree" in capsys.readouterr().err, handover
        assert world.calls() == []
    assert world.policies() == [], "a refused handover leaves no policy directory behind"


# ---------------------------------------------------------------------------
# The leak check runs, twice (spec 5, 6)
# ---------------------------------------------------------------------------


def test_a_leak_in_the_handover_or_the_tree_refuses_before_any_dispatch(world: World) -> None:
    world.handover.write_text(f"the value {LEAK} must not travel\n", encoding="utf-8")
    assert world.run() == 2
    assert world.calls() == [] and not world.findings.exists()

    world.handover.write_text(HANDOVER, encoding="utf-8")
    (world.tree / "src" / "late.txt").write_text(LEAK, encoding="utf-8")
    assert world.run() == 2
    assert world.calls() == []


def test_the_second_scan_catches_what_arrived_after_the_first(world: World) -> None:
    world.declare_go()
    world.script(opencode=[{"stdout": effective(GO_MODEL), "plant": {"late-leak.txt": LEAK}}])
    assert world.run(model=GO_MODEL) == 2
    assert world.calls("osascript") == [], "the window opened on the first scan's verdict"
    assert world.policies() == [], "a refused launch cleans its policy directory"
    assert not world.findings.exists() or "dispatch pending" not in world.text()


def test_the_second_scan_rereads_the_denylist(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    world.declare_go()
    denylist = os.environ["LEAKCHECK_DENYLIST"]
    world.script(opencode=[{"stdout": effective(GO_MODEL), "delete": [denylist]}])
    assert world.run(model=GO_MODEL) == 2
    assert "denylist" in capsys.readouterr().out, "the rendered verdict names the missing denylist"
    assert world.calls("osascript") == [] and world.policies() == []


# ---------------------------------------------------------------------------
# The audit line (spec 7, 8)
# ---------------------------------------------------------------------------


def test_the_audit_names_the_attempt_and_keeps_prior_findings(world: World) -> None:
    world.findings.write_text("# Findings — demo\n\nEarlier rows stand.\n", encoding="utf-8")
    assert world.run() == 0
    matches = re.findall(
        r"^Stage-2 session, \d{4}-\d{2}-\d{2}: attempt ([0-9a-f]+) · model gpt-6\.1-sol · endpoint openai-codex · "
        r"handover plans/changes/demo/handover\.md · leak check clean over (\d+) files, (\d+) commits, "
        r"(\d+) rules · dispatch accepted\.$",
        world.text(),
        re.M,
    )
    assert len(matches) == 1
    attempt, files, commits, rules = matches[0]
    assert len(attempt) == 12 and int(files) >= 2 and int(commits) >= 1 and rules == "1"
    assert "Earlier rows stand." in world.text(), "the update replaces only its own line"
    assert "dispatch pending" not in world.text()


def test_two_attempts_leave_two_distinct_audit_lines(world: World) -> None:
    assert world.run() == 0 and world.run() == 0
    ids = re.findall(
        r"^Stage-2 session, \d{4}-\d{2}-\d{2}: attempt ([0-9a-f]+) .*dispatch accepted\.$", world.text(), re.M
    )
    assert len(ids) == 2 and len(set(ids)) == 2


def test_a_failed_terminal_dispatch_is_recorded_and_cleaned(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    world.script(osascript=[{"exit": 1, "stderr": "execution error: Terminal not allowed."}])
    (world.tree / stage2_session.SESSION_ROOT / "keep").mkdir(parents=True)
    (world.tree / stage2_session.SESSION_ROOT / "keep" / "user.txt").write_text("mine\n", encoding="utf-8")
    assert world.run() == 1
    assert "Terminal dispatch failed" in capsys.readouterr().err
    assert re.search(r"dispatch failed \(osascript exited 1: execution error[^)]*\)\.", world.text(), re.M)
    assert "dispatch pending" not in world.text()
    kept = world.tree / stage2_session.SESSION_ROOT / "keep" / "user.txt"
    assert kept.read_text(encoding="utf-8") == "mine\n", "the cleanup removes only what the run created"
    assert [p for p in world.policies() if p.name.startswith("codex-")] == []


def test_a_missing_cli_or_terminal_refuses_as_a_prerequisite(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    (world.bin / "codex").unlink()
    assert world.run() == 2
    assert "not on PATH" in capsys.readouterr().err and world.calls() == []

    (world.bin / "codex").write_text(LAUNCH_STAND_IN.replace("@PYTHON@", sys.executable), encoding="utf-8")
    (world.bin / "codex").chmod(0o755)
    (world.bin / "osascript").unlink()
    assert world.run() == 2
    assert "osascript" in capsys.readouterr().err and world.calls() == []


def test_a_terminal_that_never_answers_is_a_failed_dispatch(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(stage2_session, "OSASCRIPT_TIMEOUT", 1.0)
    world.script(osascript=[{"sleep": 5}])
    assert world.run() == 1
    assert "did not answer within" in capsys.readouterr().err
    assert "dispatch failed (osascript did not answer within" in world.text()
    assert world.policies() == []


def test_an_unwritable_audit_starts_no_session(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    world.findings.mkdir(parents=True)
    assert world.run() == 1
    assert "pending audit could not be written" in capsys.readouterr().err
    assert world.calls() == []


def test_a_failed_audit_update_leaves_the_pending_line(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    real_write = Path.write_text

    def picky(self: Path, data: str, *_args: object, **_kwargs: object) -> None:
        if "dispatch accepted" in data:
            raise OSError("the write refused")
        real_write(self, data)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "write_text", picky)
    assert world.run() == 1
    assert "could not be updated" in capsys.readouterr().err
    assert "dispatch pending" in world.text() and "dispatch accepted" not in world.text()
    assert len(world.calls("osascript")) == 1


def test_a_stamp_failure_after_the_update_is_reported(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls = {"n": 0}
    real = stage2.stamp_updated

    def flaky(path: Path) -> None:
        calls["n"] += 1
        if calls["n"] >= 2:
            raise OSError("no stamp today")
        real(path)

    monkeypatch.setattr(stage2, "stamp_updated", flaky)
    assert world.run() == 1
    assert "updated but not re-stamped" in capsys.readouterr().err
    assert "dispatch accepted" in world.text(), "the status was written before the stamp failed"


# ---------------------------------------------------------------------------
# What Terminal is told to run (spec 9, 10, 12)
# ---------------------------------------------------------------------------


def test_codex_is_dispatched_interactively_with_its_exact_safety_flags(world: World) -> None:
    world.script(osascript=[{"exec_command": True}])
    assert world.run() == 0
    argv = world.cli_argv()
    assert argv == [
        "--no-daemon",
        "--model",
        "gpt-6.1-sol",
        "--cd",
        str(world.tree),
        "--sandbox",
        "workspace-write",
        "--ask-for-approval",
        "on-request",
        expected_prompt(world, HANDOVER),
    ], argv
    assert world.calls("codex")[0]["cwd"] == str(world.tree)
    (sh_record,) = [call for call in world.calls() if call["name"] == "sh"]
    assert sh_record["returncode"] == 0
    words = shlex.split(world.command())
    assert words[:5] == ["cd", str(world.tree), "&&", "exec", "/usr/bin/env"], "env is absolute, not looked up"
    assert words.count(str(world.bin / "codex")) == 1, "the CLI is named once"
    assert words[words.index(str(world.bin / "codex")) + 1 :] == argv, "Terminal runs the CLI with exactly this argv"


def test_opencode_is_dispatched_interactively_with_the_checked_agent(world: World) -> None:
    world.declare_go()
    world.script(
        opencode=[{"stdout": effective(GO_MODEL)}, {"stdout": effective(GO_MODEL)}],
        osascript=[{"exec_command": True}],
    )
    assert world.run(model=GO_MODEL) == 0
    debug = [call for call in world.calls("opencode") if call["argv"][:2] == ["--pure", "debug"]]
    assert [call["argv"] for call in debug] == [
        ["--pure", "debug", "agent", stage2_session.AGENT],
    ], "the runner runs the diagnostics - once, bounded, without --tool or --params"
    for call in debug:
        assert "--tool" not in call["argv"] and "--params" not in call["argv"]
    launched = [call for call in world.calls("opencode") if call["argv"][:2] == ["--pure", str(world.tree)]]
    assert len(launched) == 1, "the launch is the only opencode call the Terminal shell runs"
    (interactive,) = launched
    assert interactive["argv"] == [
        "--pure",
        str(world.tree),
        "--model",
        GO_MODEL,
        "--agent",
        stage2_session.AGENT,
        "--prompt",
        expected_prompt(world, HANDOVER),
    ]
    assert interactive["env"]["OPENCODE_CONFIG"].startswith(str(world.tree / stage2_session.SESSION_ROOT))


def test_hostile_prompt_text_stays_data(world: World) -> None:
    hostile = "start\n'; touch PWNED-escape; echo '\n$(must-not-run)\n`also-not-this`\n\"quoted\""
    world.handover.write_text(hostile, encoding="utf-8")
    world.script(osascript=[{"exec_command": True}])
    assert world.run() == 0
    assert world.cli_argv()[-1] == expected_prompt(world, hostile), "the prompt travelled as one data argument"
    assert not (world.tree / "PWNED-escape").exists(), "an extra command ran in the launch stand-in"
    script = world.script_file().read_text(encoding="utf-8")
    assert script == stage2_session.APPLESCRIPT and "PWNED" not in script, "the prompt reached the AppleScript source"


# ---------------------------------------------------------------------------
# The OpenCode policy and what the effective agent says (spec 11)
# ---------------------------------------------------------------------------


def test_the_policy_repairs_the_truncation_allowance_once(world: World) -> None:
    world.declare_go()
    world.script(
        opencode=[
            {"stdout": effective(GO_MODEL, appended=True)},
            {"stdout": effective(GO_MODEL)},
            {},
        ],
        osascript=[{"exec_command": True}],
    )
    assert world.run(model=GO_MODEL) == 0
    assert len(world.calls("opencode")) == 3, "two diagnostics and one interactive launch"
    config = world.config()
    assert config["permission"]["external_directory"] == {"**": "deny", TRUNCATION: "deny"}
    assert config["agent"][stage2_session.AGENT]["permission"]["external_directory"] == {
        "**": "deny",
        TRUNCATION: "deny",
    }, "the agent level carries the explicit denial too"
    assert world.policies() != [], "an accepted launch keeps the policy for the session to load"


@pytest.mark.parametrize(
    ("second", "needle"),
    [
        (effective(GO_MODEL, appended=True), "keeps"),
        (effective(GO_MODEL, after=(rule("external_directory", "*", "allow"),)), "catch-all allow"),
        (effective(GO_MODEL, after=(rule("bash", "**", "allow"),)), "catch-all allow"),
        (effective(GO_MODEL, pinned="opencode-go/another-model"), "not the pinned"),
        (effective(GO_MODEL, after=(rule("task", "*", "ask"),)), "catch-all ask"),
        (effective(GO_MODEL, after=(rule("*", "*", "allow"),)), "catch-all allow"),
        (effective(GO_MODEL, after=(rule("external*", "/etc/*", "allow"),)), "after its catch-all"),
        (effective(GO_MODEL, after=(rule("bash", "rm *", "allow"),)), "after its catch-all"),
        (effective(GO_MODEL, mode="all"), "not as the primary agent"),
    ],
    ids=[
        "persistent-allowance",
        "outside-allow",
        "bash-allow",
        "model-switch",
        "task-ask",
        "wildcard-name-allow",
        "wildcard-name-specific",
        "bash-specific-allow",
        "not-primary",
    ],
)
def test_an_override_the_runner_did_not_write_refuses(
    world: World, second: str, needle: str, capsys: pytest.CaptureFixture[str]
) -> None:
    world.declare_go()
    world.script(
        opencode=[
            {"stdout": effective(GO_MODEL, appended=True)},
            {"stdout": second},
        ]
    )
    assert world.run(model=GO_MODEL) == 2
    assert needle in capsys.readouterr().err
    assert world.calls("osascript") == [] and world.policies() == []


@pytest.mark.parametrize(
    "step",
    [
        {"stdout": effective(GO_MODEL, after=(rule("external_directory", "**", "allow"),))},
        {"stdout": "not json"},
        {"exit": 3, "stderr": "no agent"},
        {"stdout": json.dumps({"name": "other-agent", "mode": "primary", "permission": []})},
        {
            "stdout": json.dumps(
                {
                    "name": stage2_session.AGENT,
                    "mode": "primary",
                    "model": {"providerID": "opencode-go", "modelID": GO_BARE},
                }
            )
        },
        {"stdout": json.dumps({**json.loads(effective(GO_MODEL)), "model": GO_MODEL})},
        {
            "stdout": json.dumps(
                {**json.loads(effective(GO_MODEL)), "permission": {"external_directory": {"**": "deny"}}}
            )
        },
        {"stdout": json.dumps({**json.loads(effective(GO_MODEL)), "permission": [{"permission": "bash"}]})},
        {"stdout": effective(GO_MODEL)[:-1] + ', "permission": []}'},
    ],
    ids=[
        "catch-all-allow",
        "not-json",
        "nonzero",
        "agent-missing",
        "no-permission-list",
        "model-as-string",
        "permission-as-map",
        "rule-without-fields",
        "empty-rule-list",
    ],
)
def test_an_unknown_effective_policy_refuses(world: World, step: dict) -> None:
    world.declare_go()
    world.script(opencode=[step])
    assert world.run(model=GO_MODEL) == 2
    assert world.calls("osascript") == [] and world.policies() == []


# ---------------------------------------------------------------------------
# Environment, launch files and cleanup (spec 13, 14)
# ---------------------------------------------------------------------------


def test_the_session_reads_no_secrets_and_sends_no_tokens(world: World) -> None:
    world.script(osascript=[{"exec_command": True}])
    assert world.run() == 0
    env = world.calls("codex")[0]["env"]
    for name in ("GH_TOKEN", "OPENAI_API_KEY", "X_SECRET"):
        assert name not in env
    assert not [name for name in env if name.startswith("ANTHROPIC_")], list(env)
    assert env["HOME"] == os.environ["HOME"] and "PATH" in env
    assert "caller-openai-key" not in json.dumps(world.config())


def test_launch_files_stay_inside_their_private_directory(world: World) -> None:
    base = world.tree / stage2_session.SESSION_ROOT
    (base / "existing").mkdir(parents=True)
    (base / "existing" / "user.txt").write_text("mine\n", encoding="utf-8")
    assert world.run() == 0
    (policy,) = [p for p in world.policies() if p.name.startswith("codex-")]
    assert {p.name for p in policy.iterdir()} == {stage2_session.SCRIPT_NAME}
    assert (base / "existing" / "user.txt").exists(), "an accepted launch keeps user files"
    strays = []
    for path in world.tree.rglob("*"):
        relative = path.relative_to(world.tree).as_posix()
        launched = "terminal-session" in path.name or "opencode.policy" in path.name
        if path.is_file() and launched and not relative.startswith(stage2_session.SESSION_ROOT):
            strays.append(relative)
    assert strays == []


@pytest.mark.parametrize("shape", ["file", "symlink"], ids=["base-is-a-file", "base-is-a-link"])
def test_a_runtime_root_that_is_not_a_real_directory_refuses(world: World, shape: str) -> None:
    base = world.tree / stage2_session.SESSION_ROOT
    if shape == "file":
        base.write_text("not a directory\n", encoding="utf-8")
    else:
        base.symlink_to(world.root / "elsewhere")
    assert world.run() == 2
    assert world.calls() == [] and world.policies() == []


# ---------------------------------------------------------------------------
# The parser (spec 1, 15)
# ---------------------------------------------------------------------------


def test_the_session_switches_belong_to_no_other_verb(world: World) -> None:
    assert world.run("--stage2-off", model=None) == 2
    assert world.run(model=None) == 2, "session needs its model"
    for verb in ("spec-review", "review", "release-loop"):
        assert stage2.main([verb, "demo", "--model", "gpt-6.1-sol", "--root", str(world.tree)]) == 2
    for verb in ("explore", "spec-review"):
        assert stage2.main([verb, "demo", "--handover", "x", "--root", str(world.tree)]) == 2
    assert stage2.main(["explore", "demo", "--stage2-off", "r", "--model", "m", "--root", str(world.tree)]) == 2
    assert world.calls() == []


# ---------------------------------------------------------------------------
# The doctrine (spec 15, 16)
# ---------------------------------------------------------------------------

WORKFLOW = REPO_ROOT / "docs" / "WORKFLOW.md"


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\n[> ]*", " ", text))


def section(text: str, title: str) -> str:
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(title)]
    if not starts:
        return ""
    level = len(title) - len(title.lstrip("#"))
    follow = re.compile(rf"^#{{1,{level}}} ")
    end = next((i for i in range(starts[0] + 1, len(lines)) if follow.match(lines[i])), len(lines))
    return "\n".join(lines[starts[0] : end])


def session_doc_problems(text: str) -> list[str]:
    one = flat(section(text, "### The interactive session"))
    found = []
    for phrase in (
        "scripts/stage2.py session <change> --model <id>",
        "runs twice in the same invocation",
        "covers this launch only",
        "not a confinement at the operating-system level",
        "another model goes through the runner again",
        "dispatch pending",
        "Accepted means Terminal took the command",
        "opencode-go/<model>",
        "approves no endpoint",
        "the review order is not this verb's business",
    ):
        if phrase not in one:
            found.append(f"the session docs lack: {phrase}")
    for claim in ("scans every later prompt", "confines the session to the worktree", "continuous scanning"):
        if claim in one:
            found.append(f"the session docs claim: {claim}")
    return found


def test_the_workflow_states_what_a_session_proves_and_what_it_does_not() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert session_doc_problems(text) == []
    for old, new in (
        ("covers this launch only", "covers the whole session continuously"),
        ("not a confinement at the operating-system level", "a confinement at the operating-system level"),
        ("another model goes through the runner again", "another model is picked in the window"),
        ("approves no endpoint", "approves the endpoint"),
    ):
        # Markdown wraps lines anywhere: the phrase is found, and replaced, across any whitespace.
        spaced = r"\s+".join(re.escape(word) for word in old.split())
        changed, count = re.subn(spaced, new, text, count=1)
        assert count == 1, old
        assert session_doc_problems(changed), old


def test_the_amendment_stays_a_draft_beside_the_change() -> None:
    draft = REPO_ROOT / "plans" / "changes" / "stage2-session" / "adr-0007-session-amendment.md"
    assert draft.is_file() and "Status: proposed" in draft.read_text(encoding="utf-8")
    assert [p.name for p in (REPO_ROOT / "docs" / "adr").glob("*session*")] == []
