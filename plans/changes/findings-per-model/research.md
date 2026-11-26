---
title: "Research — findings-per-model"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-qut1
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-17", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# findings per model — Research

Stage-2 call, 2026-11-17: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1110 files, 4538 commits, 12 rules.

## Runner exploration — 2026-11-17

Research is complete. Here is the phase-1 report, ready to append to `plans/changes/findings-per-model/research.md`.

---

## What exists today

**Per-model attribution at the row level is already built.** Every loop row of the review loop carries the model that raised the finding in its `Reviewer` cell. The row grammar is nine cells — `ID, Severity, Dimension, Origin, Where, Finding, Reviewer, Status, Broke a test` (`ROW_COLUMNS`, `scripts/stage2.py:438`) — and when the runner writes a swarm round it stamps each parsed six-cell reviewer row with the member's name: `numbered.append([ident, *row[1:], member, "", ""])` (`stage2.py`, the round assembly near line 11073). One round is one heading (`## Round N — member1, member2, <date>`, `stage2.py` round-write near line 11108) with one shared id series `L<n>-<k>`, each row's `Reviewer` cell its member's. This shape is pinned by acceptance criterion 2 of the archived change `plans/changes/archive/2026-11-06-loop-until-clean/spec.md` ("the actual model in each row's Reviewer cell") and by the test `test_a_round_is_written_as_its_rung` (`tests/test_stage2.py:8420`, docstring "Criterion 2: the swarm round is one heading, its ids one series, each row's Reviewer cell its member's").

