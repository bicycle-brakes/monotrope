---
title: "Plan — swarm-report-format"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-4q9y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm]
---

# Plan — swarm-report-format

```text
For you:     Research reports survive harmless wrapping and get one correction after a format rejection.
Done when:   Regression tests and make verify pass, and a real explore accepts every selected seat's report.
Appetite:    9 hours of phase 4 in total, repairs included — a stop, not an estimate (raised by the maintainer on 2026-11-12, decisions.md#Q-6).
Not now:     Schema relaxation, model replacement, transport retries or longer time limits.
Pre-mortem:  suppose it failed: most likely because the correction bypassed the original seat's boundaries.
Starts unless you say stop.
```

## Basis and ownership

Use the nine criteria of `spec.md` and the five maintainer answers in
`decisions.md` dated 2026-11-10. Class stays `bounded`: no `design.md` and
no new ADR draft. The amendment to the existing architecture decision,
`docs/adr/0020-phase-1-research-swarm.md`, point 9, is already prepared at
829e316b; retain it unchanged in the decision pull request. It takes effect
on merge. The prior draft's unanswered budget question is now answered.

The implementation attempt owns the two code/test files below and its spec
and plan bookkeeping. The orchestrator owns held paths, the live run and
findings. No file deletion or unnamed source file is planned.

## Build sequence and files

1. Attempt: in `tests/test_stage2_swarm.py`, use `SwarmWorld` and synthetic
   responses to reproduce leading prose and trailing tool residue; measure
   the wrapper regression red before changing production code. Add the new
   ledger tests for extraction, correction, boundaries, persistence and call
   counts. Parameterise canonical bare/fenced and ambiguous/malformed cases.
   Keep existing contract-failure scenarios invalid on both attempts rather
   than weakening their assertions when a correction now occurs. Retain
   clean-run assertions of `39 + 3N` calls; update manifest-budget assertions
   to distinguish logical slots from the enlarged invocation ceiling.
2. Attempt: in `scripts/stage2_research_run.py`, add topic-only extraction in
   `validate_topic`, leaving `payload_text` and non-topic callers unchanged.
   Accept a bare object or exactly one complete JSON-object fence with text
   around it and no competing object. Locate candidates without changing
   content; feed the selected JSON text to the unchanged strict validator.
   Never choose among objects, repair JSON, strip unknown fields or truncate
   claims. Preserve duplicate-key and non-finite-value rejection.
3. Attempt: in `scripts/stage2_research_run.py`, request one correction for
   each process-successful topic answer rejected by extraction or validation.
   Use the same frozen seat, model, effort and tools, with its original brief
   plus its own rejected answer and the validation reason as untrusted data.
   Keep that data outside instruction authority and neutralise record/fence
   delimiters. Empty process-successful output is a format failure; failed,
   timed-out, cancelled or refused processes are not correction candidates.
   Validate the correction identically; a second invalid answer ends the seat.
   Required failures still prevent the judge, free failures remain named.
4. Attempt: in `scripts/stage2_research_run.py`, send corrections through the
   existing dispatcher, declaration checks, exact-prompt leak check, address
   admission and provider queues. Run initial calls and correction calls in
   non-overlapping dispatch batches, preserving required-before-free order
   within each batch and the provider limit of four. Track each seat's used
   execution allowance; the correction gets only its remaining original
   topic allowance, further capped by the run deadline and judge reserve.
   No fresh allowance is granted. Online prompts contain only their original
   public brief, their own rejected answer and rejection reason; use fresh
   scratch and only the correction's own retrieval receipts for validation.
   A refusal cancels queued work and retains exit-2 precedence as today.
5. Attempt: in `scripts/stage2_research_run.py`, keep one logical slot per
   contribution and runner-owned attempt history inside its durable record.
   Each attempt retains ordinal, exact prompt hash, launch/leak audit, raw
   answer, receipts, process outcome and validation error; store the first
   rejected attempt before dispatching its correction and retain it in later
   writes. Keep the original prompt hash as the logical resume key; an
   explicit final-attempt link selects the validated result and its receipts.
   Persist a pending state and its launch audit before sending the correction;
   a pending or interrupted correction must not expose an `ok` logical result.
   Reuse only the final revalidated successful contribution, preserving its
   full attempt history and original launch provenance; reuse starts no call.
   The existing store's sealed atomic writes/adoption suffice; do not change
   its API. Publish both attempts' evidence through existing manifest/partial
   and audit blocks, including the rejected first attempt after successful
   correction, because complete publication clears the private store. Emit
   one final report/outcome per logical seat for judge, scoring and inventory.
   Keep v2 envelopes and block kinds unchanged. Report the invocation ceiling
   as `72 + 6N`, separately from the `39 + 3N` logical slots and actual calls;
   bound dispatch by one initial and at most one correction per topic slot.
6. Orchestrator, after the accepted attempt: in `docs/WORKFLOW.md`, align the
   research-swarm paragraph's ceiling and no-retry wording with ADR 0020's
   existing amendment, explicitly retaining time limits and prohibiting other
   retries. Regenerate `plans/INDEX.md` from the final artifact headers.
   Run the verification below and the normal prepare/report/fresh-receipt
   sequence for a real explore of an existing eligible change. Record its
   exact commands, date, commit, run identifier, selected seats and accepted
   reports in `plans/changes/swarm-report-format/findings.md`. Use the existing
   public-isolation qualification prerequisite; do not manufacture a feature,
   change this change's class or treat a fixture run as live completion.

