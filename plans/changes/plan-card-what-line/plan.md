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
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, plan-card]
---

# Plan — plan-card-what-line

```text
For you:     New plan cards explain the problem, an example, the change and its main risk in plain words.
Done when:   The card instruction, draft checks, date boundary and report regressions pass with make verify.
Appetite:    3 hours of phase 4, repairs included; stop at the limit.
Not now:     A full card redesign, rewriting old plans or changing the acceptance card.
Pre-mortem:  suppose it failed: most likely because the cutoff wrongly rejects an existing plan.
Starts unless you say stop.
```

## Files and sequence

1. In `scripts/stage2.py`, extend the existing opening-card check rather than
   adding a second path: for a spec date strictly after the recorded adoption
   day, require first a nonblank `What:` whose trimmed, case-folded value is
   different from `For you:`; retain the five-label check for older dates.
   Read the spec's frontmatter date and the adoption day through the existing
   adoption reader; unreadable or invalid dates refuse the draft with a useful
   diagnostic. Preserve the other fields' order and the absent-plan diagnostic.
2. In `tests/test_stage2.py`, exercise the real draft verification path with
   valid new cards, missing and blank fields, copied values, ordering, the day
   before/on/after the cutoff, and missing or malformed dates; retain old-card
   and missing-plan coverage. In `tests/test_run_report.py`, update valid card
   fixtures and prove appetite remains readable with a defective `What:`.
3. After the accepted attempt, the orchestrator edits the held
   `prompts/03-plan.md`: add `What:` first, require the three content elements
   in at most three short sentences, and include it in scope widening; keep the
   preface, other fields, ordinary veto and widening approval. There is no
   separate plan template in `templates/` at this revision. In
   `tests/test_check_question_context.py`, update the form and mutation checks
   to hold the new instruction and the existing presentation behavior.
4. The orchestrator records the actual merge date under `plan-card-what-line`
   in the human-decided `decisions/adoption.yaml`, using the existing adoption
   reader; coordinate the date with the merge and update it before merging if
   the planned day changes. Do not invent a past or future merge date. Tests
   use isolated adoption records, including an unreadable or missing record.
5. Update this plan's ledger as tests are written; the runner owns call evidence
   in `plans/changes/plan-card-what-line/findings.md` and the generated
   `plans/INDEX.md`. No file is deleted. The bounded class has no design or
   ADR. Leave historical plans, `tests/fixtures/research_refs/plan-prompt-d862bc2.md`,
   the report parser and `prompts/07-commit.md` untouched.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_run_report.py tests/test_check_question_context.py
make verify
```

Run the focused checks after the orchestrator's prompt and adoption edits; run
the full verification before phase 6. The phase-6 review checks the quality of
the explanation, which the mechanical check cannot establish.

## Criterion ledger

- 1: not yet written tests/test_check_question_context.py::test_what_field_is_first_in_plan_card — a missing or reordered field passes
- 2: not yet written tests/test_check_question_context.py::test_what_field_requires_plain_explanation — the example, change, risk or sentence limit is removed
- 3: not yet written tests/test_stage2.py::test_new_plan_card_requires_nonblank_what — a missing or blank field passes
- 4: not yet written tests/test_stage2.py::test_new_plan_card_rejects_copied_what — the same value with changed case or whitespace passes
- 5: not yet written tests/test_stage2.py::test_old_plan_cards_keep_five_field_check — a valid old card is refused
- 6: not yet written tests/test_stage2.py::test_plan_card_refuses_unreadable_dates — an unreadable date grants an exemption
- 7: not yet written tests/test_check_question_context.py::test_what_field_is_in_scope_widening_rule — an uncovered promise escapes approval
- 8: not yet written tests/test_run_report.py::test_appetite_survives_defective_what — a defective What field hides appetite
- 9: tests/test_check_question_context.py::test_plan_card_requires_preface_and_preserves_veto — the preface or veto is removed

## Time used

2026-11-22 08:36:34–08:39:16 UTC, 162 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
