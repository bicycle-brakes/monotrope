---
title: "Go wire APIs — live measurement 2026-11-06"
category: research
created: 2026-11-06
updated: 2026-11-07
last_reviewed: 2026-11-06
status: draft
implementation_status: partial
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-36za
owner: framework-architect
tags: [stage-2, opencode-go, wire-api, measurement]
---

# Go wire APIs — live measurement 2026-11-06

Plan step 8 of the change go-wire-apis (bead coding-harness-36za). Measured by
the orchestrating session through `python3 scripts/stage2.py prepare-loop
go-wire-apis` — its forced catalog refresh, leak check and pinned tool-free
probes — on 2026-11-06 at 18:48 UTC, code commit `7da000ef` (branch
feat/go-wire-apis with the staged declaration), Pi `1.5.0`. Its receipt was
not used for a review loop. Audit: the runner's preparation state under
`~/.local/state/coding-harness/stage2/`; no key or raw traffic is copied here.

## Source reading

The Go page (https://opencode.ai/docs/go, read 2026-11-06) lists an endpoint
and AI SDK package per model and says every text model also works through the
other APIs, which Console translates:

| API | Endpoint on the page | Package | Ids on the page |
|---|---|---|---|
| openai-completions | https://opencode.ai/inference/go/openai/v1/chat/completions | @ai-sdk/openai-compatible | the GLM, Kimi, LongCat, DeepSeek, MiMo, Hy and Step ids |
| anthropic-messages | https://opencode.ai/inference/go/anthropic/v1/messages | @ai-sdk/anthropic | claude-haiku-5-5, minimax-m3, qwen3.8-max, qwen3.8-flash, qwen3.7-plus |
| openai-responses | https://opencode.ai/inference/go/openai/v1/responses | @ai-sdk/openai | grok-4.7, gpt-6-luna, gpt-5.6-luna, the two muse-spark contributor ids, crouton-alpha-free |
| google-generative-ai | https://opencode.ai/inference/go/google/v1beta/models/gemini-4-argon | @ai-sdk/google | gemini-4-argon |

## Result per API

| API | Base declared | Outcome | Representative |
|---|---|---|---|
| anthropic-messages | https://opencode.ai/inference/go/anthropic | **measured** — answers from qwen3.8-flash, qwen3.7-plus, qwen3.8-max, minimax-m3 | qwen3.8-flash (the preferred claude-haiku-5-5 failed, see below) |
| openai-responses | https://opencode.ai/inference/go/openai/v1 | **measured** — answer from grok-4.7 | grok-4.7 (the preferred gpt-6-luna is disabled) |
| google-generative-ai | not declared | **blocked** — the live catalog lists only gemini-4-argon-contributor, no exact admitted id | none |

Models that stay skipped, with the measured reason:

- claude-haiku-5-5 — 400 `"thinking.type.enabled" is not supported for this
  model. Use "thinking.type.adaptive"`: Pi sends a thinking setting this model
  refuses. A Pi adapter setting, not the address; the plan returns such a
  defect to the orchestrator instead of widening this change.
- gpt-6-luna, gpt-5.6-luna — 403 `Model access is disabled`.
- gemini-4-argon — not in the live catalog (only the contributor alias, which
  trains on request data and is not admitted).

Now qualifying (wire skip removed): qwen3.8-flash, qwen3.7-plus, qwen3.8-max,
minimax-m3 (Messages) and grok-4.7 (Responses); fresh preparation places them
on the paid ladder.


Routes. The offline contracts (`GO_NATIVE_ROUTES` in
`tests/test_pi_contract.py`) prove that the pinned Pi appends `/v1/messages` to the Messages base
`https://opencode.ai/inference/go/anthropic` and `/responses` to the
Responses base `https://opencode.ai/inference/go/openai/v1`; the expected
live routes are therefore the two documented page endpoints in the table
above.

## Open

Criterion "three APIs measured" is **not met**: Google has no representative.
This change is therefore not complete as planned; whether it ships with two
of three APIs is the maintainer's decision.
