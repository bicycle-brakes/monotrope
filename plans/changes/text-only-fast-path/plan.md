---
title: "Plan — text-only-fast-path"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-is4h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, spike, ci, fast-path]
---

# Plan — `text-only-fast-path`

```text
For you:     Evidence and a recommendation on faster hosted checks for text-only pull requests.
Done when:   The note maps gate coverage, measures eligible pull requests and compares alternatives, or identifies evidence missing at the time limit.
Appetite:    2 hours of phase 4, including repairs — a stop, not an estimate.
Not now:     Changing CI or local verification, building a stop hook, or deciding the fast path.
Pre-mortem:  suppose it failed: most likely because historical CI data or test file reads cannot be reconstructed reliably.
Starts unless you say stop.
```

## Work and files

1. Start a two-hour clock. Create `docs/research/2026-11-21-text-only-fast-path.md` as the sole research deliverable; record the source revision, measurement cutoff and limitations. Stop at the limit and report incomplete criteria explicitly.
2. Inventory every entry of `decisions/gates.yaml` by inspecting its command or action and reachable code; record dependencies on Markdown bytes, paths, presence or history, evidence paths, and unknowns. Search `tests/` for named files, live-tree globs, fixtures, scripts run by tests and indirect or dynamic reads; cite sources, record today's glob matches and the repeatable search method, and distinguish unknown coverage from no read. For pytest and `scripts/kit/probe.py --strict`, list the test files over Markdown omitted by each, using that inventory, and compare the documentation faults they detect with the remaining checks; state uncertain coverage.
3. Use `gh pr list`, `gh run list` and paginated API queries to enumerate pull requests merged from 2026-11-01 through a stated cutoff, their final changed paths and hosted CI runs. Use the recorded source revision's test inventory for all PRs, count both rename paths, and record excluded, indeterminate and inaccessible cases. Separately list associated `pull_request` and `merge_group` runs and `push` runs for merge commits, including every rerun and cancelled superseded attempt; record PR and run identifiers, event, attempt, conclusion, timestamps, elapsed seconds and conversion to minutes. Explain intermediate runs with a different diff, shared-run attribution, missing durations and associations; count each run attempt at most once in the total and do not call it savings or billable minutes.
4. Compare at least two alternatives and recommend one with evidence, consequences and risk. A fast-path candidate retains every gate except the two possible skips and tracker hydration; place any pytest or kit-probe conditions on the `gates` job steps and leave the required `verify` aggregator unchanged. Do not prescribe a workflow path filter or assume an unresolved test read is safe.
5. Add a link to the note in `plans/changes/text-only-fast-path/research.md`; review the note against each criterion and protected path. Record phase-4 time in `plans/changes/text-only-fast-path/plan.md` under `## Time used`; the runner regenerates the derived `plans/INDEX.md` from the new plan and spec before its checks. The orchestrator handles any held-path edit if one becomes necessary, rather than assigning it to the attempt; none is planned. Do not change `scripts/ci_gates.py`, `.github/workflows/ci.yml`, `decisions/gates.yaml`, local verification or the stop hook.

## Criterion ledger

- 1: not a test — compare the note's gate inventory with `decisions/gates.yaml` and inspect cited evidence for byte, path, presence and history dependencies; an omitted or unsupported gate fails review.
- 2: not a test — repeat the documented test-read search including globs and indirect reads; an omitted read, glob match or hidden dynamic unknown fails review.
- 3: not a test — compare each candidate's omitted test-file list with the inventory and inspect cited fault coverage; an omitted test file or unsupported claim fails review.
- 4: not a test — recalculate the total from the dated pull request and run-attempt evidence and audit eligibility and attribution; a missing qualifying item, duplicate attempt or mismatched total fails review.
- 5: not a test — compare failed or indeterminate lookups with the limitations; an unreported gap fails review.
- 6: not a test — review the alternatives and recommendation; fewer than two or an absent risk or consequence fails review.
- 7: not a test — review the candidate against the fixed boundaries; skipping another gate or hydration, changing the required aggregator, or using a workflow path filter fails review.
- 8: not a test — compare the phase-4 time record and report with the two-hour stop; overtime or hidden unfinished work fails review.

## Verification

For this text-only change, the author skips local `make verify` under the repository rule; CI and the runner's full check before phase 6 remain required. Run the available document checks before handoff:

```sh
python3 scripts/check_interview_minimums.py --change text-only-fast-path
python3 scripts/plans_registry.py --check
python3 scripts/check_criterion_ledger.py
```

The runner performs its own required checks; record any unavailable command or incomplete data rather than claiming it passed.

## Time used

2026-11-21 15:44:44–15:47:21 UTC, 157 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 16:29:05–16:31:28 UTC, 142 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
