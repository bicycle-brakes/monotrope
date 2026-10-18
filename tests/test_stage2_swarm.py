"""The phase-1 research swarm and its boundary - routing, packets, pairs, judge and limits.

`scripts/stage2_swarm.py` runs only through the explore verb of the runner when
the change's class is `feature` or `architectural`. Every case here runs that
verb in-process against a temporary repository and two stand-ins: programs
named `pin-pi` and `claude` that record their arguments, environment and prompt,
print canned output and contact nothing. No test starts a real Pi, a real
Claude Code against a model endpoint, or reads the maintainer's real denylist
or secrets.

Each test comes with its fault: the planted mutation is named in the comment
and turned the test red before it was kept. The doctrine test at the end reads
the repository's own declaration and documents.
"""

from __future__ import annotations

import datetime
import json
import re
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
import stage2_availability  # noqa: E402
import stage2_swarm  # noqa: E402

GIT = shutil.which("git")  # resolved before any test narrows the PATH

# The planted OpenCode Go key, the credential every swarm Pi call rides on; the
# planted GLM key only the single-explorer route of a small class reads.
OKEY = "ok-7Rt2Wm9xQb4Nv6Lc"
GKEY = "sk" + "-zq7Hk2mVw9Xr4Tn8Lb3Pd6Jc1Fy5Ga0"  # split so the leak check sees no key literal
LEAK = "LEAKMARK-123456"
DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"

TOPIC_OK = "container isolation for AI agent runs"
PUBLIC_REPORT = "Public practice: [the pattern](https://example.com/pattern) matches this change's problem."
RECEIPT = {
    "kind": "fetch",
    "url": "https://example.com/pattern",
    "final_url": "https://example.com/pattern",
    "status": 200,
    "title": "The pattern",
    "retrieved": "2026-10-15",
    "excerpt": "public practice text",
    "bytes": 20,
}


def pi_table(rows: list[tuple[str, str]]) -> list[str]:
    """`pi --list-models` as Pi 1.1.0 prints it (`dist/cli/list-models.js`): a padded table, provider first."""
    header = ("provider", "model", "context", "max-out", "thinking", "images")
    cells = [header] + [(provider, model, "256K", "128K", "yes", "no") for provider, model in sorted(rows)]
    widths = [max(len(row[n]) for row in cells) for n in range(6)]
    return ["  ".join(cell.ljust(width) for cell, width in zip(row, widths, strict=True)) for row in cells]


# The test inventory: the roster on the free provider beside rows the pinned
# Pi also lists for the same credential - the paid Go provider's ids, one of
# them a free id's namesake. The Flash endpoint's provider never carries a free call.
PI_MODELS = pi_table(
    [
        ("opencode", "longcat-2.5-preview-free"),
        ("opencode", "space-bunny-free"),
        ("opencode", "big-pickle"),
        ("opencode-go", "longcat-2.5-preview-free"),
        ("opencode-go", "deepseek-v4.1-flash"),
        ("opencode-go", "mimo-v2.6-flash"),
    ]
)
FREE_IDS = ("longcat-2.5-preview-free", "space-bunny-free", "big-pickle")

SEED = "---\ntitle: Research\nupdated: 2026-10-15\nbead: demo-1\nclass: feature\n---\n\n# Research\n\nseed fact\n"


def judge_ok() -> str:
    """A judge answer the runner must accept: six sections, six labelled fields, one tracked citation."""
    sections = []
    for number in range(1, 7):
        sections.append(
            f"### Topic {number}\n\n"
            f"**Supported facts:** topic {number} holds at `src/app.py::value`.\n\n"
            "**Practice comparison:**\n\n"
            "**Architecture comparison:**\n\n"
            "**Adjacent-spec comparison:**\n\n"
            "**Disagreement:**\n\n"
            "**Gaps:**\n\n"
            "**Human questions:**\n"
        )
    return "\n".join(sections)


# A stand-in: the standard library only. The `kind` of a call decides which
# scenario list serves it, so a test addresses the topic author, the free
# researchers, the Flash pair and the judge separately.
STAND_IN = """#!@PYTHON@
# stage2-swarm-stand-in: records its call, prints canned output, contacts nothing.
import json
import os
import sys
import time
from pathlib import Path

here = Path(__file__).resolve().parent
name = Path(sys.argv[0]).name
program_path = sys.argv[0]
if name == "pin-pi":
    name = "pi"
scenario = json.loads((here / "scenario.json").read_text())
log = here / "calls.jsonl"
previous = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
argv = sys.argv[1:]
if name == "pi" and argv == ["--version"]:
    # Infrastructure has a separate path log; no model call is counted.
    with (here / "infrastructure.jsonl").open("a") as handle:
        handle.write(json.dumps({"path": program_path, "argv": argv}) + "\\n")
    sys.stdout.write(scenario.get("pi_version", "@PI@") + "\\n")
    raise SystemExit(0)
if name == "pi" and argv == ["--list-models"]:
    # Infrastructure has a separate path log; no model call is counted.
    with (here / "infrastructure.jsonl").open("a") as handle:
        handle.write(json.dumps({"path": program_path, "argv": argv}) + "\\n")
    for line in scenario.get("pi_models", []):
        sys.stdout.write(line + "\\n")
    raise SystemExit(scenario.get("pi_models_exit", 0))


def option(flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


prompt_file = option("--append-system-prompt-file") or option("--append-system-prompt")
prompt = Path(prompt_file).read_text() if prompt_file else ""
agent = os.environ.get("PI_CODING_AGENT_DIR")
if name == "claude":
    if "one-sentence public topic" in prompt:
        kind = "topic"
    elif "# The six pairs" in prompt:
        kind = "judge"
    else:
        kind = "work"
elif "STAGE2_PUBLIC_RECEIPTS" in os.environ:
    kind = "public"
else:
    kind = "flash"
steps = scenario.get(kind, [])
index = sum(1 for call in previous if call.get("kind") == kind)
step = steps[index] if index < len(steps) else {}
record = {
    "name": name,
    "program_path": program_path,
    "kind": kind,
    "argv": argv,
    "env": dict(os.environ),
    "cwd": os.getcwd(),
    "stdin": os.read(0, 100).decode(),
    "prompt": prompt,
    "prompt_path": str(prompt_file) if prompt_file else None,
    "agent_dir": agent,
    "agent_listing": sorted(os.listdir(agent)) if agent and os.path.isdir(agent) else None,
    "agent_settings": (Path(agent) / "settings.json").read_text()
    if agent and (Path(agent) / "settings.json").is_file()
    else None,
    "home_listing": sorted(os.listdir(os.environ.get("HOME", "")))
    if os.path.isdir(os.environ.get("HOME", ""))
    else None,
}
with log.open("a") as handle:
    handle.write(json.dumps(record) + "\\n")
key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("OPENCODE_API_KEY", "")
receipts = os.environ.get("STAGE2_PUBLIC_RECEIPTS")
if receipts and step.get("receipts"):
    with Path(receipts).open("a") as handle:
        for line in step["receipts"]:
            handle.write(json.dumps(line).replace("@KEY@", key) + "\\n")
for relative, text in step.get("plant", {}).items():
    Path(relative).parent.mkdir(parents=True, exist_ok=True)
    Path(relative).write_text(text.replace("@KEY@", key))
for relative, text in step.get("append", {}).items():
    with Path(relative).open("a") as handle:
        handle.write(text.replace("@KEY@", key))
sys.stdout.write(step.get("stdout", "").replace("@KEY@", key))
sys.stderr.write(step.get("stderr", "").replace("@KEY@", key))
sys.stdout.flush()
sys.stderr.flush()
time.sleep(step.get("sleep", 0))
raise SystemExit(step.get("exit", 0))
"""


