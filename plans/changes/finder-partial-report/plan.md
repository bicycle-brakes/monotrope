---
title: "Plan — finder-partial-report"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm]
---

# Plan — finder-partial-report

```text
For you:     Valid finder entries survive malformed neighbours, with one shared format and visible gaps.
Done when:   Tests prove schema use, filtering, published gaps, resume and unchanged failure boundaries; make verify passes.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Finder retries, whole-file locators and structured output for all Pi calls.
Pre-mortem:  suppose it failed: most likely because recovery loses a valid entry or hides a dropped one.
Starts unless you say stop.
```

## Files and steps

1. Orchestrator bootstrap before the implementation attempt: create `prompts/research-swarm/finder-locator.schema.json` as the single schema for the four nonempty lists and required nonblank strings; change `prompts/research-swarm/finder.md` to replace its entry-format prose with a reference to the appended schema. Both paths are held and must not be edited by the implementation attempt; the implementation attempt reads these canonical files. Put the exact-symbol-or-section guidance, including the exclusion of line numbers, bare paths and prose, in schema descriptions.
2. Change `scripts/stage2_research_map.py`: read that schema and interpret its supported keywords, refusing unknown keywords; provide strict validation and entry-level filtering, per-entry errors and the fixed empty-after-filter marker. Derive finder outer shape from the schema, check schema categories against merge categories in a test, allow the annotation keywords `description`, `title` and `$schema`, and preserve duplicate-key, outer-shape and exact-union failures. Leave path and reference form to existing merge resolution.
3. Change `scripts/stage2_research_run.py`: append the schema to the shared finder prompt; use `--output-format json --json-schema` for Claude finders only, extract and serialize `structured_output`, load and check the schema before finder calls, failing incomplete with its filename on a missing, malformed or unsupported schema; classify missing output as invalid except for turn, budget or API limits, and classify those limits and nonzero exits as failed. Store the serialized structured output on success; otherwise store only the envelope result text or empty stdout. Filter the first successful answer without retry, persist `ok` plus `filtered`, publish those details without the raw answer in a filtered-success partial fence and in the manifest, and reuse them on resume. Preserve other failure boundaries and exclude rejected entries from map gaps.
4. Change `tests/test_stage2_research_map.py` and `tests/test_stage2_swarm.py`: cover the schema, boundaries, merge, publication and resume with deterministic stand-ins. Change `tests/test_stage2_research_deep_review.py` if needed for the shared prompt.
5. Update this change's `spec.md`, `plan.md` and `findings.md` as work advances. The orchestrator handles held paths, any derived index, commit and pull request.

