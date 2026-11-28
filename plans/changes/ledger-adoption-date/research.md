---
title: "Research — ledger-adoption-date"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-64fa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# ledger adoption date — Research

## Topic (bead coding-harness-64fa)

Class: bounded. check_criterion_ledger.py exempts plans before a hard-coded CUTOFF = 2026-10-11; decision PR #276 (bead coding-harness-wpv) records criterion-ledger: 2026-10-29 in decisions/adoption.yaml, which no code reads yet. Make the gate read the adoption entry (one source). Note: moving from 10-11 to 10-29 widens the exemption to archived plans of 10-11..10-28 without a ledger — state that in the PR.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6213 commits, 12 rules.

## Runner exploration — 2026-11-28

Research for `ledger-adoption-date`, ready to append to `plans/changes/ledger-adoption-date/research.md`. Read-only: I edited nothing.

## What exists today

**The gate's cut-off is a hard-coded constant.** `scripts/check_criterion_ledger.py` sets `CUTOFF = date(2026, 10, 11)` (line 63), with a comment saying that changing it is a governance act stated in `docs/WORKFLOW.md`. `exempt_by_date()` (line 256) exempts an archived plan without a ledger when its single `date: YYYY-MM-DD` header line is `< CUTOFF`. The gate never reads `decisions/`. Its summary line prints the constant as "dated before 2026-10-11 exempt" (`run()`, line 474).

**The adoption record already holds the new day.** `decisions/adoption.yaml` lists `criterion-ledger: 2026-10-29` next to `interview-minimums: 2026-10-08`, `question-context: 2026-10-15` and `research-census: 2026-11-10`. Its header says moving a day is a decision pull request. Nothing in `scripts/` reads the `criterion-ledger` key. The topic cites PR #276 (bead `coding-harness-wpv`) as the origin of the 10-29 value; I did not verify that PR in git history, as my tools do not reach it.

**The reader already exists.** `scripts/adoption.py` exposes `adopted_on(root, gate) -> date` and raises `NotRecorded` for a missing, unreadable, malformed, quoted, impossible or absent-key record. Its docstring already names bead `coding-harness-wpv`. Two gates call it: `scripts/check_interview_minimums.py` (`GATE`, lines 388–389, with `NotRecorded` turned into "NOT MEASURED … exit 3", line 528) and `scripts/check_question_context.py` (lines 345–346, 381). `scripts/research_census.py` (line 178) calls it too. The pattern to follow is therefore in-repo.

**The record reader has its own tests.** `tests/test_adoption.py` builds its own trees in `tmp_path` and asserts `criterion-ledger` reads as `2026-10-11` (line 69). That fixture is independent of the repository's record. `tests/test_this_repository_adoption.py` exists; a grep found no `criterion` or `2026-10-29` in it.

**The kit classifies both files.** `scripts/kit/manifest.yaml` lists `scripts/check_criterion_ledger.py` and `scripts/adoption.py` as mechanism (lines 142, 154), `tests/test_check_criterion_ledger.py` (line 234) and `tests/test_adoption.py` (line 246) as travelling, and `decisions/adoption.yaml` as stock that stays in its repository (line 383).

**The gate is wired as blocking.** `decisions/gates.yaml` (lines 232–241) defines `criterion-ledger` with command `python3 scripts/check_criterion_ledger.py`. `.github/workflows/ci.yml` line 137–139 runs it. `docs/governance/gate-catalog.md` line 72 lists it as `verify`, `block`.

## What is unclear, or not read

- **The two values disagree in the tree.** `decisions/adoption.yaml` says 2026-10-29; the gate constant and `docs/adr/0013-every-criterion-names-its-proof.md` say 2026-10-11, the day of the maintainer's answers. The spike `docs/research/2026-10-29-ledger-gate-instance-trial.md` (lines 80–84) proposed recording `criterion-ledger: 2026-10-11`, which is not what the record now holds.
- **The widening is real and not counted here.** The code exempts `day < CUTOFF`. Moving the effective day from 10-11 to 10-29 exempts archived plans dated 10-11 through 10-28 that carry no ledger. ADR 0013 counted "17 archived plans dated before 2026-10-11" at `e31100f`; I did not count the 10-11–10-28 subset in the current `plans/changes/archive/`.
- **An instance without the record is red, not green.** ADR 0014 (lines 161–162) states that until an instance writes its record, the adoption gate exits 3 and `make verify` is red. The 2026-10-29 spike says the same of the current constant-based gate's exit 3 when `plans/changes/` is absent. The number of instances affected is not counted here.
- **ADR 0014 holds a pending statement.** `docs/adr/0014-a-change-claims-its-adr-files.md` lines 171–172 say "the criterion-ledger gate keeps its own cut-off until bead `coding-harness-wpv` makes it read the record". That sentence becomes stale when the gate reads the record.
- **Whether the current archive has plans in the 10-11–10-28 window** is not measured here.

## Which files a change would have to touch

- `scripts/check_criterion_ledger.py`: remove `CUTOFF` (and the date-based comment at lines 61–63), import `adoption` as the other gates do (`sys.path` insert plus `import adoption`), read the day through `adopted_on(root, "criterion-ledger")`, map `NotRecorded` to "not measured" exit 3 with the record's remedy, and update the module docstring (lines 9–12, 32–34) and the summary text (line 474, 484) that prints the date.
- `tests/test_check_criterion_ledger.py`: the helper `_tree` (line 31) builds trees without `decisions/adoption.yaml`, and no test in the file writes one, so every tree would hit exit 3 unless the fixture writes the record. Tests asserting the 2026-10-11 boundary and the message text (lines 137–157, 400–405) need the new boundary values. The row test (lines 601–609) asserts `"2026-10-11" in row`, and the row sentence (`docs/WORKFLOW.md` line 538) would need the same change.
- `docs/WORKFLOW.md` line 538 (the "Criterion tests" row) and its governance sentence.
- `docs/adr/0014-a-change-claims-its-adr-files.md` lines 171–172 (stale statement), and possibly a note in `docs/adr/0013-every-criterion-names-its-proof.md`, which records 2026-10-11 as its decision date.
- `decisions/adoption.yaml`: no change, because the value 2026-10-29 is already there. Any change to its value is a decision pull request (its own header says so), not part of this change.
- `scripts/kit/manifest.yaml`: no change expected, since both reader and gate already travel as mechanism.
- New test: a reader-based check that the gate refuses to measure without a record, in the style of `tests/test_check_interview_minimums.py` (lines 975–982).
