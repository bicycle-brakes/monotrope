---
title: "Redrafting after a scope change — three remedies compared on five documented cases"
category: research
created: 2026-11-06
updated: 2026-11-06
last_reviewed: 2026-11-06
owner: framework-architect
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Sonnet 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-y0qm
tags: [scope, redraft, spike, workflow]
---

# Redrafting after a scope change

**Result (a proposal; the maintainer decides).** Five cases are documented. Four
(guard-test, research-swarm, sol-effort, loop-until-clean) are *artifacts that
lagged a changed scope*; one (the protected prompt edit in handoff-new-feature)
is *an edit that crossed a fence the spec already drew*. These are different
faults. A redraft rule addresses the first group and a protected-area check
addresses the second; neither covers the other. Recommendation: do not make
redrafting mandatory by gate; write the existing, already-consistent redraft
practice down as a short procedure, and treat a protected-area check as a
separate, smaller follow-up. Nothing here is adopted.

## Scope of this report

- Source review only: no live model trial, no external research, no measured
  prevention rate (spec, Non-goals). Five cases cannot support a rate.
- Read in the worktree `redraft-after-scope` on 2026-11-06 at baseline
  `3c1e2581`. A claim below names the file it rests on.
- **Not read:** the tracker (`.beads/`, so the text of bead
  `coding-harness-y0qm` itself); hosted PR state; and, for the prompt
  incident, the contents of commit `b04c119d` and of
  `plans/changes/handoff-new-feature/` — that folder is not present in this
  worktree and no command tool was available to run `git show`. The incident
  rests on one source, the reasoned interview skip
  (`plans/changes/redraft-after-scope/decisions.md`, written 2026-11-06),
  which states: the orchestrator edited `prompts/` that the spec keeps
  unchanged (loop row L6-1), and the edit was reverted in `b04c119d`. The
  row's text, the spec's exact fence and whether the edit was an authorized
  cross-folder exception are therefore **not verified here**; a reviewer with
  `git show b04c119d` should check them before the maintainer relies on case 5.

## Evidence

### Case 1 — guard-test: stale branch, answers retained (2026-10-29)

- Trigger: the branch `explore/guard-test` was 1199 commits behind
  `origin/main`; the class had moved from `bounded` to `feature` and the bead
  `coding-harness-a7m` was closed on main
  (`plans/changes/guard-test/decisions.md`, "Where these answers come from").
- Maintainer decision, 2026-10-29: spec and plan redrafted on current main;
  answers Q-1 to Q-5 "stand without a new interview" (same file).
- Executed shape: a new folder replaces the dropped branch; the old records
  are copied verbatim with their source commit (`1d6cd430`); the stale
  "class bounded" wording is reconciled in prose rather than rewritten
  (same file). ADR 0023's review block records the retention
  (`docs/adr/0023-guard-proof-for-test-only-repairs.md`, line 23).
- Lesson: the trigger was a *stale base*, not a scope-changing answer, and
  the maintainer authorized the redraft explicitly.

### Case 2 — research-swarm: scope grew through late answers (2026-10-15 to 10-18)

- Dated appendices in `plans/changes/research-swarm/research.md`: "Redraft
  repository evidence — 2026-10-15" (line 135), "Go free-model redraft
  evidence — 2026-10-16" (line 214), "Q-12 and Q-13 redraft evidence —
  2026-10-18" (line 409).
- Phase-2a rulings were folded in as redrafts
  (`plans/changes/research-swarm/decisions.md`, line 426, "Phase 2a rulings —
  2026-10-16, orchestrator (Q-10 redraft)"); the plan keeps a dated
  "Draft handoff" section per redraft (`plans/changes/research-swarm/plan.md`,
  line 1101).
- The spec states the convention: "This redraft specifies the amended
  behavior; existing code is an earlier slice" and keeps historical evidence
  in `research.md` (`plans/changes/research-swarm/spec.md`, lines 35–39).
- Lesson: four redrafts of one change, each dated and baseline-anchored,
  show the practice is stable; it also shows scope can move repeatedly.

### Case 3 — sol-effort: answers after the first draft (2026-10-14)

- `plans/changes/sol-effort/research.md`, line 129: "Redraft evidence —
  2026-10-14, at `9943b8f`". Six distinct answers existed; Q-3 to Q-6 split
  the scope. The text says "the earlier observation that only two answers
  existed describes the earlier draft, not this redraft" — history is
  qualified, not erased.

### Case 4 — loop-until-clean: an answer arrived mid-redraft (2026-10-16)

- `plans/changes/loop-until-clean/decisions.md`, line 226: "Addendum
  2026-10-16 — after the redraft (a0d5bc8)". Two maintainer statements came
  "after the redraft had started"; one of them showed that the redraft's own
  sentence about catalog freshness was wrong. The addendum states "the text
  above stays as it was written" and gives the revised detail below the
  refuted one.
- Lesson: a redraft can itself be overtaken; the append-only addendum is the
  mechanism that survived.

### Case 5 — handoff-new-feature: a protected prompt edit (2026-11-06)

- Source: only the interview skip in this change's `decisions.md` (see
  "Not read" above). Reported facts: the spec kept `prompts/` unchanged; the
  orchestrator edited a prompt anyway (row L6-1); the edit was reverted in
  `b04c119d`.
