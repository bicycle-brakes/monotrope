---
title: "Research — merge-queue"
status: draft
implementation_status: partial
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-eh42
owner: framework-architect
class: bounded
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# merge queue — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), by the
runner's GLM Flash route; the orchestrator's measured addendum closes its gaps.

Stage-2 call, 2026-10-30: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 773 files, 2742 commits, 12 rules.

## Runner exploration — 2026-10-30

Die Recherche ist vollständig. Hier das Ergebnis als Text, bereit zum Einfügen in `plans/changes/merge-queue/research.md` (nur der Runner schreibt die Datei).

---

**Suggested `neighbours:` header** (paths to neighbouring change specs; the runner places it in the frontmatter):

```
neighbours:
  - plans/changes/archive/2026-10-08-rb-g7-merge-freshness/spec.md
  - plans/changes/index-merge-regenerates/spec.md
  - plans/changes/harness-decide-adr/spec.md
  - plans/changes/ci-minutes/spec.md
  - plans/changes/hermes-runner/spec.md
```

---

## What exists today

**The change itself.** `plans/changes/merge-queue/` holds only the empty `research.md` skeleton (frontmatter `provenance: human-written`, bead `coding-harness-eh42`); it was opened by commit `1bf4cdff` ("change(merge-queue): open the change folder (bead coding-harness-eh42)") on branch `fix/merge-queue`. `plans/INDEX.md` lists the row as draft, implementation none, dated 2026-10-30. No `spec.md`, no `class:` declaration exists in the folder yet. The `docs/research/2026-10-28-night-run-plan.md` ("Not tonight" section) names coding-harness-eh42 among the **decision pull requests** that "need the maintainer" (alongside -fctf, -pwdi, -k0ub). The bead's own title, description and class live in the Dolt tracker under `.beads/` and could not be read in this phase (no shell access; only `metadata.json`, `config.yaml`, `interactions.jsonl` and hooks are committed, no rendered copy per house rule 2) — an open question, not a guess.

**A merge queue was explicitly deferred once.** The archived spec `plans/changes/archive/2026-10-08-rb-g7-merge-freshness/spec.md`, section "Non-goals", states: "A merge queue, auto-update of branches or auto-merge. Each would take the update off the maintainer's hands; none was asked for." That change instead built the manual machinery: the CI checks GitHub's merge ref (`tests/test_ci.py::test_the_verification_runs_against_the_merge_ref`), and the ruleset requires branches to be up to date before merging (RB-G7, `strict_required_status_checks_policy`).

**The merge procedure is a written procedure, not a queue.** `prompts/07-commit.md`, section "The merge": the maintainer merges or asks an agent; the agent restates, then runs `gh pr merge <n> --merge --match-head-commit <sha>`; `--admin` is never used; a behind branch is updated with `gh pr update-branch <n>`, CI waited green, restatement repeated (steps 5–7, carrying RB-G7). ADR 0008 (`docs/adr/0008-merge-confirms-a-decision.md`) makes the maintainer's merge the confirmation of a decision; `docs/WORKFLOW.md` §2 "Change classes, the ADR question and decision pull requests" repeats the doctrine and its limits.

**Merges are brake-guarded, not locked.** `.claude/settings.json` `permissions.ask` carries eight merge ask rules; `scripts/merge_guard.py` (`MERGE_ASK_RULES`, with samples) is the one list, and `tests/test_merge_guard.py` (nine tests, e.g. `test_settings_ask_before_every_merge`) holds settings and list together. The rules cover `gh pr merge` in its spellings, the REST merge endpoint, the GraphQL `enablePullRequestAutoMerge` mutation (auto-merge), `gh alias set`, pushes to main, and any GitHub MCP merge tool. `docs/WORKFLOW.md` §2 "What this does not do" names the pass-around spellings (curl, `sh -c`, moved flags, GraphQL from a file).

