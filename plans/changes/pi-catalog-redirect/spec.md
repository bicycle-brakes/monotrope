---
title: "Spec — pi-catalog-redirect"
status: draft
implementation_status: partial
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-j2wb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, pi, catalog]
class: bounded
appetite: 1
adr_files: []
neighbours:
  - plans/changes/research-swarm/spec.md
  - plans/changes/pi-pin/spec.md
---

# Spec — pi-catalog-redirect

The research preflight accepts the catalog's single pinned-version redirect
without permitting other destinations or retries (bead `coding-harness-j2wb`).
Research: `research.md`; approved boundary and one-hour appetite:
`decisions.md`, "SKIP · interview" and "Details for the draft".

## Problem

On 2026-10-30 the orchestrator measured Pi 1.2.0's catalog request receiving
307 to the same URL with `pi-version=1.2.0` added, then 200. The bridge's
redirect refusal instead produced `request-failed` and `pi-refresh-failed`,
preventing research preflight. Pi's retry was blocked by the one-request
guard. The measured addendum in `research.md` records the cause and three
failed preparations on 2026-10-29/30; the CLI discovery path already follows
the redirect, and models.dev answered 200.

## Terms

**Admitted redirect:** a 301, 302, 303, 307 or 308 with a Location that resolves
against the original request to the same origin and pathname, preserves all
original query name/value pairs including multiplicity, and adds exactly one
`pi-version` equal to the repository's pinned Pi version. The original has no
`pi-version`; the target has no credentials or fragment. Query ordering and
encoding of equivalent values do not matter. Relative and absolute Locations
are eligible under the same conditions.

## Acceptance criteria

1. When the Pi catalog returns an admitted redirect followed by a valid 200 catalog, the bridge yields a successful fresh pinned-Pi snapshot usable by the existing selector.
   *Refuted by:* the loopback version redirect fails preflight, the version is hard-coded independently of the pin, or fresh catalog entries are lost.
2. If an initial Pi redirect is not admitted, the bridge refuses it before contacting its target with `sources.pi.outcome: redirect-refused` and an error identifying the Location or its absence.
   *Refuted by:* a changed origin, path, existing query value or multiplicity, wrong/duplicate version, extra parameter, credentials, fragment, missing or invalid Location reaches a target or is accepted as an empty catalog.
3. If the admitted target redirects again, the bridge fails with `sources.pi.outcome: redirect-refused` without a third catalog GET and identifies the admitted target in the error.
   *Refuted by:* a third request occurs, preflight succeeds, or the second redirect becomes an indistinguishable ordinary request failure.
4. When the bridge issues an admitted redirect GET, the source record preserves the requested `url` and adds `redirected_to` and `redirect_status`, with any received final response represented by the existing status, body, timestamp and digest fields.
   *Refuted by:* the initial URL is overwritten, either hop field is missing, the digest describes the redirect body, selection drops the hop evidence, or a failed followed request loses the hop fields.
5. If the catalog request or its admitted hop fails, Pi's retry attempts cause no further network requests beyond that original GET and its at-most-one admitted hop.
   *Refuted by:* a direct failure sends two catalog GETs, a followed failure sends three, or a retry overwrites the first refusal evidence.
6. While the admitted hop is pending, the original shared deadline still bounds the refresh and a timeout remains an unmeasured Pi catalog failure.
   *Refuted by:* the hop gets a fresh deadline, a third request starts, or a held hop produces a successful or measured-empty snapshot.
7. When models.dev redirects or otherwise fails, its existing redirect refusal and nonfatal capability-failure behavior remain in effect.
   *Refuted by:* its redirect target is fetched, fixed seats are lost solely for that failure, or free seats are selected without capability evidence.
8. When Pi returns a valid catalog directly with 200, preflight retains its existing snapshot and credential-free behavior without redirect fields.
   *Refuted by:* an extra catalog GET or model subprocess occurs, credentials are read or sent, ordinary selection changes, or hop fields claim a nonexistent redirect.

## Non-goals

- Generic redirect following, changes to models.dev fetching, Pi CLI discovery, model selection or model-call routing.
- Moving the catalog source, updating the Pi pin, adding retries, changing the deadline or admitting stale catalogs.
- Gate, doctrine, endpoint declaration or architecture-decision changes. Phase 2b does not run for this bounded change.

## Protected areas

`tools/pi/`, `scripts/stage2.py`, `scripts/stage2_swarm.py`,
`scripts/stage2_availability.py`, `model-endpoints.yaml`, `docs/adr/`,
`decisions/`, `prompts/`, `templates/`, `provenance.yaml` and harness
configuration stay unchanged: the existing bridge and its test harness suffice.

## Definition of Done

- The offline loopback contracts pass with the real pinned runtime; `make verify` is green in the runner.
- Companion documents: this change's `spec.md`, `plan.md` and runner-owned `findings.md`; no design or ADR is due.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes `coding-harness-j2wb`; its last commit carries `Closes-Bead: coding-harness-j2wb` (runner/orchestrator responsibility).
- Special live runs: none required; the measured incident is in research and automated proof uses local servers.

## Open decisions

None open. The maintainer's approved remedy is recorded in `decisions.md`;
no answer or ADR decision is added here.

[DETAIL] Compare resolved query pairs as a multiset, requiring an absent-then-single
version; reject credentials and fragments because the version addition must be
the sole change. This admits harmless query reordering without widening targets.

[DETAIL] Both requests run with `redirect: "manual"`, and a second redirect is
recognised by its status (301, 302, 303, 307 or 308), never followed, and
refused as `redirect-refused` naming the admitted request URL, not the second
Location (review rows L1-1, L1-7, L2-1; this supersedes the wording of
`redirect: "error"` in `decisions.md`, which records the answer as it was
given). Any other status, a 300 with a Location included, is an ordinary
answer: it is not followed and is recorded as `http-error` (review row L2-2).
Other network failures keep their existing failure classification.
