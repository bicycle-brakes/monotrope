---
title: "Findings — codex-drafts"
category: findings
status: draft
implementation_status: none
date: 2026-10-12
created: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-rhq
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — codex-drafts

Stage-2 call, 2026-10-12: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 376 files, 932 commits, 12 rules.

## Phase 2a — Codex, 2026-10-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`, criteria 13 and 16 | [AMBIGUITY] A draft has only the missing-answer `adr-answers` gate failure, but its plan lacks `## Time used`. Reading criterion 13 as passing all post-run checks produces a commit; reading it as waiving only the verification failure leaves criterion 16 failing and triggers another attempt. The precedence is unspecified. | Codex | fixed in `873d2af` — not a test — criterion 13 now waives only the red `make verify`; criteria 14 to 16 still apply, and its refutation names a `plan.md` without `## Time used` | — |
| F-2 | BLOCKER | SPEC | base | `spec.md`, criteria 28, 31 and 34 | [AMBIGUITY] Input: an old `Reviewer session: codex <id>` line followed by a new Opus phase-2a block. Criterion 31 requires resuming that Codex session; criterion 34 requires a fresh session where Opus performed phase 2a. Selecting the recorded line resumes the earlier context; selecting the latest review starts fresh. The controlling rule is unspecified. | Codex | fixed in `873d2af` — not a test — criteria 30 and 31 key on the last `## Phase 2a` block: resume only when it is Codex's with its session line, fresh after an Opus block; plan's DETAIL follows | — |
| F-3 | MAJOR | SPEC | base | `spec.md`, criteria 8, 10 and 33 | The mandatory second draft starts with the first draft's committed ADR in its baseline. Criterion 8 therefore restores edits to that ADR, while criterion 10 permits another new ADR because the first no longer counts as new. When review findings require corresponding ADR changes, the spec provides no repair contract: retaining the original leaves stale content, while creating a replacement leaves two records for the change. | Codex | fixed in `873d2af` — not a test — a new ADR file is counted against the merge base of the baseline and `origin/main`, so a second draft edits the first draft's ADR and criterion 10 still counts one | — |

Reviewer session: codex 01a130f4-7a06-7710-82b0-acf5a60d9dd1

