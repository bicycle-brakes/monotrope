---
title: "Plan — verify-two-slots"
category: plan
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification]
---

# Plan — `verify-two-slots`

```text
For you:     Two protected verification runs can share the machine, with visible holders and a one-slot fallback.
Done when:   Admission regressions and make verify pass, and the two-run night-load trial meets the 1.6x limit.
Appetite:    Four hours of phase 4 including repairs and the trial; stop at the limit.
Not now:     Worker tuning, extra slots, central configuration and multiple handles per process.
Pre-mortem:  suppose it failed: most likely because concurrent runs overload the machine.
Starts unless you say stop.
```

## Build sequence

1. In `scripts/verify_lock.py`, parse `HARNESS_VERIFY_SLOTS` once per independent entry: absent means 2; only `1` and `2` are valid. Under the existing registry lock, publish each updated holder and waiter setting and use the minimum of all reserved holders and the head live waiter as effective capacity; a dead supervisor's setting remains until its final inherited descriptor closes. Only the first live waiter may reserve. Treat a legacy empty queue record as an exclusive waiter, drain for it or any head set to 1, and do not let later waiters overtake it. Keep the legacy `verify.lock` shared for new holders and exclusive for legacy holders; use separately locked stable slot files. Preserve the legacy exclusive holder reader for mixed versions. Pass both the compatibility and slot descriptors through each protected child path so that a survivor keeps both locks; safely reject substituted state, and prune stale records only when their associated locks are free.
2. Publish one atomic holder record per slot, including the existing token, admission ID and wait; release only the matching record. Validate descendants against their own slot and locked descriptor, and support the existing legacy marker. Keep tokens out of diagnostics. Show every occupied slot or an explicit unavailable holder at the initial and periodic wait log, including an exclusive legacy holder. Coordinate publish, release and probes to avoid confusing replaced ownership with a descendant's.
3. Reserve a process-local acquisition guard atomically before queueing, clear it on every exit including failures, and refuse a second independent in-process request promptly. Preserve valid inherited reuse, per-slot memory checks, signals and measurement context. Adapt `scripts/verify_run.py` and `scripts/stage2.py` to carry both descriptors through the existing scheduler and targeted paths. Forward `HARNESS_VERIFY_SLOTS` to local children in `inherit_env`, but keep the foreign-call `ENV_ALLOW` closed to `HARNESS_*`; do not alter worker sizing.
4. Write the ledger's subprocess and concurrency regressions, using isolated shared-state roots. Exercise both free slots, a third waiter, mixed-capacity holders and waiters, old/new lock owners and an earlier old waiter, FIFO and dead waiters, exact malformed configuration and inherited reuse before parsing, concurrent threads, stale and forged nesting, independent release, inherited descriptors, memory floor, holder logs and timeout/context propagation. Update old one-slot assertions to explicitly select one slot.
5. After a green targeted run and `make verify`, use two separate worktrees at the same committed revision and unchanged default workers. Discard one warm-up per worktree, then run one serial `make verify` and a simultaneous pair in the two worktrees, starting each trial with both slots free. Record warm-up identifiers and order, date, revision, background processes/lanes, settings, verdicts, individual launch-to-exit wall and execution seconds, existing combined queue-plus-memory admission wait, both parallel/serial ratios, and start/end 1-, 5- and 15-minute load averages. Use an external sampler of `verify_lock.read_available_memory()` every five seconds throughout each run; record start and minimum percentages and invalidate missing readings or gaps over 15 seconds. Observe and record all protected admissions, including targeted checks, and their intervals: invalidate any additional overlap with the serial run or any third overlap or contention with the pair, or incomplete observation. Other workstation/harness activity may continue. All three exits must be zero and each ratio at most 1.6. If a parallel test fails, rerun it serially on the same revision solely to classify the failure; stop and report for any failed or unavailable trial, including non-test failures and timeouts. A single pair does not prove absence of flakes. Verify `git diff <trial-commit>..HEAD -- scripts/` is empty; a later scripts change requires a repeat, while verified and noted documentation, test or plans changes do not. Stop at the four-hour appetite.

## Files and limits

