---
title: "Plan — stage2-session"
status: draft
implementation_status: partial
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-09
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, session]
---

# Plan — stage2-session

```text
For you:     Start a checked interactive Pi or Codex session in a new Terminal window.
Done when:   Session refusal/dispatch tests and make verify pass, reviewed code is in a decision PR.
Appetite:    4 hours of implementation and repairs; a stop, not an estimate.
Not now:     Continuous scans, new endpoint approvals, review migration and full harness parity.
Pre-mortem:  suppose it failed: most likely because the policy extension's behaviour differs inside a live Pi from its tests.
Starts unless you say stop.
```

## Route and boundaries

Codex takeover produced research, spec, design and plan because the Claude
session exhausted its budget; research was not a GLM explore call. Phase 4
uses the existing GLM Flash runner. Stop at four hours, never merge. Leave
Flash branch, protected ADRs, provenance, declarations, global configuration,
credentials and reviewer routing untouched. The wider parity bead stays open.
The accepted spec and design are the contract; F-2 is answered.

**Re-pointed on 2026-10-09** (work package 2 of
`docs/research/2026-10-09-session-verb-on-pi-plan.md`, approved by the
maintainer that day): the OpenCode Go path launches Pi, not the OpenCode CLI.
This section, "Files and operations", "Helper algorithm" and "Tests and
faults" describe the target; "Runner route" and "Time used" below are the
record of the first build and stay as written. The code still starts the
OpenCode CLI until work package 4 lands. Packages 3 to 7 of the Pi plan
(extension, runner port, docs, decision PR, Mac smoke test) are the new
implementation steps; the appetite for them is the Pi plan's own sizes, a
stop and not an estimate.

## Files and operations

- `scripts/stage2.py`: add session dispatch, required `--model`, optional
  `--handover`, reject these switches for other verbs and stage2-off here;
  pass the invoking module to preserve shared exception types under __main__.
- `scripts/stage2_session.py`: implement the algorithm below as a helper,
  never a standalone model entry or credential reader. The seven OpenCode-only
  functions (`policy_config`, `effective_policy`, `wildcard`, `catch_all`,
  `policy_problems`, `insert_denials`, `verify_policy`) go; `pi` replaces
  `opencode` in `TRANSPORTS`, `executables`, `prepare` and `cli_argv`.
- The policy extension (JavaScript or TypeScript for Pi 1.1.0), written by the
  helper into the private directory; its source lives in the repository and
  its handlers are tested without Pi. Where it lives and how the Python tests
  run it (a `node` call that skips when `node` is absent) is a [GAP] for
  work package 3 to settle by reading.
- `tests/test_stage2_session.py`: temporary linked worktrees and fake CLI,
  loaded-extension and Terminal stand-ins; no real model or GUI calls. The 25
  uses of the canned `effective(...)` answer change.
- `.gitignore`: ignore `.stage2-sessions/` runtime policies.
- `docs/WORKFLOW.md`, `AGENTS.md` and the comments in `model-endpoints.yaml`:
  describe command, audit meaning, cleanup, the Pi policy and its limits
  (start-only scan, tool permissions, `bash` outside the dangerous patterns,
  other providers in `~/.pi/agent`), not a review-order change.
- `plans/changes/stage2-session/research.md`, `decisions.md`, `spec.md`,
  `design.md`, `plan.md`, `findings.md`, `adr-0007-session-amendment.md`:
  retain decisions/reviews, record evidence/time and the proposed amendment.
- `plans/INDEX.md`: regenerate with the registry after artifact edits.
- `docs/journal/handover/2026-10-07-stage2-session-takeover.md`: append dated
  evidence, ownership, branch/PR and one resumption action.

## Helper algorithm

1. Require macOS, attached branch and root/cwd exactly matching the git common
   directory parent's `.claude/worktrees/<change>`. Use shared preflight.
   Defensively validate declaration structure, uniqueness, framework permission
   and residency. Exact plain IDs on openai-codex or full opencode-go/<model>
   IDs whose bare model opencode-go lists (these select Pi); no aliases,
   guessing, approval or fallback. For a Pi model call `require_pi` first.
2. Resolve default change-local handover.md or explicit source inside worktree
   before reading; require regular readable nonempty UTF-8. Full text is first
   prompt, with AGENTS/read and launch-limit instructions. Refuse NUL, prompt
   over 32 KiB UTF-8, command over 64 KiB. Resolve CLI and osascript executables
   first; missing prerequisites exit 2. Shared checked_prompt scans actual text.
