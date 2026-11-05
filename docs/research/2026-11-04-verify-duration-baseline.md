---
title: "make verify baseline — five serial runs on bc2fe411, and a warning-budget proposal"
category: research
created: 2026-11-05
updated: 2026-11-05
last_reviewed: 2026-11-05
owner: framework-architect
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-1um6
tags: [verify, duration, baseline, spike, measurement]
---

# make verify baseline

**Result: a full local `make verify` took 1,215–1,261 s of execution on one
clean revision (median 1,223 s, about 20.4 minutes; five green runs,
2026-11-05). The pytest gate is 81 % of it and the kit probe (`leerprobe`)
16 %; everything else together is under 3 %.** Waiting at the machine-wide
verify lock is a separate quantity and varied from 2 s to 1,254 s in the
same five runs. Proposal: warn when execution exceeds **1,400 s**.

## How it was measured

- Revision `bc2fe411` of branch `spike/verify-duration`, clean tree (`dirty:
  false` in every record), the instrumentation this change adds.
- Command, five times serially, through ordinary lock admission (no bypass):
  `PYTEST_ADDOPTS=--durations=30 PYTHON=.venv/bin/python3 make verify`.
- Same job (`verify`), placement (`local`), gate configuration
  (`config_sha256` prefix `afaec60c0743`) and worker setting (4 configured).
  The actually started worker count is not printed in the retained output —
  not read.
- Source: the run records in `~/.local/state/coding-harness/verify-duration.jsonl`
  (`run_start`, `gate`, `run_end` events) and each run's stdout for the
  30 slowest pytest durations. No foreign model call.
- Other lanes were running on the same machine (review loops, repairs); the
  lock admits one verification at a time, so no two full runs overlapped, but
  model calls and editors did. Free memory at admission: 55–67 %.

## The five runs

| Run | Admitted (UTC) | Execution s | pytest s | leerprobe s | Lock wait s | Free memory % | Workers |
|---|---|---|---|---|---|---|---|
| 765c156b | 2026-11-05T00:08:32Z | 1261 | 1031 | 194 | 960 | 61 | 4 |
| c695e555 | 2026-11-05T00:49:21Z | 1218 | 981 | 200 | 1188 | 55 | 4 |
| 0864a0f1 | 2026-11-05T01:30:34Z | 1215 | 984 | 195 | 1254 | 59 | 4 |
| 414ab592 | 2026-11-05T01:50:55Z | 1233 | 999 | 198 | 5 | 66 | 4 |
| 4d648f85 | 2026-11-05T02:11:30Z | 1223 | 991 | 196 | 2 | 67 | 4 |

All five ended green; none was excluded (no failed, incomplete or dirty run).
Range of execution: 46 s (3.8 % of the median).

## Where the time goes

Median seconds per gate over the five runs (20 gates):

| Gate | Median s | Range s | Share of median run |
|---|---|---|---|
| pytest | 991 | 981–1031 | 81 % |
| leerprobe (kit probe) | 196 | 194–200 | 16 % |
| markdownlint | 10 | 10–10 | 1 % |
| ruleset | 9 | 9–9 | 1 % |
| frontmatter-current | 6 | 6–6 | <1 % |
| the other 15 gates | ≤ 2 each | — | <1 % together |

Slowest single tests (call phase, median over the runs that listed them;
every one below appeared in all five unless noted):

| s | Test |
|---|---|
| 26.3 | `tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours` |
| 24.8 | `tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps` |
| 20.5 | `tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts` |
| 19.9 | `tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons` |
| 16.2 | `tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection` |
| 15.7 | `tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence` |
| 15.0 | `tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims` |
| 13.8 | `tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence` |
| 13.8 | `tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing` |
| 13.6 | `tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map` |
| 13.5 | `tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected` |
| 13.5 (4 of 5) | `tests/test_stage2_swarm.py::test_only_the_runner_appends_research` |

Eleven of the twelve slowest tests are research-swarm tests. The first run's
pytest suite reported 4,710 passed and 17 skipped in 1,030.87 s.

