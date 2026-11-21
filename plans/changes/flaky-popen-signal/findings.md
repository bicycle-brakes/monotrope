---
title: "Findings — flaky-popen-signal"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-oag7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — flaky-popen-signal

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5147 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1153 files, 5153 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | phase 2a | spec.md AC1 (l.31–32), AC6 (l.41–42), Definition of Done (l.58), Open decisions (l.65) | [GAP] The spec has no outcome for the case where the cause is not found, or found but not reproducible, within the two-hour appetite. AC1 and AC6 apply only "when" a cause is established, so with no cause neither one can go red. The DoD still requires a recorded cause and a controlled pre-fix failure, so it cannot be met. The implementer would have to choose the result alone: (a) ship a speculative production or test change and call it the cause, (b) stop and hand back with no PR, or (c) open a PR that records "cause not established" with partial evidence. These lead to opposite pull requests, and (a) is the silent filling the bead's "find the race" rules out. | Opus | open | — |
| S-2 | MAJOR | SPEC | phase 2a | spec.md AC1 (l.31–32); decisions.md "Fix at the cause" (l.39) | [AMBIGUITY] decisions.md allows the cause to be only in the test's own cleanup or liveness verdict ("the test is fixed instead and the spec says why production is safe"). AC1 still asks for a controlled regression that "reproduces that cause against the pre-fix code". Reading A: "pre-fix code" means production. The regression is a production-behaviour test that must be red on today's `scripts/stage2.py`. If production is correct this cannot be done, which pushes the implementer to invent a production fault. Reading B: "pre-fix code" means the old test. The reproduction forces the test-side defect: the old verdict reports a survivor while production killed and reaped the child, and production stays unchanged. Separately, no criterion or DoD line requires the "why production is safe" statement that decisions.md names as the output of that branch. | Opus | open | — |
| S-3 | MAJOR | SPEC | phase 2a | spec.md AC2 (l.33–34) against Problem (l.27) and the title sentence (l.23) | [AMBIGUITY] In the worker case, the spec does not say at which point the child must be gone. Reading A, per launch call: the worker's own `launch` kills and reaps its child before it returns or raises. Today's `NotStarted` path in `scripts/stage2.py:1083–1096` already claims this. The cancelled `main` may return 130/143 while the worker is still draining, so the test has to join the worker before its verdict, and the fix can stay in the test. Reading B, per runner cancellation: when the cancelled run returns from `main` (the point where the failing test checks, right after `world.run`), no child from any in-flight launch is still running or unreaped. That needs `main`/`kill_live` to wait for launches in progress, which is a production change. The refutation's wording "after the launch finishes" supports A. The problem statement and "leaves no launched child behind" support B. | Opus | open | — |
| S-4 | MAJOR | SPEC | phase 2a | spec.md title sentence (l.23), AC7 (l.43–44) | [AMBIGUITY] "its regression test gives a deterministic verdict" and "the deterministic signal tests" do not name the tests. Reading A: the existing `test_a_signal_during_process_creation_leaves_no_child` (and the sibling test, if in scope) is rewritten to force its ordering, so the test that flaked on CI cannot flake again. Reading B: a new controlled regression is added and the existing test stays as it is. It can then keep going red at the old rate if the real cause is elsewhere, and every criterion still passes. Because AC7 does not say which tests it covers, a refutation cannot be aimed at any named test. | Opus | open | — |
| S-5 | MINOR | SPEC | phase 2a | spec.md AC5 (l.39–40), Problem (l.27) | [AMBIGUITY] "the sibling main-thread interrupt failure" is singular, but the record holds two: `test_an_interrupt_on_the_main_thread_kills_the_launched_group[Terminated]` on PR #404 (research.md l.34) and `[KeyboardInterrupt]` on PR #419 (decisions.md l.28). Runs 44352084851 and 44697459207 are listed without naming their test. Reading A: only the #419 `[KeyboardInterrupt]` failure, as decisions.md scopes it. Reading B: every recorded failure of the sibling, both parametrizations and the two unnamed runs included. The two readings need different evidence and can lead to a different number of follow-ups. | Opus | open | — |
| S-6 | MINOR | SPEC | phase 2a | spec.md AC5 (l.39–40), Protected areas (l.54) | [GAP] AC5 requires that "a separate follow-up is handed to the orchestrator", but the tracker is protected and the spec names no channel or form for the handoff (a PR-body section, a findings row, a file in the change folder). Without one, the refutation "an evidenced different cause is left without a follow-up handoff" has no artefact a reviewer could check, and the implementer has to invent where the handoff goes. | Opus | open | — |
