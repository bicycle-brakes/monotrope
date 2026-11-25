---
title: "Research — repair-scope-guard"
status: draft
implementation_status: none
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# repair scope guard — Research

Stage-2 call, 2026-11-02: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 823 files, 3020 commits, 12 rules.

## Runner exploration — 2026-11-02

The exploration is complete. Here is the research, ready to append to `plans/changes/repair-scope-guard/research.md` (this session is read-only and writes nothing; the runner owns the file). Suggested header line first, then the body.

---

**Header addition** (the `neighbours:` requirement; empty today, extended per topic-5/finder rules):

```yaml
neighbours:
  - plans/changes/repair-restore-status/spec.md
  - plans/changes/repair-fixed-lines/spec.md
  - plans/changes/repair-fixed-line-format/spec.md
  - plans/changes/stage2-repair/spec.md
  - plans/changes/codex-repairs/spec.md
  - plans/changes/guard-test/spec.md
  - plans/changes/plan-held-paths/spec.md
  - plans/changes/verify-machine-lock/spec.md
  - plans/changes/dirty-index/spec.md
  - plans/changes/tolerate-derived-leftovers/spec.md
  - plans/changes/restore-symlink-parent/spec.md
  - plans/specs/implementation-verification/spec.md
```

---

# Research — repair-scope-guard

*Model-written by the phase-1 explorer (GLM 5.3 Flash, repository seat), 2026-11-02, worktree `repair-scope-guard`, branch `fix/repair-scope-guard` at the opening commit `6c308058`. Provenance class for the filled file: `ai-drafted-reviewed` (the skeleton's own note).*

## What exists today

**The term "repair scope guard" names nothing yet.** A case-insensitive search for `scope[-_ ]?guard|repair[-_ ]?scope` across `plans/` matches only this change's own `research.md`; the word "scope" appears in `docs/WORKFLOW.md` exactly once, in the `decide(<scope>)` pull-request-title rule (`docs/WORKFLOW.md`, the decision-pull-request section). The topic is new, not a continuation of a named mechanism.

**What a repair may write, as the runner enforces it today, rests on three mechanisms, not on a scope declaration.**

1. **Pre-call cleanliness refusal.** `repair()` sets `allowed = {ctx.findings.relative_to(root)}` and calls `refuse_preexisting` (`scripts/stage2.py`, `repair` near `refuse_preexisting` in the same file, `repair` function at `scripts/stage2.py:7699`, guard `refuse_preexisting` at `scripts/stage2.py:4153`). The refusal message names findings.md only: "the worktree has pre-existing changes outside this change's findings.md". This makes everything that later differs from the baseline the attempt's own work — it is not a scope rule for the attempt, only a blame rule.
2. **Commit-time held-prefix guard.** The only path-class guard at commit time is `uncommittable` (`scripts/stage2.py:5496`): a stage-2 attempt must not commit paths under a `provenance.yaml` prefix whose `allowed` classes are exactly `human-decided` (read from the committed map by `_held_prefixes`, `scripts/stage2.py:5479`) or under the hard-coded `RUNNER_HELD` list (`scripts/stage2.py:5456` — `provenance.yaml`, `decisions/gates.yaml`, `model-endpoints.yaml`, `.claude/`, `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`, `templates/`, `.github/`, `.beads/`, `AGENTS.md`, `README.md`). The docstring states the deliberate exception: "the change's own folder is not" held (`scripts/stage2.py`, `uncommittable` docstring). `checkpoint` refuses and rolls the attempt back when a held path changed (`scripts/stage2.py`, `checkpoint` at `scripts/stage2.py:5516`, refusal branch naming bead coding-harness-rcyf). Everything else — any non-held file, including files of *other* changes under `plans/changes/` and unrelated code or docs — is committed by the passing attempt's `git add -A` (`scripts/stage2.py`, `checkpoint`).
3. **Baseline restore on failure.** On a failed attempt the runner restores every path except `keep` — for implement, draft and repair alike `keep` is findings.md alone (`run_attempts` at `scripts/stage2.py:6815`, `restore_baseline` at `scripts/stage2.py:4318`, `plan_baseline_restore` at `scripts/stage2.py:4242`; the checkpoint passes `keep=allowed` at `scripts/stage2.py:7212`). The `allowed` set never grows inside `run_attempts` — no `.add`/`.update` on it exists in the file. So a repair that *passes* every check keeps everything non-held it wrote; a repair that *fails* loses everything but findings.md. There is no middle state where partial scope is judged.

**What a repair's success check inspects.** `check_repair_answer` (`scripts/stage2.py:6045`) validates the answer's fixed lines against the taken rows, holds findings.md row-for-row as it stood before the attempt (released and phase-6 tables, count-compared), requires the attempt's audit line to survive, and — only after those pass — proves each claimed test red-first on the baseline (`red_first`/`red_first_python` after `scripts/stage2.py:6045`; the "Red first" paragraph in `docs/WORKFLOW.md`, "Repairing taken findings" section). It never reads the attempt's changed-path set: no function in `scripts/stage2.py` compares the repair's diff against the taken findings' files, tests or plan. **"Not there" is a verified statement, not "not found":** the diff-measuring machinery exists (`changed_paths` at `scripts/stage2.py:4005`, `worktree_tree` at `scripts/stage2.py:4575`) and is used by the guards above, but nothing connects it to the findings' content.

**Where the taken rows come from.** `repair_targets` (`scripts/stage2.py:2811`) collects taken rows from three places: the loop record (outside the worktree, `docs/WORKFLOW.md`, "The loop record" paragraph), every released block in `findings.md`, and every phase-6 table; the verb refuses while any row stands undecided or an id is doubled. The repair prompt sends the accepted spec and plan plus the taken rows and the must-run ledger references (`repair_prompt` at `scripts/stage2.py:7668`); the implement contract applies ("the plan is the contract", `prompts/04-implement.md`, "The plan is the contract" section, reused by repair via `work_prompt(... "04-implement.md" ...)` at `scripts/stage2.py:7696`).

**Sandbox reality.** Codex repair attempts run command tools in the CLI's configured `workspace-write` sandbox; the whole worktree is writable there. The prompt forbids committing and repository-changing git commands, and a Codex call that moved HEAD stops the run unrewritten (`docs/WORKFLOW.md`, "Reads: what each call can reach" paragraph and the repair section's sandbox note; `scripts/stage2.py`, HEAD check in `run_attempts` and the `run_codex(... writable=True ...)` call). The workflow states plainly: "The sandbox is the CLI's configured `workspace-write`; the tests show the configured call, not the CLI's confinement" (`docs/WORKFLOW.md`, end of "Repairing taken findings"). Reads are not confined for Codex calls — only the prompt's request bounds them (`docs/WORKFLOW.md`, same isolation paragraph).