Explore fallback, 2026-11-19: Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM via Z.ai returned `claude-code:unrecognized_model` (research.md).

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_research_map.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py -q
python3 scripts/check_interview_minimums.py --change finder-partial-report
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py
python3 scripts/plans_registry.py --check
make verify
```

Do not touch model configuration, security checks, topic validation, other prompts, templates or other change folders. The runner owns full verification and the final commit.

## Criterion ledger

- 1: tests/test_stage2_swarm.py::test_finder_claude_enforces_shared_schema — Claude argv lacks or changes the schema.
- 2: tests/test_stage2_swarm.py::test_finder_pi_prompt_contains_shared_schema — Pi receives a different schema.
- 3: tests/test_stage2_research_map.py::test_finder_validation_uses_shared_schema — schema and validation diverge.
- 4: tests/test_stage2_swarm.py::test_finder_first_answer_filters_without_retry — valid entries disappear, invalid entries reach merge or another call occurs.
- 5: tests/test_stage2_research_map.py::test_finder_filter_reports_each_invalid_entry — an entry fault survives or its error is absent.
- 6: tests/test_stage2_research_map.py::test_finder_filter_marks_emptied_category — the fixed marker is missing or wrong.
- 7: tests/test_stage2_swarm.py::test_finder_filtered_gaps_are_published — either publication omits a seat, category, entry or error.
- 8: tests/test_stage2_swarm.py::test_finder_filtered_entries_stay_out_of_map_gaps — a rejected entry becomes map evidence.
- 9: tests/test_stage2_swarm.py::test_finder_filtered_record_is_stored_ok — the outcome or filtered details are wrong.
- 10: tests/test_stage2_swarm.py::test_finder_filtered_record_is_reused_on_resume — resume relaunches or changes the retained answer or gaps.
- 11: tests/test_stage2_swarm.py::test_finder_filtered_merge_preserves_exact_union — an altered locator or origin passes.
- 12: tests/test_stage2_swarm.py::test_finder_invalid_outer_shape_stops — invalid JSON or outer shape reaches merge.
- 13: tests/test_stage2_swarm.py::test_finder_failure_and_refusal_still_stop — a failed or refused call reaches merge.

- 14: tests/test_stage2_swarm.py::test_claude_finder_stores_structured_output — the envelope or result text is stored instead.
- 15: tests/test_stage2_swarm.py::test_claude_finder_missing_structured_output_is_invalid — missing output is accepted or marked failed.
- 16: tests/test_stage2_swarm.py::test_claude_finder_error_result_is_failed — a nonzero exit or a turn, budget or API limit is accepted or marked invalid.
- 17: tests/test_stage2_swarm.py::test_filtered_success_partial_fence_omits_raw_answer — required fields are missing or raw answer is published.
- 18: tests/test_stage2_swarm.py::test_finder_shared_prompt_and_hash_include_schema — prompts or hashes differ or the schema is absent.
- 19: tests/test_stage2_research_map.py::test_finder_schema_rejects_unknown_keyword — an unknown keyword is silently ignored.
- 20: tests/test_stage2_swarm.py::test_non_finder_claude_keeps_text_output — another seat uses JSON output.

- 21: tests/test_stage2_swarm.py::test_claude_finder_stdout_excludes_envelope_on_all_paths — success omits the structured answer, or another path stores more than result text or empty stdout, or any path exposes session or cost.
- 22: tests/test_stage2_research_map.py::test_finder_schema_outer_shape_and_entry_fault_boundary — outer rules are ignored, categories diverge or a fault is misclassified.
- 23: tests/test_stage2_swarm.py::test_invalid_finder_schema_stops_before_calls — a finder runs or the failure omits the schema filename.
- 24: tests/test_stage2_research_map.py::test_finder_schema_annotations_and_reference_guidance — annotations are rejected or enforced or reference guidance is absent.
- 25: tests/test_stage2_research_map.py::test_finder_field_form_is_resolved_at_merge — a form-only issue is filtered or bypasses merge resolution.
- 26: tests/test_stage2_swarm.py::test_finder_old_claude_stops_before_calls — an unsupported Claude Code version reaches a finder call or the incomplete reason omits the versions.

## Runner route — 2026-11-19

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-20

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-20

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-19 14:42:57–14:44:52 UTC, 114 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 14:55:55–14:57:56 UTC, 121 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 15:04:46–15:06:29 UTC, 103 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 15:21:12–15:22:37 UTC, 85 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 16:17:52–17:06:28 UTC, 2916 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-19 17:06:40–17:21:10 UTC, 871 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-19 17:21:19–17:25:50 UTC, 271 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 17:28–18:32 UTC, 64 min — implement · orchestrator hand finishing (Opus subagent): fixture fault behind the one red targeted test (a substituted Pi finder seat had no scenario step), the schema's `minItems` enforced by the filter, a ruff-format line, two full `make verify` runs (the first red at `ruff-format`, the second green: 6367 passed, 17 skipped at 9f6c09ab) · measured by hand from commit and run timestamps; about 34 min of it was the wait for the shared verify lock
2026-11-19 21:47:30–23:07:19 UTC, 4789 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-20 06:33:26–08:52:19 UTC, 8333 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-20 10:27:08–12:01:09 UTC, 5640 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 12:01:18–12:11:54 UTC, 636 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 12:12:03–12:20:53 UTC, 531 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-20 12:35–13:25 UTC, 50 min — repair · round 3 · orchestrator hand finishing (Opus subagent) after the runner's red-first check refused three attempts: rows L3-1..L3-9 completed from the attempts' tree (L3-2 limit subtypes taken from the documented SDKResultMessage type, L3-3 the `--json-schema` minimum declared with version, date and sources), every new test red by hand against the HEAD versions of both changed scripts, origin/main merged without conflict (d928ff2d), targeted 484 passed, full `make verify` green: 6502 passed, 17 skipped at d928ff2d · measured by hand from commit and run timestamps; about 18 min of it was the wait for the shared verify lock
2026-11-20 13:38:37–13:46:13 UTC, 456 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 13:46:25–13:47:56 UTC, 91 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 13:48:09–13:54:50 UTC, 401 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-20 16:51:20–17:55:05 UTC, 3825 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-20 21:02:59–23:30:40 UTC, 8861 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-20 23:53:45–2026-11-21 00:03:28 UTC, 584 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-21 00:03:42–01:45:17 UTC, 6095 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-21 11:30:50–11:36:30 UTC, 339 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-21 12:01:08–12:07:05 UTC, 358 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
