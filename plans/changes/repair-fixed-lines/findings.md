---
title: "Findings — repair-fixed-lines"
category: findings
status: draft
implementation_status: partial
date: 2026-10-15
created: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-ugi
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — repair-fixed-lines

Stage-2 call, 2026-10-15: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 459 files, 1277 commits, 12 rules.

Stage-2 call, 2026-10-15: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 462 files, 1279 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +8 -1
> - `plans/changes/repair-fixed-lines/plan.md` +13 -8
> - `scripts/stage2.py` +49 -12
> - `tests/test_stage2.py` +209 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 22 lines of this gate left out …]
> ........................................................................ [ 77%]
> ........................................................................ [ 81%]
> ........................................................................ [ 84%]
> ........................................................................ [ 87%]
> ........................................................................ [ 91%]
> ........................................................................ [ 94%]
> ........................................................................ [ 98%]
> ..........................................                               [100%]
> =================================== FAILURES ===================================
> _______________ test_repair_prose_alone_still_needs_fixed_lines ________________
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4552/test_rep...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4552/test_repair_prose_alone_still_0/state'))
>
>     def test_repair_prose_alone_still_needs_fixed_lines(world: World) -> None:
>         """Criterion 4. Planted fault: prose alone passes, or duplicates spaced by prose escape the count."""
>         repair_world(world)
>         prose = "\n".join(
>             [
>                 "## Report",
>                 "expected: all rows are repaired",
>                 "found: nothing left to fix",
>                 "Resume: when I start, I will look again",
>             ]
>         )
>         script_repair(world, [repair_step(stdout=prose), repair_step()], make=[{"stdout": "green\n"}] * 2)
>         assert world.run("repair") == 0
>         prompt = prompt_of(world.calls("codex")[1])
>         assert "L1-1: no fixed line" in prompt
>         assert "no fixed line: " not in prompt and "no taken row carries this id" not in prompt
>         world.write_record([("L1-1", "taken — test_a", "no")])
>         duplicated = "\n".join(
>             [
>                 "L1-1: fixed — tests/test_fix.py::test_fix",
>                 "expected: one line per row",
>                 "L1-1: fixed — tests/test_fix.py::test_fix",
>             ]
>         )
>         script_repair(world, [repair_step(stdout=duplicated), repair_step()], make=[{"stdout": "green\n"}] * 2)
> >       assert world.run("repair") == 0
> E       AssertionError: assert 1 == 0
> E        +  where 1 = run('repair')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4552/test_rep...var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4552/test_repair_prose_alone_still_0/state')).run
>
> tests/test_stage2.py:5643: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 2 commits, 1 rules, 1 prompt texts
> repair: verified and committed · route codex-repair · attempt 2
> INFO  (1):
>   - leak check clean: 26 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: codex call failed: no thread.started event; the worktree needed no restore.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_repair_prose_alone_still_needs_fixed_lines
> 1 failed, 2113 passed, 16 skipped in 470.98s (0:07:50)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 10596 earlier lines left out …]
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

Stage-2 call, 2026-10-16: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 462 files, 1279 commits, 12 rules.

Stage-2 call, 2026-10-16: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 462 files, 1280 commits, 12 rules.

Stage-2 call, 2026-10-16: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 462 files, 1281 commits, 12 rules.

Stage-2 call, 2026-10-16: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 462 files, 1282 commits, 12 rules.

Stage-2 call, 2026-10-16: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 462 files, 1284 commits, 12 rules.
