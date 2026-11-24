---
title: "Decisions — advance-verb"
category: decisions
status: draft
implementation_status: none
date: 2026-11-24
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-z40g
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, lanes, advance]
---

# advance-verb — Decisions

Class: architectural (bead coding-harness-z40g; it changes who starts runner verbs and amends ADR 0021). The interview ran in the conversation of session c820a13d on 2026-11-24; the answers are recorded below with the options as they were put. Basis: research run bf9a45e8.

## Q-1 · Start the next step, or only name it

asked: 2026-11-24
answer: "A — `advance` starts the named next step itself. ADR 0021's consumed-ladder amendment (\"does not start either verb itself\") is amended in a decision PR the maintainer merges."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-7
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-18
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-22
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-28
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-32
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-34
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-36
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-42
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-47
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-69
context: |
  Topic: whether the new command starts the next step of a lane or only names it.
  Intention: no idle lanes at night (bead coding-harness-z40g); on 2026-11-24 no runner job ran from 03:20 to 08:00 although lanes were waiting.
  Today: ADR 0021's consumed-ladder amendment has the runner name `next: repair|review <change>` and start neither.
  Repository change: Options: A start the next step (needs an ADR 0021 amendment); B only name it, ADR 0021 unchanged.
  Architecture change: who starts runner verbs.

In the context of lanes that wait for a hand start, facing a runner that only names the next step, we decided that `advance` starts it, to achieve lanes that keep moving without the orchestrator, accepting an amendment to ADR 0021. — 2026-11-24

## Q-2 · Which command hosts it

asked: 2026-11-24
answer: "Own command, for modularity, not a runner verb: `scripts/lanes.py` with the subcommand `advance` (name chosen in a follow-up question; options were `scripts/lanes.py advance`, `scripts/advance.py`, `scripts/lane_driver.py`). It starts model steps only through `scripts/stage2.py`; it is not added to `stage2.VERBS`, the dispatcher's `known` list or `ORIGIN_VERBS`, and pushing stays with the runner verbs it starts. The lanes-file parser lives in the same module."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-1
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-2
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-3
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-6
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-16
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-17
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-19
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-20
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-21
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-29
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-33
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-37
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-41
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-50
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-54
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-64
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-66
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-67
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-70
context: |
  Topic: where the advance command lives.
  Intention: keep the runner from growing further and keep lane driving a separate module.
  Today: two CLI entry points exist, `scripts/stage2.py` (verb registry, locks, loop record) and `scripts/harness.py` (decide adr, time-log); lanes.txt has no parser.
  Repository change: Options put: A `scripts/stage2.py` VERBS; B `scripts/harness.py`. The maintainer answered with an own command for modularity and asked for a name; name options: `scripts/lanes.py advance`, `scripts/advance.py`, `scripts/lane_driver.py`.
  Architecture change: a new module beside the runner that calls it.

In the context of a runner that already owns many verbs, facing a choice between adding one more verb and a separate command, we decided on an own command `scripts/lanes.py advance` that calls `scripts/stage2.py`, to achieve a modular lane driver, accepting one more entry point. — 2026-11-24

## Q-3 · Relation to ladder-next-step (bead coding-harness-hwll)

asked: 2026-11-24
answer: "A — hwll lands first and produces the `next:` line; `advance` consumes that line and does not decide the next step itself."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-39
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-44
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-46
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-53
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-58
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-59
context: |
  Topic: who decides the next step.
  Intention: one place decides, one place executes.
  Today: bead coding-harness-hwll (ladder-next-step) is to print `next: <verb> <change>` after each runner step; it has no spec yet.
  Repository change: Options: A hwll first, advance reads its line; B advance derives the next step itself.
  Architecture change: none beyond Q-1.

In the context of deciding a lane's next step, facing the same logic in two places, we decided that hwll lands first and advance only consumes its `next:` line, to achieve one decider, accepting that z40g waits for hwll. — 2026-11-24

## Q-4 · Class and decision instrument

asked: 2026-11-24
answer: "A — architectural; one amendment to ADR 0021, no new ADR; no new workflow phase, `advance` is a tool, not a phase."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-23
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-24
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-25
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-26
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-27
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-30
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-31
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-35
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-40
context: |
  Topic: class and ADR of this change.
  Intention: the change alters who starts runner verbs.
  Today: ADR 0021 governs the review ladder and its hand-back.
  Repository change: Options: A architectural with an ADR 0021 amendment; B architectural with a new ADR; C feature without ADR.
  Architecture change: ADR 0021 amended.

