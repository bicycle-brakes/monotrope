---
title: "Plan — isolated-attempts"
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, attempts]
---

# Plan — isolated-attempts

```text
For you:     Failed attempts are contained and writing routes continue visibly after a failed call.
Done when:   Isolation, fallback, cleanup and direct-entry protections pass their tests and make verify; the first rollout has one night of evidence.
Appetite:    24 hours of phase 4, including repairs; stop when spent.
Not now:     Network isolation, foreign-read blocking, containers and changes to research or review-loop routing.
Pre-mortem:  suppose it failed: most likely because shared state lets an attempt alter the lane despite its separate worktree.
Starts unless you say stop.
```

## Files and steps

1. Implementer: add `scripts/stage2_attempts.py` as the shared lifecycle and protected CLI, receiving the runner module and an attempt-specific Context; route implement, repair, draft and review through it in `scripts/stage2.py`. Preserve declared route order and all existing policy checks. Create detached worktrees under the state directory, exclude them from discovery and record-key scans, and prune only this session's orphans. Pin inputs and check lane HEAD before applying an accepted checkpoint. Preserve failed state in scoped refs and remove worktrees. Enforce read-only access to Python and Pi; a symlink alone is not read-only. Refuse the attempt if the protection cannot be enforced; checksum both before and after, reject and restore with `make venv` on mismatch without traversing links. Demonstrate that attempt writes cannot reach the lane or runner inputs; a Git worktree alone is not a security boundary. On failed writing calls record the reason and continue from saved state; stop on leak or restoration refusal.
2. Implementer: change `scripts/close_merged_beads.py` to delete only the merged change's attempt refs locally and on origin; add the lifecycle, CLI, isolation, fallback, cleanup and structural checks in `tests/test_stage2_attempts.py`. Add any necessary regression coverage in existing `tests/test_stage2.py` and `tests/test_close_merged_beads.py`.
3. Orchestrator after the accepted attempt: update held `AGENTS.md` for the harness-neutral worktree exception; update `docs/WORKFLOW.md` sections 3 and 4 for location, entry and fallback; amend `plans/changes/stage2-session/spec.md` for the protected second entry. Carry the proposed `docs/adr/0026-isolated-attempts.md` in the decision pull request and regenerate `plans/INDEX.md` with `python3 scripts/plans_registry.py` if required. Do not edit held paths in an attempt.
4. First pull request: enable repair and review isolation; draft and implement use the same lifecycle with isolation disabled. Record one night's use and its commit. Second pull request: enable isolation for draft and implement; rerun verification. Do not change explore, research swarm, review-loop routing, endpoint declarations, credentials or unrelated refs.

Verification: `make verify`

## Criterion ledger

- 1: not yet written tests/test_stage2_attempts.py::test_criterion_1 — A covered verb starts its model outside the lifecycle.
- 2: not yet written tests/test_stage2_attempts.py::test_criterion_2 — The direct entry bypasses a protection enforced by the runner.
- 3: not yet written tests/test_stage2_attempts.py::test_criterion_3 — The attempt uses the lane checkout or a different base.
- 4: not yet written tests/test_stage2_attempts.py::test_criterion_4 — A failed attempt changes the lane or a later prompt input.
- 5: not yet written tests/test_stage2_attempts.py::test_criterion_5 — An attempt is created under the lane or a harness-specific directory.
- 6: not yet written tests/test_stage2_attempts.py::test_criterion_6 — An attempt is treated as a lane or contributes a record key.
- 7: not yet written tests/test_stage2_attempts.py::test_criterion_7 — A different session’s worktree is pruned.
- 8: not yet written tests/test_stage2_attempts.py::test_criterion_8 — A model starts without a dependency or the refusal omits its remedy.
- 9: not yet written tests/test_stage2_attempts.py::test_criterion_9 — An attempt writes through either shared link.
- 10: not yet written tests/test_stage2_attempts.py::test_criterion_10 — A changed environment is accepted or restoration is omitted.
- 11: not yet written tests/test_stage2_attempts.py::test_criterion_11 — Recovery follows a link into the shared lane environment.
- 12: not yet written tests/test_stage2_attempts.py::test_criterion_12 — A failed call stops despite another route, loses saved state, or omits the reason.
- 13: not yet written tests/test_stage2_attempts.py::test_criterion_13 — Another route starts after a leak refusal.
- 14: not yet written tests/test_stage2_attempts.py::test_criterion_14 — Another route starts after restoration refusal.
- 15: not yet written tests/test_stage2_attempts.py::test_criterion_15 — A completed attempt leaves a registered worktree or a failed state cannot be inspected.
- 16: not yet written tests/test_stage2_attempts.py::test_criterion_16 — A matching ref remains or an unrelated ref is deleted.
- 17: not yet written tests/test_stage2_attempts.py::test_criterion_17 — The commit lands only on the detached attempt or overwrites a moved lane.
- 18: not yet written tests/test_stage2_attempts.py::test_criterion_18 — A covered writing verb bypasses the lifecycle or the rollout is not staged.
- 19: not a test — inspect the second pull request and the recorded first-night evidence; missing evidence or either verb left unisolated refutes it.
- 20: not yet written tests/test_stage2_attempts.py::test_criterion_20 — Review writes in the lane or the review loop uses the writing fallback.
- 21: not a test — phase-6 review reads the doctrine against the spec; either obsolete rule refutes it.

## Time used

2026-11-24 13:24:28–13:28:39 UTC, 251 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
