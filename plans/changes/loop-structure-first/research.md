---
title: "Research — loop-structure-first"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-mvk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, review-loop, structure, findings]
---

# Review-loop round 1 looks at the structure of the code first — Research

Phase 1 for bead coding-harness-mvk, read on 2026-10-14 against `origin/main`
at `3199a28`. Exploration only, during the night run; the questions below
wait for the maintainer. The bead is marked "not scheduled" by the
maintainer (2026-10-12).

## Result first

- Today every round of the review loop gets the same prompt
  (`prompts/04b-review-loop.md`); the runner only adds "This is round *n*;
  you are `<model>`" (`scripts/stage2.py`, `review_loop`). Nothing in the
  prompt asks about structure; phase 6 even says the question is "not 'is
  this written cleanly'" (`prompts/06-review.md`).
- The real obstacle is not the prompt but the **evidence rule**: a loop row
  is taken only when a test demonstrates it or the spec supports it
  (`docs/WORKFLOW.md`, "The review loop (phase 4b)"). A structure finding —
  duplication, a function too long, logic in the wrong module — has neither,
  so today it is either rejected or taken as `taken — not a test`, and the
  standing rule "style rows are accepted limits" (AGENTS.md, "Findings
  returned as text") pushes it toward rejection.
- Structure findings already appear, unasked and rare: of 152 released loop
  rows in 17 `findings.md` files (`3199a28`), 10 match structure words
  (duplicated test, a second reader of `model-endpoints.yaml`, a private
  helper reached from outside), all `MINOR`/`MAINT`.
- The change is therefore three small decisions plus a prompt and runner
  change: what structure is measured **against** (recommended: the change's
  `design.md` where it has one, and the existing code's own patterns), what a
  structure row may lead to, and how it is told apart in `findings.md`.
- Relation to the swarm bead coding-harness-4fk: mvk defines a **lens**
  (what round 1 looks at); 4fk defines **who** runs a round (one rung or a
  swarm of free models). The two compose if the lens is bound to the round,
  not to a model; mvk should land first or be folded into 4fk's interview.

## What exists today

### The prompt (`prompts/04b-review-loop.md`, provenance `human-written`)

- One text for every round (lines 1-14: model, input, result, gate). The
  reviewer reports "three kinds of finding, as phase 6 does": promised and not
  done, done and not asked, and what a maintainer would trip over (error
  handling, edge cases, outward contracts, security), lines 26-30.
- Dimensions `SPEC` and `MAINT`, severities `BLOCKER`, `MAJOR`, `MINOR`
  (line 29-30). The dimension vocabulary lives in `templates/findings.md`
  ("Dimension") and `prompts/06-review.md`; `docs/WORKFLOW.md` "The findings
  process" refers to the template.
- "For the orchestrator": the evidence rule and the status forms
  `taken — <test or criterion>`, `taken — not a test — <reason>`,
  `rejected — <reason>` (lines 40-48).

### The runner (`scripts/stage2.py`)

- `review_loop`: round number = rounds run + 1; refuses past `MAX_ROUNDS = 3`
  and refuses round 3 unless round 2 wrote a taken row (`taken_in_round`);
  model = `ladder(root)[round_number - 1]`.
- The prompt is `04b-review-loop.md` read whole, then "This is round
  {n}; you are `{model}`.", `ANSWER_FORMAT`, `READ_REQUEST`, the diff,
  `READ_REQUEST` again. There is no round-specific text today.
- `parse_rows` checks a row's shape (six cells; severity only in the
  overflow case) and never the Dimension cell: a new dimension name would
  pass the runner unchanged.
- `REPAIR_FORMAT`: "A code row needs a test that fails on the baseline's
  code"; only a row taken as `taken — not a test` may be answered `not a
  test`. A pure restructuring has no red test, so it can only travel that
  way.

### The ladder and ADR 0011

- `model-endpoints.yaml`, entry `opencode-go`, `modelle`:
  `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro`. Round 1 is the
  fastest and presumably the weakest rung.
- ADR 0011 (`docs/adr/0011-stage-2-reviews-through-opencode-go.md`,
  `human-decided`) fixes the ladder, three rounds and the round-3 condition.
  It says nothing about what a round looks at; a round-1 lens changes no
  decision of it (read, decision 1-6). If the lens comes with a new
  dimension or a new status, `templates/findings.md` and `docs/WORKFLOW.md`
  change, neither of them `human-decided` (`provenance.yaml`: `templates/`
  `human-written`, `docs/WORKFLOW.md` `human-written`/`ai-drafted-reviewed`).
- `prompts/` is `human-written` (`provenance.yaml`, "prompts/"): an agent
  drafts, the maintainer's merge carries it.

### Measured on the released loop rows (`3199a28`)

- `grep "^| L[0-9]-"` over `plans/changes/**/findings.md`: 152 rows in 17
  files. Round 1: 69 rows (46 `MAINT`, 23 `SPEC`); round 2: 50; round 3: 33.
  Status words of round 1: 47 taken, 16 fixed, 6 rejected.
- Rows matching duplicate/refactor/structure/repeated/copy/same-logic words:
  10; a wider search (adding "helper", "naming", "split") shows, among
  others, `tests/test_stage2.py` (a parametrize block duplicated onto
  a helper), `scripts/stage2_runs.py` (reaching into the runner's private
  `_furniture`), `scripts/stage2_session.py` (a second reader of
  `model-endpoints.yaml`), `tests/test_check_interview_minimums.py` (two
  tests with an identical fixture). All `MINOR`, `MAINT`.

### Related beads (read 2026-10-14)

- coding-harness-dx0 (P1, open): the loop runs until a round finds nothing,
  later rounds on `mimo-v2.6-pro`, a safety cap; amends ADR 0011. Proposal
  keeps "rounds 1 and 2 as today". A structure-first round 1 makes its
  repair likely the largest of the loop, so the "until nothing found" loop
  would re-review that churn — a reason for structure **first**: correctness
  rows are then written against the code that stays.
- coding-harness-km1 (P2, open): measure OpenCode Go models as reviewers on a
  change with known findings. Its fixture could carry the structure rows
  above as known findings, so the comparison also says which model sees
  structure.
- coding-harness-4fk (P2, open): the review as a swarm of OpenCode Go models,
  the first stage always all free models; open whether the swarm replaces
  the ladder or forms its first stage; amends ADR 0011.

## How mvk relates to coding-harness-4fk

- Orthogonal axes: mvk is *what* round 1 looks at; 4fk is *who* answers a
  round and how rows are merged. If 4fk makes the swarm "the first stage",
  then the swarm *is* round 1, and the structure lens is what the swarm is
  asked.
- Two ways to combine: every swarm member gets the structure lens (more
  agreement on the same question, easier deduplication); or the swarm splits
  lenses (one member structure, others correctness) — better coverage, but
  then "structure first" becomes "structure alongside", which is the
  `[DECISION]` below.
- Order: mvk is small (prompt text, one runner line, a template line); 4fk is
  an ADR amendment with an interview. Landing mvk first gives 4fk a defined
  lens to distribute; folding it into 4fk's interview avoids touching the
  same prompt twice. Either way, mvk should not bind the lens to a model id
  (the prompt "names no model", line 8).

## Candidate approaches

1. **Round-1 section in the prompt.** A paragraph "In round 1" in
   `04b-review-loop.md`; the runner keeps sending the whole text.
   - For: no runner change; the maintainer edits one file.
   - Against: rounds 2 and 3 read the round-1 instruction too and must be
     told to ignore it; weak models follow conditional text poorly.
2. **The runner sends a round-specific focus.** The prompt holds a section
   per focus (e.g. "## Round 1: structure"); the runner includes the section
   of the current round only.
   - For: each round sees one instruction; the lens stays bound to the round,
     so a swarm (4fk) or a longer loop (dx0) inherits it.
   - Against: a small parser over the prompt file and a test; the prompt file
     gains structure the runner depends on.
3. **A separate structure round (round 0) before the ladder.**
   - For: correctness rounds unchanged.
   - Against: one more call per change, against ADR 0011's "at most three"
     — a decision PR; overlaps dx0's cap.
4. **Structure as a phase-6 concern instead.**
   - For: Codex, the strongest reviewer, sees it.
   - Against: too late — the bead asks for it first, before the correctness
     repairs.

Recommended: candidate 2, with "first focus" rather than "only focus"
(structure rows first, correctness rows still allowed).

## Which files a change would touch

- `prompts/04b-review-loop.md` (the lens text; `human-written`).
- `scripts/stage2.py` (`review_loop`: pick the round's section), with tests
  in `tests/test_stage2.py` (the prompt sent in round 1 holds the structure
  section, round 2 does not).
- `templates/findings.md` and `docs/WORKFLOW.md` ("The findings process",
  "The review loop (phase 4b)") if a dimension or a status is added.
- Possibly `prompts/06-review.md` if `STRUCT` becomes a dimension phase 6
  also uses.
- No change to ADR 0011 for candidates 1 and 2; candidate 3 amends it.

## Questions this change has to answer

- [DECISION] Is structure round 1's **only** focus or its **first** one?
  Recommendation: first — the reviewer reports structure rows first and may
  still report a correctness fault it sees; a round-1 rung that saw a
  BLOCKER and stayed silent would be a loss, and round 1 writes nearly half of
  all loop rows (69 of 152, `3199a28`).
- [DECISION] What a structure finding is measured against, so the evidence
  rule can take it. Recommendation: the change's `design.md` where it has one
  (it states boundaries and "what the architecture looks like after",
  `prompts/02b-design.md`) and the patterns of the surrounding code (an
  existing helper the change duplicates); a structure row cites one of the
  two in `Where`, and is taken as `taken — not a test — <design.md section
  or the duplicated helper>`. Without such an anchor it is rejected as today.
- [DECISION] Whether structure gets its own dimension name (e.g. `STRUCT`) in
  `findings.md`. Recommendation: yes — it lets release, phase 6 and km1 count
  structure rows and keeps them apart from `MAINT`'s error-handling view;
  the runner needs no change for it (`parse_rows` does not check the cell).
- [DECISION] Whether structure rows of severity `MINOR` stay "accepted
  limits" (AGENTS.md rule for style rows). Recommendation: a `MINOR`
  structure row is an accepted limit as today; a structure row is `MAJOR`
  only when it names a duplicated contract or logic in the wrong module that
  a later change would have to fix twice — that is what the maintainer's
  "how the code is built" is after, not naming taste.
- [GAP] Whether round 1's rung (`deepseek-v4.1-flash`) gives useful
  structure rows at all. km1's comparison on a change with known structure
  rows (the 10 above) would answer it; until then mvk is untested on the
  model that runs it.
- [GAP] How the lens reaches a swarm (4fk): same lens for all members, or one
  member per lens. Settled in 4fk's interview, not here.
- [DETAIL] The lens is bound to the round number, never to a model id, so
  reordering the ladder (`model-endpoints.yaml`) or a swarm (4fk) keeps it.
  Reason: the prompt's own rule, "this text names no model".
- [DETAIL] Structure means, for this change: module boundaries, function
  size and shape, duplication, naming, where logic sits — the bead's list,
  nothing about formatting (ruff owns that, gates `ruff-check`,
  `ruff-format`).
- [DETAIL] The repair of a structure row is answered `fixed — not a test —
  <reason>` (REPAIR_FORMAT already allows it for a row taken that way), and
  `make verify` green after it is the proof that behaviour held.
