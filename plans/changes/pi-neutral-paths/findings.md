---
title: "Findings — pi-neutral-paths"
category: findings
status: draft
implementation_status: none
date: 2026-10-29
created: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-31
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
