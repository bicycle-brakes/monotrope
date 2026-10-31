---
title: "Research — time-records-data"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-v6vk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# time records data — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2835 commits, 12 rules.

## Runner exploration — 2026-10-31

The exploration is complete. Here is the research, ready to append to `plans/changes/time-records-data/research.md`.

---

## What exists today

**Two writers share one Markdown section, with one format privileged.** Every change's `plan.md` carries a `## Time used` section; the bytes below it up to the next level-two heading are what all readers see. The section is extracted by `TIME_HEADING` and `time_log()` (`scripts/stage2.py`, `time_log` and `TIME_HEADING`; extraction bound at `time_log` in `scripts/stage2.py` and re-used read-only by `read_time()` in `scripts/run_report.py`). No template file ships the heading — `templates/` contains no `## Time used` match — instead the drafting prompt requires it ("holds a `## Time used` section, empty until phase 4", `scripts/stage2.py` `implementation_prompt` at the draft wording) and the runner refuses to start implement or repair without it (`time_log(ctx.plan)` preflight calls, `scripts/stage2.py`, two sites marked "Require the initial time heading before a model call starts", plus a third preflight site; the missing heading also reaches model diagnostics per `plans/changes/attempt-diagnostics/spec.md`, criteria quoting `plan.md did not add a measured line below ## Time used`).

**Writer 1 — the runner, exactly one line per completed attempt.** `time_entry()` (`scripts/stage2.py`) formats `<start date> <HH:MM:SS>–[<end date> ]<HH:MM:SS> UTC, <N> s — <verb> · attempt <n> · route <route> · model <model> · accepted|rejected · measured by the runner`; the seconds come from the monotonic clock (`monotonic_now`), the UTC endpoints (`utc_now`) only name the span, and the end date appears only across midnight (docstring of `time_entry`). The persistence path is `persist_time_entry()` → `with_time_entry()`, the single writer for normal and exceptional departures: a retried rejected attempt gets its entry onto the trusted pre-call plan (`prior` argument), a rejected attempt whose plan became missing/unreadable/aliased recovers the pre-call plan first, and a failed write fails closed without retry or checkpoint (docstring of `persist_time_entry`, `scripts/stage2.py`). Call sites sit in the attempt loop right after the verdict and the post-gate credential re-scan (`scripts/stage2.py`, the block beginning "The verdict is in: the runner writes the attempt's span"). The contract: exactly one runner entry per completed attempt, kept across restore and retry (`plans/changes/runner-time-line/spec.md` criteria 1–6; `plans/changes/runner-time-line-exits/spec.md` criteria 1–5, bead `coding-harness-9wp` for both). The implementation model itself is barred from writing time entries (`scripts/stage2.py` prompt text "Write no entry under `## Time used` in plan.md: the runner measures this attempt and writes it"; `prompts/04-implement.md` lines at the top: "write no entry under `## Time used`").

**Writer 2 — interactive sessions, prose of their own shape.** `prompts/04-implement.md` ("The appetite is a stop") has the session read `date` at span boundaries and append `<date> <start>–<end>, <span>[, break counted]` under `## Time used`, plus appetite extensions and stop answers ("Write the answer under `## Time used`: the new appetite or narrowed `Done when:`"). This writer-side rule predates and survives the runner-owned measurement: the runner-time-line spec explicitly keeps "interactive sessions' responsibility to read their clock and log their own spans" as a non-goal, and its criterion 7 forbids prompts from demanding model-measured attempt entries. A real record of this second shape with a measured note exists in `plans/changes/run-report/plan.md` `## Time used` (two lines of `… — review loop round N · … · measured with `date -u``) directly beside seven runner entries — the only place in the tree where both shapes sit in one section.

**Reader — one machine reader, one accepted grammar.** `RUNNER_ENTRY` (`scripts/run_report.py`, above `parse_time_line`) full-matches only the runner's format; `parse_time_line` returns `TimeRecord` or `None`; `read_time` sums explicit seconds, skips blank and furniture lines (`FURNITURE`), counts everything else as `unread`, and collects attempt rows (`TimeReading`). The module docstring states the outcome as fact: "Only the runner's own fixed time format counts; every orchestrator time record stays unread" (`scripts/run_report.py` docstring, last sentence). The half-appetite warning reads the opening plan card only (`appetite_seconds`, report-local parser; spec criterion 6–7 in `plans/changes/run-report/spec.md`), and appetite extensions written as prose under the time section are unread records for it.

