---
title: "Research — model-endpoints-refresh"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-363r.5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# model endpoints refresh — Research

## Topic (bead coding-harness-363r.5)

Class: bounded. Maintainer 2026-11-25 (session 9200c6b1). Measured 2026-11-25 ~17:50 through scripts/stage2.py prepare-loop: (1) mimo-v2.5 and mimo-v2.5-pro answer 410 ModelDeprecated although the fresh Go catalog (pi 1.5.0, 16:41 UTC) still lists them; remove them from the admitted lists and seats in model-endpoints.yaml with the measurement as reason. (2) Stale skip records: beam-free and kimi-k3.1-pro are skipped as 'not in the live Go catalog (2026-10-30)' but both are in today's catalog; gpt-6-luna and gpt-5.6-luna carry a 403 from 2026-11-06; claude-haiku-5-5 a 400 (thinking not supported) from 2026-11-06; gemini-4-argon an unmeasured wire API (bead coding-harness-twdu). Re-measure each through the runner (prepare-loop) and update or remove its record. (3) Seven admitted models answer 403 'Model access is disabled' for this Go workspace (hy3, hy4-preview, deepseek-v4-pro, glm-5.3, grok-4.7, qwen3.8-max, kimi-k3): record the state; enabling them is the maintainer's console setting, not part of this change. Do not call unadmitted models (hy4, qwen4-max, muse-spark-1.2/1.3): their data terms are unread.

Further evidence (orchestrator, 2026-11-27): the prepare-loop of worktree-setup-hook-race (18:48Z) again recorded 403 'Model access is disabled' for deepseek-v4-pro and glm-5.3 among others, so the review loop ran with a single member (hy4-flash-free).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1320 files, 6156 commits, 12 rules.

## Runner exploration — 2026-11-28

Phase 1 research for `model-endpoints-refresh` (bounded, bead coding-harness-363r.5). Read-only: I changed no file and ran no command. The text below is ready to append to `research.md`.

## What exists today

**The declaration.** `model-endpoints.yaml` (repository root) is the single declaration of which endpoints and models may be called. Its `opencode-go` entry has:
- `modelle`: the paid ladder, an unordered set of 27 ids. It includes `mimo-v2.5` and `mimo-v2.5-pro`, each with a trailing comment "not reachable since 2026-10-30 (prepare-loop: 410, deprecated); kept, marked, on the maintainer's word (plans/changes/kimi-admission Q-3)". It also includes `glm-5.2` (comment: not reachable since 2026-10-30, 403), `beam-free`, `kimi-k3.1-pro`, `gpt-5.6-luna`, `gpt-6-luna`, `claude-haiku-5-5` and `gemini-4-argon`.
- `modelle_terms`: one record per id. A dated terms reading carries `gelesen`, `valid_until`, `quelle`, `aufbewahrung`, `training` and `anfragen_5h`. A skip carries `uebersprungen` (a date) and `grund`.
- `flash_swarm`: `deepseek-v4.1-flash`, `glm-5.3-flash`, `mimo-v2.6-pro`. No `mimo-v2.5*` id is in it.
- `free_stage` and `online_free`: exclusion lists for free ids only. No mimo or 403 model is in them.
- `adresse`: the one admitted Go host and its wire APIs.
- `availability_preflight`: `flash_size`, `max_age_seconds`, `exclude_until`.

**The research seats.** `research_swarm.repository_seats` and `online_seats` pin no Go model. Their entries are `{endpoint: opencode-go}` (open seats), except one `claude-code-plan` seat pinned to `claude-haiku-5-5`. `prepare-explore` fills the open seats per run from the reachable admitted models. Nothing in the seats block names `mimo-v2.5` or `mimo-v2.5-pro`. The yaml comment on `research_swarm` says Go seats name no model since 2026-10-21.

**The skip check.** In `scripts/stage2.py`, `_reading_problem` refuses any record with `uebersprungen` set. It returns "the model … was skipped on <date>: <grund>". `_expiry_problem` refuses a record with no usable `valid_until` or one past its date. `terms_problem` (the paid-model check) calls both.

**The probe.** `scripts/stage2_availability.py` decides reachability at run time. It returns `unreachable` with the endpoint's error text as the reason. It is not a record in the yaml: it is re-probed at each `prepare-loop` and `prepare-explore`, so a yaml entry does not by itself exclude a model from a run.

**The tests.** `tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading` asserts that every `modelle` id has either a `uebersprungen` record with a dated `uebersprungen` and a `grund`, or a `gelesen` record with a `quelle`, `training == "Not used"` and an `aufbewahrung`. It also asserts that the admitted and skipped sets together equal `modelle`. The test does not forbid orphan `modelle_terms` records. The test also checks the cost ordering: `ordered_models` follows `anfragen_5h`, and `cheapest_notice` compares `flash_swarm` with the top three.

**Other notes.** `plans/changes/model-endpoints-refresh/decisions.md` (ai-drafted-reviewed, review pending) records a skip of phase 1a with the bounded standing grant of 2026-11-25 as the reason. The change's header in `research.md` carries the bead text with the three measurement groups listed below. `docs/research/2026-11-24-verified-audit-synthesis-and-roadmap.md` names the 2026-11-30 DeepSeek expiry in the same way.

## Where the three measurement groups stand in the repository

