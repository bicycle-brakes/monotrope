---
title: "Findings — interview-fenced-examples"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-k2r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings]
---

# Findings — interview-fenced-examples

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: all
four new test cases failed before the edit. The gate measures 23 changes
on the repository and stays green.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- An unclosed fence blanks everything after it, as CommonMark reads it;
  a `decisions.md` with a stray fence then loses its later records and
  the gate reports the debt, which is the safe direction.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request a read-only Opus 5.5 subagent reviewed the
change before phase 6 (Codex, unreachable here). Phase 6 is still owed;
this section replaces nothing of it. Repairs were made by a Sonnet 5.5
subagent at the orchestrator's direction, uncommitted.

- P244-1 (MINOR): a CRLF `decisions.md` never matched a closing fence
  (the `\r` defeated `[ \t]*$`), so every real record after the first
  fence was blanked, a false red. Fence lines are now matched without
  their `\r`. Status: repaired.
  Test: `test_a_crlf_file_with_a_closed_fence_still_counts_the_real_record`.
- P244-2 (MINOR): the CommonMark fence rules were not pinned. Added
  five cases (shorter closer, tilde inside a backtick fence, closer with
  an info string, one-line fence, four-space indent). Mutations shown red:
  no closer-length check (1 case), any fence line closes (3 cases), no
  indent limit (1 case), no backtick-info rule (1 case). Status: repaired.
  Test: `test_the_commonmark_fence_rules_decide_what_is_hidden`.
- P244-3 (NIT): the `_records` docstring in `scripts/check_question_context.py`
  said the other gate reads without fence awareness; it now says both
  gates skip fenced content. Status: repaired. No test (prose).
- P244-4 (NIT): an unclosed fence before the real records hides them, so
  the gate counts 0 and fails red, the safe direction; now pinned.
  Status: repaired.
  Test: `test_an_unclosed_fence_before_the_records_hides_them`.
- P244-5 (NIT): the Implementation section above says the gate "measures
  23 changes"; read at commit f255b3d it prints 24. The earlier text stays
  as written; this is the correction. Status: noted.
- P244-6 (NIT): the test derived the closer with `fence.rstrip("markdown")`,
  which strips characters, not a suffix. The closer is now a second
  parametrize value. Status: repaired.
  Test: `test_a_fenced_record_or_skip_is_not_counted`.
