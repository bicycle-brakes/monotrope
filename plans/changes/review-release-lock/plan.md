---
title: "Plan — review-release-lock"
status: draft
implementation_status: partial
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-751
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, record-lock]
---

# Plan — review-release-lock

```text
For you:     A competing review refuses before calling a model and leaves the loop record and findings intact.
Done when:   Contention, continuous ownership and lock cleanup have regression tests, normal review still works, and make verify is green.
Appetite:    1 hour of phase 4, repairs included; stop at the limit.
Not now:     Review-answer validation, other record verbs, waiting, retries or transactional release.
Pre-mortem:  suppose it failed: most likely because the lock starts only at release and leaves the checked record open to change during review.
Starts unless you say stop.
```

## Files and steps

1. Change `tests/test_stage2.py`: add the four regression functions named
   below, using `World`, scripted Codex stand-ins and real nonblocking locks;
   add an invalid-change regression during repair.
2. Change `scripts/stage2.py`: dispatch `review` inside
   `with holding_record(args.change, Path(args.root))` in `main`, following
   `prepare-loop` and `release-loop`; update the adjacent comment to reflect
   review's ownership. Validate the change with `folder_of` before taking
   the lock, so invalid names cannot create lock paths. Keep `release` and
   the review body unchanged.
3. Update `plans/changes/review-release-lock/plan.md`: convert pending ledger
   entries as tests land; the runner appends measured time below, maintains
   `plans/changes/review-release-lock/findings.md` and regenerates
   `plans/INDEX.md`. No implementation file is created or deleted.

## Implementation contract

- Use the existing worktree-specific lock beside the record directory, once
  for the whole CLI review invocation, including loop marking. Do not lock
  `release` separately: `release-loop` already owns the same lock.
- For contention, seed a decided record with an extra sentinel and existing
  findings, snapshot all record files and findings, then hold its real lock
  and call `world.run("review")`. Assert exit 2, the existing diagnostic,
  no model calls, and identical bytes and file existence. Parameterize absent
  findings and absent records too. Use a bounded test deadline to expose waiting.
- Observe the initial `read_record`, verdict `run_codex`, verdict `append`
  and `release` with delegating wrappers; at each boundary attempt a separate
  nonblocking acquisition of the same lock. Check before and after the real
  release to cover directory removal; never replace `holding_record` itself.
- Cover successful review with decided rows and without a record, asserting
  exit 0, verdict before release, rows released once, record directory removed,
  expected marks and the existing no-loop marker. Retain existing verdict and
  session regression tests.
- After success, undecided-row refusal, verdict-call failure and marks-call
  failure, independently acquire the same lock. Assert the original exit
  code and call count too, so cleanup cannot hide a failure or invoke a retry.
- Do not touch prompts, endpoints, record format, other verbs, ADRs or
  governance files. No design or ADR is due for this bounded fix. Explore
  ran in the orchestrating session for this reproduced finding. The Stage-1
  fallback ran after two Flash post-run checks failed, as recorded below.

## Verification

Run the new contention and continuous-ownership tests before the production
edit to demonstrate failure, then all four regressions and the existing
review tests after it. Use only stand-ins, never real model endpoints.

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'review_refuses_a_held_record_lock or review_holds_record_lock_through_release or review_lock_preserves_normal_flow or review_releases_record_lock_on_exit or no_loop_row_reaches_the_verdict_call or codex_marks_each_loop_row_after_its_verdict or a_failed_mark_call_leaves_the_marks_empty or review_is_refused_while_a_loop_row_is_undecided'
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_review_refuses_a_held_record_lock — review waits, returns another exit or diagnostic, or invokes a model while the lock is held.
- 2: tests/test_stage2.py::test_review_refuses_a_held_record_lock — contention changes record files or findings bytes or existence.
- 3: tests/test_stage2.py::test_review_holds_record_lock_through_release — a separate acquisition succeeds at a read, verdict or release boundary, or a boundary is no longer observed.
- 4: tests/test_stage2.py::test_review_lock_preserves_normal_flow — an uncontended review refuses, changes ordering, duplicates rows, retains its record or breaks the no-record path. Existing regression relied on: tests/test_stage2.py::test_codex_marks_each_loop_row_after_its_verdict — marking changes the verdict or loses expected marks.
- 5: tests/test_stage2.py::test_review_releases_record_lock_on_exit — the lock stays held after a successful or exceptional return.

## Runner route — 2026-10-24

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-24 02:50:54–03:06:03 UTC, 909 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-24 03:06:07–03:17:37 UTC, 690 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-24 03:17:41–03:23:24 UTC, 342 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-24 05:12:37–05:23:51 UTC, 674 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
