"""One harness-neutral permission check, its host adapters, launchers and generated configuration.

The subject is `scripts/agent_policy.py` (the shared check and the renderer), `scripts/agent_policy_hooks.py`
(the Claude Code and Antigravity adapters), `tools/claude-code/night.py` and `tools/antigravity/night.py`
(plans/changes/agent-policy-list). The expected rule lists below are typed here, not read from the sources,
so a rule dropped from any source still fails. Every rendering runs in a temporary root; nothing here
touches the held `.claude/settings.json`, `.agents/hooks.json` or any user setting.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import agent_policy as ap  # noqa: E402
import agent_policy_hooks as hooks  # noqa: E402
import merge_guard as mg  # noqa: E402
import omnigent_policy as op  # noqa: E402

SETTINGS = REPO / ".claude" / "settings.json"
HOOKS_SCRIPT = REPO / "scripts" / "agent_policy_hooks.py"
CLAUDE_NIGHT = REPO / "tools" / "claude-code" / "night.py"
ANTIGRAVITY_NIGHT = REPO / "tools" / "antigravity" / "night.py"
NIGHT_FRAGMENT = REPO / "tools" / "claude-code" / "night-settings.json"

ASK, DENY, ABSTAIN = "ask", "deny", "abstain"


def _module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


night_cc = _module("agent_policy_test_claude_night", CLAUDE_NIGHT)
night_agy = _module("agent_policy_test_antigravity_night", ANTIGRAVITY_NIGHT)

# The Claude Code rules at commit 937cdec8, typed here.
BASELINE_ASK = [
    "Bash(gh pr merge *)",
    "Bash(gh -* pr merge*)",
    "Bash(gh pr -* merge *)",
    "Bash(gh api *PUT*pulls/*/merge*)",
    "Bash(gh api *pulls/*/merge*PUT*)",
    "Bash(gh api *query=*mergePullRequest*)",
    "Bash(gh api *query=*enablePullRequestAutoMerge*)",
    "Bash(gh api *query=*enqueuePullRequest*)",
    "Bash(gh alias set *)",
    "Bash(git push *main*)",
    "mcp__*__merge_pull_request",
    "Bash(codex *)",
    "mcp__omnigent__sys_advise_models",
]
BASELINE_DENY = [
    "mcp__omnigent__sys_os_write",
    "mcp__omnigent__sys_os_edit",
    "mcp__omnigent__sys_os_shell",
    "mcp__omnigent__sys_agent_download",
    "mcp__omnigent__sys_terminal_launch",
    "mcp__omnigent__sys_terminal_send",
    "mcp__omnigent__sys_terminal_close",
    "mcp__omnigent__sys_session_create",
    "mcp__omnigent__sys_session_send",
    "mcp__omnigent__sys_session_message",
    "mcp__omnigent__sys_session_close",
    "mcp__omnigent__sys_session_rename",
    "mcp__omnigent__sys_session_share",
    "mcp__omnigent__sys_scheduled_task_create",
    "mcp__omnigent__sys_scheduled_task_update",
    "mcp__omnigent__sys_scheduled_task_delete",
    "mcp__omnigent__sys_call_async",
    "mcp__omnigent__sys_cancel_async",
    "mcp__omnigent__sys_cancel_task",
    "mcp__omnigent__sys_read_inbox",
    "mcp__omnigent__sys_add_policy",
    "mcp__omnigent__ui_open_file",
    "mcp__omnigent__update_comment",
    "mcp__omnigent__browser_navigate",
    "mcp__omnigent__browser_click",
    "mcp__omnigent__browser_type",
    "mcp__omnigent__hindsight_retain",
    "mcp__omnigent__hindsight_recall",
    "mcp__omnigent__hindsight_reflect",
    "Edit(//**/.omnigent/config.yaml)",
]
# The maintainer mode of the enqueue script (decisions.md, details of 2026-11-25).
ENQUEUE_ASK = [
    "Bash(python3 scripts/enqueue_pr.py * --maintainer*)",
    "Bash(.venv/bin/python scripts/enqueue_pr.py * --maintainer*)",
]


# ---------------------------------------------------------------------------
# Helpers: the adapters' answers, read back in each host's form
# ---------------------------------------------------------------------------


def bash(command: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": command}}


def run_command(command: str) -> dict:
    return {"tool_name": "run_command", "tool_input": {"command": command}}


def tool(name: str) -> dict:
    return {"tool_name": name, "tool_input": {}}


def _text(payload: dict | str) -> str:
    return payload if isinstance(payload, str) else json.dumps(payload)


def claude(payload: dict | str, env: dict[str, str] | None = None) -> tuple[str, str]:
    """(decision, reason) as Claude Code reads the adapter's answer."""
    code, out, err = hooks.run("claude-code", _text(payload), env or {})
    if code == 2:
        return DENY, err
    assert code == 0, (code, out, err)
    if not out:
        assert not err
        return ABSTAIN, ""
    body = json.loads(out)["hookSpecificOutput"]
    assert body["hookEventName"] == "PreToolUse"
    return body["permissionDecision"], body["permissionDecisionReason"]


