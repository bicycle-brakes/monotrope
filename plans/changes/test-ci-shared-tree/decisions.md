---
title: "Decisions — test-ci-shared-tree"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, xdist]
---

# test-ci-shared-tree — Decisions

## SKIP · interview

status: skipped
reason: The change is a test-only fix with one stated remedy and no open design choice: the bead (coding-harness-bxxt.12, filed at the maintainer's request on 2026-11-24 from a checked analysis) says to build the orphan-script case in a temporary copy instead of writing into the shared scripts/ directory; behaviour of scripts/ and of every gate stays unchanged.

## Details decided by the orchestrator

[DETAIL] **D-1 (where the orphan case lives)**: the test builds a throwaway tree (tmp_path) holding the files the orphan check reads, writes the orphan script there and points the glob at that tree, so no file is ever created under the repository's scripts/. Reason: the bead's remedy; it keeps parallel workers and the kit probe's cached file list from ever seeing the file.

[DETAIL] **D-2 (the probe's dated test count)**: scripts/kit/probe.py line 259 counts this test by name; the test keeps its name so the count stays true, or the count moves with the rename in the same change. Reason: the explore found the dated count (research.md).

[DETAIL] **D-3 (scope)**: --dist worksteal (coding-harness-bxxt.18) and a parallel kit probe are not part of this change; it only removes the shared-tree write they depend on. Reason: bead scope.
