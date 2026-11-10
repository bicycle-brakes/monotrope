---
title: "Spec — swarm-report-format"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-4q9y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm]
class: bounded
appetite: 3
adr_files: [docs/adr/0020-phase-1-research-swarm.md]
neighbours: []
---

# Spec — swarm-report-format

Research seats can recover from wrapped JSON and one correctable report
rejection without weakening the report contract (bead coding-harness-4q9y —
repair rejected research reports). Research: `research.md`; intent and
mechanical choices: `decisions.md`.

**Draft blocked:** the requested correction call conflicts with the decided
invocation budget and no-retry rule. Acceptance criteria describe the intended
result; they do not authorise overriding that rule. Resolve the open decision
and redraft before phase 4. No design is due for class `bounded`.

## Problem

The replay documented in `research.md`, “Orchestrator addendum” (2026-11-09,
parser at 01fb3e38), measured seven report rejections in run 1938a24f:
three complete fenced objects had surrounding prose or tool residue; two
answers had extra fields; one exceeded seven claims; one omitted topic 5's
required neighbour field. An eighth partial record was empty.

The runner accepts only bare JSON or a fence occupying the entire answer.
After a topic report fails validation it records `invalid-report`, without
asking the seat to correct it; a required failure prevents reconciliation.
Extra fields, missing topic fields and excessive claims remain actual contract
violations, not material to discard until a report passes.

## Terms

- **Seat:** one frozen endpoint/model contribution to one research topic.
- **Correction:** one new call to that same seat after a process-successful
  answer fails report extraction or validation; not a timeout or transport retry.
- **N:** the number of free online models frozen by preparation; there are
  `33 + 3N` topic contributions and six other contributions.

## Acceptance criteria

1. When a seat returns a contract-valid bare object or exactly one JSON fence,
   the validated report is unchanged from today's result.
   *Refuted by:* either representation fails or its validated claims differ.

2. When a seat returns exactly one complete JSON-object fence with surrounding
   prose or tool residue and no competing JSON-object candidate, its report is
   validated as if the fenced object had been returned alone.
   *Refuted by:* a leading sentence or trailing `</arg_value></tool_call>`
   causes rejection of an otherwise valid report.

3. If an answer has competing object candidates or malformed JSON, extraction
   does not turn it into an accepted report by choosing or repairing content.
   *Refuted by:* two object fences, a bare object beside a fenced object,
   duplicate keys, non-finite values or a truncated object becomes accepted.

4. When extracted content violates the existing report contract, validation
   rejects it with a reason suitable for a correction request.
   *Refuted by:* an eighth claim, an extra field, a missing required topic field
   or a report below the existing evidence floor is silently accepted.

5. When a process-successful topic answer is rejected, the same frozen seat
   receives exactly one correction request containing its rejection reason.
   *Refuted by:* no correction is requested despite available time, more than
   one is requested, a different model is substituted, or a valid first answer
   or a failed/timed-out/cancelled/refused process is retried.

6. When a correction runs, it remains inside that seat's original information,
   tool, declaration, leak-check, concurrency and time boundaries.
   *Refuted by:* a peer answer or private context reaches an online seat, a
   correction bypasses its exact-prompt check, receipts from a different
   attempt support it, provider concurrency exceeds four, or its call exceeds
   the remaining original topic allowance, run deadline or judge reserve.

7. When a correction ends, the published and resumable result retains both
   attempts' evidence and exposes exactly one final outcome for that seat.
   *Refuted by:* the first answer/error or either launch audit disappears, an
   invalid correction reaches the judge, a valid correction is scored twice,
   or resume reuses an unvalidated result or repeats a successful contribution.

8. While corrections are enabled, the run accounts for at most one additional
   invocation per topic contribution under the explicitly authorised budget.
   *Refuted by:* invocation accounting omits corrections or exceeds that
   budget; a clean run consumes correction calls. The proposed ceiling is
   `72 + 6N`, pending the decision below; the current authorised ceiling
   remains `39 + 3N` until an amendment takes effect.

9. When every selected seat supplies a valid report initially or on correction,
   an explore run completes with every selected report accepted.
   *Refuted by:* a wrapper-only failure prevents completion, a corrected seat
   remains failed, or completion drops a selected seat or weakens validation.

## Non-goals

