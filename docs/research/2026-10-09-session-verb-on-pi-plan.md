---
title: "The session verb on Pi — plan and open questions, as of 2026-10-09"
category: research
status: proposed
created: 2026-10-09
last_reviewed: 2026-10-09
updated: 2026-10-09
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-09"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, stage-2, session, pi, plan]
---

# The session verb on Pi — plan and open questions

A plan, not a build. Nothing in `scripts/` or `tests/` changes until the
maintainer approves it. Facts as of 2026-10-09 at `origin/main` `7afa5b8`; the
Pi facts come from the docs of the pinned Pi 1.1.0, read and not run (the
assessment is the addendum of
`docs/journal/handover/2026-10-09-0al-local-start.md`, branch
`chore/0al-prep`).

## What can the harness do afterwards that it could not before?

**Nothing new.** `stage2.py session` already starts an interactive session on
an OpenCode Go model. Afterwards it does so without the OpenCode CLI, so one
launcher (Pi) carries all OpenCode Go traffic, and the failure of
`stage2.py session` under OpenCode 2.x (bead coding-harness-0al) disappears
because no `opencode` call remains. The price is a weaker proof of the policy
(below). Choosing this is a decision about dependencies and risk, not about
capability. Reason: the maintainer, 2026-10-09 (German): "ich will keine
opencode mehr benutzen."

## As is, to be

- **As is.** Model id `opencode-go/<model>` selects the `opencode` transport.
  `verify_policy` writes the runner's policy, `effective_policy` asks
  `opencode --pure debug agent` for the rules in force and refuses what it
  cannot confirm. Under OpenCode 2.x that call fails, so the verb refuses (bead
  coding-harness-0al, measured 2026-10-08 on the maintainer's Mac, not
  re-measured).
- **To be.** The same id selects the `pi` transport. The runner starts the
  pinned Pi (`require_pi`, 1.1.0) with discovery off, one policy extension
  loaded explicitly, the declared model, `--offline` and `--no-approve`, in the
  same Terminal window and with the same leak checks and audit lines. The
  session signs in with a Pi agent directory the maintainer owns (question 6);
  the runner reads no credential. The extension asks
  before every `bash` call and blocks file tools outside the worktree. The
  runner can confirm the extension *loaded*; its behaviour is held by tests.

## Work packages

| # | Deliverable | Done when | Size |
|---|---|---|---|
| 1 | The phase-1a interview: six questions below, at least five maintainer answers in `decisions.md` of the change (it carries an ADR, so five are owed) | gate `interview-minimums` green | S, 30 min of the maintainer |
| 2 | Re-point the existing change `plans/changes/stage2-session` (spec, design, plan, the unmerged ADR 0007 amendment draft) from OpenCode to Pi; about 54 mentions in 7 files | validators green; no `opencode` left except in history notes | M, 2 h |
| 3 | The policy extension and its handler tests, run without Pi and without a model. It also blocks writes to its own file, to `.stage2-sessions/` and to `.pi/` | each rule has a test that goes red when the rule is removed | M, 3 h |
| 4 | The runner port in `scripts/stage2_session.py`: `pi` replaces `opencode`; seven OpenCode-only functions go; 25 uses of the canned `effective(...)` answer in the tests change | `make verify` green; offline tests prove the Pi argv, the loaded extension, the refusal on a Pi off the pin, and that no `opencode` is ever called | L, 4 to 6 h |
| 5 | Docs: the session section of `docs/WORKFLOW.md`, `AGENTS.md`, comments in `model-endpoints.yaml` | no remaining reference to the OpenCode CLI except history | S, 1 h |
| 6 | The decision pull request | CI green; the maintainer merges | S, 30 min |
| 7 | One real smoke test on the Mac: `pi --version` prints `1.1.0`, the extension is listed in `pi --help`, a launch opens the Terminal window | recorded in `findings.md` | S, maintainer, 20 min |

The appetite is a stop: when a package outgrows its size, stop and report
expected / found / what now. The sizes add up to 11 to 13 hours, one and a
half working days; the interview and the Mac smoke test are the maintainer's
time.

## Not now

- GLM through Pi (bead coding-harness-rwa), which needs its own decision.
- A behavioural check of the extension inside a live Pi (RPC `get_state`,
  a canary call). It needs a model call and a design of its own.