3. Pi: fresh private directory under non-symlink .stage2-sessions/ holding
   the one policy extension. Its `tool_call` handler blocks read, grep, find,
   ls, edit and write outside the worktree, blocks writes to its own file,
   .stage2-sessions/ and .pi/, asks before a bash call that matches a
   dangerous pattern (blocks it when there is no UI), and blocks when the
   handler itself fails. Read-back: confirm the extension loaded (bounded
   `pi --no-extensions -e FILE --help` lists its flag); no model call, no
   printed diagnostics; the behaviour is the tests' job. No global-file reads.
4. Codex argv: resolved CLI --no-daemon --model ID --cd ROOT --sandbox
   workspace-write --ask-for-approval on-request --, positional full prompt.
   Pi argv: resolved CLI --no-extensions -e FILE --offline --no-approve
   --model FULL-ID, positional full prompt (no print or RPC mode). Use
   foreign_env allow-list, no caller API tokens/model overrides, no key
   handed to Pi. Separately shell-quote cd, env -i variables and argv; fixed
   AppleScript takes shell command as argv data. Do not wait for interactive
   exit, use headless verbs or add writable directories. The exact flag
   spelling is read from the pinned Pi's `docs/cli.md` in work package 4.
5. Recheck prompt immediately before GUI dispatch. Persist unique pending
   audit with date/model/endpoint/source/real scan counts; preparation failure
   means no GUI. After bounded osascript invocation, update only this audit
   to accepted/failed. Failure/timeout exit 1, acceptance exit 0 is not CLI
   startup. Audit update failure leaves honest pending evidence and fails.
   Clean only newly owned policy files on preparation/dispatch failure, not
   after accepted launch; retain accepted policy until the session exits.

## Tests and faults

| Spec | Test | Fault that must go red |
|---|---|---|
| 1 | Parser/canonical worktree | main, wrong cwd, detached branch dispatch |
| 2 | Declaration schema and exact selection | malformed, ambiguous, unapproved model/transport/residency accepted; a Pi off the pin reaching the terminal |
| 3–4 | Handover boundaries | missing/empty/bad UTF-8/NUL/oversized/outside/symlink prompt sent |
| 5–6 | Leak refusal and second scan | forbidden prompt/index or missing denylist reaches GUI |
| 7–8 | Audit and GUI error injection | false counts, overwritten findings, false success, missing executables |
| 9 | Recorded CLI argv/cwd | headless verb, any `opencode` call, fallback, wrong model or wait for TUI |
| 10 | Execute command against fake CLI | hostile quotes/newlines/substitution run extra code |
| 11 | Extension handlers with fake events, run without Pi; loaded-extension check | outside path, protected-path write, listed bash pattern without a question or UI, failing handler, unloaded or second extension passes; each rule has a test that goes red when the rule is removed |
| 12 | Codex exact safety flags | bypass, auto-approval or extra-dir |
| 13–14 | Environment and preparation/cleanup faults | token copied, key handed to Pi, config overwritten, GUI after write failure or user files removed |
| 15–16 | Help/docs/draft/diff | continuous confinement claim, protected ADR or review routing edit |

## Verification and review

```sh
.venv/bin/python3 -m pytest tests/test_stage2_session.py tests/test_stage2.py -q
.venv/bin/python3 scripts/plans_registry.py --check
make verify
```

Full verify before every checkpoint. Existing GLM review loop (at most two
rounds), then final Codex review via stage2.py; decide actual findings, repair
and reverify. Keep loop rows out of final review context until its verdict.
Decision-template PR with label, touch map and open-bead milestone; no merge.
Name GUI/model smoke as unrun unless measured through runner; for Pi the
smoke test is work package 7 of the Pi plan, the maintainer's, on the Mac
(`pi --version` prints `1.1.0`, the extension is listed in `pi --help`, a
launch opens the Terminal window). Handover and hosted green checks complete
delivery.

## Runner route — 2026-10-07

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

Implementation has not started. The orchestrator measures implementation and
repairs with its clock. A file-tool worker without a clock records that
limitation honestly; never invent a measured duration.

2026-10-07 15:14:02–15:29:58 UTC, 15m 56s, waiting counted: GLM Flash
implementation attempt produced no answer or code before operator termination.
Runner returned exit 1 after the CLI exited 143; no restore was needed.
No implementation checkpoint or passing implementation verification exists.

