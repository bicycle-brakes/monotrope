---
title: "Spec — interview-context"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-zs7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, questions, context, adhd]
class: feature
appetite: 4
change: interview-context
adr_question:
  proposed: "yes"
  reason: >-
    A rule for every question adds a durable context field and a prospective
    verification contract across workflow instances.
adr_files: [docs/adr/0018-every-question-carries-its-context.md]
---

# Spec — interview-context

Every question explains its intention and its effects before asking, and
answered records retain that context under a prospective check (bead
coding-harness-zs7). Sources: `research.md` and `decisions.md`, Q-1 to Q-5.

## Problem

- Context is required only by the interview prompt; the spec's question form,
  workflow protocol and general agent rules omit it. A reader must reconstruct
  earlier discussion before answering elsewhere (`research.md`, "What exists
  today", points 1 to 4, observed 2026-10-14; the interview rule landed in
  `f287278`). The interview records the concrete trigger: a review ambiguity
  could not be answered until its background was explained (`decisions.md`,
  opening, 2026-10-14).
- The decision record and gate preserve and count answers without preserving
  the context presented with them; later readers cannot see that explanation
  (`research.md`, points 5 and 6, and "Draft gap resolution", at `c7fa059`).
- The kit carries the interview prompt, but that alone does not establish the
  general rule or check it in other repositories (`research.md`, point 8 and
  "Draft gap resolution", at `c7fa059`).

## Terms

- **Context form:** Topic; Intention, including why this comes up now; Today;
  Repository change; Architecture change, in that order. Each part uses a
  short explanation; an unchanged area says so and explains why. Conversation
  uses direct translations of these labels into the maintainer's language.
  A question stands last on its own line; an unchanged plan card follows its
  contextual preface and keeps its existing final veto invitation.
- **Context text:** a faithful English representation of the context actually
  shown, translating German presentation without adding or omitting meaning.
- **Answered record:** an actual `## Q-<id> · <title>` block in a change's
  `decisions.md` with `status: answered`, including records in the archive;
  open questions, skip records, detail prose and fenced examples are outside it.
- **Recorded-answer day:** the date ending the record's MADR decision
  statement, `— YYYY-MM-DD`, when that answer was recorded; MADR is the
  existing decision form that states situation, choice, goal and consequence.
  A changed answer carries its new recording day, independently of `asked`
  and file dates.
- **Adoption day:** the calendar day the decision pull request merges in that
  repository; answers dated that day are included, not exempt.
- **Measured check:** the adoption day, recording days and decision files
  needed for the check are readable; unknown applicability is not success.

## Acceptance criteria

1. When an agent asks the maintainer for an answer or decision in any harness,
   the general instructions require the context form for interviews, spec
   decisions, review ambiguities, plan-card presentation and ordinary
   conversation.
   *Refuted by:* a phase or conversation is exempt, or the rule remains confined
   to the interview prompt (Q-1).
2. When a question or plan card is presented, it uses the context form before
   any options or the unchanged card, with its question or veto invitation last.
   *Refuted by:* intention or either change explanation is missing, options
   precede context, the question shares its line with an explanation, or text
   follows the question or final veto invitation (Q-4).
3. When a question uses an identifier or technical term, the presentation
   explains it at first use in plain language understandable without code or
   earlier conversation.
   *Refuted by:* answering requires an unexplained finding id, acronym or
   remembered exchange (Q-1, Q-4).
4. When an answer is recorded on or after adoption, its answered record keeps
   the presented context in a dedicated, non-blank `context` text field.
   *Refuted by:* context exists only in chat or adjacent prose, belongs to another
   question, or adds explanations that were never shown (Q-2).
5. If a measured check finds a subject answered record without a non-blank
   text value in its own context field, the context gate exits 1 with the file
   and question id.
   *Refuted by:* deletion, whitespace, an empty multiline value or a non-text
   value passes, including when another record has context (Q-2).
