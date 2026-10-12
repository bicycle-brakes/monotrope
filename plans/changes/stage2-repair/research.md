---
title: "Research — stage2-repair"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-g2f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, review-loop, repair]
---

# Stage-2 repair verb — Research

Phase 1 for bead coding-harness-g2f, read against `origin/main` on
2026-10-12. Today the review findings the orchestrator takes — loop rows of
phase 4b marked `taken`, and open phase-6 findings — are repaired by a Claude
Sonnet sub-agent, which costs Claude tokens. The bead asks for a runner verb
(for example `python3 scripts/stage2.py repair <change>`) that hands those
rows to GLM 5.3 (not Flash; maintainer, 2026-10-12) with the same guards as
`implement`: the leak check before the call, `make verify` after the attempt,
one repair attempt and a Stage-1 fallback, a failing test per row, and one
checkpoint commit. The flow is: the reviewer reports, the orchestrator
decides, GLM repairs, the reviewer re-checks. Non-goal: a reviewer (Codex,
the review-loop ladder) never repairs its own findings — it would judge its
own fix, and reviewers stay read-only (ADR 0007, ADR 0011).

## Questions for the exploration

1. How `implement` in `scripts/stage2.py` is built end to end: preflight,
   the prompt it assembles, the write permission it gives the model, the
   attempt and repair sequence (route `flash-repair`, the Sonnet fallback),
   the `make verify` run, the time-log check and the checkpoint commit — and
   which parts a second verb could reuse as they are.
2. Where the rows to repair live and in which form: the loop record
   (`~/.local/state/coding-harness/stage2/<change>/loop.md`, its Status and
   "Broke a test" columns), the phase-6 table in `findings.md`, and
   `release-loop`; how a taken row and an open finding are recognised today,
   and which code parses those tables.
3. Which models and endpoints `model-endpoints.yaml` and `stage2.py` declare
   (GLM 5.3, GLM 5.3 Flash, Sonnet, Haiku), how a verb picks one, and what
   the review-loop ladder and the phase-6 review read afterwards — so a
   re-check after a repair works with what exists.
4. Which documents name the repair step today (`docs/WORKFLOW.md` phase 4b
   and 6, `prompts/04-implement.md`, `AGENTS.md`, ADR 0007, ADR 0011), and
   which tests pin `implement` and the loop (`tests/` for `stage2`).

Stage-2 call, 2026-10-12: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 364 files, 909 commits, 12 rules.

## Runner exploration — 2026-10-12

**What exists today.** `scripts/stage2.py` is the only way a foreign model starts; its `VERBS` dict and `main()` dispatch eight verbs — `explore`, `implement`, `spec-review`, `review-loop`, `release-loop`, `review`, `probe`, `session`. A repair verb is not among them (the dict is the complete list). `--stage2-off` is refused for every verb but explore and implement (`main()`: `args.verb not in {"explore", "implement"}`). Exits: 0 done, 1 a call or post-check failed, 2 refused (`Refused`/`CallFailed`, module docstring).

**How `implement` runs, end to end** (all in `scripts/stage2.py`, function `implement`):

