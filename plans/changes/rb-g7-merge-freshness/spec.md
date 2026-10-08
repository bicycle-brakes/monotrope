---
title: "Spec — rb-g7-merge-freshness"
status: draft
implementation_status: none
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-34z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, governance, ruleset, ramp-valves, decision-pr]
class: feature
appetite: 1.5
change: rb-g7-merge-freshness
adr_question: {proposed: "no", reason: "it carries out the maintainer's answer of 2026-10-08 to rule RB-G7 with two tests and one ruleset setting, the upgrade tests/test_repo_settings.py already anticipates; the rule set's history entry records it, as 4.0.0 did for RB-M6, and a later rule-set version reverses it"}
---

# Spec — rb-g7-merge-freshness

After this change, what the check `verify` passed is the merge that happens:
the CI checks the pull request's merge ref, the branch ruleset requires a
branch to be up to date before it merges, and both are asserted from within
the repository, so the valve `merge-freshness` closes before its date (bead
coding-harness-34z). Research: [`research.md`](research.md), read at
`eae78a3`, with its spec-phase addendum. Decisions:
[`decisions.md`](decisions.md), the maintainer's answer of 2026-10-08
(option 2).

## Problem

- **The date turns everything red.** The valve `merge-freshness` (rule RB-G7)
  falls due on 2026-10-31; the gate `ramp-valves` blocks every local and
  hosted `verify` run from that day, and a due valve has no green state
  (research §1).
- **Nothing asserts the merge ref.** The CI checks out GitHub's merge ref on
  `pull_request` because no checkout carries a `ref:` (research §3 and its
  checkout addendum), but no test says so; a `ref:` added tomorrow passes
  every gate.
- **A green check can describe a merge that never happens.** The merge ref
  is computed when the CI runs. When `main` moves first, `verify` stays green
  for a merge against the older `main` — two open pull requests changing the
  same file both pass and both merge (decisions.md). The live ruleset does not
  require branches to be up to date: `strict_required_status_checks_policy`
  is `false` (research addendum, 2026-10-08).
- **The floor does not know the setting.** `tests/test_repo_settings.py`
  asserts five requirements; up-to-date branches are not among them, and its
  stubs leave the key out (research §4).

## Terms

- **Merge ref** — `refs/pull/<n>/merge`, the commit GitHub builds by merging
  a pull request's head into its base; `actions/checkout` checks it out on
  `pull_request` when its `with:` has no `ref:`.
- **Up-to-date requirement** — the ruleset option "Require branches to be up
  to date before merging": an active rule of type `required_status_checks`
  whose `parameters.strict_required_status_checks_policy` is `true` and whose
  list holds at least one check. GitHub aggregates the rules of every ruleset
  on a branch and applies the most restrictive version (research addendum).
- **The six requirements** — RB-M6's five (`tests/test_repo_settings.py`
  docstring) and the up-to-date requirement, which is RB-G7's. "No bypass"
  covers every ruleset that supplies any of the other five.
- **Gate `ruleset`** — `RULESET_ASSERT=1 python3 -m pytest
  tests/test_repo_settings.py -q -rs`, `placement: writer`: it runs in
  `make verify` on the maintainer's machine and never in hosted CI.
- **`<DAY>`** — the day phase 4 writes the texts.

## Acceptance criteria

Each criterion names what refutes it. "A stub" is an API answer a test
invents; no test and no agent changes anything at GitHub.

1. **The verification runs against the merge ref.**
   `tests/test_ci.py::test_the_verification_runs_against_the_merge_ref`
   exists and passes on the committed `.github/workflows/ci.yml` and on
   `ci_gates.generate_ci()`. For each it holds: `pull_request` is a trigger
   and carries no filter (`branches`, `branches-ignore`, `paths`,
   `paths-ignore`, `types`); there is no `pull_request_target`; the matrix job
   (`ci_gates.MATRIX_JOB`) names `pull_request` in its `if:`; it has an
   `actions/checkout` step before its first gate step; no `actions/checkout`
   step in any job has `ref` or `repository` under `with:`; no `run:` in any
   job calls `git checkout`, `git switch` or `git reset`.
   *Refuted by:* the test red on today's workflow, or criterion 2 failing.

