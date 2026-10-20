---
title: "Plan — failed-check-secrets"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-8hr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, leak-check]
---

# Plan — failed-check-secrets

```text
For you:     A fixture secret printed by a failed check no longer blocks the runner's retry; other leak-check violations still stop it.
Done when:   Regression tests hold criteria 1–7, including a successful retry through the real leak check, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Earlier findings, source/history cleanup, leak-check exemptions, routing or model-answer redaction.
Pre-mortem:  suppose it failed: most likely because findings.md was cleaned but the retry kept the original diagnostic string.
Starts unless you say stop.
```

Implements `spec.md` (bounded; no design or ADR). Inspection baseline:
`2cc2c81`, 2026-10-16. Explore ran on Stage 2, route flash, model
`glm-5.3-flash`; no Stage-1 fallback is recorded to carry forward.

## Files and steps

1. `tests/test_stage2.py` — add the ledger's tests first, using `world`,
   `draft_world`, `repair_world`, the make/model stand-ins and prompt capture.
   Add a test-local `secret:` rule alongside the existing non-secret
   `DENYLIST`; do not relabel the shared planted rule. Build synthetic key
   values from parts. Exercise draft, implement and repair, including keyless
   Codex and Stage-1 routes, with a failing then passing check. Assert both
   findings and captured prompts lack the value, keep the marker and useful
   exception/location lines, and reach the second model through the real
   `leakcheck.check`. Cover framed stdout, unframed output and stderr;
   preparation and other postcondition messages must use the same protection.
   Inject denylist read failures after the initial clean call; assert refusal,
   no raw diagnostic write and no retry/fallback. Keep existing guards intact.
2. `scripts/stage2.py` — add a diagnostic redactor beside `scrub`, reusing
   `leakcheck.default_denylist()` and `leakcheck.read_denylist()` at emission
   time, including when the routing key is `None`. Refuse on a read error,
   naming only the safe reason. Check the original text for non-secret rule
   matches before replacement; refuse with rule name and location, never the
   value. Collect secret match spans from that same original text, coalesce
   overlaps, replace their union with the participating rule markers in
   denylist order, and preserve newline separators. Apply existing credential
   scrubbing as well; refuse safely if the resulting text still matches a
   secret rule rather than emitting unchecked evidence.
   Redact full verification streams before `red_sections`/tail reduction in
   `verify_evidence` so truncation cannot destroy a multiline match. Protect
   preparation evidence before its reduction too. In `draft` and the shared
   `run_attempts`, sanitize the assembled postcheck listing before it enters
   either `diagnostics` or `attempt_block`; protect the block's file entries
   and measurement-error text before quoting. Both destinations consume the
   same safe listing. Preserve fences, bounds, audit ordering, attempt limits,
   every `checked_prompt` call and the existing credential scans. Update the
   relevant diagnostic docstrings, including keyless-route behavior.
3. `plans/changes/failed-check-secrets/plan.md` — replace each `not yet written`
   ledger entry when its test exists and record measured phase-4 time below.
4. `plans/INDEX.md` — regenerate after the new artifacts; no hand edits.

No file is deleted. No separate template for `plan.md` exists under
`templates/`; this follows the phase-3 card, ledger and time-section form.

## Verification

