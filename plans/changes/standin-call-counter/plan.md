---
title: "Plan — standin-call-counter"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.14
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, speed]
---

# Plan — standin-call-counter

```text
For you:     Swarm tests count prior calls without repeatedly parsing their full prompt log; scripted answers stay the same.
Done when:   Parity, parallel counting, reset and guard checks pass, and make verify is green.
Appetite:    1 hour of phase 4, repairs included; a stop, not an estimate.
Not now:     The other stand-in, production behavior and a promised wall-clock speedup.
Pre-mortem:  suppose it failed: most likely because parallel calls assign a count out of log order.
Starts unless you say stop.
```

Bounded change: no design phase or ADR. No `templates/plan.md` exists at `12c773c5`; this follows `prompts/03-plan.md`. Explore used the Stage-1 route, `claude-haiku-5-5`, because GLM 5.3 Flash via Z.ai had reached its weekly limit.

## Files and steps

1. Change `tests/atomic_test_log.py`: declare a counter file beside `calls.jsonl` and add a shared helper that locks the call log, reads and increments the per-key counter and appends the corresponding complete record under that same lock. Select the step and populate its `sleep` field using the count inside that critical section; retain existing log snapshot locking and error behavior. Do not read the call log to count. Keep the counter bounded by the number of distinct keys, not the number or size of calls.
2. Change `tests/test_stage2_swarm.py`: use that helper in the embedded stand-in, preserving key fallback, scripted outputs, record fields and `repeat_last`; reset both counter and log on `SwarmWorld.rewind`. Version calls remain outside the call count.
3. Change `tests/stand_in_log_guard.py`: admit the new helper's locked access while retaining refusal of raw accesses to declared files. Change `tests/test_atomic_test_log.py` to cover guard enforcement and concurrent writers/readers. Add `tests/test_standin_call_counter.py` for a reference comparison against the former log-based count, key isolation, exhausted steps, no log read for counting, and rewind. Use process synchronization rather than sleeps to exercise parallel calls; compare returned indices with log order and assert complete JSON records.
4. Change this `plan.md` to update ledger entries once tests exist and record phase-4 time and evidence. The runner owns `findings.md`, index generation, full verification and the commit. No other files are created, changed or deleted.

The counter name and helper interface are reversible implementation details; choosing them in phase 4 lets the existing helper's lock and guard remain the single access path. Do not silently rebuild a missing or inconsistent counter from a growing log; surface an error instead of choosing a wrong step.

## Criterion ledger

- 1: not yet written tests/test_standin_call_counter.py::test_count_uses_counter_without_reading_log — a prior-record read or a count from another key changes the result.
- 2: not yet written tests/test_atomic_test_log.py::test_counter_serializes_parallel_calls_with_log — duplicate indices or indices out of log order fail.
- 3: not yet written tests/test_standin_call_counter.py::test_scripted_answers_match_log_count — a changed answer or exit status across key fallbacks and exhaustion fails.
- 4: not yet written tests/test_standin_call_counter.py::test_rewind_clears_log_and_counter — a stale record or later step survives rewind.
- 5: not yet written tests/test_atomic_test_log.py::test_counter_guard_and_locked_access — raw access succeeds or a reader sees a partial record.

## Verification and boundaries

Run focused checks during implementation, then the required full verification:

```bash
.venv/bin/python -m pytest tests/test_atomic_test_log.py tests/test_standin_call_counter.py tests/test_stage2_swarm.py -q
make verify
```

Do not alter `tests/test_stage2.py`, other stand-ins, production code, model declarations or gates. Stop at the appetite and report any unmet criteria. The orchestrator handles any held path; this plan requires none. The advertised `scripts/validate_change_artefacts.py` is absent at `12c773c5`.

## Time used

2026-11-25 04:23:01–04:24:52 UTC, 111 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
