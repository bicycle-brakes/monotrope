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

## Phase 6 — round 2, on commit `e6195de`, 2026-10-17

Re-checked by Opus 5.5 (Claude path, fresh read-only sub-agent, no Codex session). I read each P6 row against the repair `7aeb54b` and ran each named test. On `e6195de`, `.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_model_endpoints.py tests/test_pi_contract.py tests/test_stage2_session.py tests/test_templates.py` gave 867 passed. The six named regression tests (11 cases) passed, and the real-Pi contract ran rather than being skipped.

**P6-1: confirmed.** `test_real_opencode_provider_contracts` asserts again that every `stage2.ladder()` rung sits in Pi's shipped `openai-completions` catalog at `https://opencode.ai/zen/go/v1`. `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5-5` and `minimax-m3` each carry `uebersprungen: "2026-10-17"` and `grund: "wire API not measured"`. Their `gelesen`, `quelle`, `aufbewahrung` and `training` readings are kept unchanged. The live ladder is `deepseek-v4.1-flash, mimo-v2.6-flash, longcat-2.0, glm-5.3-flash, mimo-v2.6-pro`, all on the native address. I checked that the test bites with a scratch script: the same YAML without the four skip markers gives a nine-rung ladder, and exactly those four fail the catalog check. `skipped_models` names all four with the dated reason. The endpoint remark states their wire APIs and the skip.

**P6-2: confirmed.** Spec criterion 6 and ADR 0021 decision 5 now state the Q-11 rule: retention is read and recorded, training must be "Not used", and the 30-day readers were admitted on 2026-10-17. The ADR's Review bullet cites Q-11 to Q-13. The old wordings are gone, and `test_paid_terms_doctrine_records_the_retention_decision` pins both texts.

**P6-3: confirmed.** In new records, `review_loop` writes the reviewer's non-row words through `quote_reviewer`, so a `## Round …` line becomes `> ## Round …`. `ROUND_HEADING` (anchored `^`) does not match it. `rounds_run` now sums `Rounds run:` only inside a runner `RELEASE_HEADING` section, up to `Kept from the loop record:`. Both cases of `test_reviewer_words_cannot_count_as_rounds` pass and reach a real round 2.

**P6-4: confirmed.** `release` quotes every kept line. `_last_release` (`^`-anchored `RELEASE_LINE`), `findings_rows` and `released_rows` therefore cannot read a heading, a state line or a ten-cell row from the kept words. The test seeds an old-style unquoted record with a fake release heading, a `Loop state:` holding `gemini-4-argon-contributor`, `Rounds run: 5` and a ten-cell `L8-1` row. After release, the snapshot equals the real one, only `L1-1` is a row, and `rounds_run` is 1.

**P6-5: confirmed.** `terms_problem` refuses a record whose `aufbewahrung` is missing, empty, blank or not text. That check runs before the training check. `test_paid_terms_require_a_retention_reading` covers five variants.

**P6-6: confirmed.** The notice block now runs on the first non-free round of a run, whatever the stage: no `flash` and no `rung:` key is consumed yet. `cheapest_notice` stays limited to the Flash swarm. `test_first_paid_rung_names_missing_cost_when_flash_is_skipped` skips every Flash member and checks the notice on stderr and in the record.

