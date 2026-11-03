---
title: "Plan — questions-interview-tool"
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
tags: [plan, question-protocol]
---

# Plan — questions-interview-tool

```text
For you:     Questions use the available question tool one at a time, with a fixed text fallback and deferred questions kept with their context.
Done when:   The rule is in its carriers and the existing ADR addendum, prompt counterexamples fail, and make verify is green.
Appetite:    1 hour of phase 4, repairs included; stop at the limit.
Not now:     A new tool, chat monitoring, new gates or changes to interview counting and question timing.
Pre-mortem:  suppose it failed: most likely because one asking prompt still permits free-chat or bundled questions.
Starts unless you say stop.
```

## Files and steps

1. **Implementation attempt — allowed paths only.** Change `docs/WORKFLOW.md`,
   “The question protocol”, to require the available native question tool
   (Claude Code example: `AskUserQuestion`), exactly one question per call
   including cards, the fixed fallback form from spec Terms, question-free
   status updates, and deferred questions retained with context in the
   handover then asked individually in the next block. Preserve immediate
   timing exceptions, cut/park/drop night answers, classification, recorded
   context and plan-veto semantics. State that tests observe texts, not chat.
2. `tests/test_check_question_context.py`: first add a text-contract helper
   with complete good fixtures and deletion/contradiction counterexamples
   (`test_question_channel_guards_reject_missing_or_conflicting_rules`).
   Parameterize all six prompt paths and the emitted session-entry text;
   mutations must be rejected for each carrier, not just for the combined
   corpus. Check scoped instructions, not stray tool names in examples or
   negations. This accepted attempt need not assert against held texts that
   are not edited yet; final live guards are the next step, not skipped tests.
3. **Orchestrator bootstrap after the accepted attempt.** Only the
   orchestrator changes these held paths; never ask an implement/repair
   attempt to write them:
   - `prompts/01a-interview.md`: add native-tool delivery and the fixed fallback to “How you ask”.
   - `prompts/02-spec.md`: apply that channel to open decisions without adding another interview.
   - `prompts/02a-spec-review.md`: route ambiguities through the orchestrator, which asks individually; keep the reviewer's rows-only contract.
   - `prompts/03-plan.md`: deliver each complete card separately with context, never bundle cards or turn the within-scope veto into mandatory approval.
   - `prompts/04b-review-loop.md`: put question delivery in the orchestrator instructions; reviewers still return only findings.
   - `prompts/06-review.md`: have the orchestrator deliver ambiguity questions through the same channel; preserve read-only review output.
   - `AGENTS.md`: supply the exact proposal below for maintainer review, then apply it in the decision PR; retain every existing duty and the 200-line cap by reflowing the same communication bullet.
   - `docs/adr/0018-every-question-carries-its-context.md`: append a dated proposed addendum from Q-1–Q-5 covering tool/fallback, one-call cards, deferred questions, status separation and the prompt-only assurance limit; preserve accepted history and do not record a new ADR answer.
4. **Orchestrator carrier completion.** Change
   `tools/claude-code/hooks/handover.sh` only in the German SessionStart
   instruction text to repeat tool delivery and one-question serialization,
   refer to the workflow fallback, and separate status from questions.
   Change `tools/claude-code/README.md` to document this entry reminder and
   the existing reinstall command; do not run the installer in this attempt.
   Finish `tests/test_check_question_context.py` with the live guards named
   below, sharing the fixture-tested contract checks; inspect the hook's
   emitted instruction block, not its shell comments. Check the six portable
   prompts and workflow unconditionally; when `tools/claude-code/` exists,
   require AGENTS and the hook rather than skipping a missing carrier (the
   kit omits that whole directory). Include mutation cases for fallback
   context/order/options, deferral, status separation and verbatim-card veto.
5. `plans/changes/questions-interview-tool/spec.md`: update implementation
   status only from evidence. `plans/changes/questions-interview-tool/plan.md`:
   remove ledger markers as functions land and record phase-4 time below.
   `plans/changes/questions-interview-tool/findings.md`: the runner records
   checks/reviews. `plans/INDEX.md`: the runner regenerates it, never hand-edit.
   No file is deleted. The orchestrator presents the card unchanged and
   opens a decision PR; only the maintainer's merge accepts the addendum.

Exact proposed replacement for “Ask one decision at a time, with a
recommendation and its consequence” in the communication bullet (retain its
preceding implemented/proposed/tested instruction):

> Ask every question through the harness's native structured question tool
> when available (Claude Code: AskUserQuestion), exactly one per call,
> including plan cards unchanged with their context and existing veto. Without
> such a tool use one question per message: five context parts, numbered
> options with the recommendation and its consequence first, question last.
> Status updates contain no questions. While the maintainer is away, retain
> questions with context in the repository handover and ask them individually
> in the next question block. Do not re-ask settled decisions or permission.

## Verification

After the bootstrap edits, the orchestrator runs:

```sh
.venv/bin/python3 -m pytest -q tests/test_check_question_context.py tests/test_handover_entry.py tests/test_entry_points.py
.venv/bin/python3 scripts/check_interview_minimums.py --change questions-interview-tool
.venv/bin/python3 scripts/check_research_handoff.py --change questions-interview-tool
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

The runner refreshes the index and performs its verification/commit.
At `ef824324` (2026-11-03), `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent: use `prompts/03-plan.md`
and the existing checks, without creating either missing file. The draft's
interview gate must be green before this plan is handed to implementation.

## Criterion ledger

- 1: not yet written tests/test_check_question_context.py::test_native_question_tool_is_required_in_each_carrier — one listed carrier loses or contradicts the native-tool requirement.
- 2: not yet written tests/test_check_question_context.py::test_question_carriers_allow_only_one_question_per_call — one carrier allows several questions or a multi-select card bundle.
- 3: not yet written tests/test_check_question_context.py::test_question_tool_fallback_has_the_fixed_form — fallback loses a context part, ordering, numbered recommendation-first options or the final question.
- 4: not yet written tests/test_check_question_context.py::test_deferred_questions_keep_context_until_individual_delivery — deferral loses context or allows bulk delivery instead of the next block's individual questions.
- 5: not yet written tests/test_check_question_context.py::test_status_updates_cannot_contain_questions — status instructions allow a question in an update.
- 6: not yet written tests/test_check_question_context.py::test_individual_plan_cards_preserve_context_verbatim_card_and_veto — channel wording removes the preface, truncates the card or requires approval for an ordinary card.
- 7: not yet written tests/test_check_question_context.py::test_question_channel_guards_reject_missing_or_conflicting_rules — a per-carrier deletion or contradictory permission passes the guard.
- 8: not a test — phase-6 review compares the dated existing-ADR addendum with Q-1–Q-5 and checks its prompt-only assurance limit and proposed status; a missing addendum, new ADR or claim of chat enforcement refutes it.

## Boundaries and route

Do not edit gates, endpoint/model declarations, adoption or ADR-answer files,
permissions, settings, installers, kit membership, other ADRs or other change
folders. Existing `tests/test_check_question_context.py` already travels in
the kit; no new manifest entry is needed. Keep existing test names for older
ledgers. A bounded change has no design phase or new ADR draft; the existing
ADR addendum is an orchestrator edit. Explore ran through Stage 2 on
2026-11-03, route flash, endpoint `glm-coding-plan`, model `glm-5.3-flash`;
no Stage-1 fallback is recorded.

## Time used
