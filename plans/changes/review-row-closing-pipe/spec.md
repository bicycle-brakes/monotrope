---
title: "Spec — review-row-closing-pipe"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-2i9j
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, review-loop, parser]
class: bounded
appetite: 1.5
adr_files: []
---

# Spec — review-row-closing-pipe

A finding line that lacks only its closing pipe is read as a row, and an
answer the runner cannot read is kept and its first unrecognised line named,
so a formatting slip neither fails a reviewer nor erases what it said (bead
coding-harness-2i9j). Research: `research.md`. Decisions: `decisions.md`,
Q-1 (the maintainer, 2026-10-22).

## Problem

On 2026-10-22 three free members wrote five finding lines with a leading
pipe and six cells but no closing pipe; every one failed as malformed. Two
paid stages failed with the same generic message, and their answers were
lost because a refused attempt writes no record (`research.md`).

## Terms

- **Open row:** an answer line that starts with `|`, does not end with
  `|`, splits into exactly six cells after the leading pipe, and has
  `BLOCKER`, `MAJOR` or `MINOR` (any case) in its second cell.
- **Unreadable answer:** a reviewer answer with no readable row that is
  not exactly `No finding.`, and is not empty.

## Acceptance criteria

1. `parse_rows` reads an open row as a six-cell row with the same cells a
   closed line would give.
   *Refuted by:* an open row left in the text, or cells that differ from
   the same line with a closing pipe.
2. The six-cell rule stays strict otherwise: an open line with fewer or
   more than six cells, or without a severity in cell 2, and a line that
   does not start with `|`, stay text.
   *Refuted by:* any such line read as a row.
3. A review-loop round whose members answer with the five open lines F-1
   to F-5 of the 2026-10-22 shape completes with five rows.
   *Refuted by:* a member failure, a refusal, or fewer rows.
4. The failure of an unreadable answer names its first unrecognised line:
   the first non-blank line that `parse_rows` neither read as a row nor
   skipped as table furniture (header or separator), scrubbed and cut to
   200 characters.
   *Refuted by:* a failure message without that line, or with a
   credential.
5. In a written round, each member that failed with an unreadable answer
   has that answer quoted next to its failure line.
   *Refuted by:* a failure line without the quoted answer, or an answer
   that is not quoted (a table line of it read as a row of the round).
6. When the attempt is refused (every member failed, or a malformed table,
   #235), each unreadable answer is appended to `findings.md` as a quoted
   block under its own heading, and no record, snapshot or consumed stage
   is written.
   *Refuted by:* a lost answer, a quoted line read as a round or released
   row, or a written record.

## Non-goals

- Change `split_row` for any table other than reviewer answers.
- Accept F-ids alone, prose without a table, or other row shapes.
- Retry a malformed answer (coding-harness-70rw) or change how a malformed
  row beside a valid one is handled (coding-harness-vque).

## Protected areas

Model endpoints, credentials, leak-check rules, prompts, governance
decisions and ADRs stay unchanged.

## Definition of Done

- Regression tests for criteria 1 to 6, red before the production edit.
- `PYTHON=.venv/bin/python3 make verify` green except the gates this
  container cannot run (named in the pull request).
- The last commit carries `Closes-Bead: coding-harness-2i9j`.
- Special runs: none; tests use local stand-ins without model calls.

## Open decisions

None open.

- [DETAIL] The open-row rule lives in `parse_rows`, not `split_row`:
  only reviewer answers had the slip, and the runner's own tables must
  stay strict.
- [DETAIL] Decision Q-1 (1) says "into the loop record". A written round
  quotes the answer there. A refused attempt writes no record by design
  (ADR 0021 decision 6; #235), so the answer goes to `findings.md`
  instead, the place phase 6 already keeps a rejected answer
  (`rejected_review_block`). Without this the case of 2026-10-22 would
  still lose the paid answers.
- [DETAIL] Q-1 (4) asks for "exactly these five lines". Their text lives
  in the maintainer's local loop record, which this session cannot read;
  the test uses five lines of exactly that shape (F-1 to F-5, six cells,
  leading pipe, no closing pipe).
- [DETAIL] Appetite 1.5 hours of phase 4: one parser branch, one error
  field and two places that keep an answer.
