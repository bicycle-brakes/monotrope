---
title: "Research — enqueue-pr-rulesets"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-3wtk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-27", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# enqueue pr rulesets — Research

## Topic (bead coding-harness-3wtk)

Class: bounded. Observed 2026-11-27 (main `f4352686`) on PR #477:
`scripts/enqueue_pr.py <n>` refuses every pull request for two reasons in the
script itself.

1. `checks: the required checks of main could not be read: gh api
   repos/bicycle-brakes/monotrope/branches/main/protection/required_status_checks
   failed: gh: Branch not protected (HTTP 404)`. `repos/.../branches/main`
   reports `protected: true` because ruleset `24528176` ("main") is active,
   while classic branch protection does not exist; the script (around line
   383) tolerates only a 404 containing "Required status checks not enabled".
2. `phase-6: an unrecognised table line in the released block: Loop state:
   {...}`. `scripts/stage2.py:505-507` writes `Loop state: ` (`STATE_KEY`) as
   the released loop block's own line after `release-loop`, but the block
   parser of `enqueue_pr.py` (around lines 585-590) rejects it.

Effect: no pull request can enter the merge queue through the one allowed
route (AGENTS.md rule 8). What: treat the 404 "Branch not protected" answer as
no classic protection and rely on the ruleset rules already read; accept
exactly the runner's `Loop state: ` line in a released block; keep every other
failure unreadable (fail closed). Acceptance: tests with a fake `gh` answering
`protected: true` plus that 404 admit on green ruleset checks; other 404/403
texts still refuse; a released block with the runner's `Loop state:` line
parses, a different unknown line still refuses. This change edits
`enqueue_pr.py` itself, so the maintainer merges it (bootstrap exception).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-27: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1319 files, 6132 commits, 12 rules.

## Runner exploration — 2026-11-27

Research for enqueue-pr-rulesets (bead coding-harness-3wtk, class bounded). I read only the repository, with Grep, Glob and Read. Nothing was run, nothing was written, and the GitHub ruleset and PR #477 were not checked live.

## What exists today

**The script and its two refusals.** `scripts/enqueue_pr.py` is the one admission command. Its module docstring lists the conditions in report order: `script`, `pr`, `head`, `change`, `trailer`, `phase-6`, `reviewed-commit`, `post-review`, `checks`, `decision`. The `checks` condition calls `GitHub.required_checks(BASE_BRANCH)` and passes the result to `checks_problems`. The `phase-6` condition is assembled in `_attended_conditions`, which calls `phase6_problems` and `released_problems` on the head's `findings.md`.

**Failure 1: the ruleset-only 404.** `GitHub.required_checks` in `scripts/enqueue_pr.py` works in three steps:
1. It reads the active rules from `repos/{o}/{r}/rules/branches/{branch}`.
2. It reads `repos/{o}/{r}/branches/{branch}` and takes its `protected` flag.
3. If `protected` is true, it reads `.../branches/{branch}/protection/required_status_checks`. It accepts a 404 only when the diagnostic contains `Required status checks not enabled`. Any other error raises `Unreadable`.

Step 2 already tolerates `Branch not protected` (HTTP 404) and treats the branch as unprotected. Step 3 does not. So when a ruleset makes `protected` true and no classic protection exists, step 3's 404 `Branch not protected` refuses the request. The topic's observed text matches this path. The existing test `test_required_checks_union` in `tests/test_enqueue_pr.py` covers the unprotected case, where step 2 returns `Branch not protected` and the result is the ruleset's checks alone. No test covers `protected: true` followed by a `Branch not protected` 404 on the protection endpoint. The tests also cover a 403 at step 3, which must refuse.

**Failure 2: the runner's `Loop state:` line.** `scripts/stage2.py` defines `STATE_KEY = "Loop state: "` and `STATE_LINE`, a line-anchored match for `Loop state: {json}`. The function that builds the released block appends `STATE_KEY` followed by the state JSON as its own line, before the `Kept from the loop record:` line. `read_state` in `stage2.py` reads this line back as the run's stage snapshot. `enqueue_pr.py` does not know this line. In `released_problems`, a line inside the `## Phase 4b — loop rows, released` section that is not a row and contains a `|` (and does not start with `>`) is reported as `an unrecognised table line in the released block`. The topic's observed message has that shape. The `|` appears only if the state JSON contains one, which I did not verify from a real released block. `phase6_problems` has the same rule for `## Phase 6` blocks. No test in `tests/test_enqueue_pr.py` mentions `Loop state`.

