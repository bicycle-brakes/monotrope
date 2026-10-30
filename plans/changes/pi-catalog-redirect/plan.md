---
title: "Plan — pi-catalog-redirect"
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
tags: [plan, pi, catalog]
---

# Plan — pi-catalog-redirect

```text
For you:     Research preflight accepts Pi's single pinned-version catalog redirect and keeps other redirects refused.
Done when:   Offline pinned-Pi tests prove the accepted hop, refusal boundaries and audit record, and make verify is green.
Appetite:    1 hour of phase 4, repairs included — a stop, not an estimate.
Not now:     Generic redirects, models.dev changes, Pi upgrades, CLI discovery, retries or routing changes.
Pre-mortem:  suppose it failed: most likely because target validation admitted a query change beyond the pinned version.
Starts unless you say stop.
```

## Scope and baseline

Implement spec criteria 1–8 and the approved bounded remedy (bead
`coding-harness-j2wb`). At `fd84ea8b` on 2026-10-30, `findings.md` contains
only the draft invocation, no phase-2a rows. Class `bounded` requires neither
design nor ADR. Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`;
no Stage-1 fallback is recorded. `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent at this baseline; use the
phase-3 prompt's form and report the validator as unavailable.

## Build sequence

1. Extend `Sources` and its handler in `tests/test_stage2_research_catalog.py`
   with per-request-path responses and Location headers, recording both query
   forms. Use an independently counted second loopback server for the foreign
   origin case; never contact public hosts. Preserve current fixture defaults,
   credential/subprocess traps and the event-controlled deadline helper.
2. In `scripts/stage2_research_catalog.mjs`, keep the Pi-call guard outside
   redirect handling. Fetch the initial request with `redirect: "manual"`.
   Validate redirect status, Location resolution, origin/path, absent userinfo
   and fragment, and query multiset equality after removing exactly one new
   `pi-version` equal to the already validated manifest pin. Reject missing or
   malformed Locations and all other target changes before I/O. On acceptance
   issue exactly one GET through `originalFetch`, with `redirect: "manual"`,
   `credentials: "omit"`, the original headers and the same controller signal.
   Do not route the internal hop through `globalThis.fetch` or increment the
   Pi-call counter for it. Correct the comment's one-actual-GET wording.
3. Preserve `sources.pi.url`; set `redirected_to` to the resolved target and
   `redirect_status` to the initial status before the admitted GET. Record only
   the final response through `record()`; keep hop fields on HTTP/network
   failure. Classify initial policy refusals and a follow-up fetch's unexpected
   redirect as `redirect-refused` with bounded diagnostics (Location or its
   absence for the first, admitted URL for the second). Do not relabel other
   network errors. Preserve timeout precedence, `pi-refresh-failed`/exit 1 and
   Pi's retry guard so retries neither issue I/O nor replace first evidence.
4. Add the ledger's tests: admit all five statuses with relative and absolute
   targets, query reordering and duplicate preserved original pairs; refuse
   altered origin/path/query pairs, duplicate/incorrect/preexisting versions,
   extra parameters, credentials, fragments and missing/malformed Locations.
   Count requests at both servers, not only selected results. Test second
   redirects, followed HTTP/network failures, retained audit fields/digest
   through `select()`, direct compatibility and metadata redirect refusal.
   *Not reachable through the harness (review row L4-1, 2026-10-30):* Pi's
   pinned client sends the catalog request with one query pair and no
   `pi-version`, so an admitted target preserving *duplicated* original
   pairs and a refused *preexisting* version cannot be driven end to end;
   the multiset comparison and the `original.some(... "pi-version")` refusal
   cover them in the code, and the tests hold every case Pi can send.
   For the deadline case hold only the versioned request, after the initial
   redirect; adapt the event marker so it fires once that hop has arrived,
   without wall-clock sleeps or resetting the bridge's single timer.
5. Run the commands below. Demonstrate the new accepted-hop test red on baseline
   bridge code and green after the fix; keep existing refusal contracts green.
   Remove ledger markers only when the named tests exist, and record phase-4
   time and evidence through the runner.

## Files and limits

- `scripts/stage2_research_catalog.mjs` — implement the single validated Pi hop and its audit/refusal record; leave metadata fetching unchanged.
- `tests/test_stage2_research_catalog.py` — extend the loopback fixture and add the named offline contracts, retaining existing top-level test names.
- `plans/changes/pi-catalog-redirect/spec.md` — update implementation status as work advances without changing settled criteria.
- `plans/changes/pi-catalog-redirect/plan.md` — update status, ledger markers and measured phase-4 time.
- `plans/changes/pi-catalog-redirect/findings.md` — runner-owned attempt, red/green and verification evidence, preserving prior text.

No deletions. Leave `research.md` and `decisions.md` unchanged. Do not edit
`tools/pi/`, Python consumers, endpoint declarations, gates, doctrine,
credentials, routing, caches or other change folders. The runner owns generated
`plans/INDEX.md` updates; the attempt must not edit it. No held path needs a
bootstrap edit by the orchestrator.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2_research_catalog.py -q
python3 scripts/check_interview_minimums.py --change pi-catalog-redirect
python3 scripts/check_research_handoff.py --change pi-catalog-redirect
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect — an admitted status or equivalent relative/absolute target fails fresh selection
- 2: tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect — a forbidden target receives a GET or refusal evidence is absent
- 3: tests/test_stage2_research_catalog.py::test_preflight_refuses_a_second_catalog_redirect — a third GET occurs or redirect-refused/target evidence is lost
- 4: tests/test_stage2_research_catalog.py::test_preflight_redirect_record_preserves_request_and_final_evidence — original URL, hop fields or final-body digest is wrong in bridge or selection
- 4: tests/test_stage2_research_catalog.py::test_preflight_redirect_failure_keeps_hop_evidence — a followed HTTP/network failure loses hop fields or is classified as success
- 5: tests/test_stage2_research_catalog.py::test_preflight_unsuccessful_pi_response_is_not_measured_empty_or_retried — a direct failure causes another catalog GET
- 5: tests/test_stage2_research_catalog.py::test_preflight_redirect_failure_does_not_retry — Pi sends another request or replaces the initial refusal record
- 6: tests/test_stage2_research_catalog.py::test_preflight_redirect_hop_uses_shared_deadline — a held versioned GET resets the deadline or yields a usable snapshot
- 7: tests/test_stage2_research_catalog.py::test_preflight_metadata_redirect_stays_refused — the metadata target is contacted or fixed/free selection violates the existing asymmetry
- 7: tests/test_stage2_research_catalog.py::test_preflight_metadata_http_failure_keeps_fixed_slots — a metadata HTTP error drops fixed seats or admits free seats
- 8: tests/test_stage2_research_catalog.py::test_preflight_uses_fresh_pinned_go_snapshot_without_cache_date — direct fresh selection, credential/subprocess traps or request counts regress
- 8: tests/test_stage2_research_catalog.py::test_preflight_direct_catalog_has_no_redirect_fields — a direct 200 claims a redirect
- 1: tests/test_stage2_research_catalog.py::test_the_bridge_takes_the_admitted_version_from_the_pin_not_a_literal — the bridge carries the pinned version as a literal (row L1-5)
- 2: tests/test_stage2_research_catalog.py::test_preflight_records_a_300_with_location_as_an_unfollowed_http_error — a 300 with a Location is followed or refused as a redirect (rows L2-2, L5-3)

## Time used

2026-10-30 13:01:38–13:51:23 UTC, 2985 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 13:51:28–14:15:28 UTC, 1440 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
