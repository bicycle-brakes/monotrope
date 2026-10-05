---
title: "ADR 0009 — An architecture delta in design.md replaces the model as code, and decisions D-15 and O-3 are amended"
category: adr
status: accepted
created: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr]
---

# ADR 0009 — An architecture delta in design.md replaces the model as code, and decisions D-15 and O-3 are amended

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends decisions D-15 (model as code)
  and O-3 (architecture detection) of the 2026-09-16 interview; supersedes
  no ADR.
* Review: direction chosen by the maintainer, 2026-10-05, after the research
  note `docs/research/2026-10-05-likec4-roadmap-arc42.md` (its option (c)
  in section A6, with the revisit triggers of A7; the note travels in pull
  request #69) · the acceptance is the merge commit and is written nowhere
  else, so the header's `review` stays empty (ADR 0008) · Decider:
  maintainer · prepared by a Claude Code session
* Date: 2026-10-05 · takes effect on merge

## Context

Two decisions of the 2026-09-16 interview put an architecture model as code
into the kit. The continuity table of the current target carries both as
"Retain" (`docs/architecture/2026-09-17-omnigent-first-target.md`,
"Decision continuity"):

* **D-15 (model as code):** the kit ships LikeC4 with a specification that
  pins the four C4 element kinds (system, container, component, code),
  arc42 and MADR templates, and a `likec4 build` gate for applicable
  architecture changes.
* **O-3 (architecture detection):** an Architectural change requires an ADR
  and a model diff; a module created, deleted or renamed under `src/` or
  `spec/` in a change of any other class is DRIFT, with "check the class".

Neither is built (2026-10-05, at `3851f9c`): no LikeC4 file, no
specification, no build gate, and nothing checks O-3's BLOCK. The one
Architectural change so far, pull request #60, ran without a model diff.

The research note of 2026-10-05 measured LikeC4 and its alternatives:

* **A new runtime.** LikeC4 1.59.4 needs Node.js ≥ 22.22.3; the trial
  install took 118 MB. With 27 releases in twelve months, a pin in this
  Python-only repository either moves about monthly or ages.
* **The strictness D-15 relied on is not there.** `likec4 validate` checks
  the model against itself. A `system` nested inside a `component` passed
  as "Valid", so the pinned specification does not keep the C4 hierarchy —
  the reason D-15 gave for choosing LikeC4.
* **GitHub renders Mermaid, not `.c4`.** The maintainer reads pull requests
  on a phone; a Mermaid block in `design.md` arrives there, a LikeC4 model
  needs a built site or exported images.
* **The gain is small at this size.** Coding Harness's architecture is about
  ten boxes at container level (estimate). A model as code pays when many
  views share elements or an agent queries dependencies through its MCP
  server.
* **No defect so far** that a model delta would have caught (keyword search
  of the review findings in six change folders).

LakeSwitch declined the same thing. Its D-58 ("No architecture model as code
for now", ratified 2026-09-26) names the touched elements as the existing
diagrams and ADRs name them, lets the ADR record the decision, and revisits
when a review records, for the third time, a defect that a model delta would
have caught. Its decision record lists, as owed by Coding Harness, "decision
O-3 without the model diff, which D-58 declines". While D-15 stands, the kit
ships what its first instance refused.

D-14 (the design phase 2b) stays, and the template bundle (bead
coding-harness-9qo) brings its `design.md` into the kit. That file needs a
section for the architecture change that does not depend on a tool nobody
runs.

## Decision Drivers

* The picture arrives inside the pull request, readable on a phone.
* No new runtime in the kit without a measured need.
* The kit does not ship what its first instance declined: Coding Harness and
  LakeSwitch say the same thing.
* An Architectural change still leaves a record (the ADR) and a picture.
* The way to a model as code stays open, with conditions that are visible
  when they arrive.

## Considered Options

From the research note, section A6:

* (a) **Build LikeC4 now, as D-15 says.** 3–6 hours before the first use
  (estimate), Node.js in CI, a model nobody reads on a phone, and still no
  hierarchy check. The contradiction with D-58 grows.
* (b) **Defer: D-15 stands, with revisit triggers.** Nothing to build now.
  But the target keeps promising a gate nothing builds, no Architectural
  change can meet O-3's BLOCK, and the two repositories keep disagreeing in
  writing.
* (c) **Amend D-15 and O-3 by one ADR.** The architecture delta lives in
  `design.md` as a Mermaid flowchart plus lists of what is added, changed
  and removed; LikeC4 is named as the upgrade path, with triggers. No new
  dependency; agrees with D-58. Lost until a trigger fires: model queries
  through MCP, one definition for many views, safe renames.
* (d) **Drop architecture pictures entirely.** The simplest kit, but it
  undoes the phase-2b delta just kept, and quality goal 8 and scenario Q10
  of `docs/architecture/target-architecture.md` lose their picture.

## Decision

**(c)**, with these contracts:

* **The architecture delta lives in the change's `design.md`.** A section
  "Architecture delta" holds:
  1. a Mermaid diagram — a flowchart, the form GitHub renders — of the part
     of the system the change touches, as it is after the change, each box
     labelled with its C4 level (person, system, container, component);
  2. below it, three short lists of elements and relationships: **added**,
     **changed**, **removed**.

  If nothing architectural moves, one sentence says why.
* **No model as code in the kit now.** No LikeC4 specification, no `model/`
  scaffold, no `likec4 build` or `likec4 validate` gate, no Node.js
  dependency. Elements are named as the existing diagrams and ADRs name
  them, as in LakeSwitch's D-58.
* **D-15 is amended.** Its LikeC4 part — the tool, the pinned specification
  and the build gate — is replaced by the architecture delta. Its arc42 and
  MADR templates are not touched by this ADR; when the kit ships them stays
  with the template work.
* **O-3 is amended in one clause.**
  * **Kept:** an Architectural change requires an ADR in the same pull
    request. The ADR duty for architectural changes is unchanged.
  * **Changed:** "and a model diff" becomes "and a filled 'Architecture
    delta' section in its `design.md`".
  * **Not touched:** the DRIFT rule for a module created, deleted or renamed
    under `src/` or `spec/` in a change of another class.
* **LikeC4 stays the upgrade path.** The question returns, as an ADR of its
  own, when any one of these happens:
  1. a review records, for the third time, a defect in an Architectural
     change that a model delta would have caught, and the reviewer names it
     as such in `findings.md` — LakeSwitch's D-58 trigger, so both
     repositories move together;
  2. the same element appears in three or more architecture pictures, and a
     rename or split had to be made by hand in more than one of them;
  3. the model grows past about thirty elements — more than one page holds —
     and an agent's work needs dependency queries across it.

## Consequences

* **LakeSwitch's D-58 is no longer contradicted.** The kit asks for no model
  as code, and the item LakeSwitch lists as owed by Coding Harness ("O-3
  without the model diff") is answered here. Nothing in LakeSwitch has to
  change for this ADR; its own design section ("Design Impact", its D-22)
  and this delta can converge in a change of their own.
* **Lost until a trigger fires:** one definition shared by many views, safe
  renames, and dependency queries through LikeC4's MCP server. At about ten
  elements they would buy little; the triggers watch for the point where
  that stops being true.
* **When a trigger fires, the tool is looked at again.** The research note
  found that Structurizr keeps the C4 hierarchy and LikeC4 does not (its
  A2 and A7). LikeC4 is the named path; the ADR a trigger opens may still
  compare the two.
* **Presence can be checked, truth cannot.** Whether the section is filled
  is a check for the change-artefact validator (bead coding-harness-jc3);
  whether the delta is right stays the reviewer's question in phase 6, as
  it would have been with a model.
* **O-3's BLOCK is still not built.** This ADR changes what it asks for,
  not whether a gate enforces it.
* **The watched paths are not decided here.** Coding Harness has neither
  `src/` nor `spec/`, so O-3's DRIFT rule watches nothing in this
  repository. The note's option (c) proposed making the watched paths an
  instance setting; that stays open for a decision of its own.
* **Earlier wording is history.** Where the target document, the
  implementation plan, the gap analysis (P1) or
  `docs/architecture/target-architecture.md` (quality goal 8, row 2b of
  the phase table, §9.1 to §9.3, scenario Q10) name LikeC4, a model as
  code, a model diff or a model-as-code delta, they record the earlier
  design; the "model-as-code delta" of phase 2b now means the architecture
  delta. The target document
  and the implementation plan carry a notice at their top, and the
  continuity table marks D-15 and O-3 "Amend".
* **The kit's design template carries the section.** The template bundle
  (bead coding-harness-9qo) adds `templates/design.md`, whose "Architecture
  delta" section cites this ADR.

## Validation

* `python3 scripts/check_decision_continuity.py` is green: D-15 and O-3 map
  to this ADR in its `AMENDMENT_ADRS`, and this ADR names both.
* The continuity table marks D-15 and O-3 "Amend", with the date and this
  ADR.
* No kit file ships LikeC4, and the gate list has no LikeC4 gate:
  `grep -ri likec4 templates/ scripts/kit/ decisions/gates.yaml` finds
  nothing.
* The first Architectural change after this ADR carries a filled
  "Architecture delta" section in its `design.md`. The nearest candidate is
  the Kubernetes gate runner (`docs/research/2026-09-26-kubernetes-gate-runner.md`).