In the context of a change to who starts runner verbs, facing a new ADR or an amendment, we decided on an ADR 0021 amendment under class architectural, to achieve the record where the rule lives, accepting a longer ADR. — 2026-11-24

## Q-5 · Lifecycle fields

asked: 2026-11-24
answer: "A — `advance` writes no lifecycle field (status, implementation_status); the one writer of derived fields stays with bead coding-harness-7ftj. The pros and cons were put to the maintainer before the answer: one writer, no conflicting commits, no stale `updated:` risk, simple tests; against: status lags until the runner or 7ftj sets it, and \"parked\" is recorded only in the lane log."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-5
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-38
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-68
context: |
  Topic: whether advance edits document headers.
  Intention: keep a single writer of derived fields.
  Today: `archive_closed_changes`, `check_frontmatter_current --stamp` and the runner's restoration each touch header fields; bead coding-harness-7ftj makes one writer.
  Repository change: Options: A write nothing; B set status.
  Architecture change: none.

In the context of document lifecycle fields, facing a second writer, we decided that advance writes none, to achieve one writer, accepting a status that lags. — 2026-11-24

## Q-6 · What it reads and trusts

asked: 2026-11-24
answer: "B — local state plus an optional target argument: `lanes.py advance` reads the loop record's `next:` line and a small lanes file whose format `scripts/lanes.py` defines; `lanes.py advance <change>` advances that one lane. No external input (webhooks, GitHub labels, comments, branch names) ever triggers a step."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-8
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-10
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-12
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-15
context: |
  Topic: the inputs advance may act on.
  Intention: no untrusted-input entry point; still allow a targeted push of one lane.
  Today: lanes.txt (night run) is free text without a parser.
  Repository change: Options: A local state only, no target argument; B local state plus target argument; C also GitHub state.
  Architecture change: none.

In the context of what may trigger a runner step, facing external state as an attack surface, we decided on local state plus an optional change argument, to achieve targeted use without an external trigger, accepting a lanes-file format to define. — 2026-11-24

## Q-7 · How much one call does

asked: 2026-11-24
answer: "Central limit, default 2: one `advance` call runs at most N verify-bearing steps (for example repair then review); N is a central setting like the review rounds and reviewer count, default 2. A call stops at an open hand step (a repair that exits 0 with held rows is not done) or at a failed step and names the reason. Options put first: A one step and stop at a hand step; B several steps in a row; the maintainer asked for B in a milder form, and the follow-up options were: central limit default 2; one expensive step plus the cheap model-free ones; a time budget per call."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-48
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-49
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-52
context: |
  Topic: the size of one advance call.
  Intention: move lanes further per call without long unwatched chains.
  Today: each runner verb runs one step with a full make verify.
  Repository change: a central setting for N, default 2.
  Architecture change: none beyond Q-1.

In the context of chaining steps, facing a single step or an unbounded chain, we decided on a central limit of two verify-bearing steps per call, to achieve progress per call that stays easy to watch and to change, accepting up to two full verifies per call. — 2026-11-24

## Q-8 · Research basis and bookkeeping

asked: 2026-11-24
answer: "A — run bf9a45e8 is the basis; the earlier incomplete runs are superseded; neighbours trimmed to adr-0021-consumed-ladder and harness-decide-adr (ladder-next-step has no spec yet and is named in prose); tests in a new tests/test_lanes.py; the \"Thirteen verbs\" prose and the tests that pin it stay untouched, because advance is not a runner verb (Q-2). The disagreements H-80..H-88 are settled by these answers."
answered_by: maintainer
status: answered
research_items:
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-4
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-9
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-11
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-13
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-14
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-43
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-45
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-51
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-55
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-56
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-57
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-60
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-61
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-62
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-63
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-65
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-71
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-72
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-73
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-74
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-75
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-76
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-77
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-78
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-79
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-80
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-81
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-82
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-83
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-84
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-85
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-86
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-87
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-88
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-89
  - bf9a45e85a44e4a95f12a03ccafaf5a1/H-90
