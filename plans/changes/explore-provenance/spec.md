---
title: "Spec — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  - kind: llm-session
    name: codex
    version: "2026-11-09"
    model: gpt-6.1-sol
  - kind: llm-session
    name: claude-code
    version: "2026-11-09"
    model: glm-5.3
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, explore, provenance]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — `explore-provenance`

Explore publishes truthful research metadata, and a read-only census prevents
new metadata defects while the existing stock awaits its separate correction
(bead coding-harness-g19n — truthful Explore provenance).
Research: [research.md](research.md). Decisions: [decisions.md](decisions.md).
The maintainer's Q-4 answer of 2026-11-07 supersedes Q-1 through Q-3 only for
the one-time correction of existing files; publication and complete metadata
checking remain in scope.

## Problem

- Research dated 2026-11-04, “What exists today”, records that both Explore
  routes append model output while leaving the generated `human-written`
  header and empty-file notices. The read-only explorer cannot fix the output
  written by the runner.
- The same research records that currency and registry checks do not hold
  research provenance values, leaving these false declarations unreported.
- The maintainer's Q-2 and Q-3 answers of 2026-11-06 require the whole metadata
  contract and preservation of multiple producers. Q-4, dated 2026-11-07,
  defers the failed historical normalisation to its own change and explicitly
  accepts existing headers until then. Publication must be correct without
  making that historical repair a prerequisite for shipping.

## Terms

- **Publication** — an accepted single-model answer or a runner-written swarm
  record, including an incomplete swarm publication. A call audit alone, a
  failed answer, quoted text or a fenced example is not publication.
- **Active research** — every `plans/changes/<name>/research.md` directly under
  a change folder, excluding `archive/`; eligibility does not depend on its
  current provenance label.
- **Deferred stock** — the explicit failing active-research paths recorded in
  `UNCORRECTED` in `tests/test_explore_provenance.py` at commit `ff594213`
  (2026-11-09, applying Q-4). These paths are exempt from blocking on existing
  defects, not from being scanned. The set may only shrink.
- **Skeleton text** — only the generated opening empty-file paragraph and
  provenance-instruction blockquote from `scripts/new_change.py`. The title
  and authored quotations of those notices remain research.
- **Producer attribution** — one producer record, or a non-empty list for
  several known contributions. Records identify the producing program or
  swarm orchestration and its evidence-backed date; known model identities
  and earlier records in the input remain represented. A swarm orchestration
  record does not claim that one participant wrote the whole document.
- **Metadata contract** — exactly one top-level `provenance`, `produced_by`,
  `review`, `date`, `last_reviewed` and `updated` field, no duplicate keys in
  producer/review mappings, `ai-drafted-reviewed` provenance, non-empty producer
  attribution, and pending review with null approver and approval date. Each
  producer has `kind: llm-session`, an evidence-backed program name and an ISO
  calendar date string in `version`; known models are retained separately.
  Dates obey `date <= last_reviewed <= updated`, and producer dates lie within
  `date..updated`. Publication stamps the actual edit day without inventing
  a historical contribution or human review date.

## Acceptance criteria

1. When Explore publishes model research through Flash, its explicit Stage-1
   fallback or the research swarm, the resulting header declares exactly one
   `provenance: ai-drafted-reviewed`.
   *Refuted by:* any route publishes with missing, conflicting or human-written
   provenance.
   *Basis:* decisions.md#Q-1; decisions.md#Q-4.

2. When Explore publishes model research, the header identifies its producing
   program or swarm orchestration and evidence-backed publication date without
   discarding producer or model contributions already known from the input.
   *Refuted by:* missing or conflicting attribution, a wrong program or date,
   an entire swarm attributed to one model, or a producer list collapsed into
   one record. Unresolvable input attribution is refused rather than guessed.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; decisions.md#Q-4.

3. When Explore publishes model research, the resulting document's review is
   pending with no claimed human approval.
   *Refuted by:* missing or duplicate review metadata, retained approval for
   the extended document, or an invented approver or approval date.
   *Basis:* decisions.md#Q-1.

4. When Explore publishes into a generated research skeleton, its opening
   skeleton text is absent from the resulting document.
   *Refuted by:* either notice remains or a later publication reintroduces it.
   *Basis:* decisions.md#Q-1.

5. While publication corrects research metadata and opening notices, unrelated
   header fields and existing research body bytes remain unchanged.
   *Refuted by:* altered class, bead, owner, lifecycle state, historical dates,
   authored prose, audit lines, prior swarm envelopes, title or line endings
   outside the owned metadata and generated opening spans.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; decisions.md#Q-4.

6. If research cannot be prepared or its replacement fails before completion,
   the previous research bytes remain intact.
   *Refuted by:* an invalid input is rewritten, a failed replacement truncates
   research, or a partial header/body publication is left behind.
   *Basis:* decisions.md#Q-1; research.md, “What exists today”.

