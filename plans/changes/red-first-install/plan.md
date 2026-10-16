---
title: "Plan — red-first-install"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-omp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, red-first]
---

# Plan — red-first-install

```text
For you:     A missing Pi installation can no longer certify a repair as red first.
Done when:   Assertion failures count, environment faults refuse, and the regression tests and make verify are green.
Appetite:    One hour of phase 4 including repairs; stop at the limit.
Not now:     Installing baseline dependencies, the test-only guard exception, or changing Pi and model settings.
Pre-mortem:  suppose it failed: most likely because a fixture error still looks like a test assertion in the outcome record.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–8 of `spec.md`; the bounded class needs no design or ADR.
This draft changes planning artifacts only; the orchestrator shows the card
unchanged before implementation and the runner owns verification and commits.
First coordinate the shared `red_first` function with the guard-test exception
change (`coding-harness-0ho`): land after it or rebase onto it, retaining its
eligibility policy. Its branch implementation was not read for this draft.
Phase 1 used route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash` on 2026-10-16; no Stage-1 fallback is recorded.

## Build sequence

1. Replace exit-code-only classification inside `red_first`. Keep the detached
   baseline checkout, copied attempted tests, interpreter preflight, timeout,
   credential scrubbing, cleanup and reference snapshots. Inject a small
   pytest plugin from a runner-owned string into the temporary checkout;
   load it explicitly with `-p`, without editing the attempted tests or
   relying on a plugin already installed in the baseline. Use a fresh private
   JSON report path per invocation, outside the copied tests, removed by the
   existing temporary-directory cleanup. Add no dependency or tracked module.
2. With a `pytest_runtest_makereport` hook wrapper, record node id, phase,
   final outcome, expected-result markers and whether `call.excinfo.value`
   is an `AssertionError`; inspect the final report after pytest's wrappers
   so xfail conversion is visible. Record collection failures and session
   completion/exit status too. Bind the report to the requested selector and
   a fresh invocation token. Treat a token or selector mismatch, invalid
   schema, missing phase, unreadable report or unfinished session as refusal.
3. Require actual process exit 1 and matching completed-session evidence,
   at least one selected ordinary assertion-failing call, passing setup and
   teardown for every selected case, and only passes or assertion failures
   among the remaining calls. Parameterized node ids must belong to the exact
   requested function. Reject every other outcome in criteria 2–6, including
   explicit `pytest.fail`, collection errors, skips, xfail and strict XPASS.
   Never infer success from terminal output or an exit code alone.
4. Return a scrubbed cause naming the test and exit code when available;
   preserve `check_repair_answer`'s finding-id prefix and failed-attempt
   handling. Update the `red_first` docstring and the existing baseline-green
   test's obsolete exit-1-or-2 diagnostic expectation; retain all existing
   top-level test names because other criterion ledgers reference them.
5. Add the ledger's tests in the existing repair section, using `repair_world`
   and direct `red_first` calls for real pytest outcomes. The missing-install
   test plants an ignored stand-in Pi dependency only in the source worktree,
   never committing it, and uses the existing `require_installed_pi`
   fixture failure shape (`pytest.fail`), and assert it is absent in the
   scratch fixture before failing. No network, npm install or real provider
   call is needed. Also run a repair with that failure through all attempts:
   assert no checkpoint, unchanged taken status and a contextual diagnostic.
   Use actual pytest subprocesses for outcome cases; intercept only report
   corruption, timeout and secret-bearing diagnostics for those fault tests.

## Files and limits

- `scripts/stage2.py`: add the temporary outcome probe and classifier within the red-first path, replacing its exit-only rule and stale docstring.
- `tests/test_stage2.py`: add the named regressions and update the existing baseline-green diagnostic assertion.
- `plans/changes/red-first-install/spec.md`: create the contract now and update implementation metadata when implementation progresses.
- `plans/changes/red-first-install/plan.md`: create this plan; replace not-yet-written ledger markers as tests land and record measured phase-4 time.
- `plans/changes/red-first-install/findings.md`: the runner appends review and execution evidence; this draft preserves its existing audit line.
- `plans/INDEX.md`: the runner regenerates the derived registry; this draft does not edit it.

No deletion is planned. Leave `research.md` and `decisions.md` intact;
no phase-2a rows are open in `findings.md` as read on 2026-10-16.
Do not touch the protected areas in `spec.md`, other change folders, workflow
prompts or test fixtures for the real Pi installation. No live pull-request
state was read; the local branch and its remote-tracking ref both point to
draft baseline `63f1511` as checked on 2026-10-16.

## Verification

In the implementation worktree run `make venv` once, then:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change red-first-install
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

The prompt's `python3 scripts/validate_change_artefacts.py --check` cannot run:
the script is absent at draft baseline `63f1511`. No plan template exists
under `templates/` at that baseline either, so this plan follows the phase-3
prompt and existing plan form. Do not create either missing file. The runner
owns index regeneration and the full verification; a tracker-dependent check
that cannot measure is reported as such, never as green.

Draft checks on 2026-10-16 at `63f1511` plus these artifacts: the interview
minimums and criterion ledger commands above passed. The artifact-validator
command exited 2 because its file is absent. The registry's frontmatter parser
checked both new headers locally; its full `--check` was not run because its
tracker reader can leave this worktree, outside this draft's read boundary.
Implementation tests and `make verify` remain the runner's next checks.

## Criterion ledger

- 1: tests/test_stage2.py::test_red_first_accepts_only_clean_assertion_runs — an ordinary or mixed-parameter assertion failure is refused
- 2: tests/test_stage2.py::test_red_first_refuses_a_missing_pi_install — the absent ignored installation produces accepted fixture-error evidence
- 3: tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors — a fixture assertion or teardown error passes the proof
- 4: tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures — RuntimeError, ImportError or pytest.fail counts as an assertion
- 5: tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes — pass, empty selection, collection failure, interruption, internal/usage error, skip, xfail or XPASS is accepted
- 6: tests/test_stage2.py::test_red_first_refuses_missing_or_invalid_evidence — absent, malformed, incomplete, wrong-test or stale evidence passes
- 6: tests/test_stage2.py::test_red_first_refuses_a_timed_out_run — a timed-out process is accepted through partial evidence
- 7: tests/test_stage2.py::test_repair_refuses_environment_only_red_first_evidence — a fixture fault checkpoints, fixes a row or lacks finding/test/cause context
- 7: tests/test_stage2.py::test_red_first_scrubs_outcome_diagnostics — a credential reaches a refusal diagnostic
- 8: tests/test_stage2.py::test_the_red_first_run_leaves_no_worktree_behind — a successful proof leaves a worktree or edits shared state
- 8: tests/test_stage2.py::test_a_ref_created_while_the_named_test_ran_fails_the_proof_and_is_never_deleted — a created reference escapes detection or is deleted
- 8: tests/test_stage2.py::test_an_existing_ref_moved_while_the_named_test_ran_fails_the_proof — a moved reference escapes detection
- 8: tests/test_stage2.py::test_a_failed_worktree_remove_leaves_no_dead_entry_and_is_named — a refused cleanup leaves a dead entry or lacks a diagnostic

## Runner route — 2026-10-16

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-10-16

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-16 span not measured: this session had no command tool, so `date` could not be read and no span is estimated.

2026-10-16, review-loop round 1 repair: three runner attempts (Codex, Codex, Sonnet) failed the post-run checks because a test-strength finding has no red-first form (bead coding-harness-y17); the orchestrator kept attempt 1's tests, checked each against its planted fault and completed the repair by hand, about 20 minutes (20:05-20:25).
