---
title: "Spec — flaky-swarm-leak-test"
status: draft
implementation_status: partial
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-yb1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, swarm, concurrency]
class: bounded
appetite: 3
adr_files: []
neighbours:
  - plans/changes/swarm-test-speed/spec.md
  - plans/changes/raising-fault-test/spec.md
---

# Spec — flaky-swarm-leak-test

Concurrent test-log access must preserve complete observations without weakening
the swarm's security refusal (bead coding-harness-yb1l — flaky swarm leak test).
Research: `research.md`. Maintainer answers: `decisions.md`.

## Problem

The research records two main-CI failures of the refused-run notice test,
reported in the 2026-11-12 night handover: its clean second run returned 2
instead of 0. These CI logs were not read directly. Its print observer parses
the call log while stand-in processes append large records; an incomplete
line can raise inside the gate and correctly trigger a fail-closed refusal.
That causal chain is inferred, not yet reproduced.

The maintainer chose a common test-log helper and a regression guard rather
than a one-test workaround. The draft inspection at `3950c853` accounts for
the interview's 17 opens: 15 data appends and two lock-only opens across five
test files; three data appends already have a local lock. Shared readers must
participate too: locking only writers still exposes partial records.

## Terms

**Atomic observation:** a reader sees a snapshot of complete appends; an
append in progress is either absent or complete, never a partial fragment.
**Test logs:** stand-in call, infrastructure, version, installer and receipt
logs in the five files inventoried in `research.md`, including their generic
scenario-driven text appends.
**Declared stand-in log:** a JSON test log whose file name the shared helper
declares (`STAND_IN_LOGS`); the helper's JSON functions serve no other name.
Append-mode opens elsewhere under `tests/` — production-lock probes, document
mutations, the admission-order probe of the verify lock (whose writers the
lock under test admits one at a time) — are not stand-in logs.
**Receipt log (`receipts.jsonl`):** a test log with a production writer, so
not a declared stand-in log (2026-11-14, loop row L2-6). The swarm stand-in
appends receipts through the helper's `text_append`, but the production tool
wrapper (`scripts/stage2_research_tools.mjs`, `appendFileSync`) writes the same
file and cannot take Python's `flock`; production reads it without the helper,
once the seat's process has ended (`scripts/stage2_research_run.py`). Its
protection therefore rests on each writer appending one small receipt line (a
bounded title and excerpt) in a single `O_APPEND` write and on that late read,
not on the helper's lock; the helper's lock only orders the stand-in's own
appends. Changing the production writer or reader is a non-goal of this
change.

## Acceptance criteria

1. When independent stand-in processes append to a test log while another process or the pytest observer reads it, every observation contains only complete appends.
   *Refuted by:* a forced mid-append read returns a fragment or raises a JSON parsing error for otherwise valid records.
   *Basis:* decisions.md#Q-1.
2. When concurrent writers finish successfully, the final test log contains every submitted record exactly once with its full payload.
   *Refuted by:* an identifier is missing or duplicated, or a large record's payload differs from the submitted value.
   *Basis:* decisions.md#Q-1.
3. If a test log already contains malformed JSON, the shared JSON reader reports the parse failure rather than hiding it.
   *Refuted by:* a malformed stored record is skipped, truncated, retried indefinitely or returned as an empty successful observation.
   *Basis:* decisions.md#Q-1.
4. When any inventoried stand-in data append or corresponding concurrent log read executes, it uses the shared helper while preserving the existing record contents and missing-log-as-empty behavior.
   *Refuted by:* any of the 15 data appends of the five-file stand-in inventory bypasses the helper, a reader can race an append, a missing log or its missing directory fails, or a scenario text append gains or loses bytes.
   *Basis:* decisions.md#Q-1.
5. When a test reads, writes or opens a declared stand-in log without the shared helper anywhere under `tests/`, including executable stand-in source strings, the guard test fails and identifies its source location.
   *Refuted by:* a planted raw read or append of a declared log passes the guard, the guard flags a helper call or an operation on a file that is not a declared log, or it needs an exemption list to pass the repository.
   *Basis:* decisions.md#Q-2; decisions.md#Q-3; decisions.md, "Guard design after the review loop".
6. When a leak refuses a swarm run and its inputs are then restored, the refused run is announced before any model call in the next successful run.
   *Refuted by:* the leaking run starts a model call or returns success, the clean run returns 2, or its first refused-run notice is absent or observes a nonzero call count.
   *Basis:* decisions.md#Q-1.
