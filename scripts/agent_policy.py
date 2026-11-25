#!/usr/bin/env python3
"""One harness-neutral permission check for agent tool calls, and the host configuration derived from it.

Every agent host that can run a pre-tool hook asks this module before a shell
command or an MCP merge tool runs (plans/changes/agent-policy-list). The rules
come from three sources, each the only place its rules are typed:

* ``scripts/merge_guard.py`` - the merge ask rules (``MERGE_ASK_RULES``);
* ``scripts/omnigent_policy.py`` - the Omnigent deny and ask rules and the
  protected path (``layer1_rules``, ``layer1_ask_rules``);
* this module - every remaining rule (``OWN_ASK_RULES``, ``OWN_DENY_RULES``):
  the Codex brake and the maintainer mode of the merge-queue enqueue script.

A decision is ``deny``, ``ask`` or ``abstain`` (no rule matches; the host
decides as it would without the hook). A shell line is split as a shell reads
it - at unquoted ``&&``, ``||``, ``;``, ``|``, a single background ``&`` and a
newline; heredoc bodies and comments are skipped - and every part is checked.
The command string that ``bash``, ``sh`` or ``zsh`` receives through ``-c``
(alone or in a short-option cluster, by name or path, also through ``env``) is
checked as a command line of its own. The strongest decision wins: deny, then
ask, then abstain. A line whose quote never closes cannot be split; it asks
(and is denied in an unattended run, like every ask). An MCP tool whose name
ends in ``merge_pull_request`` is normalised to Claude Code's
``mcp__<server>__merge_pull_request`` form, whatever separator the host uses.

This is a brake, not a security boundary: it matches text, and spellings the
rules do not name pass (docs/WORKFLOW.md names the limits).

The module also renders what hosts read:

* ``.claude/settings.json`` - ``permissions.ask`` and ``permissions.deny``
  exactly as listed here, and the Claude Code ``PreToolUse`` registration of
  ``scripts/agent_policy_hooks.py``; every other setting and hook is kept;
* ``.agents/hooks.json`` - the Antigravity ``PreToolUse`` registration.

    python3 scripts/agent_policy.py check             # does the tree match? (default; the drift gate)
    python3 scripts/agent_policy.py write             # render the files above (and the Omnigent policy)
    python3 scripts/agent_policy.py decide --shell "gh pr merge 54"
    python3 scripts/agent_policy.py decide --tool github.merge_pull_request
"""

from __future__ import annotations

import argparse
import codecs
import json
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import merge_guard as mg  # noqa: E402
import omnigent_policy as op  # noqa: E402

ROOT = SCRIPTS.parent
SETTINGS_PATH = Path(".claude") / "settings.json"
AGENTS_HOOKS_PATH = Path(".agents") / "hooks.json"

DENY = "deny"
ASK = "ask"
ABSTAIN = "abstain"
STRENGTH = {ABSTAIN: 0, ASK: 1, DENY: 2}

# ---------------------------------------------------------------------------
# The rules this module owns. Rule -> its one-line reason.
# ---------------------------------------------------------------------------

OWN_ASK_RULES: dict[str, str] = {
    "Bash(codex *)": "a Codex typed by hand runs a second agent with its own hooks; the runner starts Codex itself",
    "Bash(python3 scripts/enqueue_pr.py * --maintainer*)": (
        "the enqueue script's maintainer mode is the maintainer's; the default call without it is allowed"
    ),
    "Bash(.venv/bin/python scripts/enqueue_pr.py * --maintainer*)": (
        "the enqueue script's maintainer mode through the checkout's interpreter is the maintainer's"
    ),
}

OWN_DENY_RULES: dict[str, str] = {}

MERGE_SOURCE = "scripts/merge_guard.py"
OMNIGENT_SOURCE = "scripts/omnigent_policy.py"
OWN_SOURCE = "scripts/agent_policy.py"


@dataclass(frozen=True)
class Rule:
    """One permission rule in Claude Code's notation, with its decision, its source and why it exists."""

    pattern: str
    decision: str
    source: str
    reason: str