**Auto-merge is the current practice, gated on the ruleset.** `templates/repo-settings.md` says auto-merge (`allow_auto_merge=true`) is switched on "only after" the default-branch ruleset is active, armed per pull request with `--match-head-commit`, never for decision pull requests; the kit manifest records it as the hosting-settings mechanism (mechanismus entry for `templates/repo-settings.md`, maintainer 2026-10-27). Night runs mark ready pull requests instead of merging; the morning handover lists them with head commits and one maintainer word merges them through GitHub's auto-merge with a single prompt (`docs/research/2026-10-28-night-run-plan.md`, "Merge rules tonight"; `docs/orchestration.md`, "Merges and the morning"; bead coding-harness-m254; handover `docs/journal/handover/2026-10-29-three-lane-night.md`, question 1). The portable template `templates/agents-mergeable-prs.md` carries a "Merged when green, without waiting" arming bullet; the repository's own rule text (`docs/WORKFLOW.md` §3 "Pull requests stay mergeable", mirrored by `AGENTS.md` line 187) has no such bullet — the two texts differ on that point.

**The manual merge-day precedent.** `docs/journal/handover/2026-10-21-merge-day.md` records a hand-driven queue: about ten open pull requests merged strictly one at a time, each with content review, local `make verify`, green hosted CI, merge of `main` into stacked branches (never rebase), `--match-head-commit`, and decision pull requests restated first. That handover's third addendum declares the queue closed ("the merge queue is empty").

**The mergeability rules that stand in for a queue today.** `docs/WORKFLOW.md` §3 "Pull requests stay mergeable" (born from the five parked pull requests of 2026-10-27, bead coding-harness-s05q, assessed in `docs/research/2026-10-27-parked-runner-prs.md`): daily sync on request by the helper, ask after five working days, ~800-line slices, at most three open pull requests per hot file, phase 6 on a current base, no stacking without a reason, generated index regenerated, hot files split. The helper is `scripts/pr_sync.py` (commands `sync` and `merge-main`, exact-head lease pushes, skip/protect policy for decision pull requests and human-decided paths), tested by `tests/test_pr_sync.py`; its remaining work is the active change `plans/changes/index-merge-regenerates/` (spec draft, review round 3 parked on the Go usage limit per the 2026-10-29 handover).

**The ruleset floor test knows six requirements, not a queue.** `tests/test_repo_settings.py` (module docstring and `RULE_TYPES` dict) asserts: pull request required, required check `verify` pinned to the GitHub Actions app, no force push, no deletion, empty bypass lists, and branches up to date (`UP_TO_DATE_OPTION`). It measures live only in the gate `ruleset` (`RULESET_ASSERT=1`, `placement: writer` in `decisions/gates.yaml`). GitHub's merge queue appears as a ruleset rule type of its own; this file has no notion of it (searched `merge_queue` — no match in `tests/`, `scripts/`, `templates/`).

**The hosted workflow has no merge-group event.** `.github/workflows/ci.yml` triggers only on `push`, `pull_request` and a nightly `schedule` cron; both job `if:` conditions name only `push` and `pull_request`. The generator `scripts/ci_gates.py` (`generate_ci`) writes the same three triggers; a `merge_group` trigger is not there (searched — no match). GitHub's merge queue fires checks on `merge_group` events, so queued merges would run no check this workflow knows. `plans/changes/ci-minutes/spec.md` (draft, bounded) records the CI economy this touches: roughly 3.5 minutes per run, and GitHub Actions stopped starting jobs on 2026-10-13 over payment/spending limits.

**The post-merge close step is documented but absent.** `prompts/07-commit.md` says "After the merge, `make close-merged ARGS=--write` closes what was declared"; the `Makefile` (read in full) has no `close-merged` target, no `scripts/*close*` file exists, and nothing under `scripts/` reads `Closes-Bead`. Two handovers of 2026-10-08 (`docs/journal/handover/2026-10-08-runner-derived-close-claude.md`, `-runner-derived-files.md`) noted the same absence at that base; whether a bead owns it could not be read from the tracker.

