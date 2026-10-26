---
title: "Plan — review-loop-deep-a"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: to be filed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — review-loop-deep-a

```text
For you:     The review loop can no longer end clean on a cut diff, a forged or doubled release, or a lost record, and waits for the repair.
Done when:   Every criterion has a test that was red first (or a guard), and tests/test_stage2.py plus the full suite are green.
Appetite:    4 hours of phase 4; stop at the limit.
Not now:     The availability receipt and probes (deep review part B); a recovery command for a record lost for good.
Pre-mortem:  suppose it failed: most likely because repairing before each round breaks many loop tests that seeded taken rows.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the tests the ledger names, red before the
   edit; tests that relied on the old behaviour adapted (see
   `findings.md`).
2. `scripts/stage2.py`:
   - `free_diff` returns `(diff, cut_note)`; `review_loop` merges the note
     into `cut_note` (criterion 1).
   - `findings_body_problem`, shared by `check_repair_answer` and a new
     answer check of `implement`, which also passes `snapshot_findings` and
     `restore_findings` to `run_attempts` (criterion 2).
   - `read_state` refuses a released block without a `Loop state:` line;
     `review_loop` reads the snapshot before its stops (criterion 3).
   - `release` writes `Record digest:`; `released_digest` and
     `record_digest` make a repeated release a removal only (criterion 4).
   - `replace_record` (temporary file, `os.replace` through
     `Path.replace`); `write_round` writes a fresh record's heading and
     snapshot in its one write; `_mark_record_rows` uses `replace_record`
     and raises naming the ids when the record is gone (criteria 5, 6).
   - `main` validates the change name before the lock for the five record
     verbs and holds the lock around `repair`; `mark_repaired_record` takes
     `lock_held` (criteria 6, 10).
   - `lost_record_refusal` in `release` and `review_loop`; `review_loop`
     appends the no-round line when it ends after its audit lines without a
     round (criterion 7).
   - `release` needs a verdict after `_last_release` and `_last_restart`
     (criterion 8).
   - `review_loop` refuses the next round over unrepaired taken rows, after
     the spent-stage stop (criterion 9).
   - `mark_consumed`, `taken_in_round`, `released_rows` and `write_state`
     deleted (criterion 11).
3. `scripts/stage2_availability.py` and `tests/test_pi_contract.py`: read
   the diff half of `free_diff`.
4. This change folder and `plans/INDEX.md`.

## Why a digest and not a tombstone (criterion 4)

A tombstone rename before the append moves the only copy of the record
out of the place every reader looks: a crash after the rename and before
the append leaves a record nobody reads and no release — the very loss
criterion 7 refuses. The digest keeps the order append-then-delete, so
every crash point leaves either the record alone (nothing appended yet;
the next call appends) or the record and its block (the next call sees
the digest and only deletes). It costs one runner line per block, read
from the runner's own lines only (cut at `Kept from the loop record:`).

## Why `write_state` goes (criterion 5)

`write_round` already holds the snapshot line; a fresh record took a
second write through `write_state` first, a window like the one R-6
closed. Writing the heading and the snapshot inside `write_round` makes a
fresh record one replace too, and leaves `write_state` without a caller.

## Verification

```sh
.venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/test_stage2.py
.venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/
.venv/bin/ruff check scripts tests && .venv/bin/ruff format --check scripts tests
python3 scripts/check_criterion_ledger.py
```

## Criterion ledger

- 1: tests/test_stage2.py::test_free_diff_reports_its_own_cut — free_diff returns no cut note for a file cut at 400 lines or a diff cut in total.
- 1: tests/test_stage2.py::test_a_free_round_over_a_cut_file_is_never_clean — the free round over a cut file carries no cut line and the next call stops clean.
- 2: tests/test_stage2.py::test_implement_cannot_write_findings — an implement attempt that wrote a release block, restart line or verdict line is committed.
- 3: tests/test_stage2.py::test_a_release_block_without_its_snapshot_refuses_the_loop — a release block without its state line ends the loop clean or reaches a reviewer.
- 4: tests/test_stage2.py::test_a_release_repeated_after_a_crash_appends_nothing — a second release-loop after a crash appends the rows again or keeps the record.
- 5: tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was — a write that fails midway changes the record or leaves a temporary file.
- 5: tests/test_stage2.py::test_a_fresh_record_is_written_whole_in_one_write — a fresh record takes two writes, or its heading and snapshot are missing.
- 6: tests/test_stage2.py::test_repair_holds_the_record_lock_for_its_whole_run — the record lock is free during the repair's model call or record read.
- 6: tests/test_stage2.py::test_marking_a_vanished_record_names_the_ids — marking a vanished record returns silently.
- 7: tests/test_stage2.py::test_a_lost_record_stops_release_and_the_loop — a lost record is released as no loop, or the next run replays round 1.
- 7: tests/test_stage2.py::test_an_attempt_without_a_round_leaves_a_line_and_admits_the_retry — an all-failed attempt leaves no no-round line, or its retry is refused.
- 8: tests/test_stage2.py::test_a_release_after_a_restart_needs_a_new_verdict — the restarted run's rows are released on the earlier verdict.
- 8: tests/test_stage2.py::test_a_continued_run_needs_a_verdict_after_the_last_release — a continued run is released on the verdict before the first release.
- 9: tests/test_stage2.py::test_the_next_round_waits_for_the_repair — a round starts over an unrepaired taken record row, or a fixed row does not admit it.
- 9: tests/test_stage2.py::test_a_released_taken_row_also_holds_the_next_round — a released taken row admits the next round.
- 9: tests/test_stage2.py::test_round_three_starts_only_after_a_taken_row — a taken round-2 row admits round 3 before its repair.
- 10: tests/test_stage2.py::test_an_invalid_change_name_takes_no_lock — a lock file is written for an escaping change name.
- 11: tests/test_stage2.py::test_the_dead_loop_helpers_are_gone — a deleted helper is still defined.

## Route

Research, spec, plan, implementation and self-review by a Claude Code
sub-agent (Opus 5.5) of the orchestrating session in a cloud container on
2026-10-25, at the maintainer's instruction. The review loop and the
phase-6 Codex review are still owed.

## Time used

2026-10-26 00:30:30–00:47:48 UTC, 1038 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
