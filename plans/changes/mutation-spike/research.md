---
title: "Research — mutation-spike"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-bvy
owner: Data Architect
provenance: human-written
tags: [research]
---

# mutation spike — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3364 commits, 12 rules.

## Runner exploration — 2026-11-06

Research complete. Here is the phase-1 prose for `plans/changes/mutation-spike/research.md`, ready to append after the stage-2 call line.

---

## Explorer research — 2026-11-06

Read in the worktree `mutation-spike`, branch `spike/mutation-spike`, head `761e61a6` ("chore(mutation-spike): open the change folder (bead coding-harness-bvy)"). The tracker was not read: this phase has no command tools, and no rendered bead copy is committed (house rule 2, `AGENTS.md`). The bead's current title and state are therefore known only from dated documents, listed below.

### What exists today

**The change's assignment, as written down elsewhere.** The only place that names the work is the night-run plan of 2026-10-20, reserve item 6: "measure test quality with mutation testing (bead coding-harness-bvy) on `scripts/check_research_handoff.py`"; done-when: "A dated note under `docs/research/` with tool and version, commit, score, surviving mutants by kind and run time, as a pull request"; appetite 2 hours; the tool "in a scratch environment, not in the lock"; it "stops when the run would not finish by 06:00 Europe/Berlin" (`docs/research/2026-10-20-night-run-plan.md`, queue table). The morning page of that run was to carry "the mutation score if item 6 ran" (same file, "Morning page"). It did not run: the tenth night-run handover lists item 6 as "not started" (`docs/journal/handover/2026-10-21-night-run-tenth.md`, queue-status table). The bead later moved to lane B ("verify, CI, hooks") of the 2026-10-31 day run as "bvy (spike, build)" with the title "mutation testing on one or two scripts", cleared by the maintainer to build past its plan card to a ready pull request (`docs/research/2026-10-31-run-plan.md`, lane table, "Bead titles" list, and the "Lanes B and C build past the plan card" note dated 2026-10-31 about 21:45 UTC). Nothing later in the tree names a second script for it.

**"Mutation" names two different mechanisms in this repository; the spike is about the second.**

1. *The RB-G4 mutation test per gate* — a hand-written known-bad run that turns a gate red. Held by `tests/test_ci.py`, section "Mutation coverage (RB-G4)": the exemption ratchet `OHNE_MUTATIONSTEST` (seven entries: pytest, ruff-check, ruff-format, markdownlint, lychee, plans-registry, plans-registry-strict), `test_the_mutation_exemption_list_only_shrinks` (cap ≤ 12), `test_every_gate_step_has_a_mutation_test`, `test_the_mutation_ratchet_only_turns_one_way`. The evidence analyzer lives in `scripts/mutation_evidence.py` (`MUTATIONS_NAMEN` name regex — goes_red, red_on, detects_tampering, refuses, is_caught, catches, not_a_write, is_an_error, is_exit_2, never_writes, is_not_a_pass, notices; `pruefling`; `evidence`; `_tests_reaching`), moved unchanged out of `tests/test_ci.py` by the change `mutation-evidence-module` (bead coding-harness-diic; its spec says so and puts "any change to what counts as evidence" out of scope). Rule row RB-G4 in `docs/governance/regelwerk.md` (rule table; still German — that translation is bead coding-harness-yim's, not this change's); naming convention in `docs/testing.md` ("Mutation names") and `prompts/05-verify.md` ("Every new gate comes with its mutation: plant the fault, watch it go red, take it back").
2. *Real mutation testing* — mutating a script and running tests against the mutant. This is "planned, not built" (`docs/testing.md`, "What this does not prove": "Counts measure how much is checked, not how well. A large suite can still miss a fault nobody wrote down. Mutation testing of the scripts is planned, not built."). The bead is the first measurement of this kind in the repository. The ratchet change explicitly excluded it: non-goal "Real mutation testing (running each test against a mutated script)" (`plans/changes/ratchet-mutation-evidence/spec.md`, "Non-goals").

**Prior positions the note must coexist with (recorded decisions, not opened by this spike).** The target architecture names PIT, Stryker and mutmut as the public analogues of principle P6 "A gate must be able to go red" (`docs/architecture/target-architecture.md`, principle table P6) and states in its gap table: "Our one-counterpart-per-test rule is cheaper and enforced. Keep it; run `mutmut` once per release in lakeswitch as a calibration, not a gate" (step 3). The same change that built the ratchet accepted two known limits — "constructs written to fool the static reading of mutation evidence" (maintainer, 2026-10-26, phase-6 rows R10-1 MAJOR and R10-2 MINOR) with follow-up bead coding-harness-4ft9 "mutation evidence from the run itself", class feature (`plans/changes/ratchet-mutation-evidence/spec.md`, last non-goal; `docs/journal/handover/2026-10-27-night-run.md`, "Decisions and preferences" and "Open work"; the 2026-11-02 tracker cleanup folded bead -up2m into -4ft9 — `docs/journal/handover/2026-11-02-five-lane-night.md`, addendum). The name-based rule's false-coverage history is documented: pull request #188 fixed a call-site test that named a gate's script without reaching it (`docs/journal/handover/2026-10-21-night-run-eleventh.md`; the reasoning stands in the `evidence` docstring of `scripts/mutation_evidence.py`, bead coding-harness-a05, option B). No repository text asks this spike to compare its score against the name-based ratchet; the comparison is available ground truth, nothing more.

