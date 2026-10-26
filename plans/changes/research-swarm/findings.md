---
title: "Findings — research-swarm"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-17
updated: 2026-10-26
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
> - `docs/adr/0019-phase-1-research-swarm.md` +123 -0
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
> >       assert "so does phase 1 now (ADR 0019)" in agents
> E       AssertionError: assert 'so does phase 1 now (ADR 0019)' in '# coding-harness — Agent Instructions\n\nThe home of the coding workflow: **seven phases, three stages**, the session...nce of the workflow |\n| `oracle-source-inventory` | customer instance — read-only boundary for framework sessions |\n'
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

Stage-2 call, 2026-10-15: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 432 files, 1191 commits, 12 rules.

Stage-2 call, 2026-10-15: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 432 files, 1193 commits, 12 rules.

## Phase 6 — Opus 5.5, 2026-10-15

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `plans/changes/research-swarm/plan.md`, build step 2, "Verification" and criterion ledger lines for 8 and 9; `plans/changes/research-swarm/research.md` | The offline capture with the real pinned Pi 1.1.0, synthetic private canaries and a local mock model server has not been run: neither `research.md` nor any other file of the change records its version, source hashes, method or canary outcomes. The plan places it in build step 2, before step 3 and before the decision pull request, and says its evidence belongs in the research artefact; the Definition of Done lists it beside `make verify`, separately from the live qualification that alone is deferred until after the merge. It contacts no external endpoint, so nothing in the spec defers it. The criterion ledger rests criteria 8 and 9 partly on it ("not a test"), so the actual Pi prompt, tool schemas and outbound payloads of a free context are unproven: every test of the boundary drives a stand-in that only records its own argv and environment. F-2 shows the capture would not have passed. [Definition of Done; criteria 8, 9] | Opus 5.5 | fixed — not a test — attended real-Pi offline capture passed at 3629fa7 on 2026-10-19T13:10:39Z, all six checks (research.md, "F-1 attended offline capture — second run, 2026-10-19"); closed by the maintainer's ruling, 2026-10-19 ("ja") | — |
| F-2 | MAJOR | SPEC | base | `scripts/stage2_research_tools.mjs:286-297`; `scripts/stage2_swarm.py:460-502`; `tests/test_stage2_swarm.py:104-108` | Read against the installed Pi 1.1.0 itself, the free-researcher route cannot work. (a) Pi calls a registered tool as `execute(toolCallId, params, signal, onUpdate, ctx)` (`dist/core/tools/tool-definition-wrapper.js`) and expects a TypeBox parameter schema and a `{content, details}` result (`docs/extensions.md`, "Tools"); the extension's `execute: async ({ query })` destructures the tool-call id string, so `public_search` searches for `undefined` and `public_fetch` always throws "a destination URL is required", its `parameters: { query: "string" }` is no JSON schema, and it returns a bare string. (b) `pi --list-models` prints a padded `provider  model  context …` table of the models whose provider has usable authentication (`dist/cli/list-models.js`), while `free_transport` runs it with no key in the environment and parses only JSON lines or `provider/id` tokens; with the real binary the mapping is empty, every free id is "unmapped", and every `feature` or `architectural` explore stops before the free stage with exit 1. The stand-in answers the inventory with JSON lines the real Pi never prints and never invokes the extension the way Pi does, so the suite is green over a route that cannot run. When the mapping does parse, it also takes whichever provider Pi lists last for an id, not one tied to the `opencode-free` declaration. [criteria 1, 10, 11] | Opus 5.5 | fixed — the extension implements Pi 1.1.0's `execute(toolCallId, params, …)` with JSON-schema parameters and a `{content, details}` result, and the inventory reads Pi's padded `--list-models` table with the OpenCode key, never maps a free id to the paid Go provider and refuses an ambiguous one (tests/test_stage2_research_tools.py::test_the_tools_run_as_pi_calls_them, ::test_the_tool_parameters_are_json_schemas; tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints), 4f5ecfd | |
| F-3 | MAJOR | SPEC | base | `scripts/stage2_swarm.py:832-843`; `scripts/stage2_swarm.py:667-676` | A free researcher whose public-web tools fail, or which never calls them and answers from memory without a URL, is recorded as a successful contribution: `receipt_problems` only checks URLs the report cites, so a report with no URL and no fetch receipt raises no failure. If the judge then cites no public URL, the run ends `complete` with exit 0 although no public page was retrieved — exactly the "unavailable public-web path" case (F-2 makes it the expected one once the inventory parses). A free contribution with no successful fetch receipt should mark its slot failed and the run incomplete. No test plants a URL-free report without receipts. [criteria 10, 18] | Opus 5.5 | fixed — a free contribution with no successful page retrieval marks its slot failed and the run incomplete, its report kept and marked (tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution), 861e4dc | |
| F-4 | MAJOR | SPEC | base | `scripts/stage2_swarm.py:77`; `scripts/stage2_swarm.py:638-664`; `tests/test_stage2_swarm.py:618-635` | The topic filter treats any token of letters and hyphens as a plain word, so the repository's dominant identifier shape passes: another bead id without a digit (`coding-harness-yim`), the repository name, an endpoint name such as `claude-code-plan` or `opencode-free`, or another change's folder name in a topic sentence reaches every free model, because only this change's own name and bead are compared and the default leak check holds denylist terms, not repository identifiers. The filter's tests use only identifiers with a digit, a slash, camel case or this change's names, so nothing holds the case. [criterion 23] | Opus 5.5 | fixed — a topic word is letters and apostrophes only, so every hyphenated token is refused and the topic author is told so (tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_free_calls, five new cases), 861e4dc | |
| F-5 | MINOR | SPEC | base | `scripts/stage2_swarm.py:529-547`; `scripts/stage2_research_tools.mjs:298-308` | The free researcher's Pi command passes neither `--no-tools` nor `--tools public_search,public_fetch`, so Pi's default built-in tools stay active and are declared to the free model; only the extension's `tool_call` hook blocks them at call time. Pi blocks on a failing handler and exits on a failed extension load, so no leaking case is shown, but the design asks for no built-in file or shell tools and the criterion is refuted by an available one; an allow-list on the command line would make the boundary hold without the hook. [criterion 9] | Opus 5.5 | fixed — the free Pi runs with `--tools public_search,public_fetch`, the hook stays as the second layer (tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input asserts the argv), 861e4dc | |
| F-6 | MINOR | SPEC | base | `scripts/stage2_swarm.py:81-83`; `scripts/stage2_swarm.py:320-338`; `scripts/stage2.py:415-440` | After the 150-minute run deadline, `allowance` returns 0 but the runner still gates the next slot, writes a "leak check clean" audit line for it, and launches the process with `timeout=0`, which `subprocess.run` starts and then kills; a run whose Flash stage ends at minute 151 still starts the judge's Claude Code process. The design says the total deadline stops dispatch and records the unfinished slots; the test asserts only the value of `allowance`, not that no process starts. [criterion 19] | Opus 5.5 | fixed — a slot whose whole-run allowance is spent is recorded unfinished before its gate: no leak-check line, no process, the judge included (tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent), cb3733d | |
| F-7 | MINOR | MAINT | base | `scripts/stage2_swarm.py:259-278`; `scripts/stage2.py:500-515` | `runner.append` re-stamps the `updated:` line of `research.md` on every append, and the publication check requires the file to begin with its frozen bytes. A run that crosses midnight therefore changes its own frozen prefix and ends incomplete with "the frozen input state changed: plans/changes/<change>/research.md", although no input changed. [criteria 17, 18] | Opus 5.5 | fixed — the publication check blanks the header's `updated:` value of this change's research.md on both sides, so the runner's own re-stamp after midnight is no input change (tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research), cb3733d | |
| F-8 | MINOR | SPEC | base | `scripts/stage2_swarm.py:702-725` | The judge's local citations are validated only in the backticked `path::symbol` form and only by path: `src/app.py::no_such_symbol` passes because the path is tracked, and a citation written with only a line number (`src/app.py:12`) or as a bare path is not checked at all. A local claim can thus stand on a nonexistent symbol or on line numbers alone. [criterion 16] | Opus 5.5 | fixed — every `path::symbol` must name a tracked path whose frozen bytes hold the symbol; line-only and bare-path citations are refused, and the judge prompt says so (tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol), cb3733d | |
| F-9 | MINOR | SPEC | base | `scripts/stage2.py:2380-2391` | A `research.md` or `spec.md` header that does not parse as YAML, or that states an empty `class:`, is treated as stating no class: with `--class feature` the swarm runs although the file may say `bounded`. The design says a present invalid header refuses and an explicit argument does not cure it. [criterion 4] | Opus 5.5 | fixed — a header that does not parse as YAML fields, or a present empty `class:`, refuses with exit 2 and an explicit `--class` does not cure it (tests/test_stage2_swarm.py::test_an_unreadable_header_or_empty_class_refuses), cb3733d | |
| F-10 | MAJOR | SPEC | base | `scripts/stage2_research_tools.mjs` `searchWeb`/`parseResults`/`validateDestination`; `scripts/stage2_swarm.py` `public_prompt` | Raised from kept loop text R2-1 (mimo-v2.6-flash): the search tool returns DuckDuckGo redirect wrappers (`//duckduckgo.com/l/?uddg=…`) instead of destination URLs, so a receipt is recorded against the wrapper while a citation of the real page has no receipt, and the wrapper cannot be fetched because `validateDestination` refuses its scheme — a live public run marks real citations unbacked and exits 1. [criterion 10] | Opus 5.5 (from loop text) | fixed — search results carry the `uddg` destination, validated like any destination, wrappers without one dropped (tests/test_stage2_research_tools.py::test_search_results_carry_the_decoded_destination), 4f5ecfd | |

Checked: all 23 acceptance criteria and the Definition of Done of `spec.md`, the interfaces, data model and architecture delta of `design.md`, and the ADR draft `docs/adr/0020-phase-1-research-swarm.md`, against `git diff origin/main...HEAD` (fetched 2026-10-15, HEAD d4e15e3). The boundary was read end to end: what the topic author receives and what the filter accepts; the free prompt (`prompts/research-swarm/public.md` with the topic and focus only); the free environment (PATH, scratch HOME and agent directory, the OpenCode key, the receipts path); the scratch copies of prompt and extension; the extension's destination checks (HTTPS, port 443, no credentials, every DNS answer checked, pinned connection, re-validated redirects); receipt parsing and citation checks; the per-call gate (declaration, exact-prompt leak check, audit line, exit 2 with no further call); the frozen input digest; scrubbing of answers, partial output, stderr and receipts; class routing and the `--stage2-off` path; `model-endpoints.yaml` (the ladder unchanged, `opencode-free` cleared for `public-web` only with residency `nicht-erklaert`); and the doctrine in `AGENTS.md`, `docs/WORKFLOW.md` and `prompts/01-explore.md`. The pinned Pi's behaviour was read from its installed source and documentation (`/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent`, version 1.1.0); no Pi or model was run. The offline capture is a pre-merge requirement (F-1): the plan puts it in build step 2 and only the live qualification is post-merge. On the test count: the four test files of this change collect 158 tests and all 158 run and pass under `.venv` (none skipped; the research-tools suite skips only without `node`, which CI's ubuntu runner has), so no test of this change is silently left out of `make verify`; the full suite collected 2100 tests on this run, and `make verify` reported 2084 passed and 16 skipped — the same 2100, so on this tree no collected test is left out; the earlier counts (2081 collected, 2038 + 16 run) were not reproduced and their cause was not measured. No finding on criteria 2, 3, 5, 6, 7, 11 (declaration side), 12, 13, 14, 15, 17 (participants), 20, 21 and 22 beyond the rows above.

Phase 6 verdict: opus-5.5, 2026-10-15
Reviewer session: none — a fresh Claude context reviewed; no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-15

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | base | `scripts/stage2_swarm.py` `pi_public_call` and `pi_repository_call` | A Pi participant that retrieved pages and then failed loses its partial evidence: the receipts file is read and dropped when the process exits nonzero or the answer is empty, a timeout discards it with the scratch directory because the read happens only after the launch returns, and the partial stdout is never read at all, so the record keeps only the exit status while `docs/WORKFLOW.md` promises a failed participant preserves its partial evidence and spec criterion 18 requires it. | deepseek-v4.1-flash | fixed — tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence | no | agree |
| L1-2 | MAJOR | MAINT | base | `scripts/stage2_swarm.py` `run` (free stage and judge prompt) and `model-endpoints.yaml` `research_swarm` | The declared free-researcher assignment shapes nothing: every free model receives the same six-question public brief, and the judge receives all free reports concatenated under a heading that claims six pairs, with no per-topic mapping, so `free_focuses` and `topic6_free` never reach a prompt and the design's declared pairing (one free model per topic, a specific free seat on topic 6) is not what the reconciliation sees. | deepseek-v4.1-flash | fixed — tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs | no | agree |
| L1-3 | MAJOR | MAINT | base | `scripts/stage2_swarm.py` `swarm_roles` and `run`; `scripts/stage2.py` `TOPIC_CALL` and `JUDGE_CALL` | The declaration's `paid_endpoint`, `topic_author` and `judge` are validated but never used: the topic and reconciliation calls go to the hardcoded `TOPIC_CALL` and `JUDGE_CALL` tuples, so a declaration naming another paid author or judge passes validation and still runs Opus, while the `research_swarm` comment says the roles are declared, not hardcoded in a script. | deepseek-v4.1-flash | fixed — tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called | no | agree |
| L1-4 | MAJOR | SPEC | base | `scripts/stage2_swarm.py` `judge_problems`, `receipt_problems` and `run` | The judge's reconciliation is published without any check of its public citations: `receipt_problems` runs only on the free reports, so an invented URL or a snippet-only claim in the judge's supported facts lands in `research.md` unchecked, although criterion 10 requires every public claim to carry a retrieved page's URL, title, date and excerpt. | deepseek-v4.1-flash | fixed — tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts | no | agree |
| L1-5 | MINOR | MAINT | base | `scripts/stage2_swarm.py` `pi_public_call`; `scripts/stage2.py` `foreign_env` and `ENV_ALLOW`; `plans/changes/research-swarm/design.md` | The free context inherits `USER`, `LOGNAME`, `SHELL`, `TMPDIR`, the locale variables and `CODEX_HOME` through the shared environment allow-list, while the design states that its environment carries only required runtime settings and the transport credential and that user identity and private paths are not inherited; the swarm tests record the environment but assert nothing about these variables. | deepseek-v4.1-flash | fixed — tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths | no | agree |
| L1-6 | MINOR | MAINT | base | `docs/WORKFLOW.md` §4, `AGENTS.md` and `prompts/01-explore.md` versus `scripts/stage2.py` `declared_class` | The doctrine says explore takes the class from `--class` or `research.md`'s header, but the runner also reads the class in `spec.md` and refuses when the two headers, or the argument and a header, disagree, so an operator following the documentation cannot predict the refusal. | deepseek-v4.1-flash | fixed — not a test — corrected all three routing documents to name both headers and refuse disagreeing declarations | no | agree |
| L1-7 | MINOR | MAINT | base | `scripts/stage2_swarm.py` `receipt_problems` | A correctly retrieved page is treated as unbacked whenever the free report cites the requested URL and the receipt's `final_url` differs after a redirect, because the backed set is built from `final_url or url` and the receipt's `url` is ignored; the run then exits 1 as incomplete although no source is missing. | deepseek-v4.1-flash | fixed — tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls | no | agree |
| L1-8 | MINOR | MAINT | base | `scripts/stage2_research_tools.mjs` `validatedAddress` and `nodeTransport` | The pinned request declares family 4 for whatever address validation chose: `validatedAddress` returns the first lookup answer and the transport callback hands it to the socket as family 4 regardless of its real family, so a public host that resolves IPv6 first, or only to IPv6, cannot be retrieved. | deepseek-v4.1-flash | fixed — tests/test_stage2_research_tools.py::test_node_transport_pins_the_resolved_ipv6_family | no | agree |

Rounds run: 2

Kept from the loop record:

mimo-v2.6-flash answered in table lines that are not six-cell rows; they are kept as they came.
The answer was not only six-cell rows; what is not one is kept below as it came.

| R2-1 | BLOCKER | MAINT | runner | scripts/stage2_swarm.py · `public_prompt`; scripts/stage2_research_tools.mjs · `searchWeb`/`parseResults`/`validateDestination` |
The free researchers are told every claim cites a page they actually retrieved, but the only retrieval tool returns DuckDuckGo HTML-endpoint redirect wrappers in `result__a` hrefs (`//duckduckgo.com/l/?uddg=…`), never the destination URL; the receipt is recorded against the wrapper URL, while a citation of the real page URL is backed by no receipt, and the wrapper itself cannot be fetched to fix this because `validateDestination` refuses its non-HTTPS scheme — so a live public run's real-page citations are marked "citations no receipt backs" and the run exits 1 through no fault of the researcher, or the researcher cites no page at all. |
| R2-2 | MAINT | MAINT | runner | scripts/stage2_swarm.py · `allowance` and every call site (`pi_public_call`, `pi_repository_call`, `run_work_model`); scripts/stage2.py · `launch` |
After the 150-minute whole-run deadline the allowance computes to 0.0, which is passed as the subprocess timeout; a zero timeout disables the subprocess timeout instead of refusing the call, so a Flash or free call that starts with no remaining budget runs unbounded — directly the refuting case the spec names, "a call after the total deadline", and no test covers a 0.0 allowance reaching a real launch. |
| R2-3 | MAINT | MAINT | runner | scripts/stage2_swarm.py · `free_transport` |
The `pi --list-models` inventory call is launched with an environment carrying only `HOME` and `PI_CODING_AGENT_DIR` — the OpenCode credential is not in it — so the real pinned-Pi inventory, which reaches the OpenCode provider, cannot authenticate; only the argv stand-in in the tests answers it, and every live feature or architectural change would fail at the free stage before any researcher runs. |
| R2-4 | MAINT | SPEC | runner | scripts/stage2_swarm.py · `judge_problems` |
Local citations are validated only in the exact `` `path::symbol` `` form, so a bare-path citation in a judge's supported facts — `src/app.py`, `plans/specs/…` — passes without any tracked-path or input-state binding, and a section that cites local facts entirely without the required form passes too; criterion 16's traceability to the frozen state is not enforced for either shape, and no test plants them. |
| R2-5 | MAINT | MAINT | runner | scripts/stage2_swarm.py · `receipt_problems` |
The backed-URL set admits any fetch receipt whose status is 200 regardless of the receipt's own `kind`, so a receipt written with `kind: "search"` and status 200 backs a citation the search tool never retrieved — the criterion-10 distinction between a search result and a retrieved page is enforced only by the run's own fixture, not by the validator. |
| R2-6 | MINOR | MAINT | origin | AGENTS.md · stage-2 paragraph |
The rewritten sentence now reads "Reviews go by class, and so does phase 1 now", making phase-1 exploration a review; the framework's phase 1 carries no review, and the same table's own wording routes only explore, draft, implement and repair — a maintainer reading this line gets the phase-1 change backwards. |
| R2-7 | MINOR | MAINT | runner | scripts/stage2_swarm.py · `build_packet` and `input_state_holds` |
Publication re-reads and byte-compares every tracked file of the repository after a run that can last 150 minutes, so any unrelated tracked write anywhere in the tree — an editor's autosave, a concurrent stage elsewhere — fails the whole run as "the frozen input state changed", discarding sixteen completed calls' evidence status even though nothing the swarm depends on changed; the digest names the changed path only after the fact. |

Triage of the kept round-2 text (orchestrating session, 2026-10-15): R2-1 raised as F-10; R2-2 is F-6, R2-3 is F-2, R2-4 is F-8 (taken there); R2-5 rejected — `receipt_problems` already requires `kind == "fetch"` (phase-6 reading); R2-6 rejected — the sentence says phase 1 goes by class, not that it is a review; R2-7 rejected — the whole-tree freeze is the design's deliberate trade-off. The runner dropped these rows because their ids were `R2-n`, not `L2-n`, and reported "0 rows" — a runner gap named in the night handover.

Stage-2 call, 2026-10-15: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 453 files, 1253 commits, 12 rules.

Stage-2 call, 2026-10-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 484 files, 1355 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0020-phase-1-research-swarm.md` +32 -13
> - `plans/changes/research-swarm/design.md` +80 -30
> - `plans/changes/research-swarm/plan.md` +85 -42
> - `plans/changes/research-swarm/research.md` +60 -2
> - `plans/changes/research-swarm/spec.md` +76 -29
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-1wyi16xg.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 578.54s (0:09:38)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 11941 earlier lines left out …]
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

Stage-2 call, 2026-10-16: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 484 files, 1355 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0020-phase-1-research-swarm.md` +2 -0
> - `plans/changes/research-swarm/design.md` +9 -0
> - `plans/changes/research-swarm/plan.md` +41 -4
> - `plans/changes/research-swarm/research.md` +27 -0
> - `plans/changes/research-swarm/spec.md` +6 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-rmj7tgrn.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 608.32s (0:10:08)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 11989 earlier lines left out …]
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

