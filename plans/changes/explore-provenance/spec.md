---
title: "Spec — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-09
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, explore, provenance]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — `explore-provenance`

Explore publishes truthful research metadata, and a read-only census prevents
new research files from inheriting false metadata (bead coding-harness-g19n —
truthful Explore provenance). Research: [research.md](research.md).
Scope: [decisions.md](decisions.md), maintainer answers Q-1 through Q-4,
2026-11-04 through 2026-11-07. Q-4 supersedes the one-time normalisation scope
of Q-1 through Q-3; their publication and producer-preservation requirements
remain. Criteria 7 and 9 below reflect that explicit scope reduction.

## Problem

- Research dated 2026-11-04 records that both Explore routes append model output
  while leaving the generated `human-written` header and empty-file notices;
  the read-only explorer cannot repair the runner's output (“What exists today”).
- The same research records that existing checks hold only selected header
  fields, allowing false provenance to survive until another review and repair.
- The maintainer's answers of 2026-11-06 require the whole metadata contract and
  preservation of multiple producers after repeated census and attribution
  failures (Q-2 and Q-3). On 2026-11-07 the maintainer separated the difficult
  history-based correction of existing files from this change (Q-4). Shipping
  must therefore prevent new debt without claiming that old files were fixed.

## Terms

- **Publication** — an accepted single-model answer or a runner-written swarm
  record, including an incomplete swarm publication; a call audit alone, a
  failed answer, quoted text or a fenced example is not publication.
- **Active research** — `plans/changes/<name>/research.md` directly under each
  active change folder, excluding `archive/`. Existing model attribution or
  accepted publication evidence establishes model-written research regardless
  of its current provenance label, including manually seeded work.
- **Stock exemption** — the adoption day recorded for the census in
  `decisions/adoption.yaml` (maintainer, `decisions.md` Q-5 and option C,
  2026-11-12), applied at one place in `scripts/research_census.py`. An active
  research file is stock only when it is unchanged in the working tree and its
  last change in Git was committed before that day: its findings are not
  reported. Dates and producer evidence inside the file do not decide the
  exemption. Uncommitted files or unreadable Git history are subject to the
  census. The removed fixed
  `UNCORRECTED` file set is no longer required anywhere. Stock files await the
  separate history-based correction (bead coding-harness-2i7x — normalise
  existing research).
- **Skeleton text** — only the generated opening empty-file paragraph and
  provenance-instruction blockquote from `scripts/new_change.py`; the title and
  authored quotations of those notices remain research.
- **Producer attribution** — one producer record, or a non-empty list for
  several known contributions. Records identify the producing program or swarm
  orchestration and its evidence-backed date; known model identities and earlier
  contributions remain represented. A swarm record does not attribute the
  whole document to one participant.
- **Metadata contract** — exactly one top-level `provenance`, `produced_by`,
  `review`, `date`, `last_reviewed` and `updated` field, without duplicate keys
  inside producer/review mappings; `ai-drafted-reviewed` provenance; non-empty
  producer attribution; pending review with null approver and approval date.
  Every producer has `kind: llm-session`, an evidence-backed program name and
  an ISO calendar date string in `version`; known models are retained separately.
  Dates obey `date <= last_reviewed <= updated`, and producer dates lie within
  `date..updated`. The edit stamp is the actual edit day, without inventing a
  historical publication or human review date.

## Acceptance criteria

1. When Explore publishes model research through Flash, its explicit Stage-1
   fallback or the research swarm, the resulting header declares exactly one
   `provenance: ai-drafted-reviewed`.
   *Refuted by:* any route publishes with missing, conflicting or human-written
   provenance.
   *Basis:* decisions.md#Q-1; decisions.md#Q-4.

2. When Explore publishes model research, the header identifies its producing
   program or swarm orchestration and evidence-backed publication date without
   discarding previously known producer or model contributions.
   *Refuted by:* missing or conflicting attribution, a wrong date, an entire
   swarm attributed to one model, or several known producers collapsed into one.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; decisions.md#Q-4.

3. When Explore publishes model research, the resulting document's review is
   pending with no claimed human approval.
   *Refuted by:* missing or duplicate review metadata, retained approval for the
   extended document, or an invented approver or approval date.
   *Basis:* decisions.md#Q-1.

4. When Explore publishes into a generated research skeleton, its opening
   skeleton text is absent from the resulting document.
   *Refuted by:* either notice remains or a second publication reintroduces it.
   *Basis:* decisions.md#Q-1.

5. While publication corrects research metadata and opening notices, unrelated
   header fields and existing research body bytes remain unchanged.
   *Refuted by:* altered class, bead, owner, lifecycle state, historical dates,
   authored prose, audit lines, prior swarm envelopes, title or line endings
   outside the owned metadata and generated opening spans.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; decisions.md#Q-4.

6. If replacement of an existing research file fails before the replacement
   completes, its previous bytes remain intact.
   *Refuted by:* truncated research or a partial combination of the corrected
   header, removed notices and appended publication.
   *Basis:* decisions.md#Q-1; research.md, “What exists today”.

7. When the active-research census runs, every reported metadata or opening-notice
   violation outside the stock exemption (adoption day) makes its repository
   test fail.
   *Refuted by:* a file published or changed from the adoption day on passes with
   a violation, another provenance label hides a model-written file, or the
   census is skipped.
   *Basis:* decisions.md#Q-2; decisions.md#Q-4.

8. When an incomplete swarm publication is corrected and resumed, the runner's
   own correction preserves reuse of otherwise unchanged results.
   *Refuted by:* successful seats repeat solely because of the correction or a
   later calendar day, or foreign header/body/tail edits pass as the same input.
   *Basis:* decisions.md#Q-1; research.md, “Where it lives”.