research_neighbours: {keep: [plans/changes/adr-0021-consumed-ladder/spec.md, plans/changes/harness-decide-adr/spec.md], drop: [plans/changes/finder-partial-report/spec.md, plans/changes/verify-two-slots/spec.md, plans/changes/repair-hand-held-rows/spec.md], add: []}
context: |
  Topic: the remaining handoff items of run bf9a45e8.
  Intention: close the bookkeeping in one answer.
  Today: three research runs, one complete (bf9a45e8); five candidate neighbours; neighbour splits for finder-partial-report and verify-two-slots.
  Repository change: spec neighbours: two paths; new test file tests/test_lanes.py.
  Architecture change: none.

In the context of the research bookkeeping, facing ninety handoff items, we decided on run bf9a45e8 and two neighbours, to achieve a focused spec, accepting that the dropped neighbours are not re-read. — 2026-11-24

## Q-9 · Several lanes in one call (spec review S-1, S-2, S-15)

asked: 2026-11-24
answer: "A — the limit applies per lane: each lane gets at most the configured number of verify-bearing steps in one call; a failure or an open hand step stops only that lane and the driver goes on with the next listed lane; lanes run one after another. Parallel lanes come later through scripts/jobs.py (bead coding-harness-a6ns.1), one job per lane. Options put: per lane, only the lane stops, sequential (recommended); per call, the first failure stops everything; per lane, in parallel."
answered_by: maintainer
status: answered
context: |
  Topic: one advance call over several lanes.
  Intention: settle spec-review rows S-1, S-2 and S-15 of 2026-11-24.
  Today: Q-7 set a limit of two verify-bearing steps without saying per what.
  Repository change: the driver loop in scripts/lanes.py.
  Architecture change: none.

In the context of a call over several lanes, facing a shared or a per-lane limit, we decided on a per-lane limit, lane-local stops and sequential lanes, to achieve progress on every lane per call, accepting that later lanes wait for earlier ones until jobs.py runs them in parallel. — 2026-11-24

## Q-10 · How a step starts, which verbs, which count (spec review S-3, S-5, S-10)

asked: 2026-11-24
answer: "A — each step is a child process `scripts/stage2.py <verb> <change>`, so each step has its own verify admission. The verbs advance may start and the verbs that count as verify-bearing are lists in the central setting; initial values: allowed repair, review, review-loop, release-loop, prepare-loop, implement; counted implement, repair, review. The per-lane limit is a key with range 1–5, initial 2; an invalid value refuses the call. Options put: child process with central lists (recommended); child process, only repair and review; import in the same process."
answered_by: maintainer
status: answered
context: |
  Topic: starting a step.
  Intention: settle spec-review rows S-3, S-5 and S-10 of 2026-11-24.
  Today: verify-two-slots admits one verify per process.
  Repository change: three keys in the central setting; child-process starts in scripts/lanes.py.
  Architecture change: none beyond Q-1.

In the context of starting runner steps, facing an in-process call or child processes, we decided on a child process per step with central allow and count lists, to achieve independent admissions and easy changes, accepting one process start per step. — 2026-11-24

## Q-11 · Where the inputs come from (spec review S-4, S-6, S-7, S-13)

asked: 2026-11-24
answer: "A — bead coding-harness-hwll also writes the `next:` line into the loop record; the latest line governs and an unreadable line stops the lane; hwll defines the line's grammar. scripts/lanes.py owns a new lanes file in the runner state directory, `$XDG_STATE_HOME/coding-harness/lanes.yaml`, with change and worktree path per lane; it replaces the night run's free-text lanes file. Options put: next: in the record plus a new lanes file (recommended); next: read from the step's output."
answered_by: maintainer
status: answered
context: |
  Topic: the driver's inputs.
  Intention: settle spec-review rows S-4, S-6, S-7 and S-13 of 2026-11-24.
  Today: ADR 0021 prints `next:` to standard output only; the night lanes file is free text; the loop record key is `<change>@<digest of the repository root>`.
  Repository change: hwll writes the line into loop.md; scripts/lanes.py defines lanes.yaml.
  Architecture change: none.

In the context of the driver's inputs, facing output parsing or recorded state, we decided on the recorded `next:` line and an own lanes file with worktree paths, to achieve inputs that survive a restart, accepting that hwll also writes the record. — 2026-11-24

## Q-12 · Stops, park marks and exit codes (spec review S-8, S-9, S-11, S-12, S-14)

