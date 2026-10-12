---
title: "Research — ledger-instance-layout"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-s9m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, criterion-ledger, kit, instances]
---

# Criterion-ledger gate on an instance layout — Research

Phase 1 for bead coding-harness-s9m, read against `origin/main` on
2026-10-12. Loop row L3-4 of change criterion-test-ledger (bead
coding-harness-909, ADR 0013) was rejected as a disclosed limit: the
`criterion-ledger` gate ships with enforcement `block` and exits 3 (cannot
measure) when `plans/changes/` is missing, so `make verify` turns red in an
instance whose plans are laid out differently. The bead asks to run the gate
against an instance layout before the first pinned release, or to decide that
it does not block on a missing root. Related: bead coding-harness-wpv (an
adoption date for instances that receive the gate later) and the adoption
record of change adr-owning-change (bead coding-harness-afa,
`decisions/adoption.yaml`, not yet merged).

## The instance read for this question

LakeSwitch (`lakeswitch-ai`, `origin/main` at `ce88eee`, read through the
GitHub API by the orchestrating session on 2026-10-12): `plans/changes/`
exists and holds 16 change folders; 15 carry a `plan.md` and 14 a `spec.md`.
None of the 15 `plan.md` files has a `## Criterion ledger` or a
`## Tests per criterion` heading (each counted 0). So the layout root is the
same as here; what differs is that every existing plan predates the ledger.

## Questions for the exploration

1. How `scripts/check_criterion_ledger.py` finds its input: the root it
   expects, what it does when `plans/changes/` is missing, when a `plan.md`
   has no ledger section, when a `spec.md` has no numbered criteria, and when
   a change is archived; which exit codes it uses and which tests pin each.
2. How `decisions/gates.yaml`, `scripts/ci_gates.py` and the `make verify`
   path treat exit 3 for a gate with enforcement `block`, and whether any
   gate already distinguishes "nothing to measure" from "cannot measure"
   (for example `check_adr_answers.py`'s "examined nothing", the
   `plans_registry.py` ramps).
3. How the gate travels with the kit (`scripts/kit/manifest.yaml`,
   `scripts/kit/probe.py`), and what an instance that pins the kit receives:
   the gate's entry, its enforcement, and any per-instance setting.
4. Which date or cut-off mechanisms exist today that would let an instance
   adopt the gate from a given day on (the `_bestand_ramp` /
   `_praesenz_ramp` of `plans_registry.py`, the interview-minimums gate's
   cut-off, anything in `decisions/`), so the change can reuse one.
