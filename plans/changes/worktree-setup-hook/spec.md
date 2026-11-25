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

1. When Git invokes the installed checkout hook for a new worktree with an all-zero previous object ID and branch-checkout flag `1`, and the checked-out state is trusted, it runs `make venv` in that worktree. A state is trusted when its commit is an ancestor of `origin/main`, or when `Makefile`, `requirements*.txt` and `tools/pi/` equal `origin/main`'s; an untrusted state, or one where `origin/main` is unknown, skips setup with one line naming the reason and the deliberate command `bash .beads/hooks/post-checkout --lane-setup`, which runs setup regardless of trust (maintainer 2026-11-25, loop row L2-5).
   *Refuted by:* A qualifying checkout skips the command or runs it elsewhere.
2. When setup runs, it runs `bash tools/pi/install.sh` in the new worktree.
   *Refuted by:* The installation is skipped or runs elsewhere.
3. When setup reaches its checks, it checks that the new worktree's virtual environment imports `yaml`.
   *Refuted by:* A broken import passes without a failure report.
4. When setup reaches its checks, it checks that the new worktree's Pi launcher reports the exact pinned version.
   *Refuted by:* A missing, failing or mismatched launcher passes without a failure report.
5. If a setup command or check fails, stderr includes a line beginning `LANE SETUP FAILED:` that names the failed step, the log path and the retry command; when the log cannot be written, stderr says so and the summary names the log as unavailable.
   *Refuted by:* A failure lacks that line, step or path.
6. If setup fails, that failure does not change an otherwise successful hook invocation to a nonzero exit.
   *Refuted by:* A setup failure makes an otherwise successful hook fail.
7. When `HARNESS_NO_LANE_SETUP` is exactly `1`, the hook skips setup and its checks.
   *Refuted by:* An opted-out invocation runs a setup command or check.
8. When a checkout is not a new worktree checkout, the hook skips setup and its checks.
   *Refuted by:* A file checkout or ordinary branch checkout runs setup or checks.
9. When the hook runs, the existing Beads integration receives its original arguments and retains its exit behavior.
   *Refuted by:* Setup prevents its invocation, changes its arguments or masks its result.
10. When setup runs, it finishes in the foreground before `git worktree add` returns.
    *Refuted by:* Git returns while setup or its checks are still running.
11. When setup exceeds `HARNESS_LANE_SETUP_TIMEOUT` seconds, defaulting to 600, it stops and reports the step and limit, with or without Perl. An unset or empty value means 600; `0`, a negative or a non-numeric value falls back to 600 and prints exactly one warning line naming the given value (decisions S-8).
    *Refuted by:* An overdue step continues or the failure report omits the step or limit.
12. When the Beads integration fails on a qualifying checkout, setup has already run.
    *Refuted by:* A failing Beads invocation prevents setup.
13. When setup runs, command and check output is written to `lane-setup.log` in the new worktree's Git directory.
    *Refuted by:* Output goes to the caller instead or the log is absent from that Git directory.
14. When setup runs, stderr shows one start line `lane setup: start: …` and one summary line, exactly `lane setup: ok` or `lane setup: failed (N checks)`, followed by `lane setup: log: <path>` (decisions S-7).
    *Refuted by:* Either line is absent or repeated.
15. When `HARNESS_NO_LANE_SETUP` has any value other than `1`, including empty or unset, a qualifying trusted checkout runs setup.
    *Refuted by:* Such a value skips setup.

## Non-goals

- Changing Git hook configuration or installing the hook in repositories where it is not enabled.
- Setting up existing worktrees, changing dependency pins, or modifying other hooks.
- Changing the runner to create worktrees.

## Protected areas

The Beads-managed block and historical handovers remain unchanged; hook additions belong outside the managed block. A test compares the text between the `BEGIN` and `END BEADS INTEGRATION` markers with `origin/main` and fails on any change (decisions S-9).

## Definition of Done

- `make verify` green; the pull request records a real new-worktree smoke test and its commit.
- Update `AGENTS.md` and `docs/WORKFLOW.md` with automatic setup and the manual fallback; the pull request records the post-merge tracker-memory follow-up.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request file list.
- The pull request closes `coding-harness-wg4z` and its last commit carries `Closes-Bead: coding-harness-wg4z`.

## Open decisions

- [DETAIL] Run both installation steps even if one fails, then report each failed check unless the overall timeout stops setup: this gives useful partial setup and diagnosis without failing checkout.
- [DETAIL] Use a 600-second overall setup limit, configurable through `HARNESS_LANE_SETUP_TIMEOUT`, to bound foreground delay.
- [DETAIL] Run setup above the unchanged Beads-managed block so a Beads failure cannot skip it.
- [DETAIL] Put setup output in the worktree Git directory and give concise stderr status and failure lines so failures remain visible.
- [DETAIL] Rewrite the tracker memory `new-worktree-needs-pi` to point to the hook after merge; the pull request records this follow-up because the tracker is outside its diff.
- [DETAIL] Three hours is the phase-4 stop, including repairs; the scope is a hook, isolated tests and documentation.
- [DETAIL] The existing `neighbours: []` is retained: neither related change was confirmed as a research-swarm neighbour.
