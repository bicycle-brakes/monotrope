---
title: "Research — review-loop-deep-a"
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
tags: [research, stage-2, review-loop]
---

# review-loop-deep-a — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), written
on 2026-10-25 by a Claude Code sub-agent of the orchestrating session, on
`fix/review-loop-deep-a` branched from `origin/main` at `f8a6b33`.

## The source

A read-only deep review of the review loop (part A: loop control and
state), run by an Opus 5.5 sub-agent on 2026-10-25 against an archive of
`origin/main` at `f8a6b33`, reproduced every finding below with a test
against the `world` fixture of `tests/test_stage2.py`. Its findings are
numbered DL-A-1 to DL-A-10; the repro tests were scratch and are not in the
repository. The maintainer asked for all ten to be repaired (2026-10-25,
conversation).

## What the runner does today (`scripts/stage2.py` at `f8a6b33`)

- **DL-A-1 (MAJOR).** `free_diff` cuts each file at `FREE_DIFF_MAX_LINES`
  (400) through `_bound_hunks` and the whole diff at `FREE_DIFF_MAX_TOTAL`
  (2000), but reports the cut only as a marker inside the prompt.
  `review_loop` takes its `cut_note` from `bounded_review_diff` alone, so a
  free round over a 1500-line file carries no `The diff was cut:` line,
  `round_was_cut` is false and a clean answer ends the loop — against
  `docs/WORKFLOW.md` §4b ("a round over a cut diff never counts as clean").
- **DL-A-2 (MAJOR).** `implement` passes no findings snapshot and no body
  check to `run_attempts`; `uncommittable` spares the change folder. The
  implementing model can therefore append a forged release block (`Rounds
  run: 1`) or a forged restart line to `findings.md`, and the runner commits
  it. `review_loop` runs its stops before `read_state`, so the forged block
  ends the loop clean with no reviewer call.
- **DL-A-3 (MAJOR, narrow window).** `release` appends the block, then
  `shutil.rmtree`s the record. A crash between the two leaves both; the next
  `release-loop` appends a second block of the same rows, `rounds_run` sums
  both `Rounds run:` lines, and `review_loop` stops clean on a round that
  never ran. The doubled ids also block `repair`.
- **DL-A-4 (MINOR).** `write_round`, `write_state` and `_mark_record_rows`
  use `Path.write_text`, which truncates and then writes. A failed write
  keeps the new snapshot (the stage consumed) without its round. The record
  is the only copy.
- **DL-A-5 (MINOR).** `repair` reads its targets outside the record lock
  and takes the lock only to mark the record after the commit. A release in
  between makes `_mark_record_rows` return silently on `record is None`; the
  committed fix is never booked and the row stays `taken`.
- **DL-A-6 (MINOR).** `release` with no record writes "the loop did not run"
  even when `findings.md` holds `review-loop` audit lines, and the next
  `review-loop` starts a fresh run that replays the consumed free stage
  (ADR 0021 decision 9). A different `XDG_STATE_HOME` is enough.
- **DL-A-7 (MAJOR, doctrine).** `release` accepts any `Phase 6 verdict:`
  line anywhere, so rows of a run after a restart or a continued run are
  released on the old verdict. The ADR 0021 restart amendment: "the new
  run's rows are released after a new phase-6 verdict".
- **DL-A-8 (MINOR, doctrine).** `review_loop` holds the next round only on
  undecided rows; a `taken` row nobody repaired admits the next paid round.
  ADR 0021 decision 6: "The orchestrator decides and repairs before another
  review"; WORKFLOW §4b: `make verify` "must be green before the next round
  starts". `test_round_three_starts_only_after_a_taken_row` relies on the
  old behaviour.
- **DL-A-9 (NIT).** `main` takes the record lock before `folder_of`
  validates the change name, so `review-loop ../../../escaped/x` creates a
  lock file outside the state base and only then refuses.
- **DL-A-10 (NIT).** `mark_consumed` (a two-write path against R-6),
  `taken_in_round` and `released_rows` are not called by any script;
  `taken_in_round` and `released_rows` are called only by tests that test
  them, and `mark_consumed` by nothing.

## Constraints

- No file under `docs/adr/`, `decisions/`, `prompts/` or `AGENTS.md`
  changes in this change: a fix that would need one is an open question in
  `findings.md`.
- `scripts/stage2_availability.py` calls `free_diff` for its empty-diff
  check, and `tests/test_pi_contract.py` builds a free prompt from it; both
  follow a signature change.

## Sources

- The deep-review report (sub-agent hand-back, 2026-10-25) and its scratch
  repro file `tests/test_zz_repro.py` (not committed).
- `scripts/stage2.py` at `f8a6b33`: `free_diff`, `_bound_hunks`,
  `bounded_review_diff`, `review_loop`, `release`, `read_state`,
  `write_round`, `write_state`, `repair`, `mark_repaired_record`,
  `_mark_record_rows`, `main`.
- `docs/WORKFLOW.md` §4b "The review loop (phase 4b)";
  `docs/adr/0021-review-swarms-until-clean.md` decisions 6 and 9 and the
  restart amendment.
