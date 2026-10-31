---
title: "Spec — verify-worker-cap"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-l7sc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — verify-worker-cap

Local verification defaults to a machine-sized pytest worker count while
preserving explicit caller choices (bead `coding-harness-l7sc` — cap local
verification workers). Research: `research.md`. Decisions: `decisions.md`.

## Problem

The exploration of 2026-10-29 found that the pytest gate uses `-n auto`
without a worker bound. Its recorded baseline at `dbef390f`, measured
2026-10-28, used eight workers and took 520.43 s. A separate probe was killed
under memory pressure; that incident motivates restraint but does not prove
the gate's memory consumption or a speed improvement from fewer workers.

The gate command is pinned across the gate declaration, generated CI,
Makefile and generated catalog. The interview skip and draft details of
2026-10-29 settle a narrower remedy than changing those pins: a default
environment value inside the local verification runner.

## Terms

**Caller value:** an exported, non-empty `PYTEST_XDIST_AUTO_NUM_WORKERS`.
**Memory bound:** usable memory divided by 2 GiB (2,147,483,648 bytes),
rounded down, with a minimum of one worker. The reading is `hw.memsize` on
macOS and `MemTotal` from `/proc/meminfo` on Linux; `MemTotal` excludes
memory the kernel reserves, so a host with exactly 4 GiB installed may
derive one worker.

## Acceptance criteria

1. When no caller value exists and logical CPU count and physical memory are readable on macOS or Linux, gates launched by `scripts/verify_all.sh` inherit a worker default equal to the smaller of half the logical cores rounded down (minimum one) and the memory bound.
   *Refuted by:* an 8-core, 8 GiB fixture yields anything other than four, a 16-core, 4 GiB fixture exceeds two, or a one-core/sub-2-GiB fixture yields zero.

2. When a caller value exists, every launched gate inherits it unchanged, regardless of detected machine size.
   *Refuted by:* an explicit `8` becomes `4`, or any other non-empty value is rewritten or validated by this change.

3. When the caller exports an empty value, the runner treats it like an unset value for default selection.
   *Refuted by:* the same readable machine produces a default when unset but an empty environment value when explicitly empty.

4. If resource detection is incomplete, unavailable or malformed, the runner uses only valid positive readings to derive the default, leaving the variable unset when neither reading is usable, without making verification fail because detection failed.
   *Refuted by:* a valid CPU-only or memory-only bound is ignored, missing or invalid readings cause an arithmetic error or zero workers, or both failed readings prevent an otherwise passing gate from running.

5. While the default is applied, the runner preserves its existing gate execution and verdict behavior.
   *Refuted by:* an environment probe cannot see the default, a blocking failure becomes green, later gates stop running after a blocking failure, or an advisory failure becomes blocking.

6. While this change is implemented, the canonical pytest command and its pinned copies, hosted CI behavior, direct `make test` behavior and Stage-2 environment allow list remain unchanged.
   *Refuted by:* the implementation diff edits a command pin or the Stage-2 runner, or adds worker configuration outside `scripts/verify_all.sh`.

7. When implementation is verified, one complete four-worker run and one complete eight-worker run of the same suite revision are recorded under the machine verification lock with no competing local verification workload.
   *Refuted by:* either run is missing, overlapping, incomplete, uses different test/code contents or the wrong worker count, or lacks its date, commit, elapsed time and pytest outcome.

## Non-goals

- Optimising tests, proving a speedup, guaranteeing an absence of memory pressure, or selecting a universally optimal worker count.
- Capping direct pytest, direct `make test`, hosted CI or the kit probe; adding a machine lock or changing runner timeouts.
- New dependencies, a configurable sizing policy, Stage-2 environment forwarding or gate/doctrine changes.

## Protected areas

`decisions/gates.yaml`, `.github/workflows/ci.yml`, `Makefile` and
`docs/governance/gate-catalog.md` retain the command pins. `scripts/stage2.py`
and its environment allow list belong to the separate runner lane.

## Definition of Done

- `make verify` is green; the criterion ledger names the implemented tests.
- The implementation changes `scripts/verify_all.sh` and `tests/test_ci.py`; this folder's spec, plan and findings carry their own evidence. No ADR or other document moves.
- The pull request's file list demonstrates the protected areas are untouched.
- The pull request closes the local worker-cap work item (`coding-harness-l7sc`); its last commit carries `Closes-Bead: coding-harness-l7sc`.
- The paired isolated measurements name their commit and date in the plan and pull request body.

## Open decisions

None open. The existing bounded interview skip is the intent basis; no
maintainer answer is added here.

[DETAIL] Use integer floors, binary GiB, and each independently usable resource
bound; discard non-positive or non-integer readings. These make the recorded
half-core/memory policy deterministic without failing on an unknown machine.

[DETAIL] Set a two-hour phase-4 appetite, including tests, isolated runs and
repairs; stop when exhausted. Neither input sets an appetite, and this bounds
the small change without promising a runtime result. Bounded changes omit
phase 2b and an ADR.
