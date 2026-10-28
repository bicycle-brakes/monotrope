---
title: "Spec — index-merge-regenerates"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-njtm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, merge, generated-index]
class: bounded
appetite: 4
adr_files: []
neighbours: []
---

# Spec — index-merge-regenerates

Local merges regenerate the plans index from the merged inputs, and an
on-request pull-request sync updates eligible branches without disturbing
protected work (lead bead coding-harness-hfsz — regenerate the index;
coding-harness-njtm — this change; coding-harness-eq6y — daily sync).
Research: `research.md`. Authority: `decisions.md#Q-1` and its five details.

## Problem

- As read on 2026-10-28, the workflow already requires regenerating
  `plans/INDEX.md` on conflicts, but only the registry gate and the Stage-2
  attempt preparation enforce the result; ordinary merges have no helper
  (`research.md`, "The doctrine" and "The second regeneration site").
- Daily branch updates are prose without an implementation, leaving agents
  to resolve the same generated-file conflict repeatedly (`research.md`,
  "The merge practice, as recorded").
- The registry's repair instruction names `make index`; the target did not
  exist when the research ran (`research.md`, "The named remedy does not
  exist") and was added by PR #267 (merge `a6ddd9d1`, 2026-10-28) before
  this change's implementation. Criterion 4 keeps it pinned.

## Terms

- **Eligible pull request:** an open, same-repository pull request targeting
  `main` that passes the protection checks below.
- **Protected pull request:** a decision pull request, one changing a
  runner-held file, or one whose locally checked-out branch has uncommitted
  changes or commits absent from its remote branch. Runner-held files mean
  the committed `scripts/stage2.py` protection prefixes; human-decided files
  in the committed provenance map also identify decision work.
- **Working days:** Monday through Friday, counted after the UTC creation
  date through the UTC run date; holidays are not modelled.

## Acceptance criteria

1. When the supported local merge completes, its committed `plans/INDEX.md`
   equals a fresh render from the complete merged plans tree.
   *Refuted by:* a merge retains either parent's index or omits either
   parent's added artefact, including when Git reported no index conflict.
2. When `plans/INDEX.md` is the only conflicted path, the supported merge
   resolves it by regeneration without asking for a textual resolution.
   *Refuted by:* it stops on that conflict or commits conflict markers.
3. If any other path conflicts, the supported merge reports those paths
   without updating the target branch.
   *Refuted by:* an ordinary conflict is resolved automatically or the
   target ref advances despite that conflict.
4. When `make index` is invoked, it runs the existing plans-index generator.
   *Refuted by:* the target is missing or produces different output from
   `python3 scripts/plans_registry.py --index` on the same inputs.
5. When the on-request sync finds an eligible branch behind the fetched
   `origin/main` with a clean merge or only an index conflict, it pushes a
   merge that preserves the pull-request head and includes that main tip.
   *Refuted by:* it only warns, loses branch commits, or pushes an index
   rendered from an incomplete tree.
6. When the sync finds a conflict outside the index, it reports the pull
   request and conflicting paths without pushing that branch.
   *Refuted by:* the report omits the paths or the branch changes remotely.
7. While a pull request is protected, the sync reports its identity and
   protection reason without merging or pushing it.
   *Refuted by:* decision, runner-held, dirty-worktree or unpushed-worktree
   cases receive a branch update or disappear from the report.
8. If eligibility or merge safety cannot be determined, the sync reports
   the error and leaves the affected branch unchanged.
   *Refuted by:* failed discovery, fetch, protection inspection, merge-tree
   execution or rendering is interpreted as permission to push.
9. If a pull-request head changes after inspection, the sync leaves the
   newly observed remote work intact and reports that the branch moved.
   *Refuted by:* the sync overwrites another writer's commit or reports an
   update of the inspected head as successful after a race.
10. When an open pull request is older than five working days, the sync
    lists its identity and age for the maintainer regardless of protection.
    *Refuted by:* the sixth working day is omitted, the fifth is overdue,
    or a weekend increases the age.
11. When the sync sees a fork pull request or a base other than `main`, it
    reports that it is outside the update scope without writing its branch.
    *Refuted by:* it pushes to a fork or merges main into another base.
12. When main is already an ancestor and the index is current, a repeated
    supported merge or sync leaves the target head unchanged.
    *Refuted by:* it creates redundant commits or pushes on every run.
13. If index generation fails or the merged plans inputs remain unreadable
    or conflicted, the supported merge does not publish a result.
    *Refuted by:* a partial render, placeholder row for invalid frontmatter,
    or failed renderer still produces a target-branch update.
14. When an operator prepares phase 6 or a local hand merge, repository
    instructions give the same supported merge command used by the sync.
    *Refuted by:* either path still prescribes hand-merging the index or
    requires choosing one parent's generated output as the final result.
15. When a committed index differs from its inputs, the existing registry
    gate still blocks it without writing a repair during checking.
    *Refuted by:* the change weakens that verdict or makes checking repair
    the index before measuring it.

## Non-goals

- GitHub's server-side Update branch and merge buttons cannot run the local
  regeneration helper; the unchanged registry gate remains their backstop.
- No scheduled job, Git hook installation, custom merge driver, automatic
  conflict resolution outside the index, or automatic merge of a pull
  request into main. The day/night orchestrator calls the sync explicitly.
- No changes to runner execution, review sessions, endpoint admission,
  tracker state, or gate definitions; no new approval or auto-merge policy.
- No installed night-run skill outside this repository is edited. No
  holiday calendar, size slicing, hot-file scheduling or stale-PR closure.
- No design phase or ADR: this remains the recorded bounded package and
  implements the existing merge doctrine without changing architecture.

## Protected areas

`scripts/stage2.py`, `scripts/plans_registry.py`, `decisions/`,
`provenance.yaml`, `model-endpoints.yaml`, `.github/`, installed harness
configuration and tracker data remain unchanged. The new helper consumes
the existing protection policy and renderer rather than weakening them.

## Definition of Done

- `make verify` green, including the criterion ledger and merge regressions.
- Move together: `scripts/pr_sync.py`, `tests/test_pr_sync.py`,
  `docs/WORKFLOW.md`, `prompts/06-review.md`,
  `templates/agents-mergeable-prs.md`, this change's workflow artefacts and
  the regenerated `plans/INDEX.md`; no implementation file is deleted.
- The pull-request file list demonstrates the protected areas and non-goals.
- One pull request names all three package beads; the final commit carries
  `Closes-Bead:` trailers for coding-harness-hfsz (index regeneration),
  coding-harness-njtm (this package) and coding-harness-eq6y (daily sync),
  with tracker closure left to the orchestrator.
- Special runs: offline real-Git merge and race fixtures, recorded with the
  tested commit; no live pull-request branch is pushed as a test.

## Open decisions

None open. The following reversible choices are `[DETAIL]` decisions made
here, with their reasons visible:

- Use an explicit merge helper, rather than a per-file merge driver, so
  regeneration sees all merged inputs and needs no local Git installation.
- Count UTC weekdays as defined above for deterministic age reporting.
- Use a four-hour phase-4 appetite, repairs included, as a stop boundary;
  neither the interview nor research states an earlier appetite.
- Conservative protection uses the existing committed runner-held and
  human-decided path policies, plus the decision label/title; uncertainty
  skips a branch rather than inventing permission.
