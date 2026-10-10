---
title: "Research — stage2-flash-runner"
status: accepted
implementation_status: done
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-qcp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, flash-runner]
---

Phase 1 per `prompts/01-explore.md`. Facts only, read 2026-10-07 in worktree at
`1952ac8` (branch `feat/stage2-flash-runner`). Open item O-1 of bead
coding-harness-qcp: build two verbs in `scripts/stage2.py` for GLM 5.3 Flash
to run phase 1 (explore) and phase 4 (implement) against Z.ai's endpoint,
behind the leak check, with fallback to Haiku 4.5/Sonnet 5.5 when stage 2 is
off.

## 1 · How the runner works today

### 1.1 scripts/stage2.py structure

The file `scripts/stage2.py` (read 2026-10-07, lines 1–905) is the runner.
Four verbs exist:

| Verb        | Phase | Endpoint         | Model       | Handler          |
|-------------|-------|------------------|-------------|------------------|
| spec-review | 2a    | openai-codex     | gpt-6.1-sol | spec_review()    |
| review-loop | 4b    | glm-coding-plan  | glm-5.3     | review_loop()    |
| release-loop| —     | —                | —           | release_loop()   |
| review      | 6     | openai-codex     | gpt-6.1-sol | review()         |

Missing: `explore` (phase 1) and `implement` (phase 4), both for GLM 5.3 Flash.

### 1.2 GLM call pattern from review_loop

Lines 789–852 show the pattern for GLM 5.3 calls:

1. Preflight checks (line 791): folder exists, endpoint declared, bead found.
2. Leak check (line 809): `scripts/leakcheck.py` scans repository, changes,
   commits and prompt. Exit 0 required; otherwise raises `Refused`.
3. Record the call (lines 444–448): date, verb, endpoint, model, leak stats
   in `findings.md`.
4. Build prompt (lines 806–808): read from `prompts/04b-review-loop.md`,
   append `ANSWER_FORMAT` and `READ_REQUEST`, wrap diff.
5. Launch Claude Code (lines 815–835):
   - Model: `GLM[1]` = `"glm-5.3"` (line 77)
   - Effort: `GLM[2]` = `"max"` (line 77)
   - Tools: `"Read,Grep,Glob"` only (line 826)
   - Environment: `glm_env(key, config_dir)` (line 835)
6. Environment setup (lines 203–212, `glm_env()` function):
   - Base URL: `"https://api.z.ai/api/anthropic"` (line 78)
   - Auth: `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` from GLM_KEY
   - GLM_MODEL_VARIABLES (lines 108–115) set to model name
   - Empty config directory
   - `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`
7. Secret handling: GLM_KEY from `~/.config/cc-routing/secrets.env` (line
   801), scrubbed from stdout (line 838).

### 1.3 Infrastructure for Flash

`model-endpoints.yaml` (lines 111–127):

- Endpoint `glm-coding-plan` lists both `glm-5.3` and `glm-5.3-flash`
- `darf_sehen: [framework]` — framework content only
- Residency `anbieter-erklaert`, billing `abonnement`
- Note: Flash models decided for phases 1 and 4, verbs not built yet

`prompts/01-explore.md` (line 3): "Model: GLM 5.3 Flash — much input, little
output, no deep reasoning; through the runner and the leak check
(`docs/WORKFLOW.md` §4). Until the runner starts this phase, Haiku 4.5
explores."

`prompts/04-implement.md` (lines 3–6): "Model: GLM 5.3 Flash — a solid worker
given a clear plan; through the runner and the leak check (`docs/WORKFLOW.md`
§4). Until the runner starts this phase, Sonnet 5.5 at effort `medium` builds."

`WORKFLOW.md` §4 (lines 622–627): "The two Flash rows are decided and not
built. The runner has no verb that starts phase 1 or phase 4 on GLM 5.3 Flash
… Until that is built (an open item of the change that wrote this section,
`plans/changes/archive/2026-09-30-stage-2-codex-glm/plan.md`, Amendment 1), §3's rows run both
phases: Haiku 4.5 explores and Sonnet 5.5 implements."

ADR 0007 (lines 58–71): "Implementation runs on GLM 5.3 Flash instead of
Sonnet 5.5" and "Exploration runs on GLM 5.3 Flash too, instead of Haiku 4.5"
(maintainer decisions, 2026-10-06).

### 1.4 Environment allow-list

`ENV_ALLOW` (lines 94–107): PATH, HOME, USER, LOGNAME, SHELL, TMPDIR, LANG,
LC_ALL, LC_CTYPE, TERM, TZ, CODEX_HOME. Only these from caller's environment
are passed.

