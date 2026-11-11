---
title: "Findings — central-config"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-twvx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — central-config

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 981 files, 3827 commits, 12 rules.

Stage-2 call, 2026-11-10: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 986 files, 3846 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +4 -0
> - `AGENTS.md` +1 -1
> - `config/harness/lanes.yaml` +1 -0
> - `decisions/gates.yaml` +10 -0
> - `docs/WORKFLOW.md` +24 -1
> - `docs/governance/gate-catalog.md` +2 -1
> - `plans/changes/central-config/plan.md` +11 -11
> - `prompts/04-implement.md` +3 -0
> - `provenance.yaml` +5 -0
> - `scripts/check_harness_config.py` +237 -0
> - `scripts/ci_gates.py` +5 -0
> - `scripts/export/manifest.yaml` +6 -0
> - `scripts/harness_config.py` +249 -0
> - `scripts/kit/manifest.yaml` +12 -0
> - `scripts/stage2.py` +41 -1
> - `tests/test_ci.py` +68 -0
> - `tests/test_harness_config.py` +296 -0
> - `tests/test_kit.py` +28 -0
> - `tests/test_stage2.py` +75 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/check_harness_config.py`, `scripts/harness_config.py`, `tests/test_harness_config.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/check_harness_config.py:122:47: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 120 | def _numeric_constant(node: ast.expr | None) -> bool:
> 121 |     """Whether the expression is a numeric literal; a Boolean is not a count."""
> 122 |     return isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool)
>     |                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
>     |
>     = help: Convert to `X | Y`
>
> scripts/harness_config.py:201:43: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 199 |             raise HarnessConfigError(None, f"{dotted}: unknown setting; known keys: {known}")
> 200 |         node = getattr(node, part)
> 201 |     if isinstance(node, BaseModel) or not isinstance(node, (int, str)):
>     |                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 202 |         raise HarnessConfigError(None, f"{dotted}: only a scalar value renders")
> 203 |     return node
>     |
>     = help: Convert to `X | Y`
>
> Found 2 errors.
> No fixes available (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-10: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 990 files, 3856 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +0 -4
> - `decisions/gates.yaml` +0 -10
> - `docs/governance/gate-catalog.md` +0 -1
> - `plans/changes/central-config/plan.md` +11 -11
> - `scripts/check_harness_config.py` +1 -1
> - `scripts/ci_gates.py` +5 -0
> - `scripts/harness_config.py` +1 -1
> - `tests/test_ci.py` +54 -28
> - `tests/test_harness_config.py` +7 -1
> - `tests/test_stage2.py` +13 -2
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_ci.py:3245:12: F821 Undefined name `in_job`
>      |
> 3243 |         "needs_history": False,
> 3244 |     }
> 3245 |     assert in_job(shape, "verify"), "the gate is not in the verify job"
>      |            ^^^^^^ F821
> 3246 |     assert in_job(shape, "docs"), "the gate is not in the draft verb's document subset"
> 3247 |     assert misst_in(shape, "lokal"), "the gate does not measure in local verification"
>      |
>
> tests/test_ci.py:3246:12: F821 Undefined name `in_job`
>      |
> 3244 |     }
> 3245 |     assert in_job(shape, "verify"), "the gate is not in the verify job"
> 3246 |     assert in_job(shape, "docs"), "the gate is not in the draft verb's document subset"
>      |            ^^^^^^ F821
> 3247 |     assert misst_in(shape, "lokal"), "the gate does not measure in local verification"
> 3248 |     assert misst_in(shape, "ci"), "the gate does not measure in hosted verification"
>      |
>
> Found 2 errors.
> ```

Stage-2 call, 2026-11-10: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 990 files, 3863 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_ci.py` +2 -2
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         step 6). Until then the test holds the planned declaration to the same schema,
>         selection and rendering rules every real gate goes through, and proves with the real
>         checker subprocess that an invalid configuration cannot pass it. The first assertion
>         turns red once the gate is registered, so the bootstrap folds these checks into
>         real-tree assertions instead of leaving two declarations of one gate.
>         """
>         document = yaml.safe_load(ci_gates.GATE_FILE.read_text(encoding="utf-8"))
>         assert all(g["id"] != CENTRAL_GATE_ID for g in document["gates"]), (
>             "the harness-config gate is registered; fold this test into real-tree assertions (plan, step 6)"
>         )
>         raw = {
>             "id": CENTRAL_GATE_ID,
>             "title": "The central harness configuration and its bindings hold",
>             "command": f"python3 {CENTRAL_GATE_SCRIPT} --check",
>             "job": "verify",
>             "enforcement": "block",
>             "floor": False,
>             "placement": "both",
>             "subsets": ["docs"],
>             "reason": (
>                 "One validated source for each migrated harness setting (ADR 0026): invalid data is "
>                 "refused, the marked prose and the prompt placeholder must state the configured value, "
>                 "and no live script may redeclare an owned setting."
>             ),
>         }
>         document["gates"].append(raw)
>         assert ci_gates.validate_schema(document) == [], "the planned harness-config declaration is not schema-valid"
>     
>         shape = {
>             "id": raw["id"],
>             "name": raw["title"],
>             "job": raw["job"],
>             "command": raw["command"],
>             "action": None,
>             "with": {},
>             "enforcement": raw["enforcement"],
>             "floor": raw["floor"],
>             "placement": raw["placement"],
>             "subsets": raw["subsets"],
>             "needs_tracker": False,
>             "needs_history": False,
>         }
>         assert ci_gates.in_job(shape, "verify"), "the gate is not in the verify job"
>         assert ci_gates.in_job(shape, "docs"), "the gate is not in the draft verb's document subset"
>         assert misst_in(shape, "lokal"), "the gate does not measure in local verification"
>         assert misst_in(shape, "ci"), "the gate does not measure in hosted verification"
>         assert ci_gates._schritt(shape) == [
>             "      - name: The central harness configuration and its bindings hold",
>             "        id: harness-config",
>             "        if: ${{ !cancelled() }}",
>             "        run: python3 scripts/check_harness_config.py --check",
>         ], "the gate does not render as a blocking step of the generated verify job"
>     
>         (tmp_path / "config" / "harness").mkdir(parents=True)
>         lanes = tmp_path / "config" / "harness" / "lanes.yaml"
>         lanes.write_text("writing_sessions_per_repository: 0\n", encoding="utf-8")
>         broken = _central_checker(tmp_path)
>         assert broken.returncode != 0, "invalid configuration or a missing binding passed the checker"
>         assert "lanes.yaml" in broken.stdout + broken.stderr, "the refusal does not name the file"
>     
>         (tmp_path / "prompts").mkdir()
>         (tmp_path / "prompts" / "04-implement.md").write_text(
>             "limit {{ harness.lanes.writing_sessions_per_repository }}\n", encoding="utf-8"
>         )
>         (tmp_path / "AGENTS.md").write_text(
>             "at most <!-- harness-config: lanes.writing_sessions_per_repository -->2<!-- /harness-config --> sessions\n",
>             encoding="utf-8",
>         )
>         (tmp_path / "scripts").mkdir()
>         green = _central_checker(tmp_path)
> >       assert green.returncode == 0, f"measured agreement failed: {green.stdout + green.stderr}"
> E       AssertionError: measured agreement failed: /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1784/popen-gw0/test_central_config_gate_block0/config/harness/lanes.yaml: writing_sessions_per_repository: Input should be greater than 0
> E         
> E       assert 3 == 0
> E        +  where 3 = CompletedProcess(args=['/Users/mikypiky/coding-harness/.claude/worktrees/central-config/.venv/bin/python3', '/Users/mi...ntral_config_gate_block0/config/harness/lanes.yaml: writing_sessions_per_repository: Input should be greater than 0\n').returncode
>
> tests/test_ci.py:3273: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_central_config_gate_blocks_locally_and_in_generated_ci
> 1 failed, 13 passed in 13.48s
> ```

Stage-2 call, 2026-11-10: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason three attempts failed on 2026-11-10; one more attempt from the kept tree on the maintainer's instruction to give every lane a task · leak check clean over 990 files, 3887 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_ci.py` +1 -0
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 2824 lines of this gate left out …]
> INFO  (1):
>   - leak check clean: 34 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 34 files, 3 commits, 1 rules, 1 prompt texts
> repair: the attempt's protected answer is saved at /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1870/popen-gw2/test_repair_prompts_keep_the_i5/repo/.git/stage2/attempts/demo/attempt-3-20261111T001842213959Z-4d392c98.md
> repair: verified and committed · route stage-1 · attempt 3
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=31091) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/central-config/tests/test_stage2.py:20418: DeprecationWarning: This process (pid=31097) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_kit.py::test_the_kit_does_not_describe_the_phases - Asserti...
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[spec-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[spec-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[plan-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[plan-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[decisions-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[decisions-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[design-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[design-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[phase-prompt-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[phase-prompt-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[agent-rules-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[agent-rules-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[all-inputs-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[all-inputs-2]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[phase-prompt-first]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[phase-prompt-second]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[phase-prompt-both]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[all-inputs-first]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[all-inputs-second]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[all-inputs-both]
> FAILED tests/test_stage2.py::test_repair_prompts_keep_the_initial_input_snapshot[phase-prompt-1]
> FAILED tests/test_stage2.py::test_repair_prompts_keep_the_initial_input_snapshot[phase-prompt-2]
> 23 failed, 5231 passed, 17 skipped, 5 warnings in 1347.42s (0:22:27)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 1 red case(s) without a declared reason
>       tests.test_kit::test_the_kit_does_not_describe_the_phases
>       
>       Add them with: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 1384 of 1429 cases carry into a foreign repository (96 %)
>       mechanismus 117 · bestand 873 file(s)
>
> BLOCK (1), repeated last:
>   - 1 red case(s) without a declared reason
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35614 earlier lines left out …]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````
