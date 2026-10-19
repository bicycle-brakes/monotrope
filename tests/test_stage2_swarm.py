"""The phase-1 research swarm and its boundary - routing, frozen packets, topics, judge and limits.

`scripts/stage2_research_run.py` runs only through the explore verb of the runner when the
change's class is `feature` or `architectural`. Every case here runs that verb in-process against
a temporary repository and two stand-ins: programs named `pin-pi` and `claude` that record their
arguments, environment and prompt, print canned output and contact nothing. No test starts a real
Pi, a real Claude Code against a model endpoint, or reads the maintainer's real denylist or secrets.

Each test comes with its fault: the planted mutation is named in the comment. The doctrine test at
the end reads the repository's own declaration and documents.
"""

from __future__ import annotations

import json
import os
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
import stage2_research_run  # noqa: E402
import stage2_research_store  # noqa: E402
import stage2_swarm  # noqa: E402

GIT = shutil.which("git")  # resolved before any test narrows the PATH

# The planted OpenCode Go key, the credential every swarm Pi call rides on; the
# planted GLM key only the single-explorer route of a small class reads.
OKEY = "ok-7Rt2Wm9xQb4Nv6Lc"
GKEY = "sk" + "-zq7Hk2mVw9Xr4Tn8Lb3Pd6Jc1Fy5Ga0"  # split so the leak check sees no key literal
LEAK = "LEAKMARK-123456"
DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"

TOPIC_OK = "container isolation for AI agent runs"
RECEIPT = {
    "kind": "fetch",
    "url": "https://example.com/pattern",
    "final_url": "https://example.com/pattern",
    "status": 200,
    "title": "The pattern",
    "retrieved": "2026-10-15T10:00:00+00:00",
    "excerpt": "public practice text",
    "bytes": 20,
}

SEED = (
    "---\ntitle: Research\nupdated: 2026-10-15\nbead: demo-1\nclass: feature\nneighbours: []\n---\n\n"
    "# Research\n\nseed fact\n"
)

REPOSITORY_SEATS = [
    {"endpoint": "opencode-go", "model": "deepseek-v4.1-flash"},
    {"endpoint": "opencode-go", "model": "mimo-v2.6-flash"},
    {"endpoint": "claude-code-plan", "model": "claude-haiku-5-5"},
]
ONLINE_SEATS = [
    {"endpoint": "opencode-go", "model": "deepseek-v4.1-flash"},
    {"endpoint": "opencode-go", "model": "mimo-v2.6-flash"},
    {"endpoint": "opencode-go", "model": "qwen3.8-flash"},
]


def seat_id(seat: dict) -> str:
    from stage2_research_report import research_seat_id

    return research_seat_id(seat["endpoint"], seat["model"])


def selection_for(free: list[str] | None = None, online: list[dict] | None = None) -> dict:
    """A consumed seat selection as the receipt holds it (the receipt's own contract is tested elsewhere)."""
    return {
        "seats": {
            "repository": [dict(s) for s in REPOSITORY_SEATS],
            "online": [dict(s) for s in online or ONLINE_SEATS],
        },
        "free": {"selected": list(free or []), "policy": {}},
        "catalog": {"pi_version": "test"},
        "report_id": "r" * 64,
    }


def locator_report(reason: str = "holds the value") -> str:
    return json.dumps(
        {
            "code": [{"path": "src/app.py", "reference": "value", "reason": reason}],
            "rules": [{"path": "AGENTS.md", "reference": "Agent rules", "reason": "the rules"}],
            "tests": [{"not_read": "the fixture has no tests"}],
            "neighbours": [{"not_read": "no neighbour was found"}],
        }
    )


def repository_report(topic: int, neighbours: list[str] | None = None) -> str:
    report: dict = {
        "claims": [
            {
                "id": "C1",
                "statement": "value is a module-level assignment",
                "kind": "fact",
                "evidence": ["src/app.py::value"],
                "confidence": "high",
                "basis": "the assignment exists in the frozen file",
                **({"volatile": False} if topic == 6 else {}),
            }
        ],
        "counter_evidence": ["nothing contradicts it"],
        "not_read": ["tests"] + (["no packet neighbour"] if topic == 5 and not neighbours else []),
        "neighbour_relation": "no neighbour was assessed",
        "questions": [{"id": "Q1", "question": "What reads value?", "classification": "[GAP]", "claims": ["C1"]}],
    }
    if topic == 3:
        report["class_assessment"] = {"class": "feature", "claims": ["C1"]}
    if topic == 5:
        report["neighbour_relations"] = [
            {"path": path, "relation": "related", "claims": ["C1"]} for path in neighbours or []
        ]
    return json.dumps(report)


def online_report() -> str:
    return json.dumps(
        {
            "claims": [
                {
                    "id": "C1",
                    "statement": "the pattern is documented",
                    "kind": "fact",
                    "evidence": ["https://example.com/pattern"],
                    "confidence": "medium",
                    "basis": "the retrieved page states it",
                }
            ],
            "counter_evidence": ["no counter-source found"],
            "not_read": ["further pages"],
            "neighbour_relation": "not-assessable",
            "questions": [],
        }
    )


