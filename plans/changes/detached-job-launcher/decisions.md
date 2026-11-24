---
title: "Decisions — detached-job-launcher"
category: decisions
status: draft
implementation_status: none
date: 2026-11-24
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-a6ns.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, night-run, jobs, tmux]
---

# detached-job-launcher — Decisions

Class: architectural (bead coding-harness-a6ns.1; it changes how night runs supervise runner jobs and needs a new ADR). The interview ran in the conversation of session c820a13d on 2026-11-24; the answers are recorded below with the options as they were put. Basis: research run 28bf813a.

## Q-1 · Entry point

asked: 2026-11-24
answer: "Own tool `scripts/jobs.py` (`jobs.py start|list|stop`), harness-independent; it starts any runner command detached; `scripts/lanes.py advance` (bead coding-harness-z40g) uses it; model starts still go only through scripts/stage2.py. Options put: own tool scripts/jobs.py; a `lanes.py launch` subcommand; a runner verb in scripts/stage2.py (the orchestrator's earlier recommendation, changed in view of the maintainer's wish for modularity and portability across harnesses)."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-4
  - 28bf813a6f483b16b5453a54f8fbe327/H-5
  - 28bf813a6f483b16b5453a54f8fbe327/H-14
  - 28bf813a6f483b16b5453a54f8fbe327/H-15
  - 28bf813a6f483b16b5453a54f8fbe327/H-17
  - 28bf813a6f483b16b5453a54f8fbe327/H-20
  - 28bf813a6f483b16b5453a54f8fbe327/H-29
  - 28bf813a6f483b16b5453a54f8fbe327/H-31
  - 28bf813a6f483b16b5453a54f8fbe327/H-35
  - 28bf813a6f483b16b5453a54f8fbe327/H-60
context: |
  Topic: where the detached launcher lives.
  Intention: modular and portable across harnesses (maintainer, same session, bead coding-harness-z40g Q-2).
  Today: runner jobs are started by hand with nohup and die with the session's kill_live.
  Repository change: new scripts/jobs.py.
  Architecture change: a launcher module beside the runner.

In the context of runner jobs that must outlive a session, facing a runner verb or an own tool, we decided on an own tool scripts/jobs.py, to achieve a modular launcher any harness can call, accepting one more entry point. — 2026-11-24

## Q-2 · Survival boundary and mechanism

asked: 2026-11-24
answer: "tmux window — each job runs in its own tmux window, outside the launching session's process group, so it survives the session's end and can be watched. Options put: own process session via setsid, macOS first (recommended); a one-shot launchd job; a tmux window."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-1
  - 28bf813a6f483b16b5453a54f8fbe327/H-2
  - 28bf813a6f483b16b5453a54f8fbe327/H-8
  - 28bf813a6f483b16b5453a54f8fbe327/H-9
  - 28bf813a6f483b16b5453a54f8fbe327/H-10
  - 28bf813a6f483b16b5453a54f8fbe327/H-12
  - 28bf813a6f483b16b5453a54f8fbe327/H-13
context: |
  Topic: how a job survives the end of the launching session.
  Intention: no lost jobs when a session ends; jobs can be watched live.
  Today: Claude Code kills the processes of its session on exit (kill_live).
  Repository change: jobs.py starts each job in a tmux window and checks tmux as a prerequisite.
  Architecture change: tmux becomes the job host of night runs.

In the context of jobs that must outlive a session, facing setsid, launchd or tmux, we decided on a tmux window per job, to achieve survival plus live observation, accepting tmux as a prerequisite. — 2026-11-24

## Q-3 · Verify admission

asked: 2026-11-24
answer: "A — a detached verify-bearing job holds the verify admission like any run (at most two concurrent make verify, memory floor); no bypass, the two-slot lock stays the one gate. Option B was an own quota."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-3
  - 28bf813a6f483b16b5453a54f8fbe327/H-42
  - 28bf813a6f483b16b5453a54f8fbe327/H-48
  - 28bf813a6f483b16b5453a54f8fbe327/H-59
context: |
  Topic: detached jobs and the verify admission.
  Intention: no memory overload at night.
  Today: the two-slot verify lock admits every run.
  Repository change: none beyond using the existing admission.
  Architecture change: none.

In the context of detached verify-bearing jobs, facing an own quota or the shared lock, we decided on the shared admission, to achieve one gate, accepting that jobs may wait. — 2026-11-24

