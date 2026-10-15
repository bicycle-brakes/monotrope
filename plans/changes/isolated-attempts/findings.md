---
title: "Findings — isolated-attempts"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — isolated-attempts

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1141 commits, 12 rules.

Stage-2 call, 2026-10-15: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 424 files, 1198 commits, 12 rules.

## Written stop — 2026-10-15

The phase-4 implement run (route flash, GLM 5.3 Flash) started at 06:31 and
the worker finished writing at about 10:20; the runner's post-run
`make verify` then hung in `pytest tests/ -q` for more than three hours
(measured 13:30: elapsed 03:08:51, normal about nine minutes). The
orchestrating session stopped the run at the maintainer's request and
committed the worker's partial state unchanged as work in progress. Nothing
in this commit is verified: `make verify` never finished, and which test
hangs was not yet measured (candidates by name: the live tests in
`tests/test_stage2_isolation.py`, which may start Podman; the Podman machine
was running). Next: run the new test files one by one with a per-test time
limit to find the hang, then decide whether the change continues after
coding-harness-agx and coding-harness-icw.
