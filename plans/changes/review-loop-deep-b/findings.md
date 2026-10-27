---
title: "Findings — review-loop-deep-b"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-27
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

Stage-2 call, 2026-10-26: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 614 files, 2223 commits, 12 rules.

Loop attempt: 2026-10-26 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Stage-2 call, 2026-10-26: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 614 files, 2224 commits, 12 rules.

## Phase 6 — Sonnet 5.5, 2026-10-26

First phase-6 review in a fresh read-only Sonnet 5.5 sub-agent of the orchestrating Claude Code session: the maintainer moved the Codex tasks to Sonnet for two hours (2026-10-26, 17:26–19:26 CET). Its rows are recorded unchanged; its checked line: criteria 1-14 read against the diff, including the main-merge decisions; 54 targeted tests run and passing; no fix was reverted to prove its test, and the full `make verify` was not run.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MINOR | MAINT | base | `scripts/stage2.py:1822–1824` | The stderr notice "catalog fields not activated" (criterion 13) prints third-party catalog ids and field names raw. The sibling free-ids-dropped path does sanitize, through `dropped_notice` (stage2.py:1773-1781) and the test `test_a_dropped_catalog_id_carries_no_control_bytes`. I ran `activate_overlay(d, {"p": {"models": [{"id": "a\x1b[31mX", "samplingParams": {}, "ev\x1b]0;pwn\x07il": 1}]}})`. It returns `{'a\x1b[31mX': ['ev\x1b]0;pwn\x07il', 'samplingParams']}`, and the `print` joins those strings unchanged. A catalog author can therefore inject terminal escape sequences into the maintainer's stderr. The cure is to route this listing through the same `visible()` escaping. | Sonnet 5.5 | fixed — tests/test_stage2.py::test_a_not_activated_catalog_field_carries_no_control_bytes | — |
| F6-2 | MINOR | SPEC | base | `scripts/stage2.py:78–89` | Criterion 5 says every value of the secrets file is scrubbed. `secret_values()` scrubs only the named keys `OPENCODE_GO_KEY` and `GLM_KEY` regardless of length. It scrubs any other value only if it is at least `FRAGMENT` (8) characters long. A short credential under another key (for example `FOO_TOKEN=abc123`) is not scrubbed from a reviewer's answer, failure line or stderr. The 8-character cut-off is a design choice the code comments justify, but it falls short of the criterion as written. Either narrow the criterion text to "at least the two named keys, plus any value of 8 or more characters", or scrub whole short values of keys whose names look like credentials. | Sonnet 5.5 | fixed — tests/test_stage2.py::test_a_short_value_of_a_credential_named_key_is_scrubbed | — |

Phase 6 verdict: sonnet-5.5 sub-agent, 2026-10-26

