---
title: "Findings — worktree-setup-hook-race"
category: findings
status: draft
implementation_status: none
date: 2026-11-27
created: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-1ba3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — worktree-setup-hook-race

Stage-2 call, 2026-11-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1302 files, 6099 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/worktree-setup-hook-race/plan.md` +61 -0
> - `plans/changes/worktree-setup-hook-race/spec.md` +62 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `interview-minimums` (block) exited 1
> 1 finding(s):
>   - worktree-setup-hook-race (bounded): neither an interview record answered by the maintainer nor a reasoned skip stands in decisions.md
> ```

Stage-2 call, 2026-11-27: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1305 files, 6099 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `interview-minimums` (block) exited 1
> 1 finding(s):
>   - worktree-setup-hook-race (bounded): neither an interview record answered by the maintainer nor a reasoned skip stands in decisions.md
> ```

Stage-2 call, 2026-11-27: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.4 · reason two Codex draft attempts failed · leak check clean over 1305 files, 6099 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.4","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/worktree-setup-hook-race/draft-attempt-3-20261127T064611151919Z (0c368d95c8cb); `git diff 09797def8e44 refs/stage2/attempts/worktree-setup-hook-race/draft-attempt-3-20261127T064611151919Z` shows it.
>
> The runner put back:
> - `plans/INDEX.md`
> - `plans/changes/worktree-setup-hook-race/plan.md`
> - `plans/changes/worktree-setup-hook-race/spec.md`

Stage-2 call, 2026-11-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1303 files, 6101 commits, 12 rules.

Stage-2 call, 2026-11-27: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1305 files, 6102 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-27

Spec fingerprint: sha256:5cdeafbb22dc690aa307bf98d06f29e395fa78bc0b53b004771fa8e8078a12aa

Spec review commit: 2145f430b81f78757a8a79f4a0f0e575bcaa9bde

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md` criterion 2; `.beads/hooks/post-checkout:69-83` | [AMBIGUITY] Criterion 2 does not say whether it must hold without Perl. Reading A: it covers only the Perl path, where a `make venv` that exits 0 after the whole-second deadline leaves `_ls_rc` at 0, and the next step reports "not started … used up by make venv". Under A this is a change to the test only. Reading B: it covers both paths, as the parent criterion 11 does ("with or without Perl"). After `wait`, the no-Perl branch sets `_ls_rc=124` whenever `date +%s` has reached `_ls_deadline` (lines 71-76), even if the step exited 0 on its own. So a completed `make venv` that used up the budget is reported as "make venv timed out", and `_ls_stopped` then makes `bash tools/pi/install.sh` return silently with no not-started line. Under B the shell watchdog branch has to change, which comes close to the "timeout enforcement" non-goal. | Opus | in spec — Reading A (Perl path only; no-Perl watchdog untouched) recorded in AC2, Non-goals & [DETAIL] F-1..F-5 (bounded standing grant) | — |
| F-2 | MAJOR | SPEC | base | `spec.md` criterion 1 (*Refuted by*) and Open decisions [DETAIL]; `.beads/hooks/post-checkout:34,138,145` | Criterion 1 can only go red with a clock that the trust check itself moves forward, and the spec never says what drives the clock. The old hook calls `date +%s` once for the deadline (line 138), then runs `_ls_trusted`, then calls it once more in `_ls_step` (line 34). The fixed hook runs `_ls_trusted` first and then makes the same two calls. A controlled clock that answers by call order, the obvious reading of "controlled clock", gives both hooks the same values. The test is then green on the unfixed hook. To refute the criterion, the clock has to advance inside `git rev-parse` / `git merge-base --is-ancestor`. The [DETAIL] mentions only the "spent-budget path". It does not say how the clock is tied to the trust check, or whether it comes from shims on the test's PATH (`date` plus a `git` wrapper) or from a new clock hook point in the shipped hook. The implementer has to invent this, and the obvious choice produces a test that cannot fail. | Opus | in spec — PATH `git`/`date` shims advancing inside `_ls_trusted` (no hook-internal seam) recorded in AC1, Non-goals & [DETAIL] F-1..F-5 | — |
| F-3 | MINOR | SPEC | base | `spec.md` Problem bullet 1, criterion 1, Non-goals; `.beads/hooks/post-checkout:34-38,138` | [AMBIGUITY] The Problem says whole-second arithmetic "can exhaust a one-second budget before `make venv` starts". Criterion 1 removes only the trust-check time. Reading A: the remaining gap between setting `_ls_deadline` and the first `_ls_step` reading `date +%s` is accepted, because sub-second clocks are a non-goal. With `HARNESS_LANE_SETUP_TIMEOUT=1` a second boundary in that gap still produces "make venv not started: … used up by the setup". Reading B: once trust passes, the first step always starts, for example because it gets the full limit without a second clock read. That closes the race the bead names without sub-second time. The two readings lead to different hook code, and no criterion or non-goal chooses between them. | Opus | in spec — Reading B (step 1 gets full `_ls_limit` directly after `_ls_trusted` without a second clock subtraction) recorded in AC1 & [DETAIL] F-1..F-5 | — |
| F-4 | MINOR | SPEC | base | `spec.md` criterion 1 | The refutation catches only a trust check that uses up the whole budget. The criterion states something broader: trust-check time must not consume the budget at all. Suppose the clock advances by limit−1 seconds during the trust check, and the first step then runs with a 1 s alarm instead of the limit. No refutation case covers that. A fix that only resets the deadline when the first step finds it at or below 0 passes the refutation. Yet in every other case, time spent checking trust still shortens the first step. | Opus | in spec — AC1 Refuted by covers both full-budget and partial (`limit - 1`) trust-check clock advances | — |
| F-5 | MINOR | SPEC | base | `spec.md` Definition of Done, bullet 3 | The pull request's file list cannot show that "the protected block is unchanged and non-goals are unbuilt". The fix moves `_ls_deadline` inside `.beads/hooks/post-checkout`, the same file that holds the Beads-managed block, so that file is in the list either way. A sub-second clock or a redesign of timeout enforcement would also land in the same two files (the hook and `tests/test_worktree_setup_hook.py`). The file list therefore looks the same whether or not the block was edited or a non-goal was built, so this check cannot fail. Only criterion 5's comparison with `origin/main` can. | Opus | in spec — DoD bullet 3 updated to rely on Criterion 5 comparison with `origin/main` and PR diff | — |
