---
title: "Plan — flaky-swarm-leak-test"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-yb1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, swarm, concurrency]
---

# Plan — flaky-swarm-leak-test

```text
For you:     Concurrent test logs stop causing false security refusals, and a guard catches new unprotected appends.
Done when:   A red/green race reproduction, repeated loaded refusal checks, migrated log access and make verify pass.
Appetite:    3 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Production behavior, swarm performance, scheduling changes or new dependencies.
Pre-mortem:  suppose it failed: most likely because one reader still bypasses the shared lock.
Starts unless you say stop.
```

## Files and steps

1. Create `tests/test_atomic_test_log.py`: first reproduce against the actual
   stand-in append path and `SwarmWorld.calls` observer, forcing the writer to
   flush half a large JSON record before the observer reads. Use process/file handshakes
   with bounded waits and unconditional child cleanup, not timing guesses.
   Capture the red fixture observation before migrating it; retain
   a passing negative control that proves the unsafe variant remains detectable.
2. Create `tests/atomic_test_log.py`, standard library only: a shared/exclusive
   `fcntl.flock` protocol on one stable sidecar per destination, a text append,
   JSON-record append and JSON snapshot read. Writers hold the lock through
   flush/close; readers hold it through read/parse. Missing data files yield
   an empty snapshot; other failures propagate. No JSON-error suppression.
   For independent opens in threads and processes use the same lock identity;
   do not lock a replaceable temporary data inode. No durability guarantee is
   added. Embed this helper's source at one render marker in generated stand-ins
   so sandboxed children need no import path, environment change or copied
   repository-visible helper. Host-side readers import the same module.
3. In `tests/test_atomic_test_log.py`, force a write split while the lock is
   held and verify the real fixture observer waits for the completed record; disable reader
   locking as the red control. Exercise several independent writer processes
   and simultaneous readers with unique IDs and payloads larger than 64 KiB;
   assert exact final records, missing-log behavior and corrupt-log failure.
   Make the forced-split seam test-local; production scripts are never patched.
4. Migrate these existing files; the inventory locations are at `3950c853`:
   - `tests/test_stage2.py`: five data appends (190, 196, 242, 298, 319),
     startup reads, `World.script`, `calls`, `versions` and direct log readers;
     replace the local `locked` log protocol with the shared one, preserving
     the lock-probe semantics at 484. The old lock-only opener at 137 is
     superseded by the helper. Keep scenario matching and record formats.
   - `tests/test_stage2_swarm.py`: four appends (206, 270, 275, 282), startup,
     `SwarmWorld.calls` and direct infrastructure/receipt log observations;
     keep the refused-run test's assertions and spy, and assert its first,
     leaking run logged no model calls before clearing the log. Generic text appends
     preserve bytes, including whether the caller supplied a trailing newline.
   - `tests/test_pi_install.py`: three stand-in appends (101, 158, 183) and
     `Pin.local_runs`, `path_runs`, `npm_calls`; retain offline installer checks.
   - `tests/test_stage2_session.py`: two appends (82, 87), startup and fixture
     `calls`; preserve the shell-result record and the no-window/no-model setup.
   - `tests/test_stage2_research_availability.py`: one append (72), including
     its independently rendered stand-in; host reads already use `World.calls`.
   Audit every rendering/copy of these source constants, including alternate
   executable paths, and retain stdlib-only transitive no-contact checks.
5. In `tests/test_atomic_test_log.py`, add the guard and its planted-fault
   tests: inspect Python under `tests/` plus executable embedded Python strings
   for append-mode built-in/Path opens, including `mode=` and `a+`. Allow only
   the shared implementation and exact, explained non-log operations (lock
   probes/document mutations), without whole-file exemptions. Exercise a new
   top-level log append and a new embedded stand-in append, and exempt-operation
   controls. Report source path and line; do not exempt a string merely because
   it is embedded. Guard test sample strings must be recognisable test data,
   not blanket exemptions for executable source. Dynamic/obfuscated I/O is
   outside this static guard, as the spec states.
6. Run the commands below. Keep one process-level forced-race test and run the
   original refused-run test ten times as separate pytest invocations, each
   concurrently scheduled with the race test via two xdist workers. Record
   pre-fix and post-fix commands, date, base/head or uncommitted patch identity,
   repeat counts, captured stdout/stderr, refusal diagnostics and outcomes in
   this plan. Do not claim a natural CI reproduction if only the forced race
   was red. If a clean run still refuses, inspect its gate diagnostics and stop
   widening this test-only repair into a production change.
7. Update this change's `spec.md` implementation status and `plan.md` evidence,
   ledger prefixes and time as work advances; the current draft inspection is
   recorded in `research.md`. No deletions or held implementation paths are
   planned. The orchestrator/runner owns `plans/INDEX.md` regeneration, commits,
   tracker updates, review-loop preparation and the final PR; the attempt does
   not edit any held path. No Explore fallback route was recorded.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_atomic_test_log.py -q
for run in $(seq 1 10); do
  .venv/bin/python3 -m pytest tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call tests/test_atomic_test_log.py::test_concurrent_log_snapshots_are_complete -q -n 2 || exit 1
