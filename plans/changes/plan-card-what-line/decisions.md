---
title: "Decisions — plan-card-what-line"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-kg8n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, plan-card]
---

# plan-card-what-line — Decisions

Class: bounded (bead coding-harness-kg8n).

## The bead (read from the tracker by the orchestrator, 2026-11-22)

> Why: on 2026-11-11 the maintainer asked 'was mach das bead' at the first of four plan cards; the card's fields (For you, Done when, Appetite, Not now, Pre-mortem) say what is delivered and checked, but not in plain words what the change does and why. […] Maintainer, 2026-11-11: 'das muss jetzt immer in die plankarte, lege einen bead dafür an'. What: every plan card carries, in plain words and readable without the spec, what the change does — the problem today with one concrete example, what changes, and the main risk. Touches prompts/03-plan.md (card form), the plan template/validator that checks the card, and the runner's draft prompt if it builds the card; the orchestrator's preface before the card stays.

## SKIP · interview

status: skipped
reason: The maintainer stated the requirement on 2026-11-11 (quoted above) and the bead names what the card carries and which files move; the maintainer asked for no question windows until the block on 2026-11-23 10:00. Related feature bead coding-harness-6xx (a full card redesign with research) stays separate; this change only adds the plain-words content. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **One new first field, `What:`,** of at most three short sentences in plain words: the problem today with one concrete example, what changes, the main risk. The existing five fields stay in their order after it. Reason: the bead's three parts, read first.
- **The check:** the plan-card check (the validator that reads the card today) refuses a card without a non-empty `What:` line, and a `What:` that only repeats `For you:`. Reason: the bead names the validator; a copy is not an explanation.
- **Card form in `prompts/03-plan.md`** and the template change together; `prompts/` is runner-held, so the prompt edit is an orchestrator hand edit after the accepted attempt, before phase 6.
- **Existing plans are not rewritten;** the check applies to plans whose spec date is after this change's merge (the adoption-day pattern). Reason: no churn in drafted lanes.
