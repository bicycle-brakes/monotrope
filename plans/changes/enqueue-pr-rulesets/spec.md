---
title: "Spec — enqueue-pr-rulesets"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-3wtk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, merge-queue]
class: bounded
appetite: 2
adr_files: []
---

# Spec — enqueue-pr-rulesets

The admission command accepts readable ruleset-only protection and the runner's released state line without weakening its other safeguards (bead `coding-harness-3wtk`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-27, PR #477 was reported refused because the branch was protected by a ruleset but the classic protection endpoint returned `Branch not protected (HTTP 404)`; the reader rejects that response even after reading the ruleset (research at main `f4352686`).
- The runner writes a `Loop state: ` line in a released loop block; the admission reader can reject it as an unrecognised table line when its contents contain a pipe (research, 2026-11-27). The live state contents were not independently checked.

## Acceptance criteria

1. When the branch reports protected and the classic required-checks endpoint returns HTTP 404 with `Branch not protected`, the required checks are taken from the successfully read applicable rulesets.
   *Refuted by:* the response is refused or a ruleset check is omitted.
2. When a required ruleset check is missing or unsuccessful on the verified head in that situation, admission is refused under the existing check policy.
   *Refuted by:* the request is admitted without a passing required check.
3. When the classic required-checks endpoint returns another unreadable error, admission is refused under the existing fail-closed policy.
   *Refuted by:* an unrelated 404 or a 403 is treated as absent protection.
4. When a released loop block contains the runner's `Loop state: {…}` line, including a pipe in its state, that line alone does not cause a refusal. "The runner's line" means: the line starts with exactly `Loop state: ` and the rest, stripped of trailing spaces and tabs, parses with `json.loads` as a JSON object (S-1, reading b).
   *Refuted by:* a released block with the runner's line is rejected as an unrecognised table line.
5. When a different malformed pipe-bearing line occurs in a released loop block, admission is refused under the existing policy. This includes a `Loop state: ` line whose rest is not a JSON object (for example `Loop state: {not json | x}`), and any `Loop state:` line inside a `## Phase 6` block, where the runner never writes one (S-2).
   *Refuted by:* a different unrecognised table line, a non-JSON `Loop state:` line, or a `Loop state:` line in a `## Phase 6` block is silently accepted.

## Non-goals

Changing the runner's state format, required checks, merge policy, other admission prerequisites, or performing a real queue admission in tests is out of scope.

## Protected areas

The runner and its state writer remain unchanged; this repair belongs in the admission reader. Tracker data and repository settings are not changed.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with the code: none beyond this change's artifacts.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- Bead: the pull request closes `coding-harness-3wtk`, and its last commit carries `Closes-Bead: coding-harness-3wtk`.
- Special runs: none. The maintainer merges this admission-script change under the bootstrap exception.

## Open decisions

[DETAIL] The implementation appetite is two hours including repairs; this reversible stop limit keeps this bounded fix small. The runner's anchored state-line form is the recognition boundary, so a prefix alone does not exempt a malformed pipe-bearing line.

[DETAIL] Spec-review S-1..S-3 (round 1, decided under the bounded standing grant): S-1 reading b — a `Loop state: ` line is exempt only when its rest parses as a JSON object (AC4, AC5); S-2 — the exemption lives in `released_problems` only, not in the shared `malformed_table_line` helper, so `## Phase 6` blocks keep refusing the line (AC5); S-3 — `enqueue_pr.py` keeps its own copy of the `Loop state: ` prefix and does not import `scripts/stage2.py`, so the `script` self-check still covers everything the admission reads; a test pins the copy to `stage2.STATE_KEY` so drift goes red.