**Hand repairs are the unguarded path.** When the orchestrator repairs a row itself, three follow-ups are owed — the loop record learns the repair, the plans registry index is regenerated, stamps follow the local date — and a targeted check (touched test files, `scripts/touch_map.py` links, ruff on touched files, the gates those file kinds feed) replaces the full verify (`docs/WORKFLOW.md`, "Hand repairs by the orchestrator"). No mechanical guard constrains which files a hand repair may touch.

**The plan card already carries a scope vocabulary, and it names held paths.** A card widens scope when its `For you:`/`Done when:` lines exceed the spec's non-goals or the appetite (`prompts/03-plan.md`, "A card widens the scope…"); plans must name "Every file by name that is created, changed or deleted" and "What you do not touch" (`prompts/03-plan.md`, "Required" list); and "Held paths go to the orchestrator" repeats the held-prefix rule into the plan prompt (`prompts/03-plan.md`, held-paths bullet — the deliverable of the `plan-held-paths` change, whose spec records the remedy as "planning guidance and a list-drift test, not a weaker guard", `plans/changes/plan-held-paths/spec.md`, Problem section). The plan is the only place a repair's intended file set is written down today, and the runner does not read it back as a constraint.

**Prior scoping decisions that border this topic.** The `repair-restore-status` spec (bounded, partial, 2026-10-25) explicitly declined, as non-goals, "Refuse a row up front because its fix may lie in a human-written path" and "Change the commit guard or what it keeps" (`plans/changes/repair-restore-status/spec.md`, Non-goals). ADR 0023 covers proof for *test-only* repairs via planted faults (`docs/adr/0023-guard-proof-for-test-only-repairs.md`) — evidence strength, not write scope. The "second finding of one mechanism ends case-by-case repair" rule and the `Boundary`-section precedent (machine lock, bead coding-harness-p6mu) live in `docs/WORKFLOW.md`, "When the same mechanism returns".

