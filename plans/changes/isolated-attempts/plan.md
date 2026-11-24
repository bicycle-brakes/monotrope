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

1. Implementer: add `scripts/stage2_attempts.py`, wrapping `run_attempts` with an attempt-specific Context and a lifecycle CLI for create, checksum, save, land, remove and prune; the CLI starts no model. Route `scripts/stage2.py` implement, repair and draft through it from the first pull request, with only repair isolated; add phase-6 review in the second. Keep spec-review, review-loop, explore and research outside. Add a structural test for the covered starts and named exemptions.
2. Implementer: create detached worktrees under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/`; create invocation identity and process-id locks for every harness, prune dead invocations on start, report unlocked worktrees without removing them, and exclude attempt worktrees from lane discovery and record-key scans in `scripts/stage2.py` and `scripts/stage2_research_store.py` where applicable. Save failed states under `refs/stage2/attempts/<change>/`; remove finished worktrees. A retry starts from the saved state, in a new worktree if isolated, except after an environment mismatch, when it starts from the clean baseline. Failed model processes and red checks fall through; leak refusals and internal failures stop.
3. Implementer: link the lane's Python environment and pinned Pi only for isolated attempts, refuse missing dependencies with their setup commands, protect them with permissions and checksum both. On mismatch reject the attempt, delete and rebuild `.venv` with `make venv`, reinstall Pi with `tools/pi/install.sh`, compare both checksums again, and stop if restoration fails. Recovery must not traverse the links. Refuse a lane dirty beyond runner-owned records; pin lane HEAD, create the worktree before the audit line, check tracked and untracked lane files after every attempt and reject unexpected changes. Run verification and held-path put-back in the isolated attempt; write failed blocks and switch reasons immediately in the lane, and include runner records in the next landing or orchestrator records commit. Linked environment parents remain a known route to the lane until containers. Stop on a moved lane or an attempt-side model commit; land accepted checkpoints only on the unchanged lane.
4. Implementer: update `scripts/close_merged_beads.py` to delete only the change's local and origin attempt refs on the final `Closes-Bead` merge and to clean archived changes' refs. Add behavior and structural tests in `tests/test_stage2_attempts.py`, with regression tests in `tests/test_stage2.py` and `tests/test_close_merged_beads.py` as appropriate.
5. Orchestrator after the accepted attempt: update held `AGENTS.md`; update `docs/WORKFLOW.md` sections 3 and 4 and `plans/changes/stage2-session/spec.md`; align the already drafted `docs/adr/0026-isolated-attempts.md` with decisions Q-17 through Q-24 before the decision pull request. Regenerate `plans/INDEX.md` using `python3 scripts/plans_registry.py` if required. The implementation attempt does not edit held paths.
6. First pull request enables isolated repair. Record the commit and one night's evidence: at least three isolated repair runs without lane damage or isolation-caused failure. If that evidence is absent or bad, stop and report; otherwise a second pull request enables isolated draft, implement and phase-6 review. The final pull request carries `Closes-Bead: coding-harness-s9r`.

Do not change endpoint declarations, credentials, foreign-read or network access, containers, explore, research, spec-review or review-loop routing, or unrelated refs.

Verification: `make verify`

## Criterion ledger

- 1: not yet written tests/test_stage2_attempts.py::test_criterion_1 — A covered verb starts its model outside the lifecycle.
- 2: not yet written tests/test_stage2_attempts.py::test_criterion_2 — A lifecycle operation is missing or the entry starts a model.
- 3: not yet written tests/test_stage2_attempts.py::test_criterion_3 — The attempt uses the lane checkout or a different base.
- 4: not yet written tests/test_stage2_attempts.py::test_criterion_4 — A failed attempt changes the lane or a later prompt input.
- 5: not yet written tests/test_stage2_attempts.py::test_criterion_5 — An attempt is created under the lane or a harness-specific directory.
- 6: not yet written tests/test_stage2_attempts.py::test_criterion_6 — An attempt is treated as a lane or contributes a record key.
- 7: not yet written tests/test_stage2_attempts.py::test_criterion_7 — A harness lacks identity or lock, a dead invocation remains, a live or unlocked worktree is pruned, or an unlocked worktree is not reported.
- 8: not yet written tests/test_stage2_attempts.py::test_criterion_8 — A model starts without a dependency or the refusal omits its remedy.
- 9: not yet written tests/test_stage2_attempts.py::test_criterion_9 — An ordinary write succeeds or tampering goes undetected.
- 10: not yet written tests/test_stage2_attempts.py::test_criterion_10 — A changed environment is accepted or an incomplete restoration continues.
- 11: not yet written tests/test_stage2_attempts.py::test_criterion_11 — Recovery follows a link into the shared lane environment.
- 12: not yet written tests/test_stage2_attempts.py::test_criterion_12 — A failed call stops despite another route, loses saved state, or omits the reason.
- 13: not yet written tests/test_stage2_attempts.py::test_criterion_13 — Another route starts after a leak refusal.
- 14: not yet written tests/test_stage2_attempts.py::test_criterion_14 — Another route starts after restoration refusal.
- 15: not yet written tests/test_stage2_attempts.py::test_criterion_15 — A completed attempt leaves a registered worktree or a failed state cannot be inspected.
- 16: not yet written tests/test_stage2_attempts.py::test_criterion_16 — A matching ref remains or an unrelated ref is deleted.
- 17: not yet written tests/test_stage2_attempts.py::test_criterion_17 — The commit lands only on the detached attempt or overwrites a moved lane.
- 18: not yet written tests/test_stage2_attempts.py::test_criterion_18 — A covered writing verb bypasses the lifecycle or the rollout is not staged.
- 19: not a test — inspect the second pull request and the recorded first-night evidence; fewer than three qualifying runs, damage, isolation-caused failure, or a covered verb left unisolated refutes it.
- 20: not yet written tests/test_stage2_attempts.py::test_criterion_20 — Review writes in the lane or the review loop uses the writing fallback.
- 21: not a test — phase-6 review reads the doctrine against the spec; either obsolete rule refutes it.

- 22: not yet written tests/test_stage2_attempts.py::test_criterion_22 — checks run in the lane, the audit precedes creation, or failed records are delayed or missing.

- 23: not yet written tests/test_stage2_attempts.py::test_criterion_23 — an attempt starts with unrelated dirty or untracked lane files.
- 24: not yet written tests/test_stage2_attempts.py::test_criterion_24 — runner records are omitted from both landing and orchestrator records commits.

## Time used

2026-11-24 13:24:28–13:28:39 UTC, 251 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 13:51:25–13:55:26 UTC, 241 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 15:12:06–15:14:28 UTC, 142 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
