---
title: "Spec — slip-counter"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-13", model: "gpt-6.1-sol"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, run-log]
class: bounded
appetite: 6
adr_files: []
neighbours: []
---

# Spec — slip-counter

Derive missed-verification observations from local check histories, with
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
  exactly one distinct start and one distinct completion after byte-identical duplicate records are collapsed, a completion not before its start, a
  known check kind, nonempty repository, change, checked-tree and
  gate-configuration identities, and, where the run records its checked tree
  at both ends, the same tree at both; targeted checks require both readings. Every in-scope run passes this one check before it may count, whatever its kind
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
   *Refuted by:* a qualifying overlapping pair counts zero, or a byte-identical duplicate full completion prevents the pair counting exactly once.
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
   each record the checked tree and comparison evidence and its completion records the actual outcome needed by the reader.
   *Refuted by:* a stable check records unknown identity, a failed check records green, a targeted green whose start and end trees differ followed by a red full run of its start tree counts as a slip, or history contains a slip event.
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
   *Refuted by:* a complete red full run whose only possible targeted predecessor has conflicting completions or a changed tree is counted as a non-slip; or a moved targeted predecessor followed by a full red on its end tree does not mark both incomplete; or a targeted green, a potentially matching full run with no end, and a full red do not mark all three incomplete.
   *Basis:* decisions.md#Q-10.
8. When the reader selects a repository, interval and optional change, only
   selected runs contribute to the reported counts.
   *Refuted by:* an out-of-scope run changes a count, or an earlier predecessor outside the interval is ignored.
   *Basis:* decisions.md#Q-2, decisions.md#Q-5, decisions.md#Q-8.
9. When the report encounters legacy duration runs or change-less full runs,
   it reports their number outside the count without treating them as incomplete.
   *Refuted by:* an attributable legacy or change-less full run raises the incomplete count or is absent from the outside-count line, or a well-formed legacy pair after a version-2 marker makes the report partial.
   *Basis:* decisions.md#Q-9.
10. If history is partial or unavailable, output and exit status distinguish it
    from a complete measurement while preserving supported observations.
    *Refuted by:* one interrupted in-scope run yields a complete exit, or either history file is missing after version-2 evidence exists and the report exits complete, or an orphan full end between a targeted green and full red leaves a slip counted, or a timestamped orphan before the lower bound still makes that selection partial, or an unassignable damaged row yields complete success.
    *Basis:* decisions.md#Q-2, decisions.md#Q-4.
11. While measurement is used, verification outcomes and duration history remain intact.
    *Refuted by:* reporting changes history, legacy duration readers reject new full-run records or count a targeted check as a full duration, an append failure changes the verification result, or substituted storage is followed.
    *Basis:* decisions.md#Q-1; research, duration-history refusal contracts.

12. When a full run's uncertain predecessor is known to be a full run and no earlier targeted green could precede it, the report keeps the later run's non-slip status and counts its flaky signal as undecided.
    *Refuted by:* a full run with conflicting green and red completions followed by a valid full red makes that later run incomplete or reports a decided flaky signal; or an uncertain intervening full run after a possible targeted green fails to make all three runs incomplete or prints a flaky line.
    *Basis:* decisions.md, agent decisions S-20 and S-26.
13. When two potentially matching checks have equal completion timestamps, both selected runs are incomplete.
    *Refuted by:* targeted green and full red at the same completion time are reported as a complete non-slip.
    *Basis:* decisions.md, agent decision S-18.
14. When a full-run completion has no start, the report classifies it as outside the count before the first version-2 comparison record in the duration history and otherwise marks the report partial.
    *Refuted by:* an orphan completion after the first version-2 comparison record is treated as legacy, or one before it makes the report partial; or a well-formed legacy start/end pair after the marker makes the report partial.
    *Basis:* decisions.md, agent decision S-12.

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
records addressed below. An invalid intervening check that could share the identity leaves the predecessor and successor undecidable too; mark all affected selected runs incomplete. A moved targeted tree remains a possible match to either its start tree or its end tree. A full run without an end may intervene after it starts, even while still running: a possible targeted predecessor and full-red successor are incomplete as well. A full-run orphan end between a targeted green and full red may intervene, so both selected sides are incomplete; the orphan is diagnosed without inventing a run count. If an uncertain full run may intervene between a targeted green and full red, because its tree or order is uncertain (including conflicting ends or equal completion times), all three are incomplete and no flaky line is printed. Only where no earlier targeted green could precede that full run does the known-full-predecessor rule in criterion 12 apply. A wholly lost run cannot be
reconstructed. The targeted history is created at the first version-2 runner record. Once the duration history has a version-2 record, a missing targeted history makes the report unavailable; a missing duration history with a present targeted history also makes it unavailable, never a complete zero.

Legacy is a record format: a well-formed version-1 start/end pair without comparison evidence is legacy wherever it appears, including after a version-2 marker. The outer duration event stays version 1; a version-2 comparison marker in an additive full-start field distinguishes orphan ends by position in that history. An orphan end before the first marker is outside the count; one after it is damaged and makes selections it could belong to partial. An end completing before the lower interval bound cannot belong to that selection; its unknown repository can be any repository. A report without bounds remains partial after such an end, and a damaged line with no timestamp makes every report partial; `--since` can exclude a timestamped end. If the first new start is lost before any marker is written, its orphan end is indistinguishable from legacy and can be classified outside the count. Legacy and change-less full runs are outside
the slip population (decisions Q-9). Count them on the outside line only where
repository and start time can be established; under a requested change, label
them as not change-scoped. Report
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

None open. The maintainer's answers Q-1 through Q-10 and accepted agent decisions S-12 through S-27 govern this revision.

[DETAIL] Keep full-run events version 1 with additive comparison fields and a version-2 comparison marker; put targeted-check records in a separate history beside `verify-duration.jsonl`. This keeps old duration readers compatible and excludes targeted durations from full-run minutes. The reader combines both histories; no slip records are written.

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
