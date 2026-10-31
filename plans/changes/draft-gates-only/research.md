---
title: "Research — draft-gates-only"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-77qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: pi, version: "GLM 5.3 Flash, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# draft gates only — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2822 commits, 12 rules.

## Runner exploration — 2026-10-31

Research complete. Here is the prose ready to append to `plans/changes/draft-gates-only/research.md`.

---

**Suggested `neighbours:` header list**

`plans/specs/implementation-verification/spec.md` · `plans/changes/verify-stages-new-files/spec.md` · `plans/changes/verify-machine-lock/` · `plans/changes/fail-fast-attempts/` · `plans/changes/codex-drafts/` · `plans/changes/venv-pycache/` · `plans/changes/interview-context/` · `plans/changes/run-report/`

---

## What exists today

**The `docs` subset mechanism is merged and tested; the draft verb does not use it yet.** The one gate list (`decisions/gates.yaml`, "THE ONE LIST", D-10/O-4, bead coding-harness-bo0) carries a `subsets` schema key whose only declared value is `docs` (`decisions/gates.yaml:39-44`; `SUBSETS` in `scripts/ci_gates.py:44-46`). Its comment describes `docs` as "the document gates the draft verb runs after writing spec, design and plan (`verify_all.sh --job docs`) instead of the whole verify job; it adds no CI job and drops no gate from `verify` (bead coding-harness-77qj)" — the bead of this very change. Eleven verify gates declare `subsets: [docs]`: `plans-registry`, `docs-links`, `frontmatter-current`, `dangling-beads`, `decision-continuity`, `adr-answers`, `interview-minimums`, `question-context`, `criterion-ledger`, `research-handoff`, `markdownlint` (the `subsets: [docs]` entries in `decisions/gates.yaml:93-255`). Nine of them are `block`, two are `report` (`docs-links`, `markdownlint`). Outside the subset stay `pytest`, `ruff-check`, `ruff-format`, `leerprobe`, `bead-export`, `gate-schema`, `ci-drift`, `ramp-valves`, `ruleset` and the drift/advisory gates; `tests/test_ci.py` pins this exact membership in `DOCS_SUBSET` and asserts no code gate is in it (`tests/test_ci.py:372-400`, "77qj" in the docstrings).

**The local runner already accepts the subset.** `scripts/verify_all.sh` parses `--job` with the value `docs` (`verify_all.sh:74-83`) and passes it to `ci_gates.py --commands --job "$JOB"` (`verify_all.sh:116-120`); `in_job()` in `scripts/ci_gates.py:381-385` selects verify gates that name the subset, and the `--job` choices include the subsets (`ci_gates.py:748`). The schema refuses subsets on drift gates and derives no CI job from one (`ci_gates.py:354-361`; test `test_the_docs_subset_derives_no_ci_job`, `tests/test_ci.py:403-407`). `verify_all.sh` still takes the machine-wide admission first and re-enters directly when an ancestor holds the marker (`verify_all.sh:89-100`), so a nested runner call from the stage-2 runner keeps the one-admission shape that `verify-machine-lock` built (bead coding-harness-p6mu).

**The draft verb today verifies with the full verify job.** `verify_draft` (`scripts/stage2.py:7453-7520`) runs the derived-file preparation (`prepare_derived`, `scripts/stage2.py:7484`), holds the admission under the label `["make", "verify"]` (`scripts/stage2.py:7490`), and launches `["make", "verify"]` with the shared step limit `VERIFY_SECONDS = 30 * 60` (`scripts/stage2.py:3854`, used at `scripts/stage2.py:7496`). That is the same command `verify_attempt` runs for implement and repair (`scripts/stage2.py:5419`) — `make verify` resolves to the runner over the whole verify job (`Makefile:18-19`). The draft's one tolerance travels through `check_adr_answers.TOLERATE_ENV`, set by `verify_draft` itself (`scripts/stage2.py:7476-7479`); the gate it tolerates, `adr-answers`, is inside the docs subset (`decisions/gates.yaml:157-164`), so the tolerance lands inside a docs-only run. Nothing in `scripts/` launches `verify_all.sh` with `--job docs` today — a search over every `verify_all.sh` reference under `scripts/` found only the runner itself, its lock helper and stage-2's log-frame readers (`scripts/stage2.py:4677-4875`): the caller the gate file's comment speaks of is *not there*.

