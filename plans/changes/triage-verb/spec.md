---
title: "Spec — triage-verb"
status: draft
implementation_status: partial
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-o2s1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, triage]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — triage-verb

Let the orchestrator record an already-made loop-row decision through a local
runner command without damaging its table (bead coding-harness-o2s1).
Research: `research.md`. Maintainer answer: `decisions.md#Q-1`.

## Problem

As recorded on 2026-11-07, the runner has no triage verb, although repair
requires the orchestrator to decide rows first (`research.md`, "What exists
today"). Manual edits have shifted table cells and sent test-only findings
into ordinary red-first repairs; the interview records failed repairs caused
by the missing `not a test` prefix (`decisions.md#Q-1`). The runner already
has row readers, a per-record lock and atomic replacement; this change adds
a safe entry point to that existing record, not a new decision maker.

## Terms

- **Active record:** the change and worktree's private `loop.md`, before release.
- **Test-only location:** a row whose `Where` cell identifies only repository
  file locations below `tests/`; line numbers and Markdown quoting do not
  change the classification. Prose without identifiable file locations or
  a mixture with production locations is not proof of test-only work.
- **Decision:** an orchestrator-supplied status and reason, not repair evidence.

## Acceptance criteria

1. When the orchestrator runs `python3 scripts/stage2.py triage <change> '<row>=<status>' '<reason>'` for one uniquely identified active loop row with a valid decision, the command records that decision and exits 0.
   *Refuted by:* the command is unavailable, targets another row/worktree, or refuses a valid request.
   *Basis:* `decisions.md#Q-1`; `research.md`, "The change itself" and the existing loop-record location.

2. When a decision is recorded, only the named row's `Status` cell changes, with a reason containing a literal or already escaped pipe remaining one cell.
   *Refuted by:* another cell, line, reviewer quotation, state snapshot or final newline changes, or parsing the result shifts `Broke a test` into another column.
   *Basis:* `research.md`, the fixed row shape and evidence ownership.

3. When an ordinary `taken` decision targets a test-only location, the command refuses without writing and suggests `taken — not a test — <reason>`.
   *Refuted by:* it writes the ordinary status, only warns, omits the correction, or refuses the explicitly supplied `taken — not a test` form for that reason.
   *Basis:* `decisions.md#Q-1`.

4. If the request has invalid syntax, an empty or multiline reason, an unsupported status, an invalid change name, no readable active record, a malformed row, a missing or repeated target ID, or a target already marked `fixed`, it fails with a cause-specific diagnostic and leaves the record unchanged.
   *Refuted by:* partial mutation, creation of a missing record, silent success or a diagnostic that does not identify the problem.
   *Basis:* `research.md`, row preservation and the existing refusal contract; reversible input restrictions below.

5. While another runner owns the record, triage refuses; if replacement fails before publication, the prior record remains intact and the command reports failure.
   *Refuted by:* a locked record is edited, a competing append is lost, a failed write truncates the record, or a failed write reports success.
   *Basis:* the existing loop ownership and atomic-write contracts read on 2026-11-07 at `ae3402c2` (`scripts/stage2.py`, `holding_record`, `replace_record`).

6. When triage runs, it requires neither a model call nor model credentials and changes no repository file, git state, repair proof or review verdict.
   *Refuted by:* it launches a model, demands endpoint setup or a clean tree, commits, edits `findings.md`, fills `Broke a test`, or starts repair/review/release.
   *Basis:* `decisions.md#Q-1`, orchestrator-supplied command; `research.md`, the division of authority.

7. When the orchestrator explicitly supplies `taken — guard test` with a nonempty unquoted reason, the recorded status retains the existing guard authorisation while repair, clean-round and release rules retain their current meaning.
   *Refuted by:* an ordinary/quoted reason silently gains guard authority, an authorised guard is rewritten as `not a test`, or triage makes a taken row clean or invents proof marks.
   *Basis:* `research.md`, guard authorisation and the existing accepted/clean-round rules; ADR 0023 remains unchanged.

8. When the orchestrator reads command help and the review-loop instructions, both show how to record a decision and explain the test-only refusal and unchanged ownership of proof marks.
   *Refuted by:* the documented example is rejected by the parser, the refusal is undocumented, or the instructions imply triage supplies repair evidence.
   *Basis:* `research.md`, "The step-by-step triage procedure"; `decisions.md#Q-1`.

## Non-goals

- Model-assisted judgment, deciding whether a finding is true, or automated
  recognition of the future repair's files from arbitrary finding prose.
- Batch updates, fixed-status/proof entry, released blocks, phase-6 tables,
  record recovery or repair of already damaged tables.
- Changes to model routing, review membership, counters, status vocabulary,
  guard-proof rules, escalation rules or the maintainer's decision authority.
- Design phase 2b and an ADR: the recorded class is bounded; the existing
  runner, row schema and authority boundaries remain in place.

## Protected areas

Model declarations, gate definitions, provenance rules, tracker data,
accepted ADRs and other change folders are outside this change. Existing
review findings and proof evidence are preserved. The orchestrator alone
applies the planned update to `prompts/04b-review-loop.md` after the accepted
implementation attempt; implementation attempts never edit held paths.

## Boundary

Maintainer, 2026-11-10, after the fifth finding of the location mechanism
(P6-2, P6-4, P6-5, P6-7, P6-8): triage does not guess what a `Where` cell
means. A token names a repository location only in one of these spellings:
a tracked path; that path followed by `:<line>` or `:<line>-<line>` (hyphen
or en dash); that path followed by `#L<line>` or `#L<line>-L<line>`; or a
Markdown link whose target is one of these. The part before the suffix must
equal a tracked path exactly; a prefix of a longer name never counts. A token
that looks like a path (it contains `/` or a file extension) and matches none
of these spellings makes triage refuse without writing and name the token, so
the row's location is corrected by hand first. Plain prose words and external
URLs are not locations. Free-text locations end with the structured finding
record (bead coding-harness-k7tv), which is separate work.

## Definition of Done

- `make verify` green with command tests demonstrating each refusal's fault.
- Updated together: `scripts/stage2.py`, `tests/test_stage2.py`,
  `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, and this change's plan/spec
  bookkeeping; the runner regenerates `plans/INDEX.md`.
- Protected areas untouched and non-goals unbuilt, checked from the PR diff.
- The PR closes coding-harness-o2s1 (triage verb), with the final commit
  trailer `Closes-Bead: coding-harness-o2s1`.
- Special live-model runs: none; tests use isolated records and fake launchers.

## Open decisions

None open. The maintainer's Q-1 answer stands unchanged.

- [DETAIL] Accept one row per invocation and these status operands: `taken`,
  `rejected`, `taken — not a test`, `taken — guard test`; append ` — <reason>`
  once. This matches the interview's command shape without a batch grammar.
- [DETAIL] Refuse edits to `fixed` rows, preserve existing proof marks and
  reject reasons with line breaks. Triage records intent; correcting finished
  repair evidence remains the existing orchestrator procedure.
- [DETAIL] Use the explicit test-only location as the mechanical refusal
  trigger; inspect path locations, not keywords like "test" in prose. Mixed
  or unspecified locations remain the orchestrator's judgment. This is a
  visible limit: triage cannot establish what a later repair will touch.
- [DETAIL] Preserve the established explicit guard exception even for
  test-only locations; this command introduces no replacement for ADR 0023.
- [DETAIL] Two hours is the implementation stop, including repair rounds;
  it bounds a local command reusing the record machinery.
