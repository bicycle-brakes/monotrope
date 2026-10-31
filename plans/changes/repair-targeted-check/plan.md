---
title: "Plan — repair-targeted-check"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-gxwg
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, repair, verification]
---

# Plan — repair-targeted-check

```text
For you:     Runner repairs use targeted checks; phase 6 still requires a fresh full check.
Done when:   Selection, failure and phase-6 boundary regressions pass and make verify is green.
Appetite:    Three hours of phase 4 including repairs; stop at the limit.
Not now:     New gates, reduced CI, automated hand repairs or changed model routes.
Pre-mortem:  suppose it failed: most likely because an uncommitted dependency is missed by test selection.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–11 of `spec.md` and preserve the bounded class and the
recorded interview skip. No design or ADR is due. Explore used route
`flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`, on 2026-10-31;
no Stage-1 fallback was recorded. The orchestrator shows this card unchanged;
this draft does not implement, commit or launch another model.

## Build sequence

1. In `scripts/touch_map.py`, expose a working-tree snapshot adapter for the
   existing `links()` rules, factoring only shared inventory indexing from
   `Snapshot` as needed. Inventory tracked and nonignored untracked paths;
   read regular files from disk, never follow aliases outside the worktree,
   and report unreadable/unsafe inputs rather than claiming zero links.
   Preserve the committed-only CLI and all its output. In `scripts/stage2.py`,
   take touched paths from `changed_paths(..., against=baseline)` across disk
   and index. Union current and baseline test links for touched endpoints,
   retain only surviving runnable tests, include touched test files, and
   deduplicate/sort. Baseline links cover deleted and renamed-away code;
   current links include uncommitted and untracked tests. Keep the entire
   repair delta on retries, not just the most recent model's writes.
2. Add an explicit post-run mode to `run_attempts`/`verify_attempt`, defaulting
   to full; only `repair()` requests targeted mode on every route. Preserve
   tool checks, findings restoration and plan-path validation before any
   repository command. Share formatting, ledger-marker clearing, stamp/index
   preparation, intent-to-add cleanup and time-heading validation. Perform
   targeted formatting/checks/preparation outside admission; keep the current
   admitted order for full mode. Select after formatting and derived refresh
   so generated files enter the applicable gate set. Preserve cheap checks'
   accepted-ledger and previous-failure targets in addition to whole-file
   touched/linked tests. Do not change fixed-answer validation, admitted
   red-first proofs, recovery, retry budgets or the checkpoint guard.
3. Resolve targeted gates through validated `ci_gates.gates()` with local
   placement and existing enforcement; copy no shell commands. Use this
   conservative applicability table, unioning rows and deduplicating IDs:

   | Touched input | Required coverage |
   | --- | --- |
   | Runner plan/findings/index or other Markdown under `plans/` or `docs/` | All locally runnable gates with `subsets: [docs]` |
   | Supported Python production or test files | Whole-file tests and ruff lint/format on touched surviving Python files, plus the document row for derived metadata |
   | A gate's command entrypoint | That gate as well as the preceding rows |
   | Added, removed or renamed files | `leerprobe` as well as the preceding rows |
   | `scripts/ci_gates.py` or `scripts/verify_all.sh` | `gate-schema`, `ci-drift` and full fallback for shared execution infrastructure |
   | `prompts/`, shared test configuration, root/build/dependency/governance configuration, unsupported file kinds, production code without linked tests, or unsafe/incomplete inventory | Full `make verify`, with a stated fallback reason |

   Treat a schema/selection error as unmeasured; require a successful full
   fallback or reject. A selected gate with no local equivalent is reported
   according to the existing local runner's semantics. Use the locked
   interpreter, explicit test argv and existing bounded `launch`/diagnostic
   helpers; never allow an empty pytest selection to discover the full suite.
   Preserve gate order, repository-root execution and the locked interpreter's
   `PYTHON`/`PATH` setup from `verify_all.sh`; honor tracker/history needs
   rather than treating unavailable prerequisites as a measured green.
   Preserve blocking versus report/advisory behavior. Fallback uses existing
   admitted full verification; it does not add an extra targeted verdict.
4. Feed the mode, selected test files/gate IDs, fallback reason when applicable
   and outcome back to `run_attempts`. Persist protected runner-owned evidence
   in this attempt's findings block and checkpoint message on success, and
   through existing bounded diagnostics on failure. Use neutral post-run
   wording in errors shared by both modes. A required command's red result,
   launch error or timeout reaches existing retry handling without fixed
   statuses or checkpoint. Do not label targeted success full green.
5. In `review()`, after current input/row preflight and before `begin_call`,
   require a current committed substantive tree (permit existing runner audit
   changes in this change's `findings.md`) and run full `make verify` under
   `verify_lock.hold_admission`, preserving environment inheritance, limits
   and descriptor handling. Capture the head and substantive tree before and
   after the check; refuse a changed head/tree or red/unstartable/timed-out
   check before any reviewer call or loop-row release. Do this on every
   phase-6 invocation, including re-checks. Do not create a receipt, reuse a
   targeted result, auto-format review inputs or start repairs from review.
6. Add the ledger regressions using real fixture repositories and captured
   local commands, with the existing `World`, `repair_world` and
   `script_repair` fixtures. Fake model responses and full-check subprocesses;
   do not fake away path selection. Parameterize staged-only, untracked,
   deletion, rename, retry, enforcement, timeout and launch-error cases.
   Keep existing repair/review tests meaningful after the new boundary;
   update their expected full-check counts and required fixture files.
7. Orchestrator bootstrap edits, after the accepted attempt: align the held
   prompts and instruction table, then the workflow's runner-repair exception.
   Preserve full verification before a pull request leaves draft and CI's
   full gate. In `tests/test_stage2.py`, align `phase_table_problems()` and
   `test_the_phase_table_has_the_review_loop()` with the new rule, including
   planted omissions of targeted repair checks and full verification before
   phase 6. These doctrine assertions belong to the orchestrator's bootstrap
   step so the attempt can pass against the still-unchanged held instructions.
   Run them and full verification after those edits and before phase 6.
   The attempt must not edit held paths.

## Files and ownership

- Attempt: `scripts/stage2.py` — select and run targeted repair checks, enforce full phase-6 verification, and align embedded repair instructions and evidence.
- Attempt: `scripts/touch_map.py` — add the working-tree adapter while preserving the committed-object CLI.
- Attempt, then orchestrator: `tests/test_stage2.py` — the attempt covers repair behavior and review ordering; the orchestrator aligns doctrine assertions after the held edits.
- Attempt: `tests/test_touch_map.py` — cover working-tree links and preserve committed-only output.
- Attempt: `docs/WORKFLOW.md` — describe the repair-only exception to full post-run verification and the enforced phase-6 check; orchestrator may finish the wording alongside held edits.
- Attempt: `plans/changes/repair-targeted-check/spec.md` — update implementation metadata without changing criteria.
- Attempt: `plans/changes/repair-targeted-check/plan.md` — clear written-test markers and record measured phase-4 time.
- Runner: `plans/changes/repair-targeted-check/findings.md` — preserve audit ownership; append protected attempt evidence and later review findings.
- Runner: `plans/INDEX.md` — regenerate through the existing derived preparation.
- Orchestrator only: `AGENTS.md` — align the phase-4b table and runner-repair summary.
- Orchestrator only: `prompts/04-implement.md` — replace unconditional runner-full-check wording for the repair path while retaining implement's full check.
- Orchestrator only: `prompts/04b-review-loop.md` — align repair-cycle instructions and the full check before phase 6.

No deletions or new modules are planned. Do not touch gate definitions,
generated CI, machine-admission internals, other changes' specs/ledgers,
living implementation-verification spec, ADRs, tracker data, model endpoints,
other held paths or permissions. The existing fail-fast contract's full-check
rule remains for implement; the current change explicitly narrows repair.

## Verification

The implementation worktree needs `make venv` and
`bash tools/pi/install.sh` once before full verification. Run verbatim:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_touch_map.py tests/test_verify_lock.py tests/test_ci.py -q
.venv/bin/python3 -m ruff check scripts/stage2.py scripts/touch_map.py tests/test_stage2.py tests/test_touch_map.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py scripts/touch_map.py tests/test_stage2.py tests/test_touch_map.py
python3 scripts/check_interview_minimums.py --change repair-targeted-check
python3 scripts/check_criterion_ledger.py
make verify
```

