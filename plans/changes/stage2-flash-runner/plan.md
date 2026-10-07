---
title: "Plan — stage2-flash-runner"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-qcp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, glm, runner]
---

# Plan — stage2-flash-runner

```text
For you:     GLM 5.3 Flash can explore and implement through the guarded runner; an explicit outage route uses Haiku/Sonnet and leaves a record
Done when:   criteria 1–19 hold, `make verify` is green, and the change has passed the real Codex and GLM review routes
Appetite:    4 h of phase 4, one repair round included
Not now:     a general orchestrator, arbitrary plan commands, spend limits, endpoint or ADR changes
Pre-mortem:  suppose it failed: most likely because a failed attempt's audit line is mistaken for pre-existing implementation work and blocks the safe fallback
Starts unless you say stop.
```

Implements `spec.md` criteria 1–19. The change is `bounded`: ADR 0007 and the
maintainer's answers already decide the routes and checks. The Codex spec
review reported three BLOCKERs; all are taken in `findings.md` and resolved in
the revised criteria 9 and 15. Facts read at `0dcf65a`.

## Decided in phase 3

No `[DECISION]` or `[AMBIGUITY]` remains.

- `[DETAIL]` — **`--stage2-off` accepts an optional reason:** no value records
  `stage 2 disabled by caller`; a following value records the caller's text,
  for example `--stage2-off "Z.ai unavailable"`. This keeps the normal command
  short and makes the required fallback reason durable.
- `[DETAIL]` — **the Stage-1 endpoint is `claude-code-plan`:** the fallback
  still passes the declaration check, but never reads the GLM secret. Haiku's
  effort is omitted because the routing decision pins none; Sonnet is pinned
  to `medium`.
- `[DETAIL]` — **the model never runs a command:** this closes Codex finding S1
  and keeps `GLM_KEY` out of child shells. The runner runs `make verify` and
  creates one checkpoint commit only after the gate and time log pass.
- `[DETAIL]` — **pre-existing dirt is allowed only in this change's
  `findings.md`:** a failed attempt leaves its audit line there. Any source,
  plan or other change needs a human to recover before another invocation.
- `[DETAIL]` — **diagnostics are bounded:** a repair prompt gets the failed
  condition and at most the final 80 lines of `make verify`; no entire build
  log is copied into the next model call.

## Steps

Read `date` at every step boundary (`prompts/04-implement.md`).

1. **Routes, preflight and prompts — `scripts/stage2.py`** (45 min).
   - Add `GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")`,
     `HAIKU = ("claude-code-plan", "claude-haiku-4-5", None)` and
     `SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")`;
     parameterise `glm_env` by model so review-loop stays on `glm-5.3`.
   - Generalise header-bead reading and `preflight`: explore reads
     `research.md`; implement reads the bead from `spec.md` and also requires
     `plan.md`; review verbs keep their current `spec.md` preflight. Every
     chosen route is checked against `model-endpoints.yaml`.
   - Add a work prompt builder that appends `AGENTS.md`, the change and read
     boundary without `ANSWER_FORMAT`; implement also appends complete spec,
     plan, baseline and any bounded repair diagnostics.
   - Extend argument parsing with `explore`, `implement` and
     `--stage2-off [REASON]`; reject that option for the four older verbs.
     Commit with step 2.

2. **Explore — `scripts/stage2.py`** (30 min).
   - Select Flash normally or Haiku when Stage 2 is explicitly off. Flash
     requires `GLM_KEY`, an empty configuration directory and model-specific
     environment; Haiku uses the declared Claude Code plan route and normal
     auth without reading the secrets file.
   - Before each process, run the existing declaration/leak sequence and
     append one attempt-aware audit line to `research.md`; invoke Claude Code
     restricted, safe, no-session, no-MCP and read-only.
   - Scrub the Flash process streams, reject non-zero or empty output, then
     append a dated `## Runner exploration` block. Preserve the existing body
     and stamp `updated:`. A Stage-1 audit line includes its reason.