def _omnigent_reason(rule: str) -> str:
    if rule.startswith(op.PREFIX):
        tool = rule[len(op.PREFIX) :]
        return op.DENIED_TOOLS.get(tool) or op.ASKED_TOOLS.get(tool) or "an Omnigent tool"
    for suffix, reason in op.PROTECTED_PATHS.items():
        if rule == f"Edit(//**{suffix})":
            return reason
    return "an Omnigent rule"


class PolicyRuleError(ValueError):
    """Conflicting policy sources."""


def rules() -> list[Rule]:
    """Every rule, asks first (merge, own, Omnigent), then denies (own, Omnigent); a duplicate is refused."""
    found: list[Rule] = []
    found += [Rule(p, ASK, MERGE_SOURCE, reason) for p, (reason, _) in mg.MERGE_ASK_RULES.items()]
    found += [Rule(p, ASK, OWN_SOURCE, reason) for p, reason in OWN_ASK_RULES.items()]
    found += [Rule(p, ASK, OMNIGENT_SOURCE, _omnigent_reason(p)) for p in op.layer1_ask_rules()]
    found += [Rule(p, DENY, OWN_SOURCE, reason) for p, reason in OWN_DENY_RULES.items()]
    found += [Rule(p, DENY, OMNIGENT_SOURCE, _omnigent_reason(p)) for p in op.layer1_rules()]
    seen: dict[str, Rule] = {}
    for rule in found:
        if rule.pattern in seen:
            raise PolicyRuleError(
                f"the policy names the rule {rule.pattern} twice: by {seen[rule.pattern].source} and by {rule.source}"
            )
        seen[rule.pattern] = rule
    return found


def permissions() -> dict[str, list[str]]:
    """The `ask` and `deny` lists of `.claude/settings.json`, in rule order."""
    listed = rules()
    return {kind: [r.pattern for r in listed if r.decision == kind] for kind in (ASK, DENY)}


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Decision:
    """A check's result: the decision and the reasons behind it (empty for abstain)."""

    kind: str
    reasons: tuple[str, ...] = field(default=())

    def message(self) -> str:
        if not self.reasons:
            return "coding-harness agent policy: no rule matches"
        return "coding-harness agent policy: " + "; ".join(self.reasons)


def combine(decisions: list[Decision]) -> Decision:
    """The strongest of the decisions (deny, then ask, then abstain), with the reasons of that strength."""
    if not decisions:
        return Decision(ABSTAIN)
    kind = max((d.kind for d in decisions), key=STRENGTH.__getitem__)
    reasons: list[str] = []
    for decision in decisions:
        if decision.kind == kind:
            reasons += [reason for reason in decision.reasons if reason not in reasons]
    return Decision(kind, tuple(reasons))


def _matched(call: str, shown: str) -> Decision:
    hits = [rule for rule in rules() if mg.covers(rule.pattern, call)]
    if not hits:
        return Decision(ABSTAIN)
    kind = max((rule.decision for rule in hits), key=STRENGTH.__getitem__)
    reasons = tuple(f"{shown} matches {r.pattern} ({r.source}): {r.reason}" for r in hits if r.decision == kind)
    return Decision(kind, reasons)


# ---------------------------------------------------------------------------
# Shell lines
# ---------------------------------------------------------------------------


class ShellSyntaxError(ValueError):
    """A shell line that cannot be split, such as one whose quote never closes."""


SHELLS = ("bash", "sh", "zsh")
MAX_NESTING = 8
_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*", re.S)
_DELIMITER_STOP = " \t\n;&|<>()"


def _at_word_start(current: list[str]) -> bool:
    return not current or current[-1][-1:] in (" ", "\t")


def _read_heredoc_delimiter(text: str, start: int) -> tuple[str, int]:
    """The delimiter word after `<<` or `<<-` (quotes removed) and the index after it."""
    k = start
    word: list[str] = []
    while k < len(text) and text[k] not in _DELIMITER_STOP:
        char = text[k]
        if char in "'\"":
            end = text.find(char, k + 1)
            if end < 0:
                raise ShellSyntaxError("a heredoc delimiter opens a quote that never closes")
            word.append(text[k + 1 : end])
            k = end + 1
        elif char == "\\" and k + 1 < len(text):
            word.append(text[k + 1])
            k += 2
        else:
            word.append(char)
            k += 1
    return "".join(word), k


