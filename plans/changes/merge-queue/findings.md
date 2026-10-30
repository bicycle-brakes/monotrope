---
title: "Findings — merge-queue"
category: findings
status: draft
implementation_status: none
date: 2026-10-30
created: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-eh42
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — merge-queue

Stage-2 call, 2026-10-30: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 774 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 777 files, 2765 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/merge-queue/plan.md` +5 -5
> - `tests/test_ci.py` +159 -2
> - `tests/test_repo_settings.py` +226 -9
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> >               if rule.get("ruleset_id") not in ids:
> E               AttributeError: 'str' object has no attribute 'get'
>
> tests/test_repo_settings.py:247: AttributeError
> ______ test_queue_supplier_is_measured_without_bypass[unreadable-detail] _______
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/merge-queue/.venv/bin/python3
>
> detail = None, finding = 'not measured: ruleset 7 could not be read'
>
>     @pytest.mark.parametrize(
>         ("detail", "finding"),
>         [
>             pytest.param(
>                 _queue_ruleset(_QUEUE_BYPASS),
>                 f"ruleset {QUEUE_RULESET_ID} lets RepositoryRole 5 bypass it",
>                 id="bypass-actor",
>             ),
>             pytest.param(
>                 {"id": QUEUE_RULESET_ID},
>                 f"not measured: ruleset {QUEUE_RULESET_ID} shows no bypass list",
>                 id="no-key",
>             ),
>             pytest.param(
>                 {"id": QUEUE_RULESET_ID, "bypass_actors": None},
>                 f"not measured: ruleset {QUEUE_RULESET_ID} shows no bypass list",
>                 id="null",
>             ),
>             pytest.param(
>                 {"id": QUEUE_RULESET_ID, "bypass_actors": "none"},
>                 f"not measured: ruleset {QUEUE_RULESET_ID} shows no bypass list",
>                 id="not-a-list",
>             ),
>             pytest.param(None, f"not measured: ruleset {QUEUE_RULESET_ID} could not be read", id="unreadable-detail"),
>         ],
>     )
>     def test_queue_supplier_is_measured_without_bypass(detail: dict[str, Any] | None, finding: str) -> None:
>         """The queue's ruleset sits under the same fail-closed bypass measurement as every supplier's.
>     
>         Fault planted: a measurement that skips queue suppliers passes a separate
>         queue ruleset with bypass actors, a hidden list, or no readable detail.
>         """
>         rules = _rules_with_a_queue()
>         rulesets: dict[int, dict[str, Any] | None] = {RULESET_ID: _todays_ruleset(), QUEUE_RULESET_ID: detail}
> >       findings = ruleset_findings(rules, rulesets)
>
> tests/test_repo_settings.py:744: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_repo_settings.py:288: in ruleset_findings
>     for ruleset_id in _suppliers(rules):
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> rules = [{'ruleset_id': 24528176, 'type': 'deletion'}, {'ruleset_id': 24528176, 'type': 'non_fast_forward'}, {'parameters': {'...EN', 'max_pull_requests': 1, 'merge_method': 'MERGE', 'min_pull_requests': 1}, 'ruleset_id': 7, 'type': 'merge_queue'}]
>
>     def _suppliers(rules: list[dict[str, Any]]) -> list[Any]:
>         """The `ruleset_id` of every rule that supplies one of the six requirements, once each."""
>         ids: list[Any] = []
>         freshness = [*_up_to_date_rules(rules), *_merge_queue_rules(rules)]
>         for matching in [*_supplying_rules(rules).values(), *freshness]:
>             for rule in matching:
> >               if rule.get("ruleset_id") not in ids:
> E               AttributeError: 'str' object has no attribute 'get'
>
> tests/test_repo_settings.py:247: AttributeError
> =========================== short test summary info ============================
> FAILED tests/test_repo_settings.py::test_merge_queue_supplies_freshness[strict-flag-removed]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-required-check]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-deletion]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-pull-request]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-force-push]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[unpinned-verify]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[supplier-bypass]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[failed-measurement]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[bypass-actor]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[not-a-list]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[no-key]
> FAILED tests/test_repo_settings.py::test_merge_queue_supplies_freshness[strict-false]
> FAILED tests/test_repo_settings.py::test_todays_ruleset_holds - AttributeErro...
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[null]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[unreadable-detail]
> 15 failed, 13 passed in 1.09s
> ```

