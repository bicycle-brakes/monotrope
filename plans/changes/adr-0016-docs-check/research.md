---
title: "Research — adr-0016-docs-check"
status: draft
implementation_status: done
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-v9xx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-03", model: "Opus 5.5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, adr]
---

# adr-0016-docs-check — Research

Read on `origin/main` on 2026-11-03 (bead `coding-harness-v9xx` — ADR 0016
names the draft's document check).

- `scripts/stage2.py` defines `DOCS_VERIFY = ["bash", "scripts/verify_all.sh",
  "--job", "docs"]`, and `verify_draft` runs it after the derived files, then
  checks the artefacts, the plan card and `## Time used`. The draft runner does
  not run `make verify`.
- The draft-gates-only change (bead `coding-harness-77qj`, 2026-10-31) made
  that switch; `docs/WORKFLOW.md` already names the document check for drafts.
- ADR 0016 still says `make verify` in decision 2 (the runner's guards),
  decision 3 (the one tolerated red gate) and decision 7 (the four checks
  before phase 4). Review-loop row L5-5 of the draft-gates-only change found
  the first of them.
- Implement and repair still run the full `make verify`; nothing about them
  changes.
