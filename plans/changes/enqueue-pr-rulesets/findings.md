---
title: "Findings — enqueue-pr-rulesets"
category: findings
status: draft
implementation_status: none
date: 2026-11-27
created: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-3wtk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — enqueue-pr-rulesets

Stage-2 call, 2026-11-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1320 files, 6136 commits, 12 rules.

Stage-2 call, 2026-11-27: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1323 files, 6138 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-27

Spec fingerprint: sha256:f45acc5a4eb30addfdc3e7c140b73147d64b173d5b59b6fcc50124486bc4ccfa

Spec review commit: 48c6883400f3f62063b5c12bfaff13c21632ecb9

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md AC4, AC5 and Open decisions [DETAIL]; decisions.md SKIP reason ("scripts/stage2.py STATE_KEY") | It is unclear what makes a line "the runner's `Loop state: {…}` line", and there are two readings. (a) Any line that matches the anchored shape of `scripts/stage2.py` `STATE_LINE` (`^Loop state: (\{.*\})[ \t]*$`) is exempt. Then `Loop state: {not json \| x}` and `Loop state: {} \| L1-1 \| MAJOR \| … \| open \| {}` both pass, and no brace-wrapped line can refute AC5. (b) Only a line whose contents parse as the JSON object the runner writes (`json.dumps`, possibly also the `free`/`paid`/`consumed` shape that `read_state` checks) is exempt. Then those same lines are refused under AC5. decisions.md names `STATE_KEY`, which is the bare prefix that the [DETAIL] says is not enough, so the two documents also disagree. The spec is also silent on two cases: a second state line in one released block, and a state line somewhere other than where the runner writes it (after the table, before `Kept from the loop record:`). Readings (a) and (b) lead to different expected outcomes in the AC4 and AC5 tests. | Opus | in spec — reading b (rest must parse as a JSON object) recorded in AC4, AC5 and [DETAIL] S-1..S-3 (bounded standing grant) | — |
| S-2 | MINOR | SPEC | base | spec.md AC4, AC5 and Protected areas; scripts/enqueue_pr.py `malformed_table_line`, `phase6_problems`, `released_problems` | The spec does not say where the exemption lives. `phase6_problems` and `released_problems` share the helper `malformed_table_line`. If the exemption goes into that helper, `## Phase 6` blocks also stop refusing a pipe-bearing `Loop state:` line, although the runner never writes one there. If it goes only into `released_problems`, Phase 6 blocks keep refusing it. No criterion covers the Phase 6 block, so both versions pass AC4 and AC5, and whoever builds it makes the choice without anyone deciding it. | Opus | in spec — exemption only in released_problems; Phase 6 blocks keep refusing, recorded in AC5 and [DETAIL] S-1..S-3 | — |
| S-3 | MINOR | SPEC | base | spec.md Protected areas and Open decisions; research.md "What is unclear" item 5; scripts/enqueue_pr.py docstring (the `script` self-check does not compare imported modules) | The spec does not settle a question the research left open: does the admission reader import `STATE_LINE`/`STATE_KEY` from `scripts/stage2.py`, or keep its own copy of the pattern? If it imports them, what the admission exempts depends on a module the `script` condition does not compare, and on the runner code this change declares protected. If it keeps a copy, the copy can drift from the runner's writer. Nothing in the spec decides this, so whoever implements it will choose silently. | Opus | in spec — own copy of the prefix, pinned to stage2.STATE_KEY by a test; recorded in [DETAIL] S-1..S-3 | — |
