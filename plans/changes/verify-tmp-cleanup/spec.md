---
title: "Spec — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-12
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, temporary-files]
class: bounded
appetite: 6
adr_files: []
neighbours: [docs/research/2026-11-09-make-verify-long-term.md]
---

# Spec — verify-tmp-cleanup

Each verification runner owns and removes its pytest temporary area, with
explicit failed-run retention and next-start recovery after a hard kill
(bead coding-harness-bxxt.3 — verification temporary-folder cleanup).
Research: `research.md`. Decisions: `decisions.md`, answered Q-1 of 2026-11-12.

## Problem

- Exploration on 2026-11-10 found no run-specific pytest temporary root or
  end-of-run file cleanup; pytest instead prunes numbered roots on a later
  session (`research.md`, "What exists today" and "What cleans up today").
- The orchestrator reported 1.3 and 1.5 GiB left by finished runs and a full
  volume on 2026-11-09; these are reported figures, not measurements repeated
  by this draft (`research.md`, "Intent of the bead").
- The maintainer rejected the large supervisor-based implementation and
  chose runner-owned, process-id-named folders with dead-process cleanup at
  startup (`decisions.md#Q-1`, answered 2026-11-12). The rollback at
  `86242545` removes that implementation; at `a320748b` the runner again has
  no temporary-area lifecycle (`research.md`, "Current baseline — 2026-11-12").

## Terms

**Run:** An admitted execution of `scripts/verify_all.sh`, including job
subsets and `--ci`; `--list` executes no gates and owns no area.
**Run area:** A private directory named after the executing runner's process
id, containing that run's pytest session roots.
**Orphan:** An unretained managed run area whose named process no longer
exists; this is a process-id check, not descendant tracking.
**Retained:** Explicitly kept for inspection, excluded from orphan sweeping.

## Acceptance criteria

1. When an admitted run starts, it receives its own process-id-named area,
   including when it inherits admission from an ancestor.
   *Refuted by:* Two live runs share an area or a nested run deletes its parent's area.
   *Basis:* decisions.md#Q-1.
2. When a pytest session inherits the run's environment, its temporary root
   and xdist worker directories lie inside that run area.
   *Refuted by:* Real serial/parallel probes or a second session report a
   temporary path outside the area or erase another session's root.
3. When a run ends normally without requested retention, it removes its
   area before returning its original verification status.
   *Refuted by:* Success or failure leaves payloads, or successful removal
   changes a gate verdict.
   *Basis:* decisions.md#Q-1.
4. When the runner handles SIGINT, SIGTERM, SIGHUP or SIGQUIT, it applies
   end-of-run area cleanup before exiting, unless retention was requested.
   *Refuted by:* A handled interruption leaves unretained payloads or the
   existing public supervisor's 128-plus-signal status is lost.
   *Basis:* decisions.md#Q-1.
5. If `HARNESS_VERIFY_KEEP_TMP=1` is set and a run ends unsuccessfully,
   its area remains available at an absolute path reported to the caller.
   *Refuted by:* Failure/interruption removes requested evidence, no path is
   reported, or the next run sweeps that evidence.
6. When a run succeeds, it removes its area regardless of the retention variable.
   *Refuted by:* A successful run with `HARNESS_VERIFY_KEEP_TMP=1` leaves payloads.
7. When a later run starts under the same managed parent, it removes
   unretained sibling areas whose named processes no longer exist.
   *Refuted by:* An area left by a hard-killed and reaped runner survives
   that startup, or an area named for a live process is reclaimed.
   *Basis:* decisions.md#Q-1.
8. While managing run areas, verification leaves unrelated paths and
   symlink targets untouched.
   *Refuted by:* A live sibling area, caller-parent sentinel, historical
   pytest root, non-managed entry or substituted symlink target changes.
9. If allocation or required cleanup cannot complete safely, the invocation
   reports the affected path and reason and returns an unsuccessful status.
   *Refuted by:* Gates start after failed allocation, removal failure is
   silent, or the final status is success despite a storage failure.
10. When run-area management is active, gate commands, admission reuse,
    worker selection, duration ownership and execution verdicts keep their contracts.
    *Refuted by:* A command pin changes, nested work queues behind its own
    ancestor, duration ownership/worker overrides change, or `--list`
    allocates an area or enters admission.
11. If inherited pytest options select an explicit basetemp, the runner
    refuses before gates with an explanation.
    *Refuted by:* An accepted basetemp spelling escapes management,
    malformed quoting proceeds silently, or unrelated pytest options are discarded.
