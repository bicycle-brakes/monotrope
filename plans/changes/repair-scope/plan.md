---
title: "Plan — repair-scope"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair]
---

# Plan — repair-scope

```text
For you:     Repair and implement workers leave handovers and governance files to the orchestrating session; the runner restores forbidden edits and names them.
Done when:   Both verbs restore every measured forbidden edit before verification, retain permitted work and runner evidence, and the ledger tests and make verify pass.
Appetite:    2 h of phase 4, repairs included; a stop, not an estimate.
Not now:     New sandbox guarantees, routing changes, draft scope changes or edits to repository governance.
Pre-mortem:  suppose it failed: most likely because restoring failed repair findings erases the record of restored paths.
Starts unless you say stop.
```

Implements [`spec.md`](spec.md), criteria 1–6, from `9943a25`. Class
`bounded`: no design document or ADR. Explore used Stage 2, route `flash`,
model `glm-5.3-flash`, on 2026-10-16; no Stage-1 fallback was recorded.

## Steps and files

1. **`scripts/stage2.py`** — add one shared worker-scope prompt sentence to
   `REPAIR_FORMAT`, `REPAIR_FORMAT_FILE_TOOLS` and `implementation_prompt`.
   Spell out the spec's denied areas, restoration before verification and the
   orchestrator's handover ownership; retain the repair-only ban on model
   edits to `findings.md`.
2. **`scripts/stage2.py`** — compute the keep set from `changed_paths` by
   excluding paths in the denied areas, using path-component boundaries and
   the current change's exact folder. Reuse `put_back(root, baseline, keep)`;
   keep `findings.md` for the existing answer checks. In `run_attempts`, run
   cleanup after the moved-HEAD guard, failed-call branch, credential scan
   and model-only file measurement, before `verify_attempt` (which prepares
   derived files and formats). Do not change those existing guards or the
   failed-process rollback. Repeat cleanup after every successful model call,
   including retries and fallback routes. A failed restore stops the call
   before verification or checkpoint.
3. **`scripts/stage2.py`** — retain each cleanup listing in memory until
   findings restoration, if any, has finished; append it on both the passing
   and failing paths before checkpoint, stop or retry. Use `quote_block` and
   `put_back_lines`, with a worker-specific heading naming attempt and route;
   pass the path lines as `quote_block`'s `whole` argument to avoid truncation. Include the scope
   listing in retry diagnostics without treating cleanup as a failed check.
4. **`tests/test_stage2.py`** — add the ledger's top-level tests using the
   existing `World` stand-ins. Parameterize both verbs and their supported
   routes; seed tracked forbidden files, then modify, delete, stage or add
   paths in each denied area. Observe the tree at verification and inspect
   checkpoint contents. Exercise three attempts with distinct stray paths,
   passing and failing outcomes, more than `ATTEMPT_FILES` paths and long or
   newline-containing names. Check allowed siblings such as
   `docs/journal-extra/` and a similarly prefixed change name. Assert retained
   code/test/doctrine edits, own `plan.md` time evidence, generated index,
   Stage-1 route evidence and runner-written fixed statuses. Existing tests
   for failed calls, credentials and moved HEAD remain regression coverage.
5. **`prompts/04-implement.md`** — make both handover references refer to
   the orchestrating session's handover and state the worker scope contract.
   **`docs/WORKFLOW.md`** — update §4's general repair-write paragraph and
   "Repairing taken findings" with the common scope, restore-and-record order
   and existing residual risks; keep draft's distinct ADR exception intact.
   Test these statements with planted contradictory wording. In
   `tests/test_stage2.py`, update only the old unrestricted-write expectation
   in `codex_repair_doctrine_problems` and its counterexample in
   `test_codex_repair_doctrine_and_endpoint_remarks_agree`; retain the tests'
   routing, read-confinement and residual-risk assertions.
6. **`plans/changes/repair-scope/plan.md`** — remove `not yet written` as
   each named test lands and record measured phase-4 time below. The runner
   stamps changed held files and refreshes **`plans/INDEX.md`** through
   `prepare_derived`; no manual index edit.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_work_prompts_forbid_denied_areas_and_assign_handovers_to_the_orchestrator — a route omits the scope sentence or a denied area
- 2: not yet written tests/test_stage2.py::test_work_attempts_restore_denied_paths_before_verification — a forbidden staged edit, deletion or new file reaches preparation, verify or checkpoint
- 3: not yet written tests/test_stage2.py::test_each_work_retry_restores_its_own_denied_paths — restoration runs only on the first or passing attempt
- 4: not yet written tests/test_stage2.py::test_work_scope_records_survive_passing_and_failed_attempts — restoring findings erases a cleanup record or misattributes its route
- 4: not yet written tests/test_stage2.py::test_work_scope_records_name_every_path_in_full — an over-limit, long or newline-containing path is truncated or omitted
- 5: not yet written tests/test_stage2.py::test_work_scope_keeps_permitted_changes_and_runner_writes — cleanup removes allowed changes, time or route evidence, derived files or fixed statuses
- 6: not yet written tests/test_stage2.py::test_worker_scope_doctrine_and_handover_ownership_agree — contradictory workflow or handover wording remains undetected

## Not touched

`AGENTS.md`, `decisions/**`, `docs/adr/**`, tracker and settings, journals,
other change folders, draft/explore paths, routing and sandbox configuration.
No test fixture rewrite, gate change or live model call is needed.

## Time used
