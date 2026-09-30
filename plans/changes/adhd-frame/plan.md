---
title: "Plan — adhd-frame"
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
tags: [plan, adhd, prompts, pull-request-templates, handover]
---

# Plan — adhd-frame

```text
For you:     a card per plan, an appetite stop, a timed "done:", "what could break" in PRs, /handover PRs
Done when:   checks 1–41 below hold, `make verify` green, a clean trial merge with the stage-2 PR (#60)
Appetite:    2 h of phase 4, repair rounds included
Not now:     other phase prompts, docs/WORKFLOW.md, checks or tests, the reinstall (yours), a status clock
Pre-mortem:  suppose it failed: most likely because 04's new text grows so long that sessions skim it
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–41), provisional like it. Stage 1: no model
markings. Facts read on 2026-09-30 at `ac30a69`, pull request 60 at `ef7407c`.
**Phase 2a was skipped** by the orchestrating session: prose-only change with
41 refutable criteria, the maintainer is away until 2026-10-04, and the phase 6
review on Opus reads the spec against the result. Phase 6 writes "Reviewer
session: none — phase 2a skipped (plan.md)" under its table in `findings.md`
and asks the three 2a questions of `spec.md` as rows of dimension `SPEC`.

## Decided in phase 3

No `[DECISION]` is open.

- `[GAP]`, closed — pull request 60 at `ef7407c` keeps the 03 and 04 hunks of
  `research.md` §3 and adds `plans/INDEX.md` rows at the end (ours: the top);
  nothing in `scripts/`, `tests/` or `decisions/` names the skill path; 03's
  gate script does not exist, so `make verify` stands in.
- `[DETAIL]` — **appetite 2 h.** `research.md` §7 puts the phase-4 parts at
  1.25 h (`make verify` ran 44 s here); the rest is room for one repair round.
  Tighter, a normal overrun would park the change until the maintainer, the
  only one who may answer continue, returns.
- `[DETAIL]` — **the card is a `text` block** aligned like the four-line stop:
  its lines survive any renderer and copy unchanged into the closing message.
- `[DETAIL]` — **spans live in `plan.md`:** each phase-4 session appends
  `<date> <start>–<end>, <span>[, break counted]` under `## Time used` when it
  ends; `plan.md` is phase 4's input, and a chat does not survive `/clear`.
- `[DETAIL]` — **line budget:** at most 30 added lines in 03 and 45 in 04, the
  guard against the pre-mortem.
- `[DETAIL]` — **the skill cites "Variante A (Variant A)"**: the translation of
  `templates/handover.md` (branch `docs/translate-templates`) renames that
  heading, and either pull request may merge first.
- `[DETAIL]` — **this change's phase 4 already runs by step 2's text:** `date`
  at the start, the stop at 2 h, the "done:" line.

## Steps

1. `prompts/03-plan.md` (15 min) — insert, between the paragraph "You describe
   **how**…" and `Required:`, a short paragraph and the card as a `text` block
   with placeholders (labels of criterion 2, the pre-mortem form of 3, the
   last line of 4), then what widens (spec, "Terms") and the rules of 5–7.
   No figure (8), none of the words of 39.
2. `prompts/04-implement.md` (25 min) — insert after the paragraph ending "it
   is the plan." two bold-led paragraphs. The first holds criteria 9–15 and
   17: time used and where spans live, the stop as a `text` block in the four
   labels, the four answers as a list, who answers, no building while it
   waits, once per appetite, no card → `of no appetite set`. The second holds
   16, 18 and 19. Commit.
3. Both templates (10 min) — after the `**Your move:**` line, each its own
   paragraph like the lines above it: `**What could break:** <what could fail
   after the merge, and where it would show>`, then `done: <verification
   command>: <result> at <short sha> · <time used> of <appetite>`.
   `prompts/07-commit.md` — one sentence at the end of the bullet "The pull
   request text explains itself", as criterion 23 words it. Commit.
