# coding-harness — Agent Instructions

The home of the coding workflow: **seven phases, three stages**, the session
handover, the kit that carries the process into new repositories, and the
research corpus behind it. This repository is the source of truth for the
process; `portfolio-agentic-engineering` and `lakeswitch-ai` run instances
of it.

**Status: bootstrapping.** The mechanism (WORKFLOW.md, prompts, templates,
kit scripts) migrates from `portfolio-agentic-engineering` in measured steps.
The migration plan and current state live in the bootstrap handover:
`docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`.

This is the only instruction file. There is no `CLAUDE.md` — Claude Code
(≥ 2.1.277) reads `AGENTS.md` itself when none exists, and a `CLAUDE.md` beside
it would silently replace it (`tests/test_entry_points.py`).

## The workflow in one screen

| # | Phase | Artifact | Gate |
|---|---|---|---|
| 1 | Explore | `plans/changes/<name>/research.md` | — |
| 1a | Interview *(optional, human-called)* | `decisions.md` | every `[DECISION]` answered — or skipped with a reason |
| 2 | Spec | `spec.md` | validator green, no open `[DECISION]` |
| 2a | Spec-Review *(optional)* | lines for `findings.md`, dimension SPEC | no open `[AMBIGUITY]` |
| 3 | Plan | `plan.md` | validator green |
| 4 | Implement | code + tests | `make verify` green |
| 5 | Verify | test output as evidence | stop-hook blocks on a red tree |
| 6 | Review | `findings.md` | no open BLOCKER — `[DIVERGENT]` counts as BLOCKER |
| 7 | Commit | pull request | CI green |

Plus the session handover (the eighth movement — `docs/journal/handover/`,
`direction: framework->framework`) and the question protocol:
`[DECISION]` → human · `[GAP]` → explore, don't ask · `[DETAIL]` → agent
decides, reason into the artifact.

Full doctrine: `docs/WORKFLOW.md` — arriving with migration step 3.6; until
then it lives at `portfolio-agentic-engineering/docs/WORKFLOW.md`.

## House rules

1. **Content artifacts are English** — commit messages and PR bodies included.
2. **Beads only.** The tracker is the Dolt database under `.beads/`,
   transported via `refs/dolt/data` on origin. No rendered copy is committed:
   the hosted CI hydrates, renders once and presets `BEAD_RENDER`; every
   reader goes through `scripts/bead_render.py`. A fresh clone needs
   `tools/beads/install.sh && tools/bd bootstrap --yes` before any
   tracker-reading gate can measure.
3. **Use `tools/bd`, never bare `bd`.** The wrapper pins the version and
   refuses `init`, `migrate`, `upgrade` — the three verbs that can change the
   shared database for everyone. The prefix (`coding-harness-`) was fixed at
   init and cannot be corrected afterwards.
4. **One writer per tracker.** While another session runs, none writes. Check
   before `bd` writes; after the writes run `tools/bd dolt push`. The push
   order is tracker first, git second: CI renders the gate from
   `refs/dolt/data`, so a git push that outruns the tracker push merges
   against a stand the commits claim to include — and goes red on exactly
   that gap (bead coding-harness-4t8). Auto-export
   is off, and no rendered copy is committed (bead coding-harness-1jg.3):
   a local reader renders fresh through `scripts/bead_render.py`. Because
   the diff no longer shows tracker changes, a pull request names in its
   body every bead it opens, changes or closes (maintainer, 2026-09-23).
5. **The handover is the file, not the chat.** Session end → a file under
   `docs/journal/handover/`. A number without its commit or date reads as a
   historical one — every count carries its cut-off.
6. **The customer instance is out of bounds.** What is needed from
   `oracle-source-inventory` travels as a *requirement*, never as an
   expression — no filename, field name, entity or layer name from there
   appears in a framework artifact.
7. **Texts carry their own meaning.** A reader without this session must
   understand every sentence; bead ids and file names go in parentheses as a
   suffix, never as the carrier of a sentence.

## Communication and session continuity

- Speak German with the maintainer; keep repository artifacts English.
- Use short, plainly worded messages with clear headings. Lead with the main
  point and one concrete next action; show at most three immediate priorities.
  Explain necessary technical terms and keep optional detail separate.
- When describing changes, say what behavior changed and why it matters.
  Distinguish proposed, implemented and tested work explicitly.
- Ask one decision at a time when possible, with a recommendation and its
  consequence. Do not ask again for settled decisions or existing permission.
- At session start or after a break, read the latest relevant handover and its
  addenda; check the working tree and current PR state before acting. Begin
  with a short orientation: **Where we are / Next step / Needed from you**.
  Say "nothing right now" when no answer is needed. Do not require the user
  to reconstruct the previous chat or read the entire backlog.
- Before ending or handing over a session, maintain a dated file under
  `docs/journal/handover/`. Record the objective, completed work and evidence,
  decisions and preferences, unfinished work/blockers, branch/commit/PR,
  parallel-session ownership constraints, and one concrete resumption action.
  Preserve prior records with a dated addendum; task status stays in Beads.
- Link the handover in the closing message. The next session must be able to
  resume from that file without asking the maintainer to repeat the context.

## Tracker quick reference

```bash
tools/bd ready              # open, unblocked work
tools/bd show <id>          # detail view
tools/bd create "title" -d "description" -p 1
tools/bd update <id> --claim
tools/bd close <id> --reason="…"
tools/bd prime              # full tracker context for a session
tools/bd dolt push          # push tracker data to origin (refs/dolt/data)
```

## Sessions across checkouts

- **Another session in the same checkout:** say so before changing a file,
  committing or switching the branch, and offer a worktree. House rule 4 holds
  for the tracker meanwhile.
- **What could not be read is "not read", never "none".** A file that would
  not open and a query that returned nothing say different things.
- **A standing rule belongs in the repository's `AGENTS.md`** — every harness
  reads it; the chat, a memory and a harness's user file do not reach the next
  one. Where an agent may not write that file (lakeswitch declares it
  `human-decided`), propose the exact text instead.
- **The maintainer's Claude Code display** — status line, entry at session
  start, handover safety net, parallel-session warning, `/uebergabe` — lives in
  `tools/claude-code/`; each line of the display is documented beside the tool.
  Change it there and reinstall with `tools/claude-code/install.sh`, never
  only in `~/.claude`.

## Sibling repositories

| Repo | Role |
|---|---|
| `portfolio-agentic-engineering` | framework governance (rule set, gates, ADRs, lessons), OSI→lakeswitch transfer logistics, domain content — the origin this repo migrates from |
| `lakeswitch-ai` | product repo running a clean-room instance of the workflow |
| `oracle-source-inventory` | customer instance — read-only boundary for framework sessions |