Stage-2 call, 2026-10-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 385 files, 961 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +2 -2
> - `docs/WORKFLOW.md` +103 -38
> - `model-endpoints.yaml` +11 -6
> - `plans/changes/codex-drafts/plan.md` +38 -31
> - `prompts/02-spec.md` +8 -2
> - `prompts/02a-spec-review.md` +11 -8
> - `prompts/02b-design.md` +5 -1
> - `prompts/03-plan.md` +8 -3
> - `prompts/06-review.md` +11 -12
> - `scripts/stage2.py` +383 -35
> - `tests/test_model_endpoints.py` +21 -3
> - `tests/test_stage2.py` +824 -71
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 715 lines of this gate left out …]
>
> tests/test_stage2.py:2232: Failed
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> ____________________ test_routing_gives_2b_the_prompt_model ____________________
>
>     def test_routing_gives_2b_the_prompt_model() -> None:
>         rows = first_table(markdown_section(workflow_text("docs/WORKFLOW.md"), "Model routing"))
>         firsts = [row[0].split()[0] for row in rows]
>         assert any(firsts[i : i + 3] == ["2a", "2b", "3"] for i in range(len(firsts))), firsts
>         bold = re.search(r"\*\*(.+?)\*\*", rows[firsts.index("2b")][1])
> >       assert bold and bold.group(1) == prompt_model(workflow_text(DESIGN_PROMPT))
> E       AssertionError: assert (<re.Match object; span=(0, 12), match='**Opus 5.5**'> and 'Opus 5.5' == 'Codex (`gpt-6.1-sol`)'
> E         
> E         - Codex (`gpt-6.1-sol`)
> E         + Opus 5.5)
>
> tests/test_templates.py:756: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves[02-spec.md-Codex (`gpt-6.1-sol`)]
> FAILED tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves[02b-design.md-Codex (`gpt-6.1-sol`)]
> FAILED tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves[03-plan.md-Codex (`gpt-6.1-sol`)]
> FAILED tests/test_stage2.py::test_table_lines_that_are_not_rows_are_never_reported_as_no_finding[three-cells]
> FAILED tests/test_stage2.py::test_table_lines_that_are_not_rows_are_never_reported_as_no_finding[five-cells]
> FAILED tests/test_stage2.py::test_table_lines_that_are_not_rows_are_never_reported_as_no_finding[short-table]
> FAILED tests/test_stage2.py::test_the_foreign_environment_is_the_runners - As...
> FAILED tests/test_stage2.py::test_no_call_carries_another_endpoints_key - Ass...
> FAILED tests/test_stage2.py::test_a_draft_starts_codex_with_workspace_write_and_no_bypass
> FAILED tests/test_stage2.py::test_the_draft_prompt_carries_the_three_phase_prompts_and_the_rules
> FAILED tests/test_stage2.py::test_paths_outside_the_change_folder_are_put_back_and_named
> FAILED tests/test_stage2.py::test_an_edited_decisions_file_is_put_back - Asse...
> FAILED tests/test_stage2.py::test_a_red_verify_fails_the_draft_attempt - Asse...
> FAILED tests/test_stage2.py::test_only_the_changes_own_missing_adr_answer_is_tolerated
> FAILED tests/test_stage2.py::test_a_missing_spec_or_plan_fails_the_attempt - ...
> FAILED tests/test_stage2.py::test_a_plan_without_its_card_fails_the_attempt
> FAILED tests/test_stage2.py::test_a_passing_draft_makes_one_commit_and_leaves_a_clean_tree
> FAILED tests/test_stage2.py::test_a_failed_first_draft_gets_one_codex_repair_with_its_diagnostics
> FAILED tests/test_stage2.py::test_two_failed_codex_attempts_fall_back_to_glm_5_3
> FAILED tests/test_stage2.py::test_a_failed_draft_call_is_put_back_and_recorded
> FAILED tests/test_stage2.py::test_a_failed_draft_check_leaves_its_block_and_its_tree
> FAILED tests/test_stage2.py::test_three_failed_draft_attempts_exit_1_without_a_commit
> FAILED tests/test_stage2.py::test_a_codex_draft_never_reads_the_glm_key - Fai...
> FAILED tests/test_templates.py::test_routing_gives_2b_the_prompt_model - Asse...
> 24 failed, 1764 passed, 16 skipped in 257.66s (0:04:17)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/stage2.py:1694:56: ARG001 Unused function argument: `key`
>      |
> 1694 | def verify_evidence(done: subprocess.CompletedProcess, key: str | None) -> str:
>      |                                                        ^^^ ARG001
> 1695 |     """The bounded evidence of a red `make verify`: the framed gates that blocked, else the run's tail."""
> 1696 |     output = (done.stdout or "") + (done.stderr or "")
>      |
>
> tests/test_stage2.py:4885:26: B905 [*] `zip()` without an explicit `strict=` parameter
>      |
> 4883 |         return [f"the draft section holds {len(steps)} numbered steps, not 5"]
> 4884 |     found = []
> 4885 |     for step, needles in zip(steps, DRAFT_ORDER_NEEDLES):
>      |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ B905
> 4886 |         one = flat(step)
> 4887 |         for needle in needles:
>      |
>      = help: Add explicit value for parameter `strict=`
>
> Found 2 errors.
> [*] 1 fixable with the `--fix` option.
> ── [ruff-check] RED (block) — der Lauf ist rot.
> ── [ruff-format] $ lauf_cmd
> Would reformat: scripts/stage2.py
> 1 file would be reformatted, 60 files already formatted
> ── [ruff-format] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (2):
>   - 5 rote(r) Fall/Faelle ohne deklarierten Grund
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-Codex (`gpt-6.1-sol`)]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02b-design.md-Codex (`gpt-6.1-sol`)]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[03-plan.md-Codex (`gpt-6.1-sol`)]
>       tests.test_model_endpoints::test_no_remark_routes_the_spec_review_to_codex
>       tests.test_templates::test_routing_gives_2b_the_prompt_model
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>   - 3 Eintrag/Eintraege in REIST_NICHT haben keinen Fall mehr
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02b-design.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[03-plan.md-Opus 5.5]
>       
>       Entweder wurde der Test umbenannt — dann den Eintrag nachziehen — oder seine Datei reist nicht mehr mit. Der zweite Fall ist der gefaehrliche: die Portabilitaet sinkt, und die gemeldete Quote steigt.
>
> INFO  (1):
>   - 840 von 877 Faellen tragen in ein fremdes Repo (95 %)
>       mechanismus 79 · bestand 306 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 7781 earlier lines left out …]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:19 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:37:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
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