- Windows. The verb runs only on macOS.
- Raising the Pi pin.

## Open questions for the interview (six, with a recommendation each)

1. **How strong is the read-back?** Extension loaded, plus handler tests
   without Pi (recommended), or also a live canary call. Consequence of the
   first: a bug in the extension's behaviour that the tests miss is not seen at
   launch.
2. **Which `bash` calls ask?** Every call (recommended; the same as today's
   `bash: ask`), or only dangerous patterns as the shipped
   `permission-gate.ts` does. Consequence of the second: fewer prompts, more
   shell commands run unasked.
3. **What may the file tools do?** Read and write inside the worktree and block
   everything outside (recommended; the same as today's
   `external_directory: deny`), or also block writes to `.git/`.
4. **One decision pull request or two, and in which change?** Fold the Pi port
   into the still unmerged ADR 0007 session amendment so there is one decision
   (recommended), or merge that amendment first as it stands and amend it
   again. Continuing `plans/changes/stage2-session` (class `architectural`) is
   recommended: the gate `adr-answers` asks only `feature` changes for an ADR
   answer file, while a new `feature` folder would owe one as well as the five
   interview answers (`check_adr_answers.py`, read 2026-10-09).
5. **What happens to an `opencode-go/<model>` id when the CLI is gone?** It
   selects Pi (recommended; the id names the endpoint, not the launcher), or
   the verb refuses it until a new id scheme is decided.
6. **How does the Pi session sign in?** The doctrine says the session reads no
   credential file and copies no token, so the loop's way (the runner reads
   `~/.config/cc-routing/secrets.env` and hands the key over) is not available.
   Pi saves a login in `<agent-dir>/auth.json`, default `~/.pi/agent`
   (`docs/providers.md`, `docs/configuration.md` in the package). Options:
   (a) a dedicated agent directory outside the repository, set by the runner
   through `PI_CODING_AGENT_DIR`, that the maintainer fills once with `/login`
   and that holds only the `opencode-go` credential (recommended: the runner
   reads nothing, and Pi has no other provider to switch to); (b) the
   maintainer's own `~/.pi/agent` (brings every stored provider, every setting
   and every installed package into the session); (c) `OPENCODE_API_KEY`
   exported in the maintainer's shell (the key then sits in every Terminal
   window).

## Risks, named

- **A model switched inside the session is not leak-checked.** The doctrine
  already says so for OpenCode. With Pi it depends on question 6: in a
  dedicated agent directory holding one credential there is no other provider
  to switch to; in the maintainer's own directory there is. `--models <id>`
  scopes cycling; whether `/model` still lists others is for package 7 to
  measure.
- **The model can write the policy.** The policy file lives under
  `.stage2-sessions/` inside the worktree, where the file tools are allowed,
  and Pi has `/reload`. The extension therefore blocks writes to its own file,
  to `.stage2-sessions/` and to `.pi/` (package 3), and `--no-approve` keeps
  project-local Pi files from loading. `bash` can still write there; the
  `bash` prompt is what holds that.
- The extension API belongs to Pi 1.1.0. Raising the pin means measuring the
  extension again; the runner already refuses any other Pi.
- Extensions are TypeScript or JavaScript run inside Pi. How the repository's
  Python tests run its handlers (a `node` call that skips when `node` is
  absent) is a [GAP] for package 3 to settle by reading, not by asking.
- `ctx.ui.select` is the prompt for `bash` calls. Whether it behaves in
  a Terminal window opened through `osascript` is what package 7 measures.
- A Pi session can run approved shell commands that read what the maintainer's
  user can read. That is the limit `docs/WORKFLOW.md` already states for the
  OpenCode path; it does not get worse, and it does not get better.

## Changes made after the review of 2026-10-09

The first draft of this plan was checked against the code and the pinned Pi's
docs. It changed in these places: the sign-in question (6) and its risks were
missing; the extension did not protect its own file; the sizes were summed as
"about one working day" but add up to 11 to 13 hours; the change folder and
class were left open although they decide whether an ADR answer file is owed;
and the OpenCode 2.x failure was stated as a fact without its source and date.
Checked and unchanged: the OpenCode-only code (seven functions, 25 test uses,
54 mentions in 7 files), the Pi facts (interactive mode, no approval prompts,
`tool_call` can block, no sub-agents, no web-fetch tool), and the pin check.
