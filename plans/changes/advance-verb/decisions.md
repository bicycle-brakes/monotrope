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
