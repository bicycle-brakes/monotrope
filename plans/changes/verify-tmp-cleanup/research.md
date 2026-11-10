---
title: "Research — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: Data Architect
provenance: human-written
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# verify tmp cleanup — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-bxxt.3, class bounded. On 2026-11-09 about 21:40 UTC the
data volume ran full (1.0 GiB free); a test run ended with "No space left on
device" and 239 errors. Two finished runs had left 1.3 and 1.5 GiB under the
pytest temporary root. Wanted: each run of the full check uses a base
temporary folder of its own and removes it when it ends, green or red, also
after an interrupt; a red run may keep it only on request. Related: the
free-disk check at admission (bead coding-harness-87b0).

Questions for the exploration: where the test gate gets its temporary root
today (`decisions/gates.yaml`, `scripts/verify_all.sh`, pytest configuration)
and whether a base folder can be set without editing the held gate list; how
the runner's own targeted and cheap test runs get theirs; what cleans up
after a killed run, given that the verify lock already supervises process
groups (`scripts/verify_lock.py`); which tests would misread a removed
folder.
