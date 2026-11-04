---
title: "Research — pi-catalog-move"
status: draft
implementation_status: none
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-vku6
owner: framework-architect
provenance: human-written
tags: [research]
---

# pi catalog move — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-04: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 887 files, 3249 commits, 12 rules.

## Runner exploration — 2026-11-04

Research complete. Here is the phase-1 result, ready to append to `plans/changes/pi-catalog-move/research.md`.

---

## Runner exploration — 2026-11-04

### What exists today

**The change folder holds a skeleton, and its bead is unreadable from this worktree.** `plans/changes/pi-catalog-move/research.md` is the frontmatter-only skeleton (frontmatter names bead `coding-harness-vku6`, `provenance: human-written`, body says "this file is empty until it has run"); `plans/INDEX.md:267` lists only this one artefact for the change. The folder was opened by the branch's commit titled `chore(pi-catalog-move): open the change folder (bead coding-harness-vku6)` (commit `0dae1403`, read from the worktree's git status at session start; its commit body was not read — this phase runs no commands). The bead's description, status and links live in the tracker, which is the Dolt database under `.beads/` transported via `refs/dolt/data` (AGENTS.md, house rule 2); this worktree's `.beads/` contains only configuration and hooks (`.beads/config.yaml`, `.beads/README.md`, `.beads/metadata.json` — no database), and a text search of the whole worktree for `vku6` and `pi-catalog-move` matches only the change's own skeleton and the generated index. So **what "move" names is not recorded anywhere in the tracked text of this worktree** — it is the interview's first question. [GAP]

**The tree itself points at the catalog as pending work in three places.** These statements exist today; whether bead `coding-harness-vku6` is their execution is unknown:

- `plans/changes/go-access-point/spec.md` (Non-goals): "The general model registry, phase and model routing, the catalog sources (`pi.dev`, `models.dev`) and their redirect handling: this change is the Go address part of that future registry, not another model list" (its `decisions.md`, detail "The catalog sources (pi.dev, models.dev) are out of scope", adds: "the model registry (bead coding-harness-wq1m) will take them up").
- `docs/adr/0024-one-access-policy-for-opencode-go.md` (Decision Drivers): "The Go address component must fit the coming provider/model registry"; (Decision): the chosen proposal "fits the future central registry without another model list".
- `plans/changes/explorer-reviewer-agents/decisions.md` (answer of 2026-11-01): the pinned sub-agent models were chosen "accepting that the registry (bead coding-harness-wq1m) will later take these choices over".

The direct predecessor also fenced the topic off: `plans/changes/pi-catalog-redirect/spec.md` (Non-goals) explicitly excluded "Moving the catalog source, updating the Pi pin, adding retries, changing the deadline or admitting stale catalogs" from that change. Its `decisions.md` statement (per its own spec's closing note) that the catalog sources are "where the catalog comes from" was the recorded reason for that fence.

**Two catalog surfaces read `pi.dev` today, with one shared source contract and divergent redirect handling.** Both were mapped by the predecessor research and re-read in their current, merged state this session:

1. **The research preflight bridge** — `collectCatalog` in `scripts/stage2_research_catalog.mjs:19`. Defaults: `catalogBaseUrl = "https://pi.dev"` (line 20) and `metadataUrl = "https://models.dev/api.json"` (line 21); the Pi source URL is `/api/models/providers/opencode-go` on that base (`sources.pi`, line 28; `PROVIDER = "opencode-go"`, line 12). The fetch guard (lines 95–101) admits only a GET whose origin equals `catalogBaseUrl`'s and whose pathname is exactly `/api/models/providers/${PROVIDER}`, exactly one runtime-initiated request — any Pi retry is aborted before I/O ("only one Go catalog request is permitted"). Since the merged `pi-catalog-redirect` change, both GETs run `redirect: "manual"` (lines 110–112, 123–125): an admitted redirect (same origin and path, credential- and fragment-free, query multiset preserved, exactly one added `pi-version` equal to the pin read from `tools/pi/package.json` — `admittedTarget`, lines 58–86; the pin is `@earendil-works/pi-coding-agent` `1.2.0`, `tools/pi/package.json:8`, checked against the installed version in `pi()`, lines 148–156) is followed once through the saved `originalFetch`; any second redirect is refused by status (`REDIRECT_STATUSES`, line 13; lines 126–133) and recorded as outcome `redirect-refused` (lines 136–141). Only status 200 records `ok` (`record`, lines 38–46); other failures are `request-failed`/`timeout` (`failed`, lines 47–52). `models.dev` is fetched separately with `redirect: "error"` and is non-fatal (lines 192–204; a failed metadata read only empties the free pool). Exit code 0 requires Pi ok, outcome `ok`, status 200 and a stored provider entry; otherwise the reason is `pi-refresh-failed` or `pi-timeout` (lines 224–232). One shared 60-second deadline bounds everything (`deadlineMs`, line 22; the timer, lines 205–212).

2. **The review loop's CLI discovery** — `discover_free` (`scripts/stage2.py:2224`) runs the pinned wrapper `pi update --models` and then `pi --list-models` in one fresh scratch HOME/agent directory (`PI_DISCOVERY_SECONDS = 120`, `scripts/stage2.py:375`), refusing the run on a failed or timed-out refresh (lines 2252–2265) — a stale cache is never listed. Before anything is activated it loads the one address record and fails closed without it (`stage2_go.load_address_policy`, lines 2236–2241); each Go row of the fetched store is assessed against that policy during overlay activation, a path move on the recorded host kept as a printed notice (`activate_overlay`, called at line 2267; the assess/notice block, lines 2099–2106), and `check_overlay` (lines 2133–2210) re-validates the activated configuration offline through the real pinned runtime. This path runs Pi natively: `requestCatalog` in the pinned source (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/remote-catalog-provider.js:56-67`) builds `/api/models/providers/<provider>` on `DEFAULT_CATALOG_BASE_URL = "https://pi.dev"` (line 5) and calls `fetchWithRetry` with no `redirect` option, so Node follows redirects by default (the measured consequence: pi.dev's 307 version redirect works on this path and broke only the bridge — the measured addendum of `plans/changes/pi-catalog-redirect/research.md`). The four-hour cache (`REMOTE_CATALOG_REFRESH_INTERVAL_MS`, line 7) is skipped by a forced refresh (lines 87–95); the same default backs `withPersonalizedCatalog` (line 148).

