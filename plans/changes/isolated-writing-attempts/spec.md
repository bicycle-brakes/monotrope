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

2. When an isolated attempt starts, it is detached at current lane HEAD after the records commit and only the previous failed state of the same invocation is applied as uncommitted changes by a three-way merge; a new invocation starts clean, and after a checksum rejection only the state taken over by the rejected attempt is applied.
   *Refuted by:* A fall-through uses an old base, imports another invocation’s work, loses inherited work, or retains the rejected attempt’s own changes.
   *Basis:* `decisions.md#Q-29`, `decisions.md#Q-34`

3. When an isolated attempt ends, the runner compares the lane against its pre-attempt snapshot before landing or writing that attempt’s records; a tracked or untracked change outside the whole files findings.md and plan.md stops the run, names changed paths and is not reverted.
   *Refuted by:* The runner misses a change, continues, reverts it, omits its path, or checks after landing or writing records.
   *Basis:* `decisions.md#Q-26`, `decisions.md#Q-27`

4. When an isolated attempt is created, its worktree is located beneath `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/<repository-id>/<lane-digest>/<invocation-id>/`.
   *Refuted by:* An attempt is created anywhere outside that directory.
   *Basis:* `decisions.md#Q-30`, `decisions.md#Q-39`

5. When worktrees are discovered or loop-record keys scanned, attempt worktrees are excluded.
   *Refuted by:* An attempt is treated as a lane or contributes a loop-record key.
   *Basis:* `decisions.md#Q-30`

6. When the runner creates an attempt, it records an invocation identifier and a lock containing the process id and start time in the attempts state directory.
   *Refuted by:* An attempt lacks its identifier, lock, process id, start time or state-directory record.
   *Basis:* `decisions.md#Q-30`, `decisions.md#Q-31`

7. When the runner starts, it restores permissions after a crash, saves a dead attempt’s tree under that invocation’s refs before pruning only its own repository’s attempts, and reports unlocked attempts without removing them; a process is dead when its id and start time no longer match a live process.
   *Refuted by:* A live or unlocked attempt is removed, a dead tree is lost, a reused process id prevents pruning, an unlocked attempt is not reported, or permissions remain unrestored.
   *Basis:* `decisions.md#Q-28`, `decisions.md#Q-29`, `decisions.md#Q-37`, `decisions.md#Q-39`, `decisions.md#Q-40`

8. While an isolated attempt runs, both the lane’s real Python environment and Pi directories are linked and every entry recursively made read-only; another invocation on that lane is refused while a live attempt holds them read-only; their reproducible installed package versions and Pi version are checksummed before and after the attempt.
   *Refuted by:* Either link or protection is absent, an ordinary write succeeds, or a change to the recorded versions is missed.
   *Basis:* `decisions.md#Q-28`, `decisions.md#Q-38`

9. When a shared environment checksum differs, the runner rejects the attempt, restores write permissions, deletes and rebuilds `.venv`, reinstalls Pi and compares the resulting package versions and Pi version to the pre-attempt checksum; an ineffective restoration stops the run.
   *Refuted by:* The changed environment is accepted, recovery is omitted, comparison uses timestamps or bytecode, or a still-different restoration continues.
   *Basis:* `decisions.md#Q-28`

10. When recovery runs, state saving, worktree removal, pruning, permission reversal, rebuild and reinstall reach real directories through recorded paths and never through an attempt’s environment link.
   *Refuted by:* Recovery follows a link into the shared lane environment.
   *Basis:* `decisions.md#Q-13`, `decisions.md#Q-42`

11. When a writing model fails by exit, time or usage limit, empty answer or a red or attempt-tree-unstartable post-run check, no work, answer-check rejection or checksum rejection, the next declared route starts from saved state if one remains, and the switch and reason are recorded in findings.
   *Refuted by:* A remaining eligible route does not start, loses its permitted starting state, or lacks a recorded reason.
   *Basis:* `decisions.md#Q-27`, `decisions.md#Q-29`, `decisions.md#Q-41`

12. When leak checking refuses a call, the run stops without fallback.
   *Refuted by:* Another route starts after a leak refusal.
   *Basis:* `decisions.md#Q-5`