## Phase 4b — loop rows, released 2026-10-26

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | BLOCKER | SPEC | base | `scripts/stage2.py` — `launch()`'s `finally: _LIVE_GROUPS.discard(process.pid)`, with `main()` and `kill_live()` | An interrupted or SIGTERM'd call is not killed when the interrupt lands inside `launch()` itself, which is the case for every main-thread call (`make verify`, the red-first runs, the tool and pinned-pi calls). The exception unwinds through `launch`'s own `finally` before the handler in `main()` runs, so the process group is deregistered first and `kill_live()` then signals nothing; the child (its own session, so the terminal's Ctrl-C does not reach it either) keeps running after the runner exits. On SIGTERM it is worse: `Popen.__exit__` waits for the child for every exception but `KeyboardInterrupt`, so the runner blocks in `wait()` and exits 143 only after the launched program has ended on its own. The two new tests pass only because they call `launch` in a worker thread, where the registration outlives the main thread's interruption; a test that raises `KeyboardInterrupt` from the main thread inside `launch` (or SIGTERMs the runner while it runs `make verify`) shows the launched program still alive after `main()` returns. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group | yes — tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group | agree |
| L1-2 | MAJOR | MAINT | base | `scripts/stage2.py` — `review_loop()`, the `except Refused` around the replacement's `checked_prompt` call | The broad `except Refused` also swallows the mandatory leak check: `checked_prompt` raises the same exception when the leak check is not clean or cannot run, and the loop reports it as `<id> not admitted: …`, tries the next rung and still writes the round, so a leak-check refusal that used to abort the whole run (exit 2) now ends in exit 0 with a note that blames the declaration. A test that makes `leakcheck.check` refuse for a replacement's prompt shows the round written and the run green instead of the run refusing. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_a_leak_refusal_for_a_replacement_stops_the_run | yes — tests/test_stage2.py::test_a_leak_refusal_for_a_replacement_stops_the_run | agree |
| L1-3 | MAJOR | MAINT | base | scripts/stage2.py, launch: the finally that discards _LIVE_GROUPS | The process group is unregistered while the interrupting exception is still inside the `with process` block, so by the time main's handler calls kill_live that group is no longer tracked and only the group leader dies (Popen's cleanup kills the pid, not the group). An interrupt or SIGTERM landing while a timed program runs on the main thread — catalog discovery's `--list-models` call, a leak check, a verification run — therefore leaves the group's other processes running after the runner exits, which is the leak this change promises to close. The new test interrupts only while launch runs in a second thread, where the group is still registered, so the failing path is uncovered. | mimo-v2.5 | fixed — tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group | yes — tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group | agree |
| L1-4 | MINOR | SPEC | base | scripts/stage2.py, review_loop: the replacement block after run_swarm | Criterion 9 promises a replacement whose launch the deadline prevents "writes no call line and is not consumed", but the call line is appended to the findings file before the run, and only afterwards does `remaining` refuse the call and the runner note it "did not start". The change's own known-limits note admits the line can still be written, so the promised behaviour is not what the code does. | mimo-v2.5 | fixed — not a test — criterion 9 now acknowledges a call line written before launch is refused by the deadline. | no — not a test | agree |
| L1-5 | MINOR | MAINT | base | scripts/stage2.py, dropped_notice and free_drops | Only a pipe is escaped when a dropped catalog id is named. An id dropped as "not a plain model id" is by definition outside the id charset and may carry control bytes — catalog parsing splits on whitespace, and such bytes are not whitespace — so it reaches stderr and the loop record verbatim apart from pipes; the charset comment promises third-party text never carries other markup into the record's cells. | mimo-v2.5 | fixed — tests/test_stage2.py::test_a_dropped_catalog_id_carries_no_control_bytes | yes — tests/test_stage2.py::test_a_dropped_catalog_id_carries_no_control_bytes | agree |
| L1-6 | MINOR | MAINT | base | scripts/stage2.py, activate_overlay | The shell of a definition crosses even when nothing allowed survives it: a definition with no allowed field and no provider equal to the store's key is written into models.json as an empty model object, and its dropped-fields report is keyed by the id `None`, so two such definitions overwrite one entry. Catalog text is precisely the untrusted input this change reasons about; such a definition should be dropped whole and named by its position. | mimo-v2.5 | fixed — tests/test_stage2.py::test_a_malformed_catalog_definition_is_dropped_whole_and_named | yes — tests/test_stage2.py::test_a_malformed_catalog_definition_is_dropped_whole_and_named | agree |
| L1-7 | MINOR | MAINT | base | scripts/stage2.py, free_drops beside select_free | The suffix/include/exclude candidate matching is written twice, once here and once in select_free, and the drop list and the selection only describe the same candidates while both copies agree. A rule dimension later added to one and not the other silently names nothing or drops the wrong id, and nothing in the tests pins the two to each other. | mimo-v2.5 | rejected — duplicated matching rules between `free_drops` and `select_free` is style; no input makes them disagree today; named as an accepted limit (orchestrator, 2026-10-26) |  | agree |
| L1-8 | MINOR | MAINT | base | scripts/stage2.py — `select_free` and `free_drops` | The maintainer's exclusion is enforced only inside `free_drops`, which `discover_free` consults; `select_free` itself still returns an id an `ausgeschlossen` entry names. Any caller of `select_free` (today `discover_free` filters afterwards, tomorrow anything else, including a state restore that re-derives the selection) silently admits an excluded free id, and the two functions now carry duplicate copies of the provider/suffix/include/exclude matching rules that can drift apart. | mimo-v2.6-flash | rejected — `discover_free`, the only caller, applies the exclusion; a future caller is speculative; the duplication is L1-7 (orchestrator, 2026-10-26) |  | agree |
| L1-9 | MINOR | MAINT | base | scripts/stage2.py — `FROM_LINE`, `_record_lines`, the `From {member}:` write in `review_loop` | The attribution line is written with the member id verbatim, but `_record_lines` only recognises it when it matches `[A-Za-z0-9][A-Za-z0-9._:/-]*`. Paid ids come from `modelle` in `model-endpoints.yaml` and are never validated against that charset, so a declared id holding `+`, a space or a `#` makes the runner's own `From …:` line fail the match: the line is then read as the previous member's words, the following kept block loses its `reviewer = False` switch, and every later block in that round is attributed to the wrong member with no error. | mimo-v2.6-flash | rejected — every id `model-endpoints.yaml` declares today matches the `From` charset, and the file is human-decided; no reachable input breaks the attribution (orchestrator, 2026-10-26) |  | agree |
| L1-10 | MAJOR | MAINT | base | scripts/stage2.py — `secret_values()`; plans/changes/review-loop-deep-b/decisions.md, "What a secrets-file value is" | Every secrets-file value of 8 or more characters is scrubbed from answers, failure lines and stderr. The file is an env file, not a key-only file: a non-credential entry such as `BASE_URL=[credential]…`, `HOME=/Users/…` or `MODEL=deepseek-v4.1-flash` is 8 characters or longer and is replaced everywhere in the record, so a reviewer's finding about that path or model is rewritten into `[credential]` and the evidence is destroyed before anyone reads it. The stated rationale only rules out short flag values; it never examines long non-secret ones. | mimo-v2.6-flash | rejected — decisions.md [DETAIL] "What a secrets-file value is": the secrets file holds keys; scrubbing a long value is the safe direction, and no declared entry is a non-credential (orchestrator, 2026-10-26) |  | disagree — phase 6 raised F6-2: criterion 5 as written promises every secrets-file value, so the rejection rests on a detail the criterion does not carry |
| L1-11 | MINOR | SPEC | base | plans/changes/review-loop-deep-b/spec.md — criterion 9 vs "Known limits"; scripts/stage2.py — replacement loop in `review_loop` | Criterion 9 promises that a replacement the deadline prevents "writes no call line and is not consumed", while the same document's Known limits and the code admit that a call line can still be written for a replacement that `remaining()` then refuses (only the note "did not start" and non-consumption follow). The change's own spec states an absolute it does not deliver in that window; its refutation clause mentions only consumption, so the mismatch is invisible unless both sections are read together. | mimo-v2.6-flash | fixed — not a test — criterion 9 now matches the documented deadline window and non-consumption behavior. | no — not a test | agree |
| L1-12 | MINOR | MAINT | base | scripts/stage2.py — `activate_overlay` | A definition that is not a dict is skipped with a bare `continue`: it never reaches `models.json` and it is never put into the returned `dropped` map, so nothing is printed on stderr. Criterion 13 requires every field (and by its wording every dropped item) to be named at discovery; a malformed catalog entry disappears from the active configuration silently, and the next reader cannot tell whether the catalog never held it or activation threw it away. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_malformed_catalog_definition_is_dropped_whole_and_named | yes — tests/test_stage2.py::test_a_malformed_catalog_definition_is_dropped_whole_and_named | agree |
| L1-13 | MINOR | MAINT | base | scripts/stage2.py — `kill_live`, `_LIVE_GROUPS`, `main`'s `KeyboardInterrupt`/`SIGTERM` handler | The live groups are signalled once, from `main`, at the moment the interrupt lands; registration happens after `Popen` returns. `run_swarm` runs members in threads, so a worker that enters `launch` after `kill_live` has snapshotted the set registers a group that is never signalled, and nothing afterwards re-runs the kill or joins the workers before the runner exits. Criterion 6 promises every running timed program is killed before the exit, but under that interleaving a reviewer program outlives the interrupted runner. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_launch_after_the_interrupt_starts_no_program | yes — tests/test_stage2.py::test_a_launch_after_the_interrupt_starts_no_program | agree |
| L2-1 | BLOCKER | SPEC | impl | scripts/stage2.py `_record_lines` | The branch `elif reviewer and FROM_LINE.fullmatch(line)` sets `reviewer = False` but never appends the `From <member>:` line to `lines`. After the first member, whose `From` line is written while `reviewer` is still `False` and reaches the `else` clause, every later member reaches this branch with `reviewer=True` and is dropped. With two or more members that keep non-row words, `kept_lines` loses the second member's `From` line and its words, so criterion 4 (DL-B-3) and its test `test_each_kept_block_names_its_member` fail: the assertion `"From beacon-2-free:" in own` does not hold. | longcat-2.0 | rejected — the `From` branch has no `continue`, so it falls through to `lines.append((line, reviewer))` with reviewer False and the line stays; test_each_kept_block_names_its_member passes (orchestrator, 2026-10-26) |  | agree |

