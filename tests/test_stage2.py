"""The runner of stage 2 and what it declares - and the cases in which it holds.

`scripts/stage2.py` is the only way this repository starts a foreign reviewer.
Every case here runs it in-process against a temporary repository and two
stand-ins: programs named `codex` and `claude` that record their arguments,
environment and input, print canned output and contact nothing. No test starts
a real Codex, a real Claude Code against a model endpoint, or reads the
maintainer's real denylist, secrets or loop record.

Each test comes with its fault: the mutation list of the plan's slice 2 was
planted one by one and each one turned a test here red.
"""

from __future__ import annotations

import ast
import copy
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

import leakcheck  # noqa: E402
import omnigent_policy  # noqa: E402
import plans_registry  # noqa: E402
import stage2  # noqa: E402

GIT = shutil.which("git")  # resolved before any test narrows the PATH

KEY = "sk-zq7Hk2mVw9Xr4Tn8Lb3Pd6Jc1Fy5Ga0"
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
for relative, text in step.get("plant", {}).items():
    Path(relative).write_text(text)
key = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
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

    def run(self, verb: str, change: str | None = "demo") -> int:
        argv = [verb] if change is None else [verb, change]
        return stage2.main([*argv, "--root", str(self.root)])

    @property
    def findings(self) -> Path:
        return self.root / "plans" / "changes" / "demo" / "findings.md"

    def text(self) -> str:
        return self.findings.read_text(encoding="utf-8")

    def record(self) -> Path:
        return self.state / "coding-harness" / "stage2" / "demo" / "loop.md"

    def write_record(self, decided: list[tuple[str, str, str]], finding: str = "") -> None:
        """A loop record of one round whose rows carry the given (id, status, broke a test)."""
        rows_ = [
            [
                ident,
                "MAJOR",
                "MAINT",
                "impl",
                "src/app.py:1",
                f"finding of {ident} {finding}".strip(),
                "GLM",
                status,
                broke,
            ]
            for ident, status, broke in decided
        ]
        directory = self.record().parent
        directory.mkdir(parents=True, exist_ok=True)
        self.record().write_text(
            f"# Loop record — demo\n\n{stage2.RECORD_INTRO}\n\n## Round 1 — GLM, 2026-09-30\n\n"
            f"{stage2.render_table(stage2.ROW_COLUMNS, rows_)}\n",
            encoding="utf-8",
        )

    def write_findings(self, *lines: str) -> None:
        self.findings.write_text("# Findings — demo\n\n" + "\n\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    """A repository, two stand-ins and an environment that belong to the test."""
    root = tmp_path / "repo"
    (root / "plans" / "changes" / "demo").mkdir(parents=True)
    (root / "plans" / "changes" / "demo" / "spec.md").write_text(
        "---\ntitle: Spec\nbead: demo-1\n---\n\n# Spec\n", encoding="utf-8"
    )
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("value = 1\n", encoding="utf-8")
    shutil.copytree(REPO_ROOT / "prompts", root / "prompts")
    shutil.copy(REPO_ROOT / "model-endpoints.yaml", root / "model-endpoints.yaml")

    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("codex", "claude"):
        program = bin_dir / name
        program.write_text(STAND_IN.replace("@PYTHON@", sys.executable), encoding="utf-8")
        program.chmod(0o755)
    git_dir = tmp_path / "gitbin"
    git_dir.mkdir()
    (git_dir / "git").symlink_to(GIT)
    (tmp_path / "denylist.txt").write_text(DENYLIST, encoding="utf-8")
    (tmp_path / "secrets.env").write_text(f"# keys\nexport GLM_KEY='{KEY}'\nOTHER=1\n", encoding="utf-8")

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
    match = re.search(r"^## Phase 6 — Codex.*?^Phase 6 verdict: [^\n]*$", text, re.M | re.S)
    assert match, "no verdict block"
    return match.group(0)


def full_flow(w: World) -> None:
    """spec-review, one GLM round decided, the verdict, the release and the marks."""
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
    assert imported <= {"json", "os", "sys", "pathlib"}


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
# The endpoint declaration (criteria 4, 5, 7)
# ---------------------------------------------------------------------------


def test_openai_codex_is_declared_as_decided() -> None:
    codex = endpoints()["openai-codex"]
    assert codex["betreiber"] == "OpenAI"
    assert codex["residenz"] == "anbieter-erklaert"
    assert codex["abrechnung"] == "abonnement"
    assert codex["darf_sehen"] == ["framework"]
    assert codex["modelle"] == ["gpt-6.1-sol"]
    remark = codex["bemerkung"]
    assert "Codex CLI" in remark and "2a" in remark and "6" in remark and "United States" in remark


def test_kimi_is_excluded_not_declared() -> None:
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    for endpoint in data["endpunkte"]:
        text = json.dumps(endpoint).lower()
        assert "moonshot" not in text and "kimi-for-coding" not in text and not re.search(r"\bk3\b", text)
    kimi = [entry for entry in data["ausgeschlossen"] if "Kimi" in entry["was"]]
    assert len(kimi) == 1
    assert "2026-09-30" in kimi[0]["grund"] and "maintainer" in kimi[0]["grund"]


def test_the_glm_remark_names_the_review_loop() -> None:
    remark = endpoints()["glm-coding-plan"]["bemerkung"].lower()
    assert "review loop" in remark and "phase 4b" in remark
    for word in ("implement", "umsetzung", "marking"):
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
    for verb in ("spec-review", "review", "review-loop"):
        assert world.run(verb) == 2
    assert world.calls() == []
    assert not world.findings.exists()


def test_each_call_runs_its_own_leak_check(world: World) -> None:
    world.write_record([("L1-1", "taken — test_a", "no")])
    world.script(codex=[codex_ok("T1", rows(1), plant={"leak.txt": LEAK}), codex_ok("T1", "L1-1: agree")])
    assert world.run("review") == 2
    assert len(world.calls("codex")) == 1, "the mark call started on the first call's check"


@pytest.mark.parametrize(
    ("verb", "endpoint"), [("spec-review", "openai-codex"), ("review-loop", "glm-coding-plan")], ids=["codex", "glm"]
)
@pytest.mark.parametrize("fault", ["missing", "no-model", "no-framework", "no-residency"])
def test_an_endpoint_the_declaration_does_not_clear_refuses(world: World, verb: str, endpoint: str, fault: str) -> None:
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
    assert world.run(verb) == 2
    assert world.calls() == []


def test_the_foreign_environment_is_the_runners(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    codex, claude = world.calls("codex")[0]["env"], world.calls("claude")[0]["env"]
    for env in (codex, claude):
        assert "GH_TOKEN" not in env and "OPENAI_API_KEY" not in env and "X_SECRET" not in env
    assert not [name for name in codex if name.startswith("ANTHROPIC_")]
    assert claude["ANTHROPIC_BASE_URL"] == stage2.GLM_BASE_URL
    assert claude["ANTHROPIC_AUTH_TOKEN"] == KEY and claude["ANTHROPIC_API_KEY"] == KEY
    for name in stage2.GLM_MODEL_VARIABLES:
        assert claude[name] == "glm-5.3"
    credentials = [n for n in claude if n.endswith(("_KEY", "_TOKEN", "_SECRET"))]
    assert sorted(credentials) == ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"]


@pytest.mark.usefixtures("busy_stdin")
def test_every_call_gets_an_empty_standard_input(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    assert [call["stdin"] for call in world.calls()] == ["", ""]


def test_the_glm_credential_never_leaves_the_runner(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    said = "| X1 | MAJOR | SPEC | a | b | saw @KEY@ |\n"
    world.script(
        claude=[{"stdout": said, "stderr": "@KEY@", "exit": 0}, {"stdout": said, "stderr": "@KEY@", "exit": 1}]
    )
    assert world.run("review-loop") == 0
    kept = "".join(p.read_text(encoding="utf-8") for p in world.state.rglob("*") if p.is_file())
    shutil.rmtree(world.state)
    assert world.run("review-loop") == 1
    seen = capsys.readouterr()
    everything = seen.out + seen.err + world.text() + kept
    assert "[credential]" in kept
    assert not any(KEY[i : i + 8] in everything for i in range(len(KEY) - 7)), "the credential leaked"


def test_every_call_leaves_its_line_in_findings(world: World) -> None:
    world.script(codex=[codex_ok("T1", rows(1))], claude=[{"stdout": rows(1)}])
    assert world.run("spec-review") == 0
    assert world.run("review-loop") == 0
    text = world.text()
    day = r"\d{4}-\d{2}-\d{2}"
    count = r"\d+ files, \d+ commits, 1 rules"
    assert re.search(
        rf"^Stage-2 call, {day}: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over {count}\.$",
        text,
        re.M,
    )
    assert re.search(
        rf"^Stage-2 call, {day}: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over {count}\.$",
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


def test_a_spec_without_a_bead_refuses(world: World) -> None:
    (world.root / "plans" / "changes" / "demo" / "spec.md").write_text("---\ntitle: Spec\n---\n", encoding="utf-8")
    assert world.run("spec-review") == 2
    assert world.calls() == [] and not world.findings.exists()


def test_every_prompt_asks_to_read_nothing_outside(world: World) -> None:
    full_flow(world)
    codex_prompts = [call["argv"][-1] for call in world.calls("codex")]
    assert len(codex_prompts) == 3
    glm_prompts = [call["prompt_file"] for call in world.calls("claude")]
    for prompt in [*codex_prompts, *glm_prompts]:
        assert prompt.rstrip().endswith(stage2.READ_REQUEST)


# ---------------------------------------------------------------------------
# Codex in phases 2a and 6 (criteria 23-31)
# ---------------------------------------------------------------------------


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


def test_the_spec_review_answer_lands_as_codex_rows_with_its_session(world: World) -> None:
    world.script(codex=[codex_ok("T-42", rows(3))])
    assert world.run("spec-review") == 0
    text = world.text()
    assert len(re.findall(r"^\| X\d \|.*\| Codex \| open \| — \|$", text, re.M)) == 3
    assert "## Phase 2a — Codex, " in text
    assert re.search(r"^Reviewer session: codex T-42$", text, re.M)
    assert "T-43" not in text


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
def test_a_failed_codex_call_writes_no_session_line(world: World, step: dict) -> None:
    world.script(codex=[step])
    assert world.run("spec-review") == 1
    text = world.text()
    assert "Reviewer session" not in text and "## Phase 2a" not in text and "X1" not in text


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


def test_the_glm_call_goes_to_zai_with_glm_5_3_at_max(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    call = world.calls("claude")[0]
    argv = call["argv"]
    assert argv[0] == "-p" and argv[argv.index("--model") + 1] == "glm-5.3"
    assert argv[argv.index("--effort") + 1] == "max"
    assert call["env"]["ANTHROPIC_BASE_URL"] == "https://api.z.ai/api/anthropic"
    assert call["env"]["ANTHROPIC_MODEL"] == "glm-5.3"


def test_the_glm_call_carries_no_user_or_project_configuration(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    call = world.calls("claude")[0]
    config = Path(call["env"]["CLAUDE_CONFIG_DIR"])
    assert call["config_listing"] == []
    assert config != Path(os.environ["HOME"]) / ".claude" and not config.is_relative_to(world.root)
    assert "--restricted" in call["argv"] and "--strict-mcp-config" in call["argv"]
    assert call["env"]["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] == "1"


def test_the_glm_call_can_only_read_and_search(world: World) -> None:
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


def test_the_glm_prompt_carries_the_loop_prompt_and_the_uncommitted_diff(world: World) -> None:
    (world.root / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
    (world.root / "src" / "new.py").write_text("fresh = 'untracked-content'\n", encoding="utf-8")
    world.script(claude=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    prompt = world.calls("claude")[0]["prompt_file"]
    assert (REPO_ROOT / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8").rstrip() in prompt
    assert "+value = 2" in prompt and "-value = 1" in prompt
    assert "src/new.py" in prompt and "untracked-content" in prompt


def test_a_round_lands_in_the_loop_record_not_the_worktree(world: World) -> None:
    world.script(claude=[{"stdout": rows(2)}])
    assert world.run("review-loop") == 0
    expected = Path(os.environ["XDG_STATE_HOME"]) / "coding-harness" / "stage2" / "demo" / "loop.md"
    text = expected.read_text(encoding="utf-8")
    assert "## Round 1 — GLM, " in text
    ids = [
        cells[0] for cells in (stage2.split_row(line) for line in text.splitlines()) if cells and cells[0][:1] == "L"
    ]
    assert ids == ["L1-1", "L1-2"]
    assert all(cells[6] == "GLM" for cells in stage2.record_rows(text))
    for path in world.root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            assert "FB1-unique-body" not in path.read_text(encoding="utf-8", errors="replace"), path
    assert not list(world.root.rglob("loop.md"))
    assert "GLM" not in world.text()


def test_a_failed_glm_call_writes_nothing(world: World) -> None:
    world.script(claude=[{"stdout": rows(1), "stderr": "boom", "exit": 1}])
    assert world.run("review-loop") == 1
    assert not world.record().exists()


def test_a_round_without_a_finding_still_counts(world: World) -> None:
    world.script(claude=[{"stdout": "Nothing to report."}, {"stdout": "Still nothing."}, {"stdout": "x"}])
    assert world.run("review-loop") == 0
    assert "GLM reported no finding." in world.record().read_text(encoding="utf-8")
    assert world.run("review-loop") == 0
    assert world.run("review-loop") == 2
    assert len(world.calls("claude")) == 2


def test_the_loop_refuses_without_the_key(world: World) -> None:
    Path(os.environ["CC_SECRETS"]).write_text("OTHER=1\n", encoding="utf-8")
    assert world.run("review-loop") == 2
    assert world.calls() == []


def test_a_third_round_is_refused(world: World) -> None:
    world.script(claude=[{"stdout": rows(1)}, {"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    world.write_record([("L1-1", "taken — test_a", "no")])
    assert world.run("review-loop") == 0
    assert len(world.calls("claude")) == 2
    # the rows of both rounds are decided, the third is refused
    text = world.record().read_text(encoding="utf-8")
    world.record().write_text(
        re.sub(r"^(\| L2-1 \|.*)\|  \|  \|$", r"\1| rejected — no evidence |  |", text, flags=re.M), encoding="utf-8"
    )
    assert world.run("review-loop") == 2
    assert len(world.calls("claude")) == 2
    # also after the release: the rounds stay counted
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert not world.record().exists()
    assert world.run("review-loop") == 2
    assert len(world.calls("claude")) == 2


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


def test_release_carries_every_row_with_its_marks(world: World) -> None:
    world.write_record(
        [("L1-1", "taken — test_a", "yes"), ("L1-2", "rejected — out of scope", ""), ("L1-3", "taken — crit 4", "no")]
    )
    world.write_findings("## Phase 6 — Codex, 2026-09-30", VERDICT)
    assert world.run("release-loop") == 0
    text = world.text()
    assert "## Phase 4b — GLM loop rows, released " in text and re.search(r"^Rounds run: 1$", text, re.M)
    released = [
        cells for cells in (stage2.split_row(line) for line in text.splitlines()) if cells and cells[0][:3] == "L1-"
    ]
    assert [(c[0], c[6], c[7], c[8], c[9]) for c in released] == [
        ("L1-1", "GLM", "taken — test_a", "yes", "—"),
        ("L1-2", "GLM", "rejected — out of scope", "", "—"),
        ("L1-3", "GLM", "taken — crit 4", "no", "—"),
    ]
    assert not world.record().exists()


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
