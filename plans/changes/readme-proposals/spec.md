---
title: "Spec — readme-proposals"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-7kzl
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: claude-opus-5-5, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, readme]
class: spike
appetite: 2
adr_files: []
---

# readme proposals — Spec

## Goal

Proposals, not edits, for how `README.md` and the documents it links to must
change to describe `main` as of dfede341 (2026-11-17). The maintainer decides
and writes: `README.md` is declared human-written in `decisions/provenance.yaml`.
The maintainer asked for this on 2026-11-17 and chose the model: DeepSeek
through Pi (`opencode-go/deepseek-v4-pro`), started with `stage2.py session`.

## Scope

The task brief is `handover.md` in this folder. The only output is
`research.md` in this folder: per file, every stale or wrong statement with
its evidence and a proposed replacement text.

## Non-goals

- No edit to `README.md` or to any linked file.
- No ADR.
