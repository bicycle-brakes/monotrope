---
title: "Spec — red-first-own-refs"
status: draft
implementation_status: partial
date: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-wkxm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, red-first]
class: bounded
appetite: 2
adr_files: []
---

# Spec — red-first-own-refs

Repair proofs detect changes to their own Git references without being
invalidated by another session's Git activity (bead `coding-harness-wkxm` —
isolate repair proofs from concurrent reference movement).
Research: [research.md](research.md). Settled scope: [decisions.md](decisions.md).

## Problem

At draft baseline `36c74d03` on 2026-11-01, both `red_first` and
`fixed_test_proof` in `scripts/stage2.py` compare every reference in the
source repository's shared store. The baseline proof uses a linked worktree;
the fixed-code proof runs in the repair worktree. Neither comparison can
attribute a changed reference to the named test or another session.

The research records a baseline refusal naming another change's branch in
`plans/changes/repair-fixed-line-format/findings.md` on 2026-10-26 and a
fixed-code refusal without reference names in
`plans/changes/terms-expiry/findings.md` on 2026-10-27. The interview skip
records further occurrences on 2026-10-31 and 2026-11-01. Repeated retries
cannot close a mechanism that treats another session's legitimate work as
test interference.

The existing protection remains necessary: the original repair review found
cleanup deleting another session's branch and a moved reference escaping
detection. The recorded remedy isolates the proof's store rather than
narrowing which references are protected (`decisions.md`, "Details for the
draft").

## Terms

- **Source repository:** the repair worktree and the Git store it shares with sibling worktrees.
- **Proof repository:** a temporary checkout with its own reference store, used for one baseline or fixed-code proof.
- **Reference change:** a difference in reference names or targets between the measurements around a proof invocation, in any namespace, including remote-tracking and runner-attempt references.
- **Qualifying run:** the existing invocation-bound pytest evidence: a qualifying call failure on baseline, or passing setup, call and teardown for every selected case on fixed code.

## Acceptance criteria

1. When another session creates, deletes or moves references in the source
   repository during either qualifying proof run, that activity does not
   invalidate the proof.
   *Refuted by:* either otherwise valid proof being refused because a source
   branch, remote-tracking reference or runner-attempt reference changed.
2. If the reference names or targets measured before and after either
   named-test invocation differ in the proof repository, the proof is refused.
   *Refuted by:* a qualifying pytest outcome being accepted despite a changed
   proof reference, including one outside the branch namespace.
3. When either proof is refused for reference changes, its scrubbed diagnostic
   identifies the named test and every changed reference by name.
   *Refuted by:* a fixed-code refusal saying only that references changed, an
   omitted changed reference, a missing selector or an exposed credential.
4. When the baseline proof runs, it exercises the baseline's production files
   with the attempted repair's current tests.
   *Refuted by:* the attempted production fix reaching the baseline proof or
   a newly added or amended test being absent from that proof.
5. When the fixed-code proof runs, it exercises the attempted repair's current
   Git-visible file tree, including uncommitted changes and new files.
   *Refuted by:* checking committed HEAD instead, losing a deletion, executable
   bit or symlink, or failing to include a new test or production file.
6. While either proof prepares, runs or cleans up, its ordinary Git operations
   and file writes leave the source worktree, index and references unchanged.
   *Refuted by:* proof setup moving a source branch, a test's cwd-relative
   branch write reaching the source store, or cleanup resetting or deleting a
   source reference created by another session.
7. If proof setup, required state measurement or cleanup fails, or the
   fixed-code proof changes its file tree, the proof is refused with the
   cause identified.
   *Refuted by:* an unreadable before/after reference listing, failed clone,
   unavailable fixed tree, changed fixed proof tree or failed cleanup yielding
   a successful proof.
8. When either proof finishes, is refused or times out, its temporary checkout,
   private reference store and probe reports are removed unless removal itself
   fails and is reported under criterion 7.
   *Refuted by:* a leftover temporary directory or a source worktree registry
   entry after successful cleanup, including a partially prepared proof.
9. When the proofs run in isolation, the existing pytest evidence rules and
   execution protections retain their verdicts.
   *Refuted by:* a nonqualifying baseline run or nonpassing fixed run receiving
   repair evidence, a modified interpreter being run, an unsanitized diagnostic,
   or loss of the existing admission and time limits.

## Non-goals

- Excluding namespaces from proof-reference comparison or accepting a named test's reference writes.
- Changing retry routing, attempt limits, checkpointing, saved-attempt references, pytest outcome classification or evidence marks.
- Provisioning ignored dependencies, copying a virtual environment or changing machine-wide test admission.
- Implementing the neighbouring test-guard change or rewriting the workflow doctrine.
- Phase 2b and an ADR: this is a `bounded` correction of proof execution, preserving the existing protection contract.

## Boundary

Isolation covers Git commands resolving their repository from the proof's
working directory and the runner's own setup and cleanup. It is not an
operating-system sandbox: a test explicitly addressing the source repository
or another external path can still write there. Shared-store observation
cannot distinguish such a write from another session's activity; it must not
invalidate a proof merely for observing a foreign move. Within the private
store every reference remains compared, without ownership guesses or prefix
exceptions. This change promises isolation of ordinary proof execution, not
attribution of arbitrary external writes. As today, before/after snapshots
detect differences that remain at the second measurement; they do not audit
transient reference writes that a test reverses before it finishes.

## Protected areas

- `save_attempt`, `checkpoint` and the source repository's refs: proof isolation must not change their ownership or lifecycle.
- `prompts/`, `templates/`, `decisions/`, `docs/adr/`, `provenance.yaml`, `model-endpoints.yaml` and agent configuration: no policy or architecture decision changes.
- Other change folders, except a dated clarification in `plans/changes/red-first-install/spec.md` linking this preservation of its criterion 8; retain its criteria and historical evidence.

## Definition of Done

- `make verify` is green after implementation, with the new isolation regressions shown red before the fix and green after it.
- Both proof paths cover local reference mutation and unrelated source-store movement; cleanup and failure cases are exercised.
- Moved with the code: `spec.md`, `plan.md` and runner evidence in this folder, the dated predecessor clarification, and the generated `plans/INDEX.md` through the runner/orchestrator.
- Protected areas remain untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes the repair-proof isolation work item and its last commit carries `Closes-Bead: coding-harness-wkxm`.
- Special external runs: none.

## Open decisions

None open. The reasoned interview skip and isolation choice are already
recorded in `decisions.md`; no maintainer answer or ADR answer is invented.

- [DETAIL] Use a two-hour phase-4 appetite, repairs included: the correction has two execution paths and a bounded regression matrix; this is a stop, not an estimate.
- [DETAIL] Compare only the proof repository's complete reference map: inspecting the shared map adds no attributable evidence and recreates the reported interference.
- [DETAIL] Preserve the original reference-protection tests' names and purpose while making the private store explicit; deleting that store after measurement is normal cleanup, never permission to delete a source reference.
- [DETAIL] Add a dated predecessor note without editing its criteria: readers can follow how its cleanup and reference protection are preserved through isolation.
