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

1. Change `tests/atomic_test_log.py`: declare a counter file beside `calls.jsonl`; under the log inode's exclusive lock, use a counter tagged with the log's device and inode, rebuilding per-key counts from that locked log if the counter is missing or has another identity. Select the step, populate its `sleep` field and append the complete record under that lock, then publish the updated counter atomically so writers on old and new inodes cannot expose a partial counter. On a later identity mismatch rebuild from the current log, including when a late old writer overwrote the counter. Keep the fast path free of log-record reads and the counter proportional to distinct keys.
2. Change `tests/test_stage2_swarm.py`: use the helper in the embedded stand-in, preserving key fallback, record fields, scripted outputs and `repeat_last`; preserve direct unlink and `SwarmWorld.rewind` semantics. Version calls remain outside the call count.
3. Change `tests/stand_in_log_guard.py`: admit the helper's locked access while retaining refusal of raw accesses to declared files. Change `tests/test_atomic_test_log.py` for guard enforcement, serialized parallel writers and synchronized late old-inode writers. Add `tests/test_standin_call_counter.py` for reference parity, key isolation, no log read on the matching fast path, direct removal, rewind and missing or mismatched counter recovery. Synchronize processes rather than relying on sleeps; compare indices with log order and check complete records.
4. Change this `plan.md` to update ledger entries once tests exist and record phase-4 time and evidence. The runner owns `findings.md`, index generation, full verification and the commit. No other files are created, changed or deleted.

The counter name and helper interface are reversible implementation details. The shared log lock and identity-tagged atomic counter publication preserve the existing clear-by-removal protocol, including concurrent old and new log inodes.

## Criterion ledger

- 1: not yet written tests/test_standin_call_counter.py::test_count_uses_counter_without_reading_log — a prior-record read on the matching fast path or a count from another key fails.
- 2: not yet written tests/test_atomic_test_log.py::test_counter_serializes_parallel_calls_with_log — duplicate indices or indices out of log order fail.
- 3: not yet written tests/test_standin_call_counter.py::test_scripted_answers_match_log_count — a changed answer or exit status across key fallbacks and exhaustion fails.
- 4: not yet written tests/test_standin_call_counter.py::test_removal_and_rewind_clear_history — a stale record or later step survives either reset.
- 5: not yet written tests/test_standin_call_counter.py::test_missing_or_mismatched_counter_rebuilds — a nonempty log produces a stale or zero count.
- 6: not yet written tests/test_atomic_test_log.py::test_late_old_writer_does_not_affect_new_log — a synchronized old writer changes the new history or step count.
- 7: not yet written tests/test_atomic_test_log.py::test_counter_guard_and_locked_access — raw access succeeds or a reader sees a partial counter or record.

## Verification and boundaries

Run focused checks during implementation, then the required full verification:

```bash
.venv/bin/python -m pytest tests/test_atomic_test_log.py tests/test_standin_call_counter.py tests/test_stage2_swarm.py -q
make verify
```

Do not alter `tests/test_stage2.py`, other stand-ins, production code, model declarations or gates. Stop at the appetite and report any unmet criteria. The orchestrator handles any held path; this plan requires none. The advertised `scripts/validate_change_artefacts.py` is absent at `12c773c5`.

## Time used

2026-11-25 04:23:01–04:24:52 UTC, 111 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 04:29:18–04:30:46 UTC, 88 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
