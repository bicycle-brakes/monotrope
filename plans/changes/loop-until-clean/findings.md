---
title: "Findings — loop-until-clean"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — loop-until-clean

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1153 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1
>
> The runner put back:
> - `docs/adr/0018-review-swarms-until-clean.md`
> - `plans/changes/loop-until-clean/decisions.md`
> - `plans/changes/loop-until-clean/design.md`
> - `plans/changes/loop-until-clean/plan.md`
> - `plans/changes/loop-until-clean/research.md`
> - `plans/changes/loop-until-clean/spec.md`

Stage-2 call, 2026-10-14: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 420 files, 1154 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1

Stage-2 call, 2026-10-14: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 420 files, 1154 commits, 12 rules.

ADR answer owed: decisions/answers/loop-until-clean/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).

Stage-2 call, 2026-10-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 465 files, 1295 commits, 12 rules.

Stage-2 call, 2026-10-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 465 files, 1304 commits, 12 rules.

Stage-2 call, 2026-10-16: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 465 files, 1306 commits, 12 rules.

## Phase 4 — records for the handover (2026-10-16)

**Paid terms read and admitted.** `deepseek-v4.1-flash` and `mimo-v2.6-flash`
carry dated retention and training readings from the Go page privacy table
(`https://opencode.ai/docs/go`, read 2026-10-07): retention `0 days`, training
"Not used". The readings stand in the entry's `modelle_terms`
(`model-endpoints.yaml`).

**Paid terms skipped, named for the handover.** `longcat-2.0`,
`glm-5.3-flash`, `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5.5`,
`minimax-m2.7`, `mimo-v2.6-pro`: their retention and training terms were not
read as of 2026-10-16, so `modelle_terms` records a dated skip for each and
the runner refuses them as paid reviewers until a dated reading stands. No
refused id was respelled or given another address; the skipped ids shorten the
ladder of a run until their readings are recorded.

**Measured: the refresh spelling.** The pinned Pi's refresh verb is
`pi update --models`; `pi update models`, as the decisions addendum's source
reading spells it, is refused by Pi's argument parser. Source: the pinned
install under `tools/pi/` (Pi 1.2.0), read 2026-10-16; the runner's discovery
therefore forces the measured spelling.

