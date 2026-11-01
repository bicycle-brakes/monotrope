---
title: "Findings — verify-worker-cap"
category: findings
status: draft
implementation_status: none
date: 2026-10-29
created: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-l7sc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-worker-cap

Stage-2 call, 2026-10-29: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 740 files, 2670 commits, 12 rules.

Stage-2 call, 2026-10-30: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 787 files, 2800 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 803 files, 2884 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 803 files, 2889 commits, 12 rules.

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 803 files, 2899 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/spec.md` +5 -2
> - `scripts/verify_all.sh` +11 -3
> - `tests/test_ci.py` +15 -2
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 1 red case(s) without a declared reason
>       tests.test_ci::test_worker_memory_term_names_platform_readings
>       
>       Add them with: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 1299 of 1342 cases carry into a foreign repository (96 %)
>       mechanismus 104 · bestand 699 file(s)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 24853 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-1-20261031T153611005006Z-eb6884d3.md
> ````

Stage-2 call, 2026-10-31: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 803 files, 2900 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/spec.md` +6 -3
> - `tests/test_ci.py` +8 -9
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: tests/test_ci.py::test_runner_preserves_explicit_worker_value: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> tests/test_ci.py::test_runner_preserves_explicit_worker_value: refs changed while the named test ran: refs/heads/docs/architecture-reconcile, refs/heads/feat/go-access-point, refs/heads/fix/pi-neutral-paths, refs/remotes/origin/__dolt_remote_info__, refs/remotes/origin/docs/architecture-reconcile, refs/remotes/origin/fix/pi-neutral-paths
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-2-20261031T153611005006Z-eb6884d3.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 803 files, 2907 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/spec.md` +5 -2
> - `tests/test_ci.py` +7 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: tests/test_ci.py::test_runner_preserves_explicit_worker_value: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> tests/test_ci.py::test_runner_preserves_explicit_worker_value: refs changed while the named test ran: refs/heads/fix/pi-neutral-paths, refs/remotes/origin/fix/pi-neutral-paths
> - L1-5: tests/test_ci.py::test_runner_worker_detection_degrades_without_failure: refs changed while the named test ran: refs/heads/fix/pi-neutral-paths, refs/remotes/origin/fix/pi-neutral-paths
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-3-20261031T153611005006Z-eb6884d3.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 803 files, 2913 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/spec.md` +1 -1
>
> Diagnostics:
> ```text
> - L1-5: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-1-20261031T190808158515Z-90d0ef98.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 803 files, 2916 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/spec.md` +1 -1
>
> Diagnostics:
> ```text
> - L1-4: no fixed line
> - L1-5: no fixed line
> - L1-6: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-2-20261031T190808158515Z-90d0ef98.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 803 files, 2921 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - L1-5: tests/test_ci.py::test_runner_worker_detection_degrades_without_failure: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> tests/test_ci.py::test_runner_worker_detection_degrades_without_failure: refs changed while the named test ran: refs/heads/docs/architecture-reconcile, refs/heads/docs/run-plan-2026-10-31, refs/heads/feat/go-access-point, refs/remotes/origin/__dolt_remote_info__, refs/remotes/origin/docs/architecture-reconcile, refs/remotes/origin/docs/run-plan-2026-10-31, refs/remotes/origin/feat/go-access-point
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-3-20261031T190808158515Z-90d0ef98.md
> ```

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 803 files, 2929 commits, 12 rules.

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 803 files, 2930 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/plan.md` +0 -4
> - `scripts/verify_all.sh` +12 -2
> - `tests/test_ci.py` +6 -8
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L2-5: tests/test_ci.py::test_runner_worker_detection_degrades_without_failure: refs changed while the named test ran: refs/remotes/origin/__dolt_remote_info__
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-1-20261031T214857652833Z-6ac2399b.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 803 files, 2936 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/plan.md` +0 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L2-5: tests/test_ci.py::test_runner_worker_detection_degrades_without_failure: refs changed while the named test ran: refs/heads/feat/beads-close-themselves, refs/remotes/origin/feat/beads-close-themselves
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-2-20261031T214857652833Z-6ac2399b.md
> ```

Stage-2 call, 2026-11-01: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 803 files, 2939 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-worker-cap/plan.md` +0 -8
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L2-5: answered `not a test`, but the row is a code row; it needs a test that was red first
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-worker-cap/stage2/attempts/verify-worker-cap/attempt-3-20261031T214857652833Z-6ac2399b.md
> ```

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model hy3 · leak check clean over 803 files, 2943 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 803 files, 2944 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 803 files, 2964 commits, 12 rules.