def _skip_heredoc_bodies(text: str, i: int, pending: list[tuple[str, bool]]) -> int:
    """The index after the bodies of the pending heredocs, which start at `i`; a body is not command text."""
    for delimiter, strip_tabs in pending:
        while i < len(text):
            end = text.find("\n", i)
            line = text[i:] if end < 0 else text[i:end]
            i = len(text) if end < 0 else end + 1
            if (line.lstrip("\t") if strip_tabs else line) == delimiter:
                break
    return i


def split_command(text: str) -> list[str]:
    """The parts of a shell line as a shell separates them; each part keeps its own quoting.

    Separators outside quotes: `&&`, `||`, `;`, `|`, `|&`, a single `&` that is not part of a
    redirection (`2>&1`, `&>`), and a newline. A comment and a heredoc body are not command text.
    """
    parts: list[str] = []
    current: list[str] = []
    pending: list[tuple[str, bool]] = []
    quote: str | None = None
    i, n = 0, len(text)
    depth = 0

    def flush() -> None:
        part = "".join(current).strip()
        if part:
            parts.append(part)
        current.clear()

    while i < n:
        char = text[i]
        if quote == "'":
            current.append(char)
            quote = None if char == "'" else quote
            i += 1
            continue
        if quote in ('"', "`"):
            if char == "\\" and i + 1 < n:
                current.append(text[i : i + 2])
                i += 2
                continue
            current.append(char)
            quote = None if char == quote else quote
            i += 1
            continue
        if char == "\\":
            if text.startswith("\\\n", i):
                i += 2
                continue
            current.append(text[i : i + 2])
            i += 2
            continue
        if char in "'\"`":
            quote = char
            current.append(char)
            i += 1
            continue
        if char == "#" and _at_word_start(current):
            end = text.find("\n", i)
            i = n if end < 0 else end
            continue
        if text.startswith("<<<", i):
            i += 3
            while i < n and text[i] in " \t":
                i += 1
            _, i = _read_heredoc_delimiter(text, i)
            current.append(" ")
            continue
        if text.startswith("<<", i):
            j = i + 2
            strip_tabs = text.startswith("-", j)
            j += 1 if strip_tabs else 0
            while j < n and text[j] in " \t":
                j += 1
            delimiter, j = _read_heredoc_delimiter(text, j)
            if delimiter:
                pending.append((delimiter, strip_tabs))
            current.append(text[i:j])
            i = j
            continue
        if char == "(":
            depth += 1
            current.append(char)
            i += 1
            continue
        if char == ")":
            depth = max(0, depth - 1)
            current.append(char)
            i += 1
            continue
        if depth:
            current.append(char)
            i += 1
            continue
        if char == "\n":
            flush()
            i += 1
            if pending:
                i = _skip_heredoc_bodies(text, i, pending)
                pending.clear()
            continue
        if char == ";":
            flush()
            i += 1
            continue
        if char == "|":
            flush()
            i += 2 if text.startswith(("||", "|&"), i) else 1
            continue
        if char == "&":
            if text.startswith("&&", i):
                flush()
                i += 2
                continue
            if (current and current[-1][-1:] in ("<", ">")) or text.startswith("&>", i):
                current.append(char)
                i += 1
                continue
            flush()
            i += 1
            continue
        current.append(char)
        i += 1
    if quote is not None:
        raise ShellSyntaxError(f"a {quote} quote never closes")
    if depth:
        raise ShellSyntaxError("nested command never closes")
    flush()
    return parts


