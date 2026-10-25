---
title: "Spec — review-loop-row-ids"
status: draft
implementation_status: partial
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-6jg
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, review-loop]
class: bounded
appetite: 2
adr_files: []
---

# Spec — review-loop-row-ids

A review-loop round refuses an unreadable finding table instead of treating
it as a failed reviewer whose missing findings can certify a clean round
(bead coding-harness-6jg). Sources: `research.md` and the maintainer's
refusal decision in `decisions.md`.

## Problem

- The original identifier loss is already fixed: the runner assigns valid
  rows its own identifiers, regardless of the reviewer's first cell
  (`research.md`, exploration at `105c270`, 2026-10-20).
- A member with no readable row becomes a generic failed member. Beside
  another member's `No finding.`, its unreadable table can therefore end
  the loop as clean; the generic diagnostic omits the unreadable lines
  (`research.md`, same exploration; confirmed at `82488fc`).
- The paid swarm can replace that malformed member, hiding the answer the
  maintainer chose to have refused. The accepted replacement rule names
  nonzero exits, timeouts and empty answers, rather than malformed tables
  (`research.md`, open gap; resolved in its dated appendix).

## Terms

- **Readable row:** a finding accepted by the existing six-cell parser,
  including its existing handling of pipes within the finding cell.
- **Malformed table answer:** an answer with no readable row and at least
  one table-shaped line retained as non-row text by that parser; table
  headings and separator lines alone do not qualify.
- **Refused attempt:** a nonzero review-loop result that completes no round;
  call audit lines remain evidence of calls already made.

## Acceptance criteria

1. When any member returns a malformed table answer, the review-loop attempt
   fails in the free swarm, paid swarm or single paid rung, regardless of
   other members' readable rows or explicit `No finding.` answers.
   *Refuted by:* any such combination returns success or completes a round.
2. When an attempt fails for malformed table answers, its diagnostic names
   every affected member and reproduces every offending non-row table line
   with its original identifier, subject to existing credential scrubbing.
   *Refuted by:* a member or offending line is omitted, an identifier is
   rewritten, or a fixture credential appears unsanitized.
3. When malformed table output refuses an attempt, completed-round state
   remains unchanged, including round headings and consumed stages.
   *Refuted by:* a fresh attempt creates a loop record or an existing or
   released snapshot gains a round or consumed stage; call audit lines are
   allowed and do not constitute completion.
4. When a refused attempt is rerun with readable answers under otherwise
   unchanged inputs, it attempts the same stage and round number.
   *Refuted by:* the rerun advances the ladder, skips the stage, increments
   the round number or stops because the failed attempt was called clean.
5. When a paid-swarm batch or its current replacement returns a malformed
   table answer, no further replacement call starts for that attempt.
   *Refuted by:* a malformed initial member is replaced, another failed
   initial member triggers replacement despite that malformed answer, or a
   malformed replacement triggers the next replacement.
6. When members return readable rows with arbitrary reviewer identifiers,
   the completed round retains every row under one unique runner-assigned
   identifier series and attributes each row to its actual reviewer.
   *Refuted by:* a valid `R2-1` or other reviewer identifier causes refusal,
   a row disappears, identifiers collide or reviewer attribution changes.
7. When members fail through a timeout, nonzero exit or empty answer without
   a malformed table answer, the existing partial-swarm and paid-replacement
   behavior remains available.
   *Refuted by:* these failures alone cause the new whole-round refusal,
   erase successful members' rows or prevent an eligible paid replacement.

## Non-goals

- Rejecting or repairing reviewer identifiers on otherwise readable rows.
- Changing the shared row parser, accepted finding-cell pipes or table
  furniture handling; responses containing both readable rows and non-row
  text keep their existing treatment.
- Expanding the new refusal to arbitrary prose, header-only tables or
  other existing unsuccessful-review responses.
- Migrating old records or retroactively reopening completed clean rounds.
- Changing clean-round decisions, model admission, stage ordering, probe
  receipts, call isolation, repair, release or credential-scrubbing rules.

The bounded class does not run phase 2b; no design or ADR draft is due.

## Protected areas

- `docs/adr/`, `decisions/`, `model-endpoints.yaml`, `AGENTS.md` and model
  launch/isolation configuration: this is an output-handling correction.
- Other change folders and historical findings: existing evidence is not
  rewritten to describe the corrected behavior.
- Tracker data: status changes belong to the orchestrating session.

## Definition of Done

- `make verify` is green after implementation and any repair.
- Regression tests demonstrate criteria 1–7, with failing-before-fix
  evidence for the new refusal; the criterion ledger names their tests.
- Documents changed with the implementation: this change's `spec.md` and
  `plan.md` for status, ledger and measured time; `findings.md` for runner
  audit/review evidence. No living capability spec or ADR changes are due.
- The pull request's file list shows protected areas untouched and
  non-goals unbuilt; it closes the malformed-output work item and its last
  commit carries `Closes-Bead: coding-harness-6jg`.
- Special live-model runs: none; deterministic reviewer fixtures hold this
  output-handling contract without foreign calls.

## Open decisions

None open. The maintainer's refusal answer is recorded in `decisions.md`;
this draft neither supplies a new answer nor records an ADR answer.

- [DETAIL] Apply refusal to a table answer with no readable row, following
  the recorded interpretation; mixed readable/non-row output stays outside
  scope to avoid broadening the settled bounded correction.
- [DETAIL] Refuse before round persistence rather than changing the meaning
  of a completed clean round; an unreadable answer completes no round.
- [DETAIL] A malformed paid answer refuses immediately after its current
  batch is collected, because the accepted replacement rule covers call
  failures, not unreadable findings (research appendix, 2026-10-20).
- [DETAIL] Set a two-hour phase-4 appetite, repairs included, as a stop for
  this localized correction and its regression matrix; no earlier appetite
  is recorded in the interview or research.
