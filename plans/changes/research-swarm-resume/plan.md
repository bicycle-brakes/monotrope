---
title: "Plan — research-swarm-resume"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-f6qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm, resume]
---

# Plan — research-swarm-resume

```text
For you:     Finished repository research survives a failed seat and is reused on resume.
Done when:   A two-run regression proves stable prompts and selective reuse; reuse guards and make verify pass.
Appetite:    4 hours of phase 4 including repairs; stop at the limit.
Not now:     Changes to model routing, security checks or the existing reuse contract.
Pre-mortem:  suppose it failed: most likely because the test misses the input that changes between real runs.
Starts unless you say stop.
```

## Files and steps

1. Change `tests/test_stage2_swarm.py`: extend the deterministic two-run swarm fixture with a repository locator into research content affected by publication, capture actual prompts and launches across both runs, fail one repository seat on run one, and assert all eight topic prompts, the other successful repository seats and the failed seat's retry. Exercise the real publication and resume path rather than substituting equal prompts.
2. Change `scripts/stage2_research_run.py`: trace every input to `repository_prompt`, including the finder map's resolved excerpts and mapped history, against the stored frozen binding and reproduced drift; correct the input at its common source so matching resumes reconstruct identical prompts while real input changes still invalidate reuse. Keep map, history, publication and security semantics intact; do not weaken `plan_reuse` or its validation.
3. Change `tests/test_stage2_research_store.py`: add a focused boundary regression if existing tests do not cover the corrected input's drift; retain the existing binding, identity, prompt-hash and invalid-result tests. Update this change's `findings.md` as reviews require.
4. If diagnosis locates the source in `scripts/stage2_research_map.py`, `scripts/stage2_research_snapshot.py` or `scripts/stage2_research_history.py`, change only the responsible file at the shared input boundary and cover it in `tests/test_stage2_research_deep_review.py`; otherwise leave those files untouched. The orchestrator owns any held-path edits; none are planned.

Explore fallback, 2026-11-26: Stage 1 through `claude-code-plan`, model `claude-haiku-5-5`, because GLM through Z.ai was at its weekly limit (`research.md`).

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_swarm.py tests/test_stage2_research_store.py tests/test_stage2_research_deep_review.py -q
python3 scripts/check_interview_minimums.py --change research-swarm-resume
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
python3 scripts/jobs.py start -- make verify
```

The orchestrator checks the detached verification job's exit before phase 6. Do not touch model configuration, leak checks, availability, prompts, templates, other changes or the existing reuse contract.

## Criterion ledger

- 1: tests/test_stage2_swarm.py::test_repository_prompts_stay_stable_across_published_resume — any corresponding prompt changes after the first publication.
- 2: tests/test_stage2_swarm.py::test_repository_resume_reuses_all_successful_seats — a successful seat is relaunched or its result is not adopted.
- 3: tests/test_stage2_swarm.py::test_a_resumed_run_is_a_new_run_within_its_slot_budget — the failed seat is reused or not relaunched.
- 4: tests/test_stage2_research_store.py::test_reuse_requires_the_exact_binding_seat_model_and_prompt — a mismatched binding, identity or prompt is reused.
- 4: tests/test_stage2_research_store.py::test_interrupted_and_invalid_results_are_not_reused_and_are_named — an invalid result is adopted.
- 5: tests/test_stage2_swarm.py::test_repository_prompts_preserve_mapped_excerpts_and_history — resolved finder-map `extent`/`excerpt_sha256` or topic-6 `# Mapped history (data)` are omitted, blanked, or disagree with validation across a three-run chain.

## Runner route — 2026-11-26

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-26 19:58:35–20:01:28 UTC, 173 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-26 21:12:30–21:28:38 UTC, 968 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_check_criterion_ledger.py`, `tests/test_check_interview_minimums.py`, `tests/test_check_question_context.py`, `tests/test_explorer_reviewer_agents.py`, `tests/test_frontmatter_current.py`, `tests/test_leakcheck.py`, `tests/test_model_endpoints.py`, `tests/test_outcome_test.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_fail_fast.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_session.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`, `tests/test_templates.py`, `tests/test_workflow_entry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-27 02:11:25–02:22:08 UTC, 643 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_judge.py`, `tests/test_stage2_research_report.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-27 03:40:14–03:53:34 UTC, 800 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-27 05:10:21–05:16:11 UTC, 351 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-27 05:16:25–05:22:14 UTC, 349 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-27 06:40:24–06:47:08 UTC, 404 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-27 08:11:16–08:16:45 UTC, 330 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-27 08:16:59–08:23:02 UTC, 363 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-27 10:39:54–10:46:56 UTC, 423 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
