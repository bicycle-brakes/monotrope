---
title: "Decisions — side-ref-attempts"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-c99h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, attempts]
---

# side-ref-attempts — Decisions

Class: bounded (one counted answer owed). The bead's description fixes the
scope (read 2026-11-03 with `tools/bd show`): one command that saves a
stopped attempt's uncommitted state to `refs/stage2/attempts/<change>/<label>`,
pushes the ref and restores the tracked files, refusing on untracked files it
would lose; the rule in `docs/WORKFLOW.md`; the run plans' rule corrected; and
a retention rule, asked below. This closes the explore's open question on the
scope split.

## Q-1 · When side refs are deleted

asked: 2026-11-03
answer: "nach dem Merge" — after a change merges, the clean-up after merge (bead coding-harness-kpaq) deletes that change's refs under refs/stage2/attempts/<change>/, locally and on origin.
answered_by: maintainer
status: answered
context: |
  Topic: when the side refs of stopped attempts are deleted.
  Intention: the bead names retention as open; the refs grow without bound (11 on origin, measured 2026-11-03 16:05 UTC), and review-loop row L5-1 of bead coding-harness-wkxm found that every red-first proof copies all refs, these included.
  Today: nothing deletes them; they stay after the merge.
  Repository change: Options: delete after the merge through the clean-up after merge (bead coding-harness-kpaq), locally and on origin; keep 14 days after the merge; keep forever.
  Architecture change: none.

In the context of side refs that keep stopped attempts, facing unbounded growth or a retention rule, we decided that a change's attempt refs are deleted after its merge, locally and on origin, to achieve a set that does not grow and proofs that copy fewer refs, accepting that a stopped attempt of a merged change can no longer be inspected. — 2026-11-03
