#!/usr/bin/env python3
"""stage2.py - the one way this repository starts a foreign model.

**What this is.** Stage 2 lets a reviewer from another vendor read framework
content: the review loop (4b) runs on OpenCode Go through Pi, at the one
address the `model-endpoints.yaml` record admits (`stage2_go`), until a round
is clean - a
discovered free-model swarm first, the declared Flash swarm next, then one
declared paid model per round (ADR 0021); Codex drafts the spec, the design
and the plan (2, 2b and 3; GLM 5.3 after two failed Codex attempts) and
reviews the change (6); Opus 5.5 reviews the spec (2a); GLM 5.3 Flash
implements (phase 4) and explores (phase 1) a `bounded` change or a `spike`,
while a `feature` or `architectural` change explores through the research
swarm (ADR 0020 draft: a finder trio maps the sources; three repository
seats cover topics 1–8, three online seats plus selected Go free models
cover topics 9–11; fresh tool-free Opus 5.5 reconciles all eleven topics).
A declaration in `model-endpoints.yaml` stops nothing; this runner stands
between the rule and the call.

    python3 scripts/stage2.py prepare-explore <change> # report seat and free-model availability before phase 1
    python3 scripts/stage2.py explore      <change>   # the swarm or GLM Flash by class, phase 1
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
outside the change folder. The swarm's free researcher contexts are a
different route: fresh scratch working directory, home and agent directory,
every discovery surface off, only the runner-owned research-tools extension
loaded, and no repository path in play - the offline capture on the pinned Pi
with synthetic private canaries, not this suite, is their isolation evidence
(ADR 0020 draft).

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
import ast
import contextlib
import contextvars
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
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_adr_answers  # noqa: E402
import check_criterion_ledger  # noqa: E402
import check_frontmatter_current  # noqa: E402
import leakcheck  # noqa: E402
import merge_guard  # noqa: E402
import stage2_go  # noqa: E402
import verify_lock  # noqa: E402

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
# The change classes (check_interview_minimums.py's vocabulary). Explore routes on
# one: the swarm for the two large classes, the single explorer for the two small
# ones (ADR 0020 draft). Stated before the spec exists - explore-only `--class`
# or the headers of `research.md` and `spec.md` - and every available statement must agree.
CLASSES = ("spike", "bounded", "feature", "architectural")
SWARM_CLASSES = ("feature", "architectural")
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
# The asked-again call after a malformed answer (bead coding-harness-70rw): the
# sentence names what went wrong, the format instruction follows it again.
FORMAT_REMINDER = (
    "Your previous answer was not in the required format, so it could not be read as findings; answer once more."
)
MARK_FORMAT = "For each loop row answer one line and nothing else: `<ID>: agree` or `<ID>: disagree — <reason>`."
REPAIR_ANSWER = (
    "Answer with one fixed line per taken row: `<ID>: fixed — tests/<path>::<function>` or\n"
    "`<ID>: fixed — not a test — <reason>`. Headings, fences and report prose around the fixed lines are\n"
    "ignored, but a colon line whose id looks like a finding id (`L1-2`, `F-12`) and names no taken row\n"
    "still fails. Letters-hyphen-digits ids count only for prefixes used by this change's row ids;\n"
    "`L<digits>-<digits>` always counts; the prefix `L` counts only when the change has a loop row.\n"
    "A colon line whose right side is a fixed status (`fixed — …`) also fails when its id names no\n"
    "taken row, whatever the id's shape. A taken row takes exactly one distinct fixed line: a repeated\n"
    "identical line counts once, and two different fixed lines for one row fail the attempt, so give\n"
    "each row's status once and leave the rest of the report as prose. Write a `|` inside a reason as `\\|`.\n"
    "A code row needs a test that fails on the\n"
    "baseline's code, which the runner runs; only a row taken as `taken — not a test — <reason>` may be\n"
    "answered `not a test`. Do not edit `findings.md`; findings.md is the runner's audit file, and an\n"
    "edit of it is restored before the checks, so the edit alone never fails the attempt. A hand repair\n"
    "is booked in the row's own Status as\n"
    "one of the two fixed statuses above; a Status that still begins `taken` while naming a fix\n"
    "(`; fixed by …`, `; fixed: …`, `; repaired by …`) refuses the repair before any call.\n"
    "Backtick-quoted markers do not count; an unquoted marker beside a backtick span still refuses the repair.\n"
    "The runner keeps every attempt's complete answer as protected local evidence and names the file in\n"
    "the attempt's diagnostics, where a rejected answer can be read again."
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
# The release block's own line: the digest of the record it released. A release-loop whose record has
# the digest of the last released block appends nothing again (DL-A-3 of the deep review).
RELEASE_END = "<!-- End of released loop record -->"
DIGEST_KEY = "Record digest: "
DIGEST_LINE = re.compile(r"^Record digest: (sha256:[0-9a-f]{64})[ \t]*$", re.M)
# The runner's line before every review-loop member call, and its line after a review-loop call that
# wrote such lines and then no round. A no-round marker accounts only for that attempt's call count;
# any other call after the last release/restart needs its record (DL-A-6 of the deep review).
LOOP_AUDIT_LINE = re.compile(r"^Stage-2 call, \d{4}-\d{2}-\d{2}: review-loop · ", re.M)
NO_ROUND_KEY = "Loop attempt: "
NO_ROUND_LINE = re.compile(r"^Loop attempt: \d{4}-\d{2}-\d{2} — no round was written\b", re.M)
# Bounds of a failed attempt's block: a gate line and a file entry keep their first characters…
QUOTE_LINE_CHARS = 500
# …and the file list keeps its first entries (spec, criteria 13 and 14).
ATTEMPT_FILES = 40
LOOP_ID = re.compile(r"L\d+-\d+")
# Non-loop finding shapes count only for prefixes already used by the change's rows.
# Loop identifiers always count; an unrelated colon label remains report prose.
FINDING_ID = re.compile(r"([A-Za-z]+)-[0-9]+")
NOT_ROWS_NOTE = "The answer was not only six-cell rows; what is not one is kept below as it came."
# The runner's line before a member's kept words, naming the member (DL-B-3 of the loop's deep review).
FROM_LINE = re.compile(r"From [A-Za-z0-9][A-Za-z0-9._:/-]*:")
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
wrappers, the expected-result markers and whether a failing call raised an AssertionError or
pytest's own failed outcome -, the collection failures and the session's completion and exit status.
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
            "pytest_failed": bool(report.failed and isinstance(raised, pytest.fail.Exception)),
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

    def __init__(self, message: str, *, partial_answer: str = "", receipts_text: str = "") -> None:
        super().__init__(message)
        self.partial_answer = partial_answer
        self.receipts_text = receipts_text


class NotStarted(CallFailed):
    """A reviewer that never started: the round's deadline had passed before its launch (DL-B-10)."""


class CheckpointRolledBack(CallFailed):
    """The commit guard refused the attempt and ran its baseline restore."""


class RestorationRefused(Refused):
    """A recovery would act through a parent outside the worktree, or one that cannot be resolved.

    The maintainer's decided stop (bead coding-harness-10w): the recovery batch stays unwritten,
    no other attempt, fallback model or checkpoint follows, and time or findings are not persisted
    after it - the explicit exception to ordinary time persistence. `main` reports it on standard
    error, exit 2, except that a propagating model-call failure remains visible and keeps
    its own exit code.
    """

    exit_code = 2


class StepTimedOut(CallFailed):
    """A started program ran into its time limit and its whole process group was killed (R-20)."""


class MalformedAnswer(CallFailed):
    """A review answer with no six-cell row that is not exactly `No finding.`; it carries the answer.

    The swarm's member fails with it as today, and the round asks the member once
    more with the format reminder (bead coding-harness-70rw); the answer rides
    along so the record can quote the first attempt. The phase-6 verdict check
    keeps its plain `CallFailed` - a malformed verdict is out of scope.
    """

    def __init__(self, answer: str) -> None:
        empty = "the answer is empty; " if not answer.strip() else ""
        super().__init__(f"malformed finding output: {empty}expected six-cell findings or exactly 'No finding.'")
        self.answer = answer


def today() -> str:
    return dt.date.today().isoformat()


# ---------------------------------------------------------------------------
# Secrets, environment, the foreign call
# ---------------------------------------------------------------------------


def secrets_path() -> Path:
    """The secrets file. Read at call time, never at import."""
    named = os.environ.get("CC_SECRETS")
    return Path(named) if named else Path.home() / ".config" / "cc-routing" / "secrets.env"


def _secret_entries() -> list[tuple[str, str]]:
    """The (name, value) pairs of the secrets file, in file order: `KEY=value` or `export KEY=value`, quotes stripped, nothing evaluated."""
    try:
        text = secrets_path().read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    entries = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        key, sep, value = line.partition("=")
        if sep:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            entries.append((key.strip(), value))
    return entries


def read_secret(name: str) -> str | None:
    """`KEY=value` or `export KEY=value`, quotes stripped, nothing evaluated."""
    for key, value in _secret_entries():
        if key == name:
            return value or None
    return None


# Credential-named entries are scrubbed whatever their length; other values must be long
# enough to distinguish them from ordinary flags (DL-B-4 of the loop's deep review).
CREDENTIAL_NAME = re.compile(
    r"(?:^|_)(?:AUTH|APIKEY|API_KEY|BEARER|PASS|PAT|KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIALS?)(?:_|$)",
    re.I,
)


def secret_values() -> list[str]:
    """Credentials longest first: credential-named entries, and every value of FRAGMENT or more characters.

    Short values under other names (flags such as `OTHER=1`) would replace ordinary text.
    """
    values = {
        value for key, value in _secret_entries() if value and (CREDENTIAL_NAME.search(key) or len(value) >= FRAGMENT)
    }
    return sorted(values, key=lambda value: (-len(value), value))


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


def scrub(text: str, secret: str | list[str] | tuple[str, ...] | None) -> str:
    """Replace the credential, whole or in any fragment of 8 or more characters, in everything printed or written.

    `secret` may be several credentials (`secret_values()`): each is replaced in turn.
    """
    for one in [secret] if isinstance(secret, str) else secret or []:
        if one:
            text = replace_credential(text, one)
    return text


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


# The process groups of the timed programs running now: an interrupted or terminated runner kills
# them before it exits, because their own sessions keep a terminal's Ctrl-C from reaching them
# (DL-B-5 of the loop's deep review).
_LIVE_GROUPS: set[int] = set()
_LIVE_LOCK = threading.RLock()
_LAUNCH_STOPPED = threading.Event()
# After a timeout kill, how long collecting the output may wait for a descendant that left the
# group and still holds a pipe (DL-B-6).
KILL_DRAIN_SECONDS = 5


def kill_live() -> int:
    """Kill the process group of every timed program still running; return how many were signalled."""
    _LAUNCH_STOPPED.set()
    with _LIVE_LOCK:
        groups = sorted(_LIVE_GROUPS)
    for group in groups:
        with contextlib.suppress(OSError):
            os.killpg(group, signal.SIGKILL)
    return len(groups)


# The trapped signals besides SIGINT: each stops the run like SIGTERM, so a closed terminal
# (SIGHUP) or Ctrl-\ (SIGQUIT) cleans the running groups before the admission is released.
TERMINATING_SIGNALS = (signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT)


class Terminated(Exception):
    """The runner received SIGTERM, SIGHUP or SIGQUIT: the running programs are killed and the
    run stops (exit 128 plus the signal number, 143 for SIGTERM)."""

    def __init__(self, signum: int = signal.SIGTERM) -> None:
        super().__init__(signal.Signals(signum).name)
        self.signum = signum


@contextlib.contextmanager
def defer_launch_signals():
    """On the main thread, deliver cancellation only after Popen's child is registered.

    Blocking signals with pthread_sigmask would pass the blocked mask to the child. Temporary
    handlers defer Python's exceptions instead; workers are already protected by _LIVE_LOCK,
    since Python delivers their signals on the main thread.
    """
    if threading.current_thread() is not threading.main_thread():
        yield
        return
    pending = []
    previous = {}
    try:
        for signum in (signal.SIGINT, *TERMINATING_SIGNALS):
            previous[signum] = signal.signal(signum, lambda received, _frame: pending.append(received))
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
        for signum in pending:
            signal.raise_signal(signum)


def _lock_fds(owned: int | None) -> tuple[int, ...]:
    """The descriptors a local check's children inherit to keep the admission's ownership alive."""
    return () if owned is None else (owned,)


def launch(
    command: list[str],
    root: Path,
    env: dict[str, str],
    secret: str | list[str] | None = None,
    timeout: float | None = None,
    limit: str | None = None,
    deadline: float | None = None,
    pass_fds: tuple[int, ...] = (),
) -> subprocess.CompletedProcess:
    """Start a foreign program: empty standard input, the worktree as its directory.

    With a `timeout` the program leads a process group of its own, and a timeout kills the whole
    group: a hung `make verify` leaves no shell, pytest or worker behind to write into the worktree
    after the run stopped (O188-4 of the #188 review). The group is registered while it runs, so an
    interrupted runner kills it too (`kill_live`), and the drain after a kill is bounded by
    `KILL_DRAIN_SECONDS`: a descendant that left the group is abandoned, not waited for.
    `pass_fds` hands descriptors — a verification admission's lock — to the child, so ownership
    outlives this process for exactly as long as the child and its own children run.
    """
    try:
        if timeout is None and deadline is None:
            return subprocess.run(
                command,
                cwd=root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                errors="replace",
                check=False,
                pass_fds=pass_fds,
            )
        process = None
        try:
            with _LIVE_LOCK:
                if _LAUNCH_STOPPED.is_set():
                    raise NotStarted("the runner was interrupted; no program starts")
                with defer_launch_signals():
                    # Admission and waiting for the launch lock use the same round budget.
                    # Recheck at process creation so a late replacement is never consumed.
                    if deadline is not None:
                        left = remaining(deadline)
                        timeout = left if timeout is None else min(timeout, left)
                    process = subprocess.Popen(
                        command,
                        cwd=root,
                        env=env,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        errors="replace",
                        start_new_session=True,
                        pass_fds=pass_fds,
                    )
                    _LIVE_GROUPS.add(process.pid)
            # Cancellation may have arrived while Popen was starting in a worker.
            if _LAUNCH_STOPPED.is_set():
                raise NotStarted("the runner was interrupted during launch")
            stdout, stderr = process.communicate(timeout=timeout)
            # A grandchild that kept running after the command exited would outlive an admission
            # released around this call; the group is ended before returning (review row F6-5).
            verify_lock.end_lingering_group(process.pid)
        except BaseException:
            if process is None:
                raise
            # Kill before unregistering and before any Popen cleanup could wait for a live child.
            with contextlib.suppress(OSError):
                os.killpg(process.pid, signal.SIGKILL)
            with contextlib.suppress(subprocess.TimeoutExpired):
                process.communicate(timeout=KILL_DRAIN_SECONDS)
            raise
        finally:
            if process is not None:
                for pipe in (process.stdout, process.stderr):
                    if pipe is not None:
                        pipe.close()
                with _LIVE_LOCK:
                    _LIVE_GROUPS.discard(process.pid)
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired as error:
        what = limit or f"the reviewer time limit after {REVIEWER_MINUTES:g} minutes"
        raise StepTimedOut(f"{command[0]} was stopped by {what}") from error
    except OSError as error:
        raise CallFailed(f"{command[0]} could not be started: {scrub(str(error), secret)}") from error


def last_error_line(done: subprocess.CompletedProcess, secret: str | list[str] | None = None) -> str:
    """The last non-empty line of the program's standard error, scrubbed and bounded; empty when there is none."""
    lines = [line.strip() for line in (done.stderr or "").splitlines() if line.strip()]
    if not lines:
        return ""
    return scrub(lines[-1], secret)[:200]


