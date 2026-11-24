---
title: "Research — repair-hand-held-rows"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-0zhf
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# repair hand held rows — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1149 files, 5086 commits, 12 rules.

## Runner exploration — 2026-11-21

I have the full picture. The rollback test at `tests/test_stage2.py:15968` (`world.run("repair") == 1`) confirms a held-path rollback ends the whole repair run — no route advances. Here is the research, ready to append to `plans/changes/repair-hand-held-rows/research.md` below its Stage-2 line.

---

## Suggested `neighbours:` for the header

`plans/specs/implementation-verification/spec.md` · `plans/changes/archive/2026-11-06-repair-fixed-lines/spec.md` · `plans/changes/archive/2026-11-16-guard-test/spec.md` · `docs/adr/0017-codex-repairs-taken-findings.md` · `docs/adr/0025-targeted-check-after-repair.md` · `docs/adr/0021-review-swarms-until-clean.md` · `plans/changes/archive/2026-11-06-index-merge-regenerates/spec.md`

## What exists today

**The trigger for this change is recorded in the latest handover.** `docs/journal/handover/2026-11-21-night-run-2026-11-20-a-morning.md`, "Needed from the maintainer" item 6(b), files exactly this wish: "the runner restores a whole repair attempt when a taken row needs a path it does not commit (`AGENTS.md`, `model-endpoints.yaml`, `prompts/`). This happened three times tonight. It should hand such rows to the orchestrator up front." The change folder was opened for bead `coding-harness-0zhf` (commit `d2900e60`, "chore(repair-hand-held-rows): open change folder for coding-harness-0zhf", branch `fix/repair-hand-held-rows`), which matches that filed proposal; that the bead is that proposal is an open question below.

**The held-path classification.** `scripts/stage2.py` defines `RUNNER_HELD` (stage2.py:7541–7561): `provenance.yaml`, `decisions/gates.yaml`, `model-endpoints.yaml`, `.claude/`, `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`, `templates/`, `.github/`, `.beads/`, `AGENTS.md`, `README.md`. `_held_prefixes` (stage2.py:7564) unites that tuple with the `human-decided` prefixes it reads from the committed `provenance.yaml` (`git show HEAD:provenance.yaml`, entries whose `allowed` is exactly `{human-decided}`); in `provenance.yaml` (`paths:`) those are `docs/governance/quality-gates.md`, `docs/governance/regelwerk.md`, `decisions/answers/`, `decisions/adoption.yaml`, `decisions/gates.yaml`, `docs/adr/`, `.claude/rules/`.

**The rollback.** `uncommittable()` (stage2.py:7581) lists the attempt's changed paths (`changed_paths`, stage2.py:5119 — working tree, index and untracked files) that start with a held prefix, sparing the `keep` set and the change's own folder. `checkpoint()` (stage2.py:7601) computes that list after a passing attempt and, when it is non-empty, raises `CheckpointRolledBack` with the reason "the attempt changed paths a stage-2 run does not commit: …" (stage2.py:7640–7652) after `restore_baseline` put the tree back to the baseline. Derived stamps on held documents are exempt via `derived_leftover` (stage2.py:7617–7629) — an `updated:` stamp alone is not a refusal. `CheckpointRolledBack` subclasses `CallFailed` (stage2.py:646), exit 1.

**A rollback consumes the attempt and ends the run.** In the shared attempt loop `run_attempts` (stage2.py:9483), the rollback handler (stage2.py:10108–10134) restores the lifecycle fields and `findings.md`, then re-raises; the finalization boundary logs the attempt as one rejected time entry (stage2.py:10174–10199) and the exception leaves the loop. A retry happens only for post-run check *problems* (stage2.py:10082, 10141), not for exceptions, so no later route (Codex → Codex-repair → Sonnet, stage2.py:10780–10786) is taken. The pinned test `test_repair_lifecycle_checkpoint_rollback_reports_restoration` (tests/test_stage2.py:15943) shows exactly the night's shape: a repair that fixes its row and also tampers `model-endpoints.yaml` passes every check, is rolled back at the checkpoint, exits 1, HEAD stands at the baseline, and no fixed status is written (assertions at tests/test_stage2.py:15968–15979).

