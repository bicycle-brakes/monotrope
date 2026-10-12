---
title: "Research — ledger-instance-layout"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-s9m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, criterion-ledger, kit, instances]
---

# Criterion-ledger gate on an instance layout — Research

Phase 1 for bead coding-harness-s9m, read against `origin/main` on
2026-10-12. Loop row L3-4 of change criterion-test-ledger (bead
coding-harness-909, ADR 0013) was rejected as a disclosed limit: the
`criterion-ledger` gate ships with enforcement `block` and exits 3 (cannot
measure) when `plans/changes/` is missing, so `make verify` turns red in an
instance whose plans are laid out differently. The bead asks to run the gate
against an instance layout before the first pinned release, or to decide that
it does not block on a missing root. Related: bead coding-harness-wpv (an
adoption date for instances that receive the gate later) and the adoption
record of change adr-owning-change (bead coding-harness-afa,
`decisions/adoption.yaml`, not yet merged).

## The instance read for this question

LakeSwitch (`lakeswitch-ai`, `origin/main` at `ce88eee`, read through the
GitHub API by the orchestrating session on 2026-10-12): `plans/changes/`
exists and holds 16 change folders; 15 carry a `plan.md` and 14 a `spec.md`.
None of the 15 `plan.md` files has a `## Criterion ledger` or a
`## Tests per criterion` heading (each counted 0). So the layout root is the
same as here; what differs is that every existing plan predates the ledger.

## Questions for the exploration

1. How `scripts/check_criterion_ledger.py` finds its input: the root it
   expects, what it does when `plans/changes/` is missing, when a `plan.md`
   has no ledger section, when a `spec.md` has no numbered criteria, and when
   a change is archived; which exit codes it uses and which tests pin each.
2. How `decisions/gates.yaml`, `scripts/ci_gates.py` and the `make verify`
   path treat exit 3 for a gate with enforcement `block`, and whether any
   gate already distinguishes "nothing to measure" from "cannot measure"
   (for example `check_adr_answers.py`'s "examined nothing", the
   `plans_registry.py` ramps).
3. How the gate travels with the kit (`scripts/kit/manifest.yaml`,
   `scripts/kit/probe.py`), and what an instance that pins the kit receives:
   the gate's entry, its enforcement, and any per-instance setting.
4. Which date or cut-off mechanisms exist today that would let an instance
   adopt the gate from a given day on (the `_bestand_ramp` /
   `_praesenz_ramp` of `plans_registry.py`, the interview-minimums gate's
   cut-off, anything in `decisions/`), so the change can reuse one.

Stage-2 call, 2026-10-12: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 370 files, 924 commits, 12 rules.

## Runner exploration — 2026-10-12

### What exists today — the gate's input rule and its three verdicts

