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
Done when: The driver and night routine respect the runner’s instruction, stops and step limit, and verification passes.
Appetite: 8 hours for phase 4, including repairs; stop at the limit.
Not now: Producing the next-step instruction, external triggers and lifecycle updates.
Pre-mortem: suppose it failed: most likely because the driver misreads the runner's handoff.
Starts unless you say stop.
```

## Prerequisites and steps

1. Wait for `ladder-next-step` (bead coding-harness-hwll) to land with its schema-validated `next.json` instruction contract, including hand actions; inspect its contract and integrate it without a second decision engine. Do not implement until it exists.
2. Create `scripts/lanes.py`: read `${XDG_STATE_HOME:-~/.local/state}/coding-harness/lanes.json` as a schema-validated ordered JSON array of objects with `change`, `worktree` and optional `park_reason`; a missing file is an empty list, while an invalid existing file or duplicate changes refuses the call. Provide `add`, `remove`, `clear` and `hold` subcommands as the sole writers of operator changes, using the same locks and atomic file replacement as `advance`. Try a per-lane lock without blocking; skip a contended lane as nothing to do and report the reason on stderr. Under that lock reread the current entry and mark before acting; hold a file lock for each read-modify-write, preserving concurrent updates. Run one lane at a time, validate its worktree, read `next.json` beside its own loop record and invoke its own runner as a child. Park on exit 1, signal termination (including 128 plus signal or no exit code), hand instruction, invalid instruction or invalid worktree; report the reason and contribute exit 1. Runner exit 2 stops without parking and contributes exit 1. A missing instruction, parked lane, or unchanged instruction content after success ends the lane without a new park. When a successful step reaches either limit, end as advanced before reading the new instruction. Clear a park through the `clear` subcommand.
3. Create `lane-driver.yaml` as the central configuration: `allowed` initially `[repair, review, review-loop, release-loop, prepare-loop, implement]`, `counted` initially `[implement, repair, review]`, `per_lane_limit` initially `2`, and `all_steps_limit` initially `6`. Validate the verify-bearing limit as an integer in 1–5 and the all-step limit as an integer in 1–20; validate both verb lists before running. The verify-bearing limit defaults to two if absent; absent or malformed lists, unknown runner verbs, or a counted list outside the allow list refuse the call. Return 0 when all selected lanes advance or have nothing to do, 1 when any lane stops, and 2 for a refused call.
4. Create `tests/test_lanes.py` with isolated state, distinct worktrees and a fake runner; exercise the ledger and verify no unexpected invocation occurs. Preserve the runner's admission, locks, commits and push behavior.
5. Orchestrator only: amend `docs/adr/0021-review-swarms-until-clean.md` with the proposal in `design.md`, retaining all existing stops. The recorded decision explicitly forbids a new ADR, while the draft instruction demanded the separate draft `docs/adr/0026-local-lane-driver.md`; resolve that conflict before treating either ADR deliverable as final. The implement attempt must not touch held paths.
6. Change `docs/WORKFLOW.md` to replace the per-run free-text lanes file and hand-start routine with `python3 scripts/lanes.py advance`, using the one machine-local file shared by concurrent runs under the locks; add each lane when work starts and remove its entry before its worktree. Run `make verify`. Do not change the next-step producer, runner verb registries, thirteen-verb prose or its pinned tests; do not introduce external triggers or a lifecycle writer.

The review did not settle what happens when the driver itself is terminated during a step; phase 6 must treat this as a named limit, not as a settled child-exit case.

The separate draft `docs/adr/0026-local-lane-driver.md` records the proposed architecture without changing the maintainer’s answer; its disposition remains unresolved. The change artifacts `spec.md`, `design.md`, `plan.md` and `findings.md` record the specification, design, plan and review disposition.

## Criterion ledger

- 1: not yet written tests/test_lanes.py::test_listed_lanes — The driver reads entries out of order or omits one.
- 2: not yet written tests/test_lanes.py::test_target_exclusive — Another or unlisted change runs.
- 3: not yet written tests/test_lanes.py::test_invalid_file_refused — A malformed file starts a step or is not refused.
- 4: not yet written tests/test_lanes.py::test_worktree_isolation — A record or execution belongs to another checkout.
- 5: not yet written tests/test_lanes.py::test_latest_instruction — The driver reads loop.md or ignores a valid next.json.
- 6: not yet written tests/test_lanes.py::test_invalid_instruction — The driver guesses or starts the instruction.
- 7: not yet written tests/test_lanes.py::test_child_process — A different step runs or the runner is called in-process.
- 8: not yet written tests/test_lanes.py::test_allow_list — A listed verb is refused as disallowed or another verb is accepted.
- 9: not yet written tests/test_lanes.py::test_counted_list — One of these is not counted or an unlisted verb is counted.
- 10: not yet written tests/test_lanes.py::test_per_lane_limit — The new instruction is read, another step starts, or reaching either limit parks the lane.
- 11: not yet written tests/test_lanes.py::test_default_limit — The default differs from two.
- 12: not yet written tests/test_lanes.py::test_invalid_limit — An invalid value is accepted or a step starts.
- 13: not yet written tests/test_lanes.py::test_hand_and_failure — A subsequent step starts in the stopped lane.
- 14: not yet written tests/test_lanes.py::test_park_persists — A later call retries a parked lane without clearing it or the reason is missing.
- 15: not yet written tests/test_lanes.py::test_sequential_lanes — A stop aborts the remaining lanes or lanes overlap.
- 16: not yet written tests/test_lanes.py::test_stop_reporting — Standard error lacks the reason.
- 17: not yet written tests/test_lanes.py::test_exit_codes — An outcome has a different exit code.
- 18: not yet written tests/test_lanes.py::test_lifecycle_untouched — The driver itself changes such a field.
- 19: not a test — phase-6 review checks the ADR amendment against the criterion and existing stops.

- 20: not yet written tests/test_lanes.py::test_missing_record_or_instruction — A missing next.json parks the lane.
- 21: not yet written tests/test_lanes.py::test_used_instruction — The same instruction starts twice in one call.
- 22: not yet written tests/test_lanes.py::test_parked_lane_skipped — A parked lane runs, counts as a stop, or its reason is not reported.
- 23: not yet written tests/test_lanes.py::test_runner_refusal — Exit 2 retries or parks the lane, or does not contribute exit 1.
- 24: not yet written tests/test_lanes.py::test_lane_lock — Concurrent calls work on the same lane, or contention blocks or returns a stop rather than being skipped with a reason.
- 25: not yet written tests/test_lanes.py::test_lanes_file_lock — Concurrent park writes lose a mark, corrupt the file or expose partial JSON.
- 26: not yet written tests/test_lanes.py::test_invalid_worktree_lane_local — A bad worktree refuses all lanes, is not parked, or does not contribute exit 1.
- 27: not yet written tests/test_lanes.py::test_invalid_verb_lists — A missing, invalid or inconsistent list starts a step.
- 28: not a test — phase-6 review checks the night routine against the criterion.
- 29: not yet written tests/test_lanes.py::test_state_subcommands_lock — An operator write loses a concurrent update or bypasses locking.
- 30: not a test — phase-6 review checks that the night routine adds and removes entries in the required order.
- 31: not yet written tests/test_lanes.py::test_all_steps_limit — A sequence of changing uncounted steps exceeds the limit.
- 32: not yet written tests/test_lanes.py::test_initial_all_steps_limit — The initial limit is not six.
- 33: not yet written tests/test_lanes.py::test_invalid_all_steps_limit — An invalid value permits a step.
- 34: not yet written tests/test_lanes.py::test_missing_lanes_file — An untargeted call on a fresh machine refuses or starts a step.
- 35: not yet written tests/test_lanes.py::test_reread_lane_under_lock — A concurrently parked or removed lane runs from stale state.
- 36: not yet written tests/test_lanes.py::test_signalled_child_parks — A signalled child does not park its lane and contribute exit 1.

## Time used

2026-11-24 13:13:43–13:15:49 UTC, 126 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 13:42:29–13:45:58 UTC, 209 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 14:27:02–14:29:57 UTC, 175 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 15:17:01–15:19:39 UTC, 158 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 15:37:51–15:40:00 UTC, 129 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 17:38:44–17:41:24 UTC, 161 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
