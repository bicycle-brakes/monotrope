---
title: "Research — rb-g7-merge-freshness"
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
tags: [research, governance, ramp-valve, rb-g7]
---

# Research — rb-g7-merge-freshness

Phase 1 for bead coding-harness-34z: the ramp valve `merge-freshness`
(rule RB-G7, `scripts/ramp_valves.py`) falls due on 2026-10-31 and turns the
blocking ramp-valves gate red that day. Its predicate is that the test
`tests/test_ci.py::test_the_verification_runs_against_the_merge_ref` exists.

## Questions for exploration

1. What RB-G7 asks, in `docs/governance/regelwerk.md` (text, stage,
   enforcers) and wherever else the rule set or ADRs name it.
2. Which ref the CI verification checks out on `pull_request` and on `push`
   (`.github/workflows/ci.yml`, `actions/checkout` options), and whether any
   step checks out the branch head instead of GitHub's merge ref.
3. Whether the branch ruleset asserted by the gate `ruleset`
   (`tests/test_repo_settings.py`, the ruleset file it reads) requires the
   branch to be up to date before merging (strict status checks), and what
   the one-account change for RB-M6 (merged in #84, change folder
   `plans/changes/rb-m6-one-account/`) decided about the ruleset.
4. How RB-M6's valve was closed: which files moved (valve entry, rule set
   version and changelog, tests) — the precedent for closing RB-G7.

Stage-2 call, 2026-10-08: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 267 files, 630 commits, 12 rules.

## Runner exploration — 2026-10-08

Appended by GLM 5.3 Flash through `stage2.py explore` (Claude Code with
Z.ai); its German preamble addressed to the orchestrator was removed
(house rule 1), the facts below are unchanged.

## 1 · The rule and the valve (what exists today)

**RB-G7** (`docs/governance/regelwerk.md`, § 5, family "G — Gates (Maschine)", row `RB-G7`) reads, in German: „Eine leere Menge ist kein Ergebnis: jedes Gate behauptet seine Schlüsselmenge als nicht leer. Geprüft wird der Merge-Stand, nicht der Branch-Kopf." It stands at level (Stufe) 4, applies in P L I, and its enforcer column names three things: `tests/test_ramp_valves.py::test_the_valve_list_is_not_empty` · `tests/test_regelwerk.py::test_the_list_is_not_empty` · `Ramp:merge-freshness`. The rule has two clauses: non-vacuity (held by the two existing tests) and merge-state-not-branch-head — the part the valve covers.

**The valve** (`scripts/ramp_valves.py`, `REGEL_VENTILE["merge-freshness"]`) is the tuple ("RB-G7: the merge ref is checked, not the branch head", `tests/test_ci.py::test_the_verification_runs_against_the_merge_ref`, `2026-10-31`). `_regel_ventil` turns it into a `Ramp` (`scripts/_verdict.py`, class `Ramp`) with `target=Level.BLOCK`, `until_then=Level.INFO`, `deadline=date.fromisoformat("2026-10-31")`; the predicate is `_enforcer_exists`, a text search for `^def test_the_verification_runs_against_the_merge_ref(` in `tests/test_ci.py`. `Ramp.due` is true once the deadline is reached **or** the predicate holds; `ramp_valves.main` exits 1 when any valve is due (module docstring: "Exit codes: 0 = no valve due, 1 = at least one is due").

**The gate that runs it** is `ramp-valves` (`decisions/gates.yaml`): command `python3 scripts/ramp_valves.py`, `job: verify`, `enforcement: block`, `floor: false`, `placement: both`; its German reason calls a valve a dated promise whose deadline must turn the run red, locally and in hosted CI (D-10). In `.github/workflows/ci.yml` it is step `ramp-valves`, the last step of the `gates` job, carrying `if: ${{ !cancelled() }}` like every gate step.

**A due valve has no green state.** The designed close is written down in the sibling change: "the enforcer is written, the valve falls due, the rule is raised and the valve leaves the list" (`plans/changes/rb-m6-one-account/research.md` §1.3). That this was executed once is the `ruleset-assert` precedent (§4 below).

**The predicate does not exist today.** The name `test_the_verification_runs_against_the_merge_ref` appears in exactly three places: the valve entry (`scripts/ramp_valves.py`), the sibling research (§1.3) and this change's own `research.md`. `tests/test_ci.py` defines no such function — searched by name across the tree; the `_enforcer_exists` text search is exactly what the predicate measures, and it is false.