12. When a git command of the runner fails, its diagnostic keeps git's
    reason line whole however long the temporary path in it is
    (`decisions.md#Q-2`, `decisions.md#Q-3`).
    *Refuted by:* A long path pushes the reason (for a held lock,
    `index.lock`) out of the diagnostic, or a warning line before git's
    `fatal:` or `error:` line replaces the reason.

## Non-goals

- Standalone Stage-2 targeted, cheap and red-first checks, direct `make test`
  or pytest calls, and subprocesses replacing the inherited pytest environment.
- Historical `pytest-of-*` roots, arbitrary temporary files, kit scratch
  repositories and application caches; only managed run areas are reclaimed.
- A free-disk admission floor (separate work, bead coding-harness-87b0 —
  minimum free disk space), admission policy, scheduling or gate membership.
- A supervisor/lease registry, descendant liveness proof, process-group
  changes, a retention expiry policy or an inspection interface.
- Design phase 2b and an ADR: Q-1 keeps this a bounded runner change.

## Protected areas

`scripts/verify_lock.py` stays unchanged, as Q-1 explicitly requires; so do
`tests/test_verify_lock.py` and the admission/process-group contract.
`decisions/gates.yaml`, `Makefile`, `pyproject.toml`,
`scripts/kit/probe.py` and `scripts/verify_duration.py` stay unchanged: the
existing commands, dependencies, separate entry points and duration
ownership do not need edits. No held harness/governance path is edited.
`scripts/stage2.py` and `tests/test_stage2.py` change only for criterion 12:
the one helper that shortens a git error and its test (`decisions.md#Q-2`,
`decisions.md#Q-3`), and the C locale (`LC_ALL=C`) for every git command the
runner starts, so git's reason line is English and recognisable (loop row
L3-1 of 2026-11-13).

## Boundary

A hard kill cannot run an exit trap: its unretained area stays until a later
run under the same parent observes the runner process gone. A reused process
id may defer reclamation. A dead runner's surviving descendants do not keep
its area alive; the process-id rule promises no descendant-protection lease
or ordering of area removal after the last descendant stops. Existing
process-group supervision remains responsible for processes. An inaccessible
or unsafe candidate is reported and left untouched. Runs using another
parent cannot recover this parent's orphans. Retained areas require manual
removal; an explicit retention request with an unknown hard-kill outcome is
preserved conservatively.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green at the implementation commit.
- The pull request carries `scripts/verify_all.sh`, `tests/test_ci.py`,
  `scripts/stage2.py`, `tests/test_stage2.py` (criterion 12 only) and the
  change artifacts; the orchestrator regenerates `plans/INDEX.md`.
- The file list shows the protected areas untouched and non-goals unbuilt.
- The pull request closes bead coding-harness-bxxt.3 — verification temporary-folder
  cleanup; its final commit carries `Closes-Bead: coding-harness-bxxt.3`.
- Revision-bound isolated probes cover real pytest/xdist placement, normal
  exit, interruption, retention and next-start hard-kill recovery.

## Open decisions

None open. The maintainer's answered Q-1 replaces the earlier interview skip
and the supervisor-based plan; Q-2 and Q-3 (2026-11-12) add the git-error
helper of criterion 12 and raise the appetite to six hours.

- [DETAIL] Exactly `HARNESS_VERIFY_KEEP_TMP=1` requests retention; other
  values remove normally, because keeping evidence must be explicit.
- [DETAIL] Use a private per-user managed parent beneath the caller's
  `PYTEST_DEBUG_TEMPROOT`, or platform temporary parent when unset. Preserve
  that parent for nested runs and leave `TMPDIR` unchanged, so only inherited
  pytest sessions move and nested runs can find sibling orphans.
- [DETAIL] Publish the retention request before gates, so startup recovery
  cannot discard requested evidence after an unknown hard-kill outcome.
- [DETAIL] Preserve an existing nonzero/signal status on removal failure;
  return 2 after otherwise successful work and report the failure, so a
  storage failure cannot turn verification green.
- [DETAIL] Refuse explicit basetemp options rather than silently rewriting
  caller options; retain all unrelated options unchanged.
- [DETAIL] The phase-4 appetite is six hours, repairs included (raised from
  four by the maintainer on 2026-11-12, `decisions.md#Q-3`); rejected attempts
  already recorded in `findings.md` count against it.

These reversible details are decided here with their reasons; they do not
reopen Q-1 or add a supervisor lifecycle.
