#!/usr/bin/env python3
"""enqueue_pr.py — admit one eligible pull request to the merge queue at its verified head (bead coding-harness-va1l).

Spec: `plans/changes/enqueue-pr/spec.md`. The command reads the pull request, its head and history, the
phase-6 record of its one change folder, the head's `Closes-Bead` trailer, the required checks of `main`
and the tracker, and refuses unless every condition holds. Only then does it send the one GraphQL
`enqueuePullRequest` mutation, pinned to the verified head through `expectedHeadOid`. It never merges,
never uses an administrative bypass and never retries. Admission is not a merge: a queued request
counts as merged only once GitHub reports it so.

Conditions, in report order (each failure is one stderr line `<condition>: <reason>`; a condition whose
evidence depends on an earlier one that could not be read reports `<condition>: not evaluated: <earlier>`):

  script           this checkout's `scripts/enqueue_pr.py` is the blob on origin's `main`
  pr               open, targets `main`, not a draft, not from a fork
  head             origin's pull ref and `main` fetched; the pull ref is the head GitHub reports
  change           the diff touches exactly one change folder, whose `bead` is the trailer's bead
  trailer          the head carries exactly one `Closes-Bead`, naming a known bead that is not closed
  phase-6          the last `## Phase 6` block is settled; released loop rows are settled and undisputed
  reviewed-commit  that block names its reviewed commit, an ancestor of the head
  post-review      after it only record-only commits, empty commits and clean merges of main
  checks           every required check of `main` (all active rulesets and classic protection) passed
  decision         no `decision` label, no path under `docs/adr/`

`--maintainer` skips change, trailer, phase-6, reviewed-commit, post-review and decision, and keeps the
rest. Until the agent policy follow-up (bead coding-harness-r7zc) is installed it is for attended use only.

The self-check of `script` detects an accidental edit only: an edited script can remove its own check,
and the modules it imports are not compared. It is no security boundary against a hostile checkout.

Usage:
    python3 scripts/enqueue_pr.py <number> [--maintainer]
Exit: 0 queued or already queued · 1 refused, or the head moved · 2 usage error or failed admission.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import uuid
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import venv_guard  # noqa: F401
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import close_merged_beads  # noqa: E402 — the one trailer parser and the one validated tracker reader
import pr_sync  # noqa: E402

CONDITIONS = (
    "script",
    "pr",
    "head",
    "change",
    "trailer",
    "phase-6",
    "reviewed-commit",
    "post-review",
    "checks",
    "decision",
)
MAINTAINER_SKIPS = ("change", "trailer", "phase-6", "reviewed-commit", "post-review", "decision")
PERMITTED_CONCLUSIONS = frozenset({"SUCCESS", "SKIPPED", "NEUTRAL"})
PENDING = "PENDING"
BASE_BRANCH = "main"
SCRIPT_IN_REPO = "scripts/enqueue_pr.py"
CHANGES_DIR = "plans/changes/"
INDEX_PATH = "plans/INDEX.md"
ADR_DIR = "docs/adr/"
DECISION_LABEL = "decision"
TRAILER_KEY = close_merged_beads.TRAILER_KEY
FULL_SHA = re.compile(r"[0-9a-f]{40}")
GIT_SECONDS = 60.0
GH_SECONDS = 120.0
PAGE = 100

# findings.md, as the phase-6 runner writes it (`scripts/stage2.py`). Read at line starts only: a quoted
# line (`> …`) is a reviewer's or an attempt's words, never the runner's.
PHASE6_HEADING = "## Phase 6"
RELEASE_HEADING = "## Phase 4b — loop rows, released"
KEPT_FROM = re.compile(r"Kept from the loop record:[ \t]*")
FINDING_COLUMNS = 9
RELEASED_COLUMNS = 10
LOOP_ID = re.compile(r"L\d+-\d+")
VERDICT_LINE = re.compile(r"Phase 6 verdict:[ \t]+(?!(?i:pending)\b)\S[^\n]*?,[ \t]*\d{4}-\d{2}-\d{2}[ \t]*\.?[ \t]*")
VERDICT_START = re.compile(r"phase 6 verdict\b", re.I)
REVIEWED_COMMIT = re.compile(r"Reviewed commit: ([0-9a-f]{40})[ \t]*")
NO_FINDING = re.compile(r"[^\W_][^\n]*? reported no finding\.[ \t]*")
_PIPE = re.compile(r"(?<!\\)\|")

# The one mutation this command sends: queue admission, pinned to the verified head.
ENQUEUE_MUTATION = (
    "mutation($pullRequestId: ID!, $expectedHeadOid: GitObjectID!) {\n"
    "  enqueuePullRequest(input: {pullRequestId: $pullRequestId, expectedHeadOid: $expectedHeadOid}) {\n"
    "    mergeQueueEntry { position state }\n"
    "  }\n"
    "}"
)
PULL_REQUEST_QUERY = (
    "query($owner: String!, $name: String!, $number: Int!) {\n"
    "  repository(owner: $owner, name: $name) {\n"
    "    pullRequest(number: $number) {\n"
    "      id number state isDraft baseRefName headRefOid isCrossRepository isInMergeQueue\n"
    f"      labels(first: {PAGE}) {{ pageInfo {{ hasNextPage }} nodes {{ name }} }}\n"
    "    }\n"
    "  }\n"
    "}"
)
ROLLUP_QUERY = (
    "query($owner: String!, $name: String!, $oid: GitObjectID!, $after: String) {\n"
    "  repository(owner: $owner, name: $name) {\n"
    "    object(oid: $oid) {\n"
    "      ... on Commit {\n"
    "        statusCheckRollup {\n"
    f"          contexts(first: {PAGE}, after: $after) {{\n"
    "            pageInfo { hasNextPage endCursor }\n"
    "            nodes {\n"
    "              __typename\n"
    "              ... on CheckRun { name status conclusion }\n"
    "              ... on StatusContext { context state }\n"
    "            }\n"
    "          }\n"
    "        }\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "}"
)


class Unreadable(Exception):
    """Evidence that could not be read or established unambiguously: always a refusal, never a pass."""


class AdmissionError(Exception):
    """The enqueue mutation did not admit the request."""


class UsageError(Exception):
    """The invocation is not valid."""


@dataclass(frozen=True)
class PullRequest:
    node_id: str
    number: int
    state: str
    is_draft: bool
    base: str
    head_oid: str
    cross_repository: bool
    in_merge_queue: bool
    labels: tuple[str, ...]


# ---------------------------------------------------------------------------
# GitHub: reads, and the one mutation
# ---------------------------------------------------------------------------


def parse_pull_request(payload: Any, number: int) -> PullRequest:
    """The pull request of a GraphQL answer; anything missing or of another shape is unreadable."""
    try:
        node = payload["data"]["repository"]["pullRequest"]
    except (KeyError, TypeError):
        raise Unreadable("the pull request answer has no data.repository.pullRequest") from None
    if not isinstance(node, dict):
        raise Unreadable(f"GitHub knows no pull request #{number}")
    try:
        labels = node["labels"]
        if labels["pageInfo"]["hasNextPage"] is not False:
            raise Unreadable(f"the pull request carries more than {PAGE} labels; they cannot all be read")
        names = tuple(item["name"] for item in labels["nodes"])
        pr = PullRequest(
            node_id=node["id"],
            number=node["number"],
            state=node["state"],
            is_draft=node["isDraft"],
            base=node["baseRefName"],
            head_oid=node["headRefOid"],
            cross_repository=node["isCrossRepository"],
            in_merge_queue=node["isInMergeQueue"],
            labels=names,
        )
    except (KeyError, TypeError):
        raise Unreadable("the pull request answer lacks a field this command needs") from None
    strings = (pr.node_id, pr.state, pr.base, pr.head_oid, *pr.labels)
    flags = (pr.is_draft, pr.cross_repository, pr.in_merge_queue)
    if not all(isinstance(value, str) and value for value in strings) or not all(isinstance(f, bool) for f in flags):
        raise Unreadable("the pull request answer holds a field of an unexpected type")
    if pr.number != number:
        raise Unreadable(f"GitHub answered for pull request #{pr.number}, not #{number}")
    if not FULL_SHA.fullmatch(pr.head_oid):
        raise Unreadable(f"the reported head {pr.head_oid!r} is no full commit id")
    return pr


def union_required(rules: Any, branch: Any) -> set[str]:
    """The required check names: every active ruleset's rule for the branch, plus classic branch protection.

    `rules` is the answer of `repos/{o}/{r}/rules/branches/{branch}` (the active rules of every ruleset that
    targets the branch), `branch` that of `repos/{o}/{r}/branches/{branch}`. A source of another shape is
    unreadable, never empty.
    """
    required: set[str] = set()
    if not isinstance(rules, list):
        raise Unreadable("the rulesets of main did not answer with a list of rules")
    if len(rules) >= PAGE:
        raise Unreadable(f"main carries {PAGE} or more active rules; more than one page cannot be read")
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
            raise Unreadable("a ruleset rule of main has no type")
        if rule["type"] != "required_status_checks":
            continue
        checks = (rule.get("parameters") or {}).get("required_status_checks")
        if not isinstance(checks, list):
            raise Unreadable("a required_status_checks rule of main lists no checks")
        for check in checks:
            context = check.get("context") if isinstance(check, dict) else None
            if not isinstance(context, str) or not context:
                raise Unreadable("a required_status_checks rule of main names a check without a context")
            required.add(context)
    protection = branch.get("protection") if isinstance(branch, dict) else None
    if not isinstance(branch, dict):
        raise Unreadable("the classic branch protection of main could not be read")
    if protection is None:
        return required
    if not isinstance(protection, dict):
        raise Unreadable("the classic branch protection of main could not be read")
    classic = protection.get("required_status_checks")
    if classic is None:
        return required
    if not isinstance(classic, dict):
        raise Unreadable("the classic required status checks of main are of an unexpected shape")
    contexts = classic.get("contexts", [])
    checks = classic.get("checks", [])
    if not isinstance(contexts, list) or not isinstance(checks, list):
        raise Unreadable("the classic required status checks of main are of an unexpected shape")
    for context in [*contexts, *(item.get("context") if isinstance(item, dict) else None for item in checks)]:
        if not isinstance(context, str) or not context:
            raise Unreadable("a classic required status check of main has no name")
        required.add(context)
    return required


def normalize_rollup(nodes: Any) -> list[tuple[str, str]]:
    """`(name, state)` per check on the head: a conclusion, or `PENDING` while it has none."""
    if not isinstance(nodes, list):
        raise Unreadable("the head's check rollup is of an unexpected shape")
    found: list[tuple[str, str]] = []
    for node in nodes:
        kind = node.get("__typename") if isinstance(node, dict) else None
        if kind == "CheckRun":
            name, status, conclusion = node.get("name"), node.get("status"), node.get("conclusion")
            if not isinstance(name, str) or not isinstance(status, str):
                raise Unreadable("a check run on the head has no name or status")
            if status != "COMPLETED":
                state = PENDING
            elif isinstance(conclusion, str) and conclusion:
                state = conclusion
            else:
                state = "NO CONCLUSION"
        elif kind == "StatusContext":
            name, raw = node.get("context"), node.get("state")
            if not isinstance(name, str) or not isinstance(raw, str):
                raise Unreadable("a status context on the head has no name or state")
            state = PENDING if raw in {"PENDING", "EXPECTED"} else raw
        else:
            raise Unreadable(f"the head's check rollup holds an unknown entry {kind!r}")
        found.append((name, state))
    return found


class GitHub:
    """`gh` against the checkout's repository. `run` is replaceable, so tests see every argument."""

    def __init__(self, root: Path, run: Callable[..., subprocess.CompletedProcess] = subprocess.run) -> None:
        self.root = root
        self._run = run
        self._repo: tuple[str, str] | None = None

    def _gh(self, *args: str) -> subprocess.CompletedProcess:
        try:
            return self._run(["gh", *args], cwd=self.root, capture_output=True, text=True, timeout=GH_SECONDS)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise Unreadable(f"gh {args[0]} could not run: {error}") from None

    def _json(self, *args: str) -> Any:
        result = self._gh(*args)
        if result.returncode != 0:
            diagnostic = (result.stderr or result.stdout or "").strip()
            raise Unreadable(f"gh {' '.join(args[:2])} failed: {diagnostic}")
        try:
            payload = json.loads(result.stdout)
        except (json.JSONDecodeError, TypeError):
            raise Unreadable(f"gh {' '.join(args[:2])} answered no JSON") from None
        if isinstance(payload, dict) and payload.get("errors"):
            raise Unreadable(f"gh {' '.join(args[:2])} answered errors: {payload['errors']}")
        return payload

    def repository(self) -> tuple[str, str]:
        if self._repo is None:
            payload = self._json("repo", "view", "--json", "owner,name")
            try:
                owner, name = payload["owner"]["login"], payload["name"]
            except (KeyError, TypeError):
                raise Unreadable("gh repo view named no owner and name") from None
            if not (isinstance(owner, str) and owner and isinstance(name, str) and name):
                raise Unreadable("gh repo view named no owner and name")
            self._repo = (owner, name)
        return self._repo

    def pull_request(self, number: int) -> PullRequest:
        owner, name = self.repository()
        payload = self._json(
            "api",
            "graphql",
            "-f",
            f"query={PULL_REQUEST_QUERY}",
            "-f",
            f"owner={owner}",
            "-f",
            f"name={name}",
            "-F",
            f"number={number}",
        )
        return parse_pull_request(payload, number)

    def required_checks(self, branch: str) -> set[str]:
        owner, name = self.repository()
        rules = self._json("api", f"repos/{owner}/{name}/rules/branches/{branch}?per_page={PAGE}")
        endpoint = f"repos/{owner}/{name}/branches/{branch}"
        result = self._gh("api", endpoint)
        if result.returncode:
            diagnostic = (result.stderr or result.stdout or "").strip()
            if "HTTP 404" in diagnostic and "Branch not protected" in diagnostic:
                protection = {}
            else:
                raise Unreadable(f"gh api {endpoint} failed: {diagnostic}")
        else:
            try:
                protection = json.loads(result.stdout)
            except (json.JSONDecodeError, TypeError):
                raise Unreadable(f"gh api {endpoint} answered no JSON") from None
        return union_required(rules, protection)

    def head_checks(self, oid: str) -> list[tuple[str, str]]:
        owner, name = self.repository()
        found: list[tuple[str, str]] = []
        after: str | None = None
        for _ in range(50):
            args = ["api", "graphql", "-f", f"query={ROLLUP_QUERY}", "-f", f"owner={owner}", "-f", f"name={name}"]
            args += ["-f", f"oid={oid}"]
            if after is not None:
                args += ["-f", f"after={after}"]
            payload = self._json(*args)
            try:
                commit = payload["data"]["repository"]["object"]
            except (KeyError, TypeError):
                raise Unreadable("the check rollup answer has no data.repository.object") from None
            if not isinstance(commit, dict):
                raise Unreadable(f"GitHub knows no commit {oid}")
            rollup = commit.get("statusCheckRollup")
            if rollup is None:
                return found
            try:
                contexts = rollup["contexts"]
                found += normalize_rollup(contexts["nodes"])
                more = contexts["pageInfo"]["hasNextPage"]
                after = contexts["pageInfo"]["endCursor"]
            except (KeyError, TypeError):
                raise Unreadable("the check rollup answer is of an unexpected shape") from None
            if more is False:
                return found
            if more is not True or not isinstance(after, str) or not after:
                raise Unreadable("the check rollup's paging is of an unexpected shape")
        raise Unreadable("the head carries more checks than this command reads")

    def enqueue(self, node_id: str, head_oid: str) -> dict:
        """The one mutation: `enqueuePullRequest`, pinned to `head_oid`. Never retried here."""
        try:
            result = self._gh(
                "api",
                "graphql",
                "-f",
                f"query={ENQUEUE_MUTATION}",
                "-f",
                f"pullRequestId={node_id}",
                "-f",
                f"expectedHeadOid={head_oid}",
            )
        except Unreadable as error:
            raise AdmissionError(str(error)) from None
        if result.returncode != 0:
            raise AdmissionError((result.stderr or result.stdout or "gh failed without a message").strip())
        try:
            payload = json.loads(result.stdout)
            entry = payload["data"]["enqueuePullRequest"]["mergeQueueEntry"]
        except (json.JSONDecodeError, KeyError, TypeError):
            raise AdmissionError("the enqueue answer is of an unexpected shape") from None
        if not isinstance(entry, dict):
            raise AdmissionError("GitHub returned no merge queue entry")
        return entry


