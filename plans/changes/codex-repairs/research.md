---
title: "Research — codex-repairs"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-0ga
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair, codex]
---

# Codex repairs the taken review findings — Research

Phase 1 for bead coding-harness-0ga, read against `origin/main` at `3199a28`
on 2026-10-13.

## The request

The maintainer, 2026-10-13, in the conversation: "Bitte lasse zukünftig das
Implementieren der Fixes der Fehler aus dem Review Sol machen" — in future,
let Sol (Codex, model `gpt-6.1-sol`) implement the fixes of the review
findings. A second remark the same day: the Z.ai budget was exhausted mainly
by GLM 5.3 (not Flash), the model ADR 0015 routes the repairs to.

## Where it stands

- ADR 0015 (`docs/adr/0015-glm-5-3-repairs-taken-findings.md`) routes
  `python3 scripts/stage2.py repair <change>` to GLM 5.3: a first attempt, one
  GLM 5.3 repair attempt with the first one's diagnostics, then a Sonnet 5.5
  stage-1 fallback (`scripts/stage2.py`, `repair`).
- ADR 0016 has Codex draft spec, design and plan (`draft <change>`), so the
  runner already starts Codex for work that writes files.
- Codex (`gpt-6.1-sol`) is the phase-6 reviewer (`review <change>`).
- The research of the repair verb (`plans/changes/stage2-repair/research.md`)
  named as a non-goal: a reviewer never repairs its own findings, because it
  would then judge its own work in the next review.

## Questions this change has to answer

- [DECISION] Phase-6 findings come from Codex. If Codex repairs them, the
  re-review judges its own repair. Is that accepted, or does the re-review
  then run in a fresh Codex session, or on another model?
- [DECISION] Does Codex repair both the loop rows (4b, found by the OpenCode
  Go ladder) and the phase-6 findings?
- [DECISION] What is the fallback when the Codex attempts fail — GLM 5.3,
  Sonnet 5.5, or straight to the maintainer?
- [GAP] How the runner starts Codex for a writing task today (the `draft`
  route), its sandbox, its time limit and how its answer is checked.
- [GAP] What in the repair verb is GLM-specific (credential scrubbing,
  `glm_env`, the post-run checks) and what carries over unchanged.

Stage-2 call, 2026-10-13: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-4-5 · reason Z.ai weekly limit exhausted until 2026-10-14 14:34 CEST (HTTP 429, code 1310), and Claude Code 2.1.296 refuses the GLM names (bead coding-harness-6th) · leak check clean over 409 files, 1018 commits, 12 rules.

## Runner exploration — 2026-10-13

Haiku 4.5's answer under `--stage2-off` (audit line above) did not explore: it
proposed to call the runner itself and reported no repository fact. The
orchestrator read the code instead, against `9ddb38a`.

- **How Codex writes today.** `run_codex` (`scripts/stage2.py`) starts
  `codex exec --json -m gpt-6.1-sol -c model_reasoning_effort="max"` with
  `sandbox_mode="workspace-write"` when `writable` is set (`read-only` for a
  review), disables hooks and memories, takes no bypass flag, and reads the
  answer from the file given with `-o`. It returns the answer and the thread
  id; `resume` continues a recorded thread. No time limit is passed to
  `launch` for Codex.
- **The draft route is the precedent.** `draft` loops over its own routes
  (`codex`, `codex-repair`, then `glm`), calls `run_codex(..., writable=True)`
  for Codex and `run_work_model` otherwise, and stops when a call moved HEAD
  rather than rewrite a commit the model made.
- **The repair route today.** `repair` builds its routes as
  `(endpoint, credential, route, reason)` — GLM 5.3, GLM 5.3 again with the
  first attempt's diagnostics, then Sonnet 5.5 — or Sonnet alone under
  `--stage2-off`, and hands them to `run_attempts`.
- **What is GLM-specific.** `run_attempts` calls only `run_work_model`
  (Claude Code with `glm_env` or the stage-1 Claude environment); it has no
  Codex branch. The credential scan (`remove_changed_credential`) runs only
  when a GLM key was read. The post-run checks — `verify_attempt` (format,
  `make verify`, the Time-used line), `check_repair_answer` (one fix line per
  taken row, red-first proof per test) and the checkpoint commit — do not
  depend on the model.
- **The reviewer's own findings.** `review` resumes the recorded Codex thread
  for the loop marks (`run_codex(ctx, marks_prompt, resume=thread)`); a
  phase-6 re-review after a repair starts a fresh Codex session
  ("a fresh session reviewed" in `findings.md`).
