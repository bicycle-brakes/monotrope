#!/usr/bin/env python3
"""The one list of Omnigent tools this repository denies, and what is derived from it.

Omnigent's own tools reach a Claude Code session as ``mcp__omnigent__<tool>``.
A path rule or a hook on Claude Code's file tools does not see them, so each
tool that writes, runs, spawns or changes state is denied by name. This module
is the single place that names them (plans/changes/omnigent-deny-layers):

* layer 1 - ``permissions.deny`` in ``.claude/settings.json`` (holds alone);
* layer 2 - ``tools/omnigent/policy.yaml``, an Omnigent default policy that the
  maintainer installs per machine with ``tools/omnigent/install.sh``.

Both are rendered from ``DENIED_TOOLS`` / ``PROTECTED_PATHS`` below. Nothing
else in the repository types the list.

    python3 scripts/omnigent_policy.py --check            # is the tree what the list renders? (default)
    python3 scripts/omnigent_policy.py --write            # re-render policy.yaml and the settings rules
    python3 scripts/omnigent_policy.py --merge-config P   # merge the policies into Omnigent's config P
    python3 scripts/omnigent_policy.py --merge-config P --remove
    python3 scripts/omnigent_policy.py --installed P      # do the policies in P equal this repository's?

Two modes run only under Omnigent's own interpreter (they import Omnigent):
``--surface`` prints the tool names of Omnigent's native surface, ``--evaluate``
runs events read from stdin through the rendered policies.

``--print-python`` names that interpreter (``$OMNIGENT_PYTHON``, else the ``omnigent`` launcher's).
It needs nothing but the standard library, so any ``python3`` can ask; ``install.sh`` does, and
so the installer and the tests resolve Omnigent's interpreter in one place.
"""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import json
import os
import shlex
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY_FILE = ROOT / "tools" / "omnigent" / "policy.yaml"
SETTINGS_FILE = ROOT / ".claude" / "settings.json"

# ---------------------------------------------------------------------------
# The list. Tool -> the one-line reason. Grouped as in the spec's tables.
# ---------------------------------------------------------------------------

DENIED_TOOLS: dict[str, str] = {
    "sys_os_write": "writes a file",
    "sys_os_edit": "edits a file",
    "sys_os_shell": "runs a shell command, unconfined without a sandbox",
    "sys_agent_download": "writes an agent archive into the working directory",
    "sys_terminal_launch": "starts a shell in a terminal",
    "sys_terminal_send": "types into a terminal",
    "sys_terminal_close": "kills a terminal",
    "sys_session_create": "starts a child session",
    "sys_session_send": "messages a child session",
    "sys_session_close": "archives a session and stops its processes",
    "sys_session_rename": "retitles a session",
    "sys_session_share": "exposes a session's transcript",
    "sys_scheduled_task_create": "creates a scheduled job",
    "sys_scheduled_task_update": "changes a scheduled job",
    "sys_scheduled_task_delete": "deletes a scheduled job",
    "sys_call_async": "runs any granted tool in the background, sys_os_shell included",
    "sys_cancel_async": "cancels a background call",
    "sys_cancel_task": "cancels a task or a child session",
    "sys_read_inbox": "empties the inbox and writes a receipt",
    "sys_add_policy": "adds a policy to the session",
    "update_comment": "changes a review comment's status",
    "browser_navigate": "loads a URL in a live page",
    "browser_click": "acts on a live page",
    "browser_type": "types into a live page",
    "hindsight_retain": "sends session content to an outside memory service",
    "hindsight_recall": "sends session content to an outside memory service",
    "hindsight_reflect": "sends session content to an outside memory service",
}

ALLOWED_TOOLS: dict[str, str] = {
    "sys_os_read": "reads a file inside the working directory",
    "sys_terminal_read": "reads a terminal's screen",
    "sys_terminal_list": "lists terminals",
    "sys_session_list": "lists sessions",
    "sys_session_get_info": "reads a session's info",
    "sys_session_get_history": "reads a session's history",
    "sys_agent_list": "lists agents",
    "sys_agent_get": "reads an agent",
    "sys_scheduled_task_list": "lists scheduled jobs",
    "sys_policy_registry": "lists policy types",
    "sys_list_models": "reads the model catalogue",
    "sys_advise_models": "reads the model catalogue (rests on its docstring; the body was not read)",
    "list_comments": "reads review comments",
    "load_skill": "reads a skill",
    "read_skill_file": "reads a file of a skill",
    "browser_snapshot": "captures the current page",
    "browser_screenshot": "captures the current page",
}

