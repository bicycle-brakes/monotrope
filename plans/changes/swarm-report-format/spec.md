---
title: "Spec — swarm-report-format"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-12
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
repair rejected research reports). Research: `research.md`; the maintainer's
five answers of 2026-11-10: `decisions.md#Q-1` through `decisions.md#Q-5`.

The invocation amendment is already in this branch's ADR 0020, point 9, at
829e316b (2026-11-10); it takes effect with this change's decision pull
request, not before its merge. No design is due for class `bounded`.

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
   *Basis:* `decisions.md#Q-2`; `decisions.md#Q-3`.

2. When a seat returns exactly one complete JSON-object fence with surrounding
   prose or tool residue and no competing JSON-object candidate, its report is
   validated as if the fenced object had been returned alone.
   *Refuted by:* a leading sentence or trailing `</arg_value></tool_call>`
   causes rejection of an otherwise valid report.
   *Basis:* `decisions.md#Q-3`.

3. If an answer has competing object candidates or malformed JSON, extraction
   does not turn it into an accepted report by choosing or repairing content.
   *Refuted by:* two object fences, a bare object beside a fenced object,
   duplicate keys, non-finite values or a truncated object becomes accepted.
   *Basis:* `decisions.md#Q-2`; `decisions.md#Q-3`.

4. When extracted content violates the existing report contract, validation
   rejects it with a reason suitable for a correction request.
   *Refuted by:* an eighth claim, an extra field, a missing required topic field
   or a report below the existing evidence floor is silently accepted.
   *Basis:* `decisions.md#Q-2`; `decisions.md#Q-5`.

5. When a process-successful topic answer is rejected, the same frozen seat
   receives exactly one correction request containing its rejected answer and
   rejection reason, if its existing time boundaries permit a launch.
   *Refuted by:* no correction is requested despite available time, more than
   one is requested, a different model is substituted, or a valid first answer
   or a failed/timed-out/cancelled/refused process is retried.
   *Basis:* `decisions.md#Q-1`; `decisions.md#Q-4`; `decisions.md#Q-5`.

6. When a correction runs, it remains inside that seat's original information,
   tool, declaration, leak-check, concurrency and time boundaries.
   *Refuted by:* a peer answer or private context reaches an online seat, a
   correction bypasses its exact-prompt check, receipts from a different
   attempt support it, provider concurrency exceeds four, or its call exceeds
   the remaining original topic allowance, run deadline or judge reserve.
   *Basis:* `decisions.md#Q-1`; `decisions.md#Q-4`; the unchanged isolation and
   scheduling contract described in research.md, “Surface 1”.

7. When a correction ends, the published and resumable result retains both
   attempts' evidence and exposes exactly one final outcome for that seat.
   *Refuted by:* the first answer/error or either launch audit disappears, an
   invalid correction reaches the judge, a valid correction is scored twice,
   or resume reuses an unvalidated result or repeats a successful contribution.
   *Basis:* `decisions.md#Q-4`; the existing publication/resume contract
   described in research.md, “Surface 1”.

8. While corrections are enabled, the run accounts for at most one additional
   invocation per topic contribution within the ceiling of `72 + 6N`.
   *Refuted by:* invocation accounting omits corrections or exceeds that
   budget; a clean run consumes correction calls instead of retaining its
   `39 + 3N` maximum. Reused contributions launch no calls.
   *Basis:* `decisions.md#Q-1`.

9. When every selected seat supplies a valid report initially or on correction,
   an explore run completes with every selected report accepted.
   *Refuted by:* a wrapper-only failure prevents completion, a corrected seat
   remains failed, or completion drops a selected seat or weakens validation.
   *Basis:* `decisions.md#Q-1`; `decisions.md#Q-2`; `decisions.md#Q-3`;
   `decisions.md#Q-4`; `decisions.md#Q-5`.

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
remain unchanged. An implementation attempt does not edit held paths.
The orchestrator owns the already prepared ADR 0020 amendment and the matching
wording in `docs/WORKFLOW.md`; their policy change takes effect on merge.

## Definition of Done

- The five answered interview records satisfy the ADR-change minimum; no
  open decision remains. The existing ADR amendment travels in the same
  decision pull request, with `docs/WORKFLOW.md` brought into agreement.
- Regression tests and `make verify` pass at the implementation commit.
- The orchestrator records a real explore run's date, commit, run identifier,
  selected seats and accepted reports in `findings.md`, including free seats
  when selected; a simulated run alone does not establish live completion.
- The pull request's file list demonstrates protected areas and non-goals;
  documents moved with the code: ADR 0020, `docs/WORKFLOW.md` and this change's
  spec, plan and findings. No new ADR or design document is due for `bounded`.
- The pull request closes coding-harness-4q9y — repair rejected research
  reports; its last commit carries `Closes-Bead: coding-harness-4q9y`.

## Open decisions

None open. The invocation ceiling, unchanged contract, wrapped-object
extraction, same-model correction and rejection of extra fields are answered
in `decisions.md#Q-1` through `decisions.md#Q-5` (2026-11-10).

[DETAIL] Retain the existing three-hour phase-4 appetite, repairs included;
no maintainer answer changes it. Retain class `bounded`, so phase 2b does not
run and no new ADR draft is due; this change amends the existing ADR 0020.

[DETAIL] Restrict tolerant extraction to topic reports, preserving strict
JSON parsing and all schema checks. Leave other callers of the shared JSON
helper unchanged because their contracts are outside this fix.