6. When a subject answered record has one non-blank context text value and its
   applicability is readable, the context gate accepts that value on presence
   alone.
   *Refuted by:* it grades clarity, requires an ADHD profile, or rejects readable
   context because its wording or length differs (Q-2, Q-3).
7. When an answered record's recorded-answer day is on or after the adoption
   day, the gate checks it regardless of its change's age or archive location.
   *Refuted by:* an adoption-day answer, a late answer to an older question, an
   answer in an old change or an archived answer evades the check (Q-5).
8. When an answered record's recorded-answer day precedes adoption, the gate
   exempts it without requiring a context backfill.
   *Refuted by:* verification requires changing an older answer or inventing
   its original context; new answers in that same file remain subject (Q-5).
9. If the gate cannot read its adoption day, an answered record's recording
   day, or a decision file it must inspect, it reports not measured and exits 3.
   *Refuted by:* absent, invalid or ambiguous dates, or unreadable files, produce
   an exemption or success; the diagnostic must identify the missing evidence.
10. When `make verify` or hosted verification runs, the context gate is a
    blocking check in both places.
    *Refuted by:* a context failure or not-measured result leaves verification
    green, or only a manually invoked command checks it (Q-2).
11. When the kit carries the workflow to another repository, it carries the
    principle "plain language, context first" with ADHD as its reason, the
    context form, gate and its tests without a profile switch.
    *Refuted by:* only the interview rule travels, any executable dependency is
    missing, the rationale is absent, or the target receives this repository's
    adoption day (Q-3).
12. When the change is presented for merge, one new ADR states the five
    maintainer answers as the proposed rule whose acceptance is that merge.
    *Refuted by:* the ADR changes an answer, declares an unmade approval, or a
    second new ADR is introduced (Q-1 to Q-5).

## Non-goals

- Backfilling answers dated before adoption or reconstructing missing context.
- Automatic judgments of clarity, truth or fidelity, or interception of chat.
- Profiles, opt-outs, additional interview questions or changed minimum counts.
- Changed plan-card or pull-request-card fields, findings schemas, or a new
  decisions template; context precedes the existing decision or veto form.
- Installing the kit in sibling repositories, fixing glossary pointers, or
  building the deferred change-artefact validator.

## Protected areas

- Existing interview counting and ADR-answer rules: their contracts stay intact.
- Historical answers before adoption: their content stays intact.
- Tracker, harness runtime configuration and sibling checkouts: this draft has
  no authority to change them.

## Definition of Done

- `make verify` and hosted CI are green with the new blocking gate.
- The general rule, workflow, interview/spec/plan prompts, context gate and
  tests, adoption entry, kit manifest, derived CI and plans index, and
  `docs/adr/0018-every-question-carries-its-context.md` move together; the plan
  names each file.
- Review confirms the displayed form and context fidelity; the file list shows
  protected areas intact and non-goals unbuilt.
- The decision PR names the bead and closes it at completion; the final commit
  carries `Closes-Bead: coding-harness-zs7`. Only the orchestrator owns these
  later actions and any maintainer-stated ADR answer; this draft records none.
- Special runs: the context mutation and kit probe, with their tested commit
  named in the PR body.

## Open decisions

None open. The author chooses the following revisable details and records why:

- [DETAIL] Use the five labels in Terms and the field name `context`; they give
  each requested explanation a stable place without another record format.
- [DETAIL] Use the existing dated decision statement for the cut-off, because
  `asked` cannot date a later answer and existing answers need no new date field.
- [DETAIL] Unknown applicability takes precedence over a missing-context
  verdict, because a partial inspection cannot establish a measured result.
- [DETAIL] Preserve the shown context's meaning in English when conversation
  was German, because repository artifacts are English; translation must not
  invent context. The unchanged plan card receives its contextual preface when
  presented, retaining its existing final invitation and veto.
- [DETAIL] Classify this as a feature with an ADR proposal, because it adds a
  self-contained check while keeping legacy interfaces usable before adoption.
- [DETAIL] Stop phase 4 after four hours including repairs; this bounds the
  small gate and documentation change without widening the interview's scope.
