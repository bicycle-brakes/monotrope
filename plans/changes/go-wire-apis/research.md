---
title: "Research — go-wire-apis"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-36za
owner: Data Architect
provenance: human-written
tags: [research]
---

# go wire apis — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3349 commits, 12 rules.

## Runner exploration — 2026-11-06

The exploration is complete. Here is the research, ready to append to `plans/changes/go-wire-apis/research.md`.

---

## What exists today

**The change folder holds a skeleton, and its bead is unreadable from this worktree.** `plans/changes/go-wire-apis/research.md` is the frontmatter-only skeleton (frontmatter names bead `coding-harness-36za`, `provenance: human-written`, body says "this file is empty until it has run"); `plans/INDEX.md` (line for `changes/go-wire-apis/research.md`, dated 2026-11-06) lists exactly that one artifact. The folder was opened by the branch's head commit `8618ce7f` ("chore(go-wire-apis): open the change folder (bead coding-harness-36za)"). The tracker is the Dolt database on `refs/dolt/data` (AGENTS.md, house rule 2); this worktree's `.beads/` holds only configuration and hooks, and a worktree-wide search for `36za` matches nothing outside this skeleton — so **what exactly "go-wire-apis" names is not recorded anywhere in the tracked text** and is the interview's first question. What the tree records as the open Go wire-API work is below. [GAP → interview]

**The measured-wire-API rule exists, admits exactly one API, and has three enforcement sites.** The research swarm's declaration carries `availability_preflight: measured_wire_apis: [openai-completions]` (`model-endpoints.yaml`, `research_swarm:` block, key `measured_wire_apis`). `select_research_catalog` in `scripts/stage2_swarm.py` takes it as a parameter (signature default `measured_wire_apis=("openai-completions",)`), and its inner `seat_reason` classifies a seat candidate on any other `api` as `wire-api-not-measured`. `prepare_research` in `scripts/stage2_availability.py` passes the declared list through (`rule["measured_wire_apis"]`), and the same file's declaration validator requires `measured_wire_apis` as "a unique, nonempty list of names" ("`flash_size` (1..3) belongs to the review swarm, `measured_wire_apis` to the research swarm"). Free candidates are classified by `pi_reason` and `metadata_reason` only, not by `seat_reason`, so the measured gate does not bind the free class in code as read. A base-less candidate whose wire API has no recorded default is skipped as `no-recorded-base` by `pi_reason` (the comment: "an unmapped api has no default and no origin to check"). On the review-loop side the gate is terms, not selection: `terms_problem` in `scripts/stage2.py` refuses any model whose `modelle_terms` record carries `uebersprungen` ("the model X was skipped on <date>: <reason>").

**Nine declared models are kept out by exactly this rule.** Their `modelle_terms` records carry `uebersprungen` with `grund: "wire API not measured"`: dated 2026-10-17 `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5-5`, `minimax-m3`; dated 2026-10-22 `qwen3.7-plus`, `qwen3.8-max`; dated 2026-10-30 `grok-4.7` and `gpt-5.6-luna` (each "the Go page names the Responses endpoint") and `gemini-4-argon` ("the Go page names the Google endpoint; the live catalog lists only gemini-4-argon-contributor") — all under `modelle_terms` of the `opencode-go` entry in `model-endpoints.yaml`. Each of the nine already carries a full dated terms reading beside the skip (`gelesen`, `valid_until`, `aufbewahrung`, `training`, `anfragen_5h`); `valid_until` runs 2026-11-16 (the 2026-10-17 group), 2026-11-21 (the 2026-10-22 group) and 2026-11-29 (the 2026-10-30 group), so under ADR 0022 the first group expires 2026-11-16. The entry's `bemerkung` states the rule and the remedy: "All four are skipped: wire API not measured. Their data-terms admission under Q-11 stands; a probe must measure their real address before use."

**The doctrine of the skip is in the ADRs and the handover, not in `docs/WORKFLOW.md`.** ADR 0020 records that on 2026-10-18 "`qwen3.8-flash`, a fixed online member, could not be called (wire API not measured)" — the origin of the open seats — and describes seat candidates as "fresh text-input chat in Pi on a measured wire API", selected from the `measured_wire_apis` list. ADR 0021 fixes "existing wire-API skips remain unchanged", and ADR 0022 states "a future date is not an independent grant of admission. Wire-API skips … still bind." A grep of `docs/WORKFLOW.md` for "wire api" finds no match — not there (the file was searched, statement is about the grep, not a full read). The handover `docs/journal/handover/2026-10-17-night-run-sixth.md` records the first four skips (phase-6 row P6-1) and adds: "The probe belongs with the ladder check of bead coding-harness-mkg."