4. The skill (15 min) — `git mv tools/claude-code/skills/uebergabe
   tools/claude-code/skills/handover`. In `SKILL.md`: lines 2–3 become lines
   2–3 of `~/.claude/skills/handover/SKILL.md` (criterion 33's hash); line 74
   says "Variante A (Variant A)"; line 110 becomes that copy's lines 109–120,
   its parenthesis reading: coding-harness: `.claude/worktrees/<name>`,
   Branch `docs/handover-<datum>-<thema>`; lakeswitch: `~/lakeswitch-wt/<name>`,
   Branch `docs/journal-<datum>-<thema>`; in einem Repository, das keinen Ort
   nennt: `.claude/worktrees/<name>`. Step 3 of §5 becomes that copy's steps
   3–4. The `updated:` line stays.
5. The rest of the rename (10 min) — `install.sh` line 27 says
   `skills/handover/SKILL.md`, `AGENTS.md` line 168 `/handover`; the README
   row reads ``| `skills/handover/SKILL.md` | `/handover` | writes the handover
   as a file in the repository, by that repository's convention, and always
   opens a pull request for it |``; the hook's lines 17, 238 and 242 say
   `/handover`, and line 327 becomes line 293 of `~/.claude/hooks/handover.sh`.
   Commit.
6. Checks (15 min) — the block below, the `## Time used` line (with
   `python3 scripts/check_frontmatter_current.py --stamp` on a new day),
   `python3 scripts/plans_registry.py --index`, the verification, push. The
   closing message ends with the "done:" line.

Verification, verbatim (the prefix only where commit signing is unavailable):
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify`,
ending `VERIFY GREEN` (criterion 41).

## Checks per criterion

No test is added or edited (spec, `[DETAIL]`). Each check goes red on its
criterion's "Refuted by"; the comment says what green prints, "read" means
the text is held against it. 8 and 39: the spec's two pipelines print nothing.

```bash
grep -oE 'For you:|Done when:|Appetite:|Not now:|Pre-mortem:' prompts/03-plan.md | head -5 | paste -sd' ' -  # 1–7, read: the five labels in order
for s in '`date`' 'done: <evidence> · <time used> of <appetite>' 'Resume: when I start, I will <one action>' 'of no appetite set'; do grep -qF -- "$s" prompts/04-implement.md || echo "missing: $s"; done  # 9–19, read: nothing
git diff -U0 origin/main -- prompts/03-plan.md prompts/04-implement.md | grep -E '^(@@|-)' | grep -v '^--- '  # 38: two @@ lines at old 8–9,0 and 21–22,0; no "-" line
git diff --numstat origin/main -- prompts/03-plan.md prompts/04-implement.md  # budget: ≤ 30 and ≤ 45 added, 0 removed
for f in .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE/decision.md; do sed -n '1,/^## /p' "$f"; done  # 20–21: Your move, What could break, done:, then ##
python3 -m pytest tests/test_pr_templates.py -q && git diff --quiet origin/main -- tests/  # 22: passed, exit 0
git diff origin/main -- prompts/07-commit.md  # 23: one sentence added; since repair round 1 also the two lines in the multi-decision form; no other list item or fence
git diff -M --name-status origin/main...HEAD | grep '^R'; test ! -e tools/claude-code/skills/uebergabe  # 24: an R line, exit 0
grep -c 'Nicht committen, es sei denn' tools/claude-code/skills/handover/SKILL.md  # 25–27, read frontmatter, §4, §5: 0
grep -c '^updated: <JJJJ-MM-TT>$' tools/claude-code/skills/handover/SKILL.md  # 28: 1
git diff --numstat origin/main -- tools/claude-code/install.sh tools/claude-code/README.md tools/claude-code/hooks/handover.sh AGENTS.md  # 29–32: 1 1, 1 1, 4 4, 1 1
bash -n tools/claude-code/install.sh && bash -n tools/claude-code/hooks/handover.sh && python3 -m pytest tests/test_handover_entry.py -q  # 29, 31: passed
grep -rn uebergabe tools/claude-code AGENTS.md  # 29–32: nothing
shasum -a 256 ~/.claude/skills/handover/SKILL.md ~/.claude/hooks/handover.sh; find ~/.claude -name '*.bak-2026????-??????'  # 33: 24c1e0a34cda875a…, cc52269aaf14e17a…; no backup
git diff --name-only origin/main...HEAD  # 37: only criterion 37's paths
git fetch origin && git merge-tree --write-tree HEAD origin/feat/stage-2-codex-glm >/dev/null; echo $?  # 40: 0
```

## Not touched

03's section `## Model markings` and 04's `**Model:**` line and last
paragraph (pull request 60's hunks); 07's multi-decision block; the README's
"six files"; the skill's German and every line step 4 does not name;
`docs/WORKFLOW.md`, the other prompts, `templates/`, `scripts/`, `tests/`,
`decisions/`; `~/.claude` — no `install.sh` without `--check`. (Touched on purpose in
repair round 1: 07's multi-decision block, F-5, and `spec.md`, criteria 9, 10, 15
and 23.)

## Phase 7

The ordinary template. What could break: after the reinstall the start entry
shows a handover's metadata, not its content, until `~/.claude/handover-trust`
exists. The body lists the four answers and `class: bounded` for confirmation
(34) and the reinstall step (35); the frame's bead closes (coding-harness-q24,
`Closes-Bead:` on the last commit), the rename's stays open with the rest the
spec's non-goals name (coding-harness-9ca) (36).

## Repair round 1

Origin `fix-r1`, 2026-09-30, on the seven rows of the phase-6 review
(`findings.md`, reviewed at `306b5ac`; this round starts at `1fc0038`). F-1 to
F-6 are fixed, in `dcd072c` (F-1 to F-3, prompt 04), `1026094` (F-4 in 03, F-5 in
07) and `3de8b5c` (F-6); F-7 stays open until phase 7. The decisions are the
orchestrating session's `[DETAIL]`s, given to this round; the maintainer confirms
them with the rest at the merge. Two places of "Not touched" were touched on
purpose: the multi-decision block of 07 (F-5) and `spec.md`, in criteria 9, 10,
15 and 23, each amendment marked in place, nothing renumbered. The fixes are
prose, so no test was added (spec, `[DETAIL]`); each is checked by reading and
by the commands of "Checks per criterion".

- **F-1 (MAJOR), the clock now has a trigger.** 04 says to read `date` between
  steps and before each commit as well as when a session starts and ends, and to
  stop when such a reading shows the time used has reached the appetite. The
  sentence "no reminder, countdown or check-in before it" stays; it means no
  timer and no message to the maintainer, and 04 and criterion 15 now say the
  agent's own readings are none of them. Criteria 9 and 10 name the readings.
  This round followed the rule it adds: `date` was read at each step boundary.
- **F-2, a stop ends the span.** A new span starts when work resumes, in the
  same conversation too (04, criterion 9), so the night behind a stop is not
  work and the next reading does not fire a spurious stop.
- **F-3, the answer has a home.** The new appetite, the narrowed `Done when:`,
  or park or drop is written under `## Time used`, where it replaces the card's
  line; the card itself stays as it was shown. The finding's second half is
  answered with three words: a new appetite is a total, because time used is one.
- **F-4, who shows the card.** One sentence in 03: when phase 3 runs as a
  subagent, the orchestrating session shows the card to the maintainer
  unchanged, and the veto stays the maintainer's.
- **F-5, the form carries the lines.** The multi-decision form in 07 now prints
  "What could break" and the `done:` line below `**Your move:**`, as the two
  templates do; criterion 23 allows exactly that and still refutes a copy of the
  template's lines anywhere else.
- **F-6, `partial` everywhere.** `implementation_status` is `partial` in all five
  artefacts. `plans_registry.py` reports `done` on a change that is not archived
  as drift, and the stage-2 change and the decide-ADR change both stand on
  `partial` until their archive; `done` comes with the archive in phase 7.

**Measured on `3de8b5c` (2026-09-30).** Line budgets, added lines over
`origin/main` with none removed: 03 has 27 of 30, 04 has 44 of 45; the two `@@`
lines of check 38 are the same two. No number with an hour or minute unit in an
added line of 03 or 04 (criterion 8), no marking word in 03 (criterion 39).
`git merge-tree --write-tree HEAD origin/feat/stage-2-codex-glm` (at `ef7407c`)
exits 0, and so does the trial merge with `origin/main`. `make verify`: 515
passed, 15 skipped, last line `VERIFY GREEN — every local gate of the 'verify' job
passed.` (`docs-links` and `markdownlint` report and do not block).

## Time used

2026-09-30 23:18–23:22, 4 min
2026-09-30 23:38–23:46, 8 min (repair round 1)