**P6-7: confirmed (not a test).** The remark now gives the dated `anfragen_5h` values (Go page, read 2026-10-17) for the six ids and says only that no token price is claimed.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| P6-8 | MINOR | MAINT | fix-r | `scripts/stage2.py` `review_loop` (stdout line and first-round `Notice:`), `probe` (the notice text "paid models skipped for unread or refusing terms") | False statement in the handover record. The P6-1 repair routes the wire-API skip through the terms channel (`uebersprungen` in `modelle_terms`). With today's configuration, the first round's notice reads "paid models skipped for unread or refusing terms: qwen3.8-flash (… skipped on 2026-10-17: wire API not measured); gpt-6-luna …; claude-haiku-5-5 …; minimax-m3 …". This was measured with `skipped_models` on `e6195de`. The terms of these four were read, and Q-11 admitted them, as the endpoint remark says ("Their data-terms admission under Q-11 stands"). The record therefore gives the handover a wrong reason for four skips. What should hold: the notice names skipped paid models without claiming a terms problem for a skip whose reason is not one, for example "paid models skipped: …" with the per-model reason. (criterion 6; ADR 0021 decision 5) | claude-opus-5-5 | fixed — not a test — reworded all three notices to "paid models skipped:", preserving each model's reason. | yes |
| P6-9 | MINOR | SPEC | base | `scripts/stage2.py` `probe` | The probe stops at the first member whose call fails, so every later free and paid member goes unchecked. Measured twice on 2026-10-17: `step-5-preview-free` ("Model is unavailable") and, after its exclusion, `cat-jam-free` (empty answer) each ended the run before any paid model was called. What should hold: a failed member is printed with its reason and the probe goes on; at the end it lists the answered and failed members and exits nonzero when one failed. No second address, no substituted model (maintainer, Q-15). (criterion 14) | claude-opus-5-5 (orchestrator) | fixed — tests/test_stage2.py::test_the_probe_continues_after_member_failures | no |
| P6-10 | MINOR | MAINT | fix-r | `model-endpoints.yaml` `free_stage.exclude` entry `step-5-preview-free`, `reason` | False statement after the P6-9 repair. The exclusion reason says "the probe stops at the first refused id, so the other members stay unmeasured while it is listed". Since 3a10892 the probe names a failed member and goes on to the next one (Q-15). What should hold: the reason gives only the measured failure and does not claim that the probe stops; if the exclusion stays, it says why on its own terms, for example that it saves a call that fails every time. (criterion 14) | claude-opus-5-5 | fixed — not a test — the reason now names the measured failure and the saved call | no |

Phase 6 verdict: claude-opus-5-5, 2026-10-17

### Checked without a finding

- The live loop record (`~/.local/state/coding-harness/stage2/loop-until-clean/loop.md`, read for headings and counts only). It has two runner round headings and no `NOT_ROWS_NOTE` block, so no old unquoted reviewer words are present.
- Residual limit, not a finding. `release` still counts `Rounds run:` with `ROUND_HEADING.findall(record)`, and `_record_lines` ends a reviewer section at any `## Round` line. Only a record written before `7aeb54b` with an unquoted reviewer round heading could miscount. The only such record holds none.
- `findings.md` on `e6195de` has no released block yet. `rounds_run` is 0, `findings_rows` returns 7 phase-6 rows, and `read_state` returns None.
- No contradiction with the skips in `docs/WORKFLOW.md` (§4 ladder paragraph, "chat-completions address") or in `prompts/04b-review-loop.md`.
- Quoting also turns the runner's own kept statements into `> ` lines in `findings.md`. Nothing reads them back.

### Read / not read

- Read: `prompts/06-review.md`, the P6 block of `findings.md`, `git show 7aeb54b` in full, the `opencode-go` entry of `model-endpoints.yaml`, spec criterion 6, ADR 0021 decisions 4 and 5 and its Review bullet, and the runner functions named above. Of `docs/WORKFLOW.md`, only the §4 ladder lines and a grep.
- Not read: `design.md` beyond the data-model and release lines, `research.md`, and `decisions.md` beyond the Q-11 heading.
  - `design.md` line 100 still lists `claude-haiku-5.5` and `minimax-m2.7`. That predates the repair, and I did not judge it.
- Not run: `make verify`, any live Pi or provider call.

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 472 files, 1391 commits, 12 rules.

