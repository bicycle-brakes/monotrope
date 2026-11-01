---
title: "Decisions — pi-neutral-paths"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-xul8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# pi-neutral-paths — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).
Exploration: `research.md` (GLM 5.3 Flash, 2026-10-29, and the addendum of
the same day).

## Q-1 · Which Pi launches the neutral-path fix covers

context: |
  Topic: the local absolute paths Pi puts into its own system prompt.
  Intention: Pi adds the working directory and its install's documentation
  paths, home directory and worktree name included, to every call it sends
  to an online model; the leak check never sees them (bead coding-harness-xul8).
  Today: no launch removes them; the research swarm, the review loop, the
  availability probes and the session all send them.
  Repository change: every Pi launch that calls a model gets the fix, or only
  the research swarm's.
  Architecture change: none beyond the launch commands.
asked: 2026-10-29, conversation 2026-10-29 (bead notes, parked after the exploration)
answer: "the neutral-path fix covers every Pi call (research swarm, review loop, Flash), not only the research swarm"
answered_by: maintainer
status: answered

The answer was given on 2026-10-29 and recorded in the bead's notes the same
day; this record copies it from there. "Flash" reads as the review loop's
Flash swarm, which runs through Pi; GLM 5.3 Flash's explore and implement run
through Claude Code and are not Pi calls (see the detail below).

In the context of Pi's own system prompt, facing local absolute paths that
reach online models unseen by the leak check, we decided that every Pi
launch that calls a model gets the neutral-path fix, to achieve that no
launch path keeps the leak, accepting that the review loop's and the probe's
launch commands change too.
— 2026-10-29

## Q-2 · How the paths are removed

context: |
  Topic: the mechanism that keeps the paths out of Pi's prompt.
  Intention: three ways were seen; they differ in what else moves.
  Today: the pinned Pi 1.2.0 offers no flag; its extension API can rewrite
  the prompt sections before every run (research.md, addendum 2026-10-29).
  Repository change: (a) one small extension, loaded with `-e` by every
  model-calling launch, sets the prompt's working directory to a neutral
  literal and suppresses the documentation section; (b) start Pi from a
  neutral directory and install it at a neutral path, which moves the
  repository seats' path lock and tool root; (c) ask Pi upstream for a flag
  and wait.
  Architecture change: (a) adds one extension file beside the path lock;
  (b) changes where Pi is installed and run.
asked: 2026-10-29, through the orchestrating session of the day run
answer: "option (a): a small Pi extension, loaded with -e at every Pi start with model contact, sets cwd to a neutral value and suppresses <docs> through before_agent_start"
answered_by: maintainer
status: answered

The maintainer answered on 2026-10-29 at about 12:10 UTC; the orchestrating
session of the day run relayed the answer, and this record copies it from
that relay. The recommendation put to the maintainer was (a): it uses Pi's
declared extension API, leaves the working directory and the path lock as
they are, and adds one file. Its risk: an extension that rewrites the prompt
is code inside the trust boundary, and a Pi upgrade can change the hook; a
capture check on the outgoing payload (criterion owed by the spec) catches
both.

In the context of Pi's own system prompt, facing a pinned Pi with no flag to
drop its `<cwd>` and `<docs>` sections, we decided that one small extension,
loaded with `-e` by every Pi start with model contact, sets the prompt's
working directory to a neutral value and suppresses the documentation
section through `before_agent_start`, to achieve that no local path leaves
the machine in Pi's prompt, accepting that the extension is code in the
trust boundary and must be re-checked on every Pi upgrade.
— 2026-10-29

## Decided by the agent

[DETAIL] **Launches without a model call stay out.** `pi update --models`,
`pi --list-models` and `pi --version` send no prompt to a model
(`scripts/stage2.py:2119, 2167, 2469`); nothing changes there.

[DETAIL] **Claude Code launches stay out.** GLM 5.3 Flash (explore,
implement) and the swarm's Opus roles run through Claude Code, whose own
context is not Pi's prompt; the bead and Q-1 name Pi. Whether Claude Code
sends the working directory to GLM's endpoint is a separate question for a
bead of its own.

[DETAIL] **The check holds the whole outgoing payload, not the system prompt
alone.** A capture through the `before_provider_request` hook (or an
equivalent stand-in in tests) asserts that no home directory, worktree name
or checkout path appears anywhere in what leaves the machine, so tool results
and future prompt sections are covered too (research.md, addendum: tool
results not read).

[DETAIL] **`scripts/stage2.py` changes, after lane A releases it.** The
review loop's launch (`stage2.py:2548-2567`) must load the extension. Lane A
of the 2026-10-29 day run owns that file today; the plan schedules the edit
after that lane's merge, and no other step depends on it first.
