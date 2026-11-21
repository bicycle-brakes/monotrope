---
title: "Spec — repair-hand-held-rows"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-0zhf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair]
class: bounded
adr_files: []
---

# Spec — repair-hand-held-rows

Before a repair attempt, separate taken findings whose named paths the runner cannot commit and hand them to the orchestrator (bead `coding-harness-0zhf`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-20/21, three repair attempts encountered paths the runner does not commit; the morning handover reports that whole attempts were restored (`research.md`, “The night's evidence”).
- At baseline `7b531fd0`, the checkpoint detects held paths only after an attempt and restores the attempt rather than advancing to another route; the existing rollback test pins that outcome (`research.md`, “The rollback” and “A rollback consumes the attempt and ends the run”).

## Terms

**Held path:** a repository path the repair checkpoint cannot commit under its existing case-insensitive prefix rules, including committed human-decided prefixes and its existing exceptions.

**Taken row:** the current finding selected for repair by the existing resolver, whether in the active loop record or findings.

## Acceptance criteria

1. When repair selects taken rows, each row whose `Where` names any held path is classified for an orchestrator hand step before a model call.
   *Refuted by:* A row naming both a committable path and a held path enters the model batch, or a held prefix accepted by the checkpoint is missed because of case or the committed provenance map.
2. When a taken row's `Where` names no readable path, it remains eligible for the model as it is today.
   *Refuted by:* A pathless row is handed off or dropped solely because its `Where` lacks a readable path.
3. When a batch contains both held and committable rows, the model receives only the committable taken rows for repair.
   *Refuted by:* The model receives a held row or does not receive an eligible committable row.
4. If every taken row is held, repair makes no model call and exits with the hand-step listing.
   *Refuted by:* A model is called, or the command exits without identifying the rows to hand repair.
5. When held rows are classified, the runner reports each row's identifier, each held path it names, and the reason `runner-held path` in its answer and in a listing appended to `findings.md`.
   *Refuted by:* Either listing omits an affected row, a named held path, or the reason, including when no model call is made.
6. While handing off held rows, the runner leaves their Status and `Broke a test` cells unchanged.
   *Refuted by:* A held row is marked fixed or its test mark is changed by the runner.
7. If an attempt nevertheless changes a held path, the existing checkpoint restores the attempt and refuses it.
   *Refuted by:* An unexpected held-path edit is committed or survives the existing rollback.

## Non-goals

- Changing `implement` or `draft` routing, retry limits, model selection, or the checkpoint's held-path policy.
- Inferring required edits from a finding's prose when its `Where` does not name a readable path.
- Performing or booking the orchestrator's hand repair, or changing the hand-repair status vocabulary.

## Protected areas

Held paths, including `provenance.yaml`, endpoint configuration, agent instructions, prompts, templates, ADRs and the tracker, remain outside the implementation attempt; the checkpoint remains authoritative for their protection.

## Definition of Done

- `make verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md` and the change artifacts, alongside the runner and its tests; no ADR.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-0zhf` and its last commit carries `Closes-Bead: coding-harness-0zhf`.
- Special runs: none.

## Open decisions

None open. The reversible scope, classification source, batch split, pathless-row treatment, hand-step record and retained checkpoint are recorded with reasons in `decisions.md` under `[DETAIL]`.
