---
title: "Findings — loop-until-clean"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — loop-until-clean

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1153 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1
>
> The runner put back:
> - `docs/adr/0018-review-swarms-until-clean.md`
> - `plans/changes/loop-until-clean/decisions.md`
> - `plans/changes/loop-until-clean/design.md`
> - `plans/changes/loop-until-clean/plan.md`
> - `plans/changes/loop-until-clean/research.md`
> - `plans/changes/loop-until-clean/spec.md`

Stage-2 call, 2026-10-14: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 420 files, 1154 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1

Stage-2 call, 2026-10-14: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 420 files, 1154 commits, 12 rules.

ADR answer owed: decisions/answers/loop-until-clean/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).