**The predecessor change built the address half and explicitly deferred the wire-API half.** The merged `go-access-point` change (bead `coding-harness-4tr4`) ships `scripts/stage2_go.py` — the one address policy — and the `adresse` record on the `opencode-go` entry (`model-endpoints.yaml`: `host: opencode.ai`, `apis:` with the single mapping `openai-completions → basis https://opencode.ai/inference/go/openai/v1`, `quelle` naming the Go page's Chat Completions endpoint, `gelesen: "2026-10-31"`). Its design says: "Only the measured wire API, `openai-completions`, is mapped. … Another API is added when it is measured and its address read from the Go page" (go-access-point `design.md`, data-model section). Its spec criterion 10 keeps the "measured-wire-API" restrictions intact — the address check replaces none of them. The record loader accepts any number of API mappings (`ADDRESS_KEYS`, the `_API` name pattern, `_record_problem` in `scripts/stage2_go.py`), and `assess` fills an absent base from the record for the definition's resolved API, refusing when unmapped ("declares no base and its wire api has no recorded base") — a mapping supplies a default address, "not permission to use an unmeasured API" (module docstring and `assess` docstring). `tests/test_stage2_go_access.py` already exercises multi-API records synthetically: `test_path_maintenance_records_source_and_date` adds an `anthropic-messages` mapping to the record and loads it, and feeds broken undated/unsourced variants expecting `RecordUnusable`. The change ended phase 6 with "No finding" (findings.md, "## Phase 6 — Codex, 2026-11-03") and was sent to its ADR 0024 decision pull request under a named stop (plan.md, "Review loop — named stop, 2026-11-03"); the ADR file carries `status: accepted` with "takes effect on merge" (docs/adr/0024), and `docs/WORKFLOW.md` carries the built address paragraph ("One address record for OpenCode Go"). Whether that decision PR has merged is tracker/PR state this phase cannot read.

**The Pi move that prepared the data is in the tree.** `tools/pi/package.json` pins `@earendil-works/pi-coding-agent` **1.5.0** (not 1.2.0), and `tests/test_pi_contract.py` carries the new shipped-catalog constants (`GO_SHIPPED = "https://opencode.ai/inference/go/openai/v1"`, `GO_SHIPPED_MESSAGES = "https://opencode.ai/inference/go/anthropic"`) plus the "Ledger 3" contract asserting the shipped Messages entries carry `anthropic-messages` on the moved base. This matches `pi-catalog-move` (bead `coding-harness-vku6`): its decisions Q-1 (2026-11-04) chose Pi 1.5.0 "to achieve all three models and the Messages address for the follow-up", its spec criterion 3 pins the shipped Messages entries, and its non-goals fence off the rest: "Admitting or calling new Go models, measuring the Messages wire API, changing model terms, routing, review membership or the shared Go address record; those return in the separate model-admission decision pull request." Observed discrepancy, stated as observed: `plans/INDEX.md` still lists all five `pi-catalog-move` artifacts with `implementation_status: none` while the tree already carries the 1.5.0 pin and its contracts — which of the two lags cannot be decided from this worktree.

**What the wire APIs are, per the shipped Pi 1.5.0 catalog** (`tools/pi/node_modules/@earendil-works/pi-ai/dist/providers/data/opencode-go.json`, read this session — shipped data, not a live reading): `anthropic-messages` at base `https://opencode.ai/inference/go/anthropic` (claude-haiku-5-5, minimax-m3, qwen3.7-plus, qwen3.8-flash, qwen3.8-max); `openai-responses` at the **same** base as completions, `https://opencode.ai/inference/go/openai/v1` (gpt-5.6-luna, gpt-6-luna, grok-4.7, muse-spark-1.2-contributor, muse-spark-1.3-contributor); `google-generative-ai` at `https://opencode.ai/inference/go/google/v1beta` (gemini-4-argon); `openai-completions` at `https://opencode.ai/inference/go/openai/v1` (the measured roster plus the free ids `beam-free`, `iceman-contributor-free`). The Go page as read on 2026-10-31 (recorded in go-access-point `research.md`, §4, Haiku sub-agent) documents per-API endpoints — Chat Completions `…/inference/go/openai/v1/chat/completions`, Anthropic Messages `…/inference/go/anthropic/v1/messages`, Responses `…/inference/go/openai/v1/responses`, Google `…/inference/go/google/v1beta/models/gemini-4-argon` — and says every text model "also works through the other APIs, which Console translates." The docs name full endpoints; Pi ships shorter bases; the one recorded precedent (`openai-completions`) records the Pi-shaped base with the docs endpoint named in `quelle`.

## Where it lives

- Declaration: `model-endpoints.yaml` — the `adresse` record (`model-endpoints.yaml:509-515`), the `research_swarm.availability_preflight.measured_wire_apis` list (same file, `research_swarm:` block), the nine `uebersprungen` skip records under `modelle_terms`, and the skip/address prose in the entry's `bemerkung` (from "As of 2026-10-17" through the 2026-10-31 address sentences).
- Enforcement: `scripts/stage2_swarm.py` (`select_research_catalog`, `seat_reason` → `wire-api-not-measured`, `pi_reason` → `no-recorded-base`); `scripts/stage2_availability.py` (the preflight declaration validator for `measured_wire_apis`, the `prepare_research` pass-through, `install_measured_models` refusing a base-less row on an unmapped API, and `probe_go` — the existing tool-free probe through pinned Pi, which assesses the destination against the record first); `scripts/stage2.py` (`terms_problem`, the `uebersprungen` refusal).
- Address policy (expected unchanged): `scripts/stage2_go.py` — the record already admits any number of API mappings; no wire-API-specific logic names a fixed API list (assessment from the read code, not a plan).
- Tests pinning today's single-API state: `tests/test_model_endpoints.py` (the `adresse` validator and fault injections, all keyed on `openai-completions`; the research-swarm rule assertion `rule["measured_wire_apis"] == ["openai-completions"]`); `tests/test_stage2_go_access.py` (`RECORDED_BASE` from the single mapping; `openai-completions`-keyed record mutations; the existing multi-API `anthropic-messages` fixtures in criterion 9's test); `tests/test_pi_contract.py` (shipped-catalog contracts, already at the 1.5.0 state). The swarm/catalog/availability fixtures carry `api: openai-completions` rows per the go-access-point research §3 — not re-verified per test this session.
- Doctrine: ADR 0020 (seat rule), ADR 0021 (skips remain), ADR 0022 (skips bind beside dated terms), `docs/WORKFLOW.md` (address paragraph; no wire-API paragraph found). History: `docs/journal/handover/2026-10-17-night-run-sixth.md` (the first four skips, P6-1).

