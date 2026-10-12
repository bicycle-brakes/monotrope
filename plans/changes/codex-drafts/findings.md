---
title: "Findings — codex-drafts"
category: findings
status: draft
implementation_status: none
date: 2026-10-12
created: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-rhq
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — codex-drafts

Stage-2 call, 2026-10-12: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 376 files, 932 commits, 12 rules.

## Phase 2a — Codex, 2026-10-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`, criteria 13 and 16 | [AMBIGUITY] A draft has only the missing-answer `adr-answers` gate failure, but its plan lacks `## Time used`. Reading criterion 13 as passing all post-run checks produces a commit; reading it as waiving only the verification failure leaves criterion 16 failing and triggers another attempt. The precedence is unspecified. | Codex | fixed in `873d2af` — not a test — criterion 13 now waives only the red `make verify`; criteria 14 to 16 still apply, and its refutation names a `plan.md` without `## Time used` | — |
| F-2 | BLOCKER | SPEC | base | `spec.md`, criteria 28, 31 and 34 | [AMBIGUITY] Input: an old `Reviewer session: codex <id>` line followed by a new Opus phase-2a block. Criterion 31 requires resuming that Codex session; criterion 34 requires a fresh session where Opus performed phase 2a. Selecting the recorded line resumes the earlier context; selecting the latest review starts fresh. The controlling rule is unspecified. | Codex | fixed in `873d2af` — not a test — criteria 30 and 31 key on the last `## Phase 2a` block: resume only when it is Codex's with its session line, fresh after an Opus block; plan's DETAIL follows | — |
| F-3 | MAJOR | SPEC | base | `spec.md`, criteria 8, 10 and 33 | The mandatory second draft starts with the first draft's committed ADR in its baseline. Criterion 8 therefore restores edits to that ADR, while criterion 10 permits another new ADR because the first no longer counts as new. When review findings require corresponding ADR changes, the spec provides no repair contract: retaining the original leaves stale content, while creating a replacement leaves two records for the change. | Codex | fixed in `873d2af` — not a test — a new ADR file is counted against the merge base of the baseline and `origin/main`, so a second draft edits the first draft's ADR and criterion 10 still counts one | — |

Reviewer session: codex 01a130f4-7a06-7710-82b0-acf5a60d9dd1
