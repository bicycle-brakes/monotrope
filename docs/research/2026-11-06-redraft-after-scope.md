---
title: "Redrafting after a scope change — three remedies compared on five documented cases"
category: research
created: 2026-11-06
updated: 2026-11-07
last_reviewed: 2026-11-06
owner: framework-architect
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: [{kind: llm-session, name: claude-code, version: "Sonnet 5.5, 2026-11-06"}, {kind: llm-session, name: stage2-runner, model: gpt-6.1-sol, version: "repair, 2026-11-07"}]
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-y0qm
tags: [scope, redraft, spike, workflow]
---

# Redrafting after a scope change

**Result (a proposal; the maintainer decides).** Five cases are documented,
including the protected-prompt incident checked against Git on 2026-11-07.
Cases 2–4 (research-swarm, sol-effort, loop-until-clean) show redrafting after
late answers or rulings; case 1 (guard-test) is a stale-base redraft expressly
authorized by the maintainer. Case 5 is an orchestrator edit that crossed an
existing protected-area fence, subsequently reverted. Mandatory redrafting
after a scope-changing answer does not cover the stale-base trigger or the
protected-path violation. Recommendation: document the observed redraft
procedure without adding a date gate, and consider protected-area checking
as a separate follow-up. Nothing here is adopted.

## Scope of this report

- Source review only: no live model trial, no external research, no measured
  prevention rate (spec, Non-goals). Five cases cannot support a rate.
- Read in the worktree `redraft-after-scope` on 2026-11-06 at baseline
  `3c1e2581`. A claim below names the file it rests on.
- Repair source review on 2026-11-07 at `5035bad0` additionally read
  `git show b04c119d`, the handoff-new-feature spec and decisions at that
  revision, introducing commit `24371185` and its spec, and
  `docs/journal/handover/2026-11-06-heartbeat-night.md`, Validation,
  lines 160–161. These close the initial file-only attempt's incident gap.
