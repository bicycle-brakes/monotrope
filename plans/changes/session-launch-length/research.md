---
title: "Research — session-launch-length"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-rm8
owner: Data Architect
provenance: human-written
tags: [research]
---

# session launch length — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3584 commits, 12 rules.

## Runner exploration — 2026-11-07

Research complete. Everything below is prose ready to append to `plans/changes/session-launch-length/research.md`, followed by the `neighbours:` list for the header.

---

**Suggested header addition**

```yaml
neighbours:
  - plans/changes/stage2-session/spec.md
  - plans/changes/go-access-point/spec.md
  - plans/changes/research-swarm/spec.md
```

---

## What exists today

The change's bead (`coding-harness-rm8`, named in `plans/changes/session-launch-length/research.md` frontmatter) is the known defect that a `stage2.py session` Terminal dispatch arrives at the Terminal window truncated. Three session-launch beads are recorded together in `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` (§ around line 162): `coding-harness-bas` (P1, "the stage-2 session launch can leave the Pi command unexecuted at the shell prompt", `docs/journal/handover/2026-10-21-night-run-tenth.md` lines 94–97), `coding-harness-rm8` (the truncation) and `coding-harness-nlq` (P2, "open a session in the VS Code terminal" — the workaround used so far). The bead full texts were not readable in this session (the tracker is the Dolt database under `.beads/`; no rendered copy is committed), so "what each bead says" is an open item — the corpus quotes above are what this session read.

**The launch path.** `python3 scripts/stage2.py session <change> --model <id>` runs `stage2_session.run` (`scripts/stage2_session.py:605`). It assembles the first prompt in `handover_prompt` (`scripts/stage2_session.py:199`): handover text, then the full `AGENTS.md` under the heading `## Repository agent rules`, then the `LAUNCH_LIMITS` block (`scripts/stage2_session.py:74`), then `runner.READ_REQUEST` (`scripts/stage2.py:263`). Two bounds guard the launch: `PROMPT_LIMIT = 32 * 1024` and `COMMAND_LIMIT = 64 * 1024` (`scripts/stage2_session.py:60-61`); the prompt refusal is raised in `run` (`scripts/stage2_session.py:616-619`), the command-bound refusal after `terminal_command` built the one shell line (`scripts/stage2_session.py:659-662`). The commit message `f05b3d98` and the skeleton `research.md` line 27 confirm the route this run travels.

**Why the command is long.** `terminal_command` (`scripts/stage2_session.py:509`) folds everything into one quoted shell line: `cd <worktree> && exec /usr/bin/env -i <env assignments> <argv>`. The argv comes from `cli_argv` (`scripts/stage2_session.py:466`): for Pi it is the pinned wrapper (`runner.PI_WRAPPER`, `scripts/stage2.py:227` = `tools/pi/pi`), eight `--no-*`/`--offline`/`--no-approve` flags, `-e <policy copy>`, `--model <id>`, `--`, and the whole prompt as one argument. The env block is `foreign_env({})` (`scripts/stage2.py:865`), the `ENV_ALLOW` allow-list (`scripts/stage2.py:371-384`, twelve names) — each assignment is quoted into the line. The prompt is the dominant term: `AGENTS.md` alone is 196 lines (read 2026-11-07; byte size not measured in this session), and Pi also reads `AGENTS.md` itself because context files stay on deliberately (maintainer, 2026-10-09; `docs/WORKFLOW.md` lines 1350–1351) — so the rules text travels in the command and again via Pi's own context reading. `shlex.quote` keeps the prompt's newlines as literal newlines inside single quotes, so the "one line" is a multi-line string handed to Terminal.

**The dispatch hop.** `dispatch` (`scripts/stage2_session.py:521`) calls `subprocess.run([osascript, script, command])` — argv data, no shell — with `OSASCRIPT_TIMEOUT = 30.0` (`scripts/stage2_session.py:63`). The script is the fixed `APPLESCRIPT` source (`scripts/stage2_session.py:72`: `do script (item 1 of argv)`), written per attempt into the private `.stage2-sessions/` directory by `prepare` (`scripts/stage2_session.py:436`; the directory is gitignored, `.gitignore:25`). For Go models the send goes through `runner.dispatch_go` (`scripts/stage2.py:1737`) with the checked model binding (`checked_session_model`, `scripts/stage2_session.py:343`; sidecar `MODEL_SIDECAR` line 277), per the `go-access-point` change.

**Acceptance semantics.** Exit 0 of osascript means only "Terminal took the command" (`scripts/stage2_session.py` docstring lines 31–33; `docs/WORKFLOW.md` lines 1371–1375). The audit line goes through `audit_line` → `write_pending` → `finalize` (`scripts/stage2_session.py:549-597`) with `dispatch pending.` → `dispatch accepted.`/`dispatch failed (<why>).`

**The observed failure.** Both truncating launches recorded `dispatch accepted.`: attempt `d0fd2830a244` (`plans/changes/research-swarm/findings.md:3523`) and attempt `598e253fa258` (`plans/changes/research-swarm/findings.md:4146`); the relaunch `191fa0246237` ran only after the maintainer started the captured command in the VS Code terminal (`docs/journal/handover/2026-10-21-merge-day.md:321`, `plans/changes/research-swarm/findings.md:3888` and `:4163`). So truncation happens after osascript returns 0 — Terminal accepted and cut the command anyway, and the audit cannot see it. Because DeepSeek sessions cannot run unattended without this, the night plans excluded them (`docs/research/2026-10-21-night-run-plan.md` lines 80–82) and queued the fix: item 16/18, "Reliable interactive launch … Compare reports before duplicate fixes. Use a short private launcher and distinguish dispatch acceptance from actual startup. Real launch qualification stays attended unless separately authorized." (same file, lines 135 and 179); `docs/research/2026-10-31-run-plan.md:283` re-queues "rm8 the session launch command truncated by the terminal" as build work.