def tracker_statuses() -> dict[str, str]:
    """`id -> status` of the tracker, through the one validated reader."""
    try:
        state = close_merged_beads.load_state()
    except close_merged_beads.PreflightError as error:
        raise Unreadable(str(error)) from None
    return {bead: str(row.get("status")) for bead, row in state.items()}


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------


def _git_run(root: Path, *args: str, timeout: float = GIT_SECONDS) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Unreadable(f"git {args[0]} could not run: {error}") from None


def _git_bytes(root: Path, *args: str) -> bytes:
    result = _git_run(root, *args)
    if result.returncode != 0:
        diagnostic = (result.stderr or result.stdout).decode("utf-8", errors="replace").strip()
        raise Unreadable(f"git {args[0]} failed: {diagnostic}")
    return result.stdout


def _git(root: Path, *args: str) -> str:
    return _git_bytes(root, *args).decode("utf-8", errors="replace").strip()


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    result = _git_run(root, "merge-base", "--is-ancestor", ancestor, descendant)
    if result.returncode in (0, 1):
        return result.returncode == 0
    raise Unreadable(f"git merge-base --is-ancestor failed: {result.stderr.decode('utf-8', 'replace').strip()}")


def fetch(root: Path, number: int) -> tuple[str, str]:
    """Origin's `main` and the pull request's head ref, fetched into refs of this run and resolved."""
    token = uuid.uuid4().hex
    main_ref, head_ref = f"refs/enqueue-pr/{token}/main", f"refs/enqueue-pr/{token}/head"
    try:
        _git(
            root,
            "fetch",
            "--quiet",
            "--no-tags",
            "--no-write-fetch-head",
            "--refmap=",
            "origin",
            f"+refs/heads/{BASE_BRANCH}:{main_ref}",
            f"+refs/pull/{number}/head:{head_ref}",
        )
        main = _git(root, "rev-parse", "--verify", f"{main_ref}^{{commit}}")
        head = _git(root, "rev-parse", "--verify", f"{head_ref}^{{commit}}")
    finally:
        for ref in (main_ref, head_ref):
            _git_run(root, "update-ref", "-d", ref)
    if _git(root, "rev-parse", "--is-shallow-repository") == "true":
        raise Unreadable("this checkout is shallow; the head's history cannot be read completely")
    return main, head


