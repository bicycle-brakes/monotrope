---
title: "Spec — review-verdict-validated"
status: draft
implementation_status: none
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-5mx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, phase-6]
class: bounded
appetite: 2
adr_files: []
---

# Spec — review-verdict-validated

The goal is to count a phase-6 review as completed only when its answer
contains findings or explicitly reports no finding, retaining unsuccessful
answers as evidence without releasing the loop record (bead
`coding-harness-5mx` — validate the phase-6 verdict). Research: `research.md`.
Decisions: `decisions.md`.

## Problem

The runner audit at `378879a` (2026-10-21) reproduced exit 0, a completion
note and deletion of the external loop record for empty, context-refusal
and malformed-table answers. Research at `7586f1a7` (2026-10-24) identifies
the cause: `review` parses the answer but unconditionally appends a verdict
and calls `release`, unlike the loop's own answer validation.

## Terms

- **Valid answer:** at least one six-cell finding row recognized by the
  existing parser, or exactly `No finding.` after trimming surrounding
  whitespace, as the runner's answer instructions require.
- **Invalid answer:** neither form above; this includes empty or whitespace
  output, refusal prose, header-only or unreadable tables, and `No finding.`
  accompanied by other prose when there is no finding row.
- **Verdict state:** authoritative phase-6 blocks and verdict lines in
  `findings.md`; call audit and explicitly rejected evidence are separate.

## Acceptance criteria

1. When `stage2.py review` receives an invalid answer from a successful model
   call, the command exits non-zero.
   *Refuted by:* any empty, refused or malformed answer returning exit 0.
2. When an invalid answer is rejected, the attempt leaves verdict state
   unchanged and reports no successful verdict completion.
   *Refuted by:* a new authoritative phase-6 block, a new verdict line, a
   changed earlier verdict, or the usual verdict-appended success message.
3. When an invalid answer is rejected, the attempt does not advance the
   loop-release workflow.
   *Refuted by:* releasing loop rows, changing or deleting any existing
   external loop-record file, or starting the loop-marks model call; an
   earlier genuine verdict does not permit these effects for this attempt.
4. When an invalid answer is rejected, its content remains inspectable as
   rejected evidence that later runner operations cannot interpret as a
   verdict or accepted findings.
   *Refuted by:* missing nonempty answer content, no explicit empty-answer
   record, or embedded verdict lines, headings or table rows authorizing
   release, becoming accepted findings or changing later session selection.
5. When the answer contains a recognized six-cell finding row, the review
   retains its existing successful verdict, release and loop-marks behavior.
   *Refuted by:* rejecting a valid table, losing a finding or its attribution,
   releasing before the verdict, or failing to resume its thread for marks.
6. When the answer is exactly `No finding.` apart from surrounding
   whitespace, the review retains its existing successful no-finding verdict
   and subsequent release behavior.
   *Refuted by:* rejecting that answer, omitting its verdict line or retaining
   an otherwise releasable loop record after a successful review.

## Non-goals

- Redefining finding-row parsing, severity or dimension validation, or the
  treatment of malformed rows beside a recognized row.
- Changing model routing, prompts, review-session policy, loop stages,
  release locking or the manual `release-loop` contract.
- Retrofitting or deleting historical verdicts, adding automatic review
  retries, or changing loop-marks failure handling.
- Design phase 2b and an ADR: this is a bounded repair of the existing
  verdict boundary, so neither is required.

## Protected areas

Prompts, workflow doctrine, ADRs, governance and model configuration stay
unchanged because their contracts already supply the intended answer form.
Other runner verbs and the shared parser retain their behavior.

## Definition of Done

- `make verify` green, including regression tests without live model calls.
- Documents moved with the repair: this change's `spec.md`, `plan.md` and
  runner-maintained `findings.md`; generated `plans/INDEX.md` follows them.
- The pull request's file list demonstrates the protected areas and
  non-goals remain untouched.
- The pull request closes the phase-6 verdict-validation task and its last
  commit carries `Closes-Bead: coding-harness-5mx`.
- Special runs: none; no real model call is needed to prove this repair.

## Open decisions

None open. The interview's reasoned skip fixes the bounded scope.

- [DETAIL] Use an explicitly rejected, quoted evidence block in `findings.md`
  outside authoritative phase-6 blocks; this reuses the existing evidence
  file while keeping reviewer words inert.
- [DETAIL] Preserve existing row recognition and trim only surrounding
  whitespace for `No finding.`; this repairs the missing validation without
  changing the shared parser's contract.
- [DETAIL] Set the phase-4 appetite to two hours including repairs, a stop
  boundary proportionate to one local guard and its regression cases.