- **Not read:** the tracker (`.beads/`, including the bead's own wording)
  and hosted PR state. The original loop row L6-1 text was not found in the
  historical findings file read at `b04c119d`; the revert commit names it.

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
- Lesson: three answer-triggered redrafts (Q-7–Q-9 on 2026-10-15, Q-10 on
  2026-10-16, Q-12/Q-13 on 2026-10-18), each dated and baseline-anchored, show
  the practice is stable; the phase-2a incorporations of 2026-10-16/17
  (rulings S-21–S-30, "without supplying a new human answer") fall outside
  A's trigger. Scope can move repeatedly.

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

- `24371185` (2026-11-06) adds seven lines about
  `research_swarm_exception` to `prompts/01a-interview.md`. Its message calls
  this an orchestrator hand edit for loop row L5-5, taken outside the runner
  because prompts are outside its write set. It was not a runner repair edit.
- `b04c119d` (2026-11-06) removes exactly those lines. Its message cites
  loop row L6-1, rejects L5-5 for this change and defers prompt documentation
  to follow-up work. This verifies the edit and revert, though not the
  original L6-1 wording, which was not found in the historical findings file.
- `plans/changes/handoff-new-feature/spec.md` at both commits explicitly
  keeps prompts unchanged. At `b04c119d`, its Protected areas and
  `decisions.md#Q-2` authorize a different cross-folder edit: the orchestrator
  may record structured exception Q-6 in
  `plans/changes/go-access-point/decisions.md`, confirmed by the maintainer
  on 2026-11-04. That exception does not permit editing a prompt.
- A second dated narrative source,
  `docs/journal/handover/2026-11-06-heartbeat-night.md`, Validation,
  lines 160–161 at `5035bad0`, records the prompt edit's targeted tests and
  revert because the spec protects prompts. The interview skip in this
  change's `decisions.md` (2026-11-06) agrees with it.
- Lesson: the historical spec already drew the fence when the edit was
  made. The checked sources establish a protected-area violation; they do
  not establish a late scope answer as its cause.

### What the current tooling measures (2026-11-06; handoff check re-read 2026-11-07)

- The word "redraft" appears in no gate, prompt, template or `docs/WORKFLOW.md`
  (grep over `prompts/`, `scripts/`, `templates/`: no match; see this change's
  `research.md`). It is practice carried by prose.
- `scripts/check_interview_minimums.py` counts `status: answered`,
  `answered_by: maintainer` records regardless of when written; it is blind to
  whether a spec still matches them semantically.
- `scripts/check_research_handoff.py` already links spec content to answers
  for changes with complete swarm runs: `_bases` requires every criterion's
  `*Basis:*` to reference answered Q-records in that change's `decisions.md`
  or supported run claims; `_parity` holds `neighbours:` to run paths and
  maintainer keep/add/drop records (read at `5035bad0`, 2026-11-07).
  This is structural criterion-to-answer and path linkage. These checks do
  not determine whether criterion prose semantically agrees with an answer;
  a proposed follow-up would extend existing linkage, not start from none.
- Currency machinery (`prompts/research-recheck.md`,
  `scripts/check_research_currency.py`) covers `docs/research/` only.

## Comparison

Remedies: **A** mandatory redraft after a scope-changing answer (the bead's
proposal); **B** a check on protected-area conflicts; **C** the current
review-led practice (phase 2a, phase 6 review, the maintainer's own reading).

| Dimension | A: mandatory redraft | B: protected-area check | C: current practice |
|---|---|---|---|
| Trigger | A maintainer answer or ruling that changes behavior, criteria, exclusions or permitted edit areas | Any diff touching a path the spec's protected/non-goal section names | A reviewer or the maintainer notices a mismatch |
| Detection boundary | Needs a judgment *that an answer changes scope*; a date comparison would detect chronology only; existing Basis/neighbour checks provide structural linkage for complete swarm runs, not semantic scope detection | Mechanical only if protected areas are machine-readable; today they are prose (spec "Protected areas" and Non-goals) | Whatever the reviewer reads; no systematic coverage |
| Actor | Orchestrator drafts; maintainer authorizes scope meaning | Gate or runner; orchestrator repairs | Reviewer, orchestrator, maintainer |
| Cost | One more draft round per scope answer (draft is a paid Codex call); extra review of the delta | Needs a parseable fence format plus a gate; false positives on authorized exceptions | Zero marginal; cost falls on the reviewer's attention |
| Residual risk | Over-triggering (every detail becomes a redraft); under-triggering when scope moves without a recorded answer; does nothing for a violation of an up-to-date fence | Cannot see a fence that is itself stale or missing; does not detect scope movement that stays inside allowed paths | Inconsistent; depends on who looks, when |

### Replay against the five cases

| Case | A | B | C |
|---|---|---|---|
| 1 guard-test | **Outside A's trigger**: a maintainer-authorized stale-base redraft, not a scope-changing answer | No effect: no fence was crossed | Caught by the stale-branch observation and the handover recommendation |
| 2 research-swarm | **Demonstrated** three times, by hand (answer-triggered); the phase-2a incorporations are **outside A's trigger** | No effect | Phase 2a produced the rulings that triggered the other redrafts |
| 3 sol-effort | **Demonstrated** | No effect | Same |
| 4 loop-until-clean | **Demonstrated**, and shows a redraft may itself be overtaken; a mandatory rule must allow an addendum to a redraft | No effect | Maintainer's reading caught the wrong sentence |
| 5 handoff-new-feature | **Hypothetical and weak**: a redraft prompted by an answer would not stop an edit to a path the spec already forbade; it helps only if the fence were missing or stale — **not established** | **Hypothetical, plausible**: would flag the edit if the fence were machine-readable and no exception was recorded; the actual catch was loop row L6-1 plus manual revert | **Demonstrated**: the review loop found it and `b04c119d` reverted it |

Reading the table: cases 2–4 demonstrate manual redrafting after late
answers or rulings. Case 1 supplies evidence for retaining answers during an
explicitly authorized stale-base redraft, but does not demonstrate A's trigger.
B targets case 5; C detected the protected-path violation and the revert
corrected it, as the checked commits show. B's prevention remains hypothetical.
No prevention rate is claimed from these five historical cases.

## Proposed procedure (a redraft, if the maintainer adopts one)

Distinguish what a redraft is from what it is not, using only rules the
repository already states:

- **Is a scope change:** a proposed or maintainer-answered change to intended
  behavior, acceptance criteria, exclusions or permitted edit areas (spec,
  Terms). A proposal is not authorized by being proposed: record it as pending
  and obtain maintainer authority before implementing its changed intent.
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
     agent's own; `prompts/01a-interview.md`, record form
     `answer: <the answer, as stated>`) and date it. An unanswered proposal
     remains pending; do not invent an answer to advance the redraft.
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
   `prompts/02-spec.md` or `docs/WORKFLOW.md`, §4). Basis: cases 2–4 show
   manual redrafting after late answers or rulings. Case 1 supports answer
   retention under a separately authorized stale-base refresh, not A's
   scope-answer trigger. Document that boundary with the procedure; the
   cases demonstrate practice, not measured prevention by a mandatory rule.
2. **Do not add a mechanical "answer newer than spec" gate now.** The
   detection boundary of A needs a judgment about meaning that no existing
   script makes. Existing Basis/neighbour linkage checks references for
   complete swarm runs, not semantic agreement; a date comparison would
   over-trigger on details and under-trigger on unrecorded scope movement.
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

- Five historical cases, not controlled prevention trials. Case 5 is now
  checked against the introducing and reverting commits, the historical spec
  and decisions, and a dated handover. The original L6-1 row wording remains
  unverified; its attribution is supplied by the revert message.
- Historical observations are dated to the cited files and baseline
  `3c1e2581` and the repair baseline `5035bad0` as identified above. The count
  of 1199 commits behind is as the source states it and was not re-measured.
- The bead's own wording was not readable; if it names a trigger or scope
  beyond what the interview skip quotes, this comparison may miss it.
- Nothing here changes workflow instructions, runner behavior, gates,
  templates or ADRs, and no maintainer answer is recorded as settled.