`GLM_MODEL_VARIABLES` (lines 108–115): ANTHROPIC_MODEL,
ANTHROPIC_DEFAULT_OPUS_MODEL, ANTHROPIC_DEFAULT_SONNET_MODEL,
ANTHROPIC_DEFAULT_HAIKU_MODEL, ANTHROPIC_SMALL_FAST_MODEL,
CLAUDE_CODE_SUBAGENT_MODEL. All set to model name for GLM (line 211).

### 1.5 Preconditions before each call

`preflight()` (lines 395–404) and `begin_call()` (lines 432–448):

1. Change folder exists
2. `spec.md` has bead in header
3. Endpoint declared in `model-endpoints.yaml`: present, model listed,
   framework in `darf_sehen`, residency not "nicht-erklaert"
4. Leak check passes
5. `findings.md` created if missing, with proper header
6. Call line recorded

### 1.6 Explore vs. implement

Explore (phase 1):

- Reads repository broadly
- Writes only `research.md` (no code)
- No `make verify` gate
- Input: change name only
- Output: research findings

Implement (phase 4):

- Reads tree and writes code to worktree
- Reads `spec.md` and `plan.md`
- Must commit per green step (AGENTS.md house rule, prompts/04-implement.md)
- Runs `make verify` after changes (WORKFLOW.md §4, line 583)
- Input: spec.md, plan.md, appetite
- Output: code + tests

Both Flash calls:

- Same Z.ai endpoint (`glm-coding-plan`)
- Same Flash model (`glm-5.3-flash`)
- Leak check before call
- Tools restricted to Read, Grep, Glob
- Full repository context

## 2 · What must change in scripts/stage2.py

### 2.1 Model constants

Currently: `GLM = ("glm-coding-plan", "glm-5.3", "max")` (line 77) for
review-loop.

Need: Separate constants:

```python
GLM = ("glm-coding-plan", "glm-5.3", "max")        # review-loop (4b)
GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")  # explore, implement
```

### 2.2 Two new verbs

`explore(root: Path, change: str)`:

- Like `spec_review()` but for phase 1, GLM Flash
- Input: phase prompt from `prompts/01-explore.md`, change name
- Reads full repository context
- Output: `plans/changes/<change>/research.md`
- No `make verify` gate

`implement(root: Path, change: str)`:

- Like `review_loop()` but for phase 4, GLM Flash
- Input: `prompts/04-implement.md`, spec.md, plan.md
- Reads tree, writes code to worktree
- Output: code + tests + commits
- Gate: `make verify` green after call

### 2.3 Prompt building

Both use `phase_prompt()` (lines 451–458):

- Read prompt file
- Append change name
- Append format instructions and read request
- Implement: also append spec.md and plan.md content

### 2.4 Make verify after implement

Implement must run `make verify` after the call (WORKFLOW.md §4, line 583).

Not read: whether runner runs it or implementer does. Current design: runner
launches, implementer checks. Recommendation for plan: implementer runs
`make verify` after call returns.

## 3 · Files touched by this change

- `scripts/stage2.py`: add two verbs, add `GLM_FLASH` constant
- `prompts/01-explore.md`: no change (already names Flash)
- `prompts/04-implement.md`: no change (already names Flash)
- `model-endpoints.yaml`: no change (already declares Flash)
- Tests: defer to phase 4 plan

## 4 · Reuse from review_loop

| Piece            | Source           | Reuse   |
|------------------|------------------|---------|
| Preflight checks | preflight()      | Yes     |
| Leak check       | begin_call()     | Yes     |
| Prompt building  | phase_prompt()   | Partial |
| Environment      | glm_env()        | Yes     |
| Launch command   | review_loop()    | Yes     |
| Tool restrictions| line 826         | Yes     |
| Secret scrubbing | scrub()          | Yes     |

Largest reuse: environment setup, launch, secret handling, preconditions.
New work: prompt building (different inputs), output recording
(research.md/code vs. loop.md).

Stage-2 call, 2026-10-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 253 files, 567 commits, 12 rules.

## Runner exploration — 2026-10-07

Read 2026-10-07 in the worktree `.claude/worktrees/stage2-flash-runner`, branch `feat/stage2-flash-runner`; HEAD per the session's git snapshot is `6951fd9` ("docs(stage2): activate Flash routes"), with uncommitted modifications to `model-endpoints.yaml`, `scripts/stage2.py`, `tests/test_stage2.py` and this change's four artefacts. This refreshes the facts above, which describe the state before the verbs were built ("Missing: `explore` and `implement`").

