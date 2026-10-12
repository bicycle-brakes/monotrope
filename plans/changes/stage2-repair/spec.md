---
title: "Spec — stage2-repair"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-g2f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, review-loop, repair]
class: feature
appetite: 8
change: stage2-repair
adr_question: {proposed: "yes", reason: "The change routes a new kind of stage-2 work, the repair of taken findings, to GLM 5.3 and amends the routing and the round-3 condition of ADR 0011, and the maintainer keeps model routing in ADRs (decisions.md Q-4)."}
adr_files: [docs/adr/0015-glm-5-3-repairs-taken-findings.md]
---

# Spec — `stage2-repair`

The goal in one sentence: after this change, `python3 scripts/stage2.py
repair <change>` hands every finding the orchestrator has taken — loop rows of
phase 4b and findings of phase 6 — to GLM 5.3 in one guarded call, proves each
repair of code with a test that was red first, marks each row `fixed`, and
ends in one checkpoint commit, so that no Claude sub-agent repairs findings any
more (bead `coding-harness-g2f`). Research: `research.md`. Decisions:
`decisions.md` (Q-1 to Q-5).

## Problem

- **Repairs cost Claude tokens and run outside the runner.** A Claude Sonnet
  sub-agent repairs the taken loop rows and the phase-6 findings today
  (`research.md`, opening, read 2026-10-12): its edits pass no leak check, no
  `make verify` and no checkpoint of the runner.
- **No verb repairs.** `scripts/stage2.py` dispatches eight verbs — explore,
  implement, spec-review, review-loop, release-loop, review, probe, session —
  and none of them repairs; `--stage2-off` is refused for every verb but
  explore and implement (`research.md`, "What exists today", read at
  `98808ca`).
- **A phase-6 finding cannot be taken.** The runner writes each phase-6 row
  with the Status `open`, and nothing reads a decision on it (`research.md`,
  "Where the rows a repair would consume live").
- **A repaired row has no word.** A loop row reads `taken — <test or
  criterion>` or `rejected — <reason>`. `undecided`, `taken_in_round` and the
  run count read only these two, so any third word holds the next round,
  blocks round 3 and is counted as undecided (`scripts/stage2.py`,
  `undecided` and `taken_in_round`; `scripts/stage2_runs.py`, `measure`; read
  2026-10-12).
- **"Red first" is a sentence, not a check.** The evidence rule asks for a test
  that demonstrates a finding (`prompts/04-implement.md`,
  `prompts/04b-review-loop.md`), and a model under the runner has no command
  tool to run one (`research.md`, "How `implement` runs").
- **No document routes a repair.** `docs/WORKFLOW.md` §4 and ADR 0011 route
  explore, implement, 2a, 4b and 6 and name no model for a repair
  (`research.md`, "What is unclear").

## Terms

- **Orchestrator** — the session that runs a change's verbs and decides on
  each finding.
- **Loop record** —
  `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`,
  outside the worktree; its rows are the nine-cell rows the runner reads today.
- **Released block** — in `findings.md`, the lines from a line that begins
  `## Phase 4b — loop rows, released` up to the line `Kept from the loop
  record:` or the next level-2 heading; its rows are the ten-cell lines whose
  first cell is a loop id (`L<n>-<k>`).
- **Phase-6 table** — in `findings.md`, the nine-cell table lines under a
  level-2 heading that begins `## Phase 6`, up to the next level-2 heading,
  without the table's header and separator. A line that begins with `>` is no
  table line.
- **Taken, rejected, fixed** — a row is taken when its Status begins with
  `taken`, rejected when it begins with `rejected`, fixed when it begins with
  `fixed`, each read without regard to case. A taken row is a **text row** when
  its Status begins `taken — not a test`, and a **code row** otherwise.
- **Fixed line** — one line of the model's answer:
  `<ID>: fixed — tests/<path>::<function>` or
  `<ID>: fixed — not a test — <reason>`. `tests/<path>::<function>` has the form
  of ADR 0013's criterion ledger — a file `tests/…/test_*.py`, a function
  `test_…` — and `<reason>` is not blank.
