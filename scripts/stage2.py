#!/usr/bin/env python3
"""stage2.py - the one way this repository starts a foreign model.

**What this is.** Stage 2 lets a reviewer from another vendor read framework
content: the review loop (4b) runs on OpenCode Go through Pi at
`https://opencode.ai/zen/go/v1/chat/completions`, round n on the n-th id of the
`opencode-go` entry's ordered `modelle` list (the ladder, at most three
rounds); Codex drafts the spec, the design and the plan (2, 2b and 3; GLM 5.3
after two failed Codex attempts) and reviews the change (6); Opus 5.5 reviews
the spec (2a); GLM 5.3 Flash implements (phase 4) and explores (phase 1) a
`bounded` change or a `spike`, while a `feature` or `architectural` change
explores through the research swarm (ADR 0018 draft: free public researchers
from one filtered topic sentence, a Flash pair on the repository, one fresh
Opus 5.5 reconciliation). A declaration in `model-endpoints.yaml` stops nothing; this runner
stands between the rule and the call.

    python3 scripts/stage2.py explore      <change>   # the swarm or GLM Flash by class, phase 1
    python3 scripts/stage2.py draft        <change>   # Codex, phases 2, 2b and 3; GLM 5.3 after two failed attempts
    python3 scripts/stage2.py spec-review  <change>   # Opus 5.5, phase 2a
    python3 scripts/stage2.py implement    <change>   # GLM Flash, phase 4
    python3 scripts/stage2.py repair       <change>   # Codex, the taken findings; Sonnet 5.5 after two failed checks
    python3 scripts/stage2.py review-loop  <change>   # one round of phase 4b: round n on rung n
    python3 scripts/stage2.py release-loop <change>   # loop rows into findings.md
    python3 scripts/stage2.py review       <change>   # Codex, phase 6; a re-check is a fresh read-only session
    python3 scripts/stage2.py probe        <change>   # one call per rung, no record written
    python3 scripts/stage2.py session      <change>   # interactive Codex/Pi, a Terminal window

Each loop round and the probe check `pi --version` against `PI_VERSION` first;
any other answer refuses with exit 2 before the leak check and before any call.

`explore`, `implement` and `repair` accept `--stage2-off [REASON]`: the declared
Stage-1 route uses Haiku 4.5 or Sonnet 5.5. A leak refusal never falls back.
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
to the worktree and the repository's git directory. **The review
loop's Pi calls are not among them, and they are not confined:** a round's
`read` reaches files outside the worktree (measured with Pi 1.1.0, research
§L), and the secrets file is among them; only the prompt's request bounds it -
to read nothing outside the worktree and the repository's git directory, a
request and not a lock. That
is the residual risk ADR 0007 accepted for its reviewers on 2026-09-30, which
ADR 0011 extends to the rungs. The loop's isolation flags (no extensions, MCP
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
(ADR 0018 draft).

**The loop record** lives outside the worktree
(`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`):
the rounds' rows and the orchestrator's decision on each, until the phase-6
verdict is written and `release-loop` carries them into `findings.md`. The
release is the only thing that deletes the record, and it deletes nothing that
has not arrived: every loop row, and every other line of the record as it
stands, is in `findings.md` first. Not carried are only the record's own
furniture: its heading, its intro, the round headings, the tables' header and
separator, and the blank lines outside the reviewer's words. The reviewer's
words are carried exactly as they came - a heading, a code comment or a table
line with a loop id included; only a line of the round tables the runner wrote
that carries a loop id and cannot be read as a row refuses the release,
because the orchestrator has to decide that row. A call counts as a round when
it succeeded and answered - with rows or with "no finding"; a failed call, an
empty answer or a call stopped by the reviewer time limit is no round.

Exit: 0 done, 1 a call or implementation post-check failed, 2 refused.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_adr_answers  # noqa: E402
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
HAIKU = ("claude-code-plan", "claude-haiku-4-5", None)
SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")
CODEX = ("openai-codex", "gpt-6.1-sol", "max")
# Opus 5.5, the spec review (2a) since ADR 0016: the strongest review on the repository's highest-demand effort.
OPUS = ("claude-code-plan", "claude-opus-5-5", "xhigh")
# The change classes (check_interview_minimums.py's vocabulary). Explore routes on
# one: the swarm for the two large classes, the single explorer for the two small
# ones (ADR 0018 draft). Stated before the spec exists - explore-only `--class`
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
# The one Pi the loop's isolation was measured on (research §L); any other prints a refusal.
PI_VERSION = "1.1.0"
PI_TOOLS = "read,grep,find,ls"
# A reviewer call that has not ended after this many minutes is stopped (spec, criterion 15).
REVIEWER_MINUTES = 30
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
    "The runner adds the reviewer, the status and the test mark. When there is no finding, answer in one sentence."
)
MARK_FORMAT = "For each loop row answer one line and nothing else: `<ID>: agree` or `<ID>: disagree — <reason>`."
REPAIR_ANSWER = (
    "Answer with one fixed line per row and no other text: `<ID>: fixed — tests/<path>::<function>` or\n"
    "`<ID>: fixed — not a test — <reason>`. Write a `|` inside a reason as `\\|`. A code row needs a test that\n"
    "fails on the baseline's code, which the runner runs; only a row taken as `taken — not a test — <reason>`\n"
    "may be answered `not a test`. Do not edit `findings.md`."
)
# The Codex attempts (ADR 0017): Codex has command tools in its configured sandbox, so it is told what it may run.
REPAIR_FORMAT = (
    "Repair only the taken rows below. You may run tests and `make verify`; write a measured entry under\n"
    "`## Time used` in `plan.md`. Do not commit and run no git command that changes the repository: the\n"
    "runner runs `make verify` and makes the one commit. " + REPAIR_ANSWER
)
# The Sonnet attempt keeps the file-tools sentence it always had.
REPAIR_FORMAT_FILE_TOOLS = (
    "Repair only the taken rows below, with the available file tools; you cannot run commands. " + REPAIR_ANSWER
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

MAX_ROUNDS = 3
ROW_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Reviewer", "Status", "Broke a test"]
RELEASED_COLUMNS = [*ROW_COLUMNS, "Phase 6"]

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
ROUND_HEADING = re.compile(r"^## Round \d+ — \S+,", re.M)
RELEASE_HEADING = "## Phase 4b — loop rows, released"
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
NOT_ROWS_NOTE = "The answer was not only six-cell rows; what is not one is kept below as it came."
# A fixed line's test, in the form of ADR 0013's criterion ledger: a file `tests/…/test_*.py`, a function
# `test_…`. A `.` or `..` path segment would climb out of `tests/`; `fixed_status` refuses it as the
# ledger's gate does (`check_criterion_ledger.py`).
FIXED_TEST = re.compile(r"^tests/(?P<file>[^|\s]+\.py)::(?P<function>test_\w+)$")
# A red-first pytest run that has not ended after this many minutes is stopped (spec, criterion 18).
RED_FIRST_MINUTES = 10

RECORD_HEADING = "# Loop record — "
RECORD_INTRO = (
    "Write `Status` (`taken — <test or criterion>`, `taken — not a test — <reason>` or "
    "`rejected — <reason>`) for every row below.\n"
    "For a taken row also write `Broke a test` (`yes` or `no`) — before the next round or the release; "
    "a row the repair marked `fixed` needs the mark too."
)

_PIPE = re.compile(r"(?<!\\)\|")


class Refused(Exception):
    """The runner refuses before any call: exit 2."""


class CallFailed(Exception):
    """A call ended without a usable answer: exit 1."""

    def __init__(self, message: str, *, partial_answer: str = "", receipts_text: str = "") -> None:
        super().__init__(message)
        self.partial_answer = partial_answer
        self.receipts_text = receipts_text


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
    """Start a foreign program: empty standard input, the worktree as its directory."""
    try:
        return subprocess.run(
            command,
            cwd=root,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        what = limit or f"the reviewer time limit after {REVIEWER_MINUTES:g} minutes"
        raise CallFailed(f"{command[0]} was stopped by {what}") from error
    except OSError as error:
        raise CallFailed(f"{command[0]} could not be started: {scrub(str(error), secret)}") from error


def fail(program: str, done: subprocess.CompletedProcess, reason: str, secret: str | None = None) -> CallFailed:
    """Print the last lines of the program's standard error, scrubbed; return the exception to raise."""
    tail = "\n".join((done.stderr or "").splitlines()[-40:])
    if tail:
        print(scrub(tail, secret), file=sys.stderr)
    return CallFailed(f"{program} call failed: {reason}")


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


