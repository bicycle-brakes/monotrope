---
title: "Spec — standin-call-counter"
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
tags: [spec, tests, speed]
class: bounded
appetite: 1
adr_files: []
---

# Spec — standin-call-counter

The swarm test stand-in selects scripted steps using a small per-key counter without changing its scripted answers (bead coding-harness-bxxt.14). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `12c773c5` on 2026-11-25, the swarm stand-in reads and parses every earlier call record just to count the records with its selected key. Those records contain prompts and other potentially large fields, so repeated counting grows with the log; the size of the actual time saving has not been measured (`research.md`, “What exists today”).

## Acceptance criteria

1. When a swarm stand-in selects a scripted step, it obtains the number of earlier calls for the selected scenario key from a small counter beside the call log without reading the log's records for that count when the counter matches the current log.
   *Refuted by:* Step selection reads prior call records, or uses a count for a different key.
2. When parallel swarm calls select steps, each call's count equals the number of earlier records with its selected key in the serialized call log.
   *Refuted by:* Two records for one key receive the same earlier-call count, or a call counts a record later in the log.
3. When the same sequential scripted calls are run with a frozen, verbatim copy of the former log-based count expression and the new counter, their answers are identical, including key selection and exhausted steps with and without `repeat_last`.
   *Refuted by:* A scripted call produces a different answer or exit status.
4. When the call log is removed, the next call uses a fresh history and starts its selected key at zero, including after direct removal or fixture rewind.
   *Refuted by:* A call after either kind of removal selects a later step or the new log contains a record from the removed history.
5. If the counter is missing, unreadable, truncated, of unknown shape, or its recorded device, inode and post-update byte size differ from the current log, the count is rebuilt from the current log's records before selecting a step.
   *Refuted by:* A nonempty current log with a missing, unreadable, truncated, unknown-shaped or mismatched counter raises or yields a stale count instead of its actual per-key count; this includes a recreated log with a reused inode and a different size.
6. When a writer holding the old log open finishes after removal and a new run has begun, its record and count do not affect the new run's step selection.
   *Refuted by:* A synchronized late old writer causes a new-run call to skip or repeat a step, or places its record in the new log.
7. While the counter is used, it is declared to the stand-in file guard and its access follows the shared locked helper protocol.
   *Refuted by:* Raw guarded access succeeds outside the helper, or concurrent access exposes a partial counter or log record.
8. When a counter update is published, readers see a complete counter even if an old-log writer publishes concurrently.
   *Refuted by:* A synchronized old and new writer exposes a partially written counter to a reader.

## Non-goals

- Change the separate stand-in in `tests/test_stage2.py`, its assignment logic, or other suites' log readers.
- Promise a particular wall-clock speedup; the baseline contribution has not been measured.
- Change production swarm behavior, model routing, leak checks or verification gates.

## Protected areas

Production code and the separate stand-in are outside this test-infrastructure fix. Existing call records and their readers retain their contract.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with the code: this spec and plan; no model or ADR change.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes the stand-in call counter work item (bead `coding-harness-bxxt.14`), and its last commit carries `Closes-Bead: coding-harness-bxxt.14`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The counter is tagged with the log device, inode and byte size after its last update, and is atomically published by temporary file and replacement; an invalid or mismatched counter is rebuilt under the current log lock. This preserves clear-by-removal behavior, including a late old writer (decisions.md D-4 through D-9). A frozen copy of the old count expression makes parity independently refutable. A one-hour implementation appetite is a reversible stop for this small test-only change; it does not prescribe a measured speedup.
