---
title: "Findings — research-swarm"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — research-swarm

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1138 commits, 12 rules.

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 420 files, 1138 commits, 12 rules.

> Attempt 1 (codex): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0018-phase-1-research-swarm.md` +123 -0
> - `plans/INDEX.md` +5 -0
> - `plans/changes/research-swarm/design.md` +204 -0
> - `plans/changes/research-swarm/plan.md` +222 -0
> - `plans/changes/research-swarm/research.md` +68 -9
> - `plans/changes/research-swarm/spec.md` +239 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> .................F...................................................... [  3%]
> ........................................................................ [  7%]
> ........................................................................ [ 10%]
> .................................s..........s..................ss....... [ 14%]
> ...........................ss.sssssss..s.......s........................ [ 18%]
> ........................................................................ [ 21%]
> ........................................................................ [ 25%]
> ........................................................................ [ 29%]
> ........................................................................ [ 32%]
> ........................................................................ [ 36%]
> ........................................................................ [ 40%]
> ........................................................................ [ 43%]
> s....................................................................... [ 47%]
> ........................................................................ [ 50%]
> ........................................................................ [ 54%]
> ........................................................................ [ 58%]
> ........................................................................ [ 61%]
> ........................................................................ [ 65%]
> ........................................................................ [ 69%]
> ........................................................................ [ 72%]
> ........................................................................ [ 76%]
> ........................................................................ [ 80%]
> ........................................................................ [ 83%]
> ........................................................................ [ 87%]
> ........................................................................ [ 90%]
> ........................................................................ [ 94%]
> ........................................................................ [ 98%]
> ....................................                                     [100%]
> =================================== FAILURES ===================================
> _______________________ test_render_twice_is_byte_equal ________________________
>
>     def test_render_twice_is_byte_equal() -> None:
>         """D-54: the verification lives as a repeatable test — render twice,
>         byte-equal. Without an executable tracker (dry run) it honestly skips.
>         """
>         from render_beads_export import RendererFehlt, _render_nach
>     
>         with tempfile.TemporaryDirectory() as td:
>             erstes, zweites = Path(td) / "a.jsonl", Path(td) / "b.jsonl"
>             try:
>                 _render_nach(erstes)
>             except (RendererFehlt, SystemExit) as exc:
>                 pytest.skip(f"no executable tracker in this environment: {exc}")
>             _render_nach(zweites)
> >           assert erstes.read_bytes() == zweites.read_bytes(), (
>                 "the same tracker state must render byte-equal on the same machine"
>             )
> E           AssertionError: the same tracker state must render byte-equal on the same machine
> E           assert b'{"_type":"i...t_count":0}\n' == b'{"_type":"i...t_count":0}\n'
> E             
> E             At index 104545 diff: b'z' != b'2'
> E             Use -v to get more diff
>
> tests/test_bead_render.py:72: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_bead_render.py::test_render_twice_is_byte_equal - Assertion...
> 1 failed, 1963 passed, 16 skipped in 1088.40s (0:18:08)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9227 earlier lines left out …]
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

Stage-2 call, 2026-10-14: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 424 files, 1146 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-10-15: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 424 files, 1170 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +2 -2
> - `docs/WORKFLOW.md` +35 -13
> - `model-endpoints.yaml` +63 -3
> - `plans/changes/research-swarm/plan.md` +33 -23
> - `prompts/01-explore.md` +12 -0
> - `prompts/research-swarm/judge.md` +47 -0
> - `prompts/research-swarm/public.md` +56 -0
> - `prompts/research-swarm/repository.md` +44 -0
> - `scripts/stage2.py` +130 -8
> - `scripts/stage2_research_tools.mjs` +297 -0
> - `scripts/stage2_swarm.py` +870 -0
> - `tests/stage2_research_tools_driver.mjs` +91 -0
> - `tests/test_model_endpoints.py` +184 -1
> - `tests/test_stage2.py` +9 -1
> - `tests/test_stage2_research_tools.py` +316 -0
> - `tests/test_stage2_swarm.py` +815 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2_swarm.py`, `tests/test_model_endpoints.py`, `tests/test_stage2_swarm.py`; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1603 lines of this gate left out …]
>   - leak check clean: 20 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: the pinned Pi's model inventory does not map the free id(s) longcat-2.5-preview-free, space-bunny, hy4-preview; the free stage refuses rather than assume a provider.
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> FAILED tests/test_stage2.py::test_preparation_commands_receive_no_model_or_caller_credentials
> FAILED tests/test_stage2.py::test_the_doctrine_and_prompts_say_the_flash_verbs_are_live
> FAILED tests/test_stage2.py::test_the_doctrine_names_the_repair_verb - Assert...
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[10.9.9.9-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[192.168.1.7-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[172.16.0.9-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[172.32.0.9-False]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[100.64.0.1-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[100.128.0.1-False]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[169.254.3.4-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[0.1.2.3-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[127.0.0.1-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[8.8.8.8-False]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[::1-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[::-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[fe80::1-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[fd00::1-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[::ffff:127.0.0.1-True]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[::ffff:8.8.8.8-False]
> FAILED tests/test_stage2_research_tools.py::test_the_address_classification[2001:4860:4860::8888-False]
> FAILED tests/test_stage2_research_tools.py::test_a_redirect_whose_fresh_lookup_turns_private_is_refused
> FAILED tests/test_stage2_research_tools.py::test_a_public_fetch_pins_the_validated_address_and_records_a_receipt
> FAILED tests/test_stage2_research_tools.py::test_search_records_a_receipt_and_parses_results
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_missing_invalid_or_conflicting_class_refuses
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls[Two sentences. Here is the second one.]
> FAILED tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls[a word word word word word word word word word word word word word word word word word word word word long]
> FAILED tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls[isolation for src/app.py runs]
> FAILED tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls[isolation for myValue runs]
> FAILED tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls[the demo change's isolation]
> FAILED tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls[isolation for the demo-1 tracker work]
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 52 failed, 2012 passed, 16 skipped in 444.56s (0:07:24)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/stage2_swarm.py:754:20: ARG005 Unused lambda argument: `member`
>     |
> 752 |             "free researcher",
> 753 |             None,
> 754 |             lambda member=member, model_id=model_id, public_text=public_text: pi_public_call(
>     |                    ^^^^^^ ARG005
> 755 |                 runner,
> 756 |                 public_text,
>     |
>
> scripts/stage2_swarm.py:843:5: SIM108 Use ternary operator `judge_faults = ["the judge call failed"] if reconciliation is None else judge_problems(str(reconciliation), tracked)` instead of `if`-`else`-block
>     |
> 841 |           "ok",
> 842 |       )
> 843 | /     if reconciliation is None:
> 844 | |         judge_faults = ["the judge call failed"]
> 845 | |     else:
> 846 | |         judge_faults = judge_problems(str(reconciliation), tracked)
>     | |___________________________________________________________________^ SIM108
> 847 |       if judge_faults:
> 848 |           failed.append("judge: " + "; ".join(judge_faults))
>     |
>     = help: Replace `if`-`else`-block with `judge_faults = ["the judge call failed"] if reconciliation is None else judge_problems(str(reconciliation), tracked)`
>
> Found 2 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9282 earlier lines left out …]
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

Stage-2 call, 2026-10-15: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 432 files, 1174 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +1 -1
> - `docs/WORKFLOW.md` +3 -3
> - `plans/changes/research-swarm/plan.md` +29 -22
> - `scripts/ci_gates.py` +4 -0
> - `scripts/stage2_research_tools.mjs` +9 -5
> - `scripts/stage2_swarm.py` +17 -9
> - `tests/stage2_research_tools_driver.mjs` +5 -1
> - `tests/test_stage2.py` +2 -2
> - `tests/test_stage2_research_tools.py` +38 -0
> - `tests/test_stage2_swarm.py` +8 -5
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 146 lines of this gate left out …]
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> swarm: six reconciled topics appended to plans/changes/demo/research.md · run swarm-35e8e96a
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> swarm: six reconciled topics appended to plans/changes/demo/research.md · run swarm-c6902298
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_the_doctrine_and_prompts_say_the_flash_verbs_are_live
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> 3 failed, 2062 passed, 16 skipped in 465.10s (0:07:45)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9335 earlier lines left out …]
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

Stage-2 call, 2026-10-15: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 432 files, 1181 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +1 -0
> - `plans/changes/research-swarm/plan.md` +2 -0
> - `scripts/stage2_swarm.py` +1 -1
> - `tests/test_stage2_swarm.py` +1 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 40 lines of this gate left out …]
> __________ test_the_doctrine_and_prompts_say_the_flash_verbs_are_live __________
>
>     def test_the_doctrine_and_prompts_say_the_flash_verbs_are_live() -> None:
>         paths = ["docs/WORKFLOW.md", "AGENTS.md", "prompts/01-explore.md", "prompts/03-plan.md", "prompts/04-implement.md"]
>         texts = {name: (REPO_ROOT / name).read_text(encoding="utf-8") for name in paths}
>         assert flash_runner_doctrine_problems(texts) == []
>         for name, needle, replacement in (
>             ("docs/WORKFLOW.md", "--stage2-off [REASON]", "automatic fallback"),
>             ("AGENTS.md", "without fallback", "with fallback"),
>             ("prompts/01-explore.md", "stage2.py explore <change>", "stage2.py research <change>"),
>             ("prompts/04-implement.md", "file tools but no command tool", "all tools"),
>             ("prompts/03-plan.md", "copy that route,\n  model and reason into `plan.md`", "remember it"),
>         ):
>             assert needle in texts[name]
>             planted = {**texts, name: texts[name].replace(needle, replacement)}
> >           assert flash_runner_doctrine_problems(planted), (name, needle)
> E           AssertionError: ('docs/WORKFLOW.md', '--stage2-off [REASON]')
> E           assert []
> E            +  where [] = flash_runner_doctrine_problems({'AGENTS.md': '# coding-harness — Agent Instructions\n\nThe home of the coding workflow: **seven phases, three stages*...r`. The plan is a file; whoever executes it does not need your\nreasoning, and fresh context beats continuity.\n', ...})
>
> tests/test_stage2.py:6690: AssertionError
> _________________ test_agents_md_names_the_loop_and_the_runner _________________
>
>     def test_agents_md_names_the_loop_and_the_runner() -> None:
>         text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
>         assert agents_md_problems(text) == []
> >       assert text.count("\n") <= 200
> E       AssertionError: assert 201 <= 200
> E        +  where 201 = <built-in method count of str object at 0x798f588000>('\n')
> E        +    where <built-in method count of str object at 0x798f588000> = '# coding-harness — Agent Instructions\n\nThe home of the coding workflow: **seven phases, three stages**, the session...nce of the workflow |\n| `oracle-source-inventory` | customer instance — read-only boundary for framework sessions |\n'.count
>
> tests/test_stage2.py:6779: AssertionError
> ________________ test_phase_one_doctrine_and_declarations_agree ________________
>
>     def test_phase_one_doctrine_and_declarations_agree() -> None:
>         # Criterion 22. Planted fault: universal single-explorer prose, an unresolvable roster or a changed ladder.
>         data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
>         assert stage2_swarm.swarm_problems(data) == [], "the declared swarm block must resolve"
>         go = next(entry for entry in data["endpunkte"] if entry["name"] == "opencode-go")
>         assert go["modelle"] == ["deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"], (
>             "the review ladder keeps its order; the swarm block changes it in no way"
>         )
>         roster = set(data["research_swarm"]["free_roster"])
>         assert roster.isdisjoint(go["modelle"]), "no free id joined the Go ladder"
>         roles = data["research_swarm"]
>         assert roles["judge"] == roles["topic_author"] == "claude-opus-5-5"
>         agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
> >       assert "so does phase 1 now (ADR 0018)" in agents
> E       AssertionError: assert 'so does phase 1 now (ADR 0018)' in '# coding-harness — Agent Instructions\n\nThe home of the coding workflow: **seven phases, three stages**, the session...nce of the workflow |\n| `oracle-source-inventory` | customer instance — read-only boundary for framework sessions |\n'
>
> tests/test_stage2_swarm.py:807: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_entry_points.py::test_instruction_file_is_under_200_lines
> FAILED tests/test_stage2.py::test_the_doctrine_and_prompts_say_the_flash_verbs_are_live
> FAILED tests/test_stage2.py::test_agents_md_names_the_loop_and_the_runner - A...
> FAILED tests/test_stage2_swarm.py::test_phase_one_doctrine_and_declarations_agree
> 4 failed, 2061 passed, 16 skipped in 466.52s (0:07:46)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [criterion-ledger] $ lauf_cmd
> plans/changes/research-swarm/plan.md:165: criterion 1: "test_large_classes_dispatch_the_swarm" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:166: criterion 2: "test_small_classes_keep_the_single_explorer" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:167: criterion 3: "test_explicit_class_explores_without_spec_or_plan" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:168: criterion 4: "test_missing_invalid_or_conflicting_class_refuses" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:169: criterion 5: "test_all_free_roles_are_attempted_before_flash" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:170: criterion 6: "test_six_topics_have_independent_permitted_pairs" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:171: criterion 7: "test_research_carries_practice_architecture_and_adjacent_spec_comparisons" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:172: criterion 8: "test_public_requests_exclude_every_private_input" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:174: criterion 9: "test_public_tools_cannot_read_local_or_private_sources" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:176: criterion 10: "test_public_claims_require_retrieved_source_receipts" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:177: criterion 11: "test_declarations_clear_only_the_role_data_class" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:178: criterion 12: "test_every_call_is_checked_and_a_leak_block_stops_dispatch" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:179: criterion 13: "test_every_attempt_has_identity_audit_and_outcome" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:180: criterion 14: "test_fresh_opus_reconciles_all_six_topics" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:181: criterion 15: "test_unresolved_dissent_and_human_questions_survive_reconciliation" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:182: criterion 16: "test_local_citations_bind_to_the_frozen_input_state" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:183: criterion 17: "test_only_the_runner_appends_research" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:184: criterion 18: "test_failures_preserve_evidence_and_never_report_complete" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:185: criterion 19: "test_deadlines_and_role_counts_bound_the_run" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:187: criterion 21: "test_all_outputs_scrub_every_used_credential" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:188: criterion 22: "test_phase_one_doctrine_and_declarations_agree" exists — remove `not yet written` from the entry
> plans/changes/research-swarm/plan.md:190: criterion 23: "test_public_topic_is_filtered_before_free_calls" exists — remove `not yet written` from the entry
> ── [criterion-ledger] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9383 earlier lines left out …]
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

Stage-2 call, 2026-10-15: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 432 files, 1190 commits, 12 rules.
