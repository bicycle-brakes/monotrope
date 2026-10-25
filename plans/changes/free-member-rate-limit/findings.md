---
title: "Findings — free-member-rate-limit"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-pj98
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings]
---

# Findings — free-member-rate-limit

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first:
`tests/test_stage2.py::test_a_rate_limited_free_round_moves_on_to_the_flash_swarm`
failed before the change (exit 1, no round, the 429 failures printed). The
criterion-2 and criterion-3 tests guard today's behaviour and passed before
and after. The full `tests/test_stage2.py` passes except the root-only
`test_an_unreadable_target_is_named_by_its_repository_path`.

- `scripts/stage2.py`: `rate_limited` reads a member's failure;
  `FreeStageUnavailable` is raised from the new `_review_round` when every
  free member failed that way; `review_loop` marks the free stage skipped
  with the reason and takes the next stage in the same call.
- `docs/WORKFLOW.md`: one sentence in the review-loop section.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- The round body moved unchanged into `_review_round`; only the
  rate-limit branch before the all-failed `CallFailed` is new.
- A time-out (`StepTimedOut`) never counts, even if its text says
  "unavailable"; an unreadable or empty answer is no `CallFailed` with
  that text and stays an ordinary failure.
- The availability receipt is spent only with the written round, as before.
- The word "unavailable" is broad: a Pi failure such as "Model is
  unavailable" also counts. The maintainer's answer names unavailability
  errors, so it is meant to.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request, a read-only Opus 5.5 subagent reviewed this
change before the phase-6 Codex review, which this container cannot reach.
Phase 6 is still owed. It found no blocker. The orchestrating session fixed
the rows below test-first, except P247-2, which goes to the maintainer.

- **P247-1 (MAJOR), fixed.** An empty answer with "429" in its last stderr
  line counted as a rate limit, against the DETAIL in decisions.md: the
  empty-answer failure carries that line too. Only a failed exit counts now.
  Tests: a third case of `test_a_free_round_with_an_ordinary_failure_still_writes_nothing`
  and `test_rate_limited_reads_only_a_failed_exit_with_a_rate_limit`, red before.
- **P247-2 (MAJOR, possible divergence), to the maintainer.** Q-1 says a
  rate-limited free member is dropped for the run. The DETAIL narrows it:
  when every member failed and only some failures are rate limits, nothing
  is dropped, because the drop needs a written round to be kept. The spec's
  non-goals now say so. The maintainer decides whether the narrowing
  stands or the drop must survive without a round.
- **P247-3 (MINOR), fixed.** A drop with no stage left gave the refusal
  "the last round was not clean" although no round ran. It now names the
  drop and the missing paid stage (criterion 4). Test:
  `test_a_dropped_free_stage_with_no_stage_left_says_so`, red before.
- **P247-4 (MINOR), wording fixed.** The drop does not survive a call in
  which the next stage fails too (a declared non-goal); criterion 1 now
  says "after the written round", and
  `test_a_failed_stage_after_the_drop_names_the_drop` pins that the drop
  stays visible in that call's output.
- **P247-5 (MINOR), fixed.** The pattern missed `rate_limit_exceeded` and
  `rate_limit_error` and read `429` inside an id. Pinned by the
  parametrised `test_rate_limited_reads_only_a_failed_exit_with_a_rate_limit`.
- **P247-6 (NIT), fixed.** `test_a_time_out_is_never_a_rate_limit` pins the
  time-out exclusion; the drop prints to stdout like the no-diff skip;
  WORKFLOW names the second deadline.
