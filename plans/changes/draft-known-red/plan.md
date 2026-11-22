---
title: "Plan — draft-known-red"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, draft]
---

# Plan — draft-known-red

```text
For you:     A draft runs without Stage 2: draft <change> --stage2-off [REASON] drafts through Sonnet 5.5, and an exhausted Codex/GLM chain names that flag as the next step.
Done when:   The flag starts one Sonnet draft attempt with its reason in the audit line, the draft's guards and document check stay as they are, and make verify passes.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     An automatic Sonnet fallback inside the chain, route changes for other verbs, and a Runner-route block in the drafted plan.
Pre-mortem:  suppose it failed: most likely because the Stage-1 route skipped a draft guard the chain attempts still hold.
Starts unless you say stop.
```

## Files and steps

1. `scripts/stage2.py` — accept and route the flag for the draft. In `_run`, add `"draft"` to the verb set that accepts `--stage2-off` and name draft in the refusal message. Dispatch the flag: the branch that passes `args.stage2_off` to `implement` also passes it to `draft`, and `draft(root, change, stage2_off=None)` gains the parameter. In `draft`, preflight the `SONNET` endpoint when the flag is given (else `CODEX`, as today) and set `routes = [(SONNET, None, "stage-1", stage2_off)]` for that case — nothing else in the attempt loop changes: the GLM key read stays bound to the GLM endpoint, and the put-back, the document check, the time entry and the checkpoint keep running through the same code. The final `CallFailed` message names `python3 scripts/stage2.py draft <change> --stage2-off <reason>` as the next step exactly when `stage2_off is None`; a Stage-1 run's message keeps naming the findings file alone. Name `draft` in the module docstring's two `--stage2-off` sentences and in the flag's argparse help.
2. `docs/WORKFLOW.md` — two edits. The `draft` row of §4's verb list gains "`--stage2-off [REASON]` uses Sonnet 5.5 at effort `medium`", mirroring the implement and repair rows. The draft section's closing sentence is rewritten: three failures exit 1 naming `--stage2-off` as the next step, the chain never falls through to Sonnet on its own, the GLM key is read only when the GLM attempt is due, and a draft takes `--stage2-off [REASON]` like the other writing verbs — Sonnet 5.5 at effort `medium`, one attempt with the reason in its audit line — while the by-hand Opus 5.5 draft of §3 stays for a maintainer who drafts without the runner.
3. `tests/test_stage2.py` — hold the new behavior and re-point the standing refusal. Drop `"draft"` from `test_stage2_off_is_only_for_work_verbs`'s parametrization (its planted fault) and add `"draft"` to `test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten`. Write the tests of the criterion ledger: the accepted Stage-1 draft (one Sonnet call at `claude-sonnet-5-5` effort `medium`, `read_secret` monkeypatched to fail, audit line with `route stage-1` and the reason, one commit naming `route stage-1`, time entry with the route), the failed Stage-1 call (exit 1, no second call, baseline restored outside the change folder, diagnostics and attempt ref quoted), the red document check failing the Stage-1 attempt, the put-back of a planted outside path, the exhausted chain's final message naming the flag (and a Stage-1 failure not naming it), and the doctrine test reading the module docstring and `docs/WORKFLOW.md` for draft among the `--stage2-off` verbs and the gone refusal sentence. Mirror the existing Stage-1 tests of implement (`test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`) and the draft tests built on `draft_world`.

What is not touched: `run_attempts` and the implement and repair route lists; the draft's guards, `draft_keep`, the put-back machinery and `document_gates`; `prompts/`, `templates/`, `AGENTS.md`, `README.md`, `decisions/`, `docs/adr/`, `model-endpoints.yaml` and the other held paths — no held path is edited, so no orchestrator bootstrap step is owed; and `plans/INDEX.md`, which the runner renders.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_sonnet_attempt_and_records_reason — the run exits 2 with the old refusal, or no model call starts.
- 2: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_sonnet_attempt_and_records_reason — a Codex or GLM call starts, the GLM key is read, or the model or effort differs.
- 3: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_sonnet_attempt_and_records_reason — the audit line lacks `route stage-1` or the given reason.
- 4: not yet written tests/test_stage2.py::test_a_failed_stage_one_draft_call_stops_without_fallback — a retry or fallback runs, the key is read, or an outside path stays changed.
- 5: not yet written tests/test_stage2.py::test_a_red_document_check_fails_a_stage_one_draft_attempt — a red check exits 0 or hides its problems.
- 6: not yet written tests/test_stage2.py::test_a_stage_one_draft_puts_back_paths_outside_the_change_folder — an outside path stays changed or reaches the commit.
- 7: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_sonnet_attempt_and_records_reason — the commit message or time entry names another route or model, or a second commit appears.
- 8: not yet written tests/test_stage2.py::test_an_exhausted_draft_chain_names_stage2_off_as_the_next_step — the chain's final message names no next step, or a Stage-1 failure names one.
- 9: tests/test_stage2.py::test_stage2_off_is_only_for_work_verbs — a verb outside explore, draft, implement and repair accepts the flag.
- 10: not yet written tests/test_stage2.py::test_the_runner_texts_name_draft_among_the_stage2_off_verbs — a text still excludes draft or keeps the old refusal sentence.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -k 'stage2_off or draft'
make verify
```

## Runner route — 2026-11-22

Stage-1 route: explore · model claude-haiku-5-5 · reason: research swarm refuses: its state store must lie outside the home directory (XDG_STATE_HOME), not set up for this night run (`research.md`, 2026-11-22).

## Time used

2026-11-22 15:30:11–15:42:22 UTC, 730 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
