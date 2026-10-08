"""The branch ruleset asks for what rules RB-M6 and RB-G7 ask — and a failed look is red.

**What RB-M6 asks.** The branch rules of the default branch are asserted from
within the repository, and they ask for what one GitHub account can hold:

1. a pull request is required,
2. the check `verify` is required, and it is pinned to GitHub Actions
   (`integration_id` 15368) — the job that runs the gate list, not a commit
   status that any token can post (RB-M6, F-3),
3. no force push,
4. no deletion,
5. no bypass — every ruleset that supplies (1) to (4), or (6) below, shows
   an empty bypass list.

The second approval (code-owner review, approval not by the last pusher) is not
asked for. It returns when a second identity exists, for example a GitHub App:
the maintainer, the agents and every token act under one account today, and
GitHub lets no author approve their own pull request (ADR 0008). A ruleset that
asks for more than the six still holds.

**What RB-G7 adds.** (6) Branches up to date before merging: an active
`required_status_checks` rule with at least one check sets
`strict_required_status_checks_policy` to `true`. The CI checks the merge ref
(`tests/test_ci.py`), and this makes it the merge that happens. GitHub applies
the most restrictive version of aggregated rules, so any ruleset may supply
it, and (5) then covers that ruleset. Decided 2026-10-08.

**Why only the writer machine measures.** GitHub shows the bypass list of a
ruleset only to whoever may edit that ruleset ("Get a repository ruleset", REST
documentation). The workflow token of the hosted CI cannot, and a token that
could would be able to change the ruleset it checks. So the live check runs in
the gate `ruleset` (`decisions/gates.yaml`, `placement: writer`) on the
maintainer's machine, with the maintainer's own `gh` login, and nowhere else.
Everything else in this file checks answers the tests invent; no test changes
anything at GitHub.

**Not measured is red, never green.** `gh` missing, a network or login failure,
an answer that is not JSON or has the wrong shape, a ruleset that shows no
bypass list, a repository other than the one this checkout is of: each is a finding that begins `not measured:` and says which step
failed. An empty list of findings means the six requirements were seen to hold
— nothing else does.

**The return trigger.** When a second identity exists, a later rule-set version
asks for the second approval again and this file asks for it with the rule.
"""

from __future__ import annotations

import copy
import functools
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.parse
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GATES = REPO_ROOT / "decisions" / "gates.yaml"

# The gate `ruleset` sets this variable; without it the live check is skipped
# and nothing is sent to GitHub. The floor gate `pytest` runs the whole suite in
# hosted CI and must not call GitHub.
LIVE_ENV = "RULESET_ASSERT"

# The check context the required-check rule must list: the hosted job that
# runs every verify gate.
REQUIRED_CHECK = "verify"

# RB-G7's requirement: the branch must be up to date with its target before it
# merges, so the merge ref the CI checked is the merge that happens.
UP_TO_DATE = "branches up to date before merging"
UP_TO_DATE_OPTION = "Require branches to be up to date before merging"

# The GitHub App id of GitHub Actions. A required check without it accepts a
# commit status of that name from anyone with a token — every agent here —
# without the job ever running.
GITHUB_ACTIONS_APP_ID = 15368

# A call that hangs must not hang `make verify`: an unreachable API is red.
GH_TIMEOUT_SECONDS = 60

# The rule types GitHub reports for a branch, and what each one asks for.
RULE_TYPES: dict[str, str] = {
    "pull_request": "pull request required",
    "required_status_checks": f"required check {REQUIRED_CHECK}",
    "non_fast_forward": "no force push",
    "deletion": "no deletion",
}

Api = Callable[[str], tuple[int, str]]
# The repository this checkout is of: `("owner/name", "")`, or `(None, reason)`.
Local = Callable[[], tuple[str | None, str]]


# --------------------------------------------------------------------------
# The measurement
# --------------------------------------------------------------------------


