---
title: "Plan — advance-verb"
category: plan
created: 2026-11-24
updated: 2026-11-24
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-z40g
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, lanes]
---

# Plan — `advance-verb`

```text
For you: Local lanes can start the runner's named next step without a hand start.
Done when: The driver respects the runner's instruction, stops and step limit, and verification passes.
Appetite: 8 hours for phase 4, including repairs; stop at the limit.
Not now: Producing the next-step instruction, external triggers and lifecycle updates.
Pre-mortem: suppose it failed: most likely because the driver misreads the runner's handoff.
Starts unless you say stop.
```

## Prerequisites and steps

1. Wait for `ladder-next-step` (bead coding-harness-hwll) to land; inspect its authoritative record and held-row signal before implementing. Do not reconstruct its decision from findings or invent a record contract.
2. In `scripts/lanes.py`, implement the local file parser and `advance` command, optional target, strict instruction validation, runner invocation, reasoned stops and central default limit of two verify-bearing steps per call. Count across all lanes in one call; preserve runner safeguards and let runner verbs own pushes.
3. In `tests/test_lanes.py`, exercise the behaviours in the criterion ledger using isolated local records and a fake runner; assert the commands and absence of additional invocations.
4. Orchestrator only: amend `docs/adr/0021-review-swarms-until-clean.md` to describe the separate driver starting the named step and retain all existing stops. Resolve the conflict between the instruction requiring a new ADR draft and the recorded decision requiring only this amendment before treating the design as final.
5. Run `make verify`. The implementation attempt must not edit held paths; the orchestrator applies the ADR amendment after the accepted attempt. The change artifacts `spec.md`, `design.md`, and `plan.md` in this folder document this contract and plan.

Do not edit runner verb registries, thirteen-verb prose, its pinned tests, lifecycle fields or the next-step producer. Do not invoke models except through the runner.

## Criterion ledger

- 1: not yet written tests/test_lanes.py::test_listed_lanes_only — an absent lane starts or a valid listed lane is ignored.
- 2: not yet written tests/test_lanes.py::test_target_is_listed_and_exclusive — an unlisted or other lane starts.
- 3: not yet written tests/test_lanes.py::test_runs_exact_next_instruction — the runner receives a different verb or change.
- 4: not yet written tests/test_lanes.py::test_invalid_next_stops — invalid instructions start a step or lack a reason.
- 5: not yet written tests/test_lanes.py::test_call_step_limit — the call starts more than its configured bound.
- 6: not yet written tests/test_lanes.py::test_failure_and_held_rows_stop — a later step starts after a failure or hand step.
- 7: not yet written tests/test_lanes.py::test_lifecycle_fields_untouched — the driver changes a lifecycle field.
- 8: not yet written tests/test_lanes.py::test_external_state_cannot_trigger — external state starts a step.
- 9: not a test — phase-6 review reads the ADR amendment against the criterion and existing stops.

## Time used

2026-11-24 13:13:43–13:15:49 UTC, 126 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
