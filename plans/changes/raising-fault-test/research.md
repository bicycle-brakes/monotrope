---
title: "Research — raising-fault-test"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-xrzf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# raising fault test — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), completed
by the model recorded in the frontmatter. The research is AI-drafted and its
human review is pending (`provenance.yaml`, class `ai-drafted-reviewed`,
`review_required: true`).

Stage-2 call, 2026-11-03: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 846 files, 3178 commits, 12 rules.

## Runner exploration — 2026-11-03

The exploration is complete. Here is the research, ready to append to `plans/changes/raising-fault-test/research.md`.

---

## What exists today

**The planted-fault convention is doctrine.** `docs/testing.md` ("How a test is written") states: "Each new test names its fault. Its docstring says which fault the test was red on (`Planted fault: …`)", that older tests are not all rewritten, and that "A test that has never been red is a test of nothing". Doctrine tests "check their fault on a planted copy of the text". Mutation names (`…_goes_red…`, `…_refuses…`, `…_is_caught…`) are counted by the gate ratchet (`docs/testing.md`, "Mutation names"). The gate catalog states the same principle for gates: "What refutes a gate is the counter-check that plants the fault it guards against and shows the run going red; a check that was never red measures nothing" (`docs/governance/gate-catalog.md`, "Before enabling a gate", closing paragraph). The ratchet itself is `scripts/mutation_evidence.py` (`MUTATIONS_NAMEN`, the name-form regex; module docstring says it moved out of `tests/test_ci.py` so a repair of the analyzer can be shown red first, bead coding-harness-diic).

**The convention is practiced widely.** `tests/test_stage2.py` module docstring: "Each test comes with its fault: the mutation list of the plan's slices 2 and 3 was planted one by one and each one turned a test here red" (`tests/test_stage2.py`, lines 10–13). Row-level examples with `Planted fault:` docstrings: `tests/test_pr_sync.py` (rows L1-15, L1-7, L1-11, L1-10, L1-12/L1-14, L2-1, P6-1–P6-3), `tests/test_stage2_research_deep_review.py` (module docstring plus per-criterion comments), `tests/test_repo_settings.py` (planted fault F03; "Fault planted:" comments), `tests/test_stage2_runs.py` (e.g. the UnicodeDecodeError fault docstring), `tests/test_model_endpoints.py` (planted mutants of the real provider remark fed to `opencode_remark_problems`), `tests/test_pi_install.py` ("planted one variant at a time and named in the test"), `tests/test_terms_fixtures.py` (planted expiry fault).

**The precedent guard tests exist by hand.** `tests/test_stage2.py::test_both_anthropic_endpoints_authorize_haiku_5_5_instead_of_4_5` deep-copies `model-endpoints.yaml`, plants the faults `missing`/`replaced`/`retained` per endpoint and asserts `anthropic_haiku_problems` flags each; `tests/test_stage2.py::test_the_current_haiku_instructions_reject_4_5` replaces every `Haiku 5.5` pin with `Haiku 4.5` in the operative texts and asserts `haiku_instruction_problems` flags it. The corresponding findings rows F-1/F-2 in `plans/changes/haiku-5-5/findings.md` were closed "guard test, plants each fault itself; red first impossible because the code was already right — completed by the orchestrating session" (recorded in `plans/changes/guard-test/research.md`, "Precedent").

