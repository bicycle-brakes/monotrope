---
title: "Spec — verify-cheap-before-admission"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, admission, kit]
class: bounded
appetite: 6
adr_files: []
neighbours: []
---

# Spec — verify-cheap-before-admission

Catch all cheap blocking faults before waiting for the machine's expensive-work
slot, everywhere the kit's full check runs (bead coding-harness-bxxt.6 — cheap
verification before admission). Research: [research.md](research.md).
Maintainer answers: [decisions.md](decisions.md), Q-1 through Q-5.

## Problem

At `b1d4e621` (2026-11-13), `scripts/verify_all.sh` takes admission before
selecting or executing gates. Ordering cheap gates first therefore still makes
them wait for the slot. The interview records a 710-second wait followed by a
lint failure in seconds. The declared cost already distinguishes cheap and
expensive gates, but the runner's TSV does not expose it (research, “What exists
today”).

The Stage-2 runner also takes admission around full verification and its
preparation, and around draft document checks. Changing only the shell would
leave those paths behind the same wait. Reusing a pre-admission result also
needs a content comparison: the existing dirty boolean cannot distinguish
different contents of an already dirty file (research, “Draft gap resolution”).

## Terms

- **Admission:** the existing per-user, per-machine queue, lock and memory
  check that grants the expensive-work slot.
- **Unprotected gates:** selected `seconds` gates without the explicit
  shared-state exception. **Protected gates:** selected `minutes` gates and
  seconds gates explicitly marked as requiring admission in the one gate list.
- **Same tree:** the same HEAD identity, index entries, tracked working paths
  and their contents/types/modes/deletions, and non-ignored untracked paths and
  contents. Ignored untracked caches, Git bookkeeping and external state are
  outside this comparison; tracked files remain included even if ignored.

## Acceptance criteria

1. When a gate is selected, its admission requirement comes only from its
   declared cost and optional boolean shared-state exception in the one gate list.
   *Refuted by:* a gate-ID allowlist, an invalid exception value being accepted,
   a minutes gate bypassing admission, or an unmarked seconds gate requesting it.
   *Basis:* decisions.md#Q-1.
2. When a local run has unprotected gates, every one executes before that run
   requests admission, even after another unprotected gate fails.
   *Refuted by:* queue registration before the last such gate, a missing cheap
   diagnostic, or any protected gate executing after a cheap blocking failure.
   The failed run names every selected protected gate it did not execute.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3.
3. When the unprotected phase has no blocking failure, all selected protected
   work executes under one valid admission, with none requested for an empty
   protected set.
   *Refuted by:* a heavy/marked gate running unlocked, one admission per heavy
   gate, or seconds-only `docs`/`drift` jobs waiting for the slot.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.
4. When admission follows a stable green unprotected phase, its results are
   reused exactly when the tree is unchanged; a changed tree requires a fresh
   selection and complete unprotected pass before protected gates execute.
   *Refuted by:* unchanged cheap gates running twice, an edit to an already
   dirty file being missed, stale gate configuration being used, or a protected
   gate executing after the fresh pass turns blocking red.
   *Basis:* decisions.md#Q-2.
5. If selection or tree comparison cannot be measured reliably, the run fails
   with a diagnostic before relying on unmeasured cheap results.
   *Refuted by:* an empty/failed selection reporting green, unreadable inputs
   being treated as unchanged, or a tree changing during a cheap pass being
   accepted as a stable baseline.
   *Basis:* decisions.md#Q-2; research, “Draft gap resolution”.
6. When gates fail, existing enforcement and selection rules still determine
   the verdict: only `block` is fatal, the local protected phase stops at its
   first blocking failure, and `--ci` remains exhaustive.
   *Refuted by:* a report/advisory fault suppressing protected work, a later
   local protected gate running after blocking red, changed job/placement
   membership, or `--ci` omitting a selected gate because an earlier one failed.
   Hosted CI's generated gate steps and always-run conditions remain identical.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; research, existing enforcement.
7. When protected work nests, is refused or is interrupted, existing admission
   ownership, refusal and descendant-cleanup guarantees still hold.
   *Refuted by:* queueing behind one's own valid ancestor, accepting a forged
   marker, executing protected work after refusal, or releasing its lock while
   a protected child or grandchild remains running.
   *Basis:* decisions.md#Q-1; research, admission mechanism.
8. When verification records durations, one invocation has one run identity
   spanning cheap and protected work, with execution time excluding queue and
   memory waits and history describing only actual executions.
   *Refuted by:* duplicate run identities at admission, omitted repeated cheap
   executions, fabricated skipped-gate records, wait counted as execution,
   misattributed admission context, unreadable old history, or a storage failure
   changing the gate verdict. A cheap-only completion states that no admission
   was requested; interrupted runs remain visibly incomplete.
   *Basis:* decisions.md#Q-2; decisions.md#Q-3; research, duration history.
