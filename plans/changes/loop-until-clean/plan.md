---
title: "Plan — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-17
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, review-loop, opencode-go, swarm]
---

# Plan — `loop-until-clean`

```text
For you:     The review loop stops when no finding is accepted: live-checked free Go models first, three Flash models together next, then one paid model per round; free selection stays editable in YAML.
Done when:   All 16 criteria have their evidence, live refresh and configurable free selection work, both swarms and stop rules hold, paid terms are read or models skipped, and make verify is green.
Appetite:    8 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     Research swarm, structure-first review, live progress, different repair or phase-6 routing, and automatic provider fallbacks.
Pre-mortem:  suppose it failed: most likely because release lost the stage history and let an already-used reviewer run again.
Starts unless you say stop.
```

Implements `spec.md`; the design essentials phase 4 needs are carried below.
Q-9 requires automatic free Go membership; Q-10 requires the separate paid
Flash swarm. The last decisions addendum requires forced live refresh and
YAML selection. The ADR answer is already recorded; do not rewrite it.

## Steps and files

1. **`scripts/stage2.py` — admission and configuration.** Remove
   `MAX_ROUNDS`; keep one round per invocation. Add typed stage/run metadata,
   validate the paid `modelle` and eligible `flash_swarm` subset, then snapshot
   stage membership. Hold undecided/evidence-incomplete rows first, then stop
   for a clean previous round, two consecutive all-accepted-`fix-r` rounds,
   or exhausted stages, naming the round or maintainer as appropriate.
   Treat `fixed` as accepted everywhere. Skip an empty paid Flash stage
   without inventing a round; no failed-only attempt consumes a stage.
2. **`scripts/stage2.py` — free discovery and declaration.** Before round 1,
   force `tools/pi/pi update models`, then run `tools/pi/pi --list-models`
   in the same fresh isolated HOME/agent directories, with disabled loaders,
   timeouts and environment-only credential. Never list/use cached models
   after a failed/timed-out refresh. Parse provider/model table columns;
   read provider, suffix, include and exclude from YAML without free ids or
   suffix literals in code. Select catalog-present ids of the configured
   provider matching suffix or include, remove exclusions, deduplicate in
   catalog order; reject Zen, invalid rules and failed/malformed/empty output.
   Persist UTC date/time, pin, source `pi.dev`, rule, catalog and selected list;
   state that this live intermediary does not verify Go billing. Add
   call-scoped free-class admission requiring both discovery membership and
   confined free-review purpose; generic paid/session declaration stays strict.
3. **`scripts/stage2.py` — payload and parallel execution.** Build the free
   diff separately from `change_diff`: allow source/test code only, including
   uncommitted and untracked code, against the same merge base, using bounded
   hunks. For this repository select Python in `scripts/` and `tests/`, and
   executable source under `tools/`; exclude symlinks, dependency/generated
   trees, binary files, docs, plans, YAML declarations, locks and credentials.
   Put that diff and static reviewer/output instructions in a standalone
   prompt; omit `READ_REQUEST` and the paid prompt. Launch with scratch cwd,
   `--no-tools` and existing loader isolation. Paid calls retain the complete
   diff, loop prompt, worktree cwd and `read,grep,find,ls`. Check/audit each
   member in the parent before dispatch; a leak BLOCK aborts without fallback.
   Start member subprocesses concurrently with separate scratch directories
   and existing timeouts; only the parent writes results. Validate responses,
   merge in membership order into one heading and `L<n>-<k>` series, preserve
   duplicate reports and original member attribution. Name failed members;
   a partial successful round stands, an all-failed round does not.
4. **`scripts/stage2.py` — persistence and probe.** Keep nine-column loop
   rows and ten-column released rows, comma-joined heading members and numeric
   `Rounds run:`. Carry trusted snapshot/stage metadata through `kept_lines`
   on release; reconstruct history from every released block plus the active
   record, never from quoted reviewer text. Test clean zero-row rounds,
   split releases, the fix-r brake and configuration edits. Probe rediscovers
   free members with a forced refresh followed by listing and checks every
   distinct free/eligible paid id once with
   the matching call purpose/tools, declaration and leak checks. Update help,
   module text and the `taken_in_round` citation to ADR 0017 as amended by 0021.
