---
title: "Spec — status-fields-restore"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-ljmi
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, runner, repair]
class: bounded
appetite: 2
adr_files: []
neighbours: [plans/changes/repair-restore-status/spec.md, plans/changes/repair-fixed-lines/spec.md, plans/changes/stage2-repair/spec.md]
---

# Spec — status-fields-restore

After every repair attempt, the change's document lifecycle fields retain
their pre-attempt state, and the runner reports that protection (bead
coding-harness-ljmi). Research: `research.md`. Authority: the existing
maintainer decision recorded in `decisions.md`, `SKIP · interview`.

## Problem

As researched on 2026-11-06, document frontmatter separates approval
(`status`) from implementation progress (`implementation_status`), and the
plans registry validates and displays both. The runner does not own their
transitions, but it also does not restore model edits to them after a passing
repair. A repair can therefore change what the change claims about its
approval or progress, rather than merely fix the taken findings
(`research.md`, "What exists today", System 2 and the existing put-back paths).

The existing restoration of review-table Status cells solves a different
problem. The interview skip resolves the research's initial ambiguity:
this change protects the frontmatter pair in spec, design and plan, and
leaves an intentional lifecycle transition to the orchestrator.

## Terms

- **Protected documents:** this change's `spec.md`, `plan.md` and, when
  present before the attempt, `design.md`.
- **Protected fields:** the top-level frontmatter keys `status` and
  `implementation_status`; a body occurrence or a review-table Status cell
  is not such a field.
- **Attempt baseline:** each protected document's field values immediately
  before that attempt's model call, including differences between documents.
- **Repair report:** runner-written attempt evidence in `findings.md`, plus
  the terminal diagnostic when a safety refusal prohibits writing evidence.

## Acceptance criteria

1. When a repair attempt returns edits to protected fields, every protected
   document has its own attempt-baseline field values before any post-run
   verification reads it or the runner checkpoints it.
   *Refuted by:* a verifier or checkpoint sees a model-written value, a
   removed field remains absent, or one document receives another's values.

2. When a repair attempt fails or is rejected, protected fields retain their
   attempt-baseline values before a retry or terminal handback, subject to
   the existing recovery safety boundary below.
   *Refuted by:* a failed call, failed check, exhausted retry chain,
   evidence-save failure, moved HEAD or refused checkpoint leaves changed
   fields in a safely writable protected document.

3. When an otherwise passing repair changes content outside the header,
   field restoration preserves those edits. The header belongs to the
   runner (decisions.md#Q-1): when an attempt changes a protected value, the
   whole header returns to its snapshot and the attempt's other header edits
   are discarded; when the protected values stay unchanged, header edits
   survive.
   *Refuted by:* an accepted body edit or runner time entry disappears
   solely because the lifecycle fields were restored, a header edit survives
   beside a changed protected value, or an edit to the protected fields alone
   causes rejection.

4. If `design.md` is absent before a repair attempt and the attempt does not
   create it, lifecycle protection leaves it absent.
   *Refuted by:* restoration creates an optional design document or refuses
   an otherwise valid repair merely because it has no design document.

5. When a repair attempt finishes, its repair report identifies each document
   and protected field restored, or explicitly says the fields were unchanged.
   *Refuted by:* an accepted or rejected attempt silently restores fields,
   claims a restoration it did not perform, or reports success when safe
   restoration was refused.

6. When the runner builds a repair prompt for any supported route, the prompt
   states that the runner restores `status` and `implementation_status` in
   the change's spec, optional design and plan after every attempt.
   *Refuted by:* either the command-capable or file-tools prompt omits a
   protected field, a protected document or the automatic restoration rule.

7. When the documented repair workflow encounters a finding whose remedy
   requires changing protected fields, it directs the orchestrator to repair
   that finding by hand before handing the remaining taken rows to a model.
   *Refuted by:* the workflow or orchestrator prompt sends that finding to
   automated repair, or leaves the lifecycle transition's owner unspecified.

## Non-goals

- Changing lifecycle values automatically, choosing when an artifact becomes
  accepted or implemented, or detecting status-related findings through
  automatic interpretation of their prose.
- Changing review-table Status or `Broke a test` semantics, repair evidence
  forms, model routing, retry counts, or checkpoint ownership.
- Protecting additional frontmatter keys, other change folders or other verbs.
- A separate design document or ADR: this is a bounded extension of the
  existing repair boundary, with no architectural decision to introduce.

## Protected areas

Model endpoints, credentials, tracker data, gate definitions and existing
recovery safety rules remain unchanged. The review findings' ownership and
the plans registry's lifecycle vocabulary remain unchanged.

## Boundary

The existing all-destinations recovery preflight remains authoritative:
an unsafe alias, hard link or destination still stops without recovery
writes. The terminal diagnostic names the protection that could not run;
the runner never reports restored fields in that case. A moved HEAD is
never reset or amended; restoration applies only to safe working-tree
documents, leaving the unverified commit to the maintainer. An uncatchable
process termination cannot promise a post-call restoration or report.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green on the implemented change.
- The pull request includes `scripts/stage2.py`, `tests/test_stage2.py`,
  `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, these change artifacts and
  the generated `plans/INDEX.md`; no ADR moves.
- The pull request's file list shows the protected areas and non-goals held.
- The pull request closes the lifecycle-field restoration work (bead
  `coding-harness-ljmi`); its last commit carries
  `Closes-Bead: coding-harness-ljmi`.
- Targeted regression results and their commit are named in the pull request;
  no live model call is needed to prove the restoration.

## Open decisions

None open. The existing maintainer decision is not reopened.

- [DETAIL] Use the values immediately before each attempt, not a shared
  default: the documents may intentionally have different lifecycle states.
- [DETAIL] Restore before verification, rather than reject an edit alone:
  checks must judge the repaired content against the standing lifecycle.
- [DETAIL] Report the paths and field names, with an explicit unchanged
  case: this makes the guarantee visible without dumping document contents.
- [DETAIL] Retain the existing safety refusal and moved-HEAD boundaries:
  lifecycle protection must use the runner's existing recovery authority.
- [DETAIL] Allow two hours for phase 4, repairs included, as a stop rather
  than an estimate; no earlier appetite is stated in the decision record.
