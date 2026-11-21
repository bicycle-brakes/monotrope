---
title: "Spec — deadline-stop-flake"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-j1i5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, flaky-test, review-loop]
class: bounded
appetite: 2
adr_files: []
---

# Spec — deadline-stop-flake

The deadline-stop test reliably exercises and reports a replacement stopped by the shared round limit (bead coding-harness-j1i5). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-08 the full verification run failed because the test found no failure line for the replacement, while it passed alone on the same tree (`decisions.md`; failure output in `plans/changes/archive/2026-11-16-address-drift-warning/findings.md`). That historical output shows the round expired before a replacement started; it predates the current fake-clock fixture, so it does not establish the cause of any present failure.
- The current test already uses a fake clock and simulated processes (`research.md`, 2026-11-21; `tests/test_stage2.py` at `617de302`), but the unexplained load-dependent path must be traced before choosing a repair. The research's proposed research-dispatcher test was an unconfirmed inference, superseded by the identified test in `decisions.md`.

## Acceptance criteria

1. When the identified real-time dependency or uncontrolled scheduling point is held to reproduce the failure, a regression test fails before the repair and passes after it without relying on machine speed.
   *Refuted by:* the forced scenario passes on the unmodified behavior, fails after repair, or depends on a short wall-clock window.
2. When the replacement exceeds its remaining shared round allowance, the test records it as stopped by the round limit with the seconds granted for that call.
   *Refuted by:* the replacement does not start, succeeds, or its failure record omits either the round limit or the seconds granted.
3. When the replacement is stopped by the round limit, the test rejects a diagnostic that names the independent reviewer time limit instead.
   *Refuted by:* a reviewer-limit diagnostic passes the test.
4. When the repair changes runner timing, all runner clock reads on the repaired path remain covered by the existing single clock boundary and guard.
   *Refuted by:* a repaired-path runner clock read bypasses the boundary or the guard no longer catches such a bypass.

## Non-goals

- Changing round limits, timeout policy, admission rules, retries, or adding sleeps to hide the failure.
- Repairing the separate research-dispatcher test suggested by the initial exploration.
- Changing unrelated tests or redesigning runner timing generally.

## Protected areas

- `scripts/stage2_research_dispatch.py` and `scripts/stage2_research_run.py`: the identified failure is in the review loop, not the research dispatcher.
- Held paths listed in `prompts/03-plan.md`: the implementation attempt must not edit them.

## Definition of Done

- The forced regression is shown red before the repair and green after it; targeted checks and `make verify` pass.
- No documents, models or ADRs move with the code beyond this change's artifacts.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes bead `coding-harness-j1i5`; its last commit carries `Closes-Bead: coding-harness-j1i5`.
- Special runs: record the forced red/green regression and repeated targeted run with their commit in the pull request body.

## Open decisions

None open. [DETAIL] Two hours is the phase-4 stop because the bounded investigation needs time to locate and reproduce the dependency; if it is not found, stop and report the trace and measurements in `findings.md` rather than guessing.