## What is unclear about it

- **The bead's subject.** The tracker is unreadable from this worktree; no tracked text names `coding-harness-36za` or its class. Whether this change *is* the "separate model-admission decision pull request" that `pi-catalog-move`'s non-goals point to, or only the measurement step before it, is open. [GAP → interview]
- **What counts as "measured".** The only recorded definition is the `bemerkung` sentence "a probe must measure their real address before use". Whether that means one tool-free `probe_go` call per model, one per wire API, or a documented-address reading plus a probe — and where the measurement is recorded (the `bemerkung`, a `docs/research/` note, a new dated field) — is written nowhere in the tree. [GAP → interview]
- **Scope of APIs.** The skips cover three unmeasured wire APIs (`anthropic-messages`, `openai-responses`, `google-generative-ai`); `pi-catalog-move`'s fence names only "the Messages wire API". Whether Responses and Google are in or out is open.
- **Admission mechanics.** Removing a `uebersprungen` skip record and extending `measured_wire_apis` are edits to the held `model-endpoints.yaml`; the go-access-point Q-5 route (orchestrator edits, runner attempts never) applies to the entry, but whether the maintainer wants the ladder order, `flash_swarm`, seat declarations and the nine skip removals in one decision PR or several is open.
- **The `gemini-4-argon` id.** The skip record says "the live catalog lists only gemini-4-argon-contributor" (2026-10-30), while Pi 1.5.0's shipped data lists `gemini-4-argon`. Whether an id correction belongs to this change is open; the live catalog was not fetched this session.
- **Responses-on-the-completions-base.** Pi 1.5.0 ships `openai-responses` at the same base as `openai-completions`, while the docs page names `…/openai/v1/responses` as the endpoint. Whether the record carries two API keys with the same `basis` (its shape allows this) and what `quelle` names for Responses is a drafting detail, not yet decided by anyone.
- **Terms renewal overlap.** The 2026-10-17 readings expire 2026-11-16 (ADR 0022). Whether admission re-reads terms fresh or admits on the existing readings is the terms change's rule, not this one's — but the dates collide with any admission work this month.
- **go-access-point closure state.** The tree carries the built, phase-6-clean state and an `accepted`-marked ADR; whether the decision PR merged (and `plans/INDEX.md`'s `partial` rows for it are stale) is tracker/PR state not readable here.

## Which files a change would have to touch

`model-endpoints.yaml` (held file, orchestrator edits: new `adresse.apis` mappings with `quelle`/`gelesen`, the `measured_wire_apis` list, the nine `uebersprungen` skip records, the `bemerkung` skip/address prose) · `scripts/stage2_swarm.py` (only if the measured gate's default or reason wording changes) · `scripts/stage2_availability.py` (only if the preflight validation or the probe flow changes; `probe_go` is the existing measurement tool) · `scripts/stage2_go.py` (no change expected from the read code) · `tests/test_model_endpoints.py` (the `adresse` validator fixtures and the `measured_wire_apis` assertion) · `tests/test_stage2_go_access.py` (single-API-keyed fixtures, `RECORDED_BASE`) · `tests/test_pi_contract.py` (only if the shipped-catalog contracts move again) · `tests/test_stage2_swarm.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_availability.py` (`api: openai-completions` fixtures, per the predecessor research — not re-verified per test) · `scripts/research_capture.py` (its fixture rows carry `api: openai-completions`) · `docs/WORKFLOW.md` (if the measured-API rule gets a paragraph — none exists today) · possibly a dated note under `docs/research/` recording the probe measurements, following the repo's pattern for live measurements (e.g. `docs/research/2026-11-03-pi-context-overflow.md`) — a convention, not a gate found.

## Proposed `neighbours:` for the header

`plans/changes/go-access-point/spec.md` (the built address record; its design defers "another API … when it is measured") · `plans/changes/pi-catalog-move/spec.md` (the Pi 1.5.0 pin; its non-goals hand "measuring the Messages wire API" to "the separate model-admission decision pull request") · `plans/changes/research-swarm/spec.md` (the measured-wire-API seat rule of ADR 0020) · `plans/changes/kimi-admission/spec.md` (the 2026-10-30 unreachable marks beside the newest skip records) · `plans/changes/terms-expiry/spec.md` (ADR 0022; the skips' readings expire from 2026-11-16) · `plans/changes/pi-pin/spec.md` (the pin the shipped catalog rides on) · `plans/changes/pi-catalog-redirect/spec.md` (the merged catalog-source policy upstream of the seats).

---

**Where we are:** phase-1 exploration for `go-wire-apis` is complete; the prose above is ready to append to `plans/changes/go-wire-apis/research.md` (whose frontmatter then needs `provenance: ai-drafted-reviewed` with `produced_by:` and `review:`, per its own note).
**Next step:** the runner appends this, sets the `neighbours:` header, and the interview (phase 1a) takes the open questions above — first of all what the bead names and what counts as "measured".
**Needed from you:** nothing right now.

## Drafting follow-up — 2026-11-06

Read at `acebe186`, within this worktree: `decisions.md` records the bounded
class, and its Q-1 selects separate native measurements for Messages,
Responses and Google. There is no complete research-swarm/v2 record and no phase-2a
finding in the change's `findings.md`.

The existing mechanism is already generic: `probe_go` in
`scripts/stage2_availability.py` installs a checked model definition and uses
the pinned Pi with static text and no tools; `stage2_go` supplies per-API
bases without a fixed API roster. `dispatch_go` in `scripts/stage2.py`
independently rechecks paid terms, including skip marks, even when supplied
an admission callback. An API-measurement plan must therefore not rely on a
callback to bypass the wire skip. The orchestrator can provisionally maintain
the held declaration for the existing tool-free preparation, retaining the
final expansion only with successful evidence; no production bypass is needed.

`stage2.py probe` is not the static tool-free measurement path: its docstring
and implementation send a diff to free members and retain read tools for
paid calls. `prepare-loop` uses the existing static availability probes.
The offline stand-in and real-provider assertion in `tests/test_pi_contract.py`
currently cover Chat Completions only; the assertion explicitly files every
eligible rung in that one shipped catalog group. Native protocol exchanges
and a per-model API assertion are the bounded contract changes needed.

`templates/plan.md` and `scripts/validate_change_artefacts.py` are not present
in this tree. Use the phase-3 prompt's plan form and the available interview,
research-handoff and criterion-ledger checks; do not report the missing
validator as green. The latest available handover read was
`docs/journal/handover/2026-11-03-five-lane-night.md`; its lane state is dated
2026-11-03 and does not establish today's parallel-session or PR state.
Current hosted PR and parallel-session state were not read: this draft is
restricted to the worktree and repository git directory and makes no tracker
write, commit or branch change.
