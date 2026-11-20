---
title: "Decisions — journal-citation-gate"
category: decisions
status: draft
implementation_status: none
date: 2026-11-19
created: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-x9ed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-19", model: "Opus 5.5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, provenance]
---

# journal-citation-gate — Decisions

Class: bounded (bead coding-harness-x9ed; one answered question is owed —
Q-1 below, answered by the maintainer on 2026-11-19 in the conversation).

The explore (research.md, route flash) could not read the bead and studied a
new gate; the problem is narrower. The check is the existing test
`tests/test_provenance.py::test_journal_is_never_cited_without_a_date`, the
named enforcer of rule RB-P5 (`docs/governance/regelwerk.md`, § P). On
2026-11-19 it is red in two places where nobody cites a journal file by hand:
a journal path inside the runner-appended `research-swarm/v2` record blocks of
`plans/changes/ontology-relation-layer/research.md` (PR #411), and the glob
`docs/journal/handover/*.md` inside a phase-2a review row of
`plans/changes/runner-stamps-provenance/findings.md` (bead
coding-harness-f9sv).

## Q-1 · What the journal-date check leaves out

asked: 2026-11-19
answer: "A: Muster + Runner-Blöcke" — in English: the check leaves out a citation whose target is a pattern or placeholder (it contains `*` or starts with `<`) and every citation inside a runner-written research-swarm record block; a hand-written citation of a journal file without its date stays red.
answered_by: maintainer
status: answered
context: |
  Topic: the RB-P5 check reports machine-written text as undated journal citations.
  Intention: it turns PR #411 and the runner-stamps-provenance lane red although no one cites a journal file without its date there.
  Today: the test scans every tracked Markdown file for `docs/journal/handover/<target>` and exempts only targets starting with `<`; it flags a JSON-escaped path in the research-swarm record blocks and the glob `docs/journal/handover/*.md` in a review row.
  Repository change: tests/test_provenance.py and a mutation test that goes red when a real undated citation slips through.
  Architecture change: none.
  Options shown: A patterns and runner blocks are exempt (recommended); B only patterns, the runner writes its paths differently; C only the runner changes and the review row is edited.

In the context of the RB-P5 date check, facing reports on machine-written
text that cites no journal file, we decided that patterns and runner-written
record blocks are not citations, to achieve a check that stays red only for a
hand-written undated citation, accepting that a runner block is trusted not
to cite a journal file undated by hand — 2026-11-19

## Decided by the agent

Spec-review round 1 rows, decided by the orchestrator with reasons
(maintainer rule of 2026-11-18: details are decided with reasons; autonomous
run of 2026-11-19: provisional, the maintainer confirms or reverts).

[DETAIL] **S-2 (what `*` means)**: a target is a pattern only when a `*`
remains after trailing Markdown emphasis markers (`*`, `_`) are stripped; an
emphasised concrete path is judged like any other. Reason: Q-1 keeps a
hand-written undated citation red, emphasised or not.

[DETAIL] **S-1 (an elided target)**: a target that is an elision (`…` or
`...`) after the same stripping is a placeholder like `<…>`. Reason: an
elision names no file, so it cannot cite one undated; the case is this
change's own runner-written research.md.

[DETAIL] **S-3, S-4, S-5 (what counts as a runner record)**: only a
well-formed research-swarm/v2 run envelope in a change's `research.md`
(active or archived) is exempt, as a whole, including its runner-written text
outside the fences; well-formed means exactly what
`scripts/check_research_handoff.py` already accepts, read through that one
reader, not a second parser. Any other file, and an envelope the handoff
reader refuses, is scanned as usual. Reason: the runner writes envelopes only
there (WORKFLOW.md), one reader keeps the two checks in step (house rule 9),
and Q-1 meant all machine-written text of the record.

Spec-review round 2 rows, decided by the orchestrator with reasons (same
rule; provisional in the autonomous run of 2026-11-19).

[DETAIL] **S-6, S-7 (stripping)**: before judging a target, trailing
sentence punctuation (`.`, `:`, `!`, `?`, `'s`, `'`) and trailing emphasis
markers (`*`, `_`) are stripped repeatedly, in any order; every listed
condition (empty, `<`, elision, ISO date, remaining `*`) is judged on the
stripped target. A target of markers only (`*`, `**`) is then empty, a
directory mention. Reason: a hand-written emphasised citation stays red, and
a bold directory mention stays a mention.

[DETAIL] **S-8, S-9 (acceptance per file, parse level)**: acceptance is per
file and at parse level: the envelopes of a `research.md` are exempt when
`check_research_handoff.parse_text` reads the file without raising; when it
raises, the whole file is scanned. Reason: one reader unchanged in its
verdict; a file it cannot parse is already red at the research-handoff gate
and must be repaired there, not hidden here.

[DETAIL] **S-10 (where the extents come from)**: the one reader in
`scripts/check_research_handoff.py` additionally returns each run's character
span (from its opening marker to the end of its closing marker); its
existing verdicts and messages do not change, and the journal-date check
uses those spans. This adds `scripts/check_research_handoff.py` and its tests
to the files this change touches. Reason: a second envelope parser would be
the side route house rule 9 forbids.

Spec-review round 3 rows (S-11 BLOCKER, S-12), decided by the orchestrator
as a provisional agent decision in the autonomous run of 2026-11-19 (the
maintainer's rule sends a BLOCKER after round 3 to the maintainer; the grant
for this run allows a provisional decision, marked here for confirmation).
No fourth review round runs (the final-draft rule of mandatory-spec-review
Q-10 and finder-partial-report Q-4).

[DETAIL] **S-11, S-12 (one general normalisation instead of a list)**: the
target is first cut at its last path character: every trailing character
outside the path alphabet `A-Z a-z 0-9 . _ / -` and `*` is dropped (quotes,
typographic apostrophes, punctuation of any kind). Then a trailing run of
`*` or `_` is emphasis only when the part before it ends in a file name with
an extension (`.md`); otherwise a `*` anywhere in the target makes it a
pattern (`2026-11-*`, `coding-harness-*`, `*.md`). Reason: a closed list of
characters invites a new row for every typographic variant; a path alphabet
does not, and a glob stays a glob while an emphasised file stays a citation.

Implementation hand finish, decided by the orchestrator as a provisional
agent decision in the autonomous run of 2026-11-19 (the maintainer asked for
a sustainable fix; the maintainer confirms or reverts).

[DETAIL] **S-13 (a change's findings.md and the failure message)**: three
implement attempts stayed red for one cause outside the code. Review row S-6
in this change's `findings.md` explains the rule with an emphasised, undated
handover path, which the decided normalisation reports; each failed attempt's
runner record then quoted the test's message, which repeated the target, so
every attempt added new hits and no implementation could go green. (a) The
check's failure message names each hit as `<file>:<line>` with one fixed
reason and never repeats the cited target, so quoting a red run into a record
cannot create a new hit. (b) A change's `findings.md` (active or archived) is
a runner record as a whole and is exempt, like the well-formed research-swarm
envelopes; every other file is scanned as before. Reason: review verdicts,
loop rows and attempt records in `findings.md` are written by the runner and
hand repairs only change a Status cell, so Q-1's exemption of runner-written
record blocks covers it; and a message that repeats its own finding makes the
record of a failure a new failure.

Confirmed by the maintainer on 2026-11-20 in the conversation: S-11, S-12
(one general normalisation) and S-13 (a change's `findings.md` is exempt;
the failure message never repeats the target) are no longer provisional, and
so is the orchestrator's hand acceptance of phase-6 rows R-1 and R-2 (the
code under test moves to `scripts/` under bead coding-harness-bf9m).
