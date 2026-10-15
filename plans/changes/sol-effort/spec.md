---
title: "Spec — sol-effort"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-yzk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, codex, effort]
class: bounded
appetite: 1
adr_files: []
---

# Spec — sol-effort

Sol's effort is set once per runner verb, initially `high` for drafting and
review and `medium` for repair, and instructions and tests follow that setting
(bead coding-harness-yzk). Sources: [research](research.md) and
[decisions](decisions.md), Q-1 to Q-6.

## Problem

The runner uses one effort, `max`, for every Sol call, including retries and
resumed review calls. The maintainer reported exhausting the Codex five-hour
window after about ten such calls in one afternoon and asked for an effort
per verb. The current behavior cannot express the agreed difference between
repair and drafting or review (research, "The request" and "Where it
stands", read at `135cb8e` on 2026-10-13 and checked at `9113a3d` on
2026-10-14).

The workflow tables, drafting prose and four phase prompts repeat Sol's
effort, and launch and doctrine regressions repeat `max`. Changing only the
launch would leave contradictory instructions; replacing all literals would
still require several edits for the next adjustment. The maintainer instead
asked for one central parameter that runner, instructions and tests follow
(research, "Where it stands"; decisions, Q-4). ADR amendments are deferred
to their own change by the maintainer's later answer (decisions, Q-3).

## Terms

**Sol** means `gpt-6.1-sol` on the declared `openai-codex` endpoint.
**Draft** includes spec, design when due, and plan in one runner call.
**Initial settings** means the effort values this change ships, fixed by Q-1;
a later deliberate adjustment uses the same central declaration.
**Active instructions** means Sol effort instructions in the workflow's
section-3 and section-4 tables and prose, including "The draft (phases 2, 2b
and 3)", and in the Model paragraphs of the spec, design, plan and review
prompts. It excludes dated evidence, change artifacts and the ADR text whose
amendment Q-3 explicitly defers.

## Acceptance criteria

1. When `stage2.py draft` invokes Sol with the initial settings, every
   attempt explicitly passes reasoning effort `high`.
   *Refuted by:* the initial call or its `codex-repair` retry passes another
   effort or leaves it to the CLI default.
2. When `stage2.py repair` invokes Sol with the initial settings, every
   attempt explicitly passes reasoning effort `medium`.
   *Refuted by:* either fresh Codex attempt passes another effort or omits
   the override.
3. When `stage2.py review` invokes Sol with the initial settings, every
   verdict or loop-marks call explicitly passes reasoning effort `high`.
   *Refuted by:* a fresh, historically resumed, repeated-review or resumed
   loop-marks argv passes another effort or omits the pin; the effort actually
   used inside a resumed thread is not asserted (Q-6).
4. When an active instruction describes Sol's effort, it references the
   central setting for that instruction's runner verb.
   *Refuted by:* a table, drafting prose sentence or Model paragraph supplies
   an independent Sol effort value, omits the reference or points to the wrong
   verb; spec, design and plan all belong to `draft` (Q-4).
5. When one supported Sol effort is changed in the central declaration, the
   next runner invocation of that verb passes the new setting without edits
   to instructions or tests.
   *Refuted by:* another operational default must be edited, a retry or resume
   retains the old setting, or a correct adjustment breaks tests that repeat
   the old value (Q-4).
6. When a Sol effort check reads an instruction naming several models, it
   assesses only the effort reference associated with Sol.
   *Refuted by:* a valid Sol reference is rejected because Opus or Sonnet has
   its own literal effort, or a wrong Sol reference passes because another
   model has a correct effort (Q-5).
7. When `stage2.py session` launches interactive Codex, the runner supplies
   no reasoning-effort override.
   *Refuted by:* an effort flag or configuration override is added to that
   interactive launch.

## Non-goals

- Measuring or guaranteeing subscription savings, review quality or the
  number of calls available in a five-hour window.
- Changing models, endpoints, fallbacks, attempt counts, session/resume
  rules, sandboxes, leak checks, evidence, checkpoints or audit formats.
- Changing any non-Sol effort, including GLM, the OpenCode Go ladder,
  Opus and Stage-1 fallbacks, or selecting an interactive-session default.
- Creating or amending an ADR: the dated amendments to ADR 0016 and ADR 0017
  follow in their own change after its interview prerequisite is met (Q-3).
- Rewriting historical evidence or introducing a general model configuration
  system, a new CLI option or an environment override.
- A design artifact: this bounded configuration change adds no subsystem
  or boundary; phase 2b does not run for its class.

## Protected areas

Keep `scripts/stage2_session.py`, `model-endpoints.yaml`, `AGENTS.md`,
permissions, provenance, gates, decision answer files and the
decision-continuity map unchanged: this change adjusts effort, not authority
or routing. Other change folders and all ADR files stay intact under Q-3.
The six maintainer answers in this change's `decisions.md` are inputs, not
editable defaults.

## Definition of Done

- `make verify` is green; argv and doctrine regressions cover retries,
  resumed calls, central-setting changes and the active prose with refuting
  cases. Phase 6 independently compares the shipped defaults to criteria 1–3.
- The same PR updates `scripts/stage2.py`, `tests/test_stage2.py`,
  `docs/WORKFLOW.md`, `prompts/02-spec.md`, `prompts/02b-design.md`,
  `prompts/03-plan.md` and `prompts/06-review.md`. No model declaration or ADR
  moves in this PR; the workflow identifies the separately deferred ADR text.
- The PR file list confirms the protected areas and non-goals.
- The PR names every changed bead, closes coding-harness-yzk and carries
  `Closes-Bead: coding-harness-yzk` on its last commit.
- Special live-model runs: none required; stand-ins establish configured
  arguments, not quota savings or live model quality.

## Open decisions

None open. Q-3 supersedes Q-2's scope for this PR: the earlier ADR criteria
are removed because the maintainer split that work off, not to bypass a gate.
Q-4 adds central parameterization; Q-5 settles mixed-model checks; Q-6 limits
resumed-call evidence to argv. All four phase-2a rows are in this spec.

- [DETAIL] Keep the existing `bounded` class and one-hour implementation
  appetite, including repairs: the answers adjust an existing runner flow;
  phase 2b therefore produces no design artifact.
- [DETAIL] Put the small per-verb declaration in the existing runner and
  reference it from instructions: this is one reversible editing location
  without a new configuration file or subsystem.
- [DETAIL] Select effort by caller verb, including retries: `codex-repair`
  names a retry of both draft and repair and cannot select the policy itself.
- [DETAIL] Tests read the central settings and plant distinct alternative
  settings to catch crossed verbs; phase 6 checks the initial values against
  this spec, avoiding a second operational policy inside test assertions.
- [DETAIL] Keep existing test names used by older ledgers, including the name
  mentioning `max`, while updating their assertions: historical artifacts
  and their anchors stay readable.

These reversible details are decided here with their reasons.
