---
title: "Spec — adhd-frame"
status: accepted
implementation_status: done
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-q24
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, adhd, prompts, pull-request-templates, handover]
class: bounded
---

# Spec — adhd-frame

> **Provisional — awaits the maintainer's confirmation at the merge.** The
> four answers in `decisions.md` were taken by the orchestrating session
> while the maintainer is away (until 2026-10-04); this spec honours them
> exactly and does not reopen them. The class of this change is provisional
> in the same way ("Open decisions", item 1). Nothing here takes effect
> before the maintainer merges the pull request, and its body lists each of
> these for confirmation (criterion 34).

Phase 2 after [`prompts/02-spec.md`](../../../prompts/02-spec.md). Inputs:
[`research.md`](research.md), [`decisions.md`](decisions.md) and the research
note [`docs/research/2026-09-30-adhd-frame.md`](../../../docs/research/2026-09-30-adhd-frame.md).
Facts read on 2026-09-30 at this branch's `5bb3d58` (on `origin/main`
`f985698`), the open pull request 60 at head `bd39160`, and lakeswitch-ai
`main` at `09c9d62`.

## Problem

A person with ADHD loses time and the next step first, and this workflow
gives neither a place (research note, §2.1, §2.5). Today (`research.md` §2):

- **A plan has no frame.** `prompts/03-plan.md` asks for files, the
  verification command and tests; it asks for no effect line, no
  done-criterion the maintainer can read, no appetite, no not-now list and no
  pre-mortem. `rg -i "appetite|timebox"` over `prompts/`, `docs/WORKFLOW.md`,
  `AGENTS.md` and `templates/` finds nothing.
- **Implementation has no time stop and no end line.**
  `prompts/04-implement.md` stops when the plan no longer holds, never
  because time ran out; it reads no clock, ends without a "done:" line, and
  leaves no resumption point when a session ends mid-work.
- **The pull request says what changes, not what could break or what it
  cost.** Both templates carry the effect and the evidence; neither has a
  "what could break" line or a `done: <evidence> · <time used> of <appetite>`
  line (`research.md` §2.3, table).
- **The handover skill in the repository contradicts the maintainer's rule.**
  `tools/claude-code/skills/uebergabe/SKILL.md` says, in German, not to
  commit unless asked; the maintainer ruled on 2026-09-27 that a handover always comes as
  a pull request from its own worktree, merged by the maintainer. That rule
  exists only in an installed copy edited in `~/.claude`, against
  `AGENTS.md` ("never only in `~/.claude`"). `install.sh --check` reports the
  repository's skill as missing there, and `AGENTS.md` still names
  `/uebergabe` (`research.md` §2.4, §2.5; bead coding-harness-9ca).

## Terms

- **The card** — the block that opens every `plan.md` (criteria 1–2).
- **Appetite** — the time the maintainer is willing to spend on phase 4 of a
  change; a stop, not an estimate.
- **Time used** — criterion 9.
- **Widens** — a card widens the *scope* when its `For you:` or `Done when:`
  line includes something `spec.md` names as a non-goal or no acceptance
  criterion of `spec.md` covers. It widens the *appetite* when its
  `Appetite:` is larger than an appetite `decisions.md` or `spec.md` states.
  Where neither states one, the card's appetite is the first and widens
  nothing.
- **Orchestrating session** — a session, not the maintainer, that starts and
  answers the sessions or subagents that run the phases.
- **The two pull request templates** — `.github/pull_request_template.md`
  (ordinary) and `.github/PULL_REQUEST_TEMPLATE/decision.md` (decision).

## Acceptance criteria

Each criterion holds one condition. "The prompt" means the file its group
names, as this change leaves it.

### The plan card — `prompts/03-plan.md`

1. The prompt requires every `plan.md` to open with the card, directly after
   the plan's header and title and before any other content.
   *Refuted by:* prompt text that lets a plan omit the card or put it after
   other content.

2. The prompt names the card's five content lines in this order, each with
   its label: `For you:` (what changes for the maintainer), `Done when:` (the
   evidence that will show it holds), `Appetite:` (time for phase 4, a stop,
   not an estimate), `Not now:` (what is left out), `Pre-mortem:`.
   *Refuted by:* a label missing, renamed or out of this order.

