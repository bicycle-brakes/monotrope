---
title: "Findings — verify-cheap-before-admission"
category: findings
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-cheap-before-admission

Stage-2 call, 2026-11-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1044 files, 4108 commits, 12 rules.

Stage-2 call, 2026-11-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1047 files, 4123 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +33 -17
> - `docs/governance/gate-catalog.md` +36 -31
> - `docs/how-it-works.md` +8 -6
> - `docs/orchestration.md` +2 -2
> - `docs/testing.md` +8 -7
> - `plans/changes/verify-cheap-before-admission/plan.md` +15 -15
> - `scripts/ci_gates.py` +86 -24
> - `scripts/kit/manifest.yaml` +8 -2
> - `scripts/stage2.py` +118 -83
> - `scripts/verify_all.sh` +14 -258
> - `scripts/verify_duration.py` +196 -54
> - `scripts/verify_lock.py` +6 -4
> - `scripts/verify_run.py` +711 -0
> - `tests/test_ci.py` +112 -74
> - `tests/test_gate_catalog.py` +10 -3
> - `tests/test_stage2.py` +251 -13
> - `tests/test_verify_before_admission.py` +712 -0
> - `tests/test_verify_cheap_first.py` +103 -24
> - `tests/test_verify_duration.py` +84 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `scripts/verify_run.py`, `tests/test_ci.py`, `tests/test_verify_before_admission.py`, `tests/test_verify_cheap_first.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/stage2.py:5635:56: ARG001 Unused function argument: `key`
>      |
> 5635 | def _scheduled_verify(root: Path, env: dict[str, str], key: str | None, job: str) -> tuple[str, str, int]:
>      |                                                        ^^^ ARG001
> 5636 |     """One run of `job` through the shared two-phase scheduler; returns (stdout, stderr, exit code).
>      |
>
> scripts/stage2.py:5652:18: ARG001 Unused function argument: `gate`
>      |
> 5650 |     limit = f"the runner's step limit after {VERIFY_SECONDS // 60} minutes"
> 5651 |
> 5652 |     def run_gate(gate: dict[str, object], command: str, gate_env: dict[str, str]) -> verify_run.GateProcess:
>      |                  ^^^^ ARG001
> 5653 |         descriptor = slot.get("fd")
> 5654 |         pass_fds = (descriptor,) if gate_env.get(verify_lock.LOCK_ENV) and descriptor is not None else ()
>      |
>
> scripts/verify_run.py:205:22: PTH115 `os.readlink()` should be replaced by `Path.readlink()`
>     |
> 203 |     if stat.S_ISLNK(info.st_mode):
> 204 |         try:
> 205 |             target = os.readlink(path)
>     |                      ^^^^^^^^^^^ PTH115
> 206 |         except OSError as error:
> 207 |             raise SnapshotUnusable(
>     |
>
> scripts/verify_run.py:215:14: PTH123 `open()` should be replaced by `Path.open()`
>     |
> 213 |     digest = hashlib.sha256()
> 214 |     try:
> 215 |         with open(path, "rb") as handle:
>     |              ^^^^ PTH123
> 216 |             for block in iter(lambda: handle.read(1 << 20), b""):
> 217 |                 digest.update(block)
>     |
>
> scripts/verify_run.py:313:14: C416 Unnecessary list comprehension (rewrite using `list()`)
>     |
> 311 |     cpu = _usable_count(cores)
> 312 |     mem = _usable_count(nbytes)
> 313 |     bounds = [bound for bound in (cpu // 2 if cpu is not None else None, mem // (2**31) if mem is not None else None)]
>     |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ C416
> 314 |     usable = [max(bound, 1) for bound in bounds if bound is not None]
> 315 |     return min(usable) if usable else None
>     |
>     = help: Rewrite using `list()`
>
> scripts/verify_run.py:324:64: ARG001 Unused function argument: `gate`
>     |
> 323 | def gate_process(
> 324 |     root: Path, python: str, lock_slot: dict[str, int | None], gate: dict[str, Any], command: str, env: dict[str, str]
>     |                                                                ^^^^ ARG001
> 325 | ) -> GateProcess:
> 326 |     """The default executor's one gate: `sh -c` with the pinned interpreter substituted.
>     |
>
> tests/test_verify_cheap_first.py:901:61: ARG005 Unused lambda argument: `doc`
>     |
> 899 |     _write_gate_file(tree, [gate])
> 900 |     monkeypatch.setattr(ci_gates, "GATE_FILE", tree / "decisions" / "gates.yaml")
> 901 |     monkeypatch.setattr(ci_gates, "validate_schema", lambda doc: [])
>     |                                                             ^^^ ARG005
> 902 |     assert ci_gates.gates()[0]["cost"] == "seconds"
> 903 |     del gate["cost"]
>     |
>
> Found 7 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-13: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1049 files, 4147 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-cheap-before-admission/plan.md` +16 -16
> - `plans/changes/verify-cheap-before-admission/spec.md` +1 -1
> - `scripts/stage2.py` +5 -5
> - `scripts/verify_run.py` +4 -4
> - `tests/test_verify_before_admission.py` +65 -0
> - `tests/test_verify_cheap_first.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>             },
>         )
>         datei.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
>         git(world.root, "add", "-A")
>         git(world.root, "commit", "--quiet", "-m", "a slow cheap gate joins the verify job")
>     
>         ready = world.state / "holder-ready-budget"
>         holder = _real_holder(ready, seconds=30.0)
>         deadlines: list[float] = []
>         waits: list[float] = []
>         real_launch = stage2.launch
>         real_hold = stage2.verify_lock.hold_admission
>     
>         def launch(command, root, env, *rest, **kwargs):
>             if command[1:2] == ["-c"]:
>                 deadlines.append(kwargs.get("deadline"))
>             return real_launch(command, root, env, *rest, **kwargs)
>     
>         def hold_admission(command):
>             entered = time.monotonic()
>             try:
>                 return real_hold(command)
>             finally:
>                 waits.append(time.monotonic() - entered)
>     
>         def release_when_queued() -> None:
>             # The cheap gate's marker proves the scheduler is past the cheap phase; the admission entry
>             # follows within milliseconds, so half a second later the run is waiting in the queue.
>             deadline = time.monotonic() + 60
>             while time.monotonic() < deadline and not marker.exists():
>                 time.sleep(0.02)
>             time.sleep(0.5)
>             holder.terminate()
>     
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 30.0)
>         monkeypatch.setattr(stage2, "launch", launch)
>         monkeypatch.setattr(stage2.verify_lock, "hold_admission", hold_admission)
>         releaser = threading.Thread(target=release_when_queued)
>         releaser.start()
>         try:
>             _holder_acquired(ready)
>             successful_implementation(world)
> >           assert world.run("implement") == 0, "the queue wait starved the shared allowance"
> E           AssertionError: the queue wait starved the shared allowance
> E           assert 1 == 0
> E            +  where 1 = run('implement')
> E            +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-138/popen-gw4...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-138/popen-gw4/test_before_admission_executio0/state')).run
>
> tests/test_stage2.py:2575: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 32 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: claude call failed: the answer is empty; the attempt is saved at refs/stage2/attempts/demo/implement-attempt-2-20261113T221202405781Z (42ca4c609efe); `git diff 845a193c17ac refs/stage2/attempts/demo/implement-attempt-2-20261113T221202405781Z` shows it; the runner restored the worktree to 845a193c17ac (undone: plans/INDEX.md, plans/changes/demo/plan.md, src/app.py); rerun the verb or add --stage2-off.
> =========================== short test summary info ============================
> FAILED tests/test_verify_cheap_first.py::test_gate_frame_uses_declared_interpreter_without_absolute_path
> FAILED tests/test_verify_cheap_first.py::test_multiple_cheap_failures_keep_parser_frames
> FAILED tests/test_ci.py::test_duration_storage_failure_warns_without_changing_verdict
> FAILED tests/test_ci.py::test_guarded_runner_preserves_gate_verdicts_and_ci_selection
> FAILED tests/test_ci.py::test_timing_preserves_job_selection_enforcement_and_nested_admission
> FAILED tests/test_ci.py::test_runner_report_keeps_gate_verdict - AssertionErr...
> FAILED tests/test_ci.py::test_runner_report_matches_selected_job - AssertionE...
> FAILED tests/test_ci.py::test_runner_worker_default_preserves_gate_verdicts
> FAILED tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout
> FAILED tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
> FAILED tests/test_stage2.py::test_before_admission_execution_budget_is_shared_and_wait_free
> ERROR tests/test_verify_before_admission.py::test_seconds_only_jobs_never_request_admission
> ERROR tests/test_verify_before_admission.py::test_changed_tree_refreshes_selection_and_rechecks
> ERROR tests/test_verify_before_admission.py::test_unmeasurable_inputs_refuse_reuse
> ERROR tests/test_verify_before_admission.py::test_all_cheap_failures_finish_without_queueing
> ERROR tests/test_verify_before_admission.py::test_unchanged_tree_reuses_cheap_results
> ERROR tests/test_verify_before_admission.py::test_two_phases_share_history_and_exclude_wait
> ERROR tests/test_verify_before_admission.py::test_enforcement_and_ci_exhaustiveness_survive_partitioning
> ERROR tests/test_verify_before_admission.py::test_only_protected_work_enters_one_admission
> ERROR tests/test_verify_before_admission.py::test_nested_refused_and_interrupted_protected_work
> ERROR tests/test_verify_before_admission.py::test_transferred_kit_keeps_before_admission_behavior
> ERROR tests/test_verify_before_admission.py::test_admission_metadata_is_validated_and_cost_derived
> 11 failed, 10 passed, 11 errors in 65.83s (0:01:05)
> ```

