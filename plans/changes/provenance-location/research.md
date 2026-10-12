---
title: "Research — provenance-location"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-3ar.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, adr-answers, provenance, kit]
---

# Provenance location for instances — Research

Phase 1 for bead coding-harness-3ar.1, read against `origin/main` on
2026-10-12. Package 1 of `docs/research/2026-10-11-adr-answer-pin-plan.md`
(row 7, the Coding Harness half): the Coding Harness command reads a root
`provenance.yaml` with `roles:`; LakeSwitch keeps `decisions/provenance.yaml`
without `roles:`, so the command refuses there. Coding Harness lets an
instance name where its provenance file lives; the default stays unchanged.
The package touches only `scripts/check_adr_answers.py`, `scripts/harness.py`
and their tests.

## Questions for the exploration

1. Where and how do `scripts/check_adr_answers.py` and `scripts/harness.py`
   (verb `decide adr`) find and read `provenance.yaml` today: path
   resolution, the `roles:` lookup, what they do when the file or `roles:`
   is missing, and which tests pin that.
2. Which ways exist in this repository for an instance to name a location
   (a command-line option, an environment variable, a key in a config file
   such as `model-endpoints.yaml` or the kit manifest), and which one other
   scripts already use, so the change follows the existing idiom.
3. Which other readers of `provenance.yaml` exist (gates, kit scripts,
   `scripts/kit/manifest.yaml`), so a change knows what stays on the default.
4. What the kit carries of these two scripts to an instance, and what an
   instance run would need to pass the new location.

The interview (phase 1a) needs the maintainer; this file stops before it.
