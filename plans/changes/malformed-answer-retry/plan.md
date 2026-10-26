---
title: "Plan — malformed-answer-retry"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-70rw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — malformed-answer-retry

```text
For you:     A reviewer's formatting slip no longer fails the round; the runner asks once more.
Done when:   The five criteria hold in tests written red first, and make verify is green.
Appetite:    2 hours of phase 4; stop at the limit.
Not now:     Malformed phase-6 verdicts; rows without a closing pipe.
Pre-mortem:  suppose it failed: most likely because the retry's call line is not counted, so a lost round is misread.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the five tests in the ledger, red first.
2. `scripts/stage2.py`: a `MalformedAnswer` error carrying the answer;
   `run_swarm` raises it; after the initial swarm, before Flash
   replacement, the round asks each member with a `MalformedAnswer` once
   more. Each replacement gets the same retry before another rung is spent.
   Both paths use `checked_prompt`, `call_line`, `audited` and the round's
   deadline; the record keeps the runner line and both answers, including a
   malformed second answer. Failed attempts keep the skipped-retry reason
   and any malformed answers in the no-round audit.
3. `docs/WORKFLOW.md` §4b: one sentence on the retry.
4. This change folder and `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k "malformed or asked_again or format_reminder or test_the_second_call_has_its_own_call_line or test_no_second_call_after_the_round_deadline or test_a_leak_block_on_the_retry_prompt_makes_no_second_call or test_a_round_failed_past_the_deadline_names_the_skipped_retry"
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_malformed_answer_is_asked_once_more — the round fails on the first malformed answer.
- 2: tests/test_stage2.py::test_the_first_malformed_answer_is_kept_in_the_round — the record drops the first answer.
- 3: tests/test_stage2.py::test_a_second_malformed_answer_fails_the_member — the member is asked a third time or passes.
- 4: tests/test_stage2.py::test_the_second_call_has_its_own_call_line — the second call writes no call line.
- 5: tests/test_stage2.py::test_no_second_call_after_the_round_deadline — a second call starts after the deadline.

## Time used

2026-10-26 10:04:39–10:42:34 UTC, 2275 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
2026-10-26 12:35:24–12:48:25 UTC, 781 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