def parse_rows(answer: str) -> tuple[list[list[str]], str]:
    """The six-cell rows of an answer and the text that is not a row.

    Six cells are known. A line of more cells that starts like a row (its second cell is a severity) holds a
    `|` inside its last cell - a shell pipe, a regular expression - and that cell takes the rest, each
    pipe escaped. Anything else that is a table line but no row stays in the text, as it came.
    """
    rows: list[list[str]] = []
    rest: list[str] = []
    for line in answer.splitlines():
        cells = split_row(line)
        if cells is None:
            if line.strip():
                rest.append(line)
        elif _furniture(cells):
            continue
        elif len(cells) == 6:
            rows.append(cells)
        elif len(cells) > 6 and cells[1].upper() in SEVERITIES:
            rows.append([*cells[:5], " \\| ".join(cells[5:])])
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

    @property
    def findings(self) -> Path:
        return self.folder / "findings.md"

    @property
    def research(self) -> Path:
        return self.folder / "research.md"

    @property
    def plan(self) -> Path:
        return self.folder / "plan.md"


def declaration_problem(root: Path, endpoint: str, model: str) -> str | None:
    """Why the declaration does not clear this endpoint and model for framework content, or None."""
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    found = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == endpoint), None)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    if model not in (found.get("modelle") or []):
        return f"the endpoint {endpoint} does not list the model {model}"
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

    The swarm's free researchers are the only role on the public class (ADR 0018
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
) -> Context:
    """The refusals that precede everything else: change, artefacts and declaration."""
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
    problem = declaration_problem(root, endpoint[0], endpoint[1])
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


def checked_prompt(ctx: Context, endpoint: tuple[str, str, str | None], prompt: str):
    """Check the declaration and exact prompt immediately before one call."""
    problem = declaration_problem(ctx.root, endpoint[0], endpoint[1])
    if problem:
        raise Refused(problem)
    result = leakcheck.check(ctx.change, leakcheck.default_denylist(), ctx.root, [("prompt", prompt)])
    print(result.verdict.render())
    if result.verdict.exit_code() != 0:
        raise Refused("the leak check is not clean; the call does not start.")
    return result


def begin_call(ctx: Context, verb: str, endpoint: tuple[str, str, str | None], prompt: str) -> None:
    """The declaration, the leak check and the call line - for this one call, immediately before it."""
    result = checked_prompt(ctx, endpoint, prompt)
    if not ctx.findings.exists():
        ctx.findings.write_text(findings_header(ctx, producer_for(endpoint)), encoding="utf-8")
    append(
        ctx.findings,
        f"Stage-2 call, {today()}: {verb} · endpoint {endpoint[0]} · model {endpoint[1]} · "
        f"leak check clean over {result.files} files, {result.commits} commits, {result.rules} rules.",
    )


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


