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

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 808 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 808 files, 2966 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 808 files, 2966 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 808 files, 2966 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 808 files, 2966 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 808 files, 2967 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 808 files, 2967 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 808 files, 2967 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 808 files, 2968 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 808 files, 2968 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 808 files, 2968 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 808 files, 2968 commits, 12 rules.

## Fresh-session model observation — 2026-11-01

Plan step 4, spec criterion 6 (review rows L1-1, L1-8, L1-14, L1-17). Checked
commit: 0abbc5b8 on `feat/explorer-reviewer-agents`, Claude Code 2.1.314,
run from the change's worktree by the orchestrating session.

| Helper | Command | Observed model (`modelUsage` of the JSON result) | Result |
|---|---|---|---|
| explorer | `claude --agent explorer -p "Reply with the single word ok. Do not use any tool." --output-format json` | `claude-haiku-5-5` | pass |
| reviewer | `claude --agent reviewer -p "Reply with the single word ok. Do not use any tool." --output-format json` | `claude-opus-5-5` | pass for the model |

Delegated from a parent on another model (phase-6 row P6-1), 2026-11-01,
Claude Code 2.1.316, same worktree, parent `claude -p --model
claude-sonnet-5-5 --allowedTools Agent --output-format json`, told to call the
Agent tool once with the helper as `subagent_type` and the prompt "Reply with
the single word ok. Do not use any tool.":

| Helper | Parent model | Models in `modelUsage` | Result |
|---|---|---|---|
| explorer | `claude-sonnet-5-5` | `claude-haiku-5-5`, `claude-sonnet-5-5` | pass: the child ran on Haiku 5.5, not the parent's model |
| reviewer | `claude-sonnet-5-5` | `claude-opus-5-5`, `claude-sonnet-5-5` | pass for the model: the child ran on Opus 5.5 |

Not observed: the reviewer's effort `high`. The JSON result names no effort
field, and `/status` is interactive; the effort is an accepted limit of this
observation, named in the pull request.

Stage-2 call, 2026-11-01: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 808 files, 2977 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model hy3 · leak check clean over 808 files, 2991 commits, 12 rules.

Stage-2 call, 2026-11-01: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 808 files, 2992 commits, 12 rules.

## Phase 6 — Codex, 2026-11-01

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| P6-1 | MAJOR | SPEC | Phase 6 | plans/changes/explorer-reviewer-agents/findings.md:355 | Both recorded checks run the helper directly through `claude --agent` and prohibit tool use; neither invokes a delegated helper from a parent using a different model. These checks can pass while delegated helpers still inherit the parent's model—the failure this observation must detect. Record both child-model observations from differently configured parents before marking this requirement passed. [Acceptance criterion 6; plan step 4] | Codex | fixed — not a test — both helpers observed delegated from a Sonnet 5.5 parent: explorer on Haiku 5.5, reviewer on Opus 5.5 (fresh-session model observation, 2026-11-01) | no — not a test |

