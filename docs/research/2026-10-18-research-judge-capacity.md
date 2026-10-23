---
title: "Research judge capacity and fixed packet sizing"
category: research
status: proposed
created: 2026-10-18
last_reviewed: 2026-10-18
updated: 2026-10-23
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, swarm, judge, context]
---

# Research judge capacity and fixed packet sizing

## Evidence read on 2026-10-18

Anthropic documents a 1,000,000-token context and 128,000-token maximum
output for the exact claude-opus-5-5 model.
([Model overview](https://platform.claude.com/docs/en/models/opus-5-5/overview))

Claude Code documents native 1M context for recent Opus versions and a
minimum client version of 2.1.280 for Opus 5.5. Configuration can lower the
window. Its noninteractive client can refuse a flagged request instead of
switching when switchModelsOnFlag is false; availableModels also constrains
fallback. A fixed-role launch must control these settings, its fallback
chain and ambient workspace discovery.
([Model configuration](https://code.claude.com/docs/en/model-config))

Local inspection on 2026-10-18 only resolved the executable's
symlink: its target names version 2.1.302. The binary was not invoked.
Account access, remaining Claude allowance, effective managed settings,
actual context acceptance and a live provider call were not measured.
No credential file was read. This is documented model capacity, not a
reachability or account entitlement result.

## Recorded implementation derivation

Authority remains the whole-packet sizing ruling (S-38 in
[decisions.md](../../plans/changes/research-swarm/decisions.md)). That ruling
requires a derived limit and records that the actual Opus context size was
not read; it deliberately sets no numeric limit. This note supplies no new
maintainer decision and does not amend that ruling.

As inspected on 2026-10-23 at repair baseline `7aacf14`,
`scripts/stage2_research_judge.py::research_judge_capacity_policy` records the
following implementation policy. The packet measurement counts every rendered
instruction and the canonical data packet:

```text
capacity tokens          = 1,000,000
output reserve tokens    =   128,000
transport reserve tokens =    72,000
tokens per character     =         4
J = floor((1,000,000 - 128,000 - 72,000) / 4) = 200,000 characters
```

The conversion and transport reserve are conservative agent estimates,
not vendor guarantees or a measured tokenizer upper bound. The output
reserve uses the maximum reported in the dated evidence above. The code
therefore applies J = 200,000; this is an agent-derived implementation value,
not a numeric limit set by S-38 or a measurement of effective pinned-client
capacity. The policy retains those source links and the 2026-10-18 read-on
date, and the run manifest records it with the measured packet size. The
sources were not re-read for this documentation repair. Re-reading them when
the model or client contract changes remains necessary; automatic currency
maintenance is separate work.

At J, the code still requires the independent launch preconditions. Above
J, it refuses judge dispatch and retains the reports, excerpts and terminal
outcomes, ending incomplete with judge-packet-over-limit. S-38 forbids
shortening evidence to fit, reducing N or adding a second judge call. The
fixed 4,000-character per-claim excerpt cap is applied before whole-packet
measurement.

## Qualification boundary

Pure packet sizing and independently derived score counts can be tested
without a model. They do not establish exact 39 + 3N dispatch, role settings,
CLI configuration precedence, isolation, complete reconciliation or handoff.
Those remain integration/capture/review obligations. The maintainer's
Claude allowance is still exhausted; no Claude or GLM call was made for
this evidence. The proposed decision pull request remains a draft.
