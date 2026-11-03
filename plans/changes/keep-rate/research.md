---
title: "Research — keep-rate"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-363r.1
owner: Data Architect
provenance: human-written
tags: [research]
---

# keep rate — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-03: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 837 files, 3109 commits, 12 rules.

## Runner exploration — 2026-11-03

Exploration complete. Below is the research prose for `plans/changes/keep-rate/research.md`, ready for the runner to append (I write no files — read-only phase).

---

## What exists today

**The change itself.** `plans/changes/keep-rate/` holds only the `research.md` skeleton: frontmatter names bead `coding-harness-363r.1`, owner Data Architect, `implementation_status: none`, and no `class:` declaration yet. `plans/INDEX.md` (line 221, entry `changes/keep-rate/research.md`) lists it as draft/none, 2026-11-03. The scope comes from the night-run plan `docs/research/2026-11-02-night-run-plan.md` (lane E, backlog 3): "Keep rate (bead coding-harness-363r.1): explore with GLM Flash up to the interview" — under that plan's rule 2, explores stop at the interview. The bead sits in the epic "Model access, routes and data terms (`coding-harness-363r`)" per `docs/journal/handover/2026-11-02-five-lane-night.md` (cluster epics list) and `docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md` (priority table, rank 5).

**A sibling measurement already exists — for implement/repair, not review.** `docs/research/2026-11-02-route-success.md` (spike, bead `coding-harness-hleu`) measures per-route accepted/rejected rates and hours from the runner time lines in `plans/changes/*/plan.md`, with a method section, per-attempt and per-chain tables, a "Reading" that names selection effects and noise, and a "Reproduce" note saying the script stayed in the session scratchpad, not the repository. Its recommendation also names the measurement-data beads: `coding-harness-zaqf` (runner event log and report) and `coding-harness-v6vk` (time records as data).

**The loop already records everything a keep-rate count needs, row by row.** `scripts/stage2.py` declares `ROW_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Reviewer", "Status", "Broke a test"]` and `RELEASED_COLUMNS = [*ROW_COLUMNS, "Phase 6"]` (stage2.py, constants block near line 352). The reviewer cell is filled by the runner when it merges a swarm's answers (`answer_block`/`answer_parts`, stage2.py near lines 1141–1163); ADR 0021 decision 6 (`docs/adr/0021-review-swarms-until-clean.md`) states the parent "merges rows into unique ids with their actual reviewers and names failures". Status vocabulary is `taken`/`rejected`/`fixed`/`open`; ADR 0021 decision 1 makes "no rows or all rejected rows" a clean round, and the clean check is implemented around stage2.py's loop-record functions (the "round whose rows were all rejected" comment near line 3250).

**A generated counter exists, but it counts per change, not per reviewer.** `scripts/stage2_runs.py` (whole file) reads each change's `findings.md` and `research.md` "with the runner's own row and line constants" (`measure()`, near line 110) and prints per change: loop rows taken / rejected / undecided (a `fixed` row counts as taken, per the comment citing spec criterion 27), rows whose repair broke a test, phase-6 rounds, phase-2a and phase-6 rows by severity, disagree marks, and stage-2 calls clean/total. It computes no rate, splits by no `Reviewer`, and its docstring states what it cannot count: leak-check refusals write no line, and "tokens and cost per vendor are not recorded by the runner". Its tests live in `tests/test_stage2_runs.py`.

**The doctrine that made those columns.** `docs/WORKFLOW.md` §4, "Two columns for every stage-2 change" and "Measuring the first three stage-2 runs" (near lines 1645–1690): every finding records its reviewer, taken/rejected, and broke-a-test; after the third run an evaluation is written under `docs/research/`; "the count is generated, not typed" via `stage2_runs.py`. The first such evaluation is `docs/research/2026-10-08-stage2-three-runs.md`, whose table shows taken/rejected per run and whose reading notes "the loop's rows were smaller and mostly true (16 of 18 taken)" while "Codex's phase 6 found what the loop did not" — the closest existing thing to a keep-rate observation.

**The recorded anomaly that motivates measuring the free stage.** `docs/journal/handover/2026-10-22-night-run-claude.md` (findings list, near line 114): "a review loop whose single free-swarm row is rejected ends clean before any paid round (ADR 0021, decision 1). PR #216's loop ended that way after one false row; phase 6 then found four MAJOR rows." The loop's economics around this are fixed in ADR 0021: decision 8's call bound ("at most one review call per discovered free member and one per eligible paid model … F + 9 member calls"), decision 2–3's free-class admission and diff-only confinement, and the Q-16 availability amendment, which says a successful probe "does not prove review quality". What no file today measures is how many findings each stage's calls actually yield that survive decision (kept) versus rejected.

