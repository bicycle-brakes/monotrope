---
title: "Findings — isolated-writing-attempts"
category: findings
status: draft
implementation_status: none
date: 2026-11-24
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — isolated-writing-attempts

Stage-2 call, 2026-11-24: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5665 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0027-isolated-writing-attempts.md` +48 -0
> - `plans/changes/isolated-writing-attempts/design.md` +63 -0
> - `plans/changes/isolated-writing-attempts/plan.md` +68 -0
> - `plans/changes/isolated-writing-attempts/spec.md` +144 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: not completed; gates none; not the full `make verify`; a fresh full `make verify` is still required before phase 6
> - the attempt left more than one new ADR file: `docs/adr/0026-isolated-attempts.md`, `docs/adr/0027-isolated-writing-attempts.md`
> ```

Stage-2 call, 2026-11-24: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1208 files, 5665 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/isolated-writing-attempts/design.md` +1 -1
> - `plans/changes/isolated-writing-attempts/plan.md` +1 -1
> - `plans/changes/isolated-writing-attempts/spec.md` +3 -3
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: not completed; gates none; not the full `make verify`; a fresh full `make verify` is still required before phase 6
> - the attempt left more than one new ADR file: `docs/adr/0026-isolated-attempts.md`, `docs/adr/0027-isolated-writing-attempts.md`
> ```

Stage-2 call, 2026-11-24: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.4 · reason two Codex draft attempts failed · leak check clean over 1208 files, 5666 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.4","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/isolated-writing-attempts/draft-attempt-3-20261124T171121272561Z (4d1b4c992f9b); `git diff d0e0ed6cc8c2 refs/stage2/attempts/isolated-writing-attempts/draft-attempt-3-20261124T171121272561Z` shows it.
>
> The runner put back:
> - `docs/adr/0027-isolated-writing-attempts.md`
> - `plans/changes/isolated-writing-attempts/design.md`
> - `plans/changes/isolated-writing-attempts/plan.md`
> - `plans/changes/isolated-writing-attempts/spec.md`
