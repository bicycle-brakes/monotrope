---
title: "Research — stage2-session"
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
tags: [research]
---

# Stage 2 interactive session — Research

Read on 2026-10-07 against `origin/main` at `1c79860`, with the incoming
Flash runner read separately at `origin/feat/stage2-flash-runner`, `11abf42`.
No foreign model was started and no credential file was read. This is local
takeover research by Codex, not a measured GLM explore run.

## What exists today

- The maintainer requested an interactive `session <change> --model <id>`
  verb with declaration and leak checks, a new terminal in the worktree,
  a handover as the first prompt, a findings audit line and OpenCode read
  restrictions. The start-only scope of the leak check is explicitly
  accepted (takeover handover in PR #90, `a3d5585`, section "Next step";
  bead coding-harness-amp, description and notes).
- PR #89 and #90 were OPEN with successful hosted verify checks when read
  on 2026-10-07. `origin/main` is still `1c79860`. The handover says research
  and spec may precede the merge, implementation may not depend on unmerged
  Flash-runner helpers (PR #90, "How to run it through the workflow").
- Existing topic search found the stage-2 reviewer change and the MiMo
  reviewer work, but no existing `stage2-session` change (`rg` over
  `plans/specs/` and `plans/changes/`, 2026-10-07). This change adds an
  interactive launch boundary, not another review-loop implementation.

## Where it lives

- `scripts/stage2.py`: `preflight` resolves the change and spec bead;
  `declaration_problem` checks endpoint, model, framework permission and
  residency; `begin_call` scans the exact prompt and writes date, endpoint,
  model and file/commit/rule counts. `foreign_env` builds an allow-listed
  child environment. The main parser has no interactive-session verb.
- The incoming Flash runner introduces `checked_prompt` and
  `begin_work_call`; the latter checks before writing an attempt audit
  into a chosen artifact (`11abf42`, `scripts/stage2.py`). It also adds the
  runner-owned implementation gate and credential cleanup. No changes were
  made to that branch.
- `scripts/leakcheck.py`, `check`: scans change files, the visible tree,
  branch-reachable history, index and supplied prompt text; reports three
  counts, refuses unmeasurable input and never prints matches. Ignored
  files, reflog and other named exclusions remain outside its coverage.
- `model-endpoints.yaml`, `endpunkte`: main declares `gpt-6.1-sol` for
  `openai-codex`, GLM through Claude Code, and Anthropic endpoints. It does
  not yet declare OpenCode Go. Reviewer declarations and ordering belong
  to the separate reviewer change (coding-harness-ymx).
- `tests/test_stage2.py`, `World` and `STAND_IN`: use temporary git
  repositories and fake executables to measure arguments, environment,
  prompts, audits and refusal paths without real model calls.

## Local CLI and external documentation evidence

- `opencode --version` returned `1.18.35`; `opencode --help` exposes the
  interactive default command, project directory, `--model provider/model`,
  `--prompt` and `--agent`. `opencode debug --help` exposes configuration
  diagnostics. Help only was run, not a model or config dump.
- [OpenCode permissions](https://opencode.ai/docs/permissions/), read
  2026-10-07: permissions may deny operations; `external_directory` applies
  to path-taking tools outside the starting directory. Matching rules use
  the last match. Agent-level rules can override global rules. This is
  tool authorization, not evidence of OS isolation or arbitrary shell-code
  confinement. Actual outside-read refusal has not been measured here.
- [OpenCode configuration](https://opencode.ai/docs/config/), read
  2026-10-07: inline runtime configuration has precedence over project and
  user configuration, but managed policy can override it. File substitution
  can load text from outside the worktree. No resolved maintainer config
  was read; effective restriction remains an implementation verification.
- `codex --version` returned `0.160.1`; `codex --help` exposes interactive
  positional prompt, `--model`, `--cd`, `--sandbox workspace-write` and
  `--ask-for-approval on-request`. It warns about an unwritable PATH-alias
  location in this sandbox; help still succeeds.
- [Official Codex CLI reference](https://developers.openai.com/codex/cli/reference/),
  read 2026-10-07: workspace-write is a recommended bounded execution mode;
  bypassing the sandbox is explicitly dangerous. Neither this page nor local
  help establishes a worktree-only read boundary for that mode.
- macOS Terminal's `do script` AppleScript command can receive a shell
  command (local `/System/Applications/Utilities/Terminal.app/Contents/Resources/Terminal.sdef`,
  command `do script`, read 2026-10-07).
  [Apple's automation guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/CallCommandLineUtilities.html)
  also establishes Terminal scriptability and the need for shell quoting.
  The implementation must pass data separately, quote shell
  arguments and measure detached handoff with a stand-in. No window was
  opened during research; a real GUI launch remains unmeasured.

## What is unclear

- The effective OpenCode permission merge, agent overrides and symlink
  behavior have not been measured on this machine. Tests must not call a
  model outside the runner to measure them.
- GUI acceptance does not prove that authentication, model availability or
  a later interactive turn succeeds. The audit must distinguish preflight
  from successful terminal dispatch, not claim a completed model run.
- The broader bead also asks for Claude/Codex workflow parity. Building
  this verb does not prove hook, skill, display or all-phase parity.
- The handover uses a validator name absent on main:
  `scripts/validate_change_artefacts.py` was not found. The available
  artifact gate is `scripts/plans_registry.py --check` and full `make verify`.

## Files a change would touch

`scripts/stage2.py`, dedicated session tests, `docs/WORKFLOW.md`, an amendment
draft in this change folder and this change's artifacts/index. Launch policy
must be shared code, not an edit to a maintainer's global OpenCode config.
`docs/adr/` and the Flash-runner branch stay untouched. Runtime files may be
created only after preflight and may contain no credential values.
