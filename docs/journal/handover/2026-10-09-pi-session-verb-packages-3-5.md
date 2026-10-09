---
title: "Session handover — the session verb on Pi after work packages 3 to 5, as of 2026-10-09"
category: handover
created: 2026-10-09
updated: 2026-10-09
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-09"
tags: [handover, stage-2, pi, session, tracker]
target_ref: 43bf6f8
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

As of 2026-10-09, nothing of the Pi move is merged. Five work packages of the
plan (`docs/research/2026-10-09-session-verb-on-pi-plan.md`) sit in four
stacked pull requests, each with green CI on its head:

| Pull request | Branch | Head | Package | What it holds |
|---|---|---|---|---|
| #110 | `feat/stage2-session-pi` | not read here | 1 and 2 | the maintainer's eight answers (Q-1 to Q-8) and the artefacts of `plans/changes/stage2-session` re-pointed to Pi |
| #111 | `feat/stage2-session-pi-policy` | `d5663cf` | 3 | the policy extension `scripts/stage2_session_policy.mjs` and its 200 test cases |
| #112 | `feat/stage2-session-pi-runner` | `171fb21` | 4 | `scripts/stage2_session.py` starts the pinned Pi, never the OpenCode CLI; suite 1560 passed |
| #113 | `feat/stage2-session-pi-docs` | `43bf6f8` | 5 | `docs/WORKFLOW.md` and its doc test |

Each PR is based on the one above it. Implemented and tested: packages 1 to 5.
Not validated anywhere: a live Pi. That the extension loads and the handlers
hold in the interactive window is package 7, on the Mac.

## The maintainer's answers (the detail is in `decisions.md`)

Q-1 confirm the load with a read-back; Q-2 the shell asks only on dangerous
patterns; Q-3 file tools bounded to the worktree plus a protected list; Q-4 one
decision pull request folded into the ADR 0007 session amendment; Q-5
`opencode-go` ids select Pi; Q-6 sign-in through the maintainer's own
`~/.pi/agent`; Q-7 network programs do not ask; Q-8 only `git reset --hard` and
`git clean` ask besides the three of Pi's example.

## Next step

1. The maintainer merges the chain in order: #110, #111, #112, #113. After each
   merge the next branch takes `main` in (merge commit, no rebase) and waits for
   CI, because `verify` is required on the merged commit.
2. Package 6: one decision pull request (title `decide(<scope>): …`, label
   `decision`, body from `.github/PULL_REQUEST_TEMPLATE/decision.md`) moving the
   amendment `plans/changes/stage2-session/adr-0007-session-amendment.md` into
   `docs/adr/`, and amending the scope of ADR 0011 and the `bemerkung` of the
   `opencode-go` entry in `model-endpoints.yaml` ("only the review loop"). The
   five-answer duty is met by Q-1 to Q-8.
3. Package 7: the smoke test on the Mac, by the maintainer.

## Needed from the maintainer

- The word "merge" in a message of their own, per pull request or for the chain.
- Pasting `tools/cloud-env/setup.sh` into the cloud environment's setup script
  field (claude.ai/code), still open.
- Deciding D-13 criterion 4 (naming the OpenCode Go rungs), and archiving
  `plans/changes/stage2-mimo` and `plans/changes/interview-minimums` in a pull
  request of its own.

## Tracker state (local to the remote container, not on origin)

`tools/bd dolt push` answered HTTP 403 throughout, so none of these writes
reached `refs/dolt/data`. They are saved as replay commands in
`docs/journal/handover/2026-10-09-remote-session-merges-tracker-and-pi-plan.md`
and need repeating where the push works:

- coding-harness-ymx and coding-harness-6yg closed (their PRs #105 and #104
  merged); coding-harness-kw0 closed (no cost tracking, the work runs on
  subscriptions); coding-harness-0al superseded by the Pi bead.
- The Pi bead (short id 6h4, created in the container only) is claimed: one comment per package 1 to 5
  is still to be added, and Q-7 and Q-8 are to be noted.
- This handover's pull requests name no bead they open or close; #113 changes
  only documents.

Reconnecting GitHub at https://claude.ai/connect-github may clear the 403; this
was suggested, not confirmed.

## Parallel sessions

None known as of this handover. House rule 4 (one tracker writer) holds.

## Resumption

Read this file, then `git fetch` and look at #110 to #113; if the maintainer has
merged any, bring `main` into the next branch before anything else.

## Addendum — review of #110 to #113, 2026-10-09

An independent read of the chain (a subagent that had not seen this session's
reasoning; it ran the policy's `decide()` in node, not pytest, and never saw a
live Pi). Nothing is fixed yet; these are open items, ranked.

**To fix before the chain merges (proposed):**

1. **MCP, skills and prompt templates stay on in the session (confirmed by me).**
   The reviewer call in `scripts/stage2.py` passes `--no-mcp`, `--no-skills`,
   `--no-context-files`, `--no-prompt-templates` and `--no-themes`; the session
   argv in `cli_argv` does not. Pi 1.1.0 reads MCP servers from
   `<agent-dir>/mcp.json` and `.pi/mcp.json`, and `decide()` allows every tool
   that is not a path tool or `bash`, so an MCP file tool bypasses the worktree
   bounds. Fix: decide which of those flags the interactive session takes (at
   least `--no-mcp`), add them to `cli_argv` with tests, and say so in the docs.
   Context files (`AGENTS.md`) probably stay on on purpose; that is the
   maintainer's call.
2. **`git -C "my dir" reset --hard` is not caught** (the option-value part of the
   `GIT` prefix cannot span a quoted space); the same for `git clean`. Fix the
   regex and add a quoted-value test.
3. **`rm` with a line continuation, or `;` inside a quoted argument, is not
   caught** (`rm \` + newline + `-rf y`; `rm "a;b" -r`). Low likelihood.

**Docs and small items:**

4. `docs/WORKFLOW.md` says the pin check runs first; in `run()` the version check
   comes after the leak check and the handover read. Nothing is sent before it,
   so it is harmless, but the sentence and the `require_pi` docstring are wrong
   for this verb.
5. `ENV_ALLOW` drops `PI_CODING_AGENT_DIR` and `SSH_AUTH_SOCK`: a custom agent
   directory is silently ignored, and `git push` over SSH fails inside the
   session. The docs should say so, or the allow-list should change (maintainer's
   call; Q-6 chose `~/.pi/agent`).
6. Only `Refused` and `CallFailed` remove the private directory; Ctrl-C leaves
   it. It is gitignored and holds no secret.
7. No test for the `process.platform` to `caseInsensitive` mapping in the
   extension's default export (matters on macOS).
8. The read-back proves the flag name appears in `--help`, not that the
   `tool_call` handler fires (known and accepted as Q-1; package 7 must show it).

**Checked by me and found not a defect:** the review's worry that `--` might not
be honoured by Pi: the pinned Pi's argument parser handles `--` explicitly
(`dist/cli/args.js`, read from the tarball, not executed). `--no-approve` on the
interactive launch is still only read from the docs.

**Found fine by the review:** path resolution (`@`, `~`, `file://`, symlinks,
`..` in find patterns), fail-closed handling, the Terminal launch quoting, no
call path to the `opencode` CLI, no credential handed over.

**Resumption:** a follow-up commit on `feat/stage2-session-pi-policy` (items 2, 3,
7) and `feat/stage2-session-pi-runner` (items 1, 4, 5, 6), then the docs branch;
the chain is not merged yet, so the fixes can go onto the existing branches.
