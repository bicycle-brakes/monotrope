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