**How that state was reached — the structural cut.** `plans/changes/run-report/decisions.md` originally recorded summing "the runner's lines and the orchestrator's dated lines alike". The review loop then produced a row sequence about orchestrator records (L1-1 approx prose entering sums; L3-1 annotated orchestrator seconds unread; L4-1 rejected — guard ordering; L5-1 fixed — a whitelist for annotated seconds; L6-1 and L6-2 fixed — the whitelist still missed real shapes: prose between round label and measurement note, minutes-plus-seconds forms, parenthesised notes), ending in the maintainer's structural cut recorded in `plans/changes/run-report/spec.md` criterion 4: "Only that format counts (maintainer, 2026-10-29: a structural cut after loop rows L1-1, L3-1, L4-1, L5-1 and L6-1 about orchestrator prose records)". Criterion 5 makes any non-runner record an `unread lines: N` line with an incomplete subtotal. The phase-6 column of rows L6-1/L6-2 carries reviewer disagreement marks stating orchestrator records are "outside the current accepted format" — the tension is documented, not hidden (`plans/changes/run-report/findings.md`, released loop rows block). The test pinning today's grammar is `tests/test_run_report.py::test_time_records_require_whitelisted_measurement_forms`: it lists roughly twenty invalid annotated/prose variants and accepts exactly one shape, the runner line (test helper `runner_line`). Before the cut, L3-1 had measured the practical effect on the change's own plan: the report summed 6322 s while the section recorded 6444 s, the two orchestrator records (104 s, 18 s) being unread.

**Consumers and entry points.** `make report` runs `@export CHANGE; python3 scripts/run_report.py` (`Makefile`, recipe at the `report:` target; asserted byte-exact by `tests/test_run_report.py::test_make_report_passes_change_as_data_and_is_not_a_gate`, which also asserts reporting is not in `decisions/gates.yaml`). The report imports the runner's own readers instead of copying regexes (`stage2.time_log`, `stage2.CARD_LABELS`, `stage2_runs.CALL_LINE`/`CALL_PREFIXES`; `scripts/run_report.py` import block and `plans/changes/run-report/decisions.md`, first `[DETAIL]`), with one known accepted gap: the appetite parser is report-local because `stage2.card_problem` returns only a problem text (loop row L1-3, rejected as an accepted limit, `plans/changes/run-report/findings.md`). `docs/WORKFLOW.md` documents the report contract in "The run report (`make report`)" (snapshot, not gate; `unread lines: N`; `time not read` never zero) and the runner measurement rule in the Flash-rows paragraph (a line below `## Time used`, "measured by the runner", for rejected attempts too). `scripts/stage2_runs.py` counts loop rows and calls, not time records. Nothing else in `scripts/` or `tests/` parses time records (`time_log(` and `parse_time_line`/`read_time` grep over the worktree return only the sites named above).

## Where it lives

- Writer: `scripts/stage2.py` — `TIME_HEADING`, `time_log`, `utc_now`, `monotonic_now`, `time_entry`, `with_time_entry`, `insert_before_time`, `persist_time_entry`, the two attempt-loop call sites, and the embedded prompt texts (draft prompt, implement prompt line "Write no entry under `## Time used`…").
- Reader: `scripts/run_report.py` — `RUNNER_ENTRY`, `FURNITURE`, `TimeRecord`, `TimeReading`, `parse_time_line`, `read_time`, `appetite_seconds`, and the docstring contract sentence.
- Interactive rules: `prompts/04-implement.md` ("The appetite is a stop" block) and `docs/WORKFLOW.md` (two sections named above).
- Specs: `plans/changes/run-report/spec.md` (criteria 4–7, the structural cut), `plans/changes/runner-time-line/spec.md`, `plans/changes/runner-time-line-exits/spec.md` (both bead `coding-harness-9wp`), `plans/changes/attempt-diagnostics/spec.md` (the missing-heading diagnostics), `plans/changes/codex-drafts/spec.md` (criterion 16, the draft-time heading requirement).
- History: `plans/changes/run-report/findings.md` (loop rows L1-1, L3-1, L4-1, L5-1, L6-1, L6-2 and their phase-6 marks), `plans/changes/run-report/decisions.md`, `plans/changes/run-report/plan.md` (`## Time used` with both shapes).
- Tests: `tests/test_run_report.py` (the grammar test, the unread-visibility test at `test_unread_time_is_visible_and_totals_are_partial`, the make/gate test), `tests/test_stage2.py` (runner-side time tests for the `coding-harness-9wp` changes).
- Origin of the interactive rule: `plans/changes/archive/2026-09-30-adhd-frame/spec.md` (criterion "Time used").

