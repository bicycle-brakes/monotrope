---
title: "Findings — loop-until-clean"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-17
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

**Paid terms read and admitted.** `deepseek-v4.1-flash`, `mimo-v2.6-flash`
and `mimo-v2.6-pro` carry dated retention and training readings from the Go
page privacy table (`https://opencode.ai/docs/go`, read 2026-10-07):
retention `0 days`, training "Not used". The readings stand in the entry's
`modelle_terms` (`model-endpoints.yaml`); the first two are the eligible
`flash_swarm` members, and `mimo-v2.6-pro` remains the sole later rung until
further readings stand.

**Paid terms skipped, named for the handover.** `longcat-2.0`,
`glm-5.3-flash`, `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5.5`,
`minimax-m2.7`: their retention and training terms were not read as of
2026-10-16, so `modelle_terms` records a dated skip for each and
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

Stage-2 call, 2026-10-16: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 472 files, 1350 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +2 -2
> - `ROADMAP.md` +3 -1
> - `docs/WORKFLOW.md` +43 -19
> - `docs/adr/0021-review-swarms-until-clean.md` +3 -2
> - `model-endpoints.yaml` +79 -4
> - `plans/changes/loop-until-clean/findings.md` +9 -7
> - `plans/changes/loop-until-clean/plan.md` +28 -20
> - `prompts/02a-spec-review.md` +2 -2
> - `prompts/04b-review-loop.md` +33 -15
> - `prompts/06-review.md` +3 -3
> - `scripts/kit/probe.py` +9 -1
> - `scripts/stage2.py` +909 -99
> - `templates/findings.md` +3 -2
> - `tests/test_model_endpoints.py` +127 -1
> - `tests/test_pi_contract.py` +87 -0
> - `tests/test_stage2.py` +950 -169
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> README.md:168:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> README.md:168:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> README.md:169:81 error MD013/line-length Line length [Expected: 80; Actual: 100]
> README.md:170:81 error MD013/line-length Line length [Expected: 80; Actual: 90]
> templates/adr.md:29 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/arc42.md:15 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/arc42.md:107:27 error MD034/no-bare-urls Bare URL used [Context: "https://creativecommons.org/li..."]
> templates/arc42.md:110:27 error MD034/no-bare-urls Bare URL used [Context: "https://arc42.org"]
> templates/design.md:16 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/design.md:97 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Added"]
> templates/design.md:101 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Changed"]
> templates/design.md:105 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Removed"]
> templates/findings.md:18 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/findings.md:45:5 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:9 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:13 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:21 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:25 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> templates/findings.md:46:7 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:15 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:22 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:54 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:99 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:106 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:63 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Severity"]
> templates/findings.md:71 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Dimension"]
> templates/findings.md:77 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Origin"]
> templates/findings.md:84 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Markers that override everythi..."]
> templates/findings.md:111:81 error MD013/line-length Line length [Expected: 80; Actual: 91]
> templates/findings.md:112:81 error MD013/line-length Line length [Expected: 80; Actual: 101]
> templates/findings.md:123:81 error MD013/line-length Line length [Expected: 80; Actual: 125]
> templates/handover.md:20:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
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

Stage-2 call, 2026-10-16: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 472 files, 1355 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +2 -3
> - `plans/changes/loop-until-clean/plan.md` +22 -20
> - `tests/test_stage2.py` +9 -3
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> README.md:168:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> README.md:168:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> README.md:169:81 error MD013/line-length Line length [Expected: 80; Actual: 100]
> README.md:170:81 error MD013/line-length Line length [Expected: 80; Actual: 90]
> templates/adr.md:29 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/arc42.md:15 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/arc42.md:107:27 error MD034/no-bare-urls Bare URL used [Context: "https://creativecommons.org/li..."]
> templates/arc42.md:110:27 error MD034/no-bare-urls Bare URL used [Context: "https://arc42.org"]
> templates/design.md:16 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/design.md:97 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Added"]
> templates/design.md:101 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Changed"]
> templates/design.md:105 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Removed"]
> templates/findings.md:18 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/findings.md:45:5 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:9 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:13 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:21 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:25 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> templates/findings.md:46:7 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:15 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:22 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:54 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:99 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:106 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:63 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Severity"]
> templates/findings.md:71 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Dimension"]
> templates/findings.md:77 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Origin"]
> templates/findings.md:84 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Markers that override everythi..."]
> templates/findings.md:111:81 error MD013/line-length Line length [Expected: 80; Actual: 91]
> templates/findings.md:112:81 error MD013/line-length Line length [Expected: 80; Actual: 101]
> templates/findings.md:123:81 error MD013/line-length Line length [Expected: 80; Actual: 125]
> templates/handover.md:20:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
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

