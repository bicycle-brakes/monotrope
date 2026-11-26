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

1. When a research swarm resumes a stored incomplete run under the store's matching-resume rule (`changed_against_stored`, including after committing the first run's appended publication to `research.md` and its `updated:` restamp so `HEAD` has moved) with the same selection, each repository-topic prompt for topics 1–8 is byte-identical to its corresponding prompt in the first run.
   *Refuted by:* A corresponding prompt for any of topics 1–8 differs because of a run identifier, publication growth, `updated:` restamp, moved `HEAD`, timestamp, changing commit count or another non-frozen input.
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
5. When a repository-topic prompt for topics 1–8 is built on run 1 or on a matching resumed run, it preserves the finder map's resolved excerpts and (for topic 6) the `# Mapped history (data)` section derived from the first run's stored frozen inputs rather than omitting them.
   *Refuted by:* A repository-topic prompt drops mapped source excerpts or topic 6 drops `# Mapped history (data)` or lacks the history entries `validate_research_report` requires for commit citations.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

- Changing the frozen-binding or exact prompt-hash contract, the selection of seats, or the research swarm's availability and retry policies.
- Maintaining prompt-hash compatibility with slots stored under a pre-fix drifted prompt hash: pre-fix slots whose prompt hash still matches and validates are reused under criterion 4, and any pre-fix slot recorded under a drifted hash is recomputed once without clearing the store or relaxing validation.
- Repairing unrelated research-swarm failures or changing published research content beyond what the existing contract requires.

## Protected areas

Model configuration, leak checks, and unrelated changes remain untouched: this is a resume fix, not a change to security or model routing.

## Definition of Done

- `make verify` green; the two-run regression (including a committed publication between runs and non-empty mapped excerpts and topic-6 history) and the existing reuse boundary tests pass.
- Documentation or ADR changes: none expected.
- Protected areas and non-goals remain untouched, shown by the pull request's file list.
- The pull request closes bead `coding-harness-f6qj`, and its last commit carries `Closes-Bead: coding-harness-f6qj`.
- Special runs: none.

## Open decisions

None open.

[DETAIL] A four-hour phase-4 appetite is a reversible stop for this bounded fix; it keeps the investigation and regression proportionate to the stated scope.

[DETAIL] Spec-review S-1 (matching resume definition): Adopt Reading B — a matching resume follows the store's existing `changed_against_stored` contract, including resuming after committing the first incomplete run's appended `research.md` publication (moved `HEAD`, appended tail and `updated:` restamp). Repository-topic prompts (including map excerpts resolved from `research.md` and topic 6's `# Mapped history (data)`) derive from the stored first-run inputs rather than the moved `HEAD` or appended tail (decided under the bounded standing grant for non-BLOCKER spec-review rows).

[DETAIL] Spec-review S-2 (evidence preservation): Byte-identity is achieved by stabilizing/replaying the stored first-run inputs (criterion 5), never by dropping mapped excerpts or `# Mapped history (data)` from repository-topic prompts (decided under the bounded standing grant).

[DETAIL] Spec-review S-3 (pre-fix stores): Existing `plan_reuse` and `validate_research_report` checks stay strict (criterion 4 and Non-goals); pre-fix stored slots with matching hashes and valid results are reused, while pre-fix slots with previously drifted hashes are recomputed once without wiping the store (decided under the bounded standing grant).
