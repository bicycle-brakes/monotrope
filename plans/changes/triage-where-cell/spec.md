---
title: "Spec — triage-where-cell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-3ha6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, triage]
class: bounded
appetite: 2
adr_files: []
---

# Spec — triage-where-cell

Triage classifies locations in a review finding consistently, including bare file names, before recording a decision (bead `coding-harness-3ha6`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `056a7ee5`, triage reads the Where cell by a fixed position and uses a stricter location reader than repair. A bare test filename or test reference can fail classification; a slash in prose can also provoke a refusal. The prompt describes a finding as test-only even though the guard measures named locations, not the finding's remedy (`research.md`, Runner exploration, 2026-11-28).

## Acceptance criteria

1. When a Where cell names a uniquely identifiable tracked test file by its bare filename, with or without a `::test` suffix, triage classifies it as a test location.
   *Refuted by:* Plain `taken` succeeds for such a test-only cell, or the explicit test-only decision is refused.
2. When a bare filename matches more than one tracked file, triage refuses the decision without changing the record.
   *Refuted by:* A matching file is guessed or the record changes.
3. When a slash-bearing token does not name a tracked path, it does not count as a location for test-only classification.
   *Refuted by:* A prose slash or untracked slash-bearing token changes the classification or causes a location refusal.
4. When a Where cell names tracked test and non-test files, triage does not classify the row as test-only.
   *Refuted by:* Plain `taken` is refused solely by the test-only guard.
5. When the declared row columns are reordered or extended, triage reads the Where cell by its declared column name.
   *Refuted by:* The guard classifies a different cell or misses the actual Where cell.
6. When triage records a decision or refuses one, its existing status-only write and proof-mark protections remain in force.
   *Refuted by:* Another cell changes, a marked row is re-decided, or a refusal changes the record.
7. When the command help and review-loop instructions describe the test-only guard, they state that it applies to named locations, give the corrective form and retain ownership of the proof mark.
   *Refuted by:* Either text claims to infer the remedy from the finding, omits the correction, or assigns the proof mark to triage.

## Non-goals

Writing or normalizing Origin, accepting a single-colon symbol suffix such as `path.py:symbol`, changing repair-scope grants, or resolving the two observed stopped lanes are outside this bounded follow-up. They require separate scope. No ADR or design phase is due for a bounded change.

## Protected areas

The review-loop prompt is held for the orchestrator; the implementation attempt must not edit it. Other held paths are outside the implementation attempt as specified in the phase-3 prompt.

## Definition of Done

- `make verify` green on the implementation.
- The command help, tests and review-loop prompt move with the code in the same pull request.
- Protected areas and non-goals are checked against the pull request's file list.
- The pull request closes `coding-harness-3ha6`; its last commit carries `Closes-Bead: coding-harness-3ha6`.
- Special runs: none.

## Open decisions

[DETAIL] A bare name must identify one tracked file; ambiguity refuses instead of guessing, so a different repository layout cannot silently change the guard's result. Untracked slash tokens contribute no location, as the recorded scope requires. Origin and single-colon symbols are separate from the recorded follow-up scope.

[DETAIL] Spec-review S-1..S-9 (round 1, decided by the orchestrator under the bounded standing grant, 2026-11-28): S-1 reading A — a `::<test>` suffix comes off any token before the path lookup, so `tests/test_stage2.py::test_x` names `tests/test_stage2.py` and counts as test-only. S-2 reading A — triage adopts repair's shared location grammar (`where_named_tokens` / `_where_token_path`), so `./tests/x.py`, an absolute path inside the checkout and the directory token `tests/` name test locations exactly as repair reads them. S-3 reading A — an exact tracked path wins over bare-filename matches (today's behaviour, kept by `test_triage_matches_extensionless_root_locations_against_tracked_files`). S-4 — the refusal for an ambiguous bare name applies only to a plain `taken` and `taken — guard test`, where the test-only classification decides the outcome; `rejected` and `taken — not a test` are recorded without it, so they never need a hand edit of the reviewer's cell. S-5 — a slash-free token with a dot that matches no tracked file stays refused as an unrecognised location, as today. S-6 reading A — "declared row columns" is the `ROW_COLUMNS` constant of `scripts/stage2.py`; a test pins `scripts/findings_reader.py`'s copy equal to it. S-7 — `record_rows(strict=True)` stays the one row splitter (Status joined from position 7 to the next-to-last cell, the mark last); triage reads Where, Status and the mark from that split by `ROW_COLUMNS` index, and a test with escaped pipes inside Status proves the reading. S-8 — the orchestrator edits the held `prompts/04b-review-loop.md` in its own commit before the implement attempt; the attempt writes the test that checks the new wording. S-9 — after `::` come one or more `::`-separated Python identifiers, optionally ending in one `[...]` parametrise id; the line suffixes `:N`, `:N-M`, `#LN`, `#LN-LM` apply to bare names as to paths.