def fail(
    program: str,
    done: subprocess.CompletedProcess,
    reason: str,
    secret: str | list[str] | None = None,
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


def failed_with_answer_file(error: CallFailed, answer_file: Path) -> CallFailed:
    """A failed Codex call keeps whatever its answer file already held, as its partial answer.

    The repair evidence saves a failed call's available output too (bead coding-harness-hgvp); the
    message and the failure class stay as `fail` built them, so failure classification and the retry
    behavior are unchanged.
    """
    with contextlib.suppress(OSError, UnicodeDecodeError):
        error.partial_answer = answer_file.read_text(encoding="utf-8")
    return error


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
    """The header or the separator of a table.

    A header is known by its first cell `ID`, or by the column names after it, whatever its first cell
    (`#`, `No.`): such a line is no finding (DL-B-11 of the loop's deep review).
    """
    named = [cell.lower() for cell in cells[1:6]] == [column.lower() for column in ROW_COLUMNS[1:6]]
    return cells[0].lower() == "id" or named or all(re.fullmatch(r":?-+:?", cell) for cell in cells)


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
    """A Markdown table; an unescaped `|` in a cell is escaped, so a cell never moves the columns (DL-B-7)."""
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    lines += ["| " + " | ".join(_PIPE.sub(r"\\|", cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines)


def append(path: Path, text: str) -> None:
    """Add a block at the end, separated by one blank line, and stamp `updated:` - in one atomic replacement.

    The earlier bytes stay exactly as they were (CRLF, lone CR, anything not LF; deep review RS-1-8): the new
    content is built from the file's bytes, never from text read with universal newlines. The appended and
    stamped result goes to a temporary file in the same directory, is flushed to disk and then replaces the
    file in one step, so a crash, a kill or a full disk leaves either the old file or the new one, never a
    truncated one (deep review RS-2-6).
    """
    existing = path.read_bytes() if path.exists() else b""
    addition = text.rstrip().encode("utf-8") + b"\n"
    separator = (b"" if existing.endswith(b"\n") else b"\n") + b"\n"
    joined = existing + separator + addition if existing else addition
    try:
        decoded = joined.decode("utf-8")
    except UnicodeDecodeError:
        stamped = joined  # a header that is not UTF-8 is never rewritten (check_frontmatter_current.stamp)
    else:
        stamped = check_frontmatter_current.stamped(decoded, dt.date.today()).encode("utf-8")
    write_atomic(path, stamped)


def write_atomic(path: Path, data: bytes) -> None:
    """Replace ``path`` with ``data``: temporary file, fsync, rename, directory fsync; the mode is kept."""
    try:
        mode = path.stat().st_mode & 0o7777
    except FileNotFoundError:
        path.write_bytes(data)  # nothing earlier to lose; the process umask applies as for any new file
        return
    handle, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        temporary.chmod(mode)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


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
        parts.append(f"{NOT_ROWS_NOTE}\n\n{quote_reviewer(kept.strip())}")
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
    go_admission: Callable[[Path, str], str | None] | None = None

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
    without a decision. One predicate (`stage2_swarm.exclusion_problem`), read by the free class, the paid
    declaration and every research path, with each research role checking its own data class (PR #208).
    """
    import stage2_swarm

    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    return stage2_swarm.exclusion_problem(data, model)


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


def public_declaration_problem(root: Path, endpoint: str, model: str) -> str | None:
    """Why the declaration does not clear this endpoint and model for public-web data, or None.

    The swarm's free researchers are the only role on the public class (ADR 0020
    draft): the endpoint must be cleared for `public-web` and nothing else, and
    the model must be listed. Unknown residency does not refuse here - it is
    what the declaration honestly records - while the framework check above
    still refuses every public-only endpoint and every residency it cannot
    read (spec, criterion 11).
    """
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    found = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == endpoint), None)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    if model not in (found.get("modelle") or []):
        return f"the endpoint {endpoint} does not list the model {model}"
    if found.get("darf_sehen") != ["public-web"]:
        return f"the endpoint {endpoint} is not cleared for public-web data only"
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
    return Context(root, change, folder, bead, go_admission=admission_problem)


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


class AdmissionRefused(Refused):
    """Only the declaration refused this model; a replacement may be skipped."""


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
        raise AdmissionRefused(problem)
    result = leakcheck.check(ctx.change, leakcheck.default_denylist(), ctx.root, [("prompt", prompt)])
    print(result.verdict.render())
    if result.verdict.exit_code() != 0:
        raise Refused("the leak check is not clean; the call does not start.")
    # A scan can cross UTC midnight: an earlier admission cannot authorize
    # dispatch after expiry, including retry and replacement calls.
    problem = (
        admission_problem(ctx.root, endpoint[1])
        if admission_problem is not None
        else declaration_problem(ctx.root, endpoint[0], endpoint[1])
    )
    if problem:
        raise Refused(problem)
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


def terms_today() -> dt.date:
    """The UTC calendar date terms expiry is judged against (a seam for tests).

    Terms are a UTC boundary (spec, terms): the local calendar date never
    decides admission, so tests pin this seam alone and leave the runner's
    accounting clocks live.
    """
    return dt.datetime.now(dt.UTC).date()


def _valid_until(record: dict) -> tuple[dt.date | None, str]:
    """The record's parsed `valid_until`, or why it is not a usable end date.

    Only a quoted ISO calendar date counts (spec, terms): a missing value, a
    YAML-native date, a timestamp and a malformed or impossible calendar date
    are all refused, never repaired or inferred (fail closed).
    """
    value = record.get("valid_until")
    if value is None:
        return None, "valid_until is missing"
    if not isinstance(value, str) or not DATE_ONLY.fullmatch(value) or not _valid_date(value):
        return None, "valid_until is not a quoted ISO date YYYY-MM-DD"
    return dt.date.fromisoformat(value), ""


def terms_problem(entry: dict, model: str) -> str | None:
    """Why the paid model's data terms are unread or no longer valid, or None when it is admitted.

    A dated, sourced reading must explicitly rule out training and carry a
    usable end date `valid_until`, valid through that UTC day; the following day
    the reading is expired (bead coding-harness-abra). A dated skip keeps the
    model out and names its reason for the handover (ADR 0021, decision 5).
    The declared dates rule: the runner never infers, extends or renews one.
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
    expiry, why = _valid_until(record)
    if expiry is None:
        return f"the model {model} has no usable terms expiry ({why}); the reading grants no admission"
    if expiry < terms_today():
        return f"the model {model}'s data terms expired on {expiry.isoformat()}; the reading admits no further call"
    return None


TERMS_WARNING_DAYS = 7
_terms_warning_evidence: contextvars.ContextVar[list[str] | None] = contextvars.ContextVar(
    "terms_warning_evidence", default=None
)


@contextlib.contextmanager
def capture_terms_warnings() -> Iterator[list[str]]:
    """Collect one operation's warnings, restoring the caller's scope even on refusal."""
    warnings: list[str] = []
    token = _terms_warning_evidence.set(warnings)
    try:
        yield warnings
    finally:
        _terms_warning_evidence.reset(token)


def retain_terms_warnings(warnings: list[str]) -> list[str]:
    """Keep each emitted warning in order, including changing day counts during probes."""
    evidence = _terms_warning_evidence.get()
    if evidence is None:
        return warnings
    evidence.extend(warning for warning in warnings if warning not in evidence)
    return evidence


_address_notice_evidence: contextvars.ContextVar[list[str] | None] = contextvars.ContextVar(
    "address_notice_evidence", default=None
)


@contextlib.contextmanager
def capture_address_notices() -> Iterator[list[str]]:
    """Collect a round's notices across concurrent members, retries and replacements."""
    notices: list[str] = []
    token = _address_notice_evidence.set(notices)
    try:
        yield notices
    finally:
        _address_notice_evidence.reset(token)


def retain_address_notices(notices: list[str]) -> list[str]:
    """Keep assessed, path-only diagnostics for the operation's durable evidence."""
    evidence = _address_notice_evidence.get()
    if evidence is None:
        return notices
    evidence.extend(notice for notice in notices if notice not in evidence)
    return evidence


def terms_warnings(entry: dict) -> list[str]:
    """The declared paid models whose reading expires within seven UTC days, declared order.

    Every declared record warns on a valid date inside the window, a skipped
    record included: a warning is advance notice, never admission ([DETAIL],
    2026-10-26). An expired date warns not — that is a skip with its reason —
    and an unusable one warns not either, for it refuses admission outright.
    """
    today = terms_today()
    warnings = []
    for model in dict.fromkeys(str(model) for model in entry.get("modelle") or []):
        expiry, _why = _valid_until(_terms(entry, model))
        if expiry is None:
            continue
        days = (expiry - today).days
        if 0 <= days <= TERMS_WARNING_DAYS:
            left = "1 day" if days == 1 else f"{days} days"
            warnings.append(f"the data terms of {model} expire on {expiry.isoformat()} ({left} left)")
    return warnings


def dispatch_go(
    root: Path, model: str, send: Callable, *args, admission=None, destination=None, configuration=None, **kwargs
):
    """The final shared Go send boundary, independent of tools, retries and saved admission.

    Only a caller's checked discovered-free admission can replace paid terms.
    A declared paid record always keeps its terms check, even with that callback.
    All command construction and leak scans precede this function.

    `destination` is the caller's checked effective definition. The boundary
    re-assesses it against the address policy read fresh from the held
    declaration (criterion 6): an earlier selection, a saved overlay, a
    receipt, a resumed round, a replacement or a retry never dispatches a
    destination the current record refuses. A same-host path move is announced
    here once more; a foreign destination is refused before the send. The
    caller supplies the models.json or checked-model.json that its launch
    consumes; its selected API and explicit base must match the assessment.
    """
    if destination is None:
        raise Refused(f"the launch of {model} carries no checked destination; no model request starts.")
    try:
        policy = stage2_go.load_address_policy(root)
    except stage2_go.RecordUnusable as error:
        raise Refused(f"the Go address record is unusable: {error}") from None
    verdict = stage2_go.assess(policy, model, destination)
    if verdict.notice:
        retain_address_notices([verdict.notice])
        print(f"Address notice: {verdict.notice}")
    if verdict.problem:
        raise Refused(verdict.problem)
    entry = endpoint_entry(root)
    paid = model in (entry.get("modelle") or []) or model in (entry.get("modelle_terms") or {})
    if paid or admission is None:
        warnings = terms_warnings({**entry, "modelle": [model]})
        retain_terms_warnings(warnings)
        for warning in warnings:
            print(f"Terms warning: {warning}")
        problem = terms_problem(entry, model)
    else:
        problem = admission(root, model)
    if problem:
        raise Refused(problem)
    # Check the artifact Pi actually consumes, not just the caller's earlier assessment.
    # Never echo its contents: a mismatched URL can carry credentials.
    try:
        if configuration is None:
            raise ValueError("missing configuration")
        content = json.loads(Path(configuration).read_text(encoding="utf-8"))
        if Path(configuration).name == "checked-model.json":
            actual = content.get("model") if content.get("provider") == OPENCODE else None
        else:
            actual = stage2_go.definition_of(content.get("providers"), OPENCODE, model)
        if not isinstance(actual, dict) or actual.get("id") != model:
            raise ValueError("missing or ambiguous model")
        if any(actual.get(field) != verdict.definition.get(field) for field in ("api", "baseUrl")):
            raise ValueError("destination mismatch")
        checked = stage2_go.assess(policy, model, actual)
        if not checked.admitted:
            raise ValueError("refused destination")
    except (OSError, UnicodeDecodeError, ValueError, TypeError, AttributeError):
        raise Refused(
            f"the sending configuration of {model} does not match its checked destination; no request starts."
        ) from None
    return send(*args, **kwargs)


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
    eligible = [model for model in models if paid_problem(root, entry, model) is None]
    return ordered_models(entry, eligible)


def paid_problem(root: Path, entry: dict, model: str) -> str | None:
    """Why a declared paid model is not eligible: its terms, or an `ausgeschlossen` entry naming it (DL-B-2)."""
    return terms_problem(entry, model) or excluded_problem(root, model)


def skipped_models(root: Path) -> list[str]:
    """The declared paid models that are not eligible, each named with its reason (ADR 0021, decision 5)."""
    entry = endpoint_entry(root)
    named = []
    declared = [str(model) for model in entry.get("modelle") or []]
    for model in dict.fromkeys([*declared, *(entry.get("flash_swarm") or [])]):
        problem = paid_problem(root, entry, model) if model in declared else "not a declared paid model"
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


# A catalog id the runner may select: third-party catalog text never carries a `|` or other markup into
# the record's cells (DL-B-7 of the loop's deep review).
MODEL_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*")


def free_drops(root: Path, rule: dict, catalog: list[dict], fresh: set[str]) -> dict[str, str]:
    """The free candidates of the fresh catalog that are not selected, each with its reason (DL-B-2, DL-B-7).

    A candidate is an id of the rule's provider that its suffix or include would select. An id outside
    `MODEL_ID` is dropped, and so is one an `ausgeschlossen` entry names: the maintainer's exclusion
    leaves that id out, not the whole stage.
    """
    suffix = rule.get("id_suffix", "")
    includes = {str(record["id"]) for record in rule.get("include") or []}
    excludes = {str(record["id"]) for record in rule.get("exclude") or []}
    dropped: dict[str, str] = {}
    for row in catalog:
        model = row["model"]
        if row["provider"] != rule["provider"] or model in excludes or model not in fresh or model in dropped:
            continue
        if not (model in includes or (suffix and model.endswith(suffix))):
            continue
        if not MODEL_ID.fullmatch(model):
            dropped[model] = "not a plain model id"
        elif problem := excluded_problem(root, model):
            dropped[model] = problem
    return dropped


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
        if model in excludes or not MODEL_ID.fullmatch(model):
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


# The catalog fields a model definition may carry into Pi's active configuration (RS-3-3 of the
# research-swarm review): `samplingParams` is merged into the request body and could name another
# model than `--model` and the audit line; `headers`, `compat` and every other field are dropped.
# `baseUrl` crosses assessed (DL-B-8, closed by go-access-point): the one address record in
# `model-endpoints.yaml` (`stage2_go`) admits it — a different path on the admitted host runs on
# with a notice, any other destination is dropped here and refused before any model request.
OVERLAY_FIELDS = ("id", "name", "api", "baseUrl", "reasoning", "input", "contextWindow", "maxTokens", "cost")


def activate_overlay(
    agent: Path, store: dict, policy: stage2_go.AddressPolicy
) -> tuple[dict[str, list[str]], list[str]]:
    """Activate fetched definitions through Pi's explicit model configuration.

    Returns the fields dropped per id and the address notices of same-host
    path moves. Pi 1.2.0 restores its remote cache only for server dates newer
    than its shipped catalog. A successful fresh retrieval need not carry such
    a date. Keep models-store.json as retrieval evidence and use models.json's
    model definitions to activate that exact catalog independently of cache
    age. Only the fields of `OVERLAY_FIELDS` cross, never provider auth
    configuration, request-body parameters or headers; the fetched store is
    never mutated (the retrieval evidence and persisted run snapshot). An
    `opencode-go` definition whose destination the address policy refuses is
    dropped and named — it never reaches Pi's active configuration.
    """
    providers = {}
    dropped: dict[str, list[str]] = {}
    notices: list[str] = []
    for provider, entry in store.items():
        models = []
        for position, definition in enumerate(entry.get("models", []), 1):
            label = f"{provider} definition {position}"
            if not isinstance(definition, dict):
                dropped[label] = ["not a model object"]
                continue
            if provider == stage2_go.PROVIDER:
                verdict = stage2_go.assess(policy, str(definition.get("id") or label), definition)
                if not verdict.admitted:
                    dropped[str(definition.get("id") or label)] = [verdict.problem]
                    continue
                if verdict.notice:
                    notices.append(verdict.notice)
                definition = verdict.definition
            model = {name: definition[name] for name in OVERLAY_FIELDS if name in definition}
            # A `provider` equal to the store's key says nothing the key does not: it crosses unnamed;
            # any other value would route the definition elsewhere and is dropped.
            if definition.get("provider") == provider:
                model["provider"] = provider
            extra = sorted(
                str(name)
                for name in definition
                if name not in OVERLAY_FIELDS and not (name == "provider" and definition[name] == provider)
            )
            if not model:
                dropped[label] = [*extra, "no allowed fields"]
                continue
            if extra:
                dropped[str(definition.get("id") or label)] = extra
            ident = definition.get("id")
            if not isinstance(ident, str) or not MODEL_ID.fullmatch(ident):
                dropped.setdefault(str(ident) if ident is not None else label, ["not a plain model id"])
                continue
            models.append(model)
        if models:
            providers[provider] = {"models": models}
    (agent / "models.json").write_text(json.dumps({"providers": providers}), encoding="utf-8")
    return dropped, notices


def check_overlay(agent: Path, home: Path, model: str | None = None, *, policy: stage2_go.AddressPolicy) -> None:
    """Refuse before any call if pinned Pi rejects or broadens the filtered configuration.

    Pi can report a configuration error yet resolve a model from its unfiltered remote cache.
    Exercise its real offline resolver, without credentials, and check both the error and the
    resolved definitions. Before Pi sees the file, its `opencode-go` rows are
    assessed against the address policy once more: the activated configuration
    carries checked bases alone. The fetched store stays untouched as evidence.
    """
    activated = json.loads((agent / "models.json").read_text(encoding="utf-8"))
    for definition in (activated.get("providers") or {}).get(stage2_go.PROVIDER, {}).get("models", []):
        verdict = stage2_go.assess(policy, str(definition.get("id")), definition)
        if not verdict.admitted:
            raise Refused(
                f"the activated configuration of {definition.get('id')} fails the address policy: "
                f"{verdict.problem}; no listing or reviewer starts."
            )
    runtime = REPO_ROOT / "tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js"
    script = r"""
import { readFileSync } from 'node:fs';
import { isDeepStrictEqual } from 'node:util';
globalThis.fetch = async () => { throw new Error('overlay validation forbids network'); };
try {
    const { ModelRuntime } = await import(process.argv[1]);
    const path = process.argv[2];
    const config = JSON.parse(readFileSync(path, 'utf8'));
    const runtime = await ModelRuntime.create({
        credentials: { async read() {}, async list() { return []; } },
        modelsPath: path, refreshOnCreate: false,
    });
    const result = await runtime.refresh({ allowNetwork: false });
    if (runtime.getError() || result.errors.size) throw new Error('Pi rejected the configuration');
    const allowed = new Set(JSON.parse(process.argv[3]).concat(['provider']));
    let selected = !process.argv[4];
    for (const [provider, entry] of Object.entries(config.providers)) {
        for (const definition of entry.models) {
            const resolved = runtime.getModel(provider, definition.id);
            if (!resolved) throw new Error('Pi did not resolve a configured model');
            if (resolved.provider !== provider) throw new Error('Pi changed the provider');
            for (const [field, value] of Object.entries(resolved)) {
                // Pi adds the chat discriminator itself; it is not a request parameter.
                if (field === 'type' && value === 'chat') continue;
                if (value !== undefined && !allowed.has(field)) throw new Error('Pi restored a dropped field');
            }
            for (const [field, value] of Object.entries(definition)) {
                if (!isDeepStrictEqual(resolved[field], value)) throw new Error('Pi changed a configured field');
            }
            if (provider === 'opencode-go' && definition.id === process.argv[4]) selected = true;
        }
    }
    if (!selected) throw new Error('the requested model is absent from the filtered configuration');
} catch {
    // Do not print untrusted catalog data or a path that might carry a credential.
    console.error('Pi overlay validation failed');
    process.exitCode = 1;
}
"""
    try:
        done = launch(
            [
                "node",
                "--input-type=module",
                "-e",
                script,
                runtime.as_uri(),
                str(agent / "models.json"),
                json.dumps(OVERLAY_FIELDS),
                model or "",
            ],
            agent,
            foreign_env({"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "PI_OFFLINE": "1"}),
            timeout=PI_DISCOVERY_SECONDS,
            limit="the offline overlay validation limit",
        )
    except CallFailed:
        raise Refused("Pi overlay validation could not complete; no listing or reviewer starts.") from None
    if done.returncode:
        raise Refused("Pi overlay validation failed; no listing or reviewer starts.")


def dropped_notice(dropped: dict[str, str]) -> str:
    """Name rejected ids as visible text, without terminal controls or table delimiters."""

    def visible(value: str) -> str:
        return "".join(
            f"\\x{ord(char):02x}" if ord(char) < 32 or 127 <= ord(char) <= 159 else char for char in value
        ).replace("|", "\\|")

    return "; ".join(f"{visible(model)} ({visible(reason)})" for model, reason in dropped.items())


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
    # The one address record, read fresh before anything is activated: without
    # it the free stage fails closed, and no literal origin stands in (Q-1).
    try:
        policy = stage2_go.load_address_policy(root)
    except stage2_go.RecordUnusable as error:
        raise Refused(f"the Go address record is unusable: {error}") from None
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
        stripped, notices = activate_overlay(agent, store, policy)
        if stripped:
            listing = dropped_notice({model: ", ".join(fields) for model, fields in sorted(stripped.items())})
            print(f"review-loop: catalog fields not activated: {listing}", file=sys.stderr)
        for notice in notices:
            print(f"Address notice: {notice}", file=sys.stderr)
        fresh = {
            str(model["id"])
            for model in store.get(rule["provider"], {}).get("models", [])
            if isinstance(model, dict) and model.get("id")
        }
        invalid = {model for model in fresh if not MODEL_ID.fullmatch(model)}
        if invalid:
            # Pi restores its remote cache before listing. Use a separate, validated cache for
            # that command; the fetched store and the snapshot remain unchanged as evidence.
            listing_agent = scratch / "listing-agent"
            listing_agent.mkdir()
            (listing_agent / "settings.json").write_bytes((agent / "settings.json").read_bytes())
            safe_store = {
                provider: {
                    **entry,
                    "models": [
                        model
                        for model in entry.get("models", [])
                        if isinstance(model, dict)
                        and isinstance(model.get("id"), str)
                        and MODEL_ID.fullmatch(model["id"])
                    ],
                }
                for provider, entry in store.items()
            }
            (listing_agent / "models-store.json").write_text(json.dumps(safe_store), encoding="utf-8")
            activate_overlay(listing_agent, safe_store, policy)
            env = {**env, "PI_CODING_AGENT_DIR": str(listing_agent)}
        check_overlay(Path(env["PI_CODING_AGENT_DIR"]), home, policy=policy)
        try:
            listing = launch(
                [str(PI_WRAPPER), "--list-models"], scratch, env, timeout=PI_DISCOVERY_SECONDS, limit=limit
            )
        except CallFailed as error:
            raise Refused(
                f"the model listing did not end within {PI_DISCOVERY_SECONDS} seconds; the free stage is not entered. ({error})"
            ) from None
    if listing.returncode != 0:
        raise Refused(f"`{PI_WRAPPER} --list-models` ended {listing.returncode}; the free stage stays unentered.")
    catalog = parse_catalog(listing.stdout or "")
    # Only ids the fresh overlay carries: an id that only Pi's shipped list holds is not selected (Q-13).
    dropped = free_drops(
        root, rule, [*catalog, *({"provider": rule["provider"], "model": model} for model in sorted(invalid))], fresh
    )
    # Only assessed definitions become selectable: a fresh catalog row whose
    # destination the record refuses is named as a drop and never reaches a
    # launch, however the rule filters (criterion 5).
    for definition in store.get(rule["provider"], {}).get("models", []):
        if not isinstance(definition, dict) or not isinstance(definition.get("id"), str):
            continue
        verdict = stage2_go.assess(policy, definition["id"], definition)
        if not verdict.admitted:
            dropped.setdefault(definition["id"], verdict.problem)
    selected = [model for model in select_free(rule, catalog) if model in fresh and model not in dropped]
    if dropped:
        print(f"review-loop: free ids dropped: {dropped_notice(dropped)}", file=sys.stderr)
    if not selected and not allow_empty:
        raise Refused("the live catalog holds no free model for the configured rule; the free stage is not entered.")
    return {
        "checked_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "source": "pi.dev",
        "pi_version": PI_VERSION,
        "rule": json.loads(json.dumps(rule)),
        "catalog": catalog,
        "selected": selected,
        "dropped": dropped,
        "notices": notices,
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


def free_diff(root: Path) -> tuple[str, str | None]:
    """The implementation diff the free swarm reviews, and what its own bounds cut from it.

    The same merge base as `change_diff`, uncommitted and untracked files
    included (criterion 3). Every file passes `_free_candidate`; each file's
    hunks are bounded and the whole diff is, so no whole source file travels.
    The second half names every cut, or is None: the round records it, because
    a clean answer over a cut diff is no clean round (DL-A-1 of the deep review).
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
    cuts: list[str] = []
    total = 0
    for index, rel in enumerate(names):
        if rel in untracked_set:
            piece = _git_output(root, "diff", *flags, "--no-index", "--", "/dev/null", rel, allow=(0, 1))
        else:
            piece = _git_output(root, "diff", *flags, base, "--", rel)
        bounded = _bound_hunks(rel, piece)
        if not bounded.strip():
            continue
        if len(piece.splitlines()) > FREE_DIFF_MAX_LINES:
            cuts.append(f"the free diff of {rel} was cut at {FREE_DIFF_MAX_LINES} lines")
        parts.append(bounded)
        total += bounded.count("\n")
        if total >= FREE_DIFF_MAX_TOTAL and index < len(names) - 1:
            parts.append(
                f"(the implementation diff was cut at {FREE_DIFF_MAX_TOTAL} lines; later files are not carried)"
            )
            cuts.append(f"the free diff was cut at {FREE_DIFF_MAX_TOTAL} lines; later files are not carried")
            break
    return "\n".join(parts), "; ".join(cuts) or None


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


def free_round_prompt(head: str, diff: str) -> str:
    """The free round's prompt; the review and the availability probe of a free model build it alike."""
    return "\n\n".join([FREE_REVIEW_BODY, head, ANSWER_FORMAT, f"## The implementation diff\n\n{diff}"])


FREE_PROBE_HEAD = "Availability probe only. Reply with OK. Do not review the diff and do not request tools."


def free_probe_prompt(root: Path) -> str | None:
    """A free model's availability probe: the real free-round prompt over the bounded free diff, asking for OK.

    None without a free diff: the free stage is skipped then, so there is nothing to probe at real size.
    """
    diff, _cut = free_diff(root)
    if not diff.strip():
        return None
    return free_round_prompt(FREE_PROBE_HEAD, bounded_review_diff(diff)[0])


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
            raise failed_with_answer_file(fail("codex", done, f"exit {done.returncode}"), answer_file)
        if thread is None:
            raise failed_with_answer_file(fail("codex", done, "no thread.started event"), answer_file)
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
        raise NotStarted("the round time limit expired; no further reviewer starts")
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
        # The launch resolves and assesses its model offline, against the one
        # address record read fresh from the held declaration. Without the
        # run's refreshed definitions there is no checked destination, and no
        # unchecked launch stands in for one (criterion 2).
        try:
            policy = stage2_go.load_address_policy(ctx.root)
        except stage2_go.RecordUnusable as error:
            raise Refused(f"the Go address record is unusable: {error}") from None
        store = getattr(ctx, "models_store", None)
        if store is None:
            raise Refused(
                f"no refreshed provider definitions accompany the reviewer call for {model}; "
                "its destination cannot be assessed and the call does not start."
            )
        (agent / "models-store.json").write_text(json.dumps(store), encoding="utf-8")
        _dropped, notices = activate_overlay(agent, store, policy)
        retain_address_notices(notices)
        for notice in notices:
            print(f"Address notice: {notice}", file=sys.stderr)
        home = scratch / "home"
        home.mkdir()
        check_overlay(agent, home, model, policy=policy)
        row = stage2_go.definition_of(store, stage2_go.PROVIDER, model)
        if row is None:
            raise Refused(f"the refreshed definitions of {model} are missing or duplicated; no reviewer starts.")
        assessment = stage2_go.assess(policy, model, row)
        if not assessment.admitted:
            raise Refused(assessment.problem)
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
        # Every key of the secrets file is scrubbed, not the OpenCode key alone: a member with read
        # tools can quote the GLM key from the same file (DL-B-4 of the loop's deep review).
        secrets = [key, *(value for value in secret_values() if value != key)]
        if timeout_seconds:
            seconds: float = timeout_seconds
            limit = f"the availability probe limit of {timeout_seconds} seconds"
        elif deadline is None:
            seconds = remaining(None)
            limit = f"the reviewer time limit of {REVIEWER_MINUTES:g} minutes"
        else:
            # The round's one deadline, not a fresh member limit: a late replacement gets what is left (DL-B-14).
            seconds = remaining(deadline)
            limit = (
                f"the round time limit of {REVIEWER_MINUTES:g} minutes ({seconds:.0f} seconds were left for this call)"
            )
        done = dispatch_go(
            ctx.root,
            model,
            launch,
            command,
            scratch if free else ctx.root,
            env,
            secrets,
            admission=getattr(ctx, "go_admission", None),
            destination=assessment.definition,
            configuration=agent / "models.json",
            timeout=seconds,
            limit=limit,
            **({"deadline": deadline} if deadline is not None else {}),
        )
        if done.returncode != 0:
            raise fail("pi", done, f"exit {done.returncode}", secrets, model)
        answer = scrub(done.stdout or "", secrets)
        if not answer.strip():
            # A successful empty response is malformed too: the round owes it its format retry.
            raise MalformedAnswer(answer)
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
    Without parsed findings, only the explicit no-finding response succeeds;
    an answer with neither raises `MalformedAnswer`, which carries the answer
    for the round's asked-again call and its record.

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
                raise MalformedAnswer(answer)
            answers[member] = answer
        except Exception as error:  # noqa: BLE001 - a member's failure is recorded, not raised, here
            answers[member] = error

    # Each worker has its own context, sharing this operation's warning list.
    # New threads otherwise lose the dispatch evidence captured by the parent.
    threads = [
        threading.Thread(target=contextvars.copy_context().run, args=(one, member), name=f"stage2-swarm-{member}")
        for member in members
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # A dispatch-time admission refusal is not a failed answer to replace or
    # overlook beside another member's success. It aborts without a round.
    for outcome in answers.values():
        if isinstance(outcome, Refused):
            raise outcome
    return answers


def _last_release(text: str) -> int:
    """The start of the last line the release block begins on, -1 without one.

    The heading is matched at the start of a line: a failed attempt's block quotes it with `>`, and a
    quoted heading is not the block's beginning (criterion 12).
    """
    matches = list(RELEASE_LINE.finditer(text))
    return matches[-1].start() if matches else -1


def _last_restart(text: str) -> int:
    """The start of the last restart line, -1 without one."""
    matches = list(RESTART_LINE.finditer(text))
    return matches[-1].start() if matches else -1


def record_digest(record: str) -> str:
    """The digest a release block carries of the record it released."""
    return "sha256:" + hashlib.sha256(record.encode("utf-8")).hexdigest()


def released_digest(text: str) -> str | None:
    """The record digest the last released block carries, read from the runner's own lines only."""
    start = _last_release(text)
    if start < 0:
        return None
    block = text[start:]
    cut = KEPT_FROM.search(block)
    match = DIGEST_LINE.search(block[: cut.start()] if cut else block)
    return match.group(1) if match else None


def record_identity(record: str) -> str:
    """Identify completed rounds independently of repair marks and the mutable stage snapshot."""
    rounds = [line for line in record.splitlines() if ROUND_HEADING.match(line)]
    rows = [row[:7] for row in record_rows(record)]
    return record_digest(json.dumps([rounds, rows], sort_keys=True))


def released_identity(text: str) -> str | None:
    start = _last_release(text)
    if start < 0:
        return None
    block = text[start:]
    cut = KEPT_FROM.search(block)
    match = re.search(r"^Record identity: (sha256:[0-9a-f]{64})[ \t]*$", block[: cut.start()] if cut else block, re.M)
    return match.group(1) if match else None


def lost_record_refusal(change: str, root: Path, text: str) -> str | None:
    """Refuse unaccounted calls after the last release/restart when their record is missing.

    Each no-round marker accounts for exactly its failed attempt's audit calls (DL-A-6).
    """
    since = max(_last_release(text), _last_restart(text))
    pending: list[int] = []
    # A failed attempt accounts only for its own calls, never an earlier completed round.
    # Old uncounted markers cannot establish which calls failed, so refuse conservatively.
    for line in text[since + 1 :].splitlines():
        if LOOP_AUDIT_LINE.match(line):
            pending.append(1)
        elif NO_ROUND_LINE.match(line):
            count = re.search(r"; audit calls: (\d+)$", line)
            if count and int(count.group(1)):
                del pending[max(0, len(pending) - int(count.group(1))) :]
    if not pending:
        return None
    return (
        f"findings.md shows review-loop calls after the last release, but there is no loop record at "
        f"{record_dir(change, root) / 'loop.md'}; the loop ran and its record is lost or under another "
        "state directory (XDG_STATE_HOME). Nothing is released or run, and no stage is retired; the maintainer decides."
    )


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
        elif reviewer and FROM_LINE.fullmatch(line):
            # Every reviewer line is quoted, so an unquoted `From <member>:` is the runner's: it closes one
            # member's words and names the next member's (DL-B-3).
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
    """`taken` or `fixed`: a repair preserves the fact that the review accepted the finding (criterion 11).

    A row the repair has marked `fixed` counts like the taken one it was, so repairing a round's row
    neither cleans that round nor cancels the next one (ADR 0017 decision 6, as amended by ADR 0021
    decision 7; ADR 0015's three-round reading is superseded).
    """
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


def replace_record(path: Path, text: str) -> None:
    """Write the record whole or not at all: a temporary file in its directory, then an atomic rename
    (`Path.replace`, which is `os.replace`).

    `Path.write_text` truncates first and writes after; a write that fails between the two keeps a
    record cut short, and the record is the only copy of its rounds (DL-A-4 of the deep review). The
    temporary file never outlives a failed write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            # Reconciliation also replaces findings.md: retain its permissions instead of
            # installing mkstemp's private mode. Fresh external records keep that private mode.
            if path.exists():
                os.fchmod(stream.fileno(), path.stat().st_mode & 0o7777)
            os.fsync(stream.fileno())
        Path(temporary).replace(path)
    except BaseException:
        with contextlib.suppress(OSError):
            Path(temporary).unlink()
        raise


def write_round(change: str, block: str, state: dict, root: Path) -> None:
    """Append the round and pin its stages as consumed in one write (R-6 of the review-swarm review).

    Two writes would leave a window: a crash between them keeps a round whose stage the snapshot does
    not know, and the next call repeats the stage as a new round with new ids - extra paid calls and
    two rounds for one stage. One `replace_record` closes it, for a fresh record too: its heading, its
    intro and the snapshot line before the rounds are part of the same write. The snapshot line is the
    runner's own; `kept_lines` leaves it out, because the release carries it itself (criterion 13).
    """
    path = record_dir(change, root) / "loop.md"
    line = f"{STATE_KEY}{json.dumps(state, sort_keys=True)}"
    text = (
        path.read_text(encoding="utf-8") if path.exists() else f"{RECORD_HEADING}{change}\n\n{RECORD_INTRO}\n{line}\n"
    )
    body = block.strip("\n")
    text = f"{text.rstrip(chr(10))}\n\n{body}\n" if text.strip() else f"{body}\n"
    if STATE_LINE.search(text):
        text = STATE_LINE.sub(lambda _match: line, text, count=1)
    else:
        match = ROUND_HEADING.search(text)
        text = text[: match.start()] + line + "\n\n" + text[match.start() :] if match else text + line + "\n"
    replace_record(path, text)


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
            if match is None:
                # Every release of a record carries the snapshot; a block without it is not the runner's,
                # and reading it as no run would let it end the loop (DL-A-2 of the deep review).
                raise Refused(
                    "the last released block in findings.md carries no Loop state line; the runner writes "
                    "one with every release, so the block is not the runner's and the loop is not continued."
                )
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


def release_block(record: str, text: str) -> str:
    """Render one released record, including a boundary for crash-time reconciliation."""
    rows = record_rows(record)
    state = read_state(record, text)
    released, _ = findings_rows(text)
    verdicts = {row[0]: row[-1] for row in released}
    block = [
        f"{RELEASE_HEADING} {today()}",
        render_table(RELEASED_COLUMNS, [[*row, verdicts.get(row[0], "—")] for row in rows]),
    ]
    if not rows:
        block.append("No loop row was reported.")
    block.append(f"Rounds run: {len(ROUND_HEADING.findall(record))}")
    block.append(f"{DIGEST_KEY}{record_digest(record)}")
    block.append(f"Record identity: {record_identity(record)}")
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
    block.append(RELEASE_END)
    return "\n\n".join(block)


def released_overlap_refusal(record: str, text: str) -> str | None:
    """Refuse a record whose rows or rounds still stand in released history."""
    released, _ = findings_rows(text)
    overlap = {row[0] for row in record_rows(record)} & {row[0] for row in released}
    released_rounds = rounds_run(None, text)
    old_rounds = [
        heading.split()[2] for heading in ROUND_HEADING.findall(record) if int(heading.split()[2]) <= released_rounds
    ]
    if not (overlap or old_rounds):
        return None
    identifiers = []
    if overlap:
        identifiers.append("row ids: " + ", ".join(sorted(overlap)))
    if old_rounds:
        identifiers.append("round ids: " + ", ".join(old_rounds))
    remedy = "the maintainer must reconcile the extended record."
    if released_digest(text) == record_digest(record):
        remedy = "run release-loop again: it appends nothing and removes the remnant already released."
    return (
        "the loop record overlaps rounds already released ("
        + "; ".join(identifiers)
        + "); nothing is appended or removed; "
        + remedy
    )


def release(root: Path, change: str) -> list[list[str]]:
    """The loop rows into findings.md, after the phase-6 verdict. Returns the rows released."""
    findings = folder_of(root, change) / "findings.md"
    text = findings.read_text(encoding="utf-8") if findings.exists() else ""
    record = read_record(change, root)
    if record is not None and (
        released_digest(text) == record_digest(record) or released_identity(text) == record_identity(record)
    ):
        # The block stands already: a run stopped between the append and the removal (DL-A-3 of the
        # deep review). Appending it again would count its rounds twice and double its ids.
        if released_digest(text) != record_digest(record):
            # Repair may have changed Status cells; stage retirement also changes the snapshot and
            # retained explanation. Reconcile the existing block atomically before deleting its copy.
            start = _last_release(text)
            end = text.find("\n" + RELEASE_END, start)
            if end < 0:
                raise Refused("the released block has no record boundary; nothing is removed.")
            end += len("\n" + RELEASE_END)
            block = release_block(record, text)
            heading = text[start:].splitlines()[0]
            block = heading + "\n" + block.split("\n", 1)[1]
            replace_record(findings, text[:start] + block + text[end:])
            stamp_updated(findings)
        remove_loop_record(record_dir(change, root))
        rows = record_rows(record)
        print(
            f"release-loop: the record was released already ({record_digest(record)}); nothing is appended, "
            "the record is removed"
        )
        return rows
    if record is None:
        refusal = lost_record_refusal(change, root, text)
        if refusal:
            raise Refused(refusal)
    # A record's rows need a verdict of their own: one after the last release and the last restart
    # (ADR 0021, restart amendment; DL-A-7 of the deep review).
    floor = max(_last_release(text), _last_restart(text), 0) if record is not None else 0
    if not VERDICT_LINE.search(text, floor):
        near = VERDICT_START.search(text, floor)
        if floor:
            raise Refused(
                "findings.md has no phase-6 verdict line after the last release or restart; the rows of "
                "this run are released after a phase-6 verdict of their own; nothing is released."
            )
        if near:
            raise Refused(
                f"findings.md has a line that starts like the phase-6 verdict but does not have the form "
                f"`Phase 6 verdict: <reviewer> <session>, <date>` (<date> as YYYY-MM-DD, last on the line; `pending` is no reviewer): "
                f"`{near.group(0).strip()}`; nothing is released."
            )
        raise Refused("findings.md has no phase-6 verdict line; nothing is released.")
    if record is None:
        # The runner's own lines stand at a line start; a block's quote of either line is not one (criterion 12).
        if not (NO_LOOP.search(text) or RELEASE_LINE.search(text)):
            append(findings, NO_LOOP_LINE)
        return []
    rows = record_rows(record)
    refusal = released_overlap_refusal(record, text)
    if refusal:
        raise Refused(refusal)
    refusal = undecided_refusal(rows, "nothing is released")
    if refusal:
        raise Refused(refusal)
    append(findings, release_block(record, text))
    remove_loop_record(record_dir(change, root))
    print(f"release-loop: {len(rows)} loop rows appended to {findings.relative_to(root)}")
    return rows


def remove_loop_record(directory: Path) -> None:
    """Delete the review loop's record, never the phase-1 research files beside it (deep review RS-2-1).

    The change's record directory also holds the research state store (`research/`, with the lock a running
    research run holds) and research preparation's receipt and probe audits (`research-*`). Deleting those
    would lose the reusable results of an interrupted run and let a second run take a fresh lock while the
    first still holds the old one. The directory goes only when nothing else is left in it.
    """
    for entry in directory.iterdir():
        if entry.name == "research" or entry.name.startswith("research-"):
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    with contextlib.suppress(OSError):
        directory.rmdir()


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
    if record is None:
        refusal = lost_record_refusal(change, root, findings_text)
        if refusal:
            raise Refused(refusal)
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
        if lost_record_refusal(change, root, text):
            raise Refused(
                f"{change} has no completed loop round and its loop record is missing; "
                "the maintainer must account for the stale audit lines in findings.md by hand before retrying. "
                "A restart cannot recover the lost record; nothing is written."
            )
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


def _git_output(
    root: Path,
    *args: str,
    allow: tuple[int, ...] = (0,),
    env: dict[str, str] | None = None,
    stdin: str | None = None,
    preserve_newlines: bool = False,
) -> str:
    try:
        done = subprocess.run(
            [GIT, "-C", str(root), *args],
            input=os.fsencode(stdin) if preserve_newlines and stdin is not None else stdin,
            capture_output=True,
            text=not preserve_newlines,
            errors=None if preserve_newlines else "replace",
            check=False,
            env=env,
            timeout=GIT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise Refused(f"git {args[0]} did not finish within {GIT_SECONDS // 60} minutes") from error
    if done.returncode not in allow:
        raise Refused(f"git {args[0]} failed: {os.fsdecode(done.stderr).strip()[:200]}")
    return os.fsdecode(done.stdout)


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

# After the safe formatting the runner runs an attempt's cheap checks, before derived preparation and
# `make verify` (bead coding-harness-5tyh): read-only ruff lint and format checks over the changed
# Python files the format step selected, then pytest over exactly the selected tests. Explicit
# targets only, passed as argv - never a shell, never a bare discovery run - and a command with no
# target is skipped. The first red, launch error or timeout ends the attempt before `make verify`
# starts, so a planted fault costs seconds instead of a full verification; cheap green never
# replaces full verification, it only earns the right to run it.
RUFF_CHECK = ("check", "--force-exclude", "--no-cache")
RUFF_FORMAT_CHECK = ("format", "--check", "--force-exclude", "--no-cache")
PYTEST = (".venv/bin/python3", "-m", "pytest", "-q", "-n", "auto")
CHEAP_LABEL = "Runner cheap checks before `make verify`"

# An attempt's edits to its own findings.md are put back before any post-run check reads model-written
# state, so the edit alone never spends the attempt (spec, criterion 8). The rejected note joins the
# attempt's problems (block and retry prompt); the accepted notice is quoted under the audit line the
# checkpoint commits - a passing restored attempt is never labelled failed (spec, criterion 9).
FINDINGS_RESTORED = (
    "the attempt's edits to findings.md were restored before the checks; the file stands as it stood "
    "before the call, and the attempt failed for the reasons below"
)
FINDINGS_RESTORED_NOTICE = (
    "The attempt edited findings.md; the runner restored it before the post-run checks, and the attempt passed them."
)


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
    """Tracked changes against `against`, in the working tree or the index, and untracked files.

    `git diff <commit>` reads only the working tree, so a path staged and then put back in the file
    differs from the commit in the index alone; `--cached` lists it (bead coding-harness-0c8).
    """
    # `--no-renames`: a rename must list both names, or the deleted one is invisible (O192-1).
    tracked = _git_output(root, "diff", "--no-renames", "--name-only", "-z", against, env=env).split("\0")
    tracked += _git_output(root, "diff", "--cached", "--no-renames", "--name-only", "-z", against, env=env).split("\0")
    untracked = _git_output(root, "ls-files", "-z", "--others", "--exclude-standard", env=env).split("\0")
    return {Path(name) for name in [*tracked, *untracked] if name}


def _git_bytes(root: Path, *args: str, env: dict[str, str] | None = None, stdin: bytes | None = None) -> bytes:
    """Run Git without decoding path output or translating pathspec stdin."""
    try:
        done = subprocess.run(
            [GIT, "-C", str(root), *args],
            input=stdin,
            capture_output=True,
            text=False,
            check=False,
            env=env,
            timeout=GIT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise Refused(f"git {args[0]} did not finish within {GIT_SECONDS // 60} minutes") from error
    if done.returncode != 0:
        raise Refused(f"git {args[0]} failed: {os.fsdecode(done.stderr).strip()[:200]}")
    return done.stdout


def intend_new_files(root: Path, env: dict[str, str] | None = None) -> list[bytes]:
    """Add every untracked, non-ignored file intent-to-add, so `git ls-files` lists it; return the names.

    A gate that reads the index (the leerprobe gate builds its foreign repository from `git ls-files`)
    would otherwise miss a script the attempt just created (bead coding-harness-fdz). Intent-to-add
    records only the path, not its content: the checkpoint's `git add -A` stages the content later, and
    `verify_attempt` drops the entries right after `make verify`.
    The names go to git on stdin, NUL-separated, so thousands of files cannot overflow the argument
    list, and `--literal-pathspecs` makes them paths, not patterns: `[i].md` does not match `i.md`
    and `:notes.md` is no pathspec magic. Paths remain filesystem bytes throughout listing,
    adding and cleanup, including names that cannot be decoded as UTF-8.
    """
    names = [
        name
        for name in _git_bytes(root, "ls-files", "-z", "--others", "--exclude-standard", env=env).split(b"\0")
        if name
    ]
    if names:
        _git_bytes(
            root,
            "--literal-pathspecs",
            "add",
            "--intent-to-add",
            "--pathspec-from-file=-",
            "--pathspec-file-nul",
            env=env,
            stdin=b"\0".join(names) + b"\0",
        )
    return names


def drop_intended(root: Path, names: list[bytes], env: dict[str, str] | None = None) -> None:
    """Remove the intent-to-add entries of `names` from the index; the files and the caller's entries stay.

    `rm --cached` on the literal paths touches only those entries: a reset to HEAD would also unstage
    a caller's change on a path that a pattern happens to match, or undo a caller's `git rm --cached`.
    """
    if names:
        _git_bytes(
            root,
            "--literal-pathspecs",
            "rm",
            "--cached",
            "-q",
            "--ignore-unmatch",
            "-f",
            "--pathspec-from-file=-",
            "--pathspec-file-nul",
            env=env,
            stdin=b"\0".join(names) + b"\0",
        )


def derived_leftover(root: Path, relative: Path) -> bool:
    """A change the runner itself derives before every verify, so a failed run may leave it (bead coding-harness-b5w).

    Three kinds, and only these: the rendered `plans/INDEX.md` (re-rendered from the tree before the next
    verify), a file whose only difference from `HEAD` is its `updated:` line (the date stamp), and Python
    bytecode under `__pycache__` that the runner's own renderer wrote. A content edit is never one.
    """
    # A stamp or rendered file never accounts for a tracked permission/type change.
    for index in ((), ("--cached",)):
        raw = _git_output(root, "diff", *index, "--raw", "--no-renames", "-z", "HEAD", "--", relative.as_posix())
        for metadata in raw.split("\0")[::2]:
            if metadata:
                modes = metadata.split()[:2]
                if modes[0] != ":000000" and modes[0][1:] != modes[1]:
                    return False
    if relative.as_posix() == "plans/INDEX.md":
        return True
    if "__pycache__" in relative.parts and relative.suffix == ".pyc":
        return True
    # The two versions are compared with the frontmatter `updated:` line masked, never through a parsed diff:
    # a diff line whose text starts `--` or `++` looks like a file header (runner review R-3). Both are
    # read as bytes and decoded without newline translation, so a CRLF to LF conversion is a change (P243-1).
    path = root / relative
    try:
        if path.is_symlink() or not path.is_file():
            return False
        now = path.read_bytes().decode("utf-8")
        then = _git_bytes(root, "show", f"HEAD:{relative.as_posix()}").decode("utf-8")
        staged = _git_bytes(root, "show", f":{relative.as_posix()}").decode("utf-8")
    except (OSError, UnicodeDecodeError, Refused):
        return False
    if now == staged == then:
        return False
    before = _mask_stamp(then, dated=False)
    # Check both independent versions against HEAD: git add -A must not erase a substantive staged edit.
    return before is not None and all(
        version == then or _mask_stamp(version, dated=True) == before for version in (now, staged)
    )


_STAMP_DATE = re.compile(r"updated: \d{4}-\d{2}-\d{2}\r?")


def _mask_stamp(text: str, *, dated: bool) -> str | None:
    """`text` with the frontmatter's one `updated:` line replaced by a mask; None when there is no such line.

    The line is found as `check_frontmatter_current.stamp` finds it, so the no-space form matches too. With
    `dated` the line must be what `stamp` writes, `updated: YYYY-MM-DD`; an inserted or missing line is None.
    """
    block = check_frontmatter_current._BLOCK.match(text)
    if block is None:
        return None
    lines = block.group(1).split("\n")
    found = [i for i, line in enumerate(lines) if check_frontmatter_current._UPDATED_LINE.match(line)]
    if len(found) != 1:
        return None
    line = lines[found[0]]
    if dated and not _STAMP_DATE.fullmatch(line):
        return None
    lines[found[0]] = "updated: <stamp>" + ("\r" if line.endswith("\r") else "")
    return text[: block.start(1)] + "\n".join(lines) + text[block.end(1) :]


def refuse_preexisting(root: Path, allowed: set[Path]) -> None:
    """Refuse pre-existing changes outside `allowed`, except the runner's own derived leftovers (bead coding-harness-b5w)."""
    outside = {path for path in changed_paths(root) - allowed if not derived_leftover(root, path)}
    if outside:
        listing = ", ".join(sorted(path.as_posix() for path in outside))
        raise Refused(f"the worktree has pre-existing changes outside this change's findings.md: {listing}")


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


AliasBaseline = tuple[dict[Path, Path], dict[Path, tuple[int, int]]]


def alias_baseline(root: Path, baseline: str, ignored_before: dict[Path, tuple[int, int]] | None) -> AliasBaseline:
    """The links that stood before the attempt: tracked ones from the baseline, ignored ones by their stat.

    Recovery compares every link in a destination's parent chain with this record instead of
    simulating what the recovery would do to it (decisions.md, Q-2): an attempt's own link, or a
    baseline link it replaced or changed, refuses the batch before its first mutation.
    """
    links: dict[Path, Path] = {}
    try:
        for entry in filter(None, _git_output(root, "ls-tree", "-rz", baseline).split("\0")):
            metadata, name = entry.split("\t", 1)
            mode, _, oid = metadata.split()
            if mode == "120000":
                links[Path(name)] = Path(_git_output(root, "cat-file", "blob", oid))
    except (Refused, OSError, ValueError) as error:
        raise RestorationRefused(
            f"restoration is refused: the links of the rollback baseline cannot be read ({error})"
        ) from error
    return links, dict(ignored_before or {})


def plan_baseline_restore(
    root: Path,
    keep: set[Path],
    ignored_before: dict[Path, tuple[int, int]] | None = None,
    baseline: str = "HEAD",
) -> tuple[list[str], list[Path]]:
    """The tracked and newly created ignored paths a failed attempt left, checked before any undo.

    Raises the restoration refusal before the caller mutates anything when a rollback or cleanup
    destination's parent chain would carry the restore outside the worktree. Callers that mutate
    other things first (findings, the saved attempt) run this before them and pass the result to
    `restore_baseline`, so the tree is read once and nothing is written against a refusal.
    """
    touched = sorted(path.as_posix() for path in changed_paths(root) - keep)
    created = sorted(ignored_snapshot(root).keys() - ignored_before.keys()) if ignored_before is not None else []
    if touched or created:
        preflight_recovery(
            root,
            [*(root / relative for relative in touched), *(root / relative for relative in created)],
            aliases=alias_baseline(root, baseline, ignored_before),
        )
    return touched, created


def save_answer_evidence(root: Path, change: str, token: str, attempt: int, answer: str, key: str | None) -> str:
    """Save one attempt's full answer as protected evidence below the worktree's own git directory.

    Written at the model-return boundary, before any HEAD check, verification or answer check can
    stop the run, so a rejected answer stays diagnosable from what the model actually returned (bead
    coding-harness-hgvp). The directory is git's resolved per-worktree `stage2/attempts/<change>/` - in
    a linked worktree below the main checkout's `.git/worktrees/<name>/`, which the diagnostics name
    as an absolute path - local evidence like `refs/stage2/attempts/`, tracked by no path and carried by no branch push.
    The answer passes `protect_diagnostics` once on every route, the keyless ones included; an empty
    or unavailable answer is recorded as such, never fabricated or retried. The file is created
    exclusively, so an earlier attempt's evidence is never overwritten; an aliased destination, a
    protection failure or a failed write raises, so no checkpoint stands on lost or unprotected
    evidence. Returns the saved file, as the diagnostics name it.
    """
    try:
        git_dir = Path(_git_output(root, "rev-parse", "--absolute-git-dir").strip())
    except Refused as error:
        raise CallFailed(f"the answer evidence directory could not be resolved ({error})") from error
    if not git_dir.is_absolute():
        git_dir = root / git_dir
    body = protect_diagnostics(answer, key) if answer.strip() else "(no answer was returned)\n"
    directory = git_dir / "stage2" / "attempts" / change
    expected = Path(os.path.realpath(git_dir)) / "stage2" / "attempts" / change
    if directory.is_symlink() or os.path.realpath(directory) != str(expected):
        raise CallFailed(
            f"the answer evidence directory {directory} is not this worktree's own stage2/attempts/{change}; "
            "no evidence is written and no checkpoint is made"
        )
    destination = directory / f"attempt-{attempt}-{token}.md"
    created = False
    try:
        directory.mkdir(parents=True, exist_ok=True)
        handle = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        created = True
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(body if body.endswith("\n") else body + "\n")
        if destination.is_symlink() or destination.stat().st_nlink > 1:
            raise OSError(f"the destination is aliased ({destination})")
    except OSError as error:
        # Remove only the file this call created, never an earlier exclusive destination.
        cleanup = "no evidence is written"
        if created:
            try:
                destination.unlink()
            except OSError as cleanup_error:
                cleanup = f"incomplete evidence remains at {destination} (cleanup failed: {cleanup_error})"
        raise CallFailed(
            f"the answer evidence could not be saved ({error}); {cleanup} and no checkpoint is made"
        ) from error
    return str(destination)


def restore_baseline(
    root: Path,
    baseline: str,
    keep: set[Path],
    ignored_before: dict[Path, tuple[int, int]] | None = None,
    planned: tuple[list[str], list[Path]] | None = None,
) -> str:
    """After a failed model call, put every path but `keep` back at the baseline; say what was undone.

    The runner refused pre-existing changes outside `keep` before the first call, so what differs
    from the baseline outside it is the run's own - including a half-finished edit of a dead process.
    Gitignored paths the attempt created are removed too: `changed_paths` cannot see them and
    `git clean` without `-x` keeps them, so the run's earlier snapshot of the ignored files tells them
    apart from the ones that stood before (phase 6, F-5). This implementation/repair rollback's
    tracked destinations and newly created ignored cleanup paths are checked for an unsafe parent
    before its first `git restore`, `git clean`, `unlink`, `rmtree` or parent removal; a refusal
    leaves this recovery batch unwritten and ends the run.
    """
    if planned is None:
        planned = plan_baseline_restore(root, keep, ignored_before, baseline)
    touched, created = planned
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
    timeout: float | None = None,
    limit: str | None = None,
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
        done = launch(command, ctx.root, env, key, timeout=timeout, limit=limit)
    if done.returncode != 0:
        error = fail("claude", done, f"exit {done.returncode}", key)
        # A failed call's printed answer travels along for the repair evidence; nothing else changes.
        error.partial_answer = scrub(done.stdout or "", key)
        raise error
    answer = scrub(done.stdout or "", key)
    if not answer.strip():
        raise fail("claude", done, "the answer is empty", key)
    return answer


def remove_changed_credential(
    root: Path,
    key: str,
    ignored_before: dict[Path, tuple[int, int]] | None = None,
    against: str = "HEAD",
    findings: Path | None = None,
) -> list[Path]:
    """Remove an exact GLM credential from changed regular files and name those files.

    "Changed" is tracked changes, untracked files, and - when the run's earlier snapshot of the
    gitignored files is given - every ignored file created or touched since that snapshot. The
    comparison is `against`, not always HEAD: a draft passes its baseline, because files a model
    committed read as clean against its own new HEAD and must still be found (spec, criterion 25;
    2a's F-4).

    Skip changed paths whose parents escape the worktree or cannot be resolved, without
    reading or writing through them. Name each skip on stderr and, when supplied and safe,
    in the findings call record. A skip does not establish whether the path holds a credential.
    """
    paths = changed_paths(root, against=against)
    if ignored_before is not None:
        paths |= {p for p, stat in ignored_snapshot(root).items() if ignored_before.get(p) != stat}
    # Scanning is not recovery: skip unsafe parents without reading or writing
    # through them, while retaining credential removal in contained files.
    found = []
    for relative in sorted(paths, key=lambda path: path.as_posix()):
        path = root / relative
        problem = restoration_parent_problem(root, path)
        if problem is not None:
            diagnostic = protect_diagnostics(
                f"credential scan skipped {relative.as_posix()}: its parent {problem}; contents were not inspected",
                key,
            )
            print(diagnostic, file=sys.stderr)
            record_credential_scan_skips(root, findings, [diagnostic], key)
            continue
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


def record_credential_scan_skips(root: Path, findings: Path | None, diagnostics: list[str], key: str | None) -> None:
    """Record scan limits only in a contained regular call record, never through an alias."""
    if not diagnostics or findings is None or restoration_parent_problem(root, findings) is not None:
        return
    if findings.is_symlink() or (findings.exists() and (not findings.is_file() or findings.stat().st_nlink > 1)):
        return
    append(findings, quote_block("\n".join(diagnostics), key))


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
                # Ruff is a local child of the verification: it gets the same verify environment
                # the timed check gets, shared state root and floor included (bead
                # coding-harness-p6mu); never the raw runner env.
                verify_lock.inherit_env(env),
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


def _cheap_evidence(done: subprocess.CompletedProcess, key: str | None) -> str:
    """The bounded evidence of a red cheap command: both streams protected whole, then the tail.

    As `verify_evidence`: the complete concatenated streams are checked before any reduction, and
    a refusal of that protection propagates - a red attempt whose output cannot be made publishable
    stops the run instead of passing silently (spec, criterion 6). The streams are then tailed apart,
    as `verify_evidence` tails standard error: a long standard error (a worker crash, plugin
    warnings) must not push pytest's `FAILED` summary on standard output out of the evidence and of
    the next attempt's selection (review rows L4-3, L5-1, L8-1).
    """
    raw_stdout = done.stdout or ""
    output, boundary = _protect_diagnostics(raw_stdout + (done.stderr or ""), key, len(raw_stdout))
    stdout, stderr = output[:boundary], output[boundary:]
    evidence = "\n".join(stdout.splitlines()[-TAIL_LINES:])
    errors = stderr.splitlines()
    if errors:
        cut = len(errors) - STDERR_LINES
        kept = ([f"[… {cut} earlier lines left out …]"] if cut > 0 else []) + errors[-STDERR_LINES:]
        evidence += ("\n\n" if evidence else "") + "Standard error, last lines:\n" + "\n".join(kept)
    return scrub(evidence, key)


def _cheap_ruff(root: Path, env: dict[str, str], key: str | None, targets: list[str]) -> str | None:
    """The read-only ruff half of the cheap checks: lint, then the format check, over the targets.

    `None` when both are green. A missing ruff, a target that cannot be read, a non-zero exit, a
    timeout and a program that cannot start are all red: a cheap check that never ran is never
    cheap-green (spec, criterion 10). The targets are the format step's - ordinary, surviving,
    changed `.py` files under `scripts/` and `tests/` - so links and hard links stay out and their
    final verdict stays with the unchanged gates.
    """
    if not (root / RUFF).is_file():
        return protect_diagnostics(f"no ruff at `{RUFF}`; `make venv` builds it.", key)
    for target in targets:
        try:
            (root / target).read_bytes()
        except OSError:
            return protect_diagnostics(f"cannot read `{target}`; the cheap checks cannot run", key)
    for command, name in ((RUFF_CHECK, "check"), (RUFF_FORMAT_CHECK, "format --check")):
        identity = f"`{RUFF} {name}`"
        try:
            done = launch(
                [RUFF, *command, *targets],
                root,
                env,
                key,
                timeout=TOOL_SECONDS,
                limit=f"the runner's tool limit after {TOOL_SECONDS // 60} minutes",
            )
        except StepTimedOut as error:
            return protect_diagnostics(f"{identity} did not finish: {error}", key)
        except CallFailed as error:
            return protect_diagnostics(f"{identity} could not be run: {error}", key)
        if done.returncode:
            return f"{identity} exited {done.returncode}\n{_cheap_evidence(done, key)}"
    return None


def _is_test_module(posix: str) -> bool:
    """Whether a repository path names a `tests/**/test_*.py` file."""
    parts = posix.split("/")
    return len(parts) >= 2 and parts[0] == "tests" and posix.endswith(".py") and parts[-1].startswith("test_")


# The id is the bare node path plus an optional `[...]` parameter part, which may itself hold ` - `
# (review rows L1-3, L1-20); the message after the separator is never part of it.
FAILED_LINE = re.compile(r"^[ \t]*FAILED (tests/[^\s\[]+(?:\[.*?\])?)(?: - .*)?[ \t]*$", re.MULTILINE)


def failed_test_ids(problems: list[str]) -> list[str]:
    """The test ids pytest reported as failed in an attempt's diagnostics, in order, without duplicates.

    Read from the `FAILED <node id>` lines of pytest's short summary, in the cheap run's output and
    in `make verify`'s alike; a line cut by the summary's width (`...`) names no usable id.
    """
    found: dict[str, None] = {}
    for problem in problems:
        for match in FAILED_LINE.finditer(problem):
            ident = match.group(1).strip()
            if not ident.endswith("..."):
                found[ident] = None
    return list(found)


def _ledger_test_refs(plan: bytes) -> list[str]:
    """The accepted plan's criterion-ledger test references, as `tests/x.py::test_y` ids.

    Both test forms count - a written entry and one still marked `not yet written`; a `not a test`
    row names no test, and lines inside a fence are examples, never references. The bytes are the
    accepted plan's snapshot, so a rejected attempt's own plan edits never change this list (spec,
    criterion 7). A plan that cannot be decoded or read raises.
    """
    lines = check_criterion_ledger._lines(plan.decode("utf-8"))
    fenced = check_criterion_ledger._fenced(lines)
    refs: list[str] = []
    for section in check_criterion_ledger.ledger_sections(lines):
        for number, line in section:
            if fenced[number - 1]:
                continue
            entry = check_criterion_ledger.parse_entry(line, number)
            if entry is None or entry.kind == "not a test" or not entry.path:
                continue
            refs.append(f"{entry.path}::{entry.function}")
    return sorted(dict.fromkeys(refs))


def _test_functions(source: str, filename: str) -> dict[str, str]:
    """The file's top-level `test_*` functions by name, each as its AST dump; parsed, never imported."""
    tree = ast.parse(source, filename=filename)
    return {
        node.name: ast.dump(node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
    }


def _top_level_names(source: str, filename: str) -> set[str]:
    """A test file's standing names: top-level functions and classes, and `Class::method` for each
    method of a top-level class; parsed, never imported. A class with a base also stands as
    `Class::*`: its inherited tests are not visible to the parse (review row F6-3)."""
    tree = ast.parse(source, filename=filename)
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            names.add(node.name)
        if isinstance(node, ast.ClassDef):
            if node.bases:
                names.add(f"{node.name}::*")
            names.update(
                f"{node.name}::{item.name}"
                for item in node.body
                if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    return names


def _id_stands(rest: str, names: set[str]) -> bool:
    """Whether a node id's part after the file names a standing test: `test_x[...]` or
    `Class::method[...]` (review row L5-2); a deeper id is judged by its first two parts."""
    parts = rest.split("[", 1)[0].split("::")
    if len(parts) > 1:
        return "::".join(parts[:2]) in names or f"{parts[0]}::*" in names
    return parts[0] in names


def _changed_test_ids(root: Path, env: dict[str, str], posix: str) -> list[str]:
    """In one changed test file, the ids of the test functions that are new or differ from HEAD.

    A file absent at HEAD is selected whole. Helpers, fixtures and classes are not compared: a
    failure reached only through a changed helper waits for `make verify` (decisions.md, Q-3).
    """
    # Absent at HEAD is measured, never inferred from a failing `git show`: a git failure is a
    # selection fault, not a reason to run a changed file whole (review row L6-1).
    if not _git_bytes(root, "ls-tree", "HEAD", "--", posix, env=env).strip():
        return [posix]
    before = _git_bytes(root, "show", f"HEAD:{posix}", env=env).decode("utf-8")
    old = _test_functions(before, posix)
    new = _test_functions((root / posix).read_text(encoding="utf-8"), posix)
    return [f"{posix}::{name}" for name, dump in new.items() if old.get(name) != dump]


def selected_tests(
    root: Path, env: dict[str, str], plan: bytes, previous: Sequence[str] = ()
) -> tuple[list[str] | None, str | None]:
    """The cheap pytest run's explicit targets, deduplicated and sorted, or why they cannot stand.

    Sources (spec, "Selected tests", amended by decisions.md Q-3): in each surviving changed
    `tests/**/test_*.py` file, the test functions that are new or differ from HEAD (a new file
    whole); the accepted plan's ledger test references in both forms, as function ids; and, on a
    retry, the ids `previous` names - the tests pytest reported as failed in the attempt before -
    whose test file and top-level test or class still stand. A test named by the ledger but not yet written stays a target:
    pytest then fails the attempt with the missing id named, which is the attempt's own gap.
    Importers of changed `scripts/` modules are not selected. `None` targets with a reason - a
    selection failure is a diagnostic, never an empty green set (spec, criterion 3).
    """
    try:
        changed = changed_paths(root, env=env)
    except (Refused, OSError) as error:
        return None, str(error)
    targets: set[str] = set()
    try:
        for posix in sorted(relative.as_posix() for relative in changed):
            if _is_test_module(posix) and (root / posix).is_file():
                targets.update(_changed_test_ids(root, env, posix))
        targets.update(_ledger_test_refs(plan))
        standing: dict[str, set[str]] = {}
        for ident in previous:
            posix, _, rest = ident.partition("::")
            if not (_is_test_module(posix) and (root / posix).is_file()):
                continue
            # A failed test the attempt removed or renamed no longer stands: pytest would refuse
            # the run on its id alone (review row L1-12).
            if posix not in standing:
                standing[posix] = _top_level_names((root / posix).read_text(encoding="utf-8"), posix)
            if not rest or _id_stands(rest, standing[posix]):
                # The function, not its parameter: a retry may rename a parameter, and pytest
                # refuses the whole run on an id it no longer collects (review row F6-2).
                targets.add(ident.split("[", 1)[0])
        # A whole file covers its ids, but only those whose function stands in it: a ledger test
        # the new file lacks stays a target, so pytest names it missing (review row L3-1).
        whole = {target for target in targets if "::" not in target}
        names = {posix: _top_level_names((root / posix).read_text(encoding="utf-8"), posix) for posix in whole}
        kept = sorted(
            t
            for t in targets
            if "::" not in t
            or (posix := t.split("::", 1)[0]) not in whole
            or not _id_stands(t.split("::", 1)[1], names[posix])
        )
    except (Refused, OSError, SyntaxError, UnicodeDecodeError, ValueError) as error:
        return None, str(error)
    return kept, None


def cheap_checks(
    root: Path,
    env: dict[str, str],
    plan: Path,
    key: str | None,
    accepted_plan: bytes | None,
    previous: Sequence[str] = (),
) -> list[str]:
    """An attempt's own cheap checks: ruff lint, ruff format check, pytest over the selected tests.

    `previous` is the test ids the attempt before reported as failed, on a retry. Empty when all
    applicable commands are green. A command with no target is skipped (spec,
    criterion 4); a red, an unstartable or an over-bound command returns that one bounded,
    protected diagnostic and the attempt ends before derived preparation and `make verify` (spec,
    criteria 1, 2 and 10). The ledger references come from `accepted_plan` - the accepted plan's
    snapshot; without one the working plan stands in, as a direct `verify_attempt` call does.
    """
    try:
        targets = format_targets(root, env)
    except (Refused, OSError) as error:
        lines = protect_diagnostics(f"the cheap lint targets could not be listed: {error}", key).splitlines()
        return ["\n".join(_shrink(lines, TAIL_LINES))]
    if targets:
        problem = _cheap_ruff(root, env, key, targets)
        if problem:
            return [problem]
    if accepted_plan is None:
        try:
            accepted_plan = plan.read_bytes()
        except OSError as error:
            return [protect_diagnostics(f"the accepted plan could not be read for the cheap tests: {error}", key)]
    tests, fault = selected_tests(root, env, accepted_plan, previous)
    if fault is not None:
        lines = protect_diagnostics(f"the cheap tests could not be selected: {fault}", key).splitlines()
        return ["\n".join(_shrink(lines, TAIL_LINES))]
    if not tests:
        return []
    identity = "`" + " ".join(PYTEST) + "`"
    if not (root / PYTEST[0]).is_file():
        return [protect_diagnostics(f"no pytest interpreter at `{PYTEST[0]}`; `make venv` builds it.", key)]
    try:
        done = launch(
            [*PYTEST, *tests],
            root,
            env,
            key,
            timeout=TOOL_SECONDS,
            limit=f"the runner's tool limit after {TOOL_SECONDS // 60} minutes",
        )
    except StepTimedOut as error:
        # Name what ran, bounded: a timeout has no output of its own (review row L1-10).
        shown = ", ".join(tests[:TAIL_LINES]) + (
            f" and {len(tests) - TAIL_LINES} more" if len(tests) > TAIL_LINES else ""
        )
        return [protect_diagnostics(f"{identity} did not finish: {error}\nselected tests: {shown}", key)]
    except CallFailed as error:
        return [protect_diagnostics(f"{identity} could not be run: {error}", key)]
    if done.returncode:
        return [f"{identity} exited {done.returncode}\n{_cheap_evidence(done, key)}"]
    return []


def must_run_refs(plan: bytes) -> str:
    """The accepted plan's ledger test references as the prompts' must-run list, or why there is none.

    A reference still marked `not yet written` is listed as it stands - the instruction says to
    write it, never that it exists (spec, criterion 7). A ledger that cannot be read names the
    section to follow instead of a list, so the prompt build never fails on it.
    """
    try:
        refs = _ledger_test_refs(plan)
    except (OSError, UnicodeDecodeError, SyntaxError, ValueError):
        return "the plan's criterion ledger could not be read for test names; follow its `## Criterion ledger` section itself"
    if not refs:
        return "none - the plan's criterion ledger names no test; write every test the plan asks for"
    return "\n".join(f"- {ref}" for ref in refs)


MUST_RUN_DELEGATED = (
    "You cannot run commands, so the runner runs this attempt's must-run checks itself, before full "
    "verification: ruff lint and format checks over the changed Python files, then pytest over exactly "
    "the selected tests - the new or changed test functions, the accepted plan's ledger tests and, on a "
    "retry, the tests the attempt before failed. "
    "Write every test the ledger names, including the rows still marked `not yet written`: a missing "
    "ledger test fails the attempt before `make verify`. Execute nothing yourself - delegation to the "
    "runner is the contract, and no extra tool is yours."
)
MUST_RUN_COMMANDS = (
    "Before you hand back, run the must-run checks yourself and leave them green: "
    "`.venv/bin/ruff check --force-exclude --no-cache` and `.venv/bin/ruff format --check "
    "--force-exclude --no-cache` over the Python files you changed, and "
    "`.venv/bin/python3 -m pytest -q -n auto` over the ledger tests below. The runner runs the same cheap "
    "checks and full `make verify` after the call. Findings.md is the runner's audit file: an edit "
    "of it is restored before the checks, so never put a verdict there."
)


def verify_attempt(
    root: Path,
    plan: Path,
    key: str | None = None,
    formatted: list[str] | None = None,
    tools: dict[str, str] | None = None,
    accepted_plan: bytes | None = None,
    previous_failures: Sequence[str] = (),
) -> list[str]:
    """Format, run the cheap checks, clear derivable ledger markers, stamp documents, render, `make verify`.

    Preparation writes to the tree and executes its registry renderer. Before `make verify` the
    runner applies ruff's safe fixes and its formatter to the changed Python files under `scripts/`
    and `tests/`; when `formatted` is given, the step's line lands there. The cheap checks follow:
    read-only ruff lint and format checks, then pytest over the selected tests, with the first red,
    launch error or timeout ending the attempt before the ledger clearing, the derived preparation
    and `make verify` (spec, criteria 1, 2 and 10). Cheap green never replaces full verification.
    Return bounded diagnostics for failed preparation or postconditions, naming the gates that
    blocked. The time section must still be readable; the entry itself is the runner's
    (`run_attempts`), so the model adds none and nothing is compared with the pre-call plan.
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
    except (OSError, RuntimeError, ValueError) as error:
        return [
            f"the criterion ledger of {plan.name} could not be updated: {getattr(error, 'strerror', None) or error}"
        ]
    intended: list[bytes] = []
    problems: list[str] = []
    try:
        # One machine-wide admission before the timed check: queue and memory waits consume no
        # step limit; a refusal is a failed check, never a started one (bead coding-harness-p6mu).
        # Preparation runs under the same admission, so ruff and the check inherit the one verify
        # environment — the format step's ruff is a local child like the `make` below, and the
        # ownership marker matches for both.
        with verify_lock.hold_admission(["make", "verify"]) as owned:
            try:
                # Ruff can normalize `def test_new ():` into the definition the ledger recognizes.
                # Clear against those final bytes, before stamping the plan and verifying (F-1).
                line = format_step(root, env, key, tools)
                if formatted is not None and line is not None:
                    formatted.append(line)
            except (OSError, RuntimeError, ValueError) as error:
                return [
                    f"the criterion ledger of {plan.name} could not be updated: "
                    f"{getattr(error, 'strerror', None) or error}"
                ]
            # The attempt's own cheap checks, before anything derived: a planted fault stops here
            # (bead coding-harness-5tyh). Cheap green continues into the clearing below. They run
            # under the same admission and verify environment as the check (bead coding-harness-p6mu).
            try:
                cheap = cheap_checks(root, verify_lock.inherit_env(env), plan, key, accepted_plan, previous_failures)
            except (OSError, RuntimeError, ValueError) as error:
                # Named as the cheap checks' own failure, never as the ledger's (review row L7-2).
                return [protect_diagnostics(f"{CHEAP_LABEL}: the cheap checks could not run: {error}", key)]
            if cheap:
                return [f"{CHEAP_LABEL}: {entry}" for entry in cheap]
            try:
                check_criterion_ledger.clear_written(root, plan)
            except (OSError, RuntimeError, ValueError) as error:
                return [
                    f"the criterion ledger of {plan.name} could not be updated: "
                    f"{getattr(error, 'strerror', None) or error}"
                ]
            preparation = prepare_derived(root, env, key)
            if preparation:
                return preparation
            try:
                intended = intend_new_files(root, env)
            except (Refused, OSError) as error:
                return [f"the attempt's new files could not be added intent-to-add before `make verify`: {error}"]
            done = launch(
                ["make", "verify"],
                root,
                verify_lock.inherit_env(env),
                timeout=VERIFY_SECONDS,
                limit=f"the runner's step limit after {VERIFY_SECONDS // 60} minutes",
                pass_fds=_lock_fds(owned),
            )
    except verify_lock.VerifyLockError as error:
        problems.append(scrub(f"`make verify` was not started: {error}", key))
    except StepTimedOut as error:
        # A hang the attempt caused is a repairable diagnostic for the next attempt, not a make that
        # could not be started (O188-4 of the #188 review).
        problems.append(f"`make verify` did not finish: {error}")
    else:
        if done.returncode != 0:
            problems.append(f"`make verify` exited {done.returncode}\n{verify_evidence(done, key)}".rstrip())
    finally:
        # The entries were for the gates only: a failed run must not leave them in the operator's index,
        # and a passing one is staged whole by the checkpoint (runner review R-5).
        # Cleanup is a postcondition even when verification passed or timed out.
        try:
            drop_intended(root, intended, env)
        except (Refused, OSError) as error:
            problems.append(f"the attempt's intent-to-add entries could not be removed after `make verify`: {error}")
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


def _held_prefixes(root: Path) -> list[str]:
    """Committed human-decided and runner-held prefixes for checkpoint protection."""
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
    # Case-folded on both sides: on a case-insensitive checkout `.Claude/Rules/` is `.claude/rules/` (O192-2).
    return [path.casefold() for path in [*decided, *RUNNER_HELD]]


def uncommittable(root: Path, change: str, keep: set[Path] | None = None) -> list[str]:
    """The changed paths a stage-2 attempt must not commit, named (R-16 of the review-swarm review).

    The classes come from the committed `provenance.yaml`, never from the tree the attempt wrote:
    a `human-decided` prefix or one of `RUNNER_HELD` is out of a model's reach, the change's own
    folder is not. `keep` holds what the verb may keep changed - a draft's own new ADR under the
    `docs/adr/` prefix is exactly that (P1 of the #192 review).
    """
    spared = {path.as_posix() for path in keep or ()}
    folder = f"plans/changes/{change}/"
    held = _held_prefixes(root)
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
        exposed = remove_changed_credential(
            root, key, ignored_before, findings=root / "plans/changes" / change / "findings.md"
        )
        if exposed:
            raise Refused(credential_message(exposed))
    stamps: set[Path] = set()
    try:
        # A protected document's derived stamp may enter the run, but must not enter its commit.
        # Reclassify both index and disk here: a substantive attempt edit still reaches the guard below.
        held = _held_prefixes(root)
        stamps = {
            path
            for path in changed_paths(root)
            if any(path.as_posix().casefold().startswith(prefix) for prefix in held) and derived_leftover(root, path)
        }
        # Classify without resetting stamps: a later rollback must check its entire batch
        # before even these derived bytes are restored.
        blocked = uncommittable(root, change, set(keep or ()) | stamps)
    except Refused as error:
        # An unreadable map is a failure of this attempt, repairable by the next one - and the edits go
        # first, so nothing the runner could not classify stays in the tree (O192-5). Preserve the
        # classification failure if the rollback itself must refuse.
        try:
            restored = restore_baseline(root, baseline, set(keep or ()) - stamps, ignored_before)
        except RestorationRefused as safety_error:
            preserve_attempt_failure(safety_error, error)
            raise
        raise CheckpointRolledBack(f"{error}; {restored}") from error
    if blocked:
        # The tree goes back to the baseline, but `keep` stands: what the verb itself may keep changed -
        # its change folder, a draft's own new ADR, the findings a human may have touched - is not the
        # refused attempt's to lose (P1 and P2 of the #192 review).
        reason = "the attempt changed paths a stage-2 run does not commit: " + ", ".join(
            f"`{path}`" for path in blocked
        )
        try:
            restored = restore_baseline(root, baseline, set(keep or ()) - stamps, ignored_before)
        except RestorationRefused as safety_error:
            preserve_attempt_failure(safety_error, Refused(reason))
            raise
        raise CheckpointRolledBack(f"{reason}; {restored}")
    if stamps:
        preflight_recovery(
            root, [root / path for path in sorted(stamps)], aliases=alias_baseline(root, baseline, ignored_before)
        )
        for path in sorted(stamps):
            _git_output(root, "restore", f"--source={baseline}", "--staged", "--worktree", "--", path.as_posix())
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
    one call of the requested test failing by an ordinary assertion or pytest's own failed outcome
    (`pytest.fail.Exception`: a DID-NOT-RAISE `pytest.raises`, a DID-NOT-WARN `pytest.warns`, an
    explicit body `pytest.fail`, a subclass included), passing setup and teardown for every selected case and no other outcome
    among the calls. The fixed-code proof runs the same classifier with `passing`: the session must
    have ended as a passing run and every selected call to have passed. Text quoted from the
    record - a foreign selector, a node id - is the caller's to scrub before it reaches a
    diagnostic.
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
            or not isinstance(phase.get("pytest_failed"), bool)
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
            # By the probe's exception-type flags, never by the recorded name: an application class
            # merely named `Failed` refuses, and so does a missing helper's error.
            if not (call["assertion"] or call["pytest_failed"]):
                # One wording for every name: a class merely named `Failed` or `AssertionError`
                # reads as what it is, without a special case per name.
                return (
                    f"the call of `{_one_line(nodeid)}` failed with {call['exception'] or 'an exception'}, "
                    "which is neither Python's AssertionError nor pytest's own failed outcome (pytest.fail.Exception)"
                )
            red = True
        elif call["outcome"] != "passed":
            return f"the call of `{_one_line(nodeid)}` ended {call['outcome']!r}"
    if not passing and not red:
        return "no selected call failed by an assertion or pytest's own failed outcome; the run is green for the requested test"
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
            # One machine-wide admission around the timed proof; queue and memory waits consume
            # none of the proof's time limit (bead coding-harness-p6mu).
            with verify_lock.hold_admission(["pytest", test]) as owned:
                done = launch(
                    [red_first_python(root), "-c", bootstrap, str(probe), test],
                    root,
                    verify_lock.inherit_env(
                        runner_env(
                            foreign_env(
                                {
                                    "STAGE2_RED_REPORT": str(report),
                                    "STAGE2_RED_TOKEN": token,
                                    "STAGE2_RED_SELECTOR": test,
                                }
                            ),
                            root,
                        )
                    ),
                    key,
                    timeout=RED_FIRST_MINUTES * 60,
                    limit="the fixed-code proof time limit",
                    pass_fds=_lock_fds(owned),
                )
            fault = _red_record_fault(_red_report_bytes(report), token, test, passing=True)
            if done.returncode != 0:
                fault = f"pytest ended {done.returncode} on the fixed code" + (f"; {fault}" if fault else "")
            if _ref_targets(root) != refs_before:
                fault = "refs changed while the fixed-code proof ran"
            elif worktree_tree(root) != tree_before:
                fault = "the worktree changed while the fixed-code proof ran"
    except (CallFailed, Refused, OSError, verify_lock.VerifyLockError) as error:
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
    requested test failed by an expectation the test itself states - an ordinary assertion or pytest's
    own failed outcome in any form, for example DID-NOT-RAISE, DID-NOT-WARN or a body `pytest.fail`
    (bead coding-harness-a7m, Q-1 and Q-2) -, every setup and
    teardown passed and no skip, xfail, XPASS, collection error or nonqualifying failure stands among
    them - so a missing dependency failing its fixture refuses instead of certifying the repair (bead
    coding-harness-omp). Never is a
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
                # The machine admission covers the pytest import probe too: it is protected work
                # (bead coding-harness-p6mu), and its waits consume none of the probe's limit.
                with verify_lock.hold_admission(["pytest", "import probe"]) as owned:
                    started = launch(
                        [red_first_python(root), "-c", "import pytest"],
                        tree,
                        verify_lock.inherit_env(runner_env(foreign_env({}), root, tree)),
                        key,
                        timeout=RED_FIRST_MINUTES * 60,
                        limit="the red-first time limit",
                        pass_fds=_lock_fds(owned),
                    )
            except (CallFailed, verify_lock.VerifyLockError) as error:
                outcome = f"{test}: {scrub(str(error), key)}"
            else:
                if started.returncode != 0:
                    outcome = (
                        f"{test}: the red-first interpreter cannot start pytest (exit {started.returncode}); "
                        "the named test did not run"
                    )
        if outcome is None:
            try:
                # The machine admission wraps the red-first pytest run itself; its queue and
                # memory waits consume none of the red-first time limit (bead coding-harness-p6mu).
                with verify_lock.hold_admission(["pytest", selector]) as owned:
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
                        verify_lock.inherit_env(
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
                            )
                        ),
                        key,
                        timeout=RED_FIRST_MINUTES * 60,
                        limit="the red-first time limit",
                        pass_fds=_lock_fds(owned),
                    )
            except (CallFailed, verify_lock.VerifyLockError) as error:
                outcome = f"{test}: {scrub(str(error), key)}"
            else:
                if done.returncode != 1:
                    outcome = (
                        f"{test}: pytest ended {done.returncode} on the baseline's code; "
                        "red first needs exit 1 with an assertion failure or pytest's own failed outcome"
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


def only_scan_records_added(before: str, now: str) -> bool:
    """Whether `now` is `before` plus nothing but the runner's own skipped-scan records.

    `record_credential_scan_skips` appends them at the end of the call record: bookkeeping, not an
    edit of a finding.
    """
    return now.startswith(before) and all(
        not line.strip() or line.startswith("> credential scan skipped ") for line in now[len(before) :].splitlines()
    )


def findings_body_problem(before: str, now: str) -> str | None:
    """Protect the whole file, allowing only the runner's one frontmatter date refresh."""
    if now == before or only_scan_records_added(before, now):
        return None
    masked = _mask_stamp(before, dated=False)
    if masked is not None and _mask_stamp(now, dated=True) == masked:
        return None
    return "findings.md changed outside runner bookkeeping; every finding and earlier attempt's evidence must stand"


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
    status. A finding-shaped id or claimed fix that names no taken row still fails. A taken row's
    claims are its collected lines whose right side starts `fixed` followed by a dash, including
    malformed spacing: explanations beside them are prose, identical claims count once, two distinct
    claims fail as `several fixed lines`, and with
    no claim at all the missing or malformed diagnostics stand as they did (spec, criteria 1-4).
    Every row of
    findings.md must also stand as `before` holds it - the taken rows and the others alike, cell for cell: the runner restores an edit
    outside the taken rows' Status before this check (spec, criterion 8), and the comparison stays as
    the guard that the restore held, so such an edit is never checkpointed (phase 6, F-3; review row L3-2). The pre-call findings body also protects
    other phases and every earlier attempt's evidence; only the frontmatter's one `updated:` date
    may be refreshed by the runner. Only when no problem stands do the red-first runs start, one pytest run
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
        # A claim starts with fixed and a dash, including malformed spacing; other text is report
        # prose (spec, criterion 1). Claims are deduplicated in their normalized form as the parser
        # collected them, before `fixed_status` rewrites anything, so two different claims can never
        # collapse into one (spec, criterion 2); identical repetitions count once, in encounter order.
        claims = list(dict.fromkeys(line for line in given if re.match(r"^fixed\s*[—–-]", line)))
        if not claims:
            # Explanations alone, or a lone malformed line, keep the missing or malformed diagnostic
            # rather than passing as a repair (spec, criterion 4).
            problems.append(f"{ident}: no fixed line" if not given else fixed_status(ident, given[0]))
            continue
        if len(claims) > 1:
            quoted = "; ".join(f"`{claim}`" for claim in claims)
            problems.append(f"{ident}: several fixed lines ({quoted})")
            continue
        outcome = fixed_status(ident, claims[0])
        if outcome.startswith("fixed — "):
            fixes[ident] = outcome
        else:
            # A malformed fixed claim stays a claim: it is validated here, or it conflicted above.
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
        problem = findings_body_problem(findings_before, findings_now)
        if problem:
            problems.append(problem)
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
    *,
    lock_held: bool = False,
) -> None:
    """Mark the record's own row lines the same way, after the checkpoint commit.

    The record lies outside what the file tools reach, so only the runner can write it; a failure
    leaves the statuses unwritten there and names the IDs to mark by hand. The record's ending stays
    as it was read. `repair` holds the record lock for its whole run (`lock_held`); a lone call takes it.
    """
    by_key = {row[0]: row for place, row in taken if place == "record"}
    if not by_key:
        return
    if lock_held:
        _mark_record_rows(change, by_key, fixes, root, marks)
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
        # Findings were marked before the checkpoint; the vanished record cannot be marked (DL-A-5).
        waiting = ", ".join(sorted(by_key))
        raise CallFailed(
            f"the loop record is gone; findings.md already carries the fixed status of {waiting}; "
            "no record was marked. Check these rows in findings.md; the maintainer must decide how to recover the record."
        )
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
        replace_record(record_dir(change, root) / "loop.md", "\n".join(lines) + ending)
    except OSError as error:
        waiting = ", ".join(sorted(by_key))
        raise CallFailed(f"the loop record could not be marked ({error}); mark {waiting} by hand.") from error


# The explorer's role, stated by the runner in every exploration prompt (bead coding-harness-e7m): on
# 2026-10-20 a `--stage2-off` model took itself for the orchestrator, said its Bash tool was disabled and
# asked to be rerun, and wrote no research.
EXPLORER_ROLE = (
    "You are the phase-1 explorer that the runner has already started; you are not the orchestrator and "
    "you run no command. Your tools are read-only (Read, Grep, Glob) and that is all this phase needs; "
    "where the phase prompt says `rg`, use Grep. Read the repository and answer with the research now."
)

_PATH_TOKEN = re.compile(r"/?[\w.\-]+(?:/[\w.\-]+)*/?")


def names_a_repository_file(root: Path, answer: str) -> bool:
    """Whether the answer names at least one file or directory that exists inside the worktree.

    A heuristic: "exists in the worktree" includes ignored files, and `.git` never counts.
    """
    base = root.resolve()
    # A bare word counts only as a file directly at the root (`Makefile`): a folder name such as
    # `tests` or `scripts` also stands in an ordinary refusal ("I cannot run the tests").
    root_files = {entry.name for entry in base.iterdir() if entry.is_file()} if base.is_dir() else set()
    seen: set[str] = set()
    for raw in _PATH_TOKEN.findall(answer.replace("\\", "/")):
        token = raw.rstrip(".-")  # sentence punctuation glued to the end of a path
        if token in seen or token.strip("/") in ("", ".", ".."):
            continue
        if "/" not in token and "." not in token:
            if token in root_files:
                return True
            continue
        seen.add(token)
        # Cap the path-like candidates, so filler words do not hide a later path.
        if len(seen) > 5000:
            break
        try:
            path = (root / token).resolve()
            # exists() raises on a component over the file system's name limit (runner review R-6).
            if path == base or not path.is_relative_to(base) or path.relative_to(base).parts[0] == ".git":
                continue
            if path.exists():
                return True
        except (OSError, RuntimeError, ValueError):
            continue
    return False


def declared_class(root: Path, change: str, klass: str | None) -> str:
    """The one class every available statement states, or the refusal before any call.

    Sources: the explore-only `--class` argument and the `class:` of
    `research.md`'s and `spec.md`'s headers. Every statement that is present
    must name a class and agree with the others - a header that does not
    parse, or a `class:` key with an empty value, is a present statement that
    names none and refuses; an explicit argument does not cure a stated one,
    and none present refuses, because a silently assumed
    small change would keep a large change off the swarm (spec, criteria 3
    and 4).
    """
    folder = root / "plans" / "changes" / change
    found: dict[str, str] = {}
    for name in ("research.md", "spec.md"):
        try:
            text = (folder / name).read_text(encoding="utf-8")
        except FileNotFoundError:
            continue  # not written yet is the normal state before the spec
        except (OSError, UnicodeDecodeError) as error:
            raise Refused(
                f"plans/changes/{change}/{name} cannot be read; repair the file and its class header ({error})."
            ) from error
        match = re.match(r"---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not match:
            if text.split("\n", 1)[0].rstrip("\r") == "---":
                raise Refused(f"plans/changes/{change}/{name}: repair the unterminated front matter header.")
            continue
        try:
            node = yaml.compose(match.group(1), Loader=yaml.SafeLoader)
            if isinstance(node, yaml.MappingNode):
                class_keys = [
                    key for key, _ in node.value if key.tag == "tag:yaml.org,2002:str" and key.value == "class"
                ]
                if len(class_keys) > 1:
                    raise Refused(
                        f"plans/changes/{change}/{name} states class more than once; "
                        "repair the header to contain exactly one `class:` declaration."
                    )
            header = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            header = None
        if not isinstance(header, dict):
            # A present header that does not read is no statement of "no class":
            # it may say `bounded`, so an explicit argument cannot cure it.
            raise Refused(
                f"plans/changes/{change}/{name} has a header that does not read as YAML fields; "
                "the class it states cannot be known."
            )
        if "class" not in header:
            continue
        stated = header["class"]
        if not isinstance(stated, str) or stated not in CLASSES:
            raise Refused(
                f"plans/changes/{change}/{name} states the class '{stated}', which is none of {', '.join(CLASSES)}."
            )
        found[name] = stated
    if klass is not None and klass not in CLASSES:
        raise Refused(f"--class {klass} is none of {', '.join(CLASSES)}.")
    for name, stated in found.items():
        if klass is not None and stated != klass:
            raise Refused(
                f"--class {klass} contradicts the class '{stated}' of plans/changes/{change}/{name}; "
                "the runner does not override a stated class."
            )
    if len(set(found.values())) > 1:
        listing = ", ".join(f"{name} says {stated}" for name, stated in sorted(found.items()))
        raise Refused(f"the stated classes disagree: {listing}.")
    if klass is not None:
        return klass
    if found:
        return next(iter(found.values()))
    raise Refused(
        f"no class is stated for {change}: pass --class <{'|'.join(CLASSES)}> or state `class:` in "
        "research.md's header - a change must say which before phase 1 routes."
    )


def seat_choice(values: list[str] | None) -> dict[str, list[str]] | None:
    """`--seats repository=a,b` and `--seats online=x,y,z` as {trio: models}, or a refusal naming the fault."""
    if not values:
        return None
    choice: dict[str, list[str]] = {}
    for value in values:
        label, sep, models = value.partition("=")
        names = [name.strip() for name in models.split(",") if name.strip()]
        if not sep or not names or label in choice:
            raise Refused(f"--seats takes TRIO=model,model once per trio (repository, online), not `{value}`.")
        choice[label] = names
    return choice


def prepare_explore(root: Path, change: str, klass: str | None = None, seats: list[str] | None = None) -> None:
    """Phase 1, step one for a swarm class: select and probe the six seats and print the report.

    Writes a single-use receipt outside the worktree; `explore <change> --availability-reported <id>`
    consumes it once the maintainer has answered which models to use (Q-18). `seats` carries that answer
    when it differs from the recommendation.
    """
    import stage2_availability

    path = stage2_availability.research_receipt_path(change, sys.modules[__name__], root)
    with stage2_availability.receipt_lock(path):
        path.unlink(missing_ok=True)
    stage2_availability.prepare_research(root, change, sys.modules[__name__], klass, seat_choice(seats))


def explore(
    root: Path,
    change: str,
    stage2_off: str | None = None,
    klass: str | None = None,
    availability_reported: str | None = None,
) -> None:
    """Phase 1: the swarm for a feature or architectural change, GLM Flash for a bounded
    change or a spike, or the explicit Haiku fallback - the answer lands in research.md."""
    if stage2_off is None:
        klass = declared_class(root, change, klass)
        if klass in SWARM_CLASSES:
            import stage2_availability
            import stage2_swarm

            # The reported receipt comes first: no research call, probe or catalog read starts without it.
            selection = stage2_availability.consume_research(
                root, change, availability_reported, sys.modules[__name__], klass
            )
            stage2_swarm.run(root, change, sys.modules[__name__], klass, selection=selection)
            return
        if availability_reported is not None:
            raise Refused(f"--availability-reported belongs to a swarm class; this change is {klass}.")
        endpoint = GLM_FLASH
    else:
        if availability_reported is not None or klass is not None:
            raise Refused("--stage2-off explores without a class or a selection receipt.")
        # The explicit Stage-1 route skips the class entirely: Haiku explores,
        # and only the reason is carried for the later plan (spec, criterion 20).
        endpoint = HAIKU
    ctx = preflight(root, change, endpoint, bead_file="research.md")
    key = None
    route = "stage-1" if stage2_off is not None else "flash"
    if stage2_off is None:
        key = read_secret("GLM_KEY")
        if key is None:
            raise Refused(f"GLM_KEY is not in the secrets file {secrets_path()}.")
    extra = (
        f"{EXPLORER_ROLE} "
        "Report repository facts with source paths as prose ready to append to `research.md`. "
        "Do not design, recommend, edit a file or use review-table formatting."
    )
    prompt = work_prompt(root, "01-explore.md", change, extra)
    begin_work_call(ctx, "explore", endpoint, prompt, 1, route, ctx.research, stage2_off)
    answer = run_work_model(ctx, prompt, endpoint, writable=False, key=key)
    if not names_a_repository_file(root, answer):
        # Research names its sources; an answer that names no file of the repository is a refusal or a
        # question, not research, and is shown rather than appended (bead coding-harness-e7m).
        tail = "\n".join(answer.strip().splitlines()[-40:])
        print(f"explore: the answer, as it came:\n{tail}", file=sys.stderr)
        raise CallFailed("the exploration answer names no file of the repository; nothing was appended")
    append(ctx.research, f"## Runner exploration — {today()}\n\n{quote_research_records(answer.strip())}")
    print(f"explore: answer appended to {ctx.research.relative_to(root)} · route {route}")


def quote_research_records(text: str) -> str:
    """A model answer with every research-swarm/v2 run marker and record fence made inert (deep review RS-1-10).

    The research-handoff gate trusts each well-formed run envelope in `research.md`; only the research runner
    writes one. A single explorer's answer is appended as prose, so a forged envelope or record fence in it is
    quoted: the marker no longer matches the gate's envelope or record syntax and is read as plain text.
    """
    text = re.sub(r"<!--(\s*/?)research-swarm/v2", r"<!--\1research-swarm/v2 (quoted)", text)
    return re.sub(r"(?m)^([ \t]*`{3,}[ \t]*)research-swarm/v2", r"\1quoted-research-swarm/v2", text)


def implementation_prompt(
    ctx: Context, baseline: str, diagnostics: list[str], inputs: dict[Path, bytes] | None = None
) -> str:
    """The accepted inputs, the must-run checks and the bounded evidence from earlier attempts."""
    spec = prompt_input(ctx.folder / "spec.md", inputs)
    plan = prompt_input(ctx.plan, inputs)
    extra = [
        "Implement only the accepted plan with the available file tools. You cannot run commands. "
        "Write no entry under `## Time used` in plan.md: the runner measures this attempt and writes "
        "its span itself. The runner runs `make verify`, stages the result and creates the checkpoint commit.",
        # The references come from the accepted plan's cached snapshot, so a rejected attempt's own
        # plan edits never change the list on a retry (spec, criterion 7).
        "## Must-run checks before handback\n\n"
        + MUST_RUN_DELEGATED
        + "\n\nLedger tests:\n"
        + must_run_refs(plan.encode("utf-8")),
        f"Implementation baseline: {baseline}",
        f"## Accepted spec\n\n{spec}",
        f"## Accepted plan\n\n{plan}",
    ]
    if diagnostics:
        extra.append("## Earlier post-run diagnostics\n\n" + "\n\n".join(diagnostics))
    return work_prompt(ctx.root, "04-implement.md", ctx.change, "\n\n".join(extra), inputs)


# The macOS kernel resolves at most 32 links; the revisit set detects loops separately.
RESTORATION_PARENT_LINK_LIMIT = 32


def restoration_parent_problem(root: Path, path: Path) -> str | None:
    """Why a recovery must not touch `path`, or None when every existing ancestor stands inside.

    Each existing ancestor between the worktree root and the destination is resolved and compared
    with the canonical root by path containment, never string prefixes. One whose resolved location
    falls outside the worktree makes the destination unsafe, including relative or nested links
    and dangling links to missing external targets. A dangling link to a missing target inside the
    worktree remains recoverable when its chain can be resolved. An ancestor whose chain cannot
    be resolved is also unsafe: a resolver that gives up (an error) or
    one that walks in circles (a link loop, self-linked or paired) leaves containment
    unestablishable, which is why the ancestor's link chain is walked by hand instead of trusting a
    resolver's partial answer for a loop. A missing ordinary parent stays recoverable: restoration
    recreates it from trusted bytes, following nothing. The leaf is not followed merely to decide
    containment, so detaching a leaf alias or a hard link stays safe.
    """
    canonical = root.resolve()
    parent = root
    for part in path.relative_to(root).parts[:-1]:
        parent = parent / part
        try:
            standing, link = parent.exists(), parent.is_symlink()
        except OSError:
            return f"{parent.relative_to(root).as_posix()} cannot be resolved"
        if not link and not standing:
            continue
        # The ancestor's link chain is walked by hand with a revisit and hop bound: a resolver's
        # answer for a loop is partial and can name a place inside the worktree, which would hide
        # the escape, and a readlink that fails leaves containment as unestablishable as a loop.
        seen: set[Path] = set()
        probe = parent
        while True:
            try:
                link = probe.is_symlink()
            except OSError:
                return f"{parent.relative_to(root).as_posix()} cannot be resolved"
            if not link:
                break
            if probe in seen:
                return f"{parent.relative_to(root).as_posix()} cannot be resolved"
            if len(seen) >= RESTORATION_PARENT_LINK_LIMIT:
                return (
                    f"{parent.relative_to(root).as_posix()} cannot be resolved "
                    f"(more than {RESTORATION_PARENT_LINK_LIMIT} links)"
                )
            seen.add(probe)
            try:
                target = probe.readlink()
            except OSError:
                return f"{parent.relative_to(root).as_posix()} cannot be resolved"
            try:
                # Resolve the containing directory before interpreting a relative target's `..`:
                # its lexical depth can differ from its real depth through an ancestor link.
                probe = target if target.is_absolute() else probe.parent.resolve() / target
            except (OSError, RuntimeError):
                return f"{parent.relative_to(root).as_posix()} cannot be resolved"
        try:
            resolved = probe.resolve()
        except (OSError, RuntimeError):
            return f"{parent.relative_to(root).as_posix()} cannot be resolved"
        if not resolved.is_relative_to(canonical):
            return f"{parent.relative_to(root).as_posix()} escapes the worktree"
        if not standing and (resolved == parent or resolved in parent.parents):
            return f"{parent.relative_to(root).as_posix()} cannot be resolved"
    return None


def refuse_unsafe_recovery(root: Path, path: Path, *, aliases: AliasBaseline | None = None) -> None:
    """Refuse linked or replaced parents before recovery, including contained unchanged links."""
    problem = restoration_parent_problem(root, path)
    if problem is None:
        problem = changed_alias_problem(root, path.relative_to(root), aliases or ({}, {}))
    if problem is not None:
        raise RestorationRefused(f"restoration of {path.relative_to(root).as_posix()} is refused: its parent {problem}")


def alias_changed(path: Path, local: Path, aliases: AliasBaseline) -> bool:
    """Whether `path` (worktree-relative `local`) is a link the attempt created or changed, or a replaced baseline link."""
    links, ignored = aliases
    before = links.get(local)
    if path.is_symlink():
        if before is not None:
            return path.readlink() != before
        if local in ignored:
            info = path.lstat()
            return (info.st_mtime_ns, info.st_size) != ignored[local]
        return True
    # The ignored snapshot contains leaves, never ordinary directories. Any such baseline
    # entry in a parent position is unsafe, including a link replaced by a file or removed.
    return before is not None or local in ignored


def changed_alias_problem(root: Path, relative: Path, aliases: AliasBaseline) -> str | None:
    """Refuse any baseline/current link or non-directory in a destination's parent chain.

    Missing ordinary directories remain recoverable. Baseline tracked links and ignored
    leaves remain unsafe even when removed or replaced. Never follow a parent link: even
    an unchanged contained link can escape after another member of the batch is restored.
    The destination leaf is excluded, preserving its safe detachment behavior.
    """
    parent = root
    for part in relative.parts[:-1]:
        parent /= part
        local = parent.relative_to(root)
        try:
            if alias_changed(parent, local, aliases):
                return f"{local.as_posix()} is a link the attempt created or changed"
            if parent.is_symlink():
                return f"{local.as_posix()} is a symbolic link (including unchanged baseline links)"
            if parent.exists() and not parent.is_dir():
                return f"{local.as_posix()} is no longer a directory"
        except (OSError, RuntimeError, ValueError):
            return f"{local.as_posix()} cannot be resolved"
    return None


def preflight_recovery(root: Path, destinations: Iterable[Path], *, aliases: AliasBaseline) -> None:
    """Validate the whole batch before mutation; all linked or replaced parents refuse."""
    for path in destinations:
        refuse_unsafe_recovery(root, path, aliases=aliases)


def restore_work_input(root: Path, path: Path, content: bytes) -> None:
    """Restore an input beneath ordinary parents, detaching aliases only at the leaf.

    Raise RestorationRefused before any tree write if a parent escapes the worktree or cannot
    be resolved, is linked or replaced; otherwise detach the leaf before restoring the input.
    """
    refuse_unsafe_recovery(root, path)
    parent = root
    for part in path.relative_to(root).parts[:-1]:
        parent /= part
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


def preserve_attempt_failure(error: RestorationRefused, original: BaseException | None) -> None:
    """Keep both causes visible without permitting recovery or hiding a call's failure exit."""
    if original is not None:
        error.args = (f"{error}; the attempt's own failure stands: {original}",)
        error.exit_code = 1 if isinstance(original, CallFailed) else 2


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

    A restoration safety refusal is the explicit exception to all of this: the parent check runs
    before any write, retry or direct, and the refusal propagates unwritten instead of an entry.
    """
    # The parent check stands before the first time write of either path: persistence must not act
    # through a parent outside the worktree, and must not be written after such a refusal.
    try:
        refuse_unsafe_recovery(root, plan)
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
        except RestorationRefused:
            raise
        except (Refused, OSError, UnicodeDecodeError, RuntimeError):
            if accepted:
                raise
            # A rejected attempt left the plan missing, unreadable or aliased: the trusted pre-call
            # plan takes the entry, aliases detached, parents repaired, never through a link.
            restore_work_input(root, plan, with_time_entry(prior, entry).encode("utf-8"))
        stamp_updated(plan)
    except RestorationRefused as error:
        preserve_attempt_failure(error, original)
        raise
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
    retain_answer: bool = False,  # repair: every attempt's protected answer is saved before any check can stop the run
) -> None:
    """The attempt loop the work verbs share: call, measure, check, commit - or leave the diagnostics.

    A failed attempt leaves its diagnostics and the files its model changed, quoted, below its audit
    line in `findings.md`; the route block on `stage-1` names the verb. A verb that passes
    `snapshot_findings` and `restore_findings` puts findings.md back as it stood right before the model
    call whenever an attempt fails: the audit line above the snapshot stays, the model's own edits to
    the file - a Status it wrote itself included - go, so no failed run leaves them behind (phase 6,
    F-2). Before the failure is decided, findings.md is restored outright: every post-run check, cheap
    or full, reads the runner's file, an edit alone fails nothing, and a completed attempt that edited
    it carries a quoted restore notice under its audit line (spec, criteria 8 and 9).

    A verb that passes `retain_answer` keeps every attempt's full answer: right at the model-return
    boundary, before any HEAD check, verification or answer check can stop the run, the protected
    answer is saved as local evidence and its location joins the attempt's diagnostics - the parser's
    rejections, the call and verify failures included - and is printed on success (bead
    coding-harness-hgvp). A failed call keeps the output it returned.

    The failed-check listing and the changed-file entries pass through `protect_diagnostics` once, on
    every route, the keyless ones included; the block in findings.md and the retry prompt both take that
    one safe text, so a fixture secret a check printed blocks neither the next attempt's leak check nor
    its prompt (bead coding-harness-8hr).

    A completed call keeps its measured time whatever stops the run afterwards: every post-call exit
    - a refusal, an unreadable or moved HEAD, an unstartable or refusing verifier, diagnostic
    protection - passes one finalization boundary that persists the attempt's one rejected entry
    through `persist_time_entry`, then lets the original refusal or failure stand (bead
    coding-harness-9wp). A call that never completed - a `CallFailed` result, an empty Codex answer
    included - gets no entry, as preflight refusals get none. The restoration safety refusal
    (`RestorationRefused`) is the explicit exception: every recovery batch stands checked before its
    first write, and the refusal propagates unwritten - no entry, no findings restore, no cleanup
    after it (bead coding-harness-10w).
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
    # The tests pytest reported as failed in the attempt before; the next cheap run selects them too.
    previous_failures: list[str] = []
    # The tools the runner itself starts, as they were before the first model ran. One digest for the
    # whole run: an attempt that overwrote a tool is refused, and the refused bytes must not become the
    # next attempt's reference by taking the digest again (P1 of the #188 review).
    tools = tool_state(root) if tools is None else tools
    # The links standing before the first call; recovery refuses any it finds created or changed (Q-2).
    aliases = alias_baseline(root, baseline, ignored_before)
    # One token per invocation: every attempt's evidence file carries it beside its attempt number,
    # so a rerun of the verb never overwrites an earlier run's evidence (spec, criterion 6).
    token = f"{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%S%fZ')}-{os.urandom(4).hex()}" if retain_answer else ""
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

        def put_findings_back(
            original: BaseException | None = None,
            kept=kept,
            destinations=(*inputs_before, ctx.findings),
        ) -> None:
            """Put findings.md back, refusing first when its parent would carry the write outside."""
            # Even implement (without a findings snapshot) must validate the complete batch
            # before its caller can append diagnostics or finalize time on an early exit.
            try:
                preflight_recovery(root, destinations, aliases=aliases)
            except RestorationRefused as safety_error:
                preserve_attempt_failure(safety_error, original)
                raise
            if kept is not None:
                restore_findings(kept)

        unmeasured: str | None = None
        try:
            before = worktree_tree(root)
        except (Refused, OSError) as error:
            before, unmeasured = "", str(error)
        call_error: CallFailed | None = None
        answer = ""
        evidence: str | None = None
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
            if retain_answer:
                # Before the HEAD checks, verification or the answer check can stop the run: the
                # whole answer, a failed call's available output included, protected once for the
                # route it arrived on. A protection or write failure raises and stops the run with
                # no checkpoint (spec, criteria 6 and 8).
                output = answer if completed else (call_error.partial_answer if call_error is not None else "")
                try:
                    evidence = save_answer_evidence(root, ctx.change, token, attempt, output, key)
                except (Refused, CallFailed, OSError) as evidence_error:
                    # Evidence is a terminal boundary, but the model's edits still need the same
                    # recovery as a failed call. Keep both failures and the snapshot location.
                    # The whole recovery batch stands checked before findings are restored, the
                    # credential removed or the attempt saved: a refusal leaves it unwritten.
                    # As in the normal HEAD check, never rewrite a commit made by the model.
                    try:
                        moved = endpoint == CODEX and _git_output(root, "rev-parse", "HEAD").strip() != baseline
                    except Refused:
                        moved = True
                    try:
                        planned = None if moved else plan_baseline_restore(root, allowed, ignored_before, baseline)
                    except RestorationRefused as safety_error:
                        preserve_attempt_failure(safety_error, evidence_error)
                        raise
                    put_findings_back(original=evidence_error)
                    exposed = remove_changed_credential(root, key, ignored_before) if key is not None else []
                    try:
                        saved = save_attempt(root, baseline, ctx.change, f"{verb}-attempt-{attempt}")
                    except OSError as save_error:
                        saved = f"saving the attempt failed ({save_error})"
                    restored = (
                        "HEAD moved or could not be read; history was not rewritten"
                        if moved
                        else restore_baseline(root, baseline, allowed, ignored_before, planned=planned)
                    )
                    failures = [str(call_error)] if call_error is not None else []
                    failures += [str(evidence_error), saved, restored]
                    if exposed:
                        failures.append(credential_message(exposed))
                    failure_type = Refused if isinstance(evidence_error, Refused) else CallFailed
                    raise failure_type("; ".join(failures)) from evidence_error
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
                    try:
                        put_findings_back()
                    except RestorationRefused as safety_error:
                        # No audit may be written after this refusal, so carry the
                        # unverified commit in stderr rather than lose the HEAD stop.
                        safety_error.args = (f"{safety_error}; {problem}",)
                        raise
                    listing = f"- {problem}"
                    if call_error is not None:
                        listing += f"\n- {call_error}"
                    if retain_answer and evidence is not None:
                        listing += f"\n- the attempt's protected answer is saved at {evidence}"
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
                            whole=[line for line in listing.splitlines() if evidence and evidence in line],
                        ),
                    )
                    raise CallFailed(problem) from call_error
            if call_error is not None:
                error = call_error
                # The whole failed-call recovery stands behind the parent check: the baseline
                # rollback and cleanup destinations are validated before findings are restored or
                # the attempt is saved, so a refusal leaves the branch without a single write.
                preflight_recovery(root, {**inputs_before, ctx.findings: findings_before}, aliases=aliases)
                planned = plan_baseline_restore(root, allowed, ignored_before, baseline)
                put_findings_back()
                exposed = []
                if key is not None:
                    # Scrub before the snapshot writes the changed files into the object store.
                    exposed = remove_changed_credential(root, key, ignored_before, findings=ctx.findings)
                try:
                    saved = save_attempt(root, baseline, ctx.change, f"{verb}-attempt-{attempt}")
                except OSError as save_error:
                    saved = f"saving the attempt failed ({save_error})"
                restored = restore_baseline(root, baseline, allowed, ignored_before, planned=planned)
                leaked = f"; {credential_message(exposed)}" if exposed else ""
                ended = f"{error}; {saved}; {restored}{leaked}"
                if retain_answer and evidence is not None:
                    ended += f"\nthe attempt's protected answer is saved at {evidence}"
                raise CallFailed(ended) from error
            # What the attempt itself left in findings.md, read before the runner's scan below can append
            # its own skipped-scan record (review rows L1-2, L5-3).
            try:
                findings_after_call: bytes | None = ctx.findings.read_bytes()
            except OSError:
                findings_after_call = None
            if key is not None:
                # Every route scans with the key read in this run - the Sonnet fallback included - before
                # the second snapshot can write the changed files into the object store (spec, criterion 9).
                exposed = remove_changed_credential(root, key, ignored_before, findings=ctx.findings)
                if exposed:
                    error = Refused(credential_message(exposed))
                    put_findings_back(original=error)
                    raise error
            if unmeasured is None:
                # Both snapshots stand around the model call alone: the runner's own writes - the audit
                # line, the route block, the preparation, the block below - fall outside both of them.
                try:
                    files: list[str] | str = attempt_files(root, before, worktree_tree(root))
                except (Refused, OSError) as error:
                    files = str(error)
            else:
                files = unmeasured
            # findings.md is runner-owned: an attempt's edits to its own audit file go back before any
            # post-run check reads model-written state, so the edit alone never spends the attempt
            # (spec, criterion 8). The whole batch stands checked before the first write; a refusal
            # propagates unwritten, as every recovery refusal does.
            findings_restored = False
            # Measured before the restore below: writing findings.md recreates its parents, and a
            # change folder the model deleted must still bring every snapshotted input back.
            parent_gone = not ctx.plan.parent.is_dir()
            if kept is not None:
                # Judged on the bytes the attempt left, before the runner's scan appended anything: the
                # runner's own record is never the attempt's edit, and a line the attempt shaped like
                # one is (review rows L1-2, L5-3).
                unchanged = findings_after_call == findings_before
                if not unchanged:
                    preflight_recovery(root, {**inputs_before, ctx.findings: findings_before}, aliases=aliases)
                    restore_findings(kept)
                    findings_restored = True
            cannot_start: CallFailed | None = None
            formatted: list[str] = []
            try:
                problems = verify_attempt(root, ctx.plan, key, formatted, tools, inputs[ctx.plan], previous_failures)
            except Refused as error:
                put_findings_back(original=error)
                raise
            except CallFailed as error:
                # `make verify` could not be started: no model can repair that, so this attempt's block
                # says why and the run stops after the scan below, with no further attempt (spec, criterion 6).
                put_findings_back(original=error)
                cannot_start = error
                lines = protect_diagnostics(str(error), key).splitlines() or ["make could not be started"]
                problems = ["`make verify` could not be run\n" + "\n".join(_shrink(lines, TAIL_LINES))]
            except (OSError, RuntimeError, ValueError) as error:
                # A model that deleted or replaced its own inputs must not break the attempt boundary:
                # the checks' unexpected filesystem failure is this attempt's diagnostic, the inputs go
                # back through the batch restore below, and the verdict stays rejected (F-5).
                put_findings_back()
                problems = [protect_diagnostics(f"the post-run checks could not run: {error}", key)]
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
            # The complete input/findings batch is checked before the first recovery, diagnostic or
            # retry-time write of the boundary below: a safe plan must not be logged or restored
            # before an unsafe later destination stops the batch (spec, criterion 1).
            batch = {**inputs_before, ctx.findings: findings_before}
            try:
                preflight_recovery(root, batch, aliases=aliases)
            except RestorationRefused as safety_error:
                if problems:
                    preserve_attempt_failure(safety_error, Refused(protect_diagnostics("\n".join(problems), key)))
                raise
            if aliased_parent or parent_gone or not ctx.plan.parent.is_dir():
                # Detach an alias itself, never a document in its target; recreate missing parents too.
                # Restore the snapshotted inputs and audit before diagnostics, logging or retry writes.
                for path, content in batch.items():
                    restore_work_input(root, path, content)
            if not problems and answer_check is not None:
                problems = answer_check(answer)
            if problems:
                previous_failures = failed_test_ids(problems)
                # The restore note stands first, then the format line: the next model learns that its
                # findings edits went back, that the runner formatted, and what failed after.
                problems = [
                    *([FINDINGS_RESTORED] if findings_restored else []),
                    *(f"{FORMAT_LABEL}: {line}" for line in formatted),
                    *problems,
                ]
                if retain_answer and evidence is not None:
                    # The locator stands last, so tailing the listing keeps it even where the
                    # displayed diagnostics are cut (spec, criterion 7).
                    problems.append(f"the attempt's protected answer is saved at {evidence}")
                # Before the block is appended, so the quoted diagnostics stand beside the rows as
                # they were, not beside the model's edits of them. The parent check inside
                # `put_findings_back` refuses first when the destination escapes the worktree.
                listing = protect_diagnostics("\n".join(f"- {p}" for p in problems), key)
                put_findings_back(original=Refused(listing))
                # The block lands below this attempt's audit line, before the next attempt starts or the
                # run exits 1; the post-run scan after it covers the block too (spec, criteria 1 and 9).
                # One safe listing and one safe file list feed both destinations (the block and the retry prompt).
                files = protect_files(files, key)
                diagnostics.append(f"Attempt {attempt} ({route}):\n{listing}")
                append(
                    ctx.findings,
                    quote_block(
                        attempt_block(attempt, route, listing, files),
                        key,
                        # Conflict diagnostics already passed protection above. Keep every quoted
                        # claim, even when a long preceding reason would push it past the line cut.
                        whole=[
                            line
                            for line in listing.splitlines()
                            if (evidence and evidence in line) or (retain_answer and ": several fixed lines (" in line)
                        ],
                    ),
                )
            record += [protect_diagnostics(f"- Attempt {attempt} ({route}): {line}", key) for line in formatted]
            exposed = []
            if key is not None:
                # The gate runs repository code the model just edited: scan again after it and the
                # diagnostic block, before finalizing either the verdict or its measured endpoint.
                exposed = remove_changed_credential(root, key, ignored_before, findings=ctx.findings)
                if exposed:
                    if not problems:
                        put_findings_back(original=Refused(credential_message(exposed)))
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
                if findings_restored:
                    # The restore is part of this attempt's record: the quoted notice lands under its
                    # audit line and is committed with the checkpoint - never a failed label, never a
                    # fabricated review row (spec, criterion 9).
                    append(ctx.findings, quote_block(FINDINGS_RESTORED_NOTICE, key))
                if before_commit is not None:
                    before_commit()
                message = commit_message
                if record:
                    # The subject stays the subject; the format line of every attempt that ran the step
                    # stands below the heading, in the commit that holds the formatted bytes.
                    message = commit_message + "\n\n" + FORMAT_COMMIT_HEADING + "\n" + "\n".join(record)
                try:
                    checkpoint(root, ctx.change, baseline, key, ignored_before, message=message, keep=allowed)
                except CheckpointRolledBack:
                    # `before_commit` may have written statuses (a repair's `fixed — <test>`) that the
                    # refused commit's restore just undid the work for; findings.md is kept by that
                    # restore, so it goes back here (bead coding-harness-rcyf). Only while no commit
                    # exists: after one, HEAD holds those statuses. A `Refused` stop (a credential, a
                    # recovery the maintainer decided writes nothing) is never followed by a write
                    # (runner review R-4). The explicit rollback signal excludes a failed `git commit`
                    # that left the fix in place (P240-1). Unrelated leftovers, such as nested Git
                    # repositories skipped by git clean, do not preserve statuses for removed fixes.
                    try:
                        moved = _git_output(root, "rev-parse", "HEAD").strip() != baseline
                    except Refused:
                        moved = True
                    if kept is not None and not moved:
                        restore_findings(kept)
                    raise
                if after_commit is not None:
                    after_commit()
                if retain_answer and evidence is not None:
                    print(f"{verb}: the attempt's protected answer is saved at {evidence}")
                print(f"{verb}: verified and committed · route {route} · attempt {attempt}")
                return
            if attempt < len(routes):
                # Failed edits stay in the attempt's evidence. Restore every differing snapshotted input
                # before the next attempt, comparing bytes so undecodable files are restored too.
                # The plan comes back at its pre-call bytes plus this attempt's runner entry.
                # Restoration never writes through a worktree path: whatever stands there (a symlink, a
                # directory or a file) is removed without being followed, then the bytes are written anew.
                # The batch stands rechecked at this recovery boundary; a refusal leaves it unwritten.
                preflight_recovery(root, inputs_before, aliases=aliases)
                for path, content in inputs_before.items():
                    restore_work_input(root, path, content)
                stamp_updated(ctx.plan)
        except BaseException as error:
            # Include interrupts: an exceptional departure of a completed attempt logs first,
            # rejected, unless the verdict's own write already ran - and the original refusal
            # or failure then stands as it was. Logging itself failing fails closed, with the
            # attempt's own failure as the cause. A restoration safety refusal is the explicit
            # exception: persisting time or findings after it would write against the no-write
            # stop, so it propagates without an entry (spec, criterion 5).
            if isinstance(error, RestorationRefused) and call_error is not None:
                preserve_attempt_failure(error, call_error)
            if completed and not logged and not isinstance(error, RestorationRefused):
                try:
                    preflight_recovery(root, {**inputs_before, ctx.findings: findings_before}, aliases=aliases)
                except RestorationRefused as safety_error:
                    preserve_attempt_failure(safety_error, error)
                    raise
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
    refuse_preexisting(root, allowed)
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
    standing: dict[str, str] = {}

    def snapshot() -> str:
        text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
        standing["text"] = text
        return text

    def check(_answer: str) -> list[str]:
        # The implementing model writes code, never loop state. The runner puts findings.md back
        # before this check (spec, criterion 8), so a model edit alone never fails here; the
        # comparison stays as the guard that the restore held (review row L3-2).
        now = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
        problem = findings_body_problem(standing.get("text", ""), now)
        return [problem] if problem else []

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
        answer_check=check,
        snapshot_findings=snapshot,
        restore_findings=lambda text: restore_work_input(root, ctx.findings, text.encode("utf-8")),
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
    # Draft rollback is outside restore-symlink-parent's scope (spec non-goal); unlike the
    # implementation/repair restore_baseline, it has no restoration-parent preflight.
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
        # One machine-wide admission before the timed check: queue and memory waits consume no
        # step limit; a refusal is a failed check, never a started one (bead coding-harness-p6mu).
        with verify_lock.hold_admission(["make", "verify"]) as owned:
            done = launch(
                ["make", "verify"],
                root,
                verify_lock.inherit_env(env),
                timeout=VERIFY_SECONDS,
                limit=f"the runner's step limit after {VERIFY_SECONDS // 60} minutes",
                pass_fds=_lock_fds(owned),
            )
    except (CallFailed, verify_lock.VerifyLockError) as error:
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
    refuse_preexisting(root, allowed)
    baseline = _git_output(root, "rev-parse", "HEAD").strip()
    # The derived leftovers the run started with: put back with the rest, but never blamed on the model.
    started_with = {path for path in changed_paths(root) if derived_leftover(root, path)}
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
            exposed = remove_changed_credential(root, key, ignored_before, against=baseline, findings=ctx.findings)
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
        put = [path for path in put if Path(path) not in started_with]
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
            exposed = remove_changed_credential(root, key, ignored_before, against=baseline, findings=ctx.findings)
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
    """The implement contract with the repair block: the format, the must-runs, the baseline, the rows."""
    rows = "\n".join(f"- {row[0]} [{row[1]}, {row[2]}] {row[4]}: {row[5]} — Status: {row[7]}" for _, row in taken)
    spec = prompt_input(ctx.folder / "spec.md", inputs)
    plan = prompt_input(ctx.plan, inputs)
    extra = [
        REPAIR_FORMAT if endpoint == CODEX else REPAIR_FORMAT_FILE_TOOLS,
        # A command-capable Codex runs the must-runs itself; the file-tools route delegates the same
        # checks to the runner. The references come from the accepted plan's cached snapshot, so a
        # retry rereads nothing the attempt may have edited (spec, criterion 7).
        "## Must-run checks before handback\n\n"
        + (MUST_RUN_COMMANDS if endpoint == CODEX else MUST_RUN_DELEGATED)
        + "\n\nLedger tests:\n"
        + must_run_refs(plan.encode("utf-8")),
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
    refuse_preexisting(root, allowed)
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
        after_commit=lambda: mark_repaired_record(change, taken, fixes, root, marks, lock_held=True),
        snapshot_findings=snapshot,
        restore_findings=lambda text: restore_work_input(root, ctx.findings, text.encode("utf-8")),
        tools=tools,
        retain_answer=True,
    )


def prepare_loop(root: Path, change: str) -> None:
    """Check reachable admitted reviewers and return the main-conversation report."""
    import stage2_availability

    stage2_availability.prepare(root, change, sys.modules[__name__])


_RATE_LIMITED = re.compile(r"(?<![\w-])429(?![\w-])|rate[ _-]?limit|too many requests|\bunavailable\b", re.IGNORECASE)


class FreeStageUnavailable(Exception):
    """Every member of a free round failed with a rate-limit or unavailability error (bead coding-harness-pj98)."""


def rate_limited(outcome: object) -> bool:
    """Whether a member's failure is a rate limit or an unavailable endpoint, not a time-out or another exit."""
    # Only a failed exit counts: an empty answer carries the last stderr line too, and a warning that
    # names 429 beside an empty answer is no rate limit (pre-review row P247-1).
    return (
        isinstance(outcome, CallFailed)
        and not isinstance(outcome, StepTimedOut)
        and str(outcome).startswith("pi call failed: exit ")
        and _RATE_LIMITED.search(str(outcome)) is not None
    )


@capture_terms_warnings()
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
    if record is not None:
        refusal = released_overlap_refusal(record, findings_text)
        if refusal:
            raise Refused(refusal)
    if record is None:
        refusal = lost_record_refusal(change, root, findings_text)
        if refusal:
            raise Refused(refusal)
    # The snapshot before the stops: a released block without the runner's snapshot is refused here,
    # never read as a finished run (DL-A-2 of the deep review).
    state = None if restarted_fresh(record, findings_text) else read_state(record, findings_text)
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
    # Warn before admission and leak checks can refuse a call, including saved runs.
    for warning in retain_terms_warnings(terms_warnings(endpoint_entry(root))):
        print(f"review-loop: Notice: {warning}.", file=sys.stderr)
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
    while True:
        stage = next_stage(state)
        free_input = None
        free_cut: str | None = None
        if stage is not None and stage["kind"] == "free":
            free_input, free_cut = free_diff(root)
            if not free_input.strip():
                state["free"]["skipped"] = "free stage skipped: no implementation source diff"
                print(f"review-loop: {state['free']['skipped']}")
                stage = next_stage(state)
        if stage is None:
            message = (
                "every stage of this run is consumed and the last round was not clean; the loop stops and "
                "reports to the maintainer. No model is substituted."
            )
            # A run whose declaration names paid models while its snapshot holds no paid stage would
            # stop without saying why: every reading was excluded at snapshot time (spec criteria 3
            # and 9). Name each exclusion, so the spent run reports the expiry, not a bare stop.
            try:
                entry = endpoint_entry(root)
            except Refused:
                entry = None
            if entry is not None:
                declared = [str(model) for model in entry.get("modelle") or []]
                paid = state["paid"]
                if declared and not (paid.get("ladder") or paid.get("flash") or paid.get("rungs")):
                    problems = "; ".join(
                        reason
                        for model in dict.fromkeys(declared)
                        if (reason := terms_problem(entry, model)) is not None
                    )
                    if problems:
                        message = (
                            "every stage of this run is consumed and the last round was not clean; no paid "
                            f"model of the declaration is admissible: {problems}. The loop stops and reports "
                            "to the maintainer. No model is substituted."
                        )
            raise Refused(message)
        # The orchestrator decides and repairs before another review (ADR 0021, decision 6): a taken row of
        # this run that no repair has marked `fixed` holds the next round (DL-A-8 of the deep review). Spent
        # stages stop first: there is no next round to hold.
        unrepaired = [
            row[0] for number in sorted(history) for row in history[number] if row[7].lower().startswith("taken")
        ]
        if unrepaired:
            raise Refused(
                f"taken rows are not repaired yet ({', '.join(unrepaired)}); run `repair` and make `make verify` "
                "green before the next round starts."
            )
        try:
            _review_round(root, change, record, findings_text, state, stage, free_input, free_cut, receipt_taken)
            return
        except FreeStageUnavailable as dropped:
            # Every free member was rate-limited or unavailable at review size: the run drops the free
            # stage and the next stage takes this call's round; the snapshot written with that round
            # holds the drop, so no later call starts the free members again (bead coding-harness-pj98).
            state["free"]["skipped"] = f"free stage skipped: {dropped}"
            print(f"review-loop: {state['free']['skipped']}")
            if next_stage(state) is None:
                # Without a paid stage the drop has no round to be written with (pre-review row P247-3).
                raise Refused(
                    f"{dropped}; no paid stage of this run is left to take the round, so nothing is written "
                    "and the next call starts the free members again. The maintainer decides what continues."
                ) from None


@capture_address_notices()
def _review_round(
    root: Path,
    change: str,
    record: str | None,
    findings_text: str,
    state: dict,
    stage: dict,
    free_input: str | None,
    free_cut: str | None,
    receipt_taken: bool,
) -> None:
    """One round of `review_loop` on its chosen stage: prompts, calls, the written round."""
    round_number = rounds_run(record, findings_text) + 1
    members: list[str] = stage["members"]
    free = stage["kind"] == "free"
    cut_note: str | None = None
    if free:
        diff, cut_note = bounded_review_diff(free_input)
        # The free diff's own bounds cut before the prompt's bound does; both cuts belong to the round.
        cut_note = "; ".join(note for note in (free_cut, cut_note) if note) or None
    else:
        diff, cut_note = bounded_review_diff(change_diff(root))
    body = "" if free else (root / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8")
    prompts: dict[str, str] = {}
    endpoints: dict[str, tuple[str, str, str]] = {}

    def prompt_for(member: str) -> str:
        head = f"This is round {round_number}; you are `{member}`."
        if free:
            return free_round_prompt(head, diff)
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
    audited = 0
    notes: list[str] = []
    malformed_blocks: list[str] = []
    try:
        key = reviewer_key()
        if not state["consumed"]:
            if state["free"].get("skipped"):
                notes.append(f"Notice: {state['free']['skipped']}.")
            if state["free"].get("dropped"):
                notes.append(f"Notice: free ids dropped: {dropped_notice(state['free']['dropped'])}.")
            for notice in state["free"].get("notices") or []:
                # A same-host path move observed at discovery stays in the
                # round's notes: the move is evidence, not a transient line.
                notes.append(f"Notice: {notice}.")
                print(f"review-loop: {notes[-1]}", file=sys.stderr)
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
        # Terms are evaluated on every round, fresh, legacy or resumed ([DETAIL],
        # 2026-10-26): review_loop prints advance notice before admission checks.
        # Keep current warnings in the round notes too, so the record and the
        # released findings carry them. A warning neither admits nor refuses a member.
        for warning in retain_terms_warnings(terms_warnings(endpoint_entry(root))):
            notes.append(f"Notice: {warning}.")
        # Expiry once more, immediately before the launch: a member whose terms
        # expired after the batch checks above refuses the round here, without a
        # call and without touching the run's history (spec criterion 5).
        if not free:
            entry = endpoint_entry(root)
            for member in members:
                problem = terms_problem(entry, member)
                if problem:
                    raise Refused(problem)
        # Audit only after the final admission check allows the initial dispatch.
        if not ctx.findings.exists():
            ctx.findings.write_text(findings_header(ctx, producer_for(endpoints[members[0]])), encoding="utf-8")
        for member in members:
            append(ctx.findings, call_line("review-loop", endpoints[member], checked[member]))
            audited += 1
        # One deadline for the round: a replacement must live inside it, or a round could take a member
        # limit per call (R-8 of the review-swarm review).
        deadline = time.monotonic() + REVIEWER_MINUTES * 60
        answers = run_swarm(ctx, members, prompts, key, free=free, deadline=deadline)
        replaced: list[str] = []

        def ask_malformed_again(member: str) -> None:
            """Retry each initial or replacement member once, before replacing a failure."""
            nonlocal audited
            first = answers[member]
            if not isinstance(first, MalformedAnswer):
                return

            def expired() -> bool:
                if time.monotonic() < deadline:
                    return False
                notes.append(f"{member} failed: {first}; the round time limit expired; no second call starts")
                print(f"review-loop: {notes[-1]}", file=sys.stderr)
                return True

            if expired():
                return
            retry_prompt = "\n\n".join([prompts[member], FORMAT_REMINDER, ANSWER_FORMAT])
            checked_retry = checked_prompt(ctx, endpoints[member], retry_prompt, _free_admission(free, state))
            # Checking the prompt must neither claim a call nor buy extra round time.
            if expired():
                return
            append(ctx.findings, call_line("review-loop", endpoints[member], checked_retry))
            audited += 1
            notes.append(f"{member} was asked again with the format reminder: the first answer was malformed")
            print(f"review-loop: {notes[-1]}", file=sys.stderr)
            malformed_blocks.append(
                f"From {member}:\n\n{member}'s first answer, which was not in the required format:\n\n"
                f"{NOT_ROWS_NOTE}\n\n{quote_reviewer(first.answer.strip())}"
            )
            answers.update(run_swarm(ctx, [member], {member: retry_prompt}, key, free=free, deadline=deadline))
            second = answers[member]
            if isinstance(second, MalformedAnswer):
                malformed_blocks.append(
                    f"From {member}:\n\n{member}'s second answer, which was not in the required format:\n\n"
                    f"{NOT_ROWS_NOTE}\n\n"
                    f"{quote_reviewer(second.answer.strip())}"
                )

        for member in members:
            ask_malformed_again(member)
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
                    endpoints[nxt] = (OPENCODE, nxt, "max")
                    prompts[nxt] = prompt_for(nxt)
                    try:
                        checked[nxt] = checked_prompt(ctx, endpoints[nxt], prompts[nxt], None)
                    except AdmissionRefused as refusal:
                        # A rung the declaration now refuses is named and passed over: the members' answers
                        # stand, and the rung is neither called nor consumed (DL-B-1 of the loop's deep review).
                        notes.append(f"{nxt} not admitted: {refusal}")
                        print(f"review-loop: {notes[-1]}", file=sys.stderr)
                        continue
                    if time.monotonic() >= deadline:
                        # The leak check can outlast the round: a replacement that cannot start writes no
                        # call line and is not consumed (DL-B-10).
                        notes.append(
                            f"{current} failed: {reasons[current]}; the round time limit expired; no replacement starts"
                        )
                        print(f"review-loop: {notes[-1]}", file=sys.stderr)
                        break
                    notes.append(f"{current} failed: {reasons[current]}; replaced by {nxt}")
                    print(f"review-loop: {notes[-1]}", file=sys.stderr)
                    append(ctx.findings, call_line("review-loop", endpoints[nxt], checked[nxt]))
                    audited += 1
                    answers.update(run_swarm(ctx, [nxt], prompts, key, free=False, deadline=deadline))
                    if isinstance(answers[nxt], NotStarted):
                        notes.append(f"{nxt} did not start: {answers[nxt]}; it is not consumed")
                        print(f"review-loop: {notes[-1]}", file=sys.stderr)
                        break
                    replaced.append(nxt)
                    ask_malformed_again(nxt)
                    current = nxt
            members = [*members, *replaced]
        succeeded = [member for member in members if not isinstance(answers[member], BaseException)]
        if free and not succeeded and all(rate_limited(answers[member]) for member in members):
            raise FreeStageUnavailable(
                "every free member was rate-limited or unavailable: "
                + "; ".join(f"{member} failed: {answers[member]}" for member in members)
            )
        if not succeeded:
            raise CallFailed("; ".join(f"{member} failed: {answers[member]}" for member in members))
        numbered: list[list[str]] = []
        statements: list[str] = []
        reviewer_blocks: list[tuple[str, str]] = []
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
                reviewer_blocks.append((member, kept.strip()))
        if cut_note:
            statements.append(
                f"{CUT_LINE} {cut_note}. A clean answer over a cut diff does not end the loop; the rest of "
                "the change needs a round of its own."
            )
        # Include warnings emitted at dispatch, including retries/replacements
        # that crossed UTC midnight after the round's earlier terms checks.
        for warning in retain_terms_warnings([]):
            note = f"Notice: {warning}."
            if note not in notes:
                notes.append(note)
        for notice in retain_address_notices([]):
            notes.append(f"Address notice: {notice}")
        parts = [f"## Round {round_number} — {', '.join(members)}, {today()}", *notes, *statements]
        for member, block in reviewer_blocks:
            # The runner's line names whose words follow (DL-B-3); the note stays the switch `_record_lines` reads.
            parts.append(f"From {member}:\n\n{NOT_ROWS_NOTE}\n\n{quote_reviewer(block)}")
        parts.extend(malformed_blocks)
        path = record_dir(change, root) / "loop.md"
        # A continued run after a release starts a fresh record: `write_round` writes its heading and the
        # run's snapshot line with the round, in one write.
        # A replacement is consumed too: it is no later rung. Both land in the same write as the round.
        state["consumed"] = [*state["consumed"], *(f"rung:{model}" for model in replaced), stage["key"]]
        write_round(change, "\n\n".join(parts), state, root)
    except BaseException:
        for notice in retain_address_notices([]):
            note = f"Address notice: {notice}"
            if note not in notes:
                notes.append(note)
        if audited:
            # The calls above wrote no round: say so in findings.md, so their audit lines read as an
            # attempt that consumed nothing and not as a lost record (DL-A-6 of the deep review).
            # This bookkeeping also follows Refused: an explicit exception to runner review R-4's
            # no-write-after-refusal rule. It accounts only for this attempt's already-written audit
            # calls; without it, a refused replacement would make the permitted retry look lost.
            with contextlib.suppress(OSError):
                append(
                    ctx.findings,
                    f"{NO_ROUND_KEY}{today()} — no round was written; the review-loop calls above consumed no stage; "
                    f"audit calls: {audited}"
                    + ("\n\n" + "\n\n".join([*notes, *malformed_blocks]) if notes or malformed_blocks else ""),
                )
        raise
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
    whether the ids are accepted at the address the one record admits
    (`model-endpoints.yaml`'s `opencode-go` `adresse`, through `stage2_go`): a
    different path on the recorded host runs on with a notice, a foreign
    destination is refused before its call. The pinned Pi is checked once
    before the first call; the free members come from a forced live refresh
    and its listing, and each free call runs through the free path - no tools,
    the implementation diff as its only content - while every paid call keeps
    the read tools. No record is written; each id and the answer's first line
    are printed for the pull request body, and skipped paid models are named.
    A failed member is reported without stopping later checks; the final
    summary lists answered and failed members and any failure makes the probe
    exit nonzero (spec, criterion 14). No second address, no substituted model.
    """
    folder_of(root, change)
    key = reviewer_key()
    problem = entry_problem(root, OPENCODE)
    if problem:
        raise Refused(problem)
    require_pi()
    free = discover_free(root, allow_empty=True)
    discovery = free
    diff, _cut = free_diff(root)
    if not free["selected"]:
        # The probe measures the ids the declaration admits; a free rule that selects nothing is a
        # finding about the catalog, not a reason to skip the paid ids (R-27 of the review-swarm review).
        print("probe: free stage skipped: the live catalog holds no model for the free rule")
    answered: list[str] = []
    failed: list[str] = []

    def check_member(ctx: Context, model: str, prompt: str, *, free: bool = False) -> None:
        # Declaration and leak checks stay outside this handler. A member's
        # refused destination, like a failed call, must not skip valid peers.
        ctx.models_store = discovery.get("models_store")
        try:
            answer = run_reviewer(ctx, model, prompt, key, free=free)
        except (CallFailed, Refused) as error:
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
    parser.add_argument("verb", choices=sorted([*VERBS, "session", "prepare-explore"]))
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
        "--class",
        dest="klass",
        default=None,
        choices=CLASSES,
        help="explore only: the change class before a spec exists, agreeing with every stated one",
    )
    parser.add_argument(
        "--availability-reported",
        dest="availability_reported",
        default=None,
        metavar="ID",
        help=(
            "the id printed by prepare-loop (review-loop) or prepare-explore (explore, swarm classes) "
            "after its selection was reported to the maintainer"
        ),
    )
    parser.add_argument(
        "--seats",
        action="append",
        default=None,
        metavar="TRIO=MODELS",
        help="prepare-explore only: the maintainer's Go models for a trio, e.g. repository=a,b",
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
    args = parser.parse_args(argv)
    _LAUNCH_STOPPED.clear()
    # SIGTERM, SIGHUP and SIGQUIT stop the run like Ctrl-C: the running programs' groups are
    # killed before the exit (DL-B-5, F6-8). The handlers are the runner's only while main runs,
    # and only from the main thread.
    previous = {}
    if threading.current_thread() is threading.main_thread():
        for signum in TERMINATING_SIGNALS:
            previous[signum] = signal.signal(signum, _terminate)
    try:
        return _run(args)
    except (KeyboardInterrupt, Terminated) as error:
        killed = kill_live()
        what = "terminated" if isinstance(error, Terminated) else "interrupted"
        print(f"{what}: the run stopped; {killed} running program group(s) killed.", file=sys.stderr)
        if isinstance(error, KeyboardInterrupt):
            raise  # Ctrl-C keeps its own exit; only the programs it could not reach are killed first.
        return 128 + error.signum
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def _terminate(signum: int, _frame: object) -> None:
    raise Terminated(signum)


def _run(args: argparse.Namespace) -> int:
    """The verb `main` parsed, with the runner's refusals mapped to their exit codes."""
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
        if args.klass is not None and args.verb not in {"explore", "prepare-explore"}:
            raise Refused("--class belongs to the explore and prepare-explore verbs alone.")
        if args.seats is not None and args.verb != "prepare-explore":
            raise Refused("--seats belongs to prepare-explore alone.")
        if args.availability_reported is not None and args.verb not in {"explore", "review-loop"}:
            raise Refused("--availability-reported belongs to the explore and review-loop verbs alone.")
        refuse_repository_git(Path(args.root))
        if (args.stage_failed is not None or args.reason is not None or args.restart) and args.verb != "release-loop":
            raise Refused("--stage-failed, --restart and --reason belong to release-loop alone.")
        if args.verb == "session":
            if not args.model:
                raise Refused("session needs --model <id>: name the model exactly as model-endpoints.yaml lists it.")
        elif args.model is not None or args.handover is not None:
            raise Refused("--model and --handover belong to the session verb alone.")
        if args.verb in {"review-loop", "release-loop", "prepare-loop", "review", "repair"}:
            # The name is checked before the lock: the lock's path is built from it, and a name that
            # escapes the state directory must create nothing there (DL-A-9 of the deep review).
            folder_of(Path(args.root), args.change)
        if args.verb == "repair":
            # Repair reads the record's taken rows and marks them after its commit: it owns the record from
            # the first read to the marking, so no release removes it in between (DL-A-5 of the deep review).
            with holding_record(args.change, Path(args.root)):
                repair(Path(args.root), args.change, args.stage2_off)
        elif args.verb == "prepare-explore":
            prepare_explore(Path(args.root), args.change, args.klass, args.seats)
        elif args.verb == "explore":
            explore(Path(args.root), args.change, args.stage2_off, args.klass, args.availability_reported)
        elif args.verb == "implement":
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
    except RestorationRefused as error:
        prefix = "failed" if error.exit_code == 1 else "refused"
        print(f"{prefix}: {error}", file=sys.stderr)
        return error.exit_code
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