**The bridge has exactly one caller and the run side never refreshes.** `catalog_bridge` (`scripts/stage2_availability.py:748`) shells node on the helper with loopback-replaceable options; its only caller in the tree is `prepare_research` (`scripts/stage2_availability.py:1176-1183`), which hands the result to `select_research_catalog` together with `address=go_policy(runner, root)` (`go_policy`, `scripts/stage2_availability.py:414`). `select_research_catalog` (`scripts/stage2_swarm.py:92`) refuses with `ResearchCatalogError` (class at line 30) when the bridge failed, the version is not the expected pin, the status is not 200, the runtime aborted or errored, or the provider is missing from `models_store` (lines 112–122); since the merged `go-access-point` change its `pi_reason` (lines 143–171) classifies each candidate against the one address record — an absent base resolves from `address.default_base` or is skipped as `no-recorded-base`, a foreign destination fails `stage2_go.url_problem` and refuses the candidate alone — and the old exact-`/zen/go/v1` origin rule is gone from it. The run side's contract statement is `scripts/stage2_research_run.py:17`: "The run never probes, refreshes the catalog, retries or swaps a seat." (The predecessor research's citation of old tests `test_preflight_free_definition_cannot_redirect_its_declared_go_origin` and `test_preflight_seat_candidate_definition_cannot_redirect_its_go_origin` at `tests/test_stage2_research_catalog.py:626-660` describes the pre-go-access-point state; whether those exact tests survive in the current file was not re-verified this session.)

**The declaration and doctrine record the catalog as a live intermediary.** `model-endpoints.yaml`'s `free_stage` rule (lines 482–502: provider `opencode-go`, `id_suffix: "-free"`, dated excludes, `input: implementation-diff`) selects membership fresh per run from "a forced live catalog refresh (`pi update --models`) before `pi --list-models`"; the entry's `bemerkung` states "the catalog's source is `pi.dev`, which Pi caches for four hours — the forced refresh skips that cache — and being an intermediary it does not measure what Go actually bills" (lines 541–546). The swarm contract holds this in criteria 38 and 41 of `plans/changes/research-swarm/spec.md` (fresh two-source record with per-source UTC time and digest before any swarm call; an unmeasurable Pi catalog exits 1 before any call, stale-only must not stand in). ADR 0021 decides the live refresh itself ("Refresh the catalog live before each fresh run", `docs/adr/0021-review-swarms-until-clean.md:63`; "The live Pi catalog is an intermediary rather than Go's …", line 184 — both read as grep excerpts, not the full ADR). `docs/WORKFLOW.md:826-838` states the neighbouring built slice: every runner-controlled Go launch reads the `adresse` record on the `opencode-go` entry ("no separate approval per documented same-host path move, and no catalog refresh ever writes the record by itself") — that record (`model-endpoints.yaml:509-515`, host `opencode.ai`, per-wire-API `basis` with `quelle`/`gelesen`) is the address part ADR 0024 and the merged `go-access-point` change built, implemented as `scripts/stage2_go.py` (module docstring lines 1–24: "The record is data, never a code default … no literal base, host or cached policy exists in this module").

