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
2. When a non-blocking gate declares a valve, the schema check rejects an `until` that is not an unquoted YAML calendar date in ISO form.
   *Refuted by:* A missing, quoted, malformed or impossible date passes; a YAML parsing failure is a rejection even if it cannot identify the gate.
3. When a non-blocking gate declares a valve, the schema check rejects a `bead` that is not `coding-harness-` followed by one or more lowercase letters or digits and zero or more dot-separated numeric child components.
   *Refuted by:* `bt8`, an empty component or a non-numeric child passes, or `coding-harness-bt8` or `coding-harness-73gi.4` fails.
4. When a non-blocking gate's reason contains a count, the schema check rejects it; a count is a run of decimal digits bounded on both sides by whitespace, the start or end of the reason, or a comma, colon, semicolon or parenthesis.
   *Refuted by:* `35 findings`, `90 days`, `(35)` or `35` passes, or a reason containing only `D-10`, `ADR-028`, `Python 3.12`, `coding-harness-bxxt.1` or `2026-10-05` as digit-bearing tokens is rejected as a count.
5. When a non-blocking gate has a valid valve whose `until` date is before the current UTC date, `--check-schema` reports the gate, date and bead without failing solely because the date has passed.
   *Refuted by:* An expired valve is silent, omits its identity or makes an otherwise valid schema check fail.
6. When a non-blocking gate has a valid valve dated on the current UTC date or later and a count-free reason, the valve rules accept it.
   *Refuted by:* A valid valve dated today or in the future is rejected by the new rules.
7. When a blocking gate has no valve, the valve rules leave it valid.
   *Refuted by:* A valid blocking gate is rejected for lacking a valve.
8. When a blocking gate declares a valve, the schema check rejects it.
   *Refuted by:* A blocking gate with a valve passes the check.
9. When the revised gate list is checked, `docs-links` names `coding-harness-bt8` in its valve and `markdownlint`, `lychee` and `research-currency` each name the rule-registry epic `coding-harness-73gi` in theirs.
   *Refuted by:* Any of those four gates names a different tracking item or has no valve.
10. When the revised gate list is checked, each existing non-blocking gate has an unquoted `until` date of 2026-12-19 and a count-free reason that retains its stated purpose.
    *Refuted by:* A date or reason differs from that requirement, including removal of the research-currency decision date or its intended end state.
11. When a reader consults the gate schema and catalog, both describe the valve's date, tracking item and warning-only expiry, and the generated catalog inventory shows each gate's valve date and bead.
    *Refuted by:* Either description omits a field or says expiry blocks, or a generated inventory row omits or misstates its valve values.
12. When a valid expired valve is read by a gate-list consumer other than `--check-schema`, that consumer emits no expiry notice.
    *Refuted by:* An expiry notice appears in generated catalog or workflow output, command TSV or another consumer's output.
13. When the changed schema is checked, its version is the integer 4.
    *Refuted by:* Version 3 or a non-integer passes, or integer 4 fails solely on version.
14. When a non-blocking gate fails during verification, its existing report-only behavior remains unchanged.
    *Refuted by:* A report or advisory failure becomes a blocking failure locally or in the generated hosted workflow.

## Non-goals

- Automatically switching enforcement, introducing a blocking deadline, or changing the three existing enforcement levels.
- Reusing or changing rule ramps, creating a rule registry, validating tracker state or existence, or repairing the documentation corpus.
- Translating existing German text or changing unrelated gate reasons and counts; the docs-links reason stays German with its count removed.

## Protected areas

The local verification scheduler and rule-ramp machinery stay unchanged: this change adds a schema obligation, not a new execution route or a rule ramp.

## Definition of Done

- `make verify` green; the gate schema check reports expired valves without failing for expiry alone.
- `decisions/gates.yaml` and `docs/governance/gate-catalog.md` move with the code in the decision pull request; the generated workflow is regenerated only if its bytes change.
- The protected areas stay untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-73gi.4` and its last commit carries `Closes-Bead: coding-harness-73gi.4`.
- Special runs: none.

## Open decisions

- [DETAIL] The `until` date is inclusive and today is the UTC date, so expiry is consistent between local and hosted runs.
- [DETAIL] The count token boundaries are explicit in criterion 4, so identifiers and dates are not mistaken for counts; spelled-out numbers are outside this check.
- [DETAIL] Additional keys in a valve mapping are ignored, consistent with the existing gate-row treatment; only `until` and `bead` are required here.
- [DETAIL] The proposed date and tracking items in criteria 9 and 10 are review points, not promises that deliberately non-blocking gates will flip; the decision pull request puts these proposals to the maintainer.
