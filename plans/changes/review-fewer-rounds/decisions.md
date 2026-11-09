---
title: "Decisions — review-fewer-rounds"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-3rtn
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, review-loop, adr-0021]
---

# review-fewer-rounds — Decisions

Class: architectural (maintainer 2026-11-07; bead coding-harness-3rtn).

The maintainer gave these answers in the orchestrating conversation on
2026-11-07 and 2026-11-08; the orchestrator recorded each in the notes of
bead coding-harness-3rtn on the day it was given. They are transcribed here
unchanged in substance, one record per question. Questions still open are
listed at the end and are not counted.

## Q-1 · Which review lenses round 1 covers

asked: 2026-11-08
answer: "Plus Wartbarkeit" — five lenses: (1) spec fidelity and scope, (2) hostile input and failure paths, (3) state, retry and abort, (4) tests as evidence, (5) maintainability; artefact formalities (headers, status, plan card against decisions, time ledger) go to a gate instead of a reviewer.
answered_by: maintainer
status: answered
context: |
  Topic: today every reviewer of the loop reads the whole change with no focus, and 26% of 296 loop rows (14 loop records, measured 2026-11-07) concern change-folder formalities only.
  Intention: fewer rounds need each round to find more of what matters; a lens gives every reviewer one job.
  Today: unfocused reviewers; one ladder id per later round; new MAJORs keep appearing late.
  Repository change: reviewer prompts per lens; a formalities gate.
  Architecture change: amends ADR 0021 (review swarms until clean).

## Q-2 · Who sits on each lens

asked: 2026-11-08
answer: every lens is reviewed by the model with the best measured precision, a cheap model of another lineage and Codex gpt-6.1-terra at effort medium — 15 calls in round 1, five of them Codex; think deeply about which aspects must be covered and check for empirical evidence.
answered_by: maintainer
status: answered
context: |
  Topic: measured precision by taken share differs widely between reviewers (2026-11-08 over 1205 loop rows: deepseek-v4.1-flash 91%, kimi-k2.7-code 30%).
  Intention: seat reviewers by evidence and lineage diversity instead of "all reachable".
  Today: round 1 runs the free swarm; later rounds one paid ladder id each.
  Repository change: a seating per lens the runner reads; Codex joins round 1.
  Architecture change: amends ADR 0021's stage order.

## Q-3 · When a second round runs

asked: 2026-11-08
answer: per lens, by the overlap of its three reviewers (a capture-recapture estimate of the defects still undiscovered); a second round runs only for lenses with a high estimate; the threshold comes from research with evidence.
answered_by: maintainer
status: answered
context: |
  Topic: round-1 size predicts later MAJOR+ findings only weakly (r=0.22 rows, 0.25 MAJOR+; 63 changes, measured 2026-11-08) and phase-6 MAJOR+ not at all (r=0.01).
  Intention: a second round where the evidence says defects remain, not by raw count.
  Today: the loop runs until a clean round or the paid ladder is spent.
  Repository change: an estimator and a threshold in the runner, read from configuration.
  Architecture change: replaces "until clean" in ADR 0021 by an estimate-driven second round.

## Q-4 · Where seating, rounds and limits live

asked: 2026-11-08
answer: the model selection must be centrally and easily changeable — likewise which rounds run, the number of rounds, which and how many models sit in a round; one declarative, validated file (the central configuration of bead coding-harness-twvx) holds lenses, seats, round count and order, the second-round trigger and its threshold, and the phase-6 re-check limit; no constant repeats it.
answered_by: maintainer
status: answered
context: |
  Topic: today the stage order and model sets are spread over the runner, model-endpoints.yaml and the documents.
  Intention: a change of seating is a one-line edit with a validator, not a code change.
  Today: constants in scripts/stage2.py; the ladder in model-endpoints.yaml.
  Repository change: the runner, prompts, docs and tests read one file; this change depends on bead coding-harness-twvx.
  Architecture change: configuration becomes the single source for the loop's shape.

## Q-5 · How many phase-6 re-checks

asked: 2026-11-08
answer: the first phase-6 review plus one re-check; after that the runner stops and reports to the maintainer with a proposal (a named limit in the PR, a mechanism repair, or stop); from the second re-check finding of one kind a mechanism repair is required instead of case repairs. The limit lives in the central configuration.
answered_by: maintainer
status: answered
context: |
  Topic: phase-6 re-checks repeated on some changes without converging.
  Intention: a hard end with a decision for the maintainer instead of open-ended re-checks.
  Today: no stated limit on phase-6 re-checks.
  Repository change: a re-check counter and a stop report in the runner.
  Architecture change: none beyond the configured limit.

## Q-6 · What round 2 does with findings