Stage-2 call, 2026-10-16: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 472 files, 1358 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/loop-until-clean/plan.md` +22 -20
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> README.md:168:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> README.md:168:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> README.md:169:81 error MD013/line-length Line length [Expected: 80; Actual: 100]
> README.md:170:81 error MD013/line-length Line length [Expected: 80; Actual: 90]
> templates/adr.md:29 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/arc42.md:15 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/arc42.md:107:27 error MD034/no-bare-urls Bare URL used [Context: "https://creativecommons.org/li..."]
> templates/arc42.md:110:27 error MD034/no-bare-urls Bare URL used [Context: "https://arc42.org"]
> templates/design.md:16 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/design.md:97 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Added"]
> templates/design.md:101 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Changed"]
> templates/design.md:105 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Removed"]
> templates/findings.md:18 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/findings.md:45:5 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:9 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:13 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:21 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:25 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> templates/findings.md:46:7 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:15 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:22 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:54 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:99 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:106 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:63 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Severity"]
> templates/findings.md:71 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Dimension"]
> templates/findings.md:77 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Origin"]
> templates/findings.md:84 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Markers that override everythi..."]
> templates/findings.md:111:81 error MD013/line-length Line length [Expected: 80; Actual: 91]
> templates/findings.md:112:81 error MD013/line-length Line length [Expected: 80; Actual: 101]
> templates/findings.md:123:81 error MD013/line-length Line length [Expected: 80; Actual: 125]
> templates/handover.md:20:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
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

Stage-2 call, 2026-10-17: review-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 472 files, 1370 commits, 12 rules.

Stage-2 call, 2026-10-17: review-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 472 files, 1370 commits, 12 rules.

Stage-2 call, 2026-10-17: review-loop · endpoint opencode-go · model step-5-preview-free · leak check clean over 472 files, 1370 commits, 12 rules.

Stage-2 call, 2026-10-17: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 472 files, 1382 commits, 12 rules.

Stage-2 call, 2026-10-17: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 472 files, 1382 commits, 12 rules.

Stage-2 call, 2026-10-17: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 472 files, 1384 commits, 12 rules.

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 472 files, 1384 commits, 12 rules.

## Phase 6 — review, on commit `42f2e4d`, 2026-10-17

Read by Opus 5.5 (Claude path, sub-agent, no Codex session), against `spec.md` (updated 2026-10-17, Q-13 inserts included), `design.md` and the ADR 0021 draft. The diff was read against the merge base `3de40c7`. No phase-2a block stands in `findings.md`, so there were no 2a rows to trace into the spec. Verdict: 2 BLOCKER (both `[DIVERGENT]`), 2 MAJOR, 3 MINOR; no `[AMBIGUITY]`.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| P6-1 | BLOCKER | MAINT | base | `tests/test_pi_contract.py::test_real_opencode_provider_contracts`; `model-endpoints.yaml` opencode-go `bemerkung` | [DIVERGENT] The weakened assertion rests on a false premise. Its comment says four ladder ids "are not in its baseline" and arrive only through the pi.dev overlay. The shipped `pi-ai/dist/providers/data/opencode-go.json` (Pi 1.2.0, read 2026-10-17) does carry them, under other wire APIs. `qwen3.8-flash`, `claude-haiku-5-5` and `minimax-m3` sit under `anthropic-messages` (baseUrl `https://opencode.ai/zen/go`, so calls go to `/v1/messages`). `gpt-6-luna` sits under `openai-responses`. Pi resolves `opencode-go/<id>` from that baseline, so these four rungs would not use `/zen/go/v1/chat/completions`. The endpoint remark says reviews go to chat/completions and that `/v1/messages` "is not used — three calls there were refused on 2026-10-08". Phase 4's own record in `findings.md` already noted the wire APIs of qwen and luna on 2026-10-16. The old per-rung assertion was red for exactly this reason. The new `if rung in catalog` filter (openai-completions only) lets any rung that moved wire API pass silently. What should hold: the per-rung wire-API check stays and bites. Either these rungs are measured and declared on their real address, or they are skipped and named. (criterion 6 / ADR 0019 launch contract; endpoint declaration) | claude-opus-5-5 | fixed — tests/test_pi_contract.py::test_real_opencode_provider_contracts | yes |
| P6-2 | BLOCKER | SPEC | base | `spec.md` criterion 6; `docs/adr/0021-review-swarms-until-clean.md` decision 5 and Review bullet; `model-endpoints.yaml` `modelle_terms`; `scripts/stage2.py` `terms_problem` | [DIVERGENT] Spec criterion 6 ("unreadable or retaining/training models are skipped") and ADR 0021 decision 5 ("skip … any whose terms retain/train") say a model that retains data is skipped. The configuration admits `gpt-6-luna` and `claude-haiku-5-5` with `aufbewahrung: "30 days"`, and the runner does too: `terms_problem` checks only training == "Not used". This follows the maintainer's Q-11 answer, which neither the spec nor the ADR records; the ADR's Review bullet cites only Q-1 to Q-10, although decision 4 cites Q-13. The record the maintainer merges therefore states the opposite of what runs. What should hold: spec criterion 6 and ADR decision 5 state Q-11's rule. Retention is read and recorded, training must be "Not used", and the 30-day readers are admitted by the maintainer's decision of 2026-10-17. (criterion 6, criterion 16) | claude-opus-5-5 | fixed — tests/test_stage2.py::test_paid_terms_doctrine_records_the_retention_decision | no |
| P6-3 | MAJOR | MAINT | base | `scripts/stage2.py` `review_loop` (`last = max(..., rounds_run(...))`), `rounds_run`, `clean_round` | Reviewer text can end the loop as "clean". Case A: a reviewer answer kept in the record contains a line `## Round 7 — x, 2026-10-17`. `rounds_run` counts it as a round, so `last` is 2 and round 2 has no rows. `clean_round` returns True and the next call refuses with "round 2 was clean", although round 1 holds a taken row. Case B: after a release, a kept reviewer line `Rounds run: 5` is summed by `ROUNDS_LINE` over the whole of `findings.md`, so `last` becomes 6, again row-less, and the loop stops as clean. Both cases were measured with a scratch script against the runner's functions. Before this change such a line only moved the cap; now it closes the loop with a false clean result. What should hold: counts and headings come only from the runner's own lines, never from the kept reviewer words. (criterion 1, criterion 13; design "quoted reviewer text never becomes control metadata") | claude-opus-5-5 | fixed — tests/test_stage2.py::test_reviewer_words_cannot_count_as_rounds | no |
| P6-4 | MAJOR | MAINT | base | `scripts/stage2.py` `release` (kept words appended verbatim), `_last_release`, `read_state`, `findings_rows`, `free_admission_problem` | Reviewer text can supply the run's snapshot. The release appends the reviewers' words unquoted after `Kept from the loop record:`. Suppose such words contain a line starting `## Phase 4b — loop rows, released`, then `Loop state: {...}`. `_last_release` then picks that line, and `read_state(None, findings)` returns the reviewer's JSON (measured with a scratch script). Under that fake heading, a ten-cell row `L<n>-1 … taken … no …` also counts as released history, which defeats the clean stop. A continued run then takes its stages from the injected JSON. Example: a `free.selected` holding `gemini-4-argon-contributor`. `free_admission_problem` admits it, because it is not in `modelle` and is in `selected`. The diff then goes to a model that trains on prompts, which Q-12 excluded. What should hold: kept reviewer words are quoted or escaped in the release block, and no heading, row or state line is read from them. (criterion 13, criterion 7) | claude-opus-5-5 | fixed — tests/test_stage2.py::test_released_reviewer_words_cannot_supply_a_snapshot | yes |
| P6-5 | MINOR | SPEC | base | `scripts/stage2.py` `terms_problem` | The runtime gate never reads `aufbewahrung`. A `modelle_terms` record with a valid `gelesen`, a `quelle` and `training: "Not used"`, but no retention reading at all, is admitted to the paid stages. Only `tests/test_model_endpoints.py` catches it, and only on the real YAML. What should hold: a record without a retention reading admits nothing, as the spec asks for "a dated reading of retention and training terms". (criterion 6) | claude-opus-5-5 | fixed — tests/test_stage2.py::test_paid_terms_require_a_retention_reading | no |
| P6-6 | MINOR | SPEC | base | `scripts/stage2.py` `review_loop` (the `unvalued_models` notice sits only in the `paid-swarm` branch) | A ladder model without `anfragen_5h` is named on stderr and in the record only when a Flash-swarm round runs. If every Flash member is ineligible, the Flash stage is skipped and the unvalued model is ordered last but never named, which is a silent drop of the notice. What should hold: the notice appears with the run's first paid round, whichever stage that is. (criterion 8; ADR 0021 decision 4) | claude-opus-5-5 | fixed — tests/test_stage2.py::test_first_paid_rung_names_missing_cost_when_flash_is_skipped | no |
| P6-7 | MINOR | MAINT | base | `model-endpoints.yaml` opencode-go `bemerkung` ("no price or limit is claimed for them") | False statement. The remark says no price or limit is claimed for the six ids beyond the three measured ones. The same entry now declares `anfragen_5h` (requests per 5 hours, read 2026-10-17) for every one of them, and the runner orders the ladder by it. What should hold: the sentence names the dated limit values it now carries. | claude-opus-5-5 | fixed — not a test — endpoint remark now names the anfragen_5h values read on 2026-10-17 | no |