**Why the measurement has room: what the existing proofs do not hold.** ADR 0013's own limits paragraph: "Whether a named test is collected, passes, is skipped or really tests its criterion stays with `pytest` and the phase-6 review: the gate holds that it is there" (`docs/adr/0013-every-criterion-names-its-proof.md`, "What stays unheld"). The measured failure behind it: deleting 29 of 30 tests in `tests/test_research_currency.py` left `make verify` green (bead coding-harness-909, replayed in the same ADR's Validation section). The planted-fault mechanics already exist in one narrow form: ADR 0023 (guard proof for test-only repairs) runs a named test red under `STAGE2_PLANT_FAULT=1` and green without it, and rejected "runner-owned mutation or replacement of a named checker" as an option there — "gives the runner fault-construction work" (`docs/adr/0023-guard-proof-for-test-only-repairs.md`, "Considered Options", "Decision"; gate `guard-test-environment` in `decisions/gates.yaml` refuses the switch's presence in any green verification). Test-strength rows, the cousin problem in the repair verb, have no red-first form and document candidate planted-fault patch forms (`plans/changes/test-strength-rows/research.md`, "What a red-first proof of a test-strength row can be", "Candidate forms").

**The measured surface.** `scripts/check_research_handoff.py` is 1028 lines; it is the script of gate `research-handoff` (`decisions/gates.yaml`, entry `research-handoff`: command `python3 scripts/check_research_handoff.py`, job `verify`, enforcement `block`, placement `both`, subsets `[docs]`), exits 0 findings / 1 findings / 3 could-not-measure (module docstring, "Usage"). It imports `scripts/research_handoff.py` (165 lines; "one pure function, standard library only, no model, tracker or network" — its module docstring). Its test file `tests/test_research_handoff.py` is 1070 lines with 42 top-level test functions (counted over `def test_`; several parametrised), many already gate-red named, e.g. `test_research_handoff_goes_red_when_a_research_answer_is_removed` and `test_a_lost_research_decision_turns_the_gate_red` — the gate has RB-G4 evidence today through the reaching rule.

**Run-time facts that bound the appetite (measured numbers, with their cut-off).** Full `make verify` was "about 12-13 minutes in total", `tests/test_stage2.py` alone "about 9.5 minutes" (`plans/changes/verify-duration/decisions.md`, Q-1 context, citing WORKFLOW; measured before the per-gate timing instrument of 2026-11-04 landed). Arithmetic, not recommendation: a mutant loop that runs the whole suite per mutant does not fit a 2-hour appetite at that baseline; a loop that runs `tests/test_research_handoff.py` alone per mutant is the shape the appetite allows. That file's standalone runtime is not measured anywhere in the tree — open question below. `verify-duration` is also the precedent for the deliverable form: its spec names a dated note `docs/research/2026-11-04-verify-duration-baseline.md` as a spike deliverable (`plans/changes/verify-duration/spec.md`, criteria 9–10 and the closing path reference).

**No tool is pinned, and none is installed.** The lock is one file, `requirements-ci.txt`, holding pytest 8.3.4, pytest-xdist 3.8.0, pyyaml 6.0.2, jinja2 3.1.6, pydantic 2.13.5, ruff 0.9.10 (compiled with `--exclude-newer 2026-10-05T00:00:00Z`, header comment). A tree-wide search for mutmut, cosmic-ray, PIT and Stryker finds them only in documents (`docs/architecture/target-architecture.md` P6 and gap table; `docs/research/Migrationsplan_Omnigent_Referenzarchitektur.md`, "Lücke 1") — no package, no config, no script. That is a "not there", searched, not a "not found". The night-run plan already places the tool outside the lock (item 6, "scratch environment, not in the lock"), which also keeps `pyproject.toml`/`requirements-ci.txt` untouched (`pyproject.toml` header: lock changes run through `make lock`/`make venv` with `--require-hashes`). Environment facts a run needs: `requires-python >= 3.12` and `[tool.pytest.ini_options] pythonpath = ["."]` (`pyproject.toml`).

**Deliverable placement.** The note lands under `docs/research/` (dated, kebab-case name, like `docs/research/2026-10-08-holding-criterion-tests.md`). It is Markdown outside `scripts/`, `tests/`, `prompts/` and `decisions/`, so a text-only change: local `make verify` is skipped and CI is its gate (`docs/testing.md`, "Where tests run" table note). `plans/INDEX.md` does not index it — the index is generated over `plans/` only (its header: "Every artefact under `plans/`", generated by `scripts/plans_registry.py --index`). The pull request body names the bead (house rule 4, "a pull request names in its body every bead it opens, changes or closes").

**Header state of this change folder.** The skeleton's frontmatter carries no `class:` key (read in full); every other recent `research.md` declares one there (e.g. `plans/changes/swarm-test-speed/research.md`, `class: bounded`). The only written classification of the bead is "(spike, build)" in the 2026-10-31 lane table. The runner's stage-2 line in this file already names route flash, consistent with spike routing (ADR 0020). Also not yet present: the `neighbours:` header line — proposal below.

**Not a neighbour, checked and set aside.** The one living spec, `plans/specs/implementation-verification/spec.md`, is about derived-file preparation before an implement attempt (bead coding-harness-mfv, PR #102) — its path name suggests verification strategy, its content is not about it.

### Where it lives

- Assignment and appetite: `docs/research/2026-10-20-night-run-plan.md` item 6; lane and title: `docs/research/2026-10-31-run-plan.md` (lane B table, "Bead titles").
- Target script and gate: `scripts/check_research_handoff.py`, `scripts/research_handoff.py`, `tests/test_research_handoff.py`, `decisions/gates.yaml` (`research-handoff`), `docs/governance/gate-catalog.md` (research-handoff row).
- Existing "mutation" machinery: `tests/test_ci.py` (RB-G4 section, `OHNE_MUTATIONSTEST`), `scripts/mutation_evidence.py`, `docs/governance/regelwerk.md` (RB-G4, RB-G7), `docs/testing.md` (layers 4, "Mutation names", "What this does not prove"), `prompts/05-verify.md`.
- Prior decisions and limits: `docs/architecture/target-architecture.md` (P6, gap table), `docs/adr/0013-every-criterion-names-its-proof.md`, `docs/adr/0023-guard-proof-for-test-only-repairs.md`, `plans/changes/ratchet-mutation-evidence/spec.md`, `plans/changes/mutation-evidence-module/spec.md`, handovers of 2026-10-21 (tenth, eleventh), 2026-10-27 and 2026-11-02.
- Related test-strength work: `plans/changes/test-strength-rows/research.md`, `plans/changes/guard-test/` (research, spec, decisions), `plans/changes/raising-fault-test/spec.md`, `plans/changes/criterion-test-ledger/spec.md`, `docs/research/2026-10-08-holding-criterion-tests.md`.

### What is unclear

- [GAP] The bead's current tracker state (title, class field, epic) — unreadable from this phase; latest written evidence is the 2026-10-31 lane table. The owner reads it with `tools/bd show coding-harness-bvy` before the interview.
- [GAP] Which second script the 10-31 title ("one or two scripts") means, whether any: no tree text names one; the only named target is `scripts/check_research_handoff.py` (10-20 plan item 6).
- [GAP] Whether the imported module `scripts/research_handoff.py` counts into the same measurement: nothing read states it either way.
- [GAP] Standalone runtime of `pytest tests/test_research_handoff.py`: not measured anywhere in the tree; the appetite arithmetic depends on it.
- [GAP] Tool and version: nothing in the repository pins one (a "not there", searched); the note is required to record "tool and version", so the choice stands open until the run records it.
- [GAP] Whether the score should be read against the RB-G4 name-based evidence for the same gate (precision/recall of the reaching rule): no repository text asks for it; recording it is the note's own judgment call, not settled anywhere.
- Not read, named so this file does not imply they were: the tracker itself; `plans/changes/archive/2026-09-20-2ee-triage/` (referenced by the plans-registry exemption reason); `docs/governance/gate-catalog.md` beyond the research-handoff row.

### Which files a change would have to touch

- New: one dated note under `docs/research/` (the deliverable; text-only change, CI gates it).
- Tracker: the evidence comment or close on bead coding-harness-bvy through `tools/bd`, then `tools/bd dolt push` before the git push (house rule 4 order).
- Nothing else is required by the written done-when: no `pyproject.toml` or `requirements-ci.txt` (scratch environment), no gate list, no test, no `scripts/` change. Follow-up work the measurement surfaces belongs in new beads (`discovered-from`), e.g. anything feeding coding-harness-4ft9, not in this change.
- This folder: this file, and — per the skeleton's own provenance note — `provenance: ai-drafted-reviewed` with `produced_by:` and `review:` once a model fills it.

### Proposed header lines (the runner decides and writes them)

```yaml
class: spike
neighbours:
  - plans/changes/ratchet-mutation-evidence/spec.md
  - plans/changes/mutation-evidence-module/spec.md
  - plans/changes/criterion-test-ledger/spec.md
  - plans/changes/guard-test/spec.md
  - plans/changes/raising-fault-test/spec.md
  - plans/changes/research-currency/spec.md
  - plans/changes/verify-duration/spec.md
```

Sourced from the tree on 2026-11-06 in the worktree at `761e61a6`; every count above carries that cut-off.
