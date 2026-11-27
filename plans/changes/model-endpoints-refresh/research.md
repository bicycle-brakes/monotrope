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
provenance: human-written
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
