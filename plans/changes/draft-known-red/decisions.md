---
title: "Decisions — draft-known-red"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage2, draft]
---

# draft-known-red — Decisions

Class: feature (bead coding-harness-83e; the maintainer's answer B on 2026-11-22 amends ADR 0016, so the change carries an ADR addendum).

## What the research changed (orchestrator, 2026-11-22)

The bead (2026-10-17) wanted two things: (1) a draft that touches only plans and docs is judged by the gates its files can break, not by a known-red test suite; (2) a Sonnet fallback when GLM fails, since `--stage2-off` is refused for `draft`.

Part (1) is already in place: the draft runs only the document subset of the gate registry (`document_gates` in `scripts/stage2.py`, `docs/WORKFLOW.md` §4 "The draft"), and every draft record of 2026-11-21 says "document checks only, no tests ran". A known-red pytest can no longer fail a draft. Part (2) is still open: `scripts/stage2.py` refuses `--stage2-off` for every verb except explore, implement and repair, and the draft's route list ends at GLM 5.3.

## SKIP · interview

status: skipped
reason: The bead states what is wanted (a Sonnet fallback for the draft when GLM fails, and the draft judged by the gates its files can break); the first part is already merged, the second is a route addition in the existing Stage-1 pattern. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope narrows to the route.** Part (1) is recorded as already done, with the evidence above; this change adds no gate selection.
- **`--stage2-off [REASON]` is accepted for `draft`,** with the same record line and reason as explore, implement and repair; the model is Opus 5.5 at effort `xhigh` (Q-1, superseding the earlier Sonnet reading). Reason: one pattern for all writing verbs; the bead names the refusal as the gap.
- **The automatic fallback:** after the GLM 5.3 attempt fails (call failure or red document check), the draft does not fall through to Sonnet on its own; the runner's final message names `--stage2-off` as the next step. Reason: `docs/WORKFLOW.md` §3 says a failed model process stops instead of silently changing route, and the relaxation for writing attempts belongs to coding-harness-s9r / coding-harness-6ie, whose maintainer decision of 2026-10-16 is not yet implemented.
- **A failed draft keeps its work visible:** unchanged; the attempt refs under `refs/stage2/attempts/` already hold it, and the final message names them.

## Q-1 · The draft's Stage-1 route against ADR 0016 decision 9

asked: 2026-11-22
answer: B — amend ADR 0016: `--stage2-off` is accepted for `draft`, and the Stage-1 draft runs on Opus 5.5 at effort `xhigh`, as `docs/WORKFLOW.md` §3 assigns phases 2, 2b and 3 — not on Sonnet. The amendment is an ADR addendum to decision 9.
answered_by: maintainer
status: answered
context: |
  Topic: whether the draft gets a Stage-1 route, and on which model.
  Intention: spec-review round 1 found that accepted ADR 0016 (human-decided), decision 9, says "Where Stage 2 is off, Opus 5.5 drafts by hand as §3 says; draft has no Stage-1 route", while this change adds exactly that route (F-1), and that §3 gives phases 2, 2b and 3 to Opus at effort xhigh, not to Sonnet (F-2).
  Today: the draft's route list ends at GLM 5.3; --stage2-off is refused for draft; the orchestrator drafts by hand when every route fails.
  Repository change: Options: A close the bead as done (part 1 merged, part 2 conflicts with the ADR); B amend ADR 0016 and add a Stage-1 draft route on Opus xhigh; C keep the Sonnet route as drafted.
  Architecture change: ADR 0016 decision 9 amended by an addendum.

In the context of a draft whose every route failed, facing a hand draft or a runner route, we decided to amend ADR 0016 so that --stage2-off runs the draft on Opus 5.5 at effort xhigh, to achieve night runs that draft without the orchestrator's hand, accepting more load on the runner account's Opus limits and an ADR addendum. — 2026-11-22

## Q-2 · Automatic fall-through to Opus after GLM

asked: 2026-11-23
answer: A — automatic: when the GLM 5.3 draft attempt fails (call failure or red document check), the runner drafts on Opus 5.5 at effort `xhigh` by itself, visibly with its reason in findings.md; `--stage2-off [REASON]` stays available to start on Opus directly.
answered_by: maintainer
status: answered
context: |
  Topic: whether the Opus draft route runs on its own after GLM or only on command.
  Intention: on 2026-11-23 Codex was usage-limited until 16:40 and GLM 5.3 answered unrecognized_model, so three lanes (isolated-attempts, doc-currency, leak-diff-tests-exemption) waited with their drafts; the maintainer decided on 2026-11-22 for coding-harness-s9r that a failed model call falls through to the next route.
  Today: the draft's route list ends at GLM 5.3; --stage2-off is refused for draft.
  Repository change: Options: A automatic fall-through to Opus after GLM, plus --stage2-off; B only on command (--stage2-off named as the next step); C skip GLM, Codex then Opus.
  Architecture change: ADR 0016 decision 9 addendum (Q-1) gains the automatic route.

In the context of drafts that stall when Codex and GLM fail, facing a manual or an automatic Opus route, we decided the draft falls through to Opus xhigh on its own after GLM, to achieve night runs whose drafts do not stall, accepting more load on the runner account's Opus limits. — 2026-11-23

## Q-3 · When Opus cannot draft either

asked: 2026-11-23
answer: A, with an addition — the runner stops with a clear message naming every failed route and its reason, the lane is parked and the other lanes go on; the attempts stay saved as side refs; after five hours the draft is tried again (the maintainer's words: "A, aber nach 5 stunden erneuter versuch").
answered_by: maintainer
status: answered
context: |
  Topic: what follows when Codex, Codex repair, GLM and Opus all fail to draft.
  Intention: the Opus route runs on the runner's Claude account, whose five-hour and weekly limits stopped calls on 2026-11-21/22; after Opus no route is left.
  Today: the draft's route list ends at GLM 5.3; the orchestrator drafts by hand (ADR 0016 decision 9).
  Repository change: Options: A stop with a message naming every failed route, park the lane, keep the attempts as side refs; B the runner waits and retries by itself (for example after 30 minutes, at most three times); C the orchestrator drafts by hand as today.
  Architecture change: none beyond the ADR 0016 addendum of Q-1.

In the context of a draft whose every route failed, facing a stop, an in-call wait or a hand draft, we decided to stop and park the lane and to retry the draft after five hours, to achieve free lanes meanwhile and a retry once a five-hour limit has reset, accepting a lane that waits five hours when the limit was short. — 2026-11-23

## Q-4 · Who starts the retry after five hours

asked: 2026-11-23
answer: A — when it parks the lane, the runner writes `retry_after: <time>` into the lane's status file in the state directory (readable by every harness) and names the time in its message and record; every lane watch (today the session watch, later the heartbeat of coding-harness-a6ns) reads the line and starts the draft once the time is reached.
answered_by: maintainer
status: answered
context: |
  Topic: the trigger of the five-hour retry decided in Q-3.
  Intention: the runner only runs while a command runs; a wake mechanism without an awake session is planned in coding-harness-a6ns (advance verb, heartbeat); on 2026-11-23 the session watch alone left gaps.
  Today: nothing schedules a retry.
  Repository change: Options: A the runner writes retry_after into the lane's status file and the lane watch acts on it; B the runner registers an operating-system timer (launchd or at) when it parks; C only the message, a person or the watch remembers it.
  Architecture change: a retry_after field in the lane status file, read by the lane watch.

In the context of a parked draft that should be retried after five hours, facing an operating-system timer or a recorded time, we decided the runner records retry_after where every harness can read it and the lane watch starts the retry, to achieve a harness-neutral trigger without a process of its own, accepting that the retry waits for the next watch. — 2026-11-23

## Q-5 · Who reviews a spec that Opus drafted

asked: 2026-11-23
answer: A — the phase-2a review stays with Opus 5.5 in a fresh session without the draft's history; the review record says visibly that draft and review came from the same vendor; the second view comes from the review loop's OpenCode Go models before any merge.
answered_by: maintainer
status: answered
context: |
  Topic: the reviewer of a spec drafted on the new Opus route.
  Intention: since PR #432 (coding-harness-ttic) the Opus spec review is mandatory before implement; with the Stage-1 draft route Opus could review its own draft, and one model tends to miss its own blind spots.
  Today: Codex or GLM drafts, Opus reviews.
  Repository change: Options: A Opus reviews in a fresh session, marked same-vendor, the loop supplies the second view; B another model (for example DeepSeek through OpenCode Go) reviews in phase 2a, an ADR 0016 addendum; C the draft waits for Codex to read it before review.
  Architecture change: none beyond the ADR 0016 addendum of Q-1.

In the context of a spec drafted by the same model that reviews it, facing a same-vendor review, a different reviewer or a wait for Codex, we decided Opus reviews in a fresh session with a visible same-vendor mark and the loop supplies the second view, to achieve no extra stage when routes fail, accepting a phase-2a review without a second vendor for these drafts. — 2026-11-23
