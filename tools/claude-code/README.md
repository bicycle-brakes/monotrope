# Claude Code session display

The maintainer's Claude Code setup for working across several repositories and
parallel sessions: a status line that says where a session is and what it is
doing, an entry point at session start, a safety net under the handover, and a
warning when two sessions share one checkout. It is user-level tooling — it is
installed into `~/.claude` and works in every repository, so it stays here and
does not travel with the kit (`scripts/kit/manifest.yaml`, catch-all `tools/`).

Provenance: written by Claude Code (Opus 5) at the maintainer's request on
2026-09-18, tested on the maintainer's machine (macOS, bash 3.2, jq 1.7);
not yet reviewed.

## What it shows

```text
lakeswitch-ai ⎇ spec/declared-document-layer ✓ aktuell │ Opus 5 (1M context) │ ctx 259k/600k 43% (max 1M)
⧉ 1 weitere Session: adhd-rellief-e7 (wartet) – Erledigt: Commits parat · Nächstes: Vault-Skelett mit Vorlag…
↻ Recap: Erledigt: Scan, Haiku getestet, CLAUDE.md, lakeswitch grün, Entscheidung für adhd-rellief · Nächstes: adhd-rellief, Portfolio
```

| Line | Says | Comes from |
|---|---|---|
| 1 | repository (and `[worktree x]` inside a linked worktree), branch, distance to the upstream (`✓ aktuell`, `↓N hinterher`, `↑N nicht gepusht`), model, context used against the auto-compact window | `statusline.sh`; a background `git fetch` at most every five minutes |
| `◆` | beads in progress, always with their title | `bd list --status in_progress`, cached 30 s, refreshed in the background; the repository's `tools/bd` wrapper when it has one |
| `⚠` (red) | another session works in **the same checkout** | `hooks/session-scan.sh` over `~/.claude/sessions/` |
| `⧉` | other live sessions, their state and their recap | same |
| `↪ Einstieg` | until this session has a recap: the next step of the handover it started from | `hooks/handover.sh start` |
| `↻ Recap` | one line — done · next — updated after every answer | `hooks/recap.sh stop` (Haiku, async) |
| `▶ Jetzt` | the request being worked on right now | `hooks/recap.sh prompt` |

The colours distinguish the kinds of information; the texts are German because
the maintainer reads them.

## The pieces

| File | Hook event | Does |
|---|---|---|
| `statusline.sh` | status line | everything above |
| `hooks/handover.sh start` | SessionStart | shows the entry (latest handover under `docs/journal/handover/` or `journal/`, its next step, the working tree measured now). The handover's content goes to Claude only for **trusted** repositories — `~/.claude/handover-trust`, one regex per line, matched against origin (bead `hit`: a cloned repo must not pipe its `journal/` into every session). Others get metadata and a hint to read the file |
| `hooks/parallel-sessions.sh` | SessionStart, UserPromptSubmit | tells Claude when another session works in the same checkout, so it warns before changing files |
| `hooks/recap.sh` | UserPromptSubmit, Stop | the rolling recap, and the automatic session note (`~/.claude/session-notes/`) |
| `hooks/session-scan.sh` | — | the one session scan both of the above and the status line use |
| `skills/handover/SKILL.md` | `/handover` | writes the handover as a file in the repository, by that repository's convention, and always opens a pull request for it |

The handover is the file in the repository, never the chat (`AGENTS.md`). The
automatic note is only a safety net for a session that ended without one: the
next start shows it when the last session kept working after the newest
handover, and says so.

## Install, check, update

```bash
tools/claude-code/install.sh --check   # what differs from ~/.claude; changes nothing
tools/claude-code/install.sh           # copy the files, merge settings.json
```

The install copies the six files into `~/.claude` and merges `settings.json`:
it sets `statusLine` and adds each hook of `./settings.json` whose command is
not there yet; everything else in the file stays. A replaced file is kept as
`<name>.bak-<timestamp>`. Restart Claude Code afterwards.

Change a file here and reinstall — a change made only in `~/.claude` is
overwritten by the next install, which `--check` shows first.

Needs `jq`, `git` and `perl`. Without `claude` on the PATH the recap and the
note stay empty; without `bd` the beads line stays hidden.

## State it keeps

| Where | What | Kept |
|---|---|---|
| `~/.claude/recaps/<session>.*` | recap, current request, entry line, which note a session continues | 7 days |
| `~/.claude/session-notes/<session>.*` | the automatic note and its metadata | 90 days |
| `$TMPDIR/claude-statusline/` | beads cache, fetch lock | until the machine clears it |
