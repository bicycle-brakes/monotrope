"""The one list of ask rules that stop an agent before it merges a pull request.

A decision in this repository takes effect when the maintainer merges the pull
request that carries it, or asks an agent to (plans/changes/harness-decide-adr,
criterion 11). So every way an agent here can merge is an ask rule in
`.claude/settings.json`: Claude Code prompts before the call in every permission
mode, and where nobody can answer the prompt the call is refused. It is a brake
against accidents, not a lock - it matches the command's text, and another
spelling passes it (docs/WORKFLOW.md, "What this does not do", names them).

`MERGE_ASK_RULES` maps each rule to its one-line reason and a sample call the
rule must match. `tests/test_merge_guard.py` compares `.claude/settings.json`
against this list; nothing else in the repository types it. The Omnigent rules
beside them belong to `scripts/omnigent_policy.py`, whose `--write` keeps every
rule it does not own.

A call is written the way a permission rule names it: `Bash(<command>)` for a
shell command, the bare tool name for any other tool
(`mcp__<server>__<tool>` for an MCP tool).

`covers(rule, call)` is Claude Code's matching as documented
(code.claude.com/docs/en/permissions, read 2026-09-30), as far as this list
needs it:

* a rule without `(` is a tool-name glob that must match the whole name; a
  server's name (`mcp__github`) also covers every tool of that server, and a
  bare `Bash` covers every command;
* `Bash(<pattern>)` matches the whole command: `*` stands for any text, a
  trailing `:*` is the older spelling of a trailing ` *`, everything else is
  literal, and a trailing ` *` that is the only wildcard also matches the bare
  command (`Bash(gh pr merge *)` matches `gh pr merge`);
* a rule for any other tool (`Edit(...)`, `WebFetch(...)`) matches no call here.
"""

from __future__ import annotations

import fnmatch
import re

# Rule -> (why it asks, a call it must match).
MERGE_ASK_RULES: dict[str, tuple[str, str]] = {
    "Bash(gh pr merge *)": (
        "every gh pr merge, any flag (--auto, --admin, --squash), and the bare command",
        "Bash(gh pr merge 54 --merge --match-head-commit abc1234)",
    ),
    "Bash(gh -* pr merge*)": (
        "gh pr merge with a flag before pr: gh takes its repository flag there (-R o/r, -Ro/r, -R=o/r, --repo o/r, "
        "--repo=o/r)",
        "Bash(gh -R o/r pr merge 54)",
    ),
    "Bash(gh pr -* merge *)": (
        "gh pr merge with the repository flag between pr and merge; gh refuses that flag without a pull request "
        'argument, so the rule wants one after merge and leaves --json mergeable alone; "merge" in a later '
        "argument also prompts",
        "Bash(gh pr -R o/r merge 54)",
    ),
    "Bash(gh api *merge*)": (
        "the REST merge endpoint and the GraphQL mergePullRequest mutation written in the command (one read from a "
        'file passes); a read containing "merge" also prompts',
        "Bash(gh api -X PUT repos/o/r/pulls/54/merge)",
    ),
    "Bash(gh api *Merge*)": (
        "the GraphQL enablePullRequestAutoMerge mutation written in the command; whether matching ignores case is "
        "not documented",
        "Bash(gh api graphql -f query='mutation { enablePullRequestAutoMerge("
        'input: {pullRequestId: "x"}) { clientMutationId } }\')',
    ),
    "Bash(gh alias set *)": (
        "gh alias set can give pr merge a name the other rules do not match; gh alias import and an edit of gh's "
        "config file can too, and pass (docs/WORKFLOW.md names the limit)",
        "Bash(gh alias set pm 'pr merge')",
    ),
    "Bash(git push *main*)": (
        'a push to the unprotected main lands a change with no pull request; any branch name containing "main" '
        "also prompts",
        "Bash(git push origin HEAD:main)",
    ),
    "mcp__*__merge_pull_request": (
        "a GitHub MCP server's merge tool, under any server name",
        "mcp__github__merge_pull_request",
    ),
}

# Further calls a merge rule must match and no deny or allow rule may cover: the GitHub MCP merge tool under
# this machine's server name, and the spellings of the repository flag before a subcommand that gh 2.101.0
# accepts (measured on 2026-09-30 with `pr view`, never with a merge; `-R/--repo` is a flag of `gh pr` that
# `pr merge` inherits, as `gh pr merge --help` lists it).
EXTRA_SAMPLES: tuple[str, ...] = (
    "mcp__plugin_engineering_github__merge_pull_request",
    "Bash(gh --repo o/r pr merge 54)",
    "Bash(gh --repo=o/r pr merge 54)",
    "Bash(gh -Ro/r pr merge 54)",
    "Bash(gh -R=o/r pr merge 54)",
    "Bash(gh pr --repo o/r merge 54)",
    "Bash(gh pr --repo=o/r merge 54)",
    "Bash(gh pr -Ro/r merge 54)",
    "Bash(gh pr -R=o/r merge 54)",
)

_CALL = re.compile(r"([A-Za-z_][\w-]*)\((.*)\)", re.S)


def _parse(call: str) -> tuple[str, str | None]:
    """`Bash(gh pr view)` -> ("Bash", "gh pr view"); a bare tool name -> (name, None)."""
    m = _CALL.fullmatch(call)
    return (m.group(1), m.group(2)) if m else (call, None)


def covers(rule: str, call: str) -> bool:
    """Does the permission rule `rule` match `call`? (Matching as the module docstring states it.)"""
    tool, command = _parse(call)
    if "(" not in rule:
        return fnmatch.fnmatchcase(tool, rule) or fnmatch.fnmatchcase(tool, rule + "__*")
    name, pattern = _parse(rule)
    if name != "Bash" or pattern is None or command is None or tool != "Bash":
        return False
    if pattern.endswith(":*"):
        pattern = pattern[:-2] + " *"
    if re.fullmatch(".*".join(re.escape(part) for part in pattern.split("*")), command, re.S):
        return True
    return pattern.endswith(" *") and pattern.count("*") == 1 and command == pattern[:-2]


def samples() -> list[str]:
    """Every call a merge rule must stop: each rule's own sample, then `EXTRA_SAMPLES`."""
    return [sample for _, sample in MERGE_ASK_RULES.values()] + list(EXTRA_SAMPLES)


def problems(settings: dict) -> list[str]:
    """What keeps the settings from asking before every merge; empty when they do."""
    permissions = settings.get("permissions") or {}
    ask = permissions.get("ask") or []
    found = [
        f".claude/settings.json lacks the ask rule {rule} - {reason}"
        for rule, (reason, _) in MERGE_ASK_RULES.items()
        if rule not in ask
    ]
    for kind in ("deny", "allow"):
        for rule in permissions.get(kind) or []:
            hit = [call for call in samples() if covers(rule, call)]
            if hit:
                found.append(f".claude/settings.json has the {kind} rule {rule}, which covers the merge {hit[0]}")
    return found