- What is *not* established: whether the spec had an authorized exception for
  a cross-folder edit (the plan for this spike asks the reviewer to separate
  "the authorized cross-folder exception from the forbidden prompt edit");
  whether the maintainer had answered anything that changed scope before the
  edit; or whether the spec was out of date. Without these, the incident
  cannot be classed as a *late scope answer* — and that is the point: the
  evidence at hand is equally consistent with a plain fence violation.

### What the current tooling measures (all observed, 2026-11-06)

- The word "redraft" appears in no gate, prompt, template or `docs/WORKFLOW.md`
  (grep over `prompts/`, `scripts/`, `templates/`: no match; see this change's
  `research.md`). It is practice carried by prose.
- `scripts/check_interview_minimums.py` counts `status: answered`,
  `answered_by: maintainer` records regardless of when written; it is blind to
  whether a spec still matches them. No checker compares artifact content
  with `decisions.md`.
- Currency machinery (`prompts/research-recheck.md`,
  `scripts/check_research_currency.py`) covers `docs/research/` only.

## Comparison

Remedies: **A** mandatory redraft after a scope-changing answer (the bead's
proposal); **B** a check on protected-area conflicts; **C** the current
review-led practice (phase 2a, phase 6 review, the maintainer's own reading).

| Dimension | A: mandatory redraft | B: protected-area check | C: current practice |
|---|---|---|---|
| Trigger | A maintainer answer or ruling that changes behavior, criteria, exclusions or permitted edit areas | Any diff touching a path the spec's protected/non-goal section names | A reviewer or the maintainer notices a mismatch |
| Detection boundary | Needs a judgment *that an answer changes scope*; only mechanical part is "a newer answer exists than the spec date" | Mechanical only if protected areas are machine-readable; today they are prose (spec "Protected areas" and Non-goals) | Whatever the reviewer reads; no systematic coverage |
| Actor | Orchestrator drafts; maintainer authorizes scope meaning | Gate or runner; orchestrator repairs | Reviewer, orchestrator, maintainer |
| Cost | One more draft round per scope answer (draft is a paid Codex call); extra review of the delta | Needs a parseable fence format plus a gate; false positives on authorized exceptions | Zero marginal; cost falls on the reviewer's attention |
| Residual risk | Over-triggering (every detail becomes a redraft); under-triggering when scope moves without a recorded answer; does nothing for a violation of an up-to-date fence | Cannot see a fence that is itself stale or missing; does not detect scope movement that stays inside allowed paths | Inconsistent; depends on who looks, when |

### Replay against the five cases

| Case | A | B | C |
|---|---|---|---|
| 1 guard-test | **Demonstrated**: this is what happened, by maintainer decision | No effect: no fence was crossed | Caught by the stale-branch observation and the handover recommendation |
| 2 research-swarm | **Demonstrated** four times, by hand | No effect | Phase 2a produced some of the rulings that triggered redrafts |
| 3 sol-effort | **Demonstrated** | No effect | Same |
| 4 loop-until-clean | **Demonstrated**, and shows a redraft may itself be overtaken; a mandatory rule must allow an addendum to a redraft | No effect | Maintainer's reading caught the wrong sentence |
| 5 handoff-new-feature | **Hypothetical and weak**: a redraft prompted by an answer would not stop an edit to a path the spec already forbade; it helps only if the fence were missing or stale — **not established** | **Hypothetical, plausible**: would flag the edit if the fence were machine-readable and no exception was recorded; the actual catch was loop row L6-1 plus manual revert | **Demonstrated**: the review loop found it and `b04c119d` reverted it |

Reading the table: A is the remedy for cases 1–4, which are already served by
a consistent *practice*; B is the only remedy aimed at case 5; C is what
actually worked in every case. No remedy is credited with preventing case 5
beyond what is shown above. With five cases and a single source for the last,
no prevention rate is claimed.

## Proposed procedure (a redraft, if the maintainer adopts one)

Distinguish what a redraft is from what it is not, using only rules the
repository already states:

- **Is a scope change:** a maintainer answer, or an orchestrator ruling the
  maintainer has not yet reversed, that changes intended behavior,
  acceptance criteria, exclusions or permitted edit areas. A proposal alone is
  not authorized by being proposed (spec, Terms).
- **Is not a scope change, so is not a redraft:**
  - an ordinary drafting detail (`[DETAIL]` — the agent decides, reason into
    the artifact; `AGENTS.md`);
  - phase-2a incorporation, which already has its own route (a second
    `draft <change>` after every `[AMBIGUITY]` is answered;
    `prompts/02-spec.md`, "After the spec review");
  - a stale-base refresh (`docs/WORKFLOW.md`, worktree rules), which moves the
    baseline, not the intended behavior — though case 1 shows the two can
    arrive together;
  - resuming an interrupted exploration, which reuses finished contributions
    and does not re-scope (`prompts/01-explore.md`).
- **Steps for a real scope change:**
  1. Record the answer in `decisions.md` as stated (never one of the
     agent's own; `AGENTS.md`, house rule 8) and date it.
  2. Redraft spec, and plan (and design where the class requires it), anchored
     to a named baseline commit, in a dated appendix or "Draft handoff"
     section, as in cases 2 and 3.
  3. Retain every earlier answer; do not re-run the interview for them
     (`prompts/01a-interview.md`; case 1).
  4. Do not rewrite history: a superseded sentence stays with the correction
     below it (case 4).
  5. Keep criterion numbers and class unless the maintainer moves them; a
     class move reconciles all declarations (`prompts/01-explore.md`).
  6. Keep findings rows' text; change only their status cells
     (`plans/changes/research-swarm/plan.md`, handoff of 2026-10-17).
  7. Re-run the existing gates on the redrafted set
     (`check_interview_minimums.py`, `check_criterion_ledger.py`,
     `check_frontmatter_current.py`, `git diff --check`).
  8. Recheck: a fresh review of the delta before implementation continues.
- **Obligations that survive a redraft:** the interview minimum for the
  (possibly new) class, and, for a `feature`/`architectural` change that ran
  the research swarm, the gate `research-handoff` (Basis and neighbours,
  `prompts/02-spec.md`, "After a research swarm"). Whether a redraft after new
  answers may keep the original run's claims and neighbour header or owes a
  new exploration is **not decided by any text read**; no precedent exists
  under the current regime (this change's `research.md`). The proposal does
  not assume the obligation disappears; it leaves the question to the
  maintainer.

## Recommendation

1. **Adopt, as documentation only, the redraft procedure above** — the eight
   steps and the four non-redraft cases — in one place (candidate:
   `prompts/02-spec.md` or `docs/WORKFLOW.md`, §4). Basis: cases 1–4 are
   consistent in shape and no case shows harm from the practice; what they
   lack is a stated trigger and a stated "is not". This traces to the
   comparison: A's demonstrated value is in cases 1–4, and its cost is
   lowest as a written procedure rather than a gate.
2. **Do not add a mechanical "answer newer than spec" gate now.** The
   detection boundary of A needs a judgment about meaning that no existing
   script makes; a date comparison would over-trigger on details and
   under-trigger on unrecorded scope movement.
3. **Treat B as a separate, smaller follow-up** only if the maintainer wants
   case 5 prevented rather than caught: it needs a machine-readable
   "protected areas" form in the spec first.

**Uncovered case (limit).** The preferred remedy (a written procedure) does
not cover case 5 and any like it: an orchestrator edits a protected path while
the spec is current. Nor does it cover scope that moves with no recorded
answer, which no remedy here detects. It also leaves open the
research-swarm handoff question above.

**Proposed follow-up (for the maintainer to authorize):**

- Affected paths: `prompts/02-spec.md` and/or `docs/WORKFLOW.md` (one
  paragraph and a short list); optionally a term note under `docs/glossar/`.
  No script, template or gate.
- Class: `bounded` (documentation of existing practice). If B is also wanted:
  `feature`, touching `templates/spec.md`, a new check script and its test.
- ADR implications: none for the procedure as documentation. A gate would
  change what `AGENTS.md` and `docs/WORKFLOW.md` promise and should be checked
  against existing ADRs before drafting; not assessed here.
- **Remaining maintainer choice:** adopt the written procedure (yes/no);
  whether B is wanted; and the swarm-handoff question (may a redraft keep the
  original Basis/neighbour header?).

## Limits

- Five cases, one of them from a single secondary source that this report
  could not check against git (see "Not read").
- Historical observations are dated to the cited files and baseline
  `3c1e2581`; the counts (1199 commits behind) are as the source states them
  and were not re-measured.
- The bead's own wording was not readable; if it names a trigger or scope
  beyond what the interview skip quotes, this comparison may miss it.
- Nothing here changes workflow instructions, runner behavior, gates,
  templates or ADRs, and no maintainer answer is recorded as settled.
