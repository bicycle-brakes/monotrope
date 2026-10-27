---
title: "Research — workflow-promises"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-i0l
owner: Data Architect
provenance: human-written
tags: [research]
---

# workflow promises — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-27: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 704 files, 2375 commits, 12 rules.

## Runner exploration — 2026-10-27

Exploration complete. Here is the research, ready to append to `plans/changes/workflow-promises/research.md`.

---

## What the change is

Bead coding-harness-i0l asks for a reconciliation of the repository state with `docs/WORKFLOW.md` ("workflow promises"): every mechanism the doctrine (and its sibling documents `README.md`, `docs/how-it-works.md`, `AGENTS.md`) describes, sorted by whether it is described only, built, or enforced. The bead's intent is recorded in three places: `docs/research/2026-10-20-night-run-plan.md` (item 9: "a dated table under `docs/research/` (described, built, enforced) … it includes the stop hook the doctrine describes and the README lists as not built"), `docs/research/2026-10-21-night-run-plan.md` (filler item: "read-only; a dated report and one bead per missing piece"), and `docs/journal/handover/2026-10-19-optimization-exploration.md` ("Open decisions" §2), which named the bead and assigned three findings to it: the § 8 statement, the DRIFT-does-not-block semantics, and the broken environment. Night-run handovers of 2026-10-21 and 2026-10-22 record the bead as not started.

## What exists today — prior reconciliation artefacts

A full blank-slate audit is not needed; four snapshots already exist and a change updates rather than re-creates them:

- **`docs/WORKFLOW.md` header block, "Not all of it is here yet"** — checked 2026-09-30 against the tree at `41abf42`. It lists as absent: `scripts/validate_change_artefacts.py`, the sub-agents `.claude/agents/explorer.md` and `reviewer.md`, the stop hook `.claude/hooks/session-stop/check-tests-green.sh`, `.claude/commands/`, the targets `make change` and `make index`, and `docs/governance/gate-catalog.md`. It also records the deliberate absence of the irreversible-action brakes in `.claude/settings.json`.
- **`README.md`, "What works today"** — checked 2026-10-22 against `main` at `72935a6`. Three levels: enforced by tooling / written rule / not built yet. The "Not built yet" list: a validator for the change files, a stop hook, slash commands, a `make change` shortcut, a gate catalogue, the research swarm ("a draft proposal"), a sandbox around paid reviewers, keeping a failed call's work ("partly built"), orchestration.
- **`docs/architecture/2026-09-17-gap-analysis.md`** — an earlier corpus-versus-harness measurement at `eddfc0b` (64 failed, 182 passed tests at that commit, per its snapshot section). It is the methodological precedent, not a spec.
- **`docs/research/2026-10-08-holding-criterion-tests.md`** — a measured audit of what holds spec-criterion tests (the 29-of-30 test deletion that left `make verify` green); it produced the criterion ledger (`scripts/check_criterion_ledger.py`, gate `criterion-ledger` in `decisions/gates.yaml`).

## What exists today — the promises checked against this tree (2026-10-27)

