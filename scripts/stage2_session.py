#!/usr/bin/env python3
"""stage2_session.py - the checked interactive session behind `stage2.py session`.

**What this is.** The mechanics of one interactive Pi or Codex session in a new
macOS Terminal window: the model resolved against the declaration, the handover
read as the first prompt, the runner-supplied Pi policy extension copied in and
confirmed loaded, and the dispatch to Terminal with an audit line in
`findings.md`. An `opencode-go/<model>` id names the endpoint, not the program:
it starts Pi (maintainer's answer Q-5); the OpenCode CLI is never called.
`scripts/stage2.py` is the only way a foreign model starts; this file runs only
through it and is never a second entry point.

**Why the runner module travels as a parameter.** Under `python3
scripts/stage2.py` the file runs as `__main__`, and an `import stage2` here
would load it a second time - with second `Refused` and `CallFailed` classes
that `main()` does not catch. So the helper receives the invoking module and
uses its exception types, its `preflight`, `checked_prompt` and `foreign_env`,
and its findings helpers.

**What a session refuses** (exit 2, before anything starts): a platform other
than macOS, an invocation outside the change's dedicated worktree
(`<main checkout>/.claude/worktrees/<change>`, attached branch, that directory
as the working one), a model the declaration does not clear for a session
transport, a handover that is missing, empty, unreadable, oversized, NUL-bound
or resolving outside the worktree, a missing CLI or `osascript`, a Pi that is not
the pinned version, a policy extension that did not load, and a leak check that cannot measure or is not
clean - scanned once after the handover is read and a second time immediately
before the window opens.

**What acceptance means.** Exit 0 says Terminal took the command, nothing
more: whether the CLI started, signed in or answered shows in the new window.
A dispatch that Terminal refuses exits 1 and says so in the audit. The command
the window runs is the trusted supervisor (`scripts/stage2_attempt.py
session-supervisor`) with the opaque invocation id alone - never the prompt,
never a login: since the isolation boundary (ADR 0018) the window populates a
private candidate from the worktree's accepted state, runs the interactive CLI
inside it, and after a normal exit returns the verified edits to the worktree
uncommitted; a cancellation or a failed check discards the candidate. The
private directory under the gitignored `.stage2-sessions/` holds that launch
state, the prompt included, for the supervisor to read, and never a credential;
a failed dispatch removes it, an accepted one keeps it. The policy extension
bounds Pi's file tools and asks before a few shell commands; it is a
configuration, not confinement at the operating-system level, and a Pi session
signs in with the maintainer's own Pi agent directory, which the runner
neither reads nor writes.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

import stage2_attempt
import yaml

SESSION_ROOT = ".stage2-sessions"
SCRIPT_NAME = "terminal-session.applescript"
# The window runs the trusted supervisor with the opaque id alone; the prompt,
# the policy path and the worktree travel through the recorded launch state.
# The supervisor inherits the window's own environment: the writer's container
# environment is built through the allow-list later (stage2_attempt), so the
# dispatch needs no assignments of its own - only the interpreter, which is
# named absolutely, and the sign-in home `interactive_login` copies from.
SUPERVISOR_SCRIPT = "scripts/stage2_attempt.py"
SUPERVISOR_VERB = "session-supervisor"
PROMPT_LIMIT = 32 * 1024
COMMAND_LIMIT = 64 * 1024
CLI_TIMEOUT = 30.0
OSASCRIPT_TIMEOUT = 30.0

# The endpoints a session can dispatch, and the one CLI each drives. Anything
# else stays undeclared for sessions, whatever its modelle list says. The id
# `opencode-go/<model>` names the endpoint; the program that serves it is Pi.
TRANSPORTS = {"openai-codex": "codex", "opencode-go": "pi"}

# The fixed AppleScript source. The shell command arrives as argv data and is
# never spliced into this text, so prompt content cannot become AppleScript.
APPLESCRIPT = 'on run argv\ntell application "Terminal"\nactivate\ndo script (item 1 of argv)\nend tell\nend run\n'

LAUNCH_LIMITS = (
    "## The limits of this launch\n\n"
    "This session was started through `python3 scripts/stage2.py session`; the leak check covered this launch\n"
    "and this first prompt, a second time immediately before the terminal window opened. It scans nothing\n"
    "after that: not later edits, not later prompts, and not a model or agent switched in the user interface -\n"
    "stay with the model this session started with, and start any other model again through the runner. The\n"
    "terminal's tool permissions are a configuration, not a confinement at the operating-system level: shell\n"
    "commands that run, whether you approved them or the policy let them pass without a question, can read\n"
    "what the user can read."
)


def on_macos() -> bool:
    """Whether this machine dispatches to Terminal."""
    return sys.platform == "darwin"


# ---------------------------------------------------------------------------
# Where a session may run, and which model it may take
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def canonical_worktree(root: Path, change: str, runner) -> None:
    """Refuse every root but `<main checkout>/.claude/worktrees/<change>`, attached and current."""
    done = _git(root, "rev-parse", "--git-common-dir")
    if done.returncode != 0:
        raise runner.Refused(f"session runs in a worktree of the repository; git says: {done.stderr.strip()[:200]}")
    common = Path(done.stdout.strip())
    if not common.is_absolute():
        common = root / common
    main_checkout = common.resolve().parent
    canonical = main_checkout / ".claude" / "worktrees" / change
    if os.path.realpath(root) != os.path.realpath(canonical):
        raise runner.Refused(
            f"session runs in the change's dedicated worktree {canonical}, not in {root}; start it there."
        )
    # A symlink at the canonical path could alias the main checkout or any other tree: refuse the alias, and
    # refuse a root git itself names as the main working tree, whatever path led there (phase 6, F-5).
    if canonical.is_symlink() or os.path.realpath(root) == os.path.realpath(main_checkout):
        raise runner.Refused(
            f"{canonical} is a link, not a worktree of its own; the dedicated worktree is a real directory."
        )
    own = _git(root, "rev-parse", "--absolute-git-dir")
    if own.returncode != 0 or os.path.realpath(own.stdout.strip()) == os.path.realpath(common):
        raise runner.Refused("session runs in a linked worktree, never in the main checkout.")
    attached = _git(root, "symbolic-ref", "--quiet", "HEAD")
    if attached.returncode != 0:
        raise runner.Refused("session needs an attached branch; this worktree is in a detached HEAD.")
    here = Path.cwd()
    if os.path.realpath(here) != os.path.realpath(root):
        raise runner.Refused(f"session runs with the worktree root as its working directory, not {here}.")


def read_declaration(root: Path, runner) -> list[dict]:
    """The endpoint entries, or a refusal: unreadable, shapeless, unnamed or duplicate declarations refuse."""
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        raise runner.Refused("model-endpoints.yaml cannot be read.") from None
    entries = data.get("endpunkte") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise runner.Refused("model-endpoints.yaml holds no list of endpoints.")
    named = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not entry["name"]:
            raise runner.Refused("model-endpoints.yaml has an endpoint entry without a name.")
        models = entry.get("modelle")
        if models is not None and (not isinstance(models, list) or not all(isinstance(m, str) for m in models)):
            raise runner.Refused(f"the endpoint {entry['name']} declares modelle that is not a list of model ids.")
        named.append(entry)
    names = [entry["name"] for entry in named]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise runner.Refused(
            f"model-endpoints.yaml declares {', '.join(duplicates)} twice; the declaration is ambiguous."
        )
    return named


def resolve_endpoint(root: Path, model: str, runner) -> tuple[tuple[str, str, None], str, str]:
    """The endpoint, the transport and the CLI's model selection for this exact id, or a refusal.

    A plain id selects only what `openai-codex` lists. A full `opencode-go/<model>` id selects `opencode-go`
    when that entry lists `<model>` - the endpoint is called with the bare id, Pi's `--model` takes the
    provider/model pair. No alias, no suffix guessing, no approval of an endpoint the file does not name.
    """
    if not model or model.split() != [model]:
        raise runner.Refused("name the model exactly as model-endpoints.yaml lists it, one id without whitespace.")
    entries = read_declaration(root, runner)
    prefix = "opencode-go/"
    if model.startswith(prefix):
        name, bare = "opencode-go", model[len(prefix) :]
        if not bare or "/" in bare:
            raise runner.Refused(f"`{model}` is not one opencode-go/<model> id; the session guesses no model.")
        if not any(entry["name"] == name and bare in (entry.get("modelle") or []) for entry in entries):
            raise runner.Refused(f"no declared endpoint opencode-go lists {bare}; the session invents no approval.")
    else:
        name, bare = "openai-codex", model
        listed = [entry["name"] for entry in entries if model in (entry.get("modelle") or [])]
        if name not in listed:
            if "opencode-go" in listed:
                raise runner.Refused(
                    f"opencode-go takes the full id opencode-go/{model}; `{model}` alone selects nothing."
                )
            if listed:
                raise runner.Refused(
                    f"the endpoint {', '.join(sorted(listed))} lists {model} but has no session transport; "
                    f"session dispatches {' and '.join(sorted(TRANSPORTS))} only."
                )
            raise runner.Refused(f"no declared endpoint lists the model {model}; the session invents no approval.")
    problem = runner.declaration_problem(root, name, bare)
    if problem:
        raise runner.Refused(problem)
    return (name, bare, None), TRANSPORTS[name], model


# ---------------------------------------------------------------------------
# The handover as the first prompt
# ---------------------------------------------------------------------------


def handover_prompt(ctx, handover: str | None, runner) -> tuple[str, str]:
    """The prompt and the handover's source: its actual text first, then the rules and the launch limits."""
    root = Path(os.path.realpath(ctx.root))
    if handover is not None and not handover.strip():
        raise runner.Refused("--handover names no file; an empty value is refused, not read as the default handover.")
    if handover is not None:
        given = Path(handover).expanduser()
        path = given if given.is_absolute() else ctx.root / given
        resolved = Path(os.path.realpath(path))
        if resolved != root and root not in resolved.parents:
            raise runner.Refused(
                f"the handover {handover} resolves to {resolved}, outside the worktree; a session sends worktree text only."
            )
        source = resolved.relative_to(root).as_posix()
    else:
        source = f"plans/changes/{ctx.change}/handover.md"
        resolved = Path(os.path.realpath(ctx.folder / "handover.md"))
        if resolved != root and root not in resolved.parents:
            raise runner.Refused(
                f"the change handover resolves to {resolved}, outside the worktree; no session starts."
            )
    if not resolved.exists():
        raise runner.Refused(f"the handover {source} does not exist.")
    if not resolved.is_file():
        raise runner.Refused(f"the handover {source} is not a regular file.")
    try:
        text = resolved.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise runner.Refused(f"the handover {source} cannot be read as UTF-8: {error}") from error
    if not text.strip():
        raise runner.Refused(f"the handover {source} is empty; a session starts with something to hand over.")
    try:
        rules = (ctx.root / "AGENTS.md").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise runner.Refused(f"AGENTS.md cannot be read: {error}") from error
    prompt = "\n\n".join(
        [text.rstrip(), "## Repository agent rules\n\n" + rules.rstrip(), LAUNCH_LIMITS, runner.READ_REQUEST]
    )
    return prompt, source


