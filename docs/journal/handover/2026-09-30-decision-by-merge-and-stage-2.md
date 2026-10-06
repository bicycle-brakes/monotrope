---
title: "Session handover — decisions by merge merged, stage 2 slice 1 done, Codex as worker pending, 2026-09-30"
category: handover
created: 2026-09-30
updated: 2026-09-30
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-30"
tags: [handover, harness-decide-adr, decision-pr, stage-2, codex, glm]
target_ref: "27dedc9"
bead: coding-harness-bc9
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

The ADR answer now lives in Coding Harness, without signing: a decision takes
effect when the maintainer merges its pull request (PRs #54 to #57, merged
2026-09-30). Stage 2, where Codex and GLM review changes before the merge, is
planned and its slice 1 is built (branch `feat/stage-2-codex-glm` at
`2e8ca15`). The maintainer's Claude budget is nearly used up, and they asked
to hand new tasks to Codex; that hand-over is not done yet (see "Needed from
the maintainer").

## Where we are

As of 2026-09-30, `origin/main` at `27dedc9`:

- **Merged:** #54 (the ADR answer in Coding Harness: the gate
  `adr-answers`, the command `scripts/harness.py decide adr`, merge ask
  rules, decision-PR templates, house rule 8), #55 (rule RB-M2 gets the
  one-account exception, rule set 3.0.0), #56 (ADR 0008: a decision takes
  effect by the maintainer's merge, no commit signing), #57 (two finished
  change folders archived).
- **Open:** #58, spec review and review on Opus 5.5 until stage 2 is live.
  Ordinary PR, `make verify` green; CI state not read at hand-over.
- **Stage 2 (bead coding-harness-bc9):** research, interview (answers 1 to
  12), spec (72 criteria, revised by a spec review), plan (three slices,
  about 10 h) are committed. Slice 1 is built: the endpoint declaration
  (`openai-codex`, Kimi excluded, Sonnet 5.5, the ChatGPT personal-use
  declaration with "Improve the model for everyone" off), a model-id
  resolver that accepts dots, and the leak check `scripts/leakcheck.py`.
  Slices 2 (the runner `scripts/stage2.py`, the review loop) and 3 (doctrine,
  prompts, ADR 0007, the D-13 chain) are open.

## Next step

Ask the maintainer the one open question below. On option 1, start slice 2
of `plans/changes/stage-2-codex-glm/plan.md` with Codex as the worker, the
leak check (`make leakcheck` / `scripts/leakcheck.py`) run first, in the
worktree `.claude/worktrees/stage-2-codex-glm`.

## Needed from the maintainer

**Should Codex take over the remaining work now that the leak check exists?**
The maintainer said on 2026-09-30 "use Codex for all new tasks from now on,
my budget here is nearly used up". Claude Code's auto-mode classifier blocked
the session's instruction to a sub-agent to switch to Codex before merge; the
session did not work around it and offered three options:

1. Wait until slice 1 (the leak check) is done, then hand slices 2 and 3 to
   Codex with the leak check before every call — **recommended**; slice 1 is
   now done, so this can start.
2. The maintainer starts Codex themselves in the stage-2 worktree.
3. The maintainer allows it explicitly in Claude Code's permissions.

**Answered while this hand-over was written:** the maintainer allowed it
explicitly in chat ("Ich erlaube es dir ausdrücklich", 2026-09-30), i.e.
option 3; the leak check exists by now, so it runs before every Codex call.
The session then started handing slice 2 to Codex; check the branch and
`decisions.md` answer 13 for how far it got. Consequence: the first real Codex call runs
before ADR 0007 is merged, which the spec's criterion "no foreign call before
the merge" forbids; that criterion then needs answer 13 in `decisions.md`
("changed by answer 13"). This record was not written, because the
classifier blocked the same instruction.

## Decisions and preferences

All 2026-09-30, from the maintainer, not to be asked again:

- **No commit signing in Coding Harness**, now or later. The maintainer's
  merge confirms a decision; agents merge only on the maintainer's explicit
  request after restating what the PR decides; `.claude/settings.json` asks
  before every recognised merge command (a brake, not a lock). ADR 0008,
  house rule 8, RB-M2 3.0.0.
- **Decision PRs** carry the label `decision` (created on GitHub), the title
  `decide(<scope>): …` and the block from
  `.github/PULL_REQUEST_TEMPLATE/decision.md`; other PRs use
  `.github/pull_request_template.md`. English, written for a reader with
  ADHD on a phone.
- **Only changes of class `feature` owe an ADR answer.** The three answers
  so far: harness-decide-adr yes (ADR 0008 is that ADR), frontmatter-current
  no, omnigent-deny-layers no.
- **Coding-Harness-specific work runs in the Coding Harness session**,
  LakeSwitch-specific work in the lakeswitch-ai session.