- `scripts/verify_lock.py`: implement configurable shared slots, compatibility, ownership, diagnostics and the process boundary.
- `scripts/verify_run.py` and `scripts/stage2.py`: propagate both descriptors and configuration through full and targeted checks; do not change worker sizing.
- `tests/test_verify_lock.py`: update existing one-slot cases and add slot, ownership, compatibility, lifecycle and logging regressions.
- `tests/test_verify_before_admission.py`: preserve scheduler, timing and descriptor integration under concurrent admissions.
- `tests/test_verify_duration.py`: preserve admission context and wait attribution with two holders.
- `tests/test_stage2.py` and `tests/test_ci.py`: adapt existing holder and lock fixtures and check full and targeted runner paths retain both descriptors and the setting.
- `docs/WORKFLOW.md`, `docs/orchestration.md`, `docs/how-it-works.md`, `docs/governance/gate-catalog.md`: replace current single-machine-slot claims with the new capacity, configuration, constraints and rollout boundary; retain historical statements.
- `plans/changes/verify-two-slots/measurements.md`: create the dated trial evidence with required frontmatter and tested revision.
- `plans/changes/verify-two-slots/spec.md`, `plan.md` and `findings.md`: maintain the scope, ledger, evidence and runner findings; the runner owns its records. `plans/INDEX.md` is regenerated by its owner if the registry requires it.

No files are deleted. Do not edit worker sizing, `Makefile`, `decisions/gates.yaml`, `provenance.yaml`, ADRs, `AGENTS.md`, prompts, templates or hosted CI. No held path is assigned to the implementation attempt. This bounded change has no design phase or ADR; `findings.md` has no open phase-2a rows as of 2026-11-21. Mixed settings use the minimum of reserved holders and the queue head, and earlier old waiters drain the slots. The stale single-slot comments in `decisions/gates.yaml:49-59` are an accepted follow-up for a separate decision pull request. Old verification launched inside a new admission may wait on its ancestor, and descendants without inherited descriptors may outlive a slot, as stated in the spec boundary.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_verify_lock.py tests/test_verify_before_admission.py tests/test_verify_duration.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_verify_lock.py::test_two_slots_admit_two_and_queue_third — a third overlaps or an eligible second cannot reserve within two polls.
- 2: not yet written tests/test_verify_lock.py::test_slot_setting_and_capacity_reduction — configured capacity is ignored or mixed settings ignore a holder or head waiter, or a one-slot request enters before draining.
- 3: not yet written tests/test_verify_lock.py::test_invalid_slot_setting_refuses — padded or otherwise invalid input starts independent work, lacks a diagnostic, or blocks valid inherited reuse.
- 4: not yet written tests/test_verify_lock.py::test_two_slot_fifo_and_dead_waiter — a live updated or legacy waiter is overtaken or the eligible head cannot reserve free capacity within two polls.
- 5: not yet written tests/test_verify_lock.py::test_nested_slot_and_legacy_ownership — an invalid marker bypasses admission or a valid descendant waits or takes peer context.
- 6: not yet written tests/test_verify_lock.py::test_second_in_process_admission_refused_during_acquisition — concurrent requests both enter or the second hangs.
- 7: not yet written tests/test_verify_lock.py::test_slot_release_preserves_peer_and_inherited_child — a peer is disturbed, a survivor loses its reservation, or the eligible waiter cannot reserve within two polls after the last descriptor closes.
- 7: not yet written tests/test_verify_lock.py::test_killed_one_slot_holder_keeps_capacity_until_child_exits — a two-slot waiter joins the inherited child of a killed one-slot supervisor.
- 8: not yet written tests/test_verify_lock.py::test_memory_floor_applies_to_both_slots — either slot bypasses or changes the floor policy.
- 9: not yet written tests/test_verify_lock.py::test_wait_log_names_both_holders_without_tokens — a holder is omitted or a token is printed.
- 10: not yet written tests/test_verify_lock.py::test_legacy_exclusive_lock_excludes_both_slots — old and new protected work overlap or an earlier legacy waiter is overtaken.
- 11: not yet written tests/test_verify_before_admission.py::test_two_slot_scheduler_preserves_wait_context_and_descriptors — wait spends the timeout or the scheduler loses a descriptor or verdict.
- 11: not yet written tests/test_verify_duration.py::test_two_slot_context_does_not_mix_holder_waits — one run records its peer's context.
- 12: not a test — the phase-6 review checks `measurements.md` against criterion 12, including worktrees, warm-ups, complete admission observation, five-second memory samples, exits, attribution, end-to-end 1.6x and final `scripts/` revision.

## Runner route — 2026-11-21

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-21 11:04:34–11:08:05 UTC, 211 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 11:23:31–11:25:47 UTC, 136 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 11:46:11–11:49:04 UTC, 173 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:00:13–16:04:26 UTC, 3853 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-21 16:04:34–16:33:10 UTC, 1715 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-21 16:33:19–16:34:02 UTC, 44 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