def executables(transport: str, runner) -> tuple[str, str]:
    """The resolved CLI and osascript. A missing executable refuses before any dispatch (exit 2)."""
    name = "codex" if transport == "codex" else "pi"
    cli = shutil.which(name)
    if cli is None:
        raise runner.Refused(f"the {name} CLI is not on PATH; a session cannot start.")
    terminal = shutil.which("osascript")
    if terminal is None:
        raise runner.Refused("osascript is not on PATH; session dispatch needs macOS Terminal.")
    return cli, terminal


# ---------------------------------------------------------------------------
# The runner-supplied Pi policy, copied in and confirmed loaded
# ---------------------------------------------------------------------------

# The one extension a Pi session loads: plain ESM with no imports beyond node's own, so a copy runs anywhere.
# Its handlers are tested without Pi in tests/test_stage2_session_policy.py.
POLICY_SOURCE = Path(__file__).resolve().parent / "stage2_session_policy.mjs"
POLICY_FILE = "stage2-session-policy.mjs"
# The flag that extension registers; `pi --help` lists it when the file is loaded.
POLICY_FLAG = "--stage2-session-policy"


def install_policy(private: Path, runner) -> Path:
    """Copy the extension into the session's private directory; the copy, not the source, is what Pi loads.

    The extension refuses writes to its own file, and a copy under `.stage2-sessions/` is one the session's
    file tools may not touch either, whereas `scripts/` holds a tracked file of the worktree.
    """
    copy = private / POLICY_FILE
    try:
        shutil.copyfile(POLICY_SOURCE, copy)
    except OSError as error:
        raise runner.Refused(f"the policy extension {POLICY_SOURCE.name} could not be copied: {error}") from error
    return copy


