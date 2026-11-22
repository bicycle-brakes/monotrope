---
title: "Plan — plan-card-what-line"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-kg8n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, plan-card]
---

# Plan — plan-card-what-line

```text
For you:     New plan cards open with What: — problem with one example, the change, the main risk, in plain words.
Done when:   Card instruction, draft check with date boundary and sentence count, and report regressions pass make verify.
Appetite:    3 hours of phase 4, repairs included; stop at the limit.
Not now:     A full card redesign, rewriting old plans, the acceptance card, the appetite parser.
Pre-mortem:  suppose it failed: most likely because the date boundary exempts a plan it should judge.
Starts unless you say stop.
```

## Files and sequence

1. In `scripts/stage2.py`, extend the existing opening-card check rather
   than adding a second path. A plan is subject when its spec date is later
   than the adoption day read through `scripts/adoption.py` (key
   `plan-card-what-line`); the spec date comes from the spec committed at
   the attempt's base — `verify_draft` receives the `baseline` that
   `draft()` already computes — and from the drafted spec only when the base
   holds none, while an unreadable date or record becomes one more post-run
   problem, never an exemption. For a subject plan the check requires
   `What:` as the card block's first line with a non-blank joined value
   (label line plus indented continuation lines, folded to single spaces) of
   at most three sentences — a sentence ends with a full stop, question or
   exclamation mark followed by a space or the end — whose trimmed,
   case-folded value differs from `For you:`. Plans on or before the
   adoption day keep today's five-label walk, and `CARD_PROBLEM` names the
   labels it refused.
2. In `tests/test_stage2.py`, exercise the real draft verification path with
   isolated adoption records: valid new cards including a wrapped `What:`,
   a missing, blank or late `What:`, a fourth sentence, a copy of
   `For you:` under case and whitespace changes, the day before, on and
   after the adoption day, missing or malformed dates, and a repair-style
   attempt that backdates the spec date committed at its base; retain
   old-card and missing-plan coverage, and move the `PLAN_CARD` fixture to
   six labels.
3. In `tests/test_run_report.py`, update valid card fixtures to the
   six-label card and prove the appetite reading survives a defective
   `What:`; `scripts/run_report.py` itself is not changed.
4. After the accepted attempt, the orchestrator makes the held-path edits —
   the attempt is never told to make them: `prompts/03-plan.md` gains
   `What:` as the first card field with the three content elements in at
   most three short sentences and the allowance to wrap onto indented
   continuation lines, and the widening rule names `What:` with the existing
   "includes" wording, while preface, other fields, closing line, veto and
   widening approval stay; `tests/test_check_question_context.py` moves with
   the prompt in the same edit (`_assert_plan_card_form` pins seven lines
   with `What:` first, the preface/veto and mutation tests keep holding
   presentation); `decisions/adoption.yaml` records the actual merge date
   under `plan-card-what-line`, coordinated with the merge and corrected
   before it when the day moves — no invented date.
5. Update this plan's ledger as tests are written; the runner owns call
   evidence in `plans/changes/plan-card-what-line/findings.md` and the
   generated `plans/INDEX.md`. No file is deleted; the bounded class has no
   design and no ADR. Historical plans,
   `tests/fixtures/research_refs/plan-prompt-d862bc2.md`,
   `scripts/run_report.py` and `prompts/07-commit.md` stay untouched.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_run_report.py tests/test_check_question_context.py
make verify
```

Run the focused checks after the orchestrator's prompt and adoption edits
(the form test reads the live prompt); run the full verification before
phase 6. The phase-6 review judges the quality of the explanation, which no
mechanical check establishes.

## Criterion ledger

- 1: not yet written tests/test_check_question_context.py::test_what_field_is_first_in_plan_card — a missing or reordered field passes
- 2: not yet written tests/test_check_question_context.py::test_what_field_requires_plain_explanation — the example, change, risk or sentence limit leaves the instruction
- 3: not yet written tests/test_stage2.py::test_new_plan_card_requires_first_nonblank_what — a missing, blank or late What passes
- 4: not yet written tests/test_stage2.py::test_new_plan_card_refuses_fourth_sentence — a four-sentence What passes
- 5: not yet written tests/test_stage2.py::test_new_plan_card_rejects_copied_what — the same joined value with changed case or whitespace passes
- 6: not yet written tests/test_stage2.py::test_old_plan_cards_keep_five_field_check — a valid old card is refused
- 7: not yet written tests/test_stage2.py::test_plan_card_refuses_unreadable_dates — an unreadable date grants an exemption
- 8: not yet written tests/test_stage2.py::test_subject_date_comes_from_base_spec — an attempt-edited backdate exempts the plan
- 9: not yet written tests/test_check_question_context.py::test_what_field_is_in_scope_widening_rule — an uncovered inclusion escapes approval
- 10: not yet written tests/test_run_report.py::test_appetite_survives_defective_what — a defective What hides the appetite
- 11: tests/test_check_question_context.py::test_plan_card_requires_preface_and_preserves_veto — the preface or veto is removed

## Time used

2026-11-22 08:36:34–08:39:16 UTC, 162 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 08:45:14–08:51:46 UTC, 391 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
