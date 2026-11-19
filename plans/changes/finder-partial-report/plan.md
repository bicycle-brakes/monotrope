---
title: "Plan — finder-partial-report"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
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

1. Change `scripts/stage2_research_map.py`: define one JSON Schema for the existing four nonempty lists and entry rules; use it for strict validation and entry-level filtering, preserving duplicate-key and outer-shape failures, per-entry errors and the fixed empty-after-filter marker in the spec. Keep exact-union validation unchanged.
2. Change `scripts/stage2_research_run.py`: pass that schema to Claude finder calls and embed it in Pi finder prompts; correctly extract Claude's schema-enforced response through the existing payload path. Filter the first successful answer before merge without a retry, persist `ok` plus `filtered` details, publish them in the manifest and a partial fence, and reuse them on resume. Preserve failure and refusal handling and ensure filtered entries do not enter map gaps.
3. Change `tests/test_stage2_research_map.py` and `tests/test_stage2_swarm.py`: test the schema, boundaries, merge, publication and resume with deterministic stand-ins, including mixed faults and all-invalid categories. Change `tests/test_stage2_research_deep_review.py` if needed to hold finder prompt separation when the schema is included.
4. Update this change's `spec.md`, `plan.md` and `findings.md` as work advances. No held path is assigned to the implementation attempt; the orchestrator handles any derived index, commit and pull request.

Explore fallback, 2026-11-19: Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM via Z.ai returned `claude-code:unrecognized_model` (research.md).

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_research_map.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py -q
python3 scripts/check_interview_minimums.py --change finder-partial-report
python3 scripts/validate_change_artefacts.py --check
make verify
```

Do not touch model configuration, security checks, topic validation, prompts, templates or other change folders. The runner owns full verification and the final commit.

## Criterion ledger

- 1: not yet written tests/test_stage2_swarm.py::test_finder_claude_enforces_shared_schema — Claude argv lacks or changes the schema.
- 2: not yet written tests/test_stage2_swarm.py::test_finder_pi_prompt_contains_shared_schema — Pi receives a different schema.
- 3: not yet written tests/test_stage2_research_map.py::test_finder_validation_uses_shared_schema — schema and validation diverge.
- 4: not yet written tests/test_stage2_swarm.py::test_finder_first_answer_filters_without_retry — valid entries disappear, invalid entries reach merge or another call occurs.
- 5: not yet written tests/test_stage2_research_map.py::test_finder_filter_reports_each_invalid_entry — an entry fault survives or its error is absent.
- 6: not yet written tests/test_stage2_research_map.py::test_finder_filter_marks_emptied_category — the fixed marker is missing or wrong.
- 7: not yet written tests/test_stage2_swarm.py::test_finder_filtered_gaps_are_published — either publication omits a seat, category, entry or error.
- 8: not yet written tests/test_stage2_swarm.py::test_finder_filtered_entries_stay_out_of_map_gaps — a rejected entry becomes map evidence.
- 9: not yet written tests/test_stage2_swarm.py::test_finder_filtered_record_is_stored_ok — the outcome or filtered details are wrong.
- 10: not yet written tests/test_stage2_swarm.py::test_finder_filtered_record_is_reused_on_resume — resume relaunches or changes the retained answer or gaps.
- 11: not yet written tests/test_stage2_swarm.py::test_finder_filtered_merge_preserves_exact_union — an altered locator or origin passes.
- 12: not yet written tests/test_stage2_swarm.py::test_finder_invalid_outer_shape_stops — invalid JSON or outer shape reaches merge.
- 13: not yet written tests/test_stage2_swarm.py::test_finder_failure_and_refusal_still_stop — a failed or refused call reaches merge.

## Time used

2026-11-19 14:42:57–14:44:52 UTC, 114 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 14:55:55–14:57:56 UTC, 121 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
