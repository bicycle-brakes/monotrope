---
title: "Findings — repair-restore-status"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-rcyf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — repair-restore-status

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: the
new test failed before the edit with the row still reading
`fixed — tests/test_fix.py::test_fix`.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- `kept` is the snapshot taken right before the model call, after the
  attempt's own call line; restoring it drops nothing the runner wrote
  for this attempt into `findings.md` except the statuses.
- `implement` and `draft` pass no `snapshot_findings`, so `kept` is `None`
  there and their behaviour is unchanged.
- This change and pull request #228 (restore-symlink-parent) both touch
  `run_attempts`; a merge of the second will need a look at that hunk.

## Independent runner review, 2026-10-25

An Opus sub-agent of the orchestrating session reviewed the runner with all
open pull requests merged (read-only, in a separate context). Its row for
this change:

| ID | Severity | Finding | Status |
|---|---|---|---|
| R-4 | MINOR | The handler around `checkpoint` caught `Refused` too, so together with #228 it wrote `findings.md` after the decided no-write `RestorationRefused` stop (reproduced), and it rewound `findings.md` after failures raised once the commit existed, while HEAD kept the `fixed` statuses (read only). | fixed — tests/test_stage2.py::test_findings_stay_when_the_checkpoint_fails_without_a_rollback |

The restore now runs only for a `CallFailed` while HEAD is still the
baseline; a `Refused` stop is re-raised untouched.