def confirm_loaded(root: Path, cli: str, extension: Path, runner) -> None:
    """Refuse unless Pi, started with only this extension, lists the extension's flag.

    This confirms that the extension *loaded*, not how it behaves; its handlers are tested without Pi
    (maintainer's answer Q-1). No model is called and no output is printed. A scratch `HOME` and agent
    directory keep this call from reading anything of the maintainer's; only the flag line is looked for.
    """
    with tempfile.TemporaryDirectory(prefix="stage2-session-") as scratch:
        env = runner.foreign_env({"HOME": scratch, "PI_CODING_AGENT_DIR": scratch})
        try:
            done = subprocess.run(
                [cli, "--no-extensions", "-e", str(extension), "--offline", "--no-approve", "--help"],
                cwd=root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=CLI_TIMEOUT,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise runner.Refused(
                f"pi --help did not answer within {CLI_TIMEOUT:g}s; the policy extension is not confirmed loaded."
            ) from error
        except OSError as error:
            raise runner.Refused(f"pi --help could not be started: {error}") from error
    if done.returncode != 0:
        raise runner.Refused(f"pi --help exited {done.returncode}; the policy extension is not confirmed loaded.")
    if not re.search(rf"(?<![\w-]){re.escape(POLICY_FLAG)}(?![\w-])", done.stdout):
        raise runner.Refused(
            "pi did not list the policy extension's flag; the extension did not load, and no session starts."
        )


# ---------------------------------------------------------------------------
# Launch files, the shell command and the dispatch
# ---------------------------------------------------------------------------


def prepare(
    root: Path,
    change: str,
    endpoint: str,
    selection: str,
    transport: str,
    cli: str,
    prompt: str,
    baseline: str,
    runner,
) -> tuple[Path, str]:
    """A fresh private directory under `.stage2-sessions/`: the recorded launch state, the fixed
    AppleScript and, for Pi, the policy extension.

    The record carries the opaque invocation id's whole lifetime: the worktree, the change, the
    endpoint and model, the accepted baseline commit, the scanned prompt, the inner command with its
    placeholders, and the policy copy's name. It holds no credential - an interactive session signs
    in with its own copied sign-in state, read by the supervisor, not dispatched. Nothing
    user-owned is written or replaced; a preparation failure removes only what this call created.
    """
    base = root / SESSION_ROOT
    if base.is_symlink() or (base.exists() and not base.is_dir()):
        raise runner.Refused(
            f"{SESSION_ROOT}/ is a link or not a directory; the runner writes session policies only into a real directory there."
        )
    attempt = uuid.uuid4().hex[:12]
    private = base / f"session-{attempt}"
    try:
        private.mkdir(parents=True)
    except OSError as error:
        raise runner.Refused(f"the session directory {private} could not be created: {error}") from error
    try:
        (private / SCRIPT_NAME).write_text(APPLESCRIPT, encoding="utf-8")
        record = {
            "root": str(root),
            "change": change,
            "endpoint": endpoint,
            "model": selection,
            "baseline": baseline,
            "prompt": prompt,
            "inner_command": cli_argv(
                transport,
                "codex" if transport == "codex" else "pi",
                selection,
                prompt,
                stage2_attempt.POLICY_PLACEHOLDER if transport == "pi" else None,
            ),
            "inner_env": {},
            "policy": POLICY_FILE if transport == "pi" else "",
        }
        (private / "invocation.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except OSError as error:
        shutil.rmtree(private, ignore_errors=True)
        raise runner.Refused(f"the launch state for attempt {attempt} could not be written: {error}") from error
    if transport == "pi":
        try:
            confirm_loaded(root, cli, install_policy(private, runner), runner)
        except BaseException:  # any failure, an unwritable temp directory or Ctrl-C included
            shutil.rmtree(private, ignore_errors=True)
            raise
    return private, attempt


def cli_argv(transport: str, cli: str, model: str, prompt: str, extension: str | None = None) -> list[str]:
    """The one interactive form per transport: no headless verb, no fallback, no extra writable directory.

    The prompt can begin with `---` (a handover's frontmatter) or with a word that is a subcommand. Codex
    and Pi get it after `--`, the end of their options. Pi reads a prompt that starts with `@` as a file name,
    which is why `run` refuses such a prompt; Pi has no print or RPC mode here, so the window stays interactive.
    `cli` is the bare program name: the supervisor's launch resolves it inside the qualified image, so no host
    path travels in the recorded command. The worktree and the extension copy ride as the supervisor's own
    placeholders (`@STAGE2_WORK@`, `@STAGE2_POLICY_FILE@`), which it fills with the candidate's paths.
    """
    if transport == "codex":
        return [
            cli,
            "--no-daemon",
            "--model",
            model,
            "--cd",
            stage2_attempt.WORK_PLACEHOLDER,
            "--sandbox",
            "workspace-write",
            "--ask-for-approval",
            "on-request",
            "--",
            prompt,
        ]
    # Discovery is off like in the reviewer call (spec criterion 11): no MCP servers (an MCP file tool would
    # bypass the policy's worktree bounds), skills, prompt templates or themes. Context files stay on, so the
    # session reads the repository's AGENTS.md (maintainer, 2026-10-09).
    return [
        cli,
        "--no-extensions",
        "--no-mcp",
        "--no-skills",
        "--no-prompt-templates",
        "--no-themes",
        "-e",
        extension or "",
        "--offline",
        "--no-approve",
        "--model",
        model,
        "--",
        prompt,
    ]


def terminal_command(root: Path, env: dict[str, str], argv: list[str]) -> str:
    """One shell line. `cd`, the `/usr/bin/env -i` assignments and every argument are quoted separately, so
    paths and prompt text stay data: quotes, substitutions and newlines in them execute nothing extra. The
    absolute `env` does not depend on the PATH it is about to replace; `argv` already starts with the CLI.
    An empty `env` passes the window's own environment through unchanged - the supervisor's dispatch needs
    exactly that, because its launch boundary is built inside `stage2_attempt`, not here.
    """
    head = ["cd", shlex.quote(str(root)), "&&", "exec"]
    if env:
        assignments = [f"{shlex.quote(key)}={shlex.quote(value)}" for key, value in sorted(env.items())]
        head += ["/usr/bin/env", "-i", *assignments]
    return " ".join(head + [shlex.quote(argument) for argument in argv])


def dispatch(terminal: str, script: Path, command: str) -> tuple[bool, str]:
    """Hand the one command line to Terminal as argv data. Returns (accepted, why-not)."""
    try:
        done = subprocess.run(
            [terminal, str(script), command],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=OSASCRIPT_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, f"osascript did not answer within {OSASCRIPT_TIMEOUT:g}s"
    except OSError as error:
        return False, f"osascript could not be started ({error})"
    if done.returncode != 0:
        lines = (done.stderr or done.stdout or "").strip().splitlines()
        tail = lines[-1][:200] if lines else "no output"
        return False, f"osascript exited {done.returncode}: {tail}"
    return True, ""


# ---------------------------------------------------------------------------
# The audit line in findings.md
# ---------------------------------------------------------------------------


def audit_line(runner, attempt: str, selection: str, endpoint: tuple[str, str, None], source: str, result) -> str:
    """One line with the date, the launch facts and the counts the scan measured - pending until dispatch."""
    return (
        f"Stage-2 session, {runner.today()}: attempt {attempt} · model {selection} · endpoint {endpoint[0]} · "
        f"handover {source} · leak check clean over {result.files} files, {result.commits} commits, "
        f"{result.rules} rules · dispatch pending."
    )


def write_pending(ctx, runner, line: str, producer: str) -> None:
    """Persist the pending audit before anything is dispatched; an unwritable audit starts no session."""
    try:
        if not ctx.findings.exists():
            ctx.findings.write_text(runner.findings_header(ctx, producer), encoding="utf-8")
        runner.append(ctx.findings, line)
    except OSError as error:
        raise runner.CallFailed(f"the pending audit could not be written: {error}; no session starts.") from error


def finalize(ctx, runner, attempt: str, status: str) -> None:
    """Turn this attempt's `dispatch pending.` into its end state; nothing else in the file moves."""
    try:
        text = ctx.findings.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise runner.CallFailed(
            f"the audit for attempt {attempt} cannot be read: {error}; the pending line stands."
        ) from error
    lines = text.splitlines()
    pending = " · dispatch pending."
    # Only the line's own ending is the status: a handover path may contain the same words (phase 6, F-7).
    hits = [i for i, line in enumerate(lines) if f"attempt {attempt} ·" in line and line.endswith(pending)]
    if len(hits) != 1:
        state = "missing" if not hits else "not unique"
        raise runner.CallFailed(f"the pending audit line for attempt {attempt} is {state}; the status stays open.")
    lines[hits[0]] = lines[hits[0]][: -len(pending)] + f" · dispatch {status}."
    # Written beside the file and moved over it: a failed write leaves the old record whole (phase 6, F-6).
    staged = ctx.findings.with_name(f".{ctx.findings.name}.{attempt}.tmp")
    try:
        staged.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
        staged.replace(ctx.findings)
    except OSError as error:
        staged.unlink(missing_ok=True)
        raise runner.CallFailed(
            f"the audit for attempt {attempt} could not be updated: {error}; the pending line stands."
        ) from error
    try:
        runner.stamp_updated(ctx.findings)
    except OSError as error:
        raise runner.CallFailed(f"the audit for attempt {attempt} was updated but not re-stamped: {error}.") from error


# ---------------------------------------------------------------------------
# The one entry, called from stage2.py only
# ---------------------------------------------------------------------------


def run(root: Path, change: str, model: str, handover: str | None, runner) -> None:
    """One checked session: worktree, declaration, handover, two scans, policy, dispatch, audit.

    The window receives the supervisor and the opaque id only; the prompt, the policy path and the
    candidate's worktree live in the recorded launch state the supervisor reads (ADR 0018).
    """
    root = Path(root)
    if not on_macos():
        raise runner.Refused("session dispatches to macOS Terminal; this platform is not supported.")
    canonical_worktree(root, change, runner)
    endpoint, transport, selection = resolve_endpoint(root, model, runner)
    ctx = runner.preflight(root, change, endpoint)
    prompt, source = handover_prompt(ctx, handover, runner)
    if "\x00" in prompt:
        raise runner.Refused("the handover text holds a NUL byte; the launch transport cannot carry it.")
    if len(prompt.encode("utf-8")) > PROMPT_LIMIT:
        raise runner.Refused(
            f"the prompt is {len(prompt.encode('utf-8'))} UTF-8 bytes; a session takes at most {PROMPT_LIMIT}."
        )
    cli, terminal = executables(transport, runner)
    if transport == "pi":
        if prompt.startswith("@"):
            raise runner.Refused(
                "the handover text starts with `@`; Pi would read the rest as a file name, so no session starts."
            )
        runner.require_pi()
    runner.checked_prompt(ctx, endpoint, prompt)
    done = _git(root, "rev-parse", "HEAD")
    if done.returncode != 0:
        raise runner.Refused(f"the worktree has no HEAD commit to baseline the session on: {done.stderr.strip()[:200]}")
    baseline = done.stdout.strip()
    private, attempt = prepare(root, change, endpoint[0], selection, transport, cli, prompt, baseline, runner)
    producer = "codex" if transport == "codex" else "pi"
    try:
        result = runner.checked_prompt(ctx, endpoint, prompt)
        command = terminal_command(
            root,
            {},
            [sys.executable, SUPERVISOR_SCRIPT, SUPERVISOR_VERB, attempt],
        )
        if len(command.encode("utf-8")) > COMMAND_LIMIT:
            raise runner.Refused(
                f"the dispatch command is {len(command.encode('utf-8'))} bytes; the launch transport takes at most {COMMAND_LIMIT}."
            )
        write_pending(ctx, runner, audit_line(runner, attempt, selection, endpoint, source, result), producer)
    except BaseException:  # any failure before the dispatch, Ctrl-C included, leaves no private directory
        shutil.rmtree(private, ignore_errors=True)
        raise
    accepted, detail = dispatch(terminal, private / SCRIPT_NAME, command)
    if not accepted:
        shutil.rmtree(private, ignore_errors=True)
        finalize(ctx, runner, attempt, f"failed ({detail})")
        raise runner.CallFailed(f"Terminal dispatch failed: {detail}")
    finalize(ctx, runner, attempt, "accepted")
    print(
        f"session: Terminal accepted the launch of {selection} in {root} (attempt {attempt}); acceptance is "
        "not a statement about the CLI, the login or the model - what follows shows in the new window. The "
        "supervisor returns the session's verified edits uncommitted; a failed check discards them."
    )
