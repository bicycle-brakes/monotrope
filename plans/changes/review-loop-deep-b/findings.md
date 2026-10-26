---
title: "Findings — review-loop-deep-b"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: to be filed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-loop-deep-b

## Implementation, 2026-10-25

Implemented test first by an Opus 5.5 sub-agent of the orchestrating Claude
Code session in a cloud container, at the maintainer's instruction of
2026-10-25 ("fix every runner defect the deep review found").

Red first, against `f8a6b33` (`origin/main`): the fourteen tests of
criteria 1 to 10 failed before the edit (one run, `pytest -n 4`; the
Ctrl-C test's uncaught interrupt stopped its xdist worker, which is the
defect); criteria 11 and 12 and the replacement-deadline test failed in a
separate run. The tests of criteria 13 and 14 were added after the code
(scope added by the orchestrator mid-change) and were then run against an
export of `f8a6b33`: all three failed there (`AttributeError` on the
integer header, no allow-list, headers activated).

| Row | Criterion | Outcome | Proof |
|---|---|---|---|
| DL-B-1 | 1 | fixed | tests/test_stage2.py::test_a_refused_flash_replacement_is_named_and_the_round_kept |
| DL-B-2 | 2, 3 | fixed | tests/test_stage2.py::test_an_excluded_free_id_is_dropped_and_named, ::test_an_excluded_paid_model_leaves_the_ladder_and_is_named, tests/test_stage2_availability.py::test_availability_names_a_dropped_free_id_as_skipped |
| DL-B-3 | 4 | fixed | tests/test_stage2.py::test_each_kept_block_names_its_member |
| DL-B-4 | 5 | fixed | tests/test_stage2.py::test_every_secrets_value_is_scrubbed_from_loop_answers_and_errors |
| DL-B-5 | 6 | fixed | tests/test_stage2.py::test_an_interrupted_runner_kills_its_running_programs, ::test_a_terminated_runner_kills_its_running_programs |
| DL-B-6 | 7 | fixed | tests/test_stage2.py::test_a_timeout_does_not_wait_for_an_escaped_descendant |
| DL-B-7 | 8 | fixed | tests/test_stage2.py::test_a_catalog_id_with_a_pipe_is_dropped_and_named, ::test_render_table_escapes_a_pipe_in_a_cell |
| DL-B-10 | 9 | fixed | tests/test_stage2.py::test_a_replacement_the_deadline_stopped_is_not_consumed |
| DL-B-11 | 10 | fixed | tests/test_stage2.py::test_a_header_named_by_its_columns_is_furniture |
| DL-B-12 | 11 | fixed (data) | tests/test_stage2.py::test_the_real_declaration_excludes_kimi_and_no_declared_model |
| DL-B-14 | 12 | fixed | tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit |
| RS-3-3 | 13 | fixed | tests/test_stage2.py::test_activation_copies_only_the_allowed_definition_fields |
| RS-3-8 | 14 | fixed | tests/test_stage2.py::test_a_non_string_header_value_does_not_break_activation |

Existing tests changed with the behaviour, each named here:

- `tests/test_stage2.py::test_a_call_over_the_time_limit_is_stopped`: the
  stop now names the round time limit (criterion 12).
- `tests/test_stage2.py::test_catalog_headers_are_activated_as_literal_data`
  (P6-15 of `loop-until-clean`): headers no longer reach `models.json` at
  all, so the escaping they needed is gone. The function keeps its name
  because the ledger of `plans/changes/loop-until-clean/plan.md` cites it;
  its docstring says what it holds now.
- `tests/test_pi_contract.py::test_real_catalog_headers_remain_literal`:
  asserts that the real composer sees no catalog header. Not run here:
  the container's Node is not 22 (the known container-only failure).

## Self-review, 2026-10-25

Read by the implementing sub-agent, so it is no independent review.

- `KeyboardInterrupt` still propagates out of `main` after the kill, as
  `tests/test_stage2.py::test_runner_logs_verification_interrupt_once`
  requires; SIGTERM returns 143. The handler is installed only from the
  main thread and restored in `finally`.
- A secrets value shorter than 8 characters (`OTHER=1`) is not scrubbed,
  except the two named keys; scrubbing it would replace ordinary text
  (`decisions.md`).
- `FROM_LINE` cannot be forged by a reviewer: every reviewer line is
  written quoted (`> `), so only the runner writes an unquoted line.
- A record written before this change has no `From` lines and reads as
  before.

## Open questions for the maintainer, 2026-10-25

Not changed here (`decisions.md`, scope cut). Each needs a decision.

- **DL-B-8 (MAJOR, doctrine) — the destination of every Go call comes from
  the pi.dev catalog.** The fetched definition's `baseUrl` (and `api`)
  crosses into Pi's configuration unchecked, for free and paid calls; the
  OpenCode key and the diff go wherever it points.
  `tests/test_pi_contract.py` even asserts that a catalog `baseUrl` is
  activated for a declared paid model. Criterion 13 narrows the fields but
  leaves `baseUrl` as it came.
  *Recommendation:* declare the address in the `opencode-go` entry
  (`adresse: https://opencode.ai/zen/go/v1`) and drop, with a notice, every
  overlay definition whose `baseUrl` differs, before activation. One
  bounded change with a decision PR for the YAML field.
- **DL-B-9 (MINOR, doctrine) — the repair brake reads an Origin cell no
  loop reviewer is told how to fill.** `fix_r_only` reads the reviewer's
  own Origin cell; neither `prompts/04b-review-loop.md` nor the free prompt
  defines `base` / `fix-r<N>`, so the brake trips on unprompted text.
  *Recommendation:* the orchestrator owns the cell — it sets Origin while
  it decides a row, and the runner refuses a taken row whose Origin is not
  `base` or `fix-r<N>`. That needs no prompt change (`prompts/` is
  `human-written`).
- **DL-B-13 (MINOR, schema) — a retention reading with an end date admits
  for ever.** The DeepSeek ZDR reading says "valid through 2026-10-31";
  `terms_problem` checks only that `aufbewahrung` is a non-empty string.
  *Recommendation:* a machine-readable `gilt_bis: YYYY-MM-DD` in
  `modelle_terms`, compared with today by `terms_problem` (past → skipped
  and named), set on both DeepSeek rows. A decision PR for the schema,
  before 2026-10-31.

## Known limits (2026-10-25)

- A rung refused at replacement stays in the run's snapshot; its own later
  round is refused by the declaration as before, and
  `release-loop --stage-failed` retires it.
- Between the deadline check and the launch, a call line can still be
  written for a replacement that `remaining()` then refuses; it is named
  ("did not start") and not consumed.
- The dropped catalog fields are named on stderr at discovery, not in the
  loop record.

## Route

The review loop and the phase-6 Codex review are still owed.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 593 files, 2184 commits, 12 rules.

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 593 files, 2186 commits, 12 rules.
