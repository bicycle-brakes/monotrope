---
title: "Findings — conflict-marker-gate"
category: findings
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — conflict-marker-gate

Stage-2 call, 2026-11-05: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 902 files, 3337 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5382 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | `decisions.md` "SKIP · interview"; `spec.md` Problem bullet 3, AC7, Non-goals bullet 1, Open decisions bullet 5 | [AMBIGUITY] The maintainer approved "a small helper for merging main into a change branch that stops with the conflicted paths instead of continuing". Reading A (the spec's): the existing `pr_sync.py merge-main` already is that helper, so the change only extends `tests/test_pr_sync.py`. Reading B: the orchestrator proposed the helper as something to build, so the change would add a new command or script. The spec's non-goal "no new merge command" and the protected `scripts/pr_sync.py` rule that out. The spec settles this as a `[DETAIL]`, but whether something named in the approved scope is built or reused is a scope question for the maintainer, not a detail the draft can decide. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A; the existing pr_sync.py merge-main is the helper, the change pins its stop-on-conflict behaviour with tests and names it in docs/WORKFLOW.md as the orchestrator's one way to merge main into a change branch | — |
| S-2 | MAJOR | SPEC | base | `spec.md` AC7 ("leaves the target branch, index, working files and remote branch unchanged"); Open decisions bullet 5 | [AMBIGUITY] "index" can mean Git's staging area or `plans/INDEX.md`; the existing `test_other_conflicts_preserve_target` reads it as `plans/INDEX.md` (`index_before`). "remote branch" can mean the branch on origin (what that test checks with `origin_ref`) or the local remote-tracking refs. Under the narrow reading the current helper passes, as the spec claims. Under the broad reading (every ref unchanged and `.git/index` byte-identical), a regression fails on unchanged code: `merge_main` runs `git fetch origin`, which moves `refs/remotes/origin/main` before the conflict is found, and `ensure_clean`'s `git status` can rewrite the index stat cache. Making that pass means editing the protected `scripts/pr_sync.py`. | Opus | in spec — [DETAIL] decided by the orchestrator: index means both Git's staging area and plans/INDEX.md, each unchanged; remote branch means the branch on origin, unchanged; local remote-tracking refs may move by the fetch | — |
| S-3 | MAJOR | SPEC | base | `spec.md` Terms "Named fixture exception"; AC3; AC4; AC8; DoD "Move together"; Non-goals bullet 3 | Missing: the spec requires a "reviewed allowlist" that starts empty but leaves four things undecided. (1) Where it lives: a constant in `scripts/check_conflict_markers.py`, or a data file, which the "Move together" list does not name. (2) Whether it travels with the kit as mechanism or stays per repository; if it lives in the script, a kit target that needs a fixture has to edit a travelling mechanism file. (3) How a test plants a non-empty list for AC3's sibling and prefix-match refutation, since a user-supplied skip flag is a non-goal. (4) What happens when a listed path is untracked or absent: ignored, reported, or failed. The builder would have to invent all four. | Opus | in spec — [DETAIL] decided by the orchestrator: the allowlist is a constant in scripts/check_conflict_markers.py, starts empty, travels with the kit as mechanism, names exact tracked paths only, and changes only through a reviewed pull request | — |
| S-4 | MINOR | SPEC | base | `spec.md` Open decisions bullet 4; AC5 ("a non-repository root"); AC6 ("a command different from the declared one"); Protected areas, last sentence | Missing: the `decisions/gates.yaml` schema requires `cost` (seconds or minutes), which decides whether the gate runs before admission or inside the verify slot. The spec gives job, placement, subset, floor and enforcement, but not cost. It also never states the declared command string, including whether the check takes a root argument (AC5 names a "non-repository root") or uses the working directory. AC6's refutation, and the gate-metadata mutation test it implies, compare against that string. The orchestrator alone writes the entry, so the implementer's test and the orchestrator's entry must agree on values the spec leaves open. | Opus | in spec — [DETAIL] decided by the orchestrator: declared cost in seconds, measured once on the change; it runs before admission with the other cheap document gates; the declared command is named in the spec | — |
| S-5 | MINOR | SPEC | base | `spec.md` AC4 ("When Git's whitespace/error check reports a fault" vs refutation "a trailing-whitespace fault passes in either change layer") | [AMBIGUITY] `git diff --check` follows `core.whitespace` from the invoking user's global and system config and the `whitespace` gitattribute. Reading A: the check reports whatever the local Git configuration flags, so on a machine with `core.whitespace=-blank-at-eol` trailing whitespace passes and the verdict depends on the machine. Reading B: the check pins Git's default rules, using a config override and isolated config, so trailing whitespace fails everywhere. The two readings lead to different implementations and different refuting cases. | Opus | in spec — [DETAIL] decided by the orchestrator: the gate runs git diff --check with a fixed core.whitespace value passed on the command line, so the user's global and system Git configuration cannot change the verdict; gitattributes in the repository still apply | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5384 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T155017349605Z (0274e81e5f59); `git diff 5e44bc0455b8 refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T155017349605Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5384 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T155028524517Z (00f073258976); `git diff 5e44bc0455b8 refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T155028524517Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5384 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5386 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5388 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-6 | MAJOR | SPEC | base | `spec.md` AC7 ("leaves … Git's staging area … unchanged"; refuted by "moves the staging area"); AC2 ("without changing repository content or refs"); Open decisions, bullet "Unchanged-by-merge wording (S-2)" | [AMBIGUITY] The S-2 decision says which index is meant, but not what "unchanged" is compared against. Reading A: the staged entries are the same before and after, as `git ls-files -s` or `git write-tree` shows. The current helper passes this. Reading B: `.git/index` is byte-identical. `merge_main` runs `ensure_clean` (`git status --porcelain`) before it reports a conflict. `git status` rewrites the index file when entries are racily clean, which they are in a disposable-repo test that commits and runs within the same second. Under B, an AC7 regression test fails on unchanged code, and it can only pass by editing the protected `scripts/pr_sync.py`. AC2 has the same split for the check itself: its worktree `git diff --check` may write a refreshed stat cache, which breaks AC2 under B and not under A. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A; unchanged means the same staged entries before and after (git ls-files -s), not a byte-identical .git/index | — |
| S-7 | MAJOR | SPEC | fix-r1 | `spec.md` AC4 ("a user's global and system Git configuration cannot change the verdict while repository `.gitattributes` still apply"; refuted by "a machine whose Git configuration disables a whitespace rule"); Open decisions, bullet "Whitespace verdict (S-5)" | [AMBIGUITY] The S-5 decision pins only `core.whitespace` with `-c`. `git diff --check` also obeys the `whitespace` attribute from the global attributes file (`core.attributesFile`, by default `~/.config/git/attributes`), from the system `gitattributes` and from `.git/info/attributes`, and that attribute overrides `core.whitespace` per path. A global `core.autocrlf` also decides whether a trailing CR on an unstaged CRLF line is reported. Reading A: "Git configuration" means config variables only, so a machine with `* -whitespace` in its global attributes file may pass trailing whitespace, and the refutation does not cover that. Reading B: the verdict must not depend on the machine, so the check must also neutralise global and system attributes and config. Under B the spec must also say whether the untracked `.git/info/attributes` counts as "repository `.gitattributes`". A test that plants a global attributes file goes red under B against an implementation built exactly to the stated mechanism. | Opus | in spec — [DETAIL] decided by the orchestrator: the gate also neutralises attribute sources outside the repository (core.attributesFile set empty on the command line, GIT_ATTR_NOSYSTEM=1); .git/info/attributes and the committed .gitattributes still apply | — |
| S-8 | MINOR | SPEC | fix-r1 | `spec.md` Open decisions, bullet "Helper (S-1)" and the sentence "its status stands in `findings.md`"; DoD "Move together"; `findings.md` S-1 Status | [AMBIGUITY] The S-1 status that the spec points to says the change "names it in docs/WORKFLOW.md as the orchestrator's one way to merge main into a change branch". The spec instead says merge-main is "already named in `docs/WORKFLOW.md` §3 … not rebuilt", and `docs/WORKFLOW.md` is not on the "Move together" list. Reading A: no doctrine edit, because §3's existing "supported local merge" sentence is enough, and the pull request touches no workflow document. Reading B: the change adds wording that makes merge-main the orchestrator's required way to merge main into a change branch. That is the gap the `31d35400` trigger exposed. Under B, `docs/WORKFLOW.md` (kit mechanism) and possibly its portable form `templates/agents-mergeable-prs.md` join a file list that the DoD says demonstrates the scope. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A; no doctrine edit, the existing supported-local-merge sentence in docs/WORKFLOW.md §3 names merge-main; the S-1 status wording is superseded by this | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5389 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T182613975018Z (2fbc8a5f370a); `git diff 21a30f1c1ae7 refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T182613975018Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5389 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T182628863827Z (f8cdc8dacc7c); `git diff 21a30f1c1ae7 refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T182628863827Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5389 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5390 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-9 | MAJOR | SPEC | fix-r2 | `spec.md` AC4 (body "the verdict is identical whatever the invoking user's global and system Git configuration … say" vs refutation "… configuration or attribute files disable a whitespace rule"); Open decisions, bullets "Whitespace verdict (S-5)" and "Attribute sources outside the repository (S-7)" | [AMBIGUITY] The decided mechanism pins `core.whitespace`, empties `core.attributesFile` and sets `GIT_ATTR_NOSYSTEM=1`. Other global or system configuration still changes what `git diff --check` compares, most plainly `core.autocrlf` and `core.eol`. With global `core.autocrlf=true`, Git converts a CRLF line added to an unstaged change in a file committed with LF before diffing, so no fault is reported. Without it, the trailing CR is reported as `blank-at-eol`. S-7 named `core.autocrlf`, but its decision covered attribute sources only. Reading A: the three listed means are the whole requirement, and the body's "whatever … configuration" is read through the narrower refutation ("disable a whitespace rule"). The CRLF case then stays machine-dependent and AC4 holds. Reading B: the body governs, so the check must also neutralise line-ending and filter configuration. It can do that per variable or by isolating global and system configuration wholesale (`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM`), which also drops settings a checkout may rely on, such as `safe.directory`. Refuting case under B: `GIT_CONFIG_GLOBAL` names a file with `core.autocrlf=true`, and an unstaged change adds a CRLF line. An implementation built exactly to the listed mechanism stays green there, which refutes AC4. | Opus | in spec — [DETAIL] decided by the orchestrator: the gate runs every git call with GIT_CONFIG_GLOBAL=/dev/null and GIT_CONFIG_NOSYSTEM=1 in addition to the S-5/S-7 settings, so no global or system configuration of any kind reaches the verdict; repository configuration and committed attributes still apply | — |
| S-10 | MINOR | SPEC | base | `spec.md` Terms "Tracked text" (no NUL byte anywhere); AC3 ("binary files … do not cause marker findings"; refuted by "a binary … marker is scanned"); AC4 ("reports a fault in staged or unstaged changes … the check fails with its diagnostic") | [AMBIGUITY] The spec calls a file binary when it holds a NUL byte anywhere. `git diff --check` treats a file as binary only when a NUL appears in its first 8000 bytes or an attribute marks it binary. Planted input: a staged or unstaged change adds a `<<<<<<< x` line to a file whose first NUL comes after byte 8000. Git reports "leftover conflict marker" for that file, but the spec classes the file as binary. Reading A: AC4 governs, so every `git diff --check` fault fails the check. This binary file then causes a marker finding, which refutes AC3. Reading B: AC3 governs, so the check must drop Git's marker diagnostics for paths it classes as binary. That needs a per-path filter over Git's output that AC4 does not mention, and it refutes AC4's "fails with its diagnostic". The two readings lead to different code and opposite verdicts for the same planted file. | Opus | in spec — [DETAIL] decided by the orchestrator: binary follows Git's own definition (a NUL byte in the first 8000 bytes, or a binary attribute) for both the marker scan and the whitespace check, so the two never disagree | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5392 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T204659101373Z (dc4326aa6cc0); `git diff 0db5abf6d256 refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T204659101373Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5392 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T204710371923Z (14325cc06d1d); `git diff 0db5abf6d256 refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T204710371923Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5392 commits, 12 rules.
