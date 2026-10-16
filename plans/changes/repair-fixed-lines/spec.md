---
title: "Spec — repair-fixed-lines"
status: draft
implementation_status: partial
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-ugi
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair]
class: bounded
appetite: 1
adr_files: []
---

# Spec — repair-fixed-lines

Repair answers tolerate incidental prose without weakening finding validation,
and hand repairs use the same completed status as runner repairs (bead
`coding-harness-ugi` — repair answer parsing and completed-row handling).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

The exploration dated 2026-10-15 records two failures in the Haiku and Pi
pin repairs. `check_repair_answer` treats `expected:`, `found:`, `relevant:`,
`proposal:` and `Resume:` as unknown finding identifiers, although the embedded
implementation prompt asks for those reports. Such an answer fails after
`make verify` has already passed.

The same exploration shows that `repair_targets` demands rows already repaired
by hand when their Status still begins `taken`. Examples include
`taken — …; fixed by …` and `taken — …; fixed: …`; the next attempt fails
with a missing fixed line. The existing `fixed — …` status already excludes
completed rows and is the agreed form for both writers.

## Terms

- **Active row:** a row selected for this repair because its Status begins
  `taken`, in the loop record, a released loop block or a phase-6 table.
- **Fixed line:** `<ID>: fixed — tests/<path>::<function>` or
  `<ID>: fixed — not a test — <reason>`, with the existing leading bullet,
  bold and backtick handling retained.
- **Finding-shaped identifier:** a complete `L<digits>-<digits>` identifier,
  or ASCII letters, a hyphen and digits whose letters are the prefix of a row
  id in the change's loop record or findings tables, such as `F-12` where
  phase-6 rows are `F-<n>` (loop round 1, row L1-3); the letters `L` count
  only when the change has a loop row (loop round 3, row L3-3).
- **Claimed fix:** a colon line whose right side is a fixed status
  (`fixed — …`), whatever the shape of its left side (loop round 3, row L3-1).
- **Legacy completion marker:** `; fixed by`, `; fixed:` or `; repaired by` within a Status
  beginning `taken — …`, compared without regard to case; a marker inside a
  backtick span is quoted text, not a marker (phase 6, row F-6).

## Acceptance criteria

1. When an otherwise valid repair answer includes lines with no colon or
   colon lines whose left side is neither an active identifier nor a
   finding-shaped identifier, those lines do not fail the attempt.
   *Refuted by:* a heading, fence, report label or closing `Resume:` causes
   a retry or a format diagnostic despite all required fixed lines being valid,
   or a line such as `ADR-0017: …` or `UTF-8: …` does, when no row id uses
   that prefix.
2. When a colon line names an active row exactly, it is checked as that row's
   fixed line regardless of whether the identifier has the usual finding shape.
   *Refuted by:* a phase-6 row named `custom` or `expected` is ignored or
   reported missing despite a valid fixed line for that identifier.
3. When a colon line names a finding-shaped identifier absent from the active
   rows, or is a claimed fix whose identifier names no active row, the attempt
   fails with `<ID>: no taken row carries this id`.
   *Refuted by:* an extra `L9-9:` or `F-999:` is ignored and checkpointed, or
   `custm: fixed — tests/…::test_…` beside a valid `custom:` line is.
4. When an active row has zero or multiple answer entries, the attempt fails
   with that identifier and `no fixed line` or `several fixed lines`, respectively.
   *Refuted by:* prose alone succeeds or duplicated entries are accepted.
5. When an active identifier's colon line has a malformed fixed status, the
   attempt fails with a diagnostic naming the identifier.
   *Refuted by:* `L1-1: done` or `L1-1: fixed — not a test` without a reason
   is discarded as prose or accepted as a repair.
6. When completed rows carry canonical `fixed — …` statuses, they are excluded
   from subsequent repair targets in all three row locations.
   *Refuted by:* a fixed row is sent to a model or needs another fixed line;
   a batch containing only completed rows starts a model call.
7. When any active row carries a legacy completion marker, repair refuses
   before a model call or `make verify`, naming the row and both canonical
   fixed-status forms without rewriting the row.
   *Refuted by:* any unquoted marker in any row location reaches an attempt,
   including one beside a backtick span, is silently skipped, or yields a
   refusal without the corrective form; or a marker quoted inside a backtick
   span refuses the repair.
8. When a fixed line survives identifier filtering, the existing test-reference,
   code-row eligibility and red-first proof requirements continue to apply.
   *Refuted by:* an undefined or escaping test reference, a code row answered
   `not a test`, or a test green on baseline code is accepted.
9. When repair instructions are read, the shared answer prompt states the
   prose-filter and legacy-status rules, and the workflow's repair section
   states the canonical hand-repair statuses and the orchestrator's test mark
   for loop rows.
   *Refuted by:* the prompt still forbids all incidental prose, or the workflow
   leaves a hand repair in a `taken` status or omits its `Broke a test` mark.

## Non-goals

- Migrate historical completed findings in other change folders.
- Add a status vocabulary, or infer completion from arbitrary prose.
- Change model routes, retries, review ownership, test-proof rules or gates.
- Redesign other answer parsers or phase-6 identifier conventions.
- Write phase-2b design or an ADR: this remains a bounded correction using
  the existing status and repair architecture.

## Protected areas

Other change folders and all ADRs remain untouched because their records are
historical evidence or decisions outside this fix. Tracker data, endpoint
configuration, permissions and gate definitions are outside the parser fix.

## Definition of Done

- `make verify` is green, with parser and pre-call refusal regression evidence.
- `docs/WORKFLOW.md` and `scripts/stage2.py`'s shared answer instructions move
  with the implementation; no ADR changes.
- The pull request's file list shows the protected areas untouched and the
  non-goals unbuilt.
- The pull request closes the repair parsing work item and its last commit
  carries `Closes-Bead: coding-harness-ugi`.
- Special live-model runs: none; deterministic runner stand-ins suffice.

## Open decisions

None open. The interview's reasoned skip and three recorded details stand.

- [DETAIL] Preserve exact active-identifier matching before applying the
  finding-shape filter: phase-6 identifiers are free text, so shape alone
  cannot identify every real fixed line.
- [DETAIL] Use case-insensitive detection of the three recorded legacy markers,
  matching the existing case-insensitive Status handling; require the
  semicolon marker rather than any mention of a fix in a reason.
- [DETAIL] Set a one-hour phase-4 appetite, repairs included, because the work
  is confined to two parser checks, regression coverage and matching doctrine;
  stop at the limit rather than widening scope.
