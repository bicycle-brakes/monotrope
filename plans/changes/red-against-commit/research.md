---
title: "Research — red-against-commit"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-qvf7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# red against commit — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1161 files, 5194 commits, 12 rules.

## Runner exploration — 2026-11-21

Exploration complete. Below is the research, ready to append to `plans/changes/red-against-commit/research.md` (after the stage-2 route line). Note for the runner: the skeleton's frontmatter still says `provenance: human-written`; per the skeleton's own note, filling it with this model output means setting `ai-drafted-reviewed` with `produced_by:` and `review:` (`provenance.yaml`, class `ai-drafted-reviewed`).

---

## What exists today

**The change is an empty folder with a skeleton.** `plans/changes/red-against-commit/` holds only `research.md` (frontmatter: bead `coding-harness-qvf7`, owner Data Architect, status draft, no `class:` key), opened by the commit `bb9f8e5a` "chore(red-against-commit): open change folder for coding-harness-qvf7" on branch `feat/red-against-commit`. `plans/INDEX.md` (line 636, "changes/red-against-commit/research.md") registers it as draft, implementation none, 2026-11-21. No spec, design, plan, decisions or findings exist for this change (Glob over the folder: one file).

**The bead is named in exactly three tree sources, and nowhere is its intent spelled out further.**
- `docs/journal/handover/2026-11-01-five-lane-night.md` ("Beads opened since 12:55 UTC", line 296): "coding-harness-qvf7 (free \"red against\" commit)".
- Same file, the 15:00-block decision record (lines 263–270): y17 folds into 0ho "built as the existing change `guard-test`"; "The free \"red against\" commit is its own bead (coding-harness-qvf7). The ADR answer of 2026-10-29 (yes, ADR 0023) stands."
- Same file, the question that produced it (lines 115–116): "y17 + 0ho (test-strength rows without a red form): one change? How is the planted fault checked? Does a free \"red against\" commit cover saved work?"
- `docs/research/2026-11-01-night-run-plan.md` (lines 81–82): "A free \"red against\" commit (bead coding-harness-qvf7) extends guard-test; it follows that merge."

**The system it extends is implemented, merged and archived.** Guard-test (bead coding-harness-0ho, folded with y17) is `plans/changes/archive/2026-11-16-guard-test/` (spec: status accepted, implementation_status done). Its decision is ADR 0023 (`docs/adr/0023-guard-proof-for-test-only-repairs.md`, status accepted): only a row taken `taken — guard test — <reason>` may be answered `fixed — guard test — tests/<path>::<function>`; the named test must reference `STAGE2_PLANT_FAULT` and plant its real fault only under it; the runner proves qualifying red with the switch and clean green without, both on the attempt's code; phase 6 records each guard test's real fault and a bare conditional failure is a BLOCKER; the form is repair-only; planting branches stay and the gate `guard-test-environment` refuses any verification run with the switch present.

**The runner machinery on this branch** (all `scripts/stage2.py`):
- `GUARD_SWITCH = "STAGE2_PLANT_FAULT"` (line 524); `RED_PROBE_NAME`/`RED_PROBE_SOURCE` (531/532, the runner-owned outcome probe); `RED_FIRST_MINUTES = 10` (526); `GUARD_SOURCE_PROBE_SOURCE` (8175, the planted-leg source collector).
- `red_first(root, baseline, test, key, tools)` (8371) — the ordinary red-first proof. Its `baseline` is a commit: the checkout is a private repository (`_private_repository`, 8047) materialized at `baseline`, then the attempt's `tests/` are restored over it from the current Git-visible tree (`worktree_tree`, 5704) via `git restore --source <current> -- tests`. It needs exit 1 with the probe-recorded qualifying failure (`_red_record_fault`): at least one call failed by the test's own assertion or pytest's failed outcome, setups/teardowns passed, no skip/xfail/XPASS/collection error.
- `guard_test_proof` (8355) and `fixed_test_proof` (8340) share one execution, `_attempt_tree_proof` (8202): the proof runs in a private repository whose checkout is the *attempt's* tree (not a baseline), guarded by tool snapshot, environment filtering (`foreign_env`/`runner_env`), admission lock, time limit, ref comparison (`_ref_targets` 7893, `_proof_reference_guard` 8147) and tree snapshot; the planted leg alone adds `STAGE2_PLANT_FAULT=1` to its own environment.
- The repair verb's baseline is HEAD at run start (`baseline = _git_output(root, "rev-parse", "HEAD").strip()`, line 10991); ordinary answers run `red_first(ctx.root, baseline, anchor, …)` then `fixed_test_proof` (8745–8755) and get the mark `yes — <anchor>`; guard answers run `guard_test_proof` and get the distinct mark `yes — guard test — <anchor>` (8735–8744).
- Authorisation and bookkeeping: `guard_authorised` (8569), refusal of a guard answer on a non-authorised row (8707–8712), `TRIAGE_STATUSES` carries `taken — guard test` (8906), the triage-side guard check (9009–9011), phase-6 guard-evidence prompt constants (307–332) and `split_guard_evidence` (1211).
- The gate: `decisions/gates.yaml` entry `guard-test-environment` (lines 244–252, command `python3 scripts/check_guard_test_environment.py`, blocking, both placements); the script exists (`scripts/check_guard_test_environment.py`, Glob).
- The tests: `tests/test_stage2.py` — `test_guard_answer_accepts_the_named_test_form` (18913), `test_guard_answer_requires_explicit_row_authorisation` (18942), `test_guard_proof_uses_attempt_code_and_planted_switch` (18956), `test_guard_proof_requires_clean_green_without_the_switch` (18990), `test_guard_proof_preserves_outcome_and_execution_guards` (19037), `test_guard_proof_scrubs_failure_diagnostics` (19070), `test_guard_source_uses_python_lines_with_unicode_separator` (19091), `test_guard_source_reads_the_definition_pytest_collected` (19116); a pre-run early exit keyed on `STAGE2_PLANT_FAULT == "1"` stands at 9845.
- Doctrine: `docs/WORKFLOW.md` §4 "Guard test (ADR 0023)" (lines 1965–1984) and the red-first paragraph (1897–1916); `prompts/04-implement.md` repair instructions (lines 140–153) carry both forms to the models.

