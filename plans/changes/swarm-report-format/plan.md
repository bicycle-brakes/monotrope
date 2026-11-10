---
title: "Plan — swarm-report-format"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-10
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
Appetite:    3 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Schema relaxation, model replacement, transport retries or longer time limits.
Pre-mortem:  suppose it failed: most likely because the correction bypassed the original seat's boundaries.
The invocation ceiling would widen from 39 + 3N to 72 + 6N; please answer "ok" to the decision in spec.md before phase 4.
```

## Prerequisite — blocked draft

Do not start phase 4: `spec.md` identifies a conflict with the decided
no-retry rule and invocation ceiling (ADR 0020, point 9). An agent's mechanical
choice in `decisions.md` does not override it. The implementation sequence
below is conditional on the recommended decision, not permission to build it.
The orchestrator must resolve that decision, meet the resulting interview/ADR
requirements and redraft with every governance path named before execution.
No governance file is claimed or drafted here; `adr_files: []` describes this
draft, not permission to omit the prerequisite later. Class stays `bounded`;
phase 2b does not run.

## Build sequence and files

1. Attempt, once unblocked: in `tests/test_stage2_swarm.py`, add the ledger's
   tests using its existing `SwarmWorld` stand-ins. Reproduce the leading
   sentence and trailing tool residue as synthetic responses; do not read or
   copy the historical external run. Measure the wrapper regression red before
   changing production code. Cover bare/fenced input, two fences, bare plus
   fenced objects, invalid JSON and the rejection/correction cases below.
2. Attempt: in `scripts/stage2_research_run.py`, add a topic-only extractor
   used by `validate_topic`; keep `payload_text` behaviour for finder, merge
   and judge callers. Accept one complete object fence with surrounding text
   only when no competing object exists. Feed its bytes to the unchanged
   strict validator; never merge objects, discard keys or truncate claims.
3. Attempt: in `scripts/stage2_research_run.py`, add one explicit correction
   dispatch for process-successful invalid topic reports, using the same
   selected endpoint/model/effort/tools, original frozen brief and only that
   seat's rejected answer and validator reason as quoted data. Do not launch
   again for a valid answer, process failure or second rejection. Dispatch
   corrections through the existing admission, leak-check and provider queue;
   consume the remaining original topic allowance and preserve the run
   deadline and judge reserve. Online corrections use only public context and
   their own new fetch receipts, never merged receipts from the first call.
4. Attempt: in `scripts/stage2_research_run.py`, persist first and correction
   launch/result evidence under distinct attempt identities using existing
   store operations; retain one final topic/seat result for reports and judge
   outcomes. Preserve the base prompt hash for logical-slot resume matching,
   the correction prompt hash for its own audit, both raw answers/errors and
   an explicit final-attempt link. Never overwrite the first result. Reuse
   only the final revalidated successful report with its matching receipts;
   reuse launches nothing, and failed/interrupted results remain ineligible.
   Publish attempt evidence as runner-owned audit/partial data without adding
   duplicate topic reports or trusting model-supplied metadata. Account for
   initial and correction calls separately and enforce the authorised ceiling.
5. Attempt: in `tests/test_stage2_swarm.py`, exercise correction success and
   repeated failure, all four observed contract violations, empty successful
   output, no process retry, online isolation/receipts, leak refusal, exhausted
   topic/run time, concurrency, persistence/resume and worst-case call counts.
   Preserve clean-run `39 + 3N` assertions; add corrected-run bounds rather
   than weakening the existing clean-run tests. Gate changes remain forbidden.
6. Orchestrator: after the accepted attempt and required governance work,
   run verification and an authorised live research explore through the normal
   prepare/report/receipt sequence for an existing eligible change. Record the
   exact invocation and completion evidence in this change's
   `plans/changes/swarm-report-format/findings.md`; do not manufacture a feature
   or change this bounded change's class to obtain a live run.

The attempt updates implementation status in
`plans/changes/swarm-report-format/spec.md` and
`plans/changes/swarm-report-format/plan.md` and removes `not yet written`
ledger markers as tests are defined. The runner owns measured time entries
and findings-call evidence. No file deletion. Any newly required source file
or held-path edit requires a revised plan before the attempt, not an implicit
extension of this list. The runner/orchestrator regenerates `plans/INDEX.md`;
this draft does not edit it.

## Limits and route

Do not edit `scripts/stage2_research_report.py`,
`scripts/stage2_research_store.py`, `scripts/stage2_research_dispatch.py`,
`scripts/check_research_handoff.py`, `research-swarm-limits.yaml`, model
declarations, review-loop parsing, historical artifacts or other change
folders. All held paths, including `prompts/`, `templates/`, `decisions/`,
`AGENTS.md` and human-decided ADRs/workflow, belong to the orchestrator after
explicit resolution; the attempt must never edit them.

Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash` on 2026-11-09;
no Stage-1 fallback is recorded. At draft baseline b9a87940 (2026-11-09),
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
use the phase-3 prompt's form. `findings.md` contains draft-call evidence and
no phase-2a rows. The latest handover read was
`docs/journal/handover/2026-11-06-heartbeat-night.md`; it does not name this
change. Live PR state and other sessions were not read within this runner's
worktree-only boundary. The orchestrator owns tracker communication.

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

