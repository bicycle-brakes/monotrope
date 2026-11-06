---
title: "Spec — night-machine-facts"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-yql7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, night-run, machine-facts]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — night-machine-facts

One read-only command gives the night orchestrator a dated block of free
disk, swap, registered worktrees and running jobs to show before lanes start
(bead coding-harness-yql7, Machine facts at night-run start).
Research: `research.md`. Scope: the reasoned interview skip in `decisions.md`.

## Problem

- Machine pressure was invisible at night-run start: the incident of
  2026-11-01/02 ended with a full disk twice and 17.9 GB of swap used, and
  three runner jobs failed. The exploration records the incident and its
  handover sources under “The incident the bead answers” (`research.md`,
  exploration dated 2026-11-06).
- Night plans record machine state inconsistently; the existing run report
  reads processes and memory but not free disk, swap usage or worktree count.
  The exploration describes both gaps under “What night-run start is today”
  and “Machine-reading code that exists” (`research.md`, 2026-11-06).

## Terms

- **Snapshot:** observations collected during one invocation, labelled with
  its UTC start time; they are not an atomic measurement or a capacity promise.
- **Running jobs:** matched runner and verification process invocations on
  this host, using the existing run report's recognition; not unique lanes,
  logical jobs, remote jobs or all desktop applications.
- **Registered worktrees:** this repository's non-bare entries in Git's
  worktree list, including the main checkout and stale registrations.

## Acceptance criteria

1. When `python3 scripts/machine_facts.py` is invoked from a repository
   worktree, it prints one machine-facts block freshly collected for that
   invocation with a UTC date and time and labelled free-disk, swap,
   registered-worktree and running-job fields.
   *Refuted by:* a field or UTC stamp is missing, a stored snapshot is reused,
   or a second invocation with changed fixtures repeats the previous values.

2. When disk usage is readable, the free-disk field reports available space
   on the filesystem containing the invoking worktree with an explicit unit
   and that filesystem scope.
   *Refuted by:* a fixture with different home and worktree volumes reports
   home-volume space, reports used space as free, or omits the unit or scope.

3. When swap usage is readable on macOS or Linux, the swap field reports
   host-wide used and total swap with explicit units, including a readable
   zero when no swap is configured.
   *Refuted by:* used and total are confused, platform units are misconverted,
   or a valid zero-total fixture is labelled unreadable.

4. When Git's worktree list is readable, the worktree field reports the
   number of registered non-bare worktrees for this repository.
   *Refuted by:* a fixture containing a main checkout, linked and stale
   registrations, a bare entry and paths with whitespace yields the wrong
   count or counts unrelated filesystem directories.

5. When the process table and shared job definitions are readable, the
   running-job field lists each matched runner or verification invocation with process identifier,
   elapsed time, verb and change attribution where known, or explicitly says
   that none matched.
   *Refuted by:* a matched process disappears, an unrelated wrapper or quoted
   command becomes a job, an unknown change becomes a guessed name, or raw
   command arguments appear in the block.

6. If an individual source is unavailable, malformed or times out, its
   affected field says `not read` with a bounded source-specific reason while
   independently readable fields remain available and a valid command
   invocation exits zero.
   *Refuted by:* a failed source becomes zero or “none”, suppresses independent
   facts, exposes raw diagnostics, hangs on an unbounded subprocess, or
   changes the snapshot into a failing admission check.

7. While collecting the snapshot, the command only reads local facts and
   prints them, without writing files, changing Git or tracker state,
   contacting a network service, or starting, stopping, locking or admitting
   work.
   *Refuted by:* the invocation creates bytecode or a state file, runs a
   mutation or network command, calls the tracker, or changes another job.

8. When an orchestrator follows the night-start instructions, those
   instructions require running the command and showing its dated block in
   the main conversation before starting lanes, and retaining the block in
   the night plan's start-state record as an observation rather than an
   admission verdict.
   *Refuted by:* the instructions omit the command, its display before lane
   startup or its recording location, or describe the snapshot as a gate.

## Non-goals

- Disk or memory floors, admission changes, automatic refusal, cleanup,
  process termination, polling, alarms or resource sizing.
- Automatic night scheduling, morning scheduling, session hooks, a new
  machine-state database or historical series. The same command can be
  rerun for a fresh morning observation without adding automation.
- Additional load, port, service, timer or memory metrics; changing the
  existing run report, its warning threshold or verification event schema.
- A guarantee that showing the block prevents a full disk or catches every
  running process. Following the display instruction remains manual.
- Design phase 2b does not run for this bounded change; no architecture
  decision record is created or amended.

## Protected areas

The runner, verification admission and event writers (`scripts/stage2.py`,
`scripts/verify_lock.py`, `scripts/verify_all.sh`,
`scripts/verify_duration.py`) retain their behavior. The existing report and
its tests (`scripts/run_report.py`, `tests/test_run_report.py`) remain
unchanged. No edits to `AGENTS.md`, `docs/WORKFLOW.md`, `Makefile`, ADRs,
prompts, templates, tracker data or harness configuration are needed: the
night-start usage belongs in `docs/orchestration.md`.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green at the implementation head.
- Code, tests and usage move together: `scripts/machine_facts.py`,
  `tests/test_machine_facts.py`, `docs/orchestration.md`; change evidence stays
  in this folder and the runner regenerates `plans/INDEX.md`.
- The pull request's file list shows the protected areas untouched and the
  non-goals unbuilt.
- The pull request closes the machine-facts work item and its last commit
  carries `Closes-Bead: coding-harness-yql7`.
- Special runs: none; deterministic macOS/Linux fixtures verify readings
  without depending on the developer machine's current pressure.

## Open decisions

None open. The following reversible details are chosen here, with reasons;
they do not replace or add maintainer answers.

- [DETAIL] Use the standalone command `python3 scripts/machine_facts.py`:
  it supplies the requested small block without changing `make report`.
- [DETAIL] Use worktree-volume disk space, host-wide swap, registered
  non-bare worktree count and process rows as defined above: these have
  reproducible scopes and avoid claiming lane or cleanup state.
- [DETAIL] Support macOS and Linux, label units explicitly, bound subprocess
  reads to two seconds each, and report unavailable facts independently:
  these follow the existing report's platforms and snapshot semantics.
- [DETAIL] Reuse the existing report's process recognizer and bounded command
  reader; do not add a second definition of runner jobs.
- [DETAIL] Document manual display and recording in `docs/orchestration.md`:
  there is no shared night-start executable to wire into, and automatic
  hooks would exceed the recorded scope.
- [DETAIL] Set a two-hour phase-4 appetite, repairs included, as a stop for
  this small local command and its fixture tests; no prior appetite is stated.
