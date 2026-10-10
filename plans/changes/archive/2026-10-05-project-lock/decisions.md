---
title: "Decisions — project-lock"
status: accepted
implementation_status: done
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-ei0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# project-lock — Decisions

Phase 1a (interview) was skipped: what the change must deliver was decided by
the maintainer in LakeSwitch's interview and carried here by bead
coding-harness-ei0, and the maintainer said "yes, start" on 2026-10-05,
relayed by the orchestrating session. What stays open is one class question
(below); every other choice is a `[DETAIL]` in [`spec.md`](spec.md) and
[`plan.md`](plan.md).

## Given, not asked again

Confirmed by the maintainer in `lakeswitch-ai`
(`plans/changes/unified-research-and-work-management/decision-interview.md`,
lakeswitch-ai PR #37; research 1):

1. **D-46 (2026-09-21):** Coding Harness gains a project file and a
   hash-locked dependency file, resolves `harness` from the repository root
   for tests and the verifier, and regenerates its derived workflow. "The
   instance lock does not travel; each instance owns its own." The
   foundation supports Python 3.11 from its first release.
2. **D-47 (2026-09-21, corrected 2026-09-22):** one exact Pydantic version,
   2.13.5, with `pydantic-core` 2.46.5; Jinja2 3.1.6; Python 3.11 and 3.12.
3. **D-54 (2026-09-22):** a verification claim lives as a repeatable test
   beside the code; a measurement in a disposable environment is a dated
   observation.
4. **2026-10-05:** start this change now — step 1 of the Now theme
   "LakeSwitch reads Coding Harness" (`ROADMAP.md`); it unblocks
   coding-harness-s6i and, through it, coding-harness-dj9.

## [DECISION] 1 — the class of this change and its ADR answer (answered 2026-10-06: option 1)

The spec author states the class; for a `feature` the maintainer answers the
ADR question (`docs/WORKFLOW.md`, "Change classes, the ADR question and
decision pull requests"). Both definitions read plausibly here, and the
choice decides whether you are asked anything at all. `spec.md` carries the
recommendation provisionally, as `research-currency` and `adhd-frame` did.

```text
Goal in one sentence:  Is this a feature whose "no ADR needed" you confirm in
                       one sentence, or a bounded change you only review?
Options:
  1. feature, ADR "no". It changes how every change is checked: CI runs every
                       gate under Python 3.11 and 3.12, installs refuse a
                       file whose hash differs, and a local `make verify` is
                       red until its environment matches the lock.
                       Consequence: your "no" is recorded in
                       decisions/answers/project-lock/adr.yaml. Until you
                       answer, the gate adr-answers keeps `make verify` red
                       on this branch; the orchestrating session records
                       your sentence with
                       `python3 scripts/harness.py decide adr --stated-in …`.
  2. bounded.          It carries out what you already decided for LakeSwitch
                       (D-46, D-47) and decides nothing new.
                       Consequence: no ADR question; `make verify` green now;
                       your review of the pull request is the only hold on
                       the class.
Recommendation:        Option 1 — because the change adds checks and alters a
                       guard test (the one that wants a gate in every CI job
                       must let the new summary job `verify` through), which
                       is what the feature class has reviewed; the ADR answer
                       is "no", since the architecture was decided in D-45 to
                       D-47 and the foundation's own record belongs to
                       coding-harness-s6i.
If you say "ok":       `class: feature` stays in spec.md with the ADR proposal
                       "no"; the orchestrating session records your answer
                       "no" with the reason from the spec header.
What is lost:          Option 2 keeps `make verify` green without waiting for
                       you and records no ADR answer for this change.
```

Answers: **ok** · **option 2** · **no, because …**.

## Addendum 2026-10-06: LakeSwitch moves to Python 3.12

The maintainer decided on 2026-10-06, after a measurement in a scratch copy
of lakeswitch-ai at `09c9d62` (1,334 tests pass under 3.11 and 3.12; `lakeswitch
verify` byte-identical; no recorded reason for 3.11): LakeSwitch moves to
Python 3.12. That change belongs to the LakeSwitch session (a signed pin in
its `decisions/gates.yaml`, its workflows, and an amendment of its D-46, D-47
and D-54). Until it lands, this change keeps both legs, 3.11 and 3.12, on
every pull request; afterwards a follow-up change reduces Coding Harness's CI
to 3.12 alone.

## Addendum 2026-10-06 (later): finding F-9

Finding F-9 came from the second repair round in a row and went to the
maintainer. The maintainer chose the recommended option on 2026-10-06 (Claude
Code session): add the missing sentence to the note on bead
coding-harness-dj9 (the release builder) — `--require-hashes` needs a hash on
every package, transitive ones included, and a lock without hashes is refused.
Done the same day; no code changed.

## Addendum 2026-10-06 (later): [DECISION] 1 answered

The maintainer answered the ADR question for this change on 2026-10-06 in
the Claude Code session ("Does project-lock need its own ADR?" — "Nein", the
recommended option), recorded in `decisions/answers/project-lock/adr.yaml`
(commit 57ab07f). The ADR question exists only for a `feature`, so the answer
takes option 1: `class: feature` stays in spec.md with the ADR answer "no".
The decision pull request restates the class, and the maintainer's merge
confirms it (ADR 0008).
