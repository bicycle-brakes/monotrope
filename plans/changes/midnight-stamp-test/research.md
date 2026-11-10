---
title: "Research — midnight-stamp-test"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.5
owner: Data Architect
provenance: human-written
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# midnight stamp test — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-bxxt.5, class bounded, a bug.
`tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current`
takes today's date once and compares it with the stamp the runner writes
later. A full check that crosses local midnight fails on it: on 2026-11-09 at
23:22 UTC (00:22 local time) a full check ended with 1 failed and 5349
passed, on `assert date(2026, 11, 10) == date(2026, 11, 9)`. One lost run
costs about 25 minutes of the one verify slot. Done when the test fixes the
clock it compares against, and a search has shown whether sibling tests take
the date the same way.

Questions for the exploration: how this test and the production code it
exercises read the date (`date.today()`, `datetime.now()`, a helper, a
timezone); which other tests under `tests/` compare a date taken in the test
with a date written by code under test, by file and test name; whether the
repository already has a way to fix the clock in tests (a fixture, a
monkeypatched helper, an environment variable) that such tests should use.
