---
title: "Spec — verify-slots"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification]
class: bounded
appetite: 4
adr_files: []
neighbours: []
---

# Spec — `verify-slots`

The goal in one sentence: two independent protected checks may run at once by
default, and their number is one value adjustable without a code change
(bead `coding-harness-u1ha` — configurable verification capacity). Research:
`research.md`. Decisions: `decisions.md`.

## Problem

- The machine-wide admission serialises protected checks across repositories
  and worktrees; measured queue waits rival execution time (research, "The
  slot is the measured bottleneck": five green runs on 2026-11-05, execution
  1,215–1,261 seconds, lock waits 2–1,254 seconds).
- On 2026-11-09 five repair lanes waited one to five hours each at the lock
  while one check of about 25 minutes ran; the maintainer authorised two
  simultaneous full checks, not the unbounded concurrency that had overloaded
  the machine before (`decisions.md#Q-1`).
- The slot count is fixed in code; no configurable value exists, and the
  maintainer requires one central, easily changed place for it
  (research, "Meaning A"; `decisions.md#Q-2`).
- Two simultaneous checks have not been measured on this implementation; the
  recorded incident concerns three checks and cannot establish how two behave
  (`decisions.md`, closing evidence note).

## Terms

- **Slot:** the capacity one independent protected admission reserves, from
  turn-taking through its memory wait and its protected children's lifetime;
  nested checks share the slot of the admission they descend from.
- **Capacity:** the maximum independent reservations this user's machine
  allows at once, shared by cooperating repositories and worktrees through
  the one state root.
- **FIFO:** live waiters reserve free capacity in registration order;
  completion order, and work-start order after separate memory waits, may
  differ.

## Acceptance criteria

1. When independent protected checks contend and no capacity setting is
   present, two slots are available across repositories and worktrees.
   *Refuted by:* an eligible second check cannot reserve the idle second
   slot, or a third runs while two are occupied.
   *Basis:* `decisions.md#Q-1`.

2. When capacity is changed in its single documented machine-wide setting,
   later reservation decisions use that positive integer, with no code edit
   and no per-checkout copy of the value.
   *Refuted by:* settings of one or three are ignored, different working
   directories select different values, or a lowered capacity grants new
   reservations before existing ones drain below it.
   *Basis:* `decisions.md#Q-2`.

3. If a present capacity setting is invalid or cannot be safely read,
   independent admission refuses with a diagnostic before any protected work.
   *Refuted by:* an empty, zero, negative, fractional, nonnumeric,
   substituted or unreadable setting silently selects a fallback, hangs, or
   lets work start.
   *Basis:* `decisions.md#Q-2` (one declared, validated value).

4. While live independent checks wait, free slots are reserved in FIFO order,
   without waiting for all occupied slots to empty.
   *Refuted by:* a later waiter overtakes an earlier live registration, a
   dead waiter blocks progress, or one occupied slot keeps another idle.
   *Basis:* `decisions.md#Q-1` (FIFO retained).

5. When a protected check nests inside an existing admission, it reuses only
   that validated admission, its slot and its measured wait, and consumes no
   further slot.
   *Refuted by:* nesting queues at full capacity, a peer's slot, token or
   context is mistaken for its own, or a stale or malformed marker bypasses
   admission.
   *Basis:* `decisions.md#Q-1` (extend the existing admission, not its
   protections).

6. When a participant exits, fails or is cancelled, its reservation stays
   held through its protected children's cleanup and then releases without
   disturbing peers.
   *Refuted by:* a successor overlaps still-protected work, cleanup removes
   a peer's ownership, or a dead participant permanently consumes capacity.
   *Basis:* `decisions.md#Q-1` (existing lifecycle retained).

7. When any slot is reserved, that admission applies the existing
   free-memory policy before starting its protected work.
   *Refuted by:* a second slot skips the probe, below-floor memory starts
   work, or the existing equality, override, polling, sustained-low refusal
   and logged-unknown behaviour changes.
   *Basis:* `decisions.md#Q-1` (memory check per admission).

8. While protected verification waits for capacity through either the shell
   or the runner entry, the existing execution limits, check selection, exit
   verdict and the separation of admission wait from execution duration are
   preserved.
   *Refuted by:* a wait spends a checking timeout, a failed check turns
   green, CI selection bypasses admission, or a peer's wait is charged to
   the run.
   *Basis:* `decisions.md#Q-1` (existing entry points retained).