def antigravity(payload: dict | str, env: dict[str, str] | None = None) -> tuple[str, str]:
    """(decision, reason) as the Antigravity adapter answers: exit 0 and silence, or a deny with exit 2."""
    code, out, err = hooks.run("antigravity", _text(payload), env or {})
    if code == 0 and not out:
        assert not err
        return ABSTAIN, ""
    body = json.loads(out)
    assert code == (2 if body["decision"] == DENY else 0), (code, out, err)
    assert err.strip() == (body["reason"] if code == 2 else "")
    return body["decision"], body["reason"]


def _without_signal() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key != "HARNESS_UNATTENDED"}


def _hook_process(host: str, payload: dict, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOKS_SCRIPT), host],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )


def _fresh_root(root: Path) -> Path:
    """A temporary root holding a copy of the held settings, rendered by the policy."""
    target = root / ".claude" / "settings.json"
    target.parent.mkdir(parents=True)
    target.write_text(SETTINGS.read_text(encoding="utf-8"), encoding="utf-8")
    ap.write(root)
    return root


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Criterion 1 - the rule sources
# ---------------------------------------------------------------------------


def test_rule_sources_preserve_permissions(monkeypatch: pytest.MonkeyPatch) -> None:
    listed = ap.permissions()
    for kind in (ASK, DENY):
        assert len(listed[kind]) == len(set(listed[kind])), f"a {kind} rule is listed twice"
    assert sorted(listed[ASK]) == sorted(BASELINE_ASK + ENQUEUE_ASK)
    assert sorted(listed[DENY]) == sorted(BASELINE_DENY)
    assert not set(listed[ASK]) & set(listed[DENY]), "a rule is both ask and deny"

    by_pattern = {rule.pattern: rule for rule in ap.rules()}
    for pattern in mg.MERGE_ASK_RULES:
        assert (by_pattern[pattern].decision, by_pattern[pattern].source) == (ASK, ap.MERGE_SOURCE)
    for pattern in op.layer1_ask_rules():
        assert (by_pattern[pattern].decision, by_pattern[pattern].source) == (ASK, ap.OMNIGENT_SOURCE)
    for pattern in op.layer1_rules():
        assert (by_pattern[pattern].decision, by_pattern[pattern].source) == (DENY, ap.OMNIGENT_SOURCE)
    for pattern in ["Bash(codex *)", *ENQUEUE_ASK]:
        assert (by_pattern[pattern].decision, by_pattern[pattern].source) == (ASK, ap.OWN_SOURCE)
    for rule in by_pattern.values():
        assert len(rule.reason.strip()) >= 10, f"{rule.pattern} has no reason"

    assert ap.decide_shell("python3 scripts/enqueue_pr.py 54 --maintainer").kind == ASK
    assert ap.decide_shell(".venv/bin/python scripts/enqueue_pr.py 54 --maintainer").kind == ASK
    assert ap.decide_shell("python3 scripts/enqueue_pr.py 54").kind == ABSTAIN, "the default call is allowed"

    # Planted faults: a rule with a second home is refused, a rule dropped from its source is missed.
    with monkeypatch.context() as planted:
        planted.setitem(ap.OWN_ASK_RULES, "Bash(gh pr merge *)", "a second home for a merge rule")
        with pytest.raises(ValueError, match="twice"):
            ap.rules()
    with monkeypatch.context() as planted:
        planted.delitem(op.DENIED_TOOLS, "sys_os_shell")
        assert sorted(ap.permissions()[DENY]) != sorted(BASELINE_DENY)


# ---------------------------------------------------------------------------
# Criterion 2 - rendering keeps unrelated settings
# ---------------------------------------------------------------------------