**The decision's provenance sits in three places, none of them a change folder.** The night-run plan of 2026-10-29 names "the decision PRs #280 (a `docs` gate job, bead coding-harness-77qj)" as waiting on the maintainer (`docs/research/2026-10-29-night-run-plan.md:41-43`); the merged artifacts (gate file, runner, generator, tests) now carry the mechanism, and the runner's usage line already calls `--job docs` "the draft verb, bead coding-harness-77qj" (`scripts/verify_all.sh:12`). No archived change folder mentions 77qj, `subsets` or `--job docs` (grep over `plans/changes/archive/` — no matches), and the doctrine has not been updated: "The draft (phases 2, 2b and 3)" still says "`make verify` runs after the put-back" and "the exit code of `make verify` decides" (`docs/WORKFLOW.md:1215-1221`). The same handover that recorded the decision process also recorded the motivation: "**The draft verb runs `make verify`.** It bears a verify, so two drafts and a kit probe once overlapped; memory held at 33 % free." (`docs/journal/handover/2026-10-29-three-lane-night.md:187-188`) — the machine-load reason for a lighter draft verification, matching the admission work of bead coding-harness-p6mu. Local evidence that the subset's tracker-reading gates run green on a writer machine exists: the full local verify runs recorded green on 2026-10-28/29 include the two `needs_tracker` subset gates (`docs/journal/handover/2026-10-29-three-lane-night.md:178-184`).

**CI side there is nothing draft-specific.** The generated workflow derives only the verify matrix job and the drift job (`generate_ci`, `scripts/ci_gates.py:640-716`); a search for "draft" over `.github/workflows/` finds no matches, so no GitHub-draft-pull-request filtering exists anywhere — the change name's scope is the draft verb's local post-run check, as every in-repo 77qj reference says.

**One report asymmetry, stated as a fact.** The runner's report header is produced by `ci_gates.py --report` without a `--job` argument (`scripts/verify_all.sh:104`), and `report()` counts the gates of its job argument, which defaults to `verify` (`scripts/ci_gates.py:479-490`, `748`). Under a `--job docs` run the printed report would therefore still name the verify job's gate count.

## Where it lives

- Gate list and subset declarations: `decisions/gates.yaml` (schema key `subsets`, `decisions/gates.yaml:39-44`; the eleven `subsets: [docs]` gates across `decisions/gates.yaml:93-255`).
- Selection logic and generator: `scripts/ci_gates.py` (`SUBSETS` at `ci_gates.py:44-46`, `in_job` at `ci_gates.py:381-385`, `--job` choices at `ci_gates.py:748`, subset schema rules at `ci_gates.py:354-361`).
- Local runner: `scripts/verify_all.sh` (`--job` parse at `verify_all.sh:74-83`, usage line naming the draft verb at `verify_all.sh:12`, gate-list fetch at `verify_all.sh:116-120`, admission nesting at `verify_all.sh:89-100`, report line at `verify_all.sh:104`).
- The draft verb and its verification: `verify_draft`, `scripts/stage2.py:7453-7520`; the draft entry `draft()`, `scripts/stage2.py:7523`; the shared limit `VERIFY_SECONDS`, `scripts/stage2.py:3854`; implement's counterpart `verify_attempt` launch, `scripts/stage2.py:5419`.
- Doctrine: `docs/WORKFLOW.md:1203-1251` ("The draft (phases 2, 2b and 3)"), still naming `make verify`.
- Prompts: `DRAFT_PROMPTS = ("02-spec.md", "02b-design.md", "03-plan.md")` (`scripts/stage2.py:213`). A grep for `verify` over `prompts/*.md` finds no hit in `02-spec.md` or `02b-design.md`; `prompts/03-plan.md:104` says a plan without criterion test forms turns "`make verify` red" — through the gate `criterion-ledger` (`decisions/gates.yaml:186-194`), which is in the docs subset, so that sentence stays true under a docs-only run.
- Subset tests: `tests/test_ci.py:372-427` (`DOCS_SUBSET`, `test_the_docs_subset_holds_the_document_gates_and_no_code_gate`, `test_the_docs_subset_derives_no_ci_job`, `test_the_schema_rejects_a_malformed_subset`).
- Draft-path tests that pin the current command: `test_a_red_verify_fails_the_draft_attempt` (`tests/test_stage2.py:3669`), `test_only_the_changes_own_missing_adr_answer_is_tolerated` (`tests/test_stage2.py:3697`), `test_a_make_that_cannot_start_fails_the_attempt_and_moves_the_chain` (`tests/test_stage2.py:3882`), `test_a_passing_draft_makes_one_commit_and_leaves_a_clean_tree` (`tests/test_stage2.py:4007`), `test_three_failed_draft_attempts_exit_1_without_a_commit` (`tests/test_stage2.py:4146`), and `test_the_runner_steps_carry_their_limits_at_the_call_sites` (`tests/test_stage2.py:5599`, asserting the `("make", stage2.VERIFY_SECONDS)` pair at `tests/test_stage2.py:5627`). Five tests call `verify_draft` directly (`tests/test_stage2.py:2142`, `5759`, `6034`, `6085`, `6180` — the tool-state and venv-cache refusals).
- Makefile: `verify` is the only runner target (`Makefile:16-19`); `tests/test_ci.py` pins Makefile and gate list together (`Makefile:4-5`).

