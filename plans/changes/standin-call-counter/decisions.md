---
title: "Decisions — standin-call-counter"
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
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, speed]
---

# standin-call-counter — Decisions

## SKIP · interview

status: skipped
reason: A test-infrastructure speed fix with a stated remedy (bead coding-harness-bxxt.14, filed at the maintainer's request on 2026-11-24 from a checked analysis): the swarm test stand-in counts its earlier calls per key from a small counter instead of re-parsing the whole calls.jsonl; what the stand-in answers must not change, so no design choice is left to the maintainer.

## Details decided by the orchestrator

[DETAIL] **D-1 (where the counter lives)**: the counter is one more file beside calls.jsonl, declared in `STAND_IN_LOGS` like the log itself, so the stand-in log guard knows it. Reason: the guard only accepts declared stand-in files.

[DETAIL] **D-2 (exact counts under parallel calls)**: the counter is read and updated under the same file lock, in the same critical section, as the append to calls.jsonl, so for every call it equals the number of earlier records the log-based count would find (including the `kind` and `name` filters and the `repeat_last` fallback the count feeds). Reason: swarm stand-ins run in parallel; an unlocked read-modify-write would race.

[DETAIL] **D-3 (parity and scope)**: a test runs the same scripted calls through the old log-based count and the new counter and asserts identical answers; only the swarm stand-in (tests/test_stage2_swarm.py) changes — the tests/test_stage2.py stand-in, which uses its records for more than counting, stays as it is. Reason: the verified analysis found only the swarm stand-in counts.
