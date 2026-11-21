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
