---
title: "Findings — explorer-reviewer-agents"
category: findings
status: draft
implementation_status: none
date: 2026-11-01
created: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-9ll
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — explorer-reviewer-agents

Stage-2 call, 2026-11-01: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 802 files, 2940 commits, 12 rules.

Stage-2 call, 2026-11-01: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 805 files, 2956 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +11 -10
> - `scripts/kit/probe.py` +9 -1
> - `tests/test_explorer_reviewer_agents.py` +363 -0
> - `tests/test_workflow_entry.py` +11 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_explorer_reviewer_agents.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> _________________ test_helpers_state_read_only_reporting_roles _________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.venv/bin/python3
>
>     def test_helpers_state_read_only_reporting_roles() -> None:
>         """Criterion 4: the instructions state the reporting roles and the prohibitions.
>     
>         The explorer reports source-backed findings and explicit unknowns; the
>         reviewer reports findings against the supplied spec and evidence. Neither
>         authorizes repairs, commits, tracker writes or accepting its own work.
>         Refuted by removing the role or authorizing any of the four.
>         """
>         for name in ("explorer", "reviewer"):
> >           frontmatter, body = _definition(name)
>
> tests/test_explorer_reviewer_agents.py:224: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'explorer'
>
>     def _definition(name: str) -> tuple[dict, str]:
>         """The definition's frontmatter and body — a missing file fails, never skips."""
>         path = AGENTS / f"{name}.md"
> >       assert path.is_file(), (
>             f"{path} is missing. The change holds the two definitions until the accepted "
>             "attempt and the orchestrator installs them after it; until then this failure "
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> _________________________ test_reviewer_pins_opus_high _________________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.venv/bin/python3
>
>     def test_reviewer_pins_opus_high() -> None:
>         """Criterion 2: the configuration selects Claude Opus 5.5 at high effort.
>     
>         Refuted by removing the definition, writing another model, or dropping or
>         changing the effort.
>         """
> >       frontmatter, _ = _definition("reviewer")
>
> tests/test_explorer_reviewer_agents.py:198: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'reviewer'
>
>     def _definition(name: str) -> tuple[dict, str]:
>         """The definition's frontmatter and body — a missing file fails, never skips."""
>         path = AGENTS / f"{name}.md"
> >       assert path.is_file(), (
>             f"{path} is missing. The change holds the two definitions until the accepted "
>             "attempt and the orchestrator installs them after it; until then this failure "
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/reviewer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/reviewer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_explorer_reviewer_agents.py::test_helpers_allow_read_tools_only
> FAILED tests/test_explorer_reviewer_agents.py::test_explorer_pins_haiku - Ass...
> FAILED tests/test_explorer_reviewer_agents.py::test_helpers_state_read_only_reporting_roles
> FAILED tests/test_explorer_reviewer_agents.py::test_reviewer_pins_opus_high
> 4 failed, 32 passed in 0.79s
> ```

Stage-2 call, 2026-11-01: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 806 files, 2957 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/explorer-reviewer-agents/plan.md` +4 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> _________________ test_helpers_state_read_only_reporting_roles _________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.venv/bin/python3
>
>     def test_helpers_state_read_only_reporting_roles() -> None:
>         """Criterion 4: the instructions state the reporting roles and the prohibitions.
>     
>         The explorer reports source-backed findings and explicit unknowns; the
>         reviewer reports findings against the supplied spec and evidence. Neither
>         authorizes repairs, commits, tracker writes or accepting its own work.
>         Refuted by removing the role or authorizing any of the four.
>         """
>         for name in ("explorer", "reviewer"):
> >           frontmatter, body = _definition(name)
>
> tests/test_explorer_reviewer_agents.py:224: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'explorer'
>
>     def _definition(name: str) -> tuple[dict, str]:
>         """The definition's frontmatter and body — a missing file fails, never skips."""
>         path = AGENTS / f"{name}.md"
> >       assert path.is_file(), (
>             f"{path} is missing. The change holds the two definitions until the accepted "
>             "attempt and the orchestrator installs them after it; until then this failure "
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> _________________________ test_reviewer_pins_opus_high _________________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.venv/bin/python3
>
>     def test_reviewer_pins_opus_high() -> None:
>         """Criterion 2: the configuration selects Claude Opus 5.5 at high effort.
>     
>         Refuted by removing the definition, writing another model, or dropping or
>         changing the effort.
>         """
> >       frontmatter, _ = _definition("reviewer")
>
> tests/test_explorer_reviewer_agents.py:198: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'reviewer'
>
>     def _definition(name: str) -> tuple[dict, str]:
>         """The definition's frontmatter and body — a missing file fails, never skips."""
>         path = AGENTS / f"{name}.md"
> >       assert path.is_file(), (
>             f"{path} is missing. The change holds the two definitions until the accepted "
>             "attempt and the orchestrator installs them after it; until then this failure "
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/reviewer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/reviewer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_explorer_reviewer_agents.py::test_helpers_allow_read_tools_only
> FAILED tests/test_explorer_reviewer_agents.py::test_explorer_pins_haiku - Ass...
> FAILED tests/test_explorer_reviewer_agents.py::test_helpers_state_read_only_reporting_roles
> FAILED tests/test_explorer_reviewer_agents.py::test_reviewer_pins_opus_high
> 4 failed, 32 passed in 0.80s
> ```

Stage-2 call, 2026-11-01: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 806 files, 2958 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> _________________________ test_reviewer_pins_opus_high _________________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.venv/bin/python3
>
>     def test_reviewer_pins_opus_high() -> None:
>         """Criterion 2: the configuration selects Claude Opus 5.5 at high effort.
>     
>         Refuted by removing the definition, writing another model, or dropping or
>         changing the effort.
>         """
> >       frontmatter, _ = _definition("reviewer")
>
> tests/test_explorer_reviewer_agents.py:198: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'reviewer'
>
>     def _definition(name: str) -> tuple[dict, str]:
>         """The definition's frontmatter and body — a missing file fails, never skips."""
>         path = AGENTS / f"{name}.md"
> >       assert path.is_file(), (
>             f"{path} is missing. The change holds the two definitions until the accepted "
>             "attempt and the orchestrator installs them after it; until then this failure "
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/reviewer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/reviewer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> _________________ test_helpers_state_read_only_reporting_roles _________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.venv/bin/python3
>
>     def test_helpers_state_read_only_reporting_roles() -> None:
>         """Criterion 4: the instructions state the reporting roles and the prohibitions.
>     
>         The explorer reports source-backed findings and explicit unknowns; the
>         reviewer reports findings against the supplied spec and evidence. Neither
>         authorizes repairs, commits, tracker writes or accepting its own work.
>         Refuted by removing the role or authorizing any of the four.
>         """
>         for name in ("explorer", "reviewer"):
> >           frontmatter, body = _definition(name)
>
> tests/test_explorer_reviewer_agents.py:224: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> name = 'explorer'
>
>     def _definition(name: str) -> tuple[dict, str]:
>         """The definition's frontmatter and body — a missing file fails, never skips."""
>         path = AGENTS / f"{name}.md"
> >       assert path.is_file(), (
>             f"{path} is missing. The change holds the two definitions until the accepted "
>             "attempt and the orchestrator installs them after it; until then this failure "
>             "is the expected pre-bootstrap state. A green check over a missing definition "
>             "would promise a helper that does not exist."
>         )
> E       AssertionError: /Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md is missing. The change holds the two definitions until the accepted attempt and the orchestrator installs them after it; until then this failure is the expected pre-bootstrap state. A green check over a missing definition would promise a helper that does not exist.
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/explorer-reviewer-agents/.claude/agents/explorer.md').is_file
>
> tests/test_explorer_reviewer_agents.py:79: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_explorer_reviewer_agents.py::test_explorer_pins_haiku - Ass...
> FAILED tests/test_explorer_reviewer_agents.py::test_helpers_allow_read_tools_only
> FAILED tests/test_explorer_reviewer_agents.py::test_reviewer_pins_opus_high
> FAILED tests/test_explorer_reviewer_agents.py::test_helpers_state_read_only_reporting_roles
> 4 failed, 32 passed in 0.84s
> ```
