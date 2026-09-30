---
title: "Findings — stage-2-codex-glm"
category: findings
created: 2026-09-30
updated: 2026-09-30
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-bc9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, spec-review, stage-2, codex, glm, leak-check, model-routing]
---

# Findings — stage-2-codex-glm

Phase 2a, on commit `4fe55f5` (branch `feat/stage-2-codex-glm`, three commits
over `origin/main` at `1c708f7`; the spec is written against `ba940fb`, the
merge of pull request #54, and was read against that tree with `git show
origin/main:<path>`), 2026-09-30. The reviewer ran on Fable 5.1 in a fresh
context that never saw the author's reasoning. Read: `spec.md`,
`research.md`, `decisions.md`, the proposal the maintainer handed over,
`docs/WORKFLOW.md`, `AGENTS.md`, the nine phase prompts, `model-endpoints.yaml`
and its test, the decision-continuity gate and the two architecture documents
that carry D-13, the merge-guard rules and their test, `provenance.yaml`, the
kit and export manifests. Measured where a criterion rests on the tree: `git
status --ignored`, `git for-each-ref`, `git worktree list`, `git rev-parse
--git-common-dir`, the registry's file glob. No program of Codex or GLM was
started; no repository content left the machine.

Every row is dimension `SPEC` and answers one of the three questions of
`prompts/02a-spec-review.md`. On the coordinating session's instruction the
reviewer also did the author's step of `prompts/02-spec.md`, "After the spec
review": each row is worked into `spec.md` or rejected with its reason, and
the Status column says which. The numbering of the criteria is unchanged, so
the rows, the plan and the maintainer's reading keep their references.

**Verdict: no `[AMBIGUITY]`, no `[DIVERGENT]`, no BLOCKER.** Every answer of
`decisions.md` and every decision relayed before the interview stands in the
spec as given ("Checked without a finding" maps them). Two MAJOR and nine
MINOR: holes a builder would have filled silently, and refutations that could
not fire or could fire without a fault — all worked into the revised
`spec.md`. One summary row names the criteria a person holds. The scope
question the coordinating session asked is answered under "Scope against the
appetite", because it is not one of the three questions of this phase.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | criterion 21 (the line per call), criterion 26 (the rows), Terms "The runner" | *What is missing.* `findings.md` does not exist when the first call of a change runs: phase 2a is its first writer, and for a `feature` or `architectural` change the runner is that writer. The gate `plans-registry` (block, floor) holds every `plans/**/*.md` except `_README.md`, `INDEX.md` and `_*` to a header with `status`, `implementation_status`, `date`, `last_reviewed` and `bead` (`scripts/plans_registry.py`, `artefacts()` and `REQUIRED`, read 2026-09-30). The spec says the runner writes lines and rows into the file and never that it creates it or what header it gives it, so the builder invents the header — or leaves a file that turns `make verify` red at the next commit, in phase 4, where the spec review's own text says a hole costs twenty times more. [criteria 21, 26] | in spec — criterion 21 says the runner creates the file with a header that passes `plans-registry`, its `bead` taken from `spec.md`, and is refuted by a created file the registry blocks |
| S-2 | MAJOR | SPEC | base | Terms "Loop record", criterion 37, criterion 39 | *What is missing.* The loop record is defined as holding "the implementer's decision on each" row, and the evidence rule wants a rejected finding "with its reason" and a taken one with its `Broke a test` mark. No criterion says who writes these into the record — the implementer, by hand, in a file outside the worktree — or that `release-loop` carries them unchanged: criterion 39 is met by a row that arrives in `findings.md` without its Status. A builder could as well let the decisions be written after the release; then phase 6 would run before any record of what was taken or rejected exists, and the three measured runs (answer 5) would count from memory. [criteria 37, 39] | in spec — the Terms say the implementer writes Status, reason and mark beside each row in the loop record before the next round or the release; criterion 39 is refuted by a released row whose Status, reason or mark differs from the record's |
| S-3 | MINOR | SPEC | base | criterion 36 | *Two readings — mechanics, not intent.* "Two rounds of the loop have run" reads as two started calls, so a call that dies without rows burns one of the maintainer's two rounds; or as two rounds with rows in the record, so a dead call is a failed call and no round. "At most two rounds" is the maintainer's; what a round is, is mechanics, and the question protocol makes that a `[DETAIL]`, not an `[AMBIGUITY]` for the person. [criterion 36] | in spec — a round has run when its rows stand in the loop record; a call that ends without rows counts as no round and is visible through its line in `findings.md` (criterion 21); written into the criterion and the `[DETAIL]` list with the reason |
| S-4 | MINOR | SPEC | base | criterion 26 | *Cannot go red.* "Carries the reviewer's answer as rows" is refuted only through the session id. A runner that appends prose, or drops an answer that is not a table, meets the criterion as written; whether it parses, refuses or pastes is decided while building. [criterion 26] | in spec — refuted by a stand-in's canned answer of three table rows of which fewer than three stand in `findings.md` with reviewer `Codex`; `[DETAIL]`: an answer that is not table rows is appended as it came, under a line that says so, and never dropped |
| S-5 | MINOR | SPEC | base | criterion 22, its refutation; Non-goals, "Scanning what the repository does not present" | *What is missing.* The refutation plants the file "in a sibling directory of the repository", but the worktree sits inside the main checkout (`.claude/worktrees/<name>`; `git worktree list`, 2026-09-30), whose working tree lies above the worktree and outside `.git/` — and that is where the tracker's live database sits (`.beads/embeddeddolt/`, measured 2026-09-30). A confinement that stops at siblings but not at the parent leaves the database readable and unscanned. In the shared git directory, which the confinement includes, `refs/dolt/data-check` and `refs/remotes/origin/__dolt_remote_info__` are commits (`git for-each-ref`, 2026-09-30) that a reviewer can show through git; only the second is a remote-tracking ref the scanned set (c) reaches. The non-goal says confinement "covers the disk", and for these two places it does not say so precisely. [criterion 22] | in spec — the refutation also plants a file in the main checkout outside `.git/`, `.beads/` named; the non-goal names the two Dolt refs as readable through git and unscanned, with the measurement that the rendered tracker held no rule hit on 2026-09-30 |
| S-6 | MINOR | SPEC | base | `[GAP]` 2 (Codex hooks and memories off), criterion 24 | *What is missing.* `[GAP]` 3 says what happens when read confinement cannot be shown — stop, report, the maintainer decides. `[GAP]` 2 does not. If hooks-off cannot be shown locally, the builder alone decides whether to ship a runner whose only proof is a flag it passes, and what the tracked `.codex/hooks.json` injects (`tools/bd codex-hook SessionStart`: tracker context) then reaches Codex outside the scanned set (d), unchecked. "Unchecked is not the same as clean" (`docs/WORKFLOW.md` §4). [criterion 24] | in spec — `[GAP]` 2 carries the same stop rule as `[GAP]` 3 |
| S-7 | MINOR | SPEC | base | criterion 1, Terms "Call", the `[GAP]` list | *What is missing.* The Terms make every start of `codex exec` a call, and criterion 1 is refuted by a session file under `~/.codex/sessions` whose working directory is this worktree. The `[GAP]`s propose measuring with the real CLI against a local stand-in; run inside this worktree, such a measurement leaves exactly that session file, and the criterion goes red on the change's own proof. The spec does not say where the measurements run. [criterion 1] | in spec — every local measurement with a real CLI runs from a scratch directory outside this worktree, without repository content, under a temporary `CODEX_HOME` or `CLAUDE_CONFIG_DIR` |
| S-8 | MINOR | SPEC | base | criterion 63 | *What is missing.* "Nothing but framework content" leaves the term to the reader. `model-endpoints.yaml` defines the class `framework` as this repository — rules, templates, workflow, tests — and answer 1 reads D-13's criterion 2 as governing lakeswitch-ai's own content. This repository's artefacts cite lakeswitch-ai decisions (D-60 and RC-003 in ADR 0006); under a wider reading of "lakeswitch-ai content", the first stage-2 run over a change that cites them would first need lakeswitch's disclosure decision, which is not written (research, gaps closed, item 7). The ADR is where the term is tied to the class. [criterion 63] | in spec — criterion 63 names the definition: framework content is this repository's tree as the class `framework` defines it; lakeswitch-ai's own trees are not sent |
| S-9 | MINOR | SPEC | base | criterion 46 | *What is missing.* `docs/WORKFLOW.md` §2 opens with "each [phase] produces one versioned artefact in the repository". The artefact of phase 4b is the loop record, which lives outside the repository until the release. A row that names the record as the artefact makes §2 contradict its own first sentence — a `[DIVERGENT]` the change itself would write. [criterion 46] | in spec — the row names the loop rows as the artefact, in `findings.md` after `release-loop`, held outside the repository until the phase-6 verdict |
| S-10 | MINOR | SPEC | base | criterion 13, its refutation | *A refutation that fires without a fault.* Four consecutive letters of a 32-letter random value against the check's own output (paths, rule names, numbers): 29 four-grams against some 300 in a report make the case fire by chance in about two runs of a hundred, and a test that goes red without a fault is read past. Criterion 20 uses eight for the same purpose. [criterion 13] | in spec — eight, as in criterion 20 |
| S-11 | MINOR | SPEC | base | criterion 7, its refutation | *Two readings — wording.* "A remark that names … phase 4": the review loop is phase 4b, and a remark naming "phase 4b" names "phase 4" to a substring test, so the correct remark refutes itself. [criterion 7] | in spec — the refutation names the implement phase, not the digit |
| S-12 | — | SPEC | base | criteria 8, 47 (second refutation), 51, 53, 69, 70, 72 | *Which criterion cannot go red?* Those the spec marks as held by a person or a later phase: 8 ("as the maintainer read it" — the reviewer did not see the session), 47's "a sentence anywhere in `docs/WORKFLOW.md` or `prompts/`", 51 and 53 (a reading of §4 and the list against the tree), 69 and 70 (phase 7), 72 (house rule 1). Each is a statement of intent with a named reader, and each says so; the repository's convention (harness-decide-adr, row 2a-3) records them and does not rewrite them. Every other criterion names an input and a state that turns it red — S-4 and S-10 were the two exceptions. | answered |

Reviewer session: none fixed — a Fable 5.1 sub-agent of the coordinating
session (`session_018qxAGMFNS3mM37eUEm5DuQ`) in a fresh context. Phase 6
cannot resume it; it starts fresh on Fable 5.1, as the spec's "Order of work"
says, and `findings.md` says so then.

## Checked without a finding

- **Every decision, one by one.** Relayed before the interview: Codex
  `gpt-6.1-sol` at `max` for 2a → criteria 23, 42, 55; the same agent for 6,
  resumed → 28, 29; Sonnet 5.5 at `medium` for 4 → 43, 57; GLM 5.3 at `max`
  in a loop before 6, Sonnet adapts, at most two rounds → 32, 36, 46, 48;
  Codex reads GLM's rows only after its verdict → 30, 31, 56; Kimi dropped →
  5, 64; framework content only → 4, 63 and the non-goals. Answer 1 (D-13
  amended; criteria 3 and 4 enforced on every call, criterion 2 read as
  lakeswitch-ai's, criterion 1 replaced by three measured runs with a stop
  rule) → 16, 17, 50, 62. Answer 2 (all five packages) → the spec's sections.
  Answer 3 (the class table, unenforced) → 40, 41 and the non-goal. Answer 4
  (ADR 0007) → 62–65, 69. Answer 5 (per finding: reviewer, taken or rejected,
  broke a test; evaluation after three; fallback) → 49, 50 and the Status
  column. Answer 6 (personal-use declaration with the setting) → 8. Answer 7
  (evidence rule, every round, its consequence) → 47, 48. Answer 8 (Sonnet 5.5
  everywhere) → 43's refutation. Answer 9 (one condition per criterion, in
  `prompts/02-spec.md`, after #54) → 59 and "Order of work". No criterion
  contradicts an answer; none reopens one.
- **D-13 and the gate.** The `[DETAIL]` "no real call before the merge"
  matches the target document ("every amendment needs its ADR and rule update
  before runtime activation") and the implementation plan ("real
  foreign-model calls still require every D-13 condition … even in an
  optional trial"). Criteria 66–68 follow the path D-3, D-4, D-7 and D-17
  took: the map `AMENDMENT_ADRS`, the row, the ADR naming the id. The gate
  does not see an "Amend" row without a map entry (research §4); 66's
  refutation names the map, so the change cannot pass with the row alone.
- **D-16 ("no fixed model names in doctrine", retained).** The doctrine has
  named models since before this change; the spec adds more (42, 43, 55, 57)
  and names the reconciliation as a non-goal. Not `[DIVERGENT]` here: D-16's
  sentence stands beside "instance `model-routing.yaml` resolves phase
  requirements to declared endpoints", so it speaks of the doctrine that
  travels with the kit — and `docs/` and `prompts/` do not travel
  (`scripts/export/manifest.yaml`: `drop`), while `AGENTS.md` travels and its
  new 4b row names no model. Recorded as a reading for the maintainer, not as
  a finding.
- **The evidence rule's "the spec supports it"** has one reading: the
  reviewer measures against `spec.md` (`prompts/06-review.md`), and a
  departure from the plan is the implementer's own stop rule
  (`prompts/04-implement.md`), so a foreign finding "the plan said X" without
  a test is rejected — the consequence the maintainer accepted in answer 7.
- **The escalation sentence of §3** ("after two failed review rounds, move up
  to Fable") is about the implementer, not the reviewer; the research's open
  `[DETAIL]` (an escalation target when Codex reviews) resolves by reading.
- **The ask rule of criterion 61 fits the tree.** `tests/test_merge_guard.py`
  checks the merge rules as a subset and has a counterpart that tolerates a
  rule beside them; `omnigent_policy.py --write` keeps rules it does not own.
- **What git ignores inside this worktree** is `.pytest_cache/`,
  `.ruff_cache/` and `__pycache__/` (2026-09-30) — byte-code of this
  repository's own scripts. The gap between "readable in the worktree" and
  "scanned" holds no content today; the revised non-goal says so with the
  date. The worktree's `.beads/` (`config.yaml`, `hooks/`,
  `interactions.jsonl`, `metadata.json`, `README.md`) is tracked and scanned;
  the database is not there.
- **`AGENTS.md`** has 178 lines on `origin/main`; a row and a sentence fit
  under the 200 of `tests/test_entry_points.py`.
- **The stop rule (50)** reads one way — all of stage 2 falls back — and
  answer 5 and the implementation plan's M2 hold agree.
- **`bounded` changes:** "the GLM loop only, review on Fable" — criterion 40's
  "a spec review if one is held, on Fable" adds nothing to the decision,
  since 2a is optional (`AGENTS.md`, the one-screen table).
- **The declaration criteria 4–8** pass the vocabulary of
  `tests/test_model_endpoints.py` (`anbieter-erklaert`, `abonnement`,
  `framework`); the cap of the kit probe's exception list is the spec's
  `[DETAIL]`.
- **Criteria 15–20 and 23–35** each name a stand-in observation that turns
  them red without a foreign call; criterion 2 keeps the real programs off
  the test's path and criterion 3 keeps the real denylist and secrets out of
  the suite.

## Not checked

The behaviour of Codex CLI 0.159.2 and of Claude Code 2.1.285 under any
sandbox or permission configuration — no program of either was started, so
criteria 22, 24 and 33 rest on the `[GAP]` measurements the plan makes. The
twelve rules of the denylist and the four lines of the secrets file (not
read). The contents of `~/.codex/`, of `refs/dolt/data-check` and of
`refs/remotes/origin/__dolt_remote_info__`. OpenAI's pages on data use (the
research read search summaries). Whether Z.ai honours effort `max`.
lakeswitch-ai's tree beyond what the research read. The study behind the
addendum's point 2.

## Scope against the appetite

The research's estimate of 9–11 hours in two sessions was made for the five
work packages plus the additions it listed. The spec adds, beyond that
estimate: the scanned set (history of every branch, untracked files, the
runner's prompt texts — about half an hour over the port); `release-loop`,
the loop record outside the repository and the round counter in two places
(about an hour); the resolver and the lettered rows (half an hour); the four
local measurements of the `[GAP]`s with the real CLIs from a scratch
directory — read confinement for two programs, hooks and memories off, the
resume settings, the session-id event — one to three hours, and the one item
that can end in a `[DECISION]`; and the test counterparts
`prompts/04-implement.md` demands for the roughly thirty mechanical
criteria. Estimate after this review: **12–15 hours, two to three
sessions.** The count of 72 is not the driver: about thirty criteria are "a
sentence stands in a file" (40–59, 62–68) and cost minutes each to build —
but each costs a plan line and a review check.

Merges that lose no decision. The numbering is kept in this revision so the
rows above and the plan keep their references; the plan may group its tests
by this map, and the spec's author may apply it before phase 3:

- 4–8 → one criterion, "the declaration after this change", with the five
  parts as a list.
- 9–10 → "every named model resolves", two refutations.
- 13–14 → "the report": a match's four parts, a clean run's three numbers.
- 23–24 → "Codex's settings on every call".
- 28–29 → "phase 6 resumes phase 2a".
- 32–34 → "GLM's settings on every call".
- 37–39 → "the loop rows travel": record until release, release after the
  verdict, reviewer and marks carried.
- 40–45 → three: the class table with its caveat (40, 41), the routing rows
  (42–44), the runner sentence (45).
- 46–50 → two: the 4b row (46), the findings process (47, 49, 50); 48 with
  47.
- 51–54 → "§4, the header note and §6 state the tree", four refutations.
- 55–59 → two: the two-path prompts (55, 56), the three edited prompts (57–59).
- 62–65 → "ADR 0007's content", four refutations.
- 66–68 → "the continuity chain", three refutations.
- Dropped as criteria: 71 (the `leerprobe` gate blocks an unclassified file
  already, and the role is the `[DETAIL]`), 72 (house rule 1 holds for every
  change), 65 as its own (into 62).

Result: about forty criteria, the same substance, the same hours of
building, fewer plan lines and review checks.

**Answered by the maintainer on 2026-09-30** (`decisions.md`, answers 10 and
11, relayed by the coordinating session): the appetite stays at 9–11 hours.
The local proofs are dropped — read confinement for both programs, hooks and
memories off as a measured proof, the settings that survive `codex exec
resume` — because data protection matters for LakeSwitch's content, not for
Coding Harness's own. The customer checkout on the same disk is an accepted
residual risk; the reviewers' prompts ask them to read nothing outside the
worktree, a request and not a lock. What costs nothing stays: model, effort
and sandbox pinned, empty standard input, the session id from
`thread.started`, and the leak check before every call. The spec's criteria
22, 24 and 33 are changed accordingly and its `[GAP]`s 1–4 dropped; rows
S-5, S-6 and S-7 above concerned what was dropped, and the spec's changed
text supersedes what they put in. The merge map above is not applied: the
numbering stays for the plan's references.

## For phase 3

The plan starts from the revised `spec.md`, not from these rows. The `[GAP]`
measurements come first, because two of them (read confinement, hooks off)
can end in a stop and a `[DECISION]` for the maintainer, and a plan written
before them would be revised. *(Superseded on 2026-09-30 by answers 10 and
11: no measurement runs, so none can end in a stop.)* `plans/INDEX.md` was regenerated with
`python3 scripts/plans_registry.py --index` for this file. No pull request
was opened and nothing was written to the tracker.

## Phase 6 — review, round 1

Phase 6, round 1, on commit `317763b` (branch `feat/stage-2-codex-glm`, 18
commits over `origin/main` at `1e4cccf`, 15 of them not merges), 2026-09-30.
The reviewer ran on Opus 5.5 — the interim routing of pull request #58, which
the maintainer's answer 12 applies to this change's own review — as a
sub-agent of the coordinating session, in a fresh context that never saw the
author's reasoning. The phase-2a session (a Fable 5.1 sub-agent without a
fixed id) could not be resumed, so a fresh session reviewed. It wrote nothing
but this section and the regenerated `plans/INDEX.md`, started no program of
Codex or GLM and no `claude -p`, sent no repository content anywhere, opened
no pull request and wrote nothing to the tracker.

Yardstick: the current `spec.md` (criteria 1–72 as changed by answers 10–12)
and `decisions.md` (answers 1–14; answer 13 void by answer 14). The plan was
read for its `[DETAIL]`s, not as the yardstick. First check: each 2a row S-1
to S-11 stands in the spec as the table above says, S-5 to S-7 superseded by
answers 10 and 11 as recorded. The plan names "implementation notes" for the
mutation results and the real leak-check counts; `plan.md` has no such
section — they stand in the messages of `c7c99fc` and `317763b` and in the
docstring of `tests/test_stage2.py`. The mutations were not re-run here;
every other claim below was read in the code or measured against stand-ins
and temporary repositories built for this review.

**Verdict: one BLOCKER (`[DIVERGENT]`), one MAJOR, seven MINOR; no
`[AMBIGUITY]`.** Phase 7 does not start while F-1 is open. F-1 is a
`[DETAIL]` on both sides, so the agent settles it — no question for the
maintainer. F-2 loses loop rows for good on plausible input; it bites only
once stage 2 runs, which is after the merge. `make verify` is green at
`317763b` (2026-09-30: `VERIFY GREEN`; markdownlint reports and does not
block).

Repair round 1 (origin `fix-r1`, 2026-09-30, on `41abf42`): all nine rows are
fixed, each with a test that was red on the unrepaired tree — 29 of the 136
tests of `tests/test_stage2.py` and `tests/test_leakcheck.py` were red at
`41abf42`, all 136 are green after (`plan.md`, "Repair round 1"). F-1 is
settled by amending `spec.md` (criterion 36 and its `[DETAIL]`, the old
wording struck); the code, the plan and the test already read as the
amendment does. The decisions are the coordinating session's `[DETAIL]`s,
the reasons stand in each Status and in `plan.md`. No reviewer has read the
repair yet, and no row is marked reviewed: a re-review closes them.

Re-review of repair round 1 (2026-09-30, on `22ba651`, the repair being
`git diff 41abf42..22ba651`): an Opus 5.5 sub-agent of the coordinating
session in a fresh context, the routing on `main` (pull request #58). It
read the diff, the amended criterion 36 and the plan's "Repair round 1",
planted the fault of each row back into the code for F-1 to F-7 and restored
it, ran the new tests against `git archive 41abf42` (29 of 136 red, as
`plan.md` says), probed the repair's edges with the stand-ins, and ran `make
verify` on `22ba651` (654 passed, 15 skipped, `VERIFY GREEN`; markdownlint
reports and does not block). It started no program of Codex or GLM and no
`claude -p`, sent no repository content anywhere, changed no code and wrote
nothing to the tracker.

**Re-review verdict: F-1 to F-9 reviewed, none reopened; two new MINOR rows,
F-10 (`base`) and F-11 (`fix-r1`); no open BLOCKER.** The carried lines of
the record reach the worktree only inside the release, after its verdict
check: in a full `review` with the stand-ins, neither the verdict call's
`findings.md` nor its prompt held a marker planted in GLM's kept answer;
the marks call, after the release, did, as designed. Phase 7 may start by
the phase-6 gate (no open BLOCKER); F-10 and F-11 stay open until a repair
or phase 7 records them. If a repair of them produces a finding of its own,
that is the second round in a row with `fix-r` findings, which
`docs/WORKFLOW.md` §2 makes an escalation, not a third round. Scope was the
repair: code outside the functions it touches was not read again, and the
real programs' behaviour stays not checked, as in round 1.

Repair round 2 (origin `fix-r2`, 2026-09-30, on `8622437`): F-10 and F-11 are fixed in `022930e`, each with tests that were red on `8622437` (8 of the 149 tests of `tests/test_stage2.py` and `tests/test_leakcheck.py`; all 149 pass after, `make verify` 667 passed, 15 skipped, `VERIFY GREEN`), and the three notes the re-review left in the Status cells of F-4, F-6 and F-7 are done (`plan.md`, "Repair round 2"). No reviewer has read this round, and no row is marked reviewed. A finding that a review of it opens is the second round in a row of `fix-r` findings: `docs/WORKFLOW.md` §2 makes that an escalation to the maintainer, not a third repair round.

Re-review of repair round 2 (2026-09-30, on `bd39160`, the repair being
`git diff 8622437..bd39160`): an Opus 5.5 sub-agent of the coordinating
session in a fresh context, the routing on `main` (pull request #58). It read
the diff, the plan's "Repair round 2", criteria 36 and 39 and `decisions.md`;
ran the new tests against `git archive 8622437` (8 of 149 red, as `plan.md`
says); planted ten faults one by one in a copy of `bd39160` and restored it,
each turning its tests red (the faults of F-10, F-11, F-4, F-6 and F-7, and
five of the mechanism: the refusal of a damaged row off, the round heading no
longer ending GLM's words, the note no longer opening them, the intro dropped
inside them, their blank lines dropped); probed the repair's edges with the
stand-ins; and ran `make verify` on `bd39160` (667 passed, 15 skipped,
`VERIFY GREEN`; markdownlint reports and does not block). It started no
program of Codex or GLM and no `claude -p`, sent no repository content
anywhere, changed no code, opened or changed no pull request and wrote
nothing to the tracker.

**Re-review verdict: F-10 and F-11 reviewed, none reopened; the round-2 notes
on F-2, F-4, F-6 and F-7 reviewed; one new MINOR row, F-12 (`fix-r2`),
escalated to the maintainer; no open BLOCKER.** F-12: the named limit reaches
further than stated — after a line of GLM's shaped like a round heading, a
table line of GLM's with a loop id refuses the release again, or, with nine
cells, is released as a decided loop row. No third repair round follows
(`docs/WORKFLOW.md` §2). The order "verdict first" still holds: in a full
`review` with the stand-ins, a marker planted in GLM's kept words (a heading,
a `#` line, a table line with a loop id) was in neither the worktree nor the
`findings.md` the verdict call saw, and was in the marks call's, after the
release, as designed. Criterion 36 reads as before; the count of
heading-shaped lines as rounds is the stated part of the limit. Criterion 39
holds for the rows of the round tables the runner wrote; F-12 names the
residue. No contradiction with `decisions.md`; answer 5 is touched only by
F-12 (b). Scope was the repair: code outside the functions it touches was not
read again, and the real programs' behaviour stays not checked.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`, criterion 36 and the `[DETAIL]` "A round has run when its rows stand in the loop record"; `plan.md`, "Decided in phase 3", `[DETAIL]` "a round is counted by its block"; `scripts/stage2.py`, `review_loop` lines 716–727 and `rounds_run` lines 594–597; `tests/test_stage2.py::test_a_round_without_a_finding_still_counts` | `[DIVERGENT]` Two artefacts answer "does a GLM call that ends successfully with no finding use up one of the two rounds?" in opposite ways. The spec: "A round has run when its rows stand in the loop record. A call that ends without rows is a failed call, not a round", so that a call without rows cannot use up one of the maintainer's two rounds. The plan, the code and a test: a successful answer writes its round block even with no row ("GLM reported no finding."), and that block counts. The case: round 1 answers "Nothing to report.", round 2 reports two rows; a third call is refused ("2 rounds have run"), where the spec's text allows it because round 1 had no rows. What a round is was ruled mechanics in phase 2a (row S-3), so this is settled by making spec and plan say the same thing, with the code and the test following the one that stays. [criterion 36] | fixed in 6b6e6f6 — `[DETAIL]` of the coordinating session: the code, plan and test side stays. A call that exits 0 and answers "no finding" is a round, because the clean result is a result and not counting it would let the loop call GLM again on an unchanged tree; a call that fails (non-zero exit) or answers nothing (empty answer) is no round. `spec.md` criterion 36 and its `[DETAIL]` amended, the old wording struck and not renumbered; the empty answer, counted before, is now a failed call. Tests `test_a_no_finding_answer_is_a_round_and_a_failed_call_is_not`, `test_a_call_without_an_answer_is_not_a_round` (`plan.md`, "Repair round 1"); reviewed 2026-09-30 on `22ba651` — criterion 36 and its `[DETAIL]`, the plan, the code and the module docstring say one thing, and no other definition of a round stands in `spec.md`, `plan.md`, `docs/WORKFLOW.md` or `prompts/`. Planted faults turn the tests red: without the empty-answer check `test_a_call_without_an_answer_is_not_a_round[empty-answer]` fails; counting only rounds with rows fails four round tests |
| F-2 | MAJOR | SPEC | base | `scripts/stage2.py`, `record_rows` lines 574–580, `kept_prose` lines 600–606, `release` lines 609–634 (`shutil.rmtree` at 632) | `release-loop` — and `review`, which calls the same function — carries only the table lines of the loop record that split into exactly nine cells with an `L<n>-<k>` id, drops every other table line, then deletes the record, the only copy. Two plausible inputs lose loop rows for good (measured against the stand-ins, 2026-09-30). (a) GLM writes a finding whose text holds an unescaped `\|` — a shell pipe, a regex alternation, a table cell: the row splits into seven cells, is kept in the record only inside the verbatim answer, and at release `kept_prose` drops it as a table line; `findings.md` then shows "The answer below was not only rows; it is kept as it came." with nothing below it. (b) The implementer writes a reason with a `\|` into the Status cell (`rejected — the spec says a\|b`): the row has ten cells, `record_rows` no longer sees it, so the undecided-row guard does not hold the release either; `release-loop` exits 0 with "0 loop rows appended", an empty table and "No loop row was reported.", and the record is gone. The rows are what the measurement of the first three stage-2 runs counts, so a lost `Broke a test: yes` hides the stop rule's trigger. What should hold: a table line of the record that is not a well-formed loop row refuses the release, as an undecided row does, or is carried as it stands; nothing is deleted that did not arrive in `findings.md`. [criterion 39; the `[DETAIL]` "an answer that is not table rows is appended as it came … and never dropped"; answer 5] | fixed in 6b6e6f6 — the parser folds a pipe inside a row's last cell into the finding, the record reads its nine known cells so a pipe typed into `Status` stays in the reason, and `release-loop` carries every line of the record it does not read as a loop row before it deletes the record — GLM's words as they came, the runner's statements as they stand, everything but the record's own furniture (repair round 2 corrects the earlier "every line … as it stands", which was wider than the code: F-10): carrying, not refusing, because criterion 39 and the `[DETAIL]` "never dropped" ask that nothing be lost and a refusal would make the implementer mend the record by hand; a line of the record's own round tables with a loop id that cannot be read as a row refuses by its id (a line GLM wrote is carried, not refused: F-11). Measured: (b) reproduces for an unescaped pipe only, an escaped one already parsed. Tests `test_a_pipe_inside_a_glm_finding_reaches_findings`, `test_a_line_that_is_not_a_loop_row_is_carried_to_findings`, `test_a_pipe_in_a_status_reason_keeps_the_row_decided`, `test_a_pipe_in_a_status_reason_does_not_hide_an_undecided_row`, `test_a_damaged_loop_row_refuses_instead_of_vanishing`, `test_parse_rows_folds_a_pipe_inside_the_finding_into_it`, each red first; reviewed 2026-09-30 on `22ba651` — (a) and (b) hold. Each of the four parts turns its test red when planted out: the fold in `parse_rows`, the tenth cell in `record_rows`, the carried table lines in `kept_lines`, the refusal of a damaged loop line. Two residues are new rows: GLM's lines that start with `#` are still dropped at release (F-10), and the new refusal also fires on a line GLM wrote (F-11) — both fixed in 022930e; the round-2 correction of this Status reviewed 2026-09-30 on `bd39160` — it now says what the code carries, apart from the case F-12 names |
| F-3 | MINOR | MAINT | base | `scripts/stage2.py`, `answer_block` lines 273–282 and `parse_rows` lines 240–255; `prompts/06-review.md` line 44 ("Your answer **is** the table …") and "Verdict first" | A Codex answer whose rows do not have exactly six cells is written under the sentence "Codex reported no finding.", followed by the answer as it came: a false statement at the head of the block, and no row with reviewer `Codex` for anyone who counts them. The phase-6 prompt the runner sends in full makes such an answer likely: it asks for "the table from `templates/findings.md` — columns exactly as they stand there" (a file this repository does not have; the `findings.md` Codex can read has nine or ten columns after its own phase 2a) and says a stage-2 change carries `Reviewer` and `Broke a test`, while the runner's closing paragraph asks for exactly six cells. `prompts/02a-spec-review.md` states the six cells for the Codex path; `06-review.md` does not. What should hold: an answer whose table lines are not six-cell rows is not headed "reported no finding" (F-2 is the GLM side of the same parser). [criterion 26; the `[DETAIL]` "every reviewer answers six cells"] | fixed in 6b6e6f6 — an answer of table lines that are not six-cell rows is headed "answered in table lines that are not six-cell rows; they are kept as they came", never "reported no finding" (Codex and GLM share one function), and `prompts/06-review.md` asks for the six cells the runner asks for, naming the `findings.md` columns for the Fable path only. Tests `test_table_lines_that_are_not_rows_are_never_reported_as_no_finding`, `test_the_review_prompt_and_the_runner_ask_for_the_same_cells`, red first; reviewed 2026-09-30 on `22ba651` — without the new branch in `answer_parts` the three cases of `test_table_lines_that_are_not_rows_are_never_reported_as_no_finding` fail; the old wording of `prompts/06-review.md` fails `test_the_review_prompt_and_the_runner_ask_for_the_same_cells` |
| F-4 | MINOR | MAINT | base | `scripts/stage2.py`, `VERDICT_LINE` line 110 and `release` lines 613–614; `prompts/06-review.md`, "Verdict first"; `docs/WORKFLOW.md` §4, "The review loop" | On the Fable path the reviewer writes `Phase 6 verdict: <reviewer> <session>, <date>` by hand, and the runner accepts exactly one word before the session, one word for it, and nothing after the date. A reviewer that names itself as the doctrine does everywhere (`Phase 6 verdict: Fable 5.1 <uuid>, 2026-10-01`), has no session id to write (`Phase 6 verdict: fable, 2026-10-01`), or ends the line with a space or a full stop is refused by `release-loop` with "findings.md has no phase-6 verdict line" while a verdict line stands in the file (each form measured against the pattern, 2026-09-30). It fails closed, and the loop rows wait until someone reads the regular expression. What should hold: the prompt shows the form the runner accepts, or the refusal names the line it found and why it does not count. [criterion 38] | fixed in 6b6e6f6 — the verdict pattern takes a reviewer of several words, no session, and a space or a full stop after the date; a line that starts like a verdict and has not the form is named in the refusal; `prompts/06-review.md` states the form. Tests `test_release_accepts_the_verdict_forms_the_prompts_can_produce`, `test_a_refused_verdict_line_is_named`, red first; reviewed 2026-09-30 on `22ba651` — the old pattern fails five of the six accepted forms; the refusal that names the line is new. Noted, no row: the form without a session also takes one word as the reviewer, so `Phase 6 verdict: pending, 2026-10-01` opens the release (measured with the stand-ins); before the repair two words did the same (`not yet, <date>`), and no prompt asks for a placeholder with a date; repair round 2 (022930e): a reviewer `pending`, with or without a session and in any case, is refused (`Phase 6 verdict: pending, <date>` no longer opens the release; the refusal names the line and says `pending` is no reviewer, and `prompts/06-review.md` says it too); tests `test_a_refused_verdict_line_is_named[pending-with-a-date]` and `[pending-with-a-session]`, red on `8622437`; round-2 note reviewed 2026-09-30 on `bd39160` — removing the look-ahead from `VERDICT_LINE` turns both cases red, and `prompts/06-review.md` says `pending` is no reviewer |
| F-5 | MINOR | SPEC | base | `scripts/leakcheck.py`, `check`, lines 220–222 (the `is_file()` filter) | A path git lists that is a symbolic link to a directory is neither scanned nor refused, and not counted. Measured 2026-09-30 in a temporary repository: an untracked link `customer` pointing at a directory outside the repository that holds a planted match is listed by `git ls-files --others --exclude-standard`, and the check reports "leak check clean: 6 files" with exit 0 and does not name it. A reviewer reads through the link inside the worktree — the one place the prompts' request allows — so the check is green over content it never read. The same filter skips a submodule's directory. What should hold: a listed path that exists and is not a regular file is a refusal that names it ("unchecked is not clean", the check's own rule). [criterion 12] | fixed in 7a89f3c — a listed path that exists and is not a regular file (a link to a directory, a submodule entry, a repository nested in the tree, a special file) is a BLOCK that names it; a link with nothing behind it is scanned as its own text; a tracked file gone from the disk is no refusal (its staged deletion shows in the index scan). Tests `test_a_link_to_a_directory_is_refused_not_skipped`, `test_a_nested_repository_is_refused_not_skipped`, `test_a_dangling_link_is_read_as_its_own_text`, red first; reviewed 2026-09-30 on `22ba651` — skipping the new branch fails the three link and nested-repository tests, dropping the link-text scan fails the dangling-link test. Neither this worktree nor the main checkout lists a path that is not a regular file (measured 2026-09-30), so the new refusal blocks no call here |
| F-6 | MINOR | MAINT | base | `scripts/leakcheck.py`, the scanned set (b) and (c), and its advice "remove or replace the value, run the check again" | Two places a reviewer reaches through git lie outside the scanned set, and the second is where the check's own advice leads. (a) The index: a value staged and then removed from the working file stays readable with `git show :<path>`; the check reads the disk and reports clean. (b) The reflog: for a match in a commit's patch the repair is rewriting that commit (amend or rebase); the check then reports clean, and `git log -g -p` still shows the value for the reflog's lifetime. Both measured in a temporary repository, 2026-09-30. The spec's non-goal names two Dolt refs as readable through git and unscanned; these two are not named, and (b) turns a found match green without removing it. What should hold: both are scanned, or the report's advice and `docs/WORKFLOW.md` §4 name them beside the Dolt refs. [the non-goal "Scanning what the repository does not present"] | fixed in 7a89f3c — (a) the staged changes (`git diff --cached`) are scanned. (b) The reflog is not scanned, and the limit is stated instead: in the check's docstring (with the stash, refs outside the branches and unreachable objects) and in `docs/WORKFLOW.md` §4, and the advice for a match in a commit no longer says the value is gone after a rewrite (`git reflog expire --expire=now --all`, then `git gc --prune=now`, measured in a temporary repository on 2026-09-30). Tests `test_a_value_staged_and_then_taken_out_of_the_file_is_still_found`, `test_the_advice_does_not_claim_a_rewritten_commit_is_clean`, `test_the_limits_of_the_scanned_set_are_stated`, red first; reviewed 2026-09-30 on `22ba651` — removing the index scan fails the staged test, the old advice for a commit fails the advice test. Noted, no row: the staged test also passes with a plain `git diff` (index against the working file) in place of `--cached`; the two differ only for a `skip-worktree` or `assume-unchanged` entry (measured in a temporary repository), and the code uses `--cached`; repair round 2 (022930e): `test_the_staged_changes_are_read_against_the_last_commit_not_the_working_file` stages a value, puts the file back and marks the entry `skip-worktree` or `assume-unchanged`, where plain `git diff` shows nothing and `--cached` shows the value; a guard, green on `8622437`, and planting plain `git diff` turns both cases red; round-2 note reviewed 2026-09-30 on `bd39160` — planted again: plain `git diff` in the staged scan turns both cases red, and the test itself asserts that plain `git diff` shows nothing for the entry |
| F-7 | MINOR | MAINT | base | `scripts/stage2.py`, `begin_call` lines 383–399 and `append` lines 264–270; the gate `frontmatter-current` | The runner appends to `findings.md` and never touches its `updated:` line. On any day after the header's date, the first call leaves the file stale and `make verify` red: measured 2026-09-30 with a header dated 2026-09-29 and one appended call line — "plans/changes/demo/findings.md: stale", exit 1 (the gate blocks). The loop's gate is "`make verify` green after each repair", so the implementer meets a red tree the runner made; the stamp the gate names repairs it. What should hold: a file the runner writes passes the gates the repository holds it to, as criterion 21 already requires of a file the runner creates. [criterion 21] | fixed in 6b6e6f6 — the runner stamps `updated:` after every write to `findings.md` (`check_frontmatter_current.stamp`, the gate's own repair); the loop record has no header and gets none. Tests `test_every_write_to_findings_keeps_its_updated_stamp_current`, `test_a_findings_file_without_a_header_is_left_without_one`, the first red first; reviewed 2026-09-30 on `22ba651` — removing the stamp from `append` fails the test; the stamp in `fill_marks` has no test of its own and is redundant within one run of `review`; repair round 2 (022930e): `test_filling_the_marks_keeps_the_updated_stamp_current` calls `fill_marks` on a stale header; a guard, green on `8622437`, and removing the stamp from `fill_marks` turns it red; round-2 note reviewed 2026-09-30 on `bd39160` — planted again: without the stamp in `fill_marks` the test fails |
| F-8 | MINOR | MAINT | base | `docs/WORKFLOW.md` §4, "The runner is the only way", lines 594–597 | §4 states as facts that Codex "runs in the read-only sandbox with its session kept and its hooks and memories switched off" and that GLM runs with "the project's settings and hooks skipped". The maintainer's answer 10 dropped the proofs: the runner passes these settings, and nobody measured that they take effect — on `codex exec resume` in particular, whose help lists no sandbox option (research §6). The spec says "passed, not measured" in its `[DETAIL]`s and its non-goals; §4, the text a maintainer reads, presents a flag as its effect. It matters because the tracked `.codex/hooks.json` injects tracker text the leak check does not scan: if the flag does not take effect, that text reaches Codex unchecked while §4 says it cannot. What should hold: §4 says "passed, not measured" here, as it says "a request, not a lock" of the reads. [criteria 24 and 33 as changed by answer 10] | fixed in 7a89f3c — §4 says the settings are "configured on every call, not measured", names that the tracked `.codex/hooks.json` text would reach Codex unchecked if they are not in force, and no longer states them as facts. Test `test_section_4_says_the_foreign_settings_are_passed_not_measured`, red first; reviewed 2026-09-30 on `22ba651` — §4 no longer states the settings as facts, and no other text in `docs/`, `prompts/` or `AGENTS.md` does; the test mutates the text itself |
| F-9 | MINOR | SPEC | base | `docs/WORKFLOW.md`, header note "Not all of it is here yet", lines 32–47 | The list, re-dated "Checked on 2026-09-30 against the tree at `3c54652`", is not exact: the file names two more pieces the tree lacks — `docs/governance/gate-catalog.md` (linked in "The five rules that make the difference") and `requirements-ci.txt` (§8) — and the sentence under the list says `.claude/settings.json` "holds only the Omnigent rules", while it holds the eight ask rules of the merge guard and now `Bash(codex *)`. All three were so on `origin/main` before this change; the change re-stamped the check without catching them. [criterion 53] | fixed in 7a89f3c — trivial: the list names `docs/governance/gate-catalog.md` and `requirements-ci.txt` (checked absent at `41abf42`) and the sentence says what `.claude/settings.json` holds. No test: criterion 53 stays held by review; reviewed 2026-09-30 on `22ba651` — all nine pieces on the list are absent at `22ba651`; `.claude/settings.json` holds the rules the sentence names, beside a `SessionStart` hook, which is not a rule |
| F-10 | MINOR | SPEC | base | `scripts/stage2.py`, `kept_lines` (its test `line.startswith("#")`) and the module docstring ("it deletes nothing that has not arrived") | Lines of GLM's answer that start with `#` stand in the loop record and are lost at release. A round block keeps what is not a row "as it came", below the note, so a heading (`## Why this matters`) or a comment inside a code excerpt (`# run: grep foo \| wc -l`) is in the record; `kept_lines` skips every line that starts with `#`, meant for the record's own headings, so these lines never reach `findings.md`, and the record is deleted (measured with the stand-ins, 2026-09-30: the remark arrived, the heading and the comment did not). The behaviour predates the repair (`kept_prose` had the same test); the repair's docstring and the Status of F-2 now say every other line arrives. What should hold: only the record's own headings (`# Loop record — <change>`, `## Round <n> — GLM, <date>`) are left out, or the docstring says which lines are not carried. [the `[DETAIL]` "an answer that is not table rows is appended as it came … and never dropped"; criterion 39] | fixed in 022930e — `kept_lines` leaves out only the record's own furniture (its heading, the intro sentences where the runner wrote them, the round headings, the tables' header and separator). The lines GLM wrote are told apart from the runner's by the "not only six-cell rows" note and the next round heading (`_record_lines`) and are carried exactly as they came, blank lines between them included; the module docstring and the Status of F-2 now say so. Tests `test_every_line_of_glms_answer_reaches_findings_even_one_that_starts_with_a_hash`, `test_an_answer_without_rows_reaches_findings_as_it_came`, `test_glm_lines_that_look_like_the_records_own_text_are_carried` (the old code also removed an intro sentence GLM had quoted), each red on `8622437`; guard `test_glms_words_of_one_round_do_not_swallow_the_rows_of_the_next`; reviewed 2026-09-30 on `bd39160` — the three tests are red on `8622437`; planted in a copy of `bd39160`, skipping GLM's `#` lines turns the first two red (as the next sentence says), dropping the intro sentences also inside GLM's words turns the third red, dropping GLM's blank lines turns the second red, the note no longer opening GLM's words turns five F-10 and F-11 cases red, and the round heading no longer ending them turns the guard red. Planted back, skipping GLM's `#` lines turns the first two red. Limit, stated not fixed: a line of GLM's in the form of the record's own round heading (`## Round <n> — GLM, `) is read as one, and the answer format asks for table rows only — the limit reaches further than this says: F-12. Noted, no row: "exactly as they came, blank lines between them included" holds for an answer without rows; when the answer has rows, `parse_rows` drops GLM's blank lines and the header (first cell `ID`) and separator of a table of GLM's own before the round is written (behaviour of `answer_parts` since the build, measured with the stand-ins), so the release carries the prose without them |
| F-11 | MINOR | MAINT | fix-r1 | `scripts/stage2.py`, `record_rows` (the new refusal of a line with a loop id and fewer than nine cells) | The refusal cannot tell the runner's round table from GLM's own words kept below it. A GLM answer that holds a table line starting with a loop id and fewer than nine cells — `\| L1-1 \| still open from the last round \|`, for example in a round that runs after a release, when `findings.md` and so the diff hold released `L1-<n>` rows — is written into the record as it came, and from then on `release-loop` and `review-loop` refuse with "mend it" (measured with the stand-ins, 2026-09-30: both exit 2, the record stays, no call starts; `review` meets the same check first, read in the code). It fails closed and loses nothing, but the only way on is to edit GLM's kept answer by hand — the silent rewrite that `plan.md`, "Carry, not refuse", gives as the reason not to refuse. What should hold: the refusal reads only the rows of the round tables the runner wrote; a line of the kept answer is carried like any other. | fixed in 022930e — the record is read by who wrote a line: `record_rows`, and through it the undecided-row guard and the refusal of a damaged row in `release-loop`, `review-loop` and `review`, reads only the record's own lines, never GLM's words, which `kept_lines` carries as they came. A damaged row of the runner's round tables still refuses by its id (criterion 39). Tests `test_a_table_line_glm_wrote_with_a_loop_id_is_carried_not_refused` (one case per verb, each red on `8622437` with exit 2 and "mend it"), guard `test_a_damaged_row_of_the_record_still_refuses_beside_glm_text`; reviewed 2026-09-30 on `bd39160` — the three verb cases are red on `8622437` (exit 2, "mend it"); planted in a copy of `bd39160`, the same two plants turn the same tests red (as the next sentence says). The fix also closes a case the row did not name: a nine-cell line of GLM's with a loop id, which `8622437` released as a decided loop row, is now carried as text (measured with the stand-ins). Behind a line in the form of a round heading both come back: F-12. Planted back, reading GLM's lines as rows turns the three verb cases red; switching the refusal off turns the two damaged-row tests red |
| F-12 | MINOR | SPEC | fix-r2 | `scripts/stage2.py`, `_record_lines` (the last sentence of its docstring) and `record_rows`; `plan.md`, "Repair round 2", "Limit, stated not fixed"; the Status of F-10 | The limit that repair round 2 names is wider than its text says. Stated: a line of GLM's in the form of the record's own round heading (`## Round <n> — GLM, `) ends GLM's words, is left out, and counts as a round. Not stated: every line GLM wrote after it, up to the next real round heading, is then read as the record's own, so the separation the round built — GLM's words carried, the record's own rows decided — is undone for those lines. Measured with the stand-ins, 2026-09-30, on `bd39160`: (a) an answer of six-cell rows, then the heading-shaped line, then `\| L1-1 \| still open from the last round \|` — `release-loop` refuses with "mend it" (exit 2), the symptom of F-11; (b) the same with a nine-cell line `\| L1-7 \| note \| MAINT \| impl \| src/app.py:1 \| forged finding \| GLM \| taken — forged \| no \|` — `release-loop` exits 0, releases `L1-7` as a GLM loop row with Status `taken — forged` and `Broke a test` `no`, which the undecided-row guard took for the implementer's decision, and deletes the record; the heading-shaped line itself reaches neither the rows nor the kept text. Without the heading-shaped line both lines are carried as text, and on `8622437` both happened without it, so this is no regression: the round narrowed them to this one case and its text does not name it. The line is plausible in this change's own review: the diff GLM reads defines that heading, and an answer that shows the record's form in a code block matches it (measured: a "no finding" answer with such a block used up the second round). The reason the plan gives, "the runner cannot write a marker GLM could not also write", does not hold as stated: the runner writes the record after the answer is in hand, so it can choose a boundary the answer does not contain, or write down how many lines are GLM's. What should hold: the limit's text says that the lines after a heading-shaped line are read as the record's own, with (a) and (b) as its consequences, or the record marks the end of GLM's words in a form the answer cannot match. [criterion 39; answer 5, the per-finding record of taken and `Broke a test`; the `[DETAIL]` "an answer that is not table rows is appended as it came … and never dropped"] | open — **escalated to the maintainer**: this is the second repair round in a row with `fix-r` findings (F-11 `fix-r1`, this row `fix-r2`), which `docs/WORKFLOW.md` §2 makes an escalation, not a third repair round. No repair is asked for. (a) fails closed; (b) needs GLM to write both a heading-shaped line and a nine-cell table line with a loop id whose second cell is no severity. The maintainer decides: record the limit as it is (text only), have it closed after the merge, or hold pull request #60 for it |

Reviewer session: none — an Opus 5.5 sub-agent of the coordinating session
(`session_018qxAGMFNS3mM37eUEm5DuQ`) in a fresh context; the phase-2a
session could not be resumed, so a fresh session reviewed (answer 12).

### Checked without a finding (phase 6)

- **The leak check immediately before every call.** Both `launch` sites are
  reached only through `begin_call` in the same invocation: `spec-review`,
  the verdict call of `review`, the mark call of `review` (its own check,
  after the release) and `review-loop`. A leak planted by the verdict call's
  stand-in keeps the mark call from starting
  (`test_each_call_runs_its_own_leak_check`). A refusal exits 2 before any
  start and before `findings.md` is created (criteria 15–17).
- **The environment.** Twelve allowed names, then the call's own. Codex gets
  no credential variable and no `ANTHROPIC_*`; GLM gets the key only in
  `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY`, `glm-5.3` in all six model
  variables and the Z.ai base address. The key is scrubbed from the answer,
  the stderr tail and a start failure; the leak-check report and the call
  line carry only counts (criteria 18, 20).
- **Standard input** is `DEVNULL` for both programs, tested with a pipe that
  holds bytes (criterion 19).
- **Codex's pins.** `-m gpt-6.1-sol`, `-c model_reasoning_effort="max"`, `-c
  sandbox_mode="read-only"`, `--disable hooks`, `--disable memories`, `-o`
  to a temporary directory outside the worktree, no `--ephemeral` —
  identical on `exec` and on `exec resume <id>`; the resumed id is the last
  `Reviewer session: codex` line, and a different thread id or no recorded
  session writes the fresh-session line (criteria 23–29).
- **GLM's call.** `claude -p` with `--tools Read,Grep,Glob`, `--restricted`,
  `--strict-mcp-config`, `--permission-mode dontAsk`,
  `--no-session-persistence`, a fresh empty `CLAUDE_CONFIG_DIR` in a
  temporary directory outside the worktree, the prompt as a file holding
  `prompts/04b-review-loop.md` in full and the diff with uncommitted and
  untracked files (criteria 32–35).
- **The order "verdict first".** The loop record lies under
  `${XDG_STATE_HOME:-~/.local/state}`; the verdict prompt holds no loop row;
  `review` refuses while a row is undecided; the mark call fills only the
  `Phase 6` cells after the last release heading, and the verdict block is
  byte-equal before and after it (criteria 30, 31, 37, 38). No loop record
  exists on this machine (`~/.local/state/coding-harness/stage2/` absent,
  2026-09-30).
- **At most two rounds**, counted in the record and in every `Rounds run:`
  line a release leaves, so a release does not reset the count (criterion
  36, apart from F-1).
- **The leak check's scope and refusals.** Change folder, every tracked or
  untracked and not ignored file on disk whatever its suffix, a symbolic
  link to a file as its target's text, every commit's message and patch on
  local and remote-tracking branches with `--cc`, the prompt texts; refusal
  with the reason for a missing, empty, unreadable or invalid denylist, no
  or an invalid name, a missing or empty folder, a mode-000 file, a tree
  that cannot be listed and a history that cannot be read; the report names
  place, rule name and length, never the match or the pattern, and an
  invalid pattern by its line number only (criteria 11–14, apart from F-5
  and F-6).
- **The ask rule.** `Bash(codex *)` stands in `permissions.ask`;
  `codex_rule_problems` catches its removal and a deny or allow rule that
  covers a bare `codex`; `omnigent_policy.py --write` keeps it (it replaces
  only rules with the Omnigent prefix) and `--check` stays silent; the
  merge guard's tests still hold its eight rules in their order. The rule
  is named once, beside the runner, as the merge rules are beside the merge
  guard (criterion 61).
- **The doctrine.** §2: the 4b row and the evidence rule (46, 47). §3:
  2a and 6 on Fable 5.1 with the Codex exception, 4 on Sonnet 5.5 at
  `medium`; the interim Opus 5.5 rows of pull request #58 are gone from §3
  and from the model lines of `02a-spec-review.md` and `06-review.md`, and
  the kit keys follow (43, 44). §4: the class table and its caveat, the
  routing rows, the runner sentence, the two columns, the stop rule, reads
  as a request and not a lock (22, 40–42, 45, 49–51). §6 and the header's
  standing line (52, 54). The prompts (55–59), `AGENTS.md` (60, 184 lines).
  ADR 0007: the four parts of the amendment, the flow limited to framework
  content with its definition, Kimi, M2 (62–65); the continuity map, the
  "Amend" row and both dated notes (66–68). No added text claims that Codex
  or GLM already ran.
- **`decisions.md` against spec and code.** Answers 1–12 and 14 are carried
  as given; answer 12's fallback of a review Codex does not do to Fable 5.1
  stands in §3 and both review prompts; answer 14's routing on `main` while
  the pull request is open stands in ADR 0007's consequences. No
  contradiction with an answer; F-1 lies between spec and plan.
- **English and the probe.** Every added line is English, apart from the
  maintainer's quoted words in `decisions.md` and the German vocabulary of
  `model-endpoints.yaml` (`nicht-erklaert`); German remarks were rewritten
  only where their meaning changed (GLM's remark, the stage-2 heading). The
  probe's `REIST_NICHT` follows the renamed parametrised ids (02a and 06
  back to Fable 5.1, 04 to Sonnet 5.5) and adds one for the new 04b prompt;
  the cap rises by exactly that one (32 entries, cap 32), with its reason in
  English; `probe.py --list` names `scripts/leakcheck.py` and its test
  (71, 72).

### Not checked (phase 6)

- Criterion 1's Codex half: `~/.codex/sessions` was not read (phase 7's
  first step). Criterion 8's source: the maintainer's statement that the
  ChatGPT setting is off was not read — the repository's only trace is the
  declaration itself and the message of `e791991`. Criteria 69 and 70
  belong to phase 7.
- Any behaviour of Codex CLI or Claude Code: that the flags exist on `codex
  exec resume`, that `--disable hooks|memories`, the read-only sandbox,
  `--restricted` and `dontAsk` take effect, and that `Read`, `Grep` and
  `Glob` work under `dontAsk` with no settings loaded. No program was
  started (answer 10).
- `~/.codex/config.toml` beyond what `research.md` reports, for example
  servers it may start for a reviewer.