Stage-2 call, 2026-10-16: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 484 files, 1355 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/design.md` +6 -5
> - `plans/changes/research-swarm/plan.md` +7 -0
> - `plans/changes/research-swarm/research.md` +23 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-tx64vny9.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 563.03s (0:09:23)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12037 earlier lines left out …]
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

Stage-2 call, 2026-10-16: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 484 files, 1356 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-16

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | `spec.md`, Terms «Complete» and «Selected Go free models»; criteria 18, 37, 39; [DETAIL] `39 + 3N` | [AMBIGUITY] It is unclear whether a selected Go free seat is a required contribution. Reading A: criterion 39, «every required contribution» and «unfinished slots remain explicit and incomplete» make all 3N free slots required. Then one free model that times out, is refused or returns no receipt makes the whole run incomplete with a nonzero exit, and the «completed swarm» of criteria 30–31 never happens. The free roster changes constantly, so many runs could end like this. Reading B: criterion 37 calls only the nine Flash contributions «mandatory», and the Terms say «catalog presence is eligibility, not proof a model call will succeed». Then free slots are best-effort, a failure is recorded, and the run can still be complete. The same run gets opposite exit codes under the two readings. | Opus | in spec — Terms; criteria 18, 39; budget detail (ruling S-1, decisions.md, 2026-10-16) | — |
| S-2 | MAJOR | SPEC | base | `spec.md`, Terms «Selected Go free models»; criteria 38, 41; `research.md`, 2026-10-16 «A listing is not proof of a live refresh» | [AMBIGUITY] It is unclear which ids a successful refresh makes eligible. `research.md` records that pinned Pi merges the shipped baseline with the fetched remote overlay. Reading A: every `-free` id in the merged catalog is eligible. A baseline id that the fetched shard no longer lists is still selected and dispatched. Reading B: only ids in this run's fetched overlay are eligible, and baseline-only ids are dropped. Criterion 38 refutes a «shipped … list» used instead of a refresh. It does not say whether shipped entries inside a refreshed catalog count. So a test with a baseline-only `x-free` id has no defined expected selection. | Opus | in spec — Terms; criterion 38 (ruling S-2, decisions.md, 2026-10-16) | — |
| S-3 | MINOR | SPEC | base | `spec.md`, Terms «Selected Go free models»; criterion 10 | Missing: «chat ids» names no catalog property that separates chat from non-chat models. Nothing says whether an eligible model must support the tool calls that produce retrieval receipts. The implementer has to invent the eligibility test. A `-free` id without tool support would be selected and could only produce a report without receipts. | Opus | in spec — Terms; criterion 39 (ruling S-3, decisions.md, 2026-10-16) | — |
| S-4 | MAJOR | SPEC | base | `spec.md`, Terms «Public topic»; criterion 23; `decisions.md` Q-6 | [AMBIGUITY] The topic filter can be read two ways in two places. (1) «Words contain letters and apostrophes only» refuses every hyphen. That rejects ordinary compounds such as «multi-agent» and the maintainer's own Q-6 example «Container-Isolation für KI-Agenten-Läufe». The next sentence's «including hyphenated identifiers» reads as refusing only identifiers like `research-swarm`. The spec also does not say whether non-ASCII letters (für, Läufe) count as letters. (2) Refusing «code, change and bead names» can mean the character rule alone, so a letters-only symbol or change name such as `explore` passes. It can also mean matching against names from the frozen repository, which refuses ordinary words that are also symbol names and needs a name source the spec does not give. The same Opus sentence passes under one reading and is refused under the other. | Opus | in spec — Public topic term; criterion 23 (ruling S-4, decisions.md, 2026-10-16) | — |
| S-5 | MAJOR | SPEC | base | `spec.md`, criteria 5, 12, 18, 23, 36; [DETAIL] stage order | Missing: what the run does after a required slot fails in a stage that later stages depend on. There are no retries. A failed finder, a failed or timed-out map merge, or a topic sentence the filter rejects leaves later stages without input. The spec does not say whether the runner stops there or continues the stages that do not depend on the failure (for example topics 1–8 without the online topics). It also does not say whether a rejected topic counts as a «security refusal» or a failed structured result. A security refusal stops dispatch and exits 2 like a leak BLOCK (criterion 36). A failed result makes the run incomplete with exit 1 (criterion 18). The two choices dispatch different calls and exit differently on the same input. | Opus | in spec — criteria 5, 18, 23, 36; stage detail (ruling S-5, decisions.md, 2026-10-16) | — |
| S-6 | MINOR | SPEC | base | `spec.md`, criteria 12, 18, 36 | Missing: what happens to calls already in flight when a leak check BLOCKs. Up to four per provider can be running, and each passed its own leak check. The spec only says no further call is dispatched. The implementer has to invent three things. Are in-flight calls killed or awaited? Are their answers kept as partial evidence? If slots are also missing, which exit code wins, 2 or 1? | Opus | in spec — criteria 12, 36; stage detail (ruling S-6, decisions.md, 2026-10-16) | — |
| S-7 | MAJOR | SPEC | base | `spec.md`, criterion 19; [DETAIL] deadlines and provider queues | Missing: how the 150-minute total is split between the topic stage and the judge, and in what order queued slots are dispatched. Worst case, with every call using its full deadline: 26 minutes before the topic stage (catalog 1, finder 10, merge 10, topic 5). Then the Go queue takes ceil((25+3N)/4)×10 minutes, and the judge takes 15. At N=6 that is 151 minutes. If no time is reserved for the judge, it cannot start and the run ends without a reconciliation. The dispatch order (fixed slots first, or by topic and model) decides which slots stay unfinished. The spec states neither. | Opus | in spec — criterion 19; deadline detail (ruling S-7, decisions.md, 2026-10-16) | — |
| S-8 | MAJOR | SPEC | base | `spec.md`, criteria 13, 16; [DETAIL] «Same-topic peers see identical frozen inputs» | Missing: what the «recorded frozen input state» is and what happens when it changes. It could be the HEAD commit. Then uncommitted worktree content, which the repository seats can read with their file tools, cannot resolve. It could also be a snapshot or hash of the working tree. The spec also does not say what happens when another session or worktree edits a mapped file during the run of up to 150 minutes: abort, incomplete result, or only a record. So criterion 16's refutation «a different source state» has no expected result. | Opus | in spec — Frozen input term; criterion 16; digest detail (ruling S-8, decisions.md, 2026-10-16) | — |
| S-9 | MAJOR | SPEC | base | `spec.md`, criteria 10, 16, 18, 27 | [AMBIGUITY] It is unclear whether an evidence failure rejects one claim or the whole report. Criterion 27 makes a template violation reject the report. Criteria 10 and 16 only say that a claim without a receipt, or with an unresolved reference, is not evidence. Reading A: that claim is dropped or marked unsupported, and the report remains a valid contribution. Reading B: the report is malformed, its slot is missing and the run is incomplete under criterion 18. Criterion 18 also names a failed «required … retrieval» without saying which retrieval is required. Under one reading a single failed fetch among a model's retrievals fails the slot. Under the other only a report with no receipt-backed claim fails, as in «a URL-free online report». | Opus | in spec — criteria 10, 16, 18; evidence-floor detail (ruling S-9, decisions.md, 2026-10-16) | — |
| S-10 | MAJOR | SPEC | base | `spec.md`, Terms «Claim» and «Handoff item»; template under Topic contract; criteria 27, 31–34 | Missing: the identity scheme that the research-to-interview-to-spec chain depends on. Claims are «uniquely identified», but the scope is not given. If ids are unique per report, ids that isolated models write independently will collide across 33+3N reports, and the «duplicate claim id» case in criterion 33 has no defined meaning. If ids must be unique across the run, isolated models cannot coordinate them. The template's questions have no id and no link to the claims they come from. Yet criterion 31 requires items «with source claim ids» and refutes «a question loses its originating claims». The spec also does not say where in a `decisions.md` Q-record the item or claim link lives, although criterion 32 checks that link. | Opus | in spec — Claim/Handoff terms; report template; criteria 27, 31, 33 (ruling S-10, decisions.md, 2026-10-16) | — |
| S-11 | MAJOR | SPEC | base | `spec.md`, criteria 31, 32; [DETAIL] raw claims and handoff inventory; [DETAIL] the gate checks «coverage» | [AMBIGUITY] It is unclear what the lost-decision coverage is measured against. Reading A: every `[DECISION]` question in every retained raw report must map to a handoff item. Then duplicates from the three peers, and decisions in reports the judge scored off-brief or refuted, all become interview obligations. Reading B: coverage is measured against the judge's handoff inventory. Then a decision the judge drops is invisible to the gate, which is exactly the loss criterion 31 targets. The gate passes or fails on the same run depending on the reading. | Opus | in spec — criteria 31, 32; raw-coverage detail (ruling S-11, decisions.md, 2026-10-16) | — |
| S-12 | MAJOR | SPEC | base | `spec.md`, criterion 32; Terms «Complete»; [DETAIL] the gate checks runs in live change folders; Definition of Done, `make verify` | [AMBIGUITY] It is unclear when the blocking handoff check applies. Reading A, from «before the spec can pass»: open items fail the check only once a spec exists. Reading B, from «checks every such run in live … change folders»: a complete run whose items still await phase 1a makes `make verify` and CI red from the end of phase 1 until the interview is answered. «Complete» explicitly allows that state. | Opus | in spec — criterion 32; pre-spec gate detail (ruling S-12, decisions.md, 2026-10-16) | — |
| S-13 | MAJOR | SPEC | base | `spec.md`, criteria 18, 30, 31; [DETAIL] «the gate checks every such run» | [AMBIGUITY] It is unclear how incomplete and repeated runs are handled. Criteria 30–31 speak of a «completed swarm», while the gate checks «every such run». Reading A: only complete runs carry obligations. If phase 1a proceeds from an incomplete run, the `[DECISION]`s from its finished slots escape the gate. Reading B: every v2 run, including incomplete and superseded ones, must have all items answered. But an incomplete run without a judge has no inventory to check, and every re-run piles up obligations from earlier runs. The spec also does not say whether phase 1a or phase 2 may proceed from an incomplete run at all. | Opus | in spec — Complete term; criteria 30–32, 34; run-scope detail (ruling S-13, decisions.md, 2026-10-16) | — |
| S-14 | MAJOR | SPEC | base | `spec.md`, criteria 15, 28 | [AMBIGUITY] It is unclear whether supported, refuted, unique and off-brief are exclusive dispositions per claim or independent counts. If they are exclusive, every claim must fall into one of the four. A claim left in an unresolved disagreement (criterion 15) would then have to be scored supported or refuted, which criterion 15 forbids. If they are independent counts, one claim can be unique and supported at once, and the per-model totals mean something else. The comparison baseline the maintainer asked for in Q-7 gives different numbers under each reading. | Opus | in spec — Evidence status/disposition term; criterion 28 (ruling S-14, decisions.md, 2026-10-16) | — |
| S-15 | MAJOR | SPEC | base | `spec.md`, criteria 30, 34; [DETAIL] «Review checks … criterion rationale; the gate checks identities, coverage and answered status only» | [AMBIGUITY] It is unclear whether a gate or only the review enforces criteria 30 and 34. Reading A: «identities» includes resolving each spec criterion's named claims or records, and the spec's `neighbours:` list, against the run. Then a criterion naming a missing claim fails `make verify`. Reading B: the gate reads only the handoff and the decisions. Criterion origins are «criterion rationale» left to review, and the neighbours rule lives only in the phase-2 prompt. Under Reading B neither criterion can go red in a test: a spec with a criterion lacking an origin, or with a confirmed neighbour dropped, passes every check. | Opus | in spec — criteria 30, 34; gate/review detail (ruling S-15, decisions.md, 2026-10-16) | — |
| S-16 | MAJOR | SPEC | base | `spec.md`, template under Topic contract; criteria 31, 35; `decisions.md` Q-7, topics 3 and 6 | Cannot go red: the fixed template has no field for the class a topic-3 report holds right, or for topic 6's way of governing each changing fact. Two inputs show this. A topic-6 report that names a model id as stale but proposes no governance should refute criterion 35. A topic-3 report whose claims hold a declared `architectural` change to be `feature`, with no `[DECISION]` question, should show the omitted class disagreement of criterion 31. Both pass template validation, so no runner or gate check can tell them apart from a clean report. | Opus | in spec — topic-specific template; criteria 27, 31, 35 (ruling S-16, decisions.md, 2026-10-16) | — |
| S-17 | MAJOR | SPEC | base | `spec.md`, criteria 7, 15, 24, 25 | Cannot go red as written. The refutations «code summaries replace a comparison», «a majority erases a sourced objection», «a finder judges the design», «code/reuse proposes new code» and «an online report judges local applicability» are about the meaning of model output. A stand-in test can only produce structure. The spec names no structural property of a report or reconciliation that these cases break, and no review step that would record them. Criterion 25's statement is about what a researcher receives, which is testable, but its refutations are about what the report says. | Opus | in spec — criteria 7, 15, 24, 25; Definition of Done (ruling S-17, decisions.md, 2026-10-16) | — |
| S-18 | MINOR | SPEC | base | `spec.md`, criteria 7, 29, 30; [DETAIL] `neighbours:` | [AMBIGUITY] Two neighbour cases have two readings each. (1) «An unread/invalid path is a gap that prevents a complete comparison» can mean the run is incomplete with exit 1, which blocks the «completed swarm» of criteria 30–31 until the header is fixed. It can also mean the run is complete with the gap named, as in criterion 7. (2) Topic 5 and the judge may find a header-given neighbour unrelated. Criterion 29 forbids dropping it from the research, but criterion 30 carries only «confirmed» neighbours into the spec. So it is either carried anyway or dropped. | Opus | in spec — criteria 4, 29, 30; neighbour preflight detail (ruling S-18, decisions.md, 2026-10-16) | — |
| S-19 | MINOR | SPEC | base | `spec.md`, criteria 23, 24, 26; [DETAIL] stage order | Missing: what the finder trio and the topic author receive as the description of the change in phase 1, before any spec exists. Candidates are the `research.md` body or header, the bead, the spec if present, or the merged map. This input is the only source of the public sentence (Q-6) and part of the «identical … evidence packets» of criterion 26. The spec also does not say whether instruction files a runtime can load on its own are given to all three repository seats or to none. The current explore embeds `AGENTS.md`. | Opus | in spec — criteria 24, 26; private-brief detail (ruling S-19, decisions.md, 2026-10-16) | — |
| S-20 | MINOR | SPEC | base | `spec.md`, [DETAIL] include/exclude | [AMBIGUITY] The detail says «an explicitly included id missing from the fresh catalog makes selection incomplete (exit 1)». Reading A: the preflight exits 1 before any model call, like a catalog failure. Reading B: the run dispatches the 39 fixed slots and the other selected models, records the missing included id as a missing slot, and ends incomplete with exit 1. Reading B spends 39 or more invocations on a run already known to be incomplete before it starts. | Opus | in spec — criterion 39; include/exclude preflight detail (ruling S-20, decisions.md, 2026-10-16) | — |

Stage-2 call, 2026-10-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 484 files, 1358 commits, 12 rules.

Phase-2a incorporation — 2026-10-16: all S-1–S-20 rulings from decisions.md
are in spec.md with matching design/plan and ADR 0020 wording. The original
finding text is preserved above; no row is rejected and no human answer is
invented. Historical phase-6 F-1 stays open until its separate attended
real-Pi isolation capture provides measured evidence.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0020-phase-1-research-swarm.md` +50 -14
> - `plans/changes/research-swarm/design.md` +122 -46
> - `plans/changes/research-swarm/findings.md` +26 -20
> - `plans/changes/research-swarm/plan.md` +175 -123
> - `plans/changes/research-swarm/research.md` +18 -0
> - `plans/changes/research-swarm/spec.md` +175 -132
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-lhsiv8wi.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 579.84s (0:09:39)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12175 earlier lines left out …]
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

Stage-2 call, 2026-10-16: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 484 files, 1358 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +23 -0
> - `plans/changes/research-swarm/spec.md` +44 -41
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-t1ov9qx0.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 622.63s (0:10:22)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12224 earlier lines left out …]
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

Stage-2 call, 2026-10-16: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 484 files, 1358 commits, 12 rules.

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +13 -0
> - `plans/changes/research-swarm/research.md` +28 -0
> - `plans/changes/research-swarm/spec.md` +5 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-6x7siowf.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 578.87s (0:09:38)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12270 earlier lines left out …]
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

