---
title: "Research — implement-route-file"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-9ycy
owner: Data Architect
provenance: human-written
tags: [research]
---

# implement route file — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3347 commits, 12 rules.

## Runner exploration — 2026-11-06

Exploration complete. Here is the research, ready to append to `plans/changes/implement-route-file/research.md`.

---

## What exists today

**The implement route ladder is hard-coded in the runner.** `scripts/stage2.py`, function `implement`, builds the attempt list as three literal tuples: `(GLM_FLASH, key, "flash", None)`, then `(GLM_FLASH, key, "flash-repair", "first Flash post-run check failed")`, then `(SONNET, None, "stage-1", "two Flash post-run checks failed")`. With `--stage2-off` the ladder collapses to a single `(SONNET, None, "stage-1", <reason>)` attempt. Each tuple is `(endpoint, credential, route label, reason)` and is consumed by `run_attempts`, which walks it in order and stops or retries per attempt. The endpoint constants themselves stand at the top of the same file: `GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")`, alongside `GLM`, `HAIKU`, `SONNET`, `CODEX`, `OPUS` and `CODEX_EFFORTS`.

**The other verbs have their own hard-coded ladders in the same file.** `draft` routes `codex → codex-repair → glm`; `repair` routes `codex → codex-repair → stage-1` with the comment "No route reads the GLM credential" (ADR 0017); `explore` picks `GLM_FLASH` for a `bounded`/`spike` class, the research swarm for `feature`/`architectural` (ADR 0020), `HAIKU` on stage-2-off.

**The repository already has a file of record for model routing — and a file-declared precedent.** `model-endpoints.yaml` declares every admitted endpoint (`endpunkte`), its operator, residency, billing, `darf_sehen` data classes and model list. `scripts/stage2.py` reads it through `declaration_problem(root, endpoint, model)` (plus `entry_problem` and `excluded_problem`): an endpoint or model not cleared there is refused before any call. Guarded by `tests/test_model_endpoints.py` (RB-A6). Crucially, two routing mechanisms are *already* declared in this file rather than in code: the `research_swarm` block (its own comment says the roles are "DEKLARIERT, nicht in einem Skript hardkodiert" — declared here, not hard-coded in a script), read by `scripts/stage2_availability.py` (`data.get("research_swarm")`, `chosen_seats` over `repository_seats`/`online_seats`); and the review loop's paid ladder, derived from the `opencode-go` entry's `modelle` set ordered by `anfragen_5h` in `modelle_terms`, with free seats from the `free_stage` rule. The implement ladder is the remaining large routing decision that lives only in Python.

**The current ladder is pinned in prose in four doctrine surfaces.** `docs/WORKFLOW.md` names it in the phase table ("4 Implement | Sonnet 5.5 | … GLM 5.3 Flash builds instead"), the Stage-2 verb list ("implement — GLM 5.3 Flash, phase 4; --stage2-off uses Sonnet") and the runner paragraph ("a failed post-check gets one fresh Flash repair, then one Sonnet 5.5 fallback"). `prompts/04-implement.md`'s header names GLM 5.3 Flash and the Sonnet fallback. The root `AGENTS.md` Stage-2 paragraph says "GLM 5.3 Flash … implements". The implement-on-Flash decision itself traces to a maintainer statement of 2026-10-06 (bead coding-harness-qcp), recorded in the `glm-coding-plan` remark of `model-endpoints.yaml` — there is no ADR of its own; the nearest ADRs govern repair (ADR 0017, with ADR 0015 superseded by it) and the review loop (ADR 0011).

**An accepted living spec pins the ladder's limits.** `plans/specs/implementation-verification/spec.md`, criterion 4: "on the default Flash route, one Flash repair, then one Sonnet fallback after the initial Flash attempt; an explicit Stage-2-off run keeps its single Sonnet attempt. No additional attempts." This spec is `accepted`, `implementation_status: done`.

**Route labels are free-form words in the record grammar, not an enum.** `scripts/time_records.py` (`RECORD` regex, `format_entry`, `_check_word`) accepts any route value without separators; `scripts/run_report.py` groups and prints records by the route string; `scripts/harness.py time-log --route` requires a value and treats `orchestrator` as the interactive-span marker; findings.md attempt blocks embed the label ("Attempt N (route) failed its post-run checks", `attempt_block`). `scripts/stage2_runs.py` imports the constants (`FOREIGN_ROUTES = (stage2.CODEX, GLM, stage2.GLM_FLASH)`) with a comment stating they are read from `stage2.py` deliberately "so it cannot drift", and its runs-report criterion 4 clears each foreign route via `declaration_problem`.

