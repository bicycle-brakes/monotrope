---
title: "Spec — verify-two-slots"
status: accepted
implementation_status: done
date: 2026-11-21
last_reviewed: 2026-11-26
updated: 2026-11-26
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

- **Slot:** one independent admission, including its memory wait and the lifetime of ownership held by inherited lock descriptors.
- **FIFO:** live waiters reserve available capacity in registration order; separate memory waits may change work-start order.

## Acceptance criteria

1. When independent checks use the default setting, at most two protected admissions share the machine across repositories and worktrees, and both available slots can be reserved.
   *Refuted by:* a third admission runs, or the eligible head waiter cannot reserve an otherwise free slot within two queue poll intervals (0.5 seconds at the default interval).
   *Basis:* `decisions.md#Q-1`.

2. When an independent entry requests capacity `1` or `2` through `HARNESS_VERIFY_SLOTS` (default `2`), effective capacity is the minimum of the settings of all live updated holders and the head live waiter; an older waiter counts as `1` and requires exclusive access.
   *Refuted by:* a `1` holder shares capacity, a head `1` waiter enters before all holders drain, or two `2` entries cannot use both free slots.

   Local child processes receive the setting when present; the foreign-model environment allow-list remains closed to `HARNESS_*` variables.
   *Basis:* `decisions.md#Q-1`.

3. If an independent entry has `HARNESS_VERIFY_SLOTS` set to anything other than the exact strings `1` or `2`, it refuses before protected work with a diagnostic naming the setting.
   *Refuted by:* an empty, padded, `02`, `+2`, fractional or other invalid value starts work, or a valid inherited descendant is refused because of that setting.
   *Basis:* `decisions.md#Q-1`.

4. While independent live checks wait, the earliest registered live waiter, including an older checkout waiting exclusively, has first claim on capacity free under criterion 2.
   *Refuted by:* a later waiter overtakes a live earlier waiter, a dead waiter blocks progress, or the eligible head waiter cannot reserve a free slot under the effective capacity within two queue poll intervals (0.5 seconds at the default interval).
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

5. When a valid descendant enters protected work, it reuses its own ancestor's admission and measured context without reserving another slot.
   *Refuted by:* a descendant waits for capacity, uses a peer's context, or an unrelated, stale or forged marker bypasses admission; a valid legacy holder's descendant must also reuse its admission.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

6. When a process holding or acquiring an independent admission requests another independent admission, the second request is refused promptly with a diagnostic.
   *Refuted by:* concurrent threads overwrite the process's admission, or the second request waits or succeeds; a valid inherited descendant remains governed by criterion 5.
   *Basis:* `decisions.md#Q-1`.

7. When a holder exits, fails or is cancelled, its slot and configured capacity remain in force until the last inherited ownership descriptor closes, without disturbing another holder.
   *Refuted by:* a replacement overlaps a child still holding the descriptor, a surviving child of a killed one-slot supervisor shares the machine with a two-slot waiter, one release removes a peer's record, or after the final inherited descriptor closes, a free slot is not reservable by the next eligible live waiter within two queue poll intervals (0.5 seconds at the 0.25-second default), with no other holder or older waiter blocking it.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

8. When an admission reserves either slot, the existing per-admission memory floor and refusal behavior apply before protected work starts.
   *Refuted by:* the second slot skips the memory check, below-floor memory starts work, or the existing floor override, equality, polling, timeout or unmeasurable-reading behavior changes.
   *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

9. While a check waits, the initial and five-minute progress diagnostics identify each occupied slot and its holder's process, command and start time, or explicitly say that its holder is unavailable, without exposing ownership tokens.
   *Refuted by:* a holder overwrites its peer, an occupied slot disappears from the diagnostic, a legacy holder is omitted, or a token appears.
   *Basis:* `decisions.md#Q-1`.

10. When an older single-slot checkout shares machine state with an updated checkout, the older exclusive admission cannot overlap updated admissions and its earlier live queue entry is honored.
    *Refuted by:* an old holder or its surviving child overlaps an updated holder, or a later updated waiter overtakes an earlier live old waiter.
    *Basis:* `decisions.md#Q-1` and `research.md`, “The admission”.

11. When shell or runner checks use admission, their check selection, verdict, timeouts, inherited descriptors and separation of admission wait from execution time remain intact.
    *Refuted by:* a full or targeted check bypasses admission, wait consumes an execution timeout, an inherited descriptor is lost, or a failure becomes success.
    *Basis:* `decisions.md#Q-1` and `research.md`, “The scheduler and its callers”.