Stage-2 call, 2026-10-13: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 385 files, 961 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +3 -3
> - `plans/changes/codex-drafts/plan.md` +45 -5
> - `prompts/02-spec.md` +3 -3
> - `prompts/02b-design.md` +4 -4
> - `prompts/03-plan.md` +5 -5
> - `scripts/kit/probe.py` +9 -3
> - `scripts/stage2.py` +15 -8
> - `tests/test_stage2.py` +73 -60
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 90 lines of this gate left out …]
>   - leak check clean: 21 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: the draft failed after the allowed attempts; why each attempt failed and the files each changed: plans/changes/demo/findings.md
> refused: the worktree has pre-existing changes outside this change's findings.md: scripts/__pycache__/_verdict.cpython-312.pyc
> ________________ test_a_plan_without_its_card_fails_the_attempt ________________
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3926/test_a_p...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3926/test_a_plan_without_its_card_f0/state'))
>
>     def test_a_plan_without_its_card_fails_the_attempt(world: World) -> None:
>         # Criterion 15. Planted fault: the labels looked for anywhere in the file.
>         draft_world(world)
>         no_pre = PLAN_CARD.replace("Pre-mortem:  it failed\n", "")
>         world.script(
>             codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": no_pre}), codex_ok("T2", "again")],
>             claude=[{"stdout": "glm"}],
>             make=[{"stdout": "green\n"}] * 3,
>         )
>         assert world.run("draft") == 1
>         assert stage2.CARD_PROBLEM in world.text()
>         world.plan.unlink()
>         # The failed run's prepare_derived left an untracked plans/INDEX.md; the next run would refuse it.
>         (world.root / "plans" / "INDEX.md").unlink(missing_ok=True)
>         (world.bin / "calls.jsonl").unlink()
>         late = (
>             "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n## Criterion ledger\n\n"
>             "```text\nFor you:     x\nDone when:   y\nAppetite:    8 h\nNot now:     n\nPre-mortem:  p\n```\n\n## Time used\n"
>         )
>         world.script(
>             codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": late}), codex_ok("T2", "again")],
>             claude=[{"stdout": "glm"}],
>             make=[{"stdout": "green\n"}] * 3,
>         )
> >       assert world.run("draft") == 1
> E       AssertionError: assert 2 == 1
> E        +  where 2 = run('draft')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3926/test_a_p...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3926/test_a_plan_without_its_card_f0/state')).run
>
> tests/test_stage2.py:2077: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: the draft failed after the allowed attempts; why each attempt failed and the files each changed: plans/changes/demo/findings.md
> refused: the worktree has pre-existing changes outside this change's findings.md: scripts/__pycache__/_verdict.cpython-312.pyc
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_the_draft_prompt_carries_the_three_phase_prompts_and_the_rules
> FAILED tests/test_stage2.py::test_a_missing_spec_or_plan_fails_the_attempt - ...
> FAILED tests/test_stage2.py::test_a_plan_without_its_card_fails_the_attempt
> 3 failed, 1785 passed, 16 skipped in 261.68s (0:04:21)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-format] $ lauf_cmd
> Would reformat: scripts/stage2.py
> Would reformat: tests/test_stage2.py
> 2 files would be reformatted, 59 files already formatted
> ── [ruff-format] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 7842 earlier lines left out …]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:19 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:37:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
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

Stage-2 call, 2026-10-13: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 385 files, 961 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/codex-drafts/plan.md` +8 -3
> - `tests/test_stage2.py` +15 -10
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [ruff-format] $ lauf_cmd
> Would reformat: scripts/stage2.py
> Would reformat: tests/test_stage2.py
> 2 files would be reformatted, 59 files already formatted
> ── [ruff-format] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 7894 earlier lines left out …]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:19 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:37:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
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

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 385 files, 962 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route glm · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 385 files, 963 commits, 12 rules.

> Attempt 1 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +16 -11
> - `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md` +4 -1
> - `plans/changes/codex-drafts/plan.md` +9 -3
> - `prompts/02a-spec-review.md` +2 -3
> - `scripts/stage2.py` +7 -4
> - `tests/test_model_endpoints.py` +7 -0
> - `tests/test_stage2.py` +10 -0
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: repair · attempt 2 · route glm-repair · endpoint glm-coding-plan · model glm-5.3 · reason first GLM 5.3 post-run check failed · leak check clean over 385 files, 963 commits, 12 rules.

> Attempt 2 (glm-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/codex-drafts/plan.md` +12 -0
>
> Diagnostics:
> ```text
> - L1-6: tests/test_model_endpoints.py::test_no_old_reviewer_remark_claims_a_review_phase: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> ```

