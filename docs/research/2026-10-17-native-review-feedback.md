---
title: "Native review feedback evidence loop"
category: research
created: 2026-10-17
updated: 2026-10-17
last_reviewed: 2026-10-17
status: draft
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Codex, version: "2026-10-17"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-0kw
tags: [research, review, feedback]
---

# Native review feedback evidence loop

Read-only Sol subagent research on 2026-10-17 at `6477d04`. Proposed, not
implemented: a native on-demand collector and source-linked recurrence report.
Hermes is unnecessary for this first slice; ADR 0010 still governs its accepted,
parked recurring research job and requires another decision for a new job.

Collect selected PR reviews, inline/discussion comments, commits and CI, plus
committed artifacts and released findings. Reuse `stage2_runs.py` parsing where
suitable. Preserve verdict-before-release isolation. Join finding identity,
disposition/reason, repair commit, baseline-red regression evidence and later
fresh-session verdict. CI success alone does not prove a particular repair.

Keep source IDs/URLs, observed/source times, commit, revision hash and evidence
completeness. Explicit IDs establish links; path/text/time similarity produces
candidates only. Missing commits, unread evidence and ambiguous links remain
gaps. Replay must be idempotent; interrupted pagination must not advance the
checkpoint prematurely. Bind CI to the actual repair SHA.

Only explicitly authorized chat excerpts or repository artifacts are inputs.
Do not assume private ChatGPT/Claude chat access or ingest home-directory
transcripts. Treat PR/chat text as untrusted data, never shell instructions.
The report proposes runner/skill improvements with examples, counterexamples
and regression checks; it makes no silent code or doctrine change.

Start on demand. Daily incremental collection and weekly synthesis are later
proposals. Scheduled Actions can be delayed/dropped; a future webhook still
needs polling reconciliation. Unattended scheduling is a separate architectural
decision, not an implication of this research.

First-slice acceptance: a selected accepted/rejected/repaired/rediscovered
corpus; duplicate/edited replay; pagination interruption; stale CI SHA and
missing commits; explicit versus inferred links; one source-linked recurrence
report. No model, tracker or repository writes by the collector.

## Primary sources

- [GitHub reviews](https://docs.github.com/en/rest/pulls/reviews) and
  [inline comments](https://docs.github.com/en/rest/pulls/comments): identities,
  review state, timestamps and commit references support attribution.
- [Check runs](https://docs.github.com/en/rest/checks/runs): revision-bound CI.
- [Workflow schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule): timing limitations.
- [Script injection](https://docs.github.com/en/actions/concepts/security/script-injections): untrusted PR text.
- [Hermes scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/): an execution mechanism, not the missing evidence joins.

Related work: Hermes groundwork (coding-harness-i3y), tracker-currency audit
(coding-harness-i3y.1), known-finding reviewer comparison (coding-harness-km1),
malformed row identities (coding-harness-6jg). New feature task created after
research: coding-harness-0kw. No duplicate feedback task was found.

Limits: targeted doctrine/code/tracker and six official sources read; private
chats, credentials, unreleased loop records and PR #157/#158 diffs not read.
No implementation or tests. Interview still needs authorized chat sources,
retention, recurrence threshold, report location/cadence and publishing boundary.
