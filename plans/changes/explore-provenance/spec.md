---
title: "Spec — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, explore, provenance]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — `explore-provenance`

Explore publishes truthful research metadata; a one-time normalisation brings
all active model-written research to the same contract without losing known
producers (bead coding-harness-g19n — truthful Explore provenance).
Research: [research.md](research.md). Scope: [decisions.md](decisions.md),
maintainer answers Q-1 through Q-3, dated 2026-11-04 and 2026-11-06.

## Problem

- Research dated 2026-11-04 records that both Explore routes append model output
  while leaving the generated `human-written` header and empty-file notices;
  the read-only explorer cannot repair the runner's output (“What exists today”).
- That research records that the existing checks hold only selected header
  fields, allowing false provenance to survive until another review and repair.
- The maintainer's 2026-11-06 answers record repeated gaps in a census limited
  to `human-written`, an unplanned normalisation script touching other active
  research, and loss of multiple-model attribution. Q-2 requires the whole
  metadata contract and Q-3 explicitly authorises the wider scope and producer
  lists; the old two-file backfill no longer describes the agreed change.

## Terms

- **Publication** — an accepted single-model answer or a runner-written swarm
  record, including an incomplete swarm publication; a call audit alone, a
  failed answer, quoted text or a fenced example is not publication.
- **Active research** — every `plans/changes/<name>/research.md` directly under
  a change folder, excluding `archive/`; eligibility does not depend on the
  current provenance label. Existing model attribution or accepted publication
  evidence establishes model-written research, including manually seeded work.
- **Skeleton text** — only the generated opening empty-file paragraph and
  provenance-instruction blockquote from `scripts/new_change.py`; the title and
  authored quotations of those notices remain research.
- **Producer attribution** — one producer record, or a non-empty list for several
  known contributions. Records identify the producing program or swarm
  orchestration and its evidence-backed date; known model identities and earlier
  contributions remain represented. A swarm orchestration record does not claim
  that one participant wrote the whole document.
- **Metadata contract** — exactly one top-level `provenance`, `produced_by`,
  `review`, `date`, `last_reviewed` and `updated` field, no duplicate keys inside
  producer/review mappings, `ai-drafted-reviewed` provenance, non-empty producer
  attribution, and pending review with null approver and approval date. Every
  producer has `kind: llm-session`, an evidence-backed program name and an ISO
  calendar date in `version`; known models are retained separately. Dates obey
  `date <= last_reviewed <= updated`, and producer dates lie within
  `date..updated`; the correction stamp is the actual edit day, not an invented
  historical publication or human review date.

## Acceptance criteria

1. When Explore publishes model research through Flash, its explicit Stage-1
   fallback or the research swarm, the resulting header declares exactly one
   `provenance: ai-drafted-reviewed`.
   *Refuted by:* any route publishes with missing, conflicting or human-written
   provenance.
   *Basis:* decisions.md#Q-1.

2. When Explore publishes model research, the header identifies its producing
   program or swarm orchestration and evidence-backed publication date without
   discarding previously known producer or model contributions.
   *Refuted by:* missing or conflicting producer metadata, unrelated authorship,
   a wrong date, an entire swarm attributed to one model, or a multi-producer
   history collapsed into one entry.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3.

3. When Explore publishes model research, the resulting document's review is
   pending with no claimed human approval.
   *Refuted by:* missing or duplicate review metadata, retained approval for the
   extended document, or an invented approver or approval date.
   *Basis:* decisions.md#Q-1.

4. When Explore publishes into a generated research skeleton, its opening
   skeleton text is absent from the resulting document.
   *Refuted by:* either notice remains or a second publication reintroduces it.
   *Basis:* decisions.md#Q-1.

5. While publication or normalisation corrects research metadata and opening
   notices, unrelated header fields and existing research body bytes remain
   unchanged.
   *Refuted by:* altered class, bead, owner, lifecycle state, authored prose,
   audit lines, prior swarm envelopes, title or line endings outside the
   metadata and generated opening spans; historical dates changed without evidence.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2; decisions.md#Q-3.

6. If replacement of an existing research file fails before the replacement
   completes, its previous bytes remain intact.
   *Refuted by:* truncated research or a partial combination of the corrected
   header, removed notices and appended publication.
   *Basis:* decisions.md#Q-1; research.md, “What exists today”.

7. When this change is completed, every active model-written research file
   satisfies the metadata contract and has no opening skeleton text.
   *Refuted by:* any active model-written file fails the contract, a compound
   attribution loses a known contributor, or an archived file is corrected.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2; decisions.md#Q-3.

