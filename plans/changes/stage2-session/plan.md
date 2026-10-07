---
title: "Plan — stage2-session"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
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
For you:     Start a checked interactive OpenCode or Codex session in a new Terminal window.
Done when:   Session refusal/dispatch tests and make verify pass, reviewed code is in a decision PR.
Appetite:    4 hours of implementation and repairs; a stop, not an estimate.
Not now:     Continuous scans, new endpoint approvals, review migration and full harness parity.
Pre-mortem:  suppose it failed: most likely because a harness override weakened the supplied permissions.
Starts unless you say stop.
```

## Route and boundaries

Codex takeover produced research, spec, design and plan because the Claude
session exhausted its budget; research was not a GLM explore call. Phase 4
uses the existing GLM Flash runner. Stop at four hours, never merge. Leave
Flash branch, protected ADRs, provenance, declarations, global configuration,
credentials and reviewer routing untouched. The wider parity bead stays open.
The accepted spec and design are the contract; F-2 is answered.

## Files and operations

- `scripts/stage2.py`: add session dispatch, required `--model`, optional
  `--handover`, reject these switches for other verbs and stage2-off here;
  pass the invoking module to preserve shared exception types under __main__.
- `scripts/stage2_session.py`: implement the algorithm below as a helper,
  never a standalone model entry or credential reader.
- `tests/test_stage2_session.py`: temporary linked worktrees and fake CLI,
  effective-policy and Terminal stand-ins; no real model or GUI calls.
- `.gitignore`: ignore `.stage2-sessions/` runtime policies.
- `docs/WORKFLOW.md`: describe command, activation dependency, audit meaning,
  cleanup and start-only/tool-permission limits, not a review-order change.
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
   IDs on opencode-go only; no aliases, guessing, approval or fallback.
2. Resolve default change-local handover.md or explicit source inside worktree
   before reading; require regular readable nonempty UTF-8. Full text is first
   prompt, with AGENTS/read and launch-limit instructions. Refuse NUL, prompt
   over 32 KiB UTF-8, command over 64 KiB. Resolve CLI and osascript executables
   first; missing prerequisites exit 2. Shared checked_prompt scans actual text.
3. OpenCode: fresh private directory under non-symlink .stage2-sessions/;
   file and inline config for primary harness-session agent pins model,
   denies external_directory and task, asks for bash; --pure. Capture bounded
   `opencode --pure debug agent harness-session` without --tool/--params or
   printed diagnostics. Check schema, primary agent/model and ordered wildcard
   rules. A catch-all denial must have no later allow/ask; bash may ask/deny,
   never allow. Insert explicit denials for specific automatic allowances and
   recheck once; unresolved/managed overrides refuse. No global-file reads.
4. Codex argv: resolved CLI --no-daemon --model ID --cd ROOT --sandbox
   workspace-write --ask-for-approval on-request, positional full prompt.
   OpenCode argv: resolved CLI --pure ROOT --model FULL-ID --agent
   harness-session --prompt PROMPT. Use foreign_env allow-list, no caller API
   tokens/model overrides. Separately shell-quote cd, env -i variables and
   argv; fixed AppleScript takes shell command as argv data. Do not wait for
   interactive exit, use headless verbs or add writable directories.
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
| 2 | Declaration schema and exact selection | malformed, ambiguous, unapproved model/transport/residency accepted |
| 3–4 | Handover boundaries | missing/empty/bad UTF-8/NUL/oversized/outside/symlink prompt sent |
| 5–6 | Leak refusal and second scan | forbidden prompt/index or missing denylist reaches GUI |
| 7–8 | Audit and GUI error injection | false counts, overwritten findings, false success, missing executables |
| 9 | Recorded CLI argv/cwd | headless verb, fallback, wrong model or wait for TUI |
| 10 | Execute command against fake CLI | hostile quotes/newlines/substitution run extra code |
| 11 | Effective policy permutations | global/agent/automatic override escapes denial |
| 12 | Codex exact safety flags | bypass, auto-approval or extra-dir |
| 13–14 | Environment and preparation/cleanup faults | token copied, config overwritten, GUI after write failure or user files removed |
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
Name GUI/model smoke as unrun unless measured through runner. Handover and
hosted green checks complete delivery.

## Time used

Implementation has not started. The orchestrator measures implementation and
repairs with its clock. A file-tool worker without a clock records that
limitation honestly; never invent a measured duration.

2026-10-07 15:14:02–15:29:58 UTC, 15m 56s, waiting counted: GLM Flash
implementation attempt produced no answer or code before operator termination.
Runner returned exit 1 after the CLI exited 143; no restore was needed.
No implementation checkpoint or passing implementation verification exists.
