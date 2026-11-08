"""The outcome test: questionnaire export, live-source grading, and the one-line history.

`scripts.outcome_test` derives every expected answer from the measured
repository at recording time and appends at most one JSONL line per measured
run. Every case here builds its own temporary git repository with injected
doctrine and code — sentinel values, never the live ones — and runs the copied
tool through subprocesses or in process. No real model, hook or tracker is
ever touched. Each docstring names the fault it was written against — planting
it turned exactly this test red.
"""

from __future__ import annotations

import ast
import fcntl
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_NAME = "outcome_test.py"
QUESTION_SET_NAME = "outcome_test_questions.json"
HISTORY_REL = "docs/research/outcome-test-results.jsonl"

QUESTION_IDS = (
    "repair-model",
    "repair-fallback",
    "verify-floor",
    "verify-floor-override",
    "run-plans",
    "handovers",
    "tracker-command",
    "instructions",
)

# Sentinel values the fixtures carry: deliberately unlike today's live answers,
# so every assertion reads the tool's own derivation, never the repository's
# current text. The declaration-change and questionnaire tests separately
# plant another instruction filename, independent of the source basename.
SENTINELS: dict[str, Any] = {
    "repair-model": "sentinel-repair-9",
    "repair-fallback": "Sentinel 9.9",
    "verify-floor": 41.5,
    "verify-floor-override": "SENTINEL_VERIFY_FLOOR",
    "run-plans": "docs/runs",
    "handovers": "docs/journal/handovers-sentinel",
    "tracker-command": "tools/bt",
    "instructions": "AGENTS.md",
}

VERIFY_LOCK_FIXTURE = """FLOOR_ENV = "{floor_env}"
DEFAULT_MEMORY_FLOOR = {floor}

def memory_floor() -> float:
    return DEFAULT_MEMORY_FLOOR

raise RuntimeError("the measurement tool must never import this module")
"""

WORKFLOW_FIXTURE = """---
title: fixture workflow
---

# Fixture workflow

### The routing

The rows name the models.

| Phase | Model | Why |
|---|---|---|
| 4 Implement | **worker-flash** | a worker for every change |
| Repair after 4b and 6 | **{repair_model}** | one sandboxed attempt; one fresh retry after a failed check, and {repair_fallback} at effort `low` after two failed ones; no other credential |
| 6 Review | **{repair_model}** | a fresh review session |

### The eighth movement: the session handover

The handover closes one session.

| When | Artefact | Gate |
|---|---|---|
| end of a session, whatever the phase | `{handovers}/<date>-<name>.md` after `templates/handover.md` | frontmatter required |

### Recurring jobs

None here.
"""

ORCHESTRATION_FIXTURE = """---
title: fixture orchestration
---

# Orchestration

## What a lane is

- A lane is an ordered queue of changes. The night plan is an example
  ([night plan]({run_plan_link})).
- One session orchestrates all of them.

## The resource rule

One verify at a time.
"""

AGENTS_FIXTURE = """# Fixture agents

`{instructions}` is the only instruction file: a fresh reader starts here, and a foreign
`OTHER.md` would silently replace it.

## House rules

1. Keep every artefact English.
2. The tracker runs through the wrapper: **Use `{tracker_command}`, never bare `{tracker_bare}`.** The wrapper pins the version.

## Sessions

Worktrees carry one change each.
"""


def _sources_text(**overrides: Any) -> dict[str, str]:
    """The four measured sources with sentinel values, `overrides` swapping single values."""
    values = {
        "repair_model": "sentinel-repair-9",
        "repair_fallback": "Sentinel 9.9",
        "floor": "41.5",
        "floor_env": "SENTINEL_VERIFY_FLOOR",
        "run_plan_link": "runs/2026-10-28-night-run-plan.md",
        "handovers": "docs/journal/handovers-sentinel",
        "tracker_command": "tools/bt",
        "tracker_bare": "bt",
        "instructions": "AGENTS.md",
    } | {key: str(value) for key, value in overrides.items()}
    return {
        "AGENTS.md": AGENTS_FIXTURE.format(**values),
        "docs/WORKFLOW.md": WORKFLOW_FIXTURE.format(**values),
        "docs/orchestration.md": ORCHESTRATION_FIXTURE.format(**values),
        "scripts/verify_lock.py": VERIFY_LOCK_FIXTURE.format(**values),
    }


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=fixture",
            "-c",
            "user.email=fixture@example.com",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )


def _commit(root: Path, message: str) -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)


def _write_repo(root: Path) -> Path:
    """One temporary repository: the real tool and question set, injected doctrine and code."""
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True, text=True, timeout=60)
    (root / "scripts").mkdir(parents=True)
    (root / "docs").mkdir()
    shutil.copy2(REPO_ROOT / "scripts" / SCRIPT_NAME, root / "scripts" / SCRIPT_NAME)
    shutil.copy2(REPO_ROOT / "scripts" / QUESTION_SET_NAME, root / "scripts" / QUESTION_SET_NAME)
    for rel, text in _sources_text().items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    _commit(root, "fixture tree")
    return root


def _overwrite(root: Path, **overrides: Any) -> None:
    for rel, text in _sources_text(**overrides).items():
        (root / rel).write_text(text, encoding="utf-8")
    _commit(root, "fixture sources moved")


def _head_of(root: Path) -> str:
    done = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return done.stdout.strip()


def _run_tool(root: Path, *args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = {**os.environ}
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-I", str(root / "scripts" / SCRIPT_NAME), *args],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(root),
        env=env,
        check=False,
    )


def _export(root: Path) -> dict[str, Any]:
    done = _run_tool(root, "questions")
    assert done.returncode == 0, f"questions failed: {done.stderr}"
    return json.loads(done.stdout)


def _record(
    root: Path,
    tmp_path: Path,
    questionnaire: dict[str, Any],
    answers: dict[str, Any],
    *,
    harness: str | None = "claude-code",
    model: str | None = "sentinel-model",
    context: str | None = "agents-file",
    access: str | None = "read-only",
    purpose: str = "baseline",
    target: str | None = None,
    fresh: bool = True,
    env_extra: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    qpath = tmp_path / "questionnaire.json"
    qpath.write_text(json.dumps(questionnaire), encoding="utf-8")
    apath = tmp_path / "answers.json"
    apath.write_text(json.dumps(answers), encoding="utf-8")
    args = ["record", "--questionnaire", str(qpath), "--answers", str(apath)]
    for flag, value in (("--harness", harness), ("--model", model), ("--context", context), ("--access", access)):
        if value is not None:
            args += [flag, value]
    args += ["--purpose", purpose]
    if target is not None:
        args += ["--target", target]
    if fresh:
        args.append("--fresh-session")
    return _run_tool(root, *args, env_extra=env_extra)


def _history(root: Path) -> list[dict[str, Any]]:
    text = (root / HISTORY_REL).read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line]


def _verdict_map(record: dict[str, Any]) -> dict[str, str]:
    return {verdict["id"]: verdict["verdict"] for verdict in record["verdicts"]}


def _leaves(node: Any) -> list[Any]:
    """Every scalar leaf of a parsed JSON document, for collision-proof leak checks.

    A raw substring search would flake: a numeric sentinel such as 41.5 can
    appear inside an ISO timestamp (`...:41.512...`) that carries no answer.
    """
    if isinstance(node, dict):
        return [leaf for value in node.values() for leaf in _leaves(value)]
    if isinstance(node, list):
        return [leaf for value in node for leaf in _leaves(value)]
    return [node]


# ---------------------------------------------------------------------------
# Criterion 1 — the eight fixed topics
# ---------------------------------------------------------------------------


