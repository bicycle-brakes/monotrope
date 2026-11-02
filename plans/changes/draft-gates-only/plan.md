---
title: "Plan — draft-gates-only"
status: draft
implementation_status: partial
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-77qj
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, verification]
---

# Plan — draft-gates-only

```text
For you:     Draft checks its documents with the existing document gates, freeing the full-suite slot sooner.
Done when:   Tests show draft uses the document subset with its safeguards, implement and repair still use the full suite, the workflow agrees, and make verify is green.
Appetite:    1 hour of phase 4, repairs included; stop at the limit.
Not now:     Gate membership, report formatting, new make targets or timeout changes.
Pre-mortem:  suppose it failed: most likely because draft tests still intercept make and never exercise the new document-check command.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: first add the ledger's new tests; give the draft
   fixture a document-check stand-in that records arguments and environment,
   returns scripted output and status, and contacts no model or real gates.
   Update all draft-chain scenarios and direct `verify_draft` callers that
   currently rely on the make stand-in; retain make for implement and repair.
   Demonstrate that the command-selection test fails against the old caller.
2. `scripts/stage2.py`: in `verify_draft` use the same command vector,
   `["bash", "scripts/verify_all.sh", "--job", "docs"]`, for admission and
   launch; retain preparation before admission, inherited environment and
   lock descriptors, `VERIFY_SECONDS`, gate-owned ADR tolerance, artifact
   checks and exit-code verdict. Name the actual command in its docstring,
   comments and failure diagnostics. Leave `verify_attempt` unchanged.
3. `docs/WORKFLOW.md`: update only the draft section's verification command
   and exit-code explanation; preserve its tolerance and five-step order,
   and state that implement and repair retain full verification.
4. `plans/changes/draft-gates-only/plan.md`: replace not-yet-written ledger
   markers as tests land and record phase-4 time under Time used.
   `plans/changes/draft-gates-only/findings.md`: carry test evidence and the
   later review rows. `plans/INDEX.md`: regenerate through
   `scripts/plans_registry.py`, never hand-edit; the runner owns its draft
   preparation and commit. No files are deleted and no held path is edited.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_ci.py
PYTHON=.venv/bin/python3 make verify
```

Use planted failures for nonzero exit, start failure, timeout and admission
refusal; assert retries and no passing commit. Observe admission at launch,
its inherited token/descriptors and execution timeout rather than sleeping
through a real timeout. Exercise the real subset selector with the existing
`tests/test_ci.py` tests; do not duplicate its gate list. In the workflow test,
plant the obsolete full-check wording and require it to fail.

## Criterion ledger

- 1: tests/test_stage2.py::test_draft_runs_the_existing_docs_subset — the launched command omits --job docs or a full-suite call appears.
- 1: tests/test_ci.py::test_the_docs_subset_holds_the_document_gates_and_no_code_gate — a code gate enters the selected subset or a document gate disappears.
- 2: tests/test_stage2.py::test_draft_docs_check_keeps_admission_and_execution_limit — launch precedes admission, lacks inherited ownership or uses a timeout other than VERIFY_SECONDS.
- 3: tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt — a nonzero exit, start error, timeout or admission refusal bypasses retries or yields a passing commit, or diagnostics name make verify.
- 4: tests/test_stage2.py::test_only_the_changes_own_missing_adr_answer_is_tolerated — the docs command loses the scoped environment or another blocking failure is tolerated.
- 5: tests/test_stage2.py::test_draft_docs_checks_preserve_preparation_and_artifact_guards — preparation runs late or a missing spec, plan, card, Time used heading or excess ADR is accepted.
- 6: tests/test_stage2.py::test_implement_and_repair_keep_full_verify_after_docs_draft — either implementation route launches document-only verification.
- 7: tests/test_stage2.py::test_the_workflow_names_the_draft_document_check — the draft section names make verify as its check or treats parsed output as the verdict.

## Boundaries and route

Do not touch `Makefile`, `scripts/verify_all.sh`, `scripts/ci_gates.py`,
`decisions/gates.yaml`, `.github/`, prompts, templates, ADRs or endpoint and
harness configuration. The report-header asymmetry remains separate work.
No design or ADR is due for this bounded change. Explore ran through Stage 2
on 2026-10-31, route flash, model `glm-5.3-flash`; no Stage-1 fallback is
recorded. The shared execution limit remains unchanged.

## Runner route — 2026-10-31

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-31 09:36:16–10:23:28 UTC, 2832 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-31 10:23:34–10:45:22 UTC, 1308 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-31 10:45:28–10:57:58 UTC, 750 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner

Overrun, owned by the orchestrator (review row L2-1): the three attempts together took 4890 s, past the one-hour stop. Under the appetite rule merged that morning (`docs/WORKFLOW.md`, PR #292) the appetite extends once by itself up to twice its size; the change ran under that extension, ending implement at 81.5 of 120 minutes, and no further extension was taken.
