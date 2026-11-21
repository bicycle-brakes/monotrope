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
2. Inventory every entry of `decisions/gates.yaml` by inspecting its command or action and reachable code; record whether it reads Markdown, evidence paths, and unknowns. Search `tests/` for file opens, fixtures and indirect or dynamic reads; list exact Markdown paths and patterns with source references, distinguishing unknown coverage from no read. Compare pytest and `scripts/kit/probe.py --strict` with the remaining checks for documentation faults they alone could catch.
3. Use `gh pr list` and `gh run list` or their paginated API equivalents to enumerate pull requests merged from 2026-11-01 through a stated cutoff, their changed paths, and associated hosted CI runs and jobs. Apply the spec's eligibility definition including both sides of renames; record excluded and indeterminate cases and inaccessible data. Record PR and run identifiers, attempts, conclusions, timestamps, chosen elapsed-time scope and seconds-to-minutes calculation; avoid counting a run twice and state how reruns, cancelled runs and missing durations are handled. Sum the observed minutes without calling them savings or billable minutes.
4. Compare at least two alternatives and recommend one with evidence, consequences and risk. Any candidate fast path keeps process gates and tracker hydration, limits possible skips to pytest and the kit probe, and uses conditions inside the existing required verify job; do not prescribe a workflow path filter. State unknown test reads as a limit to safe eligibility.
5. Review the note against each criterion and the protected paths. `plans/changes/text-only-fast-path/plan.md` receives phase-4 time in `## Time used`; the runner regenerates the derived `plans/INDEX.md` from the new plan and spec before its checks. The orchestrator handles any held-path edit if one becomes necessary, rather than assigning it to the attempt; none is planned. Do not change `scripts/ci_gates.py`, `.github/workflows/ci.yml`, `decisions/gates.yaml`, local verification or the stop hook.

## Criterion ledger

- 1: not a test — compare the note's gate inventory with `decisions/gates.yaml` and inspect cited evidence; an omitted or unsupported gate fails review.
- 2: not a test — review test read searches and cited sources; an omitted known read or hidden dynamic unknown fails review.
- 3: not a test — review both skip candidates against cited fault coverage; a missing candidate or unsupported claim fails review.
- 4: not a test — recalculate the total from the dated pull request and run evidence and audit eligibility; a missing qualifying item or mismatched total fails review.
- 5: not a test — compare failed or indeterminate lookups with the limitations; an unreported gap fails review.
- 6: not a test — review the alternatives and recommendation; fewer than two or an absent risk or consequence fails review.
- 7: not a test — review the proposed candidate against the fixed boundaries; skipping another process gate or hydration, or using a workflow path filter, fails review.
- 8: not a test — compare the phase-4 time record and report with the two-hour stop; overtime or hidden unfinished work fails review.

## Verification

For this text-only change, CI is the full verification gate; the repository rule skips local `make verify`. Run the available document checks before handoff:

```sh
python3 scripts/check_interview_minimums.py --change text-only-fast-path
python3 scripts/plans_registry.py --check
```

The runner performs its own required checks; record any unavailable command or incomplete data rather than claiming it passed.

## Time used

2026-11-21 15:44:44–15:47:21 UTC, 157 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
