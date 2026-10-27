---
title: "Research — review-loop-deep-b"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-pc7g
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, review-loop]
---

# review-loop-deep-b — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), on
2026-10-25, against `origin/main` at `f8a6b33`.

## The finding

A deep read-only review of the review-loop runner (`scripts/stage2.py`,
part B, 2026-10-25, by an Opus 5.5 sub-agent of the orchestrating session)
reproduced fourteen defects without model calls, numbered DL-B-1 to
DL-B-14. Its repro tests ran green against `f8a6b33` (each prints the faulty
behaviour). This change fixes the runner defects among them; three are
doctrine or schema questions and go to the maintainer (`findings.md`).

## What exists today (read at `f8a6b33`)

- `review_loop` replaces a failed Flash member: it picks the next ladder
  rung, calls `checked_prompt` on it without catching `Refused`, appends
  the call line, runs it and adds it to `replaced`, which is consumed as
  `rung:<id>` together with the round (DL-B-1, DL-B-10).
- `excluded_problem` is read only by `checked_prompt`'s admission; the
  free selection (`discover_free`, `select_free`) and the paid ladder
  (`ladder`, `new_state`, `skipped_models`) apply `terms_problem` alone
  (DL-B-2).
- The text of an answer that is not rows is written after
  `NOT_ROWS_NOTE` with no member name (DL-B-3).
- `run_reviewer`, `fail` and `last_error_line` scrub the OpenCode key only;
  `GLM_KEY` lives in the same secrets file (DL-B-4). `docs/WORKFLOW.md`
  §4 says both keys are scrubbed from everything the runner prints or
  writes.
- `launch` starts each timed program in its own session and kills the
  group only on its own timeout; nothing kills it when the runner is
  interrupted (DL-B-5), and the drain after that kill has no time limit
  (DL-B-6).
- `parse_catalog` splits on whitespace, so a catalog id may hold `|`;
  `render_table` writes cells unescaped (DL-B-7).
- `_furniture` treats a line as the header only when its first cell is
  `ID` (DL-B-11).
- The Kimi entry under `ausgeschlossen` in `model-endpoints.yaml` has no
  `modelle`, so `excluded_problem` skips it as legacy prose (DL-B-12).
  `provenance.yaml` maps no prefix for `model-endpoints.yaml`; the file is
  not reserved for `human-decided`, and an agent commit added an exclusion
  before (`48ba7d6`, 2026-10-17).
- `run_reviewer` names "the reviewer time limit of 45 minutes" for every
  stop, also when the round deadline left a replacement seconds (DL-B-14).

## Sources

- The deep-review notes and their repro tests (session scratchpad, not in
  the repository), 2026-10-25.
- `scripts/stage2.py`, `scripts/stage2_availability.py`,
  `model-endpoints.yaml`, `provenance.yaml`, `docs/WORKFLOW.md` §4 and
  "The review loop (phase 4b)", ADR 0021, ADR 0007 decision 3 — all at
  `f8a6b33`.
