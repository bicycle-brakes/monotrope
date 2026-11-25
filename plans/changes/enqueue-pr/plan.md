---
title: "Plan — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
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

The card is provisional: phase 4 is held by the open decision in `spec.md` and the spec-review gate.

## Steps and files

1. Create `scripts/enqueue_pr.py`: accept a PR number, resolve the repository, open state, base and exact head from GitHub, then read findings and the head commit trailer from that head rather than the local working tree. Resolve exactly one change and its newest phase-6 verdict; recognize explicit no-findings and settled rows, reject absent, ambiguous, unrecognized or open evidence. Resolve the actual required checks and enabled queue from repository protection and the results on that exact head; reject empty, incomplete, pending, non-successful or unreadable data. Render and validate tracker state through `scripts/bead_render.py`; match the existing bead exactly. Refuse any unsuccessful read and report its condition. Run `gh pr merge <number> --merge --match-head-commit <head>` only after all checks and queue confirmation, without `--admin`; propagate failure and report queued only upon successful admission. Resolve the decision-PR question before implementing that branch.
2. Create `tests/test_enqueue_pr.py`: use isolated Git histories and fake GitHub and tracker responses to verify every ledger case, including multiple reviews, wrong-head findings and checks, absent queue, changed head, failures of each reader and exact arguments; do not contact GitHub or enqueue a real PR.
3. The orchestrator owns held paths after the accepted implementation attempt: change `.claude/settings.json` to allow the guarded script while preserving direct-merge ask and night deny; update `prompts/07-commit.md` and `AGENTS.md` only to reflect the established grant and chosen decision-PR answer. Update `docs/WORKFLOW.md` for the same queue procedure. Locate the actual repository-owned Codex and Antigravity policies before editing: their paths were not found in phase 1, so stop and report if they cannot be identified inside this worktree; do not invent an external configuration or claim harness coverage. Add policy regressions in `tests/test_merge_guard.py` and `tests/test_enqueue_pr.py` for all three harnesses when their actual policy paths are known. The orchestrator regenerates `plans/INDEX.md` if required by the artifact headers. No other paths are assigned to the implementation attempt.
4. Run the commands below after the orchestrator's held-path edits; phase 6 checks the actual grant and the policy coverage. No design or ADR is due for this bounded change.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM through Z.ai was at its weekly limit until 2026-11-29 (research dated 2026-11-25).

## Verification

```sh
python3 -m pytest -q tests/test_enqueue_pr.py tests/test_merge_guard.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_enqueue_pr.py::test_eligible_head_is_queued — a fully eligible head is refused or not queued.
- 2: not yet written tests/test_enqueue_pr.py::test_closed_or_wrong_base_is_refused — a closed or non-main request reaches merge.
- 3: not yet written tests/test_enqueue_pr.py::test_newest_phase_six_must_be_settled — an open latest row is admitted.
- 4: not yet written tests/test_enqueue_pr.py::test_each_required_check_succeeded_on_head — a missing, pending or unsuccessful required result is admitted.
- 5: not yet written tests/test_enqueue_pr.py::test_head_trailer_names_existing_bead — a missing or unknown declaration is admitted.
- 6: not yet written tests/test_enqueue_pr.py::test_missing_ambiguous_or_stale_evidence_is_refused — an unreadable, ambiguous or wrong-head input, or missing queue, reaches merge.
- 7: not yet written tests/test_enqueue_pr.py::test_head_change_refuses_admission — the changed head is admitted using old evidence.
- 8: not yet written tests/test_enqueue_pr.py::test_only_pinned_queue_admission_is_issued — merge arguments omit the head or permit an administrative or direct merge.
- 9: not yet written tests/test_enqueue_pr.py::test_refusals_name_failed_condition — a refusal does not identify the failing prerequisite.
- 10: not yet written tests/test_enqueue_pr.py::test_success_reports_queued — admission reports a completed merge.
- 11: not yet written tests/test_enqueue_pr.py::test_harness_policies_allow_only_guarded_admission — any harness disallows the guarded path or allows unattended direct merge.

## Do not touch

Do not alter tracker data, required checks, unrelated changes' reviews, or execute a real merge in tests. The implementation attempt must not edit any held path; the orchestrator owns those edits.

## Time used

2026-11-25 14:45:39–14:48:05 UTC, 145 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
