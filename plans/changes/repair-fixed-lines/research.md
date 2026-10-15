---
title: "Research — repair-fixed-lines"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-ugi
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair]
---

# The repair runner's fixed-line parser — Research

Phase 1 for bead coding-harness-ugi, seeded by the orchestrating session on
2026-10-15 against `origin/main` at `135f029`.

## The question

The `repair` verb of `scripts/stage2.py` sends every taken findings row to
Codex and reads the answer's fixed lines (`check_repair_answer`). Two faults
make a usable repair fail:

1. **Any `word:` line counts as a finding id.** The parser splits each
   non-empty answer line at its first colon and takes the left part as an id.
   A line such as `expected: …`, `found: …` or `Resume: …` then fails the
   attempt with `<word>: no taken row carries this id`. Seen on 2026-10-15 in
   the pi-pin repair, attempt 2 (`plans/changes/pi-pin/findings.md` on
   `main`, the attempt-2 diagnostics: `expected`, `found`, `relevant`,
   `proposal` and `Resume` each "no taken row carries this id").
2. **A row repaired by hand is demanded again.** `repair_targets` takes every
   row whose Status begins `taken`. A row the orchestrating session repaired
   by hand keeps a Status that begins `taken — …; fixed by …` (the precedent
   in `plans/changes/haiku-5-5/findings.md` and the pi-pin phase-6 table),
   so the next repair call asks for it again and fails with
   `<ID>: no fixed line` (haiku-5-5, 2026-10-15, row L1-1).

Needed (bead text): rows already repaired are not demanded again, and only
lines whose id is a taken row's id count as fixed lines.

## Known so far (read, not run)

- `REPAIR_ANSWER` (around line 221) asks for "one fixed line per row and no
  other text"; the parser enforces "no other text" by failing on any line
  without a colon, and by failing on any colon line whose left part is no
  taken id.
- `check_repair_answer` (around line 2202) collects `parsed[ident]` for every
  colon line; ids left over after the taken rows are matched become problems.
- `fixed_status` (around line 2179) accepts `fixed — tests/<path>::<function>`
  and `fixed — not a test — <reason>`.
- `repair_targets` (around line 1034) reads Status by prefix only: `taken`,
  `rejected`, `fixed`, blank or `open`.
- Loop row ids follow `L<n>-<m>` (`LOOP_ID`); phase-6 table ids are free
  text such as `F-1`.

## To explore

How the answer parser can tell a fixed line from prose without accepting a
malformed answer as clean (which words or shapes count as an id; whether
prose lines are ignored, named once, or still fail); how a hand-repaired row
should be recorded so `repair_targets` skips it (a Status that begins
`fixed`, or a recognised `taken — …; fixed by …` form), and what the existing
records on `main` already hold; which tests in `tests/test_stage2.py` pin the
current parser and target selection; and what `docs/WORKFLOW.md` and the
repair prompt say about the answer format.
