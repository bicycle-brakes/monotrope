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
For you:     Preview and explicitly remove clean, merged worktrees and their local branches.
Done when:   Safety checks, preview, explicit removal and the handover instructions are verified.
Appetite:    4 hours for phase 4, including repairs; stop at the limit.
Not now:     Automatic cleanup, age limits, count gates and remote branch removal.
Pre-mortem:  suppose it failed: most likely because a missing safety check was mistaken for permission to delete.
Starts unless you say stop.
```

## Implementation

1. Add `scripts/worktree_prune.py`: fetch `origin/main` successfully before classifying registered worktrees; enumerate with Git's porcelain format, report candidates and kept reasons, and treat unreadable status, operation state, ancestry or upstream as refusal. Distinguish no configured upstream from an unresolved configured upstream. Before each write repeat every check, including checkout identity; use `git worktree remove` without force, then `git branch -d`, reporting partial failure and exiting nonzero. Never delete a remote branch. Keep locked, missing or otherwise uninspectable worktrees with a reason. Use temporary repositories for verification, never real worktrees.
2. Change `Makefile`: add `prune-worktrees` and help, with the existing `archive` raw command-line `ARGS` whitelist and Makefile anchoring; environment `ARGS` cannot opt into writes and invalid arguments fail before execution.
3. Add `tests/test_worktree_prune.py`: exercise the command in disposable repositories with a local origin, including fetch failure, clean merged and unmerged branches, each dirty/operation state, absent, equal, divergent and missing upstreams, main/current exclusions, recheck before removal, Git refusals, and remote-branch preservation. Exercise the Make target's argument handling including an environment-only `ARGS=--write`.
4. Change `scripts/ci_gates.py` to classify the new tested, non-gate script; change `scripts/kit/manifest.yaml` to carry the script and its test to kit instances, and satisfy the kit's empty-repository probe. The Makefile is repository-specific, so the kit test must not require it in an exported instance.
5. The orchestrator updates `docs/WORKFLOW.md` rule 6 and `tools/claude-code/skills/handover/SKILL.md` with preview and explicit-write commands; the orchestrator updates the held `prompts/07-commit.md` after the accepted implementation attempt. Before the handover-convention edit the orchestrator runs the required fresh-session pre-change measurement in `docs/WORKFLOW.md`, then reinstalls the skill with `tools/claude-code/install.sh` and records the evidence. No implement or repair attempt edits the held prompt.
6. Regenerate `plans/INDEX.md` from the artifact headers when the runner permits that generated path; do not hand-edit it.

The command reports a failed branch deletion after successful worktree removal as a partial result; it does not force deletion or recreate the worktree. The final check and removal are not atomic against concurrent writers (spec Boundary).

## Verification

```sh
python3 -m pytest tests/test_worktree_prune.py -q
make verify
```

Run the targeted test after each repair and `make verify` after the orchestrator's documentation edits. The phase-6 review checks the handover text and the recorded pre-change measurement.

## Criterion ledger

- 1: not yet written tests/test_worktree_prune.py::test_preview_lists_candidates_without_removal — an eligible worktree is omitted or removed
- 2: not yet written tests/test_worktree_prune.py::test_detached_and_unmerged_are_kept — either is omitted or eligible
- 3: not yet written tests/test_worktree_prune.py::test_dirty_worktrees_are_kept — staged, unstaged or untracked work is removed
- 4: not yet written tests/test_worktree_prune.py::test_in_progress_operations_are_kept — merge, rebase or cherry-pick is eligible
- 5: not yet written tests/test_worktree_prune.py::test_configured_upstream_must_match — divergent or missing upstream is eligible
- 6: not yet written tests/test_worktree_prune.py::test_no_upstream_requires_merged_tip — unmerged tip is eligible
- 7: not yet written tests/test_worktree_prune.py::test_main_and_invoking_worktrees_are_kept — either is eligible
- 8: not yet written tests/test_worktree_prune.py::test_write_removes_worktree_then_local_branch_without_force — removal order or force discipline is wrong
- 9: not yet written tests/test_worktree_prune.py::test_fetch_or_safety_check_failure_keeps_worktree — failed check allows removal
- 9: not yet written tests/test_worktree_prune.py::test_write_rechecks_before_removal — changed candidate is removed
- 10: not yet written tests/test_worktree_prune.py::test_git_removal_failures_report_partial_result — a failed operation exits successfully
- 11: not a test — phase-6 review checks both commands in the handover instructions
- 12: not yet written tests/test_worktree_prune.py::test_remote_branch_is_preserved — the remote branch disappears
- 13: not yet written tests/test_worktree_prune.py::test_make_target_requires_exact_write_argument — invalid or environment-only arguments cause a write

## Not touched

`scripts/stage2.py` and its review-loop records, `scripts/machine_facts.py`, `decisions/gates.yaml`, remote branches, and existing worktrees outside a user's explicit cleanup run remain outside this change. No age threshold, automatic cleanup or count gate is added.

## Time used

2026-11-22 03:36:25–03:37:58 UTC, 92 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
