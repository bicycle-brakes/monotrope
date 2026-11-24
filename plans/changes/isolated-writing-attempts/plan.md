---
title: "Plan — isolated-writing-attempts"
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

# Plan — isolated-writing-attempts

```text
For you:     Failed writing attempts are contained and declared fallback routes continue visibly.
Done when:   Lifecycle, isolation, JSON state and fallback tests pass with make verify.
Appetite:    24 hours of phase 4, including repairs; stop when spent.
Not now:     Review isolation, a lifecycle CLI, ref cleanup, the second-rollout gate and container isolation.
Pre-mortem:  suppose it failed: most likely because shared state lets an attempt alter the lane despite its separate worktree.
Starts unless you say stop.
```

## Files and steps

1. Implementer: create `scripts/stage2_attempts.py` around `run_attempts`, receiving the runner module and attempt Context; adapt `scripts/stage2.py` so draft, implement and repair all use it, with repair isolated in PR 1 and draft and implement isolated in PR 2. Preserve leak checks; after time or usage limits route to a different endpoint, including automatic Sonnet for implement and revised repair preconditions. When isolation is off retain records, locks, checksums, lane checking and saved-state fallback.
2. Implementer: store schema-validated JSON records, process-id/start-time locks and attempt-to-ref/base index alongside detached worktrees beneath `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/`. Commit runner-owned `findings.md` and `plan.md` before every attempt; refuse other porcelain changes. After the cleanliness check apply saved tracked and untracked changes, modes and symlinks as uncommitted state on lane HEAD, excluding environment links; in non-isolated mode save the failed state and restore the pinned lane before that check; after checksum rejection retain the rejected attempt's starting state. Save crashed trees before pruning, identify owners by id and start time, report unlocked attempts, retain answers and diagnostics in the lane Git directory, and remove finished worktrees. Change `scripts/stage2_research_store.py` and `scripts/stage2.py` to exclude attempts from discovery and loop-record scans.
3. Implementer: link both lane environments, protect their real directories and checksum installed package versions and Pi version. Restore permissions on every exit and after a crash; on mismatch rebuild with `make venv` and `bash tools/pi/install.sh`, comparing to the pre-attempt versions without traversing links. Compare the pre-attempt lane snapshot before runner writes or landing; on changes name paths and stop without reverting. Fingerprint shared Git hooks, config and the change's attempt refs; stop on changes. Verify and restore held paths in the attempt; land one checkpoint on unchanged lane HEAD, stop on model commits or internal failures. Report uncommitted records on the final line when a run ends without a records or landing commit.
4. Implementer: create `tests/test_stage2_attempts.py` for the criterion ledger; adapt `tests/test_stage2.py` and `tests/test_stage2_research_store.py` for routing, structural coverage and discovery. Tests use temporary repositories and fake model calls; no live model is needed.
5. Orchestrator after the accepted attempt: edit held `AGENTS.md` for the neutral worktree exception and writing fallback; update `docs/WORKFLOW.md` sections 3 and 4 for that exception, saved-state fallback and leak refusal. Carry `docs/adr/0026-isolated-writing-attempts.md` in the decision pull request, partially superseding ADR 0016 decision 4 and ADR 0017 decision 2. Update `docs/architecture/2026-09-17-omnigent-first-target.md` and `scripts/check_decision_continuity.py` if required by the amendment gate; regenerate `plans/INDEX.md` with `python3 scripts/plans_registry.py` if needed. Record findings and time in `plans/changes/isolated-writing-attempts/findings.md` and `plans/changes/isolated-writing-attempts/plan.md`.
6. Before PR 2, the orchestrator checks and records one night with at least three isolated repairs and no lane damage or isolation-caused failure. PR 1 needs no such evidence; if the night fails, stop and report instead of switching draft and implement.

Do not change endpoint declarations, credentials, network or foreign-read policy, review routing, post-merge ref cleanup, the external lifecycle CLI or the automated rollout gate. Phase-6 review isolation is a follow-up.

