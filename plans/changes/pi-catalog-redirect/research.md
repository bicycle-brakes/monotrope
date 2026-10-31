---
title: "Research — pi-catalog-redirect"
status: draft
implementation_status: none
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-j2wb
owner: framework-architect
class: bounded
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
neighbours:
  - plans/changes/research-swarm/spec.md
  - plans/changes/pi-pin/spec.md
tags: [research]
---

# pi catalog redirect — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), by the
runner's GLM Flash route; the orchestrator's measured addendum closes its gaps.

Stage-2 call, 2026-10-30: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 773 files, 2729 commits, 12 rules.

## Runner exploration — 2026-10-30

Research complete. Here is the phase-1 result, ready to append to `plans/changes/pi-catalog-redirect/research.md`.

---

## What exists today

**Two catalog surfaces read `pi.dev`, with different redirect behavior.**

1. **The pinned-Pi bridge** — `collectCatalog` in `scripts/stage2_research_catalog.mjs:15` fetches the Go catalog from `https://pi.dev/api/models/providers/opencode-go` (default `catalogBaseUrl`, `scripts/stage2_research_catalog.mjs:16`, 24) plus metadata from `https://models.dev/api.json` (`metadataUrl`, line 17). It runs the pinned Pi's `ModelRuntime.refresh` in-process, but intercepts `globalThis.fetch` (`scripts/stage2_research_catalog.mjs:53-73`) and re-dispatches the one permitted GET with `redirect: "error"` and `credentials: "omit"` (`scripts/stage2_research_catalog.mjs:62-64`). The models.dev fetch uses the same options (`scripts/stage2_research_catalog.mjs:121-124`). Under the fetch contract, `redirect: "error"` makes fetch reject instead of following a 3xx, so a redirect from either source lands in `failed()` and is recorded as outcome `request-failed` (`scripts/stage2_research_catalog.mjs:43-48`); only status 200 is recorded as `ok` (`record()`, `scripts/stage2_research_catalog.mjs:34-42`). Even a followed redirect would fail today: the guard permits only requests whose origin equals `catalogBaseUrl`'s and whose pathname is exactly `/api/models/providers/opencode-go`, and exactly one request total (`scripts/stage2_research_catalog.mjs:54-58`) — any hop to another origin or pathname is aborted before I/O with "only one Go catalog request is permitted". The header comment states the intent: one actual GET, the shared deadline instead of Pi's four-second attempt timeout, second attempts aborted (`scripts/stage2_research_catalog.mjs:50-52`).
   - Consequence chain for the pi source: fetch rejects → Pi's `fetchWithRetry` sees a network error and retries (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/utils/management-http.js:21-52`), but each retry is aborted by the one-request guard → the error reaches `runtime.refresh`'s error list → `piState.ok = false` → the bridge returns `exit_code: 1`, reason `pi-refresh-failed` (`scripts/stage2_research_catalog.mjs:109-117`, 151-155). Python then refuses: `select_research_catalog` raises `ResearchCatalogError` (exit 1) when `exit_code != 0`, `pi.status != 200`, the runtime aborted, or runtime errors exist (`scripts/stage2_swarm.py:107-115`); `prepare_research` converts that into `runner.CallFailed("the Go catalog is unmeasured: …; no probe or research call starts.")` (`scripts/stage2_availability.py:1110-1121`). The bridge result itself still parses (`catalog_bridge` only raises on `OSError`, `ValueError`, `TimeoutExpired`, `scripts/stage2_availability.py:692-713`).
   - The models.dev source is non-fatal: a `request-failed` outcome becomes `capability_reason = "request-failed"` (`scripts/stage2_swarm.py:184-185`), free seats come out empty and the fixed slots are preserved (behavior pinned by `test_models_dev_failure_excludes_free_and_keeps_required_slots`, `tests/test_stage2_research_catalog.py:784-803`).

