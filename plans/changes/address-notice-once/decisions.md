---
title: "Decisions — address-notice-once"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-zywb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage2-runner, output]
---

# address-notice-once — Decisions

Class: bounded (bead coding-harness-zywb: "Output deduplication inside existing behaviour, no ADR").

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> Seen 2026-10-31 22:13 UTC in prepare-loop go-access-point on branch feat/go-access-point (bead coding-harness-4tr4): 'Address notice: opencode-go/<model>: the recorded base path is /inference/go/openai/v1, the definition names /inference/go/v1; running on with this same-host move' printed up to three times per model in one call (probe, selection and overlay each print it), about 70 lines for 18 models.
>
> Needed: one notice per model and old/new path pair per runner call, or one summary line naming the models; a test counts the lines. Depends on coding-harness-4tr4 merging (the notice is its code).

The dependency is met: the notice code is on main (`scripts/stage2_go.py::assess`, explore). Still live on 2026-11-21: the `verify-two-slots` prepare-loop and review-loop runs printed the `gemini-4-argon` wire-api notice twice in one call (orchestrator, run output of 2026-11-21).

## SKIP · interview

status: skipped
reason: The bead fixes the unit ("one notice per model and old/new path pair per runner call") and the proof ("a test counts the lines"); the maintainer asked for no question windows until the block on 2026-11-23 10:00. The explore's open points are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope of "once": one runner call (one process), per distinct notice string.** A run-level seen-set: the first occurrence of a notice string is printed to the console; later occurrences in the same process are not printed again. Reason: the bead's unit; the string already carries model and path pair (or wire api).
- **Durable evidence keeps its promise.** ADR 0024 decision 3 and the pinned tests require the notice in durable evidence: every round record and report that records notices today still records each distinct notice once per record (the existing per-round dedup stays). Only console repetition is removed. Reason: evidence is per record, noise is per console.
- **Both kinds of notice:** the same-host path move and the unrecorded wire-api notice. Reason: same producer, same repetition (the `gemini-4-argon` lines of 2026-11-21).
- **No change to wording, streams or the two record spellings** (`Notice:` and `Address notice:`). Reason: out of the bead's scope; a separate bead if wanted.
- **Terms warnings are out of scope.** Reason: the bead names address notices only.
- **The test counts lines:** one call over many models with the same drift prints each notice string exactly once on the console, while the round record keeps it. Reason: the bead's proof.
