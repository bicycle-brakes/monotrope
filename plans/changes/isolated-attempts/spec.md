---
title: "Spec — isolated-attempts"
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
tags: [spec, stage-2, attempts]
class: architectural
adr_files: [docs/adr/0026-isolated-attempts.md]
neighbours: [plans/changes/archive/2026-11-06-fail-fast-attempts/spec.md, plans/changes/archive/2026-11-06-restore-symlink-parent/spec.md, plans/changes/loop-record-other-worktree/spec.md, plans/changes/stage2-session/spec.md]
---

# Spec — isolated-attempts

Writing attempts and review run through a shared lifecycle that isolates their work from the lane (bead coding-harness-s9r). Research: `research.md`; decisions: `decisions.md`.

## Problem

At baseline 91d19b8a1604, failed attempts wrote into the lane and required manual cleanup; draft and the other writing verbs used different attempt paths (research runs of 2026-11-22 and 2026-11-23; decisions Q-1 and Q-6). A failed repair call stopped instead of advancing to the next route, and the existing environment digest covered Python but not Pi (research reconciliation, 2026-11-23; decisions Q-13 and Q-14).

## Terms

**Lane:** the change's persistent worktree and branch. **Attempt:** one model call and its resulting state. **Pinned commit:** the fixed input commit for that attempt.

## Acceptance criteria

1. When implement, repair, draft or review starts a model, the start passes through the shared attempt lifecycle.
   *Refuted by:* A covered verb starts its model outside the lifecycle.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-9`

2. When another harness uses the attempt command, it receives the same protections as a runner invocation.
   *Refuted by:* The direct entry bypasses a protection enforced by the runner.
   *Basis:* `decisions.md#Q-16`

3. When an isolated attempt starts, it receives a detached worktree at the pinned commit.
   *Refuted by:* The attempt uses the lane checkout or a different base.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-10`

4. When an isolated attempt changes its own files, the lane and subsequent runner prompt inputs remain unchanged until an accepted result is applied.
   *Refuted by:* A failed attempt changes the lane or a later prompt input.
   *Basis:* `decisions.md#Q-2`

5. When an attempt is created, its worktree is located beneath the harness-neutral runner state directory.
   *Refuted by:* An attempt is created under the lane or a harness-specific directory.
   *Basis:* `decisions.md#Q-11`

6. When worktrees are discovered or record keys scanned, attempt worktrees are excluded.
   *Refuted by:* An attempt is treated as a lane or contributes a record key.
   *Basis:* `decisions.md#Q-11`

7. When orphan attempts are pruned, only worktrees bearing the current session identifier are removed.
   *Refuted by:* A different session’s worktree is pruned.
   *Basis:* `decisions.md#Q-11`

8. When a lane lacks its Python environment or pinned Pi installation, the runner refuses before the model call and names the setup remedy.
   *Refuted by:* A model starts without a dependency or the refusal omits its remedy.
   *Basis:* `decisions.md#Q-3`

9. While an isolated attempt runs, its linked lane environment and Pi are read-only.
   *Refuted by:* An attempt writes through either shared link.
   *Basis:* `decisions.md#Q-13`

10. When either shared environment checksum differs after an attempt, the runner rejects that attempt and restores the environment with make venv.
   *Refuted by:* A changed environment is accepted or restoration is omitted.
   *Basis:* `decisions.md#Q-13`

11. When recovery runs, it does not traverse an attempt’s environment link.
   *Refuted by:* Recovery follows a link into the shared lane environment.
   *Basis:* `decisions.md#Q-13`

12. When a writing model call fails, the next declared route starts from the saved attempt state and the switch and reason are recorded in findings.
   *Refuted by:* A failed call stops despite another route, loses saved state, or omits the reason.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-14`

13. When leak checking refuses a call, the run stops without fallback.
   *Refuted by:* Another route starts after a leak refusal.
   *Basis:* `decisions.md#Q-5`

14. When restoration is refused, the whole run stops without fallback.
   *Refuted by:* Another route starts after restoration refusal.
   *Basis:* `decisions.md#Q-14`

15. When an isolated attempt ends, its worktree is removed and its failed state remains inspectable under the change’s attempt refs.
   *Refuted by:* A completed attempt leaves a registered worktree or a failed state cannot be inspected.
   *Basis:* `decisions.md#Q-12`

16. When the change merges, post-merge cleanup deletes only that change’s attempt refs locally and on origin.
   *Refuted by:* A matching ref remains or an unrelated ref is deleted.
   *Basis:* `decisions.md#Q-7`, `decisions.md#Q-12`

17. When an isolated attempt is accepted, its checkpoint commit lands on the lane HEAD after checking the lane has not moved.
   *Refuted by:* The commit lands only on the detached attempt or overwrites a moved lane.
   *Basis:* `decisions.md#Q-15`

18. When the first pull request lands, repair is isolated and implement and draft use the same lifecycle with isolation disabled.
   *Refuted by:* A covered writing verb bypasses the lifecycle or the rollout is not staged.
   *Basis:* `decisions.md#Q-6`

19. When one night of use has passed after the first pull request, the second pull request enables isolation for draft and implement.
   *Refuted by:* Either writing verb remains unisolated after the second pull request.
   *Basis:* `decisions.md#Q-6`

20. When review runs through the lifecycle, it is isolated without changing the review loop’s routing.
   *Refuted by:* Review writes in the lane or the review loop uses the writing fallback.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-14`

21. When the doctrine is updated, it permits the protected attempt entry and the declared failed-call fallback while preserving leak refusals.
   *Refuted by:* The old sole-entry or unconditional failed-call stop rule remains.
   *Basis:* `decisions.md#Q-8`, `decisions.md#Q-16`

## Non-goals

Network isolation, blocking foreign reads, containers and micro-VMs are later work. Explore and the research swarm remain outside the lifecycle; the review loop's routing is unchanged. The second rollout waits for one night of first-stage use.

## Protected areas

Credentials, endpoint declarations and unrelated change refs remain untouched. Held paths are edited by the orchestrator, not an implementation attempt.

## Definition of Done

- `make verify` green; the two pull requests provide the staged rollout and the first night's evidence.
- `docs/WORKFLOW.md`, `AGENTS.md`, `plans/changes/stage2-session/spec.md` and `docs/adr/0026-isolated-attempts.md` move with the corresponding code; protected areas and non-goals remain untouched.
- The final pull request closes bead `coding-harness-s9r` and its last commit carries `Closes-Bead: coding-harness-s9r`.
- Special run: one night after the first pull request, with the tested commit recorded.

## Open decisions

[DETAIL] Number the proposed ADR 0026, the next number in this checkout; renumber if another ADR lands first. This is reversible and Q-8 explicitly requires the next free number at merge.
