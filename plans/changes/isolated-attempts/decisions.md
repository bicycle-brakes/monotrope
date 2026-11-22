---
title: "Decisions — isolated-attempts"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, attempts, isolation]
---

# isolated-attempts — Decisions

Class: architectural (bead coding-harness-s9r; it changes how every writing verb of the runner runs a model and amends the doctrine sentence in `docs/WORKFLOW.md` §3). The interview ran in the conversation on 2026-11-22; the answers are recorded below with the options as they were put. Earlier decisions it builds on: the shared design of 2026-10-16 (beads coding-harness-6ie and coding-harness-s9r), the design of 2026-11-12 that folded coding-harness-c99h, -t3s3, -znc and -6ie into this bead, and the retention answer of 2026-11-03 (coding-harness-c99h Q-1).

## Q-1 · Direction: own worktree per attempt, or the three-way comparison

asked: 2026-11-22
answer: A — open the lane now on the 2026-11-12 design, without the three-way comparison of 2026-10-23; the orchestrator re-checks it against the alternatives.
answered_by: maintainer
status: answered
context: |
  Topic: how a writing attempt is isolated.
  Intention: a failed attempt leaves its changes in the lane worktree and the next step trips over them; on 2026-11-22 this happened three times (u1ha, ttic, i76l).
  Today: every attempt writes in the lane worktree.
  Repository change: Options: A open now on the 2026-11-12 design (own git worktree per attempt from the fixed base, failed attempt saved as a side ref, fallback builds on it); B after Monday in a block with the maintainer; C first compare worktree, container (Podman/Docker) and k3s/OpenShift.
  Architecture change: a new attempt lifecycle for all writing verbs.

In the context of writing attempts that damage the next one, facing a cheap per-attempt worktree or a heavier container or cluster, we decided to build the per-attempt worktree now, to achieve an end to the hand clean-up at the lowest cost, accepting that network access and foreign file reads are not covered by this change. — 2026-11-22

The orchestrator's re-check: the worktree covers the damage class (lane and runner inputs) at seconds per attempt; a container adds a network lock and blocks foreign reads but needs a Linux VM on macOS and stalled on 2026-10-15 (branch explore/isolated-attempts); k3s/OpenShift is heavier still. A container can later sit on top of the worktree (bead coding-harness-yw2p).

## Q-2 · Threat model

asked: 2026-11-22
answer: A — an attempt may damage its own worktree in any way (delete, edit, symlink, replace inputs); the lane and every file the runner reads its next prompt from stay untouched; network access and reading foreign files are out of scope, with their own bead (coding-harness-yw2p).
answered_by: maintainer
status: answered
context: |
  Topic: which model behaviour the runner must withstand.
  Intention: the spec states the threat model (bead).
  Today: no stated model; each repair closed one case (codex-repairs F-8, F-10..F-14).
  Repository change: Options: A lane and runner inputs only; B also block foreign file reads without a container; C container from the start.
  Architecture change: none beyond Q-1.

In the context of the threat model, facing a narrow or a wide scope, we decided to protect the lane and the runner's inputs only, to achieve a small change that can be built and checked in days, accepting that network and foreign reads wait for the container bead. — 2026-11-22

## Q-3 · Environment in the attempt worktree

asked: 2026-11-22
answer: A — the attempt worktree links the lane's .venv and installed Pi; a lane without them is refused before the model call with the remedy (make venv, tools/pi/install.sh); the runner checksums the shared environment before and after each attempt and rejects the attempt on a difference.
answered_by: maintainer
status: answered
context: |
  Topic: where an attempt worktree gets its Python environment and Pi.
  Intention: without the pinned Pi about 110 tests fail and an attempt goes red for an environment reason (0zhf attempts 2 and 3, 2026-11-22).
  Today: the lane worktree carries both.
  Repository change: Options: A link the lane's environment; B fresh install per attempt; C copy per attempt.
  Architecture change: none.

In the context of the attempt environment, facing links, fresh installs or copies, we decided to link the lane's environment with a before-and-after checksum, to achieve seconds per attempt and the same environment for every attempt, accepting that a changed environment rejects the attempt instead of being repaired. — 2026-11-22

## Q-4 · Where attempt worktrees live, and for whom