2. **If the merge ref is given up, the check says so.** The test of
   criterion 1 rests on a function that returns findings, empty when the
   conditions hold. Each fault below, planted in a copy of today's parsed
   workflow, yields at least one finding: `ref:
   ${{ github.event.pull_request.head.sha }}` on the matrix job's checkout;
   `ref: ${{ github.head_ref }}` on the drift job's checkout; a `repository:`
   on a checkout; the `pull_request` trigger removed; it replaced by
   `pull_request_target`; a `branches:` filter on it; `pull_request` gone from
   the matrix job's `if:`; the matrix job's checkout removed; a step `run: git
   checkout ${{ github.head_ref }}` after the checkout. When the generator's
   checkout emits a `ref:` line, the function finds it in
   `ci_gates.generate_ci()`. No test name added to `tests/test_ci.py` matches
   `MUTATIONS_NAMEN` (research addendum).
   *Refuted by:* a planted fault with no finding, or
   `test_the_mutation_ratchet_only_turns_one_way` red.

3. **The floor asks for up-to-date branches.** `ruleset_findings` in
   `tests/test_repo_settings.py` returns a finding that begins `branches up to
   date before merging is not asked for` and names the ruleset option, unless
   some active `required_status_checks` rule with at least one check has
   `strict_required_status_checks_policy` exactly `true`. Each ruleset that
   supplies it is a supplying ruleset, so its bypass list must be empty.
   *Refuted by:* no such finding on a stub where the flag is `false` (the live
   value of 2026-10-08), missing, `null` or the string `"true"`, or `true` only
   on a rule without checks; or no bypass finding when only a second ruleset
   sets the flag and lets an actor bypass.

4. **What holds still holds.** The stubs `_todays_rules()` carry
   `strict_required_status_checks_policy: true` in the required-check rule,
   and their heading says they are the answers of 2026-10-05 plus the one key
   RB-G7 reads, set as the floor asks. On them `ruleset_findings` and
   `measure` return nothing; so they do when a second ruleset with an empty
   bypass list supplies the flag, and on a stricter ruleset.
   *Refuted by:* any finding on these stubs.

5. **Not measured is still not a pass.** If any call fails or answers in an
   unknown shape, `measure` returns exactly one finding that begins `not
   measured:` — every case of `test_an_unreachable_api_is_not_a_pass` and
   `test_a_hidden_bypass_list_is_not_a_pass` passes unchanged with the flag in
   the stubs. Of the existing tests only
   `test_the_ruleset_check_goes_red_when_a_rule_is_removed[required_status_checks]`
   changes what it expects: both findings, the required check and the
   up-to-date requirement, because the flag lives in that rule.
   *Refuted by:* an empty list or another finding for any unreachable case, or
   another existing assertion edited.

6. **While the live ruleset lacks it, the gate `ruleset` says so.** With
   `RULESET_ASSERT=1`, `test_master_has_a_ruleset_with_required_checks` fails
   while the live flag is `false`, listing exactly the up-to-date finding, and
   passes once the maintainer has ticked "Require branches to be up to date
   before merging". Hosted CI does not run it.
   *Refuted by:* the gate green while the live flag is `false`, red after the
   flag is set, or another finding on today's ruleset.

7. **The valve is closed, not dropped.** `merge-freshness` is gone from
   `REGEL_VENTILE`; a comment where it stood says it closed on `<DAY>`, that
   `tests/test_ci.py` and the gate `ruleset` hold RB-G7's merge clause, and
   rule set 5.0.0. No entry of `REGEL_VENTILE` is dated before 2026-11-30.
   *Refuted by:* `python3 scripts/ramp_valves.py --format=json` listing it or
   reporting a valve due, the comment missing, or an earlier date.