asked: 2026-11-08
answer: round 2 sorts by kind, not by location — a MAJOR or BLOCKER goes into the same last repair (no new full round; phase 6 with its limit follows); a MINOR follows the MINOR rule (tests, security or false statements repaired without asking; style named as an accepted limit); a follow-up bead only for a finding in code outside this change. This replaces the earlier answer of the same day that sorted by location.
answered_by: maintainer
status: answered
context: |
  Topic: round 2 reviews the repair; its reviewers also report rows outside the repair diff.
  Intention: no third full round, yet no real defect left behind.
  Today: every new row may start another round.
  Repository change: triage rules for round 2 in the runner and prompts.
  Architecture change: amends ADR 0021's end condition.

## Q-7 · Style findings

asked: 2026-11-08
answer: an unambiguous style finding (a clear proposal, not a matter of taste) rides along in a repair that runs anyway; it never triggers a repair or a round on its own; matters of taste stay accepted limits named in the PR. The MINOR rule in AGENTS.md changes with this change.
answered_by: maintainer
status: answered
context: |
  Topic: AGENTS.md says style rows are accepted limits, even when the fix is obvious.
  Intention: take the cheap, clear fixes without letting style drive rounds.
  Today: every style row is an accepted limit.
  Repository change: AGENTS.md MINOR rule; triage guidance.
  Architecture change: none.

## Q-8 · Self-review

asked: 2026-11-08
answer: exclude the implementer's model family only when it would be the sole reviewer; when several reviewers run in parallel it may sit among them. Markdownlint and the formalities gate block new and changed files only; the existing stock stays report-only until cleaned.
answered_by: maintainer
status: answered
context: |
  Topic: the implementer's model family may review its own work.
  Intention: keep independence without losing the best-precision seat.
  Today: no stated rule.
  Repository change: a seating constraint the validator checks; gate scope on changed files.
  Architecture change: none.

## Q-9 · The form of a lens

asked: 2026-11-09
answer: "Fehlerklassen + Prüffragen" — each lens is a defect class with a list of concrete check questions, not a role the reviewer plays.
answered_by: maintainer
status: answered
context: |
  Topic: the five lenses of Q-1 need a form in the reviewer prompt.
  Intention: follow the stronger evidence in research.md (scenario reading by defect class found more defects than ad hoc or checklist reading, Porter, Votta and Basili 1995; perspective-based reading showed no clear gain, Ciolkowski 2009).
  Today: reviewers read without focus.
  Repository change: one prompt per lens with its check questions.
  Architecture change: part of the ADR 0021 amendment.

## Q-10 · Where the check questions come from

asked: 2026-11-09
answer: "Aus unseren Funden + Literatur, du gibst frei" — an agent derives the questions per lens from the repository's measured loop and phase-6 rows and from the literature; the maintainer approves the list.
answered_by: maintainer
status: answered
context: |
  Topic: good check questions target the defects this repository actually has (measured 2026-11-08: 86% of phase-6 rows are SPEC, 65% of loop rows MAINT).
  Intention: questions that fit real defects, approved by the maintainer.
  Today: no check questions.
  Repository change: a question list per lens, held in the central configuration (bead coding-harness-twvx) or the prompt.
  Architecture change: none beyond Q-9.

## Q-11 · What triggers a second round

asked: 2026-11-09
answer: "Einzelfund-Anteil, Jackknife nur protokolliert" — the share of accepted findings that only one reviewer of the lens reported decides; the Mh-jackknife and Chao estimates are computed and recorded only.
answered_by: maintainer
status: answered
context: |
  Topic: the remaining-defect estimate per lens from the overlap of its three reviewers (Q-3).
  Intention: a rule that is simple and explainable; the Mh-jackknife, best at three reviewers, still runs about 27% low in the median (Briand et al. 2000) and correlated model errors push it lower.
  Today: no estimator.
  Repository change: a small computation in the runner; both estimates logged.
  Architecture change: part of the ADR 0021 amendment.

## Q-12 · How the second-round threshold is introduced

asked: 2026-11-09
answer: "B: Schatten, immer zweite Runde" — during a shadow period every lens always gets a second round; the single-finding rule (Q-11) is computed and recorded but does not decide; after 10–20 changes the threshold is set from what the second rounds actually found where the rule would have stopped.
answered_by: maintainer
status: answered
context: |
  Topic: the research proposal (second round when at least two single findings make up more than half of a lens's accepted findings, or none of two or more is confirmed by a second reviewer) is the research agent's own derivation; no published threshold exists for three reviewers (research.md).
  Intention: set the threshold from this repository's own data before it decides anything.
  Today: the loop runs until a clean round (4–8 rounds).
  Repository change: threshold and mode (shadow or live) as values in the central configuration (bead coding-harness-twvx); a per-lens record of findings, overlap and both estimates.
  Architecture change: part of the ADR 0021 amendment.

## Open — not counted

- The research questions of 2026-11-08 are not answered: (a) evidence for
  lens-based against unfocused review; (b) capture-recapture estimators for
  three reviewers per lens and a defensible threshold; (c) evidence on
  ensembles and model diversity of LLM reviewers; (d) cost of 15 round-1
  calls against today's rounds and verify runs. The stage-1 exploration of
  2026-11-09 (research.md) did not read the bead and covers the repository
  only. Answered on 2026-11-09 by the Opus research section of research.md.
