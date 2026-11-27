---
title: "Plan — model-endpoints-refresh"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-363r.5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, model-endpoints]
---

# Plan — model-endpoints-refresh

```text
For you:     The OpenCode Go model declaration reflects dated availability evidence.
Done when:   The deprecated models are removed, all six skips are re-measured, and the seven access failures are recorded and verified.
Appetite:    2 hours for implementation and repairs; stop at the limit.
Not now:     Enabling access, admitting models with unread terms, or changing runner architecture.
Pre-mortem:  suppose it failed: most likely because skipped models cannot be measured through the current runner.
Starts unless you say stop.
```

## Steps

1. Resolve the spec's measurement gap before editing records: `prepare-loop` takes paid candidates from `ladder()`, which excludes skipped terms records. Stop and report if the existing authorized runner cannot measure all six; do not remove a skip merely to force a call or use a side route.
2. Through the runner, gather and preserve dated per-model `prepare-loop` results for the six skipped models and evidence for the seven 403 observations; do not call models with unread terms. Report the selected stages and failures in the main conversation when preparing a review loop.
3. Orchestrator bootstrap edit after any accepted implementation attempt: change held `model-endpoints.yaml` to remove both deprecated ids from admitted lists and seats, retain their terms records, record the dated 410 reason, update the six skip records only according to their measurements and record the seven dated 403 observations as comments without changing their admission for that reason.
4. Orchestrator reviews the evidence against the declaration, then runs `python3 -m pytest tests/test_model_endpoints.py` and `make verify`; start the latter detached with `python3 scripts/jobs.py start -- make verify`. Include the measurement dates, results and commit in the pull request.

Phase 1 fallback: Stage 1 through `claude-code-plan`, model `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (`research.md`, 2026-11-28).

## Criterion ledger

- 1: not a test — phase-6 review checks both lists and seats and the dated 410 evidence; either id remaining or a missing reason fails review.
- 2: not a test — phase-6 review compares each of the six dated runner results with its record; missing evidence, a mismatch or unmeasured admission fails review.
- 3: not a test — phase-6 review compares the seven dated 403 observations and terms records with the declaration; a missing observation or admission change solely due to 403 fails review.
- 4: not a test — phase-6 review inspects runner audit records and admission evidence; a call to a model with unread terms fails review.

## Do not touch

Leave the `claude-code-plan` endpoint and research seat, runner architecture, provider console settings and unrelated terms unchanged. The only implementation file is the held `model-endpoints.yaml`; the orchestrator owns it. `spec.md` and `plan.md` describe the change; `findings.md` receives review results through the established review workflow.

## Time used

2026-11-27 23:21:13–23:23:12 UTC, 118 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
