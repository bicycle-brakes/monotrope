---
title: "Spec — draft-known-red"
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
tags: [spec, stage2, draft]
class: bounded
appetite: 4
adr_files: []
neighbours: []
---

# Spec — draft-known-red

The goal in one sentence: a draft can run with Stage 2 off — `draft <change> --stage2-off [REASON]` drafts through Sonnet 5.5 in one recorded attempt, and an exhausted Codex/GLM chain names that flag as the next step (bead coding-harness-83e). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The runner refuses the flag for the verb. `scripts/stage2.py` allows `--stage2-off` only for explore, implement and repair (the verb check in `_run`, read 2026-11-22, `research.md` "The `--stage2-off` refusal is in code"). Where Stage 2 is off or Z.ai is unavailable, a draft therefore has no runner route at all; the doctrine sends the maintainer back to drafting by hand on Opus 5.5 (`docs/WORKFLOW.md` §4, "The draft (phases 2, 2b and 3)": "a draft takes no `--stage2-off`").
- The chain ends at GLM 5.3 and names no way on. `draft`'s routes are Codex, a second Codex attempt with the first's diagnostics, then GLM 5.3 (`scripts/stage2.py`, `draft`'s routes list, read 2026-11-22, `research.md` "The draft verb"); when all three fail, the final message names the findings file but no next step. The bead's origin is exactly this: on the 2026-10-17 night run a draft failed every attempt, `--stage2-off` was refused, and each spec redraft cost about 30 minutes recovered from the attempt refs (`docs/journal/handover/2026-10-17-night-run-sixth.md`, bead coding-harness-83e, P1, discovered from coding-harness-icw).
- This change's own draft is the live case: on 2026-11-22 both Codex draft attempts failed their calls and the run went to its third route, GLM 5.3 (`findings.md`, attempts 1 and 2). Where GLM is not an option either, nothing is left.
- The bead's other half is already merged and stays out of scope: a draft is judged only by the document subset of the gate registry (`document_gates` in `scripts/stage2.py`), and every draft record of 2026-11-21 says "document checks only, no tests ran" (`decisions.md`, "What the research changed", 2026-11-22). A known-red test suite can no longer fail a draft; what remains is the route.

## Terms

**Stage-1 route:** the explicit `--stage2-off [REASON]` route through the `claude-code-plan` endpoint — Haiku 5.5 for explore, Sonnet 5.5 at effort `medium` for the writing verbs. **Chain:** the draft's default three attempts — Codex, a second Codex attempt with the first's diagnostics, then GLM 5.3. **Audit line:** the `Stage-2 call, <date>: draft · attempt <n> · route <route> · endpoint <endpoint> · model <model> · reason <REASON> · leak check clean …` line the runner writes to the change's `findings.md` before each call.

## Acceptance criteria

1. When `python3 scripts/stage2.py draft <change> --stage2-off [REASON]` is invoked, the runner starts the Stage-1 route instead of refusing that `--stage2-off` applies only to explore, implement and repair.
   *Refuted by:* the command exits 2 with that refusal and no model call starts.
2. While a draft runs the Stage-1 route, its single attempt calls Sonnet 5.5 at effort `medium` through the `claude-code-plan` endpoint — the same Stage-1 endpoint implement and repair use — and no Codex or GLM call starts and no GLM key is read.
   *Refuted by:* any Codex or GLM call, a read of the GLM key, or a call with another model or effort.
3. When a Stage-1 draft attempt begins, the audit line in the change's `findings.md` carries `route stage-1`, the `claude-code-plan` endpoint, the model `claude-sonnet-5-5` and, when a reason was given, `· reason <REASON>` — the same record line the other writing verbs write.
   *Refuted by:* an audit line without the route, or without the reason that was given.
4. When the Stage-1 draft attempt's call fails, the run exits 1 after that one attempt, restores the worktree to the baseline outside the change folder, and quotes the attempt's diagnostics and its saved attempt ref below the audit line.
   *Refuted by:* a second model call, an exit 0, an outside path left changed, or the diagnostics or ref missing from `findings.md`.
5. When the Stage-1 draft attempt's document check is red, the attempt fails with exit 1 and its scope line and problems are quoted below its audit line, as on the Codex chain.
   *Refuted by:* a red document check that exits 0 or whose problems are absent from `findings.md`.
6. When a Stage-1 draft attempt changes a path outside the change folder — beyond the one new ADR file under `docs/adr/` — the runner puts that path back before the document check, as on the Codex chain.
   *Refuted by:* such a path left changed after the put-back or reaching the attempt's commit.
7. When a Stage-1 draft attempt passes, the runner makes exactly one descendant commit whose message names `route stage-1`, and the time entry under the plan's `## Time used` records `route stage-1` with the model `claude-sonnet-5-5`.
   *Refuted by:* a commit message or time entry naming another route or model, or more than one commit.
8. When a draft run fails after its last allowed attempt, its final failure message names `--stage2-off` as the next step exactly when the run did not already carry the flag.
   *Refuted by:* an exhausted chain whose message names no next step, or a Stage-1 run's failure message naming the flag again.
9. When `--stage2-off` is passed to a verb other than explore, draft, implement and repair, the runner refuses with exit 2 before any call.
   *Refuted by:* any such verb starting a model call or exiting 0.
10. When the runner's own texts state which verbs accept `--stage2-off` — the module docstring, the flag's help text and `docs/WORKFLOW.md` — they name `draft`, and the workflow no longer says a draft takes no `--stage2-off`.
    *Refuted by:* any of those texts still excluding draft, or the workflow keeping the old refusal sentence.

## Non-goals

- No automatic Sonnet fallback inside the chain: after the GLM attempt fails the run stops, and only the final message names the flag. The relaxation for writing attempts belongs to coding-harness-s9r / coding-harness-6ie, whose maintainer decision of 2026-10-16 is not yet implemented (`decisions.md`, [DETAIL] items, 2026-11-22).
- No change to the draft's guards, its put-back rules or its document-subset gate — that half of the bead is already merged (`decisions.md`, "What the research changed").
- No route changes for explore, implement or repair, and no additional verb accepts the flag.
- No `## Runner route` block in a drafted `plan.md`: a Stage-1 draft's record is the `findings.md` audit line and the time entry, as for explore; that block belongs to implement and repair through the shared attempt loop, and a first draft's `plan.md` does not exist before the model writes it.
- No ADR, no change to `model-endpoints.yaml` (the Sonnet endpoint is already declared for the other writing verbs), and the by-hand Opus 5.5 draft of §3 stays as it is.

## Protected areas

The held paths — `provenance.yaml`, `decisions/gates.yaml`, `decisions/answers/`, `docs/adr/`, `model-endpoints.yaml`, `prompts/`, `templates/`, `AGENTS.md`, `README.md`, `.github/`, `.claude/`, `.beads/` — stay untouched: the change needs none of them, and the prompts' "Where Stage 2 is off, Opus 5.5 … writes it" sentences remain true for the by-hand path. The shared attempt loop `run_attempts` and the implement and repair route lists stay as they are.

## Definition of Done

- `make verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md` — the `draft` row of §4's verb list and the draft section's closing sentence; no ADR changes.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- Bead: the pull request closes coding-harness-83e, and its last commit carries the trailer `Closes-Bead: coding-harness-83e`.
- Special runs: none.

## Open decisions

None open. The scope decisions stand in `decisions.md` (the reasoned interview skip and the four [DETAIL] items, 2026-11-22). Two freely revisable wording details were decided here: the exhausted chain's final message names the exact next-step command `python3 scripts/stage2.py draft <change> --stage2-off <reason>`, mirroring implement's phrasing, and a Stage-1 run's failure message keeps naming the findings file alone; the refusal message and the flag's help text name draft in the verb list.