**What the repair verb keeps and teaches.** `repair()` (stage2.py:10730) sets `allowed = {ctx.findings.relative_to(root)}` (stage2.py:10744) — only `findings.md` is the verb's own. The prompt (`repair_prompt`, stage2.py:10700; constants `REPAIR_FORMAT` stage2.py:383 and `REPAIR_FORMAT_FILE_TOOLS` stage2.py:389) and `prompts/04-implement.md` never name the held prefixes; searched, "not there". The model meets the restriction only at the checkpoint, after its (possibly correct) work. There is no pre-call check of a taken row's remedy against the held prefixes — searched `scripts/stage2.py` for held-path logic; the only references are the comment at stage2.py:5957, the refusal at 7644, and four test hits (tests/test_stage2.py:6940, 15970, 22916, 26055). The early refusals `repair()` does have today are: waiting rows (stage2.py:10750), target/origin checks (10754–10759), empty batch (10761) and legacy fixed-markers (10763–10773, refusing before any call with the hand-repair booking instruction). The implement-only precedent for an up-front, names-the-file refusal is `new_file_guard` (stage2.py:7342–7347, set at 10260): new production code without a reachable test refuses before any test runs.

**The doctrine the rows would be handed to.** `docs/WORKFLOW.md` §4 already names the hand repair as the standing route for exactly this case: "Hand repairs by the orchestrator" (docs/WORKFLOW.md:1991) — the orchestrator repairs itself "(a held path, a one-line fix, a re-check row)" and owes three follow-ups: the loop record learns the repair (Status cell `fixed — tests/<path>::<function>`, `fixed — guard test — …` or `fixed — not a test — <reason>`, plus the `Broke a test` cell, after a backup of `loop.md`), a header edit regenerates the index (`scripts/plans_registry.py --index`), and after local midnight the stamps follow the local date (`scripts/check_frontmatter_current.py --stamp`); a targeted check, not a full verify, precedes the next round (docs/WORKFLOW.md:2009–2028; ADR 0025, bead coding-harness-24ag). The repair section "### Repairing taken findings" (docs/WORKFLOW.md:1862–1869) states the canonical hand-repair booking, and stage2.py:1897–1899 adds a second hand-repair trigger: a finding whose remedy requires changing the protected lifecycle fields is repaired by hand. AGENTS.md restates the targeted-check rule in the phase table (AGENTS.md:24) and at AGENTS.md:179. `docs/orchestration.md` has no "hand repair"/"held path" mention — searched, not there.

**Existing runner-to-orchestrator hand-off messages** (shapes already in the tree): the legacy-marker refusal of `repair()` ("book the hand repair by replacing the Status with `fixed — tests/<path>::<function>` or `fixed — not a test — <reason>` …", stage2.py:10767–10772) and the loop-record marking failures of `mark_repaired_record`/`_mark_record_rows` ("mark {waiting} by hand.", stage2.py:8676, 8694, 8708).

