---
title: "Plan — verify-cheap-before-admission"
status: accepted
implementation_status: done
date: 2026-11-13
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, admission, kit]
---

# Plan — verify-cheap-before-admission

```text
For you:     Cheap verification faults appear before the slot wait, together, in local and runner checks and in kit recipients.
Done when:   Contention proofs show cheap red never queues, changed trees are rechecked, protected gates keep their lock, and make verify is green.
Appetite:    6 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     More slots, faster test bodies, cross-run caching, a post-merge check, or migrating recipient repositories.
Pre-mortem:  suppose it failed: most likely because a runner call still takes admission around the whole check.
Starts unless you say stop.
```

## Build sequence and files

1. **Attempt — metadata.** Change `scripts/ci_gates.py` to validate optional
   `needs_admission` as a strict boolean, default false, and expose its declared
   and effective values in normalized records/JSON and the generated catalogue.
   Effective protection is `cost == "minutes" or needs_admission`; false cannot
   exempt a minutes gate. Keep schema 3, the three-column TSV, existing command
   output, filters and generated hosted workflow unchanged. Supply root-scoped
   selection/report APIs so a caller never measures the importer's checkout by
   accident. Add the scheduler's caller/test registration and update the
   admission helper's explanatory registration in this same file.
2. **Attempt — one scheduler.** Create `scripts/verify_run.py` as a library and
   CLI. It consumes the reader's normalized selection, executes every
   unprotected gate, returns red without queueing on local blocking failure,
   otherwise acquires `verify_lock.hold_admission` once for the protected set.
   Use stable seconds-before-minutes order locally, retaining declaration order
   within each class; partition out marked seconds gates into the protected
   set. Run that set with local first-blocking-stop; `--ci` exhausts both sets
   even after blocking red, preserving its placement/action-equivalent rules.
   Empty/failed selections fail before admission; empty protected sets never
   enter the lock. Print exact existing command/verdict gate frames and honest
   not-run summaries outside frames. Extract, rather than duplicate, the loop's
   command substitution, enforcement, worker sizing and duration behavior.
3. **Attempt — tree comparison in the scheduler.** Snapshot before and after
   each cheap pass using HEAD, NUL-delimited semantic index entries, and tracked
   plus non-ignored untracked path inventories; hash paths, types, modes and
   contents, including deletions and symlink targets without following links.
   Ignore index stat-cache churn and ignored untracked caches, not tracked
   ignored files. Handle unusual filenames without line parsing. Bound Git
   calls, refuse unreadable/nonregular/unsupported entries (including gitlinks
   until explicitly supported), and reject a changing snapshot. On admission,
   equal snapshots reuse cheap results; a difference reloads the gate list and
   selection and reruns the complete current unprotected set inside the held
   admission. A changed/failed refresh exits diagnostically before protected
   gates. Retain no reusable receipt on disk or through caller environment.
4. **Attempt — shell and process ownership.** Change `scripts/verify_all.sh`
   into the existing interpreter/PATH/argument bootstrap followed by the shared
   scheduler, retaining `--list` as a non-measured, admission-free operation.
   Move its worker default into the common scheduler for both callers. The
   scheduler's default executor runs each gate as a registered process group;
   signals/timeouts end all descendants before admission exits, and the lock
   descriptor is inherited by protected children. Change only explanatory
   caller text in `scripts/verify_lock.py`; reuse its queue, memory, nesting,
   refusal and cleanup APIs without changing their algorithms.
5. **Attempt — history.** Change `scripts/verify_duration.py` to expose
   root/environment-scoped library operations used by the scheduler, retaining
   its CLI and old version-1 records. Start one run before selection; record
   every executed gate, including repeated cheap gates. Add optional validated
   completion fields for `admission_requested`, final admission context and
   final revision/configuration identity; the reader prefers completion context
   when present and reads old start-only context otherwise. `run_end.seconds`
   sums active segments before/after admission, excluding queue and memory
   waits. State “no admission requested” explicitly on cheap-only completions;
   preserve unknown values, interrupted starts and warn-only storage failure.
   The final report distinguishes initial and final tree identity after a
   changed wait. Do not persist file contents or fingerprints as reusable proof.