## Warning-budget proposal

Warn when one run's **execution** (lock wait excluded) exceeds **1,400 s**:
the median 1,223 s plus about 15 %. The margin is four times the observed
spread (3.8 %), because these five runs come from one night on one machine
with other lanes active, and a quieter or busier machine was not measured.
The budget is a warning, not a timeout: this note makes no speed-up claim and
changes no timeout.

The lock wait needs its own reading: on this night it was up to 1,254 s
(about 21 minutes), as long as a run itself — the dominant cost for a lane
was queueing, not execution.

## Limits

- One night, one machine, one revision; five runs. Variance across machines,
  times of day and a quiet machine is not measured.
- Each gate reading includes the start of a small helper interpreter
  (`python -m scripts.verify_duration clock`), estimated at 0.1–0.3 s per
  reading (review-loop row L2-2, not measured here) — below the precision of
  the table.
- **Open against the Definition of Done:** the actually started pytest worker
  count. Under `-q` pytest prints only "bringing up nodes..." (all five logs
  read, 2026-11-05); only the configured setting 4 is recorded. Named open by
  the maintainer's decision (2026-11-05); follow-up bead coding-harness-xay1.

## Appendix — each run's 30 slowest durations

Copied from the pytest gate's output of each run (`--durations=30`), unchanged; the ruleset gate's own pytest call prints a second, shorter list, not copied.

### Run 765c156b

```text
26.19s call     tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours
24.42s call     tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
19.94s call     tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
19.76s call     tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts
16.14s call     tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection
15.68s call     tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence
15.02s call     tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims
13.98s call     tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits
13.81s call     tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing
13.54s call     tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected
12.88s call     tests/test_stage2_research_deep_review.py::test_a_tight_judge_limit_is_announced_before_any_topic_call
12.81s call     tests/test_stage2_research_deep_review.py::test_an_unresolved_claim_outside_every_disagreement_fails_the_judge
12.75s call     tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map
12.49s call     tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence
12.20s call     tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim
11.08s call     tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
11.01s call     tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits
10.47s call     tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required
10.26s call     tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins
10.23s call     tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
10.15s call     tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits
10.08s call     tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
9.78s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[fail]
9.28s call     tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[spec-both]
8.92s call     tests/test_stage2_swarm.py::test_a_receipt_without_output_survives_a_complete_run
8.83s call     tests/test_stage2_swarm.py::test_free_seats_are_forbidden_in_every_private_role
8.70s call     tests/test_ci.py::test_runner_report_matches_selected_job
8.70s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[skip]
8.67s call     tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes
8.63s call     tests/test_stage2_swarm.py::test_selected_free_models_cover_all_online_topics_on_identical_briefs
```

### Run c695e555

```text
34.82s call     tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours
27.81s call     tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
25.47s call     tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
20.64s call     tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence
20.48s call     tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts
20.41s call     tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims
17.07s call     tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection
14.34s call     tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits
14.32s call     tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected
13.83s call     tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence
13.78s call     tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
13.66s call     tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required
13.64s call     tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map
13.62s call     tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim
12.74s call     tests/test_stage2_research_deep_review.py::test_a_tight_judge_limit_is_announced_before_any_topic_call
12.53s call     tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits
12.42s call     tests/test_stage2_research_deep_review.py::test_an_unresolved_claim_outside_every_disagreement_fails_the_judge
11.13s call     tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
10.32s call     tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins
10.31s call     tests/test_stage2_swarm.py::test_only_the_runner_appends_research
10.24s call     tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits
10.16s call     tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
9.91s call     tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing
9.10s call     tests/test_stage2_swarm.py::test_a_receipt_without_output_survives_a_complete_run
9.01s call     tests/test_stage2_swarm.py::test_provider_limit_is_shared_across_topics_and_roles
8.89s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[skip]
8.86s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[fail]
8.72s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[xfail]
8.60s call     tests/test_stage2_swarm.py::test_free_seats_are_forbidden_in_every_private_role
8.44s call     tests/test_stage2_swarm.py::test_online_requests_exclude_private_inputs_and_ambient_paths
```

