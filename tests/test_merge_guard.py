"""Every merge an agent can start asks first, and no merge-field read does (plans/changes/night-stall-guard).

The rules are named once, in `scripts/merge_guard.py`; these tests compare settings against that list
and hold the matcher it is compared with. The action and read commands below are typed here, not read
from the module, so a rule dropped from the list still fails against an independently written spelling.
The night overlay checks come from `tools/claude-code/night.py`, which turns the day asks into denies.
The Omnigent ask rule beside them is held by `tests/test_omnigent_deny_layers.py`.

The held day settings have been bootstrapped to the narrowed merge rules. Both independent command
matrices exercise that actual profile and the night overlay derived from it. Policy rendering uses
an isolated copy of the held settings, preserving the source file and its unrelated settings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "tools" / "claude-code"))

import merge_guard as mg  # noqa: E402
import night  # noqa: E402
import omnigent_policy as op  # noqa: E402

SETTINGS = REPO / ".claude" / "settings.json"
NIGHT_FRAGMENT = REPO / "tools" / "claude-code" / "night-settings.json"


def _settings() -> dict:
    return json.loads(SETTINGS.read_text(encoding="utf-8"))


def _copy(settings: dict) -> dict:
    return json.loads(json.dumps(settings))


def _proposed_day_settings() -> dict:
    """The day ask list as this change proposes it: exactly the rules of `scripts/merge_guard.py`."""
    return {"permissions": {"ask": list(mg.MERGE_ASK_RULES)}}


def _night_denies() -> list[str]:
    """The deny rules a night overlay derives from the held day asks (the fragment adds the mode)."""
    fragment = json.loads(NIGHT_FRAGMENT.read_text(encoding="utf-8"))
    return night.build_overlay(fragment, [_settings()])["permissions"]["deny"]


def test_settings_ask_before_every_merge() -> None:
    ask = _settings()["permissions"]["ask"]
    missing = [rule for rule in mg.MERGE_ASK_RULES if rule not in ask]
    assert not missing, f".claude/settings.json does not ask before: {missing}"
    assert not {"Bash(gh api *merge*)", "Bash(gh api *Merge*)"}.intersection(ask), (
        "the held day settings still ask on merge-field reads"
    )


def test_no_deny_or_allow_rule_covers_a_merge() -> None:
    assert mg.problems(_settings()) == []


def test_each_rule_matches_its_own_sample() -> None:
    for rule, (_, sample) in mg.MERGE_ASK_RULES.items():
        assert mg.covers(rule, sample), f"{rule!r} does not match its own sample {sample!r}"
    for sample in mg.EXTRA_SAMPLES:
        assert any(mg.covers(rule, sample) for rule in mg.MERGE_ASK_RULES), f"no merge rule asks before {sample!r}"


def test_every_rule_has_a_reason_and_a_sample() -> None:
    """No rule count is pinned; the required behaviors are held by the independently written matrix below."""
    assert set(mg.MERGE_ASK_RULES), "the merge brake holds no rule"
    for rule, (reason, sample) in mg.MERGE_ASK_RULES.items():
        assert len(reason.strip()) >= 10, f"{rule!r} has no reason"
        assert sample.strip(), f"{rule!r} has no sample"


# Every merge spelling the brake must stop, written here and never read from the module: a rule dropped
# from `scripts/merge_guard.py` fails against these independently written commands even when every
# remaining rule still matches its own sample. The reads name the fields of the incident of 2026-11-08
# (`mergedAt`, `isInMergeQueue`) and the `mergeable`/`mergeStateStatus` fields beside them.
MERGE_ACTIONS: dict[str, tuple[str, ...]] = {
    "bare gh pr merge": ("Bash(gh pr merge)",),
    "a flagged gh pr merge": (
        "Bash(gh pr merge 54)",
        "Bash(gh pr merge 54 --merge)",
        "Bash(gh pr merge --squash 54)",
        "Bash(gh pr merge --auto 54)",
        "Bash(gh pr merge 54 --admin)",
    ),
    "a gh pr merge with the repository flag before pr": (
        "Bash(gh -R o/r pr merge 54)",
        "Bash(gh -Ro/r pr merge 54)",
        "Bash(gh -R=o/r pr merge 54)",
        "Bash(gh --repo o/r pr merge 54)",
        "Bash(gh --repo=o/r pr merge 54)",
    ),
    "a gh pr merge with the repository flag between pr and merge": (
        "Bash(gh pr -R o/r merge 54)",
        "Bash(gh pr -Ro/r merge 54)",
        "Bash(gh pr -R=o/r merge 54)",
        "Bash(gh pr --repo o/r merge 54 --squash)",
        "Bash(gh pr --repo=o/r merge --auto 54)",
    ),
    "a REST PUT to the merge endpoint": (
        "Bash(gh api -X PUT repos/o/r/pulls/54/merge)",
        "Bash(gh api --method PUT repos/o/r/pulls/54/merge)",
        "Bash(gh api repos/o/r/pulls/54/merge -X PUT)",
        "Bash(gh api repos/o/r/pulls/54/merge --method PUT)",
        "Bash(gh api -X PUT repos/o/r/pulls/54/merge -f merge_method=squash)",
    ),
    "the GraphQL mergePullRequest mutation": (
        "Bash(gh api graphql -f query='mutation { mergePullRequest(input: {pullRequestId: "
        '"x"}) { clientMutationId } }\')',
        "Bash(gh api graphql --raw-field query='mutation { mergePullRequest(input: {pullRequestId: "
        '"x"}) { clientMutationId } }\')',
    ),
    "the GraphQL enablePullRequestAutoMerge mutation": (
        "Bash(gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {pullRequestId: "
        '"x"}) { clientMutationId } }\')',
        "Bash(gh api graphql --raw-field query='mutation { enablePullRequestAutoMerge(input: {pullRequestId: "
        '"x"}) { clientMutationId } }\')',
    ),
    "the GraphQL enqueuePullRequest mutation": (
        "Bash(gh api graphql -f query='mutation { enqueuePullRequest(input: {pullRequestId: "
        '"x"}) { clientMutationId } }\')',
        "Bash(gh api graphql --raw-field query='mutation { enqueuePullRequest(input: {pullRequestId: "
        '"x"}) { clientMutationId } }\')',
    ),
    "the GitHub MCP merge tool": (
        "mcp__github__merge_pull_request",
        "mcp__plugin_engineering_github__merge_pull_request",
    ),
}

MERGE_FIELD_READS = (
    # The incident's query shape: a status read naming mergedAt and isInMergeQueue.
    'Bash(gh api graphql -f query=\'query { repository(owner:"o", name:"r") { pullRequest(number:54) '
    "{ mergedAt isInMergeQueue } } }')",
    'Bash(gh api graphql --raw-field query=\'query { repository(owner:"o", name:"r") { pullRequest(number:54) '
    "{ mergeable mergeStateStatus } } }')",
    "Bash(gh pr view 54 --json mergedAt,mergeable,mergeStateStatus,isInMergeQueue)",
    "Bash(gh pr view 54 -R o/r --json mergedAt)",
    "Bash(gh api repos/o/r/pulls/54)",
    "Bash(gh api -X GET repos/o/r/pulls/54/merge)",
    "Bash(gh api repos/o/r/pulls/54/merge)",
)


def test_direct_merge_actions_are_guarded() -> None:
    """Criterion 3: every independently written merge action is stopped by the day asks and by the night denies."""
    day = _settings()
    night_denies = _night_denies()
    assert mg.problems(day) == [], "a day deny or allow rule covers a merge sample"
    for behavior, calls in MERGE_ACTIONS.items():
        for call in calls:
            day_hit = [rule for rule in day["permissions"]["ask"] if mg.covers(rule, call)]
            assert day_hit, f"no merge rule asks before the {behavior} {call!r}"
            assert any(mg.covers(rule, call) for rule in night_denies), (
                f"the night overlay would not deny the {behavior} {call!r}"
            )


def test_merge_field_reads_do_not_trigger_the_brake() -> None:
    """Criterion 4: a read naming merge fields prompts nowhere - not through a day ask, not through a night deny."""
    day = _settings()
    night_denies = _night_denies()
    for call in MERGE_FIELD_READS:
        day_hit = [rule for rule in day["permissions"]["ask"] if mg.covers(rule, call)]
        night_hit = [rule for rule in night_denies if mg.covers(rule, call)]
        assert not day_hit and not night_hit, f"the read {call!r} would prompt through {day_hit + night_hit}"


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
    base = _proposed_day_settings()
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
    base = _proposed_day_settings()
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
    assert not mg.covers("Bash(gh api *PUT*pulls/*/merge*)", "Bash(gh api)"), (
        "the bare command only for a lone trailing ' *'"
    )
    assert mg.covers("Bash", "Bash(gh pr merge 54)"), "a bare Bash covers every command"
    assert mg.covers("mcp__github", "mcp__github__merge_pull_request"), "a server's name covers its tools"
    assert not mg.covers("Bash(gh pr merge *)", "mcp__github__merge_pull_request"), "a Bash rule is not an MCP rule"
    assert not mg.covers("Edit(*)", "Bash(gh pr merge 54)"), "another tool's rule matches no call here"


def test_the_omnigent_render_keeps_the_merge_rules(tmp_path: Path) -> None:
    """Criterion 5: render a copy of the held settings, keeping merge rules and unrelated settings."""
    proposed = _settings()
    target = tmp_path / ".claude" / "settings.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(proposed, indent=2) + "\n", encoding="utf-8")

    op.write(tmp_path)
    rendered = json.loads(target.read_text(encoding="utf-8"))
    ask = rendered["permissions"]["ask"]
    assert [rule for rule in ask if rule in mg.MERGE_ASK_RULES] == list(mg.MERGE_ASK_RULES)
    assert "Bash(codex *)" in ask, "the render lost the unrelated Codex brake"
    assert op.check(tmp_path) == []
    assert mg.problems(rendered) == []
    for call in MERGE_FIELD_READS:
        hit = [rule for rule in ask if mg.covers(rule, call)]
        assert not hit, f"the rendered read {call!r} would prompt through {hit}"
    assert {key: value for key, value in rendered.items() if key != "permissions"} == {
        key: value for key, value in proposed.items() if key != "permissions"
    }
    assert rendered["permissions"] == proposed["permissions"]


@pytest.mark.parametrize("broad_rule", ["Bash(gh api *merge*)", "Bash(gh api *Merge*)"])
def test_day_checker_rejects_broad_merge_asks(broad_rule: str) -> None:
    """The day checker must reject a return of either incident rule, beside the held read matrices."""
    settings = _settings()
    assert mg.problems(settings) == []
    settings["permissions"]["ask"].append(broad_rule)
    assert any(broad_rule in problem and "reads" in problem for problem in mg.problems(settings)), (
        f"the day checker accepted {broad_rule}, which prompts on merge-field reads"
    )


@pytest.mark.parametrize("broad_rule", ["Bash(gh api *merge*)", "Bash(gh api *Merge*)"])
@pytest.mark.parametrize("check", ["reads", "render"])
def test_held_profile_regressions_are_detected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, broad_rule: str, check: str
) -> None:
    """Plant the incident in a copy of the held day file; both consumers must reject it."""
    settings = _settings()
    settings["permissions"]["ask"].append(broad_rule)
    target = tmp_path / "held-settings.json"
    target.write_text(json.dumps(settings), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "SETTINGS", target)
    with pytest.raises(AssertionError, match="read"):
        if check == "reads":
            test_merge_field_reads_do_not_trigger_the_brake()
        else:
            test_the_omnigent_render_keeps_the_merge_rules(tmp_path / "render")
