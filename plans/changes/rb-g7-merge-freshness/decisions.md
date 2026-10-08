---
title: "Decisions — rb-g7-merge-freshness"
status: draft
implementation_status: none
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-34z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, governance, ramp-valve, rb-g7]
---

# Decisions — rb-g7-merge-freshness

## Answered 2026-10-08

- [DECISION] What does "the merge state is checked, not the branch head"
  (RB-G7) require, now that its valve falls due on 2026-10-31?
  1. **Merge ref only (recommended):** a test in `tests/test_ci.py` asserts
     that the generated workflow verifies on `pull_request` with no `ref:`
     override, so CI checks `refs/pull/N/merge` (true today, research
     addendum). The valve closes as RB-M6's did; rule set PATCH (test name).
     Consequence: a green check can go stale when `main` moves before the
     merge, as today.
  2. **Merge ref and up-to-date branches:** option 1, plus "require branches
     to be up to date before merging" in the branch ruleset, asserted by
     `tests/test_repo_settings.py`. One account can hold it. Consequence:
     every pull request must be updated and re-verified after any other
     merge; the maintainer changes the live ruleset; rule set MINOR or MAJOR.
  3. **Amend RB-G7:** drop the second sentence. Consequence: nothing checks
     what is merged; rule set MAJOR.
  Recommended: 1 — it makes the rule's words true by a test and closes the
  valve before its date; option 2 can follow as the ruleset upgrade
  `tests/test_repo_settings.py` already anticipates ("The five are a floor").

  **Answer (maintainer, Claude Code session of 2026-10-08): option 2** —
  merge ref and up-to-date branches. Stated in German as "option 2", after
  the orchestrating session had recommended option 1 and named its cost
  (every open pull request is updated and re-verified after each merge) and
  the gap it closes (a green check computed against an older `main`, e.g. two
  open pull requests changing the same file). What this settles for the
  change: RB-G7 keeps its wording; CI verifying the merge ref is asserted in
  `tests/test_ci.py`; the branch ruleset's "require branches to be up to
  date" is asserted in `tests/test_repo_settings.py`; the maintainer changes
  the live ruleset. The rule set is `human-decided`, so the change goes out
  as a decision pull request (`AGENTS.md` house rule 8).
