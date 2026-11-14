---
title: "Plan — runner-clock"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-pph3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, runner, clock, flaky-tests]
---

# Plan — runner-clock

```text
For you:     Runner timing tests stop depending on machine load; execution limits and cleanup stay effective.
Done when:   One guarded clock boundary and deterministic timing tests pass, real cleanup checks remain, and make verify is green.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Larger timeouts, serial verification, a repository-wide clock service or changed admission rules.
Pre-mortem:  suppose it failed: most likely because a fake runner clock left the subprocess wait running on real time.
Starts unless you say stop.
```

## Scope and prerequisites

Baseline: `9140bfb6`, read on 2026-11-14. Implements criteria 1–6 of
`spec.md`; class `bounded`, no design phase or ADR. Q-1 is the maintainer's
scope decision. `findings.md` has only an attempt record, no phase-2a rows.
Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`; no Explore fallback is recorded. There is no plan template
in `templates/` at this baseline; this plan follows the phase-3 form and the
existing bounded-change plans.

## Build sequence

1. In `scripts/stage2.py`, add one `clock_now()` function returning a small
   immutable reading with monotonic seconds, UTC datetime and local date.
   Only its body reads `time.monotonic()`, `dt.datetime.now(dt.UTC)` and
   `dt.date.today()`. Keep the four public seams named in the spec as thin
   adapters: UTC dates derive from the UTC field; local stamps use the local
   field. Keep local date acquisition compatible with the existing
   `pinned_stamp_date` helper; do not replace local dates with UTC dates.
   Route all raw reads through these adapters, including `remaining`,
   `_review_round` and its nested expiry checks, discovery timestamps,
   retained-answer tokens, mirror names and document-stamp paths. All
   constants, deadline checks, exception paths and process operations stay.
2. In `tests/test_stage2.py`, extend `FakeClock` to replace `clock_now`,
   return separate wall/monotonic/local-date values and advance explicitly;
   retain its existing constructor and `after` behavior for accounting tests.
   Do not monkeypatch the shared standard-library `time` module. Add
   test-local process doubles at the runner's `Popen`/communication boundary:
   record the timeout actually supplied, advance fake time and return output
   or raise `subprocess.TimeoutExpired` according to that timeout. Model
   bounded cleanup communication separately. Use fake PIDs and intercepted
   group operations only together, so no simulated PID reaches `os.killpg`.
   Keep the real `launch` logic in tests of timeout translation and cleanup.
3. Rewrite `test_verification_admission_is_outside_execution_timeout` with
   a fake admission context that advances the clock well beyond the step
   limit before yielding, then a fake process completing within the full
   execution allowance. Assert the passed allowance and success; run an
   over-budget outcome and assert the repairable timeout diagnostic. Remove
   its real holder, thread, sleeps and short real timeout. Convert
   `test_local_checks_preserve_nested_admission` to controlled admission
   with the existing holder/token records and environment assertions; retain
   a real child/token integration test separately. Remove `_real_holder`
   and `_holder_acquired` if they then have no callers.
4. Convert all remaining policy timing tests, starting with this census:
   `test_the_remaining_time_never_outlives_the_round_deadline`,
   `test_a_hanging_runner_step_aborts_with_its_limit_named`,
   `test_a_call_over_the_time_limit_is_stopped`, the timeout branch of
   `test_free_discovery_forces_live_refresh_before_listing`,
   `test_a_replacement_the_deadline_stopped_is_not_consumed`, and
   `test_a_deadline_stop_names_the_round_limit`. Advance at admission,
   prompt-check and process-response boundaries, asserting before/at/after
   expiry where relevant. Migrate the existing fake-time expiry tests
   `test_no_second_call_after_the_round_deadline`,
   `test_a_round_failed_past_the_deadline_names_the_skipped_retry`,
   `test_an_expired_round_starts_no_replacement_and_consumes_no_stage` and
   `test_a_replacement_admitted_after_the_deadline_is_not_started` off their
   patches of `stage2.time`. Preserve assertions about no call, audit and
   consumed stages. Find any additional short-limit cases by reading all
   `sleep`, timeout, deadline, barrier and elapsed-time uses in this test file;
   the census is a starting point, not an exemption list. The absent second
   test named in Q-1 is reconciled if present after synchronizing before merge;
   no missing behavior is invented from its name.
5. Split deterministic timeout policy from operating-system lifecycle evidence.
   For `test_both_swarms_run_in_parallel_as_one_round`, prove concurrent entry
   with thread events/barriers, retaining round and row assertions; remove
   the less-than-15-second comparison and sleeping subprocess barrier.
   Inject `TimeoutExpired` after an explicit readiness handshake for real
   cleanup tests instead of racing child startup against a one-second timer.
   In `test_a_timeout_kills_the_whole_process_group`,
   `test_a_timeout_does_not_wait_for_an_escaped_descendant`,
   `test_an_interrupt_on_the_main_thread_kills_the_launched_group`, the
   three interruption/signal tests using `_interrupting_verb`,
   `test_a_signal_during_process_creation_leaves_no_child` and
   `test_a_timed_launch_ends_a_lingering_grandchild_before_returning`, replace
   short elapsed-time verdicts and natural-sleep completion with explicit
   readiness, kill/reap or observable liveness evidence. Keep fake-clock
   assertions of timeout/drain arguments alongside the real lifecycle checks.
   A watchdog only prevents a stuck test: document that role, clean all
   children in `finally`, and do not assert scheduler speed. Never advance
   only a fake clock and expect a real child or `communicate` to accelerate.
6. Add the source guard with an AST visitor: resolve `time`/`datetime`
   imports and direct imported aliases, inspect nested functions and
   module-level expressions, permit raw acquisition only in the exact
   `clock_now` body, and reject raw sleep everywhere else. No caller or line
   exemptions. Parse source strings in parametrized guard self-tests,
   including aliased imports, assigned clock aliases, nested bypasses,
   module-level reads, nanosecond/CPU clocks, no-argument `time.localtime`,
   `gmtime`/`ctime` and wall-date APIs, including `datetime.today`; allow pure
   datetime construction/parsing and boundary calls. Prove separate wall,
   monotonic and local-date meanings, a wall-clock jump and existing pins.
7. Run the checks below, clear ledger promises only when their tests exist,
   and record measured phase-4 time. The runner performs the final full
   verification, refreshes derived metadata and commits; the attempt does
   not commit held paths.

## Files and ownership

- `scripts/stage2.py` — implementation attempt: the single clock boundary
  and routing of existing time/date reads; no timeout-policy changes.
- `tests/test_stage2.py` — implementation attempt: clock and process doubles,
  source guard and its fault cases, timing-test conversion and retained real
  lifecycle evidence.
- `plans/changes/runner-clock/spec.md` — implementation status only; criteria stay fixed.
- `plans/changes/runner-clock/plan.md` — phase-4 time and criterion-ledger progress.
- `plans/changes/runner-clock/findings.md` — runner/orchestrator-owned review evidence.
- `plans/INDEX.md` — runner-owned regeneration after artifact/status changes.

No deletions of files and no held-path edits are planned. If a held path
unexpectedly proves necessary, assign it to the orchestrator as a bootstrap
edit after the accepted attempt, never to the implementation attempt.
Do not touch the independent production components and admission tests named
in the spec, other change folders, the tracker, runtime configuration,
prompts, templates or governance files.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'clock or deadline or timeout or time_limit or admission or discovery_forces_live_refresh or swarms_run_in_parallel or interrupted_runner or terminated_runner or hangup_or_quit or interrupt_on_the_main_thread or signal_during_process_creation or lingering_grandchild or runner_logs or runner_time'
.venv/bin/python3 -m pytest tests/test_stage2.py -q -n auto
python3 scripts/check_interview_minimums.py --change runner-clock
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

The first run is serial policy/lifecycle evidence; the second checks the entire
runner test file under the suite's parallel mode. Guard self-tests must turn
red on planted bypasses; the real lifecycle checks must still fail if group
cleanup is disabled. Do not add a dependency on machine-load thresholds.
`scripts/validate_change_artefacts.py` is absent at the baseline: its prompt
command cannot be reported green; use the present interview, ledger and
registry gates, followed by the runner's full verification.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_runner_clock_is_the_only_time_source — a runner time/date read bypasses the clock boundary
- 2: not yet written tests/test_stage2.py::test_runner_clock_guard_rejects_bypasses — a planted direct or aliased acquisition outside the boundary is accepted
- 2: not yet written tests/test_stage2.py::test_runner_clock_guard_accepts_the_boundary — the guard rejects the designated backend or pure date operations
- 3: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout — queueing reduces execution allowance or an over-budget check succeeds
- 4: tests/test_stage2.py::test_the_remaining_time_never_outlives_the_round_deadline — the exact fake-clock remaining budget or expiry is wrong
- 4: tests/test_stage2.py::test_local_checks_preserve_nested_admission — inherited admission is lost or the test still needs a real holder
- 4: tests/test_stage2.py::test_a_call_over_the_time_limit_is_stopped — simulated expiry fails to stop a reviewer
- 4: tests/test_stage2.py::test_free_discovery_forces_live_refresh_before_listing — discovery proceeds after a simulated refresh timeout
- 4: tests/test_stage2.py::test_a_replacement_the_deadline_stopped_is_not_consumed — expired replacement is audited or consumed
- 4: tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit — simulated expiry reports the wrong limit
- 4: tests/test_stage2.py::test_both_swarms_run_in_parallel_as_one_round — one member waits for another to finish before entering
- 4: not a test — phase-6 review censuses all timing cases against the definition in the spec, including newly merged cases; any remaining real-time policy verdict fails criterion 4
- 5: not yet written tests/test_stage2.py::test_runner_clock_preserves_time_domains — a wall jump changes elapsed time or local/UTC dates are interchanged
- 5: tests/test_stage2.py::test_runner_time_entry_identifies_attempt_and_midnight_span — accounting changes its span or formatting semantics
- 5: tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current — a clock refactor breaks the existing local-date pin
- 6: tests/test_stage2.py::test_verify_step_limit_is_45_minutes — the default verification limit changes
- 6: tests/test_stage2.py::test_a_hanging_runner_step_aborts_with_its_limit_named — timeout translation loses the execution-limit diagnostic
- 6: tests/test_stage2.py::test_a_timeout_kills_the_whole_process_group — a timed-out group's descendant survives
- 6: tests/test_stage2.py::test_a_timeout_does_not_wait_for_an_escaped_descendant — the post-kill drain is unbounded
- 6: tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group — cancellation leaves a live child
- 6: tests/test_stage2.py::test_a_runner_check_hands_its_child_the_admission_token — a real child loses its inherited admission

## Time used

2026-11-14 18:40:12–18:45:22 UTC, 310 s — draft · attempt 1 · route codex · model gpt-6.1-sol · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
