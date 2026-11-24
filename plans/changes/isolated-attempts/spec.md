---
title: "Spec — isolated-attempts"
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: plans/changes/isolated-writing-attempts/decisions.md
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, attempts]
class: architectural
adr_files: []
neighbours: [plans/changes/archive/2026-11-06-fail-fast-attempts/spec.md, plans/changes/archive/2026-11-06-restore-symlink-parent/spec.md, plans/changes/loop-record-other-worktree/spec.md, plans/changes/stage2-session/spec.md]
---

# Spec — isolated-attempts

Writing attempts and review run through a shared lifecycle that isolates their work from the lane (bead coding-harness-s9r). Research: `research.md`; decisions: `decisions.md`.

## Problem

At baseline 91d19b8a1604, failed attempts wrote into the lane and required manual cleanup; draft and the other writing verbs used different attempt paths (research runs of 2026-11-22 and 2026-11-23; decisions Q-1 and Q-6). A failed repair call stopped instead of advancing to the next route, and the existing environment digest covered Python but not Pi (research reconciliation, 2026-11-23; decisions Q-13 and Q-14).

## Terms

**Lane:** the change's persistent worktree and branch. **Attempt:** one model call and its resulting state. **Pinned commit:** the fixed input commit for that attempt.

## Acceptance criteria

1. When implement, repair, draft or phase-6 review starts a model, the start passes through the shared attempt lifecycle; spec-review and review-loop are exempt.
   *Refuted by:* A covered verb starts its model outside the lifecycle.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-9`, `decisions.md#Q-18`

2. When another harness uses the attempt command, it can create, checksum, save state, land, remove and prune attempts through the same lifecycle as the runner; it starts its own model and owns its model policy.
   *Refuted by:* The direct entry omits a lifecycle operation or starts a model.
   *Basis:* `decisions.md#Q-16`, `decisions.md#Q-19`

3. When an isolated attempt starts, it receives a detached worktree at its pinned commit: the lane HEAD for the first attempt, the saved failed state for a fall-through, or the clean baseline after a checksum rejection.
   *Refuted by:* The attempt uses the lane checkout or a different base.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-10`, `decisions.md#Q-17`, `decisions.md#Q-24`

4. When an isolated attempt ends, the runner checks that the lane’s tracked and untracked files are unchanged except for runner-owned records, and rejects the attempt if they changed.
   *Refuted by:* An attempt changes a lane file outside runner-owned records and is accepted, or the change is not detected.
   *Basis:* `decisions.md#Q-2`, `decisions.md#Q-23`, `decisions.md#Q-24`

5. When an isolated attempt is created, its worktree is located beneath the harness-neutral runner state directory.
   *Refuted by:* An attempt is created under the lane or a harness-specific directory.
   *Basis:* `decisions.md#Q-11`

6. When worktrees are discovered or record keys scanned, attempt worktrees are excluded.
   *Refuted by:* An attempt is treated as a lane or contributes a record key.
   *Basis:* `decisions.md#Q-11`

7. When any harness creates an attempt, its invocation receives an identifier and a process-id lock file; pruning removes worktrees whose recorded process no longer runs, preserves live ones, and list and prune report worktrees without a lock without removing them automatically.
   *Refuted by:* A harness creates an attempt without identity and lock, a dead invocation remains, a live or unlocked worktree is pruned, or an unlocked worktree is not reported.
   *Basis:* `decisions.md#Q-11`, `decisions.md#Q-19`, `decisions.md#Q-22`

8. When an isolated attempt needs linked tools and the lane lacks its Python environment or pinned Pi installation, the runner refuses before the model call and names the setup remedy; unisolated attempts do not acquire this requirement.
   *Refuted by:* A model starts without a dependency or the refusal omits its remedy.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-18`

9. While an isolated attempt runs, file permissions make its linked lane environment and Pi read-only; checksums detect changes made despite those permissions.
   *Refuted by:* Ordinary writes succeed through either link, or tampering with a linked target goes undetected.
   *Basis:* `decisions.md#Q-13`, `decisions.md#Q-20`

10. When either shared environment checksum differs after an attempt, the runner rejects it, deletes and rebuilds .venv, reinstalls Pi with tools/pi/install.sh, and stops if either restored checksum still differs.
   *Refuted by:* A changed environment is accepted, a rebuild or reinstall is omitted, or an ineffective restoration continues.
   *Basis:* `decisions.md#Q-13`, `decisions.md#Q-20`

11. When recovery runs, it does not traverse an attempt’s environment link.
   *Refuted by:* Recovery follows a link into the shared lane environment.
   *Basis:* `decisions.md#Q-13`

12. When a writing model process fails by exit, time or usage limit, or empty answer, or its post-run checks are red, the next declared route, if one remains, starts from the saved state, in a new worktree when isolation is enabled, and the switch and reason are recorded in findings.
   *Refuted by:* A failed call stops despite another route, loses saved state, or omits the reason.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-14`, `decisions.md#Q-17`

