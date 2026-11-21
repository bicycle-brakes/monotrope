---
title: "Decisions — advisory-gate-valve"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-73gi.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, gates, valves]
---

# advisory-gate-valve — Decisions

Class: bounded (bead coding-harness-73gi.4).

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> docs-links is enforcement: report with a free-text reason that has aged: it names 35 findings, the tool reports 199. Extend ci_gates.py --check-schema: a gate that is not block names a valve with an until date and a bead, and its reason carries no count.

## SKIP · interview

status: skipped
reason: The bead fixes the rule, the place (`ci_gates.py --check-schema`) and the trigger case (docs-links); the maintainer asked for no question windows until the block on 2026-11-23 10:00. The explore's open points are [DETAIL] items below; the maintainer's veto on the Plan Card stays, and because the change edits the human-decided `decisions/gates.yaml`, its pull request is a decision pull request the maintainer merges.

## [DETAIL] items decided by the orchestrator

- **Where the valve lives: a field of the gate row in `decisions/gates.yaml`,** `valve: {until: YYYY-MM-DD, bead: coding-harness-…}`, required on every gate whose `enforcement` is not `block`. It is not a Regelwerk `Ramp` (the Regelwerk test allows ramps outside a rule only for `lint-*` and `provenance-review`), and not the future rule-registry YAML. Reason: the bead names the schema check; one field beside the enforcement it qualifies.
- **What `--check-schema` refuses:** a non-block gate without `valve`, an `until` that is not an ISO date, a `bead` that is not a bead id, and a `reason` that contains a count (a number followed by a noun such as findings, errors, files, or a bare integer standing for one). An `until` in the past is reported, not refused, so an expired valve shows up without breaking every pull request. Reason: the bead, plus a soft landing for aged valves.
- **Existing non-block gates get their valves in the same pull request:** each gets the bead that tracks its flip (for docs-links the bead its current reason names) and an until date the orchestrator proposes as four weeks out; the counts leave their reasons. The maintainer decides the dates on the decision pull request. Reason: the schema must be green the moment it lands.
- **Docs:** the gates schema comment and the gate catalog describe the field. Reason: the living docs follow the schema.
