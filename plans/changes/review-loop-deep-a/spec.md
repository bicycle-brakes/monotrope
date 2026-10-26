---
title: "Spec — review-loop-deep-a"
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
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 4
adr_files: []
---

# Spec — review-loop-deep-a

The review loop's control and state hold what the doctrine says they hold:
a cut free round is never clean, the implementing model cannot forge loop
state, a release cannot run twice or on an old verdict, a record write is
whole or absent, a repair always books its fix, a lost record stops the
loop instead of replaying it, and the next round waits for the repair
(deep review part A, DL-A-1 to DL-A-10). Research: `research.md`;
decisions: `decisions.md` Q-1 to Q-9.

## Terms

- **Run after the floor:** the rounds after the last `Loop restarted:` line
  (`restart_floor`), from the record and from every released block.
- **Review-loop audit line:** a line that begins `Stage-2 call, <date>:
  review-loop ·` — the runner's line before each review-loop member call.
- **No-round line:** the runner's line `Loop attempt: <date> — no round was
  written; …`, appended when a review-loop call wrote audit lines and then
  ended without writing its round.

## Acceptance criteria

1. **A cut free diff is a cut round (DL-A-1, Q-8).** `free_diff` returns
   the diff and a cut note whenever it cut a file at `FREE_DIFF_MAX_LINES`
   (the note names the file) or the diff at `FREE_DIFF_MAX_TOTAL`; it
   returns no note when nothing was cut. `review_loop` merges that note
   with `bounded_review_diff`'s into the round's `The diff was cut:` line,
   so a clean answer over such a round does not end the loop.
   *Refuted by:* a free round over a 1500-line file without a cut line, or
   a second `review-loop` that exits clean after it.
2. **Implement cannot change findings.md (DL-A-2, Q-4).** An implement
   attempt whose model changed `findings.md` outside its frontmatter fails
   its post-run check with repair's body check (`findings_body_problem`),
   findings.md is restored, and no commit carries the edit; a later attempt
   that leaves findings.md alone is committed.
   *Refuted by:* a commit holding a release heading or restart line the
   model wrote, or a failed attempt that leaves the edit in the tree.
3. **The snapshot is read before the stops (DL-A-2, Q-4).** `review_loop`
   reads the run's snapshot before its stops; a released block without a
   `Loop state:` line refuses the run, naming the missing line, before any
   reviewer call.
   *Refuted by:* a clean stop, or a reviewer call, over a release block
   that carries `Rounds run:` but no state line.
4. **Release is idempotent (DL-A-3, Q-3).** Every released block carries
   the runner's line `Record digest: sha256:<hex>` of the record it
   released. A `release-loop` whose record's digest equals the last
   released block's appends nothing, removes the record and reports it,
   whatever verdict stands; `Rounds run:` is then counted once. Every block
   also carries `Record identity: sha256:<hex>`, computed from its round
   headings and the first seven cells of each record row, excluding Status
   and Broke a test. If that identity matches the last block but the digest
   differs, release rewrites that block in place from the record (including
   statuses, snapshot, kept words and digest), preserving its heading and
   Phase 6 cells, then removes the record; it appends no second block and
   needs no new verdict.
   *Refuted by:* two release blocks of one record, or a record kept after
   the second call.
5. **A record write is whole or absent (DL-A-4, Q-5).** `write_round` and
   the repair's record marking write a temporary file in the record's
   directory and `os.replace` it over `loop.md`; a write that fails leaves
   the record byte for byte as it was and no temporary file behind. A
   fresh record's header, snapshot and first round are one write.
   *Refuted by:* a record with the new snapshot and not the new round, or
   a leftover temporary file, after a write that failed midway.
6. **Repair holds the record (DL-A-5, Q-6).** `repair` holds the record
   lock from its first record read through the marking of the record; a
   record gone when the marking runs fails the run with `CallFailed`, naming
   every id the record should have carried.
   *Refuted by:* a free lock during the repair's model call, or a silent
   return when the record is gone.
7. **A lost record stops the loop (DL-A-6, Q-7).** With no record, a
   review-loop audit line after the last release, restart and no-round
   line refuses `release-loop` (and the release inside `review`) and
   `review-loop`, naming the expected record path. A review-loop call that
   wrote audit lines and then ended without its round appends a no-round
   line, so a retry after an attempt whose every member failed still runs.
   *Refuted by:* a no-loop line or a fresh round 1 written over a lost
   record, or a refused retry after an all-failed attempt.
8. **A release needs its own verdict (DL-A-7, Q-2).** A release of a
   record needs a `Phase 6 verdict:` line that begins after the last
   released block and after the last restart line.
   *Refuted by:* a release of a restarted or continued run on the verdict
   of an earlier release.
9. **Repair before the next round (DL-A-8, Q-1).** `review-loop` refuses
   the next round, before any reviewer call, while a row of the run after
   the floor — in the record or in a released block — has a Status that
   begins `taken`, naming the ids; a row marked `fixed` admits it.
   *Refuted by:* a round started over an unrepaired taken row.
10. **The change name before the lock (DL-A-9, Q-9).** `review-loop`,
    `release-loop`, `prepare-loop`, `review` and `repair` validate the
    change name before they take the record lock: an invalid name refuses
    and creates no lock file.
    *Refuted by:* a lock file written for `../../../escaped/x`.
11. **No dead loop helper (DL-A-10, Q-9).** `mark_consumed`,
    `taken_in_round`, `released_rows` and `write_state` are gone from
    `scripts/stage2.py`; the tests that read them read the runner's live
    functions instead.
    *Refuted by:* any of the four still defined.

## Non-goals

- The availability receipt, probes and their timing (part B of the deep
  review, not read here).
- Real multi-process races beyond the lock tests.
- A command that recovers a record lost for good (criterion 7 refuses;
  recovery is the maintainer's).

## Definition of Done

- Tests red before the edit; `tests/test_stage2.py` and the full suite
  green except the two known container-only failures.
- Every criterion has a ledger line in `plan.md`.

## Open decisions

None open.

- [DETAIL] The no-round line (criterion 7): without it, an attempt whose
  every member failed leaves audit lines and no record, and Q-7's refusal
  would block the retry ADR 0021 decision 6 allows. The line marks exactly
  the attempts that wrote no round.
- [DETAIL] Digest over tombstone (criterion 4): see `plan.md`.
