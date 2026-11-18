---
title: "Spec — slip-counter"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, run-log]
class: bounded
appetite: 6
adr_files: []
neighbours: []
---

# Spec — slip-counter

Derive missed-verification observations from the one local run history, with
incomplete evidence visible beside the count (bead coding-harness-bxxt.7 —
slip counter). Research: [research.md](research.md). Decisions:
[decisions.md](decisions.md), Q-1 through Q-10.

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

- **Targeted check:** only the runner's targeted repair check; a full fallback
  and cheap checks of implement or draft attempts are not targeted checks here
  (decisions Q-7).
- **Slip:** one red local full run answering the immediately preceding completed
  check of the same identity, when that check is a green targeted check. The
  identity comprises repository, change, checked tree and gate configuration.
- **Gate configuration:** the SHA-256 digest of the bytes of
  `decisions/gates.yaml` at the check's start; it identifies that file, not the
  executed subset, interpreter, environment or runtime gate outcomes.
- **Order:** UTC completion timestamps determine order; equal timestamps do
  not establish an earlier run. File order and monotonic values do not break ties.
- **Repository:** the shared Git repository, identified by its common Git
  directory, not the path of one checkout or worktree (decisions Q-5). Runs in
  any worktree of one repository pair with each other, and a report from any
  checkout of it selects the runs of every worktree.
- **Valid run:** a run that passes the one validity check (decisions Q-6):
  exactly one start and one completion, a completion not before its start, a
  known check kind, nonempty repository, change, checked-tree and
  gate-configuration identities, and, where the run records its checked tree
  at both ends, the same tree at both. Every in-scope run passes this one check before it may count, whatever its kind
  and verdict. A pair also needs complete evidence on both sides (decisions Q-10).
- **Checked tree:** the Git-visible contents and file modes actually checked,
  including uncommitted and non-ignored untracked inputs, minus the change's
  own `plan.md` and `findings.md` (decisions Q-3); commit identity or a dirty
  flag alone is insufficient. A changed or unreadable tree during a check, or
  a check without a change name, supplies no stable identity.
- **Incomplete run:** an identifiable in-scope run lacking valid, unambiguous
  start/end or comparison evidence; counted once as not countable.
- **Interval:** optional UTC bounds on run start, inclusive lower bound and
  exclusive upper bound; absent bounds select all recorded time.

## Acceptance criteria

1. When a valid red full run completes immediately after a valid green targeted
   check of the same identity, the reader counts one slip for the full run.
   *Refuted by:* a qualifying overlapping pair counts zero, or identical duplicate records multiply it.
   *Basis:* decisions.md#Q-1, decisions.md#Q-8.
2. If a check of the same identity completes between a targeted green and a
   full red, the earlier targeted green does not pair with that full red.
   *Refuted by:* targeted green, targeted red, full red counts a slip, or targeted green, full red, full red counts two.
   *Basis:* decisions.md#Q-8.
3. When a valid full green is immediately followed in completion order by a
   valid full red of the same identity, the report counts one separate flaky-test signal.
   *Refuted by:* full green then full red yields no signal, or an intervening same-identity check still yields one.
   *Basis:* decisions.md#Q-8.
4. When the runner executes a targeted repair check, its start and completion
   record the comparison evidence and actual outcome needed by the reader.
   *Refuted by:* a successful stable check records unknown identity, a failed check records green, or the history contains a slip event.
   *Basis:* decisions.md#Q-1, decisions.md#Q-3, decisions.md#Q-7.
5. When the runner starts a full verification for a named change, its start
   records the comparison evidence needed by the reader.
   *Refuted by:* an available repository, change, tree, gate configuration or full kind is recorded as unknown on the real runner path.
   *Basis:* decisions.md#Q-1, decisions.md#Q-5.
6. When an in-scope run fails the validity check, the report counts it once as incomplete.
   *Refuted by:* an interrupted, conflicting, unstable or unknown-identity run disappears or counts twice.
   *Basis:* decisions.md#Q-4, decisions.md#Q-6.
7. When a potentially matching pair has incomplete evidence on either side,
   each selected side is counted once as incomplete rather than as a slip or non-slip.
   *Refuted by:* a complete red full run whose only possible targeted predecessor has conflicting completions is counted as a non-slip.
   *Basis:* decisions.md#Q-10.
8. When the reader selects a repository, interval and optional change, only
   selected runs contribute to the reported counts.
   *Refuted by:* an out-of-scope run changes a count, or an earlier predecessor outside the interval is ignored.
   *Basis:* decisions.md#Q-2, decisions.md#Q-5, decisions.md#Q-8.
9. When the report encounters legacy duration runs or change-less full runs,
   it reports their number outside the count without treating them as incomplete.
   *Refuted by:* an attributable legacy or change-less full run raises the incomplete count or is absent from the outside-count line.
   *Basis:* decisions.md#Q-9.