def ladder(root: Path) -> list[str]:
    """The `modelle` of the `opencode-go` entry, in order: position is the round (spec, criterion 4).

    A rung the list does not hold is no model id in the code: reordering the
    ladder or replacing its ids is a one-line pull request that touches
    `model-endpoints.yaml` and nothing else (spec, criterion 5).
    """
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        raise Refused("model-endpoints.yaml cannot be read") from None
    entry = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == OPENCODE), None)
    if entry is None:
        raise Refused(f"model-endpoints.yaml declares no endpoint {OPENCODE}")
    models = [str(model) for model in entry.get("modelle") or []]
    if not models:
        raise Refused(f"the endpoint {OPENCODE} lists no model")
    return models


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


def run_codex(ctx: Context, prompt: str, resume: str | None = None, writable: bool = False) -> tuple[str, str]:
    """One Codex call, first or resumed, pinned the same way. Returns (answer, thread id).

    A review reads in the CLI's `read-only` sandbox; a draft writes in
    `workspace-write`, and the runner puts back what lands outside the change
    folder. No call takes a bypass flag (spec, criterion 1).
    """
    _, model, effort = CODEX
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
    """Refuse unless `pi --version` prints exactly the pinned version (spec, criterion 27).

    Runs before the prompt check, the call line and any call, in a scratch
    directory with no key: a Pi off the pin sends nothing. The session verb
    calls it after its argument and handover checks.
    """
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        env = foreign_env({"HOME": tmp, "PI_CODING_AGENT_DIR": tmp})
        try:
            done = launch(
                ["pi", "--version"],
                Path(tmp),
                env,
                timeout=PI_VERSION_SECONDS,
                limit=f"the version check's limit of {PI_VERSION_SECONDS} seconds",
            )
        except CallFailed as error:
            raise Refused(
                f"pi could not be checked ({error}); it is not the pinned {PI_VERSION}; no call starts."
            ) from None
    said = (done.stdout or "").strip()
    if done.returncode != 0:
        raise Refused(f"pi --version ended {done.returncode}; it is not the pinned {PI_VERSION}; no call starts.")
    if said != PI_VERSION:
        raise Refused(f"pi {said or 'printed nothing'} is not the pinned {PI_VERSION}; no call starts.")


