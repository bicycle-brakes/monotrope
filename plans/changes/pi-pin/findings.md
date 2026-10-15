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

## Phase 6 — Opus 5.5, 2026-10-15

Orchestrator's decision on each row below (2026-10-15): every BLOCKER and MAJOR is taken; MINOR rows on tests, security and false statements are taken; the one STYLE row is taken because it is a false statement. Each taken row names the criterion or test the repair must satisfy. The review text itself is committed unchanged below the table.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `tests/test_pi_contract.py:466-537`; `tests/test_pi_contract.py:479`; `tests/pi_contract_driver.mjs` | Criterion 7's trap test cannot fail for most trap types. The extension trap is a `.mjs` file, and Pi auto-discovers only `.ts` and `.js` (`core/package-manager.js:444`). Without isolation flags, print mode treats the project as untrusted and loads none of its `.pi/` resources, so removing `--no-extensions`, `--no-mcp`, `--no-skills`, `--no-prompt-templates` or `--no-themes` would leave the test green. `.pi/auth.json` and `.pi/agent/models.json` are never read (`config.js:503-508`). No assertion covers the skill, prompt-template or theme traps, and the positive controls run plain node, not Pi. Only the AGENTS.md context-file trap tests real behaviour. | Opus 5.5 | taken — criterion 7: `test_real_reviewer_ignores_discovery_traps`; fixed: the traps are a `.js` extension, a skill, a prompt template, a theme and an MCP entry; each fires through real Pi when its flag is removed (the positive controls start Pi, and a preload records real reads); the inert `auth.json` and `models.json` traps are gone | no |
| F-2 | MAJOR | SPEC | base | `tests/test_pi_contract.py:396-401`; `tests/test_pi_contract.py:683-688` | The native-address check reads only the `openai-completions` section of the installed catalog, and nothing ties the runner's ladder models to that section. In the installed catalog `opencode-go` lists `https://opencode.ai/zen/go` under `anthropic-messages`, and `opencode` lists `https://opencode.ai/zen`. The three ladder ids in `model-endpoints.yaml` are in `openai-completions` today. A future Pi could move one and the test would stay green (criterion 11: a wrong native address or key mapping). | Opus 5.5 | taken — criterion 11: `test_real_opencode_provider_contracts`; fixed: every ladder model of `opencode-go` is asserted in the `openai-completions` section whose base URL is checked | no |
| F-3 | MAJOR | SPEC | base | `tests/test_stage2.py:3644-3651` | Two existing pin-check guards lost their power. "non-zero" and "too-slow" now print the off-pin version, so the version mismatch alone causes the refusal: a runner that ignored the exit code or the timeout would still pass. The case "newer" now carries `1.2.0-rc1`, which is not newer. | Opus 5.5 | taken — criterion 3: `test_a_pi_off_the_pin_is_refused`; fixed: the non-zero and too-slow cases use `stage2.PI_VERSION`, so only the exit code or the timeout refuses; `newer` uses 999.0.0; red first is not possible because the runner already refuses correctly | no |
| F-4 | MAJOR | SPEC | base | `tests/test_pi_install.py:79-130`; `tests/test_pi_install.py:339-375` | Criterion 1's refusals (lock mismatch, integrity error) come from a synthetic npm written to refuse. Real `npm ci` is never run against a broken lock. The subject `install.sh` is real, but the refusal evidence is not. An offline check with real npm and a `file:` fixture is possible. | Opus 5.5 | taken — criterion 1: `test_install_obeys_lock_integrity_and_disables_scripts`; fixed: real `npm ci` runs offline over a local tarball and an empty cache, and npm itself refuses a manifest dependency missing from the lock; red first is not possible because the installer already refuses correctly | no |
| F-5 | MINOR | TEST | base | `tests/test_pi_contract.py:9-11`; `tests/test_pi_contract.py:317-318`; `tests/test_pi_contract.py:404-414` | Two docstrings say no second flag list exists, but `REVIEWER_FLAGS` is one: a hand-written list without `--no-context-files`, against plan step 5 (no second handwritten isolation-flag list). | Opus 5.5 | taken — not a test: `REVIEWER_FLAGS` is captured from the production `run_reviewer` call, so no second flag list exists; both docstrings are corrected | no |
| F-6 | MINOR | DOC | base | `docs/WORKFLOW.md:871-878`; `docs/adr/0019-repository-pinned-pi-and-contract-tests.md:74-78`; `tools/pi/README.md:59-61` | The docs say the suite measures discovery isolation, which F-1 disproves (criterion 14: unsupported safety claim). `docs/WORKFLOW.md:871-873` also says no test has run a real program to see its isolation take effect, and the next sentence contradicts it. | Opus 5.5 | taken — not a test: `docs/WORKFLOW.md`, `tools/pi/README.md` and ADR 0019 item 4 name only what the suite measures; the ADR text change is named in the decision pull request | no |
| F-7 | MINOR | TEST | base | `tests/test_pi_contract.py:644-645` | The symlink read's refusal is not checked on its own. `requests[3]` carries the whole conversation, so the phrase "outside the worktree" from the `../outside` refusal already satisfies the assertion; the symlink read could fail for another reason and still pass. | Opus 5.5 | taken — criterion 9: `test_real_session_policy_blocks_foreign_reads`; fixed: the symlink refusal is checked on its own tool result, separately from the `../outside` refusal | no |
| F-8 | MINOR | TEST | base | `tests/test_stage2.py:3693-3708` | Criterion 13's truncated-print test uses a stand-in that exits 1. Whether real Pi 1.2.0 exits non-zero on a truncated print is not measured; no contract sends `finish_reason: "length"`. | Opus 5.5 | taken — criterion 13: `test_real_truncated_pi_print_failure_is_refused`; fixed: a real-Pi contract sends `finish_reason: length`; measured on Pi 1.2.0: exit 0 with empty stdout, refused by the empty-answer guard | no |
| F-9 | MINOR | TEST | base | `scripts/stage2.py:181` | No test pins `PI_WRAPPER` to `REPO_ROOT/tools/pi/pi`. Every runner test monkeypatches it, and the contract tests accept whatever it points to if it prints 1.2.0, so a global Pi 1.2.0 would pass. | Opus 5.5 | taken — criterion 2: `test_pi_wrapper_is_repository_local`; fixed: `PI_WRAPPER` must be exactly `REPO_ROOT/tools/pi/pi` | no |
| F-10 | MINOR | SECURITY | base | `tests/test_pi_contract.py:287-294` | `run_pi` passes the whole parent environment to real Pi, including any real provider keys in the maintainer's shell. The network guard and the overridden `OPENCODE_API_KEY` stop real calls, but keys should not reach the contract run at all. | Opus 5.5 | taken — criterion 10: `test_contract_environment_excludes_parent_provider_keys`; fixed: `contract_environment()` passes only PATH, LANG, LC_ALL, LC_CTYPE and TZ to Pi | no |
| F-11 | MINOR | SCOPE | base | `decisions/gates.yaml:217-223`; `.github/workflows/ci.yml:61-68` | markdownlint now also scans `tools/pi/node_modules/` (278 third-party `.md` files, counted 2026-10-15). The gate is report-only, but the noise can hide findings in this change's own Markdown. | Opus 5.5 | taken — not a test: `decisions/gates.yaml` and `.github/workflows/ci.yml` exclude `tools/pi/node_modules/` from the markdownlint globs; this deviates from plan step 7 and is named in the pull request | no |
| F-12 | MINOR | SCOPE | base | `scripts/ci_gates.py:455-462`; `scripts/kit/manifest.yaml:76`; `.github/workflows/ci.yml:133` | The generator, which travels with the kit, now always emits the `setup-node` step and `bash tools/pi/install.sh`. `tools/` stays behind in the kit (`manifest.yaml:329`), so a repository built from the kit gets CI steps it cannot run. | Opus 5.5 | taken — not a test: `scripts/ci_gates.py` adds the Pi steps only where `tools/pi/` exists; `test_pi_provisioning_only_in_repositories_with_pi` covers both cases | no |
| F-13 | MINOR | SCOPE | base | `scripts/kit/probe.py:101`; `scripts/kit/probe.py:190-193`; `plans/changes/pi-pin/plan.md:112-113` | `plan.md` says all created or changed files are named above, but `scripts/kit/probe.py` is not named. The edit adds a `REIST_NICHT` entry and raises the `DECKEL` cap from 38 to 39, with a reason. | Opus 5.5 | taken — not a test: `plans/changes/pi-pin/plan.md` names `scripts/kit/probe.py`, the `REIST_NICHT` entry and the `DECKEL` change from 38 to 39 | no |
| F-14 | STYLE | DOC | base | `scripts/stage2.py:24` | The module docstring still says each round checks `pi --version`; it is now the wrapper. | Opus 5.5 | taken — not a test: the module docstring of `scripts/stage2.py` names `tools/pi/pi` | no |

