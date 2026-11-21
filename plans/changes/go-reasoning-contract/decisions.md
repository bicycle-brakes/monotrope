---
title: "Decisions — go-reasoning-contract"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-1zqh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, pi, opencode-go, contract-tests]
---

# go-reasoning-contract — Decisions

Class: bounded (bead coding-harness-1zqh).

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> Split from coding-harness-36za (loop row L3-1, maintainer 2026-11-08): the native contracts prove Messages and Responses only with plain text answers; the admitted models' reasoning path is unproven. A test with a reasoning-enabled synthetic row per API failed in its setup three times (state at refs/stage2/attempts/go-wire-apis/orchestrator-saved-20261107b).

So the scope is the Go overlay path through Pi's native wire APIs (Messages and Responses), not the Codex effort setting. The explore ran with `--stage2-off` because GLM 5.3 Flash refused (bead coding-harness-b5pu).

## SKIP · interview

status: skipped
reason: The maintainer decided the split and its content on 2026-11-08 (loop row L3-1 of coding-harness-36za, quoted in the bead): one reasoning-enabled synthetic row per native API in the contract tests. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope: the two native wire APIs the contracts already cover,** `anthropic-messages` and `openai-responses`, each with one synthetic catalog row whose `reasoning` is true, run through the pinned Pi's real request building and response parsing against a local stub server, as the existing native contracts do. Reason: the bead; the Google endpoint and Codex efforts are out of scope.
- **What the test proves per API:** the request Pi builds for that row carries the reasoning setting the overlay declares (the thinking or reasoning-effort field of that wire format), and a stub answer that contains a reasoning block plus text is parsed into the text answer the runner reads, the reasoning block not leaking into it. Reason: "the reasoning path is unproven" — both directions.
- **Start from the saved attempt.** The draft reads `refs/stage2/attempts/go-wire-apis/orchestrator-saved-20261107b` and names why its setup failed three times, before the plan picks a setup. Reason: the third failure is evidence; repeating it wastes the appetite.
- **No live call to OpenCode Go and no paid model.** Reason: contract tests stay hermetic.