# Suffix of a file path -> why it is protected.
PROTECTED_PATHS: dict[str, str] = {
    "/.omnigent/config.yaml": "carries the Omnigent default policy (layer 2)",
}

# Claude Code's own file tools, whose `file_path` the protected-path policy reads.
HARNESS_FILE_TOOLS: tuple[str, ...] = ("Write", "Edit", "MultiEdit")

PREFIX = "mcp__omnigent__"  # how Claude Code names an Omnigent tool
OWNED_PREFIX = "coding_harness__"  # what the installer may add, replace and remove
WRITING_POLICY = OWNED_PREFIX + "omnigent_writing_tools"
PATHS_POLICY = OWNED_PREFIX + "protected_paths"
CEL_HANDLER = "omnigent.policies.builtins.cel.cel_policy"

RESTART_CHANGED = (
    "Omnigent reads `policies:` only when its server starts, and a running background server is reused. "
    "If one runs, stop it with `omnigent server stop` (its sessions end); the next `omnigent claude` "
    "starts it with this policy. A foreground `omnigent server` reads it only with `--config <path>`."
)
RESTART_UNCHANGED = "no restart needed"

_HEADER = (
    "# GENERATED by scripts/omnigent_policy.py from its one list of Omnigent tools. Do not edit.\n"
    "# Change the list, then run: python3 scripts/omnigent_policy.py --write\n"
    "# Installed per machine, by the maintainer, in a terminal: tools/omnigent/install.sh\n"
    "# See tools/omnigent/README.md.\n"
)


class ConfigError(ValueError):
    """The Omnigent config is not something this module may merge into."""


# ---------------------------------------------------------------------------
# Layer 1 - Claude Code's permission rules
# ---------------------------------------------------------------------------


def _path_rules() -> list[str]:
    return [f"Edit(//**{suffix})" for suffix in PROTECTED_PATHS]


def _is_owned_rule(rule: str) -> bool:
    """A rule `--write` may replace: an Omnigent tool rule, or exactly a protected-path rule the list renders.

    An `Edit(//**...)` rule for any other path is the maintainer's; it is kept.
    """
    return rule.startswith(PREFIX) or rule in _path_rules()


def layer1_rules() -> list[str]:
    """The deny rules layer 1 owns: one per denied tool, one per protected path."""
    return [PREFIX + tool for tool in DENIED_TOOLS] + _path_rules()


# ---------------------------------------------------------------------------
# Layer 2 - the Omnigent default policy
# ---------------------------------------------------------------------------


def _q(text: str) -> str:
    """A string literal valid in both CEL and YAML double quotes (ASCII only)."""
    return json.dumps(text)


def _cel_list(items: list[str]) -> str:
    return "[\n" + ",\n".join(f"  {_q(item)}" for item in items) + "\n]"


def _guards_data() -> str:
    # Each guard protects the one after it: an evaluation error abstains, which would open the gate.
    return (
        'has(event.type) && type(event.type) == string && event.type == "tool_call"\n'
        "&& has(event.data) && type(event.data) == map\n"
        "&& has(event.data.name) && type(event.data.name) == string"
    )


def _writing_tools_expression() -> str:
    reason = (
        '"coding-harness: Omnigent\'s " + event.data.name + " writes, runs, spawns or changes state '
        "outside Claude Code's permission rules - use the harness's own tools "
        '(list: scripts/omnigent_policy.py)"'
    )
    # `in` over a literal list, not `.exists(t, ...)`: celpy evaluates both sides of `&&` and, on an event
    # without a name, the macro's chain of errors doubles its message at every element - 27 tools hang
    # the server (measured, see the plan's implementation notes).
    spellings = list(DENIED_TOOLS) + [PREFIX + tool for tool in DENIED_TOOLS]
    return (
        f"{_guards_data()}\n"
        f"&& event.data.name in {_cel_list(spellings)}\n"
        f'? {{"result": "DENY", "reason": {reason}}}\n'
        ": null"
    )


def _protected_paths_expression() -> str:
    reason = (
        '"coding-harness: " + event.data.arguments.file_path + " carries Omnigent\'s policy; '
        'only the maintainer changes it (tools/omnigent/install.sh)"'
    )
    ends_with = "\n    || ".join(f"event.data.arguments.file_path.endsWith({_q(suffix)})" for suffix in PROTECTED_PATHS)
    return (
        f"{_guards_data()}\n"
        f"&& event.data.name in {json.dumps(list(HARNESS_FILE_TOOLS))}\n"
        "&& has(event.data.arguments) && type(event.data.arguments) == map\n"
        "&& has(event.data.arguments.file_path) && type(event.data.arguments.file_path) == string\n"
        f"&& ({ends_with})\n"
        f'? {{"result": "DENY", "reason": {reason}}}\n'
        ": null"
    )


