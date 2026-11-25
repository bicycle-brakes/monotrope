---
title: "Decisions — review-diff-4000"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, review-loop, diff-bound]
---

# review-diff-4000 — Decisions

## SKIP · interview

status: skipped
reason: The maintainer stated the change in the bead itself (coding-harness-mwzv.4, created by the maintainer on 2026-11-20 after asking whether the 2,000-line bound could be raised a little for now): raise `REVIEW_DIFF_MAX_LINES` from 2,000 to 4,000 as interim relief until multi-part diff splitting (coding-harness-hchx) lands, with the measurement it rests on (~44,000 tokens per 2,000 lines, smallest admitted window 256,000 tokens, Pi compaction off so an overflow fails as `CallFailed`). The class is `bounded` and the bead leaves no open choice for an interview to settle; skipped by the orchestrator in night run 2026-11-20-a under the maintainer's standing instruction to decide by recommendation overnight.

## Details decided by the orchestrator

[DETAIL] **D-1 (the earlier four-parts ceiling)**: the 2026-10-26 "at most four parts of 2,000 lines" figure belongs to the diff-splitting design (coding-harness-hchx) and is not changed here; this change moves only the single-part bound. Reason: the bead names hchx as the later, separate change.

[DETAIL] **D-2 (historical texts)**: research notes, handovers and the merged decision record of `adr-0021-consumed-ladder` keep their "2,000" wording as records of their dates; only living documentation (`docs/WORKFLOW.md`, `docs/how-it-works.md`) and the constant move. Reason: house rule 5, a number carries its cut-off.

[DETAIL] **D-3 (the 45-minute round deadline)**: unchanged; a longer diff on the parked lane's path (coding-harness-8kht) is measured after the change, not guessed now. Reason: the bead asks for the bound only.

## Q-1 · Ambiguity S-1 (one 4,000-line constant across all review-loop stages)

asked: 2026-11-21
answer: "One constant, 4,000 for every stage including the free stage; the spec's protected area that shields the free stage from widening is removed."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 ambiguity row S-1 of review-diff-4000.
  Intention: clarify whether the free stage keeps a separate 2,000-line bound or shares the raised 4,000-line constant.
  Today: `_review_round` and `free_probe_prompt` pass `free_diff`'s output through `bounded_review_diff`, which cuts at `REVIEW_DIFF_MAX_LINES`; `free_diff` itself can overshoot 2,000 up to ~2,400 lines.
  Repository change: `scripts/stage2.py` (`REVIEW_DIFF_MAX_LINES = 4000`, `free_diff` constants unchanged) and `plans/changes/review-diff-4000/spec.md` (remove the protected area shielding the free stage from widening).
  Architecture change: none — keeps a single diff-line bound constant across all stages.

In the context of `bounded_review_diff` applying `REVIEW_DIFF_MAX_LINES` to the
free stage as well as paid stages, facing a spec protected area that forbade
widening the free stage, we decided to keep one 4,000-line constant for every
stage including the free stage and remove that protected-area shield (`free_diff`'s
own per-file/total constants remain unchanged), to achieve a single bound with
minimal code change, accepting that free rounds may carry up to ~2,400 lines
uncut — 2026-11-21

## Q-2 · Ambiguity S-4 (stage wording in the spec)

asked: 2026-11-21
answer: "The spec says only 'every round of the review loop'; the doctrine's stage names stay as they are."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 ambiguity row S-4 of review-diff-4000.
  Intention: align the spec wording across free stage, Flash swarm, and paid ladder without altering doctrine stage names.
  Today: spec intro/criteria say "paid review" while `docs/WORKFLOW.md` §4b separates Flash swarm ("the same bounded diff") from paid rounds and paid ladder.
  Repository change: `plans/changes/review-diff-4000/spec.md` (use "every round of the review loop") and `docs/WORKFLOW.md` / `docs/how-it-works.md` bound updates keeping stage names intact.
  Architecture change: none — wording aligns spec with the single shared constant.

In the context of spec wording that referred only to "paid review" while one
constant governs free, Flash-swarm, and paid-ladder rounds, facing doctrine
that separates those stage names, we decided that the spec states "every round
of the review loop" and the doctrine's stage names remain unchanged, to achieve
exact alignment between code and spec without rewriting stage taxonomy,
accepting that all three stages share the 4,000-line constant — 2026-11-21
