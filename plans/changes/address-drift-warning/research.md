---
title: "Research — address-drift-warning"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-x2g9
owner: Data Architect
provenance: human-written
tags: [research]
---

# address drift warning — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3584 commits, 12 rules.

## Runner exploration — 2026-11-07

Research complete. Here is the repository research for `address-drift-warning`, written as prose ready to append to `plans/changes/address-drift-warning/research.md`.

---

## What exists today

**The change's own trail.** The change name decodes through the tracker trail: bead `coding-harness-x2g9` is "Warn on a differing OpenCode Go **address**" — call address, network endpoint, not code location. It comes from maintainer answer 3 of 2026-10-25 (interview item DL-B-8), recorded in `docs/research/2026-10-25-night-run-plan.md` ("Call address of OpenCode Go (DL-B-8). Warn only. When a catalog entry's `baseUrl` or `api` differs from the declared address, the runner names it, and the call still runs. Overlay definitions are not dropped."), and listed again in that file's addendum as item 7. The literal phrase "drift warning" exists nowhere else in the tree — a search for `drift[- ]?warn` matches only this change folder and its `plans/INDEX.md` row; the thing the name points at lives under other names ("Address notice", `verdict.notice`, finding DL-B-8).

**The answer was largely absorbed by its predecessor.** The destination finding DL-B-8 became the `go-access-point` change (bead `coding-harness-4tr4`), which carries the accepted ADR 0024 ("One access policy for OpenCode Go", `docs/adr/0024-one-access-policy-for-opencode-go.md`, status accepted 2026-10-31). ADR 0024's decision 3 says a different path on the admitted host is "preserved and visibly reported with the model and old/new paths" and never updates the record by itself; decision 4 says missing bases use the recorded default and unmapped wire APIs never fall through; decision 5 puts the record on the `opencode-go` entry of `model-endpoints.yaml`, maintained by the orchestrating session. A comment at `activate_overlay` in `scripts/stage2.py` (the `OVERLAY_FIELDS` block) states: "`baseUrl` crosses assessed (DL-B-8, closed by go-access-point)". The go-access-point spec's criteria 3, 5, 9 and 11 (`plans/changes/go-access-point/spec.md`) cover the notice, the refusal of refused rows, the orchestrator maintenance route and the audit evidence — the substance of answer 3, with ADR 0024's stricter refusal replacing answer 3's unconditional "call still runs" for foreign hosts.

**The declared address record.** `model-endpoints.yaml`, `endpunkte` entry `opencode-go`, key `adresse`: host `opencode.ai`, one wire API `openai-completions` with `basis: https://opencode.ai/inference/go/openai/v1`, `quelle` the Go page, `gelesen: 2026-10-31`. The entry's `bemerkung` states that on 2026-10-31 Pi's live catalog reports `https://opencode.ai/inference/go/v1` and that "a path on that host runs on with a notice and any other host is refused". So a live, persistent same-host path divergence existed at declaration time: recorded `/inference/go/openai/v1` vs catalog `/inference/go/v1`.

**The warning machinery is implemented and wired.** `scripts/stage2_go.py` holds the one policy: `load_address_policy` (fail-closed reader with a duplicate-key-rejecting YAML loader), `url_problem` (HTTPS, exact host, default port, no userinfo/query/fragment/control characters), and `assess`, which returns an `Assessment` whose `notice` names provider, model, recorded path and observed path for a same-host move, and whose `problem` refuses anything else. Call sites, all reading the same record fresh at call time:

- `scripts/stage2.py` — `activate_overlay` assesses every `opencode-go` row, drops and names refused rows, returns notices; `check_overlay` re-assesses the activated file and raises `Refused` before any listing or reviewer; the free-stage listing flow prints `Address notice: …` to stderr and stores the notices in the state dict; `run_reviewer` prints the notices, retains them, and refuses a non-admitted assessment; the review loop collects per-round notices through `capture_address_notices`/`retain_address_notices` (context manager at the loop entry).
- `scripts/stage2_swarm.py` — `select_research_catalog` collects same-host move notices per candidate into the selection state as `address_notices`; a row without a base whose wire API has no recorded base is skipped with reason `no-recorded-base`; a foreign or malformed base classifies the row `pi-malformed`.
- `scripts/stage2_availability.py` — `go_policy` refuses on an unusable record; `install_measured_models` fills a missing base from the record, assesses, raises on refusal and appends `address notice · …` to the audit; `probe_go` raises `DestinationRefused` before probing a refused destination and prints/appends the notice.
- `scripts/stage2_session.py` — `checked_session_model` loads the policy, reads the pinned install's provider catalog, assesses and returns the assessment, and refuses to start when Pi does not resolve the checked binding.

**Tests exist.** `tests/test_stage2_go_access.py` (created by the predecessor change; named in the `ci_gates.py` script-to-test mapping), plus address-related tests in `tests/test_model_endpoints.py` (record shape validation), `tests/test_stage2_session_policy.py`, `tests/test_pi_contract.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_research_catalog.py`.

**The drift warning fires today, per model, per launch.** The released loop record at the end of `plans/changes/go-access-point/findings.md` (rounds of 2026-11-03) shows the identical `Address notice` for roughly eighteen model ids per round — recorded base path `/inference/go/openai/v1`, definition names `/inference/go/v1` — interleaved into every free and paid member's record. The record itself has not moved since `gelesen: 2026-10-31`.

**Predecessor status.** All six `plans/changes/go-access-point/` artefacts carry `status: draft`, `implementation_status: partial` (`plans/INDEX.md`); its `findings.md` ends with the phase-6 Codex re-check of 2026-11-03 reporting "No finding." ADR 0024 is `status: accepted`. `docs/WORKFLOW.md` §"One address record for OpenCode Go" documents the policy, including the orchestrator maintenance route ("no separate approval per documented same-host path move, and no catalog refresh ever writes the record by itself").