- **Baseline** — the commit `HEAD` names when the verb starts.
- **Red first** — a test named in a fixed line, run alone by pytest in a
  temporary checkout of the baseline whose `tests/` directory is the worktree's
  `tests/` as the attempt left it, exits 1 (a test failed) or 2 (collection
  failed).
- **Attempt** — one model call and the post-run checks after it.

## Acceptance criteria

### Which rows, and when the verb refuses

1. When `repair <change>` runs, each attempt's prompt lists every taken row of
   the loop record, of every released block and of every phase-6 table, each
   with its ID, Severity, Dimension, Where, Finding and Status, and lists no
   rejected and no fixed row.
   *Refuted by:* a taken row of one of the three places missing from the
   prompt, or a rejected or fixed row in it.

2. When `repair <change>` runs, each attempt's prompt holds the full
   `prompts/04-implement.md`, the repository rules of `AGENTS.md`, the change's
   `spec.md` and `plan.md`, the baseline commit and the form of a fixed line,
   and ends with the request to read nothing outside the worktree and the
   repository's git directory.
   *Refuted by:* a prompt that lacks one of these or does not end with the
   request.

3. If no taken row stands in any of the three places, the verb exits 2 and says
   that nothing is taken, before any leak check and any model call.
   *Refuted by:* a model call, an audit line, or exit 0.

4. If a row of the loop record has a Status that is neither taken, rejected nor
   fixed, or a row of a phase-6 table has a Status that is blank or begins
   `open`, the verb exits 2 and names each such ID, before any model call.
   *Refuted by:* a model call while such a row stands, or a refusal that names
   no ID.

5. If two taken rows carry the same ID, the verb exits 2 and names the ID,
   before any model call.
   *Refuted by:* a model call, or a Status written into a row the answer did
   not mean.

6. If the worktree has a change outside the change's `findings.md`, or the
   change lacks a `spec.md` with a bead, a readable `plan.md` or the heading
   `## Time used` in it, the verb exits 2 before any model call.
   *Refuted by:* a model call in one of these states.

### Routes and the call

7. While stage 2 is on, the attempts are these, in this order and no more:
   GLM 5.3 (`glm-coding-plan`, `glm-5.3`, effort `max`) on route `glm`; after
   a failed post-run check, GLM 5.3 again on route `glm-repair`; after a second
   failed post-run check, Sonnet 5.5 (`claude-code-plan`, `claude-sonnet-5-5`,
   effort `medium`) on route `stage-1`. Each later attempt's prompt carries the
   diagnostics of the attempts before it.
   *Refuted by:* a call with `glm-5.3-flash`, a fourth attempt, an attempt
   after a passing one, or a later prompt without an earlier attempt's
   diagnostics.

8. When `--stage2-off [REASON]` is given, exactly one attempt runs, Sonnet 5.5
   on route `stage-1`; no GLM key is read; and the reason stands in the
   attempt's audit line and in a route block `Stage-1 route: repair · model
   claude-sonnet-5-5 · reason: <reason>.` in `plan.md` before `## Time used`.
   *Refuted by:* a GLM call, the secrets file read, or the reason missing from
   one of the two places.

9. If stage 2 is on and the secrets file holds no `GLM_KEY`, the verb exits 2
   before any model call.
   *Refuted by:* a model call, or exit 0.

10. Before each attempt, the declaration in `model-endpoints.yaml` clears that
    attempt's endpoint and model, and the leak check passes over the change,
    the tree, the history and that attempt's exact prompt; if either fails, the
    verb exits 2 and no further attempt starts.
    *Refuted by:* a model call after a declaration that does not clear it or
    after a leak-check BLOCK, or a fallback attempt after either.

11. Each attempt appends one audit line to `findings.md`: `Stage-2 call,
    <date>: repair · attempt <n> · route <route> · endpoint <endpoint> · model
    <model>[ · reason <reason>] · leak check clean over <n> files, <n>
    commits, <n> rules.`
    *Refuted by:* an attempt without its line, or a line that
    `scripts/stage2_runs.py` does not count under the verb `repair`.

12. Each attempt starts Claude Code in the worktree with the file tools
    `Read,Grep,Glob,Edit,Write` and no command tool, `--restricted`, an empty
    standard input and the runner's allow-list environment; on the GLM routes
    every model variable names `glm-5.3`.
    *Refuted by:* `Bash` or another command tool among the tools, a caller's
    variable outside the allow-list, or a model variable that names another
    model.