3. The prompt limits the pre-mortem to one line of the form
   `suppose it failed: most likely because <one reason>`.
   *Refuted by:* prompt text asking for a list of risks or for more than one
   line.

4. The prompt fixes the last line of a card that widens nothing as
   `Starts unless you say stop.`
   *Refuted by:* another last line for such a card, or none.

5. When phase 3 ends, the prompt requires the card to be shown to the
   maintainer in the phase's closing message, identical to the card in
   `plan.md`.
   *Refuted by:* prompt text that leaves the card only in the file.

6. While the maintainer has not said stop, the prompt lets phase 4 start
   once the card has been shown, without waiting for an "ok".
   *Refuted by:* prompt text requiring an "ok" for a card that widens
   nothing.

7. If the card widens the scope or the appetite, the prompt requires the
   maintainer's "ok" before phase 4 starts, and the card's last line names
   what widens and asks for that "ok" in place of `Starts unless you say
   stop.`
   *Refuted by:* prompt text that lets a widening card start phase 4 on
   silence.

8. The lines this change adds to `prompts/03-plan.md` and
   `prompts/04-implement.md` give no figure as a default or example
   appetite.
   *Refuted by:* an added line with a number of hours or minutes
   (`git diff origin/main -- prompts/03-plan.md prompts/04-implement.md | grep '^+' | grep -E '[0-9]+ ?(h|hours?|min|minutes?)([^a-z]|$)'`
   printing a line).

### The appetite stop, the clock and the resumption line — `prompts/04-implement.md`

9. The prompt defines time used as the sum of the spans of the sessions that
   worked under the phase-4 prompt on this change, each span read with
   `date` at ~~the session's start~~ *(changed in repair round 2, F-8 of the
   round-2 review: its start, which is a session's start or the point where
   work resumes)* and at its end (its stop, resumption line or "done:" line)
   ~~*(added in repair round 1, F-1 and F-2 of the phase-6 review: and, while
   work goes on, at each step boundary and before each commit; a stop ends a
   span, and work that resumes starts a new one, in the same conversation
   too)* with breaks inside a session counted and said to be counted~~
   *(split off in repair round 2, F-9 of the round-2 review, so that this
   criterion holds one condition: the readings during work are criterion 42,
   the stop and the resumed span 43, the breaks 44)*.
   *Refuted by:* prompt text allowing an estimated or remembered time, not
   naming `date`, or counting the time between two sessions; ~~*(added in
   repair round 1)* prompt text that names no reading of `date` between a
   session's start and its end~~ *(changed in repair round 2: prompt text
   that names no reading of `date` at a span's start, whether a session's
   start or where work resumes, or none at its end)*.

10. When ~~the time used reaches the card's appetite~~ *(changed in repair
    round 1, F-1 of the phase-6 review: a reading of `date` during work shows
    that the time used has reached the card's appetite)*, the prompt requires
    the agent to stop once and report in the labels of the existing four-line
    stop, in its order: `expected:` (the appetite and the done-criterion),
    `found:` (the time used by the clock, what holds and what is open),
    `relevant:` (what the open part needs), `proposal:`.
    *Refuted by:* other labels, another order, or a `found:` without the time
    read from the clock.

11. The prompt gives the appetite stop's `proposal:` exactly four answers —
    continue, cut, park, drop — and requires the agent to recommend one of
    them.
    *Refuted by:* an answer missing, a fifth answer, or no recommendation.

12. The prompt states what each answer does: *continue* — the maintainer
    names a new appetite; *cut* — the done-criterion narrows to what already
    holds, only the work that makes that part pass its verification follows,
    and what is cut is named as not-now in the stop and in the pull request;
    *park* — work stops and stays on its branch, and the session ends with
    the resumption line; *drop* — the change is abandoned and the reason goes
    into the handover.
    *Refuted by:* an answer without its effect, or a *cut* that lets new
    building continue.