def test_question_set_has_eight_fixed_topics(tmp_path: Path) -> None:
    """The eight identities are fixed constants: a source-value edit renames no question and drops no topic.

    Fault this pins: question identities derived from source values, so a
    changed rule silently changed what is asked; a set of seven or nine.
    """
    qset = json.loads((REPO_ROOT / "scripts" / QUESTION_SET_NAME).read_text(encoding="utf-8"))
    assert qset["schema_version"] == 1
    assert [q["id"] for q in qset["questions"]] == list(QUESTION_IDS)
    assert len(qset["questions"]) == 8
    assert all(q["answer_type"] in {"string", "directory", "number"} for q in qset["questions"])
    assert all(q["resolver"] == q["id"] for q in qset["questions"])

    root = _write_repo(tmp_path / "repo")
    first = _export(root)
    assert [q["id"] for q in first["questions"]] == list(QUESTION_IDS)
    assert len(first["questions"]) == 8

    _overwrite(root, floor="77.25")
    second = _export(root)
    assert [q["id"] for q in second["questions"]] == list(QUESTION_IDS)
    assert [q["answer_type"] for q in second["questions"]] == [q["answer_type"] for q in first["questions"]]


# ---------------------------------------------------------------------------
# Criterion 2 — expected answers follow the live sources
# ---------------------------------------------------------------------------


def test_expected_answers_follow_live_sources(tmp_path: Path) -> None:
    """Expected answers are derived from the measured tree: an edited source moves the passing answer, and no code import runs.

    Fault this pins: a stored answer key that still scored yesterday's floor
    after the source moved on, or the tool importing the measured module —
    whose fixture body raises on import.
    """
    root = _write_repo(tmp_path / "repo")
    answers = dict(SENTINELS)

    done = _record(root, tmp_path, _export(root), answers)
    assert done.returncode == 0, done.stderr
    record = _history(root)[-1]
    assert record["correct"] == 8 and record["total"] == 8

    _overwrite(root, floor="77.25")
    done = _record(root, tmp_path, _export(root), answers)
    assert done.returncode == 1
    record = _history(root)[-1]
    assert record["correct"] == 7 and record["total"] == 8
    assert _verdict_map(record)["verify-floor"] == "incorrect"

    done = _record(root, tmp_path, _export(root), answers | {"verify-floor": 77.25})
    assert done.returncode == 0, done.stderr


# ---------------------------------------------------------------------------
# Criterion 3 — the questionnaire carries no answer key
# ---------------------------------------------------------------------------


def test_questionnaire_contains_no_answer_key(tmp_path: Path) -> None:
    """The questionnaire carries questions and shapes only: no derived value and no expected-value field reaches the session material.

    Fault this pins: an expected-value field or a copied solution passage
    travelling with the questions.
    """
    root = _write_repo(tmp_path / "repo")
    _overwrite(root, instructions="SENTINEL-INSTRUCTIONS.md")
    sentinels = SENTINELS | {"instructions": "SENTINEL-INSTRUCTIONS.md"}
    document = _export(root)
    leaves = _leaves(document)
    leaked = [f"{qid}={value!r}" for qid, value in sentinels.items() if any(leaf == value for leaf in leaves)]
    assert leaked == [], f"derived values reached the questionnaire: {leaked}"
    assert set(document) == {
        "schema_version",
        "run_id",
        "prepared_at",
        "commit",
        "question_set_sha256",
        "source_sha256",
        "questions",
        "submission_format",
    }
    for question in document["questions"]:
        assert set(question) == {"id", "text", "answer_type", "source"}


# ---------------------------------------------------------------------------
# Criterion 4 — session metadata and the freshness attestation
# ---------------------------------------------------------------------------


def test_session_metadata_and_fresh_attestation_are_required(tmp_path: Path) -> None:
    """A run without its four labels, with a blank label, or without the freshness attestation records nothing.

    Fault this pins: an anonymous or unattested run appended as if it had
    measured a separately started, memory-free session.
    """
    root = _write_repo(tmp_path / "repo")
    history = root / HISTORY_REL
    questionnaire = _export(root)
    answers = dict(SENTINELS)

    for label in ("harness", "model", "context", "access"):
        done = _record(root, tmp_path, questionnaire, answers, **{label: None})
        assert done.returncode == 3, f"{label} was optional"
        assert "not measured" in done.stderr
    done = _record(root, tmp_path, questionnaire, answers, harness="   ")
    assert done.returncode == 3
    done = _record(root, tmp_path, questionnaire, answers, fresh=False)
    assert done.returncode == 3
    assert not history.exists(), "an unattested run was recorded"

    done = _record(root, tmp_path, questionnaire, answers)
    assert done.returncode == 0, done.stderr
    record = _history(root)[-1]
    assert record["harness"] == "claude-code"
    assert record["model"] == "sentinel-model"
    assert record["context"] == "agents-file"
    assert record["access"] == "read-only"
    assert record["fresh_session"] is True


# ---------------------------------------------------------------------------
# Criterion 5 — exact grading, fixed denominator
# ---------------------------------------------------------------------------


def test_grading_is_exact_and_keeps_denominator_eight(tmp_path: Path) -> None:
    """Grading is exact per shape and the denominator never moves: omissions, wrong types, case and prose earn nothing.

    Fault this pins: a missing answer shrinking the total, a numeric string or
    boolean accepted as the floor, a keyword inside contradictory prose
    scoring, case-insensitive or substring matching.
    """
    root = _write_repo(tmp_path / "repo")
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 0, done.stderr

    wrong = dict(SENTINELS)
    del wrong["repair-fallback"]
    wrong["verify-floor"] = "41.5"
    wrong["verify-floor-override"] = "sentinel_verify_floor"
    wrong["tracker-command"] = True
    wrong["run-plans"] = "the plans sit in docs/runs, and nowhere else"
    wrong["repair-model"] = SENTINELS["repair-fallback"]
    done = _record(root, tmp_path, _export(root), wrong)
    assert done.returncode == 1
    record = _history(root)[-1]
    assert record["total"] == 8 and record["correct"] == 2
    assert _verdict_map(record) == {
        "repair-model": "incorrect",
        "repair-fallback": "incorrect",
        "verify-floor": "incorrect",
        "verify-floor-override": "incorrect",
        "run-plans": "incorrect",
        "tracker-command": "incorrect",
        "handovers": "correct",
        "instructions": "correct",
    }

    soft = dict(SENTINELS)
    soft["tracker-command"] = "  tools/bt  "
    soft["run-plans"] = "docs/runs/"
    done = _record(root, tmp_path, _export(root), soft)
    assert done.returncode == 0, done.stderr


# ---------------------------------------------------------------------------
# Criterion 6 — unread or moved-on evidence prevents recording
# ---------------------------------------------------------------------------


def test_unread_or_changed_evidence_prevents_recording(tmp_path: Path) -> None:
    """Missing, conflicting, unrecognised or moved-on sources measure nothing and append nothing.

    Fault this pins: an unavailable expected answer graded as a wrong model
    answer, or a changed source silently scored as though the session had
    seen it.
    """
    root = _write_repo(tmp_path / "repo")
    history = root / HISTORY_REL
    before_removal = _export(root)

    (root / "docs" / "orchestration.md").unlink()
    _commit(root, "remove the run-plan source")
    done = _run_tool(root, "questions")
    assert done.returncode == 3 and "not measured" in done.stderr
    done = _record(root, tmp_path, before_removal, dict(SENTINELS))
    assert done.returncode == 3
    assert not history.exists()

    _overwrite(root)
    valid = _export(root)
    conflicting = _sources_text()["AGENTS.md"].replace(
        "## Sessions",
        "4. **Use `other/bx`, never bare `bx`.** A second wrapper.\n\n## Sessions",
    )
    (root / "AGENTS.md").write_text(conflicting, encoding="utf-8")
    _commit(root, "second tracker rule")
    done = _record(root, tmp_path, valid, dict(SENTINELS))
    assert done.returncode == 3
    assert "not measured" in done.stderr

    _overwrite(root)
    reworded = _sources_text()["docs/WORKFLOW.md"].replace(
        "at effort `low` after two failed ones",
        "as the second reserve once two attempts have failed",
    )
    (root / "docs" / "WORKFLOW.md").write_text(reworded, encoding="utf-8")
    _commit(root, "reword the fallback clause")
    done = _run_tool(root, "questions")
    assert done.returncode == 3

    _overwrite(root)
    stale = _export(root)
    _overwrite(root, floor="12.5")
    done = _record(root, tmp_path, stale, dict(SENTINELS))
    assert done.returncode == 3
    assert "stale" in done.stderr
    assert not history.exists(), "an unmeasurable run appended a record"


# ---------------------------------------------------------------------------
# Criterion 7 — one dated, commit-bound line per measured run
# ---------------------------------------------------------------------------


def test_measured_runs_append_one_dated_commit_bound_line(tmp_path: Path) -> None:
    """One measured run appends exactly one dated, commit-bound line; earlier bytes stand and no expected value is stored.

    Fault this pins: a record missing its metadata or verdicts, history
    rewritten by a second run, or the derived answer key persisted beside the
    subject's own answers.
    """
    root = _write_repo(tmp_path / "repo")
    history = root / HISTORY_REL
    history.parent.mkdir(parents=True)
    assert _record(root, tmp_path, _export(root), dict(SENTINELS)).returncode == 0
    seed = history.read_text(encoding="utf-8")

    questionnaire = _export(root)
    wrong = {qid: f"zzz-wrong-{qid}" for qid in QUESTION_IDS}
    wrong["verify-floor"] = 0.5
    done = _record(root, tmp_path, questionnaire, wrong)
    assert done.returncode == 1

    lines = history.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert lines[0] == seed.rstrip("\n")
    record = json.loads(lines[1])
    assert record["run_id"] == questionnaire["run_id"]
    assert record["prepared_at"] == questionnaire["prepared_at"]
    assert record["commit"] == questionnaire["commit"] == _head_of(root)
    assert record["question_set_sha256"] == questionnaire["question_set_sha256"]
    assert record["source_sha256"] == questionnaire["source_sha256"]
    stamp = datetime.fromisoformat(record["recorded_at"])
    assert stamp.utcoffset() is not None
    for field in ("harness", "model", "context", "access"):
        assert isinstance(record[field], str) and record[field]
    assert record["fresh_session"] is True
    assert record["purpose"] == "baseline" and record["target"] is None
    assert record["answers"] == wrong
    assert [verdict["id"] for verdict in record["verdicts"]] == list(QUESTION_IDS)
    assert all(verdict["verdict"] == "incorrect" for verdict in record["verdicts"])
    assert record["correct"] == 0 and record["total"] == 8
    record_leaves = _leaves(record)
    for qid, value in SENTINELS.items():
        if qid != "instructions":
            assert not any(leaf == value for leaf in record_leaves), (
                f"an expected value for '{qid}' travelled into the history"
            )

    head_before = _head_of(root)
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 0, done.stderr
    lines = history.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    assert lines[0] == seed.rstrip("\n")
    assert _head_of(root) == head_before


# ---------------------------------------------------------------------------
# Criterion 8 — bad history and failed appends preserve the old records
# ---------------------------------------------------------------------------


