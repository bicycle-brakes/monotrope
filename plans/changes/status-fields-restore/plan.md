---
title: "Plan — status-fields-restore"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-ljmi
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, runner, repair]
---

# Plan — status-fields-restore

```text
For you:     Automated repairs preserve the approval and implementation states of spec, design and plan, and report that protection.
Done when:   Regression tests prove restoration on passing and failing attempts, prompts assign status changes to hand repair, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; stop at the limit.
Not now:     Automatic lifecycle transitions, review-table status changes or protection of other metadata.
Pre-mortem:  suppose it failed: most likely because an early failure exit bypassed restoration.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: add the ledger tests using the existing repair
   fixtures and scripted models, with distinct valid states for spec, design
   and plan; assert the verifier's observed bytes and the committed result.
2. `scripts/stage2.py`: snapshot the two top-level frontmatter fields of
   existing spec, design and plan immediately before each repair call;
   restore just those fields before verification and at failed-attempt
   exits, and append a runner-owned per-attempt restoration report.
3. `docs/WORKFLOW.md`: document lifecycle protection in "Repairing taken
   findings" and direct status-changing findings to orchestrator hand repair,
   with the existing row-booking and index-refresh follow-ups.
4. **Orchestrator bootstrap edit, after the accepted attempt:**
   `prompts/04b-review-loop.md` is held (`prompts/`); add the same hand-repair
   exception before the instruction to pass taken rows to the model. The
   implementation attempt must not edit this file. Finish its doctrine test
   and rerun the targeted checks after this edit, before the final verify.
5. `plans/changes/status-fields-restore/plan.md`: the runner fills `Time used`
   from measured attempts and clears ledger markers as tests are added.
   `plans/changes/status-fields-restore/findings.md`: the runner records
   attempt evidence; the orchestrator records review dispositions.
   `plans/INDEX.md`: the runner or orchestrator regenerates it through
   `python3 scripts/plans_registry.py --index` after artifact/header changes.

## Implementation constraints

Keep this extension repair-only in the shared `run_attempts` loop. Capture
each document's field lines separately; avoid serializing the whole YAML
header, which would alter unrelated metadata and formatting. Restore edited
or removed protected keys inside the initial frontmatter, never body text.
Use the existing snapshotted-input recovery for a deleted document or an
unreadable/missing header; reject that structurally broken attempt rather
than accept invented surrounding content. Do not create an absent optional
design or invent baseline values for a document newly created by the model.

Preserve the evidence and changed-file measurement before restoration, then
restore before `verify_attempt` and derived-index rendering. Use the same
per-attempt snapshot on retries and early exits: failed transport, answer
evidence persistence, HEAD checks, verifier/answer failures, exhausted routes
and checkpoint rollback. Cover Codex, its fresh retry, Sonnet fallback and
explicit Stage-1 repair. No new foreign call or route is introduced.

Preflight the complete recovery batch before its first write, reusing
`preflight_recovery`, alias baselines and `restore_work_input` as appropriate;
never follow an unsafe destination or write after `RestorationRefused`.
Keep the original failure and no-history-rewrite behavior. Report actual
restorations by document and field, or unchanged; on a no-write refusal use
the terminal diagnostic, without claiming restoration succeeded. Preserve
runner time entries, row marking and the accepted repair's other legal edits.

Both repair prompt routes receive the restoration sentence through their
shared instructions. The manual finding-selection rule is documentation,
not a new prose classifier. The doctrine test can cover the runner sentence
and workflow first; its assertion on the held prompt is added by the
orchestrator with step 4, so the accepted model attempt can verify green.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'repair_lifecycle or repair_status_changes_are_hand_repairs'
.venv/bin/python3 -m ruff check scripts/stage2.py tests/test_stage2.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py tests/test_stage2.py
PYTHON=.venv/bin/python3 make verify
```

The orchestrator runs the final command after the held prompt edit. Use
temporary fixture repositories, not live model calls, for every regression.
No Explore fallback was recorded: phase 1 used Stage 2, GLM 5.3 Flash,
endpoint `glm-coding-plan`, on 2026-11-06.

## Criterion ledger

- 1: tests/test_stage2.py::test_repair_lifecycle_fields_are_restored_before_verification — distinct values or removed keys reach the verifier or checkpoint.
- 2: tests/test_stage2.py::test_repair_lifecycle_fields_survive_failed_attempts — a parameterized early exit, retry or exhaustion leaves changed fields.
- 2: tests/test_stage2.py::test_repair_lifecycle_early_failure_reports_restoration — failed calls and evidence-save failures leave changed fields or omit the restoration report.
- 2: tests/test_stage2.py::test_repair_lifecycle_checkpoint_rollback_reports_restoration — a refused checkpoint leaves changed fields or drops its restoration report.
- 1: tests/test_stage2.py::test_repair_lifecycle_snapshot_refuses_unusable_documents — unreadable protected documents or missing frontmatter are silently omitted from the baseline.
- 2: tests/test_stage2.py::test_repair_lifecycle_recovery_keeps_safety_refusals — an unsafe destination is written or moved HEAD is reset.
- 3: tests/test_stage2.py::test_repair_lifecycle_restoration_preserves_other_edits — valid body/header edits or runner time disappear, or a field edit alone rejects the repair.
- 4: tests/test_stage2.py::test_repair_lifecycle_protection_allows_no_design — absent optional design is created or the repair is refused.
- 5: tests/test_stage2.py::test_repair_lifecycle_early_failure_reports_restoration — failed calls or evidence-save failures omit the restoration report.
- 5: tests/test_stage2.py::test_repair_lifecycle_checkpoint_rollback_reports_restoration — a refused checkpoint drops its restoration report.
- 5: tests/test_stage2.py::test_repair_lifecycle_report_describes_each_attempt — accepted, rejected or unchanged attempts lack an accurate report, including safety refusal diagnostics.
- 6: tests/test_stage2.py::test_repair_lifecycle_prompts_name_the_protected_fields — either route omits the keys, documents or restoration sentence.
- 7: tests/test_stage2.py::test_repair_status_changes_are_hand_repairs — workflow or orchestrator instructions omit the exception to automated repair.

## Not touched

No changes to other change folders, review-table vocabularies, registry
rules, tracker data, model endpoints, ADRs or recovery safety contracts.
No standalone design: the class is bounded. The orchestrator owns the one
held prompt edit; all other held paths remain outside the implementation.

## Time used

2026-11-06 00:58:03–02:34:23 UTC, 5779 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 02:34:40–04:14:38 UTC, 5998 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-11-07 01:50:33–05:22:57 UTC, 12743 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-07 08:28:14–11:26:24 UTC, 10689 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
