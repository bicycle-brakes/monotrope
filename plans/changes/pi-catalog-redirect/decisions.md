---
title: "Decisions — pi-catalog-redirect"
status: draft
implementation_status: none
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-j2wb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# pi-catalog-redirect — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: the change touches the catalog
bridge `scripts/stage2_research_catalog.mjs` and its tests; no gate, ADR,
doctrine text or `scripts/stage2.py` changes.

## SKIP · interview

status: skipped
reason: the maintainer approved the remedy on 2026-10-30 (~11:20 UTC, one hour, bounded, lane C) as put to them: allow exactly one redirect, only to the same origin and path, and only when the sole change is an added `pi-version` equal to the pinned Pi version; record the redirect in the result. The cause is measured (research.md, orchestrator addendum); no question remains that only the maintainer can answer.

## Details for the draft

[DETAIL] **One redirect, strictly shaped.** The first catalog GET uses
`redirect: "manual"`. A 301, 302, 303, 307 or 308 whose `Location` resolves
to the same origin and path, with the same query parameters plus exactly
`pi-version=<pinned version>`, is followed by one second GET with
`redirect: "error"`. Any other redirect is a failure with outcome
`redirect-refused`, naming the location. Reason: pi.dev's redirect carries
only the version (measured), and the bridge's contract is fixed public
sources with no wandering.

[DETAIL] **Pi still sees one request.** The guard keeps counting Pi's calls,
and Pi's retry stays refused; the redirect hop is the bridge's own second
I/O inside that one call. Reason: the guard exists so the shared deadline,
not Pi's retry loop, bounds the refresh.

[DETAIL] **The record names the hop.** `sources.pi` keeps the requested
`url` and adds `redirected_to` and `redirect_status` when a hop was
followed. Reason: the selection state keeps `sources`, so an audit sees why
the body came from another URL.

[DETAIL] **`models.dev` is unchanged.** It answered 200 in the same run;
its `redirect: "error"` stays. Reason: no measured need, smallest change.

[DETAIL] **The loopback harness gets a redirect branch.** The tests serve a
307 to the versioned path, a 307 elsewhere (another path, another origin, a
different version, an extra parameter), and a second hop, and assert
followed, refused and refused. Reason: research.md found no 3xx case in the
test file.