def test_bad_history_and_append_failure_preserve_old_records(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An unreadable history, a duplicate run id or a failing write reports failure and leaves the old bytes standing.

    Fault this pins: a truncated last record silently repaired, an unsupported
    history accepted, a duplicate run id recorded twice, or a refused append
    reported as success.
    """
    root = _write_repo(tmp_path / "repo")
    history = root / HISTORY_REL
    history.parent.mkdir(parents=True)
    assert _record(root, tmp_path, _export(root), dict(SENTINELS)).returncode == 0
    good = history.read_text(encoding="utf-8")

    cases = {
        "truncated": good + '{"schema_version": 1, "run_id": "trunc',
        "unsupported-schema": good + json.dumps({"schema_version": 99, "run_id": "x"}) + "\n",
        "blank-line": good + "\n",
        "not-an-object": good + json.dumps(["a", "b"]) + "\n",
        "no-run-id": good + json.dumps({"schema_version": 1}) + "\n",
    }
    for name, content in cases.items():
        history.write_text(content, encoding="utf-8")
        done = _record(root, tmp_path, _export(root), dict(SENTINELS))
        assert done.returncode == 3, f"{name}: the bad history was accepted"
        assert history.read_text(encoding="utf-8") == content, f"{name}: the history was changed"

    questionnaire = _export(root)
    previous = json.loads(good)
    previous["run_id"] = questionnaire["run_id"]
    seed = json.dumps(previous) + "\n"
    history.write_text(seed, encoding="utf-8")
    done = _record(root, tmp_path, questionnaire, dict(SENTINELS))
    assert done.returncode == 3
    assert "not measured" in done.stderr
    assert history.read_text(encoding="utf-8") == seed

    # A failing append rolls back to the original end position, in process.
    history.write_text(good, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("outcome_test_fixture_copy", root / "scripts" / SCRIPT_NAME)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def _broken_fsync(_handle: int) -> None:
        raise OSError("injected write failure")

    monkeypatch.setattr(module, "_fsync", _broken_fsync)
    qpath = tmp_path / "questionnaire.json"
    qpath.write_text(json.dumps(_export(root)), encoding="utf-8")
    apath = tmp_path / "answers.json"
    apath.write_text(json.dumps(dict(SENTINELS)), encoding="utf-8")
    argv = [
        "record",
        "--questionnaire",
        str(qpath),
        "--answers",
        str(apath),
        "--harness",
        "claude-code",
        "--model",
        "m",
        "--context",
        "c",
        "--access",
        "a",
        "--fresh-session",
        "--purpose",
        "baseline",
    ]
    assert module.main(argv) == 3
    assert history.read_text(encoding="utf-8") == good, "a failed append changed the old bytes"

    # A history locked by another writer refuses, then records once free.
    with history.open("rb") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        started = time.monotonic()
        done = _record(root, tmp_path, _export(root), dict(SENTINELS))
        waited = time.monotonic() - started
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    assert done.returncode == 3, "a locked history recorded anyway"
    assert waited < 60, "the tool waited unreasonably long on the lock"
    assert history.read_text(encoding="utf-8") == good
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 0, done.stderr
    assert len(history.read_text(encoding="utf-8").splitlines()) == 2


# ---------------------------------------------------------------------------
# Criterion 10 — the tool's only write is the explicit history
# ---------------------------------------------------------------------------


def test_tool_only_writes_explicit_history(tmp_path: Path) -> None:
    """The tool's only repository write is the explicit history append: no tracker, no git mutation, no substituted output path, no model shortcut.

    Fault this pins: a side effect through a substituted result path, a
    tracker or git write, or a model/API client in the measurement path.
    """
    root = _write_repo(tmp_path / "repo")
    outside = tmp_path / "outside"
    outside.mkdir()

    def _tree() -> dict[str, bytes]:
        found: dict[str, bytes] = {}
        for path in sorted(root.rglob("*")):
            if path.is_file():
                found[str(path.relative_to(root))] = path.read_bytes()
        return found

    before = _tree()
    head_before = _head_of(root)
    done = _record(
        root,
        tmp_path,
        _export(root),
        dict(SENTINELS),
        env_extra={"OUTCOME_TEST_RESULTS": str(outside / "substituted.jsonl")},
    )
    assert done.returncode in (0, 1)
    assert list(outside.iterdir()) == [], "an env-var substitution took the write"

    after = _tree()
    changed = {name for name in set(before) | set(after) if before.get(name) != after.get(name)}
    assert changed == {HISTORY_REL}, f"unexpected repository writes: {sorted(changed)}"
    assert not any(element.is_dir() and element.name == "__pycache__" for element in root.rglob("*"))
    assert _head_of(root) == head_before
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert status.stdout.splitlines() == [f"?? {HISTORY_REL}"]

    source = (REPO_ROOT / "scripts" / SCRIPT_NAME).read_text(encoding="utf-8")
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert imported <= {
        "__future__",
        "argparse",
        "ast",
        "collections",
        "datetime",
        "fcntl",
        "hashlib",
        "json",
        "math",
        "os",
        "pathlib",
        "re",
        "subprocess",
        "stat",
        "sys",
        "time",
        "typing",
        "uuid",
    }, f"the measurement path carries a foreign client: {sorted(imported)}"

    # A symlink anywhere in the history's path refuses the write.
    target_dir = tmp_path / "symlink-target"
    target_dir.mkdir()
    shutil.rmtree(root / "docs" / "research")
    (root / "docs" / "research").symlink_to(target_dir, target_is_directory=True)
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 3
    assert list(target_dir.iterdir()) == [], "the write travelled through the symlink"

    (root / "docs" / "research").unlink()
    (root / "docs" / "research").mkdir()
    outside_file = tmp_path / "outside-file.jsonl"
    outside_file.write_text("elsewhere\n", encoding="utf-8")
    (root / HISTORY_REL).symlink_to(outside_file)
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 3
    assert outside_file.read_text(encoding="utf-8") == "elsewhere\n", "the symlinked history was written through"


def _module(root: Path) -> Any:
    spec = importlib.util.spec_from_file_location("outcome_repair_fixture", root / "scripts" / SCRIPT_NAME)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_new_history_rollback_removes_created_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A refused recheck or failed first append leaves the original absent history absent."""
    root = _write_repo(tmp_path / "repo")
    module = _module(root)
    history = root / HISTORY_REL

    def refuse() -> None:
        raise module.NotMeasured("snapshot moved")

    with pytest.raises(module.NotMeasured):
        module._append_record({"run_id": "new"}, refuse)
    assert not history.parent.exists(), "a refused run created a result directory"

    calls = 0

    def refuse_second_check() -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise module.NotMeasured("snapshot moved just before append")

    with pytest.raises(module.NotMeasured):
        module._append_record({"run_id": "new"}, refuse_second_check)
    assert not history.parent.exists(), "a late refusal left newly created paths"

    def fail_sync(_handle: int) -> None:
        raise OSError("injected sync failure")

    monkeypatch.setattr(module, "_fsync", fail_sync)
    with pytest.raises(module.NotMeasured):
        module._append_record({"run_id": "new"}, lambda: None)
    assert not history.parent.exists(), "a failed run left its new file or directory"
    history.parent.mkdir()
    with pytest.raises(module.NotMeasured):
        module._append_record({"run_id": "new"}, lambda: None)
    assert history.parent.is_dir() and not history.exists(), "remove only paths created by this run"


def test_history_requires_regular_file(tmp_path: Path) -> None:
    """Directories and FIFOs refuse with exit 3, without an exception or unbounded wait."""
    root = _write_repo(tmp_path / "repo")
    history = root / HISTORY_REL
    history.parent.mkdir()
    questionnaire = _export(root)
    history.mkdir()
    done = _record(root, tmp_path, questionnaire, dict(SENTINELS))
    assert done.returncode == 3 and "Traceback" not in done.stderr
    history.rmdir()
    os.mkfifo(history)
    done = _record(root, tmp_path, questionnaire, dict(SENTINELS))
    assert done.returncode == 3 and "Traceback" not in done.stderr, "a FIFO must be refused as not measured"
    assert "regular file" in done.stderr, "a FIFO must be refused because it is not a regular file"
    assert history.is_fifo()


def test_declared_resolver_and_known_ids(tmp_path: Path) -> None:
    """The declared resolver changes the reading; unknown identities refuse before export."""
    root = _write_repo(tmp_path / "repo")
    path = root / "scripts" / QUESTION_SET_NAME
    document = json.loads(path.read_text())
    document["questions"][0]["resolver"] = "repair-fallback"
    path.write_text(json.dumps(document))
    _commit(root, "switch resolver")
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 1, "changing the declared resolver must change grading"
    assert _verdict_map(_history(root)[-1])["repair-model"] == "incorrect"
    document["questions"][0]["id"] = "unknown"
    path.write_text(json.dumps(document))
    _commit(root, "unknown identity")
    assert _run_tool(root, "questions").returncode == 3


def test_instruction_declaration_controls_answer(tmp_path: Path) -> None:
    """A differently named declaration changes grading, while question text gives no solution."""
    root = _write_repo(tmp_path / "repo")
    path = root / "AGENTS.md"
    path.write_text(path.read_text().replace("`AGENTS.md` is the only", "`policies/SESSION.md` is the only"))
    _commit(root, "name another instruction file")
    document = _export(root)
    question = next(q for q in document["questions"] if q["id"] == "instructions")
    assert "AGENTS.md" not in question["text"], "the eighth question must not print its answer"
    done = _record(root, tmp_path, document, dict(SENTINELS) | {"instructions": "SESSION.md"})
    assert done.returncode == 0, "the declared basename must be read instead of the source basename"
    done = _record(root, tmp_path, _export(root), dict(SENTINELS))
    assert done.returncode == 1
    assert _verdict_map(_history(root)[-1])["instructions"] == "incorrect"


def test_fallback_identifier_ignores_surrounding_prose(tmp_path: Path) -> None:
    """Capitalised multiword prose cannot become part of the fallback identifier."""
    root = _write_repo(tmp_path / "repo")
    for name in ("Sonnet 5.5", "glm_5_3", "openai/gpt-6"):
        text = _sources_text(repair_fallback=name)["docs/WORKFLOW.md"]
        text = text.replace(
            f"one sandboxed attempt; one fresh retry after a failed check, and {name} at effort `low`",
            f"One sandboxed attempt then {name}",
        )
        (root / "docs/WORKFLOW.md").write_text(text)
        _commit(root, "fallback identifier changed")
        done = _record(root, tmp_path, _export(root), dict(SENTINELS) | {"repair-fallback": name})
        assert done.returncode == 0, f"the full fallback identifier {name!r} must be read: {done.stderr}"


def test_history_requires_complete_record(tmp_path: Path) -> None:
    """Syntactically valid history still needs all supported record fields."""
    root = _write_repo(tmp_path / "repo")
    assert _record(root, tmp_path, _export(root), dict(SENTINELS)).returncode == 0
    history = root / HISTORY_REL
    row = _history(root)[0]
    questionnaire = _export(root)
    for field in set(row) - {"schema_version", "run_id"}:
        incomplete = {key: value for key, value in row.items() if key != field}
        raw = json.dumps(incomplete) + "\n"
        history.write_text(raw)
        done = _record(root, tmp_path, questionnaire, dict(SENTINELS))
        assert done.returncode == 3, f"history missing {field} must be refused"
        assert history.read_text() == raw


def test_schema_versions_require_integer(tmp_path: Path) -> None:
    """True and 1.0 are not schema version integers, in any supported document."""
    root = _write_repo(tmp_path / "repo")
    module = _module(root)
    qset = module._load_question_set()
    questionnaire = _export(root)
    qpath = tmp_path / "questionnaire.json"
    question_path = root / "scripts" / QUESTION_SET_NAME
    questions = json.loads(question_path.read_text())
    for value in (True, 1.0):
        question_path.write_text(json.dumps(questions | {"schema_version": value}))
        with pytest.raises(module.NotMeasured, match="schema_version"):
            module._load_question_set()
        qpath.write_text(json.dumps(questionnaire | {"schema_version": value}))
        with pytest.raises(module.NotMeasured, match="schema_version"):
            module._load_questionnaire(qpath, qset)
        with pytest.raises(module.NotMeasured, match="schema_version"):
            module._validate_history((json.dumps({"schema_version": value, "run_id": "x"}) + "\n").encode())


def test_history_rejects_duplicate_keys(tmp_path: Path) -> None:
    """History uses the same duplicate-key refusal as input documents."""
    root = _write_repo(tmp_path / "repo")
    assert _record(root, tmp_path, _export(root), dict(SENTINELS)).returncode == 0
    history = root / HISTORY_REL
    row = _history(root)[0]
    for field in ("run_id", "schema_version"):
        raw = json.dumps(row)[:-1] + f', "{field}": ' + json.dumps(row[field]) + "}\n"
        history.write_text(raw)
        done = _record(root, tmp_path, _export(root), dict(SENTINELS))
        assert done.returncode == 3, f"duplicate {field} must refuse history"
        assert history.read_text() == raw


def test_questions_refuses_unread_readers(tmp_path: Path) -> None:
    """Export refuses ambiguous live evidence before a subject session is started."""
    root = _write_repo(tmp_path / "repo")
    path = root / "AGENTS.md"
    path.write_text(path.read_text() + "\nUse `another/bd`, never bare `bd`.\n")
    _commit(root, "ambiguous tracker rule")
    done = _run_tool(root, "questions")
    assert done.returncode == 3 and done.stdout == "", "unread evidence must prevent questionnaire export"
    assert "not measured" in done.stderr