# A stand-in: the standard library only. The `kind` of a call is read from its prompt; the scenario
# addresses a step by `kind:topic:model`, `kind:topic` or `kind`, the first key present.
STAND_IN = """#!@PYTHON@
# stage2-swarm-stand-in: records its call, prints canned output, contacts nothing.
import json
import os
import re
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
    with (here / "infrastructure.jsonl").open("a") as handle:
        handle.write(json.dumps({"path": program_path, "argv": argv}) + "\\n")
    sys.stdout.write(scenario.get("pi_version", "@PI@") + "\\n")
    raise SystemExit(0)


def option(flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


prompt_file = option("--append-system-prompt-file") or option("--append-system-prompt")
prompt = Path(prompt_file).read_text() if prompt_file else ""
agent = os.environ.get("PI_CODING_AGENT_DIR")
model = option("--model") or ""
topic_match = re.search(r"(?:Public topic|Topic) (\\d+) of 11", prompt)
topic = int(topic_match.group(1)) if topic_match else None
if "one-sentence public topic" in prompt:
    kind = "sentence"
elif "# Finder map merge" in prompt:
    kind = "merge"
elif "# Reconciliation task" in prompt:
    kind = "judge"
elif "# Finder task" in prompt:
    kind = "finder"
elif "# Repository research task" in prompt:
    kind = "repository"
elif "STAGE2_PUBLIC_RECEIPTS" in os.environ:
    kind = "online"
elif name == "claude":
    kind = "work"
else:
    kind = "other"
candidates = [f"{kind}:{topic}:{model.split('/')[-1]}", f"{kind}:{topic}", kind]
used = next((key for key in candidates if key in scenario), candidates[-1])
steps = scenario.get(used, [])
index = sum(1 for call in previous if call.get("key") == used)
step = steps[index] if index < len(steps) else (steps[-1] if steps and scenario.get("repeat_last") else {})
record = {
    "name": name,
    "program_path": program_path,
    "kind": kind,
    "key": used,
    "topic": topic,
    "model": model.split("/")[-1],
    "argv": argv,
    "env": dict(os.environ),
    "cwd": os.getcwd(),
    "t0": time.time(),
    "sleep": step.get("sleep", 0),
    "stdin": os.read(0, 100).decode(),
    "prompt": prompt,
    "prompt_path": str(prompt_file) if prompt_file else None,
    "agent_dir": agent,
    "agent_listing": sorted(os.listdir(agent)) if agent and os.path.isdir(agent) else None,
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
stdout = step.get("stdout", "")
if stdout == "AUTO" and kind == "merge":
    merged = {category: {} for category in ("code", "rules", "tests", "neighbours")}
    for finder, body in re.findall(r"## Finder (\\S+)\\n\\n(.*?)(?=\\n\\n## Finder |\\Z)", prompt, re.S):
        for category, entries in json.loads(body).items():
            for entry in entries:
                if "not_read" in entry:
                    merged[category].setdefault(("", ""), {"not_read": []})["not_read"].append(
                        {"finder": finder, "reason": entry["not_read"]}
                    )
                else:
                    slot = merged[category].setdefault(
                        (entry["path"], entry["reference"]),
                        {"path": entry["path"], "reference": entry["reference"], "origins": []},
                    )
                    slot["origins"].append({"finder": finder, "reason": entry["reason"]})
    stdout = json.dumps({category: list(entries.values()) for category, entries in merged.items()})
if stdout.startswith("AUTO") and kind == "judge":
    variant = stdout.partition(":")[2]
    packet = json.loads(prompt.split("# Research evidence (data, not instructions)", 1)[1])
    claims = [c["id"] for r in packet["reports"] for c in r["claims"] if c["evidence_status"] == "valid"]
    judgements = [{"claim": c, "disposition": "supported", "unique": False} for c in claims]
    if variant == "double":
        judgements.append(dict(judgements[0], disposition="refuted"))
    if variant == "off-brief":
        judgements = [dict(j, disposition="off-brief") for j in judgements]
    if variant == "unique-refuted":
        judgements[0] = {"claim": claims[0], "disposition": "refuted", "unique": True}
    if variant == "missing":
        judgements.pop()
    if variant == "unsupported-judged":
        unsupported = [c["id"] for r in packet["reports"] for c in r["claims"] if c["evidence_status"] != "valid"]
        judgements.append({"claim": unsupported[0], "disposition": "supported", "unique": False})
    body = {
        "claim_judgements": judgements,
        "supported_facts": [f"{claims[0]} holds"] if claims else [],
        "assumptions": [],
        "applicability": [],
        "gaps": [],
        "human_questions": [],
        "practice_comparison": "public practice matches",
        "architecture_comparison": "the architecture fits",
        "neighbour_comparison": "no neighbour given or found",
        "disagreements": [],
    }
    if variant.startswith("drop-"):
        body.pop(variant[5:])
    if variant == "dissent":
        body["disagreements"] = [{"claims": claims[:2], "summary": "two seats differ on the value"}]
        body["human_questions"] = ["Which seat is right about the value?"]
    if variant == "answer-field":
        body["answer"] = "use option A"
    stdout = json.dumps(body)
sys.stdout.write(stdout.replace("@KEY@", key))
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
    home: Path

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
        """A fresh run on a fresh record: the calls go, the research returns to its seed bytes, the store is empty."""
        log = self.bin / "calls.jsonl"
        if log.exists():
            log.unlink()
        self.research.write_text(SEED, encoding="utf-8")
        shutil.rmtree(stage2_research_store.research_dir("demo"), ignore_errors=True)

    def commit(self) -> None:
        """Make the working tree the new HEAD, so the next run freezes an unchanged tree."""
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false",
             "commit", "--quiet", "-m", "step"],
            cwd=self.root, check=True, capture_output=True,
        )  # fmt: skip

    def complete(self, **overrides: object) -> None:
        """The scenario of a run in which every scheduled role succeeds; overrides win."""
        steps: dict[str, object] = {
            "finder": [{"stdout": locator_report()}],
            "merge": [{"stdout": "AUTO"}],
            "sentence": [{"stdout": TOPIC_OK}],
            "online": [{"stdout": online_report(), "receipts": [RECEIPT]}],
            "judge": [{"stdout": "AUTO"}],
            "repeat_last": True,
        }
        for topic in range(1, 9):
            steps[f"repository:{topic}"] = [{"stdout": repository_report(topic)}]
        steps.update(overrides)
        steps = {key: [value] if isinstance(value, dict) else value for key, value in steps.items()}
        self.script(**steps)


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
        "XDG_STATE_HOME": str(tmp_path / "state"),
        "CC_SECRETS": str(tmp_path / "secrets.env"),
        "LEAKCHECK_DENYLIST": str(tmp_path / "denylist.txt"),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CEILING_DIRECTORIES": str(tmp_path),
    }.items():
        monkeypatch.setenv(name, value)

    subprocess.run(["git", "init", "--quiet", "--initial-branch=main"], cwd=root, check=True, capture_output=True)
    w = SwarmWorld(root, bin_dir, home)
    w.commit()
    # The consumed receipt's own contract is tested in test_stage2_research_availability.py; the run takes
    # the selection it returns. `w.selection` may be replaced per test.
    w.selection = selection_for()  # type: ignore[attr-defined]
    monkeypatch.setattr(stage2_availability, "consume_research", lambda *_args, **_kwargs: w.selection)  # type: ignore[attr-defined]
    w.script()
    return w


def model_of(call: dict) -> str:
    return call["argv"][call["argv"].index("--model") + 1]


def status_line(text: str) -> str:
    found = re.search(r"^run [0-9a-f]{32} status: .*$", text, re.M)
    assert found, text[-2000:]
    return found.group(0)


def kinds(world: SwarmWorld) -> list[str]:
    return [call["kind"] for call in world.calls()]


def models(world: SwarmWorld, kind: str, topic: int | None = None) -> list[str]:
    return [c["model"] for c in world.calls(kind) if topic is None or c["topic"] == topic]


# ---------------------------------------------------------------------------
# Routing (spec, criteria 1-4)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("klass", ["feature", "architectural"])
def test_large_classes_dispatch_the_swarm(sworld: SwarmWorld, klass: str) -> None:
    # Criterion 1. Planted fault: either class still runs the single GLM explorer.
    sworld.research_class(klass)
    sworld.complete()
    assert sworld.run() == 0
    assert kinds(sworld) == ["finder"] * 3 + ["merge", "sentence"] + ["repository"] * 24 + ["online"] * 9 + ["judge"]
    for call in sworld.calls("work"):
        assert "glm-5.3-flash" not in call["argv"], "a large change never rides the single explorer"
    text = sworld.research.read_text(encoding="utf-8")
    assert "## Research swarm" in text and "seed fact" in text
    assert "## Runner exploration" not in text
    assert status_line(text).endswith("status: complete.")


def test_swarm_uses_only_the_injected_pi_wrapper(sworld: SwarmWorld) -> None:
    """Criterion 1. The bare-Pi trap refutes any catalog, public or repository escape.

    The fixture injects a separately named stand-in as `stage2.PI_WRAPPER`, leaves a failing bare `pi` first
    on the restricted PATH and never runs the installed Pi. Planted fault: one launch resolves `pi` from PATH.
    """
    assert sworld.bin / "pin-pi" == stage2.PI_WRAPPER, "the fixture did not inject the stand-in"
    assert stage2.PI_WRAPPER != stage2.PI_TOOLS_DIR / "pi", "the installed Pi would run in a unit test"
    assert shutil.which("pi") == str(sworld.bin / "pi"), "the bare-Pi trap is not what PATH resolves"
    trap = subprocess.run([str(sworld.bin / "pi"), "--version"], capture_output=True, text=True, check=False)
    assert trap.returncode != 0 and "bare pi bypassed" in (trap.stderr + str(trap.stdout)), "the trap does not fire"
    sworld.complete()
    assert sworld.run() == 0
    pinned = str(sworld.bin / "pin-pi")
    infrastructure = [json.loads(line) for line in (sworld.bin / "infrastructure.jsonl").read_text().splitlines()]
    assert {tuple(call["argv"]) for call in infrastructure} == {("--version",)}
    assert all(call["path"] == pinned for call in infrastructure)
    calls = [call for call in sworld.calls() if call["name"] == "pi"]
    assert {call["kind"] for call in calls} == {"finder", "repository", "online"}
    assert all(call["program_path"] == pinned for call in calls)


@pytest.mark.parametrize("klass", ["bounded", "spike"])
def test_small_classes_keep_the_single_explorer(sworld: SwarmWorld, klass: str) -> None:
    # Criterion 2. Planted fault: a small change starts a finder or the swarm judge.
    sworld.research_class(klass)
    sworld.script(
        work=[{"stdout": "A fact from `src/app.py::value`."}],
        finder=[{"stdout": "must not run"}],
        judge=[{"stdout": "must not run"}],
    )
    assert sworld.run() == 0
    assert kinds(sworld) == ["work"]
    explorer = sworld.calls()[0]
    assert model_of(explorer) == "glm-5.3-flash"
    assert explorer["env"]["ANTHROPIC_BASE_URL"] == stage2.GLM_BASE_URL
    text = sworld.research.read_text(encoding="utf-8")
    assert "## Research swarm" not in text and "## Runner exploration" in text


def test_explicit_class_explores_without_spec_or_plan(sworld: SwarmWorld) -> None:
    # Criterion 3. Planted fault: early exploration refuses although the class is stated.
    (sworld.root / "plans/changes/demo/spec.md").unlink()
    (sworld.root / "plans/changes/demo/plan.md").unlink(missing_ok=True)
    sworld.commit()
    sworld.complete()
    assert sworld.run() == 0, "the header's class routes before a spec exists"
    assert sworld.calls()[0]["kind"] == "finder"

    sworld.rewind()
    sworld.research_class(None)
    sworld.script(work=[{"stdout": "A fact."}])
    assert sworld.run("--class", "bounded") == 0, "the explicit argument routes a headerless change"
    assert kinds(sworld) == ["work"]


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
        (sworld.root / "plans/changes/demo/spec.md").write_text(
            "---\ntitle: [unclosed\nbead: demo-1\nclass: bounded\n---\n\n# Spec\n", encoding="utf-8"
        )
    else:
        sworld.research_class("")
    assert sworld.run("--class", "feature") == 2, "an explicit argument does not cure a present invalid header"
    assert sworld.calls() == []
    assert "## Research swarm" not in sworld.research.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Frozen packets, finders, map and sentence (plan step 3; spec criteria 5, 6, 14, 23, 24, 43)
# ---------------------------------------------------------------------------


def test_finders_use_the_repository_seat_selection(sworld: SwarmWorld) -> None:
    # Criteria 6 and 43. Planted fault: a finder runs a model other than its repository seat's selection.
    sworld.selection = selection_for()
    sworld.selection["seats"]["repository"][1] = {"endpoint": "opencode-go", "model": "longcat-2.0"}
    sworld.complete()
    assert sworld.run() == 0
    finders = sworld.calls("finder")
    assert sorted(c["model"] for c in finders) == sorted(["deepseek-v4.1-flash", "longcat-2.0", "claude-haiku-5-5"])
    assert {c["name"] for c in finders} == {"pi", "claude"}
    assert len({c["prompt"] for c in finders}) == 1, "the trio receives the same packet and template"


def test_finder_merge_precedes_every_topic(sworld: SwarmWorld) -> None:
    # Criterion 5. Planted fault: a topic starts before three valid finder results and a validated map.
    sworld.complete()
    assert sworld.run() == 0
    order = kinds(sworld)
    assert order[:5] == ["finder"] * 3 + ["merge", "sentence"]
    assert "repository" not in order[:5] and "online" not in order[:5]
    merge = sworld.calls("merge")[0]
    for seat in REPOSITORY_SEATS:
        assert f"## Finder {seat_id(seat)}" in merge["prompt"]


def test_merge_is_exact_finder_union_with_all_origins(sworld: SwarmWorld) -> None:
    # Criterion 5. Planted fault: a dropped, added or duplicate key dispatches topics, or deduplication
    # loses a finder or reason.
    finders = [seat_id(s) for s in REPOSITORY_SEATS]
    origins = [{"finder": f, "reason": "holds the value"} for f in finders]
    good = {
        "code": [{"path": "src/app.py", "reference": "value", "origins": origins}],
        "rules": [{"path": "AGENTS.md", "reference": "Agent rules", "origins": [dict(o, reason="the rules") for o in origins]}],
        "tests": [{"not_read": [dict(o, reason="the fixture has no tests") for o in origins]}],
        "neighbours": [{"not_read": [dict(o, reason="no neighbour was found") for o in origins]}],
    }  # fmt: skip
    dropped = dict(good, code=[{"not_read": [dict(o, reason="gone") for o in origins]}])
    added = dict(good, code=[*good["code"], {"path": "src/other.py", "reference": "x", "origins": origins}])
    lost_origin = dict(good, code=[{**good["code"][0], "origins": origins[:2]}])
    for bad in (dropped, added, lost_origin):
        sworld.rewind()
        sworld.complete(merge=[{"stdout": json.dumps(bad)}])
        assert sworld.run() == 1
        assert kinds(sworld) == ["finder"] * 3 + ["merge"], "no sentence or topic starts after a bad merge"
        assert "incomplete" in status_line(sworld.research.read_text(encoding="utf-8"))
    sworld.rewind()
    sworld.complete(merge=[{"stdout": json.dumps(good)}])
    assert sworld.run() == 0


@pytest.mark.parametrize("fault", ["finder-exit", "finder-bad-json", "merge-exit", "sentence-exit"])
def test_preparatory_failure_prevents_dependent_stages(sworld: SwarmWorld, fault: str) -> None:
    # Criterion 18. Planted fault: a failed finder, merge or sentence still dispatches a later stage.
    steps = {
        "finder-exit": {"finder:None:mimo-v2.6-flash": [{"exit": 3, "stderr": "boom"}]},
        "finder-bad-json": {"finder:None:claude-haiku-5-5": [{"stdout": "not a locator list"}]},
        "merge-exit": {"merge": [{"exit": 1}]},
        "sentence-exit": {"sentence": [{"exit": 1}]},
    }[fault]
    sworld.complete(**steps)
    assert sworld.run() == 1
    seen = kinds(sworld)
    cut = {
        "finder-exit": ["finder"] * 3,
        "finder-bad-json": ["finder"] * 3,
        "merge-exit": ["finder"] * 3 + ["merge"],
        "sentence-exit": ["finder"] * 3 + ["merge", "sentence"],
    }[fault]
    assert seen == cut
    text = sworld.research.read_text(encoding="utf-8")
    assert "incomplete" in status_line(text) and "Audit" in text, "partial evidence stays in research.md"


def test_all_opus_roles_have_empty_tools_and_packet_only_context(sworld: SwarmWorld) -> None:
    # Criteria 5, 14, 23. Planted fault: the merge, the sentence author or the judge has any tool.
    sworld.complete()
    assert sworld.run() == 0
    expected = {"merge": "xhigh", "sentence": "high", "judge": "xhigh"}
    for kind, effort in expected.items():
        (call,) = sworld.calls(kind)
        argv = call["argv"]
        assert argv[argv.index("--tools") + 1] == "", f"{kind} has a tool list"
        assert {"--restricted", "--safe-mode", "--strict-mcp-config"} <= set(argv)
        assert argv[argv.index("--model") + 1] == "claude-opus-5-5"
        assert argv[argv.index("--effort") + 1] == effort
        assert Path(call["cwd"]) != sworld.root, f"{kind} starts inside the repository"


@pytest.mark.parametrize(
    "sentence",
    [
        TOPIC_OK,
        "KI-Agenten-Läufe in isolierten Umgebungen",
        "Isolation, Prüfung und Wiederherstellung für Agentenläufe.",
        "multi-agent isolation – a practice (with “quotes”) and «guillemets»?",
        "teams' own isolation and don’t forget recovery",
    ],
)
def test_public_sentence_allow_list_accepts(sentence: str) -> None:
    # Criterion 23. Planted fault: the allowed German examples or separators are refused.
    assert stage2_research_run.public_sentence_problems(sentence, "demo", "demo-1", {"src/app.py"}) == []


@pytest.mark.parametrize(
    "sentence",
    [
        "",
        "see src/app.py for the isolation",
        "isolation for demo-1 runs",
        "the research-swarm project",
        "isolation [of] runs",
        "runs {x}",
        "mail me @ home",
        "a = b",
        "isolation 2 runs",
        "snake_case runs",
        "one sentence. and another",
        "stand - alone hyphen",
        "double--hyphen runs",
        "a dash—without spaces",
        "mixedCase inside a word",
        "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
        "seventeen eighteen nineteen twenty twentyone",
        "colon: here",
        "`ticks`",
    ],
)
def test_public_sentence_allow_list_refuses(sentence: str) -> None:
    # Criterion 23. Planted fault: digits, paths, brackets, change or bead names, or loose punctuation pass.
    found = stage2_research_run.public_sentence_problems(
        sentence, "research-swarm", "demo-1", {"src/app.py", "plans/changes/research-swarm/spec.md"}
    )
    assert found, f"{sentence!r} must be refused"


def test_public_topic_is_filtered_before_online_calls(sworld: SwarmWorld) -> None:
    # Criterion 23. Planted fault: a rejected sentence still dispatches topics, or exits other than 1.
    sworld.complete(sentence=[{"stdout": "see src/app.py for runs"}])
    assert sworld.run() == 1
    assert kinds(sworld) == ["finder"] * 3 + ["merge", "sentence"]
    assert "rejected" in sworld.research.read_text(encoding="utf-8")


def test_map_resolution_excludes_unresolved_and_inserts_given_neighbours(sworld: SwarmWorld) -> None:
    # Criteria 24, 29. Planted fault: live-tree resolution grants scope, a given neighbour vanishes.
    other = sworld.root / "plans/changes/other"
    other.mkdir()
    (other / "spec.md").write_text("---\ntitle: Other\nbead: o-1\n---\n\n# Other\n", encoding="utf-8")
    text = sworld.research.read_text(encoding="utf-8").replace(
        "neighbours: []", "neighbours: [plans/changes/other/spec.md]"
    )
    sworld.research.write_text(text, encoding="utf-8")
    sworld.commit()
    rel = "plans/changes/other/spec.md"
    entries = {
        "code": [{"path": "src/app.py", "reference": "no_such_symbol", "reason": "a guess"}],
        "rules": [{"path": "AGENTS.md", "reference": "Agent rules", "reason": "the rules"}],
        "tests": [{"not_read": "none"}],
        "neighbours": [{"not_read": "none"}],
    }
    sworld.complete(
        finder=[{"stdout": json.dumps(entries)}],
        **{"repository:5": [{"stdout": repository_report(5, [rel])}]},
    )
    assert sworld.run() == 0
    block = sworld.research.read_text(encoding="utf-8")
    found = re.search(r"```research-swarm/v2 map\n(.*?)\n```", block, re.S)
    assert found
    packet = json.loads(found.group(1))
    unresolved = [e for e in packet["entries"] if e["status"] == "unresolved"]
    assert [e["reference"] for e in unresolved] == ["no_such_symbol"]
    assert ["code", "src/app.py", "no_such_symbol"] not in packet["scope"], "an unresolved locator grants no scope"
    assert packet["neighbours"] == [{"path": rel, "status": "given", "map_keys": []}]
    topic5 = sworld.calls("repository")
    topic5 = [c for c in topic5 if c["topic"] == 5]
    assert len(topic5) == 3 and all(rel in c["prompt"] for c in topic5), "the packet carries the given neighbour"


def test_history_collection_failure_prevents_all_topics(sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch) -> None:
    # Criterion 18. Planted fault: failed read-only git collection starts a topic.
    def fail(*_a, **_k):
        raise stage2_research_run.ResearchHistoryError("git said no")

    monkeypatch.setattr(stage2_research_run, "build_research_history", fail)
    sworld.complete()
    assert sworld.run() == 1
    assert kinds(sworld) == ["finder"] * 3 + ["merge", "sentence"]
    assert "git said no" in sworld.research.read_text(encoding="utf-8")


def test_frozen_copies_are_scratch_only_and_removed_after_run(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criterion 16. Planted fault: success or abort retains the copies, or copying fails yet models launch.
    seen: list[Path] = []
    real = stage2_research_run.freeze_research_state

    def spy(*args, **kwargs):
        state = real(*args, **kwargs)
        seen.append(state.directory)
        assert not state.directory.resolve().is_relative_to(sworld.root), "copies stay outside the repository"
        return state

    monkeypatch.setattr(stage2_research_run, "freeze_research_state", spy)
    sworld.complete()
    assert sworld.run() == 0
    assert len(seen) == 1 and not seen[0].exists()
    sworld.rewind()
    sworld.complete(merge=[{"exit": 1}])
    assert sworld.run() == 1
    assert len(seen) == 2 and not seen[1].exists()
    sworld.rewind()

    def broken(*_a, **_k):
        raise stage2_research_run.ResearchSnapshotError("cannot copy")

    monkeypatch.setattr(stage2_research_run, "freeze_research_state", broken)
    assert sworld.run() == 1
    assert kinds(sworld) == [], "a failed freeze launches no model"


# ---------------------------------------------------------------------------
# Topics, free seats and the judge (plan steps 3, 4, 5; spec criteria 6, 7, 10, 14, 19, 26, 28, 37, 39)
# ---------------------------------------------------------------------------

FREE = ["alpha-free", "beta-free"]


def test_selected_free_models_cover_all_online_topics_on_identical_briefs(sworld: SwarmWorld) -> None:
    # Criteria 19, 26, 39. Planted fault: an extra invocation or retry, differing peer briefs, a missing free seat.
    sworld.selection = selection_for(free=FREE)
    sworld.complete()
    assert sworld.run() == 0
    assert len(sworld.calls()) == 39 + 3 * len(FREE)
    for topic in range(1, 12):
        calls = [c for c in sworld.calls() if c["topic"] == topic and c["kind"] in ("repository", "online")]
        assert len({c["prompt"] for c in calls}) == 1, f"topic {topic} peers received different briefs"
        assert len(calls) == (3 if topic <= 8 else 5)
    free = [c for c in sworld.calls("online") if c["model"] in FREE]
    assert sorted((c["topic"], c["model"]) for c in free) == sorted((t, m) for t in (9, 10, 11) for m in FREE)


def test_repository_topics_have_three_independent_models(sworld: SwarmWorld) -> None:
    # Criteria 6, 37. Planted fault: a seat runs another model, one session supplies two seats.
    sworld.complete()
    assert sworld.run() == 0
    for topic in range(1, 9):
        assert sorted(models(sworld, "repository", topic)) == sorted(s["model"] for s in REPOSITORY_SEATS)
    for topic in (9, 10, 11):
        assert sorted(models(sworld, "online", topic)) == sorted(s["model"] for s in ONLINE_SEATS)
    assert all(c["name"] == "pi" for c in sworld.calls("online")), "online seats ride Pi, never Claude Code"


def test_free_seats_are_forbidden_in_every_private_role(sworld: SwarmWorld) -> None:
    # Criterion 11. Planted fault: a free model fills a finder, repository, merge, sentence or judge role.
    sworld.selection = selection_for(free=FREE)
    sworld.complete()
    assert sworld.run() == 0
    for call in sworld.calls():
        if call["kind"] != "online":
            assert call["model"] not in FREE


def test_measured_empty_catalog_keeps_all_required_slots(sworld: SwarmWorld) -> None:
    # Criteria 39, 42. Planted fault: a valid zero selection is refused or drops a required slot.
    sworld.selection = selection_for(free=[])
    sworld.complete()
    assert sworld.run() == 0
    assert len(sworld.calls()) == 39


def test_the_next_run_uses_its_own_frozen_free_selection(sworld: SwarmWorld) -> None:
    # Criterion 38. Planted fault: the first run's roster survives into the next run.
    sworld.selection = selection_for(free=FREE)
    sworld.complete()
    assert sworld.run() == 0
    assert len(sworld.calls()) == 45
    sworld.rewind()
    sworld.selection = selection_for(free=["gamma-free"])
    assert sworld.run() == 0
    assert len(sworld.calls()) == 42
    assert {c["model"] for c in sworld.calls("online")} >= {"gamma-free"}
    assert not ({"alpha-free", "beta-free"} & {c["model"] for c in sworld.calls()})


def test_online_requests_exclude_private_inputs_and_ambient_paths(sworld: SwarmWorld) -> None:
    # Criterion 8. Planted fault: a canary from rules, paths, identifiers, finder output, history or private
    # reports appears in an online payload; the call starts in the repository or carries identity.
    (sworld.root / "AGENTS.md").write_text("# Agent rules\n\nCANARY-RULE-TEXT stays private.\n", encoding="utf-8")
    sworld.commit()
    sworld.selection = selection_for(free=FREE)
    sworld.complete()
    assert sworld.run() == 0
    online = sworld.calls("online")
    assert len(online) == 15
    for call in online:
        blob = call["prompt"] + " ".join(call["argv"]) + json.dumps(call["env"])
        for canary in (
            "CANARY-RULE-TEXT",
            "seed fact",
            "src/app.py",
            "AGENTS.md",
            "demo-1",
            "plans/changes",
            str(sworld.root),
        ):
            assert canary not in blob, f"{canary!r} reached an online seat"
        assert TOPIC_OK in call["prompt"]
        assert call["cwd"] != str(sworld.root)
        assert (
            "--tools" in call["argv"]
            and call["argv"][call["argv"].index("--tools") + 1] == "public_search,public_fetch"
        )
        assert call["env"].get("OPENCODE_API_KEY") == OKEY
        assert not {"USER", "LOGNAME", "SHELL"} & set(call["env"]), "no user identity reaches an online seat"
    for call in sworld.calls("repository") + sworld.calls("finder"):
        assert "CANARY-RULE-TEXT" in call["prompt"], "repository seats embed the identical rules file"


def test_peers_receive_identical_frozen_briefs_without_reports(sworld: SwarmWorld) -> None:
    # Criterion 26. Planted fault: a topic prompt carries a peer's or an earlier topic's report text.
    marker = "PEER-REPORT-MARKER"
    report = json.loads(repository_report(1))
    report["claims"][0]["statement"] = marker
    sworld.complete(**{"repository:1": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    for call in sworld.calls():
        if call["kind"] != "judge":
            assert marker not in call["prompt"], f"{call['kind']} read a report early"
    assert marker in sworld.calls("judge")[0]["prompt"]


def test_online_claims_require_successful_page_receipts(sworld: SwarmWorld) -> None:
    # Criterion 10. Planted fault: a search-only or snippet receipt supports a claim, or a receiptless
    # report is accepted.
    for receipts in ([], [dict(RECEIPT, kind="search")], [dict(RECEIPT, status=404)]):
        sworld.rewind()
        sworld.complete(online=[{"stdout": online_report(), "receipts": receipts}])
        assert sworld.run() == 1, f"receipts {receipts} must not back the claim"
        assert "judge" not in kinds(sworld)


def test_unsupported_claims_are_retained_and_report_requires_evidence(sworld: SwarmWorld) -> None:
    # Criterion 10. Planted fault: one bad claim fails a valid report, or an unsupported claim is promoted.
    report = json.loads(repository_report(2))
    report["claims"].append(
        dict(report["claims"][0], id="C2", evidence=["src/app.py::value", "src/app.py::no_such_symbol"])
    )
    sworld.complete(**{"repository:2": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    assert '"evidence_status": "unsupported"' in text
    judge = sworld.calls("judge")[0]["prompt"]
    assert judge.count('"evidence_status": "unsupported"') == 3, "the unsupported claim of each of the 3 seats stays"
    only = json.loads(repository_report(2))
    only["claims"][0]["evidence"] = ["src/app.py::no_such_symbol"]
    sworld.rewind()
    sworld.complete(**{"repository:2": [{"stdout": json.dumps(only)}]})
    assert sworld.run() == 1, "a report whose only claim is unsupported fails the evidence floor"
    assert "judge" not in kinds(sworld)


def test_report_template_refuses_missing_fields_and_eighth_claim(sworld: SwarmWorld) -> None:
    # Criterion 27. Planted fault: required fields are missing or an eighth claim passes.
    base = json.loads(repository_report(4))
    missing = {k: v for k, v in base.items() if k != "counter_evidence"}
    many = dict(base, claims=[dict(base["claims"][0], id=f"C{n}") for n in range(1, 9)])
    for bad in (missing, many):
        sworld.rewind()
        sworld.complete(**{"repository:4:mimo-v2.6-flash": [{"stdout": json.dumps(bad)}]})
        assert sworld.run() == 1
        assert "judge" not in kinds(sworld)
        assert "invalid-report" in sworld.research.read_text(encoding="utf-8")


def test_topic_specific_class_and_volatile_fields_are_required(sworld: SwarmWorld) -> None:
    # Criterion 35. Planted fault: topic 3 omits its class, or a volatile topic-6 claim omits governance.
    t3 = json.loads(repository_report(3))
    del t3["class_assessment"]
    t6 = json.loads(repository_report(6))
    t6["claims"][0]["volatile"] = True
    for key, bad in (("repository:3", t3), ("repository:6", t6)):
        sworld.rewind()
        sworld.complete(**{key: [{"stdout": json.dumps(bad)}]})
        assert sworld.run() == 1


def given_neighbour(world: SwarmWorld) -> str:
    other = world.root / "plans/changes/other"
    other.mkdir(exist_ok=True)
    (other / "spec.md").write_text("---\ntitle: Other\nbead: o-1\n---\n\n# Other\n", encoding="utf-8")
    rel = "plans/changes/other/spec.md"
    text = world.research.read_text(encoding="utf-8").replace("neighbours: []", f"neighbours: [{rel}]")
    world.research.write_text(text, encoding="utf-8")
    world.commit()
    return rel


def test_topic_five_relations_cover_exact_packet_neighbours(sworld: SwarmWorld) -> None:
    # Criterion 27. Planted fault: missing, extra or duplicate relation paths, or dangling claims, pass.
    rel = given_neighbour(sworld)
    good = json.loads(repository_report(5, [rel]))
    for bad_relations in [
        [],  # the packet neighbour has no relation
        [{"path": rel, "relation": "related", "claims": ["C1"]}, {"path": rel, "relation": "unrelated", "claims": ["C1"]}],
        [{"path": rel, "relation": "related", "claims": ["C1"]}, {"path": "plans/changes/x/spec.md", "relation": "related", "claims": ["C1"]}],
        [{"path": rel, "relation": "related", "claims": ["C9"]}],
    ]:  # fmt: skip
        sworld.rewind()
        sworld.research.write_text(
            sworld.research.read_text(encoding="utf-8").replace("neighbours: []", f"neighbours: [{rel}]"),
            encoding="utf-8",
        )
        sworld.complete(**{"repository:5": [{"stdout": json.dumps(dict(good, neighbour_relations=bad_relations))}]})
        assert sworld.run() == 1
        assert "judge" not in kinds(sworld)
    sworld.rewind()
    sworld.research.write_text(
        sworld.research.read_text(encoding="utf-8").replace("neighbours: []", f"neighbours: [{rel}]"), encoding="utf-8"
    )
    sworld.complete(**{"repository:5": [{"stdout": json.dumps(good)}]})
    assert sworld.run() == 0


def test_empty_neighbour_topic_runs_three_seats_without_invented_evidence(sworld: SwarmWorld) -> None:
    # Criteria 7, 18, 27. Planted fault: an empty packet lacks its marker or comparison gap, admits relations,
    # or prevents completion.
    sworld.complete(**{"repository:5": [{"stdout": repository_report(5, ["plans/changes/other/spec.md"])}]})
    assert sworld.run() == 1, "a relation for a path outside the empty packet is an extra path"
    sworld.rewind()
    report = json.loads(repository_report(5))
    report["not_read"] = ["tests"]
    sworld.complete(**{"repository:5": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 1, "an empty packet needs its exact not-read marker"
    sworld.rewind()
    noclaims = json.loads(repository_report(5))
    noclaims["claims"], noclaims["questions"] = [], []
    sworld.complete(**{"repository:5": [{"stdout": json.dumps(noclaims)}]})
    assert sworld.run() == 0, "the empty packet waives the evidence floor"
    topic5 = [c for c in sworld.calls("repository") if c["topic"] == 5]
    assert len(topic5) == 3 and all("no packet neighbour" in c["prompt"] for c in topic5)
    assert len(sworld.calls("repository")) == 24, "the 39 fixed slots stay"


def test_every_failed_slot_keeps_partial_output_before_cleanup(sworld: SwarmWorld) -> None:
    # Criteria 14, 18. Planted fault: missing required reports still reach the judge.
    sworld.complete(**{"repository:4:mimo-v2.6-flash": [{"exit": 2, "stderr": "provider down", "stdout": "half"}]})
    assert sworld.run() == 1
    assert "judge" not in kinds(sworld)
    assert len(sworld.calls()) == 39 - 1, "siblings finish; only the judge is withheld"
    text = sworld.research.read_text(encoding="utf-8")
    assert "topic 4" in text and "failed" in text
    partial = re.findall(r"```research-swarm/v2 partial\n(.*?)\n```", text, re.S)
    assert any("half" in item and "provider down" in item for item in map(str, partial)), "partial output is kept"


def test_failed_free_seat_is_named_without_failing_completion(sworld: SwarmWorld) -> None:
    # Criterion 18. Planted fault: a free failure vanishes or fails an otherwise valid run.
    sworld.selection = selection_for(free=FREE)
    sworld.complete(**{"online:10:beta-free": [{"exit": 1}]})
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    assert "best-effort free seats did not finish" in text and "topics-10-free-beta-free" in text
    assert "judge" in kinds(sworld)
    packet = sworld.calls("judge")[0]["prompt"]
    assert "beta-free" in packet, "the failed free seat is named to the judge"


def test_fresh_opus_reconciles_eleven_topics_and_map(sworld: SwarmWorld) -> None:
    # Criteria 14, 28. Planted fault: another model judges, a valid claim lacks its exclusive disposition.
    sworld.complete()
    assert sworld.run() == 0
    (judge,) = sworld.calls("judge")
    assert model_of(judge) == "claude-opus-5-5"
    for topic in range(1, 12):
        assert f'"topic": {topic}' in judge["prompt"]
    sworld.rewind()
    sworld.complete(judge=[{"stdout": json.dumps({"claim_judgements": []})}])
    assert sworld.run() == 1, "an answer without the closed fields or any judgement is refused"
    assert "failed validation" in sworld.research.read_text(encoding="utf-8")


def test_judge_packet_limit_refuses_before_launch_without_shortening(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criteria 14, 18. Planted fault: J+1 reaches the judge, or a second call/N reduction occurs.
    import stage2_research_judge

    policy = stage2_research_judge.research_judge_capacity_policy()
    monkeypatch.setattr(
        stage2_research_judge, "research_judge_capacity_policy", lambda: dict(policy, limit_characters=10)
    )
    sworld.complete()
    assert sworld.run() == 1
    assert "judge" not in kinds(sworld) and len(sworld.calls()) == 39 - 1
    assert "judge-packet-over-limit" in sworld.research.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Dispatch behaviour inside the run (plan step 4; spec criteria 12, 13, 19, 36)
# ---------------------------------------------------------------------------


def test_a_leak_in_the_first_prompt_starts_no_model(sworld: SwarmWorld) -> None:
    # Criterion 12. Planted fault: a blocked prompt still starts a model, or the secret reaches research.md.
    sworld.research.write_text(SEED + f"\nAn accident: {LEAK}.\n", encoding="utf-8")
    sworld.complete()
    assert sworld.run() == 2
    assert sworld.calls() == [], "a blocked prompt starts no model"
    text = sworld.research.read_text(encoding="utf-8")
    assert "refused" in text and LEAK not in text.split("## Research swarm")[1]


def test_leak_block_cancels_queued_dispatch(sworld: SwarmWorld) -> None:
    # Criteria 12, 36. Planted fault: a queued call starts after BLOCK, a running child is awaited instead of
    # stopped, partial output is lost instead of kept as cancelled, or exit 1 overrides exit 2.
    sleeper = {"stdout": repository_report(1), "sleep": 20}
    planter = {"stdout": repository_report(1), "sleep": 20, "plant": {"leak.txt": f"{LEAK}\n"}}
    sworld.complete(
        repository=[sleeper],
        **{"repository:1:deepseek-v4.1-flash": [planter]},
    )
    assert sworld.run() == 2
    started = sworld.calls("repository")
    assert 1 <= len(started) < 24, "queued topic slots never started"
    text = sworld.research.read_text(encoding="utf-8")
    assert "refused" in text and "cancelled" in text
    assert "judge" not in kinds(sworld)


def test_concurrent_slots_keep_distinct_audits_and_outcomes(sworld: SwarmWorld) -> None:
    # Criteria 13, 36. Planted fault: output cannot be assigned to a slot; a fifth Go call runs at once.
    sworld.complete(
        online=[{"stdout": online_report(), "receipts": [RECEIPT], "sleep": 0.4}],
        repository=[{"stdout": repository_report(1), "sleep": 0.2}],
        **{f"repository:{n}": [{"stdout": repository_report(n), "sleep": 0.2}] for n in range(1, 9)},
    )
    sworld.selection = selection_for(free=FREE)
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    audit = [line for line in text.splitlines() if line.startswith("- Stage-2 call")]
    assert len(audit) == len(sworld.calls())
    keys = {
        (re.search(r"swarm (\w+)", line).group(1), line.split(" · ")[1], re.search(r"model (\S+)", line).group(1))
        for line in audit
    }
    assert len(keys) == len(audit), "each audit line names its own slot"  # noqa: E501
    outcomes = [line for line in text.splitlines() if line.startswith("- Swarm outcome")]
    assert len(outcomes) == len(audit)
    go = [c for c in sworld.calls() if c["name"] == "pi"]
    spans = [(c["t0"], c["t0"] + c["sleep"]) for c in go]
    peak = max(sum(1 for lo, hi in spans if lo <= start < hi) for start, _ in spans)
    assert peak <= 4 and len(go) > 4, f"Go calls overlapped {peak} at a time"


def test_required_slots_precede_free_and_reserve_judge_time(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criterion 19. Planted fault: topic work consumes the judge reserve, or unlaunched slots lack outcomes.
    offset = [0.0]
    real_history = stage2_research_run.build_research_history

    def late(*args, **kwargs):
        offset[0] += 140 * 60.0  # 10 minutes remain, less than the 15-minute judge reserve
        return real_history(*args, **kwargs)

    monkeypatch.setattr(stage2_research_run, "CLOCK", lambda: __import__("time").monotonic() + offset[0])
    monkeypatch.setattr(stage2_research_run, "build_research_history", late)
    sworld.selection = selection_for(free=FREE)
    sworld.complete()
    assert sworld.run() == 1
    assert kinds(sworld) == ["finder"] * 3 + ["merge", "sentence"], "no topic and no judge launches"
    text = sworld.research.read_text(encoding="utf-8")
    assert text.count("not-started-deadline") >= 33, "every unlaunched slot has an outcome"


def test_required_slots_are_dispatched_before_any_free_slot(sworld: SwarmWorld) -> None:
    # Criterion 19. Planted fault: a free slot is gated ahead of queued required slots.
    sworld.selection = selection_for(free=FREE)
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    audit = [line for line in text.splitlines() if line.startswith("- Stage-2 call") and " · topic " in line]
    free_at = [n for n, line in enumerate(audit) if any(f"model {m} " in line for m in FREE)]
    required_at = [n for n, line in enumerate(audit) if not any(f"model {m} " in line for m in FREE)]
    assert free_at and max(required_at) < min(free_at)


def test_frozen_digest_detects_tracked_and_change_input_edits(sworld: SwarmWorld) -> None:
    # Criterion 16. Planted fault: a mid-run edit of a tracked file still publishes complete.
    sworld.complete(
        **{"finder:None:deepseek-v4.1-flash": [{"stdout": locator_report(), "append": {"src/app.py": "value = 2\n"}}]}
    )
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    assert "the frozen input state changed" in text and "src/app.py" in text
    subprocess.run(["git", "checkout", "--", "src/app.py"], cwd=sworld.root, check=True, capture_output=True)
    sworld.rewind()
    sworld.complete(
        **{
            "finder:None:deepseek-v4.1-flash": [
                {"stdout": locator_report(), "plant": {"plans/changes/demo/decisions.md": "# Q-1 answer\n"}}
            ]
        }
    )
    assert sworld.run() == 1, "a new untracked change input also breaks the frozen state"
    assert "decisions.md" in sworld.research.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Durable results and resume (Q-13; spec criteria 46, 52-58)
# ---------------------------------------------------------------------------


def store_dir(_world: SwarmWorld) -> Path:
    return stage2_research_store.research_dir("demo")


def manifest_of(world: SwarmWorld) -> dict:
    text = world.research.read_text(encoding="utf-8")
    blocks = re.findall(r"```research-swarm/v2 manifest\n(.*?)\n```", text, re.S)
    return json.loads(blocks[-1])


def test_store_paths_and_peer_results_never_reach_a_model(sworld: SwarmWorld) -> None:
    # Criterion 52. Planted fault: a store canary or a stored result reaches a prompt, argv, env or cwd.
    sworld.complete()
    assert sworld.run() == 0
    state = str(Path(store_dir(sworld)).parent.parent.parent)
    for call in sworld.calls():
        blob = json.dumps({k: call[k] for k in ("prompt", "argv", "env", "cwd")})
        assert state not in blob and "research.json" not in blob


def test_a_complete_run_clears_the_store_and_a_second_lock_refuses(sworld: SwarmWorld) -> None:
    # Criteria 53, 57. Planted fault: a complete run's results stay reusable; a held lock is ignored.
    sworld.complete()
    assert sworld.run() == 0
    leftovers = [p for p in store_dir(sworld).iterdir() if p.name != ".lock"]
    assert leftovers == [], "a complete publication clears the store"
    sworld.rewind()
    holder = stage2_research_store.Store(store_dir(sworld))
    holder.acquire_lock()
    try:
        assert sworld.run() == 2
        assert sworld.calls() == []
    finally:
        holder.release_lock()


def test_a_resumed_run_is_a_new_run_within_its_slot_budget(sworld: SwarmWorld) -> None:
    # Criteria 53, 54, 55. Planted fault: a failed or invalid result is reused, a discarded result is
    # unnamed, a resumed run exceeds its budget or loses the source run and times of a reused slot.
    sworld.complete(**{"repository:4:mimo-v2.6-flash": [{"exit": 2}]})
    assert sworld.run() == 1
    first = manifest_of(sworld)
    assert len(sworld.calls()) == 38
    sworld.complete()
    log = sworld.bin / "calls.jsonl"
    log.unlink()
    assert sworld.run() == 0
    second = manifest_of(sworld)
    assert second["run_id"] != first["run_id"], "a resumed run is a new run"
    launched = list(sworld.calls())
    assert [(c["kind"], c["topic"], c["model"]) for c in launched[:-1]] == [("repository", 4, "mimo-v2.6-flash")]
    assert launched[-1]["kind"] == "judge"
    assert len(launched) + sum(1 for s in second["slots"] if s["reused_from"]) == 39, "within the budget"
    reused = [s for s in second["slots"] if s["reused_from"]]
    assert len(reused) == 37 and all(s["reused_from"] == first["run_id"] for s in reused)
    assert {"topics-4-2"} == {s["slot_id"] for s in second["slots"] if not s["reused_from"] and s["stage"] == "topics"}
    assert ["topics-4-2", "outcome"] in second["resume"]["not_reused"], "the failed slot is named with its reason"
    assert second["resume"]["source_run"] == first["run_id"] and second["resume"]["usable"] is True


def test_only_finished_valid_results_are_reused_and_others_are_named(sworld: SwarmWorld) -> None:
    # Criterion 53. Planted fault: an invalid, timed-out or cancelled result is reused or left unnamed.
    sworld.complete(
        **{
            "repository:2:mimo-v2.6-flash": [{"stdout": "not json at all"}],  # an invalid report
            "repository:3:deepseek-v4.1-flash": [{"exit": 5, "stdout": "half"}],  # a failed slot
        }
    )
    assert sworld.run() == 1
    sworld.complete()
    (sworld.bin / "calls.jsonl").unlink()
    assert sworld.run() == 0
    relaunched = sorted((c["topic"], c["model"]) for c in sworld.calls("repository"))
    assert relaunched == [(2, "mimo-v2.6-flash"), (3, "deepseek-v4.1-flash")], "only the unfinished slots run again"
    named = {tuple(item) for item in manifest_of(sworld)["resume"]["not_reused"]}
    assert ("topics-2-2", "outcome") in named and ("topics-3-1", "outcome") in named


def test_reused_and_interrupted_slots_are_marked_in_the_manifest(sworld: SwarmWorld) -> None:
    # Criterion 55. Planted fault: a reused result looks launched by this run, loses its source run or times,
    # or an interrupted source slot is missing.
    sworld.complete(judge=[{"exit": 1}])
    assert sworld.run() == 1
    first = manifest_of(sworld)
    run_dir = store_dir(sworld) / first["run_id"]
    victim = run_dir / "topics-6-1.result.json"
    assert victim.exists()
    victim.unlink()  # a launch record with no result: the slot was interrupted
    sworld.complete()
    (sworld.bin / "calls.jsonl").unlink()
    assert sworld.run() == 0
    second = manifest_of(sworld)
    assert "topics-6-1" in second["resume"]["interrupted"]
    by_id = {s["slot_id"]: s for s in second["slots"]}
    assert by_id["topics-6-1"]["reused_from"] is None and by_id["topics-6-1"]["launched"] is True
    assert by_id["finders-0-1"]["reused_from"] == first["run_id"] and by_id["finders-0-1"]["launched"] is False
    assert by_id["finders-0-1"]["ended_at"], "the original time is kept"


def test_a_foreign_edit_breaks_the_binding_and_reuses_nothing(sworld: SwarmWorld) -> None:
    # Criterion 53. Planted fault: results are reused although a tracked file changed in between.
    sworld.complete(judge=[{"exit": 1}])
    assert sworld.run() == 1
    (sworld.root / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
    sworld.complete()
    (sworld.bin / "calls.jsonl").unlink()
    assert sworld.run() == 0
    assert len(sworld.calls()) == 39, "nothing was reused"
    reasons = manifest_of(sworld)["resume"]
    assert reasons["usable"] is False and any("src/app.py" in r for r in reasons["reasons"])


def test_a_refused_run_is_named_and_never_reused(sworld: SwarmWorld) -> None:
    # Criterion 56. Planted fault: results of a run with a refused slot are reused.
    sworld.research.write_text(SEED + f"\nAn accident: {LEAK}.\n", encoding="utf-8")
    sworld.complete()
    assert sworld.run() == 2
    sworld.research.write_text(SEED, encoding="utf-8")
    (sworld.bin / "calls.jsonl").unlink(missing_ok=True)
    assert sworld.run() == 0
    reasons = manifest_of(sworld)["resume"]
    assert reasons["usable"] is False and any("refused" in r for r in reasons["reasons"])


def test_finder_trio_locates_four_categories_without_judging(sworld: SwarmWorld) -> None:
    # Criterion 24. Planted fault: a fifth locator field passes, or an empty category lacks its unread marker.
    good = json.loads(locator_report())
    bad_fifth = dict(good, code=[{**good["code"][0], "judgement": "this is the right design"}])
    bad_empty = dict(good, tests=[])
    bad_category = {**good, "design": [{"not_read": "x"}]}
    for bad in (bad_fifth, bad_empty, bad_category):
        sworld.rewind()
        sworld.complete(finder=[{"stdout": json.dumps(bad)}])
        assert sworld.run() == 1
        assert kinds(sworld) == ["finder"] * 3, "an invalid locator list stops before the merge"
    finder = sworld.calls("finder")[0]["prompt"]
    assert "do not judge" in finder.lower() or "you do not judge" in finder.lower()


def test_each_topic_uses_its_agreed_questions_and_scope(sworld: SwarmWorld) -> None:
    # Criterion 25. Planted fault: a packet differs from its topic prompt or names another topic's scope.
    sworld.complete()
    assert sworld.run() == 0
    for topic in range(1, 12):
        call = next(c for c in sworld.calls() if c["topic"] == topic and c["kind"] in ("repository", "online"))
        assert stage2_research_run.TOPIC_NAMES[topic] in call["prompt"]
        assert stage2_research_run.TOPIC_SCOPES[topic] in call["prompt"]
        others = [t for t in range(1, 12) if t != topic]
        assert not any(stage2_research_run.TOPIC_SCOPES[t] in call["prompt"] for t in others)


def test_online_topics_use_the_three_online_seat_selections(sworld: SwarmWorld) -> None:
    # Criterion 37. Planted fault: a free model, Claude Code or a model other than the seat's selection
    # supplies one of the nine required online contributions.
    sworld.selection = selection_for(
        free=FREE, online=[*ONLINE_SEATS[:2], {"endpoint": "opencode-go", "model": "longcat-2.0"}]
    )
    sworld.complete()
    assert sworld.run() == 0
    for topic in (9, 10, 11):
        assert set(models(sworld, "online", topic)) == {"deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", *FREE}
    required = [c for c in sworld.calls("online") if c["model"] not in FREE]
    assert len(required) == 9 and all(c["name"] == "pi" for c in required)


def test_selection_is_frozen_for_the_run_and_recorded(sworld: SwarmWorld) -> None:
    # Criterion 46. Planted fault: a failing selected model is replaced, retried or probed again; the manifest
    # lacks the receipt id, the selection or a model's mark.
    sworld.selection = selection_for()
    sworld.selection["seats"]["online"][2] = {
        "endpoint": "opencode-go",
        "model": "longcat-2.0",
        "mark": "substitute for online seat 3",
    }
    sworld.complete(**{"online:11:longcat-2.0": [{"exit": 1}]})
    assert sworld.run() == 1
    assert len(sworld.calls()) == 39 - 1, "the failing model is neither retried nor replaced; only the judge waits"
    manifest = manifest_of(sworld)
    assert manifest["receipt_id"] == "r" * 64
    assert manifest["selection"]["online"][2]["mark"] == "substitute for online seat 3"
    assert manifest["selection"]["repository"] == REPOSITORY_SEATS
    assert [c["model"] for c in sworld.calls("online") if c["topic"] == 11].count("longcat-2.0") == 1


@pytest.mark.parametrize(
    ("header", "problem"),
    [
        ("missing", "no neighbours key"),
        ("null", "neighbours: null"),
        ("scalar", "neighbours: plans/changes/other/spec.md"),
        ("duplicate", "neighbours: [plans/changes/other/spec.md, plans/changes/other/spec.md]"),
        ("escape", "neighbours: [../elsewhere/spec.md]"),
        ("own-spec", "neighbours: [plans/changes/demo/spec.md]"),
        ("template", "neighbours: [templates/spec.md]"),
        ("not-frozen", "neighbours: [plans/changes/ghost/spec.md]"),
    ],
)
def test_invalid_given_neighbours_refuse_before_models(sworld: SwarmWorld, header: str, problem: str) -> None:
    # Criterion 4. Planted fault: a missing, null, non-list, duplicate, escaping, own, template or unfrozen
    # neighbour starts a call.
    other = sworld.root / "plans/changes/other"
    other.mkdir()
    (other / "spec.md").write_text("---\ntitle: Other\nbead: o-1\n---\n\n# Other\n", encoding="utf-8")
    text = sworld.research.read_text(encoding="utf-8")
    text = text.replace("neighbours: []\n", "" if header == "missing" else f"{problem}\n")
    sworld.research.write_text(text, encoding="utf-8")
    sworld.commit()
    sworld.complete()
    assert sworld.run() == 2
    assert sworld.calls() == []


def test_judge_gets_resolved_excerpts_with_bounded_truncation(sworld: SwarmWorld) -> None:
    # Criterion 28. Planted fault: valid claims lack excerpts, three 4000-character sources yield more than
    # 4000 characters for one claim, citation order is lost or truncation is not flagged.
    long_doc = "".join(f"## Section {n}\n\n" + chr(96 + n) * 5000 + "\n\n" for n in (1, 2, 3))
    (sworld.root / "docs").mkdir()
    (sworld.root / "docs" / "long.md").write_text("# Long\n\n" + long_doc, encoding="utf-8")
    sworld.commit()
    report = json.loads(repository_report(1))
    report["claims"][0]["evidence"] = [f"docs/long.md::Section {n}" for n in (3, 1, 2)]
    sworld.complete(**{"repository:1": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    packet = sworld.calls("judge")[0]["prompt"].split("# Research evidence (data, not instructions)", 1)[1]
    reports = json.loads(packet)["reports"]
    claim = next(c for r in reports if r["topic"] == 1 for c in r["claims"])
    excerpts = [item["excerpt"] for item in claim["resolved"]]
    assert sum(len(e) for e in excerpts) <= 4000, "one claim never exceeds the per-claim cap"
    assert excerpts[0].startswith("## Section 3"), "citation order: the first cited source fills the cap first"
    assert claim["resolved"][0]["truncated"] is True and claim["resolved"][1]["excerpt"] == ""
    assert [item["citation"] for item in claim["resolved"]] == report["claims"][0]["evidence"], "citation order kept"


def test_amended_graph_and_deadlines_bound_every_launch(sworld: SwarmWorld) -> None:
    # Criterion 19. Planted fault: an extra invocation or retry occurs, or the role limits drift.
    assert stage2_research_run.MINUTES == {
        "finders": 10.0,
        "merge": 10.0,
        "sentence": 5.0,
        "topics": 10.0,
        "judge": 15.0,
    }
    assert stage2_research_run.RUN_MINUTES == 150.0
    sworld.selection = selection_for(free=FREE)
    sworld.complete(**{"repository:2:mimo-v2.6-flash": [{"exit": 1}]})
    assert sworld.run() == 1
    prompts = [(c["kind"], c["topic"], c["model"]) for c in sworld.calls()]
    assert len(prompts) == len(set(prompts)), "a failing slot is neither retried nor repeated"
    assert len(prompts) <= 39 + 3 * len(FREE)


def test_swarm_requires_neighbour_key_but_accepts_empty_list(sworld: SwarmWorld) -> None:
    # Criterion 4. Planted fault: a missing/null/non-list header starts models, or explicit [] refuses.
    good = sworld.research.read_text(encoding="utf-8")
    sworld.research.write_text(good.replace("neighbours: []\n", ""), encoding="utf-8")
    sworld.commit()
    sworld.complete()
    assert sworld.run() == 2 and sworld.calls() == []
    sworld.research.write_text(good, encoding="utf-8")
    sworld.commit()
    assert sworld.run() == 0


def test_neighbour_paths_use_only_active_archive_and_living_specs(sworld: SwarmWorld) -> None:
    # Criterion 4. Planted fault: a template or a fourth path form starts a call; a valid form refuses.
    for rel in (
        "plans/changes/archive/2026-01-01-old/spec.md",
        "plans/specs/living/spec.md",
        "plans/changes/other/spec.md",
    ):
        folder = sworld.root / Path(rel).parent
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "spec.md").write_text("---\ntitle: S\nbead: s-1\n---\n\n# S\n", encoding="utf-8")
    text = sworld.research.read_text(encoding="utf-8")
    forms = "[plans/changes/archive/2026-01-01-old/spec.md, plans/specs/living/spec.md, plans/changes/other/spec.md]"
    sworld.research.write_text(text.replace("neighbours: []", f"neighbours: {forms}"), encoding="utf-8")
    sworld.commit()
    packet = [
        "plans/changes/archive/2026-01-01-old/spec.md",
        "plans/specs/living/spec.md",
        "plans/changes/other/spec.md",
    ]
    sworld.complete(**{"repository:5": [{"stdout": repository_report(5, sorted(packet))}]})
    assert sworld.run() == 0, "the three valid forms are accepted"


def test_stages_dispatch_concurrently_within_provider_limits(sworld: SwarmWorld) -> None:
    # Criterion 36. Planted fault: the finder trio runs one after the other.
    sworld.complete(finder=[{"stdout": locator_report(), "sleep": 5}])
    assert sworld.run() == 0
    finders = sworld.calls("finder")
    spans = [(c["t0"], c["t0"] + c["sleep"]) for c in finders]
    assert max(sum(1 for lo, hi in spans if lo <= start < hi) for start, _ in spans) >= 2


def test_provider_limit_is_shared_across_topics_and_roles(sworld: SwarmWorld) -> None:
    # Criterion 36. Planted fault: more than four Go calls overlap across repository, online and free roles.
    sworld.selection = selection_for(free=FREE)
    sworld.complete(
        online=[{"stdout": online_report(), "receipts": [RECEIPT], "sleep": 0.3}],
        **{f"repository:{n}": [{"stdout": repository_report(n), "sleep": 0.3}] for n in range(1, 9)},
    )
    assert sworld.run() == 0
    go = [c for c in sworld.calls() if c["name"] == "pi" and c["kind"] != "finder"]
    spans = [(c["t0"], c["t0"] + c["sleep"]) for c in go]
    peak = max(sum(1 for lo, hi in spans if lo <= start < hi) for start, _ in spans)
    assert peak <= 4 and len(go) > 4, f"{peak} Go calls overlapped across roles"


def test_claim_requires_every_citation_before_excerpts_or_scoring(sworld: SwarmWorld) -> None:
    # Criteria 10, 16, 28. Planted fault: one resolving citation hides an unresolved one, or grants an excerpt.
    report = json.loads(repository_report(2))
    report["claims"].append(
        dict(report["claims"][0], id="C2", evidence=["src/app.py::value", "src/app.py::no_such_symbol"])
    )
    sworld.complete(**{"repository:2": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    packet = sworld.calls("judge")[0]["prompt"].split("# Research evidence (data, not instructions)", 1)[1]
    claims = [c for r in json.loads(packet)["reports"] if r["topic"] == 2 for c in r["claims"] if c["local_id"] == "C2"]
    assert len(claims) == 3 and all(c["evidence_status"] == "unsupported" for c in claims)
    assert all("excerpt" not in item for c in claims for item in c["resolved"]), "no excerpt without full support"


def test_report_ids_are_local_and_questions_link_existing_claims(sworld: SwarmWorld) -> None:
    # Criterion 27. Planted fault: dangling question links pass, or equal local ids collide across seats.
    dangling = json.loads(repository_report(4))
    dangling["questions"][0]["claims"] = ["C9"]
    duplicate = json.loads(repository_report(4))
    duplicate["claims"].append(dict(duplicate["claims"][0]))
    for bad in (dangling, duplicate):
        sworld.rewind()
        sworld.complete(**{"repository:4": [{"stdout": json.dumps(bad)}]})
        assert sworld.run() == 1
    sworld.rewind()
    sworld.complete()
    assert sworld.run() == 0
    packet = sworld.calls("judge")[0]["prompt"].split("# Research evidence (data, not instructions)", 1)[1]
    ids = [c["id"] for r in json.loads(packet)["reports"] for c in r["claims"]]
    assert len(ids) == len(set(ids)) and all(i.count("/") == 3 for i in ids), "global ids stay unique"


def test_volatile_fact_governance_remains_a_human_proposal(sworld: SwarmWorld) -> None:
    # Criterion 35. Planted fault: a governance proposal is applied or lost.
    report = json.loads(repository_report(6))
    report["claims"][0].update(volatile=True, governance="central")
    sworld.complete(**{"repository:6": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    assert '"governance": "central"' in sworld.research.read_text(encoding="utf-8")
    done = subprocess.run(["git", "status", "--porcelain"], cwd=sworld.root, capture_output=True, text=True, check=True)
    assert [line.split()[-1] for line in done.stdout.splitlines()] == ["plans/changes/demo/research.md"]


@pytest.mark.parametrize("variant", ["double", "unique-refuted", "missing", "unsupported-judged"])
def test_dispositions_are_exclusive_and_unique_is_supported_subset(sworld: SwarmWorld, variant: str) -> None:
    # Criterion 28. Planted fault: a valid claim has two dispositions or none, unique marks an unsupported
    # disposition, or an unsupported claim is judged.
    report = json.loads(repository_report(2))
    report["claims"].append(dict(report["claims"][0], id="C2", evidence=["src/app.py::no_such_symbol"]))
    sworld.complete(**{"repository:2": [{"stdout": json.dumps(report)}], "judge": [{"stdout": f"AUTO:{variant}"}]})
    assert sworld.run() == 1
    assert "failed validation" in sworld.research.read_text(encoding="utf-8")


def test_model_scores_name_the_claims_they_count(sworld: SwarmWorld) -> None:
    # Criterion 28. Planted fault: a score lacks claim ids, or a failed seat has no named outcome.
    sworld.selection = selection_for(free=FREE)
    sworld.complete(**{"online:10:beta-free": [{"exit": 1}]})
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    block = re.search(r"```research-swarm/v2 reconciliation\n(.*?)\n```", text, re.S)
    assert block
    scores = json.loads(block.group(1))["scores"]
    assert len(scores) == 33 + 3 * len(FREE)
    ok = next(item for item in scores if item["topic"] == 1)
    assert ok["supported"]["count"] == len(ok["supported"]["claims"]) == 1 and ok["unsupported"]["claims"] == []
    failed = [item for item in scores if item["outcome"] != "ok"]
    assert [(item["topic"], item["outcome"]) for item in failed] == [(10, "failed")], "the failed seat is named"


def test_given_and_suggested_neighbours_keep_their_provenance(sworld: SwarmWorld) -> None:
    # Criteria 29, 24. Planted fault: a suggestion becomes authoritative, or a given path vanishes.
    for name in ("other", "third"):
        folder = sworld.root / "plans/changes" / name
        folder.mkdir()
        (folder / "spec.md").write_text(f"---\ntitle: {name}\nbead: x-1\n---\n\n# {name}\n", encoding="utf-8")
    text = sworld.research.read_text(encoding="utf-8")
    sworld.research.write_text(
        text.replace("neighbours: []", "neighbours: [plans/changes/other/spec.md]"), encoding="utf-8"
    )
    sworld.commit()
    suggested = {
        "code": [{"path": "src/app.py", "reference": "value", "reason": "x"}],
        "rules": [{"not_read": "none"}],
        "tests": [{"not_read": "none"}],
        "neighbours": [
            {"path": "plans/changes/other/spec.md", "reference": "other", "reason": "suggested too"},
            {"path": "plans/changes/third/spec.md", "reference": "third", "reason": "only suggested"},
        ],
    }
    packet = ["plans/changes/other/spec.md", "plans/changes/third/spec.md"]
    sworld.complete(
        finder=[{"stdout": json.dumps(suggested)}], **{"repository:5": [{"stdout": repository_report(5, packet)}]}
    )
    assert sworld.run() == 0
    found = re.search(r"```research-swarm/v2 map\n(.*?)\n```", sworld.research.read_text(encoding="utf-8"), re.S)
    neighbours = {item["path"]: item["status"] for item in json.loads(found.group(1))["neighbours"]}
    assert neighbours == {"plans/changes/other/spec.md": "given", "plans/changes/third/spec.md": "suggested"}


def test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps(sworld: SwarmWorld) -> None:
    # Criteria 24, 27, 29. Planted fault: an eligible spec-backed entry is omitted or marked no-spec, an
    # own-change entry gains neighbour status, or a no-spec entry gains a relation.
    other = sworld.root / "plans/changes/other"
    other.mkdir()
    (other / "spec.md").write_text("---\ntitle: o\nbead: o-1\n---\n\n# Other\n", encoding="utf-8")
    (other / "design.md").write_text(
        "---\ntitle: d\nbead: o-1\n---\n\n# Design\n\n## Data model\n\ntext\n", encoding="utf-8"
    )
    (sworld.root / "docs").mkdir()
    (sworld.root / "docs" / "notes.md").write_text("# Notes\n\ntext\n", encoding="utf-8")
    sworld.commit()
    entries = {
        "code": [{"path": "src/app.py", "reference": "value", "reason": "x"}],
        "rules": [{"not_read": "none"}],
        "tests": [{"not_read": "none"}],
        "neighbours": [
            {"path": "plans/changes/other/design.md", "reference": "Data model", "reason": "a sibling design"},
            {"path": "plans/changes/demo/plan.md", "reference": "Plan", "reason": "this change"},
            {"path": "docs/notes.md", "reference": "Notes", "reason": "outside the forms"},
        ],
    }
    sworld.complete(
        finder=[{"stdout": json.dumps(entries)}],
        **{"repository:5": [{"stdout": repository_report(5, ["plans/changes/other/spec.md"])}]},
    )
    assert sworld.run() == 0
    found = re.search(r"```research-swarm/v2 map\n(.*?)\n```", sworld.research.read_text(encoding="utf-8"), re.S)
    record = json.loads(found.group(1))
    by_path = {e["path"]: e for e in record["entries"] if e["category"] == "neighbours"}
    assert by_path["plans/changes/other/design.md"]["neighbour_spec"] == "plans/changes/other/spec.md"
    assert by_path["plans/changes/demo/plan.md"]["neighbour_status"] == "self"
    assert by_path["docs/notes.md"]["neighbour_status"] == "no-spec"
    assert [item["path"] for item in record["neighbours"]] == ["plans/changes/other/spec.md"]
    assert [g["key"][1] for g in record["gaps"]] == ["docs/notes.md"]


def test_history_packet_binds_only_mapped_frozen_head_commits(sworld: SwarmWorld) -> None:
    # Criteria 16, 26. Planted fault: history reaches another topic, or a hash outside the packet is evidence.
    def head() -> str:
        done = subprocess.run(["git", "rev-parse", "HEAD"], cwd=sworld.root, capture_output=True, text=True, check=True)
        return done.stdout.strip()

    (sworld.root / "src" / "unmapped.py").write_text("x = 1\n", encoding="utf-8")
    sworld.commit()
    unmapped = head()
    (sworld.root / "src" / "app.py").write_text("value = 1\n# touched\n", encoding="utf-8")
    sworld.commit()
    mapped = head()
    sworld.complete()
    assert sworld.run() == 0
    topic6 = [c for c in sworld.calls("repository") if c["topic"] == 6]
    assert len({c["prompt"] for c in topic6}) == 1 and mapped in topic6[0]["prompt"]
    assert unmapped not in topic6[0]["prompt"], "a commit touching no mapped path is not in the packet"
    assert not any("frozen_head" in c["prompt"] for c in sworld.calls("repository") if c["topic"] != 6)
    report = json.loads(repository_report(6))
    report["claims"][0]["evidence"] = [mapped]
    report["claims"].append(dict(report["claims"][0], id="C2", evidence=[unmapped]))
    sworld.rewind()
    sworld.complete(**{"repository:6": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    packet = sworld.calls("judge")[0]["prompt"].split("# Research evidence (data, not instructions)", 1)[1]
    claims = {
        c["local_id"]: c["evidence_status"]
        for r in json.loads(packet)["reports"]
        if r["topic"] == 6
        for c in r["claims"]
    }
    assert claims == {"C1": "valid", "C2": "unsupported"}


def test_research_carries_practice_architecture_and_adjacent_spec_comparisons(sworld: SwarmWorld) -> None:
    # Criterion 7. Planted fault: a comparison section or the unread-neighbour gap entry is absent.
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    block = json.loads(re.search(r"```research-swarm/v2 reconciliation\n(.*?)\n```", text, re.S).group(1))
    reconciliation = block["reconciliation"]
    for name in ("practice_comparison", "architecture_comparison", "neighbour_comparison"):
        assert reconciliation[name].strip()
    assert "no neighbour given or found" in reconciliation["neighbour_comparison"]
    for name in ("practice_comparison", "architecture_comparison", "neighbour_comparison"):
        sworld.rewind()
        sworld.complete(judge=[{"stdout": f"AUTO:drop-{name}"}])
        assert sworld.run() == 1, f"a judge answer without {name} is refused"


def test_unresolved_dissent_and_human_questions_survive_reconciliation(sworld: SwarmWorld) -> None:
    # Criterion 15. Planted fault: an unresolved disagreement loses an opposing claim id, or judge output
    # carries a maintainer answer field.
    sworld.complete(judge=[{"stdout": "AUTO:dissent"}])
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    block = json.loads(re.search(r"```research-swarm/v2 reconciliation\n(.*?)\n```", text, re.S).group(1))
    (dissent,) = block["reconciliation"]["disagreements"]
    assert len(set(dissent["claims"])) == 2 and dissent["summary"]
    assert block["reconciliation"]["human_questions"] == ["Which seat is right about the value?"]
    sworld.rewind()
    sworld.complete(judge=[{"stdout": "AUTO:answer-field"}])
    assert sworld.run() == 1, "the judge schema permits no answer field"


@pytest.mark.parametrize(
    "evidence",
    [["src/app.py:1"], ["src/app.py"], ["src/app.py::no_such_symbol"], ["src/app.py::value", "src/app.py:1-2"]],
)
def test_local_citations_name_a_path_and_a_symbol(sworld: SwarmWorld, evidence: list[str]) -> None:
    # Criterion 16. Planted fault: unresolvable or line-only references become supported.
    report = json.loads(repository_report(2))
    report["claims"].append(dict(report["claims"][0], id="C2", evidence=evidence))
    sworld.complete(**{"repository:2": [{"stdout": json.dumps(report)}]})
    assert sworld.run() == 0
    packet = sworld.calls("judge")[0]["prompt"].split("# Research evidence (data, not instructions)", 1)[1]
    claims = {
        c["local_id"]: c["evidence_status"]
        for r in json.loads(packet)["reports"]
        if r["topic"] == 2
        for c in r["claims"]
    }
    assert claims == {"C1": "valid", "C2": "unsupported"}


def test_only_the_runner_appends_research(sworld: SwarmWorld) -> None:
    # Criterion 17. Planted fault: a participant edits a file, rewrites an answer or replaces earlier research.
    seed = sworld.research.read_text(encoding="utf-8")
    sworld.complete()
    assert sworld.run() == 0
    now = sworld.research.read_text(encoding="utf-8")
    stamped_seed = re.sub(r"^updated: .*?$", f"updated: {stage2.today()}", seed, count=1, flags=re.M)
    assert now.startswith(stamped_seed), "only the updated date may change before the append"
    done = subprocess.run(["git", "status", "--porcelain"], cwd=sworld.root, capture_output=True, text=True, check=True)
    assert [line.split()[-1] for line in done.stdout.splitlines()] == ["plans/changes/demo/research.md"]
    sworld.rewind()
    sworld.complete(
        **{
            "finder:None:deepseek-v4.1-flash": [
                {
                    "stdout": locator_report(),
                    "append": {"plans/changes/demo/research.md": "\nA participant wrote here.\n"},
                }
            ]
        }
    )
    assert sworld.run() == 1, "a participant's write to research.md is drift, never a clean run"
    assert "research.md" in sworld.research.read_text(encoding="utf-8").split("status:")[-1]


@pytest.mark.parametrize("kind", ["repository", "online"])
@pytest.mark.parametrize("fault", ["nonzero", "empty", "timeout"])
def test_failed_pi_calls_preserve_partial_evidence(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch, kind: str, fault: str
) -> None:
    # Criteria 18, 21. Planted fault: a failed call loses its partial output or receipts, or reports a clean run.
    receipts = [RECEIPT]
    step = {
        "nonzero": {"stdout": "PARTIAL-TEXT", "exit": 7, "stderr": "provider said no", "receipts": receipts},
        "empty": {"stdout": "", "receipts": receipts},
        "timeout": {"stdout": "PARTIAL-TEXT", "sleep": 30, "receipts": receipts},
    }[fault]
    if fault == "timeout":
        monkeypatch.setitem(stage2_research_run.MINUTES, "topics", 0.03)
    key = f"{kind}:1:deepseek-v4.1-flash" if kind == "repository" else f"{kind}:9:deepseek-v4.1-flash"
    sworld.complete(**{key: [step]})
    assert sworld.run() == 1
    assert "judge" not in kinds(sworld)
    text = sworld.research.read_text(encoding="utf-8")
    assert "incomplete" in status_line(text)
    partial = "\n".join(re.findall(r"```research-swarm/v2 partial\n(.*?)\n```", text, re.S))
    if fault != "empty":
        assert "PARTIAL-TEXT" in partial, "the partial answer is kept"
        assert ("timed-out" if fault == "timeout" else "failed") in partial
    if kind == "online":
        assert "example.com/pattern" in partial or fault == "empty", "the call's receipts are kept"


def test_all_outputs_scrub_every_used_credential(sworld: SwarmWorld, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 21. Planted fault: a planted fragment survives in an answer, receipt, store record or error.
    leaky = json.loads(repository_report(1))
    leaky["claims"][0]["statement"] = "the key is @KEY@ and a fragment @KEY@"
    sworld.complete(
        **{"repository:1": [{"stdout": json.dumps(leaky), "stderr": "token @KEY@ rejected"}]},
        judge=[{"exit": 1, "stdout": "@KEY@", "stderr": "failed with @KEY@"}],
        online=[{"stdout": online_report(), "receipts": [dict(RECEIPT, title="@KEY@")]}],
    )
    assert sworld.run() == 1
    seen = capsys.readouterr()
    blobs = [sworld.research.read_text(encoding="utf-8"), seen.out, seen.err]
    for path in store_dir(sworld).rglob("*"):
        if path.is_file():
            blobs.append(path.read_text(encoding="utf-8", errors="replace"))
    fragment = OKEY[3:15]
    for blob in blobs:
        assert OKEY not in blob and fragment not in blob
    assert any("[credential]" in blob for blob in blobs)


def test_local_citations_bind_to_the_frozen_input_state(sworld: SwarmWorld) -> None:
    # Criterion 16. Planted fault: citations resolve against live bytes, or mid-run edits still publish complete.
    edit = {"src/app.py": "new_symbol = 1\n"}
    report = json.loads(repository_report(1))
    report["claims"].append(dict(report["claims"][0], id="C2", evidence=["src/app.py::new_symbol"]))
    sworld.complete(
        **{
            "finder:None:deepseek-v4.1-flash": [{"stdout": locator_report(), "append": edit}],
            "repository:1": [{"stdout": json.dumps(report)}],
        }
    )
    assert sworld.run() == 1
    assert "judge" in kinds(sworld), "the frozen bytes still back every other claim"
    packet = sworld.calls("judge")[0]["prompt"].split("# Research evidence (data, not instructions)", 1)[1]
    claims = {
        c["local_id"]: c["evidence_status"]
        for r in json.loads(packet)["reports"]
        if r["topic"] == 1
        for c in r["claims"]
    }
    assert claims == {"C1": "valid", "C2": "unsupported"}, "a symbol added mid-run is not in the frozen bytes"
    assert "the frozen input state changed: src/app.py" in sworld.research.read_text(encoding="utf-8")


def test_no_call_starts_once_the_run_deadline_is_spent(sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch) -> None:
    # Criterion 19. Planted fault: a call starts although the whole-run deadline is spent, or a slot has no outcome.
    offset = [0.0]
    real = stage2_research_run.freeze_research_state

    def late(*args, **kwargs):
        state = real(*args, **kwargs)
        offset[0] += 151 * 60.0
        return state

    monkeypatch.setattr(stage2_research_run, "CLOCK", lambda: __import__("time").monotonic() + offset[0])
    monkeypatch.setattr(stage2_research_run, "freeze_research_state", late)
    sworld.complete()
    assert sworld.run() == 1
    assert sworld.calls() == []
    text = sworld.research.read_text(encoding="utf-8")
    assert text.count("not-started-deadline") >= 3


# ---------------------------------------------------------------------------
# The doctrine and the declaration agree (spec, criterion 22)
# ---------------------------------------------------------------------------


def test_amended_doctrine_and_research_roles_agree() -> None:
    # Criterion 22. Planted fault: the Zen roster, the six-topic pairs or a fixed trio return, the preparation or resume
    # step is missing from phase-1 doctrine, the seats do not resolve or the ladder changes.
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    assert stage2_swarm.seat_problems(data) == [], "the declared seats and rule must resolve"
    go = next(entry for entry in data["endpunkte"] if entry["name"] == "opencode-go")
    # After the main sync (#157, ADR 0021) `modelle` is a set the runner orders by `anfragen_5h`, no longer a
    # three-id list: the original three stay in it, and the swarm block adds nothing to it.
    assert {"deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"} <= set(go["modelle"]), (
        "the review ladder lost a member; the swarm block changes it in no way"
    )
    block = data["research_swarm"]
    for removed in ("free_endpoint", "free_roster", "free_focuses", "topic6_free", "flash_endpoint", "flash_pair"):
        assert removed not in block, f"{removed} belongs to the removed Zen transport"
    assert all(endpoint["name"] != "opencode-free" for endpoint in data["endpunkte"]), "the Zen endpoint is gone"
    assert all(endpoint.get("abrechnung") != "free" for endpoint in data["endpunkte"]), "no free billing category"
    stage2_swarm.validate_research_free_policy(block["online_free"])
    assert block["judge"] == block["topic_author"] == "claude-opus-5-5"
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "so does phase 1 now (ADR 0020)" in agents
    assert "the research swarm (ADR 0020" in agents
    workflow = (REPO_ROOT / "docs/WORKFLOW.md").read_text(encoding="utf-8")
    assert "| 1 Explore swarm |" in workflow and "| 1 Explore |" in workflow
    explore_prompt = (REPO_ROOT / "prompts/01-explore.md").read_text(encoding="utf-8")
    assert "Routing by class (ADR 0020)." in explore_prompt
    for free_id in ("longcat-2.5-preview-free", "space-bunny-free", "big-pickle"):
        assert free_id not in workflow and free_id not in agents, "a free id stays out of the review-ladder doctrine"
    docs = {
        "AGENTS.md": agents,
        "docs/WORKFLOW.md": workflow,
        "prompts/01-explore.md": explore_prompt,
    }
    for name, text in docs.items():
        flat_text = " ".join(text.split()).lower()
        for stale in ("six topics", "six pairs", "six reconciled topics", "flash pair", "free roster", "sixteen"):
            assert stale not in flat_text, f"{name} still carries the replaced design: {stale}"
    explore_flat = " ".join(explore_prompt.split())
    for needle in (
        "prepare-explore",
        "--availability-reported",
        "finder",
        "eleven topics",
        "neighbours:",
        "[]",
        "resume",
        "research-handoff",
    ):
        assert needle in explore_flat, f"prompts/01-explore.md lacks '{needle}'"
    workflow_flat = " ".join(workflow.split())
    for needle in (
        "`prepare-explore`",
        "--availability-reported",
        "research-handoff",
        "33 + 3N",
        "resumes",
        "F-1",
        "Twelve verbs exist",
    ):
        assert needle in workflow_flat, f"docs/WORKFLOW.md lacks '{needle}'"
    agents_flat = " ".join(agents.split())
    for needle in ("prepare-explore", "research-handoff", "finder"):
        assert needle in agents_flat, f"AGENTS.md lacks '{needle}'"
    for name, needles in {
        "prompts/01a-interview.md": ("research_items", "research_neighbours", "keep", "no ceiling"),
        "prompts/02-spec.md": ("neighbours:", "Basis", "research_neighbours", "research-handoff"),
        "templates/spec.md": ("neighbours:", "decisions.md#Q-", "Basis"),
    }.items():
        text = " ".join((REPO_ROOT / name).read_text(encoding="utf-8").split())
        for needle in needles:
            assert needle in text, f"{name} lacks '{needle}'"


# ---------------------------------------------------------------------------
# Role identities and per-invocation permissions (plan step 2; spec criteria 11, 37, 40)
# ---------------------------------------------------------------------------


def _declaration() -> dict:
    return yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))


def _selection(substitute: bool = False) -> dict:
    """A consumed seat selection as the receipt holds it; `substitute` swaps one Go seat model for a pool one."""
    online = [
        {"endpoint": "opencode-go", "model": "deepseek-v4.1-flash"},
        {"endpoint": "opencode-go", "model": "mimo-v2.6-flash"},
        {"endpoint": "opencode-go", "model": "longcat-2.0" if substitute else "qwen3.8-flash"},
    ]
    repository = [
        {"endpoint": "opencode-go", "model": "deepseek-v4.1-flash"},
        {"endpoint": "opencode-go", "model": "mimo-v2.6-flash"},
        {"endpoint": "claude-code-plan", "model": "claude-haiku-5-5"},
    ]
    return {"seats": {"repository": repository, "online": online}}


def test_role_launches_read_identities_from_the_frozen_selection_and_declaration() -> None:
    # Criteria 6 and 37 (identity part only). Planted fault: a launch names a model other than its frozen seat.
    data = _declaration()
    state = _selection(substitute=True)
    roles = stage2_availability.research_roles(state, data)
    launches = stage2_swarm.role_launches(data, roles, ["alpha-free", "beta-free"])
    by_role: dict[str, list[dict]] = {}
    for launch in launches:
        by_role.setdefault(launch["role"], []).append(launch)
    assert [(item["endpoint"], item["model"]) for item in by_role["online"]] == [
        (seat["endpoint"], seat["model"]) for seat in state["seats"]["online"]
    ], "an online launch follows the frozen selection, substitute included"
    assert [item["model"] for item in by_role["repository"]] == [seat["model"] for seat in state["seats"]["repository"]]
    assert [item["model"] for item in by_role["online_free"]] == ["alpha-free", "beta-free"]
    programs = {item["role"]: set() for item in launches}
    for item in launches:
        programs[item["role"]].add(item["program"])
    assert programs["online"] == {"pi"} and programs["online_free"] == {"pi"}
    assert programs["repository"] == {"pi", "claude-code"}, (
        "Go seats ride Pi, the Claude Code seat the official program"
    )
    for role in ("finder_merge", "topic_author", "judge"):
        assert programs[role] == {"claude-code"}
        assert all(item["model"].startswith("claude-opus") for item in by_role[role])
    assert {item["data_class"] for item in launches if item["role"].startswith("online")} == {"public-web"}
    assert {item["data_class"] for item in launches if not item["role"].startswith("online")} == {"framework"}


def test_role_permissions_do_not_follow_endpoint_privileges() -> None:
    # Criterion 11. Planted fault: the endpoint's framework permission lets a role carry data it was not given.
    data = _declaration()
    go = next(entry for entry in data["endpunkte"] if entry["name"] == "opencode-go")
    assert "framework" in go["darf_sehen"], "the premise: the Go endpoint itself may see framework content"
    problem = stage2_swarm.invocation_problem
    assert problem(data, "repository", "opencode-go", "deepseek-v4.1-flash") is None
    assert problem(data, "online", "opencode-go", "deepseek-v4.1-flash") is None
    # An online seat never carries the framework packet, however much its endpoint may see.
    assert problem(data, "online", "opencode-go", "deepseek-v4.1-flash", data_class="framework")
    assert problem(
        data, "online_free", "opencode-go", "alpha-free", data_class="framework", selected_free=["alpha-free"]
    )
    # A private role never carries public-only data under a mislabelled class either.
    assert problem(data, "repository", "opencode-go", "deepseek-v4.1-flash", data_class="public-web")
    # A model outside its role's endpoint kind is refused: online seats ride Go, Opus rides Claude Code.
    assert problem(data, "online", "claude-code-plan", "claude-haiku-5-5")
    assert problem(data, "judge", "opencode-go", "deepseek-v4.1-flash")
    assert problem(data, "judge", "claude-code-plan", "claude-haiku-5-5"), "only Opus fills an Opus role"
    assert problem(data, "topic_author", "claude-code-plan", "claude-opus-5-5") is None
    # No program is launched for an endpoint no launcher serves, nor for an unknown role or undeclared model.
    assert problem(data, "repository", "glm-coding-plan", "glm-5.3-flash")
    assert problem(data, "repository", "opencode-go", "ghost-model")
    assert problem(data, "reviewer", "opencode-go", "deepseek-v4.1-flash")
    # An endpoint without a stated residency never serves a private role.
    nameless = _declaration()
    next(e for e in nameless["endpunkte"] if e["name"] == "opencode-go")["residenz"] = "nicht-erklaert"
    assert problem(nameless, "repository", "opencode-go", "deepseek-v4.1-flash")


@pytest.mark.parametrize("role", ["finder", "repository", "finder_merge", "topic_author", "judge", "online"])
def test_dynamic_free_permission_is_public_only(role: str) -> None:
    # Criterion 40. Planted fault: a Go free model fills a private (or paid online) role through the endpoint.
    data = _declaration()
    endpoint = "claude-code-plan" if role in {"finder_merge", "topic_author", "judge"} else "opencode-go"
    # Even when the declaration were to list the free id as an ordinary model, no seat or private role takes it.
    next(e for e in data["endpunkte"] if e["name"] == "opencode-go")["modelle"].append("alpha-free")
    assert stage2_swarm.invocation_problem(data, role, endpoint, "alpha-free", selected_free=["alpha-free"])
    assert stage2_swarm.invocation_problem(data, role, "opencode-go", "alpha-free", selected_free=["alpha-free"])


def test_selected_free_models_ride_only_the_public_role_under_the_policy() -> None:
    # Criteria 39 and 40. Planted fault: an unselected, excluded, off-suffix or off-provider id is launched.
    data = _declaration()
    problem = stage2_swarm.invocation_problem
    assert problem(data, "online_free", "opencode-go", "alpha-free", selected_free=["alpha-free"]) is None
    assert problem(data, "online_free", "opencode-go", "alpha-free", selected_free=[]), "not in this run's selection"
    assert problem(data, "online_free", "opencode-go", "alpha", selected_free=["alpha"]), "no -free suffix"
    assert problem(data, "online_free", "opencode", "alpha-free", selected_free=["alpha-free"]), "another provider"
    assert problem(data, "online_free", "claude-code-plan", "alpha-free", selected_free=["alpha-free"])
    data["research_swarm"]["online_free"]["exclude"] = ["alpha-free"]
    assert problem(data, "online_free", "opencode-go", "alpha-free", selected_free=["alpha-free"]), "exclude wins"
    data["research_swarm"]["online_free"].update(exclude=[], include=["beta-free"])
    assert problem(data, "online_free", "opencode-go", "alpha-free", selected_free=["alpha-free"]), "include narrows"
    assert problem(data, "online_free", "opencode-go", "beta-free", selected_free=["beta-free"]) is None


@pytest.mark.parametrize(
    "policy",
    [
        None,
        {},
        {"provider": "opencode", "suffix": "-free", "include": [], "exclude": []},
        {"provider": "opencode-go", "suffix": "", "include": [], "exclude": []},
        {"provider": "opencode-go", "suffix": "-free", "include": ["paid-flash"], "exclude": []},
        {"provider": "opencode-go", "suffix": "-free", "include": [], "exclude": "a-free"},
        {"provider": "opencode-go", "suffix": "-free", "include": ["a-free", "a-free"], "exclude": []},
        {"provider": "opencode-go", "suffix": "-free", "include": [], "exclude": [], "extra": 1},
    ],
)
def test_malformed_online_free_policy_is_a_declaration_fault(policy: object) -> None:
    # Criterion 39. Planted fault: a malformed or non-free policy reaches a launch instead of exit 2.
    data = _declaration()
    data["research_swarm"]["online_free"] = policy
    roles = stage2_availability.research_roles(_selection(), data)
    with pytest.raises(stage2_swarm.ResearchCatalogError) as caught:
        stage2_swarm.role_launches(data, roles, [])
    assert caught.value.exit_code == 2
    assert stage2_swarm.invocation_problem(data, "online_free", "opencode-go", "a-free", selected_free=["a-free"])


def test_a_role_launch_set_with_one_unpermitted_role_starts_none() -> None:
    # Criterion 11. Planted fault: the set is partly returned, so earlier roles would launch before the refusal.
    data = _declaration()
    state = _selection()
    state["seats"]["repository"][0] = {"endpoint": "glm-coding-plan", "model": "glm-5.3-flash"}
    roles = stage2_availability.research_roles(state, data)
    with pytest.raises(stage2_swarm.ResearchCatalogError) as caught:
        stage2_swarm.role_launches(data, roles, [])
    assert caught.value.exit_code == 2 and "glm-coding-plan" in str(caught.value)


# ---------------------------------------------------------------------------
# Step 8: the runner-derived obligation inventory (criteria 29, 31)
# ---------------------------------------------------------------------------

RUN = "abc123"


def derived_claim(seat: str, local: str, valid: bool = True, topic: int = 5) -> dict:
    return {"id": f"{RUN}/{topic}/{seat}/{local}", "evidence_status": "valid" if valid else "unsupported"}


def derived_report(topic: int, seat: str, *, claims=None, questions=(), assessment=None, relations=None) -> dict:
    report = {
        "topic": topic,
        "seat": seat,
        "claims": claims if claims is not None else [derived_claim(seat, "C1", topic=topic)],
        "questions": [],
    }
    for number, (text, classification, links) in enumerate(questions, 1):
        report["questions"].append(
            {
                "id": f"{RUN}/{topic}/{seat}/Q{number}",
                "question": text,
                "classification": classification,
                "claims": [f"{RUN}/{topic}/{seat}/{link}" for link in links],
            }
        )
    if assessment is not None:
        report["class_assessment"] = {"class": assessment, "claims": [f"{RUN}/{topic}/{seat}/C1"]}
    if relations is not None:
        report["neighbour_relations"] = [
            {"path": path, "relation": relation, "claims": [f"{RUN}/{topic}/{seat}/{c}" for c in links]}
            for path, relation, links in relations
        ]
    return report


NEIGHBOUR = "plans/changes/other/spec.md"
SEATS = ("opencode-go:a", "opencode-go:b", "claude-code-plan:c")


def topic_five(relations_by_seat: dict[str, list], *, invalid: frozenset = frozenset()) -> list[dict]:
    reports = []
    for seat in SEATS:
        claims = [derived_claim(seat, "C1", valid=(seat not in invalid), topic=5), derived_claim(seat, "C2", topic=5)]
        if seat in invalid:
            claims = claims[:1]
        reports.append(derived_report(5, seat, claims=claims, relations=relations_by_seat[seat]))
    return reports


def inventory_of(reports, packet, disagreements=(), declared="feature"):
    import research_handoff

    return research_handoff.derive_inventory(
        run_id=RUN, declared_class=declared, packet=packet, reports=reports, disagreements=list(disagreements)
    )


def status_of(inventory: dict, path: str = NEIGHBOUR) -> str:
    (entry,) = [n for n in inventory["neighbours"] if n["path"] == path]
    return entry["status"]


SUGGESTED = [{"path": NEIGHBOUR, "status": "suggested", "map_keys": []}]
GIVEN = [{"path": NEIGHBOUR, "status": "given", "map_keys": []}]


def relations(*kinds: str) -> dict[str, list]:
    return {seat: [(NEIGHBOUR, kind, ["C1"])] for seat, kind in zip(SEATS, kinds, strict=True)}


def test_neighbour_status_uses_three_relations_and_never_judge_verdict() -> None:
    # Criterion 29, 31. Planted fault: any unrelated seat permits confirmation, three unrelated relations are not
    # rejected, a split or contradicts entry loses its human item, or a judge disposition sets the status.
    for kinds, status in [
        (("related", "related", "related"), "confirmed"),
        (("related", "contradicts", "related"), "confirmed"),
        (("unrelated", "unrelated", "unrelated"), "rejected"),
        (("related", "unrelated", "related"), "split"),
        (("related", "unrelated", "unrelated"), "split"),
    ]:
        inventory = inventory_of(topic_five(relations(*kinds)), SUGGESTED)
        assert status_of(inventory) == status, kinds
        splits = [i for i in inventory["items"] if i.get("kind") == "split"]
        assert bool(splits) == (status == "split"), kinds
    mixed = inventory_of(topic_five(relations("related", "contradicts", "related")), SUGGESTED)
    (contradiction,) = [i for i in mixed["items"] if i.get("kind") == "contradicts"]
    assert contradiction["path"] == NEIGHBOUR and contradiction["reason"] == "neighbour"
    # fewer than three seats is split, never confirmed
    two = topic_five(relations("related", "related", "related"))[:2]
    assert status_of(inventory_of(two, SUGGESTED)) == "split"
    # the derivation takes no judge disposition at all
    import inspect

    import research_handoff

    assert "scores" not in inspect.signature(research_handoff.derive_inventory).parameters
    # a given neighbour stays given, whatever its relations say
    assert status_of(inventory_of(topic_five(relations("unrelated", "unrelated", "unrelated")), GIVEN)) == "given"


def test_neighbour_status_ignores_relations_without_valid_claims() -> None:
    # Criteria 29, 31. Planted fault: unsupported-only evidence confirms or rejects a path, or an unsupported-only
    # contradicts / unrelated-given relation loses its human item.
    only_unsupported = frozenset({SEATS[2]})
    related = topic_five(relations("related", "related", "related"), invalid=only_unsupported)
    inventory = inventory_of(related, SUGGESTED)
    assert status_of(inventory) == "split"
    assert any(i.get("kind") == "split" for i in inventory["items"])
    rows = {r["seat"]: r for r in inventory["neighbours"][0]["relations"]}
    assert rows[SEATS[2]]["counting"] is False and rows[SEATS[0]]["counting"] is True
    unrelated = topic_five(relations("unrelated", "unrelated", "unrelated"), invalid=only_unsupported)
    assert status_of(inventory_of(unrelated, SUGGESTED)) == "split", "three unrelated, one without valid evidence"
    # unsupported-only contradicts and unrelated-given still derive their item
    contradicts = topic_five(relations("related", "related", "contradicts"), invalid=only_unsupported)
    kinds = {i.get("kind") for i in inventory_of(contradicts, SUGGESTED)["items"]}
    assert "contradicts" in kinds
    given = topic_five(relations("related", "related", "unrelated"), invalid=only_unsupported)
    kinds = {i.get("kind") for i in inventory_of(given, GIVEN)["items"]}
    assert "unrelated-given" in kinds


def test_neighbour_relations_derive_items_without_judge_or_question() -> None:
    # Criterion 31. Planted fault: a contradicts or unrelated-given field loses its obligation when Opus omits it.
    reports = topic_five(relations("related", "contradicts", "unrelated"))
    inventory = inventory_of(reports, GIVEN, disagreements=[])
    kinds = {i.get("kind") for i in inventory["items"] if i["reason"] == "neighbour"}
    assert kinds == {"contradicts", "unrelated-given"}
    for item in inventory["items"]:
        assert item["path"] == NEIGHBOUR and item["claims"], "an item keeps its path and source claims"
    ids = [i["id"] for i in inventory["items"]]
    assert ids == sorted(set(ids), key=ids.index) and all(re.fullmatch(r"H-[1-9][0-9]*", i) for i in ids)
    # a suggested path that is rejected cleanly derives nothing
    clean = inventory_of(topic_five(relations("unrelated", "unrelated", "unrelated")), SUGGESTED)
    assert clean["items"] == []


def test_decisions_and_dissent_enter_the_interview_inventory() -> None:
    # Criterion 31. Planted fault: a report decision, a differing class or a judge disagreement is omitted, or
    # grouping duplicates loses a source question or claim id.
    a, b = SEATS[0], SEATS[1]
    reports = [
        derived_report(1, a, questions=[("Which store?", "[DECISION]", ["C1"]), ("Who reads it?", "[GAP]", ["C1"])]),
        derived_report(1, b, questions=[("which   store?", "[DECISION]", ["C1"]), ("Name it", "[DETAIL]", ["C1"])]),
        derived_report(2, a, claims=[derived_claim(a, "C1", False, 2)], questions=[("Keep v1?", "[DECISION]", ["C1"])]),
        derived_report(3, a, assessment="spike"),
        derived_report(3, b, assessment="feature"),
    ]
    inventory = inventory_of(
        reports, [], disagreements=[{"claims": [f"{RUN}/1/{a}/C1", f"{RUN}/1/{b}/C1"], "summary": "seats differ"}]
    )
    by_reason: dict[str, list[dict]] = {}
    for item in inventory["items"]:
        by_reason.setdefault(item["reason"], []).append(item)
    decisions = {tuple(i["questions"]): i for i in by_reason["decision"]}
    grouped = decisions[(f"{RUN}/1/{a}/Q1", f"{RUN}/1/{b}/Q1")]
    assert grouped["claims"] == [f"{RUN}/1/{a}/C1", f"{RUN}/1/{b}/C1"], "duplicates keep every source id"
    assert (f"{RUN}/2/{a}/Q1",) in decisions, "a decision whose claim is unsupported still has an item"
    assert len(by_reason["decision"]) == 2, "gap and detail questions are not obligations"
    (klass,) = by_reason["class"]
    assert "spike" in klass["summary"] and klass["claims"] == [f"{RUN}/3/{a}/C1"]
    (dissent,) = by_reason["disagreement"]
    assert dissent["claims"] == [f"{RUN}/1/{a}/C1", f"{RUN}/1/{b}/C1"]
    assert inventory["declared_class"] == "feature"


def published_blocks(world: SwarmWorld, name: str) -> list[dict]:
    text = world.research.read_text(encoding="utf-8")
    return [json.loads(m) for m in re.findall(rf"```research-swarm/v2 {name}\n(.*?)\n```", text, re.S)]


def decision_report(topic: int, neighbours: list[str] | None = None, *, assessed: str = "feature") -> str:
    report = json.loads(repository_report(topic, neighbours))
    report["questions"] = [
        {"id": "Q1", "question": "Should the store move?", "classification": "[DECISION]", "claims": ["C1"]}
    ]
    if topic == 3:
        report["class_assessment"]["class"] = assessed
    return json.dumps(report)


def test_raw_off_brief_decisions_and_class_mismatches_cannot_disappear(sworld: SwarmWorld) -> None:
    # Criterion 31. Planted fault: judge filtering hides an accepted report decision, or a class mismatch lacks
    # its derived item. The judge here marks every claim off-brief and omits all disagreements.
    sworld.complete(
        judge=[{"stdout": "AUTO:off-brief"}],
        **{
            "repository:2": [{"stdout": decision_report(2)}],
            "repository:3": [{"stdout": decision_report(3, assessed="spike")}],
        },
    )
    assert sworld.run() == 0
    (inventory,) = published_blocks(sworld, "inventory")
    manifest = published_blocks(sworld, "manifest")[0]
    assert inventory["run_id"] == manifest["run_id"] and inventory["declared_class"] == "feature"
    reasons = [item["reason"] for item in inventory["items"]]
    assert reasons.count("class") == 1
    decision_questions = {q for item in inventory["items"] if item["reason"] == "decision" for q in item["questions"]}
    assert len(decision_questions) == 6, "three seats each of topics 2 and 3 keep their decision question"
    assert all(q.startswith(manifest["run_id"] + "/") for q in decision_questions)


def test_the_inventory_is_persisted_in_the_fenced_run_block(sworld: SwarmWorld) -> None:
    # Criteria 29, 31. Planted fault: the runner derives the inventory but never persists it, or persists it
    # outside the one fenced run block.
    rel = given_neighbour(sworld)
    reports = {
        f"repository:5:{model}": [{"stdout": json.dumps(dict(json.loads(repository_report(5, [rel])),
            neighbour_relations=[{"path": rel, "relation": relation, "claims": ["C1"]}]))}]
        for model, relation in (
            ("deepseek-v4.1-flash", "unrelated"), ("mimo-v2.6-flash", "contradicts"), ("claude-haiku-5-5", "related"),
        )
    }  # fmt: skip
    sworld.complete(**reports)
    assert sworld.run() == 0
    (inventory,) = published_blocks(sworld, "inventory")
    assert {i.get("kind") for i in inventory["items"]} == {"contradicts", "unrelated-given"}
    assert [n["status"] for n in inventory["neighbours"]] == ["given"]
    text = sworld.research.read_text(encoding="utf-8")
    start, end = text.index("<!-- research-swarm/v2 run"), text.index("<!-- /research-swarm/v2 -->")
    assert start < text.index("research-swarm/v2 inventory") < end


# ---------------------------------------------------------------------------
# Preparation: catalog, policy and capability rows (spec criteria 38, 39, 41, 42)
# ---------------------------------------------------------------------------
# These drive the real `prepare-explore` verb with the catalog helper replaced by a document of its own
# shape (the helper itself is covered with loopback servers in test_stage2_research_catalog.py).

from test_stage2 import world as _prep_world  # noqa: E402
from test_stage2_research_availability import GO as PREP_GO  # noqa: E402
from test_stage2_research_availability import Fixture as PrepFixture  # noqa: E402
from test_stage2_research_availability import fx as _prep_fx  # noqa: E402
from test_stage2_research_availability import pi_model  # noqa: E402

world = _prep_world  # the fixture `fx` builds on
fx = _prep_fx


def _free_policy(**changes: object):
    def edit(data: dict) -> None:
        data["research_swarm"]["online_free"].update(changes)

    return edit


def _no_model_call_and_no_receipt(fx: PrepFixture) -> None:
    assert fx.w.calls() == [], "a probe or model call started"
    assert not stage2_availability.research_receipt_path("demo", stage2).exists(), "a receipt exists"


@pytest.mark.parametrize(
    "fault", ["pi-timeout", "pi-http-error", "pi-malformed", "pi-duplicate", "no-node", "stale-only"]
)
def test_catalog_failure_stops_before_all_model_calls(
    fx: PrepFixture, monkeypatch: pytest.MonkeyPatch, fault: str
) -> None:
    # Criterion 41. Planted fault: a Pi catalog failure starts a model or probe, falls back to a cached or Zen
    # roster, or exits 0, 2 or 3 instead of 1.
    def broken(_runner, _root):
        bridge = fx.catalog.bridge()
        pi = bridge["sources"]["pi"]
        if fault == "pi-timeout":
            bridge.update(exit_code=1, reason="pi-timeout")
            pi.update(outcome="timeout", status=None)
        elif fault in ("pi-http-error", "stale-only"):
            # Only the cached store is left: the refresh itself did not succeed.
            bridge.update(exit_code=1, reason="pi-refresh-failed")
            pi.update(outcome="http-error", status=500)
        elif fault == "pi-malformed":
            pi["body"] = "{broken"
        elif fault == "pi-duplicate":
            pi["body"] = '[{"id":"deepseek-v4.1-flash","id":"mimo-v2.6-flash"}]'
        else:
            raise stage2.CallFailed("node is not installed; the Go catalog cannot be refreshed and no call starts.")
        return bridge

    monkeypatch.setattr(stage2_availability, "catalog_bridge", broken)
    assert fx.prepare() == 1
    _no_model_call_and_no_receipt(fx)


def test_missing_explicit_include_stops_before_models(fx: PrepFixture) -> None:
    # Criterion 39. Planted fault: a missing included id starts the fixed slots instead of preflight exit 1.
    fx.edit_declaration(_free_policy(include=["absent-free"]))
    assert fx.prepare() == 1
    _no_model_call_and_no_receipt(fx)
    # An id that exists but fails the capability check is just as fatal.
    fx.catalog.tools["alpha-free"]["tool_call"] = False
    fx.edit_declaration(_free_policy(include=["alpha-free"]))
    assert fx.prepare() == 1
    _no_model_call_and_no_receipt(fx)


def test_go_free_policy_filters_and_freezes_each_run(fx: PrepFixture) -> None:
    # Criteria 38, 39. Planted fault: an unselected, off-suffix, tool-less or excluded model is selected, or one run's
    # frozen selection survives into the next preparation.
    fx.catalog.pi += [pi_model("delta-free"), pi_model("epsilon-free"), pi_model("gamma-paid", provider="other")]
    fx.catalog.tools["delta-free"] = {"id": "delta-free", "tool_call": False}
    fx.catalog.tools["epsilon-free"] = {"id": "epsilon-free", "tool_call": True}
    assert fx.prepare() == 0
    first = fx.receipt()["state"]["free"]
    assert first["selected"] == ["alpha-free", "beta-free", "epsilon-free"]
    assert first["policy"] == {"provider": PREP_GO, "suffix": "-free", "include": [], "exclude": []}
    # A narrower policy and a changed catalog give the next run its own selection.
    fx.edit_declaration(_free_policy(exclude=["alpha-free"]))
    fx.catalog.pi = [item for item in fx.catalog.pi if item["id"] != "epsilon-free"]
    assert fx.prepare() == 0
    second = fx.receipt()["state"]["free"]
    assert second["selected"] == ["beta-free"]
    assert second["policy"]["exclude"] == ["alpha-free"]
    fx.edit_declaration(_free_policy(include=["beta-free"]))
    assert fx.prepare() == 0
    assert fx.receipt()["state"]["free"]["selected"] == ["beta-free"]
    chosen = {call["model"] for call in fx.w.calls()}
    assert not chosen & {"alpha-free", "beta-free", "delta-free", "epsilon-free", "gamma-paid"}, (
        "a free model was probed"
    )


def test_capability_unavailable_keeps_required_slots_unless_include_is_required(fx: PrepFixture) -> None:
    # Criterion 42. Planted fault: the default fallback blocks required slots, or an ineligible explicit include
    # starts models.
    for item in fx.catalog.pi:
        if item["id"] == "qwen3.8-flash":
            item["api"] = "openai-completions"  # the preferred seat model needs no substitute pool
    fx.catalog.metadata_ok = False
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert state["free"]["selected"] == []
    assert state["catalog"]["capability_status"] == "capability-unavailable"
    assert state["catalog"]["selection_outcome"] != "measured-empty"
    data = yaml.safe_load((fx.w.root / "model-endpoints.yaml").read_text(encoding="utf-8"))
    consumed = stage2_availability.consume_research(fx.w.root, "demo", fx.receipt()["report_id"], stage2, "feature")
    roles = stage2_availability.research_roles(consumed, data)
    graph = stage2_swarm.research_slot_plan(roles, consumed["free"]["selected"])
    assert len(graph) == 39 and all(slot["required"] for slot in graph)
    # With an explicit include the unavailable capability is fatal and nothing starts.
    before = len(fx.w.calls())
    fx.edit_declaration(_free_policy(include=["alpha-free"]))
    assert fx.prepare() == 1
    assert len(fx.w.calls()) == before, "a model started on an ineligible explicit include"
    assert not stage2_availability.research_receipt_path("demo", stage2).exists()


def test_a_run_longer_than_the_preparation_deadline_still_publishes_complete(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criteria 16, 18 (phase-6 F-11). Planted fault: the publication drift check reuses the expired freezing
    # deadline, so an unchanged tree of a run lasting over 60 seconds ends incomplete.
    import time as real_time

    import stage2_research_snapshot

    offset = [0.0]

    class SkewedTime:
        def __getattr__(self, name: str) -> object:
            return getattr(real_time, name)

        @staticmethod
        def monotonic() -> float:
            return real_time.monotonic() + offset[0]

    real_history = stage2_research_run.build_research_history

    def late(*args, **kwargs):
        offset[0] += 90.0  # past the 60-second preparation deadline, well inside the run budget
        return real_history(*args, **kwargs)

    monkeypatch.setattr(stage2_research_snapshot, "time", SkewedTime())
    monkeypatch.setattr(stage2_research_run, "time", SkewedTime())
    monkeypatch.setattr(stage2_research_run, "build_research_history", late)
    sworld.complete()
    assert sworld.run() == 0
    text = sworld.research.read_text(encoding="utf-8")
    assert "drift check failed" not in text and manifest_of(sworld)["status"] == "complete"


def test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criteria 18, 57 (phase-6 F-15). Planted fault: after the first failed terminal write the siblings'
    # outcomes are dropped from the record, or a failed binding write loses the incomplete publication.
    def broken(*_args, **_kwargs):
        raise stage2_research_store.StoreWriteError("disk full")

    monkeypatch.setattr(stage2_research_store.Store, "write_result", broken)
    monkeypatch.setattr(stage2_research_store.Store, "set_append", broken)
    sworld.complete()
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    slots = {s["slot_id"]: s for s in manifest_of(sworld)["slots"]}
    assert manifest_of(sworld)["status"].startswith("incomplete") and "state-store-unwritable" in text
    finders = [s for sid, s in slots.items() if sid.startswith("finders-")]
    assert len(finders) == 3 and all(s["outcome"] for s in finders), "every finder keeps its terminal outcome"


def test_a_failed_append_binding_write_ends_incomplete_with_exit_one(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criterion 57 (phase-6 F-20). Planted fault: a failure writing only the research-append binding is
    # suppressed, so the run publishes complete and exits 0 with no storage failure on record.
    def broken(*_args, **_kwargs):
        raise stage2_research_store.StoreWriteError("disk full")

    monkeypatch.setattr(stage2_research_store.Store, "set_append", broken)
    sworld.complete()
    assert sworld.run() == 1
    text = sworld.research.read_text(encoding="utf-8")
    assert manifest_of(sworld)["status"].startswith("incomplete"), "the record must not read complete"
    assert "state-store-unwritable" in text


def test_an_aborted_run_names_every_expected_slot_with_its_outcome(sworld: SwarmWorld) -> None:
    # Criterion 18 (phase-6 F-17). Planted fault: after a finder fails the manifest lists only the three finder
    # slots; merge, topic author, topic slots and judge carry neither identity nor outcome.
    sworld.selection = selection_for(free=FREE)
    sworld.complete(**{"finder:None:deepseek-v4.1-flash": [{"stdout": "not a locator list"}]})
    assert sworld.run() == 1
    manifest = manifest_of(sworld)
    slots = manifest["slots"]
    ids = [slot["slot_id"] for slot in slots]
    assert len(ids) == len(set(ids)) == manifest["budget"], "39 + 3N identities, each once"
    unstarted = [slot for slot in slots if slot["outcome"] == "not-started"]
    assert {"merge", "sentence", "judge"} <= {slot["slot_id"] for slot in unstarted}
    assert sum(slot["stage"] == "topics" for slot in unstarted) == 33 + 3 * len(FREE)
    assert all(slot["endpoint"] and slot["model"] and slot["launched"] is False for slot in unstarted)


def test_a_reused_result_keeps_its_original_start_and_leak_check_in_the_published_manifest(
    sworld: SwarmWorld,
) -> None:
    # Criterion 55 (phase-6 F-18). Planted fault: a completed resumed run loses the original start time or the
    # original leak-check record of a reused slot (the store holding them is cleared on completion).
    sworld.complete(judge=[{"exit": 1}])
    assert sworld.run() == 1
    first = {s["slot_id"]: s for s in manifest_of(sworld)["slots"]}
    assert first["finders-0-1"]["started_at"] and first["finders-0-1"]["leak_check"]["clean"] is True
    sworld.complete()
    (sworld.bin / "calls.jsonl").unlink()
    assert sworld.run() == 0
    assert not [p for p in store_dir(sworld).iterdir() if p.name != ".lock"], "the store is cleared"
    second = {s["slot_id"]: s for s in manifest_of(sworld)["slots"]}
    reused = second["finders-0-1"]
    assert reused["reused_from"] and reused["started_at"] == first["finders-0-1"]["started_at"]
    assert reused["ended_at"] == first["finders-0-1"]["ended_at"]
    assert reused["leak_check"] == first["finders-0-1"]["leak_check"]


def test_the_receipt_keeps_each_candidates_evidence_and_exclusion(fx: PrepFixture) -> None:
    # Criteria 38, 44 (phase-6 F-14). Planted fault: the receipt drops a free candidate's id, source value and
    # exclusion reason.
    fx.catalog.pi += [pi_model("delta-free")]
    fx.catalog.tools["delta-free"] = {"id": "delta-free", "tool_call": False}
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    candidates = {c["id"]: c for c in state["catalog"]["candidates"]}
    assert candidates["delta-free"]["reason"] == "no-tool-support"
    assert candidates["delta-free"]["evidence"]["tool_call"] == {"present": True, "value": False}
    assert any(model["id"] == "qwen3.8-flash" for model in state["catalog"]["models"])


def test_the_manifest_publishes_preparation_time_pool_candidates_and_probe_audit(sworld: SwarmWorld) -> None:
    # Criteria 38, 46 (phase-6 F-14). Planted fault: the manifest omits preparation time, pool, candidate outcomes
    # or the probe audit lines of the consumed selection.
    sworld.selection = {
        **selection_for(free=[]),
        "checked_at": "2026-10-19T08:00:00+00:00",
        "pool": [{"model": "pool-a"}],
        "models": {"m": {"state": "ok", "reason": None}},
        "audit": ["probe line"],
    }
    sworld.selection["catalog"] = {
        "pi_version": "test",
        "candidates": [{"id": "delta-free", "reason": "no-tool-support", "evidence": {}}],
    }
    sworld.complete()
    assert sworld.run() == 0
    manifest = manifest_of(sworld)
    assert manifest["preparation"]["checked_at"] == "2026-10-19T08:00:00+00:00"
    assert manifest["preparation"]["pool"] == [{"model": "pool-a"}]
    assert manifest["preparation"]["audit"] == ["probe line"]
    assert {c["id"]: c["reason"] for c in manifest["catalog"]["candidates"]}["delta-free"] == "no-tool-support"


def test_the_measured_catalog_reaches_pis_agent_directory_for_probes_and_launches(
    fx: PrepFixture,
) -> None:
    # Criteria 38, 43, 61 (phase-6 F-13). Planted fault: probes and research launches start Pi with an agent
    # directory that holds no measured model definitions, so Pi resolves shipped metadata instead.
    assert fx.prepare() == 0
    probes = [call for call in fx.w.calls("pi") if "--no-tools" in call.get("argv", [])]
    assert probes, "a Go probe ran"
    for call in probes:
        assert {"models.json", "models-store.json"} <= set(call["agent_listing"]), call["agent_listing"]
    store = fx.receipt()["state"]["catalog"]["models_store"]
    assert store, "the receipt carries the measured model store for the launches"


def test_research_launches_install_the_consumed_catalog_store(sworld: SwarmWorld) -> None:
    # Criteria 43, 61 (phase-6 F-13). Planted fault: a research launch gets an agent directory without the
    # measured definitions.
    sworld.selection["catalog"] = {
        "pi_version": "test",
        "models_store": {"opencode-go": {"models": [{"id": "qwen3.8-flash", "api": "openai-completions"}]}},
    }
    sworld.complete()
    assert sworld.run() == 0
    go = [call for call in sworld.calls() if call["name"] == "pi"]
    assert go and all({"models.json", "models-store.json"} <= set(call["agent_listing"]) for call in go)
    assert "models_store" not in manifest_of(sworld)["catalog"], "raw definitions stay out of research.md"


def test_a_store_inside_the_real_home_is_refused_and_one_outside_it_is_accepted(
    sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 52 (phase-6 F-12, Q-15). Planted fault: the default store beneath the home Claude research
    # processes inherit passes the placement guard.
    home = Path(os.environ["HOME"])
    monkeypatch.delenv("XDG_STATE_HOME")  # the default beneath HOME
    sworld.complete()
    assert sworld.run() == 1
    assert sworld.calls() == [], "no model starts"
    message = capsys.readouterr().err
    assert "XDG_STATE_HOME" in message and str(home) in message
    monkeypatch.setenv("XDG_STATE_HOME", str(home.parent / "state-outside-home"))
    assert sworld.run() == 0
