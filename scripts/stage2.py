#!/usr/bin/env python3
"""stage2.py - the one way this repository starts a foreign model.

**What this is.** Stage 2 lets a reviewer from another vendor read framework
content: the review loop (4b) runs on OpenCode Go through Pi at
`https://opencode.ai/zen/go/v1/chat/completions` until a round is clean - a
discovered free-model swarm first, the declared Flash swarm next, then one
declared paid model per round (ADR 0021); Codex drafts the spec, the design
and the plan (2, 2b and 3; GLM 5.3 after two failed Codex attempts) and
reviews the change (6); Opus 5.5 reviews the spec (2a); GLM 5.3 Flash
explores (phase 1) and implements (phase 4). A declaration in
`model-endpoints.yaml` stops nothing; this runner
stands between the rule and the call.

    python3 scripts/stage2.py explore      <change>   # GLM Flash, phase 1
    python3 scripts/stage2.py draft        <change>   # Codex, phases 2, 2b and 3; GLM 5.3 after two failed attempts
    python3 scripts/stage2.py spec-review  <change>   # Opus 5.5, phase 2a
    python3 scripts/stage2.py implement    <change>   # GLM Flash, phase 4
    python3 scripts/stage2.py repair       <change>   # Codex, the taken findings; Sonnet 5.5 after two failed checks
    python3 scripts/stage2.py prepare-loop <change>   # availability report before a fresh phase-4b run
    python3 scripts/stage2.py review-loop  <change>   # one round of phase 4b, until a round is clean
    python3 scripts/stage2.py release-loop <change>   # loop rows into findings.md
    python3 scripts/stage2.py release-loop <change> --restart --reason <text>   # maintainer only: a fresh run
    python3 scripts/stage2.py review       <change>   # Codex, phase 6; a re-check is a fresh read-only session
    python3 scripts/stage2.py probe        <change>   # one call per free and paid member, no record written
    python3 scripts/stage2.py session      <change>   # interactive Codex/Pi, a Terminal window

A fresh loop run and the probe check `tools/pi/pi --version` against `PI_VERSION` first;
any other answer refuses with exit 2 before the leak check and before any call.
A fresh loop run forces a live catalog refresh (`pi update --models`) before it
lists the models (`pi --list-models`) in the same fresh scratch directories; a
failed or timed-out refresh refuses instead of listing a stale cache.

`explore`, `implement` and `repair` accept `--stage2-off [REASON]`: the declared
Stage-1 route uses Haiku 5.5 or Sonnet 5.5. A leak refusal never falls back.
Implement lets the model edit but not run commands; before `make verify` the
runner applies ruff's safe fixes and its formatter to the changed Python files
under `scripts/` and `tests/`, then runs `make verify`, checks the time log and
makes the one checkpoint commit. A
failed attempt leaves its diagnostics and the files its model changed, quoted,
below its audit line in `findings.md`. `repair` takes every taken finding of
the loop record, the released blocks and the phase-6 tables to Codex in one
call (a fresh Codex attempt after a failed check, then Sonnet 5.5; a failed call
stops), proves each repair of code with a test that was red first, and marks the
rows `fixed` from the answer's fixed lines. Codex runs in its configured
`workspace-write` sandbox; the tests do not measure that confinement.

`session` starts one interactive Pi or Codex session in a new macOS
Terminal window, inside the change's dedicated worktree
(`<main checkout>/.claude/worktrees/<change>`, attached branch, that directory
as the working one). It takes `--model <id>` - exactly as
`model-endpoints.yaml` lists it: a plain id on `openai-codex` runs the
official Codex CLI, a full `opencode-go/<model>` id runs the pinned Pi (the
id names the endpoint, not the program) with a runner-supplied policy
extension when `opencode-go` lists the bare `<model>` - and `--handover <path>`
for a file inside the worktree (default: the change's `handover.md`); its full text is the first
prompt. The declaration and the leak check run as for every call, the second
time immediately before the window opens, and one audit line goes into
`findings.md` as `dispatch pending.`, replaced afterwards by `accepted` or
`failed`. **Accepted means Terminal took the command**, not that the CLI
started, signed in or the model answered: what follows shows in the window.
The leak check covered this launch only - later edits, later prompts and a
model switched in the UI are not scanned, and the terminal permissions
confine nothing at the operating-system level; another model starts again
through this runner. `--model` and `--handover` belong to the session verb
alone, and `--stage2-off` to explore, implement and repair.

**What every call carries** (before it starts, in this order):

1. the change named, and `plans/changes/<change>/` a directory; its phase
   artefact with a `bead` in its header;
2. an endpoint the declaration clears: present, the model listed, `framework`
   among what it may see, a residency other than `nicht-erklaert`;
3. the leak check (`scripts/leakcheck.py`), in this process, immediately before
   this call, over the change, the tree, the history and the call's own prompt;
4. one line in the phase's durable artefact naming the date, the verb, the
   endpoint, the model and the leak check's three numbers;
5. an empty standard input, and an environment the runner built from an
   allow-list - never the caller's.

**Reads: what each call can reach.** The Claude Code calls (explore, the
draft's GLM attempt, implement, spec-review and the Sonnet 5.5 fallback attempts) start in the worktree
with `--restricted` and no `--add-dir`; `claude --help` says `--restricted`
"confines the file tools to the working directories", so
`~/.config/cc-routing/secrets.env` is outside what those file tools reach.
That is the CLI's documented behaviour, not measured here. Codex's draft and
repair attempts have command tools in the configured `workspace-write`
sandbox; a repair may run tests and `make verify` but must not commit or run
git commands that change the repository. Codex's review, draft and repair
calls are not confined in their reads: only the prompt's request bounds them
to the worktree and the repository's git directory. **The paid review
loop's Pi calls are not among them, and they are not confined:** a round's
`read` reaches files outside the worktree (measured with Pi 1.1.0, research
§L), and the secrets file is among them; only the prompt's request bounds it -
to read nothing outside the worktree and the repository's git directory, a
request and not a lock. That
is the residual risk ADR 0007 accepted for its reviewers on 2026-09-30, which
ADR 0011 extends to the rungs. **The free swarm's calls are the exception:**
they get no tools at all (`--no-tools`, a scratch working directory) and their
prompt carries nothing but static instructions and bounded hunks of the
implementation diff (ADR 0021, decision 3). The loop's isolation flags (no
extensions, MCP
servers, skills, context files, prompt templates or themes; no approval; a
fresh agent directory and home per call) are configured on every call and
were measured once by hand on the pinned version; the suite starts no real
Pi, and the version pin (`require_pi`) is what ties the measurement to the
call. The Codex review calls run in the CLI's read-only sandbox; a draft's
Codex call runs in `workspace-write`, and the runner puts back what lands
outside the change folder.

**The loop record** lives outside the worktree
(`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md`):
the rounds' rows, the run's stage snapshot (`Loop state:`, the runner's own
line), and the orchestrator's decision on each row, until the phase-6
verdict is written and `release-loop` carries them into `findings.md`. The
release is the only thing that deletes the record, and it deletes nothing that
has not arrived: every loop row, and every other line of the record as it
stands, is in `findings.md` first. Not carried are only the record's own
furniture: its heading, its intro, the round headings, the tables' header and
separator, and the blank lines outside the reviewer's words. The reviewer's
words are carried exactly as they came - a heading, a code comment or a table
line with a loop id included; only a line of the round tables the runner wrote
that carries a loop id and cannot be read as a row refuses the release,
because the orchestrator has to decide that row. A round counts as completed
when at least one of its members succeeded and answered - with rows or with
"no finding"; an attempt in which every member failed is no round, consumes no
stage and is refused as a failed call.

Exit: 0 done, 1 a call or implementation post-check failed, 2 refused.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import functools
import hashlib
import io
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_adr_answers  # noqa: E402
import check_criterion_ledger  # noqa: E402
import check_frontmatter_current  # noqa: E402
import leakcheck  # noqa: E402
import merge_guard  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

# (endpoint, model, effort) - what the declaration must clear and the call pins.
# The reviews have no fixed tuple: their model is the round's rung of the
# `opencode-go` entry's ordered `modelle` list (the ladder, see `ladder`).
GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")
# GLM 5.3, not Flash: the draft's fallback routes here (the repair did until ADR 0017), shared with stage2_runs.py.
GLM = ("glm-coding-plan", "glm-5.3", "max")
HAIKU = ("claude-code-plan", "claude-haiku-5-5", None)
SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")
# Sol's reasoning effort, one entry per runner verb (bead coding-harness-yzk): the draft and the
# review start at `high`, the repair at `medium`. This mapping is the one place a later adjustment
# edits - the instructions link its entries and the tests read them. A call's verb selects the
# entry, retries included: the `codex-repair` route label names a retry of draft and repair and
# picks no policy of its own. `CODEX` keeps its endpoint identity with an empty effort slot;
# `run_codex` takes the effort from the caller's verb instead.
CODEX_EFFORTS = {"draft": "high", "repair": "medium", "review": "high"}
CODEX = ("openai-codex", "gpt-6.1-sol", None)
# Opus 5.5, the spec review (2a) since ADR 0016: the strongest review on the repository's highest-demand effort.
OPUS = ("claude-code-plan", "claude-opus-5-5", "xhigh")
# A new ADR file of a draft: four digits, a slug of lowercase letters, digits and hyphens. Counted against the
# merge base of the baseline and origin/main, so a second draft may edit the ADR the first one committed.
NEW_ADR = re.compile(r"docs/adr/\d{4}-[a-z0-9][a-z0-9-]*\.md")
# The plan card's lines, in the order the drafted plan.md must open with (spec, criterion 15).
CARD_LABELS = ("For you:", "Done when:", "Appetite:", "Not now:", "Pre-mortem:")
# The phase prompts a draft carries in full, in drafting order (spec, criterion 3).
DRAFT_PROMPTS = ("02-spec.md", "02b-design.md", "03-plan.md")
GLM_BASE_URL = "https://api.z.ai/api/anthropic"
OPENCODE = "opencode-go"
# The runner's own Pi (bead coding-harness-agx, ADR 0019): one repository-local
# install under `tools/pi/`, started only through its wrapper. The pin has one
# source - the manifest the wrapper enforces - and is read from it, so a moved
# pin cannot leave the runner checking a version it no longer ships. A missing
# or floating pin stops the import: without it the runner has no pin to check.
# The loop's isolation was first measured by hand on Pi 1.1.0 (research §L);
# the offline contract suite now measures the pinned install itself.
PI_TOOLS_DIR = REPO_ROOT / "tools" / "pi"
PI_WRAPPER = PI_TOOLS_DIR / "pi"
PI_MANIFEST = PI_TOOLS_DIR / "package.json"
PI_PACKAGE = "@earendil-works/pi-coding-agent"


def _pi_pin() -> str:
    """The exact Pi version `tools/pi/package.json` pins - anything else stops the runner."""
    try:
        manifest = json.loads(PI_MANIFEST.read_text(encoding="utf-8"))
        pin = manifest["dependencies"][PI_PACKAGE]
        exact = isinstance(pin, str) and re.fullmatch(r"\d+\.\d+\.\d+", pin) is not None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError):
        exact = False
    if not exact:
        raise SystemExit(
            f"stage2: {PI_MANIFEST} does not pin an exact {PI_PACKAGE} version; "
            "the runner has no pin to check (see tools/pi/README.md)."
        )
    return pin


PI_VERSION = _pi_pin()
PI_TOOLS = "read,grep,find,ls"
# A reviewer call that has not ended after this many minutes is stopped (spec, criterion 15);
# raised from 30 by the maintainer on 2026-10-24.
REVIEWER_MINUTES = 45
# The exit code of a loop that finished, told apart from the refusal's 2 (R-11 of the review-swarm review).
CLEAN_CODE = 3
# `pi --version` that has not ended after this many seconds is a Pi off the pin (spec, criterion 27).
PI_VERSION_SECONDS = 30

CODEX_ASK_RULE = (
    "Bash(codex *)",
    "codex typed directly skips the leak check and the declaration; the runner is the way in",
)

READ_REQUEST = "Read nothing outside this worktree and the repository's git directory."
ANSWER_FORMAT = (
    "Answer with table rows only: one row per finding, exactly six cells, no header and no other text -\n"
    "`| ID | Severity | Dimension | Origin | Where | Finding |`. Write a `|` inside a cell as `\\|`.\n"
    "The severity cell is free text (BLOCKER, MAJOR or MINOR is the convention); the orchestrator\n"
    "decides what is taken, so a word of your own is not a fault.\n"
    "The runner adds the reviewer, the status and the test mark. When there is no finding, answer exactly: No finding."
)
MARK_FORMAT = "For each loop row answer one line and nothing else: `<ID>: agree` or `<ID>: disagree — <reason>`."
REPAIR_ANSWER = (
    "Answer with one fixed line per taken row: `<ID>: fixed — tests/<path>::<function>` or\n"
    "`<ID>: fixed — not a test — <reason>`. Headings, fences and report prose around the fixed lines are\n"
    "ignored, but a colon line whose id looks like a finding id (`L1-2`, `F-12`) and names no taken row\n"
    "still fails. Letters-hyphen-digits ids count only for prefixes used by this change's row ids;\n"
    "`L<digits>-<digits>` always counts; the prefix `L` counts only when the change has a loop row.\n"
    "A colon line whose right side is a fixed status (`fixed — …`) also fails when its id names no\n"
    "taken row, whatever the id's shape. Write a `|` inside a reason as `\\|`. A code row needs a test that fails on the\n"
    "baseline's code, which the runner runs; only a row taken as `taken — not a test — <reason>` may be\n"
    "answered `not a test`. Do not edit `findings.md`. A hand repair is booked in the row's own Status as\n"
    "one of the two fixed statuses above; a Status that still begins `taken` while naming a fix\n"
    "(`; fixed by …`, `; fixed: …`, `; repaired by …`) refuses the repair before any call.\n"
    "Backtick-quoted markers do not count; an unquoted marker beside a backtick span still refuses the repair."
)
# The Codex attempts (ADR 0017): Codex has command tools in its configured sandbox, so it is told what it may run.
REPAIR_FORMAT = (
    "Repair only the taken rows below. You may run tests and `make verify`; write no entry under\n"
    "`## Time used` in `plan.md`, the runner measures the attempt and writes it. Do not commit and run no\n"
    "git command that changes the repository: the runner runs `make verify` and makes the one commit. " + REPAIR_ANSWER
)
# The Sonnet attempt keeps the file-tools sentence it always had.
REPAIR_FORMAT_FILE_TOOLS = (
    "Repair only the taken rows below, with the available file tools; you cannot run commands. Write no\n"
    "entry under `## Time used` in `plan.md`, the runner measures the attempt and writes it. " + REPAIR_ANSWER
)
# What a draft may write and what the runner takes back; `<change>` is filled in (spec, criterion 3).
DRAFT_RULES = (
    "Write, in `plans/changes/<change>/`, `spec.md`, `design.md` when `prompts/02b-design.md` asks for one,\n"
    "and `plan.md`, as the three prompts above say and in the form of the files under `templates/`. An ADR\n"
    "draft, when one is due, is exactly one new file `docs/adr/<NNNN>-<slug>.md`, numbered after the highest\n"
    "file there. Change nothing else: the runner puts back every changed path outside the change folder\n"
    "except the one new ADR draft, and the change's `decisions.md`. If `findings.md` holds phase-2a\n"
    "rows whose Status is `open`, work each into\n"
    '`spec.md` as `prompts/02-spec.md`, "After the spec review", says, write its Status in `findings.md`,\n'
    'and bring `design.md` and `plan.md` into line. A `[DECISION]` goes into the spec\'s "Open decisions"\n'
    "in the form `prompts/02-spec.md` gives. Never write an answer for the maintainer, never record an ADR\n"
    "answer, and never change a class, a criterion or a decision to make a gate green. `plan.md` opens with\n"
    "the card and holds a `## Time used` section, empty until phase 4. Do not commit and run no git command\n"
    "that changes the repository: the runner runs `make verify` and makes the one commit."
)

# The environment a foreign program gets: these, when set, then the call's own.
ENV_ALLOW = (
    "PATH",
    "HOME",
    "USER",
    "LOGNAME",
    "SHELL",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "TZ",
    "CODEX_HOME",
)
GLM_MODEL_VARIABLES = (
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_SMALL_FAST_MODEL",
    "CLAUDE_CODE_SUBAGENT_MODEL",
)
# Claude Code knows no GLM id, so it warns at every start and assumes a 200k context window
# (bead coding-harness-6th). Per the Claude Code docs, naming the window ends the warning (not yet
# seen in a live start); it stays at the assumed 200k,
# because no Z.ai source read on 2026-10-16 states the Coding Plan's window, and a window set
# above the real one would overflow instead of compacting.
GLM_CONTEXT_TOKENS = "200000"

ROW_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Reviewer", "Status", "Broke a test"]
RELEASED_COLUMNS = [*ROW_COLUMNS, "Phase 6"]

# The loop ends on a clean round, on the repair brake or on spent stages - never
# on a round count (ADR 0021). The run's stage snapshot travels as the record's
# own `Loop state:` line and, after a release, as the released block's own line;
# it is never read from the reviewers' words.
STATE_KEY = "Loop state: "
STATE_LINE = re.compile(r"^Loop state: (\{.*\})[ \t]*$", re.M)
# The maintainer's restart of a completed loop (ADR 0021, restart amendment): the runner's own line in
# findings.md, at a line start - a quoted copy is a reviewer's or an attempt's words, not a restart.
RESTART_LINE = re.compile(r"^Loop restarted: (\d{4}-\d{2}-\d{2}) after round (\d+) — (.+)$", re.M)
# The Zen provider, which the free rule may never select.
ZEN = "opencode"
# `pi update --models` and `--list-models` share one fresh scratch directory and
# this timeout; a refresh that has not ended inside it refuses the run (criterion 5).
PI_DISCOVERY_SECONDS = 120
# Bounds of the implementation diff a free call may see: per file and in total,
# so no whole source file travels (criterion 3).
FREE_DIFF_MAX_LINES = 400
FREE_DIFF_MAX_TOTAL = 2000
# A paid member reads the whole change, but not without end: over this bound the prompt carries a cut
# marker and the round says so. Pi 1.2.0 compacts an oversized context instead of failing (read in the
# pinned install: `docs/compaction.md`, "Auto-compaction triggers when contextTokens > contextWindow -
# reserveTokens"; `dist/core/agent-session.js:418`), so a `No finding.` could rest on a summary the
# member never saw in full (R-15 of the review-swarm review).
REVIEW_DIFF_MAX_LINES = 2000

SEVERITIES = {"BLOCKER", "MAJOR", "MINOR"}

# `Phase 6 verdict: <reviewer> <session>, <date>` - the reviewer may be several words, the session may be
# missing, and a space or a full stop after the date does not matter (repair round 1, F-4). `pending` names
# nobody who reviewed, so a line that starts with it is no verdict (repair round 2).
VERDICT_LINE = re.compile(
    r"^Phase 6 verdict:[ \t]+(?!(?i:pending)\b)\S[^\n]*?,[ \t]*\d{4}-\d{2}-\d{2}[ \t]*\.?[ \t]*$", re.M
)
VERDICT_START = re.compile(r"^phase 6 verdict\b[^\n]*$", re.M | re.I)
SESSION_LINE = re.compile(r"^Reviewer session: codex (\S+)", re.M)
ROUNDS_LINE = re.compile(r"^Rounds run: (\d+)\s*$", re.M)
CUT_ROUNDS_LINE = re.compile(r"^Cut rounds: (\d+(?:, \d+)*)\s*$", re.M)
ROUND_HEADING = re.compile(r"^## Round \d+ — \S+,", re.M)
RELEASE_HEADING = "## Phase 4b — loop rows, released"
# The runner's own sentence, matched as a whole line: a reviewer's table cell may quote it, and a
# substring search cut the block there and left the loop unreadable (R-3 of the review-swarm review).
KEPT_FROM = re.compile(r"^Kept from the loop record:[ \t]*$", re.M)
NO_LOOP_LINE = "Loop rows: none — the loop did not run for this change."
# Readers of findings.md match these at the start of a line only: a failed attempt's block quotes its
# lines with `>`, so quoted gate output can hold them without being taken for the runner's own (criterion 11).
RELEASE_LINE = re.compile("^" + re.escape(RELEASE_HEADING), re.M)
NO_LOOP = re.compile("^" + re.escape(NO_LOOP_LINE) + r"[ \t]*$", re.M)
# Bounds of a failed attempt's block: a gate line and a file entry keep their first characters…
QUOTE_LINE_CHARS = 500
# …and the file list keeps its first entries (spec, criteria 13 and 14).
ATTEMPT_FILES = 40
LOOP_ID = re.compile(r"L\d+-\d+")
# Non-loop finding shapes count only for prefixes already used by the change's rows.
# Loop identifiers always count; an unrelated colon label remains report prose.
FINDING_ID = re.compile(r"([A-Za-z]+)-[0-9]+")
NOT_ROWS_NOTE = "The answer was not only six-cell rows; what is not one is kept below as it came."
# A fixed line's test, in the form of ADR 0013's criterion ledger: a file `tests/…/test_*.py`, a function
# `test_…`. A `.` or `..` path segment would climb out of `tests/`; `fixed_status` refuses it as the
# ledger's gate does (`check_criterion_ledger.py`).
FIXED_TEST = re.compile(r"^tests/(?P<file>[^|\s]+\.py)::(?P<function>test_\w+)$")
# A red-first pytest run that has not ended after this many minutes is stopped (spec, criterion 18).
RED_FIRST_MINUTES = 10
# The runner-owned probe of a red-first run: written into the temporary checkout as a file and
# loaded with `-p`, never installed and never part of the attempted tests. It records what pytest
# actually did, so an exit code alone can no longer read a missing dependency's fixture error as a
# test failure (bead coding-harness-omp).
RED_PROBE_NAME = "stage2_red_probe"
RED_PROBE_SOURCE = '''"""The red-first outcome probe of scripts/stage2.py: it records what pytest actually did.

Loaded with `-p`, it writes one JSON record the runner reads back. The environment names the private
report path, the fresh invocation token and the requested selector. The record holds the selected
node ids, one entry per setup, call and teardown phase - the final outcome after pytest's own
wrappers, the expected-result markers and whether a failing call raised an AssertionError -, the
collection failures and the session's completion and exit status.
"""

import json
import os

import pytest

_REPORT = os.environ.get("STAGE2_RED_REPORT", "")
_TOKEN = os.environ.get("STAGE2_RED_TOKEN", "")
_SELECTOR = os.environ.get("STAGE2_RED_SELECTOR", "")
_RECORD = {
    "schema": 1,
    "token": _TOKEN,
    "selector": _SELECTOR,
    "collection_errors": [],
    "selected": [],
    "phases": [],
    "session": None,
}


def _write() -> None:
    """The record so far, rewritten in place; a killed run leaves the phases it reached."""
    if not _REPORT:
        return
    try:
        with open(_REPORT, "w", encoding="utf-8") as handle:
            json.dump(_RECORD, handle)
    except OSError:
        pass


def pytest_collectreport(report):
    if report.failed:
        _RECORD["collection_errors"].append(report.nodeid)


def pytest_collection_finish(session):
    _RECORD["selected"] = [item.nodeid for item in session.items]
    _write()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """One phase outcome, read after pytest's own wrappers so the xfail conversion is visible."""
    outcome = yield
    report = outcome.get_result()
    raised = getattr(call.excinfo, "value", None)
    _RECORD["phases"].append(
        {
            "nodeid": item.nodeid,
            "phase": report.when,
            "outcome": report.outcome,
            "assertion": bool(report.failed and isinstance(raised, AssertionError)),
            "exception": type(raised).__name__ if raised is not None else None,
            "expected": bool(item.get_closest_marker("xfail"))
            or bool(getattr(report, "wasxfail", False))
            or bool(getattr(report, "skipped_by_mark", False)),
        }
    )
    _write()


def pytest_sessionfinish(session, exitstatus):
    _RECORD["session"] = {"finished": True, "exitstatus": int(exitstatus)}
    _write()
