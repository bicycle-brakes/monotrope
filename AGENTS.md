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
   transported via `refs/dolt/data` on origin. `.beads/issues.jsonl` is a
   rendered export, not the wire protocol.
3. **Use `tools/bd`, never bare `bd`.** The wrapper pins the version and
   refuses `init`, `migrate`, `upgrade` — the three verbs that can change the
   shared database for everyone. The prefix (`coding-harness-`) was fixed at
   init and cannot be corrected afterwards.
4. **One writer per tracker.** While another session runs, none writes. Check
   before `bd` writes; after every write let auto-export render
   `.beads/issues.jsonl` and run `bd dolt push`.
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

## Sibling repositories

| Repo | Role |
|---|---|
| `portfolio-agentic-engineering` | framework governance (rule set, gates, ADRs, lessons), OSI→lakeswitch transfer logistics, domain content — the origin this repo migrates from |
| `lakeswitch-ai` | product repo running a clean-room instance of the workflow |
| `oracle-source-inventory` | customer instance — read-only boundary for framework sessions |