**The attribution survives into the repository.** `release-loop` renders the released block `## Phase 4b — loop rows, released <date>` with the ten-cell table `RELEASED_COLUMNS` (`ROW_COLUMNS` + `Phase 6`, `scripts/stage2.py:439`, rendered in `release_block` near line 4509), so each released row keeps its `Reviewer` cell; the runner's furniture (headings, snapshot line) and the reviewers' prose (`From <member>:` quoted blocks, member failure notes, `<member> reported no finding.`) are carried over by `kept_lines` (`scripts/stage2.py:4469`) with the member labels intact. A live example with six distinct models across four released rounds is `plans/changes/flaky-swarm-leak-test/findings.md:443-477` (reviewers `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `glm-5.3-flash`, `qwen3.8-flash`, `hy3`, `qwen3.7-plus`).

**Where the doctrine is written.** `docs/WORKFLOW.md` §4, "Two columns for every stage-2 change" (`docs/WORKFLOW.md:2082-2091`): "`Reviewer` — the rung that raised the finding (an id of the ladder), Codex, or Opus: who raised it." The root requirement is ADR 0007 decision 1 (`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md:84-90`): "each finding recording its reviewer, whether it was taken and whether it broke a test", with the stop rule "if at least one taken Codex or GLM finding broke a test, stage 2 falls back to Opus 5.5". The column vocabulary in the template: the base table has seven cells and no `Reviewer` column; the stage-2 forms add it (`templates/findings.md:44` base header, `templates/findings.md:111-113` stage-2 headers). Phase-2a and phase-6 rows have no per-row reviewer; their reviewer is named at section level only, by the `Reviewer session: codex <id>` line (`templates/findings.md:124`, `prompts/06-review.md:21`).

**Per-model data that exists but is never aggregated.** `scripts/stage2_runs.py` reads released rows with the runner's own constants (`stage2_runs.py:66-68`, counting code `stage2_runs.py:140-174`) and counts taken / rejected / undecided, `Broke a test: yes`, phase-6 rounds, 2a/6 rows by severity, disagree marks and clean calls — its column list (`COLUMNS`, `stage2_runs.py:69-84`) has no per-reviewer dimension; the `Reviewer` cell is read nowhere in the counter. `scripts/run_report.py` prints each `Stage-2 call` audit line's model field (`CALL_FIELDS` at `run_report.py:76`, printed near line 316) but aggregates nothing per model. The audit lines themselves name the model per call (`call_line`, `scripts/stage2.py:1917-1922`). The ADR 0007 stop-rule evaluation is therefore done by a person reading the rows: "The rule is written, not counted by a script" (`docs/WORKFLOW.md:2104-2105`); the one evaluation note in tree, `docs/research/2026-10-08-stage2-three-runs.md`, counts per run, not per reviewer.

**Related per-member mechanics the records already distinguish:** the duplicate rule keeps one row per member with explicit rejected copies (`prompts/04b-review-loop.md:80-81`); a failed member is named beside the answering members' rows and is no finding (`prompts/04b-review-loop.md:73-74`; failure statement and Flash replacement recording in `scripts/stage2.py`, round assembly near lines 11066 and 11037); triage rewrites only the `Status` cell and cannot touch `Reviewer` (`stage2.py`, `triage` row-editing near lines 8609-8617). Loop rows live outside the repository until release: `~/.local/state/coding-harness/stage2/<change>@<worktree-hash>/loop.md` (`record_base`/`record_dir`, `scripts/stage2.py:3921-3938`).

## Where it lives

- Row grammar and release: `scripts/stage2.py` (`ROW_COLUMNS` 438, `RELEASED_COLUMNS` 439, `ROUND_HEADING` 482, `release_block` ~4509, `kept_lines` 4469, round assembly ~10940-11118).
- Counter: `scripts/stage2_runs.py` (header docstring 1-35, `COLUMNS` 69-84, counting 120-174); its tests `tests/test_stage2_runs.py`; report reader `scripts/run_report.py` with `tests/test_run_report.py`.
- Doctrine and decisions: `docs/WORKFLOW.md` §4 (2082-2131), `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` decision 1, `docs/adr/0021-review-swarms-until-clean.md`, archived spec `plans/changes/archive/2026-11-06-loop-until-clean/spec.md` criterion 2 (90-94).
- Template: `templates/findings.md` (44, 104-143), checked by `tests/test_templates.py:455`.
- Prompt: `prompts/04b-review-loop.md` (52-54 row format, 72-81 member/record rules), `prompts/06-review.md` (21, 44).
- Live examples: `plans/changes/flaky-swarm-leak-test/findings.md:443-477`; `plans/changes/archive/2026-11-06-codex-repairs/findings.md:190+`.

## What is unclear

- **The bead's description was not readable in this session.** The tracker is the Dolt database transported on `refs/dolt/data`; this worktree holds only `.beads/config.yaml`, `.beads/metadata.json` and `.beads/interactions.jsonl` (hydrated store not present), and a search of `docs/journal/` and the tree found `coding-harness-qut1` only in `plans/INDEX.md:598` and the skeleton itself. Which exact scope the bead names is an open question for the interview — the candidates the repository offers: (a) per-model aggregation in the generated count (`stage2_runs.py` columns per `Reviewer`), (b) regrouping the released block in `findings.md` by model, (c) a per-row reviewer for phase-2a/phase-6 rows, (d) something else the bead states.
- Whether the ADR 0007 stop-rule count ("a taken finding of Codex or of a rung broke a test") is meant to become generated rather than person-read is undecided in the tree; `docs/WORKFLOW.md:2104-2105` states the written-not-counted state as current, with no change folder claiming it (`plans/changes/` searched for per-model measurement topics — none found besides this change).
- `model-endpoints.yaml` declares the ladder and cost values (`modelle`, `anfragen_5h`, entry `opencode-go` at `model-endpoints.yaml:179-430`) but no notion of a reviewer display name distinct from the model id; whether ids alone satisfy "who raised it" long-term is not recorded anywhere I read.

## Which files a change would have to touch

- If the count grows per-model columns: `scripts/stage2_runs.py` (the only consumer that could aggregate `Reviewer`), `tests/test_stage2_runs.py`; `docs/WORKFLOW.md` §4 "Measuring the first three stage-2 runs" if the stop-rule count becomes generated.
- If the released block's shape changes: `scripts/stage2.py` (`release_block`, `kept_lines`, `record_rows`, the strict readers and `findings_rows`), `scripts/stage2_runs.py` and `scripts/run_report.py` row readers, `templates/findings.md` reference section, `prompts/04b-review-loop.md`, `prompts/06-review.md`, `docs/WORKFLOW.md` §4, and the pinned tests (`tests/test_stage2.py:8420` and the release tests); the archived criterion (`2026-11-06-loop-until-clean/spec.md` criterion 2) states the current contract such a change would supersede.
- If phase-2a/phase-6 rows gain a reviewer column: `templates/findings.md`, `prompts/02a-spec-review.md`, `prompts/06-review.md`, the phase-6/release parsers in `scripts/stage2.py`, and `scripts/stage2_runs.py` severity counters.

**Suggested neighbours** for the `neighbours:` header: `plans/changes/archive/2026-11-06-loop-until-clean/spec.md`, `plans/changes/swarm-test-speed/spec.md`, `plans/changes/flaky-swarm-leak-test/findings.md`, `templates/findings.md`, `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`, `docs/adr/0021-review-swarms-until-clean.md`.

**Not checked, stated as such:** the bead description itself (see above); `docs/WORKFLOW.md` beyond the targeted sections quoted; the other released `findings.md` files beyond the two read; `scripts/stage2_availability.py` and the availability snapshot's role in reviewer naming (the snapshot I read, `flaky-swarm-leak-test/findings.md:485`, records members only as stage/consumption state).