## Q-4 · Records and visibility

asked: 2026-11-24
answer: "A — job records (command, tmux window, start, end, exit code, log path) live beside the loop records in the runner state directory ($XDG_STATE_HOME/coding-harness/), harness-neutral; `jobs.py list` and run_report show running jobs; the lanes file and busy markers stay written by the orchestrator or lanes.py only. Option B relied on tmux alone."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-6
  - 28bf813a6f483b16b5453a54f8fbe327/H-7
  - 28bf813a6f483b16b5453a54f8fbe327/H-34
  - 28bf813a6f483b16b5453a54f8fbe327/H-47
  - 28bf813a6f483b16b5453a54f8fbe327/H-55
context: |
  Topic: where job state is recorded.
  Intention: exit codes survive the window; every harness sees the same state.
  Today: no job records; logs are ad-hoc files.
  Repository change: a job record format in the state directory; run_report reads it.
  Architecture change: none.

In the context of detached jobs, facing tmux-only or recorded state, we decided on job records beside the loop records, to achieve visible, lasting outcomes, accepting a small record format. — 2026-11-24

## Q-5 · Class and ADR

asked: 2026-11-24
answer: "A — architectural; one new ADR (the next free number at merge) for the change of night-run supervision: detached jobs in tmux instead of session background processes. Option B was feature without ADR."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-18
  - 28bf813a6f483b16b5453a54f8fbe327/H-19
  - 28bf813a6f483b16b5453a54f8fbe327/H-22
  - 28bf813a6f483b16b5453a54f8fbe327/H-23
  - 28bf813a6f483b16b5453a54f8fbe327/H-24
  - 28bf813a6f483b16b5453a54f8fbe327/H-25
  - 28bf813a6f483b16b5453a54f8fbe327/H-26
  - 28bf813a6f483b16b5453a54f8fbe327/H-27
  - 28bf813a6f483b16b5453a54f8fbe327/H-28
  - 28bf813a6f483b16b5453a54f8fbe327/H-49
context: |
  Topic: class and decision record.
  Intention: the change alters how night runs are supervised.
  Today: night-heartbeat and night-stall-guard rules assume session-bound jobs.
  Repository change: a new ADR.
  Architecture change: night-run supervision.

In the context of night-run supervision, facing an unrecorded change, we decided on class architectural with a new ADR, to achieve a recorded decision, accepting one more ADR. — 2026-11-24

## Q-6 · Doctrine it changes

asked: 2026-11-24
answer: "A — the new ADR explicitly supersedes the night-heartbeat and night-stall-guard non-goals on headless jobs and amends the AGENTS.md background-mode bullet; the 30-minute wake stays until `lanes.py advance` (bead coding-harness-z40g) lands. Option B dropped the wake at once."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-21
  - 28bf813a6f483b16b5453a54f8fbe327/H-32
  - 28bf813a6f483b16b5453a54f8fbe327/H-36
  - 28bf813a6f483b16b5453a54f8fbe327/H-38
  - 28bf813a6f483b16b5453a54f8fbe327/H-39
  - 28bf813a6f483b16b5453a54f8fbe327/H-40
  - 28bf813a6f483b16b5453a54f8fbe327/H-41
  - 28bf813a6f483b16b5453a54f8fbe327/H-43
  - 28bf813a6f483b16b5453a54f8fbe327/H-44
  - 28bf813a6f483b16b5453a54f8fbe327/H-45
  - 28bf813a6f483b16b5453a54f8fbe327/H-46
  - 28bf813a6f483b16b5453a54f8fbe327/H-54
  - 28bf813a6f483b16b5453a54f8fbe327/H-56
  - 28bf813a6f483b16b5453a54f8fbe327/H-57
context: |
  Topic: existing rules that detached jobs touch.
  Intention: no silent contradiction with earlier changes.
  Today: night-heartbeat and night-stall-guard exclude jobs without a session; AGENTS.md has a background-mode rule.
  Repository change: AGENTS.md (proposed text for the maintainer if held), the ADR.
  Architecture change: as Q-5.

In the context of earlier night-run rules, facing silent drift, we decided to supersede them explicitly in the new ADR and keep the wake until advance lands, to achieve consistent rules, accepting an interim with both. — 2026-11-24

