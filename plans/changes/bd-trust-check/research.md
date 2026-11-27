---
title: "Research — bd-trust-check"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-5ane.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-27", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# bd trust check — Research

## Topic (bead coding-harness-5ane.2)

Class: bounded. Why (audit S-5, confirmed and understated):
`tools/claude-code/statusline.sh:157` runs `"$beads_root/tools/bd"` whenever
`.beads` exists, `hooks/handover.sh:151` and `hooks/beads-start.sh:149` run
`"$root/tools/bd"`; installed user-wide, they execute the `tools/bd` of any
repository a session opens, so a cloned untrusted repository runs its own
script. `handover.sh:199-204` matches the trust file with `grep -qE -f`, where
a blank line matches everything. What: run a repository-local `tools/bd` only
for repositories on an explicit trusted list (harness-neutral location),
otherwise the `bd` on `PATH` or nothing; ignore blank lines in the trust file.
Acceptance: tests with a temporary untrusted repository whose `tools/bd`
writes a marker: no marker after status line, start hook and handover hook;
trusted repository still works. Source: PR #437 (full codebase audit, base
`24632499`), re-verified against main `b9ce3ac0` on 2026-11-24.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-27: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1319 files, 6132 commits, 12 rules.

## Runner exploration — 2026-11-27

Research for `bd-trust-check` (bead coding-harness-5ane.2). Read-only; nothing written. The runner appends this to `plans/changes/bd-trust-check/research.md`.

## What exists today

**Repository-local `tools/bd` execution in the status line.** `tools/claude-code/statusline.sh`, in the beads block (between the `beads_root` assignment and the background refresh), sets `beads_root` to the repository top or main-worktree top when `.beads/` exists. It then sets `bdc=bd` and switches to `$beads_root/tools/bd` when that file is executable, and runs `"$bdc" -C "$beads_root" list --status in_progress …` in a detached `nohup bash -c` job. The comment there says "A repository that pins its tracker version ships a wrapper; use it." No trust check precedes this. The same pattern appears in `beads_json()` in `tools/claude-code/hooks/handover.sh`: `[ -x "$root/tools/bd" ] && bdc="$root/tools/bd"`, guarded only by the presence of `.beads`.

**Handover hook.** `tools/claude-code/hooks/handover.sh`, in `render()`, has the trust check for handover content. It reads `${HANDOVER_TRUST:-$HOME/.claude/handover-trust}`, takes `origin` from `git remote get-url origin`, and sets `vertraut=1` when `printf '%s' "$origin" | grep -qE -f "$trust"` matches. The trust gate covers only the injection of handover content into Claude's context. The `beads_json` call that runs the repository's `tools/bd` sits outside that gate and is not conditioned on trust. The header of the same file documents the trust file format (one regex per line, matched against origin).

**Repository start hook.** `tools/claude-code/hooks/beads-start.sh` runs `"$repo_root/tools/bd" prime --hook-json` (`run_bounded`, after a `[ ! -x "$repo_root/tools/bd" ]` check). Its header says it is "a repository hook, not part of the user-level installed set — tools/claude-code/install.sh does not wire it." It is wired through `.claude/settings.json` with `bash "$CLAUDE_PROJECT_DIR/tools/claude-code/hooks/beads-start.sh"`.

**Existing trust precedent in the repository.** `.agents/hooks/session-start.sh`, function `trusted_for_repo_tools(repo)`, returns true only when `origin/main` exists and `HEAD` is an ancestor of it. It gates `tools/bd prime` for the Antigravity hook. Its header describes this as the "trust check". No other repository hook uses this criterion.

**Installer.** `tools/claude-code/install.sh` lists `statusline.sh`, `hooks/recap.sh`, `hooks/handover.sh`, `hooks/parallel-sessions.sh` and `hooks/session-scan.sh` as the user-wide set. `beads-start.sh` is not in that list.

**Tests.** `tests/test_handover_entry.py` covers the handover trust branch: a fake HOME with no trust file, and a trusted repository that receives content (`test_a_trusted_repository_gets_the_content`). `tests/test_beads_start.py` uses a recording fake `tools/bd` as a fixture, placed in the repository under test. Its header states that it is "never this repo's" tool. `tests/test_session_scan.py`, `tests/test_recap_lock.py`, `tests/test_omnigent_deny_layers.py` and `tests/test_night_profile.py` also mention the hook scripts. I did not read them in full; I have not checked whether any of them exercise the status line.

