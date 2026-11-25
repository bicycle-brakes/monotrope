---
title: "Plan — frontmatter-batch-log"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25", model: "gpt-6.1-terra"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, performance]
---

# Plan — frontmatter-batch-log

```text
For you:     The document-date check uses one history call while keeping its existing results and messages.
Done when:   Equivalence and failure tests pass and the pull request records before and after timings at the same commit.
Appetite:    4 hours for implementation and repairs; stop at the limit.
Not now:     Changes to date policy, stamping, gate configuration or other checks.
Pre-mortem:  suppose it failed: most likely because batched Git history differs from a single path at a merge.
Starts unless you say stop.
```

## Steps

1. Change `scripts/check_frontmatter_current.py`: keep dirty detection and the existing per-path contract, obtain clean paths' dates and hashes through one Git log call, preserve root-relative and arbitrary path names, rename and merge semantics, and fail closed with the existing per-file diagnostic. Do not silently substitute a history traversal that differs from the per-path oracle; stop and report if equivalence cannot be achieved with one call.
2. Change `tests/test_frontmatter_current.py`: compare every clean path against the old per-path Git command in synthetic histories, including renames, divergent branches, merges, a nested root, unusual path names and a missing commit; test failed Git, dirty and untracked paths, exact output, stamp behavior and the number of log calls. Use existing repository fixtures and isolate Git configuration. Faults are listed in the ledger.
3. Before changing the implementation, measure the gate at the current commit in a clean, full-history checkout; measure the changed implementation against the same committed history with the same command, environment and repetitions. Record command, commit, individual elapsed times, verdicts and environmental caveats in the pull request. Do not equate working-tree changes with a different history commit.
4. Run `make verify`; report the result and timings for the orchestrator's pull request. No held path needs an implementation edit.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM 5.3 Flash via Z.ai had reached its weekly limit until 2026-11-29 (`research.md`, 2026-11-25).

## Criterion ledger

- 1: not yet written tests/test_frontmatter_current.py::test_clean_documents_use_one_log_call — a second log process is started for another clean document.
- 2: not yet written tests/test_frontmatter_current.py::test_batch_matches_per_path_history — a date or hash differs from the per-path oracle after a rename, merge or nested root.
- 3: tests/test_frontmatter_current.py::test_an_uncommitted_edit_is_held_against_today — a dirty file is dated from history rather than today.
- 3: tests/test_frontmatter_current.py::test_a_root_below_the_top_of_the_repository_sees_its_own_edits — a nested-root edit is missed.
- 3: not yet written tests/test_frontmatter_current.py::test_staged_and_untracked_documents_use_today — a staged or untracked path receives a commit reference.
- 4: not yet written tests/test_frontmatter_current.py::test_batch_failure_keeps_per_file_diagnostic — missing history or a failed log changes the diagnostic or exit 3.
- 5: not yet written tests/test_frontmatter_current.py::test_batch_preserves_check_and_stamp_output — an exit, stale line or stamped byte changes.
- 6: not a test — phase-6 review checks the pull request's same-commit timing method, results and exit statuses.

## Do not touch

Leave `provenance.yaml`, `decisions/gates.yaml`, `.github/workflows/ci.yml`, `docs/governance/gate-catalog.md`, other gates and the second held-file enumeration alone.

## Time used

2026-11-25 02:07:21–02:08:47 UTC, 85 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