8. **The valve list test needs no closed valve.**
   `tests/test_ramp_valves.py::test_the_valve_list_is_not_empty` names no
   single valve: every key of `REGEL_VENTILE` is among `valves()`, and there
   are at least ten.
   *Refuted by:* the test green with `REGEL_VENTILE` emptied, or with
   `valves()` returning no rule valve.

9. **The rule says how it is held.** RB-G7's two sentences stand verbatim;
   two German sentences follow them in the same cell: the CI checks the pull
   request's merge ref, and the ruleset requires the branch to be up to date
   with its target before the merge; whether the ruleset requires it is
   measured only on the maintainer's machine (gate `ruleset`, `placement:
   writer`), as §3 asks of a level-4 row. Level 4 and P L I stay. The
   enforcers are the two named today plus
   `tests/test_ci.py::test_the_verification_runs_against_the_merge_ref` and
   `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks`;
   no `Ramp:`.
   *Refuted by:* `tests/test_regelwerk.py` red, a `Ramp:` left, either old
   sentence altered, or the writer sentence missing.

10. **Version and history.** `version: 5.0.0`, `updated: <DAY>`. A §7 entry
    `### 5.0.0 — <DAY>` stands above 4.0.0 with the four mandatory lines; it
    names the decision of 2026-10-08, why MAJOR, the closed valve, that the
    ruleset part is measured on the writer machine, and that LakeSwitch's
    ruleset already asks for up-to-date branches. Nothing else in the rule
    set changes.
    *Refuted by:* `tests/test_regelwerk.py` or the gate `frontmatter-current`
    red, or a diff outside the RB-G7 row, the two header keys and the entry.

11. **The machine-gate page says why the merge ref is the merged one.** In
    `docs/governance/quality-gates.md`, the paragraph below the machine-gate
    table gains German sentences: the ruleset requires the branch to be up to
    date before the merge (RB-G7), so the merge ref the CI checked is the one
    merged; when `main` moves, the pull request is updated and checked again.
    `updated:` moves; the rows MG-0 to MG-3 do not change.
    *Refuted by:* the sentence missing, a row changed, or
    `frontmatter-current` red.

12. **The merge procedure handles a branch that is behind.**
    `prompts/07-commit.md`, "The merge", gains a step: if GitHub refuses the
    merge because the branch is behind its base, the agent runs `gh pr
    update-branch <n>`, waits for CI green on the new head and starts again at
    step 2; if the update reports a conflict, it stops and says so.
    *Refuted by:* the step missing, or one that merges without a new
    restatement.

13. **Nothing else grows.** `.github/workflows/ci.yml`, `scripts/ci_gates.py`,
    `decisions/gates.yaml` and `scripts/kit/manifest.yaml` are byte-identical;
    `OHNE_MUTATIONSTEST`, `OHNE_AUFRUFER`, `OHNE_TEST`, `MAY_BE_WRITER_ONLY`,
    `REIST_NICHT` and `DECKEL` are unchanged; the gates `leerprobe` and
    `ci-drift` are green.
    *Refuted by:* a diff of any of them, or either gate red.

14. **On this repository.** Once the maintainer's ADR answer is recorded and
    the ruleset option is set, `make verify` on the maintainer's machine is
    green, the gate `ruleset` included. Before the option is set it is red on
    `ruleset` alone, with the one up-to-date finding; before the answer, on
    `adr-answers` too.
    *Refuted by:* any other block gate red.

## Non-goals

- **Any change at GitHub.** The maintainer ticks the option by hand (step in
  `plan.md`, "Phase 7"); agents only read the API.
- **A merge queue, auto-update of branches or auto-merge.** Each would take
  the update off the maintainer's hands; none was asked for.
- **A ruleset check in hosted CI** — the reason RB-M6 gave holds (research
  §4): the workflow token cannot see the bypass list.
- **RB-M6's row, MG-3's stale "Code-Owner-Review"** and
  `docs/architecture/target-architecture.md` — rb-m6-one-account left them for
  their own change.
- **LakeSwitch**: its ruleset already asks for up-to-date branches; its
  missing app pin is the 4.0.0 entry's.
