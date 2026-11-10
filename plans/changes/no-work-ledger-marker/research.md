---
title: "Research — no-work-ledger-marker"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-twbl
owner: Data Architect
provenance: human-written
class: bounded
tags: [research]
neighbours:
  - plans/changes/no-work-done/spec.md
---

# no work ledger marker — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-twbl, class bounded, a follow-up of phase-6 finding F-1
of the change no-work-done (bead coding-harness-te7q, merged with pull
request #360 on 2026-11-10). The no-work check rejects an implement or repair
attempt that changed only the runner's own bookkeeping. The gap: a rejected
attempt leaves a new test; the retry restores the ledger marker `not yet
written`; verification clears the marker again; and the path-only candidate
filter counts that ledger edit, which the runner itself made, as work of the
model. The finding was reproduced in memory with `clear_written` and
`attempt_has_work`. Wanted: the clearing of a ledger marker by the runner is
discounted before the check decides whether there was work; a retry whose
only change is that clearing is rejected as no work done.

Questions for the exploration: where `attempt_has_work`, `clear_written` and
the candidate filter live in `scripts/stage2.py` and in which order they run
within one attempt; which other runner-owned writes the check already
discounts and how (findings file, plan index, stamp-only edits, the plan's
time section); which tests of `tests/test_stage2.py` pin the check; what the
spec of no-work-done states about this accepted limit.