Stage-2 call, 2026-10-16: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 484 files, 1360 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-16

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-21 | MAJOR | SPEC | fix-r1 | `spec.md`, Terms «Selected Go free models»; criteria 39, 41, 42; `research.md`, «Phase-2a incorporation evidence» [GAP] | [AMBIGUITY] The Terms require «explicit catalog tool-call support» and exclude models whose support is «absent». `research.md` records that pinned Pi 1.2.0's Model interface has no tool-support field and leaves the raw capability mapping to phase 4. The spec names no field. Reading A: support is judged per catalog entry. A fresh overlay whose entries carry no such field then excludes every `-free` id as `no-tool-support`, criterion 42 records a valid measured empty selection (N=0), and every run completes with exit 0 while Q-10 never takes effect. Reading B: an overlay whose schema has no tool-support capability cannot be measured reliably (criterion 41). The run then exits nonzero before any model call, and no swarm runs until the mapping exists. The same catalog yields a complete 39-slot run under A and a refused run under B. | Opus | in spec — Selected Go free models term; criteria 38–42; two-source preflight detail (Q-11, 2026-10-17 replaces the Pi-only field rule of S-21); incorporated 2026-10-17 | — |
| S-22 | MAJOR | SPEC | fix-r1 | `spec.md`, Terms «Frozen input state»; criterion 16; [DETAIL] «Local references resolve against retained frozen bytes» | [AMBIGUITY] The frozen state includes a «retained copy of every tracked file», and criterion 16 is refuted when «the retained bytes/reports are absent». Neither says how long the copy is kept or where. Reading A: the copy lives in run scratch and is discarded at the end. Only HEAD and the digest persist, and the absence case can only arise during the run. Reading B: the copy is durable run evidence. Kept under the change folder outside `research.md`, it makes every run incomplete, because the digest check ignores only the runner's research appends and restamp. Appended to `research.md`, the whole tracked tree is added on every run, and the next run's private brief («frozen research.md header/body») carries every earlier copy to the finders and the topic author. A post-run test that looks for the retained bytes passes under B and fails under A. | Opus | in spec — Frozen input state term; criterion 16; scratch lifetime detail (ruling S-22); incorporated 2026-10-17 | — |
| S-23 | MAJOR | SPEC | fix-r1 | `spec.md`, criterion 34; Terms «Evidence status and disposition» | [AMBIGUITY] Criterion 34 accepts a Basis that resolves to «a global claim from a complete run». The Terms say unsupported claims «are never evidence», and refuted or off-brief claims are valid claims that carry a judge disposition. Reading A: any existing global id from a complete run resolves, so a criterion resting on an `unsupported`, `refuted` or `off-brief` claim passes the gate. Reading B: only a valid claim, or only a `supported` one, can serve as a basis, and the same spec exits 1. Criterion 34's refutations name only missing and incomplete-run claims, so a test whose Basis names an unsupported claim has no expected result. | Opus | in spec — criterion 34; supported-only direct Basis detail (ruling S-23); incorporated 2026-10-17 | — |
| S-24 | MAJOR | SPEC | fix-r1 | `spec.md`, template under Topic contract; criteria 29, 31; [DETAIL]s «neighbour contradictions and proposed removal of given neighbours also do so» and «class/neighbor fields» | Cannot go red as specified. The [DETAIL]s say neighbour contradictions and proposed removals of given neighbours derive obligations «independently of the judge», from «class/neighbor fields». Criteria 29 and 31 are refuted when such a case has no item. The template defines `class_assessment` for topic 3, but topic 5 has no field for a contradiction or for a given neighbour found unrelated, only the free-prose section «relation to neighbouring specs». Refuting input: a topic-5 report whose claim C2 says a given neighbour's criterion contradicts the change, with no `[DECISION]` question. It passes the template, and neither runner nor gate has a field to derive the item from. The only remaining source is the judge's output, which the [DETAIL] says the derivation must not depend on. The implementer has to invent the field or fall back on the judge. | Opus | in spec — Topic contract neighbour_relations; criteria 27, 29, 31; independent derivation detail (ruling S-24); incorporated 2026-10-17 | — |
| S-25 | MAJOR | SPEC | base | `spec.md`, Topic contract, finder paragraph; criteria 5, 24, 29 | Missing: what makes the Opus map merge a «valid recorded result» (criterion 5). Topics 1–8 are bounded to mapped code and places, so the merge sets every repository topic's scope. The spec does not say: (1) whether the merge must keep every finder entry (a union without duplicates) or may drop or add entries, and how a drop is recorded; (2) whether finder and merge entries must resolve against the frozen state like claims under criterion 16, and what happens to an entry that does not; (3) whether every given neighbour must appear in the map. Test case: a merge that omits a `path::symbol` one finder listed, or adds one no finder listed, has no expected result under criterion 5 or 24. | Opus | in spec — Topic contract exact finder union; criteria 5, 24 (ruling S-25); incorporated 2026-10-17 | — |
| S-26 | MINOR | SPEC | fix-r1 | `spec.md`, Terms «Public topic»; criterion 23 | [AMBIGUITY] The rule refuses a listed set of characters (digits, underscores, slashes, backticks, colons, other dots). It also says each word is letters «joined only by» single hyphens or apostrophes. It says nothing about commas, semicolons, quotation marks, parentheses, question marks, stand-alone dashes or the typographic apostrophe ’. Reading A: a word is a whitespace-separated token that must match the letter pattern. Then «Isolation, Prüfung und Wiederherstellung für Agentenläufe» is refused, and the run ends with exit 1 after five model calls. Reading B: only the listed characters are refused and other punctuation separates words, so the same sentence passes. Criterion 23 gives opposite expected results for it. | Opus | in spec — Public topic term; criterion 23 (ruling S-26); incorporated 2026-10-17 | — |
| S-27 | MINOR | SPEC | fix-r1 | `spec.md`, criterion 30; [DETAIL] «enforces neighbour parity» | [AMBIGUITY] Criterion 30 is refuted by a lost confirmed or given path, an escaping or duplicate path, and «an unconfirmed suggestion». The [DETAIL] says the gate «enforces neighbour parity». Reading A (parity): the header must equal the confirmed and given neighbours minus those a maintainer dropped. A `spec.md` path that no finder suggested and no header gave then fails with exit 1. Reading B (the criterion's list): such a path is not a suggestion at all and passes. A phase-2 author who adds a neighbour found while drafting gets opposite gate results. | Opus | in spec — criterion 30; exact neighbour parity detail (ruling S-27); incorporated 2026-10-17 | — |
| S-28 | MINOR | SPEC | base | `spec.md`, criterion 41; [DETAIL] «Preflight validates class and given neighbours, then measures the catalog» | Missing: the exit code for criterion 41. It says only «exits nonzero» for a timeout, a stale-only, malformed or ambiguous catalog. Every neighbouring preflight case has a fixed code: invalid neighbours and malformed policy exit 2, a missing include exits 1, and the repository's code for not measured is 3 (criterion 33). A catalog failure could be exit 1 (failed result) or exit 3 (not measured). The implementer has to pick, and a caller that treats 1 and 3 differently behaves differently. | Opus | in spec — criterion 41; Pi-failure exit 1 and Q-11 capability-source distinction (ruling S-28); incorporated 2026-10-17 | — |
| S-29 | MINOR | SPEC | base | `spec.md`, criteria 14, 23, 28; [DETAIL] stage order and private brief | Missing: what the three Opus roles (map merge, topic author, judge) may read beyond their packets. The spec fixes their inputs but not whether they run with file tools. With tools, the judge can check a cited `path::symbol` before scoring a claim `supported` or `refuted`, and the author can read past the brief. Without them, «supported» can only mean cited and not contradicted by peers. The implementer has to choose, and the choice changes the dispositions criterion 28 counts and what can reach criterion 23's public sentence. | Opus | in spec — Evidence status and disposition term; criteria 5, 14, 23, 28; packet-only Opus and bounded excerpts detail (ruling S-29); incorporated 2026-10-17 | — |
| S-30 | MINOR | SPEC | base | `spec.md`, Open decisions, [DETAIL] «Keep the architectural class, ADR 0020 and 12-hour phase-4 stop»; header `appetite: 12` | Missing: how the 12-hour phase-4 stop is computed. The [DETAIL] keeps the stop and says earlier implementation «counts», its span «unmeasured» and «not reset». Nothing says how that span is to be established, so neither the remaining appetite nor the moment phase 4 must stop can be determined from the spec. | Opus | in spec — Open decisions historical-time computation and immediate unmeasurable-time stop detail (ruling S-30); incorporated 2026-10-17 | — |

Stage-2 call, 2026-10-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 484 files, 1364 commits, 12 rules.

Phase-2a incorporation — 2026-10-17: S-21–S-30 are incorporated in spec.md
with matching design, plan and sole new ADR 0020 revisions. Original finding
text is unchanged; only statuses above are updated. Q-11 is the maintainer's
recorded answer, not an agent answer: it replaces S-21's Pi-only capability
field with fresh-Pi/models.dev intersection and a capability-unavailable
fallback that retains fixed slots. Phase-6 F-1 remains open; no runtime or
isolation qualification is claimed by this artifact redraft.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0020-phase-1-research-swarm.md` +53 -18
> - `plans/changes/research-swarm/design.md` +86 -38
> - `plans/changes/research-swarm/findings.md` +18 -10
> - `plans/changes/research-swarm/plan.md` +155 -42
> - `plans/changes/research-swarm/research.md` +44 -2
> - `plans/changes/research-swarm/spec.md` +119 -49
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-ma4pqon4.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 560.62s (0:09:20)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/research-swarm/decisions.md: stale — updated 2026-10-16 is older than its last change 2026-10-17 (9beb00d)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12398 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 484 files, 1366 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/research-swarm/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/decisions.md` +1 -1
> - `plans/changes/research-swarm/plan.md` +33 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-h14i3o2v.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 576.78s (0:09:36)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/research-swarm/decisions.md: stale — updated 2026-10-16 is older than its last change 2026-10-17 (9beb00d)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12447 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 484 files, 1368 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/research-swarm/decisions.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/decisions.md` +1 -1
> - `plans/changes/research-swarm/plan.md` +27 -0
>
> Diagnostics:
> ```text
> - `make verify` exited -15
> E        +    where run = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4886/tes...e/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4886/test_local_citations_name_a_pa2/bin')).run
>
> tests/test_stage2_swarm.py:1082: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-sssq0ncc.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> ____________________ test_only_the_runner_appends_research _____________________
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4886/tes...e/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4886/test_only_the_runner_appends_r0/bin'))
>
>     def test_only_the_runner_appends_research(sworld: SwarmWorld) -> None:
>         # Criterion 17. Planted fault: a participant edits the tree, or earlier research is replaced.
>         seed = sworld.research.read_text(encoding="utf-8")
>         sworld.complete()
> >       assert sworld.run() == 0
> E       AssertionError: assert 2 == 0
> E        +  where 2 = run()
> E        +    where run = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4886/tes...e/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4886/test_only_the_runner_appends_r0/bin')).run
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-jy3hv_z_.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 553.47s (0:09:13)
> make: *** [verify] Terminated: 15
> ```

Stage-2 call, 2026-10-17: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 484 files, 1370 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-31 | MAJOR | SPEC | fix-r2 | `spec.md`, criteria 29, 30, 32; [DETAIL]s «Version manifests research-swarm/v2» and «exact neighbour parity» | [AMBIGUITY] Obligations carry across every complete v2 run, and the [DETAIL] names «confirmed by a new complete run» as a way to add a neighbour. So one change can hold several complete runs. Criterion 30 does not say which runs supply the «confirmed and given paths». Reading A (union of all complete runs): a path that run 1 confirmed stays required after run 2 rejects it. A given path removed from `research.md`'s header between the runs also stays required until a linked maintainer answer drops it. Reading B (latest complete run only): run 2's header and run 2's confirmations alone define the set, so that path must now be absent, and keeping it exits 1. Test case: run 1 confirms suggestion P and run 2 rejects it. A spec header that contains P passes under A and fails under B. A header without P fails under A and passes under B. | Opus | in spec — criteria 29–32; Open decisions, complete-run union and parity (S-31) | — |
| S-32 | MAJOR | SPEC | base | `spec.md`, Topic contract row 6; Terms «Claim»; criterion 16; [DETAIL] «Opus map merge, topic author and judge have empty tool lists»; `decisions.md`, Q-7 topic 6 (evidence «commit hash, PR number, bead id or `path::section`») | [AMBIGUITY] Topic 6 is limited to «mapped history only», and Q-7 accepted commit hashes as its evidence. The spec resolves local evidence only as a path plus a symbol or section against frozen bytes, and the judge's excerpts are only «resolved symbol/section or receipt excerpts». Reading A: a claim that cites a commit has no resolvable local reference, so the runner marks it `unsupported`. A topic-6 report that backs its history claims (last change, reason, reversal) with commits alone then fails the one-evidence-backed-claim floor, and the run is incomplete. Reading B: a commit reachable from the frozen HEAD resolves, and the runner attaches its message as the excerpt. The spec also does not say how a repository seat gets history at all: no packet content and no tool for git data is named. PR numbers and bead ids cannot resolve under either reading, because the tracker is not read. Test case: a topic-6 report whose only evidence is a commit hash from frozen HEAD's ancestry is accepted under B and rejected under A. | Opus | in spec — Terms Claim; Topic contract 6; criterion 16; Open decisions, bounded history (S-32) | — |
| S-33 | MINOR | SPEC | fix-r2 | `spec.md`, Terms «Selected Go free models»; criterion 42; [DETAIL] «Preflight validates class and given neighbours» («malformed/unreachable metadata excludes all») | [AMBIGUITY] The [DETAIL] excludes single ids for «missing entries/absent or false tool_call/deprecated status». It excludes every candidate when the metadata is «malformed». Criterion 42 records a different reason for each case (measured-empty or capability-unavailable). The spec does not say where «malformed» starts. Reading A: only a document that does not parse is malformed. A missing `opencode-go` key, or a candidate whose `tool_call` is a string or null, excludes only the ids concerned, each with its own reason, and the other candidates stay eligible. Reading B: any part that departs from the expected shape makes the whole metadata malformed and excludes all candidates as capability-unavailable. That includes a candidate's non-boolean `tool_call`, a missing `opencode-go` key, or a malformed entry of an unrelated provider. Test case: candidate X has `tool_call: "true"` and candidate Y has `tool_call: true`. Under A, N is 1 and Y is selected. Under B, N is 0 with the reason capability-unavailable. | Opus | in spec — Terms Selected Go free models; criterion 42; Open decisions, metadata fault boundaries (S-33) | — |
| S-34 | MINOR | SPEC | fix-r2 | `spec.md`, [DETAIL] «The budget is at most `39 + 3N` calls» («catalog 60 seconds»); criteria 41, 42; Terms «Selected Go free models» | [AMBIGUITY] The catalog stage has one 60-second deadline, but it now holds two reads with opposite failure rules. A Pi failure exits 1 (criterion 41). An unavailable models.dev gives N=0 and the fixed slots still run (criterion 42). Reading A: models.dev gets its own share of the stage, and a request still open when that share ends counts as «unavailable», so the run goes on with N=0. Reading B: the 60 seconds bound the whole stage, and a stage that overruns them is a catalog timeout under criterion 41, so preflight exits 1 before any model call. Test case: Pi refreshes in 5 seconds and the models.dev request does not answer within 60 seconds. Under A the run dispatches the 39 fixed slots; under B it exits 1 with none. | Opus | in spec — criteria 19, 41–42; Open decisions, shared catalog deadline (S-34) | — |
| S-35 | MINOR | SPEC | fix-r2 | `spec.md`, Topic contract (finder paragraph; topic-5 `neighbour_relations`); criteria 29, 30 | [AMBIGUITY] Finder entries are keyed by `path::symbol` or `path::section`. Topic 5 needs exactly one relation per packet neighbour «path». The spec does not say how a suggestion becomes a packet neighbour. Header-given neighbours must be existing `spec.md` paths (otherwise exit 2), but no such rule is stated for suggestions. Reading A: only resolved suggestions whose path is a `spec.md` count, merged to one neighbour per path. A suggestion such as `plans/changes/foo/design.md::Data model` stays a map entry without neighbour status. Reading B: the path of every resolved entry in the neighbour category is a packet neighbour. It then needs a relation, can be confirmed, and once confirmed must enter the spec's `neighbours:` header under criterion 30. Test case: a topic-5 report with no relation for that `design.md` path is accepted under A and rejected as a missing path under B. | Opus | in spec — Topic contract finder mapping; criteria 27, 29; no-spec gaps (S-35) | — |
| S-36 | MINOR | SPEC | fix-r1 | `spec.md`, criterion 4; [DETAIL] «Preflight validates class and given neighbours» | [AMBIGUITY] Criterion 4 refuses invalid given-neighbour headers with exit 2, and the [DETAIL] defines an invalid entry. Neither says what a missing `neighbours:` key or an empty list means. In this worktree, no template carries the key, and no change's `research.md` other than this one has it. Reading A: a missing key means no given neighbours, and the run goes on with finder suggestions only. Reading B: a missing header is invalid, like a missing class, and preflight exits 2. Test case: the first swarm run of any other feature change runs under A and exits 2 before any model call under B. | Opus | in spec — criterion 4; Open decisions, explicit neighbours list (S-36) | — |
| S-37 | MINOR | SPEC | base | `spec.md`, Terms «Repository trio» and «Online researchers»; criteria 19, 37, 38, 41 | Missing: what preflight does when a fixed Go model (`deepseek-v4.1-flash`, `mimo-v2.6-flash` or `qwen3.8-flash`) is absent from this run's fresh `opencode-go` overlay, or present only in the shipped baseline. The spec checks only `-free` ids against the catalog. The implementer has to choose. Either preflight exits 1 before any call, as it does for a missing explicit include. Or the required slots are dispatched, fail at call time, and the run ends incomplete with exit 1 after up to 36 + 3N other calls. Test case: a fresh overlay without `qwen3.8-flash` has no expected call count under criterion 19 or 41. | Opus | in spec — criteria 38, 41; Open decisions, fixed-model-unavailable (S-37) | — |
| S-38 | MINOR | SPEC | fix-r2 | `spec.md`, criterion 14; [DETAIL] «Opus map merge, topic author and judge have empty tool lists» (4,000-character cap) | Missing: a limit on the size of the whole judge packet, and what happens when it exceeds what one Opus context accepts. The cap applies per cited source. A claim may cite several sources, and the number of reports grows with N. 33 required reports with seven claims and one full excerpt each already give 924,000 characters of excerpts, and each free model adds 84,000 more. Criterion 14 requires a single context and fails a judge that lacks any valid claim's excerpt. The implementer therefore has to choose between failing the judge, which makes the run incomplete, and shortening excerpts or limiting N, which the spec does not allow. Test case: a run with N=10 and full excerpts has no expected outcome (complete, incomplete, or shortened excerpts). | Opus | in spec — criteria 14, 18; Open decisions, per-claim cap and whole-packet refusal (S-38) | — |
| S-39 | MINOR | SPEC | fix-r2 | `spec.md`, criteria 38, 39, 42; Terms «Selected Go free models»; [DETAIL] «retain source/time/digest and per-model reasons»; `decisions.md`, Q-11 | Cannot go red as specified. Q-11 says a model excluded through models.dev keeps its recorded reason, and the [DETAIL] requires the models.dev source, time and digest to be kept. Criterion 38 names only the Pi refresh («its freshly fetched overlay, source, UTC time and selection»). Criterion 42 checks the reason only when N=0, and criterion 39 checks only which models run. Refuting input: in models.dev, `longcat-2.5-preview-free` is eligible and `cat-jam-free` is deprecated. The manifest records N=1 but has neither the models.dev source, time and digest nor `cat-jam-free`'s reason «deprecated». No refutation names this run, unless criterion 38's «selection lacks dated provenance» is read as covering a second source the criterion does not name. | Opus | in spec — criterion 38; Open decisions, both-source and per-candidate provenance at every N (S-39) | — |

Stage-2 call, 2026-10-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 484 files, 1372 commits, 12 rules.

> Attempt 1 (codex): the runner put back what a draft may not change:
> - `plans/changes/research-swarm/decisions.md`

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0020-phase-1-research-swarm.md` +45 -6
> - `plans/changes/research-swarm/decisions.md` +1 -1
> - `plans/changes/research-swarm/design.md` +79 -32
> - `plans/changes/research-swarm/findings.md` +9 -9
> - `plans/changes/research-swarm/plan.md` +133 -15
> - `plans/changes/research-swarm/spec.md` +82 -30
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-phx4xli4.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 540.74s (0:09:00)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/research-swarm/decisions.md: stale — updated 2026-10-16 is older than its last change 2026-10-17 (63dd5d4)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12577 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 484 files, 1372 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/changes/research-swarm/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/decisions.md` +1 -1
> - `plans/changes/research-swarm/plan.md` +17 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-xtzjks2o.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 543.94s (0:09:03)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/research-swarm/decisions.md: stale — updated 2026-10-16 is older than its last change 2026-10-17 (63dd5d4)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12626 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 484 files, 1374 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1
>
> the attempt is saved at refs/stage2/attempts/research-swarm/draft-attempt-3-20261016T233834915141Z (5b13c323c03d); `git diff 63dd5d4b2208 refs/stage2/attempts/research-swarm/draft-attempt-3-20261016T233834915141Z` shows it.
>
> The runner put back:
> - `docs/adr/0020-phase-1-research-swarm.md`
> - `plans/changes/research-swarm/design.md`
> - `plans/changes/research-swarm/plan.md`
> - `plans/changes/research-swarm/spec.md`

Stage-2 call, 2026-10-17: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 484 files, 1377 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-40 | MAJOR | SPEC | base | `spec.md`, criteria 29–31; Topic contract, topic-5 `neighbour_relations`; [DETAIL]s «Version manifests research-swarm/v2» and «exact neighbour parity»; `decisions.md`, Q-7 topic 5 | [AMBIGUITY] The gate's required neighbour set and both kinds of cross-run item depend on whether a run «confirmed» or «rejected» a suggested path. The spec never says what makes either happen. Topic 5 gives three relations, one per seat (`related`, `unrelated`, `contradicts`), and no field holds a confirmation. Reading A: the judge's reconciliation confirms or rejects each suggestion, and the gate reads that verdict. Reading B: the runner derives the status from the three relations. For example, any `related` or `contradicts` confirms, or only agreement of all three seats does. The spec also does not say whether a `contradicts` suggestion counts as confirmed, or what a suggestion is when the seats split and the judge does not mention it. Test case: suggestion P gets `related`, `unrelated`, `related`, and the judge confirms P. A spec header with P passes under A and under B with «any seat». It fails as an unconfirmed suggestion under B with «all seats». | Opus | in spec — Terms Neighbour status; Topic contract; criteria 29–31; Open decisions runner-derived status and parity | — |
| S-41 | MAJOR | SPEC | fix-r1 | `spec.md`, criterion 30; Terms «Handoff item»; [DETAIL]s «Version manifests research-swarm/v2» and «exact neighbour parity»; Non-goals («automatic semantic grading of human answers») | [AMBIGUITY] Criterion 30 adds «linked maintainer additions» and subtracts «linked maintainer drops». A Q-record carries only `research_items:`, `research_claims:` and its free-text answer. Nothing says how the gate learns whether a linked answer keeps, drops or adds a path. Reading A: the gate reads the decision from the answer text. That comes close to the automatic grading of human answers that the Non-goals exclude, and the spec gives no vocabulary for it. Reading B: any linked, answered record closes the neighbour item, and the header may then keep or omit the path. Test case: topic 5 calls header-given P `unrelated`, and a maintainer record links that item with the answer «P bleibt Nachbar». A spec header without P exits 1 under A and 0 under B. Additions have a further gap. A path found while drafting has no handoff item in any run, so `research_items:` has nothing to link, and no named field carries the added path. Under either reading the gate cannot accept it. | Opus | in spec — Terms Handoff item; criteria 30, 33; Open decisions structured keep/drop/add parity | — |
| S-42 | MAJOR | SPEC | base | `spec.md`, Terms «Claim»; criterion 16; Topic contract, map resolution and topic scope; [DETAIL] «Opus map merge, topic author and judge have empty tool lists» («resolved symbol/section») | Missing: what «resolves» means for `path::symbol` and `path::section`, and which text becomes the excerpt. Reading A is what the earlier slice does (`scripts/stage2_swarm.py::symbol_problem`): a symbol resolves when its text, or each of its dotted parts as a word, occurs anywhere in the file. That leaves the 4,000-character excerpt with no defined extent. Reading B: the reference must name a definition (a Python def, class or assignment, a YAML key path, a Markdown heading), and the excerpt is that definition or section. That needs rules the spec does not give: for YAML, JavaScript, shell and nested methods, for headings with formatting or duplicates, and for where a section ends. Test case: a claim cites `docs/WORKFLOW.md::routing table`, and those words occur only in prose. The claim is valid under A and unsupported under B. The same choice decides which map entries grant topic scope, whether a report meets the evidence floor, and which claims a criterion Basis may name. | Opus | in spec — Terms Resolves; criterion 16; Open decisions frozen references | — |
| S-43 | MINOR | SPEC | fix-r3 | `spec.md`, Topic contract, finder paragraph; criterion 4; [DETAIL] «Preflight validates class and given neighbours» | [AMBIGUITY] The repository keeps living specs at `plans/specs/<capability>/spec.md` and closed changes at `plans/changes/archive/YYYY-MM-DD-<name>/` (`docs/WORKFLOW.md`, «Artefact lifecycle»). A header-given neighbour is valid as any existing frozen `spec.md` path. A finder suggestion becomes a packet neighbour only «inside `plans/changes/<name>/`». Reading A (literal): a neighbour entry `plans/specs/implementation-verification/spec.md::…`, or one in an archived change's `design.md`, is `no-spec`. It needs no topic-5 relation and can never be confirmed. Reading B: any folder that holds a frozen `spec.md` yields a packet neighbour, including archive folders and a directly cited living spec. Test case: a topic-5 report with a relation for that living spec is rejected as an extra path under A and accepted under B. A report without that relation is accepted under A and rejected under B. Given paths have a parallel gap: `templates/spec.md` could be a valid given neighbour or a non-spec path that exits 2. | Opus | in spec — Terms Neighbour spec; Topic contract; criterion 4; Open decisions neighbour preflight | — |
| S-44 | MINOR | SPEC | fix-r3 | `spec.md`, Terms «Selected Go free models» («matching exact id»); [DETAIL] «Preflight validates class and given neighbours» («duplicate claimed ids», «an id different from its key»); criterion 42 | [AMBIGUITY] The spec does not say what identifies a candidate under `opencode-go.models`: the object key or the entry's `id` field. Reading A (key): keys are the identities. An entry whose `id` differs from its key is `metadata-malformed`, and only repeated raw JSON keys count as «duplicate claimed ids». A default JSON parser drops repeated keys without notice. Reading B (`id` field): two entries under different keys with the same `id` are duplicate claimed ids, and every candidate is excluded as capability-unavailable. The spec also does not say whether an entry with no `id` field has «an id different from its key». Test case: Pi lists `a-free` and `b-free`, and models.dev has both keys, each with `id: "a-free"` and `tool_call: true`. Under A, N=1: `a-free` is selected and `b-free` is `metadata-malformed`. Under B, N=0 with the reason capability-unavailable. Second case: an entry `x-free` with `tool_call: true` and no `id` is selected under one reading of the absent field and `metadata-malformed` under the other. | Opus | in spec — Terms Selected Go free models; criterion 42; Open decisions catalog identity and duplicate-id | — |
| S-45 | MINOR | SPEC | fix-r1 | `spec.md`, Topic contract, topic-5 row and the one-evidence-backed-claim floor; criteria 4, 18, 27 | Missing: what topic 5 does when its packet holds no neighbour. `neighbours: []` is valid (criterion 4), and the finders may suggest none, or only `no-spec` entries. Topic 5 may only use the neighbours' spec, design, plan and decisions as evidence. Yet each of its three required seats must return at least one evidence-backed claim. A seat that stays inside that scope has nothing to cite. Its report fails the floor, and the run ends incomplete with exit 1. A seat that cites something outside the scope passes the floor and is only scored off-brief. The implementer has to choose: skip topic 5 (which changes the 39 required slots), exempt it from the floor, or let it fail. Test case: a feature change with `neighbours: []` and no neighbour-category finder entry. Whether the run ends complete or incomplete depends only on whether the seats leave their scope. | Opus | in spec — Topic contract empty-neighbour exception; criteria 7, 18, 27; Open decisions report floor | — |
| S-46 | MINOR | SPEC | fix-r3 | `spec.md`, criterion 29; Topic contract, finder paragraph | Cannot go red for one case the Topic contract fixes. A resolved neighbour-category entry inside a change folder whose `spec.md` exists must become a packet neighbour. Criterion 29 refutes only a spec-backed suggestion «dropped without a gap entry». Refuting input: an entry `plans/changes/foo/design.md::Data model` with `foo/spec.md` present in the frozen state. The runner lists it as a `no-spec` gap and gives topic 5 no packet neighbour for it. Criterion 29 passes because a gap entry exists. Criterion 27 passes because relations are checked against the runner's own packet. Criterion 24 names only unresolved scope and given neighbours. | Opus | in spec — Topic contract independent packet derivation; criteria 24, 29 | — |

Stage-2 call, 2026-10-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 484 files, 1379 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0020-phase-1-research-swarm.md` +60 -16
> - `plans/changes/research-swarm/design.md` +87 -29
> - `plans/changes/research-swarm/findings.md` +8 -8
> - `plans/changes/research-swarm/plan.md` +149 -29
> - `plans/changes/research-swarm/spec.md` +126 -44
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-vx575csg.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 550.93s (0:09:10)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12746 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 484 files, 1380 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +33 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-j6k07shs.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 555.14s (0:09:15)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12793 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 484 files, 1380 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1
>
> the attempt is saved at refs/stage2/attempts/research-swarm/draft-attempt-3-20261017T002930167611Z (3aacaae6abb7); `git diff a68bbd02c258 refs/stage2/attempts/research-swarm/draft-attempt-3-20261017T002930167611Z` shows it.
>
> The runner put back:
> - `docs/adr/0020-phase-1-research-swarm.md`
> - `plans/INDEX.md`
> - `plans/changes/research-swarm/design.md`
> - `plans/changes/research-swarm/plan.md`
> - `plans/changes/research-swarm/spec.md`

Stage-2 call, 2026-10-17: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 484 files, 1381 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-47 | MINOR | SPEC | fix-r4 | `spec.md`, Terms «Resolves» (Markdown rule, `criterion <n>` form); criterion 16 («an ambiguous heading … resolves», «the excerpt differs from the type-specific extent») | Missing: the spec does not say whether a Markdown heading is found line by line or by Markdown structure. The rule needs «exactly one heading's text» and ends the excerpt «before the next heading of the same or higher level». It does not say whether a `#` line inside a fenced code block counts as a heading. Reading A (by line): every line that starts with `#` marks is a heading. Reading B (CommonMark): lines inside a fence are not headings. Test case from the tree: `prompts/03-plan.md` has the heading `## The criterion ledger` at line 65. At line 83, inside a fenced `markdown` block opened at line 82, it has the line `## Criterion ledger`. The next real heading is `## Questions` at line 95. Under A, the excerpt for `prompts/03-plan.md::The criterion ledger` stops at line 82, and `prompts/03-plan.md::Criterion ledger` resolves to the fenced example. Under B, the first excerpt runs to line 94 and the second citation is unsupported. The same choice decides whether a fenced copy of a heading makes a real heading a duplicate (and so unsupported). It also decides whether a fenced `## Acceptance criteria` example breaks «the file's one» heading that `criterion <n>` needs. | Opus | in spec | Terms «Resolves» and resolver detail; criterion 16: one structural Markdown scan ignores front matter/fences and defines ATX headings; design resolver and plan step 3 carry all five fixtures. |
| S-48 | MINOR | SPEC | fix-r4 | `spec.md`, Terms «Resolves» (YAML and JSON rule: «a parsed dotted key path … its value as canonical JSON»); criterion 16 | Missing: the spec does not say how a dotted key path handles keys that contain dots, list items, or values with no JSON form. Example: `model-endpoints.yaml` line 254 has the key `longcat-2.5-preview-free` under `research_swarm.free_focuses`. Reading A: X is split at every dot. `model-endpoints.yaml::research_swarm.free_focuses.longcat-2.5-preview-free` then looks for the keys `longcat-2` and `5-preview-free` and is unsupported, so no key with a dot can ever be cited. Reading B: X is matched against the parsed key sequence and resolves to `[1, 4]`. Under B the spec would also have to say what happens when two splits both match. Values: an unquoted date such as `interview-minimums: 2026-10-08` (`decisions/adoption.yaml` line 5; also `vacant_since` in `provenance.yaml`) loads as a date object, which has no JSON form. Either it becomes the string `"2026-10-08"` and resolves, or JSON conversion fails and the claim is unsupported. The spec also does not say whether a list item can be cited by an index segment. «Canonical JSON» is not defined either (key order, separators, non-ASCII escaping), yet criterion 16 refutes an excerpt that «differs» from that extent. | Opus | in spec | Terms «Resolves» and resolver detail; criterion 16: exact mapping segments, duplicate/value refusals, ISO dates and fixed canonical JSON; design resolver and plan step 3 carry the cases. |
| S-49 | MINOR | SPEC | base | `spec.md`, Terms «Evidence status and disposition» and «Resolves» («unsupported references confer no evidence»); [DETAIL]s «Opus map merge, topic author and judge have empty tool lists» («joined in citation order») and «Template breaches reject a report» («Bad citations mark individual claims unsupported»); criteria 16, 18, 34 | [AMBIGUITY] A claim may cite several sources. The spec does not say what status the claim gets when only some of those citations resolve. Reading A: one bad citation marks the whole claim `unsupported` («Bad citations mark individual claims unsupported»). Reading B: the bad citation adds no evidence, the claim stays `valid` on the citations that resolve, and only their excerpts are joined («unsupported references confer no evidence»). Test case: a topic-1 claim cites `scripts/stage2.py::explore`, which resolves, and `scripts/stage2.py::no_such_symbol`, which does not. Under A the claim is unsupported. It cannot be scored supported or named in a criterion Basis. If it is the report's only claim, the report fails the floor and the run ends incomplete. Under B the claim is valid, carries the `explore` excerpt and may be scored supported. The same question applies to an online claim that cites one URL with a receipt and one without. | Opus | in spec | Terms «Evidence status and disposition», report detail and criterion 16: every citation must succeed before excerpt/disposition/Basis; design «Reports → judge» and plan step 7 carry mixed-citation fixtures. |
| S-50 | MINOR | SPEC | fix-r1 | `spec.md`, Terms «Selected Go free models» («unique `opencode-go` ids», «non-chat models … are excluded with reasons»); criterion 41 («malformed or ambiguous result»); [DETAIL] «Preflight validates class and given neighbours» | [AMBIGUITY] For models.dev the spec separates faults of the whole document from faults of one entry. For the fresh Pi overlay it does not. Criterion 41 makes a «malformed or ambiguous» Pi result exit 1 for the whole run. The Terms, however, exclude a non-chat free model on its own and speak of «unique» ids. Reading A: any malformed or repeated overlay entry makes the Pi result malformed or ambiguous. The run then exits 1 before any model call, fixed slots included. Reading B: only a fault of the whole response counts as malformed. A bad `-free` entry is excluded with a reason, and a repeated id is either merged into one or excluded as ambiguous. Test case: the fresh overlay is valid except for one thing. Either `cat-jam-free` has `"input": "text"` (a string, not a list), or `longcat-2.5-preview-free` appears twice with different `input` values. Under A no model call starts and the run exits 1. Under B the 39 fixed slots run and only that candidate is excluded. The same choice decides whether a malformed entry for a fixed id is reported as a malformed catalog or as `fixed-model-unavailable` with its id. | Opus | in spec | Terms «Selected Go free models», preflight detail and criteria 41/42: duplicate Pi ids block all calls, malformed free entries are pi-malformed, malformed fixed entries name fixed-model-unavailable; design catalog and plan step 2 carry three cases. |
| S-51 | MINOR | SPEC | fix-r4 | `spec.md`, Terms «Neighbour status» and «Evidence status and disposition» («unsupported claims … are never evidence»); Topic contract, `neighbour_relations`; criteria 29, 30 | [AMBIGUITY] Each topic-5 relation names local claims as its support. The spec does not say whether a relation still counts toward the runner's status when all of its claims are marked `unsupported`. Reading A: the status uses the three relation fields as written. Reading B: a relation with no valid claim is not evidence and does not count. The unanimity rule then has fewer than three relations, and the spec defines no status for that case. Test case: all three seats say `related` for suggestion P, but one seat's relation cites only a claim whose reference does not resolve. Under A, P is `confirmed`: it joins the required header set with no human item, and once a spec exists, a header without P exits 1. Under B, P lacks a unanimous confirmation. It becomes either `split` with a human item or a path with no defined status. The same question applies to `rejected`. | Opus | in spec | Terms «Neighbour status», handoff detail and criterion 29: count only relations backed by a valid claim, fewer than three is split, human items stay unfiltered; design handoff and plan steps 8/9 carry evidence-gap fixtures. |
| S-52 | MINOR | SPEC | base | `spec.md`, criteria 4 and 20; [DETAIL] «Preflight validates class and given neighbours» | [AMBIGUITY] Criterion 4 refuses «Stage 2 exploration» when the class is missing or the sources disagree. Criterion 20 keeps single Haiku exploration under `--stage2-off [REASON]`, a route that does not depend on the class. The spec does not say whether `--stage2-off` still needs a valid class. Reading A: class validation is part of every `explore` preflight. A change with no class in its research header, run without `--class`, then exits 2 before any call, even with `--stage2-off`. Reading B: `--stage2-off` uses no class-dependent route, so the class check is skipped and Haiku runs, as it did before this change. Test case: `research.md` names a bead but no class, and the command is `scripts/stage2.py explore <change> --stage2-off "quota"`. It exits 2 under A and makes one Haiku call under B. Criterion 20's refutations decide neither case. The same question applies when the header says `feature`, the call passes `--class bounded`, and `--stage2-off` is set. | Opus | in spec | Criteria 4/20 and preflight detail: explicit fallback skips class/neighbour checks and refuses --class with exit 2; design router and plan step 3 carry no-class/invalid-header/conflicting-argument cases. |

Stage-2 call, 2026-10-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 484 files, 1384 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/design.md` +57 -22
> - `plans/changes/research-swarm/findings.md` +6 -6
> - `plans/changes/research-swarm/plan.md` +131 -15
> - `plans/changes/research-swarm/spec.md` +70 -25
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-h_dbs7f0.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 536.21s (0:08:56)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12902 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 484 files, 1384 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +23 -0
> - `plans/changes/research-swarm/spec.md` +6 -2
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1467 lines of this gate left out …]
>
> tests/test_stage2_swarm.py:1091: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi --version ended 1; it is not the pinned 1.2.0; no call starts: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi: line 9: dirname: command not found
> tools/pi/pi: the Node declaration .node-version is missing from /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/stage2-nqto7u61.
> tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[feature]
> FAILED tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm[architectural]
> FAILED tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan
> FAILED tests/test_stage2_swarm.py::test_all_free_roles_are_attempted_before_flash
> FAILED tests/test_stage2_swarm.py::test_six_topics_have_independent_permitted_pairs
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[False]
> FAILED tests/test_stage2_swarm.py::test_declared_free_focuses_shape_research_and_topic_pairs[True]
> FAILED tests/test_stage2_swarm.py::test_declared_paid_endpoint_and_models_are_called
> FAILED tests/test_stage2_swarm.py::test_fresh_opus_reconciles_all_six_topics
> FAILED tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons
> FAILED tests/test_stage2_swarm.py::test_public_requests_exclude_every_private_input
> FAILED tests/test_stage2_swarm.py::test_public_claims_require_retrieved_source_receipts
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts0]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts1]
> FAILED tests/test_stage2_swarm.py::test_a_free_report_without_a_retrieved_page_is_no_contribution[receipts2]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[invented-url]
> FAILED tests/test_stage2_swarm.py::test_judge_public_citations_require_retrieved_receipts[search-snippet]
> FAILED tests/test_stage2_swarm.py::test_redirect_receipts_back_requested_and_final_urls
> FAILED tests/test_stage2_swarm.py::test_free_environment_excludes_identity_and_private_paths
> FAILED tests/test_stage2_swarm.py::test_an_accepted_topic_is_recorded_and_reaches_the_free_calls
> FAILED tests/test_stage2_swarm.py::test_every_call_is_checked_and_a_leak_block_stops_dispatch
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[nonzero-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[empty-flash]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-public]
> FAILED tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence[timeout-flash]
> FAILED tests/test_stage2_swarm.py::test_every_attempt_has_identity_audit_and_outcome
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[free-fails]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[flash-empty]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[judge-malformed]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[all-free-fail]
> FAILED tests/test_stage2_swarm.py::test_failures_preserve_evidence_and_never_report_complete[unmapped-free-id]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[pinned-registry]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[ambiguous]
> FAILED tests/test_stage2_swarm.py::test_the_free_inventory_reads_what_the_pinned_pi_prints[no-models]
> FAILED tests/test_stage2_swarm.py::test_deadlines_and_role_counts_bound_the_run
> FAILED tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent
> FAILED tests/test_stage2_swarm.py::test_a_run_across_midnight_keeps_its_frozen_research
> FAILED tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential
> FAILED tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation
> FAILED tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py::no_such_symbol`-names no symbol of src/app.py]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py:1`-gives line numbers only]
> FAILED tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol[`src/app.py`-is a bare path]
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - As...
> 46 failed, 2254 passed, 16 skipped in 620.39s (0:10:20)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12948 earlier lines left out …]
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

Stage-2 call, 2026-10-17: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 484 files, 1384 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1
>
> the attempt is saved at refs/stage2/attempts/research-swarm/draft-attempt-3-20261017T011315688870Z (bdf5a00d90fe); `git diff 769b1b891333 refs/stage2/attempts/research-swarm/draft-attempt-3-20261017T011315688870Z` shows it.
>
> The runner put back:
> - `plans/changes/research-swarm/design.md`
> - `plans/changes/research-swarm/plan.md`
> - `plans/changes/research-swarm/spec.md`

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 526 files, 1502 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-11 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:296`; `scripts/stage2_research_snapshot.py:118` | A successful run lasting more than 60 seconds cannot publish complete: the snapshot retains its preparation deadline, and the final `changed_paths()` reuses that expired deadline. A clock-controlled reproduction raises `ResearchSnapshotError` for an unchanged tree; `run()` converts this into incomplete exit 1. Publication needs its own valid checking deadline. [criteria 16, 18] | Codex | fixed — tests/test_stage2_swarm.py::test_a_run_longer_than_the_preparation_deadline_still_publishes_complete | — |
| F-12 | BLOCKER | SPEC | base | `scripts/stage2_research_store.py:58`; `scripts/stage2_research_run.py:286,535` | Without `XDG_STATE_HOME`, the store defaults to a directory beneath the user's HOME, which Claude research processes inherit. The placement guard checks only the worktree and git directory, so it accepts storage inside a model's home. The default configuration therefore violates the required separation of stored peer results from model home directories. [criterion 52] | Codex | fixed — tests/test_stage2_swarm.py::test_a_store_inside_the_real_home_is_refused_and_one_outside_it_is_accepted | — |
| F-13 | BLOCKER | SPEC | base | `scripts/stage2_availability.py:197`; `scripts/stage2_research_run.py:537` | The measured catalog never reaches Pi's fresh agent directory: neither probes nor research launches write its model definitions or model store. Pi consequently resolves models from shipped metadata or fabricated defaults. Locally reproduced: the selector accepts `qwen3.8-flash` advertised as `openai-completions`, while pinned Pi resolves that id as `anthropic-messages`; a newly selected `alpha-free` advertised as `anthropic-messages` resolves as `openai-completions`. Calls can therefore use an unmeasured transport despite passing preparation. [criteria 38, 43, 61] | Codex | fixed — tests/test_stage2_swarm.py::test_the_measured_catalog_reaches_pis_agent_directory_for_probes_and_launches | — |
| F-14 | BLOCKER | SPEC | base | `scripts/stage2_availability.py:564`; `scripts/stage2_research_run.py:941` | Preparation discards the catalog's per-candidate evidence and exclusions when constructing its receipt. For example, a free candidate excluded because `tool_call` is false leaves no candidate id, field value or exclusion reason in that receipt. Publication also omits preparation time, pool, candidate outcomes and probe audits from the manifest; consumption deletes the receipt. The published run cannot establish why candidates were admitted or excluded. [criteria 38, 44, 46] | Codex | fixed — tests/test_stage2_swarm.py::test_the_receipt_keeps_each_candidates_evidence_and_exclusion | — |
| F-15 | BLOCKER | SPEC | base | `scripts/stage2_research_dispatch.py:175`; `scripts/stage2_research_run.py:675,1042` | After a terminal store write fails, dispatch stops invoking terminal callbacks. Cancelled siblings and their available output remain only in `DispatchResult`, which `run_stage()` discards when raising the stop. A two-slot reproduction returns both outcomes but delivers only the first to the run. A persistent write failure additionally escapes from `publish()` at `set_append()` before research is appended, losing the required incomplete record and partial evidence. [criteria 18, 57] | Codex | fixed — tests/test_stage2_swarm.py::test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete | — |
| F-16 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:103,404` | The handoff gate silently chooses the last duplicate JSON or nested YAML key. Reproduced with an answered record containing two `research_neighbours.keep` keys, first naming A and then B: a spec containing only B produces no findings, silently discarding A. A manifest containing contradictory duplicate `class` keys is also accepted. These ambiguous inputs must produce not-measured exit 3 instead of a successful interpretation. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_duplicate_keys_in_records_are_not_measured | — |
| F-17 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:693,923` | If a finder fails, the manifest contains only the three finder slots. Merge, topic author, all topic slots and judge receive neither expected identities nor terminal outcomes because later entries are constructed only when their stages start. The numeric budget does not identify the missing contributions. An aborted run must retain the complete expected slot inventory and explicitly account for unstarted slots. [criterion 18; Data model — Run manifest] | Codex | fixed — tests/test_stage2_swarm.py::test_an_aborted_run_names_every_expected_slot_with_its_outcome | — |
| F-18 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:427,450,930`; `scripts/stage2_research_store.py:269` | Reused results cannot retain the required original start time: it exists only in the separate launch record, while result records and adoption omit it. Publication also omits each reused result's original leak-check record, and successful completion clears the store holding that record. A completed resumed run therefore permanently loses both required provenance fields despite reporting reuse. [criterion 55] | Codex | fixed — tests/test_stage2_swarm.py::test_a_reused_result_keeps_its_original_start_and_leak_check_in_the_published_manifest | — |

Phase 6 verdict: codex 01a15339-b204-7d12-b7e6-91aca1cfc69d, 2026-10-19
Reviewer session: codex 01a15339-b204-7d12-b7e6-91aca1cfc69d — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 530 files, 1516 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-19 | BLOCKER | SPEC | fix-r1 | `scripts/stage2_research_store.py:150–160` | The home-directory guard compares lexical paths without resolving `..` or parent symlinks. Reproduced: with HOME `/Users/mikypiky`, a store beneath `/Users/../Users/mikypiky/.local/state` passes `assert_outside()` although it lies inside the inherited home. This is new bypass evidence after the F-12 repair; the forbidden placement must be refused. [criterion 52] | Codex | fixed — tests/test_stage2_research_store.py::test_the_home_guard_resolves_dotdot_and_parent_links_before_comparing| — |
| F-20 | BLOCKER | SPEC | fix-r1 | `scripts/stage2_research_run.py:1107–1111` | A failure writing the research-append binding is silently suppressed. Reproduced with `set_append()` alone raising `StoreWriteError`: the run publishes `complete`, finishes normally with exit 0 and records no storage failure. Every state-store write failure must instead produce incomplete exit 1 with `state-store-unwritable`, unless security requires exit 2. [criterion 57] | Codex | fixed — tests/test_stage2_swarm.py::test_a_failed_append_binding_write_ends_incomplete_with_exit_one| — |
| F-21 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:1156–1163` | A storage failure during finalization overrides a preceding security refusal. Reproduced with a stage raising `Stop(..., 2)` and `finish_run()` raising `StoreWriteError`: `run()` raises `CallFailed` (exit 1) before reaching `Refused` (exit 2). Security exit 2 must retain precedence when storage also fails. [criteria 12, 57] | Codex | fixed — tests/test_stage2_swarm.py::test_a_security_refusal_keeps_exit_two_when_finishing_the_store_also_fails| — |
| F-22 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:480–484,1077–1082` | When the terminal write fails for a finder that exited successfully, its stdout remains only in memory. Dispatch aborts before map construction, while publication excludes its output because the outcome is `ok`. Reproduced: the incomplete publication loses the finder-output canary, and no terminal record was stored. Available evidence must survive this write failure; the F-15 repair preserves outcomes but still loses this output. [criteria 18, 57] | Codex | fixed — tests/test_stage2_swarm.py::test_a_finder_output_survives_a_failed_terminal_write| — |
| F-23 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:96–98,748–770` | The handoff gate trusts the stored supported-score list without checking the claim’s evidence status. Reproduced through `check_change()`: a report marks C1 `unsupported`, reconciliation still lists C1 as supported, and a criterion citing C1 produces no findings. Contradictory records must not allow an unsupported claim to pass as a criterion basis. [criteria 33–34] | Codex | fixed — tests/test_research_handoff.py::test_a_supported_list_contradicting_the_claim_evidence_status_is_not_measured| — |

