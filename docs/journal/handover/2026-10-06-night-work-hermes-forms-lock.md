---
title: "Session handover — night of 2026-10-05/06: seven pull requests to merge, Hermes groundwork, three answers owed, 2026-10-06"
category: handover
created: 2026-10-06
updated: 2026-10-06
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-06"
tags: [handover, hermes, template-bundle, project-lock, rb-m6, research]
target_ref: "d5813ec"
bead: coding-harness-i3y
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

On 2026-10-05 and in the night to 2026-10-06 the session worked down the
plan with the maintainer's answers. Merged to `main` (at `d5813ec`): the
translations and the ADHD frame (#63–#68), the LikeC4/ROADMAP/arc42 research
(#69), ADR 0009 (Mermaid architecture delta, #70), the trial ROADMAP (#71),
the Hermes assessment (#72) and the research-currency age list (#73). The
maintainer also created a branch ruleset on `main` (pull request required,
required check `verify`, no force push, no deletion, no bypass). Seven pull
requests are green and wait for the maintainer's merge (#74–#80); three more
changes are built and reviewed but wait for answers.

## Next step

Ask the maintainer the first open question below (the template bundle's two
minor findings are already accepted by merging #75), then merge the green
pull requests the maintainer names, one at a time, restating each decision
block first (`prompts/07-commit.md`, "The merge").

## Needed from the maintainer

One at a time, each with a recommendation:

1. **Merge the seven green pull requests** (all `verify` green at their heads
   on 2026-10-06): #74 roadmap (Hermes takes the third Now place), #75
   template bundle (decision; merging accepts findings 6-17, 6-18), #76
   Hermes slice 1 (job prompt; merging accepts F-12), #77 ADR 0010
   (decision: Hermes as the first unattended writing agent), #78, #79, #80
   (research notes). Recommended order: #74, #75, #76, #77, then #78–#80
   (the notes conflict only in `docs/research/_INDEX.md`; an agent resolves).
2. **Should LakeSwitch move to Python 3.12?** Recommendation: yes — measured
   on 2026-10-05 in a scratch copy at lakeswitch-ai `09c9d62`: 1,334 tests
   pass on 3.11 and on 3.12, `lakeswitch verify` byte-identical; no reason for
   3.11 is written down. It is the LakeSwitch session's change (a signed pin
   in its `decisions/gates.yaml`); Coding Harness keeps both versions until
   then. If yes: hand the LakeSwitch session a paste text.
3. **ADR answer for project-lock** (bead coding-harness-ei0, branch
   `feat/project-lock` at `abac041`): proposed "no" (the architecture was
   decided in LakeSwitch D-45 to D-47). Record only as stated, with
   `python3 scripts/harness.py decide adr --change project-lock …`.
4. **ADR answer for rb-m6-one-account** (bead coding-harness-bma, branch
   `decide/rb-m6-one-account` at `b9ee999`): proposed "no" (it applies ADR
   0008; precedent #55). Plus **its finding F-2**: the rule set's §3 says
   level 4 blocks the merge in CI, but RB-M6 is now measured only on the
   maintainer's machine — amend §3, choose another level, or reject with a
   reason. Must land before 2026-10-31.
5. **Hermes F-14 (keys readable by the agent):** fixed only in part
   (`security.redact_secrets`, `.env` in `$HERMES_HOME`, a spike check CH-4).
   An OS-level barrier needs a design change: the orchestrator passes the
   keys on the wrapper's stdin from a file in the maintainer's home (touches
   design Interfaces 2 and 5, criteria 50 and 54, slice 4). Recommendation:
   yes, build it into slice 4.

Later, not urgent: which of the five i-have-adhd rules, the three
mattpocock adoptions and the ponytail prompt text to adopt (#78–#80); the
minor findings left as "the maintainer's choice" in project-lock (F-1–F-6),
rb-m6 (F-3–F-7) and Hermes slices 2/5 (F-16–F-24).

## Decisions and preferences

- Recorded in the change folders this session: template bundle answers 1–12
  (`plans/changes/template-bundle/decisions.md`; ADR answer "no" in
  `decisions/answers/template-bundle/adr.yaml`); research-currency class
  `bounded`; hermes-runner Q1–Q6 (`plans/changes/hermes-runner/decisions.md`;
  Q5 — the scheduled job may run before PR #60 without a leak check — was
  chosen against the recommendation); RB-M6 asks for what one account can
  hold (`plans/changes/rb-m6-one-account/decisions.md`).
- **Hermes is pushed on purpose** (maintainer, 2026-10-05), against the
  assessment's "not now" (#72): one host and pinned install shared with
  adhd-relief; two service users; GLM-5.3 through OpenCode Go.
- **Work sequentially** (maintainer, 2026-10-06): one change at a time, few
  agents, a visible queue ("step n of m").
- **Review findings as text:** when Claude Code refuses a review subagent's
  `findings.md` write, the orchestrating session commits the returned text
  unchanged and says so in the commit (maintainer's standing permission,
  2026-10-05). A standing rule — proposed for `AGENTS.md`, not yet written.
- Reviews stay on Opus 5.5 and implementation on Sonnet 5.5 until stage 2
  (#60) is live; #60 waits for the laptop (`/permissions` for `codex exec`,
  finding F-12 of that change).
- Plugins (i-have-adhd, ponytail, mattpocock/skills): the three notes
  recommend not installing them; agents never install into `~/.claude`.

## Open work and blockers

Task status is in Beads; the pieces in flight (2026-10-06):

- Hermes as the runner (coding-harness-i3y): slice 1 is #76; slices 2 and 5
  (endpoint entry, `tools/hermes/` profile) are on `feat/hermes-runner-2` at
  `7bd5787`, reviewed, repair round 1 for F-13/F-14 done but **not yet
  re-reviewed**; slice 4 (the publish script) needs phase 2a first (rows F-5,
  F-8, F-9, F-15, F-21, F-22); slice 7 is the maintainer's laptop afternoon
  (about 2.5–3 h: adhd-relief's spike, install, token, CH-1 to CH-8).
- project-lock (coding-harness-ei0): reviewed, no blocker; waits for the ADR
  answer; six minor rows open.
- rb-m6-one-account (coding-harness-bma): reviewed; F-1 repaired (not
  re-reviewed); F-2 and the ADR answer wait; due before 2026-10-31.
- RB-G7 `merge-freshness` valve also falls due on 2026-10-31
  (coding-harness-34z) — untouched.
- A test-holding gap: deleting 29 of 30 tests left `make verify` green
  (coding-harness-909).
- LakeSwitch's D-58 may take the ~30-elements LikeC4 trigger: a paste text
  went to the maintainer on 2026-10-05; the LakeSwitch session owns it.

## Working state and parallel-session boundary

- `main` at `d5813ec`; this handover is on `docs/handover-2026-10-06`.
- Open pull requests (heads 2026-10-06): #60 `ef7407c` (stays open, laptop),
  #74 `b76cce8`, #75 `9c930e0`, #76 `7beed6b`, #77 `03cd67f`, #78 `70ff946`,
  #79 `744c9a5`, #80 `db03547`.
- Branches without a pull request: `feat/hermes-runner-2` `7bd5787`,
  `feat/project-lock` `abac041`, `decide/rb-m6-one-account` `b9ee999`.
- Worktrees under `.claude/worktrees/`: adr-0010, hermes-runner,
  hermes-runner-2, project-lock, rb-m6, research-adhd, research-mattpocock,
  research-ponytail, roadmap-hermes, stage-2-codex-glm, template-bundle,
  handover-2026-10-06. Remove each after its merge.
- Another session runs in lakeswitch-ai (not in this checkout); it owns
  LakeSwitch. This session was the tracker writer for coding-harness.
- Tracker pushed after every write (`tools/bd dolt push`).

## Validation

- Every branch above ended `make verify` green with commit signing off
  (`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign
  GIT_CONFIG_VALUE_0=false`), except project-lock and rb-m6, which are red on
  `adr-answers` alone by design until the ADR answers exist.
- Hosted `verify` green on #74–#80 at the heads listed (read 2026-10-06).
- GitHub Actions had a degraded period and a major outage on 2026-10-05;
  runs without a runner were cancelled and re-run.
- Not run: any Hermes, Codex or GLM call; any install; the re-reviews of
  rb-m6 F-1 and Hermes F-13/F-14.
