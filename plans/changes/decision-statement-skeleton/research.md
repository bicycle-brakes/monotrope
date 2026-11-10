---
title: "Research — decision-statement-skeleton"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-nr6h
owner: Data Architect
provenance: human-written
tags: [research]
---

# decision statement skeleton — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the change — from the bead, 2026-11-10

Written by the orchestrator before the first exploration, because an
explorer cannot read the tracker (bead coding-harness-nr6h).

Class: bounded.

A decision record in `decisions.md` needs a decision statement: one sentence
that begins "In the context of", names what was decided and what is accepted
with it, and ends with its date. A draft may not edit `decisions.md`, and the
document checks refuse a record without the statement. In the night of
2026-11-10 two changes (verify-slots, review-fewer-rounds) lost all three
draft attempts each on the missing statement alone.

Wanted: no draft starts without the statements. The skeleton that
`make change` writes and the interview prompt should lead to a statement for
every answered record, and its accepting clause — the downside the
maintainer accepts — is asked from the maintainer, not invented.

To explore: which gate requires the statement and what exactly it checks;
what `scripts/new_change.py` writes today; what the interview prompt
(`prompts/`) says about recording an answer; whether the `draft` verb could
refuse early, before a model call, when a statement is missing; which tests
pin these today.