done
.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_stage2_swarm.py tests/test_pi_install.py tests/test_stage2_session.py tests/test_stage2_research_availability.py tests/test_atomic_test_log.py -q -n 2
python3 scripts/check_interview_minimums.py --change flaky-swarm-leak-test
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py --change flaky-swarm-leak-test
python3 scripts/plans_registry.py --check
make verify
```

Run the same loaded loop before and after; any early exit is a failed
measurement, never ten passes. Run the forced reproduction before/after too.
The runner executes full verification after derived index regeneration.
`scripts/validate_change_artefacts.py` and `templates/plan.md` are absent at
the draft's base; use the available individual gates above, not a substitute
green claim. Protected: all production code, configuration, governance,
other change folders and test files beyond the seven named Python files.

## Draft validation — 2026-11-13

On base `3950c853` plus this uncommitted draft: interview-minimums and the
criterion ledger passed; research-handoff reported the legacy exemption.
Local structural checks passed for headers, the opening card, bounded class,
one ledger and the empty time section; `git diff --check` passed.
The derived index differs and is left to the runner as required. Full
`plans_registry.py --check` was not run because its tracker read can leave the
permitted worktree boundary. `make verify` and implementation tests were not
run in this drafting phase; the runner owns full verification.

## Red/green evidence — 2026-11-14

Orchestrator hand work, measured 2026-11-14 00:05–00:22 UTC on one macOS
machine (12 cores) with the worktree's interpreter `.venv/bin/python`.
Pre-fix = a throwaway detached checkout of `079e0aac` (draft spec and plan, no
implementation); post-fix = head `a4359af9`. The throwaway checkout was
removed afterwards.

**Forced race (criterion 1).** Command, ten separate invocations each:

```sh
.venv/bin/python -m pytest tests/test_atomic_test_log.py::test_concurrent_log_snapshots_are_complete -q -p no:cacheprovider
```

- Red, pre-fix: `tests/atomic_test_log.py` and `tests/test_atomic_test_log.py`
  from `a4359af9` copied into the `079e0aac` checkout, so the test drives the
  pre-fix, unlocked `SwarmWorld.calls` observer. 10 of 10 failed, each with
  `AssertionError: JSONDecodeError('Unterminated string starting at: line 1
  column 23 (char 22)')` at the observer assertion: the old observer parsed
  the half-written record.
- Green, `a4359af9`: 10 of 10 passed. The unlocked-reader red control inside
  the test (`pytest.raises(json.JSONDecodeError)` on a plain read at the same
  moment) holds in every green run, so the unsafe variant stays detectable.

**Natural failure under load (criterion 6).** Sixty repetitions in one shell
loop, each a separate invocation:

```sh
for i in $(seq 1 60); do
  .venv/bin/python -m pytest tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call -q -n 4 -p no:cacheprovider
done
```

started together with one background load run in the same checkout,
`.venv/bin/python -m pytest tests/test_stage2_swarm.py -q -n 6 -p no:cacheprovider`.

- Pre-fix `079e0aac`: 60 passed, 0 failed (00:11:32–00:16:17 UTC). The load
  run (224 passed in 120 s, 00:11:32–00:13:33) overlapped repetitions 1–19
  only; repetitions 20–60 ran without the extra load.
- Post-fix `a4359af9`: 60 passed, 0 failed (00:16:32–00:21:12 UTC). The load
  run (224 passed in 120 s, 00:16:32–00:18:32) overlapped repetitions 1–19.

**The natural failure was not reproduced.** Only the forced race was red; the
two main-CI failures named in the spec stay an inferred cause, not a measured
one. The ten-run loop of the section "Verification" (the refused-run test
beside the race test on two workers) was not run separately; the 60-run loop
above stands in for it and is named here as such.

## Criterion ledger

- 1: tests/test_atomic_test_log.py::test_concurrent_log_snapshots_are_complete — a reader observes a forced partial append
- 2: tests/test_atomic_test_log.py::test_concurrent_writers_preserve_every_record — missing, duplicate or damaged large records after writers join
- 3: tests/test_atomic_test_log.py::test_corrupt_log_is_not_hidden — malformed JSON silently becomes a successful observation
- 4: tests/test_atomic_test_log.py::test_missing_log_is_empty — an absent log raises instead of yielding no records
- 4: tests/test_atomic_test_log.py::test_text_appends_preserve_bytes — helper adds a newline or alters scenario text
- 4: not a test — review the 17-site inventory and all corresponding readers/renderings; the five migrated suites verify existing fixture behavior
- 5: tests/test_atomic_test_log.py::test_test_logs_use_the_shared_helper — a bypass remains in the repository inventory
- 5: tests/test_atomic_test_log.py::test_guard_detects_new_unlocked_log_appends — planted direct or embedded bypasses pass, or exact non-log controls fail
- 6: tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call — leak accepted, clean run refused, or notice absent/late
- 7: not a test — review dated red/green and ten-run loaded evidence with commands and commit/patch identity in this plan and the PR

## Runner route — 2026-11-13

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-13 19:17:30–20:17:30 UTC, 3600 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-13 20:17:37–21:01:10 UTC, 2613 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-13 21:01:17–21:38:55 UTC, 2258 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