@dataclass
class SwarmWorld:
    """A repository, two stand-ins and an environment that belong to one swarm test."""

    root: Path
    bin: Path

    @property
    def research(self) -> Path:
        return self.root / "plans" / "changes" / "demo" / "research.md"

    def script(self, **steps: object) -> None:
        (self.bin / "scenario.json").write_text(json.dumps(steps), encoding="utf-8")

    def calls(self, kind: str | None = None) -> list[dict]:
        log = self.bin / "calls.jsonl"
        found = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        return [call for call in found if kind is None or call["kind"] == kind]

    def run(self, *options: str) -> int:
        return stage2.main(["explore", "demo", *options, "--root", str(self.root)])

    def research_class(self, klass: str | None) -> None:
        text = self.research.read_text(encoding="utf-8")
        text = re.sub(r"^class: .*\n", "", text, count=1, flags=re.M)
        if klass is not None:
            text = re.sub(r"^(bead: .*)$", rf"\1\nclass: {klass}", text, count=1, flags=re.M)
        self.research.write_text(text, encoding="utf-8")

    def rewind(self) -> None:
        """A fresh run on a fresh record: the calls go, the research returns to its seed bytes."""
        log = self.bin / "calls.jsonl"
        if log.exists():
            log.unlink()
        self.research.write_text(SEED, encoding="utf-8")

    def complete(self, **overrides: object) -> None:
        """The scenario of a run in which every scheduled role succeeds; overrides win, other keys survive."""
        steps: dict[str, object] = {
            "topic": [{"stdout": TOPIC_OK}],
            "public": [{"stdout": PUBLIC_REPORT, "receipts": [RECEIPT]}] * 3,
            "flash": [{"stdout": f"FLASH-{n} on `src/app.py::value`"} for n in range(11)],
            "judge": [{"stdout": judge_ok()}],
        }
        scenario: dict[str, object] = json.loads((self.bin / "scenario.json").read_text(encoding="utf-8"))
        scenario.setdefault("pi_models", list(PI_MODELS))
        scenario.update(steps)
        scenario.update(overrides)
        # One step per call: a bare object stands for the first call of its kind.
        scenario = {key: [value] if isinstance(value, dict) else value for key, value in scenario.items()}
        self.script(**scenario)