- Changing claim limits, required/allowed fields, evidence resolution, scoring,
  handoff derivation, research record version or reviewer answer formats.
- Retrying other research stages, process failures or an exhausted correction;
  replacing models, adding debate or extending configured time limits.
- Repairing the historical run, importing its external records, or guaranteeing
  success when a model does not answer or continues to break the contract.

## Protected areas

The validator in `scripts/stage2_research_report.py`, selection and availability
policy, public/repository isolation, gate definitions and model endpoints
remain unchanged. Existing ADRs, workflow rules and held prompts are not edited
by an implementation attempt. Changing the retry rule requires the separate
maintainer decision below, not an unannounced exception in code.

## Definition of Done

- The budget decision is resolved and all resulting governance/interview
  obligations are met before implementation; no open decision remains.
- Regression tests and `make verify` pass at the implementation commit.
- The orchestrator records a real explore run's date, commit, run identifier,
  selected seats and accepted reports in `findings.md`, including free seats
  when selected; a simulated run alone does not establish live completion.
- The pull request's file list demonstrates protected areas and non-goals;
  any authorised governance amendment is named in the revised plan.
- The pull request closes coding-harness-4q9y — repair rejected research
  reports; its last commit carries `Closes-Bead: coding-harness-4q9y`.

## Open decisions

[DETAIL] Use three hours of phase 4, including repairs, as the appetite stop;
the existing decisions set no appetite. Keep the selected class `bounded` and
write no `design.md` or ADR draft while the governance question is unresolved.
This makes the limitation visible rather than inventing a maintainer answer.

[DETAIL] Restrict tolerant extraction to topic reports, preserving strict
duplicate-key/non-finite parsing and all schema checks. Leave other callers of
the shared JSON helper unchanged because their contracts are outside this fix.

### [DECISION] Correction calls and the decided invocation ceiling

Topic: Forschungsberichte nach einem Formatfehler einmal korrigieren lassen.
Intention: Den gewünschten Korrekturversuch ermöglichen, ohne eine geltende
Grenze für Modellaufrufe stillschweigend zu überschreiben.
Today: Die Architekturentscheidung zum Forschungsschwarm verbietet
Wiederholungen und erlaubt höchstens `39 + 3N` Aufrufe; `N` ist die Zahl der
ausgewählten kostenlosen Modelle (ADR 0020, Punkt 9).
Repository change: Zusätzlich zur toleranteren Erkennung verpackter Berichte
käme je fehlerhaftem Themenbericht höchstens ein Korrekturaufruf hinzu.
Architecture change: Dafür müsste die beschlossene Aufrufgrenze geändert
werden; Modellauswahl, Berichtsschema und Zeitgrenzen blieben bestehen.

Goal in one sentence: Vollständige Berichte trotz Verpackungsfehlern annehmen
und echte Formatfehler einmal vom ursprünglichen Modell korrigieren lassen.

Options:
1. Einen Korrekturversuch je Themenbericht erlauben: höchstens `33 + 3N`
   zusätzliche Aufrufe, insgesamt höchstens `72 + 6N`; das erhöht den möglichen
   Kontingentverbrauch und erfordert eine wirksame Architekturentscheidung.
2. Die heutige Aufrufgrenze und das Wiederholungsverbot behalten: Nur die
   Verpackungsfehler werden behoben; echte Vertragsverstöße beenden den Sitz
   weiterhin. Dafür müsste der bisherige Änderungsumfang ausdrücklich gekürzt
   und anschließend neu spezifiziert werden.

Recommendation: Option 1 — sie erfüllt den festgehaltenen Korrekturwunsch mit
einer endlichen, nachvollziehbaren Obergrenze.
If you say "ok": Die Orchestrierung bereitet zuerst die erforderliche
Entscheidungsänderung und deren Interviewnachweise vor; nach deren Wirksamkeit
wird dieser Entwurf aktualisiert und die beschriebene Korrektur gebaut.
What is lost: Die bisherige feste Obergrenze für Kontingentverbrauch; die
bestehenden Zeitgrenzen bleiben der Stop für einen laufenden Schwarm.

Darf die Aufrufgrenze für höchstens einen Korrekturversuch je Themenbericht
von `39 + 3N` auf höchstens `72 + 6N` steigen?