Stage-2 call, 2026-10-30: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 777 files, 2769 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_repo_settings.py` +5 -5
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E               AttributeError: 'str' object has no attribute 'get'
>
> tests/test_repo_settings.py:247: AttributeError
> __________ test_queue_supplier_is_measured_without_bypass[not-a-list] __________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/merge-queue/.venv/bin/python3
>
> detail = {'bypass_actors': 'none', 'id': 7}
> finding = 'not measured: ruleset 7 shows no bypass list'
>
>     @pytest.mark.parametrize(
>         ("detail", "finding"),
>         [
>             pytest.param(
>                 _queue_ruleset(_QUEUE_BYPASS),
>                 f"ruleset {QUEUE_RULESET_ID} lets RepositoryRole 5 bypass it",
>                 id="bypass-actor",
>             ),
>             pytest.param(
>                 {"id": QUEUE_RULESET_ID},
>                 f"not measured: ruleset {QUEUE_RULESET_ID} shows no bypass list",
>                 id="no-key",
>             ),
>             pytest.param(
>                 {"id": QUEUE_RULESET_ID, "bypass_actors": None},
>                 f"not measured: ruleset {QUEUE_RULESET_ID} shows no bypass list",
>                 id="null",
>             ),
>             pytest.param(
>                 {"id": QUEUE_RULESET_ID, "bypass_actors": "none"},
>                 f"not measured: ruleset {QUEUE_RULESET_ID} shows no bypass list",
>                 id="not-a-list",
>             ),
>             pytest.param(None, f"not measured: ruleset {QUEUE_RULESET_ID} could not be read", id="unreadable-detail"),
>         ],
>     )
>     def test_queue_supplier_is_measured_without_bypass(detail: dict[str, Any] | None, finding: str) -> None:
>         """The queue's ruleset sits under the same fail-closed bypass measurement as every supplier's.
>     
>         Fault planted: a measurement that skips queue suppliers passes a separate
>         queue ruleset with bypass actors, a hidden list, or no readable detail.
>         """
>         rules = _rules_with_a_queue()
>         rulesets: dict[int, dict[str, Any] | None] = {RULESET_ID: _todays_ruleset(), QUEUE_RULESET_ID: detail}
> >       findings = ruleset_findings(rules, rulesets)
>
> tests/test_repo_settings.py:744: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_repo_settings.py:288: in ruleset_findings
>     for ruleset_id in _suppliers(rules):
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> rules = [{'ruleset_id': 24528176, 'type': 'deletion'}, {'ruleset_id': 24528176, 'type': 'non_fast_forward'}, {'parameters': {'...EN', 'max_pull_requests': 1, 'merge_method': 'MERGE', 'min_pull_requests': 1}, 'ruleset_id': 7, 'type': 'merge_queue'}]
>
>     def _suppliers(rules: list[dict[str, Any]]) -> list[Any]:
>         """The `ruleset_id` of every rule that supplies one of the six requirements, once each."""
>         ids: list[Any] = []
>         freshness = [*_up_to_date_rules(rules), *_merge_queue_rules(rules)]
>         for matching in [*_supplying_rules(rules).values(), *freshness]:
>             for rule in matching:
> >               if rule.get("ruleset_id") not in ids:
> E               AttributeError: 'str' object has no attribute 'get'
>
> tests/test_repo_settings.py:247: AttributeError
> =========================== short test summary info ============================
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-deletion]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-required-check]
> FAILED tests/test_repo_settings.py::test_merge_queue_supplies_freshness[strict-flag-removed]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-force-push]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[unpinned-verify]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[no-pull-request]
> FAILED tests/test_repo_settings.py::test_merge_queue_supplies_freshness[strict-false]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[supplier-bypass]
> FAILED tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements[failed-measurement]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[bypass-actor]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[null]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[unreadable-detail]
> FAILED tests/test_repo_settings.py::test_todays_ruleset_holds - AttributeErro...
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[no-key]
> FAILED tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass[not-a-list]
> 15 failed, 13 passed in 2.47s
> ```

Stage-2 call, 2026-10-30: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 777 files, 2769 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 780 files, 2773 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 780 files, 2777 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model hy3 · leak check clean over 780 files, 2780 commits, 12 rules.
