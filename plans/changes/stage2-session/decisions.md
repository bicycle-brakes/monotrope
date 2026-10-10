---
title: "Decisions — stage2-session"
status: draft
implementation_status: partial
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, session]
---

# Decisions — stage2-session

## Settled maintainer instructions

Source: the takeover handover in PR #90 (`a3d5585`, 2026-10-07),
the notes of the shared bead, and the current takeover request. This record
does not turn the unmerged ADR amendment into accepted repository policy.

1. Extend the runner-only rule to interactive sessions. Keep declared
   endpoints and the clean leak check as prerequisites; no bypass verb.
2. Open a terminal in the change's own worktree with the chosen model and
   handover as its first prompt. Record date, model and leak-check counts
   in `findings.md`.
3. Deny outside-worktree reads in OpenCode as far as its configuration
   supports it; name the remaining limit. Check only the state at launch.
4. Use the existing endpoint declaration. OpenCode Go reviewer ordering
   is separate work, not another routing table in this verb.
5. Draft the ADR 0007 amendment in the change folder; do not edit
   `docs/adr/`. End in a decision PR and never merge.
6. Leave PR #89 and its branch untouched. Research/spec may proceed while
   it is open; implementation waits for its merge onto main.

## Reversible implementation details

- [DETAIL] Class `architectural`: interactive dispatch extends the trusted
  launch boundary and requires the ADR 0007 amendment already requested.
- [DETAIL] Default handover is `plans/changes/<change>/handover.md`; an
  explicit `--handover <path>` accepts an existing file inside the worktree,
  including `docs/journal/handover/`. Refuse a missing default rather than
  guessing relevance from a date or sending another change's handover.
- [DETAIL] Initial platform is macOS Terminal, matching this machine.
  Other platforms refuse before dispatch instead of silently running a
  background noninteractive job.
- [DETAIL] Pin the selected model and permission policy at launch, make no
  automatic fallback. A failed launch must not silently choose another
  endpoint.
- [DETAIL] The implementation appetite proposal is four hours including
  repairs. It is a stop boundary, not a promise of completion time.

None of these details authorizes a model call, merge or credential-file read
outside the takeover instructions.

## Spec-review decision — start-success boundary (answered)

Source: phase-2a finding F-2, 2026-10-07. Asked once through the user-input
question. The maintainer subsequently replied "mach weiter" directly after
the recommendation and confirmation question (2026-10-07). This is recorded
as assent to option 1, not a new decision made by the agent.

Goal in one sentence: make the returned launch status tell the maintainer
exactly what has been confirmed.

Options:
1. Terminal accepted the start request after the runner checked the CLI
   prerequisite. Later login/model/start errors appear in the new window.
   The runner returns promptly and does not supervise the interactive session.
2. Require a separate program-start acknowledgment before returning success.
   The runner must supervise that acknowledgment and fail on a bounded timeout;
   it still cannot prove login or a successful model answer.

Recommendation: option 1, because the maintainer asked for an independent
interactive window, and success can explicitly mean dispatch rather than a
completed model call.

If accepted: distinguish missing-program preflight refusal, failed Terminal
dispatch and accepted dispatch in help, audit and tests.

What is lost: immediate confirmation that the selected CLI actually started
after Terminal accepted the command.

Answer: "mach weiter" (maintainer, 2026-10-07), accepting the immediately
preceding recommendation: Terminal acceptance after CLI prerequisite checks.
The session is not supervised for program-start acknowledgment or model success.

## Further reversible details for the plan

- [DETAIL] A helper module holds interactive launch mechanics; the sole public
  model entry stays `scripts/stage2.py`, avoiding reviewer-migration overlap.
- [DETAIL] Runtime policy files live in a fresh private directory under
  `.stage2-sessions/` in the worktree. Failed preparation removes only that
  directory; accepted dispatch retains it for the new CLI to load. No keys.
- [DETAIL] OpenCode uses a dedicated primary agent and no external plugins.
  Effective permission diagnostics are checked before dispatch. Subagents are
  denied initially to avoid bypassing the checked primary agent.
- [DETAIL] Initial prompts are capped at 32 KiB UTF-8, complete shell dispatch
  commands at 64 KiB: refuse oversized arguments before GUI dispatch.

