---
title: "Decisions — model-endpoints-refresh"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-363r.5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, model-endpoints]
---

# Decisions — model-endpoints-refresh

Phase-1a record for `model-endpoints-refresh` (bead `coding-harness-363r.5`).

## SKIP · interview

status: skipped
reason: "Bounded data refresh the maintainer set in the bead (2026-11-25, session 9200c6b1), run autonomously under the bounded standing grant (2026-11-25): remove the deprecated mimo-v2.5 and mimo-v2.5-pro from admitted lists and seats in model-endpoints.yaml with the 410 measurement as reason, re-measure every stale skip record through the runner (prepare-loop) and update or remove it from the measurement. Every record changes only on a dated runner measurement; no model is admitted without one. No product or architectural choice is open; enabling model access in the OpenCode console is the maintainer's and stays outside the change."
