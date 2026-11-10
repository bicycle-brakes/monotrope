---
title: "Findings — central-config"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
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
