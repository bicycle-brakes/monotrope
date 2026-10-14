---
title: "Decisions — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, review-loop, opencode-go, swarm]
---

# Review loop until clean, as a swarm and a ladder — Decisions

Phase 1a, asked by the orchestrating Claude Code session on 2026-10-14, each
question with its context first. The change began as bead coding-harness-dx0
(the review loop runs until a round finds nothing); by the maintainer's answer
Q-4 it merged into bead coding-harness-4fk (the implementation review as a
swarm of OpenCode Go models), which carries it from here.

## Q-1 · Which models review, in which order

asked: 2026-10-14
answer: first three Flash models of OpenCode Go — DeepSeek V4.1 Flash, MiMo-V2.6-Flash, LongCat-2.0; then GLM-5.3-Flash, then Qwen3.8 Flash, then GPT 6 Luna, then Claude Haiku 5.5, then MiniMax M2.7, then MiMo-V2.6-Pro.
answered_by: maintainer
status: answered

Asked as "where is the upper bound" (8 rounds, 5 rounds, or none); the
maintainer answered with the ladder itself: "ich möchte, dass am anfange drei
flash modelle von opencoe laufen, nämlich DeepSeek V4.1 Flash,
MiMo-V2.6-Flash, LongCat-2.0, danach soll GLM-5.3-Flash, dann Qwen3.8 Flash,
dann GPT 6 Luna, dann Claude Haiku 5.5, dann MiniMax M2.7, dann
MiMo-V2.6-Pro". The bead of 2026-10-11 had named MiMo-V2.6-Pro for every
round after the third; this ladder replaces it.

In the context of a loop capped at three rounds on three OpenCode Go models,
facing the choice between a fixed cap and a longer ladder, we decided on a
nine-model ladder across providers to achieve fresh eyes in every round,
accepting more providers to declare and more calls per change. — 2026-10-14

## Q-2 · What "nothing found" means

asked: 2026-10-14
answer: a round is clean when it leaves no taken finding; a round whose findings were all rejected counts as clean.
answered_by: maintainer
status: answered

In the context of rounds that may report only findings the orchestrator
rejects, facing the choice between "no taken finding" and "no finding at
all", we decided on no taken finding to achieve that a model reporting
trivia cannot keep the loop running, accepting that a rejected finding does
not earn another round. — 2026-10-14

## Q-3 · The repair-caused emergency brake

asked: 2026-10-14
answer: it stays — two consecutive rounds whose taken findings were caused by a repair (origin `fix-r`) stop the loop and go to the maintainer, also before the ladder ends.
answered_by: maintainer
status: answered

In the context of the fix-by-case pattern of PR #138, facing the choice
between keeping and dropping the brake in a longer loop, we decided to keep
it to achieve an early stop when repairs feed the reviews, accepting more
interruptions. — 2026-10-14

## Q-4 · The order against the review swarm

asked: 2026-10-14
answer: merged — the loop-until-clean change goes into bead coding-harness-4fk; one rebuild of the review loop instead of two.
answered_by: maintainer
status: answered

In the context of two beads that change the same loop, facing the choice
between this change first and one merged change, we decided to merge them to
achieve one rebuild, accepting that the longer loop arrives with the swarm.
— 2026-10-14

## Q-5 · How the first three Flash models run

asked: 2026-10-14
answer: at the same time, in round 1 — three reviews in parallel, their findings merged, then one repair; from round 2 on one model of the ladder per round.
answered_by: maintainer
status: answered

In the context of "first three Flash models", which could mean parallel or
consecutive rounds, facing that choice, we decided on parallel in round 1 to
achieve three independent views at once and a faster loop, accepting a
merge step for their findings. — 2026-10-14

## Q-6 · When the ladder runs out

asked: 2026-10-14
answer: the ladder is the upper bound — when MiMo-V2.6-Pro's round still leaves a taken finding, the loop stops and reports to the maintainer.
answered_by: maintainer
status: answered

In the context of a nine-step ladder, facing the choice between stopping and
repeating the last model, we decided to stop and report to achieve a bounded
loop, accepting that a hard case reaches the maintainer. — 2026-10-14

## Q-7 · How undeclared models enter

asked: 2026-10-14
answer: each new model (LongCat-2.0, Qwen3.8 Flash, GPT 6 Luna, MiniMax M2.7, and any other not yet in `model-endpoints.yaml`) is declared with its data terms read; a model whose terms show retention or training, or cannot be read, is skipped in the ladder and named in the handover.
answered_by: maintainer
status: answered

In the context of a private repository and models whose data terms are not
read, facing the choice between declaring with read terms and releasing all
at once, we decided on read terms to achieve that no provider keeps or trains
on framework content, accepting a ladder that may run shorter. — 2026-10-14

## Q-8 · Whether free models review

asked: 2026-10-14
answer: when the review reads only the implementation's code — one part of the repository — the free models run first, as a swarm; before each run the list of free models currently offered by OpenCode Go is checked.
answered_by: maintainer
status: answered

The maintainer's words: "wenn nur der code der implemntierung, als nur ein
teil der repo gelesen wird, dann sollten die freien modelle zu erst als
schwarm genutzt werden. dazu sollte vorher immer überprüft werden, welche
freien modelle es gerade bei opencode go gibt". This narrows the research
swarm's rule (change research-swarm, Q-3: free models see no repository
content) for the review: a review limited to the implementation's diff may
go to the free models. How the review's input is limited to the
implementation is left to the spec.

In the context of free models that change over time and whose data terms are
unread, facing the choice between leaving them out of the review and a free
first stage on the implementation only, we decided on the free first stage
with a fresh list each run to achieve many cheap views before the ladder,
accepting that part of the code reaches models without read terms. —
2026-10-14
