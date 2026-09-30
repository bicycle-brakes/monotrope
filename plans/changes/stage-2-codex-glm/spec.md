---
title: "Spec — stage-2-codex-glm"
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-bc9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, codex, glm, leak-check, model-routing, adr]
class: architectural
---

# Spec — stage-2-codex-glm

Models from two other vendors review Coding Harness changes before the merge,
and only framework content leaves the machine (bead coding-harness-bc9).
Research: `research.md` — its sections "Corrections after verification" and
"Gaps closed in phase 2" hold where they disagree with the text above them.
Decisions: `decisions.md` (interview of 2026-09-30). Every answer there is
taken as given; none is reopened here.

Revised after phase 2a on 2026-09-30 (`findings.md`, rows S-1 to S-12): two
holes closed in the Terms and criterion 21, three refutations sharpened
(criteria 7, 13, 26), one refutation widened (22), two `[DETAIL]`s added and
the stop rule of `[GAP]` 3 extended to `[GAP]` 2. The numbering of the
criteria is unchanged.

Changed again on 2026-09-30 by the maintainer's answers 10 and 11
(`decisions.md`, addendum "after the spec review"): the local proofs are
dropped and the customer checkout on the same disk is an accepted residual
risk. Criteria 22, 24 and 33 are rewritten and marked, the `[GAP]`s 1–4 are
dropped, and the Non-goals and two `[DETAIL]`s follow. Answer 12 moves this
change's own review (6) to Opus 5.5 ("Order of work"). The numbering is
unchanged.

Written against `origin/main` at `ba940fb`, the merge of pull request #54,
which brought the change classes, decision pull requests and the rule that a
decision takes effect when the maintainer merges it.

## Order of work