6. **Attempt — runner integration.** Change `scripts/stage2.py::full_verify`,
   full-mode `verify_attempt`, and `verify_draft` to call the common scheduler
   API instead of taking outer admission and launching an admitted whole-run
   `make`/docs shell. Keep full versus docs selection, draft's existing ADR
   tolerance environment, preparation order, tool checks, intent-to-add cleanup,
   scrubbing, time logging and retry decisions. Run full-mode preparation
   outside admission, as targeted preparation already does. Pass a callback
   using existing `launch` for each gate with the remaining `VERIFY_SECONDS`
   allowance and current minute label; never reset the allowance per gate.
   Pause only around admission, bound metadata subprocesses, and reuse existing
   cancellation/group cleanup. Use explicit root/env/output parameters, never
   process-wide cwd/environment changes. Add `scripts/verify_run.py` to shared
   infrastructure and any relevant tool-snapshot dependency inventory. Targeted
   selection and independent proof/import-probe admission remain unchanged.
7. **Attempt — proofs and compatibility.** Create portable
   `tests/test_verify_before_admission.py` for the new ledger entries below.
   Change `tests/test_verify_cheap_first.py` to retain its named proofs while
   expecting all cheap diagnostics before protected-work suppression and copying
   the new dependency. Initialize copied trees as Git repositories and put
   command markers outside them (or in ignored fixture paths), so the proofs
   measure real input edits rather than their own test logs. Change
   `tests/test_ci.py` copied-runner fixtures and
   timing/admission expectations; retain hosted exhaustiveness/worker tests.
   Change `tests/test_stage2.py` to exercise all three scheduler consumers with
   planted gates, retaining the existing named timeout, nesting, draft-selection
   and refusal proofs instead of asserting a whole-run `make` stand-in.
   Its frame guard must exercise the real shared scheduler's output. Put the
   multiple-failure parser proof in `tests/test_verify_cheap_first.py`, whose
   existing Stage-2 import does not travel, rather than importing Stage 2 in
   the new portable test file. Change
   `tests/test_verify_duration.py` for additive completion fields, old records,
   repeat events, fake-clock wait exclusion and storage failure. Change
   `tests/test_gate_catalog.py` for the admission column.
8. **Attempt — portable distribution and docs.** Change
   `scripts/kit/manifest.yaml` to classify `scripts/verify_run.py` and
   `tests/test_verify_before_admission.py` as mechanism and update the admission
   description. The new proof copies manifest-selected mechanism files into
   an isolated Git recipient, uses renamed gates and runs without source-tree
   imports or Stage 2. Change `docs/WORKFLOW.md`, `docs/how-it-works.md`,
   `docs/orchestration.md`, and `docs/testing.md` to describe two phases,
   exhaustive cheap diagnostics, tree reuse, seconds-only jobs and active-time
   measurement. Explain that only protected work occupies the machine slot;
   retain existing lane priority and memory policy. Change
   `docs/governance/gate-catalog.md`: refresh its generated inventory with
   `python3 scripts/ci_gates.py --catalog` and explain the admission column.
   This unheld output must match the generator before the attempt is accepted.
9. **Orchestrator bootstrap, after the accepted attempt.** Audit every current
   seconds command for a shared-state operation needing serialized verification;
   the draft audit identified none. Edit held `decisions/gates.yaml` only to
   document `needs_admission` and the new execution rule, leaving existing
   costs/commands/enforcement and schema 3 intact. If the audit uncovers a gate
   contradicting the draft audit, resolve that evidence before activation;
   never guess which work is safe. Edit held `prompts/05-verify.md`'s local-run
   description. Verify that `docs/governance/gate-catalog.md` still matches
   `python3 scripts/ci_gates.py --catalog`; the held comment edits should change
   no generated rows or hosted workflow bytes. Run final checks after these
   edits; an accepted attempt before bootstrap is not final evidence.

Maintain this change's `spec.md` and `plan.md` status/ledger markers as phase 4
progresses. The runner owns `findings.md`, measured Time used entries and
`plans/INDEX.md` regeneration. No files are deleted; no design or ADR is due.

## Verification

Use isolated state roots and small marker gates, not the real suite behind a
long queue. Hold a real admission in a separate process, wait for explicit
holder/cheap-gate markers, and prove cheap red completes with no queue entry
while the holder stays alive. For green contention, prove cheap completion
before release and protected start only afterwards. Change an already dirty
file without changing porcelain status, index entries, HEAD, untracked bytes,
deletions/modes/symlinks and the gate list while queued; unchanged and ignored
cache changes must reuse. Reclassification must use the refreshed list. Plant
an unstable/unreadable snapshot, refusal, forged marker and cancellation with a
lingering grandchild. Check marker order, gate frames, parser results, history
and exit status together. No network or model calls belong in these proofs.

Use injected clocks and short execution bounds to show two gate durations
consume one allowance and queue/memory waits consume none. Exercise local
verify/docs/drift, nonblocking levels, `--list`, `--ci`, inherited admissions,
and all three Stage-2 consumers. Update existing fixture plumbing for the new
dependency; preserve old named tests because earlier criterion ledgers cite
them. No blanket skip or expected-failure switch is final evidence.