**Promised and present.** The gate-list mechanism stands: `decisions/gates.yaml` holds 23 gate ids (grep `- id:`: pytest, ruff-check, ruff-format, leerprobe, plans-registry, docs-links, frontmatter-current, bead-export, dangling-beads, decision-continuity, adr-answers, interview-minimums, question-context, criterion-ledger, research-handoff, gate-schema, ci-drift, ramp-valves, ruleset, markdownlint, lychee, plans-registry-strict, research-currency); `scripts/verify_all.sh` and `scripts/ci_gates.py` exist; `Makefile` targets `verify` and `gates` delegate to them, and its header comment names `tests/test_ci.py` as the pin (W-6) — that test file exists. Every gate script the doctrine names exists under `scripts/` (`check_adr_answers.py`, `check_interview_minimums.py`, `check_question_context.py`, `check_criterion_ledger.py`, `check_research_handoff.py` with `research_handoff.derive_inventory` in `scripts/research_handoff.py`, `plans_registry.py`, `leakcheck.py`, `stage2_runs.py`, `adoption.py`, `harness.py`, `omnigent_policy.py`, the `stage2_research_*` modules). `scripts/stage2.py` dispatches exactly the twelve verbs the doctrine's §4 lists (explore, prepare-explore, draft, spec-review, implement, repair, prepare-loop, review-loop, release-loop, review, probe, session; dispatch table around `stage2.py` `VERBS`, lines ~7859–7878). `Makefile` also carries `leakcheck`, `venv` and `lock`, which §3's entry-commands row does not mention. `.claude/settings.json` holds the SessionStart hook (`tools/bd prime --hook-json`), the merge-guard ask rules (`gh pr merge` in four spellings, `gh api *merge*`, `gh alias set *`, `git push *main*`, `mcp__*__merge_pull_request`), `Bash(codex *)`, the `mcp__omnigent__sys_advise_models` ask rule, and the Omnigent deny list plus `Edit(//**/.omnigent/config.yaml)` — matching WORKFLOW §3 items 3 and 5. `.codex/hooks.json` and `.codex/config.toml` exist as §4 claims. `decisions/adoption.yaml`, `decisions/gates.yaml` and twenty `decisions/answers/<change>/adr.yaml` files exist; `.github/PULL_REQUEST_TEMPLATE/decision.md`, `.github/pull_request_template.md` and `.github/workflows/ci.yml` exist. `templates/` holds adr, agents-mergeable-prs, arc42, design, findings, gate-record.yaml, handover, spec. `prompts/` holds all eleven phase prompts plus `research-recheck.md` and seven `research-swarm/` prompts. All 22 ADRs `docs/adr/0001`–`0022` exist; ADR 0020's header says `status: accepted`. The tools stand: `tools/bd`, `tools/beads/install.sh`, `tools/pi/` (pinned `package.json`, `pi` wrapper, `install.sh`), `tools/claude-code/` (including the four hooks `handover.sh`, `parallel-sessions.sh`, `recap.sh`, `session-scan.sh` that README's parallel-work section describes), `tools/omnigent/` (`policy.yaml`, `install.sh`), `tools/cloud-env/`. `tests/test_repo_settings.py` exists and holds exactly the branch-ruleset live check (RB-M6/RB-G7) the header note describes; `tests/test_entry_points.py`, `tests/test_regelwerk.py` and `tests/test_stage2_swarm.py` exist as AGENTS.md and the Regelwerk reference them. `provenance.yaml` and `model-endpoints.yaml` exist at the root. `docs/research/2026-10-27-parked-runner-prs.md`, cited by §3's "Pull requests stay mergeable", exists.

**Promised and absent (described, not built — verified by Glob/Grep over this worktree, not found anywhere in the tree):**