def changed_paths(root: Path, main: str, head: str) -> list[str]:
    """The pull request's diff: every path changed between the merge base with main and the head."""
    base = _git(root, "merge-base", main, head)
    raw = _git_bytes(root, "diff", "--name-only", "--no-renames", "-z", base, head)
    return sorted(path.decode("utf-8", errors="replace") for path in raw.split(b"\x00") if path)


def show(root: Path, rev: str, path: str) -> str:
    return _git_bytes(root, "show", f"{rev}:{path}").decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# findings.md
# ---------------------------------------------------------------------------


def split_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if len(stripped) < 2 or not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.strip() for cell in _PIPE.split(stripped[1:-1])]


def malformed_table_line(line: str, cells: list[str] | None) -> bool:
    """Reject non-quoted pipe-bearing lines that cannot be parsed as table rows."""
    return cells is None and "|" in line and not line.lstrip().startswith(">")


def _furniture(cells: list[str]) -> bool:
    return cells[0].lower() in {"id", "#"} or all(re.fullmatch(r":?-+:?", cell) for cell in cells)


def settled(status: str) -> bool:
    return bool(re.fullmatch(r"(?:fixed|rejected)(?:\s*(?:—|:|-|\().*)?", status.strip(), re.IGNORECASE))


def agreed(mark: str) -> bool:
    return bool(re.fullmatch(r"agree(?:\s*(?:—|:|-|\().*)?", mark.strip(), re.IGNORECASE))


