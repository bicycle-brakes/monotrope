---
title: "Decisions — sonnet-continues-flash"
category: decisions
status: draft
implementation_status: none
date: 2026-11-02
created: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-6ie
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# sonnet-continues-flash — Decisions

Class: bounded, with an ADR addendum: the answers relax a doctrine sentence
of `docs/WORKFLOW.md` §3 ("a failed model process stops instead of silently
changing route"), so the change owes five counted interview records; five are
recorded below.

The maintainer gave all five answers in the conversation, before this file
existed; the tracker carries them verbatim in the notes of bead
coding-harness-6ie (2026-10-16 about 02:00, shared design with bead
coding-harness-s9r; 2026-10-31 about 13:30 UTC). The orchestrator copied them
here on 2026-11-02 unchanged. The `context` blocks are reconstructed from the
bead's description and notes; the original wording of the questions was not
kept.

## Q-1 · What the next attempt starts from after a failed post-run check

asked: 2026-10-16
context: |
  Topic: the runner's attempt chain (Flash, Flash repair, then Sonnet) in scripts/stage2.py run_attempts (bead coding-harness-6ie, shared design with coding-harness-s9r).
  Intention: Sonnet redoes Flash's work, because the next prompt carries only the failure text, not which files Flash changed.
  Today: the worktree stays as Flash left it; the next prompt does not name the changed files.
  Repository change: the runner and its tests.
  Architecture change: how earlier attempts' edits persist between attempts.
  Question: after an attempt fails its post-run check, what does the next attempt start from?
answer: "Weiterbauen, geschützt" — the next attempt builds on the previous one, protected: it starts from the previous attempt's state as a copy in a fresh environment; its prompt lists the changed files with their diff against the baseline and says continue, do not redo; the runner's inputs (spec, plan, findings and the other files it reads its next prompt from) are restored from git before every attempt, so no attempt can damage them. Rejected: always restart from the baseline (Flash's partial work lost), and continue in the same worktree as today (the s9r damage class stays open).
answered_by: maintainer
status: answered

In the context of a runner whose next attempt redoes the previous attempt's work, facing a choice between a restart from the baseline, the same worktree as today and a protected copy, we decided that the next attempt builds on a copy of the previous state with its diff listed and the runner's inputs restored from git, to achieve that no partial work is lost and no attempt can damage the runner's inputs, accepting one copy per attempt. — 2026-10-16

## Q-2 · What a failed model call does

asked: 2026-10-16
context: |
  Topic: a Flash call that errors or times out (not a red check) in scripts/stage2.py run_attempts (bead coding-harness-6ie).
  Intention: today such an error runs restore_baseline, reverts all of Flash's changes and raises CallFailed, so Sonnet never runs.
  Today: docs/WORKFLOW.md §3 says a failed model process stops instead of silently changing route.
  Repository change: the runner, its tests, and an addendum to the ADR that states the doctrine sentence.
  Architecture change: a failed call becomes a visible route change instead of a stop.
  Question: does a failed model call fall through to the next route, and what happens to the earlier attempts' work?
answer: "Weiter zur nächsten Route" — a failed model call (error or time limit, not a red check) counts as a failed attempt and falls through to the next route, recorded visibly with its reason; nothing an earlier attempt built is reverted. Rejected: stop without reverting. This relaxes the doctrine sentence "a failed model process stops instead of silently changing route" (docs/WORKFLOW.md §3): the change is no longer silent; the amendment goes into the ADR addendum of this change. (Where it is recorded: superseded by Q-5.)
answered_by: maintainer
status: answered

In the context of a failed model call that today reverts all earlier work and stops, facing a choice between stopping without reverting and falling through, we decided that a failed call counts as a failed attempt, falls through to the next route visibly and reverts nothing, to achieve that the later route can still finish the work, accepting an ADR addendum that relaxes the doctrine sentence on silent route changes. — 2026-10-16

## Q-3 · Whether a Flash call abort counts as an attempt

asked: 2026-10-31
context: |
  Topic: the attempt count of the Flash route (two attempts, then Sonnet) when a call aborts (bead coding-harness-6ie).
  Intention: Q-2 lets an aborted call fall through; the count decides whether Flash gets another try first.
  Today: an aborted call raises out of the loop and is not counted.
  Repository change: the runner's attempt loop and its tests.
  Architecture change: none beyond Q-2.
  Question: does a Flash call abort count as one of the route's attempts?
answer: "Zählt als Versuch" — a Flash call abort counts as an attempt.
answered_by: maintainer
status: answered

In the context of the Flash route's attempt count, facing whether a call abort uses up an attempt, we decided that it counts as an attempt, to achieve a bounded number of Flash tries before Sonnet, accepting that an abort caused by the provider costs Flash a try. — 2026-10-31

## Q-4 · What the next attempt gets after an abort left half-written files

asked: 2026-10-31
context: |
  Topic: the worktree state after a call abort, possibly with half-written files (bead coding-harness-6ie).
  Intention: Q-1 says the next attempt builds on the previous state; an abort may leave that state incomplete.
  Today: the abort state is reverted to HEAD.
  Repository change: the runner's attempt hand-over and its tests.
  Architecture change: none beyond Q-1.
  Question: does the next attempt start from the abort state or from the last complete state?
answer: "Auf dem Abbruch-Stand" — the next attempt gets the abort state as a copy, with its diff list and a note that files may be incomplete; the state is saved as an attempt.
answered_by: maintainer
status: answered

In the context of an abort that may leave half-written files, facing a choice between the abort state and the last complete state, we decided that the next attempt gets the abort state as a copy with its diff list and a note that files may be incomplete, and that the state is saved as an attempt, to achieve that no written work is lost, accepting that the next attempt must check incomplete files. — 2026-10-31

## Q-5 · Where a route change shows

asked: 2026-10-31
context: |
  Topic: the visible record of a route change after a failed call (bead coding-harness-6ie).
  Intention: Q-2 made the route change visible; the place was still open.
  Today: Q-2's wording of 2026-10-16 named findings.md.
  Repository change: the runner's output and the change's plan.md.
  Architecture change: none.
  Question: where does a route change show?
answer: "Runner-Ausgabe + plan.md" — in the runner's output and in plan.md; supersedes the 2026-10-16 wording "recorded in findings.md".
answered_by: maintainer
status: answered

In the context of a visible route change after a failed call, facing where to record it, we decided on the runner's output and plan.md, to achieve that the maintainer sees it at run time and in the change's plan, accepting that findings.md no longer carries it (superseding the wording of 2026-10-16). — 2026-10-31

## Details for the draft

[DETAIL] **The ADR addendum is proposed, not written.** Reason: agents do not
write `docs/adr/` (AGENTS.md); the draft names the ADR that holds the doctrine
sentence and gives the addendum text as a proposal for a decision pull
request.

[DETAIL] **The overlap with bead coding-harness-s9r (isolated attempts) and
coding-harness-znc (a failed attempt's work is saved, not deleted) is
designed once.** Reason: the maintainer chose one shared design on
2026-10-15; the draft states which part each bead carries.
