---
title: "Decisions — repair-line-skeleton"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-k93f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# repair-line-skeleton — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: the repair verb's prompt carries
one prefilled fixed line per taken row and its parser reads each completion;
the fixed-line format itself, gates, ADRs and architecture stay as they are.

## SKIP · interview

status: skipped
reason: the bead (coding-harness-k93f) states the remedy in full — the repair prompt carries one prefilled line per taken row (`<ID>: fixed — ` plus the row's kind, a test or not a test), the parser reads the model's completion of each, a missing or malformed completion fails only that row and the rest is still accepted — and the maintainer queued it on 2026-10-28 ("Ja") after repairs whose code was right failed on their answer lines (workflow-promises attempts 2 and 3, terms-test-fixtures attempt 3, red-first-pytest-failed attempt 1); no question remains that only the maintainer can answer. In the context of the repair verb's answer lines, facing repairs rejected for a malformed line although their code was right, we keep the maintainer's queueing of 2026-10-28 and let the runner write each row's line skeleton, to achieve that a model fills only the test or the reason, accepting that a row whose completion is unreadable still fails on its own. — 2026-10-31

## Details for the draft

[DETAIL] **The fixed-line grammar does not change.** The skeleton is the
existing `<ID>: fixed — tests/<path>::<function>` or `<ID>: fixed — not a
test — <reason>`; only who writes the prefix changes. Reason: the loop record,
findings and gates read that grammar.

[DETAIL] **The kind comes from the row's Status.** `taken — not a test — …`
prefills the not-a-test form, every other taken row the test form. Reason:
the orchestrator decides the kind when it takes the row.

[DETAIL] **One bad line fails one row.** The other rows' fixes are still
accepted and marked. Reason: the bead's test.
