---
title: "Tracker pin to bd 1.3.0, the missing items, and the session-end interview — as of 2026-09-17"
category: handover
created: 2026-09-17
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-17"
tags: [handover, beads, tracker, interview, target-architecture]
questions: "8 ([E]8 [F]0 [D]0)"
target_ref: eddfc0b
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Handover — tracker pin to bd 1.3.0 and the session-end interview

Measured on 2026-09-17 at about 14:45: `main` at `4a3af4f` (pull requests
#1–#4 merged), pull request #6 open at `eddfc0b`, the tracker's
`refs/dolt/data` on origin at `162e85e`. Every number below carries this
cut-off unless its line names another.

The session had one task list from the maintainer — operational fixes, two
re-scoped items and five intake items from the target architecture
(`docs/architecture/target-architecture.md`). It ended, on the maintainer's
request, with an interview on the open decisions; each question is recorded
below with the context and the recommendation it was answered against.

## What changed in this repository — pull request #6, open

The tracker store had been migrated to schema v66 overnight, and bd 1.1.2
refuses that store. Three kinds of callers still ran whatever `bd` was on
PATH — the git hooks, the Claude Code SessionStart hook, the Codex hooks — and
the wrapper checked the version of one binary and then executed another.
Pull request #6 routes every caller through the pin:

- The pinned version is 1.3.0; the wrapper finds `~/.local/bin/bd-<version>`
  first and executes the binary it checked (`tools/bd`, `tools/beads/VERSION`).
- A PATH shim that the five git hooks put first on PATH, outside the section
  beads manages, so a reinstall keeps it (`tools/beads/bin/bd`); the agent
  hooks call the wrapper directly.
- Auto-export is off (D-4); house rule 4 in `AGENTS.md` says how the export is
  rendered at session end until the export script arrives with the gate file.
- The kit manifest classifies `tools/` as `bestand` until the tracker
  conventions decide whether the pin travels with the kit.

## Tracker — 15 items

| State | Items |
|---|---|
| closed (3) | bootstrap (`tmr`); research corpus intake (`anw`); verification of the bd 1.3.0 repair (`7px`) |
| ready (9) | P1: classify the red mechanism tests (`2ee`); gate file and one `verify` command (`bo0`); worktree verification (`m34`); template bundle for M1 (`9qo`); CLAUDE.md importing AGENTS.md (`21f`) · P2: corpus correction pull request (`bt8`); change-artefact validator (`jc3`); model routing file (`qvl`) · P3: the five workflow-entry tests from portfolio (`kkh`) |
| blocked (3) | Omnigent step M0, by `2ee`, `bo0`, `m34`, `21f` (`eev`); stage-2 entry measurement, by `9qo`, `bo0` (`kw0`); public readiness, by `bo0` — only its gate waits, the licence and the onboarding page do not (`lir`) |

Written by this session: the gate-list item and the template item re-scoped
to decisions D-10 and the M1 template bundle; nine items created; the
dependencies in the table.

**A second writer was active.** A Codex session ran in this checkout from
14:09 and created and closed the verification item (`7px`) at 14:38, while
this session wrote its last batch of tracker changes. No write was lost — the
export in pull request #6 holds all 15 items and the Dolt push succeeded — but
house rule 4 was not held. This session had checked for running Claude
sessions before its first write and never for Codex. From 14:40 on it wrote
nothing to the tracker, and this file was committed with git plumbing, so that
the shared checkout, its index and its hooks stayed untouched.

**Lesson:** before every tracker write, look for any agent process whose
working directory is the checkout — `claude` and `codex` both — not only at
session start.

## On the maintainer's machine, outside any repository

- **The global `bd` is 1.3.0 behind a guard** (a shell script at
  `~/.local/bin/bd`; the previous binary stays next to it as `bd-1.1.2`). The
  customer instance (`oracle-source-inventory`) still runs a store at bd
  1.1.2's schema, and bd 1.3.0 migrates a store when it opens it — a one-way
  write. The guard refuses, with exit code 64, every call that would reach
  that repository: from inside it or one of its worktrees, or pointed at it
  with `-C`, `--directory`, `--db`, `BEADS_DIR` or `BEADS_DB`. It was tested in
  thirteen cases against a stand-in binary, then live. In that repository `bd`
  now works only when `bd-1.1.2` is called by name.
- **Portfolio's default branch still pins 1.1.2** on a store already at v66;
  its wrapper refuses until its tracker migration branch lands.
- **The local snapshot copy of the customer instance was caught up** (the copy
  dated 2026-08-30). Its git history was fast-forwarded to the instance's
  current default branch, fetched from the instance's remote. Its tracker was
  replaced by the merge of the instance's remote tracker data and its local
  store; the remote data were the newer ones, with a latest change on
  2026-09-17. The merge ran on scratch copies whose Dolt remote pointed at a
  scratch repository, with pushes to the instance's address redirected by git
  configuration. The copy's previous store is kept in its tracker backup
  directory, a local regeneration from 2026-09-01 in its stash, and its
  tracker still syncs only to the snapshot's own remote. The copy was not
  pushed (decision 3). Its tracker is still at the 1.1.2 schema: a bare `bd`
  there migrates it — acceptable for a copy, and a rehearsal for the
  instance's own migration.
- **Nothing was written to the customer instance.** Checked at the end: its
  index and its tracker files keep their earlier timestamps, and its remote
  references are unchanged. One read-only `git status` ran there without
  `GIT_OPTIONAL_LOCKS=0`; the index timestamp shows that it wrote nothing.
- **Incident, contained:** bd 1.1.2 commits a configuration change on its own
  when `bd dolt remote add` or `remove` runs. It created two commits in the
  snapshot copy; both were reset before anything was pushed. Lesson: after
  `bd dolt remote …`, look at `git log`.

## Decisions — session-end interview, 2026-09-17

Each question was put with its context and a recommendation. Seven answers
followed the recommendation; one (4) followed it in part.

| # | Question | Context | Recommendation | Decided |
|---|---|---|---|---|
| 1 | Which commit address this repository uses | the clone carried a placeholder; every commit keeps its address, and the repository is to become a public template (D-17) | the GitHub noreply address, as in portfolio | as recommended — set in the clone's configuration |
| 2 | How the work is cut into pull requests | a handover describing the pull request it sits in was a blocking finding on #3 | two: the operational fixes (#6), then this handover on its own | as recommended |
| 3 | Whether the caught-up snapshot copy is pushed to its remote | a push distributes the customer estate at its 2026-09-17 state once more; no second reader of that remote is known | do not push | as recommended |
| 4 | Which missing items are created | four topics decided in the target architecture had no item | all four: CLAUDE.md import, change-artefact validator, model routing file, the first ADRs together with the WORKFLOW rewrite | three created (`21f`, `jc3`, `qvl`); **the ADRs and the WORKFLOW rewrite were not** — both stay prerequisites of M1 without an item |
| 5 | Whether two more dependencies are set | §12 of the target architecture does not set them; `bd ready` should show only what can start | both: public readiness after the gate file, the measurement after templates and gate file | as recommended |
| 6 | What happens to the nine tests portfolio #162 deleted | four read a portfolio artefact (its run-log schema); five test the entry into a change | split: the four are recorded as lost in portfolio's ADR-032; the five are adopted here once the entry exists | as recommended (`kkh`); the ADR-032 sentence is portfolio's to write |
| 7 | Where the next session starts | the classification of the red tests decides which gates the gate file takes | the classification first | as recommended — noted on the item (`2ee`) |
| 8 | Whether the three merged local branches are deleted | all three are in `origin/main` through #2–#4 | locally only | as recommended — deleted |

## Measured

| What | Result | Cut-off |
|---|---|---|
| `pytest tests/ -q --ignore=tests/test_kit.py` (venv `~/.venvs/portfolio-agentic-engineering`) | 60 failed, 167 passed, 4 skipped — identical on `main` | `eddfc0b` and `4a3af4f`, 2026-09-17 |
| tracked files without a kit role | 4 (two under `.agents/`, two under `.codex/`), down from 6 | `eddfc0b` |
| git hooks through the wrapper | checkout, fast-forward merge and commit ran their hooks without errors | 2026-09-17 |

## The previous handover's first steps, status now

1. The commit address — done (decision 1).
2. Merging #1, #2, #3 in order — done; #4 merged as well.
3. The tracker rule for document-only work — **still open**: an item per pull
   request, or a clause for a session that cannot write. This session created
   items for its own work, not for its two pull requests.
4. The nine lost tests — decided (decision 6). **The twelve deliberate
   duplicates between the repositories are still unrecorded**, here and in
   portfolio's ADR-032.
5. The ready items — the classification is next (decision 7); the gate-list
   and template items are re-scoped.

## What to do first, next session

1. Look for other agent sessions in this checkout — `claude` and `codex` —
   before any tracker write.
2. Review and merge pull request #6, then this handover's pull request.
3. Start the classification of the red mechanism tests (`2ee`).
4. Carry into portfolio #162's next round: the four lost tests for ADR-032,
   and the twelve deliberate duplicates.
5. Before M1 starts, put the question of the ADRs and the WORKFLOW rewrite
   to the maintainer again (decision 4).

## Addendum — state at session close, 2026-09-17 14:55

A parallel agent session — Codex, working in this checkout since 14:09 — was
still active when this session closed. What it changed bears on everything
above. **Where this addendum and the sections above differ, the addendum
holds.**

**The tracker moved on.** That session created and closed one more item, an
evidence-based target state for an Omnigent-first harness (`atx`), and pushed:
the tracker holds 16 items, `refs/dolt/data` on origin is at `3c83da8`. The
export committed in pull request #6 holds 15 and is one item behind. The
export has to be rendered once more — by whichever session writes last, at
its end — and committed to exactly one pull request, so that two pull
requests do not conflict on `.beads/issues.jsonl`. Recommended: pull request
#6, which carries the tracker changes.

**Its work sits on the branch of pull request #6, uncommitted.** Three new
architecture documents dated 2026-09-17 (a target state, a gap analysis
against `eddfc0b`, a dependency-ordered implementation plan), its own
handover of the same date, a pointer in `README.md`, a note in the target
architecture that marks it superseded for sequencing, and the re-rendered
export. Recommended: that work moves to its own branch from `main` before it
is committed, so that pull request #6 stays a tracker change.

**The direction changed.** In that session the maintainer confirmed that
Omnigent coordinates parallel agents from the first proof of concept: two
coding workers in separate worktrees, tracker writes kept with one
coordinator until the five-check worktree verification proves more. §12 of
the target architecture had put parallelism at step M3, and this session
wrote the M0 item (`eev`) and its dependency on the worktree verification
(`m34`) against that older sequence. Both items need reconciling once the
decision record for the new sequence exists.

**Two handovers of the same day, two first steps.** This handover says:
start with the classification of the red tests (`2ee`, decision 7). The
parallel one says: review its three documents, record the decision on the
changed M0/M3 sequence, reconcile the M0 item, then start the gate manifest
and the rule enforcers. Both agree that gates and truthful rule enforcers
come before any pilot. Recommended order for the next session:

1. Review the three Omnigent-first documents and record the decision on the
   sequence — it can change items this session wrote.
2. Reconcile the M0 item and the worktree verification with that decision
   (`eev`, `m34`).
3. Then the classification of the red tests (`2ee`). Decision 7 still holds
   among the implementation items; steps 1 and 2 are decisions, not
   implementation. The classification is unaffected by the new direction and
   may run alongside them — as long as only one session writes the tracker.
4. Merge pull request #6 with the export re-rendered, then pull request #7,
   then the parallel session's pull request.

**The measurements agree.** The parallel session measured the full suite at
`eddfc0b`: 64 failed, 182 passed, 4 skipped. This session's 60 / 167 / 4
excludes `tests/test_kit.py`; the difference is exactly its 4 known red and
15 green tests — the same baseline.

**Deliberately not done.** No tracker write after 14:38: the order of the
next steps is not made mechanical — neither a higher priority for the
classification nor a dependency of the gate file on it — because a second
writer is active; the note on the classification item does not change what
`bd ready` shows. None of the parallel session's files was touched.
