---
title: "Decisions — frontmatter-current"
status: accepted
implementation_status: none
date: 2026-09-29
last_reviewed: 2026-09-29
updated: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-qd7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# frontmatter-current — Decisions

Phase 1a (interview) was skipped: the maintainer gave the intent and approved
the direction in the session of 2026-09-29, and what remains open is mechanics.

What the maintainer decided on 2026-09-29, in their words where they gave them:

1. "The frontmatter headers in the files must always be maintained and
   current. This must be a basic mechanism." — asked while the English
   translation of `docs/WORKFLOW.md` was in progress.
2. The direction, answered "yes" to a proposal:
   - every Markdown document that carries frontmatter gets a field `updated:`;
   - a CI check fails when `updated:` is older than the last commit that
     changed the file, so a stale header cannot be merged;
   - a command stamps the date, so that upkeep is not a manual step;
   - Coding Harness first, then lakeswitch-ai.
3. Which files carry frontmatter, answered "yes" to a proposal: documents a
   person reads and that age — `docs/` (architecture, governance, how-to,
   research, the workflow), `docs/adr/`, `plans/changes/`, the handovers. Not:
   instruction files (`AGENTS.md`, `README.md`), `prompts/`, `templates/`,
   generated output, harness configuration whose frontmatter is functional
   (`.claude/agents/`, `.agents/skills/`, `.github/`). The list is the
   provenance map's `frontmatter:` field per prefix, not a second list.
4. "Implement as the workflow intends" — the seven phases, with the model
   routing of `docs/WORKFLOW.md` §3.
5. Answer to `[DECISION] 1` of `spec.md` (who confirms the headers on the six
   accepted ADRs), 2026-09-29: "I want the headers, but without a signature."
   That is option 2: the implementing session commits the six headers like
   any other file, and the maintainer's review of the pull request is the
   confirmation. The maintainer decided this knowingly: a header-only edit to
   an accepted ADR needs no signed commit. It does not settle whether this
   repository adopts the signed-decision rule for the content of ADRs; that
   question stays open.
