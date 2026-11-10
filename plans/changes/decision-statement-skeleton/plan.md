---
title: "Plan — decision-statement-skeleton"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-nr6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, interview, stage-2]
---

# Plan — decision-statement-skeleton

```text
For you:     The interview asks the downside you accept; draft refuses missing decision statements before spending a model call.
Done when:   Counterexamples prove early refusal and valid-input continuation, the interview instructions require immediate recording, and make verify is green.
Appetite:    3 hours for phase 4, repairs included; stop at the limit.
Not now:     Record migration, a structured record store, a new gate, or changes to make change.
Pre-mortem:  suppose it failed: most likely because the early check and the existing gate interpret statements differently.
Starts unless you say stop.
```

## Files and steps

1. Runner-owned implementation: in `scripts/check_question_context.py`
   expose a statement-only helper over the existing `_records` and
   `_recording_day` reader, returning record-specific problems without
   changing the gate's CLI, context/adoption checks or exit codes. In
   `scripts/stage2.py`, use it for this change's `decisions.md` after the
   existing preflight and pre-existing-change refusal, before snapshots,
   attempt bookkeeping or dispatch. Read failures and problems raise
   `Refused` with the relative path, question id where readable, original
   reason and a return-to-interview remedy; never rewrite decisions or
   enter the fallback chain. Do not run the repository-wide gate here.
2. Runner-owned tests: extend `tests/test_check_question_context.py` to
   compare the helper with the existing reader's malformed/valid cases;
   extend `tests/test_stage2.py` with the dispatch counterexamples below.
   Use committed fixture input so dirty-tree refusal cannot make a missing
   statement test pass. Make `draft_world` use a real answered record and
   statement. Assert no Codex/Claude call, attempt entry, credential read,
   changed answer or new commit on refusal; preserve the current ADR test.
3. After the accepted runner attempt, the orchestrator alone edits the held
   path `prompts/01a-interview.md`: ask the accepted downside with every
   question, preserve context-before-options and question-last ordering,
   and require the complete statement immediately with the answer. An
   answer accepts only the downside actually shown or stated; if unresolved,
   keep it open, never invent it. Keep the existing record fields and dated
   six-part statement template. The orchestrator adds the two prompt tests
   named below in `tests/test_check_question_context.py` with removed-rule
   counterexamples; these tests are added together with the prompt edit,
   so the earlier runner attempt does not require an unavailable held edit.
4. In `docs/WORKFLOW.md`, document immediate faithful interview recording and
   the selected-change draft refusal, retaining the later document job and
   missing-ADR-answer tolerance. In this folder's `spec.md` and `plan.md`,
   update implementation evidence and convert implemented ledger entries
   from `not yet written` to tests. Regenerate `plans/INDEX.md` through
   `python3 scripts/plans_registry.py`; these are derived lifecycle updates.

No files are deleted. Do not touch `scripts/new_change.py`, `decisions.md`,
`decisions/`, endpoint declarations, dependencies, ADRs, restore rules or
other changes. The runner never edits the held prompt. There is no design
file for this bounded change and no Stage-1 fallback recorded in research.

## Verification

Run the targeted check after each repair; after the orchestrator's bootstrap
edit and before phase 6, run the full check:

```sh
.venv/bin/python -m pytest -q tests/test_check_question_context.py tests/test_check_interview_minimums.py tests/test_stage2.py -k 'statement or interview or draft or question or adr_answer'
python3 scripts/check_interview_minimums.py --change decision-statement-skeleton
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_check_question_context.py::test_interview_asks_the_accepted_downside — deleting the explicit downside request still passes
- 2: not yet written tests/test_check_question_context.py::test_interview_records_the_statement_with_the_answer — deferred recording, an invented downside or a missing statement clause/date still passes
- 3: not yet written tests/test_stage2.py::test_draft_refuses_unreadable_statements_before_dispatch — absent, duplicate, wrongly dated or fence-only statements start any model route or leave no actionable diagnostic; include repeated and agent-attributed answered records
- 4: not yet written tests/test_stage2.py::test_draft_refuses_an_unreadable_decision_file_before_dispatch — an I/O or UTF-8 read failure starts a model or rewrites the input
- 5: not yet written tests/test_stage2.py::test_draft_statement_precheck_accepts_supported_records — valid wraps/remarks, old dated answers, open/skipped records or fenced examples are refused
- 5: tests/test_stage2.py::test_only_the_changes_own_missing_adr_answer_is_tolerated — the statement precheck consumes the existing ADR-answer exception
- 5: not yet written tests/test_check_question_context.py::test_statement_helper_matches_the_gate_reader — the helper disagrees with the existing statement grammar or starts enforcing context/adoption itself
- 6: not yet written tests/test_stage2.py::test_draft_statement_precheck_ignores_other_changes — a malformed live or archived neighbour prevents dispatch despite valid selected input

## Time used
