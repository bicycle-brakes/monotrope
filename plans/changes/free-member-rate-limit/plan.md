---
title: "Plan — free-member-rate-limit"
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
tags: [plan, review-loop, free-swarm]
---

# Plan — free-member-rate-limit

```text
For you:     a rate-limited free model no longer blocks the review loop; the run goes on to the Flash swarm.
Done when:   the three criteria have tests, red first where they change behaviour, and make verify is green but for the container's known limits.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     dropping a member without a completed round; paid members.
Pre-mortem:  suppose it failed: most likely because a time-out or an unreadable answer was read as "unavailable" and silently skipped the free review.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the tests named in the ledger, run red first.
2. `scripts/stage2.py`: a predicate for a rate-limit or unavailability
   failure; the round body of `review_loop` moves into a helper that raises
   a dedicated exception when every free member failed that way;
   `review_loop` then marks the free stage skipped with the reason and takes
   the next stage in the same call.
3. `docs/WORKFLOW.md`: one sentence where the free stage's skip is
   described, if such a place exists.
4. Update this plan, `findings.md` and `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q -n 4 -p no:cacheprovider tests/test_stage2.py -k "rate_limited or free_round or did_not_review"
PYTHON=$PWD/.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_rate_limited_free_round_moves_on_to_the_flash_swarm — the call fails, writes no round, omits the notice, or calls a free member again.
- 2: tests/test_stage2.py::test_a_free_round_with_an_ordinary_failure_still_writes_nothing — a time-out or another exit beside a 429 skips the free stage.
- 2: tests/test_stage2.py::test_a_round_that_did_not_review_writes_nothing — an all-failed round writes a record.
- 3: tests/test_stage2.py::test_a_rate_limited_member_beside_an_answer_keeps_the_free_round — a free round with an answer is skipped or loses the failure statement.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction (conversation 2026-10-25). The review loop and the phase-6
Codex review are still owed.

## Time used
2026-10-25 17:10:17–17:14:47 UTC, 270 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