Review text as returned by the Opus 5.5 reviewer (committed unchanged; the reviewer's own indentation removed, nothing else changed):

Open BLOCKER: yes — BLOCKER 1 · DIVERGENT 0 · MAJOR 3 · MINOR 9 · STYLE 1 (review of explore/pi-pin at f071a51, 2026-10-15)

## Check 1 — the three repaired assertions (none was changed to match output)
Commit 58614f8 names the three repairs. The earlier versions of the file are gone: there are no unreachable blobs and no copies on disk. So I judged each repair against the spec text.
- Repair 1, the extension driver signature (tests/pi_contract_driver.mjs:44-52). It now follows the declared API, `execute(toolCallId, params, signal, onUpdate, ctx)` in `pi-coding-agent/dist/core/extensions/types.d.ts:514`. The expected values did not change: the input must equal the requested input, and the echo result must reach the model (test_pi_contract.py:580, :585). This does not violate the spec.
- Repair 2, the listing by exact provider id (test_pi_contract.py:666-670). The expected ids `opencode-go` and `opencode` are the spec's own words (criterion 10). I ran the real Pi listing: its header row is `provider model …`, so the header assertion matches what Pi prints. This does not violate the spec.
- Repair 3, the native addresses read from the installed catalog (test_pi_contract.py:379-401, :683-688). The expected values GO_NATIVE and ZEN_NATIVE equal the spec text. The scope was narrowed, though; see the MAJOR row below. This is not a BLOCKER.

## Findings
[BLOCKER] tests/test_pi_contract.py:466-537 — Criterion 7's trap test cannot fail for most trap types, so it gives no real evidence for the extension, MCP, skill, prompt-template, theme, saved-auth and command-config parts — spec: "Refuted by: a planted extension, MCP server, skill, context file, prompt template, theme, saved authentication or command-valued configuration marker being loaded…". Plan step 6 also asks for "ambient discovery/config traps with positive activation controls". Measured on the pinned Pi 1.2.0 in scratch directories:
  - (a) The extension trap is `.pi/extensions/trap-extension.mjs` (:479). Pi only auto-discovers `.ts` and `.js` files (`core/package-manager.js:444`). A `.mjs` trap did not fire even with `--approve`; the same trap as `.js` fired with `--approve`.
  - (b) Without any isolation flag, print mode treats the project as untrusted. Untrusted projects get none of their `.pi/` resources loaded (`core/project-trust.js`, `core/trust-manager.js:8-17`; a `.js` trap did not fire with no flags). So removing `--no-extensions`, `--no-mcp`, `--no-skills`, `--no-prompt-templates` or `--no-themes` from the runner would leave this test green.
  - (c) `.pi/auth.json` and `.pi/agent/models.json` inside the project are paths Pi never reads: auth and models come only from the agent directory (`config.js:503-508`). Those two traps are inert in every configuration.
  - (d) Nothing asserts that TRAP-SKILL-TEXT, TRAP-PROMPT-TEXT or the theme stayed out.
  - (e) The "positive controls" (:501-514) run the trap with plain `node` and `touch`, never through Pi.
  - Only the AGENTS.md context-file trap can tell a pass from a failure.
  - Verdict: CONFIRMED (measured).

[MAJOR] tests/test_pi_contract.py:396-401, :683-688 — The native-address check now reads only the `openai-completions` section of the catalog, and nothing ties the runner's ladder models to that section — evidence: in the installed catalog, `opencode-go` lists `https://opencode.ai/zen/go` for `anthropic-messages`, and `opencode` lists `https://opencode.ai/zen`. The three ladder ids in model-endpoints.yaml (deepseek-v4.1-flash, mimo-v2.6-flash, mimo-v2.6-pro) are in `openai-completions` today (measured). If a future Pi moves one of them, this test stays green. Spec criterion 11 is refuted by "a wrong native address/key mapping". Repair: assert that every `modelle` id of `opencode-go` sits in the section whose baseUrl is checked — CONFIRMED.

[MAJOR] tests/test_stage2.py:3644-3651 — Two existing pin-check guards lost their power — evidence: on main, "non-zero" and "too-slow" printed the pinned version with exit 1 or a 30 s sleep. They now print OFF_PIN, so the version mismatch alone causes the refusal: a runner that ignored the exit code or the timeout would still pass. The case with id "newer" now carries `1.2.0-rc1`, which is not newer. No other test sets `pi_version_exit` or `pi_version_sleep`. Repair: use `stage2.PI_VERSION` for those two cases, and a real higher version for "newer" — CONFIRMED.

[MAJOR] tests/test_pi_install.py:79-130, :339-375 — Criterion 1's refusals (lock mismatch, integrity error) come from a synthetic npm that is written to refuse; real `npm ci` is never run against a broken lock — evidence: the synthetic npm "refuse(... not in sync)" and an integrity check by regex only. The plan (step 4) accepted fixtures, and the subject `install.sh` is real. Real npm runs only on the happy path, in CI (not read: no CI run of this branch exists). An offline real-npm check with a `file:` fixture is possible — PLAUSIBLE.

[MINOR] tests/test_pi_contract.py:9-11, :317-318 vs :404-414 — Two docstrings say no second flag list exists, but `REVIEWER_FLAGS` is exactly that — a hand-written list, without `--no-context-files`, against plan step 5 ("do not maintain a second handwritten isolation-flag list"). Criteria 8, 11 and 12 use it, not 6 and 7 — CONFIRMED.

[MINOR] docs/WORKFLOW.md:871-878, docs/adr/0019-repository-pinned-pi-and-contract-tests.md:74-78, tools/pi/README.md:59-61 — The docs say the suite "measures … the discovery isolation", which the BLOCKER above disproves (criterion 14: "unsupported safety/compatibility claim"). WORKFLOW.md:871-873 also still says "no test has run a real program to see them take effect", and the next sentence now contradicts it — CONFIRMED.

[MINOR] tests/test_pi_contract.py:644-645 — The symlink read's refusal is not checked on its own. requests[3] carries the whole conversation, so the phrase "outside the worktree" from the `../outside` refusal already satisfies the assertion. The symlink read could fail for another reason and still pass, though the check that the sentinel never leaks does hold (:641-643) — CONFIRMED.

[MINOR] tests/test_stage2.py:3693-3708 — Criterion 13's truncated-print test uses a stand-in that exits 1. Whether real Pi 1.2.0 really exits non-zero on a truncated print is not measured: no contract sends `finish_reason: "length"` — CONFIRMED.

[MINOR] scripts/stage2.py:181 — No test pins `PI_WRAPPER` to `REPO_ROOT/tools/pi/pi`. Every runner test monkeypatches it, and the contract tests accept whatever it points to if it prints 1.2.0, so a global Pi 1.2.0 would pass — CONFIRMED.

[MINOR] tests/test_pi_contract.py:287-294 — `run_pi` passes the whole parent environment to real Pi, including any real provider keys in the maintainer's shell. The network guard blocks egress, and `OPENCODE_API_KEY` is overridden, so the assertions cannot pass through a real key. Hygiene against spec criterion 10's "maintainer's credentials" — PLAUSIBLE.

[MINOR] decisions/gates.yaml:217-223 (generated .github/workflows/ci.yml:61-68) — markdownlint now also scans `tools/pi/node_modules/`: 278 third-party .md files next to 316 repository files (counted 2026-10-15).
  - Caused by this change: the installer creates the directory locally, and in CI `setup-pi` (ci.yml:44, :173) runs before the lint step.
  - Severity: only noise. The gate is `report` with `continue-on-error`, but the noise can hide findings in this change's own Markdown.
  - Minimal repair: add `!tools/pi/node_modules/**` (or `#node_modules`) to the `globs` of the markdownlint gate in `decisions/gates.yaml`, then regenerate ci.yml with `scripts/ci_gates.py --generate-ci`. The local `npx` equivalent reads the same block. `gates.yaml` is not human-decided (provenance.yaml read), but plan step 7 promised to keep it unchanged, so name the deviation in the pull request — CONFIRMED.

[MINOR] scripts/ci_gates.py:455-462 — The generator, which travels with the kit (`scripts/kit/manifest.yaml:76`, `.github/workflows/ci.yml` at :133), now always emits `setup-node` from `tools/pi/.node-version` and `bash tools/pi/install.sh`. `tools/` stays behind (manifest.yaml:329), so a repository built from the kit would get CI steps it cannot run. There is precedent: `bash tools/beads/install.sh` (ci_gates.py:404) already does the same — PLAUSIBLE.

[MINOR] scripts/kit/probe.py:101, :190-193 — This change is outside the plan: plan.md:112-113 says "all created/changed files are named above", but probe.py is not named. The edit adds a REIST_NICHT entry and raises the cap DECKEL from 38 to 39, with a reason. It was needed after attempt 3 — CONFIRMED.

[STYLE] scripts/stage2.py:24 — The module docstring still says each round checks "`pi --version`"; it is now the wrapper — CONFIRMED.

## Check 2 — evidence per criterion
- 1: test_pi_install.py::test_install_obeys_lock_integrity_and_disables_scripts. The real install.sh runs; npm and node are imitations (MAJOR above).
- 2: test_wrapper_ignores_global_pi_from_any_cwd. The real wrapper script runs with a synthetic node, a synthetic local CLI and a hostile PATH `pi`. `require_installed_pi` also starts real Pi through the wrapper from a temporary working directory. Real evidence for the wrapper.
- 3: test_wrapper_refuses_unusable_local_pi. The real wrapper with synthetic node. Real evidence for the wrapper.
- 4: test_wrapper_checks_node_major and test_a_wrapper_without_node_refuses_before_everything. Same setup as 3; real evidence for the wrapper.
- 5: test_loop_and_probe_use_repository_pi and test_all_session_pi_launches_use_repository_wrapper. The runner code is real, Pi is a stand-in. test_real_reviewer_tool_contract:454 additionally shows real Pi through the wrapper. Sufficient for the routing claim.
- 6: test_real_reviewer_tool_contract. Real Pi through the wrapper, using the production `run_reviewer`. Real evidence.
- 7: test_real_reviewer_ignores_discovery_traps. Real Pi, but the traps cannot fire (BLOCKER). Only the context-file part is evidence.
- 8: test_real_extension_tool_input_and_result. Real Pi through the wrapper. Real evidence.
- 9: test_real_session_policy_blocks_foreign_reads. Real Pi with the production policy file and hand-listed flags. Real evidence, with the MINOR symlink gap.
- 10: test_real_model_listing_is_a_provider_table. Real Pi; the expected output matches what I measured.
- 11: test_real_opencode_provider_contracts uses real Pi plus a static catalog read (MAJOR narrowing). test_contract_network_guard_denies_external_destinations uses plain node, not Pi; the guard did deny opencode.ai inside real Pi in my run.
- 12: test_contract_prerequisites_and_failures_are_mandatory: real Pi for the timeout and malformed-exchange cases; the missing-prerequisite cases test the helper itself. test_real_pi_is_provisioned_before_contracts checks the YAML structure only. A real CI run is not read.
- 13: existing runner tests plus the stand-in truncation test. The runner side is real; Pi's truncation behaviour is imitated (MINOR).
- 14: not a test, judged by review: README, WORKFLOW, the endpoint remark and ADR 0019 exist, the historical ADRs are unchanged, and no Zen endpoint is enabled. The discovery-isolation claim is unsupported (MINOR).

## Check 3 — no soft pass
- The four Pi test files (test_pi_contract.py, test_pi_install.py and the two .mjs files) contain no skip, skipif, importorskip, xfail or `assert True`.
- The `return`s at test_pi_contract.py:153/157/208/211 and test_pi_install.py:219 are inside HTTP handlers or fixture builders, not inside test bodies.
- A missing prerequisite ends in `pytest.fail` or `ContractFailure`. The `PIN` lookup at import time (:71) raises, which fails collection.
- Skip markers, all pre-existing (test_ci.py's diff adds none): test_feedback_channel.py (8 unconditional); test_ci.py:1186 and :1400 (2 unconditional); conditional ones in test_repo_settings, test_omnigent_deny_layers, test_bead_render, test_templates, test_check_criterion_ledger and test_leakcheck (both root-only), test_harness_decide_adr, test_handover_entry, test_recap_lock and test_session_scan.
- The only skip near Pi is test_stage2_session_policy.py:29, `skipif` when node is absent. It is not a test_pi_* file, the plan keeps it unchanged, and node is present whenever the Pi suite runs.
- Which 6 conditional skips make up the 16 is not measured (I did not run pytest).

## Check 4 — wrapper and installer
- Matches ADR 0019 and design.md: no global fallback, no `npx`, no install from the wrapper, `npm ci --ignore-scripts`, Node major checked in both scripts, exact pin by regex. Both scripts are committed with mode 100755.
- Lock file: lockfileVersion 3, 119 entries, every non-root entry has a well-formed `sha512-…==` integrity, the only host is registry.npmjs.org, and all `@earendil-works/*` packages are at 1.2.0. Two packages (@google/genai, protobufjs) declare install scripts, which `--ignore-scripts` suppresses. Nothing suggests hand editing.

## Check 5 — scope
- Named in the plan: `.github/workflows/ci.yml` (regenerated), `.gitignore` (only `tools/pi/node_modules/`), `docs/WORKFLOW.md`, `model-endpoints.yaml`, `scripts/ci_gates.py`, `scripts/stage2.py`, `scripts/stage2_session.py`, `scripts/stage2_session_policy.mjs` (comments only), `tests/test_ci.py`, `tests/test_stage2.py`, `tests/test_stage2_session.py`, and the ADR.
- Owned by the orchestrator, as the plan says: `plans/INDEX.md` and `decisions/answers/pi-pin/adr.yaml`.
- Not named: `scripts/kit/probe.py` (MINOR above).
- Protected areas untouched: decisions/gates.yaml, .claude/settings.json, existing ADRs, test_stage2_session_policy.py and its driver.

## Check 7 — secrets
No credential-like values found. The only key-shaped strings are synthetic test constants (tests/test_pi_contract.py:48-49), a fake integrity value (tests/test_pi_install.py:32) and the registry integrity hashes in tools/pi/package-lock.json.

## Not read
- No earlier version of tests/test_pi_contract.py exists to diff the repairs against: not read.
- Results of a hosted CI run of this branch: not read, including whether actions/setup-node resolves Node 26.9.0.
- pi-mcp's real config schema for the `.pi/mcp.json` trap: not read.
- Which tests produced the 16 skips: not measured.
- markdownlint-cli2's default handling of node_modules: not read, inferred from the report you passed on.
- How I measured: I ran the real pinned Pi through `tools/pi/pi` 5 times, with scratch HOME and agent directories under my scratchpad, a synthetic key and the network guard. Pi wrote auth.json and models-store.json only into that scratch agent directory. Nothing in the repository was changed.

Resume: review complete, no edits made

Stage-2 call, 2026-10-15: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 457 files, 1271 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +1 -0
> - `decisions/gates.yaml` +1 -0
> - `docs/WORKFLOW.md` +13 -8
> - `docs/adr/0019-repository-pinned-pi-and-contract-tests.md` +3 -1
> - `plans/changes/pi-pin/plan.md` +42 -1
> - `scripts/ci_gates.py` +6 -2
> - `scripts/stage2.py` +1 -1
> - `tests/pi_contract_driver.mjs` +44 -0
> - `tests/test_ci.py` +11 -0
> - `tests/test_pi_contract.py` +226 -79
> - `tests/test_pi_install.py` +104 -1
> - `tests/test_stage2.py` +9 -7
> - `tools/pi/README.md` +7 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F-3: tests/test_stage2.py::test_a_pi_off_the_pin_is_refused: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> - F-4: tests/test_pi_install.py::test_install_obeys_lock_integrity_and_disables_scripts: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> - F-9: tests/test_stage2.py::test_pi_wrapper_is_repository_local: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> ```

Stage-2 call, 2026-10-15: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 457 files, 1271 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-pin/plan.md` +43 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F-1: no fixed line
> - F-2: no fixed line
> - F-3: no fixed line
> - F-4: no fixed line
> - F-5: no fixed line
> - F-6: no fixed line
> - F-7: no fixed line
> - F-8: no fixed line
> - F-9: no fixed line
> - F-10: no fixed line
> - F-11: no fixed line
> - F-12: no fixed line
> - F-13: no fixed line
> - F-14: no fixed line
> - expected: no taken row carries this id
> - found: no taken row carries this id
> - relevant: no taken row carries this id
> - proposal: no taken row carries this id
> - Resume: no taken row carries this id
> ```

Stage-2 call, 2026-10-15: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 457 files, 1271 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-pin/plan.md` +14 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```