`scripts/check_criterion_ledger.py` takes its root from the `--root` flag, default `.` resolved (`main()`), and expects the change tree at the constant `CHANGES_DIR = "plans/changes"` beside the constants `ARCHIVE = "archive"`, `HEADING = "## Criterion ledger"` and `CUTOFF = date(2026, 10, 11)` (module head; the CUTOFF comment says changing it is a governance act, stated in `docs/WORKFLOW.md` beside this gate). `measure(root)` raises `CannotMeasure` in exactly three cases: the root is not a readable directory, `root/plans/changes` is not a directory ("has no plans/changes/ directory"), or the changes directory exists but cannot be listed (`OSError`, criterion 18 of the change's spec). `run()` catches `CannotMeasure`, prints `criterion-ledger: not measured — …` and returns 3; the module docstring fixes the vocabulary "0 = nothing found, 1 = findings, 3 = could not measure". Two further facts complete the input rule: a change folder without a `plan.md` — live or archived — is not examined at all (`_measure_plan` returns before reading, docstring "spec criterion 1", pinned by `tests/test_check_criterion_ledger.py::test_a_live_change_without_a_plan_is_not_examined`), and an unsearchable single change folder is one finding while the run goes on (criterion 17, pinned by `test_an_unsearchable_change_directory_is_a_finding_and_later_plans_are_still_read`) — a per-folder permission problem and a root that cannot be listed are different verdicts.

The gate already separates "nothing to measure" from "cannot measure" on its own: with `plans/changes/` present but no held plan, `run()` prints `criterion-ledger: examined nothing — no plan.md under plans/changes/ is held; …` and returns 0 (the `tally.held == 0` branch, pinned by `test_an_empty_tree_says_it_examined_nothing`; `test_a_live_change_without_a_plan_is_not_examined` asserts the same wording). Exit 3 is reserved for the structural cases above, pinned by `test_a_root_it_cannot_measure_exits_3` (empty directory, missing path, a file as root) and `test_an_unlistable_plans_changes_directory_exits_3_without_a_traceback` (a `chmod 000` `plans/changes/`, review-loop row L3-5). The date exemption is per plan, not per instance: `exempt_by_date()` exempts an archived ledger-less plan only when its header holds exactly one plain `date: YYYY-MM-DD` strictly before the cut-off — the seven-case table including `date: 2026-10-11` (held) and quoted, commented, doubled or impossible dates (measured) stands in `test_an_archived_plan_without_a_ledger_is_exempt_only_by_an_earlier_plain_date`, and `test_every_live_plan_is_held_whatever_its_date_and_class` holds a live plan dated 2026-09-01 to the ledger whatever its date.

### What exists today — how exit 3 lands in `make verify` and in CI

`decisions/gates.yaml` declares the gate as id `criterion-ledger`, command `python3 scripts/check_criterion_ledger.py`, job `verify`, enforcement `block`, floor `false`, placement `both` (pinned by `tests/test_check_criterion_ledger.py::test_gates_yaml_declares_criterion_ledger`), and its header states the rule this change asks about: "Unreachable counts as failing: a gate that cannot measure exits 3, and the runner turns that red on a block gate (bead coding-harness-4t8)". The two runners implement exactly that, with no special case for the code 3: `scripts/verify_all.sh` iterates the TSV from `ci_gates.py --commands --tsv` and sets `fehler=1` → "VERIFY RED" (exit 1) whenever a `block` gate's `sh -c` returns non-zero — any non-zero, 3 included; in the derived workflow, `ci_gates.py::_schritt` adds `continue-on-error: true` only to `advisory`/`report` steps, gives every gate step `if: ${{ !cancelled() }}`, and `_summary_job` fails the `verify` check unless the matrix job's result is exactly `success`. So today, on a root whose `plans/changes/` is missing, `make verify` is red at `criterion-ledger` — the situation research.md's header describes for an instance with a different layout.

Two sibling gates already answer the same question differently, by reading: `scripts/check_adr_answers.py` checks only that the root is a readable directory (`run()`'s `os.access` check) — its `anchors()` globs `plans/changes/*/spec.md` and the archive glob, and a glob over a missing `plans/changes/` yields nothing, so such a root ends in the `not ex.features` branch of `run()`: `adr-answers: examined nothing — read 0 change anchors, none of them a feature`, exit 0, green. `scripts/check_interview_minimums.py` returns `[]` from `_active_changes()` when `plans/changes/` is missing, and its `CannotMeasure` (exit 3, `main()`) is reserved for git failures and the detached-HEAD-at-`origin/main` case of `_base()`; with no ADR paths and no subject folders it prints `interview-minimums ok: 0 change(s) measured … stock exempt`, exit 0. Not found versus not there, stated separately: for a root without `plans/changes/`, criterion-ledger exits 3 (red on block), adr-answers exits 0 (green), interview-minimums exits 0 in a git checkout (green) — three behaviours exist today, none unified.

### What exists today — what an instance receives with the kit

`scripts/kit/manifest.yaml` scaffolds `geruest_ordner` `plans/changes`, `plans/changes/archive`, `plans/specs` as empty folders (created with `.gitkeep` by `probe.py::_baue`), and carries as `mechanismus` under its longest-prefix rule (`probe.rolle()`): `scripts/check_criterion_ledger.py` ("the gate file travels, so its script does (ADR 0013)"), `tests/test_check_criterion_ledger.py` ("builds its own trees and reads only files that travel; holds in the probe copy"), the whole `decisions/` prefix ("im Zielrepo gilt dieselbe Datei" — so `gates.yaml` travels), `.github/workflows/ci.yml` ("reist paarweise mit decisions/gates.yaml"), plus `scripts/ci_gates.py`, `scripts/verify_all.sh`, `scripts/check_adr_answers.py`, `scripts/plans_registry.py`, `scripts/ramp_valves.py`, `scripts/harness.py`. Travel of this gate's script and test is pinned by `tests/test_check_criterion_ledger.py::test_the_kit_carries_the_script_and_its_test`.

One measured inconsistency in today's tree: `scripts/check_interview_minimums.py` is named by no manifest rule — a search of `scripts/kit/` for `interview`/`check_interview_minimums` matches only `probe.py`'s comments about `prompts/01a-interview.md` — so it falls under the `scripts/` catch-all rule, role `bestand` ("Validatoren mit Domaenenbezug … Was mitreist, steht oben"), and stays home, while its gate entry travels inside `decisions/gates.yaml` and the derived `ci.yml` that travels runs `python3 scripts/check_interview_minimums.py` as a step. Nothing in the tree measures that consistency: `probe.py::_baue`/`_faelle` copy the `mechanismus` files and run only `pytest tests/` in the throwaway repo — `make verify` and the gate commands are never executed there; the test list of `tests/test_kit.py` (read in full, function names) holds no gate-command↔manifest case; the orphan-script tests of `tests/test_ci.py` (`test_an_orphan_shell_script_gets_flagged` docstring) state the same split — "only the explicitly named scripts are `mechanismus`, the rest is `bestand`" — without checking gate commands. Per-instance settings the gate file knows today: none — the schema of `decisions/gates.yaml` (header comment) and `ci_gates.py::validate_schema` enumerate `id/title/command/action/job/enforcement/floor/placement/needs_tracker/needs_history/reason/with`; `validate_schema` does not refuse an unknown key in a gate entry, but `ci_gates.gates()` reads only the known keys, so an extra key would be carried by nothing.

### What exists today — the dated-transition mechanisms to reuse or sit beside

Four exist, three of them live: (1) `check_criterion_ledger.py::CUTOFF` (2026-10-11), the per-plan archive exemption, whose governance sentence in the `docs/WORKFLOW.md` "Criterion tests" row is pinned by `test_the_workflow_names_the_gate_and_its_exemption` and `test_the_workflow_row_makes_moving_the_cutoff_a_governance_act`; (2) `check_interview_minimums.py::CUTOFF` (2026-10-8), prospective-only — a change is subject when its spec header `date:` is strictly later, the stock stays exempt active and archived (`_spec_class_and_date`/`measure()`, phase-6 rows F-10/F-11 in its comments; the `docs/WORKFLOW.md` "Interview" row and the `gates.yaml` reason document it), an unreadable date is measured rather than exempt; (3) the `Ramp` vocabulary of `scripts/_verdict.py` — `condition`, `predicate`, `target`, `until_then`, `deadline: date | None`, `due` true when the predicate holds or `date.today() >= deadline` — consumed by `scripts/ramp_valves.py` (the `ramp-valves` block gate; `REGEL_VENTILE` deadlines 2026-11-30/2026-12-31; its docstring names `tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open` as the enforcer) and by `scripts/plans_registry.py::_bestand_ramp` (`Ramp(name="bead-ohne-artefakt-bestand", target=DRIFT, until_then=INFO, deadline=2026-11-30)` over `BESTAND_OHNE_ARTEFAKT`). (4) `_praesenz_ramp` of `validate_change_artefacts.py` is named in `_bestand_ramp`'s docstring, but the name occurs nowhere else in the worktree (searched; matches only `plans_registry.py`, the archived interview-minimums research, and this change's research.md), and `scripts/validate_change_artefacts.py` does not exist (`Glob scripts/validate*` → no files) — the absence is already recorded in `plans/changes/attempt-diagnostics/research.md` ("does not exist in this tree, searched 2026-10-11") and in the bootstrap quote block of `docs/WORKFLOW.md`, while two later passages of that same document and the phase-gate lines of `prompts/02-spec.md`/`prompts/03-plan.md` name the validator in the present tense — an internal tension of the documentation, stated here without judging it. For context, ADR 0013 (`docs/adr/0013-every-criterion-names-its-proof.md`) already fixes the reach: the gate travels at once (Q-5), "an instance runs the gate without a trial period here first", "how the instance's plans are laid out was not read for this record", instance delivery is pinned to the release of bead coding-harness-dj9, and "not validated by this record: an instance running the gate".

### What is unclear

The bead bodies were not read by the explorer (no shell). The orchestrating session read bead coding-harness-s9m with `tools/bd show` on 2026-10-12; this file's header quotes it faithfully. The kit manifest gap for `scripts/check_interview_minimums.py` is planned to close in change adr-owning-change (bead coding-harness-afa, maintainer answer Q-3: the interview-minimums gate travels with the kit; its plan touches `scripts/kit/manifest.yaml`), not yet merged. `decisions/adoption.yaml` (adr-owning-change, bead afa) is not in this worktree (`Glob decisions/**` lists only `answers/*/adr.yaml` and `gates.yaml`), which matches "not yet merged" in research.md's header; whether it has landed on `origin/main` since is unverified here. The LakeSwitch figures in this file's "instance read" section rest on the orchestrating session's GitHub API read at `ce88eee`; this session read nothing outside the worktree and cannot confirm them. Not found in this tree: any script or test that runs the gate commands (as opposed to `pytest`) inside a scaffolded instance — whether the probe copy's `make verify` would be red is therefore unknown, not measured.

### Which files a change would have to keep in step

The dependency wiring as it stands: the gate's root/verdict logic lives in `scripts/check_criterion_ledger.py` (`CHANGES_DIR`, `measure`, `run`, `CUTOFF`); its behaviours are pinned in `tests/test_check_criterion_ledger.py` (the two exit-3 tests, the empty-tree test, the kit test, the two WORKFLOW-row tests); the gate's declaration and both runners flow from `decisions/gates.yaml` through `scripts/ci_gates.py` into the generated `.github/workflows/ci.yml` (hand edits fail the `ci-drift` gate; regeneration is `python3 scripts/ci_gates.py --generate-ci`); the governance sentence lives in the `docs/WORKFLOW.md` "Criterion tests" row and is pinned by name; the kit side is `scripts/kit/manifest.yaml` plus `scripts/kit/probe.py` (`REIST_NICHT`, the closed `GRUENDE` vocabulary, the `DECKEL` that may only move with a reason in the diff); the dated-transition precedents live in `scripts/check_interview_minimums.py`, `scripts/ramp_valves.py` with `scripts/_verdict.py`, and `scripts/plans_registry.py`; and the plan prompt's ledger section in `prompts/03-plan.md` is pinned by `test_the_plan_prompt_requires_the_ledger`, whose phase-gate line names the nonexistent `validate_change_artefacts.py`.