Verification: `make verify`

## Criterion ledger

- 1: not yet written tests/test_stage2_attempts.py::test_criterion_1 — a writing verb starts a model outside the shared lifecycle
- 2: not yet written tests/test_stage2_attempts.py::test_criterion_2 — fallback uses an intermediate HEAD or loses the prior saved tree
- 3: not yet written tests/test_stage2_attempts.py::test_criterion_3 — a lane change is missed, reverted or does not stop the run
- 4: not yet written tests/test_stage2_attempts.py::test_criterion_4 — a worktree appears outside the attempts state directory
- 5: not yet written tests/test_stage2_attempts.py::test_criterion_5 — an attempt appears as a lane or contributes a loop-record key
- 6: not yet written tests/test_stage2_attempts.py::test_criterion_6 — a lock lacks the process identity or invocation record
- 7: not yet written tests/test_stage2_attempts.py::test_criterion_7 — a dead tree is lost, a reused PID is treated as the owner, or an unlocked worktree is removed
- 8: not yet written tests/test_stage2_attempts.py::test_criterion_8 — an environment is not linked or protected, or changed recorded versions are missed
- 9: not yet written tests/test_stage2_attempts.py::test_criterion_9 — a rebuild is omitted or compared against a new baseline
- 10: not yet written tests/test_stage2_attempts.py::test_criterion_10 — recovery follows an attempt environment link
- 11: not yet written tests/test_stage2_attempts.py::test_criterion_11 — an eligible fallback loses its saved state or its switch reason
- 12: not yet written tests/test_stage2_attempts.py::test_criterion_12 — a model starts after a leak refusal
- 13: not yet written tests/test_stage2_attempts.py::test_criterion_13 — an unstartable verification or other internal failure falls through
- 14: not yet written tests/test_stage2_attempts.py::test_criterion_14 — saved state loses a tracked or untracked change, mode or symlink, or includes an environment link
- 15: not yet written tests/test_stage2_attempts.py::test_criterion_15 — landing creates multiple commits, overwrites a moved lane, or accepts a model commit
- 16: not yet written tests/test_stage2_attempts.py::test_criterion_16 — verification uses the lane or records are missing or mistimed
- 17: not yet written tests/test_stage2_attempts.py::test_criterion_17 — an attempt starts with a non-record porcelain change
- 18: not yet written tests/test_stage2_attempts.py::test_criterion_18 — pending runner records are absent from the next pinned base
- 19: not yet written tests/test_stage2_attempts.py::test_criterion_19 — a writing verb bypasses the lifecycle or non-isolated mode drops required checks
- 20: not a test — phase-6 review checks the second rollout proceeds without the required repair-night evidence
- 21: not yet written tests/test_stage2_attempts.py::test_criterion_21 — malformed or incomplete JSON state is accepted or stored inside a worktree
- 22: not a test — phase-6 review checks a named doctrine passage contradicts saved-state fallback or the leak stop
- 23: not yet written tests/test_stage2_attempts.py::test_criterion_23 — an isolated model starts without both tools or without a setup remedy
- 24: not yet written tests/test_stage2_attempts.py::test_criterion_24 — a limit retries the same endpoint or blocks the automatic next route
- 25: not yet written tests/test_stage2_attempts.py::test_criterion_25 — either environment remains read-only after an attempt
- 26: not yet written tests/test_stage2_attempts.py::test_criterion_26 — answer or diagnostics disappear with the attempt worktree
- 27: not yet written tests/test_stage2_attempts.py::test_criterion_27 — the last output line fails to name an uncommitted record
- 28: not yet written tests/test_stage2_attempts.py::test_criterion_28 — a changed shared Git hook, config or attempt ref is missed or lands

## Time used

2026-11-24 17:39:33–17:41:10 UTC, 97 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 19:24:43–19:28:06 UTC, 203 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
