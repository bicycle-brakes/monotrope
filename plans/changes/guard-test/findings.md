---
title: "Findings — guard-test"
category: findings
status: draft
implementation_status: none
date: 2026-10-15
created: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — guard-test

Stage-2 call, 2026-10-15: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 441 files, 1260 commits, 12 rules.

Stage-2 call, 2026-10-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 462 files, 1310 commits, 12 rules.

Stage-2 call, 2026-10-16: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 462 files, 1312 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +4 -0
> - `decisions/gates.yaml` +9 -0
> - `docs/WORKFLOW.md` +23 -7
> - `docs/adr/0017-codex-repairs-taken-findings.md` +21 -1
> - `plans/changes/guard-test/plan.md` +24 -16
> - `prompts/04-implement.md` +8 -2
> - `prompts/04b-review-loop.md` +5 -1
> - `prompts/06-review.md` +9 -0
> - `scripts/check_guard_environment.py` +44 -0
> - `scripts/stage2.py` +164 -38
> - `templates/findings.md` +8 -1
> - `tests/test_guard_environment.py` +116 -0
> - `tests/test_stage2.py` +641 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/check_guard_environment.py`, `scripts/stage2.py`, `tests/test_stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 646 lines of this gate left out …]
> E        +  where 1 = run('repair')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4700/test_ord...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4700/test_ordinary_proofs_and_not_a0/state')).run
>
> tests/test_stage2.py:6686: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: codex call failed: no thread.started event; the runner restored the worktree to 030da65cd143 (undone: plans/INDEX.md, scripts/__pycache__/_verdict.cpython-312.pyc, src/app.py, tests/test_broken.py); rerun the verb or add --stage2-off.
> __ test_phase6_keeps_a_guard_evidence_line_per_test_with_or_without_findings ___
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4700/test_pha...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4700/test_phase6_keeps_a_guard_evid0/state'))
>
>     def test_phase6_keeps_a_guard_evidence_line_per_test_with_or_without_findings(world: World) -> None:
>         """Ledger 11. Planted fault: a guard evidence line lost, the effective prompt rows-only again, or
>         a private loop row in the verdict call."""
>         # Without findings, both lines survive the no-finding sentence.
>         world.script(codex=[codex_ok("T1", "No finding in the change.\n" + GUARD_LINES)])
>         assert world.run("review") == 0
>         for line in GUARD_LINES.splitlines():
>             assert line in world.text(), line
>         # With a finding row and a decided record: the lines stand beside the rows, the verdict prompt
>         # carries the evidence-line format, and the record's private rows reach no call before it.
>         world.write_record([("L1-1", "taken — test_a", "no")])
>         world.script(codex=[codex_ok("T2", rows(1) + "\n" + GUARD_LINES), codex_ok("T2", "L1-1: agree")])
> >       assert world.run("review") == 0
> E       AssertionError: assert 1 == 0
> E        +  where 1 = run('review')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4700/test_pha...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4700/test_phase6_keeps_a_guard_evid0/state')).run
>
> tests/test_stage2.py:6949: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 21 files, 1 commits, 1 rules, 1 prompt texts
> review: verdict appended to plans/changes/demo/findings.md; session codex T1
> INFO  (1):
>   - leak check clean: 22 files, 1 commits, 1 rules, 1 prompt texts
> review: verdict appended to plans/changes/demo/findings.md; session codex T2
> release-loop: 1 loop rows appended to plans/changes/demo/findings.md
> INFO  (1):
>   - leak check clean: 22 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: codex call failed: no thread.started event
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_guard_fixed_line_selects_guard_proof - As...
> FAILED tests/test_stage2.py::test_a_guard_planted_run_requires_exit_one_on_baseline_code[planted-green]
> FAILED tests/test_stage2.py::test_a_guard_planted_run_requires_exit_one_on_baseline_code[planted-collection-exit]
> FAILED tests/test_stage2.py::test_a_guard_planted_run_uses_the_baseline_code_not_the_repaired_tree
> FAILED tests/test_stage2.py::test_a_guard_requires_an_unplanted_green_run_without_an_ambient_switch
> FAILED tests/test_stage2.py::test_guard_startup_and_timeouts_fail_with_the_stage_named
> FAILED tests/test_stage2.py::test_guard_proofs_preserve_refs_and_clean_up_the_checkout
> FAILED tests/test_stage2.py::test_guard_statuses_survive_all_three_row_locations_only_after_success
> FAILED tests/test_stage2.py::test_ordinary_proofs_and_not_a_test_permissions_do_not_change_with_guard_support
> FAILED tests/test_stage2.py::test_phase6_keeps_a_guard_evidence_line_per_test_with_or_without_findings
> 10 failed, 2116 passed, 16 skipped in 655.37s (0:10:55)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 10695 earlier lines left out …]
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

Stage-2 call, 2026-10-16: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 464 files, 1321 commits, 12 rules.

Stage-2 call, 2026-10-16: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Z.ai 5-hour GLM budget used up (maintainer, 2026-10-16) · leak check clean over 462 files, 1327 commits, 12 rules.
