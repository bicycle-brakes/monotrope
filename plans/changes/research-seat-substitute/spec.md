---
title: "Spec — research-seat-substitute"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-0ysc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm]
class: bounded
appetite: 4
adr_files: [docs/adr/0020-phase-1-research-swarm.md]
---

# Spec — research-seat-substitute

A failed research seat gets one eligible substitute so a single model failure need not end the run (bead `coding-harness-0ysc`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- As recorded in `research.md` on 2026-11-28, a failed finder stops the run, and a failed required topic seat stops it before the judge; neither receives a substitute. The research reports 2 of 10 runs complete as of 2026-11-25, without independently reading those runs.
- The same research records that two finder runs ended on invalid reports and a third completed after a manual model change, as reported on 2026-11-27.
- The existing research-swarm decision forbids run-time swaps; it must be reconciled with the maintainer's later direction recorded in `decisions.md` before implementation can be merged.

## Acceptance criteria

1. When a required finder or topic seat times out, fails, or produces an invalid report, the run gives that logical seat at most one substitute attempt.
   *Refuted by:* A qualifying failure launches two substitutes for the same logical seat.
2. When an eligible substitute is available and the run permits another call, the failed seat receives one substitute attempt.
   *Refuted by:* A qualifying failure ends without an attempt despite an eligible substitute and available call time.
3. When a substitute is selected, it is the next reachable admitted model for the failed seat's own trio and data class.
   *Refuted by:* The run selects an ineligible model, a model from the other trio, or a later eligible candidate.
4. When a substitute returns a valid report, the run uses it as the failed logical seat's result.
   *Refuted by:* A valid substitute report is discarded and that required seat remains failed.
5. If the substitute also fails, the required logical seat remains unsuccessful and the run is incomplete.
   *Refuted by:* A required seat with two failed attempts is treated as successful or the run completes.
6. When a substitute is attempted, the run history records its model and the reason for replacing the original seat.
   *Refuted by:* The published history omits the substitute model or the original failure reason.
7. When a run resumes, a completed substitute result is reused only after the existing identity and validation checks succeed.
   *Refuted by:* Resume accepts a mismatched or invalid substitute report, or launches another substitute after an eligible result is reused.
8. When no eligible substitute or call time remains, the run records the reason and leaves the required seat unsuccessful.
   *Refuted by:* The run silently selects an ineligible model or reports the required seat successful.
9. While a substitute is used, the existing admission, data-class and leak checks apply to its calls.
   *Refuted by:* A substitute receives a prompt after one of those checks rejects it.

## Non-goals

- Changing finder limits, model terms, provider admission policy, or the judge's standard of evidence.
- Promising a measured improvement in completion rate from this change alone.
- Choosing the unresolved treatment of best-effort free seats or topic corrections without the maintainer's answer below.

## Protected areas

Model credentials, private customer material and existing admission and leak-check boundaries remain protected; no prompt may bypass them.

## Definition of Done

- `make verify` green at the implementation head.
- `docs/adr/0020-phase-1-research-swarm.md` and `docs/WORKFLOW.md` reconciled with the approved behavior in the same pull request; the interview gate's requirements for the ADR edit are met.
- Protected areas untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-0ysc`; its last commit carries `Closes-Bead: coding-harness-0ysc`.
- Special runs: none required; future completion rates are observations, not a release gate.

## Open decisions

[DETAIL] A substitute is associated with the original logical seat in the record, so downstream counting still sees one seat. This is reversible and prevents double-counting.

[DECISION] The recorded direction does not specify whether an invalid topic report gets the existing same-model correction before its substitute, nor whether the direction changes the best-effort free online seats. The existing decision also forbids swaps and describes those seats as never substituted. These choices affect call cost and the scope of the established research contract and cannot be settled by a silent default.

Topic: Ersatz bei ungültigen Berichten und freiwilligen Forschungsplätzen.
Intention: Die neue Ersatzregel muss zu den bestehenden Regeln für Korrekturen und freiwillige Plätze passen.
Today: Ein ungültiger Themenbericht kann einmal vom gleichen Modell korrigiert werden; freiwillige Online-Plätze werden nicht ersetzt.
Repository change: Die Änderung legt fest, wann ein Ersatz gestartet wird und ob freiwillige Plätze ihn erhalten.
Architecture change: Die bestehende Forschungsentscheidung wird entsprechend angepasst; Zulassung und Datenschutz bleiben bestehen.

Goal in one sentence: Fehlgeschlagene Forschungsplätze sollen mit einem klar begrenzten Aufwand behandelt werden.
Options: A — Bestehende Korrektur zuerst, Ersatz nur für verpflichtende Plätze: bewahrt die heutige Korrektur, kann aber einen zusätzlichen Aufruf kosten und freiwillige Ausfälle bleiben bestehen. B — Ersatz sofort für alle Plätze: kann mehr Ausfälle abfangen, ersetzt aber die bisherige Korrektur und erhöht mögliche Aufrufe für freiwillige Plätze.
Recommendation: A — weil sie die bisherige Behandlung freiwilliger Plätze und die Korrektur erhält.
If you say "ok": Verpflichtende Themenplätze erhalten nach einer erfolglosen bestehenden Korrektur höchstens einen Ersatz; freiwillige Online-Plätze bleiben unverändert.
What is lost: Option B könnte auch Ausfälle freiwilliger Plätze auffangen und früher ein anderes Modell einsetzen.
Downside you accept: A — ein zusätzlicher Korrekturaufruf kann Zeit kosten und freiwillige Plätze bleiben ohne Ersatz; B — die bisherige Korrektur entfällt und freiwillige Plätze können weitere Aufrufe verursachen.

Welche Option und den dazu genannten Nachteil akzeptierst du?
