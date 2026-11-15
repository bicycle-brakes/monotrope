---
title: "Decisions — swarm-citation-feedback"
category: decisions
status: draft
implementation_status: none
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-t2wm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, citations, correction-prompt]
---

# swarm-citation-feedback — Decisions

Class: bounded (bead coding-harness-t2wm).

## Q-1 · Repair the present citation form, or replace it with runner-issued ids

asked: 2026-11-14
answer: "Klein reparieren, Ausweise als eigener Bead (Empfohlen)" — this change makes the four small repairs; citations by runner-issued ids become a change of their own (bead coding-harness-z3d2, class feature) with its own explore and interview.
answered_by: maintainer
status: answered
context: |
  Topic: how a seat of the research swarm cites a source; today it writes free text ("path::heading") and the runner checks afterwards whether the place exists.
  Intention: the maintainer asked whether something other than Markdown heading text gives more safety and compliance; the answer sets the size of this change, and the explore of the change verify-result-reuse (bead coding-harness-bxxt.2) waits for it.
  Today: a heading cited with its # marks is refused, and the seat is not told which citation failed or why (confirmed by the explore of this change).
  Repository change: the small repair is four edits, in the reference resolver, the correction prompt and two prompt texts; ids issued by the runner would touch the prompts, the validator, the judge and every swarm test.
  Architecture change: none for the small repair; runner-issued ids change the report format of the swarm.

In the context of three explores in a row that stayed incomplete, facing a choice between a small repair of the present citation form and a closed list of citable ids issued by the runner, we decided for the small repair now and the ids as a change of their own, to achieve a working swarm quickly for the change that waits, accepting that free-text citations and their spelling faults remain possible until the second change. — 2026-11-14

## Decided by the agent

[DETAIL] **The four repairs are those the diagnosis of 2026-11-14 names** (notes of bead coding-harness-bxxt.2): a leading run of # marks is dropped before a heading is compared; the correction prompt carries each failing citation with its reason; the report prompt gains one Markdown citation example; the online brief names a fetch budget. Reason: each sits at the choke point of its fault and was reproduced or read in the run 6ebe4331; whether a timed-out seat is replaced stays out, because that is a scheduling rule, not a citation rule.
