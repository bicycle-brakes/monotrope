---
title: "Decisions — detached-job-launcher"
category: decisions
status: draft
implementation_status: none
date: 2026-11-24
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-25
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

## Q-8 · What jobs.py starts and how it uses tmux (spec review S-1, S-2, S-3, S-6)

asked: 2026-11-24
answer: "A — `jobs.py start` runs any command (harness-independent, Q-1); the job record notes whether it is a runner verb. Jobs run in an own tmux server `coding-harness` (`tmux -L coding-harness`), started detached when absent, so a launch works without an open tmux and survives the end of the caller's process tree and of the caller's own tmux sessions. The launch is refused only when the tmux binary is missing. jobs.py passes the caller's working directory, PATH, virtual environment, XDG_STATE_HOME and HARNESS_VERIFY_* values explicitly. Options put: any command on an own tmux server (recommended); runner commands only."
answered_by: maintainer
status: answered
context: |
  Topic: the command and the tmux use of a job.
  Intention: settle spec-review rows S-1, S-2, S-3 and S-6 of 2026-11-24.
  Today: a tmux window inherits the tmux server's environment and start directory.
  Repository change: scripts/jobs.py start.
  Architecture change: an own tmux server for jobs.

In the context of the spec-review rows of 2026-11-24, we decided as answered above, to achieve a spec without open readings, accepting the consequences named in the options — 2026-11-24

## Q-9 · Records, verify slot and display (spec review S-4, S-5, S-9, S-12)

asked: 2026-11-24
answer: "A — job records live in `$XDG_STATE_HOME/coding-harness/jobs/`, one per job; jobs.py does not import scripts/stage2.py. A job never inherits a held verify admission; it acquires its own. run_report reads the job records and deduplicates against its process recognition by process id. Finished records are kept 14 days; `jobs.py list` shows running jobs and those of the last 24 hours, `--all` shows all. Options put: own folder, own slot, 14 days (recommended); beside the loop records under coding-harness/stage2/. Refines Q-4."
answered_by: maintainer
status: answered
context: |
  Topic: the job records.
  Intention: settle spec-review rows S-4, S-5, S-9 and S-12 of 2026-11-24.
  Today: Q-4 said both 'beside the loop records' and '$XDG_STATE_HOME/coding-harness/'.
  Repository change: record folder, retention, run_report reading.
  Architecture change: none.

In the context of the spec-review rows of 2026-11-24, we decided as answered above, to achieve a spec without open readings, accepting the consequences named in the options — 2026-11-24

## Q-10 · Stopping a job and its end record (spec review S-7, S-8)

asked: 2026-11-24
answer: "A — `jobs.py stop` ends the job's whole process tree, including children in their own sessions (through recorded process groups), and so frees its verify slot. A small wrapper in the window writes the end record: the exit code, or 'signal N' for a signal death. If the wrapper dies as well (tmux killed, reboot), `jobs.py list` marks the job 'lost' once its process id is gone without an end record. Options put: whole tree, wrapper, 'lost' (recommended); close the window only."
answered_by: maintainer
status: answered
context: |
  Topic: stop and end of a job.
  Intention: settle spec-review rows S-7 and S-8 of 2026-11-24.
  Today: stage2's timed launches use start_new_session; closing a window leaves such children running.
  Repository change: jobs.py stop and the wrapper.
  Architecture change: none.

In the context of the spec-review rows of 2026-11-24, we decided as answered above, to achieve a spec without open readings, accepting the consequences named in the options — 2026-11-24

## Q-11 · The rules the ADR changes, and when jobs.py is required (spec review S-10, S-11)

asked: 2026-11-24
answer: "A — the ADR quotes the exact non-goal sentences of night-heartbeat and night-stall-guard and exempts only detached runner jobs from them; a scheduler, a daemon and automatic restarts stay excluded. jobs.py is the required route for every runner verb that runs a full make verify; the harnesses' background mode stays allowed for short commands. Options put: quote the sentences, required for verify-bearing jobs (recommended); quote the sentences, jobs.py only offered. Refines Q-6."
answered_by: maintainer
status: answered
context: |
  Topic: the doctrine change.
  Intention: settle spec-review rows S-10 and S-11 of 2026-11-24.
  Today: night-heartbeat excludes 'a new scheduler, daemon, … automatic restart'; night-stall-guard excludes 'a scheduler, daemon, headless heartbeat architecture, automatic restart'.
  Repository change: the ADR text; the AGENTS.md background-mode bullet.
  Architecture change: as Q-5.

