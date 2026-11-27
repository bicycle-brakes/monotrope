---
title: "Decisions — bd-trust-check"
category: decisions
status: draft
implementation_status: none
date: 2026-11-27
created: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-5ane.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-27", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, security, hooks, tracker]
---

# Decisions — bd-trust-check

Phase-1a record for `bd-trust-check` (bead `coding-harness-5ane.2`).

## SKIP · interview

status: skipped
reason: "Bounded security fix from the verified PR #437 audit (S-5), run autonomously under the maintainer's bounded standing grant (2026-11-25). The bead (maintainer-written, 2026-11-24) already decides the policy: a repository-local tools/bd runs only for repositories on an explicit trusted list in a harness-neutral location, otherwise the bd on PATH or nothing, and blank lines in the trust file are ignored. Left to the spec as reversible [DETAIL] choices: the list's exact path and line format (preferring one file under XDG_CONFIG_HOME that every harness reads, matched on the origin URL like the existing handover trust file), and whether the Antigravity hook's origin/main-ancestry check (trusted_for_repo_tools) is kept beside it. No architectural choice is open."