13. When restoration is refused or ineffective, the lane changes, or an internal runner failure occurs including moved HEAD, checkpoint rollback, runner setup failure or a saved-state merge conflict, the whole run stops without fallback.
   *Refuted by:* A further route starts after any such failure, including a saved-state merge conflict; the saved state remains inspectable.
   *Basis:* `decisions.md#Q-27`, `decisions.md#Q-34`, `decisions.md#Q-41`

14. When an isolated attempt ends, its worktree is removed and its saved state remains inspectable under the change’s attempt refs, including tracked changes, untracked files, modes and symlinks but excluding the environment links.
   *Refuted by:* A completed worktree remains, saved state is lost or incomplete, or an environment link is saved.
   *Basis:* `decisions.md#Q-29`

15. When an isolated attempt is accepted, exactly one checkpoint commit whose parent is the unchanged lane HEAD lands on the lane; a moved lane or model commit rejects the attempt and stops without rebase or cherry-pick.
   *Refuted by:* The checkpoint has an intermediate parent, fails to land, overwrites a moved lane, or the run continues after a model commit.
   *Basis:* `decisions.md#Q-29`

16. When verification and held-path put-back run for an isolated attempt, they operate in the attempt worktree; the runner writes its audit line in the lane only after the attempt worktree exists, and writes a failed attempt’s block and switch reason immediately after that attempt.
   *Refuted by:* A check runs against the lane, an audit line precedes creation, or a failed attempt’s block or switch reason is delayed or missing.
   *Basis:* `decisions.md#Q-20`, `decisions.md#Q-24`

17. When the lane has changes listed by `git status --porcelain` other than the runner-owned whole files findings.md and plan.md at the pre-attempt cleanliness check, the runner refuses to start an attempt; saved fall-through state is applied only after that check.
   *Refuted by:* An attempt starts despite such a tracked or untracked change.
   *Basis:* `decisions.md#Q-26`

18. When the runner starts any attempt, it first commits pending runner-owned lane records in a records commit so the pinned lane is clean.
   *Refuted by:* An attempt starts with pending records uncommitted or without those records in its pinned tree.
   *Basis:* `decisions.md#Q-26`

19. When the first pull request lands, repair is isolated while draft and implement use the same lifecycle without a separate worktree, retaining invocation records, locks, lane checks, checksums and saved-state fall-through.
   *Refuted by:* A writing verb bypasses the lifecycle, repair is not isolated, or a non-isolated verb omits a required lifecycle operation; non-isolated verbs perform only the pre-attempt lane check and checksums, not the post-attempt lane comparison or read-only protection; after failure their tracked and new untracked state is saved and the pinned tracked state restored and new untracked files removed before the next attempt, including after checksum rejection, without removing ignored files.
   *Basis:* `decisions.md#Q-31`, `decisions.md#Q-35`

20. When draft and implement are isolated in the second pull request, the maintainer has first recorded in `decisions.md` a night check naming at least three repair runner invocations, each with at least one isolated attempt, with no lane damage or isolation-caused failure.
   *Refuted by:* Either verb remains unisolated in the second pull request or it proceeds without that evidence.
   *Basis:* `decisions.md#Q-31`, `decisions.md#Q-43`

21. When the runner reads or writes an attempt record, lock or saved-state index, it uses schema-validated JSON in the attempts state directory; the record contains invocation id, change, verb, route, pinned base, worktree path, repository root, lane worktree, real environment paths, process id and start time, and state, while the index maps each attempt to its saved ref and base.
   *Refuted by:* Malformed JSON or missing required fields is accepted, or state is stored inside a lane or attempt worktree.
   *Basis:* `decisions.md#Q-30`, `decisions.md#Q-38`, `decisions.md#Q-39`

22. When the doctrine describes writing-call failures, `docs/WORKFLOW.md` section 4 and `AGENTS.md` describe the declared saved-state fallback and leak-refusal stop, and the new ADR partially supersedes ADR 0017 decision 2 and ADR 0016 decision 4.
   *Refuted by:* Any named draft, implement or repair passage still requires baseline restoration or unconditional stop, or permits fallback after leak refusal, or either partial supersession is missing.
   *Basis:* `decisions.md#Q-32`

23. When an isolated attempt starts, it refuses before the model call if either the lane’s Python environment or pinned Pi is missing, including an installed Pi with a version different from the pin, and names the setup remedy.
   *Refuted by:* A model starts without either dependency or the refusal omits `make venv` or `tools/pi/install.sh` as applicable.
   *Basis:* `decisions.md#Q-28`, `decisions.md#Q-42`

