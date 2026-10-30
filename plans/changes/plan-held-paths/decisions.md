---
title: "Decisions — plan-held-paths"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-h5tj
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# plan-held-paths — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: the change adds one required
item to the plan prompt (`prompts/03-plan.md`) and one test that keeps it in
step with the runner's held paths; no gate, ADR or runner behavior changes.

The intent, which the explorer could not read: the bead (coding-harness-h5tj)
targets mechanism (1) of the research, the runner-held paths a stage-2
implement or repair never commits (`RUNNER_HELD` and the `human-decided`-only
prefixes of `provenance.yaml`, `scripts/stage2.py`). Its trigger: the
implement attempt 2 of review-diff-order (coding-harness-ut8q) was refused on
2026-10-29 for editing `prompts/04b-review-loop.md`, a step its accepted plan
named.

## SKIP · interview

status: skipped
reason: the bead (coding-harness-h5tj) states the remedy — the plan template and the draft prompt state which paths a stage-2 implement or repair does not commit, so a plan routes those edits to the orchestrator — and the maintainer decided the same routing for review-diff-order on 2026-10-29 (the prompt edit moves from the model to the orchestrator); no question remains that only the maintainer can answer.

## Details for the draft

[DETAIL] **The plan prompt is the template.** No `templates/plan.md` exists;
the plan's required items live in `prompts/03-plan.md` ("Required:"), which
the draft verb sends (`DRAFT_PROMPTS`). The new item goes there. Reason:
measured 2026-10-29, `ls templates/`.

[DETAIL] **The prompt names the held set by its rule and its list.** It names
the `RUNNER_HELD` entries and says that a `human-decided`-only prefix of
`provenance.yaml` is held too; a step that edits one of them is marked as the
orchestrator's bootstrap edit after the accepted attempt. Reason: the list
changes rarely; the rule covers the map without copying it.

[DETAIL] **A test keeps the prompt in step.** A test in `tests/test_stage2.py`
asserts that every `RUNNER_HELD` entry appears in `prompts/03-plan.md`, red
when an entry is added to the runner without the prompt. Reason: a copied
list drifts; the test is the place the drift is caught.

[DETAIL] **The orchestrator implements this change.** The edit is under
`prompts/`, itself a runner-held path, so a stage-2 implement attempt cannot
commit it, and the test alone would stay red in the attempt. The orchestrator
writes test and prompt edit by hand, shows the test red first, runs
`make verify` and then the review loop and phase 6 as for any change.
Reason: the same routing as the maintainer's decision for review-diff-order;
the runner's guard is the cause, not a model failure.
