---
title: "Research — runner-derived-files"
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

# Research — runner-derived-files

Read on 2026-10-08 at origin/main 8f097a3. `implement` writes its audit
into findings.md, then `verify_attempt` immediately launches make verify.
The registry checks its generated index byte-for-byte. The frontmatter gate
requires modified held documents to carry a current updated date. File-only
workers cannot run either renderer (coding-harness-mfv).

Existing mechanisms: `check_frontmatter_current.is_held` applies provenance
prefixes and exclusions; `stamp` edits only updated and refuses duplicate
headers or invalid UTF-8. `scripts/plans_registry.py --index` renders the index.
Use these instead of a second renderer. Only changed held documents may be
stamped; clean documents and unheld files must remain untouched. Regeneration
belongs to implement postchecks, not the read-only make verify command.
The same helper may later serve review-loop; that integration is outside this
bounded repair and needs its own acceptance evidence.