**The night's evidence.** The handover's "Hand steps of the orchestrator, per lane" names three hand steps on held paths: L3 `AGENTS.md`/`docs/orchestration.md` commit `60ad1df7` (which then caused phase-6 row F6-1 of coding-harness-qut1), L5 `prompts/04-implement.md` commits `94ebd4d8` and `444de810`, L6 `model-endpoints.yaml` commit `217adb13` — one per each of the three prefixes proposal (b) names. The per-attempt detail of the three rolled-back attempts is outside this worktree: loop records live under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md` (stage2.py:140, `record_dir`), and the lanes' branches (`fix/loop-record-other-worktree` and others) are not checked out here. The same handover records the cost frame: one verify slot on main, a full `make verify` at 15–24 minutes, admission waits up to 77 minutes (handover "Where we are", measured 2026-11-20/21).

**Pinning tests a change here meets.** tests/test_stage2.py:15943 (rollback behavior and message), 26042 (`test_derived_leftover_refuses_a_human_decided_document`, asserting `uncommittable()` coverage at 26055), 22916 (rollback vs `RestorationRefused`, parameterized), 15467 (`test_repair_instructions_describe_answer_filtering_and_hand_repairs`, pinning the workflow hand-repair sentence verbatim, hand_rule at 15510–15516), 20369/20443/20450 (pinning the phase-4b gate wording "a targeted check after each runner repair and each orchestrator hand repair").

## Where it lives

- Mechanism: `scripts/stage2.py` — `RUNNER_HELD` 7541, `_held_prefixes` 7564, `uncommittable` 7581, `checkpoint` 7601, `CheckpointRolledBack` 646, attempt loop `run_attempts` 9483 (rollback handler 10108), repair verb `repair` 10730, row selection `repair_targets` 3617, fixed-status vocabulary `fixed_status` 8352, record marking `mark_repaired_findings`/`mark_repaired_record` 8603/8647.
- Doctrine: `docs/WORKFLOW.md` §4 — "### Repairing taken findings" (~1862) and "### Hand repairs by the orchestrator" (1991); phase table in `AGENTS.md` (24, 179).
- Classification source: `provenance.yaml` (`paths:`, human-decided prefixes).
- Evidence: `docs/journal/handover/2026-11-21-night-run-2026-11-20-a-morning.md` (item 6(b), per-lane hand steps, verify-slot frame).
- Neighbouring records: `plans/specs/implementation-verification/spec.md` (bead coding-harness-mfv; the repair attempt limits and derived preparation as a living spec), `plans/changes/archive/2026-11-06-repair-fixed-lines/spec.md` (bead coding-harness-ugi; canonical hand-repair statuses, `repair_targets` behavior, refusal-before-call), `plans/changes/archive/2026-11-16-guard-test/spec.md` (bead coding-harness-0ho, ADR 0023; the guard-test fixed status), `docs/adr/0017-codex-repairs-taken-findings.md` (decision 3: "The orchestrator decides, the verb repairs, the reviewer re-checks"; decision 2: attempt chain and stop rules), `docs/adr/0025-targeted-check-after-repair.md` (targeted check after runner and hand repair; full verify before phase 6), `docs/adr/0021-review-swarms-until-clean.md` (the ladder the loop rows come from), `plans/changes/archive/2026-11-06-index-merge-regenerates/` (the index-regeneration follow-up of a hand repair).

## What is unclear about it

- **The bead's exact wording and class.** `coding-harness-0zhf` is readable only through the tracker (`tools/bd show coding-harness-0zhf`); the Dolt database under `.beads/` is not readable in this phase (`.beads/` in the tree holds only `config.yaml`, `metadata.json`, `hooks/` — no rendered copy is committed, AGENTS.md house rule 2). That it is handover item 6(b) is inferred from the commit message and naming; not proven.
- **The class declaration.** The change's `research.md` header carries no `class:` field yet and no `spec.md` exists, so no class declaration is readable anywhere in the tree for this change; the bead description should name one (AGENTS.md, 2026-10-22).
- **The three occurrences' per-row detail.** Which row ids, which attempt numbers, which diagnostics: the loop records and attempt evidence live outside this worktree (state directory and the lanes' own branches); the handover names only the lanes (L3, L5, L6) and the hand-step commits. Not read, therefore open.
- **The intended remedy shape.** The tree records three existing shapes — an early refusal with a hand-off instruction (legacy-marker refusal, stage2.py:10767), a names-the-file up-front refusal (`new_file_guard`, stage2.py:7342), and a keep-list exception in the checkpoint (`keep`, stage2.py:7586, the draft's own ADR). Which of these the bead wants, whether the batch may be split (committable rows repaired, held-path rows handed over), and what the refusal output must contain are undecided; nothing in the tree decides it.
- **Interaction with the `Broke a test` mark.** The mark "stays the orchestrator's mark" (docs/WORKFLOW.md:1928); a runner-driven hand-off would have to say which side writes what. Open question for the interview.
- **Scope beyond `repair`.** `implement` and `draft` share `checkpoint()`/`uncommittable()` (implement at stage2.py:10240, draft through the same loop); whether the bead concerns only repair rows or all verbs is open.

## Which files a change would have to touch

- `scripts/stage2.py` — the repair verb (`repair`, 10730) and its pre-call refusals; the classification pair `_held_prefixes`/`uncommittable` (7564–7598) it would read; possibly the rollback handler in `run_attempts` (10108–10134).
- `docs/WORKFLOW.md` — §4, the repair section (~1862) and "Hand repairs by the orchestrator" (1991), if the doctrine gains a runner-side hand-off rule; its wording is pinned verbatim by tests/test_stage2.py:15467.
- `tests/test_stage2.py` — the rollback test (15943) and neighbours above; new behavior tests alongside.
- `prompts/04-implement.md` and/or the `REPAIR_FORMAT` constants (stage2.py:383–394), only if the prompt text is part of the remedy.
- `plans/INDEX.md` — machine-rendered (`plans_registry.py --index` after any header edit, docs/WORKFLOW.md:2002–2004); never edited by hand.
- The change's own artefacts under `plans/changes/repair-hand-held-rows/` (`research.md` now; `decisions.md`, `spec.md`, `plan.md` later).
