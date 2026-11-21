---
title: "Spec — advisory-gate-valve"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-73gi.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, gates, valves]
class: bounded
appetite: 4
adr_files: []
---

# Spec — advisory-gate-valve

Non-blocking gates carry a dated review point and a tracking item, and their reasons no longer embed counts (bead `coding-harness-73gi.4`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-21, `research.md` found that `docs-links` reported rather than blocked while its reason still named 35 findings; the bead read by the orchestrator records that the tool reported 199. Neither number is a live measurement in this spec.
- On 2026-11-21, `research.md` found four non-blocking gates in `decisions/gates.yaml`, none with a machine-readable date or tracking item; only the `docs-links` reason named a transition item.
- On 2026-11-21, `research.md` found that the existing dated rule ramps block once due, while three non-blocking gates were documented as deliberate end states. An expiry must therefore be visible without silently changing their enforcement.

## Terms

**Valve:** the date and tracking item attached to a non-blocking gate, identifying when its status needs attention; it does not itself change enforcement.

## Acceptance criteria

1. When a gate has `report` or `advisory` enforcement, the schema check rejects it unless it declares a valve mapping.
   *Refuted by:* A non-blocking gate without a mapping passes the check.
2. When a non-blocking gate declares a valve, the schema check rejects a missing or invalid calendar date in `until`.
   *Refuted by:* A missing, malformed or impossible date passes the check.
3. When a non-blocking gate declares a valve, the schema check rejects a missing or malformed repository bead identifier in `bead`.
   *Refuted by:* An empty or malformed identifier passes the check.
4. When a non-blocking gate's reason contains a numeric count, the schema check rejects that reason.
   *Refuted by:* A reason containing `35 findings`, `90 days` or a standalone count `35` passes.
5. When a non-blocking gate has a well-formed valve whose date is before today, `--check-schema` reports its gate, date and bead without failing solely because the date has passed.
   *Refuted by:* An expired valve is silent, omits its identity or makes an otherwise valid schema check fail.
6. When a non-blocking gate has a valid valve dated today or later and a count-free reason, the valve rules accept it.
   *Refuted by:* A valid current or future valve is rejected by the new rules.
7. When a blocking gate has no valve, the new valve rules leave it valid.
   *Refuted by:* A valid blocking gate is rejected for lacking a valve.
8. When the revised gate list is checked, every existing non-blocking gate has a valid valve and a count-free reason, and `docs-links` retains its existing tracking item.
   *Refuted by:* An existing non-blocking gate lacks either field, keeps a numeric count, or `docs-links` no longer identifies its corpus-correction item.
9. When a reader consults the gate schema and catalog, both describe the valve's date, tracking item and non-blocking expiry behavior.
   *Refuted by:* Either description omits a field or says expiry changes the enforcement or fails the schema check.
10. When a non-blocking gate fails during verification, its existing report-only behavior remains unchanged.
    *Refuted by:* A report or advisory failure becomes a blocking failure locally or in the generated hosted workflow.

## Non-goals

- Automatically switching enforcement, introducing a blocking deadline, or changing the three existing enforcement levels.
- Reusing or changing rule ramps, creating a rule registry, validating tracker state or existence, or repairing the documentation corpus.
- Translating unrelated German text or changing other gate reasons and counts.

## Protected areas

The local verification scheduler and rule-ramp machinery stay unchanged: this change adds a schema obligation, not a new execution route or a rule ramp.

## Definition of Done

- `make verify` green; the gate schema check reports expired valves without failing for expiry alone.
- `decisions/gates.yaml` and `docs/governance/gate-catalog.md` move with the code in the decision pull request; the generated workflow is regenerated only if its bytes change.
- The protected areas stay untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-73gi.4` and its last commit carries `Closes-Bead: coding-harness-73gi.4`.
- Special runs: none.

## Open decisions

- [DETAIL] A valve expires on the day after its `until` date; this makes the named date inclusive and avoids a partial-day deadline.
- [DETAIL] A numeric count is a standalone decimal integer, including one followed by a noun; digits inside identifiers and ISO dates are not counts. This deterministic boundary catches the aged examples without mistaking a bead identifier for a count; spelled-out numbers are outside this check.
- [DETAIL] The proposed dates are 2026-12-19, four weeks after the 2026-11-21 decision record; the maintainer decides them through the decision pull request. A tracking item must be evidenced, not invented.
