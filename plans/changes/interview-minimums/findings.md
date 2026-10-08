---
title: "Findings — interview-minimums"
category: findings
status: draft
implementation_status: none
date: 2026-10-08
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-6yg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — interview-minimums

Stage-2 call, 2026-10-08: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 309 files, 701 commits, 12 rules.

## Phase 2a — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`, Protected areas, Definition of Done and Open decisions | [DIVERGENT] This feature must have an ADR answer for `verify` to pass, as documented in research, but the spec forbids creating an answer file and requires protected areas to remain untouched. No answer for this change exists in HEAD. Recording the pending answer violates the scope; omitting it prevents completion. | Codex | in spec | — |
| F-2 | MAJOR | SPEC | base | `spec.md`, Terms and AC 4 | [AMBIGUITY] The counted-record definition excludes every record whose ID occurs elsewhere, while AC 4 excludes duplicates of an ID already counted. With answered maintainer records Q-1, Q-1, Q-2 and Q-3, the first reading counts two and rejects a feature; the second counts three and accepts it. | Codex | in spec | — |
| F-3 | MAJOR | SPEC | base | `spec.md`, AC 5; `decisions.md`, Q-2 | [AMBIGUITY] AC 5 can require a skip line for every non-ADR bounded change, or require that line only when the interview was skipped. A bounded change with one completed maintainer interview and no skip fails under the first reading and may pass under the second. No passing condition defines completion of a bounded interview. | Codex | in spec | — |
| F-4 | MAJOR | SPEC | base | `spec.md`, AC 5 and Terms | The gate-readable representation of a reasoned skip and of the three answered spike topics is missing. An implementer must invent how these differ from merely mentioning “learning goal”, “time budget” and “expected outcome”, or from a skip marker with no actual justification. The question-record format does not define either case. | Codex | in spec | — |
| F-5 | MAJOR | SPEC | base | `spec.md`, AC 2 and AC 9 | No rule identifies which change owns an ADR modification during a repository-wide gate run. With eligible changes A and B holding five and three records respectively, and only A modifying an ADR, applying the ADR minimum globally incorrectly rejects B. Selecting only A requires an ownership rule that the spec does not supply; an ADR-only diff has no specified outcome either. | Codex | in spec | — |
| F-6 | MAJOR | SPEC | base | `spec.md`, AC 6–7 | [AMBIGUITY] “HEAD sits on main” can mean a checkout of the local branch or the main commit regardless of checkout mode. For detached HEAD at a merge equal to `origin/main`, the branch reading uses merge-base HEAD and sees no ADR changes; the commit reading uses the first parent and detects them. The hosted post-merge result therefore depends on an unstated interpretation. | Codex | in spec | — |
| F-7 | MAJOR | SPEC | base | `spec.md`, AC 8; `decisions.md`, Q-4 | [AMBIGUITY] The strict date rule and the exemption for all existing stock differ for changes created before the merge on its calendar date. If this change merges on 2026-10-08, an existing feature dated 2026-10-08 with fewer than three records is checked and rejected under AC 8, but skipped under Q-4’s existing-stock exemption. | Codex | in spec | — |
| F-8 | MAJOR | SPEC | base | `spec.md`, Counted record and AC 1–4; `decisions.md`, G-1 and G-4 | Distinct IDs are sufficient for counting, but the maintainer requires distinct substantive questions and excludes repeated confirmations. Three differently numbered records repeating the same settled confirmation satisfy the specified counting conditions. The spec does not assign enforcement of substantive distinctness to either the gate or a review obligation. | Codex | in spec | — |
| F-9 | MAJOR | SPEC | base | `spec.md`, AC 10 | The stated refuting check cannot detect omission of the required gate. Given `gates.yaml` without `interview-minimums` and a workflow correctly regenerated from that list, `ci_gates.py --check-ci` exits 0. It checks agreement between the files, so the missing declaration—and matching omission from CI—does not turn this acceptance check red. | Codex | in spec | — |

Reviewer session: codex 01a11c4d-7cf9-78d3-81e5-d51fe3941095

## Addendum — 2026-10-08, all nine rows worked into the spec