## Phase 4b — loop rows, released 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | Correctness | ADR 0021 decision 5 / criterion 6 | scripts/stage2.py, terms_problem | `terms_problem` admits a paid model with any truthy `gelesen` string (including a non-ISO date) and ignores an empty `uebersprungen` value, so malformed or blank paid-terms dates can pass admission, while the free-rule validator `_exception_problem` requires a valid ISO date for every exception record. | cat-jam-free | fixed — ADR 0021 decision 5 / criterion 6: a paid model is admitted only with a dated reading; terms_problem accepts a gelesen value that is no ISO date; repaired in 90841e1 by the Sonnet sub-agent beside Q-13, not through `repair` | no | agree |
| L1-2 | MINOR | Correctness | tests/test_stage2.py, write_record method | snapshot line: `snapshot = "" if state is None else ...` | Dead code/unreachable branch. After `if state is None: state = loop_state()`, state is never None. The `"" if state is None` check is unreachable and should be removed or clarified. | longcat-2.5-preview-free | fixed — not a test — the branch after `state = loop_state()` is unreachable and misreads as a record without snapshot; repaired in 90841e1 by the Sonnet sub-agent beside Q-13, not through `repair` | no | agree |
| L1-3 | MINOR | Test reliability | tests/test_stage2.py, wrapper barrier mechanism | barrier: `wait_dir.glob("*.arrived")` | Barrier files accumulate across tests if .barrier dir is not cleaned between test runs. Stale .arrived files could cause subsequent tests to pass the barrier prematurely or never reach the expected count. | longcat-2.5-preview-free | rejected — the barrier directory lies under the test's own tmp_path (`world.root / ".barrier"`), so no file outlives a test |  | agree |
| L1-4 | MAJOR | Test correctness | tests/test_stage2.py, full_flow test | `pi=[{"stdout": rows(2)}, {"stdout": rows(2)}]` | Insufficient pi steps for full free+flash+paid swarm flow. Only 2 steps provided but review-loop needs 2 free + 2 flash + 1 paid = 5 reviewer calls. Flash and paid calls receive no step and will output empty stdout, potentially causing unexpected test behavior. | longcat-2.5-preview-free | rejected — one review-loop call runs one round; round 1 is the free swarm, and the world's catalog holds two free ids, so two pi steps are exact |  | agree |
| L1-5 | MINOR | Test correctness | tests/test_model_endpoints.py, test_free_selection_exceptions_require_dates_and_reasons | assertion: `assert any("Zen" in problem for problem in runner.free_rule_problems(broken))` | Test assumes free_rule_problems returns specific "Zen" string when provider="opencode". If implementation uses different wording (e.g., "opencode" or "Zen provider"), assertion fails. | longcat-2.5-preview-free | rejected — the runner's message is "the free rule may not select the Zen provider" (scripts/stage2.py free_rule_problems), which the assertion matches |  | agree |
| L1-6 | MINOR | Test correctness | tests/test_model_endpoints.py, test_every_new_paid_model_carries_its_terms_reading | assertion order: `assert skipped == [...]` | Test expects specific non-alphabetical order for skipped models. If model-endpoints.yaml reorders modelle list, test fails even though content is correct. Order dependency is fragile. | longcat-2.5-preview-free | rejected — the ladder's declared order is what the test pins on purpose (the skip list is named in that order for the handover) |  | agree |
| L2-1 | MAJOR | SPEC | base | scripts/stage2.py:1325-1328 (`_free_candidate`), 1359 (`free_diff`) | The free swarm's candidate filter silently drops source changes the implementation diff promises to carry: only a top-level `scripts/<file>.py` passes, so a changed file under `scripts/` subdirectories — this change's own `scripts/kit/probe.py` hunk included — never reaches round 1, and a changed file that was deleted fails `full.is_file()` and is dropped even though its deletion is a source change; neither omission is marked or tested, while the plan names Python under `scripts/` as free-stage input. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_free_diff_includes_nested_and_deleted_source | no | agree |
| L2-2 | MAJOR | SPEC | base | docs/WORKFLOW.md:735, 1076, 670, 696; tests/test_stage2.py:7896 | The live loop text says the later rungs run "in declared order" and still presents the ladder as the entry's ordered `modelle` list whose rungs are three DeepSeek/MiMo lineages, while the runner orders the nine paid models by `anfragen_5h` descending and the entry's own comment says the list order does not count; the routing test pins "declared order", so correcting the sentence turns the suite red. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_workflow_describes_cost_order | yes | agree |
| L2-3 | MINOR | SPEC | base | scripts/stage2.py:932-960 (`terms_problem`); tests/test_model_endpoints.py:419 | The paid-terms gate admits any model whose record carries a `gelesen` date and a `quelle`, whatever retention or training the record states, so a `modelle_terms` record that says `training: "Yes"` would still be called although the change's own rules keep models that train on prompts out (ADR 0021 decision 5, spec criterion 6, Q-12); the declaration test checks dates only and nothing else reads the training value. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_paid_terms_reject_training | no | agree |
| L2-4 | MINOR | MAINT | base | scripts/stage2.py:26 vs 4004-4012 (`review_loop`) | The runner's own help says "Each loop round and the probe check `tools/pi/pi --version` against `PI_VERSION` first", but only the call that starts a fresh run runs `require_pi`; the Flash swarm, every later rung and every replacement launch Pi without the runner's check, so the stated guarantee and the code disagree (the wrapper still enforces the installed pin, so the defect is the false statement and the lost explicit check). | deepseek-v4.1-flash | fixed — not a test — corrected help to describe version checks before fresh runs and probes | no | agree |
| L2-5 | MINOR | MAINT | base | scripts/stage2.py:2090 (`read_state`), 2204 (`release`) | A loop record written before this change carries no `Loop state:` line, and `release` reads the state before it releases; such a record can neither be continued nor released and the refusal speaks only of continuing, so an in-flight loop from the previous runner is stuck until the external record is hand-edited or deleted, although the design only meant to refuse continuing with invented stages. | deepseek-v4.1-flash | rejected — no record without a `Loop state:` line is in flight (measured 2026-10-17: the only record under ~/.local/state/coding-harness/stage2/ carries one); the false comment is taken as L2-16 |  | agree |
| L2-6 | MINOR | SPEC | base | docs/how-it-works.md:56, 72-94 | The live overview that README links still says the review loop is "at most three rounds" and that the review swarm is "in progress, not merged" and waits for a decision pull request; after this merge both statements are false, and no part of this file is updated. | deepseek-v4.1-flash | fixed — not a test — updated the overview to describe both review swarms and current stop rules | no | agree |
| L2-7 | MINOR | MAINT | base | scripts/stage2.py:1398-1399 (`free_diff`), 4180 (`probe`) | When a change has no file the free filter admits (a config-, prompt- or docs-only change), `free_diff` raises "the implementation diff is empty; the free stage has nothing to review", so `review-loop` refuses before the Flash swarm and ladder that could review the change, and `probe` refuses as well; neither the spec nor the plan defines a fallback or a skipped-free-stage path for this case. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_empty_free_diff_skips_to_paid_models | no | agree |
| L2-8 | MAJOR | SPEC | base | scripts/stage2.py, `terms_problem` | The check that admits a paid model reads only the skip marker, an ISO `gelesen` and `quelle` and never looks at the record's retention or training fields, so a model whose own declaration records that it trains on prompts is admitted to the paid stages; the spec (criterion 6) and ADR 0021 decision 5 promise such models are skipped and named, and no test plants a retaining or training record, so nothing refuses one. | mimo-v2.6-pro | rejected — duplicate of L2-3 (same defect in terms_problem) |  | agree |
| L2-9 | MAJOR | SPEC | base | scripts/stage2.py, `ladder` / `new_state` | When no listed paid model has a terms reading, `ladder` refuses and `new_state` calls it before any stage is chosen, so the whole `review-loop` run refuses and the free swarm — which needs no paid model and is allowed to end the loop before any paid round — never runs. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_free_round_needs_no_eligible_paid_ladder | no | agree |
| L2-10 | MAJOR | SPEC | base | scripts/stage2.py, `flash_problem` / `new_state` | A `flash_swarm` member that is not an eligible paid model raises `Refused` for the whole run instead of being skipped and named for the handover, as ADR 0021 decisions 4 and 5 require; one member whose terms go unread blocks every review round until the configuration is edited, and `tests/test_stage2.py::test_ineligible_paid_models_are_skipped_and_named` pins the refusal as the expected behavior. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_ineligible_flash_member_is_named_and_skipped | yes | agree |
| L2-11 | MAJOR | SPEC | base | docs/WORKFLOW.md, the 4b row of the model table and the review-loop section | Both places say a later round calls "one eligible `modelle` id per round in declared order", while the runner orders the set by the declared cost value cheapest first (ADR 0021 decision 4, prompts/04b-review-loop.md and the endpoint remark all say so); the stale phrase is itself pinned by `tests/test_stage2.py::test_workflow_section_4_routes_the_three_reviews`, so the change ships a live-doctrine conflict its own suite preserves. | mimo-v2.6-pro | rejected — duplicate of L2-2 (same WORKFLOW.md sentence and test) |  | agree |
| L2-12 | MAJOR | MAINT | base | scripts/stage2.py `ladder` docstring, prompts/04b-review-loop.md, docs/adr/0021, tests/test_model_endpoints.py, tests/test_stage2.py | The change repeatedly promises that adding or replacing a ladder model is "a one-line pull request" that touches `model-endpoints.yaml` and nothing else, but the tests pin the exact model set and its count (`test_the_opencode_go_entry_is_declared`, `test_every_new_paid_model_carries_its_terms_reading`, `test_no_doctrine_text_repeats_the_ladder_order`), so the advertised edit path turns the suite red and does not exist. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_adding_a_paid_model_requires_only_configuration | yes | agree |
| L2-13 | MINOR | MAINT | base | scripts/stage2.py, `free_diff` | The untracked file's diff is built from the absolute path (`git diff --no-index /dev/null <abs>`), where `change_diff` uses the relative name, so every untracked file's header in the free swarm's only input carries the local worktree's absolute path out to models whose data terms are unread. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_free_diff_untracked_headers_are_relative | no | agree |
| L2-14 | MINOR | MAINT | base | scripts/stage2.py, `_free_candidate` | Only top-level `scripts/*.py` and `tests/*.py` count as implementation source — nested Python such as `scripts/kit/probe.py` (edited by this very change), non-Python test files and any deleted source file never reach the free diff (`full.is_file()` drops deletions), so the free round judges a silently incomplete implementation diff while the paid rounds see the full one. | mimo-v2.6-pro | rejected — duplicate of L2-1 (same _free_candidate filter) |  | agree |
| L2-15 | MINOR | MAINT | base | scripts/stage2.py, `parse_catalog` | The model listing is read positionally, skipping any line whose first token is "provider", instead of by the header's columns as the design states; a changed column order or a stray line in the listing produces wrong rows or an empty selection with a misleading refusal instead of a named parse failure. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_catalog_parser_uses_header_columns | no | agree |
| L2-16 | MINOR | MAINT | base | scripts/stage2.py, `review_loop` comment vs `read_state` | The comment in the fresh-run branch says a record without a `Loop state:` line "starts over with the current discovery and configuration", but `read_state` refuses such a record outright ("it predates the swarms and cannot be continued"), so the continuation path the code documents for pre-swarm records does not exist. | mimo-v2.6-pro | fixed — not a test — corrected the comment to state that records without a Loop state line are refused | no | agree |

