---
title: "Findings — frontmatter-batch-log"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — frontmatter-batch-log

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5772 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/frontmatter-batch-log/plan.md` +50 -0
> - `plans/changes/frontmatter-batch-log/spec.md` +68 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - `plan.md` does not open with the plan card (For you:, Done when:, Appetite:, Not now:, Pre-mortem:)
> ```

Stage-2 call, 2026-11-25: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1206 files, 5772 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5773 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:0b6dd9d8920717a538d04fe23ec64d9a6bd2ef69ef6047fe1d26f3590f2a1254

Spec review commit: 64478ce86aba8d9957587f8cc0ab1c2d4d7a7b66

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | Acceptance criterion 1 | [AMBIGUITY] "Git log invocation" can be read two ways. Reading A: only processes of the `git log` command count. Under it, one `git log` plus a `git rev-list -1 --no-merges HEAD -- <path>` for each document meets the criterion and survives its refutation case. So does a per-path fallback for documents near a merge. Either way there is still one history process for each document, which is the cost the bead is meant to remove. Reading B: every Git process that walks commit history to date a document counts. Under it, a design that pairs one `git log` with a second history process fails, for example `git diff-tree --stdin` to get merge-parent diffs for rebuilding per-path simplification. The refutation case counts only "Git log processes", so it tests reading A alone. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-5 (2026-11-25) | — |
| S-2 | MAJOR | SPEC | base | Acceptance criterion 6; Non-goals, third bullet; Problem | [AMBIGUITY] The spec does not say what the timing record decides. Reading A: the record is only information. A batch as slow as or slower than the per-file loop still meets every criterion and ships. One example is a full-history `git log -m --name-only` walk followed by rebuilding per-path merge simplification in Python, which criterion 2 at merges may force. Reading B: the Problem section states runtime as the reason for the change, so a later runtime that is not below the earlier one stops the change. No criterion fails on the measured result: criterion 6 is refuted only by a missing runtime, different commits or an unreported failing run. Under reading B, the failure this change exists to prevent has no refutation case. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-6 (2026-11-25) | — |
| S-3 | MINOR | SPEC | base | Acceptance criterion 2, the oracle command | [AMBIGUITY] The oracle gives `<path>` to Git as a pathspec, not as a literal path. Take a held name with `*`, `?` or `[` in it, such as `docs/[draft].md`: as a glob it also matches `docs/d.md`. A name that starts with `:` is read as pathspec magic. For such names the oracle returns the newest commit that changed any matching path. Reading A: the batch must reproduce that match, so a batch that assigns commits by the exact names in its `--name-only` output fails criterion 2. Reading B: the reference is the newest non-merge commit that changed that exact path, as the script's docstring says ("the newest non-merge commit that changed it"). Then the oracle needs literal pathspecs, and the output for such names changes, which criterion 5 forbids. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-7 (2026-11-25) | — |
| S-4 | MINOR | SPEC | base | Acceptance criterion 4 (and criterion 5 for its exit status) | The spec does not say which `<file>` and `<reason>` the diagnostic names when the single invocation exits non-zero. Today each clean document has its own process. The message names the first document in sorted order whose own call failed and carries that call's stderr. A batch failure belongs to no document, so the implementer has to invent who it is blamed on. Consider a fault that only some per-path walks reach, such as an unreadable object deep in history. Today's `-1` walks stop at the first match and may never read it; the batch walk reads it. Such a fault changes the named path, the reason and the exit status: 3 instead of 0 or 1. The refutation "a different path or reason, or a different exit code" cannot be avoided for that input, and the spec does not say whether that input is in scope. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-8 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5774 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5777 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:e090657a7c820a3fc2a3db974b4c4dd05f15649bd95d204f7186d572c32be30b

