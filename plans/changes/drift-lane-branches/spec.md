---
title: "Spec — drift-lane-branches"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-l54q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, plans-registry, drift]
class: bounded
appetite: 2
adr_files: []
---

# Spec — drift-lane-branches

The reverse coupling recognises running work on pushed branches while still reporting claims without an artefact (bead `coding-harness-l54q`). Research: `research.md`; correction and scope: `decisions.md`.

## Problem

- The registry checks running beads against artefacts in the checked tree only (`scripts/plans_registry.py`, researched 2026-11-21); the correction in `decisions.md` records that active lanes keep their change folders on unmerged branches, so the scheduled check reported them as drift on all eight nights of 2026-11-13–20.
- The drift job's checkout does not fetch all branch refs (`scripts/ci_gates.py`, researched 2026-11-21), so the job cannot distinguish those lanes from claims with no artefact anywhere.

## Terms

**Branch artefact:** a Markdown file under `plans/changes/` on a `refs/remotes/origin/*` branch whose frontmatter names the bead, using the same interpretation as an artefact in the checked tree.

## Acceptance criteria

1. When an in-progress bead has a branch artefact but no artefact in the checked tree, the reverse coupling does not report that bead as drift.
   *Refuted by:* The bead is reported as having no artefact.
2. When an in-progress bead has no artefact in the checked tree or on any origin remote-tracking branch, the reverse coupling reports that bead as drift with the existing missing-artefact message.
   *Refuted by:* The bead is omitted or reported without that message.
3. When branch-only artefacts satisfy running beads, an INFO summary reports the number of distinct running beads found on branches and examples of their branch names.
   *Refuted by:* The count includes duplicates or checked-tree matches, or the summary lacks the count or branch examples.
4. When no origin remote-tracking branches exist, the reverse coupling retains its checked-tree-only behaviour and reports that absence as INFO.
   *Refuted by:* A missing bead is suppressed or no INFO explains the absence of refs.
5. When the scheduled or manually dispatched drift job runs the strict registry check, it first fetches all origin branch heads into origin remote-tracking refs.
   *Refuted by:* The generated job omits that fetch, fetches only the checked-out branch, or runs the strict check first.
6. If branch enumeration or reading a branch fails, the registry check reports a blocking failure instead of treating the incomplete search as a complete result.
   *Refuted by:* An unreadable branch or failed ref enumeration yields a successful or ordinary missing-artefact verdict.
7. When the drift job cannot fetch the branch heads, it does not run the strict registry check as though the branch search were complete.
   *Refuted by:* A failed fetch is followed by a strict check that can report a complete result.
8. When the registry examines branch artefacts, it leaves the checked-out branch and working tree unchanged.
   *Refuted by:* The check switches a branch or changes a tracked or untracked working-tree file.

## Non-goals

- Releasing or closing stale claims; the tracker writer handles those after the change is merged.
- Synchronising lane branches with main, reading unpushed work or changing the forward artefact-to-bead coupling.
- Declaring the scheduled job green before a run demonstrates that no other drift remains.

## Protected areas

Tracker data and branch contents remain unchanged: the check reads them, and stale-claim cleanup is separate work.

## Definition of Done

- `make verify` green; a subsequent scheduled drift run with only running-lane claims demonstrates the live outcome, identified by its run and commit in the pull request or follow-up.
- The generated `.github/workflows/ci.yml` moves with `scripts/ci_gates.py`; no ADR is changed.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes `coding-harness-l54q` and its last commit carries `Closes-Bead: coding-harness-l54q`.
- Special runs: the scheduled drift run described above.

## Open decisions

- [DETAIL] A failed Git read is a BLOCK, not an empty branch set: otherwise the check would present an incomplete measurement as a real drift result.
- [DETAIL] Count distinct branch-only beads and show a bounded sample of branch names: duplicate artefacts or branches must not inflate the summary.
- [DETAIL] The phase-4 appetite is two hours including repairs: this bounds a small registry and generated-job change without altering its scope.
