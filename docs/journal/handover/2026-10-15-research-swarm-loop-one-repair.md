---
title: "Session handover — research swarm loop-one repairs, 2026-10-15"
category: handover
created: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
tags: [handover, stage-2, research, swarm, repair]
target_ref: 5d72f6de5d546786dd59338fa32417c1815945ed
bead: coding-harness-icw
status: pending
review: {status: pending, approved_by: null, approved_at: null}
---

# Research swarm — loop-one repair handover

The objective is to repair only the eight taken loop-one findings, preserving
the accepted spec, plan and pending decision. This is the runner's Codex
repair attempt on branch `explore/research-swarm`, based on
`5d72f6de5d546786dd59338fa32417c1815945ed`. No commit or git mutation was
performed. The hosted PR state was not read under the worktree-only boundary.

## Completed work

- Failed public and Flash Pi calls retain scrubbed partial stdout; public
  receipts are collected before scratch cleanup on nonzero exit, empty
  answer and timeout. Failed reports reach the record and judge as partial
  evidence, without becoming successful contributions (L1-1).
- The free prompts use the declared topic focuses. The judge receives each
  topic's independent seats and its assigned public evidence, including the
  declared free seat on topic 6. A contradictory topic-6 focus refuses.
  Paid topic and judge calls use their declared endpoint and model (L1-2,
  L1-3).
- The judge's public citations undergo the same receipt check as free
  reports. A rejected reconciliation is retained as failed partial evidence.
  Redirect receipts back both requested and final URLs (L1-4, L1-7).
- Free launchers inherit only executable lookup plus their own scratch
  settings and transport credential. Ambient identity, locale and private
  configuration paths are excluded. The public HTTP transport retains the
  DNS answer's address family through its pinned lookup callback (L1-5,
  L1-8).
- The three routing documents now name `--class`, the research header and
  the spec header, and explain that stated declarations must agree (L1-6).

## Evidence and remaining work

Each of the seven code-row regression functions failed against the untouched
repair baseline before implementation. The fixtures plant the reported
faults, including actual subprocess timeouts and a captured production
HTTPS lookup callback with IPv6-only and IPv6-first DNS answers. They make
no live model or web calls. The final named tests are recorded in the
criterion ledger and the repair response.

The follow-up check after adding topic-6 consistency validation and allowing
one second for the timeout fixture passed: 27 tests, 82 deselected, on
2026-10-15. Ruff lint and formatting, the interview minimums and criterion
ledger checks passed. The four-file regression command passed 650 tests in
337.43 seconds on 2026-10-15:

```sh
.venv/bin/python3 -m pytest tests/test_stage2_swarm.py tests/test_stage2_research_tools.py tests/test_stage2.py tests/test_model_endpoints.py -q --tb=short
```

The follow-up selection covered the final consistency and timeout refinements.
The handover schema suite passed 46 tests with 13 declared skips. The current
frontmatter check and `git diff --check` passed. The report-only documentation
checker still reports corpus link/metadata issues and this handover's absent
`owner` field; that field is excluded by the dedicated handover schema, which
this file follows. No unrelated corpus or schema repair was made.

The runner owns the final red-first replay, `make verify`, findings statuses
and the single checkpoint commit. Full verification was not run by this
attempt: tracker-dependent checks require access outside its permitted
worktree. No complete live swarm or refreshed pinned-Pi runtime qualification
is claimed by these offline repairs. Live free-endpoint qualification still
waits for the maintainer's decision merge.

## Ownership and decisions

No new maintainer decision, appetite or permission is inferred. Repository
artifacts remain English. The pre-existing change to `findings.md` belongs
to the runner and was not edited. This worker claims no tracker ownership,
reads no tracker and makes no tracker write; the orchestrator retains the
single-writer duties and the tracker-before-git push order. No other checkout
or user configuration was read. The measured repair span belongs under
`## Time used` in the change plan.

## Next step

Resume: when I start, I will run `make verify` from the research-swarm worktree as the owning runner.