def owned_policies() -> dict[str, dict]:
    """The two policies, as the mapping that goes under `policies:`."""

    def policy(reason: str, expression: str) -> dict:
        return {
            "type": "function",
            "handler": CEL_HANDLER,
            "factory_params": {"reason": reason, "expression": expression},
        }

    return {
        WRITING_POLICY: policy(
            "coding-harness: this Omnigent tool writes, runs, spawns or changes state.",
            _writing_tools_expression(),
        ),
        PATHS_POLICY: policy(
            "coding-harness: this file carries Omnigent's policy.",
            _protected_paths_expression(),
        ),
    }


def _block(text: str, indent: int) -> str:
    pad = " " * indent
    return "\n".join(pad + line if line else line for line in text.split("\n"))


def render_policy_yaml() -> str:
    """The text of tools/omnigent/policy.yaml."""
    out = [_HEADER, "policies:\n"]
    for name, spec in owned_policies().items():
        params = spec["factory_params"]
        out.append(f"  {name}:\n")
        out.append("    type: function\n")
        out.append(f"    handler: {spec['handler']}\n")
        out.append("    factory_params:\n")
        out.append(f"      reason: {_q(params['reason'])}\n")
        out.append("      expression: |-\n")
        out.append(_block(params["expression"], 8) + "\n")
    return "".join(out)


# ---------------------------------------------------------------------------
# The tree: check and write
# ---------------------------------------------------------------------------


