#!/usr/bin/env python3
"""stage2_session.py - the checked interactive session behind `stage2.py session`.

**What this is.** The mechanics of one interactive OpenCode or Codex session in
a new macOS Terminal window: the model resolved against the declaration, the
handover read as the first prompt, the runner-supplied OpenCode policy checked
against the effective agent, and the dispatch to Terminal with an audit line in
`findings.md`. `scripts/stage2.py` is the only way a foreign model starts; this
file runs only through it and is never a second entry point.

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
or resolving outside the worktree, a missing CLI or `osascript`, a policy the
effective agent overrides, and a leak check that cannot measure or is not
clean - scanned once after the handover is read and a second time immediately
before the window opens.

**What acceptance means.** Exit 0 says Terminal took the command, nothing
more: whether the CLI started, signed in or answered shows in the new window.
A dispatch that Terminal refuses exits 1 and says so in the audit. The policy
directory under the gitignored `.stage2-sessions/` holds no prompt and no
credential; a failed attempt removes it, an accepted one keeps it for the
session to load. The tool permissions passed along are a configuration, not
confinement at the operating-system level.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import yaml

SESSION_ROOT = ".stage2-sessions"
AGENT = "harness-session"
SCRIPT_NAME = "terminal-session.applescript"
PROMPT_LIMIT = 32 * 1024
COMMAND_LIMIT = 64 * 1024
CLI_TIMEOUT = 30.0
OSASCRIPT_TIMEOUT = 30.0

# The endpoints a session can dispatch, and the one CLI each drives. Anything
# else stays undeclared for sessions, whatever its modelle list says.
TRANSPORTS = {"openai-codex": "codex", "opencode-go": "opencode"}

# The guarded OpenCode permissions and the actions the effective policy may end
# on: outside directories and subagents denied, bash asked for or denied - an
# allow anywhere is not the runner's policy.
GUARDED = {"external_directory": ("deny",), "task": ("deny",), "bash": ("ask", "deny")}

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
    "commands you approve can read what the user can read."
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
    canonical = common.resolve().parent / ".claude" / "worktrees" / change
    if os.path.realpath(root) != os.path.realpath(canonical):
        raise runner.Refused(
            f"session runs in the change's dedicated worktree {canonical}, not in {root}; start it there."
        )
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
    when that entry lists `<model>` - the endpoint is called with the bare id, OpenCode's CLI takes the
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
    name = "codex" if transport == "codex" else "opencode"
    cli = shutil.which(name)
    if cli is None:
        raise runner.Refused(f"the {name} CLI is not on PATH; a session cannot start.")
    terminal = shutil.which("osascript")
    if terminal is None:
        raise runner.Refused("osascript is not on PATH; session dispatch needs macOS Terminal.")
    return cli, terminal


# ---------------------------------------------------------------------------
# The runner-supplied OpenCode policy, checked against the effective agent
# ---------------------------------------------------------------------------


def policy_config(model: str) -> dict:
    """The policy handed to OpenCode: one primary agent pinned to the model; outside directories and
    subagents denied, bash asked for. The rule maps are ordered and the last match wins, so what the tool
    inserts after a catch-all denial can be named and denied explicitly in the same form.
    """
    permission = {
        "bash": {"**": "ask"},
        "webfetch": {"**": "deny"},
        "external_directory": {"**": "deny"},
        "task": {"**": "deny"},
    }
    agent = {
        "description": "started by scripts/stage2.py session; the runner checked this policy at launch",
        "mode": "primary",
        "model": model,
        "permission": json.loads(json.dumps(permission)),
    }
    return {
        "$schema": "https://opencode.ai/config.json",
        "model": model,
        "agent": {AGENT: agent},
        "permission": permission,
    }


def effective_policy(root: Path, cli: str, model: str, env: dict[str, str], runner) -> list[dict]:
    """The resolved rules of `opencode --pure debug agent`, captured, bounded and never printed.

    OpenCode 1.18.35 prints the agent's `Agent.Info`: `model` as `{providerID, modelID}` and `permission`
    as one ordered rule list (`{permission, pattern, action}`, defaults first, the agent's own last).
    No `--tool`, no `--params`, no diagnostics on the terminal: the output is read here and the refusal
    says only what could not be confirmed.
    """
    try:
        done = subprocess.run(
            [cli, "--pure", "debug", "agent", AGENT],
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
            f"opencode debug agent did not answer within {CLI_TIMEOUT:g}s; the policy is unknown."
        ) from error
    except OSError as error:
        raise runner.Refused(f"opencode debug agent could not be started: {error}") from error
    if done.returncode != 0:
        raise runner.Refused(f"opencode debug agent exited {done.returncode}; the effective policy is unknown.")
    try:
        entry = json.loads(done.stdout)
    except ValueError as error:
        raise runner.Refused("opencode debug agent did not answer in JSON; the effective policy is unknown.") from error
    if not isinstance(entry, dict) or entry.get("name") != AGENT:
        raise runner.Refused(f"opencode debug agent does not describe the agent {AGENT}; no session starts.")
    if entry.get("mode") != "primary":
        raise runner.Refused(f"the agent {AGENT} resolves as {entry.get('mode')!r}, not as the primary agent.")
    pinned = entry.get("model")
    resolved = f"{pinned.get('providerID')}/{pinned.get('modelID')}" if isinstance(pinned, dict) else None
    if resolved != model:
        raise runner.Refused(
            f"the effective agent runs the model {resolved!r}, not the pinned {model!r}; no session starts."
        )
    rules = entry.get("permission")
    if (
        not isinstance(rules, list)
        or not rules
        or not all(
            isinstance(rule, dict)
            and all(isinstance(rule.get(field), str) for field in ("permission", "pattern", "action"))
            for rule in rules
        )
    ):
        raise runner.Refused("the effective agent carries no ordered permission rule list; the policy is unknown.")
    return rules


def wildcard(text: str, pattern: str) -> bool:
    """OpenCode's `Wildcard.match`: `*` is any run, `?` one character, the whole text must match."""
    escaped = re.sub(r"[.+^${}()|[\]\\]", lambda found: "\\" + found.group(0), pattern.replace("\\", "/"))
    escaped = escaped.replace("*", ".*").replace("?", ".")
    if escaped.endswith(" .*"):
        escaped = escaped[:-3] + "( .*)?"
    return re.fullmatch(escaped, text.replace("\\", "/"), re.S) is not None


def catch_all(pattern: str) -> bool:
    """A pattern made of `*` only matches every request."""
    return bool(pattern) and set(pattern) == {"*"}


def policy_problems(rules: list[dict]) -> tuple[list[str], list[tuple[str, str, str]]]:
    """Where the effective rules end outside the runner's policy.

    OpenCode evaluates the last rule whose permission name and pattern both match. For each guarded
    permission the last catch-all rule must carry an action the runner allows - anything else is a
    global or agent override and refuses. After it, only one kind of rule is tolerated: a specific
    `external_directory` allowance, which is what OpenCode appends for its truncation directory unless
    that exact pattern is denied explicitly; it is denied once and rechecked. Every other later rule -
    another permission name that matches by wildcard, another action - refuses.
    """
    fatal: list[str] = []
    fixable: list[tuple[str, str, str]] = []
    for key, allowed in GUARDED.items():
        applying = [rule for rule in rules if wildcard(key, rule["permission"])]
        last = max((i for i, rule in enumerate(applying) if catch_all(rule["pattern"])), default=None)
        if last is None:
            fatal.append(f"{key} has no catch-all rule")
            continue
        if applying[last]["action"] not in allowed:
            fatal.append(f"{key} ends on the catch-all {applying[last]['action']}")
        for rule in applying[last + 1 :]:
            if rule["action"] in allowed:
                continue
            if key == "external_directory" and rule["permission"] == key and rule["action"] == "allow":
                fixable.append((key, rule["pattern"], rule["action"]))
            else:
                fatal.append(f"{key} meets {rule['permission']} {rule['pattern']} {rule['action']} after its catch-all")
    return fatal, fixable


def insert_denials(config: Path, fixable: list[tuple[str, str, str]], runner) -> None:
    """One explicit denial per automatic allowance, after it - the last match wins."""
    try:
        data = json.loads(config.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise runner.Refused(f"the OpenCode policy {config} cannot be re-read: {error}") from error
    try:
        maps = [data["permission"], data["agent"][AGENT]["permission"]]
    except (KeyError, TypeError):
        maps = []
    if len(maps) != 2 or not all(isinstance(permission, dict) for permission in maps):
        raise runner.Refused(f"the OpenCode policy {config} holds no permission map; a denial cannot be inserted.")
    for permission in maps:
        for key, pattern, _action in fixable:
            rules = permission.get(key)
            if not isinstance(rules, dict):
                raise runner.Refused(f"the policy for {key} is not a rule map; an explicit denial cannot be inserted.")
            rules[pattern] = "deny"
    try:
        config.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        raise runner.Refused(f"the OpenCode policy {config} could not be amended: {error}") from error


def verify_policy(root: Path, private: Path, cli: str, model: str, runner) -> None:
    """Write the policy, read the effective agent, insert explicit denials once, refuse what stays."""
    config = private / "opencode.policy.json"
    try:
        config.write_text(json.dumps(policy_config(model), indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        raise runner.Refused(f"the OpenCode policy {config} could not be written: {error}") from error
    env = runner.foreign_env({"OPENCODE_CONFIG": str(config)})
    fatal, fixable = policy_problems(effective_policy(root, cli, model, env, runner))
    if fixable:
        insert_denials(config, fixable, runner)
        fatal, fixable = policy_problems(effective_policy(root, cli, model, env, runner))
    if fatal or fixable:
        detail = "; ".join(fatal + [f"{key} keeps {pattern} on {action}" for key, pattern, action in fixable])
        raise runner.Refused(f"the effective OpenCode policy keeps what the runner did not write ({detail}).")


# ---------------------------------------------------------------------------
# Launch files, the shell command and the dispatch
# ---------------------------------------------------------------------------


def prepare(root: Path, transport: str, selection: str, cli: str, runner) -> Path:
    """A fresh private directory under `.stage2-sessions/`, the fixed AppleScript, and the checked policy.

    Nothing user-owned is written or replaced; a preparation failure removes only what this call created.
    """
    base = root / SESSION_ROOT
    if base.is_symlink() or (base.exists() and not base.is_dir()):
        raise runner.Refused(
            f"{SESSION_ROOT}/ is a link or not a directory; the runner writes session policies only into a real directory there."
        )
    private = base / f"{transport}-{uuid.uuid4().hex[:12]}"
    try:
        private.mkdir(parents=True)
    except OSError as error:
        raise runner.Refused(f"the session directory {private} could not be created: {error}") from error
    script = private / SCRIPT_NAME
    try:
        script.write_text(APPLESCRIPT, encoding="utf-8")
    except OSError as error:
        shutil.rmtree(private, ignore_errors=True)
        raise runner.Refused(f"the launch script {script} could not be written: {error}") from error
    if transport == "opencode":
        try:
            verify_policy(root, private, cli, selection, runner)
        except runner.Refused:
            shutil.rmtree(private, ignore_errors=True)
            raise
    return private


def cli_argv(transport: str, root: Path, cli: str, model: str, prompt: str) -> list[str]:
    """The one interactive form per transport: no headless verb, no fallback, no extra writable directory."""
    if transport == "codex":
        return [
            cli,
            "--no-daemon",
            "--model",
            model,
            "--cd",
            str(root),
            "--sandbox",
            "workspace-write",
            "--ask-for-approval",
            "on-request",
            prompt,
        ]
    return [cli, "--pure", str(root), "--model", model, "--agent", AGENT, "--prompt", prompt]


def terminal_command(root: Path, env: dict[str, str], argv: list[str]) -> str:
    """One shell line. `cd`, the `/usr/bin/env -i` assignments and every argument are quoted separately, so
    paths and prompt text stay data: quotes, substitutions and newlines in them execute nothing extra. The
    absolute `env` does not depend on the PATH it is about to replace; `argv` already starts with the CLI.
    """
    assignments = [f"{shlex.quote(key)}={shlex.quote(value)}" for key, value in sorted(env.items())]
    return " ".join(
        ["cd", shlex.quote(str(root)), "&&", "exec", "/usr/bin/env", "-i", *assignments]
        + [shlex.quote(argument) for argument in argv]
    )


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
    hits = [i for i, line in enumerate(lines) if f"attempt {attempt} ·" in line and "dispatch pending." in line]
    if len(hits) != 1:
        state = "missing" if not hits else "not unique"
        raise runner.CallFailed(f"the pending audit line for attempt {attempt} is {state}; the status stays open.")
    lines[hits[0]] = lines[hits[0]].replace("dispatch pending.", f"dispatch {status}.", 1)
    try:
        ctx.findings.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    except OSError as error:
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
    """One checked session: worktree, declaration, handover, two scans, policy, dispatch, audit."""
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
    runner.checked_prompt(ctx, endpoint, prompt)
    private = prepare(root, transport, selection, cli, runner)
    producer = "codex" if transport == "codex" else "opencode"
    try:
        result = runner.checked_prompt(ctx, endpoint, prompt)
        command = terminal_command(
            root,
            runner.foreign_env(
                {"OPENCODE_CONFIG": str(private / "opencode.policy.json")} if transport == "opencode" else {}
            ),
            cli_argv(transport, root, cli, selection, prompt),
        )
        if len(command.encode("utf-8")) > COMMAND_LIMIT:
            raise runner.Refused(
                f"the dispatch command is {len(command.encode('utf-8'))} bytes; the launch transport takes at most {COMMAND_LIMIT}."
            )
        attempt = uuid.uuid4().hex[:12]
        write_pending(ctx, runner, audit_line(runner, attempt, selection, endpoint, source, result), producer)
    except (runner.Refused, runner.CallFailed):
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
        "not a statement about the CLI, the login or the model - what follows shows in the new window."
    )