13. If the loop record holds rows when the verb runs, the runner writes none of
    their text into the worktree: the rows reach the model only in its prompt.
    *Refuted by:* a file in the worktree, `findings.md` included, that holds a
    record row's Finding after a run in which the model wrote no file.

### The checks after each attempt

14. When an attempt's model returns, the runner runs `implement`'s post-run
    checks on it — the credential clean-up, the preparation of derived files,
    exactly `make verify`, and a new measured line below `## Time used` in
    `plan.md`; a failed check leaves the attempt's quoted block below its audit
    line and its diagnostics for the next attempt.
    *Refuted by:* a checkpoint after a red `make verify`, or a failed attempt
    without its block.

15. If the answer does not hold exactly one fixed line for each taken row, or
    holds a fixed line for an ID that is no taken row, the attempt fails its
    post-run checks, and its diagnostic names each such ID.
    *Refuted by:* a checkpoint with a taken row unanswered or answered twice, or
    with an unknown ID answered.

16. If a code row is answered `fixed — not a test — <reason>`, the attempt
    fails its post-run checks, and its diagnostic names the row.
    *Refuted by:* a code row whose Status reads `fixed — not a test` after a
    run.

17. If a fixed line names a test whose file holds no line that begins
    `def <function>(`, the attempt fails its post-run checks, and its
    diagnostic names the row and the test.
    *Refuted by:* a checkpoint for a row whose named test is not defined.

18. When `make verify` is green, each test that a fixed line names is run for
    red first; if it is not red first, the attempt fails its post-run checks,
    and its diagnostic names the row, the test and pytest's exit code.
    *Refuted by:* a checkpoint for a row whose named test passes on the
    baseline's code, or whose run collects no test.

19. When the red-first runs are over, the worktree's files, its index, its
    branches and the list `git worktree list` prints stand as they stood
    before them.
    *Refuted by:* a file, an index entry, a branch or a worktree entry that the
    red-first runs left behind.

20. If an attempt's model process fails, the runner restores every path except
    the change's `findings.md` to the baseline, says what it undid, and exits 1
    without a further attempt.
    *Refuted by:* a further attempt, or a path the failed attempt changed left
    in place.

### After a passing attempt

21. When every post-run check of an attempt passes, the Status of each taken
    row reads `fixed — tests/<path>::<function>` or `fixed — not a test —
    <reason>` as its fixed line says, with a `|` of the reason written `\|`, in
    the place the row stands; no other cell of any row and no other row
    changes.
    *Refuted by:* a changed `Broke a test`, `Phase 6` or `Finding` cell, a
    changed rejected row, or a Status that differs from its fixed line.

22. When every post-run check of an attempt passes, the run ends in one
    checkpoint commit: exactly one descendant of the baseline, a clean worktree
    after it, the fixed statuses of `findings.md` inside it, and the message
    `fix(<change>): repair taken findings <IDs>`.
    *Refuted by:* no commit, two commits, a dirty worktree, or a fixed status
    of `findings.md` outside the commit.

23. If no attempt passes its post-run checks, the run changed no Status in the
    loop record or in `findings.md`; and the loop record's statuses change only
    after the checkpoint commit exists.
    *Refuted by:* a Status that reads `fixed` after a run without a passing
    attempt, or a fixed record row while the commit is missing.

24. When the verb ends, it has started no review: no Codex and no Pi call
    belongs to its run.
    *Refuted by:* a `codex` or `pi` call during the run.

### The loop and the count

25. While a loop row's Status is fixed, `review-loop`, `review` and
    `release-loop` treat it as decided when its `Broke a test` is `yes` or
    `no`, and as undecided otherwise.
    *Refuted by:* a refusal that names a fixed row marked `no`, or a round or a
    release that starts while a fixed row has neither.

26. When round 2 wrote a row whose Status is now fixed, round 3 may start.
    *Refuted by:* round 3 refused as "round 2 wrote no taken row" while such a
    row stands.

