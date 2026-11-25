---
title: "Decisions — red-first-baseline"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, red-first, repair, bug]
---

# red-first-baseline — Decisions

## SKIP · interview

status: skipped
reason: The maintainer filed this as a bug with its expected behaviour stated (coding-harness-7aso, 2026-11-20): a test that is red on the baseline must not be reported as "pytest ended 0 on the baseline"; the task is to find how the red-first baseline is built and why a red test reads as exit 0, and to make the check report what pytest reports. A bug fix whose wanted outcome is the current contract leaves no open choice for an interview; skipped by the orchestrator in night run 2026-11-20-a under the maintainer's standing instruction to decide by recommendation overnight.

## Details decided by the orchestrator

[DETAIL] **D-1 (the exit-code contract)**: the red side is pytest exit exactly 1, as `red_first` and the successor spec `red-first-pytest-failed` state; the `docs/WORKFLOW.md` sentence "exits 1 or 2" is aligned to it in this change. Reason: the governing spec and the code agree; the doc is the outlier.

[DETAIL] **D-2 (first step is a reproduction)**: the spec's first criterion reproduces one of the two recorded refusals (finder-partial-report round 3, row L3-1, branch `fix/finder-partial-report`) as a failing test of `red_first` before any fix. Reason: research could not read the incident evidence; the mechanism must be measured, not guessed.

[DETAIL] **D-3 (the bf9m class stays out)**: a test whose code under test lives in the test file itself (coding-harness-bf9m) is a known limit of a tests-only baseline and is not changed here. Reason: the bead names it as a possibly different case.

## Q-1 · Ambiguity S-1 (which two runs define the mismatch)

asked: 2026-11-21
answer: "The reproduction compares `red_first` with a direct `pytest` run on the same inputs (the refused attempt's `tests/` tree on the captured baseline `HEAD`), so the test isolates the runner, not the code."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 blocker ambiguity row S-1 of red-first-baseline.
  Intention: pin the exact inputs compared in criterion 1 so the reproduction isolates a runner fault in `red_first`.
  Today: `spec.md` did not explicitly say both `red_first` and the direct `pytest` run use the refused attempt's `tests/` tree on the captured baseline `HEAD`.
  Repository change: `plans/changes/red-first-baseline/spec.md` criterion 1 and investigation/regression tests.
  Architecture change: none — clarifies the reproduction comparison baseline.

In the context of reproducing a `red_first` refusal that reported "pytest ended 0 on the baseline" while hand checks saw a failure, facing ambiguity over whether the comparison ran against the same commit and test bytes, we decided that the reproduction compares `red_first` against a direct `pytest` run on the exact same inputs (the refused attempt's `tests/` tree on the captured baseline `HEAD`), to achieve an unambiguous isolation of the runner, accepting that if both runs agree on those inputs no runner mismatch exists for that pair — 2026-11-21

## Q-2 · Ambiguity S-2 (what the fix must achieve)

asked: 2026-11-21
answer: "The fix makes the proof report what `pytest` actually reports (exit code, skip/xfail, collection error) and accept exit 1 only; it need not turn the round-3 test into an accepted red if `pytest` truly ended 0 there."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 blocker ambiguity row S-2 of red-first-baseline.
  Intention: resolve the conflict between accepting the recorded round-3 run as red vs reporting pytest's true outcome and accepting only qualifying exit 1.
  Today: `red_first` can report "pytest ended 0 on the baseline" when pytest ran differently or failed, and criterion 1 appeared to demand turning the round-3 run into an accepted red regardless of pytest's actual outcome.
  Repository change: `scripts/stage2.py` (`red_first`), `plans/changes/red-first-baseline/spec.md`, and tests.
  Architecture change: none — keeps the exit-1 qualifying-failure contract intact while enforcing truthful outcome reporting.

In the context of conflicting readings on whether the round-3 test must become an accepted red or whether `red_first` must strictly report what `pytest` reported, facing non-goals that preserve the qualifying exit-1 contract, we decided that the fix makes `red_first` report what `pytest` actually reports (exit code, skip/xfail, collection error) and accept exit 1 only, to achieve honest diagnostics without relaxing the red-first proof standard, accepting that the round-3 test stays refused if `pytest` truly ended 0 or non-qualifying — 2026-11-21
