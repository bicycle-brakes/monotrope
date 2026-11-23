---
title: "Plan — commit-hook-stamp"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, commit-hook]
---

# Plan — commit-hook-stamp

```text
For you:     Normal commits stamp staged documents that require a current date.
Done when:   Temporary-repository commit tests prove the stamp and staging boundaries, and make verify is green.
Appetite:    3 hours of phase 4, repairs included — stop at the limit.
Not now:     Changing CI policy, other stamp writers or commits that bypass hooks.
Pre-mortem:  suppose it failed: most likely because a partially staged file brought unstaged edits into a commit.
Starts unless you say stop.
```

## Files and sequence

The plan remains provisional until the maintainer settles the open phase-2a ambiguities; do not start implementation on this card yet.

1. Create `scripts/hooks/stamp_staged.py` to select staged held documents, reuse the gate's classification and stamp writer, validate all results before changing the index, and preserve modes and staged bytes outside the date. Report measurement refusal and leave the index untouched; report runtime and stamping failures. Keep existing stamp callers intact.
2. Create `tests/test_commit_hook_stamp.py` with temporary Git repositories and real commits to exercise staging, failures, the installed and regenerated hook, and tracker integration through a controlled stand-in. Replace the ledger's `not yet written` markers when tests exist.
3. After the accepted implementation attempt, the orchestrator edits held path `.beads/hooks/pre-commit` to call the script outside the managed section, preserving tracker behavior, and `scripts/kit/manifest.yaml` to carry the script. Exercise actual installation and regeneration; if another held installer path is needed, the orchestrator owns that edit too.
4. Change `docs/WORKFLOW.md` to explain automatic stamping for installed hooks, its index-only behavior and the continued manual command for hook-bypassed commits. The runner owns derived index and findings updates. No files are deleted; no design or ADR is due for a bounded change.

Do not change the Beads managed section, tracker data, CI gate, other stamp writers, or custom hook configurations.

## Verification

```sh
python3 -m pytest tests/test_commit_hook_stamp.py tests/test_frontmatter_current.py -q
make verify
```

## Criterion ledger

- 1: not yet written tests/test_commit_hook_stamp.py::test_commit_stamps_staged_held_documents — stale, future or missing dates remain in the commit.
- 2: not yet written tests/test_commit_hook_stamp.py::test_partial_staging_preserves_index_content — unstaged edits enter the commit or staged content is lost.
- 3: not yet written tests/test_commit_hook_stamp.py::test_stamp_leaves_worktree_and_unrelated_index_unchanged — worktree or unrelated staged content changes.
- 4: not yet written tests/test_commit_hook_stamp.py::test_unsafe_header_blocks_commit_with_diagnostic — unsafe input commits or lacks a path and reason.
- 5: not yet written tests/test_commit_hook_stamp.py::test_beads_hook_still_runs_and_propagates_failure — tracker execution is skipped or failure ignored.
- 6: not yet written tests/test_commit_hook_stamp.py::test_deleted_and_nonheld_paths_are_untouched — deletion or non-held content changes.
- 7: not yet written tests/test_commit_hook_stamp.py::test_measurement_refusal_warns_and_preserves_index — measurement refusal blocks, silently passes, or changes the index.
- 8: not yet written tests/test_commit_hook_stamp.py::test_later_failure_preserves_entire_index — an earlier index entry changes after a later failure.
- 9: not yet written tests/test_commit_hook_stamp.py::test_installed_and_regenerated_hook_stamps — installation or regeneration loses the invocation.
- 10: not yet written tests/test_commit_hook_stamp.py::test_future_threshold_matches_currency_gate — the threshold differs from tomorrow UTC.
- 11: not yet written tests/test_commit_hook_stamp.py::test_kit_contains_staged_stamp_script — the assembled kit lacks the script.
- 12: not yet written tests/test_commit_hook_stamp.py::test_post_stamp_validation_blocks_invalid_result — a failed validation permits a commit.

## Time used

2026-11-23 17:16:42–17:19:01 UTC, 139 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 17:30:30–17:33:13 UTC, 163 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
