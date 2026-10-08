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

GIT = shutil.which("git")  # resolved before any test narrows the PATH

KEY = "sk-zq7Hk2mVw9Xr4Tn8Lb3Pd6Jc1Fy5Ga0"
OKEY = "ok-7Rt2Wm9xQb4Nv6Lc"
LEAK = "LEAKMARK-123456"
DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"
SETTINGS = REPO_ROOT / ".claude" / "settings.json"
VERDICT = "Phase 6 verdict: codex T1, 2026-09-30"

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


def option(flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


config = os.environ.get("CLAUDE_CONFIG_DIR")
prompt_file = option("--append-system-prompt-file")
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
    "prompt_file": Path(prompt_file).read_text() if prompt_file else None,
    "marker_paths": found,
    "findings": findings.read_text() if findings.exists() else None,
}
with log.open("a") as handle:
    handle.write(json.dumps(record) + "\\n")
time.sleep(step.get("sleep", 0))
key = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
for relative, text in step.get("plant", {}).items():
    Path(relative).write_text(text.replace("@KEY@", key))
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


def claude_ok(session: str, answer: str, **more: object) -> dict:
    """A reviewer step that succeeds: the JSON result carries the session id and the answer."""
    return {"stdout": json.dumps({"type": "result", "session_id": session, "result": answer}), **more}


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
    shutil.copy(REPO_ROOT / "model-endpoints.yaml", root / "model-endpoints.yaml")

    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("codex", "claude", "make"):
        program = bin_dir / name
        program.write_text(STAND_IN.replace("@PYTHON@", sys.executable), encoding="utf-8")
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
        codex=[
            codex_ok("T1", rows(2)),
            codex_ok("T1", rows(1)),
            codex_ok("T1", "L1-1: agree\nL1-2: disagree — no test shows it"),
        ],
        claude=[{"stdout": rows(2)}],
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
        for name in ("codex", "claude"):
            program = Path(entry) / name
            if program.is_file():
                found.append(name)
                assert "stage2-stand-in" in program.read_text(encoding="utf-8"), f"{program} is not a stand-in"
    assert sorted(found) == ["claude", "codex"]
    assert Path(shutil.which("codex") or "").parent == world.bin


def test_a_stand_in_contacts_nothing() -> None:
    tree = ast.parse(STAND_IN.replace("@PYTHON@", "python3"))
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
    remark = " ".join(endpoints()["glm-coding-plan"]["bemerkung"].lower().split())
    assert "stage2.py explore" in remark and "stage2.py implement" in remark
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
    world.script(codex=[codex_ok("T1", answer)], claude=[{"stdout": answer}])
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
        ("spec-review", "openai-codex"),
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
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}, {"stdout": "a fact"}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert world.run("explore") == 0
    spec, loop, explorer = (
        world.calls("codex")[0]["env"],
        world.calls("claude")[0]["env"],
        world.calls("claude")[1]["env"],
    )
    for env in (spec, loop, explorer):
        assert "GH_TOKEN" not in env and "OPENAI_API_KEY" not in env and "X_SECRET" not in env
    assert not [name for name in spec if name.startswith("ANTHROPIC_")], "a Codex call carries an Anthropic variable"
    for env in (loop,):
        assert env["ANTHROPIC_BASE_URL"] == stage2.OPENCODE_BASE_URL
        assert env["ANTHROPIC_AUTH_TOKEN"] == OKEY and env["ANTHROPIC_API_KEY"] == OKEY
        assert all(value != KEY for value in env.values()), "an OpenCode Go call carries the GLM key"
        for name in stage2.MODEL_VARIABLES:
            assert env[name] == "deepseek-v4.1-flash"
    assert explorer["ANTHROPIC_BASE_URL"] == stage2.GLM_BASE_URL
    assert explorer["ANTHROPIC_AUTH_TOKEN"] == KEY
    assert all(value != OKEY for value in explorer.values()), "a GLM call carries the OpenCode Go key"
    credentials = [n for n in loop if n.endswith(("_KEY", "_TOKEN", "_SECRET"))]
    assert sorted(credentials) == ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"]


