---
title: "Findings — review-diff-4000"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.4
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-diff-4000

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1149 files, 5005 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1152 files, 5006 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | `spec.md` Protected areas ("the paid allowance does not widen what the free stage carries") and criterion 3; `scripts/stage2.py` `_review_round` free branch, `free_probe_prompt`; `research.md` "Where the free diff comes from" | [AMBIGUITY] The free prompt is cut by the same constant this change raises: `_review_round` calls `bounded_review_diff(free_input)`, and `free_probe_prompt` calls `bounded_review_diff(diff)[0]`. `free_diff` itself does not stop at 2,000 lines. Its total check runs only after a whole file (up to 400 lines plus a marker) has been added, and its count misses the newline that joins each file. So it can return about 2,400 lines or more, with no free-total note when the overshoot is on the last file. Today such a diff is cut at 2,000 and the round is recorded as cut, and `docs/WORKFLOW.md` §4b names `REVIEW_DIFF_MAX_LINES` as the free prompt's bound. `research.md`'s claim that a raise "widens only the paid cut" is therefore wrong. Reading A: "its limits" means only `free_diff`'s own constants, and only the one constant changes. Free rounds and free probes then carry up to about 2,400 lines, and a free round that is cut today becomes uncut and can count as clean. That contradicts the protected-area sentence. Reading B: the free prompt keeps its present 2,000-line cap. The free branch and the probe then need a bound of their own (a parameter or a second constant), which edits the code the spec protects and adds behaviour no criterion names. The two readings give different code, different free-round records and different criterion-5 doctrine. | Opus | in spec | — |
| S-2 | MAJOR | SPEC | base | `spec.md` criterion 3 | Criterion 3 cannot go red for the one way this change actually widens the free stage. `free_diff` never reads `REVIEW_DIFF_MAX_LINES`, so "the free diff no longer cuts at either existing bound" stays false at any value of the raised constant. Only an edit to `FREE_DIFF_MAX_LINES` or `FREE_DIFF_MAX_TOTAL` refutes it, and this change has no reason to make one. The input whose outcome does change is not named: a `free_diff` output of 2,001 to about 2,400 lines with no free-total note (overshoot on the last file). Today that is cut at 2,000 and recorded as cut; after the raise it reaches the free prompt whole and uncut. Without that case the criterion neither settles S-1 nor catches a widening under its Reading B. | Opus | in spec | — |
| S-3 | MINOR | SPEC | base | `spec.md` criteria 4–5; `docs/how-it-works.md` "Runner details" diff-lines bullet; `research.md` "What a cut means in the record" | Criterion 5 has the change rewrite the `docs/how-it-works.md` bullet that says the free 400-line per-file cut "is not recorded as a cut round". The runner does record it as one: `_review_round` merges `free_cut` into `cut_note`, which writes the `The diff was cut:` line. `test_a_free_round_over_a_cut_file_is_never_clean` asserts `cut_rounds(record) == [1]` for exactly this per-file cut. `research.md` repeats the wrong claim ("the free diff reports its own cuts as notes, not as cut rounds"), and criterion 4 covers only "the overall review bound". The spec does not say whether the rewritten bullet keeps that sentence. It also does not say whether "misstates a free-review bound" in criterion 5 covers how a bound is recorded or only its number. An implementer following `research.md` keeps the sentence, and the doctrine still contradicts the runner after the change. | Opus | in spec | — |
| S-4 | MINOR | SPEC | base | `spec.md` intro and criteria 1–2 ("paid review"); `docs/WORKFLOW.md` §4b Flash-swarm sentence ("the same bounded diff") | [AMBIGUITY] It is unclear whether "paid review" includes the Flash swarm. The code files the Flash swarm under `state["paid"]` with kind `paid-swarm` and cuts it in the same branch as the ladder. The doctrine separates "the Flash swarm" from "the paid rounds" and "the paid ladder", and says Flash gets "the same bounded diff" as the free round. Reading A: the 4,000 bound covers Flash and the ladder. Only the constant changes, each of the three parallel Flash members reads the doubled diff, and the §4b Flash sentence becomes false and must be rewritten. Reading B: only the ladder gets 4,000 and Flash keeps 2,000, which needs a per-stage bound. Criteria 1–2 tested on a ladder rung pass under both readings. | Opus | in spec | — |
| S-5 | MINOR | SPEC | base | `spec.md` Definition of Done, third bullet; Protected areas, second bullet | The Definition of Done says the pull request's file list shows the protected areas untouched. For the free-review area that check cannot go red: the free filter and its limits (`_free_candidate`, `FREE_DIFF_SKIP_PARTS`, `FREE_DIFF_TEXT_SUFFIXES`, `FREE_DIFF_MAX_*`, `free_diff`) live in `scripts/stage2.py`. That is the file holding `REVIEW_DIFF_MAX_LINES`, so it is in every pull request for this change. A pull request that also edits `_free_candidate` has the same file list as a clean one. No criterion covers the filter, only criterion 3's two numbers. | Opus | in spec | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1152 files, 5049 commits, 12 rules.
