---
title: "Plan — targeted-check-more-verbs"
status: draft
implementation_status: none
date: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-0swp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, model: gpt-6.1-sol, version: "2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, verification]
---

# Plan — targeted-check-more-verbs

```text
For you:     Implement and draft checks avoid unnecessary full-run waits; missing tests fail early and local misses are counted.
Done when:   Routing, import-chain, refusal and slip-count regressions pass; full phase-6 and CI gates remain intact and make verify is green.
Appetite:    Seven and a half hours (raised from six by the maintainer on 2026-11-12, decisions.md#Q-6) of phase 4 including repairs; stop at the limit under the existing appetite protocol.
Not now:     Splitting the runner, coverage instrumentation, smaller CI, admission redesign or a dashboard.
Pre-mortem:  suppose it failed: most likely because the test-link graph misses an indirect dependency.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–13 of `spec.md` from maintainer answers Q-1–Q-5;
retain class bounded. No design or new ADR draft is due: the orchestrator
amends the existing ADR 0025. Explore used route `flash`, endpoint
`glm-coding-plan`, model `glm-5.3-flash`, on 2026-11-10; no Stage-1 fallback
was recorded. The orchestrator shows the card unchanged before phase 4.
This drafting call writes artifacts only; the runner verifies and commits.

## Build sequence

1. Extend selection inside `scripts/stage2.py`, consuming separate current
   and baseline `touch_map.links()` graphs without changing the map's CLI.
   Reverse-traverse `imports` edges with a visited set, then collect `tests`
   edges to each reached node; do not traverse `runs`/`reads`. Union the two
   snapshots' independently computed closures for coverage of the entire
   baseline-to-attempt delta, never fabricate a chain across snapshots.
   Keep surviving whole test modules, touched tests, deterministic ordering,
   deleted/renamed-path coverage, and retained edits across retries.
2. For implement only, preflight all added production `.py`/`.sh` files
   against the current graph before cheap pytest or fallback admission.
   Report every proven uncovered new file with "add a test that reaches this
   file" and reject via existing retry diagnostics. A current untracked test
   may satisfy it; baseline-only, deleted or unreachable tests may not.
   This refusal precedes conservative fallback even in a mixed delta with
   shared infrastructure. Unreadable inventories cannot prove absence and
   retain full fallback; existing uncovered code and covered shell inputs
   also retain their existing full fallback. Do not run coverage tools.
3. Explicitly pass targeted mode from `implement()` on all model routes,
   retaining full defaults for other callers. Reuse `_targeted_body` and its
   preparation, document gates, gate enforcement, time limits and sanitized
   diagnostics. Keep every existing fallback, especially SHARED_INFRASTRUCTURE
   and whole `tests/test_stage2.py`; targeted red/timeout is a failed attempt,
   never an invitation to full fallback. Preserve repair proofs and all
   accepted-ledger, prior-red-test, held-path and checkpoint guards.
4. Factor shared gate selection/execution so `verify_draft()` requests only
   local `docs` gates from `ci_gates.gates()`, in registry order. Do not run
   the admitted `DOCS_VERIFY` shell command, pytest or the membership-triggered
   kit probe. Strip admission ownership/token/context from the child env;
   keep locked Python/PATH, timeouts, blocking/report behavior, derived
   preparation, tool checks, artifact/card/time-heading guards and the gate's
   own change-scoped missing-ADR-answer tolerance. Use exit status, not parsed
   prose, for gate verdicts. Share scope evidence for draft/implement/repair;
   keep failure evidence protected and success evidence in the checkpoint.
5. Extend `scripts/verify_duration.py` additively with validated targeted
   result and slip records in its existing `verify-duration.jsonl` store;
   preserve version-1 duration records and readers. A targeted result stores
   UTC, canonical repository/worktree, change/verb, unique check ID, selected
   tests/gates, outcome, gate-config digest and accepted checkpoint tree ID.
   Bind a green to that checkpoint only after the existing checkpoint guard
   proves verification inputs unchanged: allow only the runner's known audit,
   timing/lifecycle and derived-index bookkeeping, not arbitrary file edits.
   Store no raw output or credentials; reuse protected bounded identifiers.
6. At `require_fresh_full_verification`, associate the local full run's ID
   with its captured head/tree/config and outcome. Pass a runner-owned
   correlation ID through the existing full-check environment into duration
   records; use the existing per-gate records to identify blocking red gates,
   and extract bounded failed pytest IDs from protected failure evidence
   where available (otherwise null, never fabricated). Match the latest green
   targeted checkpoint tree/config of this repository; differing commits
   with identical trees may match, differing trees may not. Permit only the
   already-approved uncommitted findings audit difference of phase 6.
   On completed blocking red append one slip referencing both IDs. Keep
   timeouts, launch/admission failures and identity races unmeasured, and
   preserve the review stop and fresh full check on every invocation.
7. Serialize evidence with the existing safe append lock. Make deduplication
   by full-run ID atomic with checking/appending; preserve concurrent writes
   and diagnose storage gaps without changing gate verdicts. Add
   `python3 -m scripts.verify_duration slips --repository "$PWD" --since <UTC-ISO> --until <UTC-ISO>`
   to count distinct slip full-run IDs in the half-open UTC interval. Return
   explicit unavailable/incomplete measurement for missing, corrupt or
   incomplete correlation evidence, never a trustworthy zero from it.
8. Add regressions in the ledger using actual fixture trees and captured
   commands, not a mocked selector. Parameterize initial/retry/fallback
   routes, current/baseline links, chains/cycles, mixed-delta refusal,
   admission markers, red/timeout, identity mismatch and concurrent history.
   Adapt existing fixture full-check expectations and obsolete repair-only
   assertions while retaining test function names referenced by historical
   ledgers. Preserve existing unrelated histories and review boundary tests.
9. Orchestrator bootstrap, after the accepted attempt: amend ADR 0025 from
   the five recorded answers (retain historical acceptance; mark the new
   amendment proposed until merge), align held instructions and the workflow,
   and add the interval/count command to the handover skill. Defer the
   workflow prose edit to this same step so cross-file doctrine tests remain
   consistent during the attempt. Align doctrine
   assertions in `tests/test_stage2.py` and the new criterion-13 test only in
   this bootstrap step, so the attempt remains testable against current held
   text. The decision PR carries the amendment and lists the bead it changes;
   do not record an ADR answer. Re-run verification after bootstrap, before
   phase 6. Reinstall the display skill through `tools/claude-code/install.sh`
   in the orchestrator's authorised environment, not inside a model attempt.

### Correction for the fifth run (decisions.md#Q-6, 2026-11-12)

The fourth run's full check showed 13 red tests. Do this, nothing wider:

1. Remove the extra quote block `> Runner verification scope:` the code
   writes to findings.md after an attempt. A passing attempt's scope goes
   into the runner's time line in plan.md (after the verdict word), a failed
   attempt's scope stays one line inside its one diagnostics block. The
   eight tests that guard one audit line per passing attempt and one block
   per failed attempt must pass unchanged
   (`test_a_passing_attempt_leaves_only_its_audit_line`,
   `test_a_passing_attempt_that_was_formatted_leaves_only_its_audit_line`,
   `test_a_failed_attempt_quotes_its_diagnostics_below_its_audit_line`,
   `test_an_unmeasured_file_list_says_why_and_changes_nothing_else`,
   `test_a_failure_after_the_first_snapshot_says_why_and_changes_nothing_else`,
   `test_an_unmeasured_reason_stays_one_line_with_one_full_stop`,
   `test_a_malformed_numstat_record_says_not_measured_and_the_run_goes_on`).
2. Rewrite `tests/test_stage2_fail_fast.py::test_cheap_green_still_requires_full_verification`
   to the new rule: a targeted green checkpoints when the coverage is safe;
   the full check runs when it is not, and its red result still blocks.
3. `tests/test_stage2_fail_fast.py::test_empty_targets_skip_their_command`
   states a standing guarantee (a text-only attempt starts neither ruff nor
   pytest). Find why ruff is started now and repair the code, not the test.
4. Adapt only the fixtures of
   `test_ruff_gets_the_verify_environment_without_credentials`,
   `test_runner_preserves_precall_time_on_final_verdict` and
   `test_a_bash_call_beside_the_document_check_runs_the_real_bash` to the
   route the attempt now takes; what each asserts stays.

5. Sixth run (2026-11-12): one test is left red,
   `tests/test_stage2.py::test_a_bash_call_beside_the_document_check_runs_the_real_bash`.
   Its last assertion guards the test stand-in itself: a step scripted under
   the key `bash` must end the stand-in with status 97 and "not served" on
   standard error instead of being dropped silently. The attempts removed
   that guard from the bash stand-in together with its document-check
   branch. Put the guard back in the stand-in (the document-check branch
   stays removed); do not change the test's assertions.

## Files and ownership

- Attempt: `scripts/stage2.py` — extend selection, early refusal, implement/draft dispatch, scope evidence and local-slip correlation; align embedded verification instructions.
- Attempt: `scripts/verify_duration.py` — add compatible safe evidence writes, correlation/deduplication and the interval-count reader.
- Attempt, then orchestrator: `tests/test_stage2.py` — behavioral regressions and fixture updates first; doctrine assertions after bootstrap.
- Attempt: `tests/test_verify_duration.py` — correlation records, counts, legacy compatibility, concurrent deduplication and unsafe/unavailable storage cases.
- Orchestrator bootstrap: `docs/WORKFLOW.md` — document targeted implement/repair, unlocked draft documents, conservative fallback, missing-test refusal, local slips and unchanged full gates alongside held prose and its doctrine tests.
- Attempt: `plans/changes/targeted-check-more-verbs/spec.md` — lifecycle metadata only; retain criteria and decisions.
- Attempt: `plans/changes/targeted-check-more-verbs/plan.md` — clear written-test markers and let the runner populate measured time.
- Runner: `plans/changes/targeted-check-more-verbs/findings.md` — audit/check-scope evidence and subsequent reviews.
- Runner: `plans/INDEX.md` — derived registry refresh.
- Orchestrator only: `docs/adr/0025-targeted-check-after-repair.md` — proposed amendment covering the five answers; preserve prior history.
- Orchestrator only: `AGENTS.md` — align the summary of post-run checks and final full verification.
- Orchestrator only: `prompts/04-implement.md` — align runner post-check and missing-test instructions while retaining interactive-session duties.
- Orchestrator only: `prompts/04b-review-loop.md` — align selection/fallback wording and retain the fresh full phase-6 boundary.
- Orchestrator only: `tools/claude-code/skills/handover/SKILL.md` — require the locally measured slip count, repository and interval, or explicit unavailability, in the night report.

No files are deleted and no new code module is needed. Do not edit
`scripts/touch_map.py`, `scripts/verify_lock.py`, `scripts/verify_all.sh`,
gate/model declarations, generated CI, tracker data, other change artifacts
or any other held path. In particular, do not rename historical ledger tests
or relax the runner/monolithic-test fallback to speed up this change's own
implementation: this change itself still requires full verification.

## Verification

At baseline `e635f03b`, neither `templates/plan.md` nor
`scripts/validate_change_artefacts.py` exists. Use the phase-3 form and existing
gates; do not create substitute infrastructure. The runner owns index refresh,
full verification and commit. Before phase-4 full verification, the worktree
needs its one-time `make venv` and `bash tools/pi/install.sh` setup. Run:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_verify_duration.py tests/test_touch_map.py tests/test_ci.py -q
.venv/bin/python3 -m ruff check scripts/stage2.py scripts/verify_duration.py tests/test_stage2.py tests/test_verify_duration.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py scripts/verify_duration.py tests/test_stage2.py tests/test_verify_duration.py
python3 scripts/check_interview_minimums.py --change targeted-check-more-verbs
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py
python3 scripts/plans_registry.py --check
make verify
```