The attempt updates `plans/changes/swarm-report-format/spec.md` and
`plans/changes/swarm-report-format/plan.md` as implementation proceeds and
removes `not yet written` from ledger entries when their tests exist. The
runner records measured phase-4 time under `Time used` and owns call evidence.
Stop at the nine-hour appetite, including repair rounds, and report unfinished
work. A newly necessary file or held edit requires a revised plan first.

## Limits and route

Do not edit `scripts/stage2_research_report.py`,
`scripts/stage2_research_store.py`, `scripts/stage2_research_dispatch.py`,
`scripts/check_research_handoff.py`, `research-swarm-limits.yaml`, model
selection/declarations, review-loop parsing, historical artifacts or other
change folders. Held paths, including `prompts/`, `templates/`, `decisions/`,
`.github/` and `AGENTS.md`, are never assigned to the attempt. The existing
ADR amendment and the workflow edit belong to the orchestrator.

Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash` on 2026-11-09;
no Stage-1 fallback is recorded. At baseline 829e316b (2026-11-10),
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
use the phase-3 prompt's form. `findings.md` holds runner audit/diagnostics,
with no open phase-2a review rows. The latest repository handover read,
`docs/journal/handover/2026-11-06-heartbeat-night.md`, does not name this change.
Live PR state and other sessions were not read within this runner's
worktree-only boundary; the orchestrator owns tracker communication.

## Verification

```sh
.venv/bin/python3 -m ruff check scripts/stage2_research_run.py tests/test_stage2_swarm.py
.venv/bin/python3 -m ruff format --check scripts/stage2_research_run.py tests/test_stage2_swarm.py
.venv/bin/python3 -m pytest tests/test_stage2_swarm.py tests/test_stage2_research_report.py tests/test_stage2_research_store.py tests/test_stage2_research_deep_review.py tests/test_research_handoff.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change swarm-report-format
.venv/bin/python3 scripts/check_research_handoff.py --change swarm-report-format
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

For correction tests, cover all observed contract faults (extra top-level and
claim fields, an eighth claim and missing topic-5 relations), the evidence
floor, a valid first answer, successful/invalid correction and empty output.
Plant boundary failures for private/peer context, cross-attempt receipts,
leak refusal, provider concurrency, exhausted topic/run time and judge reserve.
Exercise durable writes, an interrupted correction, resume of a valid corrected
seat, publication after private-store clearing and worst-case calls with
`N=0` and nonzero `N`. Completion must retain every selected valid seat.

The exact live command depends on the orchestrator's eligible change and
fresh receipt and is recorded when selected. Endpoint failure leaves live
completion unverified; it does not justify loosening a criterion.

## Criterion ledger

- 1: tests/test_stage2_swarm.py::test_topic_report_preserves_bare_and_exact_fence — valid canonical reports change or fail
- 2: tests/test_stage2_swarm.py::test_topic_report_accepts_single_wrapped_object — prose or trailing tool residue still rejects valid JSON
- 3: tests/test_stage2_swarm.py::test_topic_report_refuses_ambiguous_or_malformed_objects — extraction chooses among competing objects or repairs invalid JSON
- 4: tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim — missing fields or too many claims pass
- 4: tests/test_stage2_research_report.py::test_report_duplicate_ids_and_extra_fields_are_refused — strict schema violations pass
- 4: tests/test_stage2_research_report.py::test_report_without_any_supported_claim_fails_except_empty_neighbours — unsupported reports pass the evidence floor
- 5: tests/test_stage2_swarm.py::test_topic_report_gets_one_same_seat_correction — the rejected answer/reason is missing, or a missing, duplicate, substituted or non-format correction passes
- 6: tests/test_stage2_swarm.py::test_topic_correction_keeps_security_and_time_boundaries — correction escapes prompt, receipt, queue or original time boundaries
- 7: tests/test_stage2_swarm.py::test_topic_correction_persists_attempts_and_resumes_final_report — lost attempts, duplicate scoring or unvalidated reuse passes
- 8: tests/test_stage2_swarm.py::test_topic_corrections_account_for_every_invocation — hidden or excess correction calls pass
- 9: tests/test_stage2_swarm.py::test_wrapped_and_corrected_seats_complete_explore — a selected seat is dropped or remains failed after a valid correction
- 9: not a test — orchestrator records a real explore's commit, run identifier, selected seats and all accepted reports in findings.md; missing or incomplete live evidence leaves this criterion unverified

## Draft validation — 2026-11-10

Over baseline 829e316b, interview-minimums, criterion-ledger,
frontmatter-current and `git diff --check` passed. Research-handoff explicitly
reported the legacy/no-v2-evidence exemption. These are draft checks, not
implementation or live-run evidence. The general artifact validator and plan
template are absent in this tree. The registry check was not run because its
tracker renderer can read outside the permitted worktree. Index regeneration,
full `make verify` and the commit belong to the runner/orchestrator. No code,
maintainer answer, class or held path was changed by this draft.

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-12

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-12

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-12

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-10 13:20:33–15:44:54 UTC, 8660 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 15:45:23–17:15:25 UTC, 5402 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 17:15:44–19:03:38 UTC, 6473 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-11 23:28:06–23:36:10 UTC, 485 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-11 23:36:28–23:45:44 UTC, 556 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-11 23:46:03–23:53:12 UTC, 429 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 00:37:57–00:41:19 UTC, 202 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 00:41:38–00:46:53 UTC, 315 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 00:47:11–01:05:40 UTC, 1109 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 11:28:28–11:37:32 UTC, 544 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 11:37:47–11:46:48 UTC, 541 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 11:47:05–11:54:14 UTC, 429 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
