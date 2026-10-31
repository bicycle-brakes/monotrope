---
title: "Research — architecture-reconcile"
category: research
status: draft
implementation_status: none
date: 2026-10-31
created: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-190
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "stage-2 explore, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
---

# architecture reconcile — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 801 files, 2896 commits, 12 rules.

## Runner exploration — 2026-10-31

Exploration complete. Below is the research, ready to append to `plans/changes/architecture-reconcile/research.md`.

---

## What exists today

**The subject.** Bead `coding-harness-190` is described, in the only place its description is visible to me — the quote in `docs/journal/handover/2026-10-21-merge-day.md` ("Earlier today: … reconcile target state and gap analysis through ADR 0021 (coding-harness-190)") — as reconciling the target state and the gap analysis. The tracker itself was not read (this explorer runs no commands), so the bead's full title, class label and current status are unknown to me.

**The four architecture documents** under `docs/architecture/`:

1. `docs/architecture/target-architecture.md` — frontmatter `status: superseded`, `superseded_by: 2026-09-17-omnigent-first-target.md`, `updated: 2026-10-20`. A historical proposal measured at commit `5a950c2`. Its §5.1 layer table still carries "Today" cells describing September: H1 "Copied from portfolio; German; no task classes", H3 "no design prompt … no spec template in either repository", H4 "coding-harness has no `ci.yml`; 60 red tests", H9 "no onboarding page, no licence". Its D-17 rows and the §12 "Template switch" row name Apache-2.0 and `docs/onboarding.md`.
2. `docs/architecture/2026-09-17-omnigent-first-target.md` — frontmatter `status: proposed`, `updated: 2026-10-07`; the current target. It carries three dated "Changed" banners (ADR 0006 of 2026-09-27, ADR 0007 of 2026-09-30, ADR 0009 of 2026-10-05) that mark where later decisions overrule the text. The machine-checked `## Decision continuity` table maps D-1–D-17 and O-1–O-4 as Retain or Amend. Body sections beyond the banners still describe the earlier design: "Run limits … M0 permits at most two coding workers", "pause M0", the coordinator-only sequence diagram, the D-16 row "Retain … Instance `model-routing.yaml` resolves phase requirements", and the D-17 row naming Apache-2.0.
3. `docs/architecture/2026-09-17-gap-analysis.md` — frontmatter `status: proposed`, `updated: 2026-09-29`. Its snapshot section states the measurement: repository commit `eddfc0b`, 2026-09-17, "64 failed, 182 passed, 4 skipped". About 24 gap rows (P0/P1/P2) cite beads `coding-harness-bo0`, `-2ee`, `-9qo`, `-jc3`, `-m34`, `-eev`, `-21f`, `-qvl`, `-bt8`, `-lir`. Its first P0 row claims "No `Makefile`, platform-neutral gate file or `.github/workflows/ci.yml` exists; 27 CI tests fail" — contradicted by today's tree (see below). The 2026-09-29 revision states it "restructured presentation only", so the measurements are six weeks old and were never re-taken.
4. `docs/architecture/2026-09-17-implementation-plan.md` — frontmatter `status: proposed`, `updated: 2026-10-07`; two dated banners (ADR 0007, ADR 0009). Its dependency-path diagram still routes "W0/W1 → M0 pilot → M1 → M2 → M3 → M4" although the banner above records that ADR 0006 dropped M0. Its M4 section says "Publication remains a separate D-17 event: Apache-2.0, onboarding and scan are already delivered" — true for the licence on 2026-10-07 (Apache-2.0 landed with the public switch per `docs/research/2026-10-20-public-readiness.md`), but the licence was replaced the same day (see below), and that note lists the onboarding page and the denylist gate under "Still open before the switch".

**The machine pins on these documents.** A reconciliation edit is not free-form:

- `decisions/gates.yaml`, gate `decision-continuity` (job verify, enforcement block, floor true, subsets docs) runs `python3 scripts/check_decision_continuity.py`.
- `scripts/check_decision_continuity.py` requires the target document's `## Decision continuity` section to name every id in `EXPECTED_D`/`EXPECTED_O` (D-1–D-17, O-1–O-4), and its `AMENDMENT_ADRS` map requires the ADR files 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0009 and 0010 to exist and name the ids they speak for (D-3, D-4, D-7, D-13, D-15, D-17, O-3, "coordinator-permission"). A missing target file exits 3 and is red because the gate is floor.
- `tests/test_stage2.py` pins both living documents by the constants `TARGET` and `PLAN_DOC`: `test_d13_is_amended_by_adr_0007` asserts the D-13 row reads `| D-13 — cross-vendor entry | Amend |` containing "ADR 0007", that `check_decision_continuity.run(TARGET)` is empty, several needle sentences in ADR 0007, and that **both** TARGET and PLAN_DOC carry the flat strings "Changed, 2026-09-30" and "ADR 0007". Rewording those banners means changing this test in the same pull request.
- The gap analysis and the superseded `target-architecture.md` are pinned by no test: a search of `tests/` for `2026-09-17|gap.analysis|target.architecture` finds only the two constants above.
- Two general gates touch any edit here: `docs-links` (`scripts/check_docs.py` — frontmatter, links, anchors resolve) and `frontmatter-current` (`scripts/check_frontmatter_current.py` — `updated:` may not be older than the file's last git change; the stage-2 runner stamps edited headers itself, `scripts/stage2.py` around the `check_frontmatter_current.stamp` calls).

**The repository state the stale claims meet** (all read in this worktree, 2026-10-31):

- The one gate list exists: `decisions/gates.yaml` with the gate ids pytest, ruff-check, ruff-format, leerprobe, plans-registry, docs-links, frontmatter-current, bead-export, dangling-beads, decision-continuity, adr-answers, interview-minimums, question-context, criterion-ledger, research-handoff, gate-schema, ci-drift, ramp-valves, ruleset, markdownlint, lychee, plans-registry-strict, research-currency. `Makefile`'s `verify` delegates to `scripts/verify_all.sh`, and the `ci-drift` gate pins `.github/workflows/ci.yml` to that list. This resolves the gap analysis's first P0 row and the historical target's H4 "Today" cell.
- Templates and prompts the September documents call missing now exist: `templates/spec.md`, `templates/design.md`, `templates/findings.md`, `templates/adr.md`, `templates/arc42.md`, `templates/handover.md`, `templates/gate-record.yaml`; prompts `02a-spec-review.md`, `02b-design.md`, `04b-review-loop.md`.
- The repository went public on 2026-10-20 (`docs/research/2026-10-20-public-readiness.md`, bead `coding-harness-lir`). `LICENSE` is PolyForm Noncommercial 1.0.0; `COMMERCIAL.md` ("Why this license") states this "replaces the Apache-2.0 choice in the public-readiness decision D-17 … for future releases; the rest of that decision stands". No file under `docs/adr/` (0001–0023 exist) records the licence replacement — it lives in `COMMERCIAL.md` prose and `README.md` ("Releases published before 2026-10-20 were under Apache 2.0").
- Not in the tree, as distinct findings from separate searches: no `docs/onboarding.md` anywhere (glob `**/onboarding*` finds nothing); no denylist/public-scan gate in `decisions/gates.yaml` (a search for scan/denylist/public/licence in that file returns nothing); no `model-routing.yaml` (the name appears only in doctrine and plan documents); no `docs/planning/` directory.
- Stage 2 and the swarms are operational: `docs/adr/0020-phase-1-research-swarm.md` and `docs/adr/0021-review-swarms-until-clean.md` (with the Q-16 availability preflight amendment and the 2026-10-21 restart amendment) are accepted; night runs are routine per the handover series `docs/journal/handover/2026-10-12-night-run-first-rehearsal.md` through `2026-10-31-night-and-day-run.md`, and the merge queue has been the merge path since 2026-10-31 07:00 UTC (latest handover, "Where we are").
- `docs/WORKFLOW.md` §"Worktrees" cites the gap analysis as evidence in living doctrine: "worktrees share git's refs, hooks and configuration (`docs/architecture/2026-09-17-gap-analysis.md`)" — any rewrite of that document touches a citation the doctrine relies on.
- Naming: `README.md` and `COMMERCIAL.md` call the product "Monotrope"; `AGENTS.md` and all four architecture documents say "coding-harness" throughout. I record the divergence, not a resolution.

## Where it lives

- The subject documents: `docs/architecture/target-architecture.md`, `docs/architecture/2026-09-17-omnigent-first-target.md`, `docs/architecture/2026-09-17-gap-analysis.md`, `docs/architecture/2026-09-17-implementation-plan.md`.
- The pins: `scripts/check_decision_continuity.py` (`AMENDMENT_ADRS`), `decisions/gates.yaml` (`decision-continuity`), `tests/test_stage2.py` (`TARGET`, `PLAN_DOC`, `test_d13_is_amended_by_adr_0007`).
- The later decisions the documents lag behind: `docs/adr/0001` through `docs/adr/0023`, especially 0006 (no M0), 0007 (stage-2 terms), 0009 (architecture delta), 0010 (M3), 0020, 0021; the public switch in `docs/research/2026-10-20-public-readiness.md`, `LICENSE`, `COMMERCIAL.md`, `README.md`.
- The change's own folder: `plans/changes/architecture-reconcile/` — only the research skeleton exists; no spec, decisions, design or plan yet.

## What is unclear

1. **The class is undeclared.** The research skeleton carries no `class:` field and no `spec.md` exists; the stage-2 report line reads "route flash" (the bounded/spike route per ADR 0020). The runner refuses disagreeing class declarations, so the class must be settled before the spec.
2. **Tracker state not read.** Whether the cited gap beads (`bo0`, `2ee`, `9qo`, `jc3`, `m34`, `eev`, `21f`, `qvl`, `bt8`, `lir`) and `coding-harness-190` itself are open or closed is unknown to me; I read no tracker.
3. **The bead description is second-hand.** "Through ADR 0021" is known only from the 2026-10-21 merge-day handover quote. Whether it binds this change to the review-loop process, and with which stages for a documentation diff, is an interview question.
4. **Depth of the reconciliation is undecided:** re-measure the gap analysis at a current commit, or mark the September documents superseded by a new dated document — the supersede pattern exists in `target-architecture.md`'s frontmatter (`status: superseded`, `superseded_by:`). This is a decision, not explored here.
5. **Three continuity-table rows contradict later state without an amendment entry:** D-16 ("Retain … `model-routing.yaml`") against a tree with no such file, where routing lives in the doctrine table pinned by `STAGE2_ROUTING` in `tests/test_stage2.py` plus `model-endpoints.yaml`; D-17 (Apache-2.0) against `LICENSE`/`COMMERCIAL.md`; the M0 rows against ADR 0006. Whether each is answered by a banner (the established pattern), by extending `AMENDMENT_ADRS` (which touches the script and its test), or by a new ADR is undecided.
6. **The test-pinned banner strings** ("Changed, 2026-09-30", the D-13 row wording) bound how far the two living documents may be reworded without a test change in the same pull request.
7. **"Not read" versus "not there":** I did not read `docs/governance/quality-gates.md`, `docs/governance/gate-catalog.md` or the kit manifest in full; their consistency with the reconciled documents is an open question, and the gate catalog is the subject of the neighbouring change `workflow-promises`.

## Which files a change would have to touch

- `docs/architecture/2026-09-17-gap-analysis.md` — the main subject.
- `docs/architecture/2026-09-17-omnigent-first-target.md` — keeping the `## Decision continuity` heading, all D-/O-ids, the D-13 row wording and the dated banners intact or deliberately re-pinned.
- `docs/architecture/2026-09-17-implementation-plan.md` — same banner pin; its M0/M4 statements.
- `docs/architecture/target-architecture.md` — only for status/header maintenance of the historical record.
- Possibly `scripts/check_decision_continuity.py` and `tests/test_stage2.py` (the D-13 test) if the amendment mapping or pinned wording changes; possibly new `docs/adr/00XX-*.md` files if the maintainer decides amendments need ADRs.
- The change's own artefacts under `plans/changes/architecture-reconcile/`; the plans index row follows from the tooling.

## Neighbours

Read: `plans/changes/workflow-promises/spec.md` (bead `coding-harness-i0l`, class bounded — the workflow-reconciliation sibling; its research names the gap analysis "the methodological precedent, not a spec") and `plans/changes/research-currency/spec.md` (bead `coding-harness-pu9` — the 90-day staleness list for `docs/research/`). Known by path, not read: `plans/changes/adr-owning-change/spec.md` (ADR 0014, a change claims its ADR files), `plans/changes/loop-until-clean/spec.md` (the change folder whose `decisions.md` carries ADR 0021's Q-1–Q-16), and the living spec `plans/specs/implementation-verification/spec.md`. Suggested header value: `neighbours: [plans/changes/workflow-promises/spec.md, plans/changes/research-currency/spec.md, plans/changes/adr-owning-change/spec.md, plans/changes/loop-until-clean/spec.md, plans/specs/implementation-verification/spec.md]`.