1. `scripts/validate_change_artefacts.py` — no file of that name exists tree-wide (`**/validate_change_artefacts.py` finds nothing). It is promised as a runnable gate command in `prompts/02-spec.md` (gate line: `python3 scripts/validate_change_artefacts.py --check` green) and `prompts/03-plan.md` (same gate line), and in `docs/WORKFLOW.md` §2 twice ("since `validate_change_artefacts.py` one does"; phase-2/3 gates "run as one line … by `validate_change_artefacts.py`"), plus `scripts/plans_registry.py` (comment referencing a future `_praesenz_ramp` in the validator) and `docs/architecture/target-architecture.md` (D-11). Several change folders already record the absence at their baselines (`plans/changes/research-currency/research.md` and `spec.md`, `plans/changes/pi-pin/research.md`, `plans/changes/venv-pycache/research.md`, `plans/changes/haiku-5-5/plan.md`, `plans/changes/codex-repairs/plan.md`, `plans/changes/runner-time-line/plan.md`). Consequence visible today: the phase-2 and phase-3 gates named "validator green" cannot run as written.
2. `.claude/agents/explorer.md` and `.claude/agents/reviewer.md` — not there. `.claude/agents/` holds seven different definitions (code-generation-orchestrator, consistency-auditor, entity-builder, entity-deployer, migration-supervisor, preconditions-gate-runner, reconciliation-orchestrator), German, carrying the Regelwerk's RB-A1 evidence contract "byte-gleich" per `docs/governance/regelwerk.md` §6, held equal by `tests/test_regelwerk.py`; e.g. `reconciliation-orchestrator.md` declares `tools: Read, Write, Grep, Glob, Bash` — not the read-only pair §3's table describes. `docs/governance/regelwerk.md`'s changelog also notes sixteen agent definitions resolving, fourteen pinning an older model generation than WORKFLOW routes, as "ein eigener Vorgang".
3. `.claude/hooks/session-stop/check-tests-green.sh` — not there; `.claude/` contains only `agents/` and `settings.json`. The stop hook is promised as the phase-5 gate in `docs/WORKFLOW.md` §2 (phase table: "the stop hook blocks on a red tree") and §3's table, and in `AGENTS.md`'s phase table ("stop-hook blocks on a red tree"). README's "Not built yet" states the same absence.
4. `.claude/commands/` — not there, so `/workflow-start` (promised in the `docs/WORKFLOW.md` header block, "Starting a session") does not exist. README lists slash commands under "Not built yet".
5. `make change` and `make index` — the Makefile defines only verify, test, staleness, gates, leakcheck, venv, lock. §3's "Entry commands" row promises six targets including `change` and `index`; four of the six exist. README records the `make change` gap; the `make index` gap is visible only by comparing the row with the Makefile.
6. `docs/governance/gate-catalog.md` — not there (`docs/governance/` holds `quality-gates.md` and `regelwerk.md`). `docs/WORKFLOW.md` §2 ("A gate is sensible …") links `governance/gate-catalog.md#bevor-ein-gate-scharfgestellt-wird` — a dead link whose anchor fragment is still German in an English file — and says its checklist "stands once" there.

**Stale statements — described one way, the tree says another:**

