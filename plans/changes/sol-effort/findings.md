---
title: "Findings — sol-effort"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-yzk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — sol-effort

Stage-2 call, 2026-10-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 418 files, 1063 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/sol-effort/plan.md` +119 -0
> - `plans/changes/sol-effort/research.md` +48 -0
> - `plans/changes/sol-effort/spec.md` +138 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/sol-effort/findings.md: stale — updated 2026-10-13 is older than its last change 2026-10-14 (uncommitted)
> plans/changes/sol-effort/plan.md: stale — updated 2026-10-13 is older than its last change 2026-10-14 (uncommitted)
> plans/changes/sol-effort/research.md: stale — updated 2026-10-13 is older than its last change 2026-10-14 (uncommitted)
> plans/changes/sol-effort/spec.md: stale — updated 2026-10-13 is older than its last change 2026-10-14 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
> ── [interview-minimums] $ lauf_cmd
> 1 finding(s):
>   - docs/adr/0017-codex-repairs-taken-findings.md is claimed by codex-repairs, sol-effort in one diff — one change claims an edit and a correct claim is never removed to settle it; split the pull request — the amendment in one, the edit to the other change's folder in another
> ── [interview-minimums] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9159 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
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
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-14: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 421 files, 1063 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/sol-effort/plan.md` +29 -28
> - `plans/changes/sol-effort/research.md` +52 -2
> - `plans/changes/sol-effort/spec.md` +10 -7
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [interview-minimums] $ lauf_cmd
> 1 finding(s):
>   - docs/adr/0017-codex-repairs-taken-findings.md is claimed by codex-repairs, sol-effort in one diff — one change claims an edit and a correct claim is never removed to settle it; split the pull request — the amendment in one, the edit to the other change's folder in another
> ── [interview-minimums] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 9208 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
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
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-14: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 421 files, 1063 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1
>
> The runner put back:
> - `plans/INDEX.md`
> - `plans/changes/sol-effort/plan.md`
> - `plans/changes/sol-effort/research.md`
> - `plans/changes/sol-effort/spec.md`

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 420 files, 1108 commits, 12 rules.

> Reconstructed from the session, not the original output: the record of this second run was not committed and a checkout discarded it.
>
> Attempt 1 (codex) failed its post-run checks. `make verify` exited 2 at the gate `frontmatter-current`: `plans/changes/sol-effort/decisions.md` is stale, its `updated` date 2026-10-13 is older than its last change (commit `20bc86c`, rebased on 2026-10-14).
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/sol-effort/plan.md` +124 -0
> - `plans/changes/sol-effort/research.md` +75 -2
> - `plans/changes/sol-effort/spec.md` +136 -0

Stage-2 call, 2026-10-14: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 422 files, 1108 commits, 12 rules.

> Reconstructed from the session, not the original output (see above).
>
> Attempt 2 (codex-repair): the runner put back what a draft may not change: `plans/INDEX.md` and `plans/changes/sol-effort/decisions.md`. The attempt failed its post-run checks; `make verify` exited 2 at the gate `frontmatter-current`.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/sol-effort/decisions.md` +2 -2
> - `plans/changes/sol-effort/plan.md` +6 -6
> - `plans/changes/sol-effort/research.md` +48 -0

Stage-2 call, 2026-10-14: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 422 files, 1108 commits, 12 rules.

> Reconstructed from the session, not the original output (see above).
>
> Attempt 3 (glm) failed its call: claude call failed: exit 1. The Claude Code output names `glm-5.3` as not in this version's model catalog. Z.ai is exhausted until 2026-10-14 14:34 CEST.

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 420 files, 1109 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-14