## Where it lives

- Runner: `scripts/stage2.py` — `repair_targets` (:2811), `refuse_preexisting` (:4153), `changed_paths` (:4005), `restore_baseline` (:4318), `plan_baseline_restore` (:4242), `RUNNER_HELD` (:5456), `_held_prefixes` (:5479), `uncommittable` (:5496), `checkpoint` (:5516), `check_repair_answer` (:6045), `mark_repaired_findings` (:6201), `mark_repaired_record` (:6230), `run_attempts` (`allowed` set at :6815, checkpoint call at :7212), `implement` (:7285), `draft` (:7533), `repair_prompt` (:7668), `repair` (:7699), verb dispatch near the file end.
- Doctrine: `docs/WORKFLOW.md` — isolation paragraph ("Reads: what each call can reach"), "Repairing taken findings (repair)", "When the same mechanism returns", "Hand repairs by the orchestrator", repair row of the stage table; `AGENTS.md` phase table and house rules 6–7 (customer-instance boundary, texts carry their own meaning).
- Prompts: `prompts/03-plan.md` (card, held paths, "what you do not touch"), `prompts/04-implement.md` (contract reused by repair).
- Guard map source: `provenance.yaml` (`paths:` entries with `allowed: [human-decided]` are the decided prefixes the commit guard derives; `docs/governance/*` two files, `decisions/answers/`, `decisions/adoption.yaml`, `decisions/gates.yaml`, `docs/adr/`, `.claude/rules/`).
- Tests: `tests/test_stage2.py` — held-path refusal and restore (:761), the plan prompt naming every held path (:801), rename-into-allowed refusal (:830), unreadable provenance fails and restores (:955), passing repair ends in one checkpoint commit (:12581), restore refuses unsafe parents (:9890), checkpoint failures (:5445, :15864).
- Neighbour artefacts (status per `plans/INDEX.md`): all listed in the header above are `draft` change specs except the living `plans/specs/implementation-verification/spec.md` (`status: accepted`). Of these I read: `repair-restore-status`, `guard-test`, `plan-held-paths`, `stage2-repair`, `implementation-verification`. I did **not** open: `repair-fixed-lines`, `repair-fixed-line-format`, `codex-repairs`, `verify-machine-lock`, `dirty-index`, `tolerate-derived-leftovers`, `restore-symlink-parent` — their topics are known only from titles, `plans/INDEX.md` rows and references inside `scripts/stage2.py` (beads `ugi`, `0c8`, `b5w`, `10w`, `rcyf`), not from reading them.

## What is unclear

1. **The maintainer's intended meaning of "repair scope"** — the bead (`coding-harness-t83`) description sits in the tracker (Dolt database under `.beads/`), which this read-only explorer cannot query; the opening commit (`6c308058`, from the git status) carries only the title. Candidate readings, none decided here: (a) which files a repair attempt may touch; (b) which rows/records a repair takes; (c) which routes and attempts a repair may consume; (d) how far a repair may reach into the loop (the repair brake, `docs/WORKFLOW.md`, repair-brake rule). This is the interview's first question.
2. **Relation to the 2026-10-25 non-goals.** A scope guard that refuses a repair up front, or changes what the commit guard keeps, revisits a boundary a previous bounded change drew (`plans/changes/repair-restore-status/spec.md`, Non-goals). Whether that boundary still stands is a decision question.
3. **Whether hand repairs are in scope.** The orchestrator's own repairs have no mechanical guard at all (three follow-ups and a targeted check only, `docs/WORKFLOW.md`, "Hand repairs by the orchestrator"). Not read, not guessed: whether the maintainer wants the guard to cover them.
4. **Whether the change folder's exemption stands.** `uncommittable` deliberately spares `plans/changes/<change>/` and everything non-held (`scripts/stage2.py`, `uncommittable` docstring); `plan-held-paths` chose planning guidance over a stronger guard. A guard inside that space would reverse a recorded stance — decision question.
5. **Untracked and new files.** `changed_paths` includes untracked files (`scripts/stage2.py`, `changed_paths`); nothing today distinguishes a repair's intended new test from any other new non-held file. Whether that is part of "scope" is open.
6. **Neighbour specs not read** (listed above) may hold decisions about the loop record, restore safety and derived leftovers that a scope guard must respect; they are marked not read, not assumed.