## Where it lives

- Declaration: `model-endpoints.yaml` — `adresse` record and the address prose in the `opencode-go` `bemerkung`. This file is a held path: a stage-2 attempt never edits it; edits go through the orchestrator (go-access-point spec, "Protected areas").
- Policy code: `scripts/stage2_go.py` (whole module is the policy).
- Call sites: `scripts/stage2.py` (`activate_overlay`, `check_overlay`, free-stage listing flow, `run_reviewer`, `capture_address_notices`/`retain_address_notices`), `scripts/stage2_swarm.py` (`select_research_catalog`, `address_notice`), `scripts/stage2_availability.py` (`go_policy`, `install_measured_models`, `probe_go`, the report lines that print `Address notice:`, the snapshot key `address_notices`), `scripts/stage2_session.py` (`checked_session_model`).
- Tests: `tests/test_stage2_go_access.py` and the address rows in the test files listed above.
- Doctrine: `docs/adr/0024-one-access-policy-for-opencode-go.md`; `docs/WORKFLOW.md`, "One address record for OpenCode Go" paragraph.
- History/origin: `docs/research/2026-10-25-night-run-plan.md` (answers 3 and addendum 7); `plans/changes/go-access-point/` (spec, decisions Q-1–Q-5, research, design, plan, findings — findings read only in part: attempts head and the released loop record plus phase-6 tail; its decisions/design/plan bodies I have not read).

## What is unclear about it

1. **Remaining scope against the predecessor.** Answer 3's behaviour (warn on a differing `baseUrl`, the call runs, overlay definitions are not dropped) is implemented and covered by go-access-point criteria 3/5/11, and `stage2.py`'s `OVERLAY_FIELDS` comment marks DL-B-8 "closed by go-access-point". Not clear from the repository: whether bead `coding-harness-x2g9` remains open for new behaviour, for verification-and-close on its own trail, or for something the maintainer saw in a run. The bead's description lives in the Dolt tracker; I read no rendered copy (house rule 2), so this is an open question, not a guess.
2. **The persistent record divergence.** The record still names `/inference/go/openai/v1` (read 2026-10-31) while the live catalog named `/inference/go/v1` at least through 2026-11-03 (go-access-point findings loop record). Whether this change should exercise the criterion-9 maintenance route — a fresh documented reading of the Go page and an orchestrator edit of the record or an explicit re-confirmation — is undecided. Not known from the tree: what the live catalog reports today, 2026-11-07 (a catalog refresh is a network action; this phase is read-only).
3. **Notice volume.** The divergence makes the warning fire once per model per activation, printed to stderr and retained per round, so a single run emits dozens of identical lines (evidence: the findings loop record). Whether consolidating the warning is in scope is unstated anywhere I read. A bead for reducing this specific notice volume: not found (the noise bead named in `plans/changes/registry-block-last/spec.md`, `coding-harness-cqun`, concerns the plans-registry gate's DRIFT lines, a different mechanism).
4. **The "`api` differs" half of answer 3.** A row whose wire API differs from the measured `openai-completions` (e.g. the `anthropic-messages`/`openai-responses` rows named in the `bemerkung`) is skipped or refused today (`no-recorded-base` in `stage2_swarm.py`, the unmapped-API refusal in `stage2_go.assess`, the raise in `install_measured_models`) — ADR 0024 decision 4, stricter than answer 3's "warn only, still runs". Whether the maintainer reads ADR 0024 as superseding that wording is unrecorded in what I read.
5. **Class and appetite of this change are undeclared.** The `research.md` header carries no class; the bead description was not readable by me. The declarations that exist (`--class` from the runner, the headers of `research.md`/`spec.md`) must agree before explore consumes them (ADR 0020 routing).
6. **Merge state of the predecessor.** ADR 0024 is marked accepted, but the go-access-point artefacts remain `draft`/`partial` and unarchived. Whether its pull request has merged is not decidable from the tree alone; this change builds on its code either way, as it stands in this worktree.

## Which files a change would have to touch

Depending on which open question the interview settles: `scripts/stage2_go.py` (notice wording or assessment behaviour); `scripts/stage2.py` (`activate_overlay`, `check_overlay`, the free-stage listing flow, `run_reviewer`, the review-loop notice evidence); `scripts/stage2_swarm.py` (`select_research_catalog` notices); `scripts/stage2_availability.py` (`install_measured_models`, `probe_go`, the availability report lines and snapshot keys); `scripts/stage2_session.py` (`checked_session_model`) — with their tests (`tests/test_stage2_go_access.py`, `tests/test_stage2.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_session.py`, `tests/test_stage2_session_policy.py`, `tests/test_pi_contract.py`, `tests/test_model_endpoints.py`). A record update touches `model-endpoints.yaml` (orchestrator route only) and the `bemerkung` prose; doctrine changes touch `docs/WORKFLOW.md` and, if one were needed, a new ADR file under `docs/adr/`. This change's own folder `plans/changes/address-drift-warning/` and `plans/INDEX.md` (regenerated) follow in every case.

**Neighbours known** (for the header): `plans/changes/go-access-point/spec.md` (direct predecessor; also its `research.md`, `decisions.md`, `plan.md`, `findings.md`), `plans/changes/pi-catalog-redirect/spec.md`, `plans/changes/research-swarm/spec.md`, `plans/changes/pi-pin/spec.md`, `plans/changes/kimi-admission/spec.md`, `plans/changes/terms-expiry/spec.md`, `plans/changes/review-loop-deep-b/spec.md`, `plans/changes/registry-block-last/spec.md`.
