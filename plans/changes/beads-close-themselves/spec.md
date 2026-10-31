---
title: "Spec — beads-close-themselves"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-l1if
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, beads, reconciliation]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — beads-close-themselves

Beads declared complete by a merged commit close at the next eligible session
start or own merge, without a remembered manual step (bead
`coding-harness-l1if`). Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

- The completion trailer and local `make close-merged ARGS=--write` command
  are promised, but neither the command nor its executor exists at base
  `9b9e9116` (2026-10-31; `research.md`, “What exists today”).
- Closure therefore depends on someone remembering it: the interview records
  nine merged beads closed manually on 2026-10-30 (`decisions.md#Q-1`).
- Existing artefact/tracker coupling reports drift; it does not execute a
  declared closure (`research.md`, “The enforcement that does exist”).

## Terms

**Completion declaration:** a Git-parsed commit trailer whose key is exactly
`Closes-Bead` and whose value is one bead identifier; repeated trailers may
name several beads. A mention in ordinary prose is not a declaration.

**Merged history:** all commits reachable from a freshly fetched `origin/main`,
including commits brought in through merge parents, irrespective of local HEAD.

**Tracker writer:** the session authorised by the existing one-writer rule;
this change grants no additional tracker or merge authority.

## Acceptance criteria

1. When the tracker writer runs the reconciler with `--write`, every existing
   non-closed bead declared in merged history is submitted for normal closure.
   *Refuted by:* an eligible bead remains unattempted after a successful run,
   including one declared in a merged side-branch commit or merged by a person.
   *Basis:* decisions.md#Q-1.

2. When a bead has no valid completion declaration in merged history, the
   reconciler leaves its state unchanged.
   *Refuted by:* an unmerged trailer, subject/body mention, PR prose, malformed
   trailer value or unrelated local-main commit causes a closure.
   *Basis:* decisions.md#Q-1; decisions.md, “Only the trailer counts”.

3. When declarations repeat or a declared bead is already closed, reconciliation
   makes at most one closure attempt per non-closed bead per run and never
   rewrites an already closed bead.
   *Refuted by:* duplicate attempts in a run or another close/reason change for
   the same bead on a subsequent successful run.
   *Basis:* decisions.md, “Idempotent and quiet”.

4. When a bead closes, its closure reason identifies the declaring commit and
   the PR number if that commit message explicitly identifies the PR.
   *Refuted by:* a missing/wrong commit identifier, missing explicit PR number,
   or a PR number invented from an unrelated number in the message.
   *Basis:* decisions.md, “Idempotent and quiet”.

5. When the reconciler runs without `--write`, it only reports eligible closures.
   *Refuted by:* any tracker mutation or `tools/bd dolt push` in reporting mode.
   *Basis:* research.md, existing command contract in `prompts/07-commit.md`.

6. If fresh main history or a complete current tracker render cannot be read,
   the reconciler reports failure without attempting any closure.
   *Refuted by:* a failed fetch, shallow history, missing ref or invalid/unreadable
   render produces a successful empty result or writes based on stale data.
   *Basis:* decisions.md#Q-1; research.md, tracker render contract.

7. If a declaration names an unknown bead or a normal closure is refused, the
   reconciler reports that unresolved item with a nonzero result without
   forcing the closure.
   *Refuted by:* silently dropping the item, creating it, overriding ownership
   with `--force`, or reporting complete success after refusal.
   *Basis:* research.md, “The rule of who closes”.

8. When an eligible write run finishes its closure attempts, it attempts
   `tools/bd dolt push` even if no new closure was needed.
   *Refuted by:* a partial batch is left unpublished, or a rerun after a failed
   push skips publication because the beads are already locally closed.
   *Basis:* decisions.md, “Only the tracker writer runs it”.

9. If publication fails, the reconciler reports that failure without claiming
   the local closures reached the remote tracker.
   *Refuted by:* a failed `dolt push` returns success or is described as published.
   *Basis:* decisions.md, “Only the tracker writer runs it”.