def nested_commands(text: str) -> tuple[str, list[str]]:
    """Replace executable nesting with inert words and return its command texts."""
    nested: list[str] = []

    def scan(start: int, closing: str | None = None, depth: int = 0) -> tuple[str, int]:
        if depth > MAX_NESTING:
            raise ShellSyntaxError("substitution nesting too deep")
        out: list[str] = []
        quote: str | None = None
        i = start
        while i < len(text):
            c = text[i]
            if c == "\\" and quote != "'":
                if i + 1 >= len(text):
                    raise ShellSyntaxError("unfinished escape")
                out.append(text[i : i + 2])
                i += 2
                continue
            if quote == "'":
                out.append(c)
                if c == "'":
                    quote = None
                i += 1
                continue
            if c == "'" and quote is None:
                quote = "'"
                out.append(c)
                i += 1
                continue
            if c == '"':
                quote = None if quote == '"' else '"'
                out.append(c)
                i += 1
                continue
            if closing and c == closing and quote is None:
                return "".join(out), i + 1
            if c == "`":
                end = i + 1
                while end < len(text):
                    if text[end] == "\\":
                        end += 2
                    elif text[end] == "`":
                        break
                    else:
                        end += 1
                if end >= len(text):
                    raise ShellSyntaxError("backtick substitution never closes")
                nested.append(text[i + 1 : end])
                out.append("placeholder")
                i = end + 1
                continue
            if text.startswith("$(", i) or (c == "(" and quote is None):
                if text.startswith("$((", i):
                    level, j = 2, i + 3
                    while j < len(text) and level:
                        level += (text[j] == "(") - (text[j] == ")")
                        j += 1
                    out.append("0")
                    i = j
                    continue
                inner, i = scan(i + (2 if c == "$" else 1), ")", depth + 1)
                nested.append(inner)
                out.append("placeholder")
                continue
            out.append(c)
            i += 1
        if closing:
            raise ShellSyntaxError("nested command never closes")
        if quote:
            raise ShellSyntaxError(f"a {quote} quote never closes")
        return "".join(out), i

    outer, _ = scan(0)
    return outer, nested


def decode_ansi_quotes(part: str) -> str:
    """Decode ANSI-C words before rule matching, refusing unsupported escapes."""

    def replace(match: re.Match[str]) -> str:
        try:
            value = codecs.decode(match.group(1), "unicode_escape")
        except (ValueError, UnicodeError) as exc:
            raise ShellSyntaxError("invalid ANSI-C quote") from exc
        if "\x00" in value:
            return shlex.quote(match.group(1))
        return shlex.quote(value)

    return re.sub(r"\$'((?:\\.|[^'\\])*)'", replace, part)


def shell_c_command(part: str) -> str | None:
    """The command string a `bash`, `sh` or `zsh` invocation receives through `-c`, or None."""
    try:
        tokens = shlex.split(part)
    except ValueError:
        return None
    i = 0
    while i < len(tokens) and _ASSIGNMENT.fullmatch(tokens[i]):
        i += 1
    expansions = 0
    while i < len(tokens):
        name = Path(tokens[i]).name
        if name not in ("env", "sudo", "timeout", "nohup", "nice", "exec", "command", "time", "xargs"):
            break
        i += 1
        value_options = {
            "env": ("-u", "--unset", "-C", "--chdir", "-P", "--path", "-f", "--file"),
            "sudo": (
                "-u",
                "-g",
                "-h",
                "-p",
                "-C",
                "-T",
                "-R",
                "-D",
                "--user",
                "--group",
                "--host",
                "--prompt",
                "--chdir",
                "--chroot",
                "--close-from",
                "--command-timeout",
            ),
            "timeout": ("-k", "--kill-after", "-s", "--signal"),
            "nice": ("-n", "--adjustment"),
            "xargs": (
                "-a",
                "-d",
                "-E",
                "-I",
                "-L",
                "-n",
                "-P",
                "-s",
                "--arg-file",
                "--delimiter",
                "--eof",
                "--replace",
                "--max-lines",
                "--max-args",
                "--max-procs",
                "--max-chars",
                "--process-slot-var",
            ),
            "time": ("-f", "-o", "--format", "--output"),
        }.get(name, ())
        while i < len(tokens):
            token = tokens[i]
            if name == "env" and token in ("-S", "--split-string"):
                if i + 1 >= len(tokens):
                    raise ShellSyntaxError("env split-string lacks its argument")
                expansions += 1
                if expansions > MAX_NESTING:
                    raise ShellSyntaxError("env split-string nesting too deep")
                try:
                    tokens[i : i + 2] = shlex.split(tokens[i + 1])
                except ValueError as exc:
                    raise ShellSyntaxError("invalid env split-string") from exc
            elif token in value_options:
                if i + 1 >= len(tokens):
                    raise ShellSyntaxError(f"{name} option lacks its argument")
                i += 2
            elif token == "--":
                i += 1
                break
            elif token.startswith("-") or (name == "env" and _ASSIGNMENT.fullmatch(token)):
                i += 1
            else:
                break
        if name == "timeout" and i < len(tokens):
            i += 1
    if i >= len(tokens) or Path(tokens[i]).name not in SHELLS:
        return None
    i += 1
    has_c = False
    while i < len(tokens):
        token = tokens[i]
        if token == "--":
            i += 1
            break
        if token.startswith("--"):
            i += 2 if token in ("--rcfile", "--init-file") else 1
            continue
        if len(token) > 1 and token[0] in "-+":
            flags = token[1:]
            if token[0] == "-" and "c" in flags:
                has_c = True
            i += 2 if ("o" in flags or "O" in flags) else 1
            continue
        break
    return tokens[i] if has_c and i < len(tokens) else None


