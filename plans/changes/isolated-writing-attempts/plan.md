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

1. Implementer: add `scripts/stage2_attempts.py` as the single lifecycle around `run_attempts`, receiving the runner module and attempt-specific Context; route draft, implement and repair through it in `scripts/stage2.py`, with isolation as a per-verb parameter. Repair is isolated in the first pull request; draft and implement are switched on in a later pull request. Preserve existing model policy and leak checking.
2. Implementer: in `scripts/stage2_attempts.py` create detached worktrees under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/`; persist schema-validated JSON attempt records, invocation locks and saved-state index; report unlocked attempts and prune dead owners only. Save failed state in `refs/stage2/attempts/<change>/`, remove completed worktrees, and start fallback from saved state except after environment mismatch, when the clean baseline is used. In `scripts/stage2.py` and `scripts/stage2_research_store.py`, exclude attempts from worktree discovery and record-key scans.
3. Implementer: refuse a dirty lane other than runner records, pin its HEAD and compare tracked and untracked files after each attempt. Protect linked `.venv` and Pi, checksum both, and on mismatch reject, rebuild `.venv` with `make venv`, reinstall Pi with `bash tools/pi/install.sh`, verify restoration and stop if ineffective; never recover through the attempt links. Run verification and held-path put-back in the attempt, write audit and failure records at the specified times, and land only on unchanged lane HEAD; stop on model commits or internal failures.
4. Implementer: add `tests/test_stage2_attempts.py` for the ledger, including structural coverage of each writing verb and exemptions, state-schema failures, process locks, fallback and worktree integration; adapt `tests/test_stage2.py` and `tests/test_stage2_research_store.py` for existing behavior and discovery.
5. Orchestrator after the accepted attempt: update held `AGENTS.md` and `docs/WORKFLOW.md` for the neutral worktree exception and writing-call fallback; Update `docs/architecture/2026-09-17-omnigent-first-target.md` and `scripts/check_decision_continuity.py` if ADR 0017 amends a numbered decision, and regenerate `plans/INDEX.md` with `python3 scripts/plans_registry.py` if needed. Record runner-owned findings and time in `plans/changes/isolated-writing-attempts/findings.md` and `plans/changes/isolated-writing-attempts/plan.md`. The attempt does not edit held paths.

Do not change endpoint declarations, credentials, network or foreign-read policy, review routing, ref cleanup or the follow-up rollout gate.

Verification: `make verify`

## Criterion ledger

- 1: not yet written tests/test_stage2_attempts.py::test_criterion_1 — A writing verb starts its model outside that lifecycle.
- 2: not yet written tests/test_stage2_attempts.py::test_criterion_2 — The attempt uses the lane checkout or a different base.
- 3: not yet written tests/test_stage2_attempts.py::test_criterion_3 — An attempt changes a lane file outside runner-owned records and is accepted, or the change is not detected.
- 4: not yet written tests/test_stage2_attempts.py::test_criterion_4 — An attempt is created under the lane or a harness-specific directory.
- 5: not yet written tests/test_stage2_attempts.py::test_criterion_5 — An attempt is treated as a lane or contributes a record key.
- 6: not yet written tests/test_stage2_attempts.py::test_criterion_6 — An isolated attempt has no identifier or process-id lock.
- 7: not yet written tests/test_stage2_attempts.py::test_criterion_7 — A live or unlocked attempt is removed, a dead attempt remains, or an unlocked attempt is not reported.
- 8: not yet written tests/test_stage2_attempts.py::test_criterion_8 — Ordinary writes succeed through either link, or tampering with a linked target goes undetected.
- 9: not yet written tests/test_stage2_attempts.py::test_criterion_9 — A changed environment is accepted, a rebuild or reinstall is omitted, or an ineffective restoration continues.
- 10: not yet written tests/test_stage2_attempts.py::test_criterion_10 — Recovery follows a link into the shared lane environment.
- 11: not yet written tests/test_stage2_attempts.py::test_criterion_11 — A failed call stops despite another route, loses saved state, or omits the reason.
- 12: not yet written tests/test_stage2_attempts.py::test_criterion_12 — Another route starts after a leak refusal.
- 13: not yet written tests/test_stage2_attempts.py::test_criterion_13 — Another route starts after a restoration refusal, ineffective restoration or internal runner failure.
- 14: not yet written tests/test_stage2_attempts.py::test_criterion_14 — A completed attempt leaves a registered worktree or a failed state cannot be inspected.
- 15: not yet written tests/test_stage2_attempts.py::test_criterion_15 — The checkpoint remains detached, overwrites a moved lane, or the run continues after a model commit.
- 16: not yet written tests/test_stage2_attempts.py::test_criterion_16 — A check runs against the lane, an audit line precedes creation, or a failed attempt’s block or switch reason is delayed or missing.
- 17: not yet written tests/test_stage2_attempts.py::test_criterion_17 — An attempt starts with such changes present.
- 18: not yet written tests/test_stage2_attempts.py::test_criterion_18 — Those records are omitted from both commits.
- 19: not yet written tests/test_stage2_attempts.py::test_criterion_19 — A writing verb bypasses the lifecycle or the first rollout isolates a different set.
- 20: not yet written tests/test_stage2_attempts.py::test_criterion_20 — Either writing verb remains unisolated after that rollout.
- 21: not yet written tests/test_stage2_attempts.py::test_criterion_21 — A malformed state record is accepted or a state file is not schema-validated JSON.
- 22: not a test — phase-6 review compares doctrine to the criterion; The doctrine still requires every failed writing call to stop or permits fallback after a leak refusal.

- 23: not yet written tests/test_stage2_attempts.py::test_criterion_23 — A model starts without a required dependency or the refusal omits its remedy.

## Time used

2026-11-24 17:39:33–17:41:10 UTC, 97 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
