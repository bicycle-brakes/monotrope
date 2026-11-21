---
title: "Measurements — verify-two-slots"
category: measurements
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3-flash, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [measurements, verification]
---

# Measurements — verify-two-slots

**Status: the criterion-12 trial has not run yet.** This file is the record
the trial will fill; every measurement below is outstanding. The implement
attempt of 2026-11-21 ran on file tools only (no command execution), so it
could not start `make verify` in two worktrees, could not sample memory
externally and could not observe admissions. The trial belongs to the
command-bearing stage of this change (plan build sequence step 5) and must
run there, before phase 6.

## Trial — two simultaneous `make verify` against one serial run

Required by spec criterion 12 (`spec.md`); the 1.6 threshold is carried by
the 2026-11-17 handover. Every field below is pending; a trial recorded with
any of them missing is invalid.

| Field | Requirement | Recorded |
| --- | --- | --- |
| Trial revision | committed revision whose final `scripts/` tree matches HEAD: `git diff <trial-commit>..HEAD -- scripts/` empty | pending |
| Worktrees | two separate worktrees at the trial revision | pending |
| Warm-up | one discarded warm-up per worktree, before the serial run; warm-up identifiers and order recorded | pending |
| Order | warm-ups, then the serial run, then the simultaneous pair; each trial started with both slots free | pending |
| Date and settings | date, `HARNESS_VERIFY_SLOTS` and worker calculation (unchanged default) recorded | pending |
| Verdicts and exits | all three invocations exit zero | pending |
| Wall times | each invocation's launch-to-exit wall time, individual | pending |
| Execution seconds | per invocation | pending |
| Admission wait | combined queue-plus-memory wait seconds, per invocation | pending |
| Ratios | each simultaneous run's wall time over the serial run's, at most 1.6 | pending |
| Load | background processes/lanes; start and end 1-, 5- and 15-minute load averages | pending |
| Memory | starting and minimum available memory percentage; an external sampler reading `verify_lock.read_available_memory()` every five seconds, gaps over 15 seconds invalidate | pending |
| Admission observation | every protected admission seen in each run, with intervals; no extra admission over the serial run, no third admission over the pair | pending |
| Failure attribution | a failed parallel test rerun serially on the same revision: serial pass = parallelism-caused, serial failure = content failure; stop and report on any trial failure | pending |

## Scope notes

- One paired trial demonstrates zero observed failures, not a statistical
  absence of flakes; no long-run claim is made from it.
- A later change to `scripts/` after a recorded trial invalidates it and
  requires the complete trial again, within the four-hour appetite.
  Documentation-only, test-only or plans changes after the trial are
  verified and noted here without a rerun.
- If any trial run fails or cannot run — including a non-test gate failure
  or a timeout — the trial stops and reports; nothing is recorded as a pass.