Rounds run: 2

Loop state: {"consumed": ["free", "rung:mimo-v2.6-pro", "flash"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "big-pickle", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-flash", "provider": "opencode"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "exo-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "ling-3.0-flash-fin-free", "provider": "opencode"}, {"model": "ling-3.1-flash-free", "provider": "opencode"}, {"model": "longcat-2.5-preview-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-spark-1.3-contributor-free", "provider": "opencode"}, {"model": "nemotron-3-ultra-free", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "space-bunny-free", "provider": "opencode"}, {"model": "step-5-preview-free", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-flash", "provider": "opencode-go"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon-contributor", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.6", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-preview-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m2.7", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "space-bunny", "provider": "opencode-go"}, {"model": "step-5-preview-free", "provider": "opencode-go"}], "checked_at": "2026-10-16T22:55:12+00:00", "pi_version": "1.2.0", "rule": {"exclude": [], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["cat-jam-free", "longcat-2.5-preview-free", "step-5-preview-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"], "rungs": ["mimo-v2.6-pro"]}}

Kept from the loop record:

> step-5-preview-free failed: pi call failed: exit 1
> Notice: flash_swarm [deepseek-v4.1-flash, mimo-v2.6-flash] differs from the three cheapest admitted models [deepseek-v4.1-flash, mimo-v2.6-flash, mimo-v2.6-pro] by anfragen_5h; the list stays as declared.
> mimo-v2.6-flash failed: pi call failed: exit 1 (400: {"param":"model","type":"invalid_request_error","message":"Upstream request failed: [model_coming_soon] This model is coming soon."}); replaced by mimo-v2.6-pro

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model cat-jam-free · leak check clean over 477 files, 1401 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 477 files, 1401 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model step-5-preview-free · leak check clean over 477 files, 1401 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model cat-jam-free · leak check clean over 477 files, 1401 commits, 12 rules.

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 477 files, 1403 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model cat-jam-free · leak check clean over 477 files, 1404 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 477 files, 1404 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 477 files, 1404 commits, 12 rules.


