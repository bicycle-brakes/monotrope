---
title: "Spec — repair-scope-guard"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-25
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

The runner prevents repair attempts from committing new files outside their scope and reserves journal files for the orchestrator (bead coding-harness-t83). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- A repair wrote its own handover into the branch on 2026-10-15; the orchestrator removed it. The repair prompt did not prohibit journal files (`decisions.md`, interview skip).
- On 2026-11-21 the repair check did not compare new paths with the taken findings; a passing attempt could commit unrelated, non-held files (`research.md`, re-verification). Since that research, the orchestrator has reserved `docs/journal/` in the runner and synchronized the plan prompt (commit `f1fc1836`).

## Terms

**Repair scope:** descendants of the current change folder and `tests/`, plus paths named in the selected taken rows' Where cells, frozen before the attempt. A named file grants that file alone, whether or not it is tracked yet. A directory grants its descendants only when the cell writes it with a trailing `/`; a bare word that merely names a tracked directory grants nothing. The plan does not grant paths. Existing held-path restrictions take precedence.

**Where path:** a path-like token, or Markdown link text or target, in a taken Where cell. A trailing `:line`, `:line-line`, `#L<line>` or `#L<line>-L<line>` selector is removed. The cell is read only through the shared Where classifier; nothing is refused. A bare file name resolves against the change folder first, then the repository root; paths cannot escape the repository. Prose without a path grants nothing.

**New file:** a file absent from the pre-attempt baseline and present right after the attempt's call, before the runner's own checks write anything and judged by the ignore rules the attempt started under, including a non-ignored untracked file, an indexed addition, and a rename destination. Untracked ignored files do not count, including test and tool caches; an explicitly indexed ignored addition does count.

## Acceptance criteria

1. When a Stage-2 writing attempt changes a tracked or non-ignored journal path, the held-path rule refuses and restores it before a checkpoint commit.
   *Refuted by:* a writing attempt commits or leaves such a journal edit or addition, including a case-variant held prefix.
2. When either repair prompt is assembled, it states in words the scope of the change folder, `tests/` and paths named by taken Where cells, and prohibits handover and journal writes and new files outside that scope.
   *Refuted by:* either command-tools or file-tools prompt omits the rule or a prohibition.
3. When a repair leaves a new file outside its scope at the checkpoint, the runner refuses the attempt and names every such path in the checkpoint refusal text.
   *Refuted by:* an out-of-scope non-ignored untracked file, indexed addition or rename destination is committed or absent from the refusal text.
4. When a repair leaves a non-held new file within its scope at the checkpoint, this scope guard permits it.
   *Refuted by:* this guard rejects a file in the change folder, `tests/`, a named file or a named directory's descendants.
5. When a repair edits an existing tracked file outside its scope, this new-file guard does not reject that edit.
   *Refuted by:* an otherwise permitted existing tracked edit is rejected solely for its path.
6. When the new-file guard refuses a repair, the runner follows the held-path checkpoint refusal path: it saves the attempt under a local attempt ref, restores the baseline and pre-call findings, reports the refusal with the saved-attempt location, and stops the run without trying another route.
   *Refuted by:* the attempt is committed, another route starts in that run, an attempt edit remains, pre-call findings are lost, or the refusal omits the offending paths or saved-attempt location, provided saving and safe restoration succeed.
7. When an attempt changes its plan or finding rows, those edits do not enlarge the scope used to judge that attempt.
   *Refuted by:* a path introduced only by attempt-written plan or finding text permits an otherwise out-of-scope new file.
8. When a taken Where cell names paths, the scope follows the Where path rules above.
   *Refuted by:* line selectors, Markdown link text or target, bare names, directories, prose or an escaping path produce a different scope from those rules.
9. When a repair leaves only an untracked ignored file outside the scope, this new-file guard does not refuse it.
   *Refuted by:* an ignored cache or other ignored untracked file alone triggers this guard, or an explicitly indexed ignored addition escapes criterion 3.

## Non-goals

- Restrict edits to existing tracked files beyond existing guards, or change the change-folder exemption and lifecycle protection.
- Guard an orchestrator's hand repairs, change row selection or model routing, or change the repair's existing test and review requirements.
- Use the plan as a source of repair scope, or protect arbitrary ignored files with this new-file guard.
- Change the committed provenance map or create or amend an architecture decision record.

## Boundary

- The new-file inventory reads git's implicit global excludes file (`$XDG_CONFIG_HOME/git/ignore`, used when `core.excludesFile` is not set) as it stands when the inventory runs; it does not freeze that file. An attempt that edits a `.gitignore` so that a cache only the implicit global file ignores reads as a new file can therefore be refused as out of scope. This is an accepted limit (maintainer, 2026-11-24; phase-6 row P6-1 of that day); phase 6 rejects a row that describes only this case.

## Protected areas

The customer instance remains out of bounds. Human-decided paths and the existing held paths retain their protections; `docs/journal/` is held for the orchestrator.

## Definition of Done

- `make verify` green, with the new regression tests and existing failure and restoration tests passing.
- The runner, its tests and `docs/WORKFLOW.md` move together; the orchestrator already updated the runner's journal-held list and the matching `prompts/03-plan.md` line together before implementation (commit `f1fc1836`), because the prompt is held.
- Protected areas stay protected and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes the repair scope guard work item (bead coding-harness-t83), and its last commit carries `Closes-Bead: coding-harness-t83`.
- Special runs: none.

## Open decisions

- [DETAIL] Freeze scope from selected rows before the attempt; do not read permissions from the plan. This prevents attempt-written text and a plan's exclusions from authorizing files.
- [DETAIL] Apply the shared Where-path interpretation recorded in spec-review S-4; this keeps the repair guard aligned with held-row routing.
- [DETAIL] Use the held-path refusal boundary and exclude untracked ignored files as recorded in spec-review S-1, S-2 and S-6; this restores refused work without treating ordinary caches as stray files.
- [DETAIL] Use a four-hour phase-4 stop, repairs included: the runner, prompt and failure-path tests are a bounded change.
