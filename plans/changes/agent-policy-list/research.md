---
title: "Research — agent-policy-list"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-r7zc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# agent policy list — Research

## Topic (bead coding-harness-r7zc)

Class: bounded. Measured 2026-11-25: the repository's layer-1 deny/ask rules (push to main, merges through gh pr merge and the GitHub API, codex, gh alias set, Omnigent tools) live only in .claude/settings.json; Antigravity (agy 1.5.14) does not read them, and its user settings carry a hand-maintained, different list. Omnigent is not involved (agy has no Omnigent MCP server). Build one source list in the repository (pattern of scripts/omnigent_policy.py) that (1) generates the permissions block of .claude/settings.json and (2) backs an Antigravity PreToolUse hook (.agents/hooks.json, matcher run_command) that answers deny or ask for the same commands, with ask turned into deny in an unattended run (as tools/claude-code/night.py does); a drift gate holds the generated files to the list. The enqueue script of the companion bead is the only allowed merge path. Needed before the 72-hour Antigravity run.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29; bounded change · leak check clean over 1234 files, 5894 commits, 12 rules.

## Runner exploration — 2026-11-25

## Research: agent-policy-list (bounded, bead coding-harness-r7zc)

Cut-off: the worktree at `e68a00e6`, read 2026-11-25. Read-only; nothing edited, nothing run.

### What exists today

**Claude Code's permission rules are hand-kept in one file, `.claude/settings.json`.** It has 30 deny rules and 13 ask rules.
- Deny: 29 `mcp__omnigent__*` names plus `Edit(//**/.omnigent/config.yaml)`. There are no non-Omnigent deny rules.
- Ask: 12 non-Omnigent rules (the merge family, `Bash(gh alias set *)`, `Bash(git push *main*)`, `mcp__*__merge_pull_request`, `Bash(codex *)`) and one Omnigent rule, `mcp__omnigent__sys_advise_models`.
- A `SessionStart` hook also lives there (`tools/claude-code/hooks/beads-start.sh`).

**The merge ask rules are a list in code, checked but not generated.** `scripts/merge_guard.py` holds `MERGE_ASK_RULES`: 10 rules, each with a reason and a sample call. `covers(rule, call)` is a matcher that follows Claude Code's documented rule forms. `problems(settings)` reports missing ask rules and any deny or allow rule that covers a merge sample. The module docstring says nothing writes the merge rules; `tests/test_merge_guard.py` compares the settings file against the list. It also has the night-overlay checks, which take the day asks through `tools/claude-code/night.py`.

**The Omnigent rules are generated from one list.** `scripts/omnigent_policy.py` has `DENIED_TOOLS` (29), `ALLOWED_TOOLS` (16), `ASKED_TOOLS` (1) and `PROTECTED_PATHS`. Its `write()` rewrites only the rules it owns (`mcp__omnigent__*` and the protected path) and keeps every other rule, so `Bash(codex *)` and the merge rules survive a write. Its `check()` is the drift gate: it reports when `.claude/settings.json` or `tools/omnigent/policy.yaml` differs from what the list renders. `tests/test_merge_guard.py` also re-renders the settings in a temporary copy.

**The unattended launcher turns asks into denies.** `tools/claude-code/night.py`, `build_overlay(fragment, layers)`, reads the user settings and the project's `.claude/settings.json` and `settings.local.json`. It writes a private overlay with every deny, and every ask as a deny. `tools/claude-code/night-settings.json` sets `defaultMode: dontAsk`. It refuses to run if a present settings file cannot be parsed.

**Codex has a hook file of its own.** `.codex/hooks.json` wires `tools/bd codex-hook` events (`SessionStart`, `PreCompact`, `PostCompact`, `UserPromptSubmit`). It holds no permission rules. `docs/WORKFLOW.md` (near the Codex hook passage, around line 1465) says the runner starts Codex with hooks off, and the `Bash(codex *)` ask guards a `codex` typed by hand.

**Antigravity is not in the repository's configuration.** Searching for "antigravity" and "agy" finds it only in handovers (`docs/journal/handover/2026-11-21-day-run.md`, `2026-11-21-evening-run-2026-11-21-a.md`, `2026-11-25-night-run-seven-prs.md` mentions an "agy session") and in the change files `adr-0021-consumed-ladder` (its `produced_by`). `.agents/` holds only `.agents/skills/beads/SKILL.md` and `agents/openai.yaml`. Glob for `.agents/hooks.json` and `.agents/**/*.json` returns nothing. **Not found:** an Antigravity hook file or any `run_command` matcher in this tree.

**Merge enforcement is described in `docs/WORKFLOW.md`** (around lines 494 and 818–853): the ask rules are "a brake, not a lock", and another spelling passes. `docs/adr/0008-merge-confirms-a-decision.md` (around lines 129–130) says the rules come from one list, `scripts/merge_guard.py`.