Spec review by hand in a remote Claude Code session (Opus 5.5 sub-agent in a
fresh context, read-only; input: `spec.md`, `research.md`, `decisions.md`, and
the code and documents on `main` the spec names). Not started through
`stage2.py spec-review`. Checked: the three files; on `main` `scripts/stage2.py`
(`CODEX`, `run_codex`, `review`, `draft`, `repair`, `run_attempts`,
`begin_call`, `preflight`), `scripts/stage2_runs.py` (`FOREIGN_ROUTES`),
`scripts/check_interview_minimums.py` (`MINIMUMS`), the `openai-codex` entry in
`model-endpoints.yaml`, the Sol `max` mentions in `docs/WORKFLOW.md`, the four
prompts and ADRs 0016 and 0017.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | spec | Criterion 4; Terms ("Active instructions") | [AMBIGUITY] Criterion 4 is limited to "active workflow tables" and the four prompts' Model lines, while Terms defines a wider "Active instructions" that no criterion uses; the prose of `docs/WORKFLOW.md` §"The draft (phases 2, 2b and 3)" also says Codex (`gpt-6.1-sol`, effort `max`). Reading A: only tables and Model lines are in scope, the prose keeps `max`, criterion 4 stays green and the workflow contradicts itself. Reading B: every active instruction as Terms defines it is in scope, the prose changes too, and the doctrine check must cover it. As written the criterion cannot go red on the prose sentence. | Opus 5.5 | in spec | — |
| S-2 | MAJOR | SPEC | decisions | Open decisions; Definition of Done ("`make verify` is green") | [GAP] Editing a claimed ADR (`adr_files` lists 0016 and 0017) requires five maintainer interview records under `check_interview_minimums.py`; `decisions.md` holds two. The spec says three more answers are owed before the ADR edits but names no questions, and does not say whether phases 3/4 wait for them or whether the ADR amendments are split off until they exist. As written, criteria 5 and 6 and a green `make verify` cannot all be reached, so the implementer would have to decide whether to stop, defer the ADR edits or proceed. | Opus 5.5 | in spec | — |
| S-3 | MINOR | SPEC | spec | Criterion 3 | [AMBIGUITY] The refuting cases include a "historically resumed" verdict call: the first phase-6 review resumes a recorded phase-2a Codex thread (ADR 0016), which may have been started at `max`. Reading A: the runner only has to pass `high` on the resume argv, which an argv stand-in can prove. Reading B: the resumed thread must actually run at `high`, which needs live evidence the Definition of Done excludes ("stand-ins establish configured arguments"). Under A the criterion is an argv check; under B it cannot be proven red or green offline. | Opus 5.5 | in spec | — |
| S-4 | MINOR | SPEC | spec | Criterion 4 (refutation) | [AMBIGUITY] Draft, design, plan and review instructions are refuted if they "still say `max` or `medium`", but the WORKFLOW §4 repair row names both Sol and "Sonnet 5.5 at effort `medium`", and the stage-1 rows (2 Spec, 2b Design, 3 Plan) put Sol inside Opus rows. Reading A: only the effort attached to Sol counts, so the doctrine check must parse effort per model. Reading B: any `max` or `medium` in a row that mentions Sol refutes, which turns correct rows red or forces edits to non-Sol text the non-goals protect. The existing row-level regression in `tests/test_stage2.py` (effort `max` in every non-Flash row of WORKFLOW §4) leaves open which granularity replaces it. | Opus 5.5 | in spec | — |

Original phase-2a verdict, before the maintainer's answers: four
`[AMBIGUITY]`/`[GAP]` rows were open; the spec did not pass that review.

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 422 files, 1119 commits, 12 rules.

## Phase-2a integration — 2026-10-14

The maintainer's answers are preserved in Q-3 to Q-6 of `decisions.md`.
The reviewer text is unchanged; only the rows' Status cells are resolved.

- S-1: in spec — Q-4 requires one central setting; criterion 4 includes all
  active Sol effort instructions, including drafting prose, and criterion 5
  requires subsequent adjustments to propagate without other edits.
- S-2: in spec — Q-3 splits off the ADR amendments; the former ADR criteria
  are removed, `adr_files: []` records the authorized scope, and the plan
  has no ADR work or interview wait for this change.
- S-3: in spec — Q-6 makes criterion 3 an argument check; the resumed thread's
  actual internal effort remains explicitly unproven.
- S-4: in spec — Q-5 makes criterion 6 assess Sol's effort reference per
  model; other models' valid effort literals remain allowed.

Gate after integration: no phase-2a row is open; spec and plan follow the
recorded answers. The bounded class requires no design artifact.

Stage-2 call, 2026-10-14: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 422 files, 1151 commits, 12 rules.

Stage-2 call, 2026-10-14: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 422 files, 1154 commits, 12 rules.

Stage-2 call, 2026-10-14: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 422 files, 1155 commits, 12 rules.

Stage-2 call, 2026-10-14: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 422 files, 1164 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/sol-effort/plan.md` +3 -0
> - `tests/test_stage2.py` +38 -15
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-1: tests/test_stage2.py::test_sol_effort_checks_every_later_sol_mention: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> ```

Stage-2 call, 2026-10-15: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 422 files, 1165 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/sol-effort/plan.md` +11 -1
> - `tests/test_stage2.py` +26 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-1: tests/test_stage2.py::test_sol_effort_checks_appended_sol_sentences: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> ```

Stage-2 call, 2026-10-15: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 422 files, 1165 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +15 -0
> - `tests/test_stage2.py` +1 -7
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-15: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 422 files, 1166 commits, 12 rules.

