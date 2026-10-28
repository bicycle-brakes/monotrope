---
title: "Research — reviewer-inner-rounds"
status: draft
implementation_status: none
date: 2026-10-21
last_reviewed: 2026-10-21
updated: 2026-10-21
supersedes: null
superseded_by: null
bead: coding-harness-py5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, review-loop, pi, codex, adr-0021]
---

# Reviewer inner rounds — Research

Phase 1 for bead coding-harness-py5, read against `origin/main` at `c3196a2`
on 2026-10-21 (worktree `reviewer-inner-rounds`). The bead asks that each
reviewer call continue, in its own context, for two more rounds after its first
answer ("Review again. Your findings so far are above. Find what you missed; do
not repeat a finding."), and that the runner collect rows only after inner
round 3. This file records what exists; it designs and recommends nothing.

Notation: "inner round" is a turn inside one reviewer's context; "loop round"
is a round of ADR 0021 (`L<n>-<m>` ids). "Not read" means a source was not
opened; "not found" means it was searched for and absent.

Pinned Pi was installed in the worktree with `bash tools/pi/install.sh`;
`tools/pi/pi --version` printed `1.2.0`, the pin in `tools/pi/package.json`.
No model was called. No flag below was run against a model; every Pi statement
is from the pinned install's docs and `dist/` source, every Codex and Claude
statement from `--help` output and `scripts/stage2.py`.

## 1. What exists today

### 1.1 The review loop in the runner (phase 4b)

- `review_loop()` in `scripts/stage2.py` completes one loop round per call. It
  builds one prompt per member (`prompt_for`), checks every prompt in the
  parent (`checked_prompt`, the leak check), then calls `run_swarm()` for the
  stage's members. The stages are the free swarm (`kind: free`, tools off), the
  Flash swarm (`kind: paid-swarm`) and one ladder rung per later round.
- `run_swarm()` starts one thread per member; each calls `run_reviewer()` once
  and parses the answer with `parse_rows()`. A member succeeds when its answer
  holds six-cell rows or is exactly `No finding.`; anything else raises
  `CallFailed` ("malformed finding output"). A failed Flash member is replaced
  by the cheapest unconsumed ladder model (`review_loop`, ADR 0021 decision 4).
- `review_loop()` numbers the rows: for every succeeding member in order it
  assigns `L<round>-<running count>` itself and discards the id the model wrote
  (`ident = f"L{round_number}-{len(numbered) + 1}"`), writes the member's name
  into the `Reviewer` column, and leaves `Status` and `Broke a test` empty. The
  round heading is `## Round <n> — <members>, <date>` in the loop record
  `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`.
- `ROW_COLUMNS` (`scripts/stage2.py`) is `ID, Severity, Dimension, Origin,
  Where, Finding, Reviewer, Status, Broke a test`. `round_rows()` selects a
  round's rows by the `L<n>-` id prefix; `clean_round()` is true when no row of
  the round is accepted (`taken`/`fixed`) and none is undecided;
  `taken_in_round()` and `fix_r_only()` (the repair brake) use the same prefix.
- Prompts: `prompts/04b-review-loop.md` (paid rounds) and `FREE_REVIEW_BODY`
  (free round, in `scripts/stage2.py`) plus `ANSWER_FORMAT` and `READ_REQUEST`.
  Each call is one prompt, once; no prompt today mentions an earlier answer.
- Free members get `--no-tools` and the scratch directory as working directory;
  their only input is the implementation diff, capped by `FREE_DIFF_MAX_LINES`
  (400 per file) and `FREE_DIFF_MAX_TOTAL` (2000). Paid members get
  `--tools read,grep,find,ls` (`PI_TOOLS`) and the worktree; the paid diff is
  unbounded on `main` (open pull request #191 bounds it, §4.5).
- Each reviewer call has a limit: `REVIEWER_MINUTES = 30`, passed to `launch()`
  as the whole process's timeout.

### 1.2 How Pi is invoked for a reviewer

`run_reviewer()` in `scripts/stage2.py` builds this argv (through
`tools/pi/pi`, the repository wrapper, ADR 0019): `--print --no-session
--no-approve --no-extensions --no-mcp --no-skills --no-context-files
--no-prompt-templates --no-themes --offline`, then `--no-tools` (free) or
`--tools read,grep,find,ls`, `--thinking max`, `--model opencode-go/<id>`,
`--append-system-prompt <scratch>/review-prompt.md`, and one task string
(`Review the change <change> as the appended instructions say.`) as the single
positional message. Each call gets a fresh `HOME`, an agent directory with
`settings.json` (`{"retry": {"enabled": false}}`) and the run's overlay, and
the key only as `OPENCODE_API_KEY`. The call returns the process's stdout,
scrubbed; a nonzero exit or an empty stdout raises `CallFailed`.

Tests pin this exactly. `tests/test_stage2.py` has `PI_FLAGS` (the ten fixed
flags, in order) and `test_the_review_loop_launches_pi_isolated`, which asserts
the option list equals `[*PI_FLAGS, "--append-system-prompt"]` and asserts that
`--mode`, `--api-key`, `--approve`, `-p`, `--resume` and `--restricted` are not
in the argv. `tests/test_pi_contract.py` (with `tests/pi_contract_driver.mjs`)
starts the real pinned Pi against a loopback stand-in and measures the flag set
offline.

### 1.3 What the pinned Pi 1.2.0 offers for more than one turn

Read in `tools/pi/node_modules/@earendil-works/pi-coding-agent/` (docs: `docs/cli.md`,
`docs/sessions.md`, `docs/json.md`, `docs/rpc.md`, `docs/cli-integration.md`,
`docs/compaction.md`; source: `dist/modes/print-mode.js`,
`dist/cli/initial-message.js`, `dist/main.js`):

- **Several messages in one print run share one session.** `cli.md` documents
  `pi [options] [--] [@files...] [messages...]` and says `--print` "run[s] the
  supplied prompts". `dist/cli/initial-message.js` (`buildInitialMessage`) takes
  `parsed.messages[0]` as the initial message and shifts it off; `runPrintMode`
  in `dist/modes/print-mode.js` then awaits `session.prompt(initialMessage)`
  and `await session.prompt(message)` for every remaining message, in order,
  on the same `session`. With `--no-session` the session is "in-memory ... not
  persisted" (`cli.md`, `sessions.md`), so the history still accumulates in
  memory across the messages. Not run against a model: that two later messages
  see the first answer is read from the source, not measured.
- **Text mode prints only the last assistant message.** After the loop,
  `runPrintMode` in `text` mode writes the text blocks of
  `session.state.messages[length - 1]` only (when its role is `assistant`). A
  stop reason `error` or `aborted` sets exit code 1 and prints the error to
  stderr instead; `length` prints the partial text and exits 1. So today's
  `--print` text mode would return round 3's answer alone, and would discard
  rounds 1 and 2 when any later message fails. `--mode json` "run[s] the
  supplied prompts, write[s] JSONL events to stdout, then exit[s]" (`cli.md`,
  `json.md`) and emits `message_end` events with the assistant message per
  turn and `agent_end` with the messages; that would carry every turn's answer
  (read in `docs/json.md`; not run). The existing contract test refuses `--mode`
  in the argv; the documented JSON event shapes were not compared with the
  runner's parser, which reads plain stdout.
- **The follow-up texts are fixed at launch.** Every message is an argv entry;
  the runner cannot let turn 2's text depend on turn 1's answer, and cannot
  stop after turn 1 or 2, in one print process. The bead's follow-up text is
  constant, so the first limit is not binding for it; the second is (§3).
- **Other ways to keep a context:** `--mode rpc` ("read[s] JSONL commands from
  stdin ... until shutdown", `rpc.md`, `rpc-commands.md` not read in full) would
  let the runner send turn N+1 after reading turn N; `--session-dir <dir>` plus
  `--session-id <id>` / `--continue` / `--session <path|id>` (`cli.md`) would
  persist a session between separate `pi --print` processes (`--continue` is
  "most recent session for the current project"; `--session-id` "creates it if
  absent" and "cannot be combined with `--session`, `--continue`, or
  `--resume`"); the SDK (`docs/sdk.md`, not read) is in-process Node. None of
  these is used by the runner today.
- **Context size.** `docs/compaction.md` states that Pi auto-compacts when
  context passes `contextWindow - reserveTokens` (default reserve 16384 per the
  text quoted in open pull request #191, which cites `docs/compaction.md` and
  `dist/core/agent-session.js`; the lines were not re-read here). Each turn
  re-sends the active branch (`docs/sessions.md`: "The active branch ... supplies
  conversation history for the next model request"), so turn 3 carries the
  prompt, the diff, turn 1, turn 2 and any tool results.
- `pi --list-models` / `pi update --models` are unaffected (the free-stage
  discovery) and `scripts/stage2_availability.py` probes are static, tool-free
  and not reviews; neither is a reviewer call in the bead's sense.

### 1.4 Codex reviews (phase 6, and phase 2a on a Codex route)

- `run_codex()` in `scripts/stage2.py` runs `codex exec [resume <thread>]
  --json -m gpt-6.1-sol -c model_reasoning_effort=... -c sandbox_mode=...
  --disable hooks --disable memories -o <answer file> <prompt>` and returns
  `(answer, thread_id)`; the thread comes from the `thread.started` event
  (`thread_id()`). A resumed call is a new process on a stored thread.
  `codex exec resume --help` (codex-cli 0.163.0) confirms `resume [SESSION_ID]
  [PROMPT]`. A docstring in `run_codex` states that a resumed thread "actually
  runs at that effort inside Codex is not asserted" (bead coding-harness-yzk).
- `review()` (phase 6) already uses two turns in one thread: the verdict call
  (`run_codex(..., resume=recorded, verb="review")`, with `recorded` the phase-2a
  Codex session when one exists, else fresh), then, after `release()`, the loop
  marks call `run_codex(marks_prompt, resume=thread, verb="review")` in the
  same thread. The line `Phase 6 verdict: codex <thread>, <date>` is written
  before the loop rows are read; `SESSION_LINE` matches `Reviewer session:
  codex <id>`. A phase-6 re-check starts a fresh session (`recheck`).
- `spec_review()` (phase 2a) calls `run_work_model()` with Opus 5.5: `claude -p
  ... --tools <read tools> --restricted --safe-mode --strict-mcp-config
  --permission-mode dontAsk --permission-prompts none --no-session-persistence
  --output-format text`. It keeps no session ("the reviewer is recorded by the
  rows alone"); `recorded_2a_session()` returns no session for an `Opus 5.5`
  block. `claude --help` (2.1.305) lists `-r/--resume`, `--session-id <uuid>`,
  `-c/--continue`, `--fork-session`, `--input-format` and says
  `--no-session-persistence` "only works with --print". Whether a `-p` call
  with a session id can be resumed under `--restricted --safe-mode` and
  `--no-session-persistence` removed was not run: not read.
- Rows of 2a and 6 go straight into `plans/changes/<name>/findings.md` as
  `## Phase 2a — ...` / `## Phase 6 — ...` blocks written by `answer_block()`
  with the reviewer name (`Opus`, `Codex`); they do not pass the loop record.

### 1.5 Budget and cost data

- `model-endpoints.yaml`, entry `opencode-go` (`modelle_terms`, `anfragen_5h`
  read from the Go page's "Estimated requests" table on 2026-10-17;
  `anfragen_quelle: https://opencode.ai/docs/go`): deepseek-v4.1-flash 34670,
  mimo-v2.6-flash 30100, longcat-2.0 11400, glm-5.3-flash 6320, qwen3.8-flash
  5400, gpt-6-luna 4230, claude-haiku-5-5 3850, mimo-v2.6-pro 3250, minimax-m3
  3200 (requests per 5 hours; the runner orders the ladder by it, descending).
  Retention: `0 days` except gpt-6-luna and claude-haiku-5-5 at `30 days`;
  training "Not used" for all nine. The Go page itself was not re-read; the
  meaning of one "request" for a call with tool use (one per model API call, or
  per prompt) is not stated in the repository: not found.
- `availability_preflight` sets `flash_size: 3` and `max_age_seconds: 900`; the
  Flash swarm is the three cheapest reachable admitted paid models; the
  `flash_swarm` list (deepseek-v4.1-flash, mimo-v2.6-flash, longcat-2.0) is
  legacy. The free swarm's member count F comes from the live catalog and is
  not constant.
- ADR 0021 decision 8 bounds a completed run at one review call per free member
  and one per eligible paid model: with nine paid models at most eight
  completed rounds and `F + 9` member calls. Probes and failed attempts are
  extra audited calls; "no new money cap is claimed". With three turns per call
  the turn count of that bound is `3 × (F + 9)`; a measured count of Pi model
  requests per turn (one for a no-tool free call; more for a paid call with
  tools) was not found in the repository.
- Free members are subject to no per-model terms reading and their cost is not
  measured ("the check proves which catalog was read, not what OpenCode Go
  bills", WORKFLOW.md §4).
- Time: one process per call under one 30-minute limit (`REVIEWER_MINUTES`);
  swarm members run concurrently, so turns multiply wall time per member, not
  per swarm.

## 2. Evidence of yield

### 2.1 The maintainer's observation

Bead coding-harness-py5: on 2026-10-20 the maintainer observed that DeepSeek 4.1
Flash "keeps finding new errors round after round" on the research-swarm review
loop. The bead's own acceptance asks for a measurement of new findings per
inner round on one change. The until-clean loop's "measure first" memory
(bead coding-harness-4fk) names rounds/time/phase-6 findings to be measured on
two or three changes after merge; the repository holds no such measurement that
this exploration read: not found in the files read, and the memory file
itself was not opened.

### 2.2 The 19-pass review of the review-swarm runner (open pull request #184)

Source: `docs/journal/handover/2026-10-20-review-swarm-runner-review.md` on
branch `docs/handover-2026-10-20-review-swarm-runner-rounds` (fetched,
read with `git show FETCH_HEAD:...`; section "Addendum — 2026-10-20, review
passes 2 to 19"), plus the body of pull request #184 (state OPEN on 2026-10-21).

What the file says:

- The first pass (reviewed `59630b7`) found R-1 to R-13 (thirteen findings).
  Passes 2 to 19, reviewed at `94ae6cc`, found R-14 to R-28 (fifteen new
  findings). The addendum text says "seventeen further read-only passes" and
  "Six of the seventeen passes found nothing new"; the table in the same
  section lists eighteen rows (passes 2 to 19). The two counts differ by one
  pass; the discrepancy is in the source.
- Per the table, passes with **no new R-number** are: 2 (R-4, R-5 "already
  reported", negative results), 11, 12, 14, 15, 16, 18 ("in order") and 13
  (R-11 "documented", an earlier finding). The six "found nothing new" the
  text counts are passes 11, 12, 14, 15, 16, 18; pass 2 and pass 13 also add
  no new number. Passes with new numbers: 4 (R-14), 5 (R-15), 6 (R-16, R-17,
  R-18), 7 (R-19, R-20), 8 (R-21, R-22), 9 (R-23, R-24), 10 (R-25, R-26),
  17 (R-27), 19 (R-28) — fifteen in all (pass 3 yielded R-13, counted in the
  first batch).
- Severity by pass: the six MAJOR findings of the addendum come from passes
  4 to 8 (R-14, R-15, R-16, R-19, R-21, R-22); passes 9, 10, 17 and 19
  produced only MINOR or "note" rows (R-23 to R-28). The text says "from pass
  14 on the yield of that method drops visibly" and recommends stopping the
  review and starting repairs. Two of the late "new" rows (R-24, R-28) are notes.
- **What the data does not measure.** The passes are not the bead's
  mechanism. Each pass covers a different slice (governance, parsing, commit
  path, prompts, ...) as the table's "Slice" column shows; the addendum's
  "Where the review stands" table does not say whether a pass ran in a fresh
  context or the previous pass's, and which model ran each pass is not stated
  in the sections read (the cut-off statement says "no foreign model was
  called"). The data therefore shows a diminishing yield of successive
  differently-scoped passes by (apparently) one reviewing session; it does not
  show the yield of repeating the same prompt over the same input in one
  context, which is what the bead proposes. Findings were also verified or
  reproduced by that reviewer (R-23, R-25, R-26 "reproduced"), unlike a Flash
  model's unverified rows.
- The same addendum records stale and corrected earlier findings (R-13 "half
  wrong", R-9 "narrower than written"): later passes also corrected earlier
  rows, so later output includes retractions.

### 2.3 Other data in the repository about later rounds

- ADR 0021 context: "A clean first round still admits round 2" and the first
  night run refused a needed fourth round (`docs/journal/handover/
  2026-10-12-night-run-first-rehearsal.md`, section 4, cited by the ADR; the
  handover was not opened here).
- Bead coding-harness-6jg describes a round-2 swarm member (mimo-v2.6-flash,
  2026-10-15) whose seven rows were numbered `R2-1`…`R2-7`, of which "one of
  the seven rows was real and new" (raised as F-10 of research-swarm). That is
  one observation about a later round yielding one real finding in seven.
- `plans/changes/loop-until-clean/` (spec, design, findings, decisions) was
  not read beyond the `anfragen_5h` matches; any per-round yield figure there
  is not read.

## 3. Interactions

### 3.1 Row ids `L<n>-<m>` (bead coding-harness-6jg)

The bead (IN_PROGRESS, lease expired, interview note of 2026-10-16: "refuse —
a round whose answer holds row-shaped lines with non-conforming ids fails, and
the refusal names the ids; no renumbering") concerns a model writing ids other
than `L<n>-<m>`. In the code read here `review_loop()` replaces the id cell
with a runner-assigned `L<round>-<count>` for rows `parse_rows()` accepts, so
the 6jg refusal is not yet in `main`'s `review_loop` and its status in the
tracker is "in progress" (a branch for it was not looked up). With inner rounds
three answers per member exist; today's numbering is one running count per loop
round across members, and `round_rows()`/`clean_round()`/`taken_in_round()`/
`fix_r_only()`/`parse_marks()` (regex `L\d+-\d+`) /`REPAIR_ANSWER` all depend on
the shape `L<digits>-<digits>`. `release()` carries rows to `findings.md` "with
the reviewer its round had". A third id component, a second prefix or a
`Reviewer` suffix would each touch different readers; the readers named above
were identified by grep and not each read to the end.

### 3.2 The clean-round rule

`clean_round()` looks only at rows of the loop round (decided and none
accepted; no rows is clean). It is silent about how many answers a member gave
or whether a member said `No finding.`. If inner rounds 2 and 3 add rows under
the same loop-round id prefix, a loop round that is clean today (member said
`No finding.` at turn 1) could gain rows from turns 2 and 3 and no longer be
clean; if rows of inner rounds are decided and rejected they stay clean. The
free swarm ends the loop on a clean round before any paid review (ADR 0021
decision 1), so inner rounds at the free stage change how often that ends the
loop. The "malformed finding output" rule in `run_swarm()` (only table rows or
exactly `No finding.` pass) would apply to every inner answer; an inner round
that answers prose such as "nothing new" would fail the member under today's
rule, and a failure after a good turn 1 loses turn 1 in text mode (§1.3).
The repair brake (`fix_r_only`, two consecutive rounds of only `fix-r` rows)
and the ladder stop are per loop round and are not changed by inner rounds as
written.

### 3.3 Early stop

An early stop "when an inner round adds nothing" needs the runner to read turn
N before deciding turn N+1. One `pi --print` process with fixed positional
messages cannot do that (§1.3); RPC mode, separate processes on a stored
session, or the SDK could. A stop after turn 1 saves the later turns' requests;
whether the saved cost is material is not measured (no per-turn request or
token count exists in the repository: not found). What "adds nothing" means for
a free-text answer (exactly `No finding.`, zero rows, or only rows already
rejected) is not defined anywhere.

### 3.4 Duplicates

The follow-up text says "do not repeat a finding"; the runner has no
deduplication. WORKFLOW.md says duplicates "keep one row per member — reject
the copies explicitly, do not delete them"; across three inner rounds the
orchestrator would face up to three answers per member, and a repeated finding
is a row to reject. `stage2_runs.py` counts released loop rows and tolerates
unknown severities; no reader of an "inner round" label was found (not found by
grep in the files read).

### 3.5 The 2000-line diff bound (open pull request #191)

Pull request #191 (state OPEN, stacked on #187 → #188 → #189 → #190, base
`fix/review-loop-lock`) adds `PAID_DIFF_MAX_LINES = 2000` and
`bounded_paid_diff`: a paid prompt's diff is cut at 2000 lines with a marker,
and a paid round over a cut diff is never clean (so it goes on to the next
stage). Its open item O191-1: a diff over 2000 lines cannot pass the paid
loop. Its text says line counts do not bound tokens, Pi compacts instead of
failing on overflow (read from docs, not measured), and paid members keep read
tools whose reads add context the bound does not see. With inner rounds the
same diff is carried across three turns in one context: the repeated context is
the prompt, the diff, and the answers and tool results of earlier turns. The
interaction of the cut marker with inner rounds (a cut diff, three turns on it)
is not defined anywhere. This change does not depend on #191 being merged; the
paid-prompt code both touch (`prompt_for` and the `change_diff` call in
`review_loop`) is shared.

### 3.6 Other touch points found

- The repair verb, the repair brake and `release-loop` read ids and the
  `Reviewer` column; the phase-6 mark call lists rows as `- <id> [<severity>,
  <dimension>] <where>: <finding>`.
- `call_line()`/`begin_call()` write one audit line per call into
  `findings.md` (`Stage-2 call, ...`); inner turns inside one process would
  carry no separate line unless added. The leak check (`checked_prompt`) runs
  on the prompt once per member; a follow-up message is text the runner
  controls, with no repository content.
- `stage2_runs.py` counts "Stage-2 runs" from `findings.md` and `research.md`;
  its treatment of an inner-round label was not read.
- A `--session-dir`/`--session-id` route would write session files to disk
  under the scratch directory (deleted with it today); with `--no-session`
  nothing persists. The free stage's rule "scratch directory, no tools" is
  unchanged by follow-up messages.

## 4. Where the change would live — files it would have to touch

Identified by reading and grep; each is a candidate, not a decision.

- `scripts/stage2.py`: `run_reviewer()` (argv, message list, output parsing,
  timeout), `run_swarm()` (success rule per inner answer), `review_loop()`
  (row numbering, `Reviewer` cell, notes about inner rounds, replacement
  logic), `spec_review()` / `run_work_model()` (Claude route), `review()` /
  `run_codex()` (Codex route), and the prompts `ANSWER_FORMAT`,
  `FREE_REVIEW_BODY`, plus a new follow-up constant.
- `prompts/04b-review-loop.md`, `prompts/02a-spec-review.md`,
  `prompts/06-review.md` (the reviewer-facing and orchestrator-facing text).
- `docs/WORKFLOW.md` §2 table row 4b, §4 "The review loop (phase 4b)" and the
  Stage-2 routing paragraph; `docs/how-it-works.md` (matches `anfragen_5h`);
  `AGENTS.md` ("Stage 2" paragraph and the 4b table row). `provenance.yaml`
  (read) lists the prefixes `prompts/` and `AGENTS.md` as `allowed:
  [human-written]`, so changes there are not agent-drafted text.
- `docs/adr/0021-review-swarms-until-clean.md` (decision 8's call bound, the
  round/call vocabulary) — amended in place or by a new ADR; the change must
  claim the file in `adr_files` of its `spec.md` (WORKFLOW.md §2, ADR 0014).
- `model-endpoints.yaml`: `opencode-go` notes and, if a limit is configurable,
  a new key; `tests/test_model_endpoints.py` reads this file.
- `tests/test_stage2.py` (the `PI_FLAGS`/argv pin, the fake Pi, the clean-round
  and numbering tests), `tests/test_pi_contract.py` and
  `tests/pi_contract_driver.mjs` (a real-Pi multi-message print run against the
  loopback stand-in would be offline), `tests/test_stage2_availability.py`
  (matches `anfragen_5h`), and a test for the turn count (acceptance
  criterion of the bead).
- `scripts/stage2_runs.py`, only if an inner-round label changes what it counts.
- Class: by the bead and the ADR 0021 amendment this looks like an ADR change
  (five interview records owed, WORKFLOW.md §2 phase 1a).

## 5. What is unclear

1. Whether Pi's print run actually gives message 2 and 3 the earlier answers
   (source says one `session.prompt` per message on one session; unmeasured).
2. Which output channel carries all three answers (JSON event stream vs a
   persisted session vs RPC); the exact `message_end` schema the runner would
   parse was read in docs only, and `--mode json` interacts with the pinned
   argv test and the contract test.
3. What a "request" is for `anfragen_5h` when a call has several turns and
   tool calls; the Go page was not re-read; no per-call request count is
   recorded in the repository.
4. How `--thinking max` behaves on turns 2 and 3 (per-turn re-spend of
   reasoning tokens): not read.
5. Whether Pi's auto-compaction could summarise earlier turns on a large diff
   with three turns, and what a reviewer sees then (#191 states it is unmeasured).
6. Claude route: whether `claude -p` can continue a session when
   `--restricted --safe-mode` is set, and what session files it would write
   (`--no-session-persistence` is incompatible with resume); not run.
7. Codex route: the effort of a resumed thread is "not asserted" in the
   runner's own docstring; whether a read-only resume sees the earlier answer
   as context is the documented purpose of `codex exec resume`, not measured here.
8. Which reviewer-facing wording is binding for the follow-up text (bead
   text vs a prompt file under `prompts/`, where `provenance.yaml` reservations
   may apply — R-18 of pull request #184 says the free round's vocabulary
   belongs in `scripts/stage2.py`, not `prompts/`).
9. Whether 2a (Opus, a different route: Claude Code, subscription) and 6
   (Codex, the verdict-then-marks protocol) "fit" at all; the bead says "where
   it fits" without defining it.
10. Where the measurement the bead requires would be written and on which
    change (the until-clean "measure first" memory names two or three changes).

## 6. Questions for the interview (phase 1a)

An ADR change owes at least five answered records. Each question carries its
context (ADR 0018). Options are listed neutrally; none is recommended here.

**Q1. Which reviewers get inner rounds**
- Topic: the scope of the change.
- Intention: the bead says every reviewer in the loop "and, where it fits, the
  2a and 6 reviews"; the three routes differ technically (Pi one process,
  Codex resumable thread, Claude Code no session today).
- Today: only the loop's calls are single-turn; phase 6 already uses two turns
  (verdict, then loop marks) in one Codex thread; 2a is a single Opus call
  with no session kept.
- Repository change: the set of callers that get the follow-up turns decides
  which functions change (`run_reviewer`, `spec_review`, `review`) and which
  prompts and tests move.
- Architecture change: ADR 0021 covers only the loop; adding 2a and 6 widens
  the amendment to ADR 0016 and ADR 0011's routing, which is a larger decision.
- Question: which of free swarm, Flash swarm, paid ladder, 2a and 6 get inner
  rounds in this change (all three loop stages and nothing else; loop stages
  plus 2a; loop stages plus 2a and 6; or only some loop stages)?

**Q2. How many inner rounds, and whether the number is data**
- Topic: the count and where it is set.
- Intention: the bead fixes "two more rounds"; the call bound in ADR 0021
  decision 8 and the budget in `anfragen_5h` scale with it.
- Today: one turn per call; the ladder, Flash size and free rule are data in
  `model-endpoints.yaml`, the 30-minute limit is a constant in the runner.
- Repository change: a constant in the runner, or a key in the `opencode-go`
  entry (or per stage), with its test; the bead's "a test pins the turn count".
- Architecture change: a configurable count lets a pull request tune cost
  without a code change; a constant makes the doctrine one number.
- Question: is "three turns per call" a fixed number written into the ADR, a
  value in `model-endpoints.yaml` (one for all stages or one per stage), or
  something else?

**Q3. How the context is kept (Pi/OpenCode Go)**
- Topic: the mechanism for a continued context.
- Intention: the pinned Pi can run several fixed messages in one print process
  (cheapest to change, but text mode prints only the last answer and nothing
  can be decided between turns), or be driven turn by turn (RPC, or separate
  processes on a stored session), or the runner can resend the transcript.
- Today: `pi --print --no-session` with one message; the argv is pinned by
  `test_the_review_loop_launches_pi_isolated`, which refuses `--mode`.
- Repository change: the argv, the output parser and two tests change under
  every option; RPC or stored sessions add process or file handling and
  contract tests; the resent transcript adds prompt-building and a larger
  leak-checked prompt.
- Architecture change: a one-process fixed-message call keeps the isolation
  model of ADR 0019 (no session on disk) but forbids an early stop; the others
  allow an early stop at the price of a new Pi surface the contract suite must
  pin.
- Question: which mechanism do you want the runner to use for Pi calls: all
  turns as fixed messages in one process (JSON output), one process per turn
  on a session kept in the scratch directory, an RPC conversation, or a
  resent transcript?

**Q4. Early stop and what "nothing new" means**
- Topic: ending the inner loop early.
- Intention: the bead leaves open whether a round that adds nothing ends the
  inner loop; each skipped turn saves a request and the repeated diff context.
- Today: no inner loop; the strict output rule accepts only six-cell rows or
  exactly `No finding.`, otherwise the member fails.
- Repository change: an early stop needs the runner to read each answer
  before the next turn (see Q3) and a definition of "nothing new" in code and
  prompt; without it the runner always sends all follow-ups.
- Architecture change: the number of calls per member becomes variable between
  one and three, so the call bound in ADR 0021 decision 8 becomes a maximum.
- Question: should an inner round that answers `No finding.` (or only rows the
  member already gave) end that reviewer's inner rounds early, or must every
  reviewer always take all three turns?

**Q5. Row identity and attribution**
- Topic: ids and the Reviewer cell for inner-round rows.
- Intention: the bead wants rows attributed to the reviewer "with the inner
  round named"; the readers of `L<n>-<m>` (`round_rows`, `clean_round`,
  `parse_marks`, `REPAIR_ANSWER`, `release`) all assume that shape, and bead
  coding-harness-6jg (refuse non-conforming ids) is in progress.
- Today: the runner assigns one running `L<round>-<count>` across members and
  puts the member name into `Reviewer`; the model's id cell is discarded.
- Repository change: either the id shape stays and the inner round is named in
  the `Reviewer` cell (for example the model name plus a turn label), or the
  id grows a component and every reader of the shape changes.
- Architecture change: keeping the shape keeps rows, repair, release and
  phase-6 marks unchanged; a new id shape is a change to the repair and
  release contracts of ADR 0017 and the row vocabulary.
- Question: should inner-round rows keep the id `L<n>-<m>` as one running
  series per loop round and name the inner round only in the `Reviewer` cell,
  or get a new id shape that carries the inner round?

**Q6. The clean-round rule with inner rounds**
- Topic: when a loop round is clean.
- Intention: ADR 0021 decision 1 ends the loop on a round with no accepted
  row; with inner rounds a member can say `No finding.` at turn 1 and add rows
  at turn 2 or 3.
- Today: `clean_round()` judges the rows of a loop round after the
  orchestrator decides them; a clean free round ends the loop before any paid
  review.
- Repository change: if all inner rows share the loop-round prefix,
  `clean_round()` needs no change; if inner rounds were judged separately, the
  clean test, the repair brake and the stop messages change.
- Architecture change: either "a round is clean" keeps its meaning with a
  larger set of rows (rounds become less often clean), or the ADR defines a
  second kind of cleanliness for inner rounds.
- Question: is a loop round clean only when the rows of all three inner rounds
  of all its members are decided and none accepted (one rule, as today), or
  should the inner rounds be judged by another rule?

**Q7. Cost and request ceiling**
- Topic: the budget for three turns per call.
- Intention: ADR 0021 decision 8 bounds completed runs at `F + 9` member calls
  and claims "no new money cap"; the Go limits are `anfragen_5h` per model
  (3200 to 34670 on 2026-10-17), and the cost of a turn with tools is
  unmeasured.
- Today: one request counts per call in the ADR's arithmetic; turn and tool
  counts are not recorded.
- Repository change: the runner could record turns per call (and Pi's token
  and request figures, if the JSON events expose them) in the loop record, or
  could refuse a run when a configured ceiling would be crossed.
- Architecture change: a recorded or enforced ceiling moves the cost
  statement of the ADR from "no cap claimed" to a measurable bound.
- Question: should the runner only record turns per call in the loop record
  (so the measurement the bead asks for can be made), or also refuse or stop
  when a configured request ceiling for a model would be crossed?

**Q8. A turn fails after an earlier turn answered**
- Topic: partial results from a continued context.
- Intention: in a single Pi print process, a failure at turn 2 or 3 sets
  exit code 1; the earlier answers are lost in text mode and kept only with
  JSON events or a stored session.
- Today: a nonzero exit or empty answer fails the member for the round; a
  partially successful swarm stands with the failure visible; a failed Flash
  member is replaced by the next ladder model.
- Repository change: either the member fails as a whole (as now), or the
  answers of the completed turns are kept and the failure is named in the
  record beside them.
- Architecture change: "a round completes when at least one member answered"
  (ADR 0021 decision 6) gets a second sense: an answered turn versus an
  answered member.
- Question: when turn 2 or 3 of a member fails, should the member count as
  failed (all its rows dropped, replacement as today), or should its completed
  turns' rows be kept and the failure named?

**Q9. The ADR route and the measurement**
- Topic: how the decision is recorded and proven.
- Intention: the change amends ADR 0021 (decision 8, rounds and calls) and
  possibly ADR 0016 (2a) and 0017 (repair ids); the bead's acceptance wants a
  measurement of new findings per inner round with its date, and the
  until-clean "measure first" memory wants it on two or three changes.
- Today: ADR 0021 is accepted; amendments so far were added as dated
  sections inside the ADR; the owning change claims the file in `adr_files`.
- Repository change: an amendment section (or a new ADR) plus the claim line;
  the measurement either becomes an acceptance gate of this change or follows
  after the merge.
- Architecture change: an in-place amendment keeps one doctrine text for the
  loop; a new ADR leaves ADR 0021 historical and says "amends" at the top.
- Question: should the change amend ADR 0021 in place with a dated section or
  be written as a new ADR that amends it, and must the one-change measurement
  of new findings per inner round be finished before the merge or may it
  follow in a later bead?

Stage-2 call, 2026-10-21: explore · run by a Claude Code sub-agent (Sonnet 5.5,
read-only research in the worktree, no foreign model called); not through
`scripts/stage2.py explore`, so no runner leak-check line exists for this file.

The interview (phase 1a) needs the maintainer; this file stops before it.
