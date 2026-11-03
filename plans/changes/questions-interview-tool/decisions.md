---
title: "Decisions — questions-interview-tool"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-8v2c.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, question-protocol]
---

# questions-interview-tool — Decisions

Class: bounded, and an ADR change: Q-2 decided an addendum to ADR 0018, so the
spec claims `docs/adr/0018-every-question-carries-its-context.md` and five
counted answers are owed. Interview held on 2026-11-03 between 07:20 and
07:45 UTC through the interview tool, one question per call. The bead
(coding-harness-8v2c.1) already settles that "the interview tool" is the
harness's own structured question tool (Claude Code: AskUserQuestion), which
closes the research's open question 1.

## Q-1 · Questions while the maintainer is away

asked: 2026-11-03
answer: "Sammeln, dann einzeln" — at night or whenever the maintainer is away, questions are collected with their context in the handover; in the next block the session asks them one at a time through the tool.
answered_by: maintainer
status: answered
context: |
  Topic: what the rule says for night runs and other times nobody answers in the chat.
  Intention: AGENTS.md gets the rule; it is silent today about questions without the maintainer present.
  Today: night lanes collect questions in the handover for the 15:00 block (night-plan rule 8); the session asks them one by one through the tool once the maintainer is there.
  Repository change: one sentence in AGENTS.md and in docs/WORKFLOW.md, "The question protocol". Options: collect then ask one by one; always ask through the tool at once, a lane waits; no exception stated, the night plan rules it.
  Architecture change: none.

In the context of questions that arise while the maintainer is away, facing a lane that waits at the tool or a collected list, we decided that questions are collected with their context in the handover and asked one at a time through the tool in the next block, to achieve no lane blocked overnight and no question asked in bulk, accepting that a night answer stays cut, park or drop until then. — 2026-11-03

## Q-2 · An addendum to ADR 0018

asked: 2026-11-03
answer: "Nachtrag zu ADR 0018" — the channel (through the tool, one per call) becomes part of the decision, as an addendum to ADR 0018 in a decision pull request.
answered_by: maintainer
status: answered
context: |
  Topic: whether ADR 0018 (every question carries its context) needs an addendum.
  Intention: the size of the change depends on it — an addendum makes it a decision pull request and owes five answers instead of one.
  Today: ADR 0018 says what a question contains (five parts, the question last), not how it reaches the maintainer.
  Repository change: without an addendum AGENTS.md (proposed text), docs/WORKFLOW.md, prompts, tools/claude-code; with one also docs/adr/0018.
  Architecture change: without, none; with, the channel becomes part of the decision.

In the context of a rule about how questions reach the maintainer, facing a working rule beside ADR 0018 or an addendum to it, we decided on an addendum to ADR 0018, to achieve a binding channel that every harness inherits with the decision, accepting a decision pull request and five interview answers. — 2026-11-03

## Q-3 · How the rule is checked

asked: 2026-11-03
answer: "Prompt-Test" — a test checks that the phase prompts that ask questions (01a, 02, 02a, 03, 04b, 06) and the session-entry texts in tools/claude-code name the tool; the chat itself is not checked, a named limit.
answered_by: maintainer
status: answered
context: |
  Topic: how the rule is kept from getting lost.
  Intention: the bead asks for a check, and the addendum should say what a machine can check and what not.
  Today: the question-context gate checks only that each answered Q-record has a context field; no machine sees whether a chat question came through the tool.
  Repository change: Options: A — a test in tests/ over the prompts and session-entry texts; B — extend the question-context gate (a decisions/gates.yaml change for the maintainer); none.
  Architecture change: B would add a gate; A does not.

In the context of a rule no machine can observe in the chat, facing a prompt test, a gate extension or no check, we decided on a prompt test over the asking prompts and the session-entry texts, to achieve a rule that cannot vanish from its carriers unnoticed, accepting that the chat itself stays unchecked. — 2026-11-03

## Q-4 · Harnesses without a question tool

asked: 2026-11-03
answer: "Festes Textformat" — a harness without a structured question tool asks in a fixed text form: exactly one question per message, the five context parts, numbered options with the recommendation first, the question on the last line.
answered_by: maintainer
status: answered
context: |
  Topic: what holds for a harness without a question tool.
  Intention: every harness reads AGENTS.md; Claude Code has AskUserQuestion, Codex exec and Pi have no comparable tool (as of 2026-11-03, from the repository's documents, not measured).
  Today: questions from Codex or Pi arrive as free chat text, sometimes several at once.
  Repository change: a fixed text form in docs/WORKFLOW.md, "The question protocol", and one sentence in the addendum. Options: fixed text form; only Claude Code asks, the others write questions into the handover.
  Architecture change: part of the addendum.

In the context of harnesses without a structured question tool, facing a fixed text form or routing every question through Claude Code, we decided on a fixed text form with one question per message, to achieve the same shape in every harness, accepting that the form is kept by the text, not by a tool. — 2026-11-03

## Q-5 · No exception to one question per call

asked: 2026-11-03
answer: "Keine Ausnahme" — every question, plan cards included, comes one per call; the bead's proposed multi-select call for plan cards is not adopted.
answered_by: maintainer
status: answered
context: |
  Topic: exceptions to "one question per call", and status messages.
  Intention: the last of the five answers for the addendum.
  Today: the bead proposes that status messages carry no question and that plan cards may come together in one multi-select call, each card verbatim.
  Repository change: two sentences in the addendum and docs/WORKFLOW.md, and the multi-select case in prompts/03-plan.md. Options: both as in the bead; no exception; only the status rule.
  Architecture change: part of the addendum.

In the context of the one-question-per-call rule, facing a multi-select exception for plan cards, we decided on no exception: plan cards too come one per call, to achieve one rule without a special case, accepting more calls when several plan cards wait. — 2026-11-03
