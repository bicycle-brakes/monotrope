---
title: "Plan — triage-where-cell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-3ha6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, triage]
---

# Plan — triage-where-cell

```text
For you:     Triage recognizes bare test filenames and ignores slash-bearing prose when checking locations.
Done when:   The location, column and record-preservation tests pass and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Changing Origin, single-colon symbol locations or repair-scope grants.
Pre-mortem:  suppose it failed: most likely because an ambiguous filename is classified as the wrong file.
Starts unless you say stop.
```

## Build sequence and files

1. Change `scripts/stage2.py`: read Where through `ROW_COLUMNS`; classify tracked paths and unique tracked basenames, including `::test` references, refuse ambiguous basenames without writing, and ignore slash-bearing tokens that do not name tracked paths. Preserve the existing decision and proof safeguards; align command help with the location-based guard.
2. Change `tests/test_stage2.py`: cover bare and suffixed names, ambiguous names, tracked mixed locations, slash-bearing prose and untracked paths, reordered and extended columns, preservation on success and refusal, and matching help text. Update existing strict-reader expectations only where the spec changes them.
3. After accepting the implementation attempt, the **orchestrator** changes held `prompts/04b-review-loop.md`: describe the guard in terms of named locations, retaining the correction and proof ownership; the attempt must not edit this path.

Do not change Origin handling, the single-colon symbol grammar, repair-scope grants, or any other held path. Explore used Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM via Z.ai had reached its weekly limit until 2026-11-29.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_triage_bare_test_locations — a unique bare test file or its test reference escapes the guard.
- 2: not yet written tests/test_stage2.py::test_triage_refuses_ambiguous_bare_filename — an ambiguous name is guessed or refusal changes the record.
- 3: not yet written tests/test_stage2.py::test_triage_ignores_untracked_slash_tokens — an untracked slash token affects classification or refuses.
- 4: not yet written tests/test_stage2.py::test_triage_mixed_tracked_locations — a mixed cell triggers the test-only guard.
- 5: not yet written tests/test_stage2.py::test_triage_reads_where_from_declared_columns — a changed layout makes the guard read another cell.
- 6: tests/test_stage2.py::test_triage_changes_only_the_target_status_and_escapes_pipes_once — another cell changes.
- 6: tests/test_stage2.py::test_triage_refuses_to_redecide_a_row_with_a_proof_mark — triage re-decides a proven row or changes the record on refusal.
- 7: tests/test_stage2.py::test_triage_help_and_instructions_match_the_cli_and_proof_ownership — the help or instructions omit the guard, correction or proof ownership; extend it to hold location-based wording.

## Verification

```sh
make verify
```

Run the targeted `tests/test_stage2.py` triage tests after the implementation and again after the orchestrator's prompt edit; run full verification through `python3 scripts/jobs.py start -- make verify` before phase 6.

## Time used

2026-11-28 04:26:00–04:27:53 UTC, 113 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
