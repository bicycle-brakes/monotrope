---
title: "Decisions — runner-derived-files"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-mfv
owner: Data Architect
provenance: ai-generated
produced_by: {kind: llm-session, name: codex, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [stage-2, runner, derived-files]
---

# Decisions — runner-derived-files

The maintainer requested this repair on 2026-10-08 and then requested Codex
instead of Claude because Claude has little remaining budget. Codex authors
research, spec, plan and implementation for this change. Foreign review calls
still use stage2.py and its leak check. This is a change-local budget exception,
not a persistent model-routing amendment.

[DETAIL] Class bounded: repair an existing internal flow using existing
renderers; no new subsystem or external interface. No ADR or design needed.
[DETAIL] Interview skipped: scope is the requested deterministic repair;
there is no open human intent question. Feature/ADR minimums do not apply.
[DETAIL] Stamp only changed documents held by provenance.yaml, preserving
clean or unheld inputs; set updated, never last_reviewed or approval status.

## Addendum — 2026-10-08, preparation failures use existing repair attempts

The maintainer explicitly confirmed the recommended behavior in the
conversation: use the existing repair attempts, because a generator damaged
by the implementation can thereby be repaired automatically; keep the
existing attempt limits; successful completion requires the generator and
verification to be green. This answers spec-review F-1 and loop row L1-1.
The existing Sonnet fallback remains in the runner; this decision does not
replace it or add attempts. The change's authors still use the separate
Codex budget exception recorded above.

[DETAIL] Reject aliased document/index paths even when their targets are
inside the worktree. Otherwise a changed link could stamp or overwrite an
unrelated clean or unheld target, contradicting criterion 2. Existing path
boundary checks now cover both external and internal link targets.
