---
title: "Spec — archive-closed-changes"
category: spec
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-cqun
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, archive, plans-registry]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — archive-closed-changes

Archive completed change folders through a repeatable local command, apply it
once to the measured backlog, and include it in the post-merge procedure
(bead coding-harness-cqun — archive closed changes). Research: `research.md`.
Authority: the maintainer's answered `decisions.md#Q-1` and its recorded details.

## Problem

- The lifecycle requires completed changes to leave the active tree, but no
  archive command exists; the existing archive was maintained manually
  (`research.md`, "What exists today", explored 2026-11-06).
- The registry reports a closed bead's active or unfinished artifacts as
  drift, so closing after a merge leaves a second, unautomated duty
  (`research.md`, "The tracker-side close machinery exists"). The interview
  records the backlog on 2026-11-06; it is not a current measurement here.
- Moving alone is insufficient: the registry requires archived completion
  headers and a regenerated index, and the freshness check holds the moved
  files' update dates (`research.md`, "Which files a change would have to touch").

## Terms

**Eligible folder:** an immediate real directory under `plans/changes/`, other
than `archive`, whose registry artifacts all name the same nonempty bead and
whose bead is `closed` in the validated tracker render for this invocation.
Registry artifacts are the Markdown files the existing registry enumerates.

**Archiving day:** the local calendar date captured once at invocation start;
the same date supplies the archive prefix and all changed date fields.

## Acceptance criteria

1. When the command inspects active change folders, its report identifies exactly the eligible folders and gives a reason for each skipped folder.
   *Refuted by:* selecting an open, unknown, beadless or mixed-bead folder, silently omitting a closed eligible folder, or treating an existing archive or living spec as active.
   *Basis:* `decisions.md#Q-1` and its tracker-read detail.

2. When invoked without `--write`, including through `make archive`, the command leaves repository files and tracker state unchanged.
   *Refuted by:* a changed file, folder move, index rewrite, tracker write or Git mutation caused by a report invocation.
   *Basis:* `decisions.md`, report-default detail.

3. When invoked with `--write` on a valid batch, the command relocates every eligible folder in full to `plans/changes/archive/YYYY-MM-DD-<name>/` for the archiving day.
   *Refuted by:* a remaining eligible source, a different date/name, a missing companion file, a changed non-artifact byte or a changed historical Markdown body.
   *Basis:* `decisions.md#Q-1` and its archive-day detail.

4. When an artifact is archived, its header has `status: accepted`, `implementation_status: done`, and `updated` and `last_reviewed` equal to the archiving day.
   *Refuted by:* an omitted or incorrect completion field, or a changed original `date`, bead, class, criterion, decision, provenance or other unrelated field.
   *Basis:* `decisions.md`, header-normalisation detail.

5. When a write run completes successfully, `plans/INDEX.md` equals the existing registry generator's output for the resulting tree.
   *Refuted by:* a stale source row, missing archive row or any byte difference from that generator's output.
   *Basis:* `decisions.md#Q-1`; `research.md`, index regeneration evidence.

6. If the tracker render or an otherwise eligible folder cannot be safely interpreted, the command exits nonzero before modifying the batch.
   *Refuted by:* any mutation despite an unreadable, empty, malformed or duplicate-ID render, malformed artifact header, existing destination, or symbolic-link source/member/destination boundary.
   *Basis:* `decisions.md`, tracker-read detail; `research.md`, per-artifact coupling.

7. If a filesystem operation or index generation fails during writing, the command returns nonzero with a diagnostic distinguishing completed moves from unfinished work.
   *Refuted by:* a success exit, a claim that the batch completed, overwritten destination evidence or a hidden partial result.
   *Basis:* `decisions.md#Q-1`; the command must give usable evidence for the requested application.

8. When rerun after a successful archive operation with unchanged inputs, the command leaves the resulting tree byte-identical.
   *Refuted by:* another dated copy, changed historical archive headers or an unnecessary index rewrite.
   *Basis:* `decisions.md#Q-1`, recurring use after merges.

9. When following the documented merge procedure after confirmed `MERGED` and closure reconciliation, the responsible session runs the archive command in write mode against an up-to-date checkout and retains its changes for the ordinary reviewed Git workflow.
   *Refuted by:* an omitted command, execution before merge confirmation or closure reconciliation, an automatic commit/push, or an instruction to modify another session's checkout.
   *Basis:* `decisions.md#Q-1`, use after every merge next to `make close-merged`.

10. When the orchestrator applies the tool once to the real backlog, it records the dated source/destination file manifest and before/after registry evidence covering every eligible folder of that run.
    *Refuted by:* an eligible folder left active, a move outside the manifest, missing evidence, or a claim of a green strict registry while unrelated drift remains.
    *Basis:* `decisions.md#Q-1`, one-off application to the whole backlog.

## Non-goals

- Closing or reopening beads, deciding whether work was actually completed,
  promoting deltas into living specs, changing ADRs, or repairing unrelated drift.
- Altering archive-sensitive gates, granting new historical exemptions, or
  rewriting old criteria, interview answers, findings or criterion ledgers.
- New SessionStart automation, CI write jobs, scheduling, merge automation,
  automatic commits/pushes, or rollout to other repositories.
- General reference/link migration; historical body text is preserved, including
  old relative links. Whole-batch transactional recovery after an I/O failure
  and concurrent writers are outside the guarantee; partial failure is explicit.
- Design phase 2b and an ADR: the recorded class is `bounded`, using the
  existing archive layout and tracker/render/index contracts.

## Protected areas

The tracker database and its wrapper, living specs under `plans/specs/`,
pre-existing archived folders, ADRs, gate/adoption/answer records, provenance
rules, model routing, kit manifests and harness configuration stay untouched.
`prompts/07-commit.md` is held: only the orchestrator adds the post-merge
invocation after the implementation attempt is accepted.

## Definition of Done

- `make verify` is green on the combined tool, procedure and backlog diff.
- Delivered together: `scripts/archive_closed_changes.py`, its tests, the
  Make target/help, its local-caller inventory entry, `prompts/07-commit.md`,
  the measured archive moves and regenerated `plans/INDEX.md`.
- Tests preserve the existing archive-sensitive gate behavior; the protected
  areas and non-goals are checked against the pull request file list.
- The orchestrator records the live report, named move manifest and registry
  evidence with the application commit in `findings.md` and the PR body.
  Unrelated strict-registry findings are reported separately, never waived.
- The PR closes the archive-tool work item (coding-harness-cqun); its final
  completion commit carries `Closes-Bead: coding-harness-cqun`.

## Open decisions

None open. The following reversible implementation details are explicit;
none changes the recorded class or the maintainer's answer.

- [DETAIL] Require agreement on one bead across the folder's registry
  artifacts; report missing/mixed identities instead of guessing which work
  item owns historical evidence.
- [DETAIL] Validate the render before selecting anything, through
  `bead_render.py`; preflight every eligible source and destination before
  writing. An unavailable state is a failure, never an empty backlog.
- [DETAIL] Preserve Markdown bodies and unrelated header values rather than
  reserialising historical documents. Only the four recorded lifecycle fields
  change; relative-link repair would require a separate scope.
- [DETAIL] Use the existing post-merge prompt as the recurring caller, with
  archive changes reviewed normally. Do not add automatic working-tree writes
  to the startup hook or make closure itself mutate files.
- [DETAIL] Set a three-hour phase-4 appetite including repairs. This bounds
  the local command and bootstrap/application work without promising wider
  drift repair; stop and report unfinished work at that limit.
