---
title: "Spec — model-endpoints-refresh"
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
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, model-endpoints]
class: bounded
appetite: 2
adr_files: []
---

# Spec — model-endpoints-refresh

The OpenCode Go declaration reflects measured deprecations and availability without admitting a model on an unmeasured assumption (bead `coding-harness-363r.5`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-25, the two mimo-v2.5 models returned 410 ModelDeprecated but remain declared for admission; the earlier decision retained them after the 2026-10-30 measurement (`research.md`).
- Six skip records rely on catalog, access or API observations from 2026-10-30 or 2026-11-06 and need renewed evidence (`research.md`).
- Seven admitted models returned access-disabled 403 responses, but the declaration does not record that state (`research.md`, observations dated 2026-11-25 and 2026-11-27).

## Acceptance criteria

1. When the declaration is refreshed, neither `mimo-v2.5` nor `mimo-v2.5-pro` is in an admitted OpenCode Go model list or research seat, and the 2026-11-25 410 measurement is recorded as the reason.
   *Refuted by:* Either model remains in such a list or seat, or its dated reason is missing.
2. When each of `beam-free`, `kimi-k3.1-pro`, `gpt-6-luna`, `gpt-5.6-luna`, `claude-haiku-5-5` and `gemini-4-argon` is re-measured through `prepare-loop`, its skip record is updated or removed according to its dated result and only a measured model can be admitted.
   *Refuted by:* A named model lacks a dated runner result, its record contradicts that result, or an unmeasured model is admitted.
3. When the seven observed access-disabled models are recorded, each of `hy3`, `hy4-preview`, `deepseek-v4-pro`, `glm-5.3`, `grok-4.7`, `qwen3.8-max` and `kimi-k3` has its dated 403 observation recorded without changing its terms admission solely because of that observation.
   *Refuted by:* A named observation is missing or undated, or a terms admission is changed solely because of the 403.
4. While the refresh is performed, models with unread terms are not called.
   *Refuted by:* A runner call is made to `hy4`, `qwen4-max`, `muse-spark-1.2`, `muse-spark-1.3`, or another model with unread terms.

## Non-goals

- Enabling model access in the OpenCode console, changing data-term policy, or reading terms for new models.
- Renewing DeepSeek terms, translating unrelated existing German text, or changing the runner's architecture.

## Protected areas

The separate `claude-code-plan` endpoint and its research seat remain unchanged: the Haiku skip concerns OpenCode Go only.

## Definition of Done

- `make verify` green; the dated runner evidence and its commit are named in the pull request.
- `model-endpoints.yaml` and these change artifacts move together; no ADR is changed.
- The pull request's file list shows protected areas and non-goals respected.
- The pull request closes `coding-harness-363r.5` and its last commit carries `Closes-Bead: coding-harness-363r.5`.

## Open decisions

- [DETAIL] Record the seven 403 observations as dated comments beside their model entries: the existing declaration already uses comments for reachability, and this leaves admission semantics unchanged.
- [DETAIL] Retain the two removed models' terms records as historical evidence: orphan records do not admit models and can be removed later without changing this refresh's behavior.
- [GAP] The current `prepare-loop` builds its paid candidates from the eligible ladder, which excludes dated skips; resolve an authorized runner path for measuring the six skipped models before changing their records. Do not bypass admission or invent a measurement.
