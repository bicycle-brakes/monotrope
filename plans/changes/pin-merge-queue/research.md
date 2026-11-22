---
title: "Research — pin-merge-queue"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-tsdr
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# pin merge queue — Research

Stage-2 call, 2026-11-22: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1167 files, 5317 commits, 12 rules.

## Runner exploration — 2026-11-22

Research complete. This is the phase-1 result for `pin-merge-queue`, ready to append to `plans/changes/pin-merge-queue/research.md` (only the runner writes the file).

---

**Suggested `neighbours:` header** (paths to neighbouring specs; the runner places it in the frontmatter — the skeleton's frontmatter carries none today):

```
neighbours:
  - plans/changes/archive/2026-11-06-merge-queue/spec.md
  - plans/changes/archive/2026-10-08-rb-g7-merge-freshness/spec.md
  - plans/changes/archive/2026-11-06-ci-minutes/spec.md
  - plans/changes/harness-decide-adr/spec.md
```

## What exists today

**The change itself.** `plans/changes/pin-merge-queue/` holds only the `research.md` skeleton (frontmatter `bead: coding-harness-tsdr`, `provenance: human-written`, `status: draft`; no `neighbours:` header, and no `class:` declaration anywhere in the folder yet — there is no `spec.md` to disagree with). `plans/INDEX.md` lists the row as draft, implementation none, dated 2026-11-22 (`plans/INDEX.md`, "changes/pin-merge-queue/research.md" row). The branch is `test/pin-merge-queue`; the folder was opened by commit `d90adc02` ("chore(pin-merge-queue): open change folder for coding-harness-tsdr"). The bead's own title, description and class live in the Dolt tracker under `.beads/`, which commits only `metadata.json`, `config.yaml`, `interactions.jsonl` and hooks (house rule 2 — no rendered copy); a search of `interactions.jsonl` for `tsdr` found no match, so the bead body was not readable in this phase — an open question, not a guess.

**This change is the deferred half of the predecessor.** The archived spec `plans/changes/archive/2026-11-06-merge-queue/spec.md`, section "Boundary", first bullet ("Accepted limit, queue parameters (maintainer, 2026-10-30, 'Erst messen, dann pinnen')") states it verbatim: the local ruleset check accepts any active merge queue as the freshness alternative and does not pin its merge method or group sizes; criterion 9's merge commits and groups of one are read back live once after activation (its plan step 6); "Pinning them in the local check waits for the field names GitHub reports on the live rule, in follow-up bead coding-harness-tsdr; the fixtures' parameter names are not measured." The predecessor's review loop recorded the same limit twice as rejected rows: L1-8 (the fixture omits `max_pull_requests_to_build`, "the build-group size the spec requires to be one") and L2-4 ("the fixture's singleton/merge-commit parameters … are never pinned by any test, so a live queue drifting to multi-pull-request groups, another merge method, or a loosened grouping strategy keeps the gate green") — both rejected with the reason "pinning follows the live readback in bead coding-harness-tsdr" (`plans/changes/archive/2026-11-06-merge-queue/findings.md`, "Phase 4b — loop rows").

**The queue is live since 2026-10-31 07:00 UTC.** `docs/journal/handover/2026-10-31-night-and-day-run.md` ("Decisions and preferences", first bullet): "The merge queue was switched on at 07:00 UTC, before the first merge of the day. The read-back and the undo path are in bead coding-harness-tsdr." `docs/research/2026-10-31-run-plan.md` ("State at the start"): "The merge queue has been the merge path on `main` since 07:00 UTC (bead coding-harness-tsdr)." The night plan of the day before queued the lane: "pin the merge queue's method and group sizes (coding-harness-tsdr, bounded; only after the maintainer merges the merge-queue decision)" (`docs/research/2026-10-30-night-run-plan.md`, lane E row). That plan line is the only committed statement of the bead's scope and class.

**The local check accepts any queue, whatever it carries.** `tests/test_repo_settings.py`:
- The module docstring's paragraph "What RB-G7 adds" defines freshness in two forms — the strict up-to-date flag, or "an active `merge_queue` rule lets GitHub check each group's merge candidate against current `main` without a branch update first (bead coding-harness-eh42)" — and records "the queue joined as the second alternative on 2026-10-30".
- The constant `MERGE_QUEUE = "merge_queue"` and the helper `_merge_queue_rules`, whose docstring says "Any active rule counts, whatever parameters it carries"; it filters on type only.
- `_suppliers` folds queue rules into the fail-closed bypass measurement; `ruleset_findings` accepts either freshness alternative and reports when neither holds.
- The fixture `_queue_rule` models the live rule with parameters `merge_method: "MERGE"`, `grouping_strategy: "ALLGREEN"`, `min_pull_requests: 1`, `max_pull_requests: 1` — and no build-group key at all. Per the predecessor's Boundary these names were "not measured" against the live rule.
- No test asserts any queue parameter; the only assertion on the queue is its presence (`test_merge_queue_supplies_freshness`), the bypass measurement of its ruleset (`test_queue_supplier_is_measured_without_bypass`), and the preserved floor (`test_queue_preserves_the_other_ruleset_requirements`).
- The live assertion `test_master_has_a_ruleset_with_required_checks` runs only in the gate `ruleset` (`decisions/gates.yaml`, entry `id: ruleset`: `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs`, `enforcement: block`, `placement: writer`).

**No committed file records the live queue's parameters after activation.** A tree-wide search for `max_pull_requests_to_build|grouping_strategy|merge_method` finds the fixture, the merge-guard samples and the archived findings diagnostics — nothing measured from the live repository after 2026-10-31 07:00 UTC. The predecessor's plan step 6 ("read back the active branch rules and queue settings … merge method MERGE, minimum/maximum entries to merge 1, maximum entries to build 1") used GitHub's settings vocabulary, and the handover of 2026-10-31 names the read-back as this bead's own task. The predecessor's spec "Definition of Done" also required the orchestrator to record the post-merge ruleset readback; its `findings.md` carries the loop record but no recorded readback values — whether that evidence lives in the bead notes could not be read in this phase.

**The doctrine and template texts the predecessor landed.** `docs/WORKFLOW.md` §3 "Merging a series, one at a time" (queue admission with `gh pr merge <n> --merge --match-head-commit <sha>`, no branch update, "Admission is not a merge", the strict fallback path). `prompts/07-commit.md` "The merge", step 7: which alternative holds "is read, not remembered" — `gh api repos/{owner}/{repo}/rules/branches/main --jq '[.[].type]'` lists `merge_queue` when active; queued is not merged; step 8 keeps `update-branch` only for the no-queue alternative. `docs/governance/regelwerk.md` RB-G7 row (§5): bilingual rule text naming eight enforcers, among them the three ruleset queue tests and both merge-group CI tests; the change history §7 holds 6.0.0 (2026-10-30, the queue accepted, MAJOR, decision pull request) and 7.0.0 (2026-11-18, RB-A1) as the newest entry. `docs/governance/quality-gates.md` MG-2 (gate table row "beim Pull Request and for each merge group" and the explanation paragraph under it). `AGENTS.md` summary line "Pull requests stay mergeable" ("merged through the merge queue at their exact head"). `docs/orchestration.md` "Merges and the morning" (the morning word admits to the queue; each counts as merged only once GitHub shows it merged). `templates/repo-settings.md` "The default branch ruleset": the queue alternative is described as 'merge method "merge commit", build and merge groups of one', switched on only after the workflow is on the default branch, then read back (`gh api repos/<owner>/<repo>/rules/branches/<branch>`). `scripts/ramp_valves.py` (`REGEL_VENTILE`): the valve `merge-freshness` closed on 2026-10-08 with a comment citing "a merge queue or the up-to-date flag; rule set 6.0.0".

**The surrounding machine.** `.github/workflows/ci.yml` triggers on `merge_group` (`types: [checks_requested]`) and admits the event in the `gates` and `verify` job conditions; the generator `scripts/ci_gates.py` emits the same three lines (searched: `merge_group` at the trigger, the matrix condition and `_summary_job`'s condition). `scripts/merge_guard.py` `MERGE_ASK_RULES` covers the queue's enqueue mutation (`Bash(gh api *query=*enqueuePullRequest*)`, "the GraphQL enqueuePullRequest mutation (the merge queue)"). The living spec `plans/specs/implementation-verification/spec.md` names no queue, ruleset or freshness term (searched — not found there). A flaky required test can turn any merge-queue run red, which is the recorded motivation of the neighbouring flaky-swarm-leak-test change (`plans/changes/flaky-swarm-leak-test/decisions.md`, answered question for bead coding-harness-yb1l).

## Where it lives

The deferred limit and its wording: `plans/changes/archive/2026-11-06-merge-queue/spec.md` (Boundary, first bullet; criterion 9; plan step 6) and `.../findings.md` (rows L1-8, L2-4, L1-1 through L5-6 for the doctrine sweep). The check to pin: `tests/test_repo_settings.py` (`MERGE_QUEUE`, `_merge_queue_rules`, `_queue_rule`, `ruleset_findings`, `test_master_has_a_ruleset_with_required_checks`). The gate that turns the live check on: `decisions/gates.yaml` (entry `ruleset`). The live state's record: `docs/journal/handover/2026-10-31-night-and-day-run.md`, `docs/research/2026-10-31-run-plan.md`, `docs/research/2026-10-30-night-run-plan.md` (lane E). Doctrine: `docs/WORKFLOW.md` §3, `prompts/07-commit.md` steps 5–8, `docs/governance/regelwerk.md` RB-G7 + §7 (6.0.0), `docs/governance/quality-gates.md` MG-2, `AGENTS.md`, `docs/orchestration.md`, `templates/repo-settings.md`, `scripts/ramp_valves.py`. CI surface: `.github/workflows/ci.yml`, `scripts/ci_gates.py`. Enforcement beside the check: `scripts/merge_guard.py`, `tests/test_merge_guard.py`. Provenance reservations: `provenance.yaml` (`docs/governance/quality-gates.md` and `docs/governance/regelwerk.md` are `allowed: [human-decided]`).

## What is unclear about it

- **The bead's own words.** Title, description and class of coding-harness-tsdr sit in the Dolt tracker, unreadable in this phase; the committed evidence is the lane line ("pin the merge queue's method and group sizes", bounded) and the two 2026-10-31 statements that the read-back and undo path belong to it.
- **The live field names and values.** What GitHub's branch-rules endpoint actually reports for the queue rule today — whether `max_pull_requests_to_build` appears beside `min_pull_requests`/`max_pull_requests`, what `grouping_strategy` and `merge_method` values are live — is recorded nowhere in the tree; the fixture's parameter names are declared unmeasured, and the read-back is this bead's own owed task. It needs `gh` on the writer machine; this phase cannot measure it.
- **Whether the predecessor's criterion-9 readback was performed** after the 2026-10-31 activation, and where its evidence lives (bead notes, handover, nowhere). The predecessor's `findings.md` holds no recorded readback values.
- **The shape of the pin.** The maintainer's "Erst messen, dann pinnen" (2026-10-30) approves pinning in principle; which parameters the local check pins (merge method only, group sizes, the build group, the grouping strategy) and what it reports when a pinned parameter drifts is decided nowhere in the tree. Whether a drifted live queue is a `not measured:` finding, a drift finding, or a red assertion is unwritten.
- **Decision pull request or not.** If only `tests/test_repo_settings.py` and `templates/repo-settings.md` change, no rule text changes; if the pinning must be stated in RB-G7's row or its enforcer list, `docs/governance/regelwerk.md` is reserved `human-decided` (`provenance.yaml`), and the precedent is the predecessor's 6.0.0 entry (MAJOR, decision pull request, §4's four impact lines). Phase 1 records the surfaces, not the choice.
- **The undo path.** The handover of 2026-10-31 names an undo path as part of this bead; no committed text describes what it undoes (the queue back to the strict flag) or through which API call.

## Which files a change would have to touch

- `tests/test_repo_settings.py` — the pinning itself: the queue predicate `_merge_queue_rules` (accept-anything today), the fixture `_queue_rule` (measured parameters), new planted-fault tests for a drifted parameter (rule RB-G4 asks a mutation test per gate), and possibly the finding texts of `ruleset_findings`. The live test and the gate wiring (`decisions/gates.yaml` entry `ruleset`) exist and need no change unless the findings vocabulary grows.
- `templates/repo-settings.md` — only if its queue bullet's wording ('merge commit, build and merge groups of one') must match what the check now enforces.
- `docs/governance/regelwerk.md` and `docs/governance/quality-gates.md` — only if the rule text, level or enforcer list changes; both are `human-decided` in `provenance.yaml`, and the predecessor's precedent made that a decision pull request with a §7 entry (four impact lines, version bump from the current 7.0.0).
- `docs/WORKFLOW.md` §3, `prompts/07-commit.md`, `AGENTS.md`, `docs/orchestration.md` — the procedure texts name no queue parameters today (searched); they change only if the pin introduces a user-visible behaviour change.
- `scripts/merge_guard.py` / `tests/test_merge_guard.py` — unlikely: the enqueue mutation is already covered; only a new merge-adjacent call shape would touch them.
- `scripts/ramp_valves.py` — only if the closed valve's comment is refreshed or a valve is involved.
- The change folder artefacts and the regenerated `plans/INDEX.md` (`scripts/plans_registry.py --index`), per the standing registry duty.
