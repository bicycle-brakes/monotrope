#!/usr/bin/env python3
"""stage2.py - the one way this repository starts a foreign model.

**What this is.** Stage 2 lets a reviewer from another vendor read framework
content: GLM 5.3 Flash explores (phase 1) and implements (phase 4), Codex
reviews the spec and code (phases 2a and 6), and GLM 5.3 runs the review loop
(phase 4b). A declaration in `model-endpoints.yaml` stops nothing; this runner
stands between the rule and the call.

    python3 scripts/stage2.py explore      <change>   # GLM Flash, phase 1
    python3 scripts/stage2.py spec-review  <change>   # Codex, phase 2a, a fresh session
    python3 scripts/stage2.py implement    <change>   # GLM Flash, phase 4
    python3 scripts/stage2.py review-loop  <change>   # GLM, one round of phase 4b
    python3 scripts/stage2.py release-loop <change>   # loop rows into findings.md
    python3 scripts/stage2.py review       <change>   # Codex, phase 6, the 2a session resumed

`explore` and `implement` accept `--stage2-off [REASON]`: the declared
Stage-1 route uses Haiku 4.5 or Sonnet 5.5. A leak refusal never falls back.
Implement lets the model edit but not run commands; the runner runs
`make verify`, checks the time log and makes the one checkpoint commit.

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

**Reads: confined for the Claude Code calls, asked for Codex.** Every Claude
Code call (explore, implement, the Flash and Sonnet fallback attempts, the GLM
review loop) starts in the worktree with `--restricted` and no `--add-dir`;
`claude --help` says `--restricted` "confines the file tools to the working
directories", so `~/.config/cc-routing/secrets.env` is outside what those file
tools reach. That is the CLI's documented behaviour, not measured here: no test
has run the real program against a path outside the worktree. The Codex calls
(`spec-review`, `review`) have no such flag: every prompt ends with the request
to read nothing outside the worktree and the repository's git directory, which
is a request, not a lock - Codex can read the rest of the disk.

**The loop record** lives outside the worktree
(`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`):
GLM's rows and the implementer's decision on each, until the phase-6 verdict is
written and `release-loop` carries them into `findings.md`. The release is the
only thing that deletes the record, and it deletes nothing that has not arrived:
every loop row, and every other line of the record as it stands, is in
`findings.md` first. Not carried are only the record's own furniture: its
heading, its intro, the round headings, the tables' header and separator, and
the blank lines outside GLM's words. GLM's words are carried exactly as they
came - a heading, a code comment or a table line with a loop id included; only
a line of the round tables the runner wrote that carries a loop id and cannot
be read as a row refuses the release, because the implementer has to decide
that row. A call counts as a round when it succeeded and answered - with rows
or with "no finding"; a failed call or an empty answer is no round.

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
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_frontmatter_current  # noqa: E402
import leakcheck  # noqa: E402
import merge_guard  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

# (endpoint, model, effort) - what the declaration must clear and the call pins.
CODEX = ("openai-codex", "gpt-6.1-sol", "max")
GLM = ("glm-coding-plan", "glm-5.3", "max")
GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")
HAIKU = ("claude-code-plan", "claude-haiku-4-5", None)
SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")
GLM_BASE_URL = "https://api.z.ai/api/anthropic"

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

MAX_ROUNDS = 2
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
ROUND_HEADING = re.compile(r"^## Round \d+ — GLM,", re.M)
RELEASE_HEADING = "## Phase 4b — GLM loop rows, released"
NO_LOOP_LINE = "Loop rows: none — the GLM loop did not run for this change."
LOOP_ID = re.compile(r"L\d+-\d+")
NOT_ROWS_NOTE = "The answer was not only six-cell rows; what is not one is kept below as it came."

RECORD_HEADING = "# Loop record — "
RECORD_INTRO = (
    "Write `Status` (`taken — <test or criterion>` or `rejected — <reason>`) for every row below.\n"
    "For a taken row also write `Broke a test` (`yes` or `no`) — before the next round or the release."
)

_PIPE = re.compile(r"(?<!\\)\|")


class Refused(Exception):
    """The runner refuses before any call: exit 2."""


class CallFailed(Exception):
    """A call ended without a usable answer: exit 1."""


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


def glm_env(key: str, config_dir: Path, model: str = GLM[1]) -> dict[str, str]:
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
    command: list[str], root: Path, env: dict[str, str], secret: str | None = None
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
        )
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
    """The block of a Codex answer: its rows with the reviewer, `open` and no test mark."""
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
    if "framework" not in (found.get("darf_sehen") or []):
        return f"the endpoint {endpoint} may not see framework content"
    if found.get("residenz") in (None, "nicht-erklaert"):
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
        producer = "codex" if endpoint == CODEX else "claude-code"
        ctx.findings.write_text(findings_header(ctx, producer), encoding="utf-8")
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
        destination.write_text(findings_header(ctx, "claude-code"), encoding="utf-8")
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


def work_prompt(root: Path, prompt_file: str, change: str, extra: str = "") -> str:
    """A work phase, the repository rules and its inputs, without review row instructions."""
    body = (root / "prompts" / prompt_file).read_text(encoding="utf-8")
    rules = (root / "AGENTS.md").read_text(encoding="utf-8")
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
# Codex
# ---------------------------------------------------------------------------


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


def run_codex(ctx: Context, prompt: str, resume: str | None = None) -> tuple[str, str]:
    """One Codex call, first or resumed, pinned the same way. Returns (answer, thread id)."""
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
            'sandbox_mode="read-only"',
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


def spec_review(root: Path, change: str) -> None:
    """Phase 2a: a fresh Codex session reads the spec."""
    ctx = preflight(root, change, CODEX)
    prompt = phase_prompt(root, "02a-spec-review.md", change)
    begin_call(ctx, "spec-review", CODEX, prompt)
    answer, thread = run_codex(ctx, prompt)
    rows, _ = parse_rows(answer)
    append(
        ctx.findings,
        f"## Phase 2a — Codex, {today()}\n\n{answer_block(rows, answer, 'Codex')}\n\nReviewer session: codex {thread}",
    )
    print(f"spec-review: {len(rows)} rows appended to {ctx.findings.relative_to(root)}; session codex {thread}")


def review(root: Path, change: str) -> None:
    """Phase 6: the 2a session resumed, the verdict written, the loop rows released and marked."""
    ctx = preflight(root, change, CODEX)
    record = read_record(change)
    if record is not None:
        waiting = undecided(record_rows(record))
        if waiting:
            raise Refused(f"the loop record has undecided rows ({', '.join(waiting)}); decide them first.")
    text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
    sessions = SESSION_LINE.findall(text)
    recorded = sessions[-1] if sessions else None
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
        block += f"\nReviewer session: codex {thread} — a fresh session reviewed: no phase-2a session was recorded"
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
    start = text.rfind(RELEASE_HEADING)
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
# The loop record, release, and the GLM round
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
    """Each line of the record, and whether it is GLM's words - not the runner's or the implementer's.

    The runner writes a round as its heading, then a table or one statement and, when the answer was not
    only six-cell rows, the note `NOT_ROWS_NOTE` and the rest of the answer as it came. The lines after the
    note, up to the next round heading, are GLM's; every other line is the record's own. A line of GLM's
    that has the form of a round heading cannot be told from one.
    """
    lines = []
    glm = False
    for line in record.splitlines():
        if ROUND_HEADING.match(line):
            glm = False
        elif not glm and line.strip() == NOT_ROWS_NOTE:
            lines.append((line, False))
            glm = True
            continue
        lines.append((line, glm))
    return lines


def record_rows(record: str) -> list[list[str]]:
    """The loop rows of the record: every table line of its own whose first cell is a loop id.

    Only the record's own lines are read, never GLM's words, which are carried as they came: a table line
    GLM wrote is not a row the implementer has to decide, whatever its first cell says.

    Nine cells are known. A `|` the implementer typed into `Status` makes a tenth; the cells between the
    reviewer and the last one are that reason, each pipe escaped. A line with a loop id and fewer cells
    than a row has is not skipped, which would let the release delete it with the record: it is refused,
    by its id.
    """
    rows = []
    for line, glm in _record_lines(record):
        cells = None if glm else split_row(line)
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
    """Rows whose Status does not begin `taken` or `rejected`, or a taken row without `yes` or `no`."""
    waiting = []
    for row in rows:
        status, broke = row[7].lower(), row[8].lower()
        decided = status.startswith("rejected") or (status.startswith("taken") and broke in {"yes", "no"})
        if not decided:
            waiting.append(row[0])
    return waiting


def rounds_run(record: str | None, findings_text: str) -> int:
    """A round is counted by its block in the record, and by every count left behind by a release."""
    in_record = len(ROUND_HEADING.findall(record)) if record else 0
    return in_record + sum(int(n) for n in ROUNDS_LINE.findall(findings_text))


def kept_lines(record: str) -> str:
    """Everything the record holds that the release does not carry as a row, exactly as it stands.

    Left out: the record's own furniture - its heading, its intro, the round headings, the tables' header and
    separator - and the loop rows (`record_rows` has them). What is left goes to `findings.md`, because the
    record is deleted afterwards and is the only copy: the runner's own statements, and GLM's words line by
    line as they came, blank lines between them included (a heading or a comment that starts with `#`, a table
    line that is no row). GLM's words stand apart from the runner's lines by a blank line.
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
        if NO_LOOP_LINE not in text and RELEASE_HEADING not in text:
            append(findings, NO_LOOP_LINE)
        return []
    rows = record_rows(record)
    waiting = undecided(rows)
    if waiting:
        raise Refused(f"the loop record has undecided rows ({', '.join(waiting)}); nothing is released.")
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