Stage-2 call, 2026-10-13: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two GLM 5.3 post-run checks failed · leak check clean over 385 files, 963 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - the answer holds a line that is no fixed line: All seven rows are already repaired in the tree. I checked L1-1 (the prompt) and
> - On L1-4, `begin_work_call` now takes its producer from `producer_for(endpoint)`. I did not find the name of the pinning test: no taken row carries this id
> ```

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 385 files, 964 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route glm · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 385 files, 965 commits, 12 rules.

> Attempt 1 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +1 -1
> - `docs/WORKFLOW.md` +14 -11
> - `scripts/stage2.py` +22 -4
> - `tests/test_stage2.py` +53 -3
> - `tests/test_templates.py` +3 -2
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 2 lines of this gate left out …]
> .....................................................s..........s....... [ 11%]
> ...........ss................................ss.sssssss..s.......s...... [ 15%]
> ........................................................................ [ 19%]
> ........................................................................ [ 23%]
> ........................................................................ [ 27%]
> ........................................................................ [ 31%]
> ........................................................................ [ 35%]
> ........................................................................ [ 39%]
> ........................................................................ [ 43%]
> ..................s..................................................... [ 47%]
> ........................................................................ [ 51%]
> ........................................................................ [ 55%]
> ........................................................................ [ 59%]
> ..............F......................................................... [ 63%]
> ........................................................................ [ 67%]
> ........................................................................ [ 71%]
> ........................................................................ [ 75%]
> ........................................................................ [ 79%]
> ........................................................................ [ 83%]
> ........................................................................ [ 87%]
> ........................................................................ [ 91%]
> ........................................................................ [ 95%]
> ........................................................................ [ 99%]
> ........                                                                 [100%]
> =================================== FAILURES ===================================
> ____________ test_the_put_back_names_its_remainder_beyond_the_bound ____________
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3949/test_the...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3949/test_the_put_back_names_its_re0/state'))
>
>     def test_the_put_back_names_its_remainder_beyond_the_bound(world: World) -> None:
>         # Repair L2-5. Planted fault: the put-back listing stops at `ATTEMPT_FILES` with no remainder line.
>         draft_world(world)
>         plant = {
>             "plans/changes/demo/spec.md": "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n",
>             "plans/changes/demo/plan.md": PLAN_CARD,
>         }
>         for n in range(stage2.ATTEMPT_FILES + 1):
>             plant[f"stray/file-{n:02d}.txt"] = f"stray {n}\n"
>         world.script(codex=[codex_ok("T1", "drafted", plant=plant)], make=[{"stdout": "green\n"}])
>         assert world.run("draft") == 0
>         assert git(world.root, "status", "--porcelain") == ""
>         block = quote_blocks(world.text())[0]
>         assert block[0] == "Attempt 1 (codex): the runner put back what a draft may not change:"
>         assert f"- `stray/file-{stage2.ATTEMPT_FILES - 1:02d}.txt`" in block, "the last named path"
>         assert f"- `stray/file-{stage2.ATTEMPT_FILES:02d}.txt`" not in block, "the bound holds"
> >       assert "- … and 1 more files" in block, "the remainder is named"
> E       AssertionError: the remainder is named
> E       assert '- … and 1 more files' in ['Attempt 1 (codex): the runner put back what a draft may not change:', '- `stray/file-00.txt`', '- `stray/file-01.txt`', '- `stray/file-02.txt`', '- `stray/file-03.txt`', '- `stray/file-04.txt`', ...]
>
> tests/test_stage2.py:1912: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 2 commits, 1 rules, 1 prompt texts
> draft: verified and committed · route codex · attempt 1
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_the_put_back_names_its_remainder_beyond_the_bound
> 1 failed, 1791 passed, 16 skipped in 268.46s (0:04:28)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-format] $ lauf_cmd
> Would reformat: tests/test_stage2.py
> 1 file would be reformatted, 60 files already formatted
> ── [ruff-format] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 7951 earlier lines left out …]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:19 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:37:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
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
> - `plan.md` did not add a measured line below `## Time used`
> ````

