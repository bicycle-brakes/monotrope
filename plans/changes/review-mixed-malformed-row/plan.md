---
title: "Plan — review-mixed-malformed-row"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-vque
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — review-mixed-malformed-row

```text
For you:     A broken finding line next to a good one stops the round instead of vanishing undecided.
Done when:   Both criteria have tests that were red first (criterion 2 as a guard) and make verify is green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     Carrying unreadable lines as undecided rows.
Pre-mortem:  suppose it failed: most likely because a summary table beside real rows refuses paid rounds.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the two tests named in the ledger.
2. `scripts/stage2.py`: `finding_shaped(line)`; in `run_swarm`, raise
   `MalformedTable` with the finding-shaped non-row lines when readable
   rows exist beside them.
3. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'malformed_finding_row_beside or summary_table_beside'
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_malformed_finding_row_beside_a_valid_one_refuses_the_round — the round stands or the refusal omits the member or line.
- 2: tests/test_stage2.py::test_a_summary_table_beside_valid_rows_keeps_the_round — a summary table refuses the round.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 11:47:30–11:51:08 UTC, 218 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