Spec review commit: 556da4590fdf0afc5c995b38b71539c3347c587a

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-5 | MAJOR | SPEC | base | Acceptance criterion 1; decisions.md D-5; Non-goals, second bullet | [AMBIGUITY] "The date check" has no defined scope, and D-5 says "at most three for the whole run". Reading A: only the date lookup in `reference_dates` counts. That is the dirty-set `git diff` and `git ls-files --others` plus the batch, so three processes, and the preflight and the held-file enumerations are left as they are. Reading B: every Git process of one gate run counts, as D-5's "whole run" says. That is three preflight `rev-parse` calls, the `ls-files` in `held_files`, the two dirty-set calls, the batch and the second `held_files` enumeration in `run()`: eight. Under B the criterion can only be met by merging the preflight calls and removing the second enumeration, and the non-goals forbid touching that enumeration. A test that counts `_git` calls around `reference_dates()` stays green at 3. Around `findings()` it goes red at 4, and around `run()` at 8. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-9 (2026-11-25) | — |
| S-6 | MINOR | SPEC | base | Acceptance criterion 5 and its refutation; decisions.md D-8 | [AMBIGUITY] The spec does not define "protected stderr". In this repository "protect" names `protect_diagnostics` in `scripts/stage2.py`, and no gate script uses it. That function redacts matches of the leak denylist's secret rules and refuses on non-secret rules. Reading A: the batch's stderr goes through that redaction. The gate then depends on the runner or `leakcheck`, a secret-shaped string in stderr appears as a `[secret:…]` marker, and the spec does not say what exit status or message a refusal gives. Reading B: "protected" means kept, so Git's stderr is carried as `_git_z` carries it today, stripped but otherwise verbatim. Put a secret-shaped string into a failing batch's stderr: a test that expects the raw text passes under B and fails under A, and a test that expects the marker does the opposite. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-10 (2026-11-25) | — |
| S-7 | MINOR | SPEC | base | Acceptance criteria 7 and 8 | [AMBIGUITY] The gate's script is part of the commit, so the before version and the after version exist at different commits, and the spec does not say how both are timed "at the same commit". Reading A: one commit is checked out and both script versions run against that same tree, for example the base's script run with `--root`. The held set and the dirty state are then the same for both. Reading B: the before is measured at the base commit before implementation and the after at the implementation's commit, and "same commit" means the same underlying history. The held set then differs by this change's own documents, so the two runs do different work. A record made the B way is refuted by "different commits" under A and accepted under B. Criterion 8's halving verdict, which decides whether the change ships, rests on that record. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-11 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5778 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5779 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:1bf79158ce763b952c62911bada2a5c87379888927540b77cf01376b493586a1

Spec review commit: 6915e8551a30925cb14e6019616fe1d006f47fdd

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-8 | MINOR | SPEC | base | Acceptance criterion 2, "from the same root and Git configuration"; criteria 1 and 6 | [AMBIGUITY] The oracle is a `git log` call with one path, so its answer depends on the Git configuration it runs under, and one setting changes that answer. Git documents that with `log.follow=true`, `git log` acts as if `--follow` were given whenever a single path is passed. It then has `--follow`'s limitations, including that it "does not work well on non-linear history". The batch names many paths or none, so the setting does not reach it, except when exactly one clean document is left. `_git` in `scripts/check_frontmatter_current.py` passes the user's environment and global configuration through unchanged, so the per-file call honours `log.follow` today. Reading A: "the same Git configuration" means whatever the checkout and the user carry. For a developer with `log.follow=true`, the batch must then give the `--follow` answer. It cannot know to do that without either a fourth Git process such as `git config` (criterion 1 red) or parsing Git's configuration files by hand. Reading B: the oracle and the batch both run with the setting turned off, for example `-c log.follow=false`. That developer's results then change, and criterion 6 lists no exception for it. A test that tells the readings apart: `log.follow=true` in the test repository's config, and a held document with a merge in its history that dropped a side-branch edit. Under A the batch is compared with the `--follow` walk; under B it is compared with default history simplification. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-12 (2026-11-25) | — |
| S-9 | MINOR | SPEC | base | Acceptance criterion 7, "running the base commit's script from a temporary file" | The spec does not say how the extracted base script finds the module next to it. `scripts/check_frontmatter_current.py` line 34 imports `venv_guard`, and Python looks for it in the directory of the script being run. A copy written to a temporary file outside `scripts/` stops with `ModuleNotFoundError` before it measures anything. The implementer has to invent a workaround, and each one runs into the criterion. Setting `PYTHONPATH` for the before-runs only means the two versions run in different environments. Putting the temporary file inside `scripts/` adds an untracked file to the work tree during one version's runs, which "different checkout trees" can be read to refute. If nobody notices the import failure, the before-runs are quick exit-1 runs. They meet criterion 7 once they are reported, and criterion 8 then compares the after runtime with an import failure instead of a measurement. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-13 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5780 commits, 12 rules.

Stage-2 call, 2026-11-25: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1206 files, 5781 commits, 12 rules.