- [DETAIL] (2026-10-07, repair session) The `opencode-go` entry lists bare
  model ids, as the reviewer change (coding-harness-ymx, spec criterion 1 on
  `feat/stage2-mimo` at `8310a2c`) declares them for its Claude Code calls.
  `--model opencode-go/<model>` therefore resolves against the bare `<model>`
  and hands the full id to OpenCode's CLI; a plain id stays Codex's. Requiring
  the full id in `modelle` would have refused every OpenCode Go session once
  both changes merge. The maintainer was told and did not object.
- [DETAIL] (2026-10-07, repair session) The effective-policy check follows
  OpenCode 1.18.35 as read from its source (`agent/agent.ts`,
  `permission/index.ts`, `cli/cmd/debug/agent.handler.ts`): `model` is
  `{providerID, modelID}`, `permission` one ordered rule list, the last rule
  whose wildcard permission name and pattern match wins, and the truncation
  directory allowance is appended unless that exact pattern is denied. The
  check requires each guarded permission's last catch-all rule to be the
  runner's action and refuses every later rule except that one allowance.

## Implementation route after the unanswered attempt

Maintainer, 2026-10-07: "kannst du mit glm implementieren?" following the
offer of direct Codex implementation or another GLM attempt. Continue with
the existing GLM Flash runner route, not a direct Codex implementation.
This requests another attempt; it is not evidence that the endpoint works.
Keep declaration/leak checks, post-run gates, review phases and no-merge rule.

## Answers