Phase 6 verdict: claude-opus-5-5, 2026-10-17

### Checked without a finding

- Ladder ordering (`ordered_models`, `ladder`): `anfragen_5h` descending, ties by id, unvalued last; booleans and values ≤0 count as absent.
- Flash replacement (`review_loop`): it draws from the snapshot `rungs`, minus round members and consumed rungs. Each model is tried at most once, and a failed replacement is consumed too. The swap is recorded and printed, the reason carries the last scrubbed Pi stderr line, and the stderr tail is labelled with the model id. An all-failed attempt consumes nothing.
- Free stage reads the overlay: the refresh flag is `pi update --models` (checked against `package-manager-cli.js`). The store is `models-store.json` in `PI_CODING_AGENT_DIR` (checked against `model-runtime.js` and `remote-catalog-provider.js`). The selection is listing ∩ overlay, and a missing or unreadable store refuses.
- `terms_problem`: `gelesen` must be an ISO date (regex plus `fromisoformat`), and an empty or false `uebersprungen` counts as absent.
- Run snapshot (decision 9): members are pinned and consumed stages survive release and YAML edits. The live record shows this: its snapshot predates Q-11 (ladder of 3, all consumed), so this run will report "every stage consumed" despite the six newly admitted rungs. That is the documented behaviour, not a defect.
- The free path uses `--no-tools`, a scratch cwd, no `READ_REQUEST` and a bounded diff. Each member is checked against its declaration and the leak check in the parent before dispatch. AGENTS.md is at 200 lines.
- Tests: `.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_model_endpoints.py tests/test_pi_contract.py tests/test_stage2_session.py tests/test_templates.py` gave 857 passed at `42f2e4d`.

