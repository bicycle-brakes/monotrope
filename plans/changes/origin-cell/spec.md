---
title: "Spec — origin-cell"
status: draft
implementation_status: partial
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-ywbh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, repair-brake]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — origin-cell

The orchestrator supplies the finding provenance on which the repair brake
depends, and the runner refuses accepted findings with invalid provenance
(bead coding-harness-ywbh — make the repair brake's Origin cell reliable).
Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

At baseline `ec375553` (2026-11-07), reviewers supply Origin verbatim without
being told its vocabulary; the orchestrator instructions mention only Status
and Broke a test. The runner accepts arbitrary Origin values, although the
brake tests simulate an orchestrator writing valid ones. The existing brake
therefore depends on an undocumented action with no enforcing check
(`research.md`, “Where Origin content comes from today” and “The brake”).

The maintainer assigned Origin to the orchestrator and required refusal of
invalid taken rows, without prompt changes (`decisions.md#Q-1`). This fixes
the missing precondition of the existing brake; it does not replace its rule.

## Terms

- **Accepted row:** a row whose Status starts with `taken` or `fixed`, using
  the runner's existing case-insensitive status handling; repairing a finding
  does not erase its acceptance.
- **Valid Origin:** after the existing cell whitespace trimming, exactly
  `base` or `fix-r<N>`, where N is a positive decimal integer without leading
  zeroes. Spelling is lowercase and the complete cell must match.
- **Origin ownership:** the orchestrator sets `base` for a finding not caused
  by a repair, or `fix-r<N>` for a finding caused by repair round N, when it
  decides the row. Reviewer text alone is not a decision about provenance.
- **Authoritative rows:** the selected change's own loop-record rows,
  released loop rows and phase-6 finding rows, as recognized by the existing
  parsers; quoted reviewer answers and example tables are not extra rows.

## Acceptance criteria

1. When the workflow describes deciding a finding, it assigns Origin to the
   orchestrator and explains the two allowed values by their causal meaning.
   *Refuted by:* the row-decision instructions omit Origin, assign it to a
   reviewer, or fail to distinguish an existing defect from a repair defect.
   *Basis:* decisions.md#Q-1.

2. If any authoritative accepted row has an invalid Origin, `review-loop`,
   `review`, ordinary `release-loop` and `repair` refuse before a model call,
   stage consumption, findings rewrite or loop-record deletion.
   *Refuted by:* an empty, unknown or malformed Origin in any of the three
   row locations permits one of those effects, including on release retry.
   *Basis:* decisions.md#Q-1.

3. When an invalid Origin causes refusal, the diagnostic identifies each
   offending row and its location and tells the orchestrator to supply
   `base` or `fix-r<N>` with positive N.
   *Refuted by:* the refusal hides the offending identifier or location,
   omits the allowed values, or asks the reviewer to repair provenance.
   *Basis:* decisions.md#Q-1.

4. While accepted rows carry valid Origins, Origin validation admits those
   rows without changing the existing status, evidence or other preconditions.
   *Refuted by:* `base`, `fix-r1` or `fix-r12` is rejected as an Origin, or
   supplying it bypasses an existing undecided-row or test-evidence refusal.
   *Basis:* decisions.md#Q-1.

5. When a row is rejected or not yet decided, its Origin alone does not
   cause refusal.
   *Refuted by:* a rejected row needs provenance to release, or newly received
   reviewer rows are refused before the orchestrator can decide them; existing
   undecided-row checks still apply to continuation.
   *Basis:* decisions.md#Q-1.

6. When reviewers return findings, the runner leaves their Origin text
   available for the orchestrator's decision without inventing a valid Origin.
   *Refuted by:* intake defaults an empty or arbitrary reviewer Origin to
   `base` or `fix-r<N>`, or rewrites the retained reviewer answer.
   *Basis:* decisions.md#Q-1.

7. When repair or release processes a valid accepted row, its Origin is
   preserved.
   *Refuted by:* marking a row fixed, releasing it or reconciling a repeated
   release erases or replaces the orchestrator's Origin.
   *Basis:* decisions.md#Q-1.

8. When two consecutive rounds contain accepted findings all attributed to
   repairs, the existing repair brake stops continuation across record and
   released history alike.
   *Refuted by:* release or a transition from taken to fixed permits another
   round, or an accepted `base` row in either round fails to quiet this brake;
   rejected rows do not count as accepted findings.
   *Basis:* decisions.md#Q-1; research.md, “The brake”.

## Non-goals

- No reviewer prompt changes, including embedded runner answer instructions.
- No automatic inference or historical backfill of provenance, and no proof
  that an orchestrator's causal attribution is true.
- No new repair-brake threshold, restart policy, round numbering, stage
  selection, repair route, status grammar or finding-selection rule.
- No new recovery command, schema or migration of other changes' findings.
- No design or ADR: this bounded correction enforces an existing decision
  within the current row and command boundaries.

## Protected areas

- `prompts/`, `templates/` and runner prompt constants: the maintainer
  explicitly excluded prompt changes; the findings template already defines
  Origin values.
- `docs/adr/`, `decisions/`, `provenance.yaml`, `model-endpoints.yaml`,
  `AGENTS.md`, harness settings and tracker data: no new governance, access
  policy or architecture is part of this correction.
- Other change folders: legacy data is not silently rewritten to pass the check.

## Definition of Done

- `make verify` is green, including refusal, preservation and brake regressions.
- Documentation moved with the code: the row-decision paragraph of
  `docs/WORKFLOW.md` and this change's spec and plan; no ADR is due.
- The pull request's file list demonstrates the protected areas untouched
  and non-goals unbuilt.
- The pull request closes coding-harness-ywbh (repair-brake Origin ownership);
  its last commit carries `Closes-Bead: coding-harness-ywbh`.
- Special runs: none; command tests use local model stand-ins.

## Open decisions

None open. The maintainer's answer remains unchanged in `decisions.md#Q-1`.
The following reversible execution details are explicit agent choices.

- [DETAIL] Apply the check to taken and fixed rows of the selected change's
  loop record and phase-6 table. A released row is checked once, by the
  ordinary `release-loop` before it writes the block; already released history
  is not re-checked, so legacy rows released before this change (for example
  in attempt-diagnostics and malformed-answer-retry) never block a verb, and no
  history is backfilled (loop row L1-4, 2026-11-08). Other changes are not
  scanned.
- [DETAIL] Require canonical lowercase whole-cell values and positive decimal
  repair numbers without leading zeroes. This matches the existing `fix-r`
  comparison and round spelling without silently normalizing provenance.
  Reject `fix-r`, `fix-r0`, `fix-r01`, `fix-r-1`, `fix-r1x`, `FIX-R1` and
  `BASE`; ordinary surrounding cell whitespace remains harmless.
- [DETAIL] Validate vocabulary, not causality or chronology: no new rule
  compares N to the finding's round, especially when history spans releases.
- [DETAIL] Keep validation at the four action boundaries, before their
  effects, rather than making the shared parsers reject undecided reviewer
  text or changing restart/stage-retirement behavior.
- [DETAIL] Set a two-hour phase-4 stop, repairs included; the interview set
  no appetite and this bounds the runner, regression and documentation work.