2026-10-07, second implementation attempt (file-tool worker): this worker has
no clock and claims no span; it read the date 2026-10-07 at start and end. It
wrote the helper, the runner wiring, the tests, the workflow section and the
ignore entry as the plan lists them, then stopped for the runner's verify.
The orchestrator's clock measures the real span; no duration is invented here.

2026-10-07, repair attempt on the attempt-2 code (file-tool worker): this
worker has no clock and claims no span; it read the date 2026-10-07 at start
and end. It reviewed the attempt-2 code against the block gates and repaired
three defects, all in `tests/test_stage2_session.py`: the denylist refusal is
now asserted against the rendered verdict on standard output, and the two
OpenCode dispatch tests now script the `osascript` stand-in step that executes
the launch command, so the asserted interactive `opencode` call is actually
recorded. The helper, the runner wiring, the docs and the gates stood the
review otherwise unchanged. The orchestrator's clock measures the real span;
no duration is invented here.

2026-10-07, second repair attempt (file-tool worker): this worker has no clock
and claims no span; it read the date 2026-10-07 at start and end. The reported
`make verify` output was markdownlint noise from a report-only gate, so it
named no blocking gate. By reading the code against `ruff.toml` (line length
120) it found one blocking defect, `ruff format --check`: the `opencode-go
takes the full id` refusal in `scripts/stage2_session.py` fits on one line at
exactly 120 characters and is now written as one. No command ran, so nothing is
verified; the runner's `make verify` decides. The orchestrator's clock measures
the real span; no duration is invented here.

## Package 3 of the Pi plan: the policy extension (2026-10-09)

Built and tested; the runner does not use it yet (package 4).

**The [GAP] of the plan is settled by reading.** The extension is plain ESM
JavaScript in `scripts/stage2_session_policy.mjs`: Pi loads direct TypeScript or
JavaScript files (`docs/extensions.md` of the pinned Pi 1.1.0), and node ESM
needs no build step. It imports only `node:` modules, so the runner can copy it
into the session's private directory and the copy runs unchanged. The Python
tests (`tests/test_stage2_session_policy.py`) run a copy through a node driver
(`tests/stage2_session_policy_driver.mjs`) with made-up events, without Pi and
without a model, and skip when `node` is not installed.

**What it enforces**, with the Pi facts it rests on (all read, none run in a
live Pi): it resolves a tool path the way Pi does (`dist/utils/paths.js`: a
leading `@` stripped, `~` expanded, `file://` read, relative to `ctx.cwd`),
follows symlinks to the deepest existing part so a new file beneath a link
cannot leave the worktree, and blocks `read`, `grep`, `find`, `ls`, `edit`,
`write` outside it; `grep`, `find` and `ls` without a path search the working
directory. `edit` and `write` are also blocked on its own file,
`.stage2-sessions/` and `.pi/`; `.git/` is not (Q-3). A `find` pattern or
`grep` glob that is anchored elsewhere or climbs with `..` is blocked. A `bash`
call matching a dangerous pattern asks through `ctx.ui.select`, and is blocked
without a UI (Q-2). Any failure of the handler blocks the call, as Pi's own
fail-safe does. It registers the flag `--stage2-session-policy`, which
`pi --help` lists when the file is loaded: that is what package 4's read-back
looks for (Q-1).

**The test run caught one defect before any review.** The first pattern for
`git push` did not know a global option with an argument, so `git -C . push` ran
unasked. The patterns now allow `-C <dir>`, `-c k=v` and `--no-pager` before the
verb.

**Planted faults, 2026-10-09:** one rule at a time was removed in the source,
the suite run, the source restored. 25 faults: the outside check, the symlink
resolution, the `@` prefix, `~/` and a bare `~`, the `file://` form, the NUL
check, the own-file and protected-directory rules, case folding, the `find`
pattern and `grep` glob checks, a missing required path, the no-UI block, any
answer accepted, a failing handler letting the call through, a `bash` call
without a command, the flag not registered, and each of the seven dangerous
patterns. The first run left two alive (a bare `~`, and the NUL check's own
message); the tests were strengthened and both then went red. At the end all 25
turn a test red; the suite is 200 cases, green.

**Named limits.** The dangerous-pattern list is the three of Pi's shipped
`permission-gate.ts` plus four of the runner's own (a network client, `git
push`, `git reset --hard`, `git clean`), because the OpenCode policy kept
network and pushes shut; it is one array, `DANGEROUS`, and the maintainer can
shorten it. A tool name the extension does not know (none is enabled with
discovery off) passes. Nothing here was run inside a live Pi: whether the
handler behaves there the way the tests say is package 7, on the Mac.