**The known gap this bead sits beside is recorded verbatim.** `docs/journal/handover/2026-11-01-five-lane-night.md` "Known gaps" (lines 104–108): the shared-refs remedy (implemented since as red-first-own-refs, merged) ended hand proofs, and "A rejected attempt's saved work, once committed, makes the next repair's red-first impossible (noted on bead coding-harness-y17)"; the interim hand remedy was "run repairs one at a time or prove red first by hand (`git show <pre-fix>:<file>` over the file, run the named test, restore)". `save_attempt` (5318) saves a rejected attempt's tree as a commit with parent = baseline under `refs/stage2/attempts/<change>/<label>-<stamp>`, local-only ("no branch push carries" it); a search for readers of that namespace finds only the writer and doc mentions — no proof consumes a saved-attempt ref today (Grep `refs/stage2/attempts` in `scripts/`: three hits, all in `save_attempt` and its neighbours' docstrings).

**`docs/testing.md` still carries the pre-guard wording.** "Reviews find, tests prove" (lines 80–84): "Where a fix lives only in test code, the old code cannot show it red. Today the orchestrator then shows, by hand, a planted fault that turns the new test red while the old test stays green; a runner form for it is open work." The file mentions neither the guard proof nor the switch anywhere (Grep `guard|STAGE2` in `docs/testing.md`: one unrelated hit), and guard-test's Definition of Done coordinated-documents list (`plans/changes/archive/2026-11-16-guard-test/spec.md`, lines 149–155) names `docs/WORKFLOW.md`, three prompts, `templates/findings.md` and the ADR — not `docs/testing.md`.

**The older exploration already mapped the option space.** `plans/changes/archive/2026-11-06-test-strength-rows/research.md` (bead y17, done) lists four candidate forms for proving a test-strength row red (lines 111–141): a runner-applied fault patch, the orchestrator naming the fault at take-time, old-test-versus-new-test on the planted fault, and a formalised green-only exception. Guard-test chose none of them; its spec's Non-goals (lines 126–136) explicitly exclude "Guard proof for initial implementation or the criterion ledger", "Runner-generated fault patches … old-versus-new test comparison, or proof-free exceptions", and its criteria 12 keeps repair-only scope.

**The planted-fault convention this must stay inside:** `docs/testing.md` "How a test is written" (44–53): each new test names its fault (`Planted fault: …`), "A test that has never been red is a test of nothing", mutation names counted by the gate ratchet (`scripts/mutation_evidence.py`); `prompts/05-verify.md` (27–28): "Every new gate comes with its mutation: plant the fault, watch it go red, take it back."

## Where it lives

- This change: `plans/changes/red-against-commit/research.md` (skeleton); registry row `plans/INDEX.md` line 636.
- Bead mentions: `docs/journal/handover/2026-11-01-five-lane-night.md` lines 116, 268–269, 296; `docs/research/2026-11-01-night-run-plan.md` lines 81–82.
- Decision record: `docs/adr/0023-guard-proof-for-test-only-repairs.md` (accepted); its parent contract ADR 0017 (`docs/adr/0017-codex-repairs-taken-findings.md`, decision 4, red-against-baseline wording at line 99).
- Runner mechanism: `scripts/stage2.py` — symbols above; gate list `decisions/gates.yaml`; generated `.github/workflows/ci.yml`.
- Archived neighbours: `plans/changes/archive/2026-11-16-guard-test/` (spec with the twelve criteria, decisions Q-1–Q-5, design, plan, findings), `plans/changes/archive/2026-11-06-test-strength-rows/research.md`, `plans/changes/archive/2026-11-16-red-first-own-refs/spec.md` (bead wkxm — proofs isolated in private repositories with own refs), `plans/changes/archive/2026-11-16-raising-fault-test/spec.md` (bead xrzf — raising-fault instruction change, repair-instruction wording).
- Practice: `tests/test_stage2.py` guard tests (names above); `scripts/check_guard_test_environment.py`.
- Doctrine: `docs/testing.md` (planted-fault convention; the hand-remedy paragraph); `docs/WORKFLOW.md` §4.