**What the research corpus says about the pattern.** `docs/research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md` (German): the "Abgrenzung" paragraph after table AG deliberately does **not** adopt the full-orchestrator (Gas Town) with its merge queues; the risk table's "Paralleler Blast Radius" row names the "Merge-Queue-Muster als KANN bei hoher Parallelität" beside sequential merging (P6-2); decision ADW-D09 makes the pull request the last gate with no agent merge and lists "Auto-Merge bei grüner CI" as a rejected alternative. `docs/research/Lake-Switch-Architektur-arc42.md` §8.1.3 notes for the LakeSwitch instance that `Fixes #N` must stand in the PR body because pull requests merged through a merge queue do not close issues from the commit trailer alone.

## Where it lives

Procedure and doctrine: `prompts/07-commit.md` ("The merge"), `docs/WORKFLOW.md` §2 (decision doctrine, "What this does not do") and §3 ("Pull requests stay mergeable", "Night runs"), `docs/orchestration.md` ("Merges and the morning"), `AGENTS.md` (mergeable-PR summary line), `docs/adr/0008-merge-confirms-a-decision.md`, the decision template `.github/PULL_REQUEST_TEMPLATE/decision.md`. Enforcement: `.claude/settings.json`, `scripts/merge_guard.py`, `tests/test_merge_guard.py`. Hosting settings: `templates/repo-settings.md`, `templates/agents-mergeable-prs.md`, kit entry in `scripts/kit/manifest.yaml`. Ruleset measurement: `tests/test_repo_settings.py`, gate `ruleset` in `decisions/gates.yaml`. Sync and merge engine: `scripts/pr_sync.py`, `tests/test_pr_sync.py`. CI surface: `scripts/ci_gates.py`, `.github/workflows/ci.yml`. History and precedent: `plans/changes/archive/2026-10-08-rb-g7-merge-freshness/` (spec, plan), `docs/journal/handover/2026-10-21-merge-day.md`, `docs/research/2026-10-27-parked-runner-prs.md`, `docs/research/2026-10-28-night-run-plan.md`, `docs/journal/handover/2026-10-29-three-lane-night.md`.

## What is unclear about it

- **The bead's own words.** Title, description and class of coding-harness-eh42 are in the Dolt tracker, which this phase cannot read (`tools/bd show coding-harness-eh42` is the runner's or maintainer's read). The night plan's grouping with decision pull requests is the only committed evidence of its kind.
- **Which "merge queue" is meant.** Not stated in any committed file: GitHub's hosted merge queue (a ruleset rule type plus `merge_group` CI events), a repository-local queue script or gate, or a doctrine/template decision only. The branch name `fix/merge-queue` suggests code but decides nothing.
- **The live GitHub settings today.** Last measured reads: 2026-10-05, `allow_auto_merge: false`, rulesets `[]` (`plans/changes/hermes-runner/research.md` §3.1); 2026-10-08, the up-to-date flag live `false` (rb-g7 spec). Nothing in the tree records the current values; the gate `ruleset` measures them only at run time on the writer machine. Whether the merge-queue rule type is even available on this account's plan is unknown — the same research notes the plan itself was not readable through the API (`plan: null`).
- **The absent `make close-merged`.** Documented in `prompts/07-commit.md`, absent from `Makefile` and `scripts/` since at least 2026-10-08; no owning bead could be read from the tracker in this phase.
- **The class declaration.** The research skeleton declares none; `spec.md` does not exist yet, so the runner's class sources (`--class`, research header, spec header) cannot agree or disagree — there is nothing to read.

## Which files a change would have to touch

Any variant lands on one or more of these surfaces; which ones is the decision's, not the research's:

- **Doctrine texts:** `docs/WORKFLOW.md` §3 "Pull requests stay mergeable" and/or §4 "Night runs"; `docs/orchestration.md` "Merges and the morning"; `AGENTS.md` line 187 area; `prompts/07-commit.md` "The merge" (its steps 5–7 — `--match-head-commit`, `update-branch` — are what a queue would replace or surround).
- **Hosting settings texts:** `templates/repo-settings.md` (merge-queue rule type versus the up-to-date option), `templates/agents-mergeable-prs.md` (the arming bullet), the kit manifest entry beside them.
- **Enforcement:** `.claude/settings.json`, `scripts/merge_guard.py`, `tests/test_merge_guard.py` — only if merge commands change shape.
- **Ruleset floor:** `tests/test_repo_settings.py` (`RULE_TYPES`, the docstring's six requirements) — only if the ruleset gains a seventh requirement.
- **CI:** `scripts/ci_gates.py` (`generate_ci`) and `.github/workflows/ci.yml` — only if queued merges must run checks (`merge_group`); interacts with the standing decisions of `plans/changes/ci-minutes/`.
- **Sync engine:** `scripts/pr_sync.py`, `tests/test_pr_sync.py` — only if the sync's eligibility/skip policy must treat queued branches differently; the neighbouring change `plans/changes/index-merge-regenerates/` is mid-flight on the same engine.
- **If it is a decision pull request:** no file beyond the texts above — the decision mechanics (`decide(` title, `decision` label, `.github/PULL_REQUEST_TEMPLATE/decision.md` block, house rule 8 merge-by-the-maintainer) already exist and ask for nothing new.

## Orchestrator addendum — measured 2026-10-30 (closes the gaps above)

- **The bead's words** (bead coding-harness-eh42, read with `tools/bd show`):
  class bounded; "repository setting plus tests/test_repo_settings.py and
  templates/repo-settings.md; decision PR, the maintainer merges". Measured
  2026-10-27/28: every merge on main put the other open pull requests BEHIND;
  `update-branch` gave them a new head, so auto-merge armed with
  `--match-head-commit` no longer fired (PRs #250, #262, #264, #265). The
  maintainer approved the switch to a GitHub merge queue on 2026-10-28.
- **Which queue.** GitHub's hosted merge queue: the ruleset rule type
  `merge_queue` plus the `merge_group` event for the required check.
- **Live settings, 2026-10-30 ~14:15 UTC.** The repository is owned by an
  organization on the Team plan and is public (`gh api`), so the hosted
  merge queue is available. Ruleset `main` (id 24528176, active):
  `deletion`, `non_fast_forward`, `pull_request`, and
  `required_status_checks` with `verify` (integration 15368) and
  `strict_required_status_checks_policy: true`. Repository:
  `allow_auto_merge: true`, merge commits and squash allowed.
- **Measured cost today.** Merging eight pull requests one at a time on
  2026-10-30 (#279, #277, #285, #282, #280, #283, #281, #287) needed an
  update and a fresh CI run before almost every merge.
- **RB-G7 is the rule that changes.** `docs/governance/regelwerk.md`
  (`human-decided`) states that the ruleset requires a branch to be up to date
  before merging, enforced by `tests/test_repo_settings.py`. A merge queue
  tests the merge result itself, which is what RB-G7 protects, so the change
  is a decision pull request.
- **`make close-merged`** is out of scope here.

## Draft gap check — 2026-10-30, base `bdfbe53f`

- `scripts/ci_gates.py` splits the matrix event condition (`generate_ci`)
  from the summary condition (`_summary_job`); both exclude `merge_group`.
  `tests/test_ci.py::test_the_schedule_runs_only_the_drift_job` asserts the
  exact old conditions, so adding only the trigger cannot meet the goal.
- `docs/governance/quality-gates.md`, the current MG-2 explanation, explicitly
  requires branch updates and cites merge step 7; it needs the same queue
  alternative as the rulebook. The rulebook's §4 requires a version increase
  and four impact lines for every edit; its current version is 5.0.0.
- `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent
  from this tree. The plan uses the supplied phase-3 form; existing interview,
  criterion-ledger and research-handoff checks can measure their own contracts.
- The draft reads no external session registry, tracker store or live PR
  state: those are outside this attempt's worktree-only reading boundary.

