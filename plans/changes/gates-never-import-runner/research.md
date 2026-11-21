---
title: "Research — gates-never-import-runner"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7ayv
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# gates never import runner — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1161 files, 5231 commits, 12 rules.

## Runner exploration — 2026-11-21

Exploration complete. Here is the research, prose ready to append to `plans/changes/gates-never-import-runner/research.md`.

---

## What exists today

**The change's origin is a research note, not yet a decision.** `docs/research/2026-11-18-trust-pyramid-against-the-harness.md` (§6, building block 11, "Lock the import direction") states the rule this change names: no file under `scripts/check_*.py` imports `stage2`, because "a gate is read-only, while the runner writes, calls foreign models and takes the verify admission" — and it names this bead: "a ratchet, in the form of RB-G4's mutation ratchet (bead coding-harness-7ayv)". The same section header says the eleven blocks are "a **proposal, not a decision**: no bead, no change folder, no code" (that sentence predates this change folder, opened by commit `3ed62ebe`).

**The rule's declared subject set is small and complete.** `scripts/check_*` contains exactly twelve Python gate scripts (`check_adr_answers.py` through `check_research_handoff.py`) plus one shell script (`check_worktree_state.sh`). Their complete import surface today: standard library, `venv_guard`, `yaml`, and three in-repo leaves — `adoption` (`scripts/check_interview_minimums.py:69`, `scripts/check_question_context.py:57`), `check_adr_answers` (`scripts/check_interview_minimums.py:70`), `research_handoff` (`scripts/check_research_handoff.py:48`, annotated "the one derivation the runner shares"). A scan of `scripts/` for imports of `stage2`/`verify_run`/`verify_all` finds **no** check script among them — the property holds on this tree (my scan, 2026-11-21, branch `test/gates-never-import-runner`), as the note measured on 2026-11-18.

**The dependency direction runner → gate library is established and load-bearing.** `scripts/ci_gates.py` is the only reader of the one gate list `decisions/gates.yaml` (its module docstring; D-10/O-4, bead coding-harness-bo0). `scripts/verify_run.py` (the two-phase local verification scheduler) imports `ci_gates` at `scripts/verify_run.py:82` and selects gates through `ci_gates.selection_at` (module docstring); `scripts/stage2.py` imports both `ci_gates` (`scripts/stage2.py:198`) and `verify_run` (`scripts/stage2.py:208`). The `research-handoff` gate and the research runner share the leaf `scripts/research_handoff.py` (`scripts/stage2_research_run.py:44` imports it; `scripts/check_research_handoff.py:48` too) — shared leaf, no gate→runner edge.

**"The runner" has a canonical narrow definition.** The archived runner-clock spec (`plans/changes/archive/2026-11-16-runner-clock/spec.md`, Terms) defines: "**Runner:** `scripts/stage2.py`; imported components retain their own clock boundaries." `tests/runner_clock_guard.py:55` encodes exactly that set (`GUARDED_FILES` holds only `scripts/stage2.py`) with the comment that every other `scripts/stage2*.py` keeps its own boundary. Two other "runner" meanings exist and must not be confused with it: the local verify runner (`scripts/verify_all.sh`, called by `make verify`; `scripts/ci_gates.py` OHNE_AUFRUFER entry "Der lokale Lauf fuer Menschen") and an unrelated change folder `plans/changes/hermes-runner/` (not read in this pass).

**The census is the one gate-adjacent module that does import the runner.** `scripts/research_census.py:22` has a module-level `import stage2  # noqa: E402` and uses `stage2.research_visible_text` (`research_census.py:39`; defined at `scripts/stage2.py:1300`, the CommonMark fence masker) and `stage2.producer_for` (`research_census.py:53`; defined at `scripts/stage2.py:1870`, the endpoint→program map). The census carries gate identity outside `decisions/gates.yaml`: `GATE = "research-census"` (`scripts/research_census.py:28`) and an adoption day `research-census: 2026-11-10` in `decisions/adoption.yaml`. It has no row in `decisions/gates.yaml` (checked the full command list) — it is measured through the pytest gate: `tests/test_explore_provenance.py:28` imports it lazily and fails on findings, and `tests/test_stage2_research_deep_review.py:808-826` asserts swarm output passes it. `scripts/ci_gates.py` lists it in `OHNE_AUFRUFER` as a library that "only reads research files, never rewrites them". Under the note's declared scope (`scripts/check_*.py`), `research_census.py` is **not** covered — it is not named `check_*.py`; it is the one live `stage2` import outside the stage2 family and the runner entry points.

**Other `stage2` importers are all outside the gate scope.** Entry points with lazy imports: `scripts/run_report.py:57,65`, `scripts/research_capture.py:803-1005`, `scripts/stage2_runs.py:51`. Inside the stage2 family there are deliberate circular-lazy imports a guard must not cut: `scripts/stage2_availability.py:145` (`from stage2 import scrub`), `scripts/stage2_availability.py:965` ("imported here: that module imports this one"), and `scripts/stage2.py`'s many lazy family imports (`scripts/stage2.py:1707,9193,11645`, among others).

