---
title: "Findings — address-notice-once"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-zywb
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — address-notice-once

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1157 files, 5185 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1160 files, 5187 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | BLOCKER | SPEC | base | `spec.md` criteria 1 and 5; `scripts/stage2_availability.py:1509` (`print(report(state))`), `:1252` (`print(research_report(state))`), `:1042`, `:1373` | [AMBIGUITY] It is unclear whether a printed availability report counts as console output or as a report. The preparation reports go only to stdout. In prepare-loop, `report()` lists every discovery notice as `Address notice: X` and prints it after `discover_free` has already printed X to stderr (`scripts/stage2.py:2831–2832`) and `probe_go` has printed it to stdout (`:532`). `research_report()` does the same for the catalog notices. Criterion 1 lists "reporting" among the console sources to deduplicate. Criterion 5 says a report keeps each notice "even if that notice was already printed in the call". Reading A: the printed report is console output. Its notice lines are dropped, so the prepare-loop report shows no notices, or only ones not printed before, and criterion 5 fails for that report. Reading B: the printed report is a report. It keeps every line, so prepare-loop still prints X three times (discovery, probe, report), which is the bead's own complaint, and criterion 1 fails. On the bead's own path, each reading makes one of the two criteria fail. | Opus | in spec — [DETAIL] decided by the orchestrator: a printed availability report is a report and keeps every distinct notice once; in a call that prints such a report, the earlier console prints of the same notices (discover_free, probe_go) are suppressed, so prepare-loop shows each notice once, in its report. Reason: the bead's complaint is the triple print in prepare-loop, and the report is the one place a reader looks | — |
| S-2 | MAJOR | SPEC | base | `spec.md` Terms «Runner call», criteria 1 and 3; `tests/test_stage2.py:413–415`; `tests/test_stage2_swarm.py:481–482`; `tests/test_stage2_go_access.py:1157–1168`, `:322–327`; `scripts/research_capture.py:1149` | [AMBIGUITY] The Terms define a runner call as one operating-system process. But the runner is also run inside other processes: tests call `stage2.main([...])` and runner functions directly, and `research_capture.py` calls `probe_go` from another program. Reading A (literal): a whole pytest process is one call, and one seen-set covers the process. `test_notices_are_kept_and_sanitised` runs review-loop and then a reviewer call in the same process, and expects `Address notice:` on stderr again (`:1166–1168`). That expectation now breaks criterion 1, so the test must be rewritten. Every test that checks for a printed notice depends on which tests ran before it. Criterion 3 can only be refuted by starting two real processes. Reading B: a call is one runner entry, i.e. one `main()` invocation, with a new seen-set each time. The pinned tests stay valid, and criterion 3 can be tested with two `main()` calls. But the spec does not say whether notices emitted outside an entry (direct function calls, `research_capture.py`) are deduplicated at all. The readings disagree on which pinned tests stay valid and on how criterion 3 is proved. | Opus | in spec — [DETAIL] decided by the orchestrator: a runner call is one invocation of the runner's entry point (stage2.main and the availability and research entry points); the seen-set is a context opened at that entry and closed at its exit, so tests that call main twice get two calls, and a direct function call outside any entry prints as today. Reason: one operating-system process is not testable and not how the runner is embedded | — |
| S-3 | MAJOR | SPEC | base | `spec.md` criteria 5–6; `scripts/stage2_availability.py:530–532`, `:467–468`, `:551`, `:785–794`, `:1246`; `tests/test_stage2_go_access.py:325–327` | The probe's launch audit is durable evidence, but no criterion protects it. Criterion 5 covers round records and reports. Criterion 6 covers research-seat and session audits. `probe_go` appends `address notice · X` to its audit and prints X in the same `if verdict.notice:` block (`:530–532`). `install_measured_models` adds the same note (`:467–468`, added to the audit at `:551`). In research preparation, `_ProbeAudit.append` writes each audit line to a receipt file (`:785–794`), and the selection state keeps the audit (`:1246`). This is the launch evidence ADR 0024 says preserves path notices. Suppose an implementation skips the whole block when X was already printed. It passes all eight criteria, but it drops the probe audit line that `test_same_host_path_moves_run_with_notice` checks. The spec does not say whether the probe and install audits must keep every notice, so whoever builds it has to decide. | Opus | in spec — [DETAIL] decided by the orchestrator: add a criterion — the probe's launch audit (probe_go and install_measured_models audit lines) keeps each distinct notice; only the console print is subject to the seen-set. Reason: the audit is durable evidence like the round record | — |
| S-4 | MAJOR | SPEC | base | `spec.md` Terms «Distinct notice», criterion 5 refutation, Non-goals (record spellings); `scripts/stage2.py:11053`, `:11070–11073`, `:3263–3264`, `:11271–11272` | [AMBIGUITY] It is unclear whether one round record that holds the same notice under both spellings "repeats the same notice". On a run's first unconsumed round, `_review_round` writes `Notice: X.` from the stored discovery notices (`11070–11073`). The reviewer then activates the same `models_store` (`11053`, `3263–3264`), and its retained notices add `Address notice: X` to the same round block (`11271–11272`). The Terms say a distinct notice does not depend on its prefix. Reading A: criterion 5's "a record repeats the same notice" covers this pair, so one of the two lines must leave the round record. That changes the record content, which `decisions.md` says stays ("the existing per-round dedup stays"). Reading B: "repeats" means the identical line appearing twice. The non-goal on record spellings allows the pair, and the record stays as it is. Today's first round fails criterion 5 under A and passes under B. | Opus | in spec — [DETAIL] decided by the orchestrator: the two existing spellings are two record sections and stay as they are; within each section a notice appears at most once per record, and the same notice under both spellings is not a repeat. Reason: no spelling change (non-goal), and each section has its own source | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1160 files, 5191 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1160 files, 5195 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1160 files, 5204 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-5 | MAJOR | SPEC | base | `spec.md` criteria 1–2, Open decisions [DETAIL] ("already encountered notices still appear once"); `scripts/stage2_session.py:639–640`, `:652`; `scripts/stage2_swarm.py:290–296`; `scripts/stage2_availability.py:325–331`, `:909–916`, `:1252` | [AMBIGUITY] The spec does not say when a notice counts as "encountered" or as "occurring" in a call. Several assessments produce a notice that no console line shows today. First, the session keeps the notice from `checked_session_model` only for its pending audit line. If `confirm_binding` refuses (`stage2_session.py:652`), the call ends before `dispatch_go` prints anything. Second, `select_research_catalog` collects a notice for every candidate (`stage2_swarm.py:290–296`), and these reach the console only through `research_report` (`stage2_availability.py:1252`). A probe refused by `_checked_probe`'s admission or leak check (`:325–331`) raises `Refused`, which `reachable` does not catch (`:909–916`). Prepare-explore then ends with those notices unprinted. Reading A: only a notice that an existing print site would have printed counts. These paths stay silent, and the early-exit [DETAIL] flushes only the notices whose print was held back. Reading B: every notice the assessment returns during the call counts. Criterion 2 and the early-exit [DETAIL] then require new console lines on these paths: every candidate's notice when prepare-explore exits early, and the session's notice when its binding is refused. Criterion 7 gives these lines no wording or stream, because they have no existing first occurrence. The two readings put the seen-set in different places (at the print sites or at the assessment), and they give different console output for every early exit. | Opus | in spec — [DETAIL] decided by the orchestrator: a notice counts as encountered only when a console print of it would happen today; assessments whose notice no console line shows today (session audit prefix, research catalog selection, availability internals) neither print nor enter the seen-set. Reason: the change removes repeats, it never adds a new console line | — |
| S-6 | MAJOR | SPEC | base | `spec.md` Open decisions [DETAIL] ("The report's existing stdout takes precedence over an earlier discovery stream in this case"), criterion 7; `scripts/stage2.py:2831–2832`; `scripts/stage2_availability.py:325–331`, `:1450`, `:1468–1478`, `:1509` | [AMBIGUITY] "In this case" could refer to either of the two preceding sentences. In prepare-loop, `discover_free` meets a notice X first and today prints it to stderr (`stage2.py:2832`). `prepare` can still stop before `print(report(state))` (`stage2_availability.py:1509`): `preflight` (`:1450`) or `_checked_probe`'s admission and leak-check refusals (`:325–331`) raise `Refused`, and the probe loop catches only `CallFailed` and `DestinationRefused` (`:1468–1478`). Reading A: the sentence refers to the early exit named just before it, so held notices are flushed to stdout, the report's stream. Reading B: the sentence refers to the printed report and explains why the report's stdout line replaces discovery's stderr line. On an early exit, criterion 7 then applies ("printed outside a preparation report … the stream of its first occurrence"), so X goes to stderr. A test of this early exit that reads stderr passes under B and fails under A, and Reading A contradicts criterion 7. | Opus | in spec — [DETAIL] decided by the orchestrator: 'in this case' means a call that prints an availability report: there the report's stdout line is the one console appearance, and discover_free and probe_go stay silent for the notices that report will list; in calls without such a report the first console print wins. Reason: one sentence, one rule per call kind | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1160 files, 5212 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1188 files, 5536 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/address-notice-once/plan.md` +13 -13
> - `scripts/stage2.py` +21 -6
> - `scripts/stage2_availability.py` +42 -2
> - `scripts/stage2_go.py` +157 -0
> - `tests/test_stage2_go_access.py` +461 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_stage2_go_access.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
>      |
> 1589 |     seeded_round(world, ("free", "flash"), go_store(*(row(member, baseUrl=MOVED_BASE) for member in TEST_LADDER)))
> 1590 |
> 1591 |     def refusing_dispatch(root, member, send, *args, **kwargs):
>      |                                                        ^^^^^^ ARG001
> 1592 |         raise stage2.Refused("the planted dispatch refusal")
>      |
>
> tests/test_stage2_go_access.py:1643:64: ARG001 Unused function argument: `monkeypatch`
>      |
> 1643 | def test_first_address_notice_preserves_text_and_stream(world, monkeypatch, capsys):
>      |                                                                ^^^^^^^^^^^ ARG001
> 1644 |     """Criterion 7: the first printed occurrence keeps its exact wording and its stream.
>      |
>
> tests/test_stage2_go_access.py:1672:40: F821 Undefined name `TEST_FLASH`
>      |
> 1670 |     capsys.readouterr()
> 1671 |     assert world.run("review-loop") == 0
> 1672 |     assert len(world.reviews()) == len(TEST_FLASH), "a suppressed notice stopped or replaced a launch"
>      |                                        ^^^^^^^^^^ F821
> 1673 |     record = world.record().read_text(encoding="utf-8")
> 1674 |     assert f"Address notice: opencode-go/{model}:" in record, "the admitted move left no evidence"
>      |
>
> tests/test_stage2_go_access.py:1817:32: ARG001 Unused function argument: `root`
>      |
> 1815 |     fixture.catalog.tools["drift-free"] = {"id": "drift-free", "tool_call": True}
> 1816 |
> 1817 |     def refusing_probe(runner, root, change, model, *args, **kwargs):
>      |                                ^^^^ ARG001
> 1818 |         raise runner.Refused("the planted probe refusal")
>      |
>
> tests/test_stage2_go_access.py:1817:38: ARG001 Unused function argument: `change`
>      |
> 1815 |     fixture.catalog.tools["drift-free"] = {"id": "drift-free", "tool_call": True}
> 1816 |
> 1817 |     def refusing_probe(runner, root, change, model, *args, **kwargs):
>      |                                      ^^^^^^ ARG001
> 1818 |         raise runner.Refused("the planted probe refusal")
>      |
>
> tests/test_stage2_go_access.py:1817:46: ARG001 Unused function argument: `model`
>      |
> 1815 |     fixture.catalog.tools["drift-free"] = {"id": "drift-free", "tool_call": True}
> 1816 |
> 1817 |     def refusing_probe(runner, root, change, model, *args, **kwargs):
>      |                                              ^^^^^ ARG001
> 1818 |         raise runner.Refused("the planted probe refusal")
>      |
>
> tests/test_stage2_go_access.py:1817:54: ARG001 Unused function argument: `args`
>      |
> 1815 |     fixture.catalog.tools["drift-free"] = {"id": "drift-free", "tool_call": True}
> 1816 |
> 1817 |     def refusing_probe(runner, root, change, model, *args, **kwargs):
>      |                                                      ^^^^ ARG001
> 1818 |         raise runner.Refused("the planted probe refusal")
>      |
>
> tests/test_stage2_go_access.py:1817:62: ARG001 Unused function argument: `kwargs`
>      |
> 1815 |     fixture.catalog.tools["drift-free"] = {"id": "drift-free", "tool_call": True}
> 1816 |
> 1817 |     def refusing_probe(runner, root, change, model, *args, **kwargs):
>      |                                                              ^^^^^^ ARG001
> 1818 |         raise runner.Refused("the planted probe refusal")
>      |
>
> tests/test_stage2_go_access.py:1840:23: ARG001 Unused function argument: `state`
>      |
> 1838 |     monkeypatch.setattr(stage2, "free_diff", lambda _root: ("", ""))
> 1839 |
> 1840 |     def broken_report(state):
>      |                       ^^^^^ ARG001
> 1841 |         raise stage2.Refused("the planted report failure")
>      |
>
> Found 18 errors.
> ```

Stage-2 call, 2026-11-23: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1188 files, 5547 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1188 files, 5550 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash answers unrecognized_model since 2026-11-23 18:16 UTC (bead coding-harness-363r.4); maintainer: Sonnet is back · leak check clean over 1188 files, 5556 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash answers unrecognized_model since 2026-11-23 18:16 UTC (bead coding-harness-363r.4); maintainer: Sonnet is back · leak check clean over 1188 files, 5560 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1188 files, 5578 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/address-notice-once/plan.md` +13 -13
> - `scripts/stage2.py` +23 -6
> - `scripts/stage2_availability.py` +34 -1
> - `scripts/stage2_go.py` +166 -0
> - `tests/test_stage2_go_access.py` +496 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     def mkdir(self, mode=0o777, parents=False, exist_ok=False):
>         """
>         Create a new directory at this given path.
>         """
>         try:
> >           os.mkdir(self, mode)
> E           FileExistsError: [Errno 17] File exists: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3482/popen-gw1/test_address_notice_audits_sur0/repo/plans/changes/demo'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1311: FileExistsError
> __________ ERROR at setup of test_assessment_only_notices_stay_silent __________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3482/popen-gw5/test_assessment_only_notices_s0')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x1089431a0>
>
>     @pytest.fixture
>     def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
>         """A repository, its dedicated worktree, three stand-ins and an environment that belong to the test."""
>         root = tmp_path / "repo"
>         tree = root / ".claude" / "worktrees" / "demo"
> >       (root / "plans" / "changes" / "demo").mkdir(parents=True)
>
> tests/test_stage2_session.py:259: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> self = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3482/popen-gw5/test_assessment_only_notices_s0/repo/plans/changes/demo')
> mode = 511, parents = True, exist_ok = False
>
>     def mkdir(self, mode=0o777, parents=False, exist_ok=False):
>         """
>         Create a new directory at this given path.
>         """
>         try:
> >           os.mkdir(self, mode)
> E           FileExistsError: [Errno 17] File exists: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3482/popen-gw5/test_assessment_only_notices_s0/repo/plans/changes/demo'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1311: FileExistsError
> =================================== FAILURES ===================================
> ______________ test_probe_and_install_audits_keep_address_notices ______________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3482/popen-gw...---|---|---|---|---|---|---|\n| R1 | MAJOR | SPEC | criterion 1 | spec.md:1 | FB1 unique body | Opus 5.5 | open | — |')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x107212540>
> capsys = <_pytest.capture.CaptureFixture object at 0x1071fb2f0>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3482/popen-gw1/test_probe_and_install_audits_0')
>
>     def test_probe_and_install_audits_keep_address_notices(world, monkeypatch, capsys, tmp_path):
>         """Ledger 10: the probe audit and the installation notes keep their lines.
>     
>         Fault: the boundary's printed set filtered the audit list or the
>         installation notes of a notice announced earlier in the call.
>         """
>         moved = TEST_LADDER[0]
>         notice = notice_of(world, moved, baseUrl=MOVED_BASE)
>         store = go_store(row(moved, baseUrl=MOVED_BASE))
>         harness = Harness(world, monkeypatch)
>         agent = tmp_path / "agent"
>         agent.mkdir()
>         policy = stage2_go.load_address_policy(world.root)
>         with stage2_go.console_notice_scope():
>             stage2_go.announce_address_notice(notice, stream=sys.stderr)
>             capsys.readouterr()
>             probe_call, audit = harness.probe(moved, store)
>             probe_call()
>             notes = availability.install_measured_models(None, agent, store, model=moved, address=policy)
>         captured = capsys.readouterr()
> >       assert (captured.out + captured.err).count(notice) == 1, "an audit path printed the notice again"
> E       AssertionError: an audit path printed the notice again
> E       assert 0 == 1
> E        +  where 0 = <built-in method count of str object at 0x10184b1e8>('opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host move')
> E        +    where <built-in method count of str object at 0x10184b1e8> = ('' + '').count
> E        +      where '' = CaptureResult(out='', err='').out
> E        +      and   '' = CaptureResult(out='', err='').err
>
> tests/test_stage2_go_access.py:1762: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_go_access.py::test_probe_and_install_audits_keep_address_notices
> ERROR tests/test_stage2_go_access.py::test_address_notice_audits_survive_console_deduplication
> ERROR tests/test_stage2_go_access.py::test_assessment_only_notices_stay_silent
> 1 failed, 10 passed, 2 errors in 13.20s
> ```

Stage-2 call, 2026-11-23: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1188 files, 5579 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/address-notice-once/plan.md` +13 -13
> - `scripts/stage2_go.py` +36 -38
> - `tests/test_stage2_go_access.py` +20 -2
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_stage2_go_access.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> EE...........                                                            [100%]
> ==================================== ERRORS ====================================
> __ ERROR at setup of test_address_notice_audits_survive_console_deduplication __
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/.venv/bin/python3
> Fixture "world" called directly. Fixtures are not meant to be called directly,
> but are created automatically when test functions request them as parameters.
> See https://docs.pytest.org/en/stable/explanation/fixtures.html for more information about fixtures, and
> https://docs.pytest.org/en/stable/deprecations.html#calling-fixtures-directly about how to update your code.
> __________ ERROR at setup of test_assessment_only_notices_stay_silent __________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/.venv/bin/python3
> Fixture "world" called directly. Fixtures are not meant to be called directly,
> but are created automatically when test functions request them as parameters.
> See https://docs.pytest.org/en/stable/explanation/fixtures.html for more information about fixtures, and
> https://docs.pytest.org/en/stable/deprecations.html#calling-fixtures-directly about how to update your code.
> =========================== short test summary info ============================
> ERROR tests/test_stage2_go_access.py::test_address_notice_audits_survive_console_deduplication
> ERROR tests/test_stage2_go_access.py::test_assessment_only_notices_stay_silent
> 11 passed, 2 errors in 12.70s
> ```

Stage-2 call, 2026-11-23: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1188 files, 5580 commits, 12 rules.

Stage-2 call, 2026-11-24: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1188 files, 5596 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/address-notice-once/plan.md` +13 -13
> - `scripts/stage2.py` +23 -6
> - `scripts/stage2_availability.py` +20 -3
> - `scripts/stage2_go.py` +144 -0
> - `tests/test_stage2_go_access.py` +510 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `tests/test_stage2_go_access.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_stage2_go_access.py:1485:58: ARG001 Unused function argument: `monkeypatch`
>      |
> 1485 | def test_distinct_address_notices_each_print_once(world, monkeypatch, capsys):
>      |                                                          ^^^^^^^^^^^ ARG001
> 1486 |     """Criterion 2: distinct notices — another model, path pair, wire api or kind — are never suppressed.
>      |
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-24: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1188 files, 5597 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/address-notice-once/plan.md` +13 -13
> - `scripts/stage2.py` +2 -1
> - `scripts/stage2_availability.py` +3 -1
> - `tests/test_stage2_go_access.py` +30 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> >       assert (read.out + read.err).count(notice) == 2, "a direct call lost or shared another call's suppression"
> E       AssertionError: a direct call lost or shared another call's suppression
> E       assert 4 == 2
> E        +  where 4 = <built-in method count of str object at 0x7ad6be8300>('opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host move')
> E        +    where <built-in method count of str object at 0x7ad6be8300> = ('Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inferenc...sh: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host move\n' + 'Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inferenc...sh: the recorded base path is /zen/go/v1, the definition na [… 67 characters left out …]
> E        +      where 'Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inferenc...sh: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host move\n' = CaptureResult(out='Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definiti...h: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host mov [… 9 characters left out …]
> E        +      and   'Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inferenc...sh: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host move\n' = CaptureResult(out='Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definiti...h: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host mov [… 9 characters left out …]
>
> tests/test_stage2_go_access.py:1840: AssertionError
> _____________ test_first_address_notice_preserves_text_and_stream ______________
> [gw10] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3496/popen-gw...---|---|---|---|---|---|---|\n| R1 | MAJOR | SPEC | criterion 1 | spec.md:1 | FB1 unique body | Opus 5.5 | open | — |')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10a67ce00>
> capsys = <_pytest.capture.CaptureFixture object at 0x10acef1a0>
>
>     def test_first_address_notice_preserves_text_and_stream(world, monkeypatch, capsys):
>         """Criterion 7: the first printed occurrence keeps its exact text and its site's stream.
>     
>         Fault: the first announcement was reworded, or a suppressed site's stream
>         won — the notice moved between stdout and stderr.
>         """
>         model = TEST_LADDER[0]
>         # The reviewer announces first: stderr keeps the line, stdout stays clean.
>         state = loop_state(consumed=("free",))
>         state["free"]["models_store"] = go_store(*(row(member, baseUrl=MOVED_BASE) for member in TEST_LADDER))
>         world.write_record([RESUMED_NOTE], state=state)
>         world.script(pi=[{"stdout": "No finding."}] * len(TEST_FLASH))
>         notice = notice_for(world, model, baseUrl=MOVED_BASE)
>         capsys.readouterr()
>         assert world.run("review-loop") == 0
>         read = capsys.readouterr()
>         assert (read.out + read.err).count(notice) == 1
>         assert f"Address notice: {notice}" in read.err, "the first announcement changed its text or stream"
>         assert notice not in read.out, "the notice moved to stdout"
>         # The dispatch announces first: activation saw a known path, the record moved back.
>         rung = TEST_RUNGS[0]
>         state = loop_state(consumed=("free", "flash"))
>         state["free"]["models_store"] = go_store(*(row(member, baseUrl=MOVED_BASE) for member in TEST_LADDER))
>         world.write_record([RESUMED_NOTE], state=state)
>         edit_entry(world, lambda e: e["adresse"]["apis"]["openai-completions"].update(basis=MOVED_BASE))
>         real_check = stage2.check_overlay
>     
>         def check_then_move(*args, **kwargs):
>             real_check(*args, **kwargs)
>             edit_entry(world, lambda e: e["adresse"]["apis"]["openai-completions"].update(basis=RECORDED_BASE))
>     
>         monkeypatch.setattr(stage2, "check_overlay", check_then_move)
>         world.script(pi=[{"stdout": "No finding."}])
> >       rung_notice = notice_for(world, rung, baseUrl=MOVED_BASE)
>
> tests/test_stage2_go_access.py:1704: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> w = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3496/popen-gw...---|---|---|---|---|---|---|\n| R1 | MAJOR | SPEC | criterion 1 | spec.md:1 | FB1 unique body | Opus 5.5 | open | — |')
> model = 'mimo-v2.6-pro'
> row_changes = {'baseUrl': 'https://opencode.ai/inference/go/v1'}
> root = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3496/popen-gw10/test_first_address_notice_pres0/repo')
> policy = AddressPolicy(host='opencode.ai', apis={'openai-completions': BaseRecord(api='openai-completions', base='https://opencode.ai/inference/go/v1', source='the synthetic test record (go-access-point)', read='2026-10-31')})
> verdict = Assessment(definition={'id': 'mimo-v2.6-pro', 'name': 'mimo-v2.6-pro', 'provider': 'opencode-go', 'api': 'openai-compl... 'output': 0, 'cacheRead': 0, 'cacheWrite': 0}, 'contextWindow': 128000, 'maxTokens': 4096}, notice=None, problem=None)
> @py_assert1 = None
> @py_format3 = "the planted drift produced no notice\n>assert None\n{None = Assessment(definition={'id': 'mimo-v2.6-pro', 'name': 'mi...0, 'cacheRead': 0, 'cacheWrite': 0}, 'contextWindow': 128000, 'maxTokens': 4096}, notice=None, problem=None).notice\n}"
>
>     def notice_for(w, model: str, **row_changes: object) -> str:
>         """The exact assessment notice for one row shape against this world's record."""
>         root = getattr(w, "tree", w.root)
>         policy = stage2_go.load_address_policy(root)
>         verdict = stage2_go.assess(policy, model, row(model, **row_changes))
> >       assert verdict.notice, "the planted drift produced no notice"
> E       AssertionError: the planted drift produced no notice
> E       assert None
> E        +  where None = Assessment(definition={'id': 'mimo-v2.6-pro', 'name': 'mimo-v2.6-pro', 'provider': 'opencode-go', 'api': 'openai-compl... 'output': 0, 'cacheRead': 0, 'cacheWrite': 0}, 'contextWindow': 128000, 'maxTokens': 4096}, notice=None, problem=None).notice
>
> tests/test_stage2_go_access.py:1414: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_go_access.py::test_direct_calls_keep_notice_output
> FAILED tests/test_stage2_go_access.py::test_first_address_notice_preserves_text_and_stream
> ERROR tests/test_stage2_go_access.py::test_address_notice_audits_survive_console_deduplication
> ERROR tests/test_stage2_go_access.py::test_assessment_only_notices_stay_silent
> 2 failed, 9 passed, 2 errors in 12.41s
> ```