## Which files a change would have to touch

- `scripts/stage2.py` — the guard sites themselves: `uncommittable`/`RUNNER_HELD`/`_held_prefixes`, `checkpoint`, `refuse_preexisting`, `run_attempts` (`allowed`), `repair`, `repair_prompt`, `repair_targets`, `check_repair_answer`, depending on the chosen reading.
- `docs/WORKFLOW.md` — the repair section, the isolation paragraph and "Hand repairs by the orchestrator" (every behaviour change in the runner has its doctrine sentence there).
- `prompts/03-plan.md` and/or `prompts/04-implement.md` — if the guard's expectation is told to the attempt or planned.
- `tests/test_stage2.py` — the guard tests around the existing held-path, restore and checkpoint tests.
- `provenance.yaml` — only if the human-decided map itself changes; that file is `human-decided` (`provenance.yaml`, its own header) and would travel as a decision pull request.
- Not touched by any reading found: `scripts/plans_registry.py` (only regenerated after frontmatter edits, `docs/WORKFLOW.md`, hand-repair follow-ups) and the review-swarm scripts (`scripts/stage2_research_run.py`), which see no repair path.

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1149 files, 5117 commits, 12 rules.

## Runner exploration — 2026-11-21

The exploration is complete. The change artefact `plans/changes/repair-scope-guard/research.md` already carries the 2026-11-02 exploration; since then the tree absorbed ~1500 commits, so this section re-verifies every claim against the current worktree and corrects the drift. Ready to append to `plans/changes/repair-scope-guard/research.md` (this session is read-only and writes nothing; the runner owns the file).

---

**Corrected `neighbours:` header list** (the 2026-11-02 header names twelve `plans/changes/<name>/spec.md` paths that no longer exist at those locations; the archive migration of 2026-11-06/16 moved them — verified by glob today):

```yaml
neighbours:
  - plans/changes/adr-repair-check/spec.md
  - plans/changes/adr-0021-consumed-ladder/spec.md
  - plans/changes/archive/2026-11-06-repair-restore-status/spec.md
  - plans/changes/archive/2026-11-06-repair-fixed-lines/spec.md
  - plans/changes/archive/2026-11-06-repair-fixed-line-format/spec.md
  - plans/changes/archive/2026-11-06-stage2-repair/spec.md
  - plans/changes/archive/2026-11-06-codex-repairs/spec.md
  - plans/changes/archive/2026-11-16-guard-test/spec.md
  - plans/changes/archive/2026-11-06-plan-held-paths/spec.md
  - plans/changes/archive/2026-11-16-verify-machine-lock/spec.md
  - plans/changes/archive/2026-11-06-dirty-index/spec.md
  - plans/changes/archive/2026-11-06-tolerate-derived-leftovers/spec.md
  - plans/changes/archive/2026-11-06-restore-symlink-parent/spec.md
  - plans/changes/archive/2026-11-16-repair-targeted-check/spec.md
  - plans/specs/implementation-verification/spec.md
```

---

## Runner exploration — 2026-11-21 (re-verification)

*Re-verified by the phase-1 explorer (GLM 5.3 Flash, repository seat), 2026-11-21, worktree `repair-scope-guard`, branch `fix/repair-scope-guard` at the opening state after the merge commit `340357d7` (1502 commits from main). Line numbers are anchors of this hour; every statement names its file and symbol first.*

### What exists today