def _load_settings(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def check(root: Path = ROOT) -> list[str]:
    """Problems between the tree and the list; empty when the tree is what the list renders."""
    problems: list[str] = []
    policy_file = root / "tools" / "omnigent" / "policy.yaml"
    settings_file = root / ".claude" / "settings.json"

    if not policy_file.exists():
        problems.append(f"{policy_file.relative_to(root)} is missing")
    elif policy_file.read_text(encoding="utf-8") != render_policy_yaml():
        problems.append(f"{policy_file.relative_to(root)} differs from what the list renders")

    try:
        settings = _load_settings(settings_file)
    except (OSError, json.JSONDecodeError) as exc:
        problems.append(f".claude/settings.json cannot be read: {exc}")
        return problems
    deny = settings.get("permissions", {}).get("deny", [])
    wanted = layer1_rules()
    problems += [f".claude/settings.json lacks the deny rule {rule}" for rule in wanted if rule not in deny]
    allowed_names = [PREFIX + tool for tool in ALLOWED_TOOLS] + [PREFIX.rstrip("_")]
    for rule in deny:
        if rule in wanted or "(" in rule:
            continue
        if rule.startswith(PREFIX) or any(fnmatch.fnmatchcase(name, rule) for name in allowed_names):
            problems.append(f".claude/settings.json denies {rule}, which is not on the list of denied tools")
    return problems


def write(root: Path = ROOT) -> None:
    """Re-render policy.yaml and the Omnigent rules of `.claude/settings.json`."""
    policy_file = root / "tools" / "omnigent" / "policy.yaml"
    policy_file.parent.mkdir(parents=True, exist_ok=True)
    policy_file.write_text(render_policy_yaml(), encoding="utf-8")

    settings_file = root / ".claude" / "settings.json"
    settings = _load_settings(settings_file)
    permissions = settings.setdefault("permissions", {})
    kept = [rule for rule in permissions.get("deny", []) if not _is_owned_rule(rule)]
    permissions["deny"] = kept + layer1_rules()
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(json.dumps(settings, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# The installer's core: merge into Omnigent's global config
# ---------------------------------------------------------------------------


def _load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    import yaml  # not at module level: --print-python must run under any python3

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ConfigError(f"{path} is not a YAML mapping - refusing to touch it")
    policies = data.get("policies")
    if policies is not None and not isinstance(policies, dict):
        raise ConfigError(f"{path}: `policies:` is neither a mapping nor empty - refusing to touch it")
    return data


def _file_policies() -> dict[str, dict]:
    """The policies of the committed tools/omnigent/policy.yaml."""
    import yaml

    data = yaml.safe_load(POLICY_FILE.read_text(encoding="utf-8"))
    return dict(data["policies"])


def _validate(policies: dict[str, dict]) -> None:
    """Omnigent's own parser over the whole block, then its CEL compiler over each owned expression."""
    try:
        from omnigent.policies.builtins.cel import cel_policy
        from omnigent.spec import parse_default_policies
    except ImportError as exc:
        raise RuntimeError(
            f"cannot validate: Omnigent is not importable here ({exc}) - run under Omnigent's own Python "
            "(the launcher's interpreter, or set OMNIGENT_PYTHON)"
        ) from exc
    # A foreign policy the server could not boot with fails here too - that is intended.
    parse_default_policies(policies, expand_env=False)
    for name, spec in policies.items():
        if name.startswith(OWNED_PREFIX):
            cel_policy(**spec["factory_params"])


def _dump(data: dict) -> str:
    import yaml

    class _Dumper(yaml.SafeDumper):
        pass

    def _str(dumper: yaml.SafeDumper, value: str):
        style = "|" if "\n" in value else None
        return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)

    _Dumper.add_representer(str, _str)
    return yaml.dump(data, Dumper=_Dumper, sort_keys=False, default_flow_style=False, allow_unicode=True)


def merge_config(
    path: Path,
    policies: dict[str, dict] | None = None,
    *,
    remove: bool = False,
    validate: bool = True,
) -> str:
    """Merge the owned policies into the Omnigent config at `path`.

    Returns "created", "merged", "removed" or "unchanged". Keeps every key and every policy not
    named ``coding_harness__*``; replaces the owned ones as a set. Validates before anything is
    written and keeps `<name>.bak-<timestamp>` before a change. `remove=True` does not validate what
    remains: it deletes only owned policies, so it cannot make a foreign one worse, and a foreign
    policy Omnigent rejects must not block the moment the owned ones are to go.
    """
    path = Path(path)
    existed = path.exists()
    config = _load_config(path)
    old_policies = config.get("policies") or {}
    foreign = {k: v for k, v in old_policies.items() if not str(k).startswith(OWNED_PREFIX)}
    owned = {} if remove else (policies if policies is not None else _file_policies())

    new_config = dict(config)
    merged = {**foreign, **owned}
    if merged:
        new_config["policies"] = merged
    else:
        new_config.pop("policies", None)

    if new_config == config and (existed or remove):
        return "unchanged"
    if validate and merged and not remove:
        _validate(merged)

    if existed:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.name}.bak-{stamp}")
        shutil.copy2(path, backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(_dump(new_config))
        Path(tmp_name).replace(path)
    except BaseException:
        with contextlib.suppress(OSError):
            Path(tmp_name).unlink()
        raise
    if remove:
        return "removed"
    return "merged" if existed else "created"


def last_backup(path: Path) -> Path | None:
    backups = sorted(path.parent.glob(path.name + ".bak-*"))
    return backups[-1] if backups else None


def installed_differences(path: Path) -> list[str]:
    """How the owned policies in the config at `path` differ from the repository's; empty when equal."""
    if not Path(path).exists():
        return [f"{path} does not exist"]
    have = {
        k: v for k, v in (_load_config(Path(path)).get("policies") or {}).items() if str(k).startswith(OWNED_PREFIX)
    }
    want = _file_policies()
    out = [f"missing in {path}: {name}" for name in want if name not in have]
    out += [f"not in the repository (stale): {name}" for name in have if name not in want]
    out += [f"differs: {name}" for name in want if name in have and have[name] != want[name]]
    return out


# ---------------------------------------------------------------------------
# Omnigent's interpreter (installer and offline tests)
# ---------------------------------------------------------------------------


def omnigent_python() -> str | None:
    """$OMNIGENT_PYTHON, else the interpreter of the `omnigent` launcher's `#!` line; None when neither is usable."""
    env = os.environ.get("OMNIGENT_PYTHON")
    if env:
        return env if os.access(env, os.X_OK) else None
    launcher = shutil.which("omnigent")
    if not launcher:
        return None
    try:
        with Path(launcher).resolve().open(encoding="utf-8", errors="replace") as handle:
            head = [handle.readline().strip(), handle.readline().strip()]
    except OSError:
        return None
    return _launcher_interpreter(*head)


def _launcher_interpreter(first: str, second: str = "") -> str | None:
    """The interpreter a launcher's first two lines name; None when it is not an executable file.

    Three forms: `#!/path/to/python`, `#!/usr/bin/env python3` (looked up on the PATH), and the
    `#!/bin/sh` + `'''exec' "/path with spaces/python" "$0" "$@"` form installers use for a path a
    shebang cannot carry. install.sh asks this function (`--print-python`) rather than parse the line itself.
    """
    if not first.startswith("#!"):
        return None
    try:
        parts = shlex.split(first[2:])
        if Path(parts[0]).name in ("sh", "bash") and second.startswith("'''exec'"):
            parts = shlex.split(second[len("'''exec'") :])
    except (ValueError, IndexError):
        return None
    if Path(parts[0]).name == "env" and len(parts) > 1:
        found = shutil.which(parts[1])
        return found if found and os.access(found, os.X_OK) else None
    return parts[0] if os.access(parts[0], os.X_OK) else None


def _surface() -> list[str]:
    from omnigent.runner.tool_dispatch import _NATIVE_RELAY_BUILTIN_TOOLS
    from omnigent.tools.builtins.os_env import SysOsEditTool, SysOsReadTool, SysOsShellTool, SysOsWriteTool

    os_tools = {tool.name() for tool in (SysOsReadTool, SysOsWriteTool, SysOsEditTool, SysOsShellTool)}
    return sorted(set(_NATIVE_RELAY_BUILTIN_TOOLS) | os_tools)


def _evaluate(events: list[dict]) -> list[dict]:
    """Per event and policy: what `cel_policy` returns, and what celpy raises on the raw expression."""
    import celpy
    from celpy.adapter import json_to_cel
    from omnigent.policies.builtins.cel import cel_policy
    from omnigent.policies.schema import request_user_text
    from omnigent.spec import parse_default_policies

    policies = _file_policies()
    parse_default_policies(policies, expand_env=False)
    env = celpy.Environment()
    programs = {name: env.program(env.compile(spec["factory_params"]["expression"])) for name, spec in policies.items()}
    callables = {name: cel_policy(**spec["factory_params"]) for name, spec in policies.items()}

    results = []
    for event in events:
        per_policy = {}
        for name, program in programs.items():
            cel_event = {k: v for k, v in event.items() if k != "llm_client"}
            if event.get("type") == "request":
                cel_event["data"] = request_user_text(event.get("data"))
            error = None
            try:
                program.evaluate({"event": json_to_cel(cel_event)})
            except Exception as exc:  # the point is to see every kind of failure
                error = f"{type(exc).__name__}: {exc}"
            per_policy[name] = {"result": callables[name](event), "error": error}
        results.append(per_policy)
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="the tree is what the list renders (default)")
    mode.add_argument("--write", action="store_true", help="re-render policy.yaml and the settings rules")
    mode.add_argument("--merge-config", metavar="PATH", help="merge the policies into the Omnigent config at PATH")
    mode.add_argument("--installed", metavar="PATH", help="do the policies at PATH equal the repository's?")
    mode.add_argument("--print-python", action="store_true", help="print Omnigent's interpreter; exit 1 if none")
    mode.add_argument("--surface", action="store_true", help="(Omnigent's Python) print the native tool surface")
    mode.add_argument("--evaluate", action="store_true", help="(Omnigent's Python) evaluate events from stdin")
    parser.add_argument("--remove", action="store_true", help="with --merge-config: take the owned policies out")
    args = parser.parse_args(argv)

    if args.remove and not args.merge_config:
        parser.error("--remove goes with --merge-config")

    if args.write:
        write()
        print("rewrote tools/omnigent/policy.yaml and the Omnigent rules of .claude/settings.json")
        return 0

    if args.print_python:
        found = omnigent_python()
        if not found:
            return 1
        print(found)
        return 0

    if args.surface:
        print(json.dumps(_surface()))
        return 0

    if args.evaluate:
        print(json.dumps(_evaluate(json.load(sys.stdin)), default=str))
        return 0

    if args.installed:
        diffs = installed_differences(Path(args.installed))
        if diffs:
            print("\n".join(diffs))
            return 1
        print(f"the coding_harness__* policies in {args.installed} match this repository's")
        return 0

    if args.merge_config:
        path = Path(args.merge_config)
        try:
            status = merge_config(path, remove=args.remove)
        except (ConfigError, RuntimeError, ValueError) as exc:
            print(f"nothing written: {exc}", file=sys.stderr)
            return 1
        print(f"{status}: {path}")
        if status in ("merged", "removed"):
            backup = last_backup(path)
            if backup:
                print(f"backup: {backup}")
            print("comments in the config are not carried over by the merge; the backup keeps them")
        if status in ("created", "merged", "removed"):
            print(RESTART_CHANGED)
        else:
            print(RESTART_UNCHANGED)
        return 0

    problems = check()
    if problems:
        print("\n".join(problems))
        print("run: python3 scripts/omnigent_policy.py --write")
        return 1
    print("the tree is what the list renders")
    return 0


if __name__ == "__main__":
    sys.exit(main())