13. If the appetite stop is answered by anyone other than the maintainer,
    the prompt allows only cut, park or drop, and says that only the
    maintainer may answer continue.
    *Refuted by:* prompt text letting an orchestrating session answer
    continue.

14. While the appetite stop waits for an answer, the prompt forbids building
    further, and parks the work if the session must end first.
    *Refuted by:* prompt text letting work go on while the stop is open.

15. The prompt raises the appetite stop once per appetite: after continue,
    the next appetite stop comes when the new appetite is reached, and no
    reminder, countdown or check-in comes before it *(clarified in repair
    round 1, F-1: these are timers and messages to the maintainer; the agent's
    own readings of `date` during work are none of them)*.
    *Refuted by:* prompt text asking for interim check-ins, reminders or a
    countdown.

16. When phase 4 ends, the prompt requires its last line to read
    `done: <evidence> · <time used> of <appetite>`, where the evidence names
    the verification command, its result and the short commit.
    *Refuted by:* prompt text without this form, or one that accepts "done"
    without a command, a result and a commit.

17. If `plan.md` carries no card, the prompt runs phase 4 without an
    appetite stop and ends its "done:" line with `of no appetite set`.
    *Refuted by:* prompt text without this case, or one that has the agent
    set an appetite itself.

18. When a phase-4 session ends before its "done:" line — at the appetite
    stop, the four-line stop, a `[DECISION]` or the maintainer's stop — the
    prompt requires its last line to read
    `Resume: when I start, I will <one action>`, one action that begins with
    a verb and names the file, command or test it starts from.
    *Refuted by:* prompt text without the line, or one that allows more than
    one action.

19. If that session writes a handover, the prompt makes the resumption line
    the handover's "Next step".
    *Refuted by:* prompt text without this sentence.

### The acceptance card — the two pull request templates and `prompts/07-commit.md`

20. Each of the two templates carries a line labelled `**What could break:**`
    directly below its `**Your move:**` line and before its first `##`
    heading.
    *Refuted by:* either template without the line, or with it below a
    heading.

21. Each of the two templates carries, below the "What could break" line and
    before its first `##` heading, a line of the form
    `done: <evidence> · <time used> of <appetite>`; placeholders may say more,
    but `done:`, ` · ` and ` of ` stay.
    *Refuted by:* either template without such a line.

22. `tests/test_pr_templates.py` passes unchanged.
    *Refuted by:* `python3 -m pytest tests/test_pr_templates.py -q` red, or
    any diff to that file.

23. `prompts/07-commit.md` gains exactly one sentence, which names the
    acceptance card — what changes for you, how it was checked, what could
    break, and the "done:" line — and says that both templates carry it and
    every pull request body keeps it, the multi-decision form included
    ~~*(added in repair round 1, F-5 of the phase-6 review: and the two new
    lines, "What could break" and the "done:" line, stand in the
    multi-decision form that file already prints, directly below its
    `**Your move:**` line)*~~ *(split off in repair round 2, F-9 of the
    round-2 review, so that this criterion holds one condition: the two lines
    in the form are criterion 46)*.
    *Refuted by:* more than one added sentence, a second copy of the
    template's lines (a list or a code block) *(except the two lines of
    criterion 46, as repair round 1 allowed)*, or no pointer to the
    templates; ~~*(added in repair round 1)* a multi-decision form without
    either line~~ *(moved to criterion 46, which refutes a form that lacks
    either one)*.

### The handover skill — `tools/claude-code/` and `AGENTS.md`

24. The skill is `tools/claude-code/skills/handover/SKILL.md`, git records it
    as a rename of `tools/claude-code/skills/uebergabe/SKILL.md`, and the old
    directory no longer exists.
    *Refuted by:* `git diff -M --name-status origin/main...HEAD` without an
    `R` line for the file, or the old path present.

25. The skill's frontmatter reads `name: handover`, and its description says
    that it always opens a pull request for the handover and links both.
    *Refuted by:* another name, or a description without the pull request.

26. The skill's section 4 replaces "Nicht committen, es sei denn, die Person
    bittet darum." with the pull-request rule of the installed copy (read
    2026-09-30): always a pull request, without asking; its own worktree and
    branch from the current `main` — in coding-harness
    `.claude/worktrees/<name>`, branch `docs/handover-<date>-<topic>`; in
    lakeswitch `~/lakeswitch-wt/<name>`, branch `docs/journal-<date>-<topic>`;
    in a repository that names no place, `.claude/worktrees/<name>`;
    committing, pushing and opening the pull request belong to the handover;
    only the maintainer merges; commit message and pull request text in
    English; and the exception for a repository without a remote or with
    another session in the same checkout.
    *Refuted by:* the old sentence still there, any of these parts missing,
    or text that lets an agent merge.

27. The skill's section 5 ends with committing, pushing and opening the pull
    request, and a closing message that links the handover file and the pull
    request and says the merge is the maintainer's.
    *Refuted by:* a section 5 without these steps.

28. The skill keeps the line `updated: <JJJJ-MM-TT>` in its section 3a
    block.
    *Refuted by:* the line missing — every handover the skill writes would
    then be reported by the gate `frontmatter-current`.

29. `tools/claude-code/install.sh` names `skills/handover/SKILL.md` in its
    `files` list where it named `skills/uebergabe/SKILL.md`, and no other line
    of it changes.
    *Refuted by:* another changed line, or `bash -n tools/claude-code/install.sh`
    failing.

30. `tools/claude-code/README.md` names `skills/handover/SKILL.md` and
    `/handover` in its table of pieces and says the skill opens a pull
    request for the handover.
    *Refuted by:* the row still naming `uebergabe`, or no pull request in it.

31. `tools/claude-code/hooks/handover.sh` says `/handover` in its header
    comment and its three display strings that named `/uebergabe`, its
    session-end instruction says the handover is opened as a pull request and
    merged by the maintainer, and no other line changes.
    *Refuted by:* `python3 -m pytest tests/test_handover_entry.py -q` red,
    another changed line, or `bash -n tools/claude-code/hooks/handover.sh`
    failing.

32. `AGENTS.md` names `/handover` where its display bullet named
    `/uebergabe`, and no other line of `AGENTS.md` changes *(changed in repair
    round 2, F-4 of the round-2 review: except the one bullet of criterion
    47)*.
    *Refuted by:* `git diff origin/main -- AGENTS.md` showing another line
    *(than that bullet)*.

33. While this change is implemented, no agent runs
    `tools/claude-code/install.sh` other than with `--check`.
    *Refuted by:* a `*.bak-<timestamp>` file under `~/.claude` with a
    timestamp inside the change's work, or `~/.claude/skills/handover/SKILL.md`
    or `~/.claude/hooks/handover.sh` no longer matching their SHA-256 of
    2026-09-30 (prefixes `24c1e0a34cda875a` and `cc52269aaf14e17a`).

### The pull request

34. The pull request's body lists, for the maintainer's confirmation, the
    four provisional answers of `decisions.md` and the provisional class of
    this spec.
    *Refuted by:* a body that lacks any of the five.

35. The pull request's body names the reinstall as the maintainer's step —
    `tools/claude-code/install.sh --check` first, then the install and a
    restart — and says that the install also brings the newer hooks, which
    turn on the handover trust list: without `~/.claude/handover-trust`, the
    start entry shows a handover's metadata, no longer its content.
    *Refuted by:* a body without the step, the `--check`, or the trust-list
    consequence.

36. The pull request's body names bead coding-harness-q24 as closed by it
    and bead coding-harness-9ca as changed and still open, with what remains
    of it.
    *Refuted by:* 9ca declared closed, or either bead not named.

### Boundaries

37. The change touches only these paths, beside its own artefacts under
    `plans/changes/archive/2026-09-30-adhd-frame/`, the regenerated `plans/INDEX.md`, and the
    research note and `docs/research/_INDEX.md` of phase 1:
    `prompts/03-plan.md`, `prompts/04-implement.md`, `prompts/07-commit.md`,
    the two pull request templates, the skill (old and new path),
    `tools/claude-code/install.sh`, `tools/claude-code/README.md`,
    `tools/claude-code/hooks/handover.sh` and `AGENTS.md`.
    *Refuted by:* `git diff --name-only origin/main...HEAD` naming another
    path — any file under `scripts/`, `tests/` or `decisions/` among them.

38. In `prompts/03-plan.md` and `prompts/04-implement.md` the diff against
    `origin/main` only adds lines: in 03 above the line `Required:`, in 04
    between the paragraph that ends "it is the plan." and the paragraph "An
    ambiguous contract is not yours to settle."
    *Refuted by:* a removed or changed line, or an added line elsewhere.

39. No line this change adds to `prompts/03-plan.md` contains `[FLASH]`,
    `[GLM5.3]`, `[SONNET]`, `plan-marking` or `Model markings`.
    *Refuted by:* `git diff origin/main -- prompts/03-plan.md | grep '^+' | grep -F -e '[FLASH]' -e '[GLM5.3]' -e '[SONNET]' -e plan-marking -e 'Model markings'`
    printing a line.

40. A trial merge with pull request 60 has no conflict:
    `git merge-tree --write-tree HEAD origin/feat/stage-2-codex-glm` exits 0,
    measured at that branch's head at the time of the check (`bd39160` on
    2026-09-30; exit 0 at `5bb3d58`).
    *Refuted by:* exit status 1 or a conflicted file listed.

41. `make verify` is green at the head of the pull request.
    *Refuted by:* any gate red.

### Added in repair round 2

Criteria 42 to 47 are appended and nothing above is renumbered. 42 to 44 and
46 split criteria 9 and 23 (F-9 of the round-2 review); 45 holds the rule added
for F-3 of the phase-6 review; 47 holds the rule added for F-4.

42. While work goes on, the prompt requires a reading of `date` between steps
    and another before each commit.
    *Refuted by:* prompt text that names only one of the two moments, or
    neither.

43. The prompt splits a span at a stop: the stop ends it, and work that
    resumes, in the same conversation too, starts a new one.
    *Refuted by:* prompt text that lets a span run on across a stop, or that
    names no new span for work resumed in the same conversation.

44. The prompt counts a break inside a session as work and says the record
    notes it.
    *Refuted by:* prompt text that leaves a break out of the time used, or
    that does not say the record notes it.

45. When the appetite stop is answered, the prompt requires the answer — a
    new appetite or a narrowed done-criterion, which replaces the card's
    line, or park or drop — to be written under `## Time used` in `plan.md`.
    *Refuted by:* prompt text that leaves the answer in the chat only, that
    names no place for it in `plan.md`, or that leaves a new appetite or a
    narrowed done-criterion beside the card's old line without saying which
    one holds.

46. The multi-decision form that `prompts/07-commit.md` prints carries both
    lines of the acceptance card, `**What could break:**` and the `done:`
    line, each as its own paragraph directly below its `**Your move:**` line
    and above its first `##` heading.
    *Refuted by:* a form that lacks either line, or that puts either one
    below a `##` heading or above `**Your move:**`.

47. The rule that an orchestrating session shows a sub-agent's plan card to
    the maintainer unchanged, the veto staying the maintainer's, stands in
    `prompts/03-plan.md` and in `AGENTS.md`.
    *Refuted by:* either file without the rule, or a rule that leaves the
    veto to anyone but the maintainer.

## Non-goals

In this change, not now:

- **The other phase prompts** (01, 01a, 02, 02a, 05, 06) and
  `docs/WORKFLOW.md`: they go with package 1c, and pull request 60 rewrites
  `docs/WORKFLOW.md`.
- **Any other `AGENTS.md` text** *(except the one bullet of criterion 47,
  added in repair round 2)*. The pull-request rule for handovers is not
  added to "Communication and session continuity" here; it stands in the
  skill and the hook. The rest of bead coding-harness-9ca — owed item 7 of
  the LakeSwitch decision record (session start through `harness home`, a
  handover drafted by the session-end hook and acknowledged, limits named by
  their key) — needs mechanisms Coding Harness does not have and is "the
  maintainer's own edit" there, so 9ca stays open.
- **Any check, script, gate or new test.** A rule becomes a check only after
  it has been broken twice (research note, §4).
- **Running the reinstall**, and the installed display being behind the
  repository (research §2.4, side finding) — its own bead, for the tracker
  writer.
- **A session clock in the status line** (the journal's "Hyperfocus",
  measure 1), and whether Claude Code's status-line input carries a session
  duration (not read; nothing here depends on it).
- **Parking the irreversible after the stop** (a "to sign" list in 07 and
  `AGENTS.md`), the cap of three things waiting, and showing the oldest
  not-now item at session start: parts of the frame outside package 1.
- **An appetite or checkpoint figure** anywhere in the prompts.
- **Translating** the skill or `templates/handover.md` into English: each is
  its own pull request (house rule 1, bead coding-harness-yim).
- `templates/plan-marking.md`, which `prompts/03-plan.md` names and which
  does not exist: pull request 60 removes the reference.
- The missing `docs/research/_INDEX.md` row for the decision-PR note, and the
  "effort range" wording of the 2026-09-18 note.

## Open decisions

The four questions of phase 1a are answered provisionally in `decisions.md`
(the rename travels here; the acceptance card lives in the templates; the
card starts phase 4 unless the maintainer says stop; only the maintainer
answers continue). This spec does not reopen them. One question arose here.

### [DECISION] 1 — The class of this change (provisionally answered: `bounded`)

The spec author states the class and the maintainer's review of the pull
request holds it (`plans/changes/harness-decide-adr/spec.md`, non-goals).
Here the two definitions both read plausibly, and the choice decides whether
the maintainer is asked the ADR question, so it is written out and taken
provisionally with the recommendation, like the answers in `decisions.md`.

```
Goal in one sentence:  Is this change a small change to existing texts, or a
                       feature that needs your yes-or-no on "does it need an
                       architecture decision record"?
Options:
  1. bounded.          It changes existing, readable texts — three prompts,
                       two templates, one skill — and adds no mechanism.
                       Consequence: no ADR question; every gate stays green
                       while you are away; your review of the pull request
                       is the only hold on the class.
  2. feature.          It changes what agents must do in phases 3 and 4.
                       Consequence: the header gains `change:` and
                       `adr_question` (proposal: "no" — prose defaults, no
                       subsystem, interface or trust boundary), and the gate
                       `adr-answers` keeps `make verify` red until you answer
                       with `python3 scripts/harness.py decide adr`, not
                       before 2026-10-04.
Recommendation:        Option 1 — because nothing here is architecture, and
                       a red tree until your return would stop phase 4 for a
                       question whose proposal is "no".
If you say "ok":       `class: bounded` stays; nothing else follows.
What is lost:          Option 2 would record your explicit "no ADR" for this
                       change in `decisions/answers/adhd-frame/adr.yaml`.
```

The weak point of option 1: `bounded` reads "without deciding anything new",
and this change sets new defaults — the veto by default and who may answer
continue. Those are the maintainer's provisional answers, recorded in
`decisions.md`, not architecture.

### `[GAP]`s — closed by reading

- **What bead 9ca's "session start after D-60" still asks.** Read in
  lakeswitch-ai at `09c9d62`: the decision record's "What is owed outside
  this record", Coding Harness item 7, is "`AGENTS.md`, session start and
  handover — as LakeSwitch item 13", and item 13 lists `harness home`, a
  hook-drafted and acknowledged handover, D-60's tracker rule and limits by
  key. House rule 4 carries D-60's tracker rule (pull request 48); the rest
  is not in this change (non-goals).
- **The worktree places the skill names.** `AGENTS.md` here:
  `.claude/worktrees/<name>`; lakeswitch-ai `AGENTS.md` at `09c9d62`, lines
  67–69: `~/lakeswitch-wt/<name>`; portfolio-agentic-engineering `AGENTS.md`
  at `20a279c` names none. Handover branches here are named
  `docs/handover-<date>-<topic>` (merges of pull requests 59 and 61).
- **Which tests pin the touched texts.** `tests/test_pr_templates.py` pins
  the ordinary template's third line (`**Your move:** nothing to decide.`),
  the decision line within the decision template's first three lines, one
  alert in the decision template and none in the ordinary one, no table or
  checkbox, and exactly one HTML comment in the decision template.
  `tests/test_handover_entry.py` runs the hook and pins "Übergabe:",
  "keinen Übergabe-Ordner", "nicht automatisch eingelesen" and
  "Vertrauensliste". No test names `/uebergabe` or the skill path. Pull
  request 60's `tests/test_stage2.py` reads the `**Model:**` paragraph of 04,
  the phrases of the paragraph it appends to 04, and the marking words in 03. With
  the placements below, **no existing test needs a change**; if one goes
  red, the placement is wrong, not the test.
- **Whether the pull request decides.** No touched path is `human-decided`
  in `provenance.yaml` (`prompts/`, `.github/` and `AGENTS.md` are
  `human-written`; `tools/` has no entry), so it is an ordinary pull request
  with the ordinary template.

### `[DETAIL]` — decided here, with the reason

Each is reversible and binds nothing beyond this change.

- **The card's labels** are `For you:`, `Done when:`, `Appetite:`,
  `Not now:`, `Pre-mortem:`, then the closing line. "For you" matches the
  templates' "What changes for you". The journal's "at most five lines"
  counts the content; the closing line is the veto, not content.
- **Every `plan.md` gets the card**, without the journal's "an hour or more":
  "never plan what one sentence describes" already keeps small work out of
  phase 3.
- **The appetite bounds phase 4**, including repair rounds that return to
  the phase-4 prompt, not phases 5 to 7. The stop lives only in the phase-4
  prompt; a clock that also ran through phases whose prompts have no stop
  would report an overrun nobody could have stopped. The pull request's
  "done:" line repeats phase 4's last one.
- **The clock is `date`**, and time used is the sum of session spans. Any
  harness can read it and nothing is installed; a night between two sessions
  is not work, a coffee inside one is counted and said to be.
- **Cut builds nothing new.** A cut that went on building would be a
  continue under another name, and continue is the maintainer's
  (`decisions.md`, item 4).
- **An unanswered stop stands.** A stop that lapses into continuing is no
  stop; parking is the one move that loses nothing.
- **A plan without a card has no appetite stop.** Plans written before this
  change must not stop at an appetite nobody set, and `of no appetite set`
  keeps that visible.
- **The resumption line is the handover's "Next step"**: one action, verb
  first, so the start hook's entry line shows it.
- **No figure as a default appetite.** A number in a prompt becomes a rule
  nobody chose; the journal's "about two hours" stays an example there.
- **Placement in 03: above `Required:`.** The card is the first thing a plan
  shows, and pull request 60 deletes the section after `Required:`.
- **Placement in 04: after the four-line stop's paragraph.** The appetite
  stop reuses that format, and the gap is away from pull request 60's model
  line and closing paragraph.
- **Placement in the templates: directly below `**Your move:**`.** The first
  screen then carries the whole card, next to the action it concerns (W3C
  COGA 4.8.3, research note §2.8). In the decision template "What could
  break" stands beside `**Undo:**`, which says how to reverse, not what may
  fail.
- **The sentence in 07 closes the bullet "The pull request text explains
  itself"**, which is where 07 describes the body. Pull request 60 does not
  touch 07.
- **No new test, and no test edited.** The bead says prose only, and the
  frame's own rule keeps a check away until a rule is broken twice. Each
  criterion is refuted by a command the plan names (`grep`, `git diff`,
  `git merge-tree`, the existing tests), not by a committed test.
- **The skill takes the installed copy's rule text**, the maintainer's own of
  2026-09-27, and adds only the worktree place per repository; where a
  repository names none, `.claude/worktrees/<name>`, Claude Code's own place.
  It stays German (house rule 1 names `tools/claude-code/`; translating in
  passing is what the same rule forbids), keeps its `updated:` line, and
  moves with `git mv` so its history follows.
- **The hook's session-end string takes the installed copy's wording.**
- **This spec sets no appetite.** `research.md` §7's sizes are an estimate;
  under criterion 7, the plan's card sets the first one.
