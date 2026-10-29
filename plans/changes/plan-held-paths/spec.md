---
title: "Spec — plan-held-paths"
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
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, planning]
class: bounded
appetite: 1
adr_files: []
---

# Spec — plan-held-paths

Plans identify edits the stage-2 implement or repair runner cannot commit
and assign them to the orchestrator (bead coding-harness-h5tj).
Sources: [research](research.md) and [decisions](decisions.md).

## Problem

As measured on 2026-10-29, the runner rejects substantive edits under
`RUNNER_HELD` and prefixes whose committed provenance permits only
`human-decided`, but the plan prompt gives no such planning constraint
(`research.md`, “The commit guard” and “Per-verb keep sets”). The accepted
review-diff-order plan consequently assigned a prompt edit to an implement
attempt that the guard refused (`decisions.md`, “The intent”). The remedy
is planning guidance and a list-drift test, not a weaker guard.

## Terms

- **Held path:** a path covered by `RUNNER_HELD` or a prefix whose committed
  `provenance.yaml` entry allows exactly `human-decided`.
- **Orchestrator bootstrap edit:** an explicitly assigned edit outside the
  implement or repair attempt, performed by the orchestrating session.

## Acceptance criteria

1. When the draft model reads the plan prompt, its required planning instructions name every current `RUNNER_HELD` entry as outside an implement or repair attempt's committable scope.
   *Refuted by:* any current entry is absent or described as committable by those attempts.
2. When the draft model reads the plan prompt, its required planning instructions also identify prefixes allowed only as `human-decided` by the committed `provenance.yaml` as held.
   *Refuted by:* the rule is absent, uses the attempt's edited map, or treats a mixed-class prefix as held merely because it includes `human-decided`.
3. If a planned step requires a substantive held-path edit, the plan prompt requires the plan to assign it to the orchestrator as a bootstrap edit after the accepted attempt.
   *Refuted by:* the prompt permits assigning that edit to the implement or repair attempt, or omits its owner or timing.

## Non-goals

- Changing the runner's guard, exemptions, restoration, keep sets or verbs.
- Enforcing plans with a new gate, parsing their file lists, or guaranteeing
  that a model obeys the guidance.
- Changing provenance policy, its stale comments, other prompts, or workflow
  doctrine; no ADR is created or amended.
- Design phase 2b does not run for this bounded change.

## Protected areas

`scripts/stage2.py`, `provenance.yaml`, `decisions/`, harness configuration,
and other changes' folders remain untouched: this change documents the
existing boundary rather than changing it. Within `prompts/`, only
`prompts/03-plan.md` is in scope, written by the orchestrator.

## Definition of Done

- The held-list regression test is red before the prompt edit and green
  after it; omitting a newly held entry also makes it red.
- `make verify` is green after the orchestrator's prompt and test edits.
- The same pull request includes `prompts/03-plan.md` and
  `tests/test_stage2.py`; its file list respects the protected areas.
- The review loop and phase-6 review find no unresolved blocker.
- The pull request closes the plan-held-paths work item
  (coding-harness-h5tj); its last commit carries
  `Closes-Bead: coding-harness-h5tj`.

## Open decisions

None open. The reasoned interview skip and bounded class stand in
`decisions.md`; no maintainer answer is inferred here.

[DETAIL] Phase 4 has a one-hour appetite, including repairs, because the
implementation is one prompt item and one regression test; stop at that bound.
[DETAIL] The test checks list coverage; review checks the meaning of the
provenance rule and owner/timing instruction, avoiding assertions tied to
incidental wording.
