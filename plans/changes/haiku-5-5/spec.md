---
title: "Spec — haiku-5-5"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-eao
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, models, haiku]
class: bounded
appetite: 1
adr_files: []
---

# Spec — haiku-5-5

Use Haiku 5.5 wherever the current workflow selects a Haiku version, while
preserving dated evidence of earlier runs (bead coding-harness-eao).
Research: [research.md](research.md). Authority: the maintainer's answer
of 2026-10-14, [decisions.md](decisions.md), Q-1.

## Problem

The research of 2026-10-14, at `6c66c49`, identifies three coupled leftovers:

- The runner's explicit Stage-1 exploration route still selects
  `claude-haiku-4-5`, and both Anthropic endpoint declarations still list it.
- The current routing tables, fallback instructions and phase prompts still
  direct the maintainer to Haiku 4.5, contrary to the recorded choice of 5.5.
- Existing runner expectations and the kit probe's commit-prompt case name
  embed the old version, so changing only the operative references breaks
  verification or leaves the portability accounting stale.

## Acceptance criteria

1. When exploration runs with `--stage2-off [REASON]`, its selected model is
   `claude-haiku-5-5`.
   *Refuted by:* the recorded Claude command naming another model, or the
   new exploration audit line naming Haiku 4.5.
2. When either `anthropic-api` or `claude-code-plan` is read from the endpoint
   declaration, its authorized Haiku version is `claude-haiku-5-5` in place
   of `claude-haiku-4-5`.
   *Refuted by:* either endpoint missing the new id or retaining the old id.
3. While the maintainer follows the current versioned Haiku instructions,
   those instructions consistently name Haiku 5.5.
   *Refuted by:* a Haiku 4.5 instruction remaining in `AGENTS.md`,
   `docs/WORKFLOW.md`, `prompts/01-explore.md`, `prompts/07-commit.md` or the
   operative docstrings of `scripts/stage2.py`.
4. When the kit probe measures the commit prompt's model-resolution case,
   its portability accounting matches the Haiku 5.5 case without increasing
   the exception allowance.
   *Refuted by:* an unexplained new case, an orphaned Haiku 4.5 entry, or an
   increased exception count or cap.

## Non-goals

- Centralizing model selection; that is a separate change
  (bead coding-harness-ylu).
- Changing other model routes, credentials, permissions, fallback behavior,
  CLI options or the leak check.
- Verifying provider availability, running a paid model probe, or promising
  that a provider serves the requested id; repository evidence does not
  establish this, and a provider refusal keeps its existing behavior.
- Changing unversioned `/model haiku` guidance or the recap hook's `haiku`
  alias; their provider-controlled resolution is outside this version-pin
  update and is not asserted to be Haiku 5.5.
- Rewriting dated records. As a bounded substitution in an existing flow,
  this change has neither a design phase nor an ADR draft.

## Protected areas

- `docs/adr/`, `docs/research/`, `docs/journal/handover/` and other changes'
  artifacts retain their historical model names, including old audit lines;
  Q-1 explicitly preserves dated records.
- `tools/claude-code/`, `.claude/agents/` and `decisions/` need no change to
  the workflow's version pins or the maintainer's recorded answers.
- `scripts/kit/manifest.yaml` and the probe's allowance size, reasons and
  cap stay fixed: one parameterized case changes its name, not its role.
- Unrelated endpoint fields and model ids retain their existing values.

## Definition of Done

- `make verify` green, including model resolution and the strict kit probe.
- Moved together: `scripts/stage2.py`, `model-endpoints.yaml`, `AGENTS.md`,
  `docs/WORKFLOW.md`, `prompts/01-explore.md`, `prompts/07-commit.md`,
  `tests/test_stage2.py` and `scripts/kit/probe.py`.
- The pull request's diff shows the protected areas untouched and the
  non-goals unbuilt.
- The pull request closes coding-harness-eao; its last commit carries
  `Closes-Bead: coding-harness-eao`.
- Special live runs: none; command and declaration checks are local.

## Open decisions

None open. Q-1 already settles the version; this draft decides the following
revisable details and records their reasons.

- `[DETAIL]` Use class `bounded`: the change substitutes a model in an
  existing route without adding a capability or changing an interface.
- `[DETAIL]` Set a one-hour phase-4 appetite, repairs included: the work is
  a coordinated substitution with existing verification; stop at the limit.
- `[DETAIL]` Treat ADRs and earlier change artifacts as dated records, even
  where they describe old fallback rules; the current workflow text receives
  the new version, and Q-1 excludes rewriting that history.
- `[DETAIL]` Leave generic Haiku names and unversioned aliases intact:
  they contain no 4.5 pin to replace, and this change makes no claim about
  their external resolution.
- `[DETAIL]` Retarget existing positive test expectations and their matching
  fault examples; unrelated wrong-model fixtures and historical explanatory
  comments may keep the old name because they do not select a live model.
