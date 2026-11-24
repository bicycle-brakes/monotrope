---
title: "Spec — isolated-writing-attempts"
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
adr_files: [docs/adr/0026-isolated-writing-attempts.md]
neighbours: [plans/changes/archive/2026-11-06-fail-fast-attempts/spec.md, plans/changes/archive/2026-11-06-restore-symlink-parent/spec.md, plans/changes/loop-record-other-worktree/spec.md, plans/changes/stage2-session/spec.md]
---

# Spec — isolated-writing-attempts

Writing attempts run through a shared lifecycle that isolates their work from the lane (bead coding-harness-s9r). Research: `research.md`; decisions: `decisions.md`.

## Problem

At baseline 91d19b8a1604, failed attempts wrote into the lane and required manual cleanup; draft and the other writing verbs used different attempt paths (research runs of 2026-11-22 and 2026-11-23; decisions Q-1 and Q-6). A failed repair call stopped instead of advancing to the next route, and the existing environment digest covered Python but not Pi (research reconciliation, 2026-11-23; decisions Q-13 and Q-14).

## Terms

**Lane:** the change's persistent worktree and branch. **Attempt:** one model call and its resulting state. **Pinned commit:** the fixed input commit for that attempt.

## Acceptance criteria

1. When draft, implement or repair starts a model, the start passes through the shared attempt lifecycle.
   *Refuted by:* A writing verb starts its model outside that lifecycle.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-25`

2. When an isolated attempt starts, it receives a detached worktree at its pinned commit: the lane HEAD for the first attempt, the saved failed state for a fall-through, or the clean baseline after a checksum rejection.
   *Refuted by:* The attempt uses the lane checkout or a different base.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-10`, `decisions.md#Q-17`, `decisions.md#Q-24`

3. When an isolated attempt ends, the runner checks that the lane’s tracked and untracked files are unchanged except for runner-owned records, and rejects the attempt if they changed.
   *Refuted by:* An attempt changes a lane file outside runner-owned records and is accepted, or the change is not detected.
   *Basis:* `decisions.md#Q-2`, `decisions.md#Q-23`, `decisions.md#Q-24`

4. When an isolated attempt is created, its worktree is located beneath `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/`.
   *Refuted by:* An attempt is created under the lane or a harness-specific directory.
   *Basis:* `decisions.md#Q-11`

5. When worktrees are discovered or record keys scanned, attempt worktrees are excluded.
   *Refuted by:* An attempt is treated as a lane or contributes a record key.
   *Basis:* `decisions.md#Q-11`

6. When the runner creates an isolated attempt, it records an invocation identifier and a process-id lock.
   *Refuted by:* An isolated attempt has no identifier or process-id lock.
   *Basis:* `decisions.md#Q-19`, `decisions.md#Q-25`

7. When the runner starts, it prunes attempts with a recorded dead process and reports unlocked attempts without removing them.
   *Refuted by:* A live or unlocked attempt is removed, a dead attempt remains, or an unlocked attempt is not reported.
   *Basis:* `decisions.md#Q-19`, `decisions.md#Q-22`, `decisions.md#Q-25`

8. While an isolated attempt runs, file permissions make its linked lane environment and Pi read-only; checksums detect changes made despite those permissions.
   *Refuted by:* Ordinary writes succeed through either link, or tampering with a linked target goes undetected.
   *Basis:* `decisions.md#Q-13`, `decisions.md#Q-20`

9. When either shared environment checksum differs after an attempt, the runner rejects it, deletes and rebuilds .venv, reinstalls Pi with tools/pi/install.sh, and stops if either restored checksum still differs.
   *Refuted by:* A changed environment is accepted, a rebuild or reinstall is omitted, or an ineffective restoration continues.
   *Basis:* `decisions.md#Q-13`, `decisions.md#Q-20`

10. When recovery runs, it does not traverse an attempt’s environment link.
   *Refuted by:* Recovery follows a link into the shared lane environment.
   *Basis:* `decisions.md#Q-13`

11. When a writing model process fails by exit, time or usage limit, or empty answer, or its post-run checks are red, the next declared route, if one remains, starts from the saved state, or the clean baseline after an environment checksum rejection, in a new worktree when isolation is enabled, and the switch and reason are recorded in findings.
   *Refuted by:* A failed call stops despite another route, loses saved state, or omits the reason.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-14`, `decisions.md#Q-17`

