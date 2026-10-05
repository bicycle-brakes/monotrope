---
title: "Decisions — research-currency"
status: draft
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-pu9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# research-currency — Decisions

Phase 1a (interview) was skipped: the maintainer set the scope in the
session of 2026-10-05, relayed to this phase by the orchestrating session,
and what stays open is mechanics plus one class question (below).

## What the maintainer decided on 2026-10-05

1. **Two parts, one bead.** A recurring job checks whether the research under
   `docs/research/` is still current: (1) a deterministic list of the notes
   whose last review is too old, report-only, in the nightly `drift` job of
   `.github/workflows/ci.yml`; (2) a recurring agent that re-checks the oldest
   note's dated facts and sources on the web and opens a pull request with an
   addendum (holds / overtaken / new), never editing findings in place and
   never writing the tracker, from a runner-neutral prompt in the repository
   (bead coding-harness-pu9).
2. **This change is part 1 only.** Report-only means it never turns a run
   red.
3. **Part 2 waits.** Its runner waits for the Hermes assessment (bead
   coding-harness-6hx, research in progress on branch
   `docs/research-hermes`). This change may write the runner-neutral contract
   part 2 will need from part 1.

## [DECISION] 1 — the class of this change (answered: `bounded`, 2026-10-05)

The spec author states the class and the maintainer's review of the pull
request holds it (`docs/WORKFLOW.md`, "Change classes, the ADR question and
decision pull requests"). Here both definitions read plausibly, and the choice
decides whether the maintainer is asked the ADR question. It is taken
provisionally with the recommendation, as `adhd-frame` did
(`plans/changes/adhd-frame/spec.md`, "Open decisions").

```text
Goal in one sentence:  Is this change a small addition to the nightly job,
                       or a feature that needs your yes-or-no on "does it
                       need an architecture decision record"?
Options:
  1. bounded.          It adds one list to the existing nightly job and
                       turns no verdict: nothing goes red, nobody has to do
                       anything, one revert removes it.
                       Consequence: no ADR question; `make verify` stays
                       green; your review of the pull request is the only
                       hold on the class.
  2. feature.          It is a deliverable of its own — a new script, a new
                       gate entry, and the output form part 2 will read.
                       Consequence: the spec header gains `change:` and an
                       ADR proposal ("no": one report over existing headers,
                       one gate entry, removed by one revert), and the gate
                       `adr-answers` keeps `make verify` red until you
                       answer — one sentence in the chat, which the
                       orchestrating session records with
                       `python3 scripts/harness.py decide adr`.
Recommendation:        Option 1 — because a list that never turns anything
                       red changes no check and decides nothing for anyone;
                       the ADR question has substance in part 2 (an agent on
                       a schedule, with a runner of its own), not here.
If you say "ok":       `class: bounded` stays in spec.md; nothing else
                       follows.
What is lost:          Option 2 would record your explicit "no ADR" for this
                       change in `decisions/answers/research-currency/adr.yaml`.
```

The weak point of option 1: the sibling change `frontmatter-current` — a
check over the same headers with one gate entry — was a `feature`, answered
"no" on 2026-09-30, and the bead is typed `feature`. The difference: that
check blocks a merge; this list blocks nothing. The bead's type covers part
2 as well.

No second `[DECISION]` is open. The `[DETAIL]`s phase 2 decided stand with
their reasons in `spec.md`, "Open decisions".

## Addendum 2026-10-05: the maintainer answers [DECISION] 1

The maintainer answered in the Claude Code session on 2026-10-05: class
`bounded`, the recommended option — "small addition to the nightly job:
turns nothing red, decides nothing; the ADR question belongs to part 2". The
class is no longer provisional, `class: bounded` stays in `spec.md`, and no
ADR question is asked for this change. The text above stays as it was
written; this addendum changes only its status.