27. When `scripts/stage2_runs.py` counts a change, a released loop row whose
    Status is fixed counts as taken.
    *Refuted by:* a fixed row counted as undecided, or not counted.

### The flag, the declaration and the texts

28. `--stage2-off` is accepted for explore, implement and repair, and refused
    with exit 2 for every other verb.
    *Refuted by:* a refusal for repair, or a review verb that accepts the flag.

29. `model-endpoints.yaml` keeps `glm-coding-plan` as it stands in every key but
    its remark, and the remark names `stage2.py repair` beside `stage2.py
    explore` and `stage2.py implement` and still says that no review phase
    routes to the endpoint.
    *Refuted by:* a changed model list, `darf_sehen` or residency, or a remark
    without `stage2.py repair`.

30. `docs/WORKFLOW.md` §4 names nine verbs with `repair` among them and routes
    the repair to GLM 5.3, with one GLM 5.3 repair attempt and the Sonnet 5.5
    fallback; its section on the review loop says that the orchestrator writes
    the Status, that `repair` repairs the taken rows and writes `fixed`, and
    that the orchestrator writes `Broke a test` before the next round; and
    `AGENTS.md`'s Stage-2 paragraph names `repair <change>` on GLM 5.3.
    *Refuted by:* one of the texts without the verb, or §4 still saying
    "Eight verbs exist".

31. `prompts/04b-review-loop.md` tells the orchestrator to run `python3
    scripts/stage2.py repair <change>` after writing the Status, and
    `prompts/04-implement.md` names the verb, the fixed line and that a code
    row needs a test that is red first.
    *Refuted by:* one of the two prompts without these.

32. `templates/findings.md` lists the Status words `taken — <reason>`,
    `taken — not a test — <reason>`, `fixed — tests/<path>::<function>` and
    `fixed — not a test — <reason>` for a stage-2 row.
    *Refuted by:* one of the four missing.

33. `docs/adr/0015-glm-5-3-repairs-taken-findings.md` exists in the form of
    `templates/adr.md`, states that it amends ADR 0011, and records that the
    repair of taken findings runs on GLM 5.3 and that a reviewer never repairs
    its own findings.
    *Refuted by:* the file missing, or one of the three statements missing.

## Non-goals

- **No re-check.** The verb starts no review. The orchestrator re-checks with
  the existing verbs: the loop's next round for loop rows, `review` for
  phase-6 findings (Q-3).
- **No reviewer repairs.** The rungs and Codex keep their read-only tools, and
  nothing in the review calls changes. No runner check compares a row's
  Reviewer with the repair's model: the routing holds that rule (ADR 0015).
- **`Broke a test` stays the orchestrator's.** The verb writes no `Broke a
  test` cell; the orchestrator writes it from the run's evidence before the
  next round or the release, as today.
- **No phase-2a rows.** A spec-review row goes into the spec (`in spec`), never
  to the repair.
- **No automatic pick.** No row is taken by severity or by any rule of the
  runner (Q-2).
- **No rewrite of earlier statuses.** A row decided before this change, whose
  `taken — <test>` meant "taken and repaired", keeps its words; nothing
  migrates the findings of live or archived changes, and the verb is meant for
  rows decided after it.
- **No other headings.** A phase-6 table written by hand under a heading that
  does not begin `## Phase 6` is not read.
- **`implement` unchanged.** Its routes, prompt, messages and commit message
  stay as they are; a helper both verbs share may take a parameter.
- **No new endpoint, model or residency.** `glm-5.3` is declared on
  `glm-coding-plan` already (`research.md`, "Models, endpoints").

## Protected areas

