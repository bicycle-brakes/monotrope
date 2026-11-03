---
title: "Spec — questions-interview-tool"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-8v2c.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, question-protocol]
class: bounded
appetite: 1
adr_files: [docs/adr/0018-every-question-carries-its-context.md]
neighbours: []
---

# Spec — questions-interview-tool

Questions reach the maintainer through the harness's native structured
question tool, one at a time, or through a fixed text form when that tool
is unavailable (bead coding-harness-8v2c.1 — questions through the interview
tool). Research: `research.md`. Answers: `decisions.md`.

## Problem

- The standing question protocol specifies context but not the delivery
  channel. Native-tool use is recorded only as session practice, so an agent
  can follow the standing text while asking in free chat (`research.md`,
  “The rule that exists” and “The channels questions actually travel today”,
  exploration committed at `3c93f7b0`, 2026-11-03).
- Deferred night questions and harnesses without a question tool have no
  stated channel contract. The interview settled collection followed by
  individual delivery, and a fixed fallback form (`research.md`, open
  questions 1–2; `decisions.md#Q-1` and `decisions.md#Q-4`, `ef824324`,
  2026-11-03).
- The existing question-context gate proves a recorded field is present;
  it cannot prove which channel a chat question used. The maintainer chose
  tests of the asking prompts and session-entry instructions instead of a
  new gate (`research.md`, “The gates behind it”; `decisions.md#Q-3`,
  `ef824324`, 2026-11-03).

## Terms

- **Native question tool:** the current harness's available structured
  question interface; Claude Code's example is `AskUserQuestion`, not a new
  repository-owned interview service.
- **Fixed fallback form:** exactly one question per message; Topic,
  Intention, Today, Repository change and Architecture change before
  numbered options; the recommendation first with its consequence; the
  actual question last on its own line. Conversation labels are German.
- **Carriers:** the standing rule, workflow question protocol, phase prompts
  01a, 02, 02a, 03, 04b and 06, and the instructions delivered at Claude Code
  session start. Read-only reviewers still return findings; their
  orchestrator delivers any resulting question to the maintainer.

## Acceptance criteria

1. When a harness has a native question tool available, the carriers require
   maintainer questions to use that tool.
   *Refuted by:* any listed carrier omits the tool requirement or permits
   free chat instead despite tool availability.
   *Basis:* decisions.md, introduction; decisions.md#Q-2; decisions.md#Q-3.

2. When questions are delivered, the carriers require exactly one question
   per tool call, including plan cards without a multi-select exception.
   *Refuted by:* a carrier permits two questions or several plan cards in
   one call.
   *Basis:* decisions.md#Q-5.

3. If no native question tool is available, the carriers require the fixed
   fallback form.
   *Refuted by:* fallback instructions permit multiple questions per
   message, lack an ordered context part, omit option numbering or the
   recommendation-first rule, or put text after the actual question.
   *Basis:* decisions.md#Q-4; research.md, “The rule that exists”.

4. When the maintainer is away, the protocol retains questions with their
   context in the repository handover for individual delivery in the next
   question block.
   *Refuted by:* instructions discard the context, treat the collected list
   as an answered interview, require an unattended tool call, or permit
   bulk delivery when the maintainer returns.
   *Basis:* decisions.md#Q-1.

5. When an agent sends a status update, the protocol keeps that update free
   of questions.
   *Refuted by:* instructions allow a status message to contain a request
   for the maintainer's answer.
   *Basis:* decisions.md#Q-5, its stated status-message context.

6. When a plan card is delivered individually, the presentation preserves
   the complete card verbatim with its contextual preface and existing
   stop invitation.
   *Refuted by:* a card is shortened into tool options, its context is
   omitted, or a card within scope now requires an affirmative approval
   before work starts.
   *Basis:* decisions.md#Q-5; research.md, “The rule that exists” (ADR 0018).

7. When a carrier's channel instruction is removed or contradicted, prompt
   tests fail on that carrier.
   *Refuted by:* deleting the instruction from any required carrier or
   allowing bundled questions leaves the tests green.
   *Basis:* decisions.md#Q-3.

8. When the decision pull request is prepared, it carries the channel rule
   as a dated addendum to the existing context decision, explicitly limiting
   automated assurance to the instruction texts.
   *Refuted by:* the addendum is absent, a separate ADR replaces the chosen
   addendum, or the proposal claims to verify actual chat tool usage.
   *Basis:* decisions.md#Q-2; decisions.md#Q-3.

## Non-goals

- No new question tool, skill, hook, live-chat observer, gate, transcript
  parser, endpoint, or harness capability detection service.
- No changes to interview counting, answer/context schemas, adoption days,
  question timing exceptions, night answers (cut, park or drop), or the
  existing rule that a widening plan card needs approval.
- No question-frontier, yes-wording, research-basis or prototype-option work
  from the neighbouring backlog; no glossary repair or old-answer backfill.
- No design phase: this bounded change specifies delivery through existing
  interfaces and their text carriers; `prompts/02b-design.md` excludes it.
- No new ADR draft: the bounded change amends the existing ADR by the
  maintainer's explicit choice; that held-path edit belongs to the
  orchestrator after the accepted implementation attempt.

## Protected areas

Gate definitions, tracker data, model endpoints, adoption/answer records,
permissions, installed user settings, unrelated ADRs and other changes are
untouched: none implements the answered scope. Held prompts, `AGENTS.md` and
the existing ADR are orchestrator edits only; the AGENTS rule is supplied as
exact proposed text for the maintainer's review, within its existing line cap.

## Definition of Done

- `make verify` is green after the orchestrator's carrier edits, including
  live-text guards and their counterexamples; actual chat compliance remains
  a human review duty.
- Documents moved together: `docs/WORKFLOW.md`, the six named phase prompts,
  `AGENTS.md` after maintainer review, the existing ADR's dated addendum,
  `tools/claude-code/hooks/handover.sh` and `tools/claude-code/README.md`;
  `plan.md` lists tests and generated evidence by path.
- The pull request shows protected areas untouched and non-goals unbuilt;
  its decision template and label leave acceptance to the maintainer's merge.
- The pull request closes the question-channel work item
  (coding-harness-8v2c.1); its last commit carries
  `Closes-Bead: coding-harness-8v2c.1`.
- Special runs: none; tests inspect repository text and use local mutations.

## Open decisions

None open. The five maintainer answers stand unchanged in `decisions.md`.

- [DETAIL] Apply the fallback by actual tool availability, not by a frozen
  list of harness names, because capabilities vary between sessions.
- [DETAIL] Set a one-hour phase-4 appetite, including repairs, as a stop for
  this bounded text-and-test change; neither research nor answers sets one.
- [DETAIL] Extend the existing portable question-context test file rather
  than adding a new test module and kit classification; local hook and
  AGENTS checks run when the Claude Code directory exists, so losing either
  file here fails while kit copies that omit the directory stay portable.
- [DETAIL] Keep the plan-card veto semantics when choosing the channel;
  one card per call adds no new approval requirement.
