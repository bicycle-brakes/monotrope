---
title: "Plan — review-row-closing-pipe"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-2i9j
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop, parser]
---

# Plan — review-row-closing-pipe

```text
For you:     A finding line that only lacks its closing | is read, and an answer the runner cannot read is kept with its first bad line named.
Done when:   The open-row rule, the named line and both places that keep an answer have tests that were red first, and make verify is green.
Appetite:    1.5 hours of phase 4, repairs included; stop at the limit.
Not now:     Retrying a malformed answer (coding-harness-70rw); a malformed row beside a valid one (coding-harness-vque).
Pre-mortem:  suppose it failed: most likely because a kept answer's table lines were read back as rows of the record.
Starts unless you say stop.
```

## Files and steps

1. Change `tests/test_stage2.py`: add the tests named in the ledger.
2. Change `scripts/stage2.py`:
   - `parse_rows`: read an open row (spec, Terms).
   - `UnreadableAnswer(CallFailed)` carries the scrubbed answer and its
     first non-blank line; `run_swarm` raises it for an unreadable answer,
     keeping the message prefix "malformed finding output: expected six-cell
     findings or exactly 'No finding.'" and adding "; first unrecognised
     line: …". `MalformedTable` becomes its subtype.
   - `review_loop`: quote each unreadable answer after the round's
     statements; before a refusal, append one
     `## Rejected review-loop answer — <member>, <date>` block per
     unreadable answer to `findings.md`.
3. Update this plan's ledger and time, `findings.md`, and `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'open_row or unreadable_answer or five_open_lines'
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_parse_rows_reads_an_open_row — an open row stays text or its cells differ from the closed line.
- 2: tests/test_stage2.py::test_parse_rows_keeps_other_open_lines_as_text — a short, long, severity-less or pipe-less line is read as a row.
- 3: tests/test_stage2.py::test_five_open_lines_complete_the_round — a member fails, the attempt refuses, or rows are missing.
- 4: tests/test_stage2.py::test_unreadable_answer_names_its_first_line — the message lacks the line or carries a credential.
- 5: tests/test_stage2.py::test_unreadable_answer_is_quoted_in_the_round — the failure line stands without the quoted answer, or a quoted table line becomes a row.
- 6: tests/test_stage2.py::test_unreadable_answer_of_a_refused_attempt_is_kept_in_findings — an answer is lost, a quoted line becomes a row, or a record is written.

## Route

Spec, plan, implementation and self-review by the orchestrating Claude Code
session in a cloud container on 2026-10-25, at the maintainer's instruction
(conversation 2026-10-25): Codex, GLM and OpenCode Go are unreachable there.
The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 11:27:09–11:30:33 UTC, 204 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
