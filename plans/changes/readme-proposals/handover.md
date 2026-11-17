# Task: proposals for README.md and its linked documents

You are working in a git worktree of this repository (branch
`docs/readme-proposals`, branched from `origin/main` at dfede341 on
2026-11-17). Bead: coding-harness-7kzl. Class: spike.

## Goal

Work out **proposals** for how `README.md` and the documents it links to must
change so that they describe the repository as it stands on `main` today.
Write nothing except the one output file below. **Do not edit README.md or any
other file**: README.md is declared human-written in
`decisions/provenance.yaml`, so the maintainer decides and writes.

## Files in scope

`README.md`, and the files it links to:

- `AGENTS.md`
- `docs/how-it-works.md`
- `docs/orchestration.md`
- `docs/testing.md`
- `docs/WORKFLOW.md`, only where README.md summarises or cites it
- `tools/claude-code/README.md`
- `model-endpoints.yaml`, only where README.md names models, routes or terms
- `COMMERCIAL.md`

## How to work

1. Read README.md fully. Read each linked file where README.md summarises or
   cites it.
2. Compare each statement with the code and documents on this branch. Typical
   drift to look for:
   - phases and gates;
   - which model runs which phase (Codex is `gpt-6.1-terra` since
     2026-11-15; the review loop is per ADR 0021);
   - runner verbs (`.venv/bin/python scripts/stage2.py --help`);
   - counts and dates without a cut-off;
   - links that point nowhere;
   - features described as planned that exist, or the reverse.
3. Use `git log` and `git grep` for evidence. Every claim needs a
   `file:line` or a command with its output.
4. Keep the README's structure and tone: short sentences, plain words, a
   reader without context. Bead coding-harness-tlr4 asks that the top lead
   with what the workflow enforces that a prompt-only workflow can only
   advise, with measured numbers and their cut-off. Make one proposal for
   that too, marked as such.

## Output

Write `plans/changes/readme-proposals/research.md` in English. Keep its
existing header (frontmatter) unchanged and append below it. Structure:

- `## Summary`: at most 8 bullets, the most important first.
- One `## <file>` section per file. Each finding is a block with these
  fields:
  - **Where** (`file:line`)
  - **Today** (the quoted text)
  - **Why it is stale or wrong** (evidence)
  - **Proposed text** (ready to paste)
  - **Linked files that must change with it**
- `## Not checked`: what you could not read or verify. Write "not read",
  never "none".

Cut-off for every statement: commit dfede341, 2026-11-17. When done, say so
in the terminal and stop.