def decide_shell(command: str, _depth: int = 0) -> Decision:
    """The decision for one shell line: every part and every `-c` command string, the strongest wins."""
    if _depth > MAX_NESTING:
        return Decision(ASK, (f"shell -c nesting deeper than {MAX_NESTING} levels is not checked",))
    try:
        # Split first so comments and heredoc bodies never become executable text.
        parts = split_command(command)
        decisions: list[Decision] = []
        for part in parts:
            outer, nested = nested_commands(part)
            decoded = decode_ansi_quotes(outer)
            words = shlex.split(decoded)
            normalised = " ".join(words)
            decisions.append(_matched(f"Bash({normalised})", f"`{part}`"))
            shell_command = shell_c_command(decoded)
            if shell_command is not None:
                nested.append(shell_command)
            decisions.extend(decide_shell(item, _depth + 1) for item in nested)
    except PolicyRuleError as exc:
        return Decision(DENY, (f"policy fault: {exc}",))
    except (ShellSyntaxError, ValueError) as exc:
        return Decision(ASK, (f"the line cannot be split ({exc}), so its parts cannot be checked",))
    return combine(decisions)


# ---------------------------------------------------------------------------
# Tool names
# ---------------------------------------------------------------------------

MERGE_TOOL_SUFFIX = "merge_pull_request"
_CLAUDE_MERGE_NAME = re.compile(r"mcp__.+__" + MERGE_TOOL_SUFFIX)


def normalise_tool_name(name: str) -> str:
    """A merge tool's host name in Claude Code's `mcp__<server>__merge_pull_request` form; others unchanged."""
    if not name.endswith(MERGE_TOOL_SUFFIX) or _CLAUDE_MERGE_NAME.fullmatch(name):
        return name
    server = name[: -len(MERGE_TOOL_SUFFIX)]
    if server.startswith("mcp__"):
        server = server[len("mcp__") :]
    server = re.sub(r"[^A-Za-z0-9_-]", "_", server).strip("_-")
    return f"mcp__{server or 'server'}__{MERGE_TOOL_SUFFIX}"


def decide_tool(name: str) -> Decision:
    """The decision for a non-shell tool call, by its (normalised) name."""
    normalised = normalise_tool_name(name)
    shown = f"`{name}`" if normalised == name else f"`{name}` (as {normalised})"
    return _matched(normalised, shown)


# ---------------------------------------------------------------------------
# Generated host configuration
# ---------------------------------------------------------------------------

HOOK_EVENT = "PreToolUse"
HOOK_SCRIPT = "agent_policy_hooks.py"
HOOK_TIMEOUT = 10

REGISTRATIONS: dict[str, dict] = {
    "claude-code": {
        "matcher": "Bash|.*merge_pull_request",
        "hooks": [
            {
                "command": f'python3 "$CLAUDE_PROJECT_DIR/scripts/{HOOK_SCRIPT}" claude-code',
                "timeout": HOOK_TIMEOUT,
                "type": "command",
            }
        ],
    },
    "antigravity": {
        "matcher": "run_command|.*merge_pull_request",
        "hooks": [
            {
                "command": f"cd .. && ${{HARNESS_PYTHON:-$( [ -x .venv/bin/python ] && printf .venv/bin/python || printf python3 )}} scripts/{HOOK_SCRIPT} antigravity",
                "timeout": HOOK_TIMEOUT,
                "type": "command",
            }
        ],
    },
}


