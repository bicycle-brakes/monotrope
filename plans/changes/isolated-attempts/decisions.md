---
title: "Decisions — isolated-attempts"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-24
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
superseded_by: Q-11 (2026-11-24: the location moves to the runner state directory; the harness-neutral definition stays)
answer: 'A — under $TMPDIR/coding-harness-attempts/<change>/<attempt>, registered git worktrees, removed after the attempt, orphans pruned at the next start. The maintainer added: "es müssen sich andere harnesses darauf zugreifen können bzw. es umsetzen können" — location, naming, lifecycle and the side-ref rule are defined harness-neutrally (runner code plus docs/WORKFLOW.md and AGENTS.md), so Codex, Pi or any other harness can find the attempt worktrees and follow or implement the same procedure.'
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
answer: 'A — implement the 2026-10-16 decision: a failed model call (error, time or usage limit) counts as a failed attempt and falls through to the next route, building on its saved state; the switch and its reason stand visibly in findings.md; the doctrine sentence in docs/WORKFLOW.md §3 is amended with an ADR addendum. A leak refusal still never falls back.'
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
answer: 'A — one change, two pull requests: PR 1 the shared attempt lifecycle, isolation switched on for repair; PR 2 switches it on for draft and implement after one night of use. Checked, at the maintainer''s request, against modularisation and centralisation (AGENTS.md rule 9, bead coding-harness-vg9): the lifecycle lives in one new module scripts/stage2_attempts.py, the single choke point all three verbs call from PR 1 on; isolation is a declared per-verb parameter, so no second attempt path stands beside it at any time; the module has its own command-line entry for other harnesses; a check goes red when a writing verb starts a model outside it.'
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
answer: '"nach dem Merge" — after a change merges, the clean-up after merge (bead coding-harness-kpaq) deletes that change''s refs under refs/stage2/attempts/<change>/, locally and on origin (asked 2026-11-03 under coding-harness-c99h, which this bead absorbed on 2026-11-12).'
answered_by: maintainer
status: answered
context: |
  Topic: retention of side refs of stopped attempts.
  Intention: the refs grow without bound (11 on origin, measured 2026-11-03).
  Today: nothing deletes them.
  Repository change: Options: delete after the merge; keep 14 days; keep forever.
  Architecture change: none.

In the context of side refs that keep stopped attempts, facing unbounded growth or a retention rule, we decided that a change's attempt refs are deleted after its merge, locally and on origin, accepting that a stopped attempt of a merged change can no longer be inspected. — 2026-11-03

## Interview of 2026-11-24

The research handoff of run 0ef63f34 (89 items) was put to the maintainer in session c820a13d on 2026-11-24, grouped into eight questions with recommendations and two follow-ups; the answers below are the maintainer's.

## Q-8 · ADR instrument and doctrine sentences

asked: 2026-11-24
answer: "A — a new ADR (the next free number at merge) that partially supersedes ADR 0017 decision 2; it amends the docs/WORKFLOW.md §4 sentences \"The runner is the only way\" and \"a failed call stops\"; decision PR, the maintainer merges. Option B was an addendum to ADR 0017."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-3
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-16
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-20
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-22
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-23
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-27
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-28
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-29
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-35
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-36
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-39
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-49
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-52
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-53
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-55
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-56
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-85
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-88
context: |
  Topic: the decision record for isolated attempts.
  Intention: a clear record of what changes against ADR 0017.
  Today: ADR 0017 decision 2 and WORKFLOW §4 state the runner as the only way and a failed call as a stop.
  Repository change: Options: A new ADR; B addendum to ADR 0017.
  Architecture change: ADR 0017 decision 2 partially superseded.

In the context of attempt isolation, facing an addendum or a new record, we decided on a new ADR that partially supersedes ADR 0017 decision 2, to achieve one decision per record, accepting one more ADR. — 2026-11-24

## Q-9 · Which verbs run through the attempt module