**Measured on 2026-10-06** (rb-m6-one-account, phase-6 findings, "Checked without a finding"): `python3 scripts/ramp_valves.py --format=json` listed 26 valves, none due; with the date forced, on 2026-10-30 none is due and on 2026-10-31 exactly `merge-freshness` falls due. No other valve shares the date — `REGEL_VENTILE` holds 2026-10-31 only here; every other entry is 2026-11-30 or 2026-12-31.

**The tests that hold the valve list in place:**
- `tests/test_ramp_valves.py::test_the_valve_list_is_not_empty` asserts `"merge-freshness" in namen` ("das Ventil aus RB-G7 fehlt — die Liste wurde geleert?") and `len(namen) >= 10`. A close that removes the valve without editing this test turns it red.
- `tests/test_regelwerk.py::test_every_named_ramp_exists_and_no_valve_is_orphaned` holds both directions: every `Ramp:<name>` named in the rule set must exist in `ramp_valves.valves()`, and every rule valve no rule names is orphaned — except `lint-*` and `provenance-review`, declared in the test. `Ramp:merge-freshness` must therefore leave the RB-G7 row in the same change that removes the valve entry.
- The level contract: `test_rules_at_level_three_or_higher_name_an_existing_enforcer` demands at least one existing non-`Ramp:` enforcer for a level-4 rule; RB-G7's two other named enforcers exist. `_enforcer_da` returns `True` for every `Ramp:`-prefixed reference — the column check does not verify valves.
- `tests/test_ci.py::test_every_step_after_a_failing_gate_still_runs` requires that some step runs `ramp_valves.py` (recognised by the command string, not the id) and that later steps carry `if:` — it concerns the script, not single valves.

## 2 · Where else the rule's content lives