asked: 2026-11-24
answer: "A — the runner writes `next: hand <change> <rows>` for an open hand step (hwll) and advance stops there. A stopped lane gets a park mark with its reason in lanes.yaml and runs again only after the orchestrator clears it. Exit 0: every lane advanced or had nothing to do; 1: at least one lane stopped; 2: the call was refused; reasons on standard error and in the job record. 'Writes no lifecycle field' (Q-5) binds advance's own code, not the runner steps it starts. Criterion 8 becomes testable: lanes or steps taken from remote data (labels, comments, fetched files) are ignored. Options put: next: hand plus park mark (recommended); no park mark."
answered_by: maintainer
status: answered
context: |
  Topic: recognising and remembering a stop.
  Intention: settle spec-review rows S-8, S-9, S-11, S-12 and S-14 of 2026-11-24.
  Today: a repair with only held rows exits 0; after a failure the same `next:` line remains.
  Repository change: hwll's `next: hand` form; park marks in lanes.yaml; the exit contract of scripts/lanes.py.
  Architecture change: none.

In the context of failed or held steps, facing silent retries, we decided on a `next: hand` line and a park mark the orchestrator clears, to achieve no repeated failing step, accepting one more hand action per stopped lane. — 2026-11-24

## Q-13 · Empty, used and parked instructions (spec review S-16, S-18, S-24)

asked: 2026-11-24
answer: "A — no loop record or no `next:` line means nothing to do: exit 0, no park mark. An instruction the driver started in this call counts as used; if the latest line is still that instruction after the step, the lane ends for this call. A parked lane is skipped and counts as nothing to do; its reason is written to standard error again. Options put: nothing to do (recommended); count each case as a stop with exit 1 and a park mark."
answered_by: maintainer
status: answered
context: |
  Topic: lanes without a fresh instruction.
  Intention: settle spec-review rows S-16, S-18 and S-24 of 2026-11-24.
  Today: release-loop deletes the loop record; a new lane has none; a step may leave the same `next:` line.
  Repository change: the lane loop in scripts/lanes.py.
  Architecture change: none.

In the context of lanes with no new instruction, facing parked-by-default lanes or endless repeats, we decided that a missing, used or parked instruction means nothing to do, to achieve a bounded call without false stops, accepting that a stalled lane shows only on standard error.  — 2026-11-24

## Q-14 · Failures, the limit and concurrent calls (spec review S-17, S-19, S-22)

asked: 2026-11-24
answer: "A — runner exit 1 is a failure and parks the lane. Exit 2 (a refusal, such as a held record lock) ends the lane for this call without a park mark. A lane at its limit starts no further step of any kind in this call and counts as advanced (exit 0, no mark). The driver holds a lock per lane while it works on it and writes lanes.yaml under a file lock. Options put: lock per lane (recommended); one lock for the whole call, a second call refused with exit 2."
answered_by: maintainer
status: answered
context: |
  Topic: failed and refused steps, the limit, and parallel calls.
  Intention: settle spec-review rows S-17, S-19 and S-22 of 2026-11-24.
  Today: the runner exits 1 on failure and 2 on refusal; Q-9 plans one job per lane through scripts/jobs.py.
  Repository change: per-lane lock and locked writes in scripts/lanes.py.
  Architecture change: none.

In the context of failed steps and overlapping calls, facing lost park marks or parked running lanes, we decided on park-on-failure, no park on refusal, a full stop at the limit and a lock per lane, to achieve safe parallel calls later, accepting one lock file per lane.  — 2026-11-24

## Q-15 · Validating the inputs (spec review S-21, S-26, S-27, S-28)

asked: 2026-11-24
answer: "A — a worktree entry is valid only when the path exists and is a worktree of this repository; an invalid entry parks only its lane. An invalid central allow or counted list refuses the whole call with exit 2, like an invalid limit. The ADR 0021 amendment names the six initial verbs; adding a verb needs a further amendment. Each step runs the lane worktree's own scripts/stage2.py. Options put: strict and lane-local (recommended); form check only, bad list entries ignored, the ADR allows whatever the list holds."
answered_by: maintainer
status: answered
context: |
  Topic: checking lanes.yaml and the central setting.
  Intention: settle spec-review rows S-21, S-26, S-27 and S-28 of 2026-11-24.
  Today: stage2.py takes its repository root from its own file path.
  Repository change: validation in scripts/lanes.py; the ADR 0021 amendment text.
  Architecture change: the ADR 0021 amendment lists its verbs.

