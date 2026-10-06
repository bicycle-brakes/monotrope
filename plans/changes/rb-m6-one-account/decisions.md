---
title: "Decisions — rb-m6-one-account"
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-bma
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# rb-m6-one-account — Decisions

Phase 1a (interview) was skipped: the maintainer decided what rule RB-M6 asks
for in the Claude Code session of 2026-10-05, relayed to phases 1–3 by the
orchestrating session, and what remains is mechanics. Below, that decision is
recorded as answered; the spec carries the `[DETAIL]`s that follow from it.

## Addendum 2026-10-05: the maintainer decides RB-M6 (answered)

The question: rule RB-M6 asks for code-owner review and an approval not by the
last pusher, which no one can give while the maintainer, the agents and every
token act as one GitHub account; its valve falls due on 2026-10-31 and then
turns every run red. The maintainer had created a ruleset on `main` the same
day (pull request required with no approval, required check `verify`, no
force push, no deletion, no bypass).

The answer, in the maintainer's words:

> "RB-M6 asks for what one account can hold: pull request required, required
> check verify, no force push, no deletion, no bypass — exactly today's
> ruleset, asserted from within the repository. The second approval
> (code-owner review, approval not by the last pusher) returns as soon as a
> second identity exists (e.g. a GitHub App)."

What this settles for the change: RB-M6's row is amended to these five
requirements and the return trigger, its last sentence (an unreachable
management API is BLOCK, not green) stays, and the requirements are checked
against the live ruleset from within the repository. The rule set is
`human-decided`, so the change goes out as a decision pull request (`AGENTS.md`
house rule 8); the merge confirms it.

## Awaiting the maintainer: the ADR question

The spec classes the change as a `feature` and proposes "no ADR" in its header
(reasons there). That is the workflow's standard question for a feature, not
an open `[DECISION]` of this spec; the maintainer's one-sentence answer is
recorded with `python3 scripts/harness.py decide adr --change
rb-m6-one-account --answer … --reason "…" --stated-in "…"`, exactly as
stated. Until then the gate `adr-answers` keeps `make verify` red.

## Addendum 2026-10-06: the maintainer's answers in the interview

Asked one at a time in the Claude Code session on 2026-10-06:

1. **ADR question: no** (recorded with `scripts/harness.py decide adr`, the
   recommended option: the change applies ADR 0008 and the decision of
   2026-10-05; the RB-M2 exception of PR #55 set the precedent without an
   ADR).
2. **Finding F-2 (level 4 against §3): keep level 4 and amend the ladder.**
   The maintainer chose the recommended option: §3 gains a sentence that a
   gate with `placement: writer` blocks only the run on the maintainer's
   machine, so a merge on GitHub without that run is not stopped, and the
   RB-M6 row says so in its own words. Not chosen: back to level 2; a real
   CI block later through a second identity.

## Addendum 2026-10-06 (later): the GitHub Actions pin

3. **Finding F-8: keep the pin** (maintainer, Claude Code session
   2026-10-06, the recommended option). RB-M6's `verify` must come from
   GitHub Actions (`integration_id` 15368); spec term (b), criterion 5 and the
   RB-M6 row say so, and the 4.0.0 entry says LakeSwitch's ruleset lacks the
   pin, which the maintainer adds there in GitHub. Finding F-9 (the §3 edit
   and the heading date against criterion 3) follows from the F-2 answer and
   is fixed with it, without a question of its own.
