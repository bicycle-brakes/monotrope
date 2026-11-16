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
For you:     qwen4-max and hy4 are checked for the paid review ladder; an id that fails is recorded as skipped.
Done when:   Each id has dated evidence and either compliant terms with a successful probe or a reasoned skip.
Appetite:    1 hour for phase 4, including repairs; stop when used.
Not now:     longcat-2.0, contributor models and runner changes.
Pre-mortem: suppose it failed: most likely because the public tables cannot be matched unambiguously to an id.
Starts unless you say stop.
```

## Steps

1. The orchestrator reads the current public OpenCode Go privacy and request tables for each exact id; in `plans/changes/admit-qwen4-hy4/findings.md` preserve the date, source, relevant rows, exact-id attribution, and evidence of missing or ambiguous rows. A single ambiguous Hy4 row is missing for `hy4`; do not borrow `hy4-preview` terms. Record retention, training and requests per five hours; derive expiry from the source end date or 30 days after reading. Retention above zero is allowed when training is `Not used`.
2. The orchestrator edits held path `model-endpoints.yaml` as a bootstrap edit after the accepted attempt: list both ids in `opencode-go.modelle` and add per-id `modelle_terms` records. For compliant readings use `gelesen`, `valid_until`, `quelle`, `aufbewahrung`, `training`, `anfragen_5h`, `anfragen_gelesen` and `anfragen_quelle`; for missing, ambiguous or non-compliant readings use dated `uebersprungen` and factual `grund`, following existing skips. Never assign the held path to a stage-2 implement or repair attempt.
3. Run `python3 scripts/stage2.py prepare-loop admit-qwen4-hy4`; inspect and record each eligible id's refreshed definition, address-policy result and probe in findings, and report the selected stages and failures to the maintainer. For an unmapped API or failed probe, replace that id's terms record with a dated skip and the actual reason; the other id can proceed. Both may be skipped. A refreshed catalog missing the id also cannot establish reachability and is recorded as a skip. The runner may probe other eligible models.
4. Check that each skip fails `terms_problem` and the research probe's shared terms check; eligible records also make those ids research candidates under existing rules. Review the declaration against the saved readings and verify the existing ladder orders eligible ids by requests per five hours, descending with id as tiebreaker. Preserve `hy4-preview`, other declarations, free policy and runner code; use the decision pull request form and record the evidence and tested commit in its body.

## Verification

```sh
make verify
```

## Criterion ledger

- 1: not a test — inspect both exact memberships in `model-endpoints.yaml`; a missing id fails.
- 2: not a test — compare each failed reading or probe with its dated skip and recorded reason; a missing or inaccurate skip fails.
- 3: tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading — missing or invalid fields fail; compare retained values with saved source evidence.
- 4: tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading — invalid request fields fail; compare values with saved source rows.
- 5: not a test — inspect the fresh `prepare-loop` report for each unskipped id; a missing definition or failed probe fails.
- 6: not a test — compare exact-id attribution with the preserved source evidence; an ambiguous row used as proof fails.
- 7: not a test — review the dated evidence in findings against each record and skip; a missing row, attribution or missing-row observation fails.
- 8: not a test — run the existing paid and research terms checks against each skip; either accepting it fails.

## Time used

2026-11-16 16:51:25–16:53:35 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 17:11:51–17:13:36 UTC, 105 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