def run_reviewer(ctx: Context, model: str, prompt: str, key: str) -> str:
    """One reviewer call of the loop: Pi against OpenCode Go's chat-completions address.

    The launch is the measured set (spec, criterion 8): the rung's id under
    the `opencode-go` provider, thinking `max` (Pi clamps it per model), the
    read-only tools, every discovery switched off, no session, retries off.
    Each call gets its own scratch directory: a `HOME`, an agent directory
    whose only file is `settings.json`, and the prompt file. The key reaches
    Pi as `OPENCODE_API_KEY` only. Returns the scrubbed answer. A call that
    has not ended after `REVIEWER_MINUTES` is stopped (criterion 15).
    """
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        home = scratch / "home"
        home.mkdir()
        prompt_file = scratch / "review-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        command = [
            "pi",
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
            "--tools",
            PI_TOOLS,
            "--thinking",
            "max",
            "--model",
            f"{OPENCODE}/{model}",
            "--append-system-prompt",
            str(prompt_file),
            f"Review the change {ctx.change} as the appended instructions say.",
        ]
        env = foreign_env({"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "OPENCODE_API_KEY": key})
        done = launch(command, ctx.root, env, key, timeout=REVIEWER_MINUTES * 60)
        if done.returncode != 0:
            raise fail("pi", done, f"exit {done.returncode}", key)
        answer = scrub(done.stdout or "", key)
        if not answer.strip():
            # "No finding" is an answer; nothing at all is a call that failed.
            raise fail("pi", done, "the answer is empty", key)
    return answer


def taken_in_round(rows: list[list[str]], round_number: int) -> bool:
    """Whether the round wrote at least one row whose Status begins `taken` or `fixed` (spec, criterion 7).

    A row the repair has marked `fixed` counts like the taken one it was, so repairing round 2's row
    does not cancel round 3 (ADR 0015, decision 5).
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


def released_rows(findings_text: str) -> list[list[str]]:
    """The loop rows of the last released block in findings.md, with the status they were decided by."""
    start = _last_release(findings_text)
    if start < 0:
        return []
    block = findings_text[start:]
    kept = block.find("Kept from the loop record:")
    if kept >= 0:
        block = block[:kept]  # what follows is the reviewers' words, carried as they came, not rows of the record
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
        if kind == "released" and line.startswith("Kept from the loop record:"):
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


def review(root: Path, change: str) -> None:
    """Phase 6: verdict first, then release and mark the loop rows.

    A re-check after an earlier `## Phase 6` block in `findings.md` starts a
    fresh read-only Codex session. The first phase-6 review resumes a recorded
    Codex phase-2a session, otherwise starts fresh; loop marks resume the verdict thread.
    """
    ctx = preflight(root, change, CODEX)
    record = read_record(change)
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
    answer, thread = run_codex(ctx, prompt, resume=recorded)
    rows, _ = parse_rows(answer)
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
    answer, _ = run_codex(ctx, marks_prompt, resume=thread)
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


def record_dir(change: str) -> Path:
    """Outside the worktree and outside the git directory. Read at call time."""
    state = os.environ.get("XDG_STATE_HOME")
    base = Path(state) if state else Path.home() / ".local" / "state"
    return base / "coding-harness" / "stage2" / change


def read_record(change: str) -> str | None:
    path = record_dir(change) / "loop.md"
    try:
        return path.read_text(encoding="utf-8") if path.exists() else None
    except (OSError, UnicodeDecodeError) as error:
        raise Refused(f"the loop record {path} cannot be read.") from error


def _record_lines(record: str) -> list[tuple[str, bool]]:
    """Each line of the record, and whether it is the reviewer's words - not the runner's or the orchestrator's.

    The runner writes a round as its heading, then a table or one statement and, when the answer was not
    only six-cell rows, the note `NOT_ROWS_NOTE` and the rest of the answer as it came. The lines after the
    note, up to the next round heading, are the reviewer's; every other line is the record's own. A line
    of the reviewer's that has the form of a round heading cannot be told from one.
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
        decided = status.startswith("rejected") or (status.startswith(("taken", "fixed")) and broke in {"yes", "no"})
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
        parts.append(f"the loop record has undecided rows ({', '.join(plain)}); {consequence}")
    if unmarked:
        parts.append(
            f"the loop record has fixed rows without their `Broke a test` mark ({', '.join(unmarked)}); "
            "write `yes` or `no` from the repair run's evidence first"
        )
    return "; ".join(parts) + "."


def rounds_run(record: str | None, findings_text: str) -> int:
    """A round is counted by its block in the record, and by every count left behind by a release."""
    in_record = len(ROUND_HEADING.findall(record)) if record else 0
    return in_record + sum(int(n) for n in ROUNDS_LINE.findall(findings_text))


def kept_lines(record: str) -> str:
    """Everything the record holds that the release does not carry as a row, exactly as it stands.

    Left out: the record's own furniture - its heading, its intro, the round headings, the tables' header and
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
    record = read_record(change)
    if record is None:
        # The runner's own lines stand at a line start; a block's quote of either line is not one (criterion 12).
        if not (NO_LOOP.search(text) or RELEASE_LINE.search(text)):
            append(findings, NO_LOOP_LINE)
        return []
    rows = record_rows(record)
    refusal = undecided_refusal(rows, "nothing is released")
    if refusal:
        raise Refused(refusal)
    block = [f"{RELEASE_HEADING} {today()}", render_table(RELEASED_COLUMNS, [[*row, "—"] for row in rows])]
    if not rows:
        block.append("No loop row was reported.")
    block.append(f"Rounds run: {len(ROUND_HEADING.findall(record))}")
    kept = kept_lines(record)
    if kept:
        block.append(f"Kept from the loop record:\n\n{kept}")
    append(findings, "\n\n".join(block))
    shutil.rmtree(record_dir(change))
    print(f"release-loop: {len(rows)} loop rows appended to {findings.relative_to(root)}")
    return rows


def release_loop(root: Path, change: str) -> None:
    release(root, change)


def _git_output(root: Path, *args: str, allow: tuple[int, ...] = (0,), env: dict[str, str] | None = None) -> str:
    done = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, errors="replace", check=False, env=env
    )
    if done.returncode not in allow:
        raise Refused(f"git {args[0]} failed: {done.stderr.strip()[:200]}")
    return done.stdout


def change_diff(root: Path) -> str:
    """The diff against the merge base with origin/main, uncommitted and untracked files included."""
    done = subprocess.run(
        ["git", "-C", str(root), "merge-base", "HEAD", "origin/main"], capture_output=True, text=True, check=False
    )
    base = done.stdout.strip()
    if done.returncode != 0 or not base:
        raise Refused("there is no merge base with origin/main; the diff cannot be built.")
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


def changed_paths(root: Path, env: dict[str, str] | None = None, against: str = "HEAD") -> set[Path]:
    """Tracked changes against `against` and untracked files, as repository-relative paths."""
    tracked = _git_output(root, "diff", "--name-only", "-z", against, env=env).split("\0")
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


def prepare_derived(root: Path, env: dict[str, str], key: str | None = None) -> list[str]:
    """Stamp only changed, held documents, then render the index before verification.

    Clean documents are not an implementation's repair surface. The existing stamp leaves
    duplicate or absent headers alone, so the verifier still reports those structural errors.
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
        if errors:
            evidence = "\n".join(_shrink("\n".join(errors).splitlines(), TAIL_LINES))
            return [f"Derived-file preparation failed: {scrub(evidence, key)}"]
        index = root / "plans" / "INDEX.md"
        if not index.resolve().is_relative_to(root.resolve()):
            raise OSError("refusing an index outside the worktree: plans/INDEX.md")
        if index.resolve() != root.resolve() / "plans" / "INDEX.md":
            raise OSError("refusing an aliased index path: plans/INDEX.md")
        if index.exists() and index.stat().st_nlink > 1:
            raise OSError("refusing a hard-linked index path: plans/INDEX.md")
        done = launch([sys.executable, "scripts/plans_registry.py", "--index"], root, env, key)
    except (
        check_frontmatter_current.CannotMeasure,
        check_frontmatter_current.CannotStamp,
        OSError,
        CallFailed,
        Refused,
        RuntimeError,
        UnicodeError,
    ) as error:
        evidence = "\n".join(str(error).splitlines()[-TAIL_LINES:])
        return [f"Derived-file preparation failed: {scrub(evidence, key)}"]
    if done.returncode:
        evidence = "\n".join(((done.stdout or "") + (done.stderr or "")).splitlines()[-TAIL_LINES:])
        return [f"Derived-file preparation failed: index renderer exited {done.returncode}\n{scrub(evidence, key)}"]
    return []


def verify_evidence(done: subprocess.CompletedProcess, key: str | None) -> str:
    """The bounded evidence of a red `make verify`: the framed gates that blocked, else the run's tail."""
    output = (done.stdout or "") + (done.stderr or "")
    # verify_all.sh frames gates on standard output; a gate's standard error arrives unframed after them.
    red = red_sections(done.stdout or "")
    if red is None:
        return scrub("\n".join(output.splitlines()[-TAIL_LINES:]), key)
    evidence = "The gates that blocked, each with its last lines:\n" + red
    errors = (done.stderr or "").splitlines()
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
    return scrub(f"not run — {' '.join(reason.split()).rstrip('.')}.", key)


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


def format_step(root: Path, env: dict[str, str], key: str | None = None) -> str | None:
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
        return scrub(f"not run — no ruff at `{RUFF}`; `make venv` builds it.", key)
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
            done = launch([RUFF, *command, *targets], root, env, key)
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
    return scrub(line + ".", key)


def verify_attempt(
    root: Path,
    plan: Path,
    baseline_time: str,
    key: str | None = None,
    formatted: list[str] | None = None,
) -> list[str]:
    """Stamp changed held documents, render the index, format the targets, then run `make verify`.

    Preparation writes to the tree and executes its registry renderer. Before `make verify` the
    runner applies ruff's safe fixes and its formatter to the changed Python files under `scripts/`
    and `tests/`; when `formatted` is given, the step's line lands there. Return bounded
    diagnostics for failed preparation or postconditions, naming the gates that blocked.
    `baseline_time` holds the pre-call plan: restoring a heading or moving an old entry into the
    time section cannot count as this attempt's new measured line.
    """
    env = foreign_env(
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "commit.gpgsign",
            "GIT_CONFIG_VALUE_0": "false",
        }
    )
    preparation = prepare_derived(root, env, key)
    if preparation:
        return preparation
    line = format_step(root, env, key)
    if formatted is not None and line is not None:
        formatted.append(line)
    done = launch(["make", "verify"], root, env)
    problems = []
    if done.returncode != 0:
        problems.append(f"`make verify` exited {done.returncode}\n{verify_evidence(done, key)}".rstrip())
    try:
        current_time = time_log(plan)
    except Refused as error:
        problems.append(str(error))
    else:
        added_time = Counter(current_time.splitlines()) - Counter(baseline_time.splitlines())
        if not any(line.strip() for line in added_time):
            problems.append("`plan.md` did not add a measured line below `## Time used`")
    return problems


def checkpoint(
    root: Path,
    change: str,
    baseline: str,
    key: str | None = None,
    ignored_before: dict[Path, tuple[int, int]] | None = None,
    message: str | None = None,
) -> None:
    """Commit a passing work phase and prove the one clean descendant commit."""
    if key is not None:
        exposed = remove_changed_credential(root, key, ignored_before)
        if exposed:
            raise Refused(credential_message(exposed))
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
    ancestor = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", baseline, "HEAD"],
        capture_output=True,
        check=False,
    )
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


