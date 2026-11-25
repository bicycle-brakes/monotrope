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

1. Change `scripts/check_frontmatter_current.py`: retain dirty detection; use at most one batched history invocation and three Git processes in `reference_dates` including dirty-set calls, excluding preflight and held-file enumeration, with no per-document fallback. Force `log.follow=false` for both batch and literal per-path oracle while retaining other Git configuration; match dates and hashes, including nested roots, renames and merges. A missing path retains its per-file diagnostic; a failed batch names the command and stderr bounded to the last 20 lines and 2,000 characters with a truncation marker when cut and no redaction, without blaming a file, and exits 3. Stop and report if equivalence cannot be achieved within the process bound.
2. Change `tests/test_frontmatter_current.py`: compare dates and hashes with the literal per-path oracle in synthetic histories, including divergent merges, renames, nested roots, glob and pathspec-magic names and missing history; set repository `log.follow=true` to verify the override. Exercise dirty, staged and untracked paths, failure diagnostics, output and stamp bytes, and count every Git process in the date check for different held-set sizes; faults are in the ledger.
3. On one checkout after implementation, export the base commit's complete `scripts/` directory with `git archive` to a temporary directory; run its gate script with `--root` pointing at the checkout and run the changed script on the same checkout and machine, five times each with the same environment. Record the checkout commit, method, each elapsed time and exit status and both medians in the pull request; stop and report if a run fails or the after median exceeds half the before median.
4. Run `python3 -m pytest tests/test_frontmatter_current.py` and `make verify`; report results and timings for the orchestrator's pull request. No held path needs an implementation edit.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM 5.3 Flash via Z.ai had reached its weekly limit until 2026-11-29 (`research.md`, 2026-11-25).

## Criterion ledger

- 1: tests/test_frontmatter_current.py::test_date_check_has_bounded_git_processes — a fourth process inside `reference_dates` or a per-document fallback occurs as the held set grows.
- 2: tests/test_frontmatter_current.py::test_batch_matches_literal_per_path_history — a date or hash differs from the literal oracle with `log.follow=false` at a merge, rename, nested root or special path, including with repository `log.follow=true`.
- 3: tests/test_frontmatter_current.py::test_an_uncommitted_edit_is_held_against_today — an edited file is dated from history.
- 3: tests/test_frontmatter_current.py::test_a_root_below_the_top_of_the_repository_sees_its_own_edits — a nested-root edit is missed.
- 3: tests/test_frontmatter_current.py::test_staged_and_untracked_documents_use_today — a staged or untracked path receives a commit reference.
- 4: tests/test_frontmatter_current.py::test_missing_history_keeps_per_file_diagnostic — a missing path changes the diagnostic or exit 3.
- 5: tests/test_frontmatter_current.py::test_failed_batch_names_command_without_blaming_file — the failure omits stderr, exceeds either bound, lacks a truncation marker when cut, redacts stderr, blames a file or changes exit 3.
- 6: tests/test_frontmatter_current.py::test_batch_preserves_check_and_stamp_output — an exit, stale line or stamped byte changes outside the specified exceptions.
- 7: not a test — phase-6 review checks five runs of each script on one checkout and machine, including the archived base scripts directory and its gate script with `--root`, individual results, exit statuses and medians; a missing measurement fails review.
- 8: not a test — phase-6 review compares the recorded five-run medians; an after median over half the before median stops shipping.

## Do not touch

Leave `provenance.yaml`, `decisions/gates.yaml`, `.github/workflows/ci.yml`, `docs/governance/gate-catalog.md`, other gates and the second held-file enumeration alone.

## Runner route — 2026-11-25

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu).

## Time used

2026-11-25 02:07:21–02:08:47 UTC, 85 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:13:25–02:15:08 UTC, 103 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:19:24–02:20:52 UTC, 88 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:26:39–02:28:01 UTC, 82 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:28:23–02:41:41 UTC, 798 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_check_adr_answers.py`, `tests/test_frontmatter_current.py`, `tests/test_harness_decide_adr.py`, `tests/test_harness_time_log.py`, `tests/test_run_report.py`, `tests/test_templates.py`, `tests/test_venv_guard.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