### What exists today

- The runner `scripts/stage2.py` has six verbs (`VERBS`): `explore`, `implement`, `spec-review`, `review-loop`, `release-loop`, `review`; the module docstring names all six with phases and exit meanings (0 done, 1 call or implementation post-check failed, 2 refused).
- Route constants: `GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")`, `GLM = ("glm-coding-plan", "glm-5.3", "max")`, `HAIKU = ("claude-code-plan", "claude-haiku-4-5", None)`, `SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")`, `GLM_BASE_URL = "https://api.z.ai/api/anthropic"` (`scripts/stage2.py`).
- `explore()`: preflight reads the bead from `research.md` (`preflight(bead_file="research.md")`, no required artefacts); Flash requires `GLM_KEY` (`read_secret`), `--stage2-off` selects `HAIKU` and never reads the key. `work_prompt()` assembles `prompts/01-explore.md` + change name + full `AGENTS.md` + the facts-only instruction + `READ_REQUEST`; `begin_work_call()` writes the attempt-aware audit line into `research.md` before the process starts; `run_work_model(writable=False)` launches `claude -p … --tools Read,Grep,Glob --restricted --safe-mode --strict-mcp-config --permission-mode dontAsk --permission-prompts none --no-session-persistence`, with `glm_env()` (Flash, empty config dir) or the bare allow-list `foreign_env({})` (Stage 1). A non-empty answer is appended under `## Runner exploration — <date>`; empty or failed exits 1; streams are scrubbed (`scrub`).
- `implement()`: preflight reads the bead from `spec.md` and requires `plan.md`; refuses pre-existing worktree changes outside this change's `findings.md` (`changed_paths`); captures baseline `HEAD` and the `## Time used` bytes (`time_log`). Route ladder: Flash → one Flash repair ("first Flash post-run check failed") → one Sonnet 5.5 ("two Flash post-run checks failed"); `--stage2-off` starts with a single Sonnet attempt and writes a `## Runner route — <date>` line into `plan.md` (`insert_before_time`) only after that attempt's clean leak check. The model gets `Read,Grep,Glob,Edit,Write` and `--permission-mode acceptEdits`, never a shell. After a usable answer the runner replaces an exact key occurrence in changed files with `[credential]` and refuses without fallback (`remove_changed_credential`), runs `make verify` with `commit.gpgsign=false` plus the time-log check (`verify_attempt`, diagnostics bounded to the last 80 lines), and on success makes exactly one checkpoint commit `feat(<change>): implement accepted plan` (`checkpoint`, identity `stage2-runner`, one descendant commit, clean status).
- `--stage2-off` is refused for the four older verbs (`main()`); without a value it records "stage 2 disabled by caller".
- `model-endpoints.yaml`, endpoint `glm-coding-plan`: models `glm-5.3` and `glm-5.3-flash`, `darf_sehen: [framework]`, residency `anbieter-erklaert`, `abrechnung: abonnement`; its note names both Flash verbs as live through `stage2.py explore` / `implement` (bead coding-harness-qcp).
- The operative texts agree the verbs are live: `docs/WORKFLOW.md` §4 ("The two Flash rows are live through the runner", the six-verb list, the leak barrier, "Those settings are configured on every call, not measured"); `AGENTS.md` stage-2 paragraph; `prompts/01-explore.md` and `prompts/04-implement.md` name the runner commands and the `--stage2-off` form; `prompts/03-plan.md` ("Carry an Explore fallback forward") has the Stage-1 route line copied from `research.md` into the new `plan.md`.
- Tests: `tests/test_stage2.py` covers the Flash verbs with stand-ins only (`test_the_runner_finds_only_stand_ins`, `test_a_stand_in_contacts_nothing`). By name — explore: `test_explore_uses_flash_read_only_and_appends_research`, `test_explore_needs_research_but_not_spec_or_plan`, `test_explore_stage2_off_uses_haiku_without_reading_the_glm_key`, `test_explore_scrubs_the_flash_credential_from_its_answer`, `test_an_empty_explore_answer_fails_without_an_answer_block`; implement: `test_implement_flash_has_file_tools_and_the_complete_contract`, `test_implement_requires_spec_plan_time_heading_and_no_preexisting_work`, `test_a_failed_or_empty_work_call_stops_without_retry`, `test_a_postcheck_failure_gets_one_flash_repair_with_its_diagnostic`, `test_two_failed_postchecks_route_once_to_sonnet`, `test_verify_failure_is_bounded_in_the_repair_prompt`, `test_a_time_heading_deleted_mid_run_becomes_a_repair_diagnostic`, `test_checkpoint_failures_are_call_failures`, `test_findings_only_dirt_is_allowed_and_committed`, `test_a_changed_file_with_the_glm_key_is_cleaned_and_refused`; routes/leak/audit: `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`, `test_a_leak_between_work_attempts_stops_before_fallback`, `test_a_stage1_route_line_is_written_only_after_a_clean_leak_check`, `test_stage2_off_is_only_for_work_verbs`; doctrine and endpoint note: `test_the_doctrine_and_prompts_say_the_flash_verbs_are_live`, `test_the_flash_rows_say_they_are_live_through_the_runner`, `test_the_explore_prompt_names_the_live_flash_command_and_haiku_fallback`, `test_the_implement_prompt_names_flash_and_keeps_sonnet_5_5_at_medium`, `test_the_glm_remark_names_all_three_live_verbs`.
- Review state of this change: `findings.md` holds the phase-2a Codex rows S1–S3 (each status "taken") and audit lines for spec-review and one review-loop round (model `glm-5.3`); no released loop rows and no phase-6 verdict yet. `plan.md` §Revisions in phase 4 records steps 1–4 as one checkpoint (`e9738c5`), step 5 as `6951fd9`, and GLM findings L1-3 and L1-6 as taken (the endpoint note joined step 5).