**The runner's repair proofs today.** `scripts/stage2.py` holds the full machinery on this branch: `repair` (line 7879) with the Codex→Codex→Sonnet route of ADR 0017; answer grammar `REPAIR_ANSWER`/`REPAIR_FORMAT`/`REPAIR_FORMAT_FILE_TOOLS` (lines 274–302); `fixed_status` (6181) and `FIXED_TEST` (427, `^tests/<file>.py::test_\w+$`); `check_repair_answer` (6225), whose only look inside a named test file is the `def <function>(` existence check; `red_first` (6019) — a private repository clone whose `tests/` is the attempt's, the runner-owned outcome probe `RED_PROBE_SOURCE` (435) read back by `_red_record_fault` (5657), `RED_FIRST_MINUTES = 10` (429), interpreter `red_first_python` (5628), exit 1 with a qualifying failure (pytest's own failed outcome counts, bead a7m); `fixed_test_proof` (5916) — the same probe on a private materialization of the attempt's tree, requiring exit 0 and every selected case passing, launched through `verify_lock.hold_admission` with the environment built as `runner_env(foreign_env({...}))` carrying only `STAGE2_RED_REPORT`/`STAGE2_RED_TOKEN`/`STAGE2_RED_SELECTOR`; the allow-list `ENV_ALLOW` (323: PATH, HOME, USER, LOGNAME, SHELL, TMPDIR, LANG, LC_ALL, LC_CTYPE, TERM, TZ, CODEX_HOME) with `foreign_env` (807) and `runner_env` (3987); statuses via `RECORD_INTRO` (512), row selection `repair_targets` (2811), marks `mark_repaired_findings` (6381) and `mark_repaired_record` (6410). The doctrine text of this contract stands in `docs/WORKFLOW.md` §4 ("Repairing taken findings (repair)", including the red-first rule and the two fixed forms) and `templates/findings.md` (the five stage-2 Status words).

**ADR 0023 is accepted; its implementation is not on this branch.** `docs/adr/0023-guard-proof-for-test-only-repairs.md` (status accepted) decides "Test-owned planted fault with explicit authorisation and review": only `taken — guard test — <reason>` authorises `fixed — guard test — tests/<path>::<function>`; the runner requires the `STAGE2_PLANT_FAULT` reference in the named test and proves qualifying red with the switch, clean green without; phase 6 records each guard test's real fault and catches-without-switch verdict, a bare conditional failure is a BLOCKER; the form is repair-only; planting branches stay and a blocking verification gate refuses the switch's presence regardless of value. This adds the guard exception to ADR 0017 decision 4 ("The existing proof and statuses stand"). A repo-wide search on this worktree finds `STAGE2_PLANT_FAULT` only in `docs/adr/0023…`, the `plans/changes/guard-test/` folder and one handover — not in `scripts/`, not in `tests/`, not in `prompts/`, not in `templates/` (searched with Grep; "not there" is verified, not assumed). Likewise `scripts/check_guard_test_environment.py` does not exist in this tree (Glob: no files).

**The neighbour change guard-test is drafted, not implemented.** `plans/changes/guard-test/spec.md` (bead coding-harness-0ho, class feature, implementation_status none) carries twelve acceptance criteria and the terms guard test / authorised row / qualifying red / clean green; `decisions.md` records the maintainer's Q-1–Q-5 (the switch with one red and one green run; orchestrator-only authorisation; mandatory phase-6 check with BLOCKER for a bare conditional failure; repair-only scope; the branch stays and a verify gate refuses a set switch); `design.md` plans a shared attempt-tree proof helper with default clean and explicit planted mode; `plan.md` holds the build sequence, the phase-6 answer format `Guard evidence: <test> — fault: <description> — catches without switch: <yes|no and reason>`, the presence gate `guard-test-environment` and a criterion ledger that is mostly "not yet written". Per `docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md` (lane E) and `2026-11-02-five-lane-night.md` (lane E), the change waits for the maintainer's `guard-test-environment` entry in `decisions/gates.yaml`; the worktree `guard-test` at 2dbfd454 holds five modified files and the untracked presence-check script from a stopped implement attempt — none of it is on this branch. `decisions/gates.yaml` on this branch lists 23 gates, with no `guard-test-environment` entry. No "guard test" wording exists anywhere in `scripts/`, `prompts/` or `templates/` (Grep over those directories: no matches). The related bead coding-harness-y17 (test-strength rows, `plans/changes/test-strength-rows/research.md`) is folded into 0ho; two further guard-related beads are named only in `docs/journal/handover/2026-11-01-five-lane-night.md`: coding-harness-jy1p ("an independent party checks a guard test's planted fault; measure first") and coding-harness-qvf7 (free "red against" commit).

## Where it lives

- Doctrine: `docs/testing.md`; `docs/governance/gate-catalog.md`; `docs/governance/regelwerk.md` (RB-G4/RB-G7, still German-language per house rule 1); `docs/WORKFLOW.md` §4 repair section and the `Broke a test` column.
- Decision record: `docs/adr/0023-guard-proof-for-test-only-repairs.md` (accepted); `docs/adr/0017-codex-repairs-taken-findings.md` decision 4 (the amended contract).
- Runner mechanism: `scripts/stage2.py` (symbols listed above); gate list `decisions/gates.yaml`; generated `.github/workflows/ci.yml`.
- Neighbour change folder: `plans/changes/guard-test/` (research, decisions, spec, design, plan, findings).
- Practice: `tests/test_stage2.py` (precedent guard tests; planted-fault comments throughout), the planted-fault tests listed above.
- This change's own folder: `plans/changes/raising-fault-test/research.md` only — no spec, design or plan exists yet, and the frontmatter carries no `class:` key (read today).

## What is unclear

- **The bead's own wording was not read.** The tracker is the Dolt database under `.beads/` with no rendered copy committed (AGENTS.md, house rule 2), and this phase's read-only tool set cannot render it. The bead coding-harness-xrzf's description — which by house rule names the change's class — and any notes on it are therefore an open question.
- **The change's exact target is not decidable from the repository.** The folder was opened on 2026-11-03 (commit 51839f64, "chore(raising-fault-test): open the change folder") while guard-test (0ho) still stands open and unimplemented on main. Whether `raising-fault-test` means a first concrete guard test that raises its planted fault, a repair to an existing test's fault-raising, or (part of) the runner guard-proof form is stated nowhere in the tree; the stage-2 route line in the skeleton records the Flash route only.
- **Not read:** `plans/changes/guard-test/findings.md` (only referenced through its plan: no phase-2a rows, audit lines preserved); the `guard-test` worktree's five uncommitted files (outside this worktree, outside the read boundary); the live tracker beyond the two 2026-11-02 handovers; live pull-request state.

## Files a change would have to touch

Depends on which surface the change targets; all three are mapped:

- **A planted-fault test in `tests/` only:** the test file itself (docstring or comment naming the fault, per the `docs/testing.md` convention; a mutation-evidence name per `scripts/mutation_evidence.py` if it proves a gate red). No runner or doctrine change.
- **The runner guard-proof form (ADR 0023's mechanism):** `scripts/stage2.py` (`REPAIR_ANSWER`, `REPAIR_FORMAT`, `REPAIR_FORMAT_FILE_TOOLS`, `FIXED_TEST`, `RECORD_INTRO`, `fixed_status`, `check_repair_answer`, a planted/clean execution beside `red_first`/`fixed_test_proof`, `_red_record_fault`, `runner_env`/`foreign_env`, `repair_targets`, `mark_repaired_findings`, `mark_repaired_record`, the phase-6 `review` answer handling) · `tests/test_stage2.py` and `tests/test_ci.py` · new `scripts/check_guard_test_environment.py` · `decisions/gates.yaml` (maintainer-owned; guard-test plan step 5) · `.github/workflows/ci.yml` (regenerated, never hand-edited) · `docs/WORKFLOW.md` §4 · `prompts/04-implement.md`, `prompts/04b-review-loop.md`, `prompts/06-review.md` · `templates/findings.md` · `scripts/check_criterion_ledger.py` must stay untouched — its grammar (`TEST`, `NOT_YET`, `NOT_A_TEST`, lines 68–70) takes no guard status (guard-test spec criterion 12 and its protected areas).
- **Doctrine-only:** `docs/testing.md` ("Reviews find, tests prove" — "a runner form for it is open work" would need updating once the runner form lands).

**Suggested `neighbours:` for the header** (specs of active changes; y17 has research only): `plans/changes/guard-test/spec.md` · `plans/changes/red-first-own-refs/spec.md` · `plans/changes/red-first-pytest-failed/spec.md` · `plans/changes/red-first-install/spec.md` · `plans/changes/test-strength-rows/research.md`.

---

Nothing was designed, recommended or judged; every statement names its file and symbol. The one human question this research leaves: the bead coding-harness-xrzf's description (class and exact target) is only readable through `tools/bd show coding-harness-xrzf` — the tracker is outside this phase's read boundary.