asked: 2026-11-24
answer: "C — the writing verbs implement, repair and draft, plus review; explore and the research swarm stay outside. Options with their pros and cons were put: A writing verbs only (the observed damage, smallest change); B every model start (one rule without exceptions, but a worktree per read call and the research seats would have to move); C writing verbs plus review (review is a single call on finished code, cheap to isolate). Follow-up answer: the check that none of these verbs starts a model outside the module is an ordinary structural test under tests/ over scripts/stage2.py, run in make verify, not a decisions/gates.yaml entry."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-1
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-4
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-15
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-30
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-32
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-37
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-41
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-48
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-57
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-59
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-62
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-66
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-77
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-82
context: |
  Topic: the scope of the attempt module and of its red check.
  Intention: failed writes no longer damage the lane; review is cheap to include.
  Today: each verb starts its model inside scripts/stage2.py.
  Repository change: implement, repair, draft and review call the module; a structural test in tests/.
  Architecture change: one attempt path for four verbs.

In the context of which runner verbs start a model in an isolated attempt, facing the observed damage and the cost of isolating read steps, we decided on the writing verbs plus review, checked by an ordinary test, to achieve protection where code is written or reviewed, accepting that explore and the research swarm stay outside until the container layer. — 2026-11-24

## Q-10 · The isolation boundary

asked: 2026-11-24
answer: "A — one linked git worktree per attempt, detached HEAD at the pinned commit; local only; containers and micro-VMs stay a later layer (beads coding-harness-nevd, coding-harness-3gc6). Option B was a container now."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-5
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-6
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-7
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-8
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-9
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-11
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-12
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-13
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-74
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-75
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-76
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-79
context: |
  Topic: what isolates an attempt.
  Intention: seconds per attempt, no Linux VM on macOS.
  Today: attempts write in the lane worktree.
  Repository change: Options: A git worktree per attempt; B container now.
  Architecture change: none beyond Q-1.

In the context of isolating an attempt, facing a worktree or a container, we decided on a detached git worktree per attempt, to achieve cheap isolation now, accepting that network and foreign reads stay open until the container layer. — 2026-11-24

## Q-11 · Location of attempt worktrees

asked: 2026-11-24
answer: "Runner state directory — `$XDG_STATE_HOME/coding-harness/attempts/` (default `~/.local/state/coding-harness/attempts/`), where the runner already keeps its loop records. The maintainer required a place valid for all harnesses; `.claude/worktrees/` is Claude-specific and therefore out. Options put: the runner state directory; $TMPDIR (cleared on reboot); a neutral `.worktrees/attempts/` in the repository. Supersedes the $TMPDIR location of Q-4; AGENTS.md and WORKFLOW §3 get an explicit, harness-neutral exception; attempt worktrees are excluded from worktree discovery and record-key scans; orphan pruning removes only worktrees whose name carries this session's id."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-21
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-25
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-31
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-33
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-34
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-43
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-47
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-54
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-60
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-64
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-69
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-71
context: |
  Topic: where attempt worktrees live.
  Intention: one location every harness (Claude Code, Codex, Pi) can find and use.
  Today: Q-4 (2026-11-22) chose $TMPDIR; lane worktrees live under .claude/worktrees/.
  Repository change: runner code, AGENTS.md and docs/WORKFLOW.md §3.
  Architecture change: attempts live beside the runner's state, outside the repository.

In the context of attempt worktrees, facing a Claude-specific, a temporary or a state location, we decided on the runner's state directory, to achieve one harness-neutral place that survives a reboot for inspection, accepting that pruning is the runner's job. — 2026-11-24

## Q-12 · Lifecycle of a failed attempt

asked: 2026-11-24
answer: "A — the worktree is removed after the run; the attempt's state stays as a ref under refs/stage2/attempts/ for inspection; close_merged_beads deletes the refs after the lane merges, with a test (consistent with Q-7). Option B kept the worktree until the merge."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-10
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-50
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-58
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-61
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-70
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-73
context: |
  Topic: what remains of a failed attempt.
  Intention: inspectable without filling the disk.
  Today: Q-7 deletes a change's attempt refs after its merge.
  Repository change: worktree removal after each run; ref deletion in close_merged_beads.
  Architecture change: none.

In the context of failed attempts, facing kept worktrees or kept refs, we decided to remove the worktree and keep the ref until the merge, to achieve inspection at low cost, accepting that inspection goes through git. — 2026-11-24

