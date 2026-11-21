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

1. In `scripts/verify_lock.py`, parse `HARNESS_VERIFY_SLOTS` once per independent entry: absent means 2; only `1` and `2` are valid. Under the existing registry lock, let only the first live waiter reserve an available slot and count all live slot locks before honoring a reduction. Keep the legacy `verify.lock` shared for new holders and exclusive for legacy holders; use separately locked stable slot files. Preserve the legacy exclusive holder reader for mixed versions. Pass both the compatibility and slot descriptors through each protected child path so that a survivor keeps both locks; safely reject substituted state, and prune stale records only when their associated locks are free.
2. Publish one atomic holder record per slot, including the existing token, admission ID and wait; release only the matching record. Validate descendants against their own slot and locked descriptor, and support the existing legacy marker. Keep tokens out of diagnostics. Show every occupied slot or an explicit unavailable holder at the initial and periodic wait log, including an exclusive legacy holder. Coordinate publish, release and probes to avoid confusing replaced ownership with a descendant's.
3. Reserve a process-local acquisition guard atomically before queueing, clear it on every exit including failures, and refuse a second independent in-process request promptly. Preserve valid inherited reuse, per-slot memory checks, signals and measurement context. Adapt `scripts/verify_run.py` and `scripts/stage2.py` to carry both descriptors and the environment setting through the existing scheduler and targeted paths; do not alter worker sizing.
4. Write the ledger's subprocess and concurrency regressions, using isolated shared-state roots. Exercise both free slots, a third waiter, mixed old/new lock owners, FIFO and dead waiters, lowered capacity, malformed configuration, concurrent threads, stale and forged nesting, independent release, inherited descriptors, memory floor, holder logs and timeout/context propagation. Update old one-slot assertions to explicitly select one slot.
5. After a green targeted run and `make verify`, run one serial and two simultaneous full checks on the same implemented revision with the same default worker calculation under representative night load. Record date, commit, background workload, slot and worker configuration, each verdict and wall time, sampled load, each parallel/serial ratio and investigation of failures in `measurements.md`. Both ratios must be at most 1.6 and no red or flaky test may be caused by parallelism; if evidence is unavailable or the trial fails, stop and report instead of claiming completion. Run the trial only while the four-hour appetite remains.

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

No files are deleted. Do not edit worker sizing, `Makefile`, `decisions/gates.yaml`, `provenance.yaml`, ADRs, `AGENTS.md`, prompts, templates or hosted CI. No held path is assigned to the implementation attempt. This bounded change has no design phase or ADR; `findings.md` has no open phase-2a rows as of 2026-11-21. The environment setting is per process: apply a consistent value to all new entries; mixed settings do not establish a common one-slot limit. Old verification launched inside a new admission may wait on its ancestor, as stated in the spec boundary.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_verify_lock.py tests/test_verify_before_admission.py tests/test_verify_duration.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_verify_lock.py::test_two_slots_admit_two_and_queue_third — a third overlaps or the second cannot enter.
- 2: not yet written tests/test_verify_lock.py::test_slot_setting_and_capacity_reduction — configured capacity is ignored or a reduction admits before draining.
- 3: not yet written tests/test_verify_lock.py::test_invalid_slot_setting_refuses — invalid input starts protected work or lacks a diagnostic.
- 4: not yet written tests/test_verify_lock.py::test_two_slot_fifo_and_dead_waiter — a live waiter is overtaken or a free slot remains idle.
- 5: not yet written tests/test_verify_lock.py::test_nested_slot_and_legacy_ownership — an invalid marker bypasses admission or a valid descendant waits or takes peer context.
- 6: not yet written tests/test_verify_lock.py::test_second_in_process_admission_refused_during_acquisition — concurrent requests both enter or the second hangs.
- 7: not yet written tests/test_verify_lock.py::test_slot_release_preserves_peer_and_inherited_child — a peer is disturbed or a survivor loses its reservation.
- 8: not yet written tests/test_verify_lock.py::test_memory_floor_applies_to_both_slots — either slot bypasses or changes the floor policy.
- 9: not yet written tests/test_verify_lock.py::test_wait_log_names_both_holders_without_tokens — a holder is omitted or a token is printed.
- 10: not yet written tests/test_verify_lock.py::test_legacy_exclusive_lock_excludes_both_slots — old and new protected work overlap.
- 11: not yet written tests/test_verify_before_admission.py::test_two_slot_scheduler_preserves_wait_context_and_descriptors — wait spends the timeout or the scheduler loses a descriptor or verdict.
- 11: not yet written tests/test_verify_duration.py::test_two_slot_context_does_not_mix_holder_waits — one run records its peer's context.
- 12: not a test — the phase-6 review checks `measurements.md` against the two-slot night-load trial, the 1.6x threshold and outcomes on the tested revision.

## Time used

2026-11-21 11:04:34–11:08:05 UTC, 211 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