- `docs/governance/quality-gates.md` §4: the machine-gate row **MG-2** ("PR-Verifikation | beim Pull Request | die eine Gate-Liste, gegen den Merge-Ref | `.github/workflows/ci.yml`") and the paragraph below it: „MG-2 prüft **`refs/pull/N/merge`**, nicht den Branch-Kopf. Lokal grün und in der CI rot ist deshalb kein Widerspruch, sondern der Normalfall: die CI baut, was nach dem Merge entsteht." This is the only `refs/pull` mention in the tree (searched).
- `docs/architecture/target-architecture.md`, decision-table row Q4: "The gate's mutation test goes red; a gate over an empty set is refused (RB-G4, RB-G7)" — cites RB-G7 for the non-vacuity clause.
- `docs/governance/regelwerk.md` §7, entry 2.0.0 (2026-09-19): the 2ee triage "re-showed" enforcers — „RB-G7 auf `tests/test_ramp_valves.py` und die Regel-Liste selbst" — and added `tests/test_ramp_valves.py` (RB-G7) plus the thirteen dated valves.
- `docs/research/2026-10-06-ponytail-skill.md` and `docs/research/2026-09-16-review-corpus-vs-running-workflow.md` cite RB-G7 as the non-vacuity rule.
- **ADRs: not there.** A search of `docs/adr/` for `RB-G7`, `merge.?freshness`, `Branch-Kopf`, `branch head` returns no match.
- **`docs/WORKFLOW.md`: no hit** for `RB-G7`, `merge-freshness` or `freshness` (searched tree-wide).
- The handovers queue the work: `docs/journal/handover/2026-10-06-night-work-hermes-forms-lock.md` („RB-G7 `merge-freshness` valve also falls due on 2026-10-31"; "Queue after that (one at a time): RB-G7 merge-freshness valve") and both 2026-10-07 handovers ("RB-G7 merge-freshness valve (coding-harness-34z), due 2026-10-31").

## 3 · What the CI checks out — and what no test asserts

- `.github/workflows/ci.yml` is generated (header: "GENERATED by `python3 scripts/ci_gates.py --generate-ci` from decisions/gates.yaml (D-10). Hand-edits fail the ci-drift gate on purpose."). Triggers: `push`, `pull_request`, `schedule`, `workflow_dispatch`; the `gates` job is limited to `push`/`pull_request` by its `if`. Both jobs check out with `actions/checkout@v4`; the `gates` job passes `fetch-depth: 0`, the `drift` job does not. The generator's `_checkout` (`scripts/ci_gates.py`) emits exactly these two forms — **neither carries a `ref:` input, and no other step checks anything out.** `fetch-depth: 0` is keyed to `needs_history` (declared by `frontmatter-current`; held by `tests/test_ci.py::test_a_gate_that_needs_history_gets_a_full_checkout_only_in_its_job`, bead qd7).
- The repository's own claim about the ref is MG-2's sentence above. What `actions/checkout@v4` presents on `pull_request` and on `push` without a `ref:` is the action's documented behaviour, which this session did not read — open question (§6).
- `tests/test_ci.py` asserts nothing about the checkout ref today: searches for `merge[-_]?ref`, `refs/pull` (tree-wide) and `checkout|fetch-depth` in that file find only the fetch-depth placement test and unrelated matches. The file's assertions over the generated workflow concern triggers, job ids, `needs`, `if` conditions and step inventory (`ci_gates.SUMMARY_JOB == "verify"`, the `always()` condition, exactly one job reporting the check `verify`, and so on).

## 4 · The ruleset floor and the RB-M6 precedent

**The asserted floor** (`tests/test_repo_settings.py`, module docstring "What RB-M6 asks"): (1) a pull request is required; (2) the check `verify` is required and pinned to GitHub Actions (`integration_id` 15368); (3) no force push; (4) no deletion; (5) every supplying ruleset shows an empty bypass list. A requirement that the branch be up to date before merging is **not among them**, and the module's stub answers — labelled "the live answers of 2026-10-05, only the keys read above" (`_todays_rules`) — hold exactly the four rule types, none a strict/up-to-date policy. `test_a_stricter_ruleset_still_holds` states "The five are a floor: asking for more is the upgrade the rule expects." Whether the live ruleset holds more than the five is not readable from this repository in this session — open question (§6).

**What RB-M6 decided** (`docs/governance/regelwerk.md` §7, entry 4.0.0 of 2026-10-06; `plans/changes/rb-m6-one-account/`, spec and findings): the rule now asks for exactly what one GitHub account can hold — the five — with the second approval returning when a second identity exists (ADR 0008's upgrade path); level 2 → 4; enforcers `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks` and `::test_an_unreachable_api_is_not_a_pass`; §3's level-4 row amended (a `placement: writer` gate blocks only the run on the maintainer's machine); `version:` 4.0.0 (MAJOR). The new gate `ruleset` (`decisions/gates.yaml`) runs `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs` with `job: verify`, `enforcement: block`, `floor: false`, `placement: writer`. `.github/workflows/ci.yml` stayed byte-identical. The change explicitly did **not** touch merge freshness: the spec names the valve a non-goal ("It falls due on the same day … No bead tracks it (research 1.3)"), and its phase-7 section asks the pull-request body to say "under 'after the merge' that the valve `merge-freshness` still falls due on 2026-10-31". The same findings already name bead `coding-harness-34z` for merge-freshness — the bead existed by 2026-10-06, while the sibling research of 2026-10-05 had found none. The PR number "#84" named in this change's questions was not confirmed by any file read in this session.

**How `ruleset-assert` was closed** (rb-m6 spec criterion 9, "closed, not dropped"; the tree today):
- the entry left `REGEL_VENTILE`; a comment stands where it was: `# "ruleset-assert" (RB-M6) closed on 2026-10-05: the gate ruleset asserts the branch ruleset (tests/test_repo_settings.py); rule set 4.0.0 records it.` (`scripts/ramp_valves.py`);
- `Ramp:ruleset-assert` left the RB-M6 row, replaced by the two real enforcers, with new wording and level;
- the rule set's `version:`/`updated:` moved and a §7 entry with the four mandatory lines (Geändert / Tests / Agents-Hooks-Templates / lakeswitch-ai) records the close; its `Tests:` line names the closed valve;
- the new enforcer file took the role `mechanismus` in `scripts/kit/manifest.yaml`;
- `docs/WORKFLOW.md`'s "Not all of it is here yet" note gained one sentence; `plans/INDEX.md` was regenerated.

§4 of the rule set fixes the semver for such an amendment: MAJOR = a rule removed or its meaning changed · MINOR = a new rule · PATCH = wording or test name (held by the rule-set tests named in rb-m6 research §1.1 — `test_version_is_semver_and_history_is_monotone`, `test_sync_impact_entry_exists_for_the_current_version` — not re-read in this session).

## 5 · Kit and registry facts

- `scripts/kit/manifest.yaml` lists as `mechanismus`: `scripts/ramp_valves.py`, `tests/test_regelwerk.py` („die konkreten Regeln sind Bestand, siehe REIST_NICHT"), `tests/test_ci.py` (listed; its reason line was not in the excerpt read), `tests/test_repo_settings.py` (bead bma), `docs/governance/regelwerk.md`, `ruff.toml` („ramp_valves.py liest die aktiven Regelgruppen daraus"). The rb-m6 research §1.7 adds: `tests/` otherwise falls to the catch-all `bestand`, and RB-G7 stands in `REIST_NICHT` with "braucht-ein-gate-das-hier-lebt" (that list not re-read here).
- `plans/specs/` holds only `.gitkeep` — no earlier artefact on this topic ("not there" after a listing). `plans/changes/rb-g7-merge-freshness/` holds only this `research.md` (untracked at session start). `plans/INDEX.md` is generated by `python3 scripts/plans_registry.py --index` and held by the gate `plans-registry` (ci.yml step; rb-m6 findings).

## 6 · What is unclear

- What `actions/checkout@v4` checks out on `pull_request` and on `push` without a `ref:` input: the action's documented default, not read in this session (no network or shell here). The repository's own wording is MG-2's `refs/pull/N/merge` sentence.
- Whether the live ruleset on GitHub holds more than the five asserted requirements (a strict up-to-date policy would be the ruleset-level home of "merge freshness"): not measurable from the repository; the stubs copy the 2026-10-05 answers, which carry no such rule; the live measurement runs only in the writer gate.
- Whether `tests/test_ramp_valves.py` asserted `ruleset-assert` before the RB-M6 close — git history was not readable in this session (no shell); the current file names only `merge-freshness`.
- What the predicate test `test_the_verification_runs_against_the_merge_ref` is expected to assert over the generated workflow: the valve's condition sentence and MG-2 are the only wordings in the tree; nothing sketches the test.
- Whether the RB-G7 row changes beyond its enforcer column when the valve closes: a rule-set amendment question for the spec phase; §4's semver names PATCH for "Wortlaut oder Testname" (fact of the rule, not a recommendation).
- The bead `coding-harness-34z` is named in this artefact's frontmatter, in the rb-m6 findings and in both 2026-10-07 handovers; the tracker itself was not read in this session (this sub-agent has no `tools/bd` access).

## 7 · Files a change would have to touch

Named by the facts above and the RB-M6 close precedent:
- `tests/test_ci.py` — the predicate test the valve names; it does not exist today.
- `scripts/ramp_valves.py` — the `merge-freshness` entry out, a dated close comment in (form per the `ruleset-assert` comment).
- `docs/governance/regelwerk.md` — the RB-G7 row's enforcer column (`Ramp:merge-freshness` out), `version:`, `updated:`, a §7 entry with the four mandatory lines.
- `tests/test_ramp_valves.py` — the `"merge-freshness" in namen` assertion.
- `plans/INDEX.md` — regenerated.
- `decisions/gates.yaml` and `.github/workflows/ci.yml` — only if the change adds a gate of its own; the valve's predicate lives in the existing floor suite (the `pytest` step runs `tests/` whole), and the RB-M6 change left `ci.yml` byte-identical. `ci.yml` is generated; `ci-drift` holds it to the generator.
- `scripts/kit/manifest.yaml` — only if the change adds a file of its own; a new test inside `tests/test_ci.py` needs no new row, the file is already listed.

## Orchestrator addendum — the checkout default, 2026-10-08

Read on 2026-10-08 in the `actions/checkout` v4 README
(`https://raw.githubusercontent.com/actions/checkout/v4/README.md`): `ref`
"defaults to the reference or SHA for that event", and the README carries a
scenario "Checkout pull request HEAD commit instead of merge commit" — so on
`pull_request` the default is GitHub's merge commit (`refs/pull/N/merge`),
which is what MG-2 claims; on `push` it is the pushed commit. The generator
emits no `ref:` (§3), so the first clause of RB-G7's second sentence holds
today; no test says so.

What the merge ref does not give: it is computed when CI runs. If `main`
moves before the merge, the green check describes a merge that will not
happen. Only a ruleset rule "require branches to be up to date before
merging" (strict status checks) closes that gap; the asserted floor does not
contain it (§4), and whether the live ruleset does is not measured here.

## Addendum — spec phase, 2026-10-08

Gaps the spec needed, closed by reading (worktree at `eae78a3`; GitHub API
with the maintainer's `gh` login, GET only; GitHub documentation read as text).

- **The live ruleset lacks the up-to-date requirement.** `gh api
  'repos/{owner}/{repo}/rules/branches/main'` (2026-10-08): the
  `required_status_checks` rule of ruleset `24528176` carries
  `parameters: {strict_required_status_checks_policy: false,
  do_not_enforce_on_create: false, required_status_checks: [{context: verify,
  integration_id: 15368}]}`. The key sits in the same `parameters` object
  `tests/test_repo_settings.py` already reads `required_status_checks` from;
  `rulesets/24528176` shows the same rule. Answers §6, second bullet.
- **What the key means** (REST "Repository rules"):
  `strict_required_status_checks_policy` — "Whether pull requests targeting a
  matching branch must be tested with the latest code. This setting will not
  take effect unless at least one status check is enabled." In the web form
  it is the checkbox "Require branches to be up to date before merging" under
  "Require status checks to pass" ("Available rules for rulesets"). Rules of
  several rulesets on one branch are aggregated, and "the most restrictive
  version of the rule applies" ("About rulesets"). A ruleset is edited under
  Settings → Rules → Rulesets → its name → "Save changes".
- **LakeSwitch already asks for it.** Ruleset `22305982` of
  `MPAdesso/lakeswitch-ai` (2026-10-08): `strict_required_status_checks_policy:
  true`, checks `verify` and `floor`, neither pinned to an app. Its workflows
  `verify.yml` and `floor.yml` check out with `actions/checkout@v4` and no
  `ref:` (local clone at `471df3f`, 2026-09-30, not fetched).
- **The provenance map is `provenance.yaml` at the root**, not under
  `decisions/`: `docs/governance/regelwerk.md` and
  `docs/governance/quality-gates.md` are `allowed: [human-decided]`,
  `frontmatter: required`; `prompts/` is `human-written`, no header.
- **A mutation-test name in `tests/test_ci.py` is a trap.** That file names
  `plans_registry.py`, and `test_the_mutation_ratchet_only_turns_one_way`
  counts any `MUTATIONS_NAMEN` match in a file that mentions a script as
  evidence for that script's gate; `plans-registry` stands in
  `OHNE_MUTATIONSTEST`, so such a name turns the ratchet red. No test in the
  file matches today; `MAY_BE_WRITER_ONLY`'s comment names the trap
  (rb-m6-one-account, D8).
- **The kit probe has no room.** `REIST_NICHT` holds 33 entries and `DECKEL`
  is 33. `tests/test_ci.py`, `tests/test_repo_settings.py`, `decisions/`,
  `.github/workflows/ci.yml`, `scripts/ci_gates.py` and
  `scripts/ramp_valves.py` travel as `mechanismus`; `tests/test_ramp_valves.py`
  does not (catch-all `bestand`), which is why
  `test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G7]` is red
  in the probe and listed.
- **The valve falls due the moment its test exists.** `_enforcer_exists` is a
  text search; once `tests/test_ci.py` defines the function, `ramp_valves.py`
  exits 1 until the entry leaves `REGEL_VENTILE`, and `test_regelwerk.py`
  needs `Ramp:merge-freshness` out of the RB-G7 row in the same commit.
- **The merge flow is written in `prompts/07-commit.md`**, "The merge" (six
  steps); it has no step for a branch that is behind. `docs/WORKFLOW.md`
  points there and states no merge mechanics itself. `.claude/settings.json`
  asks before `gh pr merge`, not before `gh pr update-branch` (gh 2.101.0
  has the command; default: a merge commit from the base).
- **`plans/INDEX.md` lists every artefact file**, so a new `spec.md` or
  `plan.md` needs `python3 scripts/plans_registry.py --index`.
- **Baseline:** `make verify` at `eae78a3` green (pytest 1125 passed,
  16 skipped; gate `ruleset` 82 passed against the live ruleset);
  `ramp_valves.py --format=json` 26 valves, none due.
