---
title: "Findings — runner-preflight-gates"
category: findings
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-preflight-gates

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1185 files, 5522 commits, 12 rules.

Stage-2 call, 2026-11-23: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1188 files, 5526 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-23

Spec fingerprint: sha256:ac6b2318050d927110718707454861a64fbeaa526c4ebffbfa445d96c5a13df6

Spec review commit: e8e79326f4c556afaedde377de95f88b89885d3e

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 2; Problem; header | The header and Problem say the waste to prevent is "a fault the attempt cannot fix", but AC 2 stops the run on any blocking document-gate failure. Reading A: any red blocking document gate refuses, including a document fault inside the change folder that the verb itself would rewrite (a stale `updated:` on this change's `spec.md` or `findings.md`, a `plan.md` line `criterion-ledger` rejects, a `research-handoff` neighbours header mismatch), so a second draft round cannot start until the operator hand-edits the files the draft exists to write; the only tolerance stated is the ADR answer. Reading B: only faults outside the verb's writable scope refuse, which requires a per-verb writable-scope rule the spec never states. Both readings satisfy the stated refutation (a fake model records no call), so the criteria and the planned regressions are identical while operator behaviour for every refusal inside `plans/changes/<change>/` differs. | deepseek-v4.1-flash | open | — |
| S-2 | MINOR | SPEC | base | spec.md AC 1 | Cannot go red as written: "non-admitted" selects nothing out. Every gate carrying `subsets: [docs]` is declared `cost: seconds` and none sets `needs_admission`, so `ci_gates.declared_cheap` is true and `gate["admission"]` is false for all of them (`decisions/gates.yaml`; `scripts/ci_gates.py:489-501`), which makes a preflight that also selects admitted gates run exactly the same set. No input the repository presents distinguishes the two, so the qualifier is a statement of intent until a document gate is declared admitted or exempted from the seconds class. The second half of the same criterion's refutation, "uses a separate hand-maintained gate list", is likewise a property of the source and not of any run. | deepseek-v4.1-flash | open | — |
