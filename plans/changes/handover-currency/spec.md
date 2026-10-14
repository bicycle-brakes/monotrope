---
title: "Spec — handover-currency"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, handover, documentation, currency]
class: feature
appetite: 4
change: handover-currency
adr_question: {proposed: "no", reason: "This extends the existing handover schema, authoring procedure and gate runner prospectively without introducing a subsystem or breaking the historical handover contract."}
adr_files: []
---

# Spec — handover-currency

Every session handover leaves an explicit check of the repository's architecture
and front documents, and a refreshed management status view, without rewriting
earlier handovers (bead coding-harness-ni8). Inputs:
[`research.md`](research.md), explored on 2026-10-14, and the maintainer's four
answers in [`decisions.md`](decisions.md), committed at `d9cbe20`.

## Problem

- The existing checks validate handover fields and `updated:` against a file's
  last change; they do not establish that its account agrees with the current
  repository. An untouched handover can stay green while the code changes
  (research, "What enforces currency today", read on 2026-10-14).
- The roadmap already asks every handover to check whether Now is still true,
  but neither the schema nor the authoring procedure demands evidence of this
  check. Architecture documents and the front page have the same omission
  (research, "The handover and its doctrine").
- The management vault is another reader of repository status; the existing
  daily reconciliation does not establish that a particular handover updated
  that view. The maintainer explicitly requires that update at each handover
  (decisions Q-1 and Q-2; the vault registration was read by the interviewer,
  not by this draft session).

## Terms

- **Handover** — a new session record, including a session recorded as a dated
  addendum to an existing file. This requirement also accompanies a new return
  channel handover; its immutable findings and acknowledgement rules remain.
- **Target** — a repository-configured document, document tree or external
  management view. Checking a tree includes its Markdown documents recursively.
- **Current** — the document's claims agree with the inspected state at the
  stated cut-off, including whether a document is a historical proposal.
  A recent date alone proves nothing; a superseded record need not be rewritten.
- **Small correction** — a local factual or wording correction that fits the
  remaining session appetite and needs no new decision. Anything else is
  follow-up work, subject to the existing tracker ownership rule.
- **Adoption** — the introduction of this rule in the repository. Earlier
  handover text is historical; later session records are subject to the rule.

## Acceptance criteria

1. When a handover is written after adoption, its documentation-currency
   section contains a check record for every configured target.
   *Refuted by:* a new handover with no section, an empty section, or an omitted
   configured target passing the completion check.

2. When this repository's documents are checked, the record names each
   Markdown document under `docs/architecture/`, `AGENTS.md`, `ROADMAP.md`,
   `README.md`, and each vault note registered for this repository, as current
   or stale at the stated cut-off.
   *Refuted by:* an omitted architecture document or registered note, or a
   document labelled current solely because its date is recent.

3. When a checked document is stale, its record describes the specific claim
   that is stale.
   *Refuted by:* a stale record with only its status, an empty explanation,
   or an explanation that does not identify the wrong claim.

4. When a stale claim needs a small correction, the handover's pull request
   includes that correction and identifies it in the check record.
   *Refuted by:* a small factual correction deferred to an unrelated change,
   or a claimed correction absent from the handover pull request.

5. When correcting a stale claim exceeds the small-correction boundary, the
   record links a follow-up bead describing that correction.
   *Refuted by:* untracked larger work, or a worker violating tracker ownership
   to create it rather than obtaining the reference from the owning session.

6. When a handover is completed, its author has refreshed this repository's
   configured management status view from the repository state for that
   handover, even when the substantive status is unchanged.
   *Refuted by:* relying on the next daily reconciliation, an unchanged
   checked-at value, or claiming completion without writing and reading back
   the configured view.

7. When the management update is recorded, its evidence identifies the view,
   the update cut-off, and the repository source path and commit from which
   its status was taken.
   *Refuted by:* a completion claim with no view locator, date, source path,
   or source commit, or a view treated as a second task tracker.

8. If a required document or management view cannot be read or updated, the
   author records the inability explicitly and the check remains incomplete.
   *Refuted by:* reporting an inaccessible target as current, absent or
   successfully updated, or accepting that record as a completed check.

9. While a handover contains only text written before adoption, this rule
   requires no change to that text or its existing frontmatter contract.
   *Refuted by:* an unchanged legacy handover failing for lacking this section,
   or an implementation that backfills the handover corpus.

10. When a session appends a handover after adoption to an older file, the
    appended session contains its own check without replacing the old body.
    *Refuted by:* an unchecked new addendum passing because its file is old,
    or requiring a rewrite of the old session to make the addendum pass.

11. When a new handover claims an earlier creation date, it remains subject
    to the rule if it did not exist at adoption.
    *Refuted by:* backdating a new file or changing `created:` exempting it.

