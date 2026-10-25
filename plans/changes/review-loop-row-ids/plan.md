---
title: "Plan — review-loop-row-ids"
status: draft
implementation_status: partial
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-6jg
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, review-loop]
---

# Plan — review-loop-row-ids

```text
For you:     Unreadable finding tables stop the review round and show which member and lines need attention.
Done when:   Refusal, diagnostics, same-stage retry and compatibility regressions pass, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Mixed readable/non-row answers, old records, reviewer-id rules or model routing changes.
Pre-mortem:  suppose it failed: most likely because the paid replacement path still treats malformed output as a call failure.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–7 of `spec.md`; the class stays bounded, with no design
or ADR. The runner owns verification and commits; this draft implements no
code. The orchestrator shows the card unchanged before phase 4.

Explore fallback (2026-10-20): route `stage-1`, endpoint `claude-code-plan`,
model `claude-haiku-5-5`, reason `GLM unavailable until 2026-10-21T20:34+08:00`.
That call produced no research; the orchestrator (Opus 5.5) instead read the
code at `105c270`, as recorded in research. Before the cutoff use active Sol
6.1 for implementation while Claude budget is exhausted; launch no Z.ai GLM.

## Build sequence

1. Add a distinct `CallFailed` subtype for malformed table answers, carrying
   the offending lines from the already scrubbed answer. In `run_swarm`,
   use `parse_rows` unchanged: only zero readable rows plus a `split_row`
   match in its retained text raises this subtype. Preserve the existing
   generic failure for other non-row answers and the exact `No finding.`
   success rule. Do not guess at ids or tighten valid-row parsing.
2. In `review_loop`, check the collected initial outcomes for this subtype
   before paid replacement starts; fail with all malformed members and
   their lines. Check each replacement outcome immediately as well. Use
   the existing exit-1 failure path; do not append a round, write a snapshot
   or call `mark_consumed`. Keep audit lines for calls already made. Leave
   `clean_round`, ordinary replacement and valid-row numbering unchanged.
3. Use `World`, `world.script`, `loop_state` and `_flash_round_world` for
   red-first regressions. Cover free/paid swarms and a single rung; peers
   return either rows or `No finding.`. Check several malformed members,
   multiple lines, original ids and credential scrubbing. Compare record
   bytes and released snapshots before/after refusal, then rerun and assert
   the same models and round number. In paid cases include another initial
   transport failure and a malformed replacement, asserting no next call.
4. Update the malformed-table partial-success expectation in the existing
   test, retaining its top-level name for its older ledger. Keep generic
   prose-failure expectations unchanged. Add arbitrary-id row controls and
   parameterize ordinary-failure controls over exit, timeout and empty
   output. Replace each ledger's `not yet written` marker when implemented.

## Files

- `scripts/stage2.py`: distinguish malformed table output and refuse before replacement or completed-round persistence.
- `tests/test_stage2.py`: add the new regressions and adjust the existing malformed-table expectation without renaming ledger-referenced tests.
- `plans/changes/review-loop-row-ids/spec.md`: create the contract and later update implementation metadata.
- `plans/changes/review-loop-row-ids/plan.md`: create this plan, then update ledger markers and measured phase-4 time.
- `plans/changes/review-loop-row-ids/research.md`: append the dated checks that resolve persistence and replacement gaps.
- `plans/changes/review-loop-row-ids/findings.md`: preserve prior evidence; the runner adds call and review records.
- `plans/INDEX.md`: runner-generated registry update only; this draft does not edit it.

No files are deleted. Do not touch ADRs, other changes, decisions, prompts,
the shared parser, completed records, configuration, tracker data or gates.

## Verification

```sh
python3 scripts/check_interview_minimums.py --change review-loop-row-ids
python3 scripts/check_criterion_ledger.py
.venv/bin/python -m pytest tests/test_stage2.py -q
make verify
```

Use the worktree's initialized environment. The earlier failed attempts
reported missing pinned Pi; the runner must satisfy that prerequisite for
full verification, never skip its contracts or change a gate to pass.
`scripts/validate_change_artefacts.py` and `templates/plan.md` do not exist
at `82488fc`; use the available gates and the phase-3 prompt's plan form.

## Criterion ledger

- 1: tests/test_stage2.py::test_malformed_table_refuses_the_whole_round — a malformed member beside clean or readable peers completes any stage.
- 2: tests/test_stage2.py::test_malformed_table_refusal_names_scrubbed_member_lines — any affected member or line vanishes, ids change, or a credential leaks.
- 3: tests/test_stage2.py::test_malformed_table_refusal_preserves_round_state — refusal creates a record or changes existing/released completion state.
- 4: tests/test_stage2.py::test_malformed_table_retry_uses_the_same_stage — retry skips models or advances the round number.
- 5: tests/test_stage2.py::test_malformed_flash_answer_stops_before_replacement — an initial malformed member permits any replacement call.
- 5: tests/test_stage2.py::test_malformed_replacement_stops_the_paid_round — a malformed replacement permits the next ladder call.
- 6: tests/test_stage2.py::test_a_round_is_written_as_its_rung — arbitrary reviewer ids lose rows, collide or change attribution.
- 6: tests/test_stage2.py::test_colliding_reviewer_ids_keep_their_rows_and_attribution — two members' identical `R2-1` ids collide, lose a row or change attribution.
- 6: tests/test_stage2.py::test_parse_rows_folds_a_pipe_inside_the_finding_into_it — valid finding-cell pipes become malformed output.
- 7: tests/test_stage2.py::test_a_failed_swarm_member_preserves_successful_answers — ordinary member failure erases successful rows.
- 7: tests/test_stage2.py::test_a_failed_flash_member_is_replaced_by_the_cheapest_unconsumed_rung — an ordinary failure prevents its eligible replacement.
- 7: tests/test_stage2.py::test_ordinary_call_failures_keep_partial_and_replacement_rules — timeout or empty output is wrongly classified as malformed table output.

## Time used
2026-10-25 11:09:56–11:14:31 UTC, 275 s — implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
