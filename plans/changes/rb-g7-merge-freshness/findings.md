---
title: "Findings — rb-g7-merge-freshness"
category: findings
status: draft
implementation_status: partial
date: 2026-10-08
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-34z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — rb-g7-merge-freshness

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 293 files, 666 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 294 files, 669 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | MAINT | base | `tests/test_ci.py:490` | Adding `run: git -C . checkout ${{ github.event.pull_request.head.sha }}` after checkout leaves `_merge_ref_findings` empty, including when emitted by the generator. The command switches verification to the PR head, but the guard misses Git commands with global options. Such tree changes must produce a finding. [Acceptance criterion 1] | Codex | closed — `_MOVES_THE_TREE` reads git global options and `gh pr checkout`; test_the_merge_ref_check_flags_a_planted_fault[git-c-checkout-step], [gh-pr-checkout-step], red without the repair | no |
| F-2 | BLOCKER | SPEC | base | `tests/test_repo_settings.py:201` | With the existing `verify` rule non-strict, a second rule containing `strict_required_status_checks_policy: true` and `required_status_checks: [null]`, and empty bypass lists, `measure` returns `[]`. A nonempty list is counted without validating its entries, so an unknown API shape passes the gate. It must return exactly one `not measured:` finding. [Acceptance criterion 5] | Codex | closed — `measure` refuses a check entry that is no object with a context; test_an_unreachable_api_is_not_a_pass[rules-with-a-check-that-is-no-object], red without the repair | no |

Phase 6 verdict: codex 01a11abe-f4ea-76f3-9f86-63ec41c9d652, 2026-10-08
Reviewer session: codex 01a11abe-f4ea-76f3-9f86-63ec41c9d652 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — GLM loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | MAINT | code | tests/test_ci.py:490 | The tree-movement detector matches only `git checkout`, `git switch` and `git reset`, yet its finding text claims "a `run` moves the checked-out tree": a later step running `git pull`, `git merge`, `git rebase` or `git restore` replaces the checked-out merge-ref tree just as well and passes the check unflagged, so the message promises more coverage than the regex delivers. | GLM | taken — test_the_merge_ref_check_flags_a_planted_fault[git-pull-step] | no | agree |
| L1-2 | MINOR | MAINT | docs | docs/governance/quality-gates.md:77 | The added sentence says that when `main` moves, the pull request "wird aktualisiert und neu geprüft" — indicative passive, as if the platform did it; nothing updates the branch automatically, the merge simply stays refused until someone updates it, which is why the merge procedure gains a manual update step in this same change. A reader of this page may wait for an automation that does not exist. | GLM | taken — criterion 11 (quality-gates.md wording) | no | agree |
| L1-3 | MINOR | MAINT | code | tests/test_repo_settings.py:12 | The numbered requirement list still reads "(5) no bypass — every ruleset that supplies (1) to (4) shows an empty bypass list", while the RB-G7 paragraph added directly below says requirement (5) "then covers that ruleset" for a ruleset supplying only the up-to-date flag: list and paragraph contradict each other, and the list understates what the code now checks (the flag's suppliers are in the bypass check). | GLM | taken — criterion 3 (test_repo_settings.py docstring) | no | agree |

Rounds run: 1

Kept from the loop record:

The answer was not only six-cell rows; what is not one is kept below as it came.

I've verified the change end to end against the worktree: the merge-ref checker passes on both the committed workflow and the generator output (traced every job, step and `run` in the workflow); the nine planted faults and the generator-emitted `ref:` each produce findings; the new floor tests are consistent with `ruleset_findings`/`_suppliers` (I traced each stub case, including the second-ruleset and bypass ones); the mutation-name trap is genuinely avoided (`MUTATIONS_NAMEN` anchors `^def test_…(goes_red|red_on|…)`, the new names use `flags`, and the ratchet's file-scan logic confirms it); the valve close follows the recorded precedent (entry out, dated comment, all remaining deadlines later, no orphaned `Ramp:` in the parsed rule rows, §7 history prose is not scanned as a row); version/history/enforcer rows satisfy the rule-set tests' parsers; the ADR answer file matches the checker's required keys and the repo's convention; and the valve-count fallback still catches an emptied list. What remains are three small, real defects:

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 294 files, 670 commits, 12 rules.
