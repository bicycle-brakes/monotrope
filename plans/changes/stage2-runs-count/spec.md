---
title: "Spec — stage2-runs-count"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-09
supersedes: null
superseded_by: null
bead: coding-harness-kw0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, measurement]
class: bounded
appetite: 2
---

# Spec — stage2-runs-count

The counts of the first stage-2 runs come from a script in the repository,
not from a throwaway one, and anyone can repeat them at the commit they name.
Inputs: [`research.md`](research.md).

## Problem

The three-run note (`docs/research/2026-10-08-stage2-three-runs.md`) was
counted by a script that is not in the repository, so its numbers cannot be
repeated or checked, and bead coding-harness-kw0 asks for metrics generated
rather than typed. `docs/WORKFLOW.md` §4 states D-13's criteria in prose and
none of them as a number.

## Acceptance criteria

`scripts/stage2_runs.py <change> [<change> …] [--rev <commit>]` prints a
Markdown table, one row per named change, then a few summary lines.

1. When a change is named, its `findings.md` is read from
   `plans/changes/<change>/`, or else from the one archived folder
   `plans/changes/archive/YYYY-MM-DD-<change>/`; the row's first cell names
   the folder read beside the change (loop row L1-1).
   *Refuted by:* an archived change reported as not found, or a folder
   `…-other-<change>` taken for it.
2. If a named change has no `findings.md` (or two archived folders match),
   the script prints why on standard error and exits 2, with no table.
   *Refuted by:* exit 0 with an empty row.
3. Loop rows are the rows of `RELEASED_COLUMNS` width whose ID matches
   `LOOP_ID`; the row shows taken / rejected by the start of `Status`, and
   any loop row that is neither is shown as undecided, not dropped.
   *Refuted by:* a `rejected` row counted as taken, or an undecided row
   missing from every count.
4. "Rows marked Broke a test: yes" counts every row of every table in the
   file, whatever its status (the workflow asks for the mark on a taken row only) —
   phase 2a, phase 6, loop or any other table whose header has the column —
   whose `Broke a test` cell is `yes` (phase 6, F-1). A header is the line
   above a table's separator; a heading or any other line ends the table
   (F-5, F-6).
   *Refuted by:* a row marked `yes` in any such table not counted.
5. Phase-6 rounds are the number of `Phase 6 verdict:` lines
   (`VERDICT_LINE`); phase-2a and phase-6 rows are counted by severity from
   the rows under the headings `## Phase 2a` and `## Phase 6`, separately.
   *Refuted by:* a file with two verdict lines reported as one round, or a
   2a row counted as phase 6.
6. Loop rows whose `Phase 6` cell starts `disagree` are counted, as
   "<n> of <loop rows>".
   *Refuted by:* an `agree` mark counted.
7. Every line that starts `Stage-2 call, ` or `Stage-2 session, ` in the
   change's `findings.md` and `research.md` is a call; a call is clean when
   its line says `leak check clean over`. The row shows clean / total.
   A line with the prefix whose rest is not the runner's form still counts,
   as verb `unparsed` (phase 6, F-2).
   *Refuted by:* an explore line in `research.md` not counted, a prefixed
   line dropped, or a line without `leak check clean over` counted clean.
8. With `--rev <commit>`, resolved once to one commit (phase 6, F-3), every file (`findings.md`, `research.md`,
   `model-endpoints.yaml`) is read from that commit through git, and the
   "Measured at" cell names its short sha; without it the working tree is
   read and the cell says `tree at <short HEAD>`.
   *Refuted by:* `--rev` reporting a row that exists only in the working
   tree.
9. Under the table, generated lines give D-13's criteria as numbers where
   one exists: criterion 1 — runs measured and rows marked as having broken a
   test; criterion 3 — clean calls of recorded calls, with the note that a
   refused leak check writes no line; criterion 4 — foreign routes
   (`CODEX`, `GLM`, `GLM_FLASH`) that `declaration_problem` clears, of
   three. Criterion 2 is named as not measured here. Tokens and cost per
   vendor are printed as "not recorded by the runner", never as a number.
   A declaration of a shape the check cannot read clears no route and is
   reported, not raised (phase 6, F-4).
   *Refuted by:* a fixture endpoint without residency still counted as
   cleared, a traceback on a malformed declaration, or any token or cost
   figure in the output.
10. The note `docs/research/2026-10-08-stage2-three-runs.md` gains a dated
    addendum carrying the script's output unchanged and the command that
    made it; nothing above the addendum changes. `docs/WORKFLOW.md` §4 names
    the command and carries the criteria as numbers with their cut-off.
    *Refuted by:* a changed line above the addendum in `git diff`.

## Non-goals

- Recording tokens, cost or wall time in the runner (the gap is named, not
  closed).
- Changing any format `scripts/stage2.py` writes, or what a `Phase 6` mark
  means.
- Applying or evaluating the stop rule; a person reads the numbers
  (`docs/WORKFLOW.md` §4).
- Closing bead coding-harness-kw0: tokens and cost stay open.

## Decided here

- [DETAIL] Class `bounded`: a reader of files `scripts/stage2.py` already
  writes, reusing its constants; nothing new is decided about the flow.
  No spec review (optional for `bounded`, §4), no design (never for
  `bounded`).
- [DETAIL] Criterion 2 is printed as "not measured here": by ADR 0007 it
  governs lakeswitch-ai's content, which this repository never sends, and
  its state lives in that repository. The bead's third acceptance line is
  therefore met for three of the four criteria; the pull request says so.
- [DETAIL] `runner-derived-files` (#102) is measured beside the first three
  in the addendum, labelled as the fourth run: it is the first archived
  run, which exercises criterion 1's archive path on real data.
