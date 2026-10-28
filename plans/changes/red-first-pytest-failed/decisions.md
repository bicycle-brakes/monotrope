---
title: "Decisions — red-first-pytest-failed"
status: draft
implementation_status: partial
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-a7m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage-2, runner, red-first]
---

# Decisions — red-first-pytest-failed

Interview for a `bounded` change (at least one counted record).

## Q-1 · Which call-phase failures prove a test red first

context: |
  Topic: the runner's red-first check, which proves a repair's test fails on
  the baseline code before the repair counts as fixed.
  Intention: on 2026-10-27 the check rejected correct repairs whose tests were
  written as `with pytest.raises(...)` (14 of 32 rejected attempts that day).
  Today: only an uncaught AssertionError counts as red; pytest's own `Failed`
  outcome ("DID NOT RAISE") is refused.
  Repository change: the classifier in `scripts/stage2.py` and its tests.
  Architecture change: none; the red-first contract of red-first-install
  gains one accepted failure shape.
  Question: which call-phase failures should prove a test red first?
asked: 2026-10-27, the directing conversation
answer: option 1 — an uncaught `AssertionError` and pytest's own `Failed`
  outcome (a `pytest.raises` block that did not raise, an explicit
  `pytest.fail` in the test body) both count as red; a missing helper
  (`NameError`, `ImportError`, `AttributeError` on a name the baseline lacks)
  stays not red
answered_by: maintainer
status: answered

In the context of the runner's red-first check, which today refuses every
call-phase failure that is not an `AssertionError` and so rejected repairs
whose tests were written as `with pytest.raises(...)` (phase 6 of
review-loop-deep-b, rows F6-7 and F6-8, 2026-10-27; 14 of 32 rejected repair
attempts that day), facing either keeping the strict rule or accepting every
call-phase exception, we decided to accept pytest's `Failed` beside
`AssertionError` and to keep refusing a missing helper, to achieve that a
test which states an expected exception proves the bug while a test that
only fails because the fix's new name does not exist yet still proves
nothing, accepting that an explicit `pytest.fail` in a test body now counts
as red too (the probe records the exception type only, so it cannot tell the
two `Failed` forms apart). This amends criterion 4 and the term "Assertion
failure" of `plans/changes/red-first-install/spec.md`. The guard-test design
(bead coding-harness-0ho) follows as a separate change. — 2026-10-27

## Q-2 · Q-1 as a principle: is DID-NOT-WARN red

context: |
  Topic: the runner's red-first check, which proves a repair's test fails on
  the baseline code before the repair counts as fixed.
  Intention: review-loop row L4-1 (MAJOR) read Q-1's two examples in
  parentheses as a closed list and called a `pytest.warns` block whose
  warning never came (DID-NOT-WARN) wider than the answer.
  Today: the probe accepts every exception of pytest's own failed-outcome
  class by type, DID-NOT-WARN included; it did so since Q-1 was built.
  Repository change: this record and the spec term state the principle
  first and the forms as examples; no code changes.
  Architecture change: none.
  Question: should Q-1 be stated as a principle — red is a failure the test
  itself states (an assertion or pytest's Failed, for example DID NOT RAISE,
  DID NOT WARN, pytest.fail), never a crash?
asked: 2026-10-28, the directing conversation
answer: option 1 — yes, as a principle
answered_by: maintainer
status: answered

In the context of the red-first check, whose answer Q-1 named two forms of
pytest's own failed outcome as examples, facing a closed list of forms (which
needs the runner to tell forms apart by message text, fragile across pytest
versions) or the principle behind the answer, we decided that red is any
failure the test itself states — an uncaught AssertionError or pytest's own
failed outcome in any form — while a crash such as a missing helper stays
not red, to achieve a rule that holds for every pytest helper by exception
type, accepting that a new pytest helper raising Failed counts without a
further decision. This clarifies Q-1; it does not change it. — 2026-10-28
