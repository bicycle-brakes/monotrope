---
title: "Decisions — merged-worktree-cleanup"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, worktrees, disk]
---

# merged-worktree-cleanup — Decisions

Class: bounded (bead coding-harness-bxxt.4).

## The bead (read from the tracker by the orchestrator, 2026-11-22)

> Why: on 2026-11-09, 91 worktrees stood under .claude/worktrees (16 GiB, 71 with a .venv of their own) although AGENTS.md says a worktree is removed after the merge; with the temporary test folders they filled the disk. What: a command that lists worktrees whose branch is merged into origin/main and whose tree is clean, and removes them only with an explicit write argument (same discipline as make archive); the handover routine names it. Never removes a worktree with uncommitted or unpushed work. Source: docs/research/2026-11-09-make-verify-long-term.md (PR #361); maintainer 2026-11-09: 'Erstelle auch die anderen notwendigen Beads'.

On 2026-11-21 `git worktree list` showed about 120 worktrees.

## SKIP · interview

status: skipped
reason: The bead fixes what the command does, its safety rule and its write discipline; the maintainer asked for the bead on 2026-11-09 and for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Merged** means the worktree's branch tip is an ancestor of a freshly fetched `origin/main` (the merge queue merges with merge commits, so the tip is reachable). Detached worktrees and branches not merged are listed as kept, with the reason.
- **Clean and pushed** means: no staged, unstaged or untracked-not-ignored change; no merge, rebase or cherry-pick in progress; and the branch tip equals its upstream's tip, or the branch has no upstream and its tip is on `origin/main`. Anything else is kept and named.
- **Dry run by default:** `make prune-worktrees` lists what it would remove and what it keeps and why; `make prune-worktrees ARGS=--write` removes the worktree (`git worktree remove`, never `--force`) and then deletes the local branch with `git branch -d` (which refuses an unmerged branch on its own). Remote branches are not touched. Reason: the `make archive` discipline, and git's own refusals as a second guard.
- **The main checkout and the current worktree are never candidates.**
- **The handover routine names the command** (the handover prompt and `docs/WORKFLOW.md` §3, rule 6 on retiring worktrees). The prompt file is runner-held, so that line is an orchestrator hand edit after the accepted attempt.
