---
title: "Findings — review-loop-deep-a"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: to be filed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2, review-loop]
---

# Findings — review-loop-deep-a

## Implementation, 2026-10-25

Implemented by hand by a Claude Code sub-agent (Opus 5.5) of the
orchestrating session, in a cloud container, at the maintainer's
instruction of 2026-10-25. No foreign model was called.

**Red first.** The 24 new or rewritten tests the ledger names were run
against an archive of `origin/main` at `f8a6b33` with only
`tests/test_stage2.py` replaced: 22 failed, 2 passed. The two that passed
are guards: `test_an_invalid_change_name_takes_no_lock[review]` and
`[repair]` — `review` already validated the name before its lock, and
`repair` took no lock before this change. Every other test failed on the
defect it names (a `ValueError` unpacking the old one-value `free_diff`, a
committed forgery, a clean stop, a doubled block, a changed record, a free
lock, a silent return, a written no-loop line, a release on the old
verdict, a started round, a lock file, a defined helper).

**Green.** `tests/test_stage2.py` at the commit of this file: 903 passed,
1 failed (`test_an_unreadable_target_is_named_by_its_repository_path`,
the known root-only failure of this container). The full suite: 2518
passed, 30 skipped, 3 failed and 16 errors; the 16 errors are
`tests/test_pi_contract.py` (Node 22, known); the 3 failures are the
root-only test, `test_the_plans_registry_staleness_check_runs_green_here`
(the suite started before `plans/INDEX.md` was regenerated; green alone
afterwards) and `test_ineligible_paid_models_are_skipped_and_named` (a
stand-in race, see "Side findings"; green alone three times).

## Per finding

- **DL-A-1, fixed (criterion 1).** `free_diff` returns `(diff,
  cut_note)`; `review_loop` merges the note into `cut_note`.
  `scripts/stage2_availability.py`, `probe` and `tests/test_pi_contract.py`
  read the diff half.
- **DL-A-2, fixed (criteria 2 and 3).** `findings_body_problem` is
  repair's body check, now shared; `implement` passes it as its answer
  check with `snapshot_findings` and `restore_findings`. `read_state`
  refuses a released block without a `Loop state:` line, and
  `review_loop` reads the snapshot before its stops.
- **DL-A-3, fixed (criterion 4).** A `Record digest:` line in every
  release block; the plan says why not a tombstone. A repeated release
  returns the record's rows, so a `review` re-run after such a crash
  still asks the reviewer for their marks.
- **DL-A-4, fixed (criterion 5).** `replace_record` writes a temporary
  file and renames it (`Path.replace`, which is `os.replace`; ruff's
  PTH105 asks for the `Path` spelling). `write_round` writes a fresh
  record's heading and snapshot in its one write, so `write_state` lost
  its last caller and went with DL-A-10. The record file is now created
  with mode 0600 (`mkstemp`); it lives in the user's state directory.
- **DL-A-5, fixed (criterion 6).** `main` holds the record lock around
  the whole `repair`; `mark_repaired_record(..., lock_held=True)` does not
  take it a second time (a second `flock` on a new descriptor in the same
  process would refuse). `_mark_record_rows` raises `CallFailed` naming
  the ids when the record is gone. Consequence: `review-loop`,
  `release-loop` and `review` refuse while a repair runs.
- **DL-A-6, fixed with one addition (criterion 7).** Release-loop, the
  release inside `review` and `review-loop` refuse with no record when a
  review-loop audit line stands after the last release, restart and
  no-round line, naming the expected record path. *Addition:* a
  `review-loop` call that wrote its audit lines and then ended without a
  round (every member failed, a leak block of a replacement, an
  interrupt) appends `Loop attempt: <date> — no round was written; …`.
  Without it the refusal would block the retry after an all-failed
  attempt, which ADR 0021 decision 6 allows (spec [DETAIL]); without it
  `test_a_call_without_an_answer_is_not_a_round` failed.
- **DL-A-7, fixed (criterion 8).** A release of a record needs a verdict
  line after the last release block and the last restart line. With no
  record the old rule stands (nothing is released).
