---
title: "Research — go-access-point"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-4tr4
owner: Data Architect
class: spike
provenance: human-written
tags: [research]
---

# go access point — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

> **Phase 1 routing exception (maintainer, 2026-10-31).** The bead is a
> `feature` (bead coding-harness-4tr4), but its own subject blocks the research
> swarm: every OpenCode Go model is refused at the swarm's origin check. The
> maintainer approved phase 1 through GLM 5.3 Flash instead, plus a Claude
> Haiku 5.5 sub-agent research of the repository and the public Go page, so
> this header declares `class: spike` for the explore verb alone. From the
> interview on, the change is a `feature` again; the spec's header says so.

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 793 files, 2870 commits, 12 rules.

## Runner exploration — 2026-10-31

The exploration is complete. Here is the research, ready to append to `plans/changes/go-access-point/research.md`.

---

## What exists today

**The subject is DL-B-8.** This change grows from the open doctrine finding DL-B-8 (MAJOR), recorded in `plans/changes/review-loop-deep-b/findings.md` (section "Open questions for the maintainer, 2026-10-25") and in full in `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` (finding DL-B-8 and the open-points table): where every OpenCode Go call goes is taken from the pi.dev catalog's per-model `baseUrl` and never compared with a declared address. The runner states the gap in code: the comment above `OVERLAY_FIELDS` in `scripts/stage2.py` (`# baseUrl crosses as it came: checking it against a declared address is the open DL-B-8.`). The recorded smallest fix, as stated in both sources: declare the address on the `opencode-go` entry and drop, with a notice, overlay definitions whose `baseUrl` or `api` differ. The same source calls the YAML field a decision pull request and pairs it with a bounded change.

