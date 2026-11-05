---
title: "Decisions — raising-fault-test"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-xrzf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, repair, red-first]
---

# raising-fault-test — Decisions

Class: bounded (bead coding-harness-xrzf, read 2026-11-03 with `tools/bd show`).

## SKIP · interview

status: skipped
reason: The maintainer decided the intent in the 15:00 block on 2026-11-03 (question 18 of the block, through the interview tool): the runner's red-first rule stays — only an assertion or pytest's own failed outcome counts as red — and one sentence in the repair and implement prompts tells the model that when the fault itself raises, the regression test catches it and fails with assert or pytest.fail; plus a prompt test. Evidence for it: on 2026-11-03 both Codex and Sonnet failed the lane D repair (bead coding-harness-v6vk, F6-1) because the fault raised ValueError on the baseline. The phase-1 explore could not read the bead and mapped three possible targets; the bead's description names this one. Nothing is left for the maintainer to answer.

## Decided by the agent

[DETAIL] **Where the sentence goes:** `prompts/04-implement.md` (the implement and repair doctrine) and the runner's repair prompt text, wherever it states the red-first rule. Reason: both models read the rule there before writing their test.

[DETAIL] **The runner's rule does not change.** Reason: the maintainer's answer; a crash, a skip or a setup error stays "could not run", never red.