9. When cheap or protected gates fail, their existing gate frames remain usable
   by the repair-evidence parser without inventing sections for skipped gates.
   *Refuted by:* the parser losing either of two cheap failures, its command or
   diagnostic, or treating a not-run summary as an executed gate.
   *Basis:* decisions.md#Q-3; research, frame guard.
10. When Stage 2 performs full post-attempt verification, full fallback/final
    review verification, or draft document verification, it uses the same
    admission-by-gate behavior as the shell entry point.
    *Refuted by:* any of those paths taking a whole-run admission before cheap
    gates/preparation, changing its selected gate set, losing its execution
    bound or timeout diagnostic, or charging admission wait to that bound.
    *Basis:* decisions.md#Q-1; decisions.md#Q-4; research, outer runner and limits.
11. When the kit transfers the full check into a recipient repository, the same
    behavior works with recipient gate IDs and no opt-out switch.
    *Refuted by:* a missing transferred dependency or proof, renamed IDs
    defeating classification, or configuration restoring whole-run admission.
    *Basis:* decisions.md#Q-5.

## Non-goals

- A separate check after a merge, cross-run caching, skipped mandatory gates,
  faster test bodies, or changing cost assignments, commands or enforcement.
- More slots, a new queue, memory/worker policy, priority policy, or a service
  reporting verification state. The existing lock remains the admission engine.
- Changing targeted-repair selection, proof/import-probe admission, foreign
  model routes, retry counts, or the shared verification execution allowance.
- Freezing tracker, network or machine state between the two phases, or
  preventing concurrent repository edits throughout protected execution.
- Migrating kit recipients. Phase 2b and an ADR are not due for this bounded
  change; no architecture decision is introduced.

## Boundaries

- The tree comparison hashes the content of every tracked and non-ignored
  untracked path, because "same tree" is defined by content; its cost grows
  with the checkout and has no bound of its own. Only a run with protected
  work measures it, at most five times (before and after each cheap pass and
  at the admission boundary); a seconds-only job and a cheap pass that ended
  blocking red measure no baseline at all. Measured at `36b4b356`
  (2026-11-14): 0.07 to 0.19 s per snapshot over 1,066 paths. A recipient
  with a large non-ignored untracked tree ignores it or pays that cost (loop
  row L2-8).

## Protected areas

Held `decisions/gates.yaml` and `prompts/05-verify.md` are orchestrator-only
bootstrap edits after the accepted implementation attempt. Hosted workflow
output must remain identical; `.github/workflows/ci.yml` needs no write.
Other held paths, other change folders, ADRs, tracker state and model settings
are outside this implementation. Admission's queue, memory floor, token
validation and lock-lifetime mechanics retain their current guarantees.

## Definition of Done

- `make verify` green after orchestrator bootstrap, with planted cheap faults,
  real isolated contention, changed-tree reuse checks and a transferred-kit proof.
- The same pull request updates `docs/WORKFLOW.md`, `docs/how-it-works.md`,
  `docs/orchestration.md`, `docs/testing.md`, `prompts/05-verify.md`, and
  `docs/governance/gate-catalog.md` for the new order and timing meaning.
- The file list shows the non-goals unbuilt and held-path ownership respected.
- The pull request closes the cheap-before-admission task; its closing commit
  carries `Closes-Bead: coding-harness-bxxt.6`.
- Isolated contention and kit-proof evidence name their tested commit in the
  pull request; no real long queue or foreign-model invocation is required.

## Open decisions

None open. The five maintainer answers are retained unchanged.

[DETAIL] Use an optional `needs_admission` boolean under schema 3 and derive
effective protection as `cost == minutes` or that value being true. Absence
means false; false cannot exempt a minutes gate. This is an additive field,
not a second gate list. No current seconds gate needs the mark on the evidence
read; audit again before activation.

[DETAIL] Preserve enforcement when interpreting “all red”: collect all cheap
diagnostics, but only blocking red refuses the local protected phase. Otherwise
this change would silently turn reporting gates into blocking ones. `--ci`
runs both partitions exhaustively, still admitting protected work.

[DETAIL] A stable snapshot brackets each cheap pass; after a changed wait the
fresh cheap pass runs inside the already acquired admission. An unstable or
unreadable snapshot fails with a request to rerun, rather than looping or
claiming unchanged. Results belong to this invocation only. This makes the
tree-comparison obligation explicit without inventing an external-state cache.

[DETAIL] Use one internal scheduler from the shell and Stage 2, retaining the
shell's public entry points and canonical gate selection. Stage 2 invokes its
API with bounded gate-launch callbacks rather than wrapping `make` in a
whole-run admission. This reversible launch detail closes the outer-lock gap
and keeps waits outside execution limits; preparation remains before gates.

[DETAIL] Allow six hours for phase 4 including repairs, stopping at that limit.
It covers admission, runner integration, timing and portable contention proofs.
Use the phase-3 prompt's form because `templates/plan.md` is absent at the
research commit; the artifact validator named in the prompt is absent too.
