---
title: "Decisions — bd-1-3-4"
category: decisions
status: draft
implementation_status: none
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-tr84
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tracker, beads, supply-chain]
---

# bd-1-3-4 — Decisions

Class: bounded (bead coding-harness-tr84).

## Q-1 · Which bd version to pin, and from which repository

asked: 2026-11-14
answer: "ja" to bd 1.3.4 (not 1.4.0), and "nehme die neue repo" — download from github.com/gastownhall/beads.
answered_by: maintainer
status: answered
context: |
  Topic: the pinned tracker program bd is 1.3.0 of 2026-09-15; the newest stable release is 1.3.4 of 2026-11-04, and 1.4.0 exists only as release candidates.
  Intention: 1.3.3 closes a path by which a committed .beads/.env or a cloned repository's config could make bd run a command, and updates two dependency advisories govulncheck reported as reachable; 1.3.1 to 1.3.3 fix data loss and wrong targets (bd delete, bd doctor --fix, bd compact, bd purge).
  Today: bd 1.3.0 without those fixes; tools/beads/install.sh downloads from github.com/steveyegge/beads, which redirects to github.com/gastownhall/beads on 2026-11-14.
  Repository change: tools/beads/VERSION, the checksum files under tools/beads/checksums/, the download address in tools/beads/install.sh, the wrapper's pin and its tests; a small pull request.
  Architecture change: none; within 1.3.x there is no schema migration, so the update is a binary swap. 1.4.0 would be a one-way schema migration (schema v74, Dolt 2.6 or newer), which tools/bd refuses by design, and stays a decision of its own.

In the context of a tracker program two months and four releases behind, facing a choice between the stable 1.3.4 and the 1.4.0 release candidate, we decided for 1.3.4 from the new repository address, to achieve the security and data-loss fixes without a migration, accepting that 1.4.0 and its schema migration wait for a stable release and a decision of their own. — 2026-11-14
