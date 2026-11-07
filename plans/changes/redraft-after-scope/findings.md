---
title: "Findings — redraft-after-scope"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-y0qm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — redraft-after-scope

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3375 commits, 12 rules.

Stage-2 call, 2026-11-06: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason spike: on 2026-11-06 Flash implement was accepted with an empty diff on both spikes tried (beads bvy and xay1; bug coding-harness-te7q), so this spike goes to Sonnet first · leak check clean over 913 files, 3382 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 916 files, 3461 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 916 files, 3466 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 916 files, 3467 commits, 12 rules.

## Phase 6 — Opus 5.5, 2026-11-07

Read-only Opus 5.5 sub-agent (a spike's review per docs/WORKFLOW.md, "Which change gets what"), at b41b86d9; its answer is recorded unchanged.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MINOR | SPEC | base | docs/research/2026-11-06-redraft-after-scope.md:77–78 (Case 2 lesson), :162 (replay row 2), :167–168 (reading the table) | The report credits remedy A ("redraft after a scope-changing answer") as **Demonstrated** four times in research-swarm. One of those four is a phase-2a incorporation. The report's own procedure (:186–188) says a phase-2a incorporation is not a scope change and so not a redraft. The evidence section names only three answer-triggered appendices: 2026-10-15 for Q-7–Q-9, 2026-10-16 for Q-10, and 2026-10-18 for Q-12/Q-13 (research-swarm/research.md:135, :214, :409). The fourth is the 2026-10-17 set of rulings S-21–S-30, which the source describes as incorporated "without supplying a new human answer" (research-swarm/research.md:375–378). research-swarm/plan.md has four separate "Draft handoff — 2026-10-17, second … fifth phase-2a incorporation" sections (:1116, :1176, :1246, :1301), plus one dated 2026-10-16 "after phase 2a" (:1394), so the count "four" matches neither reading. The report already marks case 1 as "Outside A's trigger" for the same kind of reason; case 2 should get the same treatment: three answer-triggered redrafts that demonstrate A, plus phase-2a incorporations that fall outside A's trigger. The recommendation survives, because cases 2–4 still contain answer-triggered redrafts, but the replay table and the procedure contradict each other on what counts. [Acceptance criteria 2 and 3] | Opus | open | — |
| F6-2 | MINOR | MAINT | fix-r1 | docs/research/2026-11-06-redraft-after-scope.md:11 (frontmatter `produced_by`) | The report's provenance still says `claude-code, "Sonnet 5.5, 2026-11-06"` as its only producer. Repair commit f24ffd12 (2026-11-07, stage2-runner, gpt-6.1-sol) rewrote 141 lines of this file: the case 5 evidence, the `check_research_handoff.py` correction, and the replay and recommendation text. The change's own research.md:13 was updated to name the "gpt-6.1-sol repair, 2026-11-07"; the report was not. A reader who checks who wrote the case 5 and handoff-linkage claims is pointed only at the first attempt, which, by its own account (research.md:88–95), could not read that evidence. `produced_by` should name the repair model as well. | Opus | open | — |

Phase 6 verdict: Claude Opus 5.5, 2026-11-07

Checked (no further findings): every cited line and anchor resolves at b41b86d9; case 5 matches `git show 24371185` and `git show b04c119d`; `_bases` and `_parity` exist in scripts/check_research_handoff.py; "redraft" appears nowhere in prompts/, scripts/, templates/, docs/WORKFLOW.md or AGENTS.md; the procedure's anchors exist; criterion 4 and criterion 5 hold; no guard tests to assess.