```sh
python3 scripts/check_interview_minimums.py --change verify-cheap-before-admission
.venv/bin/python3 -m ruff check scripts/ci_gates.py scripts/verify_run.py scripts/verify_duration.py scripts/verify_lock.py scripts/stage2.py tests/test_verify_before_admission.py tests/test_verify_cheap_first.py tests/test_ci.py tests/test_stage2.py tests/test_verify_duration.py tests/test_gate_catalog.py
.venv/bin/python3 -m ruff format --check scripts/ci_gates.py scripts/verify_run.py scripts/verify_duration.py scripts/verify_lock.py scripts/stage2.py tests/test_verify_before_admission.py tests/test_verify_cheap_first.py tests/test_ci.py tests/test_stage2.py tests/test_verify_duration.py tests/test_gate_catalog.py
bash -n scripts/verify_all.sh
.venv/bin/python3 -m pytest tests/test_verify_before_admission.py tests/test_verify_cheap_first.py tests/test_verify_lock.py tests/test_verify_duration.py tests/test_ci.py tests/test_gate_machinery.py tests/test_gate_catalog.py -q
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'verification_admission_is_outside_execution_timeout or local_checks_preserve_nested_admission or draft_docs_check_keeps_admission_and_execution_limit or draft_runs_the_existing_docs_subset or frames_red_sections_reads or before_admission'
python3 scripts/ci_gates.py --check-schema
python3 scripts/ci_gates.py --check-ci
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py --change verify-cheap-before-admission
python3 scripts/plans_registry.py --check
make verify
```

