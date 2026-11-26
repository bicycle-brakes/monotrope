---
title: "Plan — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-va1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, merge-queue]
---

# Plan — enqueue-pr

```text
For you:     An eligible pull request can enter the merge queue unattended through one guarded command.
Done when:   Admission, refusal, exact-head and permission tests pass and make verify is green.
Appetite:    6 hours for implementation and repairs; stop at the limit.
Not now:     Direct merges, administrative bypass, closing beads or changing required checks.
Pre-mortem:  suppose it failed: most likely because evidence is attributed to the wrong pull request head.
Starts unless you say stop.
```

## Steps and files

1. Implement `scripts/enqueue_pr.py`: read PR metadata, changed paths, the head tree and commit history, the applicable main ruleset and head checks, and validated tracker state; fail closed as specified. Match one trailer to one touched change and read the latest phase-6 block at the head. Enforce the reviewed-commit history rule; compare the script blob to `origin/main`. Send only the pinned `enqueuePullRequest` mutation and classify its result. Implement `--maintainer` with the specified bypasses and retain all other checks; default mode refuses decision PRs. Evaluate dependencies and released loop rows as specified; union all active ruleset and classic protection checks. Fetch `origin/main` and verify first-parent history and clean main merges. Do not treat a self-check as protection from a malicious modified checkout.
2. Update `scripts/stage2.py` to record the actual reviewed commit in each new phase-6 block at the runner's existing verdict writer. Add regression coverage in `tests/test_stage2.py` for the recorded value and its association with the review.
3. Create `tests/test_enqueue_pr.py` using isolated histories and fake GitHub and tracker responses. Exercise every ledger case without a real queue mutation, including main merges, missing data, a moved head, and all fixed output identifiers.
4. After the accepted implementation attempt, the orchestrator owns all held-path edits: update `.claude/settings.json`, `prompts/07-commit.md`, `.github/PULL_REQUEST_TEMPLATE/decision.md`, and `AGENTS.md` for the granted path and existing approval controls; keep `--maintainer` behind attended approval and unattended denial in the agent policy follow-up (bead `coding-harness-r7zc`). Update `docs/WORKFLOW.md` for the same procedure; update `tests/test_merge_guard.py` for the permission regression. Regenerate `plans/INDEX.md` if required by header changes. Do not assign held paths to the implementation attempt.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM through Z.ai was at its weekly limit until 2026-11-29 (research dated 2026-11-25).

## Verification

```sh
python3 -m pytest -q tests/test_enqueue_pr.py tests/test_stage2.py tests/test_merge_guard.py
make verify
```

## Criterion ledger

- 1: tests/test_enqueue_pr.py::test_eligible_head_is_queued — an eligible head is refused.
- 2: tests/test_enqueue_pr.py::test_ineligible_request_is_refused — an ineligible request reaches admission.
- 3: tests/test_enqueue_pr.py::test_latest_phase_six_is_settled — an open or ambiguous review is admitted.
- 4: tests/test_enqueue_pr.py::test_single_open_bead_trailer — an invalid trailer is admitted.
- 5: tests/test_enqueue_pr.py::test_unique_changed_folder_matches_bead — a missing or ambiguous match is admitted.
- 6: tests/test_enqueue_pr.py::test_reviewed_commit_is_ancestor — missing or unrelated review evidence is admitted.
- 7: tests/test_enqueue_pr.py::test_only_allowed_commits_follow_review — a later code change is admitted.
- 8: tests/test_enqueue_pr.py::test_ruleset_checks_on_head — a missing check passes or a permitted conclusion fails.
- 9: tests/test_enqueue_pr.py::test_decision_pr_refused_unattended — a decision PR is admitted in default mode.
- 10: tests/test_enqueue_pr.py::test_unreadable_evidence_refused — an unreadable input reaches admission.
- 11: tests/test_enqueue_pr.py::test_pinned_enqueue_mutation — the call is unpinned or can merge directly.
- 12: tests/test_enqueue_pr.py::test_moved_head_is_not_retried — the command retries or omits the identifier.
- 13: tests/test_stage2.py::test_phase_six_records_reviewed_commit — a verdict omits or misstates the reviewed commit.
- 14: tests/test_enqueue_pr.py::test_admitted_result — admission reports merged or fails.
- 15: tests/test_enqueue_pr.py::test_already_queued_is_idempotent — it admits again or fails.
- 16: tests/test_enqueue_pr.py::test_refusals_report_all_identifiers — a determinable failure is omitted.
- 17: tests/test_enqueue_pr.py::test_usage_and_mutation_failures — either failure returns the wrong status.
- 18: tests/test_enqueue_pr.py::test_modified_script_refuses — an unchanged checker admits a modified blob.
- 19: tests/test_merge_guard.py::test_enqueue_permission_preserves_merge_controls — a direct merge becomes unattended.
- 20: not a test — phase-6 review checks the three documented procedures for the guarded path.

- 21: tests/test_enqueue_pr.py::test_maintainer_mode_bypasses_only_specified_conditions — a bypassed condition blocks or a retained condition is bypassed.
- 22: tests/test_enqueue_pr.py::test_no_finding_requires_unquoted_runner_statement — quoted or absent evidence passes.
- 23: tests/test_enqueue_pr.py::test_released_loop_rows_and_disagreements_refuse — a disputed or unsettled row passes.
- 24: tests/test_enqueue_pr.py::test_required_checks_union — a required check from any applicable source is omitted.

## Do not touch

Do not alter tracker data, required checks, other changes' findings, or perform a real queue admission in tests. Codex and Antigravity policy enforcement remains follow-up work. The implementation attempt must not edit held paths.

## Runner route — 2026-11-25

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-25 14:45:39–14:48:05 UTC, 145 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 15:24:33–15:26:55 UTC, 142 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 16:01:07–16:03:06 UTC, 119 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 17:12:46–17:26:46 UTC, 840 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-25 20:24:34–20:27:42 UTC, 188 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 20:27:58–20:38:35 UTC, 636 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_enqueue_pr.py`, `tests/test_merge_guard.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-26 15:42:11–15:45:54 UTC, 223 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_enqueue_pr.py`, `tests/test_merge_guard.py`, `tests/test_pr_templates.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