@pytest.fixture
def sworld(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SwarmWorld:
    """A repository whose class states `feature`, the real declaration, and stand-ins for pi and claude."""
    root = tmp_path / "repo"
    folder = root / "plans" / "changes" / "demo"
    folder.mkdir(parents=True)
    (folder / "research.md").write_text(SEED, encoding="utf-8")
    (folder / "spec.md").write_text("---\ntitle: Spec\nbead: demo-1\n---\n\n# Spec\n", encoding="utf-8")
    (folder / "plan.md").write_text("---\ntitle: Plan\nbead: demo-1\n---\n\n# Plan\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agent rules\n\nStay inside the repository.\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("value = 1\n", encoding="utf-8")
    shutil.copytree(REPO_ROOT / "prompts", root / "prompts")
    shutil.copy(REPO_ROOT / "model-endpoints.yaml", root / "model-endpoints.yaml")

    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("claude", "pin-pi"):
        program = bin_dir / name
        program.write_text(
            STAND_IN.replace("@PYTHON@", sys.executable).replace("@PI@", stage2.PI_VERSION), encoding="utf-8"
        )
        program.chmod(0o755)
    # A bare executable is a trap: every production launch must use the pin.
    bare_pi = bin_dir / "pi"
    bare_pi.write_text(
        f"#!{sys.executable}\nraise SystemExit('bare pi bypassed the pinned wrapper')\n",
        encoding="utf-8",
    )
    bare_pi.chmod(0o755)
    monkeypatch.setattr(stage2, "PI_WRAPPER", bin_dir / "pin-pi")
    git_dir = tmp_path / "gitbin"
    git_dir.mkdir()
    (git_dir / "git").symlink_to(GIT)
    (tmp_path / "denylist.txt").write_text(DENYLIST, encoding="utf-8")
    (tmp_path / "secrets.env").write_text(
        f"# keys\nexport GLM_KEY='{GKEY}'\nexport OPENCODE_GO_KEY='{OKEY}'\n", encoding="utf-8"
    )
    for name, value in {
        "PATH": f"{bin_dir}:{git_dir}",
        "HOME": str(home),
        "CC_SECRETS": str(tmp_path / "secrets.env"),
        "LEAKCHECK_DENYLIST": str(tmp_path / "denylist.txt"),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CEILING_DIRECTORIES": str(tmp_path),
    }.items():
        monkeypatch.setenv(name, value)

    subprocess.run(["git", "init", "--quiet", "--initial-branch=main"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--quiet",
            "-m",
            "base",
        ],
        cwd=root,
        check=True,
        capture_output=True,
    )
    # Until the run consumes its frozen seat selection (plan steps 2-8), the old run needs no receipt: the
    # receipt's own contract is tested in test_stage2_research_availability.py.
    monkeypatch.setattr(stage2_availability, "consume_research", lambda *_args, **_kwargs: {"seats": {}})
    w = SwarmWorld(root, bin_dir)
    w.script()
    return w


def model_of(call: dict) -> str:
    return call["argv"][call["argv"].index("--model") + 1]


def status_line(text: str) -> str:
    found = re.search(r"^run swarm-[0-9a-f]{8} status: .*$", text, re.M)
    assert found, text[-2000:]
    return found.group(0)


# ---------------------------------------------------------------------------
# Routing (spec, criteria 1-4)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("klass", ["feature", "architectural"])
def test_large_classes_dispatch_the_swarm(sworld: SwarmWorld, klass: str) -> None:
    # Criterion 1. Planted fault: either class still runs the single GLM explorer.
    sworld.research_class(klass)
    sworld.complete()
    assert sworld.run() == 0
    assert [call["kind"] for call in sworld.calls()] == (["topic"] + ["public"] * 3 + ["flash"] * 11 + ["judge"])
    for call in sworld.calls("claude"):
        assert "glm-5.3-flash" not in call["argv"], "a large change never rides the single explorer"
        assert call["env"].get("ANTHROPIC_BASE_URL") != stage2.GLM_BASE_URL
    text = sworld.research.read_text(encoding="utf-8")
    assert "## Research swarm" in text and "seed fact" in text
    assert "## Runner exploration" not in text


def test_all_swarm_pi_launches_use_pinned_wrapper(sworld: SwarmWorld) -> None:
    """The bare-Pi trap refutes any catalog, public or repository escape."""
    sworld.complete()
    assert sworld.run() == 0
    pinned = str(sworld.bin / "pin-pi")
    infrastructure = [json.loads(line) for line in (sworld.bin / "infrastructure.jsonl").read_text().splitlines()]
    assert {tuple(call["argv"]) for call in infrastructure} == {
        ("--version",),
        ("--list-models",),
    }
    assert all(call["path"] == pinned for call in infrastructure)
    calls = [call for call in sworld.calls() if call["name"] == "pi"]
    assert {call["kind"] for call in calls} == {"public", "flash"}
    assert all(call["program_path"] == pinned for call in calls)


@pytest.mark.parametrize("klass", ["bounded", "spike"])
def test_small_classes_keep_the_single_explorer(sworld: SwarmWorld, klass: str) -> None:
    # Criterion 2. Planted fault: a small change starts a free researcher or the swarm judge.
    sworld.research_class(klass)
    sworld.script(
        work=[{"stdout": "A fact from `src/app.py::value`."}],
        topic=[{"stdout": "must not run"}],
        public=[{"stdout": "must not run"}],
        flash=[{"stdout": "must not run"}],
        judge=[{"stdout": "must not run"}],
    )
    assert sworld.run() == 0
    assert [call["kind"] for call in sworld.calls()] == ["work"]
    explorer = sworld.calls()[0]
    assert model_of(explorer) == "glm-5.3-flash"
    assert explorer["env"]["ANTHROPIC_BASE_URL"] == stage2.GLM_BASE_URL
    text = sworld.research.read_text(encoding="utf-8")
    assert "## Research swarm" not in text and "## Runner exploration" in text


def test_explicit_class_explores_without_spec_or_plan(sworld: SwarmWorld) -> None:
    # Criterion 3. Planted fault: early exploration refuses although the class is stated.
    (sworld.root / "plans/changes/demo/spec.md").unlink()
    (sworld.root / "plans/changes/demo/plan.md").unlink(missing_ok=True)
    sworld.complete()
    assert sworld.run() == 0, "the header's class routes before a spec exists"
    assert sworld.calls()[0]["kind"] == "topic"

    sworld.rewind()
    sworld.research_class(None)
    sworld.script(work=[{"stdout": "A fact."}])
    assert sworld.run("--class", "bounded") == 0, "the explicit argument routes a headerless change"
    assert [call["kind"] for call in sworld.calls()] == ["work"]


def test_missing_invalid_or_conflicting_class_refuses(sworld: SwarmWorld) -> None:
    # Criterion 4. Planted fault: the runner guesses, overrides a contrary spec, or calls anyway.
    sworld.complete()
    sworld.research_class(None)
    assert sworld.run() == 2
    assert sworld.calls() == []
    sworld.research_class("huge")
    assert sworld.run() == 2
    assert sworld.calls() == []
    sworld.research_class("bounded")
    (sworld.root / "plans/changes/demo/spec.md").write_text(
        "---\ntitle: Spec\nbead: demo-1\nclass: feature\n---\n\n# Spec\n", encoding="utf-8"
    )
    assert sworld.run() == 2
    assert sworld.calls() == []
    assert sworld.run("--class", "feature") == 2, "an explicit argument does not override a stated class"
    assert sworld.calls() == []
    assert "## Research swarm" not in sworld.research.read_text(encoding="utf-8")


@pytest.mark.parametrize("header", ["unreadable", "empty-class"])
def test_an_unreadable_header_or_empty_class_refuses(sworld: SwarmWorld, header: str) -> None:
    # F-9. Planted fault: a header that does not parse, or an empty `class:`, reads as "no class stated".
    sworld.complete()
    if header == "unreadable":
        # In spec.md: the research header carries the bead, so preflight would refuse an unreadable one anyway.
        (sworld.root / "plans/changes/demo/spec.md").write_text(
            "---\ntitle: [unclosed\nbead: demo-1\nclass: bounded\n---\n\n# Spec\n", encoding="utf-8"
        )
    else:
        sworld.research_class("")
    assert sworld.run("--class", "feature") == 2, "an explicit argument does not cure a present invalid header"
    assert sworld.calls() == []
    assert "## Research swarm" not in sworld.research.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The run's shape (spec, criteria 5, 6, 14)
# ---------------------------------------------------------------------------


def test_all_free_roles_are_attempted_before_flash(sworld: SwarmWorld) -> None:
    # Criterion 5. Planted fault: a roster member is skipped or Flash starts during the free stage.
    sworld.complete()
    assert sworld.run() == 0
    assert [(call["name"], call["kind"]) for call in sworld.calls()] == (
        [("claude", "topic")] + [("pi", "public")] * 3 + [("pi", "flash")] * 11 + [("claude", "judge")]
    )
    assert [model_of(call) for call in sworld.calls("public")] == [
        "opencode/longcat-2.5-preview-free",
        "opencode/space-bunny-free",
        "opencode/big-pickle",
    ], "every declared roster member rides the mapped inventory id, none skipped"


def test_six_topics_have_independent_permitted_pairs(sworld: SwarmWorld) -> None:
    # Criterion 6. Planted fault: a local topic rides a free seat, a duplicate report or a shared session.
    sworld.complete()
    assert sworld.run() == 0
    flash = sworld.calls("flash")
    assert len(flash) == 11
    seen: dict[int, list[str]] = {}
    for call in flash:
        model = model_of(call)
        assert model.startswith("opencode-go/"), "a Flash seat rides the Go endpoint"
        assert not any(free in model for free in FREE_IDS), "a free model never inspects the repository"
        match = re.search(r"Topic (\d) of 6", call["prompt"])
        assert match, call["prompt"][:200]
        seen.setdefault(int(match.group(1)), []).append(model.split("/", 1)[1])
    assert {topic: sorted(models) for topic, models in seen.items()} == {
        1: ["deepseek-v4.1-flash", "mimo-v2.6-flash"],
        2: ["deepseek-v4.1-flash", "mimo-v2.6-flash"],
        3: ["deepseek-v4.1-flash", "mimo-v2.6-flash"],
        4: ["deepseek-v4.1-flash", "mimo-v2.6-flash"],
        5: ["deepseek-v4.1-flash", "mimo-v2.6-flash"],
        6: ["deepseek-v4.1-flash"],
    }
    assert len({call["prompt"] for call in flash}) == 11, "no two seats share one report"
    assert len({call["agent_dir"] for call in flash}) == 11, "no two seats share one session"
    assert not any("FLASH-" in call["prompt"] for call in flash), "a peer's answer never enters another's prompt"
    judge_prompt = sworld.calls("judge")[0]["prompt"]
    assert all(f"FLASH-{n}" in judge_prompt for n in range(11)), "the judge receives every pair"


@pytest.mark.parametrize("swap", [False, True])
def test_declared_free_focuses_shape_research_and_topic_pairs(sworld: SwarmWorld, swap: bool) -> None:
    # L1-2: swap two public assignments, including the declared topic-6 seat.
    declaration = sworld.root / "model-endpoints.yaml"
    data = yaml.safe_load(declaration.read_text(encoding="utf-8"))
    roles = data["research_swarm"]
    if swap:
        first, last = FREE_IDS[0], FREE_IDS[2]
        roles["free_focuses"][first], roles["free_focuses"][last] = (
            roles["free_focuses"][last],
            roles["free_focuses"][first],
        )
        roles["topic6_free"] = first
        declaration.write_text(yaml.safe_dump(data), encoding="utf-8")
    sworld.complete(public=[{"stdout": f"PUBLIC-SEAT-{n}", "receipts": [RECEIPT]} for n in range(3)])
    assert sworld.run() == 0
    for member, call in zip(FREE_IDS, sworld.calls("public"), strict=True):
        assert "## Your assigned focus\n" in call["prompt"], "the model must receive its declared assignment"
        focus = call["prompt"].split("## Your assigned focus\n", 1)[1].split("\n## ", 1)[0]
        assert re.findall(r"Topic (\d):", focus) == [str(n) for n in roles["free_focuses"][member]]
        assert "Answer only your assigned questions" in call["prompt"]
    pairs = sworld.calls("judge")[0]["prompt"].split("# The six pairs\n", 1)[1].split("# Public source receipts", 1)[0]
    for topic in range(1, 7):
        section = pairs.split(f"## Topic {topic}:", 1)[1].split("\n## Topic ", 1)[0]
        for n, member in enumerate(FREE_IDS):
            assert (f"PUBLIC-SEAT-{n}" in section) == (topic in roles["free_focuses"][member])
        expected_flash = [2 * (topic - 1), 2 * (topic - 1) + 1] if topic <= 5 else [10]
        assert [int(n) for n in re.findall(r"FLASH-(\d+)", section)] == expected_flash
    assert f"Free seat: {roles['topic6_free']}" in pairs.split("## Topic 6:", 1)[1]


def test_declared_paid_endpoint_and_models_are_called(sworld: SwarmWorld) -> None:
    # L1-3: remove the old paid endpoint so even preflight must use the declaration.
    declaration = sworld.root / "model-endpoints.yaml"
    data = yaml.safe_load(declaration.read_text(encoding="utf-8"))
    roles = data["research_swarm"]
    paid = next(entry for entry in data["endpunkte"] if entry["name"] == roles["paid_endpoint"])
    paid["name"] = roles["paid_endpoint"] = "declared-paid-route"
    roles["topic_author"] = "claude-sonnet-5-5"
    roles["judge"] = "claude-haiku-4-5"
    paid["modelle"] = [roles["topic_author"], roles["judge"]]
    declaration.write_text(yaml.safe_dump(data), encoding="utf-8")
    sworld.complete()
    assert sworld.run() == 0
    assert model_of(sworld.calls("topic")[0]) == roles["topic_author"]
    assert model_of(sworld.calls("judge")[0]) == roles["judge"]
    record = sworld.research.read_text(encoding="utf-8")
    for model in (roles["topic_author"], roles["judge"]):
        assert f"endpoint declared-paid-route · model {model} · leak check clean" in record


def test_fresh_opus_reconciles_all_six_topics(sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 14. Planted fault: another model judges, a context is resumed, or a topic is missing.
    sworld.complete()
    assert sworld.run() == 0
    judge = sworld.calls("judge")[0]
    assert model_of(judge) == "claude-opus-5-5"
    assert judge["argv"][judge["argv"].index("--effort") + 1] == "xhigh"
    assert not any(flag in judge["argv"] for flag in ("--resume", "--continue", "-c"))
    topic = sworld.calls("topic")[0]
    assert model_of(topic) == "claude-opus-5-5"
    assert topic["argv"][topic["argv"].index("--effort") + 1] == "high"
    text = sworld.research.read_text(encoding="utf-8")
    assert "### Reconciliation" in text
    for number in range(1, 7):
        assert f"### Topic {number}" in text
    sworld.rewind()
    sworld.complete(judge={"stdout": judge_ok().replace("### Topic 3\n\n", "### Dropped\n\n", 1)})
    assert sworld.run() == 1
    assert "not 1-6 once each" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# The comparisons, the evidence and the boundary (spec, criteria 7-10, 23)
# ---------------------------------------------------------------------------


def test_research_carries_practice_architecture_and_adjacent_spec_comparisons(
    sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 7. Planted fault: a comparison field disappears or unread neighbours are labelled absent.
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    for field in ("Practice comparison:", "Architecture comparison:", "Adjacent-spec comparison:"):
        assert text.count(field) == 6, field
    sworld.rewind()
    dropped = judge_ok().replace("**Architecture comparison:**", "**Skipped:**", 1)
    sworld.complete(judge={"stdout": dropped})
    assert sworld.run() == 1
    assert "topic 1 lacks 'Architecture comparison:'" in capsys.readouterr().err


def test_public_requests_exclude_every_private_input(sworld: SwarmWorld) -> None:
    # Criterion 8. Planted fault: a repository canary reaches a public model or web request.
    canary = "PRIVATE-CANARY-42"
    for name in ("spec.md", "plan.md"):
        path = sworld.root / "plans/changes/demo" / name
        path.write_text(path.read_text(encoding="utf-8") + f"\ncanary: {canary}\n", encoding="utf-8")
    agents = sworld.root / "AGENTS.md"
    agents.write_text(agents.read_text(encoding="utf-8") + f"\nRule: {canary}\n", encoding="utf-8")
    sworld.complete()
    assert sworld.run() == 0
    for call in sworld.calls("public"):
        joined = " ".join(call["argv"])
        for blob in (call["prompt"], joined, json.dumps(call["env"])):
            assert canary not in blob, "repository content reached a free researcher"
            assert "demo" not in blob, "the change name reached a free researcher"
        assert str(sworld.root) not in call["cwd"]
        assert str(sworld.root) not in (call["prompt_path"] or "")
        assert Path(call["prompt_path"]).name == "public-prompt.md", "the prompt travels under a generic name"
        extension = call["argv"][call["argv"].index("-e") + 1]
        assert Path(extension).name == "research-tools.mjs" and str(sworld.root) not in extension
        assert str(sworld.root) not in call["env"]["STAGE2_PUBLIC_RECEIPTS"]
        assert "--no-extensions" in call["argv"], "the built-in tool surface stays off"
        # F-5. Planted fault: no `--tools` allow-list, so Pi declares its built-in tools to the free model.
        assert call["argv"][call["argv"].index("--tools") + 1] == "public_search,public_fetch"
    text = sworld.research.read_text(encoding="utf-8")
    assert canary not in text, "nothing private is published"
    assert "### Public source receipts" in text


def test_public_claims_require_retrieved_source_receipts(
    sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 10. Planted fault: an unfetched URL or a bare search snippet stands as page evidence.
    sworld.complete()
    assert sworld.run() == 0
    sworld.rewind()
    unbacked = PUBLIC_REPORT.replace("example.com/pattern", "example.com/unfetched")
    sworld.complete(public=[{"stdout": unbacked, "receipts": [RECEIPT]}] * 3)
    assert sworld.run() == 1
    assert "citations no receipt backs" in capsys.readouterr().err
    text = sworld.research.read_text(encoding="utf-8")
    assert "citations without receipts" in text, "the unbacked report is published as failed, not dropped"


@pytest.mark.parametrize("receipts", [[], [dict(RECEIPT, kind="search")], [dict(RECEIPT, status=404)]])
def test_a_free_report_without_a_retrieved_page_is_no_contribution(sworld: SwarmWorld, receipts: list) -> None:
    # F-3. Planted fault: a report from memory, with no URL and no page retrieved, passes as public evidence.
    sworld.complete(
        public=[
            {"stdout": PUBLIC_REPORT, "receipts": [RECEIPT]},
            {"stdout": "From memory: teams usually isolate such runs.", "receipts": receipts},
            {"stdout": PUBLIC_REPORT, "receipts": [RECEIPT]},
        ]
    )
    assert sworld.run() == 1, "a run cannot end complete on a contribution that retrieved no page"
    record = sworld.research.read_text(encoding="utf-8")
    assert "free researcher space-bunny-free: retrieved no public page" in status_line(record)
    assert "### Free researcher space-bunny-free (no retrieved page)" in record, "the report is kept, marked"
    assert len(sworld.calls("flash")) == 11 and sworld.calls("judge"), "the remaining roles still run"


@pytest.mark.parametrize("fault", ["invented-url", "search-snippet"])
def test_judge_public_citations_require_retrieved_receipts(sworld: SwarmWorld, fault: str) -> None:
    # L1-4: a judge cannot promote its own invented URL or a search-only receipt to fact.
    supported = judge_ok().replace("topic 1 holds", PUBLIC_REPORT + " topic 1 holds", 1)
    sworld.complete(judge={"stdout": supported})
    assert sworld.run() == 0, "a retrieved public page can support the reconciliation"
    sworld.rewind()
    if fault == "invented-url":
        sworld.complete(judge={"stdout": supported.replace("example.com/pattern", "example.com/invented")})
    else:
        sworld.complete(
            public=[{"stdout": "No public facts established.", "receipts": [dict(RECEIPT, kind="search")]}] * 3,
            judge={"stdout": supported},
        )
    assert sworld.run() == 1
    record = sworld.research.read_text(encoding="utf-8")
    assert "judge: public citations no receipt backs" in status_line(record)
    assert "### Reconciliation (failed validation" in record


def test_redirect_receipts_back_requested_and_final_urls(sworld: SwarmWorld) -> None:
    # L1-7: citing either side of a successful redirect is backed by the same retrieval.
    redirected = dict(RECEIPT, final_url="https://example.com/final-pattern")
    sworld.complete(
        public=[{"stdout": PUBLIC_REPORT, "receipts": [redirected]}] * 3,
        judge={"stdout": judge_ok() + "\n" + PUBLIC_REPORT.replace("/pattern", "/final-pattern")},
    )
    assert sworld.run() == 0
    assert "status: complete" in status_line(sworld.research.read_text(encoding="utf-8"))
    assert stage2_swarm.receipt_problems(PUBLIC_REPORT, [dict(redirected, status=503)])


def test_free_environment_excludes_identity_and_private_paths(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # L1-5: plant ambient identity, configuration, temp paths and every locale variable.
    forbidden = ("USER", "LOGNAME", "SHELL", "TMPDIR", "LANG", "LC_ALL", "LC_CTYPE", "LC_MESSAGES", "CODEX_HOME")
    for name in forbidden:
        monkeypatch.setenv(name, "/private-identity/ambient")
    captured: list[dict] = []
    launch = stage2.launch

    def capture(command, root, env, *args, **kwargs):
        if "STAGE2_PUBLIC_RECEIPTS" in env or command == [str(stage2.PI_WRAPPER), "--list-models"]:
            captured.append(dict(env))
        return launch(command, root, env, *args, **kwargs)

    monkeypatch.setattr(stage2, "launch", capture)
    sworld.complete()
    assert sworld.run() == 0
    assert len(captured) == 4
    assert captured[0]["OPENCODE_API_KEY"] == OKEY, "the inventory runs with the free call's own credential"
    for env in captured:
        assert not set(forbidden) & env.keys(), env
        assert "PATH" in env and "HOME" in env and "PI_CODING_AGENT_DIR" in env
        assert "/private-identity/ambient" not in json.dumps(env)
        assert set(env) <= {"PATH", "HOME", "PI_CODING_AGENT_DIR", "OPENCODE_API_KEY", "STAGE2_PUBLIC_RECEIPTS"}


@pytest.mark.parametrize(
    "answer",
    [
        "Two sentences. Here is the second one.",
        "a " + "word " * 20 + "long",
        "isolation for src/app.py runs",
        "isolation for myValue runs",
        "the demo change's isolation",
        "isolation for the demo-1 tracker work",
        # F-4. Planted fault: a hyphenated identifier without a digit passes as a plain word.
        "isolation for the coding-harness-yim tracker work",
        "container isolation in the coding-harness repository",
        "routing research through claude-code-plan",
        "public research on the opencode-free endpoint",
        "exploration in the style of research-swarm",
    ],
)
def test_public_topic_is_filtered_before_free_calls(sworld: SwarmWorld, answer: str) -> None:
    # Criterion 23. Planted fault: a rejected topic still reaches the free researchers.
    sworld.complete(topic={"stdout": answer})
    assert sworld.run() == 1
    assert sworld.calls("public") == [] and sworld.calls("flash") == [] and sworld.calls("judge") == []
    text = sworld.research.read_text(encoding="utf-8")
    assert "public topic rejected" in text and "No free call starts" in text
    assert f"public topic: {answer}" not in text


def test_an_accepted_topic_is_recorded_and_reaches_the_free_calls(
    sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 23's accepted side: the topic is recorded and is the only change text the free calls carry.
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    assert "public topic: container isolation for AI agent runs" in text
    assert TOPIC_OK in sworld.calls("public")[0]["prompt"]
    sworld.rewind()
    sworld.complete(topic={"stdout": "   "})
    assert sworld.run() == 1
    assert not sworld.calls("public")
    assert "the public topic call failed" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# The declaration and the leak check (spec, criteria 11, 12)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate",
    ["free-sees-framework", "roster-off-endpoint", "pair-off-endpoint", "judge-off-endpoint", "topic6-wrong-focus"],
)
def test_declarations_clear_only_the_role_data_class(sworld: SwarmWorld, mutate: str) -> None:
    # Criterion 11. Planted fault: an undeclared model is called or a public endpoint reads framework content.
    sworld.complete()
    text = (sworld.root / "model-endpoints.yaml").read_text(encoding="utf-8")
    if mutate == "free-sees-framework":
        text = text.replace("    darf_sehen: [public-web]\n", "    darf_sehen: [public-web, framework]\n", 1)
    elif mutate == "roster-off-endpoint":
        text = text.replace("      - space-bunny-free\n", "", 1)
    elif mutate == "pair-off-endpoint":
        text = text.replace(
            "  flash_pair: [deepseek-v4.1-flash, mimo-v2.6-flash]",
            "  flash_pair: [deepseek-v4.1-flash, glm-5.3-flash]",
        )
    elif mutate == "judge-off-endpoint":
        text = text.replace("  judge: claude-opus-5-5", "  judge: mimo-v2.6-pro")
    else:
        text = text.replace("  topic6_free: big-pickle", "  topic6_free: longcat-2.5-preview-free")
    (sworld.root / "model-endpoints.yaml").write_text(text, encoding="utf-8")
    assert sworld.run() == 2
    assert sworld.calls() == [], "a declaration fault refuses before any model call"


def test_the_public_endpoint_stays_out_of_the_framework_check(sworld: SwarmWorld) -> None:
    # Criterion 11's scoped checks: the public check alone clears the roster; the framework check refuses it.
    for member in FREE_IDS:
        assert stage2.public_declaration_problem(sworld.root, "opencode-free", member) is None
        assert stage2.declaration_problem(sworld.root, "opencode-free", member) is not None, (
            "unknown residency and no framework permission stay refused for repository content"
        )
    assert stage2.public_declaration_problem(sworld.root, "opencode-free", "mimo-v2.6-pro") is not None


def test_every_call_is_checked_and_a_leak_block_stops_dispatch(sworld: SwarmWorld) -> None:
    # Criterion 12. Planted fault: one scan covers all calls, or a call follows a BLOCK.
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    assert text.count("leak check clean over") == 16, "every call carries its own check"
    sworld.rewind()
    (sworld.root / "src" / "leak.txt").write_text(f"planted = {LEAK}\n", encoding="utf-8")
    assert sworld.run() == 2
    assert sworld.calls() == [], "no call starts after a BLOCK, and no fallback follows it"
    text = sworld.research.read_text(encoding="utf-8")
    assert "refused - the leak check is not clean" in text
    assert "leak check clean" not in text, "a blocked slot is never claimed as clean"


# ---------------------------------------------------------------------------
# The audit, the failures and the budgets (spec, criteria 13, 18, 19, 21)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("kind", ["public", "flash"])
@pytest.mark.parametrize("fault", ["nonzero", "empty", "timeout"])
def test_failed_pi_calls_preserve_partial_evidence(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch, kind: str, fault: str
) -> None:
    # L1-1: retrieve a page and emit partial output before failure or the actual subprocess timeout.
    partial = f"PARTIAL-{kind} @KEY@"
    step = {
        "stdout": "" if fault == "empty" else partial,
        "receipts": [dict(RECEIPT, excerpt="page @KEY@")],
        "exit": 7 if fault == "nonzero" else 0,
        "sleep": 5 if fault == "timeout" else 0,
    }
    sworld.complete(**{kind: [step]})
    if fault == "timeout":
        launch = stage2.launch

        def short_launch(command, root, env, *args, **kwargs):
            is_public = "STAGE2_PUBLIC_RECEIPTS" in env
            if command[0] == str(stage2.PI_WRAPPER) and "--print" in command and is_public == (kind == "public"):
                kwargs["timeout"] = 1.0
            return launch(command, root, env, *args, **kwargs)

        monkeypatch.setattr(stage2, "launch", short_launch)
    assert sworld.run() == 1
    record = sworld.research.read_text(encoding="utf-8")
    assert "status: incomplete" in status_line(record)
    assert "failed" in record
    if fault != "empty":
        assert f"PARTIAL-{kind} [credential]" in record, "failed stdout is durable and scrubbed"
        assert f"PARTIAL-{kind} [credential]" in sworld.calls("judge")[0]["prompt"]
    if kind == "public":
        assert '"excerpt": "page [credential]"' in record, "receipts survive scratch cleanup on every failure"
        assert '"excerpt": "page [credential]"' in sworld.calls("judge")[0]["prompt"]
        assert len(sworld.calls("public")) == 3
    assert len(sworld.calls("flash")) == 11
    assert not any(OKEY[n : n + 8] in record for n in range(len(OKEY) - 7))


def test_every_attempt_has_identity_audit_and_outcome(sworld: SwarmWorld) -> None:
    # Criterion 13. Planted fault: a failed slot is silent, or the judge has no audit of its own.
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    day = r"\d{4}-\d{2}-\d{2}"
    run_id = re.search(r"run (swarm-[0-9a-f]{8})", text).group(1)
    clean = re.findall(
        rf"^Stage-2 call, {day}: swarm .+ · run {run_id} · endpoint \S+ · model \S+ · "
        rf"leak check clean over \d+ files, \d+ commits, \d+ rules\.$",
        text,
        re.M,
    )
    assert len(clean) == 16
    assert re.search(
        rf"^Stage-2 call, {day}: swarm judge · run {run_id} · endpoint claude-code-plan · "
        rf"model claude-opus-5-5 · leak check clean over \d+ files",
        text,
        re.M,
    )
    outcomes = re.findall(rf"^Swarm outcome, {day}: swarm .+ · run {run_id} · model \S+ · ok \(\d+s\)\.$", text, re.M)
    assert len(outcomes) == 16
    sworld.rewind()
    flash = [{"stdout": f"FLASH-{n}"} for n in range(11)]
    flash[4] = {"stdout": "broken", "exit": 1}
    sworld.complete(flash=flash)
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    second = re.search(r"run (swarm-[0-9a-f]{8})", text).group(1)
    assert re.search(
        rf"^Swarm outcome, {day}: swarm flash researcher · topic 3 · run {second} · "
        rf"model deepseek-v4\.1-flash · failed - pi \(deepseek-v4\.1-flash\) ended 1 \(\d+s\)\.$",
        text,
        re.M,
    ), "the failed slot keeps its durable audit"


@pytest.mark.parametrize(
    "fault",
    ["free-fails", "flash-empty", "judge-malformed", "all-free-fail", "unmapped-free-id"],
)
def test_failures_preserve_evidence_and_never_report_complete(sworld: SwarmWorld, fault: str) -> None:
    # Criterion 18. Planted fault: a broken run exits 0 or claims a complete result.
    if fault == "free-fails":
        sworld.complete(
            public=[
                {"stdout": PUBLIC_REPORT, "receipts": [RECEIPT]},
                {"stdout": "stalled", "exit": 1},
                {"stdout": PUBLIC_REPORT, "receipts": [RECEIPT]},
            ]
        )
    elif fault == "flash-empty":
        flash = [{"stdout": f"FLASH-{n}"} for n in range(11)]
        flash[2] = {"stdout": "   "}
        sworld.complete(flash=flash)
    elif fault == "judge-malformed":
        sworld.complete(judge={"stdout": "I could not reconcile everything, sorry."})
    elif fault == "all-free-fail":
        sworld.complete(public=[{"stdout": "", "exit": 1}] * 3)
    else:
        sworld.script(pi_models=pi_table([("opencode", "longcat-2.5-preview-free")]))
        sworld.complete()
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    if fault == "unmapped-free-id":
        assert "does not map the free id(s) space-bunny-free, big-pickle" in text
        assert "status:" not in text and not sworld.calls("public")
        return
    assert "status: complete" not in text
    assert re.search(r"^run swarm-[0-9a-f]{8} status: incomplete - ", text, re.M)
    if fault == "free-fails":
        assert "flash researcher · topic 1" in text and "### Reconciliation" in text
    if fault == "flash-empty":
        assert "answered nothing" in text and "### Repository reports" in text
    if fault == "judge-malformed":
        assert "the judge wrote topic sections [], not 1-6 once each" in text
        assert "### Reconciliation" in text
    if fault == "all-free-fail":
        assert "(none succeeded)" in text and "flash researcher · topic 1" in text


@pytest.mark.parametrize("inventory", ["pinned-registry", "ambiguous", "no-models"])
def test_the_free_inventory_reads_what_the_pinned_pi_prints(sworld: SwarmWorld, inventory: str) -> None:
    # F-2(b). Planted fault: the inventory parses only JSON lines, or takes whichever provider is listed last.
    if inventory == "pinned-registry":
        # Pi 1.1.0's registry (read, not run) listed the first roster's `space-bunny` and `hy4-preview`
        # only under the paid Go provider; here a roster id stands only there.
        listing = pi_table(
            [
                ("opencode", "longcat-2.5-preview-free"),
                ("opencode", "space-bunny-free"),
                ("opencode-go", "big-pickle"),
                ("opencode-go", "longcat-2.5-preview-free"),
                ("opencode-go", "space-bunny"),
            ]
        )
        expected = "does not map the free id(s) big-pickle to a provider other than the paid opencode-go"
    elif inventory == "ambiguous":
        listing = pi_table([*(("opencode", member) for member in FREE_IDS), ("mirror", "space-bunny-free")])
        expected = "lists the free id(s) space-bunny-free (mirror, opencode) under more than one provider"
    else:
        listing = ["No models available. Set an API key or log in."]
        expected = "does not map the free id(s) longcat-2.5-preview-free, space-bunny-free, big-pickle"
    sworld.script(pi_models=listing)
    sworld.complete()
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    assert expected in text, text[-800:]
    assert not sworld.calls("public") and not sworld.calls("flash") and not sworld.calls("judge")
    sworld.rewind()
    sworld.script(pi_models=PI_MODELS)
    sworld.complete()
    assert sworld.run() == 0
    assert "free transport: longcat-2.5-preview-free rides opencode/longcat-2.5-preview-free;" in (
        sworld.research.read_text(encoding="utf-8")
    ), "the free provider wins over the paid namesake"


def test_deadlines_and_role_counts_bound_the_run(sworld: SwarmWorld) -> None:
    # Criterion 19. Planted fault: a role is retried, or a launch outruns its remaining allowance.
    assert stage2_swarm.allowance(0.0, stage2_swarm.TOPIC_MINUTES) == 300.0
    assert stage2_swarm.allowance(0.0, stage2_swarm.RESEARCHER_MINUTES) == 600.0
    assert stage2_swarm.allowance(0.0, stage2_swarm.JUDGE_MINUTES) == 900.0
    assert stage2_swarm.allowance(30.0, stage2_swarm.RESEARCHER_MINUTES) == 600.0
    assert stage2_swarm.allowance(149 * 60.0, stage2_swarm.RESEARCHER_MINUTES) == 60.0, (
        "a launch takes the run's remaining allowance when the role deadline is longer"
    )
    assert stage2_swarm.allowance(200 * 60.0, stage2_swarm.RESEARCHER_MINUTES) == 0.0, (
        "nothing starts after the whole-run deadline"
    )
    sworld.complete()
    assert sworld.run() == 0
    assert len(sworld.calls()) == 16, "one topic call, three free researchers, eleven Flash calls, one judge"
    sworld.rewind()
    flash = [{"stdout": f"FLASH-{n}"} for n in range(11)]
    flash[3] = {"stdout": "", "exit": 1}
    sworld.complete(flash=flash)
    assert sworld.run() == 1
    flash_calls = sworld.calls("flash")
    assert len(flash_calls) == 11, "a failed seat is attempted once, never retried"
    models = [model_of(call) for call in flash_calls]
    assert models.count("opencode-go/mimo-v2.6-flash") == 5
    assert models.count("opencode-go/deepseek-v4.1-flash") == 6


def test_no_call_starts_once_the_run_deadline_is_spent(sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch) -> None:
    # F-6. Planted fault: a spent deadline still gates, audits as clean and launches with timeout 0.
    launch = stage2.launch

    def spend_after_the_free_stage(command, root, env, *args, **kwargs):
        done = launch(command, root, env, *args, **kwargs)
        if "STAGE2_PUBLIC_RECEIPTS" in env and len(sworld.calls("public")) == 3:
            monkeypatch.setattr(stage2_swarm, "RUN_MINUTES", 0.0)
        return done

    monkeypatch.setattr(stage2, "launch", spend_after_the_free_stage)
    sworld.complete()
    assert sworld.run() == 1
    assert [call["kind"] for call in sworld.calls()] == ["topic"] + ["public"] * 3, "no process after the deadline"
    record = sworld.research.read_text(encoding="utf-8")
    assert record.count("leak check clean over") == 4, "no gate and no clean claim for an unstarted slot"
    assert record.count("not started - the whole-run deadline is spent") == 12, "every unfinished slot is recorded"
    assert "judge: not started - the whole-run deadline of 0 minutes is spent" in status_line(record)


def test_a_run_across_midnight_keeps_its_frozen_research(sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch) -> None:
    # F-7. Planted fault: the runner's own `updated:` re-stamp counts as a changed input.
    day = [datetime.date(2026, 10, 15)]
    stamp = stage2.check_frontmatter_current.stamp
    monkeypatch.setattr(stage2.check_frontmatter_current, "stamp", lambda path, _today: stamp(path, day[0]))
    launch = stage2.launch

    def midnight(command, root, env, *args, **kwargs):
        if "STAGE2_PUBLIC_RECEIPTS" in env:
            day[0] = datetime.date(2026, 10, 16)
        return launch(command, root, env, *args, **kwargs)

    monkeypatch.setattr(stage2, "launch", midnight)
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    assert "\nupdated: 2026-10-16\n" in text.split("\n---\n", 1)[0], "the date did cross during the run"
    assert "status: complete" in status_line(text)
    assert stage2_swarm.without_updated(b"---\ntitle: A\nupdated: 2026-10-16\n---\nbody updated: x\n") == (
        b"---\ntitle: A\nupdated:\n---\nbody updated: x\n"
    ), "only the header's stamp is left out; the body and other fields still compare"


def test_all_outputs_scrub_every_used_credential(sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 21. Planted fault: an eight-character fragment of the used credential survives anywhere.
    receipt = dict(RECEIPT, excerpt="bytes @KEY@ here")
    sworld.complete(
        public=[{"stdout": "public saw @KEY@", "receipts": [receipt]}] * 3,
        flash=[{"stdout": "flash saw @KEY@", "stderr": "@KEY@", "exit": 1}]
        + [{"stdout": f"FLASH-{n}"} for n in range(1, 11)],
    )
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    seen = capsys.readouterr()
    assert "[credential]" in text, "the report text is scrubbed"
    assert "[credential]" in text.split("```jsonl")[1], "the receipts are scrubbed"
    assert "[credential]" in seen.err, "the failed call's relayed stderr is scrubbed"
    for blob in (text, seen.out + seen.err):
        assert not any(OKEY[i : i + 8] in blob for i in range(len(OKEY) - 7)), blob


# ---------------------------------------------------------------------------
# The frozen input state and the append-only research (spec, criteria 15-17)
# ---------------------------------------------------------------------------


def test_unresolved_dissent_and_human_questions_survive_reconciliation(
    sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 15. Planted fault: sourced dissent is erased or a preference becomes a human answer.
    dissent = "the free source says sandboxing suffices; `src/app.py::value` shows the worktree is the boundary"
    question = "should the swarm also cover the review loop?"
    answer = (
        judge_ok()
        .replace("**Disagreement:**\n\n**Gaps:**", f"**Disagreement:** {dissent}\n\n**Gaps:**", 1)
        .replace("**Human questions:**\n", f"**Human questions:** {question}\n", 1)
    )
    sworld.complete(judge={"stdout": answer})
    assert sworld.run() == 0, "dissent does not make a run incomplete; it is retained, not resolved"
    text = sworld.research.read_text(encoding="utf-8")
    assert dissent in text and question in text
    assert "status: complete" in status_line(text)
    sworld.rewind()
    sworld.complete(judge={"stdout": judge_ok().replace("**Disagreement:**\n\n", "", 1)})
    assert sworld.run() == 1
    assert "topic 1 lacks 'Disagreement:'" in capsys.readouterr().err


def test_local_citations_bind_to_the_frozen_input_state(sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 16. Planted fault: a nonexistent source, a changed input or a lost report passes validation.
    sworld.complete()
    assert sworld.run() == 0, "`src/app.py::value` is tracked at the frozen state"
    sworld.rewind()
    sworld.complete(judge={"stdout": judge_ok().replace("`src/app.py::value`", "`src/ghost.py::x`", 1)})
    assert sworld.run() == 1
    assert "src/ghost.py::x" in capsys.readouterr().err
    sworld.rewind()
    flash = [{"stdout": f"FLASH-{n}"} for n in range(11)]
    flash[6] = {"stdout": "FLASH-6", "plant": {"src/app.py": "value = 2\n"}}
    sworld.complete(flash=flash)
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    assert "the frozen input state changed: src/app.py" in text
    assert "### Reconciliation" in text, "the run still publishes what it collected, as incomplete"


@pytest.mark.parametrize(
    ("citation", "problem"),
    [
        ("`src/app.py::no_such_symbol`", "names no symbol of src/app.py"),
        ("`src/app.py:1`", "gives line numbers only"),
        ("`src/app.py`", "is a bare path"),
    ],
)
def test_local_citations_name_a_path_and_a_symbol(
    sworld: SwarmWorld, capsys: pytest.CaptureFixture[str], citation: str, problem: str
) -> None:
    # F-8. Planted fault: a tracked path vouches for a missing symbol, or line numbers stand in for one.
    sworld.complete(judge={"stdout": judge_ok().replace("`src/app.py::value`", citation, 1)})
    assert sworld.run() == 1
    assert problem in capsys.readouterr().err
    assert "### Reconciliation (failed validation" in sworld.research.read_text(encoding="utf-8")


def test_only_the_runner_appends_research(sworld: SwarmWorld) -> None:
    # Criterion 17. Planted fault: a participant edits the tree, or earlier research is replaced.
    seed = sworld.research.read_text(encoding="utf-8")
    sworld.complete()
    assert sworld.run() == 0
    now = sworld.research.read_text(encoding="utf-8")
    # The runner may refresh this one metadata line while appending. Every
    # other byte of the earlier header and body must stay unchanged.
    stamped_seed = re.sub(r"^updated: .*?$", f"updated: {stage2.today()}", seed, count=1, flags=re.M)
    assert now.startswith(stamped_seed), "only the updated date may change before the append"
    done = subprocess.run([GIT, "status", "--porcelain"], cwd=sworld.root, capture_output=True, text=True, check=True)
    assert [line for line in done.stdout.splitlines() if line.strip()] == [" M plans/changes/demo/research.md"], (
        "no repository file outside the research artefact changed"
    )


# ---------------------------------------------------------------------------
# The doctrine and the declaration agree (spec, criterion 22)
# ---------------------------------------------------------------------------


def test_phase_one_doctrine_and_declarations_agree() -> None:
    # Criterion 22. Planted fault: universal single-explorer prose, an unresolvable roster or a changed ladder.
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    assert stage2_swarm.swarm_problems(data) == [], "the declared swarm block must resolve"
    go = next(entry for entry in data["endpunkte"] if entry["name"] == "opencode-go")
    assert go["modelle"] == ["deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"], (
        "the review ladder keeps its order; the swarm block changes it in no way"
    )
    roster = set(data["research_swarm"]["free_roster"])
    assert roster.isdisjoint(go["modelle"]), "no free id joined the Go ladder"
    roles = data["research_swarm"]
    assert roles["judge"] == roles["topic_author"] == "claude-opus-5-5"
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "so does phase 1 now (ADR 0020)" in agents
    assert "the research swarm (ADR 0020" in agents
    workflow = (REPO_ROOT / "docs/WORKFLOW.md").read_text(encoding="utf-8")
    assert "| 1 Explore swarm |" in workflow and "| 1 Explore |" in workflow
    explore_prompt = (REPO_ROOT / "prompts/01-explore.md").read_text(encoding="utf-8")
    assert "Routing by class (ADR 0020)." in explore_prompt
    for free_id in roster:
        assert free_id not in workflow and free_id not in agents, "a free id stays out of the review-ladder doctrine"
