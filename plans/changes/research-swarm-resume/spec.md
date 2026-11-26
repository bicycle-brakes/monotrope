---
title: "Spec — research-swarm-resume"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-f6qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm, resume]
class: bounded
appetite: 4
adr_files: []
---

# Spec — research-swarm-resume

Finished repository research contributions survive an aborted run and are reused on a matching resume (bead `coding-harness-f6qj`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

The maintainer recorded that consecutive runs with unchanged selection and tree recomputed all repository-topic seats because their prompt hashes changed, while finder, merge, sentence and online seats reused successfully (2026-11-25, `decisions.md` Q-1; the two observed changes and runs are named there). The exploration at commit `39004d9e` describes the existing exact binding and prompt-hash reuse checks and the persistence of terminal results (`research.md`); it did not establish the source of the drift.

## Acceptance criteria

1. When a research swarm resumes with the same frozen inputs and selection after an incomplete run, each repository-topic prompt for topics 1–8 is byte-identical to its corresponding prompt in the first run.
   *Refuted by:* A corresponding prompt differs because of a run identifier, publication growth, timestamp, changing commit count or another non-frozen input.
   *Basis:* `decisions.md#Q-1`.
2. When one repository-topic seat fails in the first run and the matching resumed run succeeds, every other finished, valid repository-topic seat is reused without another launch.
   *Refuted by:* A successful repository-topic seat is launched again or its stored result is not adopted.
   *Basis:* `decisions.md#Q-1`.
3. When that failed repository-topic seat is resumed, it is launched again rather than adopted as a successful result.
   *Refuted by:* The failed seat is reused or never launched.
   *Basis:* `decisions.md#Q-1`.
4. When a binding, seat identity, model, prompt hash or result validity fails the existing reuse checks, the affected result is not reused.
   *Refuted by:* A mismatched or invalid result is adopted despite the existing checks.
   *Basis:* `decisions.md#Q-1`; `research.md`, “The reuse decision”.

## Non-goals

- Changing the frozen-binding or exact prompt-hash contract, the selection of seats, or the research swarm's availability and retry policies.
- Repairing unrelated research-swarm failures or changing published research content beyond what the existing contract requires.

## Protected areas

Model configuration, leak checks, and unrelated changes remain untouched: this is a resume fix, not a change to security or model routing.

## Definition of Done

- `make verify` green; the two-run regression and the existing reuse boundary tests pass.
- Documentation or ADR changes: none expected.
- Protected areas and non-goals remain untouched, shown by the pull request's file list.
- The pull request closes bead `coding-harness-f6qj`, and its last commit carries `Closes-Bead: coding-harness-f6qj`.
- Special runs: none.

## Open decisions

None open. [DETAIL] A four-hour phase-4 appetite is a reversible stop for this bounded fix; it keeps the investigation and regression proportionate to the stated scope.
