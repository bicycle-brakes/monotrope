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
For you:     The document-date check uses bounded Git processes and keeps its results, with literal paths and clear batch failures.
Done when:   Equivalence and failure tests pass and same-commit timings show the gate is at least twice as fast.
Appetite:    4 hours for implementation and repairs; stop at the limit.
Not now:     Changes to date policy, stamping, gate configuration or other checks.
Pre-mortem:  suppose it failed: most likely because batched Git history differs from a single path at a merge.
Starts unless you say stop.
```

## Steps

1. Change `scripts/check_frontmatter_current.py`: retain dirty detection; use at most one batched history invocation and three Git processes in the date check, with no per-document fallback. Match the literal per-path oracle for dates and hashes, including nested roots, renames and merges. A missing path retains its per-file diagnostic; a failed batch names the command and protected stderr without blaming a file, and exits 3. Stop and report if equivalence cannot be achieved within the process bound.
2. Change `tests/test_frontmatter_current.py`: compare dates and hashes with the literal per-path oracle in synthetic histories, including divergent merges, renames, nested roots, glob and pathspec-magic names and missing history. Exercise dirty, staged and untracked paths, failure diagnostics, output and stamp bytes, and count every Git process in the date check for different held-set sizes; faults are in the ledger.
3. Before implementation, measure `python3 scripts/check_frontmatter_current.py` five times on this repository's clean full history; after implementation measure it five times on the same machine and committed history, using the same environment and command. Record the commit, method, each elapsed time and exit status in the pull request; compare medians. Stop and report instead of shipping if the after median exceeds half the before median or a run fails.
4. Run `python3 -m pytest tests/test_frontmatter_current.py` and `make verify`; report results and timings for the orchestrator's pull request. No held path needs an implementation edit.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM 5.3 Flash via Z.ai had reached its weekly limit until 2026-11-29 (`research.md`, 2026-11-25).

## Criterion ledger

- 1: not yet written tests/test_frontmatter_current.py::test_date_check_has_bounded_git_processes — a fourth process or per-document fallback occurs as the held set grows.
- 2: not yet written tests/test_frontmatter_current.py::test_batch_matches_literal_per_path_history — a date or hash differs from the literal oracle at a merge, rename, nested root or special path.
- 3: tests/test_frontmatter_current.py::test_an_uncommitted_edit_is_held_against_today — an edited file is dated from history.
- 3: tests/test_frontmatter_current.py::test_a_root_below_the_top_of_the_repository_sees_its_own_edits — a nested-root edit is missed.
- 3: not yet written tests/test_frontmatter_current.py::test_staged_and_untracked_documents_use_today — a staged or untracked path receives a commit reference.
- 4: not yet written tests/test_frontmatter_current.py::test_missing_history_keeps_per_file_diagnostic — a missing path changes the diagnostic or exit 3.
- 5: not yet written tests/test_frontmatter_current.py::test_failed_batch_names_command_without_blaming_file — the failure omits protected stderr, blames a file or changes exit 3.
- 6: not yet written tests/test_frontmatter_current.py::test_batch_preserves_check_and_stamp_output — an exit, stale line or stamped byte changes outside the specified exceptions.
- 7: not a test — phase-6 review checks the pull request's same-commit, same-machine timing method, individual results and exit statuses; a missing measurement fails review.
- 8: not a test — phase-6 review compares the recorded five-run medians; an after median over half the before median stops shipping.

## Do not touch

Leave `provenance.yaml`, `decisions/gates.yaml`, `.github/workflows/ci.yml`, `docs/governance/gate-catalog.md`, other gates and the second held-file enumeration alone.

## Time used

2026-11-25 02:07:21–02:08:47 UTC, 85 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:13:25–02:15:08 UTC, 103 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
