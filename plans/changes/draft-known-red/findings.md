---
title: "Findings — draft-known-red"
category: findings
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — draft-known-red

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1168 files, 5378 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/draft-known-red/draft-attempt-1-20261122T152959163530Z (a5be20083f3d); `git diff 0f20c7590b1c refs/stage2/attempts/draft-known-red/draft-attempt-1-20261122T152959163530Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1169 files, 5378 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/draft-known-red/draft-attempt-2-20261122T153011450100Z (90a8d1fa4714); `git diff 0f20c7590b1c refs/stage2/attempts/draft-known-red/draft-attempt-2-20261122T153011450100Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1169 files, 5378 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5381 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | spec.md "Non-goals" (last bullet: "No ADR") and "Definition of Done" ("no ADR changes"); docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md decision 9 | [AMBIGUITY] Accepted ADR 0016 (provenance human-decided), decision 9, says: "Where Stage 2 is off, Opus 5.5 drafts by hand as §3 says; `draft` has no Stage-1 route." The spec adds exactly that route but says "No ADR" and "no ADR changes", and `docs/adr/` is a held path. Neither research.md nor decisions.md mentions decision 9. Reading A: ADR 0016 stays as it is, and after the merge the accepted ADR says the opposite of the code and of WORKFLOW §4, which cites it. Reading B: ADR 0016 gets an amendment note like its 2026-11-01 one, which touches held `docs/adr/` and breaks the DoD's "no ADR changes". The interview was skipped and the route was set as an orchestrator [DETAIL], so no human has yet decided to set aside a human-decided ADR. | Opus | in spec — maintainer answer B (decisions.md Q-1, 2026-11-22): ADR 0016 decision 9 is amended by an addendum; the spec drops 'No ADR' and names the addendum | — |
| F-2 | MAJOR | SPEC | base | spec.md "Terms" (Stage-1 route), criteria 2, 3 and 7; decisions.md [DETAIL] "`--stage2-off [REASON]` is accepted for `draft`" | [AMBIGUITY] decisions.md says the draft gets "the same Stage-1 route … as explore, implement and repair". For those verbs, `--stage2-off` runs §3's model for that phase (docs/WORKFLOW.md: "uses §3's Haiku 5.5 or Sonnet 5.5 route"; explore uses Haiku because §3 gives phase 1 to Haiku, implement uses Sonnet because §3 gives phase 4 to Sonnet). For phases 2, 2b and 3, §3 assigns Opus 5.5 at effort `xhigh` "a spike, or Stage 2 off" (maintainer, 2026-09-29, for the whole repository). Reading A, as the spec has it: Sonnet 5.5 at effort `medium`. Reading B: the phase's §3 model through the runner, so `claude-opus-5-5` at `xhigh`, and criteria 2, 3 and 7 would name a different model and effort. Under A, §3 and the held prompts 02-spec.md, 02b-design.md and 03-plan.md (all sent to the drafting model) still say Opus 5.5 at `xhigh` writes the draft when Stage 2 is off. The workflow would then give two Stage-2-off draft routes with no rule for when each applies. | Opus | in spec — maintainer answer B (decisions.md Q-1): the Stage-1 draft runs on Opus 5.5 at effort xhigh per docs/WORKFLOW.md §3, not Sonnet | — |
| F-3 | MAJOR | SPEC | base | spec.md criterion 4 | [AMBIGUITY] The criterion says "restores the worktree to the baseline outside the change folder". Reading A, taken literally: only paths outside `plans/changes/<change>/` are put back. A failed call's partial spec.md, design.md or plan.md then survives, and so does any edit the model made to decisions.md. The next `draft` run is refused by `refuse_preexisting` with exit 2. Reading B: the chain's current call-failure path, `put_back(root, baseline, allowed)` with `allowed` = findings.md only, which puts back everything except findings.md, the change folder included. The refutation ("an outside path left changed") passes under both readings, so a test cannot tell which one was built. | Opus | in spec — [DETAIL] decided by the orchestrator: reading B; a failed call puts back everything except findings.md, the change folder included, as the chain's current call-failure path does | — |
| F-4 | MAJOR | SPEC | base | spec.md criteria 1 and 2 | Missing: which endpoint the draft's preflight declaration check clears on the Stage-1 route. `draft` calls `preflight(root, change, CODEX, …)`; implement and repair pass `first = SONNET` when the flag is set. If the Codex check is kept, a Stage-1 draft exits 2 wherever the openai-codex declaration does not clear, which is one form of "Stage 2 off", the case the route exists for. Neither criterion can catch this: criterion 1's refutation names only the verb refusal ("exits 2 with that refusal"), and criterion 2 counts Codex or GLM calls, not a declaration check. | Opus | in spec — [DETAIL] decided by the orchestrator: with --stage2-off the draft's preflight clears the Opus Stage-1 declaration (claude-code-plan), not the openai-codex one, as implement and repair pass their Stage-1 model | — |
| F-5 | MAJOR | SPEC | base | spec.md criterion 8; decisions.md [DETAIL] "A failed draft keeps its work visible" | Missing: the tree state the named next step needs. When the chain's last (GLM) attempt fails its document check, the chain leaves its tree (WORKFLOW §4: "a failed post-run check leaves its tree"), and it saves no attempt ref (`save_attempt` runs only on a failed call). The next step criterion 8 names, `draft <change> --stage2-off <reason>`, is then refused by `refuse_preexisting` (exit 2, pre-existing changes outside findings.md). The spec does not say whether the message must also tell the user to discard the tree (losing unsaved work), whether a ref is saved first, or whether the Stage-1 run accepts the leftover files (a guard change the non-goals exclude). The refutation checks only the message text, so it stays green while the named command refuses. decisions.md's "the attempt refs … already hold it" is also false for this case. | Opus | in spec — [DETAIL] decided by the orchestrator: when the last attempt fails its document check, the runner saves the tree as an attempt ref first, restores the tree, and its final message names the ref and the next step draft <change> --stage2-off <reason> | — |
| F-6 | MINOR | SPEC | base | spec.md criterion 8; "Problem" bullets 1 and 3 | Missing: whether the chain's GLM-key refusal names `--stage2-off`. After two failed Codex attempts, the third route raises `GLM_KEY is not in the secrets file …` (exit 2) before any GLM call. The Problem names this case ("Z.ai is unavailable", "Where GLM is not an option either, nothing is left"). Criterion 8 covers only a run that "fails after its last allowed attempt", so this stop has no next step and no criterion. | Opus | in spec — [DETAIL] decided by the orchestrator: the GLM-key refusal on the third route also names --stage2-off as the next step | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5400 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/draft-known-red/draft-attempt-1-20261122T212659690284Z (dec8ac181f95); `git diff bb60054a37ef refs/stage2/attempts/draft-known-red/draft-attempt-1-20261122T212659690284Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5400 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/draft-known-red/draft-attempt-2-20261122T212714658309Z (07bab165f7e4); `git diff bb60054a37ef refs/stage2/attempts/draft-known-red/draft-attempt-2-20261122T212714658309Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5400 commits, 12 rules.
