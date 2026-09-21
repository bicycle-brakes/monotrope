# ADR 0003 — The public scan names tools, never customers, employers or secrets

* Status: proposed · amends D-17 (public readiness) at its naming boundary
* Review: pending (maintainer) · Deciders: framework-architect, maintainer
* Date: 2026-09-19

## Context

D-17 decided public readiness in the interview of 2026-09-16
([§9.1](../architecture/target-architecture.md#91-outcomes-of-the-interview-2026-09-16)):
Apache-2.0, an onboarding page, and the denylist scan as a kit gate **from
now on, not at the switch** — the template switch itself happens only when
the Leerprobe reaches 95 % in both instances, the first full run is
measured, and Q13 has been passed once by someone who was not there. The
scan's wording left a corner
open — the harness legitimately names its own tooling (Omnigent, LikeC4), and
a denylist that rejects every capitalized name would flag the harness
itself. The
[target document](../architecture/2026-09-17-omnigent-first-target.md#outcome-and-boundaries)
amends the boundary; this ADR records the amendment and keeps D-17's timing
untouched.

## Decision Drivers

* The public corpus must never carry customer, employer or vendor-internal
  identifiers — measured, not assumed.
* The harness must be able to name the tools it is built on; a rule that
  forbids its own architecture reads as a defect and gets ignored.
* Model selection stays in routing configuration and out of doctrine.

## Considered Options

* **(a) The scan permits an explicit, reviewed allowlist of tool names;
  everything else follows D-17's denylist.**
* (b) Keep the scan name-blind and exempt the tool names by comment.
* (c) Drop the naming check entirely and rely on review.

## Decision

**(a)**:

* The public scan **permits exactly the documented tool names** the harness
  is built on (currently: Omnigent, LikeC4). The allowlist is part of the
  scan configuration and changes only in a reviewed change.
* The scan **rejects** customer identifiers, employer identifiers and
  secrets — unchanged from D-17.
* Model selection stays in routing configuration (`model-endpoints.yaml`,
  instance routing files); doctrine never names a vendor beyond the tool
  allowlist.
* This amendment does not postpone any public-readiness work: the template
  switch remains the separate D-17 event with its own criteria.

## Consequences

* New tools enter the harness with a one-line allowlist change plus the
  reason — reviewed, dated, in the same change that introduces the tool.
* A false-positive scan finding is fixed by correcting the allowlist or the
  text, never by weakening the scan.
* The scan runs as a gate over the whole tracked tree before publication and
  stays in CI afterwards.

## Validation

* Known-bad fixtures (a customer name, an employer name, a fake secret) fail
  the scan; the documented tool names pass it.
* The scan's allowlist diff is reviewed in the change that edits it.
