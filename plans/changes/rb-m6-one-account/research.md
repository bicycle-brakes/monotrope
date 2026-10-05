---
title: "Research — rb-m6-one-account"
status: draft
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-bma
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, governance, ruleset, ramp-valves]
---

# rb-m6-one-account — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). Read on
2026-10-05 in the worktree at `d5813ec` (`origin/main`), the GitHub API with
the maintainer's `gh` login, the sibling clones `portfolio-agentic-engineering`
(`20a279c`) and `lakeswitch-ai` (`09c9d62`), and the GitHub REST documentation
(fetched as text from docs.github.com). No search in `plans/specs/` or
`plans/changes/` found an earlier artefact on this rule; this folder is the
first.

## 1 · What exists today

### 1.1 The rule

- **RB-M6** (`docs/governance/regelwerk.md`, §5, family M, row `RB-M6`),
  German: "Die Branch-Regeln werden aus dem Repository heraus behauptet:
  geforderte Prüfungen gleich der Gate-Liste, Code-Owner-Review an, Zustimmung
  nicht vom letzten Pusher. Eine unerreichbare Verwaltungs-Schnittstelle ist
  BLOCK, nicht grün". Level 2; enforcer column
  `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks`
  · `Ramp:ruleset-assert`; applies in P L I.
- The rule set is `version: 3.0.0`, `updated: 2026-09-30`,
  `provenance: human-decided` (its frontmatter; `provenance.yaml`, entry
  `docs/governance/regelwerk.md`, `allowed: [human-decided]`,
  `frontmatter: required`).
- **Its own change rule** (§4 "SYNC IMPACT"): every change raises `version:`
  and adds a history entry in §7 with exactly four lines — `Geändert:`,
  `Tests:`, `Agents/Hooks/Templates:`, `lakeswitch-ai:`. Semver: MAJOR = a rule
  removed or its meaning changed · MINOR = a new rule · PATCH = wording or test
  name. Held by `tests/test_regelwerk.py::test_version_is_semver_and_history_is_monotone`
  and `::test_sync_impact_entry_exists_for_the_current_version`.
- **The level contract** (`tests/test_regelwerk.py`): a rule at level 3 or
  higher names an enforcer that exists (`::test_rules_at_level_three_or_higher_name_an_existing_enforcer`);
  below 3 it names a `Ramp:` with a deadline
  (`::test_rules_without_an_enforcer_are_at_most_level_two_and_carry_a_dated_ramp`);
  every named valve exists in `scripts/ramp_valves.py` and no rule valve is
  unnamed (`::test_every_named_ramp_exists_and_no_valve_is_orphaned`). Level 4
  rules may still name a valve for an unenforced part (RB-M1, RB-G7 do).
- **Level 4** in §3 reads "CI blockierend — der Lauf schlägt fehl (BLOCK);
  ohne Fix kein Merge"; level 3 "CI berichtend … (DRIFT)".
- **RB-G2** (same table) sets the gate level by mobility: when the other side
  of a check lies outside the repository, the form is "DRIFT mit Timer". It is
  itself at level 2 (`Ramp:fehler-katalog-transfer`).

### 1.2 The enforcer the rule names does not exist here

- `tests/` holds no `test_repo_settings.py` (listing at `d5813ec`), and
  `git log --all -- tests/test_repo_settings.py` returns nothing.
