---
title: "Findings — pi-pin"
category: findings
status: draft
implementation_status: none
date: 2026-10-15
created: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-agx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — pi-pin

Stage-2 call, 2026-10-15: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 441 files, 1261 commits, 12 rules.

ADR answer owed: decisions/answers/pi-pin/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).

Stage-2 call, 2026-10-15: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 447 files, 1264 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +16 -0
> - `.gitignore` +5 -0
> - `docs/WORKFLOW.md` +24 -8
> - `model-endpoints.yaml` +2 -1
> - `plans/changes/pi-pin/plan.md` +25 -16
> - `scripts/ci_gates.py` +14 -3
> - `scripts/stage2.py` +56 -18
> - `scripts/stage2_session.py` +17 -5
> - `scripts/stage2_session_policy.mjs` +8 -3
> - `tests/pi_contract_driver.mjs` +110 -0
> - `tests/pi_network_guard.mjs` +63 -0
> - `tests/test_ci.py` +33 -0
> - `tests/test_pi_contract.py` +781 -0
> - `tests/test_pi_install.py` +531 -0
> - `tests/test_stage2.py` +69 -12
> - `tests/test_stage2_session.py` +31 -6
> - `tools/pi/.node-version` +1 -0
> - `tools/pi/README.md` +74 -0
> - `tools/pi/install.sh` +41 -0
> - `tools/pi/package.json` +10 -0
> - `tools/pi/pi` +57 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `tests/test_ci.py`, `tests/test_pi_contract.py`, `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1854 lines of this gate left out …]
>     def test_real_pi_is_provisioned_before_contracts() -> None:
>         """Criterion 12 (pi-pin): both toolchain jobs set up the exact declared Node and install the locked Pi with the shared installer, before pytest runs.
>     
>         Planted faults: dropping the Node step, duplicating the runtime version as a
>         literal, a job-local installer instead of `tools/pi/install.sh`, or letting
>         the install fail softly — each turned this red.
>         """
>         declared_node = (REPO_ROOT / "tools" / "pi" / ".node-version").read_text(encoding="utf-8").strip()
>         assert re.fullmatch(r"\d+\.\d+\.\d+", declared_node), "the Node runtime declaration is not an exact version"
>         checked = 0
>         for name, job in _ci_doc()["jobs"].items():
>             if _install_index(job) is None:
>                 continue
>             checked += 1
>             steps = job["steps"]
>             node = next((step for step in steps if step.get("id") == "setup-node"), None)
>             assert node is not None, f"{name}: no declared Node runtime is set up"
>             assert node["uses"] == "actions/setup-node@v4", f"{name}: the Node runtime comes from {node.get('uses')!r}"
>             assert node["with"]["node-version-file"] == "tools/pi/.node-version", (
>                 f"{name}: the runtime is not read from the repository's declaration"
>             )
>             assert "if" not in node and "continue-on-error" not in node, f"{name}: the Node setup can fail softly"
>             pi = next((step for step in steps if step.get("id") == "setup-pi"), None)
>             assert pi is not None, f"{name}: the pinned Pi is not installed"
>             assert pi["run"] == "bash tools/pi/install.sh", (
>                 f"{name}: the installer is {pi.get('run')!r}, not the shared one"
>             )
>             assert "if" not in pi and "continue-on-error" not in pi, f"{name}: the Pi install can fail softly"
> >           first_gate = next(
>                 index for index, step in enumerate(steps) if "scripts/ramp_valves.py" in str(step.get("run", ""))
>             )
> E           StopIteration
>
> tests/test_ci.py:854: StopIteration
> ________________ test_the_opencode_go_remark_names_every_source ________________
>
>     def test_the_opencode_go_remark_names_every_source() -> None:
>         """Criterion 2: the remark says what OpenCode states, with its source and date."""
>         remark = _endpunkt("opencode-go")["bemerkung"]
> >       assert opencode_remark_problems(remark) == []
> E       AssertionError: assert ['Pi at the v... runner pins'] == []
> E         
> E         Left contains one more item: 'Pi at the version the runner pins'
> E         Use -v to get more diff
>
> tests/test_model_endpoints.py:387: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_real_pi_is_provisioned_before_contracts - StopI...
> FAILED tests/test_model_endpoints.py::test_the_opencode_go_remark_names_every_source
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_extension_tool_input_and_result - ...
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory
> 2 failed, 2090 passed, 16 skipped, 7 errors in 443.88s (0:07:23)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> tests/test_pi_contract.py:760:50: ARG005 Unused lambda argument: `args`
>     |
> 758 |         pytest.raises(pytest.fail.Exception, match="not installed or will not start"),
> 759 |     ):
> 760 |         quiet.setattr(subprocess, "run", lambda *args, **kwargs: Off())
>     |                                                  ^^^^ ARG005
> 761 |         require_installed_pi()
>     |
>
> tests/test_pi_contract.py:760:58: ARG005 Unused lambda argument: `kwargs`
>     |
> 758 |         pytest.raises(pytest.fail.Exception, match="not installed or will not start"),
> 759 |     ):
> 760 |         quiet.setattr(subprocess, "run", lambda *args, **kwargs: Off())
>     |                                                          ^^^^^^ ARG005
> 761 |         require_installed_pi()
>     |
>
> Found 2 errors.
> ── [ruff-check] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 1 rote(r) Fall/Faelle ohne deklarierten Grund
>       tests.test_ci::test_real_pi_is_provisioned_before_contracts
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 1006 von 1045 Faellen tragen in ein fremdes Repo (96 %)
>       mechanismus 85 · bestand 362 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 10176 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
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
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-15: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 456 files, 1265 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `model-endpoints.yaml` +3 -2
> - `plans/changes/pi-pin/plan.md` +20 -16
> - `tests/test_ci.py` +13 -2
> - `tests/test_pi_contract.py` +1 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `tests/test_ci.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1803 lines of this gate left out …]
>                 if err_filename is not None:
> >                   raise child_exception_type(errno_num, err_msg, err_filename)
> E                   PermissionError: [Errno 13] Permission denied: '/Users/mikypiky/coding-harness/.claude/worktrees/pi-pin/tools/pi/pi'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py:1955: PermissionError
>
> During handling of the above exception, another exception occurred:
>
>     @pytest.fixture(scope="module")
>     def installed_pi() -> str:
>         """The suite's mandatory prerequisite, checked once: the pinned install answers."""
> >       return require_installed_pi()
>
> tests/test_pi_contract.py:115: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
>     def require_installed_pi() -> str:
>         """Fail the run - never skip - when the pinned Pi or its Node is missing (spec, criterion 12)."""
>         if shutil.which("node") is None:
>             pytest.fail(
>                 "the Pi contracts need Node (tools/pi/.node-version) on PATH; missing prerequisites fail, they do not skip"
>             )
>         wrapper = stage2.PI_WRAPPER
>         if not wrapper.is_file():
>             pytest.fail(f"the repository Pi wrapper {wrapper} is missing; run bash tools/pi/install.sh")
>         with tempfile.TemporaryDirectory(prefix="pi-contract-") as tmp:
>             env = {
>                 **os.environ,
>                 "HOME": tmp,
>                 "PI_CODING_AGENT_DIR": tmp,
>             }
>             try:
>                 done = subprocess.run(
>                     [str(wrapper), "--version"],
>                     cwd=tmp,
>                     env=env,
>                     stdin=subprocess.DEVNULL,
>                     capture_output=True,
>                     text=True,
>                     errors="replace",
>                     timeout=120,
>                     check=False,
>                 )
>             except (OSError, subprocess.TimeoutExpired) as error:
> >               pytest.fail(f"the pinned Pi {PIN} could not be checked ({error}); run bash tools/pi/install.sh")
> E               Failed: the pinned Pi 1.2.0 could not be checked ([Errno 13] Permission denied: '/Users/mikypiky/coding-harness/.claude/worktrees/pi-pin/tools/pi/pi'); run bash tools/pi/install.sh
>
> tests/test_pi_contract.py:102: Failed
> =========================== short test summary info ============================
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_extension_tool_input_and_result - ...
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory
> 2092 passed, 16 skipped, 7 errors in 478.20s (0:07:58)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 1 rote(r) Fall/Faelle ohne deklarierten Grund
>       tests.test_ci::test_real_pi_is_provisioned_before_contracts
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 1006 von 1045 Faellen tragen in ein fremdes Repo (96 %)
>       mechanismus 85 · bestand 362 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 10233 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
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
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-15: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 456 files, 1265 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/kit/probe.py` +5 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 1803 lines of this gate left out …]
>                 if err_filename is not None:
> >                   raise child_exception_type(errno_num, err_msg, err_filename)
> E                   PermissionError: [Errno 13] Permission denied: '/Users/mikypiky/coding-harness/.claude/worktrees/pi-pin/tools/pi/pi'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py:1955: PermissionError
>
> During handling of the above exception, another exception occurred:
>
>     @pytest.fixture(scope="module")
>     def installed_pi() -> str:
>         """The suite's mandatory prerequisite, checked once: the pinned install answers."""
> >       return require_installed_pi()
>
> tests/test_pi_contract.py:115: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
>     def require_installed_pi() -> str:
>         """Fail the run - never skip - when the pinned Pi or its Node is missing (spec, criterion 12)."""
>         if shutil.which("node") is None:
>             pytest.fail(
>                 "the Pi contracts need Node (tools/pi/.node-version) on PATH; missing prerequisites fail, they do not skip"
>             )
>         wrapper = stage2.PI_WRAPPER
>         if not wrapper.is_file():
>             pytest.fail(f"the repository Pi wrapper {wrapper} is missing; run bash tools/pi/install.sh")
>         with tempfile.TemporaryDirectory(prefix="pi-contract-") as tmp:
>             env = {
>                 **os.environ,
>                 "HOME": tmp,
>                 "PI_CODING_AGENT_DIR": tmp,
>             }
>             try:
>                 done = subprocess.run(
>                     [str(wrapper), "--version"],
>                     cwd=tmp,
>                     env=env,
>                     stdin=subprocess.DEVNULL,
>                     capture_output=True,
>                     text=True,
>                     errors="replace",
>                     timeout=120,
>                     check=False,
>                 )
>             except (OSError, subprocess.TimeoutExpired) as error:
> >               pytest.fail(f"the pinned Pi {PIN} could not be checked ({error}); run bash tools/pi/install.sh")
> E               Failed: the pinned Pi 1.2.0 could not be checked ([Errno 13] Permission denied: '/Users/mikypiky/coding-harness/.claude/worktrees/pi-pin/tools/pi/pi'); run bash tools/pi/install.sh
>
> tests/test_pi_contract.py:102: Failed
> =========================== short test summary info ============================
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_extension_tool_input_and_result - ...
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory
> 2092 passed, 16 skipped, 7 errors in 438.74s (0:07:18)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [criterion-ledger] $ lauf_cmd
> plans/changes/pi-pin/plan.md:120: criterion 1: "test_install_obeys_lock_integrity_and_disables_scripts" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:121: criterion 2: "test_wrapper_ignores_global_pi_from_any_cwd" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:122: criterion 3: "test_wrapper_refuses_unusable_local_pi" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:123: criterion 4: "test_wrapper_checks_node_major" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:124: criterion 5: "test_loop_and_probe_use_repository_pi" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:125: criterion 5: "test_all_session_pi_launches_use_repository_wrapper" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:126: criterion 6: "test_real_reviewer_tool_contract" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:127: criterion 7: "test_real_reviewer_ignores_discovery_traps" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:128: criterion 8: "test_real_extension_tool_input_and_result" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:129: criterion 9: "test_real_session_policy_blocks_foreign_reads" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:130: criterion 10: "test_real_model_listing_is_a_provider_table" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:131: criterion 11: "test_real_opencode_provider_contracts" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:132: criterion 11: "test_contract_network_guard_denies_external_destinations" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:133: criterion 12: "test_contract_prerequisites_and_failures_are_mandatory" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:134: criterion 12: "test_real_pi_is_provisioned_before_contracts" exists — remove `not yet written` from the entry
> plans/changes/pi-pin/plan.md:139: criterion 13: "test_truncated_pi_print_failure_is_refused" exists — remove `not yet written` from the entry
> ── [criterion-ledger] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 10285 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
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
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> - `plan.md` did not add a measured line below `## Time used`
> ````