### Where it lives

Runner and leak barrier: `scripts/stage2.py` (symbols above), `scripts/leakcheck.py` (called from `checked_prompt`). Declaration: `model-endpoints.yaml`, guarded by `tests/test_model_endpoints.py`. Prompts: `prompts/01-explore.md`, `prompts/03-plan.md`, `prompts/04-implement.md`. Doctrine: `docs/WORKFLOW.md` §4; decision record `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`. Change artefacts: the five files under `plans/changes/archive/2026-10-07-stage2-flash-runner/`; `plans/INDEX.md` lists all five as `draft` / `none`, dated 2026-10-07 (bead coding-harness-qcp).

### What is unclear (open questions)

1. Committed vs. uncommitted: the git snapshot lists `scripts/stage2.py`, `tests/test_stage2.py`, `model-endpoints.yaml` and the four artefacts as modified on top of `6951fd9`. I read file contents only; which parts are uncommitted is open. The endpoint-note edit attributed to GLM finding L1-6 may be among them.
2. Whether `make verify`, `pytest tests/test_stage2.py` and `python3 scripts/plans_registry.py --check` are green right now: I ran nothing (read-only phase). `plan.md` §Verification names the exact commands.
3. The loop record of the first review-loop round lives outside the worktree (`record_dir()` → `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/stage2-flash-runner/loop.md`); I read nothing outside the worktree, so round 1's rows and their decided state are unknown here. `findings.md` gets them only after the phase-6 verdict (`release()`).
4. `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` still carries "Explore and implement run on GLM 5.3 Flash — decided, not built" (its point 5) and the evidence bullet "the statement that the two Flash rows are not built", while every operative text says live. `plan.md` §Not touched excludes the ADR ("the decision is unchanged") and spec criterion 17's file list omits it; whether the ADR's interim sentence stays as a historical record is not settled in anything I read.
5. `plan.md`'s Tests table names functions that differ from several actual names in `tests/test_stage2.py` (for example planned `test_two_postcheck_failures_route_one_repair_then_sonnet` vs. actual `test_two_failed_postchecks_route_once_to_sonnet`; planned `test_each_work_verb_requires_its_phase_artefacts` vs. actual `test_explore_needs_research_but_not_spec_or_plan` and `test_implement_requires_spec_plan_time_heading_and_no_preexisting_work`). Each named behaviour has an apparent counterpart; the names diverge.
6. The only `explore` audit line in `research.md` is this invocation's ("attempt 1 · route flash", written by `begin_work_call` before the call); the `## Runner exploration` block that `explore()` appends afterwards does not exist yet. Whether this call serves as plan step 6's real-explore evidence is for the orchestrating session to place.

### Which files a continuation would touch

Per `plan.md` step 6 and its Revisions: the four artefacts (evidence, `implementation_status` → `partial`), `plans/INDEX.md` (regenerate), then the real runner calls in `plan.md` §Verification (`review-loop`, `review`, explore evidence) with the commits they make. `scripts/stage2.py` and `tests/test_stage2.py` only if a review round raises a finding. The step-5 texts (WORKFLOW, prompts, AGENTS) are committed at `6951fd9`; the endpoint-note edit may still be uncommitted (open question 1).
