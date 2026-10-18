---
title: "Research judge capacity and fixed packet sizing"
category: research
status: proposed
created: 2026-10-18
last_reviewed: 2026-10-18
updated: 2026-10-18
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

## Agent derivation under the existing research-swarm contract

Use one fixed whole-packet Unicode-character limit, counting every rendered
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
reserve retains the documented maximum. This implements the existing
spec's derivation duty; it changes no model admission or participant count.
Persist the numeric terms, model, source links and read-on date with the
measured packet size. Re-read the sources when the model or client contract
changes; automatic currency maintenance is separate work.

At J, the normal independent launch preconditions still apply. Above J,
do not call the judge, trim evidence again, reduce the free roster or add
another judge call. Retain all reports, excerpts and terminal outcomes,
and end incomplete with judge-packet-over-limit. The fixed four-thousand-
character per-claim excerpt cap is applied before whole-packet measurement.

## Qualification boundary

Pure packet sizing and independently derived score counts can be tested
without a model. They do not establish exact 39 + 3N dispatch, role settings,
CLI configuration precedence, isolation, complete reconciliation or handoff.
Those remain integration/capture/review obligations. The maintainer's
Claude allowance is still exhausted; no Claude or GLM call was made for
this evidence. The proposed decision pull request remains a draft.
