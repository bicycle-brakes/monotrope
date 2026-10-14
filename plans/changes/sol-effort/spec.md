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
adr_files:
  - docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md
  - docs/adr/0017-codex-repairs-taken-findings.md
---

# Spec — sol-effort

Sol drafts and reviews at effort `high` and repairs at effort `medium`,
with the existing runner contracts retained (bead coding-harness-yzk).
Sources: [research](research.md) and [decisions](decisions.md), Q-1 and Q-2.

## Problem

The runner uses one effort, `max`, for every Sol call, including retries and
resumed review calls. The maintainer reported exhausting the Codex five-hour
window after about ten such calls in one afternoon and asked for an effort
per verb. The current behavior cannot express the agreed difference between
repair and drafting or review (research, "The request" and "Where it
stands", read at `135cb8e` on 2026-10-13 and checked at `9113a3d` on
2026-10-14).

The workflow tables, four phase prompts and the two governing ADRs still
describe Sol at `max`; the doctrine regression also requires it. Changing
only the launch would leave the instructions and checks describing a
different policy (research, "Where it stands" and "Draft preparation").

## Terms

**Sol** means `gpt-6.1-sol` on the declared `openai-codex` endpoint.
**Draft** includes spec, design when due, and plan in one runner call.
**Active instructions** excludes dated historical evidence and the original
ADR decision text that a dated amendment explicitly supersedes.

## Acceptance criteria

1. When `stage2.py draft` invokes Sol, every attempt uses effort `high`.
   *Refuted by:* either the initial call or the `codex-repair` retry passes
   another effort or leaves the effort to the CLI default.
2. When `stage2.py repair` invokes Sol, every attempt uses effort `medium`.
   *Refuted by:* either fresh Codex attempt passes `high`, `max` or no
   explicit effort.
3. When `stage2.py review` invokes Sol, every verdict or loop-marks call
   uses effort `high`.
   *Refuted by:* a fresh, historically resumed, repeated-review or resumed
   loop-marks call passes another effort or omits the pin.
4. When active workflow tables or the Model lines of the spec, design,
   plan and review prompts describe Sol, their efforts match the agreed
   per-verb policy.
   *Refuted by:* a Sol draft/design/plan/review instruction still says `max`
   or `medium`, or a Sol repair instruction says anything but `medium`.
5. When this change is ready for merge, ADR 0016 contains a dated amendment
   stating that `high` supersedes `max` for Sol drafting.
   *Refuted by:* the amendment is missing, undated or assigns another
   drafting effort.
6. When this change is ready for merge, ADR 0017 contains a dated amendment
   stating `medium` for Sol repairs and `high` for phase-6 reviews.
   *Refuted by:* either effort is missing or wrong, or the amendment is
   missing or undated.
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
- Creating a new ADR or rewriting historical decisions and findings.
- A design artifact: this bounded configuration change adds no subsystem
  or boundary; phase 2b does not run for its class.

## Protected areas

Keep the interactive runner, endpoint declaration, permissions, provenance,
gates, decision answers and decision-continuity map unchanged. Other change
folders and historical ADR decision bodies stay intact: the new policy is
recorded by this change's claimed amendments, not by altering earlier
criteria or removing correct ADR claims.

## Definition of Done

- `make verify` is green, and argv and doctrine regressions cover retries,
  resumed calls and each dated amendment with refuting cases.
- The same PR updates `scripts/stage2.py`, `tests/test_stage2.py`,
  `docs/WORKFLOW.md`, `prompts/02-spec.md`, `prompts/02b-design.md`,
  `prompts/03-plan.md`, `prompts/06-review.md`,
  `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md` and
  `docs/adr/0017-codex-repairs-taken-findings.md`.
- The PR file list confirms the protected areas and non-goals; the two
  original ADR decision bodies remain readable with dated overrides.
- The decision PR names every changed bead, closes coding-harness-yzk and
  carries `Closes-Bead: coding-harness-yzk` on its last commit; the
  maintainer's merge makes the amendments effective.
- Special live-model runs: none required; stand-ins establish configured
  arguments, not quota savings or live model quality.

## Open decisions

None open on intent: Q-1 settles the efforts and Q-2 settles dated amendments
without a new ADR. Phase 1a still owes three additional distinct substantive
maintainer answers before the planned ADR edits: only two of five are
recorded. A green draft-only check does not satisfy that prerequisite; this
phase neither interviews nor writes answers for the maintainer.

- [DETAIL] Class `bounded`: the agreed change adjusts existing readable
  flows without adding a capability or changing a boundary; this does not
  reduce the five-answer duty for ADR edits.
- [DETAIL] Allow one hour for phase 4 including repairs, stopping at that
  limit: the change is a configuration and instruction update, not a
  budget-measurement project.
- [DETAIL] Select effort by the caller's verb, including all its retries:
  the shared retry label cannot distinguish drafting from repairing.
- [DETAIL] Retain existing test function names used by older criterion
  ledgers; update their assertions to this amendment rather than editing
  earlier criteria or breaking the ledger anchors.

These reversible details are decided here with their reasons.
