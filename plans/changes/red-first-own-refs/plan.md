---
title: "Plan — red-first-own-refs"
status: draft
implementation_status: partial
date: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-wkxm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, red-first]
---

# Plan — red-first-own-refs

```text
For you:     Parallel Git activity no longer voids repair proofs; each proof still refuses changes to any of its own references.
Done when:   Both proofs tolerate foreign reference changes, detect and name their own changes, clean up their private repositories, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Reference exclusions, retry policy, dependency provisioning, the neighbouring test guard, or a sandbox for arbitrary external writes.
Pre-mortem:  suppose it failed: most likely because the fixed-code clone tested committed HEAD instead of the uncommitted repair.
Starts unless you say stop.
```

## Scope and baseline

Implements criteria 1–9 of `spec.md` (bead `coding-harness-wkxm` — isolate
repair proofs from concurrent reference movement). At `36c74d03` on
2026-11-01 the class is `bounded`; no design phase or ADR is due.
`findings.md` has one draft-call record and no phase-2a rows. Explore used
Stage 2, route `flash`, model `glm-5.3-flash`; no Stage-1 fallback is recorded.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
this baseline: use the phase-3 prompt's form and report that validator as
unavailable, never green.

## Build sequence

1. In `tests/test_stage2.py`, add the not-yet-written ledger tests below,
   parameterized over baseline and fixed-code proofs where applicable. Use
   real temporary repositories and the existing `World`, `repair_world` and
   planted-test helpers. A runner-side hook around the actual pytest launch
   changes source refs while the selected test executes; assert the valid
   proof succeeds and the foreign refs retain their new state. Cover branch,
   remote-tracking and `refs/stage2/attempts/` creation, deletion and movement.
   Establish red isolation cases against the pre-fix runner.
2. In `scripts/stage2.py`, introduce one private-repository lifecycle shared
   by `red_first` and `fixed_test_proof`. Create a local scratch clone with
   its own `.git`, copied objects and refs, no hardlinks or object alternates,
   and no dependency on the source worktree registry. Preserve the source's
   initial named refs in the clone so the existing moved-branch fixture
   remains a move, not an accidental creation. Detach its checkout at the
   requested commit; leave source refs and index untouched. Remove the
   clone's source remote configuration before running tests so ordinary Git
   operations cannot push back to the source. All setup is local, bounded by
   existing Git timeouts, and failures become scrubbed proof refusals.
3. For baseline proof, check out the supplied baseline and replace `tests/`
   with the attempt's tests as today, excluding caches. For fixed proof,
   capture `worktree_tree(root)` with its temporary index before cloning;
   materialize that exact tree in the private checkout: tracked files as
   present on disk rather than stale staged bytes, deletions, untracked
   nonignored files, file modes and symlinks. Local object copying must carry that
   unreferenced tree too; refuse if it cannot be read. Do not use an archive
   that can silently omit `export-ignore` files, commit in the source, create
   a transport ref there, or copy `.git`/ignored dependencies as work files.
4. Run pytest from the private checkout using the source's checked interpreter
   and current `tool_problem` protection. Keep the baseline import precheck,
   selector, runner-owned probe/report, fresh token, outcome classifier,
   admission lock and `RED_FIRST_MINUTES` limits. Keep the fixed probe outside
   the tested tree and its all-pass rule; filter PATH against both source and
   scratch roots through the existing environment helpers. Snapshot all
   private refs immediately before execution and compare names and targets
   in `finally`, before deleting the store, including on launch failure or
   timeout. Name every differing ref in both paths' scrubbed diagnostics.
   Measure the fixed checkout's file tree before/after too; reject writes.
5. Clean up the private checkout, store and probe directory on every exit.
   Report cleanup failure as refusal; never prune the source registry,
   restore a source ref or compare shared refs as an acceptance condition.
   Adapt the existing created/moved-ref tests to inspect private refs before
   disposal and prove source refs survive. Keep every existing top-level test
   name, including the failed-worktree-removal regression: retarget its
   injected failure to private-directory removal and retain its purpose of
   naming cleanup failure without a dead registry entry. Update comments and
   docstrings to describe the new boundary, not weakened reference checks.
6. Add the dated predecessor clarification, run verification below, record
   red/green evidence and phase-4 time, and clear each `not yet written`
   marker only when its top-level test is defined. Coordinate the shared
   `scripts/stage2.py` proof functions with the neighbouring test-guard work
   before integration; retain its changes if present.

## Files and limits

- `scripts/stage2.py` — add the shared private-repository helper and update the two proof paths, comparisons, cleanup and directly related diagnostics/docstrings.
- `tests/test_stage2.py` — add ledger regressions and adapt existing proof, cleanup and launch fixtures without renaming their top-level tests.
- `plans/changes/red-first-install/spec.md` — append one dated amendment note linking this change's preservation of criterion 8; leave its criteria unchanged.
- `plans/changes/red-first-own-refs/spec.md` — update implementation status, retaining the criteria.
- `plans/changes/red-first-own-refs/plan.md` — update status, ledger markers and phase-4 time.
- `plans/changes/red-first-own-refs/findings.md` — runner-owned attempt and verification evidence, preserving earlier entries.
- `plans/INDEX.md` — runner/orchestrator regenerates after header changes; the implement attempt does not hand-edit it.

