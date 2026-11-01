---
title: "Findings — pi-neutral-paths"
category: findings
status: draft
implementation_status: none
date: 2026-10-29
created: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-xul8
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — pi-neutral-paths

Stage-2 call, 2026-10-29: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 733 files, 2611 commits, 12 rules.

Stage-2 call, 2026-10-30: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 787 files, 2799 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-neutral-paths/plan.md` +11 -11
> - `scripts/stage2.py` +10 -0
> - `scripts/stage2_availability.py` +8 -0
> - `scripts/stage2_pi_neutral_paths.mjs` +143 -0
> - `scripts/stage2_research_run.py` +13 -2
> - `scripts/stage2_session.py` +61 -27
> - `tests/test_pi_contract.py` +442 -2
> - `tests/test_stage2.py` +37 -0
> - `tests/test_stage2_availability.py` +20 -0
> - `tests/test_stage2_research_availability.py` +21 -0
> - `tests/test_stage2_session.py` +45 -6
> - `tests/test_stage2_swarm.py` +24 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_pi_contract.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> tests/test_pi_contract.py:539:21: SIM102 Use a single `if` statement instead of nested `if` statements
>     |
> 537 |                       event = await_event(f"answer turn {index}", deadline)
> 538 |                       events.append(event)
> 539 | /                     if event.get("type") == "response" and event.get("command") == "prompt":
> 540 | |                         if not event.get("success"):
>     | |____________________________________________________^ SIM102
> 541 |                               raise ContractFailure(f"turn {index} was refused: {event.get('error')}: {why()}")
> 542 |                       if event.get("type") == "agent_settled":
>     |
>     = help: Combine `if` statements using `and`
>
> tests/test_pi_contract.py:545:13: SIM105 Use `contextlib.suppress(OSError)` instead of `try`-`except`-`pass`
>     |
> 543 |                           settled = True
> 544 |           finally:
> 545 | /             try:
> 546 | |                 process.stdin.close()
> 547 | |             except OSError:
> 548 | |                 pass
>     | |____________________^ SIM105
> 549 |               try:
> 550 |                   process.wait(timeout=30)
>     |
>     = help: Replace with `contextlib.suppress(OSError)`
>
> tests/test_stage2.py:5389:29: F821 Undefined name `types`
>      |
> 5387 |     monkey.setattr(stage2, "launch", capture)
> 5388 |     try:
> 5389 |         stage2.run_reviewer(types.SimpleNamespace(change="demo", root=world.root), TEST_LADDER[0], "capture", "key")
>      |                             ^^^^^ F821
> 5390 |     finally:
> 5391 |         monkey.undo()
>      |
>
> Found 3 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-10-31: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 788 files, 2809 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-neutral-paths/plan.md` +10 -10
> - `tests/test_pi_contract.py` +8 -6
> - `tests/test_stage2.py` +2 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> tests/test_stage2.py:5390:29: F821 Undefined name `types`
>      |
> 5388 |     monkey.setattr(stage2, "launch", capture)
> 5389 |     try:
> 5390 |         stage2.run_reviewer(types.SimpleNamespace(change="demo", root=world.root), TEST_LADDER[0], "capture", "key")
>      |                             ^^^^^ F821
> 5391 |     finally:
> 5392 |         monkey.undo()
>      |
>
> Found 1 error.
> ```

Stage-2 call, 2026-10-31: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 788 files, 2809 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-neutral-paths/plan.md` +10 -10
> - `tests/test_stage2.py` +1 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>             [
>                 {"tool_calls": [{"name": "read", "arguments": {"path": "sentinel.txt"}}]},
>                 {"tool_calls": [{"name": "read", "arguments": {"path": "absent-file.txt"}}]},
>                 {"content": "No finding."},
>             ]
>         )
>         transport.providers["opencode-go"] = {"baseUrl": standin.url}
>         try:
>             answer = stage2.run_reviewer(
>                 types.SimpleNamespace(change="demo", root=project), "contract-rung", "Review demo.", SYNTHETIC_KEY
>             )
>             assert "No finding." in answer, "the scripted stop never reached the runner"
>         finally:
>             standin.close()
>         assert len(standin.requests) == 3, "the tool result and the tool error did not each draw a follow-up"
>         assert_payloads_are_neutral(standin.requests, shape_identifiers(transport.calls[0]["env"], project), "the reviewer")
>         assert SENTINEL_IN in message_text(standin.requests[1]), "the positive control read never executed"
>         assert "absent-file.txt" in json.dumps(standin.requests[2].body), "the tool error did not travel"
>         assert str(project / "sentinel.txt") not in json.dumps(standin.requests[1].body), (
>             "the tool result kept its absolute path"
>         )
>         # the free member
>         free = StandIn([{"content": "No finding."}])
>         transport.providers["opencode-go"] = {"baseUrl": free.url}
>         try:
>             answer = stage2.run_reviewer(
>                 types.SimpleNamespace(change="demo", root=project), "acme-1-free", "Free review.", SYNTHETIC_KEY, free=True
>             )
>             assert "No finding." in answer, "the scripted stop never reached the runner"
>         finally:
>             free.close()
>         (one,) = free.requests
>         assert_payloads_are_neutral([one], shape_identifiers(transport.calls[-1]["env"], None), "the free member")
>         assert tool_names(one) == set(), "the free member was offered tools"
>         # the interactive session: context on, two user turns, one tool follow-up
>         (project / "AGENTS.md").write_text(CONTEXT_CANARY + "\n", encoding="utf-8")
>         scratch = scratch_of(tmp_path)
>         argv, _policy, _neutral = rpc_argv(project, scratch)
>         session = StandIn(
>             [
>                 {"tool_calls": [{"name": "read", "arguments": {"path": "sentinel.txt"}}]},
>                 {"content": "done one"},
>                 {"content": "done two"},
>             ]
>         )
>         try:
> >           events = drive_rpc(
>                 project,
>                 scratch,
>                 argv,
>                 {"opencode-go": {"baseUrl": session.url}},
>                 ["Turn one: read the sentinel.", "Turn two: stop."],
>             )
>
> tests/test_pi_contract.py:1244: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_pi_contract.py:538: in drive_rpc
>     event = await_event(f"answer turn {index}", deadline)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> what = 'answer turn 0', deadline = 447031.707611958
>
>     def await_event(what: str, deadline: float) -> dict:
>         budget = deadline - time.monotonic()
>         if budget <= 0:
>             raise ContractFailure(f"the RPC run did not {what} within {timeout}s: {why()}")
>         try:
>             event = lines.get(timeout=budget)
>         except queue.Empty:
> >           raise ContractFailure(f"the RPC run did not {what} within {timeout}s: {why()}") from None
> E           test_pi_contract.ContractFailure: the RPC run did not answer turn 0 within 180s:
>
> tests/test_pi_contract.py:525: ContractFailure
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_all_review_members_load_neutral_paths - Ass...
> FAILED tests/test_stage2_swarm.py::test_research_seats_load_neutral_paths - A...
> FAILED tests/test_pi_contract.py::test_real_pi_neutral_cwd_on_every_run - tes...
> FAILED tests/test_pi_contract.py::test_real_neutralization_preserves_tool_roots_and_boundaries
> FAILED tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers
> 5 failed, 9 passed in 190.89s (0:03:10)
> ```

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 806 files, 2914 commits, 12 rules.

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 806 files, 2916 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-neutral-paths/decisions.md` +1 -1
> - `plans/changes/research-swarm/plan.md` +1 -1
> - `scripts/stage2_pi_neutral_paths.mjs` +17 -16
> - `scripts/stage2_research_run.py` +6 -1
> - `scripts/stage2_session.py` +2 -0
> - `tests/test_pi_contract.py` +27 -0
> - `tests/test_stage2_repository_pathlock.py` +34 -3
> - `tests/test_stage2_session.py` +11 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-3: tests/test_stage2_session.py::test_pi_cli_argv_refuses_missing_extension_paths: refs changed while the named test ran: refs/heads/docs/architecture-reconcile, refs/heads/feat/go-access-point, refs/remotes/origin/docs/architecture-reconcile, refs/remotes/origin/feat/go-access-point
> - L1-5: tests/test_pi_contract.py::test_neutral_prefix_preserves_embedded_paths: refs changed while the named test ran: refs/heads/docs/architecture-reconcile, refs/heads/docs/run-plan-2026-10-31, refs/heads/feat/go-access-point, refs/remotes/origin/__dolt_remote_info__, refs/remotes/origin/docs/architecture-reconcile, refs/remotes/origin/docs/run-plan-2026-10-31, refs/remotes/origin/feat/go-access-point
> - L1-8: tests/test_stage2_session.py::test_pi_cli_argv_refuses_missing_extension_paths: refs changed while the named test ran: refs/heads/docs/architecture-reconcile, refs/heads/feat/explorer-reviewer-agents, refs/heads/feat/go-access-point, refs/heads/fix/verify-worker-cap, refs/remotes/origin/HEAD, refs/remotes/origin/__dolt_remote_info__, refs/remotes/origin/docs/architecture-reconcile, refs/remotes/origin/feat/explorer-reviewer-agents, refs/remotes/origin/feat/go-access-point, refs/remotes/o [… 145 characters left out …]
> - L1-9: tests/test_stage2_repository_pathlock.py::test_research_neutral_source_failure_is_a_named_refusal: the call of `tests/test_stage2_repository_pathlock.py::test_research_neutral_source_failure_is_a_named_refusal[failure0]` failed with FileNotFoundError, which is neither Python's AssertionError nor pytest's own failed outcome (pytest.fail.Exception)
> tests/test_stage2_repository_pathlock.py::test_research_neutral_source_failure_is_a_named_refusal: refs changed while the named test ran: refs/remotes/origin/__dolt_remote_info__
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-1-20261031T193523195322Z-0faad25e.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 806 files, 2936 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-neutral-paths/decisions.md` +1 -1
> - `tests/test_stage2_repository_pathlock.py` +4 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/pi-neutral-paths/decisions.md: stale — updated 2026-10-31 is older than its last change 2026-11-01 (uncommitted)
> plans/changes/pi-neutral-paths/findings.md: stale — updated 2026-10-31 is older than its last change 2026-11-01 (uncommitted)
> plans/changes/pi-neutral-paths/plan.md: stale — updated 2026-10-31 is older than its last change 2026-11-01 (uncommitted)
> plans/changes/research-swarm/plan.md: stale — updated 2026-10-31 is older than its last change 2026-11-01 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 24870 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-2-20261031T193523195322Z-0faad25e.md
> ````

Stage-2 call, 2026-11-01: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 806 files, 2937 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-neutral-paths/decisions.md` +1 -1
> - `plans/changes/research-swarm/plan.md` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-3: tests/test_stage2_session.py::test_pi_cli_argv_refuses_missing_extension_paths: refs changed while the named test ran: refs/heads/feat/beads-close-themselves
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-3-20261031T193523195322Z-0faad25e.md
> ```

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 806 files, 2944 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 806 files, 2946 commits, 12 rules.

Stage-2 call, 2026-11-01: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 806 files, 2946 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +2 -2
> - `scripts/stage2_availability.py` +2 -3
> - `scripts/stage2_pi_extensions.py` +16 -0
> - `scripts/stage2_pi_neutral_paths.mjs` +29 -5
> - `scripts/stage2_research_run.py` +2 -8
> - `scripts/stage2_session.py` +2 -8
> - `tests/test_pi_contract.py` +57 -2
> - `tests/test_stage2_pi_extensions.py` +43 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 85 lines of this gate left out …]
>         heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
> >       assert not heimatlos, (
>             "Without a caller and without a reason:\n  "
>             + "\n  ".join(heimatlos)
>             + "\n\nEither a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER."
>         )
> E       AssertionError: Without a caller and without a reason:
> E           stage2_pi_extensions.py
> E         
> E         Either a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER.
> E       assert not ['stage2_pi_extensions.py']
>
> tests/test_ci.py:1898: AssertionError
> ______________ test_every_script_has_a_test_or_a_declared_reason _______________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/pi-neutral-paths/.venv/bin/python3
>
>     def test_every_script_has_a_test_or_a_declared_reason() -> None:
>         """A tool without a test is invisibly broken.
>     
>         Without a caller, a script is conspicuous: it does nothing. Without a test it
>         is not conspicuous — it may be doing the wrong thing, and nobody runs it to
>         notice. Hence the same rule as for the callers: either a test executes it, or
>         it stands with a reason in `ci_gates.OHNE_TEST`.
>         """
>         from ci_gates import OHNE_TEST
>     
>         ungehalten = [p.name for p in _scripts() if p.name not in OHNE_TEST and not _belegt(p)]
> >       assert not ungehalten, (
>             "Without a test and without a reason:\n  "
>             + "\n  ".join(ungehalten)
>             + "\n\nEither a test file that imports the module or starts it as a "
>             "subprocess, or a line in ci_gates.OHNE_TEST."
>         )
> E       AssertionError: Without a test and without a reason:
> E           stage2_pi_extensions.py
> E         
> E         Either a test file that imports the module or starts it as a subprocess, or a line in ci_gates.OHNE_TEST.
> E       assert not ['stage2_pi_extensions.py']
>
> tests/test_ci.py:2059: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=81443) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/pi-neutral-paths/tests/test_stage2.py:17180: DeprecationWarning: This process (pid=81444) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> FAILED tests/test_ci.py::test_every_script_has_a_test_or_a_declared_reason - ...
> 2 failed, 4416 passed, 17 skipped, 5 warnings in 571.57s (0:09:31)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 24925 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-1-20261101T073634885341Z-f042820e.md
> ````

Stage-2 call, 2026-11-01: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 808 files, 2950 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/ci_gates.py` +4 -0
> - `tests/test_stage2_pi_extensions.py` +9 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L2-2: tests/test_stage2_pi_extensions.py::test_neutral_copy_failure_is_shared_named_refusal: the call of `tests/test_stage2_pi_extensions.py::test_neutral_copy_failure_is_shared_named_refusal[failure0-review]` failed with FileNotFoundError, which is neither Python's AssertionError nor pytest's own failed outcome (pytest.fail.Exception)
> - L2-3: tests/test_pi_contract.py::test_neutral_registration_covers_launch_directories: refs changed while the named test ran: refs/heads/feat/go-access-point
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-2-20261101T073634885341Z-f042820e.md
> ```

Stage-2 call, 2026-11-01: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 808 files, 2952 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2_pi_extensions.py` +15 -5
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2_pi_extensions.py`.
> - L2-2: tests/test_stage2_pi_extensions.py::test_neutral_copy_failure_is_shared_named_refusal: the call of `tests/test_stage2_pi_extensions.py::test_neutral_copy_failure_is_shared_named_refusal[failure0-review]` failed with FileNotFoundError, which is neither Python's AssertionError nor pytest's own failed outcome (pytest.fail.Exception)
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-3-20261101T073634885341Z-f042820e.md
> ```

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model hy3 · leak check clean over 808 files, 2956 commits, 12 rules.

Stage-2 call, 2026-11-01: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 808 files, 2957 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2_pi_neutral_paths.mjs` +65 -11
> - `tests/test_pi_contract.py` +197 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L3-1: tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers: the setup phase of `tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers` ended failed; red first needs passing setup and teardown
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-1-20261101T085557541965Z-9f26e0d6.md
> ```

Stage-2 call, 2026-11-01: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 808 files, 2957 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L3-1: tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers: the setup phase of `tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers` ended failed; red first needs passing setup and teardown
> - L3-2: tests/test_pi_contract.py::test_neutral_cwd_fails_closed: refs changed while the named test ran: refs/heads/feat/go-access-point
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-2-20261101T085557541965Z-9f26e0d6.md
> ```

Stage-2 call, 2026-11-01: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 808 files, 2959 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L3-1: tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers: the setup phase of `tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers` ended failed; red first needs passing setup and teardown
> - L3-3: tests/test_pi_contract.py::test_neutral_prefix_redacts_colon_locations: refs changed while the named test ran: refs/heads/feat/beads-close-themselves
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/pi-neutral-paths/stage2/attempts/pi-neutral-paths/attempt-3-20261101T085557541965Z-9f26e0d6.md
> ```
