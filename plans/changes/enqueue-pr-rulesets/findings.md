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

Stage-2 call, 2026-11-27: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1323 files, 6139 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-27

Spec fingerprint: sha256:193a0690d2aff5f2a0ae9b1804a96a2f5a391c725db99d537c48650dc92a8acb

Spec review commit: 082e38af6672a26f1a752c387299d787627972e9

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-4 | [AMBIGUITY] | SPEC | fix-r1 | spec.md AC5 (lead sentence and *Refuted by:*), Open decisions [DETAIL] S-2 ("`## Phase 6` blocks keep refusing the line"); scripts/enqueue_pr.py `malformed_table_line`, `phase6_problems`, `released_problems` | AC5's lead sentence covers only "a different malformed pipe-bearing line … in a released loop block". The two clauses added in round 1 and the refutation leave out the pipe condition: "a non-JSON `Loop state:` line, or a `Loop state:` line in a `## Phase 6` block is silently accepted". This allows two readings. (a) Only `Loop state:` lines that contain a `\|` are refused. That is how the code already works, because `malformed_table_line` flags only lines containing `\|`, and `phase6_problems` and `released_problems` skip any other line that is not a row. Under (a) nothing is built for Phase 6 blocks, which matches S-2's "keep refusing". (b) Every such line is refused, with or without a pipe. That would add a new refusal to `phase6_problems` and, for non-JSON lines, to `released_problems`, which means changing "other admission prerequisites" (a non-goal). Two cases give different results: a released block containing `Loop state: {not json}` (no pipe), and the last `## Phase 6` block containing `Loop state: {"free": {}}` (valid JSON, no pipe). Reading (a) admits both, and AC5's refutation as written counts that as a failure. Reading (b) refuses both. So a test written from the refutation text fails against a build that follows reading (a). | Opus | in spec — reading a (pipe-bearing lines only, as today) in AC5 and [DETAIL] S-4 (bounded standing grant) | — |

Stage-2 call, 2026-11-27: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1323 files, 6142 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-27

Spec fingerprint: sha256:1137604fb1dedd89f970703137c27e4eb500a5cf65131d33943530f5d63651d2

Spec review commit: f11122f541658802e696487909330f3d4d83fcde

Opus reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding.
