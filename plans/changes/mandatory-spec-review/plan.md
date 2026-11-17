---
title: "Plan — mandatory-spec-review"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-ttic
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-terra, 2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, spec-review, stage-2]
---

# Plan — mandatory-spec-review

```text
For you:     Bounded, feature and architectural changes receive a spec review before their plan card; new implementation calls stop on missing, stale or ambiguous reviews.
Done when:   Runner and workflow checks cover the required classes, the spike exception and the morning inventory, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — stop at the limit.
Not now:     Retroactive implementation changes, automatic catch-up reviews, a new gate or verb, and ADR changes.
Pre-mortem:  suppose it failed: most likely because a clean review or a revised spec cannot be distinguished from a missing or stale review.
Starts unless you say stop.
```

## Files and sequence

1. In `scripts/stage2.py`, add one implement precondition before model invocation for bounded, feature and architectural changes, on both normal and `--stage2-off` routes. Read the change class and recorded phase-2a evidence, reject missing or stale evidence and open ambiguity, and report the reason; leave the spike path and other preconditions intact. Make a successful clean review distinguishable from a missing review in `findings.md`, retaining the existing review and redraft workflow. Do not treat a failed review call as evidence. Use the recorded review and last spec change dates required by Q-1; fail closed when the dates or class cannot be established. Do not exempt a change merely because it was implemented before this change merged.
2. In `tests/test_stage2.py`, exercise actual implement admission without invoking external models: missing, stale, current and clean review, open and resolved ambiguity, each required class, spike, both implementation routes, failed review, and a later call on a formerly implemented change. Include the spec revision following review and ensure a review predating it is refused.
3. After the accepted implementation attempt, the orchestrator edits held paths: `AGENTS.md` makes phase 2a mandatory for the three classes and states the spike exception; `prompts/02a-spec-review.md` makes the same scope and clean-review evidence explicit. The orchestrator updates `docs/WORKFLOW.md` to align the class table, phase gate and runner flow, and to require the morning handover to list all open changes without a spec review for individual maintainer decisions. Update affected doctrine assertions in `tests/test_stage2.py` after those edits. No separate design or ADR is due for this bounded change.
4. The runner owns `plans/changes/mandatory-spec-review/findings.md` call evidence and time entries; update the ledger in `plans/changes/mandatory-spec-review/plan.md` as tests are created and regenerate `plans/INDEX.md` for new artifact headers using the repository's registry command. Do not edit historical handovers or automatically run catch-up reviews. Any additional held path goes to the orchestrator, never to the implement attempt.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change mandatory-spec-review
python3 scripts/plans_registry.py --check
make verify
```

## Criterion ledger

- 1: not a test — phase-6 review checks the class table and plan-card sequence against the spec; permitting a card first fails.
- 2: not a test — phase-6 review checks that the new doctrine exempts spikes; requiring review fails.
- 3: not yet written tests/test_stage2.py::test_implement_refuses_missing_or_stale_spec_review — missing or stale evidence reaches a model.
- 4: not yet written tests/test_stage2.py::test_implement_refuses_open_spec_review_ambiguity — an open ambiguity reaches a model.
- 5: not yet written tests/test_stage2.py::test_implement_accepts_current_spec_review — the new precondition rejects current clean or resolved evidence.
- 6: not yet written tests/test_stage2.py::test_implement_exempts_spike_from_spec_review — the new precondition rejects an unreviewed spike.
- 7: not a test — phase-6 review checks the morning handover instructions require a complete open-change inventory and leave catch-up decisions to the maintainer.
- 8: not yet written tests/test_stage2.py::test_implement_rechecks_previously_implemented_change — a later call bypasses the review precondition.

## Time used

2026-11-17 22:27:44–22:29:55 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
