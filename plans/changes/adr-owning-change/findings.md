---
title: "Findings — adr-owning-change"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — adr-owning-change

Stage-2 call, 2026-10-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 383 files, 976 commits, 12 rules.

Stage-2 call, 2026-10-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 384 files, 976 commits, 12 rules.

Stage-2 call, 2026-10-13: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3-flash as an unrecognized model twice on 2026-10-13 (bead coding-harness-3fc) · leak check clean over 384 files, 976 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `decisions/adoption.yaml` +5 -0
> - `docs/WORKFLOW.md` +22 -7
> - `docs/adr/0014-a-change-claims-its-adr-files.md` +181 -0
> - `plans/changes/adr-owning-change/plan.md` +23 -21
> - `plans/changes/criterion-test-ledger/plan.md` +2 -8
> - `plans/changes/criterion-test-ledger/spec.md` +1 -0
> - `prompts/02-spec.md` +7 -0
> - `provenance.yaml` +5 -0
> - `scripts/adoption.py` +67 -0
> - `scripts/check_interview_minimums.py` +149 -103
> - `scripts/ci_gates.py` +4 -0
> - `scripts/kit/manifest.yaml` +15 -0
> - `templates/spec.md` +3 -0
> - `tests/test_adoption.py` +91 -0
> - `tests/test_check_interview_minimums.py` +355 -112
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [leerprobe] $ lauf_cmd
> BLOCK (2):
>   - 1 rote(r) Fall/Faelle ohne deklarierten Grund
>       ::tests.test_check_interview_minimums
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>   - 35 Eintrag/Eintraege in REIST_NICHT haben keinen Fall mehr
>       tests.test_ci::test_der_echte_lesepfad_des_bead_gates_wird_erkannt
>       tests.test_ci::test_every_gate_step_has_a_mutation_test
>       tests.test_ci::test_every_script_has_a_test_or_a_declared_reason
>       tests.test_ci::test_no_declared_reason_cites_a_closed_or_unknown_bead
>       tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_caller
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
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02a-spec-review.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02b-design.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[03-plan.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[04-implement.md-GLM 5.3 Flash]
>         …
>       
>       Entweder wurde der Test umbenannt — dann den Eintrag nachziehen — oder seine Datei reist nicht mehr mit. Der zweite Fall ist der gefaehrliche: die Portabilitaet sinkt, und die gemeldete Quote steigt.
>
> INFO  (1):
>   - 0 von 1 Faellen tragen in ein fremdes Repo (0 %)
>       mechanismus 81 · bestand 302 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 7718 earlier lines left out …]
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
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 388 files, 977 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route glm · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 388 files, 978 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3 as an unrecognized model on 2026-10-13 (bead coding-harness-3fc) · leak check clean over 388 files, 980 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/adr-owning-change/plan.md` +2 -2
> - `plans/changes/criterion-test-ledger/plan.md` +16 -19
> - `scripts/check_interview_minimums.py` +3 -3
> - `tests/test_adoption.py` +0 -6
> - `tests/test_this_repository_adoption.py` +20 -0
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 389 files, 982 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th) · leak check clean over 389 files, 984 commits, 12 rules.
