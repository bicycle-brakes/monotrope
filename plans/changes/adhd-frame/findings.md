---
title: "Findings — adhd-frame"
category: findings
created: 2026-09-30
updated: 2026-09-30
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-q24
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, adhd, prompts, pull-request-templates, handover]
---

# Findings — adhd-frame

Phase 6, round 1, on commit `306b5ac` (branch `docs/adhd-frame`, eight
commits over `origin/main` at `f985698`), 2026-09-30. The reviewer ran on
Opus 5.5 in a fresh context, wrote nothing but this file and the regenerated
`plans/INDEX.md`, opened no pull request, wrote nothing to the tracker and
changed nothing under `~/.claude`. Measured against `spec.md` (criteria
1–41, non-goals) and the provisional answers in `decisions.md`; `plan.md`
was read for its card, its checks and its time record, not as the
yardstick. Phase 2a was skipped, so its three questions are answered here
as rows of dimension `SPEC`. `templates/findings.md` does not exist in this
repository yet (`docs-links` reports the dead link); the columns are those
of the earlier `findings.md` files.

**Verdict: no BLOCKER, no `[AMBIGUITY]`, no `[DIVERGENT]`.** One MAJOR, six
MINOR, all open. The MAJOR is that the appetite stop has no moment at which
the clock is read while work goes on, so it can only be noticed at the end;
it is a one-clause gap in 04's text, recorded for a repair round or the
maintainer, not fixed here.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MAJOR | MAINT | base | `prompts/04-implement.md`, lines 25–31 and 50–52 | The appetite stop has no trigger. The prompt names exactly two moments to read the clock — "when a session starts and when it ends" — and then says to stop "when the time used reaches the appetite". Nothing tells the agent to read `date` again while it works, and the rule a few lines later ("no reminder, countdown or check-in before it") makes an agent less likely to look on its own. Case: a card with an appetite of two hours, one phase-4 session that works for five; followed literally, the agent reads `date` at the start and next at its "done:" line, so the first moment time used can be compared with the appetite is after the whole overrun — the stop becomes a report of it. The accounting part is sound (`date`, spans summed, written to `plan.md`); the stop's trigger is what is missing. The spec is silent on it too: criterion 9 names only the start and end reads, criterion 10 needs a comparison during work. [criteria 9, 10, 15] | open |
| F-2 | MINOR | MAINT | base | `prompts/04-implement.md`, lines 25–30 | A span ends "at its stop", but nothing starts a new one when the same session goes on after the answer. Case: a phase-4 session stops at the four-line stop at 18:00, appends its span, and the maintainer answers at 09:00 the next day in the same conversation (or resumes it with `claude --resume`). The session never "starts" again, so either the agent counts the night as "a break inside a session" — time used jumps by fifteen hours and the next reading fires a spurious appetite stop, which, while the maintainer is away, an orchestrating session can only answer with cut, park or drop — or it opens a second span the prompt does not name. The spec's own reason ("a night between two sessions is not work") favours the second reading, so this is recorded as a gap, not `[AMBIGUITY]`. [criterion 9] | open |
| F-3 | MINOR | MAINT | base | `prompts/04-implement.md`, lines 28–30 and 40–43 | The answers given at the appetite stop have no home in a file. *continue* names a new appetite and *cut* narrows the done-criterion, but the prompt writes neither into `plan.md`; only the spans go there, for the reason it gives itself ("a chat does not survive `/clear`"). Case: a session is answered *continue* with a new appetite of three hours, later parks, and the next session reads the card's old two hours against more than two hours used — it stops at once; after a *cut*, the next session reads the uncut `Done when:` and builds the cut part again. The prompt also does not say whether the new appetite is a total or an increment; since time used is a total (criterion 9), a maintainer's "one more hour" has to be turned into one. [criteria 12, 15] | open |
| F-4 | MINOR | SPEC | base | `prompts/03-plan.md`, lines 23–26 | The card's veto can be offered to nobody. The prompt says "show the card in the closing message" and "phase 4 starts once the card is shown", without saying to whom. When phase 3 runs as a subagent, its closing message reaches the orchestrating session, and nothing asks that session to put the card before the maintainer, so phase 4 starts on a silence the maintainer never had the chance to break. Case, this change: the plan was committed at 23:16:54 and phase 4 started at 23:18 with the maintainer away. The criterion says the card is shown "to the maintainer"; the provisional answer Q3 accepted a veto by default, which the maintainer confirms at the merge. [criteria 5, 6] | open |
| F-5 | MINOR | MAINT | base | `prompts/07-commit.md`, lines 19–21 against lines 32–54 | The one added sentence says every pull request body keeps "what could break" and the `done:` line, "the multi-decision form included". The multi-decision form printed a few lines below shows `**Your move:**` followed directly by `## 1 ·`, and the sentence after it lists what "then appear[s] once, as in the template" without either new line. An agent copying that form writes a body without both lines, or has to guess where they go (the templates put them below `**Your move:**`). Not `[DIVERGENT]`: the form omits, it does not contradict; and the spec ruled out a second copy of the lines, so the gap is the spec's by design. [criterion 23] | open |
| F-6 | MINOR | MAINT | base | `plans/changes/adhd-frame/spec.md`, `plan.md`, `research.md`, `decisions.md`, line 4 each; `plans/INDEX.md` | All four artefacts still say `implementation_status: none`, and the regenerated index lists the change as unbuilt, while the branch carries the built change and its last phase-4 commit declares the bead closed (`Closes-Bead: coding-harness-q24`). `plans/_README.md` says the field moves when the code moves; the previous change moved to `partial` after its phase 4 (`1964244`). This file states `partial`. [no criterion; the plans convention] | open |
| F-7 | MINOR | SPEC | base | criteria 34, 35, 36 (the pull request body), 41 (hosted run) | Held by phase 7, which has not happened: there is no pull request whose body could list the four provisional answers and the class, name the reinstall with `--check` first and the trust-list consequence, and name bead coding-harness-q24 as closed and coding-harness-9ca as changed and open; hosted CI has not run on the head. Closes itself when the body carries all of it and CI is green on its last commit. | open — closes in phase 7 |
| 2a-1 | — | SPEC | base | `spec.md`, the places weighed | *Where does the spec admit two plausible readings?* Three candidates, each read one way by the spec's own words. (a) Whether a new appetite after *continue* is a total or an increment: criterion 15 compares it with time used, which criterion 9 defines as a total, so it is a total (the unsaid conversion is in F-3). (b) Whether "check-in" in criterion 15 forbids the agent's own look at the clock: the criterion's refutation names "interim check-ins, reminders or a countdown" as prompt text asking for them, i.e. messages to the maintainer, so it does not (the missing read itself is F-1). (c) Whether the wait after a stop inside one session counts: the spec's `[DETAIL]` ("a night between two sessions is not work") favours not counting it (F-2). No `[AMBIGUITY]`. | answered |
| 2a-2 | — | SPEC | base | `spec.md`, criteria 9–15; `plan.md`, "Decided in phase 3" | *What is missing that would have to be decided while building?* Three holes the spec leaves: when the clock is read during work (F-1), where a span starts again after a stop inside one session (F-2), and where the answer at the stop is kept (F-3). The build filled none of them silently — the prompt is simply silent, as the spec is. One hole the plan filled in the open: where spans live (`plan.md`, `## Time used`, the plan's `[DETAIL]`). Everything else the build needed — placements, labels, the skill's text, the hook's wording — the spec names down to the source line. | answered |
| 2a-3 | — | SPEC | base | `spec.md`, criteria 8, 34–36, 40 and the prose criteria | *Which acceptance criterion cannot go red?* Criteria 34–36 cannot until the pull request exists (F-7). Criterion 8's pipeline only sees a number written in digits directly followed by an hour or minute unit: "two hours" or "a 90-minute appetite" pass it (checked here by reading instead — no figure, in digits or words, in the added lines). Criterion 40 is measured at a moving head and can turn red later without any change here (green at `ef7407c`). The prose criteria (1–7, 9–19, 23, 25–27) each name the text that would refute them and go red only by a reader's reading — by the spec's choice of no new test; each was read, and a deleted sentence would refute each. | answered |

Reviewer session: none — phase 2a skipped (plan.md).

## Checked without a finding

- **The plan card, criteria 1–8.** `prompts/03-plan.md` lines 10–34: the
  card opens every plan directly after header and title; the five labels
  stand in the criterion's order with their meanings; the pre-mortem is one
  line with one reason, "never a list of risks"; the last line is `Starts
  unless you say stop.`; a widening card names what widens and asks for the
  maintainer's "ok" in its place; "widens" is the spec's definition. No
  number, hour or minute in the 26 added lines (criterion 8's pipeline
  prints nothing, and reading finds no spelled-out figure). This change's
  own card follows the form: `text` block, five lines, veto line, an
  appetite that widens nothing because neither `decisions.md` nor `spec.md`
  sets one.
- **The appetite stop, criteria 9–19, apart from F-1 to F-3.**
  `prompts/04-implement.md` lines 23–62: `date`, never estimated or
  recalled; breaks inside counted and said to be, time between sessions not;
  the stop in the four labels in their order with the clock time in
  `found:`; exactly four answers and a recommendation; each answer's effect,
  *cut* building nothing new; *continue* reserved to the maintainer and
  cut, park or drop open to an orchestrating session — unambiguous; nothing
  built while the stop waits, park if the session must end; once per
  appetite; no card → no stop, `of no appetite set`, none set by the agent;
  the `done:` line with command, result and short commit; the `Resume:` line
  with one verb-first action naming its file, command or test, and as the
  handover's "Next step".
- **The pre-mortem's risk: 04 grown so long it is skimmed.** 04 went from 31
  to 72 lines (+41, within the plan's budget of 45; 03 +26 of 30). The new
  part is two bold-led paragraphs, one `text` block and four bullets; each
  rule is one sentence and the answers are a list. The densest spot is the
  first paragraph (lines 23–31), which carries definition, clock, record and
  trigger at once — the trigger being the part that is missing (F-1). Read
  as an agent would: usable, and the labels a later session greps for are
  all there.
- **The templates, criteria 20–22.** Both carry `**What could break:**`
  directly below `**Your move:**` and the `done:` line below it, before the
  first `##`, with `done:`, ` · ` and ` of ` intact;
  `tests/test_pr_templates.py`: 6 passed, no diff under `tests/`. The
  ordinary template's line 3 is unchanged. `markdownlint` (report-only) now
  also lists the `done:` line's placeholders as inline HTML (MD033), the same
  class it already reported for the other `<…>` placeholders in both
  templates.
- **07, criterion 23.** Exactly one sentence added at the end of "The pull
  request text explains itself", no list, no fence, pointing to both
  templates (the gap it cannot close is F-5).
- **The skill, criteria 24–28.** `git diff -M --name-status` shows `R072`
  from `skills/uebergabe/SKILL.md` to `skills/handover/SKILL.md`; the old
  directory is gone. Against the installed copy
  (`~/.claude/skills/handover/SKILL.md`, read only, SHA-256 `24c1e0a3…`):
  `diff` shows exactly three differences — "Variante A (Variant A)", the
  kept `updated: <JJJJ-MM-TT>` line, and the worktree places for
  coding-harness, lakeswitch and a repository naming none. Name,
  description with the pull request, §4's rule (always a pull request
  without asking, own worktree and branch from `main`, commit, push and PR
  belong to the handover, only the maintainer merges, English message and
  PR text, the exception without a remote or with another session in the
  checkout), §5 steps 3–4 with both links and the merge left to the
  maintainer: all there, "Nicht committen" gone. "Variante A" matches
  `templates/handover.md` on `main`, "Variant A" matches it on
  `origin/docs/translate-templates` (`b8667ed`); a trial merge with that
  branch exits 0.
- **Install, README, hook, AGENTS.md, criteria 29–32.** One changed line each
  in `install.sh`, `README.md` and `AGENTS.md`, four in the hook (header
  comment, two display strings, the session-end string, which equals line
  293 of the installed hook byte for byte). `bash -n` passes on both
  scripts; `tests/test_handover_entry.py`: 6 passed. No `/uebergabe` or
  `skills/uebergabe` left outside the change's own artefacts and the
  archive. `install.sh` was read in full: the file list is the only change,
  the copy loop creates `skills/handover/` with `mkdir -p`, and `--check`
  only reads. `install.sh --check` was run (it writes nothing): it now
  reports `differs ~/.claude/skills/handover/SKILL.md` where it reported
  the skill missing before, plus four other files that differ. An install
  does not remove an old `~/.claude/skills/uebergabe/`; on this machine none
  exists, so nothing is left behind.
- **No install run, criterion 33.** `~/.claude/skills/handover/SKILL.md` and
  `~/.claude/hooks/handover.sh` still hash to `24c1e0a34cda875a…` and
  `cc52269aaf14e17a…`; the only `*.bak-2026*` under `~/.claude` is a shell
  snapshot from 2026-09-06.
- **Boundaries, criteria 37–39.** `git diff --name-only` names only the
  allowed paths; 03 and 04 only gain lines, in one hunk each, above
  `Required:` and between "it is the plan." and "An ambiguous contract";
  none of the stage-2 marking words.
- **Trial merge, criterion 40.** `git merge-tree --write-tree HEAD
  origin/feat/stage-2-codex-glm` at `ef7407c`: exit 0. On the merged tree,
  extracted to a scratch directory, `tests/test_stage2.py`,
  `tests/test_pr_templates.py` and `tests/test_handover_entry.py`: 133
  passed. Also exit 0 against `origin/main`.
- **Suite, criterion 41.** `make verify` on `306b5ac` (with
  `commit.gpgsign` off): VERIFY GREEN, pytest 515 passed, 15 skipped;
  `docs-links` and `markdownlint` red but report-only, neither with a line
  this change added apart from the MD033 note above.
- **Time used and the clock.** `plan.md` records `23:18–23:22, 4 min`. The
  four building commits fall inside that span (23:19:29, 23:19:49, two at
  23:20:32 — one command, after the edits of steps 4 and 5), the plan's
  commit before it (23:16:54), and the commit that records the time after
  it (23:23:19), as the prompt's order has it: the end is read at the
  "done:" line and then written down. A `make verify` of about 45 s fits
  between 23:20:32 and 23:22. Plausible; the session itself was not read.
  The first measurement is also information: the plan's step estimates add
  up to 90 minutes, its appetite is 2 hours, and the agent needed 4
  minutes, so an appetite sized in human effort binds an agent-run phase 4
  only at many times its real length.
- **`Closes-Bead:`.** On `306b5ac`, the branch's last phase-4 commit, in one
  trailer block with `Co-Authored-By:` and `Claude-Session:`;
  `git interpret-trailers --parse` and `%(trailers:key=Closes-Bead)` both
  read `coding-harness-q24`. With the merge form of `prompts/07-commit.md`
  (`gh pr merge --merge`) the commit reaches `main` unchanged. This
  repository has no `close-merged` target yet, so the trailer is a
  declaration nothing here carries out — not this change's doing.
- **Language.** Every added line outside the skill and the hook is English;
  the German there is display text by house rule 1, and German elsewhere is
  quotation. Commit messages are English.
- **Non-goals.** No other phase prompt, no `docs/WORKFLOW.md`, no script,
  gate or test, no reinstall, no status-line clock, no figure, no
  translation of the skill or of `templates/handover.md`, no other
  `AGENTS.md` line.

## Not checked

The phase-3 and phase-4 sessions themselves: whether the card was shown in
a closing message and whether `date` was read are known only from `plan.md`
and the commit times. The pull request body and hosted CI (F-7). The full
suite on the trial-merged tree (only the three test files above ran there,
outside a git checkout). How Claude Code picks up a renamed skill after the
reinstall.

## For phase 7

`plans/INDEX.md` was regenerated with `python3 scripts/plans_registry.py
--index` for this file. F-1 wants one clause in 04 — when the clock is read
during work — in a repair round, or the maintainer's acceptance of the gap
at the merge; F-2 and F-3 sit in the same paragraph and can go with it.
F-4 belongs next to Q3 in the body's list of provisional answers. F-5 and
F-6 are small. F-7 closes itself in phase 7.
