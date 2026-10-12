---
title: "Research — adr-owning-change"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, gates, interview-minimums, adr]
---

# ADR owning change — Research

Phase 1 for bead coding-harness-afa, read against `origin/main` on
2026-10-12. The gate interview-minimums (`scripts/check_interview_minimums.py`)
attributes an ADR under `docs/adr/` to the change folders the same diff
touches and requires exactly one. Change criterion-test-ledger (bead
coding-harness-909, pull request #126, not merged on 2026-10-12) adds ADR 0013
and migrates four other plans; it carries an interim heuristic (a folder the
diff touches through `plan.md` alone is no owner; beside other owners the ADR
text decides) that this change replaces with an explicit statement.

## Questions for the exploration

1. How does the gate find an ADR's owner today on `main`: the code path, the
   base rule, the findings it writes, the tests that pin it.
2. Which places could state the owner explicitly, and what reads them today:
   `decisions/answers/<change>/adr.yaml` (written by `scripts/harness.py
   decide adr`), an ADR frontmatter field, `decisions.md` of the change.
3. Which existing ADRs and answer files would a new rule meet, and which of
   them carry a change name already (for a cut-off or a one-time migration).
4. Which other scripts, gates, kit files and prompts read ADR ownership or
   the answer files (`scripts/check_adr_answers.py`, `scripts/kit/`,
   `prompts/`), so a change knows what it must keep consistent.

The interview (phase 1a) needs the maintainer; this file stops before it.
