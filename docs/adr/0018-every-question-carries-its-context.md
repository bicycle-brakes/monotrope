---
title: "ADR 0018 — Every question carries its context, and answered records preserve it"
category: adr
status: accepted
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, questions, context, adhd, gates, kit]
---

# ADR 0018 — Every question carries its context, and answered records preserve it

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends no decision and supersedes no ADR.
* Review: the maintainer chose the direction on 2026-10-14, recorded as Q-1
  through Q-5 in `plans/changes/interview-context/decisions.md`; the acceptance
  is the merge commit and is written nowhere else, so the header's `review`
  stays pending · Decider: maintainer · prepared by Codex
* Date: 2026-10-14 · takes effect on merge

## Context

The interview prompt already required short background before options, but
the general rules and spec question form did not. A review ambiguity reached
the maintainer without enough explanation to answer it. Decision records
preserved the answers without the context presented with them; the gate counted
answers only. These observations and the trigger are recorded in the change's
research and interview at `c7fa059`, 2026-10-14.

The kit carries the workflow and phase prompts into other repositories, while
each repository keeps its own adoption record. The existing interview gate
uses a change's spec date, which cannot determine when a later answer to an
older question was recorded (`scripts/adoption.py`,
`scripts/check_interview_minimums.py`, read 2026-10-14).

## Decision Drivers

* Every question can be understood without code or remembered conversation (Q-1).
* Readers with ADHD find the purpose and each part in a stable place (Q-3, Q-4).
* Intention and effects on repository and architecture are explicit (Q-4).
* Later readers see the context to which the maintainer answered (Q-2).
* The principle travels for everyone, without a personal profile (Q-3).
* Older answers are not given invented context after the fact (Q-5).

## Considered Options

* **Keep the rule in interviews.** Fewer changes, but other questions continue
  to depend on unexplained background.
* **Apply it to workflow decisions only.** Covers formal phases but leaves
  ordinary conversation outside the rule.
* **Apply it to every question, record context and check its presence.** Gives
  one obligation across harnesses, at the cost of longer questions and a field
  maintained with every new answered record.

The interview also weighed free context against a fixed form (Q-4), a profile
against a principle for all (Q-3), and backfilling older records against a
prospective cut-off (Q-5). For enforcement, a writing rule alone was weighed
against a recorded field and gate (Q-2).

## Decision

Chosen option: "Apply it to every question, record context and check its
presence", because the maintainer needs the intention and effects before
answering, and the explanation must remain available with the answer.

The proposed rule, from the five interview answers:

1. Every agent question to the maintainer carries context: interview, spec
   decision, review ambiguity, plan-card presentation and conversation, in
   every harness. Use plain language and explain identifiers at first use.
2. A fixed context form precedes options: Topic, Intention (including why now),
   Today, Repository change, Architecture change. An unchanged area says why.
   The question itself stands last on its own line. When presenting the
   unchanged plan card, its contextual preface comes first and its existing
   veto invitation remains last. Translate labels into the conversation's language.
3. Each subject answered record keeps the context actually presented in its
   own `context` text field, faithfully in English for repository artifacts.
   A blocking gate in `make verify` refuses a missing or blank text value.
   It proves presence, not clarity or fidelity; those remain review duties.
4. The kit carries the principle "plain language, context first", with ADHD
   named as its reason, the form, gate and tests. There is no profile switch;
   each repository records its own adoption day.
5. The gate applies to answers recorded on or after the calendar day the rule
   merges in that repository, also in older changes and the archive. Earlier
   answers remain exempt and unchanged. The dated MADR statement records the
   answer day; an unknown day is not grounds for an exemption.

## Consequences

* Questions become longer, with intention and both kinds of effects in fixed
  places; the maintainer no longer has to reconstruct them from an earlier chat.
* Agents preserve the shown context with an answer, translating its meaning
  when needed, and maintain the decision's actual recording day.
* A separate context gate joins verification; the interview-counting contract
  stays intact. Unreadable adoption or answer evidence produces not measured,
  which blocks verification rather than silently exempting the record.
* The rule covers conversation, but a repository gate observes only recorded
  answers. It cannot authenticate a recording date, the author of a record or
  whether its context was truly shown; review and merge carry that assurance.
* There is no backfill before adoption. Answers from the adoption day itself
  need their authentic presented context; moving the day to hide a failure or
  inventing that context is not a repair.

## Validation

* Mutate a subject record by removing its context; the command must exit 1
  and `make verify` must go red. Exercise empty and multiline values as well.
* Test the day before adoption, adoption day, a later answer to an older
  question, mixed-date files and archived/spec-less records independently.
* Refuse unreadable dates or files as not measured, exit 3; pin the blocking
  local/hosted gate and confirm the portable copy in the strict kit probe.
* Review the fixed form and recorded fidelity against the interview answers;
  the maintainer's merge of the decision PR confirms this proposal (ADR 0008).