def test_render_preserves_unrelated_settings(tmp_path: Path) -> None:
    held = _read(SETTINGS)
    foreign_pre = {"matcher": "Write", "hooks": [{"type": "command", "command": "echo foreign"}]}
    foreign_post = {"matcher": "", "hooks": [{"type": "command", "command": "echo after"}]}
    settings = json.loads(json.dumps(held))
    settings["statusLine"] = {"type": "command", "command": "echo status"}
    settings["model"] = "sonnet"
    settings["permissions"]["allow"] = ["Bash(ls *)"]
    settings["permissions"]["defaultMode"] = "default"
    settings.setdefault("hooks", {})["PreToolUse"] = [foreign_pre]
    settings["hooks"]["PostToolUse"] = [foreign_post]
    before = json.loads(json.dumps(settings))

    rendered = ap.render_settings(settings)
    assert settings == before, "the renderer changed its input"
    assert {k: v for k, v in rendered.items() if k not in ("hooks", "permissions")} == {
        k: v for k, v in before.items() if k not in ("hooks", "permissions")
    }
    assert rendered["hooks"]["SessionStart"] == held["hooks"]["SessionStart"], "the SessionStart hook changed"
    assert rendered["hooks"]["PostToolUse"] == [foreign_post]
    assert rendered["hooks"]["PreToolUse"] == [foreign_pre, ap.registration("claude-code")]
    assert rendered["permissions"]["allow"] == ["Bash(ls *)"]
    assert rendered["permissions"]["defaultMode"] == "default"
    assert ap.render_settings(rendered) == rendered, "a second render changed the first"

    agents = {"hooks": {"PostToolUse": [foreign_post], "PreToolUse": [foreign_pre]}, "other": 1}
    rendered_agents = ap.render_agents_hooks(agents)
    assert rendered_agents["other"] == 1
    assert rendered_agents["hooks"]["PostToolUse"] == [foreign_post]
    assert rendered_agents["hooks"]["PreToolUse"] == [foreign_pre, ap.registration("antigravity")]

    root = _fresh_root(tmp_path / "root")
    on_disk = _read(root / ".claude" / "settings.json")
    assert on_disk["hooks"]["SessionStart"] == held["hooks"]["SessionStart"]
    assert {k: v for k, v in on_disk.items() if k not in ("hooks", "permissions")} == {
        k: v for k, v in held.items() if k not in ("hooks", "permissions")
    }


# ---------------------------------------------------------------------------
# Criteria 3, 4 - adapters agree with the shared check; MCP names
# ---------------------------------------------------------------------------

SHELL_SAMPLES = (
    "gh pr merge 54",
    "cd /repo && gh pr merge 54",
    "git push origin main",
    "codex exec x",
    'bash -c "gh pr merge 54"',
    "python3 scripts/enqueue_pr.py 54 --maintainer",
    'echo "a quote that never closes',
    "ls -la",
    "gh pr view 54 --json mergeable",
)
TOOL_SAMPLES = (
    "mcp__github__merge_pull_request",
    "github.merge_pull_request",
    "github_merge_pull_request",
    "mcp__omnigent__sys_os_write",
    "mcp__omnigent__sys_advise_models",
    "mcp__github__get_pull_request",
)


def _on_antigravity(kind: str) -> str:
    """Antigravity expresses the shared decision."""
    return kind


def test_adapters_match_shared_check(capsys: pytest.CaptureFixture[str]) -> None:
    seen: set[str] = set()
    for command in SHELL_SAMPLES:
        shared = ap.decide_shell(command).kind
        seen.add(shared)
        assert claude(bash(command))[0] == shared, f"Claude Code disagrees on {command!r}"
        assert antigravity(run_command(command))[0] == _on_antigravity(shared), f"Antigravity disagrees on {command!r}"
    for name in TOOL_SAMPLES:
        shared = ap.decide_tool(name).kind
        seen.add(shared)
        assert claude(tool(name))[0] == shared, f"Claude Code disagrees on {name!r}"
        assert antigravity(tool(name))[0] == _on_antigravity(shared), f"Antigravity disagrees on {name!r}"
    assert seen == {ASK, DENY, ABSTAIN}, "the samples must reach every decision"

    claude_matcher = ap.registration("claude-code")["matcher"]
    agy_matcher = ap.registration("antigravity")["matcher"]
    for name in ("Bash", "mcp__github__merge_pull_request", "github.merge_pull_request"):
        assert re.fullmatch(claude_matcher, name), f"the Claude Code registration does not reach {name}"
    for name in ("run_command", "github_merge_pull_request"):
        assert re.fullmatch(agy_matcher, name), f"the Antigravity registration does not reach {name}"
    assert not re.fullmatch(claude_matcher, "Read")

    env = _without_signal()
    done = _hook_process("claude-code", bash("gh pr merge 54"), env)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["hookSpecificOutput"]["permissionDecision"] == ASK
    done = _hook_process("antigravity", run_command("gh pr merge 54"), env)
    assert done.returncode == 0 and json.loads(done.stdout)["decision"] == ASK

    assert ap.main(["decide", "--shell", "cd /repo && gh pr merge 54"]) == 0
    assert json.loads(capsys.readouterr().out)["decision"] == ASK
    assert ap.main(["decide", "--tool", "github.merge_pull_request"]) == 0
    assert json.loads(capsys.readouterr().out)["decision"] == ASK


def test_mcp_merge_names_normalised() -> None:
    names = (
        "github.merge_pull_request",
        "github_merge_pull_request",
        "github/merge_pull_request",
        "github:merge_pull_request",
        "github-merge_pull_request",
        "mcp__github__merge_pull_request",
        "mcp__github_merge_pull_request",
        "merge_pull_request",
    )
    for name in names:
        normalised = ap.normalise_tool_name(name)
        assert re.fullmatch(r"mcp__[A-Za-z0-9_-]+__merge_pull_request", normalised), (name, normalised)
        decision = ap.decide_tool(name)
        assert decision.kind == ASK, f"{name} abstains"
        assert "mcp__*__merge_pull_request" in decision.message()
        assert claude(tool(name))[0] == ASK
        assert antigravity(tool(name))[0] == ASK
    for name in ("github.get_pull_request", "github.merge_pull_request_status", "mcp__github__list_pull_requests"):
        assert ap.normalise_tool_name(name) == name
        assert ap.decide_tool(name).kind == ABSTAIN, f"{name} is not a merge tool"
    # Without normalisation the existing rule does not reach these names: the adapter's step is the point.
    assert not mg.covers("mcp__*__merge_pull_request", "github.merge_pull_request")
    assert not mg.covers("mcp__*__merge_pull_request", "github_merge_pull_request")


