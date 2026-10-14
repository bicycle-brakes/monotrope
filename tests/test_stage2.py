"""The runner of stage 2 and what it declares - and the cases in which it holds.

`scripts/stage2.py` is the only way this repository starts a foreign reviewer.
Every case here runs it in-process against a temporary repository and two
stand-ins: programs named `codex` and `claude` that record their arguments,
environment and input, print canned output and contact nothing. No test starts
a real Codex, a real Claude Code against a model endpoint, or reads the
maintainer's real denylist, secrets or loop record.

Each test comes with its fault: the mutation list of the plan's slices 2 and 3
was planted one by one and each one turned a test here red. The doctrine tests
at the end read the repository's own documents and prompts; each one checks
its fault on a planted copy of the text in the same test.
"""

from __future__ import annotations

import ast
import copy
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_decision_continuity  # noqa: E402
import check_frontmatter_current  # noqa: E402
import leakcheck  # noqa: E402
import omnigent_policy  # noqa: E402
import plans_registry  # noqa: E402
import stage2  # noqa: E402
import stage2_runs  # noqa: E402

GIT = shutil.which("git")  # resolved before any test narrows the PATH

KEY = "sk-zq7Hk2mVw9Xr4Tn8Lb3Pd6Jc1Fy5Ga0"
LEAK = "LEAKMARK-123456"
DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"
SETTINGS = REPO_ROOT / ".claude" / "settings.json"
VERDICT = "Phase 6 verdict: codex T1, 2026-09-30"

# The planted OpenCode key keeps its distance from the planted GLM key above: an
# inserted line beside that one pulls it into every diff's context, the loop's
# prompt carries the diff, and the leak check rightly refuses key-shaped text
# there (measured 2026-10-08, prompt line 3647).
OKEY = "ok-7Rt2Wm9xQb4Nv6Lc"

# A stand-in: one template for both programs, the standard library only.
STAND_IN = """#!@PYTHON@
# stage2-stand-in: records its call, prints canned output, contacts nothing.
import json
import os
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
if name == "pi" and argv == ["--version"]:
    # The version check is answered from the scenario and not recorded: it is no call.
    time.sleep(scenario.get("pi_version_sleep", 0))
    sys.stdout.write(scenario.get("pi_version", "@PI@") + "\\n")
    raise SystemExit(scenario.get("pi_version_exit", 0))


def option(flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


config = os.environ.get("CLAUDE_CONFIG_DIR")
prompt_file = option("--append-system-prompt-file") or option("--append-system-prompt")
agent = os.environ.get("PI_CODING_AGENT_DIR")
marker = scenario.get("marker")
found = []
if marker:
    for directory, names, files in os.walk(os.getcwd()):
        names[:] = [n for n in names if n != ".git"]
        for file in files:
            path = Path(directory) / file
            try:
                if marker in path.read_text(errors="replace"):
                    found.append(str(path))
            except OSError:
                pass
findings = Path("plans/changes/demo/findings.md")
record = {
    "name": name,
    "argv": argv,
    "env": dict(os.environ),
    "cwd": os.getcwd(),
    "stdin": os.read(0, 100).decode(),
    "config_listing": sorted(os.listdir(config)) if config and os.path.isdir(config) else None,
    "agent_listing": sorted(os.listdir(agent)) if agent and os.path.isdir(agent) else None,
    "agent_settings": (Path(agent) / "settings.json").read_text() if agent and (Path(agent) / "settings.json").is_file() else None,
    "home_listing": sorted(os.listdir(os.environ["HOME"])) if os.path.isdir(os.environ.get("HOME", "")) else None,
    "prompt_file": Path(prompt_file).read_text() if prompt_file else None,
    "marker_paths": found,
    "findings": findings.read_text() if findings.exists() else None,
}
with log.open("a") as handle:
    handle.write(json.dumps(record) + "\\n")
time.sleep(step.get("sleep", 0))
key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("OPENCODE_API_KEY", "")
for relative, text in step.get("plant", {}).items():
    Path(relative).parent.mkdir(parents=True, exist_ok=True)
    Path(relative).write_text(text.replace("@KEY@", key))
for relative in step.get("delete", []):
    Path(relative).unlink()
for relative, text in step.get("append", {}).items():
    with Path(relative).open("a") as handle:
        handle.write(text.replace("@KEY@", key))
sys.stdout.write(step.get("stdout", "").replace("@KEY@", key))
sys.stderr.write(step.get("stderr", "").replace("@KEY@", key))
answer_path = option("-o")
if answer_path and "answer" in step:
    Path(answer_path).write_text(step["answer"])
raise SystemExit(step.get("exit", 0))
"""


def codex_ok(thread: str, answer: str, **more: object) -> dict:
    """A Codex step that succeeds: a `thread.started` event and the answer file."""
    started = json.dumps({"type": "thread.started", "thread_id": thread})
    return {"stdout": started + '\n{"type": "turn.completed"}\n', "answer": answer, **more}


def rows(count: int, prefix: str = "X") -> str:
    return "\n".join(
        f"| {prefix}{n} | MAJOR | SPEC | criterion {n} | spec.md:{n} | FB{n}-unique-body |" for n in range(1, count + 1)
    )


def git(cwd: Path, *args: str) -> str:
    run = subprocess.run(
        [GIT, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return run.stdout.strip()


@dataclass
class World:
    root: Path
    bin: Path
    state: Path

    def script(self, **steps: object) -> None:
        (self.bin / "scenario.json").write_text(json.dumps(steps), encoding="utf-8")

    def calls(self, name: str | None = None) -> list[dict]:
        log = self.bin / "calls.jsonl"
        found = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        return [call for call in found if name is None or call["name"] == name]

    def run(self, verb: str, change: str | None = "demo", *options: str) -> int:
        argv = [verb] if change is None else [verb, change]
        return stage2.main([*argv, *options, "--root", str(self.root)])

    @property
    def findings(self) -> Path:
        return self.root / "plans" / "changes" / "demo" / "findings.md"

    @property
    def research(self) -> Path:
        return self.root / "plans" / "changes" / "demo" / "research.md"

    @property
    def plan(self) -> Path:
        return self.root / "plans" / "changes" / "demo" / "plan.md"

    def text(self) -> str:
        return self.findings.read_text(encoding="utf-8")

    def record(self) -> Path:
        return self.state / "coding-harness" / "stage2" / "demo" / "loop.md"

    def write_record(
        self, decided: list[tuple[str, str, str]], finding: str = "", reviewer: str = "deepseek-v4.1-flash"
    ) -> None:
        """A loop record of one round whose rows carry the given (id, status, broke a test)."""
        rows_ = [
            [
                ident,
                "MAJOR",
                "MAINT",
                "impl",
                "src/app.py:1",
                f"finding of {ident} {finding}".strip(),
                reviewer,
                status,
                broke,
            ]
            for ident, status, broke in decided
        ]
        directory = self.record().parent
        directory.mkdir(parents=True, exist_ok=True)
        self.record().write_text(
            f"# Loop record — demo\n\n{stage2.RECORD_INTRO}\n\n## Round 1 — {reviewer}, 2026-09-30\n\n"
            f"{stage2.render_table(stage2.ROW_COLUMNS, rows_)}\n",
            encoding="utf-8",
        )

    def write_findings(self, *lines: str) -> None:
        self.findings.write_text("# Findings — demo\n\n" + "\n\n".join(lines) + "\n", encoding="utf-8")


def decide_record(w: World, status: str = "taken — test_a", broke: str = "no") -> None:
    """Decide every row of the loop record the way the implementer would: by editing the file."""
    text = w.record().read_text(encoding="utf-8")
    text = re.sub(r"^(\| L\d+-\d+ \|.*\|)  \|  \|$", rf"\1 {status} | {broke} |", text, flags=re.M)
    w.record().write_text(text, encoding="utf-8")


def old_header(updated: str = "2026-09-29") -> str:
    """A findings.md header of a day long gone, as `plans-registry` holds it."""
    return (
        "---\ntitle: Findings\ncategory: findings\nstatus: draft\nimplementation_status: none\n"
        f"date: {updated}\ncreated: {updated}\nlast_reviewed: {updated}\nupdated: {updated}\n"
        "bead: demo-1\n---\n\n# Findings — demo\n"
    )


def render_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


TEST_LADDER = ("deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro")


def pin_the_ladder(target: Path) -> None:
    """Copy the real declaration into a test world with the ladder in the tests' own order.

    The real order is the maintainer's to change in `model-endpoints.yaml` alone; the tests that follow a round
    to its model must not break when it changes, so they run on this order.
    """
    text = (REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8")
    real = next(e for e in yaml.safe_load(text)["endpunkte"] if e["name"] == "opencode-go")["modelle"]
    assert sorted(real) == sorted(TEST_LADDER), "the real ladder holds other models; update TEST_LADDER"
    block = "".join(f"      - {m}\n" for m in real)
    assert block in text
    target.write_text(text.replace(block, "".join(f"      - {m}\n" for m in TEST_LADDER), 1), encoding="utf-8")


@pytest.fixture
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    """A repository, two stand-ins and an environment that belong to the test."""
    root = tmp_path / "repo"
    (root / "plans" / "changes" / "demo").mkdir(parents=True)
    (root / "plans" / "changes" / "demo" / "spec.md").write_text(
        "---\ntitle: Spec\nbead: demo-1\n---\n\n# Spec\n", encoding="utf-8"
    )
    (root / "plans" / "changes" / "demo" / "research.md").write_text(
        "---\ntitle: Research\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Research\n\nseed fact\n",
        encoding="utf-8",
    )
    (root / "plans" / "changes" / "demo" / "plan.md").write_text(
        "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n## Time used\n",
        encoding="utf-8",
    )
    (root / "AGENTS.md").write_text("# Agent rules\n\nStay inside the repository.\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("value = 1\n", encoding="utf-8")
    shutil.copytree(REPO_ROOT / "prompts", root / "prompts")
    pin_the_ladder(root / "model-endpoints.yaml")
    (root / "provenance.yaml").write_text(
        "paths:\n  - {prefix: 'plans/', frontmatter: required}\nexcluded: []\n", encoding="utf-8"
    )
    (root / "scripts").mkdir()
    for script in (Path(plans_registry.__file__).name, "_verdict.py"):
        shutil.copy(REPO_ROOT / "scripts" / script, root / "scripts" / script)

    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("codex", "claude", "pi", "make"):
        program = bin_dir / name
        program.write_text(
            STAND_IN.replace("@PYTHON@", sys.executable).replace("@PI@", stage2.PI_VERSION), encoding="utf-8"
        )
        program.chmod(0o755)
    git_dir = tmp_path / "gitbin"
    git_dir.mkdir()
    (git_dir / "git").symlink_to(GIT)
    (tmp_path / "denylist.txt").write_text(DENYLIST, encoding="utf-8")
    (tmp_path / "secrets.env").write_text(
        f"# keys\nexport GLM_KEY='{KEY}'\nexport OPENCODE_GO_KEY='{OKEY}'\nOTHER=1\n", encoding="utf-8"
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
    git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    w = World(root, bin_dir, tmp_path / "state")
    w.script()
    return w


@pytest.fixture
def busy_stdin():
    """Something waiting on the caller's standard input, for a program that would inherit it."""
    read_end, write_end = os.pipe()
    os.write(write_end, b"from the caller")
    os.close(write_end)
    saved = os.dup(0)
    os.dup2(read_end, 0)
    os.close(read_end)
    try:
        yield
    finally:
        os.dup2(saved, 0)
        os.close(saved)


def endpoints() -> dict[str, dict]:
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    return {e["name"]: e for e in data["endpunkte"]}


def verdict_block(text: str) -> str:
    match = re.search(r"^## Phase 6 — .*?^Phase 6 verdict: [^\n]*$", text, re.M | re.S)
    assert match, "no verdict block"
    return match.group(0)


def full_flow(w: World) -> None:
    """spec-review, one loop round decided, the verdict, the release and the marks."""
    w.script(
        claude=[{"stdout": rows(2)}],
        codex=[
            codex_ok("T1", rows(1)),
            codex_ok("T1", "L1-1: agree\nL1-2: disagree — no test shows it"),
        ],
        pi=[{"stdout": rows(2)}],
    )
    assert w.run("spec-review") == 0
    assert w.run("review-loop") == 0
    w.write_record([("L1-1", "taken — test_a", "no"), ("L1-2", "rejected — out of scope", "")])
    assert w.run("review") == 0


# ---------------------------------------------------------------------------
# No real program, no real file (criteria 2, 3)
# ---------------------------------------------------------------------------


def test_the_runner_finds_only_stand_ins(world: World) -> None:
    found = []
    for entry in os.environ["PATH"].split(os.pathsep):
        for name in ("codex", "claude", "pi"):
            program = Path(entry) / name
            if program.is_file():
                found.append(name)
                assert "stage2-stand-in" in program.read_text(encoding="utf-8"), f"{program} is not a stand-in"
    assert sorted(found) == ["claude", "codex", "pi"]
    assert Path(shutil.which("codex") or "").parent == world.bin


def test_a_stand_in_contacts_nothing() -> None:
    tree = ast.parse(STAND_IN.replace("@PYTHON@", "python3").replace("@PI@", "1.1.0"))
    imported = {
        alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names
    } | {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert imported <= {"json", "os", "sys", "time", "pathlib"}


@pytest.mark.usefixtures("world")
def test_the_suite_never_reaches_the_real_denylist_or_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    home = Path(os.environ["HOME"])
    tmp = home.parent
    assert leakcheck.default_denylist().is_relative_to(tmp)
    assert stage2.secrets_path().is_relative_to(tmp)
    assert stage2.record_dir("demo").is_relative_to(tmp)
    for name in ("LEAKCHECK_DENYLIST", "CC_SECRETS", "XDG_STATE_HOME"):
        monkeypatch.delenv(name)
    assert leakcheck.default_denylist().is_relative_to(home)
    assert stage2.secrets_path().is_relative_to(home)
    assert stage2.record_dir("demo").is_relative_to(home)


# ---------------------------------------------------------------------------
# The entries that stay declared (the remark corrections of criterion 3)
# ---------------------------------------------------------------------------


def test_openai_codex_is_declared_as_decided() -> None:
    codex = endpoints()["openai-codex"]
    assert codex["betreiber"] == "OpenAI"
    assert codex["residenz"] == "anbieter-erklaert"
    assert codex["abrechnung"] == "abonnement"
    assert codex["darf_sehen"] == ["framework"]
    assert codex["modelle"] == ["gpt-6.1-sol"]
    remark = codex["bemerkung"]
    assert "Codex CLI" in remark and "United States" in remark
    assert "moved to `opencode-go`" in remark


def test_kimi_is_excluded_not_declared() -> None:
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    for endpoint in data["endpunkte"]:
        text = json.dumps(endpoint).lower()
        assert "moonshot" not in text and "kimi-for-coding" not in text and not re.search(r"\bk3\b", text)
    kimi = [entry for entry in data["ausgeschlossen"] if "Kimi" in entry["was"]]
    assert len(kimi) == 1
    assert "2026-09-30" in kimi[0]["grund"] and "maintainer" in kimi[0]["grund"]


def test_the_glm_remark_names_its_work_verbs_and_no_review_phase() -> None:
    # Criterion 36. Planted fault: the remark loses `stage2.py draft`, or claims a review phase.
    remark = " ".join(endpoints()["glm-coding-plan"]["bemerkung"].lower().split())
    assert "stage2.py explore" in remark and "stage2.py implement" in remark
    assert "stage2.py draft" in remark and "glm-5.3" in remark
    assert "is used for the review loop" not in remark
    assert "moved to `opencode-go`" in remark
    assert "does not have yet" not in remark
    for word in ("umsetzung", "marking"):
        assert word not in remark


# ---------------------------------------------------------------------------
# The rows of an answer
# ---------------------------------------------------------------------------


def test_parse_rows_takes_six_cell_rows_and_keeps_the_rest() -> None:
    answer = "Before.\n| ID | Severity | Dimension | Origin | Where | Finding |\n|---|---|---|---|---|---|\n"
    answer += rows(2) + "\n| only | three | cells |\n\nAfter.\n"
    found, rest = stage2.parse_rows(answer)
    assert [row[0] for row in found] == ["X1", "X2"]
    assert rest.splitlines() == ["Before.", "| only | three | cells |", "After."]
    assert stage2.parse_rows(rows(1))[1] == ""


def test_parse_marks_reads_agreement_and_disagreement() -> None:
    marks = stage2.parse_marks("L1-1: agree\n- **L1-2**: disagree — no test | shows it\nL1-3: Disagree\nnoise\n")
    assert marks == {"L1-1": "agree", "L1-2": "disagree — no test \\| shows it", "L1-3": "disagree"}


def test_parse_rows_folds_a_pipe_inside_the_finding_into_it() -> None:
    """Repair round 1, F-2: six cells are known; a seventh after a valid severity is part of the last one."""
    found, rest = stage2.parse_rows(
        "| X1 | MAJOR | SPEC | a | b.py:1 | a | b \\| c | d |\n| X2 | MAJOR | SPEC | a | b | ok |"
    )
    assert [row[0] for row in found] == ["X1", "X2"] and rest == ""
    assert found[0][5] == "a \\| b \\| c \\| d" and found[1][5] == "ok"
    # a line of seven cells that does not start like a row is not guessed at
    found, rest = stage2.parse_rows("| one | two | three | four | five | six | seven |")
    assert found == [] and "seven" in rest


@pytest.mark.parametrize(
    "answer",
    [
        "| only | three | cells |",
        "| X1 | MAJOR | SPEC | a | b |",
        "| ID | Severity | Dimension |\n|---|---|---|\n| X1 | MAJOR | SPEC |",
    ],
    ids=["three-cells", "five-cells", "short-table"],
)
def test_table_lines_that_are_not_rows_are_never_reported_as_no_finding(world: World, answer: str) -> None:
    """Repair round 1, F-3: a table the parser cannot read is passed through, under a head that is true."""
    world.script(claude=[{"stdout": answer}], pi=[{"stdout": answer}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    kept = world.record().read_text(encoding="utf-8")
    for text in (world.text(), kept):
        assert "reported no finding" not in text
        assert "not six-cell rows" in text and stage2.NOT_ROWS_NOTE in text
    assert answer.splitlines()[-1] in world.text() and answer.splitlines()[-1] in kept


def test_the_review_prompt_and_the_runner_ask_for_the_same_cells() -> None:
    """Repair round 1, F-3: what the runner asks for last, the phase prompt must not contradict."""
    header = "| ID | Severity | Dimension | Origin | Where | Finding |"
    assert header in stage2.ANSWER_FORMAT and "six cells" in stage2.ANSWER_FORMAT
    assert "\\|" in stage2.ANSWER_FORMAT, "a pipe inside a cell is asked to be escaped"
    for name in ("02a-spec-review.md", "06-review.md", "04b-review-loop.md"):
        text = flat((PROMPTS / name).read_text(encoding="utf-8"))
        assert header in text and "six cells" in text, name
    review = flat((PROMPTS / "06-review.md").read_text(encoding="utf-8"))
    assert "columns exactly as they stand there" not in review, "the nine-column form would outvote the runner"


# ---------------------------------------------------------------------------
# Every call goes through the runner's preconditions (criteria 15-21)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("verb", sorted(stage2.VERBS))
@pytest.mark.parametrize("change", [None, "missing", "..", "a/b"])
def test_no_change_or_a_missing_folder_refuses_every_verb(world: World, verb: str, change: str | None) -> None:
    assert world.run(verb, change) == 2
    assert world.calls() == []
    assert not world.findings.exists()


def test_a_leak_refuses_the_call(world: World) -> None:
    (world.root / "src" / "leak.txt").write_text(LEAK, encoding="utf-8")
    for verb in ("spec-review", "review", "review-loop", "probe"):
        assert world.run(verb) == 2
    assert world.calls() == []
    assert not world.findings.exists()


def test_each_call_runs_its_own_leak_check(world: World) -> None:
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(codex=[codex_ok("T1", rows(1), plant={"leak.txt": LEAK}), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 2
    assert len(world.calls("codex")) == 1, "the mark call started on the first call's check"


REVIEW_VERBS = ("spec-review", "review-loop", "review", "probe")


@pytest.mark.parametrize(
    ("verb", "endpoint"),
    [
        ("spec-review", "claude-code-plan"),
        ("review", "openai-codex"),
        ("review-loop", "opencode-go"),
        ("probe", "opencode-go"),
    ],
)
@pytest.mark.parametrize("fault", ["missing", "no-model", "no-framework", "no-residency"])
def test_an_endpoint_the_declaration_does_not_clear_refuses(world: World, verb: str, endpoint: str, fault: str) -> None:
    """Criterion 10: every call clears the entry it calls, each in front of its own check."""
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = next(e for e in data["endpunkte"] if e["name"] == endpoint)
    if fault == "missing":
        data["endpunkte"].remove(entry)
    elif fault == "no-model":
        entry["modelle"] = []
    elif fault == "no-framework":
        entry["darf_sehen"] = []
    else:
        entry["residenz"] = "nicht-erklaert"
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    assert world.run(verb) == 2
    assert world.calls() == []


@pytest.mark.parametrize(
    ("verb", "options", "endpoint"),
    [
        ("explore", (), "glm-coding-plan"),
        ("implement", (), "glm-coding-plan"),
        ("explore", ("--stage2-off", "r"), "claude-code-plan"),
        ("implement", ("--stage2-off", "r"), "claude-code-plan"),
    ],
    ids=["explore-flash", "implement-flash", "explore-stage1", "implement-stage1"],
)
@pytest.mark.parametrize("fault", ["missing", "no-model", "no-framework", "no-residency"])
def test_a_broken_declaration_stops_the_work_verbs_before_any_model(
    world: World, verb: str, options: tuple[str, ...], endpoint: str, fault: str
) -> None:
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = next(e for e in data["endpunkte"] if e["name"] == endpoint)
    if fault == "missing":
        data["endpunkte"].remove(entry)
    elif fault == "no-model":
        entry["modelle"] = ["another-model"]
    elif fault == "no-framework":
        entry["darf_sehen"] = []
    else:
        entry["residenz"] = "nicht-erklaert"
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    assert world.run(verb, "demo", *options) == 2
    assert world.calls() == []


@pytest.mark.parametrize("verb", ["explore", "implement"])
def test_a_leak_before_the_first_work_call_starts_no_model(world: World, verb: str) -> None:
    (world.root / "src" / "leak.txt").write_text(LEAK, encoding="utf-8")
    if verb == "implement":
        git(world.root, "add", "-A")
        git(world.root, "commit", "--quiet", "-m", "planted leak")
    world.script(claude=[{"stdout": "must not run"}])
    assert world.run(verb) == 2
    assert world.calls() == []
    assert world.run(verb, "demo", "--stage2-off", "r") == 2, "a leak never falls back"
    assert world.calls() == []


@pytest.mark.parametrize("verb", ["explore", "implement"])
def test_a_missing_glm_key_refuses_the_flash_route(world: World, verb: str) -> None:
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    world.script(claude=[{"stdout": "must not run"}])
    assert world.run(verb) == 2
    assert world.calls() == []


def test_the_foreign_environment_is_the_runners(world: World) -> None:
    # Two Claude calls run: the spec review first, then the explorer.
    world.script(pi=[{"stdout": rows(1)}], claude=[{"stdout": rows(1)}, {"stdout": "a fact"}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert world.run("explore") == 0
    spec, loop, explorer = (
        world.calls("claude")[0]["env"],
        world.calls("pi")[0]["env"],
        world.calls("claude")[1]["env"],
    )
    for env in (spec, loop, explorer):
        assert "GH_TOKEN" not in env and "OPENAI_API_KEY" not in env and "X_SECRET" not in env
    assert not [name for name in spec if name.startswith("ANTHROPIC_")], "the spec review carries an Anthropic variable"
    assert loop["OPENCODE_API_KEY"] == OKEY
    assert all(value != KEY for value in loop.values()), "an OpenCode Go call carries the GLM key"
    assert not [n for n in loop if n.startswith(("ANTHROPIC_", "CLAUDE_"))], "a Pi call carries a Claude variable"
    assert loop["HOME"] != os.environ["HOME"] and "PI_CODING_AGENT_DIR" in loop
    assert explorer["ANTHROPIC_BASE_URL"] == stage2.GLM_BASE_URL
    assert explorer["ANTHROPIC_AUTH_TOKEN"] == KEY
    assert "CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT" not in explorer, "GLM's environment is main's"
    assert all(value != OKEY for value in explorer.values()), "a GLM call carries the OpenCode Go key"
    credentials = [n for n in loop if n.endswith(("_KEY", "_TOKEN", "_SECRET"))]
    assert credentials == ["OPENCODE_API_KEY"]


def test_no_call_carries_another_endpoints_key(world: World) -> None:
    """Criterion 13: the OpenCode Go key and the GLM key never meet in one environment."""
    world.script(pi=[{"stdout": rows(1)}], claude=[{"stdout": rows(1)}, {"stdout": "a fact"}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert world.run("explore") == 0
    _spec, loop, explorer = (
        world.calls("claude")[0]["env"],
        world.calls("pi")[0]["env"],
        world.calls("claude")[1]["env"],
    )
    assert all(value != KEY for value in loop.values()), "an OpenCode Go call carries the GLM key"
    assert all(value != OKEY for value in explorer.values()), "a GLM call carries the OpenCode Go key"


@pytest.mark.usefixtures("busy_stdin")
def test_every_call_gets_an_empty_standard_input(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}], pi=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert [call["stdin"] for call in world.calls()] == ["", ""]


def test_the_opencode_key_never_leaves_the_runner(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criteria 11 and 12: the key rides in the environment only - no argv, no stream, no record carries it."""
    said = "| X1 | MAJOR | SPEC | a | b | saw @KEY@ |\n"
    world.script(pi=[{"stdout": said, "stderr": "@KEY@", "exit": 0}, {"stdout": said, "stderr": "@KEY@", "exit": 1}])
    assert world.run("review-loop") == 0
    first = world.calls("pi")[0]
    assert first["env"]["OPENCODE_API_KEY"] == OKEY
    assert "--api-key" not in first["argv"]
    assert [name for name, value in first["env"].items() if OKEY in value] == ["OPENCODE_API_KEY"]
    assert first["agent_listing"] == ["settings.json"]
    for call in world.calls():
        assert not any(OKEY[i : i + 8] in " ".join(call["argv"]) for i in range(len(OKEY) - 7)), call["argv"]
        seen_in_directory = " ".join(str(call[field]) for field in ("agent_settings", "home_listing", "agent_listing"))
        assert not any(OKEY[i : i + 8] in seen_in_directory for i in range(len(OKEY) - 7))
    kept = "".join(p.read_text(encoding="utf-8") for p in world.state.rglob("*") if p.is_file())
    shutil.rmtree(world.state)
    assert world.run("review-loop") == 1
    seen = capsys.readouterr()
    everything = seen.out + seen.err + world.text() + kept
    assert "[credential]" in kept
    assert not any(OKEY[i : i + 8] in everything for i in range(len(OKEY) - 7)), "the credential leaked"


def test_every_call_leaves_its_line_in_findings(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}], pi=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    text = world.text()
    day = r"\d{4}-\d{2}-\d{2}"
    count = r"\d+ files, \d+ commits, 1 rules"
    assert re.search(
        rf"^Stage-2 call, {day}: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · "
        rf"leak check clean over {count}\.$",
        text,
        re.M,
    )
    assert re.search(
        rf"^Stage-2 call, {day}: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · "
        rf"leak check clean over {count}\.$",
        text,
        re.M,
    )


def test_a_findings_file_the_runner_creates_has_a_registry_header(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    header = plans_registry._frontmatter(world.findings)
    assert header is not None
    for field in plans_registry.REQUIRED:
        assert header.get(field), field
    assert header["status"] in plans_registry.STATUS
    assert header["implementation_status"] in plans_registry.IMPLEMENTATION
    assert header["bead"] == "demo-1" and header["category"] == "findings"


def updated_of(path: Path) -> object:
    return check_frontmatter_current.read_updated(path.read_text(encoding="utf-8"))


def test_every_write_to_findings_keeps_its_updated_stamp_current(world: World) -> None:
    """Repair round 1, F-7: a findings.md older than today stays one the gate `frontmatter-current` accepts."""
    today = dt.date.today()
    world.findings.write_text(old_header(), encoding="utf-8")
    assert updated_of(world.findings) == dt.date(2026, 9, 29)
    world.script(
        claude=[{"stdout": rows(1)}],
        codex=[
            codex_ok("T1", rows(1)),
            codex_ok("T1", "L1-1: agree"),
        ],
        pi=[{"stdout": rows(1)}],
    )
    assert world.run("spec-review") == 0
    assert updated_of(world.findings) == today, "the call line left the header stale"

    world.findings.write_text(world.text().replace(f"updated: {today}", "updated: 2026-09-29", 1), encoding="utf-8")
    assert world.run("review-loop") == 0
    assert updated_of(world.findings) == today
    decide_record(world)

    world.findings.write_text(world.text().replace(f"updated: {today}", "updated: 2026-09-29", 1), encoding="utf-8")
    assert world.run("review") == 0
    assert updated_of(world.findings) == today, "the verdict, the release or the marks left the header stale"
    assert world.text().count("\nupdated:") == 1 and "date: 2026-09-29" in world.text()


# ---------------------------------------------------------------------------
# The GLM Flash work phases (stage2-flash-runner criteria 1-16, 18)
# ---------------------------------------------------------------------------


def successful_implementation(world: World, *, stdout: str = "implemented") -> None:
    """One model edit, measured plan line and passing make stand-in."""
    world.script(
        claude=[
            {
                "stdout": stdout,
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )


def test_explore_uses_flash_read_only_and_appends_research(world: World) -> None:
    before = world.research.read_text(encoding="utf-8")
    world.script(claude=[{"stdout": "Fact from `src/app.py` and its symbol `value`."}])
    assert world.run("explore") == 0
    call = world.calls("claude")[0]
    argv, prompt = call["argv"], call["prompt_file"]
    assert argv[argv.index("--model") + 1] == "glm-5.3-flash"
    assert argv[argv.index("--effort") + 1] == "max"
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"Read", "Grep", "Glob"}
    assert "--restricted" in argv and "--safe-mode" in argv and "--strict-mcp-config" in argv
    assert "--add-dir" not in argv and call["cwd"] == str(world.root)
    assert argv[argv.index("--permission-mode") + 1] == "dontAsk"
    assert call["env"]["ANTHROPIC_BASE_URL"] == stage2.GLM_BASE_URL
    assert call["env"]["ANTHROPIC_MODEL"] == "glm-5.3-flash"
    assert (REPO_ROOT / "prompts" / "01-explore.md").read_text(encoding="utf-8").rstrip() in prompt
    assert "Stay inside the repository." in prompt and stage2.ANSWER_FORMAT not in prompt
    text = world.research.read_text(encoding="utf-8")
    assert "seed fact" in before and "seed fact" in text
    assert "## Runner exploration" in text and "Fact from `src/app.py`" in text
    assert "attempt 1 · route flash" in text and "model glm-5.3-flash" in text
    assert not world.findings.exists()


def test_explore_needs_research_but_not_spec_or_plan(world: World) -> None:
    (world.root / "plans/changes/demo/spec.md").unlink()
    world.plan.unlink()
    world.script(claude=[{"stdout": "A sourced fact."}])
    assert world.run("explore") == 0
    world.research.write_text("# no header\n", encoding="utf-8")
    assert world.run("explore") == 2
    assert len(world.calls("claude")) == 1


def test_explore_stage2_off_uses_haiku_without_reading_the_glm_key(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on Stage 1: {name}"))
    world.script(claude=[{"stdout": "Fallback fact."}])
    assert world.run("explore", "demo", "--stage2-off", "Z.ai unavailable") == 0
    call = world.calls("claude")[0]
    argv, env = call["argv"], call["env"]
    assert argv[argv.index("--model") + 1] == "claude-haiku-4-5"
    assert "--effort" not in argv
    assert "ANTHROPIC_BASE_URL" not in env and "ANTHROPIC_AUTH_TOKEN" not in env
    text = world.research.read_text(encoding="utf-8")
    assert "route stage-1" in text and "reason Z.ai unavailable" in text


def test_explore_scrubs_the_flash_credential_from_its_answer(world: World) -> None:
    world.script(claude=[{"stdout": "the credential was @KEY@"}])
    assert world.run("explore") == 0
    text = world.research.read_text(encoding="utf-8")
    assert "[credential]" in text
    assert not any(KEY[i : i + 8] in text for i in range(len(KEY) - 7))


def test_an_empty_explore_answer_fails_without_an_answer_block(world: World) -> None:
    world.script(claude=[{"stdout": ""}, {"stdout": "must not run"}])
    assert world.run("explore") == 1
    assert len(world.calls("claude")) == 1
    assert "## Runner exploration" not in world.research.read_text(encoding="utf-8")


def test_implement_flash_has_file_tools_and_the_complete_contract(world: World) -> None:
    successful_implementation(world)
    assert world.run("implement") == 0
    call = world.calls("claude")[0]
    argv, prompt = call["argv"], call["prompt_file"]
    assert argv[argv.index("--model") + 1] == "glm-5.3-flash"
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"Read", "Grep", "Glob", "Edit", "Write"}
    assert "Bash" not in argv[argv.index("--tools") + 1]
    assert "--restricted" in argv and "--safe-mode" in argv and "--strict-mcp-config" in argv
    assert "--add-dir" not in argv and call["cwd"] == str(world.root)
    assert argv[argv.index("--permission-mode") + 1] == "acceptEdits"
    assert argv[argv.index("--permission-prompts") + 1] == "none"
    for forbidden in ("WebFetch", "bypassPermissions", "--dangerously-skip-permissions", "--allowedTools"):
        assert forbidden not in argv
    assert "# Agent rules" in prompt and "# Spec" in prompt and "# Plan" in prompt
    assert "Implementation baseline:" in prompt and "the runner runs `make verify`" in prompt
    assert [call["argv"] for call in world.calls("make")] == [["verify"]]
    assert git(world.root, "log", "-1", "--pretty=%s") == "feat(demo): implement accepted plan"
    assert git(world.root, "status", "--porcelain") == ""


def checking_derived_make(world: World) -> None:
    """A verifier stand-in that refuses stale generated inputs before recording its call."""
    checks = """
if name == "make":
    import datetime
    index = Path("plans/INDEX.md").read_text()
    assert "changes/demo/findings.md" in index, "audit artefact missing from index"
    assert "updated: " + datetime.date.today().isoformat() in Path("plans/changes/demo/plan.md").read_text()
"""
    (world.bin / "make").write_text(
        STAND_IN.replace("@PYTHON@", sys.executable).replace("record = {", checks + "\nrecord = {"),
        encoding="utf-8",
    )


def test_first_implement_refreshes_derived_files_without_a_model_repair(world: World) -> None:
    successful_implementation(world)
    checking_derived_make(world)
    assert world.run("implement") == 0
    assert len(world.calls("claude")) == 1
    assert len(world.calls("make")) == 1
    assert "changes/demo/findings.md" in (world.root / "plans/INDEX.md").read_text()
    assert git(world.root, "status", "--porcelain") == ""


def test_preparation_stamps_only_changed_held_documents(world: World) -> None:
    clean = world.research.read_bytes()
    unheld = world.root / "src/note.md"
    unheld.write_text(old_header(), encoding="utf-8")
    held = world.root / "plans/changes/demo/new.md"
    held.write_text(old_header() + "\nBody stays verbatim.\n", encoding="utf-8")
    before = held.read_text()
    deleted = world.root / "plans/changes/demo/deleted.md"
    deleted.write_text(old_header(), encoding="utf-8")
    git(world.root, "add", str(deleted))
    git(world.root, "commit", "-m", "document to delete")
    deleted.unlink()
    duplicate = world.root / "plans/changes/demo/duplicate.md"
    duplicate.write_text(old_header().replace("updated:", "updated: 2026-09-29\nupdated:", 1))
    no_header = world.root / "plans/changes/demo/no-header.md"
    no_header.write_text("# No header\n")
    before_duplicate = duplicate.read_bytes()
    world.script(make=[{"stdout": "green"}])
    stage2.verify_attempt(world.root, world.plan, "")
    assert held.read_text() == before.replace("updated: 2026-09-29", f"updated: {dt.date.today()}")
    assert world.research.read_bytes() == clean
    assert unheld.read_text() == old_header()
    assert duplicate.read_bytes() == before_duplicate
    assert no_header.read_text() == "# No header\n"
    assert not deleted.exists()


def test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics(world: World) -> None:
    checking_derived_make(world)
    world.script(
        claude=[
            {"stdout": "first", "append": {"plans/changes/demo/plan.md": "measured first attempt\n"}},
            {"stdout": "repair", "append": {"plans/changes/demo/plan.md": "measured repair\n"}},
        ],
        make=[
            {"stdout": "actual test failed", "exit": 1, "plant": {"plans/INDEX.md": "stale again\n"}},
            {"stdout": "green"},
        ],
    )
    assert world.run("implement") == 0
    assert len(world.calls("make")) == 2
    assert len(world.calls("claude")) == 2
    assert "actual test failed" in world.calls("claude")[1]["prompt_file"]


def test_renderer_failure_is_bounded_scrubbed_and_prevents_verify(world: World) -> None:
    # This is a runner failure case, not mutation evidence for the registry's own gate.
    # Use the imported module's filename: test_ci's source-text heuristic otherwise
    # counts this file's existing refusal tests as registry mutation coverage.
    script = world.root / "scripts" / Path(plans_registry.__file__).name
    script.write_text("import sys\nprint(('" + KEY + "\\n') * 100)\nsys.exit(7)\n")
    problems = stage2.verify_attempt(world.root, world.plan, "", KEY)
    assert len(problems) == 1 and "index renderer exited 7" in problems[0]
    assert KEY not in problems[0] and "[credential]" in problems[0]
    assert len(problems[0].splitlines()) <= stage2.TAIL_LINES + 1
    assert world.calls("make") == []


@pytest.mark.parametrize("repair_on", [1, 2, None], ids=["flash-repair", "sonnet-fallback", "exhausted"])
def test_broken_renderer_uses_existing_repair_limits_and_checkpoints_only_after_green(
    world: World, repair_on: int | None
) -> None:
    script = Path("scripts") / Path(plans_registry.__file__).name
    original = (world.root / script).read_text()
    baseline = git(world.root, "rev-parse", "HEAD")
    steps = []
    for attempt in range(3):
        step = {
            "stdout": "implemented",
            "append": {"plans/changes/demo/plan.md": f"measured attempt {attempt + 1}\n"},
        }
        if attempt == 0:
            step["plant"] = {str(script): "print('renderer broken')\nraise SystemExit(7)\n"}
        elif attempt == repair_on:
            step["plant"] = {str(script): original}
        steps.append(step)
    world.script(claude=[*steps, {"stdout": "must not run"}], make=[{"stdout": "green"}])
    checking_derived_make(world)
    assert world.run("implement") == (1 if repair_on is None else 0)
    calls = world.calls("claude")
    assert len(calls) == (3 if repair_on is None else repair_on + 1)
    assert "index renderer exited 7" in calls[1]["prompt_file"]
    models = [call["argv"][call["argv"].index("--model") + 1] for call in calls]
    assert models == ["glm-5.3-flash", "glm-5.3-flash", "claude-sonnet-5-5"][: len(calls)]
    assert len(world.calls("make")) == (0 if repair_on is None else 1)
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == ("0" if repair_on is None else "1")


def test_invalid_utf8_preparation_cannot_reach_verify(world: World) -> None:
    bad = world.root / "plans/changes/demo/bad.md"
    bad.write_bytes(b"---\nupdated: yesterday\n---\n\xff")
    before = bad.read_bytes()
    problems = stage2.verify_attempt(world.root, world.plan, "")
    assert "not valid UTF-8" in problems[0]
    assert bad.read_bytes() == before and world.calls("make") == []


def test_preparation_collects_all_document_refusals_in_one_bounded_diagnostic(world: World) -> None:
    outside = world.root.parent / "outside.md"
    outside.write_text(old_header())
    directory = world.root / "plans/changes/demo"
    (directory / "a-link.md").symlink_to(outside)
    (directory / "b-utf8.md").write_bytes(b"---\nupdated: old\n---\n\xff")
    (directory / "c-cycle.md").symlink_to(directory / "c-cycle.md")
    problems = stage2.verify_attempt(world.root, world.plan, "")
    assert len(problems) == 1
    for name in ("a-link.md", "b-utf8.md", "c-cycle.md"):
        assert name in problems[0]
    assert len(problems[0].splitlines()) <= stage2.TAIL_LINES
    assert outside.read_text() == old_header() and world.calls("make") == []


def test_preparation_refuses_a_document_outside_the_worktree(world: World) -> None:
    outside = world.root.parent / "outside.md"
    outside.write_text(old_header())
    (world.root / "plans/changes/demo/link.md").symlink_to(outside)
    problems = stage2.verify_attempt(world.root, world.plan, "")
    assert "outside the worktree" in problems[0]
    assert outside.read_text() == old_header() and world.calls("make") == []


@pytest.mark.parametrize("relative", ["plans/changes/demo/link.md", "plans/INDEX.md"])
def test_preparation_keeps_clean_targets_of_internal_document_and_index_links_unchanged(
    world: World, relative: str
) -> None:
    target = world.root / "src/untouched.md"
    target.write_text(old_header())
    provenance = world.root / "provenance.yaml"
    provenance.write_text(provenance.read_text().replace("excluded: []", "excluded: ['plans/INDEX.md']"))
    git(world.root, "add", "-A")
    git(world.root, "commit", "-m", "clean link target")
    (world.root / relative).symlink_to(target)
    problems = stage2.verify_attempt(world.root, world.plan, "")
    assert any("aliased" in problem for problem in problems)
    assert target.read_text() == old_header()
    assert world.calls("make") == []


@pytest.mark.parametrize("relative", ["plans/changes/demo/linked.md", "plans/INDEX.md"])
def test_preparation_refuses_hardlinked_document_and_index(world: World, relative: str) -> None:
    target = world.root / "src/untouched.md"
    target.write_text(old_header())
    linked = world.root / relative
    if linked.exists():
        linked.unlink()
    os.link(target, linked)
    git(world.root, "add", "-A")
    git(world.root, "commit", "-m", "clean hardlink targets")
    world.findings.write_text("# New findings\n")
    if relative != "plans/INDEX.md":
        linked.write_text(old_header() + "\nAttempt edit\n")
    before = target.read_bytes()
    problems = stage2.verify_attempt(world.root, world.plan, "")
    assert any("hard-linked" in problem for problem in problems)
    assert target.read_bytes() == before and world.calls("make") == []


@pytest.mark.parametrize("content", ["paths: [null]\n", "paths: [{}]\n", "paths: [3]\n"])
def test_malformed_provenance_returns_preparation_diagnostics(world: World, content: str) -> None:
    (world.root / "provenance.yaml").write_text(content)
    (world.root / "plans/changes/demo/new.md").write_text(old_header())
    problems = stage2.verify_attempt(world.root, world.plan, "")
    assert len(problems) == 1 and "Derived-file preparation failed" in problems[0]
    assert "provenance" in problems[0] and world.calls("make") == []


def test_preparation_git_commands_receive_no_caller_credentials(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    original_run = stage2.subprocess.run
    commands = []

    def record(command, *args, **kwargs):
        if command[0] == "git":
            commands.append((command, kwargs.get("env")))
        return original_run(command, *args, **kwargs)

    monkeypatch.setattr(stage2.subprocess, "run", record)
    assert stage2.prepare_derived(world.root, stage2.foreign_env({})) == []
    assert len(commands) == 2
    for command, env in commands:
        assert env is not None, command
        for name in ("OPENAI_API_KEY", "GH_TOKEN", "X_SECRET", "ANTHROPIC_AUTH_TOKEN"):
            assert name not in env


def test_preparation_commands_receive_no_model_or_caller_credentials(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_launch = stage2.launch
    commands = []

    def record(command, root, env, secret=None):
        commands.append((command, dict(env)))
        return original_launch(command, root, env, secret)

    monkeypatch.setattr(stage2, "launch", record)
    successful_implementation(world)
    assert world.run("implement") == 0
    renderer_envs = [env for command, env in commands if "--index" in command]
    assert len(renderer_envs) == 1
    env = renderer_envs[0]
    assert KEY not in env.values()
    for name in ("GLM_KEY", "ANTHROPIC_AUTH_TOKEN", "OPENAI_API_KEY", "GH_TOKEN", "X_SECRET"):
        assert name not in env


def test_git_failure_in_preparation_is_a_bounded_scrubbed_diagnostic(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken_git(_root, **_kwargs):
        raise stage2.Refused((KEY + " git failure\n") * 100)

    monkeypatch.setattr(stage2, "changed_paths", broken_git)
    problems = stage2.verify_attempt(world.root, world.plan, "", KEY)
    assert len(problems) == 1 and "git failure" in problems[0]
    assert KEY not in problems[0] and "[credential]" in problems[0]
    assert len(problems[0].splitlines()) <= stage2.TAIL_LINES
    assert world.calls("make") == []


def test_implement_requires_spec_plan_time_heading_and_no_preexisting_work(world: World) -> None:
    world.plan.unlink()
    assert world.run("implement") == 2
    assert world.calls() == []

    world.plan.write_text("---\nbead: demo-1\n---\n# Plan\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "plan without time")
    assert world.run("implement") == 2
    assert world.calls() == []

    world.plan.write_text("---\nbead: demo-1\n---\n# Plan\n\n## Time used\n", encoding="utf-8")
    (world.root / "src/app.py").write_text("dirty = True\n", encoding="utf-8")
    assert world.run("implement") == 2
    assert world.calls() == []


def test_a_failed_or_empty_work_call_stops_without_retry(world: World) -> None:
    world.script(claude=[{"stderr": "boom", "exit": 1}, {"stdout": "must not run"}])
    assert world.run("implement") == 1
    assert len(world.calls("claude")) == 1 and world.calls("make") == []


def test_a_failed_flash_process_restores_the_baseline_so_stage2_off_can_proceed(world: World) -> None:
    head = git(world.root, "rev-parse", "HEAD")
    plan_before = world.plan.read_text(encoding="utf-8")
    world.script(
        claude=[
            {
                "stderr": "Z.ai outage",
                "exit": 1,
                "plant": {"src/half.py": "x = 1\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n", "src/app.py": "# edit\n"},
            },
            {
                "stdout": "built",
                "plant": {"src/app.py": "value = 3\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 11:00–11:05, 5 min\n"},
            },
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert git(world.root, "rev-parse", "HEAD") == head
    assert not (world.root / "src/half.py").exists()
    assert world.plan.read_text(encoding="utf-8") == plan_before
    assert git(world.root, "status", "--porcelain", "--", ".", ":(exclude)plans/changes/demo/findings.md") == ""
    assert "Stage-2 call" in world.text()  # the audit line stays in findings.md
    assert world.run("implement", "demo", "--stage2-off", "Z.ai outage") == 0
    assert git(world.root, "rev-list", "--count", f"{head}..HEAD") == "1"


def test_a_failed_model_call_names_what_was_restored(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    world.script(claude=[{"stderr": "boom", "exit": 1, "plant": {"src/half.py": "x = 1\n"}}])
    assert world.run("implement") == 1
    err = capsys.readouterr().err
    assert "restored the worktree" in err and "src/half.py" in err


def test_a_postcheck_failure_gets_one_flash_repair_with_its_diagnostic(world: World) -> None:
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {
                "stdout": "repaired",
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:06, 6 min\n"},
            },
        ],
        make=[{"stdout": "green\n"}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    calls = world.calls("claude")
    assert len(calls) == 2
    assert [c["argv"][c["argv"].index("--model") + 1] for c in calls] == [
        "glm-5.3-flash",
        "glm-5.3-flash",
    ]
    assert "plan.md` did not add a measured line" in calls[1]["prompt_file"]
    assert "attempt 2 · route flash-repair" in world.text()


def test_two_failed_postchecks_route_once_to_sonnet(world: World) -> None:
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "second"},
            {
                "stdout": "fallback fixed it",
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:08, 8 min\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n"}, {"stdout": "green\n"}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    calls = world.calls("claude")
    models = [call["argv"][call["argv"].index("--model") + 1] for call in calls]
    assert models == ["glm-5.3-flash", "glm-5.3-flash", "claude-sonnet-5-5"]
    assert calls[-1]["argv"][calls[-1]["argv"].index("--effort") + 1] == "medium"
    assert "ANTHROPIC_BASE_URL" not in calls[-1]["env"]
    assert len(world.calls("make")) == 3
    plan = world.plan.read_text(encoding="utf-8")
    assert "Stage-1 route: implement" in plan and "two Flash post-run checks failed" in plan
    text = world.text()
    assert "attempt 3 · route stage-1" in text and "reason two Flash post-run checks failed" in text


def test_verify_failure_is_bounded_in_the_repair_prompt(world: World) -> None:
    noisy = "\n".join(f"line-{number}" for number in range(100))
    world.script(
        claude=[
            {
                "stdout": "first",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:02, 2 min\n"},
            },
            {
                "stdout": "fixed",
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:02–10:03, 1 min\n"},
            },
        ],
        make=[{"stdout": noisy, "exit": 1}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    prompt = world.calls("claude")[1]["prompt_file"]
    assert "`make verify` exited 1" in prompt and "line-99" in prompt
    assert "line-0" not in prompt and "line-19" not in prompt and "line-20" in prompt


def _gate(name: str, body: list[str], verdict: str) -> list[str]:
    """One gate as `verify_all.sh` frames it."""
    end = {
        "green": f"── [{name}] gruen",
        "red": f"── [{name}] RED (block) — der Lauf ist rot.",
        "report": f"── [{name}] rot, aber nur report — er meldet, er blockiert nicht.",
    }[verdict]
    return [f"── [{name}] $ run {name}", *body, end, ""]


def _red_run(world: World, output: str) -> str:
    """Run implement with one red verify carrying `output`, then green; return the repair prompt."""
    world.script(
        claude=[
            {
                "stdout": "first",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"},
            },
            {
                "stdout": "fixed",
                "append": {"plans/changes/demo/plan.md": "2026-10-08 10:02–10:03, 1 min\n"},
            },
        ],
        make=[{"stdout": output, "exit": 1}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    return world.calls("claude")[1]["prompt_file"]


def test_the_repair_prompt_names_the_gate_that_blocked_not_the_report_tail(world: World) -> None:
    # runner-red-gate criterion 1. Planted fault: the tail instead of the red sections.
    output = "\n".join(
        _gate("pytest", ["FAILED tests/test_app.py::test_value - assert 2 == 1", "1 failed, 9 passed"], "red")
        + _gate("ruff-check", ["All checks passed!"], "green")
        + _gate("markdownlint", [f"README.md:{n} error MD013" for n in range(500)], "report")
        + ["VERIFY RED — at least one gate failed; the report above names it."]
    )
    prompt = _red_run(world, output)
    assert "FAILED tests/test_app.py::test_value" in prompt and "── [pytest] RED (block)" in prompt
    assert "MD013" not in prompt and "[ruff-check]" not in prompt, "only blocking sections travel"


def test_a_blocking_gates_standard_error_reaches_the_repair_prompt(world: World) -> None:
    # Loop row L1-1: a gate's error on standard error arrives after every frame and must still travel.
    world.script(
        claude=[
            {
                "stdout": "first",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"},
            },
            {
                "stdout": "fixed",
                "append": {"plans/changes/demo/plan.md": "2026-10-08 10:02–10:03, 1 min\n"},
            },
        ],
        make=[
            {
                "stdout": "\n".join(_gate("shellcheck", [], "red")),
                "stderr": "sh: shellcheck: command not found\n",
                "exit": 1,
            },
            {"stdout": "green\n"},
        ],
    )
    assert world.run("implement") == 0
    prompt = world.calls("claude")[1]["prompt_file"]
    assert "── [shellcheck] RED (block)" in prompt and "shellcheck: command not found" in prompt


def test_a_long_standard_error_is_cut_with_a_marker(world: World) -> None:
    # Loop row L2-3 and criterion 5: the standard-error window is bounded and says what it left out.
    world.script(
        claude=[
            {
                "stdout": "first",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"},
            },
            {
                "stdout": "fixed",
                "append": {"plans/changes/demo/plan.md": "2026-10-08 10:02–10:03, 1 min\n"},
            },
        ],
        make=[
            {
                "stdout": "\n".join(_gate("pytest", ["FAILED x"], "red")),
                "stderr": "\n".join(f"err-{n}" for n in range(100)),
                "exit": 1,
            },
            {"stdout": "green\n"},
        ],
    )
    assert world.run("implement") == 0
    prompt = world.calls("claude")[1]["prompt_file"]
    assert "err-99" in prompt and "err-60" in prompt and "err-59\n" not in prompt
    assert "[… 60 earlier lines left out …]" in prompt


def test_a_gate_closes_on_any_verdict_spelling() -> None:
    # Loop row L2-1: a renamed green verdict must not swallow the following red gate.
    output = [
        "── [ruff] $ ruff",
        "ok",
        "── [ruff] green",
        "── [pytest] $ pytest",
        "FAILED y",
        "── [pytest] RED (block) — x",
    ]
    found = stage2.red_sections("\n".join(output))
    assert found is not None and "FAILED y" in found and "ok" not in found


def test_a_frame_quoted_inside_a_gate_opens_no_section() -> None:
    # Loop row L1-2: another gate's frames printed inside the open gate are data. Accepted limit: a quoted end
    # line of the open gate itself is indistinguishable from the real one and closes the section there.
    body = ["── [ghost] $ quoted", "── [ghost] RED (block) — quoted", "real-failure"]
    found = stage2.red_sections("\n".join(_gate("pytest", body, "red") + _gate("ruff", ["ok"], "green")))
    assert found.count("── [pytest] $") == 1 and "real-failure" in found
    assert found.splitlines()[-1].startswith("── [pytest] RED (block) — der Lauf ist rot.")


def test_red_sections_are_bounded_and_say_what_they_left_out() -> None:
    # runner-red-gate criterion 2, phase 6 F-2: markers count against both bounds.
    long = _gate("pytest", [f"trace-{n}" for n in range(1000)], "red")
    found = stage2.red_sections("\n".join(long))
    lines = found.splitlines()
    assert len(lines) == stage2.RED_SECTION_LINES and "trace-999" in found and "trace-0\n" not in found
    assert "lines of this gate left out" in lines[1] and lines[0].startswith("── [pytest] $")
    assert lines[-1].startswith("── [pytest] RED (block)")
    for count in (2, 3, 4, 6, 7, 70):
        many = []
        for number in range(count):
            many += _gate(f"gate-{number}", [f"g{number}-{n}" for n in range(100)], "red")
        assert len(stage2.red_sections("\n".join(many)).splitlines()) <= stage2.RED_TOTAL_LINES, count


def test_every_blocking_gate_keeps_its_frame_and_last_line() -> None:
    # Phase 6, F-1: the budget is shared, so the fourth of four red gates is not left out.
    many = []
    for number in range(4):
        many += _gate(f"gate-{number}", [f"g{number}-{n}" for n in range(100)], "red")
    found = stage2.red_sections("\n".join(many))
    for number in range(4):
        assert f"── [gate-{number}] RED (block)" in found and f"g{number}-99" in found, number


def test_a_frame_printed_onto_a_gates_last_line_is_still_a_frame() -> None:
    # Phase 6, F-3: a gate whose output ends without a newline must not swallow the gates after it.
    output = ["── [ruff] $ ruff", "no newline at the end── [ruff] gruen", *_gate("pytest", ["FAILED z"], "red")]
    output += [f"README.md:{n} error MD013" for n in range(500)]
    found = stage2.red_sections("\n".join(output))
    assert found is not None and "FAILED z" in found and "no newline" not in found


def test_the_frames_red_sections_reads_are_the_ones_verify_all_prints() -> None:
    # runner-red-gate pre-mortem: verify_all.sh renames its frame lines and the parser finds nothing.
    # The printed format, not the shell spelling (loop row L1-3): `── [<gate>] $ ` and `── [<gate>] RED (block)`.
    script = (REPO_ROOT / "scripts" / "verify_all.sh").read_text(encoding="utf-8")
    assert re.search(r"── \[\$\{?\w+\}?\] \$ ", script) and re.search(r"── \[\$\{?\w+\}?\] RED \(block\)", script)
    assert stage2.GATE_START.match("── [pytest] $ make test") and stage2.GATE_END.match("── [pytest] RED (block) — x")


def test_without_a_red_frame_the_repair_prompt_keeps_the_tail(world: World) -> None:
    # runner-red-gate criterion 3. Planted fault: empty diagnostics when nothing is framed.
    prompt = _red_run(world, "\n".join(f"make-{n}" for n in range(100)))
    assert "make-99" in prompt and "make-20" in prompt and "make-19" not in prompt


def test_a_red_section_is_scrubbed_of_the_glm_key(world: World) -> None:
    # runner-red-gate criterion 4. Planted fault: the red section passed unscrubbed.
    output = "\n".join(_gate("pytest", [f"E   AssertionError: token {KEY}"], "red"))
    prompt = _red_run(world, output)
    assert "── [pytest] RED (block)" in prompt and KEY not in prompt


def test_a_time_heading_deleted_mid_run_becomes_a_repair_diagnostic(world: World) -> None:
    valid = "---\ntitle: Plan\nupdated: 2026-10-07\nbead: demo-1\n---\n\n# Plan\n\n## Time used\n"
    world.script(
        claude=[
            {"stdout": "first", "plant": {"plans/changes/demo/plan.md": "# no time heading\n"}},
            {
                "stdout": "repaired",
                "plant": {"plans/changes/demo/plan.md": valid + "2026-10-07 10:00–10:04, 4 min\n"},
            },
        ],
        make=[{"stdout": "green\n"}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert "has no `## Time used` heading" in world.calls("claude")[1]["prompt_file"]


def test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading(
    world: World,
) -> None:
    gone = "# no time heading\n"
    world.script(
        claude=[
            {"stdout": "first", "plant": {"plans/changes/demo/plan.md": gone}},
            {"stdout": "second", "plant": {"plans/changes/demo/plan.md": gone}},
            {
                "stdout": "fallback",
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:09, 9 min\n"},
            },
        ],
        make=[{"stdout": "green\n"}, {"stdout": "green\n"}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    calls = world.calls("claude")
    assert len(calls) == 3
    prompt = calls[2]["prompt_file"]
    assert "Attempt 1 (flash)" in prompt and "Attempt 2 (flash-repair)" in prompt
    assert prompt.count("has no `## Time used` heading") == 2
    plan = world.plan.read_text(encoding="utf-8")
    assert plan.index("## Runner route") < plan.index("## Time used")
    assert "attempt 3 · route stage-1" in world.text()


def test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on Stage 1: {name}"))
    successful_implementation(world)
    assert world.run("implement", "demo", "--stage2-off", "Z.ai unavailable") == 0
    calls = world.calls("claude")
    assert len(calls) == 1
    argv, env = calls[0]["argv"], calls[0]["env"]
    assert argv[argv.index("--model") + 1] == "claude-sonnet-5-5"
    assert argv[argv.index("--effort") + 1] == "medium"
    assert "ANTHROPIC_BASE_URL" not in env and "ANTHROPIC_AUTH_TOKEN" not in env
    plan = world.plan.read_text(encoding="utf-8")
    assert "reason: Z.ai unavailable" in plan
    assert plan.index("## Runner route") < plan.index("## Time used")


def test_a_leak_between_work_attempts_stops_before_fallback(world: World) -> None:
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/leak.txt": LEAK}},
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 2
    assert len(world.calls("claude")) == 1


def test_a_stage1_route_line_is_written_only_after_a_clean_leak_check(world: World) -> None:
    (world.root / "src/leak.txt").write_text(LEAK, encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "planted leak")
    before = world.plan.read_bytes()
    assert world.run("implement", "demo", "--stage2-off", "Z.ai unavailable") == 2
    assert world.calls() == [] and world.plan.read_bytes() == before


def test_a_changed_file_with_the_glm_key_is_cleaned_and_refused(world: World) -> None:
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "credential = '@KEY@'\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "must not run"}],
    )
    assert world.run("implement") == 2
    assert len(world.calls("claude")) == 1 and world.calls("make") == []
    source = (world.root / "src/app.py").read_text(encoding="utf-8")
    assert "[credential]" in source and KEY not in source


def test_a_key_written_by_the_gate_into_a_changed_file_is_removed_and_refused(world: World) -> None:
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n", "plant": {"src/app.py": f"credential = '{KEY}'\n"}}],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("implement") == 2
    assert len(world.calls("claude")) == 1
    assert git(world.root, "rev-parse", "HEAD") == before
    source = (world.root / "src/app.py").read_text(encoding="utf-8")
    assert "[credential]" in source and KEY not in source


def test_a_key_in_a_gitignored_file_written_by_the_run_is_removed_and_refused(world: World) -> None:
    (world.root / ".gitignore").write_text("*.local\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "ignore *.local")
    old = world.root / "old.local"
    old.write_text(f"mine = {KEY}\n", encoding="utf-8")  # there before the run: not the run's
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"new.local": f"token = {KEY}\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n"}],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("implement") == 2
    assert len(world.calls("claude")) == 1
    assert git(world.root, "rev-parse", "HEAD") == before
    planted = (world.root / "new.local").read_text(encoding="utf-8")
    assert "[credential]" in planted and KEY not in planted
    assert KEY in old.read_text(encoding="utf-8")


def test_scrub_replaces_every_fragment_of_eight_or_more_characters() -> None:
    half = len(KEY) // 2
    printed = f"a {KEY[:half]} and {KEY[half:]} b"
    cleaned = stage2.scrub(printed, KEY)
    assert cleaned == "a [credential] and [credential] b"
    assert stage2.scrub(f"prefix {KEY[:8]} only", KEY) == "prefix [credential] only"
    assert stage2.scrub(f"mid {KEY[5:21]} run", KEY) == "mid [credential] run"
    assert stage2.scrub(f"short {KEY[:7]} stays", KEY) == f"short {KEY[:7]} stays"
    assert stage2.scrub(f"whole {KEY}!", KEY) == "whole [credential]!"
    assert stage2.scrub(KEY, None) == KEY
    assert stage2.replace_credential(f"x{KEY[3:15]}y".encode(), KEY) == b"x[credential]y"


def test_a_key_fragment_never_survives_the_relayed_streams(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    world.script(
        claude=[
            {"stdout": "the model saw @KEY@\n" + KEY[:8] + " tail", "stderr": KEY[10:20], "exit": 1},
            {"stdout": f"fact {KEY[:8]} and {KEY[16:]}"},
        ]
    )
    assert world.run("explore") == 1
    seen = capsys.readouterr()
    assert KEY[10:18] not in seen.err and "[credential]" in seen.err
    assert world.run("explore") == 0
    text = world.research.read_text(encoding="utf-8")
    assert not any(KEY[i : i + 8] in text for i in range(len(KEY) - 7))
    assert "fact [credential] and [credential]" in text


def test_a_key_fragment_in_a_changed_file_is_removed_and_refused(world: World) -> None:
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": f"credential = '{KEY[4:16]}'\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n"}],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("implement") == 2
    assert len(world.calls("claude")) == 1
    assert git(world.root, "rev-parse", "HEAD") == before
    source = (world.root / "src/app.py").read_text(encoding="utf-8")
    assert source == "credential = '[credential]'\n"


def test_a_key_the_gate_writes_under_venv_is_removed_and_refused(world: World) -> None:
    (world.root / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    (world.root / ".venv").mkdir()
    old = world.root / ".venv" / "old.txt"
    old.write_text(f"mine = {KEY}\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "ignore .venv")
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n", "plant": {".venv/gate.txt": f"token = {KEY}\n"}}],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("implement") == 2
    assert len(world.calls("claude")) == 1
    assert git(world.root, "rev-parse", "HEAD") == before
    written = (world.root / ".venv" / "gate.txt").read_text(encoding="utf-8")
    assert "[credential]" in written and KEY not in written
    assert KEY in old.read_text(encoding="utf-8")


def test_a_key_in_the_gate_output_never_reaches_the_next_attempt(world: World) -> None:
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {
                "stdout": "repaired",
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:06, 6 min\n"},
            },
        ],
        make=[{"stdout": f"token {KEY} leaked\n", "exit": 1}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    prompt = world.calls("claude")[1]["prompt_file"]
    assert KEY not in prompt and "token [credential] leaked" in prompt


def test_findings_only_dirt_is_allowed_and_committed(world: World) -> None:
    world.findings.write_text("# Findings\n\nEarlier failed attempt.\n", encoding="utf-8")
    successful_implementation(world)
    assert world.run("implement") == 0
    assert git(world.root, "status", "--porcelain") == ""
    assert "Earlier failed attempt." in world.text()


def test_a_findings_file_an_implement_run_creates_names_claude_code(world: World) -> None:
    # Repair L2-1. Planted fault: `producer_for` falls through to `pi` for the GLM endpoints.
    assert not world.findings.exists()
    successful_implementation(world)
    assert world.run("implement") == 0
    header = plans_registry._frontmatter(world.findings)
    assert header is not None and header["produced_by"]["name"] == "claude-code"


# ---------------------------------------------------------------------------
# The draft (phases 2, 2b and 3; spec criteria 1-26)
# ---------------------------------------------------------------------------


PLAN_CARD = (
    "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n"
    "```text\n"
    "For you:     one command drafts the change\n"
    "Done when:   the criteria hold\n"
    "Appetite:    8 h\n"
    "Not now:     nothing\n"
    "Pre-mortem:  it failed\n"
    "```\n\n## Time used\n"
)


def draft_world(world: World) -> None:
    """A change a draft can start from: no spec, no plan, a decisions.md with its bead, committed.

    The commit that adds the existing ADR is also where `origin/main` goes, so the merge base a
    `draft_keep` reads holds that ADR and only a second, new one counts as new (spec, criterion 8).
    """
    folder = world.root / "plans" / "changes" / "demo"
    (folder / "spec.md").unlink()
    world.plan.unlink()
    (folder / "decisions.md").write_text(
        "---\ntitle: Decisions\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Decisions\n\nQ-1 answered.\n",
        encoding="utf-8",
    )
    (world.root / "docs" / "adr").mkdir(parents=True)
    (world.root / "docs" / "adr" / "0007-existing-record.md").write_text("# ADR\n\nheld.\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "decisions")
    git(world.root, "update-ref", "refs/remotes/origin/main", "HEAD")


def clear_derived_leftovers(world: World) -> None:
    """Remove what a failed run's `prepare_derived` left untracked; the next run would refuse it."""
    (world.root / "plans" / "INDEX.md").unlink(missing_ok=True)
    for cache in (world.root / "scripts").rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)


def passing_draft(world: World) -> None:
    """One Codex step that plants spec and plan, and a `make` that answers green."""
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                },
            )
        ],
        make=[{"stdout": "green\n"}],
    )


def red_verify(*gates: list[str]) -> dict:
    """A red `make verify` with the given blocking gate bodies; `gates` entries are (name, lines)."""
    output = ""
    for name, lines in gates:
        output += "\n".join(_gate(name, lines, "red"))
    return {"stdout": output, "exit": 1}


def test_a_draft_starts_codex_with_workspace_write_and_no_bypass(world: World) -> None:
    # Criterion 1. Planted fault: the draft call keeps `read-only`, or passes `--add-dir`.
    draft_world(world)
    passing_draft(world)
    assert world.run("draft") == 0
    (call,) = world.calls("codex")
    argv = call["argv"]
    assert argv[:2] == ["exec", "--json"]
    assert argv[argv.index("-m") + 1] == "gpt-6.1-sol"
    assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["draft"]}"' in argv
    assert 'sandbox_mode="workspace-write"' in argv
    assert 'sandbox_mode="read-only"' not in argv
    disabled = [argv[i + 1] for i, word in enumerate(argv) if word == "--disable"]
    assert sorted(disabled) == ["hooks", "memories"]
    for flag in (
        "--add-dir",
        "--approve-for-me",
        "--dangerously-bypass-approvals-and-sandbox",
        "-s",
        "--sandbox",
        "--ephemeral",
    ):
        assert flag not in argv


def test_a_findings_file_the_draft_creates_names_codex(world: World) -> None:
    # Repair L1-4. Planted fault: the header's producer stays `claude-code` whatever the endpoint.
    draft_world(world)
    assert not world.findings.exists()
    passing_draft(world)
    assert world.run("draft") == 0
    header = plans_registry._frontmatter(world.findings)
    assert header is not None and header["produced_by"]["name"] == "codex"


def test_the_draft_prompt_carries_the_three_phase_prompts_and_the_rules(world: World) -> None:
    # Criterion 3. Planted fault: the prompt built without `03-plan.md`, or for another change.
    draft_world(world)
    passing_draft(world)
    assert world.run("draft") == 0
    prompt = world.calls("codex")[0]["argv"][-1]
    for name in ("02-spec.md", "02b-design.md", "03-plan.md"):
        assert (REPO_ROOT / "prompts" / name).read_text(encoding="utf-8").rstrip() in prompt, name
    assert "## Repository agent rules" in prompt and "Stay inside the repository." in prompt
    assert "Change: demo (`plans/changes/demo/`)" in prompt and "Change: other" not in prompt
    flat = " ".join(prompt.split())
    assert "the runner puts back every changed path outside the change folder except the one new ADR draft" in flat
    assert "the change's `decisions.md`" in flat and "Never write an answer for the maintainer" in flat
    assert "## Phase 2b prompt" in prompt and "## Phase 3 prompt" in prompt
    assert prompt.rstrip().endswith(stage2.READ_REQUEST)


def test_a_draft_without_decisions_or_a_research_bead_refuses(world: World) -> None:
    # Criterion 4. Planted fault: `required` left empty, or the bead file the wrong one.
    draft_world(world)
    (world.root / "plans/changes/demo/decisions.md").unlink()
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "no decisions")
    assert world.run("draft") == 2
    assert world.calls() == []
    (world.root / "plans/changes/demo/decisions.md").write_text(
        "---\ntitle: Decisions\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Decisions\n", encoding="utf-8"
    )
    (world.root / "plans/changes/demo/research.md").write_text(
        "---\ntitle: Research\nupdated: 2026-09-30\n---\n\n# Research\n", encoding="utf-8"
    )
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "no bead")
    assert world.run("draft") == 2
    assert world.calls() == []


def test_a_draft_refuses_changes_outside_findings(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 5. Planted fault: the pre-existing check skipped for the draft.
    draft_world(world)
    (world.root / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
    world.script(codex=[{"stdout": "must not run"}])
    assert world.run("draft") == 2
    assert world.calls() == []
    error = capsys.readouterr().err
    assert "pre-existing changes outside this change's findings.md" in error and "src/app.py" in error


def test_each_draft_attempt_has_its_audit_line_and_reason(world: World) -> None:
    # Criterion 6. Planted fault: the reason dropped from a fallback attempt's audit line.
    draft_world(world)
    world.script(
        codex=[
            codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}),
            codex_ok("T2", "drafted again"),
        ],
        claude=[{"stdout": "drafted by GLM"}],
        make=[red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert"]))] * 3,
    )
    assert world.run("draft") == 1
    text = world.text()
    day = r"\d{4}-\d{2}-\d{2}"
    count = r"\d+ files, \d+ commits, \d+ rules"
    assert re.search(
        rf"^Stage-2 call, {day}: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · "
        rf"leak check clean over {count}\.$",
        text,
        re.M,
    )
    assert re.search(
        rf"^Stage-2 call, {day}: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol"
        rf" · reason the first draft attempt failed · leak check clean over {count}\.$",
        text,
        re.M,
    )
    assert re.search(
        rf"^Stage-2 call, {day}: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5\.3"
        rf" · reason two Codex draft attempts failed · leak check clean over {count}\.$",
        text,
        re.M,
    )


def test_a_leak_before_a_draft_attempt_stops_the_chain(world: World) -> None:
    # Criterion 7. Planted fault: a `Refused` caught as a failed call, so a later attempt starts.
    draft_world(world)
    (world.root / "src" / "leak.txt").write_text(LEAK, encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "planted leak")
    world.script(codex=[{"stdout": "must not run"}, {"stdout": "nor this"}], claude=[{"stdout": "nor GLM"}])
    assert world.run("draft") == 2
    assert world.calls() == [], "a leak refusal starts no later attempt"


def test_paths_outside_the_change_folder_are_put_back_and_named(world: World) -> None:
    # Criterion 8. Planted fault: the put-back skipped, or an existing ADR kept as new.
    draft_world(world)
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                    "src/new.py": "new = 1\n",
                    "src/app.py": "value = 2\n",
                    "docs/adr/0007-existing-record.md": "# ADR\n\nedited by the model.\n",
                },
            )
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    assert git(world.root, "status", "--porcelain") == ""
    assert (world.root / "src" / "app.py").read_text(encoding="utf-8") == "value = 1\n"
    assert not (world.root / "src" / "new.py").exists()
    assert "edited by the model" not in (world.root / "docs" / "adr" / "0007-existing-record.md").read_text(
        encoding="utf-8"
    )
    committed = git(world.root, "show", "--name-only", "--pretty=format:", "HEAD").splitlines()
    assert "src/app.py" not in committed and "src/new.py" not in committed
    assert "docs/adr/0007-existing-record.md" not in committed
    assert "plans/changes/demo/decisions.md" not in committed
    block = quote_blocks(world.text())[0]
    assert block[0] == "Attempt 1 (codex): the runner put back what a draft may not change:"
    for path in ("`src/app.py`", "`src/new.py`", "`docs/adr/0007-existing-record.md`"):
        assert f"- {path}" in block, path


def test_the_put_back_names_every_path_beyond_the_bound(world: World) -> None:
    # 2a's F-8. Planted fault: the put-back listing stops at `ATTEMPT_FILES` and hides the last
    # path behind a remainder line, so the audit cannot name every restored path.
    draft_world(world)
    plant = {
        "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
        "plans/changes/demo/plan.md": PLAN_CARD,
    }
    for n in range(stage2.ATTEMPT_FILES + 1):
        plant[f"stray/file-{n:02d}.txt"] = f"stray {n}\n"
    world.script(codex=[codex_ok("T1", "drafted", plant=plant)], make=[{"stdout": "green\n"}])
    assert world.run("draft") == 0
    assert git(world.root, "status", "--porcelain") == ""
    block = quote_blocks(world.text())[0]
    assert block[0] == "Attempt 1 (codex): the runner put back what a draft may not change:"
    assert f"- `stray/file-{stage2.ATTEMPT_FILES:02d}.txt`" in block, "the path beyond the bound is named"
    assert "more files" not in "\n".join(block), "no remainder line hides a path"


def test_an_edited_decisions_file_is_put_back(world: World) -> None:
    # Criterion 9. Planted fault: `decisions.md` kept with the folder.
    draft_world(world)
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                    "plans/changes/demo/decisions.md": "---\ntitle: Decisions\nupdated: 2026-09-30\nbead: demo-1\n"
                    "---\n\n# Decisions\n\nQ-1 answered.\nQ-2 answered by the model.\n",
                },
            )
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    committed = git(world.root, "show", "--name-only", "--pretty=format:", "HEAD").splitlines()
    assert "plans/changes/demo/decisions.md" not in committed
    assert "Q-2 answered by the model" not in (world.root / "plans/changes/demo/decisions.md").read_text(
        encoding="utf-8"
    )
    assert "- `plans/changes/demo/decisions.md`" in quote_blocks(world.text())[0]


def test_two_new_adr_files_fail_the_attempt(world: World) -> None:
    # Criterion 10. Planted fault: no count of new ADR files.
    draft_world(world)
    plants = {
        "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
        "plans/changes/demo/plan.md": PLAN_CARD,
        "docs/adr/0016-first-record.md": "# First\n",
        "docs/adr/0017-second-record.md": "# Second\n",
    }
    world.script(
        codex=[codex_ok("T1", "drafted", plant=plants), codex_ok("T2", "again", plant=plants)],
        claude=[{"stdout": "glm", "plant": plants}],
        make=[{"stdout": "green\n"}] * 3,
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 1
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0", "no commit is made"
    block = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0]
    joined = "\n".join(block)
    assert "the attempt left more than one new ADR file" in joined
    assert "`docs/adr/0016-first-record.md`" in joined and "`docs/adr/0017-second-record.md`" in joined


def test_a_second_draft_that_adds_another_adr_fails_the_attempt(world: World) -> None:
    # 2a's F-5. Planted fault: the count reads only paths changed against HEAD, so the first
    # draft's committed ADR no longer counts and a second one reaches the commit.
    draft_world(world)
    first = {
        "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
        "plans/changes/demo/plan.md": PLAN_CARD,
        "docs/adr/0016-first-record.md": "# First\n",
    }
    world.script(codex=[codex_ok("T1", "drafted", plant=first)], make=[{"stdout": "green\n"}])
    assert world.run("draft") == 0
    (world.bin / "calls.jsonl").unlink()
    second = {"docs/adr/0017-second-record.md": "# Second\n"}
    world.script(
        codex=[codex_ok("T1", "again", plant=second), codex_ok("T2", "once more", plant=second)],
        claude=[{"stdout": "glm", "plant": second}],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 1
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0", "no second commit is made"
    block = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0]
    joined = "\n".join(block)
    assert "the attempt left more than one new ADR file" in joined
    assert "`docs/adr/0016-first-record.md`" in joined and "`docs/adr/0017-second-record.md`" in joined


def test_a_draft_call_that_moves_head_stops_the_run(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 11. Planted fault: the HEAD check after the put-back, or skipped.
    draft_world(world)
    started = [0]

    def committing_codex(ctx, prompt, resume=None, writable=False, verb=""):
        del prompt, resume, writable, verb
        git(ctx.root, "commit", "--quiet", "--allow-empty", "-m", "the model committed")
        started[0] += 1
        return "drafted", "T1"

    monkeypatch.setattr(stage2, "run_codex", committing_codex)
    assert world.run("draft") == 1
    assert started == [1], "no later attempt starts"
    error = capsys.readouterr().err
    assert "moved HEAD from" in error and "nothing was put back or committed" in error
    assert git(world.root, "log", "-1", "--pretty=%s") == "the model committed", "the runner makes no commit"


def test_a_red_verify_fails_the_draft_attempt(world: World) -> None:
    # Criterion 12. Planted fault: the exit code of `make verify` ignored, or `make` never run.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[
            codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}),
            codex_ok("T2", "again"),
        ],
        claude=[{"stdout": "glm"}],
        make=[red, red, red],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 1
    assert [call["argv"] for call in world.calls("make")] == [["verify"]] * 3
    block = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0]
    joined = "\n".join(block)
    assert "`make verify` exited 1" in joined and "── [pytest] RED (block)" in joined
    assert "FAILED tests/test_x.py::test_a" in joined
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0"


FEATURE_SPEC = (
    "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\nchange: demo\nclass: feature\n"
    'adr_question: {proposed: "no", answered_by: null, reason: "A reason."}\n---\n\n# Spec\n'
)


def test_only_the_changes_own_missing_adr_answer_is_tolerated(world: World) -> None:
    # Criterion 13 (phase-6 F-9, F-10: the gate tolerates, the exit code decides). Planted fault:
    # the runner does not ask the gate to tolerate this change, or does not say the answer is owed.
    draft_world(world)
    owed = (
        "adr-answers: demo: no answer — demo.rel is a feature and decisions/answers/demo/adr.yaml does not exist; "
        "fix: python3 scripts/harness.py decide adr"
    )
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={"plans/changes/demo/spec.md": FEATURE_SPEC, "plans/changes/demo/plan.md": PLAN_CARD},
            )
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    assert world.calls("make")[0]["env"][stage2.check_adr_answers.TOLERATE_ENV] == "demo"
    assert "ADR answer owed: decisions/answers/demo/adr.yaml does not exist" in world.text()
    assert "tolerated that for this run" in world.text()
    assert "was red only because" not in world.text(), "make verify exited 0 (F-14)"
    assert "the answer is the maintainer's" in world.text()
    assert git(world.root, "log", "-1", "--pretty=%s") == "docs(demo): draft spec and plan — route codex"

    (world.bin / "calls.jsonl").unlink()
    other = "\n".join(_gate("adr-answers", [owed.replace("demo:", "other:", 1)], "red"))
    world.script(
        codex=[codex_ok("T1", "drafted"), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": other, "exit": 1}] * 3,
    )
    assert world.run("draft") == 1
    assert world.text().count("ADR answer owed") == 1, "another change's missing answer is not tolerated"
    (world.bin / "calls.jsonl").unlink()
    second_gate = "\n".join(
        _gate("adr-answers", [owed], "red") + _gate("pytest", ["FAILED tests/test_x.py::test_a"], "red")
    )
    world.script(
        codex=[codex_ok("T1", "drafted"), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": second_gate, "exit": 1}] * 3,
    )
    assert world.run("draft") == 1
    assert world.text().count("ADR answer owed") == 1, "a second blocking gate is not tolerated"
    (world.bin / "calls.jsonl").unlink()
    no_time = PLAN_CARD.replace("\n## Time used\n", "\n")
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": no_time}), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "\n".join(_gate("adr-answers", [owed], "red")), "exit": 1}] * 3,
    )
    assert world.run("draft") == 1
    assert "plans/changes/demo/plan.md has no `## Time used` heading." in world.text()
    assert world.text().count("ADR answer owed") == 1, "criteria 14 to 16 still apply"


OWED_ANSWER = (
    "adr-answers: demo: no answer — demo.rel is a feature and decisions/answers/demo/adr.yaml does not exist; "
    "fix: python3 scripts/harness.py decide adr"
)


def refused_verification(world: World, verification: str) -> None:
    """Run a draft whose every `make verify` prints `verification` and exits 1; nothing may be committed."""
    draft_world(world)
    planted = {
        "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
        "plans/changes/demo/plan.md": PLAN_CARD,
    }
    world.script(
        codex=[codex_ok("T1", "drafted", plant=planted), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": verification, "exit": 1}] * 3,
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 1
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0", "the draft was committed"
    assert "ADR answer owed" not in world.text()
    block = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0]
    assert "`make verify` exited 1" in "\n".join(block)


def test_a_verification_that_stopped_before_its_gates_closed_owes_nothing(world: World) -> None:
    # 2a's F-6, first case. Planted fault: the exception reads only the gates that closed, so the
    # missing ADR answer followed by an unfinished `interview-minimums` gate passes for tolerated.
    interview = "── [interview-minimums] $ run the gate\nhalf the report\n"
    refused_verification(world, "\n".join(_gate("adr-answers", [OWED_ANSWER], "red")) + interview)


def test_a_gate_output_printing_a_green_frame_does_not_hide_its_red_frame(world: World) -> None:
    # 2a's F-6, second case. Planted fault: a pytest line `── [pytest] gruen` in a gate's output
    # passes for the gate's closing frame, hiding the real RED one.
    spoofed = "\n".join(
        _gate("adr-answers", [OWED_ANSWER], "red")
        + _gate("pytest", ["FAILED tests/test_x.py::test_a", "── [pytest] gruen"], "red")
    )
    refused_verification(world, spoofed)


def test_a_verification_that_ended_right_after_the_adr_gate_owes_nothing(world: World) -> None:
    # Phase-6 F-9. Planted fault: the exception reads gate frames, so output that stops right after the
    # missing-answer gate closed - before the next gate started - looks like a complete run.
    refused_verification(world, "\n".join(_gate("adr-answers", [OWED_ANSWER], "red")))


def test_a_failing_gate_printing_gate_frames_cannot_hide_its_red_frame(world: World) -> None:
    # Phase-6 F-10. Planted fault: a failing pytest gate prints `── [pytest] gruen` and a start frame of
    # ruff-check, the frame reader follows them and the real RED frame of pytest goes unseen.
    spoofed = "\n".join(
        _gate("pytest", ["── [pytest] gruen", "── [ruff-check] $ captured command"], "red")
        + _gate("ruff-check", [], "green")
        + _gate("adr-answers", [OWED_ANSWER], "red")
    )
    refused_verification(world, spoofed)


def test_a_rename_of_the_drafts_own_unmerged_adr_counts_one_adr(world: World) -> None:
    # Phase-6 F-11. Planted fault: the count includes the deleted old path, so a rename reads as two new ADRs.
    draft_world(world)
    first = {
        "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
        "plans/changes/demo/plan.md": PLAN_CARD,
        "docs/adr/0016-first-record.md": "# First\n",
    }
    world.script(codex=[codex_ok("T1", "drafted", plant=first)], make=[{"stdout": "green\n"}])
    assert world.run("draft") == 0
    (world.bin / "calls.jsonl").unlink()
    world.script(
        codex=[
            codex_ok(
                "T1",
                "renamed",
                plant={"docs/adr/0016-renamed-record.md": "# First\n"},
                delete=["docs/adr/0016-first-record.md"],
            )
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    assert (world.root / "docs/adr/0016-renamed-record.md").is_file()
    assert not (world.root / "docs/adr/0016-first-record.md").exists()


def test_put_back_paths_are_named_in_full_however_long(world: World) -> None:
    # Phase-6 F-12. Planted fault: quote_block cuts each put-back path at 500 characters, so two
    # long paths that share their first 500 characters become one line.
    draft_world(world)
    head = "src/" + "d" * 250 + "/" + "e" * 250 + "/"
    tail = 616 - len(head)
    one = head + "f" * (tail - len("one.txt")) + "one.txt"
    two = head + "f" * (tail - len("two.txt")) + "two.txt"
    assert len(one) == len(two) == 616
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                    one: "x\n",
                    two: "y\n",
                },
            )
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    text = world.text()
    assert f"> - `{one}`" in text and f"> - `{two}`" in text


def test_a_put_back_path_with_a_newline_is_never_cut() -> None:
    # Phase-6 F-15. Planted fault: quote_block compares the split lines of an entry with the whole
    # entries, so the long continuation line of a multiline path is cut and two paths become one.
    head = "src/dir\n" + "e" * 600 + "/"
    one, two = head + "one.txt", head + "two.txt"
    entries = stage2.put_back_lines([one, two])
    block = stage2.quote_block("Attempt 1 (codex): put back:\n" + "\n".join(entries), None, entries)
    assert "left out" not in block
    assert one.split("\n")[1] in block and two.split("\n")[1] in block


def test_a_make_that_cannot_start_fails_the_attempt_and_moves_the_chain(world: World) -> None:
    # 2a's F-7. Planted fault: the `CallFailed` of a make that cannot start escapes the post-run
    # checks, so the runner stops after one attempt without a block and starts no later route.
    draft_world(world)
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                },
            ),
            codex_ok("T2", "again"),
        ],
        claude=[{"stdout": "glm drafted"}],
    )
    (world.bin / "make").chmod(0o644)
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 1
    assert world.calls("make") == [], "make never ran"
    assert len(world.calls("codex")) == 2 and len(world.calls("claude")) == 1
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0"
    block = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0]
    joined = "\n".join(block)
    assert "`make verify` could not run" in joined and "could not be started" in joined
    assert "Permission denied" in joined


def test_a_missing_spec_or_plan_fails_the_attempt(world: World) -> None:
    # Criterion 14. Planted fault: only `plan.md` checked.
    draft_world(world)
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("draft") == 1
    assert "plans/changes/demo/spec.md is missing after the draft." in world.text()
    world.plan.unlink()
    clear_derived_leftovers(world)
    (world.bin / "calls.jsonl").unlink()
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                },
            ),
            codex_ok("T2", "again"),
        ],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("draft") == 1
    assert "plans/changes/demo/plan.md is missing after the draft." in world.text()


def test_a_missing_plan_md_is_reported_once(world: World) -> None:
    # Repair L3-4. Planted fault: the card and Time-used checks read an empty string for an absent plan.md.
    draft_world(world)
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                },
            ),
            codex_ok("T2", "again"),
        ],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("draft") == 1
    text = world.text()
    assert "plans/changes/demo/plan.md is missing after the draft." in text
    assert stage2.CARD_PROBLEM not in text
    assert "has no `## Time used` heading" not in text


def test_a_plan_without_its_card_fails_the_attempt(world: World) -> None:
    # Criterion 15. Planted fault: the labels looked for anywhere in the file.
    draft_world(world)
    no_pre = PLAN_CARD.replace("Pre-mortem:  it failed\n", "")
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": no_pre}), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("draft") == 1
    assert stage2.CARD_PROBLEM in world.text()
    world.plan.unlink()
    clear_derived_leftovers(world)
    (world.bin / "calls.jsonl").unlink()
    late = (
        "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n## Criterion ledger\n\n"
        "```text\nFor you:     x\nDone when:   y\nAppetite:    8 h\nNot now:     n\nPre-mortem:  p\n```\n\n## Time used\n"
    )
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": late}), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("draft") == 1
    assert stage2.CARD_PROBLEM in world.text()


def test_a_plan_without_time_used_fails_the_attempt(world: World) -> None:
    # Criterion 16. Planted fault: the heading check left out.
    draft_world(world)
    no_time = PLAN_CARD.replace("\n## Time used\n", "\n")
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": no_time}), codex_ok("T2", "again")],
        claude=[{"stdout": "glm"}],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("draft") == 1
    assert "plans/changes/demo/plan.md has no `## Time used` heading." in world.text()


def test_a_passing_draft_makes_one_commit_and_leaves_a_clean_tree(world: World) -> None:
    # Criterion 17. Planted fault: `findings.md` written after the commit, or a second commit made.
    draft_world(world)
    passing_draft(world)
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 0
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "1"
    assert git(world.root, "log", "-1", "--pretty=%s") == "docs(demo): draft spec and plan — route codex"
    assert git(world.root, "status", "--porcelain") == ""
    committed = git(world.root, "show", "--name-only", "--pretty=format:", "HEAD").splitlines()
    for name in ("plans/changes/demo/spec.md", "plans/changes/demo/plan.md", "plans/changes/demo/findings.md"):
        assert name in committed, name


def test_a_failed_first_draft_gets_one_codex_repair_with_its_diagnostics(world: World) -> None:
    # Criterion 18. Planted fault: the diagnostics not passed to the second prompt.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[
            codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}),
            codex_ok(
                "T2",
                "repaired",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                },
            ),
        ],
        make=[red, {"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    assert len(world.calls("codex")) == 2
    assert world.calls("claude") == []
    for call in world.calls("codex"):  # the retry keeps the draft entry (bead coding-harness-yzk)
        assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["draft"]}"' in call["argv"]
    prompt = world.calls("codex")[1]["argv"][-1]
    assert "## Earlier attempts' diagnostics" in prompt
    assert "Attempt 1 (codex)" in prompt and "── [pytest] RED (block)" in prompt
    assert git(world.root, "log", "-1", "--pretty=%s") == "docs(demo): draft spec and plan — route codex-repair"


def test_two_failed_codex_attempts_fall_back_to_glm_5_3(world: World) -> None:
    # Criterion 19. Planted fault: the GLM route on `glm-5.3-flash`, a shell tool, or a fourth attempt.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}), codex_ok("T2", "again")],
        claude=[
            {
                "stdout": "glm drafted",
                "plant": {
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                },
            }
        ],
        make=[red, red, {"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    assert len(world.calls("codex")) == 2
    (call,) = world.calls("claude")
    argv, prompt = call["argv"], call["prompt_file"]
    assert argv[argv.index("--model") + 1] == "glm-5.3"
    assert argv[argv.index("--effort") + 1] == "max"
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"Read", "Grep", "Glob", "Edit", "Write"}
    assert "glm-5.3-flash" not in argv
    for name in ("02-spec.md", "02b-design.md", "03-plan.md"):
        assert (REPO_ROOT / "prompts" / name).read_text(encoding="utf-8").rstrip() in prompt, name
    assert "Attempt 1 (codex)" in prompt and "Attempt 2 (codex-repair)" in prompt
    assert git(world.root, "log", "-1", "--pretty=%s") == "docs(demo): draft spec and plan — route glm"


def test_a_failed_draft_call_is_put_back_and_recorded(world: World) -> None:
    # Criterion 20. Planted fault: the put-back left out after a dead call, or no block written.
    draft_world(world)
    world.script(
        codex=[
            {"stdout": "", "exit": 1, "plant": {"plans/changes/demo/spec.md": "# half-written spec\n"}},
            codex_ok(
                "T2",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                },
            ),
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    block = quote_blocks(world.text())[0]
    assert block[0].startswith("Attempt 1 (codex) failed its call:")
    assert "The runner put back:" in block and "- `plans/changes/demo/spec.md`" in block
    committed = git(world.root, "show", "--name-only", "--pretty=format:", "HEAD").splitlines()
    assert "plans/changes/demo/spec.md" in committed
    assert "half-written" not in (world.root / "plans/changes/demo/spec.md").read_text(encoding="utf-8")


def test_a_failed_draft_check_leaves_its_block_and_its_tree(world: World) -> None:
    # Criterion 21. Planted fault: the tree put back after a post-run failure.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[
            codex_ok(
                "T1",
                "drafted",
                plant={
                    "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
                    "plans/changes/demo/plan.md": PLAN_CARD,
                },
            ),
            codex_ok("T2", "passed on the tree the first attempt left"),
        ],
        make=[red, {"stdout": "green\n"}],
    )
    assert world.run("draft") == 0
    (block,) = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]]
    files = "\n".join(block)
    assert "plans/changes/demo/spec.md" in files and "plans/changes/demo/plan.md" in files
    prompt = world.calls("codex")[1]["argv"][-1]
    assert "Attempt 1 (codex)" in prompt and "── [pytest] RED (block)" in prompt
    committed = git(world.root, "show", "--name-only", "--pretty=format:", "HEAD").splitlines()
    assert "plans/changes/demo/spec.md" in committed and "plans/changes/demo/plan.md" in committed


def test_three_failed_draft_attempts_exit_1_without_a_commit(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 22. Planted fault: the loop ends without raising, or a commit is still made.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[
            codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}),
            codex_ok("T2", "again"),
        ],
        claude=[{"stdout": "glm"}],
        make=[red, red, red],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 1
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0"
    assert "findings.md" in capsys.readouterr().err
    blocks_ = [b for b in quote_blocks(world.text()) if "post-run checks" in b[0]]
    assert [block[0] for block in blocks_] == [
        "Attempt 1 (codex) failed its post-run checks.",
        "Attempt 2 (codex-repair) failed its post-run checks.",
        "Attempt 3 (glm) failed its post-run checks.",
    ]


def test_a_codex_draft_never_reads_the_glm_key(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    # Criterion 23. Planted fault: the key read before the loop.
    draft_world(world)
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on a Codex draft: {name}"))
    passing_draft(world)
    assert world.run("draft") == 0


def test_a_missing_glm_key_refuses_the_glm_draft_attempt(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 24. Planted fault: a `None` key passed to the GLM call.
    draft_world(world)
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}), codex_ok("T2", "again")],
        claude=[{"stdout": "must not run"}],
        make=[red, red],
    )
    assert world.run("draft") == 2
    assert len(world.calls("codex")) == 2 and world.calls("claude") == []
    assert "GLM_KEY" in capsys.readouterr().err


def test_a_glm_draft_that_writes_the_key_is_refused_without_a_commit(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 25. Planted fault: the scan skipped on the GLM route.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[{"stdout": "drafted"}, {"stdout": "again"}],
        claude=[{"stdout": "glm drafted", "plant": {"plans/changes/demo/spec.md": "the key was @KEY@\n"}}],
        make=[red, red, {"stdout": "green\n"}],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 2
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0"
    spec = (world.root / "plans/changes/demo/spec.md").read_text(encoding="utf-8")
    assert "[credential]" in spec and not any(KEY[i : i + 8] in spec for i in range(len(KEY) - 7))
    text = world.text()
    assert not any(KEY[i : i + 8] in text for i in range(len(KEY) - 7))
    assert "refused" in capsys.readouterr().err


def test_a_failed_glm_draft_call_that_writes_the_key_is_refused(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Repair L2-4. Planted fault: the failed-call branch scans nothing, so the key stays in findings.md.
    draft_world(world)
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
    world.script(
        codex=[{"stdout": "drafted"}, {"stdout": "again"}],
        claude=[{"stdout": "", "exit": 1, "append": {"plans/changes/demo/findings.md": "the key was @KEY@\n"}}],
        make=[red, red],
    )
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 2
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0"
    text = world.text()
    assert "[credential]" in text and not any(KEY[i : i + 8] in text for i in range(len(KEY) - 7))
    assert "refused" in capsys.readouterr().err


def test_a_glm_draft_that_writes_the_key_and_moves_head_still_refuses(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Repair L3-2. Planted fault: the moved-HEAD stop runs before the credential scan, so the key stays.
    draft_world(world)

    def committing_glm(ctx, prompt, endpoint, writable=False, key=None):
        del prompt, endpoint, writable
        (ctx.root / "plans" / "changes" / "demo" / "spec.md").write_text(f"the key was {key}\n", encoding="utf-8")
        git(ctx.root, "commit", "--quiet", "--allow-empty", "-m", "the model committed")
        return "drafted"

    monkeypatch.setattr(stage2, "run_work_model", committing_glm)
    world.script(codex=[{"stdout": "drafted"}, {"stdout": "again"}])
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 2
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "1", "only the model's commit stands"
    spec = (world.root / "plans" / "changes" / "demo" / "spec.md").read_text(encoding="utf-8")
    assert "[credential]" in spec and not any(KEY[i : i + 8] in spec for i in range(len(KEY) - 7))
    error = capsys.readouterr().err
    assert "refused:" in error and "the GLM credential occurred in changed files" in error
    assert "moved HEAD" not in error


def test_a_glm_draft_that_commits_the_key_is_refused(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # 2a's F-4. Planted fault: the credential scan compares against the model's new HEAD, so the
    # committed key file reads as clean and the moved-HEAD stop leaves the key in file and commit.
    draft_world(world)

    def committing_glm(ctx, prompt, endpoint, writable=False, key=None):
        del prompt, endpoint, writable
        (ctx.root / "plans" / "changes" / "demo" / "spec.md").write_text(f"the key was {key}\n", encoding="utf-8")
        git(ctx.root, "add", "-A")
        git(ctx.root, "commit", "--quiet", "-m", "the model committed the key")
        return "drafted"

    monkeypatch.setattr(stage2, "run_work_model", committing_glm)
    world.script(codex=[{"stdout": "drafted"}, {"stdout": "again"}])
    before = git(world.root, "rev-parse", "HEAD")
    assert world.run("draft") == 2
    assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "1", "only the model's commit stands"
    spec = (world.root / "plans" / "changes" / "demo" / "spec.md").read_text(encoding="utf-8")
    assert "[credential]" in spec and not any(KEY[i : i + 8] in spec for i in range(len(KEY) - 7))
    error = capsys.readouterr().err
    assert "refused:" in error and "the GLM credential occurred in changed files" in error
    assert "moved HEAD" not in error


# ---------------------------------------------------------------------------
# The failed attempt's block in findings.md (spec criteria 1-15, bead coding-harness-cit)
# ---------------------------------------------------------------------------


def quote_blocks(text: str) -> list[list[str]]:
    """Each maximal run of consecutive `>` lines of findings.md, mark and one space stripped."""
    found: list[list[str]] = []
    quoted = False
    for line in text.splitlines():
        if line.startswith(">"):
            if not quoted:
                found.append([])
            quoted = True
            found[-1].append("" if line == ">" else line[2:])
        else:
            quoted = False
    return found


def prompt_entry(prompt: str, attempt: int, route: str) -> list[str]:
    """One attempt's diagnostics entry in a prompt: the lines after its `Attempt` line.

    The entry ends where the next `Attempt <n> (` heading begins, or where the prompt's closing read
    request begins: a diagnostic may hold blank lines of its own, so a blank line is no boundary.
    """
    head = f"Attempt {attempt} ({route}):"
    after = prompt[prompt.index(head) + len(head) + 1 :]
    boundary = rf"\n\nAttempt \d+ \(|\n\n{re.escape(stage2.READ_REQUEST)}"
    return re.split(boundary, after, maxsplit=1)[0].splitlines()


def files_of(block: list[str]) -> list[str]:
    """The file part of a block: its `Files` line and the entries below it."""
    start = next(i for i, line in enumerate(block) if line.startswith("Files the attempt changed"))
    return block[start : block.index("Diagnostics:") - 1]


def line_of(lines: list[str], needle: str) -> int:
    """The index of the first line holding `needle`."""
    return next(i for i, line in enumerate(lines) if needle in line)


def test_a_failed_attempt_quotes_its_diagnostics_below_its_audit_line(world: World) -> None:
    # Criterion 1. Planted fault: the blocks are written once, after the last audit line.
    red = "\n".join(_gate("pytest", ["FAILED tests/test_app.py::test_value - assert 2 == 1"], "red"))
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "repair"},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:03, 3 min\n"}},
        ],
        make=[{"stdout": red, "exit": 1}, {"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    calls = world.calls("claude")
    entry1 = prompt_entry(calls[1]["prompt_file"], 1, "flash")
    entry2 = prompt_entry(calls[2]["prompt_file"], 2, "flash-repair")
    blocks_ = quote_blocks(world.text())
    assert [block[0] for block in blocks_] == [
        "Attempt 1 (flash) failed its post-run checks.",
        "Attempt 2 (flash-repair) failed its post-run checks.",
    ]
    for entry, block in ((entry1, blocks_[0]), (entry2, blocks_[1])):
        assert block[block.index("```text") + 1 : -1] == entry, "the block does not quote the entry whole"
    lines = world.text().splitlines()
    order = [
        line_of(lines, "attempt 1 · route flash"),
        line_of(lines, blocks_[0][0]),
        line_of(lines, "attempt 2 · route flash-repair"),
        line_of(lines, blocks_[1][0]),
        line_of(lines, "attempt 3 · route stage-1"),
    ]
    assert order == sorted(order), "a block does not stand below its own audit line"


def test_a_diagnostic_with_a_blank_line_before_its_stderr_tail_is_compared_whole(world: World) -> None:
    # Criterion 1. Planted fault: the entry is read back out of the prompt only up to its first blank line.
    red = "\n".join(_gate("pytest", ["FAILED tests/test_app.py::test_value - assert 2 == 1"], "red"))
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "repair"},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:03, 3 min\n"}},
        ],
        make=[
            {"stdout": red, "stderr": "warning: unframed\nTraceback: tail", "exit": 1},
            {"stdout": "green"},
            {"stdout": "green"},
        ],
    )
    assert world.run("implement") == 0
    entry = prompt_entry(world.calls("claude")[1]["prompt_file"], 1, "flash")
    assert "" in entry, "the scenario has no blank line inside the diagnostics"
    assert "Traceback: tail" in entry
    block = quote_blocks(world.text())[0]
    assert block[block.index("```text") + 1 : -1] == entry, "the block does not quote the entry whole"


def test_each_failed_attempt_lists_only_the_files_its_model_changed(world: World) -> None:
    # Criterion 2. Planted fault: a snapshot taken at the baseline, before the route block or after verify.
    red = "\n".join(_gate("pytest", ["FAILED src/test_app.py - assertion"], "red"))
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/a.py": "alpha\nbeta\n"}},
            {
                "stdout": "second",
                "plant": {"src/b.py": "bravo\n", "src/app.py": "value = 22\n", "src/blob.bin": "a\x00b"},
                "delete": ["src/a.py"],
            },
            {"stdout": "third", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:03, 3 min\n"}},
        ],
        make=[{"stdout": red, "exit": 1}] * 3,
    )
    assert world.run("implement") == 1
    blocks_ = quote_blocks(world.text())
    assert len(blocks_) == 3
    assert set(files_of(blocks_[0])) == {
        "Files the attempt changed (lines added, removed):",
        "- `src/a.py` +2 -0",
    }
    assert set(files_of(blocks_[1])) == {
        "Files the attempt changed (lines added, removed):",
        "- `src/a.py` +0 -2",
        "- `src/app.py` +1 -1",
        "- `src/b.py` +1 -0",
        "- `src/blob.bin` binary",
    }
    assert set(files_of(blocks_[2])) == {
        "Files the attempt changed (lines added, removed):",
        "- `plans/changes/demo/plan.md` +1 -0",
    }
    joined = "\n".join(part for block in blocks_ for part in files_of(block))
    assert "plans/INDEX.md" not in joined and "findings.md" not in joined


def test_a_failed_attempt_that_changed_nothing_says_so(world: World) -> None:
    # Criterion 3. Planted fault: an empty list renders as a bare heading.
    world.script(
        claude=[
            {"stdout": "nothing"},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    (block,) = quote_blocks(world.text())
    assert "Files the attempt changed: none." in block


def test_an_unmeasured_file_list_says_why_and_changes_nothing_else(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criterion 4. Planted fault: a snapshot failure propagates and stops the run.
    def broken(_root: Path) -> str:
        raise stage2.Refused("git add failed: planted")

    monkeypatch.setattr(stage2, "worktree_tree", broken)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    (block,) = quote_blocks(world.text())
    assert "Files the attempt changed: not measured — git add failed: planted." in block
    assert world.text().count("not measured") == 1


def test_a_failure_after_the_first_snapshot_says_why_and_changes_nothing_else(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criterion 4. Planted fault: only the first snapshot's failure is caught.
    real = stage2.worktree_tree
    calls: list[int] = []

    def second_fails(root: Path) -> str:
        calls.append(1)
        if len(calls) == 2:
            raise stage2.Refused("git write-tree failed: planted")
        return real(root)

    monkeypatch.setattr(stage2, "worktree_tree", second_fails)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    assert len(calls) >= 2
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    (block,) = quote_blocks(world.text())
    assert "Files the attempt changed: not measured — git write-tree failed: planted." in block
    assert world.text().count("not measured") == 1


def test_an_unmeasured_reason_stays_one_line_with_one_full_stop(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    # Criterion 4. Planted fault: the raw git error is put into the sentence as it is.
    def broken(_root: Path) -> str:
        raise stage2.Refused("git add failed: fatal: first line\n  second   line.\n")

    monkeypatch.setattr(stage2, "worktree_tree", broken)
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    (block,) = quote_blocks(world.text())
    lines = [line for line in block if line.startswith("Files the attempt changed")]
    assert lines == ["Files the attempt changed: not measured — git add failed: fatal: first line second line."]


def test_a_malformed_numstat_record_says_not_measured_and_the_run_goes_on(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Criterion 4. Planted fault: a record without two counts raises ValueError and ends the run.
    real = stage2._git_output

    def malformed(root: Path, *args: str, **kwargs: object) -> str:
        if args and args[0] == "diff-tree":
            return "no-tabs-here\0"
        return real(root, *args, **kwargs)

    monkeypatch.setattr(stage2, "_git_output", malformed)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    (block,) = quote_blocks(world.text())
    assert (
        "Files the attempt changed: not measured — "
        "git diff-tree --numstat returned a record without two counts: 'no-tabs-here'."
    ) in block
    assert world.text().count("not measured") == 1


@pytest.mark.parametrize("passing", ["first", "second"], ids=["first-try", "after-a-failure"])
def test_a_passing_attempt_leaves_only_its_audit_line(world: World, passing: str) -> None:
    # Criterion 5. Planted fault: a block written for every attempt.
    fixed = {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}}
    if passing == "first":
        world.script(claude=[fixed], make=[{"stdout": "green"}])
    else:
        world.script(
            claude=[{"stdout": "first", "plant": {"src/app.py": "value = 2\n"}}, fixed],
            make=[{"stdout": "green"}, {"stdout": "green"}],
        )
    assert world.run("implement") == 0
    lines = world.text().splitlines()
    audits = [i for i, line in enumerate(lines) if line.startswith("Stage-2 call,")]
    assert audits and not lines[audits[-1] + 1 :], "something follows the passing attempt's audit line"
    assert world.text().count("failed its post-run checks.") == (0 if passing == "first" else 1)


def test_when_every_attempt_fails_each_keeps_its_block_and_the_exit_names_findings(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 6. Planted fault: the loop raises before the last block.
    world.script(
        claude=[{"stdout": "one"}, {"stdout": "two"}, {"stdout": "three"}],
        make=[{"stdout": "green"}] * 3,
    )
    assert world.run("implement") == 1
    blocks_ = quote_blocks(world.text())
    assert [block[0] for block in blocks_] == [
        "Attempt 1 (flash) failed its post-run checks.",
        "Attempt 2 (flash-repair) failed its post-run checks.",
        "Attempt 3 (stage-1) failed its post-run checks.",
    ]
    assert "plans/changes/demo/findings.md" in capsys.readouterr().err


def test_a_verify_that_cannot_start_still_leaves_the_block_and_the_findings_exit_line(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criteria 1, 6 and 8. Planted fault: a CallFailed from the verify launch escapes `implement` untouched,
    # or is turned into retry diagnostics so that further model attempts start.
    original_launch = stage2.launch

    def no_make(command, root, env, secret=None, **kwargs):
        if command[:2] == ["make", "verify"]:
            raise stage2.CallFailed(f"make could not be started: [Errno 2] no such file {KEY}")
        return original_launch(command, root, env, secret, **kwargs)

    monkeypatch.setattr(stage2, "launch", no_make)
    world.script(claude=[{"stdout": "one"}, {"stdout": "two"}, {"stdout": "three"}], make=[{"stdout": "green"}] * 3)
    assert world.run("implement") == 1
    blocks_ = quote_blocks(world.text())
    assert [block[0] for block in blocks_] == ["Attempt 1 (flash) failed its post-run checks."]
    assert len(world.calls("claude")) == 1
    assert "make could not be started" in "\n".join(blocks_[0])
    assert not any(KEY[i : i + 8] in world.text() for i in range(len(KEY) - 7))
    assert "plans/changes/demo/findings.md" in capsys.readouterr().err


def test_a_restore_after_a_dead_model_keeps_the_earlier_blocks(world: World) -> None:
    # Criterion 7. Planted fault: the blocks kept where the restore reaches.
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "dead", "stderr": "boom", "exit": 1, "plant": {"src/half.py": "x = 1\n"}},
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green"}],
    )
    assert world.run("implement") == 1
    assert not (world.root / "src/half.py").exists()
    (block,) = quote_blocks(world.text())
    assert block[0] == "Attempt 1 (flash) failed its post-run checks."


def test_a_block_holds_no_fragment_of_the_key(world: World) -> None:
    # Criterion 8. Planted fault: the file list or the diagnostics written unscrubbed.
    red = "\n".join(_gate("pytest", [f"E   AssertionError: token {KEY}"], "red"))
    world.script(
        claude=[
            {"stdout": "first", "plant": {f"src/k{KEY[3:15]}.txt": "named after the credential\n"}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": red, "exit": 1}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    text = world.text()
    assert "[credential]" in text
    assert f"src/k{KEY[3:15]}" not in text and "src/k[credential].txt" in text
    assert not any(KEY[i : i + 8] in text for i in range(len(KEY) - 7))


def test_measuring_files_stores_no_key_the_model_wrote(world: World) -> None:
    # Criterion 9. Planted fault: the second snapshot taken before the credential scan.
    world.script(
        claude=[
            {"stdout": "implemented", "plant": {"src/app.py": f"credential = '{KEY}'\n"}},
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "must not run"}],
    )
    assert world.run("implement") == 2
    assert world.calls("make") == []
    done = subprocess.run(
        [GIT, "-C", str(world.root), "cat-file", "--batch-all-objects", "--batch"], capture_output=True
    )
    held = done.stdout.decode("utf-8", "replace")
    assert not any(KEY[i : i + 8] in held for i in range(len(KEY) - 7))


def test_a_fallback_attempt_that_writes_the_key_leaves_no_blob_with_it(world: World) -> None:
    # Criterion 9. Planted fault: the credential scan before the second snapshot skipped on the Sonnet route.
    red = "\n".join(_gate("pytest", ["E   AssertionError"], "red"))
    world.script(
        claude=[
            {"stdout": "one"},
            {"stdout": "two"},
            {"stdout": "fallback", "plant": {"src/app.py": f"credential = '{KEY}'\n"}},
        ],
        make=[{"stdout": red, "exit": 1}, {"stdout": red, "exit": 1}],
    )
    assert world.run("implement") == 2
    assert KEY not in (world.root / "src/app.py").read_text(encoding="utf-8")
    done = subprocess.run(
        [GIT, "-C", str(world.root), "cat-file", "--batch-all-objects", "--batch"], capture_output=True
    )
    held = done.stdout.decode("utf-8", "replace")
    assert not any(KEY[i : i + 8] in held for i in range(len(KEY) - 7))


def test_measuring_files_leaves_index_stash_and_refs_alone(world: World) -> None:
    # Criterion 10. Planted fault: the snapshot written through the real index.
    (world.root / "src/staged.py").write_text("staged = 1\n", encoding="utf-8")
    git(world.root, "add", "src/staged.py")
    (world.root / "src/loose.py").write_text("untracked = 1\n", encoding="utf-8")
    (world.root / "src/app.py").write_text("value = 3\n", encoding="utf-8")
    git(world.root, "stash", "push", "-m", "wip", "--", "src/app.py")
    index = world.root / ".git" / "index"
    index_before = index.read_bytes()
    stash_before = git(world.root, "stash", "list")
    refs_before = git(world.root, "for-each-ref")
    tree = stage2.worktree_tree(world.root)
    assert index.read_bytes() == index_before
    assert git(world.root, "stash", "list") == stash_before
    assert git(world.root, "for-each-ref") == refs_before
    shown = git(world.root, "ls-tree", "-r", "--name-only", tree)
    assert "src/staged.py" in shown and "src/loose.py" in shown
    assert "value = 3" not in git(world.root, "show", f"{tree}:src/app.py")


def test_quoted_reader_lines_count_for_no_reader(world: World) -> None:
    # Criterion 11. Planted fault: lines prefixed after a split at \n only.
    quoted = [
        "Stage-2 call, 2026-10-11: implement · attempt 9 · route flash · endpoint glm-coding-plan",
        "Stage-2 session, 2026-10-11: probe · endpoint opencode-go · model mimo-v2.6-pro",
        "Phase 6 verdict: codex T1, 2026-09-30",
        "Reviewer session: codex T9",
        "Rounds run: 3",
        "## Phase 6 — Codex, 2026-09-30",
        "## Phase 4b — loop rows, released",
        "| X1 | MAJOR | SPEC | a | b | six |",
        "| L1-1 | MAJOR | MAINT | impl | src/app.py:1 | f | deepseek | taken — t | no | — |",
    ]
    red = "\n".join(_gate("pytest", quoted, "red"))
    world.script(
        claude=[
            {
                "stdout": "first",
                "plant": {
                    "src/n\nStage-2 call, 2026-10-11: implement": "named with a newline\n",
                    "src/u  Stage-2 session, 2026-10-11: probe": "named with a line separator\n",
                },
            },
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": red, "exit": 1}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    text = world.text()
    without = "\n".join(line for line in text.splitlines() if not line.startswith(">"))
    for pattern in (
        stage2.SESSION_LINE,
        stage2.ROUNDS_LINE,
        stage2.VERDICT_LINE,
        stage2.VERDICT_START,
        stage2.ROUND_HEADING,
    ):
        assert pattern.findall(text) == pattern.findall(without) == []
    assert stage2_runs.measure(text) == stage2_runs.measure(without)
    assert stage2_runs.measure(text).calls == [("implement", True), ("implement", True)]
    assert "Stage-2 session, 2026-10-11: probe` +1 -0" in text, "the name's separator did not split the entry"


def test_a_quoted_release_heading_or_no_loop_line_moves_no_release(world: World) -> None:
    # Criterion 12. Planted fault: today's substring checks.
    quoted = stage2.quote_block(f"{stage2.RELEASE_HEADING} 2026-10-11\n\n{stage2.NO_LOOP_LINE}", None)
    assert all(line.startswith(">") for line in quoted.splitlines())
    world.write_findings(VERDICT, quoted)
    assert world.run("release-loop") == 0
    assert world.text().count(stage2.NO_LOOP_LINE) == 2, "the quote stood in for the runner's own line"
    released = f"{stage2.RELEASE_HEADING} 2026-10-11\n\n" + stage2.render_table(
        stage2.RELEASED_COLUMNS,
        [["L1-1", "MAJOR", "MAINT", "impl", "src/app.py:1", "f", "deepseek", "taken — t", "no", "—"]],
    )
    world.write_findings(VERDICT, released, quoted)
    assert [row[0] for row in stage2.released_rows(world.text())] == ["L1-1"]


# ---------------------------------------------------------------------------
# The format step before `make verify` (spec stage2-format, criteria 1-12, bead coding-harness-52r)
# ---------------------------------------------------------------------------


def venv_ruff(world: World, executable: bool = True) -> None:
    """The test ruff: `STAND_IN` reached through `<worktree>/.venv/bin/ruff`, never on `PATH`.

    The link resolves beside the scenario in `world.bin`, so the stand-in reads its steps and
    records under the name the link gives it (`ruff`); `.venv/` is excluded, so no reader of
    tracked files sees the link. With `executable=False` the path holds a plain file of mode 0644:
    the system refuses to run it.
    """
    stand_in = world.bin / "ruff.stand-in"
    stand_in.write_text(
        STAND_IN.replace("@PYTHON@", sys.executable).replace("@PI@", stage2.PI_VERSION), encoding="utf-8"
    )
    stand_in.chmod(0o755)
    ruff = world.root / ".venv" / "bin" / "ruff"
    ruff.parent.mkdir(parents=True, exist_ok=True)
    if executable:
        ruff.symlink_to(stand_in)
    else:
        ruff.write_text("# a ruff stand-in that cannot be run\n", encoding="utf-8")
        ruff.chmod(0o644)
    (world.root / ".git" / "info" / "exclude").write_text(".venv/\n", encoding="utf-8")


def formatted_attempt(**more: object) -> dict:
    """One Flash attempt that plants an unformatted `scripts/a.py` and measures the plan."""
    return {
        "stdout": "implemented",
        "plant": {"scripts/a.py": "a=1\n"},
        "append": {"plans/changes/demo/plan.md": "2026-10-12 10:00–10:02, 2 min\n"},
        **more,
    }


def test_the_format_step_runs_check_then_format_on_the_targets_before_verify(world: World) -> None:
    # Criteria 1 and 2. Planted fault: the commands in another order, another argument list, or ruff
    # given `scripts/ tests/` whole instead of the targets. The modified, already tracked
    # `scripts/old.py` must stand among them: dropping modified tracked files from the targets would
    # pass while only newly created files carry the step.
    venv_ruff(world)
    (world.root / "scripts/old.py").write_text("x = 1\n", encoding="utf-8")
    (world.root / "scripts/gone.py").write_text("y = 2\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "an unformatted neighbour, a file the attempt deletes")
    world.script(
        claude=[
            formatted_attempt(
                plant={
                    "scripts/a.py": "a=1\n",
                    "scripts/old.py": "x=1\n",
                    "tests/test_b.py": "def test_b():\n    assert 1\n",
                    "src/c.py": "c = 3\n",
                    "scripts/notes.md": "# notes\n",
                },
                delete=["scripts/gone.py"],
            )
        ],
        ruff=[{"plant": {"scripts/a.py": "a = 1\n"}}, {}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert [call["name"] for call in world.calls()] == ["claude", "ruff", "ruff", "make"]
    assert [call["argv"] for call in world.calls("ruff")] == [
        [
            "check",
            "--fix",
            "--no-unsafe-fixes",
            "--force-exclude",
            "--no-cache",
            "scripts/a.py",
            "scripts/old.py",
            "tests/test_b.py",
        ],
        ["format", "--force-exclude", "--no-cache", "scripts/a.py", "scripts/old.py", "tests/test_b.py"],
    ]
    for call in world.calls("ruff"):
        assert call["cwd"] == str(world.root)


def test_the_format_step_leaves_out_links_and_hard_linked_files(world: World) -> None:
    # Criterion 2. Planted fault: the targets filtered by suffix and directory alone.
    venv_ruff(world)
    (world.root / "scripts/real.py").write_text("real = 1\n", encoding="utf-8")
    outside = world.root.parent / "outside.py"
    outside.write_text("out = 1\n", encoding="utf-8")
    (world.root / "scripts/link.py").symlink_to(outside)
    (world.root / "tests").mkdir()
    (world.root / "tests/hard_twin.py").write_text("twin = 1\n", encoding="utf-8")
    os.link(world.root / "tests/hard_twin.py", world.root / "tests/hard.py")
    world.script(ruff=[{}, {}], make=[{"stdout": "green\n"}])
    formatted: list[str] = []
    stage2.verify_attempt(world.root, world.plan, "", formatted=formatted)
    assert [call["argv"] for call in world.calls("ruff")] == [
        ["check", "--fix", "--no-unsafe-fixes", "--force-exclude", "--no-cache", "scripts/real.py"],
        ["format", "--force-exclude", "--no-cache", "scripts/real.py"],
    ]
    assert formatted == ["ruff changed no file."]
    assert outside.read_text(encoding="utf-8") == "out = 1\n"


def test_without_a_target_file_no_ruff_starts(world: World) -> None:
    # Criteria 3 and 8. Planted fault: ruff started with an empty path list, or the commit heading
    # written with no line below it.
    venv_ruff(world)
    successful_implementation(world)
    assert world.run("implement") == 0
    assert world.calls("ruff") == []
    assert git(world.root, "log", "-1", "--format=%B") == "feat(demo): implement accepted plan"


def test_the_format_step_runs_the_worktrees_ruff_not_the_one_on_path(world: World) -> None:
    # Criterion 4. Planted fault: ruff started by its bare name, so the program on `PATH` answers.
    venv_ruff(world)
    decoy = world.bin / "ruff"
    decoy.write_text('#!/bin/sh\ntouch "$(dirname "$0")/decoy-called"\nexit 97\n', encoding="utf-8")
    decoy.chmod(0o755)
    world.script(claude=[formatted_attempt()], ruff=[{}, {}], make=[{"stdout": "green\n"}])
    assert world.run("implement") == 0
    assert len(world.calls("ruff")) == 2
    assert not (world.bin / "decoy-called").exists()


def test_ruff_gets_the_verify_environment_without_credentials(world: World) -> None:
    # Criterion 5. Planted fault: the ruff launch given `glm_env` or the caller's environment.
    venv_ruff(world)
    world.script(claude=[formatted_attempt()], ruff=[{}, {}], make=[{"stdout": "green\n"}])
    assert world.run("implement") == 0
    make_env = world.calls("make")[0]["env"]
    for call in world.calls("ruff"):
        assert call["env"] == make_env
        assert KEY not in call["env"].values()
        for name in ("ANTHROPIC_AUTH_TOKEN", "GH_TOKEN", "OPENAI_API_KEY", "X_SECRET"):
            assert name not in call["env"], name


def test_the_format_steps_writes_stay_out_of_the_models_file_list(world: World) -> None:
    # Criterion 6. Planted fault: the second snapshot taken after `verify_attempt`. The stand-in
    # spends one ruff step per call - check and format each take one - so the `{}` entries put each
    # plant on a format call, the only place its bytes survive to a snapshot: the faulted snapshot
    # counts ruff's four lines in block 1 and names `scripts/a.py` in block 2.
    venv_ruff(world)
    world.script(
        claude=[
            {"stdout": "first", "plant": {"scripts/a.py": "a=1\n"}},
            {"stdout": "second"},
            {"stdout": "third", "append": {"plans/changes/demo/plan.md": "2026-10-12 10:00–10:02, 2 min\n"}},
        ],
        ruff=[
            {},
            {"plant": {"scripts/a.py": "a = 1  # the fix\n# and three\n# more\n# lines\n"}},
            {},
            {"plant": {"scripts/a.py": "a = 1\n"}},
        ],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("implement") == 0
    blocks_ = quote_blocks(world.text())
    assert files_of(blocks_[0]) == [
        "Files the attempt changed (lines added, removed):",
        "- `scripts/a.py` +1 -0",
    ]
    assert "Files the attempt changed: none." in blocks_[1]


def test_a_failed_attempt_carries_its_format_line_first_in_its_diagnostics(world: World) -> None:
    # Criterion 7. Planted fault: the format line appended after the other entries.
    venv_ruff(world)
    red = "\n".join(_gate("pytest", ["FAILED tests/test_b.py::test_b - assert 1 == 2"], "red"))
    world.script(
        claude=[
            {
                "stdout": "first",
                "plant": {"scripts/a.py": "a=1\n", "tests/test_b.py": "def test_b():\n    assert 1\n"},
            },
            {"stdout": "second", "append": {"plans/changes/demo/plan.md": "2026-10-12 10:00–10:02, 2 min\n"}},
        ],
        ruff=[{"plant": {"scripts/a.py": "a = 1\n"}}, {}],
        make=[{"stdout": red, "exit": 1}, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    first = "- Runner format before `make verify`: ruff changed `scripts/a.py`."
    entry = quote_blocks(world.text())[0]
    assert entry[entry.index("```text") + 1] == first
    assert prompt_entry(world.calls("claude")[1]["prompt_file"], 1, "flash")[0] == first


def test_a_passing_run_lists_each_format_line_in_its_commit_message(world: World) -> None:
    # Criterion 8. Planted fault: an earlier attempt's format line dropped before the checkpoint
    # (only the passing attempt's line kept), or a line for an attempt that ran no format step.
    venv_ruff(world)
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n", "scripts/b.py": "b=1\n"}},
            formatted_attempt(),
        ],
        ruff=[{}, {"plant": {"scripts/b.py": "b = 1\n"}}, {}, {"plant": {"scripts/a.py": "a = 1\n"}}],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("implement") == 0
    assert git(world.root, "log", "-1", "--format=%B") == (
        "feat(demo): implement accepted plan\n\n"
        "Runner format before `make verify` (ruff check --fix with safe fixes only, then ruff format):\n"
        "- Attempt 1 (flash): ruff changed `scripts/b.py`.\n"
        "- Attempt 2 (flash-repair): ruff changed `scripts/a.py`."
    )


def test_a_passing_attempt_that_was_formatted_leaves_only_its_audit_line(world: World) -> None:
    # Criterion 9. Planted fault: the format line appended to findings.md for every attempt.
    venv_ruff(world)
    world.script(
        claude=[formatted_attempt()],
        ruff=[{"plant": {"scripts/a.py": "a = 1\n"}}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    lines = world.text().splitlines()
    audits = [i for i, line in enumerate(lines) if line.startswith("Stage-2 call,")]
    assert audits and not lines[audits[-1] + 1 :], "something follows the passing attempt's audit line"


@pytest.mark.parametrize("case", ["no-ruff", "not-executable", "findings-left", "format-error"])
def test_a_ruff_failure_leaves_the_verdict_to_make_verify(world: World, case: str) -> None:
    # Criterion 10. Planted fault: a non-zero ruff exit turned into a problem of the attempt.
    if case == "not-executable":
        venv_ruff(world, executable=False)
    elif case != "no-ruff":  # no-ruff: no helper, no `.venv/bin/ruff` in the worktree
        venv_ruff(world)
    check: dict = {}
    fmt: dict = {}
    if case == "findings-left":
        check = {"stdout": "scripts/a.py:1:1: F401 `a` imported but unused", "exit": 1}
    elif case == "format-error":
        fmt = {"stdout": "error: cannot reformat scripts/a.py", "exit": 2}
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(claude=[formatted_attempt()], ruff=[check, fmt], make=[{"stdout": "green\n"}])
    assert world.run("implement") == 0
    assert len(world.calls("claude")) == 1 and len(world.calls("make")) == 1
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    message = git(world.root, "log", "-1", "--format=%B")
    if case == "findings-left":
        assert "ruff check left findings without a safe fix" in message
    if case == "format-error":
        assert "ruff format exited 2" in message


@pytest.mark.parametrize("case", ["no-ruff", "not-executable"])
def test_a_ruff_that_cannot_start_is_reported_as_not_run(world: World, case: str) -> None:
    # Criterion 11. Planted fault: the ruff launch's `CallFailed` propagates like make's.
    if case == "not-executable":
        venv_ruff(world, executable=False)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(claude=[formatted_attempt()], ruff=[{}, {}], make=[{"stdout": "green\n"}])
    assert world.run("implement") == 0
    assert world.calls("ruff") == []
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    message = git(world.root, "log", "-1", "--format=%B")
    line = next(line for line in message.splitlines() if line.startswith("- Attempt 1 (flash):"))
    assert line.startswith("- Attempt 1 (flash): not run —")
    assert "no ruff at" in line or "could not be started" in line


def test_a_check_exit_one_covers_findings_and_a_file_that_does_not_parse(world: World) -> None:
    # Repair round 3 (L3-1). Planted fault: the note calls every exit 1 of `ruff check` findings
    # without a safe fix alone, although a target that does not parse exits 1 as well.
    venv_ruff(world)
    world.script(
        claude=[formatted_attempt()],
        ruff=[{"stdout": "error: Failed to parse scripts/a.py:1:5: expected an expression", "exit": 1}, {}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    message = git(world.root, "log", "-1", "--format=%B")
    line = next(entry for entry in message.splitlines() if entry.startswith("- Attempt 1 (flash):"))
    assert "ruff check left findings without a safe fix or a file that does not parse" in line


def test_an_unreadable_target_is_named_by_its_repository_path(world: World) -> None:
    # Repair round 3 (L3-3). Planted fault: the raw `OSError` text as the `not run` reason, carrying
    # the worktree's absolute path into the block and the checkpoint commit message.
    venv_ruff(world)
    unreadable = world.root / "scripts" / "a.py"
    unreadable.write_text("a=1\n", encoding="utf-8")
    unreadable.chmod(0o000)
    world.script(ruff=[{}, {}], make=[{"stdout": "green\n"}])
    formatted: list[str] = []
    stage2.verify_attempt(world.root, world.plan, "", formatted=formatted)
    assert world.calls("ruff") == []
    assert formatted == ["not run — cannot read `scripts/a.py`."]
    assert str(world.root) not in formatted[0]


def test_a_target_named_with_a_line_break_keeps_the_format_line_one_line(world: World) -> None:
    # Repair round 4 (F-1). Planted fault: the target path interpolated verbatim, so a newline in
    # its name split the format line in two - in the block's entry and the checkpoint commit message.
    venv_ruff(world)
    name = "scripts/a\nb.py"
    world.script(
        claude=[formatted_attempt(plant={name: "a=1\n"})],
        ruff=[{}, {"plant": {name: "a = 1\n"}}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert world.calls("ruff")[1]["argv"] == ["format", "--force-exclude", "--no-cache", name]
    message = git(world.root, "log", "-1", "--format=%B")
    assert "- Attempt 1 (flash): ruff changed `scripts/a\\nb.py`." in message.splitlines()


def test_a_commit_message_holds_no_fragment_of_the_key(world: World) -> None:
    # Criterion 12. Planted fault: the format line built without `scrub`.
    venv_ruff(world)
    name = f"scripts/k{KEY[3:15]}.py"
    world.script(
        claude=[formatted_attempt(plant={name: "a=1\n"})],
        ruff=[{"plant": {name: "a = 1\n"}}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    message = git(world.root, "log", "-1", "--format=%B")
    assert "[credential]" in message
    assert not any(KEY[i : i + 8] in message for i in range(len(KEY) - 7))


def test_a_long_diagnostic_line_is_cut_with_a_marker(world: World) -> None:
    # Criterion 13. Planted fault: no cut, or a cut without its marker.
    red = "\n".join(_gate("pytest", ["x" * 5000], "red"))
    world.script(
        claude=[
            {"stdout": "first", "plant": {"src/app.py": "value = 2\n"}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": red, "exit": 1}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    text = world.text()
    assert "x" * 500 in text and "x" * 501 not in text
    assert "… 4500 characters left out …" in text


def test_a_long_file_list_is_cut_with_a_count(world: World) -> None:
    # Criterion 14. Planted fault: no cap on the list.
    world.script(
        claude=[
            {"stdout": "first", "plant": {f"src/bulk-{n:02d}.py": f"value = {n}\n" for n in range(60)}},
            {"stdout": "fixed", "append": {"plans/changes/demo/plan.md": "2026-10-08 10:00–10:02, 2 min\n"}},
        ],
        make=[{"stdout": "green"}, {"stdout": "green"}],
    )
    assert world.run("implement") == 0
    (block,) = quote_blocks(world.text())
    assert len([line for line in block if line.startswith("- `src/bulk-")]) == 40
    assert "- … and 20 more files" in block
    assert "src/bulk-40.py" not in "\n".join(block)


def test_a_failed_stage2_off_attempt_leaves_its_block_without_reading_the_key(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 15. Planted fault: the block reads the key to scrub it.
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on Stage 1: {name}"))
    world.script(claude=[{"stdout": "nothing"}], make=[{"stdout": "green"}])
    assert world.run("implement", "demo", "--stage2-off", "Z.ai unavailable") == 1
    (block,) = quote_blocks(world.text())
    assert block[0] == "Attempt 1 (stage-1) failed its post-run checks."
    assert "Files the attempt changed: none." in block
    assert "plans/changes/demo/findings.md" in capsys.readouterr().err


@pytest.mark.parametrize("fault", ["command", "non-descendant", "dirty", "status-fails"])
def test_checkpoint_failures_are_call_failures(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, fault: str) -> None:
    def fake_git(root: Path, *args: str, allow: tuple[int, ...] = (0,)) -> str:
        del root, allow
        if fault == "command" and args[0] == "add":
            raise stage2.Refused("git add failed")
        if args[0] == "rev-list":
            return "2\n" if fault == "non-descendant" else "1\n"
        if args[0] == "status":
            if fault == "status-fails":
                raise stage2.Refused("git status failed")
            return " M src/app.py\n" if fault == "dirty" else ""
        return ""

    ancestor = 1 if fault == "non-descendant" else 0
    monkeypatch.setattr(stage2, "_git_output", fake_git)
    monkeypatch.setattr(
        stage2.subprocess,
        "run",
        lambda *args, **_kwargs: subprocess.CompletedProcess(args[0], ancestor, b"", b""),
    )
    with pytest.raises(stage2.CallFailed):
        stage2.checkpoint(tmp_path, "demo", "base")


@pytest.mark.parametrize("verb", ["explore", "implement"])
def test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten(
    world: World, verb: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert world.run(verb, None, "--stage2-off", "demo") == 2
    error = capsys.readouterr().err
    assert "`demo` was taken as the --stage2-off reason" in error and "--stage2-off=REASON" in error
    assert world.calls() == []


@pytest.mark.parametrize("verb", ["draft", *REVIEW_VERBS, "release-loop"])
def test_stage2_off_is_only_for_work_verbs(world: World, verb: str) -> None:
    # Criterion 26. Planted fault: `draft` joins the verbs that accept `--stage2-off`.
    assert world.run(verb, "demo", "--stage2-off") == 2
    assert world.calls() == []


def test_filling_the_marks_keeps_the_updated_stamp_current(world: World) -> None:
    """Repair round 2 (F-7 note): `fill_marks` stamps the file by itself, not only through the append before it."""
    released = f"{stage2.RELEASE_HEADING} 2026-09-29\n\n" + stage2.render_table(
        stage2.RELEASED_COLUMNS,
        [["L1-1", "MAJOR", "MAINT", "impl", "src/app.py:1", "f", "deepseek-v4.1-flash", "taken — t", "no", "—"]],
    )
    world.findings.write_text(old_header() + "\n" + released + "\n", encoding="utf-8")
    assert updated_of(world.findings) == dt.date(2026, 9, 29)
    stage2.fill_marks(world.findings, ["L1-1"], {"L1-1": "agree"})
    assert updated_of(world.findings) == dt.date.today(), "filling the marks left the header stale"
    assert "| taken — t | no | agree |" in world.text()


def test_a_findings_file_without_a_header_is_left_without_one(world: World) -> None:
    """The stamp edits a header and invents none: the loop record has no header and gets none."""
    world.script(pi=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    assert "updated:" not in world.record().read_text(encoding="utf-8")


def test_a_spec_without_a_bead_refuses(world: World) -> None:
    (world.root / "plans" / "changes" / "demo" / "spec.md").write_text("---\ntitle: Spec\n---\n", encoding="utf-8")
    assert world.run("spec-review") == 2
    assert world.calls() == [] and not world.findings.exists()


def test_every_prompt_asks_to_read_nothing_outside(world: World) -> None:
    full_flow(world)
    codex_prompts = [call["argv"][-1] for call in world.calls("codex")]
    assert len(codex_prompts) == 2
    loop_prompts = [call["prompt_file"] for call in world.calls("pi")]
    spec_prompt = world.calls("claude")[0]["prompt_file"]
    for prompt in [*codex_prompts, *loop_prompts, spec_prompt]:
        assert prompt.rstrip().endswith(stage2.READ_REQUEST)


# ---------------------------------------------------------------------------
# The reviewer in phases 2a and 6 (criteria 8, 9, 19)
# ---------------------------------------------------------------------------


def rung_of(call: dict) -> str:
    """The ladder id a Pi call asked for, without the provider prefix."""
    return call["argv"][call["argv"].index("--model") + 1].removeprefix("opencode-go/")


PI_FLAGS = [
    "--print",
    "--no-session",
    "--no-approve",
    "--no-extensions",
    "--no-mcp",
    "--no-skills",
    "--no-context-files",
    "--no-prompt-templates",
    "--no-themes",
    "--offline",
]


def test_the_review_loop_launches_pi_isolated(world: World) -> None:
    """Criterion 8: one launch path for the loop's rounds - the rung under the provider, the measured flag set, a fresh home."""
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    assert world.calls("codex") == [] and world.calls("claude") == []
    call = world.calls("pi")[0]
    argv = call["argv"]
    options = [a for a in argv if a.startswith("--") and a not in {"--tools", "--thinking", "--model"}]
    assert options == [*PI_FLAGS, "--append-system-prompt"], "a flag is missing, added or reordered"
    assert argv[argv.index("--tools") + 1] == "read,grep,find,ls"
    assert argv[argv.index("--thinking") + 1] == "max"
    assert argv[argv.index("--model") + 1] == "opencode-go/deepseek-v4.1-flash"
    assert argv[-1] == "Review the change demo as the appended instructions say."
    for refused in ("--mode", "--api-key", "--approve", "--no-tools", "-p", "--resume", "--restricted"):
        assert refused not in argv
    assert Path(argv[argv.index("--append-system-prompt") + 1]).name == "review-prompt.md"
    assert call["prompt_file"].rstrip().endswith(stage2.READ_REQUEST)
    # the agent directory holds one file, and a second call gets a directory of its own
    assert call["agent_listing"] == ["settings.json"]
    assert json.loads(call["agent_settings"]) == {"retry": {"enabled": False}}
    env = call["env"]
    assert env["HOME"] != os.environ["HOME"] and not Path(env["HOME"]).is_relative_to(world.root)
    assert not Path(env["PI_CODING_AGENT_DIR"]).is_relative_to(world.root)
    assert call["home_listing"] == []
    assert not [n for n in env if n.startswith(("ANTHROPIC_", "CLAUDE_"))]
    assert call["cwd"] == str(world.root.resolve()) and call["stdin"] == ""
    assert argv[0] not in {"claude", "codex"} and "claude" not in call["name"]
    decide_record(world)
    assert world.run("review-loop") == 0
    second = world.calls("pi")[1]["env"]
    assert second["PI_CODING_AGENT_DIR"] != env["PI_CODING_AGENT_DIR"] and second["HOME"] != env["HOME"]


@pytest.mark.parametrize("verb", ["review-loop", "probe"])
@pytest.mark.parametrize(
    "fault",
    [
        {"pi_version": "1.1.1"},
        {"pi_version": "1.1.0 (dev)"},
        {"pi_version": ""},
        {"pi_version": "1.1.0", "pi_version_exit": 1},
        {"pi_version": "1.1.0", "pi_version_sleep": 30},
        "absent",
    ],
    ids=["newer", "suffix", "silent", "non-zero", "too-slow", "absent"],
)
def test_a_pi_off_the_pin_is_refused(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], verb: str, fault: dict | str
) -> None:
    """Criterion 27: a Pi that is not exactly the pinned version starts no leak check, no call line and no call."""
    assert stage2.PI_VERSION == "1.1.0"
    monkeypatch.setattr(stage2, "PI_VERSION_SECONDS", 0.5)
    steps = {"pi": [{"stdout": rows(1)}] * 3}
    if fault == "absent":
        (world.bin / "pi").unlink()
        world.script(**steps)
    else:
        world.script(**steps, **fault)
    assert world.run(verb) == 2, "a Pi off the pin must refuse with exit 2"
    assert world.calls() == [], "a call started"
    assert not world.record().exists()
    assert not world.findings.exists() or "Stage-2 call" not in world.text(), "a call line was written"
    assert "leak check" not in capsys.readouterr().out.lower(), "the leak check ran before the pin"


def test_the_pinned_pi_runs_the_probe_on_every_rung(world: World) -> None:
    """Criterion 27, the other side: the exact pin starts the run and the probe reaches every rung."""
    world.script(pi=[{"stdout": "rung one"}, {"stdout": "rung two"}, {"stdout": "rung three"}])
    assert world.run("probe") == 0
    assert len(world.calls("pi")) == 3


def test_an_answer_that_is_not_rows_is_kept(world: World) -> None:
    world.script(claude=[{"stdout": "An opening remark.\n" + rows(1)}, {"stdout": "No finding at all."}])
    assert world.run("spec-review") == 0
    assert "An opening remark." in world.text() and stage2.NOT_ROWS_NOTE in world.text()
    assert world.run("spec-review") == 0
    assert "No finding at all." in world.text() and "Opus reported no finding." in world.text()


def test_the_spec_review_answer_lands_as_opus_rows_without_a_session(world: World) -> None:
    # Criterion 28. Planted fault: the session line of the Codex review is appended after the rows.
    world.script(claude=[{"stdout": rows(3)}])
    assert world.run("spec-review") == 0
    text = world.text()
    assert len(re.findall(r"^\| X\d \|.*\| Opus \| open \| — \|$", text, re.M)) == 3
    assert "## Phase 2a — Opus 5.5, " in text
    assert "Reviewer session" not in text


@pytest.mark.parametrize(
    "step",
    [
        {"stdout": ""},
        {"stdout": rows(1), "exit": 1},
    ],
    ids=["empty-answer", "non-zero-exit"],
)
def test_a_failed_spec_review_call_writes_no_rows(world: World, step: dict) -> None:
    world.script(claude=[step])
    assert world.run("spec-review") == 1
    text = world.text()
    assert "Reviewer session" not in text and "## Phase 2a" not in text and "X1" not in text


def test_the_spec_review_starts_opus_with_read_only_tools(world: World) -> None:
    # Criterion 27. Planted fault: the spec review still calls `codex`, or the Claude call writes.
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.calls("codex") == []
    call = world.calls("claude")[0]
    argv, prompt = call["argv"], call["prompt_file"]
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5"
    assert argv[argv.index("--effort") + 1] == "xhigh"
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"Read", "Grep", "Glob"}
    assert "--restricted" in argv and "--no-session-persistence" in argv
    assert "ANTHROPIC_BASE_URL" not in call["env"] and "OPENCODE_API_KEY" not in call["env"]
    assert (REPO_ROOT / "prompts" / "02a-spec-review.md").read_text(encoding="utf-8").rstrip() in prompt
    assert "plans/changes/demo/" in prompt


def test_a_findings_file_the_spec_review_creates_names_claude_code(world: World) -> None:
    # Criterion 29. Planted fault: the producer map stays at `codex` or `pi`.
    assert not world.findings.exists()
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    header = plans_registry._frontmatter(world.findings)
    assert header is not None and header["produced_by"]["name"] == "claude-code"


def seed_2a_session(world: World, session: str = "T1") -> None:
    """A findings.md whose last phase-2a block is a Codex one with its session line (criteria 30 and 31)."""
    world.write_findings(f"## Phase 2a — Codex, 2026-09-30\n\n{rows(1)}\n\nReviewer session: codex {session}")


def test_codex_is_pinned_on_first_and_resumed_calls(world: World) -> None:
    # Criterion 2. Planted fault: `review` passes `workspace-write`, a bypass flag or another pin.
    seed_2a_session(world)
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 0
    for call in world.calls("codex"):
        argv = call["argv"]
        assert argv[:3] == ["exec", "resume", "T1"]
        assert argv[argv.index("-m") + 1] == "gpt-6.1-sol"
        assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in argv
        assert 'sandbox_mode="read-only"' in argv
        assert "--ephemeral" not in argv and "-s" not in argv
        for flag in ("--add-dir", "--approve-for-me", "--dangerously-bypass-approvals-and-sandbox", "--sandbox"):
            assert flag not in argv


def test_codex_runs_with_hooks_and_memories_off(world: World) -> None:
    seed_2a_session(world)
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 0
    for call in world.calls("codex"):
        disabled = [call["argv"][i + 1] for i, word in enumerate(call["argv"]) if word == "--disable"]
        assert sorted(disabled) == ["hooks", "memories"]


def test_the_codex_prompt_carries_its_phase_prompt_in_full(world: World) -> None:
    seed_2a_session(world)
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 0
    for call in world.calls("codex"):
        prompt = call["argv"][-1]
        assert (REPO_ROOT / "prompts" / "06-review.md").read_text(encoding="utf-8").rstrip() in prompt
        assert "plans/changes/demo/" in prompt


def test_review_resumes_the_recorded_session(world: World) -> None:
    # Criterion 31. Planted fault: the last phase-2a block is not read, so a recorded session is not resumed.
    seed_2a_session(world)
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 0
    assert world.calls("codex")[0]["argv"][:3] == ["exec", "resume", "T1"]
    text = world.text()
    assert re.search(r"^Phase 6 verdict: codex T1, \d{4}-\d{2}-\d{2}$", text, re.M)
    assert "fresh session" not in text


def test_a_fresh_phase_6_session_says_so(world: World) -> None:
    # Criterion 30. Planted fault: the last `Reviewer session: codex` line anywhere is resumed.
    world.script(codex=[codex_ok("T5", rows(1))])
    assert world.run("review") == 0
    assert world.calls("codex")[0]["argv"][:2] == ["exec", "--json"]
    assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in world.calls("codex")[0]["argv"]
    assert "a fresh session reviewed: no phase-2a session was recorded" in world.text()

    world.findings.unlink()
    (world.bin / "calls.jsonl").unlink()
    world.write_findings(
        f"## Phase 2a — Codex, 2026-09-30\n\n{rows(1)}\n\nReviewer session: codex T1",
        f"## Phase 2a — Opus 5.5, 2026-10-13\n\n{rows(1)}",
    )
    world.script(codex=[codex_ok("T5", rows(1))])
    assert world.run("review") == 0
    assert world.calls("codex")[0]["argv"][:2] == ["exec", "--json"], "an Opus block after the line is no resume"
    assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in world.calls("codex")[0]["argv"]
    assert "a fresh session reviewed: no phase-2a session was recorded" in world.text()

    world.findings.unlink()
    (world.bin / "calls.jsonl").unlink()
    world.write_findings(f"## Phase 2a — Codex, 2026-09-30\n\n{rows(1)}\n\nReviewer session: codex T1")
    world.script(codex=[codex_ok("T2", rows(1))])
    assert world.run("review") == 0
    assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in world.calls("codex")[0]["argv"]
    assert "a fresh session reviewed: the resume of T1 started a new thread" in world.text()


def test_phase6_after_codex_repair_starts_a_fresh_read_only_session(world: World) -> None:
    # Criterion 18. Planted fault: a re-check resumes the repair, an earlier verdict or the historical 2a thread,
    # or its verdict call gets write access.
    world.write_findings(
        f"## Phase 2a — Codex, 2026-09-30\n\n{rows(1)}\n\nReviewer session: codex T1",
        phase6_block([phase6_cells("F-1", "fixed — tests/test_seed.py::test_seed", "phase finding")])
        + "\n\nPhase 6 verdict: codex T7, 2026-10-12",
    )
    world.script(codex=[codex_ok("T9", rows(1))])
    assert world.run("review") == 0
    (call,) = world.calls("codex")
    argv = call["argv"]
    assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in argv
    assert "resume" not in argv and argv[:2] == ["exec", "--json"]
    assert "T1" not in argv and "T7" not in argv and "TR1" not in argv
    assert 'sandbox_mode="read-only"' in argv and not any("workspace-write" in part for part in argv)
    assert "a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check" in world.text()
    assert re.search(r"^Phase 6 verdict: codex T9, \d{4}-\d{2}-\d{2}$", world.text(), re.M)


def test_a_phase6_rerun_without_repair_records_the_actual_recheck_reason(world: World) -> None:
    """L2-4. Planted fault: a second verdict claims a repair ran, although only an earlier verdict exists."""
    seed_2a_session(world)
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T9", rows(1))])
    assert world.run("review") == 0
    assert world.run("review") == 0
    first, second = world.calls("codex")
    for call in (first, second):  # both review calls keep the review entry (bead coding-harness-yzk)
        assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in call["argv"]
    assert first["argv"][:3] == ["exec", "resume", "T1"]
    assert "resume" not in second["argv"] and 'sandbox_mode="read-only"' in second["argv"]
    text = world.text()
    assert (
        "Reviewer session: codex T9 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check"
        in text
    )
    assert "after a repair" not in text and "fixed —" not in text
    assert world.calls("claude") == [] and world.calls("make") == []


def test_the_first_phase6_review_still_resumes_the_recorded_2a_session(world: World) -> None:
    # Criterion 18, the other side (ADR 0016, decision 6). Planted fault: every review starts fresh.
    seed_2a_session(world)
    world.script(codex=[codex_ok("T1", rows(1))])
    assert world.run("review") == 0
    assert world.calls("codex")[0]["argv"][:3] == ["exec", "resume", "T1"]


def test_the_loop_marks_after_a_recheck_resume_the_fresh_verdict_thread(world: World) -> None:
    # Criterion 18. Planted fault: the mark call resumes a thread other than the re-check's own.
    world.write_findings(phase6_block([phase6_cells("F-1", "fixed — tests/test_seed.py::test_seed", "phase finding")]))
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(codex=[codex_ok("T9", rows(1)), codex_ok("T9", "L1-1: agree")])
    assert world.run("review") == 0
    verdict_call, mark_call = world.calls("codex")
    for call in (verdict_call, mark_call):  # both review calls keep the review entry (bead coding-harness-yzk)
        assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["review"]}"' in call["argv"]
    assert "resume" not in verdict_call["argv"] and mark_call["argv"][:3] == ["exec", "resume", "T9"]
    assert 'sandbox_mode="read-only"' in mark_call["argv"]


def test_no_loop_row_reaches_the_verdict_call(world: World) -> None:
    world.write_record([("L1-1", "taken — test_a", "no")], finding="LOOPMARK-7")
    world.script(marker="LOOPMARK-7", codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 0
    verdict_call, mark_call = world.calls("codex")
    assert "LOOPMARK-7" not in verdict_call["argv"][-1] and verdict_call["marker_paths"] == []
    assert "LOOPMARK-7" in mark_call["argv"][-1]


def test_codex_marks_each_loop_row_after_its_verdict(world: World) -> None:
    world.write_record(
        [("L1-1", "taken — test_a", "yes"), ("L1-2", "rejected — out of scope", ""), ("L1-3", "taken — crit 4", "no")]
    )
    world.script(codex=[codex_ok("T1", rows(2)), codex_ok("T1", "L1-1: agree\nL1-2: disagree — it is covered")])
    assert world.run("review") == 0
    text = world.text()
    before = verdict_block(world.calls("codex")[1]["findings"])
    assert verdict_block(text) == before, "the mark call changed the verdict"
    released = {
        cells[0]: cells
        for cells in (stage2.split_row(line) for line in text.splitlines())
        if cells and len(cells) == 10 and cells[0].startswith("L1-")
    }
    assert released["L1-1"][9] == "agree"
    assert released["L1-2"][9] == "disagree — it is covered"
    assert released["L1-3"][9] == "no answer"


def test_a_failed_mark_call_leaves_the_marks_empty(world: World) -> None:
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(codex=[codex_ok("T1", rows(1)), {"stdout": "", "exit": 1}])
    assert world.run("review") == 1
    assert "| — |" in world.text() and "agree" not in world.text()


def test_review_is_refused_while_a_loop_row_is_undecided(world: World) -> None:
    world.write_record([("L1-1", "", "")])
    assert world.run("review") == 2
    assert world.calls() == []


# ---------------------------------------------------------------------------
# The GLM review loop (criteria 32-39)
# ---------------------------------------------------------------------------


def test_the_review_prompts_give_both_paths() -> None:
    spec_review = (PROMPTS / "02a-spec-review.md").read_text(encoding="utf-8")
    review = (PROMPTS / "06-review.md").read_text(encoding="utf-8")
    assert review_prompt_problems(spec_review, review) == []
    assert review_prompt_problems(
        spec_review.replace("python3 scripts/stage2.py spec-review <change>", "codex exec -m gpt-6.1-sol"), review
    )
    assert review_prompt_problems(spec_review.replace("Opus 5.5", "Haiku 4.5"), review)
    assert review_prompt_problems(spec_review, review.replace("Phase 6 verdict:", "Verdict:"))
    assert review_prompt_problems(spec_review, review.replace("release-loop", "release"))
    assert review_prompt_problems(spec_review, review.replace("before you read any loop\nrow", "sometime"))
    assert review_prompt_problems(spec_review, review.replace("scripts/stage2.py", "stage2"))


def test_a_round_calls_its_rung_from_the_entry(world: World) -> None:
    """Criterion 4: round n calls modelle[n-1]; no rung of the ladder stands as a literal in the runner."""
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    called = [rung_of(call) for call in world.calls("pi")]
    assert called == stage2.ladder(world.root)
    source = (REPO_ROOT / "scripts" / "stage2.py").read_text(encoding="utf-8")
    for rung in stage2.ladder(world.root):
        assert rung not in source, f"{rung} stands as a literal in scripts/stage2.py"


def test_reordering_the_ladder_touches_no_code(world: World) -> None:
    """Criterion 5: the rounds call what the reordered list gives - the yaml changes, the runner does not."""
    endpoints = world.root / "model-endpoints.yaml"
    text = endpoints.read_text(encoding="utf-8")
    reordered = text.replace(
        "      - deepseek-v4.1-flash\n      - mimo-v2.6-flash\n      - mimo-v2.6-pro\n",
        "      - mimo-v2.6-pro\n      - deepseek-v4.1-flash\n",
    )
    assert reordered != text
    endpoints.write_text(reordered, encoding="utf-8")
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    called = [rung_of(call) for call in world.calls("pi")]
    assert called == ["mimo-v2.6-pro", "deepseek-v4.1-flash"]

    shutil.rmtree(world.record().parent)
    endpoints.write_text(
        reordered.replace(
            "      - mimo-v2.6-pro\n      - deepseek-v4.1-flash\n",
            "      - spike-a\n      - spike-b\n      - spike-c\n",
        ),
        encoding="utf-8",
    )
    (world.bin / "calls.jsonl").unlink()
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    called = [rung_of(call) for call in world.calls("pi")]
    assert called == ["spike-a", "spike-b", "spike-c"]


def test_the_reviewer_call_can_only_read_and_search(world: World) -> None:
    world.script(pi=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    argv = world.calls("pi")[0]["argv"]
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"read", "grep", "find", "ls"}
    assert "--approve" not in argv and "--no-approve" in argv


def test_the_reviewer_prompt_carries_the_loop_prompt_and_the_uncommitted_diff(world: World) -> None:
    (world.root / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
    (world.root / "src" / "new.py").write_text("fresh = 'untracked-content'\n", encoding="utf-8")
    world.script(pi=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    prompt = world.calls("pi")[0]["prompt_file"]
    assert (REPO_ROOT / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8").rstrip() in prompt
    assert "+value = 2" in prompt and "-value = 1" in prompt
    assert "src/new.py" in prompt and "untracked-content" in prompt
    assert "This is round 1; you are `deepseek-v4.1-flash`." in prompt


def test_a_round_is_written_as_its_rung(world: World) -> None:
    """Criterion 18: the heading, the Reviewer cell and the record's place carry the rung, outside the worktree."""
    world.script(pi=[{"stdout": rows(2)}])
    assert world.run("review-loop") == 0
    expected = Path(os.environ["XDG_STATE_HOME"]) / "coding-harness" / "stage2" / "demo" / "loop.md"
    text = expected.read_text(encoding="utf-8")
    assert "## Round 1 — deepseek-v4.1-flash, " in text
    ids = [
        cells[0] for cells in (stage2.split_row(line) for line in text.splitlines()) if cells and cells[0][:1] == "L"
    ]
    assert ids == ["L1-1", "L1-2"]
    assert all(cells[6] == "deepseek-v4.1-flash" for cells in stage2.record_rows(text))
    for path in world.root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            assert "FB1-unique-body" not in path.read_text(encoding="utf-8", errors="replace"), path
    assert not list(world.root.rglob("loop.md"))
    assert "GLM" not in world.text() and "Codex" not in world.text()


def test_a_round_that_did_not_review_writes_nothing(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 14: no block, exit 1, and the cause named on standard error."""
    world.script(pi=[{"stdout": rows(1), "stderr": "boom", "exit": 1}])
    assert world.run("review-loop") == 1
    assert not world.record().exists()
    assert "pi call failed" in capsys.readouterr().err


def test_a_round_without_a_finding_still_counts(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """A round that reports no finding is a round; two of them stop the loop before round 3 (criterion 7)."""
    world.script(pi=[{"stdout": "Nothing to report."}, {"stdout": "Still nothing."}])
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    assert "deepseek-v4.1-flash reported no finding." in record
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    assert "mimo-v2.6-flash reported no finding." in record
    capsys.readouterr()
    assert world.run("review-loop") == 2
    assert "round 2 wrote no taken row; the loop stops at 2." in capsys.readouterr().err
    assert len(world.calls("pi")) == 2


@pytest.mark.parametrize(
    "step",
    [{"stdout": "partial", "stderr": "boom", "exit": 1}, {"stdout": "  \n", "exit": 0}],
    ids=["non-zero-exit", "empty-answer"],
)
def test_a_call_without_an_answer_is_not_a_round(world: World, step: dict) -> None:
    """Criterion 14: a failed call, or one with no answer at all, writes no round; the loop itself still runs to three."""
    world.script(pi=[step, step, {"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 1
    assert world.run("review-loop") == 1
    assert not world.record().exists()
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    assert world.run("review-loop") == 2
    assert len(world.calls("pi")) == 5


@pytest.mark.parametrize("verb", ["review-loop", "probe"])
def test_the_loop_refuses_without_the_key(world: World, verb: str) -> None:
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    assert world.run(verb) == 2
    assert world.calls() == []


def test_the_loop_stops_at_three_rounds(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 6: three rounds run; the fourth is refused, also after the release."""
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    assert len(world.calls("pi")) == 3
    decide_record(world)
    capsys.readouterr()
    assert world.run("review-loop") == 2
    assert "3 rounds have run; the loop stops at 3." in capsys.readouterr().err
    assert len(world.calls("pi")) == 3
    # also after the release: the rounds stay counted
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert not world.record().exists()
    assert world.run("review-loop") == 2
    assert len(world.calls("pi")) == 3


def test_round_three_starts_only_after_a_taken_row(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 7: rounds 1 and 2 run as today; round 3 only when round 2 wrote at least one taken row."""
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — out of scope")
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — no evidence")
    capsys.readouterr()
    assert world.run("review-loop") == 2
    assert "round 2 wrote no taken row; the loop stops at 2." in capsys.readouterr().err
    assert len(world.calls("pi")) == 2
    text = world.record().read_text(encoding="utf-8")
    world.record().write_text(
        re.sub(
            r"^(\| L2-1 \|.*\|) rejected — no evidence \| no \|$",
            r"\1 taken — test_b | yes |",
            text,
            flags=re.M,
        ),
        encoding="utf-8",
    )
    assert world.run("review-loop") == 0
    called = [rung_of(call) for call in world.calls("pi")]
    assert called == ["deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"]


def test_a_call_over_the_time_limit_is_stopped(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 15: a call that outlasts the limit is stopped, and stopping is one of criterion 14's causes."""
    assert stage2.REVIEWER_MINUTES == 30
    monkeypatch.setattr(stage2, "REVIEWER_MINUTES", 0.03)
    world.script(pi=[{"stdout": "too late", "sleep": 30}])
    started = time.monotonic()
    assert world.run("review-loop") == 1
    assert time.monotonic() - started < 15
    assert not world.record().exists()
    assert "stopped by the reviewer time limit" in capsys.readouterr().err


def test_a_refused_rung_stops_the_run_without_fallback(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 17: an address that refuses a rung stops the run - no second launcher, no other rung, no other endpoint."""
    world.script(
        pi=[{"stdout": "", "stderr": "404: unknown model", "exit": 1}, {"stdout": "must not run"}],
        claude=[{"stdout": "must not run"}],
        codex=[codex_ok("T1", "must not run")],
    )
    assert world.run("review-loop") == 1
    assert [call["name"] for call in world.calls()] == ["pi"]
    argv = world.calls("pi")[0]["argv"]
    assert argv[argv.index("--model") + 1] == "opencode-go/deepseek-v4.1-flash"
    assert not world.record().exists()
    assert "pi call failed" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# release-loop (criteria 38, 39)
# ---------------------------------------------------------------------------


def test_release_without_a_verdict_line_refuses_and_changes_nothing(world: World) -> None:
    world.write_record([("L1-1", "taken — test_a", "no")])
    for lines in ((), ("No verdict here.",)):
        if lines:
            world.write_findings(*lines)
        before = world.findings.read_bytes() if world.findings.exists() else None
        assert world.run("release-loop") == 2
        assert (world.findings.read_bytes() if world.findings.exists() else None) == before
        assert world.record().exists()


def test_the_release_carries_each_rows_reviewer(world: World) -> None:
    """Criterion 19: every released row carries the rung its round had, not one fixed name."""
    world.write_record(
        [("L1-1", "taken — test_a", "yes"), ("L1-2", "rejected — out of scope", ""), ("L1-3", "taken — crit 4", "no")]
    )
    world.write_findings("## Phase 6 — deepseek-v4.1-flash, 2026-09-30", VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    assert stage2.RELEASE_HEADING + " " in text and re.search(r"^Rounds run: 1$", text, re.M)
    released = [
        cells for cells in (stage2.split_row(line) for line in text.splitlines()) if cells and cells[0][:3] == "L1-"
    ]
    assert [(c[0], c[6], c[7], c[8], c[9]) for c in released] == [
        ("L1-1", "deepseek-v4.1-flash", "taken — test_a", "yes", "—"),
        ("L1-2", "deepseek-v4.1-flash", "rejected — out of scope", "", "—"),
        ("L1-3", "deepseek-v4.1-flash", "taken — crit 4", "no", "—"),
    ]
    assert not world.record().exists()


@pytest.mark.parametrize(
    "line",
    [
        "Phase 6 verdict: codex T1, 2026-09-30",
        "Phase 6 verdict: Opus 5.5 3f1c2a9e-0000-4000-8000-000000000001, 2026-10-01",
        "Phase 6 verdict: opus, 2026-10-01",
        "Phase 6 verdict: codex T1, 2026-09-30 ",
        "Phase 6 verdict: codex T1, 2026-09-30.",
        "Phase 6 verdict: Opus 5.5, 2026-10-01 .",
    ],
    ids=["as-written", "named-reviewer", "no-session", "trailing-space", "full-stop", "space-and-full-stop"],
)
def test_release_accepts_the_verdict_forms_the_prompts_can_produce(world: World, line: str) -> None:
    """Repair round 1, F-4: a reviewer that names itself, has no session id or ends its line loosely is not refused."""
    world.write_findings(line)
    assert world.run("release-loop") == 0
    assert stage2.NO_LOOP_LINE in world.text()


@pytest.mark.parametrize(
    "line",
    [
        "Phase 6 verdict: pending",
        "Phase 6 verdict: codex T1, yesterday",
        "Phase 6 verdict, 2026-10-01",
        "phase 6 verdict: x, 2026-10-01",
        "Phase 6 verdict: pending, 2026-10-01",
        "Phase 6 verdict: Pending T1, 2026-10-01",
    ],
    ids=["no-date", "word-for-date", "no-colon", "lower-case", "pending-with-a-date", "pending-with-a-session"],
)
def test_a_refused_verdict_line_is_named(world: World, line: str, capsys: pytest.CaptureFixture[str]) -> None:
    """Repair round 1, F-4: a line that starts like a verdict and does not count is shown, with the form it lacks."""
    world.write_findings("## Phase 6 — Codex, 2026-10-01", line)
    before = world.findings.read_bytes()
    assert world.run("release-loop") == 2
    error = capsys.readouterr().err
    assert world.findings.read_bytes() == before
    assert f"`{line}`" in error and "does not have the form" in error


def test_release_without_a_record_says_so_once(world: World) -> None:
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert world.run("release-loop") == 0
    assert world.text().count(stage2.NO_LOOP_LINE) == 1


@pytest.mark.parametrize(
    "rows_",
    [
        [("L1-1", "", "")],
        [("L1-1", "taken — test_a", "")],
        [("L1-1", "taken — test_a", "maybe")],
        [("L1-1", "taken — test_a", "no"), ("L1-2", "pending", "")],
    ],
    ids=["empty", "taken-without-mark", "taken-with-a-wrong-mark", "one-of-two"],
)
def test_an_undecided_loop_row_holds_the_next_round_and_the_release(world: World, rows_: list) -> None:
    world.write_record(rows_)
    world.write_findings(VERDICT)
    before = world.findings.read_bytes()
    assert world.run("release-loop") == 2
    assert world.findings.read_bytes() == before
    world.script(pi=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 2
    assert world.calls() == []


def released_rows(text: str) -> list[list[str]]:
    """The cells of every row of the released block, whatever the row."""
    block = text[text.rfind(stage2.RELEASE_HEADING) :]
    return [c for c in (stage2.split_row(line) for line in block.splitlines()) if c and c[0].startswith("L")]


def test_a_pipe_inside_a_reviewers_finding_reaches_findings(world: World) -> None:
    """Repair round 1, F-2 (a): a shell pipe in a finding is part of the finding, not a seventh cell."""
    said = "| X1 | MAJOR | SPEC | a | src/app.py:1 | the filter `cat x | sort` drops the last row |"
    world.script(pi=[{"stdout": said}])
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    assert [row[0] for row in stage2.record_rows(record)] == ["L1-1"]
    decide_record(world)
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    assert "No loop row was reported." not in text
    (row,) = released_rows(text)
    assert row[0] == "L1-1" and "cat x" in row[5] and "sort` drops the last row" in row[5]
    assert row[6:9] == ["deepseek-v4.1-flash", "taken — test_a", "no"]


def test_a_line_that_is_not_a_loop_row_is_carried_to_findings(world: World) -> None:
    """Repair round 1, F-2 (a): what the release cannot read as a row arrives as it stands, and the record goes last."""
    answer = rows(1) + "\n| half | a row |\nA remark.\n"
    world.script(pi=[{"stdout": answer}])
    assert world.run("review-loop") == 0
    decide_record(world)
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    assert "| half | a row |" in text and "A remark." in text
    assert not world.record().exists()


@pytest.mark.parametrize(
    "reason", ["rejected — the spec says a | b", "rejected — the spec says a\\|b"], ids=["raw", "escaped"]
)
def test_a_pipe_in_a_status_reason_keeps_the_row_decided(world: World, reason: str) -> None:
    """Repair round 1, F-2 (b): the implementer's reason may hold a pipe; the row stays a row, with its reason."""
    world.write_record([("L1-1", reason, ""), ("L1-2", "taken — test_a", "no")])
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    assert "No loop row was reported." not in text
    released = {row[0]: row for row in released_rows(text)}
    assert sorted(released) == ["L1-1", "L1-2"]
    assert "the spec says a" in released["L1-1"][7] and released["L1-1"][7].endswith("b")
    assert released["L1-1"][8] == "" and released["L1-2"][8] == "no"


def test_a_pipe_in_a_status_reason_does_not_hide_an_undecided_row(world: World) -> None:
    """Repair round 1, F-2 (b): a row whose reason holds a pipe is still held to the decision rule."""
    world.write_record([("L1-1", "taken — a | b", "")])
    world.write_findings(VERDICT)
    before = world.findings.read_bytes()
    assert world.run("release-loop") == 2
    assert world.findings.read_bytes() == before and world.record().exists()


def test_a_damaged_loop_row_refuses_instead_of_vanishing(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Repair round 1, F-2: a line that carries a loop id and cannot be read is named, and nothing is deleted."""
    world.write_record([("L1-1", "taken — test_a", "no")])
    with world.record().open("a", encoding="utf-8") as handle:
        handle.write("| L1-2 | MAJOR | broken |\n")
    world.write_findings(VERDICT)
    before = world.findings.read_bytes()
    for verb in ("release-loop", "review-loop"):
        assert world.run(verb) == 2
        assert "L1-2" in capsys.readouterr().err
    assert world.findings.read_bytes() == before and world.record().exists()
    assert world.calls() == []


REVIEWER_PROSE = ["## Why this matters", "A remark.", "```sh", "# run: grep foo \\| wc -l", "ls", "```"]


def test_every_line_of_a_reviewers_answer_reaches_findings_even_one_that_starts_with_a_hash(world: World) -> None:
    """Repair round 2, F-10: a heading or a code comment of the reviewer is not one of the record's own headings."""
    world.script(pi=[{"stdout": rows(1) + "\n" + "\n".join(REVIEWER_PROSE) + "\n"}])
    assert world.run("review-loop") == 0
    decide_record(world)
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    lines = text.splitlines()
    for line in REVIEWER_PROSE:
        assert line in lines, line
    assert "# Loop record" not in text and "## Round 1 — deepseek" not in text, "the record's own headings were carried"
    assert not world.record().exists()


def test_an_answer_without_rows_reaches_findings_as_it_came(world: World) -> None:
    """Repair round 2, F-10: the blank lines and the `#` lines of an answer with no row are kept as they stand."""
    answer = "## Notes\n\nFirst paragraph.\n\n# a comment line\n\nLast."
    world.script(pi=[{"stdout": answer}])
    assert world.run("review-loop") == 0
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert answer in world.text()
    assert "# Loop record" not in world.text() and "## Round 1 — deepseek" not in world.text()


def test_a_reviewers_lines_that_look_like_the_records_own_text_are_carried(world: World) -> None:
    """Repair round 2, F-10: the intro sentences are the runner's only where the runner wrote them."""
    world.script(pi=[{"stdout": stage2.RECORD_INTRO}])
    assert world.run("review-loop") == 0
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    lines = world.text().splitlines()
    for line in stage2.RECORD_INTRO.splitlines():
        assert line in lines, line


def test_a_new_records_intro_names_the_not_a_test_status_and_the_fixed_mark(world: World) -> None:
    """Repair round 1, L1-2. Planted fault: the intro a new record gets names only the two old Status words."""
    world.script(pi=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    assert "taken — not a test — <reason>" in record
    assert "a row the repair marked `fixed` needs the mark too" in record


def test_a_rounds_words_do_not_swallow_the_rows_of_the_next(world: World) -> None:
    """Repair round 2: one round's words end at the next round heading; round 2's rows are read, round 1's words carried."""
    world.script(pi=[{"stdout": rows(1) + "\nA remark of round 1."}, {"stdout": rows(1) + "\nA remark of round 2."}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    assert [r[0] for r in released_rows(text) if len(r) == 10] == ["L1-1", "L2-1"]
    assert "A remark of round 1." in text and "A remark of round 2." in text
    assert re.search(r"^Rounds run: 2$", text, re.M)


@pytest.mark.parametrize("verb", ["release-loop", "review-loop", "review"])
def test_a_table_line_a_reviewer_wrote_with_a_loop_id_is_carried_not_refused(
    world: World, verb: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Repair round 2, F-11: the refusal is for the rows the implementer must decide, not the reviewer's own words."""
    said = rows(1) + "\n| L1-1 | still open from the last round |\n"
    if verb == "review":
        world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")], pi=[{"stdout": said}])
    elif verb == "review-loop":
        world.script(pi=[{"stdout": said}, {"stdout": "Nothing to report."}])
    else:
        world.script(pi=[{"stdout": said}])
    assert world.run("review-loop") == 0
    decide_record(world)
    if verb == "release-loop":
        world.write_findings(VERDICT)
    capsys.readouterr()
    assert world.run(verb) == 0, capsys.readouterr().err
    if verb == "review-loop":
        assert "## Round 2 — mimo-v2.6-flash, " in world.record().read_text(encoding="utf-8")
        assert "This is round 2; you are `mimo-v2.6-flash`." in world.calls("pi")[-1]["prompt_file"]
        return
    text = world.text()
    assert "| L1-1 | still open from the last round |" in text.splitlines()
    assert [r[0] for r in released_rows(text) if len(r) == 10] == ["L1-1"]
    assert not world.record().exists()


def test_a_damaged_row_of_the_record_still_refuses_beside_reviewer_text(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    """Repair round 2, F-11: the record's own rows are held to the rule even when the reviewer's text stands below them."""
    world.script(pi=[{"stdout": rows(2) + "\n| L1-1 | still open |\n"}])
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    world.record().write_text(re.sub(r"^\| L1-2 \|.*$", "| L1-2 | MAJOR |", record, flags=re.M), encoding="utf-8")
    world.write_findings(VERDICT)
    before = world.findings.read_bytes()
    capsys.readouterr()
    for verb in ("release-loop", "review-loop"):
        assert world.run(verb) == 2
        assert "L1-2" in capsys.readouterr().err
    assert world.findings.read_bytes() == before and world.record().exists()


# ---------------------------------------------------------------------------
# The repair of the taken findings (stage2-repair criteria 1-28)
# ---------------------------------------------------------------------------


FIX_TEST = (
    "from pathlib import Path\n\n\ndef test_fix():\n"
    '    value = (Path(__file__).resolve().parent.parent / "src" / "app.py").read_text(encoding="utf-8")\n'
    '    assert "value = 2" in value\n'
)


def seed_tests(world: World) -> None:
    """A committed `tests/test_seed.py`, so a red-first checkout has a baseline tree to take tests from."""
    tests = world.root / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "test_seed.py").write_text("def test_seed():\n    assert True\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "seed tests")


def repair_step(**more: object) -> dict:
    """A model step that repairs `src/app.py`, plants the test that is red on it, and measures the plan."""
    return {
        "stdout": "L1-1: fixed — tests/test_fix.py::test_fix",
        "plant": {"src/app.py": "value = 2\n", "tests/test_fix.py": FIX_TEST},
        "append": {"plans/changes/demo/plan.md": "2026-10-12 10:00–10:05, 5 min\n"},
        **more,
    }


def codex_step(step: dict, number: int = 1) -> dict:
    """The step the Codex stand-in plays for a repair step: its answer in the answer file, a thread event on stdout."""
    if step.get("exit"):
        return step
    rest = {key: value for key, value in step.items() if key != "stdout"}
    return codex_ok(f"TR{number}", step.get("stdout", ""), **rest)


def script_repair(world: World, steps: list[dict], **more: object) -> None:
    """Attempts 1 and 2 of a repair are Codex, attempt 3 is Sonnet (ADR 0017); `steps` follow that order."""
    scripted: dict[str, object] = {"codex": [codex_step(s, n) for n, s in enumerate(steps[:2], 1)], **more}
    if steps[2:]:
        scripted["claude"] = steps[2:]
    world.script(**scripted)


def repair_calls(world: World) -> list[dict]:
    """Every model call of the run, in the order it started."""
    return [call for call in world.calls() if call["name"] in ("codex", "claude")]


def prompt_of(call: dict) -> str:
    """The prompt a model call received: a file for Claude Code, the last argument for Codex."""
    return call["prompt_file"] or call["argv"][-1]


def repair_world(world: World, *record: tuple[str, str, str]) -> str:
    """A clean tree with a committed tests/ directory and a decided loop record, scripted for one repair."""
    seed_tests(world)
    world.write_record([*record] or [("L1-1", "taken — test_a", "no")])
    script_repair(world, [repair_step()], make=[{"stdout": "green\n"}])
    return git(world.root, "rev-parse", "HEAD")


def released_cells(ident: str, status: str, broke: str, finding: str) -> list[str]:
    return [ident, "MAJOR", "MAINT", "impl", "src/app.py:1", finding, "deepseek-v4.1-flash", status, broke, "—"]


def phase6_cells(ident: str, status: str, finding: str) -> list[str]:
    return [ident, "MAJOR", "SPEC", "base", "spec.md:3", finding, "Codex", status, "—"]


def released_block(rows_: list[list[str]]) -> str:
    return f"{stage2.RELEASE_HEADING} 2026-10-12\n\nRounds run: 1\n\n" + stage2.render_table(
        stage2.RELEASED_COLUMNS, rows_
    )


def phase6_block(rows_: list[list[str]]) -> str:
    return "## Phase 6 — Codex, 2026-10-12\n\n" + stage2.render_table(stage2.ROW_COLUMNS, rows_)


def test_repair_lists_every_taken_row_and_no_rejected_or_fixed_one(world: World) -> None:
    """Criterion 1. Planted fault: a released block or a phase-6 table is not read, or a rejected row is listed."""
    baseline = repair_world(
        world,
        ("L1-1", "taken — test_a", "no"),
        ("L1-2", "rejected — out of scope", ""),
    )
    world.write_findings(
        VERDICT,
        released_block(
            [
                released_cells("L1-3", "taken — test_c", "no", "released finding"),
                released_cells("L1-4", "rejected — no evidence", "", "released rejection"),
                released_cells("L1-5", "fixed — tests/test_seed.py::test_seed", "no", "released repaired"),
            ]
        ),
        phase6_block(
            [
                phase6_cells("F-1", "taken — crit 6", "phase finding"),
                phase6_cells("F-2", "rejected — covered", "phase rejection"),
                phase6_cells("F-3", "fixed — tests/test_seed.py::test_seed", "phase repaired"),
            ]
        ),
    )
    answer = "\n".join(
        [
            "L1-1: fixed — tests/test_fix.py::test_fix",
            "L1-3: fixed — tests/test_fix.py::test_fix",
            "F-1: fixed — tests/test_fix.py::test_fix",
        ]
    )
    script_repair(world, [repair_step(stdout=answer)], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[0])
    assert f"Repair baseline: {baseline}" in prompt
    for listed in (
        "- L1-1 [MAJOR, MAINT] src/app.py:1: finding of L1-1 — Status: taken — test_a",
        "- L1-3 [MAJOR, MAINT] src/app.py:1: released finding — Status: taken — test_c",
        "- F-1 [MAJOR, SPEC] spec.md:3: phase finding — Status: taken — crit 6",
    ):
        assert listed in prompt, listed
    for body in ("finding of L1-2", "released rejection", "phase rejection", "released repaired", "phase repaired"):
        assert body not in prompt, body


def test_the_repair_prompt_carries_the_contract_and_ends_with_the_read_request(world: World) -> None:
    """Criterion 2. Planted fault: the plan left out, or the read request standing before the rows."""
    baseline = repair_world(world)
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[0])
    assert stage2.REPAIR_FORMAT in prompt and stage2.REPAIR_FORMAT_FILE_TOOLS not in prompt
    assert "you cannot run commands" not in prompt
    assert "may run tests and `make verify`" in prompt and "Do not commit" in prompt
    assert f"Repair baseline: {baseline}" in prompt
    assert "## Taken rows" in prompt
    assert "## Accepted spec" in prompt and "# Spec" in prompt
    assert "## Accepted plan" in prompt and "## Time used" in prompt
    assert (PROMPTS / "04-implement.md").read_text(encoding="utf-8").rstrip() in prompt
    assert "Stay inside the repository." in prompt
    assert prompt.rstrip().endswith(stage2.READ_REQUEST)


def test_repair_with_nothing_taken_refuses_before_any_call(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 3. Planted fault: a model call with an empty row list, or a refusal after the key."""
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret before the refusals: {name}"))
    seed_tests(world)
    world.write_record([("L1-1", "rejected — out of scope", "")])
    world.script(claude=[{"stdout": "must not run"}])
    assert world.run("repair") == 2
    assert world.calls() == [] and not world.findings.exists()
    assert "no row is taken" in capsys.readouterr().err
    shutil.rmtree(world.record().parent)
    assert world.run("repair") == 2
    assert world.calls() == []


def test_an_undecided_row_holds_the_repair(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 4. Planted fault: an `open` phase-6 row ignored, or a refusal that names no ID."""
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret before the refusals: {name}"))
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no"), ("L1-2", "", "")])
    world.script(claude=[{"stdout": "must not run"}])
    assert world.run("repair") == 2
    assert world.calls() == []
    assert "L1-2" in capsys.readouterr().err
    world.write_record([("L1-1", "taken — test_a", "no"), ("L1-2", "rejected — out of scope", "")])
    world.write_findings(VERDICT, phase6_block([phase6_cells("F-1", "open", "phase finding")]))
    assert world.run("repair") == 2
    assert world.calls() == []
    error = capsys.readouterr().err
    assert "F-1" in error and "waiting for a decision" in error


def test_a_doubled_taken_id_refuses_the_repair(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 5. Planted fault: the first row of an ID wins and the call starts."""
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret before the refusals: {name}"))
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.write_findings(VERDICT, released_block([released_cells("L1-1", "taken — test_c", "no", "released finding")]))
    world.script(claude=[{"stdout": "must not run"}])
    assert world.run("repair") == 2
    assert world.calls() == []
    error = capsys.readouterr().err
    assert "L1-1" in error and "same id" in error


def test_repair_requires_a_clean_tree_a_spec_and_a_plan_with_its_time_heading(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Criterion 6. Planted fault: a preflight that lets one of the three states reach a model call."""
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret before the refusals: {name}"))
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(claude=[{"stdout": "must not run"}])
    plan = world.plan.read_text(encoding="utf-8")
    spec = (world.root / "plans" / "changes" / "demo" / "spec.md").read_text(encoding="utf-8")

    world.plan.unlink()
    assert world.run("repair") == 2 and world.calls() == []

    # committed, so the tree stays clean and the time heading itself is what refuses
    world.plan.write_text("---\nbead: demo-1\n---\n# Plan\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "plan without the time heading")
    assert world.run("repair") == 2 and world.calls() == []
    world.plan.write_text(plan, encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "plan restored")

    (world.root / "plans" / "changes" / "demo" / "spec.md").write_text("---\ntitle: Spec\n---\n", encoding="utf-8")
    assert world.run("repair") == 2 and world.calls() == []
    (world.root / "plans" / "changes" / "demo" / "spec.md").write_text(spec, encoding="utf-8")

    (world.root / "src" / "dirty.py").write_text("dirty = True\n", encoding="utf-8")
    assert world.run("repair") == 2 and world.calls() == []


def test_repair_uses_codex_at_max_effort(world: World) -> None:
    """Criterion 1. Planted fault: the first attempt on Claude Code, GLM or another effort."""
    repair_world(world)
    assert world.run("repair") == 0
    assert world.calls("claude") == []
    (call,) = world.calls("codex")
    argv = call["argv"]
    assert argv[argv.index("-m") + 1] == "gpt-6.1-sol"
    assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["repair"]}"' in argv
    assert "resume" not in argv, "a repair attempt resumed a thread"
    assert "route codex · endpoint openai-codex · model gpt-6.1-sol" in world.text()


def test_codex_repair_uses_workspace_write_without_bypass(world: World) -> None:
    """Criterion 2. Planted fault: a read-only repair, an enabled hook or memory, or a widening flag."""
    repair_world(world)
    assert world.run("repair") == 0
    argv = world.calls("codex")[0]["argv"]
    assert 'sandbox_mode="workspace-write"' in argv
    assert not any("read-only" in part for part in argv[:-1])
    for feature in ("hooks", "memories"):
        assert argv[argv.index(feature) - 1] == "--disable", feature
    assert "--add-dir" not in argv and "--full-auto" not in argv
    assert not any("bypass" in part or "dangerously" in part for part in argv)
    assert world.calls("codex")[0]["cwd"] == str(world.root)


def test_repair_retry_uses_fresh_codex_with_diagnostics(world: World) -> None:
    """Criterion 4. Planted fault: the retry resumes the first thread, loses its diagnostics or leaves Codex."""
    repair_world(world)
    script_repair(world, [{"stdout": "still looking"}, repair_step()], make=[{"stdout": "green\n"}] * 2)
    assert world.run("repair") == 0
    first, second = world.calls("codex")
    for call in (first, second):  # both attempts keep the repair entry (bead coding-harness-yzk)
        assert f'model_reasoning_effort="{stage2.CODEX_EFFORTS["repair"]}"' in call["argv"]
    assert "resume" not in first["argv"] and "resume" not in second["argv"]
    assert world.calls("claude") == []
    prompt = prompt_of(second)
    assert "Attempt 1 (codex):" in prompt and "did not add a measured line" in prompt
    text = world.text()
    assert "attempt 2 · route codex-repair" in text and "reason first Codex post-run check failed" in text


@pytest.mark.parametrize("deleted_attempt", [1, 2])
@pytest.mark.parametrize(
    "deleted_inputs",
    [
        ("plans/changes/demo/spec.md",),
        ("plans/changes/demo/plan.md",),
        ("plans/changes/demo/decisions.md",),
        ("plans/changes/demo/design.md",),
        ("prompts/04-implement.md",),
        ("AGENTS.md",),
        (
            "plans/changes/demo/spec.md",
            "plans/changes/demo/plan.md",
            "plans/changes/demo/decisions.md",
            "plans/changes/demo/design.md",
            "prompts/04-implement.md",
            "AGENTS.md",
        ),
    ],
    ids=["spec", "plan", "decisions", "design", "phase-prompt", "agent-rules", "all-inputs"],
)
def test_repair_retry_starts_after_a_completed_attempt_deletes_plan(
    world: World, monkeypatch: pytest.MonkeyPatch, deleted_attempt: int, deleted_inputs: tuple[str, ...]
) -> None:
    """F-11: every prompt input can be deleted without preventing either retry's diagnostics.

    The F-8 name remains a criterion-ledger anchor; it covers the change files, phase prompt and rules.
    """
    folder = world.plan.parent
    for name in ("decisions.md", "design.md"):
        (folder / name).write_text(f"---\ntitle: {name}\nbead: demo-1\n---\n\n# {name}\n", encoding="utf-8")
    baseline = repair_world(world)
    inputs = {
        relative: (world.root / relative).read_bytes()
        for relative in (
            "plans/changes/demo/spec.md",
            "plans/changes/demo/plan.md",
            "plans/changes/demo/decisions.md",
            "plans/changes/demo/design.md",
            "prompts/04-implement.md",
            "AGENTS.md",
        )
    }
    steps = [{"stdout": "still looking"}] * (deleted_attempt - 1)
    steps += [repair_step(delete=list(deleted_inputs), append={}), repair_step()]
    script_repair(
        world,
        steps,
        make=[{"stdout": f"post-run-check-{n}\n", "exit": 1} for n in range(1, deleted_attempt + 1)]
        + [{"stdout": "green\n"}],
    )
    real_begin_work_call = stage2.begin_work_call
    real_checkpoint = stage2.checkpoint
    ready_attempts: list[int] = []
    checkpoints: list[int] = []

    def begin_work_call(*args, **kwargs):
        # Check on disk before either transport starts, including inputs not inlined in its prompt.
        for relative, content in inputs.items():
            assert (world.root / relative).is_file(), f"{relative} was not restored before the next attempt"
            assert (world.root / relative).read_bytes() == content
        ready_attempts.append(len(repair_calls(world)) + 1)
        real_begin_work_call(*args, **kwargs)

    def checkpoint(*args, **kwargs):
        checkpoints.append(len(repair_calls(world)))
        real_checkpoint(*args, **kwargs)

    monkeypatch.setattr(stage2, "begin_work_call", begin_work_call)
    monkeypatch.setattr(stage2, "checkpoint", checkpoint)
    assert world.run("repair") == 0
    calls = repair_calls(world)
    assert len(calls) == deleted_attempt + 1
    assert ready_attempts == list(range(1, deleted_attempt + 2))
    assert checkpoints == [deleted_attempt + 1], "the attempt that deleted an input reached a checkpoint"
    assert len(world.calls("codex")) == 2
    assert len(world.calls("claude")) == deleted_attempt - 1
    assert all("resume" not in call["argv"] for call in world.calls("codex"))
    retry_prompt = prompt_of(calls[deleted_attempt])
    for attempt in range(1, deleted_attempt + 1):
        route = "codex" if attempt == 1 else "codex-repair"
        assert f"Attempt {attempt} ({route}):" in retry_prompt
        assert f"post-run-check-{attempt}" in retry_prompt and f"post-run-check-{attempt}" in world.text()
    if "plans/changes/demo/plan.md" in deleted_inputs:
        assert "plan.md cannot be read." in retry_prompt
    else:
        assert "did not add a measured line" in retry_prompt
    for name in ("spec.md", "plan.md"):
        content = inputs[f"plans/changes/demo/{name}"].decode("utf-8")
        assert f"## Accepted {name.removesuffix('.md')}\n\n{content}" in retry_prompt
    assert inputs["prompts/04-implement.md"].decode("utf-8").rstrip() in retry_prompt
    assert inputs["AGENTS.md"].decode("utf-8").rstrip() in retry_prompt
    for relative in deleted_inputs:
        assert f"> - `{relative}` +0 -{len(inputs[relative].splitlines())}" in world.text()
    for relative, content in inputs.items():
        if relative != "plans/changes/demo/plan.md":
            assert (world.root / relative).read_bytes() == content
    assert "2026-10-12 10:00–10:05, 5 min" in world.plan.read_text(encoding="utf-8")
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    assert git(world.root, "status", "--porcelain") == ""


@pytest.mark.parametrize("corrupted_attempts", [(1,), (2,), (1, 2)], ids=["first", "second", "both"])
@pytest.mark.parametrize(
    "corrupted_inputs",
    [
        ("plans/changes/demo/spec.md",),
        ("plans/changes/demo/plan.md",),
        ("plans/changes/demo/decisions.md",),
        ("plans/changes/demo/design.md",),
        ("prompts/04-implement.md",),
        ("AGENTS.md",),
        (
            "plans/changes/demo/spec.md",
            "plans/changes/demo/plan.md",
            "plans/changes/demo/decisions.md",
            "plans/changes/demo/design.md",
            "prompts/04-implement.md",
            "AGENTS.md",
        ),
    ],
    ids=["spec", "plan", "decisions", "design", "phase-prompt", "agent-rules", "all-inputs"],
)
def test_repair_retry_restores_non_utf8_prompt_inputs(
    world: World,
    monkeypatch: pytest.MonkeyPatch,
    corrupted_attempts: tuple[int, ...],
    corrupted_inputs: tuple[str, ...],
) -> None:
    """F-12: undecodable inputs cannot prevent a fresh Codex retry or the Sonnet fallback."""
    for name in ("decisions.md", "design.md"):
        (world.plan.parent / name).write_text(f"---\ntitle: {name}\nbead: demo-1\n---\n\n# {name}\n", encoding="utf-8")
    baseline = repair_world(world)
    original = {relative: (world.root / relative).read_bytes() for relative in corrupted_inputs}
    failed_attempts = max(corrupted_attempts)
    script_repair(
        world,
        [repair_step(append={}) for _ in range(failed_attempts)] + [repair_step()],
        make=[{"stdout": "green\n"}] * 3,
    )
    real_codex, real_begin = stage2.run_codex, stage2.begin_work_call
    real_input, real_checkpoint = stage2.prompt_input, stage2.checkpoint
    observed_inputs: list[dict[str, bytes]] = []
    checkpoints: list[int] = []

    def codex(*args, **kwargs):
        result = real_codex(*args, **kwargs)
        if len(world.calls("codex")) in corrupted_attempts:
            for relative, content in original.items():
                (world.root / relative).write_bytes(b"\xff" + content)
        return result

    def begin_work_call(*args, **kwargs):
        # Observe bytes without decoding or asserting here, so the baseline shows its actual crash.
        observed_inputs.append({relative: (world.root / relative).read_bytes() for relative in original})
        real_begin(*args, **kwargs)

    def prompt_input(*args, **kwargs):
        assert not repair_calls(world), "a later prompt reread an input after the first model call"
        return real_input(*args, **kwargs)

    def checkpoint(*args, **kwargs):
        checkpoints.append(len(repair_calls(world)))
        real_checkpoint(*args, **kwargs)

    monkeypatch.setattr(stage2, "run_codex", codex)
    monkeypatch.setattr(stage2, "begin_work_call", begin_work_call)
    monkeypatch.setattr(stage2, "prompt_input", prompt_input)
    monkeypatch.setattr(stage2, "checkpoint", checkpoint)
    assert world.run("repair") == 0
    calls = repair_calls(world)
    assert [call["name"] for call in calls] == ["codex", "codex", "claude"][: failed_attempts + 1]
    assert observed_inputs == [original] * (failed_attempts + 1)
    assert checkpoints == [failed_attempts + 1], "a failed attempt reached the checkpoint"
    assert all("resume" not in call["argv"] for call in world.calls("codex"))
    final_prompt = prompt_of(calls[-1])
    for attempt in range(1, failed_attempts + 1):
        route = "codex" if attempt == 1 else "codex-repair"
        assert f"Attempt {attempt} ({route}):" in final_prompt
        diagnostics = "\n".join(prompt_entry(final_prompt, attempt, route))
        if attempt in corrupted_attempts and any(relative.startswith("plans/") for relative in original):
            assert "Derived-file preparation failed" in diagnostics
        else:
            assert "did not add a measured line" in diagnostics
    for relative, content in original.items():
        if relative not in ("plans/changes/demo/decisions.md", "plans/changes/demo/design.md"):
            assert content.decode("utf-8").rstrip() in final_prompt
        assert f"> - `{relative}`" in world.text()
    assert "2026-10-12 10:00–10:05, 5 min" in world.plan.read_text(encoding="utf-8")
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    assert git(world.root, "status", "--porcelain") == ""


def test_repair_retry_restores_aliased_and_directory_inputs_without_following(
    world: World, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """F-13/F-14: restoration removes what stands at an input's path, never writing through it."""
    baseline = repair_world(world)
    spec, plan = world.root / "plans/changes/demo/spec.md", world.plan
    spec_bytes, plan_bytes = spec.read_bytes(), plan.read_bytes()
    outside = tmp_path / "outside-target.md"
    outside.write_bytes(b"outside content\n")
    script_repair(
        world,
        [repair_step(append={}), repair_step(append={}), repair_step()],
        make=[{"stdout": "green\n"}] * 3,
    )
    real_codex, real_begin = stage2.run_codex, stage2.begin_work_call
    observed: list[tuple[bytes, bytes, bool, bool]] = []

    def codex(*args, **kwargs):
        result = real_codex(*args, **kwargs)
        count = len(world.calls("codex"))
        if count == 1:
            spec.unlink()
            spec.symlink_to(outside)
        elif count == 2:
            plan.unlink()
            plan.mkdir()
        return result

    def begin_work_call(*args, **kwargs):
        observed.append(
            (spec.read_bytes(), plan.read_bytes(), spec.is_symlink(), plan.is_file() and not plan.is_symlink())
        )
        real_begin(*args, **kwargs)

    monkeypatch.setattr(stage2, "run_codex", codex)
    monkeypatch.setattr(stage2, "begin_work_call", begin_work_call)
    assert world.run("repair") == 0
    assert outside.read_bytes() == b"outside content\n", "restoration wrote through the symlink"
    assert [call["name"] for call in repair_calls(world)] == ["codex", "codex", "claude"]
    assert observed == [(spec_bytes, plan_bytes, False, True)] * 3
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"


@pytest.mark.parametrize("edited_attempt", [1, 2])
@pytest.mark.parametrize(
    "edited_input",
    ["plans/changes/demo/spec.md", "plans/changes/demo/plan.md", "prompts/04-implement.md", "AGENTS.md"],
    ids=["spec", "plan", "phase-prompt", "agent-rules"],
)
def test_repair_prompts_keep_the_initial_input_snapshot(
    world: World, monkeypatch: pytest.MonkeyPatch, edited_attempt: int, edited_input: str
) -> None:
    """F-11/F-12: failed edits cannot replace later calls' accepted inputs, in the prompt or on disk."""
    baseline = repair_world(world)
    original = (world.root / edited_input).read_text(encoding="utf-8")
    marker = "FAILED-ATTEMPT-INPUT-EDIT"
    # Keep the time heading available: the failure is verification, not inability to read the plan.
    edited = original + f"\n{marker}\n"
    steps = [{"stdout": "still looking"}] * (edited_attempt - 1)
    steps += [repair_step(plant={edited_input: edited}, append={})]
    last = repair_step()
    last["plant"][edited_input] = original
    steps.append(last)
    script_repair(
        world,
        steps,
        make=[{"stdout": f"snapshot-diagnostic-{n}\n", "exit": 1} for n in range(1, edited_attempt + 1)]
        + [{"stdout": "green\n"}],
    )
    real_begin = stage2.begin_work_call

    def begin_work_call(*args, **kwargs):
        assert (world.root / edited_input).read_text(encoding="utf-8") == original
        real_begin(*args, **kwargs)

    monkeypatch.setattr(stage2, "begin_work_call", begin_work_call)
    assert world.run("repair") == 0
    calls = repair_calls(world)
    assert len(calls) == edited_attempt + 1
    assert [call["name"] for call in calls] == ["codex", "codex", "claude"][: edited_attempt + 1]
    for call in calls:
        prompt = prompt_of(call)
        assert original.rstrip() in prompt
        assert marker not in prompt
    for attempt in range(1, edited_attempt + 1):
        route = "codex" if attempt == 1 else "codex-repair"
        assert f"Attempt {attempt} ({route}):" in prompt_of(calls[-1])
        assert f"snapshot-diagnostic-{attempt}" in prompt_of(calls[-1])
    assert all("resume" not in call["argv"] for call in world.calls("codex"))
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    assert git(world.root, "status", "--porcelain") == ""


def test_two_failed_codex_repairs_fall_back_to_sonnet(world: World) -> None:
    """Criterion 5. Planted fault: GLM as the fallback, lost earlier evidence or a fourth attempt."""
    repair_world(world)
    script_repair(
        world,
        [{"stdout": "still looking"}, {"stdout": "still stuck"}, repair_step(), {"stdout": "must not run"}],
        make=[{"stdout": "green\n"}] * 4,
    )
    assert world.run("repair") == 0
    assert len(world.calls("codex")) == 2 and len(world.calls("claude")) == 1
    (sonnet,) = world.calls("claude")
    argv = sonnet["argv"]
    assert argv[argv.index("--model") + 1] == "claude-sonnet-5-5"
    assert argv[argv.index("--effort") + 1] == "medium"
    assert "ANTHROPIC_BASE_URL" not in sonnet["env"] and "ANTHROPIC_AUTH_TOKEN" not in sonnet["env"]
    prompt = prompt_of(sonnet)
    assert "you cannot run commands" in prompt
    assert "Attempt 1 (codex):" in prompt and "Attempt 2 (codex-repair):" in prompt
    assert "did not add a measured line" in prompt
    text = world.text()
    for line in (
        "attempt 1 · route codex",
        "attempt 2 · route codex-repair",
        "attempt 3 · route stage-1",
        "reason first Codex post-run check failed",
        "reason two Codex post-run checks failed",
    ):
        assert line in text, line
    assert "attempt 4" not in text
    assert len(world.calls("make")) == 3


def test_stage2_off_repairs_with_one_sonnet_attempt_and_records_the_reason(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Criterion 8. Planted fault: the key read on Stage 1, or the reason missing from one of the two places."""
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on Stage 1: {name}"))
    repair_world(world)
    world.script(claude=[repair_step()], codex=[{"stdout": "must not run"}], make=[{"stdout": "green\n"}])
    assert world.run("repair", "demo", "--stage2-off", "Z.ai unavailable") == 0
    calls = world.calls("claude")
    assert len(calls) == 1 and world.calls("codex") == []
    assert "you cannot run commands" in prompt_of(calls[0]) and stage2.REPAIR_FORMAT not in prompt_of(calls[0])
    argv, env = calls[0]["argv"], calls[0]["env"]
    assert argv[argv.index("--model") + 1] == "claude-sonnet-5-5"
    assert argv[argv.index("--effort") + 1] == "medium"
    assert "ANTHROPIC_BASE_URL" not in env and "ANTHROPIC_AUTH_TOKEN" not in env
    text = world.text()
    assert "route stage-1" in text and "reason Z.ai unavailable" in text
    plan = world.plan.read_text(encoding="utf-8")
    assert "Stage-1 route: repair · model claude-sonnet-5-5 · reason: Z.ai unavailable." in plan
    assert plan.index("## Runner route") < plan.index("## Time used")


# The four tests below keep the names the stage2-repair ledger cites; since ADR 0017 they pin the
# replacement of the route they once described, and each still fails on the fault it names.


def test_repair_routes_glm_5_3_then_its_repair_then_sonnet(world: World) -> None:
    """Stage2-repair criterion 7, replaced by ADR 0017. Planted fault: a GLM model anywhere in the routes."""
    repair_world(world)
    script_repair(
        world, [{"stdout": "still looking"}, {"stdout": "still stuck"}, repair_step()], make=[{"stdout": "green\n"}] * 3
    )
    assert world.run("repair") == 0
    calls = repair_calls(world)
    models = [call["argv"][call["argv"].index("-m" if call["name"] == "codex" else "--model") + 1] for call in calls]
    assert models == ["gpt-6.1-sol", "gpt-6.1-sol", "claude-sonnet-5-5"]
    assert not any("glm" in " ".join(call["argv"][:-1]) for call in calls if call["name"] == "codex")
    assert not any("glm" in " ".join(call["argv"]) for call in calls if call["name"] == "claude")
    assert "Attempt 1 (codex):" in prompt_of(calls[2]) and "Attempt 2 (codex-repair):" in prompt_of(calls[2])


def test_a_missing_glm_key_refuses_the_repair(world: World) -> None:
    """Stage2-repair criterion 9, replaced by ADR 0017. Planted fault: a repair that still needs the GLM key."""
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    repair_world(world)
    assert world.run("repair") == 0
    assert len(world.calls("codex")) == 1


def test_an_undeclared_glm_5_3_refuses_the_repair(world: World) -> None:
    """Stage2-repair criterion 10, replaced by ADR 0017. Planted fault: a repair that still checks `glm-5.3`."""
    repair_world(world)
    path = world.root / "model-endpoints.yaml"
    text = path.read_text(encoding="utf-8")
    line = "      - glm-5.3\n"
    assert line in text
    path.write_text(text.replace(line, "", 1), encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "drop glm-5.3")
    assert world.run("repair") == 0
    assert len(world.calls("codex")) == 1


def test_repair_has_file_tools_and_pins_glm_5_3(world: World) -> None:
    """Stage2-repair criterion 12, replaced by ADR 0017. Planted fault: `Bash` among the Sonnet attempt's tools."""
    repair_world(world)
    world.script(claude=[repair_step()], make=[{"stdout": "green\n"}])
    assert world.run("repair", "demo", "--stage2-off", "Codex unavailable") == 0
    call = world.calls("claude")[0]
    argv, env = call["argv"], call["env"]
    assert argv[argv.index("--model") + 1] == "claude-sonnet-5-5"
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"Read", "Grep", "Glob", "Edit", "Write"}
    assert "--restricted" in argv and "--safe-mode" in argv and "--strict-mcp-config" in argv
    assert "--add-dir" not in argv and call["cwd"] == str(world.root) and call["stdin"] == ""
    assert "ANTHROPIC_BASE_URL" not in env and "ANTHROPIC_AUTH_TOKEN" not in env


def test_repair_never_reads_the_glm_key(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 8. Planted fault: a secret read, a refusal for a missing key or a Z.ai variable in a call."""
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret in a repair: {name}"))
    repair_world(world)
    script_repair(
        world, [{"stdout": "still looking"}, {"stdout": "still stuck"}, repair_step()], make=[{"stdout": "green\n"}] * 3
    )
    assert world.run("repair") == 0
    calls = repair_calls(world)
    assert [call["name"] for call in calls] == ["codex", "codex", "claude"]
    for call in calls:
        env = call["env"]
        assert not any(name in env for name in ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN")), call["name"]
        assert all(value != KEY for value in env.values())


def test_a_leak_in_a_taken_row_stops_the_repair_without_fallback(world: World) -> None:
    """Criterion 10. Planted fault: the rows outside the scanned prompt, or a fallback after the BLOCK."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")], finding=f"leak {LEAK}")
    world.script(
        codex=[{"stdout": "must not run"}] * 3,
        claude=[{"stdout": "must not run"}] * 3,
        make=[{"stdout": "must not run"}],
    )
    assert world.run("repair") == 2
    assert world.calls() == []
    assert not world.findings.exists()


@pytest.mark.parametrize(("blocked", "calls_before"), [(2, 1), (3, 2)])
def test_repair_leak_blocks_each_route_without_fallback(
    world: World, monkeypatch: pytest.MonkeyPatch, blocked: int, calls_before: int
) -> None:
    """Criterion 10. Planted fault: a leak found at the second or third attempt reaches another call."""
    real = leakcheck.check
    prompts: list[str] = []

    def planted(change, denylist, root, items):
        if any("Repair baseline:" in text for _, text in items):
            prompts.append("repair")
            if len(prompts) == blocked:
                items = [*items, ("prompt", f"leak {LEAK}")]
        return real(change, denylist, root, items)

    monkeypatch.setattr(leakcheck, "check", planted)
    repair_world(world)
    script_repair(
        world,
        [{"stdout": "first"}, {"stdout": "second"}, repair_step(), {"stdout": "must not run"}],
        make=[{"stdout": "green\n"}] * 4,
    )
    assert world.run("repair") == 2
    assert len(repair_calls(world)) == calls_before


@pytest.mark.parametrize(
    ("missing", "options", "calls_before"),
    [
        ("gpt-6.1-sol", (), 0),
        ("claude-sonnet-5-5", ("--stage2-off", "r"), 0),
        ("claude-sonnet-5-5", (), 2),
    ],
)
def test_an_undeclared_repair_endpoint_refuses_before_call(
    world: World, missing: str, options: tuple[str, ...], calls_before: int
) -> None:
    """Criterion 9. Planted fault: no declaration check before a Codex or a Sonnet attempt."""
    repair_world(world)
    script_repair(world, [{"stdout": "first"}, {"stdout": "second"}, repair_step()], make=[{"stdout": "green\n"}] * 3)
    path = world.root / "model-endpoints.yaml"
    text = path.read_text(encoding="utf-8")
    line = f"      - {missing}\n"
    entry = text.index("  - name: claude-code-plan" if missing.startswith("claude") else "  - name: openai-codex")
    start = text.index(line, entry)
    path.write_text(text[:start] + text[start + len(line) :], encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "drop a declared model")
    assert world.run("repair", "demo", *options) == 2
    assert len(repair_calls(world)) == calls_before


def test_each_repair_attempt_leaves_an_audit_line_the_count_reads(world: World) -> None:
    """Criterion 11. Planted fault: the verb word `implement` in the line, or a line the count cannot read."""
    repair_world(world)
    script_repair(
        world, [{"stdout": "still looking"}, {"stdout": "still stuck"}, repair_step()], make=[{"stdout": "green\n"}] * 3
    )
    assert world.run("repair") == 0
    day = r"\d{4}-\d{2}-\d{2}"
    count = r"\d+ files, \d+ commits, \d+ rules"
    for attempt, route, endpoint, model, reason in (
        (1, "codex", "openai-codex", "gpt-6.1-sol", ""),
        (2, "codex-repair", "openai-codex", "gpt-6.1-sol", " · reason first Codex post-run check failed"),
        (3, "stage-1", "claude-code-plan", "claude-sonnet-5-5", " · reason two Codex post-run checks failed"),
    ):
        assert re.search(
            rf"^Stage-2 call, {day}: repair · attempt {attempt} · route {route} · endpoint {endpoint} · "
            rf"model {model}{reason} · leak check clean over {count}\.$",
            world.text(),
            re.M,
        ), attempt
    assert stage2_runs.measure(world.text()).calls == [("repair", True)] * 3


@pytest.mark.parametrize(("attempt", "earlier"), [(2, 1), (3, 1), (3, 2)])
@pytest.mark.parametrize("evidence", ["audit", "diagnostics", "files"])
def test_a_repair_retry_cannot_remove_earlier_attempt_evidence(
    world: World, monkeypatch: pytest.MonkeyPatch, attempt: int, earlier: int, evidence: str
) -> None:
    """Codex-repairs F-5: a valid retry deletes earlier evidence while keeping its own audit and rows."""
    baseline = repair_world(world)
    script_repair(
        world,
        [repair_step()] * 3,
        make=[
            {"stdout": f"DIAGNOSTIC-ATTEMPT-{number}\n", "exit": 1} if number < attempt else {"stdout": "green\n"}
            for number in range(1, 4)
        ],
    )
    protected: list[str] = []
    checkpoints: list[int] = []
    real_codex, real_claude, real_checkpoint = stage2.run_codex, stage2.run_work_model, stage2.checkpoint

    def remove_evidence() -> None:
        if len(repair_calls(world)) != attempt:
            return
        text = world.text()
        protected.append(text)
        audit = next(line for line in text.splitlines() if f"repair · attempt {earlier} ·" in line)
        start = text.index(audit)
        end = text.index("Stage-2 call,", start + len(audit))
        block = text[start:end]
        if evidence == "audit":
            removed = audit
        elif evidence == "diagnostics":
            removed = f"> DIAGNOSTIC-ATTEMPT-{earlier}"
        else:
            removed = next(line for line in block.splitlines() if line.startswith("> - `plans/changes/demo/plan.md`"))
        assert removed in block
        world.findings.write_text(text[:start] + block.replace(removed + "\n", "", 1) + text[end:], encoding="utf-8")

    def codex(*args, **kwargs):
        result = real_codex(*args, **kwargs)
        remove_evidence()
        return result

    def claude(*args, **kwargs):
        result = real_claude(*args, **kwargs)
        remove_evidence()
        return result

    def checkpoint(*args, **kwargs):
        checkpoints.append(len(repair_calls(world)))
        real_checkpoint(*args, **kwargs)

    monkeypatch.setattr(stage2, "run_codex", codex)
    monkeypatch.setattr(stage2, "run_work_model", claude)
    monkeypatch.setattr(stage2, "checkpoint", checkpoint)
    assert world.run("repair") == (0 if attempt == 2 else 1)
    assert checkpoints == ([3] if attempt == 2 else [])
    assert len(repair_calls(world)) == 3
    assert world.text().startswith(protected[0]), "the retry lost an earlier attempt's evidence"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == ("1" if attempt == 2 else "0")


@pytest.mark.parametrize(
    ("phase", "status"),
    [
        ("2a", "taken — already decided"),
        ("2a", "rejected — covered"),
        ("2a", "fixed — prior repair"),
        ("6", "rejected — covered"),
        ("released", "rejected — covered"),
    ],
)
def test_a_repair_cannot_change_a_finding_outside_its_batch(
    world: World, monkeypatch: pytest.MonkeyPatch, phase: str, status: str
) -> None:
    """Codex-repairs F-6: the model changes an unrelated finding's Status, including a phase-2a row."""
    repair_world(world)
    if phase == "released":
        row = released_cells("L1-2", status, "", "unrelated finding")
        block = released_block([row])
    else:
        row = phase6_cells("S-1", status, "unrelated finding")
        block = phase6_block([row]).replace("## Phase 6", f"## Phase {phase}", 1)
    world.write_findings(block)
    altered = [*row]
    altered[7] = "rejected — changed by repair" if status.startswith("fixed") else "fixed — tests/test_fix.py::test_fix"
    script_repair(world, [repair_step()] * 2, make=[{"stdout": "green\n"}] * 2)
    real_codex, real_checkpoint = stage2.run_codex, stage2.checkpoint
    checkpoints: list[int] = []

    def codex(*args, **kwargs):
        result = real_codex(*args, **kwargs)
        if len(world.calls("codex")) == 1:
            text = world.text()
            assert render_row(row) in text
            world.findings.write_text(text.replace(render_row(row), render_row(altered), 1), encoding="utf-8")
        return result

    def checkpoint(*args, **kwargs):
        checkpoints.append(len(repair_calls(world)))
        real_checkpoint(*args, **kwargs)

    monkeypatch.setattr(stage2, "run_codex", codex)
    monkeypatch.setattr(stage2, "checkpoint", checkpoint)
    assert world.run("repair") == 0
    assert checkpoints == [2], "an attempt that changed an unrelated finding reached the checkpoint"
    assert render_row(row) in world.text()
    assert render_row(altered) not in world.text()
    prompt = prompt_of(world.calls("codex")[0])
    assert f"- {row[0]} [" not in prompt, "the unrelated finding was put in the repair batch"


@pytest.mark.parametrize("attempt", [2, 3])
@pytest.mark.parametrize("removed_heading", [False, True])
def test_each_repair_retry_must_add_its_own_time_entry(
    world: World, monkeypatch: pytest.MonkeyPatch, attempt: int, removed_heading: bool
) -> None:
    """F-7/F-12: a retry still needs its own measurement after the failed plan edit is restored."""
    baseline = repair_world(world)
    steps = [repair_step()] * 3
    steps[attempt - 1] = repair_step(append={})
    script_repair(
        world,
        steps,
        make=[{"stdout": "red\n", "exit": 1}] * (attempt - 1) + [{"stdout": "green\n"}] * (4 - attempt),
    )
    real_codex, real_claude, real_checkpoint = stage2.run_codex, stage2.run_work_model, stage2.checkpoint
    checkpoints: list[int] = []

    def change_heading() -> None:
        if not removed_heading:
            return
        number = len(repair_calls(world))
        if number not in (attempt - 1, attempt):
            return
        before, after = ("## Time used", "## Omitted time heading")
        text = world.plan.read_text(encoding="utf-8")
        if number == attempt:
            # F-12 restores the failed edit before this retry; the model adds no measured line.
            assert before in text and after not in text
            return
        assert before in text
        world.plan.write_text(text.replace(before, after, 1), encoding="utf-8")

    def codex(*args, **kwargs):
        result = real_codex(*args, **kwargs)
        change_heading()
        return result

    def claude(*args, **kwargs):
        result = real_claude(*args, **kwargs)
        change_heading()
        return result

    def checkpoint(*args, **kwargs):
        checkpoints.append(len(repair_calls(world)))
        real_checkpoint(*args, **kwargs)

    monkeypatch.setattr(stage2, "run_codex", codex)
    monkeypatch.setattr(stage2, "run_work_model", claude)
    monkeypatch.setattr(stage2, "checkpoint", checkpoint)
    assert world.run("repair") == (0 if attempt == 2 else 1)
    assert checkpoints == ([3] if attempt == 2 else [])
    assert len(repair_calls(world)) == 3
    assert "did not add a measured line below `## Time used`" in world.text()
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == ("1" if attempt == 2 else "0")


def test_record_rows_reach_the_model_only_in_the_prompt(world: World) -> None:
    """Criterion 13. Planted fault: the rows written into a worktree file."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")], finding="LOOPMARK-9")
    script_repair(world, [repair_step()], marker="LOOPMARK-9", make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    call = world.calls("codex")[0]
    assert "LOOPMARK-9" in prompt_of(call)
    assert call["marker_paths"] == [], call["marker_paths"]
    assert "LOOPMARK-9" not in world.text()


def test_a_red_verify_or_a_missing_time_line_fails_a_repair_attempt(world: World) -> None:
    """Criterion 14. Planted fault: a checkpoint after a red `make verify`, or a failed attempt without its block."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    baseline = git(world.root, "rev-parse", "HEAD")
    red = "\n".join(_gate("pytest", ["FAILED tests/test_fix.py::test_fix - assert 2 == 1"], "red"))
    script_repair(
        world,
        [
            {"stdout": "attempt one", "plant": {"src/app.py": "value = 2\n", "tests/test_fix.py": FIX_TEST}},
            repair_step(),
        ],
        make=[{"stdout": red, "exit": 1}, {"stdout": "green\n"}],
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "Attempt 1 (codex):" in prompt
    assert "`make verify` exited 1" in prompt and "did not add a measured line" in prompt
    assert "attempt 2 · route codex-repair" in world.text()
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    assert len(quote_blocks(world.text())) == 1, "the failed attempt left no block"


@pytest.mark.parametrize(
    ("record", "first", "second", "problem"),
    [
        pytest.param(
            [("L1-1", "taken — test_a", "no"), ("L1-2", "taken — test_b", "no")],
            "L1-1: fixed — tests/test_fix.py::test_fix",
            "L1-1: fixed — tests/test_fix.py::test_fix\nL1-2: fixed — tests/test_fix.py::test_fix",
            "L1-2: no fixed line",
            id="missing",
        ),
        pytest.param(
            [("L1-1", "taken — test_a", "no")],
            "L1-1: fixed — tests/test_fix.py::test_fix\nL1-1: fixed — tests/test_fix.py::test_fix",
            "L1-1: fixed — tests/test_fix.py::test_fix",
            "L1-1: several fixed lines",
            id="doubled",
        ),
        pytest.param(
            [("L1-1", "taken — test_a", "no")],
            "L1-1: fixed — tests/test_fix.py::test_fix\nL9-9: fixed — not a test — nothing carries it",
            "L1-1: fixed — tests/test_fix.py::test_fix",
            "L9-9: no taken row carries this id",
            id="unknown",
        ),
    ],
)
def test_each_taken_row_needs_exactly_one_fixed_line(
    world: World, record: list, first: str, second: str, problem: str
) -> None:
    """Criterion 15. Planted fault: a missing, doubled or unknown fixed line accepted."""
    seed_tests(world)
    world.write_record(record)
    script_repair(world, [repair_step(stdout=first), repair_step(stdout=second)], make=[{"stdout": "green\n"}] * 2)
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "Attempt 1 (codex):" in prompt and problem in prompt, prompt


def test_a_code_row_answered_not_a_test_fails_the_attempt(world: World) -> None:
    """Criterion 16. Planted fault: `not a test` accepted for a code row."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(
        world,
        [repair_step(stdout="L1-1: fixed — not a test — the spec pins the behavior"), repair_step()],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "L1-1: answered `not a test`, but the row is a code row; it needs a test that was red first" in prompt


def test_a_reason_with_a_pipe_is_escaped_once_as_its_fixed_line_gives_it(world: World) -> None:
    """Repair round 2, L2-1. Planted fault: a pipe the fixed line already escaped is escaped again."""
    repair_world(world, ("L1-1", "taken — not a test — one", "no"), ("L1-2", "taken — not a test — two", "no"))
    answer = "L1-1: fixed — not a test — a pipe \\| inside the reason\nL1-2: fixed — not a test — a bare | pipe"
    script_repair(world, [repair_step(stdout=answer)], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    written = {row[0]: row[7] for row in stage2.record_rows(world.record().read_text(encoding="utf-8"))}
    assert written["L1-1"] == "fixed — not a test — a pipe \\| inside the reason", repr(written["L1-1"])
    assert written["L1-2"] == "fixed — not a test — a bare \\| pipe", repr(written["L1-2"])


def test_a_text_row_taken_as_not_a_test_is_repaired_and_its_status_written(world: World) -> None:
    """Repair round 2, L2-2. Planted fault: the write path of a text row's repair ran in no test."""
    repair_world(world, ("L1-1", "taken — not a test — no test can show it", "no"))
    world.write_findings(
        VERDICT, phase6_block([phase6_cells("F-1", "taken — not a test — the doctrine pins it", "a text finding")])
    )
    answer = "L1-1: fixed — not a test — the record row is written\nF-1: fixed — not a test — a pipe \\| in the reason"
    script_repair(world, [repair_step(stdout=answer)], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    record = {row[0]: row for row in stage2.record_rows(world.record().read_text(encoding="utf-8"))}
    assert record["L1-1"][7] == "fixed — not a test — the record row is written"
    assert record["L1-1"][8] == "no", "the runner wrote Broke a test"
    _, phase6 = stage2.findings_rows(world.text())
    assert {row[0]: row for row in phase6}["F-1"][7] == "fixed — not a test — a pipe \\| in the reason"
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert "fixed — not a test — a pipe \\| in the reason" in committed
    assert "taken — not a test — the doctrine pins it" not in committed
    assert git(world.root, "log", "-1", "--pretty=%s") == "fix(demo): repair taken findings L1-1, F-1"


def test_a_fixed_line_naming_an_undefined_test_fails_the_attempt(world: World) -> None:
    """Criterion 17. Planted fault: no definition check."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(
        world,
        [repair_step(stdout="L1-1: fixed — tests/test_absent.py::test_absent"), repair_step()],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "L1-1: tests/test_absent.py::test_absent defines no function `def test_absent(`" in prompt


def test_a_fixed_line_whose_test_path_climbs_out_of_tests_fails_the_attempt(world: World) -> None:
    """Repair round 1, L1-1. Planted fault: a `.` or `..` path segment in the fixed line's test accepted."""
    seed_tests(world)
    (world.root / "src" / "test_x.py").write_text(FIX_TEST, encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "a test outside tests/, red on the baseline")
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(
        world,
        [
            repair_step(
                stdout="L1-1: fixed — tests/../src/test_x.py::test_fix",
                plant={"src/app.py": "value = 2\n", "src/test_x.py": FIX_TEST},
            ),
            repair_step(),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "would climb out of `tests/`; a `.` or `..` path segment is no test path" in prompt, prompt


def test_a_named_test_that_is_not_red_first_fails_the_attempt(world: World) -> None:
    """Criterion 18. Planted fault: exit 0 on the baseline accepted as red first."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    green_on_baseline = (
        "from pathlib import Path\n\n\ndef test_not_red():\n"
        '    value = (Path(__file__).resolve().parent.parent / "src" / "app.py").read_text(encoding="utf-8")\n'
        '    assert "value = 1" in value\n'
    )
    script_repair(
        world,
        [
            repair_step(
                stdout="L1-1: fixed — tests/test_notred.py::test_not_red",
                plant={"src/app.py": "value = 2\n", "tests/test_notred.py": green_on_baseline},
            ),
            repair_step(),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert (
        "L1-1: tests/test_notred.py::test_not_red: pytest ended 0 on the baseline's code; red first is exit 1 or 2"
    ) in prompt


def test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt(world: World) -> None:
    """Phase 6, F-1. Planted fault: an interpreter whose pytest never starts, exit 1, read as red first."""
    repair_world(world)
    (world.root / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "ignore the venv")
    python = world.root / ".venv" / "bin" / "python3"
    python.parent.mkdir(parents=True)
    python.write_text("#!/bin/sh\necho 'No module named pytest' >&2\nexit 1\n", encoding="utf-8")
    python.chmod(0o755)
    head = git(world.root, "rev-parse", "HEAD")
    script_repair(world, [repair_step()] * 3, make=[{"stdout": "green\n"}] * 3)
    assert world.run("repair") == 1
    prompt = prompt_of(world.calls("codex")[1])
    assert "L1-1: tests/test_fix.py::test_fix: the red-first interpreter cannot start pytest (exit 1)" in prompt
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")
    assert git(world.root, "rev-parse", "HEAD") == head, "a checkpoint landed without the named test running"


def test_the_red_first_run_leaves_no_worktree_behind(world: World) -> None:
    """Criterion 19. Planted fault: the temporary worktree not removed."""
    repair_world(world)
    refs_before = {line.split()[-1] for line in git(world.root, "for-each-ref").splitlines()}
    assert world.run("repair") == 0
    listed = git(world.root, "worktree", "list").splitlines()
    assert len(listed) == 1, listed
    assert git(world.root, "status", "--porcelain") == ""
    assert {line.split()[-1] for line in git(world.root, "for-each-ref").splitlines()} == refs_before


def test_a_ref_created_while_the_named_test_ran_fails_the_proof_and_is_never_deleted(world: World) -> None:
    """Phase 6, F-6. Planted fault: the clean-up deleted a branch that appeared during the red-first run."""
    repair_world(world)
    branch_test = (
        "import subprocess\nfrom pathlib import Path\n\n\ndef test_branch():\n"
        '    subprocess.run(["git", "branch", "red-first-probe"], check=True)\n'
        '    value = (Path(__file__).resolve().parent.parent / "src" / "app.py").read_text(encoding="utf-8")\n'
        '    assert "value = 2" in value\n'
    )
    script_repair(
        world,
        [
            repair_step(
                stdout="L1-1: fixed — tests/test_branch.py::test_branch",
                plant={"src/app.py": "value = 2\n", "tests/test_branch.py": branch_test},
            ),
            repair_step(),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "refs changed while the named test ran: refs/heads/red-first-probe" in prompt, prompt
    assert "refs/heads/red-first-probe" in git(world.root, "for-each-ref"), "a neighbour's branch was deleted"
    assert len(git(world.root, "worktree", "list").splitlines()) == 1


def test_an_existing_ref_moved_while_the_named_test_ran_fails_the_proof(world: World) -> None:
    """Phase 6, F-7. Planted fault: the snapshot kept ref names only, so a moved branch passed as red first."""
    repair_world(world)
    git(world.root, "branch", "keep-me")
    git(world.root, "commit", "--quiet", "--allow-empty", "-m", "advance past keep-me")
    move_test = (
        "import subprocess\nfrom pathlib import Path\n\n\ndef test_move():\n"
        '    subprocess.run(["git", "branch", "-f", "keep-me", "HEAD"], check=True)\n'
        '    value = (Path(__file__).resolve().parent.parent / "src" / "app.py").read_text(encoding="utf-8")\n'
        '    assert "value = 2" in value\n'
    )
    script_repair(
        world,
        [
            repair_step(
                stdout="L1-1: fixed — tests/test_move.py::test_move",
                plant={"src/app.py": "value = 2\n", "tests/test_move.py": move_test},
            ),
            repair_step(),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "refs changed while the named test ran: refs/heads/keep-me" in prompt, prompt


def test_a_failed_worktree_remove_leaves_no_dead_entry_and_is_named(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Repair round 3, L3-4. Planted fault: a failed removal left a dead entry and went unnamed."""
    seed_tests(world)
    (world.root / "tests" / "test_fix.py").write_text(FIX_TEST, encoding="utf-8")
    baseline = git(world.root, "rev-parse", "HEAD")
    original_run = stage2.subprocess.run

    def refusing(command, *args, **kwargs):
        if "worktree" in command and "remove" in command:
            return subprocess.CompletedProcess(command, 128, stdout="", stderr="planted removal failure")
        return original_run(command, *args, **kwargs)

    monkeypatch.setattr(stage2.subprocess, "run", refusing)
    outcome = stage2.red_first(world.root, baseline, "tests/test_fix.py::test_fix", None)
    listed = git(world.root, "worktree", "list")
    assert "stage2-red-" not in listed, listed
    assert outcome is not None and "`git worktree remove` ended 128" in outcome, outcome


def test_a_failed_repair_process_restores_the_baseline_without_a_further_attempt(world: World) -> None:
    """Criterion 20. Planted fault: a fallback after a dead model process, or a path left in place."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    head = git(world.root, "rev-parse", "HEAD")
    script_repair(
        world,
        [
            {
                "stderr": "boom",
                "exit": 1,
                "plant": {"src/half.py": "x = 1\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-12 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "must not run"}],
    )
    assert world.run("repair") == 1
    assert len(repair_calls(world)) == 1 and world.calls("make") == []
    assert not (world.root / "src/half.py").exists()
    assert git(world.root, "rev-parse", "HEAD") == head
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")
    assert "Stage-2 call" in world.text(), "the audit line stays in findings.md"


@pytest.mark.parametrize(
    "broken",
    [
        pytest.param(
            {"stdout": '{"type": "turn.completed"}\n', "answer": "L1-1: fixed — not a test — x"}, id="no-thread"
        ),
        pytest.param({"stdout": '{"type": "thread.started", "thread_id": "T9"}\n'}, id="no-answer-file"),
        pytest.param(codex_ok("T9", "  \n"), id="empty-answer"),
    ],
)
def test_codex_repair_transport_failures_stop_the_chain(world: World, broken: dict) -> None:
    """Criterion 6. Planted fault: a missing thread event, answer file or answer reaches the retry or Sonnet."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    head = git(world.root, "rev-parse", "HEAD")
    world.script(
        codex=[{**broken, "plant": {"src/half.py": "x = 1\n"}}, codex_ok("T9", "must not run")],
        claude=[{"stdout": "must not run"}],
        make=[{"stdout": "must not run"}],
    )
    assert world.run("repair") == 1
    assert [call["name"] for call in repair_calls(world)] == ["codex"]
    assert world.calls("make") == []
    assert not (world.root / "src/half.py").exists()
    assert git(world.root, "rev-parse", "HEAD") == head
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")


def test_a_missing_codex_executable_stops_the_repair(world: World) -> None:
    """Criterion 6. Planted fault: a Codex that cannot start advances to the retry or Sonnet."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    (world.bin / "codex").unlink()
    world.script(claude=[{"stdout": "must not run"}], make=[{"stdout": "must not run"}])
    assert world.run("repair") == 1
    assert world.calls() == []


def test_codex_repair_that_moves_head_stops_without_rewriting(world: World) -> None:
    """Criterion 17. Planted fault: a reset, a verify, a retry or a runner commit after the model moved HEAD."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(codex=[codex_ok("T9", "L1-1: fixed — tests/test_fix.py::test_fix")], make=[{"stdout": "must not run"}])
    # a Codex call that commits: the stand-in cannot, so the commit lands through the CLI's launch
    real_launch = stage2.launch
    moved: list[str] = []

    def committing(command, cwd, env, *args, **kwargs):
        done = real_launch(command, cwd, env, *args, **kwargs)
        if command[0] == "codex":
            (Path(cwd) / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
            git(Path(cwd), "add", "-A")
            git(Path(cwd), "commit", "--quiet", "-m", "the model committed")
            moved.append(git(Path(cwd), "rev-parse", "HEAD"))
        return done

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(stage2, "launch", committing)
        assert world.run("repair") == 1
    assert len(moved) == 1 and git(world.root, "rev-parse", "HEAD") == moved[0], "HEAD was rewritten or advanced"
    assert (world.root / "src" / "app.py").read_text(encoding="utf-8") == "value = 2\n", "the commit was reset"
    assert len(repair_calls(world)) == 1 and world.calls("make") == []
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")


def test_a_failed_codex_repair_call_that_moves_head_stops_without_rewriting(world: World) -> None:
    """Criterion 17. Planted fault: a dead call that also moved HEAD is restored, which rewrites its commit."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(codex=[{"stderr": "boom", "exit": 1}], claude=[{"stdout": "must not run"}])
    real_launch = stage2.launch
    moved: list[str] = []

    def committing(command, cwd, env, *args, **kwargs):
        done = real_launch(command, cwd, env, *args, **kwargs)
        if command[0] == "codex":
            git(Path(cwd), "commit", "--quiet", "--allow-empty", "-m", "the model committed")
            moved.append(git(Path(cwd), "rev-parse", "HEAD"))
        return done

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(stage2, "launch", committing)
        assert world.run("repair") == 1
    assert git(world.root, "rev-parse", "HEAD") == moved[0]
    assert len(repair_calls(world)) == 1 and world.calls("make") == []


@pytest.mark.parametrize("call_failed", [False, True], ids=["completed-call", "failed-call"])
def test_a_codex_repair_that_commits_findings_restores_statuses_and_records_diagnostics(
    world: World, monkeypatch: pytest.MonkeyPatch, call_failed: bool
) -> None:
    """L2-3/L3-3: restore statuses and report a moved-HEAD stop without claiming post-run checks ran."""
    repair_world(world)
    world.write_findings(VERDICT, phase6_block([phase6_cells("F-1", "taken — crit 18", "phase finding")]))
    vandal = (
        VERDICT + "\n\n" + phase6_block([phase6_cells("F-1", "fixed — tests/test_fix.py::test_fix", "phase finding")])
    )
    plant = {"src/app.py": "value = 2\n", "plans/changes/demo/findings.md": vandal}
    step = (
        {"stderr": "boom after writing", "exit": 1, "plant": plant}
        if call_failed
        else codex_ok("T9", "F-1: fixed — tests/test_fix.py::test_fix", plant=plant)
    )
    world.script(
        codex=[step, {"stdout": "must not run"}],
        claude=[{"stdout": "must not run"}],
        make=[{"stdout": "must not run"}],
    )
    real_launch = stage2.launch
    moved: list[str] = []

    def committing(command, cwd, env, *args, **kwargs):
        done = real_launch(command, cwd, env, *args, **kwargs)
        if command[0] == "codex":
            git(Path(cwd), "add", "-A")
            git(Path(cwd), "commit", "--quiet", "-m", "the model committed its own statuses")
            moved.append(git(Path(cwd), "rev-parse", "HEAD"))
        return done

    def unexpected_check(*_args, **_kwargs):
        pytest.fail("a moved-HEAD stop must precede every post-run check")

    monkeypatch.setattr(stage2, "launch", committing)
    monkeypatch.setattr(stage2, "verify_attempt", unexpected_check)
    monkeypatch.setattr(stage2, "check_repair_answer", unexpected_check)
    assert world.run("repair") == 1
    assert len(moved) == 1 and git(world.root, "rev-parse", "HEAD") == moved[0]
    assert (world.root / "src" / "app.py").read_text(encoding="utf-8") == "value = 2\n"
    (call,) = repair_calls(world)
    assert call["name"] == "codex" and world.calls("make") == []
    text = world.text()
    assert text.startswith(call["findings"]), "the original statuses and this attempt's audit must be restored"
    _, phase6 = stage2.findings_rows(text)
    assert {row[0]: row for row in phase6}["F-1"][7] == "taken — crit 18"
    assert "fixed — tests/test_fix.py::test_fix" not in text
    (block,) = quote_blocks(text)
    assert block[0] == "Attempt 1 (codex) stopped because the call moved HEAD; no post-run check ran."
    assert "failed its post-run checks" not in "\n".join(block)
    assert any("moved HEAD from" in line for line in block)
    changed = "\n".join(files_of(block))
    assert "`plans/changes/demo/findings.md`" in changed and "`src/app.py`" in changed
    if call_failed:
        assert any("codex call failed: exit 1" in line for line in block)
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")


def test_a_failed_repair_process_removes_the_ignored_paths_it_created(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    """Phase 6, F-5. Planted fault: an ignored file the failed attempt created stayed behind."""
    repair_world(world)
    (world.root / ".gitignore").write_text("lychee/\n", encoding="utf-8")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "ignore lychee")
    script_repair(
        world,
        [
            {
                "stderr": "boom",
                "exit": 1,
                "plant": {"lychee/repair.txt": "left behind\n", "src/half.py": "x = 1\n"},
            },
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "must not run"}],
    )
    assert world.run("repair") == 1
    assert not (world.root / "lychee" / "repair.txt").exists()
    assert not (world.root / "lychee").exists()
    err = capsys.readouterr().err
    assert "ignored paths removed: lychee/repair.txt" in err, err
    assert "undone: src/half.py" in err


def test_a_passing_repair_writes_fixed_into_each_rows_place_and_nothing_else(world: World) -> None:
    """Criterion 21. Planted fault: `Broke a test` written, or a rejected row changed."""
    repair_world(
        world,
        ("L1-1", "taken — test_a", "no"),
        ("L1-2", "rejected — out of scope", ""),
    )
    released_before = released_block(
        [
            released_cells("L1-3", "taken — test_c", "no", "released finding"),
            released_cells("L1-4", "rejected — no evidence", "", "released rejection"),
        ]
    )
    phase6_before = phase6_block(
        [
            phase6_cells("F-1", "taken — crit 6", "phase finding"),
            phase6_cells("F-2", "rejected — covered", "phase rejection"),
        ]
    )
    world.write_findings(VERDICT, released_before, phase6_before)
    answer = "\n".join(
        [
            "L1-1: fixed — tests/test_fix.py::test_fix",
            "L1-3: fixed — tests/test_fix.py::test_fix",
            "F-1: fixed — tests/test_fix.py::test_fix",
        ]
    )
    script_repair(world, [repair_step(stdout=answer)], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    record = {row[0]: row for row in stage2.record_rows(world.record().read_text(encoding="utf-8"))}
    assert record["L1-1"][7] == "fixed — tests/test_fix.py::test_fix"
    assert record["L1-1"][8] == "no", "the runner wrote Broke a test"
    assert record["L1-1"][:7] == [
        "L1-1",
        "MAJOR",
        "MAINT",
        "impl",
        "src/app.py:1",
        "finding of L1-1",
        "deepseek-v4.1-flash",
    ]
    assert record["L1-2"][7] == "rejected — out of scope"
    released_now, phase6_now = stage2.findings_rows(world.text())
    rows = {row[0]: row for row in [*released_now, *phase6_now]}
    for ident in ("L1-3", "F-1"):
        assert rows[ident][7] == "fixed — tests/test_fix.py::test_fix", ident
    assert rows["L1-3"][9] == "—" and rows["L1-3"][5] == "released finding"
    assert rows["F-1"][6] == "Codex" and rows["F-1"][5] == "phase finding"
    assert rows["L1-4"][7] == "rejected — no evidence" and rows["F-2"][7] == "rejected — covered"
    lines = world.text().splitlines()
    for untouched in (
        render_row(released_cells("L1-4", "rejected — no evidence", "", "released rejection")),
        render_row(phase6_cells("F-2", "rejected — covered", "phase rejection")),
    ):
        assert untouched in lines, untouched


def test_an_edit_outside_the_taken_rows_fails_the_attempt_and_never_reaches_a_commit(world: World) -> None:
    """Phase 6, F-3. Planted fault: an overwritten rejected row passed the check into the checkpoint."""
    repair_world(world, ("L1-1", "rejected — out of scope", ""))
    world.write_findings(
        VERDICT,
        phase6_block(
            [
                phase6_cells("F-1", "taken — crit 21", "phase finding"),
                phase6_cells("F-2", "rejected — covered elsewhere", "phase rejection"),
            ]
        ),
    )
    vandal = (
        "# Findings — demo\n\n"
        + VERDICT
        + "\n\n"
        + phase6_block(
            [
                phase6_cells("F-1", "taken — crit 21", "phase finding"),
                phase6_cells("F-2", "rejected — silenced by the model", "phase rejection overwritten"),
            ]
        )
        + "\n"
    )
    script_repair(
        world,
        [
            repair_step(
                stdout="F-1: fixed — tests/test_fix.py::test_fix",
                plant={
                    "src/app.py": "value = 2\n",
                    "tests/test_fix.py": FIX_TEST,
                    "plans/changes/demo/findings.md": vandal,
                },
            ),
            repair_step(stdout="F-1: fixed — tests/test_fix.py::test_fix"),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "F-2: the phase-6 row no longer stands in findings.md as it stood before the repair" in prompt
    _, phase6 = stage2.findings_rows(world.text())
    rows = {row[0]: row for row in phase6}
    assert rows["F-2"][5] == "phase rejection" and rows["F-2"][7] == "rejected — covered elsewhere"
    assert rows["F-1"][7] == "fixed — tests/test_fix.py::test_fix"
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert "silenced by the model" not in committed and "rejected — covered elsewhere" in committed


def test_a_passing_repair_ends_in_one_checkpoint_commit_with_its_statuses(world: World) -> None:
    """Criterion 22. Planted fault: implement's message, or the statuses outside the commit."""
    repair_world(
        world,
        ("L1-1", "taken — test_a", "no"),
        ("L1-2", "rejected — out of scope", ""),
    )
    world.write_findings(
        VERDICT,
        released_block([released_cells("L1-3", "taken — test_c", "no", "released finding")]),
        phase6_block([phase6_cells("F-1", "taken — crit 6", "phase finding")]),
    )
    answer = "\n".join(
        [
            "L1-1: fixed — tests/test_fix.py::test_fix",
            "L1-3: fixed — tests/test_fix.py::test_fix",
            "F-1: fixed — tests/test_fix.py::test_fix",
        ]
    )
    baseline = git(world.root, "rev-parse", "HEAD")
    script_repair(world, [repair_step(stdout=answer)], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "1"
    assert git(world.root, "log", "-1", "--pretty=%s") == "fix(demo): repair taken findings L1-1, L1-3, F-1"
    assert git(world.root, "status", "--porcelain") == ""
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert committed.count("fixed — tests/test_fix.py::test_fix") == 2
    assert "taken — test_c" not in committed


def test_a_failed_repair_writes_no_fixed_status(world: World) -> None:
    """Criterion 23. Planted fault: statuses written before the checks pass."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(world, [{"stdout": "working"}] * 3, make=[{"stdout": "green\n"}] * 3)
    assert world.run("repair") == 1
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")
    assert "fixed — " not in world.text()
    assert [block[0] for block in quote_blocks(world.text())] == [
        "Attempt 1 (codex) failed its post-run checks.",
        "Attempt 2 (codex-repair) failed its post-run checks.",
        "Attempt 3 (stage-1) failed its post-run checks.",
    ]


def test_a_failed_repair_puts_every_status_back_as_it_stood(world: World) -> None:
    """Phase 6, F-2. Planted fault: a model-written `fixed` survived the failed attempts."""
    repair_world(world)
    world.write_findings(VERDICT, phase6_block([phase6_cells("F-1", "taken — crit 18", "phase finding")]))
    vandal = (
        "# Findings — demo\n\n"
        + VERDICT
        + "\n\n"
        + phase6_block([phase6_cells("F-1", "fixed — tests/test_fix.py::test_fix", "phase finding")])
        + "\n"
    )

    def vandal_step() -> dict:
        return {
            "stdout": "working on it",
            "plant": {
                "src/app.py": "value = 2\n",
                "tests/test_fix.py": FIX_TEST,
                "plans/changes/demo/findings.md": vandal,
            },
            "append": {"plans/changes/demo/plan.md": "2026-10-12 10:00–10:05, 5 min\n"},
        }

    script_repair(world, [vandal_step()] * 3, make=[{"stdout": "green\n"}] * 3)
    assert world.run("repair") == 1
    _, phase6 = stage2.findings_rows(world.text())
    assert {row[0]: row for row in phase6}["F-1"][7] == "taken — crit 18"
    assert "fixed — tests/test_fix.py::test_fix" not in world.text()
    assert "taken — test_a" in world.record().read_text(encoding="utf-8")


def test_a_credential_refusal_puts_the_original_statuses_back(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """Phase 6, F-8, kept for the Codex route. Planted fault: the block left the model-written `fixed` Status."""
    real = leakcheck.check
    seen: list[str] = []

    def planted(change, denylist, root, items):
        if any("Repair baseline:" in text for _, text in items):
            seen.append("repair")
            if len(seen) == 2:
                items = [*items, ("prompt", f"leak {LEAK}")]
        return real(change, denylist, root, items)

    monkeypatch.setattr(leakcheck, "check", planted)
    repair_world(world)
    world.write_findings(VERDICT, phase6_block([phase6_cells("F-1", "taken — crit 18", "phase finding")]))
    vandal = (
        "# Findings — demo\n\n"
        + VERDICT
        + "\n\n"
        + phase6_block([phase6_cells("F-1", "fixed — tests/test_fix.py::test_fix", "phase finding")])
        + "\n"
    )
    script_repair(
        world,
        [
            repair_step(
                stdout="working on it",
                plant={"src/app.py": "value = 2\n", "plans/changes/demo/findings.md": vandal},
            ),
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("repair") == 2
    assert len(repair_calls(world)) == 1
    _, phase6 = stage2.findings_rows(world.text())
    assert {row[0]: row for row in phase6}["F-1"][7] == "taken — crit 18"
    assert "fixed — tests/test_fix.py::test_fix" not in world.text()


def test_an_added_copy_of_a_rejected_row_fails_the_attempt(world: World) -> None:
    """Phase 6, F-9. Planted fault: row preservation by membership let an identical extra copy through."""
    repair_world(world)
    both_lines = "L1-1: fixed — tests/test_fix.py::test_fix\nF-1: fixed — tests/test_fix.py::test_fix"
    rows_ = [
        phase6_cells("F-1", "taken — crit 21", "phase finding"),
        phase6_cells("F-2", "rejected — covered elsewhere", "phase rejection"),
    ]
    world.write_findings(VERDICT, phase6_block(rows_))
    vandal = (
        "# Findings — demo\n\n"
        + VERDICT
        + "\n\n"
        + phase6_block([*rows_, phase6_cells("F-2", "rejected — covered elsewhere", "phase rejection")])
        + "\n"
    )
    script_repair(
        world,
        [
            repair_step(
                stdout=both_lines,
                plant={
                    "src/app.py": "value = 2\n",
                    "tests/test_fix.py": FIX_TEST,
                    "plans/changes/demo/findings.md": vandal,
                },
            ),
            repair_step(stdout=both_lines),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "F-2: findings.md holds a phase-6 row that stood nowhere before the repair" in prompt, prompt
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert committed.count("phase rejection") == 1


def test_a_removed_audit_line_fails_the_attempt(world: World) -> None:
    """Phase 6, F-11. Planted fault: a model that dropped this call's audit line was accepted and checkpointed."""
    repair_world(world)
    both_lines = "L1-1: fixed — tests/test_fix.py::test_fix\nF-1: fixed — tests/test_fix.py::test_fix"
    rows_ = [phase6_cells("F-1", "taken — crit 21", "phase finding")]
    world.write_findings(VERDICT, phase6_block(rows_))
    vandal = "# Findings — demo\n\n" + VERDICT + "\n\n" + phase6_block(rows_) + "\n"
    script_repair(
        world,
        [
            repair_step(
                stdout=both_lines,
                plant={
                    "src/app.py": "value = 2\n",
                    "tests/test_fix.py": FIX_TEST,
                    "plans/changes/demo/findings.md": vandal,
                },
            ),
            repair_step(stdout=both_lines),
        ],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = prompt_of(world.calls("codex")[1])
    assert "findings.md no longer holds the audit line of this call" in prompt, prompt
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert committed.count("Stage-2 call,") == 2, committed


def test_the_record_is_marked_only_after_the_checkpoint_commit(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 23. Planted fault: the record written before the commit exists."""
    seed_tests(world)
    world.write_record([("L1-1", "taken — test_a", "no")])
    baseline = git(world.root, "rev-parse", "HEAD")
    seen = []
    real = stage2.mark_repaired_findings

    def spy_findings(ctx: stage2.Context, taken: list, fixes: dict) -> None:
        seen.append(("findings", git(world.root, "rev-list", "--count", f"{baseline}..HEAD")))
        real(ctx, taken, fixes)

    def spy_record(_change: str, _taken: list, _fixes: dict) -> None:
        seen.append(("record", git(world.root, "rev-list", "--count", f"{baseline}..HEAD")))

    monkeypatch.setattr(stage2, "mark_repaired_findings", spy_findings)
    monkeypatch.setattr(stage2, "mark_repaired_record", spy_record)
    script_repair(world, [repair_step()], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    assert seen == [("findings", "0"), ("record", "1")]
    assert "taken — test_a" in world.record().read_text(encoding="utf-8"), "the spy must not write the record"


def test_a_repair_keeps_the_final_newline_of_findings_and_the_record(world: World) -> None:
    """Repair round 2, L2-3. Planted fault: the rewrites join split lines and drop each file's final newline."""
    repair_world(world, ("L1-1", "taken — not a test — no test can show it", "no"))
    script_repair(
        world, [repair_step(stdout="L1-1: fixed — not a test — the doctrine names it")], make=[{"stdout": "green\n"}]
    )
    assert world.run("repair") == 0
    assert world.text().endswith("\n"), "findings.md lost its final newline"
    assert world.record().read_text(encoding="utf-8").endswith("\n"), "the loop record lost its final newline"


def test_repair_starts_no_review_call(world: World) -> None:
    """Criterion 24. Planted fault: the verb calls `review-loop` or `review`."""
    repair_world(world)
    script_repair(world, [repair_step()], make=[{"stdout": "green\n"}], pi=[{"stdout": "must not run"}])
    assert world.run("repair") == 0
    # the one Codex call is the repair itself: writable, with no verdict and no loop-mark prompt
    (call,) = world.calls("codex")
    assert 'sandbox_mode="workspace-write"' in call["argv"] and "resume" not in call["argv"]
    assert "Write only your verdict now." not in prompt_of(call)
    assert world.calls("pi") == []
    assert "Phase 6" not in world.text() and "Broke a test" not in world.text()


def test_a_fixed_loop_row_is_decided_only_with_its_broke_a_test_mark(world: World) -> None:
    """Criterion 25. Planted fault: `undecided` reads only `taken` and `rejected`."""
    fixed = "fixed — tests/test_seed.py::test_seed"
    row = ["L1-1", "MAJOR", "MAINT", "impl", "src/app.py:1", "f", "deepseek-v4.1-flash", fixed, ""]
    assert stage2.undecided([row]) == ["L1-1"]
    assert stage2.undecided([[*row[:8], "no"]]) == []
    world.write_record([("L1-1", fixed, "")])
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 2 and world.run("review-loop") == 2
    record = world.record().read_text(encoding="utf-8")
    world.record().write_text(record.replace(f"| {fixed} |  |", f"| {fixed} | no |"), encoding="utf-8")
    assert world.run("release-loop") == 0


def test_a_fixed_row_without_its_mark_is_refused_with_the_missing_mark_named(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    """Repair round 2, L2-6. Planted fault: a fixed row without its mark is told to be decided, not marked."""
    fixed = "fixed — tests/test_seed.py::test_seed"
    seed_tests(world)
    world.write_record([("L1-1", fixed, ""), ("L1-2", "taken — test_b", "")])
    world.write_findings(VERDICT)
    for verb in ("review", "review-loop", "release-loop"):
        assert world.run(verb) == 2
        error = capsys.readouterr().err
        assert "undecided rows (L1-2)" in error, error
        assert "fixed rows without their `Broke a test` mark (L1-1)" in error, error
        assert "repair run's evidence" in error, error
    world.write_record([("L1-1", fixed, "")])
    for verb in ("review", "review-loop", "release-loop"):
        assert world.run(verb) == 2
        error = capsys.readouterr().err
        assert "decide them first" not in error, error
        assert "fixed rows without their `Broke a test` mark (L1-1)" in error, error


def test_round_three_starts_after_a_fixed_round_two_row(world: World) -> None:
    """Criterion 26. Planted fault: `taken_in_round` reads only `taken`."""
    row = [
        "L2-1",
        "MAJOR",
        "MAINT",
        "impl",
        "src/app.py:1",
        "f",
        "mimo-v2.6-flash",
        "fixed — tests/test_seed.py::test_seed",
        "no",
    ]
    assert stage2.taken_in_round([row], 2)
    assert not stage2.taken_in_round([[*row[:7], "rejected — r", ""]], 2)
    world.script(pi=[{"stdout": rows(1)}] * 3)
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — out of scope")
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — out of scope")
    record = world.record().read_text(encoding="utf-8")
    world.record().write_text(
        re.sub(
            r"^(\| L2-1 \|.*\|) rejected — out of scope \| no \|$",
            r"\1 fixed — tests/test_seed.py::test_seed | no |",
            record,
            flags=re.M,
        ),
        encoding="utf-8",
    )
    assert world.run("review-loop") == 0
    assert [rung_of(call) for call in world.calls("pi")] == [
        "deepseek-v4.1-flash",
        "mimo-v2.6-flash",
        "mimo-v2.6-pro",
    ]


def test_stage2_off_is_accepted_for_repair(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 28. Planted fault: the flag refused for repair."""
    monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on Stage 1: {name}"))
    repair_world(world)
    world.script(claude=[repair_step()], make=[{"stdout": "green\n"}])
    assert world.run("repair", "demo", "--stage2-off", "Z.ai unavailable") == 0
    calls = world.calls("claude")
    assert len(calls) == 1
    argv = calls[0]["argv"]
    assert argv[argv.index("--model") + 1] == "claude-sonnet-5-5"


# ---------------------------------------------------------------------------
# The ask rule on `codex` (criterion 61)
# ---------------------------------------------------------------------------


def test_settings_ask_before_codex() -> None:
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    assert stage2.codex_rule_problems(settings) == []
    assert stage2.CODEX_ASK_RULE[0] in settings["permissions"]["ask"]


def test_a_missing_or_covered_codex_rule_is_caught() -> None:
    base = json.loads(SETTINGS.read_text(encoding="utf-8"))
    dropped = copy.deepcopy(base)
    dropped["permissions"]["ask"].remove(stage2.CODEX_ASK_RULE[0])
    assert any("lacks the ask rule" in p for p in stage2.codex_rule_problems(dropped))
    for kind, rule in (
        ("allow", "Bash(codex *)"),
        ("allow", "Bash(codex exec:*)"),
        ("deny", "Bash"),
        ("allow", "Bash(*)"),
    ):
        planted = copy.deepcopy(base)
        planted["permissions"].setdefault(kind, []).append(rule)
        assert any(f"the {kind} rule {rule}" in p for p in stage2.codex_rule_problems(planted)), (kind, rule)
    beside = copy.deepcopy(base)
    beside["permissions"].setdefault("allow", []).append("Bash(git status)")
    assert stage2.codex_rule_problems(beside) == []


def test_the_omnigent_render_keeps_the_codex_rule(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "settings.json"
    target.parent.mkdir(parents=True)
    target.write_text(SETTINGS.read_text(encoding="utf-8"), encoding="utf-8")
    omnigent_policy.write(tmp_path)
    rendered = json.loads(target.read_text(encoding="utf-8"))
    assert stage2.CODEX_ASK_RULE[0] in rendered["permissions"]["ask"]
    assert stage2.codex_rule_problems(rendered) == []
    assert omnigent_policy.check(tmp_path) == []


# ---------------------------------------------------------------------------
# The doctrine and the prompts (criteria 42-60, 66-68)
# ---------------------------------------------------------------------------

WORKFLOW = REPO_ROOT / "docs" / "WORKFLOW.md"
PROMPTS = REPO_ROOT / "prompts"
TARGET = REPO_ROOT / "docs" / "architecture" / "2026-09-17-omnigent-first-target.md"
PLAN_DOC = REPO_ROOT / "docs" / "architecture" / "2026-09-17-implementation-plan.md"
ADR_0007 = "0007-stage-2-reviews-by-codex-and-glm.md"


def flat(text: str) -> str:
    """One line: a sentence broken across lines in the source, or across quoted lines, reads as one."""
    return re.sub(r"\s+", " ", re.sub(r"\n[> ]*", " ", text))


def section(text: str, title: str) -> str:
    """The lines from the heading that starts with `title` to the next heading of its level or a higher one."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(title)]
    if not starts:
        return ""
    level = len(title) - len(title.lstrip("#"))
    follow = re.compile(rf"^#{{1,{level}}} ")
    end = next((i for i in range(starts[0] + 1, len(lines)) if follow.match(lines[i])), len(lines))
    return "\n".join(lines[starts[0] : end])


def routing_rows(text: str) -> dict[str, tuple[str, str]]:
    """Phase cell -> (model, why) for every routing row `| 2a Spec review | **model** | why |`."""
    pattern = r"^\| (\d[a-z]? [A-Za-z][A-Za-z ]*?) \| \*\*([^*]+)\*\* \| (.*) \|$"
    return {m[1]: (m[2], m[3]) for m in re.finditer(pattern, text, re.M)}


STAGE2_ROUTING = {
    "1 Explore": "GLM 5.3 Flash",
    "2 Spec": "gpt-6.1-sol",
    "2b Design": "gpt-6.1-sol",
    "2a Spec review": "Opus 5.5",
    "3 Plan": "gpt-6.1-sol",
    "4 Implement": "GLM 5.3 Flash",
    "4b Review loop": "the ladder",
    "6 Review": "gpt-6.1-sol",
}

# Sol's effort lives once per verb in `CODEX_EFFORTS`; every active instruction links its verb's
# entry instead of naming a value of its own (bead coding-harness-yzk, spec criteria 4-6).
SOL_ROUTING_VERBS = {"2 Spec": "draft", "2b Design": "draft", "3 Plan": "draft", "6 Review": "review"}
SOL_EFFORT_PROMPTS = ("02-spec.md", "02b-design.md", "03-plan.md", "06-review.md")
REPAIR_ROW_LABEL = "| Repair after 4b and 6 |"
EFFORT_LITERAL = re.compile(r"effort `[^`]+`")
OTHER_MODEL = re.compile(r"Opus|Sonnet|GLM|`?glm-5|the ladder|Haiku")


def effort_reference(verb: str) -> str:
    """The link form through which an instruction names one verb's entry of `CODEX_EFFORTS`."""
    return f'[`CODEX_EFFORTS["{verb}"]`](../scripts/stage2.py)'


def sol_clause(text: str) -> str:
    """From Sol's model id to the next model's mention, so another model's effort stays outside (Q-5)."""
    start = text.find("gpt-6.1-sol")
    rest = text[start + len("gpt-6.1-sol") :] if start >= 0 else text
    stop = OTHER_MODEL.search(rest)
    return rest[: stop.start()] if stop else rest


def sol_effort_clause_problems(clause: str, verb: str, where: str) -> list[str]:
    """One Sol clause must reference its verb's central entry and name no independent effort value."""
    found = []
    if (literal := EFFORT_LITERAL.search(clause)) is not None:
        found.append(f"{where} sets Sol's effort independently ({literal.group(0)})")
    if effort_reference(verb) not in clause:
        found.append(f"{where} does not reference {effort_reference(verb)}")
    return found


def sol_prompt_texts() -> dict[str, str]:
    return {name: (PROMPTS / name).read_text(encoding="utf-8") for name in SOL_EFFORT_PROMPTS}


def sol_texts(doc: str, text: str) -> tuple[str, dict[str, str]]:
    """The doctrine and prompt texts with one document replaced, for planting a fault in it."""
    if doc == "workflow":
        return text, sol_prompt_texts()
    return WORKFLOW.read_text(encoding="utf-8"), {**sol_prompt_texts(), doc: text}


def sol_effort_problems(workflow: str, prompts: dict[str, str]) -> list[str]:
    """Every active Sol effort clause references its verb's entry of `CODEX_EFFORTS` (spec, criteria 4-6)."""
    found = []
    rows_3 = routing_rows(section(workflow, "## 3 · "))
    for phase, verb in SOL_ROUTING_VERBS.items():
        row = routing_rows(section(workflow, "## 4 · ")).get(phase)
        if row is None:
            found.append(f"section 4 has no routing row {phase}")
        else:
            found += sol_effort_clause_problems(sol_clause(row[1]), verb, f"section 4 routes {phase}")
    for phase in ("2 Spec", "2b Design", "3 Plan"):  # §3 routes these to Opus and defers review's Sol clause to §4
        stage_1 = rows_3.get(phase)
        if stage_1 is None:
            found.append(f"section 3 has no routing row {phase}")
        else:
            found += sol_effort_clause_problems(sol_clause(stage_1[1]), "draft", f"section 3 routes {phase}")
    line = next((row for row in section(workflow, "## 4 · ").splitlines() if row.startswith(REPAIR_ROW_LABEL)), "")
    cells = stage2.split_row(line) or []
    if len(cells) != 3 or cells[1] != "**gpt-6.1-sol**":
        found.append("section 4 has no repair row for gpt-6.1-sol")
    else:
        found += sol_effort_clause_problems(sol_clause(cells[2]), "repair", "section 4 routes the repair")
    draft = section(workflow, "### The draft (phases 2, 2b and 3)")
    prose = flat(draft.partition("A drafted change runs in this order:")[0])
    found += sol_effort_clause_problems(sol_clause(prose), "draft", "the draft prose")
    for name, verb in (
        ("02-spec.md", "draft"),
        ("02b-design.md", "draft"),
        ("03-plan.md", "draft"),
        ("06-review.md", "review"),
    ):
        found += sol_effort_clause_problems(sol_clause(model_line(prompts[name])), verb, f"{name}'s Model paragraph")
    return found


SOL_EFFORT_PLACES = (
    (
        "workflow",
        "the highest reasoning demand, little output; where the runner drafts (§4), `gpt-6.1-sol` at effort "
        + effort_reference("draft")
        + " writes it instead",
        "draft",
    ),
    (
        "workflow",
        "the same demand as spec and plan; where the runner drafts (§4), `gpt-6.1-sol` at effort "
        + effort_reference("draft")
        + " writes it instead",
        "draft",
    ),
    (
        "workflow",
        "an error here is the most expensive in the whole run; where the runner drafts (§4), `gpt-6.1-sol` at effort "
        + effort_reference("draft")
        + " writes it instead",
        "draft",
    ),
    ("workflow", "effort " + effort_reference("draft") + ", one call for 2, 2b and 3", "draft"),
    ("workflow", "effort " + effort_reference("draft") + ", drafted in the same call as 2 and 3", "draft"),
    ("workflow", "effort " + effort_reference("draft") + ", drafted in the same call as 2 and 2b", "draft"),
    ("workflow", "sandbox, effort " + effort_reference("repair") + "; one fresh Codex attempt", "repair"),
    ("workflow", "effort " + effort_reference("review") + ", through the Codex CLI", "review"),
    ("workflow", "(`gpt-6.1-sol`, effort " + effort_reference("draft") + ") write", "draft"),
    ("02-spec.md", "(`gpt-6.1-sol`) at effort " + effort_reference("draft") + ", started by", "draft"),
    ("02b-design.md", "(`gpt-6.1-sol`) at effort " + effort_reference("draft") + ", started by", "draft"),
    ("03-plan.md", "(`gpt-6.1-sol`) at effort " + effort_reference("draft") + ", started by", "draft"),
    ("06-review.md", "gpt-6.1-sol at effort " + effort_reference("review") + ", started by", "review"),
)


def routing_problems(workflow: str) -> list[str]:
    """What the routing rows of the doctrine get wrong: section 4's eight rows and section 3's two."""
    found = []
    stage2_rows = routing_rows(section(workflow, "## 4 · "))
    for phase, model in STAGE2_ROUTING.items():
        row = stage2_rows.get(phase)
        if row is None:
            found.append(f"section 4 has no routing row {phase}")
        elif row[0] != model:
            found.append(f"section 4 routes {phase} to {row[0]}, not {model}")
        elif phase == "2a Spec review":
            if "effort `xhigh`" not in row[1]:
                found.append(f"section 4 gives {phase} no effort `xhigh`")
        elif phase in SOL_ROUTING_VERBS:
            found += sol_effort_clause_problems(
                sol_clause(row[1]), SOL_ROUTING_VERBS[phase], f"section 4 routes {phase}"
            )
        elif not model.endswith("Flash") and "effort `max`" not in row[1]:
            found.append(f"section 4 gives {phase} no effort `max`")
    default = routing_rows(section(workflow, "## 3 · "))
    implement = default.get("4 Implement")
    if implement is None or implement[0] != "Sonnet 5.5" or "effort `medium`" not in implement[1]:
        found.append("section 3 does not route 4 Implement to Sonnet 5.5 at effort `medium`")
    for phase in ("2a Spec review", "6 Review"):
        row = default.get(phase)
        if row is None or row[0] != "Opus 5.5":
            found.append(f"section 3 does not route {phase} to Opus 5.5")
    return found


def test_workflow_section_4_routes_the_three_reviews() -> None:
    """Criterion 32: 2, 2b, 3 and 6 stay Codex, 2a is Opus 5.5, 4b rides the ladder, 1 and 4 stay on GLM 5.3 Flash."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert routing_problems(text) == []
    assert class_table_problems(text) == []
    four = routing_rows(section(text, "## 4 · "))
    for needle in ("model-endpoints.yaml", "modelle[n-1]", "round 3 only when round 2 wrote a taken row"):
        assert needle in four["4b Review loop"][1], needle
    assert four["2a Spec review"][0] == "Opus 5.5"
    for phase in ("2 Spec", "2b Design", "3 Plan", "6 Review"):
        assert four[phase][0] == "gpt-6.1-sol", phase
    for old, new in (
        ("| 2a Spec review | **Opus 5.5** |", "| 2a Spec review | **gpt-6.1-sol** |"),
        ("| 4b Review loop | **the ladder** |", "| 4b Review loop | **GLM 5.3** |"),
        ("| 6 Review | **gpt-6.1-sol** |", "| 6 Review | **Opus 5.5** |"),
        (
            f"| 2 Spec | **gpt-6.1-sol** | effort {effort_reference('draft')}, one call",
            f"| 2 Spec | **Opus 5.5** | effort {effort_reference('draft')}, one call",
        ),
        (
            f"| 2b Design | **gpt-6.1-sol** | effort {effort_reference('draft')}, drafted",
            f"| 2b Design | **GLM 5.3 Flash** | effort {effort_reference('draft')}, drafted",
        ),
        (
            f"| 3 Plan | **gpt-6.1-sol** | effort {effort_reference('draft')}, drafted",
            f"| 3 Plan | **Sonnet 5.5** | effort {effort_reference('draft')}, drafted",
        ),
        ("| 1 Explore | **GLM 5.3 Flash** |", "| 1 Explore | **Haiku 4.5** |"),
        ("| 4 Implement | **GLM 5.3 Flash** |", "| 4 Implement | **Sonnet 5.5** |"),
        ("| `bounded` | Opus 5.5, where one is held | the ladder |", "| `bounded` | the ladder | the ladder |"),
        ("| a one-sentence change, a `spike` | no stage 2 |", "| a one-sentence change, a `spike` | the ladder |"),
    ):
        assert old in text, old
        changed = text.replace(old, new, 1)
        assert routing_problems(changed) or class_table_problems(changed), (old, new)


@pytest.mark.parametrize(
    ("doc", "fragment", "verb"),
    SOL_EFFORT_PLACES,
    ids=[f"place-{n}" for n in range(1, len(SOL_EFFORT_PLACES) + 1)],
)
def test_sol_instructions_reference_the_central_effort_for_each_verb(doc: str, fragment: str, verb: str) -> None:
    # Criterion 4. Planted faults: the link dropped, another verb's entry named, or an independent value stands.
    assert sol_effort_problems(WORKFLOW.read_text(encoding="utf-8"), sol_prompt_texts()) == []
    other = next(key for key in stage2.CODEX_EFFORTS if key != verb)
    for planted, why in (
        (fragment.replace(effort_reference(verb), f'`CODEX_EFFORTS["{verb}"]`'), "the link is dropped"),
        (fragment.replace(f'"{verb}"', f'"{other}"'), "another verb's entry is named"),
        (fragment.replace(effort_reference(verb), f"`{stage2.CODEX_EFFORTS[verb]}`"), "an independent literal stands"),
    ):
        doc_text = (WORKFLOW if doc == "workflow" else PROMPTS / doc).read_text(encoding="utf-8")
        assert fragment in doc_text, (doc, fragment)
        assert sol_effort_problems(*sol_texts(doc, doc_text.replace(fragment, planted, 1))), (doc, why)


@pytest.mark.parametrize(
    ("draft_effort", "repair_effort", "review_effort"),
    [("low", "xhigh", "medium"), ("medium", "high", "xhigh")],
    ids=["low-xhigh-medium", "medium-high-xhigh"],
)
@pytest.mark.parametrize("verb", ["draft", "repair", "review"])
def test_sol_effort_changes_propagate_without_other_edits(
    world: World,
    monkeypatch: pytest.MonkeyPatch,
    verb: str,
    draft_effort: str,
    repair_effort: str,
    review_effort: str,
) -> None:
    # Criterion 5. Planted faults: an argv keeps the shipped value, or a retry, resume or re-check loses the setting.
    monkeypatch.setattr(
        stage2, "CODEX_EFFORTS", {"draft": draft_effort, "repair": repair_effort, "review": review_effort}
    )
    if verb == "draft":
        draft_world(world)
        red = red_verify(("pytest", ["FAILED tests/test_x.py::test_a - assert 2 == 1"]))
        world.script(
            codex=[
                codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}),
                codex_ok(
                    "T2",
                    "repaired",
                    plant={
                        "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n"
                    },
                ),
            ],
            make=[red, {"stdout": "green\n"}],
        )
        assert world.run("draft") == 0
        for call in world.calls("codex"):  # the retry keeps the substituted draft entry
            assert f'model_reasoning_effort="{draft_effort}"' in call["argv"]
    elif verb == "repair":
        repair_world(world)
        script_repair(world, [{"stdout": "still looking"}, repair_step()], make=[{"stdout": "green\n"}] * 2)
        assert world.run("repair") == 0
        for call in world.calls("codex"):  # both attempts keep the substituted repair entry
            assert f'model_reasoning_effort="{repair_effort}"' in call["argv"]
    else:
        world.write_findings(
            phase6_block([phase6_cells("F-1", "fixed — tests/test_seed.py::test_seed", "phase finding")])
        )
        world.write_record([("L1-1", "taken — test_a", "no")])
        world.script(codex=[codex_ok("T9", rows(1)), codex_ok("T9", "L1-1: agree")])
        assert world.run("review") == 0
        verdict_call, mark_call = world.calls("codex")
        for call in (verdict_call, mark_call):  # the re-check and its resumed marks keep the substituted entry
            assert f'model_reasoning_effort="{review_effort}"' in call["argv"]
        assert "resume" not in verdict_call["argv"] and mark_call["argv"][:3] == ["exec", "resume", "T9"]

        world.record().unlink(missing_ok=True)
        world.findings.unlink()
        (world.bin / "calls.jsonl").unlink()
        world.write_findings(f"## Phase 2a — Codex, 2026-09-30\n\n{rows(1)}\n\nReviewer session: codex T1")
        world.script(codex=[codex_ok("T1", rows(1))])
        assert world.run("review") == 0
        (resumed,) = world.calls("codex")  # the historical resume keeps it too
        assert f'model_reasoning_effort="{review_effort}"' in resumed["argv"]
        assert resumed["argv"][:3] == ["exec", "resume", "T1"]

        (world.bin / "calls.jsonl").unlink()
        world.script(codex=[codex_ok("T8", rows(1))])
        assert world.run("review") == 0  # the repeated review re-checks fresh, at the same entry
        (recheck,) = world.calls("codex")
        assert f'model_reasoning_effort="{review_effort}"' in recheck["argv"]
        assert "resume" not in recheck["argv"]


def test_sol_effort_checks_allow_other_models_in_the_same_instruction() -> None:
    # Criterion 6. Planted faults: a valid non-Sol effort is rejected, or it masks a wrong Sol reference.
    workflow, prompts = WORKFLOW.read_text(encoding="utf-8"), sol_prompt_texts()
    assert sol_effort_problems(workflow, prompts) == []
    line = next(row for row in workflow.splitlines() if row.startswith(REPAIR_ROW_LABEL))
    assert "Sonnet 5.5 at effort `medium`" in line, "the row does not mix another model's effort in"
    mixed = workflow.replace(line, line[:-2] + "; Sonnet 5.5 drafts by hand at effort `medium` |", 1)
    assert sol_effort_problems(mixed, prompts) == [], "another model's effort is rejected"
    wrong = workflow.replace(line, line.replace(effort_reference("repair"), effort_reference("review"), 1), 1)
    assert sol_effort_problems(wrong, prompts), "a wrong Sol reference passes"
    planted = prompts["02b-design.md"].replace(effort_reference("draft"), effort_reference("review"), 1)
    assert "Opus 5.5 at effort `xhigh`" in flat(planted), "the planted prompt holds no other model's effort"
    assert sol_effort_problems(workflow, {**prompts, "02b-design.md": planted}), "a wrong Sol reference is masked"


DRAFT_ORDER_NEEDLES = (
    ("`python3 scripts/stage2.py draft <change>`", "Codex writes"),
    ("reads the whole draft",),
    ("`python3 scripts/stage2.py spec-review <change>`", "Opus 5.5"),
    ("second `draft <change>`", "open rows in"),
    ("unchanged",),
)


def draft_order_problems(workflow: str) -> list[str]:
    """The draft section's five numbered steps, each carrying its own needles (spec, criterion 33)."""
    draft = section(workflow, "### The draft (phases 2, 2b and 3)")
    if not draft:
        return ["section 4 has no draft section"]
    steps = re.findall(r"^\d+\. (.*)$", draft, re.M)
    if len(steps) != 5:
        return [f"the draft section holds {len(steps)} numbered steps, not 5"]
    found = []
    for step, needles in zip(steps, DRAFT_ORDER_NEEDLES, strict=True):
        one = flat(step)
        for needle in needles:
            if needle not in one:
                found.append(f"a draft-order step lacks '{needle}'")
    return found


def test_the_workflow_states_the_order_of_a_drafted_change() -> None:
    # Criterion 33. Planted fault: one of the five steps removed from the draft section.
    text = WORKFLOW.read_text(encoding="utf-8")
    assert draft_order_problems(text) == []
    steps = re.findall(r"^(\d+\. .*)$", section(text, "### The draft (phases 2, 2b and 3)"), re.M)
    for line in steps:
        assert draft_order_problems(text.replace(line + "\n", "", 1)), line


def test_the_drafting_prompts_name_the_draft_verb() -> None:
    # Criterion 34. Planted fault: a drafting prompt's Model line without `stage2.py draft <change>`.
    for name in ("02-spec.md", "02b-design.md", "03-plan.md"):
        line = model_line((PROMPTS / name).read_text(encoding="utf-8"))
        assert "Codex (`gpt-6.1-sol`)" in line, name
        assert "python3 scripts/stage2.py draft <change>" in line, name
        assert "GLM 5.3 after two failed attempts" in line, name
        planted = line.replace("python3 scripts/stage2.py draft <change>", "the model writes them by hand", 1)
        assert "python3 scripts/stage2.py draft <change>" not in planted, name


def phase_table_problems(workflow: str) -> list[str]:
    """The `4b` row of the phase table: between 4 and 5, with artefact, gate and prompt."""
    lines = section(workflow, "## 2 · ").splitlines()
    rows = [i for i, line in enumerate(lines) if line.startswith("| 4b |")]
    if len(rows) != 1:
        return ["the phase table has no 4b row"]
    at = rows[0]
    if not (lines[at - 1].startswith("| 4 |") and lines[at + 1].startswith("| 5 |")):
        return ["the 4b row does not stand between rows 4 and 5"]
    cells = [cell.strip() for cell in lines[at].strip().strip("|").split("|")]
    found = []
    if len(cells) != 5:
        return [f"the 4b row has {len(cells)} cells, not 5"]
    if "findings.md" not in cells[2] or "release-loop" not in cells[2]:
        found.append("the 4b artefact is not the loop rows in findings.md after release-loop")
    if "at most three rounds" not in cells[3] or "make verify" not in cells[3]:
        found.append("the 4b gate is not at most three rounds with make verify after each repair")
    if "round 3 only when round 2 wrote a taken row" not in cells[3]:
        found.append("the 4b gate does not condition round 3 on round 2's taken row")
    if "04b-review-loop.md" not in cells[4] or not (PROMPTS / "04b-review-loop.md").is_file():
        found.append("the 4b row does not link an existing prompt")
    return found


def test_the_phase_table_has_the_review_loop() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert phase_table_problems(text) == []
    row = next(line for line in text.splitlines() if line.startswith("| 4b |"))
    assert phase_table_problems(text.replace(row + "\n", "")), "the row removed"
    assert phase_table_problems(text.replace("at most three rounds", "rounds", 1))
    assert phase_table_problems(text.replace("round 3 only when round 2 wrote a taken row", "round 3 when needed", 1))
    assert phase_table_problems(text.replace("(`release-loop`)", "", 1))
    assert phase_table_problems(text.replace("04b-review-loop.md", "04c-review-loop.md"))


EVIDENCE_TEXTS = {
    "docs/WORKFLOW.md": ("docs", "WORKFLOW.md"),
    "prompts/04-implement.md": ("prompts", "04-implement.md"),
    "prompts/04b-review-loop.md": ("prompts", "04b-review-loop.md"),
}


def evidence_problems(texts: dict[str, str]) -> list[str]:
    """Where the evidence rule is missing, in the words that carry it."""
    found = []
    for name, text in texts.items():
        one = flat(text)
        for phrase in (
            "only when a test demonstrates it or the spec supports it",
            "as a disagreement",
            "every repair round",
        ):
            if phrase not in one:
                found.append(f"{name} lacks '{phrase}'")
        if not re.search(r"needs a test,? or (?:it )?is rejected", one):
            found.append(f"{name} lacks the consequence: a finding the spec does not cover needs a test or is rejected")
    return found


def test_the_evidence_rule_stands_where_findings_are_taken() -> None:
    texts = {name: REPO_ROOT.joinpath(*parts).read_text(encoding="utf-8") for name, parts in EVIDENCE_TEXTS.items()}
    assert evidence_problems(texts) == []
    for name, text in texts.items():
        for old in ("only when a test demonstrates it or the spec supports it", "as a disagreement"):
            assert old in flat(text), (name, old)
        planted = {
            **texts,
            name: flat(text).replace("only when a test demonstrates it or the spec supports it", "whenever"),
        }
        assert evidence_problems(planted), name
        planted = {**texts, name: re.sub(r"needs a test,? or (it )?is rejected", "is fine", flat(text))}
        assert evidence_problems(planted), name
    # The rule sits in the findings process of section 2, not only somewhere in the file.
    assert "only when a test demonstrates it" in flat(section(texts["docs/WORKFLOW.md"], "### The findings process"))


def standing_problems(workflow: str) -> list[str]:
    found = []
    if "prepared, not active" in workflow:
        found.append("the file still says stage 2 is prepared, not active")
    header = flat(workflow[: workflow.index("## 1 ")])
    if "stage 2 is active for framework content, by change class, since ADR 0007" not in header:
        found.append("the header note does not say stage 2 is active since ADR 0007")
    closing = flat(section(workflow, "## 6 · "))
    if "ADR 0007" not in closing or "first three stage-2 runs" not in closing:
        found.append("section 6 does not say that ADR 0007 opened stage 2 with three measured runs in its place")
    if "Stage 1 must have run for two to three weeks" in closing:
        found.append("section 6 still presents two to three weeks of stage 1 as the condition to be met")
    return found


def test_the_standing_note_says_stage_2_is_active() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert standing_problems(text) == []
    assert standing_problems(
        text.replace("stage 2 is active for framework content", "Stages 2 and 3 are prepared, not active")
    )
    assert standing_problems(re.sub(r"first three\s+stage-2 runs", "first runs", text))
    assert standing_problems(re.sub(r"ADR\s+0007 \(2026-09-30\) opened", "a decision opened", text))
    assert standing_problems(
        text.replace("Stage 1 was to run for two to three weeks", "Stage 1 must have run for two to three weeks")
    )


def configured_not_measured_problems(workflow: str) -> list[str]:
    """Section 4 must present the foreign programs' settings as passed, not as proven (repair round 1, F-8)."""
    four = flat(section(workflow, "## 4 · "))
    found = []
    if "configured on every call, not measured" not in four:
        found.append("section 4 does not say the settings are configured on every call, not measured")
    for fact in ("Codex also runs in the read-only sandbox", "GLM runs as Claude Code"):
        if fact in four:
            found.append(f"section 4 states as a fact: {fact}")
    if "tracked `.codex/hooks.json`" not in four:
        found.append("section 4 does not name what an ineffective hooks switch would let through")
    return found


def test_section_4_says_the_foreign_settings_are_passed_not_measured() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert configured_not_measured_problems(text) == []
    flatter = text.replace("configured on every call, not measured", "in force")
    assert flatter != text and configured_not_measured_problems(flatter)
    assert configured_not_measured_problems(
        text.replace("The runner starts Codex", "Codex also runs in the read-only sandbox. The runner starts Codex")
    )
    assert configured_not_measured_problems(text.replace("tracked `.codex/hooks.json`", "a hooks file"))


def review_prompt_problems(spec_review: str, review: str) -> list[str]:
    """Criterion 34: 2a's Model line is Opus 5.5 through the runner and no Codex; 6 keeps its verb and verdict."""
    found = []
    model = model_line(spec_review)
    if "gpt-6.1-sol" in model or "Codex" in model:
        found.append("02a-spec-review.md's Model line still routes the spec review to Codex")
    for needle in ("Opus 5.5", "stage2.py spec-review <change>", "scripts/stage2.py"):
        if needle not in model:
            found.append(f"02a-spec-review.md's Model line lacks {needle}")
    one = flat(review)
    if "gpt-6.1-sol" not in one or "scripts/stage2.py" not in one:
        found.append("06-review.md lacks the Codex model or the runner")
    if "stage2.py review <change>" not in one:
        found.append("06-review.md does not name the verb review")
    if "Phase 6 verdict:" not in one or "release-loop" not in one:
        found.append("06-review.md lacks the verdict line or release-loop")
    elif one.index("Phase 6 verdict:") > one.index("release-loop") or "before you read any loop row" not in one:
        found.append("06-review.md does not put the verdict before the loop rows")
    return found


def model_line(prompt: str) -> str:
    """The text of the `**Model:**` paragraph, up to the next bold label."""
    match = re.search(r"^\*\*Model:\*\*(.*?)(?=^\*\*[A-Z])", prompt, re.M | re.S)
    return flat(match[1]).strip() if match else ""


def implement_line_problems(line: str) -> list[str]:
    """The live Flash command, its explicit Sonnet fallback and leak stop."""
    found = []
    if not line.startswith("GLM 5.3 Flash —"):
        found.append("the implement prompt does not lead with GLM 5.3 Flash")
    if "stage2.py implement <change>" not in line:
        found.append("the implement prompt does not name the live runner verb")
    if "Sonnet 5.5 at effort `medium`" not in line or "claude-sonnet-5-5" not in line:
        found.append("the implement prompt does not pin the Stage-1 route to Sonnet 5.5 at effort `medium`")
    if "--stage2-off [REASON]" not in line:
        found.append("the implement prompt does not name the explicit fallback option")
    if "leak-check BLOCK stops" not in line or "never falls back" not in line:
        found.append("the implement prompt does not stop a leak without fallback")
    return found


def test_the_implement_prompt_names_flash_and_keeps_sonnet_5_5_at_medium() -> None:
    line = model_line((PROMPTS / "04-implement.md").read_text(encoding="utf-8"))
    assert implement_line_problems(line) == []
    for planted in (
        "GLM 5.3 Flash — Sonnet 5.5 at effort `medium` (`claude-sonnet-5-5`)",
        "GLM 5.3 Flash — stage2.py implement <change>; Sonnet 5 at effort `medium` (`claude-sonnet-5`)",
        "GLM 5.3 Flash — stage2.py implement <change>; Sonnet 5.5 at effort `high` (`claude-sonnet-5-5`)",
    ):
        assert implement_line_problems(model_line(f"**Model:** {planted}\n**Input:** x\n")), planted


def test_the_explore_prompt_names_the_live_flash_command_and_haiku_fallback() -> None:
    line = model_line((PROMPTS / "01-explore.md").read_text(encoding="utf-8").replace("**Result:**", "**Input:**", 1))
    assert line.startswith("GLM 5.3 Flash —")
    for required in (
        "stage2.py explore <change>",
        "--stage2-off [REASON]",
        "Haiku 4.5 explores",
        "leak-check BLOCK stops",
        "never falls back",
    ):
        assert required in line
    for planted in ("Haiku 4.5 — much input", "GLM 5.3 Flash — much input; Haiku 4.5 explores"):
        bad = model_line(f"**Model:** {planted}\n**Input:** x\n")
        assert not all(
            phrase in bad for phrase in ("stage2.py explore <change>", "--stage2-off [REASON]", "Haiku 4.5 explores")
        ), planted


def flash_runner_doctrine_problems(texts: dict[str, str]) -> list[str]:
    """The live commands, explicit fallback, leak stop and runner-owned gate in their operative texts."""
    found = []
    workflow = flat(texts["docs/WORKFLOW.md"])
    agents = flat(texts["AGENTS.md"])
    explore = flat(texts["prompts/01-explore.md"])
    implement = flat(texts["prompts/04-implement.md"])
    plan = flat(texts["prompts/03-plan.md"])
    for name, one, verb in (
        ("workflow", workflow, "explore"),
        ("workflow", workflow, "implement"),
        ("agents", agents, "explore"),
        ("agents", agents, "implement"),
        ("explore prompt", explore, "explore"),
        ("implement prompt", implement, "implement"),
    ):
        if verb not in one:
            found.append(f"{name} does not name {verb}")
    if "stage2.py explore <change>" not in explore:
        found.append("explore prompt does not name its exact runner command")
    if "stage2.py implement <change>" not in implement:
        found.append("implement prompt does not name its exact runner command")
    for name, one in (
        ("workflow", workflow),
        ("agents", agents),
        ("explore prompt", explore),
        ("implement prompt", implement),
    ):
        if "--stage2-off [REASON]" not in one:
            found.append(f"{name} does not name the explicit Stage-1 route")
        if "leak" not in one.lower() or not any(
            phrase in one.lower() for phrase in ("without fallback", "never falls back", "never selects the fallback")
        ):
            found.append(f"{name} does not stop on a leak without fallback")
    if not re.search(r"runner runs (?:exactly )?`make verify`", workflow) or "checkpoint commit" not in workflow:
        found.append("workflow does not give verification and the checkpoint to the runner")
    if "file tools but no command tool" not in implement:
        found.append("implement prompt does not state its no-command boundary")
    if "copy that route, model and reason into `plan.md`" not in plan:
        found.append("plan prompt does not carry the Explore fallback forward")
    for stale in ("two Flash rows are decided and not built", "Four verbs exist", "do not yet"):
        if stale in workflow:
            found.append(f"workflow retains stale wording: {stale}")
    return found


def test_the_doctrine_and_prompts_say_the_flash_verbs_are_live() -> None:
    paths = ["docs/WORKFLOW.md", "AGENTS.md", "prompts/01-explore.md", "prompts/03-plan.md", "prompts/04-implement.md"]
    texts = {name: (REPO_ROOT / name).read_text(encoding="utf-8") for name in paths}
    assert flash_runner_doctrine_problems(texts) == []
    for name, needle, replacement in (
        ("docs/WORKFLOW.md", "--stage2-off [REASON]", "automatic fallback"),
        ("AGENTS.md", "without fallback", "with fallback"),
        ("prompts/01-explore.md", "stage2.py explore <change>", "stage2.py research <change>"),
        ("prompts/04-implement.md", "file tools but no command tool", "all tools"),
        ("prompts/03-plan.md", "copy that route,\n  model and reason into `plan.md`", "remember it"),
    ):
        assert needle in texts[name]
        planted = {**texts, name: texts[name].replace(needle, replacement)}
        assert flash_runner_doctrine_problems(planted), (name, needle)


def class_table_problems(workflow: str) -> list[str]:
    """The class table: a change's 2a is Opus 5.5, its loop rides the ladder, phase 6 is a fresh Codex session."""
    found = []
    rows = {
        line.split("|")[1].strip(): [cell.strip() for cell in line.split("|")[2:-1]]
        for line in section(workflow, "### Which change gets what").splitlines()
        if line.startswith("| ") and not line.startswith("| Change") and not line.startswith("|---")
    }
    bounded = rows.get("`bounded`")
    if bounded is None or len(bounded) != 3:
        return ["the class table has no `bounded` row of three cells"]
    if not bounded[0].startswith("Opus 5.5") or not bounded[1].startswith("the ladder"):
        found.append("the class table does not send a change's 2a to Opus 5.5 and its 4b to the ladder")
    if not bounded[2].startswith("Codex, a fresh session"):
        found.append("the class table does not start phase 6 in a fresh Codex session")
    spike = rows.get("a one-sentence change, a `spike`")
    if spike is None or len(spike) != 3 or any(cell != "no stage 2" for cell in spike):
        found.append("the class table does not leave a spike and a one-sentence change without stage 2")
    if "Fable" in "".join("".join(cells) for cells in rows.values()):
        found.append("the class table names Fable")
    return found


def test_no_fable_in_the_routing_rows_or_the_prompts() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    rows = routing_rows(section(text, "## 3 · ")) | routing_rows(section(text, "## 4 · "))
    assert rows and not [phase for phase, (model, why) in rows.items() if "fable" in (model + why).lower()]
    assert [p.name for p in PROMPTS.glob("*.md") if "fable" in p.read_text(encoding="utf-8").lower()] == []
    planted = text.replace("| 2a Spec review | **Opus 5.5**", "| 2a Spec review | **Fable 5.1**", 1)
    assert "Fable 5.1" in routing_rows(section(planted, "## 3 · "))["2a Spec review"][0]


def test_the_flash_rows_say_they_are_live_through_the_runner() -> None:
    one = flat(section(WORKFLOW.read_text(encoding="utf-8"), "## 4 · "))
    assert "The two Flash rows are live through the runner." in one
    for phrase in ("`explore` starts phase 1", "`implement` starts phase 4", "--stage2-off [REASON]"):
        assert phrase in one
    assert "The two Flash rows are decided and not built." not in one and "Until that is built" not in one


def test_the_plan_prompt_asks_for_no_markings() -> None:
    text = (PROMPTS / "03-plan.md").read_text(encoding="utf-8")
    markings = ("[FLASH]", "[GLM5.3]", "[SONNET]", "plan-marking", "Model markings")
    assert [m for m in markings if m in text] == []
    assert [m for m in markings if m in text + "\n`[FLASH]`\n"] == ["[FLASH]"]


def test_the_spec_prompt_asks_one_condition_and_a_refutation() -> None:
    text = flat((PROMPTS / "02-spec.md").read_text(encoding="utf-8"))
    sentence = (
        "one condition each; where a trigger, a state or a failure applies, the sentence begins with When, While or If"
    )
    assert sentence in text and "comes with what would *refute* it" in text
    assert sentence not in text.replace("one condition each", "as many as fit")
    assert "comes with what would *refute* it" not in text.replace("*refute*", "")


def agents_md_problems(text: str) -> list[str]:
    found = []
    if not re.search(r"^\| 4b \| Review loop \*\(stage 2\)\* \|.*three rounds.*\|$", text, re.M):
        found.append("AGENTS.md has no 4b row with its gate")
    row = next((line for line in text.splitlines() if line.startswith("| 4b |")), "")
    if "round 3 only when round 2 wrote a taken row" not in row:
        found.append("AGENTS.md has no 4b row with the round-3 condition")
    one = flat(text)
    if (
        "is started only through `python3 scripts/stage2.py`" not in one
        or "runs the leak check before every call" not in one
    ):
        found.append("AGENTS.md lacks the sentence that a foreign reviewer is started only through the runner")
    if "Codex reviews 2a and 6" in one:
        found.append("AGENTS.md still says Codex reviews 2a and 6")
    for needle in (
        "Codex drafts spec, design and plan (`draft <change>`; GLM 5.3 after two failed attempts)",
        "Opus 5.5 reviews 2a (`spec-review <change>`)",
        "reviews 6",
        "`draft <change>`,",
    ):
        if needle not in one:
            found.append(f"AGENTS.md lacks '{needle}'")
    return found


def test_agents_md_names_the_loop_and_the_runner() -> None:
    text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert agents_md_problems(text) == []
    assert text.count("\n") <= 200
    row = next(line for line in text.splitlines() if line.startswith("| 4b |"))
    assert agents_md_problems(text.replace(row + "\n", ""))
    assert agents_md_problems(text.replace("only through", "also through"))
    assert agents_md_problems(text.replace("round 3 only when round 2 wrote a taken row", "round 3 as needed"))
    assert agents_md_problems(text.replace("Codex drafts spec, design and plan", "Codex reviews spec, design", 1))
    assert agents_md_problems(text.replace("Opus 5.5 reviews 2a", "Codex reviews 2a", 1))
    assert agents_md_problems(text.replace("GLM 5.3 after two failed attempts", "GLM 5.3 when asked", 1))


def test_workflow_section_4_keeps_the_lineage_argument() -> None:
    """Criterion 22: the why stands and names the rungs' lineages instead of two reviewers of one round."""
    four = flat(section(WORKFLOW.read_text(encoding="utf-8"), "## 4 · "))
    for phrase in (
        "blind spots",
        "Disagreements are recorded, not resolved automatically",
        "is the information",
        "DeepSeek",
        "MiMo",
        "Rung 1 flagged it, rung 2 did not",
    ):
        assert phrase in four, phrase
    assert "Codex flagged it, GLM did not" not in four


def test_the_prompts_name_the_ladder_and_the_limit() -> None:
    """Criterion 23: the loop text names the ladder and the three rounds; 2a and 6 name Codex and the limit; Flash stays."""
    texts = {
        "02a": (PROMPTS / "02a-spec-review.md").read_text(encoding="utf-8"),
        "04b": (PROMPTS / "04b-review-loop.md").read_text(encoding="utf-8"),
        "06": (PROMPTS / "06-review.md").read_text(encoding="utf-8"),
        "agents": (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8"),
    }
    one = flat(texts["04b"])
    for needle in ("ladder", "opencode-go", "three rounds", "round 3 only when round 2 wrote", "taken"):
        assert needle in one, ("04b", needle)
    for name in ("02a", "06"):
        one = flat(texts[name])
        assert "gpt-6.1-sol" in one, name
        assert "three rounds" in one and "round 3 only when round 2 wrote" in one, name
        assert "deepseek-v4.1-flash" not in one and "mimo-v2.6" not in one, name
    agents = flat(texts["agents"])
    for needle in ("ladder", "opencode-go", "three rounds", "round 3 only when round 2 wrote"):
        assert needle in agents, ("agents", needle)
    for name in ("01-explore.md", "04-implement.md"):
        assert "GLM 5.3 Flash" in (PROMPTS / name).read_text(encoding="utf-8"), name


def reads_problems(text: str, where: str) -> list[str]:
    """Criterion 28: what a loop round can read is said plainly, and the loop is not counted among the confined calls."""
    one = flat(text)
    found = []
    for needle, why in (
        ("and they are not confined", "does not say the loop's Pi calls are not confined"),
        (
            "outside the worktree (measured with Pi 1.1.0",
            "does not say a round's read reaches outside the worktree, measured",
        ),
        ("secrets file is among them", "does not name the secrets file among what a round can reach"),
        ("only the prompt's request bounds it", "does not say only the prompt's request bounds the reach"),
        ("measured once by hand on the pinned version", "does not say the isolation flags were measured once by hand"),
    ):
        if needle not in one:
            found.append(f"{where} {why}")
    for claim in (
        "Every Claude Code call (the review loop's calls",
        "Every call (explore, implement, the Sonnet fallback attempts and the reviewers)",
        "confined for every call",
        "starts in the worktree with `--restricted` and no `--add-dir`; the reviewers",
    ):
        if claim in one:
            found.append(f"{where} counts the loop among the confined calls: {claim}")
    return found


def test_section_4_says_what_a_round_can_read() -> None:
    """Criterion 28: section 4 and the runner's docstring both say it; a planted overclaim turns each red."""
    workflow = section(WORKFLOW.read_text(encoding="utf-8"), "## 4 · ")
    docstring = (REPO_ROOT / "scripts" / "stage2.py").read_text(encoding="utf-8").split('"""')[1]
    assert reads_problems(workflow, "section 4") == []
    assert reads_problems(docstring, "docstring") == []
    for text, where in ((workflow, "section 4"), (docstring, "docstring")):
        flat_text = flat(text)
        for kept, planted in (
            ("and they are not confined", "and they are confined"),
            ("the secrets file is among them", "nothing private is among them"),
            ("only the prompt's request bounds it", "the tools bound it"),
            ("measured once by hand on the pinned version", "measured by the suite"),
        ):
            assert kept in flat_text, (where, kept)
            assert reads_problems(flat_text.replace(kept, planted), where), (where, planted)
    overclaim = flat(workflow).replace(
        "Every Claude Code call (explore,", "Every Claude Code call (the review loop's calls, explore,"
    )
    assert reads_problems(overclaim, "section 4")


CAVEAT_CLIENTS = (
    "Claude Code for Z.ai",
    "the Codex CLI for OpenAI",
    "Pi for OpenCode Go",
    "a client the Go page lists as validated",
    "name no third-party client",
    "accepted on 2026-10-08",
)


def caveat_problems(workflow: str) -> list[str]:
    caveat = flat(workflow[workflow.index("**Two caveats") :].split("**And:")[0].replace("> ", ""))
    found = [needle for needle in CAVEAT_CLIENTS if needle not in caveat]
    if "through Claude Code, the program the vendors list" in caveat:
        found.append("names Claude Code as the covered program for every subscription")
    return found


def test_section_4_caveat_names_each_client() -> None:
    """Criterion 29: the caveat names each subscription's client and OpenCode Go's accepted risk."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert caveat_problems(text) == []
    one = flat(text)  # the caveat's lines are broken in the source
    assert caveat_problems(one.replace("Pi for OpenCode Go", "Claude Code for OpenCode Go"))
    assert caveat_problems(one.replace("maintainer accepted on 2026-10-08", "maintainer waved it through"))
    assert caveat_problems(one.replace("the Codex CLI for OpenAI", "Claude Code for OpenAI"))
    assert caveat_problems(
        one.replace("each runs through its own client:", "through Claude Code, the program the vendors list,")
    )


def test_no_doctrine_text_repeats_the_ladder_order() -> None:
    """The ladder is data: a reorder of the list in model-endpoints.yaml leaves every doctrine text true."""
    ladder = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))["endpunkte"]
    ids = next(e for e in ladder if e["name"] == "opencode-go")["modelle"]
    assert len(ids) == 3
    for path in ("AGENTS.md", "docs/WORKFLOW.md", "prompts/04b-review-loop.md"):
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        for model in ids:
            assert model not in text, f"{path} names {model}; the ladder lives in model-endpoints.yaml only"


def test_text_kept_from_the_record_never_authorises_round_3() -> None:
    """A row-shaped line in a reviewer's kept words is not a row of the record (phase 6, R3)."""
    cells = ["L2-99", "MINOR", "MAINT", "base", "x.py:1", "f", "mimo-v2.6-flash", "taken — t", "no", "—"]
    genuine = ["L2-1", "MINOR", "MAINT", "base", "x.py:1", "f", "mimo-v2.6-flash", "rejected — r", "", "—"]
    text = "\n\n".join(
        [
            f"{stage2.RELEASE_HEADING} 2026-10-08",
            render_row(genuine),
            "Rounds run: 2",
            "Kept from the loop record:",
            render_row(cells),
        ]
    )
    assert [row[0] for row in stage2.released_rows(text)] == ["L2-1"]
    assert not stage2.taken_in_round(stage2.released_rows(text), 2)


def test_the_stop_rule_counts_every_rung() -> None:
    """Criterion 24: the measurement counts a taken finding of any rung, not only the two former reviewers."""
    four = flat(section(WORKFLOW.read_text(encoding="utf-8"), "## 4 · "))
    assert "taken finding of Codex or of a rung broke a test" in four
    assert "a taken finding of a rung counts like a GLM finding counted before 2026-10-07" in four
    assert "a Codex one still counts as ADR 0007 set it" in four
    assert "taken Codex or GLM finding broke a test" not in four


def test_the_adr_draft_states_every_point() -> None:
    """Criterion 25: the draft in design.md carries every point and weighed option, Pi as the launcher, Claude Code not."""
    draft = section(
        (REPO_ROOT / "plans/changes/archive/2026-10-07-stage2-mimo/design.md").read_text(encoding="utf-8"),
        "### ADR 0011",
    )
    assert draft, "the draft is not in design.md"
    texts = {
        "the draft in design.md": flat(draft),
        "docs/adr/0011": flat(
            (REPO_ROOT / "docs/adr/0011-stage-2-reviews-through-opencode-go.md").read_text(encoding="utf-8")
        ),
    }
    for needle in (
        "Framework content may also go to `opencode-go`",
        "`https://opencode.ai/zen/go/v1/chat/completions`, through Pi",
        "the review loop (4b) only",
        "The interactive `session` verb reaches a declared endpoint under its own amendment",
        "The loop's reviewer role moves",
        "the spec review and the review stay with Codex",
        "explore and implement stay on GLM 5.3 Flash",
        "The ladder is data, not code",
        "modelle[n-1]",
        "one-line pull request",
        "at most three rounds",
        "The unconfined reads accepted for ADR 0007's reviewers extend to the rungs",
        "`read` reaches files outside the worktree",
        "as `OPENCODE_API_KEY`",
        "Each round is isolated, and Pi is pinned",
        "`high` for both MiMo rungs",
        "The terms risk is accepted",
        "Keep Codex and GLM in every review role",
        "An OpenCode product other than Go",
        "Claude Code at the Anthropic-compatible address",
        "OpenCode's own CLI",
        "A round without tools",
        "The model of round 2",
        "runde 2 flash",
    ):
        for name, one in texts.items():
            assert needle in one, f"{needle!r} is missing from {name}"
    for name, one in texts.items():
        assert "through Claude Code, which the vendor lists" not in one, name


def continuity_problems(amendments: dict, target: str, adr_dir: Path) -> list[str]:
    """D-13 is mapped to ADR 0007, which names it, and its row in the target document reads Amend."""
    found = []
    if amendments.get("D-13") != (ADR_0007,):
        found.append("the amendment map does not send D-13 to ADR 0007")
    adr = adr_dir / ADR_0007
    if not adr.is_file():
        found.append("ADR 0007 does not exist")
    elif not re.search(r"\bD-13\b", adr.read_text(encoding="utf-8")):
        found.append("ADR 0007 does not name D-13")
    row = next((line for line in target.splitlines() if line.startswith("| D-13 ")), "")
    if not row.startswith("| D-13 — cross-vendor entry | Amend |") or "ADR 0007" not in row:
        found.append("the D-13 row of the target document does not read Amend with ADR 0007")
    return found


def test_d13_is_amended_by_adr_0007(tmp_path: Path) -> None:
    adr_dir = REPO_ROOT / "docs" / "adr"
    target = TARGET.read_text(encoding="utf-8")
    amendments = check_decision_continuity.AMENDMENT_ADRS
    assert continuity_problems(amendments, target, adr_dir) == []
    assert continuity_problems({k: v for k, v in amendments.items() if k != "D-13"}, target, adr_dir)
    assert continuity_problems(
        amendments, target.replace("cross-vendor entry | Amend |", "cross-vendor entry | Retain |"), adr_dir
    )
    assert continuity_problems(amendments, target, tmp_path)
    (tmp_path / ADR_0007).write_text("an ADR that names nothing\n", encoding="utf-8")
    assert continuity_problems(amendments, target, tmp_path)
    # The gate itself accepts the tree, and the ADR says what the plan says it says.
    assert check_decision_continuity.run(TARGET) == []
    adr = flat((adr_dir / ADR_0007).read_text(encoding="utf-8"))
    for needle in (
        "Kimi is dropped",
        "does not enter M2",
        "a request, not a lock",
        "neither endpoint",
        # the amendment of 2026-10-06
        "and so is Fable",
        "Explore and implement run on GLM 5.3 Flash — decided, not built.",
        "LakeSwitch and customer content never go",
        "falls back to Opus 5.5",
    ):
        assert needle in adr, needle
    assert "phases 1 and 4 stay with Anthropic" not in adr and "Fable 5.1 until" not in adr
    # Both architecture documents that set D-13's criteria carry the dated note.
    for doc in (TARGET, PLAN_DOC):
        note = flat(doc.read_text(encoding="utf-8"))
        assert "Changed, 2026-09-30" in note and "ADR 0007" in note, doc.name


# ---------------------------------------------------------------------------
# The repair of the taken findings in the doctrine (stage2-repair criteria 29-33)
# ---------------------------------------------------------------------------


def glm_entry_problems(entry: dict) -> list[str]:
    """Criterion 29: the GLM entry keeps its models and its remark names every work verb."""
    found = []
    if entry.get("betreiber") != "Zhipu AI (Z.ai)":
        found.append("the operator changed")
    if entry.get("residenz") != "anbieter-erklaert" or entry.get("darf_sehen") != ["framework"]:
        found.append("residency or visibility changed")
    if entry.get("modelle") != ["glm-5.3", "glm-5.3-flash"]:
        found.append("the model list changed")
    remark = " ".join(str(entry.get("bemerkung", "")).lower().split())
    for needle in (
        "stage2.py explore",
        "stage2.py implement",
        "stage2.py repair",
        "stage2.py draft",
        "no review phase routes to it",
    ):
        if needle not in remark:
            found.append(f"the remark lacks '{needle}'")
    return found


def test_the_glm_entry_keeps_its_models_and_names_the_repair_verb() -> None:
    """Criterion 29. Planted fault: a model dropped, or the remark without `stage2.py repair`."""
    entry = endpoints()["glm-coding-plan"]
    assert glm_entry_problems(entry) == []
    assert glm_entry_problems({**entry, "modelle": ["glm-5.3-flash"]})
    assert glm_entry_problems(
        {**entry, "bemerkung": entry["bemerkung"].replace("stage2.py repair", "stage2.py fix", 1)}
    )
    assert glm_entry_problems(
        {**entry, "bemerkung": entry["bemerkung"].replace("stage2.py draft", "stage2.py sketch", 1)}
    )
    assert glm_entry_problems({**entry, "residenz": "unbekannt"})


def repair_doctrine_problems(workflow: str, agents: str) -> list[str]:
    """Criterion 30: the doctrine names the verb, routes the repair, and gives the Status to the orchestrator."""
    found = []
    four = flat(section(workflow, "## 4 · "))
    if "Nine verbs exist" in four or "Ten verbs exist" not in four:
        found.append("section 4 does not say ten verbs")
    if "- `repair` — Codex, every taken finding" not in workflow:
        found.append("the verb list has no repair bullet")
    if "| Repair after 4b and 6 | **gpt-6.1-sol** |" not in workflow:
        found.append("the routing table has no repair row")
    if "### Repairing taken findings (repair)" not in workflow:
        found.append("the repair subsection is missing")
    loop = flat(section(workflow, "### The review loop"))
    if "The orchestrator writes" not in loop or "verb repairs the taken rows" not in loop:
        found.append("the loop section does not give the Status to the orchestrator and the repair to the verb")
    fixing = flat(section(workflow, "### Repairing taken findings"))
    for needle in ("python3 scripts/stage2.py repair <change>", "Red first", "Broke a test"):
        if needle not in fixing:
            found.append(f"the repair subsection lacks '{needle}'")
    one = flat(agents)
    if "Codex repairs the findings the orchestrator takes" not in one:
        found.append("AGENTS.md does not name the repair on Codex")
    if "explore, draft, implement and repair do not" not in one:
        found.append("AGENTS.md does not count repair and draft among the verbs without reviews by class")
    return found


def test_the_doctrine_names_the_repair_verb() -> None:
    """Criterion 30. Planted fault: "Nine verbs exist" kept, or AGENTS.md without the verb."""
    workflow = WORKFLOW.read_text(encoding="utf-8")
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert repair_doctrine_problems(workflow, agents) == []
    assert repair_doctrine_problems(workflow.replace("Ten verbs exist", "Nine verbs exist", 1), agents)
    assert repair_doctrine_problems(
        workflow.replace("- `repair` — Codex, every taken finding", "- `repair` — GLM 5.3 Flash, taken findings", 1),
        agents,
    )
    assert repair_doctrine_problems(
        workflow.replace(
            "| Repair after 4b and 6 | **gpt-6.1-sol** |", "| Repair after 4b and 6 | **Sonnet 5.5** |", 1
        ),
        agents,
    )
    assert repair_doctrine_problems(
        workflow.replace("### Repairing taken findings (repair)", "### Fixing findings", 1),
        agents,
    )
    assert repair_doctrine_problems(
        workflow.replace(
            "The orchestrator writes beside each row its", "The implementer writes beside each row its", 1
        ),
        agents,
    )
    assert repair_doctrine_problems(
        workflow,
        agents.replace("Codex repairs the findings the orchestrator takes", "GLM 5.3 Flash explores and implements", 1),
    )
    assert repair_doctrine_problems(workflow, agents.replace("implement and repair do not", "implement do not", 1))
    assert repair_doctrine_problems(
        workflow, agents.replace("draft, implement and repair do not", "implement and repair do not", 1)
    )


def repair_prompt_problems(loop: str, implement: str) -> list[str]:
    """Criterion 31: the orchestrator's steps in 04b, the verb and red first in 04."""
    found = []
    one, four = flat(loop), flat(implement)
    if "For the orchestrator" not in one or "For the implementer" in one:
        found.append("04b does not speak to the orchestrator")
    for name, text in (("04b", one), ("04", four)):
        if "python3 scripts/stage2.py repair <change>" not in text:
            found.append(f"{name} does not name `stage2.py repair <change>`")
    for needle in ("taken — not a test — <reason>", "Broke a test"):
        if needle not in one:
            found.append(f"04b lacks '{needle}'")
    for needle in ("red first", "gpt-6.1-sol", "fixed — tests/<path>::<function>", "fixed — not a test — <reason>"):
        if needle not in four:
            found.append(f"04 lacks '{needle}'")
    return found


def test_the_prompts_name_the_repair_verb_and_red_first() -> None:
    """Criterion 31. Planted fault: 04b without the command, or 04 without red first."""
    loop = (PROMPTS / "04b-review-loop.md").read_text(encoding="utf-8")
    implement = (PROMPTS / "04-implement.md").read_text(encoding="utf-8")
    assert repair_prompt_problems(loop, implement) == []
    assert repair_prompt_problems(
        loop.replace("python3 scripts/stage2.py repair", "python3 scripts/stage2.py fix", 1),
        implement,
    )
    assert repair_prompt_problems(loop.replace("## For the orchestrator", "## For the implementer", 1), implement)
    assert repair_prompt_problems(loop, implement.replace("red first", "green first", 1))
    assert repair_prompt_problems(loop, implement.replace("fixed — tests/<path>::<function>", "fixed — tests", 1))


REPAIR_STATUS_WORDS = [
    "taken — <reason>",
    "taken — not a test — <reason>",
    "fixed — tests/<path>::<function>",
    "fixed — not a test — <reason>",
]


def template_problems(template: str) -> list[str]:
    """Criterion 32: the four Status words of a stage-2 row stand in the findings template."""
    one = flat(template)
    return [word for word in REPAIR_STATUS_WORDS if word not in one]


def test_the_findings_template_names_the_repair_statuses() -> None:
    """Criterion 32. Planted fault: one of the four words missing."""
    template = (REPO_ROOT / "templates" / "findings.md").read_text(encoding="utf-8")
    assert template_problems(template) == []
    one = flat(template)
    for word in REPAIR_STATUS_WORDS:
        assert template_problems(one.replace(word, "—", 1)), word


def adr_0015_problems(text: str) -> list[str]:
    """Criterion 33: the record amends ADR 0011 and holds the routing sentences."""
    found = []
    if not text.startswith("---\n"):
        found.append("the record has no yaml header")
    one = flat(text)
    for needle in ("Amends ADR 0011", "The repair of taken findings runs on GLM 5.3", "never repairs its own findings"):
        if needle not in one:
            found.append(f"the record lacks '{needle}'")
    return found


def test_adr_0015_amends_adr_0011_and_records_the_repair_route() -> None:
    """Criterion 33. Planted fault: the file missing, or the amendment unstated."""
    path = REPO_ROOT / "docs" / "adr" / "0015-glm-5-3-repairs-taken-findings.md"
    assert path.is_file(), "the record is missing"
    text = path.read_text(encoding="utf-8")
    assert adr_0015_problems(text) == []
    for needle in ("Amends ADR 0011", "The repair of taken findings runs on GLM 5.3", "never repairs its own findings"):
        assert adr_0015_problems(text.replace(needle, "something else", 1)), needle


def adr_0017_problems(old: str, new: str) -> list[str]:
    """Criterion 21: 0015 is marked superseded with its body kept; 0017 carries the rules that stand."""
    found = []
    if not re.search(r"^status: superseded$", old, re.M) or not re.search(r'^superseded_by: "0017"$', old, re.M):
        found.append("ADR 0015 lacks its supersession marker")
    if adr_0015_problems(old):
        found.append("ADR 0015's decision body was rewritten")
    one = flat(new)
    for needle in (
        "Supersedes ADR 0015",
        "Codex repairs all taken findings in one batch",
        "`workspace-write`",
        "fixed — tests/<path>::<function>",
        "red against baseline code",
        "round 3 requires a taken or fixed row in round 2",
        "the maximum stays three rounds",
        "A fixed row counts as taken",
        "a fresh session re-checks",
        "after an earlier `## Phase 6` block",
    ):
        if needle not in one:
            found.append(f"ADR 0017 lacks '{needle}'")
    return found


def test_adr_0017_supersedes_0015_and_keeps_the_repair_contract() -> None:
    """Criterion 21. Planted fault: marker missing, 0015's body rewritten, or a retained rule dropped."""
    old = (REPO_ROOT / "docs" / "adr" / "0015-glm-5-3-repairs-taken-findings.md").read_text(encoding="utf-8")
    new = (REPO_ROOT / "docs" / "adr" / "0017-codex-repairs-taken-findings.md").read_text(encoding="utf-8")
    assert adr_0017_problems(old, new) == []
    assert adr_0017_problems(old.replace("status: superseded", "status: accepted", 1), new)
    assert adr_0017_problems(old.replace('superseded_by: "0017"\n', "", 1), new)
    assert adr_0017_problems(old.replace("The repair of taken findings runs on GLM 5.3", "x", 1), new)
    # Planted on the flattened text: the checker reads a sentence broken across lines as one
    assert "the maximum stays three rounds" in flat(new)
    assert adr_0017_problems(old, flat(new).replace("the maximum stays three rounds", "no limit", 1))
    assert adr_0017_problems(old, new.replace("Supersedes ADR 0015", "Amends ADR 0015", 1))


def codex_repair_doctrine_problems(texts: dict[str, str]) -> list[str]:
    """Criteria 18 and 20: repair routing, confinement and each phase-6 session rule agree with the runner."""
    found = []
    runner = texts["scripts/stage2.py"]
    if "repair       <change>   # Codex" not in runner:
        found.append("the runner help does not name Codex for repair")
    if "you cannot run commands" in runner.split("REPAIR_FORMAT = (")[1].split("REPAIR_FORMAT_FILE_TOOLS")[0]:
        found.append("the Codex repair text claims Codex cannot run commands")
    workflow = flat(texts["docs/WORKFLOW.md"])
    for needle in ("a fresh read-only Codex session", "The exception (ADR 0017)", "not the CLI's confinement"):
        if needle not in workflow:
            found.append(f"WORKFLOW lacks '{needle}'")
    if "A reviewer never repairs its own findings" in workflow:
        found.append("WORKFLOW keeps the blanket ban")
    call_settings = workflow.partition("What every call then carries:")[2].partition("Before the loop's first call")[0]
    reads = workflow.partition("**Reads: confined for the Claude Code calls")[2].partition("### The draft")[0]
    claude_calls = re.search(r"Every Claude Code call \(([^)]*)\) starts", reads)
    if claude_calls is None:
        found.append("WORKFLOW Reads lacks the Claude Code call list")
    elif re.search(r"\brepair\b", claude_calls[1]):
        found.append("WORKFLOW Reads lists repair among the Claude Code calls")
    for where, rule, needles in (
        (
            "WORKFLOW call settings",
            call_settings,
            (
                "A repair's first two attempts run as Codex calls in the `workspace-write` sandbox",
                "What a repair's Codex call writes is checked and committed by the runner, "
                "including changes outside the change folder",
            ),
        ),
        (
            "WORKFLOW Reads",
            reads,
            (
                "Codex's review, draft and repair calls are not confined in their reads",
                "only the prompt's request bounds them",
                "ADR 0017 retains ADR 0016's residual risks for ignored files, external paths and the git directory",
            ),
        ),
    ):
        for needle in needles:
            if needle not in rule:
                found.append(f"{where} lacks '{needle}'")
    review_docstring = next(
        (
            ast.get_docstring(node) or ""
            for node in ast.parse(runner).body
            if isinstance(node, ast.FunctionDef) and node.name == "review"
        ),
        "",
    )
    review_prompt = texts["prompts/06-review.md"]
    session_rules = {
        "WORKFLOW review bullet": workflow.partition("- `review` —")[2].partition("- `probe` —")[0],
        "06-review Model paragraph": review_prompt.partition("**Model:**")[2].partition("**Input:**")[0],
        "06-review Session paragraph": review_prompt.partition("**Session:**")[2].partition("**Verdict first.**")[0],
        "review() docstring": review_docstring,
    }
    for where, rule in session_rules.items():
        one = flat(rule)
        for needle in (
            "after an earlier `## Phase 6` block",
            "fresh read-only Codex session",
            "The first phase-6 review",
            "recorded Codex phase-2a session",
        ):
            if needle not in one:
                found.append(f"{where} lacks '{needle}'")
    if "Codex repairs the findings the orchestrator takes" not in flat(texts["AGENTS.md"]):
        found.append("AGENTS.md does not name the Codex repair")
    for name in ("prompts/04-implement.md", "prompts/04b-review-loop.md"):
        one = flat(texts[name])
        if "GLM 5.3 (`glm-5.3`)" in one or "gives them to GLM 5.3" in one:
            found.append(f"{name} still routes the repair to GLM")
    if "Codex" not in flat(texts["prompts/04-implement.md"]) or "ADR 0017" not in texts["prompts/04-implement.md"]:
        found.append("the implement prompt does not name the Codex repair")
    remark = " ".join(texts["model-endpoints.yaml"].split())
    if "`glm-5.3` repairs the findings" in remark:
        found.append("an endpoint remark keeps the GLM repair")
    return found


def test_codex_repair_doctrine_and_endpoint_remarks_agree() -> None:
    """Criteria 18 and 20: plant wrong repair routes, confinement claims and phase-6 session rules."""
    paths = [
        "scripts/stage2.py",
        "docs/WORKFLOW.md",
        "AGENTS.md",
        "prompts/04-implement.md",
        "prompts/04b-review-loop.md",
        "prompts/06-review.md",
        "model-endpoints.yaml",
    ]
    texts = {name: (REPO_ROOT / name).read_text(encoding="utf-8") for name in paths}
    assert codex_repair_doctrine_problems(texts) == []
    for name, needle, replacement in (
        ("scripts/stage2.py", "repair       <change>   # Codex", "repair       <change>   # GLM 5.3"),
        ("docs/WORKFLOW.md", "a fresh read-only Codex session", "a session"),
        ("docs/WORKFLOW.md", "The exception (ADR 0017)", "A reviewer never repairs its own findings"),
        ("AGENTS.md", "Codex repairs the findings the orchestrator takes", "GLM 5.3 repairs the findings"),
        ("prompts/04b-review-loop.md", "gives them to Codex in one call", "gives them to GLM 5.3 in one call"),
        ("model-endpoints.yaml", "`glm-5.3` repaired the findings", "`glm-5.3` repairs the findings"),
    ):
        # Match wrapped sentences without flattening away the boundaries of the session rules.
        pattern = r"\s+".join(re.escape(word) for word in needle.split())
        mutated, count = re.subn(pattern, replacement, texts[name], count=1)
        assert count == 1, (name, needle)
        planted = {**texts, name: mutated}
        assert codex_repair_doctrine_problems(planted), (name, needle)
    for needle, replacement, where in (
        ("implement, `spec-review`", "implement, repair, `spec-review`", "WORKFLOW Reads"),
        (
            "A repair's first two attempts run as Codex calls in the `workspace-write` sandbox",
            "A draft's Codex call runs in the `workspace-write` sandbox",
            "WORKFLOW call settings",
        ),
        (
            "A repair's first two attempts run as Codex calls in the `workspace-write` sandbox",
            "A repair's first two attempts run as Codex calls in the read-only sandbox",
            "WORKFLOW call settings",
        ),
        (
            "What a repair's Codex call writes is checked and committed by the runner, "
            "including changes outside the change folder",
            "What such a call writes outside the change folder the runner puts back before it verifies",
            "WORKFLOW call settings",
        ),
        (
            "Codex's review, draft and repair calls are not confined in their reads",
            "Codex's review and draft calls are not confined in their reads",
            "WORKFLOW Reads",
        ),
        ("only the prompt's request bounds them", "the sandbox confines them", "WORKFLOW Reads"),
        (
            "ADR 0017 retains ADR 0016's residual risks for ignored files, external paths and the git directory",
            "ADR 0016's residual risks end",
            "WORKFLOW Reads",
        ),
    ):
        pattern = r"\s+".join(re.escape(word) for word in needle.split())
        mutated, count = re.subn(pattern, replacement, texts["docs/WORKFLOW.md"], count=1)
        assert count == 1, needle
        planted = {**texts, "docs/WORKFLOW.md": mutated}
        assert any(problem.startswith(where) for problem in codex_repair_doctrine_problems(planted)), needle
    for name, start, end, where in (
        ("docs/WORKFLOW.md", "- `review` —", "- `probe` —", "WORKFLOW review bullet"),
        ("prompts/06-review.md", "**Model:**", "**Input:**", "06-review Model paragraph"),
        ("prompts/06-review.md", "**Session:**", "**Verdict first.**", "06-review Session paragraph"),
        ("scripts/stage2.py", "def review(", "    ctx = preflight(", "review() docstring"),
    ):
        before, opening, rest = texts[name].partition(start)
        rule, closing, after = rest.partition(end)
        assert opening and closing, (name, where)
        for needle, replacement in (
            ("after an earlier `## Phase 6` block", "after fixed phase-6 rows"),
            ("fresh read-only Codex session", "recorded Codex phase-2a session"),
            ("The first phase-6 review", "Every phase-6 review"),
        ):
            pattern = r"\s+".join(re.escape(word) for word in needle.split())
            mutated, count = re.subn(pattern, replacement, rule, count=1)
            assert count == 1, (name, where, needle)
            planted = {**texts, name: before + opening + mutated + closing + after}
            assert any(problem.startswith(where) for problem in codex_repair_doctrine_problems(planted)), (
                where,
                needle,
            )
    assert stage2.REPAIR_FORMAT_FILE_TOOLS.count("you cannot run commands") == 1
    assert "you cannot run commands" not in stage2.REPAIR_FORMAT
