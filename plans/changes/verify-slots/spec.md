---
title: "Spec — verify-slots"
status: draft
implementation_status: partial
date: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-16
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

The goal in one sentence: several independent protected checks may run at
once — three by the repository default (`decisions.md`, Q-7 addendum) — and the slot count and the pytest
workers per run are set in layers, read by one function, without a code
change (bead `coding-harness-u1ha` — configurable verification capacity).
Research: `research.md`. Decisions: `decisions.md` (Q-1 and Q-2 of
2026-11-09; Q-3 to Q-8 of 2026-11-14–16, which settle the default,
worker count and shared computation).

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
- The pytest worker count is a second, separate rule (half the logical cores,
  bounded by memory) copied into `scripts/verify_all.sh` and
  `scripts/stage2.py`; it knows nothing of the slot count, so more slots
  oversubscribe the cores, and the runner's environment allow-list drops a
  caller's worker variable (`decisions.md#Q-6`).

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

1. When independent protected checks contend and no machine settings file
   is present, the repository default of slots (three) is available across
   repositories and worktrees.
   *Refuted by:* an eligible check cannot reserve an idle slot below the
   default, or one more runs while every default slot is occupied.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-6`.

2. When capacity is changed in its single documented machine-wide setting
   (`slots` in the machine-local `verify.toml`), later reservation decisions
   use that positive integer, with no code edit and no per-checkout copy of
   the value.
   *Refuted by:* settings of one or three are ignored, different working
   directories select different values, or a lowered capacity grants new
   reservations before existing ones drain below it.
   *Basis:* `decisions.md#Q-2`.

3. If a present capacity setting is invalid or cannot be safely read,
   independent admission refuses with a diagnostic before any protected work.
   *Refuted by:* an empty, zero, negative, fractional, nonnumeric,
   substituted or unreadable setting, an unknown key or table, or a leftover
   bare `verify.slots` file silently selects a fallback, hangs, or lets work
   start.
   *Basis:* `decisions.md#Q-2` (one declared, validated value),
   `decisions.md#Q-6`.

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
    *Basis:* `decisions.md`, closing evidence note; `decisions.md#Q-2`;
    `decisions.md#Q-3` (under the night load) and `decisions.md#Q-4`
    (both runs within 1.6x a single run, no test red or flaky because of the
    parallelism).

12. When a verification run starts — through `scripts/verify_all.sh`, the
    admission or the runner's targeted pytest — one reading function
    (`read_settings` in `scripts/verify_lock.py`) supplies the slot count and
    the pytest workers per run using the same effective machine readings for
    every entry point: the validated repository default (three
    slots; workers = logical cores / slots, floored, at least one, bounded
    by 2 GiB of memory per worker across all slots), overridden per value by
    the machine-local `verify.toml` (`[verify]` with `slots` and
    `workers_per_run`), and for the workers by a caller's non-empty
    `PYTEST_XDIST_AUTO_NUM_WORKERS`, which passes verbatim. Every run logs
    the values in force and where each came from, on the operator's stderr
    as one `[verify-settings]` line printed by one helper
    (`log_settings`): `scripts/verify_all.sh` through `--settings`, the
    runner's targeted pytest before it launches; the admission's own line
    names the slot, the capacity and its source. Only the shell runner's
    full check also writes the values into the duration history; the
    targeted pytest writes no history record. A slot count above the logical
    cores adds a warning to both lines and never refuses.
    *Refuted by:* a caller of its own rule (a copied half-the-cores formula),
    workers that do not follow an overriding slot count, a caller's value
    rewritten, a runner-started full check whose worker count differs from a
    shell-started one under the same settings, CPU allocation and caller
    override, including a Linux process restricted to six CPUs on a
    24-core machine, a run whose log does not name the values and
    their sources, or the two paths printing the line through separate
    wordings.
    *Basis:* `decisions.md#Q-6`, `decisions.md#Q-8`.

13. When a run of `scripts/verify_all.sh` is recorded in the verify history,
    its start record names the slots and workers in force with their
    sources, and its end record the load average at the end and the peak
    summed resident memory of its pytest process trees, sampled every five
    seconds; a value that cannot be read is recorded as unknown, never as
    zero, and records written before these fields stay readable.
    *Refuted by:* a record without the values or sources, a missing sample
    recorded as a number, xdist workers left out of the peak, or the reader
    refusing an older record.
    *Basis:* `decisions.md#Q-6`, `decisions.md#Q-7` (the real-operation
    windows read these records).

## Non-goals

- Research-swarm invocation slots, automatic worker-count tuning, priority
  scheduling, continuous memory monitoring, new bypasses, or any change to
  which work needs admission (research, "Meaning B", "Protected areas").
- The future general harness configuration (bead `coding-harness-twvx` —
  central configuration); this change supplies only the slot and worker
  values and their one documented home, whose keys move there unchanged.
- The choice between 4 x 3, 3 x 4 and 2 x 6: the real-operation windows of
  `decisions.md#Q-7` make it after the merge; a kit rule is its own bead.
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
The existing memory thresholds stay as they are. The pytest worker sizing
changes only as `decisions.md#Q-6` and Q-8 state (criterion 12): the shared
reader supplies both the readings and the formula. Historical measurements
stay historical; only current-policy statements change.

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

- [DETAIL] One optional machine-local `verify.toml` in the existing shared
  state root holds the overrides (`[verify]`, keys `slots` and
  `workers_per_run`, positive integers up to 256 and 1024); absence means
  the repository default (`DEFAULT_SLOTS = 3` in `scripts/verify_lock.py`).
  It replaces the bare `verify.slots` file of the first implementation
  (2026-11-15): no criterion needs the old file, and none was in use on the
  machine, so it is not read as a fallback; a leftover one refuses with a
  diagnostic naming the new file, so a stale value never silently changes
  meaning. Any other present content refuses. The file is re-read under
  admission coordination; a decrease drains existing reservations without
  cancelling them. Reason: one file, no code change, no per-checkout
  copies, keys that move unchanged into bead `coding-harness-twvx`.
- [DETAIL] The shared Python reader obtains machine readings for all entry
  points, using the process's effective CPU allocation where available and
  the existing safe fallback when a reading is unavailable. Reason: Q-8
  removes conflicting shell and Python readings; caller overrides and the
  memory bound remain in force.
- [DETAIL] An explicit `workers_per_run` in the machine file is not bounded
  by memory. Reason: an operator's stated value wins, as a caller's
  environment value does.
- [DETAIL] A slot count above the logical cores (the shell's reading, else
  Python's) warns, it does not refuse (review round 5, row L5-6): the
  `[verify-settings]` line and the admission's reservation line carry
  "slots N (source) exceed the M logical cores; each run gets one worker and
  the machine is oversubscribed". Reason: `read_settings` refuses unusable
  *content* — a value that is not a positive integer within its bound — and
  such a slot count is valid content judged against a machine reading that
  may be absent or differ between machines (a hosted runner has fewer cores
  than the maintainer's machine, where the repository default of three still
  has to start); the admission's own log line never refuses. The bound of
  256 stays the refusal.
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