**Tests that hold the catalog today.** `tests/test_stage2_research_catalog.py` runs the real pinned Pi against a loopback `Sources` harness (class at line 64; `held_collect`, line 264; the node invocation passes `catalogBaseUrl`/`metadataUrl` overrides, lines 243–249) and, since `pi-catalog-redirect`, carries the redirect suite: the pin-not-literal guard `test_the_bridge_takes_the_admitted_version_from_the_pin_not_a_literal` (line 1334), `test_a_redirected_request_cannot_also_be_held` (line 1346), the models.dev refusal case (lines 1300–1312) and the hop-header assertion (comment at line 1056: "pi.dev's redirect depends on the user agent, so the hop sends the original headers"). The capture harness passes the same options (`scripts/research_capture.py:809-813`). Searching that test file for the literals `pi.dev`/`models.dev` found only comments and behavior assertions — **not found**: no test pins the bridge's production default URLs; the defaults are pinned by no automated contract this search could see (the file was searched, not read line by line — a complete read could still hide a pin phrased differently).

### Where it lives

- Bridge and its redirect policy: `scripts/stage2_research_catalog.mjs` (`collectCatalog`, the fetch guard, `admittedTarget`, `RedirectRefused`).
- Selection and refusal: `scripts/stage2_swarm.py` (`ResearchCatalogError`, `select_research_catalog`, `pi_reason`, `validate_research_free_policy`).
- Consumption and the address policy: `scripts/stage2_availability.py` (`catalog_bridge`, `go_policy`, `prepare_research`), `scripts/stage2_go.py` (the whole policy module).
- CLI discovery and overlay: `scripts/stage2.py` (`discover_free`, `activate_overlay`, `check_overlay`, `parse_catalog`, `PI_DISCOVERY_SECONDS`, `PI_PACKAGE`).
- Pinned Pi source under test: `tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/remote-catalog-provider.js` (`DEFAULT_CATALOG_BASE_URL`, `requestCatalog`, `REMOTE_CATALOG_REFRESH_INTERVAL_MS`, `withRemoteCatalog`, `withPersonalizedCatalog`); pin `1.2.0` in `tools/pi/package.json:8`.
- Declaration and doctrine: `model-endpoints.yaml` (`free_stage` 482–502, `adresse` 509–515, catalog-source sentences in `bemerkung` 541–546), `docs/WORKFLOW.md` (address-record paragraph 826–838; stage-2 catalog statements at 992–993, 1048, 1410–1417), `docs/adr/0021-review-swarms-until-clean.md`, `docs/adr/0024-one-access-policy-for-opencode-go.md`.
- Tests: `tests/test_stage2_research_catalog.py` (whole file), `tests/test_stage2.py` (pin assertion at 5671), `tests/test_pi_contract.py` (native-address contract, per `plans/changes/pi-pin/spec.md` criteria 10–11; found by search, not read this session), `tests/test_model_endpoints.py` (declaration validator; found by search, not read).
- Predecessor artefacts: `plans/changes/pi-catalog-redirect/` (spec read this session; `plan.md` and `decisions.md` not read), `plans/changes/go-access-point/` (spec read; decisions detail quoted), `plans/changes/pi-pin/spec.md` (read).

### What is unclear

