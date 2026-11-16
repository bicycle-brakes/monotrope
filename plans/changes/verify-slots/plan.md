---
title: "Plan — verify-slots"
status: draft
implementation_status: partial
date: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification]
---

# Plan — `verify-slots`

```text
For you:     Four full checks can share the machine at once; slots and workers per run are one adjustable setting.
Done when:   The capacity regressions and the existing lock tests pass, make verify is green, and serial-versus-paired wall time and load are recorded.
Appetite:    Four hours of phase 4, repairs and both trials included; a stop, not an estimate.
Not now:     Worker tuning, swarm slots, automatic tuning, the general harness configuration.
Pre-mortem:  suppose it failed: most likely because a nested child inherited the wrong slot's ownership.
Starts unless you say stop.
```

## Approach and files

Bounded: no design phase and no ADR are due; implement from `spec.md`. The
change extends the existing admission (`scripts/verify_lock.py`) to a
configurable slot count; memory, timeout and duration semantics stay as they
are. Explore ran on Stage 2 (route flash, GLM 5.3 Flash, endpoint
`glm-coding-plan`, 2026-11-09, recorded in `research.md`); no Stage-1 route
is recorded, so there is no Explore fallback to carry. At the drafted commit
`templates/plan.md` and `scripts/validate_change_artefacts.py` do not exist:
this plan follows the phase-3 prompt's form, and their gate is not claimed.

1. Change `scripts/verify_lock.py`: declare the repository default of four
   slots (`DEFAULT_SLOTS`) and one reader, `read_settings`, of the layered
   settings: the default, then the machine-local `verify.toml` in the shared
   root (`${XDG_STATE_HOME:-~/.local/state}/coding-harness/`), a `[verify]`
   table with `slots` and `workers_per_run`, positive integers within their
   bounds (corrected 2026-11-15 to the shipped design, review round 5, row
   L5-3; `decisions.md#Q-6`). A missing file means the default. Refuse a
   symlinked, nonregular, unreadable or invalid file, and a leftover bare
   `verify.slots`, with a diagnostic before any protected work; read it
   without following and never write it during admission; re-read it under
   the registry lock for every reservation decision.
2. In the same file, keep `verify.lock` as the compatibility lock: the
   updated implementation takes it shared, so a legacy exclusive holder
   excludes all new work and new holders do not exclude each other. Add
   exclusive per-slot locks and per-slot ownership records (for example
   `verify.slot-<n>.lock` and `verify.slot-<n>.holder.json`, zero-based
   indices). Under the registry lock: prune dead waiters, let only the head
   live registration reserve, count every genuinely held slot lock —
   including indices at or above a lowered capacity — and reserve only
   while that count is below the capacity. Reuse freed indices; never
   unlink a lock file and never trust a record's content as liveness.
3. Still in `scripts/verify_lock.py`: publish and remove ownership only for
   the admission's own slot and token. Propagate a local slot marker (for
   example `HARNESS_VERIFY_LOCK_SLOT`) beside the existing pid/token pair;
   a nested entry validates that exact slot's held lock and stable record.
   Resolve the duration context from that same record; keep legacy nesting
   working when no slot marker stands in the environment and the old
   exclusive ownership is genuine. Add one `inherit_fds` helper that
   returns every descriptor a local child must inherit — this admission's
   slot lock and the shared compatibility lock — read from the active
   admission, so `hold_admission` keeps yielding one descriptor, or None
   when nested, exactly as today; apply it in the supervisor's spawn too.
   Release by closing descriptors after child cleanup, never by unlocking
   an inherited description. While waiting, log every occupied slot with
   its holder's details, keeping the initial and five-minute updates and
   never a token. Never hold the registry lock across a memory wait or
   protected work.
4. Change `scripts/stage2.py`: delegate the `_lock_fds` adapter to that
   helper so every admission-held local launch (the implement and draft
   `make verify` runs, the red-first probes and pytest runs, the docs
   gates) inherits both descriptors, and propagate the slot marker through
   `inherit_env`. Foreign-call environment filtering, the targeted checks
   outside admission and all timeouts stay untouched. Change
   `scripts/verify_all.sh` only where its comment states one admission;
   entry, `--held` delegation and gate commands stay as they are.