2. **The CLI discovery of the review loop's free stage** — `discover_free` (`scripts/stage2.py:2098-2199`) launches the pinned CLI `tools/pi/pi update --models` and then `pi --list-models` in one fresh scratch directory (`scripts/stage2.py:2121-2123`, 2169-2171; timeout `PI_DISCOVERY_SECONDS = 120`, `scripts/stage2.py:365-367`); a failed or timed-out refresh refuses the run (`scripts/stage2.py:2129-2133`). This path runs Pi natively: `requestCatalog` in the pinned source builds the same URL and calls `fetchWithRetry`, which calls plain `fetch` with no `redirect` option (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/remote-catalog-provider.js:56-67`; `management-http.js:28`) — Node's documented default is `redirect: "follow"`, so the CLI path follows redirects transparently today. Its retryable statuses are 408, 425, 429, 500, 502, 503, 504 (`RETRYABLE_STATUS_CODES`, `management-http.js:1`) — a redirect is neither retried nor surfaced as a status; fetch itself resolves it. Pi's own default catalog base is also `https://pi.dev` (`DEFAULT_CATALOG_BASE_URL`, `remote-catalog-provider.js:5`), with a four-hour cache that a forced refresh skips (`REMOTE_CATALOG_REFRESH_INTERVAL_MS`, `remote-catalog-provider.js:7`, 90-95) — the same four hours the declaration documents (`model-endpoints.yaml:436`).

**Why the redirect option plausibly exists.** The bridge header states the module's contract: no model operation, no user config, no credential file; fixed public sources, replaceable by loopback servers for offline contracts (`scripts/stage2_research_catalog.mjs:2-7`). The repository's other public fetcher, the free researchers' tool bridge, instead follows redirects but re-validates every hop against private addresses (`fetchPage`, `scripts/stage2_research_tools.mjs:192-213`, with `MAX_REDIRECTS`), and decodes DuckDuckGo's redirect wrappers (`resultDestination`, `scripts/stage2_research_tools.mjs:227-233`). So the tree today holds two postures: hop-validated following for web pages, outright refusal for the two catalog sources.

**Where the bridge is consumed.** `catalog_bridge` is called only from `prepare_research` (`scripts/stage2_availability.py:1111-1117`), i.e. `prepare-explore`/the research availability receipt; the selection state keeps `sources`, `candidates`, `models`, `models_store` and the capability fields (`scripts/stage2_availability.py:1129-1145`). The run side never refreshes: "The run never probes, refreshes the catalog, retries or swaps a seat" (`scripts/stage2_research_run.py:17`). A second, older redirect rule already exists and is about something else: a model definition may not redirect its declared Go origin — `baseUrl` must be `https://opencode.ai/zen/go/v1` exactly (`pi_reason` in `scripts/stage2_swarm.py:149-166`), tested as `test_preflight_free_definition_cannot_redirect_its_declared_go_origin` and `test_preflight_seat_candidate_definition_cannot_redirect_its_go_origin` (`tests/test_stage2_research_catalog.py:626-660`).

**Tests today.** `tests/test_stage2_research_catalog.py` runs the real pinned Pi against a loopback `Sources` harness whose handler answers JSON bodies with configurable statuses only (`tests/test_stage2_research_catalog.py:75-118`). Statuses 304, 404, 429, 500 are covered (`test_preflight_unsuccessful_pi_response_is_not_measured_empty_or_retried`, lines 402-408; metadata, 494-500); timeouts are tested with held requests (lines 411-425). No test exercises a 3xx on either source — the handler has no redirect branch, and the whole test file contains no 3xx case. That is a "not there", read from the complete file.

## Where it lives

- Bridge: `scripts/stage2_research_catalog.mjs` (`collectCatalog`, the fetch guard and both fetch calls).
- Selection/classification: `scripts/stage2_swarm.py` (`select_research_catalog`, `ResearchCatalogError`, `pi_reason`).
- Consumption/refusal: `scripts/stage2_availability.py` (`catalog_bridge`, `prepare_research`), `scripts/stage2.py` (`discover_free`, CLI path).
- Pinned source under test: `tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/remote-catalog-provider.js`, `dist/utils/management-http.js`; pin is `@earendil-works/pi-coding-agent` 1.2.0 (`tools/pi/package.json:8`).
- Rule text: `model-endpoints.yaml:433-449` (`free_stage`: forced live refresh, source `pi.dev`, four-hour cache, intermediary warning); the swarm contract: `plans/changes/research-swarm/spec.md` criteria 38 and 41 (fresh two-source record before every call; an unmeasurable Pi catalog exits 1 before any swarm call, stale-only must not stand in).
- Tests: `tests/test_stage2_research_catalog.py` (whole file), `tests/test_pi_contract.py`, `tests/test_model_endpoints.py` (catalog matches found by search, not read this session).

