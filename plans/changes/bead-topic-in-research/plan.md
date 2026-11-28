---
title: "Plan — bead-topic-in-research"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5vts
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research]
---

# Plan — bead-topic-in-research

```text
For you:     New research starts with the tracker description available to the explorer.
Done when:   Creation, missing descriptions, preview and research publication pass the specified tests.
Appetite:    2 hours for implementation and repairs; stop at the limit.
Not now:     Backfilling existing research or changing the tracker and model routing.
Pre-mortem:  suppose it failed: most likely because publication strips the topic along with skeleton notices.
Starts unless you say stop.
```

## Steps

1. Change `scripts/plans_registry.py` to expose status and description from the same rendered tracker records while retaining the existing status reader's behavior; use the existing export access point, not a new tracker route. The renderer preserves fields other than machine-local ones; handle absent or non-string descriptions as missing.
2. Change `scripts/new_change.py` to build the topic section from the selected bead's description, preserving non-empty text, after the existing opening notices and below the title. Use the same body for preview and creation; retain all existing bead refusals and guards. Keep dynamic topic text out of `BODY_TEMPLATE` notice detection.
3. Change `tests/test_stage2.py` to exercise actual creation and preview with multiline descriptions, absent, empty and whitespace-only descriptions, existing refusal cases, and publication of the generated skeleton with topic preserved and notices removed. Update `tests/test_stage2_swarm.py` only if its skeleton fixture needs to match the resulting body; do not alter swarm behavior.
4. Run `python3 -m pytest tests/test_stage2.py tests/test_stage2_swarm.py` and `make verify` (start the latter through `python3 scripts/jobs.py start -- make verify`). No held path needs an implementation edit.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM through Z.ai was at its weekly limit until 2026-11-29 (`research.md`, 2026-11-28).

## Criterion ledger

- 1: tests/test_stage2.py::test_new_change_copies_bead_description — a multiline description or bead heading differs from the selected tracker record.
- 2: tests/test_stage2.py::test_new_change_names_missing_description — absent, empty or whitespace-only text lacks the explicit message or is invented.
- 3: tests/test_stage2.py::test_new_change_preview_matches_topic — preview and created topic differ for the same bead.
- 4: tests/test_stage2.py::test_research_publication_preserves_generated_topic — publication drops or changes the topic or description.
- 5: tests/test_stage2.py::test_research_publication_removes_notices_with_topic — either opening notice survives publication.
- 6: tests/test_stage2.py::test_new_change_keeps_bead_refusals — a missing export, absent bead or closed bead permits creation or loses its refusal.

## Do not touch

Leave existing research files, tracker data and renderer, model routing, ADRs and held paths alone.

## Runner route — 2026-11-28

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-28 00:14:51–00:16:39 UTC, 108 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-28 03:15:14–03:41:29 UTC, 1575 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: the whole tests/test_stage2.py requires full verification until coding-harness-vg9 splits it · measured by the runner
