---
title: "Spec — frontmatter-batch-log"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25", model: "gpt-6.1-terra"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, performance]
class: bounded
appetite: 4
adr_files: []
---

# Spec — frontmatter-batch-log

The frontmatter-current gate obtains clean documents' history in one batch while preserving its existing answers (bead `coding-harness-bxxt.21`, frontmatter batch log). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `68066450`, the research identifies one `git log` process for each clean held document in `scripts/check_frontmatter_current.py`; the reported 6–16 seconds and roughly 893 files came from an external analysis and were not remeasured in that research. The equivalence of a batch with per-path Git history, especially around merges, renames and a subdirectory root, was not established (`research.md`, 2026-11-25).

## Acceptance criteria

1. When clean held documents need dates, the check obtains their history with at most one Git log invocation per run.
   *Refuted by:* a run with two clean held documents starting two Git log processes.

2. When a clean held document has a history, its reference date and short hash equal `git log -1 --no-merges --format=%cs\ %h -- <path>` run for that path from the same root with the same Git configuration.
   *Refuted by:* a different date or hash for a path in a history containing a rename, merge or subdirectory root.

3. When a held document is modified, staged or untracked, its reference is today's local date labelled `uncommitted`.
   *Refuted by:* an edited document dated by a commit or labelled with its hash.

4. When a clean held document cannot be dated, the check exits 3 and retains the existing per-file `git log cannot date <file>: <reason>` diagnostic.
   *Refuted by:* a missing history or failed log reported as a pass, a different path or reason, or a different exit code.

5. When the check or stamp runs, its findings, output, exit status and document changes match the existing behavior for the same inputs.
   *Refuted by:* a changed stale line, verdict, exit status or stamped byte for equivalent inputs.

6. When the pull request is prepared, it records before and after runtimes of the gate on this repository at the same commit, with the measurement method and outcomes.
   *Refuted by:* a missing runtime, different measured commits, or an unreported failing run.

## Non-goals

- Changing which documents are held, date policy, the stamp, gate configuration or command-line interface.
- Optimizing the second held-file enumeration or other verification gates.
- Claiming a fixed speedup or changing Git history semantics to obtain one.

## Protected areas

`provenance.yaml`, `decisions/gates.yaml`, `.github/workflows/ci.yml` and `docs/governance/gate-catalog.md` remain untouched: the gate's scope and integration do not change.

## Definition of Done

- `make verify` green; the pull request records the same-commit timing and its outcomes.
- Changed documents, models and ADRs outside this change folder: none.
- The protected areas are untouched and the non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.21` (frontmatter batch log), and its last commit carries `Closes-Bead: coding-harness-bxxt.21`.

## Open decisions

[DETAIL] The implementation appetite is four hours, including repairs; it is a reversible stop point for this bounded change, not a runtime promise. No maintainer decision is open.