- `provenance.yaml` — the provenance map is not this change's.
- `scripts/leakcheck.py` — reused as it is.
- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` and
  `docs/adr/0011-stage-2-reviews-through-opencode-go.md` — amended by the new
  record, never edited; ADR 0011 left ADR 0007's file unchanged the same way.
- `scripts/check_decision_continuity.py` and
  `docs/architecture/2026-09-17-omnigent-first-target.md` — decision D-13 is
  not touched, so the continuity map gains nothing.
- `.claude/settings.json` — no permission changes.
- The review calls in `scripts/stage2.py` (`run_codex`, `run_reviewer`,
  `PI_TOOLS`) — a reviewer's tools stay read-only.

## Definition of Done

- `make verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md`, `AGENTS.md`,
  `prompts/04-implement.md`, `prompts/04b-review-loop.md`,
  `templates/findings.md`, the remark of `glm-coding-plan` in
  `model-endpoints.yaml`, the new
  `docs/adr/0015-glm-5-3-repairs-taken-findings.md` and the answer file
  `decisions/answers/stage2-repair/adr.yaml`; beside them only this change's
  own artefacts under `plans/changes/stage2-repair/` and `plans/INDEX.md`.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- The pull request is a decision pull request — it adds a file under
  `docs/adr/` and one under `decisions/answers/`: title
  `decide(stage2-repair): …`, label `decision`, body from
  `.github/PULL_REQUEST_TEMPLATE/decision.md`.
- Bead: the pull request closes `coding-harness-g2f`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-g2f`
  (`prompts/07-commit.md`).
- Special runs: none.

## Open decisions

None open. The maintainer's answers Q-1 to Q-5 in `decisions.md` settle the
intent; what follows are details this spec decides, each with its reason.

- [DETAIL] **The orchestrator marks a text row when it takes it**
  (`taken — not a test — <reason>`); only such a row may be answered `fixed —
  not a test`. Reason: Q-5 keeps the rule that a finding on code needs a test
  that was red first, and only a mark set before the call lets the runner hold
  it; a model's own word would let a code finding through without a test. The
  form stays within Q-2's `taken — <reason>`.
- [DETAIL] **The runner proves red first** by running the named test against
  the baseline's code with the attempt's `tests/`. Reason: the model has no
  command tool, so only the runner can show the test was red; a test of the
  new `tests/` against the old code is what "red first" means, and a real git
  checkout keeps tests that call git honest.
- [DETAIL] **`<test>` has the ledger's form** `tests/<path>::<function>`.
  Reason: Q-5 names ADR 0013's form for the text rows, and the same form lets
  the runner check that the test is defined.
- [DETAIL] **The runner writes every Status**, from the fixed lines: the
  statuses of `findings.md` before the checkpoint commit, so that the commit
  carries them; the loop record's after it. Reason: the record lies outside
  what `--restricted` file tools reach, and a Status written before the commit
  could claim a repair that never landed.
- [DETAIL] **The verb refuses** when nothing is taken, while a row is
  undecided, and on a doubled ID. Reason: one call should carry every taken
  row (Q-5's "one call clears all taken rows"), as `review-loop` and `review`
  already refuse an undecided row; a doubled ID would leave the runner unable
  to tell which row an answer means.
- [DETAIL] **Released loop rows are repaired too.** Reason: Q-1 says every
  taken loop row; after the phase-6 release the record is gone and the rows
  stand only in `findings.md`.
- [DETAIL] **A fixed row counts as taken** for the round-3 condition and the
  run count. Reason: Q-2 replaces `taken` by `fixed` after the repair, and Q-3
  keeps the loop's round budget as today; without this, repairing a round-2
  row would cancel round 3. ADR 0015 records the amendment of ADR 0011's
  decision 3.
- [DETAIL] **The prompt is `prompts/04-implement.md` with the runner's repair
  block**, not a new prompt file. Reason: the repair works under the
  implement contract — the plan is the contract, the evidence rule "holds in
  every repair round", the time log — and a second file would repeat it.
- [DETAIL] **Route names `glm`, `glm-repair`, `stage-1`; GLM 5.3 at effort
  `max`.** Reason: the shape of implement's `flash`, `flash-repair`,
  `stage-1`, and the effort the runner gave GLM 5.3 when it ran the loop
  (`scripts/stage2_runs.py`, `GLM`).
- [DETAIL] **Commit message `fix(<change>): repair taken findings <IDs>`.**
  Reason: one look at the log names the rows a repair commit closed.
- [DETAIL] **ADR number 0015.** Reason: 0014 is reserved by the open branch
  `feat/adr-owning-change` (bead coding-harness-afa).
- [DETAIL] **The header line `adr_files`.** Reason: the open change
  adr-owning-change has a change claim its ADR files under that key; the line
  is inert until that change merges and keeps this change green whichever
  merges first.