**A neighbour change alters the denominators.** `plans/changes/free-member-rate-limit/spec.md` (bead `coding-harness-pj98`, class bounded, `implementation_status: partial`): when every free member fails with a rate-limit/unavailability error the free stage is skipped and the run moves to the Flash swarm. A skipped stage contributes no rows, so any per-stage keep rate must distinguish "no rows because clean" from "no rows because skipped" (the spec's criteria 1–4 define exactly which failures skip).

## Where it lives

- Runner constants and row writing: `scripts/stage2.py` — `ROW_COLUMNS`/`RELEASED_COLUMNS` (constants block), `answer_block`/`answer_parts` (reviewer cells), `split_row`, `marks_a_test`, `LOOP_ID`, `kept_lines` and the `Kept from the loop record:` block (loop-record snapshot/release), clean-round logic near the "rows were all rejected" comment, verdict lines (`VERDICT_LINE`).
- Counter: `scripts/stage2_runs.py` (`measure()`, `locate()` — active folder `plans/changes/<name>/` or archive `plans/changes/archive/YYYY-MM-DD-<name>/`, `report()`), tests `tests/test_stage2_runs.py`.
- Doctrine: `docs/WORKFLOW.md` §4 ("Two columns…", "Measuring the first three stage-2 runs").
- Decisions: `docs/adr/0021-review-swarms-until-clean.md` (decisions 1, 6, 8, Q-16 amendment, restart amendment); the change behind it `plans/changes/loop-until-clean/` (spec, design, plan, decisions, findings, research all present).
- Change data a measurement would read: `plans/changes/<name>/findings.md` loop tables with the released columns (Reviewer, Status, Broke a test, Phase 6); runner time lines in `plans/changes/<name>/plan.md` (format documented in `docs/research/2026-11-02-route-success.md`, "Data and method").
- Prior art: `docs/research/2026-11-02-route-success.md`, `docs/research/2026-10-08-stage2-three-runs.md`, `docs/research/2026-11-02-night-run-plan.md` (this change's assignment).

## What is unclear

- **The bead's own wording is not readable here.** `coding-harness-363r.1`'s title and description live in the Dolt tracker (`.beads/` holds only hooks/config in the worktree; the data travels via `refs/dolt/data`, and no rendered copy is committed — house rule 2). The explorer's read-only tools cannot query the database, so the exact intended definition of "keep rate" is unread, not absent; the interview must confirm it.
- **Two grounded candidate meanings exist in the tree.** (a) A per-reviewer/per-stage keep rate of loop findings (taken ÷ decided rows, split by the `Reviewer` cell across free swarm, Flash swarm and ladder rungs) — the `hleu` route-success analogue for review calls, sitting naturally in the "Model access, routes and data terms" epic. (b) Something else in that epic (for example catalog-refresh or probe success rates, which the Q-16 amendment separates from review quality). Both are written here as candidates; nothing in the repository decides between them.
- **Per-round attribution from `findings.md` alone is unverified.** The released loop table carries a `Reviewer` per row but no round column in `RELEASED_COLUMNS`; whether the round/stage a row came from survives release into `findings.md`, or lives only in the external loop record (the snapshot/`kept_lines` machinery in stage2.py), I have not read closely enough to state — open question.
- **Counting rules to settle at the interview:** whether `fixed` rows count as kept (today's counter says yes, citing spec criterion 27), how explicitly rejected duplicates count (ADR 0021 decision 6 keeps them visible), and whether undecided rows belong in the denominator.
- **Sample-size honesty:** the route-success reading warns its own rates rest on small samples and selection effects; any keep-rate report inherits that constraint, plus the skipped-stage case from `free-member-rate-limit` and the unmeasured cost side (no tokens/cost recorded by the runner).
- **Class declaration missing:** the skeleton's frontmatter carries no `class:`; the night plan routes the bead through a Flash explore. Where the class is declared (`--class`, `research.md`/`spec.md` headers) and what it is, is the runner's/maintainer's step, not settled here.

## Which files a change would have to touch

If keep rate becomes a generated measurement: `scripts/stage2_runs.py` (per-reviewer and/or per-stage columns, or a rate row) and `tests/test_stage2_runs.py`; possibly `docs/WORKFLOW.md` §4 if the doctrine text names the new numbers. If it is a one-off study like its sibling: only a dated note under `docs/research/` plus an update of `docs/research/_INDEX.md`, reading `plans/changes/**/findings.md` (including the archive layout `stage2_runs.locate` knows). Runner write paths (`scripts/stage2.py`) are unlikely to be in scope for a measurement-only change; nothing in this exploration says they must change.

## Proposed `neighbours:` for the header

`plans/changes/loop-until-clean/spec.md` (ADR 0021's change — the loop a keep rate would measure) · `plans/changes/free-member-rate-limit/spec.md` (skipped free stage changes the denominators) · `plans/changes/kimi-admission/spec.md` (model admission/terms, same epic) · `plans/changes/research-swarm/spec.md` (the loop run measured in the 2026-10-08 evaluation) · `plans/changes/review-loop-deep-a/spec.md` and `plans/changes/review-loop-deep-b/spec.md` (review-loop internals). Living spec `plans/specs/implementation-verification/spec.md` was checked by title only and looks unrelated; no spec for the `hleu` route-success spike exists (it is a research note, not a change folder — stated as two facts: no folder, not checked further).