7. When the repository census runs, every active model-written research file
   outside the deferred stock must satisfy the metadata contract and have no
   opening skeleton text for the check to pass.
   *Refuted by:* a violating unlisted file passes, the census is skipped, or
   passing requires rewriting the deferred stock.
   *Basis:* decisions.md#Q-2; decisions.md#Q-4.

8. When an incomplete swarm publication is corrected and resumed, the runner's
   own correction preserves reuse of otherwise unchanged results.
   *Refuted by:* successful seats repeat solely because of the correction or
   a later calendar day, or foreign header/body/tail edits pass as the same input.
   *Basis:* decisions.md#Q-1; research.md, “Where it lives”.

9. While historical correction is deferred, census exemptions remain a subset
   of the recorded deferred stock that still fails and remains active.
   *Refuted by:* a newly failing path is added to the exemption set, a directory
   wildcard exempts new research, or a compliant or archived path stays exempt.
   *Basis:* decisions.md#Q-4.

10. When the census scans active research, it reports each unreadable file and
    every model-written file's metadata-contract or opening-notice violations
    before applying exemptions, regardless of its current provenance label.
    *Refuted by:* an invalid producer-list member, missing or duplicate owned
    key, retained approval, inconsistent date or unreadable input escapes the
    report, or failed-call/quoted evidence falsely classifies an untouched
    human-written skeleton as published research.
    *Basis:* decisions.md#Q-2; decisions.md#Q-3; decisions.md#Q-4.

## Non-goals

- No one-time normaliser, Git-history reconstruction of missing producers or
  bulk correction of existing research. That work returns with its own spec
  in the separate historical-provenance correction task
  (bead coding-harness-2i7x, referenced by the current census library).
- No archive cleanup, living-spec edits or changes to another change's files.
- No new provenance class, repository-wide provenance validator or enforcement
  of the provenance map's `allowed:` declarations.
- No model selection, prompt-file, leak-check, admission, swarm-record-format,
  interview-rule or human-approval policy change. The private brief's existing
  publication-header normalisation remains part of resume consistency.
- No alteration of the deterministic new-change skeleton: an unpublished,
  human-issued skeleton may remain `human-written`.
- No design phase or ADR: this `bounded` correction stays within existing
  publication, state-store and metadata responsibilities.

## Protected areas

- Other changes' files, including `research.md` — Q-4 defers the former
  cross-folder backfill; the final PR must contain none of those corrections.
- `plans/changes/archive/` and `plans/specs/` — historical evidence and unrelated
  capability contracts remain outside the correction.
- `provenance.yaml`, `decisions/`, `docs/adr/`, `AGENTS.md`, `prompts/`,
  `templates/`, settings and model declarations — no policy or routing edit.

## Boundary

The census measures active research metadata, not the truth of claims or proof
of human authorship. It reports deferred defects but does not block on the
fixed deferred stock; those old headers may remain wrong until the separate
change lands. Retaining known input contributors during new publication does
not recover contributors already lost from that input: historical recovery is
explicitly deferred by Q-4. Missing or ambiguous input attribution is reported
without invention. An audit without accepted output does not establish
publication. Atomicity is per research-file replacement, not across the audit,
state store and publication.

## Definition of Done

- Publication/resume regressions, the enabled census with its fixed legacy
  exceptions and `make verify` are green at the implementation commit.
- The same PR contains the runner correction, read-only census library,
  its library registration and tests; it contains no normaliser or historical
  research correction. Changed documents: this spec, plan and runner evidence;
  no design, models or ADRs are due.
- The PR file list respects protected areas, and its exception set has not
  grown beyond `ff594213` (2026-11-09).
- The PR closes the truthful-Explore-provenance task and its final commit
  carries `Closes-Bead: coding-harness-g19n`.
- Special runs: none requiring live model calls; tests use local stand-ins.

## Open decisions

None open. All four maintainer answers remain unchanged; Q-4 narrows the
historical work rather than weakening the metadata contract for new research.

- [DETAIL] Keep one producer as a mapping and several as a list of mappings;
  use program names from `producer_for(endpoint)` and `stage2-research-swarm`,
  ISO dates in `version`, and a separate `model` field when known. This keeps
  the simple shape without losing earlier input contributors.
- [DETAIL] Implement Q-4 with the existing explicit path set at `ff594213`:
  report all defects, block unlisted ones, and remove corrected or archived
  entries. A fixed shrinking set makes the accepted historical limit visible.
- [DETAIL] Keep census validation read-only and independent fault fixtures
  for every contract field; deferring historical writes does not defer checks
  on new research or producer-list members.
- [DETAIL] Retain the swarm's exact prepared publication bytes/day in its
  resume binding and normalise its private brief's date with the documented
  sentinel `0000-00-00`; the sentinel never becomes a published producer date.
- [DETAIL] The two-hour header appetite records Q-3's now-spent repair tranche;
  Q-4 grants no new phase-4 tranche. Preserve measured history and stop before
  further implementation if additional budget would be needed.