Rounds run: 2

Record digest: sha256:283273be1907dbbea907e2adcc38d8e767294b4883de7b835809cef2a5699170

Record identity: sha256:066bd741b42447be7732e2704d6f3799e22bd22773d08995a442e727bf898ebc

Loop state: {"availability": {"checked_at": "2026-10-26T00:09:26+00:00", "failed": {"cat-jam-free": "pi call failed: exit 1 (400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model is unavailable.\"})", "longcat-2.5-preview-free": "pi call failed: exit 1 (429: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Endpoint is unavailable.\"})", "mimo-v2.5-pro": "pi call failed: exit 1 (400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: [400] Unsupported model mimo-v2.5-pro\"})"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "skipped": {"gemini-4-argon-contributor": "not admitted; data terms have not been read", "gpt-5.6-luna": "not admitted; data terms have not been read", "grok-4.6": "not admitted; data terms have not been read", "grok-4.7": "not admitted; data terms have not been read", "kimi-k2.7-code": "not admitted; data terms have not been read", "kimi-k3": "not admitted; data terms have not been read", "minimax-m2.7": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "space-bunny": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)"]}, "consumed": ["flash", "rung:longcat-2.0"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "big-pickle", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-flash", "provider": "opencode"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "exo-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "ling-3.0-flash-fin-free", "provider": "opencode"}, {"model": "ling-3.1-flash-free", "provider": "opencode"}, {"model": "longcat-2.5-preview-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-spark-1.3-contributor-free", "provider": "opencode"}, {"model": "nemotron-3-ultra-free", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "space-bunny-free", "provider": "opencode"}, {"model": "step-5-preview-free", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-flash", "provider": "opencode-go"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon-contributor", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.6", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-preview-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m2.7", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "space-bunny", "provider": "opencode-go"}, {"model": "step-5-preview-free", "provider": "opencode-go"}], "checked_at": "2026-10-26T00:07:45+00:00", "dropped": {}, "models_store": {"opencode-go": {"checkedAt": 1792973264638, "etag": "W/\"65e1c3b71054c3b1741fe4cb46560dbf\"", "lastModified": 1792068066000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "cat-jam-free", "input": ["text"], "maxTokens": 131072, "name": "Cat Jam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"forceAdaptiveThinking": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro (New)", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/v1", "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 0, "input": 4, "output": 20}, "id": "gemini-4-argon-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.6", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.6", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 0, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "LongCat 2.5 Preview Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 204800, "cost": {"cacheRead": 0.06, "cacheWrite": 0.375, "input": 0.3, "output": 1.2}, "id": "minimax-m2.7", "input": ["text"], "maxTokens": 131072, "name": "MiniMax-M2.7", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "space-bunny", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 524288, "name": "Space Bunny", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "step-5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "overlay": ["cat-jam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon-contributor", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.6", "grok-4.7", "hy3", "hy4-preview", "kimi-k2.7-code", "kimi-k3", "longcat-2.0", "longcat-2.5-preview-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m2.7", "minimax-m3", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "space-bunny", "step-5-preview-free"], "pi_version": "1.2.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "rungs": ["longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"]}}

Kept from the loop record:

> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured).
> Notice: in the live catalog without a terms reading: gemini-4-argon-contributor, gpt-5.6-luna, grok-4.6, grok-4.7, kimi-k2.7-code, kimi-k3, minimax-m2.7, muse-spark-1.2-contributor, muse-spark-1.3-contributor, space-bunny.

