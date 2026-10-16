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

Stage-2 call, 2026-10-16: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 462 files, 1286 commits, 12 rules.

Stage-2 call, 2026-10-16: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 462 files, 1287 commits, 12 rules.

Stage-2 call, 2026-10-16: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 462 files, 1289 commits, 12 rules.

## Phase 6 — Opus 5.5, 2026-10-16

Phase 6 verdict: Opus 5.5 sub-agent, 2026-10-16

Orchestrator's decision on each row below (2026-10-16): the BLOCKER is taken; the three MINOR rows are taken because they concern tests and a false statement in the refusal's advice; the STYLE row is rejected as an accepted limit. Each taken row names the criterion or test the repair must satisfy. The review text itself is committed unchanged in the next section.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | TEST | impl | `tests/test_stage2.py:5761-5771` (`test_repair_instructions_describe_answer_filtering_and_hand_repairs`, workflow half) against `docs/WORKFLOW.md:1107-1110` and spec criterion 9 | Criterion 9 is refuted by "the workflow leaves a hand repair in a `taken` status or omits its `Broke a test` mark". The test's workflow needles `fixed — tests/<path>::<function>`, `fixed — not a test — <reason>` and `Broke a test` all already appear in the section on `origin/main` (135f029), in the answer-form sentence and in "`Broke a test` stays the orchestrator's mark". Only the three legacy-marker needles are new. Planted in a scratch copy: (a) deleting the whole hand-repair sentence ("A hand repair books itself … from the evidence."), (b) rewriting "replace the finished row's `taken — …`" as "append to the finished row's `taken — …`", (c) dropping "`Broke a test`" from the mark. The test stays green in all three cases. Repair: pin text that is unique to the new rule, such as "replace the finished row's" and "set the loop row's `Broke a test` mark", and check that each planted fault turns it red. | Opus 5.5 | fixed — tests/test_stage2.py::test_repair_instructions_describe_answer_filtering_and_hand_repairs |  |
| F-2 | MINOR | SPEC | impl | `scripts/stage2.py:1078-1081` (`legacy_completed`) and the refusal at `scripts/stage2.py:3030-3039` | `legacy_completed` matches a marker anywhere in the Status, including quoted text. A scratch probe confirms the orchestrator's observation: a record row `taken — test_a — the docs must name \`; repaired by\` too` (taken, not repaired) is refused before any call (exit 2, zero stand-in calls). Decisions addendum 1 accepts that a false match "costs one rewrite, not a lost repair". The refusal text does not hold to that: it tells the operator to "book the hand repair by replacing the Status with `fixed — …`". Followed as written for a row that was never repaired, that instruction marks the row fixed, and the repair is lost. The doctrine sentence at `docs/WORKFLOW.md:1110-1113` does not mention the false match either. The trap is most likely in changes that discuss these markers, as this one did. Repair, either way: leave backtick spans out of the match, or make the refusal say "if the row is not repaired yet, reword its reason so it names no fix". Add a test for each. | Opus 5.5 | fixed — tests/test_stage2.py::test_repair_accepts_quoted_legacy_markers |  |
| F-3 | MINOR | SPEC | loop | `scripts/stage2.py:2257-2271` (the claimed-fix clause `rest.startswith("fixed — ")`) against spec Terms "Claimed fix" and criterion 3 | The claimed-fix rule only reads an undecorated right side. Two scratch probes, each beside a valid `custom: fixed — tests/test_fix.py::test_fix`: `**custm:** fixed — tests/test_fix.py::test_fix` (bold that wraps the colon, so `rest` starts with `** fixed`) and ``custm: `fixed — tests/test_fix.py::test_fix` ``. Each checkpointed after one Codex call with one commit. That is criterion 3's own refuted case ("`custm: fixed …` beside a valid `custom:` line is ignored and checkpointed") in the bold form the Terms say stays supported. The escape needs mixed decoration, because a decorated right side also fails the real row's line (that part is old behaviour, already on `main`). Repair: strip `*` and backticks from the start of `rest` before the claimed-fix test, or test for `fixed —` after decoration is stripped. Add a parameter case to `test_repair_rejects_unknown_claimed_fixes`. | Opus 5.5 | fixed — tests/test_stage2.py::test_repair_rejects_unknown_claimed_fixes |  |
| F-4 | MINOR | TEST | loop | `scripts/stage2.py:2267-2268` (`ident not in active`, `not LOOP_ID.fullmatch(ident)`); `tests/test_stage2.py:5592`, `:5611` | No test pins two branches of the new filter; the suite stays green when either is deleted. (1) Removing `ident not in active` keeps `test_repair_accepts_exact_free_text_identifiers` green: the claimed-fix clause masks it. The clause matters only for a malformed free-text line (`custom: done`), which then gives "custom: no fixed line" instead of the malformed-status diagnostic criterion 5 asks for. Criterion 5's test uses `L1-1` only. (2) Removing the `LOOP_ID` clause keeps `test_repair_rejects_unknown_finding_shaped_identifiers` green: its `L9-9` line has a fixed right side, and its change has a loop row, so the prefix `L` masks it. The case the clause exists for, `L9-9: see below` in a change with only phase-6 rows, is untested; a probe shows the code handles it correctly today. (3) Criterion 2's refuted-by names `expected` as a phase-6 id, but its test uses only `custom`. A stop-list fault that ignores `expected` keeps that test green and is caught only by a criterion-3 case. Repair: add the three cases. | Opus 5.5 | fixed — tests/test_stage2.py::test_repair_rejects_malformed_known_fixed_lines |  |
| F-5 | STYLE | DOC | loop | `docs/WORKFLOW.md:1113-1114` | The rewrap (row L2-4) leaves the ragged short line "test alone against the baseline's code, in a" before the old text resumes. Lines stay within 80 columns. | Opus 5.5 | rejected — STYLE, accepted limit: the lines stay within 80 columns; named in the pull request | |