- `docs/WORKFLOW.md`, the note "Not all of it is here yet", lists
  `tests/test_repo_settings.py` among the pieces **not** in this repository
  (checked 2026-09-29 at `9f14283`). Its §3 (paragraph "No container belongs
  to it") says that file holds a container fence — a target, by that note.
  The archived spec `plans/changes/archive/2026-09-29-omnigent-deny-layers/spec.md`
  chose another file name for that reason.
- The origin repository has the file
  (`portfolio-agentic-engineering/tests/test_repo_settings.py`, last changed in
  `8ce7572`): a pure function `pruefe_rulesets` (bypass actors, rules
  `pull_request`, `required_status_checks`, `non_fast_forward`, context
  `verify`), a live test `test_master_has_a_ruleset_that_actually_binds`,
  five mutation tests, the container fence and CODEOWNERS checks. Its CI runs
  the file nightly (`.github/workflows/ci.yml`, step `ruleset-drift`, with
  `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}`). Two properties of that test matter
  here:
  - it reads `r.get("bypass_actors")`, so a **missing** key reads as "no
    bypass" (see 1.6 for when GitHub leaves it out);
  - it is **skipped** when `gh` is absent or logged out, and pytest exits 0 —
    green without having looked, against RB-M6's last sentence.

### 1.3 The valve and its date

- `scripts/ramp_valves.py`, `REGEL_VENTILE["ruleset-assert"]`:
  ("RB-M6: the branch ruleset is asserted from within the repo",
  `tests/test_repo_settings.py::test_the_ruleset_assertion_runs_in_ci`,
  `2026-10-31`). The predicate names a different function than the rule's
  enforcer column.
- `_regel_ventil` builds a `Ramp` (`scripts/_verdict.py`) with target BLOCK
  and a deadline. `Ramp.due` is true once the predicate holds **or** the date
  is reached; `ramp_valves.main` exits 1 when any valve is due.
- **There is no green state for a due valve.** The designed close is in the
  comment above `_enforcer_exists` and in the rule set's 1.0.0 history entry:
  the enforcer is written, the valve falls due, the rule is raised and the
  valve leaves the list.
- The gate `ramp-valves` (`decisions/gates.yaml`) is `job: verify`,
  `enforcement: block`, `placement: both`: from 2026-10-31 every local
  `make verify` and every hosted `verify` run is red.
- **A second valve falls due the same day:** `merge-freshness` (RB-G7,
  `tests/test_ci.py::test_the_verification_runs_against_the_merge_ref`,
  `2026-10-31`). `tools/bd search` for "merge-freshness", "merge ref",
  "valve", "RB-G7" and "freshness" finds no bead for it (2026-10-05); the one
  hit for "valve" is this change's bead.
- Two other valves expect functions **in the same file**: `commit-identity`
  (RB-P4, `::test_recent_commits_carry_a_real_identity_and_trailers`,
  2026-11-30) and `codeowners-here` (RB-M7,
  `::test_codeowners_covers_every_human_decided_path`, 2026-11-30). Defining
  either name makes its valve due at once.
- `python3 scripts/ramp_valves.py` on 2026-10-05: 27 open valves, none due.

### 1.4 The live ruleset (GitHub API, 2026-10-05, read only)

- `repos/MPAdesso/coding-harness`: private, owner type `User`, default branch
  `main`; the maintainer's token has `admin`.
- `rulesets`: one, id `24528176`, name `main`, created
  2026-10-05T22:05:09+02:00.
- `rulesets/24528176`: `target: branch`, `enforcement: active`,
  `conditions.ref_name.include: ["~DEFAULT_BRANCH"]`, `bypass_actors: []`,
  `current_user_can_bypass: never`; rules `deletion`, `non_fast_forward`,
  `pull_request` (`required_approving_review_count: 0`,
  `require_code_owner_review: false`, `require_last_push_approval: false`),
  `required_status_checks` (`[{context: verify, integration_id: 15368}]`).
- `rules/branches/main` returns the same four rules, each with
  `ruleset_id: 24528176`.
- `gh api 'repos/{owner}/{repo}/…'` resolves the placeholders from this
  worktree's single remote `origin` (gh 2.101.0).

### 1.5 Where the required check comes from

- `.github/workflows/ci.yml` is generated (`scripts/ci_gates.py`,
  `generate_ci`) from `decisions/gates.yaml` and held to it by the gate
  `ci-drift`. Its job `verify` has no `name:`, so its check context is
  `verify`; it runs every `job: verify` gate measured in CI. The required
  check `verify` therefore stands for the whole verify gate list.
- No step gets a token: `_schritt` writes no `env:`, and the workflow has no
  `permissions:` block.
- **Placement** (`decisions/gates.yaml` header; `ci_gates.PLACEMENT`,
  `misst_in`): `writer` = measured only on a writer machine; the generated
  workflow leaves such a gate out, the local runner (`scripts/verify_all.sh`,
  placement `lokal`) runs it. No gate uses `writer` today;
  `tests/test_gate_machinery.py::test_the_generated_workflow_leaves_writer_only_gates_out`
  holds the rule. The runner replaces the first `python3` of a command with its
  interpreter and runs it through `sh -c`.

### 1.6 What a token can see (GitHub REST documentation, 2026-10-05)

- "Get a repository ruleset": "To prevent leaking sensitive information, the
  bypass_actors property is only returned if the user making the API request
  has write access to the ruleset."
- Fine-grained permissions: `GET …/rulesets`, `GET …/rulesets/{id}` and
  `GET …/rules/branches/{branch}` need **Metadata: read**; creating, updating
  and deleting rulesets need **Administration: write**.
- The `permissions` list of the workflow syntax has no `administration`
  scope, so the workflow token can read the rules but not the bypass list.
  Documented, **not measured** in a hosted run.
- "Get rules for a branch" returns only active rules, from every level;
  rules of rulesets in `evaluate` or `disabled` are not returned.

### 1.7 Mutation evidence and the kit

- `tests/test_ci.py`: a gate whose command runs a test file has its mutation
  evidence in that file (`_pruefling`, `test_every_gate_step_has_a_mutation_test`):
  a function name matching `MUTATIONS_NAMEN` (`goes_red`, `is_not_a_pass`, …).
  `OHNE_MUTATIONSTEST` may only shrink.
- `scripts/kit/manifest.yaml`: `tests/` falls to the catch-all `bestand`;
  `tests/test_regelwerk.py`, `docs/governance/regelwerk.md` and `decisions/`
  are `mechanismus`. `scripts/kit/probe.py` copies the `mechanismus` files and
  runs pytest there; every red case must stand in `REIST_NICHT`, whose cap
  only sinks. RB-G7, RB-P5 and RB-S1 stand there with
  "braucht-ein-gate-das-hier-lebt". A rule raised to level 3+ with its
  enforcer in a `bestand` file adds such a red case.

### 1.8 How the rule set was amended before

- **Pull request #55** (merged 2026-09-30): title "decide(governance): RB-M2
  approval is the merge when one person holds every role", label `decision`,
  body from the decision template, one file (`docs/governance/regelwerk.md`,
  +23 −3): the RB-M2 row amended in German in place, `version: 3.0.0` (MAJOR),
  a four-line history entry. No ADR and no change folder of its own; the
  wording was proposed in `plans/changes/harness-decide-adr/plan.md`.
- It rested on **ADR 0008** (`docs/adr/0008-merge-confirms-a-decision.md`):
  "Agents act under the maintainer's GitHub account"; GitHub lets no author
  approve their own pull request; option (c), "a bot identity for agents …
  branch protection requires an approval by someone other than the pusher",
  is named as "the upgrade path, not now".
- RB-M2's exception names its own end in words: "endet, sobald Agenten unter
  eigener Identität arbeiten". No file declares agent identities; no bead
  tracks a second identity (`tools/bd search` "identity", "GitHub App",
  2026-10-05).
- Decision pull requests: `AGENTS.md` house rule 8, `prompts/07-commit.md`,
  `.github/PULL_REQUEST_TEMPLATE/decision.md`. Pull request #54 carried three
  ADR answers in the multi-decision form.

### 1.9 Change class and the ADR question

- `docs/WORKFLOW.md`, "Change classes, the ADR question and decision pull
  requests": `bounded` changes a flow "without deciding anything new";
  `feature` "changes what the system must do or how it is checked" and owes
  the maintainer's answer, written by `python3 scripts/harness.py decide adr`
  to `decisions/answers/<change>/adr.yaml`; the gate `adr-answers`
  (`scripts/check_adr_answers.py`) holds every feature to that file.
- Precedents: `frontmatter-current` (one more check, one gate entry) was a
  `feature`, answered "no"; `research-currency` (a report that turns nothing
  red) was `bounded`.
- "D-13" in this repository is the stage-2 entry criteria
  (`docs/architecture/target-architecture.md`, decision table); in
  `lakeswitch-ai` it is another decision. Neither defines change classes.

### 1.10 Other texts that state RB-M6's old content

- `docs/governance/quality-gates.md` (human-decided), row MG-3: "Merge … Required
  Checks, Code-Owner-Review … GitHub-Ruleset".
- `docs/architecture/target-architecture.md`, rows T0 and T1: valves RB-M2 and
  RB-M6 close with the first collaborator.

### 1.11 LakeSwitch

- Ruleset `22305982` "lakeswitch floor" (read 2026-10-05): `deletion`,
  `pull_request` (0 approvals), `required_status_checks` (`verify`, `floor`),
  `non_fast_forward`, `bypass_actors: []`.
- The local clone at `09c9d62` has no `docs/reference/rules.md` (the rule
  set's `lakeswitch_ref`) and no mention of RB-M6.

### 1.12 Gates the artefacts and docs meet

- `plans/INDEX.md` is generated (`python3 scripts/plans_registry.py --index`);
  a stale index is BLOCK in `plans-registry`.
- `frontmatter-current` holds `updated:` current in every file whose
  `provenance.yaml` entry says `frontmatter: required` — here
  `docs/governance/regelwerk.md`, `docs/WORKFLOW.md` and `plans/`.
- `dangling-beads` resolves every `coding-harness-<id>` cited in Markdown.
- The change-artefact validator the phase prompts name
  (`scripts/validate_change_artefacts.py`) is not in this repository
  (`scripts/` listing; `docs/WORKFLOW.md` note).

## 2 · What is unclear

- How `gh` resolves `{owner}/{repo}` non-interactively when a clone has
  several remotes: not verified (this clone has one).
- What the workflow token actually receives from the ruleset endpoints in a
  hosted run: documented (1.6), not measured.
- Rulesets at organisation level: none can apply (user-owned repository); how
  the repository endpoint answers for one: not read.

## 3 · Which files a change would touch

- `docs/governance/regelwerk.md` — the RB-M6 row, `version:`, `updated:`, a §7
  entry.
- `tests/test_repo_settings.py` — new.
- `decisions/gates.yaml` — a gate that runs it.
- `scripts/ramp_valves.py` — the `ruleset-assert` entry.
- `scripts/kit/manifest.yaml` — the new test's role.
- `docs/WORKFLOW.md` — the "Not all of it is here yet" note.
- `decisions/answers/rb-m6-one-account/adr.yaml` — only if the change is a
  `feature`, and only as the maintainer answers.
- `plans/INDEX.md` — regenerated.
- `.github/workflows/ci.yml` — must stay as generated; a `writer` gate leaves
  it unchanged.