def _git_output(root: Path, *args: str, allow: tuple[int, ...] = (0,)) -> str:
    done = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, errors="replace", check=False
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


def changed_paths(root: Path) -> set[Path]:
    """Tracked changes against HEAD and untracked files, as repository-relative paths."""
    tracked = _git_output(root, "diff", "--name-only", "-z", "HEAD").split("\0")
    untracked = _git_output(root, "ls-files", "-z", "--others", "--exclude-standard").split("\0")
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


def restore_baseline(root: Path, baseline: str, keep: set[Path]) -> str:
    """After a failed model call, put every path but `keep` back at the baseline; say what was undone.

    The runner refused pre-existing changes outside `keep` before the first call, so what differs
    from the baseline outside it is the run's own - including a half-finished edit of a dead process.
    """
    touched = sorted(path.as_posix() for path in changed_paths(root) - keep)
    if not touched:
        return "the worktree needed no restore."
    spec = [f":(exclude){path.as_posix()}" for path in sorted(keep, key=lambda path: path.as_posix())]
    try:
        _git_output(root, "restore", f"--source={baseline}", "--staged", "--worktree", "--", ".", *spec)
        _git_output(root, "clean", "-fdq", "--", ".", *spec)
    except Refused as error:
        return f"restoring the worktree to {baseline[:12]} failed ({error}); discard {', '.join(touched)} by hand."
    return f"the runner restored the worktree to {baseline[:12]} (undone: {', '.join(touched)}); rerun the verb or add --stage2-off."


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
    root: Path, key: str, ignored_before: dict[Path, tuple[int, int]] | None = None
) -> list[Path]:
    """Remove an exact GLM credential from changed regular files and name those files.

    "Changed" is tracked changes, untracked files, and - when the run's earlier snapshot of the
    gitignored files is given - every ignored file created or touched since that snapshot.
    """
    paths = changed_paths(root)
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


