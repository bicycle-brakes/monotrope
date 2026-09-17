---
title: "Session handover: Omnigent-first coding harness target, 2026-09-17"
category: handover
created: 2026-09-17
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex
  version: "2026-09-17"
tags: [handover, architecture, omnigent, workflow]
target_ref: eddfc0b
bead: coding-harness-atx
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Handover: Omnigent-first target

The maintainer confirmed on 2026-09-17 that Omnigent should coordinate
parallel agents from the first proof of concept. The session produced three
linked English artefacts under `docs/architecture/`: a target state, a gap
analysis against commit `eddfc0b`, and a dependency-ordered implementation
plan. The README points to them. The older target proposal is marked
superseded for sequencing and current-state claims, while its historical
decisions remain available.

The target starts two coding workers in separate worktrees and keeps Beads
writes with one coordinator until the five-check worktree test proves more.
The first implementation dependencies are a single executable gate manifest,
truthful rule enforcers, a shared agent instruction entry and the minimum
change contract. The first Omnigent pilot must prove its policies, sandbox,
bounded sessions, recovery and fallback on the pinned release.

After the initial draft, all five Markdown files in `docs/research/` were
reviewed end to end, including both arc42 documents. The three architecture
artefacts now account explicitly for the research index and four sources.
The resulting additions are a one-page roadmap above Beads, discovered-work
links, compaction protection, living-spec delta vocabulary, a full Beads
backup/restore exercise, and two pilot probes: worktree creation under the
effective Omnigent policy and an actual stop at the cost limit. These are
proposals; version-specific Omnigent and Beads behavior still needs testing.

At `eddfc0b` on 2026-09-17, `python3 -m pytest tests -q --tb=no` reported
64 failed, 182 passed and 4 skipped. The run preceded the documentation
edits; it measures the inherited mechanism migration, not the quality of the
new documents. YAML frontmatter and local links of the architecture documents
were checked, as was `git diff --check`. No harness code was changed. No
Omnigent or concurrent worktree run was performed.

Next session: review the three artefacts for intent and boundary accuracy;
record an ADR that changes the M0/M3 parallelism sequence; then reconcile the
existing M0 Bead and its worktree dependency with that decision. Start the
gate-manifest and rule-enforcer work before the two-worker pilot. The full
implementation plan contains the pass and abort criteria.
