---
title: "Spec — worktree-setup-hook"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, worktree, setup]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — worktree-setup-hook

New worktrees receive the local Python environment and pinned Pi through the versioned checkout hook (bead `coding-harness-wg4z`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-25 a new worktree lacked its environment and Pi, and `scripts/new_change.py` failed to import YAML; setup was a manual prerequisite (`research.md`, Topic and existing worktree guidance).
- The versioned checkout hook delegates to Beads but does not set up a worktree (`research.md`, What exists today, at commit `4b6fabe9`).

## Acceptance criteria

1. When Git invokes the installed checkout hook for a new worktree with a null previous object ID and branch-checkout flag `1`, it runs `make venv` in the new worktree.
   *Refuted by:* A qualifying checkout skips the command or runs it in another worktree.
2. When that setup runs, it runs `bash tools/pi/install.sh` in the new worktree.
   *Refuted by:* The Pi installation is skipped or runs in another worktree.
3. When setup completes, it checks that the new worktree's virtual environment imports `yaml`.
   *Refuted by:* A broken YAML import passes without a setup failure message.
4. When setup completes, it checks that the new worktree's Pi launcher reports the pinned version.
   *Refuted by:* A missing, failing or mismatched launcher passes without a setup failure message.
5. If a setup command or check fails, the hook reports the failed step prominently on standard error.
   *Refuted by:* A failing step is silent or its message does not identify it.
6. If a setup command or check fails, that failure does not make the checkout hook fail.
   *Refuted by:* Setup failure changes an otherwise successful hook invocation to a nonzero exit.
7. When `HARNESS_NO_LANE_SETUP=1`, the hook skips all lane setup and its checks.
   *Refuted by:* Any setup command or check runs with the opt-out set.
8. When a checkout is not a new worktree checkout, the hook skips lane setup and its checks.
   *Refuted by:* A file checkout or an ordinary branch checkout runs setup.
9. When the hook runs, the existing Beads integration retains its arguments and exit behavior.
   *Refuted by:* Setup prevents its invocation, changes its arguments, or masks its nonzero result.

## Non-goals

- Changing Git hook configuration or installing the hook in repositories where it is not enabled.
- Setting up existing worktrees, changing dependency pins, or modifying other hooks.
- Changing the runner to create worktrees.

## Protected areas

The Beads-managed block and historical handovers remain unchanged; hook additions belong outside the managed block.

## Definition of Done

- `make verify` green; the pull request records a real new-worktree smoke test and its commit.
- Update `AGENTS.md` and `docs/WORKFLOW.md` with automatic setup and the manual fallback; retire the obsolete tracker memory after the hook is available.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request file list.
- The pull request closes `coding-harness-wg4z` and its last commit carries `Closes-Bead: coding-harness-wg4z`.

## Open decisions

- [DETAIL] Run both installation steps even if one fails, then report each failed check: this gives the maintainer the most useful partial setup and diagnosis without blocking checkout.
- [DETAIL] Three hours is the phase-4 stop, including repairs; the scope is a hook, isolated tests and documentation.
- [DETAIL] The existing `neighbours: []` is retained: neither related change was confirmed as a research-swarm neighbour.