Stage-2 call, 2026-10-13: repair · attempt 2 · route glm-repair · endpoint glm-coding-plan · model glm-5.3 · reason first GLM 5.3 post-run check failed · leak check clean over 385 files, 965 commits, 12 rules.

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 385 files, 966 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route glm · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 385 files, 967 commits, 12 rules.

> Attempt 1 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +20 -18
> - `tests/test_stage2.py` +49 -1
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: repair · attempt 2 · route glm-repair · endpoint glm-coding-plan · model glm-5.3 · reason first GLM 5.3 post-run check failed · leak check clean over 385 files, 967 commits, 12 rules.

> Attempt 2 (glm-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two GLM 5.3 post-run checks failed · leak check clean over 385 files, 967 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 385 files, 968 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-4 | BLOCKER | SPEC | base | `scripts/stage2.py:2529`; `tests/test_stage2.py:2378` | If the GLM attempt stages and commits a file containing its key, the credential scan compares against the model's new HEAD and skips that now-clean file. The runner exits 1 for moved HEAD while leaving the key in the file and commit. The regression test uses an empty commit, leaving the contaminated file uncommitted, so it misses this case. [criterion 25] | Codex | fixed — `tests/test_stage2.py::test_a_glm_draft_that_commits_the_key_is_refused` | no |
| F-5 | BLOCKER | SPEC | base | `scripts/stage2.py:2352` | A second draft can retain the first draft's committed ADR unchanged and add another ADR. The count examines only paths changed against HEAD, so it counts the second file alone and permits a commit containing two ADRs absent from the merge base. The check must count the new ADR files remaining across the whole change. [criterion 10] | Codex | fixed — `tests/test_stage2.py::test_a_second_draft_that_adds_another_adr_fails_the_attempt` | no |
| F-6 | BLOCKER | SPEC | base | `scripts/stage2.py:2369`; `scripts/stage2.py:2461` | The missing-answer exception accepts verification whose other failures were not measured correctly. Terminating verification after the missing ADR answer and an unfinished `interview-minimums` gate makes `only_answer_owed` return True. A failing pytest gate printing `── [pytest] gruen` in its output also hides its real RED closing frame. Either case can commit the draft despite incomplete or failed verification. [criterion 13] | Codex | fixed — `tests/test_stage2.py::test_a_verification_that_stopped_before_its_gates_closed_owes_nothing` and `tests/test_stage2.py::test_a_gate_output_printing_a_green_frame_does_not_hide_its_red_frame` | no |
| F-7 | MAJOR | SPEC | base | `scripts/stage2.py:2458`; `scripts/stage2.py:2570` | If `make` cannot start after a successful Codex call, `CallFailed` escapes the post-run checks. The runner stops after one attempt, writes no quoted failure block, and starts neither the Codex repair nor the GLM fallback. Post-run failures must leave their diagnostics and advance through the attempt chain. [criteria 18 and 21] | Codex | fixed — `tests/test_stage2.py::test_a_make_that_cannot_start_fails_the_attempt_and_moves_the_chain` | no |
| F-8 | MAJOR | SPEC | base | `scripts/stage2.py:1543`; `tests/test_stage2.py:1896` | When an attempt writes 41 forbidden paths, the runner restores them but names only the first 40; the last becomes “1 more files.” The test explicitly requires that path's name to be absent. Thus the audit cannot identify every restored path, contrary to the required evidence. [criterion 8] | Codex | fixed — `tests/test_stage2.py::test_the_put_back_names_every_path_beyond_the_bound` | yes |

Phase 6 verdict: codex 01a130f4-7a06-7710-82b0-acf5a60d9dd1, 2026-10-13

## Phase 4b — loop rows, released 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | MAINT | base | prompts/02a-spec-review.md:22 against :13-15 | The prompt's closing paragraph still tells the reviewer that the runner "adds the reviewer, the status and the session line", while its own Session paragraph says the runner writes "no session line" and `spec_review` appends none; the stale sentence is the last place describing the removed Codex spec-review session and should be corrected to name only the reviewer and the status. | deepseek-v4.1-flash | fixed — not a test — a false statement: the closing paragraph of prompts/02a-spec-review.md still says the runner adds a session line, which its own Session paragraph and spec_review deny; name only the reviewer and the status | no | agree |
| L1-2 | MAJOR | MAINT | base | docs/WORKFLOW.md:434-439 against :413-416, :425-428 | The paragraph "Spec and plan on Opus 5.5 at effort xhigh ... for the whole repository" was left unchanged while the table directly above routes phases 2, 2b and 3 to gpt-6.1-sol wherever the runner drafts, and the section's own "five rows leave this table" sentence plus the change's plan step 4 say drafting moves to Codex; a reader meets two answers to which model writes spec, design and plan. Add the runner caveat or scope the paragraph to the by-hand path. | deepseek-v4.1-flash | fixed — not a test — a false statement: the "Spec and plan on Opus 5.5 at effort xhigh" paragraph contradicts the routing table above it; scope it to the by-hand path (a spike, or Stage 2 off) and name the runner draft as the default | no | agree |
| L1-3 | MINOR | MAINT | base | docs/WORKFLOW.md:461-462 against :465-466, prompts/06-review.md:19-20 | The rewritten "One reviewer for both" paragraph says a fresh Codex phase-6 session "first checks that each 2a row arrived in `findings.md`", but the check is against the revised `spec.md` (the prompt says "arrived in it as `findings.md` says"); as written it names the file that already holds the rows, so the check reads as one that cannot fail. Say the revised spec. | deepseek-v4.1-flash | fixed — not a test — a false statement: the fresh phase-6 session checks that each 2a row arrived in the revised spec.md, as prompts/06-review.md says, not in findings.md | no | agree |
| L1-4 | MINOR | MAINT | base | scripts/stage2.py:655-668 against :641-646 | A draft run records its first call through `begin_work_call`, which writes a new `findings.md` header with producer `claude-code` whatever the endpoint, so a first draft whose call went to `openai-codex` stamps the wrong producer while `begin_call` gained the endpoint-to-producer map for exactly this case; derive the producer from the endpoint there too and pin the draft's header by test. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_a_findings_file_the_draft_creates_names_codex | no | agree |
| L1-5 | MINOR | MAINT | base | plans/changes/codex-drafts/plan.md:313-317 | The plan's "Not touched" list names `review` among the functions implementation leaves alone, but the change replaces `review`'s session selection with `recorded_2a_session` to resume only a recorded Codex phase-2a block and start fresh otherwise, the edit its own criteria require; the step list never mentions it either, so the plan understates the change's surface for whoever merges it. | deepseek-v4.1-flash | fixed — not a test — a false statement: plan.md lists `review` under "Not touched" although the change gives it `recorded_2a_session`; move it out of that list and name the edit in the step list | no | agree |
| L1-6 | MINOR | SPEC | base | tests/test_model_endpoints.py:401-419 against :435-441 | The remark test pins that the `openai-codex` remark names the draft and no longer the spec review, but nothing checks the criterion's other half, that the remark still names the phase-6 review: the "and for the review (phase 6) ..." clause could be deleted and `_remark_problems` stays empty. Add the needle and a planted fault for it. | deepseek-v4.1-flash | fixed — not a test — a test-strength row: add the phase-6 needle and its planted fault to the remark test; the remark names phase 6 already, so the strengthened test is green on the baseline (bead coding-harness-y17) | no | agree |
| L1-7 | MAJOR | MAINT | base | docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md:140-146, scripts/stage2.py:2303-2320, :1741 | The residual-risk record says the put-back bounds "what git sees in the worktree — not an ignored file, not a path outside the worktree", but the repository's own git directory is a third case: `put_back` restores only `changed_paths`, and `git restore`/`git clean` never touch `.git`, so a `workspace-write` draft running in a plain checkout can leave `.git/hooks` or `.git/config` behind while `checkpoint`'s `git add`/`git commit` runs right after it; ADR 0016 and WORKFLOW §4 should name the git directory among what the put-back cannot bound. | deepseek-v4.1-flash | fixed — not a test — an incomplete statement of residual risk: the put-back does not bound the git directory either (hooks, config), and a commit runs right after the draft; ADR 0016 decision 8 and WORKFLOW §4 are to name it | no | agree |
| L2-1 | MAJOR | MAINT | base | scripts/stage2.py:629 (`producer_for`), called at :671 (`begin_work_call`) | A findings.md the runner must create itself now records the wrong program in its header. `begin_work_call` used to hard-code the producer `claude-code`; this change replaced that with `producer_for(endpoint)`, whose map holds only `openai-codex` and `claude-code-plan` and falls through to `pi` for every other endpoint. `implement` and `repair` on `glm-coding-plan` (the default GLM Flash and GLM 5.3 routes) therefore write `produced_by: … name: pi` into a governance file Claude Code wrote, contradicting the function's own docstring that the producer names the program; criterion 29 pins only the spec-review case, and the test that used to create such a header now drives `spec-review`, so nothing sees it. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_findings_file_an_implement_run_creates_names_claude_code | no | agree |
| L2-2 | MAJOR | MAINT | maintainer-trip | docs/WORKFLOW.md:407–439 (§3 "Model routing": rows 2, 2b, 3 at 413/415/416; the paragraph at 423–429; the "by hand" paragraph at 434) | §3 now contradicts itself about what drafts a spec. The table names `gpt-6.1-sol` as the model of phases 2, 2b and 3, while the paragraph directly below still says "Where stage 2 applies (§4), five rows leave this table: where the runner drafts, Codex writes spec, design and plan instead" and "the rows above stay what runs wherever the runner does not start a phase", and the next paragraph calls spec and plan on Opus 5.5 by hand "the default". Every other row of that table holds the model that runs when the runner does not start the phase (row 1 Haiku 4.5, row 4 Sonnet 5.5, row 6 Opus 5.5), so these three rows invert the table's own convention: "instead" has no antecedent, Codex never runs without the runner, and a maintainer drafting a spike's spec by hand is told Codex by the table and Opus 5.5 by the prose. | mimo-v2.6-flash | fixed — not a test — §3's rows 2, 2b and 3 keep Opus 5.5 at effort `xhigh` and say "where the runner drafts (§4), `gpt-6.1-sol` at effort `max` writes it instead", as rows 1 and 4 do; the paragraph below and the by-hand paragraph no longer contradict them | no | agree |
| L2-3 | MINOR | MAINT | maintainer-trip | docs/WORKFLOW.md:449–451 (§3, "Spec review on Opus 5.5 for every change since ADR 0016") and :593–595 (§4 opening) | Two clauses the change made false are left in the doctrine. The cost note still reads "the spec review reads with the same model as the spec's author (Opus 5.5), so what stays independent is the fresh context, not the error profile", but under this change the author of every routed spec is Codex or GLM 5.3 while the paragraph claims the routing for every change, so the sentence denies exactly the error-profile independence ADR 0016's driver "No model reviews its own draft" was bought for. §4 likewise introduces Opus 5.5 as "the model that writes the framework" in the same sentence that says Codex drafted the artefacts it reads. | mimo-v2.6-flash | fixed — not a test — the cost note now says the routed spec's author is Codex or GLM 5.3 and the review reads another vendor's error profile, and §4's opening introduces Opus 5.5 as the spec reviewer, not as the model that writes the framework | no | agree |
| L2-4 | MAJOR | SPEC | promised-not-done | scripts/stage2.py:2512–2521 (draft's failed-call branch) against the scan at :2523; spec criterion 25 | The GLM key can be left in the tree when the GLM draft call fails. The only `remove_changed_credential` scan on the success path sits after the early `continue` that handles a failed call, and that branch's put-back deliberately keeps findings.md, so a `glm-5.3` attempt that writes the key (whole or as an eight-character fragment) into findings.md and then exits non-zero or answers empty leaves it in a tracked file and the run ends with exit 1 — while criterion 25 requires the runner to remove it and refuse with exit 2. Its test drives only a call that succeeds, and `implement` cannot hit this because a failed call there restores findings from a snapshot and ends the run. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_failed_glm_draft_call_that_writes_the_key_is_refused | no | agree |
| L2-5 | MINOR | SPEC | promised-not-done | scripts/stage2.py:2518 and :2538 (the two put-back blocks), against `attempt_files` at :1511; `ATTEMPT_FILES = 40` at :247 | The record of what the runner put back stops at 40 paths in silence. Both blocks print `put[:ATTEMPT_FILES]` with no remainder line, so path 41 and on are restored without ever being named, while the sibling helper `attempt_files` bounds the same kind of list and appends "… and N more files" — the omission reads as an oversight. Criterion 8 says findings.md names each path the runner put back, and those blocks are the only record of what an unattended writing call had undone. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_the_put_back_names_its_remainder_beyond_the_bound | no | agree |
| L2-6 | MINOR | MAINT | base | AGENTS.md:35 (the stage-2 paragraph's last sentence), pinned by tests/test_stage2.py:5594 (`repair_doctrine_problems`) and :5617 | Adding draft to the list of verbs reviews do not route cost repair its place in it: the sentence now reads "Reviews go by class; explore, draft and implement do not", where the previous wording was "explore, implement and repair do not". Repair is still a work verb whose model comes from the routing table and not from the change's class, so a reader must now infer that it too escapes class routing — and the test's own error message was rewritten from "does not count repair among the verbs without reviews by class" to "does not count draft", so no test can notice the loss. | mimo-v2.6-flash | fixed — not a test — AGENTS.md reads "explore, draft, implement and repair do not" and `repair_doctrine_problems` requires both repair and draft among the verbs without reviews by class | no | agree |
| L3-1 | MAJOR | SPEC | base | `scripts/stage2.py`, `DRAFT_RULES` vs `draft_keep` | The drafting rules sent to the drafter say "Change nothing else: the runner puts back every other path git sees as changed", but `draft_keep` keeps and commits every changed path under `plans/changes/<change>/` except `decisions.md` — so an edit or deletion of `research.md`, a rewritten `findings.md`, or a stray new file inside the change folder is neither put back nor named, and reaches the one commit. The prompt promises a bound the runner does not enforce; no test covers an in-folder stray or deletion. | mimo-v2.6-pro | fixed — not a test — a false statement: the runner keeps changes inside the change folder by design (maintainer answer Q-3: changes only inside the change folder plus an ADR draft), so DRAFT_RULES is to say that it puts back every changed path outside the change folder except one new ADR draft, and decisions.md, rather than "every other path" | no | agree |
| L3-2 | MAJOR | SPEC | base | `scripts/stage2.py`, `draft()`, the `head_now != baseline` raise before `remove_changed_credential` | The moved-HEAD stop runs before any credential scan, so a GLM attempt that both writes the GLM key into a changed file and moves HEAD leaves the key in the tree and in the model's commit, while criterion 25 promises the runner "removes it and refuses". The refusal text ("nothing was put back or committed") also reports no removal and no `findings.md` record of the exposure. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_a_glm_draft_that_writes_the_key_and_moves_head_still_refuses | no | agree |
| L3-3 | MAJOR | MAINT | base | `scripts/stage2.py`, `draft()` pre-existing-change check vs `prepare_derived`; `tests/test_stage2.py`, `clear_derived_leftovers` | After a failed `draft` run the runner's own writes — the rendered `plans/INDEX.md` and the `updated:` stamps — stay in the worktree, and the next `draft` invocation refuses them ("pre-existing changes outside this change's findings.md"), although the doctrine prescribes a second `draft <change>` after the spec review and says nothing about cleaning or committing the runner's leftovers first. The tests paper over exactly this (`clear_derived_leftovers`, "the next run would refuse it"); a maintainer retrying a failed draft hits the refusal on files they never touched. | mimo-v2.6-pro | rejected — out of this change's scope: implement and repair share the same pre-existing-change check after a failed run, so the fix belongs to the runner as a whole (bead coding-harness-b5w) |  | disagree — The prescribed second draft follows a successful, committed first draft. Failed post-run checks intentionally retain their tree under criterion 21; a fresh invocation refusing those changes conforms to criterion 5. |
| L3-4 | MINOR | MAINT | base | `scripts/stage2.py`, `verify_draft` | When `plan.md` is missing, the check reports three problems for one root cause — the missing file, "`plan.md` does not open with the plan card" and "has no `## Time used` heading" — the last two read from an empty string via `_read_quietly`, so the quoted block names two faults the absent file cannot have. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_a_missing_plan_md_is_reported_once | no | disagree — The missing file already causes the correct rejection. Consolidating the additional diagnostics does not address a correctness fault, a spec gap or an ineffective gate. |

Rounds run: 3

Stage-2 call, 2026-10-13: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 385 files, 968 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route glm · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 385 files, 969 commits, 12 rules.

> Attempt 1 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +79 -39
> - `tests/test_stage2.py` +132 -5
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: repair · attempt 2 · route glm-repair · endpoint glm-coding-plan · model glm-5.3 · reason first GLM 5.3 post-run check failed · leak check clean over 385 files, 969 commits, 12 rules.

> Attempt 2 (glm-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two GLM 5.3 post-run checks failed · leak check clean over 385 files, 969 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/codex-drafts/plan.md` +7 -0
>
> Diagnostics:
> ```text
> - F-6: tests/test_stage2.py::test_only_the_changes_own_missing_adr_answer_is_tolerated: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> ```