Every row is `in spec`; none is rejected. The four `[AMBIGUITY]` rows were
settled by the maintainer in the directing conversation and recorded as
`decisions.md` Q-5 to Q-8: F-2 first occurrence counts, later duplicates are
ignored; F-3 a `bounded` change owes at least one counted record or a skip
record with a reason; F-6 the branch reading — a genuine `main` checkout uses
the first parent as base, everything else the merge base, unmeasurable exits
3; F-7 the cut-off compares strictly greater, so same-day stock stays exempt.
F-1 resolved the divergence: the answer file
`decisions/answers/interview-minimums/adr.yaml` was recorded through
`harness.py decide adr` from the maintainer's stated answer and travels in
this decision pull request; Protected areas and Definition of Done now say
so. F-5 became the owning-change attribution (Terms, AC 2); F-8 the split
that the gate counts records while the phase-6 review judges substantive
distinctness (AC 4, Non-goals unchanged); F-9 the declaration test beside
`ci-drift` (AC 10). The revised `spec.md` is the one yardstick from here on.

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 313 files, 702 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 313 files, 702 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-10 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:149–156,255–259` | A feature dated `2026-10-09` with no interview exits 0 when its YAML date is quoted or followed by a comment. Both forms are valid metadata, but the reader returns `None` and silently exempts the change. The demonstrated `--change` invocation even reports it as green. [AC 1, 8] | Codex | taken — test_quoted_date_does_not_exempt | no |
| F-11 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:134–138,208–214`; `docs/WORKFLOW.md:105` | [DIVERGENT] A feature dated after the cut-off with zero records exits 0 after moving into `plans/changes/archive/`; nothing is measured. The implementation ignores archived changes, and the workflow explicitly exempts everything archived, while the spec exempts class minimums by date. Normal completion and archival therefore bypass the feature minimum. [AC 1, 8, 11] | Codex | taken — test_archived_post_cutoff_feature_is_measured; docs/WORKFLOW.md now exempts the stock by date, not by place | no |
| F-12 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:160–191` | Three Q-blocks containing only `answered_by: maintainer` and `status: answered` make a feature pass. The demonstrated blocks contain no `asked`, no `answer` and no Y-statement, so they are not interview records under the specified format. `_counted` nevertheless counts all three. [Terms, AC 1] | Codex | taken — test_minimal_blocks_are_not_interview_records | no |
| F-13 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:119–122` | A depth-one clone checked out detached at `origin/main`, containing an ADR change with four bounded interview records, exits 0. When `HEAD^` cannot be read, `_base` substitutes HEAD and loses the committed ADR delta. Missing comparison history must produce exit 3 rather than a successful measurement. [AC 2, 6–7] | Codex | taken — test_detached_at_tip_without_main_line_env_is_not_measured | no |
| F-14 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:116–120` | A detached checkout of an older ancestor of `origin/main` uses its first parent instead of its merge base. In the demonstrated clean checkout, this replays an old ADR edit and rejects an exempt bounded change with four records. Equality between merge-base and HEAD does not establish that HEAD equals the freshly merged tip. [AC 7] | Codex | taken — test_detached_at_tip_without_main_line_env_is_not_measured | no |
| F-15 | BLOCKER | MAINT | base | `scripts/check_interview_minimums.py:106–120,228–246`; `spec.md`, AC 7 | A newly started feature branch at `origin/main`, with three valid answers and no ADR edits relative to main, exits 1 demanding five answers. The first-parent comparison replays main’s previous ADR commit and attributes it to the new feature. The specified tip rule does not distinguish newly begun work from validation of the previous landfall. | Codex | taken — test_new_branch_at_tip_is_not_charged_main_landfall | no |
| F-16 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:125–131` | A bounded change with four answers passes when an ADR edit is staged but the working file is restored to its base contents. `git diff <base>` then hides the index change; the demonstrated check exits 0 although committing the index would change the ADR. Staged ADR changes must still trigger five records. [AC 2] | Codex | taken — test_index_only_staged_adr_is_seen | no |
| F-17 | BLOCKER | SPEC | base | `scripts/check_interview_minimums.py:238–239,285–289` | With a valid ADR owner holding five records, `--change real-typo` exits 0 and reports the nonexistent change as green. Measuring the ADR owner increments the global counter, which suppresses validation of the requested name. A passing unrelated measurement must not allow a missing target folder to pass. [AC 12] | Codex | taken — test_change_flag_typo_is_red_even_when_another_change_passes | no |
| F-18 | BLOCKER | MAINT | base | `docs/WORKFLOW.md:382`; `scripts/check_interview_minimums.py:106–120` | [DIVERGENT] For a detached post-merge checkout at `origin/main`, the workflow’s stage-1 table prescribes the merge base because this is not a main-branch checkout. The current spec and implementation prescribe the first parent. These instructions select different ADR deltas for the same supported checkout state. [AC 7] | Codex | taken — the docs/WORKFLOW.md stage-1 row restates the refined rule verbatim; the divergence is closed | no |
| F-19 | MAJOR | MAINT | base | `tests/test_check_interview_minimums.py:28–54,309–318` | The Git fixtures inherit commit-signing configuration and attempt interactive signing of their seed commits. With signing enabled and its signer unavailable, the review run produced 23 setup errors and one failure before the gate assertions. The suite passed only after isolating Git configuration; ordinary local verification inherits this failure. [Definition of Done: verify green] | Codex | taken — the fixtures isolate Git configuration (GIT_CONFIG_GLOBAL/SYSTEM to the null device); the suite stands green under an inherited signing setup | no |
| F-20 | MAJOR | SPEC | base | `tests/test_check_interview_minimums.py:352–358` | The documentation test passes with the original `AGENTS.md` that calls the interview optional. This was reproduced by supplying HEAD’s version to the test: its fallback accepts “three” from the introductory “three stages”. The specifically prohibited optional feature interview cannot make this acceptance test red. [AC 11] | Codex | taken — the assertions now demand the duty markers and fail against the original AGENTS.md | no |