def registration(host: str) -> dict:
    """A fresh copy of the hook group a host's configuration must carry."""
    return json.loads(json.dumps(REGISTRATIONS[host]))


def _is_ours(group: object) -> bool:
    if not isinstance(group, dict):
        return False
    hooks = group.get("hooks")
    if not isinstance(hooks, list):
        return False

    def runs_policy(command: object) -> bool:
        if not isinstance(command, str):
            return False
        # The generated Antigravity interpreter is a shell expansion with spaces.
        interpreter = REGISTRATIONS["antigravity"]["hooks"][0]["command"].split(" scripts/", 1)[0]
        command = command.replace(interpreter, "python3")
        try:
            words = shlex.split(command)
        except ValueError:
            return False
        for index, word in enumerate(words):
            if not word.endswith("/scripts/" + HOOK_SCRIPT) and word != "scripts/" + HOOK_SCRIPT:
                continue
            previous = words[index - 1] if index else ""
            if re.fullmatch(r"python(?:[0-9]+(?:\.[0-9]+)*)?", previous.rsplit("/", 1)[-1]):
                return True
            if index == 0 or previous in ("&&", "||", ";", "|"):
                return True
        return False

    return any(isinstance(hook, dict) and runs_policy(hook.get("command")) for hook in hooks)