13. When leak checking refuses a call, the run stops without fallback.
   *Refuted by:* Another route starts after a leak refusal.
   *Basis:* `decisions.md#Q-5`

14. When restoration is refused or ineffective, or an internal runner failure occurs such as a moved HEAD, checkpoint rollback or an unstartable verification, the whole run stops without fallback.
   *Refuted by:* Another route starts after a restoration refusal, ineffective restoration or internal runner failure.
   *Basis:* `decisions.md#Q-14`, `decisions.md#Q-17`, `decisions.md#Q-20`

15. When an isolated attempt ends, its worktree is removed and its failed state remains inspectable under the change’s attempt refs.
   *Refuted by:* A completed attempt leaves a registered worktree or a failed state cannot be inspected.
   *Basis:* `decisions.md#Q-12`

16. When the final pull request carrying Closes-Bead merges, post-merge cleanup deletes that change’s attempt refs locally and on origin; cleanup also removes refs for archived change folders.
   *Refuted by:* A matching ref remains or an unrelated ref is deleted.
   *Basis:* `decisions.md#Q-7`, `decisions.md#Q-12`, `decisions.md#Q-21`

17. When an isolated attempt is accepted, its checkpoint lands on the unchanged lane HEAD; if the lane moved or the model committed in its worktree, the run rejects the attempt and stops without rebasing or cherry-picking.
   *Refuted by:* The checkpoint remains detached, overwrites a moved lane, or the run continues after a model commit.
   *Basis:* `decisions.md#Q-15`, `decisions.md#Q-21`

18. When the first pull request lands, repair is isolated and implement and draft use the same lifecycle with isolation disabled; phase-6 review enters in the second pull request.
   *Refuted by:* A covered writing verb bypasses the lifecycle or the rollout is not staged.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-18`

19. When one night after the first pull request shows at least three isolated repair runs without lane damage or isolation-caused failure, the second pull request enables isolation for draft, implement and phase-6 review; otherwise the run stops and reports to the maintainer.
   *Refuted by:* Fewer than three qualifying runs or an isolation-caused failure permits the second pull request, or a covered verb remains unisolated in it.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-18`

20. When phase-6 review runs through the lifecycle in the second rollout, it is isolated without changing spec-review or review-loop routing.
   *Refuted by:* Review writes in the lane or the review loop uses the writing fallback.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-14`, `decisions.md#Q-18`

21. When the doctrine is updated, it permits the protected attempt entry and the declared failed-call fallback while preserving leak refusals.
   *Refuted by:* The old sole-entry or unconditional failed-call stop rule remains.
   *Basis:* `decisions.md#Q-8`, `decisions.md#Q-16`, `decisions.md#Q-19`

22. When verification and held-path put-back run for an isolated attempt, they operate in the attempt worktree; the runner writes its audit line in the lane only after the attempt worktree exists, and writes a failed attempt’s block and switch reason immediately after that attempt.
   *Refuted by:* A check runs against the lane, an audit line precedes creation, or a failed attempt’s block or switch reason is delayed or missing.
   *Basis:* `decisions.md#Q-20`, `decisions.md#Q-24`

23. When the lane has uncommitted or untracked changes other than runner-owned records, the runner refuses to start an attempt.
   *Refuted by:* An attempt starts with such changes present.
   *Basis:* `decisions.md#Q-24`

24. When runner-owned records are written in the lane, they travel in the next landing commit or the orchestrator’s records commit.
   *Refuted by:* Those records are omitted from both commits.
   *Basis:* `decisions.md#Q-20`, `decisions.md#Q-24`

## Non-goals

Network isolation, blocking foreign reads, containers and micro-VMs are later work. The lane remains reachable through parents of linked environments until the container layer; the lane check detects changes rather than preventing them. Explore, the research swarm, spec-review and review-loop remain outside the lifecycle; their routing is unchanged. The second rollout waits for one night of first-stage use.

## Protected areas

Credentials, endpoint declarations and unrelated change refs remain untouched. Held paths are edited by the orchestrator, not an implementation attempt.

## Definition of Done

- `make verify` green; the two pull requests provide the staged rollout and the first night’s evidence of at least three isolated repair runs without lane damage or isolation-caused failure.
- `docs/WORKFLOW.md`, `AGENTS.md`, `plans/changes/stage2-session/spec.md` and `docs/adr/0026-isolated-attempts.md` move with the corresponding code; protected areas and non-goals remain untouched.
- The final pull request closes bead `coding-harness-s9r` and its last commit carries `Closes-Bead: coding-harness-s9r`.
- Special run: one night after the first pull request, with the tested commit recorded.

## Open decisions

[DETAIL] Number the proposed ADR 0026, the next number in this checkout; renumber if another ADR lands first. This is reversible and Q-8 explicitly requires the next free number at merge.