10. When an eligible first session starts, its repository start hook runs the
    writing reconciler to completion before emitting `tools/bd prime` context.
    *Refuted by:* prime starts first, reconciliation is only suggested in prose,
    or a reconciliation failure prevents the session from receiving prime
    context and a visible failure explanation.
    *Basis:* decisions.md#Q-1; decisions.md, “Only the tracker writer runs it”.

11. If startup detects another live session in the same repository, or cannot
    establish safe startup eligibility, its hook skips writing reconciliation.
    *Refuted by:* a second session in the same checkout or a sibling worktree,
    a child run, or an unreadable eligibility check invokes the writing command.
    *Basis:* decisions.md, “Only the tracker writer runs it”.

12. When an agent completes an authorised own merge, the merge procedure requires
    the tracker writer to reconcile after actual merge confirmation.
    *Refuted by:* queue admission is treated as merge completion, the procedure
    omits reconciliation, or a secondary writer is instructed to close beads.
    *Basis:* decisions.md#Q-1; research.md, closure after merge contract.

## Non-goals

No CI gate, GitHub Action, background service, GitHub merge automation, PR-body
closure parser, tracker migration, new writer-election/locking system, archive
automation, or changes to the existing drift timing. No adapter rollout beyond
the repository's Claude Code start hook; other harnesses retain the documented
local command. No kit/export rollout or installation into the maintainer's home.
Class remains bounded as interviewed; phase 2b and an ADR are not due.

## Protected areas

- `decisions/gates.yaml`, `.github/` and `scripts/ci_gates.py`: no CI closure work.
- `tools/bd`, tracker configuration, existing ADRs, `provenance.yaml`,
  `model-endpoints.yaml`, `.codex/`, `.agents/`, `AGENTS.md` and `templates/`:
  existing ownership, pinning, architecture and completion declaration stay.
- Other repositories and their trackers: no rollout or writes here.

## Definition of Done

- `make verify` green on the combined implementation and orchestrator edits.
- Moved in the same pull request: `prompts/07-commit.md` and
  `tools/claude-code/README.md`; no models or ADRs change.
- Protected areas untouched and non-goals unbuilt, checked against the PR file list.
- Bead: the pull request closes `coding-harness-l1if`, and its last commit carries
  the trailer `Closes-Bead: coding-harness-l1if` (`prompts/07-commit.md`).
- Special runs: isolated Git/tracker fixtures prove the ledger, with verification
  results and their commit recorded in the PR; no live tracker mutations in tests.

## Open decisions

None open. The following reversible details are chosen here with their reasons.

- [DETAIL] Keep the promised `make close-merged ARGS=--write` entry and a
  reporting default; this fulfils the existing command contract without
  making an exploratory invocation write.
- [DETAIL] Fetch main before reading, pin its resulting commit for the run,
  and scan its full reachable history without a cursor; this catches manual
  merges and retries without a second persistent truth.
- [DETAIL] Read current state through `scripts/bead_render.py`; write runs
  reject a preset `BEAD_RENDER` rather than mutating from a possibly stale
  snapshot. All writes use the pinned wrapper and no `--force`.
- [DETAIL] Report malformed/unknown declarations and per-bead refusals, continue
  independent valid closures, then publish and return nonzero if anything is
  unresolved; one bad declaration must not silently hide or block all others.
- [DETAIL] Select the first declaring commit in a deterministic newest-first
  traversal for duplicate declarations, and recognise only explicit PR-message
  forms such as `Merge pull request #N` or a subject's trailing `(#N)`; no API
  lookup is needed for an optional reference.
- [DETAIL] Wrap the repository's existing prime hook in one sequential command;
  a separate global SessionStart hook would not establish ordering with prime.
  The source lives in `tools/claude-code/` and is invoked directly, not installed.
- [DETAIL] Use the existing live-session scan and conservatively skip automatic
  writing whenever another same-repository session is present; an unreadable
  registry or scan also skips. The designated writer can still reconcile in
  its merge step. This is not the general cross-harness writer guard.
- [DETAIL] The hook preserves prime output and makes reconciliation failures
  visible in German; successful no-op runs are quiet. It never turns a failure
  into an assertion that no closures are pending.
- [DETAIL] Phase-4 appetite is three hours including repairs, a stop chosen to
  bound one local command, its integrations and failure-path tests.
