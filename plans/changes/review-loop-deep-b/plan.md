---
title: "Plan — review-loop-deep-b"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-pc7g
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — review-loop-deep-b

```text
For you:     The review loop keeps its rounds, its exclusions and its keys when a member is refused, excluded, interrupted or odd.
Done when:   Every criterion has a test that was red first (or a guard) and the runner suite and the full suite are green.
Appetite:    2 hours of phase 4; stop at the limit.
Not now:     DL-B-8 declared address, DL-B-9 Origin vocabulary, DL-B-13 retention validity date.
Pre-mortem:  suppose it failed: most likely because scrubbing every secrets value mangled an answer, or a signal handler leaked into the test process.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the tests named in the ledger, written first.
2. `scripts/stage2.py`:
   - `secret_values`, `scrub` over several secrets, `run_reviewer` scrubs
     every value (criterion 5) and names the actual limit (12);
   - `launch` tracks live process groups, `kill_live`, a bounded drain
     (`KILL_DRAIN_SECONDS`), `main` kills them on `KeyboardInterrupt` and
     `SIGTERM` (6, 7);
   - `NotStarted` from `remaining`; the replacement loop catches
     `Refused`, checks the deadline after the leak check and consumes only
     launched replacements (1, 9);
   - `paid_problem` in `ladder` and `skipped_models`; `discover_free`
     drops excluded and malformed ids and names them (2, 3, 8);
   - `MODEL_ID` in `select_free`, `render_table` escapes `|` (8);
   - `From <member>:` before each kept block, `_record_lines` reads it as
     the runner's (4); `_furniture` by column names (10).
3. `scripts/stage2_availability.py`: name the dropped free ids among the
   skipped (2).
4. `activate_overlay` copies only `OVERLAY_FIELDS`; `discover_free`
   names dropped fields (13, 14); the two header tests follow (the stage-2
   one keeps its name, which another plan's ledger cites).
5. `model-endpoints.yaml`: `modelle: [kimi, k3, moonshot]` on the Kimi
   exclusion (11).
6. This folder's `findings.md`; `plans/INDEX.md` if the registry asks.

## Verification

```sh
.venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/test_stage2.py
.venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_refused_flash_replacement_is_named_and_the_round_kept — the round is lost, or the refused rung is called or consumed.
- 2: tests/test_stage2.py::test_an_excluded_free_id_is_dropped_and_named — the free stage is refused whole, or the drop is silent.
- 2: tests/test_stage2_availability.py::test_availability_names_a_dropped_free_id_as_skipped — preparation probes or hides a dropped free id.
- 3: tests/test_stage2.py::test_an_excluded_paid_model_leaves_the_ladder_and_is_named — the excluded model stays on the ladder or in the Flash swarm.
- 4: tests/test_stage2.py::test_each_kept_block_names_its_member — a kept block has no member line, or the line is read as the reviewer's.
- 5: tests/test_stage2.py::test_every_secrets_value_is_scrubbed_from_loop_answers_and_errors — the GLM key reaches the record or stderr.
- 6: tests/test_stage2.py::test_an_interrupted_runner_kills_its_running_programs — the launched program outlives the interrupted runner.
- 6: tests/test_stage2.py::test_a_terminated_runner_kills_its_running_programs — the launched program outlives a SIGTERM.
- 7: tests/test_stage2.py::test_a_timeout_does_not_wait_for_an_escaped_descendant — the stop waits out the escaped descendant.
- 8: tests/test_stage2.py::test_a_catalog_id_with_a_pipe_is_dropped_and_named — a pipe id reviews and decides its own rows.
- 8: tests/test_stage2.py::test_render_table_escapes_a_pipe_in_a_cell — a pipe in a cell moves the columns.
- 9: tests/test_stage2.py::test_a_replacement_the_deadline_stopped_is_not_consumed — a rung that never ran is consumed.
- 10: tests/test_stage2.py::test_a_header_named_by_its_columns_is_furniture — a header with another first cell becomes a finding row.
- 11: tests/test_stage2.py::test_the_real_declaration_excludes_no_declared_model — a declared model is excluded (the Kimi exclusion was lifted on 2026-10-30, bead coding-harness-bomd).
- 12: tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit — the stop names 45 minutes for a call that had seconds.
- 13: tests/test_stage2.py::test_activation_copies_only_the_allowed_definition_fields — samplingParams, headers or compat reach models.json.
- 13: tests/test_stage2.py::test_catalog_headers_are_activated_as_literal_data — a catalog header reaches models.json, or the evidence changes.
- 14: tests/test_stage2.py::test_a_non_string_header_value_does_not_break_activation — a numeric header value raises.

## Route

Research, spec, plan, implementation and self-review by an Opus 5.5
sub-agent of the orchestrating Claude Code session in a cloud container on
2026-10-25, at the maintainer's instruction. The review loop and the
phase-6 Codex review are still owed.

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: maintainer: Sonnet replaces Codex for two hours (2026-10-26).

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: maintainer: Sonnet replaces Codex for two hours (2026-10-26).

## Runner route — 2026-10-27

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-10-27

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-26 00:48:46–01:06:31 UTC, 1066 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-26 17:18:57–17:32:01 UTC, 784 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-26 17:32:44–17:39:48 UTC, 424 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-26 17:51:48–18:11:38 UTC, 1190 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-27 08:58:18–09:19:16 UTC, 1258 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 09:19:22–09:48:15 UTC, 1733 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 09:48:38–10:18:41 UTC, 1803 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-27 10:21:18–10:50:46 UTC, 1768 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-27 11:06:01–11:17:31 UTC, 690 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-27 11:56:40–12:41:32 UTC, 2692 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 12:41:45–13:10:54 UTC, 1749 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 13:11:01–13:30:33 UTC, 1171 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-27 16:10:42–16:29:52 UTC, 1151 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
