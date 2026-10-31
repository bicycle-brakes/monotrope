"""The checked interactive session behind `stage2.py session` - and every boundary it refuses.

Every case runs the verb in-process against a temporary repository with a real
git worktree at `.claude/worktrees/demo`, and against five stand-ins: `codex`,
`pi`, `opencode`, `osascript` and the repository wrapper stand-in `pin-pi`
record their call, print canned output and contact nothing. The `pi` stand-in
sits on PATH, where the runner may never reach Pi; the wrapper stand-in is what
`runner.PI_WRAPPER` names. The `opencode` stand-in exists to prove it is never called. The `osascript` stand-in can execute the command it was handed through
/bin/sh, so a test sees exactly what a Terminal would have run. No test opens a
window, starts a real CLI or reaches a model endpoint; the platform check is
stubbed, so the suite runs on a machine that has no Terminal at all.

Each test comes with its fault: the fault that must turn it red is planted one
variant at a time and named in the test.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402
import stage2_session  # noqa: E402
from terms_fixtures import admissible_terms  # noqa: E402

LEAK = "LEAKMARK-123456"
DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"
GO_BARE = "mimo-v2.6-flash"
GO_MODEL = f"opencode-go/{GO_BARE}"
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
# The repository wrapper stand-in (`pin-pi`) answers and records as `pi`, so the
# scripted steps line up; the record's path is what says which program ran.
if name == "pin-pi":
    name = "pi"
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

record = {"name": name, "path": sys.argv[0], "argv": argv, "env": dict(os.environ), "cwd": os.getcwd()}
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
    # The binding confirmations the fixture records in place of running real Pi
    # (its base-holding is proven against the pinned install by test_pi_contract).
    bindings: list[dict] = field(default_factory=list)

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

    def extension(self) -> Path:
        (policy,) = [p for p in self.policies() if p.is_dir()]
        return policy / stage2_session.POLICY_FILE

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
        # A paid model needs a dated reading of its data terms to be admitted (ADR 0021, decision 5),
        # valid through a quoted expiry date (bead coding-harness-abra); the shared builder's
        # far-future expiry keeps every fixture from aging into a skip, and a boundary test sets
        # its own (tests/terms_fixtures.py).
        entry.setdefault("modelle_terms", {model: admissible_terms() for model in entry["modelle"]})
        # The synthetic Go address record (go-access-point): the runner binds the
        # initial model offline against it; no test reads the held real file.
        entry.setdefault(
            "adresse",
            {
                "host": "opencode.ai",
                "apis": {
                    "openai-completions": {
                        "basis": "https://opencode.ai/zen/go/v1",
                        "quelle": "the synthetic test record (go-access-point)",
                        "gelesen": "2026-10-31",
                    }
                },
            },
        )
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


# The three calls a Pi session makes, in order: the runner's version check, its read-back of the extension,
# and the launch the Terminal shell runs. The stand-in answers the n-th call of a program from its n-th step.
PI_VERSION_STEP = {"stdout": f"{stage2.PI_VERSION}\n"}
PI_HELP_STEP = {
    "stdout": "Usage: pi [options] [messages...]\n\nOptions:\n"
    f"  {stage2_session.POLICY_FLAG}  stage2 session policy: file tools bounded to the worktree\n"
}


def pi_steps(*launch: dict, version: dict | None = None, help_step: dict | None = None) -> list[dict]:
    return [version or PI_VERSION_STEP, help_step or PI_HELP_STEP, *launch]


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
    for name in ("codex", "pi", "opencode", "osascript", "pin-pi"):
        program = bin_dir / name
        program.write_text(LAUNCH_STAND_IN.replace("@PYTHON@", sys.executable), encoding="utf-8")
        program.chmod(0o755)
    # The pinned install's shipped catalog, as `checked_session_model` reads it
    # beside the wrapper: a runner-owned stand-in file, never a user directory.
    catalog_dir = bin_dir / "node_modules" / "@earendil-works" / "pi-ai" / "dist" / "providers" / "data"
    catalog_dir.mkdir(parents=True)
    (catalog_dir / "opencode-go.json").write_text(
        json.dumps(
            {
                "openai-completions": {
                    GO_BARE: {
                        "id": GO_BARE,
                        "name": GO_BARE,
                        "api": "openai-completions",
                        "reasoning": True,
                        "input": ["text"],
                        "cost": {"input": 0.14, "output": 0.28, "cacheRead": 0, "cacheWrite": 0},
                        "contextWindow": 128000,
                        "maxTokens": 4096,
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    # The runner's one path to Pi is patched to the wrapper stand-in; the `pi`
    # stand-in stays on PATH, where nothing may call it.
    monkeypatch.setattr(stage2, "PI_WRAPPER", bin_dir / "pin-pi")
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
    # The binding confirmation asks the real installed Pi in production; here it
    # is recorded, so the stand-in's scripted steps stay three per launch.
    monkeypatch.setattr(
        stage2_session,
        "confirm_binding",
        lambda root, cli, extension, bare, _runner: w.bindings.append(
            {"root": root, "cli": cli, "extension": extension, "bare": bare}
        ),
    )
    w.script()
    return w


# ---------------------------------------------------------------------------
# Where a session runs (spec 1)
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("world")
def test_only_stand_ins_answer_the_session() -> None:
    found = []
    for entry in os.environ["PATH"].split(os.pathsep):
        for name in ("codex", "pi", "opencode", "osascript"):
            program = Path(entry) / name
            if program.is_file():
                found.append(name)
                assert "stage2-session stand-in" in program.read_text(encoding="utf-8"), f"{program} is no stand-in"
    assert sorted(found) == ["codex", "opencode", "osascript", "pi"]


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


def test_a_link_that_aliases_the_main_checkout_refuses(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Phase 6, F-5: `.claude/worktrees/<change>` as a symlink to the main checkout is no dedicated worktree.
    (world.root / "plans" / "changes" / "alias").mkdir()
    (world.root / "plans" / "changes" / "alias" / "spec.md").write_text("---\nbead: demo-1\n---\n", encoding="utf-8")
    (world.root / "plans" / "changes" / "alias" / "handover.md").write_text(HANDOVER, encoding="utf-8")
    alias = world.root / ".claude" / "worktrees" / "alias"
    alias.symlink_to(world.root)
    assert world.run(change="alias", root=alias, cwd=alias) == 2
    assert "link" in capsys.readouterr().err
    assert world.calls() == []


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


def test_a_declared_go_model_selects_the_pi_transport(world: World) -> None:
    world.declare_go()
    world.script(pi=pi_steps())
    assert world.run(model=GO_MODEL) == 0
    assert "endpoint opencode-go" in world.text()
    assert f"--model {GO_MODEL}" in world.command()
    assert world.calls("opencode") == [], "the id names the endpoint; the OpenCode CLI is never called"


def test_an_expired_go_model_starts_no_interactive_session(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 5: an expired Go declaration refuses before any transport, terminal or audit line."""
    world.declare_go()
    path = world.tree / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["modelle_terms"][GO_BARE]["valid_until"] = "2026-10-30"
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 31))
    assert world.run(model=GO_MODEL) == 2
    assert world.calls() == [], "an expired model reached a CLI stand-in or the terminal"
    assert not world.findings.exists(), "the refusal wrote no audit line"
    assert "expired on 2026-10-30" in capsys.readouterr().err


