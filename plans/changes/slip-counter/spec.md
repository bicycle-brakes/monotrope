---
title: "Spec — slip-counter"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, run-log]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — slip-counter

Derive missed-verification observations from the one local run history, with
incomplete evidence visible beside the count (bead coding-harness-bxxt.7 —
slip counter). Research: [research.md](research.md). Decisions:
[decisions.md](decisions.md), Q-1 and Q-2.

## Problem

At the researched head `efb2ad96` (2026-11-13), no slip counter exists in
`scripts/` or `tests/`. ADR 0025 already requires measuring failures the full
check finds after targeted green, but the duration history records neither a
targeted result nor enough evidence to pair it with a full run (research,
“What exists today”). Its commit and dirty flag cannot distinguish two
different dirty trees.

The stopped-lanes handover of 2026-11-13 records repeated findings in the
unmerged counter's own writes. The interview chooses derivation instead of
persisting slip records, and names the final failure: a missing full-run end
record produced a reported zero (decisions Q-1 and Q-2). That sibling
implementation and its findings were not read; this spec relies on the
recorded interview, not a reconstruction of its code.

## Terms

- **Slip:** one completed red local full verification run with an earlier
  completed green targeted check of the same repository, change, checked tree
  and gate configuration; an observation, not a count of distinct defects.
- **Checked tree:** the Git-visible contents and file modes actually checked,
  including uncommitted and non-ignored untracked inputs; commit identity or
  a dirty flag alone is insufficient. A changed or unreadable tree during a
  check supplies no stable identity.
- **Incomplete run:** an identifiable in-scope run lacking valid, unambiguous
  start/end or comparison evidence; counted once as not countable.
- **Interval:** optional UTC bounds on run start, inclusive lower bound and
  exclusive upper bound; absent bounds select all recorded time.

## Acceptance criteria

1. When a completed red local full verification run has an earlier completed
   green targeted check with matching repository, change, checked-tree and
   gate-configuration identities, the reader counts that full run once.
   *Refuted by:* a qualifying run counts zero, several green predecessors
   multiply it, or repeated identical records multiply it.
   *Basis:* decisions.md#Q-1; research, ADR 0025 measurement rule.
2. If a full run lacks that matching predecessor, it contributes no slip.
   *Refuted by:* targeted red, full green, full fallback masquerading as
   targeted, reversed completion order, another repository/change/tree or
   configuration, or an unknown identity establishes a slip.
   *Basis:* decisions.md#Q-1.
3. When the runner executes a targeted check, the local history contains its
   ordinary run evidence sufficient for later comparison with full checks.
   *Refuted by:* no identifiable start, green completion before successful
   completion, missing check kind or comparison identity without an explicit
   unknown, or any persisted slip event, counter or consumed marker.
   *Basis:* decisions.md#Q-1, including its accepted downside.
4. When the reader reports an interval, it shows the slip count and the
   number of incomplete runs excluded from counting beside each other.
   *Refuted by:* an identifiable interrupted or conflicting run disappears,
   is counted twice as incomplete, or is represented by a bare zero slips.
   *Basis:* decisions.md#Q-2.
5. When the reader selects an interval and repository, optionally narrowed
   to one change, only selected runs enter its counts.
   *Refuted by:* another repository, an out-of-interval full run or an
   out-of-interval incomplete run changes either count; a matching targeted
   predecessor before the interval is ignored for a selected full run.
   *Basis:* decisions.md#Q-2, “asked interval”; decisions.md#Q-1.
6. If history is partial or unavailable, the reader distinguishes that state
   from a complete measurement in both its output and exit status.
   *Refuted by:* an incomplete run, malformed/unassignable row, unsupported
   evidence or missing history produces a complete-success exit or a
   purported complete zero; valid observations beside a diagnosed gap vanish.
   *Basis:* decisions.md#Q-2; research, existing history reader contracts.
7. While the counter is used, history reading and measurement failures leave
   verification outcomes and the existing duration history intact.
   *Refuted by:* reporting writes history, repeated reporting differs on
   unchanged input, legacy duration records become unreadable, an append
   failure changes a verification verdict, or refused history is followed
   through a substituted destination.
   *Basis:* decisions.md#Q-1; research, duration-history refusal contracts.

## Boundary

The number measures only persisted, complete and comparable observations.
An interrupted run, invalid completion, conflicting duplicate or unavailable
comparison identity is not evidence of zero slips: show the number of such
identifiable runs beside the observed slips. Unassignable damaged rows are
diagnosed separately and make the report partial; do not invent run identities
or counts from them. A wholly lost run leaves no evidence and cannot be
reconstructed from this history. Missing history is unavailable, not zero.
Legacy records without comparison evidence remain readable as durations and
are not countable as slips. No equivalence between different trees is inferred.

## Non-goals

- A slip writer, persistent tally, receipt, repair of history or global service.
- Counting unique root causes, inferring a test failure from a timeout, or
  attributing the cause of an observed red result.
- CI/nightly collection, test tiers, automatic handover generation, changed
  check selection, admission, execution limits, retries or review gates.
- Porting the removed sibling counter or amending ADR 0025. Phase 2b does
  not run for this bounded change; no design or ADR draft is due.

## Protected areas

`scripts/verify_lock.py` and `scripts/verify_all.sh` retain admission and full
verification semantics. `scripts/stage2_runs.py` keeps its separate metrics.
Held paths, including prompts, templates, `AGENTS.md`, `provenance.yaml`,
`decisions/gates.yaml` and `model-endpoints.yaml`, need no changes.

## Definition of Done

- `make verify` green after focused evidence tests, including the real runner
  path from targeted evidence to full-run evidence, not only fabricated pairs.
- `docs/WORKFLOW.md`, `docs/orchestration.md` and
  `plans/specs/implementation-verification/spec.md` describe derivation and
  the two-number reporting boundary; no ADR or diagram changes.
- The pull request file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes the slip-counter task (bead coding-harness-bxxt.7);
  its closing commit carries `Closes-Bead: coding-harness-bxxt.7`.
- Focused fault demonstrations name their tested commit in the pull request.

## Open decisions

None open. The two maintainer answers remain unchanged.

[DETAIL] Count distinct red full-run identities, not distinct defects; this
matches what the history can prove without interpreting test output. Conflicting
duplicates make that run incomplete; identical duplicates do not multiply it.

[DETAIL] Use start-time interval membership, current repository by default,
and all recorded time when no bounds are given; these reversible reader
conventions make the requested interval reproducible.

[DETAIL] Set the phase-4 appetite to three hours including repairs: one local
reader plus comparison evidence, with a stop if the prerequisite cannot supply
a provable same-tree path. Implementation waits for the targeted-check change
to merge, as already recorded in decisions.md.

[DETAIL] Use the phase-3 prompt's plan form because `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent at `8807a2b8` (2026-11-13).