Phase 6 verdict: codex 01a11c4d-7cf9-78d3-81e5-d51fe3941095, 2026-10-08

## Phase 4b — GLM loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | base | `spec.md` Terms ("Counted record") vs `scripts/check_interview_minimums.py` `_counted` | The Terms define a counted record as one "whose question id has no earlier record in the same file", but `_counted` only tracks ids it already counted: when `Q-1` first appears with `answered_by: agent` or `status: open` and a later `Q-1` is maintainer-answered, the Terms exclude it (an earlier record exists) while the gate counts it — AC 4's "already counted earlier" and the Terms disagree, and the gate implements only AC 4, so the same file is a pass for the gate and a failure per the spec. | GLM | taken — test_earlier_uncounted_record_does_not_spend_the_id | no | agree |
| L1-2 | MAJOR | SPEC | base | `spec.md` AC 7; `scripts/check_interview_minimums.py` `_base`; `.github/workflows/ci.yml` checkout | The branch reading is unreachable in the hosted placement the gate declares: the workflow's `actions/checkout` always leaves a detached HEAD (`rev-parse --abbrev-ref HEAD` returns `HEAD`, never `main`), so hosted runs always take the merge-base path — and on the post-merge push event `origin/main` already equals HEAD, the diff comes out empty and the ADR minimum is silently not measured. That is exactly the "exit 0 after a merge onto main because the base diff came out empty" outcome AC 7 declares refuted; the test covers only a local branch checkout CI never produces, and the pre-merge pull-request run is the only line of defence left. | GLM | taken — test_detached_at_merged_tip_uses_first_parent | no | agree |
| L1-3 | MAJOR | MAINT | base | `scripts/check_interview_minimums.py` `measure` | The five-record ADR duty evaporates when the owning folder is exempt: the cut-off and class `continue`s run before the `adr_touched and name == owner` branch, so a diff that changes `docs/adr/` plus files under a change folder whose spec is dated on or before the cut-off — or that has no `spec.md`, so it never enters `_active_changes` — exits 0 with the ADR edit unmeasured, while the same edit attributed to an archived folder is instead red (owning counts only active folders): same intent, opposite verdicts. | GLM | taken — test_adr_edit_in_a_stock_folder_still_owes_five | no | agree |
| L1-4 | MAJOR | MAINT | base | `scripts/check_interview_minimums.py` `measure`, ADR misattribution branch | A diff touching `docs/adr/` with no `plans/changes/<name>/` path is unconditionally a finding with no route to green: the direct maintainer edit that `provenance.yaml` allows on the human-decided ADR tree, and an ADR-only decision pull request, own no change folder, so there is no `decisions.md` in which the demanded five records could even be written — such work can only merge with a blocking gate red. | GLM | taken — test_adr_outside_any_change_is_a_finding; the finding now names the route: one change folder whose decisions.md carries the five answers | no | disagree — AC 2 intentionally requires one owning change folder with five answers; human-decided provenance grants authorship, not exemption from that gate. |
| L1-5 | MINOR | MAINT | base | `scripts/check_interview_minimums.py` `_base` | On a `main` checkout whose HEAD is not a merge commit — a direct push, a rebase-merge or a fast-forward — the first-parent base reduces the measured diff to the last commit, so `docs/adr/` changes from earlier commits of the same landfall are invisible (silent green) or attributed to the wrong owner. | GLM | rejected — merge-based landfalls are the practice (the branch ruleset, RB-M6); the first parent measures the last landfall; a multi-commit direct push to main is stated as an accepted limit in the pull request | no | agree |
| L1-6 | MINOR | MAINT | base | `scripts/check_interview_minimums.py` `measure`/`main` | `--change <name>` exits 0 and prints "green" when the name matches no active post-cut-off change — a typo in the phase-2 gate invocation, or a spec whose `date` is missing or on the cut-off day, silently passes the spec gate it was written to hold. | GLM | taken — test_change_flag_with_unknown_name_is_found | no | agree |
| L1-7 | MINOR | MAINT | base | `scripts/check_interview_minimums.py` module constants | `SKIP_ALLOWED` is defined and never read — the per-class branches in `measure` encode the same rule inline, leaving a constant that suggests a check that does not exist. | GLM | taken — the unused constant is removed; suite and ruff stand green | no | disagree — The class branches enforce the rule; an unused constant alone demonstrates no correctness fault, missing requirement or ineffective gate. |
| L1-8 | MINOR | MAINT | base | `tests/test_check_interview_minimums.py` | `test_the_gate_goes_red_when_a_feature_skips_its_interview` builds the identical fixture and assertions as `test_feature_with_too_few_answers_is_found` (plus one message substring) — the "mutation evidence" label adds no distinct coverage, only a duplicate that must be maintained twice. | GLM | rejected — the mutation-coverage ratchet (tests/test_ci.py) demands a goes_red named run for every gate; the near-duplicate is that demand's price, named as an accepted limit in the pull request | no | disagree — The additional “2 of 3” assertion detects undercounting that the first test misses; the named test also satisfies the mutation-coverage gate. |

Rounds run: 1

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 313 files, 703 commits, 12 rules.