7. When the repair is submitted for review, its evidence includes a failing torn-read reproduction before the fix and the same workload passing after it, together with repeated refused-run checks under concurrent load.
   *Refuted by:* only green reruns are shown, workloads differ without explanation, an after-run fails, or commands, commits, repetition counts and diagnostics are missing.
   *Basis:* decisions.md#Q-1.

## Non-goals

- Production runner, dispatcher, leak-check or admission changes; no exception
  suppression, retries or relaxed assertions to make the flake disappear.
- Faster swarms, changed scheduling, new dependencies or workflow changes.
- A transactional allocation of scenario steps, crash recovery for a killed
  writer, or atomic reads by production readers of arbitrary fixture text.
- A claim that the historical CI failures are conclusively explained without
  their diagnostics; local reproduction proves the mechanism it exercises.
- Design phase 2b and an ADR draft: this bounded test-only repair requires neither.

## Boundary

The guard knows stand-in logs by declaration only (decisions.md#Q-3, loop
row L2-1). It fails on a raw read, write or open of a file whose name is one
of the helper's declared names (`STAND_IN_LOGS`); a test that introduces a
log under a new name and appends to it concurrently without the helper is
not seen, and the torn-read flake could return through that name. The
helper refuses an undeclared name in its JSON functions, so a log that uses
the helper is always one the guard watches; the gap is the log that never
uses it. The maintainer chose to ship with this boundary stated; the
contract that closes it is tracked separately (bead coding-harness-6zpj).
Paths that never carry a declared name, arbitrary obfuscation and raw OS
calls stay outside the guard as well ([DETAIL] under Open decisions).

## Protected areas

`scripts/`, `tools/`, `tests/terms_fixtures.py`, production configuration,
`prompts/`, `templates/`, governance files and other change folders stay
untouched: the test mechanism is the repair boundary. The neighbouring
swarm-test-speed change's protected production call and scan paths stay intact.

## Definition of Done

- Targeted checks and runner-owned `make verify` are green.
- The shared helper, its tests, the five migrated test files and this change's
  research/spec/plan move together; no model, ADR or external document changes.
- The pull request's file list demonstrates the protected areas and non-goals.
- The final implementation commit carries `Closes-Bead: coding-harness-yb1l`;
  the orchestrator owns tracker and pull-request work.
- Red/green concurrency evidence and repeated loaded runs name their date,
  measured commit, exact command and outcomes in `plan.md` and the PR body.

## Open decisions

None open. The two answers of 2026-11-13 remain unchanged; the maintainer's
third answer (decisions.md#Q-3, 2026-11-14) states the guard's name boundary.

- [DETAIL] The appetite is three hours of phase 4 including repairs, a stop
  chosen because neither answer states a budget and this is a bounded repair.
- [DETAIL] The 17-site inventory retains its two lock-only operations as
  explicit classifications; only its 15 data appends require migration. This
  follows the inspected operations without calling a lock probe a log write.
- [DETAIL] Missing logs remain empty snapshots; actual I/O and parsing errors
  propagate. This preserves fixture behavior and keeps the observer honest.
- [DETAIL] (2026-11-14, replacing the exemption-list guard.) The guard
  identifies stand-in logs by the helper's declaration and has no exemption
  list: it fails on `open`, `read_text`, `read_bytes`, `write_text` or
  `write_bytes` of a path that carries a declared name, directly, through a
  variable or through an environment key, in Python and embedded Python
  stand-ins. A path that never carries a declared name, arbitrary
  obfuscation and raw OS calls are outside this bounded static guard's claim
  (decisions.md, "Guard design after the review loop").
- [DETAIL] (2026-11-14.) The lock is the data file's own `flock`, waited for
  at most 60 s before `TimeoutError`: one identity for every spelling of a
  file, no lock file in a fixture repository, and a wedged writer fails a
  reader loudly instead of hanging it.
- [DETAIL] (2026-11-14, loop row L2-2.) The suites clear a declared log by
  removing the file, and the helper offers no locked clear. Because the lock
  is the file's own, a removal splits it: a writer of the cleared run still
  holding the old file's lock finishes its record on the removed file, while
  the next run's writers and readers lock the new file. That split is the
  clear's purpose: the late record must not reach the next run, and the next
  run must not wait on the old writer. A clear that empties the file in place
  under the lock would do both wrong (it waits for the old writer, which then
  appends into the next run's log); a lock taken only around the removal adds
  no guarantee, since the removed file's content is discarded anyway. So
  removal stays the clear, and the guard does not count it as raw access
  (`test_a_cleared_log_starts_fresh_under_a_late_writer`, red on an in-place
  clear with a `TimeoutError`, green on removal).
- [DETAIL] Deterministic handshakes plus repeated concurrent runs establish
  the regression evidence; sleep-only timing would recreate the same flake.
