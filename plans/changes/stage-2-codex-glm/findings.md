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

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`, criterion 36 and the `[DETAIL]` "A round has run when its rows stand in the loop record"; `plan.md`, "Decided in phase 3", `[DETAIL]` "a round is counted by its block"; `scripts/stage2.py`, `review_loop` lines 716–727 and `rounds_run` lines 594–597; `tests/test_stage2.py::test_a_round_without_a_finding_still_counts` | `[DIVERGENT]` Two artefacts answer "does a GLM call that ends successfully with no finding use up one of the two rounds?" in opposite ways. The spec: "A round has run when its rows stand in the loop record. A call that ends without rows is a failed call, not a round", so that a call without rows cannot use up one of the maintainer's two rounds. The plan, the code and a test: a successful answer writes its round block even with no row ("GLM reported no finding."), and that block counts. The case: round 1 answers "Nothing to report.", round 2 reports two rows; a third call is refused ("2 rounds have run"), where the spec's text allows it because round 1 had no rows. What a round is was ruled mechanics in phase 2a (row S-3), so this is settled by making spec and plan say the same thing, with the code and the test following the one that stays. [criterion 36] | open |
| F-2 | MAJOR | SPEC | base | `scripts/stage2.py`, `record_rows` lines 574–580, `kept_prose` lines 600–606, `release` lines 609–634 (`shutil.rmtree` at 632) | `release-loop` — and `review`, which calls the same function — carries only the table lines of the loop record that split into exactly nine cells with an `L<n>-<k>` id, drops every other table line, then deletes the record, the only copy. Two plausible inputs lose loop rows for good (measured against the stand-ins, 2026-09-30). (a) GLM writes a finding whose text holds an unescaped `\|` — a shell pipe, a regex alternation, a table cell: the row splits into seven cells, is kept in the record only inside the verbatim answer, and at release `kept_prose` drops it as a table line; `findings.md` then shows "The answer below was not only rows; it is kept as it came." with nothing below it. (b) The implementer writes a reason with a `\|` into the Status cell (`rejected — the spec says a\|b`): the row has ten cells, `record_rows` no longer sees it, so the undecided-row guard does not hold the release either; `release-loop` exits 0 with "0 loop rows appended", an empty table and "No loop row was reported.", and the record is gone. The rows are what the measurement of the first three stage-2 runs counts, so a lost `Broke a test: yes` hides the stop rule's trigger. What should hold: a table line of the record that is not a well-formed loop row refuses the release, as an undecided row does, or is carried as it stands; nothing is deleted that did not arrive in `findings.md`. [criterion 39; the `[DETAIL]` "an answer that is not table rows is appended as it came … and never dropped"; answer 5] | open |
| F-3 | MINOR | MAINT | base | `scripts/stage2.py`, `answer_block` lines 273–282 and `parse_rows` lines 240–255; `prompts/06-review.md` line 44 ("Your answer **is** the table …") and "Verdict first" | A Codex answer whose rows do not have exactly six cells is written under the sentence "Codex reported no finding.", followed by the answer as it came: a false statement at the head of the block, and no row with reviewer `Codex` for anyone who counts them. The phase-6 prompt the runner sends in full makes such an answer likely: it asks for "the table from `templates/findings.md` — columns exactly as they stand there" (a file this repository does not have; the `findings.md` Codex can read has nine or ten columns after its own phase 2a) and says a stage-2 change carries `Reviewer` and `Broke a test`, while the runner's closing paragraph asks for exactly six cells. `prompts/02a-spec-review.md` states the six cells for the Codex path; `06-review.md` does not. What should hold: an answer whose table lines are not six-cell rows is not headed "reported no finding" (F-2 is the GLM side of the same parser). [criterion 26; the `[DETAIL]` "every reviewer answers six cells"] | open |
| F-4 | MINOR | MAINT | base | `scripts/stage2.py`, `VERDICT_LINE` line 110 and `release` lines 613–614; `prompts/06-review.md`, "Verdict first"; `docs/WORKFLOW.md` §4, "The review loop" | On the Fable path the reviewer writes `Phase 6 verdict: <reviewer> <session>, <date>` by hand, and the runner accepts exactly one word before the session, one word for it, and nothing after the date. A reviewer that names itself as the doctrine does everywhere (`Phase 6 verdict: Fable 5.1 <uuid>, 2026-10-01`), has no session id to write (`Phase 6 verdict: fable, 2026-10-01`), or ends the line with a space or a full stop is refused by `release-loop` with "findings.md has no phase-6 verdict line" while a verdict line stands in the file (each form measured against the pattern, 2026-09-30). It fails closed, and the loop rows wait until someone reads the regular expression. What should hold: the prompt shows the form the runner accepts, or the refusal names the line it found and why it does not count. [criterion 38] | open |
| F-5 | MINOR | SPEC | base | `scripts/leakcheck.py`, `check`, lines 220–222 (the `is_file()` filter) | A path git lists that is a symbolic link to a directory is neither scanned nor refused, and not counted. Measured 2026-09-30 in a temporary repository: an untracked link `customer` pointing at a directory outside the repository that holds a planted match is listed by `git ls-files --others --exclude-standard`, and the check reports "leak check clean: 6 files" with exit 0 and does not name it. A reviewer reads through the link inside the worktree — the one place the prompts' request allows — so the check is green over content it never read. The same filter skips a submodule's directory. What should hold: a listed path that exists and is not a regular file is a refusal that names it ("unchecked is not clean", the check's own rule). [criterion 12] | open |
| F-6 | MINOR | MAINT | base | `scripts/leakcheck.py`, the scanned set (b) and (c), and its advice "remove or replace the value, run the check again" | Two places a reviewer reaches through git lie outside the scanned set, and the second is where the check's own advice leads. (a) The index: a value staged and then removed from the working file stays readable with `git show :<path>`; the check reads the disk and reports clean. (b) The reflog: for a match in a commit's patch the repair is rewriting that commit (amend or rebase); the check then reports clean, and `git log -g -p` still shows the value for the reflog's lifetime. Both measured in a temporary repository, 2026-09-30. The spec's non-goal names two Dolt refs as readable through git and unscanned; these two are not named, and (b) turns a found match green without removing it. What should hold: both are scanned, or the report's advice and `docs/WORKFLOW.md` §4 name them beside the Dolt refs. [the non-goal "Scanning what the repository does not present"] | open |
| F-7 | MINOR | MAINT | base | `scripts/stage2.py`, `begin_call` lines 383–399 and `append` lines 264–270; the gate `frontmatter-current` | The runner appends to `findings.md` and never touches its `updated:` line. On any day after the header's date, the first call leaves the file stale and `make verify` red: measured 2026-09-30 with a header dated 2026-09-29 and one appended call line — "plans/changes/demo/findings.md: stale", exit 1 (the gate blocks). The loop's gate is "`make verify` green after each repair", so the implementer meets a red tree the runner made; the stamp the gate names repairs it. What should hold: a file the runner writes passes the gates the repository holds it to, as criterion 21 already requires of a file the runner creates. [criterion 21] | open |
| F-8 | MINOR | MAINT | base | `docs/WORKFLOW.md` §4, "The runner is the only way", lines 594–597 | §4 states as facts that Codex "runs in the read-only sandbox with its session kept and its hooks and memories switched off" and that GLM runs with "the project's settings and hooks skipped". The maintainer's answer 10 dropped the proofs: the runner passes these settings, and nobody measured that they take effect — on `codex exec resume` in particular, whose help lists no sandbox option (research §6). The spec says "passed, not measured" in its `[DETAIL]`s and its non-goals; §4, the text a maintainer reads, presents a flag as its effect. It matters because the tracked `.codex/hooks.json` injects tracker text the leak check does not scan: if the flag does not take effect, that text reaches Codex unchecked while §4 says it cannot. What should hold: §4 says "passed, not measured" here, as it says "a request, not a lock" of the reads. [criteria 24 and 33 as changed by answer 10] | open |
| F-9 | MINOR | SPEC | base | `docs/WORKFLOW.md`, header note "Not all of it is here yet", lines 32–47 | The list, re-dated "Checked on 2026-09-30 against the tree at `3c54652`", is not exact: the file names two more pieces the tree lacks — `docs/governance/gate-catalog.md` (linked in "The five rules that make the difference") and `requirements-ci.txt` (§8) — and the sentence under the list says `.claude/settings.json` "holds only the Omnigent rules", while it holds the eight ask rules of the merge guard and now `Bash(codex *)`. All three were so on `origin/main` before this change; the change re-stamped the check without catching them. [criterion 53] | open |

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
