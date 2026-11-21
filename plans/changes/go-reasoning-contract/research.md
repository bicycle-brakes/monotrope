---
title: "Research — go-reasoning-contract"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-1zqh
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# go reasoning contract — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash refuses with claude-code:unrecognized_model on 2026-11-21 (bead coding-harness-b5pu) · leak check clean over 1161 files, 5255 commits, 12 rules.

## Runner exploration — 2026-11-21

## Research: go-reasoning-contract

Scope of this pass: read-only search of this worktree (`plans/`, `scripts/`, `tests/`, `docs/`, `model-endpoints.yaml`). Nothing outside the worktree was read. The tracker bead `coding-harness-1zqh` could not be read from here, so its wording is unknown.

### What exists today

**The change itself.** `plans/changes/go-reasoning-contract/` holds only `research.md`, an empty skeleton. It has no `spec.md`, `decisions.md`, or `neighbours:` header, and it declares no class. `plans/INDEX.md` lists it as a draft with no implementation status (row at line 610). No tracked text under `plans/specs/` mentions reasoning or thinking settings. What the change is meant to fix is not stated in any tracked file, so this pass cannot name its scope.

**Reasoning settings of Go-provider models (the closest match):**

- **Launch flag.** Both reviewer and availability launches pass `--thinking max` to Pi, with the model as `opencode-go/<id>`: `scripts/stage2.py`, the reviewer call function (the one around line 3290); `scripts/stage2_availability.py`, the availability probe (around line 569). The docstring of the reviewer call says Pi clamps `max` per model.
- **Overlay filter.** `OVERLAY_FIELDS` in `scripts/stage2.py` and `scripts/stage2_availability.py` is `("id", "name", "api", "baseUrl", "reasoning", "input", "contextWindow", "maxTokens", "cost")`. `activate_overlay` in `scripts/stage2.py` passes only these fields into Pi's `models.json`. Every other catalog field is dropped, including `compat`, `thinkingLevelMap`, `inputLimits` and `type`.
- **Dropped-field notices.** The dropped fields are named on stderr and in the run record. The records under `plans/changes/ontology-relation-layer/research.md` (catalog dumps) show lines such as `opencode-go/glm-5.3-flash: dropped catalog field(s) compat, inputLimits, thinkingLevelMap, type`. The same message appears in `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` (near line 309), which says the names go to stderr only.
- **Checked-model sidecar.** `scripts/stage2_session.py`, `MODEL_SIDECAR_FIELDS` (around line 279), carries `reasoning`, `compat`, `thinkingLevelMap` and `inputLimits` into the sidecar `checked-model.json` that `scripts/stage2_session_policy.mjs` binds. So the session path keeps these fields, while the overlay path drops them.
- **Address check.** `scripts/stage2_go.py` has no reasoning or thinking handling. `OVERLAY_FIELDS` in `stage2_go` is not defined there, and `assess` checks the destination only. The same file has no `thinking` text at all.
- **Schema check.** `pi_row_problem` in `scripts/stage2_availability.py` (around line 389) checks only that `reasoning` is a bool. It does not check `thinkingLevelMap` or `compat`.
- **Recorded refusal.** `model-endpoints.yaml`, `claude-haiku-5-5` (around line 274): skipped with the reason that its Messages API refuses Pi's request, `400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive"`. The measurement is in `docs/research/2026-11-06-go-wire-apis.md` (lines 50–51), under bead `coding-harness-36za`, archived as `plans/changes/archive/2026-11-16-go-wire-apis/`. The same skip is recorded in the catalog dumps of `ontology-relation-layer/research.md`.
- **Codex effort (separate route).** `CODEX_EFFORTS` in `scripts/stage2.py` (line 231) sets `draft: xhigh`, `repair: high`, `review: xhigh`, passed as `model_reasoning_effort` by `run_codex` (around line 3142). Its tests are in `tests/test_stage2.py`. Its history is in `plans/changes/archive/2026-11-06-sol-effort/`. Handover `docs/journal/handover/2026-11-20-day-run.md` (lines 31 and 74) records that this effort was raised one step, in one place.

### Where it lives

- Overlay and field filter: `scripts/stage2.py` (`OVERLAY_FIELDS`, `activate_overlay`), `scripts/stage2_availability.py` (`OVERLAY_FIELDS`, `pi_row_problem`).
- Sidecar and session policy: `scripts/stage2_session.py` (`MODEL_SIDECAR_FIELDS`), `scripts/stage2_session_policy.mjs`.
- Go address record: `scripts/stage2_go.py`, `model-endpoints.yaml` (`opencode-go` entries).
- Tests: `tests/test_stage2.py` (Codex effort assertions), the other `tests/test_stage2*.py` files, not read for Go fields.

### What is unclear

- **Scope.** The change's problem statement is not in any tracked file. Open: which of the two reasoning paths the change is about, the Go overlay (`thinkingLevelMap`, `compat`) or the Codex effort (`CODEX_EFFORTS`), or both.
- **Bead text.** `coding-harness-1zqh` could not be read here. `plans/changes/archive/2026-11-16-go-wire-apis/research.md` (line 58) records the same limit for an earlier bead.
- **Stored field values.** Whether `thinkingLevelMap` or `compat` carry the effort mapping for the Go models is not confirmed. The catalog dumps show the names but not the values. Not read: the live `models-store.json` and the Pi package code.
- **Pi's handling.** How Pi 1.2.0 turns `--thinking max` into a request body for each Go model is not read. The `--thinking` launch flag only says the request is clamped per model.
- **Haiku route.** Whether the `thinking.type.adaptive` setting is in Pi's configuration or only in the request is not read.
- **Structure.** The skeleton has no `neighbours:` header and no class declaration; `explore` refuses a run without them.

### Which files a change would have to touch (as the code stands)

- `scripts/stage2.py`: `OVERLAY_FIELDS`, `activate_overlay`, the reviewer call's `--thinking` launch.
- `scripts/stage2_availability.py`: `OVERLAY_FIELDS`, `pi_row_problem`, the availability launch's `--thinking`.
- `scripts/stage2_session.py`: `MODEL_SIDECAR_FIELDS`, and `scripts/stage2_session_policy.mjs` for the sidecar binding.
- `scripts/stage2_go.py`: only if the address record or Go row checks must change.
- `model-endpoints.yaml`: the `claude-haiku-5-5` skip entry and any other Go rows.
- `tests/test_stage2.py`, `tests/test_stage2_session_policy.py`, and the `stage2_availability` tests: the `model_reasoning_effort` and overlay assertions.
- `plans/changes/go-reasoning-contract/`: `spec.md`, `decisions.md`, and the `neighbours:` header of this file.

**Neighbours found (for the `neighbours:` header, not added here):** `plans/changes/archive/2026-11-16-go-wire-apis/`, `plans/changes/archive/2026-11-06-go-access-point/`, `plans/changes/archive/2026-11-06-sol-effort/`, `plans/changes/archive/2026-10-07-stage2-mimo/`.

I did not edit `research.md`. The runner writes it from this text.
