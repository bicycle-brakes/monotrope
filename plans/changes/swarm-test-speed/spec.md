---
title: "Spec — swarm-test-speed"
status: draft
implementation_status: partial
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-dca4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, performance, stage2]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — swarm-test-speed

Speed up repeated declaration reads in tests and real swarm runs without
changing admission or reducing test coverage (bead coding-harness-dca4 —
measure suite runtime and speed up its slowest tests). Research:
`research.md`; authorised production scope: `decisions.md#Q-1`.

## Problem

- The isolated full-suite baseline at `dbef390f` on 2026-10-28 took
  520.43 s for pytest with eight workers; 45 of the 50 slowest calls were
  swarm tests (`research.md`, "Orchestrator addendum").
- Profiling the slowest swarm test at `bb1585c7` on 2026-10-28 attributed
  37.3 s cumulatively to 376 declaration reads. They repeatedly parse the
  same 578-line file using pure-Python YAML despite libyaml being available
  (`research.md`, "Orchestrator profile"). Profiled time is not directly
  comparable to the unprofiled 32.9 s baseline for that test.
- Production scope was explicitly allowed on 2026-10-28, conditional on
  continuing to read changed declarations before each slot; deleting or
  renaming tests remains forbidden (`decisions.md#Q-1`).

## Terms

**Declaration:** the current UTF-8 contents of `model-endpoints.yaml` in the
repository supplied to `stage2_availability.read_declaration`.
**Cached parse:** reusable YAML decoding only; never a saved admission,
terms-expiry verdict, leak-check result or model selection.

## Acceptance criteria

1. When the declaration is read, its returned value or refusal text matches
   the existing safe reader's contract, with or without libyaml installed.
   *Refuted by:* different nested values or scalar types, acceptance of an
   unsafe YAML tag, a different empty/non-mapping result, or an unavailable
   C loader preventing an otherwise valid read.
   *Basis:* `decisions.md#Q-1`; `research.md`, "Orchestrator profile".

2. While an unchanged declaration's successful parse remains cached,
   subsequent sequential reads do not parse its YAML again.
   *Refuted by:* an instrumented parser runs again on immediately repeated
   identical successful reads.
   *Basis:* `decisions.md#Q-1`.

3. When declaration contents change between calls, the next read returns
   the new contents regardless of matching file size or modification time.
   *Refuted by:* an in-place edit, atomic replacement, or switch to another
   repository returns the earlier declaration.
   *Basis:* `decisions.md#Q-1`.

4. If the current declaration cannot be read or decoded, the read returns
   `model-endpoints.yaml cannot be read` rather than a previous valid value.
   *Refuted by:* deletion, a simulated read error, invalid UTF-8 or malformed
   YAML after a warm read returns the cached declaration, or restoring a
   valid file leaves a stale refusal.
   *Basis:* `decisions.md#Q-1`.

5. When callers mutate a returned declaration, other reads remain independent
   of that mutation, including concurrent callers in one process.
   *Refuted by:* changing a nested mapping or list affects another result
   or a later read of unchanged contents.
   *Basis:* `decisions.md#Q-1` — behaviour-preserving reuse.

6. When a model call reaches its existing admission boundary, current terms
   and leak checks still determine whether it may launch.
   *Refuted by:* cached data authorises expired terms across a UTC cutoff,
   a declaration edit is ignored by the send guard, or a leak BLOCK permits
   a launch that the existing guard would refuse.
   *Basis:* `decisions.md#Q-1`; `research.md`, "Couplings" and per-slot costs.

7. When the same slowest swarm test is measured before and after this change
   under matched isolated conditions, its median elapsed time decreases.
   *Refuted by:* the after median is at least the before median, either
   set has fewer than three successful unprofiled runs, or conditions differ
   without a new matched comparison.
   *Basis:* `research.md`, baseline and profile; `decisions.md#Q-1`.

8. When the implementation is reviewed against its baseline, all existing
   tests retain their names, collected cases and behavioural assertions.
   *Refuted by:* a removed/renamed test, fewer pre-existing cases, a new skip
   or xfail, weakened assertions, or altered verification parallelism/gates.
   *Basis:* `decisions.md#Q-1` — the bead's other limits stand.

## Non-goals

- Optimising leak checks, dispatch scheduling, subprocess starts, fixture
  setup or unrelated YAML readers; those need separately measured changes.
- Shrinking the test declaration, consolidating duplicate tests, changing
  model terms, adding dependencies or changing verification commands.
- Changing the declaration schema, selection policy, admission decisions,
  external interfaces or persistent state.

## Protected areas

- `decisions/`, `docs/adr/`, `model-endpoints.yaml`, `Makefile`,
  `pyproject.toml`, `requirements-ci.txt` and `.github/workflows/`: no rule,
  live declaration, dependency or gate changes are needed.
- `scripts/stage2_research_run.py`, `scripts/stage2_research_dispatch.py`
  and `scripts/leakcheck.py`: the call-boundary and scan behaviour stays intact.
- Other change folders and their criterion ledgers: no test rename or
  requirement change is necessary.

## Definition of Done

- `make verify` green with the existing command and pinned environment.
- Criteria 1–6 have regression evidence; all eight criteria have ledger entries.
- Before/after measurements and full-suite elapsed time are recorded with
  date, baseline/implementation revision, environment and result counts in
  this change's `plan.md`; the PR carries that evidence.
- Documents moving with the code: this change's `spec.md`, `plan.md` and
  runner-managed `findings.md`; no living spec, model file or ADR changes.
- Protected areas untouched and non-goals unbuilt, checked from the PR diff.
- The PR closes bead coding-harness-dca4 — measure suite runtime and speed up
  its slowest tests; its last commit carries `Closes-Bead: coding-harness-dca4`.

## Open decisions

None open. The maintainer's production-scope answer is not reopened.

- [DETAIL] Use a two-hour implementation appetite, including repairs, as a
  stop because this is one shared-reader optimisation, not a suite rewrite.
- [DETAIL] Compare three before and three after runs using a lower median,
  without promising an invented percentage; the historical baseline is context,
  not a matched acceptance measurement.
- [DETAIL] No design phase or ADR: this remains `bounded`, with the existing
  reader interface and admission boundaries preserved. The non-swarm Explore
  report proposed neighbours but supplies no complete research-swarm handoff;
  `neighbours: []` makes no such claim.