Phase 6 verdict: codex 01a1538f-5cf9-7c42-ad63-105eec047c79, 2026-10-19
Reviewer session: codex 01a1538f-5cf9-7c42-ad63-105eec047c79 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

## Phase 6 — F-1 capture, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-24 | BLOCKER | SPEC | capture | `scripts/stage2_swarm.py` repository seat launch (built in `scripts/stage2_research_run.py`, `pi_command`) / Pi `read` tool | The repository seat reads absolute paths outside the worktree: in the attended capture with the real pinned Pi 1.2.0 (commit `2028c13`), `read` returned the fake home's `.ssh` canary and the state-store peer-result canary, and both reached the model. [criterion 52] | attended capture | fixed — tests/test_stage2_repository_pathlock.py::test_an_absolute_path_outside_the_worktree_is_refused | — |

Source: the attended F-1 offline capture, 2026-10-19T11:12:34Z, recorded in research.md ("F-1 attended offline capture — 2026-10-19"). The maintainer ruled the repair in Q-16 (decisions.md). Booked first as `taken — spec criterion 52`, then repaired by the path lock (`scripts/stage2_repository_pathlock.mjs`, loaded as the repository seat's one `-e`) and booked `fixed`; also covered: `..` escape, symlink escape, `~`, a glob outside, and the launch argv test `test_the_repository_seat_launch_loads_only_the_path_lock`.

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 535 files, 1535 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-25 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:576–581` | A level-three heading beneath `## Acceptance criteria` disables Basis checking for every following criterion. Reproduced through `check_change()`: a criterion without an origin fails normally, but inserting `### Functional` makes it pass with no findings. The existing criterion-ledger reader still recognises that criterion. Subsections must not turn traceability checking into an empty-set success. [criterion 34] | Codex | fixed — tests/test_research_handoff.py::test_a_subsection_heading_does_not_end_basis_checking | — |
| F-26 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:1178–1189` | If all stages succeed but `Store.finish_run()` raises `StoreWriteError`, the runner has already published the run as `complete`. Reproduced with an isolated finalization failure: the command raises `CallFailed`, while the published status remains complete without the storage-failure reason. The handoff gate can therefore consume evidence from a run required to end incomplete with `state-store-unwritable`. [criterion 57] | Codex | fixed — tests/test_stage2_swarm.py::test_a_failed_store_finish_never_leaves_a_complete_publication | — |
| F-27 | MAJOR | SPEC | base | `scripts/stage2_availability.py:679–701,726–789`; `tests/test_stage2_research_availability.py:690–704` | Both swarms exist on the base branch, but review preparation retains its own rule validation and calls `runner.run_reviewer()` rather than the shared `probe_go()` used by research preparation. The required single implementation of validation and probing was not delivered. The shared-helper test exercises only research preparation, so it cannot detect the missing review counterpart. [criterion 50; design, Preparation → selection → receipt] | Codex | fixed — tests/test_stage2_availability.py::test_review_preparation_uses_the_shared_rule_validation_and_probe | — |

Phase 6 verdict: codex 01a15451-9861-7fe0-8369-255c5c01d9b9, 2026-10-19
Reviewer session: codex 01a15451-9861-7fe0-8369-255c5c01d9b9 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1549 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-28 | MAJOR | SPEC | fix-r3 | `scripts/stage2_research_run.py:1184–1193`; `scripts/stage2_research_store.py:374–377` | The run is stored as complete before research is published. Reproduced with `publish()` raising `OSError`: nothing is published, but the next resume rejects the finished results as “was published complete,” forcing their calls to repeat despite unchanged inputs. A failed publication must preserve reuse eligibility. [criterion 53] | Codex | fixed — tests/test_stage2_swarm.py::test_a_failed_publication_keeps_the_results_reusable | — |
| F-29 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:1113–1116,1202–1204` | A free researcher that retrieves a page and then times out with empty stdout/stderr loses its receipt. Reproduced through `compose()`: receipts alone produce no partial-evidence block. When required seats succeed, completion clears the store containing the only remaining receipt. Available retrieval evidence must survive that best-effort failure. [criterion 18; design, Data model — Slot] | Codex | fixed — tests/test_stage2_swarm.py::test_a_receipt_without_output_survives_a_complete_run | — |
| F-30 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:1202–1207` | Reproduced with `Store.clear()` raising `StoreWriteError`: the command fails with exit 1 after publishing status `complete`, without recording `state-store-unwritable`. The handoff gate can consequently consume a run whose storage operation failed. This failure must leave an incomplete publication with the required reason. [criterion 57] | Codex | fixed — tests/test_stage2_swarm.py::test_a_failed_store_clear_never_leaves_a_complete_publication | — |

Phase 6 verdict: codex 01a154b3-c0dd-7ed3-aa10-32f5f7fda4c1, 2026-10-19
Reviewer session: codex 01a154b3-c0dd-7ed3-aa10-32f5f7fda4c1 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1554 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-31 | MAJOR | SPEC | fix-r4 | `scripts/stage2_research_store.py:303–359`; `scripts/stage2_research_run.py:1085–1102` | A process killed after `stage_clear()` but before the research append leaves every stored run under `.discarded-*`. Resume searches only top-level run directories and performs no recovery. An in-memory filesystem reproduction returns “no stored run” although the unpublished records remain present, forcing completed calls to repeat. This interruption case survives the F-28 exception-handling repair. [criterion 53] | Codex | fixed — tests/test_stage2_swarm.py::test_a_run_killed_after_staging_the_clear_is_recovered_on_resume | — |
| F-32 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:900–909,1169–1175` | A judge response containing a disagreement with `claims: ["known-id", {}]` raises an unhandled `TypeError` when converted to a set. Reproduced through `validate_judge()`. The exception bypasses report rejection and incomplete publication, so a malformed required contribution ends with a traceback instead of the required retained evidence and incomplete record. [criterion 18] | Codex | fixed — tests/test_stage2_swarm.py::test_a_judge_answer_with_unhashable_members_is_a_malformed_contribution | — |
| F-33 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:156–184,637–654` | The handoff gate checks question claim links for string type but never checks that their targets exist. Reproduced through `check_change()`: a complete report contains only C1, its decision question links nonexistent C2, and an answered Q-record closes the derived item; the gate returns no findings. Dangling evidence links must produce not-measured exit 3. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_a_dangling_question_claim_link_is_not_measured | — |

Phase 6 verdict: codex 01a154d2-600a-7b41-a7e6-94ba6fbe4b42, 2026-10-19
Reviewer session: codex 01a154d2-600a-7b41-a7e6-94ba6fbe4b42 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1560 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-34 | BLOCKER | SPEC | base | `scripts/stage2_research_dispatch.py:90–105` | Cancellation leaves descendants running when the process-group leader exits on SIGTERM but a descendant ignores it. A local subprocess reproduction confirms that `_stop_and_reap()` returns while the descendant remains alive; SIGKILL is sent only when waiting for the leader times out. Security cancellation must stop the entire launched group. [criteria 12, 36] | Codex | fixed — tests/test_stage2_research_dispatch.py::test_cancellation_kills_a_descendant_that_ignores_sigterm_after_the_leader_exited | — |
| F-35 | MAJOR | SPEC | fix-r3 | `scripts/stage2_research_run.py:1199–1209`; `scripts/stage2_research_store.py:455–458` | New interruption evidence after the staged-clear recovery: SIGKILL immediately after `finish_run()` and before `publish()` leaves an unpublished run marked complete outside any staging directory. An in-memory reproduction makes resume reject its successful results as “was published complete,” forcing matching calls to repeat. Unpublished results must remain reusable. [criterion 53] | Codex | fixed — tests/test_stage2_swarm.py::test_a_run_killed_between_finishing_the_store_and_publishing_stays_reusable | — |
| F-36 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:277–325,750–755` | A complete run whose manifest gives `plans/changes/other/spec.md` but whose map omits that path passes `check_change()` with an empty spec neighbours list and no maintainer drop answer. Locally reproduced with zero findings. Required neighbours come exclusively from the map, so contradictory records silently erase a human-given dependency. [criteria 30, 33] | Codex | fixed — tests/test_research_handoff.py::test_a_manifest_given_path_the_map_omits_is_not_measured | — |
| F-37 | MINOR | SPEC | base | `scripts/stage2_research_run.py:312–317,1035–1040` | When the latest stored run recorded a security refusal, the next run starts model calls without reporting that source run, refused slot or reason. Resume reasons are retained only for the later published manifest; the opening and dispatch paths never print them. The required diagnostic must appear before any model call. [criterion 56] | Codex | fixed — tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call | — |

Phase 6 verdict: codex 01a15575-8e14-7731-860f-e4a68ea2a910, 2026-10-19
Reviewer session: codex 01a15575-8e14-7731-860f-e4a68ea2a910 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-19: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1572 commits, 12 rules.

## Phase 6 — Codex, 2026-10-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-38 | BLOCKER | SPEC | base | `scripts/stage2_availability.py:654–671` | Two concurrent consumers can accept the same single-use receipt: both read and validate it before either deletes it, and `unlink(missing_ok=True)` lets both succeed. Reproduced with synchronized readers. If one consumer pauses until the other's run releases the store lock, both runs can launch using that receipt. Consumption must atomically exclude the second consumer. [criterion 44] | Codex | fixed — tests/test_stage2_research_availability.py::test_concurrent_consumers_cannot_share_a_single_use_receipt | — |
| F-39 | BLOCKER | SPEC | fix-r5 | `scripts/check_research_handoff.py:637–654` | The handoff gate still accepts invalid evidence links after the F-33 repair. New reproductions return no findings when a report question cites another seat's claim, and when a judge disagreement cites `missing-claim` alongside an existing claim and its item has an answered record. Report links must remain within their report, and disagreement targets must exist; malformed links require exit 3. [criteria 27, 33] | Codex | fixed — tests/test_research_handoff.py::test_evidence_links_stay_in_their_report_or_judge_run | — |

Phase 6 verdict: codex 01a1561f-d0bf-7c00-83f9-a144ae4548d4, 2026-10-19
Reviewer session: codex 01a1561f-d0bf-7c00-83f9-a144ae4548d4 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1581 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +28 -0
> - `scripts/check_research_handoff.py` +11 -2
> - `scripts/stage2_availability.py` +6 -1
> - `tests/test_research_handoff.py` +36 -0
> - `tests/test_stage2_research_availability.py` +32 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [ruleset] $ lauf_cmd
> .........................................................F.............. [ 80%]
> ..................                                                       [100%]
> =================================== FAILURES ===================================
> ________________ test_master_has_a_ruleset_with_required_checks ________________
>
>     @pytest.mark.skipif(
>         os.environ.get(LIVE_ENV) != "1",
>         reason="reads GitHub; runs in the gate ruleset on a writer machine (decisions/gates.yaml)",
>     )
>     def test_master_has_a_ruleset_with_required_checks() -> None:
>         """The live ruleset of the default branch holds the six requirements.
>     
>         The name `master` is the one RB-M6 has carried since 1.0.0; the branch is
>         whatever the API calls the default.
>         """
>         findings = measure()
>         message = "\n".join(findings)
>         if any(f.startswith("not measured:") for f in findings):
>             message += (
>                 "\nThe gate `ruleset` needs network and a `gh` login on this machine; "
>                 "not measured is red, never green (RB-M6)."
>             )
> >       assert not findings, message
> E       AssertionError: not measured: repos/{owner}/{repo}/rules/branches/main: exit 1: gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)
> E         The gate `ruleset` needs network and a `gh` login on this machine; not measured is red, never green (RB-M6).
> E       assert not ['not measured: repos/{owner}/{repo}/rules/branches/main: exit 1: gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)']
>
> tests/test_repo_settings.py:821: AssertionError
> 1 failed, 89 passed in 5.59s
> ── [ruleset] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14527 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1584 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +38 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [ruleset] $ lauf_cmd
> .........................................................F.............. [ 80%]
> ..................                                                       [100%]
> =================================== FAILURES ===================================
> ________________ test_master_has_a_ruleset_with_required_checks ________________
>
>     @pytest.mark.skipif(
>         os.environ.get(LIVE_ENV) != "1",
>         reason="reads GitHub; runs in the gate ruleset on a writer machine (decisions/gates.yaml)",
>     )
>     def test_master_has_a_ruleset_with_required_checks() -> None:
>         """The live ruleset of the default branch holds the six requirements.
>     
>         The name `master` is the one RB-M6 has carried since 1.0.0; the branch is
>         whatever the API calls the default.
>         """
>         findings = measure()
>         message = "\n".join(findings)
>         if any(f.startswith("not measured:") for f in findings):
>             message += (
>                 "\nThe gate `ruleset` needs network and a `gh` login on this machine; "
>                 "not measured is red, never green (RB-M6)."
>             )
> >       assert not findings, message
> E       AssertionError: not measured: repos/{owner}/{repo}/rules/branches/main: exit 1: gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)
> E         The gate `ruleset` needs network and a `gh` login on this machine; not measured is red, never green (RB-M6).
> E       assert not ['not measured: repos/{owner}/{repo}/rules/branches/main: exit 1: gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)']
>
> tests/test_repo_settings.py:821: AssertionError
> 1 failed, 89 passed in 5.30s
> ── [ruleset] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14576 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1588 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +11 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 114 lines of this gate left out …]
>         # Criterion 42. Planted fault: a failed source launches free models, aborts required slots or reads as measured empty.
>         options = {}
>         if fault.startswith("http"):
>             sources.metadata_status = int(fault.split("-")[1])
>         elif fault == "unparsable":
>             sources.metadata_body = "{broken"
>         elif fault == "timeout":
>             sources.metadata_delay = 2.5
>             options["deadlineMs"] = 800
>         elif fault == "not-an-object":
>             sources.metadata_body = "[]"
>         else:
>             sources.metadata_body = "{}"
> >       result = select(collect(tmp_path, sources, **options))
>
> tests/test_stage2_research_catalog.py:708: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2_research_catalog.py:152: in select
>     return swarm.select_research_catalog(
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> bridge = {'baseline': ['claude-haiku-5-5', 'minimax-m3', 'qwen3.7-plus', 'qwen3.8-flash', 'qwen3.8-max', 'deepseek-v4-flash', ...], 'elapsed_ms': 830, 'exit_code': 1, 'models_store': {}, ...}
> policy = {'exclude': [], 'include': [], 'provider': 'opencode-go', 'suffix': '-free'}
> fixed_ids = ['deepseek-v4.1-flash', 'mimo-v2.6-flash', 'qwen3.8-flash']
>
>     def select_research_catalog(bridge, policy, fixed_ids, *, expected_version, measured_wire_apis=("openai-completions",)):
>         """Intersect a fresh pinned Pi response with capability evidence, never a cache union.
>     
>         The bridge transports raw source bodies. Python retains duplicate identity and
>         malformed-field evidence that the runtime's permissive parser would discard.
>         This selects a roster and classifies every seat candidate (`fixed_ids`, the
>         preferred models) and every paid model of the fresh overlay; it does not
>         authorize or dispatch any model. A candidate that is absent, baseline-only,
>         non-chat, malformed or on an unmeasured wire API is skipped with its raw
>         evidence, never a failure of the whole preflight (Q-12, Q-14).
>         """
>         validate_research_free_policy(policy)
>         provider = policy["provider"]
>         sources = bridge.get("sources", {})
>         pi = sources.get("pi", {})
>         runtime = bridge.get("pi_runtime", {})
>         if (
>             bridge.get("exit_code") != 0
>             or bridge.get("pi_version") != expected_version
>             or pi.get("status") != 200
>             or runtime.get("aborted")
>             or runtime.get("errors")
>             or provider not in bridge.get("models_store", {})
>         ):
> >           raise ResearchCatalogError(bridge.get("reason") or "pi-refresh-failed")
> E           stage2_swarm.ResearchCatalogError: pi-timeout
>
> scripts/stage2_swarm.py:103: ResearchCatalogError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_preflight_shared_deadline_has_asymmetric_failure_rules[metadata]
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[timeout]
> 2 failed, 3043 passed, 16 skipped in 381.56s (0:06:21)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruleset] $ lauf_cmd
> .........................................................F.............. [ 80%]
> ..................                                                       [100%]
> =================================== FAILURES ===================================
> ________________ test_master_has_a_ruleset_with_required_checks ________________
>
>     @pytest.mark.skipif(
>         os.environ.get(LIVE_ENV) != "1",
>         reason="reads GitHub; runs in the gate ruleset on a writer machine (decisions/gates.yaml)",
>     )
>     def test_master_has_a_ruleset_with_required_checks() -> None:
>         """The live ruleset of the default branch holds the six requirements.
>     
>         The name `master` is the one RB-M6 has carried since 1.0.0; the branch is
>         whatever the API calls the default.
>         """
>         findings = measure()
>         message = "\n".join(findings)
>         if any(f.startswith("not measured:") for f in findings):
>             message += (
>                 "\nThe gate `ruleset` needs network and a `gh` login on this machine; "
>                 "not measured is red, never green (RB-M6)."
>             )
> >       assert not findings, message
> E       AssertionError: not measured: repos/{owner}/{repo}/rules/branches/main: exit 1: gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)
> E         The gate `ruleset` needs network and a `gh` login on this machine; not measured is red, never green (RB-M6).
> E       assert not ['not measured: repos/{owner}/{repo}/rules/branches/main: exit 1: gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)']
>
> tests/test_repo_settings.py:821: AssertionError
> 1 failed, 89 passed in 5.49s
> ── [ruleset] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14625 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Orchestrator, 2026-10-20: the repair run above failed only on the `ruleset` gate in attempts 1 and 2 — GitHub refused to read branch rulesets (HTTP 403) after the repository moved to an organisation on the free plan; attempt 3 added two failing tests of its own. After the plan upgrade the rulesets read again, and the tree left by attempt 3 passed a full `make verify` (3045 passed, 16 skipped, 22:48 UTC). Red first was checked by hand: both tests, copied onto the code at `fbab88b`, fail there (F-38: 1 failed; F-39: 9 of 13 cases failed). Booked as a hand repair.