### Phase 6 re-check of P6-9 (claude-opus-5-5, 2026-10-17, read-only, returned as text and committed unchanged by the orchestrator)

**P6-9: confirmed.** Only `CallFailed` is caught, inside `check_member` in `probe`; `Refused` (declaration, admission and leak checks in `preflight`, `checked_prompt`, `begin_call`) runs outside the handler and still stops the probe. Each failure prints `probe: <id> failed: <reason>`, the end prints the answered and failed ids, and any failure raises `CallFailed` (exit 1). No retry, second address or substituted model. `test_the_probe_continues_after_member_failures` (6 cases) would fail on the old code. `.venv/bin/python -m pytest tests/test_stage2.py -q -k probe`: 26 passed on 3a10892. Test gap, not a finding: no test raises a `Refused` in the middle of a probe run; by reading, those checks sit outside the handler. One stale text found: P6-10.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 477 files, 1405 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model longcat-2.0 · leak check clean over 477 files, 1405 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model glm-5.3-flash · leak check clean over 477 files, 1405 commits, 12 rules.

Stage-2 call, 2026-10-17: probe · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 477 files, 1405 commits, 12 rules.

Stage-2 call, 2026-10-17: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 479 files, 1413 commits, 12 rules.

## Phase 6 — Codex, 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| P6-11 | MAJOR | SPEC | base | `scripts/stage2.py:4420–4456`, `review_loop` | A member returning a five-cell finding table counts as successful despite producing no parseable rows. Reproduced in memory: the runner completed round 1 with zero rows, consumed the free stage, then refused another review because “round 1 was clean”. Malformed answers must count as member failures; when every answer is malformed, no round may complete. [criterion 4; design: malformed finding output fails that member] | Codex | fixed — tests/test_stage2.py::test_malformed_finding_tables_fail_the_member | yes |
| P6-12 | MAJOR | MAINT | base | `scripts/stage2.py:1324–1387,1654–1684`, discovery and reviewer launch | Discovery deletes its refreshed catalog, retains only model ids, and launches each probe/reviewer offline with an empty agent directory. A newly discovered model therefore loses its actual API configuration. Using the installed Pi resolver, a synthetic new free model declared as `anthropic-messages` resolved instead to a guessed `openai-completions` model without the overlay. Preparation can consequently report a reachable model as unavailable because it tested the wrong protocol. Preserve the refreshed definitions for subsequent calls. [criteria 5, 17] | Codex | fixed — tests/test_stage2.py::test_refreshed_model_definitions_reach_each_launch | yes |
| P6-13 | MAJOR | SPEC | base | `scripts/stage2.py:1180–1249,1678–1679`, free admission and launch | Setting `free_stage.provider` to another provider passes validation. An id discovered only under that provider then passes free admission, but the launch still requests `opencode-go/<id>`. Reproduced locally: the rule reported no problems and admission returned no refusal for this case. The discovery provider must match the permitted Go launch provider; otherwise an undiscovered Go id receives the unread-terms exception. [criteria 5, 7] | Codex | fixed — tests/test_stage2.py::test_free_admission_requires_the_launch_provider | no |

