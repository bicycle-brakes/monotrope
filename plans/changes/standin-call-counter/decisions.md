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

[DETAIL] **D-4 (spec review S-1, what resets the counter)**: anything that removes calls.jsonl resets the count, not only `SwarmWorld.rewind`: the counter records the identity (device and inode) of the log file it belongs to; when the log under the lock has a different identity than the counter records, or the counter is missing, the stand-in rebuilds the counter once from the log's own records and goes on from there. The 32 direct unlinks in the swarm and deep-review tests therefore stay correct without edits. Reason: today removing the log is the reset, and a separate counter must not go stale.

[DETAIL] **D-5 (spec review S-2, keeping clear-by-removal; refines D-2)**: the counter is read and written only while the stand-in holds the lock on the log's own inode, and every counter write carries that inode; a late writer of a cleared run that still holds the removed inode writes a counter tagged with the removed identity, which the next run ignores by D-4. Reason: the shared locked protocol clears a log by removing it, and the counter must keep that guarantee.

[DETAIL] **D-6 (spec review round 2 S-1, inode reuse; refines D-4)**: the counter's tag is the log's device, inode and byte size right after the counter's last update; the counter describes the current log only when all three match under the lock, so a log recreated on a reused inode (size 0, or any size other than the recorded one) forces a rebuild from the log. Reason: inode numbers are reused after unlink.

[DETAIL] **D-7 (round 2 S-2, the parity oracle)**: the parity test keeps a frozen, verbatim copy of today's log-based count expression as its oracle, not a re-derivation from the counter's formula. Reason: otherwise the parity holds by construction.

[DETAIL] **D-8 (round 2 S-3, a late writer; refines D-5)**: the counter is written by a temporary file plus `os.replace`, always tagged per D-6; a late writer still holding the removed log's inode may replace the counter file, but its tag then names the removed log, so the next reader rebuilds from the current log. Correctness rests on the tag check, not on a lock shared across runs. Reason: no lock covers a removed and a new inode at once.

[DETAIL] **D-9 (round 2 S-4, foreign shape)**: a counter that is missing, unreadable, truncated or of an unknown shape is rebuilt from the log; the stand-in never raises on it. Reason: a raise would break every swarm run.

