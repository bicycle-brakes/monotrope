# terms-test-fixtures — Decisions

Class: bounded (one counted interview record or a reasoned skip owed). One
package led by coding-harness-hxkw with coding-harness-jik (maintainer,
2026-10-27).

## SKIP · interview

status: skipped
reason: Two test-only bugs whose beads state the problem and the direction. coding-harness-hxkw: at least five suites build model terms records by hand, so a new required field breaks other suites only after a merge (55 failures on 2026-10-27, `tests/test_stage2_research_availability.py`). coding-harness-jik: `test_terminal_record_survives_sigkill_after_the_outcome` times out under full `make verify` load while passing alone (measured 2026-10-20); the bead names the fix direction. No production behaviour changes; what remains is mechanics, decided below with reasons.

## Decided by the agent

[DETAIL] **One shared builder for an admissible terms record.** The suites
that hand-build a record (`research.md`, "What exists today") take it from
one test helper, so a new required field is added in one place. A test checks
that the helper's record passes the production check (`terms_problem` in
`scripts/stage2.py`), so the helper cannot fall behind the rule. Suites that
deliberately build a broken record keep doing so from the helper's output.

[DETAIL] **The flaky test waits on something load-independent.** The driver's
marker no longer depends on a pipe read within a fixed time under xdist load;
if that cannot be made reliable, the test is isolated from the parallel run.
Red first does not apply to a flake: the evidence is the measurement (the
test passes repeatedly under full `make verify` load), recorded in
`findings.md`.