Stage-2 call, 2026-10-20: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1594 commits, 12 rules.

## Phase 6 — Codex, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-40 | MAJOR | SPEC | base | `scripts/stage2.py:3685` | A research header containing both `class: architectural` and `class: bounded` silently selects bounded. Locally reproduced through `declared_class()`: YAML parsing discards the first declaration, allowing exploration to bypass the swarm and its selection receipt. Conflicting declarations must refuse before model calls with exit 2. [criterion 4] | Codex | fixed — tests/test_stage2_swarm.py::test_duplicate_header_classes_refuse_before_calls | — |
| F-41 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:590–593` | Repeating a criterion number overwrites its earlier Basis before checking. Locally reproduced through `check_change()`: the first criterion cites nonexistent C7; a second criterion numbered 1 cites an answered Q-record; the gate returns no findings. Duplicate numbering must not erase an unchecked criterion. [criteria 33–34] | Codex | fixed — tests/test_research_handoff.py::test_duplicate_criterion_numbers_are_not_measured | — |
| F-42 | MAJOR | SPEC | fix-r7 | `scripts/check_research_handoff.py:654–656` | An incomplete run containing reconciliation with `disagreements: null` raises an uncaught TypeError. Locally reproduced alongside an otherwise valid complete run. Complete-run shape validation is skipped, but the new link checker still iterates this field; malformed evidence therefore crashes instead of reporting not measured with exit 3. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_malformed_incomplete_disagreements_are_not_measured | — |
| F-43 | MINOR | SPEC | base | `scripts/stage2_research_run.py:932,1021–1048` | The runner measures judge packet size but never publishes it or the capacity policy in the run manifest. Successful publication consequently omits the required character limit, capacity, reserves, conversion and dated sources. These fields must accompany the run so its applied judge limit remains auditable. [criterion 14; design, Data model — Run manifest] | Codex | fixed — tests/test_stage2_swarm.py::test_manifest_publishes_judge_packet_size_and_capacity_policy | — |

Phase 6 verdict: codex 01a1565a-a33f-70e1-a957-f3c689094c50, 2026-10-20
Reviewer session: codex 01a1565a-a33f-70e1-a957-f3c689094c50 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1596 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +37 -0
> - `scripts/check_research_handoff.py` +11 -1
> - `scripts/stage2.py` +10 -0
> - `scripts/stage2_research_run.py` +3 -1
> - `tests/test_research_handoff.py` +26 -0
> - `tests/test_stage2_swarm.py` +39 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1596 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +22 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 25 lines of this gate left out …]
> ........................................................................ [ 53%]
> ........................................................................ [ 56%]
> ........................................................................ [ 58%]
> ........................................................................ [ 60%]
> ........................................................................ [ 63%]
> ........................................................................ [ 65%]
> ........................................................................ [ 67%]
> ........................................................................ [ 70%]
> ........................................................................ [ 72%]
> ........................................................................ [ 74%]
> ........................................................................ [ 77%]
> ........................................................................ [ 79%]
> ........................................................................ [ 81%]
> ........................................................................ [ 84%]
> ..............................................................F......... [ 86%]
> ........................................................................ [ 89%]
> ........................................................................ [ 91%]
> ........................................................................ [ 93%]
> ........................................................................ [ 96%]
> ........................................................................ [ 98%]
> ..................................................                       [100%]
> =================================== FAILURES ===================================
> ___________ test_terminal_record_survives_sigkill_after_the_outcome ____________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
> state_home = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-34/popen-gw2/test_terminal_record_survives_0/xdg-state')
>
>     def test_terminal_record_survives_sigkill_after_the_outcome(state_home):
>         m = module()
>         gate = state_home / "release-s2"
>         script = DRIVER.format(scripts=str(SCRIPTS), binding=BINDING, gate=str(gate))
>         proc = subprocess.Popen(
>             [sys.executable, "-c", script],
>             stdout=subprocess.PIPE,
>             text=True,
>             env={**os.environ, "XDG_STATE_HOME": str(state_home)},
>         )
>         try:
>             assert pipe_line(proc) == "TERMINAL s1"
> >           assert pipe_line(proc) == "LAUNCHED s2"
>
> tests/test_stage2_research_store.py:168: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> proc = <Popen: returncode: None args: ['/Users/mikypiky/coding-harness/.claude/work...>
> timeout = 60.0
>
>     def pipe_line(proc, timeout=60.0):
>         ready, _, _ = select.select([proc.stdout], [], [], timeout)
> >       assert ready, "driver printed no marker in time"
> E       AssertionError: driver printed no marker in time
> E       assert []
>
> tests/test_stage2_research_store.py:111: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome
> 1 failed, 3057 passed, 16 skipped in 313.19s (0:05:13)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14709 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1596 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +15 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Orchestrator, 2026-10-20: the round-8 repair run above failed on form, not on the code: attempt 1 added no measured line under `## Time used`, attempt 2 lost one load-sensitive test (`tests/test_stage2_research_store.py`, "driver printed no marker in time"; 3057 passed), attempt 3 changed only `plan.md`. The code in the tree passed a full `make verify` (3058 passed, 16 skipped). Red first was checked by hand: the four tests, copied onto the code at `6c5e31a`, fail there (12 of 13 cases). Booked as a hand repair.

Stage-2 call, 2026-10-20: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1597 commits, 12 rules.

## Phase 6 — Codex, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-44 | BLOCKER | SPEC | fix-r6 | `scripts/stage2_research_dispatch.py:73–103` | Cancellation still leaves descendants alive when the process-group leader exits before `_stop_and_reap()` begins. New evidence after the earlier cancellation repair: a local subprocess reproduction reaps the leader first, then calls the stop routine; its descendant survives. `_own_group()` returns false for the vanished leader, so neither signal reaches the surviving group. Security cancellation must stop that group. [criteria 12, 36] | Codex | fixed — tests/test_stage2_research_dispatch.py::test_cancellation_kills_group_after_leader_was_already_reaped | — |
| F-45 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:298–324` | The gate accepts contradictory claim dispositions. Reproduced through `check_change()`: the judge marks a claim refuted, the stored scores list it as both refuted and supported, and a criterion cites it; the gate returns no findings. It trusts the supported list without checking exclusive dispositions or agreement with the judge. Contradictory evidence must produce not-measured exit 3. [criteria 33–34] | Codex | fixed — tests/test_research_handoff.py::test_contradictory_claim_dispositions_are_not_measured | — |
| F-46 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:429–440` | An invocation interrupted by SIGKILL before its terminal callback loses its individual leak-check evidence. Capturing `write_launch()` confirms that the durable launch record contains identity, prompt hash and time but no leak-check record; the audit line remains buffered in memory. Recovery can name the interrupted slot but cannot recover its check. The check must be durable before launch. [criteria 13, 51] | Codex | fixed — tests/test_stage2_swarm.py::test_launch_record_keeps_individual_leak_check_before_launch | — |

