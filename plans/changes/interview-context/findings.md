---
title: "Findings — interview-context"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-zs7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — interview-context

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1131 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0018-every-question-carries-its-context.md` +118 -0
> - `plans/changes/interview-context/design.md` +141 -0
> - `plans/changes/interview-context/plan.md` +146 -0
> - `plans/changes/interview-context/research.md` +42 -1
> - `plans/changes/interview-context/spec.md` +167 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 14561 lines of this gate left out …]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[.pi/settings.json-read]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[.pi/settings.json-grep]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[.pi/settings.json-find]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[.pi/settings.json-ls]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[tools/policy.mjs-read]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[tools/policy.mjs-grep]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[tools/policy.mjs-find]
> FAILED tests/test_stage2_session_policy.py::test_a_read_of_a_protected_place_passes[tools/policy.mjs-ls]
> FAILED tests/test_stage2_session_policy.py::test_a_write_to_the_git_directory_is_not_protected[edit]
> FAILED tests/test_stage2_session_policy.py::test_a_write_to_the_git_directory_is_not_protected[write]
> FAILED tests/test_stage2_session_policy.py::test_a_symlink_to_a_protected_place_does_not_hide_it[edit]
> FAILED tests/test_stage2_session_policy.py::test_a_symlink_to_a_protected_place_does_not_hide_it[write]
> FAILED tests/test_stage2_session_policy.py::test_case_folding_is_a_host_setting_and_catches_a_differently_cased_name
> FAILED tests/test_stage2_session_policy.py::test_the_case_rule_follows_the_host_platform
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm -rf build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm -r build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm -fr build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm --recursive build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm build -r]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[sudo ls]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[chmod 777 x]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[chmod -R 777 .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[chown root:root x 777]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git reset --hard HEAD~1]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git reset HEAD~1 --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git -C . reset --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git -c core.pager=cat --no-pager reset --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git clean -fd]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git -C sub clean -n]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git -C "my dir" reset --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git -C 'my dir' clean -fd]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm "a;b" -r]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[rm \\\n  -rf y]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git checkout -- .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git checkout main -- src/a.txt]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git checkout .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git checkout -f]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git restore .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git restore src/a.txt]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git restore --worktree --staged .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_asks_and_runs_only_on_yes[git -C "my dir" restore .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[rm -rf build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[rm -r build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[rm -fr build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[rm --recursive build]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[rm build -r]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[sudo ls]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[chmod 777 x]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[chmod -R 777 .]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[chown root:root x 777]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[git reset --hard HEAD~1]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[git reset HEAD~1 --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[git -C . reset --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[git -c core.pager=cat --no-pager reset --hard]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[git clean -fd]
> FAILED tests/test_stage2_session_policy.py::test_a_dangerous_command_is_blocked_when_no_ui_can_ask[git -C sub clean -n]
> 183 failed, 1781 passed, 16 skipped in 586.61s (0:09:46)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9187 earlier lines left out …]
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

Stage-2 call, 2026-10-14: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 424 files, 1141 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/interview-context/design.md` +15 -7
> - `plans/changes/interview-context/plan.md` +51 -12
> - `plans/changes/interview-context/spec.md` +22 -8
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
> E             At index 106068 diff: b'y' != b'i'
> E             Use -v to get more diff
>
> tests/test_bead_render.py:72: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_bead_render.py::test_render_twice_is_byte_equal - Assertion...
> 1 failed, 1963 passed, 16 skipped in 1087.16s (0:18:07)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9275 earlier lines left out …]
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

Stage-2 call, 2026-10-14: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 424 files, 1146 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

ADR answer owed: decisions/answers/interview-context/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).
