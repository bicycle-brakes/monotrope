---
title: "Plan — merged-worktree-cleanup"
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
tags: [plan, worktrees]
---

# Plan — merged-worktree-cleanup

```text
For you:     Preview and explicitly remove finished, clean worktrees and their local branches during handover.
Done when:   Merged pull request proof, safety checks, removal and the handover instructions are verified.
Appetite:    4 hours for phase 4, including repairs; stop at the limit.
Not now:     Scheduled cleanup, age limits, count gates, remote branch removal and kit export.
Pre-mortem:  suppose it failed: most likely because missing evidence was mistaken for permission to delete.
Starts unless you say stop.
```

## Implementation

1. Add `scripts/worktree_prune.py` as the single cleanup entry point. Fetch `origin` with pruning, require fresh `origin/main`, enumerate registered worktrees using Git's porcelain output, and inspect each present tree and its operation state. Identify the main and invoking checkouts and local `main`; query merged pull requests in the origin repository by head branch and verify the exact head commit and ancestry, handling absent matches separately from failed or incomplete queries. Check the fresh `origin/<branch>` ref as specified, including behind, divergent, gone and `origin/main` upstream cases. Use process working-directory inspection and the night-run lane busy markers to keep in-use trees; unavailable or incomplete evidence fails closed. Preview reports every candidate, kept reason and missing-directory registration.
2. In that script, complete a read-only preflight for every registration before any write; on failure report it and make no removals. In write mode repeat safety checks immediately before each removal, stop on recheck failure, and report earlier changes; otherwise remove without force and run `git branch -d` from the main checkout. Continue after Git removal or branch-deletion refusals, report partial outcomes, and exit nonzero if any occur. Report prunable missing-directory registrations separately; before `git worktree prune --expire now`, inspect its dry-run set and recheck it so pruning cannot remove an unexamined or protected registration. Prune only on explicit write and never delete a branch as a consequence of registration pruning. The checks and Git's actions are not atomic against concurrent processes (spec Boundary).
3. Change `Makefile`: add `prune-worktrees` and help, following `archive`'s anchored invocation and raw command-line `ARGS` whitelist; environment-only `ARGS` cannot select writes. Reject invalid arguments before the script runs.
4. Add `tests/test_worktree_prune.py`: use disposable repositories and local origins, with controlled process, marker and pull-request-query responses. Cover exact pull-request head proof, default `origin/main` upstream, deleted remote branch, divergent and ahead tips, clean and dirty trees, operations, main/current/main-branch exclusions, live and locked trees, missing registrations, fetch and inspection failures, preflight and recheck failures, partial failures with continuation, no-force ordering, remote branch preservation and Make argument handling. Exercise the actual Git behavior for pruning and branch deletion; never use real worktrees.
5. Change `scripts/ci_gates.py` to classify the new tested non-gate script. Leave `scripts/kit/manifest.yaml` unchanged: this repository's lane housekeeping is not exported.
6. Change `docs/WORKFLOW.md` rule 6 and `tools/claude-code/skills/handover/SKILL.md`: specify preview, reading its report, then explicit write during handover. The orchestrator owns the skill edit: first run the fresh-session pre-change measurement in `docs/WORKFLOW.md`, then edit and reinstall with `tools/claude-code/install.sh`, recording evidence. The implementation attempt does not edit the held `prompts/` paths; no merge-prompt change is required.
7. Regenerate `plans/INDEX.md` through its generator when the runner permits that generated path; do not hand-edit it.

## Verification

```sh
python3 -m pytest tests/test_worktree_prune.py -q
make verify
```

Run the targeted test after each repair and `make verify` after the orchestrator's documentation edits. Phase 6 checks the handover instructions and pre-change measurement.

## Criterion ledger

- 1: not yet written tests/test_worktree_prune.py::test_preview_reports_eligible_without_removal — an eligible tree is omitted or preview removes it
- 2: not yet written tests/test_worktree_prune.py::test_ineligible_worktrees_report_reasons — a kept tree is omitted or has no reason
- 3: not yet written tests/test_worktree_prune.py::test_matching_merged_pull_request_required — an absent or mismatched head is accepted
- 4: not yet written tests/test_worktree_prune.py::test_tip_must_be_in_fresh_main — an unmerged tip is eligible
- 5: not yet written tests/test_worktree_prune.py::test_existing_remote_branch_must_contain_tip — an ahead or divergent tip is eligible
- 6: not yet written tests/test_worktree_prune.py::test_gone_remote_branch_requires_matching_pull_request — absent proof permits removal
- 7: not yet written tests/test_worktree_prune.py::test_dirty_worktrees_are_kept — staged, unstaged or untracked work is eligible
- 8: not yet written tests/test_worktree_prune.py::test_in_progress_operations_are_kept — a merge, rebase or cherry-pick is eligible
- 9: not yet written tests/test_worktree_prune.py::test_in_use_and_locked_worktrees_are_kept — a process, marker or Git lock is ignored
- 10: not yet written tests/test_worktree_prune.py::test_main_invoking_and_main_branch_are_kept — a protected checkout or branch is eligible
- 11: not yet written tests/test_worktree_prune.py::test_write_rechecks_and_removes_without_force — changed state, operation order or checkout is wrong
- 12: not yet written tests/test_worktree_prune.py::test_prunable_registrations_are_previewed_and_pruned_only_on_write — preview prunes or write deletes the branch
- 13: not yet written tests/test_worktree_prune.py::test_check_failures_are_reported_and_nonzero — a failed fetch or check is silent or exits zero
- 14: not yet written tests/test_worktree_prune.py::test_initial_check_failure_prevents_all_removals — a write proceeds after failed preflight
- 15: not yet written tests/test_worktree_prune.py::test_recheck_failure_stops_and_reports_prior_changes — later removal proceeds or prior removal is hidden
- 16: not yet written tests/test_worktree_prune.py::test_git_refusals_continue_and_report_partial_results — a refusal stops the batch, hides a partial result or exits zero
- 17: not a test — phase-6 review checks preview, review and write sequence in the handover skill
- 18: not yet written tests/test_worktree_prune.py::test_remote_branch_is_preserved — the remote branch is deleted
- 19: not yet written tests/test_worktree_prune.py::test_make_target_requires_exact_write_argument — invalid arguments are accepted or cause removal
- 20: not yet written tests/test_worktree_prune.py::test_cleanup_script_is_not_in_kit — the kit exports the cleanup script

## Not touched

`scripts/stage2.py`, review-loop record discovery, `scripts/machine_facts.py`, `decisions/gates.yaml`, `scripts/kit/manifest.yaml`, remote branches, and worktrees outside an explicit cleanup run. No scheduled cleanup, age threshold or count gate is added.

## Time used

2026-11-22 03:36:25–03:37:58 UTC, 92 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 03:42:45–03:45:42 UTC, 177 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