- `preflight(root, change, first, required=("plan.md",))`: the change folder exists (`folder_of`), the bead is read from `spec.md`'s header (`_artefact_bead`; `explore` instead reads it from `research.md`), the required files are readable, and `declaration_problem` clears the endpoint over `model-endpoints.yaml` — endpoint present, model in its `modelle`, `framework` among `darf_sehen` as a list, a residency other than `nicht-erklaert`.
- The worktree must be clean outside the change's `findings.md` (`changed_paths` minus `allowed`); the baseline commit, the plan's `## Time used` text (`time_log`) and a snapshot of the gitignored files (`ignored_snapshot`) are taken before the first call.
- With stage 2 on, `read_secret("GLM_KEY")` comes from the secrets file (`secrets_path()`, default `~/.config/cc-routing/secrets.env`); a missing key refuses. With `--stage2-off`, no key is read.
- The attempt routes are one list literal in `implement`: GLM_FLASH route `flash`; GLM_FLASH route `flash-repair`, reason "first Flash post-run check failed"; SONNET route `stage-1`, reason "two Flash post-run checks failed". With `--stage2-off`: a single SONNET `stage-1` attempt. The tuples: `GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")`, `SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")`.
- Each attempt: `implementation_prompt` assembles the full `prompts/04-implement.md` plus the repository rules from `AGENTS.md` (`work_prompt`), the accepted `spec.md` and `plan.md` in full, the implementation baseline, and the earlier attempts' diagnostics. `begin_work_call` runs the leak check for this exact prompt (`checked_prompt` → `leakcheck.check(change, leakcheck.default_denylist(), root, [("prompt", prompt)])`), appends the audit line to `findings.md`, and on the stage-1 route `insert_before_time` writes a route block into `plan.md`.
- The call: `run_work_model(..., writable=True)` starts `claude -p "Run the phase for <change> exactly as the appended instructions say." --append-system-prompt-file <scratch>/work-prompt.md --model <endpoint[1]> [--effort <endpoint[2]>] --tools Read,Grep,Glob,Edit,Write --restricted --safe-mode --strict-mcp-config --permission-mode acceptEdits --permission-prompts none --no-session-persistence --output-format text`, in the worktree, empty stdin, allow-list environment (`foreign_env`/`glm_env`: base URL `https://api.z.ai/api/anthropic`, the model pinned in every `GLM_MODEL_VARIABLES`). The read-only variant (`writable=False`, `WORK_READ_TOOLS = "Read,Grep,Glob"`) is what `explore` runs.
- Around the call: `worktree_tree` snapshots the tree through a temporary index before and after; `attempt_files` (git `diff-tree --numstat`, bounded at `ATTEMPT_FILES` = 40) lists what the model changed; `remove_changed_credential` cleans the exact key and its eight-character fragments from changed, untracked and newly touched gitignored files — once after the call and again after the gate.
- Post-run: `verify_attempt` runs `prepare_derived` first (stamps changed held documents through `check_frontmatter_current`, renders `plans/INDEX.md` via `scripts/plans_registry.py --index`), then exactly `make verify`; blocking gates are bounded by `red_sections` (gate frames, `RED_TOTAL_LINES` = 200), and `time_log(plan)` must show a new measured line.
- A failed attempt leaves `attempt_block`/`quote_block` — diagnostics and file list, every line `>`-quoted, key scrubbed — below its audit line in `findings.md`, and its problems join `diagnostics` for the next attempt's prompt. A model process that fails outright stops the run after `restore_baseline` (every path but `findings.md` back to the baseline); no silent route change.
- A green attempt ends in `checkpoint`: one commit (`git add -A`, message `feat(<change>): implement accepted plan`, author `stage2-runner <stage2-runner@invalid>`, gpgsign off), then the proof — exactly one descendant commit of the baseline, ancestor check, clean worktree.

**Where the rows a repair would consume live** (`scripts/stage2.py`):

- The loop record sits outside the repository: `record_dir(change)` → `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md` (`read_record`). Its rows are nine-cell lines (`ROW_COLUMNS`: ID, Severity, Dimension, Origin, Where, Finding, Reviewer, Status, Broke a test). Only the record's own lines count (`_record_lines` separates the reviewer's carried words); `record_rows` parses them and refuses a damaged row by id; `undecided` names rows whose Status does not begin `taken`/`rejected`, or whose taken row lacks `yes`/`no` in `Broke a test`; `taken_in_round(rows, n)` recognises a `L<n>-…` row whose Status begins `taken` — the round-3 gate. `release` deletes the record (`shutil.rmtree(record_dir(change))`) after carrying it into `findings.md`.
- After a release the rows stand in `findings.md` as ten-cell lines (`RELEASED_COLUMNS` = `ROW_COLUMNS` + `Phase 6`) under the last `## Phase 4b — loop rows, released` heading; `released_rows` reads that block and stops at `Kept from the loop record:`. `rounds_run` counts rounds from `## Round <n> —` headings in the record plus `Rounds run: <n>` lines a release left behind; `MAX_ROUNDS` = 3, and round 3 needs a taken row in round 2.
- Phase-6 findings are nine-cell rows (`ROW_COLUMNS`), Reviewer `Codex`, Status `open`, appended by `review()` under `## Phase 6 — Codex, <date>`; the release waits for a line matching `VERDICT_LINE` (`Phase 6 verdict: <reviewer> <session>, <date>`, `pending` is no reviewer), then `review()` marks each released row's `Phase 6` cell (`parse_marks`, `fill_marks`).
- `scripts/stage2_runs.py` imports `stage2` and counts with the runner's own constants (module docstring: "read with the runner's own row and line constants, so the count and the writer cannot drift apart").