12. When the completion check runs locally or in hosted CI, a missing or
    incomplete required check makes `make verify` red with the handover path
    and the missing condition.
    *Refuted by:* report-only enforcement, success when the configured corpus
    cannot be measured, or a diagnostic that does not locate the failing record.

13. When an instance configures its own document paths, handover location and
    management view, the kit's same schema and check enforce that configuration
    without inheriting Coding Harness's targets or adoption history.
    *Refuted by:* a fixture instance with `journal/` or another architecture
    tree still being checked against this repository's paths or vault.

14. While CI validates the handover evidence, it neither opens the management
    vault nor changes the repository or an external status view.
    *Refuted by:* verification needing the maintainer's home directory,
    credentials, a network connection or a write to a status view.

15. When a handover author follows the template and repository instructions,
    those instructions require the document check and management update before
    completing the handover.
    *Refuted by:* the template, standing rule or installed authoring procedure
    allowing completion after merely promising a later update.

The mechanical check holds the record's completeness. Whether its statements
are true, a correction is small, and a vault update actually happened remain
author obligations examined in review; CI cannot prove them from prose.

## Non-goals

- Calendar-age warnings, moving `pending` handover statuses, and changing the
  existing research-currency report or `updated:` gate.
- Writing handovers automatically at a usage threshold; that is separate work
  (bead coding-harness-l9s).
- An autonomous vault synchronizer, changing the existing daily reconciliation,
  choosing a kanban product, or migrating management data. A future board is a
  later repository configuration and its own integration change if needed.
- Updating other repositories, acknowledging their feedback, rebuilding the
  architecture corpus, or translating unrelated German text.
- Backfilling old handovers or rechecking their historical reports against
  today's inventory. The new check records the inventory at its own cut-off.

## Protected areas

- Existing bodies under `docs/journal/handover/`: historical records are
  preserved; future sessions may append their own records.
- Return-channel record markers, hashes and acknowledgement fields: this rule
  adds evidence outside the immutable findings, without changing the channel.
- ADRs and `decisions/answers/`: no ADR is proposed as necessary, and the
  maintainer's feature ADR answer is never supplied by this draft.
- Other repositories and private vault contents during this runner draft:
  only the worktree and its git directory may be read.

## Definition of Done

- `make verify` is green; the maintainer's ADR answer is recorded through the
  existing decision procedure before the feature is merged.
- Moved with the code: `templates/handover.md`, the new
  `templates/handover-check.yaml`, `AGENTS.md`, `docs/WORKFLOW.md`,
  `README.md`, `tools/claude-code/skills/handover/SKILL.md`,
  `tools/claude-code/README.md`, the instance configuration
  `decisions/handover-check.yaml`, both kit manifests and the derived CI file.
  Architecture shape is recorded in `design.md`; no architecture corpus
  rewrite or ADR is part of this change.
- Protected areas remain intact and non-goals remain unbuilt, shown by the PR
  file list and legacy handover tests.
- The PR closes coding-harness-ni8; its last commit carries
  `Closes-Bead: coding-harness-ni8`.
- Special run: an authorized handover author demonstrates the document check
  and actual management-view write/read-back, naming its repository commit and
  cut-off in the PR evidence. A fixture proves parsing, never an actual update.

## Open decisions

None open about the requested behavior: decisions Q-1 through Q-4 settle it.
The feature's ADR proposal is "no"; the maintainer's ADR answer remains owed
through the existing workflow and is not an answer inferred from those four
questions.

I chose the following reversible details and recorded their reasons:

- [DETAIL] This is a `feature`, with a design: it changes the completion
  obligation and its enforcement inside the existing handover flow; historical
  consumers stay compatible, so it introduces no new subsystem or interface
  break requiring the `architectural` class.
- [DETAIL] Four hours is the phase-4 appetite, including repairs, because the
  deliverable is one schema extension, one gate and its authoring instructions;
  exceeding it stops implementation and records a handover.
- [DETAIL] Scope and adoption use repository-owned configuration, with a fixed
  git snapshot distinguishing old bodies from new records. File dates can be
  backdated and cannot safely establish the exemption.
- [DETAIL] An unreadable target yields an explicit incomplete record, which
  fails completion, because "not read" cannot support current or stale.
- [DETAIL] The existing registered project status note is refreshed by the
  handover author; daily reconciliation remains a later independent check,
  avoiding a second synchronizer or competing task tracker.
- [GAP] The draft may not open the vault. The authorized author resolves its
  registered repository notes and existing status block from the registration
  identified in decisions Q-1 before the live demonstration; a guessed note or
  new board is not a substitute. No new intent answer is needed for that lookup.