## What is unclear

- The invocation path of the draft verb's lighter check is not fixed in any artifact I read: the gate file names `verify_all.sh --job docs` (`decisions/gates.yaml:41-43`), but whether the runner calls the script directly or through a new make target is stated nowhere (not found — the Makefile has no docs target, and no stage-2 code passes `--job`).
- Whether the draft's step limit stays the shared `VERIFY_SECONDS` or becomes its own, shorter bound is not stated anywhere (not found).
- Whether the report asymmetry above (`--report` without `--job` under a docs run, `verify_all.sh:104` + `ci_gates.py:748`) is meant to be addressed by this change is open (not found).
- Whether the docs subset *membership* is in scope here at all: every merged artifact presents it as decided (the subsets schema comment and tests), and I found no statement that membership changes in this change. The one needs_tracker block gate outside the subset is `bead-export` (`decisions/gates.yaml:125-133`); nothing read explains or revisits that exclusion in this change's context.
- The bead record `coding-harness-77qj` itself (its description would name the class, per the 2026-10-22 rule in `AGENTS.md`) was not readable in this phase — I run no commands, and no rendered tracker copy is committed (house rule 2). The change folder holds no `spec.md` and so no `class:` header yet; the Stage-2 call line in `research.md` names the flash explore route, which per ADR 0020 serves `bounded` or `spike`. The class declaration is an open question for the runner's records.

## Which files a change would have to touch

- `scripts/stage2.py` — `verify_draft` (`scripts/stage2.py:7453-7520`): the launched command (`7491-7498`), the admission label (`7490`), the docstring's "`make verify`" wording (`7456-7461`); possibly the limit reference (`3854`, `7496`).
- `tests/test_stage2.py` — the draft-path tests listed above; any test that intercepts `["make", "verify"]` in the draft chain, plus the direct `verify_draft` callers if the signature or command changes.
- `docs/WORKFLOW.md` — "The draft (phases 2, 2b and 3)" (`docs/WORKFLOW.md:1203-1251`), and the doctrine-reading test `test_the_workflow_states_the_order_of_a_drafted_change` (`tests/test_stage2.py:13204`).
- Either `Makefile` (a new target, held to the gate list by `test_the_makefile_runs_what_the_one_list_runs`) or nothing extra if `stage2.py` calls `scripts/verify_all.sh` directly — the tree does not fix this choice.
- `scripts/ci_gates.py` and `decisions/gates.yaml` only if the selection mechanics or the report line change; both already support `--job docs` end to end.
- `prompts/` — likely untouched: the only draft prompt naming `make verify` is `prompts/03-plan.md:104`, whose claim stays true under a docs-only run because `criterion-ledger` is in the subset.
