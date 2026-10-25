---
title: "Plan — interview-fenced-examples"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-k2r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gate, interview-minimums]
---

# Plan — interview-fenced-examples

```text
For you:     An example interview record inside a code block can no longer stand in for a real answer.
Done when:   Fenced records and skips are not counted, a later real record is (tests red first), and the gate stays green.
Appetite:    0.5 hours of phase 4; stop at the limit.
Not now:     A shared fence helper across gate scripts.
Pre-mortem:  suppose it failed: most likely because an unclosed fence swallowed the rest of a real decisions.md.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_check_interview_minimums.py`: the tests in the ledger.
2. `scripts/check_interview_minimums.py`: `_unfenced`; `_parse_records`
   splits the unfenced text.
3. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_check_interview_minimums.py
python3 scripts/check_interview_minimums.py
```

## Criterion ledger

- 1: tests/test_check_interview_minimums.py::test_a_fenced_record_or_skip_is_not_counted — a fenced block is counted.
- 2: tests/test_check_interview_minimums.py::test_a_record_after_a_closed_fence_still_counts — a real record after a fence is lost.
- 1: tests/test_check_interview_minimums.py::test_the_commonmark_fence_rules_decide_what_is_hidden — a fence rule (closer length, closer kind, closer info string, one-line fence, four-space indent) deviates from CommonMark.
- 1: tests/test_check_interview_minimums.py::test_an_unclosed_fence_before_the_records_hides_them — an unclosed fence leaks the records after it into the count.
- 2: tests/test_check_interview_minimums.py::test_a_crlf_file_with_a_closed_fence_still_counts_the_real_record — a CRLF closing fence never matches and blanks every real record after it.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 12:49:30–12:51:13 UTC, 103 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
