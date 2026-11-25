#!/usr/bin/env python3
"""Thin pre-tool hook adapters: each host's input in, the shared check's decision out in the host's form.

    python3 scripts/agent_policy_hooks.py claude-code    # registered in .claude/settings.json
    python3 scripts/agent_policy_hooks.py antigravity    # registered in .agents/hooks.json

Both registrations are rendered by ``scripts/agent_policy.py``; the decision is
always that module's (``decide_shell`` for a shell command, ``decide_tool`` for
any other tool name). An adapter changes it only in three ways:

* an ask becomes a deny in an unattended run - ``HARNESS_UNATTENDED`` is set,
  nonempty and not ``0``; unset, empty or ``0`` is attended;
* an ask becomes a deny on a host whose protocol cannot express ask;
* a fault - unreadable policy, malformed input, an exception - becomes a deny
  that names the fault, whenever the adapter can still answer.

Claude Code (hooks reference, ``PreToolUse``): the input carries ``tool_name``
and ``tool_input`` (``command`` for ``Bash``); ask and deny are answered as
``hookSpecificOutput.permissionDecision`` on stdout with exit 0; abstain is
exit 0 with no output.

Antigravity: the shell tool is ``run_command``. Its hook payload and result
form are taken here as the research recorded them and are confirmed only by the
one-time host check the policy documentation records; until then the adapter
reads the tool name and command under the spellings below, cannot express ask
(so ask is denied), and answers a deny both as ``{"decision": "deny"}`` on
stdout and as exit 2 with the reason on stderr. No support is claimed without
that check (plans/changes/agent-policy-list, criterion 17).
"""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

SCRIPTS = Path(__file__).resolve().parent

DENY = "deny"
ASK = "ask"
ABSTAIN = "abstain"

UNATTENDED_VARIABLE = "HARNESS_UNATTENDED"

# Whether a host's hook protocol can express "ask the user".
CAN_ASK: dict[str, bool] = {"claude-code": True, "antigravity": False}

ANTIGRAVITY_SHELL_TOOLS = ("run_command",)
ANTIGRAVITY_NAME_KEYS = ("tool_name", "toolName", "name", "tool")
ANTIGRAVITY_INPUT_KEYS = ("tool_input", "toolInput", "arguments", "args", "input", "parameters")
ANTIGRAVITY_COMMAND_KEYS = ("command", "CommandLine", "commandLine", "cmd")


class HookInputError(ValueError):
    """The host's hook input does not have the shape this adapter reads."""


@dataclass(frozen=True)
class Call:
    """What the host is about to run: a shell line, or a tool by name."""

    kind: str  # "shell" or "tool"
    value: str


@dataclass(frozen=True)
class Outcome:
    """The adapter's answer before it is written in the host's form."""

    kind: str
    message: str


def is_unattended(env: Mapping[str, str]) -> bool:
    """Unattended when `HARNESS_UNATTENDED` is nonempty and not `0`."""
    return env.get(UNATTENDED_VARIABLE, "") not in ("", "0")


def load_policy() -> ModuleType:
    """The shared check, imported from beside this file."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import agent_policy

    return agent_policy


def _text(value: object, what: str) -> str:
    if not isinstance(value, str) or not value:
        raise HookInputError(f"{what} is missing or not a string")
    return value


def parse_claude_code(payload: dict) -> Call:
    """Claude Code's PreToolUse input: `tool_name`, and `tool_input.command` for Bash."""
    name = _text(payload.get("tool_name"), "tool_name")
    if name != "Bash":
        return Call("tool", name)
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise HookInputError("tool_input is missing or not an object")
    return Call("shell", _text(tool_input.get("command"), "tool_input.command"))


def _first(payload: dict, keys: tuple[str, ...]) -> object:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def parse_antigravity(payload: dict) -> Call:
    """Antigravity's pre-tool input: the tool name, and the command for `run_command`."""
    name = _text(_first(payload, ANTIGRAVITY_NAME_KEYS), "the tool name")
    if name not in ANTIGRAVITY_SHELL_TOOLS:
        return Call("tool", name)
    tool_input = _first(payload, ANTIGRAVITY_INPUT_KEYS)
    if not isinstance(tool_input, dict):
        raise HookInputError("the tool input is missing or not an object")
    return Call("shell", _text(_first(tool_input, ANTIGRAVITY_COMMAND_KEYS), "the command"))


PARSERS: dict[str, Callable[[dict], Call]] = {
    "claude-code": parse_claude_code,
    "antigravity": parse_antigravity,
}


def fault(exc: BaseException) -> Outcome:
    return Outcome(
        DENY,
        f"coding-harness agent policy fault ({type(exc).__name__}: {exc}); denied because the check could not run",
    )


def decide(host: str, payload_text: str, env: Mapping[str, str]) -> Outcome:
    """The shared check's decision for the host's input, with the adapter's three changes applied."""
    try:
        policy = load_policy()
        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError as exc:
            raise HookInputError(f"the hook input is not JSON ({exc})") from exc
        if not isinstance(payload, dict):
            raise HookInputError("the hook input is not a JSON object")
        call = PARSERS[host](payload)
        decision = policy.decide_shell(call.value) if call.kind == "shell" else policy.decide_tool(call.value)
        kind, message = decision.kind, decision.message()
    except Exception as exc:  # every fault denies, named
        return fault(exc)
    if kind == ASK and is_unattended(env):
        kind, message = DENY, f"{message} - denied: unattended run ({UNATTENDED_VARIABLE}), nobody can answer"
    if kind == ASK and not CAN_ASK[host]:
        kind, message = DENY, f"{message} - denied: this host cannot ask, so an ask is a deny"
    return Outcome(kind, message)


def render(host: str, outcome: Outcome) -> tuple[int, str, str]:
    """(exit code, stdout, stderr) in the host's form."""
    if outcome.kind == ABSTAIN:
        return 0, "", ""
    if host == "claude-code":
        body = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": outcome.kind,
                "permissionDecisionReason": outcome.message,
            }
        }
        return 0, json.dumps(body) + "\n", ""
    return 2, json.dumps({"decision": DENY, "reason": outcome.message}) + "\n", outcome.message + "\n"


def run(host: str, payload_text: str, env: Mapping[str, str]) -> tuple[int, str, str]:
    """One hook call: decide and render; a fault while rendering still denies."""
    try:
        return render(host, decide(host, payload_text, env))
    except Exception as exc:  # the adapter answers whenever it can
        message = fault(exc).message
        return 2, json.dumps({"decision": DENY, "reason": message}) + "\n", message + "\n"


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1 or argv[0] not in PARSERS:
        print(
            f"usage: agent_policy_hooks.py {{{','.join(PARSERS)}}} - denied: no known host named",
            file=sys.stderr,
        )
        return 2
    try:
        payload_text = sys.stdin.read()
    except Exception as exc:  # unreadable stdin is a fault, answered in the host's form
        code, out, err = render(argv[0], fault(exc))
    else:
        code, out, err = run(argv[0], payload_text, os.environ)
    sys.stdout.write(out)
    sys.stderr.write(err)
    return code


if __name__ == "__main__":
    sys.exit(main())