**Where the bounds are written down.** The 32 KiB prompt / 64 KiB command bounds are spec criterion 3 of the neighbouring `plans/changes/stage2-session/spec.md` (lines 81–82: "bounded to 64 KiB to fit the launch transport") and documented in `docs/WORKFLOW.md` lines 1332–1333. The observed truncations prove the real transport limit sits below what the runner accepts — no repository source states the effective threshold.

## Where it lives

- `scripts/stage2_session.py` — the whole verb: `handover_prompt`, `terminal_command`, `cli_argv`, `dispatch`, `prepare`, `audit_line`/`write_pending`/`finalize`, the limits `PROMPT_LIMIT`/`COMMAND_LIMIT`, the `APPLESCRIPT` constant, `LAUNCH_LIMITS`.
- `scripts/stage2.py` — `READ_REQUEST` (`:263`), `ENV_ALLOW` (`:371`), `foreign_env` (`:865`), `dispatch_go` (`:1737`), `PI_WRAPPER` (`:227`).
- `scripts/stage2_session_policy.mjs` — the Pi policy extension copied into the private directory (`install_policy`, `scripts/stage2_session.py:294`); not itself length-bearing except for the `-e <path>` argument.
- Tests: `tests/test_stage2_session.py` (stand-in `osascript`/`codex`/`pi` record argv; `World.command()` at line 174 returns the dispatched line; `expected_prompt` at line 222 pins the prompt assembly), `tests/test_stage2_go_access.py` session tests (lines 581–947), `tests/test_run_report.py:819` (`test_session_calls_keep_explicit_fields_and_dispatch_state`), `tests/test_pi_contract.py` real-Pi contract tests (lines 1189, 1235).
- Docs that state the current bounds: `docs/WORKFLOW.md` §"The interactive session" (lines 1312–1385, bounds at 1332–1333); `plans/changes/stage2-session/spec.md` criterion 3.
- Evidence trail: `plans/changes/research-swarm/findings.md` lines 3523, 3888, 4146, 4163; `docs/journal/handover/2026-10-21-merge-day.md:321`; `docs/journal/handover/2026-10-21-night-run-tenth.md:92-105`; `docs/research/2026-10-21-night-run-plan.md:135,179`; `docs/research/2026-10-31-run-plan.md:255,283`; `docs/journal/handover/2026-10-25-cloud-runner-fixes.md:162`.

## What is unclear

- **Which layer truncates, and at how many bytes.** The chain is Python argv → osascript → AppleScript `do script` → Terminal's shell input. No repository source measures where the text is cut or the effective limit; the code fact is only that the runner's own ceiling (64 KiB) exceeds what survived. Not measured, not stated anywhere I read — written here as a gap, not a guess.
- **The byte sizes of the failed commands** (attempts `d0fd2830a244`, `598e253fa258`) are recorded nowhere; the audit line carries counts of the leak scan only, and the handover files lived in the gitignored `.stage2-sessions/` and are gone.
- **The full text of the three beads** (`-rm8`, `-bas`, `-nlq`) was not readable in this session (Dolt tracker, no rendered copy); the night-run plan's instruction to "compare reports before duplicate fixes" is not yet fulfilled by anything I read.
- **Test coverage of the command bound.** A search for `COMMAND_LIMIT`, `PROMPT_LIMIT` and the refusal message ("the launch transport takes at most") across `tests/` returned nothing: not found — the 64 KiB refusal appears untested. (Distinct from "tested and failed"; no assertion was found either way.)
- **Whether a fix may change the acceptance semantics.** Spec criterion 8 and the workflow text pin "accepted = Terminal took the command, nothing more"; a launch whose command is silently cut satisfies that wording while failing in fact — closing that gap plausibly touches the `stage2-session` spec, but that is a design/spec question left open here.
- **Why the DeepSeek relaunch (`191fa0246237`) succeeded** where its twin (`598e253fa258`) truncated — same handover, same counts in the audit lines; what differed (window state, shell state, timing) is not recorded.

## Which files a change would have to touch

- `scripts/stage2_session.py` — command construction (`terminal_command`, `cli_argv`), the private launch directory (`prepare`), the limits (`PROMPT_LIMIT`, `COMMAND_LIMIT`), the dispatch (`dispatch`) and the audit (`audit_line`, `finalize`) if acceptance evidence changes.
- `tests/test_stage2_session.py` — the stand-in harness that asserts the dispatched line and prompt; new coverage for whatever bound or launcher shape changes.
- Possibly `tests/test_stage2_go_access.py` and `tests/test_pi_contract.py` — the session's Go-binding and real-Pi paths ride on the same launch files.
- `tests/test_run_report.py` — only if the session call's recorded fields change.
- `docs/WORKFLOW.md` §"The interactive session" — the 32 KiB/64 KiB sentence and the acceptance semantics.
- `plans/changes/stage2-session/spec.md` criterion 3 and criterion 8 name the current bounds and semantics; how a change reconciles with that spec (edit vs. supersede) is an interview/spec question, not settled by anything I read.
