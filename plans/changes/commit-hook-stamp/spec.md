---
title: "Spec — commit-hook-stamp"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, commit-hook]
class: bounded
appetite: 3
adr_files: []
---

# Spec — commit-hook-stamp

A normal commit stamps its staged held documents without relying on a person remembering the date (bead `coding-harness-yv9i.2`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-23, research found that the frontmatter currency gate reports stale `updated:` dates but the pre-commit hook does not stamp them; recorded midnight incidents left verification red and consumed work. The maintainer recorded a stale hand edit that cost three draft attempts (`decisions.md#Q-1`).

## Terms

**Held document:** a Markdown path for which the provenance map requires frontmatter. **Staged content:** the version Git will commit, which can differ from the working file.

## Acceptance criteria

1. When a normal Git commit runs the installed repository pre-commit hook, each staged, added or modified held document with stampable frontmatter is committed with `updated:` set to the local date at hook execution.
   *Refuted by:* a committed staged held document retains a stale or future date or lacks the stamp.
   *Basis:* `decisions.md#Q-1`.
2. When a held document is partially staged, stamping preserves all other staged content and does not add unstaged edits to the commit.
   *Refuted by:* an unstaged edit enters the commit or staged content other than the stamp changes.
   *Basis:* `decisions.md#Q-1`.
3. When the hook stamps staged content, it leaves working-file contents and unrelated staged paths unchanged.
   *Refuted by:* an unstaged file changes or an unrelated staged path differs after the hook.
   *Basis:* `decisions.md#Q-1`.
4. If a staged held document cannot safely be stamped, the hook refuses the commit and identifies the path and reason.
   *Refuted by:* a commit succeeds with malformed, duplicate or unreadable frontmatter, or the error does not identify the affected path and reason.
   *Basis:* `decisions.md#Q-1`.
5. When the repository pre-commit hook runs, its existing Beads tracker integration retains its existing execution and failure behavior.
   *Refuted by:* a tracker hook failure that previously stopped a commit is ignored, or the tracker hook is skipped.
   *Basis:* `decisions.md#Q-1`.
6. When a staged path is deleted or is not a held document, the stamping operation leaves it alone.
   *Refuted by:* a deletion is restored or a non-held staged path is changed.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

Changing the currency gate's CI policy, the meaning of `last_reviewed:`, other existing stamp writers, hook-bypassed Git commands, or the tracker hook's managed section is outside this change. Custom hook configurations and commits made with hooks explicitly disabled remain outside the hook's reach.

## Protected areas

The Beads managed hook section and tracker database are protected to preserve tracker integration and shared data. Customer instances are outside the framework boundary.

## Definition of Done

- `make verify` green and the temporary-repository commit tests pass.
- Updated hook, stamp command, tests and workflow documentation move in the same pull request; no ADR is due.
- Protected areas and non-goals are checked against the pull request file list.
- The pull request closes `coding-harness-yv9i.2` and its last commit carries `Closes-Bead: coding-harness-yv9i.2`.
- Special runs: none.

## Open decisions

[DETAIL] Stamp the Git index without rewriting working files: this preserves partial staging and is reversible within this change. A hook deliberately disabled or replaced by a custom hook cannot run; the existing CI gate remains the backstop.
