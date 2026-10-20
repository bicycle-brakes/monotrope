---
title: "Findings — review-loop-row-ids"
category: findings
status: draft
implementation_status: none
date: 2026-10-20
created: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-6jg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-loop-row-ids

Stage-2 call, 2026-10-20: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 494 files, 1609 commits, 12 rules.

> Attempt 1 (codex): the runner put back what a draft may not change:
> - `plans/changes/review-loop-row-ids/decisions.md`

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/review-loop-row-ids/decisions.md` +17 -1
> - `plans/changes/review-loop-row-ids/plan.md` +126 -0
> - `plans/changes/review-loop-row-ids/research.md` +36 -0
> - `plans/changes/review-loop-row-ids/spec.md` +147 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 797 lines of this gate left out …]
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
>                 **contract_environment(),
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
>                 pytest.fail(f"the pinned Pi {PIN} could not be checked ({error}); run bash tools/pi/install.sh")
>         if done.returncode != 0 or done.stdout.strip() != PIN:
>             said = done.stdout.strip() or "nothing"
> >           pytest.fail(
>                 f"the pinned Pi {PIN} is not installed or will not start (printed {said!r}, ended {done.returncode}): "
>                 f"{done.stderr.strip()[:400]}; run bash tools/pi/install.sh"
>             )
> E           Failed: the pinned Pi 1.2.0 is not installed or will not start (printed 'nothing', ended 1): tools/pi/pi: the pinned Pi (@earendil-works/pi-coding-agent@1.2.0) is not installed under /Users/mikypiky/coding-harness/.claude/worktrees/review-loop-row-ids/tools/pi/node_modules.
> E           tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md); run bash tools/pi/install.sh
>
> tests/test_pi_contract.py:106: Failed
> =========================== short test summary info ============================
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-946684800000]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-946684800000]
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_free_reviewer_has_only_the_implementation_diff
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_ambient_credentials
> ERROR tests/test_pi_contract.py::test_real_extension_tool_input_and_result - ...
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory
> ERROR tests/test_pi_contract.py::test_real_truncated_pi_print_failure_is_refused
> ERROR tests/test_pi_contract.py::test_contract_environment_excludes_parent_provider_keys
> ERROR tests/test_pi_contract.py::test_real_catalog_headers_remain_literal - F...
> 2272 passed, 16 skipped, 16 errors in 138.96s (0:02:18)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [interview-minimums] $ lauf_cmd
> 1 finding(s):
>   - review-loop-row-ids (bounded): neither an interview record answered by the maintainer nor a reasoned skip stands in decisions.md
> ── [interview-minimums] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12249 earlier lines left out …]
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
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-20: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 497 files, 1609 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/review-loop-row-ids/plan.md` +16 -2
> - `plans/changes/review-loop-row-ids/research.md` +21 -0
> - `plans/changes/review-loop-row-ids/spec.md` +7 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 797 lines of this gate left out …]
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
>                 **contract_environment(),
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
>                 pytest.fail(f"the pinned Pi {PIN} could not be checked ({error}); run bash tools/pi/install.sh")
>         if done.returncode != 0 or done.stdout.strip() != PIN:
>             said = done.stdout.strip() or "nothing"
> >           pytest.fail(
>                 f"the pinned Pi {PIN} is not installed or will not start (printed {said!r}, ended {done.returncode}): "
>                 f"{done.stderr.strip()[:400]}; run bash tools/pi/install.sh"
>             )
> E           Failed: the pinned Pi 1.2.0 is not installed or will not start (printed 'nothing', ended 1): tools/pi/pi: the pinned Pi (@earendil-works/pi-coding-agent@1.2.0) is not installed under /Users/mikypiky/coding-harness/.claude/worktrees/review-loop-row-ids/tools/pi/node_modules.
> E           tools/pi/pi: set the pinned install up with: bash tools/pi/install.sh (see tools/pi/README.md); run bash tools/pi/install.sh
>
> tests/test_pi_contract.py:106: Failed
> =========================== short test summary info ============================
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-946684800000]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-946684800000]
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_free_reviewer_has_only_the_implementation_diff
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_ambient_credentials
> ERROR tests/test_pi_contract.py::test_real_extension_tool_input_and_result - ...
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory
> ERROR tests/test_pi_contract.py::test_real_truncated_pi_print_failure_is_refused
> ERROR tests/test_pi_contract.py::test_contract_environment_excludes_parent_provider_keys
> ERROR tests/test_pi_contract.py::test_real_catalog_headers_remain_literal - F...
> 2272 passed, 16 skipped, 16 errors in 134.06s (0:02:14)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [interview-minimums] $ lauf_cmd
> 1 finding(s):
>   - review-loop-row-ids (bounded): neither an interview record answered by the maintainer nor a reasoned skip stands in decisions.md
> ── [interview-minimums] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12300 earlier lines left out …]
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
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-20: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 497 files, 1609 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.3","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/review-loop-row-ids/draft-attempt-3-20261020T024526277344Z (ab56251728e8); `git diff aae2307a5a7b refs/stage2/attempts/review-loop-row-ids/draft-attempt-3-20261020T024526277344Z` shows it.
>
> The runner put back:
> - `plans/INDEX.md`
> - `plans/changes/review-loop-row-ids/plan.md`
> - `plans/changes/review-loop-row-ids/research.md`
> - `plans/changes/review-loop-row-ids/spec.md`

Stage-2 call, 2026-10-20: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 495 files, 1610 commits, 12 rules.