- **DL-A-8, fixed (criterion 9).** `review_loop` refuses the next round
  while a row of the run after the floor (record or released) has a
  Status beginning `taken`, naming the ids. The check runs after the
  spent-stage stop: with no stage left there is no next round to hold,
  and the spent-ladder report stays the one the maintainer sees
  (`test_round_history_survives_split_releases_and_config_edits`).
- **DL-A-9, fixed (criterion 10).** `main` calls `folder_of` before the
  lock for `review-loop`, `release-loop`, `prepare-loop`, `review` and
  `repair`.
- **DL-A-10, fixed (criterion 11).** A grep over `scripts/` and `tests/`
  found `mark_consumed` called nowhere, and `taken_in_round` and
  `released_rows` called only by tests of those helpers. All three are
  deleted, with `write_state` (DL-A-4). Their tests read the runner's live
  functions now: `findings_rows(...)[0]` for `released_rows`,
  `accepted_row` and `clean_round` for `taken_in_round`. The ADR 0015
  supersession sentence of `taken_in_round`'s docstring moved to
  `accepted_row` (the doctrine test requires the runner to carry it).

## Tests changed because the behaviour changed

- **DL-A-8.** `test_round_three_starts_only_after_a_taken_row` relied on
  a taken round-2 row admitting round 3. It now asserts the refusal while
  the rows are taken and round 3 after they are marked `fixed`. About 35
  loop tests seeded `taken — test_a` rows (directly or through
  `decide_record`) only to make a round not clean before the next one;
  they now seed `FIXED` (`fixed — tests/test_x.py::test_y`), which keeps
  the round accepted (not clean, counted by the repair brake) and is the
  state the doctrine requires before the next round. Tests about repair
  itself keep their taken rows.
- **DL-A-6.** Five tests deleted the record to start a change over
  (`test_the_opencode_key_never_leaves_the_runner`,
  `test_free_discovery_forces_live_refresh_before_listing`,
  `test_free_selection_changes_in_yaml_without_runner_edits`,
  `test_ineligible_paid_models_are_skipped_and_named`,
  `test_reordering_the_ladder_touches_no_code`); with the run's audit
  lines left in findings.md that is now a lost record. They remove
  findings.md too (`forget_the_run`).
  `test_every_prompt_asks_to_read_nothing_outside` marks its released
  round-1 row fixed before the next round (DL-A-8).
- **DL-A-4.** `test_the_round_and_its_consumed_stage_land_in_one_write`
  counted two `write_text` calls to loop.md (snapshot, then round); it
  now counts one `replace_record` and no `write_text`.
- **DL-A-5.** The `mark_repaired_record` spy of
  `test_the_record_is_marked_only_after_the_checkpoint_commit` accepts
  the new keyword.

## Open questions

- **A record lost for good blocks the change (DL-A-6).** The refusal
  names the expected path; if the record cannot be found (a killed
  process before any round line, a deleted state directory), no verb
  continues: `release-loop --restart` needs a completed round in
  findings.md. Whether the maintainer wants an explicit command for that
  case is their decision; it would touch ADR 0021 decision 9 and is not
  built here.
- **Doctrine text.** `docs/WORKFLOW.md` §4b already says the next round
  waits for the repair and that a release follows the verdict; it does
  not name the record digest, the no-round line or the lost-record
  refusal. No ADR, `prompts/` or `AGENTS.md` text needed a change.

## Side findings (not now)

- The pi stand-in of `tests/test_stage2.py` reads `calls.jsonl` while a
  parallel member appends to it; under load a member can read a half
  line and fail (`JSONDecodeError`), which turned
  `test_ineligible_paid_models_are_skipped_and_named` red once in the full
  suite. Pre-existing; the test is green alone.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review. The
review loop and the phase-6 Codex review are owed.

- The no-round line is written only after an audit line of the same call,
  inside `except BaseException`, and a failing append is suppressed so it
  never hides the original error.
- `released_digest` reads the runner's own lines only (cut at `Kept from
  the loop record:`), so a reviewer's quoted digest cannot stand in.
- A forged release block with a copied state line would still be read;
  criterion 2 keeps the implementing model from writing one, and the
  repair already had the same check.