## What is unclear about it

- **The change's own brief is unread.** The bead `coding-harness-v6vk` description — the recorded intent and class of this change — lives in the Dolt tracker under `.beads/`; this explorer runs no command and no rendered copy is committed (repository house rules), so it could not be read here. No handover mentions the change (the newest, `docs/journal/handover/2026-10-29-three-lane-night.md`, predates the folder opened 2026-10-31 in commit `a2646863`), and the string `time-records-data` occurs nowhere in the tree except `plans/INDEX.md` and this change's own skeleton. The interview (phase 1a) needs the bead's wording from someone who can read the tracker.
- **Direction not stated anywhere.** Whether "time records data" means a data representation of time records (storage-side), a wider writer contract (so non-runner records become machine-readable), or a reader-side change is written in no repository artifact. The findings tension above is the documented pressure, but naming a direction here would be design, which this phase does not do.
- **Two statements that are different facts.** Not found: no structured (JSON/YAML/JSONL/sidecar/database) time-record store exists in the repository — the only store is prose in each `plan.md`. Not there: `plans/specs/` holds only `implementation-verification/spec.md`, which contains no time-record statement (grep: no matches), so no living spec owns the time-record format today; ownership is spread over the four active change specs listed above.
- **Status drift to be aware of.** The `run-report` spec frontmatter still reads `status: draft` / `implementation_status: none` (updated 2026-10-29) while its `findings.md` records a phase-6 verdict with released loop rows and its tests exist in the tree — the frontmatter and the findings disagree about how far that change has got.
- The skeleton frontmatter of this research file carries no `class:` declaration and no `neighbours:` header yet; both are owed before a swarm run and only the runner writes them.

## Which files a change would have to touch

Facts about the coupling, not a plan: any change to what time records *are* touches the writer (`scripts/stage2.py`: `time_entry`, `with_time_entry`, `persist_time_entry`, `time_log`, prompt texts), the reader (`scripts/run_report.py`: `RUNNER_ENTRY`, `parse_time_line`, `read_time`), their tests (`tests/test_stage2.py`, `tests/test_run_report.py`), the interactive contract (`prompts/04-implement.md`), and the two `docs/WORKFLOW.md` paragraphs. Coordination facts from the neighbours' own specs: the run-report spec's protected areas declare `scripts/stage2.py` and `scripts/stage2_runs.py` unchanged ("this adds a consumer of their formats"), and the runner-time-line/runner-time-line-exits specs protect `scripts/stage2_availability.py` and routing; a writer- or format-side change therefore overlaps declared protected areas of three active changes, which the interview and spec phases must reconcile. `plans/INDEX.md` is runner-derived and regenerated, never hand-edited.

**Neighbours for the header:** `plans/changes/run-report/spec.md` (o2yc, active) · `plans/changes/runner-time-line/spec.md` (9wp, active) · `plans/changes/runner-time-line-exits/spec.md` (9wp, active) · `plans/changes/attempt-diagnostics/spec.md` (active) · `plans/changes/codex-drafts/spec.md` (active) · `plans/changes/archive/2026-09-30-adhd-frame/spec.md` (archived origin of the interactive rule) · `docs/WORKFLOW.md` (living doctrine, "The run report" and the Flash-rows paragraph).

## Draft gap checks — 2026-10-31

Repository baseline: `275efefd`. These are repository-answerable gaps, not
new maintainer decisions.

- The interview skip now records class `bounded`, the shared-writer remedy,
  existing format and history-preservation policy; the earlier unread brief
  and unstated direction above describe the exploration's earlier state.
- `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent.
  The available plan form is `prompts/03-plan.md`; the existing interview and
  criterion-ledger checks are executable. Do not claim the missing validator
  passed or introduce a replacement in this change.
- `scripts/kit/manifest.yaml` classifies `scripts/harness.py` as travelling
  mechanism, while its fallback for new scripts is repository stock. A new
  shared import therefore needs its own mechanism entry, with portable tests.
  `scripts/ci_gates.py` also inventories non-gate libraries explicitly.
- The runner's existing restoration-safety refusal can intentionally leave
  a completed attempt unwritten. The current regression
  `tests/test_stage2.py::test_runner_early_refusal_recovers_time_destination_safely`
  covers the aliased-parent case; consolidation must preserve this boundary,
  rather than writing through an unsafe destination to satisfy exactly-once.
