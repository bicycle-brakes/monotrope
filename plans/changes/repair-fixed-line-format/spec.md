---
title: "Spec — repair-fixed-line-format"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-hgvp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, repair]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — repair-fixed-line-format

Repair answers tolerate explanations beside an unambiguous fixed status,
and every repair attempt leaves readable, protected answer evidence
(bead coding-harness-hgvp). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At research baseline `79a74f75` (2026-10-26), the answer parser counts every
line naming a taken identifier before validating its status. An explanation
beside the actual fix therefore produces `several fixed lines`, despite the
prompt saying report prose is ignored. Research records four rejected
Sonnet repair attempts on 2026-10-26; their original answers were not kept,
so this explanation of those incidents remains an inference.

The existing failed-attempt ref preserves files, not the answer. A rejection
cannot be diagnosed from the model's actual output after its temporary
directory disappears (`research.md`, “What exists today” and “Caveat”).

## Terms

- **Taken identifier:** the exact identifier of a finding selected for repair,
  including free-text phase-6 identifiers.
- **Fixed claim:** a collected answer line whose trimmed right side starts
  `fixed — `; its validity is still checked by the existing status grammar.
- **Distinct:** different after the parser's existing line normalization
  (outer whitespace, list marker and identifier decoration removal, and
  trimming the identifier and right side); no semantic equivalence is assumed.
- **Protected answer:** the full returned answer after the existing credential
  scrubbing and diagnostic denylist protection, without tail truncation.

## Acceptance criteria

1. When a taken identifier has exactly one distinct valid fixed claim,
   explanatory lines for that identifier do not fail the answer check.
   *Refuted by:* an explanation before or after that claim causes a format
   failure for a loop identifier or an exact free-text identifier.
   *Basis:* decisions.md#Q-1.

2. When normalized fixed claims for one taken identifier are identical,
   repetitions count as one claim.
   *Refuted by:* two identical claims separated by prose cause `several fixed lines`.
   *Basis:* decisions.md#Q-2.

3. When a taken identifier has two distinct fixed claims, the answer check
   rejects the attempt with that identifier's `several fixed lines` diagnostic.
   *Refuted by:* choosing the first, last or only valid claim permits the attempt.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.

4. If a taken identifier has no valid fixed claim, the answer check rejects
   the attempt.
   *Refuted by:* explanation alone, a missing row, an invalid test reference or
   an empty `not a test` reason is accepted as a repair status.
   *Basis:* decisions.md#Q-1.

5. When an answer contains an identifier rejected by the existing unknown-id
   rules, explanatory-line filtering still rejects that identifier.
   *Refuted by:* an unknown loop id, an unknown finding id with an established
   prefix, or an unknown free-text id claiming a fix is silently accepted.
   *Basis:* decisions.md#Q-1; research.md, “What exists today”.

6. When a repair model call ends, its complete protected answer remains
   retrievable as uniquely identified local attempt evidence after success,
   rejection, retry and baseline restoration.
   *Refuted by:* an accepted or failed attempt loses its output, a later
   attempt or run overwrites it, or only a diagnostic tail survives.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3.

7. When the repair answer check rejects conflicting claims, its diagnostics
   identify the saved answer and quote each distinct contested claim for the
   affected identifier through the existing diagnostic protection.
   *Refuted by:* the failure names only `several fixed lines`, points to an
   unavailable answer, or quotes an unprotected line.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3.

8. While repair answers are retained, evidence storage obeys the existing
   credential and denylist protection policy on every repair route.
   *Refuted by:* a keyless Codex or Sonnet answer writes a matching secret
   literally, a blocking rule is hidden by redaction, or protection failure
   falls back to writing raw output.
   *Basis:* decisions.md#Q-3; research.md, “Draft gap checks”.

9. When the repair instructions describe answer handling, they state the
   unique-claim, identical-repetition, conflicting-claim and retained-answer rules.
   *Refuted by:* the shared answer prompt or workflow repair subsection still
   promises that every identifier-prefixed explanation counts as a fix, rejects
   identical repetitions, or omits how to find retained answer evidence.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2; decisions.md#Q-3.

## Non-goals

- No new status grammar, identifier grammar, repair route, attempt count,
  red-first rule, finding selection rule or checkpoint policy.
- No reconstruction of historical answers, remote evidence upload, new
  retention/cleanup policy, or full answers embedded in `findings.md`.
- No change to answer handling for explore, draft, implement or review.
- No design or ADR: this bounded fix adjusts the existing repair boundary.

## Protected areas

Other changes, ADRs, tracker data, endpoint declarations, permissions and gate
definitions remain outside this change; they do not implement the answered scope.

## Definition of Done

- `make verify` is green, including tests proving the parser and evidence failures.
- Documents moved with the code: the repair subsection of `docs/WORKFLOW.md`,
  this spec and `plan.md`; the runner maintains `findings.md` and `plans/INDEX.md`.
- The pull request's file list shows the protected areas untouched and non-goals unbuilt.
- The pull request closes coding-harness-hgvp (repair answer format and evidence);
  its last commit carries `Closes-Bead: coding-harness-hgvp`.
- Special runs: none; all model-call regressions use local stand-ins.

## Open decisions

None open. The maintainer's answer is preserved in `decisions.md#Q-1`.

- [DETAIL] Preserve the existing line normalization and compare normalized
  claims literally; deduplicate before status validation, never by the status
  validation's rewritten output, so different claims cannot collapse silently.
- [DETAIL] A lone malformed known-id line retains its current diagnostic;
  beside a fixed claim it is explanation unless it itself starts `fixed — `.
  A malformed fixed claim remains a claim and must be validated or conflict.
- [DETAIL] Retain output available from failed calls too; record explicitly
  when no answer was returned, without fabricating missing output or retrying.
  Evidence failure must be reported and must not permit a successful checkpoint.
- [DETAIL] Use local evidence beside the existing attempt machinery, outside
  tracked files, uniquely keyed per invocation and attempt; this preserves
  answers through restore without committing whole model reports.
- [DETAIL] The phase-4 appetite is one hour including repairs, a stop chosen
  for this bounded parser and evidence fix; no earlier artifact sets a budget.
