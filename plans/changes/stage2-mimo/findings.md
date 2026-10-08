---
title: "Findings — stage2-mimo"
category: findings
status: draft
implementation_status: none
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-mimo

Stage-2 call, 2026-10-07: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 271 files, 610 commits, 12 rules.

## Phase 2a — Codex, 2026-10-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S1 | BLOCKER | SPEC | base | spec.md:46,373,383; research.md:530 | [AMBIGUITY] The compatibility gap requires one live call per model in phase 4, before implementation depends on the address, while the order of work and Definition of Done forbid live calls before merge. One reading performs the probes during implementation and violates the merge restriction; the other postpones them until after merge and leaves the required compatibility check unfinished when the change ships. Stand-ins cannot establish actual endpoint compatibility. | Codex | in spec | — |
| S2 | BLOCKER | SPEC | base | spec.md:291,344,360; decisions.md:286 | [AMBIGUITY] AC25 requires ADR 0007 to be amended when OpenCode Go is declared, but the protected-area rule forbids editing the authoritative ADR and the Definition of Done includes only a draft. One reading completes this PR with the draft, leaving the declaration contrary to the effective ADR; the other requires a separate decision PR to merge first. That dependency and merge order are missing from the delivery contract. | Codex | in spec | — |
| S3 | MAJOR | SPEC | base | spec.md:228,411; decisions.md:342,376 | [AMBIGUITY] For a rejected model ID, AC17 requires stopping without another address, while the current decisions addendum explicitly specifies the OpenAI address as fallback. One reading reports the refusal and makes no second call; the other retries through `/chat/completions`, which AC17 forbids. The spec references that same decision detail without recording that its fallback was superseded. | Codex | in spec | — |
| S4 | MAJOR | SPEC | base | spec.md:150,156 | [AMBIGUITY] Consider two completed rounds with every row decided and no taken row in round 2, then request round 3. AC6 says refusing the third round refutes the criterion; AC7 requires that refusal. One reading permits the third round whenever two rounds have completed, violating AC7; the other permits it only after a taken row, violating AC6's stated test oracle. The same fixture cannot satisfy both. | Codex | in spec | — |

Reviewer session: codex 01a116db-602e-73e2-bbee-d11f961debe4

Stage-2 call, 2026-10-07: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 273 files, 618 commits, 12 rules.

Stage-2 call, 2026-10-08: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 274 files, 626 commits, 12 rules.

Stage-2 call, 2026-10-08: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 274 files, 627 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 296 files, 675 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 296 files, 676 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 296 files, 677 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 309 files, 693 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 309 files, 694 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 309 files, 694 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 309 files, 697 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 309 files, 701 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 309 files, 701 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 309 files, 702 commits, 12 rules.
