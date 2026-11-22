---
title: "Research — plan-card-what-line"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-kg8n
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# plan card what line — Research

Stage-2 call, 2026-11-22: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1167 files, 5347 commits, 12 rules.

## Runner exploration — 2026-11-22

Research complete. Here is the phase-1 report, prose ready to append to `plans/changes/plan-card-what-line/research.md`.

---

## What exists today

**The decision this change carries.** On 2026-11-11 evening the maintainer decided: "Every plan card explains in plain words what the change does — the problem with one example, what changes, the main risk" (recorded in `docs/journal/handover/2026-11-12-night-ten-lanes.md`, "Decisions and preferences", with the maintainer's words "das muss jetzt immer in die plankarte"; bead coding-harness-kg8n, opened the same night, `docs/journal/handover/2026-11-12-night-ten-lanes.md` "Tracker, carried out tonight"). Until it lands, the interim practice is that the orchestrator adds this explanation by hand to every card it shows (same handover). The bead notes themselves were **not read**: the tracker is the Dolt database under `.beads/`, and this worktree holds only `.beads/config.yaml`, `.beads/metadata.json`, `.beads/interactions.jsonl` and hooks — no readable issue store; the reading path is `scripts/bead_render.py`, which this read-only phase does not run.

**The card as it stands.** The card is defined in `prompts/03-plan.md` ("Every `plan.md` opens with a card"): five content lines in fixed order — `For you:` (what changes for the maintainer), `Done when:` (the evidence), `Appetite:` (time for phase 4, a stop not an estimate), `Not now:` (what is left out), `Pre-mortem:` (one line, "suppose it failed: most likely because \<one reason>"), closed by `Starts unless you say stop.` The card template block and the widening rule ("A card **widens** the scope when its `For you:` or `Done when:` line includes what `spec.md` names as a non-goal…", last line names what widens and asks for "ok") both live in `prompts/03-plan.md`. When phase 3 ends, a contextual preface (Topic, Intention, Today, Repository change, Architecture change — the ADR 0018 question form) is shown before the identical card; the preface "names no field of the card" (`prompts/03-plan.md`, the paragraph above the template).

**Who enforces the card today.** Three independent places, all of which a new line would meet:

1. **The runner's draft check.** `scripts/stage2.py` defines `CARD_LABELS = ("For you:", "Done when:", "Appetite:", "Not now:", "Pre-mortem:")` (comment: "the order the drafted plan.md must open with (spec, criterion 15)") and `CARD_PROBLEM`; `card_problem()` requires the first fenced block below the frontmatter, before the first `## ` heading, to hold all five labels in that order. It is appended to the draft post-run problems in the draft verification path (where `plan.md` exists), and a guard test exercises it as the `"draft-card"` case (`tests/test_stage2.py`, the `verify_draft` guard parameterisation). The docstring cites criterion 15 of the archived `2026-11-06-codex-drafts` spec.
2. **The prompt-form test.** `tests/test_check_question_context.py::_assert_plan_card_form` asserts the card block in `prompts/03-plan.md` itself: exactly **six lines**, the five labels via `zip(..., strict=True)`, last line exactly `Starts unless you say stop.`; `test_plan_card_requires_preface_and_preserves_veto` additionally pins the preface-before-card wording (five parts, in order, "before the card"/"then the card") and mutates the text to refute regressions. This is the test that breaks first when the card gains a line.
3. **The run report.** `scripts/run_report.py::card_appetite_value` lifts only the `Appetite:` line, matching lines by `startswith` against `stage2.CARD_LABELS` inside the opening fenced block; its docstring states defects in other labels do not invalidate the reading, and `appetite_seconds` parses the value (positive hours/minutes, a competing second value is refused). `tests/test_run_report.py::test_readable_appetite_survives_unrelated_card_defect` pins that appetite reading survives a card that `card_problem` rejects.

**How the card reaches the drafting model.** `scripts/stage2.py::DRAFT_PROMPTS = ("02-spec.md", "02b-design.md", "03-plan.md")` — the drafting call feeds the whole phase-3 prompt file, so the card template travels as prompt text; there is no second copy of the template in the runner. `prompts/03-plan.md` exists exactly once in the tree (glob for `**/03-plan.md`); the kit does not carry a prompt copy (`templates/` holds no card text — grep found none).

**Who reads card fields downstream.** `prompts/04-implement.md` reads the card's `Appetite:` as the stop, uses "the appetite and the done-criterion of the card" in the stop block, allows a maintainer answer to replace the card's appetite or `Done when:` line, and states a plan without a card has no appetite. The widening rule reads `For you:`/`Done when:`/`Appetite:` (`prompts/03-plan.md`). The presentation rules: `AGENTS.md` ("An orchestrating session shows a sub-agent's plan card to the maintainer unchanged"), `docs/WORKFLOW.md` phase-2b section ("The plan card reaches the maintainer unchanged — the veto stays theirs"), and the question protocol includes plan cards (`AGENTS.md`, `docs/WORKFLOW.md` "Every question carries its context", ADR 0018).

**The phase-3 gate named in the prompt does not exist.** `prompts/03-plan.md` names `python3 scripts/validate_change_artefacts.py --check` as the gate; no such file is in `scripts/` (glob), and the absence is a recorded finding (`docs/research/2026-11-18-trust-pyramid-against-the-harness.md`; `docs/architecture/target-architecture.md` D-11 plans it as a mechanism entry). The card is therefore held only by the draft post-run check and the pytest suite, not by an artefact-wide validator.

**A frozen snapshot of the prompt exists as a fixture.** `tests/fixtures/research_refs/plan-prompt-d862bc2.md` is a verbatim copy of `prompts/03-plan.md` at blob `d862bc2`, used by `tests/test_stage2_research_refs.py::test_reference_recorded_plan_prompt_extent_uses_exact_structural_title`; the test reads the fixture, not the live prompt, and its comment says the live prompt need not preserve it — editing the live card does not touch it.

**Historical cards are five-label.** Every archived `plan.md` opens with the five-label card (`Starts unless` appears in 30+ archived plans, e.g. `plans/changes/archive/2026-09-30-adhd-frame/plan.md`); they are frozen records outside `card_problem`'s reach (it reads only a freshly drafted `plan.md`).

**The acceptance card is a different card.** `prompts/07-commit.md` ("The acceptance card — what changes for you, how it was checked, what could break") is the pull-request body card; unrelated to the plan card, named here only to keep them apart.

## Where it lives

Definition: `prompts/03-plan.md` (card template + widening rule + preface rule). Enforcement: `scripts/stage2.py` (`CARD_LABELS`, `CARD_PROBLEM`, `card_problem`, draft post-run append), `tests/test_check_question_context.py` (`_assert_plan_card_form`, `test_plan_card_requires_preface_and_preserves_veto`), `scripts/run_report.py` (`card_appetite_value`, `appetite_seconds`). Consumers: `prompts/04-implement.md` (appetite stop), `AGENTS.md` and `docs/WORKFLOW.md` (unchanged presentation, question protocol). Fixtures: `tests/test_stage2.py::PLAN_CARD`, `tests/test_run_report.py::CARD`/`plan_text`, `tests/fixtures/research_refs/plan-prompt-d862bc2.md`.

## What is unclear about it

- **The label and exact wording of the new line are not stated anywhere in the tree.** The decision text gives the content (problem with one example, what changes, main risk) but no label. The change name suggests a `What:` line; that spelling is not written anywhere — open, for the interview/spec to settle.
- **The position in the card order is not stated** — before `For you:`, between it and `Done when:`, or last. `CARD_LABELS`, `card_problem`, and `_assert_plan_card_form` all pin an order, so whichever position is chosen moves through all three.
- **One line or a bounded block** is not stated. The card's own precedent is one line per field, and the pre-mortem is explicitly "one line with one reason, never a list" (`prompts/03-plan.md`); the decision asks for problem, example, change and risk, which may not fit one line at the prompt's 80-character convention (the fixture lint shows MD013 line-length 80).
- **Scope boundaries are not stated:** whether the widening rule must name the new line (a `What:` that promises more than the spec's goals could widen, as `For you:` can today), and whether the acceptance card or the interim hand-add practice is retired by it. The decision names only the plan card.
- **The bead's own description/notes were not read** (Dolt tracker; no readable store in the worktree) — anything the bead adds beyond the handover summary is an open question, answerable with `tools/bd show coding-harness-kg8n`.
- **Whether the appetite term in the run report must keep the label `Appetite:` verbatim** is settled by its spec (archived `2026-11-06-run-report`, "Appetite: the positive phase-4 time budget in the opening plan card's `Appetite:` line") — recorded here as a constraint, not a question: any re-ordering or renaming that touches `Appetite:` pulls the run report's spec in.

## Which files a change would have to touch

- `prompts/03-plan.md` — the card template and, if the widening rule extends, its widening sentence; the preface rule only if presentation wording changes.
- `scripts/stage2.py` — `CARD_LABELS` (labels and order), `CARD_PROBLEM` (the diagnostic names the labels), the `card_problem` docstring (it cites the archived codex-drafts criterion 15 wording).
- `tests/test_check_question_context.py` — `_assert_plan_card_form` (exact line count and label tuple are hard-coded).
- `tests/test_stage2.py` — `PLAN_CARD` fixture and the inline cards in the criterion-15 tests and the `draft-card` guard case (a five-label card becomes a failing card the moment `CARD_LABELS` grows).
- `scripts/run_report.py` and `tests/test_run_report.py` — no parser change is required today (the Appetite lift is order-independent and tolerant of other labels, per its docstring and pinned test), but the `CARD` fixture feeds `card_problem` in `test_readable_appetite_survives_unread_appetite…`-adjacent tests, so the fixture cards' validity under the new label set is in scope.
- `plans/INDEX.md` and the change folder artefacts per the registry row (`plans/INDEX.md`, row for `changes/plan-card-what-line/research.md`); `AGENTS.md` only if the unchanged-presentation rule is extended.

## Neighbours (for the `neighbours:` header)

- `plans/changes/archive/2026-09-30-adhd-frame/spec.md` — the card's origin: criteria 1–8 define the five labels, their order, the one-line pre-mortem, the `Starts unless you say stop.` closing line, the show-unchanged and widening rules, and the no-default-appetite-figure rule.
- `plans/changes/archive/2026-11-06-codex-drafts/spec.md` — criterion 15, the opening-card check `card_problem`'s docstring cites.
- `plans/changes/archive/2026-11-06-interview-context/spec.md` — the context form; "an unchanged plan card follows its contextual preface and keeps its existing final veto invitation"; plan-card presentation inside the question protocol.
- `plans/changes/archive/2026-11-06-run-report/spec.md` — the Appetite term (opening card's `Appetite:` line, frontmatter is no substitute) and the unread-appetite criteria.
- `plans/changes/archive/2026-09-30-template-bundle/spec.md` — the appetite stop, plan card and acceptance card as prompt rules carried by the kit.
- `plans/specs/implementation-verification/spec.md` — the only living spec; checked for card content, none found ("not there", not "not found").
