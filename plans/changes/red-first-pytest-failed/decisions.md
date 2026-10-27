---
title: "Decisions — red-first-pytest-failed"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
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
