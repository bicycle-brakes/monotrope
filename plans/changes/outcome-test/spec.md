---
title: "Spec — outcome-test"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-3nm5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, measurement, outcome-test]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — outcome-test

Measure a fresh session's answers to eight fixed harness questions against
answers read from the current repository, preserving a dated, commit-bound
result for comparison (bead coding-harness-3nm5, outcome test for fresh
sessions). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- Existing gates check artefacts, not whether a fresh session can answer
  questions about the harness. The originating evaluation explicitly ran no
  outcome experiment (`research.md`, “What exists today”, evidence dated
  2026-11-02; draft gap check at commit `86a1d919`).
- Expected answers are spread over doctrine, code and directory conventions;
  copying today's answers into a quiz would let an obsolete rule score as
  correct (`research.md`, “Ground truth”, checked again at `86a1d919`).
- There is no baseline against which to judge changes to startup knowledge.
  The maintainer chose eight questions, a baseline now, subsequent runs before
  handover-convention or instruction-file changes, and one JSONL history,
  rather than nightly runs (`decisions.md#Q-1`, 2026-11-06).

## Terms

**Fresh session:** a session without this author's conversation or a resumed
measurement thread; its permitted startup context and repository access are
the unresolved maintainer decision below.

**Question set:** eight stable question identifiers and answer shapes, with
source-reading instructions but no stored expected answers.

**Measured result:** one actual session's submitted answers graded against
readable sources from the same repository snapshot; a low score is evidence,
not a failed implementation or permission to change the questions.

## Acceptance criteria

1. When a questionnaire is requested, it contains exactly eight stable
   questions covering the primary repair model, repair fallback model,
   default verification memory floor, its override variable, run-plan
   directory, handover directory, tracker command and repository instruction
   file.
   *Refuted by:* a source-value change changes the question identities, one
   topic is missing, or the questionnaire contains seven or nine questions.

2. When answers are graded, each expected answer is derived anew from the
   measured repository's current doctrine, code or convention, without a
   persisted answer key or a fallback to an old value.
   *Refuted by:* changing a source value in a fixture leaves the old answer
   correct, or an obsolete historical ADR answer overrides current doctrine.

3. When the tool prepares material for the answering session, it supplies
   questions and answer shapes without supplying the derived answer key.
   *Refuted by:* an expected-value field or a copied solution passage appears
   in the questionnaire or answer template.

4. When a real measurement is recorded, it identifies the harness, model,
   startup context and permitted repository access of a separately started,
   memory-free session under the maintainer-selected measurement scope.
   *Refuted by:* an author answers its own quiz in its existing conversation,
   a resumed thread is called fresh, scope metadata is absent, or one
   harness's result is described as measuring all harnesses.

5. When a readable answer submission is scored, each of the eight questions
   receives a deterministic correct or incorrect verdict and the summary
   reports the number correct out of eight.
   *Refuted by:* a missing or empty answer reduces the denominator, a correct
   keyword embedded in contradictory prose earns a point, or grading calls a
   model to judge another model's answer.

6. If required evidence is unreadable, ambiguous or no longer matches the
   snapshot supplied to the answering session, the run is reported as not
   measured and appends no scored result.
   *Refuted by:* an unavailable expected answer becomes a wrong model answer,
   malformed input becomes a zero score, or a changed source is silently
   graded as though the session had seen it.

7. When a measured run is recorded, exactly one JSON line is appended to
   `docs/research/outcome-test-results.jsonl` with its UTC date, full commit,
   question-set and source fingerprints, session metadata, purpose, submitted
   answers, eight verdicts and score, without storing the derived answer key.
   *Refuted by:* a record lacks its commit or date, grading another submission
   overwrites history, one run occupies multiple lines, or expected-value
   fields are persisted alongside the subject's own answers.

8. If an existing result history cannot be read as the supported JSONL
   format or an append cannot be completed, the tool reports failure without
   presenting a successful measurement or discarding existing records.
   *Refuted by:* a truncated last record is silently repaired, previous lines
   change, or a refused append exits successfully.

9. When this change is completed, one actual baseline is recorded and the
   operating instructions require the same on-demand procedure before every
   change to `AGENTS.md` or the handover convention.
   *Refuted by:* only mocked runs exist, the baseline is fabricated from the
   answer key, the instructions omit either trigger, or they substitute a
   nightly schedule for the maintainer's chosen frequency.

10. While the measurement tool runs, its only repository write is the explicit
    append to the common result history; session launch and model access
    remain with the existing authorized workflow.
    *Refuted by:* it edits doctrine, updates Beads, invokes a model or its API,
    installs a hook or gate, changes routing, or writes through a substituted
    result-file path outside the repository.

## Non-goals

- Nightly scheduling, CI admission, a new verification gate, automatic
  change detection, dashboards or automatic consolidation comparisons.
- New model endpoints, model-call verbs, session launchers, hook changes or
  routing policy; foreign sessions still go through `scripts/stage2.py`.
- Behavioural evaluation of phase prompts, teaching the subject the answers,
  a statistically representative benchmark, a universal passing threshold,
  or a claim that one run establishes knowledge in every harness.
- Design and ADR documents: phase 2b never runs for class `bounded`.

## Protected areas

`AGENTS.md`, `tools/claude-code/`, `scripts/stage2*.py`, `scripts/verify_lock.py`,
`docs/orchestration.md`, `docs/adr/`, `decisions/`, `prompts/`, `templates/`,
model configuration and harness/CI configuration remain unchanged. They are
sources or existing launch mechanisms, not implementation targets.
`docs/WORKFLOW.md` may describe operating this measurement without changing
the rules it measures. Other changes' artefacts and the tracker are untouched.

## Definition of Done

- `make verify` green, including deterministic offline mechanism tests.
- The scope decision is answered (`decisions.md#Q-2`, 2026-11-08) and
  incorporated above; no answer or ADR answer is inferred.
- Documents moved with code: `docs/WORKFLOW.md` explains use, the two run
  triggers, source-read failures and the meaning and limits of a score.
- The baseline result names the commit actually measured; the pull request
  cites that run, even when its score is below eight. Fixture records never
  enter the real history.
- The PR file list respects protected areas and non-goals; the runner owns
  regeneration of `plans/INDEX.md` and verification evidence.
- The PR closes the outcome-test bead `coding-harness-3nm5`; its final commit
  carries `Closes-Bead: coding-harness-3nm5`.

## Decided scope

The fresh session is a new Claude Code session with its usual start context
and read access to the repository (option 1, `decisions.md#Q-2`, maintainer
2026-11-08). Every run records Claude Code, the model actually used, the start
context and the permitted read access; comparisons hold only between runs with
the same labels. What is given up: a separate statement of what the start
context alone already holds.
