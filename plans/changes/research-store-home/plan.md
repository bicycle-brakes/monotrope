---
title: "Plan — research-store-home"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-05
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-nxdy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm, state-store]
---

# Plan — research-store-home

```text
For you:     Research uses its own store setting and a default outside HOME, without moving the verification queue.
Done when:   The ten acceptance criteria have their evidence and make verify is green.
Appetite:    2 hours of phase 4 including repairs; stop at the limit.
Not now:     Automatic migration, other state locations, record formats or a new locking protocol.
Pre-mortem:  suppose it failed: most likely because a test fixture still redirects only XDG_STATE_HOME and writes to the real default store.
Starts unless you say stop.
```

Implements `spec.md` at source commit `a06da805`, read 2026-11-05. Class:
`bounded`; no design or ADR is due. Explore used Stage 2, route `flash`, model
`glm-5.3-flash`; no Stage-1 fallback is recorded. No maintainer decision is open.
There is no `templates/plan.md` in this tree; this plan follows the phase-3 prompt.

## Files and steps

1. `scripts/stage2_research_store.py`: make `research_dir` read only
   `STAGE2_RESEARCH_STATE` at call time, with a pure helper for the default base.
   An empty value selects `/Users/Shared/coding-harness-research-<uid>` on macOS
   or `/var/tmp/coding-harness-research-<uid>` on other supported POSIX systems,
   with `os.getuid()` supplying the user id; reject relative values with
   `StoreWriteError`. Preserve the suffix
   `coding-harness/stage2/<change>@<sha256(resolved-root)[:8]>/research`.
   Update the module, resolver and placement docstrings and refusal text to
   name the new setting.
   Keep seals, writes, locks, realpath boundary checks and reuse rules intact.
2. `scripts/stage2_research_run.py`: move store construction into `Run.open`'s
   existing guarded opening block so a relative-base `StoreWriteError` becomes
   the same exit-1 `CallFailed` as an unusable store; that opening failure's
   guidance names `STAGE2_RESEARCH_STATE`. Do not change receipts or publication.
3. `tests/test_stage2_research_store.py`: redirect the `state_home` fixture and
   explicit subprocess environments to the dedicated variable; test unset and
   empty defaults by mocking platform/user identity without creating real state.
   Exercise overrides after import, independence from XDG/HOME/cwd, relative
   rejection, worktree/change isolation and resolved aliases. Compare
   `verify_lock.state_root()`, `stage2.record_dir()` and `stage2.lock_path()` with
   fixed HOME/XDG and two dedicated settings. Update home-guard diagnostics and
   make the canary test select its directory through `research_dir`, using the
   production launch environment allow-list rather than manually filtering one
   variable. Preserve permission, atomic-write, kill, lock and reuse assertions.
4. `tests/test_stage2_swarm.py`: add the dedicated temporary base to `sworld`
   while retaining its XDG setting for unrelated state. Adapt the home-refusal
   test to explicit inside/outside dedicated bases; add default-startup,
   relative/unwritable-base and launch-input-canary tests through the real
   `Run.open` path with model stand-ins. For default-startup, remove the
   dedicated variable and redirect only the resolver's platform-default helper
   to a synthetic outside-home base; separately assert the real platform path
   in unit tests. All refusal cases assert exit 1, no calls, the setting named,
   and no fallback store; retain existing resume and clear/lock tests.
5. `tests/test_stage2_research_deep_review.py`: adapt the release regression to
   create loop state and store state independently, assert durable store bytes
   survive release, and prove a second holder still gets `StoreLocked`; retain
   assertions for kept research receipts/audits and removal of an empty loop record.
6. `scripts/research_capture.py`: select the synthetic store using the dedicated
   variable in `build_world` and `state_store_guard`, restoring its previous
   value in `finally`; keep HOME/XDG synthetic and the two guard outcomes intact.
   Update the canary location labels, docstring and generated report explanations.
7. `tests/test_research_capture.py`: pin the new synthetic setting and add a
   guard test for both outcomes and restoration with the variable initially set
   and unset; retain the stand-in end-to-end and environment-redaction checks.
8. `docs/WORKFLOW.md`: extend the research-resume paragraph with the variable,
   exact platform defaults and suffix, private store modes (0700 directories,
   0600 records/lock), unchanged home/repository exclusions and refusal behavior.
   Explain that XDG still places verification and review state, old stores are
   neither moved nor deleted, and selecting a previous safe base explicitly can
   resume them; a new default does not discover them automatically.
