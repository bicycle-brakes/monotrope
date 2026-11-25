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
