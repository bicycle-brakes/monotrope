---
title: "Findings — agent-policy-list"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-r7zc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — agent-policy-list

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1235 files, 5898 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/agent-policy-list/plan.md` +48 -0
> - `plans/changes/agent-policy-list/spec.md` +66 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - `plan.md` does not open with the plan card (For you:, Done when:, Appetite:, Not now:, Pre-mortem:)
> ```

Stage-2 call, 2026-11-25: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1238 files, 5900 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1238 files, 5903 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:402f4bf1881890af27b466d1e88e4f116a0b35a620badeafe557a06e5995f2d0

Spec review commit: 19e5b24a10315bab5bf16ddf432adc69714b316f

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, AC1 ("one authoritative source"); Definition of Done ("no ADR changes") | Reading A: each rule has one source. `scripts/merge_guard.py` stays the source of the merge asks, `scripts/omnigent_policy.py` keeps `DENIED_TOOLS`/`ASKED_TOOLS`, and only the rules no list holds today (`Bash(codex *)`) get a home. Reading B: one new policy list holds every deny/ask rule (the merge family, `gh alias set`, `git push *main*`, `codex`, the Omnigent tools, the protected path), and both modules derive from it. Under B, a `MERGE_ASK_RULES` or `DENIED_TOOLS` still typed by hand is the "independently maintained duplicate" that turns AC1 red. Under A it is the intended source. Under B, `docs/adr/0008-merge-confirms-a-decision.md` lines 129–130 ("come from one list (`scripts/merge_guard.py`)") become false, but the DoD forbids ADR changes. | Opus | in spec — maintainer 2026-11-25 (decisions.md Q-1): one harness-neutral check command (scripts/agent_policy.py check) reads every rule source; merge_guard.py and omnigent_policy.py stay the sources of their rules, new rules (codex) get one home; thin per-harness hooks for Claude Code, Codex and Antigravity call it; ADR 0008 stays true | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, AC3 ("covered by the existing Claude Code command rules"); Non-goals, first bullet | Reading A: "covered" is the whole-text glob of `merge_guard.covers`, where the pattern must match the entire command line. Reading B: "covered" is what Claude Code's own matcher decides, and that matcher treats shell operators such as `&&` specially and checks the parts of a compound command. Two inputs separate them: `cd /repo && gh pr merge 54` and `git add . && git push origin main`. Under A the hook leaves them to the host, and the non-goal ("alternate spellings") excuses that. Under B the hook must ask, and AC3 is red if it does not. Agents often send compound lines through `run_command`, so this choice decides what the brake stops. | Opus | in spec — maintainer 2026-11-25 (decisions.md Q-2): the check splits a command line at shell operators (&&, ||, ;, |) and checks every part; one covered part decides the whole line | — |
| S-3 | [AMBIGUITY] | SPEC | base | spec.md, AC3 and AC4 (When clause against Refuted-by); Non-goals, third bullet | The When clauses test what the hook returns. The refutations test what a command "receives" or whether it "can proceed". Reading A: the hook's output, checked on its own with fed input. Reading B: the effective decision on the installed host, after Antigravity's user-level settings and its auto-run mode have applied. Per the research those settings are a different, hand-maintained list, and this change may not touch them. Example: the user list auto-allows or denies `codex *`. Under A, AC3 is green. Under B it is red ("weaker or different decision"), and no change in scope can fix it. The DoD's host verification inherits the same split. | Opus | in spec — maintainer 2026-11-25 (decisions.md Q-3): the tests prove the check command's and the hooks' output for given input; the host's user-level settings are a named Boundary; a one-time host check on the maintainer's machine is documented in the pull request | — |
| S-4 | [AMBIGUITY] | SPEC | base | spec.md, Non-goals, third bullet ("Antigravity tools it does not expose"); AC3 (`run_command` only) | Reading A: only `run_command` is in scope, as AC3 and the research's matcher state. Reading B: every tool Antigravity does expose gets the matching rule, which is what the non-goal's qualifier implies. That would cover its file-edit tools under `Edit(//**/.omnigent/config.yaml)`, a GitHub MCP server's merge tool under `mcp__*__merge_pull_request`, and any other shell entry, such as input sent to a running terminal. Under B, a merge through an MCP merge tool configured in Antigravity refutes the change. Under A it is outside it. No criterion decides which. | Opus | in spec — maintainer 2026-11-25 (decisions.md Q-4): the hooks check shell commands and every MCP tool whose name ends in merge_pull_request; file-writing tools stay a named Boundary | — |
| S-5 | MAJOR | SPEC | base | spec.md, Open decisions; AC3, AC4 | The spec says to take the hook schema and the unattended signal from the host ("do not invent either"). It does not say what happens when the host lacks them. (a) The hook protocol may have no "ask" result: does the hook deny, pass, or does the change stop? (b) The host may have no unattended signal: what marks the 72-hour run? Options are a repository launcher like `tools/claude-code/night.py`, an environment variable, or always deny. (c) The signal may be absent or unreadable: does the hook treat the run as attended, so it asks and an unattended run hangs (AC4 red), or as unattended, so it denies? (d) Which host version counts as "the supported host" is not stated; the research measured agy 1.5.14. Until (b) and (c) are decided, AC4 has no red case anyone can write. | Opus | in spec — [DETAIL] decided by the orchestrator: where a host's hook protocol has no ask result, the hook denies; the unattended signal is the environment variable HARNESS_UNATTENDED=1 set by the run's launcher (night.py for Claude Code, the Antigravity launch settings); without it the run counts as attended | — |
| S-6 | MAJOR | SPEC | base | spec.md, AC3–AC5 | The spec does not say what the hook does when it fails: the policy cannot be read, the host's input is malformed or has an unknown shape, the hook script raises, or it times out. If it fails open, covered commands pass and AC3/AC4 are silently lost for the 72-hour run. If it fails closed, unrelated commands are blocked, which refutes AC5. `night.py` refuses when a source cannot be parsed, but the spec does not carry that rule over, so the implementer will choose. | Opus | in spec — [DETAIL] decided by the orchestrator: when the policy cannot be read, the hook fails closed and denies every command with a message naming the fault; malformed host input or an exception denies with the fault named; a timeout is the host's (Antigravity hook default) and counts as deny | — |
| S-7 | MINOR | SPEC | base | spec.md, AC7, Refuted-by | The claim is that layer two and the overlay "retain their present protection". The refutation names only a lost Omnigent denial or a lost ask-to-deny conversion. Suppose regeneration drops the layer-two ASK policy (`coding_harness__omnigent_asked_tools`, `sys_advise_models`) from `tools/omnigent/policy.yaml`, or turns it into a pass. That loses present protection, and no stated refutation case catches it. | Opus | in spec — [DETAIL] decided by the orchestrator: the refutation also names a lost layer-two ask policy (coding_harness__omnigent_asked_tools, sys_advise_models); regeneration must keep it as ask | — |
