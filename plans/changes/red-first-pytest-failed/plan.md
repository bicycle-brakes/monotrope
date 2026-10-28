---
title: "Plan — red-first-pytest-failed"
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
produced_by: {kind: llm-session, name: codex, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, red-first]
---

# Plan — red-first-pytest-failed

```text
For you:     Repairs using pytest.raises or a test-body pytest.fail can prove red on baseline; missing helpers still prove nothing.
Done when:   Both accepted failure types pass baseline proof, other failures stay refused, fixed-code proof requires every case to pass, and make verify is green.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate (maintainer, 2026-10-27).
Not now:     Other exception types, distinguishing the two Failed forms, policy on which rows need baseline proof, dependency provisioning.
Pre-mortem:  suppose it failed: most likely because a fixture-level pytest.fail was read as a test-body failure.
Starts unless you say stop.
```

## Scope and baseline

Implements criteria 1–6 of `spec.md` for accepting pytest's own failure
outcome as repair evidence (bead `coding-harness-a7m`). Class `bounded`:
phase 2b does not run, and no ADR is due. As read on 2026-10-27 at
`4a81fc9a`, `findings.md` has runner-attempt diagnostics but no phase-2a
rows. Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`; no
Stage-1 fallback is recorded. `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent at that commit; use the
phase-3 prompt's form and report the missing validator, never green.

## Build sequence

1. In `scripts/stage2.py`, add a boolean `pytest_failed` to every phase
   emitted by `RED_PROBE_SOURCE`, computed as `bool(report.failed and
   isinstance(raised, pytest.fail.Exception))`. Keep `assertion`, the
   diagnostic-only exception type name, and schema 1; records are private
   and ephemeral with a fresh token per invocation. Record no messages.
2. In `_red_record_fault`, require a boolean `pytest_failed` alongside
   `assertion` on both proof paths. Accept a failed call only when
   `call["assertion"] or call["pytest_failed"]`, never by comparing the
   exception-name string. Preserve all earlier checks and their order,
   including passing setup and teardown before checking the call.
   Preserve `passing=True`'s all-pass requirement.
   Reword the nonqualifying-call, no-red-call and exit-1 diagnostics to
   name both accepted types. Align the probe, classifier and proof
   docstrings with the resulting contract.
3. In `tests/test_stage2.py`, retain all existing top-level test names
   because archived criterion ledgers refer to them, and use the existing
   `repair_world`/`red_first_planted` fixtures:
   - Add `test_red_first_accepts_pytest_failed_call_outcomes` for
     DID-NOT-RAISE, body `pytest.fail`, a subclass of
     `pytest.fail.Exception`, and parameterized pass/assertion/Failed.
   - Extend `test_red_first_refuses_non_assertion_call_failures`: move
     pytest's Failed case to acceptance, retain RuntimeError/ImportError,
     add NameError/AttributeError and an application class named Failed,
     and refuse mixed qualifying/nonqualifying runs in either case order.
   - Extend `test_red_first_refuses_setup_and_teardown_errors` with
     pytest's Failed during teardown beside a Failed call; keep its
     assertion and RuntimeError cases and the separate missing-Pi test.
   - Extend `test_red_first_refuses_missing_or_invalid_evidence` with a
     missing field and non-boolean `pytest_failed` values (including 0, 1,
     null and a string), refusing them as invalid phase evidence.
   - Add `test_fixed_code_proof_keeps_pytest_failed_red`: exercise the real
     probe with all-pass and mixed pass/Failed cases, and reject malformed
     `pytest_failed` evidence on the fixed-code path too.
   - Add `test_repair_accepts_a_pytest_failed_baseline_proof`: baseline
     code omits an expected exception, fixed code raises it; assert one
     repair attempt, the fixed row's named test and positive evidence mark.
   - Update diagnostic expectations in the refusal tests and in
     `test_a_named_test_that_is_not_red_first_fails_the_attempt`; keep
     their refusal semantics and all other regression coverage.
   - Keep synthetic phase records current with `pytest_failed: false`
     where appropriate, so an unrelated missing field cannot mask the
     timeout or other refusal each existing regression is meant to prove.
4. Measure the new pytest-`Failed` acceptance cases red against baseline
   code and green after implementation; record commits and results in the
   runner's evidence. Keep all refusal and fixed-code regressions green
   after implementation. Run the commands below and update the ledger's
   new-test markers only as those tests become defined.

