---
title: "Research — ci-caller-rule"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-8sxb
owner: Data Architect
provenance: human-written
tags: [research]
---

# ci caller rule — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3593 commits, 12 rules.

## Runner exploration — 2026-11-07

The exploration is complete. Here is the research, ready to append to `plans/changes/ci-caller-rule/research.md`, followed by the neighbours line for the file's header.

---

## Proposed addition to `plans/changes/ci-caller-rule/research.md`

### What exists today

**The rule.** Every script under `scripts/` — `*.py` and `*.sh`, names not starting with `test_` — must stand either as `scripts/<name>` inside `.github/workflows/ci.yml`, or as `scripts/<name>` inside `scripts/verify_all.sh`, or as a key in the dict `ci_gates.OHNE_AUFRUFER` with a reason (`tests/test_ci.py`, function `test_every_script_has_a_caller_or_a_declared_reason`, with the pure decision in `_heimatlose_namen` and the candidate inventory in `_scripts`). The test's docstring dates the rule to 2026-08-14, when nine of twenty-one scripts had no caller and nowhere said which absences were intentional; the ci_gates.py comment above the dict cites review item RB-G3 (`scripts/ci_gates.py`, comment at the `OHNE_AUFRUFER` block). `ci_gates.py` itself carries no entry: its docstring in the test records that it counts as wired as soon as `verify_all.sh` starts it (test docstring; the runner names `scripts/ci_gates.py` at four places).

