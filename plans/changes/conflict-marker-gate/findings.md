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
