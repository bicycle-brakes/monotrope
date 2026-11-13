---
title: "Research — swarm-shared-fixture"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-wnka
owner: Data Architect
provenance: human-written
tags: [research]
---

# swarm shared fixture — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-13: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1044 files, 4116 commits, 12 rules.

## Runner exploration — 2026-11-13

Research complete. Here is the prose ready to append to `plans/changes/swarm-shared-fixture/research.md` (the runner writes the file; the skeleton's provenance note at that file's top still applies to whoever commits it).

---

## What exists today

**The bead's in-repo trail.** The bead's own text (title, description) could not be read in this phase — the tracker is the Dolt database under `.beads/` and this explorer reads no tracker; that is "not read", not "empty". Four repository sources state its intent:

- `docs/research/2026-11-09-make-verify-long-term.md` ("Proposed order of work", step 3): "Shared fixture for the research-swarm tests (bead coding-harness-wnka): eleven of the twelve slowest tests are in that one file (baseline note)" — filed as a loose P2/P3 speed bead in the state table at line 109, proposed to move under the epic "Verify speed and machine load" (coding-harness-bxxt) at line 233.
- `docs/research/2026-11-04-verify-duration-baseline.md` ("Slowest single tests", lines 74–87, bead coding-harness-1um6): of the twelve slowest tests in five green full runs (median full `make verify` 1,223 s, pytest gate 81 %), eleven are in `tests/test_stage2_swarm.py`; top is `test_topic_five_relations_cover_exact_packet_neighbours` at 26.3 s.
- `docs/research/2026-11-12-test-strategy-draft.md` ("What was measured", line 35, bead coding-harness-dca4's measurement): 60 slowest tests cost 792 s, 438 s of them in `tests/test_stage2_swarm.py` (cut-off 2026-11-12) — down from 615.5 s of the 50 slowest 695.4 s on 2026-10-28 (`plans/changes/swarm-test-speed/research.md`, "Orchestrator addendum"), consistent with the sibling change's cached declaration parse, whose spec frontmatter says `implementation_status: partial`.
- `docs/research/2026-11-07-night-run-plan.md` (lines 95–97): wnka listed among the speed beads "not started tonight", parked behind the testing-strategy report by maintainer-approved grooming of 2026-11-07; `plans/INDEX.md` line 563 registers this research file as draft, `implementation_status: none`.

**The fixture machinery today.** All of it lives in `tests/test_stage2_swarm.py` — now 3,399 lines with 134 test functions (counted by grep, 2026-11-13; it was 3,051 lines / 123 functions on 2026-10-28 per the dca4 research). Its parts:

- Module constants resolved before any test narrows the environment: `GIT` (line 40), the planted credentials `OKEY`/`GKEY` with the `LEAK`/`DENYLIST` leak-check pair (lines 44–47), `TOPIC_OK`, `RECEIPT`, `SEED` (the seeded `research.md` bytes), `REPOSITORY_SEATS`, `ONLINE_SEATS` (lines 49–85).
- Canned report builders `seat_id`, `selection_for`, `with_go_store`, `locator_report`, `repository_report`, `online_report` (lines 88–182).
- `STAND_IN` (line 187): an embedded stand-in program (placeholders `@PYTHON@`/`@PI@`) that records every call to `calls.jsonl`, reads `scenario.json`, prints canned output and contacts nothing. Three sibling files carry their own copies or variants: `tests/test_stage2.py` line 91, `tests/test_stage2_research_availability.py` line 41, `tests/test_stage2_session.py` line 49 (`LAUNCH_STAND_IN`) — counted by grep over `tests/`.
- The `SwarmWorld` dataclass (lines 356–417) with `script`, `calls`, `run` (in-process `stage2.main(["explore", "demo", ...])`), `research_class`, `rewind`, `commit` (real `git add -A` plus a commit subprocess) and `complete` (the full happy-path scenario).
- The function-scoped `sworld` fixture (lines 420–514): per test it builds a git repository, seeds `plans/changes/demo/{research,spec,plan}.md`, `AGENTS.md` and `src/app.py`; copies the repository's real `prompts/` tree, `model-endpoints.yaml` and `research-swarm-limits.yaml`; rewrites the copied declaration's seat models with `admissible_terms` from `tests/terms_fixtures.py` and plants a synthetic `adresse` record for `opencode-go`; compiles `pin-pi` and `claude` from `STAND_IN` plus a failing bare `pi` trap; monkeypatches the production seams `stage2.PI_WRAPPER` (line 482) and `stage2_availability.consume_research` (lines 508–512); and restricts `PATH`, `HOME`, `XDG_STATE_HOME`, `CC_SECRETS`, `LEAKCHECK_DENYLIST` and the git environment (lines 490–500). Helper predicates `model_of`, `status_line`, `kinds`, `models`, `manifest_of` (line 1347) close the file. The fixture's own injection contract is under test: `test_swarm_uses_only_the_injected_pi_wrapper` (line 555) asserts the stand-in sits on `stage2.PI_WRAPPER` and the bare `pi` trap fails.

**Existing sharing.** Two files already import the fixture across test-module boundaries: `tests/test_stage2_research_deep_review.py` (20 test functions) re-binds `sworld = swarm.sworld` at line 28 and imports `SwarmWorld`, `manifest_of`, `status_line` at line 26; `tests/test_stage2_terms_expiry.py` imports `from test_stage2_swarm import sworld as research_world` at line 47 and mixes worlds per test through `request.getfixturevalue("sworld" ... else "world")` at line 593. There is no `conftest.py` anywhere in the repository (glob `**/conftest.py` — no files found; the dca4 research states the same for 2026-10-28). The single-explorer suite keeps a parallel, separately maintained copy of the same shape — the `world` fixture at `tests/test_stage2.py` lines 649–669 (tmp repo, prompts copytree, declaration pinning, stand-ins) — shared by name convention only (`world = stage2_world` in `tests/test_stage2_terms_expiry.py` line 49). The repository's one shared-fixture precedent is `tests/terms_fixtures.py` (42 lines, builder `admissible_terms`, contract-tested by `tests/test_terms_fixtures.py`), created by the archived change `plans/changes/archive/2026-11-06-terms-test-fixtures/` (bead coding-harness-hxkw, class bounded, `implementation_status: done`) after adding mandatory expiry broke 55 tests across suites; that change's non-goals explicitly excluded "general fixture/world consolidation" — the consolidation this bead names was left out on purpose.

**Where the time goes (measured, 2026-10-28).** The profile in `plans/changes/swarm-test-speed/research.md` ("Orchestrator profile") attributes the slowest swarm test's time to per-slot production costs, not fixture setup: `stage2_availability.read_declaration` 376 calls, 37.3 s (the 578-line declaration re-parsed before every slot) and `leakcheck.check` 156 calls, 20.1 s of which `leakcheck._git` is 468 subprocess calls, 15.8 s; the store's sealing is negligible. The same research gives the file's run arithmetic — explicitly not a measurement: roughly 130 `sworld.run()`/`prepare` calls of which ~60 full runs at 39 + 3N slots each (`Run.launch` in `scripts/stage2_research_run.py` starts a fresh interpreter per slot via `subprocess.Popen(..., start_new_session=True)`), several thousand interpreter starts, plus deliberate sleeps (finder trio `sleep: 5` expected in full; `sleep: 30` timeouts bounded to ≈1.8 s by `MINUTES` monkeypatching). No number in the repository separates per-test fixture-setup cost from in-run cost — not found in any gate, artefact or note (the two baseline notes measure whole tests only). dca4's spec names its non-goals as "optimising leak checks, dispatch scheduling, subprocess starts, **fixture setup** or unrelated YAML readers; those need separately measured changes" (`plans/changes/swarm-test-speed/spec.md`, "Non-goals") — the areas this bead covers were deliberately excluded there.

**Suite wiring and constraints.** One pytest lever, `python3 -m pytest tests/ -q -n auto` (`Makefile` line 22; declared in `decisions/gates.yaml`, run by `scripts/verify_all.sh`, generated into `.github/workflows/ci.yml`, pinned in `tests/test_ci.py` — per the dca4 research). pytest config is minimal: `[tool.pytest.ini_options] pythonpath = ["."]` only, no markers, no timeout plugin (`pyproject.toml` lines 25–33). The criterion-ledger gate (`scripts/check_criterion_ledger.py`) pins named swarm tests: references to `test_stage2_swarm.py::` names appear 143 times in `plans/changes/archive/2026-11-06-research-swarm/plan.md`, 8 in `plans/changes/archive/2026-11-06-swarm-time-limits/plan.md`, 1 in the active `plans/changes/pi-no-compaction/plan.md` and 4 in the active `plans/changes/swarm-test-speed/plan.md` (grep counts) — a renamed or deleted pinned test turns the gate red. The testing-strategy draft (`docs/research/2026-11-12-test-strategy-draft.md`, a proposal awaiting the bead coding-harness-1ga5 swarm run and an ADR — nothing built) sketches tiering through a future `tests/conftest.py` whose named fixtures — "the fixtures for the swarm, the pinned Pi's real data and the kit probe" — would mark tests as `system` (lines 87–91), and records that a targeted run of the swarm tests cannot end inside the runner's 5-minute tool limit (line 59, bead coding-harness-dq4u). The strategy draft also states there are no slow or integration markers in `tests/` today (line 37) and that the suite grew from 4,082 tests in 520 s (2026-10-28) to 5,604 in 1,270 s (2026-11-12).

## Where it lives

- Fixture and world: `tests/test_stage2_swarm.py` (`sworld`, `SwarmWorld`, `STAND_IN`, the report builders, `manifest_of`).
- Cross-importing consumers: `tests/test_stage2_research_deep_review.py` (lines 24–28), `tests/test_stage2_terms_expiry.py` (lines 45–50, 593).
- Shared-builder precedent: `tests/terms_fixtures.py` with `tests/test_terms_fixtures.py`.
- Sibling machinery (separate copy): `tests/test_stage2.py` `world` (line 649) and `STAND_IN` (line 91); further stand-in copies in `tests/test_stage2_research_availability.py` (line 41) and `tests/test_stage2_session.py` (`LAUNCH_STAND_IN`, line 49).
- Constraints: `scripts/check_criterion_ledger.py`; ledger blocks in the four plan files named above; the pytest lever (`Makefile`, `decisions/gates.yaml`, `scripts/verify_all.sh`, `.github/workflows/ci.yml`, pin in `tests/test_ci.py`).
- Context documents: `docs/research/2026-11-04-verify-duration-baseline.md`, `docs/research/2026-11-09-make-verify-long-term.md`, `docs/research/2026-11-12-test-strategy-draft.md`, `docs/research/2026-11-07-night-run-plan.md` (lines 95–97).

## What is unclear about it

- The bead's exact wording and scope — not read (tracker inaccessible to this explorer); the interview should confirm it against `docs/research/2026-11-09-make-verify-long-term.md` step 3.
- What "shared fixture" concretely means is stated nowhere: a helper module in the `tests/terms_fixtures.py` pattern, a new `tests/conftest.py` (none exists), or a wider fixture scope. Not found in any source — an interview question, not a guess.
- Whether fixture sharing moves the remaining 438 s is unmeasured: the only profile attributes the slowest test's cost to per-slot production work (declaration re-read, leak checks), which the sibling change dca4 partially addressed (`implementation_status: partial`); no measurement isolates fixture setup from run time.
- Whether the two cross-import re-bindings are the target pain, or only the per-test rebuild cost — the sources name both without ranking them.
- Whether tests may be renamed during consolidation: the ledger pins live partly in an archived change's plan (`2026-11-06-research-swarm/plan.md`, 143 references); whether ledger entries in archived plans may be edited for this change is unstated here.
- Whether the sibling `world` machinery in `tests/test_stage2.py` (983 test functions by grep; 877 per the strategy draft's 2026-11-12 count) is in or out of scope — the bead text says "research-swarm tests"; nothing in the repository answers the boundary.
- The living spec `plans/specs/implementation-verification/spec.md` was checked (head read) and concerns runner derived-file preparation before verify — no fixture relation found; treated as no neighbour.

## Which files a change would have to touch

- `tests/test_stage2_swarm.py` — fixture, `SwarmWorld`, `STAND_IN`, report builders (unavoidable).
- `tests/test_stage2_research_deep_review.py` and `tests/test_stage2_terms_expiry.py` — their cross-imports and re-bindings move to the fixture's new home.
- A new shared home — either a `tests/` helper module (precedent: `tests/terms_fixtures.py` plus its contract test) or a first `tests/conftest.py` (does not exist today).
- Only if a pinned test name changes: the ledger blocks in `plans/changes/archive/2026-11-06-research-swarm/plan.md`, `plans/changes/archive/2026-11-06-swarm-time-limits/plan.md`, `plans/changes/pi-no-compaction/plan.md`, `plans/changes/swarm-test-speed/plan.md` (gate: `scripts/check_criterion_ledger.py`).
- Not required for a test-only change: `Makefile`, `decisions/gates.yaml`, `scripts/verify_all.sh`, `.github/workflows/ci.yml`, the `tests/test_ci.py` pin (only if the pytest call itself changes); `scripts/stage2_research_run.py` and other production scripts (per-slot costs are dca4's declared scope, not the fixture's).

## Suggested neighbours for the header

`plans/changes/swarm-test-speed/spec.md` (active, same file, fixture setup named out of its scope) · `plans/changes/archive/2026-11-06-terms-test-fixtures/spec.md` (done; shared-builder precedent, world consolidation excluded there) · `plans/changes/archive/2026-11-06-research-swarm/spec.md` (built the swarm and pinned its test names in `plan.md`) · `plans/changes/pi-no-compaction/plan.md` (active, pins a swarm test name) · `plans/changes/archive/2026-11-06-swarm-time-limits/plan.md` (archived; pins the time-limit tests whose sleeps the fixture scenarios carry).