## Opus 5.5 review text, phase 6, 2026-10-16

Review text as returned by the Opus 5.5 reviewer (committed unchanged; the harness's two-space indentation of the hand-back removed, nothing else changed). Its own table repeats the rows above with empty Status cells; the decided rows are the ones above.

Open BLOCKER: yes — BLOCKER 1 · DIVERGENT 0 · MAJOR 0 · MINOR 3 · STYLE 1 (review of explore/repair-fixed-lines at b508152, 2026-10-16)

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | TEST | impl | `tests/test_stage2.py:5761-5771` (`test_repair_instructions_describe_answer_filtering_and_hand_repairs`, workflow half) against `docs/WORKFLOW.md:1107-1110` and spec criterion 9 | Criterion 9 is refuted by "the workflow leaves a hand repair in a `taken` status or omits its `Broke a test` mark". The test's workflow needles `fixed — tests/<path>::<function>`, `fixed — not a test — <reason>` and `Broke a test` all already appear in the section on `origin/main` (135f029), in the answer-form sentence and in "`Broke a test` stays the orchestrator's mark". Only the three legacy-marker needles are new. Planted in a scratch copy: (a) deleting the whole hand-repair sentence ("A hand repair books itself … from the evidence."), (b) rewriting "replace the finished row's `taken — …`" as "append to the finished row's `taken — …`", (c) dropping "`Broke a test`" from the mark. The test stays green in all three cases. Repair: pin text that is unique to the new rule, such as "replace the finished row's" and "set the loop row's `Broke a test` mark", and check that each planted fault turns it red. | Opus 5.5 | | |
| F-2 | MINOR | SPEC | impl | `scripts/stage2.py:1078-1081` (`legacy_completed`) and the refusal at `scripts/stage2.py:3030-3039` | `legacy_completed` matches a marker anywhere in the Status, including quoted text. A scratch probe confirms the orchestrator's observation: a record row `taken — test_a — the docs must name \`; repaired by\` too` (taken, not repaired) is refused before any call (exit 2, zero stand-in calls). Decisions addendum 1 accepts that a false match "costs one rewrite, not a lost repair". The refusal text does not hold to that: it tells the operator to "book the hand repair by replacing the Status with `fixed — …`". Followed as written for a row that was never repaired, that instruction marks the row fixed, and the repair is lost. The doctrine sentence at `docs/WORKFLOW.md:1110-1113` does not mention the false match either. The trap is most likely in changes that discuss these markers, as this one did. Repair, either way: leave backtick spans out of the match, or make the refusal say "if the row is not repaired yet, reword its reason so it names no fix". Add a test for each. | Opus 5.5 | | |
| F-3 | MINOR | SPEC | loop | `scripts/stage2.py:2257-2271` (the claimed-fix clause `rest.startswith("fixed — ")`) against spec Terms "Claimed fix" and criterion 3 | The claimed-fix rule only reads an undecorated right side. Two scratch probes, each beside a valid `custom: fixed — tests/test_fix.py::test_fix`: `**custm:** fixed — tests/test_fix.py::test_fix` (bold that wraps the colon, so `rest` starts with `** fixed`) and ``custm: `fixed — tests/test_fix.py::test_fix` ``. Each checkpointed after one Codex call with one commit. That is criterion 3's own refuted case ("`custm: fixed …` beside a valid `custom:` line is ignored and checkpointed") in the bold form the Terms say stays supported. The escape needs mixed decoration, because a decorated right side also fails the real row's line (that part is old behaviour, already on `main`). Repair: strip `*` and backticks from the start of `rest` before the claimed-fix test, or test for `fixed —` after decoration is stripped. Add a parameter case to `test_repair_rejects_unknown_claimed_fixes`. | Opus 5.5 | | |
| F-4 | MINOR | TEST | loop | `scripts/stage2.py:2267-2268` (`ident not in active`, `not LOOP_ID.fullmatch(ident)`); `tests/test_stage2.py:5592`, `:5611` | No test pins two branches of the new filter; the suite stays green when either is deleted. (1) Removing `ident not in active` keeps `test_repair_accepts_exact_free_text_identifiers` green: the claimed-fix clause masks it. The clause matters only for a malformed free-text line (`custom: done`), which then gives "custom: no fixed line" instead of the malformed-status diagnostic criterion 5 asks for. Criterion 5's test uses `L1-1` only. (2) Removing the `LOOP_ID` clause keeps `test_repair_rejects_unknown_finding_shaped_identifiers` green: its `L9-9` line has a fixed right side, and its change has a loop row, so the prefix `L` masks it. The case the clause exists for, `L9-9: see below` in a change with only phase-6 rows, is untested; a probe shows the code handles it correctly today. (3) Criterion 2's refuted-by names `expected` as a phase-6 id, but its test uses only `custom`. A stop-list fault that ignores `expected` keeps that test green and is caught only by a criterion-3 case. Repair: add the three cases. | Opus 5.5 | | |
| F-5 | STYLE | DOC | loop | `docs/WORKFLOW.md:1113-1114` | The rewrap (row L2-4) leaves the ragged short line "test alone against the baseline's code, in a" before the old text resumes. Lines stay within 80 columns. | Opus 5.5 | | |

## Check 1 — criteria and planted faults

Method: each fault was planted in the scratch copy `ugi-p6`, the named test was run, and the copy was restored. Driver: `scratchpad/ugi-mut.py`. Before planting, the whole of `tests/test_stage2.py` in the scratch copy at b508152: 535 passed (2026-10-16).

- **1** — `test_repair_ignores_incidental_answer_prose` and `test_repair_ignores_l_prefix_prose_without_loop_rows`; the ADR/UTF-8 half sits in `test_repair_rejects_unknown_finding_shaped_identifiers`.
  - Lines without a colon fail again: red.
  - Filter removed, so every colon line counts: red.
  - Shape alone counts, without the prefix check: red.
  - `L` always in the prefix set: red.
- **2** — `test_repair_accepts_exact_free_text_identifiers`.
  - Reverted to the shape-only filter (no exact match, no claimed-fix rule): red.
  - Only `ident not in active` removed: green, masked (F-4).
  - Stop-list that ignores `expected`: green for this test, red in the criterion-3 test (F-4).
- **3** — `test_repair_rejects_unknown_finding_shaped_identifiers` and `test_repair_rejects_unknown_claimed_fixes`.
  - Leftover ids no longer reported: red.
  - Claimed-fix clause removed: red.
  - Prefix clause removed: red.
  - `LOOP_ID` clause removed: green, masked (F-4).
  - Decorated claimed fix: escapes, probe only (F-3).
- **4** — `test_repair_prose_alone_still_needs_fixed_lines` and `test_each_taken_row_needs_exactly_one_fixed_line`.
  - Missing line accepted: red.
  - Duplicate lines accepted: red.
- **5** — `test_repair_rejects_malformed_known_fixed_lines`.
  - Malformed status on a known id discarded as prose: red.
- **6** — `test_repair_skips_canonical_hand_repairs_in_every_location`.
  - A fixed row taken again, planted separately in the record, the released block and the phase-6 table: red each time.
  - Note: the test covers 3 of the 6 combinations of status form and location. A contrived fault that re-takes only phase-6 `fixed — not a test` rows stays green. The code uses `startswith("fixed")`, so this is not filed as a row.
- **7** — `test_repair_refuses_legacy_completed_taken_statuses_before_call`.
  - Each marker removed from `LEGACY_FIXED`, one at a time: red ×3.
  - Case-sensitive match: red.
  - Check only on record rows: red.
  - Rows silently skipped: red.
  - Refusal without the corrective forms: red.
  - Refusal without the `Broke a test` mark: red.
  - Any mention of "fix" counts as a marker: red, through the control.
- **8** — four existing tests (planted faults below); red-first was not mutated.
  - `test_a_fixed_line_naming_an_undefined_test_fails_the_attempt`, def check removed: red.
  - `test_a_fixed_line_whose_test_path_climbs_out_of_tests_fails_the_attempt`, `..` check removed: red.
  - `test_a_code_row_answered_not_a_test_fails_the_attempt`, code-row check removed: red.
  - `test_a_named_test_that_is_not_red_first_fails_the_attempt` was run unmutated (green) and is unchanged on this branch.
- **9** — `test_repair_instructions_describe_answer_filtering_and_hand_repairs`.
  - Prompt says "no other text" again: red.
  - `; repaired by` removed from the prompt: red.
  - **Hand-repair sentence removed from the workflow, `taken` wording planted, or `Broke a test` mark removed: green → F-1 (BLOCKER).**

## Check 2 — soft passes

- The criterion-9 workflow needles were already true before this change (F-1).
- The `L9-9` line in the criterion-3 test is caught twice over: by the claimed-fix rule and by the loop prefix. So it does not prove the `LOOP_ID` branch (F-4).
- No `or` chains that accept the wrong outcome, and no assertions loosened to match output.
- Absence checks such as `"no fixed line: " not in prompt` target the old no-colon message correctly.
- Every new test reaches `check_repair_answer` or `repair` through the runner stand-ins. `world.calls()` also logs `make`, so `== []` really means "no model call and no `make verify`".

## Check 3 — parser edges

Each item was probed in the scratch copy unless it says "read".

- Bullet, bold-on-id (`- **custm**: …`) and backtick-on-id are handled. Bold or backticks that reach the right side defeat the claimed-fix rule (F-3).
- An exact free-text active id is accepted (`custom`). `expected` as an active id works through the code path but its criterion-2 case is not pinned (F-4).
- `L<n>-<m>` always counts, including `L9-9: see below` with only phase-6 rows (probe: fails correctly).
- `L-3` counts only beside a loop row: tested both ways.
- `ADR-0017:`, `UTF-8:` and `OTHER-3:` stay prose: tested.
- `f-999:` stays prose when rows are `F-<n>` (prefix match is case-sensitive). Acceptable as prose.
- The prefix set takes rows from taken rows, every released row and every phase-6 row (any status), and the loop record outside `findings.md` (read). Record and released rows are always `L<n>-<m>`. Their only effect is to add `L`, which row L3-3 needs, so including the record matters and is correct.
- Duplicate and missing lines are caught. A duplicate spelled two ways (`L1-1:` and `**L1-1**:`) still folds to one id (read).

## Check 4 — pre-call refusal

- All three markers are matched case-insensitively, in all three row locations, in one test.
- The refusal comes after `preflight` and after the waiting and doubled-id refusals, and before `time_log`, `read_secret`, any model call or `make`: zero stand-in calls; `read_secret` is monkeypatched to fail and stays untouched.
- Rows are left unchanged (asserted for the record, the released block and phase 6).
- The message names the row ids, both canonical forms and the `Broke a test` mark.
- A control reason with ordinary semicolons repairs normally.
- False match: a marker inside quoted text, such as the orchestrator's L3-2 Status, stops a legitimate repair. The orchestrator's observation is confirmed by the probe. Severity is MINOR: the refusal costs no call, but its advice can lose a repair (F-2).

## Check 5 — doctrine

- `REPAIR_ANSWER`, the `check_repair_answer` and `repair` docstrings, and `docs/WORKFLOW.md` §4 agree with the code on every point:
  - prose is ignored;
  - a shaped or claimed unknown id fails;
  - the prefix set includes rejected and fixed rows;
  - `L` counts only beside a loop row;
  - the three legacy markers refuse before any call;
  - a hand repair is booked in Status, with its `Broke a test` mark.
- What none of them says: a marker inside quoted text also counts (F-2).
- Ruff check and ruff format check pass on both files in the scratch copy.

## Check 6 — scope

- The diff touches only these paths: `scripts/stage2.py`, `tests/test_stage2.py`, `docs/WORKFLOW.md`, `plans/INDEX.md` (regenerated rows for this change), and this change's folder (`plans/changes/repair-fixed-lines/`).
- Untouched: other change folders, ADRs, `.beads/`, `.claude/settings.json`, gates, prompts, `AGENTS.md`.
- Non-goals are unbuilt: no migration, no new status, routes unchanged.
- `research.md` holds the runner's explore answer with its chat wrapper ("ready to append", "Needed from you"). `haiku-5-5` and `pi-pin` research files carry the same wrapper, so it is runner convention on `main` and not filed against this change.

## Check 7 — secrets

- A grep of the diff for key, token, secret, bearer, password, `sk-`, `ghp_` and `auth.json` finds only the `read_secret` monkeypatch in the criterion-7 test. No credential text.
- No credential file was read.

## Not read

- `make verify`: not run, by the brief.
- The full suite outside `tests/test_stage2.py`: not run.
- `origin` was not fetched; `origin/main` was read as it stands locally (135f029, the branch's merge base).
- The exact original round-3 Status of L3-2 before it was rewritten: not read. The loop record now shows only `fixed — …`, so the false match was reproduced with an equivalent probe string.
- `plans/changes/stage2-repair/spec.md` criterion 15: not read directly, taken as quoted in decisions and loop rows.
- The red-first mutation for criterion 8 was not planted.
- Side note: before I swapped the scratch copy's `.git` pointer for its own repository, one `git status` in the scratch copy ran against the worktree's gitdir. That may have refreshed its stat cache; content is unaffected. The worktree is clean afterwards, HEAD b508152.

Resume: commit this review text unchanged as the phase-6 table in `findings.md`, take F-1 (BLOCKER; pin wording unique to the hand-repair rule and confirm the three planted workflow faults go red) and repair F-2 to F-4 (MINOR test or false-statement rows) and decide F-5, then re-run phase 6 at the new head.

## Phase 4b — loop rows, released 2026-10-16

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | SPEC | base | `plans/changes/repair-fixed-lines/spec.md:4` and the same field in `decisions.md`, `findings.md`, `plan.md` and `research.md`, with their rows at `plans/INDEX.md:164-168` | Every artefact of this change still declares `implementation_status: none` and the regenerated index prints `none` beside all five rows, although the branch already carries the implemented parser, the pre-call refusal and their tests; `plans/_README.md:50` and `docs/WORKFLOW.md:312-315` define the field as moving when the code moves, sibling in-flight changes with built code read `partial`, and the plan's own file list promises the spec "later the implementation status" — a maintainer scanning the index reads that no code exists where the code is. | deepseek-v4.1-flash | fixed — not a test — set implementation_status to partial in all five artifacts and regenerated plans/INDEX.md | no | — |
| L1-2 | MAJOR | SPEC | promised-not-done | `scripts/stage2.py:1073` (`LEGACY_FIXED`) against `plans/changes/haiku-5-5/findings.md:51` and `plans/changes/repair-fixed-lines/spec.md:99` | The recorded Haiku repair failure was row L1-1, whose Status reads `taken — not a test — metadata: …; repaired by the orchestrating session`, but the refusal recognises only `; fixed by` and `; fixed:`, so a record whose hand repair uses that form is still sent to the model and fails with `L1-1: no fixed line` — the failure the change exists to end; the spec's non-goal excludes `; repaired by …` on purpose, so the fix covers the Pi-pin form and the prose reads but leaves the Haiku row its own research cites. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_repair_refuses_legacy_completed_taken_statuses_before_call | no | — |
| L1-3 | MINOR | MAINT | impl | `scripts/stage2.py:311` (`FINDING_ID`) against the promise at `scripts/stage2.py:223` and `docs/WORKFLOW.md:1099-1101` | The filter treats any colon line whose left side is ASCII letters, a hyphen and digits as a finding id, so report text that mentions a non-taken row or an ordinary token — `F-3: already rejected`, `ADR-0017: …`, `UTF-8: …` — fails the attempt with `no taken row carries this id` after `make verify` has passed, although the prompt and the workflow name only row ids (`L1-2`, `F-12`) as the failing shape and promise that report prose is ignored; the retry is the class of spurious failure the change set out to remove. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_repair_rejects_unknown_finding_shaped_identifiers | no | — |
| L2-1 | MAJOR | SPEC | promised-not-done | `plans/changes/repair-fixed-lines/spec.md:116` (Definition of Done) against `plans/changes/repair-fixed-lines/plan.md`, "Time used" | The Definition of Done's first bullet promises "`make verify` is green, with parser and pre-call refusal regression evidence", but every verify result recorded in the change is red: plan.md's verification section states "`make verify`: exit 2, not green … 14 failed, 2086 passed, 17 skipped and 15 errors" and adds "These are verification limits, not accepted passing evidence", and findings.md's attempt-1 block also shows `make verify` exited 2. Nothing in the change records a later green run, so a maintainer reading the change cannot see the DoD met. | mimo-v2.6-flash | fixed — not a test — plan records green runner checkpoint cc42457 beside the sandboxed red run | no | — |
| L2-2 | MINOR | MAINT | impl | `scripts/stage2.py`, `repair()`'s legacy-status `Refused` raise (just after the `doubled` refusal), asserted unconditionally at `tests/test_stage2.py:4739` | The refusal collects legacy rows from all three locations — the change's own test names `L1-1`, `L2-1` and the phase-6 row `F-1` — and then instructs the operator to set "the loop row's `Broke a test` mark". A phase-6 row has nine cells and no `Broke a test` column and is nobody's loop row, so when the only legacy row is phase-6 the message demands a field that does not exist in that table; the plan's step 2 scopes the mark to the loop row, and the message does not. | mimo-v2.6-flash | rejected — the premise is false: a phase-6 table carries a `Broke a test` column (`docs/WORKFLOW.md`, "Two columns for every stage-2 change"; e.g. `plans/changes/pi-pin/findings.md`, phase-6 header), so the refusal's instruction holds there too |  | — |
| L2-3 | MINOR | SPEC | fix-r1 | `scripts/stage2.py`, the `prefixes` comprehension in `check_repair_answer`, against `plans/changes/repair-fixed-lines/spec.md`, Terms, "Finding-shaped identifier" | The term defines a finding-shaped identifier as "ASCII letters, a hyphen and digits whose letters are the prefix of a row id in the change's loop record or findings tables"; in a change whose rows are `L1-1` and `L9-2` the letters `L` are a prefix of every row id, yet the code only collects prefixes from ids that themselves fully match `[A-Za-z]+-[0-9]+` — loop record rows are never consulted and loop ids do not match that shape — so the prefix set misses `L`, and an answer line `L-3: fixed — tests/test_fix.py::test_fix` is silently dropped instead of failing with `L-3: no taken row carries this id`, which criterion 3 and stage2-repair criterion 15 ("a checkpoint … with an unknown ID answered") require. No test sends an `L-<digits>` line: the unknown-id test is parameterized only with prefixes `F` and `QA`, which do fully match the code's shape. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_repair_rejects_unknown_finding_shaped_identifiers | no | — |
| L2-4 | MINOR | MAINT | impl | `docs/WORKFLOW.md:1110` | The repaired paragraph ends with `is. **Red first:** the runner proves each repair of code by running the named test alone against the baseline's code, in a`, a single line of about 120 characters, while every other prose line of the file is wrapped at 80; markdownlint's MD013 (report gate, globs `**/*.md`, expected 80) will name a line this change added, and earlier changes recorded "markdownlint names no line the repair added" as their passing state. | mimo-v2.6-flash | fixed — not a test — workflow paragraph rewrapped to 80 columns; markdownlint reports no diagnostic on changed lines | no | — |
| L3-1 | MAJOR | SPEC | promised-not-done | `scripts/stage2.py:2265-2267`; `plans/changes/stage2-repair/spec.md:191`; `plans/changes/repair-fixed-lines/spec.md:23`; `plans/changes/repair-fixed-lines/decisions.md:35` | The answer filter decides by the left side's shape alone, so a fixed line whose free-text id names no taken row — `custm: fixed — tests/test_fix.py::test_fix` beside the correct `custom:` line — is dropped as prose and the attempt checkpoints. Criterion 15 of the repair spec this change cites still requires an answered unknown ID to fail the post-run checks (its refuted-by names exactly the checkpoint case), and this change's own spec promises prose tolerance "without weakening finding validation"; only `L…` ids and letters-hyphen-digits ids whose prefix a row uses are caught, so the promised "a mistyped id is caught as today" holds for those alone. Reading the fixed status on a line's right side instead of the id's shape would keep `expected:`-style prose ignored and still fail every fixed line that names no taken row. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_repair_rejects_unknown_claimed_fixes | no | — |
| L3-2 | MINOR | MAINT | maintainer-trip | `tests/test_stage2.py:5714-5733`; `scripts/stage2.py:1073`; `docs/WORKFLOW.md:1108-1109` | The instruction regression pins only two of the three legacy completion markers: its needle lists carry `; fixed by` and `; fixed:` but not `; repaired by`, the marker a merged record row already uses and the reason loop round 1 widened the check. Deleting `; repaired by` from the shared answer prompt and the workflow keeps every test green while the code still refuses on it, so the doctrine would name two old forms while a third silently stops a repair before any call. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_repair_instructions_describe_answer_filtering_and_hand_repairs | no | — |
| L3-3 | MINOR | SPEC | promised-not-done | `scripts/stage2.py:2246` against `plans/changes/repair-fixed-lines/spec.md:49` and `docs/WORKFLOW.md:1102` | `L` is hardcoded into the prefix set, so an `L`-prefixed letters-hyphen-digits id counts as finding-shaped even when no row id starts with `L`; the Terms say such an id counts only when its letters prefix a row id, `L-3` is not a loop id (`L<digits>-<digits>`), and the workflow states the same "only when their prefix occurs in the change's row ids" rule. In a repair with no loop record and only phase-6 rows, a report line such as `L-3: see below` therefore fails the attempt after a green `make verify` — the spurious-retry class this change sets out to remove. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_repair_ignores_l_prefix_prose_without_loop_rows | no | — |

Rounds run: 3

Stage-2 call, 2026-10-16: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 462 files, 1293 commits, 12 rules.