1. **Research swarm status, three-way divergence.** `docs/WORKFLOW.md` §2/§4 describes the swarm as live (ADR 0020 accepted; `scripts/stage2_research_*.py`, `prompts/research-swarm/`, the `research-handoff` gate in `decisions/gates.yaml` all exist), while `README.md` "Not built yet" lists "The research swarm for larger changes (a draft proposal)" and `docs/how-it-works.md` ("Research swarm") says "its implementation is not built". The two latter documents carry their 2026-10-22 snapshot; ADR 0020's header was updated 2026-10-21 and says accepted.
2. **Container fence, contradiction inside `docs/WORKFLOW.md` itself.** The header note says "the container fence §3 describes is not in it yet"; §3 ("No container belongs to it") says "`tests/test_repo_settings.py` holds the fence: a tracked `Dockerfile`, `devcontainer.json`, `dagger.json` or `docker-compose*` fails the suite." Grep over `tests/` for those four names finds no match — the header note is the true one today.
3. **Findings template.** `docs/WORKFLOW.md` §4 ("Two columns for every stage-2 change") justifies defining the columns "because the findings template is not in this repository yet" — but `templates/findings.md` exists and already carries both stage-2 headers (`Reviewer` / `Broke a test` / `Phase 6`), under a stale conditional "Once pull request #60 is merged" (stage 2 has been live since ADR 0007, long before #60's time).
4. **Failed-call work.** README lists "keeping the work of a failed model call" as partly built; `docs/WORKFLOW.md` §4 describes it as standing behaviour (the worktree restore on a failed model process, and repair answers kept as protected evidence under `stage2/attempts/<change>/` below the worktree's git directory).
5. **The header not-built list itself** is dated 2026-09-30 at `41abf42` and has not been re-checked since, while the file around it moved (`updated: 2026-10-27`).

**Recorded findings already assigned to this bead** (`docs/journal/handover/2026-10-19-optimization-exploration.md`, cut-off 2026-10-19 at `main` `6477d04`): the § 8 statement (no MCP server — recorded there as a decision, not work); the DRIFT-does-not-block semantics (`scripts/plans_registry.py` classifies DRIFT, `Verdict.exit_code()` returns 0 without `--strict`, the strict variant runs only in the nightly `plans-registry-strict` gate, and `Makefile` `staleness` runs the non-strict `--check`); the broken environment on the maintainer's machine (`.venv/bin/` without an interpreter, missing Pi install — machine state, not tree state); and the nightly drift gate red 20 consecutive nights with 91 findings (83 change folders whose bead closed while the artefact still says `implementation_status: none`/`partial`, plus 8 in-progress beads with no artefact).

## Where it lives

Promise sites: `docs/WORKFLOW.md` (header block, §2 phase table and "five rules", §3 stage-1 table, §4 verbs and mechanisms), `AGENTS.md` (phase table, house rules), `README.md` ("What works today"), `docs/how-it-works.md` (swarm sections), `docs/architecture/target-architecture.md` (D-11), the gate lines of `prompts/02-spec.md` and `prompts/03-plan.md`, `templates/findings.md` (stage-2 block), `.github/PULL_REQUEST_TEMPLATE/decision.md`. Holders: `decisions/gates.yaml` (the one gate list, D-10), `scripts/` gates and runner, `Makefile`, `.claude/settings.json`, `.github/workflows/ci.yml`. Neighbouring artefacts already read: the living spec `plans/specs/implementation-verification/spec.md` (accepted, done, per `plans/INDEX.md`), the active specs `plans/changes/research-currency/spec.md` (already records the validator's absence) and `plans/changes/verify-stages-new-files/spec.md` (verify-stage work), plus `docs/architecture/2026-09-17-gap-analysis.md` as the prior reconciliation (not a spec).

## What is unclear (open questions, not read or not readable here)

- The bead's exact current title, description and class: the tracker is the Dolt database read through `tools/bd`; this phase reads no tracker. The class declaration for this change is not in the tree — `plans/changes/workflow-promises/research.md` frontmatter carries no `class:` field; the recorded stage-2 line ("route flash") is consistent with the `bounded`/`spike` route of ADR 0020, but the declaration itself was not seen.
- Whether a live research-swarm run (the full `39 + 3N` calls) has ever happened: not found in the tree; this change's own explore ran the flash route. Stated as not found, not as "never happened".
- Whether the nightly drift gate is still red after 2026-10-19, and whether the 91 findings were since reduced: GitHub run history is not readable here; the newest tree record is the optimization handover. The change `plans/changes/verify-stages-new-files/` (active, bead coding-harness-fdz) touches this area unread.
- Whether `tools/omnigent/` is installed on this machine (`docs/WORKFLOW.md` §3: "built but not installed" as of 2026-09-29): installation is user-level state outside the tree.
- Whether `.claude/settings.json` still matches its description at phase-6 time: verified today (see above), but the file is machine-owned configuration and can change without a doctrine edit.

## Which files a change would have to touch

The report itself: a dated table under `docs/research/` (the night-run plan's named output), plus `plans/INDEX.md` regenerated via `scripts/plans_registry.py --index`. The stale statements live in `docs/WORKFLOW.md` (header not-built list, §2 validator sentences and gate-catalog link, §3 entry-commands row and container-fence sentence, §4 findings-template clause), `README.md` ("Not built yet" rows), `docs/how-it-works.md` (research-swarm section), `templates/findings.md` (the "once PR #60 is merged" conditional). The absent pieces would each be a new file or a deliberate rewording of the doctrine line that names them: `scripts/validate_change_artefacts.py` (with its gate wiring in `decisions/gates.yaml` and the `ci-drift`-generated `.github/workflows/ci.yml`), `.claude/hooks/session-stop/check-tests-green.sh`, `.claude/agents/explorer.md` and `reviewer.md`, `.claude/commands/`, the `make change`/`make index` targets in `Makefile`, and `docs/governance/gate-catalog.md`. Any touch of a file `provenance.yaml` reserves for `human-decided` (the ADRs, the rule set) is a decision pull request per `docs/WORKFLOW.md` §2; `tests/test_regelwerk.py` holds the seven present agent definitions byte-equal, so they are not free to edit. A follow-up bead per missing piece is the night-run plan's stated form for everything this change only reports.
