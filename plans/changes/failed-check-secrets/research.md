---
title: "Research — failed-check-secrets"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-8hr
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, leak-check]
---

# Failed-check diagnostics that carry test secrets — Research

Phase 1 for bead coding-harness-8hr, seeded by the orchestrating session on
2026-10-16 against `origin/main` at `6029bbf`.

## The question

On 2026-10-15 the draft of the pi-pin change (bead coding-harness-agx) failed
its first attempt's `make verify`: the disk was full, and a test raised
`OSError` (ENOSPC). The runner wrote the pytest traceback into that change's
`findings.md`, and the traceback held a test fixture's fake key value. The
leak check matched it (rules `secret:openai-style-key` and
`secret:generic-api-key-assignment`). The retry prompt carries the failure
text, so the leak check blocked attempt 2 and the draft stopped. Needed (bead
text): scrub secret-rule matches from diagnostics before they are written or
sent, and test that a failed attempt whose traceback holds a fixture key can
still be retried.

## Known so far (read, not run)

- The leak check exempts `tests/` from its secret rules ("12 secret rules not
  applied under tests/" in every stage-2 INFO line), so the fixture key is
  legal where it lives and becomes a finding only once copied elsewhere.
- A leak-check BLOCK stops without fallback (AGENTS.md, stage 2); the fix must
  not weaken that rule. It must keep the secret out of the text instead.

## To explore

1. Where the runner turns a failed post-run check (`make verify`, red-first,
   other checks) into text: which function, which files it writes
   (`findings.md`, the loop record, the plan's time section) and which prompts
   it reaches on a retry.
2. Where the leak check's secret rules live and whether the runner can reuse
   them to redact a string (the same rule set, not a second copy).
3. Every path where diagnostics leave the runner: written files, retry
   prompts, audit lines, handover notes. Which of them the leak check reads.
4. What redaction should look like so the diagnostics stay useful (rule name
   and position kept, value replaced), and whether non-test secrets in a
   traceback must still block rather than be redacted.
5. Which tests cover the failure-text path today, so a test with a fixture key
   in a failing traceback can follow them.

Stage-2 call, 2026-10-16: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 463 files, 1314 commits, 12 rules.

## Runner exploration — 2026-10-16

### What exists today: where a failed post-run check becomes text

The runner's failure-text chain in `scripts/stage2.py` has four stations. First, `verify_attempt` (statement of the chain in its docstring, „…then run `make verify`“) starts `make verify` through `launch` (the `launch` function, `subprocess.run` with `capture_output=True`) and, on a non-zero exit, builds the problem string `` `make verify` exited <code> `` plus the evidence from `verify_evidence(done, key)` (the call sits in the body of `verify_attempt`, next to the time-log check). Second, `verify_evidence` (same file) reduces a red run: `red_sections(done.stdout)` keeps the gates that `verify_all.sh` framed `RED (block)` — the frame patterns are `GATE_START`/`GATE_END`, the budgets `RED_SECTION_LINES`, `RED_TOTAL_LINES`, `STDERR_LINES`, `TAIL_LINES` — and otherwise falls back to the run's last `TAIL_LINES` lines; everything passes through `scrub(…, key)`. Third, `run_attempts` (the shared attempt loop, used by `implement` and `repair`; the draft has its own loop in `draft`) turns the problems into text: `attempt_block(attempt, route, listing, files)` renders header, changed-files list and the diagnostics inside a fenced code block, `quote_block` quotes every line with `>` and cuts lines over the `QUOTE_LINE_CHARS` bound, and the block is appended to the change's `findings.md` below the attempt's audit line; the same listing is appended to the loop-local `diagnostics` list. Fourth, the retry prompt: `run_attempts` splices a `## Earlier post-run diagnostics` section with the accumulated diagnostics into the endpoint's base prompt (between the body and `READ_REQUEST`); the builders are `implementation_prompt`, `repair_prompt` and, for the draft, `draft_prompt` (its heading reads `## Earlier attempts' diagnostics`). The prompt then goes to `begin_work_call`, which calls `checked_prompt` before anything is written or sent.

One ordering fact matters for the incident shape: `begin_work_call` appends the audit line (`Stage-2 call, …`) only after `checked_prompt` has passed. A leak-check BLOCK therefore raises `Refused` before this attempt has any line in `findings.md` — a blocked attempt is invisible in the committed record.

### The leak check's rules and their reuse

The secret rules do not live in the repository. `scripts/leakcheck.py`, function `default_denylist`, resolves the denylist to `~/.config/cc-routing/denylist.txt`, overridable by `LEAKCHECK_DENYLIST` or `--denylist`; the documented format is one `name = regex` per line, and a rule is a secret rule exactly when its name starts with `secret:` (constant `SECRET_PREFIX`). `read_denylist` returns the parsed `Rule(name, pattern, secret)` list or a reason; a missing, unreadable, invalid or empty denylist is a BLOCK („Unchecked is not clean“), never an empty pass. The scan unit `_scan` reports each match as place, rule name and match length and never the matched text — stated in the module docstring („What is NOT printed: the match“) and pinned by `tests/test_leakcheck.py` (`test_the_report_never_carries_the_match`, named in its module docstring). The `tests/` exemption for secret rules is `TESTS_PREFIX` with the helpers `_under_tests` (working tree) and `_header_in_tests` (patch hunks); a prompt text and a commit message are never exempt.

Reuse without a second copy of the rules is already established practice: `scripts/stage2.py` imports the module and calls `leakcheck.check` and `leakcheck.default_denylist` inside `checked_prompt`, so `read_denylist` and `Rule` are reachable the same way. The rules are the same objects the check blocks with — the runner would redact with the check's own rule set.

### Every path diagnostics take, and what the check reads

Written by the runner after a failed attempt: the quoted block in `plans/changes/<change>/findings.md` (the traceback carrier), the audit lines and the stage-1 route block in `plan.md` (no output text in either), the checkpoint commit message (format lines only, `FORMAT_COMMIT_HEADING`). Sent by the runner: the retry prompt with the diagnostics section (through `run_work_model`, which writes the prompt to a temporary file and passes it as `--append-system-prompt-file`, or through `run_codex`), the review-loop prompt (scratch `review-prompt.md`), and the session verb's handover prompt (`scripts/stage2_session.py`, `handover_prompt`; leak-checked in `run` through `runner.checked_prompt`).

`leakcheck.check` scans at call time: (a) every file under `plans/changes/<name>/` — so `findings.md` with its quoted tracebacks is read back on every later call in that worktree; (b) every tracked or untracked, non-ignored tree file as it stands on disk; (c) the full reachable branch and remote history with patches; (d) the staged diff; (e) the call's own prompt text, passed as `[("prompt", prompt)]` in `checked_prompt`. Both channels of the incident class therefore trip the same check: the quoted block on disk and the diagnostics copy inside the prompt. Not scanned: the loop record outside the worktree (`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`, module docstring), the runner's own terminal output (`fail` prints scrubbed stderr tails), and Codex rollout files.

### Redaction material that exists today

The runner scrubs exactly one secret today: the routing credential. `read_secret` reads a named value from the secrets file (`secrets_path`); `_fragment_pattern`, `credential_spans` and `replace_credential` match the value or any 8-character window of it and replace the run with the literal `[credential]`; `scrub(text, key)` wraps that and is applied in `quote_block`, `verify_evidence`, `prepare_derived`, `_not_run`, `launch`'s error paths and `fail`. Under `--stage2-off` the key is `None` and nothing is scrubbed (`quote_block` docstring). A second, older mechanism refuses instead of redacting: `remove_changed_credential` with `credential_message` scans the changed files for the key and raises `Refused` (call sites around the attempt loops and in `checkpoint`). The check's own reporting discipline — place and rule name kept, value never shown — is the shape the bead's „rule name and position kept, value replaced“ mirrors; the replacement marker the runner uses today is `[credential]`.

### Tests that cover the failure-text path today

`tests/test_stage2.py` already pairs a planted leak marker with a denylist rule: the constants `LEAK = "LEAKMARK-123456"` and `DENYLIST = "planted = LEAKMARK-[0-9]{6}\n"`, written into the test world by the `world` fixture alongside `secrets.env` (constants near the imports; the fixture writes `denylist.txt` and `secrets.env` and stand-in programs for `make`, `codex`, `claude`, `pi` from the `STAND_IN` template — so a red `make verify` with arbitrary output is scriptable per scenario). Existing coverage to follow: `test_each_call_runs_its_own_leak_check`; `test_a_stage1_route_line_is_written_only_after_a_clean_leak_check`; BLOCK simulation by monkeypatching `leakcheck.check` with a `planted` wrapper (two call sites); the `red_sections` tests around the `_red` helper; failed-attempt block tests (`test_a_failed_draft_check_leaves_its_block_and_its_tree`, and the assertions that the retry prompt carries `` `make verify` exited 1 `` while the block stands in `findings.md`); `scrub`/`replace_credential` tests; `quote_block` bound tests. `tests/test_leakcheck.py` builds each case its own repository and denylist (fixtures `isolated`, `denylist`, `repo`) and is the pattern for rule-level tests. A comment at the `OKEY` constant records a measured refusal of key-shaped text in a loop prompt (2026-10-08) — the same refusal class, met before.

### The incident record: what is there, what is not

The seed's account (pi-pin draft attempt 1 fails `make verify` with ENOSPC, the traceback carries a fixture key, the leak check blocks attempt 2) is quoted from bead `coding-harness-8hr`, which this sub-agent could not read. What the committed record shows: `plans/changes/pi-pin/findings.md` holds three failed implement attempts of 2026-10-15, each with a `leak check clean` audit line; the attempt-1 diagnostics show pytest `StopIteration`, ruff and markdownlint output — no ENOSPC, no key-shaped value, and no leak-check BLOCK line anywhere in the file. A repository-wide search for `ENOSPC` finds only this change's seed research. „Not there in the committed record“ and „not found elsewhere in the tree“ are two statements; both hold for the ENOSPC traceback, and whether the committed `findings.md` was restored or cleaned after the incident is unanswered — the bead text is the authority.

A second, documented incident of the same class is in `docs/journal/handover/2026-10-15-night-run-fourth.md` (section „Stuck“): after the research-swarm implement was completed by an Opus sub-agent, „The leak check then blocked the loop on two synthetic test keys in new test files; they are built from parts now.“ Same root pattern — legal `tests/` fixtures surfacing where the exemption does not reach — through a different channel (new test files in the tree/history scan, not a quoted traceback), and mitigated by building the keys from parts so the denylist no longer matches. The same handover names „a leak-check BLOCK“ among the runner's stop conditions („Stops.“ paragraph).

### What is unclear

1. The exact bead text of `coding-harness-8hr` — not readable from this sub-agent; the seed quotes it as „scrub secret-rule matches from diagnostics before they are written or sent, and test that a failed attempt whose traceback holds a fixture key can still be retried“.
2. Whether the committed `plans/changes/pi-pin/findings.md` was cleaned after the incident, or the incident's verb/attempts differ from the seed's telling (see above).
3. Whether redaction covers only `secret:`-prefixed rules or every rule; the `tests/` exemption marks `secret:` rules as the fixture class, while non-secret rules name customer data — a match there reads as a real disclosure, not as a fixture travelling.
4. What redaction does when the denylist cannot be read at that moment (`read_denylist` returns a reason; the check itself refuses — „Unchecked is not clean“).
5. Whether a redaction applied to diagnostics must also cover the quoted block in `findings.md`, the terminal output of `fail`, or only the prompt text — today the two written/sent channels are fed from the same `problems` strings, so one seam could cover both, but that is an observation, not a decision.
6. How much context a redacted traceback keeps for the next model to repair from (the check's report model keeps rule name and place; the runner's existing marker is `[credential]`).

### Which files a change would have to touch

- `scripts/stage2.py` — the producers and consumers of diagnostics: `verify_evidence`, `prepare_derived`, the `attempt_block`/`quote_block` call sites in `run_attempts` and `draft`, the `diagnostics` lists, the three retry-prompt splices (`run_attempts`, `draft_prompt`, `repair_prompt`); a redaction helper would sit beside `scrub` and reuse `leakcheck.read_denylist`/`Rule` (both module-level, already imported here).
- `tests/test_stage2.py` — the retry-with-fixture-key test follows the `world` fixture, the `make` stand-in scenario and the existing `LEAK`/`DENYLIST` pair; BLOCK simulation precedent exists.
- `scripts/leakcheck.py` — not necessarily: for a runner-side redaction that reuses its API, nothing in the check changes; the standing rule „a leak-check BLOCK stops without fallback“ stays untouched.
- `docs/WORKFLOW.md` — the stage-2 sections that name the runner's stop conditions, if the behaviour is to be stated there.

## Draft inspection — 2026-10-16

Read at `2cc2c81`: `draft` and `run_attempts` append the assembled `listing`
directly to their retry-diagnostics lists before rendering `attempt_block`.
Cleaning the block alone therefore leaves the prompt channel unprotected.
`prepare_derived` reduces evidence before calling `scrub`; multiline secret
matches need handling before that reduction as well as before verify tails.

The shared `DENYLIST` in `tests/test_stage2.py` names its planted rule
`planted`, without `secret:`. New redaction scenarios need an additional
test-local secret rule; relabelling the shared rule would change existing
refusal tests. `read_denylist` already exposes the compiled pattern and the
secret flag, including a reason for missing, unreadable, invalid or empty
rules. No scanner API change is required.

There is no `templates/plan.md` or `scripts/validate_change_artefacts.py` at
this baseline. The phase-3 prompt defines the plan form; the available
interview and criterion-ledger gates can check the draft. The drafting call
does not read the external session registry, tracker or hosting service;
their current state is not read here, and the runner owns commit and full
verification.
