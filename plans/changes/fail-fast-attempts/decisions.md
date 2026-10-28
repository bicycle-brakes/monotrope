---
title: "Decisions — fail-fast-attempts"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-5tyh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# fail-fast-attempts — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).
One package of three levers (bead coding-harness-5tyh; maintainer,
2026-10-27).

## SKIP · interview

status: skipped
reason: The maintainer approved the package and its three levers on 2026-10-27 ("Ja"), and the bead states the problem, the measurement and the done-criterion: a red cheap check ends the attempt before make verify, the pre-mortem tests appear in the prompt, and a findings.md edit is restored while the attempt still verifies. The change stays inside the existing attempt ladders of implement and repair (research.md, orchestrator addendum); routes, attempt counts, models and ADRs do not move. What remains is mechanics, decided below with reasons.

## Decided by the agent

[DETAIL] **Cheap checks are ruff and the tests of the changed files.**
After an attempt hands back and before `make verify`, the runner runs
`ruff check` and `ruff format --check` on the changed Python files, then
pytest on the changed test files and on the test files that import a
changed module under `scripts/`. A red result there is a failed post-run
check like any other: the attempt block records exactly that output, the
next route receives it, and `make verify` does not run for that attempt.
Green goes on to the full `make verify` as today, so the final verdict is
unchanged. Reason: the measured failures were ruff findings and a named
test, both visible in seconds; the full run stays the one gate.

[DETAIL] **The pre-mortem tests are the plan's criterion ledger.** The
implement and repair prompts name the test ids of the plan's criterion
ledger, and ruff, as must-runs before the model hands back. No new plan
field: the ledger already lists the tests that refute each criterion, and
`scripts/check_criterion_ledger.py` already reads it. Reason: a second list
next to the ledger would drift from it.

[DETAIL] **A runner-owned file edited by an attempt is restored, not
rejected.** When an implement or repair attempt changes `findings.md`
outside the runner's own bookkeeping, the runner puts the file back as it
stood before the model ran, notes the restore in the attempt block, and
checks the rest of the attempt as usual. The repair prompt names
`findings.md` as runner-owned. Reason: the draft verb already restores this
way; rejecting the whole attempt cost 1465 s on 2026-10-27 for an edit the
runner can undo.