**The Makefile and CI do not name these files.** `Makefile` mentions `verify:` only (grep for omnigent, merge_guard, settings, policy). `.github/workflows/ci.yml` names none of them. Whether `make verify` runs `tests/test_merge_guard.py` and the Omnigent check is therefore not established by these files; the tests may be collected by pytest, which I did not confirm.

**Earlier research on the same boundary.** `docs/research/2026-10-05-hermes-agent-runner.md` (around line 281) records that `.claude/settings.json` binds Claude Code only and that Hermes does not read it. `docs/research/2026-10-31-architecture-reconciliation.md` (rows G5, G21, T38) records the rules as brakes, not locks.

### Where it lives

- Source lists: `scripts/merge_guard.py` (`MERGE_ASK_RULES`, `EXTRA_SAMPLES`, `covers`, `problems`), `scripts/omnigent_policy.py` (`DENIED_TOOLS`, `ALLOWED_TOOLS`, `ASKED_TOOLS`, `PROTECTED_PATHS`, `write`, `check`).
- Rendered and hand-kept: `.claude/settings.json` (both lists), `tools/omnigent/policy.yaml` (generated, Omnigent only).
- Night path: `tools/claude-code/night.py` (`build_overlay`, `load_settings`), `tools/claude-code/night-settings.json`.
- Tests: `tests/test_merge_guard.py`, `tests/test_omnigent_deny_layers.py`, `tests/test_night_profile.py` (the last two exist; I did not open them).
- Git-side brake for Codex: `.codex/hooks.json`, `docs/WORKFLOW.md`.

### What is unclear

- **Antigravity's side is not in this repository.** Its settings file, its hook schema (`.agents/hooks.json`, the `run_command` matcher) and its measured version (agy 1.5.14) are not here. The topic's measurement that Antigravity does not read `.claude/settings.json`, and that its user settings hold a different list, cannot be checked from this tree.
- **The companion enqueue script is not found.** No `scripts/*enqueue*` file exists. The grep for "enqueue" matched only `merge_guard.py` and `docs/WORKFLOW.md` (around line 498). The companion bead's text was not read; I have no tracker access in this phase.
- **Count drift.** `docs/research/2026-10-31-architecture-reconciliation.md` (row G5) and `tools/omnigent/README.md` both state "27 denied, 16 allowed, 1 asked". The current lists have 29 denied, 16 allowed, 1 asked. The 27 is either stale or counts something other than the list; I did not determine which.
- **Night runs for Antigravity.** Nothing in the tree shows whether `night.py` launches Antigravity or whether an Antigravity night run would bypass its overlay.
- **Ownership of the non-Omnigent asks.** Today `Bash(codex *)` is kept by `omnigent_policy.write()` and is in neither list's rendering; the merge rules have no writer. Which file owns which rule is not stated in one place.
- **Tests not opened:** `tests/test_omnigent_deny_layers.py`, `tests/test_night_profile.py`, `tests/test_entry_points.py`, and the Makefile `verify` target body. Whether they gate the drift check is not established.
- **Not read:** `docs/adr/0006*` (named in AGENTS.md as the Omnigent-layering decision) and `docs/WORKFLOW.md` §2 and §3 in full.

### Which files a change would have to touch

These are the files that hold the content the topic names, as the repository stands today. This is not a design.
- `.claude/settings.json` — the permissions block (the merge rules, `Bash(codex *)`, the Omnigent rules).
- `scripts/merge_guard.py` — `MERGE_ASK_RULES` and `EXTRA_SAMPLES`, which name the merge rules.
- `scripts/omnigent_policy.py` — the one list pattern the topic cites; its `write()` and `check()` already keep foreign rules.
- `tests/test_merge_guard.py` — compares the settings against the merge list.
- `tools/claude-code/night.py` and `tools/claude-code/night-settings.json` — the ask-to-deny overlay for an unattended run.
- `tests/test_night_profile.py` — the held night-profile checks.
- A new Antigravity hook file (`.agents/hooks.json`, not in the tree) — the one artifact the topic adds that has no precedent here.
- Possibly `.codex/hooks.json` and `docs/WORKFLOW.md` — the Codex brake passage and the policy doctrine, if the change alters what the brake covers.

**Neighbours found by search (not opened in full; the runner decides whether they go into the header):**
- `plans/changes/archive/2026-09-29-omnigent-deny-layers/` (the Omnigent layering, the origin of `omnigent_policy.py`)
- `plans/changes/archive/2026-11-06-merge-queue/spec.md` (matches the enqueue search)
- `plans/changes/archive/2026-11-16-night-stall-guard/` (matches the `merge_guard` and night search)
- `docs/adr/0008-merge-confirms-a-decision.md`

The header `neighbours: []` in `plans/changes/agent-policy-list/research.md` is unchanged here.
