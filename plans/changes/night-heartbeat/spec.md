---
title: "Spec — night-heartbeat"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-7x3c
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, night-run, heartbeat]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — night-heartbeat

Make the orchestrating session's recurring wake a standing part of every
unattended night run, with a durable lane list and an honest wake log (bead
coding-harness-7x3c). Research: `research.md`; scope: `decisions.md`,
`SKIP · interview`, recording the maintainer's decisions of 2026-11-05/06.

## Problem

- Lane supervision has depended on session-only timers: the research cites
  the stopped timer and the earlier interval with all lanes idle in
  `docs/journal/handover/2026-11-01-five-lane-night.md` (2026-11-01).
- The standing night rules describe capacity fallback and parking, but no
  mandatory wake routine (`docs/WORKFLOW.md`, “Night runs”, read at
  `d8b3bf8c`, 2026-11-06).
- The recorded 2026-11-05/06 trial needs its lessons made repeatable: a file
  of lanes, busy markers for work outside runner calls, removing parked
  lanes, and visible usage-limit gaps (`decisions.md`).

## Terms

- **Wake:** a scheduled return of control to the orchestrating session;
  elapsed time or a printed message alone does not establish delivery.
- **Active lane:** a lane with authorised work still eligible to run;
  parked work remains recorded but leaves the active watch list.
- **Busy marker:** a temporary record of actual orchestrator work in a lane
  that cannot be inferred from a running stage-2 command.

## Acceptance criteria

The contract is a documented operating routine executed by the orchestrator,
not enforcement inside the stage-2 runner.

1. When a night run enters unattended operation, its routine requires a
   scheduled wake of its orchestrating session after 30 minutes.
   *Refuted by:* setup can finish with no scheduled return of control, or an
   idle-only watchdog substitutes for the periodic wake.
2. When a night run starts, its routine requires keep-awake for the intended
   run period.
   *Refuted by:* setup permits unattended operation without enabling and
   checking keep-awake, or leaves its lifetime unspecified.
3. While a night run is active, its routine maintains a file identifying
   each watched lane and where to resume its authorised work.
   *Refuted by:* a wake needs chat memory to reconstruct the lanes or their
   next steps, or parked lanes remain eligible in the watch list.
4. While a lane is doing orchestrator work outside a runner call, its routine
   distinguishes that work from idle time using a busy marker with an owner
   and a named activity.
   *Refuted by:* absence of a runner process alone triggers duplicate work,
   or an abandoned marker can excuse a lane indefinitely without checking
   its owner's actual activity.
5. When a wake is handled, its routine appends exactly one timestamped
   lane-watch summary line covering all watched lanes and their resulting
   actions.
   *Refuted by:* the wake has no line, creates one line per lane instead of
   one summary, or describes unchecked lanes as healthy.
6. When a wake is handled and the run continues, its routine schedules the
   next wake after 30 minutes before returning to unattended work.
   *Refuted by:* the first wake is the last because nobody rearms it, or
   completing lane work is a prerequisite for rearming.
7. When a checked lane is idle and has eligible authorised work, its routine
   serves its next step during that wake without waiting for another wake.
   *Refuted by:* eligible work is knowingly left idle until the next timer;
   work needing a maintainer decision is started instead of being parked
   with its question for the morning.
8. If a usage limit, stopped session or missed wake interrupts supervision,
   its routine records the unobserved interval as a gap at resumption.
   *Refuted by:* missing wakes are backfilled as successful checks or the
   routine claims that a timer kept the unavailable session working.
9. When the night run ends or all remaining work is parked, its routine
   retires that run's wake and keep-awake resources.
   *Refuted by:* obsolete wakes continue serving a finished run or teardown
   stops resources owned by another run.

## Non-goals

- A new scheduler, daemon, model call, notification service or automatic
  restart of an unavailable session; delivery uses the harness's existing
  scheduling or background-completion facility.
- The broader lane diary/planner, status-line integration and automatic
  backlog selection proposed for lane planning and lane watch (beads
  coding-harness-4emv and coding-harness-5q2p).
- Runner process supervision, recap-lock repair, tracker lease renewal,
  new concurrency limits or new permission to merge or start work.
- Promoting the trial watchdog's 120-second polling and ten-minute idle
  threshold to standing requirements; the accepted periodic wake is 30 minutes.
- A universal promise to dispatch immediately between wakes: “at once” means
  at the check that detects idle work, also including ordinary job completion.

## Protected areas

`scripts/stage2.py`, runtime hooks, the status line, tracker storage, model
and gate configuration, and ADRs remain untouched: this change makes an
existing session practice repeatable. `AGENTS.md` is a held path; only the
orchestrator adds its authorised pointer after the accepted runner attempt.

## Definition of Done

- The routine in `docs/WORKFLOW.md` and the pointer in `AGENTS.md` agree.
- A recorded scenario walkthrough exercises every criterion, including a
  repeated wake, busy work, an idle lane, a parked question and a resumed gap.
- Required checks pass; the runner owns verification and the commit, and
  the orchestrator completes the held-path edit before final review.
- The pull request closes bead coding-harness-7x3c (permanent night-run wake)
  and its final commit carries `Closes-Bead: coding-harness-7x3c`.
- Protected areas and non-goals are checked against the pull request file list.
  No live overnight result is claimed from a scenario walkthrough.

## Open decisions

None open. The reasoned interview skip already records the maintainer's scope.

- [DETAIL] Deliver a standing operating procedure and one instruction pointer,
  rather than a new scheduler: existing harness wake facilities suffice for
  the accepted session practice and this keeps the bounded scope.
- [DETAIL] Use run-specific local files, UTC log timestamps, and explicit
  resource ownership so concurrent runs and missed observations are separable.
- [DETAIL] Set a one-hour phase-4 appetite, repairs included; this bounds a
  documentation change and its operational walkthrough, not an overnight trial.
- [DETAIL] Omit phase 2b and an ADR: the recorded class is bounded and this
  change introduces no architecture or external contract.
