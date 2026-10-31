"""Omnigent's writing tools are denied by name, from one list (plans/changes/omnigent-deny-layers).

Layer 1 is `permissions.deny` in `.claude/settings.json`; layer 2 is
`tools/omnigent/policy.yaml`, an Omnigent default policy. Both are rendered from
`scripts/omnigent_policy.py`. Nothing here types the tool list: every test reads it
from that module, so a tool moved between the two lists moves in the tests too.

Tests marked "Omnigent" run Omnigent's own code in a subprocess under Omnigent's
interpreter and skip, saying why, where Omnigent is not installed (CI). Nothing here
touches the real ~/.omnigent: every config path is under `tmp_path`.
"""

from __future__ import annotations

import fnmatch
import json
import os
import pty
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import omnigent_policy as op  # noqa: E402

SCRIPT = REPO / "scripts" / "omnigent_policy.py"
INSTALLER = REPO / "tools" / "omnigent" / "install.sh"
SETTINGS = REPO / ".claude" / "settings.json"
SESSION_START_HOOK = '"$CLAUDE_PROJECT_DIR"/tools/bd prime --hook-json'
# The reconcile-then-prime wrapper that takes the direct prime's place at
# session start (bead coding-harness-l1if); the wiring is the held-file step.
START_HOOK_COMMAND = 'bash "$CLAUDE_PROJECT_DIR/tools/claude-code/hooks/beads-start.sh"'
PROTECTED = next(iter(op.PROTECTED_PATHS))  # "/.omnigent/config.yaml"
POLICIES = (op.WRITING_POLICY, op.ASKED_POLICY, op.PATHS_POLICY)  # the three policies the list renders


