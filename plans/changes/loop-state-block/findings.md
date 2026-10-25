---
title: "Findings — loop-state-block"
category: findings
status: draft
implementation_status: partial
date: 2026-10-23
created: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-25
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

## Repair of loop rows L3-1 and L3-5 outside the runner, 2026-10-25

On 2026-10-25 the maintainer took rows L3-1 and L3-5 of round 3 in the
conversation with a Claude Code cloud session, and told it to repair them
with a Sonnet 5.5 subagent instead of Codex. Codex is not reachable from
that container, so `stage2.py repair` could not run. This deviates from
ADR 0017, which has Codex repair through the runner. The rows themselves
stand in the loop record on the maintainer's machine, not in this file.

- **L3-1 (MAJOR), fixed.** `read_state` now refuses, naming the place and
  the field, a snapshot whose `free.selected`, `paid.ladder`, `paid.flash`,
  `paid.rungs` or `consumed` is not a list of strings. These are the inner
  fields the runner reads without a default. Before, such a block crashed
  with a `KeyError` or `TypeError` traceback. Tests:
  `tests/test_stage2.py::test_a_snapshot_without_its_membership_fields_is_refused_not_a_traceback`
  and `::test_a_state_free_dict_is_the_literal_reproduction_of_l3_1`; both
  failed on `d3e48c3` and pass after the fix.
- **L3-5 (MINOR), fixed.** `review` (phase 6) calls `read_state` with
  `legacy_release_ok=True`. Without a loop record, a release that keeps a
  bare legacy state line and no owned block then reads as no snapshot,
  instead of refusing the phase-6 re-check of a change released before the
  owned block existed. A present but broken owned block still refuses, and
  `review-loop` and `release-loop` are unchanged. Tests:
  `::test_review_proceeds_when_the_last_release_keeps_a_legacy_bare_state_line`
  (failed on `d3e48c3`, passes after) and
  `::test_review_with_a_record_still_refuses_a_missing_owned_block`. The
  case `review` over a legacy release left the parametrisation of
  `::test_invalid_owned_snapshot_refuses_without_calls_or_writes` and
  `::test_review_invalid_owned_snapshot_refuses_before_call`, because it
  asserted the behaviour L3-5 removes.
- Two fixtures that used the degenerate snapshot
  `{"consumed": ["free"], "free": {}, "paid": {}}` now use a complete one;
  the stricter check rightly refuses the old one.
- **L3-2 to L3-4 stay open**: the maintainer has not decided them.

The loop record still lists L3-1 and L3-5 as open. Marking them taken and
fixed there is the maintainer's step on their machine.

## L3-2 and L3-3, worked by the orchestrator, 2026-10-25 (night run)

The maintainer answered on 2026-10-25: "search and repair yourself". The
wording of both rows was read from the loop record on the maintainer's
machine (`loop-state-block@8bc04613`), so the match with L3-2 and L3-3 is
certain. What was measured is not certain in the same way; see L3-2.

- **L3-3, fixed.** The last sentence of the `answer_parts` docstring said
  the phase-2a block keeps its unquoted contract. Both callers, phase 2a
  and phase 6, pass `quote=True`. The sentence now says so. No test: this
  is a docstring.
- **L3-2, partly refuted.** The row said the release in
  `test_phase6_forged_snapshot_cannot_steer_resume` keeps the runner's
  no-finding statement under the kept marker. Measured at `3b2f1a4` with a
  probe of the same steps: the release block carries the owned state
  block, the row table and `Rounds run: 1`, and no `Kept from the loop
  record:` line. So the docstring ("keeps no words of its own") matches the
  built release, and it stays unchanged. The second half of the row stands:
  the plan's verification names a phase-6 exercise after a release **with**
  kept evidence, and no test runs it. That exercise is still owed, and it
  goes to the repair verb with phase 6.
- Other docstrings this change touches were not re-read one by one.