- **Stage 2** (`plans/changes/stage-2-codex-glm/decisions.md`, answers 1 to
  12): D-13 is amended by ADR 0007 (leak check and declared endpoint stay
  hard; the first three stage-2 runs are measured instead of three runs
  before); all five packages in one change; stage 2 by change class as a
  doctrine table; ChatGPT personal-use declared; the evidence rule for review
  findings; one condition per acceptance criterion; appetite 9 to 11 h, the
  data-protection proofs dropped because Coding Harness content is not
  sensitive; the customer checkout on the same disk is an accepted residual
  risk (the reviewers are asked not to read outside the worktree — a request,
  not a lock).
- **Model routing:** implement on Sonnet 5.5 for every change; spec review
  and review on Opus 5.5 until stage 2 is live (#58); other agents on Opus.
- Commits of this session are unsigned: the SSH signing key was locked while
  the maintainer travels. Coding Harness requires no signature.

## Open work and blockers

Task status is in Beads; read with `tools/bd show <id>`:

- Stage 2: Codex and GLM review Coding Harness changes before the merge
  (coding-harness-bc9), in progress, claimed by this session. Slices 2 and 3
  open.
- The ADR-answer principle in Coding Harness (coding-harness-3ar), in
  progress; stays open until LakeSwitch has switched. Its change folder
  `plans/changes/harness-decide-adr/` stays unarchived until then.
- Stage-2 entry measurement (coding-harness-kw0): to be re-scoped or closed
  as superseded once ADR 0007 is merged (comment on the bead, 2026-09-30).
- Key-list weakness of signed decisions (coding-harness-in1): now concerns
  only lakeswitch-ai gate M-30 (comment, 2026-09-30).
- Not in the tracker: a bead for the first LakeSwitch run on Northwind (owed
  since the previous hand-over; left to the lakeswitch-ai session).

## Working state and parallel-session boundary

- `main` checkout at `27dedc9`, clean.
- Worktrees: `.claude/worktrees/stage-2-codex-glm` (branch
  `feat/stage-2-codex-glm`, `2e8ca15`, pushed, no PR yet);
  `.claude/worktrees/reviews-on-opus` (branch `docs/reviews-on-opus`,
  PR #58; remove after merge); `.claude/worktrees/handover-2026-09-30b` (this
  hand-over; remove after merge).
- Other sessions (read 2026-09-30): `lakeswitch-ai-bd` in lakeswitch-ai
  (writes nothing in Coding Harness or its tracker); `mikypiky-44` in the
  home directory. No other session in this repository, so this session was
  the tracker writer.
- The handed-over stage-2 proposal existed only in a session scratchpad; its
  content is in `plans/changes/stage-2-codex-glm/research.md` and
  `decisions.md`.

## Validation

- `make verify` (with commit signing switched off by environment, because
  test fixtures commit with the global signing setting): green on every
  branch this session pushed — last on `feat/stage-2-codex-glm` at slice 1
  (533 passed, 15 skipped, 2026-09-30). markdownlint and docs-links report
  red, as on `main` before.
- The real leak check against the real denylist at `2e8ca15`: clean, 186
  files, 254 commits, 12 rules (2026-09-30).
- CI green on #54 before its merge; not read for #58 at hand-over.
- Not run: any Codex or GLM call; the GitHub-app rendering of decision PRs
  was not checked by an agent.

## Addendum — 2026-09-30, stage 2 built with Claude, PR #60 stays open

This supersedes the "Next step" and the Codex addendum above.

- The maintainer's Claude budget came back the same evening. They decided
  to finish stage 2 with Claude agents only, open its decision PR and leave
  it unmerged (answer 14 in `plans/changes/stage-2-codex-glm/decisions.md`;
  answer 13, Codex as the worker, is void — no Codex or GLM call was made).
- Slices 2 and 3 were built on Sonnet, reviewed on Opus 5.5 (1 blocker, 1
  major, 7 minor), repaired in one round, and re-reviewed: all nine fixed,
  two new minor findings open (F-10: lines starting with `#` in GLM's answer
  are dropped at release; F-11: a short table line with a loop id written by
  GLM blocks the release). `make verify` green at `22ba651`: 654 passed, 15
  skipped (2026-09-30).
- **Decision PR #60** (branch `feat/stage-2-codex-glm`, head `8622437`) is
  open and stays open until the maintainer decides otherwise. Until it
  merges, `main` keeps spec review and review on Opus 5.5 and implement on
  Sonnet.

**Next step:** nothing on stage 2 until the maintainer says so. Before a
merge of #60: fix F-10 and F-11 (a second repair round; a finding from it
escalates per `docs/WORKFLOW.md` §2), then the maintainer adds
`Bash(codex exec:*)` with `/permissions` at the laptop. Otherwise take the
next ready bead with `tools/bd ready`.

**Needed from the maintainer:** nothing right now.

Working state: worktree `.claude/worktrees/stage-2-codex-glm` stays for #60;
bead coding-harness-bc9 in progress with a comment naming #60 (tracker
pushed 2026-09-30).