The runner performs the final full check and commit after bootstrap. Phase 1
used Stage 2, route `flash`, model `glm-5.3-flash`; no Stage-1 fallback is
recorded. At `b1d4e621` (2026-11-13), `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent; use the prompt's form and
available interview, ledger and registry checks. Findings hold no phase-2a rows.

Draft checks on 2026-11-13: interview minimums, criterion ledger, research
handoff and artifact metadata/card checks passed; `git diff --check` passed.
The registry's full check was not run in this drafting call because its
tracker access can leave the worktree-only read boundary; index regeneration
and the full check belong to the orchestrating runner. Implementation proofs
and `make verify` have not run for this unimplemented change.

## Amendment 2026-11-16 — declared-cheap choke point (decisions.md#Q-7)

10. **Attempt — one classification.** In `scripts/ci_gates.py` add one
    predicate `declared_cheap(gate)`: true only for `cost == "seconds"` without
    `needs_admission: true` (missing or unknown cost is not cheap); derive
    `admission` from it. `scripts/verify_run.py` and `scripts/stage2.py`'s
    `document_gates` consume only that field; the draft check names deferred
    document gates in its scope line and does not refuse when every document
    gate is deferred. In `scripts/verify_run.py` an unmeasurable snapshot counts
    as a moved tree (cheap pass first, full cheap rerun inside the admission),
    at every measurement point. Update `docs/WORKFLOW.md` and the module
    docstring. Proofs, red before green: an unmeasurable tree (tracked FIFO)
    runs cheap gates first and reruns them admitted; a cheap red on it ends
    without admission; a minutes or marked document gate is never launched by
    the draft check; the predicate table. Existing tests that pinned the
    refusal (`test_unmeasurable_inputs_refuse_reuse`,
    `test_seconds_only_job_runs_on_an_unmeasurable_tree`,
    `tests/test_ci.py::test_runner_report_matches_selected_job`) are amended.

## Criterion ledger

- 1: tests/test_verify_before_admission.py::test_admission_metadata_is_validated_and_cost_derived — invalid booleans pass or false exempts minutes
- 2: tests/test_verify_before_admission.py::test_all_cheap_failures_finish_without_queueing — a cheap gate is skipped or red requests the held slot
- 3: tests/test_verify_before_admission.py::test_only_protected_work_enters_one_admission — protected work escapes the holder or requests multiple admissions
- 3: tests/test_verify_before_admission.py::test_seconds_only_jobs_never_request_admission — docs/drift queues despite no protected gates
- 4: tests/test_verify_before_admission.py::test_unchanged_tree_reuses_cheap_results — an unchanged cheap command runs twice
- 4: tests/test_verify_before_admission.py::test_changed_tree_refreshes_selection_and_rechecks — content/index/HEAD/config changes reuse stale cheap results
- 1: tests/test_verify_before_admission.py::test_only_declared_cheap_gates_run_before_admission — a missing/unknown cost or a marked seconds gate counts as cheap
- 5: tests/test_verify_before_admission.py::test_unmeasurable_inputs_refuse_reuse — failed selection or unstable snapshots produce green, or unreadable-tree cheap results are reused
- 5: tests/test_verify_before_admission.py::test_unmeasurable_tree_runs_cheap_first_and_defers_the_rest — an unmeasurable tree refuses before cheap gates or reuses their results
- 10: tests/test_stage2.py::test_draft_defers_document_gates_not_declared_cheap — a minutes or marked document gate runs in the draft check
- 6: tests/test_verify_before_admission.py::test_enforcement_and_ci_exhaustiveness_survive_partitioning — nonblocking red blocks or CI misses a selected gate
- 6: tests/test_ci.py::test_every_gate_step_runs_even_after_a_failing_gate — generated hosted steps lose their always-run conditions
- 7: tests/test_verify_before_admission.py::test_nested_refused_and_interrupted_protected_work — forged ownership passes, nesting deadlocks or a descendant outlives admission
- 8: tests/test_verify_before_admission.py::test_two_phases_share_history_and_exclude_wait — history duplicates the run, loses a real repeat or charges queue time
- 8: tests/test_ci.py::test_duration_storage_failure_warns_without_changing_verdict — broken measurement storage changes enforcement
- 8: tests/test_verify_duration.py::test_completion_context_is_additive_and_old_history_reads — old records fail or final context is misattributed
- 9: tests/test_verify_cheap_first.py::test_multiple_cheap_failures_keep_parser_frames — captured output loses either failed section or invents a skipped one
- 10: tests/test_stage2.py::test_full_and_draft_checks_share_before_admission_scheduler — a full consumer retains an outer admission or loses its gate selection, or the draft leg requests an admission or runs the verify selection
- 10: tests/test_stage2.py::test_draft_docs_check_keeps_admission_and_execution_limit — a draft document gate inherits an admission or loses the per-gate tool limit
- 10: tests/test_stage2.py::test_before_admission_execution_budget_is_shared_and_wait_free — each gate resets the allowance or queue time consumes it
- 10: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout — a queued timely check times out or a hung gate survives the bound
- 11: tests/test_verify_before_admission.py::test_transferred_kit_keeps_before_admission_behavior — renamed recipient gates need a source-tree import or an opt-out

## Limits and ownership

Do not edit `Makefile`, hosted workflow output, other change folders or the
existing living derived-preparation spec: their public entry points and
preparation contract remain valid. No changes to slot count, queue algorithm,
memory/worker sizing policy, targeted/proof selectors, ADRs, model settings,
provenance rules, templates or other held paths. The attempt must never edit
the two held files assigned in step 9, including during repair. The
orchestrating session presents the card unchanged; this drafting call only
writes artifacts, never starts phase 4 or commits.

## Runner route — 2026-11-13

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-14

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-16

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-18

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-19

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-13 19:41:09–21:38:56 UTC, 7067 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-13 21:39:03–22:13:03 UTC, 2040 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 16:43:52–17:05:49 UTC, 1317 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-14 17:06:08–17:45:23 UTC, 2355 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-14 17:45:31–18:11:07 UTC, 1536 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-15 14:46:20–15:31:27 UTC, 2707 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/verify_run.py` is shared execution infrastructure · measured by the runner
2026-11-15 16:04:18–17:04:08 UTC, 3589 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/verify_run.py` is shared execution infrastructure · measured by the runner
2026-11-15 19:05:46–20:32:14 UTC, 5188 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-16 13:49:35–13:51:58 UTC, 143 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-16 13:52:05–13:53:22 UTC, 76 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-16 13:53:29–15:54:31 UTC, 7262 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure · measured by the runner
2026-11-16 16:12:25–16:41:40 UTC, 1754 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure · measured by the runner
2026-11-16 23:03:06–23:17:55 UTC, 889 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-16 23:18:03–23:33:53 UTC, 950 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-18 00:12:38–01:00:49 UTC, 2892 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/verify_run.py` is shared execution infrastructure · measured by the runner
2026-11-18 13:10:44–13:26:46 UTC, 962 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-18 15:39:09–15:40:28 UTC, 79 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-18 15:40:39–15:41:54 UTC, 75 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-18 15:42:05–15:43:28 UTC, 83 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 15:33:52–15:55:52 UTC, 1320 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 15:56:44–16:14:17 UTC, 1053 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 16:14:30–16:29:54 UTC, 924 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 16:33–17:28 UTC, about 55 min — repair F6-1 · hand finish by an Opus subagent (orchestrator hand edit 219f1c73) after the three rejected attempts · full `make verify` green (21 gates; markdownlint red as report only, on files outside this change) · start estimated from the subagent's first test run, not measured by the runner
