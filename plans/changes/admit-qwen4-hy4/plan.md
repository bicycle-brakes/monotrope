---
title: "Plan — admit-qwen4-hy4"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-x0ph
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-16", model: gpt-6.1-terra}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, model-terms, opencode-go]
---

# Plan — admit-qwen4-hy4

```text
For you:     qwen4-max and hy4 can join the paid review ladder after their terms and reachability are checked.
Done when:   Both admissions have compliant source readings, pass fresh probes and follow the existing cost order.
Appetite:    1 hour for phase 4, including repairs; stop when used.
Not now:     longcat-2.0, contributor models and runner changes.
Pre-mortem: suppose it failed: most likely because current public terms or reachability do not support admission.
Starts unless you say stop.
```

## Steps

1. The orchestrator reads the current public OpenCode Go privacy and request tables for each exact id, recording source, date, retention, training and requests per five hours. Derive expiry from an explicit source end date or, if absent, 30 days after reading. If either id lacks compliant terms or a positive sourced request value, stop without admitting it and report the evidence; do not invent values.
2. The orchestrator edits held path `model-endpoints.yaml`: add both ids to `opencode-go.modelle` and each sourced record to `modelle_terms`, using existing fields `gelesen`, `valid_until`, `quelle`, `aufbewahrung`, `training`, `anfragen_5h`, `anfragen_gelesen` and `anfragen_quelle`. This is a bootstrap edit after an accepted attempt; never assign this held path to a stage-2 implement or repair attempt.
3. Run `python3 scripts/stage2.py prepare-loop admit-qwen4-hy4` and inspect the fresh report for each id's catalog definition, address-policy result and probe success. The runner appends probe audit lines to `plans/changes/admit-qwen4-hy4/findings.md`; record the dated result and tested commit in the PR, and stop and report a failure rather than claiming reachability. The preparation may probe other eligible models under the existing policy.
4. Run the verification below; review the diff and source readings against the criteria. Preserve `hy4-preview`, all other existing declarations and runner behavior. Use the decision PR form for the held declaration.

## Verification

```sh
make verify
```

## Criterion ledger

- 1: not a test — review both named memberships in the declaration; either missing id fails.
- 2: tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading — missing or invalid required fields fail; source accuracy is checked against the dated public reading.
- 3: tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading — a missing or invalid request field fails; compare both values with the public table.
- 4: not a test — inspect the fresh `prepare-loop` report; either missing definition or unsuccessful probe fails the criterion.
- 5: not a test — inspect `runner.ladder` output against both recorded request values and the existing descending-value, id-tiebreak rule; a wrong position fails.

## Time used

2026-11-16 16:51:25–16:53:35 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