- **Other valves, translating German text** (bead coding-harness-yim), **a new
  ADR**, **a rename** of the live test (it keeps RB-M6's name).
- **No `design.md`:** the change adds two assertions and texts, and moves no
  component, interface or boundary.

## Protected areas

- `.github/workflows/ci.yml`, `scripts/ci_gates.py`, `decisions/gates.yaml` —
  the merge ref already holds; the change asserts it and adds no gate.
- `docs/journal/` — append-only; its mentions of the valve are history.
- The rule set outside the RB-G7 row, the two header keys and the new entry.

## Definition of Done

- `verify` green, as criterion 14 states.
- Moved in the same pull request: `docs/governance/regelwerk.md`,
  `docs/governance/quality-gates.md`, `prompts/07-commit.md`,
  `plans/INDEX.md`.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes coding-harness-34z; its last commit carries
  `Closes-Bead: coding-harness-34z` (`prompts/07-commit.md`).
- Special runs: the planted faults of criterion 2 and the read-only live run
  of criterion 6, each with its commit in the pull request body.

## Open decisions

No `[DECISION]` is open: the maintainer's answer of 2026-10-08 settles what
RB-G7 asks for. The ADR question is proposed "no" in the header and waits for
the maintainer's answer, recorded with `python3 scripts/harness.py decide adr`
exactly as stated; until then `adr-answers` is red. Decided here, each
revisable:

- `[DETAIL]` **Class `feature`.** It changes how a rule is checked and carries
  a decision; `bounded` excludes "deciding anything new". RB-M6's close was a
  `feature` too.
- `[DETAIL]` **MAJOR, 5.0.0.** §4: MAJOR when a rule's meaning changes, MINOR
  only for a new rule, PATCH for wording or a test name. RB-G7's words stay,
  but it now demands of every repository it applies in (P L I) a ruleset
  setting it did not demand before; a PATCH would tell LakeSwitch there is
  nothing to check. No rule is added, so MINOR does not fit; the option the
  maintainer chose named "MINOR or MAJOR".
- `[DETAIL]` **Two sentences appended to RB-G7, its two kept.** §3, level 4,
  requires a row whose enforcer runs only on the writer machine to say so,
  and the live ruleset is that enforcer; naming only stub tests would claim a
  block no stub gives. "RB-G7 keeps its wording" was the answer against
  dropping the second sentence (option 3), not against a note on how it is
  held; RB-M6's row is the precedent.
- `[DETAIL]` **The sixth requirement lives in the existing measurement.** The
  live ruleset is already read in `tests/test_repo_settings.py` on the writer
  machine; a second reader would duplicate the calls and the "not measured"
  logic.
- `[DETAIL]` **The flag counts on any active required-check rule with a
  check**, not only on the one listing `verify`: GitHub applies the most
  restrictive version of aggregated rules. Only the boolean `true` counts; a
  missing key is "not asked for", red like "not measured".
- `[DETAIL]` **`_todays_rules` keeps its name** and carries the flag; the
  live value of 2026-10-08, `false`, is a case of the test of criterion 3.
- `[DETAIL]` **The merge-ref check reads both the committed file and the
  generator,** covers every job's checkout, and treats a `repository:` like a
  `ref:` — another repository is not the merge ref either.
- `[DETAIL]` **The agent updates a behind branch itself** while carrying out
  the maintainer's merge request: the update merges `main`, which is already
  merged, CI runs again, and the restatement and the ask rule still stand
  before the merge.
- `[DETAIL]` **The maintainer sets the option first, then merges.** A
  stricter ruleset holds today's five-item check, so setting it first keeps
  `make verify` green on `main`; merging first leaves it red on `ruleset` until
  set.
- `[DETAIL]` **German in the rule set and on the quality-gates page,** English
  in `prompts/07-commit.md` and the tests: each file keeps its language, and
  translating is bead coding-harness-yim.
- `[DETAIL]` **Appetite 1.5 h:** about 1 h of steps, the rest one repair round.
