---
title: "Decisions — frontmatter-batch-log"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, gates, performance]
---

# frontmatter-batch-log — Decisions

## SKIP · interview

status: skipped
reason: The change is a behaviour-preserving speed-up of one gate with a stated remedy (bead coding-harness-bxxt.21, filed at the maintainer's request on 2026-11-24 from a checked analysis): replace the per-document `git log -1` calls of scripts/check_frontmatter_current.py with one batched pass; the gate's verdicts and messages must not change, so no design choice is left to the maintainer.

## Details decided by the orchestrator

[DETAIL] **D-1 (equivalence first)**: the batched reader must give, for every held document, the same commit date and short hash the per-file `git log -1 --no-merges -- <file>` gives today; a test compares both on a synthetic repository with renames, merges, a file under a subdirectory root and a file with no commit. Reason: the explore could not show the two forms are equal (research.md, "What is unclear").

[DETAIL] **D-2 (paths and root)**: the batch keeps working when `--root` is a subdirectory of the repository (paths taken relative to that root), as the per-file call does today. Reason: research.md names the path-base difference.

[DETAIL] **D-3 (messages unchanged)**: every STALE line and the per-file `git log cannot date <file>` error keep their exact wording; dirty or untracked files keep skipping the date check. Reason: the gate's output is read by people and tests.

[DETAIL] **D-4 (measure)**: the pull request records the gate's run time before and after on this repository at the same commit. Reason: the 6-16 s figure is from an external analysis, not measured here.

[DETAIL] **D-5 (spec review S-1, what counts)**: Reading B — the number of Git processes the date check starts is bounded and does not grow with the number of held documents (at most three for the whole run); a per-document fallback of any Git command refutes criterion 1. Reason: the per-document process count is the cost the bead removes.

[DETAIL] **D-6 (spec review S-2, the timing decides)**: Reading B — the change ships only if the gate's run time on this repository, measured before and after at the same commit on the same machine, is at least halved; otherwise the lane stops and reports. Reason: run time is the change's only purpose.

[DETAIL] **D-7 (spec review S-3, literal paths)**: held paths are literal: the oracle and the batch both treat them as literal paths (`GIT_LITERAL_PATHSPECS=1` or `:(literal)`), so a name with `*`, `?`, `[` or a leading `:` matches only itself. Reason: a held document is one file, never a pattern.

[DETAIL] **D-8 (spec review S-4, a failed batch; amends D-3 for this case)**: when the single batched invocation fails, the gate reports one message naming the command and its protected stderr and blames no document, with the same exit status as today's per-file failure; the per-file "git log cannot date <file>" message stays for a document the batch output does not date. Reason: a batch failure belongs to no document.

[DETAIL] **D-9 (spec review S-5, scope of the count; narrows D-5)**: Reading A — the bound counts the Git processes of the date lookup (`reference_dates`): the dirty-set calls plus the batch, at most three, independent of the number of held documents; the preflight and the held-file enumeration stay as they are and are not counted. Reason: the per-document date calls are the cost the bead names.

[DETAIL] **D-10 (spec review S-6, protected stderr)**: "protected" means bounded, not redacted: the batch's stderr is cut to the last 20 lines and 2,000 characters with a truncation marker; the gate takes no dependency on the runner's secret redaction. Reason: git's stderr names paths, not secrets, and a gate must stay self-contained.

[DETAIL] **D-11 (spec review S-7, timing at one commit)**: Reading A — one commit is checked out and both script versions run against that same tree (the base commit's script via `git show` into a temporary file, run with `--root` on the checkout), five runs each, median compared. Reason: the held set and the dirty state must be identical for a fair comparison.

