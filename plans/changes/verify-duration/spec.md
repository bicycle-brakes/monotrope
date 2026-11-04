---
title: "Spec — verify-duration"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-1um6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, measurement]
class: spike
appetite: 4
adr_files: []
neighbours: [plans/changes/verify-machine-lock/spec.md, plans/changes/verify-worker-cap/spec.md, plans/changes/draft-gates-only/spec.md, plans/changes/swarm-test-speed/spec.md, plans/changes/runner-time-line/spec.md, plans/changes/run-report/spec.md, plans/changes/time-records-data/spec.md, plans/specs/implementation-verification/spec.md]
---

# Spec — verify-duration

Make verification durations comparable across runs by measuring each gate,
keeping local machine context, and delivering a measured baseline and a budget
proposal (bead coding-harness-1um6 — verification duration measurement).
Research: `research.md`. Maintainer answers: `decisions.md`, Q-1 through Q-3.

## Problem

At commit `4d57b1c0`, inspected 2026-11-04, `scripts/verify_all.sh` prints
gate verdicts without measuring their duration; existing duration figures are
dated prose from hand measurements (`research.md`, “What exists today”).
The machine admission can wait for a turn and free memory, and worker settings
affect execution, so timing the outer command alone cannot explain differences.
Existing model-attempt records describe another activity and supply no gate
baseline. The interview settles the research's open goal: persistent local
measurements, at least five runs, and a proposed warning threshold.

## Terms

- **Run:** one admitted execution of the runner's selected job and placement;
  its report identifies the commit and gate configuration actually checked.
- **Gate seconds:** elapsed monotonic time around one executed gate command.
- **Execution seconds:** elapsed monotonic time from the admitted runner's
  measurement start before its report and gate selection to its final verdict;
  includes runner overhead, excludes admission wait.
- **Admission wait:** queue plus memory-floor wait before protected execution;
  an inherited admission identifies its original wait as reused context.
- **Workers:** the effective `PYTEST_XDIST_AUTO_NUM_WORKERS` setting passed to
  the gates; an unset value means xdist decides, not a measured worker count.
  Baseline evidence also records the count pytest actually starts.

## Acceptance criteria

1. When a selected gate command finishes, the console identifies that gate's measured seconds and raw pass/fail result.
   *Refuted by:* a failed advisory gate has no duration, is labelled passed, or an unexecuted gate is presented as measured.
   *Basis:* decisions.md#Q-1.

2. When an admitted run reaches its final verdict, the console reports execution seconds separately from admission wait.
   *Refuted by:* an injected admission delay increases reported execution seconds, or clock adjustments produce negative gate seconds.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.

3. When measurement storage is usable, each run appends identifiable gate measurements and its completion outcome to local history outside the repository in the verification admission's state directory.
   *Refuted by:* a second run replaces the first, concurrent or nested runs mix identities, a listing-only invocation adds a run, or an interrupted run is represented as complete.
   *Basis:* decisions.md#Q-2.

4. When a measurement is recorded, it is attributable to its UTC date, commit, dirty state, gate configuration, job, placement, gate or run identity, seconds and result.
   *Refuted by:* runs of different jobs or dirty trees cannot be distinguished, or a failed command loses its exit status in history.
   *Basis:* decisions.md#Q-2; decisions.md#Q-3.

5. When an admitted run starts measuring, its records carry free-memory percentage at execution start, the effective worker setting and admission wait with its admission identity and reuse status, using explicit unknown values for unavailable readings.
   *Refuted by:* unavailable memory becomes zero, a worker override is replaced by a guessed count, or a nested run's inherited wait is attributed to gate execution.
   *Basis:* decisions.md#Q-2.

6. When the local history reader selects a run, it shows its per-gate and execution durations, outcomes and machine context without treating missing completion or malformed history as a successful complete run.
   *Refuted by:* a truncated final row crashes the reader or makes an unfinished run eligible as baseline evidence.
   *Basis:* decisions.md#Q-2; decisions.md#Q-3.