# ---------------------------------------------------------------------------
# Criteria 5-7 - compound lines, quotes, shell -c
# ---------------------------------------------------------------------------


def test_compound_parts_use_strongest_decision(monkeypatch: pytest.MonkeyPatch) -> None:
    for command in (
        "cd /repo && gh pr merge 54",
        "git add . && git push origin main",
        "git status; gh pr merge 54",
        "false || gh pr merge 54",
        "echo y | gh pr merge 54",
        "ls |& gh pr merge 54",
        "cd /repo\ngh pr merge 54",
        "sleep 1 & gh pr merge 54",
    ):
        assert ap.decide_shell(command).kind == ASK, f"{command!r} hides a merge"
    assert ap.split_command("cd /repo && gh pr merge 54") == ["cd /repo", "gh pr merge 54"]
    assert ap.split_command("gh pr view 54 2>&1 | cat") == ["gh pr view 54 2>&1", "cat"]
    assert ap.split_command("ls &>/dev/null") == ["ls &>/dev/null"]
    assert ap.decide_shell("gh pr view 54 2>&1 | cat").kind == ABSTAIN

    deny, ask = ap.Decision(DENY, ("d",)), ap.Decision(ASK, ("a",))
    assert ap.combine([ask, deny, ap.Decision(ABSTAIN)]) == deny
    assert ap.combine([ap.Decision(ABSTAIN), ask]) == ask
    assert ap.combine([]).kind == ABSTAIN

    monkeypatch.setitem(ap.OWN_DENY_RULES, "Bash(rm -rf /*)", "a deny planted for this test")
    for command in ("gh pr merge 54 && rm -rf /tmp/x", "rm -rf /tmp/x; gh pr merge 54", "ls | rm -rf /tmp/x"):
        decision = ap.decide_shell(command)
        assert decision.kind == DENY, f"the deny in {command!r} was weakened"
        assert "Bash(rm -rf /*)" in decision.message()


def test_quoted_operators_do_not_split() -> None:
    for command in (
        'git commit -m "docs; git push origin main later"',
        "echo 'a && gh pr merge 54'",
        'echo "x | gh pr merge 54"',
        'echo "a \\" ; gh pr merge 54"',
        "ls # don't git push origin main",
        "cat > n.md <<'EOF'\nIt's done; git push origin main\nEOF",
        "cat <<-EOF\n\tgh pr merge 54\n\tEOF",
    ):
        assert ap.decide_shell(command).kind == ABSTAIN, f"quoted or non-command text in {command!r} was checked"
    assert ap.split_command('git commit -m "docs; git push origin main later"') == [
        'git commit -m "docs; git push origin main later"'
    ]
    # What follows a heredoc or a comment is command text again.
    assert ap.decide_shell("cat > n.md <<'EOF'\nIt's done\nEOF\ngh pr merge 54").kind == ASK
    assert ap.decide_shell("ls # note\ngh pr merge 54").kind == ASK
    # A quote that never closes cannot be split: it asks.
    with pytest.raises(ap.ShellSyntaxError):
        ap.split_command('echo "abc')
    unsplit = ap.decide_shell('echo "abc && gh pr merge 54')
    assert unsplit.kind == ASK and "never closes" in unsplit.message()
    # Counterpart: the same text without quotes does split.
    assert ap.decide_shell("git commit -m docs; git push origin main later").kind == ASK


def test_shell_c_command_is_checked(monkeypatch: pytest.MonkeyPatch) -> None:
    for command in (
        'bash -c "cd /repo && gh pr merge 54"',
        "sh -c 'gh pr merge 54'",
        'zsh -c "git push origin main"',
        'bash -lc "gh pr merge 54"',
        'sh -ec "gh pr merge 54"',
        'bash --norc -c "gh pr merge 54"',
        'bash -o pipefail -c "gh pr merge 54"',
        '/bin/zsh -c "git push origin main"',
        '/usr/bin/env bash -c "gh pr merge 54"',
        'env FOO=1 sh -c "gh pr merge 54"',
        "bash -c \"sh -c 'gh pr merge 54'\"",
        'cd /repo && bash -c "gh pr merge 54"',
    ):
        assert ap.decide_shell(command).kind == ASK, f"{command!r} hides a merge"
    assert ap.shell_c_command('bash -lc "gh pr merge 54"') == "gh pr merge 54"
    for command in (
        "bash script.sh",
        "bash -x script.sh",
        'bash -c "gh pr view 54"',
        'python3 -c "gh pr merge 54"',
        'fish -c "gh pr merge 54"',
    ):
        assert ap.decide_shell(command).kind == ABSTAIN, f"{command!r} was taken for a hidden merge"
    monkeypatch.setattr(ap, "MAX_NESTING", 2)
    nested = "true"
    for _ in range(ap.MAX_NESTING + 2):
        nested = f"bash -c {shlex.quote(nested)}"
    deep = ap.decide_shell(nested)
    assert deep.kind == ASK and "nesting" in deep.message()


