---
title: "Findings — runner-red-gate"
category: findings
status: accepted
implementation_status: done
date: 2026-10-08
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-zci
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-red-gate

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 269 files, 626 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 270 files, 627 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 628 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `scripts/stage2.py:1121` | With four blocking gates each emitting 100 body lines, only the first three reach the repair prompt. The fourth gate’s name, failure and RED frame disappear behind a generic omission marker. Each blocking gate must retain diagnostic evidence within the shared budget. [Acceptance criteria 1–2] | Codex | closed — 94570b5; test_every_blocking_gate_keeps_its_frame_and_last_line | no |
| F-2 | BLOCKER | SPEC | base | `scripts/stage2.py:1115`; `tests/test_stage2.py:1009` | [DIVERGENT] A 1,000-line gate renders 61 lines; sections totaling 200 lines followed by another red gate render 201. Markers exceed the stated budgets, while the bound test explicitly asserts 61 and permits 201, so it passes these violations. [Acceptance criterion 2] | Codex | closed — 94570b5; test_red_sections_are_bounded_and_say_what_they_left_out | no |
| F-3 | BLOCKER | SPEC | base | `scripts/stage2.py:1102` | If an earlier gate emits output without a trailing newline, its closing frame is appended to that output and goes unrecognized. The parser remains inside that gate and ignores later, correctly framed red gates. With 500 subsequent report lines, the fallback tail loses the blocking failure entirely. [Acceptance criterion 1] | Codex | closed — 94570b5; test_a_frame_printed_onto_a_gates_last_line_is_still_a_frame | no |

Phase 6 verdict: codex 01a1189a-29e7-75d0-8956-05fd548ebf7b, 2026-10-08
Reviewer session: codex 01a1189a-29e7-75d0-8956-05fd548ebf7b — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — GLM loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | impl | scripts/stage2.py:1132 | `verify_attempt` hands `red_sections` a blind concatenation of separately captured stdout and stderr, but `verify_all.sh` prints its frames to stdout and runs each gate unmerged (`sh -c "$lauf_cmd"`, no `2>&1`, scripts/verify_all.sh:110), so a blocking gate that writes its failure to stderr — a shell `command not found`, an uncaught traceback — has that text appended after every frame: the red section then carries only the gate's stdout, the tail fallback never runs, and the actual error is dropped from the repair prompt, where today's 80-line tail always ended with that stderr block; the stand-in `make` in every new test sets only `stdout`, so the path is untested | GLM | taken — test_a_blocking_gates_standard_error_reaches_the_repair_prompt | no | agree |
| L1-2 | MINOR | MAINT | impl | scripts/stage2.py:1098 | The parser trusts any frame-shaped line anywhere in the stream, including lines printed inside a gate's own body — a tool quoting an earlier red run, or a fixture string echoed by a failing traceback at column 0: a quoted `── [x] $` followed by a quoted `── [x] RED (block)` inside one gate's output mints a phantom red section and can close the real gate's section early | GLM | taken — test_a_frame_quoted_inside_a_gate_opens_no_section; a quoted end line of the open gate itself stays a named limit | no | agree |
| L1-3 | MINOR | MAINT | impl | tests/test_stage2.py:948 | The frame guard asserts the producer's source contains `echo "── [$gid] $ `, pinning the shell variable name and the `echo` form instead of the printed format, so a refactor that leaves the emitted frames byte-identical (renaming `$gid`, switching to `printf` with the same output) fails the test spuriously and teaches maintainers to ignore it | GLM | taken — the guard now matches the printed format by pattern, not the shell spelling | no | agree |
| L1-4 | MINOR | MAINT | impl | scripts/stage2.py:1121 | `verify_attempt`'s docstring still opens "Run the one gate" while it runs `make verify` over every gate; after this change makes gate-level reading the function's whole job, the stale sentence misdirects exactly the reader it should orient | GLM | taken — docstring names make verify and the gates that blocked | no | disagree — The docstring wording demonstrates no correctness fault, acceptance gap or ineffective gate, so it falls outside the permitted finding types. |
| L2-1 | MAJOR | MAINT | code | scripts/stage2.py:1084, tests/test_stage2.py:983 | `red_sections` closes an open gate only on the three verdict spellings `gruen`, `RED (block)` and `rot, aber nur`, but the rename guard greps `verify_all.sh` for only the `$` start frame and the `RED (block)` end frame. Rename any other verdict (say `gruen` anglicised to `green`) and no gate ever closes: every following section is swallowed, `red_sections` returns None on every run and each failure silently falls back to the 80-line tail — the exact defect this change removes — with every test still green. Pin all end-verdict spellings in the guard, or close a section on any frame line of the open gate that is not a `$` start. | GLM | taken — test_a_gate_closes_on_any_verdict_spelling; any non-start frame line of the open gate ends it | no | agree |
| L2-2 | MINOR | SPEC | spec | scripts/stage2.py:1144-1148, plans/changes/archive/2026-10-08-runner-red-gate/spec.md criterion 2 | Criterion 2 bounds "the whole" diagnostics to 200 lines, but the red-section path appends up to 40 standard-error lines and header lines on top of the 200, and no acceptance criterion mentions the standard-error channel at all — the round-1 addition (loop row L1-1) never went back into the spec, so the document promises a bound the code exceeds and leaves half the diagnostics uncontracted. | GLM | taken — spec criterion 2 reworded, criterion 5 for standard error | no | agree |
| L2-3 | MINOR | MAINT | code | scripts/stage2.py:1146 | The standard-error window is the last 40 lines of the entire run's standard error, not of the blocking gates: report-only gates that run after the red gate and log on stderr push the blocking gate's error out of the window, and the cut carries no left-out marker — the red section still travels, but the gate's own error message can be the part that is lost. | GLM | taken — test_a_long_standard_error_is_cut_with_a_marker; whole-run scope stays a named limit (stderr is unframed) | no | agree |

Rounds run: 2

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 628 commits, 12 rules.