Stage-2 call, 2026-10-15: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 422 files, 1169 commits, 12 rules.

Stage-2 call, 2026-10-15: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 422 files, 1171 commits, 12 rules.

## Phase 6 — Opus 5.5, 2026-10-15

Claude path of `prompts/06-review.md`: an Opus 5.5 sub-agent at effort high
in a fresh context, started by the orchestrator, not through `stage2.py
review`. Phase 2a ran on Opus 5.5, so no phase-2a session of this reviewer
exists and none was resumed. Diff read: `git diff origin/main...HEAD` at
`5c8a460`; yardstick: the current `spec.md`, whose four phase-2a rows (S-1 to
S-4) arrived as the integration block above says (criteria 3, 4 and 6, and
the removed ADR criteria with `adr_files: []`).

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|

No finding: the diff meets criteria 1 to 7 and the Definition of Done as far
as phase 6 can measure it.

Checked: the shipped defaults against criteria 1 to 3 — `CODEX_EFFORTS` is
`{"draft": "high", "repair": "medium", "review": "high"}` and `CODEX` carries
no effort of its own (`scripts/stage2.py`); every `run_codex` caller passes
its verb — `draft` (initial and `codex-repair` attempt, one call site),
`run_attempts` with `repair` from `repair()` (both Codex attempts), and
`review` for the verdict and the resumed loop-marks call — and `run_codex`
puts `model_reasoning_effort` on every argv, a resume included; the only
other reader of an endpoint's effort slot (`run_work_model`, `--effort`) is
never reached with `CODEX`, and `implement` routes no Codex attempt, so the
`KeyError` for an unnamed verb is unreachable today; `declaration_problem`,
`begin_call`, `begin_work_call` and `stage2_runs.FOREIGN_ROUTES` read only
endpoint and model, so the empty effort slot changes no audit line or
declaration check. Criterion 4: no Sol effort literal is left in the
section-3 and section-4 tables, the drafting prose or the four Model
paragraphs (`git grep` over tracked files outside change folders, journal
and research finds only ADR 0016, line 103, deferred by Q-3 and named as
deferred in `docs/WORKFLOW.md` §4); each link names its own verb and resolves
from `docs/` and `prompts/`. Criterion 5: the tests read `CODEX_EFFORTS`
instead of repeating values, and the propagation test plants distinct
settings per verb across initial, retry, historical resume, re-check and
resumed marks argv; no other operational default exists (`git grep`
`model_reasoning` finds one site). Criterion 6: the doctrine checker cuts a
Sol clause at the next model name and was read against the planted
mixed-model cases. Criterion 7: `scripts/stage2_session.py` is untouched and
`test_codex_is_dispatched_interactively_with_its_exact_safety_flags` pins the
exact interactive argv. Protected areas: the file list touches no
`model-endpoints.yaml`, `AGENTS.md`, ADR, gate, permission, provenance or
other change folder. Considered and not raised: the doctrine checker keys
on the word "effort", so a future Sol sentence that states a value without
that word would pass; every current Sol effort sentence uses it, and the
pinned places fail closed when the word is missing. The `Closes-Bead`
trailer and the PR body are phase 7's and were not measurable here.

Phase 6 verdict: opus-5.5, 2026-10-15