# ---------------------------------------------------------------------------
# Omnigent's interpreter: skip with a stated reason where it is not there
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def omnigent_py() -> str:
    py = op.omnigent_python()
    if py is None:
        pytest.skip(
            "Omnigent is not installed here (no OMNIGENT_PYTHON, no omnigent on PATH) - "
            "the policy was not evaluated with Omnigent's code"
        )
    probe = subprocess.run(
        [py, "-c", "import omnigent.spec, omnigent.policies.builtins.cel"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if probe.returncode != 0:
        pytest.skip(
            f"{py} cannot import omnigent.spec and omnigent.policies.builtins.cel: {probe.stderr.strip()[-300:]}"
        )
    return py


def _env(tmp_path: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["OMNIGENT_CONFIG_HOME"] = str(tmp_path / "omnigent-config")
    env["OMNIGENT_DATA_DIR"] = str(tmp_path / "omnigent-data")
    env["HOME"] = str(tmp_path / "home")
    return env


def _run(py: str, args: list[str], tmp_path: Path, stdin: str | None = None, timeout: int = 120):
    try:
        return subprocess.run(
            [py, str(SCRIPT), *args],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=_env(tmp_path),
            check=False,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"{' '.join(args)} took more than {timeout} s - an expression that never finishes on some event?")


def _evaluate(py: str, tmp_path: Path, events: list[dict]) -> list[dict]:
    done = _run(py, ["--evaluate"], tmp_path, json.dumps(events))
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def _tool_call(name, arguments=None) -> dict:
    data: dict = {"name": name}
    if arguments is not None:
        data["arguments"] = arguments
    return {"type": "tool_call", "target": name, "data": data}


def _verdict(entry: dict, policy: str) -> dict | None:
    assert entry[policy]["error"] is None, entry[policy]["error"]
    return entry[policy]["result"]


# ---------------------------------------------------------------------------
# Criterion 1 - one list
# ---------------------------------------------------------------------------


def test_every_name_is_listed_once_with_a_reason() -> None:
    tables = {"denied": op.DENIED_TOOLS, "asked": op.ASKED_TOOLS, "allowed": op.ALLOWED_TOOLS}
    for left, right in (("denied", "asked"), ("denied", "allowed"), ("asked", "allowed")):
        both = set(tables[left]) & set(tables[right])
        assert not both, f"in both the {left} and the {right} list: {sorted(both)}"
    for table in (*tables.values(), op.PROTECTED_PATHS):
        for name, reason in table.items():
            assert isinstance(reason, str) and reason.strip(), f"{name!r} has no reason"
    assert op.DENIED_TOOLS and op.ASKED_TOOLS and op.ALLOWED_TOOLS and op.PROTECTED_PATHS, (
        "an empty list guards nothing"
    )


def test_the_tree_is_what_the_list_renders() -> None:
    assert op.check() == [], "run: python3 scripts/omnigent_policy.py --write"


def test_a_hand_edit_or_a_stale_render_is_caught(tmp_path: Path) -> None:
    op.write(tmp_path)
    assert op.check(tmp_path) == []

    policy = tmp_path / "tools" / "omnigent" / "policy.yaml"
    policy.write_text(policy.read_text(encoding="utf-8").replace('"sys_os_shell",', ""), encoding="utf-8")
    assert any("policy.yaml differs" in p for p in op.check(tmp_path))
    op.write(tmp_path)

    settings = tmp_path / ".claude" / "settings.json"
    data = json.loads(settings.read_text(encoding="utf-8"))
    data["permissions"]["deny"].remove(op.PREFIX + "sys_os_write")
    settings.write_text(json.dumps(data), encoding="utf-8")
    assert any(op.PREFIX + "sys_os_write" in p for p in op.check(tmp_path))


# ---------------------------------------------------------------------------
# Criterion 2 - complete against the installed Omnigent
# ---------------------------------------------------------------------------


def test_the_list_matches_omnigents_native_surface(omnigent_py: str, tmp_path: Path) -> None:
    done = _run(omnigent_py, ["--surface"], tmp_path)
    assert done.returncode == 0, done.stderr
    surface = set(json.loads(done.stdout))
    listed = set(op.DENIED_TOOLS) | set(op.ASKED_TOOLS) | set(op.ALLOWED_TOOLS)
    assert surface - listed == set(), f"Omnigent offers tools this list does not classify: {sorted(surface - listed)}"
    assert listed - surface == set(), f"listed tools Omnigent does not offer: {sorted(listed - surface)}"


# ---------------------------------------------------------------------------
# Criterion 3 - layer 1 holds alone
# ---------------------------------------------------------------------------


def _deny() -> list[str]:
    return json.loads(SETTINGS.read_text(encoding="utf-8"))["permissions"]["deny"]


def test_settings_deny_every_denied_tool() -> None:
    deny = _deny()
    missing = [rule for rule in op.layer1_rules() if rule not in deny]
    assert not missing, f".claude/settings.json does not deny: {missing}"
    assert f"Edit(//**{PROTECTED})" in deny


def test_settings_deny_no_allowed_tool_and_no_blanket_rule() -> None:
    blanket = {"mcp__omnigent", "mcp__omnigent__*", "mcp__*", "*"}
    for rule in _deny():
        assert rule not in blanket, f"blanket rule {rule!r} denies all of Omnigent"
        if "(" in rule:
            continue
        for tool in op.ALLOWED_TOOLS:
            assert not fnmatch.fnmatchcase(op.PREFIX + tool, rule), f"{rule!r} denies the allowed tool {tool}"


def test_check_names_an_allowed_tool_or_a_blanket_rule_in_the_settings(tmp_path: Path) -> None:
    op.write(tmp_path)
    settings = tmp_path / ".claude" / "settings.json"
    base = json.loads(settings.read_text(encoding="utf-8"))
    for bad in (op.PREFIX + "sys_os_read", "mcp__omnigent__*", "mcp__omnigent", "mcp__*", "*"):
        planted = json.loads(json.dumps(base))
        planted["permissions"]["deny"].append(bad)
        settings.write_text(json.dumps(planted), encoding="utf-8")
        assert any(bad in p for p in op.check(tmp_path)), f"{bad!r} was not caught"


def _permissions() -> dict:
    return json.loads(SETTINGS.read_text(encoding="utf-8"))["permissions"]


def test_settings_ask_exactly_the_asked_tools() -> None:
    """Omnigent's own ask rules are exactly the asked tools.

    The merge rules beside them in `permissions.ask` are held by `tests/test_merge_guard.py`.
    """
    ask = _permissions()["ask"]
    assert sorted(r for r in ask if r.startswith(op.PREFIX)) == sorted(op.PREFIX + tool for tool in op.ASKED_TOOLS)
    assert op.PREFIX + "sys_advise_models" in ask
    for kind in ("deny", "allow"):
        for rule in _permissions().get(kind, []):
            for tool in op.ASKED_TOOLS:
                assert not fnmatch.fnmatchcase(op.PREFIX + tool, rule), f"{kind} rule {rule!r} covers the asked {tool}"


def test_check_names_a_missing_ask_rule_and_an_asked_tool_moved_to_deny_or_allow(tmp_path: Path) -> None:
    op.write(tmp_path)
    settings = tmp_path / ".claude" / "settings.json"
    base = json.loads(settings.read_text(encoding="utf-8"))
    asked = op.PREFIX + next(iter(op.ASKED_TOOLS))

    missing = json.loads(json.dumps(base))
    missing["permissions"]["ask"].remove(asked)
    settings.write_text(json.dumps(missing), encoding="utf-8")
    assert any("lacks the ask rule" in p and asked in p for p in op.check(tmp_path)), "a missing ask rule passed"

    extra = json.loads(json.dumps(base))
    extra["permissions"]["ask"].append(op.PREFIX + "sys_os_read")
    settings.write_text(json.dumps(extra), encoding="utf-8")
    assert any("sys_os_read" in p for p in op.check(tmp_path)), "an ask rule outside the list passed"

    for kind in ("deny", "allow"):
        for rule in (asked, "mcp__omnigent__*", "mcp__omnigent"):
            moved = json.loads(json.dumps(base))
            moved["permissions"].setdefault(kind, []).append(rule)
            settings.write_text(json.dumps(moved), encoding="utf-8")
            assert any(kind in p and rule in p for p in op.check(tmp_path)), f"{kind} {rule!r} was not caught"

    settings.write_text(json.dumps(base), encoding="utf-8")
    assert op.check(tmp_path) == []


def test_a_tool_moved_between_lists_is_caught(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The list says deny, the rendered tree still says ask: the tree is stale, and check() says so."""
    op.write(tmp_path)
    tool = next(iter(op.ASKED_TOOLS))
    monkeypatch.setattr(op, "DENIED_TOOLS", {**op.DENIED_TOOLS, tool: op.ASKED_TOOLS[tool]})
    monkeypatch.setattr(op, "ASKED_TOOLS", {})
    problems = op.check(tmp_path)
    assert any("policy.yaml differs" in p for p in problems)
    assert any(f"lacks the deny rule {op.PREFIX}{tool}" in p for p in problems)
    assert any(f"asks about {op.PREFIX}{tool}" in p for p in problems)


def test_write_keeps_foreign_ask_rules_and_replaces_owned_ones(tmp_path: Path) -> None:
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(
        json.dumps({"permissions": {"ask": ["Bash(git push:*)", "mcp__omnigent__stale_tool"]}}), encoding="utf-8"
    )
    op.write(tmp_path)
    ask = json.loads(settings.read_text(encoding="utf-8"))["permissions"]["ask"]
    assert ask == ["Bash(git push:*)", *op.layer1_ask_rules()]
    assert op.check(tmp_path) == []


def test_start_hook_wires_reconciliation_before_prime() -> None:
    """The SessionStart hook runs the reconcile-then-prime wrapper, not the
    direct prime (bead coding-harness-l1if, criterion 10).

    The settings timeout must outlast the wrapper's own bounds (reconcile, scan
    and prime defaults read from the hook), or the harness kills the wrapper
    mid-reconciliation.
    """
    hooks = json.loads(SETTINGS.read_text(encoding="utf-8"))["hooks"]["SessionStart"]
    entries = [h for group in hooks for h in group["hooks"]]
    commands = [h["command"] for h in entries]
    assert commands == [START_HOOK_COMMAND], f"the SessionStart hook must run the wrapper: {commands}"
    hook = (REPO / "tools" / "claude-code" / "hooks" / "beads-start.sh").read_text(encoding="utf-8")
    bounds = sum(int(v) for v in re.findall(r"^[A-Z_]+_TIMEOUT=\$\{BEADS_START_[A-Z_]+:-(\d+)\}", hook, re.M))
    assert bounds > 0, "the hook's own time bounds were not found"
    assert all(isinstance(h.get("timeout"), int) and h["timeout"] > bounds for h in entries), (
        f"the wrapper needs a timeout above its own bounds ({bounds} s) covering reconciliation and prime"
    )


def test_write_keeps_hooks_and_foreign_rules_and_is_idempotent(tmp_path: Path) -> None:
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    hooks = {"SessionStart": [{"hooks": [{"command": SESSION_START_HOOK, "type": "command"}], "matcher": ""}]}
    settings.write_text(
        json.dumps({"hooks": hooks, "permissions": {"deny": ["Bash(rm -rf /)", "mcp__omnigent__stale_tool"]}}),
        encoding="utf-8",
    )
    op.write(tmp_path)
    once = settings.read_text(encoding="utf-8")
    data = json.loads(once)
    assert data["hooks"] == hooks
    assert data["permissions"]["deny"][0] == "Bash(rm -rf /)"
    assert "mcp__omnigent__stale_tool" not in data["permissions"]["deny"], "an owned rule outside the list survived"
    assert data["permissions"]["deny"][1:] == op.layer1_rules()
    op.write(tmp_path)
    assert settings.read_text(encoding="utf-8") == once


def test_write_keeps_an_edit_rule_it_does_not_own(tmp_path: Path) -> None:
    """A hand-added `Edit(//**...)` rule for another path is the maintainer's; only the listed path is ours."""
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    mine = ["Edit(//**/secrets/**)", "Edit(//**/.env)"]
    stale_owned = [*op._path_rules(), "mcp__omnigent__stale_tool"]
    settings.write_text(
        json.dumps({"permissions": {"deny": [mine[0], *stale_owned, mine[1]]}}),
        encoding="utf-8",
    )
    op.write(tmp_path)
    deny = json.loads(settings.read_text(encoding="utf-8"))["permissions"]["deny"]
    assert deny == mine + op.layer1_rules(), "a foreign Edit rule was dropped, or the owned ones were not restored"
    assert deny.count(op._path_rules()[0]) == 1


# ---------------------------------------------------------------------------
# Criterion 4 - layer 2 is a file in this repository
# ---------------------------------------------------------------------------


def test_policy_file_has_only_the_three_owned_policies() -> None:
    data = yaml.safe_load(op.POLICY_FILE.read_text(encoding="utf-8"))
    assert list(data) == ["policies"]
    assert sorted(data["policies"]) == sorted(POLICIES)
    for name, spec in data["policies"].items():
        assert spec["type"] == "function", name
        assert spec["handler"] == op.CEL_HANDLER, name
        assert sorted(spec["factory_params"]) == ["expression", "reason"], name


# ---------------------------------------------------------------------------
# Criterion 5 - layer 2 behaves, measured with Omnigent's own code
# ---------------------------------------------------------------------------


def test_policy_denies_denied_tools_and_leaves_allowed_ones(omnigent_py: str, tmp_path: Path) -> None:
    events, expect = [], []
    for tool in op.DENIED_TOOLS:
        for name in (tool, op.PREFIX + tool):
            for arguments in (None, {}, {"path": "/x", "content": "y"}):
                events.append(_tool_call(name, arguments))
                expect.append((name, True))
    for tool in op.ALLOWED_TOOLS:
        for name in (tool, op.PREFIX + tool):
            events.append(_tool_call(name, {}))
            expect.append((name, False))

    for entry, (name, denied) in zip(_evaluate(omnigent_py, tmp_path, events), expect, strict=True):
        verdict = _verdict(entry, op.WRITING_POLICY)
        if denied:
            assert verdict and verdict["result"] == "DENY", f"{name} was not denied"
            assert name in verdict["reason"], f"the refusal of {name} does not name it: {verdict['reason']}"
        else:
            assert verdict is None, f"{name} is allowed but was refused"
        assert _verdict(entry, op.PATHS_POLICY) is None, f"{name} touched the protected-path policy"
        assert _verdict(entry, op.ASKED_POLICY) is None, f"{name} touched the asked-tools policy"


def test_policy_asks_about_asked_tools_and_nothing_else(omnigent_py: str, tmp_path: Path) -> None:
    events, expect = [], []
    for tool in op.ASKED_TOOLS:
        for name in (tool, op.PREFIX + tool):
            for arguments in (None, {}, {"task": "write the release notes"}):
                events.append(_tool_call(name, arguments))
                expect.append(name)

    for entry, name in zip(_evaluate(omnigent_py, tmp_path, events), expect, strict=True):
        verdict = _verdict(entry, op.ASKED_POLICY)
        assert verdict and verdict["result"] == "ASK", f"{name} was not asked about"
        assert name in verdict["reason"], f"the question about {name} does not name it: {verdict['reason']}"
        assert _verdict(entry, op.WRITING_POLICY) is None, f"{name} is asked about, and was also denied"
        assert _verdict(entry, op.PATHS_POLICY) is None, f"{name} touched the protected-path policy"


def test_policy_protects_omnigents_config_file(omnigent_py: str, tmp_path: Path) -> None:
    config = "/Users/someone/.omnigent/config.yaml"
    events = [_tool_call(tool, {"file_path": config}) for tool in op.HARNESS_FILE_TOOLS]
    others = [
        "/Users/someone/.omnigent/config.yaml.bak-20260929",
        "/Users/someone/.omnigent/other.yaml",
        "/Users/someone/project/config.yaml",
        "/Users/someone/omnigent/config.yaml",
        "config.yaml",
    ]
    events += [_tool_call("Write", {"file_path": path}) for path in others]
    events += [_tool_call("Read", {"file_path": config}), _tool_call("Bash", {"command": f"cat {config}"})]

    results = _evaluate(omnigent_py, tmp_path, events)
    for entry, tool in zip(results, op.HARNESS_FILE_TOOLS, strict=False):
        verdict = _verdict(entry, op.PATHS_POLICY)
        assert verdict and verdict["result"] == "DENY", f"{tool} on the config file was not denied"
        assert config in verdict["reason"]
    for entry in results[len(op.HARNESS_FILE_TOOLS) :]:
        assert _verdict(entry, op.PATHS_POLICY) is None, "a path or tool outside the protected set was refused"


def _odd_events() -> list[dict]:
    tool = next(iter(op.DENIED_TOOLS))
    return [
        {},
        {"type": "tool_call"},
        {"type": "tool_call", "data": None},
        {"type": "tool_call", "data": "text"},
        {"type": "tool_call", "data": ["list"]},
        {"type": "tool_call", "data": {}},
        {"type": "tool_call", "data": {"name": None}},
        {"type": "tool_call", "data": {"name": 5}},
        {"type": "tool_call", "data": {"name": ["x"]}},
        {"type": "tool_call", "data": {"name": "Write"}},
        {"type": "tool_call", "data": {"name": "Write", "arguments": None}},
        {"type": "tool_call", "data": {"name": "Write", "arguments": "text"}},
        {"type": "tool_call", "data": {"name": "Write", "arguments": ["list"]}},
        {"type": "tool_call", "data": {"name": "Write", "arguments": {}}},
        {"type": "tool_call", "data": {"name": "Write", "arguments": {"file_path": None}}},
        {"type": "tool_call", "data": {"name": "Write", "arguments": {"file_path": 5}}},
        {"type": "tool_call", "data": {"name": "Read", "arguments": "text"}},
        {"type": "request", "data": "text"},
        {"type": "request", "data": {"user_content": "text", "attachments": []}},
        {"type": "request", "data": None},
        {"type": "response", "data": "text"},
        {"type": "response", "data": {"name": tool}},
        {"type": 5, "data": {"name": tool}},
    ]


def test_no_event_shape_raises_an_evaluation_error(omnigent_py: str, tmp_path: Path) -> None:
    """An evaluation error abstains, which would open the gate silently - and here it also once hung the run."""
    results = _evaluate(omnigent_py, tmp_path, _odd_events())
    assert len(results) == len(_odd_events())
    for event, entry in zip(_odd_events(), results, strict=True):
        for policy in POLICIES:
            assert entry[policy]["error"] is None, f"{policy} raised on {event}: {entry[policy]['error']}"
            assert entry[policy]["result"] is None, f"{policy} refused {event}"


# ---------------------------------------------------------------------------
# Criterion 6 - the installer merges safely
# ---------------------------------------------------------------------------


def _config(tmp_path: Path, text: str | None) -> Path:
    path = tmp_path / "cfg" / "config.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    if text is not None:
        path.write_text(text, encoding="utf-8")
    return path


def _backups(path: Path) -> list[Path]:
    return sorted(path.parent.glob(path.name + ".bak-*"))


FOREIGN = """\
host: 127.0.0.1
telemetry:
  enabled: false
policies:
  admin__audit:
    type: function
    function: myorg.policies.audit
"""


def test_merge_keeps_foreign_keys_and_policies(tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN)
    assert op.merge_config(path, validate=False) == "merged"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["host"] == "127.0.0.1" and data["telemetry"] == {"enabled": False}
    assert data["policies"]["admin__audit"] == {"type": "function", "function": "myorg.policies.audit"}
    assert {k for k in data["policies"] if k.startswith(op.OWNED_PREFIX)} == set(POLICIES)


def test_merge_creates_a_missing_config_without_a_backup(tmp_path: Path) -> None:
    path = tmp_path / "not-yet" / "config.yaml"
    assert op.merge_config(path, validate=False) == "created"
    assert set(yaml.safe_load(path.read_text(encoding="utf-8"))["policies"]) == set(POLICIES)
    assert _backups(path) == []


def test_merge_replaces_owned_policies_as_a_set(tmp_path: Path) -> None:
    stale = {
        "type": "function",
        "handler": op.CEL_HANDLER,
        "factory_params": {"expression": "null", "reason": "old"},
    }
    text = yaml.safe_dump(
        {"policies": {op.OWNED_PREFIX + "gone": stale, op.WRITING_POLICY: stale, "admin__keep": stale}}, sort_keys=False
    )
    path = _config(tmp_path, text)
    op.merge_config(path, validate=False)
    policies = yaml.safe_load(path.read_text(encoding="utf-8"))["policies"]
    assert list(policies).count(op.WRITING_POLICY) == 1
    assert op.OWNED_PREFIX + "gone" not in policies, "a stale owned policy was kept"
    assert policies[op.WRITING_POLICY] == op._file_policies()[op.WRITING_POLICY], "the owned policy was not replaced"
    assert "admin__keep" in policies


def test_merge_backs_up_before_a_change_and_not_on_a_rerun(tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN)
    assert op.merge_config(path, validate=False) == "merged"
    backups = _backups(path)
    assert len(backups) == 1 and backups[0].read_text(encoding="utf-8") == FOREIGN

    before = path.read_bytes()
    assert op.merge_config(path, validate=False) == "unchanged"
    assert path.read_bytes() == before
    assert _backups(path) == backups, "a rerun that changed nothing made a backup"


def test_remove_takes_out_only_owned_policies(tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN)
    op.merge_config(path, validate=False)
    assert op.merge_config(path, remove=True, validate=False) == "removed"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert list(data["policies"]) == ["admin__audit"], "a foreign policy was removed"
    assert data["host"] == "127.0.0.1"

    before, backups = path.read_bytes(), _backups(path)
    assert op.merge_config(path, remove=True, validate=False) == "unchanged"
    assert path.read_bytes() == before and _backups(path) == backups


def test_remove_works_on_a_config_with_a_broken_foreign_policy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Removal deletes only owned policies and validates nothing: a foreign policy Omnigent rejects must not block it."""

    def reject(_policies: dict) -> None:
        raise ValueError("Omnigent would reject a foreign policy")

    path = _config(tmp_path, FOREIGN + "  admin__broken:\n    type: no-such-type\n")
    op.merge_config(path, validate=False)
    monkeypatch.setattr(op, "_validate", reject)
    with pytest.raises(ValueError):  # the install path still validates, so a broken config is not written to
        op.merge_config(path, {**op.owned_policies(), op.OWNED_PREFIX + "x": {}}, validate=True)
    assert op.merge_config(path, remove=True) == "removed"
    assert list(yaml.safe_load(path.read_text(encoding="utf-8"))["policies"]) == ["admin__audit", "admin__broken"]


def test_remove_drops_an_emptied_policies_key(tmp_path: Path) -> None:
    path = _config(tmp_path, "host: x\n")
    op.merge_config(path, validate=False)
    op.merge_config(path, remove=True, validate=False)
    assert yaml.safe_load(path.read_text(encoding="utf-8")) == {"host": "x"}


def test_merge_refuses_a_config_it_cannot_read_as_a_mapping(tmp_path: Path) -> None:
    for text in ("- a\n- b\n", "policies:\n  - not-a-mapping\n", "just text\n"):
        path = _config(tmp_path, text)
        with pytest.raises(op.ConfigError):
            op.merge_config(path, validate=False)
        assert path.read_text(encoding="utf-8") == text and _backups(path) == []


def test_installed_check_tells_match_from_drift(tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN)
    assert op.installed_differences(path), "a config without the policies counts as a match"
    op.merge_config(path, validate=False)
    assert op.installed_differences(path) == []

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["policies"][op.WRITING_POLICY]["factory_params"]["expression"] = "null"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    assert any("differs" in d for d in op.installed_differences(path)), "a tampered policy passed"

    data["policies"][op.OWNED_PREFIX + "stale"] = data["policies"][op.PATHS_POLICY]
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    assert any("stale" in d for d in op.installed_differences(path))
    assert op.installed_differences(tmp_path / "nope.yaml"), "a missing config counts as a match"


def test_installed_check_exit_codes(tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN)
    args = [sys.executable, str(SCRIPT), "--installed", str(path)]
    assert subprocess.run(args, capture_output=True, check=False).returncode == 1
    op.merge_config(path, validate=False)
    assert subprocess.run(args, capture_output=True, check=False).returncode == 0


def test_merge_writes_nothing_omnigent_rejects(omnigent_py: str, tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN)
    before = path.read_bytes()
    probe = f"""
import sys
sys.path.insert(0, {str(REPO / "scripts")!r})
import omnigent_policy as op
from pathlib import Path
path = Path({str(path)!r})
good = op.owned_policies()
bad_syntax = {{**good, "coding_harness__bad": {{"type": "function", "handler": op.CEL_HANDLER,
    "factory_params": {{"expression": "(((", "reason": "x"}}}}}}
bad_foreign = {{**good, "admin__bad": {{"type": "no-such-type"}}}}
for label, policies in (("syntax", bad_syntax), ("foreign", bad_foreign)):
    try:
        op.merge_config(path, policies)
    except Exception as exc:
        print(label, "rejected", type(exc).__name__)
    else:
        print(label, "ACCEPTED")
"""
    done = subprocess.run(
        [omnigent_py, "-c", probe], capture_output=True, text=True, timeout=120, env=_env(tmp_path), check=False
    )
    assert done.returncode == 0, done.stderr
    assert "ACCEPTED" not in done.stdout and done.stdout.count(" rejected ") == 2, done.stdout
    assert path.read_bytes() == before, "a rejected merge changed the file"
    assert _backups(path) == [], "a rejected merge left a backup"


def test_the_cli_merges_and_says_what_to_do_next(omnigent_py: str, tmp_path: Path) -> None:
    path = tmp_path / "cfg" / "config.yaml"
    first = _run(omnigent_py, ["--merge-config", str(path)], tmp_path)
    assert first.returncode == 0, first.stderr
    assert first.stdout.startswith("created:") and "omnigent server stop" in first.stdout
    second = _run(omnigent_py, ["--merge-config", str(path)], tmp_path)
    assert second.returncode == 0 and second.stdout.startswith("unchanged:") and "no restart needed" in second.stdout
    assert "omnigent server stop" not in second.stdout
    removed = _run(omnigent_py, ["--merge-config", str(path), "--remove"], tmp_path)
    assert (
        removed.returncode == 0 and removed.stdout.startswith("removed:") and "omnigent server stop" in removed.stdout
    )


def test_the_cli_removes_from_a_config_omnigent_would_reject(omnigent_py: str, tmp_path: Path) -> None:
    path = _config(tmp_path, FOREIGN + "  admin__broken:\n    type: no-such-type\n")
    op.merge_config(path, validate=False)
    kept = {
        k: v for k, v in yaml.safe_load(path.read_text(encoding="utf-8"))["policies"].items() if k.startswith("admin__")
    }
    removed = _run(omnigent_py, ["--merge-config", str(path), "--remove"], tmp_path)
    assert removed.returncode == 0 and removed.stdout.startswith("removed:"), removed.stderr
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["policies"] == kept


def test_installer_refuses_without_a_terminal(tmp_path: Path) -> None:
    env = _env(tmp_path)
    for args in ([], ["--remove"]):
        done = subprocess.run(
            ["/bin/bash", str(INSTALLER), *args],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
            check=False,
        )
        assert done.returncode == 2, (args, done.stdout, done.stderr)
        assert "terminal" in done.stderr
    assert not (tmp_path / "home").exists() and not (tmp_path / "omnigent-config").exists(), (
        "the refusal wrote something"
    )


def test_installer_check_needs_no_terminal_but_needs_omnigent(tmp_path: Path) -> None:
    env = _env(tmp_path)
    env["PATH"] = "/usr/bin:/bin"
    env.pop("OMNIGENT_PYTHON", None)
    done = subprocess.run(
        ["/bin/bash", str(INSTALLER), "--check"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )
    assert done.returncode == 2 and "Omnigent not found" in done.stderr

    env["OMNIGENT_PYTHON"] = sys.executable  # PyYAML is enough for --installed
    done = subprocess.run(
        ["/bin/bash", str(INSTALLER), "--check"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )
    assert done.returncode == 1 and "does not exist" in done.stdout


def test_installer_runs_end_to_end_in_a_temporary_home(omnigent_py: str, tmp_path: Path) -> None:
    """With a pseudo-terminal on stdin, against a temporary config path - never the real ~/.omnigent."""
    env = _env(tmp_path)
    env["OMNIGENT_PYTHON"] = omnigent_py
    target = Path(env["OMNIGENT_CONFIG_HOME"]) / "config.yaml"
    assert str(tmp_path) in str(target)

    def run(*args: str, terminal: bool) -> int:
        master = slave = None
        if terminal:
            master, slave = pty.openpty()
        try:
            return subprocess.run(
                ["/bin/bash", str(INSTALLER), *args],
                stdin=slave if terminal else subprocess.DEVNULL,
                capture_output=True,
                env=env,
                timeout=120,
                check=False,
            ).returncode
        finally:
            for fd in (master, slave):
                if fd is not None:
                    os.close(fd)

    assert run("--check", terminal=False) == 1
    assert run(terminal=True) == 0
    assert run("--check", terminal=False) == 0
    assert run(terminal=True) == 0 and _backups(target) == [], "a rerun changed or backed up the config"
    assert run("--remove", terminal=True) == 0
    assert run("--check", terminal=False) == 1


def _fake_python(directory: Path, name: str = "python3") -> Path:
    """An executable that runs this test's interpreter (so PyYAML is there), under a name and directory of choice."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    path.chmod(0o755)
    return path


def test_launcher_forms_resolve_to_the_interpreter(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    direct = _fake_python(tmp_path / "plain", "python")
    spaced = _fake_python(tmp_path / "a dir with spaces", "python")
    bin_dir = tmp_path / "bin"
    on_path = _fake_python(bin_dir)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    resolve = op._launcher_interpreter
    assert resolve(f"#!{direct}") == str(direct)
    assert resolve("#!/usr/bin/env python3") == str(on_path)
    assert resolve("#!/usr/bin/env no-such-interpreter-anywhere") is None
    assert resolve("#!/bin/sh", f'\'\'\'exec\' "{spaced}" "$0" "$@"') == str(spaced)
    assert resolve(f"#!{tmp_path}/not/there") is None
    assert resolve("echo not a launcher") is None
    assert resolve("#!") is None


def test_installer_and_module_resolve_omnigent_alike(tmp_path: Path) -> None:
    """The launcher names its interpreter as `env python3` - a form the installer once rejected."""
    bin_dir = tmp_path / "bin"
    _fake_python(bin_dir)
    launcher = bin_dir / "omnigent"
    launcher.write_text("#!/usr/bin/env python3\nprint('not run')\n", encoding="utf-8")
    launcher.chmod(0o755)
    env = _env(tmp_path)
    env["PATH"] = f"{bin_dir}:/usr/bin:/bin"
    env.pop("OMNIGENT_PYTHON", None)

    named = subprocess.run(
        [str(bin_dir / "python3"), str(SCRIPT), "--print-python"], capture_output=True, text=True, env=env, check=False
    )
    assert named.returncode == 0 and named.stdout.strip() == str(bin_dir / "python3"), named.stderr
    done = subprocess.run(
        ["/bin/bash", str(INSTALLER), "--check"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )
    assert "Omnigent not found" not in done.stderr, "the installer did not resolve what the module resolves"
    assert done.returncode == 1 and "does not exist" in done.stdout, (done.stdout, done.stderr)


def test_omnigent_python_prefers_the_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OMNIGENT_PYTHON", sys.executable)
    assert op.omnigent_python() == sys.executable
    monkeypatch.setenv("OMNIGENT_PYTHON", "/no/such/python")
    assert op.omnigent_python() is None
