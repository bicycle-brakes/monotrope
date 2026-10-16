---
title: "Spec — red-first-install"
status: draft
implementation_status: partial
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-omp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, red-first]
class: bounded
appetite: 1
adr_files: []
---

# Spec — red-first-install

The baseline check establishes red first only through an assertion failure in
the named test, never through a missing runtime dependency (bead
`coding-harness-omp` — missing Pi installation misread as red-first evidence).
Research: `research.md`. Settled choices: `decisions.md`.

## Problem

At draft baseline `63f1511` on 2026-10-16, `red_first` in
`scripts/stage2.py` accepts pytest exit 1 or 2 without checking which phase
failed. Its temporary baseline checkout lacks the ignored Pi installation.
The research records a real-Pi fixture error with exit 1 when that installation
is absent; the fixture uses `pytest.fail`, so no assertion in the named test
needs to run. That environment fault can therefore certify a repair whose
test would pass on the baseline's production code. The scratch execution
itself was not measured in research; the exit-1 fixture outcome was recorded
there from the earlier review.

## Terms

- **Red first:** evidence that the attempted repair's named test fails on the baseline's code.
- **Assertion failure:** an uncaught `AssertionError`, including a subclass, during the test body's call phase, reported by pytest as an ordinary failure.
- **Complete run:** pytest finishes the selected invocation with recorded collection and setup, call and teardown outcomes for its selected cases.

## Acceptance criteria

1. When a complete baseline run exits 1 with at least one ordinary assertion
   failure in the named test, all selected setup and teardown phases passing,
   and all other selected calls passing or failing by assertion, the
   red-first outcome is successful.
   *Refuted by:* refusing a clean assertion failure or a parameterized named
   test with passing cases and an ordinary assertion-failing case.
2. When the baseline lacks the Pi installation and its dependency fixture
   fails before the named test body runs, the red-first outcome is refused.
   *Refuted by:* accepting that fixture's pytest exit 1 as red first.
3. If any selected setup or teardown fails, the red-first outcome is refused
   even when a selected call also fails by assertion.
   *Refuted by:* accepting an assertion in a fixture or accepting a call
   assertion accompanied by a teardown error.
4. If a selected test call fails with an exception other than
   `AssertionError`, the red-first outcome is refused.
   *Refuted by:* accepting `RuntimeError`, `ImportError`, or a call to
   `pytest.fail` in the test body as assertion evidence.
5. If the invocation passes, collects no selected case, has a collection
   error, is interrupted, has an internal or usage error, or includes a
   skipped, expected-failing or unexpectedly-passing case, the red-first
   outcome is refused.
   *Refuted by:* accepting any such invocation, including a strict unexpected
   pass with exit 1 or a skip alongside another case's assertion failure.
6. If complete, readable evidence tied to the named test's current invocation
   is unavailable, the red-first outcome is refused.
   *Refuted by:* accepting exit 1 with a missing, malformed, incomplete,
   wrong-test or stale outcome record, or accepting a process timeout.
7. When the red-first outcome is refused, the repair attempt's diagnostic
   names the finding, the test and the cause without exposing credentials.
   *Refuted by:* an environment fault checkpointing or marking the row fixed,
   a refusal lacking that context, or an unsanitized secret in its diagnostic.
8. When a baseline check finishes or is refused, the existing worktree cleanup
   and shared-reference protection still apply.
   *Refuted by:* a leftover scratch worktree, an undetected created or moved
   reference, or cleanup deleting another session's reference.

## Non-goals

- Installing, copying or linking Pi or other ignored dependencies into the baseline checkout; revisit provisioning in a separate change only if classification proves too narrow.
- Adding the test-only guard exception or changing which repair rows owe baseline proof; the separate guard-test change owns that policy.
- Proving that an assertion's meaning identifies the reviewed production defect, or sandboxing hostile tests.
- Changing model routes, attempts, time limits, fixture policy, or the Pi pin.
- A design artifact or ADR: the bounded class requires neither.

## Protected areas

- `tools/pi/` and `tests/test_pi_contract.py`: the missing-install fixture remains an error, never a skip or an automatic install.
- Other change folders, `docs/adr/`, `decisions/` and tracker data: this fix changes outcome classification, not governance or related work's contracts.
- Credentials, permissions and session ownership: existing boundaries remain in force.

## Definition of Done

- `make verify` is green, including the criterion ledger, and the new regression tests distinguish assertion failures from environment faults.
- Documents moved with the code: this change's `spec.md` and `plan.md`; no architecture document, model definition or ADR changes.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes the missing-install false-proof task (`coding-harness-omp`), with `Closes-Bead: coding-harness-omp` on its last commit.
- Special runs: the targeted baseline-classification regressions, with their tested commit named in the pull request body.

## Open decisions

None open. The following are visible agent decisions, not new maintainer answers.

- [DETAIL] Classify outcomes instead of provisioning dependencies, and refuse an unestablished proof, following `decisions.md` items 1–2; this keeps environment faults from certifying a repair.
- [DETAIL] Use the exception type and pytest's final phase outcome to define an assertion; text containing `AssertionError` and explicit `pytest.fail` are insufficient because neither proves an ordinary assertion-failing call.
- [DETAIL] A selected parameterized invocation may mix passes and assertion failures, but any error, skip or expected-result marker refuses it; otherwise one case could conceal incomplete evidence from another.
- [DETAIL] Phase 4 has one hour including repairs, then stops and reports unfinished work; this bounds a local classification fix.
- [DETAIL] Coordinate the shared `red_first` function after, or by rebasing onto, the guard-test exception change (`coding-harness-0ho`), as already recorded in `decisions.md`; do not implement its policy here.
