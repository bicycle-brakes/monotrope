# ADR 0001 — Early parallelism: Omnigent coordinates coding workers from M0

* Status: proposed · amends D-3 and D-7 of the 2026-09-16 interview
* Review: pending (maintainer) · Deciders: framework-architect, maintainer
* Date: 2026-09-19

## Context

The interview outcomes D-3 (task granularity) and D-7 (Omnigent adoption)
sequenced parallel coordination late: one Bead per change first, Omnigent
parallelism at M3, and optional task Beads only where ownership demanded
them. On 2026-09-17 the maintainer reversed the sequencing explicitly:
Omnigent coordinates parallel coding from the first proof of concept. The
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
* Every rule this amends needs its enforcer updated before runtime activation
  (gate manifest, `coding-harness-bo0`).

## Validation

* [Acceptance scenarios](../architecture/2026-09-17-omnigent-first-target.md#acceptance-scenarios)
  "First parallel run" and "Second coordinator or stale result" pass in the
  throwaway repository.
* The run protocol (commands, reds, budget) is committed beside the run.