**Conditions the fixes would sit beside.** The fail-closed rule is in the module docstring and in `union_required` and `released_problems`: unreadable evidence is always a refusal (`Unreadable` is documented as "always a refusal, never a pass"). The spec at `plans/changes/enqueue-pr/spec.md` requires this, in criteria 8, 10, 23 and 24, and the non-goals and decisions there say the same.

**Neighbours.**
- `plans/changes/enqueue-pr/spec.md` (active, bead `coding-harness-va1l`, class bounded). It owns this script and its spec. Its findings file records a rejected finding F-3 about the empty required set (`decisions.md` S-34), which concerns the same `checks` code.
- `plans/changes/enqueue-pr/research.md` (bounded, same bead family). Its "Ruleset" and "Loop state" content is absent; it mentions required checks in its "What is unclear" item 5.
- `plans/changes/archive/2026-11-06-merge-queue/spec.md` (archived). The merge queue's admission rules; its research and findings were not read.
- `decisions/gates.yaml`, gate `ruleset`: runs `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs` and reads the ruleset live with the maintainer's own login. It is listed as writer-only. This is the existing check of the ruleset, and it is not a gate that runs in CI.
- `templates/repo-settings.md`: describes the ruleset (require pull request, required check named `verify`, merge queue or up-to-date rule, block force pushes). Its read-back command is `gh api repos/<owner>/<repo>/rules/branches/<branch>`.

**Header state.** The current `plans/changes/enqueue-pr-rulesets/research.md` has no `neighbours:` header and no `class:` in its frontmatter. Its topic line says `Class: bounded`. `plans/changes/enqueue-pr/research.md` has `neighbours: []`, and its `spec.md` has `class: bounded`.

## Where it lives

- `scripts/enqueue_pr.py`: the script. `GitHub.required_checks`, `union_required`, `checks_problems`, `phase6_problems`, `released_problems`, `_attended_conditions`.
- `scripts/stage2.py`: `STATE_KEY`, `STATE_LINE`, `RELEASE_HEADING`, `KEPT_FROM`, and the released-block builder that writes the state line.
- `tests/test_enqueue_pr.py`: `test_required_checks_union` (near line 695), `released` and `phase6` helpers (around lines 65 and 321), `test_released_loop_rows_and_disagreements_refuse`, `test_malformed_released_row_refuses`, and the parametrised malformed-line test near `section == "released"`.
- `templates/repo-settings.md` and `tests/test_repo_settings.py`: the ruleset template and its test.
- `decisions/gates.yaml`: the `ruleset` gate.

## What is unclear

1. **The live ruleset.** The topic gives ruleset id `24528176` ("main") and PR #477 as the observed state. Neither is in the repository, and I did not query GitHub. Whether the protection endpoint returns exactly `Branch not protected` with HTTP 404 for a ruleset-only branch is taken from the topic's quoted error and is not verified here.
2. **The state line's contents.** I did not read a released block with a real `Loop state:` line. The claim that the JSON holds a `|` is an inference from the topic's error text, which only the pipe check in `released_problems` can produce.
3. **The bead text** `coding-harness-3wtk` was not read (no tracker access in this phase). The topic's acceptance wording is taken from the change's own `research.md`.
4. **Ruleset 24528176's required check list** is not in the repository. The repository's own statement is that the required check is `verify` (`templates/repo-settings.md`); whether the live ruleset names more is open.
5. **Two readers of the same condition.** Whether the runner's state line should be read by a shared constant or by its own pattern is not stated in any source read here.
6. **`tests/test_repo_settings.py`** and the `ruleset` gate body were only matched, not read in full.
7. **`plans/changes/archive/2026-11-06-merge-queue/`** was not read.

## Which files a change would have to touch

- `scripts/enqueue_pr.py`: `GitHub.required_checks` (the protection endpoint's 404 handling when `protected` is true) and `released_problems` (or `phase6_problems`) for the state line.
- `tests/test_enqueue_pr.py`: new cases beside `test_required_checks_union` for `protected: true` with the 404 text, and beside the released-block tests for the `Loop state:` line, including a different unknown line that must still refuse.
- `plans/changes/enqueue-pr-rulesets/research.md`: the `neighbours:` header and, if the maintainer wants it, a `class:` line in its frontmatter.
- `scripts/stage2.py` would change only if the state line's format changes. The topic does not ask for that, so it is not expected to change.
- `plans/INDEX.md`: regenerated by `scripts/plans_registry.py --index` after a header edit.

Header for the runner: the neighbours I know are `plans/changes/enqueue-pr/spec.md` and `plans/changes/archive/2026-11-06-merge-queue/spec.md`. Add them to the header of `research.md` as `neighbours:` before the swarm runs.