5. **`model-endpoints.yaml` — declarations and measured terms.** Keep existing
   German keys; `modelle` holds eligible paid models in Q-1 order:
   `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `longcat-2.0`,
   `glm-5.3-flash`, `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5.5`,
   `minimax-m2.7`, `mimo-v2.6-pro`. Add `flash_swarm` for eligible first-three
   members and `free_stage: {provider: opencode-go, id_suffix: "-free", include: [], exclude: [], input: implementation-diff}`.
   Exceptions are `{id, date, reason}` records; require nonempty id/reason
   and an ISO date. Includes select only catalog-present Go ids; excludes
   win, including over includes. No individual declaration is required for
   discovered matches. Future rule changes use an ordinary YAML PR and take
   effect on fresh runs; active runs keep their snapshot. Read actual Go data terms in phase 4,
   cite dates/sources for retention and training in the remark, and exclude
   paid ids with unread terms or permitted training (Q-11: read and record
   retention; the maintainer admitted 30-day readers on 2026-10-17). Record skipped ids and reasons for the
   handover in **`plans/changes/loop-until-clean/findings.md`**; do not silently
   respell refused ids. Preserve sourced price/limit claims without inventing
   new ones. State the diff-only unread-terms exception, forced refresh and
   the live Pi catalog's source/billing limitation.
6. **`tests/test_stage2.py`** — implement the ledger's new tests with local
   stand-ins and barrier-controlled concurrent calls; adapt existing single
   reviewer fixtures and doctrine guards. Exercise refresh-before-list
   ordering, stale-cache refusal, timeouts, changing provider/suffix/rules
   without code edits, dated exception validation, exclusion precedence,
   catalog-absent includes and Zen rejection. Preserve test names referenced by
   other live/archived ledgers, including the fixed-round-two test, while
   updating operative expectations for the amendment. Historical ADR 0011,
   ADR 0017 and archived-design assertions still test historical text.
   **`tests/test_model_endpoints.py`** checks class versus individual
   admission and dated terms/skip records, with planted negative cases.
   **`tests/test_pi_contract.py`** extends the existing real pinned-Pi
   loopback capture through production launch: plant source/doc/plan/context
   canaries, request read tools from the fake server, and assert outgoing
   free payload contains only permitted hunks and no tool schema or tool
   result. Paid launch contracts must still expose exactly the old read tools.
   Reuse **`tests/pi_contract_driver.mjs`** and **`tests/pi_network_guard.mjs`**
   unchanged; all transport is loopback with synthetic credentials.
7. **Doctrine:** **`AGENTS.md`** changes its phase-4b row/Stage-2 paragraph
   within 200 lines; **`docs/WORKFLOW.md`** changes the phase table, findings
   escalation, model table, verb list and review-loop/repair sections;
   **`prompts/02a-spec-review.md`** and **`prompts/06-review.md`** replace
   their round-limit descriptions; **`prompts/04b-review-loop.md`** describes
   both swarms, live class discovery, configurable selection, confinement and stops;
   **`templates/findings.md`** generalizes the repair-brake consequence.
   **`ROADMAP.md`** updates the review-swarm/until-clean item without claiming
   other queued work. **`docs/adr/0021-review-swarms-until-clean.md`** remains
   the sole new ADR; align only measured details, preserving human answers.
8. **Change artifacts:** **`plans/changes/loop-until-clean/plan.md`** flips
   each `not yet written` entry when its test exists and records measured time;
   **`plans/changes/loop-until-clean/findings.md`** receives runner evidence,
   skips and review statuses. **`plans/INDEX.md`** is refreshed by the runner's
   derived-file preparation. The runner owns verification and the checkpoint.

## Do not touch

Protected spec paths, existing ADR bodies, archived plans, research-swarm
implementation, `decisions/answers/loop-until-clean/adr.yaml`, stage-1 and
interactive-session behavior, repair routing, or the verdict-before-release
order. `scripts/handover_schema.py` and `scripts/stage2_runs.py` stay as they
are; exercise their existing tests against higher round numbers. No provider
call belongs in an automated test; live compatibility evidence is a separate
phase-4 special run after terms admission.

## Explore fallback carried forward

None: phase 1 used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`, on 2026-10-14 (`research.md`). Earlier draft fallbacks are
historical runner evidence, not an Explore fallback.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py tests/test_feedback_channel.py tests/test_pi_contract.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change loop-until-clean
.venv/bin/python3 scripts/check_adr_answers.py
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --check
make verify
```

The prompt's `python3 scripts/validate_change_artefacts.py --check` cannot run:
that file is absent in this worktree on 2026-10-16. Do not fabricate a passing
result or add it as part of this change. The outer runner performs full
verification and the sole commit; this drafting call does neither.

Draft checks on 2026-10-16: interview minimums, ADR answers and criterion
ledger passed; required frontmatter, opening card, empty time section and
generated-index equality were checked locally. The full registry's tracker
coupling was not measured: no in-worktree render is supplied, and this call
may read only the worktree and repository git directory. The outer runner
owns that check along with `make verify`.

## Criterion ledger

- 1: tests/test_stage2.py::test_a_clean_round_ends_the_loop — an empty or all-rejected round admits another call before or after release
- 2: tests/test_stage2.py::test_both_swarms_run_in_parallel_as_one_round — a barrier detects serialization, member omission, duplicate ids or wrong Reviewer cells
- 3: tests/test_stage2.py::test_the_free_stage_reads_nothing_beyond_the_diff — doc/plan/unrelated-file canaries or an added READ_REQUEST outside the quoted diff reach a free call, or paid tools disappear
- 3: tests/test_pi_contract.py::test_real_free_reviewer_has_only_the_implementation_diff — the actual pinned Pi sends canaries, tools or a tool response to the loopback capture
- 4: tests/test_stage2.py::test_a_failed_swarm_member_preserves_successful_answers — a failed/malformed member erases successful rows or an all-failed attempt consumes a round
- 4: tests/test_stage2.py::test_a_call_without_an_answer_is_not_a_round — an empty answer completes a round
- 5: tests/test_stage2.py::test_free_discovery_admits_new_go_models_each_run — an undeclared new matching Go model is omitted, Zen is called, empty/malformed discovery launches a call, or date/list is absent
- 5: tests/test_stage2.py::test_free_discovery_forces_live_refresh_before_listing — listing runs first, refresh/list use different scratch directories, a four-hour cached list is reused after failed/timed-out refresh, or the source/time is missing
- 5: tests/test_stage2.py::test_free_selection_changes_in_yaml_without_runner_edits — suffix/include/exclude edits do not change membership, an excluded or catalog-absent id is called, or provider selection admits Zen
- 5: tests/test_model_endpoints.py::test_free_selection_exceptions_require_dates_and_reasons — malformed rules or undated/unreasoned exception entries pass validation
- 6: tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading — a paid declaration lacks dated retention/training evidence or a skipped requested id is unnamed
- 6: tests/test_stage2.py::test_ineligible_paid_models_are_skipped_and_named — a disallowed paid model is called or empty eligible Flash membership creates a fake round
- 7: tests/test_stage2.py::test_free_class_admission_is_bound_to_discovery_and_purpose — a guessed free id, Zen id, paid call or interactive session gains the exception
- 7: tests/test_model_endpoints.py::test_unread_terms_reach_the_free_stage_alone — the entry omits or broadens the diff-only acceptance
- 8: tests/test_stage2.py::test_a_round_calls_its_rung_from_the_entry — paid stages execute out of configured order
- 8: tests/test_stage2.py::test_reordering_the_ladder_touches_no_code — changing the eligible configured order requires model literals in code
- 8: tests/test_stage2.py::test_round_two_is_the_flash_swarm_then_single_rungs — first-three reviewers run as sequential rounds or a later rung joins the swarm
- 9: tests/test_stage2.py::test_the_loop_stops_when_the_ladder_ends — the last model repeats, a refused id gets a substitute, or exhaustion is called clean
- 10: tests/test_stage2.py::test_two_fix_r_rounds_stop_the_loop — accepted fixed rows fail to trigger the brake or a base row does not prevent it
- 11: tests/test_stage2.py::test_round_three_starts_after_a_fixed_round_two_row — repair makes the preceding round clean or loses its count
- 12: tests/test_stage2.py::test_an_undecided_loop_row_holds_the_next_round_and_the_release — a pending/evidence-incomplete row admits review or release
- 13: tests/test_stage2.py::test_round_history_survives_split_releases_and_config_edits — clean/brake state, multi-digit counts or consumed stages are lost across releases
- 14: tests/test_stage2.py::test_the_probe_checks_discovered_and_paid_models_once — a member is missing/repeated, discovery skips forced live refresh or configured selection, or a per-call guard/payload boundary is bypassed
- 15: tests/test_stage2.py::test_the_loop_doctrine_names_both_swarms_until_clean — live text keeps the old cap/order/declaration rule, claims pin-limited freshness, lacks live-source/configuration limits, cites ADR 0015 or exceeds the AGENTS.md cap
- 16: tests/test_stage2.py::test_adr_0021_amends_the_round_budget — the new record omits Q-9/Q-10 or the live/configurable-selection addendum, or modifies historical ADR bodies

- 13: tests/test_stage2.py::test_reviewer_words_cannot_count_as_rounds — reviewer headings or count lines create a false clean round before or after release
- 6: tests/test_pi_contract.py::test_real_opencode_provider_contracts — an admitted rung leaves the measured wire API or address without being skipped
- 16: tests/test_stage2.py::test_paid_terms_doctrine_records_the_retention_decision — the spec or ADR omits Q-11's dated retention admission or the ADR's Q-11 to Q-13 review lineage
- 6: tests/test_stage2.py::test_paid_terms_require_a_retention_reading — missing, blank or non-text retention readings admit a paid model
- 7: tests/test_stage2.py::test_released_reviewer_words_cannot_supply_a_snapshot — kept reviewer words inject a released heading, snapshot or row
- 8: tests/test_stage2.py::test_first_paid_rung_names_missing_cost_when_flash_is_skipped — an empty Flash stage silences the first paid round's missing-cost notice

## Runner route — 2026-10-16

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-16 span not measured: this Stage-1 repair session had file tools only and could not read `date`; no estimate is recorded.

2026-10-17 02:57:40–03:14:12, 00:16:32 — repair of the taken second-round findings, including verification waits.

Repair evidence: new regression tests failed against the repair baseline `2bea51c`. The affected-suite run finished with 727 passed, 13 skipped and one obsolete lineage-text assertion; after correcting that assertion, the focused documentation and regression rerun passed all 36 tests. The 12 real Pi contracts passed with local loopback access. Ruff check, format check, interview minimums, ADR answers and the criterion ledger passed. The exploratory `make verify` runs were interrupted: the sandbox denied loopback servers and the shared tracker is outside this repair call's read scope. The separate registry check reported tracker state not measurable. The outer runner owns the final complete `make verify` and checkpoint; this call made no commit and did not edit `findings.md`.

2026-10-17 09:19:52–09:28:29, 00:08:37 — repair of taken phase-6 rows P6-1 through P6-7, including verification waits (Europe/Berlin).

Repair evidence (2026-10-17): all ten new regression cases failed against the repair baseline `d0bc4e8` in a temporary archive; the restored real-Pi per-rung contract also failed on that baseline configuration before the wire-API skips. The affected-suite run reported 653 passed and 17 failed: six cases used the earlier text expectations/test setup, and eleven Pi cases were refused loopback access by the sandbox. After correcting the text expectations and the injection fixture, the exact 17 failures passed with local loopback access. The focused final regression/text run passed 17 cases; the real-Pi contract suite passed all 12 cases. Run-log and feedback tests passed 68 cases with 13 skips. Ruff check, format check, interview minimums, ADR answers, the criterion ledger and git diff whitespace checks passed. The four unmeasured wire-API models remain named and skipped in the endpoint declaration; their Q-11 data-terms admission stands. This call did not edit `findings.md`, run a provider call or make a commit. The outer runner owns full `make verify` (including the shared tracker outside this call's read scope) and the checkpoint.