**Enforcement precedents to sit beside (facts, not a design).** RB-G3 and RB-G4 are rule rows in `docs/governance/regelwerk.md` (lines 134-135) held by named tests in `tests/test_ci.py` (`test_every_script_has_a_caller_or_a_declared_reason`, `test_every_gate_step_has_a_mutation_test`, `test_the_mutation_ratchet_only_turns_one_way`); the shrink-only ratchet pattern exists as `OHNE_AUFRUFER` with `test_the_test_exemption_list_only_shrinks` (comment at `scripts/ci_gates.py:304`); `scripts/mutation_evidence.py` is "the gate ratchet's analyzer (RB-G4)" (its `OHNE_AUFRUFER` entry). A static AST import guard exists in `tests/test_atomic_test_log.py::test_stand_ins_stay_visible_and_contact_free` ("imports a contact module", lines 789-815). The valve machinery is `scripts/ramp_valves.py` (its own gate, `decisions/gates.yaml` id `ramp-valves`): a deliberately-open valve needs what/how/target, and `tests/test_ramp_valves.py` fails when a valve is due. AGENTS.md house rule 9 states the principle such a rule takes hold through: "A rule of this kind takes hold through a check that goes red, not through prose."

## Where it lives

- Rule origin: `docs/research/2026-11-18-trust-pyramid-against-the-harness.md` §6, block 11.
- Gate list and reader: `decisions/gates.yaml` (schema_version 3); `scripts/ci_gates.py` (`gates()`, `selection_at`, `OHNE_AUFRUFER`); generated views `.github/workflows/ci.yml` and `docs/governance/gate-catalog.md` (held to their derivations by the `ci-drift` gate and `tests/test_gate_catalog.py`).
- Gate scripts (the rule's subjects): the twelve `scripts/check_*.py` files listed above.
- Runner: `scripts/stage2.py` (canonical definition in the runner-clock spec); verify scheduler `scripts/verify_run.py`; local runner `scripts/verify_all.sh`.
- The census exception: `scripts/research_census.py` with consumers `tests/test_explore_provenance.py`, `tests/test_stage2_research_deep_review.py`, and `decisions/adoption.yaml`.
- Guard precedents: `tests/test_ci.py`, `tests/test_atomic_test_log.py`, `tests/runner_clock_guard.py`, `scripts/ramp_valves.py`, `docs/governance/regelwerk.md` (RB-G3, RB-G4).

## What is unclear about it

- **Scope of "runner" in the guard.** The note names only `stage2`; the runner-clock spec defines the runner as `scripts/stage2.py` alone; `verify_run.py` and the `stage2_*` family are related but undeclared. Which module set the guard forbids is a spec decision.
- **The census sits outside the note's declared scope.** `scripts/research_census.py` imports `stage2` and is gate-adjacent (its own `GATE` id, adoption day) but is not `check_*.py`. Whether this change cuts that import — and where `research_visible_text` and `producer_for` would live afterwards, given runner-side consumers (`scripts/stage2.py:1352,1370,1457` and `scripts/stage2_availability.py:1488`) — is stated nowhere I read.
- **The maintainer's decision status.** The note self-describes as a proposal; the bead `coding-harness-7ayv` (tracker under `.beads/`, Dolt, no rendered copy committed — not readable in this pass) presumably carries the intent and class. "Not read", not "none".
- **The enforcement vehicle.** Rule row in `regelwerk.md` (with a level), plain pytest guard, ratchet entry, valve, or a combination — the note gestures at RB-G4's ratchet form; how a new RB row and its level are added I did not read (`tests/test_regelwerk.py` unread).
- **The test-suite boundary.** Tests import `stage2` legitimately to test it (`tests/test_stage2.py:59`, `tests/test_pi_contract.py:47-51`, `tests/test_explore_provenance.py:18`), and the pytest gate therefore transitively imports the runner; the note's `check_*.py` wording avoids this, but the spec should state the boundary explicitly.

## Which files a change would have to touch

- The guard itself, wherever it lands: most plausibly `tests/test_ci.py` (home of the RB-G3/RB-G4 script-set tests) or a new `tests/test_*` file; `docs/governance/regelwerk.md` if it becomes an RB row; `scripts/ramp_valves.py` only if a valve is declared.
- If the census import is cut: `scripts/research_census.py`, `scripts/stage2.py` (home of the two reused functions), `scripts/stage2_availability.py` (a runner-side `producer_for` consumer), with `tests/test_explore_provenance.py` and `tests/test_stage2_research_deep_review.py` held behavior-identical; possibly a new shared leaf module.
- No change to `decisions/gates.yaml` is forced if the guard rides the pytest gate; a separate gate row would additionally regenerate `.github/workflows/ci.yml` (`python3 scripts/ci_gates.py --generate-ci`) and `docs/governance/gate-catalog.md` (`--catalog`).
- The change folder's own artifacts under `plans/changes/gates-never-import-runner/` (`research.md` exists as the skeleton; the Stage-2 call line from 2026-11-21 is already recorded there).

---

**Suggested `neighbours:` header** (specs already known to relate): `plans/changes/archive/2026-11-16-runner-clock/spec.md` (canonical Runner definition), `plans/changes/archive/2026-11-16-explore-provenance/spec.md` (census contract and adoption day), `plans/specs/implementation-verification/spec.md` (living spec; runner's local verification measurement), `plans/changes/verify-cheap-before-admission/spec.md` (the admission the note's rationale names; not read in this pass), `plans/changes/research-currency/spec.md` (sibling check-script change; cited by `scripts/check_research_currency.py:9`; not read in this pass).
