---
title: "Findings — loop-state-block"
category: findings
status: draft
implementation_status: none
date: 2026-10-23
created: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-i70
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — loop-state-block

Stage-2 call, 2026-10-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 533 files, 1922 commits, 12 rules.

Stage-2 call, 2026-10-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 536 files, 1923 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1924 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/loop-state-block/plan.md` +7 -0
> - `scripts/stage2.py` +36 -14
> - `tests/test_stage2.py` +140 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-6: tests/test_stage2.py::test_owned_snapshot_stray_end_marker_refuses: the call of `tests/test_stage2.py::test_owned_snapshot_stray_end_marker_refuses[before]` failed with Failed, not an AssertionError
> ```

Stage-2 call, 2026-10-24: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1924 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +5 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 29 lines of this gate left out …]
> ........................................................................ [ 76%]
> ........................................................................ [ 79%]
> ........................................................................ [ 82%]
> ........................................................................ [ 85%]
> ........................................................................ [ 88%]
> ........................................................................ [ 90%]
> ........................................................................ [ 93%]
> ........................................................................ [ 96%]
> ........................................................................ [ 99%]
> ..............                                                           [100%]
> =================================== FAILURES ===================================
> ______ test_snapshot_resume_preserves_membership_consumption_and_metadata ______
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/loop-state-block/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1274/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1274/popen-gw0/test_snapshot_resume_preserves0/state'))
>
>     def test_snapshot_resume_preserves_membership_consumption_and_metadata(world: World) -> None:
>         """Criterion 4: a released snapshot survives until the runner's next legitimate state transition."""
>         world.script(pi=[{"model": model, "stdout": rows(1)} for model in TEST_FREE])
>         assert world.run("review-loop") == 0
>         decide_record(world)
>         world.write_findings(VERDICT)
>         assert world.run("release-loop") == 0
>         released_block = owned_blocks(world.text())[0]
>         state = stage2.read_state(None, world.text())
>         assert state["consumed"] == ["free"]
>         # the configuration changes after the release: the frozen members stay, nothing is rediscovered
>         pin_entry(world.root / "model-endpoints.yaml", ("moved-rung", "deepseek-v4.1-flash", "mimo-v2.6-flash"))
>         (world.bin / "calls.jsonl").unlink()
>         world.script(pi=[{"model": model, "stdout": "No finding."} for model in TEST_FLASH])
>         assert world.run("review-loop") == 0
>         assert not [call for call in world.calls("pi") if call.get("kind")], "the resume rediscovered the catalog"
> >       assert [rung_of(call) for call in world.reviews("pi")] == list(TEST_FLASH), "the frozen swarm was replayed or moved"
> E       AssertionError: the frozen swarm was replayed or moved
> E       assert ['mimo-v2.6-f...k-v4.1-flash'] == ['deepseek-v4...o-v2.6-flash']
> E         
> E         At index 0 diff: 'mimo-v2.6-flash' != 'deepseek-v4.1-flash'
> E         Use -v to get more diff
>
> tests/test_stage2.py:1289: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 1 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1274/popen-gw0/test_snapshot_resume_preserves0/state/coding-harness/stage2/demo@bf1f7e86/loop.md: 2 rows from 2 of 2 members
> release-loop: 2 loop rows appended to plans/changes/demo/findings.md
> INFO  (1):
>   - leak check clean: 23 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 23 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 2 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1274/popen-gw0/test_snapshot_resume_preserves0/state/coding-harness/stage2/demo@bf1f7e86/loop.md: 0 rows from 2 of 2 members
> ----------------------------- Captured stderr call -----------------------------
> review-loop: Notice: no anfragen_5h declared, ordered last: mimo-v2.6-pro.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_snapshot_resume_preserves_membership_consumption_and_metadata
> 1 failed, 2517 passed, 16 skipped in 178.26s (0:02:58)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 13199 earlier lines left out …]
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

Stage-2 call, 2026-10-24: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1924 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1925 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1925 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1925 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1925 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1926 commits, 12 rules.