The runner also checks the plan registry after its derived index refresh.
The requested `scripts/validate_change_artefacts.py` and a plan template do
not exist at baseline `9eae5d26`; do not create them here. The draft uses
the spec template and phase-3 plan form. The runner owns full verification
and the commit; this drafting call reads only the worktree and git directory.
The preceding draft's process-cancellation failure remains in `findings.md`;
it does not authorize unrelated test repairs or a weaker verification command.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_covered_repair_uses_targeted_verification — a narrow covered repair still calls make verify
- 2: not yet written tests/test_stage2.py::test_targeted_repair_runs_whole_touched_and_linked_test_files — an unchanged failing sibling, indexed/untracked touch or retained retry edit is omitted
- 2: not yet written tests/test_touch_map.py::test_worktree_links_include_new_content_and_preserve_committed_snapshot — current uncommitted links are missed or committed CLI output starts reading disk
- 2: not yet written tests/test_stage2.py::test_targeted_repair_keeps_baseline_links_for_removed_paths — deleting or renaming code loses its surviving tests
- 3: not yet written tests/test_stage2.py::test_targeted_repair_checks_touched_python_after_formatting — ruff misses a surviving touched file or runs before formatting
- 4: not yet written tests/test_stage2.py::test_targeted_repair_selects_declared_gates_and_enforcement — derived document gates or a changed gate is missed, commands are copied, or blocking enforcement is lost
- 5: not yet written tests/test_stage2.py::test_targeted_repair_falls_back_to_full_on_uncovered_inputs — a prompt, unknown kind, unsafe inventory or uncovered code receives targeted acceptance
- 6: not yet written tests/test_stage2.py::test_targeted_commands_run_without_verify_admission — targeted commands acquire or inherit admission while full fallback fails to acquire it
- 7: not yet written tests/test_stage2.py::test_targeted_failure_never_checkpoints_or_marks_fixed — red, launch failure or timeout reaches a checkpoint or fixed row instead of protected retry diagnostics
- 8: not yet written tests/test_stage2.py::test_targeted_repair_preserves_preparation_and_answer_proofs — targeted green bypasses derived refresh, accepted/retry test targets, fixed-line validation or red-first proof
- 9: not yet written tests/test_stage2.py::test_review_requires_fresh_full_verification_before_model_call — first review or re-check starts on stale/targeted green, a moved head/tree or failed full check
- 10: not yet written tests/test_stage2.py::test_targeted_mode_is_repair_only — implement or draft inherits repair's reduced scope or loses admission
- 11: not yet written tests/test_stage2.py::test_repair_records_verification_scope_and_outcome — success lacks scope evidence, fallback lacks a reason or targeted output claims full green

## Time used