Use isolated temporary history for the green-targeted/red-full integration
case and count it through the new CLI; do not alter the user's shared log.
The full phase-6 check and hosted full CI remain additional boundaries.

Draft validation on 2026-11-11 at baseline `e635f03b`: interview minimums,
criterion ledger and research handoff passed. Registry/index preparation and
full verification remain the runner's work after this draft.

## Criterion ledger

- 1: tests/test_stage2.py::test_implement_routes_use_targeted_postchecks — a covered initial/retry/fallback attempt invokes make verify
- 2: tests/test_stage2.py::test_draft_document_projection_runs_unadmitted — a held admission delays the draft, a marker leaks, or selection includes code gates
- 3: tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards — an existing preparation, tolerance or acceptance guard is bypassed
- 4: tests/test_stage2.py::test_targeted_selection_follows_import_chains_per_snapshot — a chain, cycle, retained retry edit or deleted/renamed endpoint loses a whole test file
- 5: tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback — uncovered Python/shell code reaches pytest, admission or a checkpoint
- 6: tests/test_stage2.py::test_targeted_repair_falls_back_to_full_on_uncovered_inputs — unsupported or unsafe coverage gets targeted acceptance
- 6: tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification — the monolithic test file runs outside full admission
- 6: tests/test_stage2.py::test_implement_preserves_full_fallback_boundaries — an implement route bypasses shared-infrastructure or unsafe-inventory fallback
- 7: tests/test_stage2.py::test_extended_targeted_failures_never_checkpoint — red, launch failure or timeout is overridden instead of failing the attempt
- 8: tests/test_stage2.py::test_all_targeted_verbs_record_actual_scope — scope is absent or document/targeted green claims a full pass
- 9: tests/test_stage2.py::test_review_requires_fresh_full_verification_before_model_call — stale, moved or red input reaches a reviewer
- 9: tests/test_ci.py::test_the_trigger_does_not_restrict_paths — a changed path ceases to trigger hosted verification
- 9: not a test — review the unchanged hosted workflow against the complete gate list; any reduction of CI verification refutes criterion 9
- 10: tests/test_stage2.py::test_phase6_records_only_correlated_local_slips — a matching completed red is missed, or a different tree/configuration or timeout is counted
- 11: tests/test_verify_duration.py::test_targeted_history_preserves_safety_and_legacy_records — new events break old records, expose raw output, mix concurrent writes or change verdicts on storage failure
- 12: tests/test_verify_duration.py::test_slip_report_counts_interval_and_reports_gaps — duplicate runs or other repositories are counted, or corrupt/incomplete evidence becomes zero
- 12: not a test — orchestrator review of the handover skill's count command and explicit repository/interval/unavailable wording; omission refutes criterion 12
- 13: tests/test_stage2.py::test_verification_doctrine_covers_extended_targeted_routes — workflow, held instructions or the ADR contradict the agreed verification boundaries; orchestrator bootstrap owns this test

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: fourth run from attempt 3's saved state on the maintainer's answer of 2026-11-12 (bead coding-harness-0swp); three tests still red: test_implement_refuses_uncovered_new_code_before_tests_or_fallback[baseline-only-test], test_secret_rules_outside_diagnostics_still_block_retry, test_targeted_history_preserves_safety_and_legacy_records.

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: fifth run from attempt 4's saved state with the correction of decisions.md Q-6 (maintainer 2026-11-12, bead coding-harness-0swp): follow the plan section 'Correction for the fifth run'.

## Time used

2026-11-11 20:50:58–23:23:11 UTC, 9132 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-11 23:23:22–2026-11-12 00:07:48 UTC, 2666 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-12 00:08:25–01:04:53 UTC, 3387 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 11:30:43–12:27:43 UTC, 3420 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 13:48:20–13:54:06 UTC, 346 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
