---
title: "Decisions — verify-tmp-cleanup"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-12
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, make-verify]
---

# verify-tmp-cleanup — Decisions

Class: bounded (bead coding-harness-bxxt.3; one answered question is owed —
Q-1 below, answered on 2026-11-12; it replaces the interview skip of
2026-11-10 and the plan approved at `e6894adc`).

## Q-1 · Where the cleanup lives and how a killed run is covered

asked: 2026-11-12
answer: "F: eigener Ordner je Lauf (Empfohlen)" — each run of `scripts/verify_all.sh` gets a temporary folder of its own, named after its process id, under one parent folder; the run removes it when it ends and on an interrupt; at its start every run removes the sibling folders whose process is no longer alive. `scripts/verify_lock.py` is not touched.
answered_by: maintainer
status: answered
context: |
  Topic: the change verify-tmp-cleanup (bead coding-harness-bxxt.3), make verify removes its own temporary test folders.
  Intention: three implement attempts of the approved plan failed in the night of 2026-11-11/12; one grew scripts/verify_lock.py by 606 lines. The maintainer asked whether pytest's own retention settings were the smartest fix.
  Today: measured on 2026-11-12 about 08:10 UTC, pytest's temporary root held 707 MB in 7 folders; 4 of them (about 630 MB) came from runs killed in the night and still carried a lock file, which pytest's cleanup skips for 3 days whatever its retention settings say.
  Repository change: about 20 lines in scripts/verify_all.sh, tests for a normal end, an interrupt and an orphan left by a hard kill, and a shorter plan.
  Architecture change: none.

In the context of full checks that leave gigabytes under pytest's temporary
root, facing killed runs whose locked folders pytest keeps for three days and
a first plan that grew the verify lock by hundreds of lines, we decided that
`scripts/verify_all.sh` gives each run a temporary folder named after its
process id, removes it at its end and on an interrupt, and removes the
folders of dead processes at its start, to achieve cleanup for every way a
run can end with about twenty lines in one script, accepting that a folder
left by a hard kill stays until the next run starts — 2026-11-12

## Q-2 · How the cut-off git error is repaired

asked: 2026-11-12
answer: "A: Runner kürzt klüger (Recommended)" — one helper in the runner keeps the start and the end of a git error, at both sites; scripts/stage2.py and one test join the plan's scope; one more runner run.
answered_by: maintainer
status: answered
context: |
  Topic: the change verify-tmp-cleanup (bead coding-harness-bxxt.3), every check run removes its own temporary files.
  Intention: all three runner attempts were rejected; in the last, 3 of 5,664 tests were still red.
  Today: the runner cuts git errors to their first 200 characters (scripts/stage2.py, two sites). The new temporary folder makes paths longer, so the message ends before the reason ("index.lock"). The fault would meet every machine with long paths. 2.8 of 4 hours are used.
  Repository change: a helper of a few lines in scripts/stage2.py, one test, one plan section.
  Architecture change: none.

In the context of a run area that lengthens every temporary path,
facing a runner that cuts a git error before its reason,
we decided that the runner keeps the start and the end of the message,
to achieve a readable reason at any path length,
accepting two files more than the plan first allowed — 2026-11-12

## Q-3 · The cut git error, second approach, and the appetite

