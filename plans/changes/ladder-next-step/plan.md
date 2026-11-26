---
title: "Plan — ladder-next-step"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-24
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — ladder-next-step

```text
For you:     A consumed review ladder names whether to repair or proceed to review and saves that instruction as machine-readable state.
Done when:   Both next steps, their saved instruction and the existing safety stops are tested, and make verify is green.
Appetite:    4 hours of phase 4, including repairs; stop at the limit.
Not now:     Automatically starting the next step or changing the ladder and its restart rules.
Pre-mortem:  suppose it failed: most likely because released history is mistaken for a fresh run.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: add the ledger's regression tests, exercising the CLI exit, both streams and side effects; adapt the existing spent-refusal assertions in `test_the_loop_stops_at_three_rounds`, `test_the_loop_stops_when_the_ladder_ends`, `test_round_history_survives_split_releases_and_config_edits`, and `test_a_failed_flash_member_is_replaced_by_the_cheapest_unconsumed_rung`.
2. `scripts/stage2.py`: in the existing `review_loop` path, reconstruct the same run and distinguish unmarked `taken` rows in every round since the last restart from undecided or unmarked `fixed` rows; preserve all other refusals and the clean and repair-brake stops. For the next-step rule, evaluate unconsumed paid rungs and Flash members against the current declaration admission check, including expired, missing or malformed terms dates, dated skips, exclusions, removed models and unread retention or training terms: an inadmissible rung counts as consumed; a Flash stage remains eligible if any member is admissible or replaceable by an unconsumed admissible rung outside that stage, otherwise it counts as consumed. A cut last round cannot trigger the clean stop even with no accepted findings. Only for an exhausted run with at least one completed post-restart round, return normally after writing exactly the specified `next:` line to stdout; send any existing all-paid-excluded reasons computed from the current declaration to stderr, and name each unconsumed model passed over for failed admission with its reason on stderr. Do not invoke another verb or alter the loop history; publish the next-step state as described below and retain exit 2 for zero-round outages. Keep the unmarked-taken exception limited to this consumed path and preserve non-consumed safeguards.
3. `scripts/next_step_schema.json`: declare a version-1 JSON schema with required fields `schema_version` (integer 1), `change` (nonempty string), `verb` (`review`, `repair`, `hand` or `review-loop`), `row_ids` (array of nonempty strings; nonempty for `hand`, empty otherwise), `producer` (nonempty verb name), and `written_at` (UTC timestamp in RFC 3339 form ending in `Z`); reject unknown fields. `scripts/next_step.py`: supply the one shared validator against that declaration and an atomic state publisher; require real UTC timestamps and reject booleans as schema versions. Use only dependencies available to the existing runner, and expose validation for the later `hand` producer.
4. `scripts/stage2.py`: under the run's existing record lock, remove any prior `next.json` at the start of review-loop processing; on the consumed path build and validate the record, then write a same-directory temporary file and replace the destination before emitting stdout. A validation or publication failure reports an error and exits 1 without the next-step line; deletion failures also fail rather than leaving stale state. On a successful `repair`, publish the same schema with verb `review-loop`, producer `repair`, an empty row list and current UTC time; invalidate the old instruction before a mutation can make it stale. A successful `triage`, `release-loop` (plain, `--stage-failed`, or `--restart`) or phase-6 release deletes it, including when `loop.md` was already released. Serialize instruction and record lifecycle changes with the existing lock, and surface invalidation or publication failures without claiming success. The instruction resides in `record_dir(change, root) / "next.json"`, including the existing `XDG_STATE_HOME` fallback and worktree digest; do not write it to Markdown or add the separate `advance` producer.
5. `tests/test_next_step.py`: test the schema and publisher directly, including all verbs, invalid fields, UTC, replacement failure, and absence of partial publication; `tests/test_stage2.py` exercises integration, output correspondence, isolation by run, all post-restart rounds, and instruction replacement or invalidation on each lifecycle path, including released history.
6. `docs/WORKFLOW.md`: update the phase table, verb exit description and review-loop doctrine with the next steps and the existing fresh verification and independent whole-diff review, preserving restart and other stops.
7. After the accepted implementation attempt, the **orchestrator** edits held paths: `prompts/04b-review-loop.md` describes the next steps and verification sequence; `prompts/02a-spec-review.md` describes the clean and exhausted paths; `prompts/06-review.md` says the loop may finish on a consumed ladder after repair without changing the reviewer's task; `AGENTS.md` rewords its exhausted-ladder bullet as decided in `decisions.md` Q-3. Align the phase tables and loop descriptions in `AGENTS.md`, `docs/WORKFLOW.md`, `prompts/04b-review-loop.md` and `prompts/02a-spec-review.md` so they no longer require a clean round on the exhausted path. The attempt must not edit the held paths.
8. `plans/changes/ladder-next-step/spec.md`, `plans/changes/ladder-next-step/plan.md`, and `plans/changes/ladder-next-step/findings.md` hold the revised yardstick, plan and disposition of the spec-review rows; change them only if review requires it. `plans/INDEX.md`: regenerate through the repository's index writer if artifact headers make it stale.

Do not edit ADRs, model declarations, tracker data, availability policy, `scripts/lanes.py` or other consumers; the ADR 0021 amendment is a separate decision and this change merges after it. Do not start the named verb automatically or change the ladder, restart authority, repair brake, clean-stop exit, night-run wake or phase-6 review task.

## Verification

```sh
.venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/test_stage2.py tests/test_next_step.py
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_spent_ladder_names_review_after_repair — exit or exact stdout differs after all post-restart taken rows are repaired.
- 2: tests/test_stage2.py::test_spent_ladder_names_repair_for_taken_row — a marked or unmarked taken row, including one in an earlier post-restart round, refuses or yields the wrong exit or stdout.
- 3: tests/test_stage2.py::test_spent_ladder_next_step_does_not_start_or_mutate — a reviewer or repair starts or loop history changes; the next-step file is allowed.
- 4: tests/test_stage2.py::test_spent_ladder_next_step_after_release — reconstructed repaired or taken rows in any post-restart round name the wrong action or admit a stage.
- 5: tests/test_stage2.py::test_spent_ladder_preserves_prior_stops — an undecided row, unmarked fixed row, invalid origin or record, clean stop or repair brake is bypassed; non-consumed guards remain in force.
- 6: tests/test_stage2.py::test_spent_ladder_retains_paid_exclusion_reasons — current all-excluded reasons are absent from stderr, appear on stdout, or remain after a declaration edit resolves them.
- 7: tests/test_stage2.py::test_spent_ladder_with_no_completed_round_stops — a total outage exits other than 2 or names a next step.
- 8: tests/test_stage2.py::test_spent_ladder_doctrine_names_next_steps — a named doctrine file omits repair or review, requires escalation solely for exhaustion, or says its loop always ends clean, including phase tables and loop descriptions.
- 9: tests/test_stage2.py::test_spent_ladder_workflow_describes_exit_zero — the workflow says exit 0 always writes a round.
- 10: tests/test_stage2.py::test_spent_ladder_review_prompt_names_exhaustion — the prompt demands a clean round or omits the repaired consumed path.
- 11: tests/test_stage2.py::test_spent_ladder_documents_full_verification_and_review — a documented path omits fresh full verification or independent whole-diff review, including after a cut diff.
- 12: tests/test_stage2.py::test_expired_rungs_count_as_consumed_for_next_step — an inadmissible-only remainder refuses solely on failed admission (including a dated skip, removal or malformed date), a remaining admissible rung yields a next step, or an existing stop is bypassed.
- 13: tests/test_stage2.py::test_flash_eligibility_for_consumed_ladder — an admissible member or an admissible unconsumed replacement rung yields a next step, or a Flash stage whose members and replacement rungs all fail admission prevents the next step when nothing else remains eligible.
- 14: tests/test_stage2.py::test_cut_last_round_with_no_accepted_findings_names_review — an empty or all-rejected cut round ends with a clean stop or refusal rather than exact review output and exit 0.