1. **mimo-v2.5 and mimo-v2.5-pro (410 ModelDeprecated).** Both are in `modelle` and in `modelle_terms` with `gelesen` 2026-11-14 and `valid_until` 2026-12-14, so they still pass the terms check. Their comments name 410 as the reason, dated 2026-10-30. `docs/research/2026-10-07`… no. The Pi research note `plans/changes/archive/2026-10-07-stage2-mimo/research.md` says the two ids were "withdrawn on 2026-10-21". So the date of withdrawal is recorded differently in two places. The bead's 2026-11-25 measurement is recorded in `plans/changes/agent-policy-list/findings.md` (prepare-loop calls on `mimo-v2.5` and `mimo-v2.5-pro`, 2026-11-25). I did not read the outcome lines of those calls.

2. **Stale skip records.**
   - `beam-free` and `kimi-k3.1-pro`: `uebersprungen` 2026-10-30, `grund` "not in the live Go catalog (2026-10-30)". Both still appear in `modelle`, so the skip is still in force.
   - `gpt-6-luna` and `gpt-5.6-luna`: `uebersprungen` 2026-11-06, `grund` "403 Model access is disabled". They are also still in `modelle`.
   - `claude-haiku-5-5`: `uebersprungen` 2026-11-06, `grund` "400 thinking.type.enabled is not supported". It is also in the `claude-code-plan` endpoint and seat list (the research seat pin), which is a separate endpoint not covered by this skip.
   - `gemini-4-argon`: `uebersprungen` 2026-10-30, `grund` "wire API not measured … bead coding-harness-twdu". Its comment on `modelle` says the live catalog of 2026-11-08 lists it again.

3. **Seven admitted models answering 403 for this workspace.** `hy3`, `hy4-preview`, `deepseek-v4-pro`, `glm-5.3`, `grok-4.7`, `qwen3.8-max` and `kimi-k3` have no state record in the yaml. Their `modelle_terms` records have no `uebersprungen`, and no comment names the 403. The only written record of the 403 is the bead text and the research header (2026-11-27, `worktree-setup-hook-race` run). The schema has no field for a reachability state; the convention in the file so far is a trailing comment on the `modelle` line (as with `glm-5.2`), and `uebersprungen` only for a skip that removes the id from admission.

Also in the tree: `hy4`, `qwen4-max` and `muse-spark-1.2`/`1.3` are not in the `opencode-go` `modelle` list or in `modelle_terms`. I checked the list, not the whole repository.

## What is unclear

- **Measurements are not in the tree I read.** The bead's 2026-11-25 measurement and the 2026-11-27 403 observation rest on the bead text and the change's header. I did not verify the calls' outcomes in their findings files, and I did not run a probe.
- **How to record a 403 state.** The yaml has no field for "reachability state, not a skip". Whether it becomes a comment, a new field, or is left to the probe is not stated in the bead or the decisions file.
- **Removing mimo from `modelle`.** The yaml comments say "kept, marked, on the maintainer's word (Q-3)". The bead asks to remove them. Whether the `kimi-admission` Q-3 word still binds is not answered in the tree; I did not read `plans/changes/archive/2026-11-06-kimi-admission/decisions.md` for that answer.
- **Withdrawal date for mimo.** Two dates appear: 2026-10-21 (`archive/2026-10-07-stage2-mimo/research.md`) and 2026-10-30 (the yaml comments). Which one is correct is not stated in the repository.
- **Orphan terms records.** The test does not fail when a `modelle_terms` record exists for an id no longer in `modelle`. Whether the removed mimo records should also go is not stated.
- **Deepseek terms expiry.** `deepseek-v4.1-flash` and `deepseek-v4-pro` carry `valid_until: 2026-11-30` (two days after this date). `docs/research/2026-11-24-verified-audit-synthesis-and-roadmap.md` tracks this as P1 `coding-harness-hw7w`. This change does not address it, but it is the nearest dated expiry in the file.
- **German text in the declaration.** Most comments and the `datenklassen` and `ausgeschlossen` blocks in `model-endpoints.yaml` are German. House rule 1 makes the repository English and reserves German for texts a maintainer reads at run time; `docs/...` in-tree German is slated for its own pull request (bead coding-harness-yim). This change should not translate it in passing.

## Which files a change would have to touch

- `model-endpoints.yaml`: the `opencode-go` `modelle` list (mimo-v2.5 and mimo-v2.5-pro lines), the `modelle_terms` records for each of the ids named in the three groups, and the comments that carry the measurements. `flash_swarm` and `repository_seats` do not name a mimo id, so the bead's "seats" reference has no hit there.
- `tests/test_model_endpoints.py`: the terms test is the one that binds the file (`test_every_new_paid_model_carries_its_terms_reading`) and the cost-order test. Any change that adds a skip record needs a dated `uebersprungen` and a `grund`.
- `scripts/stage2.py`: `_reading_problem` and `_expiry_problem` read the records. No change is needed for a skip record, only for a new field.
- `scripts/stage2_availability.py`: reads reachability at run time. No change is needed to record a 403 in the yaml, but the probe's exclusion behaviour is what actually keeps a 403 model out of a run.
- `scripts/export/manifest.yaml` and `scripts/kit/manifest.yaml` both name `model-endpoints.yaml`. The export manifest marks it `geruest` (skeleton); I did not read the kit manifest's verdict for it.
- `plans/changes/model-endpoints-refresh/decisions.md` and `research.md`: the change's own records.