Stage-2 call, 2026-11-24: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1188 files, 5597 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2_go_access.py` +27 -17
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         w = session_world
>         w.declare_go()
>         catalog = w.bin / "node_modules/@earendil-works/pi-ai/dist/providers/data/opencode-go.json"
>         data = json.loads(catalog.read_text(encoding="utf-8"))
>         data["openai-completions"][f"chat:{GO_BARE}"]["baseUrl"] = MOVED_BASE
>         catalog.write_text(json.dumps(data), encoding="utf-8")
>     
>         def refusing_confirm(*_args, **_kwargs):
>             raise stage2.Refused("planted: the binding confirmation refused")
>     
>         monkeypatch.setattr(stage2_session, "confirm_binding", refusing_confirm)
>         w.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
>         session_notice = notice_for(w, GO_BARE, baseUrl=MOVED_BASE)
>         assert w.run(model=GO_MODEL) == 2
>         read = capsys.readouterr()
>         assert "planted" in read.err
>         assert w.bindings == []
>         assert session_notice not in read.out + read.err, "a refused binding printed its assessment-only notice"
>         # Research preparation fails before its report: a catalog drift that no
>         # probe would announce stays in the selection state, off the console.
>         from test_stage2_research_availability import Fixture
>     
>         # The two world fixtures share one temporary directory, so the review world
>         # is built by the fixture's own function in a directory beside it.
>         research_dir = tmp_path / "research-world"
>         research_dir.mkdir()
>         world = stage2_world.__pytest_wrapped__.obj(research_dir, monkeypatch)
>         fx = Fixture(world, monkeypatch)
>         for item in fx.catalog.pi:
>             if item["id"] == "nocost-model":
>                 item["baseUrl"] = MOVED_BASE
>         nocost = notice_for(world, "nocost-model", baseUrl=MOVED_BASE)
>         real_launch = stage2.launch
>         probes = 0
>     
>         def refuse_second_probe(command, *args, **kwargs):
>             nonlocal probes
>             if "--print" in command:
>                 probes += 1
>                 if probes == 2:
>                     raise stage2.Refused("planted: the second probe refused")
>             return real_launch(command, *args, **kwargs)
>     
>         monkeypatch.setattr(stage2, "launch", refuse_second_probe)
>         capsys.readouterr()
> >       assert fx.prepare() == 2
>
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/tests/test_stage2_go_access.py:1902: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/tests/test_stage2_research_availability.py:258: in prepare
>     return self.w.run("prepare-explore", "demo", *options)
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/tests/test_stage2.py:419: in run
>     return stage2.main([*argv, *options, "--root", str(self.root)])
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2.py:13838: in main
>     return _run(args)
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2.py:13934: in _run
>     prepare_explore(Path(args.root), args.change, args.klass, args.seats)
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2.py:11056: in prepare_explore
>     stage2_availability.prepare_research(root, change, sys.modules[__name__], klass, seat_choice(seats))
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2_availability.py:1037: in wrapped
>     return prepare(root, change, runner, *args, **kwargs)
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2_availability.py:1204: in prepare_research
>     chosen = {label: selection.fill(label, trio) for label, trio in seats.items()}
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2_availability.py:932: in fill
>     if self.usable(endpoint, model, data_class) and self.reachable(endpoint, model, data_class):
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2_availability.py:898: in reachable
>     self.key = self.runner.reviewer_key()
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/scripts/stage2.py:3182: in reviewer_key
>     key = read_secret("OPENCODE_GO_KEY")
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'OPENCODE_GO_KEY'
>
> >   monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"session read a secret: {name}"))
> E   Failed: session read a secret: OPENCODE_GO_KEY
>
> /Users/mikypiky/coding-harness/.claude/worktrees/address-notice-once/tests/test_stage2_session.py:331: Failed
> =========================== short test summary info ============================
> FAILED tests/test_stage2_go_access.py::test_assessment_only_notices_stay_silent
> 1 failed, 12 passed in 12.14s
> ```
