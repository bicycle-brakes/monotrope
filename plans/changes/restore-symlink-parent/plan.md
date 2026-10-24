---
title: "Plan — restore-symlink-parent"
status: draft
implementation_status: partial
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-10w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, restore, symlink]
---

# Plan — restore-symlink-parent

```text
For you:     A restore through an external parent link stops the run and names the path, leaving the recovery unwritten.
Done when:   Unsafe recovery leaves its batch untouched, no fallback or checkpoint follows, safe recovery still works, and make verify is green.
Appetite:    5 hours of phase 4, repairs included; a stop, not an estimate (maintainer raised it from 2, 2026-10-24).
Not now:     Routing changes, OS-level isolation, concurrent filesystem races or other runner verbs.
Pre-mortem:  suppose it failed: most likely because a time-finalization handler writes after the safety refusal.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2.py`: preflight restoration parents and propagate a
   terminal safety refusal across input recovery, baseline cleanup and time logging.
2. Change `tests/test_stage2.py`: add the regressions below and update the
   existing external-parent recovery expectations to the decided refusal.
3. Update `plans/changes/restore-symlink-parent/plan.md`: replace pending ledger
   entries as tests land; the runner records phase-4 time below, maintains
   `plans/changes/restore-symlink-parent/findings.md` and regenerates `plans/INDEX.md`.
   No implementation file is created or deleted.

## Implementation contract

- Add a dedicated `Refused` subtype for restoration safety: exit 2, except
  that a propagating model-call failure keeps its own exit code.
  Its message names the worktree-relative destination and whether a parent
  escapes the worktree or cannot be resolved. Compare resolved parent chains
  against the canonical root using path containment, never string prefixes.
  Inspect every existing ancestor, including relative, dangling and nested
  links; missing ordinary parents remain recoverable. Do not follow the leaf
  merely to decide parent containment; retain safe leaf/hard-link detachment.
- Preflight every batch before its first mutation. Apply the guard inside
  `restore_work_input` for direct callers, and to the complete input/findings
  batch in `run_attempts` before recovery, diagnostic or retry-time writes.
  Include non-plan inputs: a safe plan must not be logged before discovering
  an unsafe prompt parent. Recheck at each recovery boundary.
- In `restore_baseline`, validate tracked rollback destinations and newly
  created ignored cleanup paths before `git restore`, `git clean`, `unlink`,
  `rmtree` or parent removal. Guard the failed-call recovery branch before
  restoring findings or saving the failed attempt; preserve ordinary safe
  rollback and saved-attempt behavior.
- Let the dedicated refusal bypass the broad handlers in `persist_time_entry`
  and the completed-attempt exception finalizer. Check parent safety before
  any direct time write too. Do not wrap it as `CallFailed`, append findings,
  stamp files, save evidence, clean up or retry after it; report on stderr.
  A safety refusal is the explicit exception to ordinary time persistence.
- Use `World`, `repair_world`, scripted providers and monkeypatched boundaries;
  parameterize implement/repair, retry/final recovery, failed calls and early
  post-call refusals. Cover absolute/relative, intermediate, missing-target
  and sibling-prefix external parents, plus loops and resolution errors.
  Compare external sentinels, alias text, safe preceding inputs, findings,
  time records and HEAD with the pre-recovery state; spy on mutators to catch
  same-byte writes. Assert refusal exit, path/reason, one model invocation
  and no checkpoint or follow-up mutation.
- Update `test_runner_retry_replaces_parent_alias_without_following` and only
  the `parent-alias` expectation in
  `test_runner_early_refusal_recovers_time_destination_safely`; retain their
  names for existing ledgers. Keep the safe recovery controls below, including
  deleted parents and non-UTF-8 inputs. Keep prior change artifacts unchanged.
- Do not touch prompts, templates, workflow, ADRs, tracker, model declarations,
  unrelated runner verbs or credential handling for safe recovery paths.

## Criterion ledger

- 1: tests/test_stage2.py::test_restore_work_input_refuses_external_parent_without_writes — recovery removes the parent alias or alters an external sentinel
- 1: tests/test_stage2.py::test_runner_restore_preflights_all_destinations — a safe earlier input or plan is written before an unsafe later input is checked
- 1: tests/test_stage2.py::test_restore_baseline_refuses_external_parents_before_mutation — Git rollback or ignored cleanup mutates before checking every target
- 2: tests/test_stage2.py::test_runner_parent_escape_stops_without_fallback — another model, ordinary failure exit or checkpoint follows the unsafe recovery
- 3: tests/test_stage2.py::test_runner_parent_escape_stops_without_fallback — stderr omits the destination or outside-parent refusal reason
- 4: tests/test_stage2.py::test_restore_parent_resolution_failure_stops_without_writes — a loop or resolution error permits mutation, fallback or an unnamed traceback
- 5: tests/test_stage2.py::test_runner_restore_refusal_bypasses_finalization — an enclosing handler logs time, restores findings or saves/cleans the attempt after refusal
- 6: tests/test_stage2.py::test_runner_restores_deleted_change_directory_before_logging — missing contained parents stop recovering trusted inputs and time
- 6: tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs — safe retries retain corrupt input bytes
- 6: tests/test_stage2.py::test_repair_retry_restores_aliased_and_directory_inputs_without_following — safe leaf detachment modifies its external target or loses a retry
- 6: tests/test_stage2.py::test_runner_final_time_write_restores_alias_without_following — leaf symlink or hard-link recovery writes to the external target
- 6: tests/test_stage2.py::test_runner_keeps_rejected_time_across_input_restore — a contained retry loses its measured time
- 6: tests/test_stage2.py::test_a_failed_flash_process_restores_the_baseline_so_stage2_off_can_proceed — safe failed-call rollback no longer restores the baseline
- 3: tests/test_stage2.py::test_credential_scan_refuses_escaped_changed_parent — a refused scan leaves a credential in a contained file or fails to report its removal
- 3: tests/test_stage2.py::test_draft_credential_scan_names_escaped_path_without_claiming_restoration — a shared scan claims to restore a draft input
- 5: tests/test_stage2.py::test_moved_head_and_escaped_parent_report_both_without_writes — a recovery refusal hides the moved HEAD or writes findings/time afterward
- 5: tests/test_stage2.py::test_time_safety_refusal_reports_original_failure_and_exit — a propagating model-call failure loses its own exit code when recovery refuses

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change restore-symlink-parent
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --check
PYTHON=$PWD/.venv/bin/python3 make verify
```

Show the new refusal regressions red against the input runner, then green after
the fix, without live providers. The runner regenerates the index before the
registry/full checks and creates the one commit. At input commit `a20d786`,
`scripts/validate_change_artefacts.py` and `templates/plan.md` are absent;
use the available gates and the phase-3 prompt's plan form.

## Explore route

Research was written by the orchestrating Claude Code Opus 5.5 session on
2026-10-23 at `7586f1a` from an already reproduced finding; no separate Explore
call or Stage-1 fallback was recorded. The draft extends it with code inspection
at `a20d786`.

## Runner route — 2026-10-23

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-23 16:52:40–17:37:39 UTC, 2699 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-23 17:37:45–18:03:45 UTC, 1561 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-23 18:03:51–18:09:31 UTC, 340 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-23 18:24:57–18:39:59 UTC, 902 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-23 18:40:05–18:55:41 UTC, 936 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-10-23 19:48:33–20:03:25 UTC, 892 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-23 20:03:31–20:18:04 UTC, 873 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-10-24 09:40:00–09:59:53 UTC, 1193 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-24 10:39:48–10:56:05 UTC, 977 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
