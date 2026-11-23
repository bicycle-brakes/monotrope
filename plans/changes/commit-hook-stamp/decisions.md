---
title: "Decisions — commit-hook-stamp"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, commit-hook]
---

# commit-hook-stamp — Decisions

Class: bounded (bead coding-harness-yv9i.2).

## Q-1 · Build this layer now, as its own bounded change

asked: 2026-11-23
answer: 'A — two small bounded P1 beads beside coding-harness-7ftj (maintainer, 2026-11-23, dialog in session c820a13d); this one: the commit hook runs check_frontmatter_current.py --stamp on the staged held documents and re-stages them, for every harness and every human commit.'
answered_by: maintainer
status: answered
context: |
  Topic: preventing the failure of 2026-11-23, when an orchestrator hand edit of plans/changes/isolated-attempts/decisions.md left updated: stale and a draft spent three model attempts on a starting tree no draft may change.
  Intention: the fault should not depend on the orchestrator's care.
  Today: the pre-commit hook in .beads/hooks/ does not check frontmatter; the gate frontmatter-current only reports after the fact.
  Repository change: the pre-commit hook stamps staged held documents; a test with a temporary repository.
  Architecture change: none.

In the context of a stale document date that cost three model attempts, facing a choice between two bounded layers, one note in bead coding-harness-7ftj, or the hook layer alone, we decided on two bounded P1 changes, of which this is one, to achieve a fix that holds for every harness and saves model calls, accepting two small changes instead of one larger feature — 2026-11-23

## Provisional agent decisions on the spec review (2026-11-23, night run 2026-11-23-a)

Decided by the orchestrator by its recommendation, marked provisional; the plan card lists them for the maintainer.

- [DETAIL] **S-1 (provisional agent decision):** 'stampable' means the gate's existing STAMPABLE set (MISSING, UNREADABLE, STALE, FUTURE) — one definition, imported, not copied.
- [DETAIL] **S-2 (provisional agent decision):** a staged held document with no frontmatter or two updated: lines is not stamped; the hook refuses the commit and names the file and the gate's fix.
- [DETAIL] **S-3 (provisional agent decision):** the hook stamps every commit, the runner's checkpoint commits included; the runner already stamps derived fields, so a stamp there is a no-op, and a test shows a checkpoint commit stays unchanged when it is current.
- [DETAIL] **S-4 (provisional agent decision):** the local date is the one check_frontmatter_current.py uses today (date.today() on the host); no second source.
- [DETAIL] **S-5 (provisional agent decision):** when the measurement itself refuses (shallow clone, empty held set), the hook lets the commit through unchanged and prints the reason on stderr; it never blocks a commit for its own inability to measure.
- [DETAIL] **S-6 (provisional agent decision):** a refused commit leaves the index exactly as the user staged it: the hook stamps into a temporary copy and re-stages only when every stamp succeeded.
- [DETAIL] **S-7 (provisional agent decision):** the stamping step lives in a tracked script (scripts/hooks/stamp_staged.py) that the tracked pre-commit entry calls; the bd-generated hook gets one call line through the repository's hook installer, so a regenerated bd hook keeps it (tested).
- [DETAIL] **S-8 (provisional agent decision):** 'future' uses the gate's own FUTURE threshold (later than tomorrow UTC); one definition.
- [DETAIL] **S-9 (provisional agent decision):** the hook script travels into kit copies through scripts/kit/manifest.yaml beside check_frontmatter_current.py; the Definition of Done names the manifest entry.

## Provisional agent decisions on spec review round 2 (2026-11-23, night run 2026-11-23-a)

- [DETAIL] **S-10 (provisional agent decision):** an unreadable `updated:` refuses the commit (criterion 4); the spec drops the second reading.
- [DETAIL] **S-11 (provisional agent decision):** criterion 12 measures the staged blobs (`git show :<path>`) with the gate's own functions, never the working tree.
- [DETAIL] **S-12 (provisional agent decision):** after stamping the index, the hook writes the same stamp to the working copy only when the working copy equals the staged blob before stamping; otherwise it leaves the working copy and prints a one-line notice. Criterion 3 is amended to allow exactly that write.
- [DETAIL] **S-13 (provisional agent decision):** a missing `python3` or PyYAML means the measurement cannot run: criterion 7 governs (commit goes through, reason on standard error).
- [DETAIL] **S-14 (provisional agent decision):** a commit aborted after stamping for another reason keeps the stamped index; the stamp is idempotent and correct; criterion 8 covers stamping failures only.
- [DETAIL] **S-15 (provisional agent decision):** the change does not rely on `bd hooks install` preserving foreign content: the repository's hook installer re-adds the call line, a test runs it after a regenerated bd hook, and the gate reports a hook without the line.
