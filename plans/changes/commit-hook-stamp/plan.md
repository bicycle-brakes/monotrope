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

1. Change `scripts/check_frontmatter_current.py` to expose a staged-only `--stamp` mode: select staged added or modified held Markdown paths using the provenance rules; read and validate index blobs, use the existing stamp writer with the local date, and replace only their index entries while preserving file modes. Handle unusual path names safely; leave deletes and other paths alone. Refuse and name unsafe or unreadable headers and Git errors; do not silently partially succeed. Keep the existing whole-tree command and its callers intact.
2. Create `tests/test_commit_hook_stamp.py` with temporary Git repositories and actual commits. Exercise the real hook and stamp command, Beads integration via a controlled stand-in, partial staging, missing and duplicate headers, invalid UTF-8, unrelated files, deletion, failure propagation, and paths with spaces. The test fixture installs the tracked hook through Git's hook path without touching the real tracker. Replace the ledger's `not yet written` markers when the tests exist.
3. After the accepted implementation attempt, the orchestrator edits held path `.beads/hooks/pre-commit`: invoke the staged-only stamp command outside the managed Beads section, propagating failure while retaining the managed section unchanged. The temporary-repository tests must exercise this final hook; run them again after the bootstrap edit.
4. Change `docs/WORKFLOW.md` to explain automatic stamping for installed hooks, its index-only behavior and the continued manual command for hook-bypassed commits. The runner owns derived index and findings updates. No files are deleted; no design or ADR is due for a bounded change.

Do not change the Beads managed section, hook installation policy, tracker data, CI gate, other stamp writers, or custom hook configurations. Stop if preserving the existing installation path requires a further held-path edit; assign that edit to the orchestrator after an accepted attempt.

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

## Time used

2026-11-23 17:16:42–17:19:01 UTC, 139 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