12. Before completion, a recorded trial compares one serial `make verify` with two simultaneous `make verify` invocations, starting each trial with both slots free and using the unchanged default worker calculation; each simultaneous invocation's launch-to-exit wall time is at most 1.6 times the serial invocation's launch-to-exit wall time, and all three exit zero.
    *Refuted by:* a nonzero exit, either ratio above 1.6, or missing recorded revision, date, configuration, verdicts, individual end-to-end wall times, execution seconds, combined admission wait seconds (queue plus memory), or ratios.
    *Basis:* `decisions.md#Q-1`; the 2026-11-17 handover records that the 1.6 threshold applies to two slots.

    Use two separate worktrees at the trial revision: run and discard one warm-up per worktree, then the serial run, then the simultaneous pair; record the order and warm-up run identifiers. Run under normal active workstation or harness load; other lanes may work. No other protected admission, including a targeted check, may overlap the serial run, and no third protected admission may overlap or contend with the pair. Record every protected admission seen in each run; an extra admission or incomplete observation invalidates the trial.

    Record background processes or lanes, start and end 1-, 5- and 15-minute load averages, and starting and minimum available memory percentage. An external sampler reads available memory every five seconds throughout each run; a gap over 15 seconds or a missing required reading invalidates the trial. If a parallel test fails, rerun that test serially on the same revision to classify it: a serial pass indicates a parallelism-caused failure and a serial failure a content failure. A single pair demonstrates zero observed failures, not a statistical absence of flakes. If any trial fails or cannot run, including a non-test gate failure or timeout, stop and report; a content failure is fixed before any later complete trial.

    The trial revision must match the final `scripts/` tree: `git diff <trial-commit>..HEAD -- scripts/` is empty. Record and verify any later documentation-only, test-only or plans changes; repeat the complete trial after any later `scripts/` change, subject to the four-hour stop.

## Non-goals

- Changing pytest worker sizing, general central configuration, explicit admission handles, product RAM-minimum telemetry or separate queue and memory wait instrumentation, or tuning three or four slots; worker sizing, central configuration and explicit handles belong to follow-up beads `coding-harness-bxxt.11`, `coding-harness-twvx` and `coding-harness-42em` respectively.
- Changing which checks require admission, hosted CI policy, memory-floor thresholds or a priority queue.
- A throughput guarantee or a claim that the two-slot trial proves other slot/worker combinations.

## Boundary

One process has at most one independent admission, including while acquiring it. A valid inherited descendant reuses its ancestor rather than taking another. Only descendants holding the inherited descriptors retain ownership: after an intermediate process is killed hard, a protected descendant in another process group that did not inherit them may outlive the slot and overlap a replacement. Explicit multiple admission handles are deferred to bead `coding-harness-42em` (explicit admission handles). An older checkout invoked inside a new holder cannot validate the new marker and may wait for its own ancestor; normal runner and full-check paths use the same checkout. The reverse direction is supported by criterion 5.

## Protected areas

Leave worker calculation, `Makefile`, `decisions/gates.yaml`, `provenance.yaml`, ADRs, `AGENTS.md`, prompts, templates, and hosted CI configuration unchanged: this slice changes admission capacity, not gate policy or worker tuning. Historical observations stay dated. The single-slot comments in `decisions/gates.yaml:49-59` remain an accepted out-of-scope follow-up for a separate decision pull request.

## Definition of Done

- `make verify` green and criteria 1–11 covered by the plan's regressions.
- `docs/WORKFLOW.md`, `docs/orchestration.md`, `docs/how-it-works.md` and `docs/governance/gate-catalog.md` describe the resulting current behavior; the trial is recorded in `plans/changes/verify-two-slots/measurements.md` and identified by revision in the pull request, with the final `scripts/` tree checked against that revision.
- Protected areas untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-u1ha` (two verify slots) and its last commit carries `Closes-Bead: coding-harness-u1ha`.

## Open decisions

No maintainer decision is open.

- [DETAIL] Accept exact `1` and `2` for independent entries, defaulting to `2`, and forward the setting locally. The bounded range avoids the previously measured three-run overload; the minimum of live holders and the queue head protects mixed settings without opening the foreign-model environment.
- [DETAIL] Preserve the old lock as a compatibility lock shared by new holders and exclusive for old holders; FIFO includes older waiters in the shared queue. This preserves the old machine-wide bound during rollout without changing old checkouts.
- [DETAIL] Measure launch-to-exit time under the stated active load and require all exits green; the trial exposes waits and cannot prove long-run flake rates. Recheck the final `scripts/` tree because a later runtime repair invalidates the result.
- [DETAIL] Two queue polls bound release after the last descriptor closes; it makes recovery testable without changing the existing poll interval.
- [DETAIL] Keep a reserved holder's configured capacity until its last descriptor closes; this preserves exclusivity after a supervisor dies. Descendants without descriptors are outside this ownership boundary.
- [DETAIL] Warm each of two worktrees before a serial run and then a concurrent pair, exclude other protected admissions, and sample memory externally every five seconds; these fix trial conditions without new product telemetry. Use the existing combined wait figure. Stop on every trial failure and report its classification; this respects the four-hour stop.
- [DETAIL] Keep the protected gate manifest unchanged and record its stale single-slot comment for a separate decision pull request; its owner controls that text.
- [DETAIL] Four hours for implementation, repairs and the trial is the stop, carried from the earlier bounded slice's spec at `b5c2105b`; report unfinished work at the limit.