8. When an incomplete swarm publication is corrected and resumed, the runner's
   own correction preserves reuse of otherwise unchanged results.
   *Refuted by:* successful seats repeat solely because of the correction or a
   later calendar day, or foreign header/body/tail edits pass as the same input.
   *Basis:* decisions.md#Q-1; research.md, “Where it lives”.

9. When the one-time normalisation is invoked, it reports proposed corrections
   without writing by default and applies only evidence-backed corrections when
   explicitly requested.
   *Refuted by:* default invocation writes, a repeated correction changes an
   already compliant file, missing evidence is guessed, or invalid input causes
   a partial batch before preparation has completed.
   *Basis:* decisions.md#Q-2; decisions.md#Q-3.

10. When the active-research census runs, it reports each unreadable active file
    and each model-written file violating any part of the metadata contract or
    retaining an opening skeleton notice, regardless of its current provenance label.
    *Refuted by:* a bad producer-list member, missing field, duplicate nested
    key, retained approval, impossible/inconsistent date or unreadable header
    passes, or failed-call/quoted evidence falsely classifies an untouched
    human-written skeleton as published model research.
    *Basis:* decisions.md#Q-2; decisions.md#Q-3.

## Non-goals

- No new provenance class, repository-wide provenance validator or enforcement
  of `allowed:` in the provenance map; the census measures active research only.
- No archive cleanup, living-spec edits or changes to other changes' research
  findings, specifications, plans or decisions.
- No model selection, prompt-file, leak-check, admission, swarm-record-format,
  interview-rule or human-approval policy change.
- No alteration of the deterministic new-change skeleton: an untouched,
  unpublished human-issued skeleton may remain `human-written`.
- No design phase or ADR: this remains the maintainer's `bounded` correction
  within existing publication, state-store and metadata responsibilities.

## Protected areas

- `plans/changes/archive/` and `plans/specs/` — historical evidence and unrelated
  capability contracts remain outside the active-research correction.
- `provenance.yaml`, `decisions/`, `docs/adr/`, `AGENTS.md`, `prompts/`,
  `templates/`, settings and model declarations — no policy or routing edit.
- Other active changes' files except `research.md` — Q-2 and Q-3 authorise
  correction of all active research metadata and generated notices, not its
  findings or any neighbouring work's other artifacts.

## Boundary

The census and one-time normaliser cover active research metadata, not the
truth of research claims or proof of human authorship. Producer evidence comes
from accepted publications, existing attribution and recoverable Git history;
a program's identity alone does not establish a model identity. Missing or
ambiguous historical facts are reported without invention, and do not justify
silently dropping a contributor. Existing history must be consulted where the
previous repair already collapsed attribution. Atomicity is per file; the
normaliser prepares and validates the batch before writing, but does not promise
rollback of earlier successful replacements after a later I/O failure.

## Definition of Done

- Targeted regressions, the enabled active-file census and `make verify` are
  green at the implementation commit; each ledger test rejects its named fault.
- The same pull request includes the runner fix, one-time normaliser, its
  explicit non-gate registration, tests and corrected active research, with all
  known producers retained; no model or ADR edits are due.
- The file list respects protected areas; only metadata and generated notices
  change in other active research files, as Q-2 and Q-3 authorise.
- The pull request closes the truthful-Explore-provenance task and its final
  commit carries `Closes-Bead: coding-harness-g19n`.
- Special runs: none requiring live model calls; tests use local stand-ins.

## Open decisions

None open. The three maintainer answers remain unchanged.

- [DETAIL] Keep one producer as a mapping and several as a list of mappings;
  use program names from `producer_for(endpoint)` and `stage2-research-swarm`,
  ISO publication dates in `version`, and a separate `model` field when known.
  This retains the existing simple shape while making all contributors visible.
- [DETAIL] Preserve earlier evidence-backed records rather than treating the
  latest Explore audit as authorship of the entire document; a new contribution
  extends attribution and never invents which paragraphs an older model wrote.
- [DETAIL] Share metadata validation between the census and normaliser, with
  independent fault fixtures proving each field and list member; this closes
  the repeated mechanism rather than fixing only the files seen in one round.
- [DETAIL] Keep dates and unrelated header bytes unless evidence requires a
  metadata repair; a missing historical date is a diagnostic, not today's date.
- [DETAIL] Retain the swarm's exact prepared publication bytes/day in its resume
  binding and normalise its private brief's date using the documented sentinel
  `0000-00-00`; the sentinel never becomes a published producer date.
- [DETAIL] The header's two-hour appetite is the additional repair tranche
  authorised by Q-3 on 2026-11-06, after the previously spent appetite; all
  earlier measured time remains in the plan, and this tranche is a stop limit.