**The term "repair scope guard" still names nothing in doctrine, prompts or runner code.** A case-insensitive search for `scope[-_ ]guard|repair[-_ ]scope` across the whole tree matches six files today: this change's own `research.md`, the `plans/INDEX.md` row, `docs/research/2026-11-02-route-success.md` ("a scope guard for repairs", its Recommendation), the two handovers `docs/journal/handover/2026-11-02-five-lane-night.md` and `2026-11-02-tracker-cleanup-and-evaluations.md` ("the repair scope guard (-t83) waits at its interview", lane table), and `plans/changes/slip-counter/research.md` (which says "repair-scoped variant" about the slip counter — a different topic). `docs/WORKFLOW.md` contains neither term.

**The recorded origin of the topic is the route-success measurement.** `docs/research/2026-11-02-route-success.md` tables "Why attempts were rejected": "a protected or out-of-scope path was touched — 24 blocks" over ten days, named in its Reading point 4 as one of the route-independent rejection causes; its Recommendation lists "a scope guard for repairs (bead coding-harness-t83)" among four follow-ups to remove those rejections. The maintainer's intended meaning still sits in the bead description in the Dolt tracker, which this read-only seat cannot query — the interview question stands.

**The 2026-11-02 section below remains accurate in structure; five of its facts have moved or grown.** The corrections, each verified in the current tree:

1. **Pre-call cleanliness refusal.** `refuse_preexisting` (`scripts/stage2.py:5284`) now exempts paths that `derived_leftover` classifies (bead coding-harness-b5w, the tolerate-derived-leftovers change) and its refusal message lists the offending paths. It is called by `repair` (`scripts/stage2.py:10745`) with `allowed = {ctx.findings.relative_to(root)}` (`scripts/stage2.py:10744`), as before: a blame rule, not a scope rule.