- **The bead's subject and motivation.** The tracker is unreadable from this worktree (see above); no tracked text names `coding-harness-vku6` or states what should move. [GAP → interview]
- **Which "move" the bead names.** Three readings are anchored in the tree; this research records them as readings with sources, not as a choice — choosing is the interview's question: (i) the catalog sources moving into the declared central registry — anchored by the `go-access-point` non-goal and its decisions detail (bead `coding-harness-wq1m` "will take them up") and ADR 0024's "coming provider/model registry"; (ii) a live move of pi.dev's catalog endpoint or host — the bridge pins origin *and* pathname exactly (`stage2_research_catalog.mjs:97-99`), so a provider-side move would refuse preflight the way the 307 did before `pi-catalog-redirect`; the newest tracked live observation is `docs/research/2026-11-03-pi-context-overflow.md`, whose forced refresh succeeded at 2026-11-03 01:12 UTC, and a search of the handovers through `docs/journal/handover/2026-11-03-five-lane-night.md` and `docs/research/` found **no** record of a live move — "not recorded in the tree" is not "not happening": whether pi.dev moved after 2026-11-03 is a live-network question this phase cannot answer; (iii) moving the research catalog acquisition itself between the two surfaces (the bridge duplicates the fetch the CLI path already performs, with divergent redirect policies — the predecessor research's "Where the bridge is consumed" and measured addendum).
- **Not read this session** (found by search or by earlier research only): `plans/changes/pi-catalog-redirect/plan.md` and `decisions.md`; `plans/changes/loop-until-clean/spec.md` (named by the predecessor as holding the forced-refresh refutations); `plans/changes/review-loop-deep-b/spec.md` (DL-B-8's original wording); `tests/test_pi_contract.py`, `tests/test_model_endpoints.py`; Pi's `model-runtime.js` refresh internals; `docs/adr/0020` and `docs/adr/0021` beyond the grep-verified excerpts cited above; the full current form of the old Go-origin redirect tests.
- **Tracker state for `coding-harness-vku6`** — status, links, `discovered-from` parent (for example whether it descends from `coding-harness-wq1m`), assignee: unknown. [GAP → interview]

### Which files a change would have to touch

The subject is open, so this is the file map of the surfaces a "move" of the catalog could touch, with the carriers named:

- `scripts/stage2_research_catalog.mjs` — the source defaults (lines 20–21, 28), the fetch guard (95–101), `admittedTarget` (58–86); any change to where the bridge fetches from or how it names its sources lands here first.
- `scripts/stage2_availability.py` — `catalog_bridge` (748), `go_policy` (414), the `prepare_research` call site (1176–1183).
- `scripts/stage2_swarm.py` — `select_research_catalog` (92), `pi_reason` (143–171), `ResearchCatalogError` (30); refusal wording and classification.
- `scripts/stage2.py` — `discover_free` (2224) and the overlay machinery (`activate_overlay`, `check_overlay`) for the CLI surface; `PI_DISCOVERY_SECONDS` (375).
- `scripts/stage2_go.py` and the `adresse` record in `model-endpoints.yaml:509-515` — only if a move changes the record's shape or its readers (the record today admits the *destination* side only; it holds no catalog source).
- `model-endpoints.yaml` — the `free_stage` rule (482–502) and the `bemerkung`'s catalog-source sentences (541–546), if the declaration is to carry a moved source.
- `tests/test_stage2_research_catalog.py` — the `Sources` harness (64) and redirect suite; any new behavior needs a loopback branch here first (the pattern `pi-catalog-redirect` followed).
- `scripts/research_capture.py` (809–813) and `tests/test_stage2.py` (5671), `tests/test_pi_contract.py` — if the exported options, the pin or the native-address contract change.
- `tools/pi/` — only if the pin moves (protected precedent: `pi-catalog-redirect` and `go-access-point` both list `tools/pi/` as protected).
- `docs/WORKFLOW.md` and, if a registry decision is due, `docs/adr/` — doctrine statements at 826–838, 992–993, 1410–1417; an ADR takes effect only on the maintainer's merge (ADR 0008).

### Proposed `neighbours:` header

Validated as tracked files this session (the format `given_neighbours` expects; specimen `plans/changes/red-first-pytest-failed/research.md:15-17`):

- `plans/changes/pi-catalog-redirect/spec.md` — the direct predecessor; its non-goals fenced off exactly this topic ("Moving the catalog source").
- `plans/changes/go-access-point/spec.md` — the built address slice; its non-goals and decisions hand the catalog sources to the future registry (bead `coding-harness-wq1m`).
- `plans/changes/research-swarm/spec.md` — criteria 38 and 41 bind the fresh two-source catalog record and the exit-1 rule.
- `plans/changes/pi-pin/spec.md` — the Pi 1.2.0 pin and the contract suite the catalog tests run under.
- `plans/changes/loop-until-clean/spec.md` — the forced-refresh discovery path and its refutations (named by the predecessor research; **not read this session**).
- `plans/changes/review-loop-deep-b/spec.md` — DL-B-8, the destination finding behind the address policy (**not read this session**; named via `go-access-point`).