Phase 6 verdict: codex 01a1568b-9fc2-7d40-b892-ea021a1f8dae, 2026-10-20
Reviewer session: codex 01a1568b-9fc2-7d40-b892-ea021a1f8dae — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1599 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +35 -0
> - `scripts/check_research_handoff.py` +65 -0
> - `scripts/stage2_research_dispatch.py` +12 -2
> - `scripts/stage2_research_run.py` +5 -1
> - `tests/test_research_handoff.py` +86 -3
> - `tests/test_stage2_research_dispatch.py` +39 -0
> - `tests/test_stage2_swarm.py` +24 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1599 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +30 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1599 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +9 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 51 lines of this gate left out …]
> sources = <test_stage2_research_catalog.Sources object at 0x10bdbbef0>
> slow = 'metadata'
>
>     @pytest.mark.parametrize("slow", ["pi", "metadata"])
>     def test_preflight_shared_deadline_has_asymmetric_failure_rules(tmp_path, sources, slow):
>         setattr(sources, slow + "_delay", 2.5)
>         started = time.monotonic()
>         bridge = collect(tmp_path, sources, deadlineMs=1200)
>         assert time.monotonic() - started < 3, "the two reads did not share one deadline"
>         if slow == "pi":
>             with pytest.raises(swarm.ResearchCatalogError) as failure:
>                 select(bridge)
>             assert failure.value.exit_code == 1
>         else:
> >           result = select(bridge)
>
> tests/test_stage2_research_catalog.py:361: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2_research_catalog.py:152: in select
>     return swarm.select_research_catalog(
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> bridge = {'baseline': ['claude-haiku-5-5', 'minimax-m3', 'qwen3.7-plus', 'qwen3.8-flash', 'qwen3.8-max', 'deepseek-v4-flash', ...], 'elapsed_ms': 1405, 'exit_code': 1, 'models_store': {}, ...}
> policy = {'exclude': [], 'include': [], 'provider': 'opencode-go', 'suffix': '-free'}
> fixed_ids = ['deepseek-v4.1-flash', 'mimo-v2.6-flash', 'qwen3.8-flash']
>
>     def select_research_catalog(bridge, policy, fixed_ids, *, expected_version, measured_wire_apis=("openai-completions",)):
>         """Intersect a fresh pinned Pi response with capability evidence, never a cache union.
>     
>         The bridge transports raw source bodies. Python retains duplicate identity and
>         malformed-field evidence that the runtime's permissive parser would discard.
>         This selects a roster and classifies every seat candidate (`fixed_ids`, the
>         preferred models) and every paid model of the fresh overlay; it does not
>         authorize or dispatch any model. A candidate that is absent, baseline-only,
>         non-chat, malformed or on an unmeasured wire API is skipped with its raw
>         evidence, never a failure of the whole preflight (Q-12, Q-14).
>         """
>         validate_research_free_policy(policy)
>         provider = policy["provider"]
>         sources = bridge.get("sources", {})
>         pi = sources.get("pi", {})
>         runtime = bridge.get("pi_runtime", {})
>         if (
>             bridge.get("exit_code") != 0
>             or bridge.get("pi_version") != expected_version
>             or pi.get("status") != 200
>             or runtime.get("aborted")
>             or runtime.get("errors")
>             or provider not in bridge.get("models_store", {})
>         ):
> >           raise ResearchCatalogError(bridge.get("reason") or "pi-refresh-failed")
> E           stage2_swarm.ResearchCatalogError: pi-timeout
>
> scripts/stage2_swarm.py:103: ResearchCatalogError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_preflight_shared_deadline_has_asymmetric_failure_rules[metadata]
> 1 failed, 3071 passed, 16 skipped in 307.53s (0:05:07)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14808 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Orchestrator, 2026-10-20: the round-9 repair run above failed on form again: attempts 1 and 2 added no measured line under `## Time used`; attempt 3 lost one load-sensitive test. The code in the tree: a first full `make verify` lost `tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome` ("driver printed no marker in time"; 3071 passed), which passed 5 of 5 times alone and with the whole file under `-n 8` (bead coding-harness-jik); the second full `make verify` was green (3072 passed, 16 skipped, 00:28:45Z to 00:35:36Z). Red first was checked by hand: the three proving tests, copied onto the code at `d8348ec`, fail there; `test_consistent_judge_and_score_dispositions_remain_measured` is a guard and passes on both sides. Booked as a hand repair.

Stage-2 call, 2026-10-20: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1600 commits, 12 rules.

## Phase 6 — Codex, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-47 | MAJOR | SPEC | base | `scripts/stage2_research_map.py:120–122`; `scripts/stage2_research_run.py:763–771` | A finder answer whose four categories contain `{"not_read": 42}` passes validation and remains `ok`, although map construction rejects it because its reasons are not text. Reproduced: `plan_reuse()` reuses that malformed result. Subsequent unchanged runs therefore repeat the merge call while retaining the invalid finder answer. Reject malformed reasons before advancing and exclude these results from reuse. [criteria 18, 53] | Codex | fixed — tests/test_stage2_swarm.py::test_malformed_finder_reasons_block_progress_and_reuse | — |
| F-48 | MAJOR | SPEC | base | `scripts/stage2.py:3676–3680` | An existing unreadable spec is treated as absent during class selection. New evidence beyond F-9’s malformed-YAML case: with research declaring `bounded` and reading the spec raising `UnicodeDecodeError`, `declared_class()` returns `bounded`. An architectural declaration in that spec can consequently be ignored, bypassing the swarm. Existing files that cannot be read must cause refusal with exit 2. [criterion 4] | Codex | fixed — tests/test_stage2_swarm.py::test_existing_unreadable_spec_refuses_class_selection | — |
| F-49 | MAJOR | SPEC | base | `scripts/check_research_handoff.py:113–120` | A spec header containing a YAML sequence key, such as `? [bad,key]`, raises an uncaught `TypeError` when the uniqueness checker tests set membership. Reproduced through `check_change()` with otherwise valid complete research. The gate crashes instead of reporting unreadable evidence as not measured with exit 3. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_unhashable_spec_header_keys_are_not_measured | — |

Phase 6 verdict: codex 01a156bc-9878-7e10-9061-cd602862dba2, 2026-10-20
Reviewer session: codex 01a156bc-9878-7e10-9061-cd602862dba2 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1617 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +36 -0
> - `scripts/check_research_handoff.py` +6 -3
> - `scripts/stage2.py` +5 -1
> - `scripts/stage2_research_map.py` +4 -0
> - `tests/test_research_handoff.py` +11 -0
> - `tests/test_stage2_research_map.py` +11 -0
> - `tests/test_stage2_swarm.py` +49 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1621 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +33 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1623 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +9 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 26 lines of this gate left out …]
> ........................................................................ [ 55%]
> ........................................................................ [ 58%]
> ........................................................................ [ 60%]
> ........................................................................ [ 62%]
> ........................................................................ [ 65%]
> ........................................................................ [ 67%]
> ........................................................................ [ 69%]
> ........................................................................ [ 72%]
> ........................................................................ [ 74%]
> ........................................................................ [ 76%]
> ........................................................................ [ 78%]
> ........................................................................ [ 81%]
> ........................................................................ [ 83%]
> ........................................................................ [ 85%]
> ........................................................................ [ 88%]
> ..............................F......................................... [ 90%]
> ........................................................................ [ 92%]
> ........................................................................ [ 95%]
> ........................................................................ [ 97%]
> ........................................................................ [ 99%]
> ....                                                                     [100%]
> =================================== FAILURES ===================================
> ___________ test_terminal_record_survives_sigkill_after_the_outcome ____________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
> state_home = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-154/popen-gw2/test_terminal_record_survives_0/xdg-state')
>
>     def test_terminal_record_survives_sigkill_after_the_outcome(state_home):
>         m = module()
>         gate = state_home / "release-s2"
>         script = DRIVER.format(scripts=str(SCRIPTS), binding=BINDING, gate=str(gate))
>         proc = subprocess.Popen(
>             [sys.executable, "-c", script],
>             stdout=subprocess.PIPE,
>             text=True,
>             env={**os.environ, "XDG_STATE_HOME": str(state_home)},
>         )
>         try:
>             assert pipe_line(proc) == "TERMINAL s1"
> >           assert pipe_line(proc) == "LAUNCHED s2"
>
> tests/test_stage2_research_store.py:168: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> proc = <Popen: returncode: None args: ['/Users/mikypiky/coding-harness/.claude/work...>
> timeout = 60.0
>
>     def pipe_line(proc, timeout=60.0):
>         ready, _, _ = select.select([proc.stdout], [], [], timeout)
> >       assert ready, "driver printed no marker in time"
> E       AssertionError: driver printed no marker in time
> E       assert []
>
> tests/test_stage2_research_store.py:111: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome
> 1 failed, 3083 passed, 16 skipped in 444.03s (0:07:24)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14898 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1627 commits, 12 rules.

## Phase 6 — Codex, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-50 | BLOCKER | SPEC | fix-r7 | `scripts/stage2_availability.py:655–675` | New evidence after the F-38 repair: two synchronized consumers validate receipt A; the first deletes A, preparation publishes receipt B, and the second deletes B while also accepting A. An in-memory reproduction accepts A twice and removes B. Consumption must reject an already consumed receipt even when its path has been replaced. [criterion 44] | Codex | fixed — tests/test_stage2_research_availability.py::test_consumed_receipt_cannot_delete_a_new_preparation | — |
| F-51 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:642–643`; `scripts/stage2_research_store.py:110–112,281–285` | An eligible catalog model named `vendor/alpha-free` is selected, but its generated slot id contains `/` and fails the store’s filename guard. Reproduced through selection and dispatch: the best-effort slot causes `state-store-unwritable`, cancels dispatch and returns exit 1. Supported model identities must yield safe storage keys without making a free contribution abort required work. [criteria 18, 39] | Codex | fixed — tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion | — |
| F-52 | MAJOR | SPEC | base | `scripts/check_research_handoff.py:822,926–930` | With valid complete research and a spec containing invalid UTF-8, the handoff gate raises an uncaught `UnicodeDecodeError`. Reproduced through `run()` with the spec read failing. This read bypasses the unreadable-evidence handling, producing a traceback instead of reporting not measured with exit 3. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_unreadable_spec_is_not_measured | — |

Phase 6 verdict: codex 01a158c5-b05d-7902-b003-5ef1128c3cd2, 2026-10-20
Reviewer session: codex 01a158c5-b05d-7902-b003-5ef1128c3cd2 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 session, 2026-10-20: attempt d0fd2830a244 · model opencode-go/deepseek-v4.1-flash · endpoint opencode-go · handover .stage2-sessions/deepseek-review-handover.md · leak check clean over 536 files, 1628 commits, 12 rules · dispatch accepted.

Stage-2 call, 2026-10-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1629 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/findings.md` +6 -0
> - `plans/changes/research-swarm/plan.md` +21 -0
> - `scripts/check_research_handoff.py` +4 -1
> - `scripts/stage2_availability.py` +35 -13
> - `scripts/stage2_research_run.py` +11 -2
> - `tests/test_research_handoff.py` +9 -0
> - `tests/test_stage2_research_availability.py` +54 -0
> - `tests/test_stage2_swarm.py` +18 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 56 lines of this gate left out …]
>     def test_models_dev_failure_excludes_free_and_keeps_required_slots(tmp_path, sources, fault):
>         # Criterion 42. Planted fault: a failed source launches free models, aborts required slots or reads as measured empty.
>         options = {}
>         if fault.startswith("http"):
>             sources.metadata_status = int(fault.split("-")[1])
>         elif fault == "unparsable":
>             sources.metadata_body = "{broken"
>         elif fault == "timeout":
>             sources.metadata_delay = 2.5
>             options["deadlineMs"] = 800
>         elif fault == "not-an-object":
>             sources.metadata_body = "[]"
>         else:
>             sources.metadata_body = "{}"
> >       result = select(collect(tmp_path, sources, **options))
>
> tests/test_stage2_research_catalog.py:708: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2_research_catalog.py:152: in select
>     return swarm.select_research_catalog(
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> bridge = {'baseline': ['claude-haiku-5-5', 'minimax-m3', 'qwen3.7-plus', 'qwen3.8-flash', 'qwen3.8-max', 'deepseek-v4-flash', ...], 'elapsed_ms': 923, 'exit_code': 1, 'models_store': {}, ...}
> policy = {'exclude': [], 'include': [], 'provider': 'opencode-go', 'suffix': '-free'}
> fixed_ids = ['deepseek-v4.1-flash', 'mimo-v2.6-flash', 'qwen3.8-flash']
>
>     def select_research_catalog(bridge, policy, fixed_ids, *, expected_version, measured_wire_apis=("openai-completions",)):
>         """Intersect a fresh pinned Pi response with capability evidence, never a cache union.
>     
>         The bridge transports raw source bodies. Python retains duplicate identity and
>         malformed-field evidence that the runtime's permissive parser would discard.
>         This selects a roster and classifies every seat candidate (`fixed_ids`, the
>         preferred models) and every paid model of the fresh overlay; it does not
>         authorize or dispatch any model. A candidate that is absent, baseline-only,
>         non-chat, malformed or on an unmeasured wire API is skipped with its raw
>         evidence, never a failure of the whole preflight (Q-12, Q-14).
>         """
>         validate_research_free_policy(policy)
>         provider = policy["provider"]
>         sources = bridge.get("sources", {})
>         pi = sources.get("pi", {})
>         runtime = bridge.get("pi_runtime", {})
>         if (
>             bridge.get("exit_code") != 0
>             or bridge.get("pi_version") != expected_version
>             or pi.get("status") != 200
>             or runtime.get("aborted")
>             or runtime.get("errors")
>             or provider not in bridge.get("models_store", {})
>         ):
> >           raise ResearchCatalogError(bridge.get("reason") or "pi-refresh-failed")
> E           stage2_swarm.ResearchCatalogError: pi-timeout
>
> scripts/stage2_swarm.py:103: ResearchCatalogError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[timeout]
> 1 failed, 3092 passed, 16 skipped in 543.80s (0:09:03)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 14992 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1629 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +41 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 96 lines of this gate left out …]
>         pi = sources.get("pi", {})
>         runtime = bridge.get("pi_runtime", {})
>         if (
>             bridge.get("exit_code") != 0
>             or bridge.get("pi_version") != expected_version
>             or pi.get("status") != 200
>             or runtime.get("aborted")
>             or runtime.get("errors")
>             or provider not in bridge.get("models_store", {})
>         ):
> >           raise ResearchCatalogError(bridge.get("reason") or "pi-refresh-failed")
> E           stage2_swarm.ResearchCatalogError: pi-timeout
>
> scripts/stage2_swarm.py:103: ResearchCatalogError
> _______ test_preflight_shared_deadline_has_asymmetric_failure_rules[pi] ________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-192/popen-gw2/test_preflight_shared_deadline0')
> sources = <test_stage2_research_catalog.Sources object at 0x10bbe58e0>
> slow = 'pi'
>
>     @pytest.mark.parametrize("slow", ["pi", "metadata"])
>     def test_preflight_shared_deadline_has_asymmetric_failure_rules(tmp_path, sources, slow):
>         setattr(sources, slow + "_delay", 2.5)
>         started = time.monotonic()
>         bridge = collect(tmp_path, sources, deadlineMs=1200)
> >       assert time.monotonic() - started < 3, "the two reads did not share one deadline"
> E       AssertionError: the two reads did not share one deadline
> E       assert (50839.06830525 - 50834.080300666) < 3
> E        +  where 50839.06830525 = <built-in function monotonic>()
> E        +    where <built-in function monotonic> = time.monotonic
>
> tests/test_stage2_research_catalog.py:355: AssertionError
> ____ test_preflight_shared_deadline_has_asymmetric_failure_rules[metadata] _____
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-192/popen-gw2/test_preflight_shared_deadline1')
> sources = <test_stage2_research_catalog.Sources object at 0x10bc29ee0>
> slow = 'metadata'
>
>     @pytest.mark.parametrize("slow", ["pi", "metadata"])
>     def test_preflight_shared_deadline_has_asymmetric_failure_rules(tmp_path, sources, slow):
>         setattr(sources, slow + "_delay", 2.5)
>         started = time.monotonic()
>         bridge = collect(tmp_path, sources, deadlineMs=1200)
> >       assert time.monotonic() - started < 3, "the two reads did not share one deadline"
> E       AssertionError: the two reads did not share one deadline
> E       assert (50844.374599166 - 50839.226643041) < 3
> E        +  where 50844.374599166 = <built-in function monotonic>()
> E        +    where <built-in function monotonic> = time.monotonic
>
> tests/test_stage2_research_catalog.py:355: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[timeout]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_shared_deadline_has_asymmetric_failure_rules[pi]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_shared_deadline_has_asymmetric_failure_rules[metadata]
> 3 failed, 3090 passed, 16 skipped in 581.45s (0:09:41)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 15054 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1630 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +13 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 93 lines of this gate left out …]
>         validate_research_free_policy(policy)
>         provider = policy["provider"]
>         sources = bridge.get("sources", {})
>         pi = sources.get("pi", {})
>         runtime = bridge.get("pi_runtime", {})
>         if (
>             bridge.get("exit_code") != 0
>             or bridge.get("pi_version") != expected_version
>             or pi.get("status") != 200
>             or runtime.get("aborted")
>             or runtime.get("errors")
>             or provider not in bridge.get("models_store", {})
>         ):
> >           raise ResearchCatalogError(bridge.get("reason") or "pi-refresh-failed")
> E           stage2_swarm.ResearchCatalogError: pi-timeout
>
> scripts/stage2_swarm.py:103: ResearchCatalogError
> _________ test_catalog_shared_deadline_keeps_asymmetric_failure_rules __________
> [gw7] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-195/popen-gw7/test_catalog_shared_deadline_k0')
> sources = <test_stage2_research_catalog.Sources object at 0x1080fb980>
>
>     def test_catalog_shared_deadline_keeps_asymmetric_failure_rules(tmp_path, sources):
>         # Criteria 19, 41, 42. Planted fault: the reads start one after the other or get separate budgets; a Pi timeout
>         # dispatches; a models.dev timeout retries, extends the deadline or aborts fixed work.
>         # The margin between a read's planted delay and the shared deadline must cover the runtime's own start-up
>         # and Pi's initialisation under load (a 0.5 s margin failed on a loaded machine); two delays that together
>         # exceed the deadline still prove the reads overlap, because sequential reads could not finish inside it.
>         sources.pi_delay = sources.metadata_delay = 3.0
>         started = time.monotonic()
>         bridge = collect(tmp_path, sources, deadlineMs=5000)
>         assert time.monotonic() - started < 7.5, "the reads ran one after the other"
>         assert len(sources.requests) == 2, "both reads were not requested"
>         assert bridge["exit_code"] == 0 and bridge["elapsed_ms"] < 5400
>         assert len(pi_requests(sources)) == 1 and len([p for p, _ in sources.requests if p == "/metadata"]) == 1
>         # Both slow past one shared deadline: Pi decides (exit 1), the models.dev timeout is a reason, never a retry.
>         sources.pi_delay = sources.metadata_delay = 3.0
>         sources.requests.clear()
>         started = time.monotonic()
>         bridge = collect(tmp_path, sources, deadlineMs=1000)
>         assert time.monotonic() - started < 2.9, "the two reads received separate budgets"
>         assert bridge["sources"]["models_dev"]["outcome"] == "timeout"
>         with pytest.raises(swarm.ResearchCatalogError) as failure:
>             select(bridge)
>         assert failure.value.exit_code == 1
> >       assert len(sources.requests) == 2, "a timed-out read was retried"
> E       AssertionError: a timed-out read was retried
> E       assert 1 == 2
> E        +  where 1 = len([('/metadata', {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': '*', 'connection': 'keep-alive', ...})])
> E        +    where [('/metadata', {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': '*', 'connection': 'keep-alive', ...})] = <test_stage2_research_catalog.Sources object at 0x1080fb980>.requests
>
> tests/test_stage2_research_catalog.py:761: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[timeout]
> FAILED tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
> 2 failed, 3091 passed, 16 skipped in 579.86s (0:09:39)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 15103 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

## Phase 6 — independent reviewer, deepseek-v4.1-flash through a Pi session, 2026-10-20

Requested by the maintainer; launched through `stage2.py session` (attempt d0fd2830a244 and its relaunches; the Terminal dispatch truncated the command, bead coding-harness-rm8, so the captured command ran in the VS Code terminal). Read `e9cb7f5` only. Its file `.stage2-sessions/deepseek-review-findings.md` is copied below unchanged.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| D-1 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:480–483` | A repeated `## Q-<id> · …` record is skipped without any check whenever its body carries no `research_` line, so two contradictory maintainer answers to one question are measured instead of reported not measured. Reproduced through `check_change()`: one complete v2 run, whose only DECISION item is `<run>/H-1`, is closed by `## Q-1` with `status: answered`, `answered_by: maintainer`, `answer: "keep the neighbour"`, `research_items: [<run>/H-1]` and `research_neighbours: {keep: [plans/changes/other/spec.md], drop: [], add: []}`; a second `## Q-1` follows with `status: answered`, `answered_by: maintainer`, `answer: "drop the neighbour"` and no `research_` field. `parse_decisions()` sees `ident in records` and `any(line.startswith("research_"))` is false, so line 483 drops the later record: the gate keeps the first answer, requires the path in `neighbours:` and closes `H-1`, returning 0 for a spec that keeps the path and 1 ("the neighbours header lacks the required path") for a spec that follows the later drop answer — never the not-measured exit 3. The sibling case with a `research_` line in the repeat already raises `CannotMeasure` ("the record stands twice and carries research links", pinned by `test_unread_or_ambiguous_handoff_is_not_measured`, "one question id answered twice is ambiguous"), so the ambiguity does not depend on the research fields. Same class as F-16 and F-41: a duplicated identity whose later content silently decides the measurement. [criterion 33; criterion 32] | deepseek-v4.1-flash | fixed — tests/test_research_handoff.py::test_duplicate_question_identity_is_not_measured | — |
| D-2 | MINOR | SPEC | base | `scripts/stage2_research_run.py:671–678,1040–1050`; `scripts/stage2_research_store.py:466–494` | Stored results of stages the new run never reaches are never named, although the criterion requires every stored result it does not reuse to be named with its reason. `run_stage()` narrows the resume source to the stage's own slot prefix (`k == stage or k.startswith(stage + "-")`) before `plan_reuse()`, and `self.not_reused` is only filled from stages that are actually started, so `manifest["resume"]["not_reused"]` cannot name results of a later stage. Reproduced: run R1 stores 33 ok topic results and one failed judge result (incomplete at the judge, exit 1); a second run R2 with the same binding reuses the finders, merge and sentence from R1, then `stage_history()` raises `ResearchHistoryError` — the 60-second preparation deadline expiring over the mapped paths, or a `_git log`/`cat-file` failure — and `run()` stops with Stop(exit 1) before `run_stage("topics", …)` is reached. R2 publishes a manifest whose `resume.not_reused` is `[]` while its store directory holds the 33 unused topic results plus the failed judge result, so neither the reason ("not planned in this run") nor the slot ids appear anywhere; a maintainer cannot see that finished contributions were left unused. [criterion 53] | deepseek-v4.1-flash | rejected — MINOR; nothing is lost, only the manifest's not_reused list is incomplete after an early stop; named as a known limit in the pull request | — |

## Phase 6 — orchestrator, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-53 | MINOR | SPEC | base | `tests/test_stage2_research_catalog.py` (`test_models_dev_failure_excludes_free_and_keeps_required_slots[timeout]`, `test_catalog_shared_deadline_keeps_asymmetric_failure_rules`, `test_preflight_shared_deadline_has_asymmetric_failure_rules`); `tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome` | These tests bound real elapsed time (for example an 800 ms deadline, a 7.5 s overlap bound, a marker wait) and fail under a loaded machine although the code is correct: measured 2026-10-20, load average 13 to 22, six runner repair attempts and three full `make verify` runs lost one to three of them; each passes alone. Rebuild them to assert order rather than speed: prove overlap by both reads starting before either finishes (recorded start/end markers), give planted delays a wide margin over the deadline (for example 60 s against a short deadline, so only a deadline that never fires can fail), and wait for markers with a generous bound. The behaviour each test refutes must stay refuted. [criteria 19, 41, 42, 53] | orchestrator | fixed — tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules | — |

Stage-2 call, 2026-10-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1636 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +32 -0
> - `scripts/check_research_handoff.py` +2 -4
> - `tests/test_research_handoff.py` +11 -0
> - `tests/test_stage2_research_catalog.py` +26 -23
> - `tests/test_stage2_research_store.py` +26 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1637 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +14 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F-50: tests/test_stage2_research_availability.py::test_consumed_receipt_cannot_delete_a_new_preparation: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - F-51: tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - F-52: tests/test_research_handoff.py::test_unreadable_spec_is_not_measured: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - F-53: tests/test_stage2_research_store.py::test_terminal_markers_already_in_one_pipe_write_are_read_in_order: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> ```

Stage-2 call, 2026-10-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1638 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +7 -0
> - `tests/test_stage2_research_catalog.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-20: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1643 commits, 12 rules.

## Phase 6 — Codex, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-54 | MAJOR | SPEC | base | `scripts/stage2_research_dispatch.py:156–159,196–204` | Required-first ordering is enforced only within each provider queue. Reproduced with the default four permits, eight required Claude slots and 25 required Go slots: the free Go slot launches before required Claude slots 5–8, and dispatch returns exit 0. Free slots must wait until all required slots have been dispatched. The ordering test covers only one provider. [criterion 19] | Codex | fixed — tests/test_stage2_research_dispatch.py::test_free_slot_of_one_provider_waits_for_required_slots_of_another | — |
| F-55 | MAJOR | SPEC | base | `scripts/check_research_handoff.py:781–788` | A complete run whose inventory contains `"items": 42` crashes the handoff gate with `TypeError: argument of type 'int' is not iterable`. Reproduced through `check_change()` using otherwise valid research, answers and spec. Inventory fields lack shape validation before membership checking; malformed evidence must produce not-measured exit 3 instead of a traceback. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_malformed_inventory_items_are_not_measured | — |

Phase 6 verdict: codex 01a1595e-a66f-79b3-b27e-783f31bcef83, 2026-10-20
Reviewer session: codex 01a1595e-a66f-79b3-b27e-783f31bcef83 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-20: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Codex limit nearly used (maintainer 2026-10-20) · leak check clean over 548 files, 1648 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +10 -0
> - `scripts/check_research_handoff.py` +8 -0
> - `scripts/stage2_research_dispatch.py` +8 -0
> - `tests/test_research_handoff.py` +14 -0
> - `tests/test_stage2_research_dispatch.py` +11 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 42 lines of this gate left out …]
> ........................................................................ [ 92%]
> ........................................................................ [ 94%]
> ........................................................................ [ 96%]
> ........................................................................ [ 99%]
> ............................                                             [100%]
> =================================== FAILURES ===================================
> ______ test_free_slot_of_one_provider_waits_for_required_slots_of_another ______
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
>     def test_free_slot_of_one_provider_waits_for_required_slots_of_another():
>         # Criterion 19 (F-54): required-first holds across providers, not only inside one queue.
>         h = Harness()
>         slots = [make_slot(f"c{i}", provider="claude", order=(1, i), script=sleeper(0.3)) for i in range(8)]
>         slots += [make_slot("g-req", order=(1, "a"), script=sleeper(0.01))]
>         slots += [make_slot("g-free", required=False, order=(1, "z"), script=sleeper(0.01))]
> >       result = run(slots, h)
>
> tests/test_stage2_research_dispatch.py:155: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2_research_dispatch.py:99: in run
>     return m.dispatch(slots, gate=kwargs.pop("gate", harness.gate), launcher=harness.launcher, **kwargs)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> slots = [Slot(slot_id='c0', provider='claude', required=True, order=(1, 0), role_allowance=30.0, identity={'run_id': 'run-1', ..."import sys,time\nprint('start',time.time(),flush=True)\ntime.sleep(0.3)\nprint('end',time.time(),flush=True)\n"), ...]
>
>     def dispatch(
>         slots,
>         *,
>         gate: Callable[[Slot], GateVerdict],
>         launcher: Callable[[Slot, float], Any],
>         audit: Callable[[Slot, GateVerdict], None] | None = None,
>         on_terminal: Callable[[Slot, SlotResult], None] | None = None,
>         stop: threading.Event | None = None,
>         deadline: float | None = None,
>         reserve: float = 0.0,
>         clock: Callable[[], float] = time.monotonic,
>         per_provider_limit: int = PER_PROVIDER_LIMIT,
>         grace: float = 2.0,
>     ) -> DispatchResult:
>         """Run one stage. Each slot ends with exactly one terminal outcome.
>     
>         ``on_terminal(slot, result)`` is called once per slot, in the thread that set the outcome and
>         before that thread takes its next slot (launched, cancelled, refused and not-started slots
>         alike). An exception from it, or from ``audit`` carrying a ``stage_stop_reason`` attribute,
>         is a stage stop without a security refusal: queued slots are cancelled, running children
>         are stopped and reaped with their output kept, no further callback runs (the store it
>         writes to is the thing that failed) and the exit code is 1 unless a security refusal makes
>         it 2. The dispatcher knows nothing about what the callbacks write.
>         """
>         stop = stop if stop is not None else threading.Event()
> >       ordered = sorted(slots, key=lambda s: (not s.required, s.order))
> E       TypeError: '<' not supported between instances of 'str' and 'int'
>
> scripts/stage2_research_dispatch.py:156: TypeError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_dispatch.py::test_free_slot_of_one_provider_waits_for_required_slots_of_another
> 1 failed, 3107 passed, 16 skipped in 567.57s (0:09:27)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/check_research_handoff.py:335:43: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 333 |         if not (isinstance(items, list) and all(isinstance(i, dict) for i in items)):
> 334 |             raise CannotMeasure(f"{where}: the inventory record has malformed items")
> 335 |         if "neighbours" in stored and not isinstance(stored["neighbours"], (list, dict)):
>     |                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 336 |             raise CannotMeasure(f"{where}: the inventory record has malformed neighbours")
> 337 |     parsed.derived = research_handoff.derive_inventory(
>     |
>     = help: Convert to `X | Y`
>
> scripts/stage2_research_dispatch.py:211:13: SIM102 Use a single `if` statement instead of nested `if` statements
>     |
> 209 |               if not queue:
> 210 |                   return "done"
> 211 | /             if not queue[0].required:
> 212 | |                 # Required-first holds across providers (F-54): a free slot waits until every
> 213 | |                 # required slot of every provider has been taken from its queue.
> 214 | |                 if any(q and q[0].required for q in queues.values()):
>     | |_____________________________________________________________________^ SIM102
> 215 |                       return "wait"
> 216 |               slot = queue.popleft()
>     |
>     = help: Combine `if` statements using `and`
>
> Found 2 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 15311 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-20: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 548 files, 1668 commits, 12 rules.

## Phase 6 — Codex, 2026-10-20

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-56 | MAJOR | SPEC | base | `scripts/stage2_availability.py:362–369` | A research header containing `neighbours: [plans/changes/other/spec.md]` followed by `neighbours: []` silently discards the given dependency. Reproduced through `given_neighbours()`, which returns an empty list. Conflicting neighbour declarations must refuse before model calls with exit 2. [criterion 4] | Codex | fixed — tests/test_stage2_swarm.py::test_conflicting_neighbour_declarations_refuse_before_calls | — |
| F-57 | MAJOR | MAINT | base | `scripts/stage2_research_dispatch.py:321–328`; `scripts/stage2_research_run.py:1174–1181` | Interrupting an active run with Ctrl-C leaves its model subprocesses running. Reproduced by sending SIGINT during dispatch: the dispatcher exits while its child remains alive. The join has no cancellation cleanup, and the run releases its store lock without stopping active children, allowing a replacement run to overlap surviving calls. | Codex | fixed — tests/test_stage2_research_dispatch.py::test_an_interrupt_stops_and_reaps_active_children_before_it_propagates | — |

Phase 6 verdict: codex 01a15b26-dd6a-7a43-9950-2da19acd0cc8, 2026-10-20
Reviewer session: codex 01a15b26-dd6a-7a43-9950-2da19acd0cc8 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 session, 2026-10-20: attempt 1d3811605ee9 · model opencode-go/deepseek-v4.1-flash · endpoint opencode-go · handover .stage2-sessions/brief-r13.md · leak check clean over 548 files, 1670 commits, 12 rules · dispatch accepted.

Stage-2 session, 2026-10-20: attempt 304e5f9c2d9e · model opencode-go/deepseek-v4.1-flash · endpoint opencode-go · handover .stage2-sessions/brief-r13.md · leak check clean over 548 files, 1670 commits, 12 rules · dispatch accepted.

Stage-2 call, 2026-10-20: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason DeepSeek session did not start (bead coding-harness-bas); maintainer 2026-10-20 switched to Sonnet · leak check clean over 548 files, 1671 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +8 -0
> - `scripts/stage2_availability.py` +8 -0
> - `scripts/stage2_research_dispatch.py` +12 -2
> - `tests/test_stage2_research_dispatch.py` +29 -0
> - `tests/test_stage2_swarm.py` +15 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-21: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 554 files, 1768 commits, 12 rules.

Stage-2 session, 2026-10-21: attempt 598e253fa258 · model opencode-go/deepseek-v4.1-flash · endpoint opencode-go · handover .stage2-sessions/deepseek-review-q18-handover.md · leak check clean over 554 files, 1768 commits, 12 rules · dispatch accepted.

Stage-2 session, 2026-10-21: attempt 191fa0246237 · model opencode-go/deepseek-v4.1-flash · endpoint opencode-go · handover .stage2-sessions/deepseek-review-q18-handover.md · leak check clean over 554 files, 1768 commits, 12 rules · dispatch accepted.

## Phase 6 — Codex, 2026-10-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-58 | MAJOR | SPEC | base | `scripts/stage2.py:4412–4414` | An unterminated front matter block is silently ignored during class selection. Reproduced with research declaring `bounded` and a spec containing `---` followed by `class: architectural` without a closing delimiter: `declared_class()` returns `bounded`, bypassing the swarm and its receipt. A present malformed header must refuse before model calls. [criterion 4] | Codex | fixed — tests/test_stage2_swarm.py::test_unterminated_class_header_refuses_before_calls | yes |
| F-59 | MAJOR | SPEC | base | `scripts/stage2_availability.py:107` | Intelligence-request errors redact only the complete API key. Reproduced with an exception containing a twelve-character prefix of a synthetic key: that prefix survives in the returned status, which preparation prints and persists in its receipt. Every credential fragment of eight or more characters must also be redacted. [criterion 21] | Codex | fixed — tests/test_stage2_research_availability.py::test_intelligence_errors_redact_credential_fragments | yes |
| F-60 | MAJOR | MAINT | base | `scripts/stage2_availability.py:111–117` | A malformed intelligence entry aborts preparation instead of producing “not read.” Reproduced with `{"data":[{"evaluations":"unavailable"}]}`: `read_intelligence()` raises an uncaught `AttributeError`, even when the entry concerns no requested model. Since this runs after seat probes and before receipt publication, an optional benchmark response prevents otherwise successful preparation from producing a usable receipt. [spec amendment, 2026-10-21: any intelligence-reading failure gives “not read”] | Codex | fixed — tests/test_stage2_research_availability.py::test_malformed_intelligence_never_blocks_a_receipt | yes |

Phase 6 verdict: codex 01a15ef4-710e-71f1-9f13-267b5402447f, 2026-10-21
Reviewer session: codex 01a15ef4-710e-71f1-9f13-267b5402447f — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

## Phase 6 — independent reviewer, deepseek-v4.1-flash through a Pi session, 2026-10-21

Requested by the maintainer; launched through `stage2.py session` (attempt 191fa0246237; attempt 598e253fa258 was truncated by the Terminal dispatch, bead coding-harness-rm8, so the captured command ran in the VS Code terminal). Read the delta `328a505..825ae65` only (Q-18 and the exclusion fix). Its file `.stage2-sessions/deepseek-review-q18-findings.md` is copied below unchanged.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| D-3 | MINOR | SPEC | base | `scripts/stage2_availability.py:110-127` | A success response whose entry shape differs from the assumed one stops the whole preparation with a traceback, and its status is reported as unreadable only for the shapes the code anticipated. `read_intelligence` reads the index with `(entry.get("evaluations") or {}).get("artificial_analysis_intelligence_index")` (line 117); when `evaluations` is a list or a string (a truthy non-mapping) — or when the live document nests the score deeper — Python raises `AttributeError`, which is not in the caught `except (OSError, ValueError, KeyError)` (line 106). Reproduction: set `ARTIFICIAL_ANALYSIS_API_KEY`, replace `INTELLIGENCE_FETCH` with a function returning `{"data": [{"slug": "x", "evaluations": [45]}]}`, run `prepare-explore <change>`: every seat has already been probed, then `AttributeError: 'list' object has no attribute 'get'` escapes from line 117, so no report, no receipt and no exit code of the intended scheme is produced (the command dies in the traceback) instead of the reading being marked "not read" with its reason. That refutes the docstring's "it never stops a preparation" and criterion 63's "a missing key or failed request stops the preparation" as a refutation condition. [criterion 63] | deepseek-v4.1-flash | fixed — tests/test_stage2_research_availability.py::test_malformed_intelligence_never_blocks_a_receipt | yes |
| D-4 | MINOR | SPEC | base | `scripts/stage2_availability.py:110`; `scripts/stage2_availability.py:683-704` | A reading that matched no candidate is reported as successfully read, and the unmatched candidates carry no reason, so the cost-alone caveat disappears exactly when it is true. `read_intelligence` sets `reading["status"] = "read"` (line 110) as soon as the response holds a `data` list, without checking that any model matched; an unmatched model keeps `None` in `scores`, and `intelligence_lines` prints `_score_text(scores.get(model))` = "not read" with no cause (line 699) while the recommendation suppresses "; intelligence was not read, so cost alone decides" because the status equals "read" (lines 702-704). Reproduction: with the shipped declaration (`research_swarm.intelligence_slugs: {}`) and a live index whose entries are named like "DeepSeek V4.1 Flash 1017 (max)", `_normal("deepseek-v4.1-flash")` = `deepseekv41flash` matches neither `deepseekv41flash1017` (slug) nor the same normalised name, so `scores["deepseek-v4.1-flash"]` stays `None` although the entry exists; the report prints "Intelligence: Artificial Analysis Intelligence Index, https://artificialanalysis.ai/ - read, <time>", then "opencode-go/deepseek-v4.1-flash: requests 34670, intelligence not read" without the reason, and "Recommendation: the seats above - per trio the cheapest reachable admitted models." — the maintainer is told intelligence was read while nothing was weighed, and a typo in an `intelligence_slugs` entry is indistinguishable from a model the index does not list, both refuting "or 'not read' with the reason". [criterion 63] | deepseek-v4.1-flash | fixed — tests/test_stage2_research_availability.py::test_unmatched_intelligence_has_per_model_reason_and_cost_only_caveat | yes |
| D-5 | MINOR | SPEC | base | `scripts/stage2.py:4465-4488`; `scripts/stage2_availability.py:757-760` | A refused `--seats` answer leaves the previously prepared receipt usable, so the recommendation the maintainer just declined can still start a run. `prepare_explore` builds the argument as `stage2_availability.prepare_research(..., seat_choice(seats))` (line 4488), so `seat_choice` refuses before `prepare_research` runs, and `prepare_research` is the function that deletes an earlier receipt under its own comment "A failed preparation must never leave an earlier receipt usable" (line 759). Reproduction: `prepare-explore demo` prints receipt `R`; the maintainer answers "use glm-5.3-flash and longcat-2.0"; the orchestrator runs `prepare-explore demo --seats repository=glm-5.3-flash` (one model for the repository trio's two Go seats) → `Refused` → exit 2 as criterion 65 asks, but `R` is untouched, its binding is unchanged (`research_binding` covers worktree, configuration digest, class and neighbours, not the choice) and its age is below `max_age_seconds`, so `explore demo --availability-reported R` consumes `R` and starts the run on the recommendation instead of the maintainer's answer, with no further refusal — the maintainer's answer is silently dropped through the exit-2 path. [criteria 44, 45, 65] | deepseek-v4.1-flash | fixed — tests/test_stage2_research_availability.py::test_refused_seat_answer_invalidates_the_previous_receipt | yes |
| D-6 | MAJOR | SPEC | base | `scripts/stage2_swarm.py:333-336`; callers `scripts/stage2_swarm.py:373`, `scripts/stage2_availability.py:557`, `scripts/stage2_availability.py:584`, `scripts/stage2_availability.py:809-811` | An exclusion whose `klasse` names no declared data class is silently ignored, so an unreadable deny rule becomes permission — and for the research swarm's public roles no exclusion of their own class can ever bind. `exclusion_problem` reads `data_class = entry.get("klasse", "framework")` and `continue`s on anything but the literal `framework` (lines 333-336); neither that function nor `research_settings`' malformed check (which calls it with `model = ""` and therefore only validates shape) compares `klasse` against the declared `datenklassen`. Reproduction: `ausgeschlossen: [{was: "dropped", klasse: "Framwork", modelle: ["deepseek-"]}]` → `exclusion_problem(data, "deepseek-v4.1-flash")` returns `None`, `research_settings` reports no problem, so `_go_outcome` admits it (`admitted: True`), it enters the pool, fills an open repository seat as "cheapest", is probed by `probe_go` (its admission check also passes) and is invoked with the private finder brief — a one-letter typo in the class name disables the denial for private content with no warning and no exit 2, which is the failure the shared predicate (O197-1, "an unreadable deny rule cannot silently become permission to send code") exists to prevent. The same branch means an entry written for the research swarm's public class, `klasse: public-web` — a class the declaration itself defines and the only class the online seats and the free researchers carry — never binds in `invocation_problem`, in `_go_outcome` or in the free-selection filter, although the fix states an excluded model is blocked in every role. [criteria 43, 48] | deepseek-v4.1-flash | fixed — tests/test_stage2_research_availability.py::test_exclusion_only_binds_its_declared_research_class | yes |
| D-7 | MINOR | SPEC | base | `scripts/stage2_availability.py:695-699` | A reachable Go candidate outside the substitute pool is reported with "subscription" instead of its declared request cost. `intelligence_lines` builds `cost` only from `state["pool"]` (line 696), and `_admitted_pool` (lines 551-557 of `_Selection`) keeps only models whose catalog record has `tool_support is None`, while `fill`'s preferred pass seats any admitted model. Reproduction: `prepare-explore demo --seats online=<mimo-v2.6-pro>,longcat-2.0,glm-5.3-flash` where `mimo-v2.6-pro` is admitted and reachable but models.dev records no tool support for it (`_go_outcome` gives `admitted: True`, reason "no-tool-support: not in the substitute pool"): the chosen seat is probed and selected, `read_intelligence` scores it, and the report prints "opencode-go/mimo-v2.6-pro: requests subscription, intelligence 46" although `modelle_terms.mimo-v2.6-pro.anfragen_5h: 3250` is declared and is the figure the maintainer needs for the cost-against-intelligence answer — the report lacks a reachable candidate's request cost. [criterion 63] | deepseek-v4.1-flash | fixed — tests/test_stage2_research_availability.py::test_reachable_chosen_go_model_outside_pool_keeps_declared_cost | yes |

Stage-2 call, 2026-10-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 554 files, 1770 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +39 -1
> - `scripts/stage2.py` +6 -1
> - `scripts/stage2_availability.py` +51 -21
> - `scripts/stage2_swarm.py` +4 -3
> - `tests/test_stage2_research_availability.py` +78 -0
> - `tests/test_stage2_swarm.py` +11 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 15 lines of this gate left out …]
> ........................................................................ [ 28%]
> ........................................................................ [ 30%]
> ........................................................................ [ 33%]
> ........................................................................ [ 35%]
> ........................................................................ [ 37%]
> ........................................................................ [ 39%]
> ........................................................................ [ 42%]
> ........................................................................ [ 44%]
> ........................................................................ [ 46%]
> ..........................F............................................. [ 48%]
> ........................................................................ [ 50%]
> ........................................................................ [ 53%]
> ........................................................................ [ 55%]
> ........................................................................ [ 57%]
> ........................................................................ [ 59%]
> ........................................................................ [ 61%]
> ........................................................................ [ 64%]
> ........................................................................ [ 66%]
> ........................................................................ [ 68%]
> ........................................................................ [ 70%]
> ........................................................................ [ 73%]
> ........................................................................ [ 75%]
> ........................................................................ [ 77%]
> ........................................................................ [ 79%]
> ........................................................................ [ 81%]
> ........................................................................ [ 84%]
> ........................................................................ [ 86%]
> ........................................................................ [ 88%]
> ........................................................................ [ 90%]
> ........................................................................ [ 92%]
> ........................................................................ [ 95%]
> ........................................................................ [ 97%]
> ........................................................................ [ 99%]
> .............                                                            [100%]
> =================================== FAILURES ===================================
> _______ test_a_customer_only_exclusion_does_not_deny_framework_admission _______
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-748/popen-gw4...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-748/popen-gw4/test_a_customer_only_exclusion0/state'))
>
>     def test_a_customer_only_exclusion_does_not_deny_framework_admission(world: World) -> None:
>         """O197-2: the exclusion's declared data class must bind as well as its model prefix."""
>         path = world.root / "model-endpoints.yaml"
>         data = yaml.safe_load(path.read_text())
>         data["ausgeschlossen"] = [{"klasse": "kundencode", "modelle": [*TEST_FREE, *TEST_LADDER]}]
>         path.write_text(yaml.safe_dump(data))
> >       assert stage2.free_admission_problem(world.root, TEST_FREE[0], list(TEST_FREE)) is None
> E       AssertionError: assert 'the model acme-v1-free is excluded by model-endpoints.yaml: excluded by the maintainer' is None
> E        +  where 'the model acme-v1-free is excluded by model-endpoints.yaml: excluded by the maintainer' = <function free_admission_problem at 0x10afaaf20>(PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-748/popen-gw4/test_a_customer_only_exclusion0/repo'), 'acme-v1-free', ['acme-v1-free', 'beacon-2-free'])
> E        +    where <function free_admission_problem at 0x10afaaf20> = stage2.free_admission_problem
> E        +    and   PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-748/popen-gw4/test_a_customer_only_exclusion0/repo') = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-748/popen-gw4...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-748/popen-gw4/test_a_customer_only_exclusion0/state')).root
> E        +    and   ['acme-v1-free', 'beacon-2-free'] = list(('acme-v1-free', 'beacon-2-free'))
>
> tests/test_stage2.py:11194: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_customer_only_exclusion_does_not_deny_framework_admission
> 1 failed, 3236 passed, 16 skipped in 488.72s (0:08:08)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 15564 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-21: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 554 files, 1770 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +24 -1
> - `tests/test_stage2.py` +7 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F-58: tests/test_stage2_swarm.py::test_unterminated_class_header_refuses_before_calls: the call of `tests/test_stage2_swarm.py::test_unterminated_class_header_refuses_before_calls[-spec.md]` failed with Failed, not an AssertionError
> - F-60: tests/test_stage2_research_availability.py::test_malformed_intelligence_never_blocks_a_receipt: the call of `tests/test_stage2_research_availability.py::test_malformed_intelligence_never_blocks_a_receipt[entry0]` failed with AttributeError, not an AssertionError
> - D-3: tests/test_stage2_research_availability.py::test_malformed_intelligence_never_blocks_a_receipt: the call of `tests/test_stage2_research_availability.py::test_malformed_intelligence_never_blocks_a_receipt[entry0]` failed with AttributeError, not an AssertionError
> - D-5: tests/test_stage2_research_availability.py::test_refused_seat_answer_invalidates_the_previous_receipt: the call of `tests/test_stage2_research_availability.py::test_refused_seat_answer_invalidates_the_previous_receipt[args0]` failed with Failed, not an AssertionError
> ```

Stage-2 call, 2026-10-21: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 554 files, 1770 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +13 -0
> - `tests/test_stage2_research_availability.py` +14 -3
> - `tests/test_stage2_swarm.py` +8 -2
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [ruff-check] $ lauf_cmd
> tests/test_stage2_research_availability.py:1088:5: SIM105 Use `contextlib.suppress(stage2.Refused)` instead of `try`-`except`-`pass`
>      |
> 1086 |       assert len(fx.w.calls()) == before
> 1087 |       consumed = None
> 1088 | /     try:
> 1089 | |         consumed = availability.consume_research(fx.w.root, "demo", receipt["report_id"], stage2, "feature")
> 1090 | |     except stage2.Refused:
> 1091 | |         pass
>      | |____________^ SIM105
> 1092 |       assert consumed is None, "the receipt of the declined recommendation is still usable"
>      |
>      = help: Replace with `contextlib.suppress(stage2.Refused)`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 15621 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Orchestrator, 2026-10-21: the night run adopted the uncommitted round-14 repair
from the three failed runner attempts and booked it as a hand repair. Fixed the
SIM105 lint finding and restored the original customer-only exclusion test.
The maintainer's D-6 correction is class-scoped: malformed classes refuse in
all admission paths, public-web exclusions bind online seats and free
researchers, and customer-only exclusions do not deny framework admission.
Selection, tool-free probe admission and invocation all retain that class.
Global-exclusion fixtures now explicitly declare both research classes.

Red first: on pre-repair commit `febe2aa`, current proving tests gave 19 failed,
6 passed (2026-10-21), with an assertion failure proving each of F-58–F-60 and
D-3–D-7. Before the class-scoping repair, five additional regression cases
failed against the inherited working tree. The focused repaired set passed
53 cases. Final full `make verify`: GREEN, 3243 passed, 16 skipped; all local
blocking gates passed, including the kit probe. Evidence logs are temporary
local files, not committed: `/private/tmp/research-swarm-round14-baseline-red.log`
and `/private/tmp/research-swarm-round14-verify.log`. No live benchmark or
research invocation was made. Reviewer findings remain unchanged; only their
Status and empirical test-proof cells are booked above.

Stage-2 call, 2026-10-21: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 554 files, 1776 commits, 12 rules.

## Phase 6 — Codex, 2026-10-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-61 | MAJOR | SPEC | base | `scripts/check_research_handoff.py:500–517` | An empty answer containing only a placeholder comment counts as a maintainer answer. In-memory reproduction with complete research, linked obligations, `status: answered`, `answered_by: maintainer` and `answer: # answer pending` returns exit 0: the obligation closes and the record supplies a criterion Basis. `answer: null` also passes. Missing answer content must leave the obligation open and cannot support a criterion. [criteria 32, 34] | Codex | fixed — tests/test_research_handoff.py::test_empty_yaml_answer_cannot_close_item_or_supply_basis, tests/test_research_handoff.py::test_real_inline_and_block_answers_still_close_handoff | yes |
| F-62 | MAJOR | SPEC | base | `scripts/stage2_availability.py:302–305,872–892` | An unsuccessful preparation loses every probe audit record. Reproduced with stand-in probes: two models succeed, two fail, and seats remain unfilled; four audit entries exist only in memory, while preparation raises `seat-unavailable` before its only persistence call. The report does not print those entries either. Probe audit records must survive a failed preparation outside the worktree, independently of whether a usable selection receipt is issued. [criteria 47, 48] | Codex | fixed — tests/test_stage2_research_availability.py::test_probe_audits_survive_unsuccessful_preparation, tests/test_stage2_research_availability.py::test_persisted_probe_audit_scrubs_credentials_before_write, tests/test_stage2_research_availability.py::test_unwritable_probe_audit_refuses_before_launch | yes |

Phase 6 verdict: codex 01a15f59-825a-7133-a432-f26b2170bb6e, 2026-10-21
Reviewer session: codex 01a15f59-825a-7133-a432-f26b2170bb6e — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 554 files, 1778 commits, 12 rules.


Orchestrator checkpoint, 2026-10-21: the first round-15 repair call ended
before post-run verification with exit 1. Its only reported stderr was
`Reading additional input from stdin...`; a budget cause is not established.
The runner saved the attempt at
`refs/stage2/attempts/research-swarm/repair-attempt-1-20261021T165418072449Z`
(commit `82f2d20f3e94`) and restored source, tests and plan to `80b2998`.
The candidate code and regression tests are retained for inspection, not
qualified: no red-first or full-verify result was produced for them. F-61
and F-62 remain taken and unresolved. No second repair or round 16 started.

Resume by inspecting the saved diff and adopting only its two source files,
two test files and plan ledger if sound; preserve these findings and their
unresolved statuses. Verify the new regression tests against baseline and
fixed code before booking either row fixed. The last qualified source stays
`ad2ff14` (3243 passed, 16 skipped). The maintainer requested a handover at
this safe checkpoint; PR #211 carries the resumption instructions.

Stage-2 call, 2026-10-21: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 556 files, 1790 commits, 12 rules.

## Phase 6 — Codex, 2026-10-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-63 | MAJOR | SPEC | fix-r15 | `scripts/check_research_handoff.py:510–526` | Empty YAML containers still count as maintainer answers after the answer-validation repair. In-memory reproduction with complete research, linked obligations, `status: answered`, `answered_by: maintainer` and either `answer: []` or `answer: {}` returns exit 0, closing the obligation and accepting the record as a criterion Basis. `str(content)` converts these empty values into nonempty punctuation. Empty answer containers must leave obligations open and cannot supply a Basis. [criteria 32, 34] | Codex | fixed — tests/test_research_handoff.py::test_empty_yaml_containers_cannot_close_item_or_supply_basis | yes |

Phase 6 verdict: codex 01a16053-cfb6-7fb1-8e27-b5edf2aa5348, 2026-10-21
Reviewer session: codex 01a16053-cfb6-7fb1-8e27-b5edf2aa5348 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 556 files, 1792 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +18 -0
> - `scripts/check_research_handoff.py` +2 -0
> - `tests/test_research_handoff.py` +13 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-21: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 556 files, 1793 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +18 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-21: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 556 files, 1793 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-swarm/plan.md` +9 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-22: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 556 files, 1798 commits, 12 rules.

## Phase 6 — Codex, 2026-10-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-64 | MAJOR | SPEC | fix-r15 | `scripts/check_research_handoff.py:503–511` | A maintainer answer containing duplicate YAML keys silently closes research obligations. Reproduced in memory with `answer:` containing two indented `choice:` keys, first `keep`, then `drop`, plus answered status, maintainer attribution and context: `check_change()` returns no findings, closes the linked item and accepts the record as a criterion Basis. The duplicate-key loader raises an error, but the historical-prose fallback suppresses it and treats the ambiguous answer as nonempty text. Duplicate answer keys must produce not-measured exit 3. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_duplicate_yaml_answer_keys_are_not_measured | — |

Phase 6 verdict: codex 01a16083-fd73-7db1-ba5e-3a505f9c7e87, 2026-10-22
Reviewer session: codex 01a16083-fd73-7db1-ba5e-3a505f9c7e87 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-22: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 556 files, 1802 commits, 12 rules.

Stage-2 call, 2026-10-22: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 556 files, 1803 commits, 12 rules.

## Phase 6 — Codex, 2026-10-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-65 | MAJOR | SPEC | fix-r17 | `scripts/check_research_handoff.py:116–127,503–514` | New evidence after the duplicate-answer-key repair (F-64): an answer containing `<<: {source: maintainer}` followed by duplicate `choice: keep` and `choice: drop` keys still closes research obligations and supplies a criterion Basis. Reproduced through `check_change()` with no findings. Constructing the merge key raises a generic YAML error before duplicate detection; the historical-prose fallback suppresses it. Duplicate answer keys must report not measured with exit 3. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_yaml_answer_errors_are_not_measured |  |

Phase 6 verdict: codex 01a160ad-c28c-7591-b2e9-9fe376556d65, 2026-10-22
Reviewer session: codex 01a160ad-c28c-7591-b2e9-9fe376556d65 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Loop restarted: 2026-10-22 after round 2 — Maintainer, 2026-10-22: fresh swarm run on PR #158 after phase-6 rounds 3-18 changed the code since the clean loop of 2026-10-15 (Q-17).

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 557 files, 1832 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 557 files, 1832 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 557 files, 1832 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 557 files, 1832 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 557 files, 1832 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 557 files, 1832 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: review-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 557 files, 1837 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: review-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 557 files, 1838 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: review-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 567 files, 1852 commits, 12 rules.

Stage-2 call, 2026-10-22: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 567 files, 1857 commits, 12 rules.

Stage-2 call, 2026-10-23: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 567 files, 1901 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 567 files, 1911 commits, 12 rules.

Stage-2 call, 2026-10-23: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 567 files, 1911 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model hy3 · leak check clean over 567 files, 1912 commits, 12 rules.

Stage-2 call, 2026-10-23: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 567 files, 1912 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 567 files, 1913 commits, 12 rules.

## Phase 6 — deep reviews RS-1, RS-2 and RS-3, 2026-10-25

Three read-only deep reviews of `explore/research-swarm` at 8480b1d (part 1 orchestration and judge, part 2 persistence and records, part 3 Pi seats, catalog and path lock) reproduced each finding below in a scratch copy; the repairs were written test-first on this branch by an orchestrated Claude Code session. Pi 1.2.0 ran under Node 22 in the scratch copies, not the declared Node 26.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| RS-3-2 | BLOCKER | SPEC | base | `scripts/stage2_repository_pathlock.mjs` `confinementError` | The repository seats' path lock resolved a `file://` URL as a relative name inside the worktree and allowed it, while Pi's `normalizePath` turns it into the real path with `fileURLToPath`: `read file:///<outside>/secret.txt`, `ls file:///etc` and `find path=file:///root` reached files anywhere on the machine and their text reached a Go model. Reproduced on the pinned Pi 1.2.0 through the real `Run.pi_command`. Repair: the lock mirrors Pi's normalisation (unicode spaces, `@`, `~` refused, `file://` through `fileURLToPath`) before it confines; re-checked on the pinned Pi under Node 22, the secret no longer reaches the model. [criterion 52, Q-16] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_repository_pathlock.py::test_a_file_url_is_judged_where_pi_reads_it, tests/test_stage2_repository_pathlock.py::test_an_unreadable_file_url_is_refused | — |
| RS-3-6 | MINOR | SPEC | base | `scripts/stage2_repository_pathlock.mjs` `confinementError` against Pi `resolveReadPathAsync` | The lock judged the literal path, but Pi's `read` falls back to curly-quote, NFD and AM/PM variants of a missing path: with a symlink `notes’` (U+2019) in the worktree pointing outside, `notes'/secret.txt` passed the lock and Pi read the outside file. Repair: for `read`, every fallback name Pi tries that exists must also stay inside the worktree. [criterion 52] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_repository_pathlock.py::test_reads_through_pi_fallback_names_are_judged_too | — |
| RS-1-2 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py` `parse_text` | The gate split `research.md` with `str.splitlines()`, which breaks at U+2028, U+2029 and U+0085 that the runner's `json.dumps(ensure_ascii=False)` keeps raw inside JSON strings; a complete run whose receipt excerpt or claim text carried one became not measured (exit 3), and CI runs the gate over every change. Repair: the gate breaks lines only at LF, CRLF and CR (`_lines`), also for `decisions.md` and `spec.md`. [criteria 31-33] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_research_handoff.py::test_unicode_line_separators_inside_records_stay_measured | — |
| RS-1-9 | MAJOR | SPEC | base | `scripts/check_research_handoff.py` `parse_text` | Markdown fence state carried across run envelopes: earlier research ending in an unclosed `~~~` or four-backtick fence swallowed every later v2 envelope ("exempt - legacy", exit 0, with an open [DECISION] obligation), and an unclosed ```` ```python ```` fence turned it into exit 3. Repair: a run envelope's opening and closing lines are hard boundaries that end a foreign fence. [criteria 31-33] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_research_handoff.py::test_run_envelope_markers_end_a_foreign_fence | — |
| RS-1-3 | MINOR | SPEC | base | `scripts/check_research_handoff.py` `_basis_lines` | After "Acceptance criteria" the scan treated any numbered line under any later heading as a criterion, so a rollout list or numbered open decisions repeated a criterion number (exit 3) or became a criterion without a Basis (exit 1); `plans/changes/criterion-test-ledger/spec.md` has one under "Open decisions". Repair: under an "Acceptance criteria" or "Amendment" heading and its subsections every numbered item counts; under any other later section only an item that reads as a criterion (When, While, If, Where, perhaps bold) counts, so F-25's later-section protection holds. [criterion 34] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_research_handoff.py::test_numbered_lists_in_later_sections_are_not_criteria | — |
| RS-1-1 | MAJOR | SPEC | base | `scripts/stage2_research_run.py` `Run.publish` | When the store's clearing failed after the binding write, the record was recomposed with an incomplete status but the stored binding kept the tail of the text composed before, so the next run found "binding changed: research.md" and repeated all 39 calls. Repair: after recomposing, the binding is written again with the tail actually appended (a store that refuses that write too leaves it to the next run). [criterion 53] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_failed_clear_binds_the_bytes_actually_appended | — |
| RS-1-8 | MAJOR | SPEC | base | `scripts/stage2.py` `append` | Publication rewrote `research.md` from text read with universal newlines, so CRLF and lone CR bytes of earlier research became LF (criterion 17) and the stored binding of an incomplete run no longer matched, discarding its 38 finished results. Repair: `append` builds the new content from the file's bytes. [criteria 17, 53] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_publication_keeps_earlier_research_bytes_and_their_resume | — |
| RS-2-6 | MAJOR | SPEC | base | `scripts/stage2.py` `append`, `stamp_updated`; `scripts/check_frontmatter_current.py` `stamp` | Publication truncated and rewrote `research.md`, then stamped it in a second rewrite; a SIGKILL mid-write left 2 MB of a 100 MB file, losing uncommitted human research and earlier run records. Repair: the appended and stamped bytes (`check_frontmatter_current.stamped`, the pure half of `stamp`) go to a temporary file in the same directory, fsync, `os.replace`, directory fsync, mode kept (`stage2.write_atomic`). `tests/test_stage2_session.py::test_a_stamp_failure_after_the_update_is_reported` counted `stamp_updated` calls including the one `append` made; its threshold now targets the session's own re-stamp. [criterion 17] | deep review 2 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_append_replaces_research_in_one_atomic_step | yes |
| RS-1-10 | MINOR | SPEC | base | `scripts/stage2.py` `explore`; `scripts/check_research_handoff.py` | The gate trusts every well-formed run envelope in `research.md`, and `explore` appended the single explorer's answer raw, so a forged envelope in a model answer counted as a complete run whose claim satisfied a criterion Basis. Repair: `quote_research_records` makes run markers and record fences in that answer inert before the append; with RS-1-9's hard boundaries, only the runner's own envelopes parse. Binding envelopes to a runner-held record of published runs stays open (not needed for the two known routes). [criteria 17, 31-34] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_forged_run_envelope_in_an_explorer_answer_is_quoted, tests/test_stage2_research_deep_review.py::test_quoting_leaves_ordinary_prose_alone | — |
| RS-1-5 | MAJOR | SPEC | base | `scripts/stage2_research_run.py` `Run.claude_command`, `Run.validate_judge` | Every Opus packet, the judge's included (reports and online receipt excerpts, i.e. web text), went into `--append-system-prompt-file`, so a page could steer `supported` dispositions and drop disagreements; and a judge could mark claims unresolved with `disagreements: []`, leaving no handoff item. Repair: the merge, sentence and judge roles get only their instruction file as system prompt; the data reaches the user turn from a scratch file on stdin (Claude Code joins the prompt argument and piped stdin into one user message; checked in the 2.1.310 binary, not with a live model); the judge must list every unresolved claim in a disagreement, stated to it as a runner rule below `judge.md` and enforced by `validate_judge`. [criteria 14, 15, 31] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_web_text_reaches_the_judge_as_data_never_as_system_prompt, tests/test_stage2_research_deep_review.py::test_an_unresolved_claim_outside_every_disagreement_fails_the_judge | — |
| RS-1-4 | MAJOR | SPEC | base | `scripts/research_capture.py` `evaluate` | A home canary that reached the repository seat's model was graded OBSERVED, and the overall verdict counted only FAIL, so the pre-merge capture could not detect a regression of the F-24 path-lock repair. Repair: a home hit is a `repository-seat` FAIL; the capture instructions in `plan.md` say so. [criterion 52] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_research_capture.py::test_a_home_canary_read_by_the_repository_seat_fails_the_capture | — |
| RS-1-6 | MAJOR | SPEC | base | `scripts/stage2_research_judge.py` `build_research_judge_packet`; `scripts/stage2_research_run.py` `Run.stage_topics` | Each report went into the judge packet twice (fields plus a `raw` copy) as indented JSON; realistic reports (5 claims) exceeded the 200,000-character limit only at the judge, after 38 + 3N calls, with no warning. Repair: no `raw` copy and compact JSON; before the first topic call the runner records the allowance per planned report and warns on stderr when it is below one full-excerpt claim (5,000 characters). The conversion estimate itself is unchanged. [criteria 14, 18, 19] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_the_judge_packet_carries_no_raw_copy_and_compact_json, tests/test_stage2_research_deep_review.py::test_a_tight_judge_limit_is_announced_before_any_topic_call | — |
| RS-3-1 | MAJOR | SPEC | base | `scripts/stage2_availability.py` `install_measured_models`, `probe_go`; `scripts/stage2_research_run.py` `Run.pi_command`, `Run.on_terminal` | Every catalog row went into each launch's `models.json`; Pi validates the whole file, so one row Pi's schema refuses (`contextWindow: 0`, `input: "text"`, a numeric id) made every selected free model "not found" (custom id at Pi's default endpoint) and seat models fall back to Pi's shipped `anthropic-messages` definition. Repair: a research launch or probe writes only its own model's row, checked against Pi 1.2.0's ModelDefinitionSchema first (`OverlayError` fails the launch closed); a Pi answer whose stderr says it did not use its models.json or model fails the slot or probe. Re-checked on the pinned Pi under Node 22: the stand-in receives the requests despite a bad unrelated row. The review loop's own `activate_overlay` path is left to the main-based review-loop repair. [criteria 38, 61] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_launch_writes_only_its_own_allow_listed_row, tests/test_stage2_research_deep_review.py::test_a_row_pi_would_refuse_fails_the_launch_closed, tests/test_stage2_research_deep_review.py::test_a_pi_answer_without_its_measured_model_is_a_failed_slot | — |
| RS-3-3 | MAJOR | SPEC | base | `scripts/stage2_availability.py` `install_measured_models` | A seat row's unchecked `samplingParams` (`{"model": "kimi-k3"}`) and `headers` reached the provider request: Pi merged the first into the body, which then named an excluded model while `--model` and the audit said minimax-m3. Repair: only `id`, `name`, `api`, `baseUrl`, `reasoning`, `input`, `contextWindow`, `maxTokens` and `cost` are written; dropped fields are named in the run's audit (`models.json for <model>: dropped catalog field(s) …`) and the probe audit. Re-checked on the pinned Pi: the body names minimax-m3 and no forged header is sent. [criterion 11] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_launch_writes_only_its_own_allow_listed_row | — |
| RS-3-7 | MINOR | SPEC | base | `scripts/stage2_swarm.py` `pi_reason` against `scripts/stage2_availability.py` `install_measured_models` | The selection admits a row without `baseUrl` as `https://opencode.ai/zen/go/v1`, but Pi fills a shipped model's row from its shipped definition (`.../zen/go`), so the call went to a path nobody checked. Repair: the written row carries the checked default when it has none. [criterion 38] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_launch_writes_only_its_own_allow_listed_row | — |
| RS-3-8 | MINOR | MAINT | base | `scripts/stage2.py` `activate_overlay` | A non-string header value in a catalog row raised `AttributeError` during a probe or launch. Repair for research launches and probes: headers never reach their `models.json` (RS-3-3), so the crash path is gone there; `activate_overlay` itself, used by the review loop, is left to the main-based review-loop repair (allow-list there). [criterion 38] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_launch_writes_only_its_own_allow_listed_row | — |
| RS-3-4 | MAJOR | SPEC | base | `scripts/stage2_research_run.py` `Run.pi_command` | Research seats ran Pi without `--offline` (probes and the review loop pass it): Pi's `grep` and `find` download the latest, unpinned `rg` or `fd` release into the scratch agent directory when it is missing from PATH and run it inside a process holding `OPENCODE_API_KEY`. Repair: every research Pi launch passes `--offline`. Re-checked on the pinned Pi with `fd` absent: no download, no `agent/bin`. [criteria 9, 52] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_every_research_pi_launch_is_offline | — |
| RS-1-7 | MINOR | SPEC | base | `scripts/stage2_research_run.py` `Run.validate_judge` | The named gap "no neighbour given or found" of an empty topic-5 packet was left to the judge's prose; a reconciliation without it was accepted. Repair: the runner adds the gap to `gaps` when the packet holds no neighbour and the judge did not name it. [criterion 7, S-45] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_an_empty_neighbour_packet_always_names_its_gap, tests/test_stage2_research_deep_review.py::test_a_neighbour_packet_gets_no_invented_gap | — |
| RS-1-11 | MINOR | SPEC | base | `scripts/stage2_research_run.py` `public_sentence_problems`, `Run.stage_sentence` | The filter checked the NFC text but the sentence sent online was not normalised (a decomposed U+0301, a class the allow-list refuses, travelled on), and confusable spellings (`rеsearch-swarm` with a Cyrillic е, fullwidth letters) passed the deny list. Repair: the sentence sent is exactly the checked NFC text; a word mixing letters of different scripts is refused (Chinese, Japanese and Korean scripts count as one); the deny list compares NFKC-casefolded words. [criterion 23] | deep review 1 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_lookalike_repository_names_are_refused, tests/test_stage2_research_deep_review.py::test_one_script_words_stay_accepted, tests/test_stage2_research_deep_review.py::test_the_sentence_sent_online_is_the_checked_nfc_text | — |
| RS-1-NIT | NIT | MAINT | base | `scripts/stage2_research_run.py` `Run.compose` | The branch "Judge answer (failed validation — partial evidence)" never ran: `judge_text` was set only after a successful validation. Repair: branch and field removed; a judge answer that fails validation stays in the record as a `partial` block (outcome `invalid-report`), as before. [criterion 18] | deep review 1 (Claude Opus 5.5) | fixed — not a test — dead code removed; tests/test_stage2_swarm.py covers the invalid judge answer's partial block | — |
| RS-2-1 | MINOR | SPEC | base | `scripts/stage2.py` `release` | `release-loop` deleted the whole record directory, the research state store inside it: an interrupted run's results and its `.lock` went, and while a run still held the old lock a second run took a fresh one (criterion 58). Repair: `remove_loop_record` deletes the loop's files and keeps `research/` and every `research-*` file (preparation receipt and probe audits); the directory goes only when empty. The review-loop repair on main (release idempotence) touches the same function; the merge of main reconciles. [criteria 53, 58] | deep review 2 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_releasing_the_loop_keeps_the_research_store_and_its_lock | — |
| RS-2-2 | MINOR | SPEC | base | `scripts/stage2_research_snapshot.py` `_read` | Any committed symlink (`CLAUDE.md -> AGENTS.md`, ELOOP) or submodule ("not a regular file") made the freeze fail, so research could never run in such a repository. Repair: a symlink git tracks as one (mode 120000) is frozen as its target text without following it; a gitlink (mode 160000) as the commit the index records; any other link or directory is refused as before (`test_snapshot_never_follows_file_or_parent_symlink` unchanged). [criterion 16] | deep review 2 (Claude Opus 5.5) | fixed — tests/test_stage2_research_snapshot.py::test_committed_symlinks_and_submodules_freeze_without_being_followed | — |
| RS-2-3 | MINOR | SPEC | base | `scripts/stage2_research_run.py` `Run.open` | In a linked worktree the placement guard got only `.git/worktrees/<w>`, so a state store under the common git directory or under the main checkout (which holds `.claude/worktrees/<w>`) was accepted. Repair: `git_boundaries` adds the common git directory and, when it is a `.git` directory, the main checkout. [criterion 52] | deep review 2 (Claude Opus 5.5) | fixed — tests/test_stage2_research_deep_review.py::test_a_store_in_the_common_git_dir_or_main_checkout_is_refused | — |
| RS-2-4 | MINOR | SPEC | base | `scripts/stage2_research_store.py` `Store.resume_source`, `plan_reuse` | Only the latest stored run is a source, so after an aborted run B an older run A's matching result was neither reused nor named, against the design ("results that do not match stay stored, because a reverted edit may match again, and are named at each run start") and criterion 53; an unusable source named no individual result either. Repair (design kept true): older runs' results are named "not the latest run" and an unusable source's results "source run unusable"; the latest-run-only rule stays. `test_only_the_latest_stored_run_is_a_source` now asserts the naming. [criterion 53] | deep review 2 (Claude Opus 5.5) | fixed — tests/test_stage2_research_store.py::test_only_the_latest_stored_run_is_a_source, tests/test_stage2_research_store.py::test_an_unusable_source_names_each_of_its_stored_results | — |
| RS-2-5 | NIT | SPEC | base | `scripts/stage2_research_store.py` `Store.adopt` | After A -> B -> C reuse, C's record named B as its source while carrying A's start and end, so the run that made the call was lost. Repair: `reused_from` keeps naming the immediate source, and a new `launched_in` (stored record and manifest slot) names the run that launched the call through every later reuse. [criterion 55] | deep review 2 (Claude Opus 5.5) | fixed — tests/test_stage2_research_store.py::test_a_reused_result_keeps_the_run_that_launched_it | — |
| RS-3-5 | MINOR | SPEC | base | `scripts/stage2_swarm.py` `select_research_catalog` | Duplicate detection searched every nested object: one repeated key inside an unrelated entry (`"cost": {"input": 1, "input": 2}`) or `tool_call` twice in one free entry made the whole models.dev source `duplicate-id` (N=0), and the same in a Pi row ended the preflight with exit 1, against S-33/S-44/S-50. Repair: document-level are only a repeated model key, a repeated `id` key in an entry and equal ids (`_identity_doubt`); any other repeated key makes that entry `metadata-malformed` or `pi-malformed`. Deviation: the existing test `test_preflight_raw_duplicate_keys_inside_models_are_document_ambiguity` expected the whole-source verdict for a repeated `tool_call` too; its `[id]` case keeps that verdict as `test_preflight_raw_duplicate_id_key_inside_models_is_document_ambiguity`, and the `tool_call` case moved to the new test, which excludes only that candidate. Run with the real Pi in a scratch copy (100 passed); the worktree has no Pi install. [criteria 41, 42] | deep review 3 (Claude Opus 5.5) | fixed — tests/test_stage2_research_catalog.py::test_other_repeated_keys_inside_one_entry_exclude_only_that_candidate, tests/test_stage2_research_catalog.py::test_a_repeated_nested_key_in_a_pi_row_excludes_only_that_row | yes |
| RS-3-NIT | NIT | SPEC | base | `scripts/stage2_research_run.py` `Run.pi_command`, `Run.gate` | Pi's own system prompt, sent to every Go model, carries absolute local paths (`<docs>`: the runner's `tools/pi/node_modules` path with home directory and worktree name; `<cwd>`: the scratch path), and the leak check sees only the slot prompt. Open: not cheap here (it needs Pi installed at a neutral path, or rendering Pi's prompt template for the leak check). Recommendation: install the pinned Pi at a neutral, user-independent path for research launches, then add a capture check that no home or worktree path reaches an online model. [criteria 8, 9] | deep review 3 (Claude Opus 5.5) | rejected — moved to its own bead coding-harness-xul8: not cheap inside this change (needs Pi at a neutral path and a capture check) (orchestrator, 2026-10-26) | — |

Bead coding-harness-jik (load-sensitive timing tests), 2026-10-25: the store's SIGKILL test already waits on a file gate and reads its markers from the raw descriptor (F-53) and took 0.29 s under load 29 (deep review 2). The catalog deadline tests no longer bet on wall-clock time: the test driver holds the slow source until teardown and runs the bridge's own deadline-timer callback once every held request has reached the server and the answering sources' bodies were read (`held_collect`, controlled deadline in `collect`), so the real abort path runs at a defined moment; the driver also asserts the bridge arms exactly one timer of `deadlineMs`. One real-timer case stays (both sources slow past a 10 s deadline in `test_catalog_shared_deadline_keeps_asymmetric_failure_rules`). Measured in the scratch copy with the real Pi: the three event-driven tests take about 0.6 s each instead of 10 to 21 s.

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 659 files, 2240 commits, 12 rules.

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 659 files, 2243 commits, 12 rules.

## Review loop ended without a clean round, 2026-10-26

The review loop (phase 4b) ran seven rounds (2026-10-22 to 2026-10-23) and
every taken row of round 7 is repaired (f127daf1, 128424b7). It cannot end
with a clean round: the change diff is 31,720 lines, each round reads the
first 2,000, and a clean answer over a cut diff does not end the loop. Even
split into parts, the change is above the bound of four parts the maintainer
set on 2026-10-26 (bead coding-harness-ut8q).

The maintainer decided on 2026-10-26, in the conversation, as a one-time
exception and not as a rule: finish round 7, release the loop without a
clean round with this note, and run a fresh phase-6 Codex review over the
whole change. The whole branch was read by the three deep reviews of
2026-10-25 (RS-1, RS-2 and RS-3 above); their repairs had no Codex re-check
until this phase 6.

Stage-2 call, 2026-10-26: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 664 files, 2246 commits, 12 rules.

## Phase 6 — Codex, 2026-10-26

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-66 | MAJOR | SPEC | base | `scripts/stage2_research_refs.py:176–209` | A literal U+2028 inside a Python string before `def target():` shifts the evidence excerpt: reproduced with `banner = "first<U+2028>second"` followed by a function returning 42, the resolver reports `supported=True` but returns the string’s tail and function declaration, omitting `return 42`. `str.splitlines()` counts Unicode separators that Python’s AST does not count as source lines. Valid evidence must contain the cited node’s actual lines. [criterion 16] | Codex | fixed — tests/test_stage2_research_refs.py::test_a_unicode_line_separator_in_a_string_keeps_the_cited_node_lines | — |
| F-67 | MAJOR | SPEC | base | `scripts/stage2_swarm.py:614–624` | A raw U+2028 inside a receipt JSON line splits the line and drops the event: Pi writes receipts with Node's `JSON.stringify`, which leaves U+2028 unescaped, and `parse_receipts` iterates `text.splitlines()`, which treats U+2028 as a line break; both halves fail `json.loads` and are skipped. Reproduced 2026-10-26: a line `{"type": "tool", "text": "first<U+2028>second"}` followed by `{"type": "end"}` parses to `["end"]` instead of `["tool", "end"]`. Receipts are JSON Lines: split on `\n` only. The other `splitlines()` calls on foreign text were read: the SSE read in `scripts/research_capture.py` is the test stand-in's own fixture input; git hashes and stderr tails carry no separator that matters. Found by the orchestrator's sweep of the F-66 class. | orchestrator | fixed — tests/test_stage2_swarm.py::test_a_unicode_line_separator_inside_a_receipt_keeps_the_receipt | — |

Phase 6 verdict: codex 01a178b2-cc69-7302-8e00-8daccaedf552, 2026-10-26
Reviewer session: codex 01a178b2-cc69-7302-8e00-8daccaedf552 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

## Phase 4b — loop rows, released 2026-10-26

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L4-1 | MAJOR | SPEC | change | `scripts/stage2_availability.py`: `probe_free_research` (713-760), `FREE_PROBE_SECONDS`/`FREE_PROBE_RETRY_SECONDS` (58-59), call in `prepare_research` (916); `spec.md` criterion 48 and its preparation DETAIL; `design.md` preparation step 3; `plan.md` criterion-48 row; `tests/test_stage2_swarm.py:2406`, `tests/test_stage2_research_availability.py:1218` | Preparation probes every selected Go free model with the real online-topic request and retries a timeout at 120 s then 360 s; a failed probe removes that model from the frozen free selection and from N. The spec, design and plan state the opposite: free models are never probed, a failing free seat stays a named best-effort outcome of the run, and preparation costs at most 60 s per probed model. The tests assert the probing, so implementation and spec must be reconciled. | deepseek-v4.1-flash | fixed — not a test — spec, design and plan now describe real-size free-model probes, timeout retry and removal of failed candidates from frozen N. | no — not a test | disagree — Criterion 48, design and plan now specify real-size free probes with 120-second and 360-second timeout allowances. |
| L4-2 | MAJOR | SPEC | change | `scripts/check_research_handoff.py`: `_basis_lines` (663) and `_bases` (888); `plans/changes/research-swarm/spec.md` criterion 34 and the `## Amendment — 2026-10-21` section holding criteria 62-65 | The gate clears its "inside acceptance criteria" flag at every level-1 or level-2 heading, so criteria added after a second section heading are never checked. This change's own spec appends criteria 62-65 under `## Amendment — 2026-10-21`; a spec that does the same can omit their `*Basis:*` and still exit 0, although criterion 34 and the gate's docstring promise a Basis for every acceptance criterion. The level-3 variant was fixed already; a level-2 heading still yields an empty-set success. | deepseek-v4.1-flash | fixed — tests/test_research_handoff.py::test_amended_criteria_after_main_headings_require_basis | yes — tests/test_research_handoff.py::test_amended_criteria_after_main_headings_require_basis | disagree — The current scanner recognises amendment sections and continues checking criteria after later headings. |
| L4-3 | MINOR | MAINT | change | `scripts/stage2.py` module docstring (`--help` description, lines 10-29 and `main()` at 5976) | The runner's own help still lists eleven verbs and omits `prepare-explore`, and it still describes phase 1 as "free public researchers from one filtered topic sentence, a Flash pair on the repository" instead of the finder trio, six seats and eleven topics. `docs/WORKFLOW.md` counts twelve verbs and names the new preparation step, so a user cannot discover `prepare-explore` or the current swarm shape from `stage2.py --help`. | deepseek-v4.1-flash | fixed — not a test — runner help names prepare-explore, the finder trio, six seats and eleven topics. | no — not a test | disagree — The module docstring lists prepare-explore and describes the finder trio, six seats and eleven topics. |
| L4-4 | MINOR | MAINT | change | `prompts/01-explore.md:10` ("**Gate:** none.") against `docs/WORKFLOW.md` phase table, phase-1 gate `research-handoff` | The phase-1 prompt still declares no gate, although the workflow now blocks a complete swarm run through the `research-handoff` check; the same prompt later names that gate. A maintainer following the phase prompt is not told that phase 1 is gated or what closes it. | deepseek-v4.1-flash | fixed — not a test — prompts/01-explore.md names the research-handoff gate; text approved by the maintainer on 2026-10-22, because prompts/ is human-written | no | disagree — The phase-1 prompt now explicitly names research-handoff as its gate. |
| L5-1 | MAJOR | SPEC | base | `plans/changes/research-swarm/spec.md:952–958` | The four criteria the Q-18 amendment adds under its own `##` heading (62–65) carry no `*Basis:*` line, while every one of the other 61 criteria names one; the new blocking handoff gate keeps holding criteria added under later main headings to the basis rule — its scan continues past later headings, and `tests/test_research_handoff.py::test_amended_criteria_after_main_headings_require_basis` proves a basis-less amendment criterion turns the gate red. Once this change gains its first complete v2 run, `make verify` fails with four "names no supported claim and no answered Q-record as its basis" findings, and ADR 0013's promise that every criterion names its proof is unmet; naming `decisions.md#Q-18` there is the missing line. | glm-5.3-flash | fixed — tests/test_research_handoff.py::test_research_swarm_seat_amendment_has_answered_bases | yes — tests/test_research_handoff.py::test_research_swarm_seat_amendment_has_answered_bases | disagree — Criteria 62–65 each now carry a Basis referencing decisions.md#Q-18. |
| L5-2 | MINOR | MAINT | base | `scripts/stage2_research_run.py:303` | `self.plan_size` is assigned once and never read anywhere in scripts or tests — the derived declared slot plan is used only for its side-effect validation — so a maintainer reading the attribute assumes the planned slot count gates the run's budget or dispatch somewhere, when only the length of `expected_slots()` and the `39 + 3N` manifest field do. | glm-5.3-flash | fixed — not a test — Removed the unread plan_size attribute; retained slot-plan validation. | no — not a test | disagree — self.plan_size is absent from the current implementation; an unused attribute alone also establishes no correctness fault. |
| L5-3 | MINOR | MAINT | base | `scripts/stage2_research_tools.mjs` (`isPrivateIp`, `validatedAddress`) | The refuse-list covers only the ranges it names; a host the model chooses that resolves to another non-global address — TEST-NET 192.0.2.0/24, benchmark 198.18.0.0/15, multicast 224.0.0.0/4, reserved 240.0.0.0/4, or IPv6 multicast such as ff02::1 — passes the address check (any well-formed hex-and-colon IPv6 past the named ranges counts as public) and is fetched with the connection pinned to it, so the public-only boundary the module header and criteria 8–9 state is enforced only for the listed ranges. | glm-5.3-flash | fixed — tests/test_stage2_research_tools.py::test_non_global_lookup_addresses_never_reach_the_transport | yes — tests/test_stage2_research_tools.py::test_non_global_lookup_addresses_never_reach_the_transport | disagree — The current address checks reject every listed IPv4 range and IPv6 multicast. |
| L6-1 | MINOR | SPEC | design | plans/changes/research-swarm/design.md:61-90 (Declaration → seats) vs model-endpoints.yaml `research_swarm.repository_seats`/`online_seats` | The design mandates three pinned preferred `{endpoint, model}` pairs per trio and lists specific Go models (deepseek-v4.1-flash, mimo-v2.6-flash, qwen3.8-flash), and says to "replace `research_swarm`'s `free_endpoint`/`free_roster`" even though the shipped YAML block is net-new with every Go seat open (`{endpoint: opencode-go}`) per Q-18; a maintainer editing the config per the design would pin models the runner (`prepare_explore`) discards in favour of live catalog selection. | hy3 | fixed — not a test — design.md now describes open Go seats selected from the live catalog under Q-18 and the pinned Haiku seat. | no — not a test | disagree — The current design explicitly declares five open Go seats and one pinned Haiku seat. |
| L6-2 | MINOR | MAINT | decisions | docs/research/2026-10-18-research-judge-capacity.md (J derivation) vs plans/changes/research-swarm/decisions.md S-38 | The research note fixes the judge whole-packet limit at J=200,000 characters from documented Opus 5.5 capacity ("This implements the existing spec's derivation duty"), but ruling S-38 explicitly states the ruling names no number for the limit because the actual context size was not read; the two artifacts in the same change disagree on whether a fixed judge-packet limit is set, leaving the cap implementation without a single authority. | hy3 | fixed — not a test — the capacity note describes the implemented limit and defers to S-38; decisions.md remains unchanged. | no — not a test | disagree — The capacity note distinguishes S-38’s derivation requirement from the agent-derived numeric implementation limit. |
| L7-1 | BLOCKER | SPEC | docs | docs/research/2026-10-18-research-judge-capacity.md ("J = 200,000 characters"), scripts/stage2_research_judge.py:32 | The whole judge packet is capped at 200,000 characters, derived with "tokens per character = 4", while the change's own excerpt caps allow 4,000 characters per claim and up to seven claims per report, and a run holds 39 required reports; at the declared caps the packet is several times the limit, so the judge is refused with judge-packet-over-limit after up to 38 spent calls and the promised complete run cannot end. The conversion factor also looks inverted (usual heuristics are about four characters per token, not four tokens per character), making the limit far smaller than the derivation intends. | mimo-v2.6-pro | fixed — tests/test_stage2_swarm.py::test_the_judge_packet_limit_assumes_at_most_one_token_per_character | yes — tests/test_stage2_swarm.py::test_the_judge_packet_limit_assumes_at_most_one_token_per_character | disagree — The current limit is 1,600,000 characters, uses 0.5 tokens per character and accounts for 33 required topic reports; oversized packets deliberately remain incomplete. |
| L7-2 | MAJOR | SPEC | docs-vs-code | docs/WORKFLOW.md §4 "The handoff is checked" (the sentence naming scripts/check_research_handoff.py) | The text promises the check re-derives the obligation inventory independently of the runner, but scripts/check_research_handoff.py imports research_handoff.derive_inventory, the same module the runner uses ("the one derivation the runner shares", its own import comment and scripts/kit/manifest.yaml); a wrong derivation makes the run's inventory and the gate agree with each other, so the gate cannot catch an obligation the derivation drops. | mimo-v2.6-pro | fixed — not a test — WORKFLOW.md names the shared research_handoff.derive_inventory function and its inability to detect obligations omitted by that derivation. | no — not a test | disagree — The workflow now explicitly names the shared derivation and states that the gate cannot detect omissions within that function. |
| L7-3 | MINOR | MAINT | declaration | model-endpoints.yaml, opencode-go `bemerkung` ("the eleven Flash research calls of the swarm declared below") | The count matches nothing in the declared run: under the shipped seats the endpoint carries 27 plus 3N research calls (2 finder, 16 repository-topic, 9 online-seat, 3N free), and "Flash" names a tier the Q-18 amendment removed from the Go seats; a maintainer planning quota from this comment is misled. | mimo-v2.6-pro | fixed — not a test — the opencode-go remark drops the eleven-Flash-calls count and names the swarm's Go call kinds and that their number grows with the free seats (no total stated: not measured); done by hand by the orchestrator, because the runner may not commit the human-decided AGENTS.md and model-endpoints.yaml (2026-10-26) | no — not a test | disagree — The endpoint comment now describes the research roles and variable call count without claiming eleven Flash calls. |
| L7-4 | MINOR | MAINT | declaration | model-endpoints.yaml, `research_swarm` comment ("Die Rollen sind hier DEKLARIERT … lehnt jede Rolle ab, deren Endpunkt oder Modell hier nicht steht") vs the block's keys | The comment claims every role is declared in this block and unlisted roles are refused, but no map-merge role is declared; scripts/stage2_availability.py fills `finder_merge` silently from `judge`, so editing `judge` changes the merge model with no declaration and no refusal. | mimo-v2.6-pro | fixed — not a test — the research_swarm comment names that finder_merge falls back to judge; done by hand by the orchestrator, because the runner may not commit the human-decided AGENTS.md and model-endpoints.yaml (2026-10-26) | no — not a test | disagree — The declaration comment now explicitly documents finder_merge defaulting to judge. |
| L7-5 | MINOR | MAINT | docs | AGENTS.md, Stage 2 paragraph ("GLM 5.3 Flash explores and implements") | The unchanged first half of the paragraph still states unconditionally that GLM 5.3 Flash explores, contradicting the routing added in the same paragraph (swarm for a feature or architectural change, GLM Flash only for bounded or spike); a reader of the file agents follow first gets both answers. | mimo-v2.6-pro | fixed — not a test — AGENTS.md says GLM 5.3 Flash explores only bounded and spike changes; done by hand by the orchestrator, because the runner may not commit the human-decided AGENTS.md and model-endpoints.yaml (2026-10-26) | no — not a test | disagree — AGENTS.md now limits GLM exploration to bounded changes and spikes. |
| L7-6 | MINOR | MAINT | declaration | model-endpoints.yaml, `datenklassen.public-web.bemerkung` ("ADR 0020 draft") | The same file elsewhere speaks of "since ADR 0020" as in force, and the ADR itself states it is proposed until its merge; one declaration calling it draft while its rules are enforced leaves unclear whether the data class and its boundary bind before the merge. | mimo-v2.6-pro | fixed — not a test — the public-web remark calls ADR 0020 proposed until its merge, like the other mentions; done by hand by the orchestrator, because the runner may not commit the human-decided AGENTS.md and model-endpoints.yaml (2026-10-26) | no — not a test | disagree — The declaration explicitly states that ADR 0020 remains proposed until merge; enforcement within its implementation branch does not establish acceptance. |
| L7-7 | MINOR | MAINT | docs | docs/WORKFLOW.md §4 ("`--stage2-off [REASON]` keeps the Stage-1 route and skips the class entirely") | The text says the fallback skips the class, but the declared contract (the same section's routing text and the design) refuses with exit 2 when `--class` is passed beside `--stage2-off`; a caller who reads "skips" as "ignores" gets a refusal instead of a run. | mimo-v2.6-pro | fixed — not a test — WORKFLOW.md states that combining --class with --stage2-off is refused with exit 2 before any call. | no — not a test | disagree — The workflow now distinguishes skipped class derivation from explicitly refusing --class alongside --stage2-off. |

Rounds run: 5

Record digest: sha256:444ae0262dfce616519a5072ef055cdf782ef28242f78df7fa791863ad6fa588

Record identity: sha256:e3927ded99088b3fc9fdeea9e023392785315ab62bc1799b43f493e4ef4a3920

Cut rounds: 3, 4, 5, 6, 7

Loop state: {"availability": {"checked_at": "2026-10-22T11:33:31+00:00", "failed": {"longcat-2.0": "pi call failed: exit 1: 402: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Endpoint is unavailable.\"}", "longcat-2.5-preview-free": "pi call failed: exit 1: 402: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Endpoint is unavailable.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: [400] Unsupported model mimo-v2.5-pro\"}"}, "reachable": ["cat-jam-free", "deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "skipped": {"gemini-4-argon-contributor": "not admitted; data terms have not been read", "gpt-5.6-luna": "not admitted; data terms have not been read", "grok-4.6": "not admitted; data terms have not been read", "grok-4.7": "not admitted; data terms have not been read", "kimi-k2.7-code": "not admitted; data terms have not been read", "kimi-k3": "not admitted; data terms have not been read", "minimax-m2.7": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "space-bunny": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)"]}, "consumed": ["free", "flash", "rung:glm-5.3-flash", "rung:hy3", "rung:mimo-v2.6-pro"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "big-pickle", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-flash", "provider": "opencode"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "exo-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "ling-3.0-flash-fin-free", "provider": "opencode"}, {"model": "ling-3.1-flash-free", "provider": "opencode"}, {"model": "longcat-2.5-preview-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-spark-1.3-contributor-free", "provider": "opencode"}, {"model": "nemotron-3-ultra-free", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "space-bunny-free", "provider": "opencode"}, {"model": "step-5-preview-free", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-flash", "provider": "opencode-go"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon-contributor", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.6", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-preview-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m2.7", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "space-bunny", "provider": "opencode-go"}, {"model": "step-5-preview-free", "provider": "opencode-go"}], "checked_at": "2026-10-22T11:31:32+00:00", "models_store": {"opencode-go": {"checkedAt": 1792668691381, "etag": "W/\"65e1c3b71054c3b1741fe4cb46560dbf\"", "lastModified": 1792068066000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "cat-jam-free", "input": ["text"], "maxTokens": 131072, "name": "Cat Jam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"forceAdaptiveThinking": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro (New)", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/v1", "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 0, "input": 4, "output": 20}, "id": "gemini-4-argon-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.6", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.6", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 0, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "LongCat 2.5 Preview Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 204800, "cost": {"cacheRead": 0.06, "cacheWrite": 0.375, "input": 0.3, "output": 1.2}, "id": "minimax-m2.7", "input": ["text"], "maxTokens": 131072, "name": "MiniMax-M2.7", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "space-bunny", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 524288, "name": "Space Bunny", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "step-5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "overlay": ["cat-jam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon-contributor", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.6", "grok-4.7", "hy3", "hy4-preview", "kimi-k2.7-code", "kimi-k3", "longcat-2.0", "longcat-2.5-preview-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m2.7", "minimax-m3", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "space-bunny", "step-5-preview-free"], "pi_version": "1.2.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["cat-jam-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "rungs": ["glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"]}}

Kept from the loop record:

> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured).
> Notice: in the live catalog without a terms reading: gemini-4-argon-contributor, gpt-5.6-luna, grok-4.6, grok-4.7, kimi-k2.7-code, kimi-k3, minimax-m2.7, muse-spark-1.2-contributor, muse-spark-1.3-contributor, space-bunny.
> cat-jam-free reported no finding.
> The diff was cut: the change diff was cut at 2000 of 2251 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> No finding.
> 
> mimo-v2.5 failed: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi was stopped by the reviewer time limit of 30 minutes; the round time limit expired; no replacement starts
> mimo-v2.6-flash failed: /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm/tools/pi/pi was stopped by the reviewer time limit of 30 minutes; the round time limit expired; no replacement starts
> The diff was cut: the change diff was cut at 2000 of 31513 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The diff was cut: the change diff was cut at 2000 of 31610 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The diff was cut: the change diff was cut at 2000 of 31700 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The diff was cut: the change diff was cut at 2000 of 31720 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.

<!-- End of released loop record -->

Stage-2 call, 2026-10-26: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 664 files, 2246 commits, 12 rules.

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 664 files, 2248 commits, 12 rules.

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 664 files, 2252 commits, 12 rules.