5. Change `tests/test_verify_lock.py`: add the ledger's new multi-process
   tests over isolated shared state roots, using separate working
   directories, events or pipes and bounded waits. Cover: the default two
   across trees, configured one and three, a live decrease draining,
   malformed settings, occupied higher indices, slot-specific nesting and
   context, peer-safe release, the memory gate on each slot, the wait
   diagnostics, and legacy exclusion including a supervisor killed with its
   child running. Keep the existing exclusivity, FIFO and lifecycle
   regressions meaningful by explicitly selecting capacity one where the
   scenario needs it; adapt fixture ownership records rather than deleting
   assertions.
6. Change `tests/test_stage2.py`: prove both descriptors and the slot
   identity reach local protected children and never foreign calls; keep
   the timeout and targeted-repair boundaries asserted. Change
   `tests/test_ci.py`: adapt fixture ownership records and add real shell
   contention at two slots, preserving gate verdicts, nested reuse and CI
   placement. `tests/test_verify_duration.py` needs no edits: the duration
   context resolves through `admission_context()`, and its slot-specific
   resolution is covered by a new lock test.
7. Change `docs/WORKFLOW.md`, `docs/orchestration.md` and
   `docs/how-it-works.md`: replace the current one-slot prescriptions with
   the configured default, the setting's shared path and format, its safe
   update by atomic replacement, draining on a decrease, and the retained
   memory policy; update the lane scheduling rule to spend the available
   configured capacity. Dated measurements stay as they are. None of these
   paths is held; the attempt edits them itself.
8. Create `plans/changes/verify-slots/measurements.md` during phase 4 with
   the trials below; update this `plan.md` only to mark written ledger
   entries and record time used. The runner regenerates `plans/INDEX.md`
   and owns derived stamps, verification and commits.

## Verification and measurement

From this worktree's locked environment:

```bash
.venv/bin/python3 -m pytest tests/test_verify_lock.py tests/test_ci.py tests/test_stage2.py tests/test_verify_duration.py -q
python3 scripts/check_interview_minimums.py --change verify-slots
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

Policy behaviour is tested with injected clocks and memory readers; no test
manufactures memory pressure. Corrected 2026-11-15 to the shipped design
(review round 5, row L5-3): the trials run under the night load, beside the
other lanes (`decisions.md#Q-3`), not in a quiet window. At one tested
implementation commit — the repaired head — the orchestrator runs three
trials, each child with the five inherited admission markers cleared so it
takes an admission of its own: a serial trial at capacity one, a paired
trial of two slots with six workers each, and a quad trial of four slots
with three workers each, starting the children of a batch coordinated and
joining them; no edits between runs. Each batch is read against
`decisions.md#Q-4` (every run within 1.6 times the serial run, no test red
or flaky because of the parallelism). After the merge the configuration is
chosen in real operation (`decisions.md#Q-7`): three windows of two days
each — four slots x three workers (the repository default), then three x
four, then two x six, the later two set in `verify.toml` — and the winner
is the shorter mean time from queueing to result, provided no additional
test turns red or flaky and free memory never falls below 25 %. The
enclosing runner's own verification stays on normal admission.

Record, in `measurements.md` (section "Trials on the repaired head"): date, commit, dirty state, Python and worker
configuration, memory floor, hardware, background workload, each exit code,
queue wait, execution and wall time per run, and the batch elapsed time.
Sample `os.getloadavg()` every five seconds across each batch and record
the one-minute series, its mean and maximum; a load that cannot be read is
explicitly not measured and leaves the evidence incomplete. Keep both
outcomes, including a slower paired result; a failure leaves completion
pending. Reuse the existing duration records; never an ownership token. The
four hours include the trials; do not claim unrun measurements.

Do not touch the `Makefile`, `decisions/gates.yaml`, generated CI,
`provenance.yaml`, ADRs, `AGENTS.md`, prompts, templates, interview
answers, model routing, worker sizing, research-swarm code, or the future
central configuration. The existing kit already ships
`scripts/verify_lock.py`; no new mechanism file is added.

Draft validation, 2026-11-10: the ledger's four existing tests are defined
in the tree and every not-yet-written entry names a function no file
defines; the card and the `## Time used` heading stand. The tracker-coupled
gates (plans-registry, dangling-beads, bead-export) need the runner's
tracker render and were not run here, nor the full suite; no green of
either is claimed. The deciding check is the runner's docs job, which stays
red on `question-context` until this change's `decisions.md` carries the
dated decision statements for Q-1 and Q-2 — a file a draft may not edit,
so only the maintainer's recording session can complete them. No phase-2a
rows stand in `findings.md`.