Stage-2 call, 2026-11-13: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1049 files, 4151 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1049 files, 4180 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1065 files, 4187 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/governance/gate-catalog.md` +5 -4
> - `docs/how-it-works.md` +2 -1
> - `docs/testing.md` +2 -2
> - `scripts/stage2.py` +29 -20
> - `scripts/verify_all.sh` +2 -2
> - `scripts/verify_duration.py` +11 -4
> - `scripts/verify_run.py` +42 -19
> - `tests/test_stage2.py` +83 -6
> - `tests/test_verify_before_admission.py` +49 -0
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-cheap-before-admission/plan.md, plans/changes/verify-cheap-before-admission/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 86 lines of this gate left out …]
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-before-admission/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-430/popen-gw4...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-430/popen-gw4/test_the_runner_steps_carry_th0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10cd17a70>
>
>     def test_the_runner_steps_carry_their_limits_at_the_call_sites(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
>         """O188-1, R-20 at the call sites: renderer and ruff get the tool limit, `make verify` the step limit."""
>         ruff = world.root / ".venv" / "bin" / "ruff"
>         ruff.parent.mkdir(parents=True, exist_ok=True)
>         if ruff.is_symlink():
>             # The fixture installed the stand-in link; this test wants a plain file in its place.
>             ruff.unlink()
>         ruff.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
>         ruff.chmod(0o755)
>         (world.root / "scripts" / "extra.py").write_text("value = 1\n", encoding="utf-8")
>         world.script(make=[{"stdout": "green\n"}])
>         with world.plan.open("a", encoding="utf-8") as handle:
>             handle.write("2026-10-07 10:00–10:05, 5 min\n")
>         seen: list[tuple[str, float | None, str | None]] = []
>         original = stage2.launch
>     
>         def record(command, root, env, secret=None, timeout=None, limit=None, **kwargs):
>             # The stem, not the file name: the mutation ratchet in test_ci.py reads a
>             # gate script's file name as mutation evidence, and this test seeds no
>             # fault into the renderer (maintainer, 2026-10-21; stricter ratchet: bead).
>             name = "renderer" if Path(command[-2]).stem == "plans_registry" else Path(command[0]).name
>             seen.append((name, timeout, limit))
>             return original(command, root, env, secret, timeout=timeout, limit=limit, **kwargs)
>     
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 7 * 60)
>         monkeypatch.setattr(stage2, "launch", record)
>         assert stage2.verify_attempt(world.root, world.plan, None, None, stage2.tool_state(world.root)) == []
>         assert ("renderer", stage2.TOOL_SECONDS, "the runner's tool limit after 5 minutes") in seen
>         assert ("ruff", stage2.TOOL_SECONDS, "the runner's tool limit after 5 minutes") in seen
> >       assert ("make", 7 * 60, "the runner's step limit after 7 minutes") in seen
> E       assert ('make', 420, "the runner's step limit after 7 minutes") in [('ruff', 300, "the runner's tool limit after 5 minutes"), ('ruff', 300, "the runner's tool limit after 5 minutes"), (...the runner's tool limit after 5 minutes"), ('bash', 419.9548561660049, "the runner's step limit after 7 minutes"), ...]
>
> tests/test_stage2.py:6908: AssertionError
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=81146) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-before-admission/tests/test_stage2.py:22754: DeprecationWarning: This process (pid=81141) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_the_runner_steps_carry_their_limits_at_the_call_sites
> 1 failed, 5791 passed, 17 skipped, 5 warnings in 856.68s (0:14:16)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 42587 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-cheap-before-admission/stage2/attempts/verify-cheap-before-admission/attempt-1-20261114T164345619628Z-08d6aa35.md
> ````

Stage-2 call, 2026-11-14: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 1065 files, 4198 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/governance/gate-catalog.md` +3 -2
> - `tests/test_stage2.py` +6 -1
> - `tests/test_verify_before_admission.py` +34 -8
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/verify-cheap-before-admission/plan.md, plans/changes/verify-cheap-before-admission/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - L1-7: no fixed line
> - L1-10: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-cheap-before-admission/stage2/attempts/verify-cheap-before-admission/attempt-2-20261114T164345619628Z-08d6aa35.md
> ```

Stage-2 call, 2026-11-14: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1065 files, 4213 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/verify-cheap-before-admission/plan.md, plans/changes/verify-cheap-before-admission/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-cheap-before-admission/stage2/attempts/verify-cheap-before-admission/attempt-3-20261114T164345619628Z-08d6aa35.md
> ```
