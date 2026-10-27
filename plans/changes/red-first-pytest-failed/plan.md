---
title: "Plan — red-first-pytest-failed"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-a7m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, red-first]
---

# Plan — red-first-pytest-failed

```text
For you:     Repairs whose test expects an exception through pytest.raises, or calls pytest.fail in the body, now prove red on the baseline; a missing helper still proves nothing.
Done when:   The classifier accepts pytest's Failed beside AssertionError, refuses every other call failure and broken runs, the fixed-code proof stays all-pass, and make verify is green.
Appetite:    One hour of phase 4, repairs included — a stop, not an estimate.
Not now:     Any other call-phase exception, distinguishing the two Failed forms, the guard-test policy (coding-harness-0ho), dependency provisioning.
Pre-mortem:  suppose it failed: most likely because a fixture-level pytest.fail was read as a test-body failure.
Starts unless you say stop.
```

## Scope and baseline

Implements criteria 1–6 of `spec.md`. Class `bounded`: no `design.md`, no
ADR (D-14). `findings.md` holds no phase-2a rows (read 2026-10-27), so none
is worked in. Phase 1 ran as a Stage-2 flash exploration (route `flash`,
model `glm-5.3-flash`, leak check clean); `research.md` records no Stage-1
fallback, so none is carried forward. `templates/plan.md` and
`scripts/validate_change_artefacts.py` do not exist at the draft baseline
`eff79689`; this plan follows the phase-3 prompt's form, and the
artefact-validator gate is reported absent here rather than claimed green.

## Build sequence

1. `RED_PROBE_SOURCE` (`scripts/stage2.py`): each phase record gains a
   boolean `pytest_failed` — `bool(report.failed and isinstance(raised,
   pytest.fail.Exception))` — beside `assertion`; `exception` stays the
   diagnostic type name, no message is recorded, and the record stays
   schema 1 (a fresh token per run; no stored record migrates).
2. `_red_record_fault`: validate `pytest_failed` like `assertion` (a
   missing or non-boolean value refuses as a phase of an invalid form); in
   the failed-call branch accept `call["assertion"] or call["pytest_failed"]`;
   every earlier check keeps its place and order (selector, token, session
   exit, collection, setup and teardown before the call, expected-outcome);
   the two refusal texts ("… not an AssertionError", "no selected call
   failed by assertion") name both accepted classes. The `passing=True`
   path keeps its every-case-passes rule untouched.
3. Wording only: the docstrings of `red_first` and `fixed_test_proof` and
   the exit-1 message ("red first needs exit 1 with an assertion failure")
   state both accepted classes.
4. `tests/test_stage2.py`, on the `repair_world`/`red_first_planted`
   pattern, keeping every existing top-level name (archived ledgers hold
   them):
   - new `test_red_first_accepts_pytest_failed_call_outcomes`: DID-NOT-RAISE,
     an explicit body `pytest.fail`, a `Failed` subclass, and a
     parameterized pass/assertion/`Failed` mixture each prove red; a
     parameterized run mixing a qualifying case with a `NameError` case
     refuses.
   - `test_red_first_refuses_non_assertion_call_failures`: the `pytest.fail`
     case moves to acceptance above; the function keeps refusing
     `RuntimeError` and `ImportError` and gains `NameError`, `AttributeError`
     and an application class merely named `Failed`, against the reworded
     refusal.
   - `test_red_first_refuses_missing_or_invalid_evidence`: a phase record
     lacking or malforming `pytest_failed` refuses.
   - new `test_fixed_code_proof_keeps_pytest_failed_red`: a green named test
     proves; a `Failed`-failing one refuses with the fixed-code all-pass
     message.
   - new `test_repair_accepts_a_pytest_failed_baseline_proof`: the planted
     baseline lacks the expected exception (DID-NOT-RAISE), the fixed code
     raises it; the repair ends in one attempt with `fixed — tests/…` and
     the positive test-evidence mark.
   - the rest of the cluster (setup/teardown, missing Pi, non-proving
     outcomes, timeout, scrubbing, changed venv, end-to-end refusals) runs
     unchanged.
5. Measure each new acceptance case red against the baseline's code and
   green after the change before the full verification.

## Files and limits

- `scripts/stage2.py` — the probe field, the classifier branch and phase
  validation, two refusal texts, three docstrings; nothing else in the file.
- `tests/test_stage2.py` — the classification cluster named above; no other
  test area.
- `plans/changes/red-first-pytest-failed/spec.md` and `plan.md` — this
  change's own artifacts; the ledger's `not yet written` markers and the
  implementation status move as phase 4 works.

No deletions. Not touched: `plans/changes/red-first-install/` and every
other change folder (the amended contract of record and the archived
ledgers), `prompts/04-implement.md` and `docs/WORKFLOW.md` (the wording
already covers the accepted forms), `docs/adr/`, `decisions/`, `tools/pi/`,
`plans/INDEX.md` (the runner renders it), every script and test file not
named above, and this change's `decisions.md` (a draft's edit of it is put
back; the maintainer's record stands as committed).

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'red_first or fixed_test_proof or repair_accepts'
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_red_first_accepts_pytest_failed_call_outcomes — the proof refuses a DID-NOT-RAISE, explicit-fail, subclass or mixed qualifying run
- 1: tests/test_stage2.py::test_red_first_accepts_only_clean_assertion_runs — an ordinary assertion or mixed parameterized assertion run is refused
- 2: tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures — a NameError, AttributeError, RuntimeError, ImportError or same-named application Failed is accepted
- 3: tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors — a fixture pytest.fail, a fixture assertion or a teardown error beside a qualifying call is accepted
- 3: tests/test_stage2.py::test_red_first_refuses_a_missing_pi_install — a missing dependency's setup failure proves red
- 4: tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes — a green, skipped, expected-failing or unselected run is accepted
- 4: tests/test_stage2.py::test_red_first_refuses_missing_or_invalid_evidence — stale, absent or malformed evidence, the new field included, is accepted
- 4: tests/test_stage2.py::test_red_first_refuses_a_timed_out_run — a timed-out run with partial evidence qualifies
- 4: tests/test_stage2.py::test_red_first_scrubs_outcome_diagnostics — a refusal carries unredacted run output
- 5: not yet written tests/test_stage2.py::test_fixed_code_proof_keeps_pytest_failed_red — a Failed on fixed code is marked proven, or a passing run is refused
- 6: not yet written tests/test_stage2.py::test_repair_accepts_a_pytest_failed_baseline_proof — a valid pytest.raises repair is retried, or lacks its fixed status and evidence mark
- 6: tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code — a still-failing fixed test receives the positive mark

## Time used
