---
title: "Decisions — finder-partial-report"
category: decisions
status: draft
implementation_status: none
date: 2026-11-19
created: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-25
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
superseded_by: Q-2 (the retry in this answer is withdrawn; do not build it, ADR 0020 point 9 forbids it)
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

## Q-4 · How the spec review ends after round 3

asked: 2026-11-19
answer: "A: Selbst entscheiden" — in English: the orchestrator decides the round-3 rows S-14..S-19 as details with reasons, the spec and plan are redrafted, and no fourth review round runs; the phase-4b review loop and phase 6 check the result.
answered_by: maintainer
status: answered
context: |
  Topic: the end of the phase-2a spec review of this change.
  Intention: the maintainer's rule of 2026-11-18 sends a spec-changing ambiguity left after round 3 to the maintainer.
  Today: round 3 returned six rows (S-14..S-19), no BLOCKER; S-15 shows criteria 15 and 16 contradicting each other for a Claude call that exits 0 with an error result.
  Repository change: decisions.md, a redrafted spec.md and plan.md.
  Architecture change: none beyond the spec.
  Options shown: A decide as details, no fourth round (recommended); B the same plus a fourth round; C re-slice the Claude output reading into its own change.

In the context of a third spec-review round that still found ambiguities but
no BLOCKER, facing one more round that has so far always raised new rows, we
decided to settle the rows as reasoned details and move to implementation,
to achieve a finished spec without an open-ended review, accepting that the
last spec edit is first checked by the review loop and phase 6 — 2026-11-19

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

Spec-review round 2 rows, decided by the orchestrator with reasons (same
rule). Facts read on 2026-11-19: `claude_command` launches every Claude seat
with `--output-format text` (`scripts/stage2_research_run.py`); the installed
Claude Code 2.1.328 offers `--json-schema` and `--output-format json`;
`check_research_handoff.py` checks a fence only by its kind (`KINDS`, line 54);
the locked dependencies hold no JSON Schema validator.

[DETAIL] **S-9 (reading a schema-enforced Claude answer)**: a Claude finder
call runs with `--output-format json --json-schema <schema>`; the runner takes
the answer from the result's `structured_output` field and stores that object,
serialised, as the record's answer; the envelope (session id, cost) is not
published. A non-zero exit or an error result stays a failed call
(criterion 13); exit 0 without `structured_output` is an invalid report
(criterion 12). Only finder calls change; every other seat keeps
`--output-format text`. Reason: the schema is only enforced in the
structured field, and the outcome mapping keeps today's two stop paths.

[DETAIL] **S-10 (blank values)**: every required string (`path`,
`reference`, `reason`, `not_read`) must hold a non-whitespace character; a
blank one drops the entry. Reason: one rule for all fields, stated once in
the schema; a path of spaces can never resolve at merge.

[DETAIL] **S-11 (the partial fence of a filtered record)**: the fence for a
filtered `ok` record holds the seat (`slot_id`), the outcome and the
`filtered` list (category, original entry, errors), without the raw answer.
Records that are not `ok` keep today's fence. Reason: the retained entries
already appear in the map; republishing the raw answer would show every
dropped entry twice and retained ones outside the map.

[DETAIL] **S-12 (where the schema text goes)**: the runner appends the schema
to the one shared finder prompt, so all three seats keep one prompt and one
`prompt_sha256`; `prompts/research-swarm/finder.md` drops its prose
description of the entry format and points to the appended schema. Reason:
Q-3 says the format exists once; a Claude seat seeing the schema in both
prompt and flag is harmless, two prompt variants are not.

[DETAIL] **S-13 (where the schema lives and what reads it)**: the schema is a
JSON file beside the finder prompt
(`prompts/research-swarm/finder-locator.schema.json`); a small interpreter in
`scripts/stage2_research_map.py` reads the few keywords the file uses and
refuses any other keyword, so a schema edit cannot be silently ignored. No
new dependency. Reason: a JSON file is language-neutral (the long-term Rust
direction), and the keyword refusal makes criterion 3 testable.

Spec-review round 3 rows, decided by the orchestrator with reasons (Q-4).

[DETAIL] **S-15 (exit 0 with an error result)**: a Claude finder call whose
result reports that no schema-conforming answer was produced (exit 0, no
`structured_output`, whatever `is_error` or `subtype` says) is an invalid
report (criterion 15); only a non-zero exit, or a result that ends before
the model answered (`subtype` naming a turn, budget or API limit), is a
failed call (criterion 16). Reason: a format failure must not read as a
process failure, which is the incident this change repairs.

[DETAIL] **S-14 (stdout of a rejected Claude finder record)**: on success
the stored `stdout` is the serialized structured output; on every other path it holds only the envelope's
`result` text, or nothing; the session id and the cost are never stored or
published. Reason: the S-9 rule must hold on the failure paths too.

[DETAIL] **S-16 (the outer shape and the schema)**: finder validation reads
the whole answer shape (the four category names, non-empty lists, closed
properties) from the schema; the merged-map validation keeps `CATEGORIES`, and
a test holds the schema's category names equal to `CATEGORIES`. A violation
inside an item of a category array is an entry fault (dropped); every other
violation is an outer fault (stop). Reason: one source for the finder format,
and the test closes the divergence the row names.

[DETAIL] **S-17 (a bad schema)**: the schema is loaded and checked when the
finder prompt is built, before any call starts; a missing file, invalid JSON
or an unsupported keyword ends the run incomplete with a reason naming the
schema file, and no finder call runs. Reason: a harness fault must not be
blamed on the seats.

[DETAIL] **S-18 (annotations)**: `description`, `title` and `$schema` are
supported annotations that validation ignores; the reference rules of
`finder.md` ("exact symbol or section", "line numbers, bare paths and prose
are not references") move into the schema's `description` strings, so every
seat sees them in the schema. Reason: these rules guard the incident itself
and must reach Claude seats through the enforced schema.

[DETAIL] **S-19 (field form)**: the schema checks type, closed fields and a
non-whitespace character only; the form of `path` and `reference` stays
checked at merge as today (an unresolved locator). Reason: new form rules
are outside this repair.

[DETAIL] **Plan order (orchestrator note)**: the orchestrator creates the
schema file and the `finder.md` edit (held paths) before the implementation
attempt, not after, so the code reads the real file from the start.


[DETAIL] **Superseded research-swarm verification commitments**: this change
supersedes criterion 24 of the archived research-swarm plan (2026-11-06),
whose fifth-field fault stopped the whole report. An extra field now drops the
entry; `test_finder_filter_reports_each_invalid_entry` verifies that boundary.
It also supersedes finding F-47's commitment that malformed finder entries are
neither accepted nor reused: valid retained entries and the empty-category marker
are accepted and reusable, as `test_finder_filtered_record_is_reused_on_resume`
verifies. Invalid outer shapes still stop, as
`test_finder_invalid_outer_shape_stops` verifies. The former commitments were
exercised by `test_finder_trio_locates_four_categories_without_judging` and
`test_malformed_finder_reasons_block_progress_and_reuse`, respectively.