9. When a check waits for capacity, diagnostics identify every occupied slot
   and its published holder, without exposing ownership tokens.
   *Refuted by:* the initial or five-minute progress logs disappear, one
   holder overwrites another's record, or a log prints a token instead of
   the holder's slot, process id, command and start time — or an explicit
   unavailable value.
   *Basis:* `decisions.md#Q-1` (existing operator visibility retained).

10. When an older single-slot checkout shares the machine state, its
    exclusive admission cannot overlap any admission of the updated
    implementation.
    *Refuted by:* the added slots let an older protected check run beside a
    new holder, including after an older supervisor dies with its protected
    child still running.
    *Basis:* `decisions.md#Q-1` (the bound stays machine-wide across
    checkouts).

11. Before the change counts as done, operation at two slots has recorded
    wall time and machine load beside a serial comparison on the same
    implementation.
    *Refuted by:* completion is claimed without revision, date,
    configuration, outcomes, per-run wall times, batch elapsed times and
    sampled load for both trials, or a current-policy document still
    prescribes one slot.
    *Basis:* `decisions.md`, closing evidence note; `decisions.md#Q-2`.

## Non-goals

- Research-swarm invocation slots, pytest worker-count tuning, priority
  scheduling, continuous memory monitoring, new bypasses, or any change to
  which work needs admission (research, "Meaning B", "Protected areas").
- The future general harness configuration (bead `coding-harness-twvx` —
  central configuration); this change supplies only the capacity value and
  its one documented home.
- A throughput guarantee, a new performance threshold or automatic tuning;
  the trials report evidence, they do not promise an improvement.
- Design phase 2b and an ADR: this is the bounded extension recorded in
  `decisions.md` (class bounded), not a change to architecture or gate
  policy.

## Boundary

One process holds at most one admission at a time (maintainer, 2026-11-11,
review round 3, rows L3-2 and L3-3). A second admission requested while the
same process still holds one is refused at once with a message that names the
held slot; it never waits and never shares descriptors, environment marker or
holder file with the first. The runner never asks for two: every caller
(`scripts/verify_all.sh`, the timed checks of `scripts/stage2.py`) holds one
admission for one run. Lifting this boundary is the work of bead
coding-harness-42em (each admission an explicit handle).

## Protected areas

`Makefile`, `decisions/gates.yaml`, `.github/`, `provenance.yaml`, ADRs,
`AGENTS.md`, prompts, templates and model routing stay unchanged: the change
adjusts admission capacity, not governance, gate commands or foreign calls.
The existing memory thresholds and pytest worker sizing stay as they are, so
the capacity measurement stays interpretable. Historical measurements stay
historical; only current-policy statements change.

## Definition of Done

- `make verify` green, including the capacity, nesting and lifecycle
  regressions of this spec.
- Moved in the same pull request: `docs/WORKFLOW.md`, `docs/orchestration.md`
  and `docs/how-it-works.md`, whose current capacity statements name the new
  default and its setting; no edit to dated measurements.
- Special runs: serial and paired full-check trials, recorded with their
  tested commit in `plans/changes/verify-slots/measurements.md` and the pull
  request body.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- The pull request closes the configurable-verification-capacity bead; its
  last commit carries `Closes-Bead: coding-harness-u1ha`. The runner owns
  commits.

## Open decisions

None open. The following reversible details are chosen visibly here, not
answered on the maintainer's behalf:

- [DETAIL] One optional `verify.slots` text file in the existing shared state
  root holds the capacity; absence means the sole declared default of two.
  This gives a machine-wide edit today without anticipating the future
  configuration system (its own change, bead `coding-harness-twvx`). A
  whitespace-trimmed positive decimal integer is the only accepted content;
  any other present content refuses. The value is re-read under admission
  coordination; a decrease drains existing reservations without cancelling
  them. Reason: one file, no code change, no per-checkout copies.
- [DETAIL] Exclusion with older checkouts is preserved by keeping the
  existing `verify.lock` as a compatibility lock the updated implementation
  takes shared; FIFO applies among the updated implementation's
  registrations, not across legacy schedulers. Reason: during rollout a
  machine must not silently allow a third check beside one old and one new.
- [DETAIL] Capacity is reserved before the memory wait, as the work lock is
  today. Reason: the admission boundary stays where it was, and waiting
  admissions stay bounded too.
- [DETAIL] Four hours of implementation, repairs and trials included, are
  the appetite; if it is exhausted, the change reports what stands and what
  evidence is missing. Reason: a stop the maintainer can see, not a silent
  overrun.
