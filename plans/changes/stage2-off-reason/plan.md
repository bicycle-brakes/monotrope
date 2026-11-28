---
title: "Plan — stage2-off-reason"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-73gi.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2]
---

# Plan — stage2-off-reason

```text
For you:     Turning off Stage 2 requires an explicit reason in the command.
Done when:   Parser, recording, process-report and instruction checks pass and make verify is green.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Changing fallback models or rewriting historical records.
Pre-mortem:  suppose it failed: most likely because a reason that matches a change name is mistaken for the change.
Starts unless you say stop.
```

## Build sequence and files

1. In `scripts/stage2.py`, remove the optional-value `nargs` and `const`, remove the consumed-change guard, and update the module and help text; keep the supported-verb check and existing route and record writers. A missing positional change must still refuse before a model call.
2. In `scripts/run_report.py`, consume the mandatory flag value regardless of whether it matches a known change, including the `--stage2-off=REASON` form; retain positional change detection and other option handling.
3. In `tests/test_stage2.py`, replace the obsolete guard test, give unsupported-verb cases a reason, and test both argument orders, missing values, a reason equal to a change, preserved routing and records. Update current-instruction assertions. In `tests/test_run_report.py`, replace the optional-value expectations with mandatory-value cases in both forms and orders, including a reason equal to a known change.
4. In `docs/WORKFLOW.md`, update current fallback syntax and the bare next-step example. After the accepted attempt, the orchestrator updates held paths `prompts/01-explore.md`, `prompts/04-implement.md`, and `AGENTS.md` to require a reason; the implementation attempt must not edit those paths.
5. The runner updates `plans/changes/stage2-off-reason/findings.md`, `plans/changes/stage2-off-reason/plan.md` (ledger and time), and `plans/INDEX.md` as needed. No files are deleted; no design or ADR is due for a bounded change.

Leave `docs/adr/0015-glm-5-3-repairs-taken-findings.md`, `docs/adr/0017-codex-repairs-taken-findings.md`, archived changes, handovers, `scripts/stage2_session.py` and fallback routing unchanged.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_run_report.py
python3 scripts/jobs.py start -- make verify
```

Inspect the detached verification job's exit before phase 6.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_stage2_off_requires_a_value — a bare flag starts a model or exits successfully.
- 2: not yet written tests/test_stage2.py::test_stage2_off_required_reason_preserves_routes — a supported verb loses its reason or selects a different route.
- 3: not yet written tests/test_stage2.py::test_stage2_off_reason_remains_in_call_record — the existing phase artefact loses or moves the reason.
- 4: not yet written tests/test_stage2.py::test_stage2_off_reason_without_change_refuses — a call starts without a positional change.
- 5: tests/test_stage2.py::test_stage2_off_is_only_for_work_verbs — an unsupported verb with a reason starts a call or exits other than 2.
- 6: not yet written tests/test_run_report.py::test_stage2_off_required_reason_preserves_change — a reason matching a known change is reported as the positional change.
- 7: not yet written tests/test_stage2.py::test_stage2_off_current_instructions_require_reason — a current invocation presents the reason as optional.

## Explore fallback

On 2026-11-28 explore used the Stage-1 route, `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (`research.md`).

## Time used

2026-11-28 14:14:51–14:16:59 UTC, 128 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