**The matching is textual.** `_heimatlose_namen` searches for the literal substring `scripts/<name>` in the two files. A dot-path form never matches: the runner execs the admission helper as `-m scripts.verify_lock` (stated in `verify_lock.py`'s own entry reason, `scripts/ci_gates.py`), which is why that script needs its declared entry. `verify_all.sh` both holds an entry (`scripts/ci_gates.py`, last dict entry) and names itself in its own usage text, so the string check would pass for it either way.

**The callers are generated, not hand-written.** `ci.yml` is derived from the one gate list `decisions/gates.yaml` by `python3 scripts/ci_gates.py --generate-ci`; hand edits fail the `ci-drift` gate (`scripts/ci_gates.py` module docstring and function `check_ci`). A new CI step for a script therefore enters through `decisions/gates.yaml`, never through the workflow file.

**Coverage arithmetic today.** `scripts/` root holds 57 files: 51 `*.py`, 2 `*.sh`, and 4 `*.mjs` (directory listing). The rule's candidates are the 53 `*.py`+`*.sh` files. Of these, 37 are declared in `OHNE_AUFRUFER` (`scripts/ci_gates.py`, dict `OHNE_AUFRUFER`; counted entries, read in full), and 17 resolve through callers: 16 distinct names appear as `scripts/…` in `.github/workflows/ci.yml` (grep over the generated file: `ci_gates.py`, `render_beads_export.py`, `plans_registry.py`, `check_docs.py`, `check_frontmatter_current.py`, `check_bead_export.py`, `check_dangling_bead_ids.py`, `check_decision_continuity.py`, `check_adr_answers.py`, `check_interview_minimums.py`, `check_question_context.py`, `check_criterion_ledger.py`, `check_research_handoff.py`, `check_guard_test_environment.py`, `ramp_valves.py`, `check_research_currency.py`), plus `verify_duration.py` named only in `scripts/verify_all.sh`. With the one double count (`verify_all.sh`), declared + wired − overlap = 53, exactly the candidate set. This is arithmetic over the sources, not a test run — the suite was not executed in this phase.

**The rule does not see four scripts.** `_scripts()` globs only `scripts/*.py` and `scripts/*.sh`, non-recursive. The four `.mjs` files under `scripts/` — `stage2_repository_pathlock.mjs`, `stage2_research_catalog.mjs`, `stage2_research_tools.mjs`, `stage2_session_policy.mjs` — appear in neither `ci.yml` nor `verify_all.sh` (grep over both for `scripts/…`), and none has an `OHNE_AUFRUFER` key. They are neither wired nor declared; the rule never asks about them. Who runs them today: `stage2_session.py` loads the policy copy (`POLICY_SOURCE`), `stage2_research_run.py` installs the tools and pathlock extensions (two sites), `stage2_availability.py` and `research_capture.py` call the catalog bridge, and the tests drive them through the `tests/stage2_*_driver.mjs` runners without Pi.

**The `scripts/kit/` subdirectory is also outside the glob**, and the kit probe documents the interplay: `ci_gates.py` travels into throwaway kit repositories with `OHNE_AUFRUFER` inside, where entries name files that are not present there — recorded as expected-red cases of class `bestand-dieses-repos` (`scripts/kit/probe.py`, numbered comment block; the `omnigent_policy.py` case at the comment dated 2026-09-29, and the caller-rule counter-test raised the count 61 → 62 on 2026-09-14, comment dated 2026-09-14). The block is a ledger: adding or removing a `tests/test_ci.py` test of this rule can move the probe's expected-red counter.

**Two sister ratchets share the file search.** The test-occurrence ratchet asks whether a test executes each script — import of the module or its name as a string literal in a `tests/test_*.py` file, measured over the syntax tree so comments and prose mentions do not count (`tests/test_ci.py`, `_zeichenketten`, `_belegt`, `test_every_script_has_a_test_or_a_declared_reason`, and the planted-fault control `test_a_mere_mention_does_not_count_as_a_test`). Its exemption list `ci_gates.OHNE_TEST` is empty since bead cke, 2026-09-22 (comment above the dict). The mutation ratchet `OHNE_MUTATIONSTEST` is not in `ci_gates.py` at all — it lives in `tests/test_ci.py` itself with 7 entries and a shrink-only cap of 12 (`tests/test_ci.py`, dict `OHNE_MUTATIONSTEST`, `test_the_mutation_exemption_list_only_shrinks`); the section comment distinguishes the three questions: does a script run, can its gate go red, does a test execute it.

**The declaration list is held honest by two age checks.** `test_no_declared_reason_stands_for_a_script_that_has_a_caller` refuses an entry for a script that already appears in `ci.yml`, an entry for a script that does not exist, and a reason shorter than ten characters. `test_no_declared_reason_cites_a_closed_or_unknown_bead` reads the tracker through the one access point (`_bead_status`, via `bead_render.render_pfad`) and refuses reasons citing closed or unknown bead ids. The drift job is tied in by `test_the_drift_job_holds_only_steps_that_can_run`, whose docstring states that everything not runnable here carries a reason in `OHNE_AUFRUFER`.

**Language state (house rule 1).** The rule's identifiers are German in code: `OHNE_AUFRUFER`, `OHNE_TEST`, `OHNE_MUTATIONSTEST`, `_heimatlose_namen`, `_belegt`, `_zeichenketten`, `_scripts` (`scripts/ci_gates.py`, `tests/test_ci.py`). Seven of the 37 reasons are written in German (`_verdict.py`, `bead_render.py`, `gate_record.py`, `handover_schema.py`, `new_change.py`, `check_worktree_state.sh`, `verify_all.sh` — line spans in the dict read in full); the other thirty are English, as is the bulk of the module's messages and CLI help in German besides (`scripts/ci_gates.py` module docstring and `main`). House rule 1 in `AGENTS.md` keeps German in `scripts/` and `tests/` for translation pull requests of their own.

**Related context from the night run.** The handover `docs/journal/handover/2026-11-06-heartbeat-night.md` records open question Q-M1: a new script without a CI caller made implement runs fail in two lanes, with recommendation A being that the implement prompt should name "every new script needs a CI step or an OHNE_AUFRUFER entry with its reason". No file under `prompts/` mentions the rule today — the search for `caller` and `AUFRUFER`, case-insensitive, over `prompts/` returns nothing; this is a "not there" finding. Likewise `docs/WORKFLOW.md` carries no statement of the rule (same search there: nothing); the rule lives only in code and tests. The living spec `plans/specs/implementation-verification/spec.md` says nothing about the caller rule either (grep for `caller|AUFRUFER|script`: no match).

### Where it lives

- Rule and ratchets: `tests/test_ci.py` — `_scripts` (:2626), `_heimatlose_namen` (:2632), `test_every_script_has_a_caller_or_a_declared_reason` (:2646), the orphan-shell counter-test `test_the_glob_itself_finds_a_real_orphan_shell_script` (:2699, which creates a real `.sh` under `scripts/` and deletes it in `finally`), the age checks (:2730, :2936) with `_bead_status` (:2905) and the id patterns `_VORGANG`/`_KATALOG` (:2901-2902), the test ratchet (:2766-2829).
- Declaration lists: `scripts/ci_gates.py` — `OHNE_AUFRUFER` (:81-260, 37 entries), `OHNE_TEST` (:267, empty); `OHNE_MUTATIONSTEST` in `tests/test_ci.py` (:3039).
- Callers: `.github/workflows/ci.yml` (generated from `decisions/gates.yaml` by `--generate-ci`; drift guard `--check-ci`, function `check_ci` :739) and `scripts/verify_all.sh` (holds no gate list of its own; pinned by `test_runner_holds_no_command_list_of_its_own`, :1255, allowing only `ci_gates.py` and `verify_duration.py`).
- Kit interplay: `scripts/kit/probe.py` numbered expected-red ledger (:140-184); the ratchet-form note at `tests/test_kit.py` (:121).
- Historical origin of the rule and of its finding-11 widening (the `.sh` glob): recorded in the test docstrings and in the kit probe ledger, not in `docs/WORKFLOW.md`.

### What is unclear about it

- **The bead's exact intent is unreadable from this worktree.** The tracker is the Dolt database under `.beads/` and holds no rendered copy locally (house rule 2), and no journal or plan file names bead `coding-harness-8sxb` — the only occurrences in the whole tree are `plans/INDEX.md` (:122) and the research frontmatter itself. Whether `ci-caller-rule` means widening the rule, translating it, encoding it into the implement prompt, or something else is an open question for the interview, not a guess recorded here.
- **Four `.mjs` scripts sit outside the rule** (facts above). Whether the rule should see them, and whether their absence from `OHNE_AUFRUFER` is deliberate silence or a gap, is undecided — stated as an open question.
- **One neighbour diverges from today's tree.** `plans/changes/hermes-runner/plan.md` (:505) names an `OHNE_AUFRUFER["research_research_recheck"]` entry — precisely: `OHNE_AUFRUFER["research_recheck.py"]` — but no `scripts/research_recheck.py` exists (directory listing) and the dict holds no such key (read in full). When that changed is unclear; recorded as observed divergence, not resolved here.
- **Q-M1 links the rule to implement-lane failures**, and no prompt names the rule today (search named above). Whether this change owns that prompt wording is the bead's word.

### Which files a change would have to touch

- `tests/test_ci.py` — the decision (`_scripts`, `_heimatlose_namen`), the main test and its two counter-tests (`test_the_glob_itself_finds_a_real_orphan_shell_script`, `test_a_mere_mention_does_not_count_as_a_test` is the test-ratchet's analogue), and the two age checks.
- `scripts/ci_gates.py` — `OHNE_AUFRUFER` (and `OHNE_TEST` beside it), plus the module's German docstring/messages if language is part of the subject.
- `decisions/gates.yaml` and the regenerated `.github/workflows/ci.yml` — only if the answer for some script is a CI step; the derivation chain (`--generate-ci`, `--check-ci`) makes hand workflow edits fail `ci-drift` by design.
- `scripts/kit/probe.py` — the numbered expected-red ledger, whenever a `tests/test_ci.py` test of this rule is added, removed or renamed (the ledger's own comment shows the pattern).
- `scripts/verify_all.sh` — only if the wired side of the rule changes; the negative pin allows it exactly two script calls.
- `plans/changes/ci-caller-rule/research.md` frontmatter itself: whoever fills the file with a language model moves `provenance` to `ai-drafted-reviewed` with `produced_by:` and `review:` (the skeleton's own note; the class exists at `provenance.yaml` :40).

---

### Neighbours for the `neighbours:` header

```yaml
neighbours:
  - plans/specs/implementation-verification/spec.md
  - plans/changes/hermes-runner/spec.md
  - plans/changes/docs-job-report-header/spec.md
  - plans/changes/harness-decide-adr/spec.md
  - plans/changes/adr-owning-change/design.md
  - plans/changes/mutation-evidence-module/spec.md
  - plans/changes/swarm-time-limits/findings.md
  - plans/changes/beads-close-themselves/plan.md
  - plans/changes/criterion-test-ledger/spec.md
  - plans/changes/archive/2026-10-06-touch-map/spec.md
  - plans/changes/archive/2026-10-08-rb-g7-merge-freshness/spec.md
```

---

Note for the runner: the front matter of `research.md` still says `provenance: human-written`; per the skeleton's own note and `provenance.yaml` (class `ai-drafted-reviewed`), the runner should set the provenance block when appending this researched text. The stage-2 receipt line at the bottom of the file (dated 2026-11-07) is unaffected.
