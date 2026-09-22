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


## Addendum: consistency review and human planning, 2026-09-18

This addendum supersedes the initial draft above where its wording differs.
The maintainer requested corrections to all four architecture documents,
remaining-gap analysis, a planning surface especially for people with ADHD,
and an updated research index. Three Sol subagents reviewed CrewAI, Alibaba
Open Code Review and Addy Osmani's Agent Skills using upstream sources and
wrote separate research assessments. Sol also revised the planning research,
updated the index and integrated the external-tool dispositions.

The current target explicitly carries D-1–D-17 and O-1–O-4 forward. Early
parallelism changes sequencing; it does not remove LikeC4, complete spec fields,
three full qualification runs or immediate public-readiness foundations. The
historical proposal keeps the interview outcomes and now identifies its stale
recommendations and corrected editorial counts.

The current no-writes-during-parallel-sessions rule remains active. A future
pilot needs an explicit coordinator permission and enforced exclusive writer
ownership before tracker writes. Isolation and ownership are M0 prerequisites;
direct worker tracker writes are a separate qualification requiring a supported
mode and all five checks. A passing sample does not make embedded Dolt a
concurrent-writer store. The live tracker was not written during this revision;
the previously closed planning item remains unchanged (coding-harness-atx).

The revised contracts cover protected verifiers, shared Git and shell access,
candidate assembly versus human final merge, stale evidence, review escalation,
aggregate limits and child cancellation, context packets and separate restart/
host-loss recovery. Reviewer qualification uses faulty and clean controls;
a real PR need not contain a defect. The kit now has proposed artifact roles,
destinations and bootstrap/update/rollback acceptance.

Human planning is an optional Markdown surface over the same authorities:
roadmap direction, Beads work status, change decisions and handovers. The
proposal includes one next action, low-friction capture, a resume breadcrumb,
batched updates and visible snapshot freshness. Obsidian is an optional client;
Foam, Zettlr and plain Markdown remain alternatives. These adjustable defaults
need a trial with the maintainer; no client or plugin was installed.

External-tool disposition: retain Omnigent as coordinator; consider CrewAI
only for a measured missing function; evaluate Open Code Review as advisory
input to the independent reviewer; selectively adapt Agent Skills techniques
without importing another workflow. Source reviews establish neither runtime
fitness nor vulnerability status in a future pinned build. No upstream code
was executed. Optional trials do not waive endpoint or disclosure conditions.

During the revision GitHub showed that another session had rebased the existing
draft PR onto main: PR #8's head was 513005e and its base was main. Compared with
the previous local head 9712f76, the tree added only the other session's tracker
handover. Preserve that history and build the revision on the remote head;
do not force-push the old branch or retarget the PR to the retired tracker base.
The assessment's eddfc0b test baseline remains historical, not a new measurement.

Next implementation still begins with decision records and tracker reconciliation
under exclusive ownership, followed by classification of inherited red tests,
the canonical gate and truthful enforcers. The research index is the entry point
for the new source notes. This revision delivers documentation only.

Validation on 2026-09-18: all ten revised/new documents passed YAML parsing,
75 local-link/anchor checks, coverage of the 21 interview decisions, research
index coverage and the handover schema; `git diff --check` passed. The full
implementation suite was not rerun for documentation changes. The ten documents
were copied back to the requested checkout only after their initial content
hashes (or absence for new files) were checked; its index, branch and tracker
were left untouched.