The six questions are work package 1 of the plan to move the interactive
session verb from the OpenCode CLI to Pi
(`docs/research/2026-10-09-session-verb-on-pi-plan.md`, on branch
`chore/0al-prep`, pull request #109). Asked one at a time in German with a
recommended option; recorded here in a faithful English translation. In the
same conversation the maintainer approved that plan (answer to "Do your
answers also approve the plan?": "Yes, plan approved").

## Q-1 · How strong is the read-back of the session policy

asked: 2026-10-09, the directing conversation
answer: confirm load — the runner confirms that Pi loaded the policy
  extension; handler tests without Pi hold the extension's behaviour
answered_by: maintainer
status: answered

In the context of a Pi session whose policy lives in a runner-supplied
extension, facing the choice between confirming that the extension loaded and
additionally firing a live canary call the policy must block, we decided to
confirm the load and test the handlers without Pi, to achieve a start that
costs no model call, accepting that whether the policy acts inside a running
Pi is not checked live. — 2026-10-09

## Q-2 · Which bash calls ask

asked: 2026-10-09, the directing conversation
answer: only dangerous patterns, as in Pi's `permission-gate.ts` example
  (not every call, which was the recommendation)
answered_by: maintainer
status: answered

In the context of the session's shell tool, facing the choice between asking
before every call (today's `bash: ask`) and asking only on dangerous patterns,
we decided to ask only on dangerous patterns, to achieve fewer interruptions
during an interactive session, accepting that a command the pattern list does
not know runs without a question. — 2026-10-09

## Q-3 · What the file tools may do

asked: 2026-10-09, the directing conversation
answer: read and write inside the worktree, block outside, and block writes to
  the extension's own file, `.stage2-sessions/` and `.pi/`; `.git/` is not
  additionally blocked
answered_by: maintainer
status: answered

In the context of Pi's read, write and edit tools, facing the choice between
the worktree with a protected list and that list plus `.git/`, we decided the
worktree with the protected list, to achieve a session that cannot rewrite its
own policy, accepting that `.git/` stays writable for the model. — 2026-10-09

## Q-4 · One decision pull request or two, and in which change

asked: 2026-10-09, the directing conversation
answer: one — fold the Pi move into the unmerged ADR 0007 session amendment
  and continue `plans/changes/stage2-session` (class `architectural`, so no
  ADR answer file is owed)
answered_by: maintainer
status: answered

In the context of an ADR 0007 amendment for the session verb that is drafted
but unmerged and still names OpenCode, facing the choice between merging it as
it stands and following with a second decision pull request, or folding the Pi
move into it, we decided to fold it into one, to achieve a single decision and
no OpenCode wording on `main` that is superseded at once, accepting a larger
diff in that one pull request. — 2026-10-09

## Q-5 · What an `opencode-go/<model>` id selects once the CLI is gone

asked: 2026-10-09, the directing conversation
answer: Pi — the id names the endpoint, not the tool
answered_by: maintainer
status: answered

In the context of the declared `opencode-go` entry in `model-endpoints.yaml`,
facing the choice between letting its ids select Pi and refusing them until a
new id scheme is decided, we decided they select Pi, to achieve unchanged ids
and an unchanged ladder, accepting that the id no longer says which client
program runs. — 2026-10-09

## Q-6 · How the Pi session signs in

asked: 2026-10-09, the directing conversation
answer: the maintainer's own `~/.pi/agent` (not a dedicated agent directory set
  through `PI_CODING_AGENT_DIR`, which was the recommendation, and not
  `OPENCODE_API_KEY` exported in the shell)
answered_by: maintainer
status: answered

In the context of a Pi session that needs the `opencode-go` credential, facing
the choice between a dedicated agent directory holding only that credential,
the maintainer's own `~/.pi/agent`, and a key exported in the shell, we decided
the maintainer's own `~/.pi/agent`, to achieve no extra setup step, accepting
that the directory may hold other providers' credentials the session could
switch to. — 2026-10-09

## Q-7 · Whether network programs ask

asked: 2026-10-09, the directing conversation
answer: no — `curl`, `wget`, `scp`, `rsync`, `ssh`, `sftp` and `nc` run without a
  question (asking was the recommendation)
answered_by: maintainer
status: answered

In the context of the shell patterns that ask (Q-2), facing the choice between
adding network programs to Pi's three (`rm -r`, `sudo`, `chmod/chown 777`) and
leaving them out, we decided to leave them out, to achieve fewer interruptions
and a list that stays close to Pi's own example, accepting that the session can
send files out with a network program without a question, and that the leak
check, which covers the launch only, does not see it. — 2026-10-09

## Q-8 · Which git commands ask

asked: 2026-10-09, the directing conversation
answer: `git reset --hard` and `git clean` ask; `git push` does not (asking before
  all three was the recommendation)
answered_by: maintainer
status: answered

In the context of the shell patterns that ask (Q-2), facing the choice between
asking before all three of `git push`, `git reset --hard` and `git clean`,
before the two that discard work, and before none, we decided the two that
discard unsaved work, to achieve a question before work in the worktree is
lost, accepting that the session can push branches to GitHub without a
question. — 2026-10-09

The patterns that ask are therefore: a recursive `rm`, `sudo`, `chmod` or
`chown` with 777 (Q-2), `git reset --hard` and `git clean` (Q-8). Q-7 and Q-8
refine Q-2; they replace nothing in it.

## Q-9 · Discovery flags of the session; further discarding git commands

asked: 2026-10-09, the directing conversation (after the independent review of
  the Pi chain, #110 to #113)
answer: (1) the session takes `--no-mcp`, `--no-skills`,
  `--no-prompt-templates` and `--no-themes`; context files (`AGENTS.md`) stay
  on ("Vier von fünf (Empfohlen)"). (2) `git checkout -- .` and `git restore .`
  ask as well, like `git reset --hard` and `git clean` of Q-8 ("Ja, beide
  (Empfohlen)")
answered_by: maintainer
status: answered

In the context of the interactive Pi session, which left MCP servers, skills,
prompt templates and themes on, so that an MCP file tool could bypass the
policy's worktree bounds, and of Q-8, which named only two of the git commands
that discard unsaved work, facing the choice between all five, four, only
`--no-mcp` or none of the reviewer call's discovery flags, and between
extending Q-8 and keeping it, we decided four of the five flags with context
files on, and that `git checkout -- .` and `git restore .` ask too, to achieve
a session that cannot get around the worktree bounds through discovery while
it still reads `AGENTS.md`, and a question before the common ways to lose
unsaved edits, accepting that spec criterion 11 ("discovery off") is met
except for context files and that two more commands ask. — 2026-10-09

The maintainer chose the option marked as recommended in a multiple-choice
question (transcript of the directing session, 2026-10-09T23:39Z), not wording
of their own.

[DETAIL] The agent generalised answer (2) to the other forms that discard the
same way: `git checkout -f`, `git checkout .`, `git checkout <ref> -- <path>`,
`git restore <path>` and `git restore --worktree`; `git restore --staged`
alone only unstages and does not ask. Those forms were not asked one by one;
the merge of the decision pull request confirms them (ADR 0012).

## Note — settled instructions 3 and the OpenCode details, 2026-10-09

Settled instruction 3 above ("Deny outside-worktree reads in OpenCode as far
as its configuration supports it") and the [DETAIL] lines on OpenCode (the
dedicated primary agent, the effective-policy check against OpenCode 1.18.35)
are the first build's record. For the OpenCode Go path they are superseded by
Q-1 to Q-6: the launcher is Pi and the policy is a runner-supplied extension.
The instruction's intent stands: deny outside-worktree reads as far as the
launcher supports it, and name the remaining limit.