Phase 6 verdict: codex 01a1987d-52fb-71f2-ae4b-2d39c8f5c743, 2026-11-01
Reviewer session: codex 01a1987d-52fb-71f2-ae4b-2d39c8f5c743 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-01

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | spec.md Definition of Done; plan.md step 4 | plans/changes/explorer-reviewer-agents/findings.md | The Definition of Done and plan step 4 require both fresh-session model observations, their commands and the checked commit in `findings.md`, and say an unobserved model is not a pass; the file holds only stage-2 call lines and availability probes, so criterion 6 is unproven and the change reports itself complete without it. | deepseek-v4.1-flash | fixed — not a test — findings.md records the fresh-session observation: explorer claude-haiku-5-5, reviewer claude-opus-5-5; the effort is named as not observed (51ccf6fd) | no — not a test | agree |
| L1-2 | MAJOR | SPEC | plan.md "Execution boundary" | plans/changes/explorer-reviewer-agents/decisions.md (Details for the draft) and plan.md ("Scope answer") | The plan says the maintainer's scope answer is recorded in `decisions.md` before implementation, but the answer is recorded only in `plan.md`, while `decisions.md` still states "Only the two agent files and a test that reads them" although the change also edits `docs/WORKFLOW.md`, `tests/test_workflow_entry.py` and `scripts/kit/probe.py`; the two artefacts contradict each other about the permitted scope. | deepseek-v4.1-flash | fixed — not a test — decisions.md carries the scope answer as Q-2; the old detail is marked superseded (51ccf6fd) | no — not a test | agree |
| L1-3 | MAJOR | SPEC | spec.md "Open decisions" (scope answer); plan.md "Do not touch" | tests/test_kit.py (phase-name check) | The scope answer names exactly three companion files and the plan forbids gate-policy changes, but the change also edits `tests/test_kit.py`: it strips `explorer.md` and `reviewer.md` from every kit file before counting phase names, widening the existing guard against a second phase description with no plan or decision line. | deepseek-v4.1-flash | fixed — not a test — decisions.md Q-2 names the kit phase-name edit as part of the admitted kit bookkeeping (51ccf6fd) | no — not a test | disagree — Necessary kit-test maintenance falls within the approved complete delivery; the overly broad masking is separately covered by L1-20. |
| L1-4 | MINOR | MAINT | research.md body | plans/changes/explorer-reviewer-agents/research.md | The file still tells the reader its frontmatter says `provenance: human-written` and that it is "empty until it has run", while the frontmatter says `ai-drafted-reviewed` with `produced_by` and `review` and the body is filled; a reader cannot tell which statement is current. | deepseek-v4.1-flash | fixed — not a test — the skeleton's provenance note is removed (51ccf6fd) | no — not a test | agree |
| L1-5 | MINOR | MAINT | docs/WORKFLOW.md header notice; spec.md step 3 | docs/WORKFLOW.md (header notice) | The notice says the check ran against the tree at `1eb84b6b` "with the delivery", but that commit is the scope-answer commit and the two helper definitions first appear in a later commit; at the cited tree the helpers are still absent, so the "supplied" claim cannot be verified there and the spec records a different baseline commit. | deepseek-v4.1-flash | fixed — not a test — the notice cites 8ae99e50, the commit that delivers the definitions (51ccf6fd) | no — not a test | agree |
| L1-6 | MINOR | MAINT | spec.md criterion 4 | tests/test_explorer_reviewer_agents.py (`_role_problems`, `CUE`) | The role guard counts `only` as a prohibition cue although its own comment defines a cue as a negation or an attribution to someone else; a role sentence such as "You only repair what you find" therefore passes the check that criterion 4 says must reject an authorization to repair, and no fixture covers that form. | deepseek-v4.1-flash | fixed — not a test — `only` entfernt; die neue Reparatur-Fixture scheiterte zuvor und besteht jetzt. | no — not a test | agree |
| L1-7 | MINOR | SPEC | plan.md card (appetite) | plans/changes/explorer-reviewer-agents/plan.md ("Time used") | The card sets a one-hour appetite and says to stop at the limit, but the three recorded attempts add up to well over an hour and nothing records a stop or a decision to continue past it. | deepseek-v4.1-flash | fixed — not a test — plan.md states the 79 min against the one-hour appetite and the hand acceptance (51ccf6fd) | no — not a test | agree |
| L1-8 | MAJOR | SPEC | round-1 swarm | plans/changes/explorer-reviewer-agents/findings.md (whole file); spec.md "Definition of Done", criterion 6 | The change promises that both fresh-session model observations (explorer on Haiku 5.5, reviewer on Opus 5.5 high, checked with `/status`) are recorded in findings.md against the checked commit, and that an unavailable observation is not a pass. findings.md contains only stage-2 audit lines and three failed-attempt diagnostics — no session observation, no command, and no "not measured" record for either helper. Criterion 6 and its ledger entry ("a mismatched or unobserved child model prevents completion") are unmet, so the change cannot be reported complete as its own DoD requires. | mimo-v2.6-flash | fixed — not a test — findings.md records the fresh-session observation: explorer claude-haiku-5-5, reviewer claude-opus-5-5; the effort is named as not observed (51ccf6fd) | no — not a test | agree |
| L1-9 | MAJOR | MAINT | round-1 swarm | spec.md "Protected areas" and "Open decisions"; decisions.md; plan.md "Scope answer — 2026-11-01" | The companion maintenance is delivered while the governing records still say it is not allowed: spec.md states "The workflow notice, its test and kit bookkeeping remain outside the recorded scope until the open scope decision is answered" and lists the scope decision as open with "no maintainer answer is inferred", yet the diff rewrites docs/WORKFLOW.md's notice, moves tests/test_workflow_entry.py's assertions, and raises scripts/kit/probe.py's DECKEL from 42 to 44. The answer exists only in plan.md's "Scope answer" section; the plan itself required "Record the maintainer's actual answer in decisions.md before implementation", and decisions.md carries no answered scope question — its [DETAIL] still says only the two agent files and a test are delivered. A maintainer who was not there reads three artefacts that contradict the tree. | mimo-v2.6-flash | fixed — not a test — spec.md says the scope is answered (Q-2) in Protected areas and Open decisions (51ccf6fd) | no — not a test | agree |
| L1-10 | MAJOR | MAINT | round-1 swarm | docs/WORKFLOW.md lines 528–531 (§4, "Codex at capacity"); .claude/agents/reviewer.md line 1–17 | The workflow still routes the Codex-unavailable phase-6 path through a different model than the one this change installs: WORKFLOW.md §4 night rule 1 sends the phase-6 review or re-check "through a read-only Sonnet 5.5 sub-agent whose rows the orchestrator records unchanged", while reviewer.md describes itself as "the phase-6 fallback when Codex is not available" and pins claude-opus-5-5 at effort high. The change updated only the header notice, so both texts stay live and name two models for the same fallback; neither §4 nor §9's "does the sub-agents' model assignment take hold?" was reconciled with the new definition. | mimo-v2.6-flash | rejected — false: reviewer.md names the §3 path (daytime, Codex unavailable; phase 6 on Opus 5.5 as the model table says); WORKFLOW §4 night rule 1 is a separate case (Codex at capacity at night, Sonnet 5.5) and names no helper file |  | agree |
| L1-11 | MINOR | MAINT | round-1 swarm | docs/WORKFLOW.md lines 34–40; repository git directory, logs/refs/heads/feat/explorer-reviewer-agents | The notice says the inventory was "Checked on 2026-11-01 against the tree at `1eb84b6b`" and lists `.claude/agents/explorer.md` and `reviewer.md` as supplied, but the two definitions land in the child commit `8ae99e50` ("feat(explorer-reviewer-agents): … the orchestrator's two helper definitions"); the reflog line shows `1eb84b6b` is its parent ("docs(explorer-reviewer-agents): the maintainer's scope answer"). A maintainer who checks out the cited commit finds the files it lists as supplied missing, so the dated check does not describe the tree it names. | mimo-v2.6-flash | fixed — not a test — same fix as L1-5 (51ccf6fd) | no — not a test | agree |
| L1-12 | MINOR | MAINT | round-1 swarm | plans/changes/explorer-reviewer-agents/research.md lines 26–31 | The note still instructs "The frontmatter says `provenance: human-written` — that holds for this skeleton. Whoever fills it with a language model sets `ai-drafted-reviewed` …", while the same file's frontmatter in this diff already says `provenance: ai-drafted-reviewed` with `produced_by:` and `review:`. The stale instruction contradicts the artefact it sits in and tells the next editor to redo a step that is done. | mimo-v2.6-flash | fixed — not a test — same fix as L1-4 (51ccf6fd) | no — not a test | agree |
| L1-13 | MINOR | MAINT | round-1 swarm | plans/changes/explorer-reviewer-agents/plan.md "Time used"; findings.md attempt blocks | The ledger records only rejected attempts — 2026-11-01 08:50–10:10 UTC, three rows, all "rejected" — yet the delivered diff contains attempt 1's exact file set (docs/WORKFLOW.md +11 −10, scripts/kit/probe.py +9 −1, tests/test_explorer_reviewer_agents.py +363, tests/test_workflow_entry.py +11 −3, per findings.md's attempt-1 block) plus the orchestrator's definitions, with no accepted attempt and no note that a human adopted a rejected attempt's output. The plan's own step 2 puts the definitions "after the accepted attempt", so a maintainer reading the ledger cannot reconstruct how the shipped code became acceptable. | mimo-v2.6-flash | fixed — not a test — same fix as L1-7 (51ccf6fd) | no — not a test | agree |
| L1-14 | BLOCKER | SPEC | glm-5.3-flash | plans/changes/explorer-reviewer-agents/spec.md §Acceptance criteria 6 and §Definition of Done; plans/changes/explorer-reviewer-agents/findings.md | Criterion 6 — a fresh-session observation that each helper actually runs on its pinned model — is promised and the DoD says a missing observation is not a pass, yet findings.md records only stage-2 call lines and failed diagnostics; no `/status` observation, command or commit for either helper exists anywhere in the change, so the change's own DoD is unmet. | glm-5.3-flash | fixed — not a test — findings.md records the fresh-session observation: explorer claude-haiku-5-5, reviewer claude-opus-5-5; the effort is named as not observed (51ccf6fd) | no — not a test | agree |
| L1-15 | MAJOR | SPEC | glm-5.3-flash | plans/changes/explorer-reviewer-agents/spec.md §Open decisions vs plans/changes/explorer-reviewer-agents/plan.md §Scope answer — 2026-11-01 | The spec still states "The following scope conflict remains open; no maintainer answer is inferred" while the plan records the maintainer answered "Ja" on 2026-11-01 and step 3 ran on that answer, so two live artefacts contradict each other on whether the scope conflict is resolved; a maintainer cannot tell which is current. | glm-5.3-flash | fixed — not a test — same fix as L1-9 (51ccf6fd) | no — not a test | agree |
| L1-16 | MAJOR | SPEC | glm-5.3-flash | plans/changes/explorer-reviewer-agents/plan.md "Appetite" and "Time used"; spec.md §Open decisions [DETAIL] | The declared appetite is "1 hour of phase 4 in total, repairs included; stop at the limit" but the Time used section records 2354 + 2387 + 21 s ≈ 79 minutes across the three implement attempts — the change overshot its own stop condition by about 30% without recording an appetite-exceeded return to the orchestrator. | glm-5.3-flash | fixed — not a test — same fix as L1-7 (51ccf6fd) | no — not a test | agree |
| L1-17 | MINOR | MAINT | glm-5.3-flash | plans/changes/explorer-reviewer-agents/decisions.md "Details for the draft" | The decisions file asserts the `model:`-field effect was "checked once by hand and recorded in findings.md", but findings.md contains no such record (only stage-2 call lines and diagnostics), so the decision cites evidence it claims exists and does not. | glm-5.3-flash | fixed — not a test — findings.md records the fresh-session observation: explorer claude-haiku-5-5, reviewer claude-opus-5-5; the effort is named as not observed (51ccf6fd) | no — not a test | disagree — The sentence prescribes a manual check; it does not claim that the check already happened. |
| L1-18 | MINOR | MAINT | glm-5.3-flash | plans/changes/explorer-reviewer-agents/plan.md "Execution boundary" vs decisions.md; plan.md §Scope answer | The plan's own boundary says to record the maintainer's actual answer in `decisions.md` before implementation, but the scope answer sits only in plan.md's "Scope answer" section while decisions.md holds just Q-1, leaving the decision that justified expanding scope (WORKFLOW, test_workflow_entry, probe.py) outside the decisions record. | glm-5.3-flash | fixed — not a test — same fix as L1-2 (51ccf6fd) | no — not a test | agree |
| L1-19 | MINOR | MAINT | glm-5.3-flash | tests/test_explorer_reviewer_agents.py (`CUE`, `_role_problems`) | The authorization counter-check treats any appearance of `caller`, `orchestrator`, `maintainer`, `only` and similar tokens in a sentence as a cue, so wordings that conditionally authorize a prohibited action — e.g. "When the caller asks, you commit the fix." or "You may commit only with approval" — satisfy the check while granting what criterion 4 must prohibit; the refutation promise is weaker than the test suggests. | glm-5.3-flash | fixed — not a test — Fremde Zuständigkeit erfordert ausdrückliche Zuweisung; bedingte Erlaubnisse werden abgelehnt. Ruff und alle 69 geprüften Fälle grün. | no — not a test | agree |
| L1-20 | MINOR | MAINT | glm-5.3-flash | tests/test_kit.py `test_the_kit_does_not_describe_the_phases` | The new masking `re.sub(r"\b(?:explorer\|reviewer)\.md\b", "", text)` strips the helper file names from every kit file's text, not only from the pytest case IDs that motivated the change, so phase-name substrings inside prose about "reviewer.md" or "explorer.md" now count as absent in the phase-description detector for all files. | glm-5.3-flash | fixed — not a test — Helfernamen werden nur in Endpunkt-Testkennungen ausgeblendet; Gegenproben erhalten ihre Erkennung in Kit-Prosa. | no — not a test | agree |
| L2-1 | MAJOR | MAINT | Phase 6 review | `.claude/agents/reviewer.md` (effort) · `tests/test_explorer_reviewer_agents.py` (`_assert_effort`) · `plans/changes/explorer-reviewer-agents/findings.md` | The reviewer's `effort: high` is a required configuration (spec criterion 2) whose runtime effect is never observed: the fresh-session check records "Not observed: the reviewer's effort `high`" and only the static frontmatter parse guards it. If the harness ignores `effort`, review silently runs at default effort with no failing test — a contract facing outward with no regression guard. | hy3 | rejected — an accepted limit: the effort is not observable in a fresh session (findings.md, the fresh-session observation: no effort field in the JSON result, /status is interactive); the static parse is the guard this change can give; named in the PR |  | disagree — Criterion 2 requires the effort configuration; criterion 6 requires observed model selection, not runtime effort measurement. |
| L2-2 | MINOR | MAINT | Phase 4 delivery | `scripts/kit/probe.py` (DECKEL 42→44) · `tests/test_kit.py` (new phase-name regex) | The kit bookkeeping is hand-tuned per agent: raising the cap and carving `explorer.md`/`reviewer.md` out of the phase-name guard. Any future agent whose filename embeds a phase word (explore/review/verify) must again be carved out of the regex and the cap raised; there is no structural fix, so the next agent quietly re-breaks the kit test until a maintainer repeats the edit. | hy3 | rejected — an accepted limit: the cap and the phase-name carve-out are the kit's existing bookkeeping for every new file; a structural rule for agent names is its own change; named in the PR |  | disagree — This proposes a broader mechanism for hypothetical future agents without identifying a current failure. |
| L2-3 | MINOR | MAINT | Test design | `tests/test_explorer_reviewer_agents.py` (`_role_problems`, `CONCEPTS`) | The read-only role contract is enforced by exact English-token matching (e.g. `unknown`, `evidence`, `spec`, `findings`, and the action words). A maintainer who rephrases the agent prose with synonyms for the same meaning — not weakening it — can fail `test_helpers_state_read_only_reporting_roles`, so the guard conflates vocabulary with contract and is brittle under legitimate edits. | hy3 | rejected — not a finding: the read-only role words are the contract the harness reads; a rewording that fails the test fails visibly, never silently, and matching synonyms would weaken the guard |  | disagree — No failing supported case is demonstrated; accepting arbitrary synonymous wording is not a specified requirement. |
| L2-4 | MINOR | MAINT | Phase 4 delivery | `.claude/agents/explorer.md` · `.claude/agents/reviewer.md` · `tests/test_explorer_reviewer_agents.py` (`_assert_tools`) | The read-only guarantee rests solely on parsing the `tools: Read, Grep, Glob` allowlist; the definitions carry no `permissions.deny`, and nothing checks at runtime that the harness honors the allowlist. Consistent with the other seven agents, but a single harness gap would silently break read-only for every helper with no failing test. | hy3 | rejected — an accepted limit: the tool allowlist is the harness's enforcement for all nine agent definitions; a runtime check of the harness is outside this change; named in the PR |  | disagree — The spec explicitly limits this check to the configured allowlist and excludes proof of runtime sandbox enforcement. |