def _event_groups(config: dict, label: str) -> list:
    hooks = config.get("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"{label}: 'hooks' is not an object")
    groups = hooks.get(HOOK_EVENT, [])
    if not isinstance(groups, list):
        raise ValueError(f"{label}: 'hooks.{HOOK_EVENT}' is not a list")
    return groups


def _with_registration(config: dict, host: str, label: str) -> dict:
    out = json.loads(json.dumps(config))
    groups = [group for group in _event_groups(out, label) if not _is_ours(group)]
    out.setdefault("hooks", {})[HOOK_EVENT] = groups + [registration(host)]
    return out


def render_settings(settings: dict) -> dict:
    """`.claude/settings.json` with the listed permissions and the Claude Code registration; the rest kept."""
    out = _with_registration(settings, "claude-code", str(SETTINGS_PATH))
    perms = out.setdefault("permissions", {})
    if not isinstance(perms, dict):
        raise ValueError(f"{SETTINGS_PATH}: 'permissions' is not an object")
    listed = permissions()
    perms[ASK] = listed[ASK]
    perms[DENY] = listed[DENY]
    return out


def render_agents_hooks(config: dict) -> dict:
    """`.agents/hooks.json` with the Antigravity registration; other hooks kept."""
    return _with_registration(config, "antigravity", str(AGENTS_HOOKS_PATH))


def _load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write(root: Path = ROOT) -> None:
    """Render the Omnigent policy, `.claude/settings.json` and `.agents/hooks.json` under `root`."""
    settings_file = root / SETTINGS_PATH
    _dump(settings_file, render_settings(_load(settings_file)))
    agents_file = root / AGENTS_HOOKS_PATH
    agents = _load(agents_file) if agents_file.exists() else {}
    _dump(agents_file, render_agents_hooks(agents))
    # The Omnigent renderer writes last: it owns the order of its own rules in the settings,
    # so both drift checks (this module's and scripts/omnigent_policy.py --check) agree.
    op.write(root)


def _permission_drift(settings: dict) -> list[str]:
    problems: list[str] = []
    perms = settings.get("permissions")
    perms = perms if isinstance(perms, dict) else {}
    wanted = permissions()
    for kind, other in ((ASK, DENY), (DENY, ASK)):
        have = perms.get(kind) or []
        if not isinstance(have, list):
            problems.append(f"{SETTINGS_PATH}: permissions.{kind} is not a list")
            continue
        want = wanted[kind]
        found = [f"{SETTINGS_PATH} lacks the {kind} rule {rule}" for rule in want if rule not in have]
        for rule in dict.fromkeys(have):
            if have.count(rule) > 1:
                found.append(f"{SETTINGS_PATH} names the {kind} rule {rule} {have.count(rule)} times")
            if rule in wanted[other]:
                found.append(f"{SETTINGS_PATH} has {rule} as {kind}; the policy lists it as {other}")
            elif rule not in want:
                found.append(f"{SETTINGS_PATH} has the {kind} rule {rule}, which the policy does not list")
        if not found and have != want:
            found.append(f"{SETTINGS_PATH}: permissions.{kind} differs in order from the policy")
        problems += found
    return problems


def _registration_drift(config: dict, host: str, label: str) -> list[str]:
    try:
        groups = [group for group in _event_groups(config, label) if _is_ours(group)]
    except ValueError as exc:
        return [str(exc)]
    if len(groups) != 1:
        return [f"{label} carries {len(groups)} {HOOK_EVENT} registrations of {HOOK_SCRIPT}; the policy wants one"]
    have, want = groups[0], REGISTRATIONS[host]
    problems: list[str] = []
    if have.get("matcher") != want["matcher"]:
        problems.append(f"{label}: the {HOOK_EVENT} matcher is {have.get('matcher')!r}, not {want['matcher']!r}")
    hooks = have.get("hooks")
    if not isinstance(hooks, list) or len(hooks) != 1 or not isinstance(hooks[0], dict):
        return problems + [f"{label}: the {HOOK_EVENT} registration does not carry exactly one hook"]
    for key in ("command", "timeout", "type"):
        expected = want["hooks"][0][key]
        if hooks[0].get(key) != expected:
            problems.append(f"{label}: the {HOOK_EVENT} hook's {key} is {hooks[0].get(key)!r}, not {expected!r}")
    return problems


def check(root: Path = ROOT) -> list[str]:
    """Problems between the tree and the policy; empty when the tree is what `write` renders."""
    problems = list(op.check(root))
    try:
        settings = _load(root / SETTINGS_PATH)
    except (OSError, ValueError) as exc:
        problems.append(f"{SETTINGS_PATH} cannot be read: {exc}")
    else:
        problems += mg.problems(settings)
        drift = _permission_drift(settings)
        for kind, shared in ((ASK, op.layer1_ask_rules()), (DENY, op.layer1_rules())):
            for rule in shared:
                message = f"{SETTINGS_PATH} lacks the {kind} rule {rule}"
                if message in problems and message in drift:
                    problems.remove(message)
                    drift[drift.index(message)] = f"{message} (Omnigent and agent policy sources)"
        problems += drift
        problems += _registration_drift(settings, "claude-code", str(SETTINGS_PATH))
    try:
        agents = _load(root / AGENTS_HOOKS_PATH)
    except (OSError, ValueError) as exc:
        problems.append(f"{AGENTS_HOOKS_PATH} cannot be read: {exc}")
    else:
        problems += _registration_drift(agents, "antigravity", str(AGENTS_HOOKS_PATH))
    return list(dict.fromkeys(problems))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("check", help="does the tree match the policy? (default)")
    commands.add_parser("write", help="render the host configuration")
    decide = commands.add_parser("decide", help="decide one shell line or tool name")
    target = decide.add_mutually_exclusive_group(required=True)
    target.add_argument("--shell", metavar="LINE")
    target.add_argument("--tool", metavar="NAME")
    args = parser.parse_args(argv)

    if args.command == "decide":
        decision = decide_shell(args.shell) if args.shell is not None else decide_tool(args.tool)
        print(json.dumps({"decision": decision.kind, "reasons": list(decision.reasons)}))
        return 0
    if args.command == "write":
        write(args.root)
        print(f"rendered {SETTINGS_PATH}, {AGENTS_HOOKS_PATH} and tools/omnigent/policy.yaml")
        return 0
    problems = check(args.root)
    if problems:
        print("\n".join(problems))
        print("run: python3 scripts/agent_policy.py write")
        return 1
    print("the tree is what the agent policy renders")
    return 0


if __name__ == "__main__":
    sys.exit(main())
