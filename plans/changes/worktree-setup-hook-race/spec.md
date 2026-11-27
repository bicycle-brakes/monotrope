---
title: "Spec — worktree-setup-hook-race"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-1ba3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, worktree, tests]
class: bounded
appetite: 2
adr_files: []
---

# Spec — worktree-setup-hook-race

A trusted new worktree gets its setup budget after the trust check, and the two budget tests distinguish the outcomes they claim to exercise (bead `coding-harness-1ba3`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- At commit `4d46d54a`, the deadline is set before the trust check; whole-second arithmetic can exhaust a one-second budget before `make venv` starts (`research.md`, 2026-11-27).
- At that commit, the not-started test accepts a timeout instead of proving its named path, and the timeout test also accepts a not-started message (`research.md`, 2026-11-27). The reported CI failure itself is not available in the tree.

## Acceptance criteria

1. When a trusted automatic setup starts, time spent checking trust does not consume the setup-step budget.
   *Refuted by:* A controlled clock advances past the budget during a successful trust check and the first setup step is reported as not started.
2. When a completed `make venv` consumes the setup budget, the next step is reported as not started and names `make venv` as the step that used it.
   *Refuted by:* The next step runs, or its failure line lacks either the not-started report or the name of the preceding step.
3. When `make venv` exceeds the setup budget, the failure reports that `make venv` timed out at the configured limit.
   *Refuted by:* The test accepts a not-started report, a missing timeout or an incorrect limit.
4. When the setup budget expires, later setup steps do not run.
   *Refuted by:* An install, import or version check is recorded after the budget is spent.
5. While setup runs, the managed Beads integration block remains unchanged.
   *Refuted by:* Its contents differ from the block on `origin/main`.

## Non-goals

Sub-second clock dependencies, changes to trust policy, the managed Beads integration, and a general redesign of timeout enforcement are outside this change.

## Protected areas

The Beads-managed block in `.beads/hooks/post-checkout` is managed externally and must remain untouched.

## Definition of Done

- `make verify` green; the targeted hook tests pass.
- Documents changed with the code: this spec and `plan.md`; no models or ADRs.
- The protected block is unchanged and non-goals are unbuilt, shown by the pull request's file list.
- The pull request closes the work item for the hook timeout race (bead `coding-harness-1ba3`), and its last commit carries `Closes-Bead: coding-harness-1ba3`.
- Special runs: none.

## Open decisions

[DETAIL] Use a controlled clock for the spent-budget path and a two-second budget for the real timeout test; these revisable test choices make the distinct paths observable without depending on a wall-clock boundary.
