---
title: "Measurements — verify-two-slots"
category: measurements
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3-flash, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [measurements, verification]
---

# Measurements — verify-two-slots

**Status: the criterion-12 trial ran green on 2026-11-22** (orchestrator, Claude Code; the implement attempt could not run commands). Every field below is recorded; the raw report and the five full run logs are kept in the orchestrator's session scratchpad (`u1ha-trial-report.json`, `trial-*.log`).

## Trial — two simultaneous `make verify` against one serial run

Required by spec criterion 12 (`spec.md`); the 1.6 threshold is carried by
the 2026-11-17 handover. Every field below is recorded; a trial recorded with
any of them missing would be invalid.

| Field | Requirement | Recorded |
| --- | --- | --- |
| Trial revision | committed revision whose final `scripts/` tree matches HEAD: `git diff <trial-commit>..HEAD -- scripts/` empty | `127e5fa5` (`fix(verify-two-slots): repair taken findings L3-2 … L3-7`); `git diff 127e5fa5..HEAD -- scripts/` empty at recording |
| Worktrees | two separate worktrees at the trial revision | two detached worktrees at `127e5fa5` under the session scratchpad (`u1ha-trial-a`, `u1ha-trial-b`), each with its own `.venv` and the pinned Pi installed (`tools/pi/install.sh`) |
| Warm-up | one discarded warm-up per worktree, before the serial run; warm-up identifiers and order recorded | warm-up A then warm-up B, both green (run ids `5c142dd9…`, `ac1ea2e8…`); an earlier attempt of the trial stopped at warm-up A on 2026-11-22 09:32 because the pinned Pi was not installed in the fresh worktree (110 tests failed for that reason only) and was restarted from scratch after `tools/pi/install.sh` |
| Order | warm-ups, then the serial run, then the simultaneous pair; each trial started with both slots free | warm-up A, warm-up B, serial A, then the pair A+B started together; both slots free at each start (holder samples empty before each run) |
| Date and settings | date, `HARNESS_VERIFY_SLOTS` and worker calculation (unchanged default) recorded | 2026-11-22, 09:46–10:56 CET; `HARNESS_VERIFY_SLOTS` unset (default 2); worker calculation unchanged |
| Verdicts and exits | all three invocations exit zero | all five invocations exit 0 (warm-ups, serial, pair A, pair B) |
| Wall times | each invocation's launch-to-exit wall time, individual | serial A 869.4 s; pair A 1120.5 s; pair B 1120.5 s (warm-ups 896.5 s and 896.4 s) |
| Execution seconds | per invocation | serial 867.3 s; pair 1118.0 s and 1118.0 s (`verify-duration.jsonl` run_end `seconds`, run ids `6140d8dc…`, `e7548c08…`, `37e5c95c…`) |
| Admission wait | combined queue-plus-memory wait seconds, per invocation | serial 0.002 s; pair 0.002 s and 0.005 s (combined queue-plus-memory, `admission_wait_seconds`) |
| Ratios | each simultaneous run's wall time over the serial run's, at most 1.6 | pair A 1.289, pair B 1.289 — both at most 1.6 |
| Load | background processes/lanes; start and end 1-, 5- and 15-minute load averages | start `{ 3.81 5.83 5.29 }`, end `{ 2.40 6.51 8.17 }` (1/5/15-minute); background: other lanes idle (Codex usage-limited), no stage2 or pytest job outside the trial |
| Memory | starting and minimum available memory percentage; an external sampler reading `verify_lock.read_available_memory()` every five seconds, gaps over 15 seconds invalidate | start 69 %, minimum 62 %; sampler read `verify_lock.read_available_memory()` every 5 s for the whole trial, largest gap 5.1 s |
| Admission observation | every protected admission seen in each run, with intervals; no extra admission over the serial run, no third admission over the pair | holder records sampled every 5 s: never more than two (`verify.holder.1.json`, `verify.holder.2.json`) and only during the pair; one during each single run; no third admission seen. **Limit (phase 6, O6-5):** this is a 5-second sample of holder records, not per-admission intervals, and the queue directory `verify.queue/` was not sampled, so an admission shorter than 5 s or a contending third waiter would not show; the trial is recorded with this limit, not rerun |
| Failure attribution | a failed parallel test rerun serially on the same revision: serial pass = parallelism-caused, serial failure = content failure; stop and report on any trial failure | no test failed in the recorded trial, so none needed classification |

## Scope notes

- One paired trial demonstrates zero observed failures, not a statistical
  absence of flakes; no long-run claim is made from it.
- Later commits, all outside `scripts/` (checked with `git diff 127e5fa5..<commit> -- scripts/`, empty): `6655dbbf` and `bec58b9c` (this record), `60d3931d` (phase-6 verdict). A repair of the phase-6 rows that touches `scripts/` invalidates the trial and requires it again.
- The raw report and run logs stay in the orchestrator's session scratchpad and are not committed; the table above is the record.
- A later change to `scripts/` after a recorded trial invalidates it and
  requires the complete trial again, within the four-hour appetite.
  Documentation-only, test-only or plans changes after the trial are
  verified and noted here without a rerun.
- If any trial run fails or cannot run — including a non-test gate failure
  or a timeout — the trial stops and reports; nothing is recorded as a pass.
