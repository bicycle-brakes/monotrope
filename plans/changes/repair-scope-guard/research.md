---
title: "Research — repair-scope-guard"
status: draft
implementation_status: none
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: Data Architect
provenance: human-written
tags: [research]
---

# repair scope guard — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

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
