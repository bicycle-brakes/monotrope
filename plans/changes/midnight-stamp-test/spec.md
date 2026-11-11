---
title: "Spec — midnight-stamp-test"
status: draft
implementation_status: none
date: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, make-verify]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — midnight-stamp-test

The goal in one sentence: every test that compares a runner-written `updated:`
stamp against a date it took itself compares against one date it set, so a
verify run that crosses local midnight stays green (bead
coding-harness-bxxt.5). Research: `research.md`. Decisions: `decisions.md`.

## Problem

All points read on 2026-11-10 in `research.md`, "What exists today":

- `tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current`
  takes the calendar date once (`tests/test_stage2.py:1735`) and compares it
  with stamps that three runner verbs write later; a full check crossing local
  midnight failed on 2026-11-09 at 23:22 UTC on
  `assert date(2026, 11, 10) == date(2026, 11, 9)`, and one lost run costs
  about 25 minutes of the one verify slot.
- Eight sibling tests take a date in the test and compare it with a stamp
  written after it: five in-process comparisons in `tests/test_stage2.py`
  (lines 1950, 5775, 11884, 21256 and 24736-24764), one through a planted
  subprocess make stand-in that reads its own clock
  (`tests/test_stage2.py:1913`), and one in `tests/test_workflow_entry.py:95`.
  Each fails the same way when its window crosses local midnight.
- The repository already pins clocks in tests — named seams
  (`stage2.terms_today`, `utc_now`, `monotonic_now`) and the module-attribute
  precedent of `tests/test_stage2_terms_expiry.py:159-160` — but none of these
  tests uses any of them.

## Terms

- **Stamp:** the `updated:` date the runner writes into a document header
  (`check_frontmatter_current.stamped` / `.stamp`, called from
  `scripts/stage2.py`).
- **Pinned date:** one date a test sets for the code under test and uses on
  its own side of the comparison; neither side reads the calendar clock
  itself.
- **Guard test:** the new source-reading test that holds criterion 5.

## Acceptance criteria

1. When
   `tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current`
   runs while the date it controls moves between the runner verbs it drives,
   every `updated:` stamp it asserts equals the date current at that write.
   *Refuted by:* the runner stamps a date other than the one current at the
   write — the captured-before-the-move form that failed on 2026-11-09, or a
   stale stamp — and the test goes red.

2. While any of the five in-process sibling tests runs
   (`test_preparation_stamps_only_changed_held_documents`,
   `test_filling_the_marks_keeps_the_updated_stamp_current`,
   `test_runner_detaches_matching_hardlinked_plan_before_stamp`,
   `test_the_release_reconcile_refreshes_the_findings_date` and
   `test_review_accepts_runner_audit_date_stamp`, all in
   `tests/test_stage2.py`), the `updated:` date each asserts against is the
   one pinned date that test set for the code under test.
   *Refuted by:* any of the five reads the calendar clock on its own side of
   the comparison — as `tests/test_stage2.py:1950`, `:5775`, `:11884`,
   `:21256` and `:24736-24764` do today — and the pinned comparison or the
   guard test goes red.

3. When `checking_derived_make` plants its subprocess make stand-in, the stamp
   date the stand-in expects is baked into the planted script from the pinned
   date the calling test set, and both tests using it
   (`test_first_implement_refreshes_derived_files_without_a_model_repair` and
   `test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics`)
   stay green with the runner stamping that date.
   *Refuted by:* the stand-in reads its own process clock — as
   `tests/test_stage2.py:1913` does today — and the guard test goes red, or a
   stamp from any other day makes the stand-in refuse and the two tests fail.

4. While `tests/test_workflow_entry.py::test_new_change_creates_the_folder_and_a_current_index`
   runs, the scaffold's `updated:` date it asserts is the pinned date the test
   set for `new_change`, not a calendar read after the write.
   *Refuted by:* the assertion re-reads `date.today()` after
   `new_change.main` wrote the scaffold — as
   `tests/test_workflow_entry.py:95` does today — and the guard test goes
   red.