## Files and limits

- `scripts/stage2.py` — change only the probe, outcome classifier and
  related proof diagnostics/docstrings described above.
- `tests/test_stage2.py` — add the named regressions and amend the existing
  classification and diagnostic tests above.
- `plans/changes/red-first-pytest-failed/spec.md` — update implementation
  status as implementation advances; keep the settled criteria.
- `plans/changes/red-first-pytest-failed/plan.md` — update implementation
  status, criterion-ledger markers and phase-4 time used.
- `plans/changes/red-first-pytest-failed/findings.md` — runner-owned attempt
  and verification evidence, preserving prior records.

No deletions. `decisions.md` changes only by a maintainer's answer: Q-2
(2026-10-28) states Q-1 as a principle (review loop rows L4-1, L5-1). Do not touch other change folders. The one exception is the
predecessor `plans/changes/red-first-install/`: its spec keeps its text and
gains one amendment note, and its `decisions.md` detail 1 gains a short
pointer to Q-1 and Q-2 (review loop rows L1-5, L3-1, L3-4, L7-1). Leave `prompts/04-implement.md` and `docs/WORKFLOW.md` unchanged:
"fails on the baseline's code" already covers the accepted forms. Do not
change `docs/adr/`, `decisions/`, `tools/pi/`, routing, retry policy,
credentials, timeouts, scratch-checkout construction, cleanup or ref
protection. The runner owns generated `plans/INDEX.md` updates.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'red_first or fixed_code_proof or repair_accepts_a_pytest_failed_baseline_proof or repair_marks_no_proof'
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_red_first_accepts_pytest_failed_call_outcomes — a complete qualifying run is refused
- 1: tests/test_stage2.py::test_red_first_accepts_only_clean_assertion_runs — ordinary assertion evidence is refused
- 2: tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures — an unrelated exception or mixed invalid run is accepted
- 3: tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors — a setup or teardown error is accepted or the wrong phase is named
- 3: tests/test_stage2.py::test_red_first_refuses_a_missing_pi_install — missing dependency setup proves red
- 4: tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes — an incomplete or nonproving run is accepted
- 4: tests/test_stage2.py::test_red_first_refuses_missing_or_invalid_evidence — stale, absent or malformed evidence is accepted
- 4: tests/test_stage2.py::test_red_first_refuses_a_timed_out_run — a timed-out run qualifies
- 4: tests/test_stage2.py::test_red_first_scrubs_outcome_diagnostics — a refusal leaks unredacted output
- 5: tests/test_stage2.py::test_fixed_code_proof_keeps_pytest_failed_red — fixed-code Failed or malformed evidence is accepted, or all-pass is refused
- 6: tests/test_stage2.py::test_repair_accepts_a_pytest_failed_baseline_proof — a valid repair is retried or lacks its fixed status or evidence mark
- 6: tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code — a still-failing fixed test receives the mark

## Runner route — 2026-10-28

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Appetite record

The card's one-hour stop (3600 s of phase 4, repairs included) was passed
without the four-line stop: the two implement attempts measured 2520 s and
1913 s, 4433 s together, before any repair ran. The Stage-2 runner drove those
attempts unattended and has no stop of its own, so no session read the clock
against the appetite and no maintainer answer (continue, cut, park or drop)
was asked for or recorded. The run continued through review round 1 and the
repair attempts below on the strength of the plan's "Starts unless you say
stop". Answer: continue — the maintainer named a new appetite of 4 hours in total
(conversation, 2026-10-27).

Red-then-green evidence for the three new acceptance tests
(`test_red_first_accepts_pytest_failed_call_outcomes`,
`test_fixed_code_proof_keeps_pytest_failed_red`,
`test_repair_accepts_a_pytest_failed_baseline_proof`): measured by the
orchestrator on 2026-10-28 — each fails with an `AssertionError` at the
baseline `0872d0cc` and the three pass at `b7048d9c`; command and results in
`findings.md`, "Red-then-green measurement of the new tests".

## Time used

2026-10-27 20:29:00–21:11:00 UTC, 2520 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-27 21:11:07–21:43:01 UTC, 1913 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-10-27 22:22:00–22:36:14 UTC, 854 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 22:36:36–23:08:04 UTC, 1887 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 23:08:26–23:39:06 UTC, 1840 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
