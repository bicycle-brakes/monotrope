---
title: "Decisions — findings-per-model"
category: decisions
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-qut1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, review-loop, measurement]
---

# findings-per-model — Decisions

Class: bounded (bead coding-harness-qut1).

## Q-1 · What counts as accepted, per model

The column choice in this answer was superseded by Q-5 (provisional agent detail, autonomous run 2026-11-19).

asked: 2026-11-17
answer: "C" — report taken and fixed as two separate columns per model id. Taken = taken, 'taken — not a test', fixed; fixed = actually repaired. A duplicate ('same as ...') counts for the model that raised it first. Also raised and rejected counts. Output JSONL plus a plain table with the cut-off commit, runnable through make; the morning handover shows the table.
answered_by: maintainer
status: answered
context: |
  Topic: the maintainer asked to measure, for every model of the review loop and of phase 6, how many of the findings it raised are accepted (bead coding-harness-qut1; maintainer 2026-11-16, verbatim: "normaler leiter und messe die anzahl der gemessene befunde die akzeptiert werden für alle modelle").
  Intention: the count feeds the contributor-model trial (bead coding-harness-wmy1) and the order of the paid review ladder; "accepted" had more than one plausible reading, so it was asked in the night preparation of 2026-11-17 before the spec.
  Today: every released loop row carries the model that raised it in its Reviewer cell, and scripts/stage2_runs.py counts taken, rejected and undecided rows per run, but nothing aggregates them per model; the evaluation is done by a person reading the rows.
  Repository change: one script with one output — JSONL plus a plain table with the cut-off commit — reading the loop records and findings.md of every change, run through make, its table shown in the morning handover.
  Architecture change: none; the row grammar and the release of loop rows stay as they are, the new script only reads them.
  (Recorded by the lane session from the bead's notes, which hold the answer; the wording of the question as originally shown was not read.)

In the context of measuring how many review findings each model raises that the orchestrator accepts, facing more than one reading of "accepted" and duplicates raised by several models, we decided to count per model id the raised, taken (taken, 'taken — not a test', fixed), fixed (actually repaired) and rejected findings, taken and fixed as two separate columns, a duplicate counted for the model that raised it first, output as JSONL plus a plain table with the cut-off commit through make and shown in the morning handover, to achieve a count that can order the review ladder and judge the contributor-model trial, accepting that a model which raises a finding another model already raised earns no count for it. — 2026-11-17

Appetite: 6 hours of phase 4, repair rounds included (maintainer, 2026-11-17, recorded in the notes of bead coding-harness-qut1). The first draft's 4 hours did not come from the maintainer; the revision states 6 hours.

## Q-2 · Which model a phase-6 finding counts for (finding F-1)

asked: 2026-11-18
answer: "A" — the maintainer asked for "eine zentrale und flexible Lösung, die sich auf die Prinzipien der Modularität stützt" ("a central and flexible solution based on the principles of modularity"). Chosen: one shared reader module for findings rows, its status vocabulary taken from one definition (templates/findings.md), with an 'attribution source' interface. The first implementation is the legacy source: a phase-6 block counts for the model of the nearest review call line directly above it with no other block in between, otherwise 'unattributed'. A later event source from bead coding-harness-oebl replaces it without changing the readers. The report, the metrics (bead coding-harness-nqaf) and the morning table are thin consumers of that module.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a finding F-1 of the Opus 5.5 spec review (2026-11-17), marked [AMBIGUITY]: which model a phase-6 finding counts for.
  Intention: the phase-2a gate lets no ambiguity through; the answer decides whether phase 6 gets per-model totals at all.
  Today: loop rows name the exact model in their Reviewer cell; phase-6 rows say only 'Codex'. The model id stands on a separate review call line, and it changed from gpt-6.1-sol to gpt-6.1-terra; call lines and phase-6 blocks do not pair one to one.
  Options as offered: A — build the attribution-source interface now; B — build the event log of bead coding-harness-oebl first; C — a single attribution rule only. The 2026-11-17 recommendation was: a phase-6 block counts for the model of the review call line just above it, otherwise 'unattributed'.
  Repository change: one shared reader module for findings rows, used by the report, the metrics and the morning table; the status vocabulary is read from one definition.
  Architecture change: an 'attribution source' interface with a legacy implementation now and an event-log implementation later, behind one reader.
  (Recorded by the lane session from the bead's notes, which hold the answer and the option labels; the full wording shown with the question was not read.)

In the context of counting phase-6 findings per model when phase-6 rows name only 'Codex' and the model id stands on a separate review call line, facing a pairing of call lines and blocks that is not one to one and a planned event log (bead coding-harness-oebl) that will record the model directly, we decided one shared reader module for findings rows with an 'attribution source' interface whose first implementation attributes a phase-6 block to the nearest review call line directly above it with no other block in between, otherwise 'unattributed', to achieve a central and modular solution in which a later event source replaces the legacy rule without changing the report, the metrics or the morning table, accepting a new module boundary in this change and 'unattributed' phase-6 findings wherever the legacy rule cannot pair a block. — 2026-11-18

## Q-3 · What marks a finding as a duplicate (finding F-2)

asked: 2026-11-18
answer: "C" — future duplicates carry one fixed form from templates/findings.md ('duplicate of <ID>'), checked by a gate. Legacy rows: a Status naming another row id with 'same as', 'duplicate of', 'repeat(s)' or 'repeat of' is a duplicate; without a row id the row counts as an ordinary rejected row.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a finding F-2, marked [AMBIGUITY]: what "marked as a duplicate" looks like.
  Intention: the phase-2a gate lets no ambiguity through; without one reading, two models can get credit for one finding.
  Today: duplicates are written in many forms ('same as L1-3', 'duplicate of L1-1', 'repeats L2-2', 'repeat of L1-6 and L3-3', 'Same as Finding 3' without a row id); no form is fixed.
  Options as offered: the 2026-11-17 recommendation was: a Status naming another row id with 'same as'/'duplicate of'/'repeat(s)' is a duplicate, a marker without an id counts as an ordinary rejected row. The maintainer chose C; the wording of the other options shown on 2026-11-18 was not read.
  Repository change: templates/findings.md states one fixed duplicate form ('duplicate of <ID>'), a gate checks it for new rows, and the reader recognises the legacy forms listed in the answer.
  Architecture change: none beyond the shared reader of Q-2; the duplicate rule lives in that reader.
  (Recorded by the lane session from the bead's notes, which hold the answer; the full wording shown with the question was not read.)

In the context of crediting a finding once when several models raise it, facing duplicate markers written in many free-text forms, some without a row id, we decided one fixed form 'duplicate of <ID>' from templates/findings.md for future rows, checked by a gate, and for legacy rows a Status naming another row id with 'same as', 'duplicate of', 'repeat(s)' or 'repeat of', a row without a row id counting as an ordinary rejected row, to achieve a duplicate rule a test can check and that new rows cannot drift from, accepting a new gate and that legacy markers without a row id are not treated as duplicates. — 2026-11-18

## Q-4 · Which row gets the credit for a duplicate (finding F-3)

asked: 2026-11-18
answer: "A" — credit goes to the row or rows the marker points to; with two originals both get credit and the duplicate none; no invented chronology.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a finding F-3, marked [AMBIGUITY]: what "first raised" means for a duplicate.
  Intention: the phase-2a gate lets no ambiguity through; within one swarm round members answer in parallel, so the row order says nothing about who raised a finding first.
  Today: markers point backwards and forwards, sometimes to two rows at once ('same as L3-2 and L4-4').
  Options as offered: the 2026-11-17 recommendation was: credit goes to the row the marker points to, the lowest-numbered one if two. The maintainer chose A; the wording of the other options shown on 2026-11-18 was not read.
  Repository change: the reader credits the row or rows a duplicate marker names.
  Architecture change: none.
  (Recorded by the lane session from the bead's notes, which hold the answer; the full wording shown with the question was not read.)

In the context of crediting a duplicate finding to the model that raised it, facing parallel swarm members whose row order is only assembly order and markers that name two originals, we decided that credit goes to the row or rows the marker points to, both originals getting credit when two are named and the duplicate none, to achieve a rule read from the record itself without an invented chronology, accepting that a marker naming two originals credits two models for one finding. — 2026-11-18

## Q-5 · Which statuses count as which outcome (finding F-5)

asked: 2026-11-18
answer: "D" (chosen after a context explanation, changed from A) — three outcome columns per model besides raised: defects accepted (leading word taken or fixed), questions settled (resolved, answered, in spec), rejected; open is not counted; an unknown status makes the report incomplete; weighting belongs to the ladder rule, not to the counter.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a finding F-5, marked [AMBIGUITY]: which statuses count as accepted when the vocabulary in use is wider than the four the spec lists.
  Intention: the phase-2a gate lets no ambiguity through; the answer decides what the morning table counts.
  Today: statuses in use include 'taken — guard test — …', 'fixed — not a test — …', 'fixed in <commit>', 'fixed — orchestrator hand edit …', 'resolved <date> by <source>', 'answered', 'in spec' and 'open' (templates/findings.md); 'resolved' has no bucket in the spec.
  Options as offered: the 2026-11-17 recommendation was: match the status by its leading word, and count 'resolved', 'answered' and 'in spec' only as raised. The maintainer first answered A, then chose D after a context explanation; the wording of the options shown on 2026-11-18 was not read.
  Repository change: the report shows per model raised, defects accepted, questions settled and rejected, read through the status vocabulary of templates/findings.md.
  Architecture change: none beyond the shared reader of Q-2.
  (Recorded by the lane session from the bead's notes, which hold the answer; the full wording shown with the question was not read.)

In the context of counting the outcome of each finding per model, facing a status vocabulary wider than the spec's list and statuses that settle a question rather than accept a defect, we decided three outcome columns per model besides raised — defects accepted (leading word taken or fixed), questions settled (resolved, answered, in spec) and rejected — with open not counted and an unknown status making the report incomplete, to achieve counts that keep defects and settled questions apart and leave their weighting to the ladder rule, accepting that the counter itself does not rank models. — 2026-11-18

## Q-6 · What the report does when a row cannot be read (finding F-8)

asked: 2026-11-18
answer: "B" — always print the table and the JSON; gaps are flagged 'incomplete' with the affected rows, and the exit code is non-zero; every unreadable row (cell count, unknown status, encoding) is a gap, never silently 'unattributed'.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a finding F-8, marked [AMBIGUITY]: what "refuses to present an incomplete count as complete" means.
  Intention: the phase-2a gate lets no ambiguity through; historical findings cannot be edited, so one unreadable historical row could otherwise stop the report at every commit.
  Today: some historical rows cannot be resolved (for example a duplicate marker without a row id); the spec names neither an exit code nor a marker for an incomplete report.
  Options as offered: the 2026-11-17 recommendation was: always print both formats, gaps as an 'incomplete' flag plus the affected inputs, non-zero exit. The maintainer chose B; the wording of the other options shown on 2026-11-18 was not read.
  Repository change: the report prints both formats every time, marks them 'incomplete' with the affected rows when a gap exists, and exits non-zero.
  Architecture change: none.
  (Recorded by the lane session from the bead's notes, which hold the answer; the full wording shown with the question was not read.)

In the context of a per-model report over historical findings that cannot be edited, facing rows that cannot be read or resolved, we decided to always print the table and the JSON, flag gaps as 'incomplete' with the affected rows and exit non-zero, every unreadable row (cell count, unknown status, encoding) being a gap and never silently 'unattributed', to achieve a report that is always visible yet never passes an incomplete count as complete, accepting a non-zero exit as long as any historical gap remains. — 2026-11-18

## Q-7 · Who enforces the cell vocabulary: the reader or a gate (phase-6 grammar review)

asked: 2026-11-20
answer: "Leser misst, Gate setzt durch" — the reader measures: severity, dimension and origin need only a non-blank cell, while ID, reviewer and Status stay strict because the count depends on them; historical rows with a free vocabulary are counted again. The gate enforces: the fixed vocabulary (origin `base`, `loop` or `fix-r<N>`, the severity set, the dimension set) applies only to new or changed rows, through the existing new-row gate `scripts/check_finding_duplicates.py`, without a new entry in `decisions/gates.yaml`.
answered_by: maintainer
status: answered
context: |
  Topic: the hand repair of phase-6 rows F6-1 and F6-2, a review of the reader's whole input grammar, found that its cell check rejects real history.
  Intention: the per-model report must be usable on main; history is protected and cannot be rewritten.
  Today: at commit faa75a3d the main report had 1555 gaps; 1414 were historical rows whose origin is free text (`impl`, `Phase 6`, a model name), 47 a free dimension, 9 a free severity. Those rows were left out of every model's count.
  Options as offered: the recommendation was to require only non-blank severity, dimension and origin in the reader and to enforce the vocabulary for new rows; the wording of the options shown on 2026-11-20 was not read.
  Repository change: the reader counts rows with a free vocabulary; a later step makes the new-row gate check the vocabulary of new or changed rows.
  Architecture change: none; the one reader and the one new-row gate stay the only paths.
  (Recorded by the lane session from the orchestrator's relay of the maintainer's answer. The reader half is built; the gate half waits on a follow-up question, because three released loop rows the runner wrote on this branch carry the dimension `Correctness`, and the gate would block runner output that may not be edited by hand.)

In the context of a per-model report over protected historical findings, facing rows whose severity, dimension or origin is free text although those cells decide no count, we decided that the reader asks only that they are not blank while ID, reviewer and Status stay strict, and that the fixed vocabulary is enforced on new or changed rows by the existing new-row gate, to achieve a report that counts the real history and a vocabulary that holds from now on, accepting that historical rows keep their free vocabulary for good. — 2026-11-20

## Q-8 · Released loop sections with a second table after a blank line (phase-6 re-check RF6-2)

asked: 2026-11-20
answer: "Option 1" — repair RF6-1 (digitless free-swarm model IDs such as `space-bunny-free`) in `MODEL_NAME` and record RF6-2 as an accepted `Boundary` in `spec.md`: a released loop section counts only its first table because `release-loop` writes one table per release heading.
answered_by: maintainer
status: answered
context: |
  Topic: handling phase-6 re-check findings RF6-1 and RF6-2 in the fourth phase-6 round of findings-per-model (bead coding-harness-qut1).
  Intention: under the repeated-mechanism stop rule, the orchestrator asks before another grammar repair round.
  Today: all four phase-6 rounds found input-grammar edge cases in scripts/findings_reader.py. RF6-1 is a real bug for digitless free-swarm model IDs (one-line fix); RF6-2 concerns a second table separated by a blank line under one released-loop heading, which release-loop never writes.
  Repository change: broaden MODEL_NAME to accept hyphenated lowercase model IDs without digits, add a regression test, and state the single-table released-section limit under Boundary in spec.md, followed by one final phase-6 re-check.
  Architecture change: none; the shared reader interface and spec structure remain unchanged.

In the context of the fourth phase-6 review round of findings-per-model, facing a genuine attribution bug for digitless free-swarm model IDs (RF6-1) alongside a second-table edge case under one released-loop heading that release-loop never produces (RF6-2), we decided to fix RF6-1 in `MODEL_NAME` and state in `spec.md` Boundary that a released loop section counts only its first table, to achieve accurate attribution for all live free-swarm models while avoiding miscounting unrelated tables after a release block, accepting that a hand-split second table under one release heading stands outside the count. — 2026-11-20

## Agent decisions on the second phase-2a rows F-12..F-19 — 2026-11-18

Second spec-review round (maintainer rule of 2026-11-18: triage each round,
at most three rounds). Decisions by the orchestrating session (Opus 5.5),
shown to the maintainer as one list and accepted as proposed ("A: So
übernehmen"). F-14 refines the maintainer's answer on F-3 and is marked so;
the rest are `[DETAIL]` decisions derived from the answers on F-1, F-2, F-8.

- **F-14, duplicate chains (refines the F-3 answer).** A chain of duplicate
  markers is followed to its root; credit goes only to the root row(s), rows
  that are not themselves duplicates. A duplicate never earns credit, even
  when other rows name it. Rows that name each other in a cycle are a gap
  (`incomplete`). Reason: otherwise criterion 8 contradicts itself on real
  chains in the records (archive/2026-11-06-workflow-promises), and the root
  is the model that actually raised the finding first.
- **F-12, what a review call is.** Only a call line of the verb `review`
  (phase 6) attributes a phase-6 block; any other verb directly above leaves
  the block `unattributed`. Reason: no guessing (F-1).
- **F-13, older phase-6 shapes.** Only headings of the runner form
  `## Phase 6 — <who>, <date>` open a phase-6 section; other phase-6-like
  headings give `unattributed` rows; tables with no heading are reported on
  the line "outside the count". Rows with `2a-` ids are phase-2a rows and are
  not counted. Reason: as for L1's legacy runs and F-8 — gaps shown, not
  guessed.
- **F-15, letter case.** Existing rows match the markers without regard to
  case; new rows must use exactly the canonical form. Reason: nine real
  duplicates in the records are capitalised.
- **F-16, the duplicate gate.** Rows are new or changed relative to the merge
  base with `origin/main`; the canonical Status is `rejected — duplicate of
  <ID>`, the form `triage` writes. Reason: the runner can produce only that
  form, and the merge base makes the gate the same locally and in CI.
- **F-17, the attribution-source interface.** A source is given the change,
  the findings file and the block identity (its heading line, its position
  and the call lines directly above it) and returns a model id or
  `unattributed`. The criterion's test plugs in a second source that
  attributes by heading alone. Reason: the criterion can then go red.
- **F-18, which commits the morning handover reports.** One report per
  unmerged change branch that gained rows that night, plus `main` at the time
  the handover is written. Reason: no lane's earlier item drops out.
- **F-19, where the formats go.** The table to stdout; the JSON Lines to a
  file under the state directory, whose path the run prints last. Reason:
  metrics and the handover read from one fixed place.

## Agent decisions on the third phase-2a rows F-20..F-28 — 2026-11-18

Third and last spec-review round (maintainer rule of 2026-11-18: triage each
round, at most three rounds). `[DETAIL]` decisions by the orchestrating
session (Opus 5.5), shown to the maintainer as one list and accepted as
proposed ("A: So übernehmen"). No fourth review runs; the final draft works
these in.

- **F-20, which headings count.** Only the heading the runner writes,
  `## Phase 6 — <who>, <date>`, and the released loop headings of F-21.
  Restated tables under any other heading do not count and never supply a
  row's current state. Reason: an empty restatement must not overwrite a
  decided row.
- **F-21, released loop rows written before the template form.** The
  heading `## Phase 4b — GLM loop rows, released <date>` is a second fixed
  form, recognised by the same helper as the runner's `RELEASE_HEADING`. The
  model comes from the Stage-2 call line, never from a Reviewer cell that
  names only a vendor.
- **F-22, rows in a moved file.** The merge-base comparison is rename-aware
  (`git diff -M`): rows that move unchanged with `make archive` are neither
  added nor changed.
- **F-23, the attributing call.** The nearest preceding Stage-2 call line of
  any verb must itself be `review`; otherwise the block is unattributed, as
  F-12 says.
- **F-24, model and state of a restated ID.** The earliest eligible row of an
  ID supplies the model that raised it; the latest eligible row supplies only
  its Status. Reason: Q-1 credits "the model that raised it".
- **F-25, finding tables outside the count.** Every table whose first cell
  holds a finding ID and that stands under a heading that is not counted is
  listed, with its heading, on the line "outside the count"; phase-2a blocks
  are listed there as one group of their own.
- **F-26, a duplicate of several rows.** `rejected — duplicate of <ID>` admits
  several IDs joined by " and ", optionally followed by a colon and a reason.
  Every named original keeps its credit; the duplicate gets none (F-14).
- **F-27, the known statuses.** A closed list in the spec: `open`, the
  leading words of criteria 11–13, and the historical forms `closed — …`
  (counted as fixed) and `accepted limit — …` (raised, not fixed). Any other
  status is a gap. Reason: history is protected, so an open set would leave
  every report with gaps for good.
- **F-28, the JSON Lines file.** The fixed place metrics read is the file for
  `main` in the state directory; a report for an unmerged branch writes a file
  of its own per branch, overwritten on each run.
