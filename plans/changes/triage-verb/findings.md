---
title: "Findings — triage-verb"
category: findings
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-o2s1
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — triage-verb

Stage-2 call, 2026-11-07: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 923 files, 3564 commits, 12 rules.

Stage-2 call, 2026-11-08: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 926 files, 3612 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +19 -1
> - `plans/changes/triage-verb/plan.md` +8 -8
> - `plans/changes/triage-verb/spec.md` +1 -1
> - `scripts/stage2.py` +156 -1
> - `tests/test_stage2.py` +344 -3
> - `tests/test_stage2_swarm.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ............................F.....                                       [100%]
> =================================== FAILURES ===================================
> _____ test_triage_help_and_instructions_match_the_cli_and_proof_ownership ______
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/triage-verb/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-797/popen-gw1...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-797/popen-gw1/test_triage_help_and_instructi0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x109447260>
>
>     def test_triage_help_and_instructions_match_the_cli_and_proof_ownership(
>         world: World, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         """Criterion 8. Planted fault: the documented example fails the parser, or the instructions omit refusal and marks."""
>         example = re.search(r"stage2\.py triage\s+<change> '(?P<row>[^']+)' '(?P<reason>[^']+)'", stage2.__doc__ or "")
>         assert example, "the runner help shows no triage example"
>         assert example.group("row").startswith("L1-1=")
>         triage_record(world, [triage_row(where="tests/test_stage2.py::test_x")])
>         capsys.readouterr()
>         example_code = world.run("triage", "demo", example.group("row"), example.group("reason"))
>         assert example_code == 0, "the documented example fails the parser"
>         assert stage2.record_rows(world.record().read_text(encoding="utf-8"))[0][7].startswith("taken — not a test")
> >       with pytest.raises(SystemExit), capsys:
> E       TypeError: 'CaptureFixture' object does not support the context manager protocol
>
> tests/test_stage2.py:19412: TypeError
> ----------------------------- Captured stdout call -----------------------------
> triage: L1-1 recorded as taken — not a test — The finding only strengthens a test.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_triage_help_and_instructions_match_the_cli_and_proof_ownership
> 1 failed, 33 passed in 7.65s
> ```

Stage-2 call, 2026-11-08: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 926 files, 3617 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/triage-verb/spec.md` +2 -2
> - `tests/test_stage2.py` +1 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 66 lines of this gate left out …]
> ........................................................................ [ 94%]
> ........................................................................ [ 95%]
> ........................................................................ [ 96%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> ....                                                                     [100%]
> =================================== FAILURES ===================================
> ________________ test_every_model_in_the_routing_table_resolves ________________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/triage-verb/.venv/bin/python3
>
>     def test_every_model_in_the_routing_table_resolves() -> None:
>         """The doctrine names models too, and they must resolve as well.
>     
>         Otherwise the rule holds for agent definitions and not for the table from
>         which a person picks a model.
>         """
>         text = WORKFLOW.read_text(encoding="utf-8")
>         tabelle = routing_models(text)
>         assert tabelle, "no model found in the routing of docs/WORKFLOW.md (RB-G7)"
>         # The table names display names ("Haiku 4.5"), the declaration ids.
>         ids = zugelassene_modelle()
>         for anzeige in tabelle:
>             if anzeige in {"the ladder", "the swarms, then the ladder"}:
>                 continue  # no model id: the ids live in the `opencode-go` entry, checked by its own test
>             if anzeige == "the research swarm":
>                 # No single model id: the swarm is a declared role roster. The row
>                 # resolves only while the declaration itself is complete and every
>                 # id it names sits on its declared endpoint.
>                 assert swarm_block_problems(_erklaerung()) == [], (
>                     "docs/WORKFLOW.md routes to 'the research swarm', but the declared swarm is incomplete"
>                 )
>                 continue
> >           assert _loest_auf(anzeige, ids), (
>                 f"docs/WORKFLOW.md routes to '{anzeige}', which no endpoint lists. "
>                 f"Looked for: {' or '.join(sorted(_kandidaten(anzeige)))}"
>             )
> E           AssertionError: docs/WORKFLOW.md routes to 'no model', which no endpoint lists. Looked for: claude-no-model or no-model
> E           assert False
> E            +  where False = _loest_auf('no model', {'beam-free', 'claude-haiku-5-5', 'claude-opus-5', 'claude-opus-5-5', 'claude-sonnet-5', 'claude-sonnet-5-5', ...})
>
> tests/test_model_endpoints.py:296: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=92518) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/triage-verb/tests/test_stage2.py:19000: DeprecationWarning: This process (pid=92524) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_model_endpoints.py::test_every_model_in_the_routing_table_resolves
> 1 failed, 4882 passed, 17 skipped, 5 warnings in 1047.46s (0:17:27)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32425 earlier lines left out …]
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

Stage-2 call, 2026-11-08: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 926 files, 3621 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 926 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 926 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 926 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 926 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3628 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 926 files, 3628 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 926 files, 3628 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 926 files, 3628 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 926 files, 3628 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 926 files, 3629 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 926 files, 3630 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 926 files, 3630 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 926 files, 3630 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 926 files, 3630 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 926 files, 3630 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3630 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3689 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3693 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3702 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3704 commits, 12 rules.

Stage-2 call, 2026-11-09: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3710 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 926 files, 3727 commits, 12 rules.
