---
title: "Decisions — harness-decide-adr"
status: accepted
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-3ar
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# harness-decide-adr — Decisions

Phase 1a (interview), held with the maintainer on 2026-09-30, against
`research.md` section 7. The maintainer works from a phone during a trip and
cannot sign anything with the Secure Enclave key until they are back at the
laptop; that constraint shaped the answer to Q2.

Scope split set by the maintainer at the start of the session: everything
specific to Coding Harness is done here; everything specific to LakeSwitch
runs in a parallel session in lakeswitch-ai.

## Answers

1. **Q1 — what must be true on the pilot's expiry date: option (b).**
   Coding Harness builds the mechanism, with its tests. LakeSwitch switches in
   a change of its own, in lakeswitch-ai, together with the pin mechanism
   (`harness.lock.yaml`, LakeSwitch decision D-21). The later date is already
   signed: lakeswitch-ai PR #68 (merged 2026-09-30) moved the pilot's
   `expires` from 2026-10-15 to 2026-12-15. This change therefore ends with
   the mechanism merged in Coding Harness; it touches nothing in lakeswitch-ai.
   Derived from the maintainer's scope split above rather than asked
   separately; the maintainer was told so and did not object.

2. **Q2 — signature check in scope: option (a).** This change ports only the
   ADR answer: the gate and the command. The signature check, with the fix of
   bead `coding-harness-in1` (a new key can approve itself; a retired key
   turns its old commits red), is the very next change. Coding Harness holding
   its own history to signed decisions stays on the not-now list.
   Consequence, accepted: until the signature change lands, Coding Harness
   cannot tell whether an answer file was written by the maintainer or by an
   agent. The spec states this limit plainly. Nothing in this change needs a
   signature by the maintainer; the anchor of the signature change is signed
   after the trip.

3. **Q3 — which changes owe an answer: option (a).** LakeSwitch's four change
   classes (`spike`, `bounded`, `feature`, `architectural`) become a closed
   set in the spec frontmatter, together with `adr_question`; only `feature`
   owes an answer. No further class duties. The format stays identical to the
   pilot (`schema_version: 1`), so LakeSwitch migrates none of its signed
   answers or Feature anchors when it switches.

4. **Q4 — recovery after losing the only key: not asked.** It applies only if
   the signature check is in scope, and Q2 put it out. It moves with the
   signature change.

## Details left to the agent

The `[DETAIL]` items of `research.md` section 7 stand as proposed there: a
script now with the verb shape of `harness decide adr`, the pilot format kept
with `answered_by`'s role as configuration, no port of the pilot expiry. The
two items about the merge rule and historical key declarations belong to the
signature change and do not apply here.

## Follow-up owed in the tracker

- A bead for the signature change (port of LakeSwitch gate M-30 with the
  `coding-harness-in1` fix, and Q4), to be created by the tracker's writer.