# ---------------------------------------------------------------------------
# Criteria 8-11 - the unattended signal and its launchers
# ---------------------------------------------------------------------------


def test_unattended_asks_are_denied() -> None:
    for value in ("1", "true", "yes", "2"):
        env = {"HARNESS_UNATTENDED": value}
        assert hooks.is_unattended(env)
        decision, reason = claude(bash("gh pr merge 54"), env)
        assert decision == DENY and "unattended" in reason, f"an ask stayed an ask for {value!r}"
        assert claude(tool("github.merge_pull_request"), env)[0] == DENY
        assert antigravity(run_command("gh pr merge 54"), env)[0] == DENY
        assert claude(tool("mcp__omnigent__sys_os_write"), env)[0] == DENY
        assert claude(bash("ls -la"), env)[0] == ABSTAIN


def test_attended_environment() -> None:
    for env in ({}, {"HARNESS_UNATTENDED": ""}, {"HARNESS_UNATTENDED": "0"}):
        assert not hooks.is_unattended(env), env
        assert claude(bash("gh pr merge 54"), env)[0] == ASK, f"{env} alone turned an ask into a deny"
        assert claude(bash("ls -la"), env)[0] == ABSTAIN
    # The hook process reads its own environment.
    for value, expected in (("0", ASK), ("", ASK), ("1", DENY)):
        env = {**_without_signal(), "HARNESS_UNATTENDED": value}
        done = _hook_process("claude-code", bash("gh pr merge 54"), env)
        assert done.returncode == 0, done.stderr
        assert json.loads(done.stdout)["hookSpecificOutput"]["permissionDecision"] == expected, value


FAKE_CHILD = """\
import os
import sys
from pathlib import Path

record = Path(os.environ["AGENT_POLICY_RECORD"])
record.write_text(os.environ.get("HARNESS_UNATTENDED", "<unset>") + "\\n" + "\\n".join(sys.argv[1:]), encoding="utf-8")
sys.exit(int(os.environ.get("AGENT_POLICY_EXIT", "0")))
"""


def _fake(bin_dir: Path, name: str) -> Path:
    bin_dir.mkdir(parents=True, exist_ok=True)
    fake = bin_dir / name
    fake.write_text(f"#!{sys.executable}\n{FAKE_CHILD}", encoding="utf-8")
    fake.chmod(0o755)
    return fake


