---
title: "Findings — close-budget-clock"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-0n4s
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — close-budget-clock

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1162 files, 5206 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1165 files, 5210 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | Acceptance criteria 3 and 5 ("controlled reconciler clock", "no test clock is installed"); Protected areas | [AMBIGUITY] The spec doesn't say how a controlled clock reaches the reconciler that the protected hook starts as a separate process (`python3 scripts/close_merged_beads.py --write --budget-seconds …`, beads-start.sh:119–121). Reading A: the script gains a test clock that can be selected from outside, for example an environment variable read at start. Criterion 5's "no test clock is installed" then describes that switch in its off state. Production gains a test surface, and the hook test runs the real entry point unchanged. Reading B: inside its disposable project, the test swaps the copied entry script for a wrapper that imports the module and replaces the clock function. Production gains no test surface, but the hook no longer runs the script's own `__main__` block (UTF-8 stream reconfigure, `sys.exit(main())`), so criterion 3 tests a stand-in entry point. decisions.md ("only where it reads the time") leans towards B but doesn't decide it. The two readings lead to different production code and a different integration boundary. | Opus | in spec — [DETAIL] the hook test uses an importing wrapper only in its disposable fixture, and no production clock switch is added; other integration tests exercise the real entry point. The earlier exclusion of the hook test conflicts with the two-test scope in decisions.md and is superseded | — |
| S-2 | MAJOR | SPEC | base | Acceptance criterion 3; Open decisions, second [DETAIL] ("for the two-second test budget") | [AMBIGUITY] The half-second step is decided "for the two-second test budget", but only the close-merged test has a 2 s budget. The session-start test passes 3 − 0.1 = 2.9 s to the reconciler inside a real 3 s watchdog (test_beads_start.py:624–625). Reading A: the step applies to criterion 2 only, and the hook test keeps 3/0.1. A 0.5 s step then gives four closes before the refusal. The real 3 s watchdog still covers git fetch, the render, Python start-up and real stub processes, so under the bead's load the run can still end "abgebrochen". The load sensitivity moves from the batch to the watchdog, and criterion 3 ("real-time sleeps determining the batch") doesn't cover that. Reading B: the hook test is rescaled to a 2 s reconciler budget with a generous real watchdog. That gives three closes, and the watchdog no longer depends on load. Criterion 3 names no count, so under either reading its refutation "accepts an incorrect closure count" has nothing to compare against. | Opus | in spec — [DETAIL] both tests use a 0.5-second step and a two-second reconciler budget; the hook fixture gets a longer outer watchdog so it does not decide the simulated batch. This supersedes the earlier hook exclusion to retain the two-test scope in decisions.md | — |
| S-3 | MAJOR | SPEC | base | Acceptance criteria 2–4 ("without real-time sleeps determining the batch") | Under a controlled clock, the simulated remaining budget still becomes the real `timeout=` of `subprocess.run`. With a 2 s budget and a 0.5 s step that is 2.0, 1.5 and 1.0 s for the closes and 0.5 s for the publication. The spec doesn't say whether the tests run real `tools/bd` stub processes under these real timeouts. The hook test must run them, and criterion 2's test does too if it keeps the current `_run_script` path with its render read-back. If they run real processes, a loaded machine that needs more than 1.0 s for the third stub close or more than 0.5 s for the push raises TimeoutExpired. The close is then refused or "publication failed" appears: the bead's failure class returns, and the criteria only forbid real-time sleeps. If they don't (an in-process `main()` with a recording stand-in, or a wrapper that removes or enlarges the timeouts), the tests stop covering the real stub, the render read-back and the real timeouts, and the timeout arguments have to be asserted somewhere else. Which of the two applies to each test would have to be decided while building. | Opus | in spec — [DETAIL] the tests keep real tools/bd stub processes but intercept the simulated short close and push timeouts, recording and asserting the timeout arguments separately. This corrects the earlier assumption: publication can have a 0.5-second timeout, and even a fast stub can time out under load | — |
| S-4 | MINOR | SPEC | base | Acceptance criterion 5 (refutation "an equivalent sequence of monotonic readings"); criterion 1 | This criterion cannot fail when the default clock is wrong. To feed "a sequence of monotonic readings", some clock has to be controlled. If the test feeds the readings through the seam, a test clock is installed and the no-test-clock path never runs. A default that reads `time.time()` or `time.perf_counter()`, or that binds `time.monotonic` at import, then passes criterion 5. Criterion 1 doesn't catch it either: its refutation covers only bypassing the function or replacing it without effect. The only input that fails is replacing `time.monotonic` itself while the seam is left uninstalled, and the spec doesn't name that input. It is also the only way the existing `monkeypatch.setattr(reconcile.time, "monotonic", …)` keeps working. | Opus | in spec — [DETAIL] patch time.monotonic after import and exercise the default function and a real budget path; call-time delegation also preserves the existing test. This corrects the proposed identity check, which would bind the function at import and miss later monkeypatching | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1165 files, 5215 commits, 12 rules.