**The review-loop side checks nothing.** `activate_overlay` in `scripts/stage2.py` copies exactly the `OVERLAY_FIELDS` (which include `api` and `baseUrl`) into `models.json` and drops other fields; no address comparison exists in the function head read (lines from its `def` onward). `scripts/stage2_availability.py` `install_measured_models` — used for every research launch and probe — likewise copies `OVERLAY_FIELDS` and, for a Go row without a `baseUrl`, writes `CHECKED_BASE_URL` via `row.setdefault` (deep review RS-3-7, named in the comment above the constant: so Pi never fills in a shipped definition's other path). The constant is `CHECKED_BASE_URL = "https://opencode.ai/zen/go/v1"` in `scripts/stage2_availability.py`. `test_real_refreshed_definition_resolves_without_newer_server_date` (P6-14) in `tests/test_pi_contract.py` asserts this crossing: a catalog definition with `baseUrl: https://catalog.example.invalid/fresh-endpoint` and `api: anthropic-messages` is activated for a declared paid model.

**The research-swarm side already refuses, but on a hard-coded address.** `select_research_catalog` in `scripts/stage2_swarm.py` classifies each catalog row through `pi_reason` → `safe_origin`: only `https`, hostname `opencode.ai`, port None or 443, no credentials, path exactly `/zen/go/v1` or `/zen/go/v1/`, no query, no fragment passes; anything else is `pi-malformed` and the candidate is skipped with its raw evidence, never failing the whole preflight (the function's docstring). A non-measured wire API is refused separately (`seat_reason` returning `wire-api-not-measured`; `measured_wire_apis: [openai-completions]` under `research_swarm.availability_preflight` in `model-endpoints.yaml`). The endpoint constant is `GO_ENDPOINT = "opencode-go"` in `scripts/stage2_swarm.py`. The maintainer's routing-exception note in this change's `research.md` (2026-10-31) reports the measured incident: every OpenCode Go model is currently refused at exactly this origin check — the fresh catalog's rows no longer carry the pinned origin. That is why the swarm cannot explore its own fix.

**"Declared" today means prose, not a field.** The research-swarm spec (`plans/changes/research-swarm/spec.md`, term "Admitted Go model") requires the id to be listed "with the declared Go origin" — but no address field exists in the declaration: the `opencode-go` entry in `model-endpoints.yaml` (from `- name: opencode-go`) declares `betreiber`, `residenz`, `abrechnung`, `darf_sehen`, `modelle`, `modelle_terms`, `availability_preflight`, `free_stage`, `bemerkung`, and nothing else. A grep for `adresse` across `scripts/` found no matches. The dispatch address exists in prose only: the `probe` docstring in `scripts/stage2.py` names `https://opencode.ai/zen/go/v1/chat/completions` as "the one Pi's built-in provider calls"; ADR 0011 (`docs/adr/0011-stage-2-reviews-through-opencode-go.md`) records the history — the OpenAI-compatible `/chat/completions` address from the Go page (read 2026-10-07), and three refused calls to the Anthropic-compatible `/messages` on 2026-10-08. `docs/WORKFLOW.md` does not name the address (grep `zen/go/v1`: no match there; 28 files name it overall, none of them doctrine).

**Context consistent with an address move, not proof of one.** The Go page moved: `https://opencode.ai/docs/go` now redirects to `https://opencode.ai/v2/docs/console/go/`, recorded in the `opencode-go` `bemerkung` (read 2026-10-29) and in the `deepseek-v4.1-flash` terms `quelle`. Whether the API base moved with it is not established by any repository source.

## Where it lives

- Declaration: `model-endpoints.yaml`, entry `- name: opencode-go`; swarm seat policy `research_swarm:` (same file), with `online_free` and `availability_preflight`.
- Enforcement (swarm): `scripts/stage2_swarm.py` — `select_research_catalog`, `pi_reason`, `safe_origin`, `seat_reason`; `GO_ENDPOINT`.
- Non-enforcement (review loop, probe, research launch): `scripts/stage2.py` — `OVERLAY_FIELDS` and its comment, `activate_overlay`, `probe`; `scripts/stage2_availability.py` — `OVERLAY_FIELDS`, `CHECKED_BASE_URL`, `pi_row_problem`, `install_measured_models`.
- Catalog fetch (sibling change's territory): `scripts/stage2_research_catalog.mjs` — `collectCatalog`, `admittedTarget`; owned by `pi-catalog-redirect` (bead `coding-harness-j2wb`), whose protected areas keep `scripts/stage2.py`, `scripts/stage2_swarm.py`, `scripts/stage2_availability.py` and `model-endpoints.yaml` unchanged, so the two changes are nearly disjoint.
- Offline fixtures: `scripts/research_capture.py` `catalog_fixture` (rows carry the pinned `baseUrl`, `api: openai-completions`).

Tests pinning today's behaviour: `tests/test_pi_contract.py` (P6-14, asserts a foreign `baseUrl` is activated), `tests/test_stage2_research_catalog.py` (refusal fixtures: wrong host, userinfo trick, plain http), `tests/test_stage2_research_deep_review.py` (asserts the `CHECKED_BASE_URL` setdefault), `tests/test_model_endpoints.py` `opencode_remark_problems` (the `bemerkung` must contain the literal address strings), `tests/test_stage2_research_availability.py` and `tests/test_stage2.py` (fixtures with the pinned `baseUrl`).

## What is unclear about it

- **The live catalog's current `baseUrl` values: not read.** This session is read-only and ran no command; the refusal incident is known only through the maintainer's note in this `research.md`. The new address, if one exists, is an open question, not a fact.
- **The bead text: not read.** `coding-harness-4tr4`'s description is not readable in this worktree — the tracker is the Dolt database on `refs/dolt/data`, and `.beads/` here holds only hooks and config (glob listed no database file). The subject reconstruction rests on the routing-exception note and DL-B-8's records.
- **Warn-only interim: not found in the runner.** Night plan item 3 (`docs/research/2026-10-25-night-run-plan.md`) proposed a warn-only comparison as an interim; the code comment still says "crosses as it came" and no warn was found in the read part of `activate_overlay`. "Not found in what I read" — the rest of the function was not read.
- **Scope of the declaration** (swarm only, or also review loop, probe, session, availability rows) and **whether `api` is constrained by the same field**: DL-B-8's smallest fix names "`baseUrl` or `api`", while the swarm checks the wire API through `measured_wire_apis` today. Open questions for the interview.
- **Decision-PR mechanics:** the recorded remedy calls the YAML field a decision pull request, but `provenance.yaml` reserves nothing for `model-endpoints.yaml` (grep "model-endpoints" there: no matches), and house rule 8 ties decision PRs to `provenance.yaml` reservations. How the maintainer wants this field decided is open.
- **A dated tension beside the subject:** the `bemerkung` (read 2026-10-29) says the DeepSeek ZDR agreement runs "through October 31, 2026" and expires 2026-11-01 unless re-read (ADR 0022), while `modelle_terms.deepseek-v4.1-flash` already carries `valid_until: "2026-11-30"` per the maintainer's statement of 2026-10-30. Both records sit in the same file; the newer one supersedes only if the maintainer says so — not this change's question, but a neighbour's.

## Which files a change would have to touch

`model-endpoints.yaml` (the `opencode-go` entry: the declared-address field; the `bemerkung` if the address moved) · `scripts/stage2.py` (`OVERLAY_FIELDS` comment, `activate_overlay`, `probe` docstring) · `scripts/stage2_availability.py` (`CHECKED_BASE_URL`, `install_measured_models`) · `scripts/stage2_swarm.py` (`safe_origin` reading the declaration instead of the literal, the endpoint-declaration reader if the field needs validation) · the tests listed above · `scripts/research_capture.py` (`catalog_fixture`). On current evidence not needed: `scripts/stage2_research_catalog.mjs` (catalog fetch from pi.dev, not the Go API address; owned by `pi-catalog-redirect`).

## Proposed `neighbours:` for the header

`plans/changes/review-loop-deep-b/spec.md` (DL-B-8's home change; its spec says "`baseUrl` is not checked here (DL-B-8)" and its plan lists DL-B-8 under "Not now") · `plans/changes/pi-catalog-redirect/spec.md` (the sibling catalog change, implementation partial, 2026-10-30) · `plans/changes/research-swarm/spec.md` (the "declared Go origin" term) · `plans/changes/pi-pin/spec.md` (the Pi pin the address rides on) · `plans/changes/kimi-admission/spec.md` (source of the 2026-10-30 unreachable markings in `modelle`) · `plans/changes/terms-expiry/spec.md` (ADR 0022; the dated DeepSeek tension) · `plans/changes/archive/2026-09-23-tracker-access-point/research.md` (name neighbour only — the tracker's access point, no shared mechanism).

---

**Where we are:** phase-1 exploration for `go-access-point` is complete; the prose above is ready to append to `plans/changes/go-access-point/research.md` (the file's frontmatter, per its own note, then needs `provenance: ai-drafted-reviewed` with `produced_by:` and `review:`).
**Next step:** the runner appends this to `research.md`, sets the `neighbours:` header, and the interview (phase 1a) can use the open questions above.
**Needed from you:** nothing right now.

## Sub-agent research (Claude Haiku 5.5) — 2026-10-31

Committed unchanged by the orchestrator; read-only research of the repository and the public Go page, as the maintainer asked (2026-10-31).

### Research report: one shared access point for OpenCode Go (bead coding-harness-4tr4)

Reads dated 2026-10-31. Worktree `/Users/mikypiky/coding-harness/.claude/worktrees/go-access-point`, branch `feat/go-access-point`.
Read-only: no repository file edited, no model called, `scripts/stage2.py` not run, no tracker write.
Scratch files (outside the repository): `/private/tmp/claude-501/-Users-mikypiky-coding-harness/0b3edc88-8c94-4bae-bd50-1f970c2a0227/scratchpad/sim/` (`sim_select.py`, `sim_loop.py`, `map_tests.py`).

#### Result first

1. **Cause of the research refusal.** `scripts/stage2_swarm.py:152-166` (`pi_reason`) admits a Go catalog row only if its `baseUrl` is `https://opencode.ai/zen/go/v1` (or with a trailing slash). Any other `baseUrl` returns `pi-malformed`. Pi's catalog now carries `https://opencode.ai/inference/go/v1`.
2. **Reproduced offline** (`sim/sim_select.py`, real `select_research_catalog`, same models, only `baseUrl` differs):
   - zen row: selected `['alpha-free', 'beta-free']`, outcome `selected`.
   - inference row: selected `[]`, outcome `measured-empty`, every candidate and every seat `pi-malformed`.
3. **Why the review loop still works.** It never runs that check. Its free stage and overlay copy `baseUrl` through unchanged. Reproduced offline (`sim/sim_loop.py`): `activate_overlay` keeps the inference `baseUrl`, `select_free` returns both free ids, `free_drops` returns nothing.
4. **The inference address is not new.** Persisted overlays in older `findings.md` files already carry it. The earliest I found: `plans/changes/runner-time-line/findings.md:194`, checked 2026-10-22T00:25Z. The store's server `lastModified` decodes to 2026-10-15T12:41:06Z. I did not measure when Pi first switched.
5. **Official docs (read 2026-10-31).** Documented chat path: `https://opencode.ai/inference/go/openai/v1/chat/completions` (note the `openai/` segment). Documented models list: `https://opencode.ai/inference/go/v1/models`. Pi's live base plus `/chat/completions` gives `.../inference/go/v1/chat/completions`, which the docs do not list. The review loop's successful use is evidence for it; I did not measure it.
6. **The pinned Pi still ships zen.** `tools/pi/node_modules/@earendil-works/pi-ai/dist/providers/data/opencode-go.json` (Pi 1.2.0, file mtime 2026-10-31 14:04) lists `https://opencode.ai/zen/go/v1` for `openai-completions`. Test `tests/test_pi_contract.py::test_real_opencode_provider_contracts` pins that.

---

#### 1. Inventory of Go names, hosts, paths, catalog sources, provider ids

Columns: location, what it does, which swarm uses it. "RL" = review loop (`stage2.py`, Pi, `prepare-loop`/`review-loop`). "RS" = research swarm (`stage2_swarm.py`, `stage2_availability.py`, `stage2_research_*`, `stage2_research_catalog.mjs`). "Session" = the interactive `session` verb.

##### 1a. Research swarm (RS)

| Location | What it does |
|---|---|
| `scripts/stage2_swarm.py:42` | `validate_research_free_policy`: refuses any provider other than `opencode-go`. |
| `scripts/stage2_swarm.py:91-304` | `select_research_catalog`: intersects the fresh Pi bridge with models.dev evidence. Returns `selected`, `candidates`, `models`, `selection_outcome`. |
| `scripts/stage2_swarm.py:152` | Default `baseUrl` when a row lacks one: `"https://opencode.ai/zen/go/v1"`. |
| `scripts/stage2_swarm.py:154-160` | The origin test: `scheme == "https"`, `hostname == "opencode.ai"`, `path in ("/zen/go/v1", "/zen/go/v1/")`, no userinfo, query, fragment. **This is the refusal.** |
| `scripts/stage2_swarm.py:165-166` | Failure returns `"pi-malformed"` (a reason, not an exception). |
| `scripts/stage2_swarm.py:172-179` | `seat_reason`: `pi_reason`, then `api in measured_wire_apis`. |
| `scripts/stage2_swarm.py:257-265` | Free candidates: `pi_reason` then `metadata_reason`. |
| `scripts/stage2_swarm.py:311,318` | `GO_ENDPOINT = "opencode-go"`, `LAUNCHERS` maps it to `"pi"`. |
| `scripts/stage2_swarm.py:367-429` | `invocation_problem` per role: endpoint, exclusions, declared model, data class. Never reads `baseUrl`. |
| `scripts/stage2_swarm.py:469, 509, 549-572` | Literal `"opencode-go"` in the slot plan and seat checks. |
| `scripts/stage2_availability.py:46` | `GO = "opencode-go"`. |
| `scripts/stage2_availability.py:350-353` | `OVERLAY_FIELDS`; `CHECKED_BASE_URL = "https://opencode.ai/zen/go/v1"`. |
| `scripts/stage2_availability.py:413-450` | `install_measured_models`: writes one row into `models.json`. Line 436-438: `if provider == GO: row.setdefault("baseUrl", CHECKED_BASE_URL)`. An existing `baseUrl` is kept as is. |
| `scripts/stage2_availability.py:463-541` | `probe_go`: tool-free probe. Line 493 calls `install_measured_models(..., model=...)` for `prepare-explore`. |
| `scripts/stage2_availability.py:692-711` | `catalog_bridge`: runs `scripts/stage2_research_catalog.mjs` under node. |
| `scripts/stage2_availability.py:1080-1150` | `prepare_research`. Line 1111: calls `select_research_catalog(...)`. Exit 2 becomes `Refused`, otherwise `CallFailed`. |
| `scripts/stage2_availability.py:254-273, 300-306` | `research_declaration_problem`, `research_probe_problem`: declared model, residency, exclusions. No URL check. |
| `scripts/stage2_availability.py:740, 860` | `_Selection` and `fill`: seat fill; with no usable model the seat stays empty. The exact refusal text after that was not read in full. |
| `scripts/stage2_research_catalog.mjs:12` | `PROVIDER = "opencode-go"`. |
| `scripts/stage2_research_catalog.mjs:20-21` | Sources: `catalogBaseUrl = "https://pi.dev"`, `metadataUrl = "https://models.dev/api.json"`. |
| `scripts/stage2_research_catalog.mjs:28` | Pi source URL: `/api/models/providers/opencode-go` on pi.dev. |
| `scripts/stage2_research_catalog.mjs:95-101` | Fetch guard: origin must equal pi.dev, path must equal `/api/models/providers/opencode-go`, one request only. |
| `scripts/stage2_research_catalog.mjs:58-86` | `admittedTarget`: the one allowed pi-version redirect (same origin and path). |
| `scripts/stage2_research_catalog.mjs:148-191` | Pi refresh through the pinned runtime; `catalogBaseUrl` passed to `ModelRuntime.create` (line 179). |
| `scripts/stage2_research_run.py:612-630` | `free_admission` (calls `invocation_problem`) and `dispatch_go` for each Go launch. |
| `scripts/stage2_research_run.py:688-698` | `pi_command`: line 692 calls `install_measured_models(..., model=entry["model"])`. So the catalog's `baseUrl` reaches `models.json` after selection. |
| `scripts/stage2_research_run.py:715` | Model string `f"{GO}/{entry['model']}"`. |
| `scripts/research_capture.py:56, 764, 796, 806, 847` | Attended capture harness (zen fixture at 764; `select_research_catalog` at 806). `scripts/ci_gates.py:114-120` says it is an entry point, not a gate. |

##### 1b. Review loop (RL) and shared code

| Location | What it does | Used by |
|---|---|---|
| `scripts/stage2.py:6, 58-60, 185` | Docstrings naming the zen chat URL and the ladder. Documentation only. | RL |
| `scripts/stage2.py:215` | `OPENCODE = "opencode-go"`. | RL (and research via `GO`/`dispatch_go`) |
| `scripts/stage2.py:365` | `ZEN = "opencode"`: the free rule may not select Zen (line 1816-1817). | RL |
| `scripts/stage2.py:1234-1268` | `declaration_problem`: model listed, `terms_problem` for `OPENCODE` (line 1253), `darf_sehen`, `residenz`. No URL check. | RL |
| `scripts/stage2.py:1515-1523` | `endpoint_entry`: reads the `opencode-go` entry fresh. | RL |
| `scripts/stage2.py:1639-1657` | `dispatch_go`: the send boundary. Checks terms or the admission callback only. No URL. | RL and RS (`stage2_availability.py:494`, `stage2_research_run.py:623`) |
| `scripts/stage2.py:1801-1846` | `free_rule_problems`: line 1818-1819, provider must equal `OPENCODE`. | RL |
| `scripts/stage2.py:1849-1870` | `free_admission_problem`: suffix, selection, exclusions, residency. No URL. | RL |
| `scripts/stage2.py:1908-1930` | `free_drops`: suffix or include match, `MODEL_ID` regex, exclusions. | RL |
| `scripts/stage2.py:1932-1952` | `select_free`: provider, suffix or include, excludes. | RL |
| `scripts/stage2.py:1954-1979` | `overlay_store`: reads `models-store.json`. Comment at line 1958 says the refresh is "pi.dev". | RL |
| `scripts/stage2.py:1991-1992` | Comment: "`baseUrl` crosses as it came: checking it against a declared address is the open DL-B-8." `OVERLAY_FIELDS` includes `baseUrl`. | RL |
| `scripts/stage2.py:1995-2038` | `activate_overlay`: copies `OVERLAY_FIELDS` into `models.json`. No `baseUrl` check. | RL (and `probe_go` only when `model` is None) |
| `scripts/stage2.py:2041-2104` | `check_overlay`: runs Pi's resolver offline; compares fields to the configured definition. Line 2078: provider literal `'opencode-go'`. No address check. | RL |
| `scripts/stage2.py:2122-2231` | `discover_free`: `pi update --models` (forced refresh), then `--list-models`. Line 2214: `"source": "pi.dev"`. Line 2222: billing note. | RL |
| `scripts/stage2.py:2414-2416` | Reads `OPENCODE_GO_KEY` from the secrets file. | RL (shared key use in RS not traced in detail) |
| `scripts/stage2.py:2533-2620` | `run_reviewer`: line 2590 `f"{OPENCODE}/{model}"` as `--model`; `dispatch_go` with `go_admission`. | RL |
| `scripts/stage2.py:8248-8320` | `probe`: docstring (line 8253) names the zen chat URL; calls `entry_problem`, free and paid probes. | RL |
| `scripts/stage2_session.py:8, 64-65, 164-177, 538-539` | `TRANSPORTS = {"opencode-go": "pi"}`; id parsing; `dispatch_go` for the opencode-go endpoint. | Session (not a swarm) |

##### 1c. Declarations, tools, decisions, docs

| Location | What it does | Used by |
|---|---|---|
| `model-endpoints.yaml:166` | The `opencode-go` entry. Has **no URL key** (no `baseUrl`, `adresse`, `url`). | RL and RS |
| `model-endpoints.yaml:170-196` | `modelle`: the review ladder (29 ids, the last `beam-free` is a free id). | RL |
| `model-endpoints.yaml:202` | `modelle_terms`: dated terms records; admit research models without the ladder. | RL and RS |
| `model-endpoints.yaml:465` | `availability_preflight` (review-loop block). | RL |
| `model-endpoints.yaml:482-502` | `free_stage` rule: `provider: opencode-go`, `id_suffix: "-free"`, exclude `step-5-preview-free`. | RL |
| `model-endpoints.yaml:503-606` | `bemerkung`. Lines 535-539 state the address: `https://opencode.ai/zen/go/v1/chat/completions` ("read 2026-10-07") and that `zen/go/v1/messages` is not used. This text is stale against the docs. | RL (and test) |
| `model-endpoints.yaml:611-643` | `research_swarm` block: seat declarations, `availability_preflight` with `measured_wire_apis: [openai-completions]` (line 642), `online_free` (line 643). | RS |
| `tools/pi/package.json` | Pins `@earendil-works/pi-coding-agent` at `1.2.0`. | RL and RS |
| `tools/pi/pi`, `tools/pi/install.sh` | No Go URL outside `node_modules`. | RL and RS |
| `tools/pi/node_modules/.../pi-ai/dist/providers/data/opencode-go.json` | Pi's shipped catalog (not live). `anthropic-messages` at `https://opencode.ai/zen/go` (5 models), `openai-completions` at `https://opencode.ai/zen/go/v1` (20), `openai-responses` at `https://opencode.ai/zen/go/v1` (6). | Read by a test only |
| `decisions/` | No decision record names a Go address. `decisions/answers/stage2-mimo/adr.yaml` names the OpenCode CLI, not a URL. | Not a code path |
| `docs/adr/0011-stage-2-reviews-through-opencode-go.md:61, 69, 90` | ADR text with zen URLs. Pinned by a test (section 3). | Documentation |
| `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` | Open findings RS-3-7 (absent `baseUrl` defaults to zen) and DL-B-8 (no check of where Go calls go). Status beyond its text: not read. | Documentation |

---

#### 2. Why the review loop works and the research swarm fails

**Research swarm, the check that fails** (`stage2_swarm.py:151-166`):

```
target = urlsplit(item.get("baseUrl", "https://opencode.ai/zen/go/v1"))
safe_origin = (target.scheme == "https" and target.hostname == "opencode.ai"
    and ... and target.path in ("/zen/go/v1", "/zen/go/v1/") ...)
...
if not safe_origin:
    return "pi-malformed"
```

Every Go row carries `inference/go/v1`, so `path` fails, `pi_reason` returns `pi-malformed`, and `seat_reason` and the candidate loop (lines 172-179, 257-265) inherit it. The selection is empty. Section 1a lists the downstream steps.

**Review loop, the checks that run instead:**

- Free stage: `free_rule_problems` (provider, suffix or include, exclusions, `input == implementation-diff`), then `select_free` and `free_drops` (suffix, excludes, `MODEL_ID`, membership in `fresh`). None of them read `baseUrl`.
- Overlay: `activate_overlay` (`stage2.py:1995-2038`) copies `OVERLAY_FIELDS`, which include `baseUrl`, unchanged. The comment at `stage2.py:1991` says so: "`baseUrl` crosses as it came: checking it against a declared address is the open DL-B-8."
- Call: `dispatch_go` (`stage2.py:1639-1657`) checks terms or the admission callback only. The model is started as `--model opencode-go/<model>` (`stage2.py:2590`). Pi chooses the URL from its `models.json` row, which holds the catalog's `baseUrl`.
- Offline check: `check_overlay` (`stage2.py:2041`) compares resolved fields to the configured ones, not to a declared address.

So the review loop trusts the pi.dev catalog's address. The research swarm is the only path with a hard-coded origin test. The two swarms disagree about the same fact.

**Second research-side place where the catalog URL is a value, not a check:** `install_measured_models` (`stage2_availability.py:438`) only supplies `CHECKED_BASE_URL` when the row has no `baseUrl`. Otherwise the row's `baseUrl` is written as is (`stage2_research_run.py:692`).

---

#### 3. Tests that pin the current Go URLs or paths

Fixtures built with the zen address make every positive test in the file depend on zen. Changing the address breaks them.

**Pinned zen address, fixture level:**

- `tests/test_stage2_research_catalog.py::model` (fixture helper, lines 35-49, `baseUrl` at line 41). Used by `Sources` (lines 63-65) and therefore by nearly every test in the file that uses the `sources` fixture. Notable:
  - `::test_go_seat_candidates_require_fresh_text_chat_entries` (line 427).
  - `::test_preflight_free_definition_cannot_redirect_its_declared_go_origin` (line 699; zen literals at lines 694-696; asserts a zen-origin row is selected).
  - `::test_preflight_seat_candidate_definition_cannot_redirect_its_go_origin` (line 717; zen literal at line 714).
- `tests/test_stage2_research_availability.py::pi_model` (line 119) and the `Catalog` class built on it (lines ~140-150). Used by all `fx` tests, e.g. `::test_pool_requires_tool_support_and_a_measured_wire_api` (line 347).
- `tests/test_stage2_research_deep_review.py::test_a_launch_writes_only_its_own_allow_listed_row` (line 251). Asserts `row == {**GOOD_ROW, "baseUrl": stage2_availability.CHECKED_BASE_URL}` (line 276). This reads the constant, so changing it does not break the test; the zen value is only the constant.
- `tests/test_stage2.py::test_activation_copies_only_the_allowed_definition_fields` (line 16456; zen literal line 16462). Asserts `baseUrl` survives activation.

**Pinned zen address, text level:**

- `tests/test_stage2.py::test_the_adr_draft_states_every_point` (line 13788; needle `` `https://opencode.ai/zen/go/v1/chat/completions`, through Pi `` at line 13803). Pins the wording of ADR 0011.
- `tests/test_model_endpoints.py::opencode_remark_problems` (line 489; literals at lines 494-495), used by `::test_the_opencode_go_remark_names_every_source` (line 525). Pins the `bemerkung` address text.

**Pinned against the installed Pi (zen):**

- `tests/test_pi_contract.py::test_real_opencode_provider_contracts` (line 959). `GO_NATIVE = "https://opencode.ai/zen/go/v1"` (line 55). Asserts `native_base_urls("opencode-go", "openai-completions") == {GO_NATIVE}` (lines 962-963) and that every ladder rung's catalog `baseUrl == GO_NATIVE` (line 973). Reads the installed Pi data file (section 1c). This test passes today only because that file still says zen (not run; see section 6).
- `tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date` (line 443). Uses `baseUrl: "https://catalog.example.invalid/fresh-endpoint"` (line 451) and asserts Pi resolves the catalog's `baseUrl` (lines 493-494). This pins the DL-B-8 behaviour (catalog decides the address). A checked address would break it on purpose.
- `tests/pi_contract_driver.mjs:123` names `https://opencode-go.invalid/zen/go/v1` as a network-guard target. Test-level mapping not done.

**Pinned the docs URL or the pi.dev source name (not a Go endpoint):**

- `tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading` (line 424; asserts `opencode.ai/docs/go` in `anfragen_quelle`, line 463).
- `tests/test_model_endpoints.py::test_the_opencode_go_entry_is_declared` (line 343). Named in `scripts/kit/probe.py:125` as a legacy exemption. Body not read.
- `tests/test_stage2.py::test_free_discovery_admits_new_go_models_each_run` (line 7504; asserts `source == "pi.dev"`, ~line 7536).
- `tests/test_stage2.py::test_the_loop_doctrine_names_both_swarms_until_clean` (line 7895; needle list includes `"pi.dev"`, line 7914).
- `tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect` (line 1019) and `::test_preflight_metadata_redirect_stays_refused` (line 1279). These pin redirect handling for pi.dev and models.dev.

**Broad-pattern counts** (provider id, `baseUrl`, hosts; cut-off 2026-10-31, from grep, not per-test): `tests/test_stage2.py` 88, `tests/test_stage2_swarm.py` 46, `tests/test_pi_contract.py` 43, `tests/test_stage2_research_catalog.py` 28, `tests/test_model_endpoints.py` 28, `tests/test_stage2_availability.py` 11, `tests/test_stage2_session.py` 11, `tests/test_stage2_research_availability.py` 8, `tests/test_stage2_research_deep_review.py` 7. `tests/test_stage2_swarm.py` contains no URL literal; its hits are the provider id.

---

#### 4. Official Go page, read by me with WebFetch (2026-10-31)

Caveat: WebFetch returns a summary written by a small model, not raw HTML. Cache 15 minutes. Two pages were read: `https://opencode.ai/docs/go/` (as asked) and `https://opencode.ai/v2/docs/console/go/` (the target named in `model-endpoints.yaml`).

**Base URL.** No standalone base URL in the text. The page links to `/console/harnesses#base-urls`. Every endpoint shares the prefix `https://opencode.ai/inference/go`. Models list (curl example): `https://opencode.ai/inference/go/v1/models`.

**Per-wire-API endpoints (docs/go):**

| Wire API | Exact path | Models per page |
|---|---|---|
| OpenAI Chat Completions | `https://opencode.ai/inference/go/openai/v1/chat/completions` | GLM-5.3-Flash, GLM-5.3, GLM-5.2, Kimi K3.1 Pro, Kimi K3, Kimi K2.7 Code, LongCat-2.0, DeepSeek V4.1 Flash, DeepSeek V4 Pro, MiMo-V2.6-Flash, MiMo-V2.6-Pro, MiMo-V2.5, MiMo-V2.5-Pro, MiniMax M3.1 Flash, Hy4 preview, Hy3, Step 5 Preview, Beam Free, Iceman Contributor Free |
| Anthropic Messages | `https://opencode.ai/inference/go/anthropic/v1/messages` | Claude Haiku 5.5, MiniMax M3, Qwen3.8 Max, Qwen3.8 Flash, Qwen3.7 Plus |
| OpenAI Responses | `https://opencode.ai/inference/go/openai/v1/responses` | Grok 4.7, GPT 6 Luna, GPT 5.6 Luna, Muse Spark 1.3 and 1.2 Contributor |
| Google v1beta | `https://opencode.ai/inference/go/google/v1beta/models/gemini-4-argon` | Gemini 4 Argon |

The page says every text model "also works through the other APIs, which Console translates."

**Pi statements:** "Current builds send session information for OpenCode. Update older installations." Pi is in the "validated clients" list. Client requirement: a stable `x-opencode-session` header per conversation.

**Redirect notice:** none in the summary. I did not determine whether a redirect happened. `model-endpoints.yaml` (line 206, 2026-10-29) says `docs/go` redirects to the v2 console; I did not verify that.

**Privacy table:** present, not repeated here. Two relevant points: the DeepSeek rows show retention `0 days*` (footnote not reproduced), and `Beam Free` shows `30 days`.

**Discrepancies to repo facts (facts, not measured):**

- The documented chat path has an `openai/` segment. Pi's base plus `/chat/completions` is not a documented path.
- The docs still list `glm-5.2`, `mimo-v2.5` and `mimo-v2.5-pro`. `model-endpoints.yaml` lines 170-196 mark them as unreachable since 2026-10-30. The docs and the live behaviour differ, or the marks are out of date. Not checked by me.
- Pi 1.2.0's shipped data lists `grok-4.6`; the docs list only `grok-4.7`.
- The docs list `muse-spark-*` and `iceman-contributor-free`, which are not declared in the repository.
- The docs use `anthropic/v1/messages` for Claude Haiku 5.5; Pi's shipped data uses `zen/go` for `anthropic-messages`. The repository's `bemerkung` (lines 535-539) still says the messages route on zen was refused on 2026-10-08.

---

#### 5. Design options for one shared access point

Facts are marked **[fact]**. Opinions are marked **[opinion]**.

##### Option A: one Python module both swarms import (recommended by me)

- **What.** A module such as `scripts/go_access.py` holds the provider id, the origin, the admitted base URLs per wire API, and one function `check_row(item) -> reason | None`. It replaces the literal in `stage2_swarm.pi_reason` (lines 152-166), the `CHECKED_BASE_URL` constant (`stage2_availability.py:353`), and is called by `stage2.activate_overlay` (`stage2.py:1995`). The `.mjs` bridge would need its own copy or a JSON read, since it is JavaScript.
- **[fact] What it fixes.** The research refusal (one constant, both swarms agree). The review loop gains the check that DL-B-8 asks for.
- **[fact] Consequences.** The review loop would start refusing rows it accepts today. That is a behaviour change and needs the DL-B-8 decision first. These tests change: `test_stage2_research_catalog.py::model` (line 41) and `test_stage2_research_availability.py::pi_model` (line 119) need a new base URL; `test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date` (line 443) asserts that the catalog decides the address, so it contradicts a check; `test_stage2.py::test_the_adr_draft_states_every_point` (line 13788) and `test_model_endpoints.py::opencode_remark_problems` (line 489) pin text that would need an ADR and remark update.
- **[opinion]** This is the cleanest single source. Ship it in two steps: first the research path only (fixes the refusal); then extend to the review loop as its own decision.

##### Option B: one record in `model-endpoints.yaml`, read by all checks

- **What.** Add a machine-readable block under `opencode-go`, for example `adresse:` with `chat_base`, `messages_base`, `responses_base`, `source` and `gelesen` (read date). `stage2_swarm.pi_reason`, `stage2_availability.CHECKED_BASE_URL` and `stage2.activate_overlay` read it through the existing readers (`_declared_endpoint` in `stage2_swarm.py:321`, `endpoint_entry` in `stage2.py:1515`).
- **[fact]** The file already holds `modelle_terms` dated records (line 202), and the repository's own remark style puts sources and dates next to values. DL-B-8 proposed the same key (handover 2026-10-25).
- **[fact] Consequences.** One reviewable place, testable with `test_model_endpoints.py`. But Pi's shipped data (zen) and the live catalog (inference) would both disagree with the record until someone updates it, and the record would be a second source of truth beside Pi's data unless a test compares them. `model-endpoints.yaml` is probably a decision-reserved file (house rule 8), so the change would be a decision PR. The provenance file was not read, so this is unconfirmed.
- **[opinion]** Good as the record of truth, weak as the only mechanism. Combine with A: A reads B.

##### Option C: smallest change, an allow-list in the research check only

- **What.** Change `stage2_swarm.pi_reason` (line 159) to accept both `/zen/go/v1` and `/inference/go/v1` on `opencode.ai`, https, no userinfo, query or fragment. Keep the review loop untouched.
- **[fact] Consequences.** Unblocks the research swarm within one function and two test fixtures. Leaves two lists of admitted origins (research and review loop), so it does not give one access point. It also does not close DL-B-8 for the review loop.
- **[opinion]** Acceptable as a hot-fix if the research swarm must run now. Not the target state.

##### Also to include in any option **[opinion]**

- Cover the catalog source as well as the model address. Today the research bridge hard-codes pi.dev and models.dev (`stage2_research_catalog.mjs:20-21, 28, 95-101`), and the review loop hard-codes pi.dev in prose and state (`stage2.py:1958, 2214`).
- Add a tool-free probe per wire API against the documented paths before trusting a new address. Neither swarm tests the address itself, only the Pi row.
- Keep the docs-derived list as evidence with date, as `model-endpoints.yaml` already does for prices and terms.

---

#### 6. Not read, not run

- **Test suite:** not run. Test names are from grep and reading, not execution.
- **Live catalog:** not fetched. The `inference/go/v1` value comes from persisted overlays in `findings.md` files, not from a fresh pi.dev or models.dev call.
- **WebFetch:** summaries from a small model, not raw HTML. The redirect question for `docs/go` is not determined.
- **Bead `coding-harness-4tr4`:** not read (no `tools/bd` call).
- **`decisions/provenance.yaml`:** not read. So I cannot say which files are decision-reserved, nor the status of DL-B-8 beyond the handover text.
- **Research seat fill:** `_Selection.usable` and `reachable` (`stage2_availability.py` ~860-920) not read in full. The exact refusal text after an empty selection is not confirmed.
- **Session verb** (`stage2_session.py`): read only at the call sites listed.
- **`tests/test_stage2_swarm.py`:** no URL literal found; per-test mapping not done.
- **`tests/test_model_endpoints.py::test_the_opencode_go_entry_is_declared`:** body not read.
- **Repository changes:** none. No file edited, no commit, no tracker write. Nothing proposed here is implemented or tested.
- **Dates:** "2026-10-15" is the server `lastModified` of a persisted store, not a verified start of Pi's switch.
