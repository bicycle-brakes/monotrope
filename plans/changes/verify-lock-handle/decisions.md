---
title: "Decisions — verify-lock-handle"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-42em
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify-lock]
---

# Decisions — verify-lock-handle

Phase-1a record for `verify-lock-handle` (bead `coding-harness-42em`).

## SKIP · interview

status: skipped
reason: "Bounded refactor the maintainer chose on 2026-11-11 as the lasting fix after verify-slots (bead coding-harness-u1ha), run autonomously under the bounded standing grant (2026-11-25): hold_admission returns an admission object carrying its lock, slot index and token; callers that spawn children pass it explicitly (inherit_fds(admission), inherit_env(admission)); temporary files are named per admission, as the bead states. No product or architectural choice is open."
