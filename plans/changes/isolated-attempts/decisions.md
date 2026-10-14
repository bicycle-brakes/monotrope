---
title: "Decisions — isolated-attempts"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, isolation]
---

# Isolate each writing attempt — Decisions

Phase 1a for bead coding-harness-s9r, asked by the orchestrating Claude Code
session on 2026-10-14, each question with its context first (what it is
about, why, what happens today, what changes).

## Q-2 · Which runner verbs are isolated

asked: 2026-10-14
answer: the three automatic writing verbs (draft, implement, repair) and the interactive session verb as well.
answered_by: maintainer
status: answered

In the context of four verbs that let a model write — three automatic, one
interactive with the maintainer present — facing the choice between the
automatic three and all four, we decided on all four to achieve one boundary
for every model that writes, accepting a larger change and a less direct
interactive session. — 2026-10-14

## Q-3 · Whether reads are isolated too

asked: 2026-10-14
answer: yes — reads outside the change are confined as well, not only writes.
answered_by: maintainer
status: answered

In the context of Codex and the review models being able to read outside the
worktree (the residual risk ADR 0007 and ADR 0011 name), facing the choice
between confining writes only and confining reads too, we decided on reads
too to achieve that a model sees only what its call needs, accepting that
this practically requires operating-system isolation. — 2026-10-14

## Q-1 · How strongly an attempt is isolated

asked: 2026-10-14
answer: a fresh container for each attempt — only the folders and the one login the call needs are passed in, network only to the model's API; the boundary is tested.
answered_by: maintainer
status: answered

The maintainer asked first what containers bring and chose after the
explanation (the model sees only what is mounted, for reads and writes; the
network can be limited; the wall becomes testable; nothing is left behind).

In the context of attempts that run as the maintainer's user behind sandbox
settings no test measures, facing the choice between a throwaway copy per
attempt and a container per attempt, we decided on a container per attempt to
achieve a tested boundary for reads and writes, accepting a container tool on
the maintainer's machine, an image to maintain and slower starts. — 2026-10-14

## Q-4 · Whether this change also removes the runner's own leftovers

asked: 2026-10-14
answer: yes — bead coding-harness-b5w (a failed run's derived writes block the next run) is taken into this change and closes with it.
answered_by: maintainer
status: answered

In the context of runner writes (INDEX render, frontmatter stamps, format, the
route block in `plan.md`) partly made before the attempt, outside any
container, facing the choice between one change and two on the same code, we
decided on one change to achieve that a failed run leaves nothing behind,
accepting that the spec must also cover writes outside the attempt. The
exploration of b5w is on branch `explore/derived-leftovers`. — 2026-10-14

## Q-5 · Which container tool is the default

asked: 2026-10-14
answer: Podman as the default; the runner calls one configurable container program, so Docker or Apple `container` can replace it by a setting.
answered_by: maintainer
status: answered

The maintainer asked for a deep dive first ("die beste Option, die sich evtl.
auch auf Windows-Maschinen nutzen lässt"); the comparison is in
`research.md`, "Container tool comparison — 2026-10-14". No container tool is
installed on the maintainer's Mac yet; the live boundary test waits for the
install.

In the context of a container per attempt that should also work on Windows,
facing the choice between Podman, Apple `container` and a trial of Docker
Sandboxes, we decided on Podman behind a configurable program to achieve one
free, rootless tool on macOS, Windows and Linux CI, accepting that attempts
share one machine VM with each other. — 2026-10-14
