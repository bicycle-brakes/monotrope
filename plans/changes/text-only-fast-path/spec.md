---
title: "Spec — text-only-fast-path"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-is4h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, spike, ci, fast-path]
class: spike
appetite: 2
adr_files: []
---

# Spec — `text-only-fast-path`

Produce evidence and a recommendation for a possible hosted CI fast path for
text-only pull requests (bead `coding-harness-is4h`). Research: `research.md`;
scope correction and interview skip: `decisions.md`.

## Problem

- The explore of 2026-11-21 mapped the local verification exception, not the
  requested hosted CI question; its correction in `decisions.md` identifies
  the missing gate inventory, historical CI measurement and recommendation.
- As recorded in `research.md` on 2026-11-21, the local text-only exception is
  prose and the existing verification paths select different subsets. That
  map alone cannot establish which hosted checks can safely be omitted.

## Terms

**Eligible text-only pull request:** a merged pull request whose changed paths
are all Markdown, with no path under `scripts/`, `tests/`, `prompts/`,
`decisions/` or `.github/`, and no Markdown file read by a test. A rename is
eligible only if both its old and new paths satisfy these conditions.

**CI minutes:** elapsed hosted CI run or job time as explicitly identified in
the report, not a claim of billable minutes or time saved.

## Acceptance criteria

1. When the research note inventories the declared gates, it identifies for
   every gate in `decisions/gates.yaml` whether it reads Markdown content,
   including an explicit unknown where the evidence is insufficient.
   *Refuted by:* a declared gate is omitted or its classification is asserted
   without evidence or an explicit unknown.
2. When the note inventories tests, it identifies Markdown paths or path
   patterns read by tests, with source references and unresolved dynamic reads.
   *Refuted by:* a discovered test read is omitted or an unresolved dynamic
   read is silently treated as a known-safe path.
3. When the note evaluates skipping the test suite and kit probe, it names
   documentation faults each could detect that remaining checks would miss,
   or states where that coverage cannot be established.
   *Refuted by:* either candidate is omitted or a coverage claim has no
   supporting evidence and no uncertainty is stated.
4. When the note measures hosted CI, it reports the CI minutes of eligible
   text-only pull requests merged since 2026-11-01, with a dated cutoff and
   per-pull-request evidence sufficient to reproduce the totals.
   *Refuted by:* a qualifying accessible pull request is excluded without
   explanation, an ineligible one is counted, or the total cannot be traced to
   the recorded runs or jobs.
5. When CI data or path classification is unavailable, the note reports the
   affected items and measurement limits rather than presenting the measured
   total as complete.
   *Refuted by:* an inaccessible run or indeterminate path is silently omitted
   while the total is presented as complete.
6. When the note presents a recommendation, it compares at least two
   alternatives and states each alternative's risks and consequences.
   *Refuted by:* only one alternative is assessed or an alternative lacks its
   risks or consequences.
7. When the note describes a candidate fast path, it retains all process gates
   and tracker hydration, considers only pytest and the kit probe for skipping,
   and keeps the required verify job present using conditions within that job.
   *Refuted by:* the candidate skips another process gate or tracker hydration,
   or relies on a workflow path filter that can leave the required check pending.
8. When the two-hour phase-4 budget expires, the investigation stops and
   reports completed evidence, missing work and any unmet criteria.
   *Refuted by:* work continues past the budget or unfinished evidence is
   represented as complete.

## Non-goals

- Implementing or enabling a fast path, changing local verification, or making
  the maintainer's CI decision; a later change would require its own decision.
- Building the missing stop hook or changing CI workflow path filters.
- Treating a historical duration as an observed future saving.

## Protected areas

`scripts/ci_gates.py`, `.github/workflows/ci.yml` and `decisions/gates.yaml`
stay unchanged: this spike researches the proposed behavior only. The rest of
the CI and local verification implementation also stays unchanged.

## Definition of Done

- The research note contains the evidence and recommendation above, or names
  the unmet criteria when the time limit or unavailable data stops the work.
- CI verifies the resulting text-only change; local `make verify` is skipped
  under the repository's text-only rule.
- The protected areas and non-goals are checked against the pull request's file
  list. No ADR or living capability spec changes are due.
- The pull request closes `coding-harness-is4h` and its last commit carries
  `Closes-Bead: coding-harness-is4h`.
- Special runs: none beyond the historical CI measurement.

## Open decisions

- [DETAIL] Count both sides of a rename for eligibility: this conservative,
  reversible measurement choice avoids hiding an excluded path.
- [DETAIL] Report elapsed run or job time with its unit and scope rather than
  assuming billing data is available; this keeps the result reproducible.
  No maintainer decision is open.