9. `plans/changes/research-store-home/plan.md`: replace each not-yet-written
   ledger marker when its test exists and record measured phase-4 time below.
   `plans/INDEX.md`: the runner regenerates the index after artifact header edits.

No files are deleted. No held path requires an orchestrator bootstrap edit.
Do not touch `scripts/verify_lock.py`, `scripts/stage2.py`,
`scripts/stage2_availability.py`, neighbouring change artifacts, governance
files, model settings or the tracker. This change
does not promise one verification lock for callers choosing different XDG roots.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_research_store.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_research_capture.py tests/test_verify_lock.py -q
.venv/bin/python scripts/check_interview_minimums.py --change research-store-home
.venv/bin/python scripts/check_research_handoff.py --change research-store-home
.venv/bin/python scripts/check_criterion_ledger.py
make verify
```

Run all storage tests against temporary bases, including child processes; mock
default path selection for opening tests so no real shared directory is written.
The phase-6 review compares the workflow paragraph with the resolver and spec.

## Criterion ledger

- 1: tests/test_stage2_research_store.py::test_research_override_is_read_at_call_time — cached environment or XDG takes precedence
- 2: tests/test_stage2_research_store.py::test_research_default_is_stable_per_user_and_outside_home — default depends on HOME, XDG or cwd, or uses the wrong platform/user path
- 2: tests/test_stage2_swarm.py::test_default_research_store_starts_without_moving_xdg — the default still causes the home guard to refuse an ordinary run
- 3: tests/test_stage2_research_store.py::test_research_setting_does_not_move_verification_or_loop_state — another state path follows the dedicated setting
- 4: tests/test_stage2_research_store.py::test_research_store_keeps_change_and_resolved_worktree_keys — roots collide or aliases split
- 5: tests/test_stage2_research_store.py::test_store_is_owner_only_outside_every_model_directory — a readable/traversable existing level is not tightened to 0700 and reported, a private record or lock mode is widened, or a group/other-writable level is accepted
- 5: tests/test_stage2_research_store.py::test_store_refuses_a_symlinked_directory — a symlink is followed
- 6: tests/test_stage2_swarm.py::test_a_store_inside_the_real_home_is_refused_and_one_outside_it_is_accepted — home overlap launches a model or guidance names only XDG
- 6: tests/test_stage2_research_store.py::test_the_home_guard_resolves_dotdot_and_parent_links_before_comparing — a resolved home or repository alias bypasses the guard
- 6: tests/test_stage2_swarm.py::test_invalid_research_base_stops_before_model_calls — a relative or unwritable base launches a model, escapes failure handling or falls back
- 7: tests/test_stage2_research_store.py::test_store_canary_never_reaches_a_payload_argv_or_environment — the dedicated setting or resolved store canary reaches a child
- 7: tests/test_stage2_swarm.py::test_research_store_setting_never_reaches_model_launch_inputs — a real launcher forwards the setting or directory
- 8: tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome — relocation loses a flushed record after interruption
- 8: tests/test_stage2_research_store.py::test_reuse_requires_the_exact_binding_seat_model_and_prompt — a mismatched slot becomes reusable
- 8: tests/test_stage2_research_store.py::test_a_changed_binding_reuses_nothing_and_names_the_paths — a different input binding reuses results
- 8: tests/test_stage2_research_deep_review.py::test_a_failed_clear_binds_the_bytes_actually_appended — matching interrupted results cease to be reusable
- 9: tests/test_stage2_research_deep_review.py::test_releasing_the_loop_keeps_the_research_store_and_its_lock — release removes store bytes or permits a competing lock holder
- 10: not a test — phase-6 review compares docs/WORKFLOW.md's setting, defaults, modes and migration guidance with the resolver and spec; stale XDG setup advice or an omitted default refutes it

## Time used

2026-11-04 23:48:56–2026-11-05 00:49:21 UTC, 3624 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-05 00:49:32–01:30:35 UTC, 2463 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-11-05 07:43:36–09:22:01 UTC, 5904 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 11:52:54–13:32:29 UTC, 5975 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 14:32:18–16:21:04 UTC, 6525 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 19:02:23–21:29:36 UTC, 8831 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-05 21:29:49–2026-11-06 00:59:19 UTC, 12568 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-06 01:08:05–03:02:09 UTC, 6843 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Appetite overrun — 2026-11-05

Phase 4 took about 5 h gross (Time used above) against the 2-hour appetite, much of it verify-lock waits. The orchestrator reported it at about 3.3 h; the maintainer let the change run to its pull request ("Weiter", 2026-11-05, ~10:15 UTC).