Phase 6 verdict: codex 01a149f1-b5b0-7813-a9bd-b77afc6bf6a7, 2026-10-17
Reviewer session: codex 01a149f1-b5b0-7813-a9bd-b77afc6bf6a7 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 479 files, 1414 commits, 12 rules.

## Phase 6 follow-up — Codex orchestrator, 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| P6-14 | MAJOR | MAINT | fix-r | `scripts/stage2.py`, `overlay_store` / `run_reviewer` | Protocol preservation is incomplete after 20f976e: Pi restores a saved catalog only when its server modification date is newer than its shipped model data. A freshly retrieved model whose HTTP Last-Modified is absent/invalid is saved with lastModified=0; copying that store into the offline launch still leaves the model unresolved. Reproduced against pinned Pi 1.2.0 with in-memory stores, no networking or credentials: the synthetic anthropic-messages model was absent at date 0 and resolved with the identical definition at a synthetic 2099 control date, while both refreshes returned no errors. Preserve and activate the admitted fresh definition without inventing server-date evidence; verify actual API/endpoint resolution for missing and older dates. Source, hashes and reproducer: docs/research/2026-10-17-pi-overlay-resolution.md. This reopens P6-12 with new evidence. [criteria 5, 17] | Codex (orchestrator, offline resolver check) | fixed — tests/test_stage2.py::test_refreshed_model_definitions_reach_each_launch | yes |

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 480 files, 1421 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/loop-until-clean/plan.md` +6 -0
> - `scripts/stage2.py` +16 -1
> - `tests/test_pi_contract.py` +71 -0
> - `tests/test_stage2.py` +6 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - P6-14: tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date: the setup phase of `tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-0]` ended failed; red first needs passing setup and teardown
> ```

