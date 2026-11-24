---
title: "Spec — detached-job-launcher"
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-a6ns.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, jobs, night-run]
class: architectural
appetite: 8
adr_files: [docs/adr/0026-detached-job-launcher.md]
neighbours:
  - plans/changes/archive/2026-11-06-verify-machine-lock/spec.md
  - plans/changes/archive/2026-11-16-night-heartbeat/spec.md
  - plans/changes/archive/2026-11-16-night-machine-facts/spec.md
  - plans/changes/archive/2026-11-16-night-stall-guard/spec.md
  - plans/changes/hermes-runner/spec.md
  - plans/changes/stage2-session/spec.md
---

# Spec — detached-job-launcher

Runner jobs survive the launching session and remain observable (bead coding-harness-a6ns.1). Research: `research.md`; decisions: `decisions.md`.

## Problem

- The runner tracks child groups in the launching process and kills them on session termination; excluding them leaves no durable lifecycle record (research run 28bf813a, 2026-11-23, reconciliation applicability).
- Existing reporting recognises runner verbs from processes, and no mapped test proves survival after the orchestrator exits (same run and date, applicability).
- A detached verify job can lose or contend with its admission if ownership is mishandled (same run and date, applicability).

## Acceptance criteria

1. When a caller starts a runner command through `scripts/jobs.py start`, it runs in its own observable tmux window and continues after the launching session ends.
   *Refuted by:* Ending the launcher session terminates the job or no separate window exists.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`.

2. If tmux is unavailable, start refuses before launching the command and reports the missing prerequisite.
   *Refuted by:* A command starts or the diagnostic does not identify tmux.
   *Basis:* `decisions.md#Q-7`.

3. When a caller requests `jobs.py stop` for a running job, only the selected job is stopped.
   *Refuted by:* The selected job continues or another job is terminated.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`.

4. When a job starts, its durable record contains its command, tmux window, start time and log path in the shared runner state directory.
   *Refuted by:* A required field is absent or the record is outside the shared state directory.
   *Basis:* `decisions.md#Q-4`.

5. When a job ends, its record retains its end time and actual exit code.
   *Refuted by:* A finished job has no end time, loses its record or reports the wrong exit code.
   *Basis:* `decisions.md#Q-4`.

6. While a job is running, `jobs.py list` identifies it as running.
   *Refuted by:* A running job is missing or reported as finished.
   *Basis:* `decisions.md#Q-4`.

7. While a job is running, `run_report.py` identifies it as running.
   *Refuted by:* The report omits the running job or reports it as finished.
   *Basis:* `decisions.md#Q-4`.

8. When a detached job runs verification, it uses the existing machine-wide verify admission, including its two-slot limit and memory floor.
   *Refuted by:* Detached verification runs outside the existing admission or exceeds its limits.
   *Basis:* `decisions.md#Q-3`.

9. When a model is started by a detached job, the model invocation still goes through `scripts/stage2.py`.
   *Refuted by:* A launcher route invokes a model directly.
   *Basis:* `decisions.md#Q-1`.

10. When the launcher is installed through the kit, its mechanism and required dependencies are available in the destination repository.
   *Refuted by:* The installed kit cannot invoke the launcher because a required mechanism is absent.
   *Basis:* `decisions.md#Q-7`.

11. When the launcher is added, the continuous integration caller declaration identifies its caller.
   *Refuted by:* The caller check finds the launcher undeclared.
   *Basis:* `decisions.md#Q-7`.

12. While detached jobs run, only the orchestrator or `lanes.py` writes lane and busy markers.
   *Refuted by:* The launcher writes either kind of marker.
   *Basis:* `decisions.md#Q-4`.

13. When the architecture decision takes effect, it supersedes the headless-job non-goals of night-heartbeat and night-stall-guard.
   *Refuted by:* The decision leaves either non-goal in force.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-6`.

14. While `lanes.py advance` has not landed, night runs retain the recurring 30-minute wake.
   *Refuted by:* The updated guidance removes the wake before advance lands.
   *Basis:* `decisions.md#Q-6`.

15. When the background-mode guidance is updated, it describes detached job launching and retains the interim wake.
   *Refuted by:* The guidance requires session-bound launching or omits the interim wake.
   *Basis:* `decisions.md#Q-6`.

## Non-goals

- Automatic lane advancement, scheduling, removing the wake, and changing the model routing or verification quota.
- A new permissions policy: the central policy is separate work (bead coding-harness-a6ns.2).
- Surviving a machine shutdown or tmux server termination; restarting a completed job automatically.

## Protected areas

The lane and busy-marker writers, verify admission policy and model invocation routes remain authoritative.

## Definition of Done

- `make verify` green; the pull request carries `docs/adr/0026-detached-job-launcher.md` and the updated background guidance.
- The file list shows protected areas and non-goals respected; the pull request closes the detached launcher bead and its last commit carries `Closes-Bead: coding-harness-a6ns.1`.
- A real tmux survival and exit-status run is recorded with its commit in the pull request.

## Open decisions

[DETAIL] Use an eight-hour phase-4 stop, including repairs: the interview sets no appetite and this leaves room for lifecycle and integration checks. The exact record encoding and command syntax are revisable implementation details specified in the plan.