def red_first(root: Path, baseline: str, test: str, key: str | None) -> str | None:
    """Run one named test against the baseline's code in a temporary git worktree; None when it was red.

    The worktree's `tests/` is the attempt's, without `__pycache__` and `.pytest_cache`: a test of the
    new tests against the old code is what "red first" means, and a real git checkout keeps tests that
    call git honest. The interpreter must start pytest first: a `No module named pytest` startup failure
    exits 1 too, and reading it as red would accept a run in which the named test never ran (phase 6,
    F-1). Exit 1 or 2 is red. The clean-up deletes the temporary directory before it prunes, so a
    failed `git worktree remove` leaves no dead entry behind, and a failed removal is named in the
    returned problem. Every ref's name and target is compared before and after: a difference fails the
    proof with the refs named and nothing is deleted, so another session's branch is never touched
    (phase 6, F-6 and F-7).
    """
    file, _, function = test.partition("::")
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
                    foreign_env({"PYTHONDONTWRITEBYTECODE": "1"}),
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
                    [red_first_python(root), "-m", "pytest", "-q", "-p", "no:cacheprovider", f"{file}::{function}"],
                    tree,
                    foreign_env({"PYTHONDONTWRITEBYTECODE": "1"}),
                    key,
                    timeout=RED_FIRST_MINUTES * 60,
                    limit="the red-first time limit",
                )
            except CallFailed as error:
                outcome = f"{test}: {scrub(str(error), key)}"
            else:
                if done.returncode not in (1, 2):
                    outcome = f"{test}: pytest ended {done.returncode} on the baseline's code; red first is exit 1 or 2"
    finally:
        if tree is not None:
            done = subprocess.run(
                ["git", "-C", str(root), "worktree", "remove", "--force", str(tree)], capture_output=True, check=False
            )
            if added and done.returncode != 0:
                removal = f"`git worktree remove` ended {done.returncode} on the red-first checkout"
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)
        if tree is not None:
            # Only after the directory is gone: a prune over a present directory keeps a failed removal's entry.
            subprocess.run(["git", "-C", str(root), "worktree", "prune"], capture_output=True, check=False)
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
) -> tuple[dict[str, str], list[str]]:
    """Read an answer's fixed lines: the Status each taken row takes, or the problems that fail the attempt.

    Each problem names its ID. Every row of findings.md must also stand as `before` holds it - the taken
    rows and the others alike, cell for cell: an edit outside the taken rows' Status is named, not
    checkpointed (phase 6, F-3). The pre-call findings body also protects other phases and every earlier
    attempt's evidence; only the frontmatter is excluded, because the runner refreshes `updated:`.
    Only when no problem stands do the red-first runs start, one pytest run per named test; every
    text is scrubbed with the key.
    """
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
        if not sep or not ident:
            problems.append(f"the answer holds a line that is no fixed line: {line[:80]}")
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
        return {}, [scrub(problem, key) for problem in problems]
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
            if not any(line.startswith(f"def {function}(") for line in body.splitlines()):
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
        return {}, [scrub(problem, key) for problem in problems]
    for _place, row in taken:
        fix = fixes[row[0]]
        if not fix.startswith("fixed — tests/"):
            continue
        outcome = red_first(ctx.root, baseline, fix[len("fixed — ") :], key)
        if outcome is not None:
            problems.append(f"{row[0]}: {outcome}")
    if problems:
        return {}, [scrub(problem, key) for problem in problems]
    return {ident: scrub(status, key) for ident, status in fixes.items()}, []


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
        elif kind == "released" and line.startswith("Kept from the loop record:"):
            kind = ""
        else:
            cells = split_row(line) if kind else None
            if cells and (kind, cells[0]) in by_key and cells == by_key[(kind, cells[0])]:
                cells[7] = fixes[cells[0]]
                line = "| " + " | ".join(cells) + " |"
        lines.append(line)
    ctx.findings.write_text("\n".join(lines), encoding="utf-8")
    stamp_updated(ctx.findings)


