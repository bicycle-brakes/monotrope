"""Every merge an agent can start asks first (plans/changes/harness-decide-adr, criterion 12).

The rules are named once, in `scripts/merge_guard.py`; these tests compare
`.claude/settings.json` against that list and hold the matcher it is compared
with. The Omnigent ask rule beside them is held by
`tests/test_omnigent_deny_layers.py`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import merge_guard as mg  # noqa: E402
import omnigent_policy as op  # noqa: E402

SETTINGS = REPO / ".claude" / "settings.json"


def _settings() -> dict:
    return json.loads(SETTINGS.read_text(encoding="utf-8"))


def _copy(settings: dict) -> dict:
    return json.loads(json.dumps(settings))


def test_settings_ask_before_every_merge() -> None:
    ask = _settings()["permissions"]["ask"]
    missing = [rule for rule in mg.MERGE_ASK_RULES if rule not in ask]
    assert not missing, f".claude/settings.json does not ask before: {missing}"


def test_no_deny_or_allow_rule_covers_a_merge() -> None:
    assert mg.problems(_settings()) == []


def test_each_rule_matches_its_own_sample() -> None:
    for rule, (_, sample) in mg.MERGE_ASK_RULES.items():
        assert mg.covers(rule, sample), f"{rule!r} does not match its own sample {sample!r}"
    for sample in mg.EXTRA_SAMPLES:
        assert any(mg.covers(rule, sample) for rule in mg.MERGE_ASK_RULES), f"no merge rule asks before {sample!r}"


def test_every_rule_has_a_reason_and_a_sample() -> None:
    assert len(mg.MERGE_ASK_RULES) == 8
    for rule, (reason, sample) in mg.MERGE_ASK_RULES.items():
        assert len(reason.strip()) >= 10, f"{rule!r} has no reason"
        assert sample.strip(), f"{rule!r} has no sample"


# Every spelling of the repository flag before a subcommand that gh 2.101.0 accepted on 2026-09-30 (measured
# with `pr view`), and the same spelling of `pr merge`. Typed here, not read from the module, so that a
# spelling dropped from `EXTRA_SAMPLES` still has to ask.
REPOSITORY_FLAG_MERGES = (
    "gh -R o/r pr merge 54",
    "gh -Ro/r pr merge 54",
    "gh -R=o/r pr merge 54",
    "gh --repo o/r pr merge 54",
    "gh --repo=o/r pr merge 54",
    "gh pr -R o/r merge 54",
    "gh pr -Ro/r merge 54",
    "gh pr -R=o/r merge 54",
    "gh pr --repo o/r merge 54 --squash",
    "gh pr --repo=o/r merge --auto 54",
    "gh -R o/r pr merge",
)

# Reads with the repository flag in the same places; none of them may prompt.
REPOSITORY_FLAG_READS = (
    "gh -R o/r pr view 53",
    "gh --repo o/r pr view 53 --json mergeable,mergeStateStatus",
    "gh pr -R o/r view 53 --json mergeable,mergeStateStatus",
    "gh pr --repo=o/r checks 54",
    "gh pr -R o/r list --state merged",
    "gh -R o/r pr list --search is:merged",
    "gh pr -R o/r checkout merge-fix",
    "gh pr view 53 -R o/r --json mergedAt",
)


def test_the_repository_flag_before_a_subcommand_still_asks() -> None:
    for command in REPOSITORY_FLAG_MERGES:
        call = f"Bash({command})"
        assert any(mg.covers(rule, call) for rule in mg.MERGE_ASK_RULES), f"no merge rule asks before {call!r}"
    for command in REPOSITORY_FLAG_READS:
        call = f"Bash({command})"
        hit = [rule for rule in mg.MERGE_ASK_RULES if mg.covers(rule, call)]
        assert not hit, f"the read {call!r} would prompt through {hit}"


def test_a_missing_or_covered_merge_rule_is_caught() -> None:
    base = _settings()
    assert mg.problems(base) == []

    for rule in mg.MERGE_ASK_RULES:
        dropped = _copy(base)
        dropped["permissions"]["ask"].remove(rule)
        assert any("lacks the ask rule" in p and rule in p for p in mg.problems(dropped)), f"dropping {rule!r} passed"

    for kind, rule in (("allow", "Bash(gh *)"), ("deny", "Bash"), ("allow", "mcp__github"), ("deny", "mcp__*")):
        planted = _copy(base)
        planted["permissions"].setdefault(kind, []).append(rule)
        assert any(f"the {kind} rule {rule}," in p for p in mg.problems(planted)), f"{kind} {rule!r} was not caught"


def test_a_rule_beside_the_merges_is_not_reported() -> None:
    """The counterpart: a matcher that takes every rule for a merge rule would block harmless settings."""
    base = _settings()
    for kind, rule in (
        ("allow", "Bash(gh pr view *)"),
        ("allow", "Bash(git push origin feat/*)"),
        ("allow", "mcp__github__get_pull_request"),
        ("deny", "mcp__gitlab"),
        ("deny", "Edit(//**/.claude/settings.json)"),
        ("deny", "WebFetch(domain:github.com)"),
    ):
        planted = _copy(base)
        planted["permissions"].setdefault(kind, []).append(rule)
        assert mg.problems(planted) == [], f"{kind} {rule!r} was taken for a merge rule"


def test_the_matcher_follows_the_documented_forms() -> None:
    assert mg.covers("Bash(gh pr merge *)", "Bash(gh pr merge)"), "a trailing ' *' also matches the bare command"
    assert mg.covers("Bash(gh pr merge:*)", "Bash(gh pr merge 54)"), "':*' is the older spelling of ' *'"
    assert not mg.covers("Bash(gh pr merge *)", "Bash(gh pr mergeable 54)"), "' *' keeps a word boundary"
    assert not mg.covers("Bash(gh api *merge*)", "Bash(gh api)"), "the bare command only for a lone trailing ' *'"
    assert mg.covers("Bash", "Bash(gh pr merge 54)"), "a bare Bash covers every command"
    assert mg.covers("mcp__github", "mcp__github__merge_pull_request"), "a server's name covers its tools"
    assert not mg.covers("Bash(gh pr merge *)", "mcp__github__merge_pull_request"), "a Bash rule is not an MCP rule"
    assert not mg.covers("Edit(*)", "Bash(gh pr merge 54)"), "another tool's rule matches no call here"


def test_the_omnigent_render_keeps_the_merge_rules(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "settings.json"
    target.parent.mkdir(parents=True)
    target.write_text(SETTINGS.read_text(encoding="utf-8"), encoding="utf-8")

    op.write(tmp_path)
    rendered = json.loads(target.read_text(encoding="utf-8"))
    ask = rendered["permissions"]["ask"]
    assert [rule for rule in ask if rule in mg.MERGE_ASK_RULES] == list(mg.MERGE_ASK_RULES)
    assert op.check(tmp_path) == []
    assert mg.problems(rendered) == []
