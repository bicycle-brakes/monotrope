---
title: "Decisions — doc-currency"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, handover, docs]
---

# doc-currency — Decisions

Class: bounded (bead coding-harness-ni8 proposed `feature` on 2026-10-27, "to confirm"; the maintainer's answer below fixes the mechanism to one small reporting script called by the handover routine, which is bounded).

## Q-1 · What "checked for currency" means at a handover

asked: 2026-11-22
answer: "D, ja" — an automatic mechanism, smaller than updating the documents in the handover PR: a small script (for example scripts/doc_currency.py) reads the paths changed on main since the last handover, maps areas to their documents through a fixed mapping (for example scripts/verify_* and Makefile to docs/how-it-works.md; new ADRs to docs/architecture/; new make targets to README.md), writes "possibly stale: <doc> — new since the last handover: <change>" lines into the handover and opens one bead per possibly stale document (none when one is open already); the handover routine calls it itself; it never blocks and never edits documents.
answered_by: maintainer
status: answered
context: |
  Topic: what the handover does about architecture documents and the front page.
  Intention: the maintainer said on 2026-10-14 that every handover checks the architecture documentation and the repository front page for currency; today nothing does.
  Today: the handover skill writes docs/journal/handover/<date>-*.md and checks nothing about docs/architecture/, docs/how-it-works.md, README.md or ROADMAP.md.
  Repository change: Options: A a fixed line in each handover written by the model; B a blocking gate; C the handover updates stale documents in its own PR; D (asked for by the maintainer: automatic, smaller than C) a reporting script with a fixed mapping that writes lines and opens beads.
  Architecture change: none.

In the context of documents that drift behind the code, facing manual checks, a blocking gate or in-PR repairs, we decided on an automatic reporting script that names possibly stale documents and opens beads, to achieve a check that runs at every handover without blocking, accepting false alarms because it detects an area changed without its document, not whether the document is wrong. — 2026-11-22

## [DETAIL] items decided by the orchestrator (after the research of 2026-11-23)

- **Placement:** the lines go into the handover's `## Needed from the maintainer` section under a sub-heading "Possibly stale documents"; with no finding the sub-heading says "none". Reason: the maintainer reads that section first.
- **The mapping** is a constant table in `scripts/doc_currency.py`, starting with the three pairs of answer D; a pair is added by a reviewed pull request. Reason: one place, visible in review.
- **"Since the last handover"** means since the `target_ref` commit of the newest handover file on `origin/main` (by filename date, then the file's commit time). Reason: every handover carries `target_ref:`.
- **Beads:** the script prints one `tools/bd create` command per possibly stale document with the title "Possibly stale: <doc>" and runs it only with `--write`, after reading open beads with that exact title (`tools/bd list --json`); the handover routine calls it with `--write`. Reason: the `make archive` dry-run discipline; no duplicate beads.
- **Callers:** the handover routine only; the script gets an `OHNE_AUFRUFER` entry with that reason, no CI gate. Reason: answer D — it reports at the handover and never blocks.
- **The vault** is out of scope: answer D names repository documents only.
