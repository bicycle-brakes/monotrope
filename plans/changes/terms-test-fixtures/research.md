---
title: "Research — terms-test-fixtures"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-hxkw
owner: Data Architect
provenance: human-written
tags: [research]
---

# terms test fixtures — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-27: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 704 files, 2375 commits, 12 rules.

## Runner exploration — 2026-10-27

Exploration complete. Below is the research, ready to append to `plans/changes/terms-test-fixtures/research.md`.

---

**Suggested header line (the runner adds what its finders suggest):**

```
neighbours:
  - plans/changes/terms-expiry/spec.md
  - plans/specs/implementation-verification/spec.md
```

`plans/changes/terms-expiry/spec.md` is the closest active change (bead coding-harness-abra); its `findings.md`, `plan.md` and `decisions.md` carry the incident this change responds to. `plans/specs/implementation-verification/spec.md` is the repository's only living spec and has **not been read** in this exploration — it is listed so it gets reported on, not because its content is known here.

## What exists today

**The incident this change is named for.** During the terms-expiry change, merging `origin/main` (commit `87df6f7b`) brought in `tests/test_stage2_research_availability.py`, whose hand-built fixture terms records carried no expiry field; under the new admission rule every such record was excluded, so no research seat had an admitted candidate, and 55 tests failed in that one file (`plans/changes/terms-expiry/findings.md`, "Cause, measured by the orchestrator" block, and the attempt-1 diagnostics above it). The orchestrator repaired it **by hand** by adding the far-future expiry to the other suite's fixture, and the repair landed outside any runner attempt. The handover names the follow-up bead verbatim: "hand-built terms fixtures break other suites after a merge (coding-harness-hxkw, bounded)" (`docs/journal/handover/2026-10-27-night-run.md`, "Open work and blockers", "New beads this session").

**The admission rule that makes fixture records load-bearing.** A paid model is admitted only with a dated, sourced reading that rules out training and carries a quoted ISO `valid_until`; a missing, unusable or passed date refuses admission, fail-closed (`scripts/stage2.py`, `terms_problem` and `_valid_until`; doctrine text at `docs/WORKFLOW.md` "Paid terms expire (ADR 0022, bead coding-harness-abra)"; ADR `docs/adr/0022-paid-model-terms-expire.md`, Decision 1–2). A terms record alone also admits a model for research seats (`scripts/stage2_availability.py`, `research_terms_problem`, "A model is listed in `modelle` or - for research only - by a `modelle_terms` record"). So any test suite that builds a synthetic `opencode-go` declaration must build terms records that satisfy the **current, full** rule — and each rule tightening silently invalidates every fixture that predates it.

**The hand-built fixture sites** (all found by searching `tests/**` for `modelle_terms`, `terms_record` and the far-future expiry literals; `tests/` has no `conftest.py` and no shared helper module — every file is a `test_*.py`):

