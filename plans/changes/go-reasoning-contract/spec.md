---
title: "Spec — go-reasoning-contract"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-1zqh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, pi, reasoning, contract-tests]
class: bounded
appetite: 4
adr_files: []
---

# Spec — go-reasoning-contract

Prove the reasoning request and response path for the two native Go wire APIs
with hermetic contracts (bead `coding-harness-1zqh`). Research: `research.md`;
scope and interview skip: `decisions.md`.

## Problem

- On 2026-11-21, research found that the Go overlay retains the `reasoning`
  flag and reviewer launches request maximum thinking, but it did not establish
  what Pi puts on either native wire or how reasoning responses are parsed.
- The maintainer's split recorded in `decisions.md` says the existing native
  contracts proved plain text only; the saved repair attempts did not establish
  the reasoning case.

## Acceptance criteria

The two exchanges use `stage2.run_reviewer`: its production overlay and
address assessment admit a synthetic row before the transport is redirected to
the guarded loopback stub. The answer is the text that reviewer path returns
after extracting and scrubbing Pi's output. The synthetic Messages row uses
the admitted id `qwen3.8-flash`; the synthetic Responses row uses the
admitted id `grok-4.7`. Each row has its native API and base,
`reasoning: true`, `input: [text]`,
`contextWindow: 128000` and `maxTokens: 4096`; the overlay does not pass
`thinkingLevelMap` or `compat`. Both exchanges use the production launch's
`--thinking max` flag. The captured request values in criteria 1 and 2 remain
unmeasured; those criteria are not final until the gap below is resolved.

1. When the pinned Pi sends an Anthropic Messages request for a synthetic,
   reasoning-enabled Go row with maximum thinking, the request carries its
   native enabled thinking setting and a positive thinking budget.
   *Refuted by:* An absent, disabled or nonpositive thinking setting; the
   exact accepted shape and value await the measurement below.
2. When the pinned Pi sends an OpenAI Responses request for a synthetic,
   reasoning-enabled Go row with maximum thinking, the request carries the
   native reasoning effort selected by the pinned Pi for that row.
   *Refuted by:* An absent or different `reasoning.effort`; the exact value
   awaits the measurement below.
3. When the Messages stub streams a reasoning block and a distinct text answer,
   the answer read by the runner contains the text.
   *Refuted by:* The runner's answer lacks the text.
4. When the Messages stub streams a reasoning block and a distinct text answer,
   the answer read by the runner excludes the reasoning.
   *Refuted by:* The runner's answer contains the reasoning marker.

5. When the Responses stub streams a reasoning block and a distinct text answer,
   the answer read by the runner contains the text.
   *Refuted by:* The runner's answer lacks the text.
6. When the Responses stub streams a reasoning block and a distinct text answer,
   the answer read by the runner excludes the reasoning.
   *Refuted by:* The runner's answer contains the reasoning marker.

The Messages stub streams a `thinking` block with a `thinking_delta` marker
and signature, then a text block with a different marker. The Responses stub
streams a reasoning output item with a summary text marker, then a message
output item with the distinct text marker. Each is a complete native stream
on the same reasoning-enabled exchange described above.

If a criterion is red against the pinned Pi, the attempt stops and reports the
finding to the orchestrator; it does not tune the row, mark the test as an
expected failure, change Pi or its pin, or change provider policy.

## Non-goals

- Live OpenCode Go calls, paid models, and claims about live model capabilities.
- Google Generative AI, Codex effort settings, provider admission changes, and
  changes to the production reasoning policy or catalog-field filter.

## Protected areas

Provider declarations, credentials, and production address policy remain
untouched: the contracts use synthetic records and a loopback server.

## Definition of Done

- `make verify` is green; the two native reasoning contracts run offline.
- No ADR or living capability document changes are due.
- The protected areas and non-goals remain untouched, as shown by the PR file list.
- The PR closes `coding-harness-1zqh` and its last commit carries
  `Closes-Bead: coding-harness-1zqh`.
- Special runs: none.

## Open decisions

[GAP] On 2026-11-21 the pinned Pi 1.5.0 was not installed in this worktree.
Measure each native request against the loopback stub using the row and
production path above, then record the exact Messages thinking shape and
budget if applicable, and the Responses `reasoning.effort`, in criteria 1
and 2. Do not infer them from the failed saved attempt. Reconcile findings S3
and S4 before treating the spec or plan as final.

[DETAIL] Use distinct synthetic reasoning and answer markers, so the test can
detect both lost text and leaked reasoning without live data.

[DETAIL] Use `qwen3.8-flash` and `grok-4.7` as the synthetic row ids, so the
measured requests use the cheapest admitted, measured model on each native
API as recorded in `model-endpoints.yaml` on 2026-11-21; this does not assert
that the other admitted models have the same reasoning settings.