## What is unclear

- **The bead's own description is unread.** The tracker is the Dolt database under `.beads/` with no rendered copy committed (AGENTS.md, house rule 2); this phase's read-only tool set cannot run `tools/bd show coding-harness-qvf7`. Its description — which by house rule names the change's class — and any maintainer notes on it are an open question. The archived raising-fault-test research hit the same limit and said so.
- **What "free" names in "free 'red against' commit" is stated nowhere in the tree.** The runner does have a technical term "free" (the review loop's round-1 free swarm, `free_stage` rule, `scripts/stage2.py` 2429–2539, 2999–3078), but no source connects that term to this bead. Two readings are compatible with the three mentions: a cost-free red proof against a commit, or something inside the free review round. The tree alone cannot decide this.
- **The exact target is not decidable from the repository.** "Red against commit" is not implemented and not designed anywhere: `red_first` already *accepts* a commit-shaped `baseline`, but its only caller passes the run's HEAD (10991→8747), and the guard proof runs on the attempt's tree, never against a commit. "Not found" (no design artefact) and "not there" (no runner symbol that proves red against a chosen commit or a `refs/stage2/attempts/` ref) are separate statements; both hold. The recorded facts that bound the intent are the known gap ("saved work, once committed, makes the next repair's red-first impossible"), the question ("Does a free 'red against' commit cover saved work?"), and the night plan's "extends guard-test".
- **Scope: repair-only or beyond?** Guard-test left "initial implementation or the criterion ledger" to separate work (its spec Non-goals, Q-4). Whether qvf7 is that separate work, a commit-baseline form of `red_first` for repairs after committed work, or something else — undecidable from the tree.
- **Not read:** the bead notes and description; `plans/changes/archive/2026-11-16-guard-test/findings.md` beyond its sampled guard-evidence lines (the file is very large); the guard-test `decisions.md` and `plan.md` in full; live pull-request state; the history of `docs/testing.md` (why the hand-remedy paragraph survived the guard-test merge).

## Which files a change would have to touch

Depends on the surface; all three mapped from what exists:

- **A commit-argument red proof in the runner:** `scripts/stage2.py` — the `red_first` call sites (8747, and the repair verb's baseline at 10991), possibly `guard_test_proof`/`_attempt_tree_proof` if the planted proof must also run against a commit, `REPAIR_ANSWER`/`REPAIR_FORMAT`/`REPAIR_FORMAT_FILE_TOOLS` (274–360) if a new answer form is needed, `fixed_status`/`FIXED_TEST`/`check_repair_answer` for any grammar; `tests/test_stage2.py` beside the guard and red-first tests; `docs/WORKFLOW.md` §4 (red-first and guard paragraphs); `prompts/04-implement.md` repair instructions (140–153); `prompts/04b-review-loop.md` if status forms change; `templates/findings.md` if marks change. If the evidence contract of ADR 0017/0023 changes, the amendment is a new numbered ADR, never an edit to an accepted record (guard-test spec, Protected areas).
- **An instruction/doctrine change only** (the raising-fault-test pattern): `prompts/04-implement.md`, `prompts/04b-review-loop.md`, `docs/testing.md` ("Reviews find, tests prove" and "How a test is written"), `docs/WORKFLOW.md` §4 — no runner change.
- **Stays untouched per accepted protected areas:** `scripts/check_criterion_ledger.py` grammar (no new evidence grammar); `AGENTS.md`, `model-endpoints.yaml`, `provenance.yaml`, tracker state, other change folders; `decisions/gates.yaml`, `prompts/`, `templates/`, `.github/` are runner-held during model attempts (guard-test spec, Protected areas — its list, applied here as the accepted precedent).

**Suggested `neighbours:` for the header:** `plans/changes/archive/2026-11-16-guard-test/spec.md` · `plans/changes/archive/2026-11-06-test-strength-rows/research.md` · `plans/changes/archive/2026-11-16-red-first-own-refs/spec.md` · `plans/changes/archive/2026-11-16-raising-fault-test/spec.md`.

---

Nothing was designed, recommended or judged; every statement names its file and symbol. The open questions above (bead description/class, the meaning of "free", the exact target and scope) are the ones the interview must resolve; the tracker is outside this phase's read boundary, so the bead itself is the first thing to read before phase 1a.
