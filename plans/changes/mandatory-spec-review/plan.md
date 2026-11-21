---
title: "Plan — mandatory-spec-review"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-19
updated: 2026-11-21
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
For you:     Required changes receive a spec review before their plan card; after three rounds a final draft can proceed without another review.
Done when:   Runner tests cover review currency, fallback and the morning inventory, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — stop at the limit.
Not now:     Automatic catch-up, review-loop and phase-6 currency, a new gate or verb, and ADR changes.
Pre-mortem:  suppose it failed: most likely because a review is accepted for spec bytes it did not read.
Starts unless you say stop.
```

## Files and sequence

1. In `scripts/stage2.py`, reuse `declared_class` for every implement route; add one shared review currency writer/check and one review admission check, before model launch. Put the spec bytes in the review prompt, fingerprint the body after front matter, compare disk body bytes at call start and end and fail the call if they differ; accept only exact `No finding.` or readable rows, require the matching adjacent audit line, fail closed if any table line is malformed, read the newest qualifying block for ambiguity even when the three-round exception applies, and treat only undigested blocks whose heading day is strictly before the fixed implementation day as legacy, compare their day to the last spec commit’s UTC committer day and refuse dirty body edits while ignoring front-matter-only changes. After three review rounds, admit one final spec body version without another review while still requiring qualifying review evidence and applying criterion 7 to open ambiguities; before three rounds refuse stale evidence. Count a fallback and its Opus re-check as one round. Apply the same admission to the inventory. Recognise clean reviews and runner-written fallback blocks; failed calls produce no qualifying evidence. Set a centrally configured initial 30-minute call timeout and retry Opus once after the centrally configured 30-second pause for a nonzero exit, timeout, empty or unreadable answer, then invoke the configured DeepSeek via the existing Pi and leak-check path; do not fall back after a leak-check BLOCK. Keep the declared-at-write fallback model in the block so later configuration changes do not invalidate it. Expose `python3 scripts/stage2.py --spec-review-inventory` as an option on the existing entry point, reusing the same admission result for non-archived changes with a spec, including implemented ones; group missing, invalid and disagreeing classes separately and list only newest current fallback reviews for an Opus re-check in the next day session. The inventory reports errors rather than silently omitting unreadable changes.
2. In `tests/test_stage2.py`, test the shared class and admission path on both routes, body-only fingerprint and header-only/dirty/same-day/fixed-cutoff legacy cases, newest-block, audit matching and partially malformed row parsing, failed or malformed calls, clean reviews, retries, fallback, leak blocks, round exceptions, same-round re-check and inventory scope. Use isolated fixtures and stub model calls; no external model is called by tests.
3. After the accepted attempt, the orchestrator edits held paths: `model-endpoints.yaml` declares the single fallback model and configurable timeout and pause; `AGENTS.md`, `docs/WORKFLOW.md`, `prompts/02-spec.md`, `prompts/02a-spec-review.md` and `prompts/02b-design.md` align review scope, triage and repeat-review sequence including the final draft allowed without another review after three rounds, the maintainer-authorized fourth round or re-slicing for a round-three BLOCKER or spec-changing ambiguity, the same-round Opus re-check of a fallback, exact clean response and fallback. The runner admits a fourth round only when the maintainer authorization is recorded in decisions.md. `tools/claude-code/skills/handover/SKILL.md` instructs the morning handover to run `python3 scripts/stage2.py --spec-review-inventory` and include its output and leave catch-up decisions to the maintainer. The orchestrator updates any affected doctrine assertions in `tests/test_stage2.py` and regenerates `plans/INDEX.md` if needed. The implementing attempt must not edit held paths.
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

- 1: tests/test_stage2.py::test_doctrine_requires_review_before_card — The workflow permits a card without a current review before three rounds or forbids the final draft after three rounds.
- 2: tests/test_stage2.py::test_doctrine_exempts_spike — The workflow text requires the review for a spike.
- 3: tests/test_stage2.py::test_doctrine_repeats_review_after_edit — The workflow permits the card after an edit without a current review before three rounds or admits a fourth round without authorization.
- 4: tests/test_stage2.py::test_implement_refuses_unknown_class — An unknown class reaches a model or the remedy is missing.
- 5: tests/test_stage2.py::test_implement_exempts_spike_from_spec_review — The new precondition refuses an unreviewed spike.
- 6: tests/test_stage2.py::test_implement_refuses_missing_stale_or_unreadable_review — A missing, unreadable, unaudited or Codex review admits a model, or stale evidence admits a model before three rounds.
- 7: tests/test_stage2.py::test_implement_names_open_review_ambiguity — The model starts or the refusal omits the row.
- 8: tests/test_stage2.py::test_implement_accepts_current_review — The new precondition refuses the call.
- 9: tests/test_stage2.py::test_stage2_off_enforces_review — The flag bypasses either precondition.
- 10: tests/test_stage2.py::test_spec_review_fingerprints_reviewed_bytes — The block lacks the fingerprint or is recorded for different prompt or disk bytes.
- 11: tests/test_stage2.py::test_review_currency_rejects_changed_bytes — A changed body is accepted as current or a header-only edit is stale.
- 12: tests/test_stage2.py::test_legacy_review_currency_by_day — A legacy block before the UTC committer day or with a dirty body is accepted, or an undigested block on the cutoff day qualifies.
- 13: tests/test_stage2.py::test_spec_review_retries_then_falls_back — Fallback runs before the retry, an unreadable answer or nonzero exit does not trigger it, or a hung call has no timeout.
- 14: tests/test_stage2.py::test_fallback_spec_review_honours_leak_check — A blocked leak check still permits the fallback call.
- 15: tests/test_stage2.py::test_fallback_review_is_marked — A fallback block is indistinguishable from an Opus block.
- 16: tests/test_stage2.py::test_morning_inventory_uses_review_admission — A review or class refusal with a spec is missing, a folder without a spec is listed, or an exempt spike is listed as review-refused.
- 17: tests/test_stage2.py::test_morning_inventory_names_fallback_rechecks — A current fallback is omitted, its Opus re-check consumes another round, or a later current Opus review remains listed.
- 18: tests/test_stage2.py::test_implement_rechecks_previously_implemented_change — Earlier implementation exempts the later call.
- 19: tests/test_stage2.py::test_final_draft_after_three_spec_review_rounds — A changed body is refused after three rounds or accepted before three rounds; an open ambiguity must still refuse.

## Runner route — 2026-11-18

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM via Z.ai refuses glm-5.3-flash (bead coding-harness-b5pu); the previous Sonnet call ended at claude exit 1; starts from the plan.

## Runner route — 2026-11-19

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-20

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-20

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-17 22:27:44–22:29:55 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 12:48:45–12:51:31 UTC, 166 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 13:36:01–13:37:53 UTC, 112 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 15:31:47–15:33:54 UTC, 126 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 21:56:19–22:17:41 UTC, 1283 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 15:38:12–15:42:11 UTC, 239 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 16:16:50–17:43:15 UTC, 5185 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-19 17:43:25–18:43:27 UTC, 3602 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-19 18:43:40–19:21:34 UTC, 2275 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-19 21:57:37–23:08:24 UTC, 4247 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-20 06:21:00–06:22:06 UTC, 66 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 06:22:15–07:04:47 UTC, 2552 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 07:04:55–07:08:18 UTC, 203 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-20 07:09–07:20 UTC — repair · round 2 · orchestrator hand finishing (Opus subagent) on runner attempt 3 (Sonnet): ruff ARG001 fixed, one interview-record reader for the fourth round (round four only), strict severity in the 2a answer format, row-named tests; targeted tests green (106), full `tests/test_stage2.py` green (2165 passed, 1 skipped); full `make verify` green (6384 passed, 17 skipped; 778 s execution) · measured with `date -u`
2026-11-20 08:15:06–08:16:17 UTC, 71 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 08:16:29–08:17:36 UTC, 67 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 08:17:47–08:52:57 UTC, 2111 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-20 until 11:30 UTC — plan step 3 · orchestrator hand step (Opus subagent), maintainer decision 2026-11-20: `spec_review` block in `model-endpoints.yaml`; AGENTS.md, docs/WORKFLOW.md, README.md, prompts/02-spec.md, prompts/02a-spec-review.md and the handover skill aligned; criterion 1–3 tests tightened and three new anchored tests, all six red first by hand against the old texts; loop rows L2-8, L2-11, L2-12, L3-2..L3-6, L3-10 marked fixed; first full `make verify` red on three older doctrine tests (round wording, five draft steps), repaired; second full `make verify` green (6391 passed, 17 skipped; 1330 s execution) · the two verify runs measured with `date -u` (10:27:18–10:51:42 and 11:07:53–11:30:05 UTC); the edits before them not timed
2026-11-20 14:25–14:54 UTC — repair · round 4 · orchestrator hand finishing (Opus subagent) after the runner refused attempt 1 (codex) for changing `prompts/02a-spec-review.md`: L4-1 (single-edit admission for a spec with no committed version) and L4-2 (the inventory reports a change it cannot measure and goes on) in `scripts/stage2.py`, each test red first by hand against HEAD's `scripts/stage2.py`, restored byte-identical; L4-3 prompt sentence (plan step 3, maintainer 2026-11-20); targeted tests green (138 passed); full `make verify` green (6393 passed, 17 skipped; 888 s execution, 649 s admission wait) · measured with `date -u` and the commit times
2026-11-21 01:44:52–03:16:30 UTC, 5497 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 03:32:56–04:12:50 UTC, 2394 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 04:18:20–04:29:47 UTC, 687 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-21 04:29:56–04:45:39 UTC, 943 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 06:04:03–06:15:33 UTC, 690 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-21 06:15:41–06:45:29 UTC, 1788 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 12:26:58–12:44:32 UTC, 1054 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 13:02:11–13:18:42 UTC, 991 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 13:19:22–13:37:31 UTC, 1088 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 13:55:32–14:16:05 UTC, 1233 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 22:26:35–22:39:50 UTC, 795 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-21 22:39:59–22:58:34 UTC, 1115 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
