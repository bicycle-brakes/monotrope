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

Class: bounded (one counted interview record or a reasoned skip owed;
two answered below).
One package of three levers (bead coding-harness-5tyh; maintainer,
2026-10-27).

## Q-1 · How much time phase 4 gets

context: |
  Topic: the appetite of this change, the stop for phase 4 including the
  review-loop repairs.
  Intention: the drafting model set four hours because no appetite was
  given; the stop is the maintainer's to name.
  Today: the draft's spec and plan state four hours.
  Repository change: this record; spec and plan cite it.
  Architecture change: none.
  Question: how much time does phase 4 get, repairs included?
asked: 2026-10-28, the directing conversation
answer: option 2 — four hours
answered_by: maintainer
status: answered

In the context of the fail-fast package, whose draft set its own appetite
because none was given, facing two, three or four hours, we decided on four
hours of phase 4 including repairs, to achieve a stop the maintainer named,
accepting that the review loop may still reach it. — 2026-10-28

## Q-2 · Who runs the must-run checks before an attempt counts

context: |
  Topic: lever 2, the plan's pre-mortem tests and ruff as must-runs.
  Intention: the approval of 2026-10-27 said the model runs them before it
  hands back, but the implement and repair models can only write files.
  Today: an attempt is judged only after the full make verify (15-24 minutes
  under load on 2026-10-27).
  Repository change: the runner runs ruff and the selected tests right after
  the attempt, before make verify; the prompts name the tests.
  Architecture change: none while the runner runs them; giving the models
  command rights would move a boundary.
  Question: who runs ruff and the plan's tests before an attempt counts?
asked: 2026-10-28, the directing conversation
answer: option 1 — the runner; the model gains no new rights, the prompt
  names the tests, and a red result ends the attempt with exactly that output
answered_by: maintainer
status: answered

In the context of lever 2, where the approval said the model runs the
must-run checks but the implement and repair models only write files,
facing giving the models command rights or letting the runner run the
checks, we decided that the runner runs ruff and the selected tests right
after each attempt and before make verify, to achieve a fast red verdict
without moving the models' boundary, accepting that the model itself never
sees a test run before it hands back. — 2026-10-28

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

## Drafting details — 2026-10-28

The drafting call (Codex, attempt 1) wrote these details; the runner put
`decisions.md` back because a draft may not change it (`findings.md`,
attempt 1). The orchestrator records them here unchanged in substance, with
the two answers above in place of the drafted appetite and delegation.

[DETAIL] **File-only attempts delegate the must-runs to the runner** (Q-2).
Keep the existing model tools. Prompts identify the criterion-ledger test
ids and require ruff and those tests before handback when commands are
available; otherwise they explicitly delegate execution to the runner,
which includes those ids in its cheap pytest selection before full
verification. Both test entry forms count; `not a test` entries do not.
Reason: a file-only model cannot execute the approved must-runs, and
granting commands would change an unrelated boundary.

[DETAIL] **Selection is deterministic and local.** Use changes against the
invocation's HEAD, including untracked files and edits retained from failed
attempts. Select surviving changed test files, direct static importers
under `tests/` of changed Python modules under `scripts/`, and the accepted
plan's ledger test ids. Match Python import statements without importing
tests; dynamic and transitive imports stay with the full suite. Deduplicate
targets and let a selected whole file cover its ledger ids. Reason: this
makes the approved "tests of the changed files" checkable without a new
dependency graph or unrestricted pytest discovery.

[DETAIL] **Keep safe formatting before read-only cheap checks.** Existing
safe fixes and formatting still run; then read-only ruff check/format-check
and selected pytest run before derived-file preparation and full
verification. A launch failure or timeout cannot count as green. Empty
target sets skip their command. Reason: auto-fixable formatting should not
spend a retry, and ruff/pytest without explicit targets would scan broadly.

[DETAIL] **A restore notice is evidence, not a failed verdict.** Restore
the complete pre-call findings snapshot, including the current audit and
earlier evidence, after the existing HEAD/credential checks and model-file
measurement but before verification. Record the restoration in the
attempt's quoted bookkeeping, also when the attempt succeeds; an accepted
attempt's notice must not claim a failure. Reason: restoration must be
visible without manufacturing a rejected attempt or accepting forged state.

[DETAIL] **The phase-4 appetite is four hours, repairs included** (Q-1).
This stop bounds the local runner, prompt and regression work without
promising a performance improvement in minutes. No live model benchmark is
needed for acceptance.