In the context of the driver's inputs, facing silent widening by a setting typo, we decided on strict, lane-local checks and an ADR that names its verbs, to achieve no new step without a decision, accepting an ADR amendment per new verb.  — 2026-11-24

## Q-16 · Scope: job record and the night routine (spec review S-20, S-23)

asked: 2026-11-24
answer: "A — the job record is dropped from this change; reasons go to standard error only, and scripts/jobs.py (bead coding-harness-a6ns.1) adds its record when it lands. This change also rewrites the night routine in docs/WORKFLOW.md to call `scripts/lanes.py advance` with one lanes.yaml per machine, shared by concurrent runs under the Q-14 locks. Options put: WORKFLOW in, job record out (recommended); both out with a follow-up bead."
answered_by: maintainer
status: answered
context: |
  Topic: what this change covers.
  Intention: settle spec-review rows S-20 and S-23 of 2026-11-24.
  Today: no job record exists; docs/WORKFLOW.md still prescribes night/<run-id>/lanes.txt.
  Repository change: docs/WORKFLOW.md night routine.
  Architecture change: none.

In the context of the change's scope, facing a reference to an unbuilt record and a stale routine, we decided to drop the job record and rewrite the night routine here, to achieve documentation that matches Q-11, accepting a larger documentation diff.  — 2026-11-24

## Q-17 · Ambiguity S-29

asked: 2026-11-24
answer: "B — the driver tries a lane's lock without blocking; a lane another advance call holds is skipped as nothing to do for this call (exit 0 for that lane), with the reason on standard error. Options put: skip without blocking (recommended); block until free; refuse the call with exit 2."
answered_by: maintainer
status: answered
context: |
  Topic: a lane lock held by another call.
  Intention: settle spec-review round three (2026-11-24, fallback reviewer deepseek-v4.1-flash) before the final draft.
  Today: criterion 25 demands a per-lane lock but no contention rule.
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of a lane lock held by another call, facing readings with different exit codes or tests, we decided as answered above, to achieve one testable reading, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-18 · Ambiguity S-30

asked: 2026-11-24
answer: "B — a lane that neither advanced nor had nothing to do is a stop and sets exit 1: a runner step that exits 2 stops its lane for this call without a park mark; an invalid worktree path stops its lane with a park mark. Options put: both count as stops, exit 1 (recommended); refusal exit 0, invalid worktree exit 0 as parked."
answered_by: maintainer
status: answered
context: |
  Topic: exit codes for a refused step and an invalid worktree.
  Intention: settle spec-review round three (2026-11-24, fallback reviewer deepseek-v4.1-flash) before the final draft.
  Today: criterion 17 knows advanced, nothing to do and stopped only.
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of exit codes for a refused step and an invalid worktree, facing readings with different exit codes or tests, we decided as answered above, to achieve one testable reading, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-19 · Criterion 19 (spec review S-31)

asked: 2026-11-24
answer: "Criterion 19 becomes a statement of scope in the Non-goals: the driver reads only lanes.yaml and the loop record. The test tests/test_lanes.py::test_remote_ignored leaves the ledger. Options put: statement of scope (recommended); keep it as a criterion."
answered_by: maintainer
status: answered
context: |
  Topic: the untestable remote-data criterion.
  Intention: settle spec-review round three (2026-11-24, fallback reviewer deepseek-v4.1-flash) before the final draft.
  Today: criterion 19 has no input that can refute it.
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of the untestable remote-data criterion, facing readings with different exit codes or tests, we decided as answered above, to achieve one testable reading, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-20 · Instruction and lanes file as JSON (amends Q-11, Q-13)