## Q-13 · Linked .venv and Pi

asked: 2026-11-24
answer: "A — link the lane's .venv and the installed Pi read-only; checksum both before and after each attempt; a difference rejects the attempt and the runner restores with make venv; no recovery path traverses the link. Option B was an own copy per attempt."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-38
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-42
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-45
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-65
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-72
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-78
context: |
  Topic: the environment inside an attempt worktree.
  Intention: no reinstall per attempt, no damage to the shared environment.
  Today: tool_state digests .venv only; nothing digests the pinned Pi install.
  Repository change: checksums of .venv and Pi around each attempt.
  Architecture change: none.

In the context of the shared Python and Pi environment, facing a copy per attempt or a checked link, we decided on a read-only link with checksums, to achieve fast attempts, accepting a restore with make venv on a mismatch. — 2026-11-24

## Q-14 · Failed-call fall-through

asked: 2026-11-24
answer: "A — implement, repair and draft fall through to the next declared route on a failed call (draft's existing behaviour); the review loop is outside; RestorationRefused still stops the whole run. Option B kept the stop. Narrows Q-5 to the writing verbs."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-18
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-24
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-63
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-67
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-83
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-86
context: |
  Topic: what a failed model call does.
  Intention: night runs that do not stall.
  Today: only draft falls through (Codex, then GLM).
  Repository change: implement and repair gain draft's fall-through.
  Architecture change: the WORKFLOW §4 sentence (Q-8).

In the context of failed model calls, facing a stop or a fall-through, we decided that writing verbs fall through to the next route, to achieve progress without a hand start, accepting that a failure is answered by the next route. — 2026-11-24

## Q-15 · Class, module shape, landing order and research bookkeeping

asked: 2026-11-24
answer: "A — class architectural stands; the module wraps run_attempts and takes the runner module as an argument (the stage2_swarm pattern); an attempt gets its own Context root; the accepted checkpoint commit lands on the lane HEAD; loop-record-other-worktree merged with PR #428, so there is no order conflict; the disagreements H-80, H-81 and H-84 are settled by the direct reads cited in their claims; the model roster stays dated declarations in model-endpoints.yaml."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-2
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-14
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-17
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-19
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-26
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-40
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-44
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-46
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-51
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-68
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-80
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-81
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-84
context: |
  Topic: the remaining handoff items of run 0ef63f34.
  Intention: close the bookkeeping in one answer.
  Today: one complete research run; scripts/stage2.py is shared by many lanes.
  Repository change: new module scripts/stage2_attempts.py.
  Architecture change: none beyond Q-1 and Q-6.

In the context of the research bookkeeping, facing eighty-nine handoff items, we decided on the module shape and order above, to achieve a focused spec, accepting the readings of the cited claims. — 2026-11-24

## Q-16 · Own command line of the attempt module

asked: 2026-11-24
answer: "B — the module keeps its own command-line entry, as decided in Q-6 on 2026-11-22; in the maintainer's words: \"Ich möchte für alle modularisiering und übertragbarkeit auf harnesse\". The stage2-session rule that scripts/stage2.py is the only public entry is amended to cover model starts outside attempts; both entries carry the same protections. Options put: A no own CLI (stage2.py stays the only entry); B own CLI, stage2-session amended."
answered_by: maintainer
status: answered
research_items:
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-87
  - 0ef63f3420f9eafc7ee5fc9cd2adcdd0/H-89
research_neighbours: {keep: [plans/changes/stage2-session/spec.md], drop: [], add: []}
context: |
  Topic: the contradiction between Q-6 (own CLI) and stage2-session (one public entry).
  Intention: modular code that other harnesses can use directly.
  Today: plans/changes/stage2-session/spec.md names scripts/stage2.py as the sole public entry.
  Repository change: scripts/stage2_attempts.py gets a CLI; the stage2-session sentence is amended.
  Architecture change: a second protected entry point.

In the context of an attempt module other harnesses should use, facing one public entry or two, we decided on an own command line for the module, to achieve modularity and portability across harnesses, accepting a second entry that must carry the same protections. — 2026-11-24