**Measured: installed-catalog spellings.** The installed catalog of
2026-10-16 spells the Haiku id `claude-haiku-5-5` where the entry declares
`claude-haiku-5.5`, and lists `qwen3.8-flash` under the `anthropic-messages`
provider shape and `gpt-6-luna` under `openai-responses`. Source:
`pi --list-models` of the pinned install, read 2026-10-16. Recorded so the
compatibility probe's evidence can be read against the declaration; the probe
names what it actually called.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +2 -2
> - `ROADMAP.md` +3 -2
> - `docs/WORKFLOW.md` +69 -30
> - `docs/adr/0021-review-swarms-until-clean.md` +2 -1
> - `model-endpoints.yaml` +61 -4
> - `plans/changes/loop-until-clean/findings.md` +30 -0
> - `plans/changes/loop-until-clean/plan.md` +22 -20
> - `prompts/02a-spec-review.md` +3 -2
> - `prompts/04b-review-loop.md` +27 -11
> - `prompts/06-review.md` +3 -3
> - `scripts/stage2.py` +805 -101
> - `templates/findings.md` +4 -2
> - `tests/test_model_endpoints.py` +106 -4
> - `tests/test_pi_contract.py` +52 -0
> - `tests/test_stage2.py` +719 -138
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1243 lines of this gate left out …]
> FAILED tests/test_stage2.py::test_table_lines_that_are_not_rows_are_never_reported_as_no_finding[short-table]
> FAILED tests/test_stage2.py::test_the_foreign_environment_is_the_runners - As...
> FAILED tests/test_stage2.py::test_no_call_carries_another_endpoints_key - Ass...
> FAILED tests/test_stage2.py::test_every_call_gets_an_empty_standard_input - A...
> FAILED tests/test_stage2.py::test_the_opencode_key_never_leaves_the_runner - ...
> FAILED tests/test_stage2.py::test_every_call_leaves_its_line_in_findings - As...
> FAILED tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current
> FAILED tests/test_stage2.py::test_a_findings_file_without_a_header_is_left_without_one
> FAILED tests/test_stage2.py::test_every_prompt_asks_to_read_nothing_outside
> FAILED tests/test_stage2.py::test_the_review_loop_launches_pi_isolated - Asse...
> FAILED tests/test_stage2.py::test_loop_and_probe_use_repository_pi - Assertio...
> FAILED tests/test_stage2.py::test_truncated_pi_print_failure_is_refused - Ass...
> FAILED tests/test_stage2.py::test_the_pinned_pi_runs_the_probe_on_every_rung
> FAILED tests/test_stage2.py::test_a_round_calls_its_rung_from_the_entry - Ass...
> FAILED tests/test_stage2.py::test_reordering_the_ladder_touches_no_code - Ass...
> FAILED tests/test_stage2.py::test_the_reviewer_call_can_only_read_and_search
> FAILED tests/test_stage2.py::test_the_reviewer_prompt_carries_the_loop_prompt_and_the_uncommitted_diff
> FAILED tests/test_stage2.py::test_a_round_is_written_as_its_rung - AssertionE...
> FAILED tests/test_stage2.py::test_a_round_that_did_not_review_writes_nothing
> FAILED tests/test_stage2.py::test_a_round_without_a_finding_still_counts - As...
> FAILED tests/test_stage2.py::test_a_call_without_an_answer_is_not_a_round[non-zero-exit]
> FAILED tests/test_stage2.py::test_a_call_without_an_answer_is_not_a_round[empty-answer]
> FAILED tests/test_stage2.py::test_the_loop_stops_when_the_ladder_ends - Asser...
> FAILED tests/test_stage2.py::test_the_loop_stops_at_three_rounds - AssertionE...
> FAILED tests/test_stage2.py::test_round_three_starts_only_after_a_taken_row
> FAILED tests/test_stage2.py::test_a_call_over_the_time_limit_is_stopped - Ass...
> FAILED tests/test_stage2.py::test_a_refused_rung_stops_the_run_without_fallback
> FAILED tests/test_stage2.py::test_a_clean_round_ends_the_loop - AssertionErro...
> FAILED tests/test_stage2.py::test_both_swarms_run_in_parallel_as_one_round - ...
> FAILED tests/test_stage2.py::test_the_free_stage_reads_nothing_beyond_the_diff
> FAILED tests/test_stage2.py::test_a_failed_swarm_member_preserves_successful_answers
> FAILED tests/test_stage2.py::test_free_discovery_admits_new_go_models_each_run
> FAILED tests/test_stage2.py::test_free_discovery_forces_live_refresh_before_listing
> FAILED tests/test_stage2.py::test_free_selection_changes_in_yaml_without_runner_edits
> FAILED tests/test_stage2.py::test_ineligible_paid_models_are_skipped_and_named
> FAILED tests/test_stage2.py::test_free_class_admission_is_bound_to_discovery_and_purpose
> FAILED tests/test_stage2.py::test_round_two_is_the_flash_swarm_then_single_rungs
> FAILED tests/test_stage2.py::test_two_fix_r_rounds_stop_the_loop - AssertionE...
> FAILED tests/test_stage2.py::test_round_history_survives_split_releases_and_config_edits
> FAILED tests/test_stage2.py::test_the_probe_checks_discovered_and_paid_models_once
> FAILED tests/test_stage2.py::test_a_pipe_inside_a_reviewers_finding_reaches_findings
> FAILED tests/test_stage2.py::test_a_line_that_is_not_a_loop_row_is_carried_to_findings
> FAILED tests/test_stage2.py::test_every_line_of_a_reviewers_answer_reaches_findings_even_one_that_starts_with_a_hash
> FAILED tests/test_stage2.py::test_an_answer_without_rows_reaches_findings_as_it_came
> FAILED tests/test_stage2.py::test_a_reviewers_lines_that_look_like_the_records_own_text_are_carried
> FAILED tests/test_stage2.py::test_a_new_records_intro_names_the_not_a_test_status_and_the_fixed_mark
> FAILED tests/test_stage2.py::test_a_rounds_words_do_not_swallow_the_rows_of_the_next
> FAILED tests/test_stage2.py::test_a_table_line_a_reviewer_wrote_with_a_loop_id_is_carried_not_refused[release-loop]
> FAILED tests/test_stage2.py::test_a_table_line_a_reviewer_wrote_with_a_loop_id_is_carried_not_refused[review-loop]
> FAILED tests/test_stage2.py::test_a_table_line_a_reviewer_wrote_with_a_loop_id_is_carried_not_refused[review]
> FAILED tests/test_stage2.py::test_a_damaged_row_of_the_record_still_refuses_beside_reviewer_text
> FAILED tests/test_stage2.py::test_round_three_starts_after_a_fixed_round_two_row
> FAILED tests/test_stage2.py::test_agents_md_names_the_loop_and_the_runner - A...
> FAILED tests/test_stage2.py::test_the_prompts_name_the_ladder_and_the_limit
> FAILED tests/test_stage2.py::test_the_loop_doctrine_names_both_swarms_until_clean
> FAILED tests/test_stage2.py::test_adr_0021_amends_the_round_budget - Assertio...
> 58 failed, 2066 passed, 16 skipped in 687.88s (0:11:27)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> tests/test_stage2.py:4383:69: ARG001 Unused function argument: `capsys`
>      |
> 4383 | def test_free_discovery_admits_new_go_models_each_run(world: World, capsys: pytest.CaptureFixture[str]) -> None:
>      |                                                                     ^^^^^^ ARG001
> 4384 |     """Criterion 5. Planted fault: a newly matching catalog id is skipped for a declaration it never had, or Zen is called."""
> 4385 |     world.script(pi=[{"stdout": rows(1)}])
>      |
>
> Found 1 error.
> ── [ruff-check] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (2):
>   - 1 rote(r) Fall/Faelle ohne deklarierten Grund
>       ::tests.test_model_endpoints
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>   - 39 Eintrag/Eintraege in REIST_NICHT haben keinen Fall mehr
>       tests.test_ci::test_der_echte_lesepfad_des_bead_gates_wird_erkannt
>       tests.test_ci::test_every_gate_step_has_a_mutation_test
>       tests.test_ci::test_every_script_has_a_test_or_a_declared_reason
>       tests.test_ci::test_no_declared_reason_cites_a_closed_or_unknown_bead
>       tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_caller
>       tests.test_ci::test_one_version_is_the_interpreter_floor
>       tests.test_ci::test_real_pi_is_provisioned_before_contracts
>       tests.test_ci::test_the_cloud_environment_builds_the_venv_with_the_floor
>       tests.test_ci::test_the_makefile_runs_what_the_one_list_runs
>       tests.test_feedback_channel::test_journal_index_lists_every_open_project_handover
>       tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[GEMEINSAM-fehlende_gemeinsame]
>       tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[PROJEKT_PFLICHT-fehlende_kanalpflicht]
>       tests.test_kit::test_the_kit_list_is_not_derivable_from_the_export_list
>       tests.test_kit::test_the_role_check_goes_red_when_a_rule_is_removed
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[code-generation-orchestrator.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[consistency-auditor.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[entity-builder.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[entity-deployer.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[migration-supervisor.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[preconditions-gate-runner.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[reconciliation-orchestrator.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01-explore.md-GLM 5.3 Flash]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01a-interview.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-gpt-6.1-sol]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02a-spec-review.md-Opus 5.5]
>         …
>       
>       Entweder wurde der Test umbenannt — dann den Eintrag nachziehen — oder seine Datei reist nicht mehr mit. Der zweite Fall ist der gefaehrliche: die Portabilitaet sinkt, und die gemeldete Quote steigt.
>
> INFO  (1):
>   - 0 von 1 Faellen tragen in ein fremdes Repo (0 %)
>       mechanismus 85 · bestand 380 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 10671 earlier lines left out …]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-16: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 465 files, 1321 commits, 12 rules.

Stage-2 call, 2026-10-16: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Z.ai 5-hour GLM budget used up (maintainer, 2026-10-16) · leak check clean over 465 files, 1327 commits, 12 rules.