In the context of the spec-review rows of 2026-11-24, we decided as answered above, to achieve a spec without open readings, accepting the consequences named in the options — 2026-11-24

## Q-12 · Runner verbs and verify jobs (spec review S-13)

asked: 2026-11-24
answer: "A — a runner verb is a command whose argv invokes `scripts/stage2.py` with a known verb, as run_report.py recognises it. AC 9 becomes a statement of scope, not a criterion. AC 15 covers stage2 verbs that run a full `make verify` and a bare `make verify` alike. Options put: stage2.py with a known verb (recommended); jobs.py start itself as the runner verb."
answered_by: maintainer
status: answered
context: |
  Topic: what a runner verb is.
  Intention: settle spec-review rows S-13 of 2026-11-24 (fallback reviewer deepseek-v4.1-flash).
  Today: the term is undefined; four criteria depend on it.
  Repository change: the job record's kind field and AC 15's check.
  Architecture change: none.

In the context of what a runner verb is, facing two readings with different builds, we decided as answered above, to achieve one testable reading for the redraft, accepting the limits named in the answer. — 2026-11-24

## Q-13 · Stop, wrapper and process IDs (spec review S-14, S-15)

asked: 2026-11-24
answer: "B — stop ends the started command's process tree, descendants in separate sessions included; the wrapper is spared, writes `signal 15` as the end record and then exits. The record holds two named fields: the started command's PID (for de-duplication against process recognition) and the wrapper's PID (for the liveness test), plus the recorded process group. Options put: spare the wrapper, two PID fields (recommended); end the wrapper too."
answered_by: maintainer
status: answered
context: |
  Topic: stopping a job and naming its processes.
  Intention: settle spec-review rows S-14, S-15 of 2026-11-24 (fallback reviewer deepseek-v4.1-flash).
  Today: AC 3 and AC 5 conflict for a stopped job; AC 4 names one unspecified PID.
  Repository change: jobs.py stop and the record format.
  Architecture change: none.

In the context of stopping a job and naming its processes, facing two readings with different builds, we decided as answered above, to achieve one testable reading for the redraft, accepting the limits named in the answer. — 2026-11-24

## Q-14 · Lost jobs and the inherited environment (spec review S-16, S-17)

asked: 2026-11-24
answer: "A — lost is a state of its own: plain `jobs.py list` shows a lost job until its record is pruned, 14 days after its start. The job receives `VIRTUAL_ENV` and the caller's PATH prefix; all four `HARNESS_VERIFY` admission values (LOCK_HELD, LOCK_TOKEN, ADMISSION_ID, ADMISSION_WAIT) are dropped. Options put: lost shown until pruned, all admission values dropped (recommended); lost hidden after 24 hours, lock pair only dropped."
answered_by: maintainer
status: answered
context: |
  Topic: lost jobs and the job's environment.
  Intention: settle spec-review rows S-16, S-17 of 2026-11-24 (fallback reviewer deepseek-v4.1-flash).
  Today: AC 6 and AC 17 disagree on a lost job; AC 16 names no variables.
  Repository change: jobs.py list and the environment the wrapper passes on.
  Architecture change: none.

In the context of lost jobs and the job's environment, facing two readings with different builds, we decided as answered above, to achieve one testable reading for the redraft, accepting the limits named in the answer. — 2026-11-24

## Q-15 · Ambiguity S-18

