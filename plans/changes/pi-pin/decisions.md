---
title: "Decisions — pi-pin"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-agx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, pi]
---

# The runner's own pinned Pi — Decisions

Phase 1a for bead coding-harness-agx. Before the interview the maintainer
had settled the scope in the conversation on 2026-10-15 (recorded on the
bead): the runner uses its own Pi install in a repository tools folder with
the version and a lock file in one place; offline contract tests gate a
version move; and "das eigene pi muss mit opencode go und zen funktioneren".

## Q-1 · How a new Pi version proves the isolation

asked: 2026-10-15
answer: "a" — the isolation measurement becomes a contract test suite against the real pinned Pi, with a local stand-in server and no key, run locally and in CI.
answered_by: maintainer
status: answered
context: |
  Topic: how we prove that a new Pi isolates foreign models as well as the old one.
  Intention: ADR 0011 decision 6 says the isolation was measured on Pi 1.1.0 and another version means measuring again; that measurement ran once by hand on 2026-10-08 (local stand-in server, no real key), and Pi keeps releasing.
  Today: the suite never starts a real Pi, only a stand-in script; no test checks whether a real Pi reads outside the worktree or admits foreign tools.
  Repository change: A — a contract suite against the real pinned Pi, locally and in CI (CI needs node and downloads Pi, about 1-2 minutes more); B — the same suite, local only; C — keep the hand measurement in a research note.
  Architecture change: A and B replace "measured on version X" with "measured by the suite" — a new ADR amending ADR 0011 decision 6.

In the context of a Pi that keeps releasing and an isolation measured once
by hand on 1.1.0, facing the choice between a hand measurement, a local
suite and a suite that also runs in CI, we decided on a contract suite
against the real pinned Pi run locally and in CI, to achieve that every
version move is measured automatically, accepting node and a Pi download in
CI. — 2026-10-15
