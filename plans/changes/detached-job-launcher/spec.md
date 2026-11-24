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

## Terms

**Runner verb:** a command whose argument vector invokes `scripts/stage2.py` with a known verb, as recognised by `run_report.py`. Model starts by runner verbs remain routed through `scripts/stage2.py`; the launcher accepts arbitrary commands (decision Q-12).

## Acceptance criteria

1. When `scripts/jobs.py start` receives any command, it starts that command in its own window on the dedicated `tmux -L coding-harness` server and the command survives termination of the caller's process tree and its own tmux sessions.
   *Refuted by:* The command stops with either caller boundary or shares a window.
   *Basis:* `decisions.md#Q-8`.

2. If the tmux binary is missing, start refuses before running the command and identifies the missing prerequisite.
   *Refuted by:* The command runs or the diagnostic does not identify tmux.
   *Basis:* `decisions.md#Q-7`, `decisions.md#Q-8`.

3. When `jobs.py stop` targets a running job, it ends the started command’s process tree, including descendants in separate sessions, and leaves the wrapper alive to record `signal 15` and then exit; the verify admission is released and other jobs keep running.
   *Refuted by:* A command descendant or admission survives, the wrapper cannot record `signal 15`, or another job stops.
   *Basis:* `decisions.md#Q-10`, `decisions.md#Q-13`.

4. When a job starts, its per-job record under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs/` contains the command, whether it is a runner verb, started command PID, wrapper PID, recorded process group, tmux window, start time and log path.
   *Refuted by:* A field or the location is wrong.
   *Basis:* `decisions.md#Q-4`, `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-13`.

5. When a job ends, its wrapper records the end time and actual exit code or `signal N` for signal death, retaining the finished record for 14 days.
   *Refuted by:* The outcome is wrong or the record disappears before 14 days.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-10`.

6. When `jobs.py list` runs, it shows running jobs, retained lost jobs and jobs finished in the last 24 hours, while `--all` shows all retained records.
   *Refuted by:* A qualifying job is omitted or an older finished job appears without `--all`.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-14`.

7. When `run_report.py` reports a running detached job, it reads its record and deduplicates it against process recognition by the started command PID.
   *Refuted by:* The job is omitted or counted twice when both sources identify it.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-13`.

8. When a detached job runs verification, it obtains its own existing machine-wide admission, including the two-slot limit and memory floor, even if its caller holds an admission.
   *Refuted by:* It inherits a held admission, bypasses the gate or exceeds its limits.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-9`.

10. When the launcher is installed through the kit, its mechanism and required dependencies are available in the destination repository.
    *Refuted by:* The installed kit cannot invoke the launcher because a required mechanism is absent.
    *Basis:* `decisions.md#Q-7`.

11. When the launcher is added, the continuous integration caller declaration identifies its caller.
    *Refuted by:* The caller check finds the launcher undeclared.
    *Basis:* `decisions.md#Q-7`.

12. While detached jobs run, only the orchestrator or `lanes.py` writes lane and busy markers.
    *Refuted by:* The launcher writes either kind of marker.
    *Basis:* `decisions.md#Q-4`.

13. When the architecture decision takes effect, it quotes the exact non-goal sentences of night-heartbeat and night-stall-guard and exempts only detached runner jobs, retaining their exclusions of a scheduler, daemon and automatic restart.
    *Refuted by:* Either sentence is missing or another exclusion is lifted.
    *Basis:* `decisions.md#Q-6`, `decisions.md#Q-11`.

14. While `lanes.py advance` has not landed, night runs retain the recurring 30-minute wake.
    *Refuted by:* The updated guidance removes the wake before advance lands.
    *Basis:* `decisions.md#Q-6`.

15. When the background guidance is updated, it requires `jobs.py` for runner verbs that run a full `make verify` and for a bare `make verify`, permits harness background mode for short commands and retains the interim wake.
    *Refuted by:* Either route or the wake is omitted or contradicted.
    *Basis:* `decisions.md#Q-11`, `decisions.md#Q-6`, `decisions.md#Q-12`.

16. When a job starts, it receives the caller's working directory, PATH including its virtual-environment prefix, `VIRTUAL_ENV`, `XDG_STATE_HOME` and `HARNESS_VERIFY_*` values, excluding `HARNESS_VERIFY_LOCK_HELD`, `HARNESS_VERIFY_LOCK_TOKEN`, `HARNESS_VERIFY_ADMISSION_ID` and `HARNESS_VERIFY_ADMISSION_WAIT`.
    *Refuted by:* The job observes a server value instead of a supplied caller value or inherits any of the four excluded admission values.
    *Basis:* `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-14`.

17. If a job's wrapper PID is gone without an end record, `jobs.py list` reports it as lost until its record is pruned 14 days after its start.
    *Refuted by:* The vanished job remains running or is reported as successfully finished.
    *Basis:* `decisions.md#Q-10`, `decisions.md#Q-13`, `decisions.md#Q-14`.

18. When no dedicated tmux server exists, start creates it detached and launches the job without requiring an attached tmux session.
    *Refuted by:* A caller outside tmux cannot launch despite an available tmux binary.
    *Basis:* `decisions.md#Q-8`.

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
