---
title: "Public readiness check — 2026-10-20"
category: research
created: 2026-10-20
updated: 2026-10-20
last_reviewed: 2026-10-20
status: draft
implementation_status: partial
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-lir
tags: [public, licence, leak-check, readiness]
---

# Public readiness check — 2026-10-20

The maintainer wants to make this repository public (2026-10-19/20). This
note records what was checked before the switch, what this pull request
changes, and what stays as an accepted limit. Cut-off: `origin/main` at
`ff1e1de` and every branch reachable on origin, measured 2026-10-20.

## What was checked

| Check | Method | Result |
| --- | --- | --- |
| Denylisted names (customer, employer) | `scripts/leakcheck.py` over the tree, the staged diff and every commit reachable from a branch; denylist outside the repository, 12 rules | clean: 536 files, 1588 commits |
| Key-shaped strings in the whole history | regular expressions for cloud, forge, model-vendor and chat tokens and private-key headers over `git log --all -p` | one hit: a synthetic test key in `tests/test_stage2.py`, split since `a9203e5` so the leak check sees no key literal |
| The customer instance's repository name | `git grep` on `origin/main`, `git log --all -G` | 7 files, 8 commits |
| The maintainer's account name (it contains the employer's name) | `git grep` on `origin/main` | 57 occurrences, almost all pull-request and Actions links |
| Commit author addresses | `git log --all --format=%ae` | one commit carries a private address; 25 carry a placeholder; the rest a forge no-reply address or runner identities |
| Tracker data (`refs/dolt/data`, 145 beads) | `tools/bd export`, the leak check's denylist rules applied to it, `grep` for the names above | clean: no denylist hit, the customer instance not named; the employer's name only inside the account name (140 times) |
| Licence | file listing | none |

## What this pull request changes

- **`LICENSE`:** Apache-2.0, the official text from apache.org (SHA-256
  `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`), as
  decided for public readiness (bead coding-harness-lir).
- **The customer instance is no longer named in living documents:**
  `AGENTS.md` (house rule 6 and the repository table) and
  `docs/architecture/target-architecture.md` (constraint C2 and the context
  diagram) say "the customer instance, a private repository not named here".
- **`tests/test_ci.py`:** the drift-job test no longer spells the instance's
  name; it asserts that no drift command reads a sibling checkout (`../` or
  `~/`), which is the property the test protects.

## Accepted limits

- **Records stay as written.** Five records still name the customer
  instance: one session handover, one research note and three change
  artefacts (two of them quote test output verbatim). Records are preserved,
  not edited.
- **History stays as written.** Every name above remains in earlier commits.
  Removing it means rewriting history, which breaks every clone, worktree and
  open pull request; not done.
- **The account name** stays in old links; GitHub redirects them to
  `bicycle-brakes/monotrope`. Living documents use the new address where this
  pull request or the README rewrite touches them.
- **Not read:** the Actions logs of past runs.

## Still open before the switch

1. The denylist gate as a kit gate (bead coding-harness-lir, third item) is
   not built; the leak check covers the same names before every foreign call
   but is not a gate on every pull request.
2. An onboarding page (bead coding-harness-lir, second item) is not written;
   the README rewrite (#177) covers the first steps.
