---
title: "Findings — isolated-attempts"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — isolated-attempts

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1141 commits, 12 rules.

Stage-2 call, 2026-10-15: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 424 files, 1198 commits, 12 rules.

## Written stop — 2026-10-15

The phase-4 implement run (route flash, GLM 5.3 Flash) started at 06:31 and
the worker finished writing at about 10:20; the runner's post-run
`make verify` then hung in `pytest tests/ -q` for more than three hours
(measured 13:30: elapsed 03:08:51, normal about nine minutes). The
orchestrating session stopped the run at the maintainer's request and
committed the worker's partial state unchanged as work in progress. Nothing
in this commit is verified: `make verify` never finished, and which test
hangs was not yet measured (candidates by name: the live tests in
`tests/test_stage2_isolation.py`, which may start Podman; the Podman machine
was running). Next: run the new test files one by one with a per-test time
limit to find the hang, then decide whether the change continues after
coding-harness-agx and coding-harness-icw.

Measured 2026-10-15 (orchestrating session, the changed and new test files
run with `-o faulthandler_timeout=180`, stopped after the dump):
`tests/test_stage2_egress.py::test_the_wire_refuses_a_bypass_and_relays_the_declared_path`
hangs — two relay threads stay in `scripts/stage2_egress.py` `pump` (line
153) and the test waits at its line 99; this is the hang that stopped
`make verify`. Before it, two tests failed:
`tests/test_stage2_attempt.py::test_each_attempt_gets_its_own_recorded_state`
and `tests/test_stage2_egress.py::test_only_globally_routable_addresses_may_be_dialled`.
The rest of the files did not run. Also found in the partial state:
`tools/stage2/Containerfile` installs Pi as `@mariozechner/pi@1.1.0`, a wrong
package name (the installed Pi is `@earendil-works/pi-coding-agent`); by the
maintainer's decision of 2026-10-15 the container's Pi comes only from
`tools/pi/` of coding-harness-agx, which this change now waits for.
