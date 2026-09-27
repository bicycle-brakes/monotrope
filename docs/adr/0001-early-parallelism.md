# ADR 0001 — Early parallelism: Omnigent coordinates coding workers from M0

* Status: accepted, superseded by ADR 0006 (2026-09-27) · amends D-3 and
  D-7 of the 2026-09-16 interview
* Review: accepted by the maintainer, 2026-09-22, with the changes of that
  review · Decider: maintainer · prepared by a framework-architect session
* Date: 2026-09-19 · accepted 2026-09-22
* Note, 2026-09-27: [ADR 0006](0006-parallel-work-without-a-pilot.md)
  (accepted 2026-09-27) supersedes this decision. The maintainer dropped
  the M0 pilot on 2026-09-23; parallel sessions now run from M1, each in a
  worktree of its own, and W0 and W1 lapse. The text below is kept as the
  record of the earlier design.

## Context

D-7 already set the full adoption path M0–M4 "starting now"; what it left
late was the *content* of M0: a single sandboxed session running one task
loop, with parallel workers only at M3. D-3 (task granularity) tied task
Beads to that: one Bead per change, task Beads under an epic only once
stage 2 has two workers claiming. On 2026-09-17 the maintainer moved both
forward: M0 itself runs two coordinated workers, and D-3's two-worker
condition is met at M0, not at stage 2. The
[decision continuity table](../architecture/2026-09-17-omnigent-first-target.md#decision-continuity)
records both amendments; this ADR is the runtime record the table points to.

## Decision Drivers

* The maintainer wants parallel workers proven early, not after routine use.
* One writer per tracker must survive the change (house rule, AGENTS.md).
* The M0 pilot must stay cheap enough to abort without loss.

## Considered Options

* **(a) Parallel coordination starts at M0; serial path stays the fallback.**
* (b) Keep D-7 as recorded — parallel at M3 only.
* (c) Parallelism without the disposable-repository constraint.

## Decision

**(a)**, with these contracts:

* M0 proves two coding workers in isolated worktrees under one fenced
  coordinator, in a throwaway repository, with `main` untouched until a human
  merge.
* D-3, amended in timing: M0 may use coordinator-claimed task Beads under the
  change epic when separate ownership is needed; plan steps keep stable IDs;
  discovered work gains a `discovered-from` edge. **Worker-side tracker
  writes remain forbidden** — the coordinator is the only writer (ADR 0002).
* Adoption re-sequences to M0 (two-worker pilot) → M1 (routine Bounded work)
  → M2 (Feature + cross-vendor) → M3 (qualified unattended runs) → M4
  (justified hardening). W0 (isolated worktrees) and W1 (authorized exclusive
  coordinator) are mandatory M0 prerequisites; W2 (direct worker tracker
  writes) branches independently after M0, only if direct writers are needed.

## Consequences

* The serial path remains the fallback; an M0 abort returns to it without
  reopening unrelated decisions.
* The pilot must measure throughput, findings, human time and cost against a
  serial baseline before M1.
* Every rule this amends needs its enforcer in the gate file
  (`decisions/gates.yaml`, in place since `coding-harness-bo0` closed) before
  runtime activation. The enforcers for W0 (isolated worktrees) and W1
  (exclusive coordinator writer) do not exist yet; they get their own Bead
  when this ADR is accepted.

## Validation

* [Acceptance scenarios](../architecture/2026-09-17-omnigent-first-target.md#acceptance-scenarios)
  "First parallel run" and "Second coordinator or stale result" pass in the
  throwaway repository.
* The run protocol (commands, reds, budget) is committed beside the run.