The live command depends on the orchestrator's eligible change and fresh
receipt; record its exact command when selected. A live endpoint failure is
unmet completion evidence, not permission to call a fixture run live success.

## Criterion ledger

- 1: not yet written tests/test_stage2_swarm.py::test_topic_report_preserves_bare_and_exact_fence — valid canonical reports change or fail
- 2: not yet written tests/test_stage2_swarm.py::test_topic_report_accepts_single_wrapped_object — prose or trailing tool residue still rejects valid JSON
- 3: not yet written tests/test_stage2_swarm.py::test_topic_report_refuses_ambiguous_or_malformed_objects — extraction chooses among competing objects or repairs invalid JSON
- 4: tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim — missing fields or too many claims pass
- 4: tests/test_stage2_research_report.py::test_report_duplicate_ids_and_extra_fields_are_refused — strict schema violations pass
- 4: tests/test_stage2_research_report.py::test_report_without_any_supported_claim_fails_except_empty_neighbours — unsupported reports pass the evidence floor
- 5: not yet written tests/test_stage2_swarm.py::test_topic_report_gets_one_same_seat_correction — absent, duplicate, substituted or non-format retries pass
- 6: not yet written tests/test_stage2_swarm.py::test_topic_correction_keeps_security_and_time_boundaries — correction escapes prompt, receipt, queue or original time boundaries
- 7: not yet written tests/test_stage2_swarm.py::test_topic_correction_persists_attempts_and_resumes_final_report — lost attempts, duplicate scoring or unvalidated reuse passes
- 8: not yet written tests/test_stage2_swarm.py::test_topic_corrections_account_for_every_invocation — hidden or excess correction calls pass
- 9: not yet written tests/test_stage2_swarm.py::test_wrapped_and_corrected_seats_complete_explore — a selected seat is dropped or remains failed after a valid correction
- 9: not a test — orchestrator records a real explore's commit, run identifier, selected seats and all accepted reports in findings.md; missing or incomplete live evidence leaves this criterion unverified

## Draft checks — 2026-11-09

On this draft over b9a87940: interview-minimums passed for this change;
research-handoff reported exemption because this change has no v2 swarm
evidence; criterion-ledger passed; `git diff --check` passed. These checks do
not close the open governance decision or verify implementation. The general
artifact validator is absent. The registry check was not run because its
tracker renderer can read outside the permitted worktree; index generation,
full `make verify`, commit and live completion evidence belong to the runner
or orchestrator. No implementation tests or live model calls ran in drafting.

## Draft retry checks — 2026-11-10

At baseline b9a87940, the retry brought the changed research, spec and plan
headers up to date; findings already carried today's `updated:`. No criterion,
class, maintainer answer or invocation policy changed. Interview-minimums,
criterion-ledger, frontmatter-current and `git diff --check` passed;
research-handoff explicitly reported the no-v2-evidence exemption. There are
no open phase-2a rows to incorporate. The unresolved decision still blocks
phase 4. The runner owns full verification and the commit; no implementation,
live calls, tracker writes or git mutations ran in this drafting attempt.

## Time used