**Models, endpoints, and what a re-check reads afterwards.** `model-endpoints.yaml` declares `glm-coding-plan` (Zhipu AI/Z.ai, `anbieter-erklaert`, `darf_sehen: [framework]`) with exactly two models: `glm-5.3` and `glm-5.3-flash`. A repair route on GLM 5.3 — the model the change's ask names (`plans/changes/stage2-repair/research.md` opening: "GLM 5.3 (not Flash; maintainer, 2026-10-12)") — is therefore already cleared by the declaration; no yaml change is needed for the route itself. The entry's remark names explore and implement as the work verbs and states that no review phase has routed to the endpoint since 2026-10-07 (ADR 0011); that remark is pinned by `tests/test_stage2.py::test_the_glm_remark_names_its_work_verbs_and_no_review_phase`. A verb picks its model by passing a tuple to `preflight`/`begin_work_call`; the call pins `endpoint[1]` as `--model`, with `--effort` when the third slot is set. After a repair, the existing re-check paths are the loop's next round (`review_loop` re-reads `change_diff` and the record, refuses undecided rows, counts through `rounds_run`) and phase 6 (`review` resumes the recorded Codex session found via `SESSION_LINE`, writes the verdict, releases, marks).

**Documents that name the repair step today:**

- `docs/WORKFLOW.md`: the phase table's 4b gate ("`make verify` green after each repair"); §2 findings process — Origin `base`/`fix-r<N>`, two consecutive `fix-r` rounds are an escalation, the evidence rule "holds in every repair round"; §4 routing — "a failed post-check gets one fresh Flash repair, then one Sonnet 5.5 fallback" (the implement route); §4 "The review loop (phase 4b)" — the implementer "repairs the taken rows and runs `make verify`, which must be green before the next round starts"; §4 "Two columns" defines `Broke a test`; §4 "The runner is the only way" says "Eight verbs exist".
- `prompts/04b-review-loop.md` ("For the implementer"): write `Status`, write `Broke a test`, "Repair the taken rows, then run `make verify`; round 2 starts only when it is green", release after the verdict.
- `prompts/04-implement.md`: file tools but no command tool; the runner verifies and commits; the evidence rule "holds in every repair round".
- `AGENTS.md`: the 4b row of the phase table (same gate wording) and the Stage-2 paragraph, which names `explore <change>` and `implement <change>` as the live runner verbs and closes "Reviews go by class; explore and implement do not."
- ADR 0007 (`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`): decisions 1 and 2 — leak check and declaration enforced on every call; framework content flows to `openai-codex` and `glm-coding-plan` through Claude Code, "Nothing else goes, and nowhere else". Decision 5 records explore/implement as "decided, not built" at that date.
- ADR 0011 (`docs/adr/0011-stage-2-reviews-through-opencode-go.md`): the loop belongs to the ladder alone (rounds `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro`; round 3 only after a taken row), Codex keeps 2a and 6, explore/implement stay on GLM 5.3 Flash. The reviewers' tools are read-only (`--tools read,grep,find,ls`; `PI_TOOLS` in `scripts/stage2.py`). The sentence "a reviewer never repairs its own findings" is not written verbatim in any file read; what is written is the read-only tool set of the reviewers and the change's own statement of the non-goal (`plans/changes/stage2-repair/research.md`: "reviewers stay read-only (ADR 0007, ADR 0011)").
- The bead's ask is recorded in `plans/changes/stage2-repair/research.md` (opening section) and named in `docs/journal/handover/2026-10-12-night-run-first-rehearsal.md` ("Beads opened tonight": "coding-harness-g2f (GLM repair verb)").

**Tests that pin what a second work verb would reuse** (`tests/test_stage2.py`, a `World` fixture with stand-in programs; no test starts a real model):