def test_no_call_carries_another_endpoints_key(world: World) -> None:
    """Criterion 13: the OpenCode Go key and the GLM key never meet in one environment."""
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}, {"stdout": "a fact"}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert world.run("explore") == 0
    _spec, loop, explorer = (
        world.calls("codex")[0]["env"],
        world.calls("claude")[0]["env"],
        world.calls("claude")[1]["env"],
    )
    assert all(value != KEY for value in loop.values()), "an OpenCode Go call carries the GLM key"
    assert all(value != OKEY for value in explorer.values()), "a GLM call carries the OpenCode Go key"


@pytest.mark.usefixtures("busy_stdin")
def test_every_call_gets_an_empty_standard_input(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert [call["stdin"] for call in world.calls()] == ["", ""]


def test_the_opencode_key_never_leaves_the_runner(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criteria 11 and 12: the key rides in the environment only - no argv, no stream, no record carries it."""
    said = "| X1 | MAJOR | SPEC | a | b | saw @KEY@ |\n"
    world.script(
        claude=[{"stdout": said, "stderr": "@KEY@", "exit": 0}, {"stdout": said, "stderr": "@KEY@", "exit": 1}]
    )
    assert world.run("review-loop") == 0
    assert world.calls("claude")[0]["env"]["ANTHROPIC_AUTH_TOKEN"] == OKEY
    for call in world.calls():
        assert not any(OKEY[i : i + 8] in " ".join(call["argv"]) for i in range(len(OKEY) - 7)), call["argv"]
    kept = "".join(p.read_text(encoding="utf-8") for p in world.state.rglob("*") if p.is_file())
    shutil.rmtree(world.state)
    assert world.run("review-loop") == 1
    seen = capsys.readouterr()
    everything = seen.out + seen.err + world.text() + kept
    assert "[credential]" in kept
    assert not any(OKEY[i : i + 8] in everything for i in range(len(OKEY) - 7)), "the credential leaked"


def test_every_call_leaves_its_line_in_findings(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    text = world.text()
    day = r"\d{4}-\d{2}-\d{2}"
    count = r"\d+ files, \d+ commits, 1 rules"
    assert re.search(
        rf"^Stage-2 call, {day}: spec-review · endpoint openai-codex · model gpt-6.1-sol · "
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
    world.script(codex=[codex_ok("T1", rows(1))])
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
        codex=[
            codex_ok("T1", rows(1)),
            codex_ok("T1", rows(1)),
            codex_ok("T1", "L1-1: agree"),
        ],
        claude=[{"stdout": rows(1)}],
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
            {"stdout": "fixed"},
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
            {"stdout": "fixed"},
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
            {"stdout": "fixed"},
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
            {"stdout": "fixed"},
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


@pytest.mark.parametrize("verb", [*REVIEW_VERBS, "release-loop"])
def test_stage2_off_is_only_for_work_verbs(world: World, verb: str) -> None:
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
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    assert "updated:" not in world.record().read_text(encoding="utf-8")


def test_a_spec_without_a_bead_refuses(world: World) -> None:
    (world.root / "plans" / "changes" / "demo" / "spec.md").write_text("---\ntitle: Spec\n---\n", encoding="utf-8")
    assert world.run("spec-review") == 2
    assert world.calls() == [] and not world.findings.exists()


def test_every_prompt_asks_to_read_nothing_outside(world: World) -> None:
    full_flow(world)
    codex_prompts = [call["argv"][-1] for call in world.calls("codex")]
    assert len(codex_prompts) == 3
    loop_prompts = [call["prompt_file"] for call in world.calls("claude")]
    for prompt in [*codex_prompts, *loop_prompts]:
        assert prompt.rstrip().endswith(stage2.READ_REQUEST)


# ---------------------------------------------------------------------------
# The reviewer in phases 2a and 6 (criteria 8, 9, 19)
# ---------------------------------------------------------------------------


def test_the_review_loop_launches_claude_on_the_anthropic_address(world: World) -> None:
    """Criterion 8: one launch path for the loop's rounds - the rung as model, effort max, the pinned settings."""
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    assert world.calls("codex") == []
    call = world.calls("claude")[0]
    argv = call["argv"]
    assert argv[0] == "-p"
    assert argv[argv.index("--model") + 1] == "deepseek-v4.1-flash"
    assert argv[argv.index("--effort") + 1] == "max"
    assert set(argv[argv.index("--tools") + 1].split(",")) == {"Read", "Grep", "Glob"}
    assert "--restricted" in argv and "--strict-mcp-config" in argv
    assert argv[argv.index("--permission-mode") + 1] == "dontAsk"
    assert call["env"]["ANTHROPIC_BASE_URL"] == stage2.OPENCODE_BASE_URL
    assert call["env"]["CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT"] == "1"
    assert argv[argv.index("--output-format") + 1] == "text"
    assert "--no-session-persistence" in argv


def test_an_answer_that_is_not_rows_is_kept(world: World) -> None:
    world.script(codex=[codex_ok("T1", "An opening remark.\n" + rows(1)), codex_ok("T2", "No finding at all.")])
    assert world.run("spec-review") == 0
    assert "An opening remark." in world.text() and stage2.NOT_ROWS_NOTE in world.text()
    assert world.run("spec-review") == 0
    assert "No finding at all." in world.text() and "Codex reported no finding." in world.text()


@pytest.mark.parametrize(
    "step",
    [
        {"stdout": '{"type": "turn.completed"}\n', "answer": rows(1)},
        {"stdout": json.dumps({"type": "thread.started", "thread_id": "T9"}) + "\n", "answer": rows(1), "exit": 1},
    ],
    ids=["no-thread-event", "non-zero-exit"],
)
def codex_ok(thread: str, answer: str, **more: object) -> dict:
    """A Codex step that succeeds: a `thread.started` event and the answer file."""
    started = json.dumps({"type": "thread.started", "thread_id": thread})
    return {"stdout": started + '\n{"type": "turn.completed"}\n', "answer": answer, **more}


def test_the_spec_review_answer_lands_as_codex_rows_with_its_session(world: World) -> None:
    world.script(codex=[codex_ok("T-42", rows(3))])
    assert world.run("spec-review") == 0
    text = world.text()
    assert len(re.findall(r"^\| X\d \|.*\| Codex \| open \| — \|$", text, re.M)) == 3
    assert "## Phase 2a — Codex, " in text
    assert re.search(r"^Reviewer session: codex T-42$", text, re.M)
    assert "T-43" not in text


@pytest.mark.parametrize(
    "step",
    [
        {"stdout": '{"type": "turn.completed"}\n', "answer": rows(1)},
        {"stdout": json.dumps({"type": "thread.started", "thread_id": "T9"}) + "\n", "answer": rows(1), "exit": 1},
    ],
    ids=["no-thread-event", "non-zero-exit"],
)
def test_a_failed_codex_call_writes_no_session_line(world: World, step: dict) -> None:
    world.script(codex=[step])
    assert world.run("spec-review") == 1
    text = world.text()
    assert "Reviewer session" not in text and "## Phase 2a" not in text and "X1" not in text


def test_codex_is_pinned_on_first_and_resumed_calls(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", rows(1))])
    assert world.run("spec-review") == 0
    assert world.run("review") == 0
    first, resumed = (call["argv"] for call in world.calls("codex"))
    assert first[:2] == ["exec", "--json"] and resumed[:3] == ["exec", "resume", "T1"]
    for argv in (first, resumed):
        assert argv[argv.index("-m") + 1] == "gpt-6.1-sol"
        assert 'model_reasoning_effort="max"' in argv
        assert 'sandbox_mode="read-only"' in argv
        assert "--ephemeral" not in argv and "-s" not in argv


def test_codex_runs_with_hooks_and_memories_off(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", rows(1))])
    assert world.run("spec-review") == 0
    assert world.run("review") == 0
    for call in world.calls("codex"):
        disabled = [call["argv"][i + 1] for i, word in enumerate(call["argv"]) if word == "--disable"]
        assert sorted(disabled) == ["hooks", "memories"]


def test_the_codex_prompt_carries_its_phase_prompt_in_full(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", rows(1))])
    assert world.run("spec-review") == 0
    assert world.run("review") == 0
    for call, name in zip(world.calls("codex"), ("02a-spec-review.md", "06-review.md"), strict=True):
        prompt = call["argv"][-1]
        assert (REPO_ROOT / "prompts" / name).read_text(encoding="utf-8").rstrip() in prompt
        assert "plans/changes/demo/" in prompt


def test_review_resumes_the_recorded_session(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", rows(1))])
    assert world.run("spec-review") == 0
    assert world.run("review") == 0
    assert world.calls("codex")[1]["argv"][:3] == ["exec", "resume", "T1"]
    text = world.text()
    assert re.search(r"^Phase 6 verdict: codex T1, \d{4}-\d{2}-\d{2}$", text, re.M)
    assert "fresh session" not in text


def test_a_fresh_phase_6_session_says_so(world: World) -> None:
    world.script(codex=[codex_ok("T5", rows(1))])
    assert world.run("review") == 0
    assert world.calls("codex")[0]["argv"][:2] == ["exec", "--json"]
    assert "a fresh session reviewed: no phase-2a session was recorded" in world.text()

    world.findings.unlink()
    (world.bin / "calls.jsonl").unlink()
    world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T2", rows(1))])
    assert world.run("spec-review") == 0
    assert world.run("review") == 0
    assert "a fresh session reviewed: the resume of T1 started a new thread" in world.text()


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
    assert review_prompt_problems(spec_review.replace("gpt-6.1-sol", "gpt"), review)
    assert review_prompt_problems(spec_review.replace("Opus 5.5", "Haiku 4.5"), review)
    assert review_prompt_problems(spec_review, review.replace("Phase 6 verdict:", "Verdict:"))
    assert review_prompt_problems(spec_review, review.replace("release-loop", "release"))
    assert review_prompt_problems(spec_review, review.replace("before you read any loop\nrow", "sometime"))
    assert review_prompt_problems(spec_review, review.replace("scripts/stage2.py", "stage2"))


def test_a_round_calls_its_rung_from_the_entry(world: World) -> None:
    """Criterion 4: round n calls modelle[n-1]; no rung of the ladder stands as a literal in the runner."""
    world.script(claude=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    called = [call["argv"][call["argv"].index("--model") + 1] for call in world.calls("claude")]
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
    world.script(claude=[{"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    called = [call["argv"][call["argv"].index("--model") + 1] for call in world.calls("claude")]
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
    world.script(claude=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    called = [call["argv"][call["argv"].index("--model") + 1] for call in world.calls("claude")]
    assert called == ["spike-a", "spike-b", "spike-c"]


def test_the_reviewer_call_carries_no_user_or_project_configuration(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    call = world.calls("claude")[0]
    config = Path(call["env"]["CLAUDE_CONFIG_DIR"])
    assert call["config_listing"] == []
    assert config != Path(os.environ["HOME"]) / ".claude" and not config.is_relative_to(world.root)
    assert "--restricted" in call["argv"] and "--strict-mcp-config" in call["argv"]
    assert call["env"]["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] == "1"


def test_the_reviewer_call_can_only_read_and_search(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    argv = world.calls("claude")[0]["argv"]
    assert set(argv[argv.index("--tools") + 1].split(",")) <= {"Read", "Grep", "Glob"}
    for word in (
        "--allowedTools",
        "--allowed-tools",
        "acceptEdits",
        "bypassPermissions",
        "--dangerously-skip-permissions",
    ):
        assert word not in argv
    assert argv[argv.index("--permission-mode") + 1] == "dontAsk"


def test_the_reviewer_prompt_carries_the_loop_prompt_and_the_uncommitted_diff(world: World) -> None:
    (world.root / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
    (world.root / "src" / "new.py").write_text("fresh = 'untracked-content'\n", encoding="utf-8")
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    prompt = world.calls("claude")[0]["prompt_file"]
    assert (REPO_ROOT / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8").rstrip() in prompt
    assert "+value = 2" in prompt and "-value = 1" in prompt
    assert "src/new.py" in prompt and "untracked-content" in prompt


def test_a_round_is_written_as_its_rung(world: World) -> None:
    """Criterion 18: the heading, the Reviewer cell and the record's place carry the rung, outside the worktree."""
    world.script(claude=[{"stdout": rows(2)}])
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
    world.script(claude=[{"stdout": rows(1), "stderr": "boom", "exit": 1}])
    assert world.run("review-loop") == 1
    assert not world.record().exists()
    assert "claude call failed" in capsys.readouterr().err


def test_a_round_without_a_finding_still_counts(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """A round that reports no finding is a round; two of them stop the loop before round 3 (criterion 7)."""
    world.script(claude=[{"stdout": "Nothing to report."}, {"stdout": "Still nothing."}])
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    assert "deepseek-v4.1-flash reported no finding." in record
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    assert "mimo-v2.6-flash reported no finding." in record
    capsys.readouterr()
    assert world.run("review-loop") == 2
    assert "round 2 wrote no taken row; the loop stops at 2." in capsys.readouterr().err
    assert len(world.calls("claude")) == 2


@pytest.mark.parametrize(
    "step",
    [{"stdout": "partial", "stderr": "boom", "exit": 1}, {"stdout": "  \n", "exit": 0}],
    ids=["non-zero-exit", "empty-answer"],
)
def test_a_call_without_an_answer_is_not_a_round(world: World, step: dict) -> None:
    """Criterion 14: a failed call, or one with no answer at all, writes no round; the loop itself still runs to three."""
    world.script(claude=[step, step, {"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 1
    assert world.run("review-loop") == 1
    assert not world.record().exists()
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    assert world.run("review-loop") == 2
    assert len(world.calls("claude")) == 5


@pytest.mark.parametrize("verb", ["review-loop", "probe"])
def test_the_loop_refuses_without_the_key(world: World, verb: str) -> None:
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    assert world.run(verb) == 2
    assert world.calls() == []


def test_the_loop_stops_at_three_rounds(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 6: three rounds run; the fourth is refused, also after the release."""
    world.script(claude=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    decide_record(world)
    assert world.run("review-loop") == 0
    assert len(world.calls("claude")) == 3
    decide_record(world)
    capsys.readouterr()
    assert world.run("review-loop") == 2
    assert "3 rounds have run; the loop stops at 3." in capsys.readouterr().err
    assert len(world.calls("claude")) == 3
    # also after the release: the rounds stay counted
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert not world.record().exists()
    assert world.run("review-loop") == 2
    assert len(world.calls("claude")) == 3


def test_round_three_starts_only_after_a_taken_row(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 7: rounds 1 and 2 run as today; round 3 only when round 2 wrote at least one taken row."""
    world.script(claude=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — out of scope")
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — no evidence")
    capsys.readouterr()
    assert world.run("review-loop") == 2
    assert "round 2 wrote no taken row; the loop stops at 2." in capsys.readouterr().err
    assert len(world.calls("claude")) == 2
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
    called = [call["argv"][call["argv"].index("--model") + 1] for call in world.calls("claude")]
    assert called == ["deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"]


def test_a_call_over_the_time_limit_is_stopped(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 15: a call that outlasts the limit is stopped, and stopping is one of criterion 14's causes."""
    assert stage2.REVIEWER_MINUTES == 30
    monkeypatch.setattr(stage2, "REVIEWER_MINUTES", 0.03)
    world.script(claude=[{"stdout": "too late", "sleep": 30}])
    started = time.monotonic()
    assert world.run("review-loop") == 1
    assert time.monotonic() - started < 15
    assert not world.record().exists()
    assert "stopped by the reviewer time limit" in capsys.readouterr().err


def test_a_refused_rung_stops_the_run_without_fallback(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 17: an address that refuses a rung stops the run - no second address, no other rung, no other endpoint."""
    world.script(claude=[{"stdout": "refused: unknown model", "stderr": "404", "exit": 1}, {"stdout": "must not run"}])
    assert world.run("review-loop") == 1
    calls = world.calls("claude")
    assert len(calls) == 1
    assert calls[0]["argv"][calls[0]["argv"].index("--model") + 1] == "deepseek-v4.1-flash"
    assert calls[0]["env"]["ANTHROPIC_BASE_URL"] == stage2.OPENCODE_BASE_URL
    assert "chat/completions" not in calls[0]["env"]["ANTHROPIC_BASE_URL"]
    assert not world.record().exists()
    assert "claude call failed" in capsys.readouterr().err


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
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 2
    assert world.calls() == []


def released_rows(text: str) -> list[list[str]]:
    """The cells of every row of the released block, whatever the row."""
    block = text[text.rfind(stage2.RELEASE_HEADING) :]
    return [c for c in (stage2.split_row(line) for line in block.splitlines()) if c and c[0].startswith("L")]


def test_a_pipe_inside_a_reviewers_finding_reaches_findings(world: World) -> None:
    """Repair round 1, F-2 (a): a shell pipe in a finding is part of the finding, not a seventh cell."""
    said = "| X1 | MAJOR | SPEC | a | src/app.py:1 | the filter `cat x | sort` drops the last row |"
    world.script(claude=[{"stdout": said}])
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
    world.script(claude=[{"stdout": answer}])
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
    world.script(claude=[{"stdout": rows(1) + "\n" + "\n".join(REVIEWER_PROSE) + "\n"}])
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
    world.script(claude=[{"stdout": answer}])
    assert world.run("review-loop") == 0
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert answer in world.text()
    assert "# Loop record" not in world.text() and "## Round 1 — deepseek" not in world.text()


def test_a_reviewers_lines_that_look_like_the_records_own_text_are_carried(world: World) -> None:
    """Repair round 2, F-10: the intro sentences are the runner's only where the runner wrote them."""
    world.script(claude=[{"stdout": stage2.RECORD_INTRO}])
    assert world.run("review-loop") == 0
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    lines = world.text().splitlines()
    for line in stage2.RECORD_INTRO.splitlines():
        assert line in lines, line


def test_a_rounds_words_do_not_swallow_the_rows_of_the_next(world: World) -> None:
    """Repair round 2: one round's words end at the next round heading; round 2's rows are read, round 1's words carried."""
    world.script(
        claude=[{"stdout": rows(1) + "\nA remark of round 1."}, {"stdout": rows(1) + "\nA remark of round 2."}]
    )
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
        world.script(codex=[codex_ok("T1", rows(1)), codex_ok("T1", "L1-1: agree")], claude=[{"stdout": said}])
    elif verb == "review-loop":
        world.script(claude=[{"stdout": said}, {"stdout": "Nothing to report."}])
    else:
        world.script(claude=[{"stdout": said}])
    assert world.run("review-loop") == 0
    decide_record(world)
    if verb == "release-loop":
        world.write_findings(VERDICT)
    capsys.readouterr()
    assert world.run(verb) == 0, capsys.readouterr().err
    if verb == "review-loop":
        assert "## Round 2 — mimo-v2.6-flash, " in world.record().read_text(encoding="utf-8")
        return
    text = world.text()
    assert "| L1-1 | still open from the last round |" in text.splitlines()
    assert [r[0] for r in released_rows(text) if len(r) == 10] == ["L1-1"]
    assert not world.record().exists()


def test_a_damaged_row_of_the_record_still_refuses_beside_reviewer_text(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    """Repair round 2, F-11: the record's own rows are held to the rule even when the reviewer's text stands below them."""
    world.script(claude=[{"stdout": rows(2) + "\n| L1-1 | still open |\n"}])
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
    "2a Spec review": "gpt-6.1-sol",
    "4 Implement": "GLM 5.3 Flash",
    "4b Review loop": "deepseek-v4.1-flash",
    "6 Review": "gpt-6.1-sol",
}


def routing_problems(workflow: str) -> list[str]:
    """What the routing rows of the doctrine get wrong: section 4's five rows and section 3's two."""
    found = []
    stage2_rows = routing_rows(section(workflow, "## 4 · "))
    for phase, model in STAGE2_ROUTING.items():
        row = stage2_rows.get(phase)
        if row is None:
            found.append(f"section 4 has no routing row {phase}")
        elif row[0] != model:
            found.append(f"section 4 routes {phase} to {row[0]}, not {model}")
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
    """Criterion 21: 4b rides the ladder, 2a and 6 stay Codex, 1 and 4 stay on GLM 5.3 Flash; a spike gets no stage 2."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert routing_problems(text) == []
    assert class_table_problems(text) == []
    four = routing_rows(section(text, "## 4 · "))
    for needle in (
        "round 1 `deepseek-v4.1-flash`",
        "round 2 `mimo-v2.6-flash`",
        "round 3 `mimo-v2.6-pro`",
        "modelle[n-1]",
        "round 3 only when round 2 wrote a taken row",
    ):
        assert needle in four["4b Review loop"][1], needle
    for phase in ("2a Spec review", "6 Review"):
        assert four[phase][0] == "gpt-6.1-sol", phase
    for old, new in (
        ("| 2a Spec review | **gpt-6.1-sol** |", "| 2a Spec review | **Opus 5.5** |"),
        ("| 4b Review loop | **deepseek-v4.1-flash** |", "| 4b Review loop | **GLM 5.3** |"),
        ("| 6 Review | **gpt-6.1-sol** |", "| 6 Review | **Opus 5.5** |"),
        ("| 1 Explore | **GLM 5.3 Flash** |", "| 1 Explore | **Haiku 4.5** |"),
        ("| 4 Implement | **GLM 5.3 Flash** |", "| 4 Implement | **Sonnet 5.5** |"),
        ("| `bounded` | Codex, where one is held | the ladder |", "| `bounded` | the ladder | the ladder |"),
        ("| a one-sentence change, a `spike` | no stage 2 |", "| a one-sentence change, a `spike` | the ladder |"),
    ):
        assert old in text, old
        changed = text.replace(old, new, 1)
        assert routing_problems(changed) or class_table_problems(changed), (old, new)


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
    found = []
    for name, text in (("02a-spec-review.md", spec_review), ("06-review.md", review)):
        one = flat(text)
        for needle in ("gpt-6.1-sol", "Opus 5.5", "scripts/stage2.py"):
            if needle not in one:
                found.append(f"{name} lacks {needle}")
    if "stage2.py spec-review <change>" not in flat(spec_review):
        found.append("02a-spec-review.md does not name the verb spec-review")
    one = flat(review)
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
    """The class table: a change's loop rides the ladder, its two reviews stay Codex, a spike gets none."""
    found = []
    rows = {
        line.split("|")[1].strip(): [cell.strip() for cell in line.split("|")[2:-1]]
        for line in section(workflow, "### Which change gets what").splitlines()
        if line.startswith("| ") and not line.startswith("| Change") and not line.startswith("|---")
    }
    bounded = rows.get("`bounded`")
    if bounded is None or len(bounded) != 3:
        return ["the class table has no `bounded` row of three cells"]
    if not bounded[0].startswith("Codex") or not bounded[1].startswith("the ladder"):
        found.append("the class table does not send a change's 2a to Codex and its 4b to the ladder")
    if not bounded[2].startswith("Codex"):
        found.append("the class table does not keep phase 6 with Codex")
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
    return found


def test_agents_md_names_the_loop_and_the_runner() -> None:
    text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert agents_md_problems(text) == []
    assert text.count("\n") <= 200
    row = next(line for line in text.splitlines() if line.startswith("| 4b |"))
    assert agents_md_problems(text.replace(row + "\n", ""))
    assert agents_md_problems(text.replace("only through", "also through"))
    assert agents_md_problems(text.replace("round 3 only when round 2 wrote a taken row", "round 3 as needed"))


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


def test_the_stop_rule_counts_every_rung() -> None:
    """Criterion 24: the measurement counts a taken finding of any rung, not only the two former reviewers."""
    four = flat(section(WORKFLOW.read_text(encoding="utf-8"), "## 4 · "))
    assert "a taken finding of a rung counts like a Codex or GLM finding counted before 2026-10-07" in four
    assert "taken Codex or GLM finding broke a test" not in four


def test_the_adr_draft_states_every_point() -> None:
    """Criterion 25: the draft in design.md carries the six points and the weighed options, ready to copy out."""
    draft = section((REPO_ROOT / "plans/changes/stage2-mimo/design.md").read_text(encoding="utf-8"), "### ADR 0011")
    assert draft, "the draft is not in design.md"
    one = flat(draft)
    for needle in (
        "Framework content may also go to `opencode-go`",
        "through Claude Code",
        "The review loop (4b) only",
        "The loop's reviewer role moves",
        "the spec review and the review stay with Codex",
        "explore and implement stay on GLM 5.3 Flash",
        "The ladder is data, not code",
        "modelle[n-1]",
        "one-line pull request",
        "at most three rounds",
        "The unconfined reads accepted for ADR 0007's reviewers extend to the rungs",
        "Keep Codex and GLM in every review role",
        "An OpenCode product other than Go",
        "OpenCode's own CLI as the launcher",
        "The model of round 2",
        "runde 2 flash",
    ):
        assert needle in one, needle


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
