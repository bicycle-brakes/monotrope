---
title: "Spec — red-first-pytest-failed"
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
produced_by: {kind: llm-session, name: codex, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, red-first]
class: bounded
appetite: 1
adr_files: []
---

# Spec — red-first-pytest-failed

The goal in one sentence: a red-first baseline proof accepts pytest's own
`Failed` beside the uncaught `AssertionError`, while a missing helper still
proves nothing (bead `coding-harness-a7m`). Research: `research.md`. Settled
scope: `decisions.md#Q-1`.

## Problem

The runner's red-first classifier `_red_record_fault` refuses every failed
call that did not raise an `AssertionError` (the branch ending "not an
AssertionError", `scripts/stage2.py`, read at `4a81fc9a` on 2026-10-27), and
the probe records only `assertion` and the exception's type name
(`RED_PROBE_SOURCE`). The expected-exception form therefore refuses on
every attempt; the research also records the separate missing-helper case:

- Phase 6 of `red-first-install` rejected its F-2 for exactly this
  (2026-10-16): a test written `with pytest.raises(...)` whose baseline does
  not raise reports "DID NOT RAISE" through pytest's own `Failed`, and a test
  calling a helper the repair adds fails with `AttributeError`.
- On 2026-10-27 the runner rejected both Codex repairs of
  `review-loop-deep-b` rows F6-7 and F6-8 "only because its red-first check
  needs an AssertionError"; both named tests drive the behavior under test
  through `pytest.raises`, the orchestrator had to measure by hand, and
  `make verify` then hit the 30-minute step limit during the retries.

The maintainer settled the scope (`decisions.md#Q-1`): an uncaught
`AssertionError` and pytest's own `Failed` outcome both count as red; a
missing helper (`NameError`, `ImportError`, `AttributeError` on a name the
baseline lacks) stays not red. This spec amends the term "Assertion failure"
and criterion 4 of `plans/changes/red-first-install/spec.md`; that folder
stays untouched as the record of the preceding contract.

## Terms

- **Red first:** the attempted repair's named test fails on the baseline's
  code, proven by the runner's own probe run, not by terminal output.
- **Qualifying failure:** an uncaught `AssertionError` or an exception of
  pytest's own failed-outcome class (`pytest.fail.Exception`, subclasses
  included) raised in a test body's call phase — a `pytest.raises` block
  that did not raise, or an explicit `pytest.fail` in the body. It is
  identified by exception type in the runner-owned probe, never by the
  recorded type name: an application class merely named `Failed` does not
  qualify.
- **Complete proof:** the existing record contract — exit exactly 1 (red
  side) or 0 (fixed side), fresh token, this selector, finished session, no
  collection errors, a non-empty selection of the requested test only, and
  passing setup and teardown for every selected case.

## Acceptance criteria

1. When a complete red-first proof holds at least one failed call and every
   failed call carries a qualifying failure — a DID-NOT-RAISE from
   `pytest.raises`, an explicit `pytest.fail` in the body, a `Failed`
   subclass, an ordinary assertion, or a parameterized mixture of passing
   and such failing cases — the proof succeeds.
   *Refuted by:* any complete run containing only those forms being
   refused, regardless of its diagnostic wording.
   *Basis:* `decisions.md#Q-1`.
2. If any selected call fails with an exception that is neither an uncaught
   `AssertionError` nor pytest's own `Failed` — a missing helper's
   `NameError`, `ImportError` or `AttributeError`, a `RuntimeError`, or an
   application class merely named `Failed` — the proof is refused, also when
   another selected case of the same run fails qualifying.
   *Refuted by:* any such run accepted.
   *Basis:* `decisions.md#Q-1`.