def verify_attempt(root: Path, plan: Path, baseline_time: str, key: str | None = None) -> list[str]:
    """Run `make verify` and return bounded diagnostics for failed postconditions: the gates that blocked."""
    env = foreign_env(
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "commit.gpgsign",
            "GIT_CONFIG_VALUE_0": "false",
        }
    )
    done = launch(["make", "verify"], root, env)
    problems = []
    if done.returncode != 0:
        output = (done.stdout or "") + (done.stderr or "")
        # verify_all.sh frames gates on standard output; a gate's standard error arrives unframed after them.
        red = red_sections(done.stdout or "")
        if red is None:
            evidence = "\n".join(output.splitlines()[-TAIL_LINES:])
        else:
            evidence = "The gates that blocked, each with its last lines:\n" + red
            errors = (done.stderr or "").splitlines()
            if errors:
                # Unframed: the last lines of the whole run's standard error, not of the blocking gate alone.
                cut = len(errors) - STDERR_LINES
                kept = ([f"[… {cut} earlier lines left out …]"] if cut > 0 else []) + errors[-STDERR_LINES:]
                evidence += "\n\nStandard error of the whole run, last lines:\n" + "\n".join(kept)
        problems.append(f"`make verify` exited {done.returncode}\n{scrub(evidence, key)}".rstrip())
    try:
        current_time = time_log(plan)
    except Refused as error:
        problems.append(str(error))
    else:
        if not current_time.strip() or current_time == baseline_time:
            problems.append("`plan.md` did not add a measured line below `## Time used`")
    return problems


