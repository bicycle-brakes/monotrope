---
title: "Decisions — red-first-baseline"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, red-first, repair, bug]
---

# red-first-baseline — Decisions

## SKIP · interview

status: skipped
reason: The maintainer filed this as a bug with its expected behaviour stated (coding-harness-7aso, 2026-11-20): a test that is red on the baseline must not be reported as "pytest ended 0 on the baseline"; the task is to find how the red-first baseline is built and why a red test reads as exit 0, and to make the check report what pytest reports. A bug fix whose wanted outcome is the current contract leaves no open choice for an interview; skipped by the orchestrator in night run 2026-11-20-a under the maintainer's standing instruction to decide by recommendation overnight.

## Details decided by the orchestrator

[DETAIL] **D-1 (the exit-code contract)**: the red side is pytest exit exactly 1, as `red_first` and the successor spec `red-first-pytest-failed` state; the `docs/WORKFLOW.md` sentence "exits 1 or 2" is aligned to it in this change. Reason: the governing spec and the code agree; the doc is the outlier.

[DETAIL] **D-2 (first step is a reproduction)**: the spec's first criterion reproduces one of the two recorded refusals (finder-partial-report round 3, row L3-1, branch `fix/finder-partial-report`) as a failing test of `red_first` before any fix. Reason: research could not read the incident evidence; the mechanism must be measured, not guessed.

[DETAIL] **D-3 (the bf9m class stays out)**: a test whose code under test lives in the test file itself (coding-harness-bf9m) is a known limit of a tests-only baseline and is not changed here. Reason: the bead names it as a possibly different case.
