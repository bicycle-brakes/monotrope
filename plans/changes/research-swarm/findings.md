---
title: "Findings — research-swarm"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-17
updated: 2026-10-19
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
| F-1 | BLOCKER | SPEC | base | `plans/changes/research-swarm/plan.md`, build step 2, "Verification" and criterion ledger lines for 8 and 9; `plans/changes/research-swarm/research.md` | The offline capture with the real pinned Pi 1.1.0, synthetic private canaries and a local mock model server has not been run: neither `research.md` nor any other file of the change records its version, source hashes, method or canary outcomes. The plan places it in build step 2, before step 3 and before the decision pull request, and says its evidence belongs in the research artefact; the Definition of Done lists it beside `make verify`, separately from the live qualification that alone is deferred until after the merge. It contacts no external endpoint, so nothing in the spec defers it. The criterion ledger rests criteria 8 and 9 partly on it ("not a test"), so the actual Pi prompt, tool schemas and outbound payloads of a free context are unproven: every test of the boundary drives a stand-in that only records its own argv and environment. F-2 shows the capture would not have passed. [Definition of Done; criteria 8, 9] | Opus 5.5 | open — maintainer, 2026-10-15: the capture runs after F-2 is repaired, with the maintainer present, as its own step before a fresh phase-6 re-check; it stays a pre-merge requirement | — |
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
| F-11 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:296`; `scripts/stage2_research_snapshot.py:118` | A successful run lasting more than 60 seconds cannot publish complete: the snapshot retains its preparation deadline, and the final `changed_paths()` reuses that expired deadline. A clock-controlled reproduction raises `ResearchSnapshotError` for an unchanged tree; `run()` converts this into incomplete exit 1. Publication needs its own valid checking deadline. [criteria 16, 18] | Codex | taken — spec criteria 16, 18 | — |
| F-12 | BLOCKER | SPEC | base | `scripts/stage2_research_store.py:58`; `scripts/stage2_research_run.py:286,535` | Without `XDG_STATE_HOME`, the store defaults to a directory beneath the user's HOME, which Claude research processes inherit. The placement guard checks only the worktree and git directory, so it accepts storage inside a model's home. The default configuration therefore violates the required separation of stored peer results from model home directories. [criterion 52] | Codex | taken — spec criterion 52 | — |
| F-13 | BLOCKER | SPEC | base | `scripts/stage2_availability.py:197`; `scripts/stage2_research_run.py:537` | The measured catalog never reaches Pi's fresh agent directory: neither probes nor research launches write its model definitions or model store. Pi consequently resolves models from shipped metadata or fabricated defaults. Locally reproduced: the selector accepts `qwen3.8-flash` advertised as `openai-completions`, while pinned Pi resolves that id as `anthropic-messages`; a newly selected `alpha-free` advertised as `anthropic-messages` resolves as `openai-completions`. Calls can therefore use an unmeasured transport despite passing preparation. [criteria 38, 43, 61] | Codex | taken — spec criteria 38, 43, 61 | — |
| F-14 | BLOCKER | SPEC | base | `scripts/stage2_availability.py:564`; `scripts/stage2_research_run.py:941` | Preparation discards the catalog's per-candidate evidence and exclusions when constructing its receipt. For example, a free candidate excluded because `tool_call` is false leaves no candidate id, field value or exclusion reason in that receipt. Publication also omits preparation time, pool, candidate outcomes and probe audits from the manifest; consumption deletes the receipt. The published run cannot establish why candidates were admitted or excluded. [criteria 38, 44, 46] | Codex | taken — spec criteria 38, 44, 46 | — |
| F-15 | BLOCKER | SPEC | base | `scripts/stage2_research_dispatch.py:175`; `scripts/stage2_research_run.py:675,1042` | After a terminal store write fails, dispatch stops invoking terminal callbacks. Cancelled siblings and their available output remain only in `DispatchResult`, which `run_stage()` discards when raising the stop. A two-slot reproduction returns both outcomes but delivers only the first to the run. A persistent write failure additionally escapes from `publish()` at `set_append()` before research is appended, losing the required incomplete record and partial evidence. [criteria 18, 57] | Codex | taken — spec criteria 18, 57 | — |
| F-16 | BLOCKER | SPEC | base | `scripts/check_research_handoff.py:103,404` | The handoff gate silently chooses the last duplicate JSON or nested YAML key. Reproduced with an answered record containing two `research_neighbours.keep` keys, first naming A and then B: a spec containing only B produces no findings, silently discarding A. A manifest containing contradictory duplicate `class` keys is also accepted. These ambiguous inputs must produce not-measured exit 3 instead of a successful interpretation. [criterion 33] | Codex | fixed — tests/test_research_handoff.py::test_duplicate_keys_in_records_are_not_measured | — |
| F-17 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:693,923` | If a finder fails, the manifest contains only the three finder slots. Merge, topic author, all topic slots and judge receive neither expected identities nor terminal outcomes because later entries are constructed only when their stages start. The numeric budget does not identify the missing contributions. An aborted run must retain the complete expected slot inventory and explicitly account for unstarted slots. [criterion 18; Data model — Run manifest] | Codex | taken — spec criterion 18 | — |
| F-18 | BLOCKER | SPEC | base | `scripts/stage2_research_run.py:427,450,930`; `scripts/stage2_research_store.py:269` | Reused results cannot retain the required original start time: it exists only in the separate launch record, while result records and adoption omit it. Publication also omits each reused result's original leak-check record, and successful completion clears the store holding that record. A completed resumed run therefore permanently loses both required provenance fields despite reporting reuse. [criterion 55] | Codex | taken — spec criterion 55 | — |

Phase 6 verdict: codex 01a15339-b204-7d12-b7e6-91aca1cfc69d, 2026-10-19
Reviewer session: codex 01a15339-b204-7d12-b7e6-91aca1cfc69d — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
