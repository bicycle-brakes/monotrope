---
title: "Spec — free-storage-keys-flake"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-068l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, flaky-test, research-swarm]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — free-storage-keys-flake

Find and fix the cause of the intermittent free-model storage-key test failure
without weakening its coverage (bead coding-harness-068l — reproduce and fix
the free storage keys flake). Research: `research.md`; decisions: `decisions.md`.

## Problem

- In the merge queue on 2026-11-08, the case with a long model name and no
  scripted failure exited 1 instead of 0; a different pull request passed the
  suite on the same base shortly afterwards (`decisions.md`, first measurement,
  base `8f740e13`).
- On 2026-11-21 at `ee349b78`, 25 serial repetitions of all six cases and one
  random-order run passed; neither the cause nor a successful reproduction was
  established (`decisions.md`, first measurement; `research.md`, What is unclear).

## Acceptance criteria

1. When reproduction is attempted, repeated runs of the full swarm test file
   use parallel workers, varied recorded test order and concurrent CPU load.
   *Refuted by:* a run omits the load, parallel workers, full file or recorded order.

2. When a reproduction attempt ends, its dated evidence records the revision,
   command, load and order, run count, failure count and failing swarm stderr.
   *Refuted by:* a missing count or setting, or a failure without captured stderr.

3. If a cause is found, a regression forces the observed nondeterministic
   interleaving and fails before the fix but passes after it.
   *Refuted by:* the regression passes against the unfixed revision, fails
   against the fix, or does not exercise the observed cause.

4. When the free-model storage-key test runs after a fix, its existing six
   cases retain their names and behavioural assertions.
   *Refuted by:* a removed or renamed case, weakened assertion, new skip or
   expected-failure marker, or a failed existing case.

5. If no cause is found within the implementation appetite, the attempt stops
   without a speculative fix and records what was tried and measured in a
   `Stopped without a cause` section of `findings.md`.
   *Refuted by:* an unproven fix or a stop without that evidence.

## Non-goals

- Retrying failures, extending timeouts, skipping tests or masking the failure.
- Changing admission, storage-key contracts or swarm behaviour unrelated to
  the demonstrated cause; broader suite or fixture optimisation is separate.
- Renaming the existing test or changing its archived criterion-ledger rows.

## Protected areas

- `plans/changes/archive/2026-11-06-research-swarm/plan.md`: the existing
  test name and its ledger rows stay intact.
- Admission and leak-check policy, model declarations and verification gates:
  the failure does not establish a reason to weaken them.

## Definition of Done

- A reproduced cause and red-before/green-after regression are documented;
  the existing six cases and `make verify` pass after the fix.
- The pull request includes the reproduction evidence, revision and commands;
  protected areas and non-goals are checked against its file list.
- The pull request closes bead coding-harness-068l — reproduce and fix the
  free storage keys flake — and its last commit carries
  `Closes-Bead: coding-harness-068l`.
- If the appetite expires without a cause, report a stop instead of claiming
  this definition of done or closing the bead.

## Open decisions

None open.

- [DETAIL] Set a two-hour phase-4 appetite including repairs: this bounds an
  investigation whose cause is not yet known. Stop rather than infer a fix.
- [DETAIL] Use at least three different recorded orders for load attempts:
  this gives a repeatable minimum without claiming to prove absence of a flake.
- [DETAIL] No research-swarm handoff is present; the suggested neighbours in
  the single-explorer report are not a completed swarm's confirmed paths.
