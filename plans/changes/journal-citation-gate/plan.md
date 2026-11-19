---
title: "Plan — journal-citation-gate"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-x9ed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, provenance]
---

# Plan — journal-citation-gate

```text
For you:     The journal-date check accepts patterns and runner records while still catching undated citations.
Done when:   Focused tests cover both exemptions and real undated citations, and make verify passes.
Appetite:    2 hours for phase 4, including repairs; stop at the limit.
Not now:     A new gate, runner changes, non-Markdown scans, and journal immutability.
Pre-mortem:  suppose it failed: most likely because an exemption hides nearby hand-written citations.
Starts unless you say stop.
```

## Implementation

1. In `tests/test_provenance.py`, retain tracked Markdown scanning and the existing date, empty-target and placeholder rules; exempt targets containing `*` and complete fenced research-swarm/v2 records within complete matching run envelopes. Recognize the runner's actual run markers and record fences; leave malformed, unclosed or standalone records scannable, and preserve prose outside records, including between multiple records and runs.
2. In the same file add focused tests exercising the existing detection helper and the tracked-file test's path through it, including real runner-shaped records, multiple records, adjacent prose, malformed markers and a mutation of a dated hand-written citation. Keep the existing enforcer and its mutation proof.
3. Do not touch `decisions/gates.yaml`, `docs/governance/regelwerk.md`, runner code, journal records, or unrelated provenance checks; no held path needs an orchestrator bootstrap edit.

Verification:

```sh
make verify
```

## Criterion ledger

- 1: not yet written tests/test_provenance.py::test_patterns_are_not_journal_citations — a wildcard target is reported.
- 2: not yet written tests/test_provenance.py::test_runner_records_are_not_journal_citations — an undated path inside a complete runner record is reported.
- 3: not yet written tests/test_provenance.py::test_undated_citations_outside_runner_records_are_reported — an undated path beside a record passes, including through the tracked-file check.
- 4: tests/test_provenance.py::test_the_date_check_goes_red_when_a_citation_loses_its_date — a dated target, directory mention or placeholder is reported.
- 5: not yet written tests/test_provenance.py::test_incomplete_or_standalone_runner_records_remain_scannable — an undated path in a malformed record is hidden.

## Time used

2026-11-19 17:13:02–17:14:16 UTC, 74 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
