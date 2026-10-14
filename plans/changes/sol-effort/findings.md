---
title: "Findings — sol-effort"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-14
updated: 2026-10-14
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