def last_phase6_block(text: str) -> list[str] | None:
    """The lines of the last `## Phase 6` block in file order, up to the next `## ` heading."""
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.startswith(PHASE6_HEADING)]
    if not starts:
        return None
    end = next((i for i in range(starts[-1] + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[starts[-1] : end]


def phase6_problems(block: list[str]) -> list[str]:
    """Why the block is not a settled verdict: open rows, unrecognised lines, a missing or doubled verdict."""
    problems: list[str] = []
    rows: list[list[str]] = []
    for line in block[1:]:
        cells = split_row(line)
        if malformed_table_line(line, cells):
            problems.append(f"an unrecognised table line in the block: {line.strip()[:80]}")
            continue
        if cells is None or _furniture(cells):
            continue
        if len(cells) != FINDING_COLUMNS:
            problems.append(f"an unrecognised table line in the block: {line.strip()[:80]}")
            continue
        rows.append(cells)
    for row in rows:
        if not settled(row[7]):
            problems.append(f"finding {row[0]} ({row[1]}) stands `{row[7]}`, not fixed or rejected")
    verdicts = [line for line in block if VERDICT_LINE.fullmatch(line)]
    unrecognised = [line for line in block if VERDICT_START.match(line) and not VERDICT_LINE.fullmatch(line)]
    for line in unrecognised:
        problems.append(f"an unrecognised verdict line: {line.strip()[:80]}")
    if not verdicts:
        problems.append("the block has no recognised `Phase 6 verdict:` line")
    elif len(verdicts) > 1:
        problems.append(f"the block has {len(verdicts)} verdict lines; the verdict is ambiguous")
    statement = any(NO_FINDING.fullmatch(line) for line in block)
    if not rows and not statement:
        problems.append("the block has no finding row and no unquoted `<reviewer> reported no finding.` line")
    if rows and statement:
        problems.append("the block has finding rows and a no-finding statement; the verdict is ambiguous")
    return problems


def released_problems(text: str) -> list[str]:
    """Released phase-4b loop rows that are unsettled or that phase 6 disagreed with; the latest row per id."""
    latest: dict[str, list[str]] = {}
    inside = False
    problems: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.startswith(RELEASE_HEADING)
            continue
        if inside and KEPT_FROM.fullmatch(line):
            inside = False
            continue
        cells = split_row(line) if inside else None
        if inside and malformed_table_line(line, cells):
            problems.append(f"an unrecognised table line in the released block: {line.strip()[:80]}")
            continue
        if cells is None or _furniture(cells):
            continue
        if len(cells) != RELEASED_COLUMNS or not LOOP_ID.fullmatch(cells[0]):
            problems.append(f"an unrecognised table line in the released block: {line.strip()[:80]}")
            continue
        latest[cells[0]] = cells
    for loop_id, cells in latest.items():
        if not settled(cells[7]):
            problems.append(f"released loop row {loop_id} stands `{cells[7]}`, not fixed or rejected")
        if cells[9].strip().lower() in {"—", "no answer", ""}:
            problems.append(f"phase 6 has no answer for released loop row {loop_id}")
        elif cells[9].strip().lower().startswith("disagree"):
            problems.append(f"phase 6 disagrees with released loop row {loop_id}: {cells[9][:80]}")
        elif not agreed(cells[9]):
            problems.append(f"phase 6 has an unrecognised mark for released loop row {loop_id}: {cells[9][:80]}")
    return problems


def front_matter_bead(text: str) -> str | None:
    """The `bead:` of a Markdown header, None when the file has no header or no bead."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        raise Unreadable("a header opens with `---` and never closes")
    try:
        header = yaml.safe_load(text[4:end])
    except yaml.YAMLError as error:
        raise Unreadable(f"a header is not valid YAML ({error})") from None
    if not isinstance(header, dict):
        raise Unreadable("a header is not a mapping")
    bead = header.get("bead")
    if bead is None:
        return None
    if not isinstance(bead, str) or not bead:
        raise Unreadable(f"a header names the bead {bead!r}, which is no bead id")
    return bead


# ---------------------------------------------------------------------------
# The conditions
# ---------------------------------------------------------------------------


@dataclass
class Outcome:
    failures: dict[str, list[str]] = field(default_factory=dict)
    pending: dict[str, str] = field(default_factory=dict)  # not evaluated: its earlier condition
    skipped: list[str] = field(default_factory=list)  # maintainer mode

    def fail(self, condition: str, reasons: Iterable[str]) -> None:
        reasons = list(reasons)
        if reasons:
            self.failures.setdefault(condition, []).extend(reasons)

    def needs(self, condition: str, earlier: str) -> None:
        self.pending[condition] = earlier

    @property
    def refused(self) -> bool:
        return bool(self.failures or self.pending)

    def lines(self) -> list[str]:
        found = []
        for condition in CONDITIONS:
            found += [f"{condition}: {reason}" for reason in self.failures.get(condition, [])]
            if condition in self.pending:
                found.append(f"{condition}: not evaluated: {self.pending[condition]}")
        return found


def pr_problems(pr: PullRequest) -> list[str]:
    problems = []
    if pr.state != "OPEN":
        problems.append(f"the pull request is {pr.state.lower()}, not open")
    if pr.base != BASE_BRANCH:
        problems.append(f"the pull request targets `{pr.base}`, not `{BASE_BRANCH}`")
    if pr.is_draft:
        problems.append("the pull request is a draft")
    if pr.cross_repository:
        problems.append("the pull request comes from a fork")
    return problems


def change_folders(paths: list[str]) -> list[str]:
    folders = set()
    for path in paths:
        parts = path.split("/")
        if path.startswith(CHANGES_DIR) and len(parts) > 3 and parts[2] != "archive":
            folders.add(parts[2])
    return sorted(folders)


def folder_bead(root: Path, head: str, folder: str) -> str:
    listing = _git(root, "ls-tree", "--name-only", head, f"{CHANGES_DIR}{folder}/")
    beads = set()
    for path in listing.splitlines():
        if path.endswith(".md"):
            bead = front_matter_bead(show(root, head, path))
            if bead is not None:
                beads.add(bead)
    if not beads:
        raise Unreadable(f"no header in {CHANGES_DIR}{folder}/ names a bead")
    if len(beads) > 1:
        raise Unreadable(f"the headers in {CHANGES_DIR}{folder}/ name several beads: {', '.join(sorted(beads))}")
    return beads.pop()


def head_trailers(root: Path, head: str) -> tuple[list[str], list[str]]:
    """The head's well-formed `Closes-Bead` values and its malformed ones."""
    message = _git_bytes(root, "log", "-1", "--format=%B", head)
    try:
        lines = close_merged_beads.raw_trailers(message)
    except close_merged_beads.PreflightError as error:
        raise Unreadable(str(error)) from None
    values: list[str] = []
    malformed: list[str] = []
    key = TRAILER_KEY.encode("ascii")
    for line in lines:
        raw_key, _, raw_value = line.partition(b":")
        raw_key = raw_key.rstrip(b" \t")
        if raw_key.lower() != key.lower():
            continue
        raw_value = raw_value.strip(b" \t")
        if raw_key == key and close_merged_beads.BEAD_ID.fullmatch(raw_value):
            values.append(raw_value.decode("ascii"))
        else:
            malformed.append(line.decode("utf-8", errors="replace"))
    return values, malformed


def regenerated_index_matches(root: Path, commit: str) -> bool:
    """Regenerate the index from the merge commit's own tree in an isolated directory."""
    archive = _git_bytes(root, "archive", "--format=tar", commit)
    try:
        with tempfile.TemporaryDirectory(prefix="enqueue-index-") as directory:
            target = Path(directory)
            with tarfile.open(fileobj=io.BytesIO(archive)) as contents:
                contents.extractall(target, filter="data")
            index = target / INDEX_PATH
            expected = index.read_bytes()
            result = subprocess.run(
                [sys.executable, str(target / "scripts/plans_registry.py"), "--index"],
                cwd=target,
                capture_output=True,
                timeout=GIT_SECONDS,
            )
            return result.returncode == 0 and index.read_bytes() == expected
    except (OSError, tarfile.TarError, subprocess.TimeoutExpired):
        return False


def commit_problems(root: Path, commit: str, parents: list[str], folder: str, main: str) -> list[str]:
    """Why one commit after the reviewed one is not allowed there; empty when it is."""
    short = commit[:12]
    if len(parents) == 1:
        options = ("-r", "--no-commit-id", "--no-renames", "--name-only", "-z")
        raw = _git_bytes(root, "diff-tree", *options, parents[0], commit)
        paths = [path.decode("utf-8", errors="replace") for path in raw.split(b"\x00") if path]
        outside = [p for p in paths if not (p.startswith(f"{CHANGES_DIR}{folder}/") or p == INDEX_PATH)]
        if outside:
            listing = ", ".join(outside[:10]) + (" …" if len(outside) > 10 else "")
            return [
                f"commit {short} changes {listing} after the reviewed commit; only record-only commits inside "
                f"{CHANGES_DIR}{folder}/ or {INDEX_PATH}, empty commits and clean merges of main may follow it"
            ]
        return []
    if len(parents) != 2:
        return [f"commit {short} merges {len(parents)} parents; only a merge of main may follow the reviewed commit"]
    if not _is_ancestor(root, parents[1], main):
        return [f"merge {short} brings in {parents[1][:12]}, which is not on origin's main"]
    try:
        clean, conflicts = pr_sync.merge_tree(root, parents[0], parents[1])
    except pr_sync.Failed as error:
        raise Unreadable(str(error)) from None
    if conflicts and conflicts != [INDEX_PATH]:
        return [f"merge {short} of main is not clean; its conflict resolution was not reviewed"]
    actual = _git(root, "rev-parse", f"{commit}^{{tree}}")
    if clean == actual and not conflicts:
        return []
    changed = _git_bytes(root, "diff-tree", "-r", "--no-renames", "--name-only", "-z", clean, actual)
    paths = [path.decode("utf-8", errors="replace") for path in changed.split(b"\0") if path]
    if set(paths) <= {INDEX_PATH} and regenerated_index_matches(root, commit):
        return []
    return [f"merge {short} of main differs from the clean merge of its parents; it changes reviewed code"]


def post_review_problems(root: Path, reviewed: str, head: str, folder: str, main: str) -> list[str]:
    chain = _git(root, "rev-list", "--first-parent", head).split()
    if reviewed not in chain:
        return [f"the reviewed commit {reviewed[:12]} is not on the head's first-parent chain"]
    problems: list[str] = []
    for commit in chain[: chain.index(reviewed)]:
        parents = _git(root, "rev-list", "--parents", "-n", "1", commit).split()[1:]
        problems += commit_problems(root, commit, parents, folder, main)
    return problems


def checks_problems(github: Any, head: str) -> list[str]:
    try:
        required = github.required_checks(BASE_BRANCH)
    except Unreadable as error:
        return [f"the required checks of {BASE_BRANCH} could not be read: {error}"]
    if not required:
        return [f"no required check is declared for {BASE_BRANCH}; the required set cannot be established"]
    try:
        states = github.head_checks(head)
    except Unreadable as error:
        return [f"the checks on the head could not be read: {error}"]
    problems = []
    for name in sorted(required):
        found = [state for check, state in states if check == name]
        if not found:
            problems.append(f"required check `{name}` is absent on the head")
        elif PENDING in found:
            problems.append(f"required check `{name}` is pending on the head")
        else:
            bad = sorted({state for state in found if state not in PERMITTED_CONCLUSIONS})
            if bad:
                problems.append(f"required check `{name}` concluded {', '.join(bad)} on the head")
    return problems


def evaluate(
    root: Path,
    pr: PullRequest,
    github: Any,
    tracker: Callable[[], dict[str, str]],
    maintainer: bool,
) -> Outcome:
    """Every condition, in report order; a dependent one is marked not evaluated, never guessed."""
    out = Outcome()
    out.fail("pr", pr_problems(pr))

    main = head = None
    paths: list[str] | None = None
    try:
        main, fetched = fetch(root, pr.number)
        if fetched != pr.head_oid:
            out.fail("head", [f"GitHub reports head {pr.head_oid}, origin's pull ref holds {fetched}; the head moved"])
        else:
            head = fetched
            paths = changed_paths(root, main, head)
    except Unreadable as error:
        out.fail("head", [f"the head or main could not be fetched and read: {error}"])
        head = paths = None

    if maintainer:
        out.skipped = list(MAINTAINER_SKIPS)
    else:
        _attended_conditions(out, root, pr, tracker, main, head, paths)

    if head is None:
        out.needs("checks", "head")
    else:
        out.fail("checks", checks_problems(github, head))
    return out


def _attended_conditions(
    out: Outcome,
    root: Path,
    pr: PullRequest,
    tracker: Callable[[], dict[str, str]],
    main: str | None,
    head: str | None,
    paths: list[str] | None,
) -> None:
    """change, trailer, phase-6, reviewed-commit, post-review and decision: the default mode's own conditions."""
    folder = folder_bead_id = None
    if head is None or paths is None or main is None:
        for condition in ("change", "trailer"):
            out.needs(condition, "head")
    else:
        folders = change_folders(paths)
        if len(folders) != 1:
            named = f": {', '.join(folders)}" if folders else ""
            out.fail("change", [f"the diff touches {len(folders)} change folders{named}; exactly one is required"])
        else:
            folder = folders[0]
            try:
                folder_bead_id = folder_bead(root, head, folder)
            except Unreadable as error:
                out.fail("change", [str(error)])
        try:
            values, malformed = head_trailers(root, head)
        except Unreadable as error:
            out.fail("trailer", [f"the head's trailers could not be read: {error}"])
        else:
            if malformed:
                out.fail("trailer", [f"malformed {TRAILER_KEY} trailer: {line}" for line in malformed])
            if len(values) != 1:
                count = f"the head carries {len(values)} {TRAILER_KEY} trailers"
                out.fail("trailer", [f"{count}; exactly one is required"])
            elif not malformed:
                try:
                    statuses = tracker()
                except Unreadable as error:
                    out.fail("trailer", [f"the tracker could not be read: {error}"])
                else:
                    status = statuses.get(values[0])
                    if status is None:
                        out.fail("trailer", [f"{TRAILER_KEY} names {values[0]}, which the tracker does not know"])
                    elif status == "closed":
                        out.fail("trailer", [f"{TRAILER_KEY} names {values[0]}, which is closed"])
            if len(values) == 1 and folder_bead_id is not None and values[0] != folder_bead_id:
                named = f"{CHANGES_DIR}{folder}/ names bead {folder_bead_id}"
                out.fail("change", [f"{named}; the head's {TRAILER_KEY} names {values[0]}"])

    block = text = None
    if folder is None or head is None:
        out.needs("phase-6", "change")
    else:
        try:
            text = show(root, head, f"{CHANGES_DIR}{folder}/findings.md")
        except Unreadable as error:
            out.fail("phase-6", [f"{CHANGES_DIR}{folder}/findings.md is not readable at the head: {error}"])
        if text is not None:
            block = last_phase6_block(text)
            if block is None:
                out.fail("phase-6", [f"{CHANGES_DIR}{folder}/findings.md has no `{PHASE6_HEADING}` block"])
            else:
                out.fail("phase-6", phase6_problems(block))
            out.fail("phase-6", released_problems(text))

    reviewed = None
    if block is None:
        out.needs("reviewed-commit", "phase-6")
    else:
        named = [match.group(1) for line in block if (match := REVIEWED_COMMIT.fullmatch(line))]
        if len(named) != 1:
            count = f"the last phase-6 block names {len(named)} reviewed commits"
            out.fail("reviewed-commit", [f"{count}; exactly one is required"])
        else:
            try:
                _git(root, "cat-file", "-e", f"{named[0]}^{{commit}}")
                if _is_ancestor(root, named[0], head):
                    reviewed = named[0]
                else:
                    out.fail("reviewed-commit", [f"the reviewed commit {named[0]} is not an ancestor of the head"])
            except Unreadable as error:
                out.fail("reviewed-commit", [f"the reviewed commit {named[0]} could not be read: {error}"])

    if reviewed is None:
        out.needs("post-review", "reviewed-commit")
    else:
        try:
            out.fail("post-review", post_review_problems(root, reviewed, head, folder, main))
        except Unreadable as error:
            out.fail("post-review", [f"the history after the reviewed commit could not be read: {error}"])

    labelled = DECISION_LABEL in pr.labels
    if labelled:
        out.fail("decision", [f"the pull request carries the `{DECISION_LABEL}` label; it is the maintainer's"])
    if paths is None:
        if not labelled:
            out.needs("decision", "head")
    else:
        adr = ", ".join(path for path in paths if path.startswith(ADR_DIR))
        if adr:
            out.fail("decision", [f"the pull request touches {ADR_DIR} ({adr}); it is the maintainer's"])
        try:
            assert main is not None
            mapping = human_decided_prefixes(root, main)
            reserved = ", ".join(
                path for path in paths if not path.startswith(ADR_DIR) and is_human_decided(path, mapping)
            )
            if reserved:
                out.fail(
                    "decision",
                    [
                        f"the pull request touches paths provenance.yaml reserves for human-decided ({reserved}); it is the maintainer's"
                    ],
                )
        except Unreadable as error:
            out.fail("decision", [f"provenance.yaml could not be read: {error}"])


# ---------------------------------------------------------------------------
# The command
# ---------------------------------------------------------------------------


def human_decided_prefixes(root: Path, ref: str = "origin/main") -> list[tuple[str, bool]]:
    """Read the authoritative main-branch map from `ref`, including non-reserved overrides."""
    try:
        data = yaml.safe_load(show(root, ref, "provenance.yaml"))
    except yaml.YAMLError as error:
        raise Unreadable(f"invalid YAML: {error}") from None
    if not isinstance(data, dict) or not isinstance(data.get("paths"), list):
        raise Unreadable("missing paths list")
    entries = []
    for item in data["paths"]:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("prefix"), str)
            or not isinstance(item.get("allowed"), list)
            or not all(isinstance(value, str) for value in item["allowed"])
        ):
            raise Unreadable("invalid path mapping")
        entries.append((item["prefix"], item["allowed"] == ["human-decided"]))
    if len({prefix for prefix, _ in entries}) != len(entries):
        raise Unreadable("duplicate path mapping")
    return entries


def is_human_decided(path: str, entries: list[tuple[str, bool]]) -> bool:
    matches = [(len(prefix), reserved) for prefix, reserved in entries if path.startswith(prefix)]
    return max(matches)[1] if matches else False


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Accept only `<positive-integer>` or `<positive-integer> --maintainer`.

    The permission rules in `scripts/agent_policy.py` and `.claude/settings.json`
    guard `--maintainer` after the pull request number (`* --maintainer*`).
    Refusing any flag or `--` before `<number>` (and any abbreviation, loop row L2-2)
    ensures no spelling accepted here can enter maintainer mode outside those rules.
    """
    if not argv:
        raise UsageError("the pull request number is required")
    if len(argv) > 2:
        raise UsageError(f"unexpected argument(s): {' '.join(argv[2:])}")
    number_raw = argv[0]
    if not re.fullmatch(r"[1-9][0-9]{0,9}", number_raw):
        raise UsageError(f"the pull request number {number_raw!r} is no positive integer")
    maintainer = False
    if len(argv) == 2:
        if argv[1] != "--maintainer":
            raise UsageError(f"unrecognised argument {argv[1]!r}; only literal --maintainer is accepted after <number>")
        maintainer = True
    return argparse.Namespace(number=int(number_raw), maintainer=maintainer)


def script_integrity(root: Path, script: Path) -> list[str]:
    """Fetch main and check the command before reading the pull request."""
    ref = f"refs/enqueue-pr/{uuid.uuid4().hex}/main"
    try:
        _git(
            root,
            "fetch",
            "--quiet",
            "--no-tags",
            "--no-write-fetch-head",
            "--refmap=",
            "origin",
            f"+refs/heads/{BASE_BRANCH}:{ref}",
        )
        theirs = _git(root, "rev-parse", "--verify", f"{ref}:{SCRIPT_IN_REPO}")
        ours = _git(root, "hash-object", "--", str(script))
        if ours != theirs:
            return [f"this checkout's {SCRIPT_IN_REPO} ({ours[:12]}) differs from origin's main ({theirs[:12]})"]
        return []
    except Unreadable as error:
        return [f"the script could not be compared with origin's main: {error}"]
    finally:
        _git_run(root, "update-ref", "-d", ref)


def run(
    argv: list[str],
    *,
    root: Path,
    github: Any,
    tracker: Callable[[], dict[str, str]],
    script: Path,
) -> int:
    try:
        args = parse_args(argv)
    except UsageError as error:
        print(f"usage: enqueue_pr.py <number> [--maintainer] — {error}", file=sys.stderr)
        return 2
    number = args.number
    problems = script_integrity(root, script)
    if problems:
        print(f"refused: PR #{number} is not admitted to the merge queue.", file=sys.stderr)
        for problem in problems:
            print(f"script: {problem}", file=sys.stderr)
        for condition in CONDITIONS[1:]:
            print(f"{condition}: not evaluated: script", file=sys.stderr)
        return 1
    try:
        pr = github.pull_request(number)
    except Unreadable as error:
        print(f"refused: PR #{number} is not admitted to the merge queue.", file=sys.stderr)
        print(f"pr: the pull request could not be read: {error}", file=sys.stderr)
        for condition in CONDITIONS[2:]:
            print(f"{condition}: not evaluated: pr", file=sys.stderr)
        return 1
    if pr.in_merge_queue:
        print(f"already queued: PR #{number} is in the merge queue; nothing was admitted again.")
        return 0

    outcome = evaluate(root, pr, github, tracker, args.maintainer)
    if outcome.refused:
        print(f"refused: PR #{number} is not admitted to the merge queue (head {pr.head_oid}).", file=sys.stderr)
        for line in outcome.lines():
            print(line, file=sys.stderr)
        return 1

    head = pr.head_oid  # verified: origin's pull ref holds exactly this commit
    try:
        entry = github.enqueue(pr.node_id, head)
    except AdmissionError as error:
        try:
            reread = github.pull_request(number)
            reported: str | None = reread.head_oid
        except Unreadable:
            reported = None
        if reported is not None and reported != head:
            print(f"head-moved: expected head {head}, GitHub reports {reported}; not retried.", file=sys.stderr)
            return 1
        if reported is not None and reread.in_merge_queue:
            print(f"already queued: PR #{number} at head {reported} is in the merge queue.")
            return 0
        state = "queue state unreadable" if reported is None else "not currently in the queue"
        print(f"admission-failed: PR #{number} at {head}; {state}: {error}", file=sys.stderr)
        return 2
    if outcome.skipped:
        print(f"maintainer mode: skipped {', '.join(outcome.skipped)}")
    position = entry.get("position")
    where = f" at position {position}" if position is not None else ""
    print(f"queued: PR #{number} at head {head} entered the merge queue{where}; queue admission is no merge yet.")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run(
        sys.argv[1:] if argv is None else argv,
        root=REPO_ROOT,
        github=GitHub(REPO_ROOT),
        tracker=tracker_statuses,
        script=Path(__file__).resolve(),
    )


if __name__ == "__main__":
    sys.exit(main())