<!-- End of released loop record -->

Stage-2 call, 2026-10-26: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason maintainer: Sonnet replaces Codex for two hours (2026-10-26) · leak check clean over 619 files, 2266 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +18 -8
> - `tests/test_stage2.py` +17 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F6-1: several fixed lines
> - F6-2: several fixed lines
> ```

Stage-2 call, 2026-10-26: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason maintainer: Sonnet replaces Codex for two hours (2026-10-26) · leak check clean over 619 files, 2270 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +23 -10
> - `tests/test_stage2.py` +18 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`.
> - F6-1: several fixed lines
> - F6-2: several fixed lines
> ```

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 619 files, 2273 commits, 12 rules.

Stage-2 call, 2026-10-27: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 682 files, 2318 commits, 12 rules.

## Phase 6 — Codex, 2026-10-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-3 | MAJOR | SPEC | base | scripts/stage2.py:1917–1919 | A refreshed catalog containing `bad id-free` aborts discovery before invalid IDs are dropped. Reproduced with pinned Pi’s real `listModels`: alongside `acme-v1-free`, the spaced ID produces a row that `parse_catalog` refuses with “wrong column count”. The invalid ID is never named as dropped, and valid reviewers cannot proceed. Validate catalog IDs before activating and listing them. [Criterion 8] | Codex | fixed — tests/test_stage2.py::test_catalog_drops_an_invalid_id_before_listing | — |
| F6-4 | MINOR | SPEC | base | scripts/stage2.py:7058–7061 | Retained malformed answers bypass the new attribution boundary. Reproduced with acme returning prose, then valid rows, while beacon returns rows plus commentary: the record contains only `From beacon-2-free:`, followed later by acme’s malformed answer without its own boundary. `_record_lines` consequently classifies the runner’s “acme-v1-free’s first answer…” label as reviewer text. Every retained block needs the promised attribution and classification. [Criterion 4] | Codex | fixed — tests/test_stage2.py::test_every_retained_answer_block_carries_its_attribution | — |
| F6-5 | MINOR | MAINT | base | tests/test_stage2.py:14231–14237 | The worker-interruption tests cannot detect surviving children on macOS: `_child_alive` reads Linux’s `/proc/<pid>/stat` and returns `False` when that file is unavailable. Both tests therefore accept a live child even if `kill_live` stops sending signals. The later main-thread tests exercise cleanup inside `launch`, leaving this worker cancellation path without an effective macOS assertion. | Codex | fixed — not a test — Portable Prozessprüfung und Test-Einsprungpunkt korrigiert; beide Unterbrechungstests erkennen ausbleibende Kill-Signale. | — |

Phase 6 verdict: codex 01a17c8f-5534-7a93-a2ae-7fcdc25203f6, 2026-10-27
Reviewer session: codex 01a17c8f-5534-7a93-a2ae-7fcdc25203f6 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 682 files, 2319 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +20 -9
> - `tests/test_stage2.py` +106 -3
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 208 lines of this gate left out …]
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-613/popen-gw6...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-613/popen-gw6/test_a_launch_after_the_interr0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10a6b3980>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-613/popen-gw6/test_a_launch_after_the_interr0')
>
>     def test_a_launch_after_the_interrupt_starts_no_program(world: World, monkeypatch, tmp_path: Path) -> None:
>         """A worker released after main has handled the interrupt cannot start another program."""
>         release = threading.Event()
>         errors = []
>         marker = tmp_path / "late"
>     
>         def worker():
>             release.wait()
>             try:
>                 stage2.launch(
>                     [sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).write_text('started')"],
>                     tmp_path,
>                     dict(os.environ),
>                     timeout=2,
>                 )
>             except stage2.NotStarted as error:
>                 errors.append(error)
>     
>         thread = threading.Thread(target=worker)
>         thread.start()
>     
>         def verb(*_args):
>             raise KeyboardInterrupt
>     
>         monkeypatch.setitem(stage2.VERBS, "explore", verb)
>         try:
> >           with pytest.raises(KeyboardInterrupt):
> E           Failed: DID NOT RAISE <class 'KeyboardInterrupt'>
>
> tests/test_stage2.py:16216: Failed
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: claude call failed: the answer is empty
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=68707) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/review-loop-deep-b/tests/test_stage2.py:14828: DeprecationWarning: This process (pid=68701) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group[KeyboardInterrupt]
> FAILED tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group[Terminated]
> FAILED tests/test_stage2.py::test_a_launch_after_the_interrupt_starts_no_program
> 3 failed, 3872 passed, 17 skipped, 5 warnings in 441.97s (0:07:21)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 18983 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/review-loop-deep-b/stage2/attempts/review-loop-deep-b/attempt-1-20261027T085802344872Z-912aac32.md
> ````

Stage-2 call, 2026-10-27: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 682 files, 2320 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +2 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F6-5: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/review-loop-deep-b/stage2/attempts/review-loop-deep-b/attempt-2-20261027T085802344872Z-912aac32.md
> ```

