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

1. When the pinned Pi sends an Anthropic Messages request for a synthetic,
   reasoning-enabled Go row with maximum thinking, the request carries its
   native enabled thinking setting and a positive thinking budget.
   *Refuted by:* An absent, disabled or nonpositive thinking setting.
2. When the pinned Pi sends an OpenAI Responses request for a synthetic,
   reasoning-enabled Go row with maximum thinking, the request carries the
   native reasoning effort selected by the pinned Pi for that row.
   *Refuted by:* An absent or different reasoning effort.
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

None open. [DETAIL] Use distinct synthetic reasoning and answer markers, so
the test can detect both lost text and leaked reasoning without live data.
