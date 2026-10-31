---
title: "Decisions — go-access-point"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-4tr4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage-2, opencode-go]
---

# go-access-point — Decisions

Class: feature (three counted interview records owed; three below). The change
introduces one place that admits the OpenCode Go address for every Go path.
Today the research swarm checks a hard-coded `/zen/go/v1`, while the review loop
checks nothing (the open finding DL-B-8). Phase 1 ran through GLM 5.3 Flash and
a Claude Haiku 5.5 sub-agent by the maintainer's exception of 2026-10-31,
because the research swarm is blocked by this change's own subject
(`research.md`).

## Q-1 · Which Go paths go through the one place

asked: 2026-10-31
context: |
  Topic: what the shared Go access point covers.
  Intention: on 2026-10-31 the research swarm refused every Go model, because Pi reports the base URL https://opencode.ai/inference/go/v1 and the swarm admits only /zen/go/v1. The question comes now because the maintainer decided that Go access is solved and managed in one place.
  Today: only the research swarm checks the address, against a literal in scripts/stage2_swarm.py. The review loop copies the catalog's baseUrl unchecked (DL-B-8). The interactive session checks nothing either. That makes three places with two opinions.
  Repository change: one module reads one address record, and every Go path calls it.
  Architecture change: yes — one source for the Go address.
  Question: who goes through the shared place? Options: all Go paths (recommended) / both swarms only / the swarm first, the rest later.
answer: "Ich möchte das bei Zentral gesteuert werden" — every Go path (review loop, research swarm, probes, interactive session) is controlled from the one place.
answered_by: maintainer
status: answered

In the context of three Go paths that disagree about which address may receive
a change's content, facing a research swarm that refuses everything and a
review loop that admits anything, we decided that every Go path — review loop,
research swarm, availability probes and the interactive session — reads its
admitted address from one place, to achieve one rule that a change of Go's
address meets everywhere at once, accepting that the review loop will refuse
catalog rows it accepts today. — 2026-10-31

## Q-2 · An address the record does not admit

asked: 2026-10-31
context: |
  Topic: what happens when Go reports an address that is not admitted.
  Intention: exactly this happened on 2026-10-31 (inference instead of zen). The swarm stood still, and the review loop noticed nothing.
  Today: the swarm blocks silently as "pi-malformed", and the loop lets everything through.
  Repository change: the central place decides alike for every path.
  Architecture change: yes — one rule for every Go path.
  Question: how should it react? Options: block and report (recommended) / warn and run on / block only a foreign host.
answer: "Sperren, nur gleicher Host" — another path on opencode.ai runs on with a notice; a foreign host is blocked.
answered_by: maintainer
status: answered

In the context of a Go catalog row whose base URL differs from the admitted
record, facing the choice between stopping every swarm at each path move and
sending content to an unchecked destination, we decided that a different path
on the admitted host `opencode.ai` (https, no credentials, no query) runs on
with a notice naming the old and the new path, while any other host is
refused, to achieve no standstill when Go moves a path and no data to a foreign
host, accepting that a path change on the admitted host takes effect before
anyone has read it. — 2026-10-31

## Q-3 · Who maintains the address record

asked: 2026-10-31
context: |
  Topic: who maintains the Go address in the central place.
  Intention: the address changes (on 2026-10-31 for the second time in two days), and someone must admit the new one.
  Today: the address stands only in code and in prose.
  Repository change: an address field (host, paths, read date, source) in the Go entry of model-endpoints.yaml.
  Architecture change: yes — admitting an address becomes a step of its own.
  Question: how is a new address admitted? Options: the agent proposes a pull request and the maintainer merges (recommended) / the agent maintains it itself / only the maintainer maintains it.
answer: "Agent pflegt selbst" — on the admitted host the agent records a new address itself when the Go page names it.
answered_by: maintainer
status: answered

In the context of an address record that must follow Go's documented paths,
facing a record that would otherwise wait on the maintainer at every path
move, we decided that the agent records a new path on the admitted host itself,
with the Go page's reading date and source, to achieve a record that stays
current without a maintainer step, accepting that `model-endpoints.yaml` is
held from agent commits today, so the spec must place the record where an
agent may write it or the maintainer must lift the hold for that one field —
a decision this change puts to the maintainer, not one it takes. — 2026-10-31

## Details for the draft

[DETAIL] **DL-B-8 is the first slice.** Reason: the review loop sends a
change's diff to whatever base URL Pi's catalog names. That is a data-flow gap
today, while the swarm's refusal only blocks work.

[DETAIL] **The catalog sources (pi.dev, models.dev) are out of scope.** Reason:
they are where the catalog comes from, not where content goes. The catalog
redirect is the merged change of bead coding-harness-j2wb, and the model
registry (bead coding-harness-wq1m) will take them up.

[DETAIL] **The design must fit the model registry** (bead coding-harness-wq1m).
Reason: the maintainer asked on 2026-10-31 for every phase's model and every
provider to be governed centrally. The Go access point is its first slice, so
its record must be a part of that registry, not a parallel one.
