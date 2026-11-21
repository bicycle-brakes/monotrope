---
title: "Spec — verify-two-slots"
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
tags: [spec, verification]
class: bounded
appetite: 4
adr_files: []
---

# Spec — `verify-two-slots`

Independent protected checks can use two shared verification slots by default, with a bounded and measured load (bead `coding-harness-u1ha` — two verify slots). Research: `research.md`. Decisions: `decisions.md#Q-1`.

## Problem

- At commit `6589014a`, the machine-wide admission holds one exclusive work lock, serialising protected checks across repositories and worktrees (`research.md`, “The admission, as this branch's code has it”). For 151 runs on 2026-11-04–09, the research reports 77.3 hours of queue wait and 57.1 hours of execution.
- On 2026-11-09, three concurrent full runs each took over 30 minutes against 11–12 minutes serial, so unrestricted parallelism risks making checks slower (`research.md`, “The bead and why”).
- At commit `6589014a`, one published holder and the in-process admission state cannot describe two independent holders; a second in-process request can wait behind itself (`research.md`, “The admission” and “The boundary refusal”).

## Terms

- **Slot:** one independent admission, including its memory wait and protected descendants' lifetime.
- **FIFO:** live waiters reserve available capacity in registration order; separate memory waits may change work-start order.

## Acceptance criteria

1. When independent checks use the default setting, at most two protected admissions share the machine across repositories and worktrees, and both available slots can be reserved.
   *Refuted by:* a third admission runs, or the second cannot reserve an otherwise free slot.
   *Basis:* `decisions.md#Q-1`.

2. When all new entries use `HARNESS_VERIFY_SLOTS=1` or `2`, that capacity applies without a code change, including draining existing excess reservations after a reduction.
   *Refuted by:* one permits a second reservation, two leaves a free slot unused, or a new reservation starts before an over-capacity state drains below the configured count.
   *Basis:* `decisions.md#Q-1`.

3. If `HARNESS_VERIFY_SLOTS` is present but is not exactly `1` or `2`, the entry refuses before protected work with a diagnostic naming the setting.
   *Refuted by:* an empty, zero, fractional, nonnumeric or greater-than-two value silently falls back or starts work.
   *Basis:* `decisions.md#Q-1`.

4. While independent live checks wait, each free slot goes to the earliest registered live waiter.
   *Refuted by:* a later waiter overtakes a live earlier waiter, a dead waiter blocks progress, or an occupied slot prevents another free slot from being used.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

5. When a valid descendant enters protected work, it reuses its own ancestor's admission and measured context without reserving another slot.
   *Refuted by:* a descendant waits for capacity, uses a peer's context, or an unrelated, stale or forged marker bypasses admission; a valid legacy holder's descendant must also reuse its admission.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

6. When a process holding or acquiring an independent admission requests another independent admission, the second request is refused promptly with a diagnostic.
   *Refuted by:* concurrent threads overwrite the process's admission, or the second request waits or succeeds; a valid inherited descendant remains governed by criterion 5.
   *Basis:* `decisions.md#Q-1`.

7. When a holder exits, fails or is cancelled, its slot stays reserved until its protected descendants release their inherited ownership, without disturbing another holder.
   *Refuted by:* a replacement overlaps a surviving protected child, one release removes a peer's record, or a dead holder without surviving ownership blocks capacity indefinitely.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

8. When an admission reserves either slot, the existing per-admission memory floor and refusal behavior apply before protected work starts.
   *Refuted by:* the second slot skips the memory check, below-floor memory starts work, or the existing floor override, equality, polling, timeout or unmeasurable-reading behavior changes.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

9. While a check waits, the initial and five-minute progress diagnostics identify each occupied slot and its holder's process, command and start time, or explicitly say that its holder is unavailable, without exposing ownership tokens.
   *Refuted by:* a holder overwrites its peer, an occupied slot disappears from the diagnostic, a legacy holder is omitted, or a token appears.
   *Basis:* `decisions.md#Q-1`.

10. When an older single-slot checkout shares the machine state with an updated checkout, the old exclusive admission and updated admissions cannot overlap.
    *Refuted by:* an old holder, including a surviving protected child, runs beside an updated holder.
    *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

11. When shell or runner checks use admission, their check selection, verdict, timeouts, inherited descriptors and separation of admission wait from execution time remain intact.
    *Refuted by:* a full or targeted check bypasses admission, wait consumes an execution timeout, an inherited descriptor is lost, or a failure becomes success.
    *Basis:* `decisions.md#Q-1` and `research.md`, “The scheduler and its callers”.

12. Before completion, a recorded trial on the implemented revision compares one full serial run with two simultaneous full runs under representative night load, using the unchanged worker calculation; both parallel run durations are at most 1.6 times the serial duration and no test turns red or flaky because of parallelism.
    *Refuted by:* missing revision, date, workload, configuration, outcomes, individual wall times, sampled load or ratios; a ratio above 1.6; or a parallelism-caused red or flaky test. An unrelated content failure is investigated separately. If the trial cannot be run or fails, stop and report; do not claim completion.
    *Basis:* `decisions.md#Q-1`; the prior lane's maintainer answers Q-3 and Q-4, `feat/verify-slots:plans/changes/verify-slots/decisions.md` at `b5c2105b`, specify the night load and threshold.

## Non-goals

- Changing pytest worker sizing, general central configuration, explicit admission handles, RAM-minimum telemetry, or tuning three or four slots; these belong to follow-up work (respectively beads `coding-harness-bxxt.11`, `coding-harness-twvx`, and `coding-harness-42em` for explicit handles).
- Changing which checks require admission, hosted CI policy, memory-floor thresholds or a priority queue.
- A throughput guarantee or a claim that the two-slot trial proves other slot/worker combinations.

## Boundary

One process has at most one independent admission, including while acquiring it. A valid inherited descendant reuses its ancestor rather than taking another. Explicit multiple admission handles are deferred to bead `coding-harness-42em` (explicit admission handles). An older checkout invoked inside a new holder cannot validate the new marker and may wait for its own ancestor; normal runner and full-check paths use the same checkout. The reverse direction is supported by criterion 5.

## Protected areas

Leave worker calculation, `Makefile`, `decisions/gates.yaml`, `provenance.yaml`, ADRs, `AGENTS.md`, prompts, templates, and hosted CI configuration unchanged: this slice changes admission capacity, not gate policy or worker tuning. Historical observations stay dated.

## Definition of Done

- `make verify` green and criteria 1–11 covered by the plan's regressions.
- `docs/WORKFLOW.md`, `docs/orchestration.md`, `docs/how-it-works.md` and `docs/governance/gate-catalog.md` describe the resulting current behavior; the trial is recorded in `plans/changes/verify-two-slots/measurements.md` and identified by revision in the pull request.
- Protected areas untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-u1ha` (two verify slots) and its last commit carries `Closes-Bead: coding-harness-u1ha`.

## Open decisions

No maintainer decision is open.

- [DETAIL] Accept only `1` and `2`, with an absent setting meaning `2`; reject an empty value. The bounded range prevents the previously measured three-run overload; consistent values must be supplied to all new entries because an environment setting is per process. A lower setting drains already held reservations before new ones enter.
- [DETAIL] Preserve the old lock as a compatibility lock shared by new holders and exclusive for old holders; FIFO applies among updated waiters. This preserves the old machine-wide bound during rollout without changing old checkouts.
- [DETAIL] Four hours for implementation, repairs and the trial is the stop, carried from the earlier bounded slice's spec at `b5c2105b`; report unfinished work at the limit.
