---
title: "Decisions — merge-queue"
status: draft
implementation_status: none
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-eh42
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# merge-queue — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: one repository setting, its
ruleset check, the CI trigger and the texts that describe the merge; no new
mechanism.

## SKIP · interview

status: skipped
reason: the maintainer approved the switch to a GitHub merge queue on 2026-10-28 in the decision interview (bead coding-harness-eh42 notes) and opened this lane on 2026-10-30; the remaining choices are details an agent decides below, and the merge of the decision pull request is the maintainer's.

## Details for the draft

[DETAIL] **The ruleset requirement becomes "the merge result is tested".**
Requirement (6) of `tests/test_repo_settings.py` is met by an active
`merge_queue` rule on `main`, or, as today, by
`strict_required_status_checks_policy: true`. Reason: both make the tested
commit the merged one; the check must not go red during the switch.

[DETAIL] **The required check runs in the queue.** `scripts/ci_gates.py`
(`generate_ci`) adds the `merge_group` event and lets the `verify` job run
on it, and `.github/workflows/ci.yml` is regenerated from it, so `ci-drift`
stays green. Reason: a queued merge waits for the required `verify` on the
`merge_group` ref; without the event it never starts.

[DETAIL] **Queue settings: one at a time, merge commits.** Merge method
`merge` (as today), group size 1, and checks on the group's ref. Reason:
the repository merges with merge commits, and one at a time keeps a red
group's cause readable.

[DETAIL] **RB-G7 changes its second and third sentence only.** The rule
keeps its id, level and enforcers; the text says the merge result is
tested, by the merge queue or the up-to-date rule. Reason: the rule's goal
(the merge state is what is checked) stays.

[DETAIL] **Merging via the queue.** `prompts/07-commit.md`, "The merge",
and `docs/WORKFLOW.md`, "Pull requests stay mergeable", say: `gh pr merge
<n> --merge --match-head-commit <sha>` puts the pull request into the queue;
no `update-branch` before it. Reason: the queue merges `main` itself.

[DETAIL] **The live setting changes after the merge.** The decision pull
request changes texts, tests and CI; the ruleset switch is applied with
`gh api` after the maintainer merged it, and the gate `ruleset` measures
it on the writer machine. Reason: a decision takes effect when the
maintainer merges (house rule 8).
