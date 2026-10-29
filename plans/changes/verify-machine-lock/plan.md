---
title: "Plan — verify-machine-lock"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-p6mu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification]
---

# Plan — `verify-machine-lock`

```text
For you:     Local verification queues across worktrees and checks free memory before starting.
Done when:   Isolated contention, nesting, memory and timeout regressions pass, and make verify is green.
Appetite:    Three hours of phase 4, including repair rounds; stop when used.
Not now:     Hand-run make test, foreign-model throttling, or continuous memory monitoring.
Pre-mortem:  suppose it failed: most likely because a nested check lost its inherited ownership marker.
Starts unless you say stop.
```

## Approach and files

This is bounded; no design or ADR is due. Implement one reusable admission
context, with a command-line supervisor for the shell entry. Exploration ran
through Stage 2, GLM 5.3 Flash (`glm-coding-plan`, 2026-10-28); no Stage-1
fallback was recorded. Basis: `spec.md` and the unchanged `decisions.md`.

1. Create `scripts/verify_lock.py`: standard-library admission, memory probe,
   live ownership validation and command supervisor; use the same context in
   the runner rather than a second implementation.
2. Change `scripts/verify_all.sh`: after interpreter/argument selection and the
   `--list` exit, use `"$PYTHON" -m scripts.verify_lock --held` to recognize
   valid nesting; otherwise exec its command supervisor with Bash, the runner
   path and original arguments. The supervisor publishes its marker to the
   child; re-entry then reaches the unchanged gate loop. Module invocation
   preserves the existing negative pin against direct gate-script calls.
3. Change `scripts/stage2.py`: acquire admission immediately before the timed
   launches in `verify_attempt`, `verify_draft`, `red_first` and
   `fixed_test_proof` (including the pytest import probe); supply the marker
   only to local children. Build the shared state path from the parent before
   environment filtering; preserve `XDG_STATE_HOME`, the floor override and
   genuine inherited ownership for local checks without expanding `ENV_ALLOW`
   for foreign calls. Leave formatting/rendering order, model launches and
   generic `launch` timeouts unchanged; report admission refusal through the
   caller's existing failed-check path, never start the rejected check.
4. Create `tests/test_verify_lock.py`: isolated multi-process exclusion, FIFO,
   lifecycle, marker and memory regressions; use temporary state roots, pipes
   or events for process ordering, and injected clocks/readers for minute-scale
   waits. Explicitly clear ambient ownership for independent test admissions.
5. Change `tests/test_ci.py`: copy the helper into `_runner_tree`; retain valid
   inherited state/marker only where a fixture represents nesting, and use
   isolated state for independent fake runners. Add guarded shell/CI/listing
   regressions without weakening the no-second-command-list assertion.
6. Change `tests/test_stage2.py`: exercise both post-run paths and the existing
   selected pytest paths with admission held/waiting/refused; show that
   execution timeout and process-group cleanup remain effective.
7. Change `scripts/kit/manifest.yaml`: carry the new helper as mechanism so
   exported `verify_all.sh` is runnable; keep existing kit checks as the proof.
8. Change `docs/WORKFLOW.md`, "Verification runs through git and CI": document
   queue scope/order, holder logs, nested marker, memory readings, override,
   bounded refusal, unknown-memory continuation and exclusion from step time.
9. Update `plans/changes/verify-machine-lock/plan.md`: replace written ledger
   markers and let the runner fill time evidence. The runner regenerates
   `plans/INDEX.md`; do not edit it by hand.

## Admission and lifecycle

- Shared state is `${XDG_STATE_HOME:-~/.local/state}/coding-harness/`, with
  exclusive `fcntl.flock` on `verify.lock`. Add ordered waiter records under
  `verify.queue/` and a short-held registry lock/counter beside it; assign
  registration order atomically. Waiters keep kernel-backed liveness locks;
  prune dead records under the registry lock. Only the first live waiter may
  acquire the work lock; do not assume `flock` supplies FIFO. Keep lock-file
  inodes stable, open private regular files without following symlinks, and
  refuse unsafe/unusable state rather than running unlocked.
- Publish PID, command and start time while owning admission; log queue entry,
  every 300 seconds and eventual admission to the operator's stderr directly,
  rather than relying on `launch`'s captured output. An entry waiting for a
  turn with no active holder reports that state explicitly.
- Validate `HARNESS_VERIFY_LOCK_HELD` against a live ancestor and published
  ownership; stale/unrelated values do not skip admission. Nested calls reuse
  admission even after local environment filtering. Keep ownership until the
  protected command and its children stop, including failure, cancellation,
  timeout and supervisor death; use inherited lock ownership where necessary.
  A dead queued process must not obstruct survivors. Signal cleanup must not
  release the lock before child cleanup completes.
- After acquiring the work lock, parse the platform's specified memory source.
  Bound probe execution (five seconds); unsupported/failed/hung/malformed
  readings are logged unknown readings and proceed. Keep the 25-percent floor,
  30-second poll, 300-second queue log interval and 3600-second memory bound as
  named constants here. Validate finite override percentages in `[0, 100]`.
  Below the floor retain ownership and poll/log; a sufficient reading starts
  work, while sustained low readings through the deadline refuse with the
  last value and floor. The first low reading starts the memory deadline.
- Acquire before calling the existing timed `launch`, release in `finally`,
  and propagate local ownership into its child environment. Admission waits
  consume neither `VERIFY_SECONDS` nor a pytest proof's execution timeout;
  actual execution still has its configured limit and group kill. Do not
  acquire around foreign calls or around an entire runner attempt.