## Criterion ledger

- 1: tests/test_verify_lock.py::test_default_slots_share_capacity_across_trees — a check cannot enter below the default or one more overlaps every occupied default slot.
- 2: tests/test_verify_lock.py::test_shared_capacity_setting_and_live_decrease — one/three are ignored or a decrease overlooks occupied higher slots.
- 3: tests/test_verify_lock.py::test_invalid_or_unsafe_capacity_refuses_before_work — invalid, substituted or unreadable settings start work or hang.
- 4: tests/test_verify_lock.py::test_slot_waiters_reserve_in_fifo_order — a later waiter overtakes or an idle slot waits for another holder to finish.
- 5: tests/test_verify_lock.py::test_nested_entries_use_their_own_slot_and_context — full-capacity nesting queues or a peer's token, slot or context is resolved.
- 6: tests/test_verify_lock.py::test_slot_release_preserves_peers_and_inherited_children — cleanup deletes peer state, leaks capacity or releases before children end.
- 7: tests/test_verify_lock.py::test_each_slot_checks_memory_before_work — the second reservation starts below the floor or bypasses the existing policy.
- 7: tests/test_verify_lock.py::test_sustained_low_memory_refuses_at_the_bound — the low-memory refusal loses its deadline or diagnostic.
- 7: tests/test_verify_lock.py::test_unknown_memory_is_logged_and_does_not_block — unknown readings block or silently pass.
- 8: tests/test_ci.py::test_shell_runner_obeys_two_slot_admission — the shell or CI bypasses capacity or nesting changes a gate verdict.
- 8: tests/test_stage2.py::test_slot_admission_descriptors_reach_local_checks — slot or compatibility ownership is lost across a local launch or reaches foreign calls.
- 8: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout — the admission wait consumes checking time.
- 8: tests/test_verify_duration.py::test_monotonic_execution_excludes_admission_wait — the wait is included in execution.
- 9: tests/test_verify_lock.py::test_wait_logs_name_all_occupied_slots_without_tokens — a holder disappears from the progress logs or a token is exposed.
- 10: tests/test_verify_lock.py::test_legacy_exclusion_survives_new_holder_supervisor_death — old and new protected intervals overlap.
- 12: tests/test_verify_lock.py::test_layered_settings_default_override_and_sources — a layer is ignored, workers do not follow an overriding slot count, or a source names the wrong layer.
- 12: tests/test_verify_lock.py::test_workers_follow_slots_and_memory_bound — the old half-the-cores rule, a per-run memory bound, or a guessed count with nothing readable.
- 12: tests/test_verify_lock.py::test_settings_command_logs_values_and_sources — a run's log does not name the values in force and their sources.
- 12: tests/test_ci.py::test_runner_takes_workers_from_the_machine_settings_file — a runner without a caller value (as the Stage-2 runner starts it) ignores the machine file or the slot-derived count.
- 12: tests/test_stage2.py::test_targeted_pytest_uses_the_memory_derived_worker_bound — the runner's targeted pytest derives its own count instead of the one reader's.
- 13: tests/test_verify_duration.py::test_history_records_settings_load_and_peak_rss — the history lacks the values, sources, end load or peak, records a missing sample as a number, or refuses older records.
- 13: tests/test_verify_duration.py::test_pytest_tree_rss_sums_pytest_trees_below_the_runner — xdist workers are left out, a process counts twice, or a foreign pytest counts.
- 11: not a test — the phase-6 review reads `measurements.md` and the three updated current-policy documents against criterion 11; absent revision-bound serial-versus-paired wall-time and load evidence, or a stale one-slot prescription, refutes it.

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash failed the post-run checks after the allowed attempts (2026-11-10).

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash failed its post-run checks on 2026-11-10; the earlier Sonnet call ended with exit 1 before it changed code.

## Stop report — 2026-11-11

The appetite is four hours, a stop and not an estimate. The runner's time
ledger below records about 12.5 hours of implement and repair attempts by
2026-11-11 03:32 UTC, about three times the appetite; the orchestrator
reported the overrun in the conversation on 2026-11-10 and did not record it
here (review round 3, row L3-1). The maintainer decided on 2026-11-10 to go on
because the speed-up of `make verify` was made first priority, and on
2026-11-11 approved this record as the third hand intervention of the change.