def test_go_session_rechecks_terms_after_command_construction(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A final scan cannot authorize a terminal dispatch after UTC midnight."""
    world.declare_go()
    world.script(pi=pi_steps())
    path = world.tree / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["modelle_terms"][GO_BARE]["valid_until"] = "2026-10-31"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    day = dt.date(2026, 10, 31)
    monkeypatch.setattr(stage2, "terms_today", lambda: day)
    original = stage2_session.terminal_command

    def cross_midnight(*args, **kwargs):
        nonlocal day
        command = original(*args, **kwargs)
        day = dt.date(2026, 11, 1)
        return command

    monkeypatch.setattr(stage2_session, "terminal_command", cross_midnight)
    assert world.run(model=GO_MODEL) == 2
    assert not world.calls("osascript"), "expired terms reached the terminal"
    assert not world.findings.exists(), "the refusal fabricated a pending launch"
    assert "expired on 2026-10-31" in capsys.readouterr().err


@pytest.mark.parametrize(
    "changes",
    [{"darf_sehen": "not-framework"}, {"darf_sehen": "framework"}, {"residenz": ""}, {"residenz": "  "}],
    ids=["seen-as-substring", "seen-as-string", "empty-residency", "blank-residency"],
)
def test_a_malformed_permission_or_residency_refuses(world: World, changes: dict) -> None:
    # Phase 6, F-4: a string is no list of what an endpoint may see, and an empty residency states none.
    world.declare_go(**changes)
    world.script(pi=pi_steps(), osascript=[{}])
    assert world.run(model=GO_MODEL) == 2
    assert world.calls() == [] and not world.findings.exists()


@pytest.mark.parametrize(
    ("model", "prepare"),
    [
        ("never-declared-1", None),
        ("mimo-v2.6-flash", "go-declared"),
        ("opencode-go/never-listed-rung", None),  # the entry is declared now (stage2-mimo); no entry lists this rung
        ("glm-5.3", None),  # declared - but for a transport no session drives
        ("gpt-6.1-sol extra", None),
    ],
    ids=["unknown", "plain-go-name", "go-rung-undeclared", "other-transport", "whitespace"],
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


@pytest.mark.parametrize("value", ["", "  "], ids=["empty", "blank"])
def test_an_empty_handover_value_refuses_instead_of_taking_the_default(
    world: World, value: str, capsys: pytest.CaptureFixture[str]
) -> None:
    # Loop row L1-3: an unset shell variable must not silently start the default handover.
    assert world.run("--handover", value) == 2
    assert "names no file" in capsys.readouterr().err
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
    world.script(pi=pi_steps(help_step={**PI_HELP_STEP, "plant": {"late-leak.txt": LEAK}}))
    assert world.run(model=GO_MODEL) == 2
    assert world.calls("osascript") == [], "the window opened on the first scan's verdict"
    assert world.policies() == [], "a refused launch cleans its policy directory"
    assert not world.findings.exists() or "dispatch pending" not in world.text()


def test_the_second_scan_rereads_the_denylist(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    world.declare_go()
    denylist = os.environ["LEAKCHECK_DENYLIST"]
    world.script(pi=pi_steps(help_step={**PI_HELP_STEP, "delete": [denylist]}))
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


def test_an_update_that_fails_mid_write_keeps_the_record_whole(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Phase 6, F-6: the failure strikes after the target is truncated, as a full disk would.
    world.findings.write_text("# Findings — demo\n\nEarlier rows stand.\n", encoding="utf-8")
    real_write = Path.write_text

    def truncating(self: Path, data: str, *args: object, **kwargs: object) -> int:
        if "dispatch accepted" in data:
            with self.open("w", encoding="utf-8"):
                pass
            raise OSError("no space left on device")
        return real_write(self, data, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "write_text", truncating)
    assert world.run() == 1
    assert "could not be updated" in capsys.readouterr().err
    assert "Earlier rows stand." in world.text() and "dispatch pending." in world.text()
    assert [p.name for p in world.findings.parent.iterdir() if p.name.endswith(".tmp")] == []


def test_a_handover_named_like_the_status_keeps_its_source(world: World) -> None:
    # Phase 6, F-7: only the line's own ending is the dispatch status.
    (world.tree / "dispatch pending.md").write_text(HANDOVER, encoding="utf-8")
    assert world.run("--handover", "dispatch pending.md") == 0
    (line,) = [entry for entry in world.text().splitlines() if entry.startswith("Stage-2 session")]
    assert "handover dispatch pending.md ·" in line and line.endswith(" · dispatch accepted.")


def test_a_stamp_failure_after_the_update_is_reported(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls = {"n": 0}
    real = stage2.stamp_updated

    def flaky(path: Path) -> None:
        # The session's own re-stamp after its status update is the first call: `append` stamps the bytes it
        # writes in one atomic replacement, not through this function (deep review RS-2-6).
        calls["n"] += 1
        if calls["n"] >= 1:
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
        "--",
        expected_prompt(world, HANDOVER),
    ], argv
    assert world.calls("codex")[0]["cwd"] == str(world.tree)
    (sh_record,) = [call for call in world.calls() if call["name"] == "sh"]
    assert sh_record["returncode"] == 0
    words = shlex.split(world.command())
    assert words[:5] == ["cd", str(world.tree), "&&", "exec", "/usr/bin/env"], "env is absolute, not looked up"
    assert words.count(str(world.bin / "codex")) == 1, "the CLI is named once"
    assert words[words.index(str(world.bin / "codex")) + 1 :] == argv, "Terminal runs the CLI with exactly this argv"


def test_pi_is_dispatched_interactively_with_the_policy_extension(world: World) -> None:
    world.declare_go()
    world.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert world.run(model=GO_MODEL) == 0
    version, readback, launch = world.calls("pi")
    extension = world.extension()
    assert version["argv"] == ["--version"]
    assert readback["argv"] == [
        "--no-extensions",
        "-e",
        str(extension),
        "--offline",
        "--no-approve",
        "--help",
    ], "the read-back runs once, bounded, with only this extension and no model call"
    assert launch["argv"] == [
        "--no-extensions",
        "--no-mcp",
        "--no-skills",
        "--no-prompt-templates",
        "--no-themes",
        "-e",
        str(extension),
        "--offline",
        "--no-approve",
        "--model",
        GO_MODEL,
        "--",
        expected_prompt(world, HANDOVER),
    ], "discovery off, one extension, the declared model, then the prompt"
    for flag in ("--print", "-p", "--mode", "--pure"):
        assert flag not in launch["argv"], f"an interactive session never takes {flag}"
    assert launch["cwd"] == str(world.tree)
    assert extension.parent.parent == world.tree / stage2_session.SESSION_ROOT
    assert extension.read_bytes() == stage2_session.POLICY_SOURCE.read_bytes(), "the copy is the tested source"
    assert {p.name for p in extension.parent.iterdir()} == {stage2_session.SCRIPT_NAME, stage2_session.POLICY_FILE}
    assert world.calls("opencode") == [], "the OpenCode CLI is never called"


def test_all_session_pi_launches_use_repository_wrapper(world: World) -> None:
    """Criterion 5: version check, confirm-load and the Terminal command all name the repository wrapper; the PATH pi stays unused."""
    world.declare_go()
    world.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert world.run(model=GO_MODEL) == 0
    wrapper = str(world.bin / "pin-pi")
    version, readback, launch = world.calls("pi")
    assert version["path"] == wrapper, "the pin check resolved Pi from PATH"
    assert readback["path"] == wrapper, "the confirm-load bypassed the repository wrapper"
    assert launch["path"] == wrapper, "the Terminal dispatch bypassed the repository wrapper"
    assert wrapper in world.command(), "Terminal was not told the repository wrapper"
    # the fault: the PATH pi stand-in exists, and nothing called it
    assert (world.bin / "pi").is_file()
    assert not [call for call in world.calls("pi") if call["path"] == str(world.bin / "pi")]


def test_the_runners_own_pi_calls_read_nothing_of_the_maintainers(world: World) -> None:
    world.declare_go()
    world.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert world.run(model=GO_MODEL) == 0
    version, readback, launch = world.calls("pi")
    for call in (version, readback):
        scratch = call["env"]["HOME"]
        assert scratch != os.environ["HOME"], "a scratch home, not the maintainer's"
        assert call["env"]["PI_CODING_AGENT_DIR"] == scratch, "a scratch agent directory"
    assert launch["env"]["HOME"] == os.environ["HOME"], (
        "the session itself signs in from the maintainer's ~/.pi/agent (Q-6)"
    )
    assert "PI_CODING_AGENT_DIR" not in launch["env"], "the runner points Pi at no directory of its own"


@pytest.mark.parametrize(
    ("version", "needle"),
    [
        ({"stdout": f"{stage2.PI_VERSION}rc1\n"}, "not the pinned"),
        ({"stdout": ""}, "printed nothing"),
        ({"exit": 3}, "ended 3"),
    ],
    ids=["other-version", "silent", "fails"],
)
def test_a_pi_off_the_pin_refuses_before_anything_else(
    world: World, version: dict, needle: str, capsys: pytest.CaptureFixture[str]
) -> None:
    world.declare_go()
    world.script(pi=pi_steps(version=version))
    assert world.run(model=GO_MODEL) == 2
    assert needle in capsys.readouterr().err
    assert len(world.calls("pi")) == 1, "only the version check ran"
    assert world.calls("osascript") == [] and world.policies() == []


def test_a_handover_that_starts_with_an_at_sign_refuses_for_pi(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Pi reads a message that starts with `@` as a file name and sends that file's content instead.
    world.handover.write_text("@secret.txt\nResume here.\n", encoding="utf-8")
    world.declare_go()
    world.script(pi=pi_steps())
    assert world.run(model=GO_MODEL) == 2
    assert "starts with `@`" in capsys.readouterr().err
    assert world.calls("pi") == [] and world.calls("osascript") == [] and world.policies() == []


@pytest.mark.parametrize("transport", ["codex", "pi"])
def test_a_handover_that_starts_like_an_option_stays_the_prompt(world: World, transport: str) -> None:
    # Loop row L2-1: a journal handover starts with `---`; no CLI may read it as an option.
    text = "---\ntitle: a journal handover\n---\n\nResume here.\n"
    world.handover.write_text(text, encoding="utf-8")
    if transport == "codex":
        world.script(osascript=[{"exec_command": True}])
        assert world.run() == 0
        argv = world.cli_argv()
        assert argv[-2:] == ["--", expected_prompt(world, text)], "options end before the prompt"
    else:
        world.declare_go()
        world.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
        assert world.run(model=GO_MODEL) == 0
        argv = world.calls("pi")[-1]["argv"]
        assert argv[-2:] == ["--", expected_prompt(world, text)], "options end before the prompt"


def test_hostile_prompt_text_stays_data(world: World) -> None:
    hostile = "start\n'; touch PWNED-escape; echo '\n$(must-not-run)\n`also-not-this`\n\"quoted\""
    world.handover.write_text(hostile, encoding="utf-8")
    world.script(osascript=[{"exec_command": True}])
    assert world.run() == 0
    assert world.cli_argv()[-1] == expected_prompt(world, hostile), "the prompt travelled as one data argument"
    assert not (world.tree / "PWNED-escape").exists(), "an extra command ran in the launch stand-in"
    script = world.script_file().read_text(encoding="utf-8")
    assert script == stage2_session.APPLESCRIPT and "PWNED" not in script, "the prompt reached the AppleScript source"


# The Pi policy extension: copied in, confirmed loaded (spec 11)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("step", "needle"),
    [
        ({"stdout": "Usage: pi [options]\n"}, "did not load"),
        ({"stdout": "  --stage2-session-policy-other  another flag\n"}, "did not load"),
        ({"stdout": "  --x-stage2-session-policy  another flag\n"}, "did not load"),
        ({**PI_HELP_STEP, "exit": 2}, "exited 2"),
        ({"stdout": "", "exit": 1, "stderr": "no such extension"}, "exited 1"),
    ],
    ids=["flag-missing", "longer-flag", "prefixed-flag", "help-fails", "help-fails-silently"],
)
def test_an_extension_that_did_not_load_refuses_and_cleans_up(
    world: World, step: dict, needle: str, capsys: pytest.CaptureFixture[str]
) -> None:
    world.declare_go()
    world.script(pi=pi_steps(help_step=step))
    assert world.run(model=GO_MODEL) == 2
    assert needle in capsys.readouterr().err
    assert world.calls("osascript") == [], "no window opens on an unconfirmed policy"
    assert world.policies() == [], "a refused launch removes the private directory it made"


def test_a_pi_that_hangs_on_the_read_back_refuses(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(stage2_session, "CLI_TIMEOUT", 0.5)
    world.declare_go()
    world.script(pi=pi_steps(help_step={**PI_HELP_STEP, "sleep": 5}))
    assert world.run(model=GO_MODEL) == 2
    assert "did not answer within" in capsys.readouterr().err
    assert world.calls("osascript") == [] and world.policies() == []


def test_a_missing_extension_source_refuses_and_cleans_up(
    world: World, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(stage2_session, "POLICY_SOURCE", tmp_path / "nowhere.mjs")
    world.declare_go()
    world.script(pi=pi_steps())
    assert world.run(model=GO_MODEL) == 2
    assert "could not be copied" in capsys.readouterr().err
    assert len(world.calls("pi")) == 1, "the read-back is never asked about a file that is not there"
    assert world.calls("osascript") == [] and world.policies() == []


@pytest.mark.parametrize(
    "failure", [OSError("temp directory not writable"), KeyboardInterrupt()], ids=["oserror", "ctrl-c"]
)
def test_any_failure_before_the_dispatch_removes_the_private_directory(
    world: World, monkeypatch: pytest.MonkeyPatch, failure: BaseException
) -> None:
    def broken(*_args: object, **_kwargs: object) -> None:
        raise failure

    monkeypatch.setattr(stage2_session, "confirm_loaded", broken)
    world.declare_go()
    world.script(pi=pi_steps())
    with pytest.raises(type(failure)):
        world.run(model=GO_MODEL)
    assert world.calls("osascript") == [] and world.policies() == []


def test_the_session_keeps_discovery_off_except_context_files(world: World) -> None:
    world.declare_go()
    world.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert world.run(model=GO_MODEL) == 0
    argv = world.calls("pi")[-1]["argv"]
    for flag in ("--no-mcp", "--no-skills", "--no-prompt-templates", "--no-themes"):
        assert flag in argv, f"the session takes {flag}"
    assert "--no-context-files" not in argv, "AGENTS.md stays on on purpose"


def test_the_extension_is_confirmed_again_for_every_launch(world: World) -> None:
    world.declare_go()
    # Terminal is a stand-in that starts nothing here, so each launch makes the two calls of the runner only.
    world.script(pi=[PI_VERSION_STEP, PI_HELP_STEP, PI_VERSION_STEP, PI_HELP_STEP], osascript=[{}, {}])
    assert world.run(model=GO_MODEL) == 0
    assert world.run(model=GO_MODEL) == 0
    readbacks = [call for call in world.calls("pi") if "--help" in call["argv"]]
    assert len(readbacks) == 2 and readbacks[0]["argv"][2] != readbacks[1]["argv"][2], "each launch has its own copy"


# ---------------------------------------------------------------------------
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


def test_the_pi_session_hands_over_no_key_and_writes_no_credential(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENCODE_API_KEY", "caller-opencode-key")
    monkeypatch.setenv("PI_CODING_AGENT_DIR", "/caller/agent")
    world.declare_go()
    world.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert world.run(model=GO_MODEL) == 0
    for call in world.calls("pi"):
        for name in ("OPENCODE_API_KEY", "GH_TOKEN", "OPENAI_API_KEY", "X_SECRET"):
            assert name not in call["env"], f"{name} reached Pi"
        assert "caller-opencode-key" not in json.dumps(call)
    assert "PI_CODING_AGENT_DIR" not in world.calls("pi")[-1]["env"]
    for file in world.extension().parent.iterdir():
        assert "caller-" not in file.read_text(encoding="utf-8"), f"{file.name} holds a caller secret"


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
        launched = "terminal-session" in path.name or stage2_session.POLICY_FILE in path.name
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
        "~/.pi/agent",
        "may hold other providers' credentials",
        "outside the dangerous patterns",
        "no call to the OpenCode CLI",
    ):
        if phrase not in one:
            found.append(f"the session docs lack: {phrase}")
    for claim in (
        "scans every later prompt",
        "confines the session to the worktree",
        "continuous scanning",
        "dispatches OpenCode",
        "OpenCode gets a runner-supplied policy",
    ):
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
        ("may hold other providers' credentials", "holds only this endpoint's credential"),
        ("outside the dangerous patterns", "inside the confined set"),
        ("no call to the OpenCode CLI", "a call to the OpenCode CLI"),
    ):
        # Markdown wraps lines anywhere: the phrase is found, and replaced, across any whitespace.
        spaced = r"\s+".join(re.escape(word) for word in old.split())
        changed, count = re.subn(spaced, new, text, count=1)
        assert count == 1, old
        assert session_doc_problems(changed), old


def test_the_amendment_moved_into_the_decision_record() -> None:
    adr = REPO_ROOT / "docs" / "adr" / "0012-interactive-stage-2-sessions-run-through-the-checked-runner.md"
    head = adr.read_text(encoding="utf-8").split("\n---\n", 1)[0]
    assert re.search(r"^status: accepted$", head, re.M) and re.search(r"^provenance: human-decided$", head, re.M)
    draft = REPO_ROOT / "plans" / "changes" / "stage2-session" / "adr-0007-session-amendment.md"
    assert re.search(r"^Status: moved .*ADR 0012", draft.read_text(encoding="utf-8"), re.M | re.S)