asked: 2026-11-12
answer: "A: Erste Zeile ganz (Recommended)" — the runner keeps the first line of git's message whole and drops the hint paragraph; the orchestrator implements it by hand and accepts it by hand; the appetite rises by 2 hours to 6; the full make verify follows before phase 6.
answered_by: maintainer
status: answered
context: |
  Topic: the change verify-tmp-cleanup (bead coding-harness-bxxt.3), every check run removes its own temporary files.
  Intention: the appetite was reached (3.9 of 4 hours) and the correction Q-2 (keep the start and the end of git's message) did not carry.
  Today: git states the reason in its first line, in the middle of the long path, and adds a long hint paragraph after it; start plus end cuts exactly the middle with the reason, so the three tests stayed red. The fourth attempt also did not finish its full check (45-minute step limit on a fully loaded machine). Everything is saved on side refs.
  Repository change: a few lines in scripts/stage2.py, the test adjusted.
  Architecture change: none.

In the context of a runner whose git errors lose their reason behind a long path,
facing a hint paragraph that git appends after the reason line,
we decided to keep git's first line whole and drop the hint,
to achieve a readable reason at any path length,
accepting a hand acceptance of real code and two more hours — 2026-11-12

## Q-4 · The whole git message instead of one line

asked: 2026-11-13
answer: "A: Ganze Meldung (Recommended)" — the runner keeps every non-empty line of git's error output (only blank lines drop); this replaces the first-line rule of Q-3.
answered_by: maintainer
status: answered
context: |
  Topic: the change verify-tmp-cleanup (bead coding-harness-bxxt.3), the runner's git error message.
  Intention: review round 5 brought the third finding of one mechanism: keeping one selected line loses the reason when git puts it on a later line. The repository rule ends case repair at the second finding of a mechanism and fixes it at one place.
  Today: Q-3 chose the first line whole; since then git runs in the C locale and the length cut is gone.
  Repository change: a few lines in scripts/stage2.py, tests, spec criterion 12.
  Architecture change: none.

In the context of git errors whose reason can stand on any line,
facing a third finding against picking one line,
we decided that the runner keeps git's whole error output without blank lines,
to achieve a reason that cannot be lost,
accepting messages that are sometimes a few lines longer — 2026-11-13

## Q-5 · After the repair brake

asked: 2026-11-13
answer: "A: Phase 6 (Recommended)" — the loop ends at the repair brake and the change goes straight to the phase-6 review.
answered_by: maintainer
status: answered
context: |
  Topic: the change verify-tmp-cleanup (bead coding-harness-bxxt.3).
  Intention: the review loop's repair brake stopped it: rounds 5 and 6 accepted only findings caused by earlier repairs.
  Today: every taken row of six rounds is repaired; the runner's last full make verify was green (2026-11-13); about 9 of 6 hours are used.
  Repository change: none from the decision itself.
  Architecture change: none.

In the context of a loop whose last two rounds only found the effects of its own repairs,
facing the repair brake,
we decided to end the loop and go to the phase-6 review,
to achieve a final review without more rounds of polish,
accepting that no further loop round reads the last repair — 2026-11-13

## Q-6 · How the runner keeps pytest inside the run area

asked: 2026-11-13
answer: "Ja" to the plugin solution — a small pytest plugin the runner loads into every pytest run checks, in pytest_configure, the temporary folder pytest itself resolved and stops the run with a clear message when it lies outside this run's area; the runner's own parser for PYTEST_ADDOPTS goes.
answered_by: maintainer
status: answered
context: |
  Topic: the change verify-tmp-cleanup (bead coding-harness-bxxt.3), phase-6 finding F6-1.
  Intention: Codex showed two more spellings (-o=addopts=…, @args.txt) by which a caller can give pytest its own basetemp; the second finding of this mechanism after L2-12.
  Today: the runner parses PYTEST_ADDOPTS to refuse --basetemp; each rule misses the next spelling. Pydantic or Jinja do not help: only pytest knows what it makes of its option sources.
  Repository change: a plugin of about fifteen lines, the parser in scripts/verify_all.sh removed, tests for the spellings.
  Architecture change: none.

In the context of pytest options that arrive through several channels,
facing a parser of our own that misses each new spelling,
we decided that a plugin asks pytest for the temporary folder it resolved and stops a run outside the area,
to achieve one check that covers every spelling,
accepting a plugin loaded into every pytest run of make verify — 2026-11-13

## Decided by the agent

[DETAIL] **The gate command line stays as it is.** The folder is set through
the environment of the run, not by an option in `decisions/gates.yaml`.
Reason: the gate list is a held file and its command is pinned byte for byte
against the Makefile; the exploration found that pytest takes its temporary
root from the environment.

[DETAIL] **Where the removal sits** is decided by Q-1 (2026-11-12): in
`scripts/verify_all.sh`, not in the verify lock's supervised entry as first
written on 2026-11-10.

[DETAIL] **"On request" is one environment variable set by the caller** for a
red run whose folder should stay; nothing is kept by default. Reason: the
bead asks for the request to be explicit, and a default that keeps red runs
is how the volume filled.

[DETAIL] **Scope is the runs that go through `scripts/verify_all.sh`** (the
full check and its job subsets). The runner's own targeted and cheap test
runs are named in the spec as covered or as a stated limit, whichever the
draft finds they share with that entry. Reason: the bead names the full
check; widening silently would be scope the maintainer has not seen.

[DETAIL] **No free-disk check is added here.** Reason: that is its own bead
(coding-harness-87b0).
