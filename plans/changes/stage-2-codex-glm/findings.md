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

## For phase 3

The plan starts from the revised `spec.md`, not from these rows. The `[GAP]`
measurements come first, because two of them (read confinement, hooks off)
can end in a stop and a `[DECISION]` for the maintainer, and a plan written
before them would be revised. `plans/INDEX.md` was regenerated with
`python3 scripts/plans_registry.py --index` for this file. No pull request
was opened and nothing was written to the tracker.
