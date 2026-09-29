---
title: "ADR 0002 — One exclusive coordinator writes the tracker during parallel sessions"
category: adr
status: accepted
created: 2026-09-19
last_reviewed: 2026-09-22
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr]
---

# ADR 0002 — One exclusive coordinator writes the tracker during parallel sessions

* Status: accepted, superseded in part by ADR 0005 (2026-09-23) and ADR
  0006 (2026-09-27) · amends the session-entry rule "no session writes while
  another session runs" (AGENTS.md house rule 4)
* Review: accepted by the maintainer, 2026-09-22, with the changes of that
  review · Decider: maintainer · prepared by a framework-architect session
* Date: 2026-09-19 · accepted 2026-09-22
* Note, 2026-09-23: [ADR 0005](0005-workers-claim-their-own-bead.md)
  (accepted 2026-09-23) supersedes the exclusive writer and the read-only
  workers; its first reason, a single-writer store, was measured false
  that day (bead coding-harness-m34). The rules on stale or duplicate
  results and on the pilot's throwaway store stay in force.
* Note, 2026-09-27: [ADR 0006](0006-parallel-work-without-a-pilot.md)
  (accepted 2026-09-27) drops the M0 pilot, so the pilot's throwaway
  store, the W1 activation condition and the M0 validation lapse. The
  rules on stale or duplicate results stay and apply to coordinated runs,
  when there are any.

## Context

Today's house rule is strict and simple: **no session writes to the tracker
while another session runs.** The Omnigent-first target depends on a
coordinator that records accepted outcomes while its tracker-read-only
workers run — the old rule forbids exactly that. The
[target document](../architecture/2026-09-17-omnigent-first-target.md#tracker-ownership-and-activation)
proposes replacing the rule with an explicit permission; this ADR records it.
It is a runtime permission, not an interpretation of the existing rule.

## Decision Drivers

* Parallel workers need their accepted outcomes recorded without human
  bookkeeping between runs.
* The embedded Dolt store is a single-writer store; concurrent writers have
  never been proven here.
* A silently shared writer is the failure mode the old rule exists against.

## Considered Options

* **(a) One authorized, exclusive coordinator writes; workers stay
  read-only.**
* (b) Workers write directly — requires a supported concurrent mode, the full
  five-check protocol, backup/restore evidence and a reviewed rule change
  (that is W2, separately qualified, not this ADR).
* (c) No tracker writes during parallel sessions — the coordinator's outcomes
  would live outside Beads and the tracker would lie by omission.

## Decision

**(a)**, bounded exactly as the target document states:

* One lock mechanism (an OS-level exclusive writer lock) is used by every
  coordinator process, and exactly **one** of them holds it at a time. The
  holder writes from the designated main checkout via `tools/bd` — never
  bare `bd`.
* A second coordinator **fails closed**: it may not write. A replacement must
  prove the old writer stopped and acquire the lock before reconciling state.
  An elapsed timeout alone does not authorize concurrent ownership.
* Run and attempt IDs reject late or duplicate results after reassignment.
* Workers receive bounded snapshots and stay tracker-read-only.
* The tracker export (`scripts/render_beads_export.py`, held by the
  `export-identity` gate) stays with the one writer: the lock holder renders
  it, nobody else.
* The harness's live store is never the pilot store: the pilot runs in a
  throwaway repository with its own tracker.
* This permission activates **only** with enforced exclusive writer ownership
  (W1) proven; until then the no-writes rule stays in force.

## Consequences

* AGENTS.md house rule 4 gains the coordinator exception, worded as above,
  activated together with W1's enforcer.
* Direct concurrent writers remain out of scope until W2 qualifies them; a
  successful stress-test sample does not promote embedded mode to
  multi-writer.
* [Beads mode documentation](https://github.com/gastownhall/beads/blob/main/docs/architecture/dolt.md)
  remains the design basis; pin-specific behavior still needs testing.

## Validation

* The M0 controls "second coordinator or stale result" and "retry or
  cancellation" pass; the protocol is committed.
* The writer lock is observed held exactly once during a two-worker run.