def checkpoint(
    root: Path,
    change: str,
    baseline: str,
    key: str | None = None,
    ignored_before: dict[Path, tuple[int, int]] | None = None,
) -> None:
    """Commit a passing implementation and prove the one clean descendant commit."""
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
            f"feat({change}): implement accepted plan",
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


def implementation_prompt(ctx: Context, baseline: str, diagnostics: list[str]) -> str:
    """The current accepted inputs and the bounded evidence from earlier attempts."""
    spec = (ctx.folder / "spec.md").read_text(encoding="utf-8")
    plan = ctx.plan.read_text(encoding="utf-8")
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
    return work_prompt(ctx.root, "04-implement.md", ctx.change, "\n\n".join(extra))


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
    baseline_time = time_log(ctx.plan)
    ignored_before = ignored_snapshot(root)
    key = None
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
        routes = [(SONNET, None, "stage-1", stage2_off)]
    diagnostics: list[str] = []
    for attempt, (endpoint, credential, route, reason) in enumerate(routes, 1):
        prompt = implementation_prompt(ctx, baseline, diagnostics)
        begin_work_call(ctx, "implement", endpoint, prompt, attempt, route, ctx.findings, reason)
        if route == "stage-1":
            insert_before_time(
                ctx.plan,
                f"## Runner route — {today()}\n\nStage-1 route: implement · model {endpoint[1]} · reason: {reason}.",
            )
        try:
            run_work_model(ctx, prompt, endpoint, writable=True, key=credential)
        except CallFailed as error:
            raise CallFailed(f"{error}; {restore_baseline(root, baseline, allowed)}") from error
        if credential is not None:
            exposed = remove_changed_credential(root, credential, ignored_before)
            if exposed:
                raise Refused(credential_message(exposed))
        problems = verify_attempt(root, ctx.plan, baseline_time, key)
        if key is not None:
            # The gate runs repository code the model just edited: scan again after it.
            exposed = remove_changed_credential(root, key, ignored_before)
            if exposed:
                raise Refused(credential_message(exposed))
        if not problems:
            checkpoint(root, change, baseline, key, ignored_before)
            print(f"implement: verified and committed · route {route} · attempt {attempt}")
            return
        diagnostics.append(f"Attempt {attempt} ({route}):\n" + "\n".join(f"- {p}" for p in problems))
    raise CallFailed("implementation post-run checks failed after the allowed attempts")


