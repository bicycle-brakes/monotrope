---
title: "Research — verify-lock-handle"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-42em
owner: Data Architect
provenance: human-written
tags: [research]
---

# verify lock handle — Research

## Topic (bead coding-harness-42em)

Class: bounded.

Why: scripts/verify_lock.py keeps the running admission in module-global state (_ACTIVE, _ACTIVE_ADMISSIONS); inherit_fds, inherit_env and the slot marker read only the latest admission, and the temporary publish file is named by pid only. Review round 3 of verify-slots (bead coding-harness-u1ha) found the third fault of this one design where two admissions overlap in one process. On 2026-11-11 the maintainer chose a Boundary for verify-slots (a second admission in one process is refused) and this bead for the lasting fix.

What: hold_admission returns an admission object carrying its lock, slot index and token; callers that spawn children pass it explicitly (inherit_fds(admission), inherit_env(admission); today the one caller is scripts/stage2.py); temporary files are named by the admission token, not the pid; the verify-slots Boundary is lifted. Contract test: two admissions in one process share nothing (descriptors, environment marker, holder file).

Fits the maintainer's long-term Rust direction: an admission is a value with an owner.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
