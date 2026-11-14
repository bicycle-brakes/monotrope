---
title: "Spec — runner-clock"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-pph3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, runner, clock, flaky-tests]
class: bounded
appetite: 4
adr_files: []
neighbours: []
---

# Spec — runner-clock

Make the runner's timing tests independent of machine load through one
injectable clock boundary, without weakening execution limits or process
cleanup (bead coding-harness-pph3 — runner clock and load-flaky tests).
Research: [research.md](research.md). Decision: [decisions.md](decisions.md#q-1--how-the-load-flaky-timing-tests-become-robust).

## Problem

At `9140bfb6` on 2026-11-14, the runner has a test seam for monotonic
time, but its remaining-budget helper and review-round expiry checks bypass
it. A fake clock therefore cannot control the whole timing policy
(research, “What exists today” and “Where it lives”).

The verification-admission test combines a two-second execution allowance,
one second of queueing and a child sleeping for 1.5 seconds. Under parallel
load, scheduling consumes that margin and produces a timeout despite a
correct admission boundary. Research cites failures in the verification-order,
research-routing and compaction review records, dated 2026-11-14.

Other tests use real short deadlines, child sleeps and elapsed-time assertions
for reviewer expiry, discovery and cleanup. Moving only runner clock reads
cannot accelerate a child's sleep or the standard library's process wait
(research, “What is unclear about it”, items 5–6). The tests must control both
the policy clock and the outcome of the process wait where timing is simulated.

## Terms

- **Runner:** `scripts/stage2.py`; imported components retain their own clock boundaries.
- **Clock boundary:** the single function through which this module obtains
  current monotonic time, UTC wall time and local calendar dates.
- **Timing test:** a runner test whose verdict depends on a short real-time
  allowance, an elapsed-duration comparison or sleeping to cross a deadline.
  A bounded wait used only to stop a stuck integration test is a watchdog,
  not evidence that a timing policy is correct.

## Acceptance criteria

1. When runner code obtains the current time or date, it does so through one
   replaceable clock function.
   *Refuted by:* a current monotonic, wall-clock or calendar-date read in
   `scripts/stage2.py` outside that function, including a read through an alias.
   *Basis:* decisions.md#Q-1; research, existing seams and direct reads.

2. If a direct clock read or sleep is introduced outside the clock boundary
   in the runner, a source test fails without adding an exemption for that site.
   *Refuted by:* accepting `time.monotonic`, `time.time`, `time.sleep`,
   `time.perf_counter`, their nanosecond variants, other current-time APIs
   (including CPU clocks and no-argument local/UTC time conversion),
   `date.today` or `datetime.now`/`utcnow`/`today` outside the boundary,
   including imported aliases;
   or requiring a list of permitted caller functions or source lines.
   *Basis:* decisions.md#Q-1; research, source-guard precedent.

3. While verification waits for admission, advancing the injected clock by
   more than the execution allowance leaves that allowance available in full
   when execution begins.
   *Refuted by:* a simulated timely check failing because it queued, or a
   simulated over-budget check succeeding; both outcomes must be checked
   without real sleeping or a real queue holder.
   *Basis:* decisions.md#Q-1; research, verification-admission failure.

4. When any runner timing test exercises a deadline or duration policy, its
   result is determined by an injected clock and controlled wait outcomes.
   *Refuted by:* a test still requiring a child to finish within a small
   real-time margin, a real sleep to expire a budget, a duration comparison
   against the machine clock, or a fake that passes without checking the
   production path's supplied timeout/deadline.
   *Basis:* decisions.md#Q-1; research, timing-test population and subprocess boundary.

5. When the clock is injected or uses its production implementation, existing
   timing meanings remain unchanged: durations use monotonic differences,
   terms use UTC dates, and document stamps use local dates.
   *Refuted by:* a wall-clock jump changing a measured duration, a timezone
   boundary making terms use the local date or stamps use the UTC date, or
   an existing independently pinned date/time seam ceasing to work.
   *Basis:* decisions.md#Q-1; research, paired clock seams and wall-clock sites.

6. When a launched program exceeds its allowance or the runner is interrupted,
   the existing bounded cleanup and diagnostic behavior remains effective.
   *Refuted by:* a changed production limit, a surviving process group after
   cleanup, an unbounded drain of escaped descendants, lost timeout diagnostics,
   or replacing all operating-system cleanup evidence with simulated processes.
   *Basis:* decisions.md#Q-1; research, existing execution and drain limits.

## Non-goals

- Increasing timeouts, serializing the suite, reducing parallel workers or
  replacing a failing assertion with a larger timing margin.
- A repository-wide clock framework, a new runtime setting, changing how
  the standard library measures subprocess timeouts, or virtualizing an
  actual operating-system scheduler.
- Changes to the time-record schema, admission protocol, model selection,
  terms policy or the verification workload.
- A design document or ADR: the class is `bounded`, and this refactor adds
  an injection boundary inside an existing component.

## Protected areas

- `scripts/verify_lock.py`, `scripts/verify_duration.py`, `scripts/time_records.py`
  and `scripts/stage2_research_*.py` — independent components, outside this
  runner-module refactor; their production clocks and protocols stay intact.
- `tests/test_verify_lock.py` — real admission integration evidence stays intact.
- Held configuration, governance and harness paths, including `AGENTS.md`,
  `provenance.yaml`, `decisions/`, `model-endpoints.yaml`, `prompts/`,
  `templates/` and the harness dot-directories — no policy change is required.

## Definition of Done

- The runner's full `make verify` is green at the reviewed commit.
- Moved in the same pull request: this spec and `plan.md`, with implementation
  status, criterion-ledger progress and measured phase-4 time; no ADR or other
  policy document changes.
- The source guard is proven red by representative bypasses and green on the
  clock boundary; timing tests pass under serial and parallel execution.
- The pull request's file list preserves the protected areas and non-goals.
- The pull request closes the runner-clock work item; its final commit carries
  `Closes-Bead: coding-harness-pph3`.

## Open decisions

None open. The maintainer's answer in Q-1 is unchanged.

- [DETAIL] Guard the runner module, including its wall-clock/date reads;
  independent imported components are outside this bounded change. This
  follows the decision's named module and avoids introducing a shared service.
- [DETAIL] Preserve the existing `utc_now`, `monotonic_now`, `today` and
  `terms_today` seams as adapters, so existing callers and date pins keep
  their meaning while the raw reads have one boundary.
- [DETAIL] Use four hours of phase 4, repairs included, as a stop: the
  interview states no appetite, and the test-boundary work is bounded here.
- [DETAIL] The second test name in Q-1,
  `test_before_admission_execution_budget_is_shared_and_wait_free`, is absent
  from this worktree at `9140bfb6` (2026-11-14). It is not silently renamed
  to the nested-admission test. Criterion 4 covers the entire present timing
  class; the plan records the missing name for reconciliation if that test
  arrives before merge, without adding a new budget policy.
