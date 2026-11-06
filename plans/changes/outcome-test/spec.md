---
title: "Spec — outcome-test"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
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
- The open scope decision is answered by the maintainer and incorporated
  into this spec before phase 4 starts; no answer or ADR answer is inferred.
- Documents moved with code: `docs/WORKFLOW.md` explains use, the two run
  triggers, source-read failures and the meaning and limits of a score.
- The baseline result names the commit actually measured; the pull request
  cites that run, even when its score is below eight. Fixture records never
  enter the real history.
- The PR file list respects protected areas and non-goals; the runner owns
  regeneration of `plans/INDEX.md` and verification evidence.
- The PR closes the outcome-test bead `coding-harness-3nm5`; its final commit
  carries `Closes-Bead: coding-harness-3nm5`.

## Open decisions

### [DECISION] What the fresh session is allowed to use

Topic: Welche frische Sitzung die Ausgangsmessung abbildet.
Intention: Vor dem Bau muss klar sein, ob der Test das Finden aktueller Regeln
oder ausschließlich das Wissen aus dem Startkontext misst.
Today: Es gibt noch keine Messung; verschiedene Sitzungsarten erhalten
unterschiedlichen Startkontext. Die bisherige Antwort legt Umfang, Häufigkeit
und Ablage fest, aber keinen Zugriff auf Repository-Dateien.
Repository change: Acht feste Fragen und eine gemeinsame Ergebnisdatei;
die gewählte Situation wird bei jedem Lauf mitgeführt.
Architecture change: Keine neue Modellanbindung oder Sitzungsverwaltung;
die vorhandenen Startwege bleiben bestehen.

Goal in one sentence: Eine vergleichbare Ausgangsmessung für spätere Änderungen
an Einstieg und Übergabe schaffen.

Options:

- Option 1 — Arbeitseinstieg messen: Eine neue Claude-Code-Sitzung erhält
  ihren üblichen Startkontext und darf das Repository lesend erkunden. Das
  misst, ob sie die Regeln im normalen Arbeitsablauf richtig findet.
- Option 2 — Startwissen messen: Eine neue Claude-Code-Sitzung antwortet
  allein aus ihrem üblichen Startkontext ohne weitere Dateizugriffe. Das
  macht Lücken der Startinformationen sichtbar, misst aber keinen normalen
  Arbeitsablauf mit Nachschlagen.

Recommendation: Option 1, weil die Ausgangsfrage lautet, ob eine neue Sitzung
mit den aktuellen Regeln arbeiten kann; der Kontext wird für Vergleiche
mitgespeichert.
If you say "ok": Gebaut wird die Messung für Option 1; die Ausgangsmessung
und spätere Läufe benennen Claude Code, das tatsächlich verwendete Modell,
den Startkontext und den erlaubten lesenden Zugriff.
What is lost: Eine isolierte Aussage darüber, welche Antworten schon ohne
Nachschlagen im Startkontext verfügbar waren.

Soll die Ausgangsmessung den normalen Arbeitseinstieg mit lesendem Zugriff
auf das Repository messen (Option 1)?

### Agent details

The following choices are proposed by the agent as reversible implementation
details; they do not answer the scope decision above.

- [DETAIL] Use a local question exporter and deterministic recorder, with the
  orchestrator administering the quiz in an existing fresh-session workflow:
  this adds a measurement without adding model routing or a new launcher.
- [DETAIL] Select the eight topics in criterion 1 from the three originating
  examples and the documented startup/tracker conventions; keep them fixed
  across a comparison instead of silently adapting questions to improve scores.
- [DETAIL] Request short typed answers and compare exact values with only
  outer whitespace and harmless trailing path separators normalized; this
  makes grading reproducible without a second model or a synonym dictionary.
- [DETAIL] Use two hours of phase 4, repairs included, as the appetite: a stop
  for a bounded exporter/recorder, not a promise about its duration.
