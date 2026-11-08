---
title: "Research — outcome-test"
status: draft
implementation_status: partial
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-3nm5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol draft gap check, 2026-11-06; exploration attributed below"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# outcome test — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3362 commits, 12 rules.

## Runner exploration — 2026-11-06

Research complete. Here is the prose for `plans/changes/outcome-test/research.md`, structured as the phase requires. (I hold only file tools and run no command, so the bead record itself was not read — noted under open questions.)

---

## What exists today

**The ask, and where it comes from.** Bead `coding-harness-3nm5` ("Outcome test for fresh sessions") was filed on 2026-11-02 from the evaluation of the model-wiki article and EGM (`docs/research/2026-11-02-model-wiki-and-egm.md`, the row "An outcome test: fixed questions, expected answers read from the live system, run nightly" at the wiki table, and the bead list in "Beads filed from this evaluation"). The idea: a small, fixed question set — the source names three examples ("which model repairs, what the verify admission's floor is, where run plans live") — answered by a fresh session, with the expected answers read from the live system, so the measurement says whether a fresh session knows the harness's current rules and state. The evaluation adopts it "as the acceptance test of bead coding-harness-g4iq" (the consolidation run), answered "before and after consolidation". The handover of the same day records it as filed on the maintainer's request (`docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`, "Decisions and preferences", "an outcome test (-3nm5)"). The evaluation's "Not done in this reading" section states explicitly that the outcome test was never tried on this repository — no experiment exists yet. The source's own evidence quality is named as "an anecdote, not a measurement this repository can lean on" (`docs/research/2026-11-02-model-wiki-and-egm.md`, "Evidence quality").

**No knowledge measurement exists.** Every gate in `decisions/gates.yaml` measures artefacts: pytest, ruff, the kit probe, the plans registry, frontmatter currency, bead export, dangling beads, decision continuity, ADR answers, interview minimums, question context, criterion ledger, research handoff, guard-test environment, gate schema, ci-drift, ramp valves, ruleset, markdownlint, lychee, plus the two `job: drift` gates (`plans-registry-strict`, `research-currency`). No gate asks a model or a session anything. A repository-wide search for a quiz/question-set/expected-answer mechanism finds exactly one hit — the source note itself. This matches the evaluation's own finding, "gates measure artefacts, not knowledge" (`docs/research/2026-11-02-model-wiki-and-egm.md`), and its row 8 statement that "prompt texts are tested structurally; no test asserts what a prompt makes a model answer" — structural checks confirmed in the tree (`tests/test_templates.py`, which asserts the ADR template's section headings; `tests/test_stage2.py`, which holds an AGENTS.md 200-line cap). A *different* filed bead covers prompt-behaviour scenarios: coding-harness-xai7, "whether a small scenario set for the phase prompts catches regressions the format checks miss" (same note, row 8) — adjacent, not this change.

**The nightly run the source points at exists in two forms.** (1) The hosted drift job: `.github/workflows/ci.yml` schedules cron `23 4 * * *`, and the `drift` job runs on schedule/dispatch — this is what `research-currency` calls "the nightly drift run" (`decisions/gates.yaml`, research-currency reason). (2) The night run: one orchestrated session working a queue, with a morning handover page of fixed form (`docs/research/2026-10-12-night-run.md`, "The shape, three parts", part 3; doctrine in `docs/WORKFLOW.md`, "Night runs"). Either could carry a recurring outcome test; the recurring-job mechanism already exists (`docs/WORKFLOW.md`, "Recurring jobs": a job prompt is a file in `prompts/` that is not a phase, started by a schedule or a person, writes no tracker, takes no git action; first instance `prompts/research-recheck.md`).