7. If measurement storage cannot be used, the runner visibly reports the missing history while retaining the gate commands' existing execution and verdict behavior.
   *Refuted by:* an append failure suppresses a gate, changes its enforcement, hides missing history, or writes through a substituted history-file symlink.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.

8. When timing is enabled for verify, docs or drift, the runner retains gate selection, order, blocking versus advisory enforcement, worker overrides and the existing shared admission behavior.
   *Refuted by:* a failed blocking gate becomes green, later gates stop running after an advisory failure, or inherited admission queues behind itself.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.

9. When the spike's baseline is delivered, a dated research note identifies at least five complete green full verification runs of the same committed instrumentation revision and configuration, including each run's machine context and pytest's 30 slowest reported durations.
   *Refuted by:* fewer than five qualifying runs, mixed revisions silently pooled, a docs-only run counted, or absent slow-test evidence claimed as measured.
   *Basis:* decisions.md#Q-3.

10. When the spike's budget proposal is delivered, the research note derives a proposed warning threshold from the baseline's execution durations and variation, explaining machine-context limitations and leaving adoption to the maintainer.
    *Refuted by:* a threshold has no measured basis, queue wait is treated as execution cost, or the proposal changes a timeout or introduces a warning gate.
    *Basis:* decisions.md#Q-3.

## Non-goals

- Optimising gates, changing worker sizing or admission policy, or claiming a
  speedup from this baseline.
- Enforcing or adopting a time budget, changing `VERIFY_SECONDS`, adding a
  gate, or changing hosted CI's gate commands.
- Uploading measurements, committing raw local history, retaining full gate
  output in measurement records, or building a telemetry service.
- Extending the model-attempt `## Time used` grammar or its report reader.
- Design phase 2b and an ADR: this is the interviewed `spike`, for which
  neither is required.

## Protected areas

- `decisions/gates.yaml`, `.github/`, `scripts/ci_gates.py`: the single gate
  declaration, its reader and derived hosted workflow stay unchanged.
- `scripts/stage2.py`, `scripts/time_records.py`, `scripts/run_report.py`,
  `scripts/harness.py`: timeout and model-attempt accounting remain separate.
- `AGENTS.md`, `provenance.yaml`, `model-endpoints.yaml`, `prompts/`,
  `templates/`, `.claude/`, `.codex/`, `.agents/`, `.pi/`, `.beads/`,
  `docs/adr/`: no governance or decision change is needed.

## Definition of Done

- `make verify` green after implementation, with its revision recorded.
- Delivered together: the instrumentation, reader, tests, kit membership and
  `docs/research/2026-11-04-verify-duration-baseline.md`; the note dates the
  actual measurements even if collected later.
- At least five qualifying full runs, with `PYTEST_ADDOPTS=--durations=30`,
  machine context, actual pytest worker counts and measured revision in the
  research note; automated tests alone do not complete this spike.
- Protected areas untouched and non-goals unbuilt, shown by the PR file list.
- The PR closes the verification-duration measurement bead and its last commit
  carries `Closes-Bead: coding-harness-1um6`.

## Open decisions

None open. The maintainer's three answers stand unchanged.

- [DETAIL] Phase 4 has a four-hour appetite, repairs and baseline collection
  included; this supplies the spike's missing stop without adopting a runtime
  budget. Stop and report incomplete evidence if it is exhausted.
- [DETAIL] Use monotonic seconds and explicit UTC attribution, with one run
  identity per admitted runner; clock changes and inherited waits must not
  corrupt comparisons.
- [DETAIL] Unknown metadata remains unknown. Inherited admission wait is
  shared context, never added repeatedly to execution totals.
- [DETAIL] An unusable measurement destination warns and leaves verification
  authoritative; such a run cannot supply the required persisted baseline.
- [DETAIL] Use local append-only structured events and a small command-line
  reader, separate from model-attempt records, so interruption is visible as
  missing completion rather than a fabricated verdict.