asked: 2026-11-22
answer: A — under $TMPDIR/coding-harness-attempts/<change>/<attempt>, registered git worktrees, removed after the attempt, orphans pruned at the next start. The maintainer added: "es müssen sich andere harnesses darauf zugreifen können bzw. es umsetzen können" — location, naming, lifecycle and the side-ref rule are defined harness-neutrally (runner code plus docs/WORKFLOW.md and AGENTS.md), so Codex, Pi or any other harness can find the attempt worktrees and follow or implement the same procedure.
answered_by: maintainer
status: answered
context: |
  Topic: the location of attempt worktrees.
  Intention: no tool mistakes them for a lane, a crash does not fill the disk, a model does not sit next to the lane.
  Today: none exist.
  Repository change: Options: A the system temporary directory; B inside the lane worktree; C the harness state directory.
  Architecture change: a harness-neutral attempt location.

In the context of attempt worktrees, facing the temporary directory, the lane or the state directory, we decided on the system temporary directory with a harness-neutral definition, to achieve no confusion with lanes and automatic clean-up after a reboot, accepting a path outside the repository. — 2026-11-22

## Q-5 · A failed model call

asked: 2026-11-22
answer: A — implement the 2026-10-16 decision: a failed model call (error, time or usage limit) counts as a failed attempt and falls through to the next route, building on its saved state; the switch and its reason stand visibly in findings.md; the doctrine sentence in docs/WORKFLOW.md §3 is amended with an ADR addendum. A leak refusal still never falls back.
answered_by: maintainer
status: answered
context: |
  Topic: what follows a model call that ends without an answer.
  Intention: on 2026-11-22 two u1ha repairs stopped at the Codex usage limit and Sonnet had to be started by hand.
  Today: the call stops; docs/WORKFLOW.md §3 says a failed model process stops instead of silently changing route.
  Repository change: Options: A fall through on every failed call except a leak refusal; B only for known causes; C keep stopping.
  Architecture change: the §3 doctrine sentence, with an ADR addendum.

In the context of failed model calls, facing a stop or a visible fall-through, we decided to fall through to the next route with the reason recorded, to achieve night runs that do not stall, accepting that an unknown failure is answered by the next route instead of a stop. — 2026-11-22

## Q-6 · Scope, order and structure

asked: 2026-11-22
answer: A — one change, two pull requests: PR 1 the shared attempt lifecycle, isolation switched on for repair; PR 2 switches it on for draft and implement after one night of use. Checked, at the maintainer's request, against modularisation and centralisation (AGENTS.md rule 9, bead coding-harness-vg9): the lifecycle lives in one new module scripts/stage2_attempts.py, the single choke point all three verbs call from PR 1 on; isolation is a declared per-verb parameter, so no second attempt path stands beside it at any time; the module has its own command-line entry for other harnesses; a check goes red when a writing verb starts a model outside it.
answered_by: maintainer
status: answered
context: |
  Topic: how much changes at once and where the code lives.
  Intention: scripts/stage2.py has 12,511 lines on origin/main (2026-11-22) and many lanes change it at once.
  Today: each verb runs its own attempt loop inside stage2.py.
  Repository change: Options: A one change, two PRs, repair first; B all three verbs in one PR; C repair only, the rest in a later bead.
  Architecture change: a new module as the one attempt path.

In the context of a large shared runner file, facing one big or two staged pull requests, we decided on one module as the single attempt path with isolation as a per-verb parameter switched on in two steps, to achieve a small first merge without a side route, accepting one night in which draft and implement run through the module without isolation. — 2026-11-22

## Q-7 · When side refs are deleted

asked: 2026-11-03
answer: "nach dem Merge" — after a change merges, the clean-up after merge (bead coding-harness-kpaq) deletes that change's refs under refs/stage2/attempts/<change>/, locally and on origin (asked 2026-11-03 under coding-harness-c99h, which this bead absorbed on 2026-11-12).
answered_by: maintainer
status: answered
context: |
  Topic: retention of side refs of stopped attempts.
  Intention: the refs grow without bound (11 on origin, measured 2026-11-03).
  Today: nothing deletes them.
  Repository change: Options: delete after the merge; keep 14 days; keep forever.
  Architecture change: none.

In the context of side refs that keep stopped attempts, facing unbounded growth or a retention rule, we decided that a change's attempt refs are deleted after its merge, locally and on origin, accepting that a stopped attempt of a merged change can no longer be inspected. — 2026-11-03