3. **Implement and its completion boundary — `scripts/stage2.py`** (65 min).
   - Refuse initial porcelain-status entries except this change's
     `findings.md`; capture baseline `HEAD` and the exact `## Time used`
     section. Start Claude Code restricted and safe with only
     `Read,Grep,Glob,Edit,Write`, no Bash or permission handler, and a fresh
     leak check/audit line for every attempt.
   - On Flash, scrub streams and inspect every changed regular file for the
     exact credential; replace an occurrence with `[credential]` and refuse
     without repair. A process error or empty answer exits 1 immediately.
   - After a usable answer, run `make verify` with signing disabled and test
     the time section. On failure, call Flash once more with the bounded
     diagnostic; after a second post-check failure, call Sonnet once with both
     diagnostics. `--stage2-off` starts with that one Sonnet attempt.
     Write a Stage-1 route block only after that attempt's leak check is clean.
   - On a passing attempt run `git add -A`, create
     `feat(<change>): implement accepted plan` with fixed local identity and
     signing off, then require one descendant commit and clean status. Any
     missing postcondition after the final route exits 1. A runner-owned git
     failure is also exit 1, not a pre-call refusal and not a model repair.
   Commit.

4. **Executable evidence — `tests/test_stage2.py`** (65 min).
   - Give the temporary world valid `research.md`, `plan.md`, `AGENTS.md` and
     a `make` stand-in; let `World.run` pass CLI options. The stand-ins still
     use only the standard library and contact nothing.
   - Add the tests in the table below: exact routes/environments/prompts and
     tool boundaries; phase-appropriate preflight; append-only research;
     declaration and leak refusals per attempt; Stage-1 reasons; failed-call
     stop; verify/time/commit/clean checks; one Flash repair then one Sonnet;
     key removal; and old-verb compatibility.
   - Extend the existing doctrine helpers at the bottom of the file rather
     than adding a second test file. Commit.

5. **The live instructions — `docs/WORKFLOW.md`, `AGENTS.md`,
   `prompts/01-explore.md`, `prompts/03-plan.md`,
   `prompts/04-implement.md`, `model-endpoints.yaml`** (25 min).
   - Replace “decided and not built” and “four verbs” with the two live
     commands, route/fallback/leak behaviour and implementation post-checks.
   - Make the Explore and Implement prompts name their runner commands. The
     plan prompt copies an Explore Stage-1 route line from research into the
     new plan. The Implement prompt says that under this runner the model
     updates the time log while the runner verifies and commits.
   - Make the one-screen AGENTS description say the Flash verbs are live and
     give the explicit fallback form. Update the existing doctrine tests with
     planted counterexamples. Replace the endpoint note that says the verbs do
     not exist. Stamp current frontmatter where applicable.
   Commit.

6. **Review and close — change artefacts and `plans/INDEX.md`** (30 min plus
   one repair round).
   - Regenerate the index. Run the verification below. Append exact evidence
     and the measured time span here; set the four artefacts' implementation
     status to `partial` (the pull request is not merged yet).
   - Run `review-loop` through real GLM 5.3 on the implementation diff, decide
     every loop row on evidence and repair once where needed. Resume the real
     Codex session `01a11588-e851-7302-9fdc-2e30e7726fab` with `review`, then
     release/mark the loop rows as the runner prescribes. No direct model CLI.
   - Re-run the verification, commit, push the feature branch and open the
     pull request. The bead closes only after the PR is merged.
   - Before the second review-loop round, run real `explore` on this change.
     Its read-only Flash call proves that the new Claude Code flags are
     accepted; commit its append-only research evidence.

## Tests

