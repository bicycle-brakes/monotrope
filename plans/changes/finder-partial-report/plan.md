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
For you:     A malformed finder report gets one correction; valid entries survive a second malformed answer.
Done when:   Tests prove correction, retained entries, visible gaps and unchanged failure boundaries; make verify passes.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Whole-file locators, finder selection and changes to other research stages.
Pre-mortem:  suppose it failed: most likely because recovery loses a valid entry or hides a dropped one.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2_research_map.py`: expose entry-level recovery for a readable object with exactly the four lists, using the same entry rules as strict validation; retain each valid entry, capture each rejected entry with category and exact error, and use an explicit unread marker for a category emptied by filtering. Keep strict validation and exact-union semantics for normal inputs.
2. Change `scripts/stage2_research_run.py`: capture the actual validation exception; request one correction from the same seat using the existing dispatch, security, budget and state machinery. Preserve attempts as data; use a valid correction directly or the recovered second report for the logical finder seat, record each dropped entry as a published gap, and feed the resulting three reports to the unchanged exact-union check. Do not recover unreadable outer structure, failed calls or refusals. Ensure interruption and resume do not silently lose the gap or exceed the one-correction limit.
3. Change `tests/test_stage2_research_map.py` to exercise mixed entries, existing validity rules, empty-after-filter categories and invalid outer structure. Change `tests/test_stage2_swarm.py` to exercise real runner correction, the merge input and published gap, failures, refusal and resume with deterministic stand-ins. Check successful first answers and strict merge rejection remain unchanged.
4. Update this change's `spec.md` and `plan.md` implementation status, ledger entries and time as work advances. The orchestrator handles derived index regeneration, commits and pull request. No held path is assigned to the implementation attempt.

Explore fallback, 2026-11-19: Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM via Z.ai returned `claude-code:unrecognized_model` (research.md).

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_research_map.py tests/test_stage2_swarm.py -q
python3 scripts/check_interview_minimums.py --change finder-partial-report
python3 scripts/validate_change_artefacts.py --check
make verify
```

Do not touch model configuration, security checks, topic validation, prompts, templates or other change folders. The runner owns full verification and the final commit.

## Criterion ledger

- 1: not yet written tests/test_stage2_swarm.py::test_finder_correction_receives_exact_error_once — the wrong error, seat or extra correction is sent.
- 2: not yet written tests/test_stage2_swarm.py::test_finder_valid_correction_reaches_merge — the merge sees the rejected original instead.
- 3: not yet written tests/test_stage2_swarm.py::test_finder_partial_correction_reaches_merge — a valid entry disappears, an invalid entry passes, or the merge stops.
- 3: not yet written tests/test_stage2_research_map.py::test_finder_recovery_filters_entries — recovery drops valid entries or retains malformed ones.
- 4: not yet written tests/test_stage2_swarm.py::test_finder_partial_gap_is_published_and_resumed — a dropped entry, seat, category or error is absent after publication or resume.
- 5: not yet written tests/test_stage2_research_map.py::test_finder_recovery_preserves_locator_rules — a locator without a path or exact reference is retained.
- 6: not yet written tests/test_stage2_swarm.py::test_finder_partial_merge_preserves_exact_union — an altered retained locator or origin passes the merge check.
- 7: not yet written tests/test_stage2_swarm.py::test_finder_unrecoverable_correction_stops — an unreadable report, failed call or refusal reaches merge.

## Time used

2026-11-19 14:42:57–14:44:52 UTC, 114 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
