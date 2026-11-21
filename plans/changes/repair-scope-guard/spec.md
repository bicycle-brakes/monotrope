---
title: "Spec — repair-scope-guard"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, repair, stage2-runner]
class: bounded
appetite: 4
adr_files: []
---

# Spec — repair-scope-guard

The runner prevents repair attempts from keeping new files outside their stated scope and reserves journal files for the orchestrator (bead coding-harness-t83). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- A repair wrote its own handover into the branch on 2026-10-15; the orchestrator removed it. The repair prompt does not prohibit journal files (`decisions.md`, interview skip).
- On 2026-11-21 the runner's held-path check did not reserve `docs/journal/`, and its repair checks did not compare new paths with the taken findings or plan. A passing attempt could commit unrelated, non-held files (`research.md`, re-verification).

## Terms

**Repair scope:** the current change folder, `tests/`, and the individual paths named in a taken row's Where cell or the accepted plan. An individual path does not grant its siblings.

**New file:** a file absent before the attempt and present afterwards, including an untracked, ignored or staged addition and a rename destination. Existing tracked files are not new files.

## Acceptance criteria

1. When any Stage-2 writing attempt changes a file under `docs/journal/`, the existing held-path rule refuses and restores the attempt before a checkpoint commit.
   *Refuted by:* an attempt commits a journal edit or addition, including a case-variant held prefix.
2. When a repair prompt is assembled for either command tools or file tools, it states the repair scope and tells the attempt not to write handovers or journal files and not to create files outside that scope.
   *Refuted by:* either prompt omits the scope or either prohibition.
3. When a repair creates a new file outside the repair scope, the post-run check refuses the attempt and names every such path.
   *Refuted by:* an untracked, ignored, staged or renamed out-of-scope new file is accepted or omitted from the diagnostic.
4. When a repair creates a non-held new file within the repair scope, this scope guard permits it.
   *Refuted by:* a new file in the change folder, `tests/`, a taken Where path or an accepted-plan path is rejected by this guard.
5. When a repair edits an existing tracked file outside the repair scope, this new-file guard does not reject that edit.
   *Refuted by:* an otherwise permitted existing tracked edit is rejected solely for its path.
6. When a repair attempt is refused by the new-file guard, its changes are restored to the pre-attempt baseline using the existing failure handling, and its diagnostic is retained.
   *Refuted by:* an out-of-scope addition or another attempt edit remains, a pre-existing kept finding is lost, or the failure record lacks the diagnostic.
7. When a repair attempt changes the plan or finding rows, its own edits cannot enlarge the scope used to judge that attempt.
   *Refuted by:* the attempt adds an out-of-scope path to its plan or a row and the guard then accepts that new file.

## Non-goals

- Restrict edits to existing tracked files beyond existing guards, or change the change-folder exemption and lifecycle protection.
- Guard an orchestrator's hand repairs, change row selection or model routing, or change the repair's existing test and review requirements.
- Change the committed provenance map or create or amend an architecture decision record.

## Protected areas

The customer instance remains out of bounds. Human-decided paths and the existing held paths retain their protections; `docs/journal/` joins the latter.

## Definition of Done

- `make verify` green, with the new regression tests and the runner's existing failure and restoration tests passing.
- The runner, its tests, `docs/WORKFLOW.md`, and the held-path list in `prompts/03-plan.md` move together in the pull request.
- Protected areas stay protected and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes the repair scope guard work item (bead coding-harness-t83), and its last commit carries `Closes-Bead: coding-harness-t83`.
- Special runs: none.

## Open decisions

- [DETAIL] Compare scope with the accepted plan and selected rows captured before the attempt: attempt-written text cannot authorize itself, and this preserves retry consistency.
- [DETAIL] Treat a rename destination as a new file and include ignored additions in the check: both can introduce the same stray file as an ordinary untracked addition.
- [DETAIL] Use a four-hour phase-4 stop, repairs included: the runner, prompt, and failure-path tests are a bounded change.
