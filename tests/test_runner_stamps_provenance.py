"""The runner stamps the actual producer of retained model work and checks touched headers.

The routes of explore, draft and repair write the real producing program, model and publication
day into every retained artifact before their post-run checks read it (spec criteria 1-3); one
shared check judges producer records, provenance and review against the committed baseline for
every file a run touched, implement included (criterion 4); committed records keep their bytes
(criterion 7) and approvals reset only when the document body changed (criteria 8 and 9).
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402


def test_block_sequence_retains_prior_record_bytes():
    field = '\n- {kind: llm-session, name: codex, version: "2026-11-04"}'
    earlier = stage2.parse_producer_records(field, "test")
    added = {"kind": "llm-session", "name": "pi", "version": "2026-11-05"}
    result = stage2.retained_producer_field(field, [*earlier, added])
    assert result.startswith(field + "\n")
    assert yaml.safe_load(result) == [*earlier, added]


def test_header_added_to_committed_headerless_file_is_new():
    current = (
        b"---\nprovenance: ai-drafted-reviewed\n"
        b"review: {status: pending, approved_by: null, approved_at: null}\n---\nBody\n"
    )
    assert stage2.header_problems("plans/example.md", b"Body\n", current) == []


SPEC_SEED = (
    "---\n"
    'title: "Spec — demo"\n'
    "status: draft\n"
    "date: 2026-11-10\n"
    "last_reviewed: 2026-11-10\n"
    "updated: 2026-11-10\n"
    "supersedes: null\n"
    "superseded_by: null\n"
    "bead: demo-1\n"
    "owner: framework-architect\n"
    "provenance: ai-drafted-reviewed\n"
    'produced_by: {kind: llm-session, name: codex, version: "2026-11-10", model: "gpt-6.1-terra"}\n'
    'review: {status: approved, approved_by: "Michael Peichl", approved_at: 2026-11-12}\n'
    "tags: [spec]\n"
    "---\n"
    "\n"
    "# Spec — demo\n"
    "\n"
    "The problem and the acceptance criteria stand here.\n"
)

PLAN_SEED = (
    "---\n"
    'title: "Plan — demo"\n'
    "status: draft\n"
    "date: 2026-11-10\n"
    "last_reviewed: 2026-11-10\n"
    "updated: 2026-11-10\n"
    "supersedes: null\n"
    "superseded_by: null\n"
    "bead: demo-1\n"
    "owner: framework-architect\n"
    "provenance: ai-drafted-reviewed\n"
    'produced_by: {kind: llm-session, name: codex, version: "2026-11-10", model: "gpt-6.1-terra"}\n'
    "review: {status: pending, approved_by: null, approved_at: null}\n"
    "tags: [plan]\n"
    "---\n"
    "\n"
    "# Plan — demo\n"
    "\n"
    "## Files and steps\n"
    "\n"
    "1. Do the thing.\n"
    "\n"
    "## Time used\n"
)

RESEARCH_SEED = (
    "---\n"
    'title: "Research — demo"\n'
    "status: draft\n"
    "date: 2026-11-17\n"
    "last_reviewed: 2026-11-17\n"
    "updated: 2026-11-17\n"
    "supersedes: null\n"
    "superseded_by: null\n"
    "bead: demo-1\n"
    "owner: framework-architect\n"
    "provenance: human-written\n"
    "class: bounded\n"
    'review: {status: approved, approved_by: "Michael Peichl", approved_at: 2026-11-17}\n'
    "tags: [research]\n"
    "---\n"
    "\n"
    "# Research — demo\n"
    "\n"
    "Authored skeleton notes name AGENTS.md as the standing rule.\n"
)

PENDING_REVIEW = "{status: pending, approved_by: null, approved_at: null}"
APPROVED_REVIEW = '{status: approved, approved_by: "Michael Peichl", approved_at: 2026-11-12}'
BROKEN_NOTE = (
    "---\n"
    'title: "Broken note"\n'
    "defaults: &shape {status: draft}\n"
    "status: *shape\n"
    f"review: {PENDING_REVIEW}\n"
    "tags: [note]\n"
    "---\n"
    "\n"
    "# Broken note\n"
    "\n"
    "A note the draft kept.\n"
)


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git_env() -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key not in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, env=_git_env(), check=True)
    return done.stdout.strip()


def _commit_file(root: Path, relative: str, text: str, message: str = "seed an artifact") -> None:
    _write(root, relative, text)
    _git(root, "add", "-A")
    _git(
        root,
        "-c",
        "user.name=tester",
        "-c",
        "user.email=tester@example.com",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-m",
        message,
    )


def _header_of(text: str) -> dict:
    return yaml.safe_load(re.match(r"\A---\n(.*?)\n---", text, re.S).group(1))


def _records(value) -> list:
    """The producer records of a `produced_by` value: one record is a mapping, several a list."""
    return value if isinstance(value, list) else [value]


def _header_at(root: Path, relative: str) -> dict:
    return _header_of((root / relative).read_text(encoding="utf-8"))


def _ctx(root: Path) -> stage2.Context:
    return stage2.Context(root, "demo", root / "plans/changes/demo", "demo-1")


def _build_prompt(ctx: stage2.Context):
    def build(_diagnostics, _endpoint, inputs):
        stage2.prompt_input(ctx.folder / "spec.md", inputs)
        stage2.prompt_input(ctx.plan, inputs)
        return f"{ctx.change} work prompt"

    return build


class _CallResult:
    files = commits = rules = 1


@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    folder = root / "plans" / "changes" / "demo"
    folder.mkdir(parents=True)
    _write(root, "plans/changes/demo/research.md", RESEARCH_SEED)
    _write(root, "plans/changes/demo/spec.md", SPEC_SEED)
    _write(root, "plans/changes/demo/plan.md", PLAN_SEED)
    _write(root, "plans/changes/demo/decisions.md", "# Decisions\n\nNo records yet.\n")
    _write(root, "AGENTS.md", "# Agent rules\n\nStay inside the worktree.\n")
    _write(root, "provenance.yaml", "paths: []\n")
    root_prompts = root / "prompts"
    root_prompts.mkdir()
    for name in ("01-explore.md", "02-spec.md", "02b-design.md", "03-plan.md", "04-implement.md"):
        _write(root, f"prompts/{name}", f"# {name}\n\nWork on the change.\n")
    _git(root, "init", "-q", "-b", "main")
    _commit_file(root, "plans/changes/demo/research.md", RESEARCH_SEED, "seed the change")
    _git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setattr(stage2, "declaration_problem", lambda *_a, **_k: None)
    monkeypatch.setattr(stage2, "subscription_terms_warnings", lambda *_a, **_k: None)
    monkeypatch.setattr(stage2, "checked_prompt", lambda *_a, **_k: _CallResult())
    monkeypatch.setattr(stage2, "read_secret", lambda *_a, **_k: "runner-test-key")
    return root


def test_explore_stamps_actual_producer(repo, monkeypatch):
    day = stage2.today()
    monkeypatch.setattr(
        stage2,
        "run_work_model",
        lambda *_a, **_k: "Facts: the runner reads AGENTS.md before any call.",
    )
    stage2.explore(repo, "demo")
    header = _header_at(repo, "plans/changes/demo/research.md")
    assert _records(header["produced_by"]) == [
        {"kind": "llm-session", "name": "claude-code", "version": day, "model": "glm-5.3-flash"}
    ], "a GLM route must record its own program, model and publication day, never codex or another day"


def test_draft_stamps_retained_artifacts_before_checks(repo, monkeypatch):
    day = stage2.today()
    adr_relative = f"docs/adr/{day}-demo-decision.md"
    adr_text = (
        "---\n"
        'title: "ADR — demo records its decision"\n'
        "status: accepted\n"
        f"date: {day}\n"
        "bead: demo-1\n"
        "provenance: human-decided\n"
        f"review: {PENDING_REVIEW}\n"
        "tags: [adr]\n"
        "---\n"
        "\n"
        "# ADR — demo records its decision\n"
        "\n"
        "The maintainer decided this record's class.\n"
    )

    def fake_run_codex(*_a, **_k):
        _write(
            repo,
            "plans/changes/demo/spec.md",
            SPEC_SEED.replace(
                "The problem and the acceptance criteria stand here.",
                "The problem changed; the criteria now name AGENTS.md.",
            ),
        )
        _write(repo, adr_relative, adr_text)
        return "drafted"

    captured: dict[str, bytes] = {}
    calls = []

    def fake_verify_draft(root, _ctx, _key, _new_adrs, _tools):
        calls.append(1)
        captured["spec"] = (root / "plans/changes/demo/spec.md").read_bytes()
        captured["adr"] = (root / adr_relative).read_bytes()
        return [], False, "document checks only, no tests ran; result: green (stub)"

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_draft", fake_verify_draft)
    stage2.draft(repo, "demo")
    assert calls == [1], "the checks run once, after the first green attempt"
    spec_header = _header_of(captured["spec"].decode("utf-8"))
    assert spec_header["produced_by"] == [
        {"kind": "llm-session", "name": "codex", "version": "2026-11-10", "model": "gpt-6.1-terra"},
        {"kind": "llm-session", "name": "codex", "version": day, "model": "gpt-6.1-terra"},
    ], "the retained draft artifact already carries both producer records when its checks read it"
    adr_header = _header_of(captured["adr"].decode("utf-8"))
    assert _records(adr_header["produced_by"]) == [
        {"kind": "llm-session", "name": "codex", "version": day, "model": "gpt-6.1-terra"}
    ], "the new ADR is stamped like any retained artifact"
    assert adr_header["provenance"] == "human-decided", "the stamp never changes a provenance class"
    assert stage2.committed_bytes(repo, "plans/changes/demo/spec.md") == captured["spec"], (
        "the checkpoint commits exactly the stamped bytes its checks read"
    )


def test_repair_stamps_retained_artifacts_before_checks(repo, monkeypatch):
    day = stage2.today()
    captured: list[bytes] = []

    def fake_run_codex(*_a, **_k):
        _write(
            repo,
            "plans/changes/demo/spec.md",
            SPEC_SEED.replace(
                "The problem and the acceptance criteria stand here.",
                "The problem stands; the criteria are repaired and name AGENTS.md.",
            ),
        )
        return "repaired", "thread"

    def fake_verify_attempt(*_a, **_k):
        captured.append((repo / "plans/changes/demo/spec.md").read_bytes())
        return []

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_attempt", fake_verify_attempt)
    ctx = _ctx(repo)
    baseline = _git(repo, "rev-parse", "HEAD")
    stage2.run_attempts(
        ctx,
        "repair",
        [(stage2.CODEX, None, "codex", None)],
        _build_prompt(ctx),
        baseline,
        None,
        None,
        commit_message="test repair",
        closing="stopped",
        tools={},
        verify_mode="targeted",
        protect_lifecycle=True,
    )
    header = _header_of(captured[0].decode("utf-8"))
    assert header["produced_by"] == [
        {"kind": "llm-session", "name": "codex", "version": "2026-11-10", "model": "gpt-6.1-terra"},
        {"kind": "llm-session", "name": "codex", "version": day, "model": "gpt-6.1-terra"},
    ], "the repair's retained artifact carries the actual producer before its check reads it"
    assert header["review"] == {"status": "pending", "approved_by": None, "approved_at": None}, (
        "the committed approval is reset before the check, not after it"
    )
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "Approval reset — plans/changes/demo/spec.md: the committed approval by Michael Peichl" in findings, (
        "the accepted attempt records whose approval its stamp reset"
    )


def test_repair_stamp_refuses_a_replaced_parent_unwritten(repo, monkeypatch, tmp_path):
    # Hand-finish of 2026-11-19: the stamp writes into the change folder, so its batch is checked
    # before its first write. Planted fault: the folder is swapped for a link outside the worktree
    # after the lifecycle restore, and the stamp writes the producer record through it.
    outside = tmp_path / "outside-change"

    def fake_run_codex(*_a, **_k):
        _write(repo, "plans/changes/demo/spec.md", SPEC_SEED.replace("stand here.", "stand here, repaired."))
        return "repaired", "thread"

    real_restore = stage2.restore_lifecycle_fields

    def swap_after_restore(*args, **kwargs):
        result = real_restore(*args, **kwargs)
        folder = repo / "plans/changes/demo"
        if not folder.is_symlink():
            shutil.copytree(folder, outside)
            shutil.rmtree(folder)
            folder.symlink_to(outside, target_is_directory=True)
        return result

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "restore_lifecycle_fields", swap_after_restore)
    monkeypatch.setattr(stage2, "verify_attempt", lambda *_a, **_k: pytest.fail("verification ran after the swap"))
    ctx = _ctx(repo)
    baseline = _git(repo, "rev-parse", "HEAD")
    with pytest.raises(stage2.RestorationRefused, match="plans/changes/demo"):
        stage2.run_attempts(
            ctx,
            "repair",
            [(stage2.CODEX, None, "codex", None)],
            _build_prompt(ctx),
            baseline,
            None,
            None,
            commit_message="test repair",
            closing="stopped",
            tools={},
            verify_mode="targeted",
            protect_lifecycle=True,
        )
    spec = (outside / "spec.md").read_text(encoding="utf-8")
    assert "stand here, repaired." in spec, "the swap carried the attempt's edit outside"
    assert _header_of(spec)["produced_by"] == {
        "kind": "llm-session",
        "name": "codex",
        "version": "2026-11-10",
        "model": "gpt-6.1-terra",
    }, "the stamp wrote through a parent that escapes the worktree"


def test_each_verb_rejects_invalid_touched_header(repo, monkeypatch):
    calls = []

    def fake_run_codex(*_a, **_k):
        calls.append(1)
        if len(calls) == 1:
            spec = repo / "plans/changes/demo/spec.md"
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    'name: codex, version: "2026-11-10"', 'name: someone-else, version: "2026-11-10"'
                ),
                encoding="utf-8",
            )
        else:
            _write(
                repo,
                "plans/changes/demo/spec.md",
                SPEC_SEED.replace(
                    "The problem and the acceptance criteria stand here.",
                    "The problem stands; the implementation names AGENTS.md.",
                ),
            )
        return "worked", "thread"

    checks = []
    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_attempt", lambda *_a, **_k: checks.append(1) or [])
    ctx = _ctx(repo)
    stage2.run_attempts(
        ctx,
        "implement",
        [(stage2.CODEX, None, "codex", None), (stage2.CODEX, None, "codex-repair", "retry")],
        _build_prompt(ctx),
        _git(repo, "rev-parse", "HEAD"),
        None,
        None,
        commit_message="test implement",
        closing="stopped",
        tools={},
        verify_mode="targeted",
    )
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "plans/changes/demo/spec.md: produced_by.name: expected producing program" in findings, (
        "the shared check judges a touched producer record for implement and names the failing file"
    )
    assert len(checks) == 1, "only the attempt whose header check passed reaches its post-run checks"

    calls.clear()

    def fake_repair_codex(*_a, **_k):
        calls.append(1)
        plan = repo / "plans/changes/demo/plan.md"
        plan.write_text(
            plan.read_text(encoding="utf-8")
            .replace(f"review: {PENDING_REVIEW}", f"review: {APPROVED_REVIEW}")
            .replace("1. Do the thing.", "1. Do the thing, repaired naming AGENTS.md."),
            encoding="utf-8",
        )
        return "repaired", "thread"

    monkeypatch.setattr(stage2, "run_codex", fake_repair_codex)
    with pytest.raises(stage2.CallFailed):
        stage2.run_attempts(
            ctx,
            "repair",
            [(stage2.CODEX, None, "codex", None)],
            _build_prompt(ctx),
            _git(repo, "rev-parse", "HEAD"),
            None,
            None,
            commit_message="test repair",
            closing="stopped",
            tools={},
            verify_mode="targeted",
            protect_lifecycle=True,
        )
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "plans/changes/demo/plan.md: review: an approval the commit does not carry is refused" in findings, (
        "repair runs the same shared check over its touched files"
    )

    # A restored file (bytes equal to HEAD) is not judged; a file without produced_by is not
    # rejected solely for its absence.
    assert stage2.touched_header_problems(repo, ["plans/changes/demo/research.md"]) == []
    plain = f"---\ntitle: Plain\nprovenance: ai-drafted-reviewed\nreview: {PENDING_REVIEW}\n---\n\n# Plain\n\nText.\n"
    _commit_file(repo, "docs/plain.md", plain)
    _write(repo, "docs/plain.md", plain.replace("Text.", "Text, changed and naming AGENTS.md."))
    assert stage2.touched_header_problems(repo, ["docs/plain.md"]) == []


def test_stamping_preserves_other_bytes(repo):
    day = stage2.today()
    relative = "plans/changes/demo/spec.md"
    head = stage2.committed_bytes(repo, relative).decode("utf-8")
    edited = head.replace(
        "The problem and the acceptance criteria stand here.",
        "The problem changed; the criteria now name AGENTS.md.",
    )
    _write(repo, relative, edited)
    notice = stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)
    stamped = (repo / relative).read_text(encoding="utf-8")
    old_lines, new_lines = edited.splitlines(), stamped.splitlines()
    assert len(old_lines) == len(new_lines), "the stamp replaces spans in place, never reflows the file"
    changed_keys = [old.split(":", 1)[0] for old, new in zip(old_lines, new_lines, strict=False) if old != new]
    assert changed_keys == ["updated", "produced_by", "review"], (
        "bytes outside updated, produced_by and a required approval reset stay untouched"
    )
    assert stamped.split("---\n", 2)[2] == edited.split("---\n", 2)[2], "prose and fences keep their bytes"
    header = _header_of(stamped)
    assert header["provenance"] == "ai-drafted-reviewed", "provenance is not one of the runner's fields"
    assert notice is not None and notice.startswith("Approval reset — plans/changes/demo/spec.md")

    adr = f"docs/adr/{day}-demo-note.md"
    _write(
        repo,
        adr,
        (
            "---\n"
            "title: ADR\n"
            "bead: demo-1\n"
            "provenance: human-decided\n"
            f"review: {PENDING_REVIEW}\n"
            "tags: [adr]\n"
            "---\n"
            "\n"
            "# ADR\n"
            "\n"
            "Decision text.\n"
        ),
    )
    stage2.stamp_artifact(repo, adr, producer="codex", model="gpt-6.1-terra", day=day)
    adr_header = _header_at(repo, adr)
    assert adr_header["provenance"] == "human-decided", "a draft ADR keeps its human-decided provenance"
    assert _records(adr_header["produced_by"]) == [
        {"kind": "llm-session", "name": "codex", "version": day, "model": "gpt-6.1-terra"}
    ]


def test_unsafe_header_refuses_attempt(repo, monkeypatch):
    day = stage2.today()
    safe = f"---\ntitle: Safe\nreview: {PENDING_REVIEW}\n---\n# Safe\n\nClean.\n"

    # (1) An anchor or an alias anywhere in the header makes the spans untrustworthy.
    for placement in ("anchor", "alias"):
        relative = f"docs/unsafe-{placement}.md"
        _commit_file(repo, relative, safe)
        record = '{kind: llm-session, name: codex, version: "2026-11-04"}'
        fields = (
            f"produced_by: &p {record}\nother: *p\n"
            if placement == "anchor"
            else f"produced_by: *p\nother: &p {record}\n"
        )
        _write(repo, relative, f"---\ntitle: Unsafe\n{fields}review: {PENDING_REVIEW}\n---\n# Unsafe\n\nEdit.\n")
        with pytest.raises(
            stage2.Refused, match=rf"{re.escape(relative)}: cannot be stamped safely \(YAML {placement}"
        ):
            stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)

    # (2) A header that is not a mapping is refused.
    relative = "docs/unsafe-list.md"
    _commit_file(repo, relative, safe)
    _write(repo, relative, "---\n- just\n- a list\n---\n# Unsafe\n\nEdit.\n")
    with pytest.raises(stage2.Refused, match=rf"{re.escape(relative)}: cannot be stamped safely"):
        stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)

    # (3) produced_by held more than once is refused.
    relative = "docs/unsafe-duplicate.md"
    _commit_file(repo, relative, safe)
    _write(
        repo,
        relative,
        (
            "---\n"
            "title: Dup\n"
            'produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}\n'
            'produced_by: {kind: llm-session, name: pi, version: "2026-11-05"}\n'
            f"review: {PENDING_REVIEW}\n"
            "---\n# Dup\n\nEdit.\n"
        ),
    )
    with pytest.raises(stage2.Refused, match=rf"{re.escape(relative)}: cannot be stamped safely"):
        stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)

    # (4) Bytes that do not decode are refused, naming the artifact.
    relative = "docs/unsafe-bytes.md"
    _commit_file(repo, relative, safe)
    (repo / relative).write_bytes(b"---\ntitle: \xff\xfe\n---\n# Unsafe\n")
    with pytest.raises(stage2.Refused, match=rf"{re.escape(relative)}: cannot be stamped safely \(not UTF-8\)"):
        stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)

    # (5) A producer field the committed baseline carries but no stamp can read stops as a
    # committed fault that names the stock migration.
    relative = "docs/unsafe-committed.md"
    _commit_file(
        repo,
        relative,
        (
            "---\n"
            "title: Dup\n"
            'produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}\n'
            'produced_by: {kind: llm-session, name: pi, version: "2026-11-05"}\n'
            f"review: {PENDING_REVIEW}\n"
            "---\n# Dup\n\nClean.\n"
        ),
    )
    _write(repo, relative, f"---\ntitle: Dup\nreview: {PENDING_REVIEW}\n---\n# Dup\n\nNow clean, naming AGENTS.md.\n")
    with pytest.raises(stage2.CommittedRecordFault, match="coding-harness-2i7x"):
        stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)

    # (6) On a draft route the refusal fails every attempt before the checks, naming the file.
    # Cases (1)-(5) left uncommitted edits behind, and a draft refuses a tree that is not clean.
    _git(repo, "reset", "-q", "--hard")
    _git(repo, "clean", "-fdq")

    def fake_run_codex(*_a, **_k):
        _write(repo, "plans/changes/demo/broken.md", BROKEN_NOTE)
        return "drafted"

    def fake_run_work_model(*_a, **_k):
        _write(repo, "plans/changes/demo/broken.md", BROKEN_NOTE)
        return "drafted"

    work_calls = []
    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "run_work_model", fake_run_work_model)
    monkeypatch.setattr(stage2, "verify_draft", lambda *_a, **_k: work_calls.append(1) or ([], False, "stub scope"))
    with pytest.raises(stage2.CallFailed):
        stage2.draft(repo, "demo")
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "plans/changes/demo/broken.md: cannot be stamped safely (YAML anchor 'shape' in header)" in findings
    assert work_calls == [], "an unsafe header is refused before any post-run check runs on the attempt"


def test_preserves_prior_contributions(repo):
    day = stage2.today()

    # (a) A committed flow list grows in place; the earlier records keep their bytes verbatim.
    relative = "docs/first.md"
    first_header = (
        "---\n"
        "title: First\n"
        'produced_by: [{kind: llm-session, name: codex, version: "2026-11-04", model: "gpt-6.1-sol"}, '
        '{kind: llm-session, name: pi, version: "2026-11-04"}]\n'
        f"review: {PENDING_REVIEW}\n"
        "---\n"
        "\n"
        "# First\n"
        "\n"
        "Early text.\n"
    )
    _commit_file(repo, relative, first_header)
    _write(repo, relative, first_header.replace("Early text.", "Early text, extended naming AGENTS.md."))
    stage2.stamp_artifact(repo, relative, producer="pi", model="claude-haiku-5-5", day=day)
    raw = (repo / relative).read_text(encoding="utf-8")
    assert (
        'produced_by: [{kind: llm-session, name: codex, version: "2026-11-04", model: "gpt-6.1-sol"}, '
        '{kind: llm-session, name: pi, version: "2026-11-04"}, '
        f'{{kind: llm-session, name: pi, version: "{day}", model: "claude-haiku-5-5"}}]'
    ) in raw, "a flow-list baseline grows in place, earlier records byte-verbatim"
    unchanged = (repo / relative).read_bytes()
    assert stage2.stamp_artifact(repo, relative, producer="pi", model="claude-haiku-5-5", day=day) is None
    assert (repo / relative).read_bytes() == unchanged, "an identical contribution is not appended twice"

    # (b) A committed block mapping grows compact sequence items (F-35): the first record line's
    # indentation becomes "- ", later lines unchanged.
    relative = "docs/second.md"
    second_header = (
        "---\n"
        "title: Second\n"
        'produced_by:\n  kind: llm-session\n  name: codex\n  version: "2026-11-04"\n'
        f"review: {PENDING_REVIEW}\n"
        "tags: [x]\n"
        "---\n"
        "\n"
        "# Second\n"
        "\n"
        "More text.\n"
    )
    _commit_file(repo, relative, second_header)
    _write(repo, relative, second_header.replace("More text.", "More text, extended naming AGENTS.md."))
    stage2.stamp_artifact(repo, relative, producer="claude-code", model="glm-5.3-flash", day=day)
    raw = (repo / relative).read_text(encoding="utf-8")
    assert (
        "produced_by:\n"
        "- kind: llm-session\n"
        "  name: codex\n"
        '  version: "2026-11-04"\n'
        "- kind: llm-session\n"
        f'  name: claude-code\n  version: "{day}"\n  model: "glm-5.3-flash"\n'
    ) in raw, "the block mapping converts to a compact sequence, earlier lines byte-identical"

    # (c) A session-written self-description is discarded; the committed state is the only history.
    relative = "docs/third.md"
    third_header = f"---\ntitle: Third\nreview: {PENDING_REVIEW}\n---\n# Third\n\nBase text.\n"
    _commit_file(repo, relative, third_header)
    _write(
        repo,
        relative,
        (
            "---\n"
            "title: Third\n"
            'produced_by: {kind: llm-session, name: codex, version: "2020-01-01"}\n'
            f"review: {PENDING_REVIEW}\n"
            "---\n"
            "\n"
            "# Third\n"
            "\n"
            "Base text, extended naming AGENTS.md.\n"
        ),
    )
    stage2.stamp_artifact(repo, relative, producer="claude-code", model="glm-5.3-flash", day=day)
    assert _records(_header_at(repo, relative)["produced_by"]) == [
        {"kind": "llm-session", "name": "claude-code", "version": day, "model": "glm-5.3-flash"}
    ], "the session's own self-description never survives as history"


def test_body_change_resets_approval(repo, monkeypatch):
    day = stage2.today()
    relative = "plans/changes/demo/spec.md"
    head = stage2.committed_bytes(repo, relative).decode("utf-8")
    _write(
        repo,
        relative,
        head.replace(
            "The problem and the acceptance criteria stand here.",
            "The problem changed; the criteria now name AGENTS.md.",
        ),
    )
    notice = stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)
    header = _header_at(repo, relative)
    assert header["review"] == {"status": "pending", "approved_by": None, "approved_at": None}
    assert notice == (
        "Approval reset — plans/changes/demo/spec.md: the committed approval by Michael Peichl on 2026-11-12 "
        "was reset to pending; the attempt changed the document outside `produced_by` and `updated`."
    )

    # An earlier failed attempt records the reset in its own findings entry, too.
    def fake_run_codex(*_a, **_k):
        _write(
            repo,
            relative,
            head.replace(
                "The problem and the acceptance criteria stand here.",
                "The problem changed again; the criteria name AGENTS.md.",
            ),
        )
        return "repaired", "thread"

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_attempt", lambda *_a, **_k: ["targeted: one test is red (planted)"])
    ctx = _ctx(repo)
    with pytest.raises(stage2.CallFailed):
        stage2.run_attempts(
            ctx,
            "repair",
            [(stage2.CODEX, None, "codex", None)],
            _build_prompt(ctx),
            _git(repo, "rev-parse", "HEAD"),
            None,
            None,
            commit_message="test repair",
            closing="stopped",
            tools={},
            verify_mode="targeted",
            protect_lifecycle=True,
        )
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "- Producer stamps: Approval reset — plans/changes/demo/spec.md" in findings, (
        "a failed attempt names the reset approver in its diagnostics block"
    )


def test_header_only_keeps_approval(repo):
    day = stage2.today()
    relative = "plans/changes/demo/spec.md"
    head = stage2.committed_bytes(repo, relative).decode("utf-8")
    _write(
        repo,
        relative,
        head.replace('model: "gpt-6.1-terra"', 'model: "gpt-6.1-sol"').replace(
            "updated: 2026-11-10", f"updated: {day}"
        ),
    )
    notice = stage2.stamp_artifact(repo, relative, producer="codex", model="gpt-6.1-terra", day=day)
    header = _header_at(repo, relative)
    assert notice is None, "a stamp that touches nothing else never resets the committed approval"
    assert header["review"] == {
        "status": "approved",
        "approved_by": "Michael Peichl",
        "approved_at": date(2026, 11, 12),
    }


def test_unmeasured_attempt_refused(repo, monkeypatch):
    real_tree = stage2.worktree_tree
    readings = []

    def flaky_tree(root):
        readings.append(1)
        if len(readings) == 2:  # the post-call measurement of the first attempt
            raise stage2.Refused("git write-tree refused (planted)")
        return real_tree(root)

    monkeypatch.setattr(stage2, "worktree_tree", flaky_tree)

    def fake_run_codex(*_a, **_k):
        _write(
            repo,
            "plans/changes/demo/spec.md",
            SPEC_SEED.replace(
                "The problem and the acceptance criteria stand here.",
                "The problem stands; this attempt names AGENTS.md.",
            ),
        )
        return "worked", "thread"

    checks = []
    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_attempt", lambda *_a, **_k: checks.append(1) or [])
    ctx = _ctx(repo)
    stage2.run_attempts(
        ctx,
        "implement",
        [(stage2.CODEX, None, "codex", None), (stage2.CODEX, None, "codex-repair", "retry")],
        _build_prompt(ctx),
        _git(repo, "rev-parse", "HEAD"),
        None,
        None,
        commit_message="test implement",
        closing="stopped",
        tools={},
        verify_mode="targeted",
    )
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "the runner could not measure whether the attempt produced work" in findings, (
        "an unmeasured attempt is rejected with a diagnostic, never accepted"
    )
    assert len(checks) == 2, "the unmeasured attempt is rejected despite its checks; the next route's checks stand"


@pytest.mark.parametrize(
    ("relative", "provenance", "review", "expected"),
    [
        (
            "plans/changes/demo/new.md",
            "human-written",
            PENDING_REVIEW,
            "provenance: expected ai-drafted-reviewed on a new file",
        ),
        (
            "plans/changes/demo/new.md",
            "ai-generated",
            PENDING_REVIEW,
            "provenance: expected ai-drafted-reviewed on a new file",
        ),
        ("plans/changes/demo/new.md", "ai-drafted-reviewed", PENDING_REVIEW, None),
        (
            "plans/changes/demo/new.md",
            "ai-drafted-reviewed",
            APPROVED_REVIEW,
            "review: expected pending without approval on a new file",
        ),
        ("docs/adr/2026-11-18-demo-note.md", "human-decided", PENDING_REVIEW, None),
        (
            "docs/adr/2026-11-18-demo-note.md",
            "human-written",
            PENDING_REVIEW,
            "provenance: expected human-decided or ai-drafted-reviewed on a new file",
        ),
        (
            "docs/adr/2026-11-18-demo-note.md",
            "human-decided",
            APPROVED_REVIEW,
            "review: expected pending without approval on a new file",
        ),
    ],
)
def test_new_files_require_pending_review(relative, provenance, review, expected):
    text = f"---\ntitle: New\nprovenance: {provenance}\nreview: {review}\ntags: [x]\n---\n# New\n\nText.\n"
    problems = stage2.header_problems(relative, None, text.encode("utf-8"))
    if expected is None:
        assert problems == []
    else:
        assert problems == [f"{relative}: {expected}"]


def test_committed_baseline_controls_approval():
    approved = (
        "---\n"
        "title: Doc\n"
        "provenance: ai-drafted-reviewed\n"
        f"review: {APPROVED_REVIEW}\n"
        "tags: [x]\n"
        "---\n"
        "\n"
        "# Doc\n"
        "\n"
        "Body.\n"
    )
    pending = approved.replace(f"review: {APPROVED_REVIEW}", f"review: {PENDING_REVIEW}")
    human = approved.replace("provenance: ai-drafted-reviewed", "provenance: human-written")
    relative = "plans/changes/demo/spec.md"

    # An unchanged compatible committed approval stands.
    assert stage2.header_problems(relative, approved.encode(), approved.encode()) == []
    # An approval the commit does not carry is refused, body changed or not.
    invented = pending.replace(f"review: {PENDING_REVIEW}", f"review: {APPROVED_REVIEW}")
    assert stage2.header_problems(relative, pending.encode(), invented.encode()) == [
        f"{relative}: review: an approval the commit does not carry is refused"
    ]
    # The runner's own reset beside a real document change stands, on a verb that stamps.
    reset = approved.replace("Body.", "Body, changed naming AGENTS.md.").replace(
        f"review: {APPROVED_REVIEW}", f"review: {PENDING_REVIEW}"
    )
    assert stage2.header_problems(relative, approved.encode(), reset.encode(), runner_reset=True) == []
    # The same reset without a document change is refused.
    bare_reset = approved.replace(f"review: {APPROVED_REVIEW}", f"review: {PENDING_REVIEW}")
    assert stage2.header_problems(relative, approved.encode(), bare_reset.encode(), runner_reset=True) == [
        f"{relative}: review: reset without a document change outside `produced_by` and `updated`"
    ]
    # A provenance class is measured against the committed class.
    assert stage2.header_problems(relative, human.encode(), approved.encode()) == [
        f"{relative}: provenance: changed from the committed class"
    ]


def test_explore_resets_class_and_approval(repo, monkeypatch):
    day = stage2.today()
    monkeypatch.setattr(
        stage2,
        "run_work_model",
        lambda *_a, **_k: "Facts: the runner reads AGENTS.md before any call.",
    )
    stage2.explore(repo, "demo")
    text = (repo / "plans/changes/demo/research.md").read_text(encoding="utf-8")
    header = _header_of(text)
    assert header["provenance"] == "ai-drafted-reviewed", "a human-written skeleton publishes as ai-drafted-reviewed"
    assert header["review"] == {"status": "pending", "approved_by": None, "approved_at": None}, (
        "an earlier approval does not survive the publication"
    )
    assert f"## Runner exploration — {day}" in text


def test_active_research_contract_matches_census(repo, monkeypatch):
    import research_census as census

    relative = "plans/changes/demo/research.md"
    published = (
        "---\n"
        'title: "Research — demo"\n'
        "status: draft\n"
        "date: 2026-11-17\n"
        "last_reviewed: 2026-11-17\n"
        "updated: 2026-11-18\n"
        "bead: demo-1\n"
        "provenance: ai-drafted-reviewed\n"
        'produced_by: [{kind: llm-session, name: claude-code, version: "2026-11-18", model: "glm-5.3-flash"}]\n'
        f"review: {APPROVED_REVIEW.replace('2026-11-12', '2026-11-18')}\n"
        "tags: [research]\n"
        "---\n"
        "\n"
        "# Research — demo\n"
        "\n"
        "Stage-2 call, 2026-11-18: explore · attempt 1 · route flash · endpoint glm-coding-plan · "
        "model glm-5.3-flash · leak check clean over 1 files, 1 commits, 1 rules.\n"
        "\n"
        "## Runner exploration — 2026-11-18\n"
        "\n"
        "Findings naming AGENTS.md.\n"
    )
    baseline = stage2.committed_bytes(repo, relative)
    problems = stage2.header_problems(relative, baseline, published.encode("utf-8"))
    assert problems == census.text_findings(relative, published), (
        "the shared post-run check applies the census's own contract to active research"
    )
    assert any("review: expected pending without approval" in line for line in problems)

    # A draft or repair result that preserves an incompatible baseline fails its own post-run
    # check instead of passing a later full verify.
    incompatible = RESEARCH_SEED.replace(
        "provenance: human-written",
        'provenance: human-written\nproduced_by: {kind: llm-session, name: claude-code, version: "2026-11-17"}',
    )
    _commit_file(repo, relative, incompatible, "seed an incompatible research baseline")
    checks = []

    def fake_run_codex(*_a, **_k):
        research = repo / relative
        research.write_text(
            research.read_text(encoding="utf-8").replace(
                "Authored skeleton notes", "Authored skeleton notes, touched and naming AGENTS.md"
            ),
            encoding="utf-8",
        )
        return "worked", "thread"

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_attempt", lambda *_a, **_k: checks.append(1) or [])
    ctx = _ctx(repo)
    with pytest.raises(stage2.CallFailed):
        stage2.run_attempts(
            ctx,
            "implement",
            [(stage2.CODEX, None, "codex", None)],
            _build_prompt(ctx),
            _git(repo, "rev-parse", "HEAD"),
            None,
            None,
            commit_message="test implement",
            closing="stopped",
            tools={},
            verify_mode="targeted",
        )
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    assert "plans/changes/demo/research.md: provenance: expected ai-drafted-reviewed" in findings
    assert checks == [], "the incompatible research fails the shared check before any post-run check"


@pytest.mark.parametrize("position", [0, 1])
def test_duplicate_key_in_producer_list_is_committed_fault(position):
    valid = '{kind: llm-session, name: codex, version: "2026-11-04"}'
    duplicate = '{kind: llm-session, name: pi, name: codex, version: "2026-11-04"}'
    records = [valid, valid]
    records[position] = duplicate
    with pytest.raises(stage2.CommittedRecordFault, match="duplicate keys"):
        stage2.parse_producer_records(f"[{', '.join(records)}]", "docs/example.md")


@pytest.mark.parametrize("position", [0, 1])
@pytest.mark.parametrize("relative", ["docs/example.md", "plans/changes/demo/research.md"])
def test_duplicate_key_in_producer_list_is_output_fault(position, relative):
    # Loop row L1-2, output side: the shared post-run check refuses a duplicate key inside any record
    # of a list-shaped produced_by a run wrote, outside active research as inside it.
    valid = '{kind: llm-session, name: codex, version: "2026-11-04"}'
    duplicate = '{kind: llm-session, name: pi, name: codex, version: "2026-11-04"}'
    records = [valid, valid]
    records[position] = duplicate
    text = (
        "---\ntitle: New\ndate: 2026-11-04\nlast_reviewed: 2026-11-04\nupdated: 2026-11-04\n"
        f"provenance: ai-drafted-reviewed\nproduced_by: [{', '.join(records)}]\nreview: {PENDING_REVIEW}\n"
        "---\n# New\n\nText.\n"
    )
    problems = stage2.header_problems(relative, None, text.encode("utf-8"))
    assert any("produced_by" in problem and "duplicate" in problem for problem in problems), problems


def test_prepublication_failure_routing(repo, monkeypatch):
    relative = "plans/changes/demo/research.md"
    model_calls = []

    def fake_run_work_model(*_a, **_k):
        model_calls.append(1)
        return "Facts: the runner reads AGENTS.md before any call."

    monkeypatch.setattr(stage2, "run_work_model", fake_run_work_model)

    # (a) A committed-record fault stops the verb before any route is spent.
    broken = RESEARCH_SEED.replace(
        "provenance: human-written",
        "provenance: human-written\n"
        'produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}\n'
        'produced_by: {kind: llm-session, name: pi, version: "2026-11-05"}',
    )
    _commit_file(repo, relative, broken, "seed a broken committed header")
    with pytest.raises(stage2.CommittedRecordFault, match="coding-harness-2i7x"):
        stage2.explore(repo, "demo")
    assert model_calls == [], "a committed header fault spends no route"

    # (b) A fault in the model output refuses the attempt; the prepared bytes never publish.
    _commit_file(repo, relative, RESEARCH_SEED, "restore a clean committed header")
    real_publication = stage2.research_publication

    def corrupting(existing, **kwargs):
        prepared = real_publication(existing, **kwargs)
        return prepared.replace(b"provenance: ai-drafted-reviewed", b"provenance: human-written")

    monkeypatch.setattr(stage2, "research_publication", corrupting)
    with pytest.raises(stage2.Refused):
        stage2.explore(repo, "demo")
    text = (repo / relative).read_text(encoding="utf-8")
    assert "## Runner exploration" not in text, "rejected output is never published"
    assert "provenance: human-written" in text, "the attempt's own fault never lands in the tree"
    assert model_calls == [1], "the model-output fault spent its one route, then refused"


SPEC_PATH = "plans/changes/demo/spec.md"


def test_indented_block_sequence_grows_without_reprefix():
    # Loop row L2-2: a committed block sequence keeps every earlier record's bytes; the new record
    # joins at the sequence's own indentation, never as a second `- ` prefix or at column 0.
    field = (
        '\n  - {kind: llm-session, name: codex, version: "2026-11-04"}'
        '\n  - {kind: llm-session, name: pi, version: "2026-11-05"}'
    )
    earlier = stage2.parse_producer_records(field, "test")
    added = {"kind": "llm-session", "name": "claude-code", "version": "2026-11-06", "model": "glm-5.3-flash"}
    result = stage2.retained_producer_field(field, [*earlier, added])
    assert result.startswith(field + "\n"), "the earlier records keep their bytes"
    try:
        loaded = yaml.safe_load("produced_by:" + result)
    except yaml.YAMLError as error:
        pytest.fail(f"the grown block sequence is not valid YAML: {error}")
    assert loaded["produced_by"] == [*earlier, added]


def test_failed_draft_attempt_block_names_the_reset_approver(repo, monkeypatch):
    # Loop row L2-3: the first attempt's stamp resets the approval and its checks fail; the later
    # attempt touches nothing. The failed attempt's own block still names the former approver.
    calls = []

    def fake_run_codex(*_a, **_k):
        calls.append(1)
        if len(calls) == 1:
            _write(
                repo,
                SPEC_PATH,
                SPEC_SEED.replace("The problem and the acceptance criteria stand here.", "A changed problem."),
            )
        return "drafted"

    verdicts = iter([(["a planted document check failure"], False, "scope"), ([], False, "scope")])
    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "verify_draft", lambda *_a, **_k: next(verdicts))
    stage2.draft(repo, "demo")
    findings = (repo / "plans/changes/demo/findings.md").read_text(encoding="utf-8")
    needle = "Producer stamps: Approval reset — plans/changes/demo/spec.md: the committed approval by Michael Peichl"
    assert needle in findings, "a failed draft attempt's block lists its stamp notices as the repair path does"


def test_draft_stamp_refuses_a_replaced_parent_unwritten(repo, monkeypatch, tmp_path):
    # Loop row L2-5: the draft stamp passes the repair path's recovery preflight. Planted fault:
    # the change folder is swapped for a link outside the worktree after the call.
    outside = tmp_path / "outside-change"

    def fake_run_codex(*_a, **_k):
        _write(repo, SPEC_PATH, SPEC_SEED.replace("stand here.", "stand here, drafted."))
        return "drafted"

    real_put_back = stage2.put_back

    def swap_after_put_back(*args, **kwargs):
        result = real_put_back(*args, **kwargs)
        folder = repo / "plans/changes/demo"
        if not folder.is_symlink():
            shutil.copytree(folder, outside)
            shutil.rmtree(folder)
            folder.symlink_to(outside, target_is_directory=True)
        return result

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "put_back", swap_after_put_back)
    monkeypatch.setattr(stage2, "verify_draft", lambda *_a, **_k: pytest.fail("the checks ran after the swap"))
    with pytest.raises(stage2.RestorationRefused, match="plans/changes/demo"):
        stage2.draft(repo, "demo")
    spec = (outside / "spec.md").read_text(encoding="utf-8")
    assert "stand here, drafted." in spec, "the swap carried the attempt's edit outside"
    assert _header_of(spec)["produced_by"] == {
        "kind": "llm-session",
        "name": "codex",
        "version": "2026-11-10",
        "model": "gpt-6.1-terra",
    }, "the stamp wrote through a parent that escapes the worktree"


def test_draft_never_stamps_the_runners_findings_file(repo, monkeypatch):
    # Loop row L2-14: findings.md and plans/INDEX.md carry no model contribution.
    stamped: list[str] = []
    real_stamp = stage2.stamp_retained_artifacts

    def spy(root, candidates, **kwargs):
        stamped.extend(candidates)
        return real_stamp(root, candidates, **kwargs)

    def fake_run_codex(*_a, **_k):
        _write(repo, SPEC_PATH, SPEC_SEED.replace("stand here.", "stand here, drafted."))
        findings = repo / "plans/changes/demo/findings.md"
        findings.write_text(findings.read_text(encoding="utf-8") + "\nA drafting session's note.\n", encoding="utf-8")
        return "drafted"

    monkeypatch.setattr(stage2, "run_codex", fake_run_codex)
    monkeypatch.setattr(stage2, "stamp_retained_artifacts", spy)
    monkeypatch.setattr(stage2, "verify_draft", lambda *_a, **_k: ([], False, "scope"))
    stage2.draft(repo, "demo")
    assert SPEC_PATH in stamped, "the drafted artifact is a stamp candidate"
    assert "plans/changes/demo/findings.md" not in stamped, "the runner's audit file is never a stamp candidate"


def test_committed_headerless_file_given_a_header_is_judged_as_new(repo):
    # Loop row L2-6: a committed document that opens with a rule and has no header gets a model-written
    # header; the header is judged as a new one, not reported as an unreadable committed header.
    relative = "plans/changes/demo/notes.md"
    _commit_file(repo, relative, "---\nJust a note between two rules\n---\n\nBody.\n", "seed a headerless note")
    good = f"---\nprovenance: ai-drafted-reviewed\nreview: {PENDING_REVIEW}\n---\n\nBody.\n"
    _write(repo, relative, good)
    assert stage2.touched_header_problems(repo, [relative]) == []
    bad = good.replace("ai-drafted-reviewed", "human-written")
    _write(repo, relative, bad)
    problems = stage2.touched_header_problems(repo, [relative])
    assert any("expected ai-drafted-reviewed on a new file" in problem for problem in problems), problems


def test_verb_without_stamp_refuses_a_session_reset_of_an_approval():
    # Loop row L2-9: only a verb that stamps may reset a committed approval beside a body change.
    current = SPEC_SEED.replace(APPROVED_REVIEW, PENDING_REVIEW).replace("stand here.", "stand here, changed.")
    base = SPEC_SEED.encode("utf-8")
    problems = stage2.header_problems(SPEC_PATH, base, current.encode("utf-8"))
    assert any("review:" in problem and "does not stamp" in problem for problem in problems), problems
    assert stage2.header_problems(SPEC_PATH, base, current.encode("utf-8"), runner_reset=True) == []


def test_swarm_publication_runs_the_shared_check_first(repo, monkeypatch):
    # Loop row L2-4: the swarm route judges its prepared publication before anything lands.
    import stage2_research_run

    run = stage2_research_run.Run(repo, "demo", stage2, "feature", {})
    run.store = object()
    run.run_id = "deadbeef"
    run.publication_bytes = RESEARCH_SEED.replace(
        "provenance: human-written",
        "provenance: human-written\n"
        'produced_by: {kind: llm-session, name: stage2-research-swarm, version: "2026-11-17"}',
    ).encode("utf-8")
    monkeypatch.setattr(stage2, "publish_research", lambda *_a, **_k: pytest.fail("a rejected publication landed"))
    with pytest.raises(stage2.Refused):
        run.publish("complete")


def test_release_loop_runs_the_shared_check_on_findings(repo, monkeypatch):
    # Loop row L2-10: a header fault in the findings.md a release wrote refuses the verb.
    def fake_release(root, _change):
        _write(
            root,
            "plans/changes/demo/findings.md",
            f"---\ntitle: Findings\nprovenance: human-written\nreview: {PENDING_REVIEW}\n---\n\n# Findings\n",
        )
        return []

    monkeypatch.setattr(stage2, "release", fake_release)
    with pytest.raises(stage2.Refused, match="findings.md"):
        stage2.release_loop(repo, "demo")


def test_committed_header_fault_stops_every_verb_naming_the_migration(repo):
    # Loop row L2-12, part 1: a committed header that is no mapping stops a verb without a stamp.
    relative = "plans/changes/demo/notes.md"
    _commit_file(repo, relative, "---\n- not\n- a mapping\n---\n\nBody.\n", "seed a faulty committed header")
    _write(repo, relative, "---\n- not\n- a mapping\n---\n\nBody, changed.\n")
    try:
        stage2.touched_header_problems(repo, [relative])
    except stage2.CommittedRecordFault as error:
        assert "coding-harness-2i7x" in str(error)
    else:
        pytest.fail("a committed header fault must stop the verb naming the migration")


def test_committed_duplicate_producer_stops_the_stamp_as_a_committed_fault(repo):
    # Loop row L2-12, part 2: the stamp's working-tree checks never pre-empt the committed fault.
    first = 'produced_by: {kind: llm-session, name: codex, version: "2026-11-10", model: "gpt-6.1-terra"}\n'
    second = 'produced_by: {kind: llm-session, name: pi, version: "2026-11-11"}\n'
    _commit_file(repo, SPEC_PATH, SPEC_SEED.replace(first, first + second), "seed a duplicate producer field")
    head = stage2.committed_bytes(repo, SPEC_PATH).decode("utf-8")
    _write(repo, SPEC_PATH, head.replace("stand here.", "stand here, changed."))
    try:
        stage2.stamp_artifact(repo, SPEC_PATH, producer="codex", model="gpt-6.1-terra", day=stage2.today())
    except stage2.CommittedRecordFault as error:
        assert "coding-harness-2i7x" in str(error)
    except stage2.Refused as error:
        pytest.fail(f"a committed fault was reported as an attempt fault: {error}")
    else:
        pytest.fail("the stamp accepted a committed duplicate producer field")
