---
title: "Plan — codex-repairs"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-0ga
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair, codex]
---

# Plan — `codex-repairs`

```text
For you:     Taken review findings move to Codex, with Sonnet 5.5 after two failed post-run checks and a fresh Codex re-check.
Done when:   The 21 criteria have their ledger evidence and make verify is green after your stated ADR answer is recorded.
Appetite:    4 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     Changing the initial implementer, other review models, the loop budget or the red-first proof for test-strength findings.
Pre-mortem:  suppose it failed: most likely because the shared attempt-loop change accidentally routes the initial implementation to Codex.
Starts unless you say stop.
```

Implements [spec.md](spec.md), shaped by [design.md](design.md). The five
interview answers stand; no implementation or ADR answer is recorded here.

## Steps

1. **`scripts/stage2.py`** changes repair's first endpoint to `CODEX` and its
   routes to `(CODEX, None, "codex", None)`,
   `(CODEX, None, "codex-repair", "first Codex post-run check failed")`,
   `(SONNET, None, "stage-1", "two Codex post-run checks failed")`; explicit
   Stage 1 stays one Sonnet route with the caller's reason. Remove repair's
   `GLM_KEY` read, keeping `GLM` for draft's fallback. In `run_attempts`,
   dispatch only `endpoint == CODEX` to `run_codex(..., writable=True)` with
   no resume, use its answer and discard its thread; all other routes retain
   `run_work_model`. Capture a Codex call error, check HEAD against baseline
   before any restoration or post-check, and stop without rewriting on a
   mismatch; otherwise preserve the existing call-error restoration and stop.
   Keep the declaration/leak checks per attempt, diagnostics, time check,
   red-first proof, status restoration and checkpoint callbacks unchanged.
   Make `REPAIR_FORMAT` permit tests and `make verify`, prohibit commits,
   repository-changing git commands and findings edits, request a measured
   time entry and retain the fixed-line forms; it must not claim Codex lacks
   command tools. In `review`, an earlier `## Phase 6` block in
   `findings.md` disables a historical 2a resume; verdict and loop-mark calls
   stay read-only and only the latter resumes the fresh verdict thread.
   Update repair/help comments.
2. **`tests/test_stage2.py`** adapts repair scenarios to `codex_ok` answer-file
   steps, tests both transports, and adds the ledger's new cases; keep existing
   top-level test names because other plans name them. Old GLM-route test
   names remain compatibility anchors with comments explaining ADR 0017;
   their repair assertions test the replacement, retaining coverage of all
   still-applicable guards. Assert Codex pins, no resume or GLM
   secret reads, all three route declarations/leak checks, post-check-only
   fallback, moved HEAD on successful and failed calls, and a re-check seeded
   with an old 2a thread. Retain row-proof, status, failure and implement tests.
3. **`AGENTS.md`**, **`docs/WORKFLOW.md`**, **`model-endpoints.yaml`**,
   **`prompts/04-implement.md`** and **`prompts/04b-review-loop.md`** update
   their current repair instructions and endpoint remarks to this route and
   fresh-session exception; retain GLM for draft's fallback and Flash for
   Explore/initial implementation, and describe Codex's command access and
   sandbox as configured rather than measured. Change no endpoint permissions.
   **`scripts/stage2_runs.py`** corrects only the obsolete current-GLM-repair
   comment, preserving its parser, probe and historical routes.
4. **`docs/adr/0017-codex-repairs-taken-findings.md`** carries the replacement
   contract; **`docs/adr/0015-glm-5-3-repairs-taken-findings.md`** gains only
   `status: superseded`, `superseded_by: "0017"`, a dated update and a note
   explaining that the replacement takes effect on merge, preserving its body.
5. **`plans/changes/codex-repairs/plan.md`** replaces each `not yet written`
   ledger entry when its test exists and measures phase 4 under `Time used`;
   **`plans/changes/codex-repairs/findings.md`** holds runner audits, reviews
   and evidence, written by the runner/orchestrator; **`plans/INDEX.md`** is
   refreshed by the runner's existing derived-file preparation. No deletions.

