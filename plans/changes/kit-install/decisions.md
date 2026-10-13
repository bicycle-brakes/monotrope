---
title: "Decisions — kit-install"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, kit, install, lakeswitch]
---

# Kit install and update — Decisions

Phase 1a for bead coding-harness-2uk, on 2026-10-13, after the exploration in
`research.md`: of the 83 files the kit carries, lakeswitch-ai at `ce88eee`
holds 0 identical, 3 edited and 80 missing; it re-implemented the mechanism in
`src/lakeswitch/`.

## Q-1 · Who the install command is for

asked: 2026-10-13
answer: A — first for fresh repositories; for an existing instance such as lakeswitch-ai a comparison report that shows what is missing or differs, and the instance adopts piece by piece in changes of its own.
answered_by: maintainer
status: answered

In the context of a kit that lakeswitch-ai never installed (80 of 83 files
missing, its own mechanism in `src/lakeswitch/`), facing the choice between an
install for fresh repositories plus a comparison report for existing
instances, a full switch of lakeswitch-ai to the kit now, or a lakeswitch-only
command, we decided on fresh repositories first plus the report to achieve a
usable command soon without risk to lakeswitch-ai, accepting that lakeswitch
gains only step by step. — 2026-10-13

## Q-2 · How later improvements reach a target

asked: 2026-10-13
answer: A — a pinned version: the target carries a lock file with the kit commit (`harness.lock.yaml`, as lakeswitch-ai already plans); `kit update` fetches the new version, overwrites only kit files, and reports a kit file the target has changed instead of overwriting it.
answered_by: maintainer
status: answered

In the context of a kit with no version or source marker today, facing the
choice between a pinned version in a lock file, a three-way merge of kit files
the target may edit, or a vendored copy in a folder of its own, we decided on
the pinned version to achieve a simple, traceable update that fits the
planned release builder and pin (bead coding-harness-dj9), accepting that a
target's edit of a kit file stops the update for that file until someone
resolves it. — 2026-10-13
