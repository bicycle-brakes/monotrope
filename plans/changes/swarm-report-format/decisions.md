---
title: "Decisions — swarm-report-format"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-4q9y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm]
---

# swarm-report-format — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a skip
below).

## SKIP · interview

status: skipped
reason: A bounded bug fix whose intent the bead already states — the research swarm's seats returned reports the runner rejected, and the change is done when a swarm explore completes with every seat's report accepted and a test pins the failing format (bead coding-harness-4q9y, class set by the maintainer on 2026-11-09). The decided report contract (ADR 0020, decision 5) stays as it is. What remains is mechanics, decided below with reasons; the plan card still goes to the maintainer before anything is built.

## Decided by the agent

[DETAIL] **The report contract itself does not change**: seven claims at
most, the listed fields, the topic-specific fields. Reason: it is decided
(ADR 0020); a model that sends eight claims or drops a required field has
broken it, and accepting that would change what the judge scores.

[DETAIL] **Extraction becomes tolerant of wrapping, not of content**: an
answer that holds exactly one JSON object in one fenced block, with prose or
tool residue around it, yields that object. An answer with two candidate
objects stays invalid. Reason: three of seven rejections in run 1938a24f
were a complete report behind one sentence of prose or before tool residue
(research.md, orchestrator addendum).

[DETAIL] **A rejected seat is asked once more with the reason**, as the
review loop already does for a malformed answer (bead coding-harness-70rw);
a second rejection fails the seat as today. Reason: the remaining four
rejections were small contract breaks a model can correct when told which
one; the budget rule of the swarm has to cover the one extra call, and the
draft states how.

[DETAIL] **Unknown extra fields stay a rejection**, answered by the one
repeat above rather than by dropping the field silently. Reason: a silently
dropped field hides that a model wrote outside the template.