def review_loop(root: Path, change: str) -> None:
    """One round of phase 4b: GLM, through Claude Code against Z.ai, reads the diff."""
    ctx = preflight(root, change, GLM)
    record = read_record(change)
    findings_text = ctx.findings.read_text(encoding="utf-8") if ctx.findings.exists() else ""
    done_rounds = rounds_run(record, findings_text)
    if done_rounds >= MAX_ROUNDS:
        raise Refused(f"{done_rounds} rounds have run; the loop stops at {MAX_ROUNDS}.")
    if record is not None:
        waiting = undecided(record_rows(record))
        if waiting:
            raise Refused(f"the loop record has undecided rows ({', '.join(waiting)}); decide them first.")
    key = read_secret("GLM_KEY")
    if key is None:
        raise Refused(f"GLM_KEY is not in the secrets file {secrets_path()}.")
    diff = change_diff(root)
    round_number = done_rounds + 1
    body = (root / "prompts" / "04b-review-loop.md").read_text(encoding="utf-8")
    # The request comes before the diff and again after it: a long diff would bury it.
    prompt = "\n\n".join([body.rstrip(), ANSWER_FORMAT, READ_REQUEST, f"## The diff\n\n{diff}", READ_REQUEST])
    begin_call(ctx, "review-loop", GLM, prompt)
    with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
        prompt_file = Path(tmp) / "glm-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        config_dir = Path(tmp) / "claude-config"
        config_dir.mkdir()
        command = [
            "claude",
            "-p",
            f"Review the change {change} as the appended instructions say.",
            "--append-system-prompt-file",
            str(prompt_file),
            "--model",
            GLM[1],
            "--effort",
            GLM[2],
            "--tools",
            "Read,Grep,Glob",
            "--restricted",
            "--strict-mcp-config",
            "--permission-mode",
            "dontAsk",
            "--no-session-persistence",
            "--output-format",
            "text",
        ]
        done = launch(command, root, glm_env(key, config_dir, GLM[1]), key)
        if done.returncode != 0:
            raise fail("claude", done, f"exit {done.returncode}", key)
        answer = scrub(done.stdout or "", key)
    if not answer.strip():
        # "No finding" is an answer; nothing at all is a call that failed, and a failed call is no round.
        raise fail("claude", done, "the answer is empty", key)
    rows, _ = parse_rows(answer)
    numbered = [[f"L{round_number}-{k}", *row[1:], "GLM", "", ""] for k, row in enumerate(rows, 1)]
    parts = [f"## Round {round_number} — GLM, {today()}"]
    parts += answer_parts(rows, answer, "GLM", render_table(ROW_COLUMNS, numbered))
    directory = record_dir(change)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "loop.md"
    if record is None:
        path.write_text(f"{RECORD_HEADING}{change}\n\n{RECORD_INTRO}\n", encoding="utf-8")
    append(path, "\n\n".join(parts))
    print(f"review-loop: round {round_number} written to {path}: {len(numbered)} rows")


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


VERBS = {
    "explore": explore,
    "implement": implement,
    "spec-review": spec_review,
    "review-loop": review_loop,
    "release-loop": release_loop,
    "review": review,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument("verb", choices=sorted(VERBS))
    parser.add_argument("change", nargs="?", default="", help="folder name under plans/changes/")
    parser.add_argument(
        "--stage2-off",
        nargs="?",
        const="stage 2 disabled by caller",
        default=None,
        metavar="REASON",
        help="use the Stage-1 route for explore or implement and record the optional reason",
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
        if args.stage2_off is not None and args.verb not in {"explore", "implement"}:
            raise Refused("--stage2-off applies only to explore and implement.")
        if args.verb in {"explore", "implement"}:
            VERBS[args.verb](Path(args.root), args.change, args.stage2_off)
        else:
            VERBS[args.verb](Path(args.root), args.change)
    except Refused as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    except CallFailed as error:
        print(f"failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
