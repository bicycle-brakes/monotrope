---
title: "Research — cheap-checks-admission"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.13
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# cheap checks admission — Research

## Topic (bead coding-harness-bxxt.13, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: scripts/stage2.py:6578 PYTEST uses -n auto; cheap_checks (8529) runs it
at 8599-8606, both callers outside the admission (9252-9275 strip the lock
env; 9440-9443 'without an admission'); the worker cap targeted_pytest_env
(8996-9034) applies only at 9163. When a touched path appears or vanishes
(8955) the targeted run selects leerprobe (8968; ~200 s) through run_gates,
documented as outside the admission (9038). On an 8 GB machine this bypasses
the two-slot limit and the memory floor. What: cap cheap-check workers like
targeted runs, and run leerprobe in targeted runs under the admission.
Related: coding-harness-9bv1 (ENV_ALLOW drops
PYTEST_XDIST_AUTO_NUM_WORKERS), coding-harness-bxxt.11.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