def mark_repaired_record(change: str, taken: list[tuple[str, list[str]]], fixes: dict[str, str]) -> None:
    """Mark the record's own row lines the same way, after the checkpoint commit.

    The record lies outside what the file tools reach, so only the runner can write it; a failure
    leaves the statuses unwritten there and names the IDs to mark by hand. The record's ending stays
    as it was read.
    """
    by_key = {row[0]: row for place, row in taken if place == "record"}
    record = read_record(change)
    if not by_key or record is None:
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
                line = "| " + " | ".join([*cells[:7], fixes[cells[0]], cells[-1]]) + " |"
        lines.append(line)
    try:
        (record_dir(change) / "loop.md").write_text("\n".join(lines) + ending, encoding="utf-8")
    except OSError as error:
        waiting = ", ".join(sorted(by_key))
        raise CallFailed(f"the loop record could not be marked ({error}); mark {waiting} by hand.") from error


def declared_class(root: Path, change: str, klass: str | None) -> str:
    """The one class every available statement states, or the refusal before any call.

    Sources: the explore-only `--class` argument and the `class:` of
    `research.md`'s and `spec.md`'s headers. Every statement that is present
    must name a class and agree with the others; an explicit argument does not
    cure a stated one, and none present refuses, because a silently assumed
    small change would keep a large change off the swarm (spec, criteria 3
    and 4).
    """
    folder = root / "plans" / "changes" / change
    found: dict[str, str] = {}
    for name in ("research.md", "spec.md"):
        try:
            text = (folder / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # not written yet is the normal state before the spec
        match = re.match(r"---\n(.*?)\n---", text, re.S)
        if not match:
            continue
        try:
            header = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        stated = header.get("class") if isinstance(header, dict) else None
        if stated is None:
            continue
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


def explore(root: Path, change: str, stage2_off: str | None = None, klass: str | None = None) -> None:
    """Phase 1: the swarm for a feature or architectural change, GLM Flash for a bounded
    change or a spike, or the explicit Haiku fallback - the answer lands in research.md."""
    if stage2_off is None:
        klass = declared_class(root, change, klass)
        if klass in SWARM_CLASSES:
            import stage2_swarm

            stage2_swarm.run(root, change, sys.modules[__name__], klass)
            return
        endpoint = GLM_FLASH
    else:
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
        "Update the measured span below `## Time used` in plan.md before returning; the runner runs "
        "`make verify`, stages the result and creates the checkpoint commit.",
        f"Implementation baseline: {baseline}",
        f"## Accepted spec\n\n{spec}",
        f"## Accepted plan\n\n{plan}",
    ]
    if diagnostics:
        extra.append("## Earlier post-run diagnostics\n\n" + "\n\n".join(diagnostics))
    return work_prompt(ctx.root, "04-implement.md", ctx.change, "\n\n".join(extra), inputs)


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
) -> None:
    """The attempt loop the work verbs share: call, measure, check, commit - or leave the diagnostics.

    A failed attempt leaves its diagnostics and the files its model changed, quoted, below its audit
    line in `findings.md`; the route block on `stage-1` names the verb. A verb that passes
    `snapshot_findings` and `restore_findings` puts findings.md back as it stood right before the model
    call whenever an attempt fails: the audit line above the snapshot stays, the model's own edits to
    the file - a Status it wrote itself included - go, so no failed run leaves them behind (phase 6,
    F-2).
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
        # Each attempt must add its own line. Keep all existing plan lines even if an earlier
        # attempt removed the time heading, so restoring it cannot reuse an earlier measurement.
        baseline_time = ctx.plan.read_text(encoding="utf-8")
        # Restore a changed plan with this attempt's pre-call time evidence and runner route, while the
        # accepted plan in every prompt stays the original snapshot. No older line satisfies a retry.
        inputs_before = {**inputs, ctx.plan: baseline_time.encode("utf-8")}
        kept = snapshot_findings() if snapshot_findings is not None else None
        unmeasured: str | None = None
        try:
            before = worktree_tree(root)
        except (Refused, OSError) as error:
            before, unmeasured = "", str(error)
        call_error: CallFailed | None = None
        answer = ""
        try:
            if endpoint == CODEX:
                # A fresh writing Codex call, never resumed; its thread is not kept (ADR 0017).
                answer, _ = run_codex(ctx, prompt, writable=True)
                if not answer.strip():
                    raise CallFailed("codex: the answer is empty")
            else:
                answer = run_work_model(ctx, prompt, endpoint, writable=True, key=credential)
        except CallFailed as error:
            call_error = error
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
                    quote_block(attempt_block(attempt, route, listing, moved_files, moved_head=True), key),
                )
                raise CallFailed(problem) from call_error
        if call_error is not None:
            error = call_error
            if kept is not None:
                restore_findings(kept)
            raise CallFailed(f"{error}; {restore_baseline(root, baseline, allowed, ignored_before)}") from error
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
            problems = verify_attempt(root, ctx.plan, baseline_time, key, formatted)
        except CallFailed as error:
            # `make verify` could not be started: no model can repair that, so this attempt's block
            # says why and the run stops after the scan below, with no further attempt (spec, criterion 6).
            cannot_start = error
            lines = scrub(str(error), key).splitlines() or ["make could not be started"]
            problems = ["`make verify` could not be run\n" + "\n".join(_shrink(lines, TAIL_LINES))]
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
            listing = "\n".join(f"- {p}" for p in problems)
            diagnostics.append(f"Attempt {attempt} ({route}):\n{listing}")
            append(ctx.findings, quote_block(attempt_block(attempt, route, listing, files), key))
        record += [f"- Attempt {attempt} ({route}): {line}" for line in formatted]
        if key is not None:
            # The gate runs repository code the model just edited: scan again after it.
            exposed = remove_changed_credential(root, key, ignored_before)
            if exposed:
                if kept is not None and not problems:
                    restore_findings(kept)
                raise Refused(credential_message(exposed))
        if cannot_start is not None:
            raise CallFailed(
                f"`make verify` could not be started; why, and the files this attempt changed: "
                f"{ctx.findings.relative_to(root)}"
            ) from cannot_start
        if not problems:
            if before_commit is not None:
                before_commit()
            message = commit_message
            if record:
                # The subject stays the subject; the format line of every attempt that ran the step
                # stands below the heading, in the commit that holds the formatted bytes.
                message = commit_message + "\n\n" + FORMAT_COMMIT_HEADING + "\n" + "\n".join(record)
            checkpoint(root, ctx.change, baseline, key, ignored_before, message=message)
            if after_commit is not None:
                after_commit()
            print(f"{verb}: verified and committed · route {route} · attempt {attempt}")
            return
        if attempt < len(routes):
            # Failed edits stay in the attempt's evidence. Restore every differing snapshotted input
            # before the next attempt, comparing bytes so undecodable files are restored too.
            # The plan keeps its pre-call time evidence; the retry must add its own measured line.
            # Restoration never writes through a worktree path: whatever stands there (a symlink, a
            # directory or a file) is removed without being followed, then the bytes are written anew.
            for path, content in inputs_before.items():
                if path.is_symlink() or not path.is_file() or path.read_bytes() != content:
                    if path.is_symlink() or path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
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
        held = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{base}:{posix}"], capture_output=True, check=False
        )
        if held.returncode != 0:
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


def verify_draft(root: Path, ctx: Context, key: str | None, new_adrs: list[str]) -> tuple[list[str], bool]:
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
    env = foreign_env(
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "commit.gpgsign",
            "GIT_CONFIG_VALUE_0": "false",
            # The one tolerance of a draft is the gate's own, set by this runner alone: with this
            # variable `adr-answers` reports this change's missing answer and passes, so the
            # exit code of `make verify` decides and no output is read (spec, criterion 13; F-9, F-10).
            check_adr_answers.TOLERATE_ENV: ctx.change,
        }
    )
    preparation = prepare_derived(root, env, key)
    if preparation:
        return preparation, owed
    try:
        done = launch(["make", "verify"], root, env)
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
                run_codex(ctx, prompt, writable=True)
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
            put = put_back(root, baseline, allowed)
            listing = f"- the call failed: {call_error}"
            diagnostics.append(f"Attempt {attempt} ({route}):\n{listing}")
            block = f"Attempt {attempt} ({route}) failed its call: {call_error}"
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
            listing = "\n".join(put_back_lines(put))
            append(
                ctx.findings,
                quote_block(
                    f"Attempt {attempt} ({route}): the runner put back what a draft may not change:\n{listing}",
                    key,
                    put_back_lines(put),
                ),
            )
        problems, owed = verify_draft(root, ctx, key, new_adrs)
        if problems:
            # The next attempt starts on the tree this one left; the block quotes its files and
            # diagnostics below its audit line (spec, criterion 21).
            listing = "\n".join(f"- {problem}" for problem in problems)
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
    `Broke a test` and starts no review.
    """
    first = SONNET if stage2_off is not None else CODEX
    ctx = preflight(root, change, first, required=("plan.md",))
    allowed = {ctx.findings.relative_to(root)}
    outside = changed_paths(root) - allowed
    if outside:
        listing = ", ".join(sorted(path.as_posix() for path in outside))
        raise Refused(f"the worktree has pre-existing changes outside this change's findings.md: {listing}")
    taken, waiting = repair_targets(ctx, read_record(change))
    if waiting:
        raise Refused(f"rows are waiting for a decision ({', '.join(waiting)}); decide them first.")
    if not taken:
        raise Refused("no row is taken; nothing to repair.")
    ids = [row[0] for _, row in taken]
    doubled = sorted({ident for ident in ids if ids.count(ident) > 1})
    if doubled:
        raise Refused(f"several taken rows carry the same id ({', '.join(doubled)}); mend the rows first.")
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
    rows_before = findings_rows(ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else "")
    standing: dict[str, str] = {}

    def snapshot() -> str:
        text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
        standing["text"] = text
        return text

    def check(answer: str) -> list[str]:
        # The last audit line of the snapshot is this attempt's own: it was appended just before it.
        audits = [line for line in standing.get("text", "").splitlines() if line.startswith("Stage-2 call,")]
        found, problems = check_repair_answer(
            ctx, answer, taken, baseline, key, rows_before, audits[-1] if audits else None, standing["text"]
        )
        if not problems:
            fixes.clear()
            fixes.update(found)
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
        after_commit=lambda: mark_repaired_record(change, taken, fixes),
        snapshot_findings=snapshot,
        restore_findings=lambda text: ctx.findings.write_text(text, encoding="utf-8"),
    )