## What is unclear

- **The bead's exact motivation.** The tracker is the Dolt database under `.beads/` (house rule 2) and this session runs no commands; a text grep of `.beads/` for `pi-catalog-redirect` found no match. The bead `coding-harness-j2wb` description and the maintainer's observed failure (if any) are an open question for the interview. [GAP]
- **Whether a live redirect is actually happening.** Nothing in the tree records one: no findings or handover mentions a catalog redirect failure (searched; the newest handover, `docs/journal/handover/2026-10-29-three-lane-night.md`, has no catalog or redirect mention). Whether `pi.dev` or `models.dev` answers 3xx today is a live-network question this read-only phase cannot answer. [GAP — explore/observe, don't guess]
- **The exact error text** a redirect produces in `sources.pi.error` — the mechanism is stated by the fetch contract, the concrete `TypeError` string is unverified (no run observed).
- **Which behavior is wanted after the change** — follow with validation, re-home the base URL, or keep refusing but report distinctly — is a design decision; this research only records that the two surfaces diverge today (bridge refuses, CLI follows).
- Not read this session (found by search only): `tests/test_pi_contract.py`, `tests/test_model_endpoints.py`, `scripts/research_capture.py` beyond its `collectCatalog` driver (`scripts/research_capture.py:776-794`), Pi's `model-runtime.js` refresh internals.

## Which files a change would have to touch

- `scripts/stage2_research_catalog.mjs` — the redirect policy (`redirect: "error"` on both fetches), the one-request guard, and the `record()`/`failed()` outcome vocabulary.
- `tests/test_stage2_research_catalog.py` — the loopback handler needs a redirect branch before any new behavior is testable; new cases sit beside the status-parameterized tests (lines 402-408, 494-500).
- `scripts/stage2_swarm.py` — only if outcome classification or refusal wording changes; `request-failed` already flows through both the models.dev reason path and the pi hard-failure path unchanged.
- `scripts/stage2_availability.py` — `catalog_bridge`/`prepare_research` messages only if they change.
- `model-endpoints.yaml` — only if the documented `free_stage` source rule text changes.

## Proposed `neighbours:` header

Validated as tracked files (the format `given_neighbours` expects, `scripts/stage2_availability.py:654-660`; specimen: `plans/changes/red-first-pytest-failed/research.md:15-17`):

- `plans/changes/research-swarm/spec.md` — criteria 38 and 41 bind the fresh two-source catalog record and the exit-1 rule.
- `plans/changes/loop-until-clean/spec.md` — the forced-refresh discovery path and its refutations (lines 32-74, 122-133).
- `plans/changes/review-loop-deep-b/spec.md` — DL-B-8, the overlay `baseUrl` origin rule (redirect-adjacent catalog fields).
- `plans/changes/pi-pin/spec.md` — the Pi 1.2.0 pin and its contract suite.

## Orchestrator addendum — measured 2026-10-30 (closes the gaps above)

- **The live redirect happens.** `prepare-explore` for bead
  coding-harness-3g53 failed three times with `pi-refresh-failed` (2026-10-29
  23:16 UTC twice, 2026-10-30 11:00 UTC). Run alone with an empty `HOME`,
  the bridge reported `sources.pi.outcome: request-failed`, error
  `fetch failed`, and `pi_runtime.errors` naming "only one Go catalog request
  is permitted" (Pi's retry, refused by the guard).
- **The exact error.** The underlying cause of `fetch failed` is undici's
  `unexpected redirect`. Pi sends `accept: application/json` and
  `user-agent: pi/1.2.0 (darwin; node/v26.12.0; arm64)`.
- **What pi.dev answers.** With Pi's user agent,
  `https://pi.dev/api/models/providers/opencode-go?types=chat%2Cimage%2Cclassifier`
  answers `307` to the same URL plus `&pi-version=1.2.0`. That target answers
  `200`. Without Pi's user agent, the original URL answers `200` directly.
  The redirect parameter follows the user agent's version (`pi/1.3.0` gives
  `pi-version=1.3.0`).
- **Only the bridge is affected.** Pi's own CLI path follows redirects by
  fetch's default, so the review loop's discovery keeps working; `models.dev`
  answered `200` in the same run.
- **The bead's motivation** is this failure (bead coding-harness-j2wb,
  discovered from coding-harness-3g53).

