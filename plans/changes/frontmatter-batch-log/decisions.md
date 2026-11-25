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