def gh_api(path: str) -> tuple[int, str]:
    """GET one API path through the `gh` login; `(exit code, stdout or stderr)`.

    `gh` fills `{owner}` and `{repo}` from `GH_REPO`, else from the default set
    with `gh repo set-default`, else from the remote — which need not be the
    repository this checkout is of, so `measure` compares (F-4). Only GET is
    ever sent: no `--method`, no field.
    """
    try:
        done = subprocess.run(
            ["gh", "api", path],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        return 127, "gh is not installed"
    except subprocess.TimeoutExpired:
        return 124, f"gh did not answer within {GH_TIMEOUT_SECONDS} s"
    return done.returncode, done.stdout if done.returncode == 0 else done.stderr


def local_repository(root: Path = REPO_ROOT) -> tuple[str | None, str]:
    """The repository this checkout is of, from its `origin` URL: `("owner/name", "")`.

    The URL forms git takes — `https://host/owner/name(.git)`,
    `git@host:owner/name(.git)`, `ssh://git@host/owner/name` — all end in
    `owner/name`. Anything else, or no `origin`, is `(None, reason)`.
    """
    try:
        done = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT_SECONDS,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return None, f"git remote get-url origin: {type(error).__name__}"
    url = done.stdout.strip()
    if done.returncode != 0 or not url:
        return None, "git remote get-url origin: " + (" ".join(done.stderr.split()) or "no origin")
    owner_and_name = [part for part in url.removesuffix("/").replace(":", "/").split("/") if part]
    if len(owner_and_name) < 3:
        return None, f"origin `{url}` does not read as owner/name"
    return f"{owner_and_name[-2]}/{owner_and_name[-1].removesuffix('.git')}", ""


def _lists_required_check(rule: dict[str, Any], *, pinned: bool = True) -> bool:
    """Does this `required_status_checks` rule list the check `verify`?

    With `pinned` the entry must also come from GitHub Actions
    (`integration_id`); a missing or other id is an unpinned check.
    """
    parameters = rule.get("parameters")
    checks = parameters.get("required_status_checks") if isinstance(parameters, dict) else None
    if not isinstance(checks, list):
        return False
    return any(
        isinstance(c, dict)
        and c.get("context") == REQUIRED_CHECK
        and (not pinned or c.get("integration_id") == GITHUB_ACTIONS_APP_ID)
        for c in checks
    )


def _supplying_rules(rules: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """The active rules that supply each of the four rule types."""
    supplied: dict[str, list[dict[str, Any]]] = {}
    for rule_type in RULE_TYPES:
        matching = [r for r in rules if r.get("type") == rule_type]
        if rule_type == "required_status_checks":
            matching = [r for r in matching if _lists_required_check(r)]
        supplied[rule_type] = matching
    return supplied


def _up_to_date_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The `required_status_checks` rules that set the up-to-date flag to `true` and list a check.

    Only the boolean counts: a missing key, `null` or the string "true" is not
    asked for. GitHub applies the most restrictive version of aggregated rules,
    so any such rule counts, not only the one that lists `verify`.
    """
    found = []
    for rule in rules:
        if rule.get("type") != "required_status_checks":
            continue
        parameters = rule.get("parameters")
        if not isinstance(parameters, dict):
            continue
        checks = parameters.get("required_status_checks")
        if parameters.get("strict_required_status_checks_policy") is True and isinstance(checks, list) and checks:
            found.append(rule)
    return found


def _suppliers(rules: list[dict[str, Any]]) -> list[Any]:
    """The `ruleset_id` of every rule that supplies one of the six requirements, once each."""
    ids: list[Any] = []
    for matching in [*_supplying_rules(rules).values(), _up_to_date_rules(rules)]:
        for rule in matching:
            if rule.get("ruleset_id") not in ids:
                ids.append(rule.get("ruleset_id"))
    return sorted(ids, key=str)


def _actor(actor: Any) -> str:
    if not isinstance(actor, dict):
        return str(actor)
    return f"{actor.get('actor_type', 'actor')} {actor.get('actor_id', '?')}"


def ruleset_findings(rules: list[dict[str, Any]], rulesets: dict[Any, Any]) -> list[str]:
    """What fails the six requirements; empty only when all six were seen to hold.

    `rules` is the answer of the branch-rules endpoint (active rules only, each
    with the `ruleset_id` it comes from); `rulesets` maps a ruleset id to the
    detail GitHub returned for it, an id without an entry being one that could
    not be read.
    """
    if not rules:
        return ["no active rule on the default branch — nothing binds a merge"]

    findings: list[str] = []
    for rule_type, matching in _supplying_rules(rules).items():
        if matching:
            continue
        if rule_type == "required_status_checks" and any(
            r.get("type") == rule_type and _lists_required_check(r, pinned=False) for r in rules
        ):
            findings.append(
                f"required check {REQUIRED_CHECK} is not pinned to GitHub Actions "
                f"(integration_id {GITHUB_ACTIONS_APP_ID}) — a commit status posted under any token could satisfy it"
            )
        else:
            findings.append(f"{RULE_TYPES[rule_type]} is not asked for")
    if not _up_to_date_rules(rules):
        findings.append(f'{UP_TO_DATE} is not asked for — tick "{UP_TO_DATE_OPTION}" in the ruleset (RB-G7)')

    for ruleset_id in _suppliers(rules):
        detail = rulesets.get(ruleset_id)
        if not isinstance(detail, dict):
            findings.append(f"not measured: ruleset {ruleset_id} could not be read")
            continue
        bypass = detail.get("bypass_actors")
        if not isinstance(bypass, list):
            findings.append(
                f"not measured: ruleset {ruleset_id} shows no bypass list — "
                "GitHub shows it only to whoever may edit the ruleset"
            )
        elif bypass:
            actors = ", ".join(_actor(a) for a in bypass)
            findings.append(f"ruleset {ruleset_id} lets {actors} bypass it")
    return findings


def _read(api: Api, path: str) -> tuple[Any, str | None]:
    """One call: `(parsed JSON, None)`, or `(None, "not measured: <path>: <reason>")`."""
    code, text = api(path)
    if code != 0:
        reason = " ".join(str(text).split()) or "no message"
        return None, f"not measured: {path}: exit {code}: {reason}"
    try:
        return json.loads(text), None
    except (TypeError, ValueError):
        return None, f"not measured: {path}: the answer is not JSON"


def measure(api: Api = gh_api, local: Local = local_repository) -> list[str]:
    """Read the default branch, its active rules and each supplying ruleset.

    Returns the findings of `ruleset_findings`, or at once the one finding
    `not measured: <path>: <reason>` for the first call that fails or answers
    in a shape the check does not know. Every step goes through `api`, so a
    test can drive the whole measurement with invented answers; `local` names
    the repository this checkout is of, and an answer about another one — a
    `GH_REPO` or a `gh` default that points elsewhere — is not measured
    either (F-4).
    """
    repo_path = "repos/{owner}/{repo}"
    repo, failed = _read(api, repo_path)
    if failed:
        return [failed]
    branch = repo.get("default_branch") if isinstance(repo, dict) else None
    if not isinstance(branch, str) or not branch:
        return [f"not measured: {repo_path}: no default_branch in the answer"]

    here, why_not = local()
    if here is None:
        return [f"not measured: {repo_path}: cannot tell which repository this checkout is of ({why_not})"]
    measured = repo.get("full_name")
    if not isinstance(measured, str) or measured.lower() != here.lower():
        return [
            f"not measured: {repo_path}: it answers for {measured!r}, but this checkout is of {here!r} "
            "(origin) — `GH_REPO` or the `gh repo set-default` points elsewhere"
        ]

    rules_path = repo_path + "/rules/branches/" + urllib.parse.quote(branch, safe="")
    rules, failed = _read(api, rules_path)
    if failed:
        return [failed]
    if not isinstance(rules, list) or not all(isinstance(r, dict) for r in rules):
        return [f"not measured: {rules_path}: the answer is not a list of rules"]

    details: dict[Any, Any] = {}
    for ruleset_id in _suppliers(rules):
        if not isinstance(ruleset_id, int) or isinstance(ruleset_id, bool):
            continue  # `ruleset_findings` reports a rule without a readable origin
        ruleset_path = f"{repo_path}/rulesets/{ruleset_id}"
        detail, failed = _read(api, ruleset_path)
        if failed:
            return [failed]
        if not isinstance(detail, dict):
            return [f"not measured: {ruleset_path}: the answer is not a ruleset"]
        details[ruleset_id] = detail
    return ruleset_findings(rules, details)


# --------------------------------------------------------------------------
# Invented answers — the live answers of 2026-10-05, only the keys read above,
# plus the one key RB-G7 reads, set as the floor asks (live: false on 2026-10-08)
# --------------------------------------------------------------------------

RULESET_ID = 24528176
REPO_PATH = "repos/{owner}/{repo}"
HERE = "example/instance"  # the repository the stubs answer for, and the checkout is of


def _here() -> tuple[str | None, str]:
    return HERE, ""


def _measure(api: Api) -> list[str]:
    """`measure` for a checkout of `HERE`."""
    return measure(api, _here)


def _todays_rules() -> list[dict[str, Any]]:
    return [
        {"type": "deletion", "ruleset_id": RULESET_ID},
        {"type": "non_fast_forward", "ruleset_id": RULESET_ID},
        {
            "type": "pull_request",
            "parameters": {
                "required_approving_review_count": 0,
                "require_code_owner_review": False,
                "require_last_push_approval": False,
            },
            "ruleset_id": RULESET_ID,
        },
        {
            "type": "required_status_checks",
            "parameters": {
                "strict_required_status_checks_policy": True,
                "required_status_checks": [{"context": "verify", "integration_id": 15368}],
            },
            "ruleset_id": RULESET_ID,
        },
    ]


def _todays_ruleset() -> dict[str, Any]:
    return {"id": RULESET_ID, "bypass_actors": []}


def _todays_answers() -> dict[str, tuple[int, str]]:
    """The answers of the three endpoints, by path."""
    return {
        REPO_PATH: (0, json.dumps({"default_branch": "main", "full_name": HERE})),
        f"{REPO_PATH}/rules/branches/main": (0, json.dumps(_todays_rules())),
        f"{REPO_PATH}/rulesets/{RULESET_ID}": (0, json.dumps(_todays_ruleset())),
    }


def _stub_api(answers: dict[str, tuple[int, str]], calls: list[str] | None = None) -> Api:
    """An API that answers by path; a path it does not know is a 404."""

    def api(path: str) -> tuple[int, str]:
        if calls is not None:
            calls.append(path)
        return answers.get(path, (1, f"gh: Not Found (HTTP 404) for {path}"))

    return api


def _without(rules: list[dict[str, Any]], rule_type: str) -> list[dict[str, Any]]:
    return [r for r in rules if r["type"] != rule_type]


# --------------------------------------------------------------------------
# What holds
# --------------------------------------------------------------------------


def test_todays_ruleset_holds() -> None:
    assert ruleset_findings(_todays_rules(), {RULESET_ID: _todays_ruleset()}) == []


def test_a_stricter_ruleset_still_holds() -> None:
    """The six are a floor: asking for more is the upgrade the rule expects."""
    rules = _todays_rules()
    for rule in rules:
        if rule["type"] == "pull_request":
            rule["parameters"] = {
                "required_approving_review_count": 1,
                "require_code_owner_review": True,
                "require_last_push_approval": True,
            }
        if rule["type"] == "required_status_checks":
            rule["parameters"]["required_status_checks"].append({"context": "floor"})
    rules.append({"type": "required_linear_history", "ruleset_id": RULESET_ID})
    # a second ruleset that repeats a rule and also has an empty bypass list
    rules.append({"type": "deletion", "ruleset_id": 7})
    rulesets = {RULESET_ID: _todays_ruleset(), 7: {"id": 7, "bypass_actors": []}}
    assert ruleset_findings(rules, rulesets) == []


def test_the_measurement_holds_on_todays_answers() -> None:
    calls: list[str] = []
    assert _measure(_stub_api(_todays_answers(), calls)) == []
    assert calls == [
        REPO_PATH,
        f"{REPO_PATH}/rules/branches/main",
        f"{REPO_PATH}/rulesets/{RULESET_ID}",
    ]


def test_the_measurement_asks_for_the_branch_the_repository_names() -> None:
    """The default branch comes from the API, and a slash in it is escaped."""
    answers = _todays_answers()
    answers[REPO_PATH] = (0, json.dumps({"default_branch": "release/1", "full_name": HERE}))
    answers[f"{REPO_PATH}/rules/branches/release%2F1"] = answers.pop(f"{REPO_PATH}/rules/branches/main")
    assert _measure(_stub_api(answers)) == []


# --------------------------------------------------------------------------
# What goes red — each requirement that goes is a finding
# --------------------------------------------------------------------------


def test_the_ruleset_check_goes_red_when_a_bypass_is_added() -> None:
    ruleset = _todays_ruleset()
    ruleset["bypass_actors"] = [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
    findings = ruleset_findings(_todays_rules(), {RULESET_ID: ruleset})
    assert findings == [f"ruleset {RULESET_ID} lets RepositoryRole 5 bypass it"]


# Listed here and not taken from RULE_TYPES: a requirement that fell out of that
# table would otherwise fall out of this test with it (planted fault F03).
THE_FOUR_RULE_TYPES = ("pull_request", "required_status_checks", "non_fast_forward", "deletion")


@pytest.mark.parametrize("rule_type", THE_FOUR_RULE_TYPES)
def test_the_ruleset_check_goes_red_when_a_rule_is_removed(rule_type: str) -> None:
    rules = _without(_todays_rules(), rule_type)
    findings = ruleset_findings(rules, {RULESET_ID: _todays_ruleset()})
    expected = [f"{RULE_TYPES[rule_type]} is not asked for"]
    if rule_type == "required_status_checks":
        # the flag lives in that rule, so it goes with it
        assert len(findings) == 2
        assert findings[0] == expected[0]
        assert findings[1].startswith(f"{UP_TO_DATE} is not asked for")
    else:
        assert findings == expected


def test_the_ruleset_check_goes_red_when_verify_is_not_required() -> None:
    rules = _todays_rules()
    for rule in rules:
        if rule["type"] == "required_status_checks":
            rule["parameters"]["required_status_checks"] = [{"context": "lint"}]
    findings = ruleset_findings(rules, {RULESET_ID: _todays_ruleset()})
    assert findings == [f"required check {REQUIRED_CHECK} is not asked for"]


@pytest.mark.parametrize(
    "entry",
    [
        pytest.param({"context": "verify"}, id="no-integration-id"),
        pytest.param({"context": "verify", "integration_id": None}, id="null-integration-id"),
        pytest.param({"context": "verify", "integration_id": 99999}, id="another-app"),
        pytest.param({"context": "verify", "integration_id": str(GITHUB_ACTIONS_APP_ID)}, id="id-as-a-string"),
    ],
)
def test_the_ruleset_check_goes_red_when_verify_is_not_pinned_to_github_actions(entry: dict[str, Any]) -> None:
    """An unpinned `verify` accepts a commit status posted by hand; it is a finding, not a pass (F-3)."""
    rules = _todays_rules()
    for rule in rules:
        if rule["type"] == "required_status_checks":
            rule["parameters"]["required_status_checks"] = [entry]
    findings = ruleset_findings(rules, {RULESET_ID: _todays_ruleset()})
    assert len(findings) == 1
    assert "not pinned to GitHub Actions" in findings[0]
    assert str(GITHUB_ACTIONS_APP_ID) in findings[0]


def test_one_pinned_verify_among_unpinned_ones_holds() -> None:
    """Rules add up: a second ruleset that lists an unpinned `verify` does not undo the pinned one."""
    rules = _todays_rules()
    rules.append(
        {
            "type": "required_status_checks",
            "parameters": {"required_status_checks": [{"context": "verify"}]},
            "ruleset_id": 7,
        }
    )
    assert ruleset_findings(rules, {RULESET_ID: _todays_ruleset(), 7: {"id": 7, "bypass_actors": []}}) == []


def _set_flag(rules: list[dict[str, Any]], value: Any, *, remove: bool = False) -> None:
    for rule in rules:
        if rule["type"] == "required_status_checks":
            if remove:
                rule["parameters"].pop("strict_required_status_checks_policy", None)
            else:
                rule["parameters"]["strict_required_status_checks_policy"] = value


@pytest.mark.parametrize(
    ("value", "remove"),
    [
        pytest.param(False, False, id="live-2026-10-08"),
        pytest.param(None, True, id="key-removed"),
        pytest.param(None, False, id="null"),
        pytest.param("true", False, id="string"),
    ],
)
def test_the_ruleset_check_goes_red_when_branches_need_not_be_up_to_date(value: Any, remove: bool) -> None:
    rules = _todays_rules()
    _set_flag(rules, value, remove=remove)
    findings = ruleset_findings(rules, {RULESET_ID: _todays_ruleset()})
    assert len(findings) == 1
    assert findings[0].startswith(UP_TO_DATE)
    assert UP_TO_DATE_OPTION in findings[0]


def _second_ruleset_rule(checks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "type": "required_status_checks",
        "parameters": {"strict_required_status_checks_policy": True, "required_status_checks": checks},
        "ruleset_id": 7,
    }


def test_the_ruleset_check_goes_red_when_only_a_rule_without_checks_asks_for_it() -> None:
    rules = _todays_rules()
    _set_flag(rules, False)
    rules.append(_second_ruleset_rule([]))
    findings = ruleset_findings(rules, {RULESET_ID: _todays_ruleset(), 7: {"id": 7, "bypass_actors": []}})
    assert len(findings) == 1
    assert findings[0].startswith(UP_TO_DATE)


def test_up_to_date_from_a_second_ruleset_holds() -> None:
    rules = _todays_rules()
    _set_flag(rules, False)
    rules.append(_second_ruleset_rule([{"context": "floor"}]))
    rulesets = {RULESET_ID: _todays_ruleset(), 7: {"id": 7, "bypass_actors": []}}
    assert ruleset_findings(rules, rulesets) == []


def test_the_ruleset_check_goes_red_when_the_up_to_date_ruleset_can_be_bypassed() -> None:
    rules = _todays_rules()
    _set_flag(rules, False)
    rules.append(_second_ruleset_rule([{"context": "floor"}]))
    bypass = [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
    rulesets = {RULESET_ID: _todays_ruleset(), 7: {"id": 7, "bypass_actors": bypass}}
    assert ruleset_findings(rules, rulesets) == ["ruleset 7 lets RepositoryRole 5 bypass it"]


def test_the_ruleset_check_goes_red_on_an_empty_rule_list() -> None:
    findings = ruleset_findings([], {})
    assert findings
    assert "nothing binds a merge" in findings[0]


# --------------------------------------------------------------------------
# Not measured is not a pass
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "ruleset",
    [
        pytest.param({"id": RULESET_ID}, id="no-key"),
        pytest.param({"id": RULESET_ID, "bypass_actors": None}, id="null"),
        pytest.param({"id": RULESET_ID, "bypass_actors": "none"}, id="not-a-list"),
        pytest.param(None, id="no-detail"),
    ],
)
def test_a_hidden_bypass_list_is_not_a_pass(ruleset: dict[str, Any] | None) -> None:
    """What GitHub returns to a token without write access: no bypass key at all."""
    rulesets = {} if ruleset is None else {RULESET_ID: ruleset}
    findings = ruleset_findings(_todays_rules(), rulesets)
    assert len(findings) == 1
    assert findings[0].startswith("not measured:")
    assert str(RULESET_ID) in findings[0]


def _no_gh_on_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Api:
    """The real `gh_api`, with a `PATH` that holds no `gh`."""
    monkeypatch.setenv("PATH", str(tmp_path))
    return gh_api


def _slow_gh_on_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Api:
    """The real `gh_api`, a `gh` that never answers, and a limit of one second."""
    gh = tmp_path / "gh"
    gh.write_text("#!/bin/sh\nexec /bin/sleep 5\n", encoding="utf-8")
    gh.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setitem(globals(), "GH_TIMEOUT_SECONDS", 1)
    return gh_api


def _failing(path: str, code: int, text: str) -> Api:
    answers = _todays_answers()
    answers[path] = (code, text)
    return _stub_api(answers)


@pytest.mark.parametrize(
    ("case", "step", "cause"),
    [
        pytest.param("no-gh", REPO_PATH, "gh is not installed", id="no-gh"),
        pytest.param("no-answer", REPO_PATH, "did not answer", id="no-answer"),
        pytest.param("exit-1", REPO_PATH, "gh auth login", id="exit-1"),
        pytest.param("not-json", REPO_PATH, "not JSON", id="not-json"),
        pytest.param(
            "empty-list-for-the-repository", REPO_PATH, "no default_branch", id="empty-list-for-the-repository"
        ),
        pytest.param("no-default-branch", REPO_PATH, "no default_branch", id="no-default-branch"),
        pytest.param("rules-exit-1", f"{REPO_PATH}/rules/branches/main", "HTTP 403", id="rules-exit-1"),
        pytest.param(
            "rules-exit-1-with-a-valid-answer",
            f"{REPO_PATH}/rules/branches/main",
            "exit 1",
            id="rules-exit-1-with-a-valid-answer",
        ),
        pytest.param(
            "rules-not-a-list", f"{REPO_PATH}/rules/branches/main", "not a list of rules", id="rules-not-a-list"
        ),
        pytest.param(
            "rules-with-a-string", f"{REPO_PATH}/rules/branches/main", "not a list of rules", id="rules-with-a-string"
        ),
        pytest.param("ruleset-exit-1", f"{REPO_PATH}/rulesets/{RULESET_ID}", "HTTP 404", id="ruleset-exit-1"),
        pytest.param("ruleset-not-json", f"{REPO_PATH}/rulesets/{RULESET_ID}", "not JSON", id="ruleset-not-json"),
        pytest.param("ruleset-a-list", f"{REPO_PATH}/rulesets/{RULESET_ID}", "not a ruleset", id="ruleset-a-list"),
    ],
)
def test_an_unreachable_api_is_not_a_pass(
    case: str, step: str, cause: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Every way the look can fail is one finding that names the step and the cause."""
    rules_path = f"{REPO_PATH}/rules/branches/main"
    ruleset_path = f"{REPO_PATH}/rulesets/{RULESET_ID}"
    apis: dict[str, Callable[[], Api]] = {
        "no-gh": lambda: _no_gh_on_path(monkeypatch, tmp_path),
        "no-answer": lambda: _slow_gh_on_path(monkeypatch, tmp_path),
        "exit-1": lambda: _failing(REPO_PATH, 1, "gh: To get started with GitHub CLI, run: gh auth login"),
        "not-json": lambda: _failing(REPO_PATH, 0, "<html>offline portal</html>"),
        "empty-list-for-the-repository": lambda: _failing(REPO_PATH, 0, "[]"),
        "no-default-branch": lambda: _failing(REPO_PATH, 0, json.dumps({"default_branch": ""})),
        "rules-exit-1": lambda: _failing(rules_path, 1, "HTTP 403"),
        "rules-exit-1-with-a-valid-answer": lambda: _failing(rules_path, 1, json.dumps(_todays_rules())),
        "rules-not-a-list": lambda: _failing(rules_path, 0, "{}"),
        "rules-with-a-string": lambda: _failing(rules_path, 0, '["deletion"]'),
        "ruleset-exit-1": lambda: _failing(ruleset_path, 1, "HTTP 404"),
        "ruleset-not-json": lambda: _failing(ruleset_path, 0, "not json"),
        "ruleset-a-list": lambda: _failing(ruleset_path, 0, "[]"),
    }
    findings = _measure(apis[case]())
    assert len(findings) == 1
    assert findings[0].startswith("not measured:")
    assert step in findings[0]
    assert cause in findings[0]


def test_the_measurement_goes_red_when_it_measured_another_repository() -> None:
    """`gh` fills `{owner}/{repo}` from `GH_REPO` or its default; another repository is not measured (F-4)."""
    calls: list[str] = []
    answers = _todays_answers()
    answers[REPO_PATH] = (0, json.dumps({"default_branch": "main", "full_name": "someone/else"}))
    findings = _measure(_stub_api(answers, calls))
    assert len(findings) == 1
    assert findings[0].startswith("not measured:")
    assert "someone/else" in findings[0]
    assert HERE in findings[0]
    assert calls == [REPO_PATH], "the rules of another repository must not be read"


def test_the_measurement_does_not_mind_the_case_of_the_repository_name() -> None:
    answers = _todays_answers()
    answers[REPO_PATH] = (0, json.dumps({"default_branch": "main", "full_name": HERE.upper()}))
    assert _measure(_stub_api(answers)) == []


@pytest.mark.parametrize("answer", [{"default_branch": "main"}, {"default_branch": "main", "full_name": ""}])
def test_an_answer_without_a_repository_name_is_not_measured(answer: dict[str, Any]) -> None:
    answers = _todays_answers()
    answers[REPO_PATH] = (0, json.dumps(answer))
    findings = _measure(_stub_api(answers))
    assert len(findings) == 1
    assert findings[0].startswith("not measured:")


def test_a_checkout_that_cannot_name_its_repository_is_not_measured() -> None:
    calls: list[str] = []
    findings = measure(_stub_api(_todays_answers(), calls), lambda: (None, "no origin"))
    assert len(findings) == 1
    assert findings[0].startswith("not measured:")
    assert "no origin" in findings[0]
    assert calls == [REPO_PATH]


@pytest.mark.parametrize(
    ("url", "name"),
    [
        pytest.param("https://github.com/Owner/Name.git", "Owner/Name", id="https-git"),
        pytest.param("https://github.com/Owner/Name", "Owner/Name", id="https"),
        pytest.param("https://github.com/Owner/Name/", "Owner/Name", id="https-slash"),
        pytest.param("https://user:token@github.com/Owner/Name.git", "Owner/Name", id="https-userinfo"),
        pytest.param("git@github.com:Owner/Name.git", "Owner/Name", id="scp-like"),
        pytest.param("ssh://git@github.com/Owner/Name.git", "Owner/Name", id="ssh"),
        pytest.param("ssh://git@github.com:22/Owner/Name.git", "Owner/Name", id="ssh-port"),
        pytest.param("https://git.example.org/group/Owner/Name.git", "Owner/Name", id="nested-path"),
    ],
)
def test_the_checkout_names_its_repository_by_its_origin(url: str, name: str, tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "remote", "add", "origin", url], check=True)
    assert local_repository(tmp_path) == (name, "")


@pytest.mark.parametrize("url", [None, "name-only"])
def test_a_checkout_without_a_readable_origin_names_no_repository(url: str | None, tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    if url:
        subprocess.run(["git", "-C", str(tmp_path), "remote", "add", "origin", url], check=True)
    name, reason = local_repository(tmp_path)
    assert name is None
    assert reason


def test_a_missing_gh_says_so(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Without `gh` the message names the cause, so `make verify` offline reads clearly."""
    assert _no_gh_on_path(monkeypatch, tmp_path)(REPO_PATH) == (127, "gh is not installed")


# --------------------------------------------------------------------------
# The live check and its gate
# --------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get(LIVE_ENV) != "1",
    reason="reads GitHub; runs in the gate ruleset on a writer machine (decisions/gates.yaml)",
)
def test_master_has_a_ruleset_with_required_checks() -> None:
    """The live ruleset of the default branch holds the six requirements.

    The name `master` is the one RB-M6 has carried since 1.0.0; the branch is
    whatever the API calls the default.
    """
    findings = measure()
    message = "\n".join(findings)
    if any(f.startswith("not measured:") for f in findings):
        message += (
            "\nThe gate `ruleset` needs network and a `gh` login on this machine; "
            "not measured is red, never green (RB-M6)."
        )
    assert not findings, message


def _run_the_live_test(*, variable: bool, path: str) -> subprocess.CompletedProcess[str]:
    """Run only the live test in a pytest of its own, with `path` as `PATH`."""
    env = {k: v for k, v in os.environ.items() if k != LIVE_ENV}
    env["PATH"] = path
    if variable:
        env[LIVE_ENV] = "1"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks",
            "-q",
            "-rs",
            "-p",
            "no:cacheprovider",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


def _assertion_message(output: str) -> str:
    """The failure message of the run: pytest's `E` lines, not the source it prints.

    The traceback shows the line that appends the hint as source, so a search of
    the whole output finds the hint's words even when the hint is never appended
    (F-7). Only the lines that begin `E` carry what the assertion said.
    """
    return "\n".join(line for line in output.splitlines() if line.startswith("E"))


def test_the_assertion_message_is_read_from_the_e_lines_only() -> None:
    output = (
        "    message += 'a hint, as source'\n>   assert not findings, message\nE   AssertionError: said this\nE   more"
    )
    assert _assertion_message(output) == "E   AssertionError: said this\nE   more"


def test_the_live_check_goes_red_without_gh_when_the_gate_turns_it_on(tmp_path: Path) -> None:
    """With the variable set and no `gh`, the live check fails — it neither skips nor passes."""
    done = _run_the_live_test(variable=True, path=str(tmp_path))
    assert done.returncode == 1, done.stdout + done.stderr
    message = _assertion_message(done.stdout)
    assert "not measured:" in message
    assert "needs network and a `gh` login" in message
    assert "skipped" not in done.stdout


def test_the_live_check_calls_nothing_without_the_variable(tmp_path: Path) -> None:
    """Without the variable the live check is skipped, names the gate, and never calls `gh`."""
    log = tmp_path / "calls.log"
    gh = tmp_path / "gh"
    gh.write_text(f'#!/bin/sh\necho "$@" >> "{log}"\nexit 1\n', encoding="utf-8")
    gh.chmod(0o755)
    done = _run_the_live_test(variable=False, path=str(tmp_path))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 skipped" in done.stdout
    assert "gate ruleset" in done.stdout
    assert not log.exists(), "gh was called without the variable"


def _the_ruleset_gate() -> dict[str, Any]:
    gates = yaml.safe_load(GATES.read_text(encoding="utf-8"))["gates"]
    found = [g for g in gates if g.get("id") == "ruleset"]
    assert len(found) == 1, "decisions/gates.yaml must hold exactly one gate `ruleset`"
    return found[0]


LIVE_TEST = "tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks"

# Run in a pytest of its own with the gate's arguments: which tests would run,
# after every `-k`, `-m`, `--deselect` and `--ignore` of the command, and
# whether the run is only a collection. Written as a plugin so the answer does
# not depend on how verbose the arguments make pytest's own listing.
_WHAT_WOULD_RUN = """
import json, sys
import pytest

class Plugin:
    ids, dry = [], False
    def pytest_runtestloop(self, session):
        option = session.config.option
        self.ids = [item.nodeid for item in session.items]
        self.dry = bool(option.collectonly or option.setuponly or option.setupplan)
        return True

plugin = Plugin()
pytest.main(sys.argv[1:], plugins=[plugin])
print("WOULD-RUN " + json.dumps({"ids": plugin.ids, "dry": plugin.dry}))
"""


@functools.cache
def _what_would_run(arguments: tuple[str, ...], env: tuple[tuple[str, str], ...]) -> dict[str, Any] | str:
    """The tests a pytest with these arguments and variables would run, or why it would not start."""
    done = subprocess.run(
        [sys.executable, "-c", _WHAT_WOULD_RUN, "-q", "-p", "no:cacheprovider", *arguments],
        cwd=REPO_ROOT,
        env={**os.environ, **dict(env)},
        capture_output=True,
        text=True,
        timeout=120,
    )
    lines = [line for line in done.stdout.splitlines() if line.startswith("WOULD-RUN ")]
    if not lines:
        return " ".join((done.stdout + done.stderr).split())[-300:] or "no output"
    return json.loads(lines[-1].removeprefix("WOULD-RUN "))


def _command_findings(command: str) -> list[str]:
    """Does this gate command actually run the live test?

    Not "does it start with the right words": a suffix such as `-k "not master"`,
    a `--deselect`, a `--collect-only`, another file or a swallowed exit code
    switches the live check off with every other test green (F-5). The command
    must be `NAME=value … python3 -m pytest …` with nothing around it, set
    `RULESET_ASSERT=1`, and a pytest started with its arguments and variables
    must select the live test and run it.
    """
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError as error:
        return [f"command cannot be read: {error}"]
    env: dict[str, str] = {}
    while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
        name, _, value = tokens.pop(0).partition("=")
        env[name] = value
    findings: list[str] = []
    if env.get(LIVE_ENV) != "1":
        findings.append(f"command must set {LIVE_ENV}=1 in front of pytest")
    if tokens[:3] != ["python3", "-m", "pytest"]:
        findings.append("command must run `python3 -m pytest …` and nothing else")
    if any(set(t) <= set("();<>|&") or "`" in t or t.startswith("$(") for t in tokens):
        findings.append("command must not chain, redirect or substitute: an exit code could be swallowed")
    if findings:
        return findings
    would = _what_would_run(tuple(tokens[3:]), tuple(sorted(env.items())))
    if isinstance(would, str):
        return [f"pytest does not start with the command's arguments: {would}"]
    if would["dry"]:
        findings.append("command only collects or sets up; it runs no test")
    if LIVE_TEST not in would["ids"]:
        findings.append(f"command does not run `{LIVE_TEST}`")
    return findings


def _gate_findings(gate: dict[str, Any]) -> list[str]:
    """What is wrong with how a gate turns the live check on."""
    findings = _command_findings(str(gate.get("command", "")))
    for key, want in (("job", "verify"), ("enforcement", "block"), ("placement", "writer"), ("floor", False)):
        if gate.get(key) != want:
            findings.append(f"{key} must be {want!r}, is {gate.get(key)!r}")
    return findings


def test_the_ruleset_gate_turns_the_live_check_on() -> None:
    """The variable the file reads is the one the gate sets, on the writer machine."""
    assert _gate_findings(_the_ruleset_gate()) == []


@pytest.mark.parametrize(
    ("key", "value"),
    [
        pytest.param("command", "RULESET_CHECK=1 python3 -m pytest tests/test_repo_settings.py -q", id="variable"),
        pytest.param("command", "python3 -m pytest tests/test_repo_settings.py -q", id="no-variable"),
        pytest.param(
            "command", f"{LIVE_ENV}=0 python3 -m pytest tests/test_repo_settings.py -q -rs", id="variable-off"
        ),
        pytest.param(
            "command",
            f'{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs -k "not master"',
            id="k-suffix",
        ),
        pytest.param(
            "command",
            f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs --deselect {LIVE_TEST}",
            id="deselect",
        ),
        pytest.param(
            "command",
            f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs --deselect tests/test_repo_settings.py",
            id="deselect-the-file",
        ),
        pytest.param(
            "command",
            f'{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs -m "no_such_marker"',
            id="marker",
        ),
        pytest.param(
            "command",
            f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs --collect-only",
            id="collect-only",
        ),
        pytest.param("command", f"{LIVE_ENV}=1 python3 -m pytest tests/test_ci.py -q -rs", id="another-file"),
        pytest.param(
            "command",
            f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py::test_todays_ruleset_holds -q -rs",
            id="another-test",
        ),
        pytest.param(
            "command", f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs || true", id="swallowed-exit"
        ),
        pytest.param(
            "command",
            f"""PYTEST_ADDOPTS='-k "not master"' {LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs""",
            id="addopts-in-front",
        ),
        pytest.param(
            "command", f"{LIVE_ENV}=1 python -m pytest tests/test_repo_settings.py -q -rs", id="another-interpreter"
        ),
        pytest.param("placement", "both", id="placement"),
        pytest.param("enforcement", "report", id="enforcement"),
        pytest.param("job", "drift", id="job"),
        pytest.param("floor", True, id="floor"),
    ],
)
def test_the_ruleset_gate_check_goes_red_when_the_gate_drifts(key: str, value: Any) -> None:
    gate = copy.deepcopy(_the_ruleset_gate())
    gate[key] = value
    assert _gate_findings(gate)


@pytest.mark.parametrize(
    "command",
    [
        pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs", id="the-gate-as-it-is"),
        pytest.param(f"{LIVE_ENV}=1 python3 -m pytest {LIVE_TEST} -q", id="the-live-test-alone"),
        pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -k master", id="selected-by-name"),
        pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests -q -x", id="the-whole-suite"),
    ],
)
def test_the_gate_command_may_run_the_live_test_in_other_ways(command: str) -> None:
    """The tie asks whether the live test runs, not whether the words are the usual ones."""
    assert _command_findings(command) == []


@pytest.mark.parametrize(
    "tail", ["|| true", "; true", "&& true", "| tee /dev/null", "> /dev/null", "$(true)", "`true`"]
)
def test_the_gate_command_goes_red_when_it_chains_or_redirects(tail: str) -> None:
    """The live test would run, but a trailing `|| true` swallows its exit code: that is named, not a side effect."""
    findings = _command_findings(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs {tail}")
    assert any("must not chain" in f for f in findings), findings