No deletions or held-path edits. Leave `decisions.md`, other change folders,
`save_attempt`, `checkpoint`, routing, pytest classification, dependency
installation, `prompts/04-implement.md`, `docs/WORKFLOW.md`, `templates/`,
`docs/adr/`, `decisions/`, `provenance.yaml`, `model-endpoints.yaml`,
`AGENTS.md`, `README.md` and agent configuration untouched. Isolation covers
ordinary Git commands in the scratch cwd; explicit access to external paths
is the spec's documented boundary, not an ownership detector to implement.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'proof or red_first or ref_created_while or existing_ref_moved or failed_worktree_remove'
python3 scripts/check_interview_minimums.py --change red-first-own-refs
python3 scripts/check_criterion_ledger.py
make verify
```

`make verify` is the implementation gate; the runner owns it and the
checkpoint. For this draft, measure the interview and ledger gates only;
the missing artifact validator cannot be executed. Do not substitute a
partial check for a full green implementation verdict.

## Criterion ledger

- 1: tests/test_stage2.py::test_proofs_ignore_foreign_ref_changes — a valid proof fails after concurrent source branch, remote or attempt-ref movement
- 2: tests/test_stage2.py::test_proofs_refuse_private_ref_changes — either proof accepts a created, deleted or retargeted private ref in any tested namespace
- 2: tests/test_stage2.py::test_a_ref_created_while_the_named_test_ran_fails_the_proof_and_is_never_deleted — a private branch creation passes or a source branch is deleted
- 2: tests/test_stage2.py::test_an_existing_ref_moved_while_the_named_test_ran_fails_the_proof — a private existing branch's new target goes undetected
- 3: tests/test_stage2.py::test_proofs_name_all_changed_refs — either diagnostic omits a changed ref or selector, or fails credential scrubbing
- 4: tests/test_stage2.py::test_baseline_proof_uses_baseline_code_and_current_tests — fixed production bytes reach baseline proof or current tests do not
- 5: tests/test_stage2.py::test_fixed_proof_uses_current_file_tree — fixed proof loses uncommitted files, deletions, modes, symlinks or export-ignored files
- 6: tests/test_stage2.py::test_proofs_leave_source_state_untouched — private Git writes or cleanup change source bytes, index or refs
- 7: tests/test_stage2.py::test_proofs_refuse_unmeasured_state — setup, before/after ref reads or tree measurement fail yet a proof succeeds
- 7: tests/test_stage2.py::test_fixed_proof_refuses_tree_changes — the fixed test modifies a Git-visible file yet receives passing evidence
- 7: tests/test_stage2.py::test_a_failed_worktree_remove_leaves_no_dead_entry_and_is_named — adapted private cleanup failure is ignored or leaves a source registry entry
- 8: tests/test_stage2.py::test_proofs_remove_private_repositories_on_all_exits — success, refusal, partial setup or timeout leaves scratch files or a worktree entry
- 8: tests/test_stage2.py::test_the_red_first_run_leaves_no_worktree_behind — repair leaves a temporary checkout or source registry entry
- 9: tests/test_stage2.py::test_red_first_accepts_only_clean_assertion_runs — qualifying baseline evidence is refused
- 9: tests/test_stage2.py::test_red_first_accepts_pytest_failed_call_outcomes — pytest's qualifying call failure is refused
- 9: tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors — fixture failure certifies a repair
- 9: tests/test_stage2.py::test_red_first_refuses_missing_or_invalid_evidence — unbound or malformed evidence is accepted
- 9: tests/test_stage2.py::test_red_first_refuses_a_timed_out_run — timeout certifies red first
- 9: tests/test_stage2.py::test_red_first_refuses_a_changed_venv — modified interpreter executes
- 9: tests/test_stage2.py::test_fixed_code_proof_keeps_pytest_failed_red — nonpassing fixed cases receive proof
- 9: tests/test_stage2.py::test_isolated_proofs_keep_execution_limits — either private pytest launch drops admission, environment scrubbing or the existing timeout

## Runner route — 2026-11-01

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-01 07:55:19–09:29:44 UTC, 5665 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-01 09:29:53–10:09:58 UTC, 2405 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-01 10:10:05–10:24:47 UTC, 883 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-01 16:17:12–16:39:07 UTC, 1316 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Implementation accepted by hand — 2026-11-01

The implement runner rejected three attempts; the third failed only on
`test_no_git_launch_in_the_runner_names_a_bare_git` (`assert 7 >= 8`): the
change removed one bare `git` launch, which is the change's purpose. The
orchestrating session accepted the third attempt's saved work and lowered
that guard's floor from 8 to 7 with a comment naming the removed launch
(commit 5581e35a); no fourth attempt ran. Full `make verify` was green on
that commit (2026-11-01). Review row L1-8 asked for this record.
