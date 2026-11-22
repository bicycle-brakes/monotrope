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

Provide a safe, explicit way to retire merged worktrees and their local branches (bead coding-harness-bxxt.4 — merged worktree cleanup). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The post-merge worktree removal rule is manual; neither the existing session guard nor the merge cleanup sequence removes worktrees (`research.md`, 2026-11-22).
- The 2026-11-21 machine snapshot recorded 117 registered worktrees, while the 2026-11-09 bead describes disk pressure from accumulated worktrees (`research.md` and `decisions.md`).

## Terms

**Merged:** the attached branch tip is an ancestor of freshly fetched `origin/main`.

**Clean and pushed:** no staged, unstaged, or untracked non-ignored changes, no merge, rebase or cherry-pick in progress, and either the branch tip equals its upstream tip or no upstream is configured and its tip is on `origin/main`.

## Acceptance criteria

1. When `make prune-worktrees` runs, it reports each eligible registered worktree as a removal candidate without removing any worktree or local branch.
   *Refuted by:* an eligible worktree is omitted or a worktree or local branch is removed.
2. When a registered worktree is detached or its branch is not merged, it is reported as kept with a reason.
   *Refuted by:* either is reported as a candidate or omitted without a reason.
3. When a worktree has staged, unstaged, or untracked non-ignored changes, it is kept with a reason.
   *Refuted by:* a worktree with any such change is a candidate or is removed.
4. When a worktree has a merge, rebase, or cherry-pick in progress, it is kept with a reason.
   *Refuted by:* a worktree with any such operation is a candidate or is removed.
5. When a branch has a configured upstream, its worktree is eligible only if the branch and upstream tips are equal.
   *Refuted by:* a divergent or unreadable upstream is treated as eligible.
6. When a branch has no configured upstream, its worktree is eligible only if its tip is on freshly fetched `origin/main`.
   *Refuted by:* a branch without an upstream and outside that history is eligible.
7. When the main checkout or the invoking worktree is encountered, it is kept with a reason.
   *Refuted by:* either is reported as a candidate or removed.
8. When `make prune-worktrees ARGS=--write` runs, each still-eligible worktree is removed without force before its local branch is deleted using Git's non-forcing branch deletion.
   *Refuted by:* an eligible worktree is not removed, its branch is not attempted after removal, or a force option is used.
9. When the fresh fetch or a safety check cannot be completed, affected worktrees are kept and the failure is reported.
   *Refuted by:* stale merge evidence or an unreadable check is treated as permission to remove.
10. When removal or local branch deletion fails, the failure and any partial result are reported with a nonzero exit status.
    *Refuted by:* the command reports success after Git refuses either operation.
11. When the handover routine is followed, it names the preview and explicit-write cleanup commands.
    *Refuted by:* the handover instructions omit either command.
12. When the command is invoked, no remote branch is deleted.
    *Refuted by:* any remote branch is deleted.
13. When an argument other than an empty command-line `ARGS` or exactly `--write` is supplied, the Make target rejects it without removing a worktree or branch.
    *Refuted by:* an invalid argument causes removal or is accepted.

## Non-goals

- An age threshold, automatic scheduled cleanup, a worktree-count gate or a dated valve.
- Remote branch cleanup, rewriting Git history, or cleaning dirty worktrees.
- Changing how review-loop records are discovered or superseded.

## Protected areas

- Existing worktrees and branches that fail a safety check, the main checkout and the invoking worktree: they may contain work or are in use.
- Remote branches: cleanup is local only.

## Definition of Done

- `make verify` green after implementation and the orchestrator's held-path edits.
- Documentation changed with the code: `docs/WORKFLOW.md`, `prompts/07-commit.md`, and `tools/claude-code/skills/handover/SKILL.md`; no ADR.
- Protected areas untouched and non-goals unbuilt, checked against the pull request's file list.
- The pull request closes the merged worktree cleanup bead (`coding-harness-bxxt.4`), with `Closes-Bead: coding-harness-bxxt.4` in its last commit.
- Special runs: the handover-convention pre-change measurement and skill installation, recorded with the relevant commit in the pull request.

## Open decisions

None open. [DETAIL] A failed or unavailable safety check keeps the affected worktree: this conservative default is reversible and prevents missing evidence from authorizing deletion. A configured but unreadable upstream is not treated as an absent upstream for the same reason. A fresh fetch may update remote-tracking refs even in preview; preview never removes a worktree or local branch.

**Boundary:** Checks are repeated immediately before removal, but Git offers no atomic transaction spanning status, ancestry and worktree removal; a concurrent process can change a candidate between the last check and removal. Git's non-forcing removal is the final guard, not a lock on other writers.
