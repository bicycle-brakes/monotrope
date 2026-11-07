---
title: "Spec — go-wire-apis"
status: draft
implementation_status: partial
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-36za
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, opencode-go, wire-api]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — go-wire-apis

Measure OpenCode Go's Anthropic Messages, OpenAI Responses and Google wire
APIs, then enable direct calls for the already admitted models whose only
remaining obstacle is that measurement (bead `coding-harness-36za`). Research:
`research.md`; scope and direct-call choice: `decisions.md#Q-1`.

## Problem

As read in the exploration on 2026-11-06, the central Go address record maps
only `openai-completions`, and research preparation recognises only that API
as measured. Nine otherwise admitted model records retain a dated
"wire API not measured" skip. Their existing data-terms readings do not
override that skip (`research.md`, "What exists today").

At baseline `acebe186` (2026-11-06), Pi is pinned to 1.5.0 and supplies the
other API definitions, but the offline contract server answers only
`/chat/completions`. Its real-provider test requires every eligible review
rung to occur in the shipped Chat Completions group. Merely removing skips
would therefore enable protocols the contracts have not exercised. The
maintainer chose separate measurements and native calls rather than Go's
translation into Chat Completions (`decisions.md#Q-1`).

## Terms

- **Wire API:** the request and response protocol Pi uses, identified by its
  catalog `api` field; it is independent of the model's vendor.
- **Measured:** both an offline exchange through the actual pinned Pi and a
  successful live, tool-free Go probe support the API and its effective base.
  One live representative measures an API, not every model's availability.
- **Wire-skipped models:** `qwen3.8-flash`, `claude-haiku-5-5`, `minimax-m3`,
  `qwen3.7-plus`, `qwen3.8-max`, `gpt-6-luna`, `gpt-5.6-luna`, `grok-4.7`
  and `gemini-4-argon`; these are the existing records, not proposed new ids.

## Acceptance criteria

1. When the offline contracts exercise `anthropic-messages`, `openai-responses` and `google-generative-ai`, the actual repository-pinned Pi completes a native request and streamed text response for each API using only the synthetic Go credential at the expected protocol route.
   *Refuted by:* a protocol being untested, translated to Chat Completions, a wrong model or route, an undecoded reply, a foreign credential, a credential in the request body, or an external connection.
   *Basis:* `decisions.md#Q-1`.

2. If a new API's offline exchange fails, returns an empty or malformed response, or cannot start its required Pi/Node/loopback prerequisites, its contract fails visibly.
   *Refuted by:* a skip, a passing test on any such failure, or a success assertion based only on a catalog row or fabricated Pi output.
   *Basis:* `decisions.md#Q-1`; the existing mandatory contract boundary.

3. When an API is finally declared measured, a dated repository measurement note records a successful live probe through the pinned runner for that API, identifying the code commit, Pi version, exact model id, API, effective base, expected request route, documentation source and probe outcome without credentials or repository content in the model request.
   *Refuted by:* an API declared measured without its successful measurement (Google stays undeclared, `decisions.md#Q-2`), evidence for another API/base/id, an offline stand-in being reported as a live result, or an unrecorded/failed probe being treated as success.
   *Basis:* `decisions.md#Q-1`, narrowed by `decisions.md#Q-2`; `research.md`, the predecessor's measurement-before-use rule.

4. When the completed change's declaration is inspected, the one Go address record contains sourced and dated mappings for exactly the measured APIs — completions, Anthropic Messages and OpenAI Responses (`decisions.md#Q-2`) — and the research measured-API list contains exactly those three API names.
   *Refuted by:* a missing new mapping/list member, an additional unmeasured API, an unsourced or undated base, or a separate runtime address default outside that record.
   *Basis:* `decisions.md#Q-1`, narrowed by `decisions.md#Q-2`; the existing address-record contract.

5. When a wire-skipped model has an exact fresh catalog definition on a successfully measured API and still-valid admitted data terms, its wire-measurement skip no longer prevents a direct call in that definition's native protocol.
   *Refuted by:* a qualifying model retaining that wire-only obstacle, a different model id being substituted, an unrelated exclusion being removed, an absent id being admitted, or a catalog-only assertion forcing every eligible model back into Chat Completions.
   *Basis:* `decisions.md#Q-1`.

6. While the new APIs are exercised or used, the existing host/address, final-dispatch, leak, terms-expiry, capability, exclusion, receipt and free-purpose restrictions continue to apply.
   *Refuted by:* a foreign destination reaching a send, a missing base using another API's default, expired or otherwise inadmissible terms passing, an unmeasured API entering a research seat, or a free-class permission being used to admit a paid model.
   *Basis:* `decisions.md#Q-1`; `research.md`, the independent admission boundaries.

## Non-goals

- New model ids or data-terms admissions, terms renewal, changed retention or
  expiry dates, price/cost readings, manually selected seats or ladder order.
- Translation through Chat Completions, a Pi upgrade, catalog-source changes,
  a new address policy, or a new general-purpose measurement command.
- A live call to every model as the definition of API measurement; ordinary
  availability preparation continues to determine per-model reachability.
- Resolving an absent `gemini-4-argon` by using the contributor id; an absent
  exact id remains blocked and returns to the orchestrator with evidence.
- Design phase 2b and an ADR draft: this bounded change extends the existing
  address data and contracts under the already answered direct-call choice.

## Protected areas

Keep `scripts/stage2_go.py`, the runner and swarm implementation, Pi manifest,
lock, installer, network guard, agent settings, ADRs and governance unchanged:
their existing generic API and admission mechanisms are reused. The held
`model-endpoints.yaml` is the sole configuration exception and belongs to the
orchestrator, never an implement/repair attempt.

## Definition of Done

- The offline contracts and `make verify` pass after the orchestrator's final
  configuration edit, with the two successful live measurements (Messages,
  Responses) recorded; Google waits for an admissible model in its own change
  (bead coding-harness-twdu, `decisions.md#Q-2`).
- Move together: `model-endpoints.yaml`, the tests named in `plan.md`, and
  `docs/research/2026-11-06-go-wire-apis.md`; no ADR changes.
- The pull request file list respects the protected areas and non-goals.
- The pull request closes the API-measurement bead and its last commit carries
  `Closes-Bead: coding-harness-36za`.
- Special run: `python3 scripts/stage2.py prepare-loop go-wire-apis`, with its
  code commit and per-API evidence in the measurement note and PR body.
  Missing live evidence blocks completion even when offline tests pass.

## Open decisions

None open. The maintainer's direct-call answer stands unchanged.

- [DETAIL] Use one native representative per API and the existing tool-free
  preparation probes; separate API compatibility from normal model reachability.
- [DETAIL] Record evidence in the dated research note and reuse the existing
  address schema; adding a new evidence field to the address policy is unnecessary.
- [DETAIL] Set a three-hour implementation appetite, repairs included; neither
  the interview nor research supplies one, and exceeding it returns the work.
- [DETAIL] Keep `neighbours: []`: exploration used the Flash route, with no
  complete research-swarm/v2 run or structured neighbour answers to carry.

These reversible drafting choices are explicit so implementation does not
silently widen the maintainer's answer.
