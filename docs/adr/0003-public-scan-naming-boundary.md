---
title: "ADR 0003 — The public scan names tools, never customers, employers or secrets"
category: adr
status: accepted
created: 2026-09-19
last_reviewed: 2026-09-22
updated: 2026-09-29
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-19"}
review: {status: approved, approved_by: maintainer, approved_at: 2026-09-22}
tags: [adr]
---

# ADR 0003 — The public scan names tools, never customers, employers or secrets

* Status: accepted · amends D-17 (public readiness) at its naming boundary
* Review: accepted by the maintainer, 2026-09-22, with the changes of that
  review · Decider: maintainer · prepared by a framework-architect session
* Date: 2026-09-19 · accepted 2026-09-22

## Context

D-17 decided public readiness in the interview of 2026-09-16
([§9.1](../architecture/target-architecture.md#91-outcomes-of-the-interview-2026-09-16)):
Apache-2.0, an onboarding page, and the denylist scan as a kit gate **from
now on, not at the switch** — the template switch itself happens only when
the Leerprobe reaches 95 % in both instances, the first full run is
measured, and Q13 has been passed once by someone who was not there. D-17
worded the scan as "no customer, employer, vendor names in the harness".
Taken literally, "vendor names" forbids the harness its own architecture:
it names Claude Code, Codex, Beads, Dolt, GitHub, Omnigent and LikeC4 on
almost every page, and a scan that flags every one of them gets ignored.
The
[target document](../architecture/2026-09-17-omnigent-first-target.md#outcome-and-boundaries)
amends the boundary; this ADR records the amendment — **it narrows D-17's
"vendor names" to vendor-internal identifiers** — and keeps D-17's timing
untouched.

## Decision Drivers

* The public corpus must never carry customer, employer or vendor-internal
  identifiers — measured, not assumed.
* The harness must be able to name the tools it is built on; a rule that
  forbids its own architecture reads as a defect and gets ignored.
* Model selection stays in routing configuration and out of doctrine.

## Considered Options

* **(a) The scan is a denylist of explicit patterns — customer identifiers,
  employer identifiers, secrets — plus a small, reviewed allowlist for the
  exceptions a pattern would otherwise hit.**
* (b) An allowlist of the tool names the harness is built on; every other
  proper name is rejected (the 2026-09-19 draft of this ADR).
* (c) Keep the scan name-blind and exempt the tool names by comment.
* (d) Drop the naming check entirely and rely on review.

## Decision

**(a)** — (b) was the draft; the maintainer's review of 2026-09-22 replaced
it, because a two-entry allowlist (Omnigent, LikeC4) would have rejected the
tools named throughout the harness itself:

* The public scan **rejects** by explicit denylist patterns: customer
  identifiers, employer identifiers and secrets. A product or tool name is
  not a pattern; the harness may name the tools it is built on without
  listing them.
* The **allowlist holds only exceptions** a denylist pattern would otherwise
  hit (a legitimate term that resembles a rejected identifier). It is part
  of the scan configuration and changes only in a reviewed change, with the
  reason beside the entry.
* Model selection stays in routing configuration (`model-endpoints.yaml`,
  instance routing files); doctrine names tools, never a vendor's internal
  identifiers.
* This amendment does not postpone any public-readiness work: the template
  switch remains the separate D-17 event with its own criteria.

## Consequences

* New tools enter the harness without touching the scan. A new denylist
  pattern, or an allowlist exception, arrives with its reason — reviewed,
  dated, in the same change that needs it.
* A false-positive scan finding is fixed by an allowlist exception or by
  correcting the text, never by weakening a pattern.
* The scan runs as a gate over the whole tracked tree before publication and
  stays in CI afterwards.

## Validation

* Known-bad fixtures (a customer name, an employer name, a fake secret) fail
  the scan; the tracked tree of this repository, which names its tools on
  almost every page, passes it.
* The scan's allowlist diff is reviewed in the change that edits it.
