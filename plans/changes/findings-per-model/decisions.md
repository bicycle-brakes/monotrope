---
title: "Decisions — findings-per-model"
category: decisions
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
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
