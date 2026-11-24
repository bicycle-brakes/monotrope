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

1. Wait for `ladder-next-step` (bead coding-harness-hwll) to land with recorded latest instructions, their grammar and `next: hand`; inspect its contract and integrate it without a second decision engine. Do not implement until it exists.
2. Create `scripts/lanes.py`: read `${XDG_STATE_HOME:-~/.local/state}/coding-harness/lanes.yaml` as an ordered YAML list of mappings with `change`, `worktree` and optional `park_reason`; validate the whole file, reject duplicate changes and invalid paths before action, select the optional target, and persist stop reasons. Existing free-text night-run lists must be replaced with this format by the operator. Run one lane at a time, read its own record, invoke the runner in that worktree in a child process, and re-read the record after each step. Stop on failure, hand instruction, invalid instruction or repeated unchanged instruction (to prevent an unbounded non-counted cycle); persist a park reason and report it on stderr and in the job record. The operator clears `park_reason` to resume. Limit exhaustion is normal completion for that lane.
3. Create `lane-driver.yaml` as the central configuration: `allowed` initially `[repair, review, review-loop, release-loop, prepare-loop, implement]`, `counted` initially `[implement, repair, review]`, and `per_lane_limit` initially `2`; validate the limit as an integer in 1–5 and validate both verb lists before running. Missing setting uses the stated defaults; malformed settings refuse the call. The driver must not use remote labels, comments, branch names or fetched files as inputs. Return 0 when all selected lanes advance or have nothing to do, 1 when any lane stops, and 2 for a refused call.
4. Create `tests/test_lanes.py` with isolated state, distinct worktrees and a fake runner; exercise the ledger and verify no unexpected invocation occurs. Preserve the runner's admission, locks, commits and push behavior.
5. Orchestrator only: amend `docs/adr/0021-review-swarms-until-clean.md` with the proposal in `design.md`, retaining all existing stops. The recorded decision explicitly forbids a new ADR, while the draft instruction demands one; resolve that conflict before treating the ADR deliverable as final. The implement attempt must not touch held paths.
6. Run `make verify`. Do not change the next-step producer, runner verb registries, thirteen-verb prose or its pinned tests; do not introduce external triggers or a lifecycle writer.

The change artifacts `spec.md`, `design.md`, `plan.md` and `findings.md` record the specification, design, plan and review disposition.

## Criterion ledger

- 1: not yet written tests/test_lanes.py::test_listed_lanes — A listed lane is omitted or an absent lane is selected.
- 2: not yet written tests/test_lanes.py::test_target_exclusive — Another or unlisted change runs.
- 3: not yet written tests/test_lanes.py::test_invalid_file_refused — Any step starts or the call is not refused.
- 4: not yet written tests/test_lanes.py::test_worktree_isolation — A record or execution belongs to another checkout.
- 5: not yet written tests/test_lanes.py::test_latest_instruction — An earlier line overrides the latest.
- 6: not yet written tests/test_lanes.py::test_invalid_instruction — The driver guesses or starts the instruction.
- 7: not yet written tests/test_lanes.py::test_child_process — A different step runs or the runner is called in-process.
- 8: not yet written tests/test_lanes.py::test_allow_list — A listed verb is refused as disallowed or another verb is accepted.
- 9: not yet written tests/test_lanes.py::test_counted_list — One of these is not counted or an unlisted verb is counted.
- 10: not yet written tests/test_lanes.py::test_per_lane_limit — The lane starts more counted steps than its limit.
- 11: not yet written tests/test_lanes.py::test_default_limit — The default differs from two.
- 12: not yet written tests/test_lanes.py::test_invalid_limit — An invalid value is accepted or a step starts.
- 13: not yet written tests/test_lanes.py::test_hand_and_failure — A subsequent step starts in the stopped lane.
- 14: not yet written tests/test_lanes.py::test_park_persists — A later call retries a parked lane without clearing it or the reason is missing.
- 15: not yet written tests/test_lanes.py::test_sequential_lanes — A stop aborts the remaining lanes or lanes overlap.
- 16: not yet written tests/test_lanes.py::test_stop_reporting — Either destination lacks the reason.
- 17: not yet written tests/test_lanes.py::test_exit_codes — An outcome has a different exit code.
- 18: not yet written tests/test_lanes.py::test_lifecycle_untouched — The driver itself changes such a field.
- 19: not yet written tests/test_lanes.py::test_remote_ignored — Remote data selects a lane or step.
- 20: not a test — phase-6 review checks the ADR amendment against the criterion and existing stops.

## Time used

2026-11-24 13:13:43–13:15:49 UTC, 126 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 13:42:29–13:45:58 UTC, 209 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