3. If a selected case's setup or teardown fails — a fixture-level
   `pytest.fail`, a fixture assertion, or a teardown error beside a
   qualifying failed call — the proof is refused and names the failing
   phase, not the call the failure removed.
   *Refuted by:* such a run accepted, or the refusal naming the call; the
   missing-Pi-install refusal of `research.md` would then pass as red.
   *Basis:* `decisions.md#Q-1` (the extension covers call-phase failures
   only).
4. If the run is not a complete proof — an exit other than the expected one,
   a collection error, an empty or foreign selection, a skip, xfail or
   XPASS, a timeout, or missing, stale, malformed or wrong-selector
   evidence, including absent or wrongly typed failure classification —
   the proof is refused with scrubbed diagnostics.
   *Refuted by:* any such run accepted, or unredacted run output in the
   refusal.
   *Basis:* `research.md` (the existing proof requirements).
5. When the runner proves the named test on fixed code, the proof succeeds
   only with exit 0 and passing setup, call and teardown for every selected
   case; a `Failed` call on fixed code refuses it.
   *Refuted by:* a failing named test marked proven, or a passing one
   refused because the shared probe changed.
   *Basis:* `research.md` (`fixed_test_proof` shares probe and classifier).
6. When a repair's named test fails on the baseline through a qualifying
   failure and passes the fixed-code proof, the row is marked fixed with its
   named test and the positive test-evidence mark, in one attempt.
   *Refuted by:* such a repair retried or refused for lacking an
   `AssertionError`; a still-failing named test receiving the mark.
   *Basis:* `decisions.md#Q-1`; `research.md` (rows F6-7 and F6-8).

## Non-goals

- Accepting any other call-phase exception; the missing-helper form F-2
  names stays refused — widening it is a separate decision, not this one.
- Distinguishing DID-NOT-RAISE from an explicit body `pytest.fail`: the
  probe records the exception type only, and Q-1 accepts both forms.
- The guard-test policy — which repair rows owe baseline proof
  (bead `coding-harness-0ho`) — and the test-strength strand about tests
  that already pass on baseline (bead `coding-harness-y17`); both are
  separate changes.
- Provisioning baseline dependencies, and any change to routing, attempts,
  timeouts, scratch-checkout construction, cleanup, ref protection or
  credential scrubbing.
- Editing the predecessor artifacts under `plans/changes/red-first-install/`
  or any other change folder: the amendment lives in this spec.
- A `design.md` or an ADR: the class-based design rule excludes phase 2b
  for a `bounded` change, and no file under `docs/adr/` changes.

## Protected areas

- `plans/changes/red-first-install/` and every other change folder: archived
  ledgers hold their named tests, and the predecessor spec is the amended
  contract of record.
- `prompts/04-implement.md` and `docs/WORKFLOW.md`: their wording "fails on
  the baseline's code" already covers the accepted forms.
- `tools/pi/`, `decisions/`, `docs/adr/` and `plans/INDEX.md` (the runner
  renders it).

## Definition of Done

- `make verify` green.
- Moved in the same pull request: this change's `spec.md` and `plan.md`,
  and the runner's `findings.md` evidence; no models and no ADRs change.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `coding-harness-a7m`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-a7m`.
- Special runs: the new pytest-`Failed` acceptance cases measured red on
  the baseline code and green after the change, with the tested commit in
  the pull request body; existing refusal and fixed-code behavior stays
  covered by regression tests.

## Open decisions

None open. Decisions this draft made visibly, each freely revisable:

- [DETAIL] Identify pytest's `Failed` by exception type in the probe
  (`isinstance`), never by the recorded type name — a same-named application
  exception must not expand the maintainer's answer.
- [DETAIL] The probe record stays schema 1 with one new boolean field: the
  record is ephemeral (a fresh token per run in a temporary directory), so
  no stored record migrates.
- [DETAIL] The predecessor folder stays unchanged; this spec's Problem and
  criteria state the amendment, keeping the diff inside this change.
- [DETAIL] One hour of phase 4, repairs included — the code change is two
  seams in one file plus tests; a stop, not an estimate.
