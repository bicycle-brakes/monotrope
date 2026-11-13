---
title: "Spec — verify-step-limit"
status: draft
implementation_status: partial
date: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-xkvr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, timeout]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — verify-step-limit

Give executing runner verification steps 45 minutes, with diagnostics and tests
that follow the shared limit (bead coding-harness-xkvr — verification time limit).
Research: [research.md](research.md). Scope: [decisions.md](decisions.md), Q-1.

## Problem

The runner limits verification execution to 30 minutes. Research records full
checks taking 26–28 minutes on 2026-11-10 and verification attempts lost to the
limit in the 2026-11-11 handover; this leaves little margin for a correct run.
At `2ce11fe2` (2026-11-11), the runner's three verification launch sites already
derive their diagnostic from `VERIFY_SECONDS`, but several timeout test messages
and expectations still hard-code 30 minutes. Those tests can drift from the
actual limit (research sections “What exists today” and “Where it lives”).

## Acceptance criteria

1. When the runner starts a verification step currently governed by its shared
   verification limit, its default execution allowance is 45 minutes.
   *Refuted by:* a default other than 2700 seconds or any of the existing
   post-attempt, full-verification or draft-documents paths using a different limit.
   *Basis:* decisions.md#Q-1; research, “What exists today”.
2. When a runner verification step times out, its diagnostic names the minutes
   derived from the current shared execution limit.
   *Refuted by:* a stale 30-minute label at the new default, or a label that fails
   to follow a substituted limit at any of the three existing launch sites.
   *Basis:* decisions.md#Q-1.
3. When the shared verification limit changes, timeout fixtures and expectations
   in the runner tests derive their minute text from that constant.
   *Refuted by:* a timeout fixture or expectation retaining a literal 30-minute
   label, or a test needing its minute text edited after substituting the constant.
   *Basis:* decisions.md#Q-1.
4. While verification waits for machine admission, that wait consumes none of
   its execution allowance.
   *Refuted by:* a queued, otherwise timely check timing out because of its wait.
   *Basis:* decisions.md, “Settled from the tree”; research, admission-wait exclusion.

## Non-goals

- A configuration source or override; central configuration remains separate
  work (bead coding-harness-twvx — central configuration).
- Deriving the limit from measured durations; this needs its own follow-up change.
- Separate budgets per verification job, changed retry counts, faster tests,
  different gate ordering, or changes to timeout cleanup and failure handling.
- Design phase 2b and an ADR: the class is bounded and changes no architecture.

## Protected areas

`scripts/verify_lock.py` and `scripts/verify_all.sh` retain admission and execution
semantics. Tool, git, model and proof time limits stay unchanged. Held paths,
including `decisions/gates.yaml`, `model-endpoints.yaml`, `provenance.yaml`,
prompts and templates, need no edits.

## Definition of Done

- `make verify` green, with the new default pinned and all three launch paths covered.
- Changed code: `scripts/stage2.py` and `tests/test_stage2.py`; change artifacts
  and the generated `plans/INDEX.md` accompany them. No design or ADR is due.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes the verification-limit task (bead coding-harness-xkvr);
  its closing commit carries `Closes-Bead: coding-harness-xkvr`.
- No special long-running timeout demonstration: short substituted limits prove
  enforcement; evidence names the tested commit in the pull request.

## Open decisions

None open. Q-1 settles the 45-minute constant and the deferred stages.

[DETAIL] Keep the draft-documents check on the same shared constant: splitting
its budget would exceed the approved single-constant change.

[DETAIL] Set phase 4's appetite to one hour, repairs included, because the
implementation changes one value and focused test assertions; this is a stop.

[DETAIL] Use the phase-3 prompt's plan form: `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent at `2ce11fe2` (2026-11-11).
