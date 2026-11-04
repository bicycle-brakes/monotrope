---
title: "Findings — handoff-new-feature"
category: findings
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-in27
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — handoff-new-feature

Stage-2 call, 2026-11-04: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 889 files, 3262 commits, 12 rules.

Stage-2 call, 2026-11-04: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 892 files, 3264 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +24 -2
> - `plans/INDEX.md` +2 -2
> - `plans/changes/handoff-new-feature/plan.md` +10 -10
> - `plans/changes/handoff-new-feature/spec.md` +1 -1
> - `scripts/check_research_handoff.py` +191 -32
> - `tests/test_research_handoff.py` +291 -10
> - `tests/test_stage2_swarm.py` +7 -1
> - `tests/test_this_repository_adoption.py` +4 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> scripts/check_research_handoff.py:598:85: ARG001 Unused function argument: `ident`
>     |
> 596 |             return result.get(name) if isinstance(result, dict) else None
> 597 |
> 598 |         def value(name: str, body: list[str] = body, found: dict[str, int] = found, ident: str = ident) -> str:
>     |                                                                                     ^^^^^ ARG001
> 599 |             if name not in found:
> 600 |                 return ""
>     |
>
> scripts/check_research_handoff.py:602:27: B023 Function definition does not bind loop variable `loaded`
>     |
> 600 |                 return ""
> 601 |             if name == "answer":
> 602 |                 content = loaded(name)
>     |                           ^^^^^^ B023
> 603 |                 if isinstance(content, list | dict) and not content:
> 604 |                     return ""
>     |
>
> Found 2 errors.
> ```

Stage-2 call, 2026-11-04: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 892 files, 3269 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/check_research_handoff.py` +9 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> root = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/handoff-new-feature')
> gate = 'research-handoff'
>
>     def adopted_on(root: Path, gate: str) -> date:
>         """The day `root` adopted `gate`, or NotRecorded."""
>         path = root / RECORD
>         try:
>             text = path.read_bytes().decode("utf-8")
>         except FileNotFoundError:
>             raise NotRecorded(f"{RECORD} does not exist — {_remedy(gate)}") from None
>         except (OSError, UnicodeDecodeError) as exc:
>             raise NotRecorded(f"{RECORD} cannot be read ({exc}) — {_remedy(gate)}") from None
>         try:
>             data = check_adr_answers.strict_load(text)
>         except (yaml.YAMLError, ValueError) as exc:  # ValueError: an impossible date such as 2026-02-30
>             raise NotRecorded(f"{RECORD} is not valid YAML ({' '.join(str(exc).split())}) — {_remedy(gate)}") from None
>         if not isinstance(data, dict):
>             raise NotRecorded(f"{RECORD} is not a YAML mapping — {_remedy(gate)}")
>         version = data.get("schema_version")
>         if not (type(version) is int and version == 1):
>             raise NotRecorded(f"{RECORD} lacks `schema_version: 1` (it holds {version!r}) — {_remedy(gate)}")
>         adopted = data.get("adopted")
>         if not isinstance(adopted, dict):
>             raise NotRecorded(f"{RECORD} has no `adopted:` mapping — {_remedy(gate)}")
>         if gate not in adopted:
> >           raise NotRecorded(f"{RECORD} holds no day for {gate} — {_remedy(gate)}")
> E           adoption.NotRecorded: decisions/adoption.yaml holds no day for research-handoff — decisions/adoption.yaml needs `schema_version: 1` and, under `adopted:`, the line `  research-handoff: YYYY-MM-DD` (unquoted)
>
> scripts/adoption.py:63: NotRecorded
> ______ test_only_a_reasoned_maintainer_exception_waives_missing_research _______
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/handoff-new-feature/.venv/bin/python3
>
> world = <test_research_handoff.World object at 0x10a975a30>
> capsys = <_pytest.capture.CaptureFixture object at 0x10a975520>
>
>     def test_only_a_reasoned_maintainer_exception_waives_missing_research(
>         world: World, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         # Criterion 4 (bead coding-harness-in27). Planted fault: an agent answer, an open status, a missing
>         # context, a blank answer, a false or reasonless grant still waives the swarm, or the valid grant hides
>         # its question or reason in the output.
>     
>         def case(**kwargs):
>             field = kwargs.pop("field", GRANT)
>             record = q_record(1, answer="the swarm is skipped", exception=field, **kwargs)
>             world.write([], records=[record], spec=spec_text(), research=False)
>             return world.check(capsys)
>     
>         code, out = case()
>         assert code == 0, out
>         assert "Q-1" in out and "the swarm is skipped for this docs-only repair" in out
>         for kwargs in (
>             {"answered_by": "agent"},
>             {"status": "open"},
>             {"context": False},
>             {"answer": ""},
>             {"field": 'research_swarm_exception: {granted: false, reason: "no"}'},
>             {"field": 'research_swarm_exception: {reason: "only a reason"}'},
>             {"field": 'research_swarm_exception: {granted: true, reason: "   "}'},
>         ):
> >           code, out = case(**kwargs)
>
> tests/test_research_handoff.py:1229: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> kwargs = {'answer': ''}
> field = 'research_swarm_exception: {granted: true, reason: "the swarm is skipped for this docs-only repair"}'
>
>     def case(**kwargs):
>         field = kwargs.pop("field", GRANT)
> >       record = q_record(1, answer="the swarm is skipped", exception=field, **kwargs)
> E       TypeError: test_research_handoff.q_record() got multiple values for keyword argument 'answer'
>
> tests/test_research_handoff.py:1213: TypeError
> =========================== short test summary info ============================
> FAILED tests/test_this_repository_adoption.py::test_this_repository_adopted_research_handoff_on_2026_10_26
> FAILED tests/test_research_handoff.py::test_only_a_reasoned_maintainer_exception_waives_missing_research
> 2 failed, 18 passed in 0.91s
> ```

Stage-2 call, 2026-11-04: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 892 files, 3269 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_research_handoff.py` +2 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ................F...                                                     [100%]
> =================================== FAILURES ===================================
> _________ test_this_repository_adopted_research_handoff_on_2026_10_26 __________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/handoff-new-feature/.venv/bin/python3
>
>     def test_this_repository_adopted_research_handoff_on_2026_10_26() -> None:
> >       assert adoption.adopted_on(REPO_ROOT, "research-handoff") == date(2026, 10, 26)
>
> tests/test_this_repository_adoption.py:28: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> root = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/handoff-new-feature')
> gate = 'research-handoff'
>
>     def adopted_on(root: Path, gate: str) -> date:
>         """The day `root` adopted `gate`, or NotRecorded."""
>         path = root / RECORD
>         try:
>             text = path.read_bytes().decode("utf-8")
>         except FileNotFoundError:
>             raise NotRecorded(f"{RECORD} does not exist — {_remedy(gate)}") from None
>         except (OSError, UnicodeDecodeError) as exc:
>             raise NotRecorded(f"{RECORD} cannot be read ({exc}) — {_remedy(gate)}") from None
>         try:
>             data = check_adr_answers.strict_load(text)
>         except (yaml.YAMLError, ValueError) as exc:  # ValueError: an impossible date such as 2026-02-30
>             raise NotRecorded(f"{RECORD} is not valid YAML ({' '.join(str(exc).split())}) — {_remedy(gate)}") from None
>         if not isinstance(data, dict):
>             raise NotRecorded(f"{RECORD} is not a YAML mapping — {_remedy(gate)}")
>         version = data.get("schema_version")
>         if not (type(version) is int and version == 1):
>             raise NotRecorded(f"{RECORD} lacks `schema_version: 1` (it holds {version!r}) — {_remedy(gate)}")
>         adopted = data.get("adopted")
>         if not isinstance(adopted, dict):
>             raise NotRecorded(f"{RECORD} has no `adopted:` mapping — {_remedy(gate)}")
>         if gate not in adopted:
> >           raise NotRecorded(f"{RECORD} holds no day for {gate} — {_remedy(gate)}")
> E           adoption.NotRecorded: decisions/adoption.yaml holds no day for research-handoff — decisions/adoption.yaml needs `schema_version: 1` and, under `adopted:`, the line `  research-handoff: YYYY-MM-DD` (unquoted)
>
> scripts/adoption.py:63: NotRecorded
> =========================== short test summary info ============================
> FAILED tests/test_this_repository_adoption.py::test_this_repository_adopted_research_handoff_on_2026_10_26
> 1 failed, 19 passed in 1.44s
> ```
