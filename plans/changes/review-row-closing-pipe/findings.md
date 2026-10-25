---
title: "Findings — review-row-closing-pipe"
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
tags: [findings, stage-2]
---

# Findings — review-row-closing-pipe

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25 (conversation):
GLM, Codex and OpenCode Go are unreachable there, so `stage2.py implement`
could not run. Red first: five of the ten new test cases failed before the
production edit; the five counter-cases of criterion 2 passed before and
after, as guards.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review; the
review loop and the phase-6 Codex review are still owed.

- `UnreadableAnswer` keeps the message prefix "malformed finding output:
  expected six-cell findings or exactly 'No finding.'", so every existing
  test and record reader that matches it still does.
- `open_row` lives beside `split_row` but only `parse_rows` calls it: the
  runner's own tables (loop record, `findings.md`, released blocks) keep
  the strict two-pipe rule.
- The rejected-answer heading starts neither `## Round` nor `## Phase 6`
  and every kept line is quoted, so `rounds_run`, `read_state` and the
  released-row readers do not read it (criterion 6's test asserts
  `record_rows` finds nothing and no state line appears).
- A paid member that fails unreadably and is replaced: its answer is
  quoted in the written round as well, because the round lists the
  replaced member among its members.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request a read-only Opus 5.5 subagent reviewed the change
before the phase-6 Codex review, which is unreachable from this container.
Phase 6 is still owed. Repairs were made by a Sonnet 5.5 subagent at the
orchestrator's direction.

- P236-1 (MAJOR): the failure named the first non-blank line of the raw answer, which could be a header or separator the parser had skipped, against Q-1 (2) ("first unrecognised line"). Now named from the text `parse_rows` leaves over; spec criterion 4 reworded to match. Fixed; test `test_the_unreadable_failure_names_the_first_unrecognised_line_not_the_furniture`.
- P236-2 (test gap, MAJOR-adjacent): keeping the answers before the all-members-failed `CallFailed` was untested. Fixed; test `test_unreadable_answer_names_its_first_line` now asserts a rejected-answer heading per member.
- P236-3 (test gap): the 200-character cut of the named line was untested. Fixed; same test asserts at most 201 characters.
- P236-4 (test gap): keeping the answers before the refusal after a paid replacement was untested. Fixed; test `test_a_refused_replacement_keeps_both_unreadable_answers`.
- P236-5 (weak test): the quoting test could not fail for the reason it names. Fixed; `test_unreadable_answer_is_quoted_in_the_round` now plants a table-like line and asserts it quoted. Note: an unreadable answer cannot contain a closed table line (it would be a row, or a malformed table that refuses the round), so the planted line is an open five-cell line `| L1-9 | MAJOR | SPEC | c | spec.md:1`.
- P236-6 (MINOR): an open header and separator stayed as reviewer text and produced a not-a-row block. Fixed; tests `test_parse_rows_drops_open_furniture` and `test_an_all_open_table_round_carries_no_not_rows_block`.
- P236-7 (MINOR): the malformed-table refusal said nothing is written although unreadable answers go to `findings.md`. Fixed; test `test_the_malformed_refusal_says_that_unreadable_answers_are_kept`.
- Observation: `parse_rows` also serves phase 2a and phase 6, which now accept open rows too; not tested there; not now.