The runner verifies and makes the checkpoint. The orchestrating session alone
records a maintainer-stated answer in
`decisions/answers/codex-repairs/adr.yaml`, then runs the normal reviews and
opens a decision PR with title `decide(codex-repairs): Codex repairs the taken
findings`, label `decision` and the decision template. It names bead
`coding-harness-0ga`; the draft does not invent or write that answer.

## Do not touch

Keep the initial implement/draft routes, loop ladder and round limits,
the run-count logic, leak checker, gates, provenance, answer schema,
permission settings, other ADRs and continuity map unchanged. Do not rewrite
old change criteria or decisions to satisfy the new routing. Tests use local
stand-ins; no real model call is part of the test suite.

## Explore fallback carried forward

Stage-1 Explore on 2026-10-13 used endpoint `claude-code-plan`, model
`claude-haiku-4-5`, reason: Z.ai weekly limit exhausted until 2026-10-14
14:34 CEST (HTTP 429, code 1310), and Claude Code 2.1.296 refuses the GLM
names (bead coding-harness-6th). That call did not explore; the orchestrator
read the runner at `9ddb38a` and recorded the facts in research. This is
Explore evidence, not a reason to turn off the planned Codex repair route.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py -q
python3 scripts/check_interview_minimums.py --change codex-repairs
python3 scripts/check_criterion_ledger.py
make verify
```

The drafting runner alone tolerates this change's missing ADR answer. A plain
`make verify` still requires that stated answer. The requested
`python3 scripts/validate_change_artefacts.py --check` cannot run in this tree:
the script has not landed; the runner's checks and existing gates apply.

## Criterion ledger

- 1: tests/test_stage2.py::test_repair_uses_codex_at_max_effort — the default route starts Claude or pins a different effort
- 2: tests/test_stage2.py::test_codex_repair_uses_workspace_write_without_bypass — read-only, enabled hooks/memories or a widening flag
- 3: tests/test_stage2.py::test_repair_lists_every_taken_row_and_no_rejected_or_fixed_one — a source omitted or a non-taken row listed
- 3: tests/test_stage2.py::test_the_repair_prompt_carries_the_contract_and_ends_with_the_read_request — accepted inputs or read boundary omitted
- 3: tests/test_stage2.py::test_record_rows_reach_the_model_only_in_the_prompt — unreleased rows materialized in the worktree
- 4: tests/test_stage2.py::test_repair_retry_uses_fresh_codex_with_diagnostics — retry resumes or loses the first diagnostics
- 5: tests/test_stage2.py::test_two_failed_codex_repairs_fall_back_to_sonnet — wrong last model, lost diagnostics or an extra attempt
- 6: tests/test_stage2.py::test_a_failed_repair_process_restores_the_baseline_without_a_further_attempt — a dead Codex call advances or leaves its edits
- 6: tests/test_stage2.py::test_codex_repair_transport_failures_stop_the_chain — missing executable, thread event or answer file reaches fallback
- 7: tests/test_stage2.py::test_stage2_off_repairs_with_one_sonnet_attempt_and_records_the_reason — route/time evidence or supplied reason confused
- 8: tests/test_stage2.py::test_repair_never_reads_the_glm_key — a secret read or Z.ai variable on either transport
- 9: tests/test_stage2.py::test_an_undeclared_repair_endpoint_refuses_before_call — declaration skipped on any of the three routes
- 10: tests/test_stage2.py::test_repair_leak_blocks_each_route_without_fallback — a planted leak at any attempt reaches another call
- 11: tests/test_stage2.py::test_each_repair_attempt_leaves_an_audit_line_the_count_reads — wrong endpoint/route or an uncounted Codex line; extend to all attempts and reasons
- 11: tests/test_stage2.py::test_a_repair_retry_cannot_remove_earlier_attempt_evidence — a passing retry deletes an earlier attempt's audit line
- 12: tests/test_stage2.py::test_a_red_verify_or_a_missing_time_line_fails_a_repair_attempt — diagnostic block/file evidence lost
- 12: tests/test_stage2.py::test_a_failed_repair_puts_every_status_back_as_it_stood — failed model edits survive
- 12: tests/test_stage2.py::test_a_codex_repair_that_commits_findings_restores_statuses_and_records_diagnostics — moved HEAD leaves model-written statuses or loses diagnostics/file evidence
- 12: tests/test_stage2.py::test_a_repair_retry_cannot_remove_earlier_attempt_evidence — a passing retry deletes earlier quoted diagnostics or changed-file evidence
- 13: tests/test_stage2.py::test_a_red_verify_or_a_missing_time_line_fails_a_repair_attempt — checkpoint before a green verify and measured time; assert no checkpoint at the failed boundary
- 13: tests/test_stage2.py::test_each_repair_retry_must_add_its_own_time_entry — a failed attempt's time entry satisfies a retry that records none
- 14: tests/test_stage2.py::test_a_passing_repair_ends_in_one_checkpoint_commit_with_its_statuses — wrong commit count, status or dirty tree
- 14: tests/test_stage2.py::test_a_repair_cannot_change_a_finding_outside_its_batch — a repair changes an unrelated finding's Status, including a phase-2a row
- 14: tests/test_stage2.py::test_the_record_is_marked_only_after_the_checkpoint_commit — private record marked before commit
- 15: tests/test_stage2.py::test_a_named_test_that_is_not_red_first_fails_the_attempt — green baseline test accepted
- 15: tests/test_stage2.py::test_a_fixed_line_naming_an_undefined_test_fails_the_attempt — undefined test accepted
- 15: tests/test_stage2.py::test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt — interpreter failure accepted as defect evidence
- 16: tests/test_stage2.py::test_a_code_row_answered_not_a_test_fails_the_attempt — code row exempted
- 16: tests/test_stage2.py::test_a_text_row_taken_as_not_a_test_is_repaired_and_its_status_written — text-row status/reason lost
- 17: tests/test_stage2.py::test_codex_repair_that_moves_head_stops_without_rewriting — restoration, verification, retry or commit after moved HEAD
- 18: tests/test_stage2.py::test_phase6_after_codex_repair_starts_a_fresh_read_only_session — repair/reviewer/old 2a thread resumed or writable verdict
- 18: tests/test_stage2.py::test_a_phase6_rerun_without_repair_records_the_actual_recheck_reason — an earlier phase-6 block is falsely recorded as a repair
- 19: tests/test_stage2.py::test_repair_starts_no_review_call — an extra verdict/mark call or orchestrator mark written; distinguish Codex repair calls from reviews
- 19: tests/test_stage2.py::test_round_three_starts_after_a_fixed_round_two_row — changed eligibility or an extra round
- 20: tests/test_stage2.py::test_codex_repair_doctrine_and_endpoint_remarks_agree — an active GLM repair claim or a false confinement claim
- 21: tests/test_stage2.py::test_adr_0017_supersedes_0015_and_keeps_the_repair_contract — marker missing, old body rewritten or retained rules omitted

## Runner handoff — 2026-10-13

Drafting starts from branch `feat/codex-repairs`, HEAD `1c5a9ba`, with only the
runner's untracked findings audit present. No phase-2a rows were open. This
call writes spec, design, plan and the one new ADR; implementation remains
pending. Live PR state was not read within the worktree-only boundary. The
orchestrating session owns tracker writes and the dated session handover;
this draft neither claims nor closes the bead, commits nor pushes. Checks on
2026-10-13: interview minimums and criterion ledger green; headers and internal
links checked. Full registry verification and its generated index remain with
the runner, whose tracker access is outside this draft's read boundary. Resume:
read the four draft files against the five interview answers, record only the
maintainer's stated ADR answer, then run the Opus spec review and show the
unchanged plan card after its rows have been resolved.

## Runner route — 2026-10-13

Stage-1 route: implement · model claude-sonnet-5-5 · reason: Z.ai weekly limit exhausted until 2026-10-14 14:34 CEST (HTTP 429, code 1310), and Claude Code 2.1.296 refuses the GLM names (bead coding-harness-6th).

## Time used

2026-10-13 span not measured: this session (Sonnet 5.5, Stage-1 route, file tools only) has no command tool, so `date` could not be read at start or end and no span is estimated; the orchestrator supplies the measured span of this session before the appetite is compared.

2026-10-13 orchestrator repair after the failed implementation attempt, not timed: two doctrine tests planted their fault on raw text where the needle was broken across lines; they now plant on the flattened text the checker reads.

2026-10-13 17:57:06–18:06:17, 9 min 11 s — Codex repaired the taken loop findings (L1-1 to L1-3). The doctrine regression test failed on baseline 25a5a2e before the repairs and passed afterward, including the planted faults for each session-rule location. The focused stage-2, run-count and endpoint suite passed 487 tests; the final doctrine test, ruff lint and format checks, and git diff --check passed. The runner owns make verify and the checkpoint.

2026-10-13 18:31:58–18:40:36, 8 min 38 s — Codex repaired only the taken round-2 rows L2-1, L2-3, L2-4 and L2-5. The cited top-level test name is restored; a moved-HEAD repair restores the original finding statuses and writes its quoted diagnostics and changed-file evidence without rewriting history; a repeated phase-6 review records the earlier Phase 6 block as its reason; the Definition of Done includes prompts/06-review.md. The three new regression cases failed on baseline e371b18 before the code repairs and passed afterward. The focused stage-2, run-count and endpoint suite passed 490 tests; ruff lint and format checks, interview minimums, criterion ledger and git diff --check passed. The runner owns make verify, findings bookkeeping and the checkpoint; the orchestrator owns tracker writes and the dated session handover. Live PR state was not read within this worktree-only boundary.

2026-10-13 19:12:17–19:29:02, 16 min 45 s — Codex repaired only the taken round-3 rows L3-1 to L3-3. WORKFLOW §4 states the Codex repair calls' workspace-write configuration, checked and committed writes, residual read risk and repair prompt destinations at OpenAI and, for Sonnet 5.5, Anthropic. A moved-HEAD audit reports a stop before any post-run check, preserving restored statuses and changed-file evidence. The three regression cases failed on baseline d89bbeb before the repairs and passed afterward, including planted confinement faults; the existing Pi doctrine check now matches its own claim so the Codex paragraph cannot mask a planted Pi fault. The focused stage-2, run-count and endpoint stand-in suite passed 490 tests; ruff lint and format checks, interview minimums, criterion ledger and git diff --check passed. HEAD stays d89bbeb on feat/codex-repairs. The runner owns make verify, findings bookkeeping and the checkpoint; the orchestrator owns tracker writes and the dated session handover. Live PR state was not read within the worktree-only boundary.

2026-10-13 19:53:04–20:12:22, 19 min 18 s — Codex repaired only the taken phase-6 rows F-4 to F-7. Design and plan permit tests and `make verify`, and prohibit commits, repository-changing git commands and findings edits. A passing repair must preserve the pre-call findings body, including every phase-2a row and every earlier attempt’s audit line, quoted diagnostics and changed-file evidence. Each attempt must add its own time line, including after restoring a removed time heading; older diagnostics fixtures now record their retry spans without changing any test name. The final regression functions produced 16 failures and two passing controls against baseline 5dac45c, then passed all 18 cases with the repairs. The focused stage-2, run-count and endpoint stand-in suite passed 508 tests; ruff lint and format checks, interview minimums, criterion ledger and git diff --check passed. HEAD remains 5dac45c on feat/codex-repairs; this call neither edits findings.md nor commits. The runner owns make verify, findings bookkeeping and the checkpoint; the orchestrator owns tracker writes and the dated session handover. Live PR state was not read within this worktree-only boundary.

Resume: run `make verify` for the runner’s final verification and checkpoint.