5. If any of the nine tests named above or the `checking_derived_make` helper
   reintroduces a calendar-clock read (`date.today(`) in its own body, the
   guard test `tests/test_stage2.py::test_stamp_tests_pin_the_date_they_compare`
   goes red.
   *Refuted by:* a `date.today(` read added back into one of the named
   functions or the helper leaves the guard test green.

6. While the change is built, no file under `scripts/` changes: the runner
   reads the calendar date for its stamps exactly where it did before.
   *Refuted by:* the pull request's file list names a path under `scripts/`.

## Non-goals

- No production change: the four inline `dt.date.today()` stamp reads in
  `scripts/stage2.py` (lines 1199, 1234, 3202 and 5387) stay where they are,
  and the stamp keeps its local-zone meaning; no named seam is introduced for
  them.
- The `review_audit_only` re-stamp at check time (`scripts/stage2.py:3202`)
  is not repaired: its seconds-wide window is stated as a Boundary below, and
  the pull request proposes a follow-up bead instead.
- No new clock framework: no `tests/conftest.py`, no freezegun dependency, no
  environment-variable clock override; the pin follows the existing
  module-attribute precedent of `tests/test_stage2_terms_expiry.py:159-160`.
- Tests the exploration classified as not this class
  (`tests/test_archive_closed_changes.py`, `tests/test_feedback_channel.py`,
  `tests/test_frontmatter_current.py`, `tests/test_harness_decide_adr.py`,
  `tests/test_run_report.py`) are not touched.

## Protected areas

- Everything under `scripts/` — the bead is a test bug; the stamps the runner
  writes are correct (`decisions.md`, "Decided by the agent").
- Every file under `tests/` except `tests/test_stage2.py` and
  `tests/test_workflow_entry.py`.
- `templates/`, `prompts/`, `docs/`, other change folders and the tracker: no
  document changes with this code.

## Boundary

`review_audit_only` (`scripts/stage2.py:3184-3205`) re-stamps the before-bytes
with `dt.date.today()` at check time and compares them with the after-bytes,
so an append stamped immediately before local midnight and checked immediately
after it would be refused as not audit-only. The window is seconds within one
verb, no incident is recorded, and repairing a production check is scope this
bead does not carry; the pull request proposes a follow-up bead for it.

## Definition of Done

- `make verify` green.
- Moved in the same pull request: `tests/test_stage2.py`,
  `tests/test_workflow_entry.py` and this change's spec/plan bookkeeping —
  none else.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- The pull request proposes the follow-up bead for the `review_audit_only`
  boundary, closes coding-harness-bxxt.5, and its last commit carries the
  trailer `Closes-Bead: coding-harness-bxxt.5`.
- Special runs: none; everything runs in the ordinary suite.

## Open decisions

None open.

- [DETAIL] The pin follows the terms-expiry precedent: a `dt.date` subclass
  overriding only `today()`, patched onto the shared `datetime` module
  attribute, which every `dt.date.today()` read in `scripts/stage2.py` and in
  the test resolves at call time. Reason: it reaches all four stamp sites and
  the test's own reads without touching production, and the precedent is
  green in the suite; `tests/test_workflow_entry.py` binds its comparison to
  the pinned value directly because its `from datetime import date` is
  import-bound.
- [DETAIL] A shared pin helper lives in `tests/test_stage2.py`, holding the
  settable date the bead's test moves between its verbs, and
  `tests/test_workflow_entry.py` carries the same few lines locally. Reason:
  no cross-test-module import convention exists in `tests/`, and a shared
  module for three lines is more structure than the fix needs.
- [DETAIL] The guard test reads the two test files as text — the reading
  style of `scripts/check_criterion_ledger.py` — and scans the nine named
  bodies and the helper for `date.today(`. Reason: the pinned tests are green
  by construction, only a source scan catches a regression deterministically,
  and no advancing-clock meta-run can reach the subprocess stand-in.
- [DETAIL] Two hours of phase 4, repair rounds included — nine small test
  edits, one helper and one guard test in a large file.
