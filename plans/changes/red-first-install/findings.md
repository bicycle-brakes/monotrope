---
title: "Findings — red-first-install"
category: findings
status: draft
implementation_status: none
date: 2026-10-16
created: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-omp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — red-first-install

Stage-2 call, 2026-10-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 464 files, 1318 commits, 12 rules.

Stage-2 call, 2026-10-16: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 467 files, 1320 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/red-first-install/plan.md` +14 -9
> - `plans/changes/red-first-install/spec.md` +1 -1
> - `scripts/stage2.py` +232 -9
> - `tests/test_stage2.py` +340 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 713 lines of this gate left out …]
> E         ## Taken rows
> E         
> E         - L1-1 [MAJOR, MAINT] src/app.py:1: finding of L1-1 — Status: taken — test_a
> E         
> E         ## Accepted spec
> E         
> E         ---
> E         title: Spec
> E         bead: demo-1
> E         ---
> E         
> E         # Spec
> E         
> E         
> E         ## Accepted plan
> E         
> E         ---
> E         title: Plan
> E         updated: 2026-09-30
> E         bead: demo-1
> E         ---
> E         
> E         # Plan
> E         
> E         ## Time used
> E         
> E         
> E         ## Earlier post-run diagnostics
> E         
> E         Attempt 1 (codex):
> E         - Runner format before `make verify`: not run — no ruff at `.venv/bin/ruff`; `make venv` builds it.
> E         - L1-1: tests/test_pi_env.py::test_pi_contract: the outcome record holds no call phase for `tests/test_pi_env.py::test_pi_contract`
> E         
> E         Read nothing outside this worktree and the repository's git directory.
> E       assert 'L1-1: tests/test_pi_env.py::test_pi_contract: the setup phase of `tests/test_pi_env.py::test_pi_contract` ended failed; red first needs passing setup and teardown' in "# Phase 4 · Implement\n\n**Model:** GLM 5.3 Flash — a solid worker given a clear plan; through\n`python3 scripts/stag...for `tests/test_pi_env.py::test_pi_contract`\n\nRead nothing outside this worktree and the repository's git directory."
>
> tests/test_stage2.py:6359: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 23 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: repair post-run checks failed after the allowed attempts; why each attempt failed and the files it changed: plans/changes/demo/findings.md
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_repair_prose_alone_still_needs_fixed_lines
> FAILED tests/test_stage2.py::test_red_first_refuses_a_missing_pi_install - As...
> FAILED tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors
> FAILED tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures
> FAILED tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes[collection-error]
> FAILED tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes[internal-error]
> FAILED tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes[xfail-beside-assertion]
> FAILED tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes[strict-xpass-beside-assertion]
> FAILED tests/test_stage2.py::test_repair_refuses_environment_only_red_first_evidence
> 9 failed, 2142 passed, 16 skipped in 785.19s (0:13:05)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 11004 earlier lines left out …]
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

Stage-2 call, 2026-10-16: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 467 files, 1327 commits, 12 rules.