### Loop record check (read after the verdict)

- Taken/rejected decisions under the evidence rule: none of the rejected rows should have been taken.
  - L1-3 to L1-6, L2-5, and the duplicates L2-8, L2-11 and L2-14 are rejected correctly.
  - L1-6's reason ("declared order pinned on purpose") is stale after Q-13, but the order assertion it refers to no longer exists, so the point is moot.
- Repairs (`90841e1`, `2bea51c`, `42f2e4d`): every taken row is closed by code, and each named test exists. "declared order" is gone from WORKFLOW, and how-it-works is updated.
- Two partial closures:
  - L2-3 fixed training only. The retention half was left to Q-11 without amending the spec or the ADR, which is the new evidence behind P6-2 and P6-5.
  - L2-4 was closed as a help-text correction. The lost per-round `require_pi` is accepted there, so it is not repeated here.

### Not read / not checked

- Not read: `plan.md` beyond its first 80 lines, `research.md`, `ROADMAP.md`, `plans/INDEX.md`, `scripts/kit/probe.py`, `decisions/answers/.../adr.yaml`, and most of the WORKFLOW diff (only the §4 loop section).
- Not run: no live Pi or provider call, no `make verify`.
- Not measured: whether `/v1/messages` and `/v1/responses` work today for the four rungs.

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 472 files, 1388 commits, 12 rules.
