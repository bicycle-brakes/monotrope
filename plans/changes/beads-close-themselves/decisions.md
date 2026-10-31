---
title: "Decisions — beads-close-themselves"
status: draft
implementation_status: partial
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-l1if
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# beads-close-themselves — Decisions

Class: bounded (one counted interview record owed; Q-1 below). Reason for
the class: one reconciler script, its call at session start and in the merge
step, and one rule in `prompts/07-commit.md`; no gate, ADR or architecture
changes. The answer was given in German in the conversation; `answer` quotes
it and adds the English sense.

## Q-1 · How beads close once their work has merged

context: |
  Topic: beads that stay open after their pull request merged.
  Intention: on 2026-10-30 nine such beads were found and closed by hand;
  no script reads the Closes-Bead trailer, and "closes after the merge"
  lived as PR prose.
  Today: closing depends on a person or the merge agent remembering it.
  Repository change: a reconciler script, its call in the start hook
  (tools/claude-code/) and in the merge step, and the trailer rule in
  prompts/07-commit.md.
  Architecture change: none, no ADR.
asked: 2026-10-30, conversation 2026-10-30 (about 22:50 UTC)
answer: "Ja, so (Empfohlen)" — yes: an idempotent reconciler that reads Closes-Bead trailers on main, runs at session start and in every own merge step; not a CI gate and no GitHub Action
answered_by: maintainer
status: answered

In the context of the tracker drifting behind main, facing nine merged beads left open on 2026-10-30, we decided that an idempotent reconciler closes every bead named in a Closes-Bead trailer on main, at session start and in each own merge step, to achieve that the tracker follows main whoever merged, accepting that a bead closes only once a session starts or merges after its pull request. — 2026-10-30

## Details for the draft

[DETAIL] **Only the trailer counts.** A bead closes when a commit reachable
from `origin/main` carries `Closes-Bead: <id>`; PR prose never closes. Reason:
one machine-readable form; the maintainer chose the trailer as the only way.

[DETAIL] **Idempotent and quiet.** A bead already closed is left alone; the
reason names the commit and, where the message names it, the PR number.
Reason: it runs at every session start.

[DETAIL] **Only the tracker writer runs it.** The start hook calls it before
`bd prime`; the starting session is the one writer (house rule 4), and the
script ends with `tools/bd dolt push`. A second session in the same
repository does not run it. Reason: one writer per tracker.

[DETAIL] **No CI gate, no GitHub Action.** CI reads the tracker only, and a
red gate would block unrelated pull requests. Reason: the maintainer's answer.
