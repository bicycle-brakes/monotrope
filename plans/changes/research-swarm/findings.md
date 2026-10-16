---
title: "Findings — research-swarm"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-16
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
| S-21 | MAJOR | SPEC | fix-r1 | `spec.md`, Terms «Selected Go free models»; criteria 39, 41, 42; `research.md`, «Phase-2a incorporation evidence» [GAP] | [AMBIGUITY] The Terms require «explicit catalog tool-call support» and exclude models whose support is «absent». `research.md` records that pinned Pi 1.2.0's Model interface has no tool-support field and leaves the raw capability mapping to phase 4. The spec names no field. Reading A: support is judged per catalog entry. A fresh overlay whose entries carry no such field then excludes every `-free` id as `no-tool-support`, criterion 42 records a valid measured empty selection (N=0), and every run completes with exit 0 while Q-10 never takes effect. Reading B: an overlay whose schema has no tool-support capability cannot be measured reliably (criterion 41). The run then exits nonzero before any model call, and no swarm runs until the mapping exists. The same catalog yields a complete 39-slot run under A and a refused run under B. | Opus | open | — |
| S-22 | MAJOR | SPEC | fix-r1 | `spec.md`, Terms «Frozen input state»; criterion 16; [DETAIL] «Local references resolve against retained frozen bytes» | [AMBIGUITY] The frozen state includes a «retained copy of every tracked file», and criterion 16 is refuted when «the retained bytes/reports are absent». Neither says how long the copy is kept or where. Reading A: the copy lives in run scratch and is discarded at the end. Only HEAD and the digest persist, and the absence case can only arise during the run. Reading B: the copy is durable run evidence. Kept under the change folder outside `research.md`, it makes every run incomplete, because the digest check ignores only the runner's research appends and restamp. Appended to `research.md`, the whole tracked tree is added on every run, and the next run's private brief («frozen research.md header/body») carries every earlier copy to the finders and the topic author. A post-run test that looks for the retained bytes passes under B and fails under A. | Opus | open | — |
| S-23 | MAJOR | SPEC | fix-r1 | `spec.md`, criterion 34; Terms «Evidence status and disposition» | [AMBIGUITY] Criterion 34 accepts a Basis that resolves to «a global claim from a complete run». The Terms say unsupported claims «are never evidence», and refuted or off-brief claims are valid claims that carry a judge disposition. Reading A: any existing global id from a complete run resolves, so a criterion resting on an `unsupported`, `refuted` or `off-brief` claim passes the gate. Reading B: only a valid claim, or only a `supported` one, can serve as a basis, and the same spec exits 1. Criterion 34's refutations name only missing and incomplete-run claims, so a test whose Basis names an unsupported claim has no expected result. | Opus | open | — |
| S-24 | MAJOR | SPEC | fix-r1 | `spec.md`, template under Topic contract; criteria 29, 31; [DETAIL]s «neighbour contradictions and proposed removal of given neighbours also do so» and «class/neighbor fields» | Cannot go red as specified. The [DETAIL]s say neighbour contradictions and proposed removals of given neighbours derive obligations «independently of the judge», from «class/neighbor fields». Criteria 29 and 31 are refuted when such a case has no item. The template defines `class_assessment` for topic 3, but topic 5 has no field for a contradiction or for a given neighbour found unrelated, only the free-prose section «relation to neighbouring specs». Refuting input: a topic-5 report whose claim C2 says a given neighbour's criterion contradicts the change, with no `[DECISION]` question. It passes the template, and neither runner nor gate has a field to derive the item from. The only remaining source is the judge's output, which the [DETAIL] says the derivation must not depend on. The implementer has to invent the field or fall back on the judge. | Opus | open | — |
| S-25 | MAJOR | SPEC | base | `spec.md`, Topic contract, finder paragraph; criteria 5, 24, 29 | Missing: what makes the Opus map merge a «valid recorded result» (criterion 5). Topics 1–8 are bounded to mapped code and places, so the merge sets every repository topic's scope. The spec does not say: (1) whether the merge must keep every finder entry (a union without duplicates) or may drop or add entries, and how a drop is recorded; (2) whether finder and merge entries must resolve against the frozen state like claims under criterion 16, and what happens to an entry that does not; (3) whether every given neighbour must appear in the map. Test case: a merge that omits a `path::symbol` one finder listed, or adds one no finder listed, has no expected result under criterion 5 or 24. | Opus | open | — |
| S-26 | MINOR | SPEC | fix-r1 | `spec.md`, Terms «Public topic»; criterion 23 | [AMBIGUITY] The rule refuses a listed set of characters (digits, underscores, slashes, backticks, colons, other dots). It also says each word is letters «joined only by» single hyphens or apostrophes. It says nothing about commas, semicolons, quotation marks, parentheses, question marks, stand-alone dashes or the typographic apostrophe ’. Reading A: a word is a whitespace-separated token that must match the letter pattern. Then «Isolation, Prüfung und Wiederherstellung für Agentenläufe» is refused, and the run ends with exit 1 after five model calls. Reading B: only the listed characters are refused and other punctuation separates words, so the same sentence passes. Criterion 23 gives opposite expected results for it. | Opus | open | — |
| S-27 | MINOR | SPEC | fix-r1 | `spec.md`, criterion 30; [DETAIL] «enforces neighbour parity» | [AMBIGUITY] Criterion 30 is refuted by a lost confirmed or given path, an escaping or duplicate path, and «an unconfirmed suggestion». The [DETAIL] says the gate «enforces neighbour parity». Reading A (parity): the header must equal the confirmed and given neighbours minus those a maintainer dropped. A `spec.md` path that no finder suggested and no header gave then fails with exit 1. Reading B (the criterion's list): such a path is not a suggestion at all and passes. A phase-2 author who adds a neighbour found while drafting gets opposite gate results. | Opus | open | — |
| S-28 | MINOR | SPEC | base | `spec.md`, criterion 41; [DETAIL] «Preflight validates class and given neighbours, then measures the catalog» | Missing: the exit code for criterion 41. It says only «exits nonzero» for a timeout, a stale-only, malformed or ambiguous catalog. Every neighbouring preflight case has a fixed code: invalid neighbours and malformed policy exit 2, a missing include exits 1, and the repository's code for not measured is 3 (criterion 33). A catalog failure could be exit 1 (failed result) or exit 3 (not measured). The implementer has to pick, and a caller that treats 1 and 3 differently behaves differently. | Opus | open | — |
| S-29 | MINOR | SPEC | base | `spec.md`, criteria 14, 23, 28; [DETAIL] stage order and private brief | Missing: what the three Opus roles (map merge, topic author, judge) may read beyond their packets. The spec fixes their inputs but not whether they run with file tools. With tools, the judge can check a cited `path::symbol` before scoring a claim `supported` or `refuted`, and the author can read past the brief. Without them, «supported» can only mean cited and not contradicted by peers. The implementer has to choose, and the choice changes the dispositions criterion 28 counts and what can reach criterion 23's public sentence. | Opus | open | — |
| S-30 | MINOR | SPEC | base | `spec.md`, Open decisions, [DETAIL] «Keep the architectural class, ADR 0020 and 12-hour phase-4 stop»; header `appetite: 12` | Missing: how the 12-hour phase-4 stop is computed. The [DETAIL] keeps the stop and says earlier implementation «counts», its span «unmeasured» and «not reset». Nothing says how that span is to be established, so neither the remaining appetite nor the moment phase 4 must stop can be determined from the spec. | Opus | open | — |
