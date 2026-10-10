---
title: "Plan — interview-minimums"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-6yg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: cline, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, interview, gates, workflow]
---

# Plan — `interview-minimums`

```text
For you:     The interview becomes mandatory where you set the minimums —
             features ≥ 3, ADR changes ≥ 5 (feature with ADR: 5 in total),
             spike the three topics or a reasoned skip, bounded one record or
             a reasoned skip — and a gate counts it at the spec gate and in
             verify.
Done when:   make verify green with the new interview-minimums gate and the
             counterexample tests; prompts, docs and regenerated CI say the
             same thing.
Appetite:    6
Not now:     scripts/validate_change_artefacts.py (bead coding-harness-jc3),
             changes in lakeswitch-ai or portfolio-agentic-engineering, a
             decisions.md template, any change to adr-answers or decide adr.
Pre-mortem:  suppose it failed: most likely because the question-record
             format still parses real decisions.md files wrong.
Starts unless you say stop.
```

## Steps

1. **`scripts/check_interview_minimums.py` (new).** The gate, modelled on
   `check_adr_answers.py` (exit 0 findings-free, 1 findings, 3 unmeasurable).
   It reads every active change's spec frontmatter for `class:` and `date`,
   skips changes whose `date` is not later than `CUTOFF = date(2026, 10, 8)`,
   and parses `decisions.md` for interview records (`## Q-<n> ·` with the
   field lines), skip records (`## SKIP · interview` with `status: skipped`
   and a `reason:`) and their counts per the Terms of `spec.md`. The diff
   comes from the `change_diff` states: `git diff --name-only <base>` plus
   untracked `ls-files --others`; the base is `HEAD^` on a genuine `main`
   checkout, else `merge-base(HEAD, origin/main)`; without a base it exits 3.
   ADR attribution per the owning change.
2. **`tests/test_check_interview_minimums.py` (new).** The counterexample
   matrix of the spec (AC 1–8, 10): too few answers, agent answers, open
   records, duplicate ids, feature with ADR at three and five, bounded skip
   present and absent, spike forms, staged/unstaged/untracked ADR paths,
   owning-change attribution, base rule per context (work branch, main,
   unmeasurable), cut-off boundary, gates.yaml declaration test, and the
   doc-consistency assertions of AC 9 and 11. Fixtures build throwaway trees
   (`--root`), as `tests/test_check_adr_answers.py` does.
3. **`prompts/01a-interview.md`.** The optionality paragraph is replaced by
   the class-conditional duty with the minimums, and "What you write" gains
   the machine-readable record form (interview record, skip record) that the
   gate parses — one home, no template.
4. **`prompts/02-spec.md`.** The gate line names the interview check for this
   change before the spec passes; the rest of the prompt stands.
5. **`docs/WORKFLOW.md`.** Row 1a of the phase table and the paragraph after
   it state the duty and the minimums; the "Change classes…" section gains
   the per-class interview duties; the stage-1 table's enforcement row gains
   the new gate; the cut-off sentence with its date.
6. **`AGENTS.md`.** Row 1a of the workflow table — mandatory by class, the
   minimums, the skip forms.
7. **`decisions/gates.yaml` + `.github/workflows/ci.yml`.** The gate entry
   after `adr-answers` (verify, block, both), then
   `python3 scripts/ci_gates.py --generate-ci`.

## Verification

```bash
python3 scripts/check_interview_minimums.py   # the new gate on this tree
make verify                                    # every gate, CI included
```

## Per acceptance criterion, the test that holds it

| AC | Test (in `tests/test_check_interview_minimums.py` unless said) | Red when |
|---|---|---|
| 1 | `feature_with_too_few_answers_is_found` | the checker exits 0 below three counted records |
| 2 | `adr_change_demands_five_regardless_of_class`, `adr_outside_any_change_is_a_finding`, per-state: `staged_/unstaged_/untracked_adr_path_is_seen` | a staged-only or untracked ADR path is missed |
| 3 | `feature_with_adr_needs_five_not_eight` | the checker sums the minimums |
| 4 | `agent_open_and_duplicate_records_do_not_count` | agent answers or repeats count |
| 5 | `bounded_with_one_record_or_skip_passes`, `bounded_empty_file_is_found`, `spike_three_topics_or_skip` | an empty bounded file passes |
| 6 | `unmeasurable_tree_exits_three` | exit 0 without a base |
| 7 | `main_checkout_uses_first_parent`, `worktree_branch_uses_merge_base` | a post-merge run measures nothing |
| 8 | `cutoff_excludes_same_day_and_older` | a same-day change turns red |
| 9 | `spec_prompt_names_the_interview_check` (doc assertions) | the prompt's gate line omits the check |
| 10 | `gates_yaml_declares_interview_minimums` + `ci_gates.py --check-ci` in `make verify` | the entry is deleted and the test stays green |
| 11 | `workflow_and_agents_state_the_duty` (doc assertions) | docs still call 1a optional without limits |

## What is not touched

`scripts/check_adr_answers.py`, `scripts/harness.py`, `scripts/stage2.py`
(read as a pattern, not modified), `.claude/` hooks and agents, `tools/`,
`docs/adr/`, other sessions' worktrees, the tracker beyond the claimed bead.

## Explore fallback

None carried: research was authored by the directing session (reason recorded
in `research.md`); stage 2 stays reserved for the reviews.