Stage-2 call, 2026-10-27: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 682 files, 2323 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F6-5: tests/test_stage2.py::test_worker_interruption_leaves_no_live_child: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/review-loop-deep-b/stage2/attempts/review-loop-deep-b/attempt-3-20261027T085802344872Z-912aac32.md
> ```

Stage-2 call, 2026-10-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 682 files, 2326 commits, 12 rules.

Stage-2 call, 2026-10-27: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 682 files, 2331 commits, 12 rules.

## Phase 6 — Codex, 2026-10-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-6 | MINOR | MAINT | base | scripts/stage2_availability.py:1234,1199 | A catalog ID such as `bad\x1b[2J-free` is correctly dropped and escaped in discovery’s notice, but `prepare-loop` copies the raw ID into `availability.skipped`. `report()` then prints its terminal control bytes unchanged. Reproduced: the report contains an actual ESC followed by `[2J`, which clears the terminal. Escape control characters when rendering the availability report. | Codex | fixed — tests/test_stage2_availability.py::test_availability_report_escapes_control_characters_in_skipped_ids | — |

Phase 6 verdict: codex 01a17d07-19ba-7210-a12b-fba92364057b, 2026-10-27
Reviewer session: codex 01a17d07-19ba-7210-a12b-fba92364057b — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 682 files, 2332 commits, 12 rules.

Stage-2 call, 2026-10-27: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 682 files, 2336 commits, 12 rules.

## Phase 6 — Codex, 2026-10-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-7 | BLOCKER | SPEC | impl | scripts/stage2.py:1828–1850,2308–2309 | The catalog allowlist fails open when an allowed field invalidates Pi’s configuration. Reproduced with `name: ""`, `samplingParams: {"model":"kimi-k3"}` and a catalog date newer than Pi’s shipped data: activation reports the forbidden fields dropped, but Pi rejects `models.json` and restores the unfiltered `models-store.json`. Pi’s real resolver selects `synthetic-free`, while its request builder produces `model: "kimi-k3"` and restores catalog headers. Dropped fields must remain unavailable when explicit configuration fails. [Criterion 13] | Codex | taken — test: tests/test_stage2.py::test_catalog_allowlist_fails_closed_when_pi_rejects_the_overlay — when Pi does not accept the filtered models.json (or resolves a model or field it did not contain), the run refuses before any reviewer call and never falls back to the unfiltered models-store.json; a field that can redirect the request (for example a model inside samplingParams) is not on the allowlist (maintainer, 2026-10-27: repair; the free swarm is paused until this PR merges) | — |
| F6-8 | MAJOR | SPEC | impl | scripts/stage2.py:864–882 | A termination signal during process creation can leave the timed program running. Reproduced by delivering real SIGTERM immediately after `_fork_exec` creates a sleep child, before `Popen` returns: `process` remains `None`, cleanup skips it, and no process group was registered. The actual runner entry point returns 143 reporting zero groups killed, while `waitpid(..., WNOHANG)` confirms the child still runs. Cancellation must also cover the interval between child creation and registration. [Criterion 6] | Codex | taken — test: tests/test_stage2.py::test_a_signal_during_process_creation_leaves_no_child — the child is registered (or the signal deferred) before it can outlive a termination signal, so cancellation reaches it (maintainer, 2026-10-27: repair; the free swarm is paused until this PR merges) | — |

Phase 6 verdict: codex 01a17d2e-551e-7b30-b4bc-b8bab59ba680, 2026-10-27
Reviewer session: codex 01a17d2e-551e-7b30-b4bc-b8bab59ba680 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
