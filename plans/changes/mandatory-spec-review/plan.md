---
title: "Plan — mandatory-spec-review"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-18
updated: 2026-11-18
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
For you:     Required changes receive a current spec review before their plan card; implementation stops if the review is missing, stale or ambiguous.
Done when:   Runner tests cover review currency, fallback and the morning inventory, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — stop at the limit.
Not now:     Automatic catch-up, review-loop and phase-6 currency, a new gate or verb, and ADR changes.
Pre-mortem:  suppose it failed: most likely because a review is accepted for spec bytes it did not read.
Starts unless you say stop.
```

## Files and sequence

1. In `scripts/stage2.py`, reuse `declared_class` for every implement route; add one shared review currency writer/check and one review admission check, before model launch. Put the spec bytes in the review prompt, fingerprint the body after front matter, compare disk body bytes at call start and end and fail the call if they differ; accept only exact `No finding.` or readable rows, require the matching adjacent audit line, fail closed if any table line is malformed, read only the newest current qualifying block for ambiguity, and treat only undigested blocks whose heading day is strictly before the fixed implementation day as legacy, compare their day to the last spec commit’s UTC committer day and refuse dirty body edits while ignoring front-matter-only changes. Recognise clean reviews and runner-written fallback blocks; failed calls produce no qualifying evidence. Set a centrally configured initial 30-minute call timeout and retry Opus once after the centrally configured 30-second pause for a nonzero exit, timeout, empty or unreadable answer, then invoke the configured DeepSeek via the existing Pi and leak-check path; do not fall back after a leak-check BLOCK. Keep the declared-at-write fallback model in the block so later configuration changes do not invalidate it. Expose `python3 scripts/stage2.py --spec-review-inventory` as an option on the existing entry point, reusing the same admission result for non-archived changes with a spec, including implemented ones; group missing, invalid and disagreeing classes separately and list only newest current fallback reviews for an Opus re-check in the next day session. The inventory reports errors rather than silently omitting unreadable changes.
2. In `tests/test_stage2.py`, test the shared class and admission path on both routes, body-only fingerprint and header-only/dirty/same-day/fixed-cutoff legacy cases, newest-block, audit matching and partially malformed row parsing, failed or malformed calls, clean reviews, retries, fallback, leak blocks, round exceptions, same-round re-check and inventory scope. Use isolated fixtures and stub model calls; no external model is called by tests.
3. After the accepted attempt, the orchestrator edits held paths: `model-endpoints.yaml` declares the single fallback model and configurable timeout and pause; `AGENTS.md`, `docs/WORKFLOW.md`, `prompts/02-spec.md`, `prompts/02a-spec-review.md` and `prompts/02b-design.md` align review scope, triage and repeat-review sequence including the three-round limit, the maintainer-authorized fourth round or re-slicing for a round-three BLOCKER or spec-changing ambiguity, the same-round Opus re-check of a fallback, exact clean response and fallback. The runner admits a fourth round only when the maintainer authorization is recorded in decisions.md. `tools/claude-code/skills/handover/SKILL.md` instructs the morning handover to run `python3 scripts/stage2.py --spec-review-inventory` and include its output and leave catch-up decisions to the maintainer. The orchestrator updates any affected doctrine assertions in `tests/test_stage2.py` and regenerates `plans/INDEX.md` if needed. The implementing attempt must not edit held paths.
4. The bounded class has no design or ADR. Do not edit prior ADRs, historical handovers, or review-loop and phase-6 currency. The runner owns call evidence in `plans/changes/mandatory-spec-review/findings.md` and phase-4 timing in `plans/changes/mandatory-spec-review/plan.md`; update the ledger as tests are added.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change mandatory-spec-review
python3 scripts/validate_change_artefacts.py --check
python3 scripts/plans_registry.py --check
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_doctrine_requires_review_before_card — The workflow text permits a card before that review.
- 2: not yet written tests/test_stage2.py::test_doctrine_exempts_spike — The workflow text requires the review for a spike.
- 3: not yet written tests/test_stage2.py::test_doctrine_repeats_review_after_edit — The workflow permits the card after the edit without a current review or admits a fourth round without authorization.
- 4: not yet written tests/test_stage2.py::test_implement_refuses_unknown_class — An unknown class reaches a model or the remedy is missing.
- 5: not yet written tests/test_stage2.py::test_implement_exempts_spike_from_spec_review — The new precondition refuses an unreviewed spike.
- 6: not yet written tests/test_stage2.py::test_implement_refuses_missing_stale_or_unreadable_review — A missing, stale, unreadable, unaudited or Codex review admits a model.
- 7: not yet written tests/test_stage2.py::test_implement_names_open_review_ambiguity — The model starts or the refusal omits the row.
- 8: not yet written tests/test_stage2.py::test_implement_accepts_current_review — The new precondition refuses the call.
- 9: not yet written tests/test_stage2.py::test_stage2_off_enforces_review — The flag bypasses either precondition.
- 10: not yet written tests/test_stage2.py::test_spec_review_fingerprints_reviewed_bytes — The block lacks the fingerprint or is recorded for different prompt or disk bytes.
- 11: not yet written tests/test_stage2.py::test_review_currency_rejects_changed_bytes — A changed body is accepted as current or a header-only edit is stale.
- 12: not yet written tests/test_stage2.py::test_legacy_review_currency_by_day — A legacy block before the UTC committer day or with a dirty body is accepted, or an undigested block on the cutoff day qualifies.
- 13: not yet written tests/test_stage2.py::test_spec_review_retries_then_falls_back — Fallback runs before the retry, an unreadable answer or nonzero exit does not trigger it, or a hung call has no timeout.
- 14: not yet written tests/test_stage2.py::test_fallback_spec_review_honours_leak_check — A blocked leak check still permits the fallback call.
- 15: not yet written tests/test_stage2.py::test_fallback_review_is_marked — A fallback block is indistinguishable from an Opus block.
- 16: not yet written tests/test_stage2.py::test_morning_inventory_uses_review_admission — A review or class refusal with a spec is missing, a folder without a spec is listed, or an exempt spike is listed as review-refused.
- 17: not yet written tests/test_stage2.py::test_morning_inventory_names_fallback_rechecks — A current fallback is omitted, its Opus re-check consumes another round, or a later current Opus review remains listed.
- 18: not yet written tests/test_stage2.py::test_implement_rechecks_previously_implemented_change — Earlier implementation exempts the later call.

## Time used

2026-11-17 22:27:44–22:29:55 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 12:48:45–12:51:31 UTC, 166 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 13:36:01–13:37:53 UTC, 112 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 15:31:47–15:33:54 UTC, 126 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 15:36:18–16:00:36 UTC, 1459 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