2. **Commit-time held-prefix guard.** `RUNNER_HELD` (`scripts/stage2.py:7541`) carries the same sixteen prefixes as 2026-11-02; `_held_prefixes` (`scripts/stage2.py:7564`) case-folds both sides and reads the human-decided classes from the committed `provenance.yaml`; `uncommittable` (`scripts/stage2.py:7581`) gained a `keep` parameter that spares declared keep-paths (its docstring: a draft's own new ADR under `docs/adr/` — "P1 of the #192 review"), and still exempts the change's own folder while refusing and rolling back via `checkpoint` (`scripts/stage2.py:7601`). The committed human-decided map, read from `provenance.yaml` today, is unchanged: `docs/governance/quality-gates.md`, `docs/governance/regelwerk.md`, `decisions/answers/`, `decisions/adoption.yaml`, `decisions/gates.yaml`, `docs/adr/`, `.claude/rules/`. A side observation, stated not judged: `provenance.yaml`'s header comment says "`allowed:` is declared, not yet enforced; nothing here reads it" and lists three readers — the runner's `_held_prefixes` is a fourth reader that comment does not name.

3. **Baseline restore on failure.** Unchanged in essence: `plan_baseline_restore` (`scripts/stage2.py:5373`), `restore_baseline` (`scripts/stage2.py:5449`), `run_attempts`'s `allowed` set holds findings.md alone (`scripts/stage2.py:9549`) and no `.add`/`.update` on it exists in the file (grep-verified). One correction to the 2026-11-02 text: the draft no longer keeps findings.md alone — `draft_keep` (`scripts/stage2.py:10301`) returns a keep set including the draft's own new ADRs; implement and repair still keep findings.md alone. The restore-safety test suite has grown (`test_restore_baseline_refuses_external_parents_before_mutation` `tests/test_stage2.py:13896`, `test_restore_work_input_refuses_external_parent_without_writes` `tests/test_stage2.py:13777`, `test_runner_restore_preflights_all_destinations` `tests/test_stage2.py:13957`, deleted-change-directory restore `tests/test_stage2.py:14096`).

4. **New since 2026-11-02: the post-run targeted check (ADR 0025).** `repair` passes `verify_mode="targeted"` (`scripts/stage2.py:10835`) and `implement` targeted plus `new_file_guard=True` (`scripts/stage2.py:10259-10260`); the `run_attempts` parameters carry the beads (`scripts/stage2.py:9500-9501`). The selector `targeted_selection` (`scripts/stage2.py:6942`, `Targeted` dataclass at `scripts/stage2.py:6816`) reads the attempt's whole delta — index, working tree, untracked files, both names of a rename, through `changed_paths` (`scripts/stage2.py:5119`) — and runs whole touched and touch-map-linked test files (two link closures, current and baseline), ruff on touched Python, and the local gates the touched file kinds feed. It falls back to the full `make verify` when a prompt changed, a `SHARED_INFRASTRUCTURE` path (`scripts/stage2.py:4846`) or `conftest.py` was touched, a path is a link or aliased, an input kind is not Python or a plans/docs Markdown, production code has no linked test in either graph, the inventory is unreadable, or `tests/test_stage2.py` whole would run (maintainer option A, 2026-11-04, until bead coding-harness-vg9 splits the file). `new_code_without_test` (`scripts/stage2.py:6831`) refuses an *implement* attempt whose new production file no test reaches; repair does not arm that guard. Doctrine: `docs/WORKFLOW.md` review-loop section (`:1768-1769`), "Post-run verification runs the repair's targeted check" (`:1882-1888`), and the hand-repair bullet "A targeted check, not a full verify, before the next round" (`:2009-2040`); the decision record is ADR 0025 (`docs/adr/0025-targeted-check-after-repair.md`, status accepted, amends ADR 0021 decision 6, runner behaviour via pull request #343, bead coding-harness-gxwg) with the maintainer's answers Q-1 to Q-5 in `plans/changes/adr-repair-check/decisions.md` (2026-11-08) and the 2026-11-12 amendment extending the check to implement and draft (bead coding-harness-0swp). A status discrepancy, stated not resolved: the `adr-repair-check` change folder's header still says `status: draft, implementation_status: none` while the ADR file itself says accepted — the same folder-lags-merge pattern the slip-counter research records for other lanes.

5. **New since 2026-11-02: lifecycle-field protection.** `repair` passes `protect_lifecycle=True` (`scripts/stage2.py:10836`); the runner snapshots and restores `status` and `implementation_status` of the change's `spec.md`, optional `design.md` and `plan.md` around every attempt (`run_attempts` docstring, `scripts/stage2.py:9521`, doctrine `docs/WORKFLOW.md:1890-1909`). A finding whose remedy needs one of those two fields must be hand-repaired. This is a second narrow scope rule inside the change's own folder, beside the exemption: the folder is otherwise the attempt's.

6. **Which rows a repair takes is now heavily guarded** — reading (b) of "scope" is occupied territory. `repair_targets` (`scripts/stage2.py:3617`) resolves one current row per finding ID across the loop record, released blocks and phase-6 tables; `repair` refuses on undecided rows, doubled taken IDs, legacy completed statuses, and invalid `Origin` of any selected row before any call (`scripts/stage2.py:10749-10773`, `target_origin_refusal`/`origin_refusal` calls at `:10754-10759`, doctrine `docs/WORKFLOW.md:1817-1844`); a late check re-verifies the rows before the checkpoint (`require_unchanged_repair_rows`, `scripts/stage2.py:10812`). `check_repair_answer` (`scripts/stage2.py:8412`) still holds findings.md row-for-row and still never compares the attempt's changed-path set to the taken rows' files — re-verified as "not there": the diff-measuring sites (`changed_paths`, `targeted_selection`, `uncommittable`) are connected to *check selection* and *commit refusal*, never to the findings' content.

7. **Sandbox reality, restated in today's doctrine.** The isolation paragraph is retitled "Reads: confined for the Claude Code calls, asked for Codex and for the loop" (`docs/WORKFLOW.md:1453-1482`): Claude Code calls run `--restricted` (documented behaviour, not measured); Codex review, draft and repair calls are not confined in their reads; Pi's reads reach outside the worktree, secrets file included (measured, Pi 1.1.0); the maintainer accepted the unconfined reads as residual risk (2026-09-30, ADR 0007; ADR 0011 for the ladder rungs). Repair writes stay in the CLI's configured `workspace-write` sandbox — "the tests show the configured call, not the CLI's confinement" (`docs/WORKFLOW.md:1934-1935`; test `test_codex_repair_uses_workspace_write_without_bypass` `tests/test_stage2.py:11663`).

8. **Hand repairs remain the unguarded path.** The doctrine grew the targeted check and the lifecycle remedy for them (`docs/WORKFLOW.md:1991-2040`), and still no mechanical guard constrains which files a hand repair may touch.

9. **The consumed-ladder rule is new neighbouring doctrine (2026-11-20).** `docs/WORKFLOW.md:1709-1716`: when every stage of a run is consumed and the last round was not clean, the loop stops and reports — no model substitutes. `plans/changes/adr-0021-consumed-ladder/spec.md` (accepted, bounded, bead coding-harness-hwll) amends ADR 0021 decision 7: a consumed ladder with at least one completed review round names `next: repair <change>` while a taken row is open, `next: review <change>` once every taken row is fixed; zero completed rounds still escalate. The spec's non-goals put the runner behaviour in a change named `ladder-next-step` (same bead); no such folder exists at the top level of `plans/changes/` (glob-verified), and whether the runner already implements the phase-6 route for a consumed ladder is not verified from the docstring alone (`review_loop`, `scripts/stage2.py:10868-10879` names spent stages as a stop) — an open question below.

10. **Plan-side vocabulary unchanged in essence.** `prompts/03-plan.md` still carries the widening-card rule (`:41-47`), "What you do not touch" (`:56`) and "Held paths go to the orchestrator" (`:57-66`, now stating the case-folded prefix matching explicitly — `claude.md` or `README.md.bak` are held too); `prompts/04-implement.md` keeps "The plan is the contract" (`:40`) and the ambiguous-contract rule (`:113-117`). The plan remains the only place a repair's intended file set is written, and the runner still does not read it back as a constraint.

### Where it lives

- Runner: `scripts/stage2.py` — `repair_targets` (`:3617`), `changed_paths` (`:5119`), `refuse_preexisting` (`:5284`), `plan_baseline_restore` (`:5373`), `restore_baseline` (`:5449`), `SHARED_INFRASTRUCTURE` (`:4846`), `Targeted` (`:6816`), `new_code_without_test` (`:6831`), `targeted_selection` (`:6942`), the post-run check body feeding it (`:7330-7398`), `verify_attempt` (`:7401`), `RUNNER_HELD` (`:7541`), `_held_prefixes` (`:7564`), `uncommittable` (`:7581`), `checkpoint` (`:7601`), `red_first_python` (`:7697`), `red_first` (`:8181`), `check_repair_answer` (`:8412`), `mark_repaired_findings` (`:8603`), `mark_repaired_record` (`:8647`), `run_attempts` (`:9483`, parameters `:9500-9502`, `allowed` at `:9549`, checkpoint call `keep=allowed` at `:10107`), `implement` (`:10204`, `draft_keep` at `:10301`), `draft` (`:10526`), `repair_prompt` (`:10699`), `repair` (`:10730`).
- Doctrine: `docs/WORKFLOW.md` — the stage-4b table row (`:89`), the isolation paragraph (`:1453-1482`), the review-loop gate paragraph with the repair brake (`:1765-1774`), "Repairing taken findings (repair)" (`:1809-1956`, Origin checks, targeted check, lifecycle protection, ADR 0023 guard test), "When the same mechanism returns" (`:1958-1989`), "Hand repairs by the orchestrator" (`:1991-2040`), the consumed-ladder stop (`:1709-1716`).
- Decision records: `docs/adr/0015-glm-5-3-repairs-taken-findings.md`, `0017-codex-repairs-taken-findings.md`, `0023-guard-proof-for-test-only-repairs.md`, `0025-targeted-check-after-repair.md` (all repair-relevant; 0025 and its amendment are the new ones).
- Prompts: `prompts/03-plan.md`, `prompts/04-implement.md`.
- Guard map: `provenance.yaml` (human-decided prefixes listed above).
- Tests: `tests/test_stage2.py` — held-path refusal and restore (`test_an_attempt_that_writes_a_runner_held_path_is_refused_and_stored` `:937`), plan prompt names every held path (`:977`), rename-into-allowed refusal (`:1006`), unreadable provenance fails the checkpoint (`:1134`), Origin/refusal family (`:9978-11619`), targeted-verification prompt descriptions (`:10855`, `:10868`, `:10900`), restore-safety family (`:13777-14096`), answer-form family (`:14964-15437`), lifecycle family (`test_repair_lifecycle_*` `:15526-16305`, roughly two dozen tests). Targeted-selection coverage exists in `tests/test_stage2.py` and `tests/test_ci.py` (grep-verified by content); test names beyond the read windows are not read.
- Neighbours: all paths corrected in the header block above; the only living spec is `plans/specs/implementation-verification/spec.md`; `adr-repair-check` and `adr-0021-consumed-ladder` are the active ones adjacent to this topic.

### What is unclear

1. **The maintainer's intended meaning of "repair scope guard"** — unchanged from 2026-11-02 and still first: the bead (`coding-harness-t83`) description sits in the Dolt tracker, unreadable from this seat. The recorded origin (`docs/research/2026-11-02-route-success.md`, Recommendation, and the 2026-11-02 handovers' "waits at its interview") supports reading (a) — which files a repair attempt may touch, so that out-of-scope touches stop failing attempts after the model ran. Candidate readings (b) which rows a repair takes, (c) which routes and attempts a repair may consume, (d) how far a repair may reach into the loop — each has since gained its own machinery (origin checks and the resolver for b; ADR 0017's fixed ladder plus the consumed-ladder doctrine for c; the repair brake for d), which sharpens rather than answers the question.
2. **Whether the route-independent rejections the measurement counted still occur.** The 24 blocks of "a protected or out-of-scope path was touched" were measured 2026-10-28 to 2026-11-02. Since then the targeted check (check-time consequence for uncovered kinds) and lifecycle protection landed, but nothing refuses a non-held, coverable out-of-scope path before the model call — whether the cause still produces rejections is not recorded anywhere in the tree (not found).
3. **Whether hand repairs are in scope.** Still no mechanical guard; the question stands as stated 2026-11-02.
4. **Whether the change-folder exemption stands.** `uncommittable`'s docstring keeps it deliberately; the archived `plan-held-paths` change chose planning guidance over a stronger guard (`plans/changes/archive/2026-11-06-plan-held-paths/spec.md`, per its INDEX row — not re-opened today; the 2026-11-02 section quoted its Problem section). A guard inside that space would revisit a recorded stance.
5. **Whether the runner already routes a consumed ladder to phase 6** — the doctrine (`docs/WORKFLOW.md:1709-1716`) and `AGENTS.md` (2026-11-20) say yes, the change `adr-0021-consumed-ladder/spec.md` says the runner behaviour belongs to `ladder-next-step` (bead coding-harness-hwll), and no `ladder-next-step` change folder exists (not found at the top level of `plans/changes/`). Not read, not guessed: the current `review_loop` body beyond its docstring.
6. **The `adr-repair-check` status discrepancy** (folder draft/none, ADR file accepted) — stated above, resolved by nobody in the tree.
7. **Not read today:** the Dolt tracker; the bodies of the fourteen archived neighbour specs (titles and INDEX rows only); `tests/test_stage2.py` beyond the named tests; `_targeted_commands`, `run_targeted` and `full_verify` bodies (`scripts/stage2.py:7219`, `:7385` callers); `scripts/touch_map.py` internals.

### Which files a change would have to touch

- `scripts/stage2.py` — the guard sites, per the chosen reading: `refuse_preexisting`, `uncommittable`/`RUNNER_HELD`/`_held_prefixes`, `checkpoint`, `run_attempts` (`allowed`, `verify_mode`, `new_file_guard`), `repair`, `repair_prompt`, `repair_targets`, `check_repair_answer`, and `targeted_selection` if scope and check scope are to meet.
- `docs/WORKFLOW.md` — the repair section, the review-loop gate paragraph and "Hand repairs by the orchestrator".
- `prompts/03-plan.md` and/or `prompts/04-implement.md` — if the guard's expectation is told to the attempt or planned.
- `tests/test_stage2.py` — beside the held-path, restore, checkpoint, Origin and lifecycle families.
- `provenance.yaml` — only if the human-decided map itself changes; that is a decision pull request.
- Not touched by any reading found: `scripts/plans_registry.py` (regenerated, not edited), `scripts/touch_map.py` (read by selection), the research-swarm scripts (`scripts/stage2_research_run.py`), and `docs/adr/` unless a decision record changes — that tree is `human-decided` and travels as a decision pull request.
