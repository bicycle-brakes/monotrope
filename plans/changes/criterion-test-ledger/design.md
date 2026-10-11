---
title: "Design — criterion-test-ledger"
category: design
created: 2026-10-11
updated: 2026-10-11
status: draft
implementation_status: none
date: 2026-10-11
last_reviewed: 2026-10-11
supersedes: null
superseded_by: null
bead: coding-harness-909
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [design, gates, tests, acceptance-criteria]
---

# Design — `criterion-test-ledger`

Phase 2b runs only because the maintainer asked for an ADR (2026-10-11,
`decisions.md` Q-4 and Q-5). The spec's non-goal "No architecture beyond the
ADR" limits this file to the ADR draft: every other part says in one sentence
why it has nothing to add.

## Alternatives

Not weighed again here: the research note
(`docs/research/2026-10-08-holding-criterion-tests.md`, "Options") weighed the
four ways, the maintainer chose in `decisions.md` Q-1 to Q-5, and the ADR
draft below carries them as its considered options.

## Interfaces

None — the gate reads text files of the tree and prints lines with an exit
code, in the shape of every other check script, and nothing crosses a
boundary of the system.

## Data model

None — the ledger is a section of `plan.md` that phase 3 writes and phase 4
edits, and nothing else is stored.

## ADR draft

`docs/adr/0013-every-criterion-names-its-proof.md`, in the form of
`templates/adr.md`, travels in this change's pull request, which makes it a
decision pull request. It records the principle of Q-4 with its two reasons
and the reach of Q-5, and takes effect when the maintainer merges it (ADR
0008).

## Architecture delta

Nothing architectural moves: the change adds one check script and its entry
to the one gate list (`decisions/gates.yaml`), in the shape of the existing
gates, and one section to an existing artefact.