## Criterion ledger

- 1: tests/test_verify_lock.py::test_independent_entries_share_one_machine_lock — protected intervals overlap across trees/entry kinds.
- 2: tests/test_verify_lock.py::test_live_waiters_enter_in_registration_order — later live registration overtakes the first.
- 3: tests/test_verify_lock.py::test_queue_wait_logs_live_holder_and_progress — initial/update logs or holder PID, command and time are absent.
- 4: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout — waiting consumes execution time or a running hang escapes group cleanup.
- 5: tests/test_verify_lock.py::test_only_live_ancestor_ownership_allows_nested_admission — genuine descendants block or false markers bypass.
- 5: tests/test_stage2.py::test_local_checks_preserve_nested_admission — either post-run path or selected pytest path loses the marker/state root.
- 6: tests/test_verify_lock.py::test_exit_interrupt_and_dead_waiter_release_admission — a dead participant blocks or a protected child overlaps its successor.
- 7: tests/test_verify_lock.py::test_platform_memory_readers_use_the_declared_percentage — the wrong field/formula or malformed percentage is accepted.
- 7: tests/test_verify_lock.py::test_the_macos_reader_parses_the_real_memory_pressure_line — the real macOS line `System-wide memory free percentage: 56%` reads as unmeasurable.
- 8: tests/test_verify_lock.py::test_low_memory_wait_holds_exclusion_and_rechecks — work starts low, exclusion is dropped or 30-second rechecks/logs stop.
- 9: tests/test_verify_lock.py::test_sustained_low_memory_refuses_at_the_bound — low readings outlast 3600 seconds or refusal omits percentages.
- 9: tests/test_verify_lock.py::test_memory_recovery_before_deadline_starts_work — sufficient memory still refuses or never starts work.
- 10: tests/test_verify_lock.py::test_unknown_memory_is_logged_and_does_not_block — a missing/failed/hung/malformed probe blocks or silently passes.
- 11: tests/test_verify_lock.py::test_default_memory_floor_includes_equality — below 25 starts or exactly 25 waits.
- 12: tests/test_verify_lock.py::test_memory_floor_override_is_validated_and_used — valid percentages are ignored or invalid values run work.
- 13: tests/test_ci.py::test_guarded_runner_preserves_gate_verdicts_and_ci_selection — wrapper changes verdict/placement or CI bypasses admission.
- 13: tests/test_ci.py::test_runner_holds_no_command_list_of_its_own — shell adds a direct gate-script command.
- 14: tests/test_verify_lock.py::test_unusable_or_aliased_state_refuses_before_work — broken state runs unlocked or a symlink target is modified.

## Verification and boundaries

From this worktree, using its installed locked environment:

```bash
.venv/bin/python3 -m pytest tests/test_verify_lock.py tests/test_ci.py tests/test_stage2.py tests/test_kit.py -q
python3 scripts/check_interview_minimums.py --change verify-machine-lock
python3 scripts/check_criterion_ledger.py
make verify
```

Run targeted new tests first, then the commands above; no real memory-pressure
stress or simultaneous full suites. Existing kit probes verify helper export.
During drafting the runner owns full verification, derived files and commits.
The referenced change-artefact validator is absent at `8b1f2d98`; do not claim
it passed or add a replacement within this change.

Do not touch `Makefile`, `decisions/gates.yaml`, generated CI, ADRs, interview
answers, foreign-call environment policy, model routing, pytest parallelism
or unrelated changes. `scripts/ci_gates.py` stays the sole gate-list reader.

## Runner route — 2026-10-29

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-10-29

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash rejected twice (2 tests left red); the Sonnet attempt 3 stopped at the Claude five-hour limit; maintainer 2026-10-29: +1 h appetite, continue on Sonnet from the saved attempt 3 (49209675); about 2.7 of 4 h used.

## Runner route — 2026-10-29

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM attempts failed, Sonnet continues from the saved state; one test left red: tests/test_stage2.py::test_local_checks_preserve_nested_admission - a local check must pass a valid inherited lock marker through unchanged instead of setting its own PID; maintainer 2026-10-29: +30 min, total 4.5 h.

## Time used

2026-10-29 08:48:20–10:17:53 UTC, 5373 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-29 10:18:00–11:21:06 UTC, 3786 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-29 13:39:11–13:53:28 UTC, 857 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner

Orchestrator bootstrap edit, 2026-10-29 ~14:00 UTC: the macOS memory reader's pattern accepts `System-wide` as `memory_pressure` prints it (the attempt of 13:39 logged every real reading as unmeasurable); ledger entry and test added, red first. Left for the next attempt: `tests/test_stage2.py::test_local_checks_preserve_nested_admission` — a local check that inherits a valid held marker must pass the ancestor's marker on unchanged instead of taking a new admission of its own.
2026-10-29 13:54:45–14:36:10 UTC, 2485 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · claude call failed at exit 1 (Claude limit), no code change · measured with `date -u`
Appetite stop, 2026-10-29 16:55 UTC: about 3.9 of 4 h used; the change is parked with one test left red (`tests/test_stage2.py::test_local_checks_preserve_nested_admission`). The maintainer decides.
2026-10-29 17:05:21–17:18:53 UTC, 812 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-10-29 19:10:01–19:12:04 UTC, 123 s — review loop round 1 · rows L1-1/L1-12, L1-3, L1-11, L1-14 repaired by the orchestrator, each test red first; L1-5 text; nine rows rejected · measured with `date -u`
