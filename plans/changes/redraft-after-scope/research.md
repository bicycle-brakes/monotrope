---
title: "Research — redraft-after-scope"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-y0qm
owner: Data Architect
provenance: human-written
tags: [research]
---

# redraft after scope — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3374 commits, 12 rules.

## Runner exploration — 2026-11-06

Die Exploration ist abgeschlossen. Der folgende Text ist fertig zum Anhang an `plans/changes/redraft-after-scope/research.md` (nach der vorhandenen „Stage-2 call"-Zeile); erfasst im Worktree `.claude/worktrees/redraft-after-scope`, Zweig `spike/redraft-after-scope`, ohne Tracker-, Netz- oder Schreibzugriff.

---

## What exists today — explored 2026-11-06 (branch `spike/redraft-after-scope`, worktree `redraft-after-scope`)

### The change folder itself

- `plans/changes/redraft-after-scope/` holds exactly one artifact, `research.md` — the skeleton opened by commit `61c43439` ("open the change folder", bead coding-harness-y0qm, dated 2026-11-06). `plans/INDEX.md` lists exactly this one file for the change (entry "changes/redraft-after-scope/research.md", status draft, implementation none).
- The bead's charter is **not found** in this worktree: the tracker is the Dolt database under `.beads/` (house rule 2, `AGENTS.md`), which I did not read, and a case-insensitive grep for `redraft-after-scope|y0qm` over `docs/` matches nothing. What "scope" means for this change is therefore a human question, not a fact I can state.
- The skeleton's frontmatter declares no `class:`; the branch prefix says `spike`. The bead description, where the class is supposed to be named since 2026-10-22 (`AGENTS.md`, "A bead for a change names its class"), was not readable here. Open question for the maintainer: the class declaration.
- The skeleton asks whoever fills it with a language model to set `provenance: ai-drafted-reviewed` with `produced_by:` and `review:` (the note in `plans/changes/redraft-after-scope/research.md`; classes in `provenance.yaml`).

### Where the word "redraft" lives — and where it does not

- **Practice, not mechanism.** Case-insensitive greps for `redraft` find the word in `plans/changes/` (many changes) and in exactly four `docs/` files — `docs/adr/0023-guard-proof-for-test-only-repairs.md` (the review block), and the handover files `2026-10-14-night-run-third.md`, `2026-10-17-night-run-sixth.md`, `2026-10-29-three-lane-night.md`. It is **not there** in `docs/WORKFLOW.md`, **not there** in any file under `prompts/` (grep `redraft|re-draft|scope chang|Umfang` over `prompts/`: no matches), **not there** in `scripts/` (no match), **not there** in `templates/` (no match), and **not there** in `AGENTS.md`. No gate, validator or template knows the term; every occurrence is prose written by a change or a session.
- **"Scope" as a doctrine word** appears in two guarding places: the spec's Non-goals section exists "so that the scope does not grow during implementation" (`templates/spec.md`, Non-goals; same rule in `prompts/02-spec.md`, required section Non-goals), and decision pull requests are titled `decide(<scope>): …` (`docs/WORKFLOW.md`, the decision-PR passage; `templates/adr.md`). Neither text says what happens when the scope *does* move after drafting.

### The precedents — scope changed, artifacts were redrafted

Four completed changes record the practice; they agree with each other, but no text binds them.

- **guard-test — the stale-branch redraft.** The change lived on branch `explore/guard-test`, which fell 1199 commits behind `origin/main` (`plans/changes/guard-test/decisions.md`, "Where these answers come from"); the handover `docs/journal/handover/2026-10-29-three-lane-night.md` recommends "redraft spec and plan on current `main`, keeping the answers, instead of reviving the old branch". The maintainer decided on 2026-10-29: "spec and plan are redrafted on current main, and the answers Q-1 to Q-5 stand without a new interview" (`guard-test/decisions.md`). The executed shape: a new change folder replaces the dropped branch; `guard-test/research.md` opens with a dated "Refresh against main — 2026-10-29" appendix that names the source branch and commit (`1d6cd430`), lists "What moved since 2026-10-16" (the class moved `bounded` → `feature`, bead coding-harness-a7m closed on main, `red_first` and `fixed_test_proof` mechanics changed), and keeps the 2026-10-15/16 sections below unchanged, saying their symbol names hold "unless this section says otherwise". The old branch's spec and plan are "superseded by the redraft and serve at most as a reference for the drafter" (`guard-test/research.md`, "Not read"). ADR 0023's review block records that the maintainer "retained those answers for the feature redraft on 2026-10-29" (`docs/adr/0023`, Review). The class move is reconciled in prose: "The records still say 'class bounded' in their own text … the class is now feature" (`guard-test/decisions.md`).
- **research-swarm — scope grew through late answers, four times.** Dated redraft appendices stand in `plans/changes/research-swarm/research.md`: "Redraft repository evidence — 2026-10-15" (at `6e80ded`), "Go free-model redraft evidence — 2026-10-16" (at `6146fde`), a 2026-10-17 passage, and "Q-12 and Q-13 redraft evidence — 2026-10-18". Answers Q-7–Q-9 "supersede the old free roster and six-topic pairing" (2026-10-15 appendix); Q-10 adds Go free models; "No human answer is changed by this redraft" (2026-10-16 appendix). The spec states the convention in its Problem section: "This redraft specifies the amended behavior; existing code is an earlier slice. Historical evidence is retained in research.md; the redraft addenda record `6e80ded` … and `6146fde`" (`research-swarm/spec.md`). Phase-2a rulings were incorporated as redrafts too: "Phase 2a rulings — 2026-10-16, orchestrator (Q-10 redraft)" (`research-swarm/decisions.md`), with the repeated line "Findings rows stay unchanged; the redraft carries the rulings into the spec". The plan keeps one dated "Draft handoff" section per redraft ("Draft handoff — 2026-10-18, Q-12 and Q-13 redraft"; "Draft handoff — 2026-10-17, fifth phase-2a incorporation") in `research-swarm/plan.md`.
- **sol-effort — answers arrived after the first draft.** "Redraft evidence — 2026-10-14, at `9943b8f`" records that Q-3–Q-6 split the scope and that "the earlier observation that only two answers existed describes the earlier draft, not this redraft" (`plans/changes/sol-effort/research.md`); the plan opens "This redraft starts at `9943b8f` on `feat/sol-effort`" and keeps "Redraft checks, 2026-10-14, before the runner's post-check" (`sol-effort/plan.md`).
- **loop-until-clean — an answer arrived mid-redraft.** "Addendum 2026-10-16 — after the redraft (a0d5bc8)" records two maintainer statements that came "after the redraft had started", corrects the redraft's own wrong sentence about catalog freshness, and states "the text above stays as it was written" (`plans/changes/loop-until-clean/decisions.md`). The spec's `[DETAIL]`s record the redraft's limits: "this redraft corrects the recorded interpretation of the same runner change, without widening its budget or replacing a human answer" (`loop-until-clean/spec.md`, Open decisions).

### The invariants the precedents share (each observed, none written as a rule)

- **Answers are retained, never re-asked.** "the answers Q-1 to Q-5 stand without a new interview" (`guard-test/decisions.md`); the doctrine side already says "What is settled stays settled — a decision already made is not asked again" (`prompts/01a-interview.md`).
- **History is appended, not rewritten.** Every redraft adds a dated appendix to `research.md` naming its baseline commit; `loop-until-clean/decisions.md` keeps even the refuted sentence with the correction below it.
- **Criterion numbers and class are kept** unless a human moves them: "This redraft incorporates those rulings, retaining criterion numbers and class, without supplying a new human answer" (`research-swarm/research.md`, 2026-10-17 passage); "Keep class `feature` … without widening its budget or replacing a human answer" (`loop-until-clean/spec.md`).
- **Findings rows keep their text;** only Status/repair-location cells change (`research-swarm/plan.md`, draft handoff 2026-10-17).
- **The gates re-run on the redrafted set:** `check_interview_minimums.py`, `check_criterion_ledger.py`, `check_frontmatter_current.py`, `git diff --check` (command block in `research-swarm/plan.md`, handoff 2026-10-17; `guard-test/research.md` "Redraft gap checks — 2026-10-16" where `_counted(_parse_records(...)[0])` returns 5). The counted-answers gate is redraft-blind by construction: `scripts/check_interview_minimums.py` (docstring, "Counted means") counts `status: answered`, `answered_by: maintainer`, first occurrence — regardless of when the record was written, which is why guard-test's copied 2026-10-15/16 records satisfy the feature minimum after the redraft.
- **Class declarations must agree after a class move:** "All available declarations must agree; missing, invalid or disagreeing declarations refuse before any model call" (`prompts/01-explore.md`, routing by class; the same words in `docs/WORKFLOW.md` §4). guard-test reconciled bead versus old records in prose (`guard-test/decisions.md`).

### Adjacent mechanisms that exist today (facts a change would interact with)

- **Supersession pointers.** `status: draft | accepted | superseded`, with `supersedes`/`superseded_by` the only nullable fields; `scripts/plans_registry.py` (the `STATUS` set and the supersession checks in the registry function) blocks a pointer into nothing and demands "Whoever supersedes is superseded". `templates/spec.md` and `templates/design.md` carry both fields. What a redraft is versus a supersession is nowhere stated — "not there".
- **Anti-duplication rule.** Search `plans/specs/` and `plans/changes/` first; a matching artifact is updated, not created (`plans/_README.md`, "The rule against duplicate creation"; verbatim in `AGENTS.md` and `prompts/01-explore.md`). This run followed it: the change folder's artifact is the skeleton being filled.
- **Late-answer incorporation on the runner path.** "a second `draft <change>` does this, after the maintainer has answered every `[AMBIGUITY]` a row raised" (`prompts/02-spec.md`, "After the spec review"; `docs/WORKFLOW.md`, "The spec review improves the spec first"). The `[DECISION]` answer forms include "change criterion N to '…'" — an answer that alters an already-written criterion (`prompts/02-spec.md`).
- **Stale-base rule.** "Always from a freshly fetched `origin/main`. A worktree on a stale base …" (`docs/WORKFLOW.md`, worktree rules) — the rule whose violation produced the guard-test trigger.
- **Resume-not-repeat** for a cut-off run reuses finished contributions (`prompts/01-explore.md`, "If a run is cut off … the runner resumes") — a different mechanism from a scope redraft; it reuses work, it does not re-scope it.
- **Currency machinery covers `docs/research/` only.** `prompts/research-recheck.md` (scheduled re-check job appending Holds/Overtaken/New/Not-read addenda) and `scripts/check_research_currency.py` (lists notes with old `last_reviewed`; report-only) both operate on `docs/research/` notes. For `plans/changes/` artifacts the equivalent does not exist — **not there**.
- **Mechanical staleness is form-only.** `make staleness` / the registry DRIFT rules catch missing frontmatter, contradictory status, finished-not-archived, stale `plans/INDEX.md` (`plans/_README.md`, Frontmatter and DRIFT; `docs/WORKFLOW.md`, the staleness passage). Nothing measures that an artifact still matches its answers — **not found**: I know of no checker comparing artifact content against `decisions.md`; the precedents were aligned by hand.

### What is unclear (open questions, stated as questions, not guesses)

- What exactly does bead coding-harness-y0qm ask for — which "scope" (the spec's criteria, the class, the interview answers) and which trigger (a late answer, a stale base, a phase-2a ruling)? Not readable here; the tracker was not opened.
- Is "redraft" meant to become a defined term with one procedure (where: `docs/WORKFLOW.md`, a prompt, or a term note under `docs/glossar/` — the interview prompt's "Terms count" points term definitions there), or should the four precedents stay informally agreed practice?
- No redraft precedent exists under the current `research-handoff` regime (`scripts/check_research_handoff.py`; Basis/neighbours rules in `prompts/02-spec.md` "After a research swarm"): whether a redraft after new answers may keep the original run's claims and neighbour header, or owes a new exploration, is **not found** in any text I read — the swarm precedents predate the gate, and guard-test, the one feature-class redraft, shows no swarm run in its research.
- Is there a threshold for the stale-base trigger? The two data points are 1188 and 1199 commits behind (`docs/journal/handover/2026-10-29-three-lane-night.md`; `guard-test/decisions.md`); no number is written anywhere — **not there**.

### Which files a change would have to touch

Where the related rules live today, so the mapping is factual, not a recommendation: `docs/WORKFLOW.md` (the phase table rows for 1/1a/2, §4 stage-2 mechanics, "Which change gets what" class routing, the stale-worktree rule); `prompts/01-explore.md` (routing by class, update-not-create, resume), `prompts/01a-interview.md` (retained answers, record form, "Terms count"), `prompts/02-spec.md` ("After the spec review" second-draft rule, answer forms, Basis/neighbours), `prompts/03-plan.md` (the "Draft handoff" convention lives only in practice, e.g. `research-swarm/plan.md`); `templates/spec.md` and `templates/design.md` (`supersedes`/`superseded_by`, `class`, `neighbours`, the Non-goals fence); `plans/_README.md` (frontmatter semantics, DRIFT, duplicate-creation); `AGENTS.md` (only where a standing rule must reach every harness, per the house rule on standing rules); and the existing gates a redraft rule would meet: `scripts/check_interview_minimums.py`, `scripts/check_research_handoff.py`, `scripts/plans_registry.py`, plus derived `plans/INDEX.md` (regenerated, never hand-edited — "a stale `plans/INDEX.md` turns `make verify` red", `docs/WORKFLOW.md`).

### Neighbours (paths for the header, all read for this research)

`plans/changes/guard-test/spec.md` (exists; its decisions.md is the canonical precedent record), `plans/changes/research-swarm/spec.md`, `plans/changes/loop-until-clean/spec.md`, `plans/changes/sol-effort/spec.md`, `plans/changes/interview-context/spec.md`. Not read, therefore not neighbours: the live tracker, hosted PR state, and any artifact outside this worktree.