- Route sequence and fallback: `test_a_postcheck_failure_gets_one_flash_repair_with_its_diagnostic`, `test_two_failed_postchecks_route_once_to_sonnet`, `test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading`, `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`, `test_a_failed_flash_process_restores_the_baseline_so_stage2_off_can_proceed`, `test_a_leak_between_work_attempts_stops_before_fallback`, `test_stage2_off_is_only_for_work_verbs`.
- The work-call contract: `test_implement_flash_has_file_tools_and_the_complete_contract`, `test_explore_uses_flash_read_only_and_appends_research`, `test_explore_needs_research_but_not_spec_or_plan`, `test_a_missing_glm_key_refuses_the_flash_route`.
- Attempt evidence: `test_a_failed_attempt_quotes_its_diagnostics_below_its_audit_line`, `test_each_failed_attempt_lists_only_the_files_its_model_changed`, `test_a_failed_attempt_that_changed_nothing_says_so`, `test_verify_failure_is_bounded_in_the_repair_prompt`, `test_the_repair_prompt_names_the_gate_that_blocked_not_the_report_tail`, `test_a_blocking_gates_standard_error_reaches_the_repair_prompt`, `test_a_time_heading_deleted_mid_run_becomes_a_repair_diagnostic`.
- Credential guards: `test_a_changed_file_with_the_glm_key_is_cleaned_and_refused`, `test_a_key_fragment_in_a_changed_file_is_removed_and_refused`, `test_a_key_in_a_gitignored_file_written_by_the_run_is_removed_and_refused`, `test_a_key_in_the_gate_output_never_reaches_the_next_attempt`.
- Preflight: `test_implement_requires_spec_plan_time_heading_and_no_preexisting_work`, `test_no_change_or_a_missing_folder_refuses_every_verb`, `test_an_endpoint_the_declaration_does_not_clear_refuses`, `test_a_broken_declaration_stops_the_work_verbs_before_any_model`.
- Loop and release: `test_a_round_calls_its_rung_from_the_entry`, `test_reordering_the_ladder_touches_no_code`, `test_the_loop_stops_at_three_rounds`, `test_round_three_starts_only_after_a_taken_row`, `test_an_undecided_loop_row_holds_the_next_round_and_the_release`, `test_release_without_a_verdict_line_refuses_and_changes_nothing`, `test_the_release_carries_each_rows_reviewer`, `test_codex_marks_each_loop_row_after_its_verdict`, `test_a_damaged_loop_row_refuses_instead_of_vanishing`, `test_review_is_refused_while_a_loop_row_is_undecided`.
- Doctrine pins a new verb would meet: `test_workflow_section_4_routes_the_three_reviews`, `test_the_doctrine_and_prompts_say_the_flash_verbs_are_live`, `test_agents_md_names_the_loop_and_the_runner`, `test_every_prompt_asks_to_read_nothing_outside`, `test_the_glm_remark_names_its_work_verbs_and_no_review_phase`.

**What is unclear (open questions, not guesses):**

- The bead `coding-harness-g2f` itself was not read by the explorer (no shell). The orchestrating session read it with `tools/bd show` on 2026-10-12: the opening section of this file quotes it faithfully (GLM 5.3 not Flash, the guards of `implement`, one repair attempt and a Stage-1 fallback, a failing test per row, one checkpoint commit; reviewers do not repair).
- Whether the repair verb accepts `--stage2-off` is stated in no file read; the flag is today guarded to explore and implement in `main()`.
- A repair row exists in no routing document read: `docs/WORKFLOW.md` §4's tables name explore, implement, 2a, 4b and 6, and ADR 0011 gives the ladder the loop alone.
- `plans/specs/` holds no spec for this change: the directory contains only `.gitkeep` and `implementation-verification/spec.md` (directory listing taken).

**Which files a change would have to touch** (from what exists; nothing designed):

- `scripts/stage2.py` — a new verb function, its entry in `VERBS`, and `main()`'s dispatch and flag guards.
- `tests/test_stage2.py` — the pins listed above.
- The doctrine and rules that name verbs and the repair step: `docs/WORKFLOW.md` (phase table 4b row, §2 findings process, §4 routing and the "Eight verbs exist" sentence), `AGENTS.md` (phase table, Stage-2 paragraph), `prompts/04b-review-loop.md` ("Repair the taken rows…", today addressed to the implementer), and either `prompts/04-implement.md` or a new file under `prompts/` — `work_prompt` reads any `prompts/<file>` a verb names.
- `model-endpoints.yaml` needs no change for a GLM 5.3 repair route: `glm-5.3` is already declared on `glm-coding-plan` with `framework` and a residency; only the entry's remark names verbs, and a test pins it.