def review_loop(root: Path, change: str) -> None:
    """One round of phase 4b: round *n* goes to the ladder's *n*-th rung, through Pi at OpenCode Go."""
    models = ladder(root)
    endpoint = (OPENCODE, models[0], "max")
    ctx = preflight(root, change, endpoint)
    record = read_record(change)
    findings_text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
    done_rounds = rounds_run(record, findings_text)
    if done_rounds >= MAX_ROUNDS:
        raise Refused(f"{done_rounds} rounds have run; the loop stops at {MAX_ROUNDS}.")
    if record is not None:
        refusal = undecided_refusal(record_rows(record), "decide them first")
        if refusal:
            raise Refused(refusal)
    round_number = done_rounds + 1
    if round_number == MAX_ROUNDS and not taken_in_round(
        record_rows(record) if record is not None else released_rows(findings_text), done_rounds
    ):
        raise Refused(f"round {done_rounds} wrote no taken row; the loop stops at {done_rounds}.")
    if round_number > len(models):
        raise Refused(f"the ladder of {OPENCODE} has {len(models)} rungs; round {round_number} has none.")
    model = models[round_number - 1]
    key = reviewer_key()
    require_pi()
    diff = change_diff(root)
    body = (root / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8")
    # The request comes before the diff and again after it: a long diff would bury it.
    prompt = "\n\n".join(
        [
            body.rstrip(),
            f"This is round {round_number}; you are `{model}`.",
            ANSWER_FORMAT,
            READ_REQUEST,
            f"## The diff\n\n{diff}",
            READ_REQUEST,
        ]
    )
    begin_call(ctx, "review-loop", (OPENCODE, model, "max"), prompt)
    answer = run_reviewer(ctx, model, prompt, key)
    rows, _ = parse_rows(answer)
    numbered = [[f"L{round_number}-{k}", *row[1:], model, "", ""] for k, row in enumerate(rows, 1)]
    parts = [f"## Round {round_number} — {model}, {today()}"]
    parts += answer_parts(rows, answer, model, render_table(ROW_COLUMNS, numbered))
    directory = record_dir(change)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "loop.md"
    if record is None:
        path.write_text(f"{RECORD_HEADING}{change}\n\n{RECORD_INTRO}\n", encoding="utf-8")
    append(path, "\n\n".join(parts))
    print(f"review-loop: round {round_number} written to {path}: {len(numbered)} rows")


def probe(root: Path, change: str) -> None:
    """The compatibility probe: one call per rung, the declaration and the leak check in front of each.

    Declared special run of phase 4 (the Definition of Done): the three calls
    measure whether OpenCode Go's chat-completions address
    (`https://opencode.ai/zen/go/v1/chat/completions`, the one Pi's built-in
    provider calls) accepts the ladder's ids. The pinned Pi is checked once
    before the first call. No record is written; the rung's id and the answer's
    first line are printed for the pull request body. A refused rung stops the run and is reported (spec,
    criterion 17): no second address, no substituted model.
    """
    key = reviewer_key()
    require_pi()
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
        answer = run_reviewer(ctx, model, prompt, key)
        first = answer.strip().splitlines()[0]
        print(f"probe: {model} · {scrub(first, key)}")
    print(f"probe: {len(ladder(root))} rungs answered")


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
        "--class",
        dest="klass",
        default=None,
        choices=CLASSES,
        help="explore only: the change class before a spec exists, agreeing with every stated one",
    )
    parser.add_argument(
        "--handover",
        default=None,
        help="session only: a handover file inside the worktree (default: the change's handover.md)",
    )
    parser.add_argument("--root", default=str(REPO_ROOT), help=argparse.SUPPRESS)
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
        if args.klass is not None and args.verb != "explore":
            raise Refused("--class belongs to the explore verb alone.")
        if args.verb == "session":
            if not args.model:
                raise Refused("session needs --model <id>: name the model exactly as model-endpoints.yaml lists it.")
        elif args.model is not None or args.handover is not None:
            raise Refused("--model and --handover belong to the session verb alone.")
        if args.verb == "explore":
            explore(Path(args.root), args.change, args.stage2_off, args.klass)
        elif args.verb in {"implement", "repair"}:
            VERBS[args.verb](Path(args.root), args.change, args.stage2_off)
        elif args.verb == "session":
            session(Path(args.root), args.change, args.model, args.handover)
        else:
            VERBS[args.verb](Path(args.root), args.change)
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