**Tests pin the ladder's order and labels exactly.** `tests/test_stage2.py` asserts `"attempt 1 · route flash"`, `"attempt 2 · route flash-repair"`, the retry-prompt text "Attempt 2 (flash-repair) failed its post-run checks.", and a planted-fault refusal naming "the GLM route on `glm-5.3-flash`, a shell tool, or a fourth attempt" (criterion 19).

**The measurement behind any ladder change exists.** `docs/research/2026-11-02-route-success.md` (spike bead coding-harness-hleu) measured: Flash implement chains reached acceptance in a median 63.8 minutes, 6 of 22 never; stage-1 Sonnet chains median 13.5 minutes on 7 chains. Its recommendation was "No routing change now", with one named option for the maintainer — after one rejected Flash implement attempt go to Sonnet directly instead of the Flash repair attempt — conditioned on bead coding-harness-6ie ("Sonnet continues Flash's edits") landing first.

## Where it lives

Runner and constants: `scripts/stage2.py` (`GLM_FLASH`…`OPUS` constants, `implement`, `draft`, `repair`, `explore`, `run_attempts`, `declaration_problem`). Declarations: `model-endpoints.yaml` (`endpunkte`, `research_swarm`, `free_stage`, `modelle_terms`), read by `scripts/stage2_availability.py` and `scripts/stage2_swarm.py`. Label consumers: `scripts/time_records.py`, `scripts/run_report.py`, `scripts/harness.py`, `scripts/stage2_runs.py`. Doctrine: `docs/WORKFLOW.md`, `prompts/04-implement.md`, `AGENTS.md`. Guards: `tests/test_stage2.py`, `tests/test_model_endpoints.py`. Neighbouring accepted spec: `plans/specs/implementation-verification/spec.md`.

## What is unclear about it

1. **The change's exact scope is unread.** Bead coding-harness-9ycy's description lives in the tracker (the Dolt database under `.beads/`, transported via `refs/dolt/data`); no rendered copy is committed (house rule 2) and my read-only file tools cannot read git refs, so what "route file" precisely means — a new file, a block in `model-endpoints.yaml` like `research_swarm`, a per-change override, or only a different fallback order — is an open question, not a fact. The tree carries only the folder name and the `plans/INDEX.md` row.
2. **Not found anywhere: a written statement of which verbs a route file would govern.** The name says implement; whether `draft`, `repair` and `explore` ladders stay code-side is stated nowhere.
3. **Term collision to keep apart:** `prompts/04-implement.md` already uses "file-only route" for a different concept (a route whose model can edit files but has no command tool). "Route file" is not an existing term in the tree; "file-only route" is.
4. **Unexamined interaction:** `stage2_runs.py`'s comment says its foreign-route tuple is read from `stage2.py` constants so it cannot drift; how a file-driven implement route reconciles with that stance is unexamined.
5. **Spec constraint:** the accepted `implementation-verification` spec fixes "No additional attempts" on the default Flash route; whether this change must amend that spec or merely respect it is unanswered.
6. **Sequencing fact from the measurement:** `docs/research/2026-11-02-route-success.md` names bead coding-harness-6ie as something that "should land first" before any ladder change; no change folder for 6ie exists under `plans/changes/` (checked the spec listing), and its tracker state is not readable with my tools.
7. **Human question, recorded as such:** changing the default implement route touches a maintainer-stated routing decision (2026-10-06, bead qcp, in `model-endpoints.yaml`) that has no ADR; whether a decision pull request or an ADR draft is wanted is `[DECISION]` material for the interview.

## Which files a change would have to touch

`scripts/stage2.py` (the `implement` ladder and its consumption in `run_attempts`); `model-endpoints.yaml` if the route is declared there (the existing home of declared routing), with `tests/test_model_endpoints.py` as its guard; `tests/test_stage2.py` (the pinned order/label assertions listed above); `docs/WORKFLOW.md` (three prose surfaces in §4); `prompts/04-implement.md` (header); `AGENTS.md` (Stage-2 paragraph); `scripts/stage2_runs.py` (`FOREIGN_ROUTES`, criterion 4); `scripts/time_records.py` and `scripts/run_report.py` only if route-label semantics change — today the grammar is label-agnostic. `plans/INDEX.md` regenerates as a derived file.

## Known neighbours (for the header)

`plans/specs/implementation-verification/spec.md` · `plans/changes/research-swarm/spec.md` · `plans/changes/codex-repairs/spec.md` · `plans/changes/kimi-admission/spec.md`