12. When leak checking refuses a call, the run stops without fallback.
   *Refuted by:* Another route starts after a leak refusal.
   *Basis:* `decisions.md#Q-5`

13. When restoration is refused or ineffective, or an internal runner failure occurs such as a moved HEAD, checkpoint rollback or an unstartable verification, the whole run stops without fallback.
   *Refuted by:* Another route starts after a restoration refusal, ineffective restoration or internal runner failure.
   *Basis:* `decisions.md#Q-14`, `decisions.md#Q-17`, `decisions.md#Q-20`

14. When an isolated attempt ends, its worktree is removed and its failed state remains inspectable under the change’s attempt refs.
   *Refuted by:* A completed attempt leaves a registered worktree or a failed state cannot be inspected.
   *Basis:* `decisions.md#Q-12`

15. When an isolated attempt is accepted, its checkpoint lands on the unchanged lane HEAD; if the lane moved or the model committed in its worktree, the run rejects the attempt and stops without rebasing or cherry-picking.
   *Refuted by:* The checkpoint remains detached, overwrites a moved lane, or the run continues after a model commit.
   *Basis:* `decisions.md#Q-15`, `decisions.md#Q-21`

16. When verification and held-path put-back run for an isolated attempt, they operate in the attempt worktree; the runner writes its audit line in the lane only after the attempt worktree exists, and writes a failed attempt’s block and switch reason immediately after that attempt.
   *Refuted by:* A check runs against the lane, an audit line precedes creation, or a failed attempt’s block or switch reason is delayed or missing.
   *Basis:* `decisions.md#Q-20`, `decisions.md#Q-24`

17. When the lane has uncommitted or untracked changes other than runner-owned records, the runner refuses to start an attempt.
   *Refuted by:* An attempt starts with such changes present.
   *Basis:* `decisions.md#Q-24`

18. When runner-owned records are written in the lane, they travel in the next landing commit or the orchestrator’s records commit.
   *Refuted by:* Those records are omitted from both commits.
   *Basis:* `decisions.md#Q-20`, `decisions.md#Q-24`

19. When the first pull request lands, repair is isolated and draft and implement use the same lifecycle with isolation disabled.
   *Refuted by:* A writing verb bypasses the lifecycle or the first rollout isolates a different set.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-18`, `decisions.md#Q-25`

20. When the later rollout lands, draft and implement use isolated attempts.
   *Refuted by:* Either writing verb remains unisolated after that rollout.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-18`, `decisions.md#Q-25`

21. When the runner writes or reads attempt records, lock files or the saved-state index, each is code-written JSON validated against a schema.
   *Refuted by:* A malformed state record is accepted or a state file is not schema-validated JSON.
   *Basis:* `decisions.md#Q-25`

22. When the doctrine describes failed writing calls, it permits the declared fallback and retains the leak refusal stop.
   *Refuted by:* The doctrine still requires every failed writing call to stop or permits fallback after a leak refusal.
   *Basis:* `decisions.md#Q-8`, `decisions.md#Q-14`, `decisions.md#Q-25`

23. When an isolated attempt needs linked tools and the lane lacks its Python environment or pinned Pi installation, the runner refuses before the model call and names the setup remedy.
   *Refuted by:* A model starts without a required dependency or the refusal omits its remedy.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-18`

## Non-goals

Phase-6 review isolation, the lifecycle CLI for other harnesses, post-merge ref cleanup and the second-rollout evidence gate are separate follow-up changes (Q-25). Explore, the research swarm, spec-review and review-loop remain outside this lifecycle. Network isolation, blocking foreign reads, containers and micro-VMs remain later work. The lane is reachable through linked environment parents until a container layer; detection does not prevent this access.

## Protected areas

Credentials, endpoint declarations and unrelated refs remain untouched. Held paths are edited only by the orchestrator after the accepted attempt.

## Definition of Done

- `make verify` green; first and later rollout evidence recorded in their respective pull requests.
- `docs/WORKFLOW.md`, `AGENTS.md` and `docs/adr/0026-isolated-writing-attempts.md` move with the code; protected areas and non-goals remain untouched.
- The final pull request closes `coding-harness-s9r` and its last commit carries `Closes-Bead: coding-harness-s9r`.
- Special runs: none beyond the rollout evidence.

## Open decisions

[DETAIL] ADR 0026 is the next number in this checkout; renumber if another ADR lands first. This is reversible and Q-8 requires the next free number at merge.