Stage-2 call, 2026-10-17: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 480 files, 1422 commits, 12 rules.

Stage-2 call, 2026-10-17: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 480 files, 1425 commits, 12 rules.

## Phase 6 — Codex, 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| P6-15 | BLOCKER | MAINT | fix-r | `scripts/stage2.py:1345–1346`, `activate_overlay` | Fetched model headers become executable configuration. A catalog definition containing `headers: {"X-Catalog": "!printf catalog-command-ran"}` is copied unchanged into `models.json`; pinned Pi interprets that header as a shell command. Reproduced offline through Pi’s configuration composer and header resolver: the resulting header was `catalog-command-ran`. Catalog data can therefore execute local commands during a tool-free probe or review. Preserve headers as literal data without enabling command execution or environment interpolation. [criterion 3; criterion 17] | Codex | fixed — tests/test_stage2.py::test_catalog_headers_are_activated_as_literal_data | — |
| P6-16 | MAJOR | SPEC | base | `scripts/stage2.py:1752–1758`, `run_swarm` | An unsuccessful review expressed as prose still certifies a clean round. Reproduced with the answer “I could not review because the context is too long.”: `review_loop` completed round 1 with zero findings, consumed the free stage, and refused the next invocation because “round 1 was clean”. The malformed-table repair checks only pipe-delimited output. Require a valid no-finding response before treating an answer without parsed findings as successful; if every member fails to review, complete no round. [criterion 4; design: validated no-finding answers succeed, malformed output fails] | Codex | fixed — tests/test_stage2.py::test_unsuccessful_review_prose_cannot_certify_a_clean_round | — |

Phase 6 verdict: codex 01a14a5c-e94b-7650-8c28-d0c7843dcb27, 2026-10-17
Reviewer session: codex 01a14a5c-e94b-7650-8c28-d0c7843dcb27 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

### Orchestrator disposition — 2026-10-17

Both new findings are taken. Static inspection of pinned Pi 1.2.0 confirms that provider-composer.js obtains headers from models.json and passes them to resolveHeadersOrThrow; resolve-config-value.js treats a leading exclamation mark as a shell command and dollar references as environment templates. The fresh-catalog activation boundary must encode literal headers without executing either feature, while retaining the original catalog evidence. Existing scratch/no-tools restrictions do not make executable configuration safe. Regression evidence should cover ordinary, command-shaped and environment-shaped header values through the actual pinned resolver, with synthetic data and no credential access.

run_swarm currently rejects an unreadable pipe-delimited table but accepts any other nonempty prose with zero parsed rows. That contradicts the design's validated no-finding requirement. Define and document an explicit no-finding answer, reject inability/error/empty/malformed output as a member failure, retain valid findings with commentary, and preserve the no-successful-member/no-round rule. These are repairs to existing accepted criteria, not a new model-admission decision. The independent reviewer remains read-only and does not repair its own findings.

Stage-2 call, 2026-10-17: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 480 files, 1427 commits, 12 rules.