## Phase 4b — loop rows, released 2026-10-15

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | MAINT | impl | tests/test_stage2.py — `sol_clause` / `sol_effort_problems` | The new doctrine check inspects Sol's effort only inside the enumerated instruction spans and ends each span at the next mention of another model, so an independent Sol effort written after that mention — for example a further sentence appended to the repair row, which already names Sonnet 5.5, or a new prose sentence elsewhere in the workflow — is never read; the planted-fault test rewrites only the reference in place, and `test_sol_effort_checks_allow_other_models_in_the_same_instruction` even asserts an appended other-model sentence passes. Such an edit leaves the suite green while the instruction then names a value independently and contradicts the central setting the change exists to enforce. | deepseek-v4.1-flash | fixed — not a test — doctrine checker now checks every Sol mention in active instructions; planted later independent efforts and new prose refute the baseline helper. | no | agree |
| L2-1 | MINOR | MAINT | review | tests/test_stage2.py:6336 (`OTHER_MODEL`), 6347–6353 (`sol_clauses`) | The mixed-model boundary the check truncates a Sol clause at knows only six display-name spellings (`Opus \| Sonnet \| GLM \| glm-5 \| the ladder \| Haiku`); the repository also names the same models by id (`claude-sonnet-5-5` in the SONNET tuple and in §3's session commands, `claude-haiku-4-5`, `claude-opus-5-5`) and prose names Fable, Kimi, MiMo and DeepSeek. Rewrite the §4 repair row's "Sonnet 5.5 at effort `medium`" as `claude-sonnet-5-5 at effort \`medium\`` and `sol_effort_clause_problems` reads that literal as Sol's own independent effort and turns red, although spec criterion 6 (Q-5) says another model's effort in the same instruction stays allowed; the case is shown offline, no live call needed | mimo-v2.6-flash | rejected — the checker fails closed: an unknown model name makes it red, never green, so no wrong effort can pass; a reworded row would surface at once; named in the PR as an accepted limit |  | agree |
| L2-2 | MINOR | MAINT | review | scripts/stage2.py:807, 2446, 2597 | `run_codex` now takes a required keyword-only `verb` and indexes `CODEX_EFFORTS[verb]` without checking it, while `run_attempts` is shared and forwards its caller verb — `implement` already calls it with "implement". A Codex route added to any verb outside draft/repair/review crashes with a bare `KeyError` after the preflight and after the audit line has been written into `findings.md`, and neither `run_codex`'s nor `run_attempts`' docstring says which verbs a Codex route may carry | mimo-v2.6-flash | taken — not a test — docstring: `run_codex` now names the verbs that may carry a Codex route and that any other stops with a KeyError before the call; repaired by the orchestrating session | no | agree |
| L2-3 | MINOR | MAINT | review | plans/changes/sol-effort/plan.md:50–51 | Plan step 2's example link spells `../../../scripts/stage2.py`, which resolves outside the repository from both documents the change edits (`docs/WORKFLOW.md` and the four prompts) and contradicts the operative sentence on the next line ("From each edited document the link target is `../scripts/stage2.py`", the form the implementation and `effort_reference` at tests/test_stage2.py:6341 enforce); research.md records the choice the implementer made, the plan alone would lead a maintainer to links that resolve nowhere | mimo-v2.6-flash | taken — not a test — false statement in the plan: the example now shows the link as written in the edited documents (`../scripts/stage2.py`); repaired by the orchestrating session | no | agree |
| L3-1 | MAJOR | SPEC | spec | tests/test_stage2.py · `sol_effort_problems` / `sol_effort_clause_problems` | The check that an instruction names its own verb's entry runs verb-aware only for the pinned fragments, the drafting prose and the Model paragraphs; every other instruction it scans — other prose and unpinned rows of the two routing tables — is checked without a verb, so any entry of `CODEX_EFFORTS` satisfies it. An active instruction naming another verb's entry (e.g. a new sentence in the repair prose linking the drafting entry) stays green, while the central-reference criterion names the wrong verb as refuting and the plan promises a planted wrong key at every location including prose; that refutation cannot go red outside the pinned spots. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_sol_effort_check_reads_the_verb_of_every_unpinned_instruction | no | agree |
| L3-2 | MINOR | MAINT | diff | scripts/stage2.py · `run_codex` | An unmapped verb raises a bare `KeyError` out of the effort lookup instead of a refusal, and the shared attempt runner forwards its caller verb, which the mapping does not name for the implement route; a route change that ever pairs that verb with this endpoint stops the run with a traceback after the call's audit line is already written, with no message naming the cause. | mimo-v2.6-pro | rejected — repeats L2-2: the `run_codex` docstring now names the verbs a Codex route may carry; the lookup stops before the call, and no route pairs implement with Codex; a refusal message would be new runner scope, named in the PR as an accepted limit |  | agree |
| L3-3 | MINOR | MAINT | diff | tests/test_stage2.py · `SOL_EFFORT_PLACES` / `test_sol_instructions_reference_the_central_effort_for_each_verb` | The regression demands each listed instruction's full wording as a substring before it evaluates the reference rule, so a rewording of one of those sentences that keeps the correct reference still fails at the presence assertion; a maintainer editing unrelated prose there sees a red suite with no wrong reference to find. | mimo-v2.6-pro | rejected — the wording pin fails closed (red, never falsely green) and makes the reader update the pinned sentence on purpose; named in the PR as an accepted limit |  | agree |

Rounds run: 3

Kept from the loop record:

The answer was not only six-cell rows; what is not one is kept below as it came.

I found the following after reading the diff, the touched files (`scripts/stage2.py`, `tests/test_stage2.py`, `docs/WORKFLOW.md`, the four prompts, the change's spec/plan/research/decisions/findings, `plans/INDEX.md`, `plans_registry.py`, `check_docs.py`) and tracing every `run_codex` call site:
