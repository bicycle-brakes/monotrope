---
title: "Research — adhd-frame"
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-q24
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, adhd, prompts, handover]
---

# adhd frame — Research

Phase 1 after [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts
as read on 2026-09-30: this worktree at `f985698` (`origin/main`, merge of
pull request 61), the open pull request 60 at head `8622437`
(`origin/feat/stage-2-codex-glm`), lakeswitch-ai `main` at `09c9d62`.
Everything here was read in this session unless it says "not read". Sections
6 (open points) and 7 (size) were asked for by the caller of this phase; they
are candidates for the phase 1a interview, not decisions.

The evidence for the frame is in its own note,
[`docs/research/2026-09-30-adhd-frame.md`](../../../docs/research/2026-09-30-adhd-frame.md)
(asked for by the bead). This file holds the repository facts.

The change covers two beads:

- Bead `coding-harness-q24` — the ADHD frame in the phase prompts: a plan
  card with a one-line pre-mortem, the appetite stop, the acceptance card, a
  research note; "prose only … No check, no script" (bead description,
  in progress, claimed by the orchestrating session).
- Bead `coding-harness-9ca` — related, open: "`/uebergabe` renamed
  `/handover`; handover always as a pull request"; `AGENTS.md` on `main`
  "still names `/uebergabe`". House rule 4, the other part of its "owed
  item 7", is done (pull request 48, per the bead).

## 1 · The proposal and where it comes from

Source: lakeswitch-ai `journal/2026-09-28-product-start-and-principles.md`,
sections "Package 1, for the session that starts it", "First: the Coding
Harness foundation" (table row 1 and the shared Definition of Done),
"Working well with ADHD", "Three more lenses on the frame", "Hyperfocus",
and its "Addendum, 2026-09-29".

- **What package 1 touches** (journal, "Package 1"): `prompts/03-plan.md`
  (the card with the pre-mortem line), `prompts/04-implement.md` (the
  appetite stop in the format of its four-line stop, the clock in "done:",
  the resumption line), `prompts/07-commit.md` (the acceptance card, an
  English body), the repository's handover skill (renamed to `handover`,
  "always a pull request", closing the skill part of `9ca`), and a research
  note with dated sources.
- **Not in package 1** (same section): the other phase prompts (01, 01a, 02,
  02a, 05, 06) and "the `AGENTS.md` texts; those go with package 1c". The
  caller of this phase adds the `/uebergabe` mention in `AGENTS.md`.
- **"Not to do":** no check, no script, no test; nothing from the not-now
  lists.
- **The frame's rules that package 1 carries** ("Working well with ADHD",
  rules 1, 2, 4, 5, 6):
  - rule 1: work of about an hour or more starts with a card of at most
    five lines — the effect for you, the done-criterion, the appetite, the
    not-now list, one pre-mortem line; "ok" starts it;
  - rule 2: when the appetite is reached, the agent stops once and asks:
    expected / found / continue, cut, park or drop — in the format of the
    four-line stop; inside appetite and scope the agent decides;
  - rule 4: every package ends with
    `done: <evidence> · <time used> of <appetite>`, the time read from the
    clock, not estimated;
  - rule 5: what outgrows the card goes to the not-now list;
  - rule 6: the pull request opens with an acceptance card: what changes for
    you / how it was checked / what could break.
- **The resumption line** ("Hyperfocus", measure 2): the stop ends with
  `Resume: when I start, I will <one action>`.
- **The maintainer's standing preferences** (journal, "Decisions and
  preferences"; the maintainer's user instructions; `AGENTS.md`,
  "Communication and session continuity"): result first, short, one question
  at a time with a recommendation, numbered steps, a clear next step, the big
  picture visible, every step ends in a result the maintainer can see, side
  issues to a named list.

**Parts of the proposal that are stale** (checked against this worktree):

- "Coding Harness `prompts/07-commit.md` still asks for a German body"
  (journal, Definition of Done line 5 and the addendum): no longer true.
  `07-commit.md` says "Subject and body in English" since commit `e3430ea`
  (2026-09-30, part of pull request 54, merge `ba940fb`).
- The worktree path `~/coding-harness-wt/adhd-frame`: superseded by
  `.claude/worktrees/` (journal addendum; `AGENTS.md`).
- The research note's name `2026-09-29-adhd-frame.md`: the note is dated by
  the day it was written, 2026-09-30.
- The journal attributes "g≈0.69" to `PMC9962130`; that is an adult review
  without a pooled effect; the 0.688 is Metcalfe et al. 2024 (research note,
  §6).

## 2 · What exists today

### 2.1 `prompts/03-plan.md`

- Opens with model, result, gate; "You describe **how** the spec is met".
- `Required:` list: every file by name, the verification command, per
  acceptance criterion the test and its fault, what you do not touch, "No
  longer than the change".
- `## Model markings (stage 2 only)`: `[FLASH]`, `[GLM5.3]`, `[SONNET]`, with
  format rules in `templates/plan-marking.md` — **that file does not exist**
  here (`ls templates`: `gate-record.yaml`, `handover.md`; `docs/WORKFLOW.md`
  lists it among the missing pieces).
- `## Questions`: the question protocol; then `/clear`.
- **Not there:** a card, an appetite, a pre-mortem, a not-now list, an
  effect line. `rg -i "appetite|timebox|time.box"` over `prompts/`,
  `docs/WORKFLOW.md`, `AGENTS.md` and `templates/` finds nothing.
- Its gate names `scripts/validate_change_artefacts.py`, which does not exist
  (`docs/WORKFLOW.md`, note "Not all of it is here yet"); so nothing checks
  a plan's shape.

### 2.2 `prompts/04-implement.md`

- Model line "Sonnet 5"; input `plan.md` and `spec.md`; gate `make verify`.
- **"The plan is the contract"** with the four-line stop in a code block:
  `expected:` / `found:` / `relevant:` / `proposal:`; "The plan is then
  revised, never silently overwritten."
- "An ambiguous contract is not yours to settle": mark `[DECISION]`, finish
  what does not depend on it, stop.
- Test with the change, and its counterpart that plants the fault.
- **Not there:** an appetite, a time reading, a "done:" line, a resumption
  line.

### 2.3 `prompts/07-commit.md` and the pull request templates

- Conventional Commits with the bead; "Subject and body in English"; provenance
  trailer; "The pull request text explains itself"; decision pull requests
  (`decide(<scope>): …`, label, `.github/PULL_REQUEST_TEMPLATE/decision.md`,
  the multi-decision block); `Closes-Bead:`; the artefact lifecycle;
  `## The merge` (restate, `--match-head-commit`, the ask rule).
- "Every other pull request takes `.github/pull_request_template.md`."
- **The acceptance card largely exists already, in the templates** (read
  2026-09-30):

  | Card line (journal rule 6) | Ordinary template | Decision template |
  |---|---|---|
  | what changes for you | `**In one line:**`, `## What changes` | `## What changes for you` |
  | how it was checked | `<details>` "Evidence at `<short sha>`" with `make verify` | same |
  | what could break | **absent** | `**Undo:**` under "What your merge confirms" (reversal, not risk) |
  | `done: <evidence> · <time used> of <appetite>` | **absent** | **absent** |
  | your move | `**Your move:** nothing to decide` | `**Your move:** merge … comment … close` |

### 2.4 The handover skill

Three copies, read 2026-09-30:

| Where | Name | Commit rule | `updated:` in its §3a block |
|---|---|---|---|
| `tools/claude-code/skills/uebergabe/SKILL.md` (repository) | `uebergabe` | "Nicht committen, es sei denn, die Person bittet darum." | yes |
| `~/.claude/skills/handover/SKILL.md` (installed, file date 2026-09-27) | `handover` | "Die Übergabe kommt immer als Pull Request, ohne Rückfrage (Regel der Person vom 27.09.2026)" — own worktree and branch from `main`, commit, push, open the pull request; the maintainer merges; exception without a remote or with another session in the same checkout | no |
| `~/.claude/skills/uebergabe/` | — | — | missing |

- The installed copy was edited only in `~/.claude`, against `AGENTS.md`
  ("Change it there and reinstall … never only in `~/.claude`").
- `tools/claude-code/install.sh` lists `skills/uebergabe/SKILL.md` in its
  `files` array; `install.sh --check` on 2026-09-30 prints "missing
  ~/.claude/skills/uebergabe/SKILL.md".
- `tools/claude-code/README.md`: the row `skills/uebergabe/SKILL.md` |
  `/uebergabe`, and "The install copies the six files".
- `tools/claude-code/hooks/handover.sh` (repository) names `/uebergabe` in
  its header comment and in three German display strings (start entry with
  no handover yet, no handover folder, the session-end instruction). The
  installed hook says `/handover` and, in the last one, "als Pull Request
  öffnen (Merge macht die Person)".
- The skill's text is German. House rule 1 allows German for "the texts the
  maintainer's display shows at run time (`tools/claude-code/`)".
- No test names `/uebergabe` or the skill path (`rg` over `tests/`).

**Side finding: the installed display is behind the repository.**
`install.sh --check` (2026-09-30) reports `statusline.sh`, `hooks/recap.sh`,
`hooks/handover.sh` and `hooks/session-scan.sh` as different. The installed
`handover.sh` lacks the trust list of bead `hit` (handover content goes into
a session's context only for repositories listed in
`~/.claude/handover-trust`), in the repository at least since `2dfe2cc`
(2026-09-22, the file's last commit); `~/.claude/handover-trust` does not exist. Consequence: the
first reinstall after this change (needed for the renamed skill to take
effect) also switches on the trust list, and without a trust file the start
entry shows the handover's metadata only, no longer its content.

### 2.5 `AGENTS.md`

- "Sessions across checkouts", last bullet: "The maintainer's Claude Code
  display — status line, entry at session start, handover safety net,
  parallel-session warning, `/uebergabe` — lives in `tools/claude-code/`".
- "Communication and session continuity" already carries most of the
  maintainer's preferences (lead with the main point, one next action, at
  most three priorities, one decision at a time with recommendation and
  consequence, orientation at session start, a dated handover with "one
  concrete resumption action"). It does **not** say that a handover comes as
  a pull request; the maintainer's user instructions do ("Die Übergabe kommt
  immer als Pull Request, aus einem eigenen Worktree, ohne Rückfrage. Mergen
  tue ich.").

### 2.6 `docs/WORKFLOW.md`

- §2 "The five rules": "The plan is the contract … The agent stops and
  reports: expected / found / why it matters / what now"; "From about 60 %
  context use, start a new session anyway"; "Never plan what one sentence
  describes"; "the veto is one word" for reversible decisions; Stage-Gate's
  *kill*, PRINCE2's management by exception.
- §2 "Change classes": `spike`, `bounded`, `feature`, `architectural`; no
  appetite field (the LakeSwitch anchor has one, per
  `plans/changes/harness-decide-adr/research.md`).
- No appetite, card or clock anywhere in the doctrine.

### 2.7 Earlier research here

- `docs/research/2026-09-18-human-planning-and-harness-gaps.md`: a start
  page with one next action and "a visible done condition and effort range
  where useful", a resume breadcrumb, batched interruptions. The "effort
  range" is in tension with "an appetite instead of an estimate".
- `docs/research/2026-09-30-decision-pull-requests.md` §2.4: the writing
  sources, reused by the new note.
- `docs/research/_INDEX.md` does not list the 2026-09-30 decision-PR note.

### 2.8 Gates and tests that read these files

- `tests/test_model_endpoints.py` reads the `**Model:**` line of every
  phase prompt.
- `provenance.yaml`: `prompts/` is `human-written`, `frontmatter: none`;
  `tests/test_frontmatter_current.py` holds that `prompts/04-implement.md`
  carries no header.
- `scripts/kit/probe.py` names the three prompts' model tests; `tools/`
  falls under the kit manifest's catch-all (does not travel).
- Nothing reads the prose of 03, 04 or 07 on `main`. Pull request 60 adds
  tests that do (next section).

## 3 · Overlap with the open pull request 60

Pull request 60 (`decide(workflow): stage 2 — Codex and GLM review Coding
Harness changes`, open, head `8622437`, updated 2026-09-30) stays open by
the maintainer's decision. Its diff against `main` (three-dot, read with
`git diff` and `git show`):

| File | Pull request 60 | Overlap with this change |
|---|---|---|
| `prompts/03-plan.md` | deletes the section `## Model markings (stage 2 only)` (8 lines, between `Required:` and `## Questions`) | a card placed directly after `Required:` touches the same hunk → merge conflict |
| `prompts/04-implement.md` | model line → "Sonnet 5.5 — at effort `medium`" (2 lines); appends "**A foreign finding is taken on evidence.**" at the end | text appended at the end, or next to the model line, conflicts; text inserted after the four-line stop does not |
| `tests/test_stage2.py` (new) | `test_the_plan_prompt_asks_for_no_markings`: 03 must not contain `[FLASH]`, `[GLM5.3]`, `[SONNET]`, `plan-marking`, "Model markings"; `evidence_problems`: 04 must keep three phrases of its new paragraph; `test_the_implement_prompt_names_sonnet_5_5_at_medium` | this change must not write those words into 03 and must not touch 04's model line or last paragraph |
| `AGENTS.md` | adds a row `4b` to the phase table and a "Stage 2" paragraph near the top | no overlap with the `/uebergabe` bullet |
| `docs/WORKFLOW.md` | 296 lines changed | any edit here collides; this change does not need one (section 6, `[DETAIL]`) |
| `prompts/07-commit.md`, `.github/`, `tools/claude-code/` | untouched | none |

With the placements in section 6 (`[DETAIL]`, "Placement"), the two changes
share no hunk, so whichever merges second should rebase without a conflict
(expected from the diffs, not tried).

## 4 · What is unclear

1. **Who answers the appetite stop when the maintainer is not there.** The
   journal says the agent "stops once and asks"; phase runs here are often
   driven by an orchestrating session, and the maintainer is away until
   2026-10-04. Not settled anywhere.
2. **Whether the card waits for an "ok".** Journal rule 1 says "'ok' starts
   it"; `docs/WORKFLOW.md` says for reversible matters "the veto is one
   word". A plan card at phase 3 comes after the interview and the spec.
3. **What "session start after D-60" in bead `9ca`'s title still asks.** The
   bead says house rule 4 is done; no handover under `docs/journal/handover/`
   defines "owed item 7" (`rg`, 2026-09-30). Not found.
4. **How the clock survives `/clear` between phases 3 and 4.** Phase 4 may
   span sessions; nothing records a start time. Claude Code's status-line
   input reportedly carries `cost.total_duration_ms` (journal, "Hyperfocus");
   not verified here, and neither statusline copy reads it (`rg duration`).
5. **Whether `install.sh` and `hooks/handover.sh` count as "a script"** under
   "no script". The rename needs one line in the first and a comment plus
   three display strings in the second; neither adds logic.

## 5 · Files a change would touch

In the proposed scope:

- `prompts/03-plan.md` — the card (effect, done-criterion, appetite, not-now
  list, one pre-mortem line), placed away from pull request 60's hunk.
- `prompts/04-implement.md` — the appetite stop in the four-line format, the
  "done:" line with the clock, the resumption line; inserted after the
  existing stop.
- `prompts/07-commit.md` — the acceptance card (or a pointer to it, section
  6, Q2).
- `tools/claude-code/skills/uebergabe/SKILL.md` → `skills/handover/SKILL.md`
  — name, description and the pull-request rule from the installed copy,
  keeping the repository's `updated:` line.
- `AGENTS.md` — `/uebergabe` → `/handover`.
- `docs/research/2026-09-30-adhd-frame.md` — written in this phase.

Consequential, if the rename is in scope:

- `tools/claude-code/install.sh` — the `files` entry.
- `tools/claude-code/README.md` — the pieces row.
- `tools/claude-code/hooks/handover.sh` — the header comment and three
  display strings.

Only if Q2 goes that way: `.github/pull_request_template.md` and
`.github/PULL_REQUEST_TEMPLATE/decision.md` — a "What could break" line and
the "done:" line.

Not touched: `docs/WORKFLOW.md`, the other prompts, `templates/handover.md`
(German, translation is its own pull request under house rule 1), any test,
check or gate.

## 6 · Open points for the phase 1a interview

Sorted by the question protocol of `docs/WORKFLOW.md`; scope first. Each
`[DECISION]` carries a recommendation that is safe to take provisionally
while the maintainer is away (until 2026-10-04).

**Q1 `[DECISION]` — Does the handover-skill rename travel in this pull
request?**
Goal: the frame reaches the prompts, and the handover rule the maintainer
set on 2026-09-27 reaches the repository.

- (a) **Yes, with its consequential lines:** the skill renamed with the
  pull-request rule, `/uebergabe` → `/handover` in `AGENTS.md`, the
  `install.sh` entry, the README row and the hook's display strings.
  Consequence: one pull request closes both beads; two shell files change
  text, not logic; the maintainer reinstalls once, which also brings the
  newer hooks (section 2.4, side finding).
- (b) Prompts only; the rename is its own pull request. Consequence: two
  reviews, two things waiting.
- (c) Skill file and `AGENTS.md` only, without `install.sh`. Consequence:
  `install.sh` would copy a file that no longer exists and abort under
  `set -e` — broken. Not safe.

Recommendation: **(a)**. The rule is already the maintainer's (2026-09-27),
the edits are text, and "no script" reads as "no new mechanism". If "ok":
the pull request says in its first lines that a reinstall is the
maintainer's step, to run `install.sh --check` first, and that the trust
list then applies.

**Q2 `[DECISION]` — Where does the acceptance card live?**
Most of it already exists in the pull request templates (section 2.3).

- (a) Prose in `07-commit.md` only, as proposed. Consequence: a second
  description of the pull request body beside the templates — two places
  that drift.
- (b) Add the two missing lines — "What could break" and
  `done: <evidence> · <time used> of <appetite>` — to both templates, and one sentence in
  `07-commit.md` that points to them. Consequence: touches `.github/`
  templates (text, no check); every pull request shows the card at once.
- (c) Nothing; the templates are close enough. Consequence: the "done:" line
  with the clock never reaches the maintainer.

Recommendation: **(b)** — the template is what an agent actually fills, and
`07-commit.md` already defers to it. If "ok": the card is complete in every
new pull request.

**Q3 `[DECISION]` — Does the plan card wait for the maintainer's "ok"?**

- (a) Yes, phase 4 starts only after "ok" (journal rule 1). Consequence: one
  more waiting point per change; orchestrated runs stall while the
  maintainer is away.
- (b) The card is shown when phase 3 ends; phase 4 starts unless the
  maintainer vetoes. An "ok" is asked only when the card widens the scope or
  the appetite that the interview or spec set. Consequence: no new waiting
  point; a wrong appetite is caught by the stop it sets.

Recommendation: **(b)** — it matches "the veto is one word" in
`docs/WORKFLOW.md` and management by exception. If "ok": the card says
"starts unless you say stop" in its last line.

**Q4 `[DECISION]` — Who may answer the appetite stop?**

- (a) Only the maintainer; without an answer the work parks and goes into
  the handover.
- (b) An orchestrating session may answer *cut*, *park* or *drop* (the
  change gets smaller or stops), never *continue*; only the maintainer
  extends an appetite. Consequence: nothing grows without the maintainer,
  and an orchestrated run can still finish a smaller version.
- (c) Anyone who can answer. Consequence: the stop loses its point.

Recommendation: **(b)**. If "ok": the stop's format lists the four answers
and says who may give "continue".

`[GAP]`s — read, do not ask:

- What `9ca`'s "session start after D-60" still requires (section 4, item
  3): read `9ca`'s history and lakeswitch-ai D-60 before the spec; if it is
  only house rule 4, `9ca` closes with this change.
- Whether Claude Code's status-line input carries a session duration
  (section 4, item 4): read the Claude Code documentation on the status
  line; relevant only for a later display change, not for this prose.

`[DETAIL]`s — the agent decides, with the reason in the artefact:

- **Placement.** In `03-plan.md` the card goes before `Required:` (the card
  is the first thing a plan shows, and pull request 60 deletes the section
  after `Required:`). In `04-implement.md` the appetite stop, the "done:"
  line and the resumption line go directly after the four-line stop's
  paragraph, away from pull request 60's model line and closing paragraph.
- **Words.** No `[FLASH]`, `[GLM5.3]`, `[SONNET]`, "Model markings" or
  `plan-marking` in 03 (pull request 60's test).
- **The clock.** `date` at the start of phase 4 and at the "done:" line;
  elapsed wall-clock time, breaks included and said so; if phase 4 spans
  sessions, each stop or handover states its own span and the total is their
  sum. Reason: readable by any harness, nothing to install.
- **No default appetite number in the prompts.** The card states one; the
  journal's "about two hours per package" stays an example. Reason: a number
  in the prompt becomes a rule nobody chose.
- **Every `plan.md` gets the card.** "Never plan what one sentence
  describes" already keeps small work out of phase 3, so the journal's "an
  hour or more" threshold adds nothing.
- **The resumption line is the handover's "Next step"** when the session
  ends at a stop; one action, starting with a verb.
- **`docs/WORKFLOW.md` is not edited.** The journal assigns doctrine texts
  to package 1c, and pull request 60 rewrites the file; the prompts carry
  the instruction.
- **The skill keeps German and the repository's `updated:` line**; the
  rename uses `git mv` so its history follows.
- **Research index.** `docs/research/_INDEX.md` gets a row for the new note
  in this phase; the missing row for the decision-PR note goes to the
  not-now list.

Not now (side findings): the installed display behind the repository
(section 2.4) as its own bead; `templates/plan-marking.md` missing while
`03-plan.md` names it (pull request 60 removes the reference); the
decision-PR note missing from `_INDEX.md`; a session clock in the status
line (journal, "Hyperfocus", measure 1); the "effort range" wording of the
2026-09-18 note.

## 7 · Size and the smallest version (requested by the caller)

Rough sizes, from the file lengths read here (03: 45 lines, 04: 31, 07: 97
at `f985698`):

| Package | Size |
|---|---|
| spec and plan for prose (phases 2–3) | 0.5–1 h |
| 03 card, 04 stop + "done:" + resumption line (about 25 prose lines) | 0.5 h |
| acceptance card: two template lines each, one sentence in 07 (Q2 b) | 0.25 h |
| skill rename with its consequential lines and `AGENTS.md` (Q1 a) | 0.5 h |
| review (phase 6) and pull request | 0.5–1 h |

Total: **S, about 2.5–3 h, one session, one pull request.**

**Smallest useful version:** the appetite stop with the clock in "done:" and
the resumption line in `04-implement.md`, and the card with its pre-mortem
line in `03-plan.md` — the two pieces that change how the next session runs.
If time is short, the acceptance-card lines and the rename follow as a
second pull request (Q1 b), not as a half-done first one.