What stands: two slots with capacity read from one documented home, a slot
holder record per slot, nested admission, accepted after two repair rounds
(`bb1c93ca`) with a green full check. What evidence is missing: the two
measured trials (one slot against two) and the boundary of 2026-11-11 (spec,
"Boundary"), which the next repair implements.

### Addendum — 2026-11-14

This addendum corrects the report above without rewriting it (review round 4,
rows L4-3, L4-4 and L4-9).

- **The boundary is built.** The repair of 2026-11-12 (`3b36a0e7`, rows L3-2
  and L3-3) implemented the spec's one-admission-per-process boundary: a
  second admission in a process that already holds one is refused at once,
  naming the held slot (`scripts/verify_lock.py`, `hold_admission`), pinned by
  `tests/test_verify_lock.py::test_overlapping_admissions_preserve_remaining_context`.
  The sentence above that the next repair implements it describes the state
  of 2026-11-11.
- **"Accepted" above names the runner's verdict on a repair attempt**, not the
  plan's status. The plan and the spec stay `status: draft` until the change
  closes; their `implementation_status` is now `partial`, because the code
  stands and the measured trials of criterion 11 are still missing.
- **New appetite.** On 2026-11-14 the maintainer resumed the lane with a new
  appetite of three hours for the rest of the change. The paired trial runs
  first; if it shows no throughput gain over one slot, the lane stops and
  reports what stands.

### Addendum — 2026-11-15

This addendum extends the plan without rewriting it (maintainer, 2026-11-14/15,
`decisions.md#Q-3` to `#Q-7`; new appetite three hours for the lane).

- **Layered settings** (criteria 12 and 13). `read_settings` in
  `scripts/verify_lock.py` is the one reader of the slot count and the
  pytest workers per run; the repository default is four slots, so three
  workers on twelve logical cores. The machine-local `verify.toml` in the
  shared state root replaces `verify.slots`. `scripts/verify_all.sh` hands
  its machine readings to the reader instead of its half-the-cores rule;
  `scripts/stage2.py`'s targeted pytest asks the same reader. The runner's
  full check needs no worker variable, so its allow-list's drop of
  `PYTEST_XDIST_AUTO_NUM_WORKERS` no longer matters
  (`tests/test_ci.py::test_runner_takes_workers_from_the_machine_settings_file`).
  `scripts/verify_duration.py` records the values and sources at the start
  and the end load and pytest peak memory at the end. Step 8's "worker
  sizing" exclusion is superseded by `decisions.md#Q-6`.
- **The census tests.** The research header of this change was untruthful
  since pull request 388; it is corrected through `research_publication` in
  `scripts/stage2.py` (`327e51d7`).
- **The trials** of 2026-11-14 are recorded in `measurements.md`, under the
  night load, with the deviations from the protocol above named there. The
  real-operation windows of `decisions.md#Q-7` follow the merge.
- **Time used, by hand (Opus subagent), 2026-11-15:** about 1.5 hours for
  the census fix, the layered settings with their tests, and the documents;
  not measured by the runner.

## Runner route — 2026-11-11

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-10 09:26:23–10:34:38 UTC, 4095 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 10:34:48–10:39:42 UTC, 293 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 10:39:52–10:42:42 UTC, 170 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-10 10:50:19–11:36:09 UTC, 2750 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-10 13:17:54–14:17:05 UTC, 3551 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-10 16:46:53–16:50:45 UTC, 232 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-10 16:51:07–20:29:38 UTC, 13110 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-10 21:44:33–2026-11-11 03:31:56 UTC, 20841 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-11 14:25:30–15:26:28 UTC, 3657 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-11 15:26:42–16:25:04 UTC, 3501 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-11 16:25:20–16:56:13 UTC, 1853 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 01:34:57–02:02:42 UTC, 1665 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 02:02:53–02:30:49 UTC, 1676 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-15 20:25:53–21:16:02 UTC, 3009 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-16 08:31:51–08:52:02 UTC, 1211 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-16 08:52:10–09:45:53 UTC, 3224 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/verify_lock.py` is shared execution infrastructure · measured by the runner
