---
title: "Plan — plan-held-paths"
status: draft
implementation_status: partial
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-h5tj
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, planning]
---

# Plan — plan-held-paths

```text
For you:     Plans assign protected edits to the orchestrator before an attempt is refused for them.
Done when:   The list-drift test is red first and green after, the routing instruction is reviewed, and make verify is green.
Appetite:    1 hour of phase 4, including repairs; stop at the limit.
Not now:     Changes to the runner, provenance policy or gates.
Pre-mortem:  suppose it failed: most likely because the prompt's copied list drifted from the runner.
Starts unless you say stop.
```

## Files and steps

The orchestrator implements both edits by hand; do not launch stage-2 implement
or repair for this change, since its prompt edit is itself held and the test
alone cannot pass. No `templates/plan.md` exists: the plan prompt is the template.

1. `tests/test_stage2.py`: add top-level `test_the_plan_prompt_names_every_runner_held_path`, reading the real plan prompt and checking every `stage2.RUNNER_HELD` entry as a complete backticked path; prove the coverage check rejects a planted additional entry absent from the prompt, and run it red before editing the prompt.
2. `prompts/03-plan.md`: add a Required item naming `provenance.yaml`, `decisions/gates.yaml`, `model-endpoints.yaml`, `.claude/`, `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`, `templates/`, `.github/`, `.beads/`, `AGENTS.md`, `README.md`; add the committed-map rule (allowed exactly `human-decided`) and require substantive edits to these paths to be assigned in the plan to the orchestrator as bootstrap edits after the accepted attempt.
3. Re-run the test green, inspect the instruction against criteria 2–3, then run full verification and the normal review loop and phase-6 review.

## Verification

Run the first command before and after the prompt edit; run the second afterward.

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py::test_the_plan_prompt_names_every_runner_held_path
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_the_plan_prompt_names_every_runner_held_path — a held entry is omitted; a planted new entry absent from the prompt must fail the coverage check.
- 2: not a test — phase-6 review compares the prompt's rule with committed-map, exactly-human-decided semantics; omission, an edited-map source or a mixed-class rule refutes it.
- 3: not a test — phase-6 review checks the prompt requires an orchestrator bootstrap edit after the accepted attempt; missing ownership or timing, or attempt ownership, refutes it.

## Not touched

No runner, provenance, gate, other prompt, template, ADR or sibling change edits.
Only this change's `plan.md` (time used and ledger status), `spec.md`
(implementation status) and `findings.md` (evidence and reviews) need record
updates; `plans/INDEX.md` is rendered by the runner, never hand-edited.

## Route

Explore used stage 2, GLM 5.3 Flash, on 2026-10-29; no Stage-1 fallback is
recorded. This draft writes only the artifacts; the orchestrating session
shows the card unchanged before carrying out the manual implementation.

## Time used
2026-10-29 22:56:49–22:58:17 UTC — implement · orchestrator bootstrap edit by hand (prompts/ is runner-held): test red first (all fifteen RUNNER_HELD entries missing), prompt item added, test green · measured with `date -u`
2026-10-29 23:28:00–23:36:54 UTC — review loop round 1 · Flash swarm, nine rows, all repaired by the orchestrator: L1-1, L1-2, L1-9 in the prompt item and its test (red first on the word substantively), L1-3 to L1-8 in the change's own headers and research text · measured with `date -u` (start read from the prepare-loop line, to the minute)