24. When a time or usage limit ends a call, the next eligible route uses a different endpoint; implement uses one GLM Flash attempt then Sonnet 5.5 after any failure, while repair uses two Codex attempts then Sonnet 5.5 after any two failures, subject to that endpoint rule; usage limits match the endpoint-specific exit-status and message signatures in `model-endpoints.yaml`, and other failures are ordinary.
   *Refuted by:* The same endpoint is retried, implement lacks Sonnet, or repair's old preconditions block the different endpoint.
   *Basis:* `decisions.md#Q-27`, `decisions.md#Q-41`

25. When an attempt ends, the runner recursively adds the owner’s write bit to every entry of both real environment directories before recovery or return.
   *Refuted by:* A successful, failed or rejected attempt leaves either directory read-only.
   *Basis:* `decisions.md#Q-28`, `decisions.md#Q-38`

26. When the runner finishes an isolated attempt, its answer and diagnostics are stored by the runner in the lane's git directory and survive removal of the attempt worktree.
   *Refuted by:* An answer or diagnostic is absent after removal or is stored only in the attempt worktree.
   *Basis:* `decisions.md#Q-29`

27. When a run ends with runner-owned records outside a records or landing commit, its last output line names the uncommitted records.
   *Refuted by:* Such a run ends without naming each uncommitted record in its last output line.
   *Basis:* `decisions.md#Q-26`

28. When an isolated attempt ends, the runner compares fingerprints of shared Git hooks, config and this change's attempt refs to their pre-attempt values and stops before saving the ending state or landing on a difference, comparing only other invocation keys; refs include the lane digest and invocation id, and pruning saves only under the dead invocation’s own key.
   *Refuted by:* A changed hook, config or attempt ref goes undetected or landing proceeds after detection.
   *Basis:* `decisions.md#Q-33`, `decisions.md#Q-37`, `decisions.md#Q-39`

29. When an attempt ends, the runner compares the attempt record, lock, saved-state index and change loop record to its in-memory copies and stops on any difference; a changed or malformed lock counts as unlocked, is reported and is not removed.
   *Refuted by:* Tampering is missed, the run continues, or a changed or malformed lock is removed.
   *Basis:* `decisions.md#Q-40`

30. When an isolated attempt is accepted, its records are written before the checkpoint so the landing commit contains them and the lane is clean after a green run.
   *Refuted by:* Accepted records are omitted from the checkpoint or left uncommitted after a green run.
   *Basis:* `decisions.md#Q-36`

31. When the worktree doctrine is updated, `AGENTS.md` and `docs/WORKFLOW.md` both state the harness-neutral exception that attempt worktrees are detached under the state directory rather than under `.claude/worktrees`.
   *Refuted by:* Either document omits or contradicts the exception.
   *Basis:* `decisions.md#Q-43`

## Non-goals

Phase-6 review isolation, the lifecycle CLI for other harnesses, post-merge ref cleanup and the second-rollout evidence gate are separate follow-up changes (Q-25). Explore, the research swarm, spec-review and review-loop remain outside this lifecycle. Network isolation, blocking foreign reads, containers and micro-VMs remain later work. The lane is reachable through linked environment parents until a container layer; ignored lane files and tampering with the whole runner-owned files are outside the lane comparison. The checksums detect changes to recorded package and Pi versions, not arbitrary byte tampering.

## Protected areas

Credentials and unrelated refs remain untouched; endpoint declarations change only to add the usage-limit signatures required by criterion 24. Held paths are edited only by the orchestrator after the accepted attempt.

## Definition of Done

- `make verify` green; the first pull request needs no isolation evidence; the second records the manually checked night specified in criterion 20.
- `docs/WORKFLOW.md`, `AGENTS.md` and `docs/adr/0026-isolated-writing-attempts.md` move with the code; protected areas and non-goals remain untouched.
- The final pull request closes `coding-harness-s9r` and its last commit carries `Closes-Bead: coding-harness-s9r`.
- Special runs: one night of isolated repairs before the second rollout, as specified in criterion 20.

## Open decisions

[DETAIL] Saved fall-through state is applied after the cleanliness check, including in non-isolated mode, so the check does not reject the state it must resume.

[DETAIL] ADR 0026 is the next number in this checkout; renumber if another ADR lands first. This is reversible and Q-8 requires the next free number at merge.
