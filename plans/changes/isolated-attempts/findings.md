---
title: "Findings — isolated-attempts"
category: findings
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — isolated-attempts

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1168 files, 5417 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/isolated-attempts/draft-attempt-1-20261122T235341954952Z (295feb1d8d0b); `git diff b12fa3c3dfad refs/stage2/attempts/isolated-attempts/draft-attempt-1-20261122T235341954952Z` shows it.

Stage-2 call, 2026-11-23: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1169 files, 5417 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/isolated-attempts/draft-attempt-2-20261122T235356283411Z (c70df113a37a); `git diff b12fa3c3dfad refs/stage2/attempts/isolated-attempts/draft-attempt-2-20261122T235356283411Z` shows it.

Stage-2 call, 2026-11-23: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1169 files, 5417 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.3","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/isolated-attempts/draft-attempt-3-20261123T001221111819Z (c2e275bea16d); `git diff b12fa3c3dfad refs/stage2/attempts/isolated-attempts/draft-attempt-3-20261123T001221111819Z` shows it.
>
> The runner put back:
> - `docs/adr/0026-isolated-writing-attempts.md`
> - `plans/changes/isolated-attempts/design.md`
> - `plans/changes/isolated-attempts/plan.md`
> - `plans/changes/isolated-attempts/spec.md`