- **Implementation starts only after pull request #54 is in this branch.**
  The branch `feat/stage-2-codex-glm` stands on `1c708f7`; phase 4 begins
  with merging `origin/main` (containing `ba940fb`) into it. The class field,
  the decision pull request, `prompts/02-spec.md` and `prompts/07-commit.md`
  this spec builds on exist only from there (`decisions.md`, "Consequences
  for the order of work").
- **This change is reviewed under stage 1.** Its spec review (2a) and its
  review (6) run on Fable 5.1 as today, because the runners it builds and the
  ADR that permits them take effect only with its merge (criterion 1).
  *(Changed by the maintainer's answer 12 of 2026-09-30: its review (6) runs
  on Opus 5.5, the interim routing until stage 2 is merged.)*
  Phase 4 runs on Sonnet 5.5 at effort `medium` (`decisions.md`, answer 8,
  which needs no ADR).
- **Needed from the maintainer during phase 4:** the ChatGPT account's
  setting "Improve the model for everyone", read once in the account
  (criterion 8). Nothing else.

## Problem

Measured on 2026-09-30 (`research.md`, sections 1–8 and the two sections
after them):

- **No review by another vendor is possible.** Every phase runs on
  Anthropic models. `docs/WORKFLOW.md` §4 describes a stage 2 that is
  "prepared, not active", and describes the wrong one: GLM implementing by
  plan markings and Kimi reviewing, where the maintainer decided on
  2026-09-30 that Codex reviews (2a and 6), GLM reviews in a short loop
  before phase 6, Sonnet implements, and Kimi is dropped.
- **Nothing stands between the repository and a foreign endpoint.** `make
  leakcheck` is a stub that prints a message and exits 1. The only barrier is
  a line in `model-endpoints.yaml`, which nothing enforces.
- **A foreign agent sees more than a change.** Codex and Claude Code start
  agents with tools inside the worktree. Codex can run commands, so it reads
  the tracked tree, the git history and — its read-only sandbox limits
  writes, not reads — the whole disk, where the customer instance's checkout
  sits beside this one (research, gaps closed, items 5–6); Claude Code's
  read tools reach beyond the worktree too, unless they are configured not
  to. The leak check as written in
  `portfolio-agentic-engineering` scans only the change folder and the diff.
  The maintainer accepted the reads beyond the worktree as a residual risk
  on 2026-09-30 (`decisions.md`, answer 11).
- **The endpoint declaration does not match the decision.** No OpenAI
  endpoint is declared ("not listed is BLOCK"), Kimi is declared, GLM is
  declared for implementation, Sonnet 5.5 is not declared, and the
  personal-use declaration does not cover the ChatGPT subscription.
- **Two model names would not resolve.** `tests/test_model_endpoints.py`
  turns dots into dashes, so a prompt naming `GLM 5.3` or `gpt-6.1-sol` goes
  red against the vendors' real ids; its routing-table check skips rows `1a`,
  `2a` and any `4b`.
- **D-13 forbids the calls.** Decision D-13 of the 2026-09-16 interview opens
  stage 2 only after four criteria; criterion 1 (three measured runs) is not
  met and criterion 3 (a green leak check) cannot be met today. The
  maintainer decided to amend D-13 by an ADR (`decisions.md`, answer 1), and
  the gate `decision-continuity` holds every amendment to an ADR that names
  it.

## Terms

- **Foreign reviewer** — Codex (model `gpt-6.1-sol`, OpenAI, through the
  official Codex CLI signed in with the maintainer's ChatGPT subscription) or
  GLM (model `glm-5.3`, Z.ai, through Claude Code against Z.ai's
  Anthropic-compatible endpoint).
- **Call** — one start of a foreign reviewer's program: `codex exec`, `codex
  exec resume`, or `claude -p` against Z.ai.
- **The runner** — `python3 scripts/stage2.py <verb> <change>`, the only
  way this repository starts a call. Verbs: `spec-review` (Codex, phase 2a),
  `review-loop` (GLM, one round of phase 4b), `release-loop` (the loop rows
  into `findings.md` after a phase-6 verdict), `review` (Codex, phase 6).
- **The leak check** — `make leakcheck NAME=<change>`, which runs `python3
  scripts/leakcheck.py --name <change>`: the check from
  `portfolio-agentic-engineering`, ported in English.
- **The denylist** — the rule file outside the repository,
  `~/.config/cc-routing/denylist.txt` unless `--denylist` or the variable
  `LEAKCHECK_DENYLIST` names another; one rule per line, `name = regex`.
- **The scanned set** — (a) every file under `plans/changes/<change>/`;
  (b) every file of the worktree that git tracks or lists as untracked and
  not ignored, as it stands on disk; (c) the message and the patch of every
  commit reachable from a local or remote-tracking branch; (d) every text
  the runner itself puts into a call's prompt.
- **Loop record** — the file that holds the rows of the GLM loop and the
  implementer's decision on each, one per change, outside the worktree and
  outside the repository's git directory. The implementer writes its decision
  beside each row there — the Status with its reason, and for a taken row the
  `Broke a test` mark — before the next round starts or the rows are
  released; `release-loop` carries each row with these marks as they stand.
- **Loop rows** — the rows of the GLM loop: in the loop record until they
  are released, in `findings.md` after.
- **Phase-6 verdict line** — the line `Phase 6 verdict: <reviewer>
  <session>, <date>` under the table in `findings.md`. The runner writes
  Codex's; a Fable reviewer writes its own, as `prompts/06-review.md` says.
- **Stage-2 run** — a change whose review made at least one call. Runs are
  counted in the order their pull requests merge.
- **Stand-in** — a program of the test suite named `codex` or `claude` that
  records its arguments, environment and input, prints canned output and
  contacts nothing.

## Acceptance criteria

Each criterion states one condition. Where a trigger, a state or a failure
applies, it begins with When, While or If. Each names what would refute it.

### Nothing leaves before the decision takes effect

1. While this change's pull request is not merged, no call runs with content
   from this change's worktree.
   *Refuted by:* a session file under `~/.codex/sessions` whose recorded
   working directory is this worktree and whose time precedes the merge; a
   loop record of this change written before the merge.

2. When the test suite runs the runner, the only `codex` and `claude`
   programs on the runner's search path are stand-ins.
   *Refuted by:* a runner test whose search path contains a directory that
   holds the real program; a stand-in that opens a network connection.

3. When the test suite runs, no test reads the real denylist or the real
   secrets file.
   *Refuted by:* a test result that changes when the suite runs with
   `~/.config/cc-routing/denylist.txt` and `~/.config/cc-routing/secrets.env`
   made unreadable.

### The endpoint declaration

4. `model-endpoints.yaml` declares the endpoint `openai-codex`: operator
   OpenAI, `residenz: anbieter-erklaert`, `abrechnung: abonnement`,
   `darf_sehen: [framework]`, the model `gpt-6.1-sol`, and a remark naming
   the official Codex CLI as the only way in, phases 2a and 6 as its use, and
   where OpenAI says it processes data.
   *Refuted by:* one of these values missing or different; `kundencode` in
   its `darf_sehen`.

5. Kimi is moved from the endpoints of `model-endpoints.yaml` to
   `ausgeschlossen`, with the date 2026-09-30 and the maintainer's decision
   as its reason.
   *Refuted by:* an endpoint naming Moonshot AI, `k3` or `kimi-for-coding`;
   no entry for Kimi under `ausgeschlossen`, or one without the date or the
   reason.

6. `claude-sonnet-5-5` is a model of the endpoints `anthropic-api` and
   `claude-code-plan`.
   *Refuted by:* `tests/test_model_endpoints.py` red on a prompt naming
   Sonnet 5.5.

7. The remark of `glm-coding-plan` names the review loop before phase 6 as
   its use.
   *Refuted by:* a remark that names implementation, the implement phase or
   plan markings as its use.

8. The section on the purpose of use declares the ChatGPT subscription
   behind Codex as personal use — dated 2026-09-30, to be obtained again
   under the same three conditions as the GLM declaration, with the
   account's setting "Improve the model for everyone" as the maintainer read
   it and the date it was read.
   *Refuted by:* the subscription, the date, one of the three conditions or
   the setting missing; a setting that no statement of the maintainer
   supports (held by review of the session).

### Every named model resolves

9. When a phase prompt or a routing row names a model whose declared id
   contains a dot, the name resolves.
   *Refuted by:* a prompt naming `GLM 5.3` that is red while `glm-5.3` is
   declared; a name that resolves by substring (`GLM 5` against `glm-5.3`).

10. The routing-table check reads every row of `docs/WORKFLOW.md` whose first
    cell is a phase number with an optional letter, whatever the number of
    words in the phase name.
    *Refuted by:* a row `| 2a Spec review | **k3** | … |` or `| 4b Review
    loop | **k3** | … |` added to `docs/WORKFLOW.md` that leaves the test
    green.

### The leak check

11. When a denylist rule matches a line anywhere in the scanned set, the
    leak check exits 2.
    *Refuted by:* exit 0 with a match planted in any one of: a file of the
    change folder, an uncommitted edit of a tracked file, an untracked file, a
    commit message, the patch of an earlier commit, a commit reachable only
    from a remote-tracking branch, a text handed to it as prompt text.

12. If the leak check cannot measure, it exits 2 and names why.
    *Refuted by:* exit 0, or a message without the reason, in any one of
    these cases: the denylist missing, empty, unreadable or holding a rule
    that is not a valid pattern; no change named; the change folder missing
    or empty; a file of the scanned set, or the history, unreadable (a file
    of mode 000 in the change folder).

13. When the leak check reports a match, it reports the place (file and
    line, or commit and line of its patch), the rule's name and the match's
    length, and nothing of the matched text.
    *Refuted by:* a report that lacks one of the four; a planted value of 32
    random letters, eight consecutive of which appear in its standard output
    or standard error.

14. When nothing matches, the leak check exits 0 and states how many files,
    commits and rules it scanned.
    *Refuted by:* a clean run whose output lacks one of the three numbers.

### Every call goes through the runner's preconditions

15. If no change is named, or `plans/changes/<change>/` does not exist, the
    runner starts no call and exits non-zero.
    *Refuted by:* a stand-in that records a start.

16. If the leak check does not exit 0 within the same runner invocation,
    immediately before a call, that call does not start.
    *Refuted by:* a stand-in that records a start after a planted match; a
    second call of one invocation that relies on the first call's leak check.

17. If the declaration does not clear a call's endpoint for it, the call
    does not start.
    *Refuted by:* a stand-in that records a start under a temporary
    declaration in which the endpoint is missing, does not list the call's
    model, lacks `framework` in `darf_sehen`, or has `residenz:
    nicht-erklaert`.

18. When a call starts, the foreign program's environment is the one the
    runner built.
    *Refuted by:* a stand-in that sees a variable of the caller whose name
    ends in `_KEY`, `_TOKEN` or `_SECRET` (for example `GH_TOKEN`) other than
    the one credential the call needs; a GLM stand-in that sees a caller's
    `ANTHROPIC_MODEL` or `ANTHROPIC_BASE_URL` instead of the runner's value
    for every `ANTHROPIC_*` variable Claude Code reads for endpoint,
    credential and model.

19. When a call starts, its standard input is empty.
    *Refuted by:* a stand-in that reads bytes from its standard input, or
    waits on it.

20. While the runner holds the GLM credential, nothing it prints or writes
    contains that credential.
    *Refuted by:* eight consecutive characters of a test credential in the
    runner's standard output, standard error or `findings.md`.

21. When a call starts, `findings.md` of the change gains one line naming the
    date, the runner's verb, the endpoint, the model and the leak check's
    three numbers; if the file does not exist yet, the runner creates it with
    a header that passes the gate `plans-registry` (`status`,
    `implementation_status`, `date`, `last_reviewed`, and `bead` taken from
    `spec.md`).
    *Refuted by:* a stand-in start without its line; a `findings.md` the
    runner created that `python3 scripts/plans_registry.py --check` blocks.

22. *(Changed by the maintainer's answer 11 of 2026-09-30: no confinement
    and no local proof; the reviewers can read the whole disk, the customer
    checkout included, as an accepted residual risk.)* When the runner starts
    or resumes a call, the call's prompt asks the reviewer to read nothing
    outside the worktree and the repository's git directory; `docs/WORKFLOW.md`
    §4 and ADR 0007 say that this is a request, not a lock, and that the
    reviewers can read the rest of the disk.
    *Refuted by:* a stand-in's prompt without the request; §4 or ADR 0007
    presenting the request as a confinement, or not naming the residual risk.
    ~~While a foreign reviewer runs, its file access is confined to reading
    the worktree, the repository's git directory and the paths its own
    program needs. Refuted by: a local measurement in which a read of a
    planted file outside succeeds, or any write.~~

### Codex in phases 2a and 6

23. When the runner starts or resumes a Codex call, the call is pinned to
    model `gpt-6.1-sol`, effort `max`, the read-only sandbox and a session
    that is kept.
    *Refuted by:* a first or a resumed call, recorded by a stand-in while the
    user configuration names another model and effort, that lacks the model,
    the effort or the read-only sandbox, or carries `--ephemeral`.

24. *(Changed by the maintainer's answer 10 of 2026-09-30: the local proof
    is dropped; that the configuration takes effect is not measured.)* When
    the runner starts or resumes a Codex call, the call carries the
    configuration that switches Codex's hooks and memories off.
    *Refuted by:* a recorded call without that configuration.
    ~~Nothing reaches Codex but its prompt and what it reads itself. Refuted
    also by: a local measurement in which a planted hook runs.~~

25. When the runner starts or resumes a Codex call for phase 2a or 6, its
    prompt contains that phase's prompt file in full and names the change.
    *Refuted by:* a stand-in's prompt without the text of
    `prompts/02a-spec-review.md` for `spec-review`, or of
    `prompts/06-review.md` for `review`.

26. When `spec-review` finishes, `findings.md` carries the reviewer's answer
    as rows with reviewer `Codex`, and under the table `Reviewer session:
    codex <thread id>` with the id from the call's `thread.started` event.
    *Refuted by:* a stand-in that emits thread id X and a `findings.md`
    without X, or with another id; a stand-in whose canned answer is three
    table rows of which fewer than three stand in `findings.md` with reviewer
    `Codex`.

27. If a Codex call ends without a `thread.started` event, or with a
    non-zero exit, the runner writes no session line and exits non-zero.
    *Refuted by:* a session line after a failing stand-in.

28. When `review` starts for a change whose `findings.md` names a Codex
    session, the call resumes that session.
    *Refuted by:* a recorded `codex exec` without `resume <id>` while an id
    is recorded.

29. If `review` finds no phase-2a session to continue, `findings.md` says
    that a fresh session reviewed.
    *Refuted by:* silence in `findings.md` when no Codex session is recorded,
    or when a stand-in answers a resume with a `thread.started` id other than
    the recorded one.

30. While Codex's phase-6 verdict line is not written, no loop row is in the
    worktree or in the prompt of a Codex call.
    *Refuted by:* a loop row found in the worktree, or in the prompt a
    stand-in received for the verdict call.

31. When Codex answers on the loop rows after its verdict, its answer is
    recorded beside each loop row as agreement or disagreement, and not in
    its verdict.
    *Refuted by:* a loop row in `findings.md` without Codex's mark after
    `review` has finished; a verdict row that differs after the second call
    from what it was after the first.

### The GLM review loop (phase 4b)

32. When `review-loop` starts a round, the call is Claude Code against
    `https://api.z.ai/api/anthropic` with model `glm-5.3` and effort `max`.
    *Refuted by:* a stand-in that records another base address, model or
    effort.

33. *(Changed by the maintainer's answer 10 of 2026-09-30: the local proof
    is dropped; that the configuration takes effect is not measured.)* When a
    GLM call starts, it carries a fresh, empty Claude Code configuration
    directory and the configuration that skips the project's settings and
    hooks.
    *Refuted by:* a stand-in that sees `CLAUDE_CONFIG_DIR` unset, pointing to
    the user's own directory, or pointing to a directory with files in it; a
    recorded call without the configuration that skips the project's hooks.
    ~~Refuted also by: a local measurement in which the project's
    session-start hook runs.~~

34. When a GLM call starts, its tools can only read and search files.
    *Refuted by:* a recorded configuration that permits editing, writing, a
    shell, a web fetch or a web search.

35. When a GLM call starts, its prompt contains `prompts/04b-review-loop.md`
    in full and the change's diff against its merge base with `origin/main`,
    uncommitted changes included.
    *Refuted by:* a stand-in's prompt without the prompt text, or without an
    uncommitted edit made before the call.

36. If two rounds of the loop have run for a change — a round has run when
    its rows stand in the loop record — `review-loop` refuses a third and
    starts no call.
    *Refuted by:* a stand-in that records a third round's start, also after
    the first two rounds' rows were released.

37. When a round finishes, its rows go into the loop record, each marked
    with the round's number and reviewer `GLM`.
    *Refuted by:* a round's rows in the worktree; a row without its round.

38. If `findings.md` has no phase-6 verdict line, `release-loop` refuses and
    changes nothing.
    *Refuted by:* a loop row in `findings.md` after `release-loop` ran
    without a verdict line.

39. When `release-loop` runs after the verdict line, every loop row enters
    `findings.md` with reviewer `GLM`.
    *Refuted by:* a loop row missing from `findings.md`, or entered without
    its reviewer; a released row whose Status, reason or `Broke a test` mark
    differs from the loop record's.

### Doctrine and prompts

40. `docs/WORKFLOW.md` §4 routes by change class: a one-sentence change and
    a `spike` get no stage 2; a `bounded` change gets the GLM loop only, with
    its review (6), and a spec review if one is held, on Fable 5.1; a
    `feature` and an `architectural` change get Codex in 2a, the GLM loop,
    and the same Codex agent in 6.
    *Refuted by:* a class with other routing than this.

41. `docs/WORKFLOW.md` §4 states that nothing checks a change's class, so a
    feature stated as `bounded` skips Codex and only the review before the
    merge catches it.
    *Refuted by:* the statement missing.

42. `docs/WORKFLOW.md` §4 has the stage-2 routing rows in the form of §3's
    table: `2a Spec review` and `6 Review` on `gpt-6.1-sol` at effort `max`
    through the Codex CLI, `4b Review loop` on GLM 5.3 at effort `max`
    through Claude Code against Z.ai.
    *Refuted by:* a row missing or naming another model or effort.

43. The routing table of `docs/WORKFLOW.md` §3 routes `4 Implement` to Sonnet
    5.5 at effort `medium`, for every change.
    *Refuted by:* Sonnet 5 in that row; another effort; a sentence limiting
    Sonnet 5.5 to stage-2 changes.

44. Where `docs/WORKFLOW.md` §3 says that spec review and review run on
    Fable 5.1, it names the classes that §4 routes to Codex instead.
    *Refuted by:* §3 stating Fable 5.1 for the spec review or the review of
    every change without that exception.

45. `docs/WORKFLOW.md` §4 says that a call starts only through the runner,
    after a green leak check and a declaration that clears its endpoint.
    *Refuted by:* the statement missing; a way to a foreign reviewer
    described that bypasses the runner.

46. The phase table of `docs/WORKFLOW.md` §2 has a row `4b Review loop` with
    its artefact (the loop rows, in `findings.md` after `release-loop`, held
    outside the repository until the phase-6 verdict — so §2's first
    sentence, one versioned artefact in the repository per phase, stays
    true), its gate (at most two rounds, `make verify` green after each
    repair) and its prompt.
    *Refuted by:* the row missing, or one of the three; an artefact cell that
    names the loop record as the artefact.

47. The findings process in `docs/WORKFLOW.md` §2 states the evidence rule: a
    Codex or GLM finding is taken only when a test demonstrates it or the
    spec supports it; otherwise it is rejected with its reason and stays in
    `findings.md` as a disagreement; this holds in every repair round, so a
    finding about something the spec does not cover needs a test or is
    rejected.
    *Refuted by:* the rule or its consequence missing; a sentence anywhere in
    `docs/WORKFLOW.md` or `prompts/` that lets an implementer take a foreign
    finding without a test or the spec behind it.

48. `prompts/04-implement.md` and `prompts/04b-review-loop.md` state the
    evidence rule for the implementer who takes or rejects a finding.
    *Refuted by:* the rule missing from either.

49. `docs/WORKFLOW.md` §4 defines two findings columns for every stage-2
    change: `Reviewer` (Codex, GLM or Fable) and `Broke a test` (for each
    taken row, whether its repair turned a test red that was green before
    it).
    *Refuted by:* either column or its meaning missing.

50. `docs/WORKFLOW.md` §4 states the stop rule: after the third stage-2 run a
    short evaluation is written under `docs/research/`, and if at least one
    taken Codex or GLM finding broke a test, stage 2 falls back to Fable 5.1
    until the maintainer decides again.
    *Refuted by:* the rule missing; another number of runs; another fallback.

51. `docs/WORKFLOW.md` §4 presents nothing as stage 2 that does not exist
    once this change is merged.
    *Refuted by:* a sentence that presents the six `scripts/cc-*.sh`
    profiles, `scripts/run_change.sh`, plan markings or an option of the
    runner or the leak check that does not exist as part of stage 2.

52. The header note of `docs/WORKFLOW.md` says that stage 2 is active for
    framework content, by change class, since ADR 0007.
    *Refuted by:* "Stages 2 and 3 are prepared, not active" still standing.

53. The list "Not all of it is here yet" in `docs/WORKFLOW.md` names exactly
    the files the doctrine names and the tree lacks.
    *Refuted by:* a listed file that exists after this change; a listed file
    the rest of `docs/WORKFLOW.md` no longer names.

54. `docs/WORKFLOW.md` §6 says that ADR 0007 opened stage 2 for framework
    content, with the first three stage-2 runs measured in place of the
    earlier readiness signal.
    *Refuted by:* §6 presenting "two to three weeks" of stage 1 as the
    condition still to be met.

55. `prompts/02a-spec-review.md` and `prompts/06-review.md` each give the
    two paths of their phase: `gpt-6.1-sol` through the runner for `feature`
    and `architectural` changes, Fable 5.1 for the others.
    *Refuted by:* one path missing from either prompt.

56. `prompts/06-review.md` tells the reviewer to write its verdict, ending
    with the phase-6 verdict line, before it reads the loop rows.
    *Refuted by:* the order missing, or the verdict line missing from the
    Fable path.

57. `prompts/04-implement.md` names Sonnet 5.5 at effort `medium`.
    *Refuted by:* another model or effort on its model line.

58. `prompts/03-plan.md` asks for no model markings.
    *Refuted by:* `[FLASH]`, `[GLM5.3]` or `[SONNET]` in it.

59. The rule for acceptance criteria in `prompts/02-spec.md` requires one
    condition per criterion, beginning with When, While or If where a
    trigger, state or failure applies, and what would refute each.
    *Refuted by:* the sentence missing; the refutation requirement missing
    after this change.

60. `AGENTS.md` carries phase 4b in its one-screen table and the sentence
    that a foreign reviewer is started only through the runner.
    *Refuted by:* the row or the sentence missing; `AGENTS.md` longer than
    200 lines (`tests/test_entry_points.py`).

61. When an agent in a Claude Code session of this repository runs `codex`
    directly, Claude Code asks first.
    *Refuted by:* no ask rule for it in `.claude/settings.json`; the settings
    test staying green when that rule is removed.

### ADR 0007 and decision D-13

62. `docs/adr/0007-*.md` records the amendment of D-13 as the maintainer
    answered it: criteria 3 (a green leak check) and 4 (a declared endpoint
    with residency) stay and the runner enforces them on every call;
    criterion 2 governs lakeswitch-ai content; criterion 1 is replaced by
    measuring the first three stage-2 runs with the stop rule; the accepted
    loss is the measured stage-1 baseline.
    *Refuted by:* one of these parts missing or stated otherwise.

63. ADR 0007 records where framework content may flow: to the two declared
    endpoints, through their official tools, and nothing but framework
    content — this repository's tree, as the class `framework` of
    `model-endpoints.yaml` defines it; lakeswitch-ai's own trees are not
    sent, and their disclosure decision (D-13, criterion 2) stays theirs.
    *Refuted by:* another endpoint or tool named; the content limit or its
    definition missing.

64. ADR 0007 records that Kimi is dropped.
    *Refuted by:* the removal missing.

65. ADR 0007 states that it does not enter M2, the Omnigent milestone for
    cross-vendor operation.
    *Refuted by:* a sentence that declares M2 entered.

66. The gate `decision-continuity` maps D-13 to ADR 0007.
    *Refuted by:* the gate green with `"D-13"` absent from `AMENDMENT_ADRS`
    in `scripts/check_decision_continuity.py`, or with ADR 0007 not naming
    D-13.

67. The decision-continuity row of D-13 in
    `docs/architecture/2026-09-17-omnigent-first-target.md` reads "Amend" and
    points to ADR 0007.
    *Refuted by:* "Retain" in that row.

68. Both architecture documents that set D-13's criteria as the entry
    condition for foreign calls — the target document and
    `docs/architecture/2026-09-17-implementation-plan.md` — carry a dated
    note that ADR 0007 amends D-13.
    *Refuted by:* the note missing from either.

69. This change's pull request is a decision pull request.
    *Refuted by:* a title without `decide(`, no label `decision`, or a body
    that does not begin with the block of
    `.github/PULL_REQUEST_TEMPLATE/decision.md`.

### The tree stays green

70. `make verify` is green on the pull request's last commit.
    *Refuted by:* any gate red, among them the kit's empty-repository probe,
    `decision-continuity`, `adr-answers` and `frontmatter-current`.

71. The kit manifest lists the leak check and its test as `mechanismus`.
    *Refuted by:* `python3 scripts/kit/probe.py --list` without
    `scripts/leakcheck.py`.

72. Every sentence this change adds is English, and no existing German
    sentence is translated in passing.
    *Refuted by:* a new German sentence; a German line rewritten without a
    change of meaning. Held by review.

## Non-goals

- **A real call inside this change.** The proposal ended the Codex and GLM
  packages each with "one real run". Here the first real call is the first
  stage-2 run after the merge, which is also run 1 of the three measured
  runs (see the `[DETAIL]` "No real call before the merge").
- **The orchestrator and the old stage-2 design** — `scripts/run_change.sh`,
  the six `scripts/cc-*.sh` profiles, `tests/test_model_profiles.py`, plan
  markings and `templates/plan-marking.md`, `cc-glm-flash.sh` for routine
  steps, and herdr as the view of waiting agents.
- **Codex effort `ultra`.** It hands work to further agents on its own, which
  breaks "one agent for 2a and 6".
- **Customer code and lakeswitch-ai content.** Neither goes to a foreign
  reviewer. lakeswitch-ai's disclosure decision stays that repository's to
  write, and its journal line on D-13 stays as it is.
- **A check that a change's class is right, and a runner that refuses a
  phase by class.** The class table is doctrine (`decisions.md`, answer 3).
- **Enforcing the stop rule mechanically.** The rule is written; the
  evaluation after three runs is read by a person.
- **The evaluation itself**, the re-scoping of bead coding-harness-kw0 (the
  stage-2 entry measurement) and any other tracker write. The tracker is
  written by the session that holds it (house rule 4); the pull request
  names bc9 and kw0 in its body.
- **`templates/findings.md`.** The two new columns are defined in the
  doctrine; the template belongs to the template bundle (bead
  coding-harness-9qo).
- **Translating the existing German** of `model-endpoints.yaml` and
  `tests/test_model_endpoints.py` (bead coding-harness-yim).
- **Omnigent.** M2 is not entered; the runners are not wired into Omnigent.
- **Scanning what the repository does not present** — files git ignores (in
  this worktree on 2026-09-30: `.pytest_cache/`, `.ruff_cache/` and
  `__pycache__/` only), the tracker's database (`refs/dolt/data`; locally
  `refs/dolt/data-check` and `refs/remotes/origin/__dolt_remote_info__`,
  which a reviewer can show through git inside the confinement of criterion
  22 — the rendered tracker held no rule hit on 2026-09-30, research section
  5), anything else on the disk. *(Changed by answers 10 and 11.)* The
  reviewers' reads are not confined: what the scanned set leaves out stays
  readable to them, the main checkout's working tree and the customer
  checkout included, and the prompt's request (criterion 22) is all that
  stands against it. The configuration that switches hooks off (criteria 24
  and 33) keeps the tracker text out as far as it takes effect, which is not
  measured.
- **Local proofs with the real programs** (answers 10 and 11): read
  confinement for Codex and for Claude Code, hooks and memories being off,
  and which settings take effect on `codex exec resume`. No real CLI is
  started with a stand-in model endpoint either.
- **Confining the implementer.** Sonnet and Fable are Anthropic models,
  declared for customer code as well.
- **The domain agent definitions in `.claude/agents/`**, which pin
  `claude-sonnet-5`; they are not the implement phase.
- **Reconciling D-16** ("No fixed model names in doctrine") with a doctrine
  that has named models since before this change.
- **`scripts/export/manifest.yaml`, `bedrock-claude`, `glm-5.3-flash`** stay
  as they are (see the `[DETAIL]` items).
- **Proof that no agent reached a vendor by another spelling.** The ask rule
  of criterion 61 is a brake, not a lock: `sh -c`, an absolute path or a
  script file passes it, as `docs/WORKFLOW.md` says of the merge rules.

## Open decisions

None open. Every `[DECISION]` of `research.md` is answered in `decisions.md`.

### `[GAP]` — carried to the plan, answerable by measuring locally

**Dropped by the maintainer's answers 10 and 11 of 2026-09-30**, except item
5: items 1–3 are not measured, and the runner passes its configuration
without a proof (criteria 22, 24, 33 as changed); item 4 is read from the
call's own output when a real call runs, and a call without `thread.started`
writes no session line (criterion 27). The text below is the text before
that decision.

None of these needs a call with repository content. Every local measurement
with a real CLI runs from a scratch directory outside this worktree, without
repository content and under a temporary `CODEX_HOME` or
`CLAUDE_CONFIG_DIR`, so that criterion 1's refutation stays clean and the
maintainer's own sessions and memories stay untouched.

1. **Codex on resume.** Which of model, effort and sandbox take effect when
   passed to `codex exec resume` (the help lists no `--sandbox` there; `-c`
   overrides exist). Measured with the real CLI against a local stand-in
   model provider, or read in the CLI's help and source at 0.159.2.
2. **Codex hooks and memories off.** Which configuration switches off the
   tracked `.codex/hooks.json`, the user's hooks and the memories feature
   (`--ignore-user-config`, `-c` feature keys), and a local proof that they
   are off. **If it cannot be shown, the implementing session stops and
   reports**, as for item 3: what a hook injects reaches Codex outside the
   scanned set, and unchecked is not the same as clean.
3. **Read confinement for both reviewers (criterion 22).** For Codex:
   whether the permission profiles of the current documentation work in CLI
   0.159.2 on macOS, measured with the CLI's local sandbox command against a
   planted file in a sibling directory. For GLM: which Claude Code tool and
   permission configuration confines reads, measured against a local
   stand-in endpoint. **If either cannot be shown, the implementing session
   stops and reports** (`prompts/04-implement.md`); whether to accept that
   reviewer's residual risk is then a `[DECISION]` for the maintainer.
4. **Session id.** Confirm locally that `codex exec --json` of 0.159.2 emits
   `thread.started` with `thread_id`, as the documentation says.
5. **Whether Z.ai honours effort `max`.** Not measurable without a real
   call; the runner asks for it, and the record of the first stage-2 run
   says what was observed.

No longer load-bearing: whether Claude Code with its own base address reads
`AGENTS.md` (`docs/WORKFLOW.md` §8), because the GLM prompt carries what the
reviewer needs; and the study behind the addendum's point 2.

### `[DETAIL]` — decided here, with the reason

Each is reversible and binds nothing beyond this change; the maintainer's
veto is one word.

- **No real call before the merge (criterion 1).** A decision takes effect
  when the maintainer merges its pull request (`AGENTS.md`, house rule 8);
  until ADR 0007 is merged, D-13 stands unamended, the target document
  requires every amendment's ADR "before runtime activation", and the
  implementation plan requires every D-13 condition "even in an optional
  trial". What is lost: evidence, before the merge, that the runners work
  against the real endpoints; the first stage-2 run after the merge carries
  that risk, and a runner fault found there is a follow-up fix. Choosing the
  other way would send data under a decision not yet in effect, which cannot
  be taken back.
- **This change's class is `architectural`.** It carries its ADR (answer 4),
  so it is not asked the ADR question and needs no answer file.
- **The phase gate is `plans_registry.py --check`.** The validator the phase
  prompts name, `scripts/validate_change_artefacts.py`, does not exist; the
  changes `frontmatter-current` and `harness-decide-adr` found the same.
- **One runner with four verbs, `scripts/stage2.py`.** One place holds the
  preconditions every call shares — the named change, the leak check, the
  endpoint check, the reduced environment — so they cannot differ between
  the two vendors. `release-loop` is its own verb because a Fable reviewer in
  phase 6 needs it without Codex.
- **The resolver learns dots; the declaration keeps the vendors' ids.**
  `glm-5.3` and `gpt-6.1-sol` are what the CLIs accept; a dashed alias would
  be an id no program knows. Resolution stays equality, never substring.
- **Stage-2 rows in §3's row form, and the check reads lettered phases.**
  Otherwise the two models that matter most for data leaving the machine
  would be the two the test never reads.
- **The leak check scans the scanned set, not only the change and the
  diff.** A foreign agent reads the tree and the history by itself; a check
  that scans less than it can read is green over what it did not look at.
  The research counted no hit in the tree, the history and the tracker
  output on 2026-09-30, so the wider scope blocks nothing today. Uncommitted
  changes are scanned rather than refused, because the loop runs between
  repairs. The ported `--base` option goes, since the whole history is
  scanned. The runner's own prompt texts are scanned because the loop rows
  travel to Codex.
- **The reduced environment (criterion 18).** A reviewer that can run a
  command can print a variable into its context.
- **Codex's settings on every call:** model and effort pinned, because the
  user configuration names `gpt-5.6-sol` at `xhigh`; the read-only sandbox;
  never `--ephemeral`, because an ephemeral session cannot be resumed and a
  resume of one silently starts afresh (research, gaps closed, item 4); empty
  standard input, because `codex exec` waits for it in a background shell;
  hooks and memories off, so only the prompt and the files it reads reach it
  — passed, not measured (answer 10).
- **The session id comes from `thread.started`, and a resume is checked
  against it.** Codex cannot be given an id up front, and a silently fresh
  thread would review without its phase-2a context.
- **GLM's settings on every call:** a fresh empty configuration directory so
  the maintainer's global instructions and hooks stay home; the project's
  hooks skipped so `tools/bd prime` injects no tracker text (both passed, not
  measured — answer 10); read and search tools only; the diff in the prompt because the reviewer cannot run `git`;
  the house rules it needs in `prompts/04b-review-loop.md`, because a session
  with its own base address may not read `AGENTS.md`. Credential from
  `~/.config/cc-routing/secrets.env` (`GLM_KEY`, overridden by `CC_SECRETS`),
  the names the maintainer's machine already carries.
- **The loop record lives outside the worktree and the git directory**,
  by default under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/`.
  Codex can read the whole worktree, so the order "verdict first" holds only
  if the rows are elsewhere. `release-loop` removes the record once its rows
  are in `findings.md`, which stays the one record; `review-loop` counts
  rounds in both places, so a release does not reset the count.
- **A round has run when its rows stand in the loop record.** A call that
  ends without rows is a failed call, not a round; its line in `findings.md`
  (criterion 21) shows that it happened. Counting starts instead would let a
  crashed call use up one of the maintainer's two rounds.
- **An answer that is not table rows is appended as it came**, under a line
  that says so, and never dropped: the call was made, and the step that works
  the rows into the spec is a person's in any case.
- **The order also holds for Fable in phase 6 of a `bounded` change.** The
  independence of the last review does not depend on the vendor; the prompt
  and `release-loop` hold it.
- **Codex marks each loop row agree or disagree, and nothing is netted.**
  "Disagreements are recorded, not resolved" (`docs/WORKFLOW.md` §2).
- **One line per call in `findings.md` (criterion 21).** It is the evidence
  that criterion 3 of D-13 held on every call — generated, not typed, as bead
  kw0 asked of its metrics. The runner creates the file when phase 2a is its
  first writer, with the header the gate `plans-registry` holds every
  `plans/**/*.md` to; the `bead` comes from `spec.md`, the only place a
  change's bead is written down.
- **The two columns live in the doctrine**, not in a template the
  repository does not have yet.
- **"Broke a test" means:** a test green before a taken finding's repair and
  red after it, the finding's own new test excepted, which the evidence rule
  expects to be red first.
- **The stop rule, read literally:** at least one taken Codex or GLM finding
  that broke a test, over the three runs, sends all of stage 2 back to Fable
  5.1; the evaluation's pull request applies the fallback, which the
  maintainer decided in advance. Not enforced by a counter, for three events.
  The implementation plan's M2 hold points the same way.
- **The evaluation goes under `docs/research/`**, where research about this
  repository lives (`AGENTS.md`).
- **The endpoint:** named `openai-codex`; `residenz: anbieter-erklaert`,
  because OpenAI states where it processes personal-plan data and offers no
  region choice to personal plans (research, gaps closed, item 2 — from
  search summaries, as the pages refused a direct fetch); `abrechnung:
  abonnement`.
- **Kimi's exclusion entry has `klasse: framework`**, the only class it was
  ever cleared for.
- **`glm-5.3-flash` stays declared and unused; `bedrock-claude` gets no
  Sonnet 5.5.** Neither was asked for; Bedrock is declared but not in use.
- **New text in `model-endpoints.yaml` is English inside its German keys**;
  its translation is a pull request of its own (house rule 1).
- **§4 is rewritten around the decided flow.** The orchestrator, the six
  profiles, the plan markings and the herdr subsection describe GLM
  implementing by plan marking, which the maintainer's routing replaced;
  they leave §4, the "not here yet" list and `prompts/03-plan.md` with it.
- **ADR 0007** is dated 2026-09-30 with status `accepted` and says that the
  maintainer's merge of the pull request that carries it is the
  confirmation (house rule 8); the pull request carries one decision.
- **Dated notes, not rewrites, in the two architecture documents**, as the
  target document did for ADR 0006; the gap analysis is a measurement at
  `eddfc0b` and stays.
- **ADR 0007 does not enter M2.** It amends D-13's content; M2 has further
  entry conditions — the Omnigent topology, lakeswitch-ai's adoption — that
  nobody was asked about.
- **Kit and CI bookkeeping.** The leak check and its test are `mechanismus`:
  the barrier is portable and the denylist is each machine's own. The runner
  and its test fall under the catch-all `bestand`: which vendors review is
  this repository's routing (D-16 puts routing in the instance). Both
  scripts get a reason in `ci_gates.OHNE_AUFRUFER`, because no CI step holds
  the denylist or a credential. The probe's exception list takes the new
  model-line ids, and its cap rises by exactly the entries a new prompt adds,
  with the reason beside it — the probe's own rule for raising it.
- **`scripts/export/manifest.yaml` stays**; everything unlisted there stays
  home, as the maintainer's travel decision of 2026-09-20 says.
- **The ask rule for `codex`** (criterion 61) is named once, beside the
  runner, and a test compares `.claude/settings.json` with it — the pattern
  of `scripts/merge_guard.py`. An agent reaches Codex most easily by typing
  `codex`, and the rule makes that bypass of the leak check visible.
- **`AGENTS.md` gets the 4b row and one sentence**, because every harness,
  Codex included, reads it.
- **`make leakcheck` becomes the real target; the runner gets none.** The
  runner is an entry point like `scripts/harness.py`.
- **The runner does not read the change's class** (answer 3).
