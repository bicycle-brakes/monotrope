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
   *Refuted by:* any of the 15 data appends bypasses the helper, a reader can race an append, a missing log fails, or a scenario text append gains or loses bytes.
   *Basis:* decisions.md#Q-1.
5. When a new append-mode log open bypasses the shared helper anywhere under `tests/`, including executable stand-in source strings, the guard test fails and identifies its source location.
   *Refuted by:* a planted bypass passes the guard, or the guard rejects the helper's own implementation or an explicitly identified non-log lock/document test operation.
   *Basis:* decisions.md#Q-2.
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

None open. The two maintainer answers remain unchanged.

- [DETAIL] The appetite is three hours of phase 4 including repairs, a stop
  chosen because neither answer states a budget and this is a bounded repair.
- [DETAIL] The 17-site inventory retains its two lock-only operations as
  explicit classifications; only its 15 data appends require migration. This
  follows the inspected operations without calling a lock probe a log write.
- [DETAIL] Missing logs remain empty snapshots; actual I/O and parsing errors
  propagate. This preserves fixture behavior and keeps the observer honest.
- [DETAIL] Guard exemptions identify individual non-log operations, never a
  whole file. The guard covers ordinary append-mode `open`/`Path.open`, with
  positional or keyword modes beginning with `a`, in Python and embedded
  Python stand-ins; arbitrary obfuscation, dynamic mode construction and raw
  OS writes are outside this bounded static guard's claim.
- [DETAIL] Deterministic handshakes plus repeated concurrent runs establish
  the regression evidence; sleep-only timing would recreate the same flake.