**What a fresh session actually reads (the thing the test would measure knowledge of).** `AGENTS.md` at the repository root — "This is the only instruction file" (`AGENTS.md`, opening); the repository states a standing rule belongs there because "every harness reads it" (same file, house rules). The full doctrine in `docs/WORKFLOW.md`. At session start, two hooks supply context: the user-level entry `tools/claude-code/hooks/handover.sh` (`start` mode shows where things stand and injects the newest handover's content — but only for repositories in `~/.claude/handover-trust`; untrusted ones see metadata only) and the repository SessionStart hook `tools/claude-code/hooks/beads-start.sh`, which reconciles merged-bead closures and then emits `tools/bd prime --hook-json` output as context. Handovers live under `docs/journal/handover/` and "the newest file there is what a session starts from" (`tools/claude-code/hooks/handover.sh`, header comment). The doctrine calls the next reader "a session without memory" (`docs/WORKFLOW.md`, "The eighth movement: the session handover").

**Ground truth for the three example questions lives in three different kinds of place.** "Which model repairs" is prose doctrine: the repair ladder (Codex, then Sonnet 5.5; phase-6 re-check in a fresh Codex session) is stated in `AGENTS.md` (Stage 2 paragraph) and `docs/WORKFLOW.md` §4, backed by `decisions/answers/stage2-repair/adr.yaml`. "What the verify admission's floor is" is a code constant with a stated default: 25 percent, overridable by `HARNESS_VERIFY_MEMORY_FLOOR` (`scripts/verify_lock.py`, `DEFAULT_MEMORY_FLOOR`, `FLOOR_ENV`, `configured_floor`; mirrored in `docs/WORKFLOW.md`, "One admission per user and machine"). "Where run plans live" is a convention: dated run plans under `docs/research/` (`docs/orchestration.md`, "Lanes"; examples `docs/research/2026-10-25-night-run-plan.md` and later). So "expected answers read from the live system" would draw on prose, code constants and file conventions at once — no single ground-truth format exists today.

**Existing machinery a build could sit on (facts, not a design).** Foreign models start only through `python3 scripts/stage2.py` (`scripts/stage2_session.py`, module docstring); its verbs are declared at `scripts/stage2.py` (`VERBS` mapping: explore, draft, implement, repair, review-loop, …, plus `session` and `prepare-explore` in the argparse choices). Batch model calls with no tools exist as the review loop's round-1 free swarm, run "on the implementation diff alone with no tools" (`AGENTS.md`, Stage 2; ADR 0021); the research swarm runs seats with or without tools (`scripts/stage2_swarm.py`, `scripts/stage2_research_run.py`). Interactive fresh sessions go through `stage2.py session` (`scripts/stage2_session.py`): macOS Terminal, handover text as first prompt, pinned to the change's worktree. Read-only measurement reports have a precedent in `make report` → `scripts/run_report.py` (`Makefile`, report target; `docs/orchestration.md`, "Stated, enforced, planned"). Gate wiring is derived: a new gate is a `decisions/gates.yaml` entry, and `.github/workflows/ci.yml` is regenerated from it (`decisions/gates.yaml`, header; the `ci-drift` gate holds the derivation).

## Where it lives

- Source and intent: `docs/research/2026-11-02-model-wiki-and-egm.md` (wiki table row, bead list, "Not done in this reading"); `docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md` (bead filed on request).
- The change folder: `plans/changes/outcome-test/research.md` only — the skeleton this file fills; registered in `plans/INDEX.md` (draft, bead coding-harness-3nm5).
- Gates: `decisions/gates.yaml`; nightly schedule `.github/workflows/ci.yml` (schedule + drift job); runner `scripts/ci_gates.py`.
- Session-start surface: `tools/claude-code/hooks/handover.sh`, `tools/claude-code/hooks/beads-start.sh`, `tools/claude-code/hooks/recap.sh` (maintainer's display, Haiku, German — not a measurement), `AGENTS.md`, `docs/WORKFLOW.md`.
- Recurring-job precedent: `prompts/research-recheck.md`; doctrine `docs/WORKFLOW.md`, "Recurring jobs".
- Foreign-model call machinery: `scripts/stage2.py`, `scripts/stage2_session.py`, `scripts/stage2_swarm.py`, `scripts/stage2_research_run.py`, `scripts/stage2_go.py` (the one address policy for every Go launch).
- Ground-truth loci for the example questions: `AGENTS.md` + `docs/WORKFLOW.md` §4 + `decisions/answers/stage2-repair/adr.yaml` (repair ladder); `scripts/verify_lock.py` + `docs/WORKFLOW.md` (memory floor); `docs/research/<date>-*-run-plan.md` + `docs/orchestration.md` (run plans).

## What is unclear about it

- **The bead record is not read.** The tracker is the Dolt database under `.beads/`, read only through `tools/bd` (AGENTS.md, house rules 2–3); I hold file tools and run no command, so the bead's description — which by the 2026-10-22 rule names the change's class — its priority, epic and notes are "not read", not "absent". Intent here is reconstructed from the evaluation note and the handover only.
- **Which fresh session?** The source says "a fresh session" without naming the harness. Claude Code sessions (hooks, AGENTS.md, handover trust) and foreign-model sessions (`stage2.py session`, Pi/Codex) read different context; an outcome test over one says nothing about the other. Open question for the interview.
- **Which nightly carrier?** The hosted drift job (GitHub runner: no local handover trust, no session-start hooks, and nothing I read shows a model API call from hosted CI — how a model would be called there is itself an open question) versus the machine-local night run versus a person-run job prompt. Unsettled.
- **Ground truth per question.** "Expected answers read from the live system" needs a machine-readable source per question; the three examples draw on prose doctrine, a Python constant and a file convention respectively. Which questions make the set, and where each answer is read from, is undecided in the tree.
- **Scoring and sequencing.** Pass/fail per question, and the before/after-consolidation comparison tied to bead g4iq's acceptance, are stated as intent but nothing fixes the score form, the result's landing place (night-run morning page, a dated file, a report), or whether 3nm5 waits on g4iq or runs independently — the change folder holds no decisions yet.
- **Class of this change.** Not readable here (see first bullet); it decides routing: the research swarm for `feature`/`architectural`, the single Flash explorer for `bounded`/`spike` (ADR 0020). The research skeleton carries no class header yet.
- **Not found versus not there.** A repository-wide search found no existing knowledge-measurement mechanism ("not there", grounded in the gate list and the search); whether `tools/bd prime` output contains any self-check question cannot be said without running it ("not found" — not read).

## Which files a change would have to touch

- A question-set artefact (location open — a job prompt under `prompts/` like `prompts/research-recheck.md`, or a data file beside the runner that grades it).
- The asking/grading runner — a new script under `scripts/` (precedent: `scripts/check_research_currency.py`), or an extension of the `stage2.py` verb surface for model-in-the-loop scoring.
- `decisions/gates.yaml` and the regenerated `.github/workflows/ci.yml` (the `ci-drift` gate makes hand-editing the workflow fail) if the test becomes a drift or verify gate.
- `docs/WORKFLOW.md` ("Recurring jobs" and/or a new section) and possibly `docs/orchestration.md` to state the mechanism; `AGENTS.md` only if it becomes a standing rule — its 200-line cap is held by a test (`tests/test_stage2.py`).
- `tests/` for the mechanism's own behaviour, plus the red-first rule that applies to any runner change.
- If the measurement covers the session-start path itself: `tools/claude-code/hooks/` (reinstalled via `tools/claude-code/install.sh` — never changed only in `~/.claude`).

## Neighbours

- `plans/specs/implementation-verification/spec.md` — living spec on attempt verification and derived-file preparation.
- `plans/changes/verify-machine-lock/spec.md` — the verify admission whose memory floor is one of the example questions.
- `plans/changes/research-swarm/spec.md` — the swarm call machinery and the `research-handoff` gate this research must satisfy.
- `plans/changes/research-currency/spec.md` — the nightly drift-report precedent (report-level enforcement on a schedule).
- `plans/changes/run-report/spec.md` — the read-only measurement-report precedent.
- `plans/changes/stage2-session/spec.md` — the fresh-session mechanism for foreign models.

## Draft gap check — 2026-11-06

Read at worktree input commit `86a1d919`; these checks supplement, rather
than replace, the exploration above.

- The interview now records class `bounded` and one answered maintainer
  record: eight questions, on-demand before instruction-file or
  handover-convention changes, one baseline now, and one JSONL history under
  `docs/research/` (`decisions.md#Q-1`). The record does not select a harness
  or settle whether the answering session may look up repository files.
- Current model routing is the repair row under “The routing” in
  `docs/WORKFLOW.md`: `gpt-6.1-sol`, then Sonnet 5.5 after two failed checks.
  `decisions/answers/stage2-repair/adr.yaml` instead describes the older GLM
  proposal; it is historical decision evidence, not a current answer key.
- The live floor is the literal `DEFAULT_MEMORY_FLOOR = 25.0`, its variable
  name is `FLOOR_ENV = "HARNESS_VERIFY_MEMORY_FLOOR"`, and the current reader
  is `memory_floor()` (`scripts/verify_lock.py`); the exploration's name
  `configured_floor` is not the current function name.
- The normal session-start hook can reconcile the tracker before emitting
  context (`tools/claude-code/hooks/beads-start.sh`, wired in
  `.claude/settings.json`). The measurement must not launch that hook itself
  or claim that recording a score isolates every startup side effect.
- No spec or plan for this topic exists elsewhere under `plans/specs/` or
  `plans/changes/` in the topic search. The supplied `findings.md` contains
  only the runner call audit, no phase-2a review rows to resolve.
- `templates/spec.md` and `templates/design.md` exist; there is no separate
  `templates/plan.md`, and no `scripts/validate_change_artefacts.py` exists in
  this input tree. The phase-3 prompt supplies the plan's card and ledger.
  The interview check discovers changes through their spec, so its pre-draft
  “no change folder” result measured no interview; rerun after the spec exists.
- The current branch is `feat/outcome-test`. The latest relevant handovers
  were read; the GitHub PR lookup failed for connectivity, so current PR
  state is not read. The shared tracker and live session inventory are not
  read under this attempt's worktree-only access boundary; neither is changed.