- `tests/test_stage2.py` — the de-facto shared suite: constants `TEST_LADDER`, `TEST_FLASH`, `TEST_FREE`, `TEST_RUNGS` (symbol block near the top of the file's middle section), `pin_entry` and `pin_the_ladder` (each writes a full `opencode-go` entry with `valid_until: "2099-01-01"` and `anfragen_5h` for every model; `pin_the_ladder`'s docstring states the intent: "The real order and the real terms are the maintainer's … the tests … must not break when it changes"), `loop_state` (the saved-run snapshot), and the `world` fixture, which builds a temp repository and writes the synthetic declaration through `pin_the_ladder`. The same file also mutates terms records ad hoc in later tests (`del entry["modelle_terms"][...]`, `pop("anfragen_5h")`, `training = "Yes"`, `uebersprungen` planting).
- `tests/test_stage2_terms_expiry.py` — the terms-expiry suite itself; hand-built helpers `set_terms` (rewrites one model's record in the world's declaration) and `a_record` (one admissible record with every required field, far-future expiry). It does not own its fixtures: it imports `World`, the constants and `world` from `test_stage2`, `enable`/`receipt` from `test_stage2_availability`, and `sworld` from `test_stage2_swarm` (its import block; cross-module import of test modules, enabled by `pyproject.toml` `[tool.pytest.ini_options] pythonpath = ["."]`).
- `tests/test_stage2_availability.py` — `enable` (adds `availability_preflight` to the world's entry) plus direct record mutations (popping `anfragen_5h`, setting `training: "Used"`, overwriting `valid_until` for date-seam tests).
- `tests/test_stage2_session.py` — its **own** `World` class and `declare_go`, which builds a complete `opencode-go` entry with terms for `GO_BARE` (`mimo-v2.6-flash`), far-future expiry but **no `anfragen_5h`** — a third, independent shape of the same fixture.
- `tests/test_stage2_swarm.py` — the `sworld` fixture copies the **real** `model-endpoints.yaml`, then rewrites the seat models' records (pops `uebersprungen`/`grund`, stamps `gelesen`/`valid_until: "2099-01-01"`/`quelle: "synthetic dispatcher terms"`); its comment states why: "the real declaration may skip a fixture member, and its dates must not age these dispatcher tests into refusals."
- `tests/test_stage2_research_availability.py` — its own `TERMS` table (14 ids) and `terms_record(value)` builder, now carrying `valid_until: "2099-12-31"` with the comment "Every terms reading carries its expiry (ADR 0022); far ahead, so the fixture never expires" — that value is the hand-patch from the incident.
- `tests/test_pi_contract.py` — `declare_contract_models`, a fourth builder: a minimal declaration with four synthetic ids, each with a full terms record ("Synthetic, dated admission for loopback wire tests; never use live terms").
- `tests/test_model_endpoints.py` — gates the **real** declaration (`ENDPUNKTE = REPO_ROOT / "model-endpoints.yaml"`; `test_every_new_paid_model_carries_its_terms_reading` requires a `gelesen`/`quelle` for every `modelle` id) and also plants a partial record in one test (`go["modelle_terms"] = {"q-flash": ...}`).

Two further coupling mechanisms are documented in the terms-expiry review rows: L1-3 (the migration tests read the live declaration and hard-coded the DeepSeek dates, so the **required monthly renewal would have turned them red**; fixed by pinning the rule — reading plus 30 days, or the source's stated end — instead of the dates) and F6-2 (preparation tests patched `stage2.run_reviewer` while production had moved to `stage2_availability.probe_go`, so the fixtures held a stale production seam). Both rows sit in `plans/changes/terms-expiry/findings.md` (phase-6 table and loop table respectively). The repair of L1-2/L1-3 was hand work, because the runner's red-first check rejects test-only repairs (status cells of those rows; bead coding-harness-0ho, named in the handover).

**Current state of this branch.** The F6-3 repair is present in this worktree's tree — `test_research_probes_and_dispatch_recheck_expiry` (`tests/test_stage2_terms_expiry.py`) and the production recheck `research_terms_problem`, called from `scripts/stage2_research_run.py`'s `Run.gate` path — so this branch's base is newer than the handover, which still lists F6-3 as the open row on the terms-expiry decision PR. The merge commit itself is not visible in the five most recent commits shown to this session; that remains an open question, not a claim.

## Where it lives

- Incident record: `plans/changes/terms-expxiry/findings.md` — correction: `plans/changes/terms-expiry/findings.md` (attempt diagnostics and the "Cause, measured by the orchestrator" block, phase-4b section; F6-1/F6-2/F6-3 and L1-1…L1-10 rows).
- Doctrine and decision: `docs/WORKFLOW.md` ("Paid terms expire"); `docs/adr/0022-paid-model-terms-expire.md`; `plans/changes/terms-expiry/decisions.md` (Q-1…Q-7; the note that the field first named `gilt_bis` is `valid_until` in code and declaration).
- Production seam: `scripts/stage2.py` (`endpoint_entry`, `_terms`, `terms_today`, `_valid_until`, `terms_problem`, `terms_warnings`, `retain_terms_warnings`, `capture_terms_warnings`); `scripts/stage2_availability.py` (`research_terms_problem`, `preparation_terms`, the report rendering of `Terms warning:`); `scripts/stage2_research_run.py` (the two `research_terms_problem` call sites in the gate path).
- Real declaration: `model-endpoints.yaml` at the repository root (the `opencode-go` entry: `modelle`, 18 `modelle_terms` records — six with `uebersprungen` skip markers — plus `availability_preflight`, `flash_swarm`, `free_stage`, and the `research_swarm` block).
- Test-run wiring: `Makefile` (`python3 -m pytest tests/ -q -n auto`, pytest-xdist) and `pyproject.toml` (`[tool.pytest.ini_options] pythonpath = ["."]`).

## What is unclear

- The bead's exact current text and scope: the tracker is the Dolt database under `.beads/`, which this read-only exploration cannot open; the handover sentence is the only in-repository statement of the assignment. Open question for the interview.
- Whether the terms-expiry decision pull request has actually merged (see above) — for the orchestrator or maintainer to confirm, not a repository question.
- `plans/specs/implementation-verification/spec.md` exists but was not read; whether it constrains test-fixture changes is an open question.
- "Not found" vs "not there": a dedicated cross-suite fixture-compatibility gate is **not there** — no test asserts that one suite's terms records satisfy `terms_problem`, and no shared helper exists; the only compatibility mechanism today is the full suite in `make verify` (`plans/changes/terms-expiry/plan.md`, Verification section: "The full suite checks fixture compatibility"). Whether any *other* mechanism was intended is not found anywhere in the change folder.

## Which files a change would have to touch

The eight fixture sites listed above, if the fixture builders are consolidated or made rule-proof: `tests/test_stage2.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_session.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_research_availability.py`, `tests/test_pi_contract.py`, `tests/test_model_endpoints.py`. Any new shared helper must live as a plain importable module (no `conftest.py` exists; imports resolve through `pythonpath = ["."]` and the suite runs under `pytest-xdist` with `-n auto`). `plans/INDEX.md` regenerates through `scripts/plans_registry.py --index` as usual. A test-only change also interacts with the runner's red-first check (the coding-harness-0ho exception the handover records), which shapes how such a change can be implemented and repaired — stated here as a fact of the process, not as a design choice.