**Audit source.** `docs/research/2026-11-24-verified-audit-synthesis-and-roadmap.md` lists `coding-harness-5ane.2` as P1 with the description "status line and Claude hooks execute `$root/tools/bd` from any opened repository without a trust check". The handover `docs/journal/handover/2026-11-24-day-interviews-and-audit-437.md` records the P1 recommendation. The bead's own wording in `plans/changes/bd-trust-check/research.md` cites `statusline.sh:157`, `handover.sh:151`, `beads-start.sh:149` and `handover.sh:199-204`; I confirmed each of these at the named symbols.

## Where it lives

- Run sites for `tools/bd`: `tools/claude-code/statusline.sh` (beads refresh block), `tools/claude-code/hooks/handover.sh` (`beads_json`), `tools/claude-code/hooks/beads-start.sh` (prime call).
- Trust list for handover content: `${HANDOVER_TRUST:-$HOME/.claude/handover-trust}`, read in `handover.sh` `render()`. It is outside the repository.
- Existing trust criterion: `.agents/hooks/session-start.sh`, `trusted_for_repo_tools()`.
- Installed copies: `tools/claude-code/install.sh` copies `statusline.sh` and `hooks/handover.sh` to the user level. The repository copy of `beads-start.sh` runs through `.claude/settings.json`.

## What is unclear

1. **Scope of `beads-start.sh`.** The audit and the bead say hooks run a repository's `tools/bd` "user-wide". The installer does not wire `beads-start.sh`, and its header says so. It runs from the repository's own `.claude/settings.json`. Whether a cloned repository can reach it depends on that repository's settings and on Claude Code's workspace trust; I did not verify Claude Code's trust prompt behaviour, so I cannot say whether that path is reachable without a prompt. Only `statusline.sh` and `handover.sh` are confirmed as user-wide.
2. **Trust file state on the maintainer's machine.** Whether `~/.claude/handover-trust` exists and what it contains is machine-local state. The 2026-09-30 archive note `plans/changes/archive/2026-09-30-adhd-frame/research.md` records that it did not exist at that time. Current state: not read.
3. **Blank-line behaviour.** With `grep -qE -f FILE`, an empty line in the pattern file matches every string. This is standard grep behaviour, but I have not run it against this script here.
4. **Non-repository `bd` fallback.** The bead proposes falling back to `bd` on `PATH` for untrusted repositories. Whether `PATH` `bd` is intended to be used there, and whether the status line should show a stale or empty value, is not stated in any artifact I read.
5. **Name and location of the trusted list.** The bead asks for a "harness-neutral location". No existing file or convention for it was found. The handover trust file is the only current list of this kind.
6. **Interaction with the stale 30 s cache.** `statusline.sh` reads a cache first and runs `tools/bd` only when the cache is older than 30 s. A trust check placed before the cache read changes when the cache is refreshed; I did not trace whether a stale cache would then show data from an untrusted run.
7. **Not read.** `run_bounded` in `beads-start.sh`; `tests/test_handover_entry.py` beyond the trust cases; `tests/test_statusline*` (none found by name); `.claude/settings.json` in full; the rest of `tools/claude-code/install.sh`.

## Which files a change would have to touch

Per the bead's scope, and from the run sites above:

- `tools/claude-code/statusline.sh` — the `bdc=` selection in the beads refresh block.
- `tools/claude-code/hooks/handover.sh` — the `bdc=` selection in `beads_json()`, and the trust gate in `render()` (blank-line handling at the `grep -f` call).
- `tools/claude-code/hooks/beads-start.sh` — the `"$repo_root/tools/bd"` prime call, if in scope (see unclear item 1).
- `tools/claude-code/install.sh` — only if the trusted list or a helper is installed user-wide.
- `tools/claude-code/README.md` — documents the trust file and the hook behaviour (it already describes `~/.claude/handover-trust`).
- Tests: `tests/test_handover_entry.py` (trust cases exist and can be extended), `tests/test_beads_start.py` (fake `tools/bd` fixture is already present), and a new test for the status line, which I found no existing test for.
- The bead's acceptance test (a temporary untrusted repository whose `tools/bd` writes a marker) would need a fixture that runs the status line and both hooks against such a repository.
