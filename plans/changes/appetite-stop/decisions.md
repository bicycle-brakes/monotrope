---
title: "Decisions — appetite-stop"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-uxa9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, appetite]
---

# appetite-stop — Decisions

Class: bounded (one counted answer owed; two given). Interview held on
2026-11-03 through the interview tool, one question per call. The bead's
own description (maintainer, 2026-10-28, "Mach das") fixes the rest: the
runner sums the plan's measured `## Time used` spans against the card's
Appetite line before each further `implement` or `repair` attempt and stops
with an appetite-stop message; the orchestrator then answers cut, park, drop
or continue.

## Q-1 · Where the runner stops

asked: 2026-11-03
answer: "Bei 2×, Verlängerung vermerkt" — at 1× the card's appetite the runner records that the self-extension is in use; at 2× it starts no further attempt.
answered_by: maintainer
status: answered
context: |
  Topic: at which limit the runner stops.
  Intention: the runner's arithmetic depends on it; the explore found it written nowhere.
  Today: every plan card has an appetite; since PR #292 it extends once by itself up to twice its size; the runner checks nothing — on 2026-10-28 one call ran 3.9 of 4 hours unattended. A bead note of 2026-10-31 proposed stopping at 2× and recording the extension.
  Repository change: scripts/stage2.py (before each implement or repair attempt) and tests; at a stop the maintainer or orchestrator answers cut, park, drop or continue. Options: stop at 2× with the extension recorded; stop at 1×.
  Architecture change: none; an existing rule gets enforced.

In the context of a runner that starts attempts without looking at the appetite, facing a stop at the card's appetite or at its self-extended double, we decided that the runner records the extension at 1× and starts no further attempt at 2×, to achieve the rule of PR #292 enforced by the runner, accepting that a run may use up to twice its card's appetite unattended. — 2026-11-03

## Q-2 · Stop by impact

asked: 2026-11-03
answer: "Eigener Folge-Bead" — this change stays with the measured time stop; stopping by impact is weighed as a doctrine line in a bead of its own (coding-harness-7krc).
answered_by: maintainer
status: answered
context: |
  Topic: the 2026-11-02 bead note "stop by impact, not by effort".
  Intention: the note stood on the bead "for the maintainer to weigh", undecided.
  Today: the note comes from an outside template (dsh-superagent): pause when work would break callers' expectations, change a module's responsibility, or keep failing — not after a fixed time. The runner cannot measure that; it can measure time.
  Repository change: none in this change; a follow-up bead for the doctrine (prompt 04, WORKFLOW). Options: own follow-up bead; drop; widen this bead (likely class feature).
  Architecture change: none.

In the context of a stop the runner can measure and one it cannot, facing one change for both or two, we decided to keep this change on the measured time stop and weigh the impact stop in its own bead, to achieve a bounded change the runner can enforce, accepting that the impact stop waits. — 2026-11-03