Rounds run: 2

Record digest: sha256:f0973be3a57f6d249f764f72a31bd5f1b0cf0eebd4f5f15f101af3ccf98e5bdc

Record identity: sha256:684811558cef3ef7f66e8b53bf0b60870dce10e81652f06cf18c3682becd57ab

Loop state: {"availability": {"checked_at": "2026-11-01T12:54:00+00:00", "failed": {"cat-jam-free": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model is unavailable.\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model access is disabled\"}", "longcat-2.5-preview-free": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model is unavailable.\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "skipped": {"gemini-4-argon-contributor": "not admitted; data terms have not been read", "grok-4.6": "not admitted; data terms have not been read", "minimax-m2.7": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "space-bunny": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)", "grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free)", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": ["the data terms of mimo-v2.6-pro expire on 2026-11-06 (5 days left)"]}, "consumed": ["rung:glm-5.3-flash", "flash", "rung:hy3"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "big-pickle", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-flash", "provider": "opencode"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "exo-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "ling-3.0-flash-fin-free", "provider": "opencode"}, {"model": "ling-3.1-flash-free", "provider": "opencode"}, {"model": "longcat-2.5-preview-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-spark-1.3-contributor-free", "provider": "opencode"}, {"model": "nemotron-3-ultra-free", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "space-bunny-free", "provider": "opencode"}, {"model": "step-5-preview-free", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-flash", "provider": "opencode-go"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon-contributor", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.6", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-preview-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m2.7", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "space-bunny", "provider": "opencode-go"}, {"model": "step-5-preview-free", "provider": "opencode-go"}], "checked_at": "2026-11-01T12:45:32+00:00", "dropped": {}, "models_store": {"opencode-go": {"checkedAt": 1793537128185, "etag": "W/\"65e1c3b71054c3b1741fe4cb46560dbf\"", "lastModified": 1792068066000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "cat-jam-free", "input": ["text"], "maxTokens": 131072, "name": "Cat Jam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"forceAdaptiveThinking": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro (New)", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/v1", "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 0, "input": 4, "output": 20}, "id": "gemini-4-argon-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.6", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.6", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 0, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "LongCat 2.5 Preview Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 204800, "cost": {"cacheRead": 0.06, "cacheWrite": 0.375, "input": 0.3, "output": 1.2}, "id": "minimax-m2.7", "input": ["text"], "maxTokens": 131072, "name": "MiniMax-M2.7", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "space-bunny", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 524288, "name": "Space Bunny", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "step-5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "overlay": ["cat-jam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon-contributor", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.6", "grok-4.7", "hy3", "hy4-preview", "kimi-k2.7-code", "kimi-k3", "longcat-2.0", "longcat-2.5-preview-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m2.7", "minimax-m3", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "space-bunny", "step-5-preview-free"], "pi_version": "1.2.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "rungs": ["glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"]}}

