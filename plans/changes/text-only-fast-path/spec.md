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
`decisions/` or `.github/`, and no Markdown file read by a test. Use the test
inventory at the investigation's recorded source revision for every historical
pull request; this is a simplification for a recommendation about the future.
Reads include live-tree globs and indirect reads by scripts run by tests. A
rename is eligible only if both its old and new paths satisfy these conditions.

**Markdown dependency:** a gate's result depends on a Markdown file's bytes,
path, presence or history. **Process gate:** every declared gate except pytest
and the kit probe (`leerprobe`).

**CI minutes:** elapsed hosted CI run time, not billable minutes or savings.
Count associated `pull_request` and `merge_group` runs and the `push` run for
the merge commit separately, including cancelled superseded runs and reruns;
show run attempts individually. Attribution of shared runs and unavailable or
indeterminate associations must be explicit, and a run must not be counted
twice in the total. Eligibility uses the final pull-request diff, even for an
intermediate run with a different diff; identify such runs where known.

**Research note:** the new `docs/research/2026-11-21-text-only-fast-path.md`;
the change's `research.md` links to it.

## Acceptance criteria

Unless the time limit or unavailable evidence is reported under criteria 5 or
8, the completed note must contain each part below.

1. The research note identifies for every gate in `decisions/gates.yaml`
   whether it has a Markdown dependency, with evidence or an explicit unknown.
   *Refuted by:* a declared gate is omitted or its classification is asserted
   without evidence or an explicit unknown.
2. The note inventories Markdown paths and patterns read by tests, including
   live-tree globs and indirect reads, with source references, the current
   matches of each glob, a repeatable search method and unresolved dynamic reads.
   *Refuted by:* a test read found by anyone, including a reviewer, is omitted,
   or an unresolved dynamic read is silently treated as a known-safe path.
3. The note lists, for each of pytest and the kit probe, the test files over
   Markdown that skipping it would omit, derived from the test-read inventory,
   and the documentation faults those tests can detect that remaining checks
   would miss, or states where coverage cannot be established.
   *Refuted by:* an omitted applicable test file or candidate, an unsupported
   coverage claim, or an unstated uncertainty.
4. The note reports CI minutes for eligible text-only pull requests merged
   since 2026-11-01, with a dated cutoff and per-pull-request and per-run
   evidence sufficient to reproduce the totals and their attribution.
   *Refuted by:* a qualifying accessible pull request is excluded without
   explanation, an ineligible one is counted, or the total cannot be traced to
   the recorded runs or jobs.
5. When CI data or path classification is unavailable, the note reports the
   affected items and measurement limits rather than presenting the measured
   total as complete.
   *Refuted by:* an inaccessible run or indeterminate path is silently omitted
   while the total is presented as complete.
6. The note recommends an option, compares at least two alternatives and
   states each alternative's risks and consequences.
   *Refuted by:* only one alternative is assessed or an alternative lacks its
   risks or consequences.
7. The note describes a candidate fast path that retains every process gate
   and tracker hydration, considers only pytest and the kit probe for skipping,
   and puts their conditions on the steps in the `gates` job while leaving the
   required `verify` aggregator present and unchanged.
   *Refuted by:* the candidate skips any other gate or tracker hydration,
   changes the required aggregator, or relies on a workflow path filter that
   can leave the required check pending.
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
- CI verifies the resulting text-only change; the author's local `make verify`
  is skipped under the text-only rule, while the runner's required full check
  before phase 6 still runs.
- The protected areas and non-goals are checked against the pull request's file
  list. No ADR or living capability spec changes are due.
- The pull request closes `coding-harness-is4h` and its last commit carries
  `Closes-Bead: coding-harness-is4h`.
- Special runs: none beyond the historical CI measurement.

## Open decisions

- [DETAIL] Count both sides of a rename for eligibility: this conservative,
  reversible measurement choice avoids hiding an excluded path.
- [DETAIL] Report elapsed run or job time with its unit and scope rather than
  assuming billing data is available; use run time to keep the total consistent.
- [DETAIL] Count live-tree and indirect test reads at the investigation's
  source revision, including both rename paths, so reviewers can repeat one
  conservative inventory across the historical sample.
- [DETAIL] Classify path, presence and history dependencies as Markdown reads,
  and classify all gates except the two skip candidates as process gates, so
  path-sensitive failures and the remaining checks are visible.
- [DETAIL] List the test files omitted by each candidate and the glob matches,
  because a sample fault alone would understate coverage.
- [DETAIL] Put conditional skips on the existing `gates` steps and leave the
  required `verify` aggregator unchanged, preserving the required check.
- [DETAIL] Separate pull-request, merge-group and merge-commit push runs and
  their attempts, including cancellations and reruns, to expose the observed
  CI time and its limitations without conflating it with savings.
- [DETAIL] Name the research note and link it from the change research so its
  location is unambiguous.
- [DETAIL] Keep the runner's full pre-review check; this spike does not alter
  the runner's verification rules.
  No maintainer decision is open.
