---
title: "Decisions — restore-symlink-parent"
status: draft
implementation_status: partial
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-10w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# restore-symlink-parent — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What the runner does when a restore path resolves outside the worktree

context: |
  Topic: the runner's restore of a failed attempt's inputs, when a parent
  directory inside the worktree was replaced by a symbolic link.
  Intention: a runner audit reproduced a write outside the worktree through
  such a link (bead coding-harness-10w).
  Today: the restore replaces the link with a directory and continues.
  Repository change: the restore refuses before writing; a test proves no
  outside write.
  Architecture change: none.
asked: 2026-10-22, conversation 2026-10-22 (joint window)
answer: "refuse and stop: write nothing, name the path, end the run without a fallback model, like a leak-check BLOCK"
answered_by: maintainer
status: answered

In the context of the runner's restore of a failed attempt, facing a parent
directory replaced by a symbolic link that resolves outside the worktree, we
decided that the runner refuses and stops without writing, names the path
and starts no fallback model, to achieve that no attempt can make the runner
write outside its worktree, accepting that such a run ends and needs the
maintainer. — 2026-10-22

## Q-2 · How recovery treats links the attempt placed in a parent chain

context: |
  Topic: rollback and restore of a failed attempt when parent chains hold
  symbolic links.
  Intention: three phase-6 reviews in a row (F6-1, F6-2, F6-4) found a new
  link chain that the batch preflight's simulation of recovery did not
  model, so the runner wrote before refusing.
  Today: the runner simulates the recovery and refuses only when a parent
  would resolve outside the worktree.
  Repository change: spec terms, criteria 1 and 6 and a non-goal of this
  change; code and tests in the same pull request.
  Architecture change: none.
asked: 2026-10-24, conversation 2026-10-24
answer: "1"
answered_by: maintainer
status: answered

The options put to the maintainer were: (1) strict — any link the attempt
created or changed in a destination's parent chain refuses the whole
recovery before any mutation, with no simulation; (2) refine the simulation
to the actual recovery order and keep reviewing; (3) check right before each
single mutation, which may refuse after an earlier mutation and contradicts
criterion 1.

In the context of recovery after a failed attempt, facing link
chains a simulation keeps missing, we decided that a changed alias ancestor
alone refuses the batch before its first mutation, to achieve that the whole
class closes instead of one chain per review, accepting that some harmless
runs end and need the maintainer. — 2026-10-24

## Q-3 · Any linked directory on a restored path refuses recovery

context: |
  Topic: recovery through a directory that is a symbolic link.
  Intention: the phase-6 re-check found two more link chains (F6-5, F6-6)
  after the Q-2 rule, the fourth and fifth of the same mechanism.
  Today: only a link the attempt created or changed refuses the batch.
  Repository change: the parent-chain check refuses any directory on a
  restored path that is a symbolic link at the baseline or now; leaf aliases
  stay as they are; spec terms, criteria 1 and 6 and a non-goal.
  Architecture change: none; the structural fix is bead coding-harness-s9r.
asked: 2026-10-27, conversation 2026-10-27
answer: "Strenge Regel (Empfohlen)"
answered_by: maintainer
status: answered

The option chosen, as put to the maintainer (translated): Codex rebuilds the
check so that any directory on the path that is a symbolic link refuses
before anything is written; F6-5 and F6-6 close with it. Consequence named
in the option: complete and simpler, and a linked directory in the worktree
then blocks every recovery.

In the context of recovery after a failed attempt, facing link chains that
each re-check extends, we decided that any parent link, changed or not,
refuses the batch before its first mutation, to achieve that the class
closes without modelling link targets, accepting that a linked directory in
the worktree blocks recovery. — 2026-10-27