asked: 2026-11-24
answer: "B — `jobs.py stop` first writes a stop request into the job's JSON record; when the wrapper sees it, it records `signal 15` as the end, whatever exit status the command returned (a runner verb traps SIGTERM and exits 143). Options put: stop marker in the record (recommended); record the raw exit status."
answered_by: maintainer
status: answered
context: |
  Topic: the end record of a stopped job.
  Intention: settle spec-review round three (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: stage2.py, verify_run.py and verify_lock.py trap SIGTERM and exit 128+N.
  Repository change: the stop marker in the job record; the wrapper's end rule.
  Architecture change: none beyond the ADR of Q-11.

In the context of the end record of a stopped job, facing readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-16 · Ambiguity S-19

asked: 2026-11-24
answer: "B, narrowed — the ADR exempts exactly the two declared job kinds, runner verbs (`scripts/stage2.py` with a verb) and `make verify`; every other detached command stays under the quoted non-goals. Options put: the two declared kinds (recommended); every job jobs.py starts."
answered_by: maintainer
status: answered
context: |
  Topic: the reach of the ADR exemption.
  Intention: settle spec-review round three (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: AC 13 exempts 'detached runner jobs' without defining them.
  Repository change: the ADR text and the kind field of the record.
  Architecture change: none beyond the ADR of Q-11.

In the context of the reach of the ADR exemption, facing readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-17 · Ambiguity S-20

asked: 2026-11-24
answer: "B — every `scripts/stage2.py` verb, and `make verify`, is started through jobs.py; the harness background mode stays for commands outside the runner only. Options put: all runner verbs through jobs.py (recommended); background mode for everything that needs no full verify."
answered_by: maintainer
status: answered
context: |
  Topic: which commands must use jobs.py.
  Intention: settle spec-review round three (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: AGENTS.md starts long runner jobs in the harness background mode.
  Repository change: the guidance in AGENTS.md and docs/WORKFLOW.md (AC 15).
  Architecture change: none beyond the ADR of Q-11.

In the context of which commands must use jobs.py, facing readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-18 · Records, processes and environment (spec review S-21, S-22, S-23, S-24)

asked: 2026-11-24
answer: "Job records are schema-validated JSON written atomically by code (house rule 11, code before prose). S-21: jobs.py passes the record path to the command in an environment variable; scripts/stage2.py adds every process group it starts in its own session to that record; stop ends all recorded groups plus the process tree. S-22: every recorded PID is stored with its process start time; a PID whose start time differs counts as gone; stop on a finished, lost or mismatched job refuses with exit 2. S-23: a job is a runner verb when its argv runs `scripts/stage2.py` followed by a word that is not an option; jobs.py does not import stage2.py. S-24: the job receives the calling process's whole environment except the four HARNESS_VERIFY admission values, set explicitly per job, never the tmux server's environment. Options put: the orchestrator's recommendations, confirmed by the maintainer with the four critical points (S-21, S-22, S-24, S-25) explained."
answered_by: maintainer
status: answered
context: |
  Topic: job records, process identity and environment.
  Intention: settle spec-review round three (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: the record format is open; groups started inside the command are known only in stage2's memory; a tmux server keeps its first caller's environment.
  Repository change: the JSON record and its schema; stage2.py writes its process groups when a record path is given; jobs.py environment handling.
  Architecture change: none beyond the ADR of Q-11.

In the context of job records, process identity and environment, facing readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-19 · Report, ADR neighbours and lifecycle details (spec review S-25..S-29)

asked: 2026-11-24
answer: "S-25: run_report shows a job that is not a runner verb by its program name only, never its arguments. S-26: the ADR quotes and exempts night-heartbeat's 'runner process supervision' non-goal as well. S-27: start returns only when the record holds both PIDs, waiting at most 10 seconds; otherwise exit 1 and the record state 'failed to start'. S-28: the log holds the command's standard output and standard error and is pruned with its record; the 14 days run from the end, for a lost job from its start. S-29: the machine-facts jobs field reads the job records as well. Options put: the orchestrator's recommendations (confirmed)."
answered_by: maintainer
status: answered
context: |
  Topic: reporting and lifecycle details.
  Intention: settle spec-review round three (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: run_report prints only summary fields; the ADR names one non-goal per neighbour.
  Repository change: run_report.py, machine_facts.py, the ADR text, jobs.py start and prune.
  Architecture change: none beyond the ADR of Q-11.

In the context of reporting and lifecycle details, facing readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24
