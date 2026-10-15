---
title: "Research — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-0ho
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair, red-first]
---

# A guard-test mark for test-only repairs — Research

Phase 1 for bead coding-harness-0ho, seeded by the orchestrating session on
2026-10-15 against `origin/main`.

## The question

The repair verb (`python3 scripts/stage2.py repair <change>`) demands, for
every taken row, a named test that is red on the baseline production code
and green after the repair ("red-first"). On 2026-10-14/15 the right fix
was three times a test or a test helper over production code that was
already right (sol-effort L1-1 and L3-1, haiku-5-5 F-1/F-2): a new test is
then green on the baseline, the runner refuses, and one Codex attempt moved
checker logic into `scripts/stage2.py` only to satisfy the check. The
orchestrating session finished those rows by hand or through an Opus
sub-agent.

The maintainer chose (2026-10-15, answer "A") a "guard test" mark: for a row
marked that way, the test plants the fault itself (for example by swapping
a function or a fixture inside the test) and must be red with the planted
fault and green without it; the runner checks that instead of red on the
baseline. Rejected: a runner-side mutation check, and an exception without
proof. It is to be built before the implementation of coding-harness-agx,
whose contract suite is mostly tests over code that is already right.

## To explore

How the repair verb reads the answer's fixed lines and runs the red-first
proof today (the functions around the "no fixed line" check and the
red-first runs in `scripts/stage2.py`); how the existing "not a test" form
and the status forms (`fixed — <test>`) work; how the existing tests plant
faults ("planted fault" in `tests/`); what a guard-test line would have to
name so the runner can run the test once with and once without the planted
fault, without trusting the model's own word; where the doctrine
(`docs/WORKFLOW.md`, `prompts/04-implement.md`, ADR 0017) describes
red-first and would need the new mark.