## Q-7 · Kit, permissions and bookkeeping

asked: 2026-11-24
answer: "A — the launcher travels with the kit as a mechanism; permissions follow the central policy of bead coding-harness-a6ns.2; a CI caller is declared; older launch changes (hermes-runner, stage2-session) are neighbours, not blockers; tmux is checked as a prerequisite and its absence is refused with a clear message; the neighbours verify-machine-lock and night-heartbeat are kept (the first as the admission it reuses, the second as the rule the ADR supersedes); the research disagreements H-80..H-90 are settled by these answers."
answered_by: maintainer
status: answered
research_items:
  - 28bf813a6f483b16b5453a54f8fbe327/H-11
  - 28bf813a6f483b16b5453a54f8fbe327/H-16
  - 28bf813a6f483b16b5453a54f8fbe327/H-30
  - 28bf813a6f483b16b5453a54f8fbe327/H-33
  - 28bf813a6f483b16b5453a54f8fbe327/H-37
  - 28bf813a6f483b16b5453a54f8fbe327/H-50
  - 28bf813a6f483b16b5453a54f8fbe327/H-51
  - 28bf813a6f483b16b5453a54f8fbe327/H-52
  - 28bf813a6f483b16b5453a54f8fbe327/H-53
  - 28bf813a6f483b16b5453a54f8fbe327/H-58
  - 28bf813a6f483b16b5453a54f8fbe327/H-61
  - 28bf813a6f483b16b5453a54f8fbe327/H-62
  - 28bf813a6f483b16b5453a54f8fbe327/H-63
  - 28bf813a6f483b16b5453a54f8fbe327/H-64
  - 28bf813a6f483b16b5453a54f8fbe327/H-65
  - 28bf813a6f483b16b5453a54f8fbe327/H-66
  - 28bf813a6f483b16b5453a54f8fbe327/H-67
  - 28bf813a6f483b16b5453a54f8fbe327/H-68
  - 28bf813a6f483b16b5453a54f8fbe327/H-69
  - 28bf813a6f483b16b5453a54f8fbe327/H-70
  - 28bf813a6f483b16b5453a54f8fbe327/H-71
  - 28bf813a6f483b16b5453a54f8fbe327/H-72
  - 28bf813a6f483b16b5453a54f8fbe327/H-73
  - 28bf813a6f483b16b5453a54f8fbe327/H-74
  - 28bf813a6f483b16b5453a54f8fbe327/H-75
  - 28bf813a6f483b16b5453a54f8fbe327/H-76
  - 28bf813a6f483b16b5453a54f8fbe327/H-77
  - 28bf813a6f483b16b5453a54f8fbe327/H-78
  - 28bf813a6f483b16b5453a54f8fbe327/H-79
  - 28bf813a6f483b16b5453a54f8fbe327/H-80
  - 28bf813a6f483b16b5453a54f8fbe327/H-81
  - 28bf813a6f483b16b5453a54f8fbe327/H-82
  - 28bf813a6f483b16b5453a54f8fbe327/H-83
  - 28bf813a6f483b16b5453a54f8fbe327/H-84
  - 28bf813a6f483b16b5453a54f8fbe327/H-85
  - 28bf813a6f483b16b5453a54f8fbe327/H-86
  - 28bf813a6f483b16b5453a54f8fbe327/H-87
  - 28bf813a6f483b16b5453a54f8fbe327/H-88
  - 28bf813a6f483b16b5453a54f8fbe327/H-89
  - 28bf813a6f483b16b5453a54f8fbe327/H-90
  - 28bf813a6f483b16b5453a54f8fbe327/H-91
  - 28bf813a6f483b16b5453a54f8fbe327/H-92
research_neighbours: {keep: [plans/changes/archive/2026-11-06-verify-machine-lock/spec.md, plans/changes/archive/2026-11-16-night-heartbeat/spec.md], drop: [], add: []}
context: |
  Topic: the remaining handoff items of run 28bf813a.
  Intention: close the bookkeeping in one answer.
  Today: one complete research run with 92 items.
  Repository change: kit manifest entry; CI caller declaration.
  Architecture change: none beyond Q-5.

In the context of the research bookkeeping, facing ninety-two handoff items, we decided on the kit, permission and neighbour answers above, to achieve a focused spec, accepting tmux as a kit prerequisite. — 2026-11-24