| Criteria | Test and planted fault |
| --- | --- |
| 1, 18 | Extend the verb/help parametrisation and full-flow tests; remove one new verb or change an old argv to turn them red. |
| 2 | `test_each_work_verb_requires_its_phase_artefacts`; remove `spec.md` from Explore (still passes) and from Implement (refuses), then remove each bead/folder. |
| 3, 4 | `test_flash_uses_the_declared_model_and_model_environment`; plant each endpoint fault and change only `glm-5.3-flash` or review-loop's `glm-5.3`. |
| 5 | `test_every_work_attempt_runs_a_fresh_leak_check`; the first stand-in plants the deny marker and no repair/fallback call occurs. |
| 6 | `test_explore_is_read_only_and_gets_the_explore_prompt`; add `ANSWER_FORMAT` or a write/shell tool to make it red. |
| 7 | `test_explore_appends_and_scrubs_its_answer` and `test_an_empty_explore_answer_fails_without_an_answer_block`; seed unique research, return the key, then fail/empty in separate cases. |
| 8 | `test_implement_gets_rules_spec_plan_baseline_and_diagnostic`; omit each source or feed an unbounded verification log. |
| 9 | `test_implement_has_file_tools_but_no_command_tool`; add Bash, WebFetch, MCP, bypass, project settings, or remove Edit. A host-command spy accepts only `make verify` and the named git sequence. |
| 10 | The successful implementation test plus `test_a_time_heading_deleted_mid_run_becomes_a_repair_diagnostic` and parametrised `test_checkpoint_failures_are_call_failures`: verify red, unchanged/deleted time section, checkpoint command, non-descendant head and dirty status each stay non-zero; the all-green case asserts the exact commit. |
| 11 | `test_two_postcheck_failures_route_one_repair_then_sonnet`; inspect three prompts/models and prove no fourth call. A success on attempt one or two shortens the route. |
| 12 | `test_a_failed_or_empty_work_process_stops_immediately`; both cases leave exactly one model call and exit 1. |
| 13, 14 | `test_stage2_off_uses_declared_stage1_routes_and_records_the_reason`; remove `GLM_KEY`, assert Haiku/Sonnet and no Z.ai variables, and assert the research/plan route line. Older verbs with the flag refuse. |
| 15 | Extend the environment/credential test across new routes; plant the exact key in a changed file and in streams, assert replacement/refusal/no fallback; spy that Stage 1 never calls `read_secret`. |
| 16 | `test_every_work_attempt_has_a_numbered_audit_line`; two Flash attempts and Sonnet produce three distinguishable lines in the right artefact. |
| 17 | Extend `phase_table_problems` and prompt/doctrine tests with exact command, fallback, leak-stop and plan-copy assertions; each test mutates the fact it guards. |
| 19 | Commands and real runner evidence under Verification and Evidence. |

## Verification

```bash
.venv/bin/python -m pytest tests/test_stage2.py -q
.venv/bin/python scripts/plans_registry.py --check
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
.venv/bin/python scripts/stage2.py review-loop stage2-flash-runner
.venv/bin/python scripts/stage2.py review stage2-flash-runner
```

The last two commands run only after the deterministic suite is green. They
contact the declared endpoints and therefore are evidence, not unit tests.

## Not touched

The endpoint models, eligibility and data classes (only the stale explanatory
note changes), `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` (the
decision is unchanged), `scripts/leakcheck.py` and its denylist, `decisions/gates.yaml`,
`.github/workflows/ci.yml`, `.claude/settings.json`, the loop record format and
its external state, `scripts/kit/manifest.yaml` (both changed executable files
already have their roles), Omnigent, Hermes, MiMo and sibling repositories.

## Time used

2026-10-07 10:56–11:08, 12 min — implementation through the two green
checkpoint commits; both boundaries read with `date`.

## Revisions in phase 4

- Steps 1–4 became one code-and-tests checkpoint (`e9738c5`), not the three
  commits the first plan wording implied: the shared helpers and their fault
  tests were one green unit and were not independently shippable. Step 5 is
  the separate doctrine checkpoint (`6951fd9`). GLM finding L1-3 exposed the
  missing explanation; no acceptance condition changed.
- The endpoint note joins step 5 after GLM finding L1-6: its models and access
  declaration were already correct, but its prose still said the two verbs did
  not exist. This revises the first `Not touched` wording, not the scope.
- GLM finding L2-1: `insert_before_time` no longer refuses when a failed Flash
  attempt deleted the `## Time used` heading. It appends the route block and
  restores an empty heading, so the Sonnet attempt of criterion 11 starts and
  receives both diagnostics. The block is still written after that attempt's
  clean leak check (L1-5); the audit line order is unchanged because the
  restore cannot fail. The test deletes the heading in both Flash attempts.
- GLM finding L2-2: the exact-key barrier now also covers the gate run.
  `implement` rescans changed files after `make verify` (a hit is refused like
  the pre-gate hit: no repair, no fallback), `verify_attempt` replaces the exact
  key in the gate's output tail with `[credential]`, and `checkpoint` rescans
  immediately before `git add -A`. The key is the run's Flash key on every
  attempt, the Sonnet fallback included. Criterion 15 of the spec now says
  "including by the gate run" and the output scrub. Two tests: a gate that
  writes the key into a changed file, and a gate that prints it.
