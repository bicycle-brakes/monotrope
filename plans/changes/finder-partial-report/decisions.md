---
title: "Decisions — finder-partial-report"
category: decisions
status: draft
implementation_status: none
date: 2026-11-19
created: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm]
---

# finder-partial-report — Decisions

Class: bounded (bead coding-harness-yd8w; one answered question is owed —
Q-1 below, answered by the maintainer on 2026-11-19 in the conversation and
recorded in the bead's notes).

## Q-1 · What happens to a finder answer with malformed entries

asked: 2026-11-19
answer: "A: Retry + Rest behalten (Empf.)" — in English: the finder seat is asked once more with the exact validation error; if its second answer still fails, the runner keeps the valid locator entries, records the dropped ones as a gap in the run record, and the run continues; the requirement that every locator names a path and an exact symbol or section stays.
answered_by: maintainer
status: answered
context: |
  Topic: bead coding-harness-yd8w, the finder step of the research swarm.
  Intention: the trust-pyramid-swarm run could not run; finder seat 3 failed twice in two changes.
  Today: run 2277a0ed's finder answer from claude-haiku-5-5 was valid JSON with the four lists and 102 entries; 36 named a whole file without a reference. scripts/stage2_research_map.py validate_locator_report raises on the first such entry, scripts/stage2_research_run.py stage_finders voids the whole answer, and require_ok stops the run before any topic.
  Repository change: scripts/stage2_research_map.py, scripts/stage2_research_run.py and their tests.
  Architecture change: the finder step recovers before it refuses (the maintainer's rule of 2026-11-15: rules must reduce aborts).
  Options shown: A retry once, then keep the valid entries (recommended); B admit whole-file locators with a marker; C make seat 3 selectable on the command line; D rerun unchanged with Haiku.

In the context of a finder step that voids a whole answer for one malformed
entry, facing two aborted research runs, we decided to ask the seat once more
with the exact error and then keep the valid entries and record the rest as a
gap, to achieve a run that a form error no longer stops, accepting a map built
from fewer locators when a seat answers badly twice — 2026-11-19

## Q-2 · No finder retry; filter the first answer

asked: 2026-11-19
answer: "B, wie erhalten wir aber zwingend das richtige Antwort Format? Ich möchte nicht ständig Format Fehler haben?" — in English: option B; no correction request is sent to a finder seat; the runner keeps the valid locator entries of the first answer and records the dropped ones as a gap. Q-1's retry is withdrawn. The maintainer's follow-up question on the answer format is Q-3.
answered_by: maintainer
status: answered
context: |
  Topic: spec-review BLOCKER S-3 of finder-partial-report.
  Intention: Q-1's retry conflicts with an accepted ADR, which the orchestrator cannot resolve alone.
  Today: ADR 0020 point 9 allows exactly one correction, for a topic report ("No other retry is allowed"), and caps a run at 72 + 6N calls, published as invocation_ceiling.
  Repository change: A an ADR 0020 amendment as a decision PR; B none.
  Architecture change: A a second allowed correction and a ceiling three calls higher; B the finder step filters instead of asking again.
  Options shown: B without retry (recommended); A ADR amendment plus retry; C re-slice together with bead coding-harness-glqo.

In the context of a finder retry that ADR 0020 forbids, facing a BLOCKER in
the spec review, we decided to filter the first answer instead of asking
again, to achieve the same protection against aborted runs without an ADR
change or extra calls, accepting that entries a seat got wrong are lost to
the map — 2026-11-19

## Q-3 · How the locator format is enforced

asked: 2026-11-19
answer: "C: Schema überall" — in English: the locator format exists once as a JSON Schema; this change passes it to Claude Code finder seats as an enforced schema (`--json-schema`), states the same schema in the prompt for Pi seats, and keeps Q-2's filter as the net; teaching Pi and OpenCode Go structured output for every fixed-shape call is its own bead (coding-harness-fagu).
answered_by: maintainer
status: answered
context: |
  Topic: the answer format of finder seats, asked by the maintainer with Q-2.
  Intention: filtering catches format errors but does not prevent them; the maintainer does not want recurring format errors.
  Today: the format is described in the prompt and validated afterwards; Claude Code can enforce a JSON Schema with --json-schema, which the runner does not use; the pinned Pi has no such option.
  Repository change: scripts/stage2_research_run.py and scripts/stage2_research_map.py pass and read one locator schema; spec criteria for it; a separate bead for Pi.
  Architecture change: one source for the locator format, read by validation, prompt and the Claude call (house rule 9).
  Options shown: A schema plus filter (recommended); B filter now, schema later; C schema everywhere — A here plus a bead for Pi.

In the context of finder answers whose format is only requested, facing
recurring format errors, we decided to enforce one locator schema where the
harness allows it and to teach the Go path the same in its own bead, to
achieve format errors that cannot arise on Claude seats and cost only single
entries elsewhere, accepting a second change to the Pi path — 2026-11-19

## Decided by the agent

Spec-review round 1 rows that Q-2 and Q-3 leave open, decided by the
orchestrator with reasons (maintainer rule of 2026-11-18: details are decided
with reasons, real decisions go to the maintainer).

[DETAIL] **S-1, S-4 (the correction request, its error text and time
allowance)** are void: Q-2 sends no correction. The published gap names each
dropped entry with the exact error the validator gives for that entry; the
validator gains an entry-level form that returns every fault instead of
raising on the first. Reason: a gap that names only the first fault hides
the rest.

[DETAIL] **S-2, S-6 (which faults drop one entry and which stop the run)**:
faults of a single entry (a missing or empty field, an extra field, a
non-object entry) drop that entry; faults of the outer shape (not JSON, not
exactly the four categories, a category that is not a list) keep today's
invalid-report outcome and stop the run as today. A category the model sent
as an empty list is an outer-shape fault, as today. Reason: an entry fault
leaves the rest of the answer readable; an outer fault leaves nothing to
keep (Q-1's "otherwise readable" reading).

[DETAIL] **S-5 (where dropped entries are recorded)**: in the run record's
published `partial` fence for that seat and in the manifest, not in the map's
`gaps` or `not_read`. Reason: topic seats and the judge see the map; a
dropped locator was never evidence, and feeding it to them as a gap would
invite them to research a path the finder could not locate exactly.

[DETAIL] **S-7 (the marker for a category emptied by filtering)**: the
runner inserts `{"not_read": "every entry of this category was dropped by
locator validation (finder-partial-report)"}`, the same text for every seat,
so the merge can reproduce it exactly. Reason: the exact-union check needs a
fixed string.

[DETAIL] **S-8 (the outcome of a filtered answer and resume)**: a filtered
answer is stored and published with the outcome `ok`, its dropped entries in
a `filtered` list beside it; the store reuses it on resume like any `ok`
record, and the filtering is deterministic, so a resumed run publishes the
same gap. Reason: `require_ok` and the reuse rule stay unchanged.
