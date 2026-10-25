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
