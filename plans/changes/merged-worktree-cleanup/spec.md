---
title: "Spec — merged-worktree-cleanup"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, worktrees]
class: bounded
adr_files: []
---

# Spec — merged-worktree-cleanup

Provide an explicit way to retire finished, safe-to-remove worktrees and their local branches (bead coding-harness-bxxt.4 — merged worktree cleanup). Research: `research.md`. Decisions: `decisions.md`; review dispositions: `findings.md`, phase 2a.

## Problem

- Worktree removal after merge is a manual rule; neither the session guard nor the post-merge cleanup sequence carries it out (`research.md`, 2026-11-22).
- The 2026-11-21 machine snapshot recorded 117 registered worktrees; the work item records disk pressure from accumulated worktrees on 2026-11-09 (`research.md`, `decisions.md`).

## Terms

**Merged pull request:** a merged pull request in the origin repository whose head branch name and head commit exactly match the local branch and its current tip, and whose tip is an ancestor of freshly fetched `origin/main`.

**Pushed:** the local tip equals or is an ancestor of its fresh `origin/<branch>` remote-tracking tip; if that branch ref is absent after a successful pruning fetch, a matching merged pull request proves the local tip landed. An upstream of `origin/main` is not the branch's own remote ref. A configured branch-specific upstream that cannot be resolved is not evidence of a push; the gone-ref case still requires the matching merged pull request.

**Clean:** no staged, unstaged, or untracked non-ignored changes, and no merge, rebase or cherry-pick in progress.

**In use:** a running process has the worktree or a directory inside it as its working directory, or a lane busy marker identifies the worktree. An unavailable or incomplete check is not evidence that it is unused.

**Eligible:** a registered, present worktree with an attached branch other than `main`, a matching merged pull request, clean and pushed, not in use or locked, neither the main checkout nor the invoking worktree, and with every safety check completed successfully. These conditions are sufficient as well as necessary.

## Acceptance criteria

1. When `make prune-worktrees` runs with successful checks, it reports every eligible worktree as a removal candidate without removing worktrees, registrations or local branches.
   *Refuted by:* an eligible worktree is omitted, or preview removes any of those objects.
2. When a present registered worktree is ineligible, the report names it as kept and gives its reason.
   *Refuted by:* a detached, unmerged, dirty, in-use, locked, protected or otherwise ineligible worktree is omitted, lacks a reason, or is a candidate.
3. When the matching merged pull request is absent or its head branch or head commit differs from the local branch or tip, the worktree is kept.
   *Refuted by:* a fresh worktree whose tip is on `origin/main`, or a worktree with a mismatched pull request, is a candidate.
4. When the local tip is not an ancestor of freshly fetched `origin/main`, the worktree is kept.
   *Refuted by:* an unmerged tip is a candidate.
5. When a fresh `origin/<branch>` ref exists, the worktree is kept unless the local tip equals or is an ancestor of that ref.
   *Refuted by:* an ahead or divergent local tip is a candidate.
6. When a fresh `origin/<branch>` ref is absent, a matching merged pull request is required as evidence that the local tip landed.
   *Refuted by:* a missing remote branch with no matching merged pull request is treated as pushed.
7. When a worktree contains staged, unstaged or untracked non-ignored changes, it is kept.
   *Refuted by:* any of these changes is removed or the worktree is a candidate.
8. When a merge, rebase or cherry-pick is in progress in a worktree, it is kept.
   *Refuted by:* any such worktree is a candidate or removed.
9. When a worktree is in use or locked, it is kept.
   *Refuted by:* a worktree with a process working directory inside it, a lane busy marker, or a Git lock is a candidate or removed.
10. When the main checkout, the invoking worktree or a worktree on local `main` is encountered, it is kept.
    *Refuted by:* any of these is a candidate or removed.
11. When `make prune-worktrees ARGS=--write` runs after successful checks, it repeats the safety checks immediately before removing each still-eligible worktree without force, then attempts non-forcing local branch deletion from the main checkout.
    *Refuted by:* a changed candidate is removed, force is used, or branch deletion is attempted before removal or from a different checkout.
12. When a missing-directory registration is prunable, preview reports it separately and only the explicit-write form may prune it using Git's worktree prune operation.
    *Refuted by:* it is omitted, preview prunes it, or the write form removes its branch as a consequence of pruning the registration.
13. When the fresh fetch or a safety check fails, the command reports the failure and exits nonzero in both modes.
    *Refuted by:* the failure is silent or the command exits successfully.
14. When the initial fetch or any initial safety check fails, the write form makes no removals.
    *Refuted by:* a worktree, registration or branch is removed despite an initial check failure.
15. When a repeated safety check fails during a write run, the command stops further removals and reports any earlier changes.
    *Refuted by:* removal continues after that failure or an earlier removal is omitted from the report.
16. When worktree removal or local branch deletion fails, the command reports the failure and partial result, continues with other candidates, and exits nonzero.
    *Refuted by:* a refusal stops other candidates, exits successfully, or hides a removed worktree whose branch remains.
17. When the handover routine is followed, it directs the session to run preview, read its output, and then run the explicit-write form.
    *Refuted by:* either command or the intervening review is absent from the handover instructions.
18. When the command is invoked, no remote branch is deleted.
    *Refuted by:* a remote branch is deleted; pruning stale local remote-tracking refs is allowed.
19. When an argument other than empty command-line `ARGS` or exactly `--write` is supplied to the Make target, the target rejects it without removing a worktree, registration or branch.
    *Refuted by:* another argument is accepted or causes a removal.
20. When the kit is exported to a new repository, it does not include this cleanup command.
    *Refuted by:* the new cleanup script is included in the kit manifest or export.

## Non-goals

- Scheduled cleanup, age thresholds, worktree-count gates, and remote branch deletion.
- Cleaning dirty trees, rewriting history, or changing review-loop record discovery and supersession.
- Shipping this repository's lane housekeeping in the kit; a later change may reconsider portability.

## Protected areas

- The main checkout, the invoking worktree, `main`, worktrees in use and worktrees lacking safe evidence: they may contain ongoing work.
- Remote branches: only stale local remote-tracking refs may be pruned by the fetch.

## Definition of Done

- `make verify` green after implementation and orchestrator edits.
- `docs/WORKFLOW.md` and `tools/claude-code/skills/handover/SKILL.md` updated in the same pull request; no ADR.
- Protected areas preserved and non-goals unbuilt, checked against the pull request and tests.
- The pull request closes the merged worktree cleanup bead (`coding-harness-bxxt.4`), with `Closes-Bead: coding-harness-bxxt.4` in its last commit.
- The handover-convention pre-change measurement and skill installation are recorded with their relevant commits.

## Open decisions

None open. [DETAIL] The phase-2a dispositions in `findings.md` settle the merged-PR proof, use checks, stale registrations, failure handling, handover sequence and kit scope. Their reason is to avoid mistaking a branch based on main or missing evidence for a finished lane. A pruning fetch may update local remote-tracking refs during preview.

**Boundary:** The final safety checks and Git removal are not atomic against other processes. A process or marker can appear between them; Git's non-forcing removal is a final guard, not a lock on other writers. Git's registration pruning also changes the set of worktrees through which existing review-loop records are discovered; it does not change the discovery mechanism.
