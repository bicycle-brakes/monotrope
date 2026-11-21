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

**Branch artefact:** a Markdown file under `plans/changes/` on an origin remote-tracking branch, including `archive/` and excluding `INDEX.md` and filenames beginning with `_`, whose line-one YAML frontmatter has the bead value; body text is not metadata. The checked-tree parser defines YAML aliases, merge keys and quoted values alike.

## Acceptance criteria

1. When branch search is enabled and a complete search finds an in-progress bead with a branch artefact but no artefact in the checked tree, the reverse coupling does not report that bead as drift.
   *Refuted by:* The bead is reported as having no artefact.
2. When branch search is enabled and a complete search finds that an in-progress bead has no artefact in the checked tree or on an origin remote-tracking branch, the reverse coupling reports that bead as drift with the existing missing-artefact message.
   *Refuted by:* The bead is omitted or reported without that message.
3. When branch search completes over at least one origin branch, the INFO summary reports the number checked, the number found only on branches, and the number without an artefact anywhere.
   *Refuted by:* A checked-tree match or duplicate inflates the branch-only count, or the missing count includes a branch-only match.
4. When branch search is needed and no origin remote-tracking branches exist, the reverse coupling retains its checked-tree-only behaviour, including its existing two-count summary, and reports that absence as INFO.
   *Refuted by:* A missing bead is suppressed, the existing summary changes, or no INFO explains the absence of refs.
5. When the scheduled, manually dispatched, or local strict drift gate runs, it first fetches all origin branch heads into origin remote-tracking refs, pruning deleted heads, before invoking the strict registry check with branch search enabled.
   *Refuted by:* The gate fetches only one branch, keeps deleted heads, omits the branch-search option, or runs the check first.
6. If branch search is needed and Git is unavailable, the root is not a repository, ref enumeration fails, or a branch read fails, the registry check reports a BLOCK with the number of beads still unresolved, credits matches already found by completed reads, withholds missing-artefact DRIFT lines for unresolved beads, and omits the complete-search summary.
   *Refuted by:* A failed search is treated as complete, a found bead is lost, an unresolved bead is reported missing, or the unresolved count or BLOCK is absent.
7. When the strict drift gate's fetch fails, that gate fails without invoking the registry check.
   *Refuted by:* The registry runs after the failed fetch, or the gate succeeds.
8. When the registry examines branch artefacts, it leaves the checked-out branch and working tree unchanged.
   *Refuted by:* The check switches a branch or changes a tracked or untracked working-tree file.
9. When branch search is not explicitly enabled, the registry retains its existing checked-tree-only behaviour, including in the pull-request gate and local `make verify`.
   *Refuted by:* An ordinary check searches branches or changes its verdict because of a branch read.
10. When an eligible file on a searched branch has absent or unparseable frontmatter, branch search does not treat it as an artefact and counts it once per branch and path in an INFO report.
    *Refuted by:* The file satisfies a bead, is silently omitted from the count, is counted only once across two branches, or produces a BLOCK solely because its frontmatter is malformed.
11. When branch-only beads are found, the INFO summary chooses each bead's first sorted matching origin branch, sorts those selections and displays the first three or fewer, retaining repeated names selected by different beads.
    *Refuted by:* The sample is not the first three sorted selections, a repeated selection is dropped, or a bead contributes a later branch instead of its first.
12. When branch search enumerates origin refs, it excludes the `origin/HEAD` symbolic ref and includes `origin/main` as a branch.
    *Refuted by:* `origin/HEAD` satisfies a bead or appears in the sample, or an artefact only on `origin/main` is ignored.
13. When a branch file is interpreted as an artefact, its bead identity follows the checked-tree frontmatter interpretation, including quoted, escaped and aliased YAML values and merge keys, rather than matching text in the body.
    *Refuted by:* A valid quoted, escaped, aliased or merged bead is missed, a body-only match satisfies a bead, an underscore-prefixed file or `INDEX.md` is counted, or an archive file is excluded.
14. When the tracker is unavailable, no bead is in progress, or every running bead already has a checked-tree artefact, the reverse coupling performs no branch search and emits no branch-search INFO or BLOCK.
    *Refuted by:* Any of those cases reads refs or emits a branch-search message.

## Non-goals

- Releasing or closing stale claims; the tracker writer handles those after the change is merged.
- Synchronising lane branches with main, reading unpushed work or changing the forward artefact-to-bead coupling.
- Declaring the scheduled job green before a run demonstrates that no other drift remains.

## Protected areas

Tracker data and branch contents remain unchanged: the check reads them, and stale-claim cleanup is separate work.

## Definition of Done

- `make verify` is green; the pull request includes `decisions/gates.yaml` and the generated `.github/workflows/ci.yml`; no ADR is changed.
- The protected areas remain untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes `coding-harness-l54q` and its last commit carries `Closes-Bead: coding-harness-l54q`.
- After merge, the tracker writer records the first scheduled drift run and its commit on the bead whatever the result, and opens follow-up work if real drift remains. The original live outcome remains a green scheduled job on a night with only running-lane claims; it cannot be observed before merge.

## Open decisions

- [DETAIL] Branch search is opt-in through `--branches`; this prevents a new Git-read BLOCK in unrelated pull-request and local verify gates.
- [DETAIL] The strict drift gate declares the fetch and check in one command with failure short-circuiting; its existing generated step and local invocation share that declaration.
- [DETAIL] A failed Git read is a BLOCK, while malformed branch frontmatter is counted as INFO: the former makes the search incomplete, the latter is not an artefact.
- [DETAIL] Report distinct branch-only beads and at most three sorted example branches, excluding the symbolic `origin/HEAD`; this makes the summary testable and concise.
- [DETAIL] Record the first post-merge scheduled run regardless of outcome; it cannot be observed before the pull request merges.
- [DETAIL] The phase-4 appetite is two hours including repairs: this bounds the registry and generated-job change without altering its scope.
- [DETAIL] Inspect every eligible branch file when resolving beads: literal `bead:`-line narrowing cannot preserve YAML aliases, merge keys and escaped values, so the S-9 narrowing is rejected; count malformed files per branch and path.
- [DETAIL] Retain duplicate branch names in the bounded sample, one selection per bead; the specified sort then has one unambiguous result.
- [DETAIL] An incomplete search omits the complete-search summary and reports its unresolved count in the BLOCK, so it cannot imply that all branches were examined.