'''

RECORD_HEADING = "# Loop record — "
RECORD_INTRO = (
    "Write `Status` (`taken — <test or criterion>`, `taken — not a test — <reason>` or "
    "`rejected — <reason>`) for every row below.\n"
    "For a taken row also write `Broke a test` (`yes` or `no`) — before the next round or the release; "
    "a row the repair marked `fixed` needs the mark too."
)

_PIPE = re.compile(r"(?<!\\)\|")


class CleanStop(Exception):
    """The loop has finished: the last round was clean. Not a refusal, and told apart by its exit code.

    Automation that reads only the exit status could not tell a finished loop from a refused one while
    both were 2 (R-11 of the review-swarm review). `main` returns `CLEAN_CODE` for this.
    """


class Refused(Exception):
    """The runner refuses before any call: exit 2."""


class CallFailed(Exception):
    """A call ended without a usable answer: exit 1."""


class StepTimedOut(CallFailed):
    """A started program ran into its time limit and its whole process group was killed (R-20)."""


def today() -> str:
    return dt.date.today().isoformat()


# ---------------------------------------------------------------------------
# Secrets, environment, the foreign call
# ---------------------------------------------------------------------------


def secrets_path() -> Path:
    """The secrets file. Read at call time, never at import."""
    named = os.environ.get("CC_SECRETS")
    return Path(named) if named else Path.home() / ".config" / "cc-routing" / "secrets.env"


def read_secret(name: str) -> str | None:
    """`KEY=value` or `export KEY=value`, quotes stripped, nothing evaluated."""
    try:
        text = secrets_path().read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        key, sep, value = line.partition("=")
        if sep and key.strip() == name:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            return value or None
    return None


FRAGMENT = 8


@functools.lru_cache(maxsize=8)
def _fragment_pattern(secret: str, binary: bool) -> re.Pattern:
    """Every window of FRAGMENT characters of the secret (the whole secret if it is shorter), as one regex.

    The windows sit in a lookahead so that overlapping hits are all reported; the scanner then
    merges them, which expands a match to the whole run of the secret that the text carries.
    """
    windows = {secret[i : i + FRAGMENT] for i in range(max(len(secret) - FRAGMENT, 0) + 1)}
    alternatives = "|".join(re.escape(w) for w in sorted(windows, key=len, reverse=True))
    return re.compile((b"(?=(%b))" % alternatives.encode()) if binary else f"(?=({alternatives}))")


def credential_spans(data: str | bytes, secret: str) -> list[tuple[int, int]]:
    """The merged (start, end) runs of `data` that are the secret or any 8-character fragment of it."""
    pattern = _fragment_pattern(secret, isinstance(data, bytes))
    spans: list[tuple[int, int]] = []
    for match in pattern.finditer(data):
        start, end = match.start(1), match.end(1)
        if spans and start <= spans[-1][1]:
            spans[-1] = (spans[-1][0], max(end, spans[-1][1]))
        else:
            spans.append((start, end))
    return spans


def replace_credential(data: str | bytes, secret: str) -> str | bytes:
    """`data` with every run of the secret or of an 8-character fragment of it replaced by [credential]."""
    mark: str | bytes = b"[credential]" if isinstance(data, bytes) else "[credential]"
    out, last = [], 0
    for start, end in credential_spans(data, secret):
        out += [data[last:start], mark]
        last = end
    out.append(data[last:])
    return (b"" if isinstance(data, bytes) else "").join(out)


def scrub(text: str, secret: str | None) -> str:
    """Replace the credential, whole or in any fragment of 8 or more characters, in everything printed or written."""
    return replace_credential(text, secret) if secret else text


def protect_diagnostics(text: str, key: str | None = None) -> str:
    """`text` as failed-check diagnostics may be published: secret-rule matches redacted, the key scrubbed.

    Every secret rule of the active denylist is read now, on every route - a keyless Codex or Stage-1 route
    included. A match is replaced in place by `[<rule name>]` (the name already starts `secret:`); the spans
    are found in the original text, overlapping ones merge with credential spans into one marker run, and the
    replacement keeps the line breaks it covered, so a traceback keeps its shape. Known credentials are
    protected with their credential marker. Every rule reads the original text, before any replacement,
    in full and line by line to preserve multiline and anchored matches; a match wholly inside the known
    credential is left to the credential marker. Non-secret rules refuse first
    - redaction must not hide a blocking rule - and so does a denylist that cannot be read, or
    text that still matches a secret rule after the replacement. A refusal names a rule or a reason and a
    line, never a value.
    """
    return _protect_diagnostics(text, key)[0]


def _rule_spans(
    pattern: re.Pattern, text: str, credentials: list[tuple[int, int]], *, include_empty: bool = False
) -> list[tuple[int, int]]:
    """Matches of `pattern` as offsets of `text`, except those wholly inside a credential.

    Whole-text matches retain multiline rules; per-line matches mirror the leak check, including ^ and $
    without an inline multiline flag. Advancing from each match's start retains overlapping alternatives.
    Empty matches are retained for blocking checks only; they have no secret text to replace.
    """
    segments = [(0, text)]
    offset = 0
    for line in text.split("\n"):
        segments.append((offset, line))
        offset += len(line) + 1
    found: list[tuple[int, int]] = []
    for offset, segment in segments:
        position = 0
        while position <= len(segment):
            match = pattern.search(segment, position)
            if match is None:
                break
            if include_empty or match.end() > match.start():
                start, end = offset + match.start(), offset + match.end()
                # Credential spans are half-open: an empty match at the end belongs to
                # the following text, so it must still trigger a blocking rule.
                if not any(left <= start < right and end <= right for left, right in credentials):
                    found.append((start, end))
            position = match.start() + 1
    return found


def _protect_diagnostics(text: str, key: str | None, split_at: int | None = None) -> tuple[str, int | None]:
    """Protect a complete diagnostic while mapping an optional stream boundary."""
    if not text:
        return text, split_at
    credentials = credential_spans(text, key) if key else []
    rules, problem = leakcheck.read_denylist(leakcheck.default_denylist())
    if problem:
        raise Refused(f"the failed-check diagnostics cannot be checked: {problem}")
    # Every rule reads the original text, before any replacement: a credential replaced first would cut a
    # match that reaches past it (F-4 and F-5 of #215). A match wholly inside a known credential is the
    # credential's, and keeps its marker; every other non-secret match refuses before anything is replaced.
    for rule in rules:
        if rule.secret:
            continue
        for start, _end in _rule_spans(rule.pattern, text, credentials, include_empty=True):
            number = text.count("\n", 0, start) + 1
            raise Refused(
                f"the failed-check diagnostics match rule '{rule.name}' at line {number}; the call does not start."
            )
    spans: list[list] = [[start, end, ["credential"]] for start, end in credentials]
    for rule in rules:
        if rule.secret:
            spans += [[start, end, [rule.name]] for start, end in _rule_spans(rule.pattern, text, credentials)]
    spans.sort(key=lambda span: (span[0], span[1]))
    merged: list[list] = []
    for start, end, names in spans:
        if merged and start < merged[-1][1]:
            merged[-1][1] = max(end, merged[-1][1])
            merged[-1][2] += [name for name in names if name not in merged[-1][2]]
        else:
            merged.append([start, end, list(names)])
    order = {rule.name: index for index, rule in enumerate(rules)}
    order["credential"] = -1
    out, last = [], 0
    safe_boundary = None
    for start, end, names in merged:
        marks = "".join(f"[{name}]" for name in sorted(names, key=order.__getitem__))
        if split_at is not None and safe_boundary is None and split_at < end:
            prefix_length = sum(map(len, out))
            if split_at <= start:
                safe_boundary = prefix_length + split_at - last
            else:
                safe_boundary = prefix_length + start - last + len(marks) + text.count("\n", start, split_at)
        out += [text[last:start], marks, "\n" * text.count("\n", start, end)]
        last = end
    if split_at is not None and safe_boundary is None:
        safe_boundary = sum(map(len, out)) + split_at - last
    out.append(text[last:])
    safe = scrub("".join(out), key)
    for rule in rules:
        if rule.secret and (rule.pattern.search(safe) or any(rule.pattern.search(line) for line in safe.split("\n"))):
            raise Refused(f"the failed-check diagnostics still match rule '{rule.name}' after redaction.")
    return safe, safe_boundary


def protect_files(files: list[str] | str, key: str | None = None) -> list[str] | str:
    """The entries of `attempt_files`, or the reason it could not measure, through `protect_diagnostics`."""
    if isinstance(files, str):
        return protect_diagnostics(files, key)
    return [protect_diagnostics(entry, key) for entry in files]


def foreign_env(own: dict[str, str]) -> dict[str, str]:
    """The allow-list from the caller's environment, then the call's own variables."""
    env = {name: os.environ[name] for name in ENV_ALLOW if name in os.environ}
    env.update(own)
    return env


def glm_env(key: str, config_dir: Path, model: str) -> dict[str, str]:
    own = {
        "ANTHROPIC_BASE_URL": GLM_BASE_URL,
        "ANTHROPIC_AUTH_TOKEN": key,
        "ANTHROPIC_API_KEY": key,
        "CLAUDE_CONFIG_DIR": str(config_dir),
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
        "CLAUDE_CODE_MAX_CONTEXT_TOKENS": GLM_CONTEXT_TOKENS,
    }
    own.update({name: model for name in GLM_MODEL_VARIABLES})
    return foreign_env(own)


def launch(
    command: list[str],
    root: Path,
    env: dict[str, str],
    secret: str | None = None,
    timeout: float | None = None,
    limit: str | None = None,
) -> subprocess.CompletedProcess:
    """Start a foreign program: empty standard input, the worktree as its directory.

    With a `timeout` the program leads a process group of its own, and a timeout kills the whole
    group: a hung `make verify` leaves no shell, pytest or worker behind to write into the worktree
    after the run stopped (O188-4 of the #188 review).
    """
    try:
        if timeout is None:
            return subprocess.run(
                command,
                cwd=root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                errors="replace",
                check=False,
            )
        with subprocess.Popen(
            command,
            cwd=root,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            start_new_session=True,
        ) as process:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                with contextlib.suppress(OSError):
                    os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
                raise
            return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired as error:
        what = limit or f"the reviewer time limit after {REVIEWER_MINUTES:g} minutes"
        raise StepTimedOut(f"{command[0]} was stopped by {what}") from error
    except OSError as error:
        raise CallFailed(f"{command[0]} could not be started: {scrub(str(error), secret)}") from error


def last_error_line(done: subprocess.CompletedProcess, secret: str | None = None) -> str:
    """The last non-empty line of the program's standard error, scrubbed and bounded; empty when there is none."""
    lines = [line.strip() for line in (done.stderr or "").splitlines() if line.strip()]
    if not lines:
        return ""
    return scrub(lines[-1], secret)[:200]


def fail(
    program: str,
    done: subprocess.CompletedProcess,
    reason: str,
    secret: str | None = None,
    label: str | None = None,
) -> CallFailed:
    """Print the last lines of the program's standard error, scrubbed; return the exception to raise.

    The reason names the last line of the standard error beside the exit
    ("Model is unavailable"), so a failed swarm member says why in the loop
    record. A `label` (a swarm member's model id) prefixes every printed line,
    because the members' tails interleave on one stream (Q-13).
    """
    tail = "\n".join((done.stderr or "").splitlines()[-40:])
    if tail:
        printed = scrub(tail, secret)
        if label:
            printed = "\n".join(f"{label}: {line}" for line in printed.splitlines())
        print(printed, file=sys.stderr)
    last = last_error_line(done, secret)
    detail = f" ({last})" if last else ""
    return CallFailed(f"{program} call failed: {reason}{detail}")


# ---------------------------------------------------------------------------
# Tables and findings.md
# ---------------------------------------------------------------------------


def split_row(line: str) -> list[str] | None:
    """The cells of a table line, or None when the line is not one."""
    stripped = line.strip()
    if len(stripped) < 2 or not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.strip() for cell in _PIPE.split(stripped[1:-1])]


def _furniture(cells: list[str]) -> bool:
    """The header or the separator of a table."""
    return cells[0].lower() == "id" or all(re.fullmatch(r":?-+:?", cell) for cell in cells)


def parse_rows(answer: str, *, notes: list[str] | None = None) -> tuple[list[list[str]], str]:
    """The six-cell rows of an answer and the text that is not a row.

    Six cells are known. A line of more cells that starts like a row (its second cell is a severity) holds a
    `|` inside its last cell - a shell pipe, a regular expression - and that cell takes the rest, each
    pipe escaped; when a caller passes `notes`, that widening is named once per row, because an unescaped
    `|` before the finding moves the columns instead (R-25 of the review-swarm review). A decorative line of
    empty cells is no row and no text: it is dropped. Anything else that is a table line but no row stays
    in the text, as it came.
    """
    rows: list[list[str]] = []
    rest: list[str] = []
    for line in answer.splitlines():
        cells = split_row(line)
        if cells is None:
            if line.strip():
                rest.append(line)
        elif _furniture(cells) or not any(cell.strip() for cell in cells):
            continue
        elif len(cells) == 6:
            rows.append(cells)
        elif len(cells) > 6 and cells[1].upper() in SEVERITIES:
            rows.append([*cells[:5], " \\| ".join(cells[5:])])
            if notes is not None:
                notes.append(cells[0])
        else:
            rest.append(line)
    return rows, "\n".join(rest)


def render_table(columns: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


def append(path: Path, text: str) -> None:
    """Add a block at the end, separated by one blank line."""
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    joined = f"{existing}\n{text.rstrip()}\n" if existing else f"{text.rstrip()}\n"
    path.write_text(joined, encoding="utf-8")
    stamp_updated(path)


def stamp_updated(path: Path) -> None:
    """A file with a header is one the runner has just changed: its `updated:` says today (gate `frontmatter-current`).

    The stamp edits that one line. A file without a header, like the loop record, is left as it is.
    """
    check_frontmatter_current.stamp(path, dt.date.today())


def answer_parts(rows: list[list[str]], answer: str, reviewer: str, table: str) -> list[str]:
    """What follows a heading: the table, or a true statement about why there is none, then what is not a row.

    "No finding" is said only of an answer that has no table line at all. A table the parser cannot read as
    six-cell rows is a finding somebody has to read, so it is passed through and said to be one.
    """
    rest = parse_rows(answer)[1]
    if rows:
        parts = [table]
    elif any(split_row(line) is not None for line in rest.splitlines()):
        parts = [f"{reviewer} answered in table lines that are not six-cell rows; they are kept as they came."]
    else:
        parts = [f"{reviewer} reported no finding."]
    kept = rest if rows else answer
    if kept.strip():
        parts.append(f"{NOT_ROWS_NOTE}\n\n{kept.strip()}")
    return parts


def answer_block(rows: list[list[str]], answer: str, reviewer: str) -> str:
    """The block of a reviewer's answer: its rows with the reviewer, `open` and no test mark."""
    table = render_table(ROW_COLUMNS, [[*row, reviewer, "open", "—"] for row in rows])
    return "\n\n".join(answer_parts(rows, answer, reviewer, table))


# ---------------------------------------------------------------------------
# Preconditions every call meets
# ---------------------------------------------------------------------------


@dataclass
class Context:
    root: Path
    change: str
    folder: Path
    bead: str
    models_store: dict | None = None

    @property
    def findings(self) -> Path:
        return self.folder / "findings.md"

    @property
    def research(self) -> Path:
        return self.folder / "research.md"

    @property
    def plan(self) -> Path:
        return self.folder / "plan.md"


def entry_problem(root: Path, endpoint: str) -> str | None:
    """Why the declaration does not clear this endpoint for any model, or None.

    The entry-level half of `declaration_problem`, checked before the free
    discovery starts: a broken declaration starts no foreign program, the
    catalog calls included.
    """
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    found = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == endpoint), None)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    if not isinstance(found.get("modelle"), list) or not found["modelle"]:
        return f"the endpoint {endpoint} lists no model"
    allowed = found.get("darf_sehen")
    if not isinstance(allowed, list) or "framework" not in allowed:
        return f"the endpoint {endpoint} may not see framework content"
    residency = found.get("residenz")
    if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
        return f"the endpoint {endpoint} states no data residency"
    return None


def excluded_problem(root: Path, model: str) -> str | None:
    """Why `ausgeschlossen` in `model-endpoints.yaml` denies this model, or None (R-4 of the review-swarm review).

    The list was prose the runner never read: a denied provider's new free id would have reviewed diffs
    without a decision. An entry binds by naming the ids or id prefixes it excludes in `modelle`; an
    entry without that field documents a decision but names nothing the code can match. One predicate,
    read by the free class and by the paid declaration, so both paths answer the same way.
    """
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    if not isinstance(data, dict):
        return "model-endpoints.yaml has malformed exclusions: the declaration must be a mapping"
    entries = data.get("ausgeschlossen", [])
    if not isinstance(entries, list):
        return "model-endpoints.yaml has malformed exclusions: ausgeschlossen must be a list"
    full = model.lower()
    names = model.rsplit("/", 1)[-1].lower()
    for number, entry in enumerate(entries, 1):
        malformed = f"model-endpoints.yaml has a malformed exclusion at entry {number}"
        if not isinstance(entry, dict):
            return malformed + ": a mapping is required"
        data_class = entry.get("klasse", "framework")
        if not isinstance(data_class, str) or not data_class.strip():
            return malformed + ": klasse must name a data class"
        if data_class != "framework":
            continue
        if "modelle" not in entry:
            continue  # A legacy prose-only decision has no machine-readable model ids.
        listed = entry.get("modelle")
        if not isinstance(listed, list) or any(not isinstance(item, str) or not item.strip() for item in listed):
            return malformed + ": modelle must be a list of nonempty model ids or prefixes"
        for item in listed:
            prefix = item.strip().lower()
            if prefix and any(value == prefix or value.startswith(prefix) for value in (full, names)):
                reason = str(entry.get("was") or "excluded by the maintainer").strip()
                return f"the model {model} is excluded by model-endpoints.yaml: {reason}"
    return None


def declaration_problem(root: Path, endpoint: str, model: str) -> str | None:
    """Why the declaration does not clear this endpoint and model for framework content, or None.

    For the `opencode-go` endpoint a model is also refused while its data terms
    are unread or its declaration records a dated skip (ADR 0021, decision 5):
    no paid or interactive call runs on unread terms.
    """
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    found = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == endpoint), None)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    excluded = excluded_problem(root, model)
    if excluded:
        return excluded
    if model not in (found.get("modelle") or []):
        return f"the endpoint {endpoint} does not list the model {model}"
    if endpoint == OPENCODE:
        problem = terms_problem(found, model)
        if problem:
            return problem
    allowed = found.get("darf_sehen")
    # A list, not a string: `"framework" in "not-framework"` would be true (phase 6 of stage2-session, F-4).
    if not isinstance(allowed, list) or "framework" not in allowed:
        return f"the endpoint {endpoint} may not see framework content"
    residency = found.get("residenz")
    if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
        return f"the endpoint {endpoint} states no data residency"
    return None


def _artefact_bead(path: Path) -> str | None:
    """The `bead` of one change artefact's header."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        return None
    try:
        header = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    bead = header.get("bead") if isinstance(header, dict) else None
    return str(bead) if bead else None


def _spec_bead(spec: Path) -> str | None:
    """Compatibility name for the spec header reader used by older tests."""
    return _artefact_bead(spec)


def folder_of(root: Path, change: str) -> Path:
    if not change or "/" in change or change in {".", ".."}:
        raise Refused("Name the change: a single folder name under plans/changes/.")
    folder = root / "plans" / "changes" / change
    if not folder.is_dir():
        raise Refused(f"plans/changes/{change}/ does not exist.")
    return folder


def preflight(
    root: Path,
    change: str,
    endpoint: tuple[str, str, str | None],
    bead_file: str = "spec.md",
    required: tuple[str, ...] = (),
    admission_problem: Callable[[Path, str], str | None] | None = None,
) -> Context:
    """The refusals that precede everything else: change, artefacts and declaration.

    `admission_problem` replaces the individual declaration for the free class:
    it receives the root and the model id and returns a problem or None (ADR
    0021, decision 3). Every other call keeps the strict declaration.
    """
    folder = folder_of(root, change)
    bead = _artefact_bead(folder / bead_file)
    if bead is None:
        raise Refused(f"plans/changes/{change}/{bead_file} has no bead in its header; the runner cannot name the work.")
    for name in required:
        path = folder / name
        try:
            path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise Refused(f"plans/changes/{change}/{name} cannot be read.") from error
    problem = (
        admission_problem(root, endpoint[1])
        if admission_problem is not None
        else declaration_problem(root, endpoint[0], endpoint[1])
    )
    if problem:
        raise Refused(problem)
    return Context(root, change, folder, bead)


def findings_header(ctx: Context, producer: str) -> str:
    day = today()
    return (
        "---\n"
        f'title: "Findings — {ctx.change}"\n'
        "category: findings\n"
        "status: draft\n"
        "implementation_status: none\n"
        f"date: {day}\n"
        f"created: {day}\n"
        f"last_reviewed: {day}\n"
        f"updated: {day}\n"
        "supersedes: null\n"
        "superseded_by: null\n"
        f"bead: {ctx.bead}\n"
        "owner: Data Architect\n"
        "provenance: ai-drafted-reviewed\n"
        f'produced_by: {{kind: llm-session, name: {producer}, version: "{day}"}}\n'
        "review: {status: pending, approved_by: null, approved_at: null}\n"
        "tags: [findings, stage-2]\n"
        "---\n\n"
        f"# Findings — {ctx.change}\n"
    )


def producer_for(endpoint: tuple[str, str, str | None]) -> str:
    """The header's producer names the program: codex, claude-code, pi (spec, criterion 29).

    The GLM endpoints run as Claude Code against Z.ai, so their producer is `claude-code`
    too; `pi` stays the producer of an endpoint nothing here names.
    """
    producers = {"openai-codex": "codex", "claude-code-plan": "claude-code", "glm-coding-plan": "claude-code"}
    return producers.get(endpoint[0], "pi")


def checked_prompt(
    ctx: Context,
    endpoint: tuple[str, str, str | None],
    prompt: str,
    admission_problem: Callable[[Path, str], str | None] | None = None,
):
    """Check the admission and exact prompt immediately before one call.

    `admission_problem`, when given, replaces the individual declaration (the
    free class, ADR 0021 decision 3); the leak check is mandatory either way.
    """
    problem = (
        admission_problem(ctx.root, endpoint[1])
        if admission_problem is not None
        else declaration_problem(ctx.root, endpoint[0], endpoint[1])
    )
    if problem:
        raise Refused(problem)
    result = leakcheck.check(ctx.change, leakcheck.default_denylist(), ctx.root, [("prompt", prompt)])
    print(result.verdict.render())
    if result.verdict.exit_code() != 0:
        raise Refused("the leak check is not clean; the call does not start.")
    return result


def call_line(verb: str, endpoint: tuple[str, str, str | None], result) -> str:
    """The one audit line of one checked call."""
    return (
        f"Stage-2 call, {today()}: {verb} · endpoint {endpoint[0]} · model {endpoint[1]} · "
        f"leak check clean over {result.files} files, {result.commits} commits, {result.rules} rules."
    )


def begin_call(
    ctx: Context,
    verb: str,
    endpoint: tuple[str, str, str | None],
    prompt: str,
    admission_problem: Callable[[Path, str], str | None] | None = None,
) -> None:
    """The admission, the leak check and the call line - for this one call, immediately before it."""
    result = checked_prompt(ctx, endpoint, prompt, admission_problem)
    if not ctx.findings.exists():
        ctx.findings.write_text(findings_header(ctx, producer_for(endpoint)), encoding="utf-8")
    append(ctx.findings, call_line(verb, endpoint, result))


def begin_work_call(
    ctx: Context,
    verb: str,
    endpoint: tuple[str, str, str | None],
    prompt: str,
    attempt: int,
    route: str,
    destination: Path,
    reason: str | None = None,
) -> None:
    """Check and record one explore/implement attempt in its phase artefact."""
    result = checked_prompt(ctx, endpoint, prompt)
    if destination == ctx.findings and not destination.exists():
        destination.write_text(findings_header(ctx, producer_for(endpoint)), encoding="utf-8")
    why = f" · reason {reason}" if reason else ""
    append(
        destination,
        f"Stage-2 call, {today()}: {verb} · attempt {attempt} · route {route} · "
        f"endpoint {endpoint[0]} · model {endpoint[1]}{why} · leak check clean over "
        f"{result.files} files, {result.commits} commits, {result.rules} rules.",
    )


def phase_prompt(root: Path, prompt_file: str, change: str, extra: str = "") -> str:
    """The phase prompt in full, the change's name, the answer format, and the read request last."""
    body = (root / "prompts" / prompt_file).read_text(encoding="utf-8")
    parts = [body.rstrip(), f"---\n\nChange under review: {change} (plans/changes/{change}/)."]
    if extra:
        parts.append(extra)
    parts += [ANSWER_FORMAT, READ_REQUEST]
    return "\n\n".join(parts)


def prompt_input(path: Path, inputs: dict[Path, bytes] | None = None) -> str:
    """Read a prompt dependency once into the run's snapshot, keeping its bytes for restoration."""
    if inputs is None:
        return path.read_text(encoding="utf-8")
    if path not in inputs:
        inputs[path] = path.read_bytes()
    return inputs[path].decode("utf-8")


def work_prompt(
    root: Path, prompt_file: str, change: str, extra: str = "", inputs: dict[Path, bytes] | None = None
) -> str:
    """A work phase, the repository rules and its inputs, without review row instructions."""
    body = prompt_input(root / "prompts" / prompt_file, inputs)
    rules = prompt_input(root / "AGENTS.md", inputs)
    parts = [
        body.rstrip(),
        f"---\n\nChange: {change} (`plans/changes/{change}/`).",
        f"## Repository agent rules\n\n{rules.rstrip()}",
    ]
    if extra:
        parts.append(extra)
    parts.append(READ_REQUEST)
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# The reviews - one launch path for every reviewer call
# ---------------------------------------------------------------------------


def endpoint_entry(root: Path) -> dict:
    """The `opencode-go` entry of `model-endpoints.yaml`, read fresh at call time."""
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        raise Refused("model-endpoints.yaml cannot be read") from None
    entry = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == OPENCODE), None)
    if entry is None:
        raise Refused(f"model-endpoints.yaml declares no endpoint {OPENCODE}")
    return entry


def _terms(entry: dict, model: str) -> dict:
    """The model's record in `modelle_terms`, or an empty dict without one."""
    terms = entry.get("modelle_terms")
    record = terms.get(model) if isinstance(terms, dict) else None
    return record if isinstance(record, dict) else {}


def terms_problem(entry: dict, model: str) -> str | None:
    """Why the paid model's data terms are not read (yet), or None when it is admitted.

    A dated, sourced reading must explicitly rule out training. A dated skip
    keeps the model out and names its reason for the handover (ADR 0021,
    decision 5).
    """
    record = _terms(entry, model)
    if record.get("uebersprungen"):
        reason = record.get("grund") or "reason not stated"
        return f"the model {model} was skipped on {record.get('uebersprungen')}: {reason}"
    # Fail closed: an empty skip marker counts as absent only beside a valid
    # reading date, and `gelesen` must be an ISO date, not any truthy value.
    gelesen = record.get("gelesen")
    if not isinstance(gelesen, str) or not DATE_ONLY.fullmatch(gelesen) or not _valid_date(gelesen):
        return f"the model {model} has no dated reading of its data terms (gelesen is not an ISO date YYYY-MM-DD)"
    if not record.get("quelle"):
        return f"the model {model} has no dated reading of its data terms (gelesen/quelle missing)"
    retention = record.get("aufbewahrung")
    if not isinstance(retention, str) or not retention.strip():
        return f"the model {model} has no retention reading (aufbewahrung missing or unreadable)"
    if record.get("training") != "Not used":
        return f"the model {model} has disallowed or unread training terms (training must be Not used)"
    return None


def request_value(entry: dict, model: str) -> float | None:
    """The model's declared cost value `anfragen_5h` (requests per 5 hours, more is cheaper), or None when absent or unusable."""
    value = _terms(entry, model).get("anfragen_5h")
    if isinstance(value, bool) or not isinstance(value, int | float) or value <= 0:
        return None
    return float(value)


def ordered_models(entry: dict, models: list[str]) -> list[str]:
    """The models cheapest first: `anfragen_5h` descending, ties by id, a model without the value last (Q-13).

    `modelle` is a set: its declared order does not count.
    """
    return sorted(
        set(models),
        key=lambda model: (request_value(entry, model) is None, -(request_value(entry, model) or 0.0), model),
    )


def unvalued_models(entry: dict, models: list[str]) -> list[str]:
    """The models that declare no usable `anfragen_5h`; they order last and are named, never dropped silently."""
    return [model for model in ordered_models(entry, models) if request_value(entry, model) is None]


def unread_catalog_ids(entry: dict, free_state: dict) -> list[str]:
    """Non-free ids of the run's fresh overlay that have no `modelle_terms` record, sorted.

    A notice only: such an id is never admitted. A paid model still needs a
    dated terms reading and an `anfragen_5h` in the declaration (Q-13).
    """
    rule = free_state.get("rule") or {}
    suffix = rule.get("id_suffix") or ""
    terms = entry.get("modelle_terms")
    terms = terms if isinstance(terms, dict) else {}
    free = set(free_state.get("selected") or [])
    return sorted(
        model
        for model in free_state.get("overlay") or []
        if model not in free and not (suffix and model.endswith(suffix)) and model not in terms
    )


def cheapest_notice(entry: dict, ladder_ids: list[str], flash: list[str]) -> str | None:
    """A notice when the hand-kept Flash swarm is not the three admitted models with the highest `anfragen_5h`, else None.

    A notice, not a refusal: the maintainer keeps the list (Q-13), and the
    runner never changes it.
    """
    cheapest = [model for model in ladder_ids if request_value(entry, model) is not None][:3]
    if set(flash) == set(cheapest):
        return None
    return (
        f"flash_swarm [{', '.join(flash)}] differs from the three cheapest admitted models "
        f"[{', '.join(cheapest)}] by anfragen_5h; the list stays as declared"
    )


def ladder(root: Path) -> list[str]:
    """The eligible paid models of the `opencode-go` entry, cheapest first: each is one later round.

    The order is the runner's: `anfragen_5h` descending, ties by id, a model
    without the value last (Q-13). A model the list does not hold is no id in
    the code: adding or replacing one is a pull request that touches
    `model-endpoints.yaml` and nothing else (spec, criterion 5). A model whose
    data terms were not read is not eligible: it is skipped, and the skip is
    named (ADR 0021, decision 5).
    """
    entry = endpoint_entry(root)
    models = [str(model) for model in entry.get("modelle") or []]
    eligible = [model for model in models if terms_problem(entry, model) is None]
    return ordered_models(entry, eligible)


def skipped_models(root: Path) -> list[str]:
    """The declared paid models that are not eligible, each named with its reason (ADR 0021, decision 5)."""
    entry = endpoint_entry(root)
    named = []
    declared = [str(model) for model in entry.get("modelle") or []]
    for model in dict.fromkeys([*declared, *(entry.get("flash_swarm") or [])]):
        problem = terms_problem(entry, model) if model in declared else "not a declared paid model"
        if problem is not None:
            named.append(f"{model} ({problem})")
    return named


def flash_problem(entry: dict) -> str | None:
    """Why the entry's `flash_swarm` cannot be the second round's membership, or None.

    The swarm is a subset of the eligible paid models, each named once (spec,
    criterion 8): a model that is skipped or undeclared cannot review in it.
    """
    flash = entry.get("flash_swarm")
    if flash is None:
        return "the endpoint declares no flash_swarm"
    if not isinstance(flash, list) or not all(isinstance(model, str) and model for model in flash):
        return "flash_swarm must be a list of model ids"
    if len(set(flash)) != len(flash):
        return "flash_swarm names a model twice"
    return None


# ---------------------------------------------------------------------------
# The free stage: rule, admission, live discovery, the bounded diff
# ---------------------------------------------------------------------------


DATE_ONLY = re.compile(r"\d{4}-\d{2}-\d{2}")


def _valid_date(text: str) -> bool:
    try:
        dt.date.fromisoformat(text)
    except ValueError:
        return False
    return True


def _exception_problem(kind: str, record) -> str | None:
    """Why one include/exclude record of the free rule is not usable, or None.

    An exception is a decision: it carries the id, the date it was made and the
    reason. An entry without one of the three is not an intentional exclusion
    or inclusion (spec, criterion 5).
    """
    if not isinstance(record, dict):
        return f"an entry of the free rule's {kind} list must be a record with id, date and reason"
    for field in ("id", "date", "reason"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"an entry of the free rule's {kind} list has no {field}"
    if not DATE_ONLY.fullmatch(record["date"]) or not _valid_date(record["date"]):
        return f"the free rule's {kind} entry for {record['id']} has no ISO date (YYYY-MM-DD)"
    return None


def free_rule_problems(entry: dict) -> list[str]:
    """Everything that makes the entry's `free_stage` rule unusable; shared with the declaration test.

    The provider must equal the Go launch provider and must not be Zen: the free
    class never reaches a Zen id, whatever a rule says. The rule needs a suffix
    or an include list to select from, exceptions carry id, date and reason,
    and the input is the implementation diff and nothing else.
    """
    rule = entry.get("free_stage")
    if not isinstance(rule, dict):
        return ["the endpoint declares no usable free_stage rule"]
    problems = []
    provider = rule.get("provider")
    if not isinstance(provider, str) or not provider.strip():
        problems.append("the free rule names no provider")
    elif provider == ZEN:
        problems.append("the free rule may not select the Zen provider")
    elif provider != OPENCODE:
        problems.append(f"the free rule provider must equal the launch provider {OPENCODE}")
    suffix = rule.get("id_suffix", "")
    if not isinstance(suffix, str):
        problems.append("the free rule's id_suffix is no string")
    includes = rule.get("include") or []
    if not suffix and not includes:
        problems.append("the free rule would select nothing: give an id_suffix or an include list")
    for kind in ("include", "exclude"):
        entries = rule.get(kind) or []
        if not isinstance(entries, list):
            problems.append(f"the free rule's {kind} list is no list")
            continue
        for record in entries:
            problem = _exception_problem(kind, record)
            if problem:
                problems.append(problem)
    if rule.get("input") != "implementation-diff":
        problems.append("the free rule's input must be implementation-diff")
    return problems


def free_rule(root: Path) -> dict:
    """The `free_stage` rule of the declaration, refused when it is not usable."""
    entry = endpoint_entry(root)
    problems = free_rule_problems(entry)
    if problems:
        raise Refused("; ".join(problems) + ".")
    return entry["free_stage"]


def free_admission_problem(root: Path, model: str, selected: list[str]) -> str | None:
    """Why the free class does not admit this call, or None (spec, criterion 7).

    The class is bound to this run's live discovery: the id must be in the
    selection the forced refresh produced, under the configured provider. A
    paid model is refused by name, a Zen or guessed id by absence. The paid and
    session paths keep the strict individual declaration; the endpoint must
    itself stay clearable (framework, residency).
    """
    entry = endpoint_entry(root)
    problems = free_rule_problems(entry)
    if problems:
        return "; ".join(problems)
    allowed = entry.get("darf_sehen")
    if not isinstance(allowed, list) or "framework" not in allowed:
        return f"the endpoint {OPENCODE} may not see framework content"
    residency = entry.get("residenz")
    if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
        return f"the endpoint {OPENCODE} states no data residency"
    excluded = excluded_problem(root, model)
    if excluded:
        return excluded
    if model in [str(item) for item in entry.get("modelle") or []]:
        return f"the model {model} is a paid model; the free class does not admit it"
    if model not in selected:
        return f"the model {model} is not in this run's discovered free selection"
    return None


def parse_catalog(output: str) -> list[dict]:
    """The provider/model rows of `pi --list-models`, in catalog order.

    The table's columns are whitespace-separated and the ids hold no space; the
    header row is dropped. Output without one model row is malformed and
    refuses - it never becomes an empty selection that launches a call
    (spec, criterion 5).
    """
    lines = [line.split() for line in output.splitlines() if line.strip()]
    if not lines or "provider" not in lines[0] or "model" not in lines[0]:
        raise Refused("`pi --list-models` printed no model table header; catalog parse failed.")
    header = lines[0]
    if len(set(header)) != len(header):
        raise Refused("`pi --list-models` model table has duplicate columns; catalog parse failed.")
    provider, model = header.index("provider"), header.index("model")
    rows = []
    for number, parts in enumerate(lines[1:], 2):
        if len(parts) != len(header):
            raise Refused(f"`pi --list-models` model table parse failed at line {number}: wrong column count.")
        rows.append({"provider": parts[provider], "model": parts[model]})
    if not rows:
        raise Refused("`pi --list-models` printed no model table rows; the free stage cannot be filled.")
    return rows


def select_free(rule: dict, catalog: list[dict]) -> list[str]:
    """The catalog ids of the rule's provider matching suffix or include, minus excludes, in catalog order.

    Exclusions win, also over an include; a Zen id cannot pass, because only
    the configured provider's rows are read; an include for an id the catalog
    does not hold selects nothing (spec, criterion 5).
    """
    suffix = rule.get("id_suffix", "")
    includes = {str(record["id"]) for record in rule.get("include") or []}
    excludes = {str(record["id"]) for record in rule.get("exclude") or []}
    chosen: list[str] = []
    for row in catalog:
        if row["provider"] != rule["provider"]:
            continue
        model = row["model"]
        if model in excludes:
            continue
        if (model in includes or (suffix and model.endswith(suffix))) and model not in chosen:
            chosen.append(model)
    return chosen


def overlay_store(agent: Path, provider: str) -> dict:
    """The provider's complete refreshed definitions, in Pi's `models-store.json` format.

    Pi 1.2.0 (`core/remote-catalog-provider.js`, `core/models-store.js`)
    persists the forced refresh's pi.dev catalog there under the provider id,
    as `{models, lastModified, etag, checkedAt}`. `pi --list-models` lists the
    overlay merged with Pi's shipped baseline (`mergeModels`), which keeps
    baseline ids that pi.dev no longer lists; only the persisted overlay says
    what the fresh catalog holds (Q-13). A missing or unreadable store refuses.
    """
    path = agent / "models-store.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        raise Refused(
            f"the forced catalog refresh left no readable {path.name}; the fresh overlay cannot be told "
            "from Pi's shipped list, so the free stage is not entered."
        ) from None
    entry = data.get(provider) if isinstance(data, dict) else None
    models = entry.get("models") if isinstance(entry, dict) else None
    if not isinstance(models, list):
        raise Refused(f"the refreshed {path.name} holds no catalog for {provider}; the free stage is not entered.")
    return {provider: entry}


def overlay_ids(agent: Path, provider: str) -> set[str]:
    """Ids in the refreshed provider overlay; definitions are retained by discovery."""
    return {
        str(model["id"])
        for model in overlay_store(agent, provider)[provider]["models"]
        if isinstance(model, dict) and model.get("id")
    }


def activate_overlay(agent: Path, store: dict) -> None:
    """Activate fetched definitions through Pi's explicit model configuration.

    Pi 1.2.0 restores its remote cache only for server dates newer than its
    shipped catalog. A successful fresh retrieval need not carry such a date.
    Keep models-store.json as retrieval evidence and use models.json's model
    definitions to activate that exact catalog independently of cache age.
    Only model definitions cross here, never provider auth configuration.
    """
    # Pi resolves explicit-config headers as shell commands / environment
    # templates. Escape catalog literals at this boundary only: never mutate
    # the fetched store (the retrieval evidence and persisted run snapshot).
    providers = {}
    for provider, entry in store.items():
        models = []
        for definition in entry.get("models", []):
            model = dict(definition)
            if "headers" in model:
                headers = {}
                for name, value in model["headers"].items():
                    literal = value.replace("$", "$$")
                    headers[name] = "$" + literal if literal.startswith("!") else literal
                model["headers"] = headers
            models.append(model)
        if models:
            providers[provider] = {"models": models}
    (agent / "models.json").write_text(json.dumps({"providers": providers}), encoding="utf-8")


def discover_free(root: Path, *, allow_empty: bool = False) -> dict:
    """The free stage's members, from a forced live catalog refresh this run owns.

    One fresh scratch HOME and agent directory serve both commands: first the
    forced refresh (`pi update --models`), then the listing there. When the
    refresh fails or runs over its limit, the run refuses - a cached catalog is
    never listed (spec, criterion 5). The check time, the source, the Pi
    version, the rule and both lists are pinned into the run state. The
    catalog is a live intermediary: this proves which catalog was read, not
    what OpenCode Go actually bills for the call.
    """
    rule = free_rule(root)
    key = reviewer_key()
    with tempfile.TemporaryDirectory(prefix="stage2-free-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        home = scratch / "home"
        home.mkdir()
        env = foreign_env({"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "OPENCODE_API_KEY": key})
        limit = f"the catalog refresh's limit of {PI_DISCOVERY_SECONDS} seconds"
        try:
            refresh = launch(
                [str(PI_WRAPPER), "update", "--models"], scratch, env, timeout=PI_DISCOVERY_SECONDS, limit=limit
            )
        except CallFailed as error:
            raise Refused(
                f"the live catalog refresh did not end within {PI_DISCOVERY_SECONDS} seconds; "
                f"no stale cache is listed. ({error})"
            ) from None
        if refresh.returncode != 0:
            raise Refused(
                f"`{PI_WRAPPER} update --models` ended {refresh.returncode}; the free stage is not filled "
                "from a stale cache."
            )
        store = overlay_store(agent, rule["provider"])
        activate_overlay(agent, store)
        try:
            listing = launch(
                [str(PI_WRAPPER), "--list-models"], scratch, env, timeout=PI_DISCOVERY_SECONDS, limit=limit
            )
        except CallFailed as error:
            raise Refused(
                f"the model listing did not end within {PI_DISCOVERY_SECONDS} seconds; the free stage is not entered. ({error})"
            ) from None
        fresh = {
            str(model["id"])
            for model in store.get(rule["provider"], {}).get("models", [])
            if isinstance(model, dict) and model.get("id")
        }
    if listing.returncode != 0:
        raise Refused(f"`{PI_WRAPPER} --list-models` ended {listing.returncode}; the free stage stays unentered.")
    catalog = parse_catalog(listing.stdout or "")
    # Only ids the fresh overlay carries: an id that only Pi's shipped list holds is not selected (Q-13).
    selected = [model for model in select_free(rule, catalog) if model in fresh]
    if not selected and not allow_empty:
        raise Refused("the live catalog holds no free model for the configured rule; the free stage is not entered.")
    return {
        "checked_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "source": "pi.dev",
        "pi_version": PI_VERSION,
        "rule": json.loads(json.dumps(rule)),
        "catalog": catalog,
        "selected": selected,
        "overlay": sorted(fresh),
        "models_store": store,
        "billing": "not measured: pi.dev is a live catalog, not a billing statement",
    }


# The free diff sees source and test code only, never dependency or generated
# trees, binary files, documentation, plans, declarations or locks (criterion 3).
FREE_DIFF_SKIP_PARTS = {"node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".git", ".beads"}
FREE_DIFF_TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".lock", ".txt", ".cfg", ".ini", ".toml"}


def _looks_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return b"\0" in handle.read(8192)
    except OSError:
        return True


def _free_candidate(root: Path, rel: str, base: str | None = None) -> bool:
    """Whether a changed file may enter the free diff: source and test code only.

    Python in `scripts/` and `tests/`, and executable source under `tools/`.
    Symlinks, dependency and generated trees, binary files, documentation,
    plans, declarations and locks never pass (criterion 3).
    """
    path = Path(rel)
    parts = path.parts
    if not parts or path.is_absolute() or ".." in parts:
        return False
    if any(part in FREE_DIFF_SKIP_PARTS for part in parts):
        return False
    full = root / path
    if any((root / parent).is_symlink() for parent in [path, *path.parents]):
        return False
    executable = os.access(full, os.X_OK)
    if full.exists():
        if not full.is_file() or _looks_binary(full):
            return False
    else:
        if base is None:
            return False
        # Deleted source is classified by its merge-base blob and mode.
        tree = _git_output(root, "ls-tree", base, "--", rel)
        if not tree or tree.split()[0] not in {"100644", "100755"}:
            return False
        try:
            blob = subprocess.run(
                [GIT, "-C", str(root), "show", f"{base}:{rel}"],
                capture_output=True,
                check=False,
                timeout=GIT_SECONDS,
            )
        except subprocess.TimeoutExpired as error:
            raise Refused(f"git show did not finish within {GIT_SECONDS // 60} minutes") from error
        if blob.returncode or b"\0" in blob.stdout:
            return False
        executable = tree.split()[0] == "100755"
    if parts[0] == "scripts":
        return path.suffix == ".py"
    if parts[0] == "tests":
        return path.suffix == ".py"
    if parts[0] == "tools":
        try:
            return executable and path.suffix not in FREE_DIFF_TEXT_SUFFIXES
        except OSError:
            return False
    return False


def _merge_base(root: Path) -> str:
    """The merge base with origin/main, refused when there is none."""
    done = subprocess.run(
        [GIT, "-C", str(root), "merge-base", "HEAD", "origin/main"], capture_output=True, text=True, check=False
    )
    base = done.stdout.strip()
    if done.returncode != 0 or not base:
        raise Refused("there is no merge base with origin/main; the diff cannot be built.")
    return base


def _bound_hunks(rel: str, piece: str) -> str:
    """One file's diff, cut at the per-file bound with a naming marker."""
    lines = piece.splitlines()
    if len(lines) <= FREE_DIFF_MAX_LINES:
        return "\n".join(lines)
    kept = "\n".join(lines[:FREE_DIFF_MAX_LINES])
    return f"{kept}\n## (the diff of {rel} was cut at {FREE_DIFF_MAX_LINES} lines)"


def bounded_review_diff(diff: str) -> tuple[str, str | None]:
    """The prompt's diff, cut at `REVIEW_DIFF_MAX_LINES`, and what the cut left out.

    The caller writes the second half into the round record: a clean answer over a cut diff is not a
    clean answer about the change, and the record must say which of the two it was. The free round is
    bounded too (R-12 of the review-swarm review): it carries the same diff, and an uncapped prompt
    would read as a limit that is none.
    """
    # Split on "\n" only, as git counts: `splitlines()` also splits on CR and form feed, which inflates the
    # count and rewrites the kept part's line ends (O191-4).
    lines = diff.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) <= REVIEW_DIFF_MAX_LINES:
        return diff, None
    note = f"the change diff was cut at {REVIEW_DIFF_MAX_LINES} of {len(lines)} lines"
    return "\n".join([*lines[:REVIEW_DIFF_MAX_LINES], f"## ({note}; the rest is not carried)"]), note


def free_diff(root: Path) -> str:
    """The implementation diff the free swarm reviews: bounded hunks of source and test code only.

    The same merge base as `change_diff`, uncommitted and untracked files
    included (criterion 3). Every file passes `_free_candidate`; each file's
    hunks are bounded and the whole diff is, so no whole source file travels.
    """
    base = _merge_base(root)
    flags = ["--no-color", "--no-ext-diff", "--no-textconv"]
    changed = [name for name in _git_output(root, "diff", "--name-only", "-z", base).split("\0") if name]
    untracked = [
        name for name in _git_output(root, "ls-files", "-z", "--others", "--exclude-standard").split("\0") if name
    ]
    untracked_set = set(untracked)
    names: list[str] = []
    seen: set[str] = set()
    for rel in [*changed, *untracked]:
        if rel not in seen:
            seen.add(rel)
            if _free_candidate(root, rel, base):
                names.append(rel)
    parts: list[str] = []
    total = 0
    for rel in names:
        if rel in untracked_set:
            piece = _git_output(root, "diff", *flags, "--no-index", "--", "/dev/null", rel, allow=(0, 1))
        else:
            piece = _git_output(root, "diff", *flags, base, "--", rel)
        bounded = _bound_hunks(rel, piece)
        if not bounded.strip():
            continue
        parts.append(bounded)
        total += bounded.count("\n")
        if total >= FREE_DIFF_MAX_TOTAL:
            parts.append(
                f"(the implementation diff was cut at {FREE_DIFF_MAX_TOTAL} lines; later files are not carried)"
            )
            break
    return "\n".join(parts)


# The free reviewer's static instructions: what it reviews and how it answers.
# Deliberately no READ_REQUEST and no repository-reading sentence - the call has
# no tools and its only input is the diff below (criterion 3).
FREE_REVIEW_BODY = (
    "You are one member of a parallel reviewer swarm; the round's other members review the same diff.\n"
    "Your only input is the implementation diff below. You have no tools and read nothing else: do not ask\n"
    "for files, context or the repository - answer from the diff alone.\n"
    "\n"
    "Report findings a reader of the diff alone can support:\n"
    "- a defect the change would put into the tree (correctness, security, credential exposure);\n"
    "- a test the change breaks, or a behavior change without the test that holds it;\n"
    "- a contradiction between the changed lines themselves.\n"
    "Report nothing you would need the rest of the repository to confirm."
)


def reviewer_key() -> str:
    """The OpenCode Go key, read from the secrets file at call time. Never an argument."""
    key = read_secret("OPENCODE_GO_KEY")
    if key is None:
        raise Refused(f"OPENCODE_GO_KEY is not in the secrets file {secrets_path()}.")
    return key


def thread_id(stdout: str) -> str | None:
    """The `thread_id` of the first JSON line of type `thread.started`."""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "thread.started" and event.get("thread_id"):
            return str(event["thread_id"])
    return None


def run_codex(
    ctx: Context, prompt: str, resume: str | None = None, writable: bool = False, *, verb: str
) -> tuple[str, str]:
    """One Codex call, first or resumed, pinned the same way. Returns (answer, thread id).

    A review reads in the CLI's `read-only` sandbox; a draft writes in
    `workspace-write`, and the runner puts back what lands outside the change
    folder. No call takes a bypass flag (spec, criterion 1). The reasoning
    effort is the caller verb's entry of `CODEX_EFFORTS`, passed explicitly on
    every argv, a resumed call included; that a resumed thread actually runs at
    that effort inside Codex is not asserted (bead coding-harness-yzk, Q-6).
    Only the verbs `CODEX_EFFORTS` names (draft, repair, review) may carry a
    Codex route; any other verb stops with a `KeyError` before the call.
    """
    _, model, _ = CODEX
    effort = CODEX_EFFORTS[verb]
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        answer_file = Path(tmp) / "answer.md"
        command = ["codex", "exec"]
        if resume:
            command += ["resume", resume]
        command += [
            "--json",
            "-m",
            model,
            "-c",
            f'model_reasoning_effort="{effort}"',
            "-c",
            f'sandbox_mode="{"workspace-write" if writable else "read-only"}"',
            "--disable",
            "hooks",
            "--disable",
            "memories",
            "-o",
            str(answer_file),
            prompt,
        ]
        done = launch(command, ctx.root, foreign_env({}))
        thread = thread_id(done.stdout or "")
        if done.returncode != 0:
            raise fail("codex", done, f"exit {done.returncode}")
        if thread is None:
            raise fail("codex", done, "no thread.started event")
        try:
            answer = answer_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise fail("codex", done, "no answer file") from error
    return answer, thread


def require_pi() -> None:
    """Refuse unless the repository wrapper prints exactly the pinned version (spec, criterion 27).

    The wrapper is the one path to Pi (ADR 0019): it refuses a missing,
    mismatched or unusable local install before any model request, and this
    check ties its answer to the manifest pin. Runs before the prompt check,
    the call line and any call, in a scratch directory with no key: a Pi off
    the pin sends nothing. The session verb calls it after its argument and
    handover checks.
    """
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        env = foreign_env({"HOME": tmp, "PI_CODING_AGENT_DIR": tmp})
        try:
            done = launch(
                [str(PI_WRAPPER), "--version"],
                Path(tmp),
                env,
                timeout=PI_VERSION_SECONDS,
                limit=f"the version check's limit of {PI_VERSION_SECONDS} seconds",
            )
        except CallFailed as error:
            raise Refused(
                f"{PI_WRAPPER} could not be checked ({error}); it is not the pinned {PI_VERSION}; no call starts."
            ) from None
    said = (done.stdout or "").strip()
    if done.returncode != 0:
        # The wrapper's own refusal names the defect; its last lines travel with this one.
        tail = "\n".join((done.stderr or "").splitlines()[-5:])
        detail = f": {tail}" if tail else ""
        raise Refused(
            f"{PI_WRAPPER} --version ended {done.returncode}; it is not the pinned {PI_VERSION}; "
            f"no call starts{detail}."
        )
    if said != PI_VERSION:
        raise Refused(f"pi {said or 'printed nothing'} is not the pinned {PI_VERSION}; no call starts.")


def remaining(deadline: float | None) -> float:
    """The seconds this call may still take: the round's deadline, else `REVIEWER_MINUTES` (R-8).

    An expired deadline fails before launch. Granting each late replacement one extra second would
    let a round grow with the remaining ladder instead of sharing one time budget.
    """
    if deadline is None:
        return REVIEWER_MINUTES * 60
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise CallFailed("the round time limit expired; no further reviewer starts")
    return seconds


def run_reviewer(
    ctx: Context,
    model: str,
    prompt: str,
    key: str,
    *,
    free: bool = False,
    timeout_seconds: int | None = None,
    task: str | None = None,
    deadline: float | None = None,
) -> str:
    """One reviewer call through Pi with this run's refreshed OpenCode Go definitions.

    The launch is the measured set (spec, criterion 8), started through the
    repository wrapper (ADR 0019): the rung's id under the `opencode-go`
    provider, thinking `max` (Pi clamps it per model), the read-only tools,
    every discovery switched off, no session, retries off. Each call gets its
    own scratch directory: a `HOME`, an agent directory with retry settings
    and the run's refreshed provider definitions, and the prompt file. The key reaches Pi as
    `OPENCODE_API_KEY` only. Returns the scrubbed answer. A call that has not
    ended after `REVIEWER_MINUTES` is stopped (criterion 15).

    A free call (`free=True`, ADR 0021 decision 3) gets `--no-tools` instead of
    the read tools and starts in its scratch directory, not the worktree: its
    only input is the prompt it is given.
    """
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        store = getattr(ctx, "models_store", None)
        if store is not None:
            (agent / "models-store.json").write_text(json.dumps(store), encoding="utf-8")
            activate_overlay(agent, store)
        home = scratch / "home"
        home.mkdir()
        prompt_file = scratch / "review-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        command = [
            str(PI_WRAPPER),
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
            *(["--no-tools"] if free else ["--tools", PI_TOOLS]),
            "--thinking",
            "max",
            "--model",
            f"{OPENCODE}/{model}",
            "--append-system-prompt",
            str(prompt_file),
            task or f"Review the change {ctx.change} as the appended instructions say.",
        ]
        env = foreign_env({"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "OPENCODE_API_KEY": key})
        done = launch(
            command,
            scratch if free else ctx.root,
            env,
            key,
            timeout=timeout_seconds or remaining(deadline),
            limit=(
                f"the availability probe limit of {timeout_seconds} seconds"
                if timeout_seconds
                else f"the reviewer time limit of {REVIEWER_MINUTES:g} minutes"
            ),
        )
        if done.returncode != 0:
            raise fail("pi", done, f"exit {done.returncode}", key, model)
        answer = scrub(done.stdout or "", key)
        if not answer.strip():
            # "No finding" is an answer; nothing at all is a call that failed.
            raise fail("pi", done, "the answer is empty", key, model)
    return answer


def run_swarm(
    ctx: Context,
    members: list[str],
    prompts: dict[str, str],
    key: str,
    *,
    free: bool,
    deadline: float | None = None,
) -> dict[str, str | Exception]:
    """Every member called concurrently, each in its own scratch directories; only the parent writes.

    The answers come back per member: the scrubbed answer, or the exception
    that failed the member (a nonzero exit, a timeout, an empty answer). A
    member's failure never discards another member's answer (criterion 4).
    Without parsed findings, only the explicit no-finding response succeeds.

    `deadline` is the round's one deadline (`time.monotonic()` seconds): members and every
    replacement share it, so a round cannot outlast `REVIEWER_MINUTES` by summing its members'
    limits (R-8 of the review-swarm review).
    """
    answers: dict[str, str | Exception] = {}

    def one(member: str) -> None:
        try:
            answer = run_reviewer(ctx, member, prompts[member], key, free=free, deadline=deadline)
            rows, _rest = parse_rows(answer)
            # No arbitrary prose (including a refusal or context-limit error)
            # can certify a clean round. Commentary beside findings is kept.
            if not rows and answer.strip() != "No finding.":
                raise CallFailed("malformed finding output: expected six-cell findings or exactly 'No finding.'")
            answers[member] = answer
        except Exception as error:  # noqa: BLE001 - a member's failure is recorded, not raised, here
            answers[member] = error

    threads = [threading.Thread(target=one, args=(member,), name=f"stage2-swarm-{member}") for member in members]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return answers


def taken_in_round(rows: list[list[str]], round_number: int) -> bool:
    """Whether the round wrote at least one row whose Status begins `taken` or `fixed`.

    A row the repair has marked `fixed` counts like the taken one it was, so
    repairing a round's row neither cleans that round nor cancels the next one
    (ADR 0017 decision 6, as amended by ADR 0021 decision 7; ADR 0015's
    three-round reading is superseded).
    """
    prefix = f"L{round_number}-"
    return any(row[0].startswith(prefix) and row[7].lower().startswith(("taken", "fixed")) for row in rows)


def _last_release(text: str) -> int:
    """The start of the last line the release block begins on, -1 without one.

    The heading is matched at the start of a line: a failed attempt's block quotes it with `>`, and a
    quoted heading is not the block's beginning (criterion 12).
    """
    matches = list(RELEASE_LINE.finditer(text))
    return matches[-1].start() if matches else -1


def restart_floor(findings_text: str) -> int:
    """The round the last restart follows, 0 without one: the stops read only the rounds after it."""
    matches = list(RESTART_LINE.finditer(findings_text))
    return int(matches[-1].group(2)) if matches else 0


def restarted_fresh(record: str | None, findings_text: str) -> bool:
    """Whether the last restart stands after the last release with no record: the next run is fresh.

    A restarted run that completed a round has a record, and after its own release a block that follows
    the restart line and carries the new snapshot - from then on the run continues as any other.
    """
    matches = list(RESTART_LINE.finditer(findings_text))
    return record is None and bool(matches) and matches[-1].start() > _last_release(findings_text)


def released_rows(findings_text: str) -> list[list[str]]:
    """The loop rows of the last released block in findings.md, with the status they were decided by."""
    start = _last_release(findings_text)
    if start < 0:
        return []
    block = findings_text[start:]
    cut = KEPT_FROM.search(block)
    if cut:
        block = block[
            : cut.start()
        ]  # what follows is the reviewers' words, carried as they came, not rows of the record
    rows = []
    for line in block.splitlines():
        cells = split_row(line)
        if cells and len(cells) == len(RELEASED_COLUMNS) and LOOP_ID.fullmatch(cells[0]):
            rows.append(cells)
    return rows


def findings_rows(text: str) -> tuple[list[list[str]], list[list[str]]]:
    """The released loop rows (ten cells) and the phase-6 rows (nine cells) of findings.md, any status.

    Every released block and every phase-6 table is read. Section by section, a line that begins `## `
    opens the next: under a heading that begins RELEASE_HEADING, the ten-cell lines with a loop id, up
    to `Kept from the loop record:`; under a heading that begins `## Phase 6`, the nine-cell lines that
    are not furniture. Any `## ` line ends a section, and a line starting with `>` is never a row
    (`split_row` already returns None for it).
    """
    released: list[list[str]] = []
    phase6: list[list[str]] = []
    kind = ""
    for line in text.splitlines():
        if line.startswith("## "):
            kind = ""
            if line.startswith(RELEASE_HEADING):
                kind = "released"
            elif line.startswith("## Phase 6"):
                kind = "phase-6"
            continue
        if kind == "released" and KEPT_FROM.match(line):
            kind = ""  # what follows is the reviewers' words, carried as they came, not rows
            continue
        if not kind:
            continue
        cells = split_row(line)
        if not cells or _furniture(cells):
            continue
        wide = len(cells) == len(RELEASED_COLUMNS) and LOOP_ID.fullmatch(cells[0])
        if (kind == "released" and wide) or (kind == "phase-6" and len(cells) == len(ROW_COLUMNS)):
            (released if kind == "released" else phase6).append(cells)
    return released, phase6


def repair_targets(ctx: Context, record: str | None) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Every taken row with its place (record, released block, phase-6 table), and the IDs that hold the repair.

    A record row whose Status begins none of `taken`, `rejected` and `fixed` waits, and so does a
    phase-6 row whose Status is blank or begins `open`: one call should carry every taken row, so the
    verb refuses while a row stands undecided.
    """
    taken: list[tuple[str, list[str]]] = []
    waiting: list[str] = []
    if record is not None:
        for row in record_rows(record):
            status = row[7].lower()
            if status.startswith("taken"):
                taken.append(("record", row))
            elif not (status.startswith("rejected") or status.startswith("fixed")):
                waiting.append(row[0])
    text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
    released, phase6 = findings_rows(text)
    for place, rows in (("released", released), ("phase-6", phase6)):
        for row in rows:
            status = row[7].lower()
            if status.startswith("taken"):
                taken.append((place, row))
            elif place == "phase-6" and not (status.startswith("rejected") or status.startswith("fixed")):
                waiting.append(row[0])
    return taken, waiting


# A taken Status that names a fix in a legacy hand-written form needs clarification before repair.
# Quoted marker examples are not completion claims. Match unquoted markers without regard to case,
# as every Status read here is (bead coding-harness-ugi).
LEGACY_FIXED = ("; fixed by", "; fixed:", "; repaired by")


def legacy_completed(status: str) -> bool:
    """Whether a Status still begins `taken` while naming a fix in one of the three legacy forms."""
    lowered = re.sub(r"`+[^`]*`+", "", status).lower()
    return any(marker in lowered for marker in LEGACY_FIXED)


def spec_review(root: Path, change: str) -> None:
    """Phase 2a: Opus 5.5 in a fresh context reads the spec (ADR 0016).

    The call is a headless Claude Code run with read-only tools and no session
    kept: the reviewer is recorded by the rows alone, so phase 6 starts a fresh
    Codex session where no phase-2a session was recorded.
    """
    ctx = preflight(root, change, OPUS)
    prompt = phase_prompt(root, "02a-spec-review.md", change)
    begin_call(ctx, "spec-review", OPUS, prompt)
    answer = run_work_model(ctx, prompt, OPUS, writable=False)
    rows, _ = parse_rows(answer)
    append(ctx.findings, f"## Phase 2a — Opus 5.5, {today()}\n\n{answer_block(rows, answer, 'Opus')}")
    print(f"spec-review: {len(rows)} rows appended to {ctx.findings.relative_to(root)}")


def recorded_2a_session(text: str) -> str | None:
    """The session id of the last `## Phase 2a` block, when that block is a Codex one with its line.

    Only then does phase 6 resume (spec, criteria 30 and 31): the last block is the
    change's latest spec review, so a block headed `Opus 5.5`, and a Codex block
    without its `Reviewer session: codex` line, leave no session to resume.
    """
    start = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("## Phase 2a"):
            start = index
    if start is None:
        return None
    block = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        block.append(line)
    if "Opus 5.5" in lines[start]:
        return None
    found = SESSION_LINE.search("\n".join(block))
    return found.group(1) if found else None


def rejected_review_block(answer: str, thread: str) -> str:
    """The evidence of a phase-6 answer that is neither six-cell findings nor exactly `No finding.`.

    The block stands beside the authoritative phase-6 records, never inside them: its heading does
    not start `## Phase 6`, so the next review is no re-check because of it, and the runner writes
    no verdict line and no no-finding claim of its own here. The answer stands quoted, so control
    text it carries - a verdict line, a heading, table rows - stays the reviewer's words; an empty
    answer is said so plainly. Nothing was released: the loop record stands for the next attempt.
    """
    kept = quote_reviewer(answer) if answer.strip() else "The answer was empty or whitespace only."
    return "\n\n".join(
        [
            f"## Rejected phase-6 answer — Codex, {today()}",
            "The review call's answer was neither six-cell findings nor exactly `No finding.`; no verdict "
            f"was recorded and nothing was released (Codex thread: {thread}). The answer, as it came:",
            kept,
        ]
    )


def review(root: Path, change: str) -> None:
    """Phase 6: verdict first, then release and mark the loop rows.

    A re-check after an earlier `## Phase 6` block in `findings.md` starts a
    fresh read-only Codex session. The first phase-6 review resumes a recorded
    Codex phase-2a session, otherwise starts fresh; loop marks resume the verdict thread.
    """
    ctx = preflight(root, change, CODEX)
    record = read_record(change, root)
    if record is not None:
        refusal = undecided_refusal(record_rows(record), "decide them first")
        if refusal:
            raise Refused(refusal)
    text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
    recorded = recorded_2a_session(text)
    recheck = any(line.startswith("## Phase 6") for line in text.splitlines())
    if recheck:
        # An earlier phase-6 block makes this a fresh read-only session: no 2a thread, no earlier
        # verdict thread, never the repair's (ADR 0017). The first review keeps ADR 0016's rule.
        recorded = None
    prompt = phase_prompt(root, "06-review.md", change, "Write only your verdict now.")
    begin_call(ctx, "review", CODEX, prompt)
    answer, thread = run_codex(ctx, prompt, resume=recorded, verb="review")
    rows, _ = parse_rows(answer)
    # The verdict accepts only what a loop round's answer may say (the swarm's rule, at the verdict
    # boundary): six-cell findings, or exactly `No finding.`. An empty, refused or malformed answer
    # records no verdict, releases nothing, and stands as rejected evidence for the next attempt.
    if not rows and answer.strip() != "No finding.":
        append(ctx.findings, rejected_review_block(answer, thread))
        raise CallFailed("malformed finding output: expected six-cell findings or exactly 'No finding.'")
    block = "\n\n".join(
        [
            f"## Phase 6 — Codex, {today()}",
            answer_block(rows, answer, "Codex"),
            f"Phase 6 verdict: codex {thread}, {today()}",
        ]
    )
    if recorded is None:
        reason = "an earlier ## Phase 6 block makes this a re-check" if recheck else "no phase-2a session was recorded"
        block += f"\nReviewer session: codex {thread} — a fresh session reviewed: {reason}"
    elif thread != recorded:
        block += (
            f"\nReviewer session: codex {thread} — a fresh session reviewed: "
            f"the resume of {recorded} started a new thread"
        )
    append(ctx.findings, block)
    print(f"review: verdict appended to {ctx.findings.relative_to(root)}; session codex {thread}")

    released = release(root, change)
    if not released:
        return
    listing = "\n".join(f"- {r[0]} [{r[1]}, {r[2]}] {r[4]}: {r[5]}" for r in released)
    marks_prompt = "\n\n".join(
        [MARK_FORMAT, "Your verdict stands and is not changed.", f"The loop rows:\n{listing}", READ_REQUEST]
    )
    begin_call(ctx, "review (loop marks)", CODEX, marks_prompt)
    answer, _ = run_codex(ctx, marks_prompt, resume=thread, verb="review")
    marks = parse_marks(answer)
    fill_marks(ctx.findings, [r[0] for r in released], marks)
    print(f"review: {len(marks)} of {len(released)} loop rows marked")


def parse_marks(answer: str) -> dict[str, str]:
    """`<ID>: agree` or `<ID>: disagree — <reason>`, one line per loop row."""
    marks: dict[str, str] = {}
    pattern = re.compile(r"^\W*(L\d+-\d+)\W*:\s*(agree|disagree)\b[\s—–:-]*(.*?)\s*$", re.I)
    for line in answer.splitlines():
        match = pattern.match(line.strip())
        if not match or match.group(1) in marks:
            continue
        verdict, reason = match.group(2).lower(), match.group(3).replace("|", "\\|")
        marks[match.group(1)] = f"disagree — {reason}" if verdict == "disagree" and reason else verdict
    return marks


def fill_marks(findings: Path, ids: list[str], marks: dict[str, str]) -> None:
    """Fill the `Phase 6` cell of each released row, in the block `release` wrote and nowhere else."""
    text = findings.read_text(encoding="utf-8")
    start = _last_release(text)
    head, tail = text[:start], text[start:]
    lines = []
    for line in tail.split("\n"):
        cells = split_row(line)
        if cells and len(cells) == len(RELEASED_COLUMNS) and cells[0] in ids:
            cells[-1] = marks.get(cells[0], "no answer")
            line = "| " + " | ".join(cells) + " |"
        lines.append(line)
    findings.write_text(head + "\n".join(lines), encoding="utf-8")
    stamp_updated(findings)


# ---------------------------------------------------------------------------
# The loop record, release, and the round
# ---------------------------------------------------------------------------


def record_base() -> Path:
    """The directory the loop records live under, read at call time."""
    state = os.environ.get("XDG_STATE_HOME")
    return (Path(state) if state else Path.home() / ".local" / "state") / "coding-harness" / "stage2"


def record_key(change: str, root: Path) -> str:
    """The record's name: the change and a digest of the resolved repository root.

    Two worktrees may hold the same change folder, and one `release-loop` must not delete the
    other's record or hand it another's state (R-2 of the review-swarm review).
    """
    return f"{change}@{hashlib.sha256(str(root.resolve()).encode('utf-8')).hexdigest()[:8]}"


def record_dir(change: str, root: Path) -> Path:
    """Outside the worktree and outside the git directory. A record under the old key stays where it is."""
    return record_base() / record_key(change, root)


def lock_path(change: str, root: Path) -> Path:
    """The lock beside the record, not inside it: `release-loop` removes the record's directory."""
    return record_base() / f"{record_key(change, root)}.lock"


@contextlib.contextmanager
def holding_record(change: str, root: Path) -> Iterator[None]:
    """One runner per loop record at a time (R-14 of the review-swarm review).

    Two runners that both read `consumed: []` pay the same members and number the same round twice,
    and the doubled ids then block `repair`. The lock is advisory, held by the open descriptor, and
    a descriptor dies with its process - so a crashed run leaves no lock behind to break the next.
    """
    path = lock_path(change, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise Refused(
                f"another run holds the loop record `{record_key(change, root)}`; one runner at a time"
            ) from error
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_record(change: str, root: Path) -> str | None:
    path = record_dir(change, root) / "loop.md"
    try:
        return path.read_text(encoding="utf-8") if path.exists() else None
    except (OSError, UnicodeDecodeError) as error:
        raise Refused(f"the loop record {path} cannot be read.") from error


def _record_lines(record: str) -> list[tuple[str, bool]]:
    """Each line of the record, and whether it is the reviewer's words - not the runner's or the orchestrator's.

    The runner writes a round as its heading, then a table or one statement and, when the answer was not
    only six-cell rows, the note `NOT_ROWS_NOTE` and the rest of the answer as it came. The lines after the
    note, up to the next round heading, are the reviewer's; every other line is the record's own. A line
    of the reviewer is quoted when written, so it cannot become a round heading.
    """
    lines = []
    reviewer = False
    for line in record.splitlines():
        if ROUND_HEADING.match(line):
            reviewer = False
        elif not reviewer and line.strip() == NOT_ROWS_NOTE:
            lines.append((line, False))
            reviewer = True
            continue
        lines.append((line, reviewer))
    return lines


def marks_a_test(cell: str) -> bool:
    """Whether a `Broke a test` cell says yes or no, a reason after it allowed (bead coding-harness-ll5).

    `yes — <reason>` and `no — <reason>` stand as well as the bare words; only the leading word is
    evaluated, the reason stays in the record for the reader.
    """
    return bool(re.match(r"(yes|no)\b", cell.strip(), re.I))


def record_rows(record: str) -> list[list[str]]:
    """The loop rows of the record: every table line of its own whose first cell is a loop id.

    Only the record's own lines are read, never the reviewer's words, which are carried as they came: a
    table line the reviewer wrote is not a row the orchestrator has to decide, whatever its first cell says.

    Nine cells are known. A `|` the orchestrator typed into `Status` makes a tenth; the cells between the
    reviewer and the last one are that reason, each pipe escaped. A line with a loop id and fewer cells
    than a row has is not skipped, which would let the release delete it with the record: it is refused,
    by its id.
    """
    rows = []
    for line, reviewer in _record_lines(record):
        cells = None if reviewer else split_row(line)
        if not cells or not LOOP_ID.fullmatch(cells[0]):
            continue
        if len(cells) < len(ROW_COLUMNS):
            raise Refused(
                f"the loop record has a line for {cells[0]} that is not a loop row "
                f"({len(cells)} cells; {len(ROW_COLUMNS)} are needed); mend it, nothing has been deleted."
            )
        if (
            len(cells) > len(ROW_COLUMNS)
            and cells[7].strip().lower().startswith(("taken", "fixed"))
            and not marks_a_test(cells[-1])
        ):
            # A cell was inserted before the mark: the joined Status still begins `taken`/`fixed`, and
            # the last cell is no longer `Broke a test`. A Status that carries an escaped-or-typed `|`
            # with a valid mark in the last cell is a legitimate row and stays one (the review of
            # PR #194); only a row whose last cell is no mark has moved the mark out of its column.
            raise Refused(
                f"the loop record has a line for {cells[0]} with {len(cells)} cells whose Status cell "
                f"starts `{cells[7].strip()}` and whose last cell `{cells[-1].strip()}` is no "
                "`Broke a test` mark: the mark has moved out of its column; mend it, nothing has been deleted."
            )
        rows.append([*cells[:7], " \\| ".join(cells[7:-1]), cells[-1]])
    return rows


def undecided(rows: list[list[str]]) -> list[str]:
    """Rows whose Status begins none of `taken`, `fixed` and `rejected`, or such a row without `yes` or `no`.

    A fixed row is decided when its `Broke a test` is filled like a taken one: the orchestrator writes
    the mark after the repair, before the next round or the release (spec, criterion 25).
    """
    waiting = []
    for row in rows:
        status, broke = row[7].lower(), row[8].lower()
        decided = status.startswith("rejected") or (status.startswith(("taken", "fixed")) and marks_a_test(broke))
        if not decided:
            waiting.append(row[0])
    return waiting


def undecided_refusal(rows: list[list[str]], consequence: str) -> str | None:
    """The refusal that holds the verbs while a row of the record waits, or None when none does.

    An undecided row gets the consequence the caller names. A fixed row whose `Broke a test` is
    neither `yes` nor `no` is decided already: what it waits for is the mark the orchestrator writes
    from the repair run's evidence, so the refusal names that mark instead of asking for a decision
    the row carries (spec, criterion 25).
    """
    waiting = undecided(rows)
    if not waiting:
        return None
    fixed = {row[0] for row in rows if row[7].lower().startswith("fixed")}
    plain = [ident for ident in waiting if ident not in fixed]
    unmarked = [ident for ident in waiting if ident in fixed]
    parts: list[str] = []
    if plain:
        # The values a row may carry are named with the refusal (bead coding-harness-ll5).
        parts.append(
            f"the loop record has undecided rows ({', '.join(plain)}); {consequence} "
            "(`taken — <reason>`, `fixed — <anchor>` or `rejected — <reason>`, and `Broke a test` "
            "`yes`, `no`, `yes — <reason>` or `no — <reason>`)"
        )
    if unmarked:
        parts.append(
            f"the loop record has fixed rows without their `Broke a test` mark ({', '.join(unmarked)}); "
            "write `yes`, `no`, `yes — <reason>` or `no — <reason>` from the repair run's evidence first"
        )
    return "; ".join(parts) + "."


# ---------------------------------------------------------------------------
# Rounds, stops and the run's stage snapshot
# ---------------------------------------------------------------------------


ROUND_ID = re.compile(r"L(\d+)-\d+")


def round_rows(rows: list[list[str]], round_number: int) -> list[list[str]]:
    """The rows of one round, by their `L<n>-` id prefix."""
    prefix = f"L{round_number}-"
    return [row for row in rows if row[0].startswith(prefix)]


def accepted_row(row: list[str]) -> bool:
    """`taken` or `fixed`: a repair preserves the fact that the review accepted the finding (criterion 11)."""
    return row[7].lower().startswith(("taken", "fixed"))


CUT_LINE = "The diff was cut:"


def cut_rounds(record: str | None) -> list[int]:
    """The numbers of the record's rounds whose diff was cut."""
    if not record:
        return []
    heads = list(re.finditer(r"^## Round (\d+) —", record, re.M))
    ends = [head.start() for head in heads[1:]] + [len(record)]
    return [
        int(head.group(1))
        for head, end in zip(heads, ends, strict=True)
        if any(line.startswith(CUT_LINE) for line in record[head.start() : end].splitlines())
    ]


def released_cut_rounds(findings_text: str) -> set[int]:
    """The rounds that every released block of findings.md carries as cut."""
    found: set[int] = set()
    own = False
    for line in findings_text.splitlines():
        if line.startswith("## "):
            own = line.startswith(RELEASE_HEADING)
        elif KEPT_FROM.match(line):
            own = False
        elif own and (match := CUT_ROUNDS_LINE.fullmatch(line)):
            found.update(int(number) for number in match.group(1).split(", "))
    return found


def round_was_cut(record: str | None, round_number: int, findings_text: str = "") -> bool:
    """Whether that round's diff was cut. Such a round cannot end the loop, however clean it reads.

    A member's `No finding.` over a cut diff is a statement about the part it saw; letting it stop the
    loop would certify the change on a diff nobody reviewed in full (P2 of the #191 review). The record
    is deleted by a release, which carries the cut rounds as its own `Cut rounds:` line (O191-2).
    """
    return round_number in cut_rounds(record) or round_number in released_cut_rounds(findings_text)


def clean_round(rows: list[list[str]], round_number: int) -> bool:
    """A completed round is clean when every row is decided and none is accepted (ADR 0021, decision 1).

    No row at all is clean: the swarm answered and nothing was accepted; so is
    a round whose rows were all rejected. A row the repair marked `fixed` keeps
    the round not clean (criterion 11).
    """
    members = round_rows(rows, round_number)
    return not any(accepted_row(row) for row in members) and not undecided(members)


def fix_r_only(rows: list[list[str]], round_number: int) -> bool:
    """Whether the round has an accepted finding and every accepted row's Origin begins `fix-r` (criterion 10)."""
    members = round_rows(rows, round_number)
    took = [row for row in members if accepted_row(row)]
    return bool(took) and all(row[3].startswith("fix-r") for row in took)


def history_rounds(record: str | None, findings_text: str) -> dict[int, list[list[str]]]:
    """Every round's rows, from the record and from every released block (criterion 13).

    The record's rows are read through `record_rows` - the reviewers' words are
    not rows; a release contributes the rows of its block, decided statuses
    included. Round numbers never repeat between record and releases (a release
    deletes the record it counted), so rows merge by their `L<n>-` ids.
    """
    merged: dict[int, list[list[str]]] = {}
    for rows in (
        record_rows(record) if record is not None else [],
        findings_rows(findings_text)[0],
    ):
        for row in rows:
            match = ROUND_ID.fullmatch(row[0])
            if match:
                merged.setdefault(int(match.group(1)), []).append(row)
    return merged


def new_state(root: Path, free: dict) -> dict:
    """The stage snapshot of a fresh run: free selection, Flash swarm, ladder rungs.

    The snapshot pins the run's membership (ADR 0021, decision 9): an edited
    YAML takes effect on fresh runs, never inside this one. The Flash stage
    exists only when it has eligible members - an empty one is skipped without
    a round (decision 5).
    """
    entry = endpoint_entry(root)
    ladder_ids = ladder(root)
    problem = flash_problem(entry)
    if problem:
        raise Refused(f"{problem}.")
    flash = [model for model in entry.get("flash_swarm") or [] if model in ladder_ids]
    return {
        "free": free,
        "paid": {
            "ladder": ladder_ids,
            "flash": flash,
            "rungs": [model for model in ladder_ids if model not in flash],
        },
        "consumed": [],
    }


def stages_of(state: dict) -> list[dict]:
    """The run's stages in order: the free swarm, the Flash swarm, one per remaining rung."""
    stages: list[dict] = []
    if state["free"]["selected"] and not state["free"].get("skipped"):
        stages.append({"key": "free", "kind": "free", "members": list(state["free"]["selected"])})
    flash = list(state["paid"]["flash"])
    if flash:
        stages.append({"key": "flash", "kind": "paid-swarm", "members": flash})
    for model in state["paid"]["rungs"]:
        stages.append({"key": f"rung:{model}", "kind": "paid", "members": [model]})
    return stages


def next_stage(state: dict) -> dict | None:
    """The first stage the run has not consumed, or None when the stages are spent."""
    consumed = set(state["consumed"])
    for stage in stages_of(state):
        if stage["key"] not in consumed:
            return stage
    return None


def write_round(change: str, block: str, state: dict, root: Path) -> None:
    """Append the round and pin its stages as consumed in one write (R-6 of the review-swarm review).

    Two writes would leave a window: a crash between them keeps a round whose stage the snapshot does
    not know, and the next call repeats the stage as a new round with new ids - extra paid calls and
    two rounds for one stage. One `write_text` closes it.
    """
    directory = record_dir(change, root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "loop.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    body = block.strip("\n")
    text = f"{text.rstrip(chr(10))}\n\n{body}\n" if text.strip() else f"{body}\n"
    line = f"{STATE_KEY}{json.dumps(state, sort_keys=True)}"
    if STATE_LINE.search(text):
        text = STATE_LINE.sub(lambda _match: line, text, count=1)
    else:
        match = ROUND_HEADING.search(text)
        text = text[: match.start()] + line + "\n\n" + text[match.start() :] if match else text + line + "\n"
    path.write_text(text, encoding="utf-8")


def mark_consumed(change: str, state: dict, key: str, root: Path) -> None:
    """Pin that the stage has completed a round: a failed attempt consumes nothing (criterion 13)."""
    state["consumed"] = [*state["consumed"], key]
    write_state(change, state, root)


def write_state(change: str, state: dict, root: Path) -> None:
    """The run's stage snapshot into the record, as the record's own line.

    The line sits before the first round heading; the runner owns it, never the
    reviewer's words. `kept_lines` leaves it out - the release carries the line
    itself, so a continued run reads its snapshot from findings.md (criterion
    13).
    """
    line = f"{STATE_KEY}{json.dumps(state, sort_keys=True)}"
    directory = record_dir(change, root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "loop.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if STATE_LINE.search(text):
            path.write_text(STATE_LINE.sub(lambda _match: line, text, count=1), encoding="utf-8")
            return
        match = ROUND_HEADING.search(text)
        if match:
            text = text[: match.start()] + line + "\n\n" + text[match.start() :]
        else:
            text = text.rstrip("\n") + "\n\n" + line + "\n"
        path.write_text(text, encoding="utf-8")
        return
    path.write_text(f"{RECORD_HEADING}{change}\n\n{RECORD_INTRO}\n{line}\n", encoding="utf-8")


def read_state(record: str | None, findings_text: str) -> dict | None:
    """The run's stage snapshot: the record's own line first, else the last release's.

    Only the runner's own lines are read - the released block is cut at
    `Kept from the loop record:`, so the reviewers' words are never a snapshot
    (criterion 13). A record without its state line predates the swarms and is
    refused instead of continued with invented stages.
    """
    line: str | None = None
    if record is not None:
        for text, reviewer in _record_lines(record):
            if reviewer:
                continue
            match = STATE_LINE.match(text)
            if match:
                line = match.group(1)
                break
        if line is None:
            raise Refused("the loop record has no Loop state line; it predates the swarms and cannot be continued.")
    else:
        start = _last_release(findings_text)
        if start >= 0:
            block = findings_text[start:]
            cut = KEPT_FROM.search(block)
            if cut:
                block = block[: cut.start()]
            match = STATE_LINE.search(block)
            if match:
                line = match.group(1)
    if line is None:
        return None
    try:
        state = json.loads(line)
    except ValueError as error:
        raise Refused(f"the run's Loop state line is not readable JSON: {error}") from None
    if (
        not isinstance(state, dict)
        or not isinstance(state.get("free"), dict)
        or not isinstance(state.get("paid"), dict)
        or not isinstance(state.get("consumed"), list)
    ):
        raise Refused("the run's Loop state line does not hold the expected stage snapshot.")
    return state


def quote_reviewer(text: str) -> str:
    """Preserve reviewer words as Markdown quotes, never as control lines."""
    return "\n".join(line if line.startswith("> ") else "> " + line for line in text.splitlines())


def rounds_run(record: str | None, findings_text: str) -> int:
    """A round is counted by its block in the record, and by every count left behind by a release."""
    in_record = len(ROUND_HEADING.findall(record)) if record else 0
    released = 0
    own = False
    for line in findings_text.splitlines():
        if line.startswith("## "):
            own = line.startswith(RELEASE_HEADING)
        elif KEPT_FROM.match(line):
            own = False
        elif own and (match := ROUNDS_LINE.fullmatch(line)):
            released += int(match.group(1))
    return in_record + released


def kept_lines(record: str) -> str:
    """Everything the record holds that the release does not carry as a row, exactly as it stands.

    Left out: the record's own furniture - its heading, its intro, the round headings, the `Loop state:` line
    (the release carries the snapshot itself, before the kept marker), the tables' header and
    separator - and the loop rows (`record_rows` has them). What is left goes to `findings.md`, because the
    record is deleted afterwards and is the only copy: the runner's own statements, and the reviewer's words
    line by line as they came, blank lines between them included (a heading or a comment that starts with `#`,
    a table line that is no row). The reviewer's words stand apart from the runner's lines by a blank line.
    """
    intro = set(RECORD_INTRO.splitlines())
    furniture = set(render_table(ROW_COLUMNS, []).splitlines())
    segments: list[tuple[bool, list[str]]] = []
    for number, (line, glm) in enumerate(_record_lines(record)):
        if not glm:
            cells = split_row(line)
            if (
                not line.strip()
                or line in intro
                or line.strip() in furniture
                or ROUND_HEADING.match(line)
                or STATE_LINE.match(line)
                or (number == 0 and line.startswith(RECORD_HEADING))
                or (cells and LOOP_ID.fullmatch(cells[0]))
            ):
                continue
        if not segments or segments[-1][0] != glm:
            segments.append((glm, []))
        segments[-1][1].append(line)
    kept = []
    for glm, lines in segments:
        while glm and lines and not lines[0].strip():
            lines.pop(0)
        while glm and lines and not lines[-1].strip():
            lines.pop()
        if lines:
            kept.append("\n".join(lines))
    return "\n\n".join(kept)


def release(root: Path, change: str) -> list[list[str]]:
    """The loop rows into findings.md, after the phase-6 verdict. Returns the rows released."""
    findings = folder_of(root, change) / "findings.md"
    text = findings.read_text(encoding="utf-8") if findings.exists() else ""
    if not VERDICT_LINE.search(text):
        near = VERDICT_START.search(text)
        if near:
            raise Refused(
                f"findings.md has a line that starts like the phase-6 verdict but does not have the form "
                f"`Phase 6 verdict: <reviewer> <session>, <date>` (<date> as YYYY-MM-DD, last on the line; `pending` is no reviewer): "
                f"`{near.group(0).strip()}`; nothing is released."
            )
        raise Refused("findings.md has no phase-6 verdict line; nothing is released.")
    record = read_record(change, root)
    if record is None:
        # The runner's own lines stand at a line start; a block's quote of either line is not one (criterion 12).
        if not (NO_LOOP.search(text) or RELEASE_LINE.search(text)):
            append(findings, NO_LOOP_LINE)
        return []
    rows = record_rows(record)
    refusal = undecided_refusal(rows, "nothing is released")
    if refusal:
        raise Refused(refusal)
    state = read_state(record, text)
    block = [f"{RELEASE_HEADING} {today()}", render_table(RELEASED_COLUMNS, [[*row, "—"] for row in rows])]
    if not rows:
        block.append("No loop row was reported.")
    block.append(f"Rounds run: {len(ROUND_HEADING.findall(record))}")
    cut = cut_rounds(record)
    if cut:
        block.append(f"Cut rounds: {', '.join(str(number) for number in cut)}")
    if state is not None:
        # The snapshot travels as the block's own line, before the kept words:
        # a continued run reads its stages from here, never from the reviewers'
        # text (criterion 13).
        block.append(f"{STATE_KEY}{json.dumps(state, sort_keys=True)}")
    kept = kept_lines(record)
    if kept:
        block.append(f"Kept from the loop record:\n\n{quote_reviewer(kept)}")
    append(findings, "\n\n".join(block))
    shutil.rmtree(record_dir(change, root))
    print(f"release-loop: {len(rows)} loop rows appended to {findings.relative_to(root)}")
    return rows


def retire_stage(root: Path, change: str, model: str, reason: str) -> None:
    """Retire the stage `model` belongs to, and let the loop continue (R-1 of the review-swarm review).

    A stage whose model keeps failing had no way out: the snapshot pins the stages, `prepare-loop`
    refuses while a record exists, `release-loop` needs the phase-6 verdict, and no verb skipped a
    stage. The only escape was deleting `loop.md` by hand. The maintainer's decision (bead
    coding-harness-tex, 2026-10-20): an explicit command retires it - the stage is consumed, the
    reason lands in the record, and every round row stays as it is.
    """
    reason = reason.strip()
    if not reason:
        raise Refused("--stage-failed needs a non-empty --reason: what the maintainer decided must be readable.")
    findings_path = folder_of(root, change) / "findings.md"
    findings_text = findings_path.read_text(encoding="utf-8") if findings_path.exists() else ""
    record = read_record(change, root)
    if record is None and not findings_text:
        raise Refused(f"there is no loop record for {change} and no released block; nothing can be retired.")
    # After `release-loop` the snapshot lives in findings.md while loop.md is gone: a continued run
    # whose next stage fails every member writes no new record, and this is exactly the run the
    # command must unblock (the review of PR #198).
    # A restarted loop has no snapshot of its own until its first round; the old run's stages are spent.
    state = None if restarted_fresh(record, findings_text) else read_state(record, findings_text)
    if state is None:
        raise Refused("the loop record carries no stage snapshot; nothing can be retired.")
    stage = next((item for item in stages_of(state) if model in item["members"]), None)
    if stage is None:
        raise Refused(
            f"no stage of this run names {model}; the stages are "
            f"{', '.join(item['key'] for item in stages_of(state)) or 'none'}."
        )
    if stage["key"] in state["consumed"]:
        raise Refused(f"the stage {stage['key']} is consumed already; nothing is retired.")
    block = "\n\n".join(
        [
            f"## Stage failed — {stage['key']} ({model})",
            quote_reviewer(reason),
            "The stage is retired by the maintainer: no round of it counts, and the loop continues with "
            "the next stage.",
        ]
    )
    # The round and the consumption in one write, as for a finished round (R-6).
    state["consumed"] = [*state["consumed"], stage["key"]]
    write_round(change, block, state, root)
    print(f"release-loop: stage {stage['key']} retired ({model}); the reason is in the loop record.")


def restart_loop(root: Path, change: str, reason: str) -> None:
    """Restart a completed loop on the maintainer's request (ADR 0021, restart amendment; bead coding-harness-0xjr).

    Decision 9 still holds for everything an agent, a release or an edited configuration could reset. Only
    this command restarts, and only with a reason: one line in findings.md, every earlier round, row,
    snapshot and release left as it stands. The next `review-loop` is a fresh run whose round numbers
    continue, so no row id repeats.
    """
    # One line: a pasted reason must not become a heading, a row or a state line (O198-1).
    reason = " ".join(reason.split())
    if not reason:
        raise Refused("--restart needs a non-empty --reason: the maintainer's request must be readable.")
    if read_record(change, root) is not None:
        raise Refused("a loop record exists; release the running loop first, after its phase-6 verdict.")
    findings_path = folder_of(root, change) / "findings.md"
    text = findings_path.read_text(encoding="utf-8") if findings_path.exists() else ""
    last = max(max(history_rounds(None, text), default=0), rounds_run(None, text))
    if not last:
        raise Refused(f"{change} has no completed loop round; a fresh review-loop needs no restart.")
    if restarted_fresh(None, text):
        raise Refused("the loop is already restarted and no round has run since; nothing is written.")
    append(findings_path, f"Loop restarted: {today()} after round {last} — {reason}")
    print(f"release-loop: the loop of {change} restarts after round {last}; the next review-loop is a fresh run.")


def release_loop(
    root: Path, change: str, stage_failed: str | None = None, reason: str | None = None, restart: bool = False
) -> None:
    if restart:
        if stage_failed is not None:
            raise Refused("--restart and --stage-failed exclude each other; nothing is written.")
        restart_loop(root, change, reason or "")
        return
    if stage_failed is not None:
        retire_stage(root, change, stage_failed, reason or "")
        return
    if reason is not None:
        raise Refused("--reason belongs to --stage-failed or --restart; nothing is released.")
    release(root, change)


def _git_output(root: Path, *args: str, allow: tuple[int, ...] = (0,), env: dict[str, str] | None = None) -> str:
    try:
        done = subprocess.run(
            [GIT, "-C", str(root), *args],
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
            env=env,
            timeout=GIT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise Refused(f"git {args[0]} did not finish within {GIT_SECONDS // 60} minutes") from error
    if done.returncode not in allow:
        raise Refused(f"git {args[0]} failed: {done.stderr.strip()[:200]}")
    return done.stdout


def change_diff(root: Path) -> str:
    """The diff against the merge base with origin/main, uncommitted and untracked files included."""
    base = _merge_base(root)
    flags = ["--no-color", "--no-ext-diff", "--no-textconv"]
    parts = [_git_output(root, "diff", *flags, base)]
    untracked = _git_output(root, "ls-files", "-z", "--others", "--exclude-standard").split("\0")
    for path in filter(None, untracked):
        parts.append(_git_output(root, "diff", *flags, "--no-index", "--", "/dev/null", path, allow=(0, 1)))
    return "".join(parts)


# ---------------------------------------------------------------------------
# GLM Flash work phases
# ---------------------------------------------------------------------------


TIME_HEADING = re.compile(r"^## Time used[ \t]*$", re.M)
WORK_READ_TOOLS = "Read,Grep,Glob"
WORK_WRITE_TOOLS = "Read,Grep,Glob,Edit,Write"

# Before `make verify` the runner formats the change's Python files itself: Claude Code work calls
# have file tools only; Codex repair attempts are command-capable workspace-write calls. Both ruff
# gates only check. Safe fixes only, never `--unsafe-fixes` (Q-1 of the spec), and the worktree's own
# ruff by a path with a slash, so `PATH` is never consulted.
RUFF = ".venv/bin/ruff"
FORMAT_DIRS = ("scripts/", "tests/")
RUFF_COMMANDS = (
    ("check", "--fix", "--no-unsafe-fixes", "--force-exclude", "--no-cache"),
    ("format", "--force-exclude", "--no-cache"),
)
FORMAT_LABEL = "Runner format before `make verify`"
FORMAT_COMMIT_HEADING = "Runner format before `make verify` (ruff check --fix with safe fixes only, then ruff format):"


# The runner's own steps are bounded, and every program it starts from the worktree is the one it saw
# before the model ran: a step that hangs, and a tool the attempt overwrote, both abort the attempt
# with the limit or the path named - never a silent cut, never a wait without end (R-19, R-20 and
# R-21 of the review-swarm review).
# The one executable the runner resolves through `PATH`, and only once: every call names this path
# (R-17 of the review-swarm review). A poisoned `PATH` after start cannot swap it.
def resolve_git() -> str:
    """The `git` that `PATH` names now, or the bare name when there is none."""
    return shutil.which("git") or "git"


GIT = resolve_git()


def refuse_repository_git(root: Path) -> None:
    """Refuse a run whose resolved `git` lies inside the repository: an attempt could have written it (O192-3).

    Checked where a run starts. A bare name (no `git` on `PATH`) is not a path under the root and
    fails at the first call instead. Follow-up: once `runner_env` (PR #188) filters `PATH`, resolve
    through that filtered `PATH`.
    """
    program = Path(GIT)
    if not program.is_absolute():
        return
    try:
        resolved = program.resolve()
        inside = resolved.is_relative_to(root.resolve())
    except (OSError, RuntimeError):
        inside = True  # an unmeasurable path is not trusted
    if inside:
        raise Refused(
            f"`git` resolves to {GIT}, inside the repository; the runner starts no program the checkout holds. "
            "Take that directory off PATH and start the run again."
        )


TOOL_SECONDS = 5 * 60
VERIFY_SECONDS = 30 * 60
GIT_SECONDS = 2 * 60


UNREADABLE = "unreadable"  # the digest entry for a file or directory tool_state cannot inspect


def tool_state(root: Path) -> dict[str, str]:
    """The digest of the worktree's `.venv/` tree, taken before the model runs (R-21).

    `.venv/` is ignored by git: a file there is invisible to `changed_paths` and survives
    `restore_baseline`, so this digest is the only thing that shows an overwritten tool, a planted
    `*.pth` file or a replaced package. Every file maps to the SHA-256 of its bytes and every symlink
    to its target; the runner's steps run with the interpreter, ruff and packages of this tree.
    """
    state: dict[str, str] = {}
    venv = root / ".venv"
    try:
        info = venv.lstat()
        if stat.S_ISLNK(info.st_mode):
            # Record the root link AND digest its tools: an unchanged link must not hide
            # overwritten target bytes. os.walk traverses its root even with followlinks=False;
            # nested directory links remain opaque, and _unlink_cache still rejects this root.
            state[".venv"] = "link:" + str(venv.readlink())
    except FileNotFoundError:
        return state
    except OSError:
        return {".venv": UNREADABLE}

    def unreadable_directory(error: OSError) -> None:
        # os.walk otherwise silently skips failed scandir calls, hiding newly planted caches.
        path = Path(error.filename) if error.filename is not None else venv
        state[path.relative_to(root).as_posix()] = UNREADABLE

    for directory, names, files in os.walk(venv, onerror=unreadable_directory):
        for name in sorted([*names, *files]):
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            try:
                if path.is_symlink():
                    state[relative] = "link:" + str(path.readlink())
                elif path.is_file():
                    state[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                state[relative] = UNREADABLE
    return state


def _is_cache_path(relative: str) -> bool:
    """True for a worktree-relative path below an exact `__pycache__` component inside `.venv/`.

    The component must lie strictly between `.venv/` and the file itself, so a file named
    `__pycache__` is not its own cache directory. The suffix is irrelevant: the import machinery
    names `.pyc` today, and pytest's assertion rewriting may not tomorrow.
    """
    parts = relative.split("/")
    return len(parts) > 2 and parts[0] == ".venv" and "__pycache__" in parts[1:-1]


def _unlink_cache(root: Path, relative: str) -> bool | None:
    """Unlink one cache candidate, reached only through real directories; say what happened.

    Every component from `.venv/` down is checked with `lstat`, rejecting a linked root, parent,
    cache directory or file in the inspected tree (spec criterion 6). This is a check-then-act
    sequence: a concurrent directory replacement between inspection and `unlink` could redirect
    deletion outside the tree. It assumes no concurrent filesystem writer; it does not provide
    race-safe no-follow deletion. Returns `True` when the file was unlinked, `False` when an eligible
    regular file could not be deleted, and `None` when the path is not a deletable cache file - a symlink, a
    directory, or already gone - which stays an ordinary difference for the refusal.
    """
    parts = relative.split("/")
    path = root
    try:
        for index, part in enumerate(parts):
            path = path / part
            info = path.lstat()
            if index == len(parts) - 1:
                if not stat.S_ISREG(info.st_mode):
                    return None
            elif not stat.S_ISDIR(info.st_mode):
                return None
    except OSError:
        return None  # a component that cannot be stat-ed is not a proven cache file
    try:
        path.unlink()
    except OSError:
        return False
    return True


def tool_problem(root: Path, before: dict[str, str] | None) -> str | None:
    """The first path of `.venv/` that is not what the runner saw before the call, named; `None` when none is.

    A new or content-changed regular file below an exact `__pycache__` component inside `.venv/` is
    deleted before any runner-owned step: pytest's assertion rewriting writes bytecode there during
    an attempt, and a deleted cache is rebuilt, so that write is normalized instead of refused (bead
    coding-harness-q94b). Every other difference keeps the refusal with the first path named. The
    baseline bookkeeping stays narrow: each successful unlink immediately removes that path's old
    entry from the shared `before` dictionary, even if a later check fails. This records only the
    runner's own deletions. Nothing that survives is rebaselined; recreated caches are deleted again.
    """
    if before is None:
        return None

    def differences(now: dict[str, str]) -> list[str]:
        return sorted(path for path in before.keys() | now.keys() if before.get(path) != now.get(path))

    now = tool_state(root)
    cleaned = False
    for path in sorted(before.keys() | now.keys()):
        if UNREADABLE in (before.get(path), now.get(path)):
            return f"`{path}` cannot be inspected, and a tool the attempt wrote is not run"
        if not _is_cache_path(path):
            continue  # retain the difference, but still clean eligible caches that sort later
        if before.get(path) == now.get(path):
            continue
        if before.get(path, "").startswith("link:"):
            continue  # removing a baseline symlink is never a cache-byte change
        deleted = _unlink_cache(root, path)
        if deleted is None:
            continue  # a linked or non-regular cache-looking path stays a difference
        if not deleted:
            return f"`{path}` cannot be deleted, and a tool the attempt wrote is not run"
        before.pop(path, None)  # record each runner-owned deletion even if a later check fails
        cleaned = True
    if cleaned:
        now = tool_state(root)  # the tree changed through the runner's own deletions
    if now == before:
        return None
    changed = differences(now)
    return f"`{changed[0]}` is not what the runner saw before the call, and a tool the attempt wrote is not run"


def runner_env(env: dict[str, str], *roots: Path) -> dict[str, str]:
    """The environment of the runner's own steps: no `PATH` entry inside the repository, no bytecode written.

    A directory inside the worktree is attempt-writable, so a `git` or `make` planted there would
    run before the real one; a relative entry resolves against the worktree and is dropped too.
    """
    resolved = [root.resolve() for root in roots]

    def inside(entry: str) -> bool:
        if not entry or not Path(entry).is_absolute():
            return True
        place = Path(entry).resolve()
        return any(place == root or root in place.parents for root in resolved)

    kept = [entry for entry in env.get("PATH", "").split(os.pathsep) if not inside(entry)] or ["/usr/bin", "/bin"]
    return {**env, "PATH": os.pathsep.join(kept), "PYTHONDONTWRITEBYTECODE": "1"}


def changed_paths(root: Path, env: dict[str, str] | None = None, against: str = "HEAD") -> set[Path]:
    """Tracked changes against `against` and untracked files, as repository-relative paths."""
    # `--no-renames`: a rename must list both names, or the deleted one is invisible (O192-1).
    tracked = _git_output(root, "diff", "--no-renames", "--name-only", "-z", against, env=env).split("\0")
    untracked = _git_output(root, "ls-files", "-z", "--others", "--exclude-standard", env=env).split("\0")
    return {Path(name) for name in [*tracked, *untracked] if name}


def ignored_snapshot(root: Path) -> dict[Path, tuple[int, int]]:
    """Gitignored files with their mtime and size, so a later scan can tell which the run touched.

    `.venv/` is included: the gate runs repository code that can write into it. Only entries whose
    (mtime, size) differ from this snapshot are scanned, so installed third-party files are
    stat-ed, never read or rewritten. Measured 2026-10-07: about 1,700 ignored files, 0.06 s.
    """
    listing = _git_output(root, "ls-files", "-z", "--others", "--ignored", "--exclude-standard", "--", ".").split("\0")
    snapshot = {}
    for name in filter(None, listing):
        try:
            info = (root / name).lstat()
        except OSError:
            continue
        snapshot[Path(name)] = (info.st_mtime_ns, info.st_size)
    return snapshot


SAVE_IDENTITY = {
    "GIT_AUTHOR_NAME": "stage2 runner",
    "GIT_AUTHOR_EMAIL": "stage2@localhost",
    "GIT_COMMITTER_NAME": "stage2 runner",
    "GIT_COMMITTER_EMAIL": "stage2@localhost",
}


def save_attempt(root: Path, baseline: str, change: str, label: str) -> str:
    """Save the worktree as it stands after a failed call on a local ref; say where, or why not.

    A failed call is not a worthless one: a run that hits a spent budget after hours of edits still
    holds them (bead coding-harness-znc). The snapshot goes through a temporary index, so the real
    index and the files stay untouched; tracked and untracked files go in, gitignored ones do not.
    The temporary index is seeded with the baseline, as in `worktree_tree`, so a file tracked although
    ignored stays in the snapshot. The commit's parent is the baseline, so `git diff <baseline> <ref>`
    shows everything the run left in the tree: this attempt, any earlier attempt of the run whose tree
    it started on, and the runner's own writes. The ref lives under `refs/stage2/attempts/`, which no
    branch push carries. A save that fails is named and never blocks the restore that follows.
    The commit carries the runner's own identity, so a machine without a configured git user (a CI
    runner) saves as well, and the ref says who wrote it.
    """
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S%fZ")
    ref = f"refs/stage2/attempts/{change}/{label}-{stamp}"
    with tempfile.TemporaryDirectory(prefix="stage2-save-") as scratch:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(scratch) / "index"), **SAVE_IDENTITY}
        try:
            _git_output(root, "read-tree", baseline, env=env)
            _git_output(root, "add", "-A", "--", ".", env=env)
            tree = _git_output(root, "write-tree", env=env).strip()
            commit = _git_output(
                root, "commit-tree", tree, "-p", baseline, "-m", f"stage2: saved {label} of {change}", env=env
            ).strip()
            _git_output(root, "update-ref", ref, commit)
        except (Refused, OSError) as error:
            return f"saving the attempt failed ({error})"
    return f"the attempt is saved at {ref} ({commit[:12]}); `git diff {baseline[:12]} {ref}` shows it"


def restore_baseline(
    root: Path, baseline: str, keep: set[Path], ignored_before: dict[Path, tuple[int, int]] | None = None
) -> str:
    """After a failed model call, put every path but `keep` back at the baseline; say what was undone.

    The runner refused pre-existing changes outside `keep` before the first call, so what differs
    from the baseline outside it is the run's own - including a half-finished edit of a dead process.
    Gitignored paths the attempt created are removed too: `changed_paths` cannot see them and
    `git clean` without `-x` keeps them, so the run's earlier snapshot of the ignored files tells them
    apart from the ones that stood before (phase 6, F-5).
    """
    touched = sorted(path.as_posix() for path in changed_paths(root) - keep)
    created = sorted(ignored_snapshot(root).keys() - ignored_before.keys()) if ignored_before is not None else []
    if not touched and not created:
        return "the worktree needed no restore."
    spec = [f":(exclude){path.as_posix()}" for path in sorted(keep, key=lambda path: path.as_posix())]
    try:
        _git_output(root, "restore", f"--source={baseline}", "--staged", "--worktree", "--", ".", *spec)
        _git_output(root, "clean", "-fdq", "--", ".", *spec)
    except Refused as error:
        listing = ", ".join([*touched, *(path.as_posix() for path in created)])
        return f"restoring the worktree to {baseline[:12]} failed ({error}); discard {listing} by hand."
    removed = []
    for relative in created:
        path = root / relative
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
        except OSError:
            continue
        removed.append(relative.as_posix())
        parent = path.parent
        while parent not in (root, parent.parent):
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent
    undone = f"undone: {', '.join(touched)}" if touched else ""
    ignored = f"ignored paths removed: {', '.join(removed)}" if removed else ""
    inner = "; ".join(part for part in (undone, ignored) if part)
    return f"the runner restored the worktree to {baseline[:12]} ({inner}); rerun the verb or add --stage2-off."


def time_log(path: Path) -> str:
    """The bytes below `## Time used` and before the next level-two heading."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise Refused(f"{path} cannot be read.") from error
    match = TIME_HEADING.search(text)
    if match is None:
        raise Refused(f"{path} has no `## Time used` heading.")
    following = re.search(r"^## [^#]", text[match.end() :], re.M)
    end = match.end() + following.start() if following else len(text)
    return text[match.end() : end]


def utc_now() -> dt.datetime:
    """The wall clock of a measured span, in UTC (a seam for tests)."""
    return dt.datetime.now(dt.UTC)


def monotonic_now() -> float:
    """The monotonic clock whose difference is a measured span (a seam for tests)."""
    return time.monotonic()


def time_entry(
    verb: str,
    attempt: int,
    route: str,
    model: str,
    accepted: bool,
    started: dt.datetime,
    ended: dt.datetime,
    seconds: int,
) -> str:
    """The line the runner writes under `## Time used` for one completed attempt.

    The elapsed span is the monotonic difference; the UTC endpoints only name it, and the end carries
    its date when that differs from the start's, so a span across midnight reads unambiguously.
    """
    end_date = f"{ended:%Y-%m-%d} " if ended.date() != started.date() else ""
    result = "accepted" if accepted else "rejected"
    return (
        f"{started:%Y-%m-%d} {started:%H:%M:%S}–{end_date}{ended:%H:%M:%S} UTC, {seconds} s — "
        f"{verb} · attempt {attempt} · route {route} · model {model} · {result} · measured by the runner"
    )


def with_time_entry(text: str, entry: str, *, prior: str | None = None) -> str:
    """`text` with `entry` as the last line of the time section, before the next level-two heading."""
    match = TIME_HEADING.search(text)
    if match is None:
        raise Refused("the plan has no `## Time used` heading.")
    following = re.search(r"^## [^#]", text[match.end() :], re.M)
    end = match.end() + following.start() if following else len(text)
    body = text[match.end() : end]
    if prior is not None:
        # Time records are runner-owned: keep the pre-call section even when the model rewrites it.
        previous = TIME_HEADING.search(prior)
        if previous is None:
            raise Refused("the pre-call plan has no `## Time used` heading.")
        next_heading = re.search(r"^## [^#]", prior[previous.end() :], re.M)
        previous_end = previous.end() + next_heading.start() if next_heading else len(prior)
        body = prior[previous.end() : previous_end]
    body = body.rstrip() or "\n"
    tail = text[end:]
    return text[: match.end()] + body + "\n" + entry + "\n" + (f"\n{tail}" if tail else "")


def insert_before_time(path: Path, block: str) -> None:
    """Put runner routing evidence before the time section, so it cannot satisfy the time check."""
    text = path.read_text(encoding="utf-8")
    match = TIME_HEADING.search(text)
    if match is None:
        # An earlier attempt deleted the heading; the route block must still land, and the
        # restored empty heading keeps the measured-line check meaningful for this attempt.
        path.write_text(f"{text.rstrip()}\n\n{block.rstrip()}\n\n## Time used\n", encoding="utf-8")
        stamp_updated(path)
        return
    before = text[: match.start()].rstrip()
    after = text[match.start() :].lstrip("\n")
    path.write_text(f"{before}\n\n{block.rstrip()}\n\n{after}", encoding="utf-8")
    stamp_updated(path)


def run_work_model(
    ctx: Context,
    prompt: str,
    endpoint: tuple[str, str, str | None],
    writable: bool,
    key: str | None = None,
) -> str:
    """One non-interactive Claude Code work call with file tools only."""
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        prompt_file = Path(tmp) / "work-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        command = [
            "claude",
            "-p",
            f"Run the phase for {ctx.change} exactly as the appended instructions say.",
            "--append-system-prompt-file",
            str(prompt_file),
            "--model",
            endpoint[1],
        ]
        if endpoint[2]:
            command += ["--effort", endpoint[2]]
        command += [
            "--tools",
            WORK_WRITE_TOOLS if writable else WORK_READ_TOOLS,
            "--restricted",
            "--safe-mode",
            "--strict-mcp-config",
            "--permission-mode",
            "acceptEdits" if writable else "dontAsk",
            "--permission-prompts",
            "none",
            "--no-session-persistence",
            "--output-format",
            "text",
        ]
        if key is None:
            env = foreign_env({})
        else:
            config_dir = Path(tmp) / "claude-config"
            config_dir.mkdir()
            env = glm_env(key, config_dir, endpoint[1])
        done = launch(command, ctx.root, env, key)
    if done.returncode != 0:
        raise fail("claude", done, f"exit {done.returncode}", key)
    answer = scrub(done.stdout or "", key)
    if not answer.strip():
        raise fail("claude", done, "the answer is empty", key)
    return answer


def remove_changed_credential(
    root: Path,
    key: str,
    ignored_before: dict[Path, tuple[int, int]] | None = None,
    against: str = "HEAD",
) -> list[Path]:
    """Remove an exact GLM credential from changed regular files and name those files.

    "Changed" is tracked changes, untracked files, and - when the run's earlier snapshot of the
    gitignored files is given - every ignored file created or touched since that snapshot. The
    comparison is `against`, not always HEAD: a draft passes its baseline, because files a model
    committed read as clean against its own new HEAD and must still be found (spec, criterion 25;
    2a's F-4).
    """
    paths = changed_paths(root, against=against)
    if ignored_before is not None:
        paths |= {p for p, stat in ignored_snapshot(root).items() if ignored_before.get(p) != stat}
    found = []
    for relative in sorted(paths, key=lambda path: path.as_posix()):
        path = root / relative
        if path.is_symlink() or not path.is_file():
            continue
        try:
            content = path.read_bytes()
        except OSError:
            continue
        if not credential_spans(content, key):
            continue
        path.write_bytes(replace_credential(content, key))
        found.append(relative)
    return found


def credential_message(exposed: list[Path]) -> str:
    listing = ", ".join(path.as_posix() for path in exposed)
    return f"the GLM credential occurred in changed files and was removed ({listing}); no fallback starts."


def worktree_tree(root: Path) -> str:
    """The tree id of the worktree as git counts it, written through a temporary index.

    The temporary index is seeded with `git read-tree HEAD`, not copied from the real one: a file
    tracked although ignored stays in the snapshot, and the real index, the stash and the refs are
    never touched (spec, criterion 10).
    """
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        _git_output(root, "read-tree", "HEAD", env=env)
        _git_output(root, "add", "-A", env=env)
        return _git_output(root, "write-tree", env=env).strip()


def attempt_files(root: Path, before: str, after: str) -> list[str]:
    """The files between two trees, as `git diff-tree --numstat` counts them, bounded at `ATTEMPT_FILES`.

    One entry is `` `<path>` +<added> -<removed> ``, or `` `<path>` binary `` where git counts none.
    With more entries than the bound, the first ones stand and one line says how many follow
    (spec, criterion 14). `-z` keeps paths with newlines or tabs whole; the path is the record's last field.
    """
    done = _git_output(root, "diff-tree", "-r", "-z", "--numstat", "--no-renames", before, after)
    entries = []
    for record in filter(None, done.split("\0")):
        fields = record.split("\t", 2)
        if len(fields) != 3:
            raise Refused(f"git diff-tree --numstat returned a record without two counts: {record!r}")
        added, removed, relative = fields
        entries.append(f"`{relative}` binary" if added == "-" else f"`{relative}` +{added} -{removed}")
    if len(entries) > ATTEMPT_FILES:
        entries = entries[:ATTEMPT_FILES] + [f"… and {len(entries) - ATTEMPT_FILES} more files"]
    return entries


def put_back_lines(paths: list[str]) -> list[str]:
    """The put-back list lines: every path in backticks, without a bound.

    The record of what the runner put back is the audit's only way to name each restored path, so
    no remainder line may hide one (spec, criterion 8; 2a's F-8 replaces the bound of loop row
    L2-5).
    """
    return [f"- `{path}`" for path in paths]


def attempt_block(attempt: int, route: str, listing: str, files: list[str] | str, *, moved_head: bool = False) -> str:
    """The unquoted text of one failed attempt's block: its header, the files, the diagnostics.

    `files` is the entry list of `attempt_files`, a reason string when the trees could not be measured,
    or empty when the attempt's model changed no file. The diagnostics stand in a fenced code block
    whose fence is one backtick longer than the longest run they contain, at least three, so gate
    output with fences of its own is quoted whole (spec: the block's shape). A moved-HEAD stop
    precedes all post-run checks, so its header must not claim those checks failed.
    """
    head = (
        f"Attempt {attempt} ({route}) stopped because the call moved HEAD; no post-run check ran."
        if moved_head
        else f"Attempt {attempt} ({route}) failed its post-run checks."
    )
    if isinstance(files, str):
        # The reason is a raw git error: one line, and one full stop of this sentence's own.
        reason = " ".join(files.split()).rstrip(".")
        file_part = f"Files the attempt changed: not measured — {reason}."
    elif files:
        file_part = "Files the attempt changed (lines added, removed):\n" + "\n".join(f"- {entry}" for entry in files)
    else:
        file_part = "Files the attempt changed: none."
    longest = max((len(run) for run in re.findall(r"`+", listing)), default=2)
    fence = "`" * max(longest + 1, 3)
    return f"{head}\n\n{file_part}\n\nDiagnostics:\n{fence}text\n{listing}\n{fence}"


def quote_block(text: str, key: str | None, whole: tuple[str, ...] | list[str] = ()) -> str:
    """`text` as one Markdown quote: every line begins `>`, the key scrubbed, long lines cut.

    One mark on every line defeats the line-anchored readers of findings.md at once (spec, criterion 11).
    A line longer than `QUOTE_LINE_CHARS` keeps its first characters and says how many were left out
    (criterion 13). A line that is one of `whole` is never cut: the put-back list names each path in
    full, and a cut would turn two long paths into one line (spec, criterion 8; phase-6 F-12). Under
    `--stage2-off` the key is `None` and nothing is scrubbed: that run never reads it.
    """
    lines = []
    # An entry may itself hold line breaks (a path can): every line it splits into stays uncut (F-15).
    uncut = {part for line in whole for part in scrub(line, key).splitlines()}
    for line in scrub(text, key).splitlines():
        if len(line) > QUOTE_LINE_CHARS and line not in uncut:
            line = f"{line[:QUOTE_LINE_CHARS]} [… {len(line) - QUOTE_LINE_CHARS} characters left out …]"
        lines.append(f"> {line}" if line else ">")
    return scrub("\n".join(lines), key)


RED_SECTION_LINES = 60
RED_TOTAL_LINES = 200
TAIL_LINES = 80
GATE_START = re.compile(r"^── \[(?P<gate>[^\]]+)\] \$ ")
# Any frame line of the open gate that is not a start ends it, whatever its verdict is spelled (loop row L2-1).
GATE_END = re.compile(r"^── \[(?P<gate>[^\]]+)\] (?!\$ )(?P<verdict>.+)")
STDERR_LINES = 40


def _frame_lines(output: str) -> list[str]:
    """The output's lines, with a frame split off a line it was printed onto (phase 6, F-3).

    `verify_all.sh` echoes a gate's closing frame right after the gate's output; when that output ends without
    a newline, the frame lands on the same line.
    """
    found: list[str] = []
    for line in output.splitlines():
        cut = line.rfind("── [")
        if cut > 0 and (GATE_START.match(line[cut:]) or GATE_END.match(line[cut:])):
            found += [line[:cut], line[cut:]]
        else:
            found.append(line)
    return found


def _shrink(body: list[str], limit: int) -> list[str]:
    """A section of at most `limit` lines, marker included: its start frame, the marker, its last lines."""
    if len(body) <= limit:
        return body
    return [body[0], f"[… {len(body) - limit + 1} lines of this gate left out …]", *body[-(limit - 2) :]]


def red_sections(output: str) -> str | None:
    """The sections of the gates `verify_all.sh` framed `RED (block)`, bounded, in run order - or None.

    A repair attempt needs the gate that blocked. The log's tail is the report-only gates (docs-links,
    markdownlint), thousands of lines after a pytest failure (bead coding-harness-zci). The red gates share
    the budget: each keeps its start frame, its last lines and its RED line, markers count against the bounds
    (phase 6, F-1 and F-2).
    """
    lines = _frame_lines(output)
    # The gates run one after another: a frame line counts only as the open gate's end or, with none open, as
    # the next gate's start - a frame quoted inside a gate's own output opens or closes nothing.
    open_gate: tuple[str, int] | None = None
    sections: list[list[str]] = []
    for index, line in enumerate(lines):
        if open_gate is None:
            start = GATE_START.match(line)
            if start:
                open_gate = (start["gate"], index)
            continue
        end = GATE_END.match(line)
        if not end or end["gate"] != open_gate[0]:
            continue
        begin, open_gate = open_gate[1], None
        if end["verdict"].startswith("RED (block)"):
            sections.append(lines[begin : index + 1])
    if not sections:
        return None
    room = RED_TOTAL_LINES
    if len(sections) * 3 > room:
        # More red gates than three lines each can hold: the first ones, and one line saying how many follow.
        shown = (room - 1) // 3
        dropped = len(sections) - shown
        sections, room = sections[:shown], room - 1
    else:
        dropped = 0
    share = min(RED_SECTION_LINES, room // len(sections))
    kept = [line for body in sections for line in _shrink(body, share)]
    if dropped:
        kept.append(f"[… {dropped} more red gate sections left out …]")
    return "\n".join(kept)


def trusted_registry(root: Path, env: dict[str, str]) -> Path:
    """A scratch mirror of the worktree whose `scripts/` is the committed one (R-19).

    `plans_registry.py` reads its repository root from its own path, so the committed code cannot
    simply run somewhere else. Every other entry of the worktree is linked into the mirror and its
    `scripts/` comes from `HEAD`, so the renderer's code is the committed one while the data it
    renders stays the attempt's. The caller removes the mirror.

    This removes one execution path, not all of them (R-19). `make verify` still runs next, from the
    attempt's own tree: its Makefile, `scripts/verify_all.sh`, `conftest.py` and tests are all
    attempt-editable, and they run outside any sandbox with the caller's real `HOME`, `PATH` and
    `TMPDIR`. A payload moved from the renderer into a test therefore still runs. The scratch `HOME`
    and `TMPDIR` below bound the renderer only; they are not a boundary around the attempt's code.
    The residual risk is accepted, not removed: the attempt is a model the runner started itself.
    """
    mirror = Path(tempfile.mkdtemp(prefix="harness-registry-"))
    try:
        for entry in root.iterdir():
            if entry.name != "scripts":
                (mirror / entry.name).symlink_to(entry.resolve())
        try:
            archive = subprocess.run(
                [GIT, "-C", str(root), "archive", "--format=tar", "HEAD", "scripts/"],
                capture_output=True,
                check=False,
                env=env,
                timeout=GIT_SECONDS,
            )
        except subprocess.TimeoutExpired as error:
            # The runner's own bound, turned into a diagnostic: an escaping TimeoutExpired would end the
            # run as a traceback and leave the mirror behind (P2 of the #188 review).
            raise Refused(f"the committed scripts could not be read within {GIT_SECONDS // 60} minutes") from error
        if archive.returncode:
            raise Refused(f"the committed scripts could not be read: git archive exited {archive.returncode}")
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
            for member in tar.getmembers():
                if not member.isfile() or not member.name.startswith("scripts/"):
                    continue
                relative = Path(member.name).relative_to("scripts")
                if ".." in relative.parts:
                    continue
                target = mirror / "scripts" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(tar.extractfile(member).read())
    except BaseException:
        shutil.rmtree(mirror, ignore_errors=True)
        raise
    return mirror


def prepare_derived(root: Path, env: dict[str, str], key: str | None = None) -> list[str]:
    """Stamp only changed, held documents, then render the index before verification.

    Clean documents are not an implementation's repair surface. The existing stamp leaves
    duplicate or absent headers alone, so the verifier still reports those structural errors.
    Before emitting diagnostics, read the active denylist and raise Refused fail-closed if
    protection refuses, on every route including keyless routes (key=None).
    """
    try:
        paths, excluded = check_frontmatter_current.load_map(root)
        if any(not isinstance(entry, dict) or not isinstance(entry.get("prefix"), str) for entry in paths):
            raise check_frontmatter_current.CannotMeasure("provenance paths must be mappings with string prefixes")
        errors = []
        for relative in sorted(changed_paths(root, env=env)):
            if not check_frontmatter_current.is_held(relative.as_posix(), paths, excluded):
                continue
            path = root / relative
            try:
                if not path.resolve().is_relative_to(root.resolve()):
                    raise OSError("refusing a document outside the worktree")
                if path.resolve() != root.resolve() / relative:
                    raise OSError("refusing an aliased document path")
                if path.is_file():
                    if path.stat().st_nlink > 1:
                        raise OSError("refusing a hard-linked document path")
                    check_frontmatter_current.stamp(path, dt.date.today())
            except (check_frontmatter_current.CannotStamp, OSError, RuntimeError) as error:
                errors.append(f"{relative}: {error}")
        if not errors:
            index = root / "plans" / "INDEX.md"
            if not index.resolve().is_relative_to(root.resolve()):
                raise OSError("refusing an index outside the worktree: plans/INDEX.md")
            if index.resolve() != root.resolve() / "plans" / "INDEX.md":
                raise OSError("refusing an aliased index path: plans/INDEX.md")
            if index.exists() and index.stat().st_nlink > 1:
                raise OSError("refusing a hard-linked index path: plans/INDEX.md")
            mirror = trusted_registry(root, env)
            # Outside the mirror, and outside anything the worktree mirrors: the mirror links every top-level
            # entry, so a repository path named `scratch` would be written to instead (P2 of the #188 review).
            scratch = Path(tempfile.mkdtemp(prefix="harness-scratch-"))
            for name in ("home", "tmp"):
                (scratch / name).mkdir()
            try:
                done = launch(
                    [sys.executable, str(mirror / "scripts" / "plans_registry.py"), "--index"],
                    root,
                    {**env, "HOME": str(scratch / "home"), "TMPDIR": str(scratch / "tmp")},
                    key,
                    timeout=TOOL_SECONDS,
                    limit=f"the runner's tool limit after {TOOL_SECONDS // 60} minutes",
                )
            finally:
                shutil.rmtree(mirror, ignore_errors=True)
                shutil.rmtree(scratch, ignore_errors=True)
    except (
        check_frontmatter_current.CannotMeasure,
        check_frontmatter_current.CannotStamp,
        OSError,
        CallFailed,
        Refused,
        RuntimeError,
        UnicodeError,
    ) as error:
        evidence = "\n".join(protect_diagnostics(str(error), key).splitlines()[-TAIL_LINES:])
        return [f"Derived-file preparation failed: {evidence}"]
    if errors:
        evidence = "\n".join(_shrink(protect_diagnostics("\n".join(errors), key).splitlines(), TAIL_LINES))
        return [f"Derived-file preparation failed: {evidence}"]
    if done.returncode:
        text = protect_diagnostics((done.stdout or "") + (done.stderr or ""), key)
        evidence = "\n".join(text.splitlines()[-TAIL_LINES:])
        return [f"Derived-file preparation failed: index renderer exited {done.returncode}\n{evidence}"]
    return []


def verify_evidence(done: subprocess.CompletedProcess, key: str | None) -> str:
    """The bounded evidence of a red `make verify`: the framed gates that blocked, else the run's tail.

    Read the active denylist at diagnostic emission time and raise Refused fail-closed if
    protection refuses, on every route including keyless routes (key=None). The complete
    concatenated streams are checked before reduction; their mapped boundary retains framing.
    """
    # Protected whole, before any reduction: a cut must not split a multiline match and leave a part of it.
    raw_stdout = done.stdout or ""
    output, boundary = _protect_diagnostics(raw_stdout + (done.stderr or ""), key, len(raw_stdout))
    stdout, stderr = output[:boundary], output[boundary:]
    # verify_all.sh frames gates on standard output; a gate's standard error arrives unframed after them.
    red = red_sections(stdout)
    if red is None:
        return scrub("\n".join(output.splitlines()[-TAIL_LINES:]), key)
    evidence = "The gates that blocked, each with its last lines:\n" + red
    errors = stderr.splitlines()
    if errors:
        # Unframed: the last lines of the whole run's standard error, not of the blocking gate alone.
        cut = len(errors) - STDERR_LINES
        kept = ([f"[… {cut} earlier lines left out …]"] if cut > 0 else []) + errors[-STDERR_LINES:]
        evidence += "\n\nStandard error of the whole run, last lines:\n" + "\n".join(kept)
    return scrub(evidence, key)


def format_targets(root: Path, env: dict[str, str]) -> list[str]:
    """The change's Python files under `scripts/` and `tests/` that the format step may rewrite.

    Targets are the changes against HEAD - what the checkpoint commits and the gates measure - not
    one attempt's file list; formatting is idempotent, so a file an earlier attempt formatted stays
    as it is. A link is left out (ruff would write through it, out of the worktree), so is a
    hard-linked file, and a path that cannot be stated (`OSError`); the gates name whatever then
    stays unformatted.
    """
    targets: list[str] = []
    for relative in changed_paths(root, env=env):
        posix = relative.as_posix()
        if not posix.endswith(".py") or not posix.startswith(FORMAT_DIRS):
            continue
        path = root / relative
        try:
            if path.is_symlink() or not path.is_file():
                continue
            if path.resolve() != root.resolve() / relative or path.stat().st_nlink != 1:
                continue
        except OSError:
            continue
        targets.append(posix)
    return sorted(targets)


def _not_run(reason: str, key: str | None) -> str:
    """The format line of a step that did not run: the reason on one line, one full stop of its own."""
    return protect_diagnostics(f"not run — {' '.join(reason.split()).rstrip('.')}.", key)


# Every character a path can hold and still break the line the format line lands in - the block's
# first entry, the checkpoint commit message; `str.splitlines` splits on all of these. Each maps to
# its written escape, so a path holding one keeps the format line one line.
_LINE_BREAK_ESCAPES = {
    "\n": "\\n",
    "\r": "\\r",
    "\v": "\\v",
    "\f": "\\f",
    "\x1c": "\\x1c",
    "\x1d": "\\x1d",
    "\x1e": "\\x1e",
    "\x85": "\\x85",
    chr(0x2028): "\\u2028",
    chr(0x2029): "\\u2029",
}


def _one_line(path: str) -> str:
    """A target path with its line breaks written as escapes, so the format line stays one line."""
    return "".join(_LINE_BREAK_ESCAPES.get(character, character) for character in path)


def format_step(
    root: Path, env: dict[str, str], key: str | None = None, tools: dict[str, str] | None = None
) -> str | None:
    """Ruff's safe fixes, then its formatter, over the targets - and what that changed, in one line.

    `None` without targets: no ruff process starts. A ruff that cannot start, a command that ends
    non-zero another way, findings without a safe fix or a file that does not parse - the line says
    so, and the attempt passes or fails exactly as `make verify` and the time check decide. What
    the step changed is measured by comparing each target's bytes around it, not out of ruff's
    output; a launch failure of either command makes the whole line `not run`, for the binary that
    cannot start for one cannot start for the other. A target that cannot be read is named by its
    repository path, never by the absolute one its `OSError` would carry. A target whose name holds
    a line break is written with that break escaped - the line stays one line, while ruff still gets
    the path as it is.
    """
    try:
        targets = format_targets(root, env)
    except (Refused, OSError) as error:
        return _not_run(str(error), key)
    if not targets:
        return None
    if not (root / RUFF).is_file():
        return protect_diagnostics(f"not run — no ruff at `{RUFF}`; `make venv` builds it.", key)
    problem = tool_problem(root, tools)
    if problem:
        return protect_diagnostics(f"not run — {problem}.", key)
    before: dict[str, bytes] = {}
    for target in targets:
        try:
            before[target] = (root / target).read_bytes()
        except OSError:
            # The reason names the target by its repository path; the raw error text would carry the
            # machine's absolute one into the block and the checkpoint commit message.
            return _not_run(f"cannot read `{target}`", key)
    notes: list[str] = []
    for command in RUFF_COMMANDS:
        try:
            done = launch(
                [RUFF, *command, *targets],
                root,
                env,
                key,
                timeout=TOOL_SECONDS,
                limit=f"the runner's tool limit after {TOOL_SECONDS // 60} minutes",
            )
        except CallFailed as error:
            return _not_run(str(error), key)
        if done.returncode == 1 and command[0] == "check":
            # Exit 1 also covers a target that does not parse, and the exit code alone does not say
            # which of the two it left, so the note names both.
            notes.append("ruff check left findings without a safe fix or a file that does not parse")
        elif done.returncode:
            notes.append(f"ruff {command[0]} exited {done.returncode}")
    changed = []
    for target in targets:
        try:
            after = (root / target).read_bytes()
        except OSError:
            after = None  # a target that cannot be read any more counts as changed
        if after != before[target]:
            changed.append(target)
    named = ", ".join(f"`{_one_line(target)}`" for target in changed)
    line = f"ruff changed {named}" if changed else "ruff changed no file"
    if notes:
        line += "; " + "; ".join(notes)
    return protect_diagnostics(line + ".", key)


def verify_attempt(
    root: Path,
    plan: Path,
    key: str | None = None,
    formatted: list[str] | None = None,
    tools: dict[str, str] | None = None,
) -> list[str]:
    """Clear derivable ledger markers, stamp changed held documents, render the index, format, `make verify`.

    Preparation writes to the tree and executes its registry renderer. Before `make verify` the
    runner applies ruff's safe fixes and its formatter to the changed Python files under `scripts/`
    and `tests/`; when `formatted` is given, the step's line lands there. Return bounded
    diagnostics for failed preparation or postconditions, naming the gates that blocked.
    The time section must still be readable; the entry itself is the runner's (`run_attempts`), so the
    model adds none and nothing is compared with the pre-call plan.
    """
    env = runner_env(
        foreign_env(
            {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "commit.gpgsign",
                "GIT_CONFIG_VALUE_0": "false",
            }
        ),
        root,
    )
    tampered = tool_problem(root, tools)
    if tampered:
        # The attempt overwrote a program the runner starts: it fails here, before the renderer or
        # ruff runs, and the diagnostic names the path (R-21, acceptance criterion).
        return [tampered]
    try:
        # The marker of a test the attempt wrote is derivable, so it is not the attempt's to forget
        # (bead coding-harness-7g6h); the stamp below then sees the plan as changed. The plan is an
        # attempt-writable path: an alias (a symlink in it or its parents, a hard link) would carry the
        # write outside the worktree, so it is refused first (runner review R-1, 2026-10-25).
        relative = plan.relative_to(root)
        if plan.is_symlink() or plan.resolve() != root.resolve() / relative:
            return [f"refusing an aliased plan before clearing its ledger: {relative.as_posix()}"]
        if plan.exists() and plan.stat().st_nlink > 1:
            return [f"refusing a hard-linked plan before clearing its ledger: {relative.as_posix()}"]
        check_criterion_ledger.clear_written(root, plan)
    except (OSError, RuntimeError, ValueError) as error:
        return [
            f"the criterion ledger of {plan.name} could not be updated: {getattr(error, 'strerror', None) or error}"
        ]
    preparation = prepare_derived(root, env, key)
    if preparation:
        return preparation
    line = format_step(root, env, key, tools)
    if formatted is not None and line is not None:
        formatted.append(line)
    try:
        done = launch(
            ["make", "verify"],
            root,
            env,
            timeout=VERIFY_SECONDS,
            limit=f"the runner's step limit after {VERIFY_SECONDS // 60} minutes",
        )
    except StepTimedOut as error:
        # A hang the attempt caused is a repairable diagnostic for the next attempt, not a make that
        # could not be started (O188-4 of the #188 review).
        return [f"`make verify` did not finish: {error}"]
    problems = []
    if done.returncode != 0:
        problems.append(f"`make verify` exited {done.returncode}\n{verify_evidence(done, key)}".rstrip())
    try:
        time_log(plan)
    except Refused as error:
        problems.append(str(error))
    return problems


# Paths a stage-2 attempt never writes, whatever `provenance.yaml` says: the runner's own rules, the
# prompts, the workflow's decision area and the tracker. `decisions/gates.yaml` is here because it has
# no provenance class of its own - the class is the maintainer's decision (R-22 of the review-swarm
# review), and until it is made the runner refuses the file rather than let a weakened gate through.
RUNNER_HELD = (
    "provenance.yaml",
    "decisions/gates.yaml",
    "model-endpoints.yaml",
    # Everything a harness loads as instructions, hooks, agents, skills or tools. `.claude/` is held
    # whole (settings, hooks, agents, commands, rules); `CLAUDE.md` would silently replace `AGENTS.md`
    # for Claude Code (docs/WORKFLOW.md §3 lists it and `.mcp.json` as "not created"); `.codex/` holds
    # the hook list, `.agents/` the skills, `.pi/` the reviewer session's own files.
    ".claude/",
    ".codex/",
    ".agents/",
    ".pi/",
    ".mcp.json",
    "CLAUDE.md",
    "prompts/",
    "templates/",
    ".github/",
    ".beads/",
    "AGENTS.md",
    "README.md",
)


def uncommittable(root: Path, change: str, keep: set[Path] | None = None) -> list[str]:
    """The changed paths a stage-2 attempt must not commit, named (R-16 of the review-swarm review).

    The classes come from the committed `provenance.yaml`, never from the tree the attempt wrote:
    a `human-decided` prefix or one of `RUNNER_HELD` is out of a model's reach, the change's own
    folder is not. `keep` holds what the verb may keep changed - a draft's own new ADR under the
    `docs/adr/` prefix is exactly that (P1 of the #192 review).
    """
    spared = {path.as_posix() for path in keep or ()}
    try:
        data = yaml.safe_load(_git_output(root, "show", "HEAD:provenance.yaml"))
        # A commit without a provenance map declares no class; `RUNNER_HELD` still holds.
        entries = data.get("paths") or [] if isinstance(data, dict) else []
        decided = [
            str(entry["prefix"])
            for entry in entries
            if entry.get("allowed") and set(entry["allowed"]) == {"human-decided"}
        ]
    except (Refused, KeyError, TypeError, AttributeError, yaml.YAMLError) as error:
        raise Refused(f"the committed provenance map cannot be read; no attempt is committed ({error})") from error
    folder = f"plans/changes/{change}/"
    # Case-folded on both sides: on a case-insensitive checkout `.Claude/Rules/` is `.claude/rules/` (O192-2).
    held = [path.casefold() for path in [*decided, *RUNNER_HELD]]
    return sorted(
        relative.as_posix()
        for relative in changed_paths(root)
        if relative.as_posix() not in spared
        and not relative.as_posix().startswith(folder)
        and any(relative.as_posix().casefold().startswith(path) for path in held)
    )


def checkpoint(
    root: Path,
    change: str,
    baseline: str,
    key: str | None = None,
    ignored_before: dict[Path, tuple[int, int]] | None = None,
    message: str | None = None,
    keep: set[Path] | None = None,
) -> None:
    """Commit a passing work phase and prove the one clean descendant commit."""
    if key is not None:
        exposed = remove_changed_credential(root, key, ignored_before)
        if exposed:
            raise Refused(credential_message(exposed))
    try:
        blocked = uncommittable(root, change, keep)
    except Refused as error:
        # An unreadable map is a failure of this attempt, repairable by the next one - and the edits go
        # first, so nothing the runner could not classify stays in the tree (O192-5).
        restored = restore_baseline(root, baseline, set(keep or ()), ignored_before)
        raise CallFailed(f"{error}; {restored}") from error
    if blocked:
        # The tree goes back to the baseline, but `keep` stands: what the verb itself may keep changed -
        # its change folder, a draft's own new ADR, the findings a human may have touched - is not the
        # refused attempt's to lose (P1 and P2 of the #192 review).
        restored = restore_baseline(root, baseline, set(keep or ()), ignored_before)
        raise CallFailed(
            "the attempt changed paths a stage-2 run does not commit: "
            + ", ".join(f"`{path}`" for path in blocked)
            + f"; {restored}"
        )
    try:
        _git_output(root, "add", "-A")
        _git_output(
            root,
            "-c",
            "commit.gpgsign=false",
            "-c",
            "user.name=stage2-runner",
            "-c",
            "user.email=stage2-runner@invalid",
            "commit",
            "-m",
            message or f"feat({change}): implement accepted plan",
        )
        count = _git_output(root, "rev-list", "--count", f"{baseline}..HEAD").strip()
    except Refused as error:
        raise CallFailed(f"the runner checkpoint failed: {error}") from error
    try:
        ancestor = subprocess.run(
            [GIT, "-C", str(root), "merge-base", "--is-ancestor", baseline, "HEAD"],
            capture_output=True,
            check=False,
            timeout=GIT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise CallFailed(f"the runner checkpoint could not be measured within {GIT_SECONDS // 60} minutes") from error
    if ancestor.returncode != 0 or count != "1":
        raise CallFailed("the runner checkpoint is not exactly one descendant commit")
    try:
        dirty = _git_output(root, "status", "--porcelain=v1", "--untracked-files=all").strip()
    except Refused as error:
        raise CallFailed(f"the runner checkpoint failed: {error}") from error
    if dirty:
        raise CallFailed("the runner checkpoint left a dirty worktree")


# ---------------------------------------------------------------------------
# The repair of the taken findings
# ---------------------------------------------------------------------------


def red_first_python(root: Path) -> str:
    """The interpreter of a red-first run: the checkout's venv when it is executable, else this one."""
    venv = root / ".venv" / "bin" / "python3"
    return str(venv) if (venv.is_file() and os.access(venv, os.X_OK)) else sys.executable


def _ref_targets(root: Path) -> dict[str, str]:
    """Every ref of the repository, remote-tracking ones included, with the object it names."""
    listing = _git_output(root, "for-each-ref", "--format=%(refname) %(objectname)")
    return {name: target for name, _, target in (line.partition(" ") for line in listing.splitlines() if line)}


def _red_report_bytes(path: Path) -> bytes | None:
    """The outcome record's bytes, or None when it cannot be read."""
    try:
        return path.read_bytes()
    except OSError:
        return None


def _red_own_selector(nodeid: str, selector: str) -> bool:
    """Whether a recorded node id is the requested test or one of its parameterized cases."""
    return nodeid == selector or nodeid.startswith(selector + "[")


def _red_record_fault(record: bytes | None, token: str, selector: str, *, passing: bool = False) -> str | None:
    """Why the outcome record cannot prove this invocation red first, or None when it can.

    The record must be this selector's and this invocation's (a fresh token binds it to one run),
    show a finished session that pytest ended as a failing run, and hold phases that prove at least
    one ordinary assertion-failing call of the requested test, passing setup and teardown for every
    selected case and no other outcome among the calls. Text quoted from the record - a foreign
    selector, a node id - is the caller's to scrub before it reaches a diagnostic.
    """
    if record is None:
        return "the outcome record is missing; the named test's outcome cannot be proven"
    try:
        parsed = json.loads(record.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return "the outcome record is not readable JSON"
    if not isinstance(parsed, dict):
        return "the outcome record is not a JSON object"
    if parsed.get("schema") != 1:
        return f"the outcome record has schema {parsed.get('schema')!r}, not 1"
    named = parsed.get("selector")
    if named != selector:
        return f"the outcome record names `{_one_line(str(named))}`, not the requested test"
    if parsed.get("token") != token:
        return "the outcome record is not this invocation's (a stale or foreign token)"
    session = parsed.get("session")
    if not isinstance(session, dict) or session.get("finished") is not True:
        return "the outcome record shows no finished session; the run's outcome cannot be proven"
    expected_exit = 0 if passing else 1
    if session.get("exitstatus") != expected_exit:
        expected_run = "passing" if passing else "failing"
        return f"the session ended {session.get('exitstatus')!r}, not as a {expected_run} run"
    errors, selected, phases = (parsed.get("collection_errors"), parsed.get("selected"), parsed.get("phases"))
    if not isinstance(errors, list) or not isinstance(selected, list) or not isinstance(phases, list):
        return "the outcome record does not hold the collection errors, the selection and the phases"
    if errors:
        return "collection failed before any selected test ran: " + ", ".join(
            f"`{_one_line(str(nodeid))}`" for nodeid in errors
        )
    if not selected:
        return "no test was selected; the named test did not run"
    for nodeid in (*selected, *(phase.get("nodeid") for phase in phases if isinstance(phase, dict))):
        if not isinstance(nodeid, str) or not _red_own_selector(nodeid, selector):
            return f"the outcome record names `{_one_line(str(nodeid))}`, not the requested test"
    by_case: dict[str, dict[str, dict]] = {}
    for phase in phases:
        if not isinstance(phase, dict):
            return "the outcome record holds a phase that is not an object"
        nodeid, name, recorded = phase.get("nodeid"), phase.get("phase"), phase.get("outcome")
        if (
            not isinstance(nodeid, str)
            or name not in ("setup", "call", "teardown")
            or recorded not in ("passed", "failed", "skipped")
            or not isinstance(phase.get("assertion"), bool)
            or not isinstance(phase.get("expected"), bool)
            or not (phase.get("exception") is None or isinstance(phase.get("exception"), str))
        ):
            return "the outcome record holds a phase of an invalid form"
        case = by_case.setdefault(nodeid, {})
        if name in case:
            return f"the outcome record holds two {name} phases for `{_one_line(nodeid)}`"
        case[name] = phase
    red = False
    for nodeid in selected:
        case = by_case.get(nodeid)
        if case is None:
            return f"the outcome record holds no phases for `{_one_line(nodeid)}`"
        # A failed setup records no call phase, so the setup and teardown verdicts come before the
        # presence of the other phases: the refusal must name the failure, not the phase the
        # failure removed (a missing dependency's fixture error, bead coding-harness-omp).
        if "setup" not in case:
            return f"the outcome record holds no setup phase for `{_one_line(nodeid)}`"
        if case["setup"]["outcome"] != "passed":
            return (
                f"the setup phase of `{_one_line(nodeid)}` ended {case['setup']['outcome']}; "
                "red first needs passing setup and teardown"
            )
        if "teardown" not in case:
            return f"the outcome record holds no teardown phase for `{_one_line(nodeid)}`"
        if case["teardown"]["outcome"] != "passed":
            return (
                f"the teardown phase of `{_one_line(nodeid)}` ended {case['teardown']['outcome']}; "
                "red first needs passing setup and teardown"
            )
        if "call" not in case:
            return f"the outcome record holds no call phase for `{_one_line(nodeid)}`"
        call = case["call"]
        if call["expected"]:
            return f"the call of `{_one_line(nodeid)}` is marked expected-failing or unexpectedly passed"
        if call["outcome"] == "skipped":
            return f"the call of `{_one_line(nodeid)}` was skipped"
        if passing and call["outcome"] != "passed":
            return (
                f"the call of `{_one_line(nodeid)}` ended {call['outcome']}; fixed-code proof needs every case to pass"
            )
        if call["outcome"] == "failed":
            if not call["assertion"]:
                return (
                    f"the call of `{_one_line(nodeid)}` failed with {call['exception'] or 'an exception'}, "
                    "not an AssertionError"
                )
            red = True
        elif call["outcome"] != "passed":
            return f"the call of `{_one_line(nodeid)}` ended {call['outcome']!r}"
    if not passing and not red:
        return "no selected call failed by assertion; the run is green for the requested test"
    return None


def fixed_test_proof(root: Path, test: str, key: str | None, tools: dict[str, str] | None = None) -> str | None:
    """Prove the named test actually passes on fixed code before writing its evidence mark (O199-1).

    A green suite can include a skipped or expected-failing named test. The same runner-owned probe
    used for red first must show passing setup, call and teardown for every selected case here.
    Load the probe by its private absolute path, outside the attempt's tree. A proof that changes
    the tree or any ref is refused, and no changed ref is deleted or reset.
    """
    tampered = tool_problem(root, tools)
    if tampered:
        return f"{test}: fixed-code proof: {tampered}"
    bootstrap = (
        "import importlib.util, sys, pytest; "
        "spec = importlib.util.spec_from_file_location('stage2_fixed_probe', sys.argv[1]); "
        "probe = importlib.util.module_from_spec(spec); spec.loader.exec_module(probe); "
        "raise SystemExit(pytest.main(['-q', '-p', 'no:cacheprovider', sys.argv[2]], plugins=[probe]))"
    )
    token = os.urandom(16).hex()
    try:
        with tempfile.TemporaryDirectory(prefix="stage2-fixed-") as tmp:
            probe = Path(tmp) / "probe.py"
            report = Path(tmp) / "outcome.json"
            probe.write_text(RED_PROBE_SOURCE, encoding="utf-8")
            refs_before, tree_before = _ref_targets(root), worktree_tree(root)
            done = launch(
                [red_first_python(root), "-c", bootstrap, str(probe), test],
                root,
                runner_env(
                    foreign_env(
                        {"STAGE2_RED_REPORT": str(report), "STAGE2_RED_TOKEN": token, "STAGE2_RED_SELECTOR": test}
                    ),
                    root,
                ),
                key,
                timeout=RED_FIRST_MINUTES * 60,
                limit="the fixed-code proof time limit",
            )
            fault = _red_record_fault(_red_report_bytes(report), token, test, passing=True)
            if done.returncode != 0:
                fault = f"pytest ended {done.returncode} on the fixed code" + (f"; {fault}" if fault else "")
            if _ref_targets(root) != refs_before:
                fault = "refs changed while the fixed-code proof ran"
            elif worktree_tree(root) != tree_before:
                fault = "the worktree changed while the fixed-code proof ran"
    except (CallFailed, Refused, OSError) as error:
        fault = str(error)
    return scrub(f"{test}: fixed-code proof: {fault}", key) if fault else None


def red_first(root: Path, baseline: str, test: str, key: str | None, tools: dict[str, str] | None = None) -> str | None:
    """Run one named test against the baseline's code in a temporary git worktree; None when it was red.

    The worktree's `tests/` is the attempt's, without `__pycache__` and `.pytest_cache`: a test of the
    new tests against the old code is what "red first" means, and a real git checkout keeps tests that
    call git honest. The interpreter must start pytest first: a `No module named pytest` startup failure
    exits 1 too, and reading it as red would accept a run in which the named test never ran (phase 6,
    F-1). Exit 1 alone proves nothing either: the runner-owned probe (`RED_PROBE_SOURCE`) travels into
    the temporary checkout and records, in a private JSON report outside the copied tests, which cases
    pytest selected and how every setup, call and teardown phase ended. The proof holds only when the
    report is this invocation's, the session finished as exit 1, at least one selected call of the
    requested test failed on an ordinary assertion, every setup and teardown passed and no skip, xfail,
    XPASS, collection error or non-assertion failure stands among them - so a missing dependency
    failing its fixture refuses instead of certifying the repair (bead coding-harness-omp). Never is a
    success inferred from terminal output or the exit code alone. Every ref's name and target is
    compared before and after: a difference fails the proof with the refs named and nothing is deleted,
    so another session's branch is never touched (phase 6, F-6 and F-7). The clean-up deletes the
    temporary directory before it prunes, so a failed `git worktree remove` leaves no dead entry
    behind, and a failed removal is named in the returned problem.
    """
    tampered = tool_problem(root, tools)
    if tampered:
        # The red-first interpreter and pytest come from `.venv/`: a changed tree is not run (R-21).
        return f"{test}: {tampered}"
    file, _, function = test.partition("::")
    selector = f"{file}::{function}"
    token = os.urandom(16).hex()
    tree = None
    tmp = None
    outcome = None
    removal = None
    added = False
    refs_before: dict[str, str] | None = None
    refs_changed: list[str] = []
    try:
        tmp = tempfile.mkdtemp(prefix="stage2-red-")
        tree = Path(tmp) / "tree"
        report = Path(tmp) / "red-outcome.json"
        try:
            _git_output(root, "worktree", "add", "--detach", str(tree), baseline)
        except Refused as error:
            outcome = f"{test}: the red-first checkout failed ({scrub(str(error), key)})"
        else:
            added = True
        if outcome is None:
            shutil.rmtree(tree / "tests", ignore_errors=True)
            try:
                shutil.copytree(
                    root / "tests", tree / "tests", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache")
                )
            except OSError as error:
                outcome = (
                    f"{test}: the red-first checkout could not take the attempt's tests ({scrub(str(error), key)})"
                )
        if outcome is None:
            try:
                (tree / f"{RED_PROBE_NAME}.py").write_text(RED_PROBE_SOURCE, encoding="utf-8")
            except OSError as error:
                outcome = f"{test}: the red-first outcome probe could not be written ({scrub(str(error), key)})"
        if outcome is None:
            # Branches are shared with the temporary checkout; a failed snapshot fails the attempt,
            # because branch state could not be proven preserved.
            try:
                refs_before = _ref_targets(root)
            except Refused as error:
                outcome = f"{test}: the red-first ref snapshot failed ({scrub(str(error), key)})"
        if outcome is None:
            try:
                started = launch(
                    [red_first_python(root), "-c", "import pytest"],
                    tree,
                    runner_env(foreign_env({}), root, tree),
                    key,
                    timeout=RED_FIRST_MINUTES * 60,
                    limit="the red-first time limit",
                )
            except CallFailed as error:
                outcome = f"{test}: {scrub(str(error), key)}"
            else:
                if started.returncode != 0:
                    outcome = (
                        f"{test}: the red-first interpreter cannot start pytest (exit {started.returncode}); "
                        "the named test did not run"
                    )
        if outcome is None:
            try:
                done = launch(
                    [
                        red_first_python(root),
                        "-m",
                        "pytest",
                        "-q",
                        "-p",
                        "no:cacheprovider",
                        "-p",
                        RED_PROBE_NAME,
                        selector,
                    ],
                    tree,
                    runner_env(
                        foreign_env(
                            {
                                "STAGE2_RED_REPORT": str(report),
                                "STAGE2_RED_TOKEN": token,
                                "STAGE2_RED_SELECTOR": selector,
                            }
                        ),
                        root,
                        tree,
                    ),
                    key,
                    timeout=RED_FIRST_MINUTES * 60,
                    limit="the red-first time limit",
                )
            except CallFailed as error:
                outcome = f"{test}: {scrub(str(error), key)}"
            else:
                if done.returncode != 1:
                    outcome = (
                        f"{test}: pytest ended {done.returncode} on the baseline's code; "
                        "red first needs exit 1 with an assertion failure"
                    )
                else:
                    fault = _red_record_fault(_red_report_bytes(report), token, selector)
                    if fault is not None:
                        outcome = f"{test}: {scrub(fault, key)}"
    finally:
        if tree is not None:
            try:
                done = subprocess.run(
                    [GIT, "-C", str(root), "worktree", "remove", "--force", str(tree)],
                    capture_output=True,
                    check=False,
                    timeout=GIT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                done = None
            if added and done is not None and done.returncode != 0:
                removal = f"`git worktree remove` ended {done.returncode} on the red-first checkout"
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)
        if tree is not None:
            # Only after the directory is gone: a prune over a present directory keeps a failed removal's entry.
            with contextlib.suppress(subprocess.TimeoutExpired):
                # A prune that hangs leaves an entry behind; the removal above already failed then.
                subprocess.run(
                    [GIT, "-C", str(root), "worktree", "prune"],
                    capture_output=True,
                    check=False,
                    timeout=GIT_SECONDS,
                )
        if refs_before is not None:
            # Nothing is deleted or reset here: another session may create a branch meanwhile, and only
            # the comparison tells a change of the run from one of a neighbour. Any difference in a
            # ref's name or target fails the proof with the refs named (phase 6, F-6 and F-7).
            try:
                refs_now = _ref_targets(root)
            except Refused as error:
                refs_changed = [f"the ref listing failed ({scrub(str(error), key)})"]
            else:
                refs_changed = sorted(
                    ref for ref in refs_before.keys() | refs_now.keys() if refs_before.get(ref) != refs_now.get(ref)
                )
    if refs_changed:
        named = scrub(f"{test}: refs changed while the named test ran: {', '.join(refs_changed)}", key)
        outcome = f"{outcome}\n{named}" if outcome else named
    if removal is not None:
        named = scrub(f"{test}: {removal}", key)
        outcome = f"{outcome}\n{named}" if outcome else named
    return outcome


def fixed_status(ident: str, rest: str) -> str:
    """The Status one fixed line gives, or the problem sentence that holds for it."""
    match = re.fullmatch(r"fixed — (.+)", rest)
    if match is None:
        return (
            f"{ident}: the line is neither `<ID>: fixed — tests/<path>::<function>` nor "
            "`<ID>: fixed — not a test — <reason>`"
        )
    body = match.group(1).strip()
    if body == "not a test" or body.startswith("not a test —"):
        reason = body.partition("—")[2].strip()
        if not reason:
            return f"{ident}: `fixed — not a test` without a reason"
        # Escaped once, whatever the fixed line spelled: a `\|` the format asked for is unfolded first,
        # so a reason written the way REPAIR_FORMAT asks never lands with a second backslash.
        return "fixed — not a test — " + reason.replace("\\|", "|").replace("|", "\\|")
    if (test := FIXED_TEST.fullmatch(body)) and Path(test.group("file")).name.startswith("test_"):
        if any(segment in (".", "..") for segment in body.partition("::")[0].split("/")):
            return f"{ident}: `{body}` would climb out of `tests/`; a `.` or `..` path segment is no test path"
        return f"fixed — {body}"
    return f"{ident}: `{body}` is neither a test `tests/<path>::<function>` nor `not a test — <reason>`"


def check_repair_answer(
    ctx: Context,
    answer: str,
    taken: list[tuple[str, list[str]]],
    baseline: str,
    key: str | None,
    before: tuple[list[list[str]], list[list[str]]],
    audit_line: str | None = None,
    findings_before: str | None = None,
    tools: dict[str, str] | None = None,
) -> tuple[dict[str, str], dict[str, str], list[str]]:
    """Read an answer's fixed lines: the Status each taken row takes, the `Broke a test` marks its own
    evidence proves, and the problems that fail the attempt.

    Each problem names its ID. Lines without a colon, and colon lines whose left side names neither an
    active row exactly nor a finding-shaped id, are ignored unless their right side claims a fixed
    status. A finding-shaped id or claimed fix that names no taken row still fails. Every row of
    findings.md must also stand as `before` holds it - the taken rows and the others alike, cell for cell: an edit outside the taken
    rows' Status is named, not checkpointed (phase 6, F-3). The pre-call findings body also protects
    other phases and every earlier attempt's evidence; only the frontmatter is excluded, because the
    runner refreshes `updated:`. Only when no problem stands do the red-first runs start, one pytest run
    per named test; every text is scrubbed with the key.
    """
    active = {row[0] for _, row in taken}
    # Include rejected and fixed findings: they establish the same vocabulary as active rows.
    rows = [*(row for _, row in taken), *before[0], *before[1], *record_rows(read_record(ctx.change, ctx.root) or "")]
    prefixes = {match[1] for row in rows if (match := FINDING_ID.fullmatch(row[0])) and match[1] != "L"}
    if any(LOOP_ID.fullmatch(row[0]) for row in rows):
        prefixes.add("L")
    problems: list[str] = []
    parsed: dict[str, list[str]] = {}
    for raw in answer.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        ident, sep, rest = line.partition(":")
        ident = ident.strip().strip("*`").strip()
        rest = rest.strip()
        # An active row is matched exactly first: a phase-6 id is free text, so the finding shape alone
        # cannot carry every real fixed line (spec, criterion 2).
        if not sep or not ident:
            continue
        shape = FINDING_ID.fullmatch(ident)
        if (
            ident not in active
            and not LOOP_ID.fullmatch(ident)
            and not (shape and shape[1] in prefixes)
            and not rest.lstrip("*` ").startswith("fixed — ")
        ):
            continue
        parsed.setdefault(ident, []).append(rest)
    fixes: dict[str, str] = {}
    for _place, row in taken:
        ident, given = row[0], parsed.pop(row[0], [])
        if not given:
            problems.append(f"{ident}: no fixed line")
            continue
        if len(given) > 1:
            problems.append(f"{ident}: several fixed lines")
            continue
        outcome = fixed_status(ident, given[0])
        if outcome.startswith("fixed — "):
            fixes[ident] = outcome
        else:
            problems.append(outcome)
    for ident in parsed:
        problems.append(f"{ident}: no taken row carries this id")
    if problems:
        return {}, {}, [scrub(problem, key) for problem in problems]
    findings_now = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
    released_now, phase6_now = findings_rows(findings_now)
    if audit_line and audit_line not in findings_now.splitlines():
        problems.append("findings.md no longer holds the audit line of this call; a passing repair keeps it")
    if findings_before is not None:
        header = r"\A---\n.*?\n---\n"
        body_before = re.sub(header, "", findings_before, count=1, flags=re.S)
        body_now = re.sub(header, "", findings_now, count=1, flags=re.S)
        if body_now != body_before:
            problems.append(
                "findings.md changed outside runner bookkeeping; every finding and earlier attempt's evidence must stand"
            )
    for _place, row in taken:
        ident, fix = row[0], fixes[row[0]]
        if fix.startswith("fixed — not a test"):
            if not row[7].lower().startswith("taken — not a test"):
                problems.append(
                    f"{ident}: answered `not a test`, but the row is a code row; it needs a test that was red first"
                )
        else:
            test = fix[len("fixed — ") :]
            function = test.partition("::")[2]
            body = _read_quietly(ctx.root / test.partition("::")[0])
            if not defines_test(body, function):
                problems.append(f"{ident}: {test} defines no function `def {function}(`")
    for place, rows_before, rows_now in (
        ("released", before[0], released_now),
        ("phase-6", before[1], phase6_now),
    ):
        # Rows are compared with their counts: an added or a removed identical copy fails too (F-9).
        counts_before = Counter(tuple(row) for row in rows_before)
        counts_now = Counter(tuple(row) for row in rows_now)
        for row in (counts_before - counts_now).elements():
            problems.append(f"{row[0]}: the {place} row no longer stands in findings.md as it stood before the repair")
        for row in (counts_now - counts_before).elements():
            problems.append(f"{row[0]}: findings.md holds a {place} row that stood nowhere before the repair")
    if problems:
        return {}, {}, [scrub(problem, key) for problem in problems]
    marks: dict[str, str] = {}
    for _place, row in taken:
        fix = fixes[row[0]]
        if fix.startswith("fixed — tests/"):
            anchor = fix[len("fixed — ") :]
            outcome = red_first(ctx.root, baseline, anchor, key, tools)
            if outcome is None:
                outcome = fixed_test_proof(ctx.root, anchor, key, tools)
            if outcome is not None:
                problems.append(f"{row[0]}: {outcome}")
                continue
            # The proof ran and passed: the mark states exactly what was shown (R-24, the maintainer's
            # answer C in the night interview of 2026-10-20). A row without a proof gets no mark.
            marks[row[0]] = f"yes — {anchor}"
        elif fix.startswith("fixed — not a test"):
            marks[row[0]] = "no — not a test"
    if problems:
        return {}, {}, [scrub(problem, key) for problem in problems]
    return {ident: scrub(status, key) for ident, status in fixes.items()}, marks, []


def defines_test(body: str, function: str) -> bool:
    """Whether the test body defines exactly this test function, at any indentation and possibly `async`.

    A test method inside a class (`    def test_x(self):`) is a test like any other; requiring `def` at
    column 0 refused it as "defines no function" (R-23 of the review-swarm review).
    """
    return re.search(rf"^\s*(?:async\s+)?def\s+{re.escape(function)}\s*\(", body, re.M) is not None


def _read_quietly(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def mark_repaired_findings(ctx: Context, taken: list[tuple[str, list[str]]], fixes: dict[str, str]) -> None:
    """Write each taken findings row's fixed Status in its place, before the checkpoint commit.

    Only the Status cell (index 7) of a taken row changes; a `|` of a reason stands escaped, as the
    fixed line carried it. Every other cell of any row and every other line stays as it is, the
    file's final newline included: the lines are split on `\\n`, so the ending empty line survives.
    """
    by_key = {(place, row[0]): row for place, row in taken}
    lines: list[str] = []
    kind = ""
    for line in ctx.findings.read_text(encoding="utf-8").split("\n"):
        if line.startswith("## "):
            kind = ""
            if line.startswith(RELEASE_HEADING):
                kind = "released"
            elif line.startswith("## Phase 6"):
                kind = "phase-6"
        elif kind == "released" and KEPT_FROM.match(line):
            kind = ""
        else:
            cells = split_row(line) if kind else None
            if cells and (kind, cells[0]) in by_key and cells == by_key[(kind, cells[0])]:
                cells[7] = fixes[cells[0]]
                line = "| " + " | ".join(cells) + " |"
        lines.append(line)
    ctx.findings.write_text("\n".join(lines), encoding="utf-8")
    stamp_updated(ctx.findings)


def mark_repaired_record(
    change: str,
    taken: list[tuple[str, list[str]]],
    fixes: dict[str, str],
    root: Path,
    marks: dict[str, str] | None = None,
) -> None:
    """Mark the record's own row lines the same way, after the checkpoint commit.

    The record lies outside what the file tools reach, so only the runner can write it; a failure
    leaves the statuses unwritten there and names the IDs to mark by hand. The record's ending stays
    as it was read.
    """
    by_key = {row[0]: row for place, row in taken if place == "record"}
    if not by_key:
        return
    # The record is read and rewritten whole: a round appended in between, or a release that removes
    # the record, would be lost, so the rewrite holds the lock the loop verbs hold (O190-4).
    try:
        with holding_record(change, root):
            _mark_record_rows(change, by_key, fixes, root, marks)
    except Refused as error:
        waiting = ", ".join(sorted(by_key))
        raise CallFailed(f"the loop record could not be marked ({error}); mark {waiting} by hand.") from error


def _mark_record_rows(
    change: str, by_key: dict[str, list[str]], fixes: dict[str, str], root: Path, marks: dict[str, str] | None = None
) -> None:
    record = read_record(change, root)
    if record is None:
        return
    ending = "\n" if record.endswith("\n") else ""
    lines: list[str] = []
    for line, reviewer in _record_lines(record):
        if not reviewer:
            cells = split_row(line)
            if (
                cells
                and len(cells) >= len(ROW_COLUMNS)
                and LOOP_ID.fullmatch(cells[0])
                and cells[0] in by_key
                and [*cells[:7], " \\| ".join(cells[7:-1]), cells[-1]] == by_key[cells[0]]
            ):
                mark = (marks or {}).get(cells[0], cells[-1])
                line = "| " + " | ".join([*cells[:7], fixes[cells[0]], mark]) + " |"
        lines.append(line)
    try:
        (record_dir(change, root) / "loop.md").write_text("\n".join(lines) + ending, encoding="utf-8")
    except OSError as error:
        waiting = ", ".join(sorted(by_key))
        raise CallFailed(f"the loop record could not be marked ({error}); mark {waiting} by hand.") from error


def explore(root: Path, change: str, stage2_off: str | None = None) -> None:
    """Phase 1: GLM Flash, or explicit Haiku fallback, appends repository facts."""
    endpoint = HAIKU if stage2_off is not None else GLM_FLASH
    ctx = preflight(root, change, endpoint, bead_file="research.md")
    key = None
    route = "stage-1" if stage2_off is not None else "flash"
    if stage2_off is None:
        key = read_secret("GLM_KEY")
        if key is None:
            raise Refused(f"GLM_KEY is not in the secrets file {secrets_path()}.")
    extra = (
        "Report repository facts with source paths as prose ready to append to `research.md`. "
        "Do not design, recommend, edit a file or use review-table formatting."
    )
    prompt = work_prompt(root, "01-explore.md", change, extra)
    begin_work_call(ctx, "explore", endpoint, prompt, 1, route, ctx.research, stage2_off)
    answer = run_work_model(ctx, prompt, endpoint, writable=False, key=key)
    append(ctx.research, f"## Runner exploration — {today()}\n\n{answer.strip()}")
    print(f"explore: answer appended to {ctx.research.relative_to(root)} · route {route}")


def implementation_prompt(
    ctx: Context, baseline: str, diagnostics: list[str], inputs: dict[Path, bytes] | None = None
) -> str:
    """The accepted inputs and the bounded evidence from earlier attempts."""
    spec = prompt_input(ctx.folder / "spec.md", inputs)
    plan = prompt_input(ctx.plan, inputs)
    extra = [
        "Implement only the accepted plan with the available file tools. You cannot run commands. "
        "Write no entry under `## Time used` in plan.md: the runner measures this attempt and writes "
        "its span itself. The runner runs `make verify`, stages the result and creates the checkpoint commit.",
        f"Implementation baseline: {baseline}",
        f"## Accepted spec\n\n{spec}",
        f"## Accepted plan\n\n{plan}",
    ]
    if diagnostics:
        extra.append("## Earlier post-run diagnostics\n\n" + "\n\n".join(diagnostics))
    return work_prompt(ctx.root, "04-implement.md", ctx.change, "\n\n".join(extra), inputs)


def restore_work_input(root: Path, path: Path, content: bytes) -> None:
    """Replace aliases from the worktree outward before inspecting or restoring an input."""
    parent = root
    for part in path.relative_to(root).parts[:-1]:
        parent /= part
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            parent.unlink()
        parent.mkdir(exist_ok=True)
    replace = path.is_symlink() or not path.is_file()
    if not replace:
        try:
            # Matching bytes do not make a hard link safe: a later date stamp would
            # still write through it to the external target. Detach before reading.
            replace = path.stat().st_nlink > 1 or path.read_bytes() != content
        except OSError:
            # A readable parent can replace an unreadable model-written input. Recovery
            # uses trusted bytes, so a failed comparison must not prevent that replacement.
            replace = True
    if replace:
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        path.write_bytes(content)


def persist_time_entry(
    root: Path,
    plan: Path,
    entry: str,
    prior: str,
    inputs_before: dict[Path, bytes],
    *,
    accepted: bool,
    retry: bool,
    original: BaseException | None = None,
) -> None:
    """Persist one completed attempt's entry - the one writer for normal and exceptional departures.

    `retry` persists the entry on the pre-call plan and updates `inputs_before`, so even a failed
    input restore cannot lose it; every other attempt writes the plan here too. A rejected entry whose
    destination is missing, unreadable or aliased recovers the pre-call plan safely first: parents
    are rebuilt and aliases detach from the worktree outward, so a linked external target never
    receives the write, and model bytes are never restored for it. A failed write fails closed -
    beside the attempt's own failure when one stands - and never retries, checkpoints or turns a
    refusal into success. The span must already have ended at the last check that ran; this
    function only persists it.
    """
    try:
        if retry:
            # Persist before restoring any other input: that restoration can fail before reaching
            # the plan. Keep the same trusted bytes in the retry snapshot for a successful restore.
            content = with_time_entry(prior, entry).encode("utf-8")
            restore_work_input(root, plan, content)
            stamp_updated(plan)
            inputs_before[plan] = content
            return
        try:
            # A parent alias cannot safely be repaired by unlinking the document: that would
            # remove a path in the alias target. Refuse before reading or writing through it.
            if plan.parent.resolve() != root.resolve() / plan.relative_to(root).parent:
                raise Refused("refusing an aliased plan parent")
            if plan.is_symlink() or plan.stat().st_nlink > 1:
                raise Refused("refusing an aliased or hard-linked plan")
            text = with_time_entry(plan.read_text(encoding="utf-8"), entry, prior=prior)
            plan.write_text(text, encoding="utf-8")
        except (Refused, OSError, UnicodeDecodeError, RuntimeError):
            if accepted:
                raise
            # A rejected attempt left the plan missing, unreadable or aliased: the trusted pre-call
            # plan takes the entry, aliases detached, parents repaired, never through a link.
            restore_work_input(root, plan, with_time_entry(prior, entry).encode("utf-8"))
        stamp_updated(plan)
    except (Refused, OSError, UnicodeDecodeError, RuntimeError) as logging_error:
        message = f"the runner could not write the attempt's time entry to {plan}: {logging_error}"
        if original is None:
            raise CallFailed(message) from logging_error
        raise CallFailed(f"{message}; the attempt's own failure stands: {original}") from original


def run_attempts(
    ctx: Context,
    verb: str,
    routes: list[tuple[tuple[str, str, str | None], str | None, str, str | None]],
    build_prompt,  # (diagnostics, endpoint, inputs) -> prompt
    baseline: str,
    key: str | None,
    ignored_before: dict[Path, tuple[int, int]] | None,
    commit_message: str,
    closing: str,
    answer_check=None,  # answer -> problems, only when `verify_attempt` returned none
    before_commit=None,  # a write between the checks and the checkpoint commit
    after_commit=None,  # a write after the checkpoint commit
    snapshot_findings=None,  # () -> the findings text as it stands right before the model call
    restore_findings=None,  # (text) -> None, put findings.md back after a failed attempt
    tools: dict[str, str] | None = None,  # the `.venv/` digest the verb took before this call, else taken here
) -> None:
    """The attempt loop the work verbs share: call, measure, check, commit - or leave the diagnostics.

    A failed attempt leaves its diagnostics and the files its model changed, quoted, below its audit
    line in `findings.md`; the route block on `stage-1` names the verb. A verb that passes
    `snapshot_findings` and `restore_findings` puts findings.md back as it stood right before the model
    call whenever an attempt fails: the audit line above the snapshot stays, the model's own edits to
    the file - a Status it wrote itself included - go, so no failed run leaves them behind (phase 6,
    F-2).

    The failed-check listing and the changed-file entries pass through `protect_diagnostics` once, on
    every route, the keyless ones included; the block in findings.md and the retry prompt both take that
    one safe text, so a fixture secret a check printed blocks neither the next attempt's leak check nor
    its prompt (bead coding-harness-8hr).

    A completed call keeps its measured time whatever stops the run afterwards: every post-call exit
    - a refusal, an unreadable or moved HEAD, an unstartable or refusing verifier, diagnostic
    protection - passes one finalization boundary that persists the attempt's one rejected entry
    through `persist_time_entry`, then lets the original refusal or failure stand (bead
    coding-harness-9wp). A call that never completed - a `CallFailed` result, an empty Codex answer
    included - gets no entry, as preflight refusals get none.
    """
    root = ctx.root
    allowed = {ctx.findings.relative_to(root)}
    # Build each endpoint's base prompt before any model can edit or delete a dependency. Every
    # builder read goes into the same snapshot, including the phase prompt and repository rules;
    # later attempts append diagnostics to these strings and never read prompt inputs again.
    inputs: dict[Path, bytes] = {}
    prompts = {}
    for endpoint, _, _, _ in routes:
        if endpoint not in prompts:
            prompts[endpoint] = build_prompt([], endpoint, inputs)
    # These optional change inputs are read by the worker rather than inlined in its prompt.
    for name in ("decisions.md", "design.md"):
        path = ctx.folder / name
        if path.is_file():
            prompt_input(path, inputs)
    diagnostics: list[str] = []
    record: list[str] = []
    # The tools the runner itself starts, as they were before the first model ran. One digest for the
    # whole run: an attempt that overwrote a tool is refused, and the refused bytes must not become the
    # next attempt's reference by taking the digest again (P1 of the #188 review).
    tools = tool_state(root) if tools is None else tools
    for attempt, (endpoint, credential, route, reason) in enumerate(routes, 1):
        prompt = prompts[endpoint]
        if diagnostics:
            prompt = "\n\n".join(
                [
                    prompt.removesuffix(f"\n\n{READ_REQUEST}"),
                    "## Earlier post-run diagnostics\n\n" + "\n\n".join(diagnostics),
                    READ_REQUEST,
                ]
            )
        begin_work_call(ctx, verb, endpoint, prompt, attempt, route, ctx.findings, reason)
        if route == "stage-1":
            insert_before_time(
                ctx.plan,
                f"## Runner route — {today()}\n\nStage-1 route: {verb} · model {endpoint[1]} · reason: {reason}.",
            )
        # The pre-call plan, route block and time records included, is what a rejected attempt's plan is
        # restored to (plus the runner's entry), while the accepted plan in every prompt stays the
        # original snapshot.
        baseline_time = ctx.plan.read_text(encoding="utf-8")
        inputs_before = {**inputs, ctx.plan: baseline_time.encode("utf-8")}
        kept = snapshot_findings() if snapshot_findings is not None else None
        findings_before = ctx.findings.read_bytes()
        unmeasured: str | None = None
        try:
            before = worktree_tree(root)
        except (Refused, OSError) as error:
            before, unmeasured = "", str(error)
        call_error: CallFailed | None = None
        answer = ""
        # The runner's own span of this attempt starts right before the model and ends at the verdict.
        # A completed call keeps its measured entry whatever post-call check then stops the run; a
        # call that failed, an empty Codex answer included, never gets one (spec, criterion 6).
        started_wall, started_mono = utc_now(), monotonic_now()
        completed = False
        logged = False
        try:
            # The completion boundary: from here to the verdict, every departure of a completed
            # attempt - the HEAD checks, both scans, verification, the answer check and diagnostic
            # protection included - passes the handler below, which persists the attempt's one
            # rejected entry through the one writer and then lets the original refusal or failure
            # stand. The boundary never starts a model call, a retry or a checkpoint of its own,
            # and never resets HEAD.
            try:
                if endpoint == CODEX:
                    # A fresh writing Codex call, never resumed; its thread is not kept (ADR 0017).
                    answer, _ = run_codex(ctx, prompt, writable=True, verb=verb)
                    if not answer.strip():
                        raise CallFailed("codex: the answer is empty")
                else:
                    answer = run_work_model(ctx, prompt, endpoint, writable=True, key=credential)
            except CallFailed as error:
                call_error = error
            else:
                completed = True
            if endpoint == CODEX:
                try:
                    head_now = _git_output(root, "rev-parse", "HEAD").strip()
                except Refused as error:
                    raise CallFailed(f"the {verb} call's HEAD could not be read ({error})") from error
                if head_now != baseline:
                    # A moved HEAD stops the run without a rewrite: resetting a commit the model made
                    # would rewrite history, and the decision is a person's (ADR 0017). Measure its
                    # files before restoring findings alone, so its own statuses go and the audit stays.
                    problem = (
                        f"the {verb} call moved HEAD from {baseline[:12]} to {head_now[:12]}; "
                        "history was not rewritten and no runner checkpoint was made"
                    )
                    if unmeasured is None:
                        try:
                            moved_files: list[str] | str = attempt_files(root, before, worktree_tree(root))
                        except (Refused, OSError) as error:
                            moved_files = str(error)
                    else:
                        moved_files = unmeasured
                    if kept is not None:
                        restore_findings(kept)
                    listing = f"- {problem}"
                    if call_error is not None:
                        listing += f"\n- {call_error}"
                    append(
                        ctx.findings,
                        quote_block(
                            attempt_block(
                                attempt,
                                route,
                                protect_diagnostics(listing, key),
                                protect_files(moved_files, key),
                                moved_head=True,
                            ),
                            key,
                        ),
                    )
                    raise CallFailed(problem) from call_error
            if call_error is not None:
                error = call_error
                if kept is not None:
                    restore_findings(kept)
                exposed = []
                if key is not None:
                    # Scrub before the snapshot writes the changed files into the object store.
                    exposed = remove_changed_credential(root, key, ignored_before)
                try:
                    saved = save_attempt(root, baseline, ctx.change, f"{verb}-attempt-{attempt}")
                except OSError as save_error:
                    saved = f"saving the attempt failed ({save_error})"
                restored = restore_baseline(root, baseline, allowed, ignored_before)
                leaked = f"; {credential_message(exposed)}" if exposed else ""
                raise CallFailed(f"{error}; {saved}; {restored}{leaked}") from error
            if key is not None:
                # Every route scans with the key read in this run - the Sonnet fallback included - before
                # the second snapshot can write the changed files into the object store (spec, criterion 9).
                exposed = remove_changed_credential(root, key, ignored_before)
                if exposed:
                    if kept is not None:
                        restore_findings(kept)
                    raise Refused(credential_message(exposed))
            if unmeasured is None:
                # Both snapshots stand around the model call alone: the runner's own writes - the audit
                # line, the route block, the preparation, the block below - fall outside both of them.
                try:
                    files: list[str] | str = attempt_files(root, before, worktree_tree(root))
                except (Refused, OSError) as error:
                    files = str(error)
            else:
                files = unmeasured
            cannot_start: CallFailed | None = None
            formatted: list[str] = []
            try:
                problems = verify_attempt(root, ctx.plan, key, formatted, tools)
            except Refused:
                if kept is not None:
                    restore_findings(kept)
                raise
            except CallFailed as error:
                # `make verify` could not be started: no model can repair that, so this attempt's block
                # says why and the run stops after the scan below, with no further attempt (spec, criterion 6).
                if kept is not None:
                    restore_findings(kept)
                cannot_start = error
                lines = protect_diagnostics(str(error), key).splitlines() or ["make could not be started"]
                problems = ["`make verify` could not be run\n" + "\n".join(_shrink(lines, TAIL_LINES))]
            # An unchanged hard-linked plan can escape changed-document preparation. Validate the
            # logging destination independently before deciding the result, even in that case.
            try:
                if ctx.plan.resolve() != root.resolve() / ctx.plan.relative_to(root):
                    raise Refused("refusing an aliased plan destination")
                if ctx.plan.is_symlink() or ctx.plan.stat().st_nlink > 1:
                    raise Refused("refusing an aliased or hard-linked plan destination")
            except (Refused, OSError, RuntimeError) as error:
                problems.append(f"The time entry destination is unsafe or unreadable: {error}")
            try:
                aliased_parent = ctx.plan.parent.resolve() != root.resolve() / ctx.plan.relative_to(root).parent
            except (OSError, RuntimeError):
                aliased_parent = True
            if aliased_parent or not ctx.plan.parent.is_dir():
                # Detach an alias itself, never a document in its target; recreate missing parents too.
                # Restore the snapshotted inputs and audit before diagnostics, logging or retry writes.
                for path, content in {**inputs_before, ctx.findings: findings_before}.items():
                    restore_work_input(root, path, content)
            if not problems and answer_check is not None:
                problems = answer_check(answer)
            if problems:
                # The format line stands first: the step ran before `make verify`, and the next model
                # learns that the runner formats and whether ruff left findings it could not fix.
                problems = [*(f"{FORMAT_LABEL}: {line}" for line in formatted), *problems]
                if kept is not None:
                    # Before the block is appended, so the quoted diagnostics stand beside the rows as
                    # they were, not beside the model's edits of them.
                    restore_findings(kept)
                # The block lands below this attempt's audit line, before the next attempt starts or the
                # run exits 1; the post-run scan after it covers the block too (spec, criteria 1 and 9).
                # One safe listing and one safe file list feed both destinations (the block and the retry prompt).
                listing = protect_diagnostics("\n".join(f"- {p}" for p in problems), key)
                files = protect_files(files, key)
                diagnostics.append(f"Attempt {attempt} ({route}):\n{listing}")
                append(ctx.findings, quote_block(attempt_block(attempt, route, listing, files), key))
            record += [protect_diagnostics(f"- Attempt {attempt} ({route}): {line}", key) for line in formatted]
            exposed = []
            if key is not None:
                # The gate runs repository code the model just edited: scan again after it and the
                # diagnostic block, before finalizing either the verdict or its measured endpoint.
                exposed = remove_changed_credential(root, key, ignored_before)
                if exposed:
                    if kept is not None and not problems:
                        restore_findings(kept)
                    problems.append(credential_message(exposed))
            # The verdict is in: the runner writes the attempt's span, accepted or rejected,
            # through the one writer - so a later refusal cannot meet an inline writer and
            # produce a duplicate. A rejected attempt that will be retried gets its plan back
            # at the pre-call bytes plus this entry, so the restore below keeps the entry and
            # drops the model's other plan edits.
            ended_wall, ended_mono = utc_now(), monotonic_now()
            terminal_failure: Refused | CallFailed | None = None
            if exposed:
                terminal_failure = Refused(credential_message(exposed))
            elif cannot_start is not None:
                terminal_failure = CallFailed(
                    "`make verify` could not be started; why, and the files this attempt changed: "
                    f"{ctx.findings.relative_to(root)}"
                )
                terminal_failure.__cause__ = cannot_start
            logged = True
            persist_time_entry(
                root,
                ctx.plan,
                time_entry(
                    verb,
                    attempt,
                    route,
                    endpoint[1],
                    not problems,
                    started_wall,
                    ended_wall,
                    max(0, round(ended_mono - started_mono)),
                ),
                baseline_time,
                inputs_before,
                accepted=not problems,
                retry=bool(problems) and attempt < len(routes) and cannot_start is None and not exposed,
                original=terminal_failure,
            )
            if terminal_failure is not None:
                raise terminal_failure
            if not problems:
                if before_commit is not None:
                    before_commit()
                message = commit_message
                if record:
                    # The subject stays the subject; the format line of every attempt that ran the step
                    # stands below the heading, in the commit that holds the formatted bytes.
                    message = commit_message + "\n\n" + FORMAT_COMMIT_HEADING + "\n" + "\n".join(record)
                checkpoint(root, ctx.change, baseline, key, ignored_before, message=message, keep=allowed)
                if after_commit is not None:
                    after_commit()
                print(f"{verb}: verified and committed · route {route} · attempt {attempt}")
                return
            if attempt < len(routes):
                # Failed edits stay in the attempt's evidence. Restore every differing snapshotted input
                # before the next attempt, comparing bytes so undecodable files are restored too.
                # The plan comes back at its pre-call bytes plus this attempt's runner entry.
                # Restoration never writes through a worktree path: whatever stands there (a symlink, a
                # directory or a file) is removed without being followed, then the bytes are written anew.
                for path, content in inputs_before.items():
                    restore_work_input(root, path, content)
                stamp_updated(ctx.plan)
        except BaseException as error:
            # Include interrupts: an exceptional departure of a completed attempt logs first,
            # rejected, unless the verdict's own write already ran - and the original refusal
            # or failure then stands as it was. Logging itself failing fails closed, with the
            # attempt's own failure as the cause.
            if completed and not logged:
                ended_wall, ended_mono = utc_now(), monotonic_now()
                persist_time_entry(
                    root,
                    ctx.plan,
                    time_entry(
                        verb,
                        attempt,
                        route,
                        endpoint[1],
                        False,
                        started_wall,
                        ended_wall,
                        max(0, round(ended_mono - started_mono)),
                    ),
                    baseline_time,
                    inputs_before,
                    accepted=False,
                    retry=False,
                    original=error,
                )
            raise
    raise CallFailed(closing)


def implement(root: Path, change: str, stage2_off: str | None = None) -> None:
    """Phase 4: Flash, one Flash repair and Sonnet fallback, checked and committed by the runner."""
    first = SONNET if stage2_off is not None else GLM_FLASH
    ctx = preflight(root, change, first, required=("plan.md",))
    allowed = {ctx.findings.relative_to(root)}
    outside = changed_paths(root) - allowed
    if outside:
        listing = ", ".join(sorted(path.as_posix() for path in outside))
        raise Refused(f"the worktree has pre-existing changes outside this change's findings.md: {listing}")
    baseline = _git_output(root, "rev-parse", "HEAD").strip()
    time_log(ctx.plan)  # Require the initial time heading before a model call starts.
    ignored_before = ignored_snapshot(root)
    if stage2_off is None:
        key = read_secret("GLM_KEY")
        if key is None:
            raise Refused(f"GLM_KEY is not in the secrets file {secrets_path()}.")
        routes = [
            (GLM_FLASH, key, "flash", None),
            (GLM_FLASH, key, "flash-repair", "first Flash post-run check failed"),
            (SONNET, None, "stage-1", "two Flash post-run checks failed"),
        ]
    else:
        key = None
        routes = [(SONNET, None, "stage-1", stage2_off)]
    run_attempts(
        ctx,
        "implement",
        routes,
        lambda diagnostics, _endpoint, inputs: implementation_prompt(ctx, baseline, diagnostics, inputs),
        baseline,
        key,
        ignored_before,
        commit_message=f"feat({change}): implement accepted plan",
        closing=(
            "implementation post-run checks failed after the allowed attempts; why each attempt failed and "
            f"the files it changed: {ctx.findings.relative_to(root)}"
        ),
    )


# ---------------------------------------------------------------------------
# The draft - Codex writes phases 2, 2b and 3
# ---------------------------------------------------------------------------


def draft_prompt(ctx: Context, diagnostics: list[str]) -> str:
    """The spec prompt with the design and plan prompts, the drafting rules and earlier diagnostics."""
    extra = []
    for heading, name in (("## Phase 2b prompt", "02b-design.md"), ("## Phase 3 prompt", "03-plan.md")):
        body = (ctx.root / "prompts" / name).read_text(encoding="utf-8")
        extra.append(f"{heading}\n\n{body.rstrip()}")
    extra.append(DRAFT_RULES.replace("<change>", ctx.change))
    if diagnostics:
        extra.append("## Earlier attempts' diagnostics\n\n" + "\n\n".join(diagnostics))
    return work_prompt(ctx.root, "02-spec.md", ctx.change, "\n\n".join(extra))


def put_back(root: Path, baseline: str, keep: set[Path]) -> list[str]:
    """Put every changed path but `keep` back at the baseline; name what was put back, sorted.

    The same restore and clean as `restore_baseline`, without its ignored-file bookkeeping: a draft's
    leftover is what git sees. A git that refuses is a failed call, not a refusal of this run.
    """
    changed = sorted(changed_paths(root) - keep, key=lambda path: path.as_posix())
    if not changed:
        return []
    spec = [f":(exclude){path.as_posix()}" for path in sorted(keep, key=lambda path: path.as_posix())]
    try:
        _git_output(root, "restore", f"--source={baseline}", "--staged", "--worktree", "--", ".", *spec)
        _git_output(root, "clean", "-fdq", "--", ".", *spec)
    except Refused as error:
        raise CallFailed(f"putting the paths back at {baseline[:12]} failed ({error})") from error
    return changed


def draft_keep(root: Path, ctx: Context, baseline: str) -> tuple[set[Path], list[str]]:
    """What a draft attempt may keep changed, and the new ADR files among what it may not.

    A keep is every changed path under the change folder except its `decisions.md` - the
    maintainer's answers stand there (spec, criterion 9) - plus every changed path that a new ADR
    file is and the merge base of the baseline and `origin/main` does not hold, so the ADR an
    earlier draft of the same change committed stays the one new ADR file a later draft may edit
    (spec, criterion 8, and 2a's F-3). The new ADR files are counted across the whole change -
    against that merge base, what an earlier draft committed included - not only among this
    attempt's changes against HEAD: a second draft that keeps the first ADR and adds another still
    leaves two (2a's F-5).
    """
    prefix = Path("plans") / "changes" / ctx.change
    changed = changed_paths(root)
    keep = {path for path in changed if path.is_relative_to(prefix) and path != prefix / "decisions.md"}
    base = _git_output(root, "merge-base", baseline, "origin/main").strip()
    whole = changed_paths(root, against=base) | changed
    new_adrs: list[str] = []
    for path in sorted(whole - keep, key=lambda path: path.as_posix()):
        posix = path.as_posix()
        if not NEW_ADR.fullmatch(posix):
            continue
        try:
            held = subprocess.run(
                [GIT, "-C", str(root), "cat-file", "-e", f"{base}:{posix}"],
                capture_output=True,
                check=False,
                timeout=GIT_SECONDS,
            )
            present = held.returncode == 0
        except subprocess.TimeoutExpired:
            present = True  # unmeasured reads as present: the path stays a keep
        if not present:
            # Deleting the draft's own unmerged ADR is allowed, so the path stays a keep; only a
            # file that exists now counts, or a rename would read as two new ADRs (F-11).
            keep.add(path)
            if (root / path).exists():
                new_adrs.append(posix)
    return keep, new_adrs


def answer_is_owed(root: Path, change: str) -> bool:
    """Whether `change` is a feature whose ADR answer file does not exist in `root` now."""
    try:
        return any(feature.change == change for feature in check_adr_answers.examine(root).missing)
    except (OSError, ValueError):
        return False


CARD_PROBLEM = "`plan.md` does not open with the plan card (For you:, Done when:, Appetite:, Not now:, Pre-mortem:)"


def card_problem(text: str) -> str | None:
    """Why a plan.md does not open with its card, or None (spec, criterion 15).

    Below the frontmatter, before the first level-two heading, the first fenced block must hold
    lines beginning with the five `CARD_LABELS` in that order.
    """
    body = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    head = re.split(r"^## ", body, maxsplit=1, flags=re.M)[0]
    lines = head.splitlines()
    opening = next((i for i, line in enumerate(lines) if re.match(r"^(```|~~~)", line)), None)
    if opening is None:
        return CARD_PROBLEM
    block = []
    for line in lines[opening + 1 :]:
        if re.match(r"^(```|~~~)", line):
            break
        block.append(line)
    walk = 0
    for label in CARD_LABELS:
        found = next((i for i in range(walk, len(block)) if block[i].startswith(label)), None)
        if found is None:
            return CARD_PROBLEM
        walk = found + 1
    return None


def verify_draft(
    root: Path, ctx: Context, key: str | None, new_adrs: list[str], tools: dict[str, str] | None = None
) -> tuple[list[str], bool]:
    """A draft attempt's post-run checks: the problems, and whether the answer is owed.

    The order is the spec's (criteria 10 to 16): the ADR count, the derived files, `make verify` -
    its exit code decides; the one missing answer it tolerates is the gate's own, asked for through
    `check_adr_answers.TOLERATE_ENV`, never read from its output - the two
    artefacts, the plan card and the `## Time used` heading.
    """
    owed = False
    if len(new_adrs) > 1:
        problems = ["the attempt left more than one new ADR file: " + ", ".join(f"`{path}`" for path in new_adrs)]
        return problems, owed
    tampered = tool_problem(root, tools)
    if tampered:
        return [tampered], owed
    env = runner_env(
        foreign_env(
            {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "commit.gpgsign",
                "GIT_CONFIG_VALUE_0": "false",
                # The one tolerance of a draft is the gate's own, set by this runner alone: with this
                # variable `adr-answers` reports this change's missing answer and passes, so the
                # exit code of `make verify` decides and no output is read (spec, criterion 13; F-9, F-10).
                check_adr_answers.TOLERATE_ENV: ctx.change,
            }
        ),
        root,
    )
    preparation = prepare_derived(root, env, key)
    if preparation:
        return preparation, owed
    try:
        done = launch(
            ["make", "verify"],
            root,
            env,
            timeout=VERIFY_SECONDS,
            limit=f"the runner's step limit after {VERIFY_SECONDS // 60} minutes",
        )
    except CallFailed as error:
        # A make that cannot start is as failed a post-run check as a red one: its diagnostics
        # reach the attempt's block, and the chain moves on to the next attempt (2a's F-7).
        return [f"`make verify` could not run: {error}"], owed
    problems = []
    if done.returncode != 0:
        problems.append(f"`make verify` exited {done.returncode}\n{verify_evidence(done, key)}".rstrip())
    else:
        owed = answer_is_owed(root, ctx.change)
    plan_missing = not ctx.plan.is_file()
    for name in ("spec.md", "plan.md"):
        if not (ctx.folder / name).is_file():
            problems.append(f"plans/changes/{ctx.change}/{name} is missing after the draft.")
    if not plan_missing:
        # An absent plan.md is one problem of its own: the card and Time-used checks would read an
        # empty string and name two faults a missing file cannot have (repair L3-4).
        plan_text = _read_quietly(ctx.plan)
        if card_problem(plan_text) is not None:
            problems.append(CARD_PROBLEM)
        if not TIME_HEADING.search(plan_text):
            problems.append(f"plans/changes/{ctx.change}/plan.md has no `## Time used` heading.")
    return problems, owed


def draft(root: Path, change: str) -> None:
    """Phases 2, 2b and 3: Codex drafts the change; GLM 5.3 after two failed Codex attempts (ADR 0016).

    The guards are `implement`'s - the preflight, the pre-existing-change refusal, the leak check
    before each call, the credential scans, the one commit - plus what a writing Codex call needs:
    each attempt puts back what a draft may not change, and the one red gate a draft tolerates is
    its own missing ADR answer, which only the maintainer can record.
    """
    ctx = preflight(root, change, CODEX, bead_file="research.md", required=("decisions.md",))
    allowed = {ctx.findings.relative_to(root)}
    outside = changed_paths(root) - allowed
    if outside:
        listing = ", ".join(sorted(path.as_posix() for path in outside))
        raise Refused(f"the worktree has pre-existing changes outside this change's findings.md: {listing}")
    baseline = _git_output(root, "rev-parse", "HEAD").strip()
    ignored_before = ignored_snapshot(root)
    tools = tool_state(root)  # before any model runs (R-21)
    routes = [
        (CODEX, "codex", None),
        (CODEX, "codex-repair", "the first draft attempt failed"),
        (GLM, "glm", "two Codex draft attempts failed"),
    ]
    diagnostics: list[str] = []
    for attempt, (endpoint, route, reason) in enumerate(routes, 1):
        key = None
        if endpoint == GLM:
            # The key is read only when the GLM attempt is due (spec, criteria 23 and 24).
            key = read_secret("GLM_KEY")
            if key is None:
                raise Refused(f"GLM_KEY is not in the secrets file {secrets_path()}.")
        prompt = draft_prompt(ctx, diagnostics)
        begin_work_call(ctx, "draft", endpoint, prompt, attempt, route, ctx.findings, reason)
        unmeasured: str | None = None
        try:
            before = worktree_tree(root)
        except (Refused, OSError) as error:
            before, unmeasured = "", str(error)
        call_error: CallFailed | None = None
        try:
            if endpoint == CODEX:
                run_codex(ctx, prompt, writable=True, verb="draft")
            else:
                run_work_model(ctx, prompt, endpoint, writable=True, key=key)
        except CallFailed as error:
            call_error = error
        if key is not None:
            # Before any stop, the moved-HEAD one below included: a call that wrote the key and moved
            # HEAD must not leave the key in the tree and in the model's commit - the runner removes
            # it and refuses (spec, criterion 25). This is also before the second snapshot below can
            # write the changed files into the object store, a dead call included. The comparison is
            # the baseline, not the model's new HEAD: a file the call committed reads as clean
            # against its own commit and must still be found (2a's F-4).
            exposed = remove_changed_credential(root, key, ignored_before, against=baseline)
            if exposed:
                raise Refused(credential_message(exposed))
        try:
            head_now = _git_output(root, "rev-parse", "HEAD").strip()
        except Refused as error:
            raise CallFailed(f"the draft call's HEAD could not be read ({error})") from error
        if head_now != baseline:
            # A moved HEAD stops the run without a rewrite: resetting a commit the model made would
            # rewrite history, and the decision is a person's (spec, criterion 11).
            raise CallFailed(
                f"the draft call moved HEAD from {baseline[:12]} to {head_now[:12]}; nothing was put back or committed"
            )
        if call_error is not None:
            saved = save_attempt(root, baseline, ctx.change, f"draft-attempt-{attempt}")
            put = put_back(root, baseline, allowed)
            listing = f"- the call failed: {call_error}\n- {saved}"
            diagnostics.append(f"Attempt {attempt} ({route}):\n{listing}")
            block = f"Attempt {attempt} ({route}) failed its call: {call_error}\n\n{saved}."
            if put:
                block += "\n\nThe runner put back:\n" + "\n".join(put_back_lines(put))
            append(ctx.findings, quote_block(block, key, put_back_lines(put)))
            continue
        if unmeasured is None:
            # Both snapshots stand around the model call alone: the runner's own writes - the audit
            # line, the block below - fall outside both of them.
            try:
                files: list[str] | str = attempt_files(root, before, worktree_tree(root))
            except (Refused, OSError) as error:
                files = str(error)
        else:
            files = unmeasured
        keep, new_adrs = draft_keep(root, ctx, baseline)
        put = put_back(root, baseline, keep)
        if put:
            restored = protect_files(put_back_lines(put), key)
            listing = "\n".join(restored)
            append(
                ctx.findings,
                quote_block(
                    f"Attempt {attempt} ({route}): the runner put back what a draft may not change:\n{listing}",
                    key,
                    restored,
                ),
            )
        problems, owed = verify_draft(root, ctx, key, new_adrs, tools)
        if problems:
            # The next attempt starts on the tree this one left; the block quotes its files and
            # diagnostics below its audit line (spec, criterion 21).
            listing = protect_diagnostics("\n".join(f"- {problem}" for problem in problems), key)
            files = protect_files(files, key)
            diagnostics.append(f"Attempt {attempt} ({route}):\n{listing}")
            append(ctx.findings, quote_block(attempt_block(attempt, route, listing, files), key))
        if key is not None:
            # The gate runs repository code the model just edited: scan again after it, against the
            # baseline as before (2a's F-4).
            exposed = remove_changed_credential(root, key, ignored_before, against=baseline)
            if exposed:
                raise Refused(credential_message(exposed))
        if not problems:
            if owed:
                append(
                    ctx.findings,
                    f"ADR answer owed: decisions/answers/{ctx.change}/adr.yaml does not exist and the gate "
                    "tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).",
                )
            checkpoint(
                root,
                ctx.change,
                baseline,
                key,
                ignored_before,
                message=f"docs({change}): draft spec and plan — route {route}",
                keep=keep,
            )
            print(f"draft: verified and committed · route {route} · attempt {attempt}")
            return
    raise CallFailed(
        "the draft failed after the allowed attempts; why each attempt failed and the files each changed: "
        f"{ctx.findings.relative_to(root)}"
    )


def repair_prompt(
    ctx: Context,
    baseline: str,
    taken: list[tuple[str, list[str]]],
    diagnostics: list[str],
    endpoint: tuple[str, str, str | None] = CODEX,
    inputs: dict[Path, bytes] | None = None,
) -> str:
    """The implement contract with the repair block: the format, the baseline, the taken rows, the inputs."""
    rows = "\n".join(f"- {row[0]} [{row[1]}, {row[2]}] {row[4]}: {row[5]} — Status: {row[7]}" for _, row in taken)
    spec = prompt_input(ctx.folder / "spec.md", inputs)
    plan = prompt_input(ctx.plan, inputs)
    extra = [
        REPAIR_FORMAT if endpoint == CODEX else REPAIR_FORMAT_FILE_TOOLS,
        f"Repair baseline: {baseline}",
        f"## Taken rows\n\n{rows}",
        f"## Accepted spec\n\n{spec}",
        f"## Accepted plan\n\n{plan}",
    ]
    if diagnostics:
        extra.append("## Earlier post-run diagnostics\n\n" + "\n\n".join(diagnostics))
    return work_prompt(ctx.root, "04-implement.md", ctx.change, "\n\n".join(extra), inputs)


def repair(root: Path, change: str, stage2_off: str | None = None) -> None:
    """Phase 4b and 6: Codex repairs every taken finding in one call, checked and committed by the runner.

    The attempts are Codex, one fresh Codex repair attempt with the first one's diagnostics, and one
    Sonnet 5.5 stage-1 fallback after two failed post-run checks; a failed call or a leak-check BLOCK
    stops without a fallback (ADR 0017). The orchestrator decides taken or rejected and re-checks with
    the loop's next round and `review`, a fresh read-only Codex session; the verb writes no
    `Broke a test` and starts no review. A taken Status that already names a fix in the old hand-written
    form (`; fixed by`, `; fixed:`, `; repaired by`) refuses before any call.
    """
    first = SONNET if stage2_off is not None else CODEX
    ctx = preflight(root, change, first, required=("plan.md",))
    allowed = {ctx.findings.relative_to(root)}
    outside = changed_paths(root) - allowed
    if outside:
        listing = ", ".join(sorted(path.as_posix() for path in outside))
        raise Refused(f"the worktree has pre-existing changes outside this change's findings.md: {listing}")
    taken, waiting = repair_targets(ctx, read_record(change, root))
    if waiting:
        raise Refused(f"rows are waiting for a decision ({', '.join(waiting)}); decide them first.")
    if not taken:
        raise Refused("no row is taken; nothing to repair.")
    ids = [row[0] for _, row in taken]
    doubled = sorted({ident for ident in ids if ids.count(ident) > 1})
    if doubled:
        raise Refused(f"several taken rows carry the same id ({', '.join(doubled)}); mend the rows first.")
    legacy = [row[0] for _, row in taken if legacy_completed(row[7])]
    if legacy:
        # A legacy marker may name a completed fix or merely occur in an unrepaired reason.
        # Refuse without rewriting and explain both corrections (spec, criterion 7).
        raise Refused(
            f"rows carry a taken status that already names a fix ({', '.join(legacy)}); book the hand repair "
            "by replacing the Status with `fixed — tests/<path>::<function>` or "
            "`fixed — not a test — <reason>` and setting the loop row's `Broke a test` mark, then run "
            "repair again; if the row is not repaired yet, reword its reason so it names no fix instead "
            "of marking it fixed."
        )
    baseline = _git_output(root, "rev-parse", "HEAD").strip()
    time_log(ctx.plan)  # Require the initial time heading before a model call starts.
    ignored_before = ignored_snapshot(root)
    # No route reads the GLM credential: the repair is Codex, then Sonnet (ADR 0017).
    key = None
    if stage2_off is None:
        routes = [
            (CODEX, None, "codex", None),
            (CODEX, None, "codex-repair", "first Codex post-run check failed"),
            (SONNET, None, "stage-1", "two Codex post-run checks failed"),
        ]
    else:
        routes = [(SONNET, None, "stage-1", stage2_off)]
    fixes: dict[str, str] = {}
    marks: dict[str, str] = {}
    rows_before = findings_rows(ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else "")
    standing: dict[str, str] = {}
    tools = tool_state(root)  # before any model runs; the answer check and the attempts share it (R-21)

    def snapshot() -> str:
        text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
        standing["text"] = text
        return text

    def check(answer: str) -> list[str]:
        # The last audit line of the snapshot is this attempt's own: it was appended just before it.
        audits = [line for line in standing.get("text", "").splitlines() if line.startswith("Stage-2 call,")]
        found, proven, problems = check_repair_answer(
            ctx, answer, taken, baseline, key, rows_before, audits[-1] if audits else None, standing["text"], tools
        )
        if not problems:
            fixes.clear()
            fixes.update(found)
            marks.clear()
            marks.update(proven)
        return problems

    run_attempts(
        ctx,
        "repair",
        routes,
        lambda diagnostics, endpoint, inputs: repair_prompt(ctx, baseline, taken, diagnostics, endpoint, inputs),
        baseline,
        key,
        ignored_before,
        commit_message=f"fix({change}): repair taken findings {', '.join(ids)}",
        closing=(
            "repair post-run checks failed after the allowed attempts; why each attempt failed and "
            f"the files it changed: {ctx.findings.relative_to(root)}"
        ),
        answer_check=check,
        before_commit=lambda: mark_repaired_findings(ctx, taken, fixes),
        after_commit=lambda: mark_repaired_record(change, taken, fixes, root, marks),
        snapshot_findings=snapshot,
        restore_findings=lambda text: ctx.findings.write_text(text, encoding="utf-8"),
        tools=tools,
    )


def prepare_loop(root: Path, change: str) -> None:
    """Check reachable admitted reviewers and return the main-conversation report."""
    import stage2_availability

    stage2_availability.prepare(root, change, sys.modules[__name__])


def review_loop(root: Path, change: str, availability_reported: str | None = None) -> None:
    """One round of phase 4b, until a round is clean (ADR 0021).

    A fresh run discovers its free members through a forced live refresh and
    pins the stage snapshot; every later call takes the run's next unconsumed
    stage. The stops come before any stage: undecided or evidence-incomplete
    rows first, then a clean previous round, then the repair brake (two
    consecutive rounds whose accepted findings all begin `fix-r`), then spent
    stages - each naming the round or the maintainer, and none reset by a
    release or an edited configuration (ADR 0021, decision 9). One call
    completes one round; a swarm's members run concurrently and merge into one
    heading and one id series; an attempt whose every member failed completes
    no round and consumes no stage.
    """
    record = read_record(change, root)
    if record is not None:
        refusal = undecided_refusal(record_rows(record), "decide them first")
        if refusal:
            raise Refused(refusal)
    findings_text = ""
    findings_path = folder_of(root, change) / "findings.md"
    if findings_path.exists():
        findings_text = findings_path.read_text(encoding="utf-8")
    # After a maintainer's restart the stops read only the rounds that followed it (restart amendment).
    floor = restart_floor(findings_text)
    history = {number: rows for number, rows in history_rounds(record, findings_text).items() if number > floor}
    # A round that found nothing has a heading but no row: it is counted by its heading.
    last = max(max(history, default=0), rounds_run(record, findings_text))
    if last > floor:
        refusal = undecided_refusal(history.get(last, []), "decide them first")
        if refusal:
            raise Refused(refusal)
        if clean_round(history.get(last, []), last) and not round_was_cut(record, last, findings_text):
            raise CleanStop(f"round {last} was clean: every row was decided and none accepted; the loop stops.")
        if (
            last in history
            and last - 1 in history
            and fix_r_only(history[last], last)
            and fix_r_only(history[last - 1], last - 1)
        ):
            raise Refused(
                f"rounds {last - 1} and {last} accepted only findings whose Origin begins `fix-r`; "
                "the repair brake stops the loop; the maintainer decides what continues."
            )
    state = None if restarted_fresh(record, findings_text) else read_state(record, findings_text)
    receipt_taken = False
    if record is None and state is None:
        # A fresh run has neither a record nor a released snapshot. read_state
        # refuses a pre-swarm record without its Loop state line.
        problem = entry_problem(root, OPENCODE)
        if problem:
            raise Refused(problem)
        import stage2_availability

        if stage2_availability.settings(root, sys.modules[__name__]) is not None:
            state = stage2_availability.consume(root, change, availability_reported, sys.modules[__name__])
            receipt_taken = True
            require_pi()
        else:
            require_pi()
            state = new_state(root, discover_free(root))
        skipped = skipped_models(root)
        if skipped:
            print(f"review-loop: paid models skipped: {'; '.join(skipped)}")
        # The snapshot is written only with the first completed round: a failed
        # attempt consumes no stage and leaves no record (ADR 0021, decision 6).
    stage = next_stage(state)
    free_input = None
    if stage is not None and stage["kind"] == "free":
        free_input = free_diff(root)
        if not free_input.strip():
            state["free"]["skipped"] = "free stage skipped: no implementation source diff"
            print(f"review-loop: {state['free']['skipped']}")
            stage = next_stage(state)
    if stage is None:
        raise Refused(
            "every stage of this run is consumed and the last round was not clean; the loop stops and "
            "reports to the maintainer. No model is substituted."
        )
    round_number = rounds_run(record, findings_text) + 1
    members: list[str] = stage["members"]
    free = stage["kind"] == "free"
    cut_note: str | None = None
    if free:
        diff, cut_note = bounded_review_diff(free_input)
    else:
        diff, cut_note = bounded_review_diff(change_diff(root))
    body = "" if free else (root / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8")
    prompts: dict[str, str] = {}
    endpoints: dict[str, tuple[str, str, str]] = {}

    def prompt_for(member: str) -> str:
        head = f"This is round {round_number}; you are `{member}`."
        if free:
            return "\n\n".join([FREE_REVIEW_BODY, head, ANSWER_FORMAT, f"## The implementation diff\n\n{diff}"])
        # The request comes before the diff and again after it: a long diff would bury it.
        return "\n\n".join([body.rstrip(), head, ANSWER_FORMAT, READ_REQUEST, f"## The diff\n\n{diff}", READ_REQUEST])

    for member in members:
        endpoints[member] = (OPENCODE, member, "max")
        prompts[member] = prompt_for(member)
    ctx = preflight(root, change, endpoints[members[0]], admission_problem=_free_admission(free, state))
    ctx.models_store = state["free"].get("models_store")
    # Every member is checked in the parent before any starts; one BLOCK aborts
    # the round without a fallback (criterion 3).
    checked = {
        member: checked_prompt(ctx, endpoints[member], prompts[member], _free_admission(free, state))
        for member in members
    }
    if not ctx.findings.exists():
        ctx.findings.write_text(findings_header(ctx, producer_for(endpoints[members[0]])), encoding="utf-8")
    for member in members:
        append(ctx.findings, call_line("review-loop", endpoints[member], checked[member]))
    key = reviewer_key()
    notes: list[str] = []
    if not state["consumed"]:
        if state["free"].get("skipped"):
            notes.append(f"Notice: {state['free']['skipped']}.")
        skipped = skipped_models(root)
        if skipped:
            notes.append(f"Notice: paid models skipped: {'; '.join(skipped)}.")
        gap = unread_catalog_ids(endpoint_entry(root), state["free"])
        if gap:
            notes.append(f"Notice: in the live catalog without a terms reading: {', '.join(gap)}.")
            print(f"review-loop: {notes[-1]}", file=sys.stderr)
    if not free and not any(key == "flash" or key.startswith("rung:") for key in state["consumed"]):
        entry = endpoint_entry(root)
        if stage["kind"] == "paid-swarm":
            notice = cheapest_notice(entry, state["paid"]["ladder"], members)
            if notice:
                notes.append(f"Notice: {notice}.")
        missing = unvalued_models(entry, state["paid"]["ladder"])
        if missing:
            notes.append(f"Notice: no anfragen_5h declared, ordered last: {', '.join(missing)}.")
        for note in notes:
            print(f"review-loop: {note}", file=sys.stderr)
    # One deadline for the round: a replacement must live inside it, or a round could take a member
    # limit per call (R-8 of the review-swarm review).
    deadline = time.monotonic() + REVIEWER_MINUTES * 60
    answers = run_swarm(ctx, members, prompts, key, free=free, deadline=deadline)
    replaced: list[str] = []
    if stage["kind"] == "paid-swarm":
        # A failed Flash member is replaced by the cheapest admitted ladder model
        # not in this round and not consumed, on the same paid prompt; each model
        # at most once, until one answers or the ladder is spent (Q-13).
        used = set(members)
        spent = {key_[len("rung:") :] for key_ in state["consumed"] if key_.startswith("rung:")}
        reasons: dict[str, str] = {}
        for member in list(members):
            current = member
            while isinstance(answers[current], BaseException):
                reasons[current] = str(answers[current])
                if time.monotonic() >= deadline:
                    notes.append(
                        f"{current} failed: {reasons[current]}; the round time limit expired; no replacement starts"
                    )
                    print(f"review-loop: {notes[-1]}", file=sys.stderr)
                    break
                options = [m for m in state["paid"]["rungs"] if m not in used and m not in spent]
                if not options:
                    notes.append(f"{current} failed: {reasons[current]}; no replacement is left on the ladder")
                    print(f"review-loop: {notes[-1]}", file=sys.stderr)
                    break
                nxt = options[0]
                used.add(nxt)
                notes.append(f"{current} failed: {reasons[current]}; replaced by {nxt}")
                print(f"review-loop: {notes[-1]}", file=sys.stderr)
                endpoints[nxt] = (OPENCODE, nxt, "max")
                prompts[nxt] = prompt_for(nxt)
                checked[nxt] = checked_prompt(ctx, endpoints[nxt], prompts[nxt], None)
                append(ctx.findings, call_line("review-loop", endpoints[nxt], checked[nxt]))
                answers.update(run_swarm(ctx, [nxt], prompts, key, free=False, deadline=deadline))
                replaced.append(nxt)
                current = nxt
        members = [*members, *replaced]
    succeeded = [member for member in members if not isinstance(answers[member], BaseException)]
    if not succeeded:
        raise CallFailed("; ".join(f"{member} failed: {answers[member]}" for member in members))
    numbered: list[list[str]] = []
    statements: list[str] = []
    reviewer_blocks: list[str] = []
    for member in members:
        outcome = answers[member]
        if isinstance(outcome, BaseException):
            # A replaced member's failure is already stated with its replacement.
            if stage["kind"] != "paid-swarm":
                statements.append(f"{member} failed: {outcome}")
            continue
        widened: list[str] = []
        rows, rest = parse_rows(outcome, notes=widened)
        member_rows = []
        for row in rows:
            ident = f"L{round_number}-{len(numbered) + 1}"
            numbered.append([ident, *row[1:], member, "", ""])
            member_rows.append(numbered[-1])
        if rows:
            statements.append(render_table(ROW_COLUMNS, member_rows))
            if widened:
                # A row that needed the widening may have been widened by an unescaped `|` before the
                # finding: the row is kept as it came, and the round says that its columns may have moved
                # (R-25 of the review-swarm review).
                statements.append(
                    f"{member} wrote {len(widened)} row(s) with more than six cells; the cells after the "
                    "fifth were joined into the finding, so an unescaped `|` before it moves the columns."
                )
        elif any(split_row(line) is not None for line in rest.splitlines()):
            statements.append(
                f"{member} answered in table lines that are not six-cell rows; they are kept as they came."
            )
        else:
            statements.append(f"{member} reported no finding.")
        # An answer with no row is kept whole, blank lines included; beside rows, what is not a row.
        kept = rest if rows else outcome
        if kept.strip():
            reviewer_blocks.append(kept.strip())
    if cut_note:
        statements.append(
            f"{CUT_LINE} {cut_note}. A clean answer over a cut diff does not end the loop; the rest of "
            "the change needs a round of its own."
        )
    parts = [f"## Round {round_number} — {', '.join(members)}, {today()}", *notes, *statements]
    for block in reviewer_blocks:
        parts.append(f"{NOT_ROWS_NOTE}\n\n{quote_reviewer(block)}")
    path = record_dir(change, root) / "loop.md"
    if record is None:
        # A continued run after a release starts a fresh record; write_state
        # puts the run's snapshot line into it before the rounds.
        write_state(change, state, root)
    # A replacement is consumed too: it is no later rung. Both land in the same write as the round.
    state["consumed"] = [*state["consumed"], *(f"rung:{model}" for model in replaced), stage["key"]]
    write_round(change, "\n\n".join(parts), state, root)
    if receipt_taken:
        import stage2_availability

        stage2_availability.spend(root, change, sys.modules[__name__])
    print(
        f"review-loop: round {round_number} written to {path}: {len(numbered)} rows "
        f"from {len(succeeded)} of {len(members)} members"
    )


def _free_admission(free: bool, state: dict) -> Callable[[Path, str], str | None] | None:
    """The free class's admission check, or None for the paid stages' strict declaration."""
    if not free:
        return None
    return lambda root_, model: free_admission_problem(root_, model, state["free"]["selected"])


def probe(root: Path, change: str) -> None:
    """The compatibility probe: every discovered free member and every eligible paid model, once each.

    Declared special run of phase 4 (the Definition of Done): the calls measure
    whether OpenCode Go's chat-completions address
    (`https://opencode.ai/zen/go/v1/chat/completions`, the one Pi's built-in
    provider calls) accepts the ids. The pinned Pi is checked once before the
    first call; the free members come from a forced live refresh and its
    listing, and each free call runs through the free path - no tools, the
    implementation diff as its only content - while every paid call keeps the
    read tools. No record is written; each id and the answer's first line are
    printed for the pull request body, and skipped paid models are named. A
    failed member is reported without stopping later checks; the final summary
    lists answered and failed members and any failure makes the probe exit
    nonzero (spec, criterion 14). No second address, no substituted model.
    """
    folder_of(root, change)
    key = reviewer_key()
    problem = entry_problem(root, OPENCODE)
    if problem:
        raise Refused(problem)
    require_pi()
    free = discover_free(root, allow_empty=True)
    discovery = free
    diff = free_diff(root)
    if not free["selected"]:
        # The probe measures the ids the declaration admits; a free rule that selects nothing is a
        # finding about the catalog, not a reason to skip the paid ids (R-27 of the review-swarm review).
        print("probe: free stage skipped: the live catalog holds no model for the free rule")
    answered: list[str] = []
    failed: list[str] = []

    def check_member(ctx: Context, model: str, prompt: str, *, free: bool = False) -> None:
        # Declaration and leak checks stay outside this handler: only a model
        # call failure permits continuing, never a failed admission check.
        ctx.models_store = discovery.get("models_store")
        try:
            answer = run_reviewer(ctx, model, prompt, key, free=free)
        except CallFailed as error:
            print(f"probe: {model} failed: {scrub(str(error), key)}")
            failed.append(model)
            return
        first = answer.strip().splitlines()[0]
        print(f"probe: {model} · {scrub(first, key)}")
        answered.append(model)

    if not diff.strip():
        print("probe: free stage skipped: no implementation source diff")
    for model in free["selected"] if diff.strip() else []:
        endpoint = (OPENCODE, model, "max")
        ctx = preflight(root, change, endpoint, admission_problem=_free_admission(True, {"free": free}))
        prompt = "\n\n".join(
            [
                "Compatibility probe of this repository's stage-2 runner, free class. Answer in one short "
                "line: name the model id you answer as.",
                f"You are `{model}`.",
                ANSWER_FORMAT,
                f"## The implementation diff\n\n{diff}",
            ]
        )
        result = checked_prompt(ctx, endpoint, prompt, _free_admission(True, {"free": free}))
        if not ctx.findings.exists():
            ctx.findings.write_text(findings_header(ctx, producer_for(endpoint)), encoding="utf-8")
        append(ctx.findings, call_line("probe", endpoint, result))
        check_member(ctx, model, prompt, free=True)
    for model in ladder(root):
        endpoint = (OPENCODE, model, "max")
        ctx = preflight(root, change, endpoint)
        prompt = "\n\n".join(
            [
                "Compatibility probe of this repository's stage-2 runner. Answer in one short line: "
                "name the model id you answer as.",
                READ_REQUEST,
            ]
        )
        begin_call(ctx, "probe", endpoint, prompt)
        check_member(ctx, model, prompt)
    skipped = skipped_models(root)
    if skipped:
        print(f"probe: paid models skipped: {'; '.join(skipped)}")
    print(f"probe: {len(answered)} members answered: {', '.join(answered) or 'none'}")
    print(f"probe: {len(failed)} members failed: {', '.join(failed) or 'none'}")
    if failed:
        raise CallFailed(f"probe: {len(failed)} members failed: {', '.join(failed)}")


# ---------------------------------------------------------------------------
# The ask rule on `codex`, and the entry point
# ---------------------------------------------------------------------------


def codex_rule_problems(settings: dict) -> list[str]:
    """What keeps Claude Code from asking before a bare `codex`; empty when it asks."""
    permissions = settings.get("permissions") or {}
    rule, reason = CODEX_ASK_RULE
    found = []
    if rule not in (permissions.get("ask") or []):
        found.append(f".claude/settings.json lacks the ask rule {rule} - {reason}")
    for kind in ("deny", "allow"):
        for other in permissions.get(kind) or []:
            if merge_guard.covers(other, "Bash(codex exec x)"):
                found.append(f".claude/settings.json has the {kind} rule {other}, which covers a bare codex call")
    return found


def session(root: Path, change: str, model: str | None, handover: str | None) -> None:
    """One checked interactive session in the change's own Terminal window."""
    import stage2_session

    stage2_session.run(root, change, model or "", handover, sys.modules[__name__])


VERBS = {
    "explore": explore,
    "draft": draft,
    "implement": implement,
    "repair": repair,
    "spec-review": spec_review,
    "review-loop": review_loop,
    "release-loop": release_loop,
    "review": review,
    "probe": probe,
    "prepare-loop": prepare_loop,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument("verb", choices=sorted([*VERBS, "session"]))
    parser.add_argument("change", nargs="?", default="", help="folder name under plans/changes/")
    parser.add_argument(
        "--stage2-off",
        nargs="?",
        const="stage 2 disabled by caller",
        default=None,
        metavar="REASON",
        help="use the Stage-1 route for explore, implement or repair and record the optional reason",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="session only: the model id, exactly as model-endpoints.yaml lists it",
    )
    parser.add_argument(
        "--handover",
        default=None,
        help="session only: a handover file inside the worktree (default: the change's handover.md)",
    )
    parser.add_argument(
        "--stage-failed",
        default=None,
        metavar="MODEL",
        help="release-loop only: retire the stage this model belongs to, so the loop can go on",
    )
    parser.add_argument(
        "--reason",
        default=None,
        metavar="TEXT",
        help="release-loop only: why the stage is retired or the loop restarted; lands in the record",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="release-loop only, on the maintainer's request: restart a completed loop as a fresh run",
    )
    parser.add_argument("--root", default=str(REPO_ROOT), help=argparse.SUPPRESS)
    parser.add_argument(
        "--availability-reported",
        default=None,
        help="review-loop only: report id printed by prepare-loop after its selection was shown in the main conversation",
    )
    args = parser.parse_args(argv)
    try:
        if (
            args.stage2_off is not None
            and not args.change
            and (Path(args.root) / "plans" / "changes" / args.stage2_off).is_dir()
        ):
            raise Refused(
                f"the change name `{args.stage2_off}` was taken as the --stage2-off reason; "
                "put the change before the flag or write --stage2-off=REASON."
            )
        if args.stage2_off is not None and args.verb not in {"explore", "implement", "repair"}:
            raise Refused("--stage2-off applies only to explore, implement and repair.")
        if args.availability_reported is not None and args.verb != "review-loop":
            raise Refused("--availability-reported belongs to review-loop alone.")
        refuse_repository_git(Path(args.root))
        if (args.stage_failed is not None or args.reason is not None or args.restart) and args.verb != "release-loop":
            raise Refused("--stage-failed, --restart and --reason belong to release-loop alone.")
        if args.verb == "session":
            if not args.model:
                raise Refused("session needs --model <id>: name the model exactly as model-endpoints.yaml lists it.")
        elif args.model is not None or args.handover is not None:
            raise Refused("--model and --handover belong to the session verb alone.")
        if args.verb in {"explore", "implement", "repair"}:
            VERBS[args.verb](Path(args.root), args.change, args.stage2_off)
        elif args.verb == "session":
            session(Path(args.root), args.change, args.model, args.handover)
        elif args.verb == "review-loop":
            # The four verbs that own the loop record hold it for their whole run (R-14): review
            # reads it and releases it too (bead coding-harness-751).
            with holding_record(args.change, Path(args.root)):
                review_loop(Path(args.root), args.change, args.availability_reported)
        elif args.verb == "release-loop":
            with holding_record(args.change, Path(args.root)):
                release_loop(Path(args.root), args.change, args.stage_failed, args.reason, args.restart)
        elif args.verb == "prepare-loop":
            with holding_record(args.change, Path(args.root)):
                VERBS[args.verb](Path(args.root), args.change)
        elif args.verb == "review":
            folder_of(Path(args.root), args.change)
            # The verdict reads the record and its release removes it, so review owns the record's
            # lock from its first read through the release (R-14, bead coding-harness-751).
            with holding_record(args.change, Path(args.root)):
                review(Path(args.root), args.change)
        else:
            VERBS[args.verb](Path(args.root), args.change)
    except CleanStop as error:
        # A finished loop is not a refusal: its own exit code, and no `refused:` on stderr.
        print(f"the loop is finished: {error}", file=sys.stderr)
        return CLEAN_CODE
    except Refused as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    except CallFailed as error:
        # A call that failed names its cause on standard error (spec, criterion 14):
        # a round that did not review must say so where the caller reads it.
        print(f"failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