Show the new retry regression red against the pre-change runner, then green
with the fix; retain the result and commit in the implementation evidence.

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_leakcheck.py
.venv/bin/python3 scripts/check_interview_minimums.py --change failed-check-secrets
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --index
make verify
```

The phase prompts also name `scripts/validate_change_artefacts.py --check`;
that script is absent at the inspected baseline. Do not claim it passed or
add a validator in this change; the runner owns the full verification gate.

## Criterion ledger

- 1: tests/test_stage2.py::test_failed_check_diagnostics_redact_secret_rules_on_every_work_route — one verb, keyless route or destination retains the value
- 1: tests/test_stage2.py::test_preparation_and_postcondition_diagnostics_redact_secret_rules — protection exists only for make output
- 1: tests/test_stage2.py::test_secret_line_anchors_are_redacted_in_failed_gate_output — an anchored secret survives a later line in framed or unframed output
- 1: tests/test_stage2.py::test_moved_head_diagnostics_protect_file_evidence — a changed path or measurement error publishes a secret after HEAD moves
- 2: tests/test_stage2.py::test_diagnostic_redaction_keeps_rule_names_and_traceback_context — replacement erases unmatched context or loses rule names
- 2: tests/test_stage2.py::test_diagnostic_redaction_handles_overlaps_and_multiline_matches — replacement or truncation leaves part of a matched span
- 3: tests/test_stage2.py::test_a_fixture_secret_in_a_failed_draft_check_allows_a_clean_retry — the real pre-call check refuses the second call
- 4: tests/test_stage2.py::test_diagnostic_redaction_refuses_an_unusable_denylist — raw diagnostics are emitted or retry/fallback starts after a failed rule read
- 5: tests/test_stage2.py::test_nonsecret_diagnostic_matches_still_refuse — an overlapping secret replacement hides a non-secret violation
- 5: tests/test_stage2.py::test_nonsecret_preparation_errors_stop_before_retry — preparation converts a diagnostic refusal into a retryable error
- 6: tests/test_stage2.py::test_secret_rules_outside_diagnostics_still_block_retry — a secret in a non-test file or history is cleaned or bypasses the next scan
- 6: tests/test_stage2.py::test_each_call_runs_its_own_leak_check — a later call skips its scan
- 6: tests/test_stage2.py::test_a_leak_between_work_attempts_stops_before_fallback — a refusal falls through to another model
- 7: tests/test_stage2.py::test_a_key_in_the_gate_output_never_reaches_the_next_attempt — credential scrubbing regresses
- 7: tests/test_stage2.py::test_a_failed_stage2_off_attempt_leaves_its_block_without_reading_the_key — diagnostic handling reads an unneeded routing key
- 7: tests/test_stage2.py::test_credentials_are_scrubbed_before_diagnostic_rules — a denylist rule refuses a known credential or changes its credential marker

## Not touched

`scripts/leakcheck.py`, `tests/test_leakcheck.py`, real denylist/secrets,
`scripts/stage2_session.py`, the review loop, routing declarations, `prompts/`,
`docs/WORKFLOW.md`, `decisions/`, `provenance.yaml` and `docs/adr/` stay as they
are: this repair changes diagnostics inside the existing runner boundary.
No earlier diagnostic record, source value or history is rewritten.

## Runner route — 2026-10-20

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM unavailable until 2026-10-21T20:34+08:00.

## Time used

2026-10-20 span not measured: this session had file tools only, no command tool to read `date`; the runner's own clock bounds it.

### Orchestrator — phase 4, 2026-10-20

Measured with `date -u`. Merge of `origin/main` (162 commits) and venv
rebuild from 00:38Z; implement run with Sonnet 5.5 (`--stage2-off`, GLM via
Z.ai unavailable until 2026-10-21) 00:39:35Z to 00:44:27Z, rejected for four
ruff findings (unused arguments in the new tests) and a red pytest gate in
its own post-run check; the orchestrator fixed the four lint findings by
hand; `tests/test_stage2.py` green (674 passed); red first checked by hand
against `ec6f322`: seven of the eight new tests fail there,
`test_secret_rules_outside_diagnostics_still_block_retry` is a guard and
passes on both sides; full `make verify` green 00:47:13Z to 00:51:24Z (2299
passed, 16 skipped). Span about 14 min of the 2 h appetite.

### Repair — multiline non-secret diagnostics, 2026-10-20

2026-10-20 01:24:55–01:32:04 UTC, 7 min 9 s (measured with `date -u`).
The full-original-text check precedes secret replacement; the existing
per-line check retains line-anchored rule behavior. The criterion-5 test
covers single-line and multiline overlapping non-secret/secret patterns,
with an explicit assertion when refusal is missing.

Red-first evidence: the current test with `protect_diagnostics` loaded from
repair baseline `3ec9fe6` produced 1 failed, 1 passed; the multiline case
failed with `AssertionError` because the non-secret match did not refuse.
The corrected function passes both cases. Verification:
`.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_leakcheck.py`
passed (739 tests); Ruff check and format check passed; the criterion-ledger
check passed. No commit was made; the runner owns `make verify` and the
checkpoint commit.

### Repair — taken loop-round-2 findings, 2026-10-20

2026-10-20 02:06:49–02:14:46 UTC, 7 min 57 s (measured with `date -u`).
The existing uncommitted repairs cover line-anchored secret matches,
preparation refusals, credential marker precedence, repair findings
restoration, framed red-gate evidence and moved-HEAD file evidence. The
credential regression now explicitly raises an assertion if diagnostics
refuse a known credential, so the baseline failure meets the runner's
red-first assertion contract.

Red-first evidence: loading `protect_diagnostics`, `prepare_derived` and
`run_attempts` from baseline `9c5c9c6` into the test module's runner made
all 11 selected parameterized regression cases fail by assertion. The
repaired code passed all 11. The combined command
`.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_leakcheck.py`
passed all 750 tests in 409.13 seconds. Ruff check and format check,
interview minimums, criterion ledger and `git diff --check` passed.
Regenerating `plans/INDEX.md` produced no content change. No edit was made
to `findings.md`; no commit or repository-changing git command was run in
this checkout. The runner owns `make verify` and the checkpoint commit.

### Orchestrator — review loop, 2026-10-20

Measured with `date -u`. Availability reported in the conversation at
00:52:31Z (free swarm cat-jam-free, longcat-2.5-preview-free; Flash swarm
deepseek-v4.1-flash, mimo-v2.6-flash, longcat-2.0; paid ladder
glm-5.3-flash, mimo-v2.6-pro). Round 1 (free swarm) 00:52:37Z to 01:12:13Z:
2 rows, L1-1 taken (criterion 5: non-secret rules were checked line by line
only), L1-2 rejected as its duplicate; repaired by Codex 01:12:40Z to
01:36:30Z (`9c5c9c6`). Round 2 (Flash swarm) 01:36:41Z to 01:53:48Z: 10 rows,
six taken (L2-1 BLOCKER anchored secret rules redacted on the first line
only; L2-2, L2-3, L2-4, L2-5, L2-8), four rejected (L2-6 and L2-7 as
duplicates, L2-9 because criterion 4 wants the refusal, L2-10 as style);
repaired by Codex 01:54:18Z to 02:19:42Z (`e7b8f94`). Round 3 (glm-5.3-flash)
02:19:53Z to 02:24:59Z: the call failed ("Request timed out"); the loop
stops there and substitutes no model. Next: the maintainer decides whether
the loop resumes (release or a fresh run) before phase 6. Span about 1 h 32
min; phase 4 and the loop together about 1 h 46 min of the 2 h appetite.