Kept from the loop record:

> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured); grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: gemini-4-argon-contributor, grok-4.6, minimax-m2.7, muse-spark-1.2-contributor, muse-spark-1.3-contributor, space-bunny.
> Notice: the data terms of mimo-v2.6-pro expire on 2026-11-06 (5 days left).
> longcat-2.0 was asked again with the format reminder: the first answer was malformed
> longcat-2.0 failed: malformed finding output: expected six-cell findings or exactly 'No finding.'; replaced by glm-5.3-flash
> From glm-5.3-flash:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> All promised evidence checks verified against the worktree: the byte-equal RB-A1 clause matches `docs/governance/regelwerk.md` §6, the pinned models are declared in `model-endpoints.yaml`, the role texts pass the intended assertions, the probe cap arithmetic (7 existing + 2 new = 44) holds, and the notice test's assertions hold against the edited notice. What remains are gaps between what the artefacts promise and what they contain:
> 
> From longcat-2.0:
> longcat-2.0's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> After thoroughly reviewing all the files in the change — the two agent definitions, the test module, the workflow notice update, the kit probe and kit test changes, the model-endpoints declarations, the spec, and the decisions — I find the implementation consistent with its spec and decisions. The agent files pin the maintainer-chosen models (`claude-haiku-5-5` and `claude-opus-5-5` at `effort: high`), carry exactly the three read-only tools, state the required prohibitions with proper cues, include the RB-A1 evidence contract byte-identical to `docs/governance/regelwerk.md` §6, and both models resolve against `model-endpoints.yaml`. The companion maintenance (workflow notice, test_workflow_entry, probe.py DECKEL 42→44, test_kit.py regex sub) is the direct, documented consequence of the maintainer's scope answer. The counter-checks are sound — correct fixtures pass, and mutations are caught.
> 
> No finding.
> 
> From longcat-2.0:
> longcat-2.0's second answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> After a thorough review of all files in the diff — the two agent definitions, the test module, the WORKFLOW.md notice update, the kit probe exceptions, the workflow entry test, the kit test regex, and the plan documents — against the normative evidence contract in `docs/governance/regelwerk.md` §6, the model declarations in `model-endpoints.yaml`, and the existing test infrastructure, I find:
> 
> - The evidence-contract paragraph in both `explorer.md` and `reviewer.md` is byte-identical to the normative text extracted from `regelwerk.md` §6 (the `test_rb_a1_clause_is_present_verbatim` extraction strips `> **Evidence contract.** ` from the blockquote and `## Evidence contract (RB-A1)\n\n` from the heading; the remaining paragraph text matches exactly).
> - Both pinned models (`claude-haiku-5-5`, `claude-opus-5-5`) are declared under `anthropic-api` and `claude-code-plan` in `model-endpoints.yaml`.
> - The tool allowlist is exactly `Read, Grep, Glob` for both, matching the spec.
> - The role texts state all required prohibitions with valid cue words and all required reporting concepts.
> - The reviewer's `effort: high` is present.
> - The WORKFLOW.md notice correctly moves `.claude/agents/explorer.md` and `reviewer.md` from the absent list to the supplied list, and the corresponding test assertions match.
> - The kit probe adds exactly two new `braucht-die-vollstaendige-suite` exceptions and raises `DECKEL` from 42 to 44.
> - The `test_kit.py` regex correctly strips the two file names from pytest case IDs before the phase-name check.
> 
> No finding.
> 
> Notice: the data terms of mimo-v2.6-pro expire on 2026-11-06 (5 days left).
> From hy3:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Based on my review of the change against the diff, the agent definitions, the test module, the kit bookkeeping, and the supporting plan/spec/findings artifacts, here are my findings.

<!-- End of released loop record -->

Stage-2 call, 2026-11-01: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 808 files, 2994 commits, 12 rules.

Stage-2 call, 2026-11-01: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 808 files, 2997 commits, 12 rules.

## Phase 6 — Codex, 2026-11-01

Codex reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding.

Phase 6 verdict: codex 01a19889-06d8-7332-aa32-493f330dc5e2, 2026-11-01
Reviewer session: codex 01a19889-06d8-7332-aa32-493f330dc5e2 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