### Run 0864a0f1

```text
36.79s call     tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours
25.05s call     tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
24.84s call     tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
21.82s call     tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence
21.30s call     tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts
20.96s call     tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims
17.07s call     tests/test_stage2_research_deep_review.py::test_a_tight_judge_limit_is_announced_before_any_topic_call
16.36s call     tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection
14.63s call     tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required
14.56s call     tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map
14.12s call     tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected
14.02s call     tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits
14.00s call     tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence
13.58s call     tests/test_stage2_swarm.py::test_only_the_runner_appends_research
13.32s call     tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim
12.82s call     tests/test_stage2_research_deep_review.py::test_an_unresolved_claim_outside_every_disagreement_fails_the_judge
12.35s call     tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits
12.14s call     tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits
11.25s call     tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
11.02s call     tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
10.56s call     tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
9.44s call     tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins
9.24s call     tests/test_stage2_swarm.py::test_a_receipt_without_output_survives_a_complete_run
8.93s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[fail]
8.88s call     tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing
8.84s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[xfail]
8.82s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[skip]
8.81s call     tests/test_stage2.py::test_repair_prose_alone_still_needs_fixed_lines
8.75s call     tests/test_stage2_swarm.py::test_provider_limit_is_shared_across_topics_and_roles
8.71s call     tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes
```

### Run 414ab592

```text
24.75s call     tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
24.57s call     tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours
20.23s call     tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts
19.78s call     tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
15.77s call     tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection
14.91s call     tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims
14.65s call     tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence
14.02s call     tests/test_stage2_swarm.py::test_only_the_runner_appends_research
13.83s call     tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing
13.77s call     tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map
13.53s call     tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence
13.40s call     tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits
12.76s call     tests/test_stage2_research_deep_review.py::test_a_tight_judge_limit_is_announced_before_any_topic_call
12.74s call     tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim
12.38s call     tests/test_stage2_research_deep_review.py::test_an_unresolved_claim_outside_every_disagreement_fails_the_judge
11.13s call     tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
10.98s call     tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits
10.67s call     tests/test_stage2_research_deep_review.py::test_a_pi_answer_without_its_measured_model_is_a_failed_slot
10.61s call     tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
10.47s call     tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures
10.17s call     tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required
10.13s call     tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits
10.01s call     tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected
9.94s call     tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
9.80s call     tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins
9.20s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[xfail]
9.02s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[fail]
8.83s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[skip]
8.64s call     tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes
8.43s call     tests/test_stage2_swarm.py::test_required_slots_are_dispatched_before_any_free_slot
```

### Run 4d648f85

```text
26.27s call     tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours
24.71s call     tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
21.26s call     tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts
19.62s call     tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
16.25s call     tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection
15.56s call     tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence
14.81s call     tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims
13.89s call     tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence
13.77s call     tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing
13.46s call     tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits
13.45s call     tests/test_stage2_swarm.py::test_only_the_runner_appends_research
13.42s call     tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map
13.13s call     tests/test_stage2_research_deep_review.py::test_a_tight_judge_limit_is_announced_before_any_topic_call
12.60s call     tests/test_stage2_research_deep_review.py::test_an_unresolved_claim_outside_every_disagreement_fails_the_judge
11.10s call     tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
11.07s call     tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim
10.77s call     tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
10.62s call     tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected
10.46s call     tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits
10.39s call     tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
10.27s call     tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits
10.16s call     tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required
10.01s call     tests/test_stage2_research_deep_review.py::test_an_empty_neighbour_packet_always_names_its_gap
9.70s call     tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins
8.83s call     tests/test_stage2_swarm.py::test_online_requests_exclude_private_inputs_and_ambient_paths
8.74s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[xfail]
8.72s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[fail]
8.64s call     tests/test_stage2_swarm.py::test_free_seats_are_forbidden_in_every_private_role
8.53s call     tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code[skip]
8.48s call     tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes
```