9. While existing research correction is deferred, the stock exemption is
   decided by the file's last change in Git against the recorded adoption day.
   An unchanged file last committed before that day is stock, regardless of
   dates or producer evidence written inside it. A last change committed on
   that day or later, any uncommitted change or unavailable Git history makes
   the file subject to the census.
   *Refuted by:* exemption for an equal-day or later Git change, an uncommitted
   file or unreadable Git history; refusal of stock exemption based on dates
   or producer evidence inside the file; or exemption by directory or file name.
   *Basis:* decisions.md#Q-4; decisions.md#Q-5; maintainer option C, 2026-11-12.

10. When the read-only census examines active research, it reports each unreadable
    file and each model-written file violating the metadata contract or retaining
    an opening skeleton notice before applying the stock exemption.
    *Refuted by:* a bad producer-list member, missing field, duplicate nested
    key, retained approval, inconsistent date or unreadable file goes unreported;
    failed-call or quoted evidence falsely establishes publication; or the
    census writes research files or requires historical producer reconstruction.
    *Basis:* decisions.md#Q-2; decisions.md#Q-3; decisions.md#Q-4.

## Non-goals

- No one-time normaliser, Git-history reconstruction or bulk correction of
  existing research. Q-4 moves that work to its own spec and bead; it resumes
  there with evidence-backed historical producers, not as a repair here.
- No new provenance class, general provenance validator or enforcement of
  `allowed:` in the provenance map; the census measures active research only.
- No model selection, prompt-file, leak-check, admission, swarm-record-format,
  interview-rule or human-approval policy change. The existing private brief's
  publication normalisation is covered by criterion 8.
- No alteration of the deterministic new-change skeleton: an untouched,
  unpublished human-issued skeleton may remain `human-written`.
- No design phase or ADR: this remains the maintainer's `bounded` correction
  within existing publication, state-store and metadata responsibilities.

## Protected areas

- Other changes' checked-in research and all their other artifacts — the former
  cross-folder correction authorisation is superseded by Q-4, with exactly one
  exception, a rule rather than a list of files: until this change merges, every
  active research file the census flags may have its header corrected
  ([decisions.md#Q-8](decisions.md#q-8--the-header-only-correction-as-a-rule-until-this-change-merges),
  2026-11-14, which generalises the files of
  [decisions.md#Q-6](decisions.md#q-6--two-research-files-that-the-git-dated-census-finds)
  and [decisions.md#Q-7](decisions.md#q-7--two-more-research-files-after-the-merge-of-main),
  2026-11-13). Header-only means its provenance, producer and review fields and
  its leftover skeleton notice; research content and every other change's
  artifacts remain protected.
- `plans/changes/archive/` and `plans/specs/` — historical evidence and unrelated
  capability contracts are outside this correction.
- `provenance.yaml`, `decisions/`, `docs/adr/`, `AGENTS.md`, `prompts/`,
  `templates/`, settings and model declarations — no policy or routing edit.

## Boundary

The census measures current publication metadata, not the truth of research
claims or proof of human authorship. Publication preserves known attribution
in the file being published; it does not reconstruct contributors already lost
from history. Unknown or ambiguous producer facts are reported without invention.
The stock exemption permits pre-existing defects until the separate
correction, without weakening checks on new files or publication routes. Correct
future Explore publication still applies when the target is a stock file.
Atomic replacement protects an existing file until replacement completes; it
makes no rollback promise after a successful replacement and later sync failure.

Adoption day (`decisions.md` Q-5; maintainer option C, 2026-11-12): the census
uses the day recorded for it in `decisions/adoption.yaml`. Stock exemption
depends only on the file's last committed Git change predating that day and
the absence of uncommitted changes, whatever change folder it belongs to.
Dates and producer evidence inside the file cannot grant or end exemption.
Files changed on or after adoption, uncommitted files and files whose Git
history cannot be read are measured in full. Correcting stock files stays
separate work.

## Definition of Done

- Targeted publication, resume and census regressions pass, and `make verify`
  is green at the implementation commit; each ledger test rejects its fault.
- The same pull request includes the runner fix, read-only census library and
  tests; no normaliser or bulk research edits remain. No model or ADR edits.
- The pull request's file list respects protected areas and the deferred scope,
  including only the header-only exception of decisions.md#Q-8 (2026-11-14):
  in research files of other changes that the census flags before this change
  merges, only provenance, producer and review fields, the leftover skeleton
  notice and the `updated:` stamp change, without research content changes.
- The pull request closes the truthful-Explore-provenance task and its final
  commit carries `Closes-Bead: coding-harness-g19n`.
- Special runs: none requiring live model calls; tests use local stand-ins.

## Open decisions

None open. All four maintainer answers remain unchanged. The following
reversible details are explicit agent choices, with their reasons.

- [DETAIL] Keep one producer as a mapping and several as a list; retain
  `producer_for(endpoint)` program names, `stage2-research-swarm` for swarm
  orchestration, ISO dates in `version` and known models in `model`. This keeps
  the simple shape while preserving multiple contributors.
- [DETAIL] Retain exact prepared publication bytes/day and the research portion
  of the private brief in the resume binding. Its date sentinel `0000-00-00`
  is private and never a published producer date; this prevents the runner's
  own correction or a later date from invalidating reusable work.
- [DETAIL] Superseded by Q-5: the exemption is the adoption day in the census,
  not a file set. Deferred debt stays visible because the exemption ends for a
  file at its first change from the adoption day on.
- [DETAIL] The header retains Q-3's historical two-hour additional repair
  tranche. Q-4 records it as spent; this redraft grants no further phase-4
  time and preserves measured history in the plan.