asked: 2026-11-24
answer: "B — the driver reads the next-step instruction only from `next.json` beside the loop record (bead coding-harness-hwll, its decision Q-6), never from loop.md; a missing file means nothing to do, an unreadable or schema-invalid file stops the lane. An instruction counts as used when the file's content (including its written time) is unchanged after the step the driver started from it. The lanes file is JSON, `$XDG_STATE_HOME/coding-harness/lanes.json`, schema-validated, written atomically under the Q-14 lock, park marks included; it replaces lanes.yaml. Maintainer rule of 2026-11-24: code before prose; Markdown only where it cannot be avoided. Options put: keep loop.md behind one reader function (recommended at the time); JSON now (chosen); wait for bead coding-harness-5ane.11."
answered_by: maintainer
status: answered
context: |
  Topic: the driver's state files.
  Intention: replace the Markdown and YAML state of Q-11 with schema-validated JSON.
  Today: Q-11 reads the latest `next:` line from loop.md and keeps lanes.yaml.
  Repository change: scripts/lanes.py reads next.json and owns lanes.json with a schema.
  Architecture change: none beyond Q-1.

In the context of the driver's inputs, facing control state parsed from Markdown, we decided on JSON instruction and lanes files, to achieve inputs code reads without patterns, accepting a fourth spec review — 2026-11-24

## Q-21 · Fourth spec-review round

asked: 2026-11-24
answer: "authorized — the maintainer answered yes on 2026-11-24: one fourth spec-review round (Opus, phase 2a) of the final draft a6479b39, because Q-20 changes the spec after the third round. Options put: a fourth review for both lanes (recommended); re-slice the JSON instruction into its own change."
answered_by: maintainer
status: answered
context: |
  Topic: whether the changed spec is reviewed again.
  Intention: the runner admits a spec change after round three only with this authorization.
  Today: AGENTS.md phase 2a ends spec review after round three.
  Repository change: none.
  Architecture change: none.

In the context of a spec changed after its third review, facing an unreviewed contract, we decided on one fourth spec review, to achieve a checked spec before phase 4, accepting one more Opus run — 2026-11-24

## Q-22 · Writers of lanes.json and a cap on all steps (spec review S-32, S-33)

asked: 2026-11-24
answer: "S-32: scripts/lanes.py gets the subcommands `add`, `remove`, `clear` and `hold`; each writes lanes.json under the same lock as `advance`; lanes.json is never edited by hand (house rule 11); the night routine adds a lane when its work starts and removes the entry before its worktree is removed. S-33: besides the verify-bearing limit, every lane runs at most a configured number of steps of any kind per call, a key in the central setting, initial value 6, range 1-20; reaching it ends the lane for the call like the verify-bearing limit. Options put: the orchestrator's recommendations (confirmed)."
answered_by: maintainer
status: answered
context: |
  Topic: who writes lanes.json and what bounds a call.
  Intention: settle spec-review round four (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: the reviewed spec leaves this open (findings.md, round four).
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of who writes lanes.json and what bounds a call, facing readings that build or test differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-23 · Ambiguity S-34

asked: 2026-11-24
answer: "A — the step that reaches a limit ends the lane before the driver reads the next.json it leaves; the lane counts as advanced, without a park mark; the next call reads the new file. Options put: end before reading (recommended); judge the new file first."
answered_by: maintainer
status: answered
context: |
  Topic: the step at the limit.
  Intention: settle spec-review round four (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: the reviewed spec leaves this open (findings.md, round four).
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of the step at the limit, facing readings that build or test differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-24 · Ambiguity S-35

asked: 2026-11-24
answer: "B — a missing lanes.json lists no lanes: the call has nothing to do and exits 0; an existing but unreadable or schema-invalid file still refuses with exit 2. Options put: missing means no lanes (recommended); missing refuses the call."
answered_by: maintainer
status: answered
context: |
  Topic: a missing lanes file.
  Intention: settle spec-review round four (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: the reviewed spec leaves this open (findings.md, round four).
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of a missing lanes file, facing readings that build or test differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24

## Q-25 · Mark reading and signal deaths (spec review S-36, S-37)

asked: 2026-11-24
answer: "S-36: a call reads a lane's entry and park mark again under that lane's lock when its turn comes, not only at call start. S-37: a step that ends by a signal (128+N) or without an exit code counts as a failed step and parks its lane. Options put: the orchestrator's recommendations (confirmed)."
answered_by: maintainer
status: answered
context: |
  Topic: when marks are read and how a killed step counts.
  Intention: settle spec-review round four (Opus, 2026-11-24) before the final draft; no further review round can run.
  Today: the reviewed spec leaves this open (findings.md, round four).
  Repository change: the spec text of the final draft.
  Architecture change: none.

In the context of when marks are read and how a killed step counts, facing readings that build or test differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that the final draft is not reviewed again. — 2026-11-24
