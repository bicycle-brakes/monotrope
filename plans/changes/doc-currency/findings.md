---
title: "Findings — doc-currency"
category: findings
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — doc-currency

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1174 files, 5429 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/doc-currency/draft-attempt-1-20261123T062549064027Z (8991b90a1309); `git diff bbf3e61bd503 refs/stage2/attempts/doc-currency/draft-attempt-1-20261123T062549064027Z` shows it.

Stage-2 call, 2026-11-23: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1175 files, 5429 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/doc-currency/draft-attempt-2-20261123T062605593732Z (24a1420144a7); `git diff bbf3e61bd503 refs/stage2/attempts/doc-currency/draft-attempt-2-20261123T062605593732Z` shows it.

Stage-2 call, 2026-11-23: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1175 files, 5429 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.3","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/doc-currency/draft-attempt-3-20261123T063600278932Z (52e19ffe93fd); `git diff bbf3e61bd503 refs/stage2/attempts/doc-currency/draft-attempt-3-20261123T063600278932Z` shows it.