- 15: tests/test_stage2.py::test_spent_ladder_reports_each_inadmissible_model — an omitted model or reason, or a diagnostic on stdout.

- 16: tests/test_stage2.py::test_spent_ladder_publishes_matching_next_instruction — the file is absent, invalid, in the wrong run directory, or disagrees with stdout.
- 17: tests/test_next_step.py::test_schema_validates_next_instruction — a required or malformed field, unsupported version or verb, or a hand instruction without row ids is accepted, or a valid verb including review-loop is rejected.
- 18: tests/test_stage2.py::test_next_instruction_has_producer_utc_time_and_no_rows — the producer, current UTC time or empty row list is wrong.
- 19: tests/test_next_step.py::test_publisher_validates_and_atomically_replaces — invalid or partial JSON is published or a failed replacement damages the destination.
- 20: tests/test_stage2.py::test_next_instruction_failure_does_not_report_success — validation or publication failure exits other than 1, emits the instruction, or lacks a diagnostic.
- 21: tests/test_stage2.py::test_review_loop_invalidates_previous_instruction — a stale instruction remains after a refusal, new round or clean stop.
- 22: tests/test_stage2.py::test_next_instruction_never_enters_markdown — a Markdown file gains the persisted instruction.
- 23: tests/test_stage2.py::test_successful_repair_publishes_review_loop_instruction — the repair leaves stale state or produces an invalid record, wrong change, verb, producer, time or rows.
- 24: tests/test_stage2.py::test_lifecycle_actions_remove_next_instruction — a successful triage, ordinary release, stage retirement, restart or phase-6 release leaves an instruction, including when the loop record is already released.

## Runner route — 2026-11-25

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Runner route — 2026-11-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-20 14:51:43–14:54:03 UTC, 140 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 01:31:09–01:34:16 UTC, 186 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:33:16–10:36:36 UTC, 200 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:51:24–10:53:15 UTC, 111 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 15:37:51–15:40:37 UTC, 166 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 17:38:34–17:41:31 UTC, 177 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 20:06:40–20:17:32 UTC, 653 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-26 15:24:36–15:48:54 UTC, 1458 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-26 15:49:08–15:49:59 UTC, 51 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-26 15:50:12–16:11:56 UTC, 1304 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
