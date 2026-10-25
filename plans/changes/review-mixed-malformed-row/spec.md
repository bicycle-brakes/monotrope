---
title: "Spec — review-mixed-malformed-row"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-vque
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 1
adr_files: []
---

# Spec — review-mixed-malformed-row

A finding line the runner cannot read refuses the review round even when
the same answer holds readable rows, so it can never drop out undecided
and let the loop end clean (bead coding-harness-vque). Research:
`research.md`.

## Terms

- **Finding-shaped line:** a line that starts with `|` and has `BLOCKER`,
  `MAJOR` or `MINOR` (any case) in its second cell, closed or not.
  Widened on 2026-10-25 by criteria 4 to 6: after blockquote or list
  markers, also with the severity in cell 1 when the line has four or
  more cells, and not inside a fenced example.

## Acceptance criteria

1. An answer with a readable row and a finding-shaped line that is no row
   refuses the round with #235's refusal, naming the member and the line;
   no record is written.
   *Refuted by:* a written round, or a refusal without the member or line.
2. A table without a severity in cell 2 beside readable rows (a summary
   table) keeps the existing treatment: the round stands.
   *Refuted by:* a refusal of such an answer.
3. An answer whose only finding-shaped line is unclosed or has the wrong
   cell count refuses the round as in criterion 1, also without a readable
   row beside it. A severity decorated with `*`, `_` or a trailing `:`
   counts as a severity. Added after runner review R-2 and pre-review row
   P238-1, 2026-10-25.
   *Refuted by:* such an answer treated as an ordinary failed member, so a
   peer's `No finding.` ends the round clean.
4. A line is finding-shaped also behind blockquote or list markers (`>`,
   `-`, `*`, `+`, `1.`, nested): beside readable rows or alone, it refuses
   the round as in criteria 1 and 3. A quoted or listed complete six-cell
   row is refused the same way, not read as a row. A line without a
   leading `|` stays out of scope. Added from rows P235-1 and the first
   2026-10-25 known limit, 2026-10-25.
   *Refuted by:* a round written beside such a line, or a quoted row read
   as the reviewer's row.
5. A line whose cell 1 is a (possibly decorated) severity and that has at
   least four cells is finding-shaped, so a finding with its ID column
   missing refuses the round; a summary keyed by severity with two or
   three cells keeps it (criterion 2). Added from row P238-2, 2026-10-25.
   *Refuted by:* a round written beside `| BLOCKER | CODE | c | loc | f |`,
   or a refusal of `| MAJOR | 1 |` or `| MAJOR | 1 | 0 |` beside rows.
6. A fenced code block (backtick or tilde fences, CommonMark rules) from
   which the parser reads no row is a format example: its lines do not
   refuse a round that has readable rows. A fenced block that holds a row
   is the reviewer's table and is checked like any other, and an answer
   without readable rows is checked fences included. Added from row
   P238-3, 2026-10-25.
   *Refuted by:* a refusal for a fenced example beside rows, or a written
   round when a fenced table holds a malformed finding line.
7. Phase 6 (`review`) and phase 2a (`spec-review`) use the same check
   (`unread_finding_lines`): an answer with readable rows and a
   finding-shaped line that is no row is refused before any verdict or
   block is appended — phase 6
   keeps it as a rejected phase-6 answer, phase 2a appends nothing, as for
   a failed call. Added from row P238-4, 2026-10-25.
   *Refuted by:* a `## Phase 6` or `## Phase 2a` block, a verdict line or
   a release after such an answer.

## Non-goals

- Carry an unreadable line as an undecided row (the bead's second route).
- Change how an answer without any finding-shaped line is handled (#235,
  #236). Criteria 3, 4 and 7 change the case with one, on purpose.

## Known limits (2026-10-25)

- A finding line without a leading `|` (`R2-1 | MAJOR | …`) is not
  caught: prose with a pipe and a severity word is too common for a cheap
  rule to tell apart, so such an answer stays an unreadable answer or
  commentary (#236).
- By design, a 2-to-5-cell table line outside a fence with a severity in
  cell 2 beside readable rows refuses the round, also when it is a
  summary keyed by ID or prose such as `| note | minor | …`; so does a
  summary keyed by severity with four or more cells (criterion 5).
- The table parser reads six-cell rows inside fences too, so a fenced
  example that is a complete six-cell row becomes a row to decide
  (criterion 6 explains why).
- A fenced malformed line beside rows outside the fence is taken for an
  example and does not refuse (criterion 6).

## Definition of Done

- Tests red before the edit; `PYTHON=.venv/bin/python3 make verify` green
  except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-vque`.

## Open decisions

None open.

- [DETAIL] Refuse rather than carry: the 2026-10-16 answer on
  coding-harness-6jg (research).
- [DETAIL] Only finding-shaped lines refuse beside rows, so a reviewer's
  summary table does not throw away a paid round.
- [DETAIL] A quoted or listed complete row is refused, not read
  (criterion 4): a reviewer quotes rows of an earlier round or of the
  spec, so reading it would plant a finding nobody made; dropping it
  could lose one. A refusal costs a re-run and decides nothing wrongly.
- [DETAIL] Fences (criterion 6): the parser keeps reading rows inside a
  fence, because models often fence their whole table and ignoring it
  would turn that answer into a quiet failed member — the R-2 hole. The
  check therefore skips a fence only when the parser reads no row from it,
  and only beside readable rows, so both readers agree on what a fenced
  table is.
- [DETAIL] Phase 2a refuses only beside readable rows (criterion 7). An
  answer without rows keeps its existing treatment there: it is appended
  and said to be table lines that are not six-cell rows
  (`test_table_lines_that_are_not_rows_are_never_reported_as_no_finding`).
  Phase 2a has no loop that could end clean on it.
