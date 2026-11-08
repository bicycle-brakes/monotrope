#!/usr/bin/env python3
"""outcome_test.py — measure a fresh session's answers against the live repository.

The gates check artefacts; this tool checks what a freshly started session can
still answer about the harness itself. `questions` prints one questionnaire —
eight fixed questions plus the run's commit and source fingerprints — for the
administrator to hand to a separately started session. `record` re-reads the
same sources on the same commit, derives every expected answer anew, grades
the session's submission deterministically, and appends exactly one JSONL line
to `docs/research/outcome-test-results.jsonl`.

No expected value is ever stored, cached or shipped: the questionnaire carries
questions and answer shapes only. Repository records carry eight verdicts;
submitted answers are retained only in the external user state directory. Exit codes for `record`: 0 = eight correct,
1 = measured with incorrect answers, 3 = not measured (refusals and failures;
nothing is appended).

Usage:
    python3 scripts/outcome_test.py questions
    python3 scripts/outcome_test.py record --questionnaire Q.json --answers A.json \
        --harness TEXT --model TEXT --context TEXT --access TEXT --fresh-session \
        --purpose baseline [--target AGENTS.md|handover-convention]

A foreign session is started through the existing `scripts/stage2.py` path;
this tool starts no session and calls no model. Its only repository write is
the history; full answers stay in the external user state directory.
"""

from __future__ import annotations

import argparse
import ast
import fcntl
import hashlib
import json
import math
import os
import re
import stat
import subprocess
import sys
import time
import uuid
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
QUESTION_FILE = HERE.parent / "outcome_test_questions.json"
RESULTS_PATH = ROOT / "docs" / "research" / "outcome-test-results.jsonl"

SCHEMA_VERSION = 1
QUESTION_COUNT = 8
QUESTION_FIELDS = {"id", "text", "answer_type", "source"}
ANSWER_TYPES = ("string", "directory", "number")
PURPOSES = {"baseline", "pre-change"}
TARGETS = {"AGENTS.md", "handover-convention"}
KNOWN_RESOLVERS = frozenset(
    {
        "repair-model",
        "repair-fallback",
        "verify-floor",
        "verify-floor-override",
        "run-plans",
        "handovers",
        "tracker-command",
        "instructions",
    }
)

EXIT_ALL_CORRECT = 0
EXIT_INCORRECT = 1
EXIT_NOT_MEASURED = 3

GIT_TIMEOUT = 30.0
LOCK_RETRY_SECONDS = 5.0
LOCK_RETRY_PAUSE = 0.1

ROUTING_HEADING = "The routing"
HANDOVER_HEADING = "The eighth movement"
RUN_PLAN_HEADING = "What a lane is"
REPAIR_ROW_LABEL = "Repair after 4b and 6"

HEADING = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.*?)\s*$")
LINK = re.compile(r"\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)\)")
DATED_PREFIX = re.compile(r"\d{4}-\d{2}-\d{2}")
RUN_PLAN_NAME = re.compile(r"run[-_]plan")
HANDOVER_PATH = re.compile(r"(?P<path>(?:[\w.-]+/)*<date>-<name>\.md)")
TRACKER_RULE = re.compile(r"Use `(?P<command>[^`]+)`, never bare `(?P<bare>[^`]+)`")
DECLARATION = re.compile(r"(?P<name>`[^`]+`|[\w./-]+)\s+is the only instruction file")
HEX40 = re.compile(r"[0-9a-f]{40}")
HEX64 = re.compile(r"[0-9a-f]{64}")


class NotMeasured(Exception):
    """A refusal or a failure: exit 3, nothing appended."""


class Reading(NamedTuple):
    """One source reader's outcome: the derived value, or why nothing was read."""

    value: Any
    reason: str

    @classmethod
    def ok(cls, value: Any) -> Reading:
        return cls(value, "")

    @classmethod
    def unread(cls, reason: str) -> Reading:
        return cls(None, reason)

    @property
    def read(self) -> bool:
        return self.reason == ""


class QuestionSet(NamedTuple):
    ids: list[str]
    questions: list[dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    sources: list[str]


class DuplicateJsonKey(ValueError):
    """A JSON object in an input carries the same key twice."""


# ---------------------------------------------------------------------------
# source readers — every expected answer is derived here, at recording time
# ---------------------------------------------------------------------------


def _section(text: str, fragment: str) -> str | None:
    """The Markdown section under the first heading whose title contains `fragment`."""
    lines = text.splitlines()
    start: int | None = None
    level = 0
    for index, line in enumerate(lines):
        match = HEADING.match(line)
        if match is None:
            continue
        if start is None:
            if fragment in match.group("title"):
                start = index
                level = len(match.group("level"))
        elif len(match.group("level")) <= level:
            return "\n".join(lines[start:index])
    if start is not None:
        return "\n".join(lines[start:])
    return None


def _table_rows(block: str) -> list[list[str]]:
    """The pipe-table rows of a section, one stripped cell list per row."""
    rows: list[list[str]] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and len(stripped) >= 2:
            rows.append([cell.strip() for cell in stripped[1:-1].split("|")])
    return rows


def _plain_text(cell: str) -> str | None:
    """A cell with emphasis, backticks and link targets removed, or None when empty."""
    text = LINK.sub(r"\1", cell).replace("**", "").replace("`", "").strip()
    return text or None


def _repair_row(workflow: str) -> Reading:
    """The routing table's repair row, as cells."""
    section = _section(workflow, ROUTING_HEADING)
    if section is None:
        return Reading.unread("the routing section is absent from docs/WORKFLOW.md")
    rows = [cells for cells in _table_rows(section) if cells and cells[0] == REPAIR_ROW_LABEL]
    if len(rows) != 1:
        return Reading.unread(f"expected exactly one '{REPAIR_ROW_LABEL}' row in the routing table, found {len(rows)}")
    return Reading.ok(rows[0])


def _read_repair_model(workflow: str) -> Reading:
    row = _repair_row(workflow)
    if not row.read:
        return row
    cells: list[str] = row.value
    if len(cells) < 2:
        return Reading.unread("the routing row carries no model cell")
    name = _plain_text(cells[1])
    if name is None or re.fullmatch(r"\S+", name) is None:
        return Reading.unread("the routing row's model cell is not exactly one identifier")
    return Reading.ok(name)


def _read_repair_fallback(workflow: str) -> Reading:
    row = _repair_row(workflow)
    if not row.read:
        return row
    # Work within the routing row's explanatory cell, then isolate the
    # identifier clause. Capitalisation is not a boundary for model names.
    names: list[str] = []
    for cell in row.value[2:]:
        for match in re.finditer(r"\s+after two failed\b", cell):
            prefix = cell[: match.start()]
            prefix = re.sub(r"\s+at effort\s+(?:`[^`]+`|[\w-]+)\s*$", "", prefix)
            clauses = re.split(r"[;,]|\b(?:and|then)\s+", prefix)
            if len(clauses) < 2:
                return Reading.unread("the fallback has no supported identifier clause")
            clause = clauses[-1].strip()
            name = _plain_text(clause)
            if name:
                names.append(name)
    if len(names) != 1:
        return Reading.unread("expected exactly one fallback identifier clause in the routing row")
    return Reading.ok(names[0])


def _read_literal(source: str, name: str, kind: str) -> Reading:
    """One module-level literal assignment, read by parsing alone — never by importing."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return Reading.unread(f"the source does not parse as Python, so '{name}' stays unread")
    found: list[ast.expr] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            candidates = [(target, node.value) for target in node.targets]
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            candidates = [(node.target, node.value)]
        else:
            continue
        for target, value in candidates:
            if isinstance(target, ast.Name) and target.id == name:
                found.append(value)
    if len(found) != 1:
        return Reading.unread(f"expected exactly one module-level assignment to '{name}', found {len(found)}")
    literal = found[0]
    if kind == "number":
        if (
            not isinstance(literal, ast.Constant)
            or isinstance(literal.value, bool)
            or not isinstance(literal.value, int | float)
        ):
            return Reading.unread(f"'{name}' is not a plain numeric literal")
        if not math.isfinite(literal.value):
            return Reading.unread(f"'{name}' is not finite")
        return Reading.ok(literal.value)
    if not isinstance(literal, ast.Constant) or not isinstance(literal.value, str):
        return Reading.unread(f"'{name}' is not a plain string literal")
    return Reading.ok(literal.value)


def _resolve_link(base_parts: list[str], target: str) -> str | None:
    """A repository-relative link resolved against `base_parts`, or None when it escapes."""
    resolved = list(base_parts)
    for part in target.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not resolved:
                return None
            resolved.pop()
        else:
            resolved.append(part)
    return "/".join(resolved) if resolved else None


def _read_run_plans(orchestration: str) -> Reading:
    section = _section(orchestration, RUN_PLAN_HEADING)
    if section is None:
        return Reading.unread("the 'What a lane is' section is absent from docs/orchestration.md")
    directories: set[str] = set()
    for match in LINK.finditer(section):
        target = match.group("target")
        if target.startswith("/"):
            continue
        stem = target.split("#", 1)[0].rsplit("/", 1)[-1]
        if DATED_PREFIX.match(stem) is None or RUN_PLAN_NAME.search(target) is None:
            continue
        resolved = _resolve_link(["docs"], target)
        if resolved is None:
            return Reading.unread("a dated run-plan link resolves outside the repository")
        directories.add("/".join(resolved.split("/")[:-1]))
    if len(directories) != 1:
        return Reading.unread(
            f"expected all dated run-plan links in one directory, found {sorted(d for d in directories if d) or 'none'}"
        )
    return Reading.ok(directories.pop())


def _read_handovers(workflow: str) -> Reading:
    section = _section(workflow, HANDOVER_HEADING)
    if section is None:
        return Reading.unread("the session-handover section is absent from docs/WORKFLOW.md")
    directories = {"/".join(match.group("path").split("/")[:-1]) for match in HANDOVER_PATH.finditer(section)}
    if "" in directories:
        return Reading.unread("the handover artefact path carries no directory")
    if len(directories) != 1:
        return Reading.unread(f"expected one handover directory, found {sorted(directories) or 'none'}")
    return Reading.ok(directories.pop())


def _read_tracker_rule(agents: str) -> Reading:
    matches = TRACKER_RULE.findall(agents)
    if len(matches) != 1:
        return Reading.unread(f"expected exactly one 'Use ..., never bare ...' house rule, found {len(matches)}")
    command = matches[0][0].strip()
    if not command:
        return Reading.unread("the tracker house rule names no executable")
    return Reading.ok(command)


def _read_instructions(agents: str, source: str) -> Reading:
    opening: list[str] = []
    for line in agents.splitlines():
        if re.match(r"^##\s", line):
            break
        opening.append(line)
    declarations = list(DECLARATION.finditer("\n".join(opening)))
    count = len(declarations)
    if count != 1:
        return Reading.unread(
            f"expected exactly one sole-instruction-file declaration in the opening of {source}, found {count}"
        )
    declared = declarations[0].group("name").strip("`")
    # "This" names the document containing the declaration; explicit names
    # refer to that named file, even when the source document stays in place.
    return Reading.ok(PurePosixPath(source if declared == "This" else declared).name)


def _expected_answer(qid: str, texts: dict[str, str], by_id: dict[str, dict[str, Any]]) -> Reading:
    """The live expected answer for one question id, derived from its named source."""
    question = by_id[qid]
    text = texts[question["source"]]
    resolver = question["resolver"]
    if resolver == "repair-model":
        return _read_repair_model(text)
    if resolver == "repair-fallback":
        return _read_repair_fallback(text)
    if resolver == "verify-floor":
        return _read_literal(text, "DEFAULT_MEMORY_FLOOR", "number")
    if resolver == "verify-floor-override":
        return _read_literal(text, "FLOOR_ENV", "string")
    if resolver == "run-plans":
        return _read_run_plans(text)
    if resolver == "handovers":
        return _read_handovers(text)
    if resolver == "tracker-command":
        return _read_tracker_rule(text)
    if resolver == "instructions":
        return _read_instructions(text, question["source"])
    return Reading.unread(f"no source reader is registered for '{qid}'")


# ---------------------------------------------------------------------------
# grading
# ---------------------------------------------------------------------------


def _grade(answer: Any, expected: Any, answer_type: str) -> bool:
    """One verdict: exact per shape, no substring, no synonyms, no partial credit."""
    if answer_type == "number":
        if isinstance(answer, bool) or not isinstance(answer, int | float):
            return False
        if not math.isfinite(answer):
            return False
        return float(answer) == float(expected)
    if not isinstance(answer, str):
        return False
    text = answer.strip()
    if not text:
        return False
    if answer_type == "directory":
        return text.rstrip("/") == str(expected).rstrip("/")
    return text == str(expected)


def _verdicts(answers: dict[str, Any], expected: dict[str, Any], qset: QuestionSet) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for qid in qset.ids:
        passed = _grade(answers.get(qid), expected[qid], qset.by_id[qid]["answer_type"])
        out.append({"id": qid, "verdict": "correct" if passed else "incorrect"})
    return out


# ---------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateJsonKey(key)
        out[key] = value
    return out


def _load_json_strict(path: Path) -> Any:
    try:
        raw = path.read_bytes()
    except OSError:
        raise NotMeasured(f"cannot read {path.name}") from None
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except UnicodeDecodeError:
        raise NotMeasured(f"{path.name} is not valid UTF-8") from None
    except json.JSONDecodeError:
        raise NotMeasured(f"{path.name} is not valid JSON") from None
    except DuplicateJsonKey:
        raise NotMeasured(f"{path.name} carries a duplicate JSON key") from None


def _escapes(relative: str) -> bool:
    pure = PurePosixPath(relative)
    return pure.is_absolute() or ".." in pure.parts


def _supported_version(value: Any) -> bool:
    return type(value) is int and value == SCHEMA_VERSION


def _load_question_set() -> QuestionSet:
    document = _load_json_strict(QUESTION_FILE)
    if not isinstance(document, dict) or not _supported_version(document.get("schema_version")):
        raise NotMeasured("the question set has an unsupported schema_version")
    questions = document.get("questions")
    if not isinstance(questions, list) or len(questions) != QUESTION_COUNT:
        raise NotMeasured(f"the question set must hold exactly {QUESTION_COUNT} questions")
    by_id: dict[str, dict[str, Any]] = {}
    sources: set[str] = set()
    for entry in questions:
        if not isinstance(entry, dict) or set(entry) != QUESTION_FIELDS | {"resolver"}:
            raise NotMeasured("a question entry has unexpected fields")
        for field in ("id", "text", "answer_type", "source", "resolver"):
            if not isinstance(entry[field], str) or not entry[field].strip():
                raise NotMeasured(f"a question entry carries a non-text {field!r}")
        qid = entry["id"]
        if qid not in KNOWN_RESOLVERS:
            raise NotMeasured("the question set carries an unknown question id")
        if entry["answer_type"] not in ANSWER_TYPES:
            raise NotMeasured(f"question '{qid}' carries an unsupported answer type")
        if entry["resolver"] not in KNOWN_RESOLVERS:
            raise NotMeasured(f"question '{qid}' names an unknown source resolver")
        if qid in by_id:
            raise NotMeasured(f"duplicate question id '{qid}' in the question set")
        if _escapes(entry["source"]):
            raise NotMeasured(f"question '{qid}' names a source outside the repository")
        by_id[qid] = entry
        sources.add(entry["source"])
    ids = [entry["id"] for entry in questions]
    return QuestionSet(ids=ids, questions=questions, by_id=by_id, sources=sorted(sources))


def _question_entries(qset: QuestionSet) -> list[dict[str, str]]:
    """The question shape the answering session receives: identity, text, shape, source."""
    return [
        {"id": q["id"], "text": q["text"], "answer_type": q["answer_type"], "source": q["source"]}
        for q in qset.questions
    ]


def _load_questionnaire(path: Path | None, qset: QuestionSet) -> dict[str, Any]:
    if path is None:
        raise NotMeasured("--questionnaire is required")
    document = _load_json_strict(path)
    if not isinstance(document, dict):
        raise NotMeasured("the questionnaire is not a JSON object")
    if not _supported_version(document.get("schema_version")):
        raise NotMeasured("the questionnaire has an unsupported schema_version")
    run_id = document.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise NotMeasured("the questionnaire carries no run id")
    prepared_at = document.get("prepared_at")
    if not isinstance(prepared_at, str):
        raise NotMeasured("the questionnaire carries no preparation time")
    try:
        datetime.fromisoformat(prepared_at)
    except ValueError:
        raise NotMeasured("the questionnaire's preparation time is not an ISO-8601 timestamp") from None
    commit = document.get("commit")
    if not isinstance(commit, str) or HEX40.fullmatch(commit) is None:
        raise NotMeasured("the questionnaire's commit is not a full hexadecimal commit")
    digest = document.get("question_set_sha256")
    if not isinstance(digest, str) or HEX64.fullmatch(digest) is None:
        raise NotMeasured("the questionnaire's question fingerprint is not a sha-256 digest")
    sources = document.get("source_sha256")
    if not isinstance(sources, dict) or set(sources) != set(qset.sources):
        raise NotMeasured("the questionnaire's source list does not match the question set")
    for rel, value in sources.items():
        if not isinstance(value, str) or HEX64.fullmatch(value) is None:
            raise NotMeasured(f"the questionnaire's fingerprint for '{rel}' is not a sha-256 digest")
    questions = document.get("questions")
    if not isinstance(questions, list) or len(questions) != QUESTION_COUNT:
        raise NotMeasured(f"the questionnaire must carry exactly {QUESTION_COUNT} questions")
    for entry, wanted in zip(questions, _question_entries(qset), strict=False):
        if not isinstance(entry, dict) or set(entry) != QUESTION_FIELDS or entry != wanted:
            raise NotMeasured("the questionnaire's questions do not match the question set")
    return document


def _load_answers(path: Path | None, qset: QuestionSet) -> dict[str, Any]:
    if path is None:
        raise NotMeasured("--answers is required")
    document = _load_json_strict(path)
    if not isinstance(document, dict):
        raise NotMeasured("the answers file is not a JSON object keyed by question id")
    unknown = sorted(set(document) - set(qset.by_id))
    if unknown:
        raise NotMeasured("the answers carry unknown question ids: " + ", ".join(unknown))
    return document


def _read_source(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError:
        raise NotMeasured(f"cannot read the measured source {path.name}") from None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise NotMeasured(f"the measured source {path.name} is not valid UTF-8") from None


# ---------------------------------------------------------------------------
# git and fingerprints — read-only argument lists, finite timeouts
# ---------------------------------------------------------------------------


def _git(*args: str) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise NotMeasured(f"git {' '.join(args)} did not finish within {GIT_TIMEOUT:.0f}s") from None
    except OSError:
        raise NotMeasured("git is not available") from None
    if done.returncode != 0:
        raise NotMeasured(f"git {' '.join(args)} failed with exit {done.returncode}")
    return done.stdout


def _head_commit() -> str:
    out = _git("rev-parse", "HEAD").strip()
    if HEX40.fullmatch(out) is None:
        raise NotMeasured("this repository has no commit to bind the measurement to")
    return out


def _refuse_dirty_measured_files(qset: QuestionSet) -> None:
    tool = HERE.relative_to(ROOT).as_posix()
    question = QUESTION_FILE.relative_to(ROOT).as_posix()
    out = _git("status", "--porcelain", "--", tool, question, *qset.sources)
    dirty = sorted({line[3:].strip() for line in out.splitlines() if line.strip()})
    if dirty:
        raise NotMeasured(
            "measured files are uncommitted; commit them so one commit and the fingerprints "
            "describe one measurement: " + ", ".join(dirty)
        )


def _sha256_file(path: Path) -> str:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError:
        raise NotMeasured(f"cannot read the measured file {path.name}") from None
    return digest.hexdigest()


def _take_snapshot(qset: QuestionSet) -> dict[str, Any]:
    return {
        "commit": _head_commit(),
        "question_set_sha256": _sha256_file(QUESTION_FILE),
        "source_sha256": {rel: _sha256_file(ROOT / rel) for rel in qset.sources},
    }


def _check_snapshot(snapshot: dict[str, Any], questionnaire: dict[str, Any]) -> None:
    if snapshot["commit"] != questionnaire["commit"]:
        raise NotMeasured("stale snapshot: HEAD moved since the questionnaire was prepared")
    if snapshot["question_set_sha256"] != questionnaire["question_set_sha256"]:
        raise NotMeasured("stale snapshot: the question set changed since the questionnaire was prepared")
    for rel, digest in snapshot["source_sha256"].items():
        if questionnaire["source_sha256"].get(rel) != digest:
            raise NotMeasured(f"stale snapshot: {rel} changed since the questionnaire was prepared")


# ---------------------------------------------------------------------------
# the repository history and external answer archive
# ---------------------------------------------------------------------------


def _fsync(handle: int) -> None:
    os.fsync(handle)


def _reject_symlinks(path: Path) -> None:
    chain: list[Path] = []
    current = path
    while current != ROOT:
        chain.append(current)
        parent = current.parent
        if parent == current:
            break
        current = parent
    for candidate in reversed(chain):
        if candidate.is_symlink():
            raise NotMeasured(
                f"'{candidate}' is a symlink; the result history must live on a real path in the repository"
            )


def _validate_record(row: dict[str, Any]) -> None:
    """Require the complete supported result shape, without deriving old answers."""
    fields = {
        "schema_version",
        "run_id",
        "prepared_at",
        "recorded_at",
        "commit",
        "question_set_sha256",
        "source_sha256",
        "harness",
        "model",
        "context",
        "access",
        "fresh_session",
        "purpose",
        "target",
        "verdicts",
        "correct",
        "total",
    }
    if set(row) != fields:
        raise NotMeasured("the result history carries an incomplete or unsupported record")
    for name in ("run_id", "harness", "model", "context", "access"):
        if not isinstance(row[name], str) or not row[name].strip():
            raise NotMeasured("the result history carries an invalid session label or run id")
    for name in ("prepared_at", "recorded_at"):
        try:
            stamp = datetime.fromisoformat(row[name])
            if stamp.utcoffset() != UTC.utcoffset(None):
                raise ValueError
        except (TypeError, ValueError):
            raise NotMeasured("the result history carries an invalid UTC date") from None
    for name, pattern in (("commit", HEX40), ("question_set_sha256", HEX64)):
        if not isinstance(row[name], str) or pattern.fullmatch(row[name]) is None:
            raise NotMeasured("the result history carries an invalid commit or fingerprint")
    sources = row["source_sha256"]
    if (
        not isinstance(sources, dict)
        or not sources
        or any(
            not isinstance(path, str)
            or _escapes(path)
            or not isinstance(digest, str)
            or HEX64.fullmatch(digest) is None
            for path, digest in sources.items()
        )
    ):
        raise NotMeasured("the result history carries invalid source fingerprints")
    if row["fresh_session"] is not True or not isinstance(row["purpose"], str) or row["purpose"] not in PURPOSES:
        raise NotMeasured("the result history carries invalid measurement metadata")
    if (row["purpose"] == "baseline" and row["target"] is not None) or (
        row["purpose"] == "pre-change" and (not isinstance(row["target"], str) or row["target"] not in TARGETS)
    ):
        raise NotMeasured("the result history carries an invalid target")
    verdicts = row["verdicts"]
    if (
        not isinstance(verdicts, list)
        or len(verdicts) != QUESTION_COUNT
        or any(
            not isinstance(item, dict)
            or set(item) != {"id", "verdict"}
            or not isinstance(item["id"], str)
            or item["id"] not in KNOWN_RESOLVERS
            or item["verdict"] not in ("correct", "incorrect")
            for item in verdicts
        )
        or len({item["id"] for item in verdicts}) != QUESTION_COUNT
    ):
        raise NotMeasured("the result history carries invalid verdicts")
    if (
        type(row["total"]) is not int
        or row["total"] != QUESTION_COUNT
        or (type(row["correct"]) is not int or row["correct"] != sum(item["verdict"] == "correct" for item in verdicts))
    ):
        raise NotMeasured("the result history carries an invalid score")


def _validate_history(raw: bytes) -> list[dict[str, Any]]:
    if raw == b"":
        return []
    if not raw.endswith(b"\n"):
        raise NotMeasured("the result history's last line is incomplete; refusing to repair it")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise NotMeasured("the result history is not valid UTF-8") from None
    rows: list[dict[str, Any]] = []
    for number, segment in enumerate(text.split("\n")[:-1], start=1):
        if not segment.strip():
            raise NotMeasured(f"result history line {number} is blank")
        try:
            row = json.loads(segment, object_pairs_hook=_reject_duplicate_keys)
        except (json.JSONDecodeError, DuplicateJsonKey):
            raise NotMeasured(f"result history line {number} is not valid JSON with unique keys") from None
        if not isinstance(row, dict):
            raise NotMeasured(f"result history line {number} is not a JSON object")
        if not _supported_version(row.get("schema_version")):
            raise NotMeasured(f"result history line {number} has an unsupported schema_version")
        run_id = row.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise NotMeasured(f"result history line {number} carries no run id")
        _validate_record(row)
        rows.append(row)
    return rows


def _read_all(handle: int, size: int) -> bytes:
    os.lseek(handle, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    remaining = size
    while remaining > 0:
        chunk = os.read(handle, min(remaining, 1 << 20))
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _hold_lock(handle: int) -> None:
    deadline = time.monotonic() + LOCK_RETRY_SECONDS
    while True:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except OSError:
            if time.monotonic() >= deadline:
                raise NotMeasured("the result history stayed locked by another writer") from None
            time.sleep(LOCK_RETRY_PAUSE)


def _append_record(record: dict[str, Any], recheck: Callable[[], None]) -> None:
    """One serialized, rollback-able append to the real result file — nothing else is written."""
    line = (json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n").encode("utf-8")
    _reject_symlinks(RESULTS_PATH)
    recheck()
    created_dirs: list[Path] = []
    handle: int | None = None
    succeeded = False
    end: int | None = None
    writing = False
    try:
        missing = RESULTS_PATH.parent
        while not missing.exists():
            created_dirs.append(missing)
            missing = missing.parent
        # Track only directories this attempt actually creates.
        pending = list(reversed(created_dirs))
        created_dirs = []
        for directory in pending:
            try:
                directory.mkdir()
                created_dirs.append(directory)
            except FileExistsError:
                pass
        flags = os.O_RDWR | os.O_NONBLOCK | os.O_NOFOLLOW
        try:
            handle = os.open(RESULTS_PATH, flags | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            handle = os.open(RESULTS_PATH, flags)
        if not stat.S_ISREG(os.fstat(handle).st_mode):
            raise NotMeasured("the result history must be a regular file")
        _hold_lock(handle)
        end = os.fstat(handle).st_size
        rows = _validate_history(_read_all(handle, end))
        if any(row.get("run_id") == record["run_id"] for row in rows):
            raise NotMeasured("this run id is already in the result history")
        recheck()
        os.lseek(handle, 0, os.SEEK_END)
        writing = True
        written = 0
        while written < len(line):
            count = os.write(handle, line[written:])
            if count == 0:
                raise OSError("zero-byte append")
            written += count
        _fsync(handle)
        succeeded = True
    except (OSError, NotMeasured) as exc:
        if writing and handle is not None and end is not None:
            try:
                os.ftruncate(handle, end)
            except OSError:
                raise NotMeasured("writing the result history failed and rollback failed") from None
        if isinstance(exc, NotMeasured):
            raise
        raise NotMeasured("cannot open or write the result history; no measurement recorded") from exc
    finally:
        # Never unlink an opened history: peers may already hold this inode,
        # including waiters that have not appended yet. An empty file is safe.
        if handle is not None:
            os.close(handle)
        if not succeeded:
            for directory in reversed(created_dirs):
                # Cleanup is best effort: a peer may have populated it.
                with suppress(OSError):
                    directory.rmdir()


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------


def _questionnaire_document(qset: QuestionSet) -> dict[str, Any]:
    texts = {rel: _read_source(ROOT / rel) for rel in qset.sources}
    for qid in qset.ids:
        reading = _expected_answer(qid, texts, qset.by_id)
        if not reading.read:
            raise NotMeasured(f"cannot derive the expected answer for '{qid}': {reading.reason}")
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": str(uuid.uuid4()),
        "prepared_at": datetime.now(UTC).isoformat(),
        "commit": _head_commit(),
        "question_set_sha256": _sha256_file(QUESTION_FILE),
        "source_sha256": {rel: _sha256_file(ROOT / rel) for rel in qset.sources},
        "submission_format": "Submit only a JSON object keyed by question id, with each answer as its value. "
        "Use strings for string/directory answers and a JSON number for number answers; no prose or list.",
        "questions": _question_entries(qset),
    }


def _questions_command() -> int:
    try:
        qset = _load_question_set()
        _refuse_dirty_measured_files(qset)
        document = _questionnaire_document(qset)
    except NotMeasured as exc:
        print(f"not measured: {exc}", file=sys.stderr)
        return EXIT_NOT_MEASURED
    print(json.dumps(document, indent=2, sort_keys=True, ensure_ascii=True))
    return EXIT_ALL_CORRECT


def _session_labels(args: argparse.Namespace) -> dict[str, str]:
    labels: dict[str, str] = {}
    for name in ("harness", "model", "context", "access"):
        value = getattr(args, name)
        if not isinstance(value, str) or not value.strip():
            raise NotMeasured(f"--{name} is required as a non-blank label")
        labels[name] = value.strip()
    return labels


def _store_answers(run_id: str, commit: str, answers: dict[str, Any]) -> None:
    """Keep full submissions in a private file outside the measured repository."""
    try:
        if str(uuid.UUID(run_id)) != run_id:
            raise ValueError
    except ValueError:
        raise NotMeasured("the answer archive requires a UUID run id") from None
    state = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state")
    if not state.is_absolute():
        raise NotMeasured("the user state directory must be absolute and outside the repository")
    directory = state / "coding-harness" / "outcome-test"
    if directory.resolve().is_relative_to(ROOT.resolve()):
        raise NotMeasured("the answer archive must be outside the repository")
    path = directory / (run_id + ".json")
    payload = (json.dumps({"run_id": run_id, "commit": commit, "answers": answers}, sort_keys=True) + "\n").encode()
    handle: int | None = None
    created = False
    try:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            created = True
        except FileExistsError:
            # A refused history append may be retried with the same submission.
            if path.is_symlink() or path.read_bytes() != payload:
                raise NotMeasured("the local answer archive already contains a different submission") from None
            return
        with os.fdopen(handle, "wb") as stream:
            handle = None
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError:
        if created:
            with suppress(OSError):
                path.unlink()
        raise NotMeasured("cannot retain submitted answers in the local user state directory") from None
    finally:
        if handle is not None:
            os.close(handle)


def _record(args: argparse.Namespace) -> int:
    labels = _session_labels(args)
    if not args.fresh_session:
        raise NotMeasured("--fresh-session is required: only an attested, separately started session is recorded")
    purpose = args.purpose
    target = args.target
    if purpose not in PURPOSES:
        raise NotMeasured("--purpose must be 'baseline' or 'pre-change'")
    if purpose == "pre-change":
        if target not in TARGETS:
            raise NotMeasured("a pre-change run requires --target AGENTS.md or --target handover-convention")
    elif target is not None:
        raise NotMeasured("--target belongs to pre-change runs only")
    qset = _load_question_set()
    questionnaire = _load_questionnaire(args.questionnaire, qset)
    answers = _load_answers(args.answers, qset)
    _refuse_dirty_measured_files(qset)
    snapshot = _take_snapshot(qset)
    _check_snapshot(snapshot, questionnaire)
    texts = {rel: _read_source(ROOT / rel) for rel in qset.sources}
    expected: dict[str, Any] = {}
    for qid in qset.ids:
        reading = _expected_answer(qid, texts, qset.by_id)
        if not reading.read:
            raise NotMeasured(f"cannot derive the expected answer for '{qid}': {reading.reason}")
        expected[qid] = reading.value
    verdict_list = _verdicts(answers, expected, qset)
    correct = sum(1 for verdict in verdict_list if verdict["verdict"] == "correct")
    record = {
        "schema_version": SCHEMA_VERSION,
        "run_id": questionnaire["run_id"],
        "prepared_at": questionnaire["prepared_at"],
        "recorded_at": datetime.now(UTC).isoformat(),
        "commit": snapshot["commit"],
        "question_set_sha256": snapshot["question_set_sha256"],
        "source_sha256": snapshot["source_sha256"],
        "purpose": purpose,
        "target": target,
        "harness": labels["harness"],
        "model": labels["model"],
        "context": labels["context"],
        "access": labels["access"],
        "fresh_session": True,
        "verdicts": verdict_list,
        "correct": correct,
        "total": QUESTION_COUNT,
    }

    def _recheck() -> None:
        _refuse_dirty_measured_files(qset)
        _check_snapshot(_take_snapshot(qset), questionnaire)

    _store_answers(questionnaire["run_id"], snapshot["commit"], answers)
    _append_record(record, _recheck)
    return correct


def _record_command(args: argparse.Namespace) -> int:
    try:
        correct = _record(args)
    except NotMeasured as exc:
        print(f"not measured: {exc}", file=sys.stderr)
        return EXIT_NOT_MEASURED
    print(f"measured: {correct}/{QUESTION_COUNT} correct")
    return EXIT_ALL_CORRECT if correct == QUESTION_COUNT else EXIT_INCORRECT


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("questions", help="print one questionnaire for a separately started session")
    record = sub.add_parser("record", help="grade submitted answers and append one history line")
    record.add_argument("--questionnaire", type=Path, help="the questionnaire file the administrator exported")
    record.add_argument("--answers", type=Path, help="the answering session's JSON answer object")
    record.add_argument("--harness", help="the harness that ran the answering session")
    record.add_argument("--model", help="the model that answered")
    record.add_argument("--context", help="the startup context the session received")
    record.add_argument("--access", help="the repository access the session was permitted")
    record.add_argument(
        "--fresh-session",
        action="store_true",
        help="the administrator's attestation of a separately started, memory-free session",
    )
    record.add_argument("--purpose", help="why this run is recorded: baseline or pre-change")
    record.add_argument("--target", help="for pre-change runs: AGENTS.md or handover-convention")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "questions":
        return _questions_command()
    return _record_command(args)


if __name__ == "__main__":
    sys.exit(main())