10. If history is partial or unavailable, output and exit status distinguish it
    from a complete measurement while preserving supported observations.
    *Refuted by:* an unassignable damaged row yields complete success or suppresses an independently valid slip.
    *Basis:* decisions.md#Q-2, decisions.md#Q-4.
11. While measurement is used, verification outcomes and duration history remain intact.
    *Refuted by:* reporting changes history, legacy or older duration readers reject the other version's records, an append failure changes the verification result, or substituted storage is followed.
    *Basis:* decisions.md#Q-1; research, duration-history refusal contracts.

## Boundary

Only complete, comparable evidence counts. A potentially matching pair has
known recorded identity fields that do not conflict and an order that could
meet the pairing rule; unknown fields never prove a match. If more than one
candidate is possible, no arbitrary pair is chosen: affected selected runs are
incomplete once. Runs with known incompatible identities are not candidates.
An in-scope start without an end, including a check still running, is incomplete
at report time; a later report may become complete. An end without a usable
start, or damaged evidence missing repository, start time or requested change
scope, cannot be assigned to the selection: diagnose it separately and mark the
report partial, without inventing a run count, except for recognizable legacy
records addressed below. A wholly lost run cannot be
reconstructed. Missing history is unavailable, not zero.

Legacy means duration records predating comparison evidence, even though both
old and new records use version 1. Legacy and change-less full runs are outside
the slip population (decisions Q-9). Count them on the outside line only where
repository, start time and requested change scope can be established. Report
recognizable legacy runs without enough scope evidence separately as unattributed
outside runs; these do not make the slip measurement partial. An unknown
change on a non-legacy targeted run is not presumed to be a change-less full run.

**Boundary — the change's bookkeeping is unseen (decisions Q-3).** The runner's
time line, its call records and phase 6's committed rows and audit lines land
in `plans/changes/<change>/plan.md` and `findings.md` between a targeted check
and the later full one, so the comparison tree leaves exactly these two files
of the change out; every other path, another change's files included, still
counts. An edit to those two files between the checks therefore goes unseen:
a red full run caused by it — for example from a gate that reads them, such as
the criterion ledger — can count as one slip too many. The count is an
observation, not a cause, and this overcount stays possible.

**Boundary — the full run records its tree only at its start (maintainer,
2026-11-15).** A targeted check records its checked tree at its start and at
its end, and a moved tree makes it not countable. The full run's start record
carries its tree, but its end record is written by `scripts/verify_all.sh`,
which is outside this change, so the full run records no tree at its end. A
red full run whose tree moved during the check therefore still pairs with the
targeted green of its starting tree and can be counted as a slip although it
proved nothing about one tree. The error goes one way only: an overcount,
never an undercount. Recording the tree at the full run's end as well is
follow-up work (bead coding-harness-cf9h).

**Boundary — what the validity check cannot see (decisions Q-6).** The check
judges only what the history records. It cannot see a tree that moved and
moved back between the two readings of one run, a full run's tree at its end
(the Boundary above), a cause of red outside the recorded identities, such as
the machine, the interpreter or the network, or a run that left no record at
all. A run that passes the check on such evidence counts as recorded; a later
phase-6 row that describes only one of these limits is this limit, not a new
case.

**Boundary — records from before the repository answer (decisions Q-5).**
A run record that carries no common Git directory cannot be assigned to a
repository without guessing. Its duration stays readable, but the reader
reports recognizable legacy records separately as unattributed outside runs;
other unassignable evidence is diagnosed as partial without inventing a count.

## Non-goals

- A slip writer, persistent tally, receipt, repair of history or global service.
- Counting unique root causes, inferring a test failure from a timeout, or
  attributing the cause of an observed red result.
- CI/nightly collection, every partial-check source (follow-up bead coding-harness-l0g6), test tiers, automatic handover generation, changed
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

None open. The maintainer's answers Q-1 through Q-10 govern this revision.

[DETAIL] Use the existing gate-file digest and additive version-1 fields: old
readers ignore extra fields and continue reading durations, while new readers
distinguish legacy records by their absent comparison fields. This avoids a
version bump that older readers reject; compatibility is verified with the old
reader contract, not assumed from the version number.

[DETAIL] Use UTC completion time with strict inequality; equal timestamps do
not establish a predecessor. This deterministic conservative rule avoids
inventing an order from concurrent appends or unrelated monotonic clocks.

[DETAIL] Count a same-identity full-green/full-red signal only for consecutive
completed checks, once per red run, independently of slips. This applies the
same immediate-successor convention to the signal in Q-8.

[DETAIL] Treat a start without an end as incomplete even while it may still be
running: the history alone cannot prove interruption and the report can be rerun.

[DETAIL] Use the resolved common Git directory recorded at run time, the current
repository by default and UTC start-time bounds; recorded paths are not resolved
again because a removed worktree need not exist.

[DETAIL] The restarted phase-4 appetite is six hours including repairs, as
recorded in decisions.md on 2026-11-18. The phase-3 prompt provides the plan
form because no `templates/plan.md` exists in this worktree.
