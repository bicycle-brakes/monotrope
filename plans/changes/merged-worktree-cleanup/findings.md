---
title: "Findings — merged-worktree-cleanup"
category: findings
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.4
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — merged-worktree-cleanup

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1168 files, 5313 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/merged-worktree-cleanup/plan.md` +68 -0
> - `plans/changes/merged-worktree-cleanup/spec.md` +87 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - `plan.md` does not open with the plan card (For you:, Done when:, Appetite:, Not now:, Pre-mortem:)
> ```

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5316 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5320 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | Terms "Clean and pushed"; AC5; AC6 | [AMBIGUITY] What counts as a "configured upstream". The house creation command in `docs/WORKFLOW.md` §3 rule 2 (`git worktree add -b <branch> .claude/worktrees/<name> origin/main`) sets the branch's upstream to `origin/main` under Git's default `branch.autoSetupMerge`. It stays that way unless the branch is pushed with `-u`. Reading A (literal): `origin/main` is a configured upstream, so AC5 applies. Once the PR lands as a merge commit, `origin/main` is ahead of the tip, so the worktree is never eligible. Reading B: "upstream" means the remote branch the work was pushed to. An `origin/main` upstream then falls to AC6, and the worktree is eligible once merged. For worktrees made the house way, A keeps nearly every merged one and B removes them. | Opus | open | — |
| S-2 | MAJOR | SPEC | base | AC5; AC9; AC12; Open decisions [DETAIL] | [AMBIGUITY] A merged PR's head branch is deleted on the remote, so the branch still has a configured upstream but its remote-tracking ref is gone (`[gone]`). Reading A: this is the "configured but unreadable upstream" of Open decisions, so the worktree is kept, possibly every merged worktree whose head branch was auto-deleted. Reading B: a gone upstream is the normal state after a merge, so `origin/main` ancestry decides. The outcome also depends on what the "fresh fetch" fetches, which the spec never says. A fetch of `main` only leaves a stale `origin/<branch>` that AC5 would compare against, and AC9's "stale evidence" names only merge evidence. A pruning fetch (`--prune` or `fetch.prune`) makes the ref gone, and it deletes local remote-tracking refs, which AC12 ("no remote branch is deleted") may or may not forbid. | Opus | open | — |
| S-3 | MAJOR | SPEC | base | Protected areas; AC7; Terms "Merged" | Gap: worktrees in use by another live session. Under "Merged", a branch with no commits of its own (tip on `origin/main`) counts as merged. Examples: a freshly opened change worktree before its first commit, the "up-to-date cleanup worktree" of `prompts/07-commit.md`, a read-only review or explore session's worktree. If such a worktree is clean and has no upstream, or an upstream equal to its tip, it is a candidate. `ARGS=--write` then removes it while a sibling session runs in it. Protected areas gives "in use" as the reason to protect but covers only the main checkout and the invoking worktree. The spec is also silent on whether `--write` is limited to the sole writing session, the way `beads-start.sh` limits tracker writes using the `session-scan.sh` `sibling` relation that research.md names. An implementer has to decide both. | Opus | open | — |
| S-4 | MINOR | SPEC | base | AC1; AC5; AC6 | Gap: "eligible" is never defined by a sufficient condition. AC5 and AC6 give only necessary conditions ("eligible only if"). No criterion says that a worktree is eligible when it is merged, clean and pushed, neither the main checkout nor the invoking worktree, and all its checks completed. So AC1's refutation ("an eligible worktree is omitted") has no input that is eligible by definition. Any extra keep rule an implementer adds (locked, directory missing, outside `.claude/worktrees/`, live session) passes every criterion unnoticed. | Opus | open | — |
| S-5 | MINOR | SPEC | base | AC1; AC8; AC9; AC10 | Gap: registered worktrees that are locked (`git worktree lock`) or prunable (directory gone; research.md says the 117 count includes stale registrations). `git worktree remove` without force refuses a locked worktree. With the spec silent, a locked worktree is a preview candidate, and every `--write` run then fails under AC10. A prunable entry cannot be status-checked, so under AC9 it is kept with a failure reported on every run. Undecided: are these kept with a reason, pruned (`git worktree prune`), or reported as failures, and what does each do to the exit status? | Opus | open | — |
| S-6 | MINOR | SPEC | base | AC8; AC10 | Gap: behaviour after a partial failure. (a) Reading A: stop at the first refused removal or deletion. Reading B: continue through the remaining candidates, then exit nonzero. (b) For a branch with no upstream, `git branch -d` checks against the invoking checkout's `HEAD`, not `origin/main`. Invoked from a worktree whose `HEAD` lacks the merge, the deletion is refused after the worktree is already removed. Later runs list only registered worktrees, so that orphaned local branch is never seen again. The spec says neither whether orphaned branches are in scope nor how this sequence is prevented. | Opus | open | — |
| S-7 | MINOR | SPEC | base | AC9 | Gap: the exit status when the fresh fetch or a safety check fails, in preview or `--write`. AC10 sets a nonzero exit only for removal or branch-deletion failures. Undecided: does an unreachable remote, which keeps every worktree, exit 0 or nonzero? The handover routine of AC11 depends on the answer. | Opus | open | — |
| S-8 | MINOR | SPEC | base | AC3; AC4; AC7; AC9; AC10 | These criteria cannot go red on their reporting clauses. AC3, AC4 and AC7 require "kept with a reason", but their refutations cover only "a candidate or removed". An implementation that leaves such a worktree out of the output, or lists it as kept without a reason, passes. AC9's "the failure is reported" and AC10's "any partial result are reported" have no refuting case: a silent keep, or a nonzero exit that names no partial result, passes. | Opus | open | — |
| S-9 | MINOR | SPEC | base | AC11; Definition of Done; decisions.md last [DETAIL] | [AMBIGUITY] "the handover routine names the preview and explicit-write cleanup commands". Reading A: `tools/claude-code/skills/handover/SKILL.md` tells the handover session to run `make prune-worktrees` and then `ARGS=--write` as a step, so worktrees are removed at every handover, close to the non-goal "automatic scheduled cleanup". Reading B: it only points to the commands for a human or a later session to run. The two give different behaviour. Separately, decisions.md calls the target a runner-held "handover prompt", but no handover prompt exists under `prompts/`, and the Definition of Done names SKILL.md. | Opus | open | — |
| S-10 | MINOR | SPEC | base | Protected areas; AC7 | Gap: the local integration branch. A worktree other than the main checkout that has local `main` checked out, is clean and has its tip on `origin/main` is a candidate. `--write` then runs `git branch -d main`, which succeeds against its `origin/main` upstream. Only the main checkout is protected, not the `main` branch. Undecided: is a worktree on `main` kept with a reason? | Opus | open | — |
| S-11 | MINOR | SPEC | base | Definition of Done | Gap: research.md names `scripts/kit/manifest.yaml` as a decision the change must make ("a new script must be added there or deliberately left out"). The spec does not settle whether the new entry point ships to new repositories through the kit, so the implementer would decide it silently. | Opus | open | — |