def test_claude_night_child_environment(tmp_path: Path) -> None:
    home, project, record = tmp_path / "home", tmp_path / "project", tmp_path / "record"
    home.mkdir()
    project.mkdir()
    fake = _fake(tmp_path / "bin", "claude")
    env = _without_signal()
    env.update(
        HOME=str(home),
        CLAUDE_CONFIG_DIR=str(home / ".claude"),
        PATH=f"{fake.parent}{os.pathsep}{env.get('PATH', '')}",
        AGENT_POLICY_RECORD=str(record),
    )
    # The probe itself reports a missing signal.
    subprocess.run([str(fake)], env=env, timeout=60, check=True)
    assert record.read_text(encoding="utf-8").splitlines()[0] == "<unset>"

    done = subprocess.run(
        [sys.executable, str(CLAUDE_NIGHT), "-p", "night check"],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    assert record.read_text(encoding="utf-8").splitlines()[0] == "1", "the night child lacks HARNESS_UNATTENDED=1"
    assert night_cc.child_environment({"A": "b", "HARNESS_UNATTENDED": "0"}) == {"A": "b", "HARNESS_UNATTENDED": "1"}


def test_antigravity_night_child_environment(tmp_path: Path) -> None:
    record = tmp_path / "record"
    fake = _fake(tmp_path / "bin", "agy")
    env = _without_signal()
    env.update(PATH=f"{fake.parent}{os.pathsep}{env.get('PATH', '')}", AGENT_POLICY_RECORD=str(record))
    env["AGENT_POLICY_EXIT"] = "5"
    done = subprocess.run(
        [sys.executable, str(ANTIGRAVITY_NIGHT), "--flag", "value"],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 5, done.stderr
    lines = record.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "1", "the Antigravity child lacks HARNESS_UNATTENDED=1"
    assert lines[1:] == ["--flag", "value"]
    assert night_agy.child_environment({"HARNESS_UNATTENDED": ""}) == {"HARNESS_UNATTENDED": "1"}

    empty = tmp_path / "empty"
    empty.mkdir()
    missing = subprocess.run(
        [sys.executable, str(ANTIGRAVITY_NIGHT)],
        env={**env, "PATH": str(empty)},
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert missing.returncode == 127 and "agy" in missing.stderr


# ---------------------------------------------------------------------------
# Criterion 12 - unmatched input abstains
# ---------------------------------------------------------------------------


def test_unmatched_input_abstains() -> None:
    for command in (
        "ls -la",
        "git status",
        "gh pr view 54 --json mergedAt,mergeable",
        "git push origin feat/x",
        "python3 scripts/enqueue_pr.py 54",
        "gh api repos/o/r/pulls/54/merge",
    ):
        assert ap.decide_shell(command).kind == ABSTAIN, command
        assert hooks.run("claude-code", json.dumps(bash(command)), {}) == (0, "", "")
        assert hooks.run("antigravity", json.dumps(run_command(command)), {}) == (0, "", "")
    for name in ("Read", "mcp__github__get_pull_request", "view_file"):
        assert ap.decide_tool(name).kind == ABSTAIN, name
        assert hooks.run("claude-code", json.dumps(tool(name)), {}) == (0, "", "")
        assert hooks.run("antigravity", json.dumps(tool(name)), {}) == (0, "", "")
    # Counterpart: a covered command beside them does not abstain.
    assert claude(bash("git push origin main"))[0] == ASK


# ---------------------------------------------------------------------------
# Criteria 13, 14 - drift, layer two and the night overlay
# ---------------------------------------------------------------------------


def _ours(config: dict) -> dict:
    """The policy's PreToolUse group in a rendered configuration."""
    return next(g for g in config["hooks"]["PreToolUse"] if ap.HOOK_SCRIPT in g["hooks"][0]["command"])


def _drop_codex(settings: dict, _agents: dict) -> None:
    settings["permissions"]["ask"].remove("Bash(codex *)")


def _drop_enqueue(settings: dict, _agents: dict) -> None:
    settings["permissions"]["ask"].remove(ENQUEUE_ASK[0])


def _add_extra(settings: dict, _agents: dict) -> None:
    settings["permissions"]["ask"].append("Bash(rm *)")


def _duplicate(settings: dict, _agents: dict) -> None:
    settings["permissions"]["ask"].append("Bash(gh alias set *)")


def _reclassify(settings: dict, _agents: dict) -> None:
    settings["permissions"]["ask"].remove("Bash(git push *main*)")
    settings["permissions"]["deny"].append("Bash(git push *main*)")


def _reorder(settings: dict, _agents: dict) -> None:
    settings["permissions"]["ask"].reverse()


def _claude_command(settings: dict, _agents: dict) -> None:
    _ours(settings)["hooks"][0]["command"] = 'python3 "$CLAUDE_PROJECT_DIR/scripts/agent_policy_hooks.py" antigravity'


def _claude_matcher(settings: dict, _agents: dict) -> None:
    _ours(settings)["matcher"] = "Bash"


def _claude_timeout(settings: dict, _agents: dict) -> None:
    _ours(settings)["hooks"][0]["timeout"] = 600


def _claude_missing(settings: dict, _agents: dict) -> None:
    settings["hooks"].pop("PreToolUse")


def _agents_command(_settings: dict, agents: dict) -> None:
    _ours(agents)["hooks"][0]["command"] = "python3 scripts/agent_policy_hooks.py claude-code"


def _agents_matcher(_settings: dict, agents: dict) -> None:
    _ours(agents)["matcher"] = "run_command"


def _agents_timeout(_settings: dict, agents: dict) -> None:
    _ours(agents)["hooks"][0]["timeout"] = 1


DRIFT_MUTATIONS = (
    (_drop_codex, "lacks the ask rule Bash(codex *)"),
    (_drop_enqueue, "lacks the ask rule"),
    (_add_extra, "does not list"),
    (_duplicate, "2 times"),
    (_reclassify, "the policy lists it as ask"),
    (_reorder, "order"),
    (_claude_command, "registrations"),
    (_claude_matcher, "matcher"),
    (_claude_timeout, "timeout"),
    (_claude_missing, "registrations"),
    (_agents_command, "registrations"),
    (_agents_matcher, "matcher"),
    (_agents_timeout, "timeout"),
)


def test_generated_configuration_drift_fails(tmp_path: Path) -> None:
    root = _fresh_root(tmp_path / "clean")
    assert ap.check(root) == []
    assert ap.main(["--root", str(root), "check"]) == 0
    assert ap.main(["--root", str(root), "write"]) == 0
    assert ap.check(root) == [], "a second write changed the first"

    for mutate, expected in DRIFT_MUTATIONS:
        name = mutate.__name__.strip("_")
        case = _fresh_root(tmp_path / name)
        settings_file, agents_file = case / ".claude" / "settings.json", case / ".agents" / "hooks.json"
        settings, agents = _read(settings_file), _read(agents_file)
        mutate(settings, agents)
        _write(settings_file, settings)
        _write(agents_file, agents)
        problems = ap.check(case)
        assert any(expected in problem for problem in problems), f"{name} passed the drift check: {problems}"
        assert ap.main(["--root", str(case), "check"]) == 1

    missing = _fresh_root(tmp_path / "agents-missing")
    (missing / ".agents" / "hooks.json").unlink()
    assert any(".agents/hooks.json" in problem for problem in ap.check(missing))


def test_layer_two_and_night_protection(tmp_path: Path) -> None:
    root = _fresh_root(tmp_path / "root")
    policy_file = root / "tools" / "omnigent" / "policy.yaml"
    assert policy_file.read_text(encoding="utf-8") == op.render_policy_yaml()

    policies = op.owned_policies()
    asked = policies[op.ASKED_POLICY]["factory_params"]["expression"]
    assert '"result": "ASK"' in asked and "sys_advise_models" in asked, "the layer-two ask was lost"
    writing = policies[op.WRITING_POLICY]["factory_params"]["expression"]
    assert '"result": "DENY"' in writing
    assert all(f'"{name}"' in writing for name in op.DENIED_TOOLS), "a layer-two deny was lost"
    assert '"result": "DENY"' in policies[op.PATHS_POLICY]["factory_params"]["expression"]

    rendered = _read(root / ".claude" / "settings.json")
    assert "mcp__omnigent__sys_advise_models" in rendered["permissions"]["ask"]
    fragment = json.loads(NIGHT_FRAGMENT.read_text(encoding="utf-8"))
    overlay = night_cc.build_overlay(fragment, [rendered])
    assert "ask" not in overlay["permissions"]
    assert overlay["permissions"]["defaultMode"] == "dontAsk"
    wanted = set(rendered["permissions"]["ask"]) | set(rendered["permissions"]["deny"])
    assert wanted <= set(overlay["permissions"]["deny"]), "the night overlay lost a conversion or a deny"

    # Planted fault: the layer-two ask turned into something else is caught.
    policy_file.write_text(
        op.render_policy_yaml().replace('"result": "ASK"', '"result": "ALLOW"'),
        encoding="utf-8",
    )
    assert any("policy.yaml" in problem for problem in ap.check(root))


# ---------------------------------------------------------------------------
# Criteria 15, 16 - faults and hosts without ask
# ---------------------------------------------------------------------------


def test_failures_deny_with_fault(monkeypatch: pytest.MonkeyPatch) -> None:
    malformed = (
        ("not json", "not JSON"),
        ("[]", "not a JSON object"),
        (json.dumps({"tool_input": {}}), "tool"),
        (json.dumps({"tool_name": "Bash", "tool_input": {}}), "command"),
        (json.dumps({"tool_name": "Bash", "tool_input": "gh pr merge 54"}), "tool_input"),
    )
    for text, cause in malformed:
        decision, reason = claude(text)
        assert decision == DENY and "fault" in reason and cause in reason, (text, reason)
    for text, cause in (
        ("not json", "not JSON"),
        (json.dumps({"tool_name": "run_command", "tool_input": {}}), "command"),
        (json.dumps({"tool_name": "run_command"}), "input"),
    ):
        decision, reason = antigravity(text)
        assert decision == DENY and "fault" in reason and cause in reason, (text, reason)

    def unreadable() -> None:
        raise OSError("policy unreadable")

    with monkeypatch.context() as planted:
        planted.setattr(hooks, "load_policy", unreadable)
        for adapter, payload in ((claude, bash("ls")), (antigravity, run_command("ls"))):
            decision, reason = adapter(payload)
            assert decision == DENY and "policy unreadable" in reason

    def broken(*_args: object) -> None:
        raise RuntimeError("check exploded")

    with monkeypatch.context() as planted:
        planted.setattr(ap, "decide_shell", broken)
        decision, reason = claude(bash("ls"))
        assert decision == DENY and "check exploded" in reason

    with monkeypatch.context() as planted:
        planted.setattr(hooks, "render", broken)
        code, out, err = hooks.run("claude-code", json.dumps(bash("ls")), {})
        assert code == 2 and "check exploded" in err and json.loads(out)["decision"] == DENY

    done = subprocess.run(
        [sys.executable, str(HOOKS_SCRIPT), "claude-code"],
        input="{broken",
        capture_output=True,
        text=True,
        env=_without_signal(),
        timeout=60,
        check=False,
    )
    body = json.loads(done.stdout)["hookSpecificOutput"]
    assert done.returncode == 0 and body["permissionDecision"] == DENY and "fault" in body["permissionDecisionReason"]
    assert hooks.main(["no-such-host"]) == 2
    # Counterpart: well-formed input is no fault.
    assert claude(bash("ls"))[0] == ABSTAIN


def test_unrepresentable_ask_denies(monkeypatch: pytest.MonkeyPatch) -> None:
    assert claude(bash("gh pr merge 54"))[0] == ASK, "a host that can ask keeps the ask"

    monkeypatch.setitem(hooks.CAN_ASK, "claude-code", False)
    decision, reason = claude(bash("gh pr merge 54"))
    assert decision == DENY and "cannot ask" in reason
    assert claude(bash("ls -la"))[0] == ABSTAIN


def test_nested_shell_constructs_are_checked() -> None:
    commands = (
        "echo $(gh pr merge 54)",
        'echo "$(gh pr merge 54)"',
        "echo `gh pr merge 54`",
        "(cd /repo; gh pr merge 54)",
        "echo $(echo $(gh pr merge 54))",
        'env -u NAME -C /tmp -P /bin FOO=1 bash -c "gh pr merge 54"',
        "env -S 'bash -c \"gh pr merge 54\"'",
        "g$'h' pr merge 54",
    )
    for command in commands:
        assert ap.decide_shell(command).kind == ASK, command
        assert claude(bash(command))[0] == ASK
        assert claude(bash(command), {"HARNESS_UNATTENDED": "1"})[0] == DENY
    for command in ("echo '$(gh pr merge 54)'", "echo '(`gh pr merge 54`)'", "echo $(gh pr view 54)"):
        assert ap.decide_shell(command).kind == ABSTAIN, command
    for command in ("echo $(gh pr merge 54", "echo `gh pr merge 54", "env -u"):
        assert ap.decide_shell(command).kind == ASK, command


def test_wrapped_shell_commands_are_checked() -> None:
    for prefix in (
        "sudo -u root",
        "timeout 5",
        "nohup",
        "nice -n 5",
        "exec",
        "command",
        "time",
        "xargs -n 1",
        "env --file F --chdir D --unset N",
    ):
        assert ap.decide_shell(f"{prefix} bash -c 'gh pr merge 54'").kind == ASK, prefix


def test_antigravity_registration_is_anchored() -> None:
    command = ap.registration("antigravity")["hooks"][0]["command"]
    assert (
        command
        == "cd .. && ${HARNESS_PYTHON:-$( [ -x .venv/bin/python ] && printf .venv/bin/python || printf python3 )} scripts/agent_policy_hooks.py antigravity"
    )


def test_noncommand_shell_syntax_abstains() -> None:
    for line in ("echo $((1+2))", "ls $((2-1))dir", "echo stray)", r"echo $'\q'"):
        assert ap.decide_shell(line).kind == ABSTAIN, line


def test_foreign_hook_mentions_are_preserved() -> None:
    foreign = {"hooks": [{"command": "echo agent_policy_hooks.py"}]}
    config = {"hooks": {"PreToolUse": [foreign]}}
    assert foreign in ap.render_settings(config)["hooks"]["PreToolUse"]


def test_substitution_depth_is_bounded() -> None:
    line = "echo " + "$(" * 1500 + "true" + ")" * 1500
    try:
        result = ap.decide_shell(line)
    except RecursionError:
        pytest.fail("deep substitutions must return a decision, not raise RecursionError")
    assert result.kind == ASK
    process = subprocess.run(
        [sys.executable, str(REPO / "scripts/agent_policy.py"), "decide", "--shell", line],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert process.returncode == 0 and "ask" in process.stdout


def test_subprocess_calls_have_timeouts() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    if os.environ.get("STAGE2_PLANT_FAULT") == "1":
        source += "\nsubprocess.run(['true'])\n"
    tree = ast.parse(source)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess"
        and node.func.attr == "run"
    ]
    assert calls
    assert all(
        any(kw.arg == "timeout" and isinstance(kw.value, ast.Constant) and kw.value.value == 60 for kw in call.keywords)
        for call in calls
    )


def test_antigravity_asks_when_attended() -> None:
    for payload in (run_command("gh pr merge 54"), tool("github.merge_pull_request")):
        assert antigravity(payload)[0] == ASK
        assert antigravity(payload, {"HARNESS_UNATTENDED": "1"})[0] == DENY


def test_duplicate_rule_is_policy_fault(monkeypatch: pytest.MonkeyPatch) -> None:
    pattern = next(iter(mg.MERGE_ASK_RULES))
    monkeypatch.setitem(ap.OWN_ASK_RULES, pattern, "duplicate")
    result = ap.decide_shell("ls")
    assert result.kind == DENY
    assert f"the policy names the rule {pattern} twice" in result.message()
    assert "cannot be split" not in result.message()


def test_missing_shared_rule_reports_both_sources_once(tmp_path: Path) -> None:
    root = _fresh_root(tmp_path / "root")
    path = root / ".claude" / "settings.json"
    settings = _read(path)
    rule = op.layer1_ask_rules()[0]
    settings["permissions"]["ask"].remove(rule)
    _write(path, settings)
    problems = [problem for problem in ap.check(root) if rule in problem]
    assert len(problems) == 1
    assert "Omnigent" in problems[0] and "agent policy" in problems[0]
